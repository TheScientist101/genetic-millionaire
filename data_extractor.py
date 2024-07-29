import pandas as pd
import numpy as np
from stock_indicators import indicators, Quote


def calculate_derivative_oscillator(quotes_list, index, NaNCount):
    double_smoothed_rsi = indicators.get_ema(
        [
            Quote(date=r.date, close=r.rsi)
            for r in indicators.get_rsi(quotes_list)
        ],
        5)

    double_smoothed_rsi = [Quote(date=r.date, close=r.ema)
                           for r in indicators.get_ema([
                               Quote(date=r.date, close=r.ema)
                               for r in double_smoothed_rsi
                           ], 3)]

    signal_line = pd.Series(
        [np.nan] * NaNCount + [
            s.sma for s in indicators.get_sma(double_smoothed_rsi, 9)
        ],
        index=index
    )

    double_smoothed_rsi = pd.Series(
        [np.nan] * NaNCount + [
            float(r.close) for r in double_smoothed_rsi
        ],
        index=index
    )

    do = double_smoothed_rsi.sub(signal_line)
    do.name = "DOSC"

    return do


def calculate_rsi(quotes_list, index, NaNCount):
    rsi = pd.Series(
        [np.nan] * NaNCount + [i.rsi for i in indicators.get_rsi(quotes_list)],
        index=index)
    rsi.name = "RSI"
    return rsi


def calculate_macd(quotes_list, index, NaNCount):
    macd = pd.Series(
        [np.nan] * NaNCount + [
            i.macd for i in indicators.get_macd(quotes_list)
        ],
        index=index)
    macd.name = "MACD"
    return macd


def extractIndicators(quotes):
    results = []
    for ticker in {q[0] for q in quotes.keys()}:
        NaNCount = len(quotes) - quotes[ticker]['Close'].count()
        specificQuotes = quotes[ticker][NaNCount:]
        quotes_list = [
            Quote(d, o, h, l, c, v)
            for d, o, h, l, c, v
            in zip(quotes.index[NaNCount:], specificQuotes['Open'],
                   specificQuotes['High'],
                   specificQuotes['Low'],
                   specificQuotes['Close'],
                   specificQuotes['Volume'])
        ]

        data = [
            calculate_derivative_oscillator(
                quotes_list, quotes.index, NaNCount),
            calculate_rsi(
                quotes_list, quotes.index, NaNCount),
            calculate_macd(
                quotes_list, quotes.index, NaNCount),
            quotes[ticker]['Close']
        ]
        ticker_results = pd.DataFrame(data).transpose()
        ticker_results.name = ticker
        results.append(ticker_results)

    return results
