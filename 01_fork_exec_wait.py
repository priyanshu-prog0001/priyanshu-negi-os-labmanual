"""Program 1: Process creation using fork(), exec(), and wait()."""

import os
import subprocess
import sys


def main() -> int:
    print(f"Parent process: PID = {os.getpid()}", flush=True)

    if hasattr(os, "fork"):
        pid = os.fork()
        if pid < 0:
            print("fork failed", file=sys.stderr)
            return 1
        if pid == 0:
            print(f"Child process: PID = {os.getpid()}, Parent PID = {os.getppid()}")
            print("Child is about to exec 'ls -l'", flush=True)
            try:
                os.execlp("ls", "ls", "-l")
            except OSError as exc:
                print(f"exec failed: {exc}", file=sys.stderr)
                os._exit(1)
        else:
            print(f"Parent waiting for child (PID = {pid}) to finish...")
            _, status = os.waitpid(pid, 0)
            if os.WIFEXITED(status):
                print(f"Child exited with status {os.WEXITSTATUS(status)}")
            print("Parent process resumes and exits.")
    else:
        # Windows does not support POSIX fork/execlp; spawn a child process instead.
        proc = subprocess.Popen(["cmd", "/c", "dir"])
        print(f"Parent waiting for child (PID = {proc.pid}) to finish...")
        returncode = proc.wait()
        print(f"Child exited with status {returncode}")
        print("Parent process resumes and exits.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
