# Critical Section Problem & Resolution

This project demonstrates the **Critical Section Problem** (Race Condition) in multi-threaded programming and how it can be resolved using **Mutexes**.

## Files in this Directory

1.  `raceCondition.c`: Demonstrates the problem. Multiple threads attempt to increment a shared counter without synchronization, leading to data inconsistency.
2.  `criticalSectionResolution.c`: Demonstrates the solution. Uses a `pthread_mutex_t` to ensure that only one thread can access the critical section (incrementing the counter) at a time.

## What is the Critical Section Problem?

A **Critical Section** is a part of the code where shared resources (like variables, files, etc.) are accessed. If multiple threads or processes modify the same resource concurrently without protection, it leads to a **Race Condition**. 

The result is "non-deterministic" behavior where the final state depends on the timing of thread execution, often leading to incorrect results.

## Requirements for a Solution

A solution to the Critical Section problem must satisfy three requirements:
1.  **Mutual Exclusion**: Only one thread at a time can be in its critical section.
2.  **Progress**: If no thread is in its critical section, and some threads wish to enter, only those threads not in their remainder sections can participate in the decision of who will enter next.
3.  **Bounded Waiting**: There must be a limit on the number of times other threads are allowed to enter their critical sections after a thread has made a request to enter its critical section.

## How to Run

### Compilation
You need a C compiler (like GCC) with `pthread` support. On Linux or Windows (MinGW), run:

```bash
gcc raceCondition.c -o raceCondition -pthread
gcc criticalSectionResolution.c -o criticalSectionResolution -pthread
```

### Execution

1.  **Run the Race Condition demo:**
    ```bash
    ./raceCondition
    ```
    *Observe that the final counter value is likely less than the expected value.*

2.  **Run the Resolution demo:**
    ```bash
    ./criticalSectionResolution
    ```
    *Observe that the final counter value is exactly as expected.*
