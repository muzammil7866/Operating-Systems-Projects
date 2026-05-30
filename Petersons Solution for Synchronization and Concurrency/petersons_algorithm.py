"""Peterson's algorithm demo for two-thread mutual exclusion."""

from __future__ import annotations

import threading
import time


class PetersonLock:
    def __init__(self) -> None:
        self.flag = [False, False]
        self.turn = 0

    def enter_critical_section(self, process_id: int) -> None:
        other = 1 - process_id
        self.flag[process_id] = True
        self.turn = other
        while self.flag[other] and self.turn == other:
            time.sleep(0)

    def exit_critical_section(self, process_id: int) -> None:
        self.flag[process_id] = False


def process(lock: PetersonLock, process_id: int, iterations: int = 5) -> None:
    for _ in range(iterations):
        lock.enter_critical_section(process_id)
        try:
            print(f"Process {process_id} is in the critical section.")
            time.sleep(1)
            print(f"Process {process_id} is leaving the critical section.")
        finally:
            lock.exit_critical_section(process_id)
        time.sleep(1)


def main() -> None:
    lock = PetersonLock()
    thread_one = threading.Thread(target=process, args=(lock, 0))
    thread_two = threading.Thread(target=process, args=(lock, 1))

    thread_one.start()
    thread_two.start()
    thread_one.join()
    thread_two.join()


if __name__ == "__main__":
    main()
