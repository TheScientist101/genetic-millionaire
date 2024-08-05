from model_base import ModelBase
import numpy as np
import time


class GeneticModel(ModelBase):
    name = "genetic model"

    def __init__(self, startingCash, parameters):
        self.weights = parameters[:4]
        self.offsets = parameters[4:8]
        self.threshold = abs(parameters[8])
        self.cash = startingCash
        self.history = []
        self.assets = {}

    def calculateFavorability(self, prices):
        adjusted = prices.sub(self.offsets)
        result = sum(np.multiply(self.weights, adjusted))
        if np.isnan(result):
            return 0
        return result

    def calculateActions(self, day):
        favorabilities = {}
        for ticker, prices in day.iterrows():
            if ticker not in self.assets:
                self.assets[ticker] = 0
            favorabilities[ticker] = self.calculateFavorability(prices)

        for ticker, favorability in sorted(favorabilities.items(), key=lambda x: x[1], reverse=True):
            price = day.loc[ticker]["Close"]
            if np.isnan(price):
                continue

            if favorability < 0:
                sell_amount = min(-favorability, self.assets[ticker])
                if sell_amount < 0:
                    raise Exception(f"Trying to sell {sell_amount} shares of {ticker}")
                self.assets[ticker] -= sell_amount
                self.cash += price * sell_amount
            elif favorability > self.threshold and self.cash > 0:
                purchase_amount = min(
                    favorability, self.cash / price)
                if purchase_amount < 0:
                    raise Exception(f"Trying to buy {purchase_amount} shares of {ticker}")
                self.assets[ticker] += purchase_amount
                self.cash -= price * purchase_amount

        value = 0
        for ticker in self.assets:
            if np.isnan(day.loc[ticker]["Close"]):
                continue
            value += self.assets[ticker] * day.loc[ticker]["Close"]

        value += self.cash

        return value

    def accountHistory(self):
        return self.history
