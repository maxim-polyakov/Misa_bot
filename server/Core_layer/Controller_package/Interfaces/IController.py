from abc import ABC, abstractmethod

class IController(ABC):
    """
    It is entity of controller
    """
    @abstractmethod
    def success_response(cls):
        pass
    @abstractmethod
    def error_response(cls):
        pass

    @abstractmethod
    def generate_jwt_token(cls):
        pass

    @abstractmethod
    def verify_jwt_token(cls):
        pass

    @abstractmethod
    def get_user_from_token(cls):
        pass

    @abstractmethod
    def register(cls):
        pass

    @abstractmethod
    def login_view(cls):
        pass

    @abstractmethod
    def check(cls):
        pass