#!/usr/bin/env python3
"""Five-page illustrated summary of the paper list (Chinese): docs/list_summary.pdf.

Built only on the user's framework (docs/agent_loop_framework.png and the three layers L1 / L2 / L3), not on the
old Seat definition. Every number comes from data/core/layer_classification.csv, except the verdict history
(VERSIONS below, from HANDOFF.md) and the size of the remaining work (from the extended lists and fine_labels.csv).
  1 the framework and the list at a glance     2 what counts: the six rules, and how the list tightened
  3 the three layers, pioneers -> 2026          4 what the list shows (layers and decision models over time)
  5 settled cases and what is left to do
Fonts, SVG helpers and printing are shared with scripts/build_report.py.

Usage: python3 scripts/build_list_summary.py [--out docs/list_summary.pdf] [--html <keep the html here>]
"""
import argparse, csv, os, re, subprocess, sys, tempfile
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_report as R  # noqa: E402

esc, T, svg, tint, text_w = R.esc, R.T, R.svg, R.tint, R.text_w
INK, INK2, MUTED, GRID, BASE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
# Layer colours: categorical slots 1-3 of the dataviz reference palette, validated all-pairs on the light surface
# (worst CVD dE 9.2, normal-vision 24.0); aqua is below 3:1, so every mark carries a text label in ink.
LC = {"L1": "#2a78d6", "L2": "#eb6834", "L3": "#1baf7a"}
LNAME = {"L1": "准备层", "L2": "中间层", "L3": "执行层"}
LQUOTE = {"L1": "给机器人创造环境，重建，设计 reward（developer 和 designer），pre-execution（preparation）",
          "L2": "可以是 policy 的生产者（CaP），蒸馏（experience transfer）；LLM 不直接控制 robot，隔了一层（harness）；"
                "runtime monitor（介于中间，exception）",
          "L3": "General LLM as policy（during execution）"}
SUBS = [("L1", "环境/重建", "生成或重建环境、场景、仿真资产与数字孪生"),
        ("L1", "奖励/任务", "设计奖励、成功判据、任务与课程"),
        ("L1", "本体/工具", "设计机器人形态、硬件或工具"),
        ("L1", "系统/代码", "改训练代码、技能库或 harness，按试验保留或回滚"),
        ("L2", "策略生产者", "写出在机器人上运行的策略代码或约束"),
        ("L2", "编排者", "规划并调用技能、工具、运动规划器或 VLA"),
        ("L2", "经验迁移", "agent 自己执行，经验蒸馏成策略或小模型"),
        ("L2", "运行时监控", "只在异常时介入：检测失败、护栏、恢复、求助"),
        ("L3", "直接动作", "通用大模型在执行中自己输出动作")]
# Representative papers per subtype (keys of the CSV): pioneers 2022-2025, then 2026; the rest shows as "+N".
REPS = {"环境/重建": (["RoboGen", "Eurekaverse", "Video2Policy"],
                     ["EmbodiedSmith", "Agentic Real2Sim", "SceneSmith", "SAGE", "CoDimRecon"]),
        "奖励/任务": (["Eureka", "Language to Rewards", "Text2Reward", "GenSim", "OMNI-EPIC"],
                     ["RDA", "RF-Agent", "ROOT", "FIND"]),
        "本体/工具": (["RoboMorph", "RobotSmith", "VLMgineer"], ["LACE-CRAFT", "Continuum Robot Design"]),
        "系统/代码": (["LRLL"], ["ENPIRE", "RPG", "SimEX", "PhysEvo", "HARBOR", "Zetta", "Skill2Real"]),
        "策略生产者": (["Code as Policies", "VoxPoser", "ReKep", "CoPa", "MOKA"],
                      ["Agentic RSR", "Real2Gym", "FAEA", "GTA-2", "AquaCap"]),
        "编排者": (["SayCan", "Inner Monologue", "Socratic Models", "ProgPrompt", "SayPlan", "LM-Nav"],
                   ["Harness VLA", "Thea", "Physical Agency", "RoboClaw", "NovaPlan", "Robo-COP"]),
        "经验迁移": (["SUDD", "RobotGPT"], ["GUAVA", "LocalNav", "CAPEX", "SkillWeaver"]),
        "运行时监控": (["REFLECT", "KnowNo", "Code-as-Monitor", "RoboGuard", "DoReMi"],
                      ["Agentic Task Graph", "FRAMES", "When to Act, Ask, or Learn"]),
        "直接动作": (["ZS-Planners", "Prompt a Robot to Walk", "NavGPT", "VLMnav"],
                     ["Show-Harness", "Agent as Policy", "OpenRUA", "VIA", "SpaceMind"])}
NAMED = {"GUAVA", "Harness VLA", "Show-Harness", "ENPIRE", "Code-as-Monitor", "ReKep", "RPG", "SimEX", "EmbodiedSmith",
         "Video2World", "Astra on RoboDojo"}
# How the 174-paper table tightened as the user's rules arrived (HANDOFF.md §1 and §7).
VERSIONS = [("按回路图初判", "「通用大语言模型agent必须存在，在里面扮演角色才行」", dict(keep=113, open=28, res=20, out=13)),
            ("箭头不必全有", "「agent必须要和其中部件有所连接即可，无论是环境还是policy」", dict(keep=146, res=24, out=4)),
            ("现成大模型 · 读全文", "「我说的是通用大模型，而不是被训练过的小模型」「我建议你读读内容」",
             dict(keep=144, res=20, out=10)),
            ("逐条复核", "「EmbodiedSmith不是real2sim的吗」", dict(keep=145, res=20, out=9))]
FAMILIES = [("GPT", r"gpt|chatgpt|codex|\bo1\b|\bo3|davinci|instructgpt|astra|\bsol\b|terra|luna|openai"),
            ("Claude", r"claude|opus|sonnet|haiku|fable"), ("Gemini", r"gemini|palm|gemma"), ("Qwen", r"qwen"),
            ("Llama", r"llama|vicuna"), ("其他开源", r"deepseek|kimi|glm|gpt-oss|internvl|mistral|phi")]

CSS = """
@page { size: A4; }
body { font-size: 8.8pt; line-height: 1.55; }
.page { height: 266mm; position: relative; overflow: hidden; break-after: page; }
.page:last-child { break-after: auto; }
.kicker { font-size: 7.4pt; letter-spacing: 1.8pt; color: #0b0b0b; font-weight: 700; margin-bottom: 6pt; }
.kicker span { color: #898781; font-weight: 400; letter-spacing: 0.8pt; }
.kicker i { display: inline-block; width: 7pt; height: 7pt; border-radius: 50%; margin-right: 2pt; vertical-align: 0; }
h1.title { font-size: 31pt; line-height: 1.08; margin: 0; letter-spacing: -0.5pt; }
.subtitle { font-size: 12.5pt; color: #52514e; margin: 5pt 0 4pt; }
h2 { font-size: 15pt; border: 0; padding: 0; margin: 0 0 3pt; letter-spacing: -0.2pt; }
h3 { font-size: 10pt; margin: 10pt 0 5pt; }
.lead { color: #52514e; font-size: 9pt; margin: 0 0 9pt; line-height: 1.6; }
figure { margin: 2pt 0 4pt; }
figcaption { font-size: 7.8pt; margin-top: 2pt; color: #52514e; }
.kp { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8pt; margin: 6pt 0 10pt; }
.kp > div { border-top: 2.5px solid #0b0b0b; padding-top: 4pt; }
.kp > div.dim { border-top-color: #c3c2b7; }
.kp .v { font-size: 21pt; font-weight: 700; line-height: 1.05; letter-spacing: -0.4pt; }
.kp .dim .v { color: #898781; }
.kp .l { font-size: 7.7pt; color: #52514e; line-height: 1.35; margin-top: 3pt; }
.lbar { display: flex; gap: 3px; height: 26pt; margin: 4pt 0 3pt; }
.lbar div { border-radius: 4px; color: #ffffff; font-size: 8.4pt; font-weight: 700; padding: 3pt 7pt; line-height: 1.25;
            white-space: nowrap; overflow: hidden; }
.lbar div span { display: block; font-weight: 400; font-size: 7.2pt; opacity: 0.92; }
.lbar-l3 { color: #0b0b0b !important; }
.lbarcap { display: flex; justify-content: space-between; font-size: 7.4pt; color: #898781; margin-bottom: 10pt; }
.abs3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14pt; font-size: 8.4pt; line-height: 1.62; }
.abs3 b { display: block; font-size: 9.6pt; margin-bottom: 3pt; }
.abs3 div { border-left: 2px solid #0b0b0b; padding-left: 8pt; }
.lcards { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10pt; margin-top: 14pt; }
.lcard { border-top: 4px solid var(--c); background: #fcfcfb; border-radius: 0 0 9px 9px; padding: 7pt 10pt 9pt;
         border-left: 1px solid #e1e0d9; border-right: 1px solid #e1e0d9; border-bottom: 1px solid #e1e0d9; }
.lcard .h { font-size: 11pt; font-weight: 700; }
.lcard .h span { float: right; font-size: 9pt; color: #52514e; font-weight: 500; }
.lcard .q { font-size: 7.3pt; color: #52514e; line-height: 1.45; margin: 3pt 0 6pt; min-height: 42pt; }
.lcard .it { display: flex; align-items: center; gap: 6pt; font-size: 8.4pt; margin: 3pt 0; }
.lcard .it span { width: 56pt; }
.lcard .it i { display: inline-block; height: 7pt; border-radius: 0 2px 2px 0; }
.lcard .it b { font-size: 8.6pt; }
.rules { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8pt; }
.rule { border: 1px solid #e1e0d9; border-radius: 9px; padding: 8pt 9pt 8pt; background: #fcfcfb; }
.rule .n { display: inline-block; width: 16pt; height: 16pt; border-radius: 50%; background: #0b0b0b; color: #fff;
           text-align: center; line-height: 16pt; font-size: 8pt; font-weight: 700; margin-right: 5pt; }
.rule h4 { display: inline; font-size: 10pt; margin: 0; }
.rule .q { font-size: 8pt; color: #0b0b0b; margin: 6pt 0 5pt; padding: 3pt 0 3pt 7pt; border-left: 2px solid #c3c2b7;
           line-height: 1.45; min-height: 30pt; }
.rule .q .src { display: block; font-size: 6.8pt; color: #898781; margin-top: 1pt; }
.rule .d { font-size: 7.6pt; color: #52514e; line-height: 1.45; margin-bottom: 4pt; min-height: 33pt; }
.rule .ok, .rule .ng { font-size: 7.4pt; line-height: 1.42; margin-top: 2pt; padding-left: 11pt; text-indent: -11pt; }
.rule .ng { color: #898781; }
.steps { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0; margin: 4pt 0 2pt; }
.steps div { font-size: 7.6pt; color: #52514e; line-height: 1.4; padding: 0 8pt 0 0; }
.steps b { display: block; font-size: 12pt; color: #0b0b0b; line-height: 1.2; }
.map { width: 100%; table-layout: fixed; border-collapse: separate; border-spacing: 0; font-size: 7.4pt; }
.map th { text-align: left; font-weight: 700; font-size: 8pt; color: #0b0b0b; padding: 0 5pt 4pt; border-bottom: 1.5px solid #0b0b0b; }
.map th span { font-weight: 400; color: #898781; font-size: 7pt; margin-left: 3pt; }
.map td { vertical-align: top; padding: 4pt 5pt 3.5pt; border-bottom: 1px solid #e1e0d9; }
.map td.c26 { background: #fafaf8; }
.map tr.lh td { background: var(--t); border-bottom: 0; padding: 6pt 8pt 5pt; border-radius: 0; }
.map tr.lh .ln { font-size: 11pt; font-weight: 700; color: #0b0b0b; margin-right: 6pt; }
.map tr.lh .ln i { display: inline-block; width: 9pt; height: 9pt; border-radius: 2px; background: var(--c); margin-right: 5pt;
                   vertical-align: -0.5pt; }
.map tr.lh .lq { font-size: 7.6pt; color: #52514e; }
.map tr.lh .lc { float: right; font-size: 8pt; color: #0b0b0b; font-weight: 700; }
.map .sn { font-size: 8.8pt; font-weight: 700; color: #0b0b0b; display: block; }
.map .sd { font-size: 7pt; color: #52514e; display: block; line-height: 1.35; margin: 1pt 0 3pt; }
.mini { display: flex; height: 5pt; gap: 1.5px; margin-top: 2pt; }
.mini span { border-radius: 1.5px; }
.mini-n { font-size: 6.8pt; color: #52514e; margin-top: 2pt; }
.chip { display: inline-block; font-size: 7.1pt; line-height: 1.3; padding: 1pt 4.5pt 1pt 4pt; margin: 1.2pt 2pt 1.2pt 0;
        border-radius: 3px; background: var(--t); border-left: 2.5px solid var(--c); color: #0b0b0b; white-space: nowrap; }
.chip.pio { background: #ffffff; box-shadow: inset 0 0 0 1px #e1e0d9; }
.more { font-size: 6.9pt; color: #898781; margin-left: 2pt; white-space: nowrap; }
.legend { font-size: 7.3pt; color: #52514e; margin: 5pt 0 0; }
.sq { display: inline-block; width: 8pt; height: 8pt; border-radius: 2px; margin-right: 3pt; vertical-align: -1pt; }
.two { display: grid; grid-template-columns: 1.15fr 1fr; gap: 16pt; }
.chart h4 { font-size: 9.6pt; margin: 0 0 1pt; }
.chart .s { font-size: 7.5pt; color: #52514e; margin-bottom: 4pt; line-height: 1.4; }
.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8pt; margin: 4pt 0 10pt; }
.tile { border-radius: 9px; background: #f4f3ef; padding: 7pt 10pt 8pt; }
.tile .v { font-size: 19pt; font-weight: 700; line-height: 1.1; letter-spacing: -0.3pt; }
.tile .v span { color: #898781; font-weight: 400; font-size: 12pt; margin: 0 3pt; }
.tile .l { font-size: 7.9pt; font-weight: 700; margin-top: 3pt; }
.tile .s { font-size: 7.3pt; color: #52514e; line-height: 1.4; }
.reads { display: grid; grid-template-columns: 1fr 1fr; gap: 9pt 16pt; margin-top: 12pt; }
.reads div { font-size: 8.3pt; line-height: 1.6; color: #52514e; border-left: 3px solid var(--c, #0b0b0b); padding: 1pt 0 1pt 8pt; }
.reads b { display: block; color: #0b0b0b; font-size: 9pt; margin-bottom: 1pt; }
.caveat { font-size: 7.3pt; color: #898781; margin-top: 8pt; }
.cases { width: 100%; border-collapse: collapse; font-size: 7.6pt; table-layout: fixed; }
.cases td { padding: 3.2pt 5pt 3.2pt 0; border-bottom: 1px solid #e1e0d9; vertical-align: top; line-height: 1.42; }
.cases td.k { font-weight: 700; color: #0b0b0b; width: 27%; }
.cases td.r { color: #52514e; }
.cases td.t { width: 14%; }
.tag { display: inline-block; font-size: 6.8pt; border-radius: 3px; padding: 0 4pt; line-height: 1.5; }
.tag.out { background: #e1e0d9; color: #52514e; }
.tag.keep { background: #0b0b0b; color: #ffffff; }
.tag.l { color: #0b0b0b; background: var(--t); border-left: 2.5px solid var(--c); }
.colh { font-size: 9.6pt; font-weight: 700; margin: 0 0 4pt; }
.colh span { font-size: 7.4pt; color: #898781; font-weight: 400; margin-left: 4pt; }
.next { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 9pt; margin-top: 6pt; }
.nx { border-radius: 9px; padding: 8pt 10pt 9pt; border: 1px solid #e1e0d9; background: #fcfcfb; }
.nx .k { font-size: 7pt; letter-spacing: 1pt; color: #898781; font-weight: 700; }
.nx h4 { font-size: 9.6pt; margin: 1pt 0 3pt; }
.nx p, .nx li { font-size: 7.8pt; color: #52514e; line-height: 1.5; margin: 0; }
.nx ul { padding-left: 11pt; margin: 0; }
.files { margin-top: 10pt; border-top: 1.5px solid #0b0b0b; padding-top: 6pt; display: grid;
         grid-template-columns: 1.25fr 1fr 1fr; gap: 12pt; font-size: 7.6pt; color: #52514e; line-height: 1.5; }
.files b { color: #0b0b0b; display: block; font-size: 8pt; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 7pt; color: #0b0b0b; }
"""


def load():
    rows = list(csv.DictReader(open(os.path.join(R.ROOT, "data/core/layer_classification.csv"), encoding="utf-8-sig")))
    return rows, {r["key"]: r for r in rows}


def chip(key, layer, pio=False):
    c = LC[layer]
    star = " ★" if key in NAMED else ""
    return f'<span class="chip{" pio" if pio else ""}" style="--c:{c};--t:{tint(c, 0.12)}">{esc(key)}{star}</span>'


def fig_loop():
    """The user's agent-loop diagram, redrawn with the three layers marked on it."""
    W, H = 680, 268
    l1, l2, l3 = LC["L1"], LC["L2"], LC["L3"]
    b = [f'<defs><marker id="am" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" '
         f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
         + "".join(f'<marker id="a{n}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6.5" markerHeight="6.5" '
                   f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
                   for n, c in (("1", l1), ("2", l2), ("3", l3), ("g", MUTED))) + '</defs>']
    # top arc: agent acts on Env / Sim directly (L1, before execution)
    b.append(f'<path d="M100,92 C100,18 580,18 580,90" fill="none" stroke="{l1}" stroke-width="2.2" marker-end="url(#a1)"/>')
    b.append(f'<rect x="196" y="16" width="288" height="36" rx="18" fill="#ffffff" stroke="{l1}" stroke-width="1.2"/>')
    b.append(T(214, 31, "L1 准备层", 9.6, 700, INK) + T(214, 44, "执行前作用于环境与训练：造环境、设奖励、改系统", 8.2, 400, INK2))
    # bottom arc: information flows back (optional)
    b.append(f'<path d="M580,200 C580,262 100,262 100,202" fill="none" stroke="{MUTED}" stroke-width="1.6" '
             f'stroke-dasharray="5 4" marker-end="url(#ag)"/>')
    b.append(f'<rect x="170" y="236" width="340" height="20" rx="10" fill="#ffffff"/>')
    b.append(T(340, 250, "Env / Sim 的信息回到 agent —— 可以有，不是必须（开环也算）", 8.6, 500, INK2, "middle"))
    # boxes
    b.append(f'<rect x="20" y="92" width="160" height="108" rx="12" fill="{INK}"/>')
    b.append(T(36, 122, "Agent", 17, 700, "#ffffff") + T(36, 142, "现成的通用大模型", 9.6, 500, "#ffffff")
             + T(36, 158, "GPT · Claude · Gemini · Qwen", 8, 400, "#c3c2b7")
             + T(36, 184, "必须在场，必须起作用", 8.2, 700, "#9ec5f4"))
    b.append(f'<rect x="500" y="92" width="160" height="108" rx="12" fill="#f4f3ef" stroke="{BASE}"/>')
    b.append(T(516, 122, "Env / Sim", 17, 700, INK) + T(516, 142, "机器人 · 真实环境 · 仿真", 9.6, 500, INK2)
             + T(516, 158, "操作、导航、人形、无人机……", 8, 400, MUTED))
    b.append(f'<rect x="262" y="78" width="156" height="62" rx="10" fill="{tint(l2, 0.12)}" stroke="{l2}" stroke-width="1.4"/>')
    b.append(T(276, 98, "L2 中间层", 8.2, 700, INK) + T(276, 116, "Policy / Code", 12.5, 700, INK)
             + T(276, 131, "写策略 · 编排 · 蒸馏 · 监控", 7.8, 400, INK2))
    b.append(f'<rect x="262" y="152" width="156" height="50" rx="10" fill="#ffffff" stroke="{l3}" stroke-width="1.4" '
             f'stroke-dasharray="4 3"/>')
    b.append(T(276, 170, "L3 执行层", 8.2, 700, INK) + T(276, 188, "None", 12.5, 700, INK)
             + T(318, 188, "大模型自己出动作", 7.8, 400, INK2))
    # arrows through the middle
    for d, m, c in (("M180,122 L259,108", "a2", l2), ("M418,108 L497,122", "a2", l2),
                    ("M180,170 L259,177", "a3", l3), ("M418,177 L497,170", "a3", l3)):
        b.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2" marker-end="url(#{m})"/>')
    return svg(W, H, "".join(b), "agent 回路框架：Agent 经 Policy/Code 或 None 作用于 Env/Sim，也可以直接作用；信息可回到 agent")


def wrap(s, size, width):
    """Break a mixed CJK / Latin string into lines no wider than width (rough glyph widths)."""
    out, cur = [], ""
    for tok in re.findall(r"[A-Za-z0-9.+\-/]+ ?|.", s):
        if cur and text_w(cur + tok, size) > width:
            out.append(cur.rstrip())
            cur = tok.lstrip()
        else:
            cur += tok
    return out + ([cur.rstrip()] if cur.strip() else [])


def fig_versions():
    W, rowh, top, left = 680, 48, 4, 236
    span = W - left - 6
    fill = {"keep": INK, "open": "#ffffff", "res": "#898781", "out": "#e1e0d9"}
    lab = {"keep": "保留", "open": "待定·开环", "res": "资源", "out": "剔除"}
    b = []
    for k, (name, quote, v) in enumerate(VERSIONS):
        y = top + k * rowh
        b.append(f'<circle cx="7" cy="{y + 9}" r="7" fill="{INK}"/>' + T(7, y + 12.5, str(k + 1), 8.4, 700, "#ffffff", "middle"))
        b.append(T(20, y + 13, name, 9.6, 700, INK))
        for j, ln in enumerate(wrap(quote, 7.6, left - 34)[:2]):
            b.append(T(20, y + 27 + 11 * j, ln, 7.6, 400, MUTED))
        x = left
        for key in ("keep", "open", "res", "out"):
            n = v.get(key, 0)
            if not n:
                continue
            w = span * n / 174 - 2
            dash = ' stroke-dasharray="3 2"' if key == "open" else ""
            b.append(f'<rect x="{x:.1f}" y="{y + 3}" width="{w:.1f}" height="28" rx="4" fill="{fill[key]}" '
                     f'stroke="{INK2 if key == "open" else fill[key]}" stroke-width="1"{dash}/>')
            txt = f"{lab[key]} {n}" if w > 66 else str(n)
            col = "#ffffff" if key in ("keep", "res") else INK
            if w > 14:
                b.append(T(x + 7, y + 21, txt, 8.8 if key == "keep" else 8.2, 700, col))
            x += w + 2
    return svg(W, top + rowh * len(VERSIONS) - 8, "".join(b), "174 篇核心表在四次规则调整后的结论变化")


def fig_todo(todo):
    """Remaining papers per source: with an arXiv id (ink) and without (grey), totals at the end."""
    W, label_w, rowh = 372, 118, 30
    span = W - label_w - 40
    mx = max(len(xs) for _, xs in todo)
    b = []
    for k, (name, xs) in enumerate(todo):
        y = 4 + k * rowh
        has = sum(1 for x in xs if x.get("arxiv"))
        b.append(T(label_w - 10, y + 15, name, 8.6, 500, INK, "end"))
        w1, w2 = span * has / mx, span * (len(xs) - has) / mx
        b.append(f'<rect x="{label_w}" y="{y + 2}" width="{w1 - 1.5:.1f}" height="18" rx="3" fill="{INK}"/>')
        b.append(T(label_w + 5, y + 15, f"arXiv {has}", 7.6, 700, "#ffffff"))
        b.append(f'<rect x="{label_w + w1:.1f}" y="{y + 2}" width="{w2:.1f}" height="18" rx="3" fill="{BASE}"/>')
        if w2 > 34:
            b.append(T(label_w + w1 + 5, y + 15, f"无 {len(xs) - has}", 7.6, 500, INK))
        b.append(T(label_w + w1 + w2 + 5, y + 15, f"{len(xs)}", 8.6, 700, INK))
    return svg(W, 4 + rowh * len(todo), "".join(b), "待补判论文：有无 arXiv 号")


def hbars(rows, maxv, label_w=104, W=380, rowh=21, unit="篇"):
    """rows: (label, layer colour or None, [(value, fill, text)]). Stacked horizontal bars with direct labels."""
    b, y = [], 4
    span = W - label_w - 34
    for lab, c, segs in rows:
        if lab is None:  # group header
            b.append(T(0, y + 12, segs, 8.2, 700, INK))
            y += 17
            continue
        b.append(T(label_w - 8, y + 11, lab, 8.4, 500, INK, "end"))
        x, tot = label_w, 0
        for v, f, _ in segs:
            if v:
                w = max(span * v / maxv - 1.5, 1.5)
                b.append(f'<rect x="{x:.1f}" y="{y + 2}" width="{w:.1f}" height="12" rx="2" fill="{f}"/>')
                x += w + 1.5
            tot += v
        txt = " + ".join(t for v, _, t in segs if v) if len([s for s in segs if s[0]]) > 1 else ""
        b.append(T(x + 4, y + 11, f"{tot}" + (f"（{txt}）" if txt else ""), 7.8, 500, INK2))
        y += rowh
    return svg(W, y + 2, "".join(b), "条形图")


def build_html(fontdir):
    rows, by = load()
    kept = [r for r in rows if r["verdict"] == "保留"]
    vc = Counter(r["verdict"] for r in rows)
    lc = Counter(r["layer"] for r in kept)
    tier = Counter(r["tier"] for r in kept)
    sub = defaultdict(Counter)
    for r in kept:
        sub[r["subtype"]][r["tier"]] += 1
    fam = {t: Counter() for t in ("先驱", "2026")}
    for r in kept:
        hits = {n for n, p in FAMILIES if re.search(p, r["decision_model"].lower())} or {"未写明"}
        for h in hits:
            fam[r["tier"]][h] += 1
    pct = lambda t, f: 100 * fam[t][f] / tier[t]
    # remaining work (HANDOFF.md §4.1)
    ext = {n: list(csv.DictReader(open(os.path.join(R.ROOT, "data/core", n)))) for n in
           ("extended_2026.csv", "extended_2022_2025.csv")}
    strong = R.STRONG
    bnd = [r for r in csv.DictReader(open(os.path.join(R.ROOT, "data/core/fine_labels.csv")))
           if r["verdict"] == "boundary" and r["pass"] in strong]
    todo = [("2026 · 旧定义合格", ext["extended_2026.csv"]), ("2022–2025 · 旧定义合格", ext["extended_2022_2025.csv"]),
            ("旧定义的边界论文", bnd)]
    n_todo = sum(len(x) for _, x in todo)
    H = []
    a = H.append

    # ---------------------------------------------------------------- page 1
    a('<section class="page">')
    a('<div class="kicker">AGENTIC EMBODIMENT <span>· 论文清单 · 2026 年 10 月</span></div>')
    a('<h1 class="title">通用大模型，<br>在机器人回路里的位置</h1>')
    a('<div class="subtitle">按我们的框架整理的论文清单：谁在做决策、它连到哪里、属于哪一层</div>')
    a(f'<figure>{fig_loop()}</figure>')
    kp = [(f"{len(rows)}", "篇逐篇读全文判定", ""), (f"{vc['保留']}", f"篇保留<br>先驱 {tier['先驱']} · 2026 年 {tier['2026']}", ""),
          (f"{vc['资源']}", "个 benchmark<br>与评测研究", ""), (f"{vc['剔除']}", "篇剔除<br>理由与原文证据见 CSV", ""),
          (f"{n_todo:,}", "篇候选待按同一<br>标准补判", "dim")]
    a('<div class="kp">' + "".join(f'<div class="{c}"><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l, c in kp)
      + '</div>')
    tot = sum(lc.values())
    segs = "".join(
        f'<div class="{"lbar-l3" if ly == "L3" else ""}" style="flex:{lc[ly]};background:{LC[ly]}">'
        f'{ly + " " + LNAME[ly] + " · " if ly != "L3" else "L3 · "}{lc[ly]}'
        f'<span>{100 * lc[ly] / tot:.0f}%</span></div>' for ly in ("L1", "L2", "L3"))
    a(f'<div class="lbar">{segs}</div>')
    a('<div class="lbarcap"><span>保留的 145 篇按层分布</span><span>L1 准备层：执行前 · L2 中间层：隔着一层 · L3 执行层：自己出动作</span></div>')
    a('<div class="abs3">'
      '<div><b>这是什么</b>一份 agentic embodiment 论文清单：现成的通用大模型作为 agent，经由 Policy / Code，'
      '或直接作用于环境，参与机器人任务。按你的框架分成 L1 准备层、L2 中间层、L3 执行层，共九个子类。</div>'
      '<div><b>怎么判的</b>六条标准（第 2 页）都来自你的原话。每篇都读了全文的方法与实验部分，记下谁在做决策、'
      '是否被作者训练过、论文主体是不是 agent，并摘出原文证据；与旧版不同的逐条写了备注。</div>'
      f'<div><b>还差什么</b>这 {len(rows)} 篇来自旧定义下挑出的核心表。另有约 {n_todo:,} 篇候选只按旧定义判过，'
      '要用同一套标准补判，清单才算完整；其中边界论文先要定下离散仿真和自动驾驶算不算。</div></div>')
    cards = []
    for ly in ("L1", "L2", "L3"):
        c = LC[ly]
        items = "".join(
            f'<div class="it"><span>{s_}</span><i style="width:{3.2 * sum(sub[s_].values()):.0f}px;background:{c}"></i>'
            f'<b>{sum(sub[s_].values())}</b></div>' for l_, s_, _ in SUBS if l_ == ly)
        cards.append(f'<div class="lcard" style="--c:{c}"><div class="h">{ly} {LNAME[ly]}<span>{lc[ly]} 篇</span></div>'
                     f'<div class="q">「{esc(LQUOTE[ly])}」</div>{items}</div>')
    a('<div class="lcards">' + "".join(cards) + '</div>')
    a('</section>')

    # ---------------------------------------------------------------- page 2
    a('<section class="page">')
    a('<div class="kicker">01 <span>· 什么算</span></div>')
    a('<h2>六条标准，全部来自你的原话</h2>')
    a('<p class="lead">前四条决定一篇论文进不进清单，第五条划定范围，第六条规定怎么判。'
      '每条都附一个保留的例子和一个剔除的例子。</p>')
    rules = [("通用大模型 agent 必须在场", "通用大语言模型agent必须存在，在里面扮演角色才行",
              "agent 要真正做决策：写计划、写代码或约束、调用技能或 VLA、设计环境，或者直接出动作。",
              "SayCan：LLM 选择技能", "RoboFind：决策回路是 VLA 导航加阈值验证"),
             ("现成的，不是训练过的", "我说的是通用大模型，而不是被训练过的小模型",
              "作者训练、微调、蒸馏出的模型不算 agent；训练过的 VLA、技能只能当工具。通用模型自己执行、再蒸馏经验的算 L2。",
              "GUAVA：前沿 VLM 当 agent，轨迹再蒸馏", "RoboFAC、AgentVLN、Ludi：微调的 Qwen"),
             ("连上就算，箭头不必全有", "agent必须要和其中部件有所连接即可，无论是环境还是policy",
              "连到 Policy / Code 或 Env / Sim 之一即可；环境信息回不回到 agent 只记录，不作门槛。",
              "Code as Policies、ReKep：一次写成也算", "LM-Nav 一类曾因开环被误删，已恢复"),
             ("一眼看上去要是在讲 agent", "robotwin一眼看上去就不是agent",
              "主体是数据集、数据平台、资产流水线或 benchmark，LLM 只是其中一个模块的，不收；评测通用 agent 的归资源。",
              "EmbodiedSmith：主体是 agent 循环", "RoboTwin 2.0、HumanoidGen：数据生成器"),
             ("不是具身大模型", "研究对象是通用大模型做具身任务",
              "VLA、分层 VLA、WAM、机器人基础模型做决策的不收；它们只作为 agent 调用的工具出现。",
              "Harness VLA：coding agent 调度冻结的 VLA", "VLABench：评测对象是 VLA"),
             ("读内容，不看标题", "我建议你读读内容",
              "每篇读全文的方法与实验设置，写明决策模型、是否经过训练、论文主体，并摘一句原文为证。",
              "174 篇全部附原文证据", "只看摘要曾把 RoboFAC 当成 agent")]
    parts = []
    for k, (h, q, d, ok, ng) in enumerate(rules):
        src = "范围（第三轮确定）" if k == 4 else "你的原话"
        parts.append(f'<div class="rule"><span class="n">{k + 1}</span><h4>{esc(h)}</h4>'
                     f'<div class="q">「{esc(q)}」<span class="src">{src}</span></div><div class="d">{esc(d)}</div>'
                     f'<div class="ok">✓ {esc(ok)}</div><div class="ng">✗ {esc(ng)}</div></div>')
    a('<div class="rules">' + "".join(parts) + '</div>')
    a('<h3 style="margin-top:14pt">清单是怎么一步步收紧的</h3>')
    a('<p class="lead" style="margin-bottom:5pt">同一批 174 篇，在你每补一条标准之后重判一次。'
      '「开环」那一批先被单独拿出来，第二步确认开环也算后全部归位；第三步按「现成大模型」与读全文改判了 15 篇。</p>')
    a(f'<figure>{fig_versions()}</figure>')
    a('<div class="legend" style="margin:0 0 8pt">'
      '<span class="sq" style="background:#0b0b0b"></span>保留　'
      '<span class="sq" style="background:#fff;border:1px dashed #52514e"></span>待定·开环（第一步单独拿出，第二步归入保留）　'
      '<span class="sq" style="background:#898781"></span>资源　<span class="sq" style="background:#e1e0d9"></span>剔除</div>')
    a('<div class="steps">'
      f'<div><b>{len(rows)} 篇</b>arXiv 全文下载为文本</div>'
      '<div><b>18 个分片</b>每片 10 篇，子 agent 逐篇读方法与实验设置</div>'
      '<div><b>4 个字段</b>决策模型 · 是否训练 · 论文主体 · 原文证据</div>'
      '<div><b>人工复核</b>改判逐条写入备注；EmbodiedSmith 经你追问后恢复</div></div>')
    a('</section>')

    # ---------------------------------------------------------------- page 3
    a('<section class="page">')
    a('<div class="kicker">02 <span>· 三层九类</span></div>')
    a('<h2>从先驱到 2026：每一层的代表作</h2>')
    a(f'<p class="lead">左列是子类、定义与篇数（浅色为 2022–2025 先驱，深色为 2026 年）；右边两列是代表作，其余以「+N」表示。'
      f'★ 是你点名必须收录的论文。完整的 {vc["保留"]} 篇见 CSV。</p>')
    t = ['<table class="map"><colgroup><col style="width:24%"><col style="width:36%"><col style="width:40%"></colgroup>'
         '<tr><th>子类</th><th>先驱<span>2022–2025</span></th><th>2026<span>同一位置上的新工作</span></th></tr>']
    for ly in ("L1", "L2", "L3"):
        c = LC[ly]
        n_l = lc[ly]
        t.append(f'<tr class="lh" style="--c:{c};--t:{tint(c, 0.1)}"><td colspan="3"><span class="ln"><i></i>{ly} {LNAME[ly]}</span>'
                 f'<span class="lq">「{esc(LQUOTE[ly])}」</span><span class="lc">{n_l} 篇</span></td></tr>')
        for ly2, s, d in SUBS:
            if ly2 != ly:
                continue
            p, n = sub[s]["先驱"], sub[s]["2026"]
            mx = 50
            mini = (f'<div class="mini"><span style="width:{100 * p / mx:.1f}%;background:{tint(c, 0.4)}"></span>'
                    f'<span style="width:{100 * n / mx:.1f}%;background:{c}"></span></div>'
                    f'<div class="mini-n">先驱 {p} · 2026 年 {n}</div>')
            pk, nk = REPS[s]
            assert all(k in by and by[k]["verdict"] == "保留" and by[k]["subtype"] == s for k in pk + nk), s
            mp, mn = p - len(pk), n - len(nk)
            t.append(f'<tr><td><span class="sn">{s}</span><span class="sd">{esc(d)}</span>{mini}</td>'
                     f'<td>{"".join(chip(k, ly, True) for k in pk)}{f"<span class=more>+{mp}</span>" if mp > 0 else ""}</td>'
                     f'<td class="c26">{"".join(chip(k, ly) for k in nk)}{f"<span class=more>+{mn}</span>" if mn > 0 else ""}</td></tr>')
    t.append('</table>')
    a("".join(t))
    a('<div class="legend">卡片左侧色条 = 所属层。每篇按主要贡献只归一个子类，兼有多层的（如 Real2Gym 既重建环境又写策略）'
      '归到主体所在层。</div>')
    a('</section>')

    # ---------------------------------------------------------------- page 4
    a('<section class="page">')
    a('<div class="kicker">03 <span>· 清单里看到了什么</span></div>')
    a('<h2>L2 仍是主体，2026 年 L1 与 L3 在长</h2>')
    a('<p class="lead">下面的数字来自保留的 145 篇。核心表是挑选出来的，比例只能看方向；'
      '补判完约 2,000 篇候选之后，再用全量数据确认这些趋势。</p>')
    s1, s26 = sub["系统/代码"], sub["直接动作"]
    l1p, l1n = sum(sub[s]["先驱"] for l, s, _ in SUBS if l == "L1"), sum(sub[s]["2026"] for l, s, _ in SUBS if l == "L1")
    a('<div class="tiles">'
      f'<div class="tile"><div class="v">{s1["先驱"]}<span>→</span>{s1["2026"]}</div><div class="l">L1 系统/代码，先驱 → 2026</div>'
      '<div class="s">coding agent 改训练代码、技能库与 harness，按真机试验保留或回滚</div></div>'
      f'<div class="tile"><div class="v">{100 * l1p / tier["先驱"]:.0f}%<span>→</span>{100 * l1n / tier["2026"]:.0f}%</div>'
      '<div class="l">L1 占比，先驱 → 2026</div><div class="s">执行前的准备工作越来越多交给 agent</div></div>'
      f'<div class="tile"><div class="v">{s26["先驱"]}<span>→</span>{s26["2026"]}</div><div class="l">L3 直接动作，先驱 → 2026</div>'
      '<div class="s">通用大模型直接当策略：Show-Harness、Agent as Policy</div></div>'
      f'<div class="tile"><div class="v">{pct("先驱", "GPT"):.0f}%<span>→</span>{pct("2026", "GPT"):.0f}%</div>'
      '<div class="l">用 GPT 做决策的论文</div><div class="s">2026 年 Claude、Qwen、Gemini 各占四分之一以上</div></div></div>')
    rows_a = []
    for ly in ("L1", "L2", "L3"):
        c = LC[ly]
        rows_a.append((None, None, f"{ly} {LNAME[ly]}"))
        for ly2, s, _ in SUBS:
            if ly2 == ly:
                rows_a.append((s, c, [(sub[s]["先驱"], tint(c, 0.4), f"先驱 {sub[s]['先驱']}"),
                                      (sub[s]["2026"], c, f"2026 {sub[s]['2026']}")]))
    fams = ["GPT", "Claude", "Gemini", "Qwen", "Llama", "其他开源", "未写明"]
    chart_b = hbars_pair(fams, pct)
    a('<div class="two">'
      f'<div class="chart"><h4>每个子类的篇数</h4><div class="s">浅色 = 先驱 2022–2025，深色 = 2026 年；括号内为两者之和的拆分。</div>'
      f'{hbars(rows_a, 74, label_w=62, W=292, rowh=31)}</div>'
      f'<div class="chart"><h4>谁在做决策</h4><div class="s">用到某一模型家族的论文占比（一篇可用多个模型）。'
      f'灰 = 先驱（{tier["先驱"]} 篇），黑 = 2026 年（{tier["2026"]} 篇）。</div>{chart_b}</div></div>')
    a('<div class="reads">'
      f'<div style="--c:{LC["L2"]}"><b>L2 中间层是主体（{lc["L2"]} 篇）</b>编排者最多（{sum(sub["编排者"].values())} 篇），'
      '从 SayCan 选技能、Inner Monologue 听反馈，到 2026 年调度冻结 VLA 的 Harness VLA 与 Robo-COP；策略生产者从 Code as Policies、'
      'ReKep 延续到 Agentic RSR、Real2Gym。</div>'
      f'<div style="--c:{LC["L1"]}"><b>L1 的重心从「设计奖励」移到「改系统」</b>先驱的 L1 以 Eureka 一类奖励设计为主；'
      f'2026 年系统/代码一类从 {s1["先驱"]} 篇增到 {s1["2026"]} 篇：ENPIRE、PhysEvo、RPG、SimEX 让 coding agent '
      '直接改训练代码与技能库，用试验决定去留。</div>'
      f'<div style="--c:{LC["L3"]}"><b>L3 回来了</b>早期 ZS-Planners、Prompt a Robot to Walk 让大模型直接出动作，'
      '之后多被 L2 取代；2026 年前沿模型足够强，Show-Harness、Agent as Policy、GPT-6 Astra 又开始直接当策略。</div>'
      '<div style="--c:#0b0b0b"><b>决策模型多样化</b>先驱几乎都用 GPT；2026 年 Claude、Qwen、Gemini 普遍出现，'
      f'开源的 Qwen 也能当 agent（{fam["2026"]["Qwen"]} 篇）。所有保留论文的决策者都是未经作者训练的通用模型。</div></div>')
    a('<div class="caveat">模型家族按「决策模型」一列的文字归类：GPT 含 Codex、GPT-6 Astra 与 GPT-5.6 Sol / Terra / Luna，'
      'Claude 含 Opus、Sonnet、Fable，Gemini 含 PaLM、Gemma；「未写明」是原文只说「现成的 VLM / LLM」的论文。</div>')
    a('</section>')

    # ---------------------------------------------------------------- page 5
    a('<section class="page">')
    a('<div class="kicker">04 <span>· 判例与下一步</span></div>')
    a('<h2>已经定下来的判例，和还没做完的事</h2>')
    a('<p class="lead">左边是剔除的论文，每篇对应第 2 页的一条标准；右边是容易误判、但按标准应当保留的论文。'
      '以后遇到相似的论文，可以直接比照。</p>')
    outs = [r for r in rows if r["verdict"] == "剔除"]
    why = {"RoboTwin 2.0": ("4", "双臂数据生成器与 benchmark，MLLM 写任务代码只是其中一步"),
           "HumanoidGen": ("4", "人形操作数据与任务生成框架"),
           "RoboFind": ("1", "决策回路是 Uni-NaVid 导航、DINO 阈值验证与确定性恢复"),
           "RoboFAC": ("2", "在自建失败数据集上微调 Qwen2.5-VL-3B / 7B"),
           "AgentVLN": ("2", "Qwen2.5-VL-3B 指令微调后当大脑"),
           "Ludi": ("2", "LoRA 微调 Qwen3.5-4B / 9B，GPT 只作对照"),
           "Articulate AnyMesh": ("4", "关节资产建模流水线，GPT-4o 是其中一个组件"),
           "Tool-Aligned VLA Agent": ("4", "主要结果衡量 VLA 后训练，规划器可随意替换"),
           "VLABench": ("5", "评测对象主要是 VLA")}
    assert {r["key"] for r in outs} == set(why), {r["key"] for r in outs} ^ set(why)
    keeps = [("Code as Policies", "L2", "一次写出策略程序、执行中不再调用 LLM；开环也算（标准 3）"),
             ("ReKep", "L2", "VLM 写关键点约束交给求解器；「rekep这一类的都算」"),
             ("GUAVA ★", "L2", "前沿 VLM 自己当 agent，轨迹蒸馏成 4B 模型，属经验迁移（标准 2）"),
             ("EmbodiedSmith ★", "L1", "不是 Real2Sim；生成式仿真，主体是 agent 循环（标准 4）"),
             ("AutoRT", "L2", "原文写明 LLM 未微调，是调度机器人的核心；采数据只是用途"),
             ("SUDD、RobotGPT", "L2", "现成 GPT 先在仿真里执行，经验再蒸馏成策略"),
             ("Agentic Real2Sim、RPG、SimEX", "L1", "agentic Real2Sim 都算，只是一个子方向")]
    left = ('<div><div class="colh">剔除 · 9 篇<span>数字 = 第 2 页的标准</span></div><table class="cases">'
            + "".join(f'<tr><td class="k">{esc(k)}</td><td class="t"><span class="tag out">标准 {why[k][0]}</span></td>'
                      f'<td class="r">{esc(why[k][1])}</td></tr>' for k in why) + '</table></div>')
    right = ('<div><div class="colh">保留 · 容易误判的<span>色条 = 所在层</span></div><table class="cases">'
             + "".join(f'<tr><td class="k">{esc(k)}</td><td class="t"><span class="tag l" style="--c:{LC[l]};--t:{tint(LC[l], 0.12)}">'
                       f'{l}</span></td><td class="r">{esc(w)}</td></tr>' for k, l, w in keeps) + '</table></div>')
    a(f'<div class="two" style="grid-template-columns:1fr 1fr">{left}{right}</div>')
    a('<h3 style="margin-top:14pt">还没判的约 {:,} 篇</h3>'.format(n_todo))
    a('<div class="two" style="grid-template-columns:1.25fr 1fr;align-items:start">'
      f'<div class="chart"><div class="s">黑 = 有 arXiv 号，可直接下载全文；灰 = 没有，需要按 DOI 找开放获取的 PDF。</div>'
      f'{fig_todo(todo)}</div>'
      '<div class="nx" style="margin-top:2pt"><div class="k">需要你先定</div><h4>边界论文算不算</h4>'
      '<p>旧定义把只在离散仿真（ALFRED、VirtualHome、R2R 离散图）里做实验的工作和自动驾驶放在边界。'
      '你的框架里 Env / Sim 是否包括它们，决定这 313 篇要不要判。</p></div></div>')
    a('<div class="next">'
      '<div class="nx"><div class="k">STEP 1</div><h4>补判，把清单补全</h4><ul>'
      '<li>流程与这 174 篇相同：下载全文 → 子 agent 读方法与实验 → 人工复核 → 写回同一份 CSV</li>'
      '<li>有 arXiv 号的约 1,350 篇可直接跑，下载约 2.5 小时</li></ul></div>'
      '<div class="nx"><div class="k">STEP 2</div><h4>等你表态的边界案例</h4><ul>'
      '<li>Tool-Aligned VLA Agent（剔除）、AutoRT（保留）</li>'
      '<li>GPT-6 Astra on RoboDojo：全文判为评测，放在资源；你举过它当 L3 的例子</li></ul></div>'
      '<div class="nx"><div class="k">STEP 3</div><h4>清单定稿之后</h4><ul>'
      '<li>README 按 L1 / L2 / L3 重排</li><li>按六条标准重写定义，再写综述正文</li></ul></div></div>')
    a('<div class="files">'
      '<div><b>清单</b><code>data/core/layer_classification.csv</code><br>每篇：层与子类、决策模型、是否训练、论文主体、理由、原文证据</div>'
      '<div><b>交接</b><code>HANDOFF.md</code><br>标准、文件状态、补判流程与命令</div>'
      '<div><b>原始判定</b><code>data/judging_runs/content_rejudge/</code><br>提示词 <code>screening/prompts/content_rejudge.txt</code></div></div>')
    a('</section>')

    css = (R.CSS + CSS).replace("FONTDIR", "file://" + os.path.abspath(fontdir)) if fontdir else \
        re.sub(r"@font-face[^}]*}", "", R.CSS + CSS)
    return (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>Agentic Embodiment 论文清单</title>'
            f'<style>{css}</style></head><body>{"".join(H)}</body></html>')


def hbars_pair(fams, pct, label_w=52, W=236, rowh=44):
    """Paired bars per model family: pioneers (grey) above 2026 (ink), value labels at the bar ends."""
    b, y = [], 4
    span = W - label_w - 36
    for f in fams:
        b.append(T(label_w - 8, y + 14, f, 8.6, 500, INK, "end"))
        for k, (t, col) in enumerate((("先驱", BASE), ("2026", INK))):
            v = pct(t, f)
            w = max(span * v / 100, 1.5)
            yy = y + 3 + k * 10
            b.append(f'<rect x="{label_w}" y="{yy}" width="{w:.1f}" height="8" rx="2" fill="{col}"/>')
            b.append(T(label_w + w + 4, yy + 7.5, f"{v:.0f}%", 7.4, 500 if k else 400, INK if k else MUTED))
        y += rowh
    return svg(W, y, "".join(b), "各模型家族在先驱与 2026 年论文中的占比")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", default=os.path.join(os.path.expanduser("~"), ".cache", "aae-report-fonts"))
    ap.add_argument("--out", default=os.path.join(R.ROOT, "docs", "list_summary.pdf"))
    ap.add_argument("--html", default=None, help="also keep the intermediate HTML here")
    args = ap.parse_args()
    page = build_html(R.ensure_fonts(args.fonts))
    tmp = args.html or os.path.join(tempfile.mkdtemp(), "list_summary.html")
    open(tmp, "w").write(page)
    env = dict(os.environ)
    try:
        env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip() + \
                           (os.pathsep + env["NODE_PATH"] if env.get("NODE_PATH") else "")
    except FileNotFoundError:
        pass
    subprocess.run(["node", os.path.join(R.ROOT, "scripts", "print_pdf.cjs"), tmp, args.out], check=True, env=env)
    print(f"wrote {args.out} (html: {tmp})")


if __name__ == "__main__":
    main()
