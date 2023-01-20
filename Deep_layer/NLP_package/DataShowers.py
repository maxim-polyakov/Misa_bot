from Deep_layer import NLP_package


class IDataShower(NLP_package.ABC):

    @NLP_package.abstractmethod
    def showdata(self,train,target):
        pass

class SnsShower(IDataShower):

    @classmethod
    def showdata(self, train, target):
        try:
            key_metrics = {'samples': len(train),
                        'samples_per_class': train[target].value_counts().median(),
                        'median_of_samples_lengths': NLP_package.np.median(train['text']
                                                                           .str.split().map(lambda x: len(x))),
                        }
            key_metrics = NLP_package.pd.DataFrame.from_dict(
                key_metrics, orient='index').reset_index()
            key_metrics.columns = ['metric', 'value']
            green = '#52BE80'
            red = '#EC7063'
            NLP_package.sns.countplot(train[target], palette=[green, red])
        except:
            print('The exception in SnsShower.showdata')


