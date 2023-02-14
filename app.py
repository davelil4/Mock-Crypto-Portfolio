# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import api_helper as help
import layout_helper as lay
import helper as h

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css], title="Mock Cryptocurreny Portfolio")
server=app.server

app.layout = dbc.Container(children=[
    dcc.Store(id='coin_mem', storage_type='local'),

    html.H1(
        children='Mock Crypto Trading Platform',
        className="bg-primary text-white p-2 mb-2 text-center"
    ),

    dbc.Card(
        dbc.CardBody(
            [
                lay.exchange_row,
                # Dropdown to change which coin data is showing from BINANCE
                lay.chart_row,
                lay.row2,
                lay.trade_collapse
            ]
        ),
        className="mb-2"
    ),
    
    dbc.Card(dbc.CardBody([
        lay.port_row,
        dbc.Row(id="pd_row", children=[], className="g-0")]))
    ],
    className="dbc"
    )

# This is to manage changes in inputs from the dropdown, and changes the chart.
@app.callback(
    Output("time-series-chart", "figure"), 
    [Input("ticker", "value"),
    Input("refresh", "n_clicks")])
def display_time_series(ticker, refresh):
    fig = help.chartCoin(ticker)
    return fig

# Shows buy drop-down menu
@app.callback(
    Output("trade_collapse", "is_open"),
    [Input("buy_b", "n_clicks_timestamp"),
    Input("sell_b", "n_clicks_timestamp"),
    State("trade_collapse", "is_open"),
    State("buy_submit", "children")])
def display_buy_form(n_clicks, sell_n_clicks, hidden, text):
    if n_clicks is None:
        n_clicks = 0
    if sell_n_clicks is None:
        sell_n_clicks = 0
    
    if n_clicks == 0 and sell_n_clicks == 0:
        return False

    if n_clicks > sell_n_clicks and text == 'Buy':
        return not hidden
    elif sell_n_clicks > n_clicks and text == 'Buy':
        return True
    elif n_clicks > sell_n_clicks and text == 'Sell':
        return True
    elif sell_n_clicks > n_clicks and text == 'Sell':
        return not hidden
    return hidden

# Updates portfolio balance
@app.callback(
    Output("bal", "children"),
    [Input("pd_row", "children"),
    Input("coin_mem", "data")
    ]
)
def update_portfolio_bal(n, data):
    data = data or None
    if data is not None and 'df' in data.keys() and len(data['df']) != 0:
        df = pd.DataFrame(data['df'])
        return "Portfolio Balance: $" + str(round(df['Current Value ($)'].sum(), 2))
    return "Portfolio Balance: $0.00"



# Updates app coin table after buying/selling/resetting coins
@app.callback(
    Output("pd_row", "children"),
    Input("coin_mem", "modified_timestamp"),
    State("coin_mem", "data")
)
def pd_data(ts, data):
    if ts is None:
        raise PreventUpdate
    
    data = data or {'df': pd.DataFrame(columns=["Coin", "Current Value ($)", "Market Value ($)"])}
    if 'df' not in data.keys() or len(data['df']) == 0:
        data['df'] = pd.DataFrame(columns=["Coin", "Current Value ($)", "Market Value ($)"])
    return [dbc.Table.from_dataframe(pd.DataFrame(data['df']), dark=False)]

# Updates coin table data
@app.callback(
    Output("coin_mem", "data"),
    [State("coins_buy", "value"),
    State("price_buy", "value"),
    State("coin_mem", "data"),
    Input("bank", "n_submit"),
    State("bank", "value"),
    Input("buy_submit", "n_clicks_timestamp"),
    State("buy_b", "n_clicks_timestamp"),
    State("sell_b", "n_clicks_timestamp"),
    Input("refresh", "n_clicks_timestamp"),
    Input("reset", "n_clicks_timestamp")]
)
def update_coins_pd(
                    coin, 
                    price, 
                    data, 
                    bank, 
                    bValue, 
                    sub_time,
                    buy_time,
                    sell_time,
                    refresh_time,
                    reset_time):
    
    data = data or {}

    if bank is not None and bank > 0:
        data['bank'] = bValue
    
    if reset_time is None or buy_time is None or sell_time is None or refresh_time is None:
        if reset_time is None:
            reset_time = 0
        if buy_time is None:
            buy_time = 0
        if sell_time is None:
            sell_time = 0
        if refresh_time is None: 
            refresh_time = 0
        if sub_time is None:
            sub_time = 0
    
    if reset_time != 0 or sub_time != 0 or buy_time != 0 or sell_time != 0:
        if reset_time == max(reset_time, sub_time, refresh_time):
            data = None
            return data
        elif sub_time == max(reset_time, sub_time, refresh_time):
            if buy_time == max(buy_time, sell_time):
                data = h.purchase(coin, price, data)
            elif sell_time == max(sell_time, buy_time):
                data = h.sell(coin, price, data)

    # Updates Coins if Market Value ($) changes
    if not (data is None or 'df' not in data.keys()) and len(data['df']) != 0:
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
                c = row['Coin']+'_start'
                open = data[row['Coin']+'_start']
                change = (open - ticker['close']) / open
                if change != 0:
                    df.loc[(df['Coin'] == row['Coin']), ('Current Value ($)')] = round((row['Current Value ($)'] * (1 - change)), 2)
                df.loc[(df['Coin'] == row['Coin']), ('Market Value ($)')] = [dcc.Graph(figure=ind_fig, style={'width': '90px', 'height': '90px'}).to_plotly_json()]
                data[row['Coin']+'_start'] = ticker['close']
        data['df'] = df.to_dict(orient='records')
    return data

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

# Changes buy button
@app.callback(
    Output("buy_submit", "children"),
    [Input("buy_b", "n_clicks_timestamp"),
    Input("sell_b", "n_clicks_timestamp")]
)
def submit_change(buy, sell):
    if buy is None:
        buy = 0
    if sell is None:
        sell = 0
    
    if max(buy, sell) == buy:
        return "Buy"
    else:
        return "Sell"

# Clears form input after pressing submit
@app.callback(
    Output("price_buy", "value"),
    Input("buy_submit", "n_clicks")
)
def update_form_input(n):
    return None


if __name__ == '__main__':
#     # app.run_server(debug=True)
    app.run_server(debug=True, host='0.0.0.0', port=8050) 
#     app.run_server(port=8000)
