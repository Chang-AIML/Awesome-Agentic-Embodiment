#!/usr/bin/env python3
"""Fetch metadata for core papers: arXiv (exact title, v1 date, authors, comment, links) and
Semantic Scholar (venue, citation count). Verifies that every arXiv id exists.

Usage: python3 scripts/fetch_metadata.py [--refresh] <csv> [<csv> ...]
       (reads the `arxiv` column; writes data/core/core_meta.json keyed by arXiv id; ids already
       verified there are kept unless --refresh, so re-runs only query new ids)
Set SEMANTIC_SCHOLAR_API_KEY to use a key; keyless requests retry on 429.
"""
import csv, json, os, re, sys, time, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harvest_citations import http_get_json  # noqa: E402  (shared retry/backoff)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
S2_FIELDS = "title,venue,year,publicationDate,citationCount,externalIds,publicationVenue"


def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


def arxiv_batch(ids):
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"id_list": ",".join(ids), "max_results": len(ids)})
    for attempt in range(8):  # the API rate-limits shared IPs (429); back off, then give up on this batch
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                root = ET.fromstring(r.read())
            break
        except Exception as e:
            print("  arXiv retry", attempt, e, file=sys.stderr)
            time.sleep(min(10 * (attempt + 1), 60))
    else:
        print("  arXiv batch failed; ids stay unverified until a re-run:", ",".join(ids), file=sys.stderr)
        return {}
    out = {}
    for e in root.findall("a:entry", NS):
        aid = norm_arxiv(e.findtext("a:id", "", NS).rsplit("/abs/", 1)[-1])
        title = re.sub(r"\s+", " ", e.findtext("a:title", "", NS)).strip()
        if not aid or title == "Error":
            continue
        out[aid] = dict(arxiv_title=title, published=e.findtext("a:published", "", NS)[:10],
                        updated=e.findtext("a:updated", "", NS)[:10],
                        authors=[a.findtext("a:name", "", NS) for a in e.findall("a:author", NS)],
                        comment=re.sub(r"\s+", " ", e.findtext("x:comment", "", NS) or "").strip(),
                        journal_ref=e.findtext("x:journal_ref", "", NS) or "",
                        primary_category=(e.find("x:primary_category", NS).get("term")
                                          if e.find("x:primary_category", NS) is not None else ""))
    return out


def s2_batch(ids):
    headers = {"Content-Type": "application/json"}
    if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
    body = json.dumps({"ids": [f"arXiv:{i}" for i in ids]}).encode()
    delay = 2.0
    for attempt in range(12):
        req = urllib.request.Request(
            "https://api.semanticscholar.org/graph/v1/paper/batch?fields=" + S2_FIELDS, data=body, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                res = json.loads(r.read())
            return {i: x for i, x in zip(ids, res) if x}
        except Exception:
            time.sleep(delay)
            delay = min(delay * 2, 30)
    return {}


def main():
    args = [a for a in sys.argv[1:] if a != "--refresh"]
    rows = [r for p in args for r in csv.DictReader(open(p))]
    path = os.path.join(ROOT, "data/core/core_meta.json")
    old = {} if "--refresh" in sys.argv or not os.path.exists(path) else json.load(open(path))
    want = sorted({norm_arxiv(r["arxiv"]) for r in rows if norm_arxiv(r.get("arxiv"))})
    ids = [i for i in want if not old.get(i, {}).get("verified")]
    meta = {}
    for k in range(0, len(ids), 20):
        meta.update(arxiv_batch(ids[k:k + 20]))
        time.sleep(3)
    s2 = {}
    for k in range(0, len(ids), 400):
        s2.update(s2_batch(ids[k:k + 400]))
    out = dict(old)
    for i in ids:
        m = meta.get(i)
        s = s2.get(i, {})
        out[i] = dict(m or {}, verified=bool(m), venue=s.get("venue") or "",
                      venue_name=(s.get("publicationVenue") or {}).get("name", ""),
                      citations=s.get("citationCount"), s2_date=s.get("publicationDate") or "",
                      dblp=(s.get("externalIds") or {}).get("DBLP", ""))
    json.dump(out, open(path, "w"), indent=1, ensure_ascii=False)
    bad = [i for i in want if not out[i]["verified"]]
    print(f"{len(want)} ids ({len(ids)} queried), arXiv-verified {len(want) - len(bad)}, S2 hits {len(s2)} -> {path}")
    if bad:
        print("NOT FOUND on arXiv:", " ".join(bad))


if __name__ == "__main__":
    main()
