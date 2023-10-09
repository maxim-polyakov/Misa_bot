import pickle as p
from tensorflow.keras.models import load_model
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.NLP_package.Interfaces import IPredictor


class MultyLSTM(IPredictor.IPredictor):


    @classmethod
    def predict(cls, inpt, tmap, model, tokenizer):
        try:
            model = load_model(model)

            inn = []
            pr = CommonPreprocessing.CommonPreprocessing()
            for i in inpt:
                inn.append(pr.preprocess_text(i))

            with open(tokenizer, 'rb') as handle:
                tokenizer = p.load(handle)

            tokenized_inpt = tokenizer.vectorize_input(inn)
            scoreplu = model.predict(tokenized_inpt)
            outpt = tmap[scoreplu.argmax(axis=-1)[0]]
            return outpt
        except:
            return 'The exeption is in MultyLSTM.predict'