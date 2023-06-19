import time
import requests

# Enter your Bitkub API credentials here
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# Enter your rebalancing parameters here
SYMBOLS = ['BTC', 'ETH']  # Symbols to rebalance
TARGET_WEIGHTS = [0.5, 0.5]  # Target weights for each symbol
# Threshold for rebalancing in decimal (e.g., 0.02 = 2%)
ALLOCATION_THRESHOLD = 0.02

# Bitkub API endpoint
API_ENDPOINT = 'https://api.bitkub.com'

# Rebalance function


def rebalance():
    # Get current balances
    endpoint = '/api/market/balances'
    headers = {'Accept': 'application/json', 'X-BTK-APIKEY': API_KEY}
    response = requests.get(API_ENDPOINT + endpoint, headers=headers)
    data = response.json()

    if 'error' in data:
        print(f"Error: {data['error']['message']}")
        return

    balances = {balance['symbol']: float(
        balance['available']) for balance in data}

    # Calculate total value
    total_value = sum(balances[symbol] for symbol in SYMBOLS)

    # Calculate target amounts
    target_amounts = {symbol: total_value * weight for symbol,
                      weight in zip(SYMBOLS, TARGET_WEIGHTS)}

    # Rebalance if allocation exceeds threshold
    for symbol in SYMBOLS:
        if balances[symbol] / target_amounts[symbol] > 1 + ALLOCATION_THRESHOLD:
            amount = balances[symbol] - target_amounts[symbol]
            place_order('SELL', symbol, amount)
            print(f"Market sell order placed for {symbol}: {amount}")
        elif balances[symbol] / target_amounts[symbol] < 1 - ALLOCATION_THRESHOLD:
            amount = target_amounts[symbol] - balances[symbol]
            place_order('BUY', symbol, amount)
            print(f"Market buy order placed for {symbol}: {amount}")

# Place order function


def place_order(side, symbol, amount):
    endpoint = '/api/market/place'
    headers = {'Accept': 'application/json', 'X-BTK-APIKEY': API_KEY}
    params = {
        'sym': symbol,
        'amt': amount,
        'rat': 0,
        'typ': 'market',
        'side': side
    }
    response = requests.post(API_ENDPOINT + endpoint,
                             headers=headers, params=params)
    data = response.json()

    if 'error' in data:
        print(f"Error: {data['error']['message']}")


# Rebalancing loop
while True:
    try:
        rebalance()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {str(e)}")

    time.sleep(60)  # Sleep for 1 minute between rebalances
