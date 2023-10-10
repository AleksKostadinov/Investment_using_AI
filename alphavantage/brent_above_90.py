import requests
from decouple import config

url = 'https://www.alphavantage.co/query?function=BRENT&interval=monthly&apikey=config(alphavantage_API)'
r = requests.get(url)
data = r.json()

above_90 = [cost for cost in data['data'] if float(cost['value']) > 90]

for entry in above_90:
    print(f"Date: {entry['date']}, Value: {entry['value']}")
