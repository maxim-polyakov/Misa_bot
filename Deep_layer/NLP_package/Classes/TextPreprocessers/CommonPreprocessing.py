from nltk.corpus import stopwords
from string import punctuation
from pymystem3 import Mystem
import re
import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing


class CommonPreprocessing(Preprocessing.Preprocessing):
    """
    It is a common preprocessing of sentences
    """
    @classmethod
    def preprocess_text(cls, text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            tokens = str(text)
            tokens = Mystem().lemmatize(text.lower())
            tokens = [token for token in tokens if token not in stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in punctuation]
            tokens = [
                token for token in tokens if token not in stopwords.words('english')]

            text = ' '.join(tokens).rstrip('\n')
            pattern3 = r'[\d]'
            pattern2 = '[.]'
            text = re.sub(pattern3, '', text)
            text = re.sub(pattern2, '', text)
            text = re.sub('  ', ' ', text)
            logging.info('The commonPreprocessing.preprocess_text is done')
            return text
        except Exception as e:
            logging.exception(str('The exception is in commonpreprocessing.preprocess_text ' + str(e)))

    @classmethod
    def reversepreprocess_text(cls, text):
        pass
