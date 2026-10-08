"""Collect Haiku core/precursor/boundary rows from finished fine-judging outputs into Sonnet verify shards.
Usage: python3 scripts/judging/make_verify.py <shard_dir> <out_dir> <verify_dir> <start_index> <shard names...>"""
import os, sys
shard_dir, out_dir, vdir, start = sys.argv[1:5]
names = sys.argv[5:]
keep = []
for b in names:
    lines = {l.split("\t")[0]: l for l in open(os.path.join(shard_dir, b + ".tsv")) if l.strip()}
    for l in open(os.path.join(out_dir, b + ".txt")):
        p = [x.strip() for x in l.split("|")]
        if len(p) >= 14 and p[1].lower() in ("core", "precursor", "boundary") and p[0] in lines:
            keep.append(lines.pop(p[0]))
os.makedirs(vdir, exist_ok=True)
n = -(-len(keep) // 100)
size = -(-len(keep) // n)
for k in range(n):
    with open(os.path.join(vdir, f"k{int(start) + k:02d}.tsv"), "w") as f:
        f.writelines(keep[k * size:(k + 1) * size])
print(len(keep), "rows ->", n, "shards of", size)
