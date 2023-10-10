import requests
from decouple import config


url = 'https://www.alphavantage.co/query?function=INFLATION&apikey=config(alphavantage_API)'
r = requests.get(url)
data = r.json()

above_10 = [inflation for inflation in data['data'] if float(inflation['value']) > 10]

for entry in above_10:
    print(f"Date: {entry['date']}, Value: {entry['value']}%")
