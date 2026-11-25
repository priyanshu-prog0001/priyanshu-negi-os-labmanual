"""Program 8: Contiguous memory allocation - First Fit, Best Fit, Worst Fit."""

from enum import Enum, auto
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


class Strategy(Enum):
    FIRST = auto()
    BEST = auto()
    WORST = auto()


def allocate(
    bsize: list[int], psize: list[int], strategy: Strategy, title: str
) -> None:
    block = bsize[:]
    alloc = [-1] * len(psize)

    for i, req in enumerate(psize):
        pick = -1
        for j, free in enumerate(block):
            if free < req:
                continue
            if pick == -1:
                pick = j
            elif strategy == Strategy.BEST and free < block[pick]:
                pick = j
            elif strategy == Strategy.WORST and free > block[pick]:
                pick = j
            if strategy == Strategy.FIRST:
                break
        if pick != -1:
            alloc[i] = pick
            block[pick] -= req

    print(f"\n--- {title} ---")
    print("Process No.\tProcess Size\tBlock No.")
    for i, req in enumerate(psize):
        block_label = f"B{alloc[i] + 1}" if alloc[i] != -1 else "Not Allocated"
        print(f"P{i + 1}\t\t{req}\t\t{block_label}")
    print(f"Total remaining free memory (fragments) = {sum(block)}")


def main() -> int:
    (bn,) = read_ints("Enter number of memory blocks: ", 1)
    bsize = read_ints("Enter sizes of blocks: ", bn)
    (pn,) = read_ints("Enter number of processes: ", 1)
    psize = read_ints("Enter sizes of processes: ", pn)

    allocate(bsize, psize, Strategy.FIRST, "First Fit")
    allocate(bsize, psize, Strategy.BEST, "Best Fit")
    allocate(bsize, psize, Strategy.WORST, "Worst Fit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
