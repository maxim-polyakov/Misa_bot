from nltk.corpus import stopwords
from string import punctuation
from Deep_layer.NLP_package.Interfaces import IPreprocessor


class Preprocessor(IPreprocessor.IPreprocessor):


    """

    This class is written for a preprocessiong of text column in a DataFrame

    """
    @classmethod
    def preprocess_text(cls, text):
        try:
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in punctuation]

            text = " ".join(tokens).rstrip('\n')
            text = text.replace('  ', ' ')
            return text
        except:
            return 'The exception is in Preprocessing.preprocess_text'

    @classmethod
    def reversepreprocess_text(cls, text):
        pass