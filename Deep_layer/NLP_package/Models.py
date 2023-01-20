from Deep_layer import NLP_package


class IModel(NLP_package.ABC):

    @NLP_package.abstractmethod
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
        optimzer = NLP_package.Adam(clipvalue=0.5)
        model = NLP_package.Sequential()
        model.add(NLP_package.Embedding(len(tokenizer.tokenizer.word_index) + 1,
                                        cls.EMBEDDING_VECTOR_LENGTH,
                                        input_length=tokenizer.MAX_SEQUENCE_LENGTH,
                                        trainable=True, mask_zero=True))
        model.add(NLP_package.Dropout(0.5))
        model.add(NLP_package.LSTM(64, dropout=0.2, recurrent_dropout=0.2))
        model.add(NLP_package.Dense(512, activation='sigmoid'))
        model.add(NLP_package.Dropout(0.5))
        model.add(NLP_package.Dense(512, activation='sigmoid'))
        model.add(NLP_package.Dense(1, activation='sigmoid'))
        # compile the model
        model.compile(optimizer=optimzer, loss='binary_crossentropy',
                      metrics=['binary_accuracy'])

        return model

    @classmethod
    def train(cls, target, mode, epochs):
        try:
            recognizedtrain = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__recognizeddataselect)
            recognizedtrain.text = recognizedtrain.text.astype(str)
            train = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)

            df = NLP_package.pd.concat([train, recognizedtrain])
            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)
            X_train, X_val, y_train, y_val = NLP_package.train_test_split(
                train, train[target], test_size=0.3, random_state=32)

            if(mode == 'evaluate'):
                with open(cls.__tokenizerfilename, 'rb') as handle:
                    tokenizer = NLP_package.p.load(handle)
            else:

                tokenizer = NLP_package.Tokenizers.Tokenizer(train_texts=X_train['text'])

            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

            if(mode == 'evaluate'):
                model = NLP_package.load_model(cls.__filemodelname)
            
                es = NLP_package.EarlyStopping(patience=10, monitor='binary_accuracy',
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
                NLP_package.p.dump(tokenizer, handle,
                                   protocol=NLP_package.p.HIGHEST_PROTOCOL)

            NLP_package.ResultSavers.ResultSaver.saveRes(history, 'resultstraining_binary.png', 'binary_accuracy')

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
        model = NLP_package.Sequential()

        optimzer = NLP_package.Adam(learning_rate=0.005)
        model.add(NLP_package.Embedding(len(tokenizer.tokenizer.word_index) + 1,
                                        cls.EMBEDDING_VECTOR_LENGTH,
                                        input_length=tokenizer.MAX_SEQUENCE_LENGTH,
                                        trainable=True))
        model.add(
            NLP_package.Bidirectional(NLP_package.LSTM(256, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))
        model.add(
            NLP_package.Bidirectional(NLP_package.LSTM(128, dropout=0.2, recurrent_dropout=0.2, return_sequences=True)))
        model.add(NLP_package.Bidirectional(NLP_package.LSTM(128, dropout=0.2, recurrent_dropout=0.2)))
        model.add(NLP_package.Dense(n_clases, activation='softmax'))
        # compile the model
        model.compile(optimizer=optimzer, loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    @classmethod
    def train(cls, target, n_clases, mode, epochs):
        try:
            train = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)
            recognizedtrain = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__recognizeddataselect)
            recognizedtrain.text = recognizedtrain.text.astype(str)

            df = NLP_package.pd.concat([train, recognizedtrain])
            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)
            X_train, X_val, y_train, y_val = NLP_package.train_test_split(
                train, train[target], test_size=0.2, random_state=64)
            print('Shape of train', X_train.shape)
            print('Shape of Validation ', X_val.shape)

            if(mode == 'evaluate'):
                with open(cls.__tokenizerfilename,
                        'rb') as handle:
                    tokenizer = NLP_package.p.load(handle)
            else:

                tokenizer = NLP_package.Tokenizers.Tokenizer(train_texts=X_train['text'])

            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            tokenized_X_val = tokenizer.vectorize_input(X_val['text'])


            y_trainmatrix = NLP_package.tensorflow.keras.utils.to_categorical(
                y_train, n_clases)
            y_valmatrix = NLP_package.tensorflow.keras.utils.to_categorical(
                y_val, n_clases)
            if(mode == 'evaluate'):
            
                es = NLP_package.EarlyStopping(patience=2, monitor='val_loss',
                                               restore_best_weights=True)

                model = NLP_package.load_model(cls.__filemodelname)
            
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
                NLP_package.p.dump(tokenizer, handle,
                                   protocol=NLP_package.p.HIGHEST_PROTOCOL)

            NLP_package.ResultSavers.ResultSaver.saveRes(history, 'resultstraining_multy.png', 'accuracy')

        except:
            print('The exception is in MultyLSTM.train')

class NaiveBayes(IModel):

    def __init__(self,filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        NaiveBayes.__filemodelname = filemodelname
        NaiveBayes.__tokenizerfilename = tokenizerfilename
        NaiveBayes.__dataselect = dataselect
        NaiveBayes.__recognizeddataselect = recognizeddataselect
    @classmethod
    def __createmodel(cls):
        nb_model = NLP_package.MultinomialNB()
        return nb_model

    @classmethod
    def train(cls, target, mode):
        try:
            train = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)
            recognizedtrain = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__recognizeddataselect)
            recognizedtrain.text = recognizedtrain.text.astype(str)
            df = NLP_package.pd.concat([train, recognizedtrain])

            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)

            X_train, X_val, Y_train, Y_val = NLP_package.train_test_split(train['text'], train[target], test_size=0.3,
                                                                          random_state=32)

            print('Shape of train', X_train.shape)
            print('Shape of Validation ', X_val.shape)

            vec = NLP_package.CountVectorizer()
            X_train = vec.fit_transform(X_train).toarray()
            X_val = vec.transform(X_val).toarray()

            nb_model = cls.__createmodel()

            nb_model.fit(X_train, Y_train)

            with open(cls.__tokenizerfilename, 'wb') as handle:
                NLP_package.p.dump(vec, handle,
                                   protocol=NLP_package.p.HIGHEST_PROTOCOL)

            with open(cls.__filemodelname, 'wb') as handle:
                NLP_package.p.dump(nb_model, handle,
                                   protocol=NLP_package.p.HIGHEST_PROTOCOL)
        except:
            print('The exception is in NaiveBayes.train')

class RandomForest(IModel):

    def __init__(cls, filemodelname, tokenizerfilename, dataselect,
                 recognizeddataselect):
        RandomForest.__filemodelname = filemodelname
        RandomForest.__tokenizerfilename = tokenizerfilename
        RandomForest.__dataselect = dataselect
        RandomForest.__recognizeddataselect = recognizeddataselect
    @classmethod
    def __createmodel(cls):
        rfc = NLP_package.RandomForestClassifier(criterion='entropy',
                                                 n_estimators=700)
        return rfc

    @classmethod
    def train(cls, target, mode):
        try:
            train = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)
            recognizedtrain = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__recognizeddataselect)
            recognizedtrain.text = recognizedtrain.text.astype(str)
            df = NLP_package.pd.concat([train, recognizedtrain])

            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)

            X_train, X_val, Y_train, Y_val = NLP_package.train_test_split(train, train[target], test_size=0.3,
                                                                          random_state=32)

            print('Shape of train', X_train.shape)
            print('Shape of Validation ', X_val.shape)

            tokenizer = NLP_package.Tokenizers.Tokenizer(train_texts=X_train['text'])

            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            #tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

            rfc = cls.__createmodel()

            rfc.fit(tokenized_X_train, Y_train)

            with open(cls.__tokenizerfilename, 'wb') as handle:
                NLP_package.p.dump(tokenizer, handle,
                                   protocol=NLP_package.p.HIGHEST_PROTOCOL)

            with open(cls.__filemodelname, 'wb') as handle:
                NLP_package.p.dump(rfc, handle,
                                   protocol=NLP_package.p.HIGHEST_PROTOCOL)
        except:
            print('The exception is in RandomForest.train')

class XGBClassifier(IModel):

    def __init__(cls, filemodelname, tokenizerfilename, dataselect,
                     recognizeddataselect):
        XGBClassifier.__filemodelname = filemodelname
        XGBClassifier.__tokenizerfilename = tokenizerfilename
        XGBClassifier.__dataselect = dataselect
        XGBClassifier.__recognizeddataselect = recognizeddataselect

    @classmethod
    def __createmodel(cls):
        model_xgboost = NLP_package.xgboost.XGBClassifier(learning_rate=0.1,
                                                          max_depth=10,
                                                          n_estimators=500,
                                                          subsample=0.5,
                                                          colsample_bytree=0.5,
                                                          eval_metric='auc',
                                                          verbosity=1)
        return model_xgboost

    @classmethod
    def train(cls, target, mode):

        try:
            train = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)
            recognizedtrain = NLP_package.DB_Bridge.DB_Communication.get_data(cls.__recognizeddataselect)
            recognizedtrain.text = recognizedtrain.text.astype(str)
            df = NLP_package.pd.concat([train, recognizedtrain])

            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)

            X_train, X_val, Y_train, Y_val = NLP_package.train_test_split(train, train[target], test_size=0.3,
                                                                          random_state=32)

            tokenizer = NLP_package.Tokenizers.Tokenizer(train_texts=X_train['text'])

            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            tokenized_X_val = tokenizer.vectorize_input(X_val['text'])

            model_xgboost = cls.__createmodel()

            eval_set = [(tokenized_X_val, Y_val)]

            model_xgboost.fit(tokenized_X_train,
                          Y_train,
                          early_stopping_rounds=100,
                          eval_set=eval_set,
                          verbose=True)

            with open(cls.__tokenizerfilename, 'wb') as handle:
                NLP_package.p.dump(tokenizer, handle,
                                   protocol=NLP_package.p.HIGHEST_PROTOCOL)

            with open(cls.__filemodelname, 'wb') as handle:
                NLP_package.p.dump(model_xgboost, handle,
                                   protocol=NLP_package.p.HIGHEST_PROTOCOL)
        except:
            print('The exception is in XGBClassifier.train')