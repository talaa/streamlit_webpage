import streamlit as st
import requests
import datetime
from transformers import pipeline

# Set up the sentiment analysis pipeline
sentiment_analysis_pipeline = pipeline("sentiment-analysis")

# Set up a dictionary to cache news articles
news_cache = {}

# Define the cache expiration time (in minutes)
CACHE_EXPIRATION_TIME_MINUTES = 30


def get_news_articles(company_symbol, days_back):
    """
    Fetch news articles about a given company from the last N days using the Google News API.
    Cache the results to avoid making unnecessary API requests.
    """
    # Check if the data is already cached
    cache_key = f"{company_symbol}_{days_back}"
    if cache_key in news_cache:
        cached_data, timestamp = news_cache[cache_key]
        if (datetime.datetime.now() - timestamp).total_seconds() / 60 < CACHE_EXPIRATION_TIME_MINUTES:
            return cached_data

    # Fetch news articles from the Google News API
    query_params = {
        "q": company_symbol,
        "tbm": "nws",
        "qdr": f"{days_back}d",
        "api": "http://newsapi.org/v2/top-headlines",
        "apiKey": "90a92466fbmsh379406da26fd50fp1854bejsn791cb2eb2dc6"
    }
    response = requests.get(query_params["api"], params=query_params)
    response_data = response.json()

    # Cache the response data with the current timestamp
    news_cache[cache_key] = (response_data, datetime.datetime.now())

    return response_data


def display_article(article):
    """
    Display the details of a single news article, including the headline, source, publication time,
    article text, and sentiment analysis.
    """
    st.subheader(article["title"])
    st.write("Source:", article["source"]["name"])
    st.write("Published at:", article["publishedAt"])
    st.write(article["description"])
    st.write("Sentiment analysis:")
    result = sentiment_analysis_pipeline(article["description"])[0]
    st.code(str(result), language="python")


def display_articles(articles):
    """
    Display the details of multiple news articles, including the headline, source, publication time,
    article text, and sentiment analysis.
    """
    for article in articles:
        display_article(article)
        st.markdown("---")


# Set up the Streamlit app
st.title("Financial Sentiment Analysis")
company_symbol = st.text_input("Enter a company symbol (e.g. AAPL):")
days_back = st.slider("Select the number of days to look back for news articles:", 1, 7, 3)

if st.button("Search"):
    # Fetch news articles from the Google News API and perform sentiment analysis
    articles = get_news_articles(company_symbol, days_back)["articles"]
    if not articles:
        st.write("No news articles found.")
    else:
        st.write(f"Displaying {len(articles)} news articles:")
        display_articles(articles)
