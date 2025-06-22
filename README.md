# 📊 Algorithmic Trading Strategy Development

**Duration:** Aug 2024 – Dec 2024  
**Technologies:** Python, Pandas, NumPy, Matplotlib  
**Strategies:** SMA, EMA, MA Bounce, MACD  
**Benchmark:** SPY Buy-and-Hold (3-Year Period)

---

## 🚀 Project Overview

This project explores the design, implementation, and evaluation of four rule-based algorithmic trading strategies using historical SPY price data. Each strategy was tested on a 3-year period and compared against a passive SPY buy-and-hold portfolio.

---

## 📈 Strategies Implemented

- **SMA Crossover:** Buy signal when short SMA crosses above long SMA.
- **EMA Crossover:** Similar to SMA, but uses exponential moving averages for faster response.
- **MA Bounce:** Buys when price bounces above the SMA after being below.
- **MACD Strategy:** Uses MACD and signal line crossovers to determine entry/exit.

---

## ⚙️ Performance Metrics

Each strategy was evaluated using the following metrics:
- **Total Return (% change)**
- **Sharpe Ratio** (Risk-adjusted return)
- **Alpha** (Excess return above market)
- **Beta** (Volatility relative to SPY)

Performance was benchmarked against:
- 🟡 **SPY Buy & Hold Strategy**

---

## 📌 Sample Output

### Strategy Portfolio Value vs SPY Buy & Hold

<img width="1391" alt="strategy_backtest" src="https://github.com/user-attachments/assets/2c6e0a9f-5dcf-4444-ac4b-c2882e1cc253" />

### Sharpe Ratio, Alpha, and Beta output for each strategy in comparison to SPY.

<img width="704" alt="metrics" src="https://github.com/user-attachments/assets/8417e682-f9dd-4ab3-bad2-af56ff1272c8" />
