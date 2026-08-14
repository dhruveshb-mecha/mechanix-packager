"""Helpers shared by package.py, resolve_version.py, and every packager.

REPO_ROOT is the cwd this tool is invoked from - the app repo being
packaged.
"""

import re
import shutil
from pathlib import Path

REPO_ROOT = Path.cwd()
STAGE_DIR = REPO_ROOT / "stage"


def read_upstream_version() -> str:
    pubspec = REPO_ROOT / "pubspec.yaml"
    if not pubspec.exists():
        raise SystemExit(f"{pubspec} not found - run this from an app repo's root")
    match = re.search(r"^version:\s*(\S+)", pubspec.read_text(), re.MULTILINE)
    if not match:
        raise SystemExit(f"No version field found in {pubspec}")
    return match.group(1).split("+")[0]


def find_bundle_dir() -> Path:
    matches = sorted(REPO_ROOT.glob("build/elinux/*/release/bundle"))
    if not matches:
        raise SystemExit(
            "No build bundle found under build/elinux/*/release/bundle. "
            "Run `flutter-elinux build elinux --release` first."
        )
    return matches[0]


def stage_bundle(bundle_dir: Path) -> Path:
    if STAGE_DIR.exists():
        shutil.rmtree(STAGE_DIR)
    STAGE_DIR.mkdir(parents=True)
    dest = STAGE_DIR / "bundle"
    shutil.copytree(bundle_dir, dest)
    return dest
