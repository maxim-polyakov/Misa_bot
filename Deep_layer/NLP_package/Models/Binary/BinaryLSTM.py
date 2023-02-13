from keras.layers import Embedding, LSTM, Dense, Dropout, GRU, Input
from keras.models import Sequential
import pickle as p
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

class BinaryLSTM(IModel.IModel):

    EMBEDDING_VECTOR_LENGTH = 33

    def __init__(self, filemodelname, tokenizerfilename, dataselect):
        BinaryLSTM.__filemodelname = filemodelname
        BinaryLSTM.__tokenizerfilename = tokenizerfilename
        BinaryLSTM.__dataselect = dataselect

    @classmethod
    def __createmodel(cls, tokenizer):
        optimzer = Adam(clipvalue=0.5)
        model = Sequential()
        model.add(Embedding(len(tokenizer.tokenizer.word_index) + 1,
                            cls.EMBEDDING_VECTOR_LENGTH,
                            input_length=tokenizer.MAX_SEQUENCE_LENGTH,
                            trainable=True, mask_zero=True))
        model.add(Dropout(0.5))
        model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.2))
        model.add(Dense(512, activation='sigmoid'))
        model.add(Dropout(0.5))
        model.add(Dense(512, activation='sigmoid'))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(optimizer=optimzer, loss='binary_crossentropy',
                      metrics=['binary_accuracy'])

        return model

    @classmethod
    def train(cls, target, epochs):

            train = DB_Communication.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)
            df = pd.concat([train])
            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()
            print(train)
            X_train, X_val, y_train, y_val = train_test_split(
                train, train[target], test_size=0.3, random_state=32)

            tokenizer = t.Tokenizer(train_texts=X_train['text'])

            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

            model = cls.__createmodel(tokenizer)

            history = model.fit(tokenized_X_train, y_train,
                                    validation_data=(tokenized_X_val, y_val),
                                    batch_size=51,
                                    epochs=epochs,
                                    verbose=2)

            score = history.history['val_binary_accuracy'].pop()
            print(score)
            model.save(cls.__filemodelname)
            with open(cls.__tokenizerfilename, 'wb') as handle:
                p.dump(tokenizer, handle,
                       protocol=p.HIGHEST_PROTOCOL)
            ResultSaver.ResultSaver.saveRes(history, 'resultstraining_binary.png', 'binary_accuracy')

        #try:
        #except:
           # print('The exception in BinaryLSTM.train')



