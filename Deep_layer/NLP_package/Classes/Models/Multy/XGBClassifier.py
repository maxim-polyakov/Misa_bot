import pickle as p
import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost
from Deep_layer.DB_package.Classes import DB_Communication
from Deep_layer.NLP_package.Interfaces import IModel
from Deep_layer.NLP_package.Classes.Tokenizers import Tokenizer as t

class XGBClassifier(IModel.IModel):

    def __init__(cls, filemodelname, tokenizerfilename, dataselect):
        XGBClassifier.__filemodelname = filemodelname
        XGBClassifier.__tokenizerfilename = tokenizerfilename
        XGBClassifier.__dataselect = dataselect


    @classmethod
    def __createmodel(cls):
        model_xgboost = xgboost.XGBClassifier(learning_rate=0.1,
                                              max_depth=10,
                                              n_estimators=500,
                                              subsample=0.5,
                                              colsample_bytree=0.5,
                                              eval_metric='auc',
                                              verbosity=1)
        return model_xgboost

    @classmethod
    def train(cls, target):
        try:
            train = DB_Communication.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)

            df = pd.concat([train])

            train = df[~df[target].isna()]
            train[target] = train[target].astype(int)
            train = train.drop_duplicates()

            print(train)

            X_train, X_val, Y_train, Y_val = train_test_split(train, train[target], test_size=0.3,
                                                                          random_state=32)

            tokenizer = t.Tokenizer(train_texts=X_train['text'])

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
                p.dump(tokenizer, handle, protocol=p.HIGHEST_PROTOCOL)

            with open(cls.__filemodelname, 'wb') as handle:
                p.dump(model_xgboost, handle, protocol=p.HIGHEST_PROTOCOL)
        except:
            print('The exception is in XGBClassifier.train')
