# Concurrent Banking System with OS Scheduling

## Overview

This project implements a multi-threaded, multi-process banking simulation in Python that applies core operating-systems concepts in a realistic context. Each OS mechanism is not merely described but actively exercised as part of normal system operation: deposits and withdrawals contend on a shared resource controlled by a mutex and a semaphore, inter-process communication dispatches notifications via a multiprocessing queue, and the session's transaction log is replayed through a Round Robin CPU scheduler with computed turnaround and waiting time metrics.

## OS Concepts Demonstrated

| Concept | Implementation |
|---|---|
| **Mutex (Lock)** | `threading.Lock` serialises all account state mutations — no two threads can modify balances simultaneously |
| **Semaphore** | `threading.Semaphore(2)` caps concurrent banking threads at 2, modelling bounded resource access |
| **Threads** | Every deposit/withdrawal is dispatched to a `threading.Thread`, then joined to preserve response ordering |
| **Processes & Fork** | IPC mode creates one `multiprocessing.Process` per transaction — each is a fully isolated OS process |
| **Inter-Process Communication (IPC)** | `multiprocessing.Queue` carries results from child processes back to the parent without shared memory |
| **CPU Scheduling — Round Robin** | Session transactions are treated as processes with equal burst time; the scheduler cycles a ready queue with a configurable time slice and reports TAT and WT per transaction |
| **File I/O as Persistent State** | `accounts.csv` acts as a simple persistent store; `transactions.log` is an append-only audit log; `session.log` captures the current session for scheduler replay |

## Project Structure

```
Concurrent Banking System with OS Scheduling/
├── main.py             Entry point — interactive menu
├── seed_data.py        Bootstraps sample accounts and transaction history
├── src/
│   ├── bank.py         BankManagementSystem class (mutex, semaphore, threads)
│   └── scheduler.py    IPC and Round Robin scheduling implementations
├── data/
│   ├── accounts.csv    Persistent account store (auto-managed)
│   ├── transactions.log Append-only historical transaction audit log
│   └── session.log     Per-session transaction log (cleared on startup)
└── docs/
    ├── OS PROJECT.docx
    └── A Simple Banking System Simulation.pdf
```

## Requirements

- Python 3.8 or later
- Standard library only (`threading`, `multiprocessing`, `csv`, `datetime`)

## Quick Start

```bash
# 1. Seed sample accounts (run once)
python seed_data.py

# 2. Launch the system
python main.py
```

Sample PINs after seeding: `1001`, `2002`, `3003`, `4004`

## Architecture

### Thread Safety

All account mutations go through two synchronisation primitives stacked together:

```
Thread → acquire Semaphore (max 2 concurrent) → acquire Lock (mutual exclusion) → modify balance → release
```

The semaphore models a resource with bounded capacity (e.g. a limited number of bank tellers). The mutex beneath it guarantees that even among the permitted threads only one at a time can write to the accounts dictionary, preventing race conditions on shared state.

### IPC Notification Processing (Dev Mode → Option 1)

Each transaction recorded in `session.log` is replayed by spawning a separate OS process. The parent process collects results via `multiprocessing.Queue` — a kernel-mediated communication channel. This demonstrates the producer-consumer pattern across process boundaries without shared memory.

```
Parent
  ├─ Process(transaction_1) → Queue.put(result)
  ├─ Process(transaction_2) → Queue.put(result)
  └─ ...
      join all → drain Queue → print results
```

### Round Robin Scheduling (Dev Mode → Option 3)

Session transactions are modelled as CPU processes, each with `burst_time = 1` unit. The scheduler maintains a ready queue and cycles through it one time slice at a time, mirroring the Round Robin algorithm taught in OS theory.

After all transactions complete, the following are printed for each transaction and as session averages:

```
Turnaround Time (TAT) = Completion Time - Arrival Time
Waiting Time (WT)     = TAT - Burst Time
```

This makes concrete the abstract metrics used when comparing scheduling algorithms.

## Menu Reference

### Main Menu

| Option | Action |
|---|---|
| 1 | Open an account |
| 2 | Deposit |
| 3 | Withdrawal |
| 4 | Transfer between accounts |
| 5 | Check balance |
| 6 | Full transaction history |
| 7 | Close an account |
| 8 | Dev Mode (password: `69420`) |
| 0 | Exit |

### Dev Menu

| Option | Action | OS Concept |
|---|---|---|
| 1 | Process session notifications | IPC via `multiprocessing.Queue` |
| 2 | Credit monthly salary | Thread-safe deposit |
| 3 | Run Round Robin scheduler | CPU scheduling with TAT/WT |

## Alert Thresholds

| Alert | Threshold |
|---|---|
| Low balance warning | Balance < 1,000 Rs |
| Large transaction flag | Amount > 5,000 Rs |

## Data Files

`data/accounts.csv` — fields: `pin, name, balance, salary, phone`  
`data/transactions.log` — fields: `pin, name, action, amount, timestamp`  
`data/session.log` — same format as `transactions.log`, cleared each run

These files are auto-created by `seed_data.py` or on first use.

## Notes

- The dev password is hardcoded as `69420` for demonstration purposes only.
- `multiprocessing.Process` requires the worker functions (`_ipc_worker`, `_rr_worker`) to be module-level — they cannot be instance methods or local functions. This is a Windows constraint tied to how `spawn` creates child processes.
- `session.log` is cleared on every startup so the IPC and Round Robin demos always operate on the current session's transactions.
