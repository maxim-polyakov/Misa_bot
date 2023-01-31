from keras.layers import Embedding, LSTM, Dense, Dropout, GRU, Input
from keras.models import Sequential
import pickle as p
import tensorflow as tensorflow
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from tensorflow.keras.models import load_model
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, LSTM, Embedding, Bidirectional
from abc import ABC, abstractmethod
from Deep_layer.DB_package import DB_Bridge
import xgboost
from Deep_layer.NLP_package import Tokenizers
from Deep_layer.NLP_package import ResultSavers
from pymystem3 import Mystem
from nltk.corpus import stopwords
from string import punctuation
import spacy
import re
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
DEVICE = torch.device('cpu')

class IGpt(ABC):

    @abstractmethod
    def generate(self):
        pass

class Gpt(IGpt):
    @classmethod
    def generate(cls, text):
        model_name_or_path = "sberbank-ai/rugpt3large_based_on_gpt2"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
        model = GPT2LMHeadModel.from_pretrained(model_name_or_path).to(DEVICE)
        input_ids = tokenizer.encode(text, return_tensors="pt").to(DEVICE)
        out = model.generate(input_ids, do_sample=False)
        generated_text = list(map(tokenizer.decode, out))[0]
        return generated_text.replace('\xa0', ' ').replace('\n','').replace(text,'').replace('—', '')