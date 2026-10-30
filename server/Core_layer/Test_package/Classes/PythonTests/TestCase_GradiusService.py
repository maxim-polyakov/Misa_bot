import os
import unittest
from unittest.mock import patch

from Deep_layer.API_package.Classes.GradiusService import GradiusService


class TestCase_GradiusService(unittest.TestCase):
    def test_user_id_is_stable_inside_chat_and_different_between_chats(self):
        with patch.dict(os.environ, {'GRADIUS_USER_ID_SECRET': 'test-secret'}):
            first = GradiusService.pseudonymous_user_id(
                user_id='user@example.com',
                chat_id='chat-1',
                platform='web',
            )
            repeated = GradiusService.pseudonymous_user_id(
                user_id='user@example.com',
                chat_id='chat-1',
                platform='web',
            )
            second_chat = GradiusService.pseudonymous_user_id(
                user_id='user@example.com',
                chat_id='chat-2',
                platform='web',
            )

        self.assertEqual(first, repeated)
        self.assertNotEqual(first, second_chat)
        self.assertTrue(first.startswith('misa_'))
        self.assertNotIn('user@example.com', first)

    def test_different_users_do_not_share_id_in_same_chat(self):
        with patch.dict(os.environ, {'GRADIUS_USER_ID_SECRET': 'test-secret'}):
            first = GradiusService.pseudonymous_user_id(
                user_id='user-1',
                chat_id='shared-chat',
                platform='web',
            )
            second = GradiusService.pseudonymous_user_id(
                user_id='user-2',
                chat_id='shared-chat',
                platform='web',
            )

        self.assertNotEqual(first, second)


if __name__ == '__main__':
    unittest.main()
