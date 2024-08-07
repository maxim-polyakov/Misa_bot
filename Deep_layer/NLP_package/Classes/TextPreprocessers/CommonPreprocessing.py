from nltk.corpus import stopwords
from string import punctuation
from pymystem3 import Mystem
import re
from Deep_layer.NLP_package.Classes.TextPreprocessers import Preprocessing


class CommonPreprocessing(Preprocessing.Preprocessing):

    @classmethod
    def preprocess_text(cls, text):
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
            return text
        #try:
        #except:
        #    return 'The exception is in CommonPreprocessing.preprocess_text'

    @classmethod
    def reversepreprocess_text(cls, text):
        pass
