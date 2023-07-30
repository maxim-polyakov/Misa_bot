import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

class IDataShower(ABC):

    @abstractmethod
    def showdata(self, train, target):
        pass