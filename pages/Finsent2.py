import streamlit as st
import pandas as pd
from GoogleNews import GoogleNews

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
googlenews.search(company + " financial news")
googlenews.getpage(1)
results = googlenews.result()

# Loop through each article and add it to the DataFrame
for result in results:
    if "source" in result:
        source = result["source"]
    else:
        source = ""

    df = pd.concat([df, pd.DataFrame({
        "title": [result["title"]],
        "datetime": [result["datetime"]],
        "desc": [result["desc"]],
        "source": [result["media"]],
        "article": [result["link"]]
    })])

# Print the DataFrame
st.write(df.head())