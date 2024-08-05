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

        for i, parameters in enumerate(parameter_set):
            instance = GeneticModel(startingCash, parameters)
            value[instance] = []
            print(f"Model {i + 1} / {len(parameter_set)}: {parameter_set}")
            for date in self.indicators.index.levels[0]:
                day = self.indicators.loc[date]
                value[instance].append(instance.calculateActions(day))
            value[instance] = pd.Series(value[instance], index=self.data.index)
            print(f"Model {i + 1} / {len(parameter_set)}: {value[instance].tail(1).item()}")

        # for model in value:
        #     value[model] = pd.DataFrame(value[model], index=self.data.index)
        #     plt.plot(value[model], label=model.name)

        # plt.legend(loc='best')
        # plt.show()

        best = [model for model, _ in sorted(
            value.items(), key=lambda x: x[1].ilocn[-1], reverse=True)]

        return best[0], best[1], value[best[0]]
