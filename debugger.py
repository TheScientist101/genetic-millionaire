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

config = [-64, 64, -16, -24, 2, 75, 88, -22, 29, 18]

simulator = Simulator(tickers)
first, second, history = simulator.simulate(initial_amount, [config, config], extra_data=True, use_processes=False)