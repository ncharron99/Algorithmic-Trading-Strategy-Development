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
