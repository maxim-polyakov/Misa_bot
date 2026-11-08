import unittest
from unittest.mock import patch

from Core_layer.Generation_package.graph import (
    ads_node,
    is_command_text,
    persist_node,
    route_node,
)
from Core_layer.Generation_package.service import GenerationService


class TestCase_GenerationGraph(unittest.TestCase):
    def test_is_command_text_draw(self):
        self.assertTrue(is_command_text('нарисуй кота'))
        self.assertFalse(is_command_text('какая погода в Москве?'))

    def test_route_node_command(self):
        state = route_node({'text': 'нарисуй собаку', 'history': []})
        self.assertEqual(state['route'], 'command')

    def test_route_node_dialogue(self):
        state = route_node({'text': 'расскажи анекдот', 'history': []})
        self.assertEqual(state['route'], 'dialogue')

    def test_ads_node_skips_when_disabled(self):
        state = {'answer': 'hello', 'skip_ads': True}
        out = ads_node(state)
        self.assertEqual(out['answer'], 'hello')

    def test_persist_node_respects_flag(self):
        out = persist_node({'should_persist': False, 'answer': 'x', 'chat_id': '1'})
        self.assertNotIn('message_id', out)

    @patch('Core_layer.Chat_package.Classes.ChatService.ChatService.save_message', return_value=42)
    def test_persist_node_saves(self, save_mock):
        out = persist_node({
            'should_persist': True,
            'answer': 'final answer',
            'chat_id': 'chat-1',
        })
        self.assertEqual(out['message_id'], '42')
        save_mock.assert_called_once()

    def test_answer_once_command_check_uses_factory(self):
        with patch(
            'Core_layer.Generation_package.service.invoke_llm',
            return_value='True',
        ) as invoke:
            result = GenerationService.answer_once('q', 'u', is_command_check=True)
            self.assertEqual(result, 'True')
            invoke.assert_called_once()


if __name__ == '__main__':
    unittest.main()
