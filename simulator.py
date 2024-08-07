import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from data_extractor import extract_indicators
from genetic_model import GeneticModel
import os
import pickle
from concurrent.futures import ProcessPoolExecutor, as_completed


class Simulator:
    def __init__(self, tickers):
        self.tickers = tickers
        self.data = None
        self.indicators = None
    
    # Simulate all actions in a day
    @staticmethod
    def execute_actions(sell, purchase, cash, assets, day, logging, date):
        # Sell first because selling can increase cash allowance
        for ticker in sell:
            if sell[ticker] < 0:
                raise Exception(f"Cannot sell negative amount of {ticker}, tried to sell: {sell[ticker]}")
            if sell[ticker] > assets[ticker]:
                raise Exception(f"Cannot sell more than {assets[ticker]} of {ticker}, tried to sell: {sell[ticker]}")
            assets[ticker] -= sell[ticker]
            cash += day.loc[ticker]["Adj Close"] * sell[ticker]
            if sell[ticker] > 0 and logging:
                print(f"{date}: Sold {sell[ticker]} of {ticker} at {day.loc[ticker]['Adj Close']}")
        
        # Execute purchases
        for ticker in purchase:
            if purchase[ticker] < 0:
                raise Exception(f"Cannot purchase negative amount of {ticker}, tried to purchase: {purchase[ticker]}")
            if day.loc[ticker]['Adj Close'] * purchase[ticker] > cash:
                raise Exception(f"Cannot purchase more than {cash / day.loc[ticker]['Adj Close']} of {ticker}, tried to purchase: {purchase[ticker]}")
            assets[ticker] += purchase[ticker]
            cash -= day.loc[ticker]["Adj Close"] * purchase[ticker]
            if purchase[ticker] > 0 and logging:
                print(f"{date}: Bought {purchase[ticker]} of {ticker} at {day.loc[ticker]['Adj Close']}")
        
        # Return newly adjusted cash amount and assets dict
        return cash, assets
    
    # Calculate total value by summing value of assets + cash
    @staticmethod
    def calculate_value(cash, assets, day):
        value = 0
        for ticker in assets:
            if np.isnan(day.loc[ticker]["Adj Close"]):
                continue
            value += assets[ticker] * day.loc[ticker]["Adj Close"]

        value += cash

        return value
    
    # Download data from Yahoo finance and replace index with pd.datetime index
    def load_data(self):
        self.data = yf.download(self.tickers,
                                    group_by='ticker')
        self.data.index = pd.to_datetime(self.data.index)

    # Extract indicators from data
    def prepare_data(self):
        self.indicators = extract_indicators(self.data)

    # Save plots as png and pkl (in case want to view interactively)
    def save_plots(self, value, cash_history, generation, model_num):
        matplotlib.use('agg')
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

    # Simulate each model in provided models
    def simulate_model(self, parameters, starting_cash, extra_data, generation, index):
        # Create instance with parameters
        instance = GeneticModel(parameters)

        # History of values created with calculate_value
        value = []

        # Assets held at any given time
        assets = {}

        # Asset History if extra logging is enabled
        if extra_data:
            asset_history = {}

        # Initialize cash and empty history
        cash = starting_cash
        cash_history = []

        print(f"Model {index + 1}: {parameters}")
        for date in self.indicators.index.levels[0]:
            day = self.indicators.loc[date]
            
            # Receive actions from model
            sell, purchase = instance.calculate_actions(day, cash, assets)

            # Execute actions
            cash, assets = Simulator.execute_actions(sell, purchase, cash, assets, day, extra_data, date)
            cash_history.append(cash)

            # Log assets to history if enabled
            if extra_data:
                for ticker in assets:
                    if ticker not in asset_history:
                        asset_history[ticker] = []
                    asset_history[ticker].append(assets[ticker] * day.loc[ticker]["Adj Close"])
            
            # Append to value history
            value.append(Simulator.calculate_value(cash, assets, day))
        
        # Convert value and cash_history to pd.Series for date index
        value = pd.Series(value, index=self.data.index)
        cash_history = pd.Series(cash_history, index=self.data.index)

        # Asset History plotting if enabled
        if extra_data:
            for ticker in asset_history:
                asset_history[ticker] = pd.Series(asset_history[ticker], index=self.data.index)
                plt.plot(asset_history[ticker], label=ticker)
            plt.plot(cash_history, label="Cash")
            plt.legend(loc='best')
            plt.show()
        
        # Save plots for later reference
        self.save_plots(value, cash_history, generation, index + 1)
        print(f"Model {index + 1}: {value.iloc[-1]}")
        return instance, value

    # Simulate set of models
    def simulate(self, starting_cash, parameter_set, generation='none', extra_data=False, use_processes=True):
        if self.data is None:
            self.load_data()
        
        if self.indicators is None:
            self.prepare_data()

        value = {}
        # Parallel can make simulation faster
        if use_processes:
            # Use ProcessPoolExecutor to run simulations in parallel across multiple cores
            with ProcessPoolExecutor() as executor:
                # Start each simulation in a separate process
                futures = [
                    executor.submit(self.simulate_model, parameters, starting_cash, extra_data, generation, i)
                    for i, parameters in enumerate(parameter_set)
                ]

                # Collect results as they complete
                for future in as_completed(futures):
                    instance, model_value = future.result()
                    value[instance] = model_value
        # Allows cleaner logging
        else:
            # Run simulations sequentially
            for i, parameters in enumerate(parameter_set):
                instance, model_value = self.simulate_model(parameters, starting_cash, extra_data, generation, i)
                value[instance] = model_value

        # Find best two models based on value
        best = [model for model, _ in sorted(
            value.items(), key=lambda x: x[1].iloc[-1], reverse=True)]

        # Return best two values
        return best[0], best[1], value[best[0]]
