import asyncio
import logging
import os
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any, AsyncIterator, Callable, Optional

from Core_layer.Generation_package.graph import get_dialogue_graph, is_command_text
from Core_layer.Generation_package.openai_factory import invoke_llm
from Deep_layer.API_package.Classes.GradiusService import GradiusService

_executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix='misa-generation')


def _chunk_batch_interval_ms() -> float:
    try:
        value = float(os.getenv('STREAM_CHUNK_BATCH_MS', '40'))
        return value if value > 0 else 40.0
    except (TypeError, ValueError):
        return 40.0


class GenerationService:
    """LangGraph-backed dialogue generation for web streaming and bot final replies."""

    @classmethod
    def answer_once(
        cls,
        text,
        user,
        is_command_check=False,
        chat_id=None,
        rag_context=None,
        history=None,
    ):
        """Compatibility helper for titles / RAG helpers / command micro-calls."""
        return invoke_llm(
            text,
            is_command_check=is_command_check,
            rag_context=rag_context,
            history=history,
        )

    @classmethod
    def _gradius_ids(cls, message, user, pltype, chat_id=None):
        source_user_id = str(user or '').strip() or 'anonymous'
        if pltype == 'telegram':
            from_user = getattr(message, 'from_user', None)
            if from_user is not None and getattr(from_user, 'id', None) is not None:
                source_user_id = str(from_user.id)
        platform = 'web' if pltype == 'server' else pltype
        gradius_chat_id = (
            str(chat_id).strip()
            if chat_id
            else f'{platform}_{source_user_id}'
        )
        gradius_user_id = GradiusService.pseudonymous_user_id(
            user_id=source_user_id,
            chat_id=gradius_chat_id,
            platform=platform,
        )
        return gradius_chat_id, gradius_user_id, platform

    @classmethod
    def _existing_ad_count(cls, pltype, chat_id):
        if pltype != 'server' or not chat_id:
            return 0
        try:
            from Core_layer.Chat_package.Classes.ChatService import ChatService
            return ChatService.count_native_ads(chat_id)
        except Exception:
            return 0

    @classmethod
    def _initial_state(
        cls,
        *,
        text: str,
        user: str,
        chat_id: Optional[str],
        pltype: str,
        message: Any = None,
        commands: Any = None,
        should_persist: bool = False,
        update_message_id: Optional[str] = None,
        stream_id: Optional[str] = None,
        skip_ads: bool = False,
    ):
        gradius_chat_id, gradius_user_id, platform = cls._gradius_ids(
            message, user, pltype, chat_id=chat_id
        )
        return {
            'text': text,
            'user': user,
            'chat_id': chat_id,
            'pltype': pltype,
            'platform': platform,
            'message': message,
            'commands': commands,
            'gradius_chat_id': gradius_chat_id,
            'gradius_user_id': gradius_user_id,
            'existing_ad_count': cls._existing_ad_count(pltype, chat_id),
            'should_persist': should_persist,
            'update_message_id': update_message_id,
            'stream_id': stream_id or str(uuid.uuid4()),
            'skip_ads': skip_ads,
            'history': [],
            'answer': '',
            'is_image': False,
        }

    @classmethod
    def _track_user(cls, state):
        try:
            GradiusService.track_user_message(
                chat_id=state['gradius_chat_id'],
                user_id=state['gradius_user_id'],
                text=str(state.get('text') or ''),
                platform=state.get('platform') or 'web',
            )
        except Exception as e:
            logging.warning('GenerationService track_user failed: %s', e)

    @classmethod
    async def ainvoke(
        cls,
        *,
        text: str,
        user: str,
        chat_id: Optional[str] = None,
        pltype: str = 'server',
        message: Any = None,
        commands: Any = None,
        should_persist: bool = False,
        update_message_id: Optional[str] = None,
        token_queue: Optional[asyncio.Queue] = None,
        skip_ads: bool = False,
    ) -> dict:
        state = cls._initial_state(
            text=text,
            user=user,
            chat_id=chat_id,
            pltype=pltype,
            message=message,
            commands=commands,
            should_persist=should_persist,
            update_message_id=update_message_id,
            skip_ads=skip_ads,
        )
        await asyncio.to_thread(cls._track_user, state)
        graph = get_dialogue_graph()
        config = {'configurable': {}}
        if token_queue is not None:
            config['configurable']['token_queue'] = token_queue
        result = await graph.ainvoke(state, config=config)
        if token_queue is not None:
            await token_queue.put(None)
        return result

    @classmethod
    def invoke_sync(
        cls,
        *,
        text: str,
        user: str,
        chat_id: Optional[str] = None,
        pltype: str = 'server',
        message: Any = None,
        commands: Any = None,
        should_persist: bool = False,
        update_message_id: Optional[str] = None,
        skip_ads: bool = False,
    ) -> dict:
        coro = cls.ainvoke(
            text=text,
            user=user,
            chat_id=chat_id,
            pltype=pltype,
            message=message,
            commands=commands,
            should_persist=should_persist,
            update_message_id=update_message_id,
            skip_ads=skip_ads,
        )
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(coro)
        future = _executor.submit(lambda: asyncio.run(coro))
        return future.result()

    @classmethod
    async def astream_tokens(
        cls,
        *,
        text: str,
        user: str,
        chat_id: Optional[str] = None,
        pltype: str = 'server',
        message: Any = None,
        commands: Any = None,
        should_persist: bool = True,
        update_message_id: Optional[str] = None,
        on_start: Optional[Callable[[str], Any]] = None,
        on_chunk: Optional[Callable[[str, int], Any]] = None,
        on_end: Optional[Callable[[dict], Any]] = None,
        on_error: Optional[Callable[[Exception], Any]] = None,
    ) -> dict:
        """Run graph while emitting batched token deltas for WebSocket clients."""
        stream_id = str(uuid.uuid4())
        if on_start:
            maybe = on_start(stream_id)
            if asyncio.iscoroutine(maybe):
                await maybe

        # Commands / media paths: no token stream, just final result.
        if is_command_text(text):
            try:
                result = await cls.ainvoke(
                    text=text,
                    user=user,
                    chat_id=chat_id,
                    pltype=pltype,
                    message=message,
                    commands=commands,
                    should_persist=should_persist,
                    update_message_id=update_message_id,
                )
                result = {**result, 'stream_id': stream_id}
                if on_end:
                    maybe = on_end(result)
                    if asyncio.iscoroutine(maybe):
                        await maybe
                return result
            except Exception as e:
                if on_error:
                    maybe = on_error(e)
                    if asyncio.iscoroutine(maybe):
                        await maybe
                raise

        queue: asyncio.Queue = asyncio.Queue()
        task = asyncio.create_task(
            cls.ainvoke(
                text=text,
                user=user,
                chat_id=chat_id,
                pltype=pltype,
                message=message,
                commands=commands,
                should_persist=should_persist,
                update_message_id=update_message_id,
                token_queue=queue,
            )
        )
        sequence = 0
        batch = []
        last_flush = time.monotonic()
        interval = _chunk_batch_interval_ms() / 1000.0

        async def flush():
            nonlocal sequence, batch, last_flush
            if not batch or not on_chunk:
                batch = []
                last_flush = time.monotonic()
                return
            delta = ''.join(batch)
            batch = []
            last_flush = time.monotonic()
            sequence += 1
            maybe = on_chunk(delta, sequence)
            if asyncio.iscoroutine(maybe):
                await maybe

        try:
            while True:
                try:
                    item = await asyncio.wait_for(queue.get(), timeout=interval)
                except asyncio.TimeoutError:
                    await flush()
                    if task.done() and queue.empty():
                        break
                    continue
                if item is None:
                    await flush()
                    break
                batch.append(item)
                if time.monotonic() - last_flush >= interval:
                    await flush()
            result = await task
            result = {**result, 'stream_id': stream_id}
            if on_end:
                maybe = on_end(result)
                if asyncio.iscoroutine(maybe):
                    await maybe
            return result
        except Exception as e:
            if not task.done():
                task.cancel()
            if on_error:
                maybe = on_error(e)
                if asyncio.iscoroutine(maybe):
                    await maybe
            raise
