"""Program 11: File allocation methods - Contiguous, Linked, Indexed."""

import sys

MAX_BLOCKS = 30
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


def contiguous_allocation() -> None:
    disk = [0] * MAX_BLOCKS
    (nf,) = read_ints("\n--- Contiguous Allocation ---\nEnter number of files: ", 1)
    for f in range(1, nf + 1):
        start, length = read_ints(f"File {f} - starting block, length: ", 2)
        if start < 0 or length <= 0 or start + length > MAX_BLOCKS or any(
            disk[i] == 1 for i in range(start, start + length)
        ):
            print("Allocation failed: blocks not free/out of range.")
            continue
        for i in range(start, start + length):
            disk[i] = 1
        print(f"File {f} allocated blocks {start} to {start + length - 1}")


def linked_allocation() -> None:
    disk = [0] * MAX_BLOCKS
    (nf,) = read_ints("\n--- Linked Allocation ---\nEnter number of files: ", 1)
    for f in range(1, nf + 1):
        (length,) = read_ints(f"File {f} - number of blocks: ", 1)
        allocated: list[str] = []
        for i in range(MAX_BLOCKS):
            if len(allocated) >= length:
                break
            if disk[i] == 0:
                disk[i] = 1
                allocated.append(str(i))
        chain = " -> ".join(allocated) + (" -> " if allocated else "") + "NULL"
        print(f"File {f} allocated blocks: {chain}")
        if len(allocated) < length:
            print("Warning: disk full, could not allocate all blocks.")


def indexed_allocation() -> None:
    disk = [0] * MAX_BLOCKS
    (nf,) = read_ints("\n--- Indexed Allocation ---\nEnter number of files: ", 1)
    for f in range(1, nf + 1):
        (length,) = read_ints(f"File {f} - number of data blocks needed: ", 1)
        index_block = next((i for i in range(MAX_BLOCKS) if disk[i] == 0), -1)
        if index_block == -1:
            print("Disk full.")
            continue
        disk[index_block] = 1
        data_blocks: list[str] = []
        for i in range(MAX_BLOCKS):
            if len(data_blocks) >= length:
                break
            if disk[i] == 0:
                disk[i] = 1
                data_blocks.append(str(i))
        blocks_str = " ".join(data_blocks)
        print(f"File {f} - Index block: {index_block}, Data blocks: {blocks_str}")
        if len(data_blocks) < length:
            print("Warning: disk full, could not allocate all blocks.")


def main() -> int:
    (choice,) = read_ints(
        "Menu:\n1. Contiguous Allocation\n2. Linked Allocation\n"
        "3. Indexed Allocation\nEnter choice: ",
        1,
    )
    if choice == 1:
        contiguous_allocation()
    elif choice == 2:
        linked_allocation()
    elif choice == 3:
        indexed_allocation()
    else:
        print("Invalid choice")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
