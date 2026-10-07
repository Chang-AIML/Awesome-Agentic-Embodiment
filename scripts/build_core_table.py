#!/usr/bin/env python3
"""Join the hand-curated selection with stage-2 labels into the core table.

Inputs:
  data/core/core_selection.csv   curated rows: id, key, tier, seat, sub, carrier, why[, arxiv]
                                 (seat/sub/carrier here override the stage-2 labels)
  data/core/fine_labels.csv      stage-2 labels for pool ids (c*/t*/seed:*)
  data/core/gap_candidates.jsonl gap-fill papers, referenced as id `gap:<arxiv>`
Output:
  data/core/core_table.csv

Usage: python3 scripts/build_core_table.py
"""
import csv, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = ["key", "tier", "seat", "seat2", "sub", "carrier", "interface", "topo", "closure", "body", "title", "arxiv",
        "date", "citations", "rep", "id", "source", "why"]


def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


SECTION_ZH = [("core", "Controller", "orchestrator", "Controller · 编排型"), ("core", "Controller", "direct", "Controller · 直接驱动型"),
              ("core", "Controller", "lifelong", "Controller · lifelong / memory 型"),
              ("core", "Controller", "trained", "Controller · 训练过的 carrier"), ("core", "Supervisor", None, "Supervisor"),
              ("core", "Teacher", None, "Teacher"), ("core", "Designer", None, "Designer"), ("core", "Developer", None, "Developer"),
              ("precursor", None, None, "前驱（precursor）"), ("resource", None, None, "Benchmark 与资源")]


def write_review(rows):
    """Chinese review sheet: every selected paper with its selection reason, for the user to check."""
    out = ["# 核心表审阅清单", "", "由 `scripts/build_core_table.py` 从 `data/core/core_selection.csv` 生成。"
           "要增删或改判，改 selection 文件后重新运行脚本。", ""]
    for tier, seat, sub, title in SECTION_ZH:
        xs = [r for r in rows if r["tier"] == tier and (seat is None or r["seat"] == seat) and (sub is None or r["sub"] == sub)]
        xs.sort(key=lambda r: (r["date"] or "9999", r["key"]))
        out += [f"## {title}（{len(xs)}）", "", "| 短名 | 年份 | Carrier | 来源 | 入选理由 |", "|---|---|---|---|---|"]
        for r in xs:
            src = "补漏" if r["id"].startswith("gap:") else ("种子" if r["id"].startswith("seed:") else "判定池")
            out.append(f"| [{r['key']}](https://arxiv.org/abs/{r['arxiv']}) | {(r['date'] or '')[:4]} | {r['carrier']} | {src} | {r['why']} |")
        out.append("")
    open(os.path.join(ROOT, "docs/core_review.md"), "w").write("\n".join(out))


def main():
    fine = {r["id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data/core/fine_labels.csv")))}
    gp = os.path.join(ROOT, "data/core/gap_candidates.jsonl")
    gap = {}
    if os.path.exists(gp):
        for o in map(json.loads, open(gp)):
            gap["gap:" + norm_arxiv(o["arxiv"])] = dict(o, id="gap:" + norm_arxiv(o["arxiv"]), source="gap",
                                                       citations="")
    mp = os.path.join(ROOT, "data/core/core_meta.json")  # from fetch_metadata.py; fills v1 date + citations
    meta = json.load(open(mp)) if os.path.exists(mp) else {}
    out, errs, seen = [], [], set()
    for s in csv.DictReader(open(os.path.join(ROOT, "data/core/core_selection.csv"))):
        base = fine.get(s["id"]) or gap.get(s["id"])
        if base is None:
            errs.append(f"unknown id {s['id']} ({s['key']})")
            continue
        row = {c: base.get(c, "") for c in COLS}
        for c in ("key", "tier", "why"):
            row[c] = s[c]
        for c in ("seat", "sub", "carrier"):
            if s.get(c):
                row[c] = s[c]
        if s.get("arxiv"):
            row["arxiv"] = s["arxiv"]
        row["arxiv"] = norm_arxiv(row["arxiv"])
        row["id"] = s["id"]
        m = meta.get(row["arxiv"], {})
        row["date"] = m.get("published") or row["date"]
        row["citations"] = m.get("citations") if m.get("citations") is not None else row["citations"]
        if row["tier"] == "core" and base.get("verdict") not in ("core", None):
            row["why"] += f"（stage-2 判为 {base.get('verdict')}，人工改判 core）"
        key = row["arxiv"] or row["title"].lower()
        if key in seen:
            errs.append(f"duplicate {s['key']}")
        seen.add(key)
        out.append(row)
    with open(os.path.join(ROOT, "data/core/core_table.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(out)
    write_review(out)
    from collections import Counter
    c = Counter((r["tier"], r["seat"]) for r in out)
    print(f"core_table.csv: {len(out)} rows;", ", ".join(f"{t}/{s}={n}" for (t, s), n in sorted(c.items())))
    for e in errs:
        print("  !", e)
    if errs:
        sys.exit(1)


if __name__ == "__main__":
    main()
