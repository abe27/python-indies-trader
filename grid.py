import ccxt
import time

# Enter your exchange API credentials here
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# Enter your trading parameters here
SYMBOL = 'BTC/USDT'
GRID_SPACING = 100  # Grid spacing in USDT
AMOUNT = 0.01  # Amount to trade in BTC

# Connect to the exchange
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

# Calculate grid levels
ticker = exchange.fetch_ticker(SYMBOL)
last_price = ticker['close']
grid_levels = [price for price in range(int(last_price) - 500, int(last_price) + 500, GRID_SPACING)]

# Place initial grid orders
for level in grid_levels:
    price = level / 100.0
    sell_order = exchange.create_limit_sell_order(SYMBOL, AMOUNT, price)
    buy_order = exchange.create_limit_buy_order(SYMBOL, AMOUNT, price)

print('Initial grid orders placed. Monitoring for fills...')

# Monitor for filled orders and place new ones accordingly
while True:
    open_orders = exchange.fetch_open_orders(SYMBOL)

    for order in open_orders:
        if order['side'] == 'sell':
            if float(order['price']) >= last_price:
                print(f"Grid sell order filled at {order['price']}")
                new_price = float(order['price']) + (GRID_SPACING / 100.0)
                new_order = exchange.create_limit_sell_order(SYMBOL, AMOUNT, new_price)
                grid_levels.append(new_price)
        elif order['side'] == 'buy':
            if float(order['price']) <= last_price:
                print(f"Grid buy order filled at {order['price']}")
                new_price = float(order['price']) - (GRID_SPACING / 100.0)
                new_order = exchange.create_limit_buy_order(SYMBOL, AMOUNT, new_price)
                grid_levels.append(new_price)

    time.sleep(10)  # Sleep for 10 seconds between checks
