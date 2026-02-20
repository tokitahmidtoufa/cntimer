import glob
import os
import platform
import shutil
import site
import sys
import sysconfig
import zipfile
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.develop import develop

# ── Wheel injection ────────────────────────────────────────────────────────────
# Modern pip installs wheels by unzipping them.  Files placed under
#   {name}-{version}.data/purelib/
# inside the .whl are extracted directly to site-packages root.
# We subclass bdist_wheel to inject cntimer.pth there after the wheel is built.
try:
    from wheel.bdist_wheel import bdist_wheel as _BdistWheel

    class BdistWheel(_BdistWheel):
        def run(self):
            super().run()
            self._inject_pth()

        def _inject_pth(self):
            here    = os.path.dirname(os.path.abspath(__file__))
            pth_src = os.path.join(here, "cntimer.pth")
            if not os.path.exists(pth_src):
                return

            # e.g. cntimer-0.1.7.data/purelib/cntimer.pth
            purelib_entry = "cntimer-0.1.7.data/purelib/cntimer.pth"

            for whl_path in glob.glob(os.path.join(self.dist_dir, "*.whl")):
                tmp = whl_path + ".tmp"
                with zipfile.ZipFile(whl_path, "r") as zin, \
                     zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
                    for item in zin.infolist():
                        if item.filename != purelib_entry:
                            zout.writestr(item, zin.read(item.filename))
                    zout.write(pth_src, purelib_entry)
                os.replace(tmp, whl_path)
                print(f"[cntimer] ✅ Injected cntimer.pth into wheel purelib")

    cmdclass_extra = {"bdist_wheel": BdistWheel}

except ImportError:
    cmdclass_extra = {}


# ── Legacy / editable install hook (pip install -e .) ─────────────────────────
def _get_site_packages():
    primary = sysconfig.get_path("purelib")
    if primary and os.path.isdir(primary) and os.access(primary, os.W_OK):
        return primary
    platlib = sysconfig.get_path("platlib")
    if platlib and os.path.isdir(platlib) and os.access(platlib, os.W_OK):
        return platlib
    if hasattr(site, "getsitepackages") and \
            not (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix):
        for p in site.getsitepackages():
            if os.path.isdir(p) and os.access(p, os.W_OK):
                return p
    if hasattr(site, "getusersitepackages"):
        user = site.getusersitepackages()
        os.makedirs(user, exist_ok=True)
        return user
    return None


def _install_pth():
    here   = os.path.dirname(os.path.abspath(__file__))
    src    = os.path.join(here, "cntimer.pth")
    sp     = _get_site_packages()
    system = platform.system()
    arch   = platform.architecture()[0]
    machine = platform.machine().lower()

    if sp and os.path.exists(src):
        dest = os.path.join(sp, "cntimer.pth")
        shutil.copy2(src, dest)
        print(f"\n[cntimer] ✅ Auto-tracking installed!")
        print(f"[cntimer]    Platform : {system} {arch} ({machine})")
        print(f"[cntimer]    Location : {dest}")
        print(f"[cntimer]    Every Python script will now show time + memory automatically.\n")
    else:
        print("\n[cntimer] ⚠️  Could not auto-install the tracking hook.")
        print(f"[cntimer]    Platform : {system} {arch} ({machine})")
        if system == "Windows":
            example = r"C:\Program Files\Python3xx\Lib\site-packages\cntimer.pth"
            print(f"[cntimer]    Run as Administrator: copy cntimer.pth \"{example}\"")
        elif system == "Darwin":
            print(f'[cntimer]    Run: cp cntimer.pth $(python3 -c "import site; print(site.getsitepackages()[0])")/cntimer.pth')
        else:
            print(f'[cntimer]    Run: sudo cp cntimer.pth $(python3 -c "import site; print(site.getsitepackages()[0])")/cntimer.pth')
        print(f"\n[cntimer]    📖 Full guide: https://github.com/tokitahmidtoufa/cntimer#manual-install\n")


class Install(install):
    def run(self):
        super().run()
        _install_pth()


class Develop(develop):
    def run(self):
        super().run()
        _install_pth()


setup(
    name="cntimer",
    version="0.1.11",
    packages=find_packages(),
    data_files=[("", ["cntimer.pth"])],
    entry_points={"console_scripts": ["cntimer=cntimer.cli:main"]},
    cmdclass={"install": Install, "develop": Develop, **cmdclass_extra},
)
