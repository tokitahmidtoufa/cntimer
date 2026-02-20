# Self-contained autostart — no imports from cntimer package needed.
# This is triggered by cntimer.pth on every Python startup.
import sys
import os
import atexit
import time
import tracemalloc


def _should_track():
    if sys.flags.interactive:
        return False
    if not sys.argv or not sys.argv[0] or sys.argv[0] in ("-c", "-m", ""):
        return False
    basename = os.path.basename(sys.argv[0])
    skip = {
        "pip", "pip3", "pip3.14", "pytest", "py.test", "mypy", "black",
        "ruff", "isort", "flake8", "pylint", "cntimer", "python", "python3",
    }
    if basename in skip:
        return False
    return True


def _format_time(seconds):
    ms = seconds * 1000
    if ms < 1000:
        return f"{ms:.1f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    else:
        return f"{int(seconds // 60)}m {seconds % 60:.1f}s"


def _format_mem(bytes_val):
    if bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.0f} KB"
    return f"{bytes_val / 1024 / 1024:.1f} MB"


def _show_stats(start_wall, start_cpu):
    wall = time.perf_counter() - start_wall
    cpu  = time.process_time() - start_cpu
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    w = 60
    print(f"\n\033[90m{'─' * w}\033[0m")
    print(f"\033[96m  🕐 Time    \033[0m  {_format_time(cpu):<14}  \033[90m(execution: {_format_time(wall)})\033[0m")
    print(f"\033[96m  📦 Memory  \033[0m  {_format_mem(current):<14}  \033[90m(peak: {_format_mem(peak)})\033[0m")
    print(f"\033[90m{'─' * w}\033[0m")


if _should_track():
    try:
        tracemalloc.start()
        _start_wall = time.perf_counter()
        _start_cpu  = time.process_time()
        atexit.register(_show_stats, _start_wall, _start_cpu)
    except Exception:
        pass
