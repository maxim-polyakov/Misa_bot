import pickle as p
from Deep_layer.NLP_package.Classes.TextPreprocessers import CommonPreprocessing
from Deep_layer.NLP_package.Interfaces import IPredictor


class NaiveBayes(IPredictor.IPredictor):


    """

    This class is written for predictions of NaiveBayes classifier

    """
    score = None
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
                tokenized_inpt = tokenizer.transform(inn).toarray()

            cls.score = model.predict_proba(tokenized_inpt)

            return(tmap[cls.score.argmax(axis=-1)[0]])
        except:
            print('The exception is in NaiveBayes.predict')
