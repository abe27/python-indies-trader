import pandas as pd
import numpy as np

def calculate_rsi(data, window=14):
    """
    คำนวณค่า RSI (Relative Strength Index) จากข้อมูลราคา
    """
    close_delta = data.diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ema_up = up.ewm(com=window - 1, min_periods=window).mean()
    ema_down = down.ewm(com=window - 1, min_periods=window).mean()
    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi

def find_rsi_divergence(data):
    """
    ค้นหา RSI divergence โดยเปรียบเทียบค่า RSI และราคา
    """
    rsi = calculate_rsi(data['Close'])
    price = data['Close']
    divergence = np.zeros_like(price)
    for i in range(2, len(price)):
        if (rsi[i] > rsi[i-1] and rsi[i] > rsi[i-2] and price[i] < price[i-1] and price[i-1] < price[i-2]):
            divergence[i] = 1  # Positive divergence
        elif (rsi[i] < rsi[i-1] and rsi[i] < rsi[i-2] and price[i] > price[i-1] and price[i-1] > price[i-2]):
            divergence[i] = -1  # Negative divergence
    return divergence

# ตัวอย่างการใช้งาน
# สร้าง DataFrame ด้วยข้อมูลราคา
price_data = {
    'Close': [10, 12, 15, 13, 16, 14, 18, 20, 17, 16]
}
df = pd.DataFrame(price_data)

# ค้นหา RSI divergence
divergence = find_rsi_divergence(df)

# แสดงผลลัพธ์
df['RSI Divergence'] = divergence
print(df)