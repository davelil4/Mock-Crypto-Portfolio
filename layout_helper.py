from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import api_helper as help



# Wallet title
wallet_head = html.H2('Wallet', className="text-center mb-4"),

# Wallet Buttons
buy_button = dbc.Col(dbc.Button(id='buy_b', children=['Buy'], color="primary", n_clicks=0))
sell_button = dbc.Col(dbc.Button(id='sell_b', children=['Sell'], color="primary", n_clicks=0))
reset_btn = dbc.Col(dbc.Button(id='reset', children=['Reset'], color="primary", n_clicks=0))
USD_bal = dbc.Col(html.P("10,000.00"))
wallet_bal = dbc.Col(html.P("0"))



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
    className="mb-4",
)
price_buy = dbc.InputGroup(
            [
                dbc.InputGroupText("$"),
                dbc.Input(id="price_buy", placeholder="Amount", type="number"),
                dbc.InputGroupText(".00"),
            ],
            className="mb-3",
        )
buy_submit = dbc.Button(id="buy_submit", children="Submit", color="secondary")
buy_form = dbc.Form(id="buy_form", children=[buy_coin_dropdown, price_buy, buy_submit])
buy_form_div = html.Div(id="buy_div", children=[buy_form], hidden=True)

# Coin table
coin_table_head = [html.Thead(html.Tr([html.Th("Coin"), html.Th("Current Price ($)"), html.Th("% start")]))]
coin_table_rows = [html.Tbody(id="coin_rows", children=[])]
coin_table = dbc.Table(coin_table_head + coin_table_rows, bordered=True, dark=False)

# Layout
row1 = dbc.Row(dbc.Col(wallet_head))
row2 = dbc.Row([dbc.Col(buy_button, width=1), dbc.Col(sell_button, width=1), dbc.Col(reset_btn, width=1)], className="mb-4")
row3 = dbc.Row(dbc.Col(buy_form_div), className="mb-4")
row4 = dbc.Row(dbc.Col(coin_table))