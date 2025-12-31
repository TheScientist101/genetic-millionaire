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

## Usage

### Running the Genetic Algorithm (main.py)

Train models using the genetic algorithm with the following command:

```bash
python3 main.py --generation-size 20 --initial-cash 10000 --generations 15 --start-date 2005-01-01 --end-date 2015-01-01 --tickers-file tickers_training.txt
```

**Available options:**

- `--generation-size`: Number of individuals in each generation (default: 10)
- `--initial-cash`: Initial cash amount (default: 100)
- `--generations`: Number of generations to simulate (default: 10)
- `--start-date`: Start date for simulation in YYYY-MM-DD format (default: 2000-01-01)
- `--end-date`: End date for simulation in YYYY-MM-DD format (default: 2010-01-01)
- `--tickers-file`: Path to the tickers file (default: tickers.txt)

### Testing a Single Configuration (simulate_single_model.py)

Test a specific model configuration using the following command:

```bash
python3 simulate_single_model.py "<config>" --initial-cash 5000 --start-date 2010-01-01 --end-date 2020-01-01 --tickers-file tickers_testing.txt
```

**Available options:**

- `config`: Configuration parameters as a list produced by `main.py` (required)
- `--initial-cash`: Initial cash amount (default: 100)
- `--start-date`: Start date for simulation in YYYY-MM-DD format (default: 2000-01-01)
- `--end-date`: End date for simulation in YYYY-MM-DD format (default: 2010-01-01)
- `--tickers-file`: Path to the tickers file (default: tickers.txt)

## License

This project is licensed under the GPL v3 License. See the [LICENSE](LICENSE) file for details.
