from abc import ABC, abstractmethod

class IPredictor(ABC):


    """

    This entity is written for a preprocessiong of text column in a DataFrame

    """
    @abstractmethod
    def predict(cls, inpt, tmap, model, tokenizer):
        pass