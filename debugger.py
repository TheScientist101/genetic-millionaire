from simulator import Simulator
import random
import numpy as np
import matplotlib.pyplot as plt
from main import get_parameters

generation_size = 10
initial_amount = 100_000
generations = 10
tickers = []

with open("tickers.txt", "r") as f:
    tickers = f.readlines()

for i, ticker in enumerate(tickers):
    tickers[i] = ticker.strip()

config = [-70, 40, -60, -83, -36, -47, 13, 80, -26, 1]

simulator = Simulator(tickers)
first, second, history = simulator.simulate(initial_amount, [config, config], extra_data=True)