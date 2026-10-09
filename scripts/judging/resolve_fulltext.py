#!/usr/bin/env python3
"""Find full texts for papers that have no arXiv id, so they can go through content_rejudge.py like the others.

  resolve <source.csv>... <out.jsonl>
      For every row without an arXiv id (key or id column; ids c* / s* are looked up in data/candidates for the
      Semantic Scholar id, DOI and abstract): a 10.48550/arXiv DOI gives the id directly; otherwise the arXiv API is
      searched by title; otherwise Semantic Scholar (paper id or DOI) may give an arXiv id or open-access PDF link.
      Writes one JSON line per paper (key, title, year, doi, arxiv, pdf, abstract, status); rerun to retry the
      lookups that failed (status err).
  fetch <resolved.jsonl> <text_dir> <ids.txt>
      Downloads the open-access PDFs to <text_dir>/<key>.txt (pdftotext); for papers with neither an arXiv id nor a
      PDF writes the abstract to <text_dir>/<key>.txt behind an "ABSTRACT ONLY" header (skipped if there is no
      abstract). Writes the arXiv ids found in step 1-2 to <ids.txt> for fetch_fulltext.sh.
  csv <resolved.jsonl> <text_dir> <out.csv>
      Writes a source CSV for `content_rejudge.py shards` (key, arxiv, title, year, text); rows whose text file is
      missing are left out and listed.
"""
import csv, difflib, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
norm = lambda s: re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def get(url, tries=3, wait=5):
    """GET bytes; None on 404, "err" after `tries` failures (e.g. 429 from Semantic Scholar without a key)."""
    for t in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "awesome-agentic-embodiment"}),
                                        timeout=30) as r:
                return r.read()
        except Exception as e:
            if getattr(e, "code", 0) == 404:
                return None
            if t + 1 < tries:
                time.sleep(wait * (t + 1))
    return "err"


def arxiv_by_title(title):
    """arXiv API title search (phrase query, else the longer words ANDed; arXiv drops stopwords such as "that");
    the id of an entry whose normalized title matches (ratio >= 0.93), else "", or "err" if the API failed."""
    clean = re.sub(r"[^A-Za-z0-9 ]+", " ", title).split()
    stop = {"that", "this", "with", "from", "into", "using", "towards", "toward", "their", "your", "through", "what",
            "when", "which", "where", "while", "over", "under", "via", "the", "and", "for"}
    long_words = [w for w in clean if len(w) > 3 and w.lower() not in stop][:6]
    for q in ('ti:"' + " ".join(clean) + '"', "+AND+".join(f"ti:{w}" for w in long_words)):
        x = get(f"https://export.arxiv.org/api/query?search_query={urllib.parse.quote(q, safe='+:')}&max_results=10", tries=3, wait=10)
        time.sleep(3)  # arXiv API: one request every 3 s
        if x == "err":
            return "err"
        x = (x or b"").decode("utf-8", "ignore")
        for aid, t in re.findall(r"<entry>.*?<id>https?://arxiv\.org/abs/([^<]+?)(?:v\d+)?</id>.*?<title>(.*?)</title>", x, re.S):
            if difflib.SequenceMatcher(None, norm(t), norm(title)).ratio() >= 0.93:
                return aid
        if "<entry>" in x:  # results, but none with this title
            return ""
    return ""


def sources():
    cand = list(csv.DictReader(open(os.path.join(ROOT, "data/candidates/candidates.csv"), encoding="utf-8-sig")))
    s2 = [json.loads(l) for l in open(os.path.join(ROOT, "data/candidates/s2_sweep_2026.jsonl"))]
    return lambda i: (cand[int(i[1:])] if i[0] == "c" else s2[int(i[1:])]) if re.match(r"[cs]\d{5}$", i) else {}


def resolve(srcs, out):
    """arXiv id from an arXiv DOI or the arXiv API title search; else Semantic Scholar (one try) for an arXiv id or
    an open-access PDF. (OpenAlex and Semantic Scholar throttle requests without an API key.) Papers whose lookup
    failed get status "err" and are retried on the next run."""
    done = {}
    if os.path.exists(out):
        for l in open(out):
            d = json.loads(l)
            done[d["key"]] = d
    src = sources()
    todo = []
    for p in srcs:
        for r in csv.DictReader(open(p, encoding="utf-8-sig")):
            key = r.get("key") or r.get("id")
            if (r.get("arxiv") or "").strip() or done.get(key, {}).get("status") == "ok":
                continue
            s = src(key)
            todo.append(dict(key=key, title=" ".join((r.get("title") or s.get("title") or "").split()),
                             year=(r.get("date") or r.get("year") or s.get("year") or "")[:4],
                             doi=(s.get("doi") or "").lower(), s2id=s.get("s2_id") or s.get("s2id") or "",
                             abstract=" ".join((s.get("abstract") or "").split())))
    print(f"{len(todo)} papers to resolve", flush=True)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    api = "https://api.semanticscholar.org/graph/v1/paper/"
    fields = "fields=title,externalIds,openAccessPdf"
    for n, d in enumerate(todo):
        d["arxiv"], d["pdf"], d["status"] = "", "", "ok"
        m = re.search(r"10\.48550/arxiv\.(\d{4}\.\d{4,5})", d["doi"])
        if m:
            d["arxiv"] = m.group(1)
        else:
            a = arxiv_by_title(d["title"]) if d["title"] else ""
            if a == "err":
                d["status"] = "err"
            elif a:
                d["arxiv"] = a
            elif d["s2id"] or d["doi"]:  # open-access PDF; one try, Semantic Scholar throttles requests without a key
                w = get(f"{api}{d['s2id'] or 'DOI:' + urllib.parse.quote(d['doi'])}?{fields}", tries=1)
                if w and w != "err":  # throttled: no PDF link, the paper is judged from its abstract
                    w = json.loads(w)
                    d["arxiv"] = re.sub(r"v\d+$", "", (w.get("externalIds") or {}).get("ArXiv") or "")
                    d["pdf"] = (w.get("openAccessPdf") or {}).get("url") or ""
        done[d["key"]] = d
        with open(out, "w") as f:
            f.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in done.values())
        if n % 50 == 0:
            print(n, flush=True)
    rows = list(done.values())
    print(f"{len(rows)} resolved: arXiv {sum(bool(r['arxiv']) for r in rows)}, "
          f"OA pdf {sum(bool(r['pdf']) and not r['arxiv'] for r in rows)}, "
          f"abstract only {sum(not r['arxiv'] and not r['pdf'] and bool(r['abstract']) for r in rows)}, "
          f"nothing {sum(not r['arxiv'] and not r['pdf'] and not r['abstract'] for r in rows)}, "
          f"lookup failed {sum(r['status'] == 'err' for r in rows)}")


def fetch(res, text_dir, ids_out):
    os.makedirs(text_dir, exist_ok=True)
    rows = [json.loads(l) for l in open(res)]
    open(ids_out, "w").write("".join(r["arxiv"] + "\n" for r in rows if r["arxiv"]))
    for r in rows:
        if r["arxiv"]:
            continue
        path = os.path.join(text_dir, r["key"] + ".txt")
        if os.path.exists(path) and os.path.getsize(path):
            continue
        ok = False
        if r["pdf"]:
            tmp = os.path.join(text_dir, "tmp_oa.pdf")
            ok = subprocess.run(["curl", "-sSL", "--max-time", "90", "-A", "Mozilla/5.0", "-o", tmp, r["pdf"]],
                                capture_output=True).returncode == 0 and open(tmp, "rb").read(5) == b"%PDF-" \
                and subprocess.run(["pdftotext", "-q", tmp, path]).returncode == 0 and os.path.getsize(path) > 2000
            if os.path.exists(tmp):
                os.remove(tmp)
            time.sleep(1)
        if not ok and r["abstract"]:
            open(path, "w").write(f"ABSTRACT ONLY (no full text available)\nTitle: {r['title']}\nDOI: {r['doi']}\n\n"
                                  f"Abstract\n{r['abstract']}\n")
            ok = "abstract"
        elif not ok and os.path.exists(path):
            os.remove(path)
        print(("ok" if ok is True else ok or "FAIL"), r["key"], flush=True)


def to_csv(res, text_dir, out):
    rows = [json.loads(l) for l in open(res)]
    kept = []
    for r in rows:
        path = os.path.abspath(os.path.join(text_dir, (r["arxiv"] or r["key"]) + ".txt"))
        if os.path.exists(path) and os.path.getsize(path):
            kept.append(dict(key=r["key"], arxiv=r["arxiv"], title=r["title"], year=r["year"], text=path))
        else:
            print("  no text", r["key"], r["title"][:80])
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["key", "arxiv", "title", "year", "text"])
        w.writeheader()
        w.writerows(kept)
    print(f"{len(kept)} of {len(rows)} have a text file -> {out}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["resolve"] and len(a) >= 3:
        resolve(a[1:-1], a[-1])
    elif a[:1] == ["fetch"] and len(a) == 4:
        fetch(*a[1:])
    elif a[:1] == ["csv"] and len(a) == 4:
        to_csv(*a[1:])
    else:
        sys.exit(__doc__)
