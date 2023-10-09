from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IToken


class Token(IToken.IToken):


    @classmethod
    def add_token(cls, token):
        DB_Communication.DB_Communication.insert_to(str(token), 'tokens')

    @classmethod
    def get_token(cls, select):
        return DB_Communication.DB_Communication.get_data(select)
