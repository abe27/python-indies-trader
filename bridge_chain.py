import requests

# Enter your Ethereum and BSC addresses here
ETH_ADDRESS = 'your_ethereum_address'
BSC_ADDRESS = 'your_bsc_address'

# Enter the token details and amount to bridge
TOKEN_SYMBOL = 'TOKEN'  # Replace with the token symbol
TOKEN_DECIMALS = 18  # Replace with the token decimals
AMOUNT = 10.0  # Replace with the amount to bridge

# Binance Bridge API endpoint
API_ENDPOINT = 'https://api.binance.org/bridge/api/v2'

# Generate the API URL
url = f"{API_ENDPOINT}/bridge"
headers = {'Content-Type': 'application/json'}

# Create the payload
payload = {
    'fromAddress': ETH_ADDRESS,
    'toAddress': BSC_ADDRESS,
    'amount': int(AMOUNT * (10 ** TOKEN_DECIMALS)),
    'asset': TOKEN_SYMBOL,
}

# Make the API request
response = requests.post(url, headers=headers, json=payload)

# Check the response
if response.status_code == 200:
    data = response.json()
    if 'result' in data and data['result']:
        print(
            f"Bridge request initiated successfully. Transaction ID: {data['result']['txId']}")
    else:
        print(f"Bridge request failed: {data.get('error', '')}")
else:
    print(f"Error: {response.status_code} - {response.text}")
