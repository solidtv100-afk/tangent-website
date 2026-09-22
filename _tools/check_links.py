#!/usr/bin/env python3
"""
Resolves every internal link in the built site against the filesystem.

A dead internal link on a privacy or data-deletion page is not a cosmetic
problem: those URLs go into the Google Play listing, and a 404 behind one is
a compliance failure as much as a broken page. This runs in CI so it cannot
be forgotten.
"""

from __future__ import annotations
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP = ("http://", "https://", "mailto:", "#", "data:", "tel:")


def main() -> int:
    broken: list[str] = []
    checked = 0

    for html in sorted(ROOT.rglob("*.html")):
        text = html.read_text()
        for attr in ("href", "src"):
            for value in re.findall(rf'{attr}="([^"]+)"', text):
                if value.startswith(SKIP):
                    continue
                checked += 1
                target = (html.parent / value.split("#")[0]).resolve()
                if not (target.exists() or (target / "index.html").exists()):
                    broken.append(f"{html.relative_to(ROOT)} -> {value}")

    print(f"checked {checked} internal links across "
          f"{len(list(ROOT.rglob('*.html')))} pages")
    if broken:
        print("BROKEN LINKS:")
        for b in broken:
            print("  " + b)
        return 1
    print("all internal links resolve")
    return 0


if __name__ == "__main__":
    sys.exit(main())
