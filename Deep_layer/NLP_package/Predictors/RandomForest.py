import pickle as p
from Deep_layer.NLP_package.TextPreprocessers import CommonPreprocessing
from Deep_layer.NLP_package.Predictors import IPredictor

class RandomForest(IPredictor.IPredictor):

    @classmethod
    def predict(cls, inpt, tmap, model, tokenizer):


        try:
            with open(model, 'rb') as handle:
                model = p.load(handle)
            inn = []
            pr = CommonPreprocessing.CommonPreprocessing()
            for i in inpt:
                inn.append(pr.preprocess_text(i))

            with open(tokenizer, 'rb') as handle:
                tokenizer = p.load(handle)
            x_val = tokenizer.vectorize_input(inn)
            val_pred = model.predict(x_val)
            return(tmap[val_pred[0]])
        except:
            return 'The exeption is in RandomForest.predict'