from nltk.corpus import stopwords
from string import punctuation
from Deep_layer.NLP_package.TextPreprocessers import IPreprocessing

class Preprocessing(IPreprocessing.IPreprocessing):

    @classmethod
    def preprocess_text(self, text):
        try:
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in punctuation]

            text = " ".join(tokens).rstrip('\n')
            text = text.replace('  ', ' ')
            return text
        except:
            return 'The exception is in Preprocessing.preprocess_text'

    @classmethod
    def reversepreprocess_text(self,text):
        pass