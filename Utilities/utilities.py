#from termios import TIOCGLCKTRMIOS
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
#import symbol
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
import sys
sys.path.append("../") 



ONE_DAY = timedelta(days=1)

HOLIDAYS_US = holidays.US()


#Google News Setup
googlenews = GoogleNews()

googlenews = GoogleNews(lang='en', region='US')
googlenews = GoogleNews(period='7d')
googlenews = GoogleNews(encode='utf-8')

#newsPaper Setup

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()

config.browser_user_agent = user_agent

# The Definitions
#def get_googlenews(tick):
#  googlenews.clear()
#    googlenews.get_news(tick)
#    x=pd.DataFrame(googlenews.results())
#    x1=x.drop(['date','img'],axis=1)
#    x1['datetime']=pd.to_datetime(x1['datetime'],unit='s')
#    return x1

def get_article(url):
  article=Article(url,config=config)
  article.download()
  article.parse()
  article.nlp()
  return article.summary,article.authors,article.keywords,article.publish_date
def getfinalurl(starturl):
  req = requests.get("http://"+starturl)
  #res = urllib.urlopen(req)
  return req.url
def SentimentAnalyzer(doc):
    pt_batch = tokenizer(doc,padding=True,truncation=True,max_length=512,return_tensors="pt")
    outputs = model(**pt_batch)
    pt_predictions = F.softmax(outputs.logits, dim=-1)
    return pt_predictions.detach().cpu().numpy()
''''
def next_business_day1(date1):
  test=0
  if (date1.dayofweek ==5):
    test=date1+timedelta(days=2)
    return test
  elif date1.dayofweek ==6:
    test=date1+timedelta(days=1)
    return test 
  else:
    return 'NA'
def is_business_day1(date):
  if bool(len(pd.bdate_range(date, date))):
    return tick.history(start=date,end=date+ONE_DAY)
  elif bool(date.today()>next_business_day1(date)):
    return tick.history(start=next_business_day1(date),end=next_business_day1(date)+ONE_DAY)
  else:
    return 'NA'
'''
def get_googlenews(tick1,n):
    x=[]
    title=[]
    date=[]
    datetime=[]
    desc=[]
    link=[]
    sent=[]
    googlenews.clear()
    googlenews.get_news(tick1)
    googlenews.search(tick1)
    for i in range(n):
      
      googlenews.get_page(n)
      x.append(googlenews.results())
    
    nn=pd.DataFrame(x).T
    for i in range(len(nn)):
      title.append(nn[0][i]['title'])
      date.append(nn[0][i]['date'])
      datetime.append(nn[0][i]['datetime'])
      desc.append(nn[0][i]['desc'])
      link.append(nn[0][i]['link'])
      sentimentArr = SentimentAnalyzer(nn[0][i]['title'])
      sent.append(np.mean(sentimentArr, axis=0))
    Data={
        "title":title,
        "desc":desc,
        "date":date,
        "datetime":datetime,
        "link":link,
        "sentiment":sent
    }

    df = pd.DataFrame(Data)
    df=df.dropna(subset=['datetime'])
    df['datetime']=df['datetime'].dt.date
    df[['pos','neg','neu']] =pd.DataFrame(df.sentiment.tolist(), index= df.index)
    df=df.sort_values(by='datetime', ascending=False)
    df=df.drop(['date','desc','sentiment'],axis=1)
    df=df.set_index('datetime')
    df.index = pd.to_datetime(df.index)
    df['datetime']=df.index
    #df1=create_add_tick(df)
    #x1=x.drop(['media','img'],axis=1)
    #x1['datetime']=pd.to_datetime(x1['datetime'],unit='s').dt.date
    
    return df
def make_clickable(link):
    
    return  f'<a target="_blank" href="{link}">{link}</a>'
def change_cell_color(val):
  if val>.5:
    return 1#df.style.set_properties(**{'background-color': 'black','color': 'green'})
'''
def create_add_tick(dfi):
  #tick=tick2
  dfi['tick']=dfi['datetime'].apply(is_business_day1)
  #dfi['tick']=dfi.apply(lambda x: is_business_day1(dfi['datetime'], tick2))
  temp=pd.DataFrame(dfi["tick"])
  #print(temp)
  Open=[]
  Close=[]
  Volume=[]
  for i in range(len(temp.tick)):
    #print(temp.tick[i].Open.values[0])
    Open.append(temp.tick[i].Open.values[0])
    Close.append(temp.tick[i].Close.values[0])
    Volume.append(temp.tick[i].Volume.values[0])
    
  tt={
      "Open":Open,
      "Close":Close,
      "Volume":Volume
  }
  vv=pd.DataFrame(tt,index=temp.index)
  res=pd.concat([gg, vv.reindex(gg.index)], axis=1)
  res=res.drop(['datetime','tick'],axis=1)
  #res['pos'] = ["{:.2%}".format(i) for i in res['pos'] ]
  #res['neg'] = ["{:.2%}".format(i) for i in res['neg'] ]
  #res['neu'] = ["{:.2%}".format(i) for i in res['neu'] ]
  res['Open']= ["{:.2f}".format(i) for i in res['Open'] ]
  res['Close']= ["{:.2f}".format(i) for i in res['Close'] ]
  return res
'''