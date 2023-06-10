# import Libraries
from binance.client import Client
import pandas as pd
import plotly.graph_objects as go
from IPython.display import display

# url to access binance api
base_url = "https://api.binance.com"

# use for testing
base_url_test = "https://testnet.binance.vision"

# create Client to access API
spot_client = Client(base_url=base_url)

# requesting exchange info
exchange_info = spot_client.exchange_info()
print(exchange_info)


# symbols as DataFrame
symbols = pd.DataFrame(exchange_info['symbols'])
symbols


# Access current Prices for your desired symbol
btcusd_price = spot_client.ticker_price("BTCUSDT")
btcusd_price

# Access historical prices
btcusd_history = spot_client.klines("BTCUSDT", "1h", limit=100)
display(btcusd_history[:2])

# show as DataFrame
columns = ['time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades',
           'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']
btcusd_history_df = pd.DataFrame(btcusd_history, columns=columns)
btcusd_history_df['time'] = pd.to_datetime(
    btcusd_history_df['time'], unit='ms')

display(btcusd_history_df)

# plot results
fig = go.Figure(data=[go.Candlestick(x=btcusd_history_df['time'],
                open=btcusd_history_df['open'],
                high=btcusd_history_df['high'],
                low=btcusd_history_df['low'],
                close=btcusd_history_df['close'])])

fig.show()
