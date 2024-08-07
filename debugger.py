# Like main.py except easy to run a single config (helps find bugs)
from simulator import Simulator
from main import get_parameters

generation_size = 10
initial_amount = 100_000
generations = 10
tickers = []

with open("tickers.txt", "r") as f:
    tickers = f.readlines()

for i, ticker in enumerate(tickers):
    tickers[i] = ticker.strip()

config = [-96, 31, 27, -49, -36, -21, 82, 77, 38, 47]

simulator = Simulator(tickers)
first, second, history = simulator.simulate(initial_amount, [config, config], extra_data=True, use_processes=False)