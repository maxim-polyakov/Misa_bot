from nltk.corpus import stopwords
from string import punctuation
import spacy
from Deep_layer.NLP_package.TextPreprocessers import Preprocessing

class CommandPreprocessing(Preprocessing.Preprocessing):

    @classmethod
    def preprocess_text(self, text):
        try:
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in punctuation]
            text = ' '.join(tokens).rstrip('\n')
            return text
        except:
            return 'The exception is in CommandPreprocessing.preprocess_text'

    @classmethod
    def reversepreprocess_text(self, text):
        try:
            document = spacy.load('ru_core_news_md')
            tokens = [token.lemma_ for token in document if token.pos_ == 'VERB']
            text = ' '.join(tokens).rstrip('\n')
            print(text)
            return text
        except:
            return 'The exception is in CommandPreprocessing.reversepreprocess_text'