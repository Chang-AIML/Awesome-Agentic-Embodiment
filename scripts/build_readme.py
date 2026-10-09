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
    ep = os.path.join(ROOT, "data/core/extended_2022_2025.csv")
    ext_pre = list(csv.DictReader(open(ep))) if os.path.exists(ep) else []

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
           "acting as agents that make explicit decisions and are connected to a robot body — through the policy, code "
           "or plans they produce, or by acting on the environment directly. Its organizing question is where such an "
           "agent sits relative to the body's "
           "deployed policy — steering it, guarding it, teaching it, designing its learning problem, or building its "
           "system (**Seat**).*", "",
           "**Thesis (draft, under revision).** *Agency spreads around the body: general models, not embodied action "
           "models, fill seat after seat.*", "",
           f"Each seat is traced from its **{len(pio)} pioneers (2022–2025)** to **{len(core)} papers from 2026**, the year "
           f"most of the field's papers appeared; VLN / embodied navigation ({len(vln)} from 2026) has its own chapter and "
           f"the Real2Sim / Sim2Real sub-direction a short section ({len(r2s)}), plus **{len(res)} benchmarks and resources**. "
           "Definition and inclusion rules: [docs/definition.md](docs/definition.md) (Chinese).", "",
           "## Scope and what counts as an agent", "",
           "**Scope.** General-purpose foundation models (LLMs / VLMs such as GPT, Gemini, Claude, Qwen-VL, GPT-6 Astra) "
           "doing embodied work as agents. They may plan, call skills, tools or VLAs, write code or constraints, or emit "
           "actions directly (LLM-as-policy, e.g. GPT-6 Astra evaluated as a robot policy on RoboDojo). A general model "
           "fine-tuned for an agent role still counts if it keeps acting through an agent interface (e.g. GUAVA). "
           "**Embodied foundation models that produce actions are not included** — VLAs (also with reasoning, memory or "
           "self-correction), hierarchical VLAs, world action models, robot foundation models (π0.5, ECoT, OneTwoVLA, "
           "Hi Robot, Gemini Robotics, PaLM-E); they appear here only as tools called by an agent.", "",
           "**Agent tests**: (1) **a general model is the agent** and makes **explicit decisions** — plans, "
           "skill/tool/VLA calls, code, constraints, verdicts, system edits, or actions; (2) **decision authority** — "
           "the model writes its options, or picks among them with a control action (stop / retry / replan / ask / "
           "keep-revert); (3) **it is connected to the body** — what it decides reaches the policy / code layer or the "
           "environment, and the agent loop is the "
           "paper's main contribution (data-generation platforms are not included). Closing the loop is **recorded, not "
           "required**: *Loop* = re-decide (the model is called again with its earlier decisions and their consequences), "
           "authored (the constraints or program it wrote read live perception and adapt, e.g. ReKep, VoxPoser, Code as "
           "Policies) or none (open loop, e.g. ZS-Planners, CoPa). The share of closed-loop papers rises every year "
           "(see `docs/core_stats.md`).", "",
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
    out += ["- [Sub-direction: Real2Sim / Sim2Real](#sub-direction-real2sim--sim2real)",
            "- [VLN and embodied navigation](#vln-and-embodied-navigation)",
            "- [Benchmarks and resources](#benchmarks-and-resources)"]
    if ext:
        out.append(f"- [More 2026 papers ({len(ext)})](#more-2026-papers)")
    if ext_pre:
        out.append(f"- [More papers from 2022–2025 ({len(ext_pre)})](#more-papers-from-20222025)")
    out.append("")
    for seat, sub, title, desc in SECTIONS:
        out += [f"## {title}", "", desc, ""] + lineage([r for r in pio if in_section(r, seat, sub)],
                                                       [r for r in core if in_section(r, seat, sub)], head, row_md)
    out += ["## Sub-direction: Real2Sim / Sim2Real", "",
            "One sub-direction that cuts across Designer and Developer: agents that build or calibrate simulators from the "
            "real world (Real2Sim), transfer what they learned in simulation to the real robot (Sim2Real), or practise in a "
            "reconstructed simulator and go back to the real one (Real2Sim2Real). Only representative papers are listed "
            "here; further ones are in *More 2026 papers*.", ""] + \
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
    groups = [(seat, sub, title) for seat, sub, title, _ in SECTIONS]
    groups.insert(3, ("vln", None, "VLN and embodied navigation"))
    for xs_all, head_, what in ((ext, "More 2026 papers", "2026 papers"),
                                (ext_pre, "More papers from 2022–2025", "papers from 2022–2025")):
        if not xs_all:
            continue
        out += ["", f"## {head_}", "",
                f"{len(xs_all)} further {what} that meet the definition (judged by a verification pass; open-loop ones "
                "have *Loop* = none) but "
                "are not in the curated tables above. Tags come from the judging pass and are not hand-checked; "
                "generated by `scripts/build_extended.py`.", ""]
        for seat, sub, title in groups:
            if seat == "vln":
                xs = [r for r in xs_all if is_nav(r)]
            else:
                xs = [r for r in xs_all if r["seat"] == seat and not is_nav(r) and (sub is None or r["sub"] == sub or (
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
          f"more-2026 {len(ext)}, more-2022-2025 {len(ext_pre)}")


if __name__ == "__main__":
    main()
