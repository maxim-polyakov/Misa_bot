from Deep_layer import API_package


class ITranslator(API_package.ABC):

    @API_package.abstractmethod
    def translate(self):
        pass

class GoogleTranslator(ITranslator):


    _translator = API_package.Translator()

    lang = 'ru'
    def __init__(self, lang,):
        GoogleTranslator.lang = lang

    @classmethod
    def _translate(cls, inputText):
        tranlated = cls._translator.translate(inputText, dest=cls.lang)
        return tranlated.text

    @classmethod
    @API_package.dispatch(object, object, object)
    def translate(cls, dataselect, insertdtname):
        try:
            train = API_package.DB_Bridge.DB_Communication.get_data(dataselect)
            train.text = train.text.astype(str)

            df = API_package.pd.concat([train])
            df = API_package.pd.DataFrame(df['text'])
            df['text'] = df['text'].apply(cls._translate)

            API_package.DB_Bridge.DB_Communication.insert_to(df, 'translated')

            return 'Готово'
        except:
            print('The exception is in GoogleTranslator.translate')

    @classmethod
    @API_package.dispatch(object, object)
    def translate(cls, inptmes):
        try:
            tranlated = cls._translate(inptmes)

            return tranlated
        except:
            print('The exception is in GoogleTranslatorMes.translate')