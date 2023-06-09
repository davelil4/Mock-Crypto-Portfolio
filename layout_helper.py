from dash import dcc, html
import dash_bootstrap_components as dbc
import api_helper as help

# Portfolio title
portfolio_head = html.H2('Portfolio', className="bg-secondary text-white text-center mb-2"),

# Exchange Buttons
buy_button = dbc.Button(id='buy_b', children=['Buy'], color="primary", n_clicks=0)
sell_button = dbc.Button(id='sell_b', children=['Sell'], color="primary", n_clicks=0)
reset_btn = dbc.Button(id='reset', children=['Reset'], color="dark")
refresh_btn = dbc.Button(id='refresh', children='Refresh', color='light')
USD_bal = dbc.InputGroup(
            [
                dbc.InputGroupText("$"),
                dbc.Input(id="bank", placeholder="Initial Balance", type="number", debounce=True),
            ]
        )
portfolio_bal = html.P(id="bal", children="Portfolio Balance: $0.00")



# Building buy form
buy_coin_dropdown = dcc.Dropdown(
            id="coins_buy",
            options=help.optionList,
            value='BTC/USD',
            clearable=True,
            style={'width': "100px"}
        )
price_buy = dbc.InputGroup(
        [
            dbc.InputGroupText("$"),
            dbc.Input(id="price_buy", placeholder="Amount", type="number"),
            dbc.InputGroupText(".00"),
            dbc.FormFeedback("Invalid value submitted.", type="invalid")
        ]
    )
buy_submit = dbc.Button(id="buy_submit", children="Submit", color="success")


# Layout Items

exchange_row = dbc.Row(dbc.Col(html.H2('Exchange', className="bg-secondary text-white text-center")))

chart_row = dbc.Row(
    dbc.Col(
        html.Div([
            dcc.Graph(id="time-series-chart"),
            dbc.Row(
                [
                    dbc.Col(html.P("Select coin:"), width=1, style={"padding": "5px 0"}),
                    dbc.Col(dcc.Dropdown(
                        id="ticker",
                        options=help.optionList,
                        value='BTC/USD',
                        clearable=False,
                        className="mb-4",
                        style={"width": "100px"}
            ), width=1)], className="g-0")
        ]),
    ),
    className="g-2"
)

port_row = dbc.Row(dbc.Col(portfolio_head))

row2 = dbc.Row(
    [
        dbc.Col(buy_button, width=1), 
        dbc.Col(sell_button, width=1),
        dbc.Col(reset_btn, width=1),
        dbc.Col(refresh_btn, width=1),
        dbc.Col(html.P("Bank Balance:"), width=1, style={"padding": "5px 0"}),
        dbc.Col(USD_bal, width=2),
        dbc.Col(portfolio_bal, width=0, style={"padding": "5px 0"})
    ],
    className="mb-2")
buy_row = dbc.Row(
            [
                dbc.Col(children=buy_coin_dropdown, width="auto", className="me-2"), 
                dbc.Col(children=price_buy, width="6", className="me-2"),
                dbc.Col(children=buy_submit, width="auto")
            ], 
            className="g-2"
        )

trade_collapse = dbc.Collapse(
    id="trade_collapse", 
    children=dbc.Card(dbc.CardBody(buy_row)), 
    className="mb-2", 
    style={"width": "25rem"},
    is_open=False)