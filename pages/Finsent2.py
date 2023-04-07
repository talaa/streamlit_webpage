import streamlit as st
import numpy as np
import pandas as pd
from GoogleNews import GoogleNews
from datetime import datetime, timedelta
from newspaper import Article
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
#import tokenizers
from newspaper import Config
import nltk
@st.cache
def nltK():
    nltk.download('punkt')

st.title("Google News")
nltk
# Define the companies you want to get news for
company = st.text_input("Enter a company name", "Microsoft")
days = st.slider("Select number of days", 1, 7)

# Define the columns you want in your DataFrame
#columns = ["title", "datetime", "desc", "source", "article", "keywords", "Pos", "Neg", "Neutral"]
columns = ["title", "Pos", "Neg" ,"Neutral", "source","datetime","keywords","desc","article"]
# Create an empty DataFrame with the columns you defined
df = pd.DataFrame(columns=columns)

#definition of the config 
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = user_agent

# Define a custom hash function for tokenizers.Tokenizer
#def hash_tokenizer(tokenizer):
#    return tokenizer.get_vocab_size()

#init the cache 
# #Making Definitions for Sentiment analysis 
# Use @st.cache with hash_funcs argument to cache SentimentAnalyzer()
#@st.cache(hash_funcs={tokenizers.Tokenizer: hash_tokenizer})
@st.cache_resource
def SentimentAnalyzer(doc):
    pt_batch = tokenizer(doc,padding=True,truncation=True,max_length=512,return_tensors="pt")
    outputs = model(**pt_batch)
    pt_predictions = F.softmax(outputs.logits, dim=-1)
    return pt_predictions.detach().cpu().numpy()

# Definition for the highlight max 
def highlight_max(s, props=''):
    return np.where(s == np.nanmax(s.values), props, '')
# Create a GoogleNews object
googlenews = GoogleNews()

# Create an empty set to store unique article titles
unique_titles = set()

# Loop through each company and get the news articles
for i in range(1, 4):
    st.progress(i)
    googlenews.search(company + " financial news")
    googlenews.getpage(i)
    results = googlenews.result()

    # Loop through each article and add it to the DataFrame
    for result in results:
        # Filter articles based on number of days selected
        if result["datetime"] is None:
          continue
        if not isinstance(result["datetime"], datetime):
          continue
        date_str = result["datetime"].strftime('%Y-%m-%d %H:%M:%S.%f')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        if (datetime.now() - date_obj).days <= days and result['title'] not in unique_titles:
            unique_titles.add(result['title'])
            article = Article(result["link"],config=config)
            article.download()
            article.parse()
            article.nlp()
            sentiment = SentimentAnalyzer(article.text)
            #print(sentiment)
            df = pd.concat([df, pd.DataFrame({
                "title": [result["title"]],
                "datetime": [result["datetime"]],
                "desc": [result["desc"]],
                "source": [result["media"]],
                "article": [result["link"]],
                "keywords": [', '.join(article.keywords)],
                "Pos": [sentiment[0][0]],
                "Neg": [sentiment[0][1]],
                "Neutral": [sentiment[0][2]]
            })])

# Print the DataFrame
df['datetime'] = pd.to_datetime(df['datetime'],unit='s')
df[['Pos', 'Neg', 'Neutral']] = df[['Pos', 'Neg', 'Neutral']].apply(lambda x: x*100)
df.drop_duplicates(subset=['title'], inplace=True)
df = df.reset_index()
df.drop('index', axis=1, inplace=True)
df.set_index('datetime', inplace=True)
ss=df.style.highlight_max(axis=1,subset=['Pos','Neg','Neutral'], props='color:white; font-weight:bold; background-color:darkblue;')
ss