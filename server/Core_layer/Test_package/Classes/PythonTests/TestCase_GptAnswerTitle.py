import unittest
from unittest.mock import patch

from Core_layer.Answer_package.Classes.GptAnswer import GptAnswer


class TestGptAnswerTitle(unittest.TestCase):
    def test_contextual_title_excludes_advertising(self):
        messages = [
            {'user': 'User', 'content': 'Как выбрать автомобиль?'},
            {
                'user': 'Misa',
                'content': (
                    'Сравните расход топлива и безопасность.\n\n'
                    '<<<misa-ad>>>\nСекретная реклама автомобиля\n'
                    '<<</misa-ad>>>'
                ),
            },
        ]

        with patch.object(
            GptAnswer._GptAnswer__gpt,
            'generate',
            return_value='Выбор автомобиля',
        ) as generate:
            title = GptAnswer.generate_chat_title(messages)

        prompt = generate.call_args.args[0]
        self.assertEqual(title, 'Выбор автомобиля')
        self.assertIn('Сравните расход топлива и безопасность.', prompt)
        self.assertNotIn('Секретная реклама автомобиля', prompt)
        self.assertNotIn('misa-ad', prompt)

    def test_ad_only_content_is_not_used_for_title(self):
        with patch.object(
            GptAnswer._GptAnswer__gpt,
            'generate',
        ) as generate:
            title = GptAnswer.generate_chat_title_from_message(
                '<<<misa-ad>>>Реклама<<</misa-ad>>>'
            )

        self.assertIsNone(title)
        generate.assert_not_called()


if __name__ == '__main__':
    unittest.main()
