# Like main.py except easy to run a single config (helps find bugs)
from simulator import Simulator
import argparse
import ast

parser = argparse.ArgumentParser(description="Run a single trading configuration over a custom date range and ticker set.")
parser.add_argument('config', type=str, 
                   help='Configuration parameters as a list, e.g., "[6, -94, -29, 21, -26, 74, 72, 46, 64, 7]"')
parser.add_argument('--initial-cash', type=float, default=100, 
                    help='Initial cash amount (default: 100)')
parser.add_argument('--start-date', type=str, default='2000-01-01', 
                    help='Start date for simulation (format: YYYY-MM-DD, default: 2000-01-01)')
parser.add_argument('--end-date', type=str, default='2010-01-01', 
                    help='End date for simulation (format: YYYY-MM-DD, default: 2010-01-01)')
parser.add_argument('--tickers-file', type=str, default='tickers.txt', 
                    help='Path to the tickers file (default: tickers.txt)')

args = parser.parse_args()

initial_cash = args.initial_cash
tickers = []

with open(args.tickers_file, "r") as f:
    tickers = f.readlines()

for i, ticker in enumerate(tickers):
    tickers[i] = ticker.strip()

config = ast.literal_eval(args.config)

simulator = Simulator(tickers)
best, history = simulator.simulate(initial_cash, [config], extra_data=True, use_processes=False, start_date=args.start_date, end_date=args.end_date)