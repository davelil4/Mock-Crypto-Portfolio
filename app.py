# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
# import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import api_helper as help
import layout_helper as lay

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = dbc.Container(children=[
    dcc.Store(id='coin_mem', storage_type='local'),
    dcc.Store(id='submit_mem', storage_type='memory'),

    html.H1(
        children='Mock Crypto Wallet',
        className="bg-primary text-white p-2 mb-2 text-center"
    ),

    html.Div(children='A mock crypto wallet you can run from your own computer.', style={
        'textAlign': 'center'
    }),


    # Dropdown to change which coin data is showing from BINANCE
    html.Div(children=[
        html.H4('Crypto price analysis'),
        dcc.Graph(id="time-series-chart"),
        html.P("Select coin:"),
        dcc.Dropdown(
            id="ticker",
            options=help.optionList,
            value='BTC/USD',
            clearable=False,
            className="mb-4"
        ),
    ]),
    
    lay.row1,
    lay.row2,
    lay.buy_form_div,
    # lay.sell_form_div,
    dbc.Row(id="pd_row", children=[])
    
    ],
    className="dbc"
    )

# This is to manage changes in inputs from the dropdown, and changes the chart.
@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
def display_time_series(ticker):
    fig = help.chartCoin(ticker)
    return fig

# Shows buy drop-down menu
@app.callback(
    Output("buy_div", "hidden"),
    Input("buy_b", "n_clicks"))
def display_buy_form(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    if n_clicks % 2 == 0:
        return True
    return False

# Sets submit button to buy
@app.callback(
    Output("submit_mem", "data"),
    Input("buy_b", "n_clicks"),
    Input("sell_b", "n_clicks"),
    State("buy_b", "active"),
    State("sell_b", "active"))
def submit_change(buy, sell, bActive, sActive):
    if buy > 0 or sell > 0:
        if bActive:
            return {'submit': 'buy'}
        elif sActive:
            return {'submit': 'sell'}
    return {}

# Resets buy button clicks

# # Shows sell dropdown menu
# @app.callback(
#     Output("sell_div", "hidden"),
#     Input("sell_b", "n_clicks"))
# def display_sell_form(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     if n_clicks % 2 == 0:
#         return True
#     return False

# UPDATES COINS IN WALLET

# Updates coin chart after buying/selling/resetting coins
@app.callback(
    Output("pd_row", "children"),
    Input("coin_mem", "modified_timestamp"),
    State("coin_mem", "data")
)
def pd_data(ts, data):
    if ts is None:
        raise PreventUpdate
    
    df = None
    if data is None or 'df' not in data.keys():
        data = {'df': pd.DataFrame(columns=["Coin", "Current Price", "% start"])}
    else:
        df = pd.DataFrame(pd.DataFrame(data['df']))
        df.reset_index()
        for index, row in df.iterrows():
            ticker = help.grabTicker(row['Coin'])
            layout = go.Layout(
                autosize=False,
                width=100,
                height=50)
            ind_fig = go.Figure(layout=layout)
            ind_fig.add_trace(go.Indicator(
                mode = "number+delta",
                value = ticker['close'],
                number = { "font": { "size":20 }},
                delta = {'reference': ticker['open'], 'relative': True}))
            if data[row['Coin']+'_start'] != ticker['close']:
                open = data[row['Coin']+'_start']
                change = (open - ticker['close']) / open
                if change != 0:
                    df.loc[(df['Coin'] == row['Coin']), ('Current Price')] = round((row['Current Price'] * (1 - change)), 2)
                df.loc[(df['Coin'] == row['Coin']), ('% start')] = [dcc.Graph(figure=ind_fig, style={'width': '90px', 'height': '90px'}).to_plotly_json()]
    if df is not None:
        return [dbc.Table.from_dataframe(df, dark=False)]
    return [dbc.Table.from_dataframe(pd.DataFrame(data['df']), dark=False)]

# Updates coin table data
@app.callback(
    Output("coin_mem", "data"),
    [State("reset", "n_clicks"),
    Input("buy_submit", "n_clicks"),
    State("coins_buy", "value"),
    State("price_buy", "value"),
    State("coin_mem", "data"),
    Input("bank", "n_submit"),
    State("bank", "value"),
    Input("sell_submit", "n_clicks"),
    State("submit_mem", "data")
    ]

)
def update_coins_pd(reset, button, coin, price, data, bank, bValue, submit_data):
    
    # if price is not None:
    #     if bank is None or bank < price:
    #         raise PreventUpdate
    
    data = data or {}

    if reset>0:
        data = None
        return data

    if bank is not None and bank > 0:
        data['bank'] = bValue
    
    if button != None and button != 0 and price != None and submit_data['submit'] == 'buy':
        if data == {} or 'df' not in data.keys():
            new = pd.DataFrame(columns=["Coin", "Current Price", "% start"])
            data['bank'] = 1000
        else: new = pd.DataFrame(data['df'])
        ticker = help.grabTicker(coin)
        layout = go.Layout(
            autosize=False,
            width=100,
            height=50)
        ind_fig = go.Figure(layout=layout)
        ind_fig.add_trace(go.Indicator(
            mode = "number+delta",
            value = ticker['close'],
            number = { "font": { "size":20 }},
            delta = {'reference': ticker['open'], 'relative': True}))
        new = pd.concat([pd.DataFrame({
            "Coin": [coin],
            "Current Price": [price],
            "% start": [dcc.Graph(figure=ind_fig, style={'width': '90px', 'height': '90px'}).to_plotly_json()]
        }), new])
        data['df'] = new.to_dict(orient='records')
        data['bank'] = round((data['bank'] - price), 2)
        data[coin+'_start'] = ticker['close']
        return data
    # elif button != None and button != 0 and price != None and submit_data['submit'] == 'sell': 

    return data

# Adjusts buy clicks to and allows reset to work without adding more coins
@app.callback(
    Output("buy_submit", "n_clicks"),
    [Input('reset', 'n_clicks'),
    State("buy_submit", "n_clicks"),
    Input("coin_mem", "modified_timestamp")]
)
def reset_buy(reset, buy, ts):
    if reset is None or reset == 0:
        raise PreventUpdate
    return 0

# Adjusts reset clicks
@app.callback(
    Output("reset", "n_clicks"),
    [Input("coin_mem", "modified_timestamp")]
)
def reset_buy(reset):
    if reset is None:
        raise PreventUpdate
    return 0

# Updates Bank Balance
@app.callback(
    Output("bank", "value"),
    [Input("coin_mem", "modified_timestamp"),
    State("coin_mem", "data")]
)
def bank_data(ts, data):
    if ts is None:
        raise PreventUpdate
    data = data or {'bank': 1000}
    return data['bank']

# Updates 



if __name__ == '__main__':
    app.run_server(debug=True)
