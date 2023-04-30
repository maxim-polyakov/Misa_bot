import pickle as p
import pandas as pd
from sklearn.model_selection import train_test_split
from Deep_layer.DB_package.DB_Bridge import DB_Communication
from Deep_layer.NLP_package.Models import IModel
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

class NaiveBayes(IModel.IModel):

    def __init__(self,filemodelname, tokenizerfilename, dataselect):
        NaiveBayes.__filemodelname = filemodelname
        NaiveBayes.__tokenizerfilename = tokenizerfilename
        NaiveBayes.__dataselect = dataselect

    @classmethod
    def __createmodel(cls):
        nb_model = MultinomialNB()
        return nb_model

    @classmethod
    def train(cls, target):
        try:
            train = DB_Communication.DB_Communication.get_data(cls.__dataselect)
            train.text = train.text.astype(str)
            df = pd.concat([train])
            #df.dropna()

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
