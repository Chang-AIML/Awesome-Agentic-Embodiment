#!/usr/bin/env python3
"""Judging pool for the Semantic Scholar 2026 sweep (s2_sweep.py), the papers the citation harvest missed.

Ids are s<line index> into data/candidates/s2_sweep_2026.jsonl. Only papers not already in
candidates.csv whose title or abstract names a foundation model (FM below) were coarse-screened
(criteria_coarse.md); "multi-agent" control and MARL hits without one are dropped before that.

    python3 scripts/build_s2_pool.py --shards <dir> [--size 355]   write coarse shards <dir>/kNN.tsv
    python3 scripts/build_s2_pool.py --coarse <dir>                merge coarse outputs <dir>/*.txt
        -> data/candidates/s2_coarse_2026.csv and data/core/pool_s2.jsonl (relevant + maybe, plus any
           FM-matching paper without a coarse label, marked unscreened, so fine judging sees it)
"""
import argparse, csv, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWEEP = os.path.join(ROOT, "data/candidates/s2_sweep_2026.jsonl")
FM = re.compile(r"\bllms?\b|\bvlms?\b|\bvlas?\b|language model|vision-language|foundation model|coding agent|"
                r"harness|\bgpt|gemini|claude|agentic|large (?:multimodal |vision |reasoning )?models?", re.I)


def clean(s):
    return re.sub(r"\s+", " ", s or "").replace("\t", " ").strip()


def screened(rows):
    return [("s%05d" % i, r) for i, r in enumerate(rows)
            if not r["cid"] and FM.search(f"{r['title']} {r['abstract']}")]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shards")
    ap.add_argument("--size", type=int, default=355)
    ap.add_argument("--coarse")
    args = ap.parse_args()
    rows = [json.loads(l) for l in open(SWEEP)]
    if args.shards:
        todo = screened(rows)
        n = (len(todo) + args.size - 1) // args.size
        os.makedirs(args.shards, exist_ok=True)
        for k in range(n):  # interleaved so every shard spans the whole year
            with open(os.path.join(args.shards, "k%02d.tsv" % k), "w") as f:
                for sid, r in todo[k::n]:
                    f.write(f"{sid}\t{clean(r['title'])}\t{clean(r['abstract'])[:1100] or '(no abstract)'}\n")
        print(f"{len(todo)} papers -> {n} shards in {args.shards}")
    if args.coarse:
        lab = {}
        for path in sorted(glob.glob(os.path.join(args.coarse, "*.txt"))):
            for line in open(path):
                p = [x.strip() for x in line.rstrip("\n").split("|")]
                if len(p) >= 5 and re.fullmatch(r"s\d{5}", p[0]) and p[1] in ("relevant", "maybe", "irrelevant"):
                    lab[p[0]] = dict(label=p[1], type=p[2], role=p[3], reason="|".join(p[4:]))
        todo = dict(screened(rows))
        todo.update({sid: rows[int(sid[1:])] for sid in lab})  # the first run's shards also hold a few others
        with open(os.path.join(ROOT, "data/candidates/s2_coarse_2026.csv"), "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["id", "label", "type", "role", "reason", "arxiv", "date", "title"])
            for sid in sorted(lab):
                r = todo[sid]
                w.writerow([sid, lab[sid]["label"], lab[sid]["type"], lab[sid]["role"], lab[sid]["reason"],
                            r["arxiv"], r["date"], r["title"]])
        pool = []
        for sid, r in todo.items():
            l = lab.get(sid) or dict(label="unscreened", role="-")  # a few match FM but missed the first shards
            if l["label"] in ("relevant", "maybe", "unscreened"):
                pool.append(dict(id=sid, title=r["title"], date=r["date"][:10] or "2026", citations=r["citations"],
                                 velocity="", arxiv=r["arxiv"], source="s2sweep2026",
                                 coarse=l["label"] + "/" + l["role"], abstract=clean(r["abstract"])[:1100] or "(no abstract)"))
        with open(os.path.join(ROOT, "data/core/pool_s2.jsonl"), "w") as f:
            for o in pool:
                f.write(json.dumps(o, ensure_ascii=False) + "\n")
        missing = sorted(set(todo) - set(lab))
        print(f"coarse labels {len(lab)} / {len(todo)} screened (missing {len(missing)}); pool {len(pool)} -> data/core/pool_s2.jsonl")
        if missing:
            print("  missing:", " ".join(missing[:40]))


if __name__ == "__main__":
    main()
