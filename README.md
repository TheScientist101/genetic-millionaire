# Genetic Algorithm Simulator

## Overview

This program implements a genetic algorithm to optimize a given model using historical stock data. It utilizes a simulation environment to evolve solutions through crossover and mutation processes, evaluating their performance over generations.

## Installation

To install the required dependencies for this project, you should have Python 3.x installed. Create a virtual environment if needed, then use `pip` to install the packages listed in `requirements.txt`.

1. **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    ```

2. **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

3. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install .NET SDK (required for stock_indicators library)**

    https://dotnet.microsoft.com/en-us/download/visual-studio-sdks

## Usage

1. **Set up parameters:**

   ```python
   generation_size = 10
   initial_amount = 100_000
   generations = 10
   ticker=["AAPL", "GOOGL"]

   generation = []
   ```

4. **Run the program:**

   ```bash
   python3 main.py
   ```

## License

This project is licensed under the GPL v3 License. See the [LICENSE](LICENSE) file for details.
