import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from data_extractor import extractIndicators


class Simulator:
    # Dates in YYYY-MM-DD
    def __init__(self, tickers, beginDate, endDate):
        self.tickers = tickers
        self.beginDate = beginDate
        self.endDate = endDate

    def simulate(self, models, startingCash, interval='1d'):
        df = yf.download(self.tickers,
                         end=self.endDate,
                         auto_adjust=True,
                         group_by='ticker')
        df.index = pd.to_datetime(df.index)
        values = {}

        # for model in models:
        #     instance = model(startingCash)
        #     for idx, day in df.iterrows():
        #         instance.calculateActions(day)
        #     values[model.name] = instance.accountHistory()
        # histories = list(values.items())
        # for idx, history in enumerate(histories):
        #     print(idx)
        #     plt.plot(history[1], label=history[0])

        for i in extractIndicators(df):
            print(i)
            plt.plot(i)
        plt.legend(loc='best')
        plt.show()
