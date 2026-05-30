import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from bank import BankManagementSystem
from scheduler import process_with_ipc, process_with_round_robin

_DEV_PASSWORD = "69420"

_MAIN_MENU = """
  ┌──────────────────────────────────────┐
  │     Concurrent Banking System        │
  ├──────────────────────────────────────┤
  │  1.  Open an Account                 │
  │  2.  Deposit                         │
  │  3.  Withdrawal                      │
  │  4.  Transfer                        │
  │  5.  Check Balance                   │
  │  6.  Transaction History             │
  │  7.  Close an Account                │
  │  8.  Dev Mode                        │
  │  0.  Exit                            │
  └──────────────────────────────────────┘"""

_DEV_MENU = """
  ┌──────────────────────────────────────┐
  │              Dev Menu                │
  ├──────────────────────────────────────┤
  │  1.  Process Notifications (IPC)     │
  │  2.  Credit Salary                   │
  │  3.  Round Robin Scheduling          │
  │  0.  Back                            │
  └──────────────────────────────────────┘"""


def _dev_menu(bank: BankManagementSystem) -> None:
    pwd = input("  Dev password: ").strip()
    if pwd != _DEV_PASSWORD:
        print("  Incorrect password.")
        return
    while True:
        print(_DEV_MENU)
        choice = input("  Option: ").strip()
        if   choice == "1": process_with_ipc()
        elif choice == "2": bank.process_salary()
        elif choice == "3": process_with_round_robin()
        elif choice == "0": break
        else: print("  Invalid option.")


def main() -> None:
    bank = BankManagementSystem()
    while True:
        print(_MAIN_MENU)
        choice = input("  Option: ").strip()
        if   choice == "1": bank.open_account()
        elif choice == "2": bank.deposit()
        elif choice == "3": bank.withdrawal()
        elif choice == "4": bank.transfer()
        elif choice == "5": bank.check_balance()
        elif choice == "6": bank.show_transaction_history()
        elif choice == "7": bank.close_account()
        elif choice == "8": _dev_menu(bank)
        elif choice == "0":
            print("  Goodbye.")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
