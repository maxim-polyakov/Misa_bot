import unittest

from Core_layer.Bot_package.Classes.response_utils import (
    clean_command_response,
    extract_image_url,
    is_image_url,
)


class TestResponseUtils(unittest.TestCase):
    """Isolated tests for command response parsing."""

    def test_extracts_image_url_before_command_marker(self):
        response = "https://cdn.example.test/images/cat.webp|command|\nignored"

        self.assertEqual(
            extract_image_url(response),
            "https://cdn.example.test/images/cat.webp",
        )
        self.assertTrue(is_image_url(response))

    def test_clean_command_response_discards_empty_segments(self):
        response = " first answer |command|\n |command| second answer "

        self.assertEqual(
            clean_command_response(response),
            ["first answer", "second answer"],
        )


if __name__ == "__main__":
    unittest.main()
