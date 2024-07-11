import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

class Simulator:
    # Dates in YYYY-MM-DD
    def __init__(self, tickers, beginDate, endDate):
        self.tickers = tickers
        self.beginDate = beginDate
        self.endDate = endDate
    def simulate(self, models, startingCash, interval = '1d'):
        data = yf.download(self.tickers, start=self.beginDate, end=self.endDate, auto_adjust=True)
        values = {}
        for model in models:
            instance = model(startingCash)
            for idx, day in data.iterrows():
                instance.calculateActions(day)
            values[model.name] = instance.accountHistory()
        histories = list(values.items())
        for idx, history in enumerate(histories):
            print(idx)
            plt.plot(history[1], label=history[0])
        plt.legend(loc='best')
        plt.show()

        
