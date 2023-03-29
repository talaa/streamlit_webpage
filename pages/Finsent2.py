import streamlit as st
import pandas as pd
from GoogleNews import GoogleNews
from datetime import datetime, timedelta

st.title("Google News")

# Define the companies you want to get news for
company = st.text_input("Enter a company name", "Microsoft")
days = st.slider("Select number of days", 1, 30)

# Define the columns you want in your DataFrame
columns = ["title", "datetime", "desc", "source", "article"]

# Create an empty DataFrame with the columns you defined
df = pd.DataFrame(columns=columns)

# Create a GoogleNews object
googlenews = GoogleNews()

# Loop through each company and get the news articles
for i in range(1, 4):
    googlenews.search(company + " financial news")
    googlenews.getpage(i)
    results = googlenews.result()

    # Loop through each article and add it to the DataFrame
    for result in results:
        # Filter articles based on number of days selected
        if result["datetime"] is None:
          continue
        date_str = result["datetime"].strftime('%Y-%m-%d %H:%M:%S.%f')
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
        if (datetime.now() - date_obj).days <= days:
            df = pd.concat([df, pd.DataFrame({
                "title": [result["title"]],
                "datetime": [result["datetime"]],
                "desc": [result["desc"]],
                "source": [result["media"]],
                "article": [result["link"]]
            })])

# Print the DataFrame
st.write(df.head())