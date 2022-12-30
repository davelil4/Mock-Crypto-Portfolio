# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
# import coinbase_helper
import api_helper as help
import layout_helper as lay

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

app.layout = dbc.Container(children=[

    html.H1(
        children='Mock Crypto Wallet',
        className="bg-primary text-white p-2 mb-2 text-center"
    ),

    html.Div(children='A mock crypto wallet you can run from your own computer.', style={
        'textAlign': 'center',
        # 'color': colors['text']
    }),


    # Dropdown to change which coin data is showing from BINANCE
    html.Div(children=[
        html.H4('Crypto price analysis', 
                # style={"color": colors['text']}
                ),
        dcc.Graph(id="time-series-chart"),
        html.P("Select coin:", 
            #    style={"color": colors['text']}
               ),
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
    lay.row3,
    lay.row4
    

    ],
    className="dbc"
    )

# This is to manage changes in inputs from the dropdown, and changes the chart.
@app.callback(
    Output("time-series-chart", "figure"), 
    Input("ticker", "value"))
def display_time_series(ticker):
    fig = help.chartCoin(ticker)
    # fig.update_layout(
    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
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
    Output("coin_rows", "children"),
    [Input("buy_submit", "n_clicks"),
     Input("coins_buy", "value"),
     Input("price_buy", "value"),
     State("coin_rows", "children")],
    # prevent_initial_call=True
)
def buy_coin(button, coin, price, child):
    new = child.copy()
    if button is None:
        raise PreventUpdate
    if button != 0 and len(new) != button:
        new.append(html.Tr(id=coin, children=[html.Td(coin), html.Td(price), html.Td("0")]))
        return new
    return new

if __name__ == '__main__':
    app.run_server(debug=True)
