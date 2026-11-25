"""Program 3: CPU Scheduling - FCFS, SJF, Priority, Round Robin."""

from collections import deque
from dataclasses import dataclass, replace
import sys
from typing import Callable

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


@dataclass
class Process:
    pid: int
    at: int
    bt: int
    pr: int
    ct: int = 0
    tat: int = 0
    wt: int = 0
    rem: int = 0


def finish(proc: Process, time: int) -> None:
    proc.ct = time
    proc.tat = proc.ct - proc.at
    proc.wt = proc.tat - proc.bt


def print_result(procs: list[Process]) -> None:
    ordered = sorted(procs, key=lambda x: x.pid)
    total_wt = 0
    total_tat = 0
    print("\nPID\tAT\tBT\tCT\tTAT\tWT")
    for x in ordered:
        print(f"{x.pid}\t{x.at}\t{x.bt}\t{x.ct}\t{x.tat}\t{x.wt}")
        total_wt += x.wt
        total_tat += x.tat
    print(f"Average Waiting Time    = {total_wt / len(ordered):.2f}")
    print(f"Average Turnaround Time = {total_tat / len(ordered):.2f}")


def fcfs(procs: list[Process]) -> None:
    p = sorted((replace(x) for x in procs), key=lambda x: (x.at, x.pid))
    time = 0
    for x in p:
        time = max(time, x.at) + x.bt
        finish(x, time)
    print_result(p)


def non_preemptive(procs: list[Process], key: Callable[[Process], int]) -> None:
    """Generic non-preemptive scheduler; key() decides who runs next (smaller = better)."""
    p = [replace(x) for x in procs]
    n = len(p)
    done = [False] * n
    completed = 0
    time = 0

    while completed < n:
        ready = [i for i in range(n) if not done[i] and p[i].at <= time]
        if not ready:
            time += 1
            continue
        idx = min(ready, key=lambda i: key(p[i]))
        time += p[idx].bt
        finish(p[idx], time)
        done[idx] = True
        completed += 1

    print_result(p)


def round_robin(procs: list[Process], quantum: int) -> None:
    p = [replace(x, rem=x.bt) for x in procs]
    n = len(p)
    order = sorted(range(n), key=lambda i: (p[i].at, p[i].pid))
    q: deque[int] = deque()
    next_idx = 0  # next process (by arrival) to admit
    time = 0
    completed = 0

    def admit() -> None:
        nonlocal next_idx
        while next_idx < n and p[order[next_idx]].at <= time:
            q.append(order[next_idx])
            next_idx += 1

    admit()
    while completed < n:
        if not q:
            time = p[order[next_idx]].at
            admit()
            continue
        idx = q.popleft()
        slice_time = min(quantum, p[idx].rem)
        time += slice_time
        p[idx].rem -= slice_time
        admit()  # new arrivals go before the preempted process
        if p[idx].rem > 0:
            q.append(idx)
        else:
            finish(p[idx], time)
            completed += 1

    print_result(p)


def main() -> int:
    (n,) = read_ints("Enter number of processes: ", 1)
    procs: list[Process] = []
    for i in range(n):
        at, bt, pr = read_ints(
            f"Process {i + 1} - Arrival Time, Burst Time, Priority: ", 3
        )
        procs.append(Process(pid=i + 1, at=at, bt=bt, pr=pr))

    (choice,) = read_ints(
        "\nMenu:\n1. FCFS\n2. SJF (Non-preemptive)\n"
        "3. Priority (Non-preemptive)\n4. Round Robin\nEnter choice: ",
        1,
    )
    if choice == 1:
        fcfs(procs)
    elif choice == 2:
        non_preemptive(procs, lambda x: x.bt)
    elif choice == 3:
        non_preemptive(procs, lambda x: x.pr)
    elif choice == 4:
        (quantum,) = read_ints("Enter time quantum: ", 1)
        round_robin(procs, quantum)
    else:
        print("Invalid choice")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
