import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_derivative_oscillator(quotes_list, index, rsi_period=14, short_smooth=5, long_smooth=3, period_ma=9):
    rsi_series = calculate_rsi(quotes_list, index, period=rsi_period)

    smoothed_rsi = rsi_series.ewm(span=short_smooth, adjust=False).mean()

    double_smoothed_rsi = smoothed_rsi.ewm(span=long_smooth, adjust=False).mean()

    signal_line = double_smoothed_rsi.rolling(window=period_ma, min_periods=1).mean()

    derivative_oscillator = double_smoothed_rsi - signal_line

    return pd.Series(derivative_oscillator, name='DOSC', index=index)


def calculate_rsi(quotes_list, index, period=14):
    delta = quotes_list.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    return pd.Series(rsi, name='RSI', index=index)


def calculate_macd(quotes_list, index, short_window=12, long_window=26):
    short_ema = quotes_list.ewm(span=short_window, adjust=False).mean()

    long_ema = quotes_list.ewm(span=long_window, adjust=False).mean()

    macd_line = short_ema - long_ema

    macd_df = pd.Series(macd_line, name='MACD', index=index)

    return macd_df

def extract_indicators(quotes):
    results = []
    tickers = {q[0] for q in quotes.keys()}
    for idx, ticker in enumerate(tickers):
        print(f"Processing {ticker} {idx + 1} / {len(tickers)}...")

        data = [
            calculate_derivative_oscillator(
                quotes[ticker]['Adj Close'], quotes.index),
            calculate_rsi(
                quotes[ticker]['Adj Close'], quotes.index),
            calculate_macd(
                quotes[ticker]['Adj Close'], quotes.index),
            quotes[ticker]['Adj Close']
        ]

        ticker_results = pd.DataFrame(data).transpose()
        ticker_results.name = ticker
        results.append(ticker_results)

    print("Done processing...")
    return pd.concat(results, keys=tickers).swaplevel(0, 1)
