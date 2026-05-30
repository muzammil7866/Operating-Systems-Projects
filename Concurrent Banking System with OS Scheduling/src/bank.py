import threading
import csv
import os
from datetime import datetime

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCOUNTS_FILE  = os.path.join(_BASE, "data", "accounts.csv")
TRANSACTIONS_LOG = os.path.join(_BASE, "data", "transactions.log")
SESSION_LOG    = os.path.join(_BASE, "data", "session.log")

LOW_BALANCE_THRESHOLD    = 1_000
LARGE_TRANSACTION_THRESHOLD = 5_000
MAX_CONCURRENT_THREADS   = 2


class BankManagementSystem:

    def __init__(self):
        self.accounts  = {}
        self.lock      = threading.Lock()
        self.semaphore = threading.Semaphore(MAX_CONCURRENT_THREADS)
        os.makedirs(os.path.join(_BASE, "data"), exist_ok=True)
        self._load_accounts()
        self._clear_session_log()

    # ── File I/O ──────────────────────────────────────────────────────────────

    def _load_accounts(self):
        try:
            with open(ACCOUNTS_FILE, newline="") as f:
                for row in csv.DictReader(f):
                    self.accounts[row["pin"]] = {
                        "name":    row["name"],
                        "balance": float(row["balance"]),
                        "salary":  float(row["salary"]),
                        "phone":   row["phone"],
                    }
            print(f"Loaded {len(self.accounts)} account(s).")
        except FileNotFoundError:
            print("No account file found — run seed_data.py to create sample accounts.")

    def _save_accounts(self):
        with open(ACCOUNTS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["pin", "name", "balance", "salary", "phone"])
            writer.writeheader()
            for pin, data in self.accounts.items():
                writer.writerow({"pin": pin, **data})

    def _clear_session_log(self):
        open(SESSION_LOG, "w").close()

    def _append_log(self, path, pin, action, amount, ts):
        name = self.accounts.get(pin, {}).get("name", "unknown")
        with open(path, "a") as f:
            f.write(f"{pin},{name},{action},{amount:.2f},{ts}\n")

    def _log_transaction(self, pin, action, amount, ts):
        self._append_log(TRANSACTIONS_LOG, pin, action, amount, ts)
        self._append_log(SESSION_LOG,      pin, action, amount, ts)

    # ── Alerts ────────────────────────────────────────────────────────────────

    def _check_alerts(self, pin, amount):
        if amount > LARGE_TRANSACTION_THRESHOLD:
            print(f"  [ALERT] Large transaction detected: {amount:.2f} Rs")
        if self.accounts[pin]["balance"] < LOW_BALANCE_THRESHOLD:
            print(f"  [ALERT] Low balance for {self.accounts[pin]['name']}: "
                  f"{self.accounts[pin]['balance']:.2f} Rs")

    # ── Auth ──────────────────────────────────────────────────────────────────

    def authenticate(self):
        pin = input("Enter PIN: ").strip()
        if pin in self.accounts:
            return pin
        print("  Invalid PIN.")
        return None

    # ── Account Management ────────────────────────────────────────────────────

    def open_account(self):
        name = input("Full name: ").strip()
        if not name:
            print("  Name cannot be empty.")
            return
        while True:
            pin = input("PIN (4 digits): ").strip()
            if len(pin) != 4 or not pin.isdigit():
                print("  PIN must be exactly 4 digits.")
                continue
            if pin in self.accounts:
                print("  PIN already in use — choose another.")
                continue
            break
        phone = input("Phone number: ").strip()
        try:
            salary  = float(input("Monthly salary (Rs): "))
            balance = float(input("Opening balance (Rs): "))
        except ValueError:
            print("  Invalid amount — account not created.")
            return
        if balance < 0 or salary < 0:
            print("  Amounts cannot be negative.")
            return
        self.accounts[pin] = {
            "name": name, "balance": balance,
            "salary": salary, "phone": phone,
        }
        self._save_accounts()
        print(f"  Account opened for {name} (PIN: {pin}).")

    def close_account(self):
        pin = self.authenticate()
        if pin:
            confirm = input(f"  Close account for {self.accounts[pin]['name']}? (yes/no): ").strip().lower()
            if confirm == "yes":
                del self.accounts[pin]
                self._save_accounts()
                print("  Account closed.")
            else:
                print("  Cancelled.")

    # ── Transactions ──────────────────────────────────────────────────────────

    def deposit(self):
        pin = self.authenticate()
        if not pin:
            return
        try:
            amount = float(input("Deposit amount (Rs): "))
        except ValueError:
            print("  Invalid amount.")
            return
        if amount <= 0:
            print("  Amount must be positive.")
            return
        t = threading.Thread(target=self._deposit_safe, args=(pin, amount))
        t.start()
        t.join()

    def _deposit_safe(self, pin, amount):
        with self.semaphore:
            with self.lock:
                if pin not in self.accounts:
                    print("  Account not found.")
                    return
                self.accounts[pin]["balance"] += amount
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"  Deposited {amount:.2f} Rs. New balance: {self.accounts[pin]['balance']:.2f} Rs  [{ts}]")
                self._log_transaction(pin, "deposit", amount, ts)
                self._check_alerts(pin, amount)
                self._save_accounts()

    def withdrawal(self):
        pin = self.authenticate()
        if not pin:
            return
        try:
            amount = float(input("Withdrawal amount (Rs): "))
        except ValueError:
            print("  Invalid amount.")
            return
        if amount <= 0:
            print("  Amount must be positive.")
            return
        t = threading.Thread(target=self._withdrawal_safe, args=(pin, amount))
        t.start()
        t.join()

    def _withdrawal_safe(self, pin, amount):
        with self.semaphore:
            with self.lock:
                if pin not in self.accounts:
                    print("  Account not found.")
                    return
                if self.accounts[pin]["balance"] < amount:
                    print(f"  Insufficient balance. Available: {self.accounts[pin]['balance']:.2f} Rs")
                    return
                self.accounts[pin]["balance"] -= amount
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"  Withdrew {amount:.2f} Rs. New balance: {self.accounts[pin]['balance']:.2f} Rs  [{ts}]")
                self._log_transaction(pin, "withdrawal", amount, ts)
                self._check_alerts(pin, amount)
                self._save_accounts()

    def transfer(self):
        print("  Source account:")
        src = self.authenticate()
        if not src:
            return
        dest = input("  Destination PIN: ").strip()
        if dest not in self.accounts:
            print("  Destination account not found.")
            return
        if dest == src:
            print("  Cannot transfer to the same account.")
            return
        try:
            amount = float(input("  Transfer amount (Rs): "))
        except ValueError:
            print("  Invalid amount.")
            return
        if amount <= 0:
            print("  Amount must be positive.")
            return
        with self.semaphore:
            with self.lock:
                if self.accounts[src]["balance"] < amount:
                    print(f"  Insufficient balance. Available: {self.accounts[src]['balance']:.2f} Rs")
                    return
                self.accounts[src]["balance"]  -= amount
                self.accounts[dest]["balance"] += amount
                ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._log_transaction(src,  "transfer-out", amount, ts)
                self._log_transaction(dest, "transfer-in",  amount, ts)
                print(f"  Transferred {amount:.2f} Rs from {self.accounts[src]['name']} "
                      f"to {self.accounts[dest]['name']}  [{ts}]")
                self._check_alerts(src, amount)
                self._save_accounts()

    def check_balance(self):
        pin = self.authenticate()
        if pin:
            print(f"  Balance: {self.accounts[pin]['balance']:.2f} Rs")

    def show_transaction_history(self):
        pin = self.authenticate()
        if not pin:
            return
        try:
            with open(TRANSACTIONS_LOG) as f:
                rows = [l.strip().split(",") for l in f if l.startswith(pin + ",")]
        except FileNotFoundError:
            print("  No transaction log found.")
            return
        if not rows:
            print("  No transactions on record.")
            return
        print(f"\n  History for {self.accounts[pin]['name']} (PIN {pin}):\n")
        print(f"  {'Timestamp':<22} {'Action':<15} {'Amount (Rs)':>12}")
        print("  " + "-" * 52)
        for r in rows:
            if len(r) == 5:
                _, _, action, amount, ts = r
                print(f"  {ts:<22} {action:<15} {float(amount):>12.2f}")

    # ── Dev / Admin ──────────────────────────────────────────────────────────

    def process_salary(self):
        pin = self.authenticate()
        if pin:
            salary = self.accounts[pin]["salary"]
            self._deposit_safe(pin, salary)
            print(f"  Salary of {salary:.2f} Rs credited.")
