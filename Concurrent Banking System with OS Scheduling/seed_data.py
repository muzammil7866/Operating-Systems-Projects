"""
Bootstraps the data/ directory with sample accounts and a transaction history.
Run once before launching main.py for the first time.
"""

import csv
import os

_BASE          = os.path.dirname(os.path.abspath(__file__))
DATA_DIR       = os.path.join(_BASE, "data")
ACCOUNTS_FILE  = os.path.join(DATA_DIR, "accounts.csv")
TRANSACTIONS_LOG = os.path.join(DATA_DIR, "transactions.log")

SAMPLE_ACCOUNTS = [
    {"pin": "1001", "name": "Alice Khan",   "balance": 15000.0, "salary": 50000.0, "phone": "03001234567"},
    {"pin": "2002", "name": "Bob Ahmed",    "balance":  3200.0, "salary": 35000.0, "phone": "03119876543"},
    {"pin": "3003", "name": "Sara Malik",   "balance":   800.0, "salary": 28000.0, "phone": "03214567890"},
    {"pin": "4004", "name": "Omar Sheikh",  "balance": 22500.0, "salary": 75000.0, "phone": "03331122334"},
]

SAMPLE_TRANSACTIONS = [
    ("1001", "Alice Khan",  "deposit",    5000.00, "2025-01-10 09:15:00"),
    ("2002", "Bob Ahmed",   "withdrawal", 1500.00, "2025-01-10 09:20:00"),
    ("3003", "Sara Malik",  "deposit",     500.00, "2025-01-10 10:05:00"),
    ("1001", "Alice Khan",  "transfer-out",2000.00,"2025-01-11 14:30:00"),
    ("2002", "Bob Ahmed",   "transfer-in", 2000.00,"2025-01-11 14:30:00"),
    ("4004", "Omar Sheikh", "deposit",   10000.00, "2025-01-12 08:00:00"),
    ("3003", "Sara Malik",  "withdrawal",  200.00, "2025-01-13 16:45:00"),
]


def seed():
    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(ACCOUNTS_FILE):
        print(f"Accounts file already exists — skipping account seed.")
    else:
        with open(ACCOUNTS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["pin", "name", "balance", "salary", "phone"])
            writer.writeheader()
            writer.writerows(SAMPLE_ACCOUNTS)
        print(f"Seeded {len(SAMPLE_ACCOUNTS)} accounts.")
        print("  Sample PINs: 1001 | 2002 | 3003 | 4004")

    if os.path.exists(TRANSACTIONS_LOG):
        print(f"Transaction log already exists — skipping history seed.")
    else:
        with open(TRANSACTIONS_LOG, "a") as f:
            for pin, name, action, amount, ts in SAMPLE_TRANSACTIONS:
                f.write(f"{pin},{name},{action},{amount:.2f},{ts}\n")
        print(f"Seeded {len(SAMPLE_TRANSACTIONS)} historical transactions.")


if __name__ == "__main__":
    seed()
