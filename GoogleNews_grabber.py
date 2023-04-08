import pandas as pd
from GoogleNews import GoogleNews
from datetime import datetime
from newspaper import Article,Config


def googlenews_C(company):
    # Define the columns you want in your DataFrame
    columns = ["title", "source","datetime","desc","article"]
    days=3
    # Create an empty DataFrame with the columns you defined
    df = pd.DataFrame(columns=columns)
    #definition of the config 
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
    config = Config()
    config.browser_user_agent = user_agent
    # Create a GoogleNews object
    googlenews = GoogleNews()

    # Create an empty set to store unique article titles
    unique_titles = set()
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
            if not isinstance(result["datetime"], datetime):
                continue
            date_str = result["datetime"].strftime('%Y-%m-%d %H:%M:%S.%f')
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
            if (datetime.now() - date_obj).days <= days and result['title'] not in unique_titles:
                unique_titles.add(result['title'])
                article = Article(result["link"],config=config)
                article.download()
                article.parse()
                article.nlp()
                
                #print(sentiment)
                df = pd.concat([df, pd.DataFrame({
                    "title": [result["title"]],
                    "datetime": [result["datetime"]],
                    "desc": [result["desc"]],
                    "source": [result["media"]],
                    "article": [result["link"]],
                    "keywords": [', '.join(article.keywords)]
                    
                })])

    # Print the DataFrame
    df['datetime'] = pd.to_datetime(df['datetime'],unit='s')
    
    df.drop_duplicates(subset=['title'], inplace=True)
    df = df.reset_index()
    df.drop('index', axis=1, inplace=True)
    df.set_index('datetime', inplace=True)
    return df