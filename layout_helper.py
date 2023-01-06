from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import api_helper as help



# Wallet title
wallet_head = html.H2('Wallet', className="text-center mb-4"),

# Wallet Buttons
buy_button = dbc.Button(id='buy_b', children=['Buy'], color="primary", n_clicks=0)
sell_button = dbc.Button(id='sell_b', children=['Sell'], color="primary", n_clicks=0)
reset_btn = dbc.Button(id='reset', children=['Reset'], color="primary", n_clicks=0)
USD_bal = dbc.InputGroup(
            [
                dbc.InputGroupText("$"),
                dbc.Input(placeholder="Initial Balance", type="number"),
            ]
        )
wallet_bal = dbc.Col(html.P("0"))



# Building buy form
# buy_coin_dropdown = html.Div(
    # [
        # dbc.Label("Coin", html_for="dropdown", width="auto"),
buy_coin_dropdown = dcc.Dropdown(
            id="coins_buy",
            options=help.optionList,
            value='BTC/USD',
            clearable=True,
            style={'width': "100px"}
        ),
    # ],
    
# )
price_buy = dbc.InputGroup(
            [
                dbc.InputGroupText("$"),
                dbc.Input(id="price_buy", placeholder="Amount", type="number"),
                dbc.InputGroupText(".00"),
            ]
        )
buy_submit = dbc.Button(id="buy_submit", children="Submit", color="secondary")


# Coin table
coin_table_head = [html.Thead(html.Tr([html.Th("Coin"), html.Th("Current Price ($)"), html.Th("% start")]))]
coin_table_rows = [html.Tbody(id="coin_rows", children=[])]
coin_table = dbc.Table(coin_table_head + coin_table_rows, bordered=True, dark=False)

pandasTable = dbc.Table()

# Layout
row1 = dbc.Row(dbc.Col(wallet_head))
row2 = dbc.Row(
    [
        dbc.Col(buy_button, width=1), 
        dbc.Col(sell_button, width=1), 
        dbc.Col(reset_btn, width=1),
        dbc.Col(USD_bal, width=2)
    ],
    className="mb-4")
row3 = dbc.Row(
            [
                dbc.Col(children=buy_coin_dropdown, width="auto", className="me-3"), 
                dbc.Col(children=price_buy, width="auto", className="me-3"),
                dbc.Col(children=buy_submit, width="auto")
            ], 
            className="g-2"
        )
buy_form_div = html.Div(id="buy_div", children=[row3], hidden=True, className="mb-4", style={'width': "auto"})
row5 = dbc.Row(dbc.Col(coin_table))