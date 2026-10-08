#!/usr/bin/env python3
"""Generate README.md (the awesome list) from data/core/core_table.csv + data/core/core_meta.json.

Sections follow the survey taxonomy: one per Seat (Controller split into three sub-types), then the
Real2Sim / Sim2Real and VLN chapters. Every section traces its lineage: pioneers (2022-2025) first, then
2026. Columns carry the anatomy tags (Carrier, Interface, Topology, Loop, Body).

Usage: python3 scripts/build_readme.py
"""
import csv, json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECTIONS = [
    ("Controller", "orchestrator", "Controller · Orchestrators",
     "Called during evaluated episodes; sequence skills, tools or VLAs-as-tools."),
    ("Controller", "direct", "Controller · Direct drivers",
     "Called during evaluated episodes; emit actions, semantic micro-actions, native commands, or code and constraints executed now."),
    ("Controller", "lifelong", "Controller · Lifelong / memory agents",
     "Improve memory, skill libraries or harness across evaluated episodes."),
    ("Supervisor", None, "Supervisor",
     "Runtime, acts only on exceptions: gates, vetoes, failure detection and recovery, by a separate check process."),
    ("Teacher", None, "Teacher",
     "Before deployment, the agent acts; its outcome-checked behaviour becomes the deployed model's training target."),
    ("Designer", None, "Designer",
     "Before deployment, the agent designs the learning problem: rewards, tasks, environments, curricula, eval suites."),
    ("Developer", None, "Developer",
     "Before deployment, the agent edits the solution: policy code, skill libraries, harness, training code, hardware; keeps or reverts by its own experiments."),
]
LEGEND = """**Legend.** *Carrier* — **G** general model used as-is, **C** general model fine-tuned or distilled for an agent role, still acting through tools, skills, code or plans (→ marks migration, e.g. G→C). *Topology* — ×1 single agent, ×R role agents on one task, ×N one agent per robot, 1:N one decider for many robots, ×O agents owning branches of a campaign. *Loop* — **re-decide**: the model is called again with its own decisions and their consequences; **authored**: constraints or a program written by the model read live perception and adapt while the robot acts (e.g. ReKep re-solves its keypoint constraints and backtracks when one breaks); **none**: written once (kept for pioneers and for the two exceptions). *Closure* — evidence the loop uses: E execution, H human."""


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
R2S_THEMES = {"real2sim", "sim2real", "real2sim2real"}  # theme "vln" marks the VLN chapter instead


def is_nav(r):
    """Navigation-first rows of the extended list go to the VLN group."""
    return r["seat"] == "Controller" and (r.get("body") or "").startswith("nav")


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
    pio = [r for r in rows if r["tier"] == "pioneer"]
    res = [r for r in rows if r["tier"] == "resource"]
    chapter = lambda r: "r2s" if r.get("theme") in R2S_THEMES else ("vln" if r.get("theme") == "vln" else "")
    r2s, vln = [r for r in core if chapter(r) == "r2s"], [r for r in core if chapter(r) == "vln"]
    ep = os.path.join(ROOT, "data/core/extended_2026.csv")  # build_extended.py
    ext = list(csv.DictReader(open(ep))) if os.path.exists(ep) else []

    def in_section(r, seat, sub):
        return not chapter(r) and r["seat"] == seat and (sub is None or r["sub"] == sub or (
            seat == "Controller" and sub == "orchestrator" and r["sub"] not in ("direct", "lifelong")))

    def lineage(pios, news, table_head, fmt):
        out = []
        if pios:
            out += ["**Pioneers (2022–2025)**", "", table_head] + [fmt(r, meta) for r in sorted(pios, key=sort_key)] + [""]
        if news:
            out += ["**2026**", "", table_head] + [fmt(r, meta) for r in sorted(news, key=sort_key)] + [""]
        return out

    out = ["# Awesome Agentic Embodiment", "",
           "> *Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs, not embodied action models — "
           "acting as agents that make explicit decisions whose consequences reach a robot body, and that re-decide on "
           "evidence of those consequences. Its organizing question is where such an agent sits relative to the body's "
           "deployed policy — steering it, guarding it, teaching it, designing its learning problem, or building its "
           "system (**Seat**).*", "",
           "**Thesis (draft, under revision).** *Agency spreads around the body: general models, not embodied action "
           "models, fill seat after seat.*", "",
           f"Each seat is traced from its **{len(pio)} pioneers (2022–2025)** to **{len(core)} papers from 2026**, the year "
           f"most of the field's papers appeared; Real2Sim / Sim2Real ({len(r2s)} from 2026) and VLN / embodied "
           f"navigation ({len(vln)} from 2026) have their own chapters, plus **{len(res)} benchmarks and resources**. "
           "Definition and inclusion rules: [docs/definition.md](docs/definition.md) (Chinese).", "",
           "## Scope and what counts as an agent", "",
           "**Scope.** General-purpose foundation models (LLMs / VLMs such as GPT, Gemini, Claude, Qwen-VL, GPT-6 Astra) "
           "doing embodied work as agents. They may plan, call skills, tools or VLAs, write code or constraints, or emit "
           "actions directly (LLM-as-policy, e.g. GPT-6 Astra evaluated as a robot policy on RoboDojo). A general model "
           "fine-tuned for an agent role still counts if it keeps acting through an agent interface (e.g. GUAVA). "
           "**Embodied foundation models that produce actions are not included** — VLAs (also with reasoning, memory or "
           "self-correction), hierarchical VLAs, world action models, robot foundation models (π0.5, ECoT, OneTwoVLA, "
           "Hi Robot, Gemini Robotics, PaLM-E); they appear here only as tools called by an agent.", "",
           "**Agent tests** (all three): (1) **explicit decisions** — plans, skill/tool/VLA calls, code, constraints, "
           "verdicts, system edits, or actions chosen by the general model; (2) **decision authority** — the model writes "
           "its options, or picks among them with a control action (stop / retry / replan / ask / keep-revert); "
           "(3) **closed loop** — the model is called again with its own earlier decisions and evidence of their "
           "consequences, *or* the constraints or program it wrote read live perception and adapt while the robot acts "
           "(an *authored* loop, e.g. ReKep, VoxPoser, Code as Policies). Two families are included even when written once "
           "(*Loop* = none): **constraint / keypoint programming** (ReKep-type) and **agentic Real2Sim**.", "",
           "Also not included: scalar reward/value models, one-shot annotators, world-model foresight, game/text worlds, "
           "purely digital agents.", "",
           "## Seat by period", "",
           "| Seat | Phase | Pioneers 2022–2025 | 2026 | of which fine-tuned (C) |", "|---|---|---|---|---|"]
    for s_, ph in (("Controller", "runtime"), ("Supervisor", "runtime"), ("Teacher", "pre-deployment"),
                   ("Designer", "pre-deployment"), ("Developer", "pre-deployment")):
        n_p = sum(1 for r in pio if r["seat"] == s_)
        n_c = sum(1 for r in core if r["seat"] == s_)
        n_ft = sum(1 for r in pio + core if r["seat"] == s_ and r["carrier"].split("→")[-1].strip() == "C")
        out.append(f"| {s_} | {ph} | {n_p} | {n_c} | {n_ft or '·'} |")
    out += ["", "Counts include the papers of the Real2Sim / Sim2Real and VLN chapters under their seats.", "",
            LEGEND, "", "## Contents", ""]
    anchor = lambda t: "#" + re.sub(r"[^a-z0-9 -]", "", t.lower()).replace(" ", "-")
    for _, _, title, _ in SECTIONS:
        out.append(f"- [{title}]({anchor(title)})")
    out += ["- [Real2Sim / Sim2Real](#real2sim--sim2real)", "- [VLN and embodied navigation](#vln-and-embodied-navigation)",
            "- [Benchmarks and resources](#benchmarks-and-resources)"]
    if ext:
        out.append(f"- [More 2026 papers ({len(ext)})](#more-2026-papers)")
    out.append("")
    for seat, sub, title, desc in SECTIONS:
        out += [f"## {title}", "", desc, ""] + lineage([r for r in pio if in_section(r, seat, sub)],
                                                       [r for r in core if in_section(r, seat, sub)], head, row_md)
    out += ["## Real2Sim / Sim2Real", "",
            "Agents that build or calibrate simulators from the real world (Real2Sim), transfer or adapt what they "
            "learned in simulation to the real robot (Sim2Real), or practise in a reconstructed simulator and go back "
            "to the real one (Real2Sim2Real). Each paper keeps its Seat: building the simulator is the problem side "
            "(Designer), adapting the solution is Developer.", ""] + \
           lineage([r for r in pio if chapter(r) == "r2s"], r2s, seat_head, seat_row_md)
    out += ["## VLN and embodied navigation", "",
            "Agents whose main task is navigation: vision-and-language navigation in continuous environments or on real "
            "robots, object-goal and instance navigation, long-range exploration. 2026 papers are evaluated in continuous "
            "simulation (e.g. Habitat VLN-CE) or on real robots; earlier agents on the discrete R2R graph appear only "
            "among the pioneers. Seats are kept, so the chapter mixes Controllers with a few Teachers and Designers.", ""] + \
           lineage([r for r in pio if chapter(r) == "vln"], vln, seat_head, seat_row_md)
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
        groups = [(seat, sub, title) for seat, sub, title, _ in SECTIONS]
        groups.insert(3, ("vln", None, "VLN and embodied navigation"))
        for seat, sub, title in groups:
            if seat == "vln":
                xs = [r for r in ext if is_nav(r)]
            else:
                xs = [r for r in ext if r["seat"] == seat and not is_nav(r) and (sub is None or r["sub"] == sub or (
                    seat == "Controller" and sub == "orchestrator" and r["sub"] not in ("direct", "lifelong")))]
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
    print(f"README.md: 2026 {len(core)} (real2sim {len(r2s)}, vln {len(vln)}), pioneers {len(pio)}, resources {len(res)}, "
          f"more-2026 {len(ext)}")


if __name__ == "__main__":
    main()
