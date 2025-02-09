from nltk.corpus import stopwords
from string import punctuation
import spacy
import logging
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing


class CommandPreprocessing(Preprocessing.Preprocessing):
    """
    It is a common preprocessing of commands
    """
    @classmethod
    def preprocess_text(cls, text):
        # text preprocessing
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # convert input text to string (though unnecessary if text is already a string)
            tokens = str(text)
            # convert text to lowercase and split it into words
            tokens = text.lower().split(' ')
            # remove stopwords, spaces, and punctuation from the token list
            tokens = [token for token in tokens if token not in stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in punctuation]
            # join the filtered tokens back into a single string and remove trailing newline characters
            text = ' '.join(tokens).rstrip('\n')
            # log successful preprocessing
            logging.info('The commandpreprocessing.preprocess_text method has completed successfully')
            return text
        except Exception as e:
            # log any exceptions that occur during preprocessing
            logging.exception('The exception occurred in commandpreprocessing.preprocess_text: ' + str(e))

    @classmethod
    def reversepreprocess_text(cls, text):
        # text preprocessing
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # load the russian language model from spacy
            document = spacy.load('ru_core_news_md')
            # extract lemmatized verbs from the text
            tokens = [token.lemma_ for token in document if token.pos_ == 'VERB']
            # join the tokens into a single string and remove trailing newline characters
            text = ' '.join(tokens).rstrip('\n')
            # log successful completion of the function
            logging.info('The commandpreprocessing.reversepreprocess_text is done')
            return text
        except Exception as e:
            # log any exceptions that occur during execution
            logging.exception('The exception occurred in commandpreprocessing.reversepreprocess_text: ' + str(e))
