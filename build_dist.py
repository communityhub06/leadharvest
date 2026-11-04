"""Build the two LeadHarvest artifacts from one source tree.

  python build_dist.py          -> dist/leadharvest-1.0.0.zip        (Free, public)
  python build_dist.py --pro    -> dist/leadharvest-1.0.0-pro.zip    (paid, Gumroad)

The only difference is ``leadharvest/tier.py`` plus two README sentences, so the
two editions can never drift apart structurally.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")

INCLUDE_DIRS = ["leadharvest", "tests", "examples"]
INCLUDE_FILES = ["README.md", "LICENSE", "pyproject.toml"]
PRO_ONLY_FILES = ["INSTALL.txt"]
EXCLUDE_DIRS = {"__pycache__", ".git", "dist", "build"}

FREE_EDITION_LINE = (
    "This build is **Free**: 25 URLs per run, CSV export, five social platforms."
)
PRO_EDITION_LINE = (
    "This build is **Pro**: unlimited URLs, CSV and JSON export, crawl mode, "
    "region hints and 14+ social platforms."
)
FREE_INSTALL_BLOCK = "```bash\npip install leadharvest\n```"
PRO_INSTALL_BLOCK = "```bash\npip install .\n```"


def pro_tier_source() -> str:
    path = os.path.join(ROOT, "leadharvest", "tier.py")
    src = open(path, encoding="utf-8").read()
    if "PRO = False" not in src:
        raise SystemExit("tier.py no longer contains PRO = False — update this script")
    return src.replace("PRO = False", "PRO = True", 1)


def pro_readme(src: str) -> str:
    if FREE_EDITION_LINE not in src:
        raise SystemExit("README edition line changed — update this script")
    if FREE_INSTALL_BLOCK not in src:
        raise SystemExit("README install block changed — update this script")
    return src.replace(FREE_EDITION_LINE, PRO_EDITION_LINE, 1).replace(
        FREE_INSTALL_BLOCK, PRO_INSTALL_BLOCK, 1
    )


def collect(pro: bool) -> list[tuple[str, str]]:
    """Return (absolute path, archive name) pairs."""
    entries: list[tuple[str, str]] = []

    files = list(INCLUDE_FILES)
    if pro:
        files += PRO_ONLY_FILES
    for name in files:
        full = os.path.join(ROOT, name)
        if not os.path.isfile(full):
            raise SystemExit(f"missing file: {name}")
        entries.append((full, name))

    for d in INCLUDE_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            raise SystemExit(f"missing dir: {d}")
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [x for x in dirnames if x not in EXCLUDE_DIRS]
            for fn in sorted(filenames):
                if fn.endswith((".pyc", ".pyo")):
                    continue
                full = os.path.join(dirpath, fn)
                rel = os.path.relpath(full, ROOT).replace("\\", "/")
                entries.append((full, rel))

    return entries


def build(pro: bool) -> str:
    os.makedirs(DIST, exist_ok=True)
    out = os.path.join(DIST, "leadharvest-1.0.0-pro.zip" if pro else "leadharvest-1.0.0.zip")
    if os.path.exists(out):
        os.remove(out)

    entries = collect(pro)
    overrides: dict[str, bytes] = {}

    if pro:
        overrides["leadharvest/tier.py"] = pro_tier_source().encode("utf-8")
        readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
        overrides["README.md"] = pro_readme(readme).encode("utf-8")

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in sorted(entries, key=lambda x: x[1]):
            data = overrides.get(rel)
            if data is None:
                with open(full, "rb") as fh:
                    data = fh.read()
            z.writestr(rel, data)

    with zipfile.ZipFile(out) as z:
        bad = z.testzip()
        names = sorted(z.namelist())
    print(f"{'pro ' if pro else 'free'} {out}  {os.path.getsize(out)}B  {len(names)} files  corrupt={bad}")
    return out


def verify(zip_path: str, pro: bool) -> None:
    """Extract, confirm the edition, and run the suite from the shipped tree."""
    tmp = os.path.join(os.environ.get("TEMP", "."), "lh_verify_pro" if pro else "lh_verify_free")
    if os.path.exists(tmp):
        shutil.rmtree(tmp, ignore_errors=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(tmp)

    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"

    probe = subprocess.run(
        [sys.executable, "-c", "from leadharvest import tier; print(tier.PRO, tier.MAX_URLS, tier.FORMATS, len(tier.SOCIAL or ()))"],
        cwd=tmp, env=env, capture_output=True, text=True, timeout=120,
    )
    print(f"  tier in archive: {probe.stdout.strip() or probe.stderr.strip()[:200]}")

    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider"],
        cwd=tmp, env=env, capture_output=True, text=True, timeout=300,
    )
    tail = (r.stdout or "").strip().splitlines()[-1] if r.stdout else (r.stderr or "")[-300:]
    print(f"  pytest rc={r.returncode}  {tail}")
    if r.returncode != 0:
        raise SystemExit(f"tests failed inside {zip_path}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pro", action="store_true", help="build the paid edition")
    args = ap.parse_args()

    path = build(args.pro)
    verify(path, args.pro)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
