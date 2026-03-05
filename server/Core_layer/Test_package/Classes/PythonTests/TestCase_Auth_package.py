import unittest
from Core_layer.Test_package.Interfases import ITestCase
from Core_layer.Auth_package.Classes import VerificationCodeStore as vcs


class TestCase_Auth_package(ITestCase.ITestCase):
    """Тесты Auth_package: VerificationCodeStore."""

    def test_put_and_get(self):
        """put сохраняет код, get_and_remove возвращает password_hash при верном коде."""
        code = vcs.put('test@example.com', 'hash123')
        self.assertIsNotNone(code)
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())
        result = vcs.get_and_remove('test@example.com', code)
        self.assertEqual(result, 'hash123')

    def test_get_wrong_code(self):
        """get_and_remove возвращает None при неверном коде."""
        code = vcs.put('wrong@example.com', 'hash456')
        result = vcs.get_and_remove('wrong@example.com', '000000')
        self.assertIsNone(result)
        # Запись остаётся, убираем для чистоты
        vcs.get_and_remove('wrong@example.com', code)

    def test_get_removes_entry(self):
        """get_and_remove удаляет запись — повторный вызов возвращает None."""
        code = vcs.put('once@example.com', 'hash789')
        vcs.get_and_remove('once@example.com', code)
        result = vcs.get_and_remove('once@example.com', code)
        self.assertIsNone(result)

    def test_has_pending(self):
        """has_pending возвращает True для email с ожидающей верификацией."""
        vcs.put('pending@example.com', 'hash')
        self.assertTrue(vcs.has_pending('pending@example.com'))
        code = vcs.put('pending@example.com', 'hash2')  # перезаписываем, получаем новый код
        vcs.get_and_remove('pending@example.com', code)
        self.assertFalse(vcs.has_pending('pending@example.com'))


if __name__ == '__main__':
    unittest.main()
