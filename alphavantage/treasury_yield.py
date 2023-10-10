import requests
from decouple import config


url = 'https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=config(alphavantage_API)'
r = requests.get(url)
data = r.json()

tresury_above_4 = [i for i in data['data'] if float(i['value']) > 4]


for entry in tresury_above_4:
    print(f"Date: {entry['date']}, Value: {entry['value']}%")
