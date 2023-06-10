# import datetime library to specify the datetime range for historical data
from datetime import datetime
import MetaTrader5 as mt5  # to access historical data
import pandas as pd  # for data analysis and calculation of technical indicators
import plotly.express as px  # for data visualization
# to display results in Jupyter Notebook
from IPython.display import display, Markdown, Latex


# connecting to MetaTrader5 platform to request historical data
is_connected = mt5.initialize()

# mt5.login(login, password, server)


symbol = "EURUSD"
timeframe = mt5.TIMEFRAME_D1  # mt5 structure which represents the daily timeframe
# start of datetime of the data that we want to request
start_datetime = datetime(2021, 1, 1)
end_datetime = datetime.now()  # end of datetime of the data that we want to reque

# use mt5.copy_rates_range to get OHLC data
ohlc = mt5.copy_rates_range(symbol, timeframe, start_datetime, end_datetime)

display(Markdown('### OHLC Results inside Array'))  # Markdown description
display(ohlc[0:10])  # display first 10 results

# Markdown description
display(Markdown('### Convert results to a Pandas DataFrame'))
df = pd.DataFrame(ohlc)  # converting ohlc array to Pandas DataFrame
display(df)

# Markdown description
display(Markdown('### Keep [time, open, high, low, close] columns only'))
# specifying columns that we want to keep
df = df[['time', 'open', 'high', 'low', 'close']]
display(df)

# Markdown description
display(Markdown('### Convert time column from Timestamp to Datetime'))
# use pandas.to_datetime, unit='s' will convert it based on seconds
df['time'] = pd.to_datetime(df['time'], unit='s')
display(df)
