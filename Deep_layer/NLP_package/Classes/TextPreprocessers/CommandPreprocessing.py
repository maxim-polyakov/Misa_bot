from nltk.corpus import stopwords
from string import punctuation
import spacy
import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing


class CommandPreprocessing(Preprocessing.Preprocessing):
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
            text = ' '.join(tokens).rstrip('\n')
            logging.info('The commandpreprocessing is done')
            return text
        except Exception as e:
            logging.exception(str('The exception is in commandpreprocessing.preprocess_text ' + e))

    @classmethod
    def reversepreprocess_text(cls, text):
#
#
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            document = spacy.load('ru_core_news_md')
            tokens = [token.lemma_ for token in document if token.pos_ == 'VERB']
            text = ' '.join(tokens).rstrip('\n')
            logging.info('The commandpreprocessing.reversepreprocess_text is done')
            return text
        except Exception as e:
            logging.exception(str('The exception is in commandpreprocessing.reversepreprocess_text ' + e))