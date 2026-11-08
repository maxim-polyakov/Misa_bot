import logging
import re
from typing import Optional

from langgraph.graph import END, START, StateGraph

from Core_layer.Generation_package.openai_factory import (
    build_rag_user_message,
    dialogue_system_prompt,
    get_chat_model,
    max_history_messages,
    max_output_tokens,
    strip_ad_blocks,
)
from Core_layer.Generation_package.state import DialogueState

_SUPPORTED_COMMAND = re.compile(
    r'(?:^|[.!?]\s*)'
    r'(?:абонируй(?:ся)?|нарисуй|нарисовать|изобрази|draw|'
    r'атакуй|атаковать|фас|пиздани|'
    r'найди\s+(?:в\s+)?(?:интернете|google|гугле|википедии)|'
    r'поищи\s+(?:в\s+)?(?:интернете|google|гугле|википедии)|'
    r'предскажи\s+погоду|скажи\s+погоду)\b',
    re.IGNORECASE | re.UNICODE,
)

_AD_BLOCK = re.compile(
    r'<<<misa-ad>>>\s*[\s\S]*?\s*<<</misa-ad>>>',
    re.IGNORECASE,
)


def is_command_text(text: str) -> bool:
    return bool(_SUPPORTED_COMMAND.search(str(text or '')))


def _load_history(user: str, chat_id: Optional[str], exclude_last: int = 0):
    if not chat_id:
        return []
    try:
        from Core_layer.Chat_package.Classes.ChatService import ChatService
        messages = ChatService.get_messages(chat_id) or []
        if exclude_last > 0:
            messages = messages[:-exclude_last]
        history = []
        for item in messages:
            role = 'assistant' if str(item.get('user', '')).strip() == 'Misa' else 'user'
            content = strip_ad_blocks(item.get('content', ''))
            if content:
                history.append({'role': role, 'content': content})
        limit = max_history_messages()
        if len(history) > limit:
            history = history[-limit:]
        return history
    except Exception as e:
        logging.warning('generation._load_history failed: %s', e)
        return []


def route_node(state: DialogueState) -> DialogueState:
    text = str(state.get('text') or '')
    route = 'command' if is_command_text(text) else 'dialogue'
    history = list(state.get('history') or [])
    if not history and state.get('chat_id'):
        exclude_last = 2 if state.get('update_message_id') else 0
        history = _load_history(state.get('user') or '', state.get('chat_id'), exclude_last)
    return {
        **state,
        'route': route,
        'history': history,
    }


def _route_edge(state: DialogueState) -> str:
    return 'command' if state.get('route') == 'command' else 'retrieve'


def command_node(state: DialogueState) -> DialogueState:
    commands = state.get('commands')
    text = str(state.get('text') or '')
    user = state.get('user') or ''
    answer = ''
    if commands is not None:
        try:
            answer = str(commands.analyse(text, user) or '')
        except Exception as e:
            logging.exception('generation.command_node failed: %s', e)
            answer = ''
    return {
        **state,
        'answer': answer,
        'rag_context': None,
    }


def retrieve_node(state: DialogueState) -> DialogueState:
    text = str(state.get('text') or '')
    user = state.get('user') or ''
    chat_id = state.get('chat_id')
    rag_context = None
    try:
        from Deep_layer.RAG_package.Classes.RagService import RagService
        rag_context = RagService.enrich_query(text, user, chat_id=chat_id)
        if not rag_context:
            logging.warning('generation.retrieve_node: empty rag_context for: %s', text[:80])
    except Exception as e:
        logging.warning('generation.retrieve_node failed: %s', e)
    return {
        **state,
        'rag_context': rag_context,
    }


def _lc_messages(state: DialogueState):
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    text = str(state.get('text') or '')
    rag_context = state.get('rag_context')
    messages = [SystemMessage(content=dialogue_system_prompt(rag_context))]
    if rag_context:
        messages.append(HumanMessage(content=build_rag_user_message(text, rag_context)))
        return messages

    for item in state.get('history') or []:
        content = strip_ad_blocks(item.get('content', ''))
        if not content:
            continue
        if item.get('role') == 'assistant':
            messages.append(AIMessage(content=content))
        else:
            messages.append(HumanMessage(content=content))
    messages.append(HumanMessage(content=text))
    return messages


async def generate_node(state: DialogueState, config=None) -> DialogueState:
    from langchain_core.messages import AIMessageChunk

    rag_context = state.get('rag_context')
    temperature = 0.2 if rag_context else 1
    model = get_chat_model(
        temperature=temperature,
        max_tokens=max_output_tokens(False),
        streaming=True,
    )
    messages = _lc_messages(state)
    token_queue = None
    if config:
        configurable = config.get('configurable') or {}
        token_queue = configurable.get('token_queue')

    answer_parts = []
    try:
        async for chunk in model.astream(messages):
            content = getattr(chunk, 'content', None)
            if content is None and isinstance(chunk, AIMessageChunk):
                content = chunk.content
            if isinstance(content, list):
                content = ''.join(
                    part.get('text', '') if isinstance(part, dict) else str(part)
                    for part in content
                )
            if not content:
                continue
            answer_parts.append(str(content))
            if token_queue is not None:
                try:
                    token_queue.put_nowait(str(content))
                except Exception:
                    pass
    except Exception as e:
        logging.exception('generation.generate_node failed: %s', e)
        return {
            **state,
            'answer': f'Sorry, an error occurred: {str(e)}',
        }

    answer = ''.join(answer_parts)
    return {
        **state,
        'answer': answer,
    }


def ads_node(state: DialogueState) -> DialogueState:
    answer = str(state.get('answer') or '')
    if state.get('skip_ads') or not answer.strip():
        return state
    if answer.startswith('http') or answer.startswith('/images/'):
        return state
    try:
        from Deep_layer.API_package.Classes.GradiusService import GradiusService
        enriched = GradiusService.enrich_assistant_answer(
            chat_id=state.get('gradius_chat_id') or state.get('chat_id') or 'unknown',
            user_id=state.get('gradius_user_id') or state.get('user') or 'anonymous',
            text=answer,
            platform=state.get('platform') or 'web',
            existing_ad_count=int(state.get('existing_ad_count') or 0),
        )
        return {**state, 'answer': enriched}
    except Exception as e:
        logging.warning('generation.ads_node failed: %s', e)
        return state


def persist_node(state: DialogueState) -> DialogueState:
    if not state.get('should_persist'):
        return state
    chat_id = state.get('chat_id')
    answer = str(state.get('answer') or '')
    if not chat_id or not answer:
        return state

    is_img = answer.startswith('http') or answer.startswith('/images/')
    try:
        from Core_layer.Chat_package.Classes.ChatService import ChatService
        update_id = state.get('update_message_id')
        if update_id:
            ChatService.update_message_content(chat_id, update_id, answer, is_img)
            return {
                **state,
                'message_id': str(update_id),
                'is_image': is_img,
            }
        message_id = ChatService.save_message(chat_id, 'Misa', answer, is_image=is_img)
        return {
            **state,
            'message_id': str(message_id) if message_id is not None else None,
            'is_image': is_img,
        }
    except Exception as e:
        logging.exception('generation.persist_node failed: %s', e)
        return state


def build_dialogue_graph():
    graph = StateGraph(DialogueState)
    graph.add_node('route', route_node)
    graph.add_node('command', command_node)
    graph.add_node('retrieve', retrieve_node)
    graph.add_node('generate', generate_node)
    graph.add_node('ads', ads_node)
    graph.add_node('persist', persist_node)

    graph.add_edge(START, 'route')
    graph.add_conditional_edges(
        'route',
        _route_edge,
        {
            'command': 'command',
            'retrieve': 'retrieve',
        },
    )
    graph.add_edge('command', 'ads')
    graph.add_edge('retrieve', 'generate')
    graph.add_edge('generate', 'ads')
    graph.add_edge('ads', 'persist')
    graph.add_edge('persist', END)
    return graph.compile()


_compiled_graph = None


def get_dialogue_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_dialogue_graph()
    return _compiled_graph
