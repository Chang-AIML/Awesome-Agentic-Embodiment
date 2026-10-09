#!/usr/bin/env python3
"""Full-text judging against the user's agent-loop framework: shards in, review, apply.

The judging itself is done by subagents that follow screening/prompts/content_rejudge.txt (one agent per shard,
INPUT = a shard .tsv, OUTPUT = <out_dir>/<shard>.txt, one line per paper:
key|arxiv|decision_model|model_status|main_contribution|connection|verdict|layer|subtype|evidence|reason).

  shards  <source.csv> <text_dir> <shard_dir> [size]
      source: data/core/layer_classification.csv, data/core/extended_2026.csv, extended_2022_2025.csv or any CSV with
      arxiv + title and key (or id). Writes <shard_dir>/kNN.tsv (key, arxiv, title, text path) and
      <shard_dir>/ids.txt for scripts/judging/fetch_fulltext.sh. Rows without an arXiv id are listed and skipped.
  review  <out_dir> [changes|verdict|all]
      Parse the outputs, check completeness, and compare with data/core/layer_classification.csv.
  apply   <out_dir> <shard_dir> [--update]
      Write the verdicts into data/core/layer_classification.csv. New keys are appended; keys already in the CSV are
      left alone unless --update is given (the core-table run of 2026-10-09 was applied with hand review, e.g.
      EmbodiedSmith was restored after the user's question, so do not re-apply data/judging_runs/content_rejudge/
      with --update). Then run scripts/build_layer_table.py.
"""
import csv, glob, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = os.path.join(ROOT, "data/core/layer_classification.csv")
FIELDS = "key arxiv model status contrib conn verdict layer subtype evidence reason".split()
VERDICTS = ["保留", "资源", "剔除"]
LAYERS = ["L1", "L2", "L3", "-"]
SUBS = ["环境/重建", "奖励/任务", "本体/工具", "系统/代码", "策略生产者", "编排者", "经验迁移", "运行时监控", "直接动作",
        "评测L1", "评测L2", "评测L3", ""]
COLS = ["verdict", "layer", "subtype", "key", "year", "tier", "title", "arxiv", "decision_model", "model_status",
        "contribution", "connection", "arrows", "reason", "evidence", "note", "old_seat"]
clean = lambda s: " ".join((s or "").split())


def shards(src, text_dir, shard_dir, size=10):
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    os.makedirs(shard_dir, exist_ok=True)
    keep, skipped = [], []
    for r in rows:
        a = re.sub(r"v\d+$", "", (r.get("arxiv") or "").strip())
        (keep if a else skipped).append((r.get("key") or r.get("id"), a, clean(r.get("title"))))
    for k in range(0, len(keep), size):
        with open(os.path.join(shard_dir, f"k{k // size:02d}.tsv"), "w") as f:
            for key, a, t in keep[k:k + size]:
                f.write(f"{key}\t{a}\t{t}\t{os.path.join(os.path.abspath(text_dir), a + '.txt')}\n")
    open(os.path.join(shard_dir, "ids.txt"), "w").write("\n".join(sorted({a for _, a, _ in keep})) + "\n")
    print(f"{len(keep)} papers -> {-(-len(keep) // size)} shards in {shard_dir}; no arXiv id, skipped: {len(skipped)}")
    for s in skipped:
        print("  skip", s[0], s[2][:80])


def parse(out_dir):
    got, bad = {}, []
    for p in sorted(glob.glob(os.path.join(out_dir, "*.txt"))):
        for line in open(p):
            x = [s.strip() for s in line.rstrip("\n").split("|")]
            if len(x) != 11:
                if line.strip():
                    bad.append((os.path.basename(p), line.strip()[:100]))
                continue
            g = dict(zip(FIELDS, x))
            layer, sub = (g["layer"].split() or ["-"])[0], g["subtype"].strip()  # agents sometimes write "L1 准备层"
            if g["verdict"] == "资源":  # evaluated layer in `layer`, 评测Lx in `subtype`
                ev = layer if layer.startswith("评测") else (sub if sub.startswith("评测") else "")
                layer, sub = ev.replace("评测", "") or "-", ev
            elif g["verdict"] == "剔除":
                layer, sub = "-", ""
            g["layer"], g["subtype"] = layer, sub
            got[g["key"]] = g
    return got, bad


def review(out_dir, mode="changes"):
    cur = {r["key"]: r for r in csv.DictReader(open(CSV, encoding="utf-8-sig"))}
    got, bad = parse(out_dir)
    print(f"parsed {len(got)}; malformed {len(bad)}; new keys {sum(k not in cur for k in got)}")
    for b in bad:
        print("  BAD", b)
    print(Counter(g["status"] for g in got.values()), Counter(g["contrib"] for g in got.values()),
          Counter(g["verdict"] for g in got.values()))
    for k, g in got.items():
        c = cur.get(k, {})
        old = (c.get("verdict"), c.get("layer"), c.get("subtype"))
        new = (g["verdict"], g["layer"], g["subtype"])
        if mode == "all" or (mode == "changes" and old != new) or (mode == "verdict" and old[0] != new[0]):
            print(f"\n## {k}  {' '.join(x or '-' for x in old)}  ->  {' '.join(new)}")
            print(f"   model: {g['model']} | {g['status']} | {g['contrib']} | {g['conn']}")
            print(f"   ev: {g['evidence']}\n   why: {g['reason']}")


def apply(out_dir, shard_dir, update=False):
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    cur = {r["key"]: r for r in rows}
    meta = {}
    for p in glob.glob(os.path.join(shard_dir, "k*.tsv")):
        for line in open(p):
            key, a, t = line.rstrip("\n").split("\t")[:3]
            meta[key] = (a, t)
    got, bad = parse(out_dir)
    assert not bad, f"{len(bad)} malformed lines; fix them first"
    added = changed = 0
    for k, g in got.items():
        bad_label = g["verdict"] not in VERDICTS or g["layer"] not in LAYERS or g["subtype"] not in SUBS
        assert not bad_label, (k, g["verdict"], g["layer"], g["subtype"])
        vals = dict(verdict=g["verdict"], layer=g["layer"], subtype=g["subtype"], decision_model=g["model"],
                    model_status=g["status"], contribution=g["contrib"], connection=g["conn"], reason=g["reason"],
                    evidence=g["evidence"])
        if k in cur:
            if update:
                r = cur[k]
                if (r["verdict"], r["layer"], r["subtype"]) != (g["verdict"], g["layer"], g["subtype"]):
                    vals["note"] = f"全文复核：原为 {r['verdict']} {r['layer']} {r['subtype']}".strip()
                r.update(vals)
                changed += 1
            continue
        a, t = meta.get(k, (g["arxiv"], ""))
        m = re.match(r"(\d{2})\d{2}\.\d{4,5}$", a)
        year = "20" + m.group(1) if m else ""
        rows.append(dict(vals, key=k, arxiv=a, title=t, year=year, tier="2026" if year == "2026" else "先驱",
                         arrows="", note="", old_seat=""))
        added += 1
    rows.sort(key=lambda r: (VERDICTS.index(r["verdict"]), LAYERS.index(r["layer"]), SUBS.index(r["subtype"]),
                             r["tier"] != "先驱", r["year"], r["key"].lower()))
    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"added {added}, updated {changed}; {len(rows)} rows:", Counter(r["verdict"] for r in rows))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["shards"] and len(a) >= 4:
        shards(a[1], a[2], a[3], int(a[4]) if len(a) > 4 else 10)
    elif a[:1] == ["review"] and len(a) >= 2:
        review(a[1], a[2] if len(a) > 2 else "changes")
    elif a[:1] == ["apply"] and len(a) >= 3:
        apply(a[1], a[2], "--update" in a)
    else:
        sys.exit(__doc__)
