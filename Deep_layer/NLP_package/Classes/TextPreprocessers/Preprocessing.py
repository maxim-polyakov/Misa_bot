from nltk.corpus import stopwords
from string import punctuation
import logging
from Deep_layer.NLP_package.Interfaces import IPreprocessing


class Preprocessing(IPreprocessing.IPreprocessing):
    """
    It is a main preprocessing
    """
    @classmethod
    def preprocess_text(cls, text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in punctuation]

            text = " ".join(tokens).rstrip('\n')
            text = text.replace('  ', ' ')
            logging.info('The preprocessing.preprocess_text is done')
            return text
        except Exception as e:
            logging.exception(str('The exception is in preprocessing.preprocess_text ' + str(e)))

    @classmethod
    def reversepreprocess_text(cls,text):
        pass