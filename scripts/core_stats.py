#!/usr/bin/env python3
"""Seat-by-year statistics on the core table (re-check of the draft's timeline on the final set).

Counts core papers by arXiv v1 year, both by primary seat and all-seat (primary + secondary seats),
plus carrier mix and the effective number of seats (exp of Shannon entropy of the all-seat counts).
Precursors are reported separately and excluded from the core counts.

Usage: python3 scripts/core_stats.py   -> prints Markdown (redirect to docs/core_stats.md)
"""
import csv, json, math, os, re
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
norm_arxiv = lambda a: re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))
SEATS = ["Controller", "Supervisor", "Teacher", "Designer", "Developer"]


def seat_table(core, year):
    prim, alls = defaultdict(Counter), defaultdict(Counter)
    for r in core:
        y = year(r)
        prim[y][r["seat"]] += 1
        seats = {r["seat"]} | {s for s in re.split(r"[+,;/ ]+", r.get("seat2") or "") if s in SEATS}
        for s in seats:
            alls[y][s] += 1
    print("| Year | n | " + " | ".join(SEATS) + " | Controller share (all-seat) | effective seats |")
    print("|---|---|" + "---|" * (len(SEATS) + 2))
    for y in sorted(prim):
        n = sum(prim[y].values())
        tot = sum(alls[y].values())
        h = -sum(c / tot * math.log(c / tot) for c in alls[y].values() if c)
        cells = [f"{prim[y][s]} ({alls[y][s]})" if prim[y][s] or alls[y][s] else "·" for s in SEATS]
        print(f"| {y} | {n} | " + " | ".join(cells) + f" | {alls[y]['Controller'] / n:.0%} | {math.exp(h):.2f} |")
    print("\nCells: primary seat (all-seat count, i.e. papers with that seat as primary or secondary).\n")


def main():
    meta = json.load(open(os.path.join(ROOT, "data/core/core_meta.json")))
    year = lambda r: (meta.get(norm_arxiv(r["arxiv"]), {}).get("published") or r["date"] or "????")[:4]
    fine = [r for r in csv.DictReader(open(os.path.join(ROOT, "data/core/fine_labels.csv"))) if r["verdict"] == "core"]
    print(f"## A. All stage-2 core verdicts (n = {len(fine)}; pool is influence-sampled, 2026 over-represented)\n")
    seat_table(fine, year)
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/core/core_table.csv"))))
    core = [r for r in rows if r["tier"] == "core"]
    print(f"## B. Curated core table (n = {len(core)}; quota-driven, not trend evidence)\n")
    seat_table(core, year)
    car = Counter((r["seat"], r["carrier"].split("→")[0].strip()) for r in core)
    print("| Seat | " + " | ".join("GCHI") + " |\n|---|---|---|---|---|")
    for s in SEATS:
        print(f"| {s} | " + " | ".join(str(car[(s, k)] or "·") for k in "GCHI") + " |")
    pre = Counter(year(r) for r in rows if r["tier"] == "precursor")
    print("\nPrecursors by year: " + ", ".join(f"{y}: {n}" for y, n in sorted(pre.items())))


if __name__ == "__main__":
    main()
