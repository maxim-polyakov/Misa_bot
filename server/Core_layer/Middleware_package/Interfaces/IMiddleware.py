from abc import ABC, abstractmethod

class IMiddleware(ABC):
    """
    It is entity of middleware
    """
    @abstractmethod
    def verify_token_and_get_user(cls):
        pass
