#!/usr/bin/env python3
"""Extended lists: every paper a strong-model pass judged `core` (closed loop) or `precursor` (open loop) that is
not in the curated table, one file for 2026 and one for the pioneer years 2022-2025.

Open-loop papers count since 2026-10-09: the agent only has to connect to the policy / code or to the environment
(user's agent-loop diagram, docs/paper_list.md); `loop` = none marks them. Papers the full-text judgement
excluded (verdict 剔除 in data/core/paper_list.csv) are left out.

The curated table (core_table.csv) is quota-driven (~100 rows). The awesome list also shows the rest
of the papers that meet the definition, so coverage of a year does not depend on the quota.
Only judgments from strong-model passes count (Sonnet stage 2, re-checks and verification passes,
and the gap-fill agents); cheap first-pass (Haiku) core verdicts that were never verified do not.
Year = arXiv v1 year from the id (YYMM.nnnnn) when there is one, else the Semantic Scholar date.

Usage: python3 scripts/build_extended.py   -> data/core/extended_2026.csv, data/core/extended_2022_2025.csv
"""
import csv, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STRONG = {"out", "recheck", "verify", "verify_s2", "recheck_r3b", "recheck_scope", "verify_pre", "verify_pf", "audit_out",
          "recheck_direct"}  # merge_fine_labels.py `pass` = shard directory name
COLS = ["id", "arxiv", "title", "date", "seat", "seat2", "sub", "carrier", "loop", "topo", "body", "rep", "conf",
        "theme", "reason", "pass"]


def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def year_of(arxiv, date):
    m = re.match(r"(\d{2})(\d{2})\.\d{4,5}$", norm_arxiv(arxiv))
    return "20" + m.group(1) if m else (date or "")[:4]


def theme_of(reason):
    m = re.match(r"\s*\[(real2sim2real|real2sim|sim2real)\]", reason or "")
    return m.group(1) if m else ""


def main():
    table = list(csv.DictReader(open(os.path.join(ROOT, "data/core/core_table.csv"))))
    taken = {norm_arxiv(r["arxiv"]) for r in table if r["arxiv"]} | {norm_title(r["title"]) for r in table}
    taken |= {r["id"] for r in table}
    lp = os.path.join(ROOT, "data/core/paper_list.csv")
    if os.path.exists(lp):  # excluded by the agent-loop judgement: keep them out of the extended lists too
        for r in csv.DictReader(open(lp, encoding="utf-8-sig")):
            if r["verdict"] == "剔除":
                taken |= {norm_arxiv(r["arxiv"]), norm_title(r["title"])} - {""}
    rows = []
    for r in csv.DictReader(open(os.path.join(ROOT, "data/core/fine_labels.csv"))):
        if r["verdict"] in ("core", "precursor") and r["pass"] in STRONG:
            rows.append(dict(r, theme=theme_of(r["reason"])))
    for name in ("gap_candidates.jsonl", "gap2_candidates.jsonl", "gap3_candidates.jsonl"):
        p = os.path.join(ROOT, "data/core", name)
        if os.path.exists(p):
            for o in map(json.loads, open(p)):
                if o.get("verdict") in ("core", "precursor"):
                    rows.append(dict(o, id="gap:" + norm_arxiv(o["arxiv"]), theme=(o.get("theme") or "").strip("-"),
                                     loop=o.get("loop") or ("none" if o["verdict"] == "precursor" else ""),
                                     **{"pass": name.split("_")[0]}))
    from collections import Counter
    for name, years in (("extended_2026.csv", {"2026"}), ("extended_2022_2025.csv", {"2022", "2023", "2024", "2025"})):
        out, seen = [], set()
        for r in rows:
            a, t = norm_arxiv(r.get("arxiv")), norm_title(r.get("title"))
            if year_of(a, r.get("date")) not in years or r["id"] in taken or (a and a in taken) or t in taken:
                continue
            k = a or t
            if k in seen:
                continue
            seen.add(k)
            out.append({c: r.get(c, "") for c in COLS} | {"arxiv": a})
        out.sort(key=lambda r: (r["seat"], r["sub"], r["date"], r["title"]))
        with open(os.path.join(ROOT, "data/core", name), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS)
            w.writeheader()
            w.writerows(out)
        print(f"{name}: {len(out)} rows;", dict(Counter(r["seat"] for r in out)),
              "open loop", sum(r["loop"] == "none" for r in out))


if __name__ == "__main__":
    main()
