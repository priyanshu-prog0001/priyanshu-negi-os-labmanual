"""Program 2: Thread creation and management (Python threading)."""

from dataclasses import dataclass
import threading

NUM_THREADS = 4


@dataclass
class PartialSum:
    start: int
    end: int
    total: int = 0


def sum_range(data: PartialSum, lock: threading.Lock) -> None:
    data.total = sum(range(data.start, data.end))
    tid = threading.get_ident() % 100000
    with lock:
        print(f"Thread {tid}: sum[{data.start}..{data.end}) = {data.total}")


def main() -> int:
    n = 1_000_000
    chunk = n // NUM_THREADS
    lock = threading.Lock()
    threads: list[threading.Thread] = []
    results: list[PartialSum] = []

    for i in range(NUM_THREADS):
        start = i * chunk
        end = n if i == NUM_THREADS - 1 else (i + 1) * chunk
        ps = PartialSum(start=start, end=end)
        results.append(ps)
        t = threading.Thread(target=sum_range, args=(ps, lock))
        threads.append(t)
        t.start()

    total = 0
    for t, ps in zip(threads, results):
        t.join()
        total += ps.total

    print(f"Total sum (0 to {n - 1}) computed using {NUM_THREADS} threads = {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
