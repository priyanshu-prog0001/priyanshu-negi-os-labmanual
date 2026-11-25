"""Program 6: Dining Philosophers (deadlock avoided by allowing at most N-1 at the table)."""

import threading
import time

from sync_common import Semaphore, safe_print

N = 5
forks = [Semaphore(1) for _ in range(N)]
room = Semaphore(N - 1)


def philosopher(phil_id: int) -> None:
    left = phil_id
    right = (phil_id + 1) % N
    for _ in range(2):
        safe_print(f"Philosopher {phil_id} is thinking")
        time.sleep(0.10)
        room.wait()
        forks[left].wait()
        forks[right].wait()
        safe_print(
            f"Philosopher {phil_id} is eating (fork {left} and fork {right})"
        )
        time.sleep(0.15)
        forks[right].post()
        forks[left].post()
        room.post()
        safe_print(f"Philosopher {phil_id} finished eating and put down forks")


def main() -> int:
    threads = [threading.Thread(target=philosopher, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
