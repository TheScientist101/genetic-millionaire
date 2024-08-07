from model_base import ModelBase
import math
import numpy as np


class GeneticModel(ModelBase):
    # Extract weights, offsets, threshold, and sensitivity from parameters
    def __init__(self, parameters, volumes):
        self.weights = parameters[:4]
        self.offsets = parameters[4:8]
        self.threshold = abs(parameters[8])
        self.sensitivity = abs(parameters[9])
        
        # Avoid division by 0 error
        if self.sensitivity == 0:
            self.sensitivity = 1
        
        self.volumes = volumes
    
    # Sigmoid function using arctan, returns value between -1 and 1
    def normalize(self, favorability):
        return math.atan(favorability / self.sensitivity) / (math.pi / 2)

    def calculate_favorability(self, prices):
        # Subtract offsets from indicators
        adjusted = prices.sub(self.offsets)

        # Sum the indicators multiplied by their weights
        result = sum(np.multiply(self.weights, adjusted))

        # Ignore values with unknown data
        if np.isnan(result):
            return 0

        # Normalize and return data
        return self.normalize(result)

    # Calculates actions for each day, called in simulator
    def calculate_actions(self, day, curr_cash, curr_assets):
        # Calculate favorabilities for each ticker
        favorabilities = {}
        for ticker, prices in day.iterrows():
            # Handled in simulator, but redundant here
            if ticker not in curr_assets:
                curr_assets[ticker] = 0
            
            favorabilities[ticker] = self.calculate_favorability(prices)

        # Empty actions dicts
        sell = {}
        purchase = {}

        # Execute in order of most favorable
        # TODO: Execute negative favorabilities first (for more cash allowance)
        for ticker, favorability in sorted(favorabilities.items(), key=lambda x: x[1], reverse=True):
            price = day.loc[ticker]["Adj Close"]

            # Ignore ticker if price is unknown
            if np.isnan(price):
                continue

            # Sell if negative favorability and is owned
            if favorability < 0 and curr_assets[ticker] > 0:
                # Sell favorability percent of owned asset of ticker
                # TODO: Potentially use threshold (or other threshold) to sell all if we have a little of a stock
                sell_amount = -favorability * curr_assets[ticker]
                curr_cash += sell_amount * price
                sell[ticker] = sell_amount
            # Sell if we have money and is favorable
            elif curr_cash > 0 and favorability > 0:
                # Purchase favorability percent of current cash of ticker
                # TODO: Find a more responsible usage of favorability purchasing
                purchase_amount = (curr_cash * favorability) / price
                purchase_amount = min(purchase_amount, self.volumes[ticker] - curr_assets[ticker])
                purchase_amount = round(purchase_amount - 0.5, 1)
                if purchase_amount > self.threshold:
                    curr_cash -= purchase_amount * price
                    purchase[ticker] = purchase_amount

        return sell, purchase
