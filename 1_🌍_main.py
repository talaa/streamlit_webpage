import streamlit as st
import pandas as pd
import requests
import json
#import sys
#sys.path.insert(0, '/Utilities/GoogleNews_grabber')

from GoogleNews_grabber import googlenews_C
from Yfinance_history import get_historical_data


from streamlit_lottie import st_lottie

st.set_page_config(page_title="News Stock Sentiment",page_icon=":crystal_ball:",layout="wide")
@st.cache
#Load Assets
def load_lottie(url):
  r=requests.get(url)
  if r.status_code != 200 :
    return None
  return r.json()
lottie_file=load_lottie("https://assets4.lottiefiles.com/packages/lf20_597nlu.json")
# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")
#Header Section 
with st.container():
  up_left_column,up_right_column=st.columns(2)
  with up_left_column:
    st.title("Finanical News Analysis")
    st.subheader("This is Financial News Sentiment Analysis")
  with up_right_column:
    st_lottie(lottie_file,height=300,key="Financial News")
#the Form 
#Tick_form="""
#    <form action="" method="GET">
#      <input type="Text" placeholder="Forexample:AAPL,Boeing,....." required>
#      <button type="Submit">Check</button>
#    </form>
#    """


with st.container():
  st.write("---")
  left_column,right_column=st.columns((1,2))
  with left_column:
    st.subheader("Check The company news")
    #st.markdown(Tick_form,unsafe_allow_html=True)
    with st.form("my_form"):
      
      tick_val=st.text_input("Enter the Tick Name","AAPL")
      days_back = st.slider("Select the number of days to look back for news articles:", 1, 7, 3)

      # Every form must have a submit button.
      submitted = st.form_submit_button("Submit")
      if submitted:
          st.write("Pease Wait")
with st.container():
  st.write("---")
  #Data_df=pd.read_json('test.json')
  Data_df =googlenews_C(tick_val,days_back)
  Data_df
with st.container():
  st.write("---")
  #company_symbol = st.text_input("Enter a company symbol (e.g. AAPL):")
  
  tick_df =get_historical_data(tick_val,days_back)
  tick_df
  

#df
#f = open('test.json')
#t=json.load(f)

