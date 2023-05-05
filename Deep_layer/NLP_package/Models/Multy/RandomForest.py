import pickle as p
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from Deep_layer.DB_package.DB_Bridge import DB_Communication
from Deep_layer.NLP_package.Models import IModel
from Deep_layer.NLP_package.Tokenizers import Tokenizer

class RandomForest(IModel.IModel):

    def __init__(cls, filemodelname, tokenizerfilename, dataselect):


        RandomForest.__filemodelname = filemodelname
        RandomForest.__tokenizerfilename = tokenizerfilename
        RandomForest.__dataselect = dataselect

    @classmethod
    def __createmodel(cls):


        rfc = RandomForestClassifier(criterion='entropy', n_estimators=700)
        return rfc

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

            X_train, X_val, Y_train, Y_val = train_test_split(train, train[target], test_size=0.3, random_state=32)
            print('Shape of train', X_train.shape)
            print('Shape of Validation ', X_val.shape)
            tokenizer = Tokenizer.Tokenizer(train_texts=X_train['text'])
            tokenizer.train_tokenize()
            tokenized_X_train = tokenizer.vectorize_input(X_train['text'])
            rfc = cls.__createmodel()
            rfc.fit(tokenized_X_train, Y_train)
            with open(cls.__tokenizerfilename, 'wb') as handle:
                p.dump(tokenizer, handle, protocol=p.HIGHEST_PROTOCOL)

            with open(cls.__filemodelname, 'wb') as handle:
                p.dump(rfc, handle, protocol=p.HIGHEST_PROTOCOL)
        except:
            print('The exception is in RandomForest.train')
