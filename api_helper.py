import ccxt #  https://github.com/ccxt/ccxt/tree/master/python
import time
from datetime import datetime
import plotly.graph_objects as go
import requests
import json

# print(ccxt.exchanges)



binance = ccxt.binanceus()
markets = binance.load_markets()

# Grabs and charts coin Data

def chartCoin(symbol):
    
    btc_usd_ohlcv = binance.fetch_ohlcv(symbol,'1d',limit=100)
    dates = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    for candle in btc_usd_ohlcv:
        dates.append(datetime.fromtimestamp(candle[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f'))
        open_data.append(candle[1])
        high_data.append(candle[2])
        low_data.append(candle[3])
        close_data.append(candle[4])

    fig = go.Figure(data=[go.Candlestick(x=dates,
                        open=open_data, high=high_data,
                        low=low_data, close=close_data)])
    
    return fig

# Holds all current coins in exchange

currencies = binance.currencies
coinSet = set()
optionList = []
for c in currencies:
    if currencies[c]['id'] not in coinSet:
        coinSet.add(currencies[c]['id'])
for coin in coinSet:
    optionList.append({'label': coin ,'value': coin+'/'+'USD'})
    
    
def grabAvg(symbol):
    request = requests.get('https://api.binance.us/api/v3/avgPrice?symbol=' + symbol + 'USD')
    json = request.json()
    return json['price']

grabAvg('BTC')