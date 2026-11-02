import unittest
from unittest.mock import patch

from Core_layer.Bot_package.Classes.Monitors.MessageMonitors.MessageMonitor import (
    MessageMonitor,
)
from Deep_layer.RAG_package.Classes.RagService import RagService


class TestLatencyRouting(unittest.TestCase):
    def test_regular_request_skips_command_model_call(self):
        with patch.object(
            MessageMonitor._gpta,
            'answer',
            side_effect=AssertionError('command classifier must not call OpenAI'),
        ):
            self.assertFalse(MessageMonitor.check('Купить автомобиль. Ок.', 'user'))

    def test_supported_command_is_detected_locally(self):
        self.assertTrue(MessageMonitor.check('Нарисуй рыжего кота', 'user'))
        self.assertTrue(MessageMonitor.check('Найди в интернете курс доллара', 'user'))

    def test_regular_request_skips_rag_model_call(self):
        with patch.object(
            RagService._gpta,
            'answer',
            side_effect=AssertionError('RAG decision must not call OpenAI'),
        ):
            self.assertFalse(
                RagService._needs_web_search(
                    'Расскажи, как выбрать автомобиль',
                    'user',
                )
            )

    def test_realtime_and_explicit_search_use_rag(self):
        self.assertTrue(
            RagService._needs_web_search('Какая цена биткоина сейчас?', 'user')
        )
        self.assertTrue(
            RagService._needs_web_search(
                'Проверь в интернете статистику продаж',
                'user',
            )
        )


if __name__ == '__main__':
    unittest.main()
