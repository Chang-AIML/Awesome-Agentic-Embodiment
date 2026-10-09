#!/usr/bin/env python3
"""Full-text judging of the paper list: shards in, review, apply.

The judging itself is done by subagents that follow screening/prompts/content_rejudge.txt (one agent per shard,
INPUT = a shard .tsv, OUTPUT = <out_dir>/<shard>.txt, one line per paper:
key|arxiv|decision_model|model_status|main_contribution|connection|verdict|seat|role|evidence|reason|multi_agent;
runs before the multi-agent chapter (2026-10-09) have no multi_agent field).
The 2026-10-09 run in data/judging_runs/content_rejudge/ used the earlier three-layer fields (layer|subtype) in those
two columns; its results were mapped to seats by hand (data/core/paper_list.csv), so it is a record, never re-applied.

  shards  <source.csv> <text_dir> <shard_dir> [size]
      source: data/core/paper_list.csv, data/core/extended_2026.csv, extended_2022_2025.csv or any CSV with
      arxiv + title and key (or id). Writes <shard_dir>/kNN.tsv (key, arxiv or -, title, text path [, year]) and
      <shard_dir>/ids.txt for scripts/judging/fetch_fulltext.sh. Rows without an arXiv id are listed and skipped,
      unless the CSV has a text column (resolve_fulltext.py csv writes one, with year, for papers off arXiv).
  review  <out_dir> [changes|verdict|all]
      Parse the outputs, check completeness, and compare with data/core/paper_list.csv.
  verify  <first_out_dir> <shard_dir> <verify_shard_dir>
      Second pass (screening/prompts/content_verify.txt, a stronger model): one shard per finished first-pass shard
      with every paper except clear exclusions (剔除 with FT / SPEC / NONE; 1 in 10 of those kept for QA), plus a
      .prior.txt with the first-pass lines. Rerun as first-pass shards finish; existing verify shards are kept.
  merge   <first_out_dir> <verify_out_dir> <final_out_dir>
      Final lines = the verified line where there is one, else the first-pass line; review / apply the final dir.
  apply   <out_dir> <shard_dir> [--update]
      Write the verdicts into data/core/paper_list.csv. New papers are appended with their candidate id in the id
      column and a short display key from the title; papers already in the CSV (by key or id) are left alone unless
      --update is given, and a paper whose arXiv id is already listed is skipped. Then run
      scripts/build_paper_list.py.
"""
import csv, glob, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV = os.path.join(ROOT, "data/core/paper_list.csv")
FIELDS = "key arxiv model status contrib conn verdict seat role evidence reason multi".split()  # multi: 2026-10-09 on
VERDICTS = ["保留", "资源", "剔除"]
SEATS = ["Designer", "Teacher", "Developer", "Controller", "Supervisor", "-"]
PHASE = {"Designer": "执行前", "Teacher": "执行前", "Developer": "执行前", "Controller": "运行时", "Supervisor": "运行时"}
ROLES = {"Designer": ["环境/重建", "奖励/任务"], "Teacher": ["示范/蒸馏"], "Developer": ["系统/代码", "本体/工具"],
         "Controller": ["编排", "写策略", "直接动作"], "Supervisor": ["监控/恢复"]}
ROLE_ORDER = ["环境/重建", "奖励/任务", "示范/蒸馏", "系统/代码", "本体/工具", "编排", "写策略", "直接动作", "监控/恢复", "评测", ""]
COLS = ["verdict", "phase", "seat", "role", "topic", "key", "year", "tier", "title", "arxiv", "decision_model",
        "model_status", "contribution", "connection", "reason", "evidence", "note", "arrows", "id"]
TOPIC_MA = "多智能体"  # topic column: ;-separated chapters across seats; the judging sets or clears only this one
clean = lambda s: " ".join((s or "").split())


def short_name(title, taken):
    """Display key for a paper added by `apply`: the name before the colon (up to 3 words), else the first 6
    words of the title; made unique against `taken`."""
    t = clean(title)
    m = re.match(r"^([^:]{2,40}?)\s*:\s+\S", t)
    k = m.group(1).strip() if m and len(m.group(1).split()) <= 3 else " ".join(t.split()[:6]).rstrip(",;:")
    base, n = k, 2
    while k.lower() in taken:
        k, n = f"{base} ({n})", n + 1
    taken.add(k.lower())
    return k


def shards(src, text_dir, shard_dir, size=10):
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig")))
    os.makedirs(shard_dir, exist_ok=True)
    keep, skipped = [], []
    for r in rows:
        a = re.sub(r"v\d+$", "", (r.get("arxiv") or "").strip())
        text = r.get("text") or (os.path.join(os.path.abspath(text_dir), a + ".txt") if a else "")
        (keep if text else skipped).append((r.get("key") or r.get("id"), a, clean(r.get("title")), text,
                                            (r.get("year") or "")[:4]))
    for k in range(0, len(keep), size):
        with open(os.path.join(shard_dir, f"k{k // size:02d}.tsv"), "w") as f:
            for key, a, t, text, year in keep[k:k + size]:
                f.write(f"{key}\t{a or '-'}\t{t}\t{text}" + (f"\t{year}" if year else "") + "\n")
    open(os.path.join(shard_dir, "ids.txt"), "w").write("\n".join(sorted({x[1] for x in keep if x[1]})) + "\n")
    print(f"{len(keep)} papers -> {-(-len(keep) // size)} shards in {shard_dir}; no arXiv id, skipped: {len(skipped)}")
    for s in skipped:
        print("  skip", s[0], s[2][:80])


def parse(out_dir):
    got, bad = {}, []
    for p in sorted(glob.glob(os.path.join(out_dir, "*.txt"))):
        for line in open(p):
            x = [s.strip() for s in line.rstrip("\n").split("|")]
            if len(x) not in (11, 12):
                if line.strip():
                    bad.append((os.path.basename(p), line.strip()[:100]))
                continue
            g = dict(zip(FIELDS, x + [""] * (12 - len(x))))
            g["multi"] = g["multi"].upper()[:1]
            seat = (g["seat"].split() or ["-"])[0].strip("·")  # agents sometimes add words after the seat
            seat = seat[:1].upper() + seat[1:].lower() if seat != "-" else seat
            role = g["role"].strip()
            if g["verdict"] == "资源":  # the evaluated seat, role 评测
                role = "评测"
            elif g["verdict"] == "剔除":
                seat, role = "-", ""
            g["seat"], g["role"], g["phase"] = seat, role, PHASE.get(seat, "-")
            got[g["key"]] = g
    return got, bad


def review(out_dir, mode="changes"):
    cur = {r["key"]: r for r in csv.DictReader(open(CSV, encoding="utf-8-sig"))}
    got, bad = parse(out_dir)
    print(f"parsed {len(got)}; malformed {len(bad)}; new keys {sum(k not in cur for k in got)}")
    for b in bad:
        print("  BAD", b)
    print(Counter(g["status"] for g in got.values()), Counter(g["contrib"] for g in got.values()),
          Counter(g["verdict"] for g in got.values()))
    for k, g in got.items():
        c = cur.get(k, {})
        old = (c.get("verdict"), c.get("seat"), c.get("role"))
        new = (g["verdict"], g["seat"], g["role"])
        if mode == "all" or (mode == "changes" and old != new) or (mode == "verdict" and old[0] != new[0]):
            print(f"\n## {k}  {' '.join(x or '-' for x in old)}  ->  {' '.join(new)}")
            print(f"   model: {g['model']} | {g['status']} | {g['contrib']} | {g['conn']} | multi-agent {g['multi'] or '?'}")
            print(f"   ev: {g['evidence']}\n   why: {g['reason']}")


def apply(out_dir, shard_dir, update=False):
    rows = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    cur = {r["key"]: r for r in rows}
    cur.update({r["id"]: r for r in rows if r.get("id")})  # papers added earlier are matched by candidate id
    have_arxiv = {r["arxiv"]: r["key"] for r in rows if r["arxiv"]}
    taken = {r["key"].lower() for r in rows}
    meta = {}
    for p in glob.glob(os.path.join(shard_dir, "k*.tsv")):
        for line in open(p):
            x = line.rstrip("\n").split("\t")
            meta[x[0]] = (x[1].strip("-"), x[2], x[4] if len(x) > 4 else "")
    got, bad = parse(out_dir)
    assert not bad, f"{len(bad)} malformed lines; fix them first"
    added = changed = 0
    redo = [k for k, g in got.items() if g["reason"].startswith("无全文")]
    for k in redo:  # the agent had no text to read; redo these once the text is there
        print("  skip (no text):", k)
        del got[k]
    for k, g in got.items():
        bad_label = g["verdict"] not in VERDICTS or g["seat"] not in SEATS or (
            g["verdict"] == "保留" and g["role"] not in ROLES.get(g["seat"], []))
        assert not bad_label, (k, g["verdict"], g["seat"], g["role"])
        vals = dict(verdict=g["verdict"], phase=g["phase"], seat=g["seat"], role=g["role"], decision_model=g["model"],
                    model_status=g["status"], contribution=g["contrib"], connection=g["conn"], reason=g["reason"],
                    evidence=g["evidence"])
        topics = [t for t in (cur.get(k, {}).get("topic") or "").split(";") if t and t != TOPIC_MA]
        vals["topic"] = ";".join(topics + [TOPIC_MA] * (g["multi"] == "Y")) if g["multi"] else cur.get(k, {}).get("topic", "")
        if k in cur:
            if update:
                r = cur[k]
                if (r["verdict"], r["seat"], r["role"]) != (g["verdict"], g["seat"], g["role"]):
                    vals["note"] = f"全文复核：原为 {r['verdict']} {r['seat']} {r['role']}".strip()
                r.update(vals)
                changed += 1
            continue
        a, t, year = meta.get(k, (g["arxiv"], "", ""))
        if a and a in have_arxiv:
            print(f"  skip {k}: arXiv {a} is already in the list as {have_arxiv[a]}")
            continue
        m = re.match(r"(\d{2})\d{2}\.\d{4,5}$", a)
        year = "20" + m.group(1) if m else year
        rows.append(dict(vals, id=k, key=short_name(t, taken) if t else k, arxiv=a, title=t, year=year,
                         tier="2026" if year == "2026" else "先驱", arrows="", note=""))
        have_arxiv[a] = k
        added += 1
    rows.sort(key=lambda r: (VERDICTS.index(r["verdict"]), SEATS.index(r["seat"]), ROLE_ORDER.index(r["role"]),
                             r["tier"] != "先驱", r["year"], r["key"].lower()))
    with open(CSV, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"added {added}, updated {changed}; {len(rows)} rows:", Counter(r["verdict"] for r in rows))


def verify_shards(first_dir, shard_dir, vdir, sample=10):
    """Second pass (screening/prompts/content_verify.txt): one verify shard per complete first-pass shard, holding
    every paper except clear exclusions (剔除 with FT / SPEC / NONE), of which 1 in `sample` is kept for QA."""
    os.makedirs(vdir, exist_ok=True)
    n = 0
    for t in sorted(glob.glob(os.path.join(shard_dir, "k*.tsv"))):
        name = os.path.basename(t)[:-4]
        out = os.path.join(first_dir, name + ".txt")
        if os.path.exists(os.path.join(vdir, name + ".tsv")) or not os.path.exists(out):
            continue
        rows = [l for l in open(t) if l.strip()]
        lines = {l.split("|")[0].strip(): l for l in open(out) if l.count("|") in (10, 11)}
        if any(r.split("\t")[0] not in lines for r in rows):
            continue  # first pass not finished
        pick = []
        for r in rows:
            k = r.split("\t")[0]
            x = [f.strip() for f in lines[k].split("|")]
            clear_out = x[6] == "剔除" and x[3] in ("FT", "SPEC", "NONE")
            if not clear_out or sum(map(ord, k)) % sample == 0:
                pick.append((r, lines[k]))
        if not pick:
            continue
        open(os.path.join(vdir, name + ".tsv"), "w").write("".join(r for r, _ in pick))
        open(os.path.join(vdir, name + ".prior.txt"), "w").write("".join(l if l.endswith("\n") else l + "\n" for _, l in pick))
        n += 1
        print(f"{name}: {len(pick)} of {len(rows)}")
    print(f"{n} verify shards written to {vdir}")


def merge(first_dir, verify_dir, out_dir):
    """Final lines: the verified line where there is one, else the first-pass line."""
    os.makedirs(out_dir, exist_ok=True)
    first, _ = parse(first_dir)
    ver, bad = parse(verify_dir)
    assert not bad, bad
    raw = {}
    for d in (first_dir, verify_dir):
        for p in sorted(glob.glob(os.path.join(d, "*.txt"))):  # sorted: a later file (e.g. zz_redo.txt) wins
            if p.endswith(".prior.txt"):
                continue
            for l in open(p):
                if l.count("|") in (10, 11):
                    raw.setdefault(d, {})[l.split("|")[0].strip()] = l.rstrip("\n")
    for p in sorted(glob.glob(os.path.join(first_dir, "k*.txt"))):
        keys = [l.split("|")[0].strip() for l in open(p) if l.count("|") in (10, 11)]
        with open(os.path.join(out_dir, os.path.basename(p)), "w") as f:
            for k in keys:
                f.write(raw.get(verify_dir, {}).get(k) or raw[first_dir][k])
                f.write("\n")
    changed = [k for k in ver if k in first and (first[k]["verdict"], first[k]["seat"], first[k]["role"], first[k]["multi"])
               != (ver[k]["verdict"], ver[k]["seat"], ver[k]["role"], ver[k]["multi"])]
    vc = Counter((first[k]["verdict"], ver[k]["verdict"]) for k in ver if k in first)
    print(f"merged {len(first)} first-pass lines, {len(ver)} verified, {len(changed)} changed;", dict(vc))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["shards"] and len(a) >= 4:
        shards(a[1], a[2], a[3], int(a[4]) if len(a) > 4 else 10)
    elif a[:1] == ["review"] and len(a) >= 2:
        review(a[1], a[2] if len(a) > 2 else "changes")
    elif a[:1] == ["verify"] and len(a) >= 4:
        verify_shards(a[1], a[2], a[3])
    elif a[:1] == ["merge"] and len(a) == 4:
        merge(a[1], a[2], a[3])
    elif a[:1] == ["apply"] and len(a) >= 3:
        apply(a[1], a[2], "--update" in a)
    else:
        sys.exit(__doc__)
