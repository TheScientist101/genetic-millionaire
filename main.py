from simulator import Simulator
from buy_everything import BuyEverything

test = Simulator(["AAPL", "GOOGL"], "2015-06-12", "2024-07-17")

test.simulate([BuyEverything], 100_000)
