# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
# import coinbase_helper
import ccxt_helper as help

app = Dash(__name__, title='Mock Crypto Wallet')

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# Building DF and Figure for Historical Data Chart
histDF = px.data.stocks()
histFig = px.line(histDF, x='date', y='GOOG')
histFig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

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
    
    # html.Div()


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

if __name__ == '__main__':
    app.run_server(debug=True)
