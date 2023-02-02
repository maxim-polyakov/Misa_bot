from keras.layers import Embedding, LSTM, Dense, Dropout, GRU, Input
from keras.models import Sequential
import pickle as p
import tensorflow as tensorflow
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from tensorflow.keras.models import load_model
import pandas as pd
#from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, LSTM, Embedding, Bidirectional
from abc import ABC, abstractmethod
from Deep_layer.DB_package import DB_Bridge
import xgboost
from Deep_layer.NLP_package import Tokenizers
from Deep_layer.NLP_package import ResultSavers

class IModel(ABC):

    @abstractmethod
    def train(self):
        pass

class BinaryLSTM(IModel):

    EMBEDDING_VECTOR_LENGTH = 33

    def __init__(self, filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        BinaryLSTM.__filemodelname = filemodelname
        BinaryLSTM.__tokenizerfilename = tokenizerfilename
        BinaryLSTM.__dataselect = dataselect
        BinaryLSTM.__recognizeddataselect = recognizeddataselect

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
    def train(cls, target, mode, epochs):
        try:
            recognizedtrain = DB_Bridge.DB_Communication.get_data(cls.__recognizeddataselect)
            recognizedtrain.text = recognizedtrain.text.astype(str)
            train = DB_Bridge.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)

            df = pd.concat([train, recognizedtrain])
            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)
            X_train, X_val, y_train, y_val = train_test_split(
                train, train[target], test_size=0.3, random_state=32)

            if(mode == 'evaluate'):
                with open(cls.__tokenizerfilename, 'rb') as handle:
                    tokenizer = p.load(handle)
            else:

                tokenizer = Tokenizers.Tokenizer(train_texts=X_train['text'])

            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

            if(mode == 'evaluate'):
                model = load_model(cls.__filemodelname)
            
                es = EarlyStopping(patience=10, monitor='binary_accuracy',
                                               restore_best_weights=True)
            
                history = model.fit(tokenized_X_train, y_train,
                                    validation_data=(tokenized_X_val, y_val),
                                    batch_size=51,
                                    epochs=epochs,
                                    verbose=2,
                                    callbacks=[es]
                                    )
            else:
                model = cls.__createmodel(tokenizer)
            
                history = model.fit(tokenized_X_train, y_train,
                                    validation_data=(tokenized_X_val, y_val),
                                    batch_size=51,
                                    epochs=epochs,
                                    verbose=2,
                                    )

            score = history.history['val_binary_accuracy'].pop()

            print(score)

            model.save(cls.__filemodelname)

            with open(cls.__tokenizerfilename, 'wb') as handle:
                p.dump(tokenizer, handle,
                                   protocol=p.HIGHEST_PROTOCOL)
            ResultSavers.ResultSaver.saveRes(history, 'resultstraining_binary.png', 'binary_accuracy')

        except:
           print('The exception in BinaryLSTM.train')

class MultyLSTM(IModel):

    EMBEDDING_VECTOR_LENGTH = 33

    def __init__(self, filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):

        MultyLSTM.__filemodelname = filemodelname
        MultyLSTM.__tokenizerfilename = tokenizerfilename
        MultyLSTM.__dataselect = dataselect
        MultyLSTM.__recognizeddataselect = recognizeddataselect
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
    def train(cls, target, n_clases, mode, epochs):

            train = DB_Bridge.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)
            recognizedtrain = DB_Bridge.DB_Communication.get_data(cls.__recognizeddataselect)
            recognizedtrain.text = recognizedtrain.text.astype(str)

            df = pd.concat([train, recognizedtrain])
            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)
            X_train, X_val, y_train, y_val = train_test_split(
                train, train[target], test_size=0.2, random_state=64)
            print('Shape of train', X_train.shape)
            print('Shape of Validation ', X_val.shape)

            if(mode == 'evaluate'):
                with open(cls.__tokenizerfilename,
                        'rb') as handle:
                    tokenizer = p.load(handle)
            else:
                tokenizer = Tokenizers.Tokenizer(train_texts=X_train['text'])
            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            tokenized_X_val = tokenizer.vectorize_input(X_val['text'])
            y_trainmatrix = tensorflow.keras.utils.to_categorical(
                y_train, n_clases)
            y_valmatrix = tensorflow.keras.utils.to_categorical(
                y_val, n_clases)

            if(mode == 'evaluate'):
                es = EarlyStopping(patience=2, monitor='val_loss',
                                               restore_best_weights=True)

                model = load_model(cls.__filemodelname)
            
                history = model.fit(tokenized_X_train, y_trainmatrix,
                                    batch_size=51, epochs=epochs,
                                    validation_data=(tokenized_X_val, y_valmatrix),
                                    verbose=2,
                                    callbacks=[es])
            else:
                model = cls.__createmodel(tokenizer, n_clases)
                history = model.fit(tokenized_X_train, y_trainmatrix,
                                    batch_size=51, epochs=epochs,
                                    validation_data=(tokenized_X_val, y_valmatrix),
                                    verbose=2)
            model.save(cls.__filemodelname)
            with open(cls.__tokenizerfilename, 'wb') as handle:
                p.dump(tokenizer, handle, protocol=p.HIGHEST_PROTOCOL)

            ResultSavers.ResultSaver.saveRes(history, 'resultstraining_multy.png', 'accuracy')

        # try:
        #xcept:
         #   print('The exception is in MultyLSTM.train')

class NaiveBayes(IModel):

    def __init__(self,filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        NaiveBayes.__filemodelname = filemodelname
        NaiveBayes.__tokenizerfilename = tokenizerfilename
        NaiveBayes.__dataselect = dataselect
        NaiveBayes.__recognizeddataselect = recognizeddataselect
    @classmethod
    def __createmodel(cls):
        nb_model = MultinomialNB()
        return nb_model

    @classmethod
    def train(cls, target, mode):
        try:
            train = DB_Bridge.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)
            recognizedtrain = DB_Bridge.DB_Communication.get_data(cls.__recognizeddataselect)
            recognizedtrain.text = recognizedtrain.text.astype(str)
            df = pd.concat([train, recognizedtrain])

            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()
            print(train)

            X_train, X_val, Y_train, Y_val = train_test_split(train['text'], train[target], test_size=0.3, random_state=32)

            print('Shape of train', X_train.shape)
            print('Shape of Validation ', X_val.shape)

            vec = CountVectorizer()
            X_train = vec.fit_transform(X_train).toarray()
            X_val = vec.transform(X_val).toarray()
            nb_model = cls.__createmodel()
            nb_model.fit(X_train, Y_train)

            with open(cls.__tokenizerfilename, 'wb') as handle:
                p.dump(vec, handle, protocol=p.HIGHEST_PROTOCOL)

            with open(cls.__filemodelname, 'wb') as handle:
                p.dump(nb_model, handle, protocol=p.HIGHEST_PROTOCOL)
        except:
            print('The exception is in NaiveBayes.train')

