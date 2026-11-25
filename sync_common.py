"""Helpers for the synchronization programs (4, 5, and 6)."""

import threading


class Semaphore:
    """Small counting-semaphore class wrapping threading.Condition."""

    def __init__(self, count: int = 0) -> None:
        self._cond = threading.Condition()
        self._count = count

    def wait(self) -> None:
        """P operation (decrement, blocking if count == 0)."""
        with self._cond:
            while self._count <= 0:
                self._cond.wait()
            self._count -= 1

    def post(self) -> None:
        """V operation (increment and wake one waiter)."""
        with self._cond:
            self._count += 1
            self._cond.notify()


_print_lock = threading.Lock()


def safe_print(*args, **kwargs) -> None:
    """Thread-safe print so lines from different threads never interleave."""
    with _print_lock:
        print(*args, flush=True, **kwargs)
