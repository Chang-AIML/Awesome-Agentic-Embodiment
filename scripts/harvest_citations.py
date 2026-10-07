#!/usr/bin/env python3
"""Forward-citation snowballing from seed papers.

For every seed in data/seeds.json, fetch the papers that cite it (Semantic
Scholar by default, OpenAlex as fallback), then merge them into one candidate
table. Each candidate records which seeds it cites; citing several seeds is a
strong relevance signal and is used to sort the table.

Usage:
    python3 scripts/harvest_citations.py                     # core + extend + broad
    python3 scripts/harvest_citations.py --tiers core        # only core seeds
    python3 scripts/harvest_citations.py --source openalex   # use OpenAlex
    SEMANTIC_SCHOLAR_API_KEY=... python3 scripts/harvest_citations.py

Outputs (under --out, default data/candidates/):
    raw/<source>/<seed>.jsonl   one citing paper per line, cached for resume
    candidates.csv              merged, deduplicated, sorted candidate table
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

S2_API = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "paperId,title,abstract,year,venue,publicationDate,externalIds,citationCount"
OA_API = "https://api.openalex.org"
OA_SELECT = "id,doi,title,publication_year,publication_date,ids,cited_by_count,primary_location,locations,abstract_inverted_index"

# Citers of tier=broad seeds are kept only if title/abstract matches this.
EMBODIED_RE = re.compile(
    r"robot|manipulat|embodi|vision[- ]language[- ]action|\bvla|humanoid|grasp|"
    r"navigat|locomot|dexterous|quadruped|mobile manip|household|sim[- ]to[- ]real|"
    r"drone|\buav|autonomous driving|end[- ]effector|gripper|teleoperat|"
    r"alfred|habitat|behavior-1k|libero|calvin|maniskill|robocasa",
    re.IGNORECASE,
)


def http_get_json(url, headers=None, retries=6):
    delay = 2.0
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


# ---------------------------------------------------------------- Semantic Scholar

def s2_citations(arxiv_id):
    headers = {}
    if os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
    offset, limit = 0, 1000
    while True:
        url = (f"{S2_API}/paper/arXiv:{arxiv_id}/citations?"
               + urllib.parse.urlencode({"fields": S2_FIELDS, "limit": limit, "offset": offset}))
        try:
            page = http_get_json(url, headers)
        except urllib.error.HTTPError as e:
            # The citations endpoint caps offset+limit; report and stop rather than fail.
            print(f"  ! S2 stopped at offset {offset}: HTTP {e.code}", file=sys.stderr)
            return
        for row in page.get("data", []):
            p = row.get("citingPaper") or {}
            if not p.get("title"):
                continue
            ext = p.get("externalIds") or {}
            yield {
                "title": p.get("title"),
                "abstract": p.get("abstract") or "",
                "year": p.get("year"),
                "date": p.get("publicationDate") or "",
                "venue": p.get("venue") or "",
                "arxiv": ext.get("ArXiv") or "",
                "doi": ext.get("DOI") or "",
                "s2_id": p.get("paperId") or "",
                "citations": p.get("citationCount") or 0,
            }
        if "next" not in page:
            return
        offset = page["next"]
        time.sleep(1.1 if not headers else 0.2)


# ---------------------------------------------------------------- OpenAlex

def oa_abstract(inv):
    if not inv:
        return ""
    words = sorted((pos, w) for w, positions in inv.items() for pos in positions)
    return " ".join(w for _, w in words)


def oa_arxiv_id(work):
    doi = (work.get("doi") or "").lower()
    m = re.search(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})", doi)
    if m:
        return m.group(1)
    for loc in work.get("locations") or []:
        m = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})", (loc or {}).get("landing_page_url") or "")
        if m:
            return m.group(1)
    return ""


def oa_citations(arxiv_id):
    # Without a key, OpenAlex bills a daily budget shared by everyone on this IP.
    # The key can come from OPENALEX_API_KEY or be injected by the environment's proxy.
    headers = {}
    if os.environ.get("OPENALEX_API_KEY"):
        headers["Authorization"] = f"Bearer {os.environ['OPENALEX_API_KEY']}"
    seed = http_get_json(f"{OA_API}/works/https://doi.org/10.48550/arXiv.{arxiv_id}", headers)
    seed_id = seed["id"].rsplit("/", 1)[-1]
    cursor = "*"
    while cursor:
        url = (f"{OA_API}/works?"
               + urllib.parse.urlencode({"filter": f"cites:{seed_id}", "per-page": 200,
                                         "cursor": cursor, "select": OA_SELECT}))
        page = http_get_json(url, headers)
        for w in page.get("results", []):
            if not w.get("title"):
                continue
            venue = ((w.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
            yield {
                "title": w.get("title"),
                "abstract": oa_abstract(w.get("abstract_inverted_index")),
                "year": w.get("publication_year"),
                "date": w.get("publication_date") or "",
                "venue": venue,
                "arxiv": oa_arxiv_id(w),
                "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
                "s2_id": "",
                "citations": w.get("cited_by_count") or 0,
            }
        cursor = (page.get("meta") or {}).get("next_cursor")
        time.sleep(0.2)


# ---------------------------------------------------------------- merge

def harvest(seeds, source, raw_dir, refresh):
    fetch = s2_citations if source == "s2" else oa_citations
    os.makedirs(raw_dir, exist_ok=True)
    per_seed = {}
    for s in seeds:
        path = os.path.join(raw_dir, f"{s['key']}.jsonl")
        if os.path.exists(path) and not refresh:
            with open(path) as f:
                per_seed[s["key"]] = [json.loads(l) for l in f]
            print(f"{s['key']}: {len(per_seed[s['key']])} citers (cached)")
            continue
        print(f"{s['key']}: fetching citers of arXiv:{s['arxiv']} from {source} ...")
        rows = list(fetch(s["arxiv"]))
        with open(path, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        per_seed[s["key"]] = rows
        print(f"{s['key']}: {len(rows)} citers")
    return per_seed


def merge(seeds, per_seed):
    tier = {s["key"]: s["tier"] for s in seeds}
    seed_arxiv = {s["arxiv"] for s in seeds}
    merged, index = [], {}
    for key, rows in per_seed.items():
        for r in rows:
            if r["arxiv"] in seed_arxiv:
                continue
            ids = [f"arxiv:{r['arxiv']}" if r["arxiv"] else None,
                   f"doi:{r['doi'].lower()}" if r["doi"] else None,
                   f"t:{norm_title(r['title'])}"]
            ids = [i for i in ids if i]
            hit = next((index[i] for i in ids if i in index), None)
            if hit is None:
                hit = dict(r, seeds=[])
                merged.append(hit)
            else:
                for k in ("arxiv", "doi", "abstract", "date", "venue", "s2_id"):
                    if not hit.get(k) and r.get(k):
                        hit[k] = r[k]
                hit["citations"] = max(hit["citations"] or 0, r["citations"] or 0)
            if key not in hit["seeds"]:
                hit["seeds"].append(key)
            for i in ids:
                index[i] = hit
    out = []
    for p in merged:
        p["embodied_kw"] = bool(EMBODIED_RE.search(f"{p['title']} {p['abstract']}"))
        # Keep a paper reached only through broad seeds only if it looks embodied.
        if all(tier[k] == "broad" for k in p["seeds"]) and not p["embodied_kw"]:
            continue
        p["n_seeds"] = len(p["seeds"])
        p["n_core"] = sum(tier[k] == "core" for k in p["seeds"])
        out.append(p)
    out.sort(key=lambda p: (-p["n_core"], -p["n_seeds"], -(p["citations"] or 0)))
    return out


def write_csv(rows, path):
    cols = ["title", "year", "date", "venue", "arxiv", "doi", "citations",
            "n_core", "n_seeds", "seeds", "embodied_kw", "s2_id", "abstract"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(dict(r, seeds=";".join(r["seeds"])))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", default=os.path.join(ROOT, "data", "seeds.json"))
    ap.add_argument("--tiers", default="core,extend,broad")
    ap.add_argument("--source", choices=["s2", "openalex"], default="s2")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "candidates"))
    ap.add_argument("--refresh", action="store_true", help="ignore cached raw files")
    args = ap.parse_args()

    tiers = set(args.tiers.split(","))
    with open(args.seeds) as f:
        seeds = [s for s in json.load(f)["seeds"] if s["tier"] in tiers]
    per_seed = harvest(seeds, args.source, os.path.join(args.out, "raw", args.source), args.refresh)
    rows = merge(seeds, per_seed)
    os.makedirs(args.out, exist_ok=True)
    path = os.path.join(args.out, "candidates.csv")
    write_csv(rows, path)
    total = sum(len(v) for v in per_seed.values())
    print(f"\n{total} citing records -> {len(rows)} unique candidates -> {path}")
    for n in sorted({r["n_seeds"] for r in rows}, reverse=True):
        print(f"  cite {n} seed(s): {sum(r['n_seeds'] == n for r in rows)}")


if __name__ == "__main__":
    main()
