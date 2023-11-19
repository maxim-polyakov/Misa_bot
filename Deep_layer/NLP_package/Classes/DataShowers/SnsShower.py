import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')
import numpy as np
import pandas as pd
from Deep_layer.NLP_package.Interfaces import IDataShower


class SnsShower(IDataShower.IDataShower):
    """

    Summary

    """
    @classmethod
    def showdata(self, train, target):
        try:
            path = 'Data.png'
            key_metrics = {'samples': len(train),
                           'samples_per_class': train[target].value_counts().median(),
                           'median_of_samples_lengths': np.median(train['text'].str.split().map(lambda x: len(x))),
                           }
            key_metrics = pd.DataFrame.from_dict(key_metrics, orient='index').reset_index()
            key_metrics.columns = ['metric', 'value']
            print(key_metrics)
            green = '#52BE80'
            red = '#EC7063'
            sns_plot = sns.countplot(train[target], palette=[green, red])
            fig = sns_plot.get_figure()
            fig.savefig(path)
            return path
        except:
            print('The exception is in SnsShower.showdata')



