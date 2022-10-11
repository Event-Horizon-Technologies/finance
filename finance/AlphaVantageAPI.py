import requests
import json

TIME_SERIES = 'INTRADAY'
SYMBOL = 'TSLA'
INTERVAL = '5min'
API_KEY = 'ZZ7E9KFFYTKGZ0XR'

if TIME_SERIES == 'INTRADAY':
    URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_{TIME_SERIES}&symbol={SYMBOL}&interval={INTERVAL}&apikey={API_KEY}'
else:
    URL = f'https://www.alphavantage.co/query?function=TIME_SERIES_{TIME_SERIES}&symbol={SYMBOL}&apikey={API_KEY}'

    

r = requests.get(URL)
data = r.json()