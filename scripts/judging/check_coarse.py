"""Check coarse-screening shard outputs against their shards: completeness, labels, duplicates, label mix.
Usage: python3 scripts/judging/check_coarse.py <shard_dir> <out_dir>"""
import collections, glob, os, sys
shard_dir, out_dir = sys.argv[1:3]
tot = collections.Counter()
for sp in sorted(glob.glob(os.path.join(shard_dir, "*.tsv"))):
    b = os.path.basename(sp)[:-4]; op = os.path.join(out_dir, b + ".txt")
    if not os.path.exists(op): continue
    ids = [l.split("\t")[0] for l in open(sp) if l.strip()]; s = set(ids)
    seen, bad = collections.Counter(), []
    for l in open(op):
        if not l.strip(): continue
        p = [x.strip() for x in l.split("|")]
        if len(p) < 5 or p[1].lower() not in ("relevant", "maybe", "irrelevant"): bad.append(l[:60]); continue
        seen[p[0]] += 1
        if p[0] in s: tot[p[1].lower()] += 1
    miss = [i for i in ids if i not in seen]; extra = [i for i in seen if i not in s]; dup = sum(v > 1 for v in seen.values())
    print(b, len(ids), sum(seen.values()), "" if not (miss or extra or dup or bad) else f"miss={len(miss)} extra={len(extra)} dup={dup} bad={bad[:3]}")
print(dict(tot))
