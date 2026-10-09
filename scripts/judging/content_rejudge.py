#!/usr/bin/env python3
"""Full-text judging of the paper list: shards in, review, apply.

The judging itself is done by subagents that follow screening/prompts/content_rejudge.txt (one agent per shard,
INPUT = a shard .tsv, OUTPUT = <out_dir>/<shard>.txt, one line per paper:
key|arxiv|decision_model|model_status|main_contribution|connection|verdict|seat|role|evidence|reason).
The 2026-10-09 run in data/judging_runs/content_rejudge/ used the earlier three-layer fields (layer|subtype) in those
two columns; its results were mapped to seats by hand (data/core/paper_list.csv), so it is a record, never re-applied.

  shards  <source.csv> <text_dir> <shard_dir> [size]
      source: data/core/paper_list.csv, data/core/extended_2026.csv, extended_2022_2025.csv or any CSV with
      arxiv + title and key (or id). Writes <shard_dir>/kNN.tsv (key, arxiv, title, text path) and
      <shard_dir>/ids.txt for scripts/judging/fetch_fulltext.sh. Rows without an arXiv id are listed and skipped.
  review  <out_dir> [changes|verdict|all]
      Parse the outputs, check completeness, and compare with data/core/paper_list.csv.
  apply   <out_dir> <shard_dir> [--update]
      Write the verdicts into data/core/paper_list.csv. New keys are appended; keys already in the CSV are left
      alone unless --update is given. Then run scripts/build_paper_list.py.
"""
import csv, glob, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = os.path.join(ROOT, "data/core/paper_list.csv")
FIELDS = "key arxiv model status contrib conn verdict seat role evidence reason".split()
VERDICTS = ["保留", "资源", "剔除"]
SEATS = ["Designer", "Teacher", "Developer", "Controller", "Supervisor", "-"]
PHASE = {"Designer": "执行前", "Teacher": "执行前", "Developer": "执行前", "Controller": "运行时", "Supervisor": "运行时"}
ROLES = {"Designer": ["环境/重建", "奖励/任务"], "Teacher": ["示范/蒸馏"], "Developer": ["系统/代码", "本体/工具"],
         "Controller": ["编排", "写策略", "直接动作"], "Supervisor": ["监控/恢复"]}
ROLE_ORDER = ["环境/重建", "奖励/任务", "示范/蒸馏", "系统/代码", "本体/工具", "编排", "写策略", "直接动作", "监控/恢复", "评测", ""]
COLS = ["verdict", "phase", "seat", "role", "key", "year", "tier", "title", "arxiv", "decision_model", "model_status",
        "contribution", "connection", "reason", "evidence", "note", "arrows"]
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
            seat = (g["seat"].split() or ["-"])[0].strip("·")  # agents sometimes add words after the seat
            seat = seat[:1].upper() + seat[1:].lower() if seat != "-" else seat
            role = g["role"].strip()
            if g["verdict"] == "资源":  # the evaluated seat, role 评测
                role = "评测"
            elif g["verdict"] == "剔除":
                seat, role = "-", ""
            g["seat"], g["role"], g["phase"] = seat, role, PHASE.get(seat, "-")
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
        old = (c.get("verdict"), c.get("seat"), c.get("role"))
        new = (g["verdict"], g["seat"], g["role"])
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
        bad_label = g["verdict"] not in VERDICTS or g["seat"] not in SEATS or (
            g["verdict"] == "保留" and g["role"] not in ROLES.get(g["seat"], []))
        assert not bad_label, (k, g["verdict"], g["seat"], g["role"])
        vals = dict(verdict=g["verdict"], phase=g["phase"], seat=g["seat"], role=g["role"], decision_model=g["model"],
                    model_status=g["status"], contribution=g["contrib"], connection=g["conn"], reason=g["reason"],
                    evidence=g["evidence"])
        if k in cur:
            if update:
                r = cur[k]
                if (r["verdict"], r["seat"], r["role"]) != (g["verdict"], g["seat"], g["role"]):
                    vals["note"] = f"全文复核：原为 {r['verdict']} {r['seat']} {r['role']}".strip()
                r.update(vals)
                changed += 1
            continue
        a, t = meta.get(k, (g["arxiv"], ""))
        m = re.match(r"(\d{2})\d{2}\.\d{4,5}$", a)
        year = "20" + m.group(1) if m else ""
        rows.append(dict(vals, key=k, arxiv=a, title=t, year=year, tier="2026" if year == "2026" else "先驱",
                         arrows="", note=""))
        added += 1
    rows.sort(key=lambda r: (VERDICTS.index(r["verdict"]), SEATS.index(r["seat"]), ROLE_ORDER.index(r["role"]),
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
