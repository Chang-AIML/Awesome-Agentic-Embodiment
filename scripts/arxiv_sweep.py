#!/usr/bin/env python3
"""Sweep arXiv listings for agentic-embodiment papers in a date range (complements citation harvest).

Citation harvesting only finds papers that cite the seeds and that Semantic Scholar has indexed, so
recent papers are under-covered. This queries the arXiv API directly, pages through all hits and
writes one JSON object per paper, marking whether it is already in the candidates table.

Usage:
    python3 scripts/arxiv_sweep.py --from 20260101 --to 20261008 --out data/candidates/arxiv_2026.jsonl
    python3 scripts/arxiv_sweep.py --count-only ...
"""
import argparse, csv, json, os, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom",
      "o": "http://a9.com/-/spec/opensearch/1.1/"}
AGENT = ('(abs:agent OR abs:agents OR abs:agentic OR abs:LLM OR abs:LLMs OR abs:VLM OR abs:VLMs OR '
         'abs:"language model" OR abs:"language models" OR abs:"vision-language" OR abs:"foundation model" OR '
         'abs:"foundation models" OR abs:"coding agent" OR abs:harness OR abs:GPT OR abs:Gemini OR abs:Claude)')
QUERIES = {  # name -> query (date range appended)
    "ro": f"cat:cs.RO AND {AGENT}",
    "other": f'(cat:cs.AI OR cat:cs.CL OR cat:cs.LG OR cat:cs.CV OR cat:cs.MA OR cat:eess.SY) AND '
             f'(abs:robot OR abs:robots OR abs:robotic OR abs:humanoid OR abs:quadruped OR abs:manipulation OR '
             f'abs:embodied OR abs:drone OR abs:UAV) AND {AGENT} AND NOT cat:cs.RO',
}


def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


def fetch(query, start, n):
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"search_query": query, "start": start, "max_results": n, "sortBy": "submittedDate", "sortOrder": "ascending"})
    for attempt in range(8):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return ET.fromstring(r.read())
        except Exception as e:
            print("  retry", attempt, e, file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("arXiv API failed")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="d0", default="20260101")
    ap.add_argument("--to", dest="d1", default="20261008")
    ap.add_argument("--out", default=os.path.join(ROOT, "data/candidates/arxiv_2026.jsonl"))
    ap.add_argument("--count-only", action="store_true")
    ap.add_argument("--page", type=int, default=1000)
    args = ap.parse_args()
    known = {}
    for i, c in enumerate(csv.DictReader(open(os.path.join(ROOT, "data/candidates/candidates.csv")))):
        if c["arxiv"]:
            known[norm_arxiv(c["arxiv"])] = "c%05d" % i
    rng = f" AND submittedDate:[{args.d0}0000 TO {args.d1}2359]"
    seen, out = set(), []
    for name, q in QUERIES.items():
        root = fetch(q + rng, 0, 1)
        total = int(root.findtext("o:totalResults", "0", NS))
        print(f"{name}: {total} hits")
        if args.count_only:
            continue
        for start in range(0, total, args.page):
            root = fetch(q + rng, start, args.page)
            for e in root.findall("a:entry", NS):
                aid = norm_arxiv(e.findtext("a:id", "", NS).rsplit("/abs/", 1)[-1])
                if not aid or aid in seen:
                    continue
                seen.add(aid)
                out.append(dict(arxiv=aid, title=re.sub(r"\s+", " ", e.findtext("a:title", "", NS)).strip(),
                                published=e.findtext("a:published", "", NS)[:10], query=name,
                                categories=[c.get("term") for c in e.findall("a:category", NS)],
                                abstract=re.sub(r"\s+", " ", e.findtext("a:summary", "", NS)).strip(),
                                cid=known.get(aid, "")))
            print(f"  {name} {start + args.page}/{total} -> {len(out)} unique", file=sys.stderr)
            time.sleep(3)
    if args.count_only:
        return
    with open(args.out, "w") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    new = sum(1 for o in out if not o["cid"])
    print(f"{len(out)} papers ({new} not in candidates.csv) -> {args.out}")


if __name__ == "__main__":
    main()
