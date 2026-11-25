"""Program 10: Disk scheduling - FCFS, SSTF, SCAN, C-SCAN.

SCAN / C-SCAN: head first moves towards the higher cylinders.
"""

import sys

_tokens: list[int] = []


def read_ints(prompt: str, count: int) -> list[int]:
    if prompt:
        print(prompt, end="", flush=True)
    while len(_tokens) < count:
        line = sys.stdin.readline()
        if not line:
            raise EOFError("Unexpected end of input")
        _tokens.extend(int(tok) for tok in line.split())
    values = _tokens[:count]
    del _tokens[:count]
    return values


def fcfs(req: list[int], head: int) -> int:
    total = 0
    cur = head
    for r in req:
        total += abs(cur - r)
        cur = r
    return total


def sstf(req: list[int], head: int) -> int:
    n = len(req)
    visited = [False] * n
    total = 0
    cur = head
    for _ in range(n):
        idx = min(
            (i for i in range(n) if not visited[i]),
            key=lambda i: abs(cur - req[i]),
        )
        visited[idx] = True
        total += abs(cur - req[idx])
        cur = req[idx]
    return total


def scan(req: list[int], head: int, disk_size: int) -> int:
    lo = sorted(r for r in req if r < head)
    hi = sorted(r for r in req if r >= head)
    total = 0
    cur = head
    for r in hi:
        total += abs(cur - r)
        cur = r
    if lo:  # go to the end, then reverse
        total += abs(cur - (disk_size - 1))
        cur = disk_size - 1
        for r in reversed(lo):
            total += abs(cur - r)
            cur = r
    return total


def cscan(req: list[int], head: int, disk_size: int) -> int:
    lo = sorted(r for r in req if r < head)
    hi = sorted(r for r in req if r >= head)
    total = 0
    cur = head
    for r in hi:
        total += abs(cur - r)
        cur = r
    if lo:
        total += abs(cur - (disk_size - 1))  # to the last cylinder
        total += disk_size - 1  # jump back to cylinder 0
        cur = 0
        for r in lo:
            total += abs(cur - r)
            cur = r
    return total


def main() -> int:
    (n,) = read_ints("Enter number of requests: ", 1)
    req = read_ints("Enter the requests: ", n)
    (head,) = read_ints("Enter initial head position: ", 1)
    (disk_size,) = read_ints("Enter disk size (max cylinder + 1): ", 1)

    print(f"FCFS   total head movement = {fcfs(req, head)}")
    print(f"SSTF   total head movement = {sstf(req, head)}")
    print(f"SCAN   total head movement = {scan(req, head, disk_size)}")
    print(f"C-SCAN total head movement = {cscan(req, head, disk_size)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
