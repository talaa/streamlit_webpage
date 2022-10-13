from logging import PlaceHolder
import streamlit as st
import yfinance as yf
import pandas as pd
import sys
sys.path.append("../") 
 
from Utilities.utilities import *



st.set_page_config(page_title="Financial Sentiment", page_icon="📈",layout="wide")
#st.markdown("# Financial Sentiment")
#st.sidebar.header("Financial Sentiment")
# Setup the Side bar 

option=st.sidebar.selectbox("Choose source",("Yahoo Finance","Google News","News Channels","Wallstreetbets"))

symbol=st.sidebar.text_input("Symbol",placeholder="AAPL",max_chars=5)
 
st.subheader(option)

#Switch Options

if (option == "Google News"):
  st.subheader("This is the Google news")
  n=4
  gn=get_googlenews(symbol,n)
  tiset=create_add_tick(gn)
  tiset

if (option == "Yahoo Finance"):
  #Stocktwitssurl=f"https://api.stocktwits.com/api/2/streams/{symbol}.json"
  tick = yf.Ticker(symbol)
  st.header(symbol)
  info=tick.info['longName']
  
  st.subheader(info['sector'])
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
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")



    

