from pathlib import Path
from Deep_layer.NLP_package.Classes.Models.Multy import MultyLSTM
from Deep_layer.NLP_package.Classes.Models.Binary import BinaryLSTM
from Core_layer.Bot_package.Classes import Selects
from Core_layer.Bot_package.Classes import LSTMtrain
import os


class BinaryLSTMtrain(LSTMtrain.LSTMtrain):
    """

    This method is written for traning models

    """
    sel = Selects.Select()

    filemodel = None
    filetokenizer = None
    datasetfile = None
    target = None

    sel = Selects.Select()

    trainerBinary = BinaryLSTM.BinaryLSTM(filemodel, filetokenizer, datasetfile)
    trainerMulty = MultyLSTM.MultyLSTM(filemodel, filetokenizer, datasetfile)

    def __init__(self, filemodel, filetokenizer, datasetfile, target, epochs):
        BinaryLSTMtrain.filemodel = filemodel
        BinaryLSTMtrain.filetokenizer = filetokenizer
        BinaryLSTMtrain.datasetfile = datasetfile
        BinaryLSTMtrain.target = target

    @classmethod
    def train(cls, epochs):
        #
        #
        try:
            cls.trainer.train(cls.target, epochs)
        except:
            pass