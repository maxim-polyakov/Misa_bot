from nltk.corpus import stopwords
from pymystem3 import Mystem
import re
import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing


class QuestionPreprocessing(Preprocessing.Preprocessing):
    """
    It is a preprocessing of questions
    """
    @classmethod
    def preprocess_text(cls, text):
#
#       Its a method for text preprocessing
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            tokens = str(text).split(' ')
            tokens = Mystem().lemmatize(text.lower())
            tokens = [token for token in tokens if token != " "]
            text = " ".join(tokens).rstrip('\n')
            text = re.sub('[!@#$-><%^&*()_=+/\|:;~,.]', '', text)
            text = re.sub('  ', ' ', text)
            text = text.replace(' ? ', '?')
            logging.info('The questionpreprocessing.preprocess_text is done')
            return text
        except Exception as e:
            logging.exception(str('The exception is in preprocessing.preprocess_text ' + str(e)))

    @classmethod
    def reversepreprocess_text(cls, text):
        try:
            tokens = str(text)
            tokens = Mystem().lemmatize(text.lower())
            tokens = [token for token in tokens if token in stopwords.words('russian')
                      and (token != ' ' or token == '?')]
            text = ' '.join(tokens).rstrip('\n')
            text = re.sub('  ', ' ', text)
            logging.info('The questionpreprocessing.reversepreprocess_text is done')
            return text
        except Exception as e:
            logging.exception(str('The exception is in preprocessing.reversepreprocess_text ' + str(e)))
