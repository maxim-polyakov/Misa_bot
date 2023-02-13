from Deep_layer.DB_package import DB_Bridge
from Core_layer.Bot_package.Token import Interfaces

class Token(Interfaces.IToken):

    @classmethod
    def add_token(cls, token):
        DB_Bridge.DB_Communication.insert_to(str(token), 'tokens')

    @classmethod
    def get_token(cls, select):
        return DB_Bridge.DB_Communication.get_data(select)
