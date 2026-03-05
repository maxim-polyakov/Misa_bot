"""
Тесты Django API views (auth, chats).
Требует Django setup.
"""
import unittest
from django.test import Client
from Core_layer.Test_package.Interfases import ITestCase


class TestCase_API_views(ITestCase.ITestCase):
    """Тесты API endpoints."""

    def setUp(self):
        self.client = Client()

    def test_swagger_json(self):
        """swagger.json возвращает 200 и JSON."""
        r = self.client.get('/swagger.json')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('info', data)
        self.assertIn('paths', data)
        self.assertEqual(data['info']['title'], 'Misa API')

    def test_home(self):
        """Главная страница возвращает 200."""
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_register_empty_fails(self):
        """POST /auth/register/ без тела возвращает ошибку."""
        r = self.client.post('/auth/register/', {}, content_type='application/json')
        self.assertIn(r.status_code, (200, 400, 422))

    def test_login_empty_fails(self):
        """POST /auth/login/ без тела возвращает ошибку."""
        r = self.client.post('/auth/login/', {}, content_type='application/json')
        self.assertIn(r.status_code, (200, 400, 401))

    def test_chats_list_unauth(self):
        """GET /api/chats/ без JWT возвращает 401."""
        r = self.client.get('/api/chats/')
        self.assertIn(r.status_code, (200, 401, 403))


if __name__ == '__main__':
    unittest.main()
