import logging
import os
import threading
from typing import Optional

from langchain_openai import ChatOpenAI

from Deep_layer.DB_package.Classes import DB_Communication

_client_lock = threading.Lock()
_cached_creds = None


def _positive_int_env(name, default):
    try:
        value = int(os.getenv(name, str(default)))
        return value if value > 0 else default
    except (TypeError, ValueError):
        return default


def load_openai_credentials():
    """Load OpenAI api_key / organization / project from DB (cached)."""
    global _cached_creds
    if _cached_creds is not None:
        return _cached_creds
    with _client_lock:
        if _cached_creds is not None:
            return _cached_creds
        credentials = DB_Communication.DB_Communication().execute_query(
            """
            SELECT
                (SELECT token FROM assistant_sets.tokens
                 WHERE botname = 'Misa' AND platformname = 'Gpt' LIMIT 1) AS api_key,
                (SELECT token FROM assistant_sets.projects
                 WHERE botname = 'Misa' AND platformname = 'Gpt' LIMIT 1) AS project,
                (SELECT token FROM assistant_sets.organizations
                 WHERE botname = 'Misa' AND platformname = 'Gpt' LIMIT 1) AS organization
            """
        )
        if credentials is None or credentials.empty:
            raise RuntimeError('OpenAI credentials are unavailable')
        row = credentials.iloc[0]
        _cached_creds = {
            'api_key': row['api_key'],
            'organization': row['organization'],
            'project': row['project'],
        }
        return _cached_creds


def get_chat_model(
    *,
    temperature: float = 1,
    max_tokens: Optional[int] = None,
    streaming: bool = False,
) -> ChatOpenAI:
    creds = load_openai_credentials()
    model = (os.getenv('OPENAI_CHAT_MODEL') or 'gpt-4o-mini').strip()
    kwargs = {
        'model': model,
        'api_key': creds['api_key'],
        'organization': creds['organization'],
        'temperature': temperature,
        'streaming': streaming,
        'top_p': 1,
        'frequency_penalty': 0,
        'presence_penalty': 0,
    }
    # langchain-openai accepts openai_api_key; project via default_headers if needed
    if creds.get('project'):
        kwargs['default_headers'] = {'OpenAI-Project': str(creds['project'])}
    if max_tokens is not None:
        kwargs['max_tokens'] = max_tokens
    try:
        return ChatOpenAI(**kwargs)
    except TypeError:
        # older langchain-openai may not accept default_headers
        kwargs.pop('default_headers', None)
        return ChatOpenAI(**kwargs)


def build_rag_user_message(text, rag_context):
    import re
    fact_lines = []
    for line in str(rag_context).splitlines():
        line = line.strip()
        if line and re.search(r'\d+[.,]\d+|\$|USD|EUR|₽', line, re.IGNORECASE):
            fact_lines.append(line[:400])
    facts_block = ''
    if fact_lines:
        facts_block = (
            'Ключевые числа из поиска:\n'
            + '\n'.join(f'- {ln}' for ln in fact_lines[:8])
            + '\n\n'
        )
    return (
        f'{facts_block}'
        f'Результаты поиска в интернете:\n\n{rag_context}\n\n'
        f'---\n'
        f'Вопрос: {text}\n\n'
        f'Ответь на вопрос, используя числа и факты из результатов поиска. '
        f'Начни с прямого ответа с цифрами. Укажи источник (URL). '
        f'Запрещено: отказы, «проверьте на сайте», «не могу дать актуальные данные».'
    )


def dialogue_system_prompt(rag_context=None):
    if rag_context:
        return (
            "Ты — ассистент Misa. Отвечай на языке вопроса. "
            "Используй ТОЛЬКО блок «Результаты поиска» в сообщении пользователя. "
            "Если там есть цены, курсы, даты — обязательно укажи их в ответе."
        )
    return (
        "When you output code or structured content, always wrap it in markdown code blocks: "
        "```label\\ncontent\\n```. Use these labels for different frame styles:\n"
        "- Code: python, javascript, typescript, go, rust, java, etc.\n"
        "- json: JSON data\n"
        "- yaml/yml: YAML configs\n"
        "- bash/sh: shell commands\n"
        "- sql: SQL queries\n"
        "- md/markdown: Markdown snippets\n"
        "- diff: file diffs\n"
        "- warning: warnings\n"
        "- error: error messages\n"
        "- quote: citations\n"
        "- output: command output or logs"
    )


def max_output_tokens(is_command_check=False):
    return _positive_int_env(
        'OPENAI_COMMAND_MAX_OUTPUT_TOKENS' if is_command_check else 'OPENAI_MAX_OUTPUT_TOKENS',
        32 if is_command_check else 500,
    )


def max_history_messages():
    return _positive_int_env('OPENAI_MAX_HISTORY_MESSAGES', 20)


def strip_ad_blocks(content):
    import re
    return re.compile(
        r'<<<misa-ad>>>\s*[\s\S]*?\s*<<</misa-ad>>>',
        re.IGNORECASE,
    ).sub('', str(content or '')).strip()


def invoke_llm(text, *, is_command_check=False, rag_context=None, history=None):
    """Synchronous one-shot LLM call (titles, RAG helpers, command checks)."""
    try:
        temperature = 0.2 if rag_context and not is_command_check else (0 if is_command_check else 1)
        model = get_chat_model(
            temperature=temperature,
            max_tokens=max_output_tokens(is_command_check),
            streaming=False,
        )
        from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

        if is_command_check:
            messages = [HumanMessage(content=text)]
        elif rag_context:
            messages = [
                SystemMessage(content=dialogue_system_prompt(rag_context)),
                HumanMessage(content=build_rag_user_message(text, rag_context)),
            ]
        else:
            messages = [SystemMessage(content=dialogue_system_prompt(None))]
            for item in history or []:
                role = item.get('role')
                content = strip_ad_blocks(item.get('content', ''))
                if not content:
                    continue
                if role == 'assistant':
                    messages.append(AIMessage(content=content))
                else:
                    messages.append(HumanMessage(content=content))
            messages.append(HumanMessage(content=text))

        result = model.invoke(messages)
        content = getattr(result, 'content', None) or str(result)
        if isinstance(content, list):
            content = ''.join(
                part.get('text', '') if isinstance(part, dict) else str(part)
                for part in content
            )
        return content
    except Exception as e:
        logging.exception('invoke_llm failed: %s', e)
        return {
            'response': f'Sorry, an error occurred: {str(e)}',
            'error': True,
        }
