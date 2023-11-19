import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod

class IDataShower(ABC):


    """

    This entyty describes a showing of data and loking it in picture

    """

    @abstractmethod
    def showdata(self, train, target):
        pass