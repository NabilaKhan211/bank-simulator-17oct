"""Menu-Driven Bank Account Simulator.

Supports balance inquiry, deposit, withdrawal and transaction history.

State management:
    The whole account lives in ONE dictionary (`account`), which every
    function receives and updates:
        {"holder": ..., "number": ..., "balance": Decimal, "transactions": [ ... ]}
    Each transaction is a dictionary stored in the `transactions` list.

Money is handled with Decimal (not float) to avoid rounding errors such as
0.1 + 0.2 = 0.30000000000000004.
"""
from datetime import datetime
from decimal import Decimal, InvalidOperation

MAX_TRANSACTION = Decimal("1000000")  # safety limit per transaction


# ---------- Account operations (all kept inside functions) ----------
def create_account(holder, number, opening_balance=Decimal("0")):
    """Create the account dictionary (the application state)."""
    account = {"holder": holder, "number": number,
               "balance": Decimal("0.00"), "transactions": []}
    if opening_balance > 0:
        deposit(account, opening_balance, note="Opening balance")
    return account


def record_transaction(account, kind, amount, note=""):
    """Append a transaction record to the history list."""
    account["transactions"].append({
        "id": len(account["transactions"]) + 1,
        "type": kind,
        "amount": amount,
        "balance_after": account["balance"],
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": note,
    })


def deposit(account, amount, note=""):
    """Add money to the account. Returns (success, message)."""
    if amount <= 0:
        return False, "Deposit amount must be greater than zero."
    account["balance"] += amount
    record_transaction(account, "Deposit", amount, note)
    return True, f"Deposited {money(amount)}. New balance: {money(account['balance'])}"


def withdraw(account, amount):
    """Remove money if funds are available. Returns (success, message)."""
    if amount <= 0:
        return False, "Withdrawal amount must be greater than zero."
    if amount > account["balance"]:
        return False, (f"Insufficient funds. Available balance: {money(account['balance'])}, "
                       f"requested: {money(amount)}.")
    account["balance"] -= amount
    record_transaction(account, "Withdrawal", amount)
    return True, f"Withdrew {money(amount)}. New balance: {money(account['balance'])}"


def get_balance(account):
    return account["balance"]


# ---------- Validation and formatting helpers ----------
def money(amount):
    return f"Rs. {amount:,.2f}"


def parse_amount(text):
    """Convert text to a valid Decimal amount, or return (None, error message)."""
    try:
        value = Decimal(text.strip())
    except InvalidOperation:
        return None, "Invalid amount. Please enter a number (e.g. 1500 or 250.75)."
    if not value.is_finite():
        return None, "Invalid amount. Please enter a number (e.g. 1500 or 250.75)."
    if value <= 0:
        return None, "Amount must be greater than zero."
    if value != value.quantize(Decimal("0.01")):
        return None, "Amount can have at most 2 decimal places."
    if value > MAX_TRANSACTION:
        return None, f"Amount exceeds the per-transaction limit of {money(MAX_TRANSACTION)}."
    return value, None


def ask_amount(prompt):
    amount, error = parse_amount(input(prompt))
    if error:
        print(error)
    return amount


# ---------- Menu actions ----------
def show_balance(account):
    print(f"\nAccount holder : {account['holder']}")
    print(f"Account number : {account['number']}")
    print(f"Current balance: {money(get_balance(account))}")


def do_deposit(account):
    amount = ask_amount("Enter amount to deposit: ")
    if amount is not None:
        print(deposit(account, amount)[1])


def do_withdraw(account):
    amount = ask_amount("Enter amount to withdraw: ")
    if amount is not None:
        print(withdraw(account, amount)[1])


def show_history(account):
    if not account["transactions"]:
        print("No transactions yet.")
        return
    print(f"\n{'#':<4}{'Type':<12}{'Amount':>14}{'Balance After':>16}  {'Time'}")
    print("-" * 68)
    for t in account["transactions"]:
        print(f"{t['id']:<4}{t['type']:<12}{t['amount']:>14,.2f}{t['balance_after']:>16,.2f}  {t['time']}")
    print(f"\nTotal transactions: {len(account['transactions'])}")


MENU = """
======= BANK ACCOUNT SIMULATOR =======
1. Check balance
2. Deposit money
3. Withdraw money
4. Transaction history
5. Exit
======================================
"""
ACTIONS = {"1": show_balance, "2": do_deposit, "3": do_withdraw, "4": show_history}


def read_opening_balance():
    """Ask for an opening balance. Blank or invalid input means a zero balance."""
    raw = input("Enter opening balance (press Enter for 0): ").strip()
    if raw == "":
        return Decimal("0")
    amount, error = parse_amount(raw)
    if error:
        print(f"{error} Starting with a zero balance.")
        return Decimal("0")
    return amount


def main():
    holder = input("Enter account holder name: ").strip() or "Customer"
    account = create_account(holder, "AC1001", read_opening_balance())
    print(f"\nWelcome, {holder}! Account AC1001 created.")

    while True:
        print(MENU)
        choice = input("Choose an option (1-5): ").strip()
        if choice == "5":
            print(f"Thank you for banking with us, {holder}. Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            action(account)
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()