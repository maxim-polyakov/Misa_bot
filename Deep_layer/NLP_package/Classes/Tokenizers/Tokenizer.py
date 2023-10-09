from keras.preprocessing.text import Tokenizer as token
from tensorflow.keras.preprocessing.sequence import pad_sequences
from Deep_layer.NLP_package.Interfaces import ITokenizer


class Tokenizer(ITokenizer.ITokenizer):
    """

    Summary

    """
    TOP_K = 20000
    MAX_SEQUENCE_LENGTH = 33

    def __init__(self, train_texts):
        self.train_texts = train_texts
        self.tokenizer = token(num_words=self.TOP_K)

    def train_tokenize(self):
        max_length = len(max(self.train_texts, key=len))
        self.max_length = min(max_length, self.MAX_SEQUENCE_LENGTH)
        self.tokenizer.fit_on_texts(self.train_texts)

    def vectorize_input(self, tweets):
        tweets = self.tokenizer.texts_to_sequences(tweets)
        tweets = pad_sequences(tweets, maxlen=self.max_length, truncating='post', padding='post')
        return tweets