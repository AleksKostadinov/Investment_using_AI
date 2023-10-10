import requests
from decouple import config


url = 'https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey=config(alphavantage_API)'
r = requests.get(url)
data = r.json()

above_10 = [unemployment for unemployment in data['data'] if float(unemployment['value']) > 10]

for entry in above_10:
    print(f"Date: {entry['date']}, Value: {entry['value']}%")
