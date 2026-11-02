import os
import unittest
from unittest.mock import patch

from Deep_layer.NLP_package.Classes.GPT.Gpt import Gpt, _positive_int_env


class TestGptConfig(unittest.TestCase):
    def setUp(self):
        Gpt._response_cache.clear()

    def tearDown(self):
        Gpt._response_cache.clear()

    def test_positive_integer_from_environment(self):
        with patch.dict(os.environ, {'OPENAI_MAX_OUTPUT_TOKENS': '250'}):
            self.assertEqual(
                _positive_int_env('OPENAI_MAX_OUTPUT_TOKENS', 500),
                250,
            )

    def test_invalid_integer_uses_default(self):
        for value in ('invalid', '0', '-1'):
            with self.subTest(value=value):
                with patch.dict(
                    os.environ,
                    {'OPENAI_MAX_OUTPUT_TOKENS': value},
                ):
                    self.assertEqual(
                        _positive_int_env('OPENAI_MAX_OUTPUT_TOKENS', 500),
                        500,
                    )

    def test_first_turn_cache_normalizes_case_and_spaces(self):
        Gpt._cache_first_turn_response(
            'Купить   автомобиль. Ок.',
            'gpt-4o-mini',
            'cached answer',
        )

        self.assertEqual(
            Gpt._cached_first_turn_response(
                '  купить автомобиль. ок. ',
                'gpt-4o-mini',
            ),
            'cached answer',
        )
        self.assertIsNone(
            Gpt._cached_first_turn_response(
                'Купить автомобиль. Ок.',
                'another-model',
            )
        )


if __name__ == '__main__':
    unittest.main()
