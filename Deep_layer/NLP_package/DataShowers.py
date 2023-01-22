from Deep_layer import NLP_package
from tensorflow.keras.models import load_model
import psycopg2
from tensorflow.keras.optimizers import Adam

from keras.layers import Embedding, LSTM, Dense, Dropout, GRU, Input
from keras.models import Sequential

from nltk.corpus import stopwords
import pickle as p
import keras
from keras import backend as K
from keras.preprocessing import text
#from keras.preprocessing import sequence
import requests
import tqdm as tqdm
from string import punctuation
from pymystem3 import Mystem
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.initializers import Constant
from tensorflow.keras.callbacks import EarlyStopping
from tqdm import tqdm

from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
import string
#import gensim
import re
import pandas as pd
import tensorflow as tensorflow
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from tensorflow.keras.models import load_model
import spacy
import category_encoders as ce
import random
plt.style.use('ggplot')
import re
import string
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import CategoricalEncoder
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, LSTM, Embedding, Bidirectional
from abc import ABC, abstractmethod


class IDataShower(ABC):

    @abstractmethod
    def showdata(self,train,target):
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
            NLP_package.sns.countplot(train[target], palette=[green, red])
        except:
            print('The exception in SnsShower.showdata')


