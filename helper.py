# HELPER FUNCTINONS
from dash import dcc
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objects as go
import api_helper as help

def purchase(coin, price, data):
    new = None
    if data == {} or 'df' not in data.keys() or len(data['df']) == 0:
            new = pd.DataFrame(columns=["Coin", "Current Value ($)", "Market Value ($)"])
            data['bank'] = 1000
    else: 
        new = pd.DataFrame(data['df'])
    if coin in new['Coin'].unique():
        new.loc[(new['Coin'] == coin), ('Current Value ($)')] = round(
            (new.loc[(new['Coin'] == coin), ('Current Value ($)')]) + price, 2)
        data['df'] = new.to_dict(orient='records')
        data['bank'] = data['bank'] - price
    else:
        ticker = help.grabTicker(coin)
        layout = go.Layout(
            autosize=False,
            width=100,
            height=50)
        ind_fig = go.Figure(layout=layout)
        ind_fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = ticker['close'],
            number = { "font": { "size": 20 }},
            delta = {'reference': ticker['open'], 'relative': True}))
        new = pd.concat([pd.DataFrame({
            "Coin": [coin],
            "Current Value ($)": [price],
            "Market Value ($)": [dcc.Graph(figure=ind_fig, style={'width': '90px', 'height': '90px'}).to_plotly_json()]
        }), new])
        data['df'] = new.to_dict(orient='records')
        data['bank'] = round((data['bank'] - price), 2)
        data[coin+'_start'] = ticker['close']
    return data
    
def sell(coin, price, data):
    if data == {} or 'df' not in data.keys():
        raise PreventUpdate
    df = pd.DataFrame(data['df'])
    if coin in df['Coin'].unique():
        df.loc[(df['Coin'] == coin), ('Current Value ($)')] = round(
            (df.loc[(df['Coin'] == coin), ('Current Value ($)')]) - price, 2)
        if df.loc[(df['Coin'] == coin), ('Current Value ($)')].values[0] == 0:
            df = df[df['Coin'] != coin]
        data['df'] = df.to_dict(orient='records')
        data['bank'] = data['bank'] + price
        
    else:
        raise PreventUpdate
    return data