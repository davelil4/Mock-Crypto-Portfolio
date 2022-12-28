from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import api_helper as help

# Building buy form
buy_coin_dropdown = html.Div(
    [
        dbc.Label("Coin", html_for="dropdown"),
        dcc.Dropdown(
            id="coins_buy",
            options=help.optionList,
            value='BTC/USD',
            clearable=True
        ),
    ],
    className="mb-3",
)
price_buy = dbc.Input(id="price_buy", placeholder="Type here...", type="text")
buy_submit = dbc.Button(id="buy_submit", color="primary")
buy_form = dbc.Form(id="buy_form", children=[buy_coin_dropdown, price_buy, buy_submit])
buy_form_div = html.Div(id="buy_div", children=[buy_form], hidden=True)