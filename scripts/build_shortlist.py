#!/usr/bin/env python3
"""Build the core-candidate shortlist from coarse screening labels.

Union of: top-250 by citations, top-250 (2025+) by citation velocity
(citations per month since publication), and recent "frontier agentic"
papers whose titles match agentic keywords; plus all seed papers.

Usage: python3 scripts/build_shortlist.py [--today 2026-10-07]
Output: data/core/shortlist.jsonl
"""
import argparse, csv, datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KW = re.compile(r"harness|agentic|\bagents?\b|coding agent|self[- ]evolv|self[- ]improv|monitor|failure|distill|"
                r"reflect|memory|multi[- ]robot|multi[- ]agent|tool|code|program|planner|planning|reason|"
                r"chain[- ]of[- ]thought|skill librar|lifelong|reward design|ask for help|clarif", re.I)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default="2026-10-07")
    ap.add_argument("--top", type=int, default=250)
    args = ap.parse_args()
    today = datetime.date.fromisoformat(args.today)
    lab = {r["cid"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data/screening/coarse_labels.csv")))}
    cand = list(csv.DictReader(open(os.path.join(ROOT, "data/candidates/candidates.csv"))))
    seeds = json.load(open(os.path.join(ROOT, "data/seeds.json")))["seeds"]

    rows = []
    for cid, r in lab.items():
        if r["label"] == "irrelevant":
            continue
        c = cand[int(cid[1:])]
        d = c["date"] or (f"{c['year']}-07-01" if c["year"] else "")
        try:
            dt = datetime.date.fromisoformat(d[:10])
        except ValueError:
            dt = None
        months = max((today - dt).days / 30.4, 3) if dt else 60
        cit = int(c["citations"] or 0)
        rows.append(dict(cid=cid, c=c, r=r, date=d[:10], cit=cit, vel=cit / months))

    by_cit = sorted(rows, key=lambda x: -x["cit"])[:args.top]
    by_vel = sorted([x for x in rows if x["date"] >= "2025-01-01"], key=lambda x: -x["vel"])[:args.top]
    front = [x for x in rows if x["date"] >= "2025-01-01" and x["r"]["label"] == "relevant"
             and KW.search(x["c"]["title"]) and (x["vel"] >= 1.5 or x["cit"] >= 40)]
    sel = {}
    for src, xs in (("citations", by_cit), ("velocity", by_vel), ("frontier-agentic", front)):
        for x in xs:
            sel.setdefault(x["cid"], (x, []))[1].append(src)

    out = []
    for cid, (x, src) in sel.items():
        c = x["c"]
        ab = re.sub(r"\s+", " ", c["abstract"] or "")[:1100] or "(no abstract)"
        out.append(dict(id=cid, title=c["title"], date=x["date"], citations=x["cit"], velocity=round(x["vel"], 1),
                        arxiv=c["arxiv"], source=";".join(src), coarse=x["r"]["label"] + "/" + x["r"]["role"],
                        abstract=ab))
    for s in seeds:
        out.append(dict(id="seed:" + s["key"], title=s["title"], date="", citations="", velocity="", arxiv=s["arxiv"],
                        source="seed", coarse="seed", abstract="(seed paper; judge from title and your knowledge)"))
    out.sort(key=lambda o: o["id"])
    os.makedirs(os.path.join(ROOT, "data/core"), exist_ok=True)
    with open(os.path.join(ROOT, "data/core/shortlist.jsonl"), "w") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(f"citations {len(by_cit)}, velocity {len(by_vel)}, frontier {len(front)} -> shortlist {len(out)}")


if __name__ == "__main__":
    main()
