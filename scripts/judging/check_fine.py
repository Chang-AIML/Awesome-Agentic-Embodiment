"""Dry-run check of fine-judging shard outputs: field count, enums, missing / duplicate ids, verdict mix.
Usage: python3 scripts/judging/check_fine.py <shard_dir> <out_dir>"""
import collections, glob, os, sys
shard_dir, out_dir = sys.argv[1:3]
ENUM = dict(verdict={"core", "precursor", "boundary", "resource", "out"},
            seat={"Controller", "Supervisor", "Teacher", "Designer", "Developer", "-"},
            carrier={"G", "C", "-"}, sub={"orchestrator", "direct", "lifelong", "-"},
            conf={"high", "med", "low", "medium"}, loop={"re-decide", "authored", "none", "-"})
IDX = dict(verdict=1, seat=2, carrier=4, sub=5, conf=11, loop=12)
tot = collections.Counter()
for sp in sorted(glob.glob(os.path.join(shard_dir, "*.tsv"))):
    b = os.path.basename(sp)[:-4]
    op = os.path.join(out_dir, b + ".txt")
    if not os.path.exists(op):
        continue
    ids = [l.split("\t")[0] for l in open(sp) if l.strip()]
    seen, bad, dup = collections.Counter(), [], 0
    for l in open(op):
        if not l.strip():
            continue
        p = [x.strip() for x in l.rstrip("\n").split("|")]
        if len(p) < 14:
            bad.append(f"short:{l[:60]}")
            continue
        seen[p[0]] += 1
        for k, i in IDX.items():
            v = p[i].lower() if k in ("verdict", "conf") else p[i]
            if k == "seat" and v != "-":
                v = v.capitalize()
            if v not in ENUM[k]:
                bad.append(f"{p[0]} {k}={p[i]}")
        if p[0] in set(ids):
            tot[p[1].lower()] += 1
    miss = [i for i in ids if i not in seen]
    extra = [i for i in seen if i not in set(ids)]
    dup = sum(1 for v in seen.values() if v > 1)
    flag = "" if not (miss or extra or dup or bad) else f"  miss={len(miss)} extra={len(extra)} dup={dup} bad={len(bad)} {bad[:3]} {miss[:5]}"
    print(b, len(ids), sum(seen.values()), flag)
print(dict(tot))
