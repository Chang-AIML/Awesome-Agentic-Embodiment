#!/usr/bin/env python3
"""Round-3 coverage completion: the two candidate sets that earlier passes never reached.

1. data/core/pool_pre2026.jsonl: harvest candidates that coarse screening kept (relevant / maybe) but that no
   fine-judging pool covered (pool, pool_bulk, pool_s2); mostly 2022-2025 papers below the earlier citation bar.
2. Candidates that were never coarse-screened (the first coarse pass only took candidates with an embodied
   keyword). Those from 2022 on (title only when there is no abstract) were coarse-screened by Haiku against
   screening/criteria_coarse.md, one line per paper `id|label|type|role|reason`; this script writes the shards
   for that pass and imports its output:
     data/screening/coarse_labels_completion.csv   same columns as coarse_labels.csv
     data/core/pool_prefilter.jsonl                 relevant + maybe, the pool for fine judging

Usage:
  python3 scripts/build_completion_pools.py pre2026
  python3 scripts/build_completion_pools.py prefilter-shards <dir>   # TSV shards (id, title, abstract) to screen
  python3 scripts/build_completion_pools.py prefilter <dir>          # import the coarse pass output (*.txt)
"""
import csv, glob, json, os, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = lambda *x: os.path.join(ROOT, *x)
clean = lambda s: " ".join((s or "").split())


def candidates():
    return list(csv.DictReader(open(p("data/candidates/candidates.csv"))))  # id c00042 = row 42


def coarse_labels():
    return {r["cid"]: r for r in csv.DictReader(open(p("data/screening/coarse_labels.csv")))}


def pool_row(cid, c, label, role, source):
    return dict(id=cid, title=c["title"], date=c["date"] or c["year"], citations=int(c["citations"] or 0), velocity="",
                arxiv=c["arxiv"], source=source, coarse=f"{label}/{role}",
                abstract=clean(c["abstract"])[:1100] or "(no abstract)")  # same format as pool_bulk.jsonl


def write_jsonl(path, rows):
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def pre2026():
    cand, lab = candidates(), coarse_labels()
    judged = {json.loads(l)["id"] for n in ("pool.jsonl", "pool_bulk.jsonl", "pool_s2.jsonl")
              for l in open(p("data/core", n))}
    rows = [pool_row(cid, cand[int(cid[1:])], r["label"], r["role"], "pre2026") for cid, r in sorted(lab.items())
            if r["label"] in ("relevant", "maybe") and cid not in judged]
    write_jsonl(p("data/core/pool_pre2026.jsonl"), rows)
    print(f"pool_pre2026.jsonl: {len(rows)}", Counter(r["date"][:4] for r in rows))


def never_screened():
    cand, lab = candidates(), coarse_labels()
    return [(f"c{i:05d}", c) for i, c in enumerate(cand)
            if f"c{i:05d}" not in lab and c["year"][:4] >= "2022"]


def prefilter_shards(out_dir, n=15):
    rows = never_screened()
    os.makedirs(out_dir, exist_ok=True)
    size = -(-len(rows) // n)
    for k in range(n):
        with open(os.path.join(out_dir, f"k{k:02d}.tsv"), "w") as f:
            for cid, c in rows[k * size:(k + 1) * size]:
                f.write(f"{cid}\t{clean(c['title'])}\t{clean(c['abstract'])}\n")
    print(f"{len(rows)} never-screened candidates -> {n} shards in {out_dir}")


def prefilter(in_dir):
    todo = dict(never_screened())
    got, bad = {}, []
    for path in sorted(glob.glob(os.path.join(in_dir, "*.txt"))):
        for line in open(path):
            x = [s.strip() for s in line.rstrip("\n").split("|")]
            if len(x) < 5 or x[0] not in todo or x[1].lower() not in ("relevant", "maybe", "irrelevant"):
                if line.strip():
                    bad.append(line.strip()[:80])
                continue
            got[x[0]] = dict(label=x[1].lower(), type=x[2], role=x[3], reason="/".join(x[4:]))
    cols = list(next(csv.DictReader(open(p("data/screening/coarse_labels.csv")))).keys())
    with open(p("data/screening/coarse_labels_completion.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for cid, v in sorted(got.items()):
            c = todo[cid]
            w.writerow(dict(cid=cid, title=c["title"], year=c["year"], arxiv=c["arxiv"], doi=c["doi"],
                            citations=c["citations"], n_core=c["n_core"], n_seeds=c["n_seeds"], **v))
    rows = [pool_row(cid, todo[cid], v["label"], v["role"], "prefilter") for cid, v in sorted(got.items())
            if v["label"] in ("relevant", "maybe")]
    write_jsonl(p("data/core/pool_prefilter.jsonl"), rows)
    print(f"coarse labels {len(got)} / {len(todo)}", Counter(v["label"] for v in got.values()),
          f"-> pool_prefilter.jsonl {len(rows)}; malformed {len(bad)}; missing {len(set(todo) - set(got))}")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "pre2026":
        pre2026()
    elif mode == "prefilter-shards":
        prefilter_shards(sys.argv[2])
    elif mode == "prefilter":
        prefilter(sys.argv[2])
    else:
        sys.exit(__doc__)
