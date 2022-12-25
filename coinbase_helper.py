import pandas as pd
from coinapi_rest_v1.restapi import CoinAPIv1
import constants

# API as class from CoinAPI Library
api = CoinAPIv1(constants.CBAPIKey)

# Grabbing all symbol metadata
symbolsResponse = api.metadata_list_symbols(query_parameters={"filter_exchange_id": 'BINANCE'})
# symbolSet = set(x['asset_id_base'] for x in symbolsResponse)
coinSet = set()
symbolSet = set()
symbolDictList = []
# for x in symbolSet:
#     n = {}
#     n['label'] = x
#     n['value'] = x
#     symbolDictList.append(n)

for x in symbolsResponse:
    if x['asset_id_base'] not in coinSet and x['asset_id_quote'] == 'USD':
        coinSet.add(x['asset_id_base'])
        n = {}
        n['label'] = x['asset_id_base']
        n['value'] = x['symbol_id']
        symbolDictList.append(n)


# Grabbing latest month data

def grabLatestData(symbol):
    return api.ohlcv_latest_data(symbol_id=symbol, query_parameters={'period_id': '1MTH'})