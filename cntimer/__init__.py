import os
import shutil
import sysconfig


def _ensure_pth_installed():
    """
    Fallback: copy cntimer.pth into the active site-packages if it's not
    already there. This runs on first `cntimer script.py` in case the
    wheel's purelib injection didn't place it (e.g. very old pip).
    """
    try:
        target_dir = sysconfig.get_path("purelib")
        if not target_dir or not os.path.isdir(target_dir):
            return

        dest = os.path.join(target_dir, "cntimer.pth")
        if os.path.exists(dest):
            return  # already installed — stay silent

        pkg_dir = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(pkg_dir, "cntimer.pth")

        if os.path.exists(src) and os.access(target_dir, os.W_OK):
            shutil.copy2(src, dest)
            print("[cntimer] ✅ Auto-tracking enabled for this environment!")
            print("[cntimer]    Run your script once normally — it now tracks automatically.\n")
    except Exception:
        pass


_ensure_pth_installed()

from .tracker import start  # noqa: E402

__version__ = "0.1.11"
__all__ = ["start"]
