import requests
import time

# ป้อนข้อมูลประจำตัว API ของ Bitkub ที่นี่
API_KEY = 'your_api_key'
API_SECRET = 'your_api_secret'

# ป้อนพารามิเตอร์ rebalancing ที่นี่
SYMBOLS = ['BTC', 'ETH']  # สัญลักษณ์ที่ต้องการ rebalance
TARGET_WEIGHTS = [0.5, 0.5]  # น้ำหนักเป้าหมายสำหรับแต่ละสัญลักษณ์
# ค่า threshold สำหรับการ rebalance ในรูปแบบทศนิยม (เช่น 0.02 = 2%)
ALLOCATION_THRESHOLD = 0.02

# Bitkub API endpoint
API_ENDPOINT = 'https://api.bitkub.com'

# ฟังก์ชันสำหรับการ rebalance


def rebalance():
    # รับยอดคงเหลือปัจจุบัน
    endpoint = '/api/market/balances'
    headers = {'Accept': 'application/json', 'X-BTK-APIKEY': API_KEY}
    response = requests.get(API_ENDPOINT + endpoint, headers=headers)
    data = response.json()

    if 'error' in data:
        print(f"เกิดข้อผิดพลาด: {data['error']['message']}")
        return

    balances = {balance['symbol']: float(
        balance['available']) for balance in data}

    # คำนวณมูลค่ารวม
    total_value = sum(balances[symbol] for symbol in SYMBOLS)

    # คำนวณจำนวนเป้าหมาย
    target_amounts = {symbol: total_value * weight for symbol,
                      weight in zip(SYMBOLS, TARGET_WEIGHTS)}

    # ดำเนินการ rebalance หากการจัดสรรเกินขีดจำกัด
    for symbol in SYMBOLS:
        if balances[symbol] / target_amounts[symbol] > 1 + ALLOCATION_THRESHOLD:
            amount = balances[symbol] - target_amounts[symbol]
            place_order('SELL', symbol, amount)
            print(f"สั่งขายที่ตลาดสำหรับ {symbol}: {amount}")
        elif balances[symbol] / target_amounts[symbol] < 1 - ALLOCATION_THRESHOLD:
            amount = target_amounts[symbol] - balances[symbol]
            place_order('BUY', symbol, amount)
            print(f"สั่งซื้อที่ตลาดสำหรับ {symbol}: {amount}")

# ฟังก์ชันสำหรับการส่งคำสั่ง


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
        print(f"เกิดข้อผิดพลาด: {data['error']['message']}")


# ลูป rebalancing
while True:
    try:
        rebalance()
    except requests.exceptions.RequestException as e:
        print(f"เกิดข้อผิดพลาด: {str(e)}")

    time.sleep(60)  # หน่วงเวลา 1 นาทีระหว่างการ rebalancing
