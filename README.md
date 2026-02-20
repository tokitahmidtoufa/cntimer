# cntimer ⏱

[![PyPI version](https://badge.fury.io/py/cntimer.svg)](https://pypi.org/project/cntimer/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://pypi.org/project/cntimer/)

**Automatic execution time and memory tracker for Python scripts.**

No code changes. No config. Just `pip install cntimer` — every script you run will automatically show timing and memory at the end, whether you use VSCode, terminal, or any Python runner.

---

## Install

```bash
pip install cntimer
```

That's it. Every Python script you run will show this automatically:

```
────────────────────────────────────────────────────────────
  🕐 Time      0.74 ms        (execution: 1.44 s)
  📦 Memory    31.2 MB       (peak: 62.4 MB)
────────────────────────────────────────────────────────────
```

> ✅ Works in base Python, virtual environments (venv), conda, and pipx — no extra steps needed.

---

## How it works

`cntimer` places a `cntimer.pth` file into your Python's `site-packages` directory. Python automatically reads all `.pth` files on **every startup** — which is what makes tracking work with zero code changes.

When you uninstall with `pip uninstall cntimer`, the `.pth` hook removes itself automatically on the next Python startup — no orphaned files, no errors.

- ✅ Works with VSCode Run button
- ✅ Works in terminal
- ✅ Works in virtual environments (venv, conda, pipx)
- ✅ Works on Windows (x86, x64, ARM64), macOS, Linux
- ✅ No imports needed in your code
- ✅ Cleans up after itself on uninstall

---

## Output explained

| Field | Meaning |
|---|---|
| 🕐 Time | CPU time — actual computation (excludes sleep, I/O, network wait) |
| execution | Total execution time (how long you waited) |
| 📦 Memory | Memory still in use when script finished |
| peak | Highest memory used at any point during execution |

If **Time** is much bigger than **cpu**, your script spent time waiting (file I/O, network, sleep).  
If they're close, your script is CPU-bound (pure computation).

---

## Manual install (if auto-install failed)

Find your site-packages path:

```bash
# Mac / Linux
python3 -c "import site; print(site.getsitepackages()[0])"

# Windows
python -c "import site; print(site.getsitepackages()[0])"
```

Then copy the file:

### macOS

```bash
cp cntimer.pth $(python3 -c "import site; print(site.getsitepackages()[0])")/cntimer.pth
```

### Linux

```bash
sudo cp cntimer.pth $(python3 -c "import site; print(site.getsitepackages()[0])")/cntimer.pth
```

### Windows 64-bit / ARM64 — run Command Prompt as Administrator

```
copy cntimer.pth "C:\Program Files\Python3xx\Lib\site-packages\cntimer.pth"
```

### Windows 32-bit — run Command Prompt as Administrator

```
copy cntimer.pth "C:\Program Files (x86)\Python3xx\Lib\site-packages\cntimer.pth"
```

> Replace `3xx` with your Python version (e.g. `312` for Python 3.12).

---

## Uninstall

```bash
pip uninstall cntimer
```

The `.pth` hook removes itself automatically on the next Python startup. No manual cleanup needed.

---

## License

[MIT](LICENSE) © 2026 tokitahmidtoufa
