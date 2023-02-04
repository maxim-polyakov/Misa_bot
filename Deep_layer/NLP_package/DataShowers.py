from Deep_layer import NLP_package
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

class SnsShower(IDataShower):

    @classmethod
    def showdata(self, train, target):
        try:
            key_metrics = {'samples': len(train),
                        'samples_per_class': train[target].value_counts().median(),
                        'median_of_samples_lengths': np.median(train['text'].str.split().map(lambda x: len(x)))}
            key_metrics = pd.DataFrame.from_dict(
                key_metrics, orient='index').reset_index()
            key_metrics.columns = ['metric', 'value']
            green = '#52BE80'
            red = '#EC7063'
            sns.countplot(train[target], palette=[green, red])
        except:
            print('The exception in SnsShower.showdata')


