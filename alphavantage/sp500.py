import requests
from decouple import config


url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=SPY&apikey=config(alphavantage_API)'
r = requests.get(url)
data = r.json()

m_date = list(data['Monthly Time Series'].keys())
close = [data['Monthly Time Series'][date]['4. close'] for date in m_date]

# Print the monthly dates and corresponding "close" values
for date, close_value in zip(m_date, close):
    print(f"Date: {date}, Close: {close_value}")
