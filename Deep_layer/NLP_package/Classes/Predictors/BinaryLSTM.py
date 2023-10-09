import pickle as p
from tensorflow.keras.models import load_model
import numpy as np
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.NLP_package.Interfaces import IPredictor


class BinaryLSTM(IPredictor.IPredictor):
    """

    Summary

    """
    @classmethod
    def predict(cls, inpt, tmap, model, tokenizer):
            model = load_model(model)

            inn = []
            pr = CommonPreprocessing.CommonPreprocessing()
            for i in inpt:
                inn.append(pr.preprocess_text(i))

            with open(tokenizer, 'rb') as handle:
                tokenizer = p.load(handle)
                tokenized_inpt = tokenizer.vectorize_input(inn)

            score = model.predict(tokenized_inpt)
            outpt = max(np.round(score).astype(int))
            cls.outscore = max(score)
            return(tmap[outpt[0]])