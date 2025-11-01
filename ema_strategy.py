import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import quantstats as qs

# Infosys data
ticker = "INFY.NS"
end_date = datetime.now()
start_date = end_date - timedelta(days=5*365)

data = yf.download(ticker, start=start_date, end=end_date, progress=False)

if isinstance(data.columns, pd.MultiIndex):
    data.columns = data.columns.get_level_values(0)

df = data[['Close']].copy()
df['Close'] = df['Close'].astype(float)
df = df.dropna()

if len(df) < 50:
    print("Error: Not enough data points.")
    exit()

print(f"Data loaded: {len(df)} rows")

# EMA Crossover Strat
fast_period = 5
slow_period = 15

df['EMA_fast'] = df['Close'].ewm(span=fast_period, adjust=False).mean()
df['EMA_slow'] = df['Close'].ewm(span=slow_period, adjust=False).mean()

# Generate signals
df['signal'] = 0
df.loc[df['EMA_fast'] > df['EMA_slow'], 'signal'] = 1
df.loc[df['EMA_fast'] <= df['EMA_slow'], 'signal'] = -1

df['position'] = df['signal'].diff()

# Calculate returns with position sizing
df['daily_return'] = df['Close'].pct_change()
df['strategy_return'] = df['signal'].shift(1) * df['daily_return'] * 1.2

df = df.dropna()

# Clean returns
strategy_return_clean = df['strategy_return'].replace([np.inf, -np.inf], 0).fillna(0)

# Performance Metrics
total_return = (df['Close'].iloc[-1] / df['Close'].iloc[0] - 1) * 100
strategy_total_return = (np.prod(1 + strategy_return_clean) - 1) * 100

# CAGR calculation
years = len(df) / 252
buy_hold_cagr = ((df['Close'].iloc[-1] / df['Close'].iloc[0]) ** (1 / years) - 1) * 100
strategy_cagr = ((np.prod(1 + strategy_return_clean) ** (1 / years)) - 1) * 100
strategy_annual_return = strategy_cagr

volatility = strategy_return_clean.std() * np.sqrt(252) * 100
sharpe_ratio = (strategy_annual_return / volatility) if volatility > 0 else 0

# Drawdown calculation
cumulative_return = (1 + strategy_return_clean).cumprod()
running_max = cumulative_return.expanding().max()
drawdown = (cumulative_return - running_max) / running_max
max_drawdown = drawdown.min() * 100

# Win rate
wins = (strategy_return_clean > 0).sum()
total_trades = (strategy_return_clean != 0).sum()
win_rate = (wins / total_trades * 100) if total_trades > 0 else 0

# Printing results
print("=" * 50)
print("EMA CROSSOVER STRATEGY - INFOSYS")
print("=" * 50)
print(f"Fast EMA: {fast_period}, Slow EMA: {slow_period}")
print(f"Period: {df.index[0].date()} to {df.index[-1].date()}")
print("RETURNS:")
print(f"  Buy & Hold Return: {total_return:.2f}%")
print(f"  Strategy Return: {strategy_total_return:.2f}%")
print(f"  Outperformance: {strategy_total_return - total_return:.2f}%")
print("ANNUALIZED METRICS:")
print(f"  Buy & Hold CAGR: {buy_hold_cagr:.2f}%")
print(f"  Strategy CAGR: {strategy_cagr:.2f}%")
print(f"  Volatility: {volatility:.2f}%")
print(f"  Sharpe Ratio: {sharpe_ratio:.2f}")
print("RISK METRICS:")
print(f"  Max Drawdown: {max_drawdown:.2f}%")
print(f"  Win Rate: {win_rate:.2f}%")
print("=" * 50)

# Generating Quantstats
qs_returns = pd.Series(strategy_return_clean, index=pd.to_datetime(df.index))
qs.reports.html(
    qs_returns,
    benchmark="^NSEI",  # Nifty 50 Index
    title="Infosys EMA Crossover Strategy (2020–2025)",
    output="infosys_ema_report.html"
)
print("QuantStats report generated: infosys_ema_report.html")
print("DISCLAIMER:")
print("This analysis is for educational and research purposes only.")
print("It does not constitute financial advice or a recommendation to trade.")
