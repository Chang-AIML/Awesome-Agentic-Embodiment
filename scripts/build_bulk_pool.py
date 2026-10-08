#!/usr/bin/env python3
"""Bulk judging pool: every coarse relevant/maybe 2026 candidate not yet judged, plus 2022-2025 ones
above a per-year citation bar (the first pool sampled by influence, which misses recent papers).

Usage: python3 scripts/build_bulk_pool.py   -> data/core/pool_bulk.jsonl
"""
import csv, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BAR = {"2022": 40, "2023": 40, "2024": 25, "2025": 12}  # min citations for pre-2026 years; 2026 takes all


def main():
    cand = list(csv.DictReader(open(os.path.join(ROOT, "data/candidates/candidates.csv"))))
    lab = {r["cid"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data/screening/coarse_labels.csv")))}
    pool = {json.loads(l)["id"] for l in open(os.path.join(ROOT, "data/core/pool.jsonl"))}
    out = []
    for i, c in enumerate(cand):
        cid = "c%05d" % i
        r = lab.get(cid)
        if cid in pool or not r or r["label"] not in ("relevant", "maybe"):
            continue
        y = (c["date"] or c["year"] or "")[:4]
        cit = int(c["citations"] or 0)
        if y != "2026" and not (y in BAR and cit >= BAR[y]):
            continue
        ab = re.sub(r"\s+", " ", c["abstract"] or "")[:1100] or "(no abstract)"
        out.append(dict(id=cid, title=c["title"], date=(c["date"] or y)[:10], citations=cit, velocity="",
                        arxiv=c["arxiv"], source="bulk2026" if y == "2026" else "bulk-pre2026",
                        coarse=r["label"] + "/" + r["role"], abstract=ab))
    with open(os.path.join(ROOT, "data/core/pool_bulk.jsonl"), "w") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(f"bulk pool {len(out)} -> data/core/pool_bulk.jsonl")


if __name__ == "__main__":
    main()
