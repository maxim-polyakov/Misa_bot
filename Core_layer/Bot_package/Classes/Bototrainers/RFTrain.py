from pathlib import Path
from Deep_layer.NLP_package.Classes.Models.Multy import RandomForest
from Core_layer.Bot_package.Classes import Selects
from Core_layer.Bot_package.Interfaces import ITrainer


class RFtrain(ITrainer.ITrainer):


    """

    This method is written for traning models

    """
    filemodel = None
    filetokenizer = None
    datasetfile = None
    target = None

    sel = Selects.Select()
    trainer = RandomForest.RandomForest(filemodel, filetokenizer, datasetfile)

    def __init__(self, filemodel, filetokenizer, datasetfile, target):
        RFtrain.filemodel = filemodel
        RFtrain.filetokenizer = filetokenizer
        RFtrain.datasetfile = datasetfile
        RFtrain.target = target

    @classmethod
    def train(cls):
        try:
            cls.trainer.train(cls.target)
            return "trained"
        except:
            return "The exception is in RFtrain.train"


