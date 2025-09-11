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
        # text preprocessing
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # convert input text to string (redundant, as text is already a string)
            tokens = str(text)
            # convert text to lowercase and split it into words
            tokens = text.lower().split(' ')
            # remove stopwords, spaces, and punctuation from the token list
            tokens = [token for token in tokens if token not in stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in punctuation]
            # join the filtered tokens back into a single string
            text = " ".join(tokens).rstrip('\n')
            # replace double spaces with a single space
            text = text.replace('  ', ' ')
            # log successful completion of text preprocessing
            logging.info('The preprocessing.preprocess_text method has completed successfully')
            return text
        except Exception as e:
            # log any exceptions that occur during preprocessing
            logging.exception('The exception occurred in preprocessing.preprocess_text: ' + str(e))

    @classmethod
    def reversepreprocess_text(cls,text):
        pass