#!/usr/bin/env python3
"""Sweep Semantic Scholar for robot + agent papers in one year (complements the citation harvest).

Citation harvesting only finds papers that cite the 14 seeds. This pages through S2's bulk search
(robot terms AND agent terms, Computer Science / Engineering), keeps hits whose title or abstract
really mentions both, and marks which are already in data/candidates/candidates.csv.
(The arXiv API is the other option, see arxiv_sweep.py, but it rate-limits shared IPs hard.)

Usage: python3 scripts/s2_sweep.py --year 2026 [--out data/candidates/s2_sweep_2026.jsonl]
Set SEMANTIC_SCHOLAR_API_KEY to use a key; keyless requests retry on 429.
"""
import argparse, csv, json, os, re, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUERY = ('(robot | robots | robotic | humanoid | quadruped | legged | manipulation | manipulator | embodied | '
         'drone | UAV | "mobile manipulation") + (agent | agents | agentic | LLM | LLMs | VLM | VLMs | '
         '"language model" | "language models" | "vision-language" | "foundation model" | "foundation models" | '
         '"coding agent" | harness)')
ROBOT = re.compile(r"robot|humanoid|quadruped|legged|manipulat|embodied|drone|\buav|mobile base|gripper|"
                   r"end-effector|locomotion|navigation", re.I)
AGENT = re.compile(r"\bagent|agentic|\bllms?\b|\bvlms?\b|language model|vision-language|foundation model|"
                   r"coding agent|harness|\bgpt|gemini|claude", re.I)


def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def get(url, headers):
    delay = 2.0
    for attempt in range(14):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=90) as r:
                return json.loads(r.read())
        except Exception as e:
            print("  retry", attempt, e, file=sys.stderr)
            time.sleep(delay)
            delay = min(delay * 2, 40)
    raise RuntimeError("S2 bulk search failed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", default="2026")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_path = args.out or os.path.join(ROOT, f"data/candidates/s2_sweep_{args.year}.jsonl")
    headers = {"x-api-key": os.environ["SEMANTIC_SCHOLAR_API_KEY"]} if os.environ.get("SEMANTIC_SCHOLAR_API_KEY") else {}
    known_a, known_t = {}, {}
    for i, c in enumerate(csv.DictReader(open(os.path.join(ROOT, "data/candidates/candidates.csv")))):
        cid = "c%05d" % i
        if c["arxiv"]:
            known_a[norm_arxiv(c["arxiv"])] = cid
        known_t[norm_title(c["title"])] = cid
    params = {"query": QUERY, "year": args.year, "fieldsOfStudy": "Computer Science,Engineering",
              "fields": "title,abstract,externalIds,publicationDate,citationCount,venue"}
    token, rows, total = None, [], None
    while True:
        p = dict(params, **({"token": token} if token else {}))
        d = get("https://api.semanticscholar.org/graph/v1/paper/search/bulk?" + urllib.parse.urlencode(p), headers)
        total = d.get("total", total)
        for x in d.get("data", []):
            text = f"{x.get('title') or ''} {x.get('abstract') or ''}"
            if not (ROBOT.search(text) and AGENT.search(text)):
                continue
            ids = x.get("externalIds") or {}
            a = norm_arxiv(ids.get("ArXiv"))
            rows.append(dict(s2id=x.get("paperId"), arxiv=a, doi=ids.get("DOI") or "", title=x.get("title") or "",
                             abstract=re.sub(r"\s+", " ", x.get("abstract") or ""), date=x.get("publicationDate") or "",
                             citations=x.get("citationCount") or 0, venue=x.get("venue") or "",
                             cid=known_a.get(a) or known_t.get(norm_title(x.get("title"))) or ""))
        print(f"  fetched {len(rows)} kept of {total}", file=sys.stderr)
        token = d.get("token")
        if not token:
            break
        time.sleep(1.5)
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    new = sum(1 for r in rows if not r["cid"])
    print(f"S2 total {total}; kept {len(rows)} with robot+agent terms; {new} not in candidates.csv -> {out_path}")


if __name__ == "__main__":
    main()
