import ccxt
import time

# Enter your exchange API credentials here
BINANCE_API_KEY = 'your_binance_api_key'
BINANCE_API_SECRET = 'your_binance_api_secret'

KUCOIN_API_KEY = 'your_kucoin_api_key'
KUCOIN_API_SECRET = 'your_kucoin_api_secret'

# Enter your arbitrage parameters here
SYMBOL = 'BTC/USDT'
BINANCE_MARKET = 'binance'
KUCOIN_MARKET = 'kucoin'

# Connect to the exchanges
exchange1 = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_API_SECRET,
})

exchange2 = ccxt.kucoin({
    'apiKey': KUCOIN_API_KEY,
    'secret': KUCOIN_API_SECRET,
})

# Arbitrage function


def perform_arbitrage():
    ticker1 = exchange1.fetch_ticker(SYMBOL)
    ticker2 = exchange2.fetch_ticker(SYMBOL)

    # Calculate potential profit
    bid_price1 = ticker1['bid']
    ask_price2 = ticker2['ask']
    profit = (ask_price2 - bid_price1) / bid_price1

    # Perform arbitrage if profitable
    if profit > 0:
        amount = 0.01  # Set your desired amount to trade
        buy_order = exchange1.create_limit_buy_order(
            SYMBOL, amount, bid_price1)
        sell_order = exchange2.create_limit_sell_order(
            SYMBOL, amount, ask_price2)
        print(
            f"Arbitrage opportunity found! Bought {amount} at {bid_price1} on {BINANCE_MARKET} and sold at {ask_price2} on {KUCOIN_MARKET}. Profit: {profit * 100:.2f}%")


# Arbitrage loop
while True:
    try:
        perform_arbitrage()
    except ccxt.BaseError as e:
        print(f"An error occurred: {str(e)}")

    time.sleep(10)  # Sleep for 10 seconds between arbitrage attempts
