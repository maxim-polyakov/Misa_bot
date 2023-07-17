from keras.layers import Embedding, LSTM, Dense, Dropout, GRU, Input
from keras.models import Sequential
import pickle as p
import tensorflow as tensorflow
from tensorflow.keras.models import load_model
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, LSTM, Embedding, Bidirectional
from Deep_layer.DB_package.DB_Bridge import DB_Communication
from Deep_layer.NLP_package.Tokenizers import Tokenizer as t
from Deep_layer.NLP_package.ResultSavers import ResultSaver
from Deep_layer.NLP_package.Models import IModel

class MultyLSTM(IModel.IModel):
    EMBEDDING_VECTOR_LENGTH = 33

    def __init__(self, filemodelname, tokenizerfilename, dataselect):

        MultyLSTM.__filemodelname = filemodelname
        MultyLSTM.__tokenizerfilename = tokenizerfilename
        MultyLSTM.__dataselect = dataselect

    @classmethod
    def __createmodel(cls, tokenizer, n_clases):
        model = Sequential()

        optimzer = Adam(learning_rate=0.005)
        model.add(Embedding(len(tokenizer.tokenizer.word_index) + 1,
                            cls.EMBEDDING_VECTOR_LENGTH,
                            input_length=tokenizer.MAX_SEQUENCE_LENGTH,
                            trainable=True))
        model.add(Bidirectional(LSTM(256, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))
        model.add(Bidirectional(LSTM(128, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))
        model.add(Bidirectional(LSTM(128, dropout=0.2, recurrent_dropout=0.2)))
        model.add(Dense(n_clases, activation='softmax'))
        model.compile(optimizer=optimzer, loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    @classmethod
    def train(cls, target, n_clases, epochs):

            train = DB_Communication.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)

            df = pd.concat([train])
            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)
            X_train, X_val, y_train, y_val = train_test_split(
                train, train[target], test_size=0.2, random_state=64)
            print('Shape of train', X_train.shape)
            print('Shape of Validation ', X_val.shape)


            tokenizer = t.Tokenizer(train_texts=X_train['text'])
            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            tokenized_X_val = tokenizer.vectorize_input(X_val['text'])
            y_trainmatrix = tensorflow.keras.utils.to_categorical(
                y_train, n_clases)
            y_valmatrix = tensorflow.keras.utils.to_categorical(
                y_val, n_clases)

            model = cls.__createmodel(tokenizer, n_clases)
            history = model.fit(tokenized_X_train, y_trainmatrix,
                                    batch_size=51, epochs=epochs,
                                    validation_data=(tokenized_X_val, y_valmatrix),
                                    verbose=2)

            model.save(cls.__filemodelname)
            with open(cls.__tokenizerfilename, 'wb') as handle:
                p.dump(tokenizer, handle, protocol=p.HIGHEST_PROTOCOL)

            ResultSaver.ResultSaver.saveRes(history, 'resultstraining_multy.png', 'accuracy')