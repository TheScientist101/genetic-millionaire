import pandas as pd
from stock_indicators import indicators, Quote


def calculate_derivative_oscillator(data, ticker, short_window=12,
                                    long_window=26, signal_window=9):
    # Calculate short-term and long-term moving averages
    data['Short_MA'] = data['Close'][ticker].rolling(
        window=short_window, min_periods=1).mean()
    data['Long_MA'] = data['Close'][ticker].rolling(
        window=long_window, min_periods=1).mean()

    # Calculate the difference (fast - slow)
    data['DOSC'] = data['Short_MA'] - data['Long_MA']

    # Calculate the signal line (moving average of the difference)
    data['Signal_Line'] = data['DOSC'].rolling(
        window=signal_window, min_periods=1).mean()

    # Return the Derivative Oscillator values (DOSC)
    return pd.DataFrame(data['DOSC'])


def calculate_rsi(quotes_list, index):
    rsi = pd.DataFrame(
        [i.rsi for i in indicators.get_rsi(quotes_list)], index=index)
    return rsi


def calculate_macd(quotes_list, index):
    macd = pd.DataFrame(
        [i.macd for i in indicators.get_macd(quotes_list)], index)
    return macd


def extractIndicators(quotes):
    ticker = 'AAPL'
    quotes_list = [
        Quote(d, o, h, l, c, v)
        for d, o, h, l, c, v
        in zip(quotes.index, quotes['Open'][ticker],
               quotes['High'][ticker],
               quotes['Low'][ticker],
               quotes['Close'][ticker],
               quotes['Volume'][ticker])
    ]

    results = calculate_derivative_oscillator(quotes, ticker)
    results.loc[:, "RSI"] = calculate_rsi(
        quotes_list, quotes.index)
    results.loc[:, "MACD"] = calculate_macd(quotes_list, quotes.index)
    return results
