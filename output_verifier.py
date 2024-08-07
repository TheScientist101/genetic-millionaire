# Initialize cash balance
cash_balance = 100000.0

# Portfolio to keep track of the number of shares for each stock
portfolio = {}

# Function to process each transaction
def process_transaction(date, action, shares, stock, price):
    global cash_balance, portfolio

    cost = shares * price

    if action == "Bought":
        if stock not in portfolio:
            portfolio[stock] = 0.0
        # Check if there is enough cash to buy
        if cash_balance >= cost:
            cash_balance -= cost
            portfolio[stock] += shares
        else:
            raise Exception(f"{date}: Insufficient funds to buy {shares:.3f} of {stock}")

    elif action == "Sold":
        # Check if there are enough shares to sell
        if portfolio[stock] >= shares:
            cash_balance += cost
            portfolio[stock] -= shares
        else:
            raise Exception(f"{date}: Insufficient shares to sell {shares:.3f} of {stock}")

# Open and read the transactions from the file
with open('outputs/purchases.txt', 'r') as file:
    for line in file:
        # Parse the line using string manipulation
        parts = line.strip().split(': ')
        date = parts[0]
        action, shares, _, stock, _, price = parts[1].split(' ')

        shares = float(shares)
        price = float(price)

        # Process each transaction
        process_transaction(date, action, shares, stock, price)

# Output final portfolio and cash balance
print("\nFinal Portfolio:")
for stock, shares in portfolio.items():
    print(f"{stock}: {shares:.3f} shares")

print(f"\nFinal Cash Balance: ${cash_balance:.2f}")
