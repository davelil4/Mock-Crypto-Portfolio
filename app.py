# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
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
    lay.buy_form_div,
    dcc.Store(id='coin_mem', storage_type='local'),
    lay.row5,
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
    # fig.update_layout(
    #     plot_bgcolor=colors['background'],
    #     paper_bgcolor=colors['background'],
    #     font_color=colors['text']
    # )
    return fig

@app.callback(
    Output("buy_div", "hidden"),
    Input("buy_b", "n_clicks"))
def display_buy_form(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    if n_clicks % 2 == 0:
        return True
    return False

# Callbacks for table involving storing local data

# # Updates coins from data held locally
# @app.callback(
#     Output("coin_rows", "children"),
#     Input("coin_mem", "modified_timestamp"),
#     State("coin_mem", "data")
# )
# def coin_data(ts, data):
#     if ts is None:
#         raise PreventUpdate
    
#     data = data or {}
#     return data.get('t_rows', None)

# # Updates coin table data
# @app.callback(
#     Output("coin_mem", "data"),
#     [State("reset", "n_clicks"),
#     Input("buy_submit", "n_clicks"),
#     State("coins_buy", "value"),
#     State("price_buy", "value"),
#     State('coin_mem', 'data')]

# )
# def update_coins(reset, button, coin, price, data):

#     data = data or {'t_rows': []}

#     if reset>0:
#         data = None
#         return data



#     if button != None and button != 0 and price != None:
#         new = data['t_rows'].copy()
#         new.append(html.Tr(id=coin, children=[html.Td(coin), html.Td(price), html.Td("0")]))
#         data['t_rows'] = new
#         return data

    
#     return data

# # Sets reset buy clicks to 0
# @app.callback(
#     Output("reset", "n_clicks"),
#     Input('coin_mem', 'modified_timestamp')
# )
# def reset(ts):
#     if ts is None:
#         raise PreventUpdate
#     return 0

# # Adjusts buy clicks to and allows reset to work without adding more coins
# @app.callback(
#     Output("buy_submit", "n_clicks"),
#     [Input('reset', 'n_clicks'),
#     State("buy_submit", "n_clicks"),
#     Input("coin_mem", "modified_timestamp")]
# )
# def reset_buy(reset, buy, ts):
#     if reset is None or reset == 0:
#         raise PreventUpdate
#     return 0


# PANDAS DIFFERENCE
@app.callback(
    Output("pd_row", "children"),
    Input("coin_mem", "modified_timestamp"),
    State("coin_mem", "data")
)
def pd_data(ts, data):
    if ts is None:
        raise PreventUpdate
    data = data or {}
    return dbc.Table.from_dataframe(pd.DataFrame(data['df']), dark=False) or []

# Updates coin table data
@app.callback(
    Output("coin_mem", "data"),
    [State("reset", "n_clicks"),
    Input("buy_submit", "n_clicks"),
    State("coins_buy", "value"),
    State("price_buy", "value"),
    State('coin_mem', 'data')]

)
def update_coins_pd(reset, button, coin, price, data):

    data = {'df': pd.DataFrame({
        "Coin": [],
        "Current Price": [],
        "% start": []
    }).to_dict("records")}

    if reset>0:
        data = None
        return data



    if button != None and button != 0 and price != None:
        new = pd.DataFrame(data['df'])
        new = pd.concat([pd.DataFrame({
            "Coin": [coin],
            "Current Price": [price],
            "% start": "0"
        }), new])
        data['df'] = new.to_dict("records")
        return data

    
    return data

if __name__ == '__main__':
    app.run_server(debug=True)
