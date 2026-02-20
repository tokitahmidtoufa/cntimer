import sys
import os
import runpy


def main():
    args = sys.argv[1:]

    if not args:
        print("cntimer v0.1.11")
        print("Usage: cntimer script.py [args...]")
        sys.exit(0)

    script = args[0]

    if not os.path.exists(script):
        print(f"[cntimer] ❌ File not found: {script}")
        sys.exit(1)

    sys.argv = args

    from cntimer.tracker import start
    start()

    runpy.run_path(script, run_name="__main__")


if __name__ == "__main__":
    main()
