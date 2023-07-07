from pathlib import Path
from Deep_layer.NLP_package.Predictors import BinaryLSTM, MultyLSTM
from Core_layer.Answer_package.Answers.Classes import QuestionAnswer, RandomAnswer
from Deep_layer.NLP_package import Mapas
from Deep_layer.NLP_package.TextPreprocessers import CommonPreprocessing
from Deep_layer.DB_package.DB_Bridge import DB_Communication
from Core_layer.Bot_package.Monitors import IMonitor
import os

class PictureMonitor(IMonitor):

    def monitor(self):
        pass