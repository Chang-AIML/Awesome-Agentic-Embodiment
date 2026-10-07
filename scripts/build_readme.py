#!/usr/bin/env python3
"""Generate README.md (the awesome list) from data/core/core_table.csv + data/core/core_meta.json.

Sections follow the survey taxonomy: one per Seat (Controller split into four sub-types), then
precursors and resources. Columns carry the anatomy tags (Carrier, Interface, Topology, Body).

Usage: python3 scripts/build_readme.py
"""
import csv, json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECTIONS = [
    ("Controller", "orchestrator", "Controller · Orchestrators",
     "Called during evaluated episodes; sequence skills, tools or VLAs-as-tools."),
    ("Controller", "direct", "Controller · Direct drivers",
     "Called during evaluated episodes; emit semantic micro-actions, native commands or code executed now."),
    ("Controller", "lifelong", "Controller · Lifelong / memory agents",
     "Improve memory, skill libraries or harness across evaluated episodes."),
    ("Controller", "trained", "Controller · Trained carriers (C / H / I)",
     "The decider itself is embodied-trained: generic executor (C), co-designed executor (H) or one model (I)."),
    ("Supervisor", None, "Supervisor",
     "Runtime, acts only on exceptions: gates, vetoes, failure detection and recovery, by a separate check process."),
    ("Teacher", None, "Teacher",
     "Before deployment, the agent acts; its outcome-checked behaviour becomes the deployed model's training target."),
    ("Designer", None, "Designer",
     "Before deployment, the agent designs the learning problem: rewards, tasks, environments, curricula, eval suites."),
    ("Developer", None, "Developer",
     "Before deployment, the agent edits the solution: policy code, skill libraries, harness, training code, hardware; keeps or reverts by its own experiments."),
]
LEGEND = """**Legend.** *Carrier* — weights of the top-level decider: **G** general model used as-is, **C** embodied-trained decider + generic executor, **H** trained decider + co-designed learned executor, **I** one model decides and acts (→ marks migration, e.g. G→C). *Topology* — ×1 single agent, ×R role agents on one task, ×N one agent per robot, 1:N one decider for many robots, ×O agents owning branches of a campaign. *Closure* — evidence used to re-decide: E execution, H human."""


def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


def venue_of(r, m):
    v = r.get("venue") or ""
    if v:
        return v
    v = m.get("venue") or ""
    if v and v.lower() not in ("arxiv.org", "arxiv", "corr"):
        short = {"Conference on Robot Learning": "CoRL", "Computer Vision and Pattern Recognition": "CVPR",
                 "International Conference on Learning Representations": "ICLR",
                 "Neural Information Processing Systems": "NeurIPS", "International Conference on Machine Learning": "ICML",
                 "IEEE International Conference on Robotics and Automation": "ICRA",
                 "IEEE/RJS International Conference on Intelligent RObots and Systems": "IROS",
                 "Robotics: Science and Systems": "RSS", "International Conference on Computer Vision": "ICCV",
                 "European Conference on Computer Vision": "ECCV"}
        return short.get(v, v)
    return "arXiv"


def row_md(r, meta):
    a = norm_arxiv(r["arxiv"])
    m = meta.get(a, {})
    year = (m.get("published") or r.get("date") or "")[:4]
    title = m.get("arxiv_title") or r["title"]
    link = f"https://arxiv.org/abs/{a}" if a else (r.get("url") or "")
    name = f"[{title}]({link})" if link else title
    proj = f" [[project]]({r['project']})" if r.get("project") else ""
    code = f" [[code]]({r['code']})" if r.get("code") else ""
    topo = r["topo"].replace("x", "×") if r["topo"] not in ("", "-") else "–"
    seat2 = r.get("seat2") if r.get("seat2") not in (None, "", "-") else "–"
    return (f"| **{r['key']}** | {name}{proj}{code} | {year} | {venue_of(r, m)} | {r['carrier']} | {r['interface']} | "
            f"{topo} | {r['closure']} | {r['body']} | {seat2} |")


def main():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/core/core_table.csv"))))
    mp = os.path.join(ROOT, "data/core/core_meta.json")
    meta = json.load(open(mp)) if os.path.exists(mp) else {}
    sort_key = lambda r: ((meta.get(norm_arxiv(r["arxiv"]), {}).get("published") or r.get("date") or "9999"), r["key"])
    head = "| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |\n|---|---|---|---|---|---|---|---|---|---|"

    core = [r for r in rows if r["tier"] == "core"]
    pre = [r for r in rows if r["tier"] == "precursor"]
    res = [r for r in rows if r["tier"] == "resource"]
    seats = Counter(r["seat"] for r in core)
    out = ["# Awesome Agentic Embodiment", "",
           "> *Agentic Embodiment studies foundation-model-driven processes that make explicit decisions whose "
           "consequences reach a robot body, and that re-decide on evidence of those consequences. Its organizing "
           "question is where such a process sits relative to the body's deployed policy — steering it, guarding it, "
           "teaching it, designing its learning problem, or building its system (**Seat**) — and which weights carry it "
           "(**Carrier**).*", "",
           "**Thesis.** *Agency spreads around the body — and loop closure, not weights, makes a carrier an agent.*", "",
           f"This list holds the survey's core table: **{len(core)} core papers**, **{len(pre)} precursors** and "
           f"**{len(res)} resources**, organized by Seat. Definition and inclusion rules: "
           "[docs/definition.md](docs/definition.md) (Chinese).", "",
           "## What counts as an agent", "",
           "All three must hold: (1) **explicit decisions** — plans, skill/tool/VLA calls, code, verdicts, system edits "
           "(not scores, latents or action chunks); (2) **decision authority** — the model writes its options, or picks "
           "among them with a control action (stop / retry / replan / ask / keep-revert); (3) **closed loop** — the model "
           "is called again with its own earlier decisions and evidence of their consequences, and can revise them.", "",
           "Not included: reactive VLAs (incl. RL-finetuned), latent dual-systems, scalar reward/value models, one-shot "
           "annotators, world-model foresight (see the WAM survey), game/text worlds, purely digital agents.", "",
           "## Seat × Carrier", "",
           "Core papers per cell (carrier of the source decider; Teacher rows count the teacher).", "",
           "| Seat | Phase | G | C | H | I | Total |", "|---|---|---|---|---|---|---|"]
    for s, ph in (("Controller", "runtime"), ("Supervisor", "runtime"), ("Teacher", "pre-deployment"),
                  ("Designer", "pre-deployment"), ("Developer", "pre-deployment")):
        car = Counter(r["carrier"].split("→")[0].strip() for r in core if r["seat"] == s)
        out.append(f"| {s} | {ph} | " + " | ".join(str(car.get(k, 0) or "·") for k in "GCHI") + f" | {seats.get(s, 0)} |")
    out += ["", LEGEND, "", "## Contents", ""]
    for _, _, title, _ in SECTIONS:
        out.append(f"- [{title}](#{re.sub(r'[^a-z0-9 -]', '', title.lower()).replace(' ', '-')})")
    out += ["- [Precursors](#precursors)", "- [Benchmarks and resources](#benchmarks-and-resources)", ""]
    for seat, sub, title, desc in SECTIONS:
        xs = sorted([r for r in core if r["seat"] == seat and (sub is None or r["sub"] == sub)], key=sort_key)
        out += [f"## {title}", "", desc, "", head] + [row_md(r, meta) for r in xs] + [""]
    out += ["## Precursors", "",
            "Foundational works that make explicit decisions with authority but do not close the loop on their own "
            "decisions (one-shot plans or programs, per-step decisions without own history). Kept as lineage.", "",
            head] + [row_md(r, meta) for r in sorted(pre, key=sort_key)] + [""]
    out += ["## Benchmarks and resources", "",
            "| Name | Paper | Year | Venue | Evaluated seat | Body |", "|---|---|---|---|---|---|"]
    for r in sorted(res, key=sort_key):
        a = norm_arxiv(r["arxiv"])
        m = meta.get(a, {})
        title = m.get("arxiv_title") or r["title"]
        out.append(f"| **{r['key']}** | [{title}](https://arxiv.org/abs/{a}) | {(m.get('published') or r.get('date') or '')[:4]} | "
                   f"{venue_of(r, m)} | {r['seat']} | {r['body']} |")
    out += ["", "---", "", "Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.", ""]
    open(os.path.join(ROOT, "README.md"), "w").write("\n".join(out))
    print(f"README.md: core {len(core)}, precursor {len(pre)}, resource {len(res)}")


if __name__ == "__main__":
    main()
