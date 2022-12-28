# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
# import coinbase_helper
import api_helper as help
import layout_helper as lay

app = Dash(__name__, title='Mock Crypto Wallet', external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[

    html.H1(
        children='Mock Crypto Wallet',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='A mock crypto wallet you can run from your own computer.', style={
        'textAlign': 'center',
        'color': colors['text']
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
            clearable=False
        ),
    ]),
    
    html.H2('Wallet', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    
    # Wallet Buttons
    html.Div(
        children=[
            dbc.Button(id='buy', children=['Buy'], color="Primary"),
            dbc.Button(id='sell', children=['Sell'], color="Primary")
            ],
        style = {
            'display': 'inline-block'
        }),
    
    # Gui to add coins
    
    lay.buy_form_div,
    
    # Wallet coins
    html.Div(
        id='coins',
        children=[]
    )

])

# This is to manage changes in inputs from the dropdown, and changes the chart.
@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
def display_time_series(ticker):
    fig = help.chartCoin(ticker)
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text']
    )
    return fig

@app.callback(
    Output("buy_div", "hidden"),
    Input("buy", "n_clicks"))
def display_buy_form(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    if n_clicks % 2 == 0:
        return True
    return False

@app.callback(
    Output("coins", "children"),
    [Input("buy_submit", "n_clicks"),
     Input("coins_buy", "value"),
     Input("price_buy", "value")]
)
def buy_coin(button, coin, price):
    if button is None:
        raise PreventUpdate
    if button % 2 == 0:
        return True
    return False

if __name__ == '__main__':
    app.run_server(debug=True)
