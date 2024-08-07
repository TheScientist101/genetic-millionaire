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

config = [-78, 32, -66, -48, 45, -38, -22, -83, 61, 18]

simulator = Simulator(tickers)
best, history = simulator.simulate(initial_amount, [config], extra_data=True, use_processes=False)