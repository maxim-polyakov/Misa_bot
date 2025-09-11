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
        # text preprocessing
        # configure logging settings
        logging.basicConfig(level=logging.INFO, filename="misa.log", filemode="w")
        try:
            # convert the input text to a string and split it into tokens
            tokens = str(text).split(' ')
            # perform lemmatization using the mystem tool
            tokens = Mystem().lemmatize(text.lower())
            # remove empty spaces from the token list
            tokens = [token for token in tokens if token != " "]
            # join tokens back into a single string and remove trailing newline characters
            text = " ".join(tokens).rstrip('\n')
            # remove special characters and punctuation from the text
            text = re.sub('[!@#$-><%^&*()_=+/\|:;~,.]', '', text)
            # replace double spaces with a single space
            text = re.sub('  ', ' ', text)
            # ensure proper spacing around question marks
            text = text.replace(' ? ', '?')
            # log that the preprocessing was successfully completed
            logging.info('The questionpreprocessing.preprocess_text method has completed successfully')
            return text
        except Exception as e:
            # log any exceptions that occur during preprocessing
            logging.exception(str('The exception is in preprocessing.preprocess_text: ' + str(e)))

    @classmethod
    def reversepreprocess_text(cls, text):
        # text preprocessing
        # convert the input text to a string
        try:
            tokens = str(text)
            # perform lemmatization using the mystem library
            tokens = Mystem().lemmatize(text.lower())
            # filter out stopwords, keeping only those that are in the russian stopword list
            # also, retain only spaces or question marks
            tokens = [token for token in tokens if token in stopwords.words('russian')
                      and (token != ' ' or token == '?')]
            # join the tokens back into a single string and remove trailing newline characters
            text = ' '.join(tokens).rstrip('\n')
            # replace double spaces with a single space
            text = re.sub('  ', ' ', text)
            # log that the preprocessing function has completed successfully
            logging.info('The questionpreprocessing.reversepreprocess_text method has completed successfully')
            return text
        except Exception as e:
            # log any exceptions that occur during preprocessing
            logging.exception('The exception is in preprocessing.reversepreprocess_text: ' + str(e))
