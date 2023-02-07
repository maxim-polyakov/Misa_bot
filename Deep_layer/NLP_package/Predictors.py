import pickle as p
from tensorflow.keras.models import load_model
import numpy as np
from abc import ABC, abstractmethod
import Deep_layer.NLP_package.TextPreprocessers as TextPreprocessers

class IPredictor(ABC):

    @abstractmethod
    def predict(cls):
        pass

class BinaryLSTM(IPredictor):

    @classmethod
    def _preprocessing(cls, inpt, prep):
        inp = []
        if(prep == 'qu'):
            for i in inpt:
                pr = TextPreprocessers.QuestionPreprocessing()
                inp.append(pr.preprocess_text(i))
        elif(prep == 'command'):
            for i in inpt:
                pr = TextPreprocessers.CommandPreprocessing()
                inp.append(pr.preprocess_text(i))
        else:
            for i in inpt:
                pr = TextPreprocessers.CommonPreprocessing()
                inp.append(pr.preprocess_text(i))
        return inp

    @classmethod
    def predict(cls, inpt, tmap, model, tokenizer, prep):
            model = load_model(model)
            inn = []
            inn.append(cls._preprocessing(inpt, prep).pop())
            with open(tokenizer, 'rb') as handle:
                tokenizer = p.load(handle)
                tokenized_inpt = tokenizer.vectorize_input(inn)
            score = model.predict(tokenized_inpt)
            outpt = max(np.round(score).astype(int))
            cls.outscore = max(score)
            return(tmap[outpt[0]])


class NaiveBayes(BinaryLSTM):

    @classmethod
    def __preprocessing(cls, inpt, prep):
        return super()._preprocessing(inpt,prep)

    @classmethod
    def predict(cls, inpt, tmap, model, tokenizer, prep):

            with open(model, 'rb') as handle:
                model = p.load(handle)
            inn = []
            inn.append(cls.__preprocessing(inpt, prep).pop())
            pr = TextPreprocessers.CommonPreprocessing()
            with open(tokenizer, 'rb') as handle:
                tokenizer = p.load(handle)
                tokenized_inpt = tokenizer.transform(inn).toarray()

            cls.score = model.predict_proba(tokenized_inpt)
            return(tmap[cls.score.argmax(axis=-1)[0]])


class RandomForest(BinaryLSTM):

    @classmethod
    def predict(cls, inpt, tmap, model, tokenizer, prep):
        try:
            with open(model, 'rb') as handle:
                model = p.load(handle)
            inn = []
            inn.append(super()._preprocessing(inpt, prep).pop())
            with open(tokenizer, 'rb') as handle:
                tokenizer = p.load(handle)
            X_val = tokenizer.vectorize_input(inn)
            val_pred = model.predict(X_val)
            return(tmap[val_pred[0]])
        except:
            return 'The exeption is in RandomForest.predict'

class Xgboost(BinaryLSTM):

    @classmethod
    def predict(cls, inpt, tmap, model, tokenizer, prep):
        try:
            with open(model, 'rb') as handle:
                model = p.load(handle)
            inn = []
            inn.append(super()._preprocessing(inpt, prep).pop())
            with open(tokenizer, 'rb') as handle:
                tokenizer = p.load(handle)
            X_val = tokenizer.vectorize_input(inn)
            val_pred = model.predict(X_val)
            return (tmap[val_pred[0]])
        except:
            return 'The exeption is in Xgboost.predict'

class CombineModelBinary(IPredictor):


    def __init__(self, nbmodel, nbtokenizer, rfmodel, rftokenizer, lstmmodel, lstmtokenizer, xgboostmodel, xgbtokenizer):
        CombineModelBinary.nbmodel = nbmodel
        CombineModelBinary.nbtokenizer = nbtokenizer
        CombineModelBinary.rfmodel = rfmodel
        CombineModelBinary.rftokenizer = rftokenizer
        CombineModelBinary.lstmmodel = lstmmodel
        CombineModelBinary.lstmtokenizer = lstmtokenizer
        CombineModelBinary.xgboostmodel = xgboostmodel
        CombineModelBinary.xgbtokenizer = xgbtokenizer

    @classmethod
    def predict(cls, inpt, tmap):
        modelcount = 0
        answer = tmap[0]
        nbpred = NaiveBayes.predict(inpt, tmap, cls.nbmodel, cls.nbtokenizer, '')
        rfpred = RandomForest.predict(inpt, tmap, cls.rfmodel, cls.rftokenizer, '')
        lstmpred = BinaryLSTM.predict(inpt, tmap, cls.lstmmodel, cls.lstmtokenizer, '')
        xgbpred = Xgboost.predict(inpt,tmap,cls.xgboostmodel, cls.xgbtokenizer, '')

        if(nbpred == tmap[1]):
            modelcount = modelcount + 1
        if(rfpred == tmap[1]):
            modelcount = modelcount + 1
        if(nbpred == tmap[1]):
            modelcount = modelcount + 1
        if(lstmpred == tmap[1]):
            modelcount = modelcount + 1
        if(xgbpred ==tmap[1]):
            modelcount = modelcount + 1
        if(modelcount > 2):
            answer = tmap[1]
        return answer

class MultyLSTM(IPredictor):

    @classmethod
    def predict(cls, inpt, tmap, model, tokenizer):
        try:
            model = load_model(model)
            inp = []
            pr = TextPreprocessers.CommonPreprocessing()
            for i in inpt:
                inp.append(pr.preprocess_text(i))
                inn = []
                inn.append(inp.pop())
            with open(tokenizer, 'rb') as handle:
                tokenizer = p.load(handle)
            tokenized_inpt = tokenizer.vectorize_input(inn)
            scoreplu = model.predict(tokenized_inpt)
            outpt = tmap[scoreplu.argmax(axis=-1)[0]]
            return outpt
        except:
            return 'The exeption is in Multy.predict'
