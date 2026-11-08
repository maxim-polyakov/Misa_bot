import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from Core_layer.Generation_package.service import GenerationService


class TestCase_StreamProtocol(unittest.TestCase):
    def test_astream_tokens_emits_start_chunk_end(self):
        async def _run():
            events = []

            async def on_start(sid):
                events.append(('start', sid))

            async def on_chunk(delta, sequence):
                events.append(('chunk', delta, sequence))

            async def on_end(result):
                events.append(('end', result.get('answer'), result.get('stream_id')))

            async def fake_ainvoke(**kwargs):
                queue = kwargs.get('token_queue')
                if queue is not None:
                    await queue.put('Hel')
                    await queue.put('lo')
                    await queue.put(None)
                return {'answer': 'Hello', 'message_id': '7'}

            with patch.object(GenerationService, 'ainvoke', new=fake_ainvoke):
                with patch(
                    'Core_layer.Generation_package.service.is_command_text',
                    return_value=False,
                ):
                    result = await GenerationService.astream_tokens(
                        text='hi',
                        user='u',
                        chat_id='c1',
                        should_persist=False,
                        on_start=on_start,
                        on_chunk=on_chunk,
                        on_end=on_end,
                    )

            self.assertEqual(result['answer'], 'Hello')
            self.assertEqual(events[0][0], 'start')
            chunk_events = [e for e in events if e[0] == 'chunk']
            self.assertTrue(chunk_events)
            self.assertEqual(''.join(e[1] for e in chunk_events), 'Hello')
            self.assertEqual(events[-1][0], 'end')
            self.assertEqual(events[-1][1], 'Hello')

        asyncio.run(_run())

    def test_command_path_skips_chunks(self):
        async def _run():
            events = []

            async def on_start(sid):
                events.append('start')

            async def on_chunk(delta, sequence):
                events.append('chunk')

            async def on_end(result):
                events.append('end')

            async def fake_ainvoke(**kwargs):
                return {'answer': 'img', 'message_id': '1'}

            with patch.object(GenerationService, 'ainvoke', new=fake_ainvoke):
                with patch(
                    'Core_layer.Generation_package.service.is_command_text',
                    return_value=True,
                ):
                    await GenerationService.astream_tokens(
                        text='нарисуй кота',
                        user='u',
                        should_persist=False,
                        on_start=on_start,
                        on_chunk=on_chunk,
                        on_end=on_end,
                    )

            self.assertEqual(events, ['start', 'end'])

        asyncio.run(_run())


if __name__ == '__main__':
    unittest.main()
