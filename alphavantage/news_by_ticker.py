import requests
from decouple import config

try:
    ticker = input("Enter a ticker: ").upper()
    time_from = input("Enter a time from: ")

    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='
    url += ticker
    url += '&time_from=' + time_from +'T0130'
    url += '&apikey=config(alphavantage_API)'

    r = requests.get(url)
    data = r.json()
    print(data)
    ticker_feed = [feed for feed in data['feed']]

    for entry in ticker_feed:
        print(f"Title: {entry['title']}\nURL: {entry['url']}")
        print("="*50)

except Exception as e:
    print(e)
    print("="*50)
    print("Please try again.")
    print("="*50)

