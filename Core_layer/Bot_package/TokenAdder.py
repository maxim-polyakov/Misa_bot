from Core_layer import Bot_package


class TokenAdder:
    def __init_(cls):
        pass

    @classmethod
    def add_token(cls, token):
        Bot_package.DB_Bridge.DB_Communication.insert_to(str(token), 'tokens')