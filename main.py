from simulator import Simulator
import random
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Configuration Parameters
    generation_size = 10
    initial_amount = 100_000
    generations = 10
    tickers = []

    with open("tickers.txt", "r") as f:
        tickers = f.readlines()

    for i, ticker in enumerate(tickers):
        tickers[i] = ticker.strip()

    simulator = Simulator(tickers)

    generation_params = []

    # Generate random first generation
    for _ in range(generation_size):
        generation_params.append(random.sample(range(-100, 100), 10))

    # Simulate Each Generation
    for i in range(generations):
        print(f"Generation {i + 1} / {generations}...")

        # Simulate
        best, history = simulator.simulate(
            initial_amount, generation_params, generation=i + 1)
        
        first = best[0]

        second = best[1]

        print("Generation " + str(i + 1) + ": " + str(history.iloc[-1]))

        first_params = get_parameters(first)

        print("Parameters: ", first_params)
        plt.plot(history, label="Generation " + str(i + 1))

        # Crossover for next generation
        generation_params = crossover(
            first_params, get_parameters(second), generation_size)

    plt.legend(loc='best')
    plt.show()

# Crossover best 2 arrays
def crossover(first, second, generation_size):
    fl = len(first)
    first = np.array(first)
    second = np.array(second)

    offspring = []

    for _ in range(generation_size):
        # Single point or Uniform crossover at random
        crossover_type = np.random.choice(['single', 'uniform'])

        if crossover_type == 'single':
            # Take first `half` of one and second of the other
            crossover_point = np.random.randint(1, fl)
            child = np.concatenate(
                (first[:crossover_point], second[crossover_point:]))
        elif crossover_type == 'uniform':
            # Randomly select each attribute between parents
            mask = np.random.randint(0, 2, fl, dtype=bool)
            child = np.where(mask, first, second)

        # Create some randomness
        random_values = np.random.uniform(-10, 10, fl)
        np.add(
            child, random_values,
            out=child, casting='unsafe')

        offspring.append(child.tolist())

    return offspring

# Reconstruct parameters array from disected attributes in model
def get_parameters(model):
    parameters = model.weights.copy()
    parameters += model.offsets
    parameters.append(model.threshold)
    parameters.append(model.sensitivity)

    return parameters

if __name__ == "__main__":
    main()