import unittest
from Core_layer.Test_package.Classes.PythonTests import (
    TestCase_Auth_package,
    TestCase_API_views,
    TestCase_GradiusService,
    TestCase_ResponseUtils,
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
        # Pure command response parsing
        suite.addTests(loader.loadTestsFromModule(TestCase_ResponseUtils))
        # Gradius receives a pseudonymous ID scoped to each chat
        suite.addTests(loader.loadTestsFromModule(TestCase_GradiusService))

        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite)