from nltk.corpus import stopwords
from pymystem3 import Mystem
import re
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing


class QuestionPreprocessing(Preprocessing.Preprocessing):

    @classmethod
    def preprocess_text(cls, text):
        try:
            tokens = str(text).split(' ')
            tokens = Mystem().lemmatize(text.lower())
            tokens = [token for token in tokens if token != " "]
            text = " ".join(tokens).rstrip('\n')
            text = re.sub('[!@#$-><%^&*()_=+/\|:;~,.]', '', text)
            text = re.sub('  ', ' ', text)
            text = text.replace(' ? ', '?')
            return text
        except:
            return 'The exception is in QuestionPreprocessing.preprocess_text'

    @classmethod
    def reversepreprocess_text(cls, text):
        try:
            tokens = str(text)
            tokens = Mystem().lemmatize(text.lower())
            tokens = [token for token in tokens if token in stopwords.words('russian')
                      and (token != ' ' or token == '?')]
            text = ' '.join(tokens).rstrip('\n')
            text = re.sub('  ', ' ', text)
            return text
        except:
            return 'The exception is in QuestionPreprocessing.reversepreprocess_text'