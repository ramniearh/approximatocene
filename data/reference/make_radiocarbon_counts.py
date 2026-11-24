"""One-off script: calibrate the p3k14c radiocarbon dates with IntCal20 and
count them per 500 calendar years. Plain Python, no extra packages.

Usage:
    python make_radiocarbon_counts.py p3k14c_scrubbed_fuzzed.csv intcal20.14c

Inputs (not kept in the repo; see docs/notes.md for where they came from):
    p3k14c_scrubbed_fuzzed.csv  Bird et al. 2022, version 2022.01 (Zenodo 5597795)
    intcal20.14c                Reimer et al. 2020, from intcal.org/curves/intcal20.14c

Writes, next to this script:
    intcal20.csv                 the curve as published, with a source column
    radiocarbon_counts_p3k14c.csv  calibrated dates per 500 years, by continent

How a date is calibrated (the standard method, simplified):
    For each calendar year on a 5-year grid from 0 to 55,000 cal BP, the
    chance of the measured radiocarbon age given the curve at that year is
    a normal density with variance (lab error^2 + curve error^2). These are
    scaled to sum to 1 over the curve, so each date counts once in total and
    is shared across the 500-year bins its calibrated range covers.
    IntCal20 is used for every date, including southern-hemisphere and
    marine samples (shells), which strictly need other curves.
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).parent
STEP = 5          # calendar grid, years
BIN = 500         # bin width, years
CAL_MAX = 55000   # IntCal20 ends here (cal BP)
P3K = ("p3k14c (Bird et al. 2022, Scientific Data 9:27, doi:10.1038/s41597-022-01118-7), "
       "version 2022.01 from Zenodo 5597795, read 2026-11-24; calibrated here with IntCal20")
ICAL = ("IntCal20 (Reimer et al. 2020, Radiocarbon 62, doi:10.1017/RDC.2020.41), "
        "intcal.org/curves/intcal20.14c, read 2026-11-24")


def read_curve(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        rows.append([float(x) for x in line.split(",")])
    rows.sort()
    return rows  # cal BP, 14C age, sigma, Delta14C, sigma


def grid_from(curve):
    """Interpolate curve mean and error onto a regular calendar grid."""
    mu, sd, j = [], [], 0
    for i in range(CAL_MAX // STEP + 1):
        t = i * STEP
        while curve[j + 1][0] < t:
            j += 1
        a, b = curve[j], curve[j + 1]
        f = (t - a[0]) / (b[0] - a[0])
        mu.append(a[1] + f * (b[1] - a[1]))
        sd.append(a[2] + f * (b[2] - a[2]))
    return mu, sd


def main(p3k_path, curve_path):
    curve = read_curve(curve_path)
    with open(HERE / "intcal20.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["cal_bp", "c14_age", "c14_sigma", "delta14c", "delta14c_sigma", "source"])
        for r in curve:
            w.writerow([int(r[0]), int(r[1]), int(r[2]), r[3], r[4], ICAL])

    mu, sd = grid_from(curve)
    n = len(mu)
    c14_min, c14_max = min(mu), max(mu)
    # index: 14C age bucket (50 yr) -> grid points whose curve value falls in it
    buckets = {}
    for i, m in enumerate(mu):
        buckets.setdefault(int(m // 50), []).append(i)

    nbins = CAL_MAX // BIN
    conts = ["Africa", "Asia", "Australia", "Central America", "Europe",
             "North America", "South America"]
    total = [0.0] * nbins
    by = {c: [0.0] * nbins for c in conts + ["other"]}
    skipped = {"no age or error": 0, "younger than the curve (modern)": 0,
               "older than the curve": 0}
    used = 0

    with open(p3k_path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            try:
                age, err = float(row["Age"]), float(row["Error"])
            except (TypeError, ValueError):
                skipped["no age or error"] += 1
                continue
            if err <= 0:
                skipped["no age or error"] += 1
                continue
            if age < c14_min:
                skipped["younger than the curve (modern)"] += 1
                continue
            if age > c14_max:
                skipped["older than the curve"] += 1
                continue
            # candidate grid points: curve within 6 combined sigmas (curve error up to ~1,100)
            reach = 6 * math.sqrt(err * err + 1100 * 1100) if age > 30000 else 6 * math.sqrt(err * err + 300 * 300)
            idx = []
            for b in range(int((age - reach) // 50), int((age + reach) // 50) + 1):
                idx.extend(buckets.get(b, ()))
            ps, tot = [], 0.0
            for i in idx:
                v = err * err + sd[i] * sd[i]
                d = age - mu[i]
                p = math.exp(-d * d / (2 * v)) / math.sqrt(v)
                if p > 0:
                    ps.append((i, p))
                    tot += p
            if tot == 0:
                skipped["older than the curve"] += 1
                continue
            used += 1
            c = row.get("Continent") or ""
            tgt = by[c] if c in by else by["other"]
            for i, p in ps:
                k = min(i * STEP // BIN, nbins - 1)
                total[k] += p / tot
                tgt[k] += p / tot

    with open(HERE / "radiocarbon_counts_p3k14c.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["young_cal_bp", "old_cal_bp", "dates"] + [c.lower().replace(" ", "_") for c in conts] + ["other", "source"])
        for k in range(nbins):
            w.writerow([k * BIN, (k + 1) * BIN, round(total[k], 1)]
                       + [round(by[c][k], 1) for c in conts + ["other"]] + [P3K])

    print(f"calibrated {used} dates; skipped: {skipped}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
