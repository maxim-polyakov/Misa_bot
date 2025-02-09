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
        # text preprocessing
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # convert input text to string
            tokens = str(text)
            # perform lemmatization using mystem
            tokens = Mystem().lemmatize(text.lower())
            # remove stopwords (russian) and punctuation
            tokens = [token for token in tokens if token not in stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in punctuation]
            # remove stopwords (english)
            tokens = [
                token for token in tokens if token not in stopwords.words('english')]
            # join tokens back into a single string and remove trailing newline characters
            text = ' '.join(tokens).rstrip('\n')
            # define regex patterns for removing digits and dots
            pattern3 = r'[\d]'
            pattern2 = '[.]'
            # remove digits and dots from the text
            text = re.sub(pattern3, '', text)
            text = re.sub(pattern2, '', text)
            # replace double spaces with a single space
            text = re.sub('  ', ' ', text)
            # log successful preprocessing
            logging.info('The commonpreprocessing.preprocess_text method has completed successfully')
            return text
        except Exception as e:
            # log any exceptions that occur during preprocessing
            logging.exception('The exception occurred in commonpreprocessing.preprocess_text: ' + str(e))

    @classmethod
    def reversepreprocess_text(cls, text):
        pass
