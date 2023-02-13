import pickle as p
from tensorflow.keras.models import load_model
import Deep_layer.NLP_package.TextPreprocessers as TextPreprocessers
from Deep_layer.NLP_package.Predictors import IPredictor

class MultyLSTM(IPredictor.IPredictor):

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