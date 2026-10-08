#!/usr/bin/env python3
"""Merge stage-2 (fine) judgments from shard outputs into data/core/fine_labels.csv.

Each shard output line: id|verdict|seat|seat2|carrier|sub|interface|topo|closure|body|rep|conf|reason
Re-judging runs add a loop field before the reason (14 fields):
    id|verdict|seat|seat2|carrier|sub|interface|topo|closure|body|rep|conf|loop|reason
where loop is re-decide / authored / none (criteria_fine.md step A.3). Rows without it get
re-decide for core and none for precursor (the strict first pass only admitted re-decision).
Validates enums and completeness against data/core/pool.jsonl, and joins pool metadata plus the
definition test-set placement (matched by arXiv id) for comparison.

Usage: python3 scripts/merge_fine_labels.py <dir> [<dir> ...]   (later dirs override earlier ones)
"""
import csv, glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIELDS = ["id", "verdict", "seat", "seat2", "carrier", "sub", "interface", "topo", "closure", "body", "rep", "conf",
          "reason"]
ENUM = dict(verdict={"core", "precursor", "boundary", "resource", "out"},
            seat={"Controller", "Supervisor", "Teacher", "Designer", "Developer", "-"},
            carrier={"G", "C", "H", "I", "-"},
            sub={"orchestrator", "direct", "lifelong", "trained", "-"},
            rep={"1", "2", "3", "4", "5", "-"},
            conf={"high", "med", "low"},
            loop={"re-decide", "authored", "none", "-"})
LOOPS = ENUM["loop"]


def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


def main():
    pool = {o["id"]: o for o in map(json.loads, open(os.path.join(ROOT, "data/core/pool.jsonl")))}
    ts = {norm_arxiv(r["arxiv_id"]): r for r in
          csv.DictReader(open(os.path.join(ROOT, "docs/definition_testset_placements.csv")))}
    got, bad = {}, []
    paths = [p for d in sys.argv[1:] for p in sorted(glob.glob(os.path.join(d, "*.txt")))]
    for path in paths:
        for line in open(path):
            parts = [p.strip() for p in line.rstrip("\n").split("|")]
            if len(parts) < 13 or parts[0] not in pool:
                if line.strip():
                    bad.append((os.path.basename(path), line.strip()[:80]))
                continue
            loop = None
            if len(parts) >= 14 and parts[12] in LOOPS:
                loop, parts = parts[12], parts[:12] + parts[13:]
            row = dict(zip(FIELDS, parts[:12] + ["|".join(parts[12:])]))
            row["loop"] = loop or {"core": "re-decide", "precursor": "none"}.get(row["verdict"].lower(), "-")
            row["pass"] = os.path.basename(os.path.dirname(path))  # which run produced this judgment
            row["verdict"] = row["verdict"].lower()
            row["seat"] = row["seat"].capitalize() if row["seat"] != "-" else "-"
            row["conf"] = row["conf"].lower().replace("medium", "med")
            errs = [k for k, ok in ENUM.items() if row[k] not in ok]
            if errs:
                bad.append((os.path.basename(path), f"{row['id']} bad {errs}: " + "|".join(row[k] for k in errs)))
            got[row["id"]] = row  # last judgment wins (re-runs append)
    missing = sorted(set(pool) - set(got))
    out = []
    for i, row in sorted(got.items()):
        p = pool[i]
        t = ts.get(norm_arxiv(p["arxiv"]), {})
        out.append(dict(row, title=p["title"], date=p["date"], citations=p["citations"], arxiv=p["arxiv"],
                        source=p["source"], coarse=p["coarse"], testset_tier=t.get("in_scope", ""),
                        testset_primary=t.get("primary", "")))
    path = os.path.join(ROOT, "data/core/fine_labels.csv")
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    print(f"judged {len(got)} / pool {len(pool)}; missing {len(missing)}; malformed {len(bad)} -> {path}")
    for b in bad[:30]:
        print("  bad:", *b)
    if missing:
        print("  missing:", " ".join(missing[:60]))


if __name__ == "__main__":
    main()
