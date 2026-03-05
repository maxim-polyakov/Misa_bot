import unittest
from Core_layer.Test_package.Classes.PythonTests import (
    TestCase_Auth_package,
    TestCase_API_views,
)


class TestRun:
    """Запуск набора тестов."""

    @classmethod
    def run_all_tests(cls):
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()

        # Auth (VerificationCodeStore)
        suite.addTests(loader.loadTestsFromModule(TestCase_Auth_package))
        # Django API views
        suite.addTests(loader.loadTestsFromModule(TestCase_API_views))

        # API package (calc, finders) — требует внешние сервисы
        try:
            from Core_layer.Test_package.Classes.PythonTests import TestCase_API_package
            suite.addTests(loader.loadTestsFromModule(TestCase_API_package))
        except Exception:
            pass

        # Command analyzer — требует GPT
        try:
            from Core_layer.Test_package.Classes.PythonTests import TestCase_Command_package
            suite.addTests(loader.loadTestsFromModule(TestCase_Command_package))
        except Exception:
            pass

        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite)