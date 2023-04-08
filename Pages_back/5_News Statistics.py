from logging import PlaceHolder
import streamlit as st
import pandas as pd 
from newspaper import Article


st.set_page_config(page_title="Financial News Sentiment", page_icon="📈",layout="wide")

@st.cache
def check_url(link):
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    Authors=article.authors
    text=article.text
    Pub_date=article.publish_date
    Keywords=article.keywords
    summary=article.summary

    Data={
        'Authors':Authors,
        'text':text,
        'Publication Date':Pub_date,
        'Keywords':Keywords,
        'summary':summary
    }
    df =pd.Dataframe(Data)

    return link
with st.form("my_form"):
   #st.write("Inside the form")
   url_input=st.text_input('Link of the news Article',placeholder='Yahoo Finnance')

   #slider_val = st.slider("Form slider")
   #checkbox_val = st.checkbox("Form checkbox")

   # Every form must have a submit button.
   submitted = st.form_submit_button("Submit")
   if submitted:
    check_url(url_input)
      # st.write("slider", slider_val, "checkbox", checkbox_val)

