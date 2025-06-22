#compiling all of the strategy files here

## Strategies Implemented
- `sma_strategy.py`: Uses a crossover of two simple moving averages.
- `ema_strategy.py`: Similar approach but with exponential moving averages.
- `macd_strategy.py`: Uses MACD and signal line crossovers.
- `ma_bounce_strategy.py`: Trades on "bounce" behavior around a simple moving average.

### strategies/sma_strategy.py
import pandas as pd

def sma_backtest(data: pd.DataFrame, short_window=10, long_window=20, capital=0.0, transaction_cost=0.0, return_signals=False):
    df = data.copy()
    df['SMA_short'] = df['Close'].rolling(short_window).mean()
    df['SMA_long'] = df['Close'].rolling(long_window).mean()
    df['Signal'] = (df['SMA_short'] > df['SMA_long']).astype(int)
    df['Position'] = df['Signal'].diff()

    cash, holdings = capital, 0.0
    in_market = False
    portfolio = []

    for _, row in df.iterrows():
        if row['Position'] == 1 and not in_market:
            holdings = (cash * (1 - transaction_cost)) / row['Close']
            cash = 0
            in_market = True
        elif row['Position'] == -1 and in_market:
            cash = holdings * row['Close'] * (1 - transaction_cost)
            holdings = 0
            in_market = False
        portfolio.append(cash + holdings * row['Close'])

    df['Portfolio Value'] = portfolio

    if return_signals:
        return df[['Position', 'Portfolio Value']]
    else:
        return {'Portfolio Value': df['Portfolio Value']}

  ### strategies/macd_strategy.py
import pandas as pd

def macd_backtest(data: pd.DataFrame, fast=10, slow=20, signal=10, capital=0.0, transaction_cost=0.0):
    df = data.copy()
    df['EMA_fast'] = df['Close'].ewm(span=fast, adjust=False).mean()
    df['EMA_slow'] = df['Close'].ewm(span=slow, adjust=False).mean()
    df['MACD'] = df['EMA_fast'] - df['EMA_slow']
    df['Signal_line'] = df['MACD'].ewm(span=signal, adjust=False).mean()
    df['Position'] = (df['MACD'] > df['Signal_line']).astype(int).diff()

    cash, holdings = capital, 0.0
    in_market = False
    portfolio = []

    for _, row in df.iterrows():
        if row['Position'] == 1 and not in_market:
            holdings = (cash * (1 - transaction_cost)) / row['Close']
            cash = 0
            in_market = True
        elif row['Position'] == -1 and in_market:
            cash = holdings * row['Close'] * (1 - transaction_cost)
            holdings = 0
            in_market = False
        portfolio.append(cash + holdings * row['Close'])

    df['Portfolio Value'] = portfolio
    return df[['Portfolio Value']]

### strategies/ma_bounce_strategy.py
import pandas as pd

def ma_bounce_backtest(data: pd.DataFrame, window=20, capital=0.0, transaction_cost=0.0):
    df = data.copy()
    df['SMA'] = df['Close'].rolling(window).mean()
    df['Bounce'] = ((df['Close'].shift(1) < df['SMA'].shift(1)) & (df['Close'] > df['SMA'])).astype(int)
    df['Exit'] = (df['Close'] < df['SMA']).astype(int)
    df['Signal'] = df['Bounce'] - df['Exit']

    cash, holdings = capital, 0.0
    in_market = False
    portfolio = []

    for _, row in df.iterrows():
        if row['Signal'] == 1 and not in_market:
            holdings = (cash * (1 - transaction_cost)) / row['Close']
            cash = 0
            in_market = True
        elif row['Signal'] == -1 and in_market:
            cash = holdings * row['Close'] * (1 - transaction_cost)
            holdings = 0
            in_market = False
        portfolio.append(cash + holdings * row['Close'])

    df['Portfolio Value'] = portfolio
    return df[['Portfolio Value']]

### strategies/ema_strategy.py
import pandas as pd

def ema_backtest(data: pd.DataFrame, short_span=10, long_span=20, capital=0.0, transaction_cost=0.0):
    df = data.copy()
    df['EMA_short'] = df['Close'].ewm(span=short_span, adjust=False).mean()
    df['EMA_long'] = df['Close'].ewm(span=long_span, adjust=False).mean()
    df['Position'] = (df['EMA_short'] > df['EMA_long']).astype(int).diff()

    cash, holdings = capital, 0.0
    in_market = False
    portfolio = []

    for _, row in df.iterrows():
        if row['Position'] == 1 and not in_market:
            holdings = (cash * (1 - transaction_cost)) / row['Close']
            cash = 0
            in_market = True
        elif row['Position'] == -1 and in_market:
            cash = holdings * row['Close'] * (1 - transaction_cost)
            holdings = 0
            in_market = False
        portfolio.append(cash + holdings * row['Close'])

    df['Portfolio Value'] = portfolio
    return df[['Portfolio Value']]
