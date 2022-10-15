from termios import TIOCGLCKTRMIOS
import pandas as pd
import yfinance as yf
import requests
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from tqdm import tqdm
import datetime
import matplotlib.pyplot as plt
import tensorflow as tf
import torch
import re
import yfinance as yf
import holidays
import pickle
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers.experimental import preprocessing
from transformers import AutoTokenizer, AutoModelForSequenceClassification
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from tensorflow.keras.optimizers import Adam
import torch.nn.functional as F
import holidays
from  datetime import datetime,timedelta