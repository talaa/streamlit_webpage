import streamlit as st
import pandas as pd

st.set_page_config(page_title="News Stock Sentiment",page_icon=:crystal_ball:,layout="wide")
#Header Section 

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df
