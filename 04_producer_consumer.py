"""Program 4: Producer-Consumer (bounded buffer) using semaphores."""

import threading
import time

from sync_common import Semaphore, safe_print

BUFFER_SIZE = 5
ITEMS = 10

buffer = [0] * BUFFER_SIZE
in_idx = 0
out_idx = 0
empty_slots = Semaphore(BUFFER_SIZE)
full_slots = Semaphore(0)
mtx = Semaphore(1)


def producer() -> None:
    global in_idx
    for i in range(1, ITEMS + 1):
        empty_slots.wait()
        mtx.wait()
        buffer[in_idx] = i
        safe_print(f"Producer produced item {i} at slot {in_idx}")
        in_idx = (in_idx + 1) % BUFFER_SIZE
        mtx.post()
        full_slots.post()
        time.sleep(0.10)


def consumer() -> None:
    global out_idx
    for _ in range(ITEMS):
        full_slots.wait()
        mtx.wait()
        item = buffer[out_idx]
        safe_print(f"\t\tConsumer consumed item {item} from slot {out_idx}")
        out_idx = (out_idx + 1) % BUFFER_SIZE
        mtx.post()
        empty_slots.post()
        time.sleep(0.15)


def main() -> int:
    prod = threading.Thread(target=producer)
    cons = threading.Thread(target=consumer)
    prod.start()
    cons.start()
    prod.join()
    cons.join()
    print("All items produced and consumed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
