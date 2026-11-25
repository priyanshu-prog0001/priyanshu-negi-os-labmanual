"""Program 9: Page replacement - FIFO, LRU, Optimal."""

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


def fifo(ref: list[int], nf: int) -> int:
    frames = [-1] * nf
    front = 0
    faults = 0
    for page in ref:
        if page not in frames:
            frames[front] = page
            front = (front + 1) % nf
            faults += 1
    return faults


def lru(ref: list[int], nf: int) -> int:
    frames: list[int] = []
    last_used: list[int] = []
    faults = 0
    for i, page in enumerate(ref):
        if page in frames:
            last_used[frames.index(page)] = i
            continue
        faults += 1
        if len(frames) < nf:
            frames.append(page)
            last_used.append(i)
        else:
            victim = min(range(nf), key=lambda j: last_used[j])
            frames[victim] = page
            last_used[victim] = i
    return faults


def optimal(ref: list[int], nf: int) -> int:
    frames: list[int] = []
    faults = 0
    n = len(ref)
    for i, page in enumerate(ref):
        if page in frames:
            continue
        faults += 1
        if len(frames) < nf:
            frames.append(page)
            continue
        victim = -1
        farthest = -1
        for j, frame_page in enumerate(frames):
            try:
                next_use = ref.index(frame_page, i + 1)
            except ValueError:
                victim = j  # never used again
                break
            if next_use > farthest:
                farthest = next_use
                victim = j
        frames[victim] = page
    return faults


def main() -> int:
    (n,) = read_ints("Enter number of pages in reference string: ", 1)
    ref = read_ints("Enter the reference string: ", n)
    (nf,) = read_ints("Enter number of frames: ", 1)
    if nf <= 0:
        print("Number of frames must be positive.")
        return 1

    print(f"FIFO Page Faults    = {fifo(ref, nf)}")
    print(f"LRU Page Faults     = {lru(ref, nf)}")
    print(f"Optimal Page Faults = {optimal(ref, nf)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
