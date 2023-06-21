from stolgo.breakout import Breakout
from stolgo.candlestick import CandleStick
from bandl.binance import Binance
testObj = Binance()  # returns 'Yfinance class object'.
dfs = testObj.get_data("ETHBTC")  # returns last 90 days data
print(dfs)

candle_test = CandleStick()
is_be = candle_test.is_bullish_engulfing(dfs)
print(is_be)

candle_test = CandleStick()
is_it = candle_test.is_inverse_hammer_candle(dfs)
print(is_it)

breakout_test = Breakout()
# periods:Number of candles,percentage: range of consolidation in percentage
is_be = breakout_test.is_breaking_out(dfs, periods=None, percentage=None)
print(is_be)
