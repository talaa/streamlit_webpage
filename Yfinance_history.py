import yfinance as yf
from datetime import datetime, timedelta

def get_historical_data(company, days_from_today):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_from_today)
    
    data = yf.download(company, start=start_date, end=end_date)
    #reverse ordering from newset to oldest 
    data = data.iloc[::-1]
    return data[['Open', 'Close', 'Volume']]