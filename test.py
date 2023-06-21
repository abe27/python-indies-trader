import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
from bandl.binance import Binance

# สร้าง DataFrame ที่มีข้อมูลราคา
obj = Binance()
dfs = obj.get_data("ETHBTC")  # returns last 90 days data
print(dfs)

df = pd.DataFrame(dfs)
df['Date'] = pd.to_datetime(df['CloseTime'])
df['Date'] = df['Date'].apply(mpl_dates.date2num)
df = df[['', 'Date', 'Open', 'High', 'Low', 'Close']]

print(df)
# พล็อตกราฟแท่งเทียน
plt.figure(figsize=(10, 6))
candlestick_ohlc(plt.gca(), df.values, width=0.6,
                 colorup='green', colordown='red')
plt.title('Candlestick Chart')
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mpl_dates.DateFormatter('%Y-%m-%d'))
plt.show()
