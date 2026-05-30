
# Peterson's Solution

## Overview

This project demonstrates Peterson's algorithm for two-thread mutual exclusion. It shows how two worker threads coordinate access to a critical section without a heavyweight lock.

## Business Goal

The goal is educational: it translates a classic operating-systems concept into runnable code that can be studied, demonstrated, and compared against other synchronization approaches.

## Structure

- `petersons_algorithm.py` - lock implementation and thread demo

## Run

```bash
python petersons_algorithm.py
```

## Notes

This is a teaching example for synchronization and concurrency, not a production concurrency primitive.
