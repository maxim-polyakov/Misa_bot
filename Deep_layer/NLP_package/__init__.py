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
from Deep_layer.DB_package import DB_Bridge
from sklearn.metrics import accuracy_score
from enum import Enum
import xgboost

from Deep_layer.NLP_package import TextPreprocessers
from Deep_layer.NLP_package import ResultSavers
from Deep_layer.NLP_package import Tokenizers