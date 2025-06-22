### main.py
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from strategies.sma_strategy import sma_backtest
from strategies.macd_strategy import macd_backtest
from strategies.ma_bounce_strategy import ma_bounce_backtest
from strategies.ema_strategy import ema_backtest

# === Configuration ===
csv_path = "data/SPY.csv"
INITIAL_CAPITAL = 15000
TX_COST = 0.00  #__% per trade

# === Load and clean data ===
df = pd.read_csv(csv_path, skiprows=3, header=None)
df.columns = ["Date", "Price", "Close", "High", "Low", "Open"]
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)
df = df.apply(pd.to_numeric, errors='coerce').dropna()

# === Run strategies ===
strategy_outputs = {
    "SMA": sma_backtest(df, capital=INITIAL_CAPITAL, transaction_cost=TX_COST),
    "MACD": macd_backtest(df, capital=INITIAL_CAPITAL, transaction_cost=TX_COST),
    "MA Bounce": ma_bounce_backtest(df, capital=INITIAL_CAPITAL, transaction_cost=TX_COST),
    "EMA": ema_backtest(df, capital=INITIAL_CAPITAL, transaction_cost=TX_COST),
}

# === Compute metrics ===
def compute_metrics(portfolio_series, initial_capital):
    returns = portfolio_series.pct_change().dropna()
    total_return = (portfolio_series.iloc[-1] / initial_capital - 1) * 100
    sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)
    return round(total_return, 2), round(sharpe_ratio, 2)

def compute_beta(strategy_returns, spy_returns):
    strategy_excess = strategy_returns - strategy_returns.mean()
    spy_excess = spy_returns - spy_returns.mean()
    covariance = np.cov(strategy_excess, spy_excess)[0, 1]
    variance = np.var(spy_excess)
    beta = covariance / variance
    return round(beta, 2)

def compute_alpha(strategy_returns, spy_returns):
    beta = compute_beta(strategy_returns, spy_returns)
    alpha_series = strategy_returns - (beta * spy_returns)
    alpha = alpha_series.mean() * 252  # annualized alpha
    return round(alpha * 100, 2), beta  # percentage annualized and beta

# === Compute SPY Buy & Hold ===
spy_portfolio = (df['Close'] / df['Close'].iloc[0]) * INITIAL_CAPITAL
spy_returns = spy_portfolio.pct_change().dropna()
spy_return, spy_sharpe = compute_metrics(spy_portfolio, INITIAL_CAPITAL)

# === Print strategy metrics ===
for name, df_out in strategy_outputs.items():
    portfolio_series = df_out['Portfolio Value']
    total_return, sharpe = compute_metrics(portfolio_series, INITIAL_CAPITAL)
    strategy_returns = portfolio_series.pct_change().dropna()
    alpha, beta = compute_alpha(strategy_returns, spy_returns)
    print(f"{name} | Final: ${portfolio_series.iloc[-1]:,.2f} | Return: {total_return:.2f}% | Sharpe: {sharpe:.2f} | Alpha: {alpha:.2f}% | Beta: {beta:.2f}")

print(f"SPY Buy & Hold | Final: ${spy_portfolio.iloc[-1]:,.2f} | Return: {spy_return:.2f}% | Sharpe: {spy_sharpe:.2f} | Alpha: 0.00% | Beta: 1.00")

# === Plot results ===
plt.figure(figsize=(14, 7))
for name, df_out in strategy_outputs.items():
    plt.plot(df_out['Portfolio Value'], label=name)

plt.plot(spy_portfolio, label='SPY Buy & Hold', linestyle='--', color='black')

# Optional: Plot entry/exit points for SMA (as an example)
sma_signals = sma_backtest(df, capital=INITIAL_CAPITAL, transaction_cost=TX_COST, return_signals=True)
if sma_signals is not None:
    entry_dates = sma_signals[sma_signals['Position'] == 1].index
    exit_dates = sma_signals[sma_signals['Position'] == -1].index
    plt.scatter(entry_dates, sma_signals.loc[entry_dates, 'Portfolio Value'], marker='^', color='green', label='SMA Entry', zorder=5)
    plt.scatter(exit_dates, sma_signals.loc[exit_dates, 'Portfolio Value'], marker='v', color='red', label='SMA Exit', zorder=5)

plt.title("Strategy Portfolio Value vs SPY Buy & Hold")
plt.xlabel("Date")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.show(block=True)
