from simulator import Simulator
import random
import numpy as np
import matplotlib.pyplot as plt

generation_size = 10
initial_amount = 100_000
generations = 10
tickers = []

with open("tickers.txt", "r") as f:
    tickers = f.readlines()

for i, ticker in enumerate(tickers):
    tickers[i] = ticker.strip()

# To make it easier to process
tickers = tickers[:200]

simulator = Simulator(tickers)

generation = []


def crossover(first, second, generation_size):
    fl = len(first)
    first = np.array(first)
    second = np.array(second)

    offspring = []

    for _ in range(generation_size):
        crossover_type = np.random.choice(['single', 'uniform'])

        if crossover_type == 'single':
            crossover_point = np.random.randint(1, fl)
            child = np.concatenate(
                (first[:crossover_point], second[crossover_point:]))
        elif crossover_type == 'uniform':
            mask = np.random.randint(0, 2, fl, dtype=bool)
            child = np.where(mask, first, second)

        random_values = np.random.uniform(-10, 10, fl)
        np.add(
            child, random_values,
            out=child, casting='unsafe')

        offspring.append(child.tolist())

    return offspring


def get_parameters(model):
    parameters = model.weights
    parameters += model.offsets
    parameters.append(model.threshold)

    return parameters


for _ in range(generation_size):
    generation.append(random.sample(range(-100, 100), 9))

for i in range(generations):
    print(f"Generation {i + 1} / {generations}...")
    first, second, history = simulator.simulate(
        initial_amount, generation)

    print("Generation " + str(i + 1) + ": " + str(history.iloc[-1]))

    first_params = get_parameters(first)

    print("Parameters: ", first_params)
    plt.plot(history, label="Generation " + str(i + 1))

    generation = crossover(
        first_params, get_parameters(second), generation_size)

plt.legend(loc='best')
plt.show()
