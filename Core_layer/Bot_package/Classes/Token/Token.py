from Deep_layer.DB_package.Classes import DB_Communication
from Core_layer.Bot_package.Interfaces import IToken


class Token(IToken.IToken):
    """

    This class describes object of taking monitors from a database

    """
    __dbc = DB_Communication.DB_Communication()

    @classmethod
    def add_token(cls, token):
        cls.__dbc.insert_to(str(token), 'tokens')

    @classmethod
    def get_token(cls, select):
        return cls.__dbc.get_data(select)
