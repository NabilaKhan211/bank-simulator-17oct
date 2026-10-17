# Menu-Driven Bank Account Simulator

**Veda Technology: Python Programming Track · Level 1 · Task 17 (Day 17)**

A simple banking simulator that supports **balance inquiry, deposit, withdrawal, and transaction history** through a menu.

## Features
- Account state kept in one dictionary that every function receives and updates
- Transactions stored in a list (each transaction is a dictionary)
- Withdrawals greater than the available balance are rejected
- Input validation: numbers only, positive amounts, maximum 2 decimal places, per-transaction limit
- Uses `Decimal` instead of `float` so money is always exact
- Optional opening balance when the account is created
- Menu runs in a loop until the user exits

## Requirements
Python 3.6+ (standard library only)

## How to Run
```bash
python bank_simulator.py
```

## Menu
```
1. Check balance
2. Deposit money
3. Withdraw money
4. Transaction history
5. Exit
```

## Data Structure
```python
account = {
    "holder": "Nabila",
    "number": "AC1001",
    "balance": Decimal("3750.25"),
    "transactions": [
        {"id": 1, "type": "Deposit", "amount": Decimal("5000.00"),
         "balance_after": Decimal("5000.00"), "time": "2026-10-17 07:31:21", "note": "Opening balance"},
        ...
    ],
}
```

## Sample Output
```
Enter amount to deposit: 1500
Deposited Rs. 1,500.00. New balance: Rs. 6,500.00

Enter amount to withdraw: 10000
Insufficient funds. Available balance: Rs. 4,500.00, requested: Rs. 10,000.00.

#   Type                Amount   Balance After  Time
--------------------------------------------------------------------
1   Deposit           5,000.00        5,000.00  2026-10-17 07:31:21
2   Deposit           1,500.00        6,500.00  2026-10-17 07:31:21
3   Withdrawal        2,000.00        4,500.00  2026-10-17 07:31:21
```

## Functions
| Function | Purpose |
|---|---|
| `create_account()` | Builds the account dictionary (the application state) |
| `deposit()` | Adds money and records the transaction |
| `withdraw()` | Checks funds, subtracts money, records the transaction |
| `get_balance()` | Returns the current balance |
| `record_transaction()` | Appends a transaction to the history list |
| `parse_amount()` | Validates and converts user input to a `Decimal` |
| `show_history()` | Prints the transaction table |

## Author
Nabila, Veda Technology Intern