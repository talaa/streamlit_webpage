import streamlit as st
import yfinance as yf
import pandas as pd 

tick = yf.Ticker('TWTR')
news=tick.news
ne=pd.DataFrame(news)
ne1=ne.drop(columns=['uuid', 'type','thumbnail'])
ne1['providerPublishTime'] = pd.to_datetime(ne1['providerPublishTime'],unit='s')

#st.write("[link](https://www.google.com)")
url_a="https://www.google.com"
url_b="https://www.apple.com"
a_link = st.multiselect("choose a link", [url_a,url_b])
# mock up of a user who can dynamically change the link, url_a and _b 
# need to be actual web addresses 

#text='check out this [link]({link1})'.format(link1=a_link)
st.markdown(a_link,unsafe_allow_html=True)



link1 = "https://stackoverflow.com/questions/71641666/hyperlink-in-streamlit-dataframe"
link2 = "https://stackoverflow.com/questions/71731937/how-to-plot-comparison-in-streamlit-dynamically-with-multiselect"
title=pd.DataFrame(['Streamlit','comparison'])
df = pd.DataFrame(
    {
        "url": [
            f'<a target="_blank" href="{link1}">'+title[0][0]+'</a>',
            f'<a target="_blank" href="{link2}">How to plot comparison in Streamlit dynamically with multiselect?</a>'
        ],
        "label": ["question", "question"]
    }
)

st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

 # # Show user table 
colms = st.columns((1, 2, 2, 1, 1))
fields = ["№", 'title', 'publisher', 'Time']
for col, field_name in zip(colms, fields):
# header
    col.write(field_name)

for x, email in enumerate(ne1['title']):
    title=""
    col1, col2, col3, col4, col5 = st.columns((.5, 3, 2, 1, 1))
    col1.write(x)  # index
    title=ne1['title'][x]
    link=ne1['link'][x]
    print(title,link)
    #link="https://www.google.com"
    text2='[({title})]({link2})'.format(link2=link)
    col2.markdown(text2,unsafe_allow_html=True)
    #col2.write('[{title}]'({link}))  # title
    col3.write(ne1['publisher'][x])  # publisher
    col4.write(ne1['providerPublishTime'][x])   # Publish Time
    #disable_status = ne1['relatedTracker'][x]  # flexible type of button
    disable_status=False
    button_type = "Unblock" if disable_status else "Block"
    button_phold = col5.empty()  # create a placeholder
    do_action = button_phold.button(button_type, key=x)
    if do_action:
        pass # do some action with a row's data
        button_phold.empty()  #  remove button       