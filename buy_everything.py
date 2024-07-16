from model_base import ModelBase


class BuyEverything(ModelBase):
    name = "buy everything"

    def __init__(self, startingCash):
        self.cash = startingCash
        self.history = []
        self.assets = {}

    def calculateActions(self, day):
        self.prices = day['Close'].to_dict()
        for key in self.prices:
            if key not in self.assets:
                self.assets[key] = 0
        newlyPurchasedAmount = self.cash / list(self.prices.values())[0]
        self.assets[list(self.prices.keys())[0]] += newlyPurchasedAmount
        self.cash -= newlyPurchasedAmount * list(self.prices.values())[0]
        self.history.append(self.calculateValue())

    def calculateValue(self):
        value = 0
        for ticker, amount in self.assets.items():
            value += amount * self.prices[ticker]

        return value + self.cash

    def accountHistory(self):
        return self.history
