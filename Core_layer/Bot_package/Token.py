from Deep_layer.DB_package import DB_Bridge

class Token:
    def __init_(cls):
        pass
    @classmethod
    def add_token(cls, token):
        DB_Bridge.DB_Communication.insert_to(str(token), 'tokens')

    @classmethod
    def get_token(cls, select):
        return DB_Bridge.DB_Communication.get_data(select)
