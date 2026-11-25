"""Program 7: Deadlock avoidance - Banker's Algorithm."""

import sys

P = 5  # processes
R = 3  # resource types

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


def calculate_need(
    maximum: list[list[int]], allocation: list[list[int]]
) -> list[list[int]]:
    return [
        [maximum[i][j] - allocation[i][j] for j in range(R)]
        for i in range(P)
    ]


def is_safe(
    available: list[int],
    allocation: list[list[int]],
    need: list[list[int]],
) -> tuple[bool, list[int]]:
    work = available[:]
    finish = [False] * P
    safe_seq: list[int] = []

    while len(safe_seq) < P:
        found = False
        for i in range(P):
            if finish[i]:
                continue
            if all(need[i][j] <= work[j] for j in range(R)):
                for k in range(R):
                    work[k] += allocation[i][k]
                safe_seq.append(i)
                finish[i] = True
                found = True
        if not found:
            return False, []
    return True, safe_seq


def request_resources(
    pid: int,
    request: list[int],
    available: list[int],
    allocation: list[list[int]],
    need: list[list[int]],
) -> bool:
    for j in range(R):
        if request[j] > need[pid][j]:
            print("Error: process has exceeded its maximum claim.")
            return False
        if request[j] > available[j]:
            print("Request denied: not enough resources available.")
            return False

    for j in range(R):  # tentative allocation
        available[j] -= request[j]
        allocation[pid][j] += request[j]
        need[pid][j] -= request[j]

    safe, seq = is_safe(available, allocation, need)
    if safe:
        seq_str = " ".join(f"P{s}" for s in seq)
        print(f"Request can be granted safely.\nSafe sequence: {seq_str}")
        return True

    for j in range(R):  # rollback
        available[j] += request[j]
        allocation[pid][j] -= request[j]
        need[pid][j] += request[j]

    print("Request denied: would lead to an unsafe state.")
    return False


def main() -> int:
    available = read_ints(f"Enter available resources of each type ({R} types): ", R)

    max_flat = read_ints(f"Enter Maximum matrix ({P} processes x {R} resources):\n", P * R)
    maximum = [max_flat[i * R : (i + 1) * R] for i in range(P)]

    alloc_flat = read_ints("Enter Allocation matrix:\n", P * R)
    allocation = [alloc_flat[i * R : (i + 1) * R] for i in range(P)]

    need = calculate_need(maximum, allocation)

    safe, seq = is_safe(available, allocation, need)
    if safe:
        seq_str = " ".join(f"P{s}" for s in seq)
        print(f"System is in a SAFE state.\nSafe sequence: {seq_str}")
    else:
        print("System is in an UNSAFE state.")

    (pid,) = read_ints("\nEnter process number requesting resources: ", 1)
    if pid < 0 or pid >= P:
        print("Invalid process number.")
        return 1
    request = read_ints(f"Enter request vector ({R} values): ", R)
    request_resources(pid, request, available, allocation, need)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
