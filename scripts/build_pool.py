#!/usr/bin/env python3
"""Build the stage-2 judging pool: shortlist + rare-seat supplement + definition test set.

The shortlist (build_shortlist.py) ranks by influence, so it misses moderately cited papers in the
small seats (e.g. Code-as-Monitor, 83 citations, Dec 2024). This adds:
  * coarse-relevant methods not in the shortlist, with a lower bar for rare coarse roles
    (monitor / teacher / developer / self-evolving / multi-agent) than for common ones;
  * every non-OUT paper of the definition test set (data/definition/testset_papers.json), using the
    candidates row when the arXiv id matches, else the test-set summary as abstract.

Usage: python3 scripts/build_pool.py [--today 2026-10-07]
Output: data/core/pool.jsonl
"""
import argparse, csv, datetime, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RARE = {"monitor", "teacher", "developer", "self-evolving", "multi-agent"}
BAR = {True: (20, 0.8), False: (60, 2.5)}  # rare?: (min citations, min 2025+ citations/month)


def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


def months_since(d, today):
    try:
        return max((today - datetime.date.fromisoformat(d[:10])).days / 30.4, 3)
    except ValueError:
        return 60


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default="2026-10-07")
    args = ap.parse_args()
    today = datetime.date.fromisoformat(args.today)
    lab = {r["cid"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data/screening/coarse_labels.csv")))}
    cand = list(csv.DictReader(open(os.path.join(ROOT, "data/candidates/candidates.csv"))))
    by_arxiv = {norm_arxiv(c["arxiv"]): i for i, c in enumerate(cand) if c["arxiv"]}
    pool = {o["id"]: dict(o) for o in map(json.loads, open(os.path.join(ROOT, "data/core/shortlist.jsonl")))}

    def cand_entry(i, source):
        c, cid = cand[i], "c%05d" % i
        d = (c["date"] or (f"{c['year']}-07-01" if c["year"] else ""))[:10]
        cit = int(c["citations"] or 0)
        r = lab.get(cid)
        ab = re.sub(r"\s+", " ", c["abstract"] or "")[:1100] or "(no abstract)"
        return dict(id=cid, title=c["title"], date=d, citations=cit, velocity=round(cit / months_since(d, today), 1),
                    arxiv=c["arxiv"], source=source, coarse=(r["label"] + "/" + r["role"]) if r else "unscreened",
                    abstract=ab)

    n_sup = 0
    for cid, r in lab.items():
        if cid in pool or r["label"] != "relevant" or r["type"] != "method":
            continue
        e = cand_entry(int(cid[1:]), "supplement")
        min_cit, min_vel = BAR[r["role"] in RARE]
        if e["citations"] >= min_cit or (e["date"] >= "2025-01-01" and e["velocity"] >= min_vel):
            pool[cid] = e
            n_sup += 1

    seed_by_arxiv = {norm_arxiv(o["arxiv"]): k for k, o in pool.items() if k.startswith("seed:")}
    n_ts = 0
    for k, t in enumerate(json.load(open(os.path.join(ROOT, "data/definition/testset_papers.json")))):
        if t.get("in_scope") == "out":
            continue
        a = norm_arxiv(t.get("arxiv_id"))
        if a in seed_by_arxiv:
            pool[seed_by_arxiv[a]]["source"] += ";testset"
            continue
        if a in by_arxiv:
            cid = "c%05d" % by_arxiv[a]
            if cid in pool:
                pool[cid]["source"] += ";testset"
            else:
                pool[cid] = cand_entry(by_arxiv[a], "testset")
                n_ts += 1
            continue
        tid = "t%03d" % k
        pool[tid] = dict(id=tid, title=t["title"], date=str(t.get("year") or ""), citations="", velocity="",
                         arxiv=t.get("arxiv_id") or "", source="testset", coarse="unscreened",
                         abstract=("(test-set summary) " + " ".join(
                             filter(None, [t.get("summary"), t.get("agent_component"), t.get("embodied_component")])))[:1100])
        n_ts += 1

    out = sorted(pool.values(), key=lambda o: o["id"])
    with open(os.path.join(ROOT, "data/core/pool.jsonl"), "w") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    print(f"shortlist {len(pool) - n_sup - n_ts}, supplement {n_sup}, test-set additions {n_ts} -> pool {len(out)}")


if __name__ == "__main__":
    main()
