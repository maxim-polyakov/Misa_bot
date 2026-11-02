import os
import threading
import unittest
from itertools import count
from unittest.mock import patch

from Deep_layer.API_package.Classes.GradiusService import GradiusService


class TestCase_GradiusService(unittest.TestCase):
    def test_request_timeout_is_configurable_and_bounded(self):
        with patch.dict(
            os.environ,
            {'GRADIUS_REQUEST_TIMEOUT_SECONDS': '6.5'},
        ):
            self.assertEqual(GradiusService.request_timeout(), 6.5)
        for value in ('invalid', '0', '-1'):
            with self.subTest(value=value), patch.dict(
                os.environ,
                {'GRADIUS_REQUEST_TIMEOUT_SECONDS': value},
            ):
                self.assertEqual(GradiusService.request_timeout(), 8.0)

    def test_ad_return_target_is_configurable_and_bounded(self):
        with patch.dict(os.environ, {'GRADIUS_ADS_BEFORE_RETURN': '7'}):
            self.assertEqual(GradiusService.ads_before_return(), 7)
        for value in ('invalid', '0', '-1'):
            with self.subTest(value=value), patch.dict(
                os.environ,
                {'GRADIUS_ADS_BEFORE_RETURN': value},
            ):
                self.assertEqual(GradiusService.ads_before_return(), 1)

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

    def test_insert_native_ads_respects_remaining_chat_limit(self):
        placements = [
            {
                'type': 'native-text-ad',
                'content': {'content': f'ad-{index}', 'insert_index': index},
            }
            for index in range(3)
        ]

        result = GradiusService.insert_native_ads('answer', placements, max_ads=2)

        self.assertEqual(result.count('<<<misa-ad>>>'), 2)
        self.assertIn('ad-0', result)
        self.assertIn('ad-1', result)
        self.assertNotIn('ad-2', result)

    def test_enrichment_skips_request_after_ten_ads_in_chat(self):
        with patch.dict(
            os.environ,
            {
                'GRADIUS_API_KEY': 'test-key',
                'GRADIUS_MAX_ADS_PER_CHAT': '10',
            },
        ), patch.object(GradiusService, '_request') as request:
            result = GradiusService.enrich_assistant_answer(
                chat_id='chat-1',
                user_id='user-1',
                text='answer',
                existing_ad_count=10,
            )

        self.assertEqual(result, 'answer')
        request.assert_not_called()

    def test_enrichment_collects_ten_test_api_responses(self):
        def placement(*args, **kwargs):
            index = request.call_count
            return [{
                'type': 'native-text-ad',
                'content': {'content': f'ad-{index}', 'insert_index': index},
            }]

        with patch.dict(
            os.environ,
            {
                'GRADIUS_API_KEY': 'test-key',
                'GRADIUS_MAX_ADS_PER_CHAT': '10',
                'GRADIUS_REQUESTS_PER_ANSWER': '10',
                'GRADIUS_ADS_BEFORE_RETURN': '10',
            },
        ), patch.object(GradiusService, '_request', side_effect=placement) as request:
            result = GradiusService.enrich_assistant_answer(
                chat_id='chat-1',
                user_id='user-1',
                text='answer',
            )

        self.assertEqual(request.call_count, 10)
        self.assertEqual(result.count('<<<misa-ad>>>'), 10)

    def test_late_ad_responses_are_available_for_background_save(self):
        release_late = threading.Event()
        indexes = count()

        def placement(*args, **kwargs):
            index = next(indexes)
            if index > 0:
                release_late.wait(timeout=2)
            return [{
                'type': 'native-text-ad',
                'content': {'content': f'ad-{index}', 'insert_index': index},
            }]

        with patch.dict(
            os.environ,
            {
                'GRADIUS_API_KEY': 'test-key',
                'GRADIUS_MAX_ADS_PER_CHAT': '10',
                'GRADIUS_REQUESTS_PER_ANSWER': '10',
                'GRADIUS_ADS_BEFORE_RETURN': '1',
            },
        ), patch.object(GradiusService, '_request', side_effect=placement) as request:
            initial = GradiusService.enrich_assistant_answer(
                chat_id='background-chat',
                user_id='user-1',
                text='answer',
                platform='web',
            )
            completion = GradiusService.pop_pending_enrichment(
                'background-chat'
            )
            release_late.set()
            complete = completion.result(timeout=3)

        self.assertEqual(request.call_count, 10)
        self.assertGreaterEqual(initial.count('<<<misa-ad>>>'), 1)
        self.assertEqual(complete.count('<<<misa-ad>>>'), 10)


if __name__ == '__main__':
    unittest.main()
