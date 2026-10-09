#!/usr/bin/env python3
"""Generate README.md (the awesome list) from data/core/core_table.csv + data/core/core_meta.json.

Sections follow the user's classification (2026-10-09): two phases, pre-execution (Designer, Teacher, Developer) and
runtime (Controller split into three sub-types, Supervisor), then the Real2Sim / Sim2Real, VLN and multi-agent chapters. Every section traces its lineage: pioneers (2022-2025) first, then
2026. Columns carry the anatomy tags (Carrier, Interface, Topology, Loop, Body).

Usage: python3 scripts/build_readme.py
"""
import csv, json, os, re
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PHASES = {"pre": ("Pre-execution", "The agent's output is produced before the robot executes the task and is frozen into "
                                    "the deployed system."),
          "run": ("Runtime", "The agent acts while the robot executes the task.")}
SECTIONS = [  # (phase, seat, Controller sub-type or None, title, description)
    ("pre", "Designer", None, "Designer",
     "Designs the learning problem: environments and scenes, simulation, rewards, tasks, curricula."),
    ("pre", "Teacher", None, "Teacher",
     "Executes the task itself; its verified demonstrations or experience become training targets for a policy or a "
     "smaller model."),
    ("pre", "Developer", None, "Developer",
     "Modifies the system itself: training code, skill libraries, harnesses, planning domains, hardware and tools; keeps "
     "or reverts by its own trials."),
    ("run", "Controller", "orchestrator", "Controller · Orchestrators",
     "Decides at each step by planning and calling skills, tools or VLAs-as-tools."),
    ("run", "Controller", "direct", "Controller · Direct drivers",
     "Writes the code, constraints or rewards executed now, or emits the actions itself."),
    ("run", "Controller", "lifelong", "Controller · Lifelong / memory agents",
     "Improves memory, skill libraries or harness across episodes while acting."),
    ("run", "Supervisor", None, "Supervisor",
     "Acts only on anomalies: failure detection, safety guardrails, recovery, asking for help."),
]
LEGEND = """**Legend.** *Carrier* — **G** general model used as-is (models the authors fine-tuned are no longer included). *Topology* — ×1 single agent, ×R role agents on one task, ×N one agent per robot, 1:N one decider for many robots, ×O agents owning branches of a campaign. *Loop* — **re-decide**: the model is called again with its own decisions and their consequences; **authored**: constraints or a program written by the model read live perception and adapt while the robot acts (e.g. ReKep re-solves its keypoint constraints and backtracks when one breaks); **none**: written once (open loop, included). *Closure* — evidence the loop uses: E execution, H human."""


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
ROLE_EN = {"环境/重建": "Environments / reconstruction", "奖励/任务": "Rewards / tasks", "示范/蒸馏": "Demonstration / distillation",
           "系统/代码": "System / code", "本体/工具": "Embodiment / tools", "编排": "Orchestration", "写策略": "Policy writing",
           "直接动作": "Direct action", "监控/恢复": "Monitoring / recovery", "评测": "Evaluation"}


def more_name(r):
    a = norm_arxiv(r["arxiv"])
    t = " ".join(r["title"].split()).replace("|", "/")
    return f"[{t}](https://arxiv.org/abs/{a})" if a else t
R2S_THEMES = {"real2sim", "sim2real", "real2sim2real"}  # theme "vln" marks the VLN chapter instead
is_ma = lambda r: "多智能体" in (r.get("topic") or "")  # multi-agent chapter (user, 2026-10-09); may overlap VLN


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
    ma = [r for r in core if is_ma(r)]
    # The "More papers" sections: every paper of data/core/paper_list.csv (judged from full text) that is kept or a
    # resource but not in the curated tables above.
    lp = os.path.join(ROOT, "data/core/paper_list.csv")
    plist = list(csv.DictReader(open(lp, encoding="utf-8-sig"))) if os.path.exists(lp) else []
    curated = {r["key"] for r in rows} | {norm_arxiv(r["arxiv"]) for r in rows if r["arxiv"]}
    more = [r for r in plist if r["verdict"] in ("保留", "资源") and r["key"] not in curated
            and norm_arxiv(r["arxiv"]) not in curated]
    ext = [r for r in more if r["year"] == "2026"]
    ext_pre = [r for r in more if r["year"] != "2026"]

    def in_section(r, seat, sub):
        return not chapter(r) and not is_ma(r) and r["seat"] == seat and (sub is None or r["sub"] == sub or (
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
           "used as-is, acting as agents that make explicit decisions and are connected to a robot body — through the "
           "policy, code or plans they produce, or by acting on the environment directly. Its organizing question is when "
           "and where such an agent acts on the robot: **before execution** — designing its learning problem, teaching it, "
           "or developing its system — or **at runtime** — controlling it or supervising it (**Seat**).*", "",
           "**Thesis (draft, under revision).** *Agency spreads around the body: general models, not embodied action "
           "models, fill seat after seat.*", "",
           f"Each seat is traced from its **{len(pio)} pioneers (2022–2025)** to **{len(core)} papers from 2026**, the year "
           f"most of the field's papers appeared; VLN / embodied navigation ({len(vln)} from 2026) and multi-agent systems "
           f"({len(ma)} from 2026) have their own chapters and "
           f"the Real2Sim / Sim2Real sub-direction a short section ({len(r2s)}), plus **{len(res)} benchmarks and resources**. "
           "Definition and inclusion rules: [docs/definition.md](docs/definition.md); the judged list with evidence: "
           "[docs/paper_list.md](docs/paper_list.md) (both in Chinese).", "",
           "## Scope and what counts as an agent", "",
           "**Scope.** General-purpose foundation models (LLMs / VLMs such as GPT, Gemini, Claude, Qwen-VL, GPT-6 Astra) "
           "doing embodied work as agents. They may plan, call skills, tools or VLAs, write code or constraints, or emit "
           "actions directly (LLM-as-policy, e.g. GPT-6 Astra evaluated as a robot policy on RoboDojo). The agent must be "
           "a general model used as-is: a model the authors trained or fine-tuned does not count; trained VLAs, skills "
           "and perception models appear only as tools the agent calls, and a general agent's own experience may be "
           "distilled into a smaller model (e.g. GUAVA). "
           "**Embodied foundation models that produce actions are not included** — VLAs (also with reasoning, memory or "
           "self-correction), hierarchical VLAs, world action models, robot foundation models (π0.5, ECoT, OneTwoVLA, "
           "Hi Robot, Gemini Robotics, PaLM-E); they appear here only as tools called by an agent.", "",
           "**Inclusion** (every paper judged from its full text): (1) a **general model used as-is** is the agent and "
           "plays a real role — models the authors trained, fine-tuned or distilled do not count; (2) the agent is "
           "**connected** to the policy / code layer or to the environment — closing the loop is recorded, not required "
           "(*Loop* = re-decide, authored, or none); (3) at a glance the paper is **about the agent** — datasets, "
           "data-generation platforms and asset pipelines with an LLM inside are not included, benchmarks of general "
           "agents are listed as resources; (4) general models, not embodied foundation models.", "",
           "Environments: real robots, physics simulators and discrete embodied simulators (ALFRED, VirtualHome, R2R "
           "navigation graphs) count; pure text worlds and autonomous driving do not. Also not included: scalar "
           "reward/value models, one-shot annotators, world-model foresight, purely digital agents.", "",
           "## Seat by period", "",
           "| Phase | Seat | Pioneers 2022–2025 | 2026 |", "|---|---|---|---|"]
    for ph_, s_ in (("pre-execution", "Designer"), ("pre-execution", "Teacher"), ("pre-execution", "Developer"),
                    ("runtime", "Controller"), ("runtime", "Supervisor")):
        n_p = sum(1 for r in pio if r["seat"] == s_)
        n_c = sum(1 for r in core if r["seat"] == s_)
        out.append(f"| {ph_} | {s_} | {n_p} | {n_c} |")
    out += ["", "Counts include the papers of the Real2Sim / Sim2Real, VLN and multi-agent chapters under their seats.", "",
            LEGEND, "", "## Contents", ""]
    anchor = lambda t: "#" + re.sub(r"[^a-z0-9 -]", "", t.lower()).replace(" ", "-")
    last = None
    for ph, _, _, title, _ in SECTIONS:
        if ph != last:
            out.append(f"- [{PHASES[ph][0]}]({anchor(PHASES[ph][0])})")
            last = ph
        out.append(f"  - [{title}]({anchor(title)})")
    out += ["- [Sub-direction: Real2Sim / Sim2Real](#sub-direction-real2sim--sim2real)",
            "- [VLN and embodied navigation](#vln-and-embodied-navigation)",
            "- [Multi-agent systems](#multi-agent-systems)",
            "- [Benchmarks and resources](#benchmarks-and-resources)"]
    if ext:
        out.append(f"- [More 2026 papers ({len(ext)})](#more-2026-papers)")
    if ext_pre:
        out.append(f"- [More papers from 2022–2025 ({len(ext_pre)})](#more-papers-from-20222025)")
    out.append("")
    last = None
    for ph, seat, sub, title, desc in SECTIONS:
        if ph != last:
            out += [f"## {PHASES[ph][0]}", "", PHASES[ph][1], ""]
            last = ph
        out += [f"### {title}", "", desc, ""] + lineage([r for r in pio if in_section(r, seat, sub)],
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
    out += ["## Multi-agent systems", "",
            "Systems where multiple agents are the point: general-model agents that allocate, plan or coordinate the "
            "work of two or more robots (including heterogeneous teams such as drones with ground robots), or a team "
            "of general-model agents with distinct roles that talk, debate or hand work to each other. A single robot "
            "driven by a pipeline of prompted calls is not listed here. Seats are kept; multi-agent navigation papers "
            "also appear in the VLN chapter.", ""] + \
           lineage([r for r in pio if is_ma(r)], ma, seat_head, seat_row_md)
    ma_res = [r for r in res if is_ma(r)]
    if ma_res:
        out += [f"Multi-agent benchmarks (listed under *Benchmarks and resources*): "
                + ", ".join(f"**{r['key']}**" for r in sorted(ma_res, key=sort_key)) + ".", ""]
    ma_more = sorted([r for r in more if is_ma(r) and r["verdict"] == "保留"], key=lambda r: (r["year"], r["key"].lower()))
    if ma_more:
        out += [f"<details><summary><b>More multi-agent papers</b> ({len(ma_more)})</summary>", "",
                "| Paper | Year | Seat · role |", "|---|---|---|"]
        out += [f"| {more_name(r)} | {r['year']} | {r['seat']} · {ROLE_EN.get(r['role'], r['role'])} |" for r in ma_more]
        out += ["", "</details>", ""]
    out += ["## Benchmarks and resources", "",
            "| Name | Paper | Year | Venue | Evaluated seat | Body |", "|---|---|---|---|---|---|"]
    for r in sorted(res, key=sort_key):
        a = norm_arxiv(r["arxiv"])
        m = meta.get(a, {})
        title = m.get("arxiv_title") or r["title"]
        pj, cd = links(r, m)
        out.append(f"| **{r['key']}** | [{title}](https://arxiv.org/abs/{a}){pj}{cd} | {(m.get('published') or r.get('date') or '')[:4]} | "
                   f"{venue_of(r, m)} | {r['seat']} | {r['body']} |")
    for xs_all, head_, what in ((ext, "More 2026 papers", "2026 papers"),
                                (ext_pre, "More papers from 2022–2025", "papers from 2022–2025")):
        if not xs_all:
            continue
        out += ["", f"## {head_}", "",
                f"{len(xs_all)} further {what} that meet the definition but are not in the curated tables above. Each was "
                "judged from its full text (a first pass, then a verification pass by a stronger model; papers off arXiv "
                "without an open-access PDF were judged from the abstract); the reasons and quotes are in "
                "[docs/paper_list.md](docs/paper_list.md). `MA` marks the multi-agent chapter.", ""]
        for seat in ["Designer", "Teacher", "Developer", "Controller", "Supervisor"]:
            for role in [x for x in ROLE_EN if x != "评测"]:
                xs = [r for r in xs_all if r["verdict"] == "保留" and r["seat"] == seat and r["role"] == role]
                if not xs:
                    continue
                out += [f"<details><summary><b>{seat} · {ROLE_EN[role]}</b> ({len(xs)})</summary>", "",
                        "| Paper | Year | Decision model |", "|---|---|---|"]
                for r in sorted(xs, key=lambda r: (r["year"], r["key"].lower())):
                    out.append(f"| {more_name(r)}{' `MA`' if is_ma(r) else ''} | {r['year']} | "
                               f"{r['decision_model'][:80].replace('|', '/')} |")
                out += ["", "</details>", ""]
        xs = [r for r in xs_all if r["verdict"] == "资源"]
        if xs:
            out += [f"<details><summary><b>Benchmarks and evaluation studies</b> ({len(xs)})</summary>", "",
                    "| Paper | Year | Evaluated seat |", "|---|---|---|"]
            out += [f"| {more_name(r)} | {r['year']} | {r['seat']} |" for r in sorted(xs, key=lambda r: (r["year"], r["key"].lower()))]
            out += ["", "</details>", ""]
    out += ["", "---", "", "Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.", ""]
    open(os.path.join(ROOT, "README.md"), "w").write("\n".join(out))
    print(f"README.md: 2026 {len(core)} (real2sim {len(r2s)}, vln {len(vln)}, multi-agent {len(ma)}), pioneers {len(pio)}, "
          f"resources {len(res)}, "
          f"more-2026 {len(ext)}, more-2022-2025 {len(ext_pre)}")


if __name__ == "__main__":
    main()
