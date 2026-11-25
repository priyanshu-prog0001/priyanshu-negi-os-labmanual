# priyanshu-negi-os-labmanual
# Operating Systems Lab Practicals (CEC301 / CSC301)

A collection of 11 core Operating Systems lab programs implemented in **Python 3** for **B.Tech (CSE) — 5th Semester**.

* **Submitted by:** Priyanshu Negi (Roll No. `2472171`)

* **Submitted to:** Mrs. Yashvi Uniyal

## Programs Overview

| \# | File | Topic | Brief Description | 
| ----- | ----- | ----- | ----- | 
| 1 | `01_fork_exec_wait.py` | Process Management | Demonstrates POSIX process creation and lifecycle using `os.fork()`, `os.execlp()`, and `os.waitpid()` (with a Windows `subprocess` fallback). | 
| 2 | `02_pthreads_sum.py` | Multithreading | Splits the summation of `0..999,999` across 4 concurrent threads using Python's `threading` module and combines partial sums via `join()`. | 
| 3 | `03_cpu_scheduling.py` | CPU Scheduling | Interactive menu-driven simulator for **FCFS**, **SJF (Non-preemptive)**, **Priority (Non-preemptive)**, and **Round Robin**, computing CT, TAT, WT, and averages. | 
| — | `sync_common.py` | Shared Helper | Provides a custom counting `Semaphore` (built on `threading.Condition`) and `safe_print()` used by Programs 4, 5, and 6. | 
| 4 | `04_producer_consumer.py` | Producer-Consumer | Solves the Bounded Buffer problem using three semaphores (`empty_slots`, `full_slots`, `mtx`) for mutual exclusion and buffer coordination. | 
| 5 | `05_readers_writers.py` | Readers-Writers | Implements the first Readers-Writers problem (readers' preference), allowing concurrent reads while guaranteeing exclusive writer access. | 
| 6 | `06_dining_philosophers.py` | Dining Philosophers | Prevents circular-wait deadlock among 5 philosophers by using a `room` semaphore that limits at most `N - 1` philosophers at the table concurrently. | 
| 7 | `07_bankers_algorithm.py` | Deadlock Avoidance | Implements the Banker's Safety Algorithm and Resource-Request Algorithm with tentative allocation and rollback on unsafe states. | 
| 8 | `08_memory_allocation.py` | Memory Allocation | Compares **First Fit**, **Best Fit**, and **Worst Fit** contiguous memory allocation strategies and reports total remaining free memory (fragmentation). | 
| 9 | `09_page_replacement.py` | Page Replacement | Simulates **FIFO**, **LRU**, and **Optimal** page replacement policies for a given reference string and frame count, comparing total page faults. | 
| 10 | `10_disk_scheduling.py` | Disk Scheduling | Computes total disk head movement for **FCFS**, **SSTF**, **SCAN**, and **C-SCAN** scheduling algorithms. | 
| 11 | `11_file_allocation.py` | File Allocation | Simulates **Contiguous**, **Linked**, and **Indexed** disk block allocation methods across a 30-block disk. | 

## Prerequisites

* **Python 3.10+** (uses standard library modules only — no external packages required).

* For `01_fork_exec_wait.py`, a Linux/macOS environment exercises `os.fork()`, `os.execlp()`, and `os.waitpid()`; on Windows, it automatically falls back to `subprocess.Popen`.

## How to Run

Keep `sync_common.py` in the same directory as the program files, then run any script with:

```
python3 01_fork_exec_wait.py
python3 02_pthreads_sum.py
python3 03_cpu_scheduling.py
python3 04_producer_consumer.py
python3 05_readers_writers.py
python3 06_dining_philosophers.py
python3 07_bankers_algorithm.py
python3 08_memory_allocation.py
python3 09_page_replacement.py
python3 10_disk_scheduling.py
python3 11_file_allocation.py

```
