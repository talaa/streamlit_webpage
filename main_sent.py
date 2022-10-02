import streamlit as st
import pandas as pd
import requests

from streamlit_lottie import st_lottie

st.set_page_config(page_title="News Stock Sentiment",page_icon=":crystal_ball:",layout="wide")

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

with st.container():
  st.write("---")
  left_column,right_column=st.columns((1,2))
  with left_column:
    Tick_form="""
    <form action="" method="GET">
    <input type="Text" placeholer="Forexample:AAPL,Boeing,....." required>
    <button type="Submit">Check</button>
    </form>
    """

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

#df
Data_df=pd.read_json(test.json, lines=True)
Data_df
