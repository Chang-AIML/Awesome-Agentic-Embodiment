"""Curation helper: list 2022-2025 strong-pass core / precursor papers not yet in the selection, by seat / sub, ranked by
representativeness and citations.  Usage: python3 scripts/judging/pioneer_candidates.py data/core/fine_labels.csv [min_rep] [top_n]"""
import csv, collections, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STRONG = {"out", "recheck", "verify", "verify_s2", "recheck_r3b", "recheck_scope", "verify_pre", "verify_pf", "audit_out",
          "recheck_direct"}
fl = list(csv.DictReader(open(sys.argv[1])))
min_rep = int(sys.argv[2]) if len(sys.argv) > 2 else 3
sel = {r["id"] for r in csv.DictReader(open(f"{ROOT}/data/core/core_selection.csv"))}
nt = lambda t: re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()[:40]
selt = {nt(r["title"]) for r in csv.DictReader(open(f"{ROOT}/data/core/core_table.csv"))}
selx = {r["arxiv"] for r in csv.DictReader(open(f"{ROOT}/data/core/core_selection.csv")) if r["arxiv"]}
def yr(r):
    m = re.match(r"(\d{2})\d{2}\.\d{4,5}$", r["arxiv"] or "")
    return "20" + m.group(1) if m else r["date"][:4]
c = [r for r in fl if r["pass"] in STRONG and r["verdict"] in ("core", "precursor") and yr(r) in ("2022", "2023", "2024", "2025")
     and r["id"] not in sel and r["arxiv"] not in selx and nt(r["title"]) not in selt]
print(len(c), collections.Counter((r["verdict"], r["seat"]) for r in c))
groups = collections.defaultdict(list)
for r in c:
    nav = bool(re.search(r"\bnav|VLN|navigation", r["body"] + " " + r["title"], re.I))
    k = ("VLN/nav" if nav and r["seat"] == "Controller" else r["seat"] + ("/" + r["sub"] if r["seat"] == "Controller" else ""))
    groups[k].append(r)
for k in sorted(groups):
    top = int(sys.argv[3]) if len(sys.argv) > 3 else 999
    xs = [r for r in groups[k] if (int(r["rep"]) if r["rep"].isdigit() else 0) >= min_rep]
    xs = sorted(xs, key=lambda r: -int(r["citations"] or 0))[:top]
    print(f"\n## {k} ({len(groups[k])})")
    for r in xs:
        if (int(r["rep"]) if r["rep"].isdigit() else 0) < min_rep:
            continue
        print(f"{r['id']} {yr(r)} rep{r['rep']} cit{r['citations']:>5} {r['verdict'][:4]} {r['loop'][:4]} {r['pass']:<13} {r['title'][:70]} | {r['body'][:20]}")
