import ccxt
import time

# Enter your exchange API credentials here
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# Enter your rebalancing parameters here
SYMBOLS = ['BTC/USDT', 'ETH/USDT']  # Symbols to rebalance
TARGET_WEIGHTS = [0.5, 0.5]  # Target weights for each symbol
# Threshold for rebalancing in decimal (e.g., 0.02 = 2%)
ALLOCATION_THRESHOLD = 0.02

# Connect to the exchange
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

# Calculate initial balances
initial_balances = {}
for symbol in SYMBOLS:
    balance = exchange.fetch_balance()[symbol.split('/')[0]]
    initial_balances[symbol] = balance['free']

# Rebalance function


def rebalance():
    current_balances = {}
    total_value = 0.0

    # Calculate current balances and total value
    for symbol in SYMBOLS:
        balance = exchange.fetch_balance()[symbol.split('/')[0]]
        current_balances[symbol] = balance['free']
        ticker = exchange.fetch_ticker(symbol)
        total_value += ticker['close'] * balance['free']

    # Calculate target amounts
    target_amounts = {}
    for symbol in SYMBOLS:
        target_amounts[symbol] = total_value * \
            TARGET_WEIGHTS[SYMBOLS.index(symbol)] / \
            exchange.fetch_ticker(symbol)['close']

    # Rebalance if allocation exceeds threshold
    for symbol in SYMBOLS:
        if current_balances[symbol] / target_amounts[symbol] > 1 + ALLOCATION_THRESHOLD:
            amount = current_balances[symbol] - target_amounts[symbol]
            exchange.create_market_sell_order(symbol, amount)
            print(f"Market sell order placed for {symbol}: {amount}")
        elif current_balances[symbol] / target_amounts[symbol] < 1 - ALLOCATION_THRESHOLD:
            amount = target_amounts[symbol] - current_balances[symbol]
            exchange.create_market_buy_order(symbol, amount)
            print(f"Market buy order placed for {symbol}: {amount}")


# Rebalancing loop
while True:
    rebalance()
    time.sleep(60)  # Sleep for 1 minute between rebalances
