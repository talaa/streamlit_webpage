from cmath import inf
from logging import PlaceHolder
from turtle import onclick
import streamlit as st
import yfinance as yf
import pandas as pd
import sys
sys.path.append("../") 
from PIL import Image
import seaborn as sns

from Utilities.utilities import *
@st.cache
def next_business_day1(date1):
  test=0
  if (date1.dayofweek ==5):
    test=date1+timedelta(days=2)
    return test
  elif date1.dayofweek ==6:
    test=date1+timedelta(days=1)
    return test 
  else:
    return 0
def is_business_day1(date):
  if bool(len(pd.bdate_range(date, date))):
    return tick.history(start=date,end=date+ONE_DAY)
  elif bool(date.today()>next_business_day1(date)):
    return tick.history(start=next_business_day1(date),end=next_business_day1(date)+ONE_DAY)
  else:
    data={'Open':[0],'Close':[0],'Volume':[0]}
    df = pd.DataFrame(data)
    #df=pd.fillna()
    return df
def create_add_tick(dfi):
  #tick=tick2
  temp=[]
  dfi['tick']=dfi['datetime'].apply(is_business_day1)
  #dfi['tick']=dfi.apply(lambda x: is_business_day1(dfi['datetime'], tick2))
  temp=pd.DataFrame(dfi["tick"])
  #print(len(temp))
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
  res=pd.concat([dfi, vv.reindex(dfi.index)], axis=1)
  res=res.drop(['datetime','tick'],axis=1)
  #res['pos'] = ["{:.2%}".format(i) for i in res['pos'] ]
  #res['neg'] = ["{:.2%}".format(i) for i in res['neg'] ]
  #res['neu'] = ["{:.2%}".format(i) for i in res['neu'] ]
  #res['Open']= ["{:.2f}".format(i) for i in res['Open'] ]
  #res['Close']= ["{:.2f}".format(i) for i in res['Close'] ]
  return res
    
columnsTitles = ['title','news','datetime' ,'pos', 'neg','neu','Open','Close','Volume','link']

st.set_page_config(page_title="Financial Sentiment", page_icon="📈",layout="wide")
#st.markdown("# Financial Sentiment")
#st.sidebar.header("Financial Sentiment")
# Setup the Side bar 

option=st.sidebar.selectbox("Choose source",("Yahoo Finance","Google News","News Channels","Wallstreetbets"))

symbol=st.sidebar.text_input("Symbol",value='AAPL',placeholder="AAPL",max_chars=5)
submitted1 = st.sidebar.button(label = 'Search Symbol 🔎') 
tick = yf.Ticker(symbol)
info=tick.info
st.subheader(option)

#Switch Options

if (option == "Google News"):
  st.subheader(info['longName'])
  n=1
  gn=get_googlenews(symbol,n)
  tiset=create_add_tick(gn)
  tiset['datetime']=tiset.index
  tiset=tiset.reset_index(drop=True)
  
  #tiset['pos'] = ["{:.2%}".format(i) for i in tiset['pos'] ]
  #tiset['neg'] = ["{:.2%}".format(i) for i in tiset['neg'] ]
  #tiset['neu'] = ["{:.2%}".format(i) for i in tiset['neu'] ]
  
  #tiset = tiset.astype({'pos':'float','neg':'float','neu':'float'})
  #tiset['pos'] = tiset['pos'] .astype(float)
  #tiset['neg'] = tiset['neg'] .astype(float)
  #tiset['neu'] = tiset['neu'] .astype(float)
  #tiset["pos"] = pd.to_numeric(tiset["pos"], downcast="float")
  #print(tiset.dtypes)
  #tiset.style.format({'link': make_clickable})
  tiset=tiset.reindex(columns=columnsTitles)
  tiset = tiset.astype({'Open':'float','Close':'float','link':'string'})
  tiset['Move']=tiset['Close']-tiset['Open']
  #print(tiset.dtypes)
  #the Styling Part 
  ss=tiset.style.highlight_max(axis=1,subset=['pos','neg'], props='color:white; font-weight:bold; background-color:darkblue;')
  
  cm = sns.light_palette("green", as_cmap=True)
  cv= sns.light_palette("yellow",as_cmap=True)
  ss.background_gradient(cmap=cm,subset=['Volume'])
  ss.background_gradient(cmap=cv,subset=['Move'])
  
  ss.format({'neg':'{:.2%}','pos':'{:.2%}','neu':'{:.2%}','Open':'{:.2f}','Close':'{:.2f}','Volume':'{: ,}','link':make_clickable})
  #ss.format({'neu':'{:.2%}'})
  
  #tiset['More']=st.button('more')
  
  #st.dataframe(tiset.reset_index(drop=True).style.applymap(color_df, subset=['pos']))
  #tiset.style.set_properties(**{'background-color': 'black','color': 'green'},subset=['pos'])
  #ss
  st.write(ss.to_html(escape=False, index=False), unsafe_allow_html=True)
  #col11,col22,col33,col44,col55,col66,col77,col88,col99=st.columns((3,1,1,1,1,1,1,1,1))
 


if (option == "Yahoo Finance"):
  #Stocktwitssurl=f"https://api.stocktwits.com/api/2/streams/{symbol}.json"
  #tick = yf.Ticker(symbol)
  #
  # info=tick.info
  col1,col2,col3 =st.columns(3)
  with col1:
    st.subheader(symbol)
    st.subheader(info['longName'])
    st.text(info['sector'])
    st.text(info['industry'])
    #st.write(info['sector'])
  with col2:
    st.write("Open:",info['open'])
    st.write("Market Cap:",info['marketCap']/1000000,'M')
    st.write("Total Cash:",info['totalCash']/1000000,'M')
    st.write("Total Debt:",info['totalDebt']/1000000,'M')
  with col3:
    #image = Image.open(info['logo_url'])
    st.image(info['logo_url'])
    #st.markdown=(info['logo_url'])
  news=tick.news
  ne=pd.DataFrame(news)
  ne1=ne.drop(columns=['uuid', 'type','thumbnail'])
  ne1['providerPublishTime'] = pd.to_datetime(ne1['providerPublishTime'],unit='s')
  ne1

  
  st.write("---")
  left_column,right_column=st.columns(2)
  with left_column:
      st.write("financials")
      dd=pd.DataFrame(tick.financials)
      dd
  with right_column:
      st.write("Cash Flow")
      ff=pd.DataFrame(tick.cashflow)
      ff

# Use local CSS
#def local_css(file_name):
#    with open(file_name) as f:
#        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#local_css("style/style.css")



