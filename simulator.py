import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from data_extractor import extractIndicators
from genetic_model import GeneticModel


class Simulator:
    # Dates in YYYY-MM-DD
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None

    def simulate(self, startingCash, parameter_set, interval='1d'):
        if self.data is None:
            self.data = yf.download(self.tickers,
                                    auto_adjust=True,
                                    group_by='ticker')
            self.data.index = pd.to_datetime(self.data.index)

            self.indicators = extractIndicators(self.data)
        value = {}

        for parameters in parameter_set:
            instance = GeneticModel(startingCash, parameters)
            value[instance] = []
            for date in self.indicators.index.levels[0]:
                day = self.indicators.loc[date]
                value[instance].append(instance.calculateActions(day))

        # for model in value:
        #     value[model] = pd.DataFrame(value[model], index=self.data.index)
        #     plt.plot(value[model], label=model.name)

        # plt.legend(loc='best')
        # plt.show()

        best = [model for model, _ in sorted(
            value.items(), key=lambda x: x[1][-1], reverse=True)]

        return best[0], best[1], value[best[0]]
