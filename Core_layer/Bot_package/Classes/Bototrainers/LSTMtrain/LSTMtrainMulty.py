from pathlib import Path
from Deep_layer.NLP_package.Classes.Models.Multy import MultyLSTM
from Deep_layer.NLP_package.Classes.Models.Binary import BinaryLSTM
from Core_layer.Bot_package.Classes import Selects
from Core_layer.Bot_package.Interfaces import ITrainer
import os

class MultyLSTMtrain:

    filemodel = None
    filetokenizer = None
    datasetfile = None
    target = None
    def __init__(self, filemodel, filetokenizer, datasetfile, target, epochs):
        MultyLSTMtrain.filemodel = filemodel
        MultyLSTMtrain.filetokenizer = filetokenizer
        MultyLSTMtrain.datasetfile = datasetfile
        MultyLSTMtrain.target = target