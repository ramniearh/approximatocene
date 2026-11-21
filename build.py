"""Rebuild index.html from src/page.html and data/atlas.json.

Usage:  python3 build.py

Stops with a plain message if a date in the data has no unit
(e.g. "11700" instead of "11700 b2k"), because a date without a unit
is ambiguous and the page would quietly misplace it.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
TEMPLATE = ROOT / "src" / "page.html"
DATA = ROOT / "data" / "atlas.json"
OUT = ROOT / "index.html"
MARK = "/*__ATLAS__*/"

UNIT = re.compile(r"^-?[\d.]+\s*(Ga|Ma|ka|b2k|BP|BCE|CE|yr)$", re.I)


def ok_time(v):
    return isinstance(v, str) and (v in ("now", "present") or bool(UNIT.match(v.strip())))


def check(node, where, problems):
    """Look at every t / t0 / t1 value (and est/lo/hi inside them)."""
    if isinstance(node, dict):
        for k, v in node.items():
            here = f"{where}.{k}"
            if k == "rows" and isinstance(v, list) and v and isinstance(v[0], list):
                # compact series: [age, value, ...] rows need one stated unit for the whole block
                if node.get("ageUnit") not in ("Ga", "Ma", "ka", "b2k", "BP", "BCE", "CE", "yr"):
                    problems.append(f"{where}.ageUnit = {node.get('ageUnit')!r} (rows need an age unit)")
            elif k in ("t", "t0", "t1"):
                if isinstance(v, dict):
                    for part in ("est", "lo", "hi"):
                        if part in v and not ok_time(v[part]):
                            problems.append(f"{here}.{part} = {v[part]!r}")
                elif not ok_time(v):
                    problems.append(f"{here} = {v!r}")
            else:
                check(v, here, problems)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            check(v, f"{where}[{i}]", problems)


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    problems = []
    check(data, "atlas", problems)
    if problems:
        print("Not built. These dates need a unit (Ga, Ma, ka, b2k, BP, BCE, CE, yr or 'now'):")
        for p in problems:
            print("  ", p)
        sys.exit(1)

    html = TEMPLATE.read_text(encoding="utf-8")
    if html.count(MARK) != 1:
        sys.exit(f"Not built. src/page.html must contain {MARK} exactly once.")
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    OUT.write_text(html.replace(MARK, blob), encoding="utf-8")
    print(f"Built index.html ({OUT.stat().st_size // 1024} KB).")


if __name__ == "__main__":
    main()
