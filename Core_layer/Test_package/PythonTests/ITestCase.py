import unittest
from abc import ABC, abstractmethod

class ITestCase(unittest.TestCase, ABC):

    @abstractmethod
    def test_calc(self):
        pass

    @abstractmethod
    def test_founder(self):
        pass

    @abstractmethod
    def test_trans(self):
        pass

    @abstractmethod
    def test_bridge(self):
        pass

    @abstractmethod
    def test_tmon(self):
        pass

    @abstractmethod
    def test_answer(self):
        pass