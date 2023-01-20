from Deep_layer import NLP_package


class IPreprocessing(NLP_package.ABC):

    @NLP_package.abstractmethod
    def preprocess_text(self, text):
        pass
    @NLP_package.abstractmethod
    def reversepreprocess_text(self,text):
        pass

class Preprocessing(IPreprocessing):

    @classmethod
    def preprocess_text(self, text):
        try:
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in NLP_package.stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in NLP_package.punctuation]

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
            tokens = NLP_package.Mystem().lemmatize(text.lower())
            tokens = [token for token in tokens if token not in NLP_package.stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in NLP_package.punctuation]
            tokens = [
                token for token in tokens if token not in NLP_package.stopwords.words('english')]

            text = ' '.join(tokens).rstrip('\n')
            pattern3 = r'[\d]'
            pattern2 = '[.]'
            text = NLP_package.re.sub(pattern3, '', text)
            text = NLP_package.re.sub(pattern2, '', text)
            text = NLP_package.re.sub('  ', ' ', text)
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
            tokens = NLP_package.Mystem().lemmatize(text.lower())
            tokens = [token for token in tokens if token != " "]

            text = " ".join(tokens).rstrip('\n')
            text = NLP_package.re.sub('[!@#$-><%^&*()_=+/\|:;~,.]', '', text)
            text = NLP_package.re.sub('  ', ' ', text)
            text = text.replace(' ? ', '?')

            return text
        except:
            return 'The exception is in QuestionPreprocessing.preprocess_text'

    @classmethod
    def reversepreprocess_text(self, text):
        try:
            tokens = str(text)
            tokens = NLP_package.Mystem().lemmatize(text.lower())
            tokens = [token for token in tokens if token in NLP_package.stopwords.words('russian')
                      and (token != ' ' or token == '?')]
            text = ' '.join(tokens).rstrip('\n')
            text = NLP_package.re.sub('  ', ' ', text)
            return text
        except:
            return 'The exception is in QuestionPreprocessing.reversepreprocess_text'

class CommandPreprocessing(Preprocessing):

    @classmethod
    def preprocess_text(self, text):
        try:
            tokens = str(text)
            tokens = text.lower().split(' ')
            tokens = [token for token in tokens if token not in NLP_package.stopwords.words('russian')
                      and token != ' '
                      and token.strip() not in NLP_package.punctuation]
            text = ' '.join(tokens).rstrip('\n')
            return text
        except:
            return 'The exception is in CommandPreprocessing.preprocess_text'

    @classmethod
    def reversepreprocess_text(self, text):
        try:
            document = NLP_package.spacy.load('ru_core_news_md')

            tokens = [token.lemma_ for token in document if token.pos_ == 'VERB']

            text = ' '.join(tokens).rstrip('\n')
            print(text)
            return text
        except:
            return 'The exception is in CommandPreprocessing.reversepreprocess_text'