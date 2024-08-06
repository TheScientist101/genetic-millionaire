from model_base import ModelBase
import math
import numpy as np


class GeneticModel(ModelBase):
    name = "genetic model"

    def __init__(self, parameters):
        self.weights = parameters[:4]
        self.offsets = parameters[4:8]
        self.threshold = abs(parameters[8])
        self.sensitivity = abs(parameters[9])
    
    def normalize(self, favorability):
        return math.atan(favorability / self.sensitivity) / (math.pi / 2)

    def calculate_favorability(self, prices):
        adjusted = prices.sub(self.offsets)
        result = sum(np.multiply(self.weights, adjusted))
        if np.isnan(result):
            return 0
        return self.normalize(result)

    def calculate_actions(self, day, curr_cash, curr_assets):
        favorabilities = {}
        for ticker, prices in day.iterrows():
            if ticker not in curr_assets:
                curr_assets[ticker] = 0
            favorabilities[ticker] = self.calculate_favorability(prices)

        sell = {}
        purchase = {}

        for ticker, favorability in sorted(favorabilities.items(), key=lambda x: x[1], reverse=True):
            price = day.loc[ticker]["Adj Close"]
            if np.isnan(price):
                continue

            if favorability < 0 and curr_assets[ticker] > 0:
                sell_amount = -favorability * curr_assets[ticker]
                curr_cash += sell_amount * price
                sell[ticker] = sell_amount
            elif curr_cash > 0 and favorability > 0:
                purchase_amount = (curr_cash * favorability) / price
                purchase_amount = math.floor(purchase_amount * 1000) / 1000
                if purchase_amount > self.threshold:
                    curr_cash -= purchase_amount * price
                    purchase[ticker] = purchase_amount

        return sell, purchase
