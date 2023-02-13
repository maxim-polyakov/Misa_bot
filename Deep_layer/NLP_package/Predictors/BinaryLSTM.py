import pickle as p
from tensorflow.keras.models import load_model
import numpy as np
from Deep_layer.NLP_package.TextPreprocessers import QuestionPreprocessing, CommandPreprocessing, CommonPreprocessing
from Deep_layer.NLP_package.Predictors import IPredictor

class BinaryLSTM(IPredictor.IPredictor):

    @classmethod
    def _preprocessing(cls, inpt, prep):
        inp = []
        if(prep == 'qu'):
            for i in inpt:
                pr = QuestionPreprocessing.QuestionPreprocessing()
                inp.append(pr.preprocess_text(i))
        elif(prep == 'command'):
            for i in inpt:
                pr = CommandPreprocessing.CommandPreprocessing()
                inp.append(pr.preprocess_text(i))
        else:
            for i in inpt:
                pr = CommonPreprocessing.CommonPreprocessing()
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