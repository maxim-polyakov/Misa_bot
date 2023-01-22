from nltk.corpus import stopwords
from string import punctuation
from pymystem3 import Mystem
import spacy
import re
from abc import ABC, abstractmethod

class IPreprocessing(ABC):

    @abstractmethod
    def preprocess_text(self, text):
        pass
    @abstractmethod
    def reversepreprocess_text(self,text):
        pass

class Preprocessing(IPreprocessing):

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


class CommonPreprocessing(Preprocessing):

    @classmethod
    def preprocess_text(self, text):
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
            return text
        except:
            return 'The exception is in CommonPreprocessing.preprocess_text'

    @classmethod
    def reversepreprocess_text(self, text):
        pass


class QuestionPreprocessing(Preprocessing):

    @classmethod
    def preprocess_text(self, text):
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
    def reversepreprocess_text(self, text):
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

class CommandPreprocessing(Preprocessing):

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