import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from data_extractor import extract_indicators
from genetic_model import GeneticModel
import os
import pickle

class Simulator:
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None
        self.indicators = None
    
    @staticmethod
    def execute_actions(sell, purchase, cash, assets, day, logging, date):
        for ticker in sell:
            if sell[ticker] < 0:
                raise Exception(f"Cannot sell negative amount of {ticker}, tried to sell: {sell[ticker]}")
            if sell[ticker] > assets[ticker]:
                raise Exception(f"Cannot sell more than {assets[ticker]} of {ticker}, tried to sell: {sell[ticker]}")
            assets[ticker] -= sell[ticker]
            cash += day.loc[ticker]["Adj Close"] * sell[ticker]
            if sell[ticker] > 0 and logging:
                print(f"{date}: Sold {sell[ticker]} of {ticker} at {day.loc[ticker]['Adj Close']}")
        for ticker in purchase:
            if purchase[ticker] < 0:
                raise Exception(f"Cannot purchase negative amount of {ticker}, tried to purchase: {purchase[ticker]}")
            if day.loc[ticker]['Adj Close'] * purchase[ticker] > cash:
                raise Exception(f"Cannot purchase more than {cash / day.loc[ticker]['Adj Close']} of {ticker}, tried to purchase: {purchase[ticker]}")
            assets[ticker] += purchase[ticker]
            cash -= day.loc[ticker]["Adj Close"] * purchase[ticker]
            if purchase[ticker] > 0 and logging:
                print(f"{date}: Bought {purchase[ticker]} of {ticker} at {day.loc[ticker]['Adj Close']}")
        return cash, assets
    
    @staticmethod
    def calculate_value(cash, assets, day):
        value = 0
        for ticker in assets:
            if np.isnan(day.loc[ticker]["Adj Close"]):
                continue
            value += assets[ticker] * day.loc[ticker]["Adj Close"]

        value += cash

        return value
    
    def load_data(self):
        self.data = yf.download(self.tickers,
                                    group_by='ticker')
        self.data.index = pd.to_datetime(self.data.index)

    def prepare_data(self):
        self.indicators = extract_indicators(self.data)

    def save_plots(self, value, cash_history, generation, model_num):
        plt_fig = plt.figure()
        plt.plot(value - cash_history, label="Total Invested")
        plt.plot(cash_history, label="Cash")
        plt.plot(value, label="Total Value")
        plt.legend(loc='best')
        os.makedirs(f"outputs/generation_{generation}", exist_ok=True)
        # Save image
        plt.savefig(f"outputs/generation_{generation}/model_{model_num}.png")
        # Save pickle of figure
        with open(f"outputs/generation_{generation}/model_{model_num}.pkl", "wb") as f:
            pickle.dump(plt_fig, f)
        plt.close()

    def simulate(self, starting_cash, parameter_set, generation='none', extra_data=False):
        if self.data is None:
            self.load_data()
        
        if self.indicators is None:
            self.prepare_data()

        value = {}

        for i, parameters in enumerate(parameter_set):
            instance = GeneticModel(parameters)
            value[instance] = []
            assets = {}
            if extra_data:
                asset_history = {}
            cash = starting_cash
            cash_history = []
            print(f"Model {i + 1} / {len(parameter_set)}: {parameters}")
            for date in self.indicators.index.levels[0]:
                day = self.indicators.loc[date]
                sell, purchase = instance.calculate_actions(day, cash, assets)
                cash, assets = Simulator.execute_actions(sell, purchase, cash, assets, day, extra_data, date)
                cash_history.append(cash)
                if extra_data:
                    for ticker in assets:
                        if ticker not in asset_history:
                            asset_history[ticker] = []
                        asset_history[ticker].append(assets[ticker] * day.loc[ticker]["Adj Close"])
                value[instance].append(Simulator.calculate_value(cash, assets, day))
            value[instance] = pd.Series(value[instance], index=self.data.index)
            cash_history = pd.Series(cash_history, index=self.data.index)
            if extra_data:
                for ticker in asset_history:
                    asset_history[ticker] = pd.Series(asset_history[ticker], index=self.data.index)
                    plt.plot(asset_history[ticker], label=ticker)
                plt.plot(cash_history, label="Cash")
                plt.legend(loc='best')
                plt.show()
            self.save_plots(value[instance], cash_history, generation, i + 1)
            print(f"Model {i + 1} / {len(parameter_set)}: {value[instance].iloc[-1]}")

        best = [model for model, _ in sorted(
            value.items(), key=lambda x: x[1].iloc[-1], reverse=True)]

        return best[0], best[1], value[best[0]]
