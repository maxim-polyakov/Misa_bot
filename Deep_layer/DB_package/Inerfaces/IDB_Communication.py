from abc import ABC, abstractmethod

class IDB_Communication(ABC):
    """

    Summary

    """
    @abstractmethod
    def insert_to(cls):
        pass

    @abstractmethod
    def get_data(cls):
        pass

    @abstractmethod
    def delete_data(cls, delete):
        pass

    @abstractmethod
    def checkcommands(cls):
        pass