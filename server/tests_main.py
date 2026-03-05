"""
Запуск тестов из Test_package.
Аналог server_main, telegram_main, discord_main — отдельный main для тестов.
"""
import os
import sys

# Добавляем корень проекта в path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Django нужен для тестов API/views
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Front_layer.django_server.settings')
    import django
    django.setup()

    import unittest
    from Core_layer.Test_package.Classes.PythonTests import TestRun

    print("=" * 60)
    print("Запуск тестов Misa Bot")
    print("=" * 60)

    result = TestRun.TestRun.run_all_tests()
    sys.exit(0 if result.wasSuccessful() else 1)
