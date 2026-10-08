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
LEGEND = """**Legend.** *Carrier* — weights of the top-level decider: **G** general model used as-is, **C** embodied-trained decider + generic executor, **H** trained decider + co-designed learned executor, **I** one model decides and acts (→ marks migration, e.g. G→C). *Topology* — ×1 single agent, ×R role agents on one task, ×N one agent per robot, 1:N one decider for many robots, ×O agents owning branches of a campaign. *Loop* — **re-decide**: the model is called again with its own decisions and their consequences; **authored**: constraints or a program written by the model read live perception and adapt while the robot acts (e.g. ReKep re-solves its keypoint constraints and backtracks when one breaks). *Closure* — evidence the loop uses: E execution, H human."""


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
                 "European Conference on Computer Vision": "ECCV",
                 "Robotics: Science and Systems Conference": "RSS", "IEEE International Conference on Computer Vision": "ICCV",
                 "AAAI Conference on Artificial Intelligence": "AAAI", "IEEE Robotics and Automation Letters": "RA-L",
                 "Conference on Empirical Methods in Natural Language Processing": "EMNLP"}
        return short.get(v, v)
    return "arXiv"


def links(r, m):
    """Project / code links: explicit columns win, else URLs from the arXiv comment."""
    urls = [u.rstrip(".") for u in re.findall(r"https?://[^\s,;)]+", m.get("comment", ""))]
    pj = r.get("project") or next((u for u in urls if "github.com" not in u), "")
    cd = r.get("code") or next((u for u in urls if "github.com" in u), "")
    return (f" [[project]]({pj})" if pj else ""), (f" [[code]]({cd})" if cd else "")


SEAT_ORDER = {"Controller": 0, "Supervisor": 1, "Teacher": 2, "Designer": 3, "Developer": 4}


def seat_row_md(r, meta):
    a = norm_arxiv(r["arxiv"])
    m = meta.get(a, {})
    year = (m.get("published") or r.get("date") or "")[:4]
    title = m.get("arxiv_title") or r["title"]
    proj, code = links(r, m)
    seat2 = r.get("seat2") if r.get("seat2") not in (None, "", "-") else "–"
    return (f"| **{r['key']}** | [{title}](https://arxiv.org/abs/{a}){proj}{code} | {year} | {venue_of(r, m)} | {r['seat']} | "
            f"{r['carrier']} | {r['interface']} | {r.get('loop') or '–'} | {r['body']} | {seat2} |")


def row_md(r, meta):
    a = norm_arxiv(r["arxiv"])
    m = meta.get(a, {})
    year = (m.get("published") or r.get("date") or "")[:4]
    title = m.get("arxiv_title") or r["title"]
    link = f"https://arxiv.org/abs/{a}" if a else (r.get("url") or "")
    name = f"[{title}]({link})" if link else title
    proj, code = links(r, m)
    topo = r["topo"].replace("x", "×") if r["topo"] not in ("", "-") else "–"
    seat2 = r.get("seat2") if r.get("seat2") not in (None, "", "-") else "–"
    return (f"| **{r['key']}** | {name}{proj}{code} | {year} | {venue_of(r, m)} | {r['carrier']} | {r['interface']} | "
            f"{topo} | {r.get('loop') or '–'} | {r['closure']} | {r['body']} | {seat2} |")


def main():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data/core/core_table.csv"))))
    mp = os.path.join(ROOT, "data/core/core_meta.json")
    meta = json.load(open(mp)) if os.path.exists(mp) else {}
    sort_key = lambda r: ((meta.get(norm_arxiv(r["arxiv"]), {}).get("published") or r.get("date") or "9999"), r["key"])
    head = ("| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|")
    seat_head = ("| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |\n"
                 "|---|---|---|---|---|---|---|---|---|---|")

    core = [r for r in rows if r["tier"] == "core"]
    r2s = [r for r in core if r.get("theme")]
    pio = [r for r in rows if r["tier"] == "pioneer"]
    res = [r for r in rows if r["tier"] == "resource"]
    ep = os.path.join(ROOT, "data/core/extended_2026.csv")  # build_extended.py
    ext = list(csv.DictReader(open(ep))) if os.path.exists(ep) else []
    seats = Counter(r["seat"] for r in core)
    out = ["# Awesome Agentic Embodiment", "",
           "> *Agentic Embodiment studies foundation-model-driven processes that make explicit decisions whose "
           "consequences reach a robot body, and that re-decide on evidence of those consequences. Its organizing "
           "question is where such a process sits relative to the body's deployed policy — steering it, guarding it, "
           "teaching it, designing its learning problem, or building its system (**Seat**) — and which weights carry it "
           "(**Carrier**).*", "",
           "**Thesis.** *Agency spreads around the body — and loop closure, not weights, makes a carrier an agent.*", "",
           f"The list focuses on **2026**: **{len(core)} core papers** from 2026 organized by Seat (including a "
           f"Real2Sim / Sim2Real section of {len(r2s)}), **{len(pio)} pioneers** from 2022–2025, and **{len(res)} "
           "benchmarks and resources**. Definition and inclusion rules: [docs/definition.md](docs/definition.md) "
           "(Chinese).", "",
           "## What counts as an agent", "",
           "All three must hold: (1) **explicit decisions** — plans, skill/tool/VLA calls, code, verdicts, system edits "
           "(not scores, latents or action chunks); (2) **decision authority** — the model writes its options, or picks "
           "among them with a control action (stop / retry / replan / ask / keep-revert); (3) **closed loop** — the model "
           "is called again with its own earlier decisions and evidence of their consequences and can revise them, *or* "
           "the constraints or program it wrote read live perception and adapt the behaviour while the robot acts "
           "(an *authored* loop, e.g. ReKep, VoxPoser, Code as Policies).", "",
           "Not included: reactive VLAs (incl. RL-finetuned), latent dual-systems, scalar reward/value models, one-shot "
           "annotators, world-model foresight (see the WAM survey), game/text worlds, purely digital agents.", "",
           "## Seat × Carrier (2026 core)", "",
           "Core papers per cell (carrier of the source decider; Teacher rows count the teacher).", "",
           "| Seat | Phase | G | C | H | I | Total |", "|---|---|---|---|---|---|---|"]
    for s, ph in (("Controller", "runtime"), ("Supervisor", "runtime"), ("Teacher", "pre-deployment"),
                  ("Designer", "pre-deployment"), ("Developer", "pre-deployment")):
        car = Counter(r["carrier"].split("→")[0].strip() for r in core if r["seat"] == s)
        out.append(f"| {s} | {ph} | " + " | ".join(str(car.get(k, 0) or "·") for k in "GCHI") + f" | {seats.get(s, 0)} |")
    out += ["", LEGEND, "", "## Contents", ""]
    anchor = lambda t: "#" + re.sub(r"[^a-z0-9 -]", "", t.lower()).replace(" ", "-")
    for _, _, title, _ in SECTIONS:
        out.append(f"- [{title}]({anchor(title)})")
    out += ["- [Real2Sim / Sim2Real](#real2sim--sim2real)", "- [Pioneers (2022–2025)](#pioneers-20222025)",
            "- [Benchmarks and resources](#benchmarks-and-resources)"]
    if ext:
        out.append(f"- [More 2026 papers ({len(ext)})](#more-2026-papers)")
    out.append("")
    for seat, sub, title, desc in SECTIONS:
        xs = sorted([r for r in core if r["seat"] == seat and (sub is None or r["sub"] == sub) and not r.get("theme")],
                    key=sort_key)
        out += [f"## {title}", "", desc, "", head] + [row_md(r, meta) for r in xs] + [""]
    out += ["## Real2Sim / Sim2Real", "",
            "Agents that build or calibrate simulators from the real world (Real2Sim), transfer or adapt what they "
            "learned in simulation to the real robot (Sim2Real), or practise in a reconstructed simulator and go back "
            "to the real one (Real2Sim2Real). Each paper keeps its Seat: building the simulator is the problem side "
            "(Designer), adapting the solution is Developer.", "",
            seat_head] + [seat_row_md(r, meta) for r in sorted(r2s, key=sort_key)] + [""]
    out += ["## Pioneers (2022–2025)", "",
            "Earlier foundational and representative works, listed briefly. *Loop* shows whether a paper already "
            "closes the loop (re-decide / authored) or is an open-loop forerunner (none).", "",
            seat_head] + [seat_row_md(r, meta) for r in sorted(pio, key=lambda r: (SEAT_ORDER.get(r["seat"], 9), sort_key(r)))] + [""]
    out += ["## Benchmarks and resources", "",
            "| Name | Paper | Year | Venue | Evaluated seat | Body |", "|---|---|---|---|---|---|"]
    for r in sorted(res, key=sort_key):
        a = norm_arxiv(r["arxiv"])
        m = meta.get(a, {})
        title = m.get("arxiv_title") or r["title"]
        pj, cd = links(r, m)
        out.append(f"| **{r['key']}** | [{title}](https://arxiv.org/abs/{a}){pj}{cd} | {(m.get('published') or r.get('date') or '')[:4]} | "
                   f"{venue_of(r, m)} | {r['seat']} | {r['body']} |")
    if ext:
        out += ["", "## More 2026 papers", "",
                f"{len(ext)} further 2026 papers that meet the definition (judged `core` by a verification pass) but "
                "are not in the curated tables above. Tags come from the judging pass and are not hand-checked; "
                "generated by `scripts/build_extended.py`.", ""]
        for seat, sub, title, _ in SECTIONS:
            xs = [r for r in ext if r["seat"] == seat and (sub is None or r["sub"] == sub or
                                                            (seat == "Controller" and sub == "orchestrator" and r["sub"] in ("", "-")))]
            if not xs:
                continue
            out += [f"<details><summary><b>{title}</b> ({len(xs)})</summary>", "",
                    "| Paper | Month | Carrier | Loop | Body |", "|---|---|---|---|---|"]
            for r in sorted(xs, key=lambda r: (r["date"], r["title"])):
                link = f"https://arxiv.org/abs/{r['arxiv']}" if r["arxiv"] else ""
                name = f"[{r['title']}]({link})" if link else r["title"]
                tag = f" `{r['theme']}`" if r.get("theme") else ""
                out.append(f"| {name}{tag} | {r['date'][:7]} | {r['carrier']} | {r['loop']} | {r['body']} |")
            out += ["", "</details>", ""]
    out += ["", "---", "", "Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.", ""]
    open(os.path.join(ROOT, "README.md"), "w").write("\n".join(out))
    print(f"README.md: core {len(core)} (real2sim {len(r2s)}), pioneer {len(pio)}, resource {len(res)}, more-2026 {len(ext)}")


if __name__ == "__main__":
    main()
