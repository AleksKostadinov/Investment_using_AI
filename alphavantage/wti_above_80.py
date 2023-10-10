import requests
from decouple import config

url = 'https://www.alphavantage.co/query?function=WTI&interval=monthly&apikey=config(alphavantage_API)'
r = requests.get(url)
data = r.json()

above_80 = [cost for cost in data['data'] if float(cost['value']) > 80]

for entry in above_80:
    print(f"Date: {entry['date']}, Value: {entry['value']}")
