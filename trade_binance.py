# import Libraries
from binance.spot import Spot as Client
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

# keep these secret on your real accounts!
api_key = 'oYiRMlgbrkTxEbnsHlrZ976v18emLfjcy81mX1GnU0wJVudCIK3PeElxLsxpEeVc'
secret_key = 'pVMZVVTcSCQZsRnYxsjeVWEMWBCHYFioTnnFrLjHYs0TE1mHP1CaCUP8nQW9seCw'

# url to access binance api
base_url = "https://api.binance.com"

# use for testing
base_url_test = "https://testnet.binance.vision"

# create Client to access API
client = Client(api_key, secret_key, base_url=base_url_test)
client.account()

# market order
params = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "MARKET",
    "quantity": 0.002,
}

response = client.new_order(**params)

# limit order
params = {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 0.002,
    "price": 30000,
}

response = client.new_order(**params)


# get open orders
response = client.get_open_orders()

client.my_trades("BTCUSDT")
