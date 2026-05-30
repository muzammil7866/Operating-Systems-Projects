"""
OS Scheduling demonstrations using session transaction data.

Two algorithms are provided:
  - IPC via multiprocessing.Queue: each transaction is dispatched to a
    separate OS process; results are collected through a shared queue.
  - Round Robin CPU scheduling: transactions are treated as processes
    with equal burst time, cycled through a time-sliced queue.
    Turnaround Time (TAT) and Waiting Time (WT) are reported.
"""

import os
from multiprocessing import Process, Queue

_BASE        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSION_LOG  = os.path.join(_BASE, "data", "session.log")


# ── Standalone worker functions (must be module-level for multiprocessing) ────

def _ipc_worker(queue, pin, name, action, amount, ts):
    msg = f"  [{ts}]  {name} (PIN {pin}):  {action}  {amount:.2f} Rs — processed"
    queue.put(msg)


def _rr_worker(queue, pin, name, action, amount, time_slice):
    msg = (f"  {name} (PIN {pin}):  {action}  {amount:.2f} Rs "
           f"— completed in {time_slice}s slice")
    queue.put(msg)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _load_session_transactions():
    """Parse session.log into a list of transaction dicts."""
    try:
        with open(SESSION_LOG) as f:
            rows = []
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 5:
                    pin, name, action, amount, ts = parts
                    rows.append({
                        "pin":    pin,
                        "name":   name,
                        "action": action,
                        "amount": float(amount),
                        "ts":     ts,
                    })
            return rows
    except FileNotFoundError:
        return []


# ── Public scheduling functions ───────────────────────────────────────────────

def process_with_ipc():
    """
    Dispatch each session transaction to a separate OS process.
    Processes communicate results back to the parent via a Queue (IPC).
    Demonstrates: fork-based process creation, inter-process communication.
    """
    transactions = _load_session_transactions()
    if not transactions:
        print("  No session transactions to process.")
        return

    print(f"\n  IPC Notification Processing — {len(transactions)} transaction(s)\n")
    queue    = Queue()
    procs    = []

    for t in transactions:
        p = Process(
            target=_ipc_worker,
            args=(queue, t["pin"], t["name"], t["action"], t["amount"], t["ts"]),
        )
        procs.append(p)
        p.start()

    for p in procs:
        p.join()

    while not queue.empty():
        print(queue.get())

    print(f"\n  All {len(transactions)} notifications dispatched.\n")


def process_with_round_robin(time_slice: int = 1):
    """
    Simulate Round Robin CPU scheduling over session transactions.

    Each transaction is modelled as a process with burst_time = 1 unit.
    The scheduler cycles through the ready queue in time slices.
    After all transactions complete, per-process TAT and WT are printed
    alongside averages — the same metrics used in OS scheduling analysis.

    TAT = Completion Time - Arrival Time (arrival assumed 0 for all)
    WT  = TAT - Burst Time
    """
    transactions = _load_session_transactions()
    if not transactions:
        print("  No session transactions to process.")
        return

    print(f"\n  Round Robin Scheduling — time slice: {time_slice}s  "
          f"({len(transactions)} transaction(s))\n")

    queue        = Queue()
    current_time = 0
    completed    = []
    # Each entry carries scheduling state alongside transaction data
    ready_queue  = [
        {**t, "burst": 1, "start": None, "end": None}
        for t in transactions
    ]

    while ready_queue:
        entry = ready_queue.pop(0)
        if entry["start"] is None:
            entry["start"] = current_time

        p = Process(
            target=_rr_worker,
            args=(queue, entry["pin"], entry["name"],
                  entry["action"], entry["amount"], time_slice),
        )
        p.start()
        p.join()

        current_time   += time_slice
        entry["burst"] -= time_slice

        while not queue.empty():
            print(queue.get())

        if entry["burst"] <= 0:
            entry["end"] = current_time
            completed.append(entry)
        else:
            ready_queue.append(entry)  # re-queue if not finished

    if not completed:
        print("  No transactions completed.")
        return

    print(f"\n  {'PIN':<8} {'Name':<20} {'Action':<14} {'TAT':>5} {'WT':>5}")
    print("  " + "─" * 56)

    total_tat = total_wt = 0
    for e in completed:
        tat = e["end"] - e["start"]
        wt  = tat - 1          # WT = TAT - burst_time (burst_time = 1)
        total_tat += tat
        total_wt  += wt
        print(f"  {e['pin']:<8} {e['name']:<20} {e['action']:<14} {tat:>5} {wt:>5}")

    n = len(completed)
    print(f"\n  Average Turnaround Time : {total_tat / n:.2f}")
    print(f"  Average Waiting Time    : {total_wt  / n:.2f}\n")
