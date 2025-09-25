import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.compat import HAS_PYARROW
import yfinance as yf

#ticker1 is main ticker, change tickers and start/end date to your liking
tickers = ['IONQ', 'SRPT']
ticker1 = tickers[0]
ticker2 = tickers[1]
start_date = '2010-09-24'
end_date = '2025-09-25' 

data = yf.download(tickers, start=start_date, end=end_date)

if data is None or data.empty:
    print("No data downloaded. Check tickers or date range.")
else:
    close_prices = data['Close']
    print(close_prices.tail())

daily_returns = data.pct_change()
if daily_returns is None or daily_returns.empty:
    print("No data available")
else:
    print("Data Available")

cumulative_returns = (1+daily_returns).cumprod()
summary_stats = daily_returns['Close'].describe()
avg_daily_return = daily_returns['Close'].mean()
volatility = daily_returns.std()

print("--- Daily Returns (first 5 rows) ---")
print(daily_returns['Close'].head())
print("--- Daily Returns (last 5 rows) ---")
print(daily_returns['Close'].tail(10))
print("\n--- Cumulative Returns (last 5 rows) ---")
print(cumulative_returns['Close'].tail())
print("\n--- Average Daily Return ---")
print(avg_daily_return)
print("\n--- Volatility (Standard Deviation) ---")
print(volatility)
print("\n--- Summary Statistics ---")
print(summary_stats)

data['{0}_SMA50'.format(ticker1)] = data['Close'][ticker1].rolling(window=50).mean()
data['{0}_SMA200'.format(ticker1)] = data['Close'][ticker1].rolling(window=200).mean()

# Line graph of closing prices
plt.plot(data['Close'][ticker1])
plt.plot(data['Close'][ticker2])
plt.ylabel('Price')
plt.legend([ticker1, ticker2])
plt.savefig('Line_Graph_Closing_Prices.png', dpi=300)

#Graph of QURE's price and Moving Averages
plt.figure(figsize=(12, 6))
data['Close'][ticker1].plot(label='{0} Close Price'.format(ticker1), color='skyblue')
data[f'{ticker1}_SMA50'].plot(label='50-Day SMA', color='orange')
data[f'{ticker1}_SMA200'].plot(label='200-Day SMA', color='red')
plt.title(f'{ticker1} Closing Price and Moving Averages')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True)
plt.savefig("Closing_Moving_Averages.png", dpi=300)
#Histogram of QURE's daily returns
plt.figure(figsize=(10,6))
daily_returns['Close'][ticker1].dropna().hist(bins=1000, color='purple', alpha=0.7)
plt.title(f'Distribution of {ticker1} Daily Returns')
plt.xlabel('Daily Return')
plt.ylabel('Frequency')
plt.grid(True)
plt.savefig("Daily_Returns.png", dpi=300)

#Scatter plot of daily returns
plt.figure(figsize=(8, 8))
plt.scatter(daily_returns['Close'][ticker1], daily_returns['Close'][ticker2], alpha=0.5)
plt.title(f'Daily Returns: {ticker1} vs. {ticker2}')
plt.xlabel(f'{ticker1} Daily Returns')
plt.ylabel(f'{ticker2} Daily Returns')
plt.grid(True)
plt.savefig("Scatter_Plot_Closing_Daily_Returns.png", dpi=300)
