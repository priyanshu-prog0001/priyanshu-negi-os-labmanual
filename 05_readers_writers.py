"""Program 5: Readers-Writers problem (first problem, readers preference)."""

import threading
import time

from sync_common import Semaphore, safe_print

mtx = Semaphore(1)
wrt = Semaphore(1)
read_count = 0
shared_data = 0


def reader(reader_id: int) -> None:
    global read_count
    mtx.wait()
    read_count += 1
    if read_count == 1:
        wrt.wait()  # first reader locks the resource
    mtx.post()

    safe_print(f"Reader {reader_id}: read shared_data = {shared_data}")
    time.sleep(0.20)

    mtx.wait()
    read_count -= 1
    if read_count == 0:
        wrt.post()  # last reader unlocks the resource
    mtx.post()


def writer(writer_id: int) -> None:
    global shared_data
    wrt.wait()
    shared_data += 1
    safe_print(f"Writer {writer_id}: wrote shared_data = {shared_data}")
    time.sleep(0.30)
    wrt.post()


def main() -> int:
    threads: list[threading.Thread] = []

    w1 = threading.Thread(target=writer, args=(1,))
    threads.append(w1)
    w1.start()

    time.sleep(0.02)  # let writer 1 start first

    for i in range(1, 6):
        r = threading.Thread(target=reader, args=(i,))
        threads.append(r)
        r.start()

    w2 = threading.Thread(target=writer, args=(2,))
    threads.append(w2)
    w2.start()

    for t in threads:
        t.join()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
