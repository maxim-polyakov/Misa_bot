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
