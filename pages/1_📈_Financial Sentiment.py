from logging import PlaceHolder
import streamlit as st

st.set_page_config(page_title="Financial Sentiment", page_icon="📈")
#st.markdown("# Financial Sentiment")
#st.sidebar.header("Financial Sentiment")
# Setup the Side bar 
option=st.sidebar.selectbox("Choose source",("Twitter","Stocktwits,News Channels","Wallstreetbets"))

 
st.subheader(option)

#Switch Options

if (option == "Twitter"):
  st.subheader("This is the Twitter feeds")
if (option == "Stocktwits"):
  symbol=st.sidebar.text_input("Symbol",PlaceHolder="AAPL")
  Stocktwitssurl=f"https://api.stocktwits.com/api/2/streams/{symbol}.json"

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")


#the Form 
Tick_form="""
    <form action="" method="GET">
      <input type="Text" placeholder="Forexample:AAPL,Boeing,....." required>
      <button type="Submit">Check</button>
    </form>
    """
    
with st.container():
  #st.write("---")
  left_column,right_column=st.columns((1,2))
  with left_column:
    st.subheader("Check The company news")
    st.markdown(Tick_form,unsafe_allow_html=True)
with st.container():
    st.write("---")