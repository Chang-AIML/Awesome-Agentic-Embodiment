#!/usr/bin/env python3
"""Five-page illustrated survey preview (Chinese): docs/survey_brief.pdf.

A condensed, figure-first version of the survey for reading before the full text is written:
  1 overview (thesis, seat map, key numbers)   2 scope and the agent tests
  3 lineage map: pioneers 2022-2025 -> 2026     4 the five seats and the two topic chapters
  5 trends and open problems
Numbers come from the same data as the progress report (core_table.csv, fine_labels.csv, core_meta.json);
colors, fonts, chips and charts are shared with scripts/build_report.py.

Usage: python3 scripts/build_brief.py [--out docs/survey_brief.pdf] [--html <keep the html here>]
"""
import argparse, csv, os, re, subprocess, sys, tempfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_report as R  # noqa: E402

esc, T, svg, tint, text_w, COLOR, SEATS, SEAT_ZH = R.esc, R.T, R.svg, R.tint, R.text_w, R.COLOR, R.SEATS, R.SEAT_ZH
INK, INK2, MUTED, GRID, BASE, SURFACE = R.INK, R.INK2, R.MUTED, R.GRID, R.BASE, R.SURFACE
BLUE, BLUE_D = COLOR["Controller"], "#1c5cab"

# Lineage map rows: (label, sub-label, seat whose color marks the row or None, keys of the curated table).
LINES = [
    ("Controller", "编排型", "Controller",
     ["ZS-Planners", "SayCan", "Socratic Models", "Inner Monologue", "RoCo", "SayPlan", "Look Before You Leap",
      "COME-robot", "LLM3", "BUMBLE", "ORGANA", "Being-0", "AquaChat",
      "Tool-Aligned VLA Agent", "Physical Agency", "Thea", "SpaceMind", "Astra Robot Agents"]),
    ("Controller", "直接驱动型", "Controller",
     ["Code as Policies", "ProgPrompt", "ChatGPT for Robotics", "VoxPoser", "Language to Rewards",
      "Prompt a Robot to Walk", "TypeFly", "CoPa", "MOKA", "ReKep", "OmniManip",
      "CaP-X", "Show-Harness", "Agent as Policy", "Astra on RoboDojo", "OpenRUA"]),
    ("Controller", "lifelong", "Controller",
     ["DROC", "Incremental Humanoid Learning", "LRLL", "ReMEmbR", "RoboMemory",
      "Harness VLA", "PhysMem", "MessyMem", "Robo-COP"]),
    ("Supervisor", "监督者", "Supervisor",
     ["REFLECT", "DoReMi", "Safety Chip", "Real-Time Anomaly Detection", "Code-as-Monitor", "RoboGuard", "RoboFAC",
      "Agentic Task Graph", "Zetta", "WhenToAsk", "Beyond Human Demos"]),
    ("Teacher", "教师", "Teacher",
     ["SUDD", "RobotGPT", "Manipulate-Anything", "RoboTwin 2.0", "HumanoidGen",
      "GUAVA", "EmbodiedSWE", "CAPEX", "Frontier Demo Generation"]),
    ("Designer", "设计者", "Designer",
     ["Eureka", "Text2Reward", "GenSim", "RoboGen", "Agentic Skill Discovery", "OMNI-EPIC", "CurricuLLM",
      "Eurekaverse", "SceneSmith", "SAGE", "RF-Agent", "FIND", "ROOT"]),
    ("Developer", "开发者", "Developer",
     ["RoboMorph", "PDDLLM", "RobotSmith", "VLMgineer", "ENPIRE", "ASPIRE", "AdaHVLA", "PhysEvo", "LACE-CRAFT"]),
    ("VLN", "专题", None,
     ["LM-Nav", "NavGPT", "SayNav", "InstructNav", "Open-Nav", "VLMnav", "CA-Nav",
      "AgentVLN", "OnFly", "HarnessVLN", "ASENA", "Air-Ground VLN"]),
    ("Real2Sim", "子方向", None,
     ["DrEureka", "Video2Policy", "Articulate AnyMesh", "Agentic Real2Sim", "RPG", "SimEX", "Real2Gym",
      "EmbodiedSmith"]),
]
YEARS = ["2022", "2023", "2024", "2025", "2026"]

CSS = """
@page { size: A4; }
body { font-size: 8.9pt; line-height: 1.55; }
.page { height: 266mm; position: relative; overflow: hidden; break-after: page; }
.page:last-child { break-after: auto; }
.kicker { font-size: 7.6pt; letter-spacing: 1.6pt; color: #1c5cab; font-weight: 700; margin-bottom: 5pt; }
.kicker span { color: #898781; font-weight: 400; letter-spacing: 0.8pt; }
h1.title { font-size: 30pt; line-height: 1.1; margin: 0; letter-spacing: -0.4pt; }
.subtitle { font-size: 13pt; color: #52514e; margin: 4pt 0 10pt; }
h2 { font-size: 13pt; border: 0; padding: 0; margin: 2pt 0 3pt; }
.lead { color: #52514e; font-size: 9pt; margin: 0 0 8pt; }
h3 { font-size: 10pt; margin: 9pt 0 5pt; }
.band { background: #0b0b0b; color: #ffffff; border-radius: 10px; padding: 10pt 14pt 11pt; margin: 0 0 10pt; }
.band .tag { font-size: 7.4pt; letter-spacing: 1.2pt; color: #9ec5f4; font-weight: 700; }
.band .q { font-size: 13.2pt; font-weight: 700; line-height: 1.35; margin: 3pt 0 4pt; }
.band .qz { font-size: 8.8pt; color: #d6d4cc; line-height: 1.5; }
figure { margin: 4pt 0 6pt; }
figcaption { font-size: 7.9pt; margin-top: 3pt; }
.kp { display: grid; grid-template-columns: 1.15fr 1fr 1fr 1fr 1.35fr; gap: 6pt; margin: 8pt 0 9pt; }
.kp div { border-top: 2.5px solid #0b0b0b; padding-top: 4pt; }
.kp .v { font-size: 19pt; font-weight: 700; line-height: 1.1; letter-spacing: -0.3pt; }
.kp .l { font-size: 7.8pt; color: #52514e; line-height: 1.35; margin-top: 2pt; }
.abstract { font-size: 8.9pt; line-height: 1.65; columns: 2; column-gap: 16pt; }
.abstract b { color: #1c5cab; }
.flow4 { display: grid; grid-template-columns: 1fr 11pt 1fr 11pt 1fr 11pt 1fr; align-items: stretch; margin: 2pt 0 4pt; }
.flow4 .arr { align-self: center; text-align: center; color: #898781; font-size: 11pt; }
.tcard { border: 1px solid #e1e0d9; border-radius: 8px; padding: 7pt 8pt 8pt; background: #fcfcfb; }
.tcard .no { display: inline-block; width: 15pt; height: 15pt; border-radius: 50%; background: #0b0b0b; color: #fff;
             text-align: center; line-height: 15pt; font-size: 8pt; font-weight: 700; margin-right: 4pt; }
.tcard.scope .no { background: #1c5cab; }
.tcard h4 { display: inline; font-size: 9.6pt; margin: 0; }
.tcard .rule { font-size: 8pt; color: #0b0b0b; line-height: 1.45; margin: 5pt 0 5pt; min-height: 35pt; }
.tcard .yes, .tcard .no2 { font-size: 7.5pt; line-height: 1.42; margin-top: 3pt; padding-left: 11pt; text-indent: -11pt; }
.tcard .yes { color: #0b0b0b; }
.tcard .no2 { color: #898781; }
.loops { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8pt; }
.lcard { border-radius: 8px; padding: 6pt 8pt 7pt; background: #fcfcfb; border: 1px solid #e1e0d9; }
.lcard h4 { font-size: 9.4pt; margin: 0 0 1pt; }
.lcard .d { font-size: 7.7pt; color: #52514e; line-height: 1.42; }
.lcard .ex { font-size: 7.4pt; color: #0b0b0b; margin-top: 3pt; }
.notes { display: grid; grid-template-columns: 1fr 1fr; gap: 8pt; margin-top: 8pt; }
.notes > div { font-size: 7.9pt; line-height: 1.5; color: #52514e; border-top: 1px solid #c3c2b7; padding-top: 4pt; }
.notes b { color: #0b0b0b; }
.pill { display: inline-block; font-size: 7.1pt; border: 1px solid #c3c2b7; color: #52514e; border-radius: 9px;
        padding: 0 5pt; margin: 1.5pt 2pt 1.5pt 0; background: #ffffff; }
.lineage { table-layout: fixed; width: 100%; font-size: 7.3pt; border-collapse: separate; border-spacing: 0; }
.lineage th { text-align: left; vertical-align: bottom; padding: 0 4pt 5pt; border-bottom: 1.5px solid #0b0b0b; }
.lineage th .y { font-size: 11pt; font-weight: 700; color: #0b0b0b; }
.lineage th .bar { height: 5pt; border-radius: 0 2px 2px 0; background: #9ec5f4; margin: 3pt 0 1pt; }
.lineage th .bn { font-size: 6.9pt; color: #898781; font-weight: 400; }
.lineage td { border-bottom: 1px solid #e1e0d9; padding: 4pt 3pt 3pt 4pt; vertical-align: top; }
.lineage td.c26 { background: #f5f9fe; }
.lineage tr.topic td { background: #fcfcfb; }
.lineage tr.topic td.c26 { background: #eef4fc; }
.lineage td.lab { padding-left: 5pt; }
.lineage .ln { font-size: 8.6pt; font-weight: 700; color: #0b0b0b; line-height: 1.2; display: block; }
.lineage .ls { font-size: 7.1pt; color: #52514e; display: block; line-height: 1.3; }
.lineage .lc { font-size: 6.9pt; color: #898781; display: block; margin-top: 2pt; }
.lineage .chip { white-space: normal; font-size: 7pt; margin: 1.2pt 1.5pt 1.2pt 0; }
.lineage .sw2 { display: inline-block; width: 4pt; height: 22pt; border-radius: 2px; float: left; margin: 1pt 5pt 0 0; }
.legend { font-size: 7.4pt; color: #52514e; margin: 5pt 0 0; }
.legend .chip { margin-right: 2pt; }
.reads { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8pt; margin-top: 9pt; }
.reads div { font-size: 7.9pt; line-height: 1.5; color: #52514e; border-left: 3px solid #0b0b0b; padding: 1pt 0 1pt 7pt; }
.reads b { display: block; color: #0b0b0b; font-size: 8.8pt; margin-bottom: 1pt; }
.cards { display: grid; grid-template-columns: 1fr 1fr; gap: 8pt 9pt; }
.scard { border: 1px solid #e1e0d9; border-top: 4px solid var(--c); border-radius: 8px; padding: 7pt 9pt 8pt;
         background: #ffffff; break-inside: avoid; }
.scard .hd { display: flex; align-items: baseline; gap: 5pt; }
.scard .nm { font-size: 11.5pt; font-weight: 700; }
.scard .zh { font-size: 8pt; color: #52514e; margin: 0; flex: 1; }
.scard .ct { font-size: 7.4pt; color: #52514e; white-space: nowrap; }
.scard .ct b { font-size: 10pt; color: #0b0b0b; }
.scard .when { font-size: 7.5pt; color: #52514e; margin: 1pt 0 4pt; }
.scard .ln2 { margin: 2pt 0 4pt; line-height: 1.5; }
.scard .ln2 .chip { white-space: normal; font-size: 7pt; }
.scard .arr { color: #898781; font-size: 9pt; margin: 0 3pt 0 1pt; }
.scard .tg { font-size: 6.6pt; color: #898781; letter-spacing: 0.5pt; margin-right: 3pt; }
.scard p { font-size: 8.2pt; line-height: 1.52; margin: 0; }
.scard .share { margin-top: 5pt; font-size: 7.2pt; color: #52514e; display: flex; align-items: center; gap: 5pt; }
.scard .share .tr { flex: 1; height: 5pt; background: #f0efea; border-radius: 3px; position: relative; }
.scard .share .fl { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 3px; background: var(--c); }
.scard .share b { color: #0b0b0b; font-size: 8pt; }
.ibar { display: grid; grid-template-columns: 52pt 1fr 22pt; align-items: center; gap: 4pt; font-size: 7.3pt;
        color: #52514e; margin: 2pt 0; }
.ibar .tr { height: 7pt; background: #f0efea; border-radius: 0 3px 3px 0; position: relative; }
.ibar .fl { position: absolute; left: 0; top: 0; bottom: 0; border-radius: 0 3px 3px 0; background: #3987e5; }
.ibar .n { text-align: right; color: #0b0b0b; font-variant-numeric: tabular-nums; }
.tiles { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8pt; margin: 6pt 0 8pt; }
.tile { border-radius: 8px; background: #f5f9fe; padding: 7pt 10pt 8pt; }
.tile .v { font-size: 20pt; font-weight: 700; line-height: 1.1; letter-spacing: -0.3pt; color: #0b0b0b; }
.tile .v span { color: #898781; font-weight: 400; font-size: 13pt; margin: 0 3pt; }
.tile .l { font-size: 8pt; color: #0b0b0b; font-weight: 700; margin-top: 3pt; }
.tile .s { font-size: 7.5pt; color: #52514e; line-height: 1.4; }
.probs { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8pt; }
.prob { border: 1px solid #e1e0d9; border-radius: 8px; padding: 6pt 8pt 7pt; background: #fcfcfb; }
.prob .k { font-size: 7pt; color: #1c5cab; font-weight: 700; letter-spacing: 0.8pt; }
.prob h4 { font-size: 9.2pt; margin: 1pt 0 2pt; }
.prob p { font-size: 7.8pt; color: #52514e; line-height: 1.48; margin: 0; }
.method { margin-top: 9pt; border-top: 1.5px solid #0b0b0b; padding-top: 6pt; }
.mflow { display: grid; grid-template-columns: 1fr 9pt 1fr 9pt 1fr 9pt 1fr 9pt 1fr; align-items: center; }
.mflow .a { text-align: center; color: #898781; }
.mflow .m { font-size: 7.4pt; color: #52514e; line-height: 1.35; }
.mflow .m b { display: block; font-size: 13pt; color: #0b0b0b; line-height: 1.15; }
.mflow .m.last b { color: #1c5cab; }
.method .fine { font-size: 7.3pt; color: #898781; line-height: 1.5; margin-top: 5pt; }
.mflow { align-items: start; }
.mflow .a { padding-top: 4pt; }
.abs3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12pt; font-size: 8.4pt; line-height: 1.6; color: #0b0b0b; }
.abs3 b { display: block; font-size: 9.4pt; color: #1c5cab; margin-bottom: 2pt; }
.toc { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8pt; margin-top: 14pt; }
.toc div { background: #f4f3ef; border-radius: 8px; padding: 7pt 9pt 8pt; }
.toc .n { display: block; font-size: 15pt; font-weight: 700; color: #c3c2b7; line-height: 1.1; }
.toc b { display: block; font-size: 9.2pt; margin: 2pt 0 1pt; }
.toc .d { display: block; font-size: 7.5pt; color: #52514e; line-height: 1.4; }
.cases { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6pt 8pt; }
.case { border-bottom: 1px solid #e1e0d9; padding: 2pt 0 5pt; font-size: 7.7pt; line-height: 1.45; }
.case b { font-size: 8.6pt; margin-right: 3pt; }
.case .why { display: block; color: #52514e; margin-top: 1pt; }
.vd { display: inline-block; font-size: 6.8pt; border-radius: 3px; padding: 0 4pt; margin-right: 4pt; vertical-align: 1pt; }
.vd.yes { background: #0b0b0b; color: #ffffff; }
.vd.pio { border: 1px dashed #52514e; color: #52514e; }
.vd.no { background: #e1e0d9; color: #52514e; }
.lineage .chip { font-size: 6.8pt; padding: 1pt 3.5pt; }
.lineage td { padding: 3pt 2pt 2pt 3pt; }
"""


def wrap(s, size, width):
    """Break a mixed CJK / Latin string into lines no wider than width (rough glyph widths)."""
    out, cur = [], ""
    for tok in re.findall(r"[A-Za-z0-9.+\-/★]+ ?|.", s):
        if cur and text_w(cur + tok, size) > width:
            out.append(cur.rstrip())
            cur = tok.lstrip()
        else:
            cur += tok
    return out + ([cur.rstrip()] if cur.strip() else [])


def seat_card(x, y, w, h, seat, role, ex, pio, core):
    c = COLOR[seat]
    b = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{tint(c, 0.08)}" stroke="{tint(c, 0.35)}" stroke-width="1"/>',
         f'<rect x="{x}" y="{y + 8}" width="4" height="{h - 16}" rx="2" fill="{c}"/>',
         T(x + 14, y + 20, seat, 12.5, 700, INK),
         T(x + 18 + text_w(seat, 12.5), y + 20, SEAT_ZH[seat], 9.5, 400, INK2),
         T(x + w - 10, y + 20, f"{pio} → {core}", 12, 700, INK, "end"),
         T(x + w - 10, y + 31, "先驱 → 2026", 7.6, 400, MUTED, "end")]
    ly = y + 44
    for line in role:
        b.append(T(x + 14, ly, line, 9.2, 400, INK2))
        ly += 13
    for k, line in enumerate(wrap(ex, 8.4, w - 26)):
        b.append(T(x + 14, y + h - 10 - 11 * (len(wrap(ex, 8.4, w - 26)) - 1 - k), line, 8.4, 500, INK))
    return "".join(b)


def fig_hero(cnt):
    W, H = 680, 314
    b = [T(100, 14, "部署前 · pre-deployment", 10.5, 700, INK, "middle"),
         T(100, 28, "agent 的产出冻结后，交给部署的系统", 8.6, 400, MUTED, "middle"),
         T(580, 14, "运行时 · runtime", 10.5, 700, INK, "middle"),
         T(580, 28, "agent 在 episode 中被调用", 8.6, 400, MUTED, "middle"),
         f'<line x1="340" y1="40" x2="340" y2="128" stroke="{BASE}" stroke-width="1" stroke-dasharray="3 4"/>',
         f'<line x1="340" y1="222" x2="340" y2="310" stroke="{BASE}" stroke-width="1" stroke-dasharray="3 4"/>']
    left = [("Designer", 40, ["设计学习问题：奖励、任务、", "环境与仿真、课程、评测"], "Eureka → SceneSmith、FIND"),
            ("Teacher", 132, ["亲自执行并检验，经检验的", "轨迹成为策略的训练目标"], "SUDD → GUAVA ★、CAPEX"),
            ("Developer", 224, ["修改系统本身：代码、技能库、", "harness、硬件；试验定去留"], "RoboMorph → ENPIRE ★、PhysEvo")]
    for seat, y, role, ex in left:
        b.append(seat_card(0, y, 200, 86, seat, role, ex, *cnt[seat]))
    b.append(seat_card(480, 40, 200, 130, "Controller",
                       ["每一步决定机器人做什么：", "计划、调用技能或 VLA、写", "当下执行的代码或约束，", "或直接输出动作"],
                       "SayCan、Code as Policies → Thea、Show-Harness ★", *cnt["Controller"]))
    b.append(seat_card(480, 180, 200, 130, "Supervisor",
                       ["只在异常时介入：解释失败、", "检测违例、执行安全规范，", "触发恢复或否决危险动作"],
                       "REFLECT、Safety Chip → Agentic Task Graph、Zetta", *cnt["Supervisor"]))
    b.append(f'<rect x="258" y="132" width="164" height="86" rx="10" fill="#ffffff" stroke="{INK}" stroke-width="1.6"/>')
    b.append(f'<circle cx="340" cy="158" r="9" fill="none" stroke="{INK2}" stroke-width="1.4"/>'
             f'<path d="M340,167 L340,186 M328,174 L352,174 M340,186 L331,198 M340,186 L349,198" stroke="{INK2}" '
             f'stroke-width="1.4" fill="none" stroke-linecap="round"/>')
    b.append(T(340, 211, "机器人身体 + 部署的策略", 9.6, 700, INK, "middle"))
    for y0, y1 in ((83, 152), (175, 175), (267, 198)):
        b.append(R.arrow(f"M200,{y0} C232,{y0} 228,{y1} 255,{y1}"))
    b.append(R.arrow("M480,105 C452,105 452,150 425,152"))
    b.append(R.arrow("M480,245 C452,245 452,200 425,198"))
    b.append(T(452, 96, "持续驱动", 8.4, 500, MUTED, "middle"))
    b.append(T(452, 262, "仅在异常时", 8.4, 500, MUTED, "middle"))
    return svg(W, H, "".join(b), "五个 Seat 围绕机器人身体")


def node(x, y, w, h, lines, fill="#ffffff", stroke=BASE, color=INK, size=9.2, bold_first=True):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>']
    y0 = y + h / 2 - (len(lines) - 1) * 6.5 + 3.5
    for k, ln in enumerate(lines):
        out.append(T(x + w / 2, y0 + 13 * k, ln, size if k == 0 else size - 1.2, 700 if (k == 0 and bold_first) else 400,
                     color if k == 0 else INK2, "middle"))
    return "".join(out)


def fig_routes():
    W, H = 680, 178
    g = "#f4f3ef"
    b = [f'<rect x="0" y="0" width="318" height="{H}" rx="10" fill="{g}"/>',
         T(16, 22, "具身大模型路线", 11, 700, INK2), T(108, 22, "不收 · 只作为被调用的工具", 8.4, 400, MUTED),
         node(16, 44, 82, 42, ["图像 + 指令"], fill="#ffffff", color=INK2),
         node(118, 38, 104, 54, ["VLA / WAM", "一个训练好的模型"], fill="#ffffff", color=INK2),
         node(242, 44, 60, 42, ["动作"], fill="#ffffff", color=INK2),
         R.arrow("M98,65 L115,65"), R.arrow("M222,65 L239,65"),
         T(16, 120, "把感知、语言和动作训练进同一个模型，直接输出动作", 8.8, 400, INK2),
         T(16, 138, "π0.5、ECoT、Hi Robot、Gemini Robotics 1.5、PaLM-E", 8.4, 400, MUTED),
         T(16, 156, "在本综述中只作为工具出现，例如 Harness VLA 里被调度的 VLA", 8.4, 400, MUTED),
         f'<rect x="362" y="0" width="318" height="{H}" rx="10" fill="{tint(BLUE, 0.08)}" stroke="{tint(BLUE, 0.45)}"/>',
         T(378, 22, "通用大模型 agent 路线", 11, 700, INK), T(504, 22, "本综述", 8.4, 700, BLUE_D),
         node(378, 44, 70, 42, ["LLM / VLM"], fill="#ffffff", stroke=BLUE, color=BLUE_D),
         node(466, 34, 120, 62, ["harness", "技能 · 工具 · VLA", "代码 · 约束 · 动作"], fill="#ffffff"),
         node(604, 44, 62, 42, ["机器人"], fill="#ffffff", stroke=INK),
         R.arrow("M448,65 L463,65"), R.arrow("M586,65 L601,65"),
         f'<path d="M635,86 C635,112 413,112 413,89" fill="none" stroke="{BLUE}" stroke-width="1.4" '
         f'stroke-dasharray="4 3" marker-end="url(#ah)"/>',
         T(524, 116, "执行后果的证据 → 再决策", 8.4, 700, BLUE_D, "middle"),
         T(378, 138, "通用模型规划、调工具、写代码或约束，也可以直接出动作", 8.8, 400, INK2),
         T(378, 156, "SayCan、Code as Policies、ReKep、Harness VLA ★、GPT-6 Astra", 8.4, 400, MUTED),
         T(340, 70, "vs", 11, 700, MUTED, "middle")]
    return svg(W, H, "".join(b), "两条路线")


def loop_icon(kind):
    W, H = 200, 58
    b = []
    if kind == "re":
        b += [node(4, 14, 50, 26, ["模型"], stroke=BLUE, color=BLUE_D, size=8.6), node(76, 14, 50, 26, ["执行"], size=8.6),
              node(146, 14, 50, 26, ["观测"], size=8.6), R.arrow("M54,27 L73,27"), R.arrow("M126,27 L143,27"),
              f'<path d="M171,40 C171,56 29,56 29,43" fill="none" stroke="{BLUE}" stroke-width="1.3" marker-end="url(#ah)"/>',
              T(100, 11, "带着先前的决策与后果再调用", 7.6, 500, MUTED, "middle")]
    elif kind == "au":
        b += [node(4, 14, 44, 26, ["模型"], stroke=BLUE, color=BLUE_D, size=8.6),
              node(66, 14, 62, 26, ["约束 / 程序"], size=8.4), node(146, 14, 50, 26, ["实时感知"], size=8.4),
              R.arrow("M48,27 L63,27"),
              f'<path d="M128,21 C136,10 140,10 146,19" fill="none" stroke="{INK2}" stroke-width="1.2" marker-end="url(#ah)"/>',
              f'<path d="M146,35 C140,46 136,46 129,36" fill="none" stroke="{INK2}" stroke-width="1.2" marker-end="url(#ah)"/>',
              T(137, 56, "执行中重解 / 回溯", 7.6, 500, MUTED, "middle"), T(26, 52, "只写一次", 7.6, 500, MUTED, "middle")]
    else:
        b += [node(4, 14, 50, 26, ["模型"], stroke=BLUE, color=BLUE_D, size=8.6),
              node(76, 14, 50, 26, ["计划"], size=8.6), node(146, 14, 50, 26, ["执行"], size=8.6),
              f'<path d="M54,27 L73,27" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 3" marker-end="url(#ah)"/>',
              f'<path d="M126,27 L143,27" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="3 3" marker-end="url(#ah)"/>',
              T(100, 54, "没有回到模型的环", 7.6, 500, MUTED, "middle")]
    return svg(W, H, "".join(b), "闭环形式示意", width="100%")


def lineage(rows, trend):
    byk = {r["key"]: r for r in rows}
    missing = [k for line in LINES for k in line[3] if k not in byk]
    assert not missing, f"lineage keys not in core_table.csv: {missing}"
    n = {x["year"]: x["n"] for x in trend}
    top = max(n.values())
    out = ['<table class="lineage"><colgroup><col style="width:10.5%"><col style="width:14%"><col style="width:18.5%">'
           '<col style="width:17.5%"><col style="width:13.5%"><col style="width:26%"></colgroup><tr><th></th>']
    for y in YEARS:
        out.append(f'<th><span class="y">{y}</span><div class="bar" style="width:{max(3, 100 * n[y] / top):.1f}%"></div>'
                   f'<span class="bn">{n[y]} 篇 core</span></th>')
    out.append("</tr>")
    for name, sub, seat, keys in LINES:
        xs = [byk[k] for k in keys]
        pio = sum(r["tier"] == "pioneer" for r in xs)
        edge = f"4px solid {COLOR[seat]}" if seat else f"4px dotted {MUTED}"
        out.append(f'<tr class="{"topic" if not seat else ""}"><td class="lab" style="border-left:{edge}">'
                   f'<span class="ln">{esc(name)}</span><span class="ls">{esc(sub)}</span></td>')
        for y in YEARS:
            cell = sorted([r for r in xs if r["year"] == y], key=lambda r: r["date"])
            out.append(f'<td class="{"c26" if y == "2026" else ""}">' + "".join(R.chip(r) for r in cell) + "</td>")
        out.append("</tr>")
    out.append("</table>")
    out.append('<div class="legend"><span class="chip" style="--c:#2a78d6">实心</span>再决策　'
               '<span class="chip au" style="--c:#2a78d6">空心</span>编写闭环　'
               '<span class="chip op" style="--c:#2a78d6">虚线</span>开环（开创了方向，不满足闭环）　'
               '颜色 = Seat　★ 你点名的论文　◆ Real2Sim 章　△ VLN 章　'
               '表头的条形 = 该年全部判为 core 的论文数（2026 年全量检索）</div>')
    return "".join(out)


def scard(rows, seat, name, zh, when, pios, news, text, share=None, col=None):
    byk = {r["key"]: r for r in rows}
    c = col or COLOR[seat]
    sel = [r for r in rows if r["tier"] in ("pioneer", "core") and (
        (seat and r["seat"] == seat) or (not seat and r.get("theme") in name))]
    n_p, n_c = sum(r["tier"] == "pioneer" for r in sel), sum(r["tier"] == "core" for r in sel)
    chips = lambda ks: "".join(R.chip(byk[k]) for k in ks)
    out = [f'<div class="scard" style="--c:{c}"><div class="hd"><span class="nm">{esc(name if seat else zh)}</span>'
           f'<span class="zh">{esc(zh if seat else "")}</span>'
           f'<span class="ct"><b>{n_p}</b> 先驱 · <b>{n_c}</b> 2026</span></div>'
           f'<div class="when">{esc(when)}</div>'
           f'<div class="ln2"><span class="tg">源头</span>{chips(pios)}<span class="arr">→</span>'
           f'<span class="tg">2026</span>{chips(news)}</div><p>{text}</p>']
    if share is not None:
        out.append(f'<div class="share">2026 年全部 core 论文中以此为主 seat<span class="tr">'
                   f'<span class="fl" style="width:{share:.0f}%"></span></span><b>{share:.0f}%</b></div>')
    out.append("</div>")
    return "".join(out)


def build_html(fontdir):
    rows, c, trend, *_ = R.load()
    t = {x["year"]: x for x in trend}
    cnt = {s: (sum(r["tier"] == "pioneer" and r["seat"] == s for r in rows),
               sum(r["tier"] == "core" and r["seat"] == s for r in rows)) for s in SEATS}
    n_pio = sum(r["tier"] == "pioneer" for r in rows)
    n_core = sum(r["tier"] == "core" for r in rows)
    n_res = sum(r["tier"] == "resource" for r in rows)
    eff0, eff1 = t["2022"]["eff"], t["2026"]["eff"]
    ctl = {y: x["alls"]["Controller"] / x["n"] for y, x in t.items()}
    share26 = {s: 100 * t["2026"]["prim"][s] / t["2026"]["n"] for s in SEATS}
    dev = {y: 100 * x["prim"]["Developer"] / x["n"] for y, x in t.items()}
    H = []
    a = H.append

    # ------------------------------------------------------------------ page 1: overview
    a('<section class="page">')
    a('<div class="kicker">AGENTIC EMBODIMENT <span>· 综述预览 · 2026 年 10 月</span></div>')
    a('<h1 class="title">Agentic Embodiment</h1>')
    a('<div class="subtitle">通用大模型如何一步步占据机器人身体周围的位置</div>')
    a('<div class="band"><div class="tag">主线 · 草案</div>'
      '<div class="q">Agency spreads around the body — general models, not embodied action models, fill seat after seat.</div>'
      '<div class="qz">agency 没有离开机器人，而是在身体周围逐个占据新的位置：一个接一个填满这些位置的，是通用大模型，而不是具身动作模型。</div></div>')
    a(f'<figure>{fig_hero(cnt)}<figcaption><b>图 1　五个 Seat。</b>按 agent 的产出在什么阶段产生、由谁消费来分：左边三个在部署前起作用，'
      f'右边两个在运行时起作用。数字为核心表中先驱（2022–2025）与 2026 年论文的篇数，含 VLN 与 Real2Sim 两章；★ 为你点名的论文。</figcaption></figure>')
    kp = [(f"{c['judged']:,}", "篇候选论文逐篇判定"), (f"{n_pio}", "篇先驱<br>2022–2025"), (f"{n_core}", "篇 2026 年<br>代表作"),
          (f"{n_res}", "个 benchmark<br>与资源"), (f"{eff0:.2f} → {eff1:.2f}", "每年的有效 seat 数<br>2022 → 2026")]
    a('<div class="kp">' + "".join(f'<div><div class="v">{v}</div><div class="l">{l}</div></div>' for v, l in kp) + '</div>')
    a('<div class="abs3">'
      '<div><b>研究对象</b>通用大模型（LLM / VLM）作为 agent 驱动机器人：规划、调用技能与 VLA、写代码与约束，必要时直接输出动作，'
      '并依据执行后果重新决策。具身大模型（VLA、WAM）只作为被调用的工具出现。</div>'
      '<div><b>组织方式</b>按 agent 相对于机器人部署策略的位置（Seat）分成五类；每类从 2022–2025 年的先驱讲到 2026 年，'
      '另设 VLN 与 Real2Sim 两个专题。每篇另记接口、闭环形式、拓扑与 carrier。</div>'
      f'<div><b>主要发现</b>2022 年的工作全部坐在 Controller；此后 Supervisor、Teacher、Designer、Developer 相继出现，'
      f'有效 seat 数从 {eff0:.2f} 升到 {eff1:.2f}，Controller 始终是多数：seat 在增加，而不是迁移。</div></div>')
    toc = [("01", "范围与定义", "两条路线；什么算 agent；三种闭环形式；边界案例"),
           ("02", "脉络地图", f"{n_pio} 篇先驱到 {n_core} 篇 2026 年论文，按年份排开"),
           ("03", "五个 Seat 与两个专题", "每个位置何时起作用、产出交给谁、怎么演变"),
           ("04", "趋势与开放问题", "seat 分布的年度变化；六个开放问题；数据来源")]
    a('<div class="toc">' + "".join(f'<div><span class="n">{n}</span><b>{t}</b><span class="d">{d}</span></div>'
                                    for n, t, d in toc) + '</div>')
    a('</section>')

    # ------------------------------------------------------------------ page 2: scope and tests
    a('<section class="page">')
    a('<div class="kicker">01 <span>· 范围与定义</span></div>')
    a('<h2>两条路线，本综述只讲一条</h2>')
    a('<p class="lead">界线模糊时，看模型是什么，不看输出是什么：通用模型直接出动作算（GPT-6 Astra 在 RoboDojo 上不经微调直接当策略），'
      '具身大模型输出计划也不算。</p>')
    a(f'<figure>{fig_routes()}</figure>')
    a('<h2 style="margin-top:9pt">什么算 agent：一个范围，三条判定</h2>')
    a('<p class="lead">判定对象是「模型 + harness + 环」构成的过程，而不是权重本身；四项全部满足才收录。</p>')
    cards = [("scope", "⓪", "通用大模型", "决策者是 LLM / VLM，原样使用，或为 agent 角色微调后仍通过工具、技能、代码行动",
              ["GPT-6 Astra 直接出动作", "GUAVA 蒸馏出的 4B agent"], ["VLA（π0.5、ECoT）", "分层 VLA（Hi Robot）、WAM"]),
             ("", "①", "显式决策", "输出可检查的决策：计划、技能 / 工具 / VLA 调用、代码、约束、裁决、系统编辑或动作",
              ["SayCan 选择技能", "Code as Policies 写程序"], ["奖励模型、价值模型、打分器", "embedding、latent"]),
             ("", "②", "决策权", "自己写出选项；或在含停止、重试、重规划、求助、保留 / 回滚的选项中做选择",
              ["Inner Monologue 重规划", "WhenToAsk 决定求助"], ["只给代码枚举的候选打分", "（PIVOT、按 frontier 打分）"]),
             ("", "③", "闭环", "带着自己的决策与后果被再次调用；或写下的约束 / 程序在执行中读实时感知并调整",
              ["Inner Monologue（再决策）", "ReKep（编写闭环）"], ["一次写成的技能序列", "只靠自身预测的「检查」"])]
    parts = []
    for cls, no, title, rule, yes, no_ in cards:
        parts.append(f'<div class="tcard {cls}"><span class="no">{no}</span><h4>{title}</h4><div class="rule">{esc(rule)}</div>'
                     + "".join(f'<div class="yes">✓ {esc(x)}</div>' for x in yes)
                     + "".join(f'<div class="no2">✗ {esc(x)}</div>' for x in no_) + '</div>')
    a('<div class="flow4">' + '<div class="arr">→</div>'.join(parts) + '</div>')
    a('<h3>三种闭环形式（脉络图里卡片的三种样式）</h3>')
    loops = [("re", "chip", "再决策", "同一次运行中，模型带着自己先前的决策和后果证据被再次调用，可以修订决策。",
              "SayCan、Inner Monologue、Eureka"),
             ("au", "chip au", "编写闭环", "模型只写一次约束或程序，执行时由求解器读实时感知重解或回溯；随结果而变的逻辑是模型写的。",
              "ReKep（约 10 Hz 重解）、VoxPoser、Code as Policies"),
             ("op", "chip op", "开环（只收先驱）", "计划或约束一次写成、不回到模型；作为开创方向的先驱收录。",
              "ZS-Planners、Socratic Models、CoPa、MOKA")]
    a('<div class="loops">' + "".join(
        f'<div class="lcard"><h4><span class="{cls}" style="--c:#2a78d6">{title}</span></h4>{loop_icon(kind)}'
        f'<div class="d">{esc(d)}</div><div class="ex">{esc(ex)}</div></div>' for kind, cls, title, d, ex in loops) + '</div>')
    a('<div class="notes"><div><b>两个例外。</b>约束 / 关键点编程（VLM 写约束交给求解器，如 CoPa、MOKA）和 agentic Real2Sim'
      '（agent 从真实数据重建可交互的仿真场景）即使一次写成也收录，标为开环。</div>'
      '<div><b>不收。</b>' + "".join(f'<span class="pill">{x}</span>' for x in
                                       ("VLA 与分层 VLA", "世界动作模型", "机器人基础模型", "奖励 / 价值模型", "游戏与文本世界",
                                        "纯数字 agent")) +
      '　离散仿真（ALFRED、R2R）与自动驾驶只在边界一节讨论。</div></div>')
    cases = [("Prompt a Robot to Walk", "yes", "收 · 先驱", "通用 LLM 以观测-动作历史为提示，逐步直接输出关节动作"),
             ("Harness VLA ★", "yes", "收 · 2026", "冻结的 VLA 只是被 coding agent 调度的工具，agent 跨 episode 记忆"),
             ("KnowNo", "pio", "先驱 · 开环", "不确定时请人从选项中挑选，人替代了模型的再决策"),
             ("SayPlan", "pio", "先驱 · 边界", "3D 场景图上迭代重规划，但证据主要来自符号层面的模拟"),
             ("PIVOT", "no", "不收", "VLM 只在代码采样的候选动作中打分，循环与候选都归代码"),
             ("π0.5 · ECoT", "no", "不收", "具身大模型直接出动作，即使带推理链或子任务文本")]
    a('<h3>边界案例怎么判</h3><div class="cases">' + "".join(
        f'<div class="case"><span class="vd {k}">{v}</span><b>{esc(n)}</b><span class="why">{esc(w)}</span></div>'
        for n, k, v, w in cases) + '</div>')
    a('</section>')

    # ------------------------------------------------------------------ page 3: lineage map
    a('<section class="page">')
    a('<div class="kicker">02 <span>· 脉络地图</span></div>')
    a('<h2>从先驱到 2026：每个 seat 都有自己的源头</h2>')
    a(f'<p class="lead">每行是一条研究脉络，每张卡片是核心表中的一篇论文（共 {n_pio} 篇先驱、{n_core} 篇 2026 年论文，这里各取代表）。'
      '2022 年的论文都坐在 Controller（含导航的 LM-Nav）；2023 年起其余 seat 依次出现，2026 年每一行都铺满。</p>')
    a(lineage(rows, trend))
    a('<div class="reads">'
      '<div><b>2022：一切从 Controller 开始</b>SayCan 选技能、Inner Monologue 听反馈、Code as Policies 写程序，'
      '奠定「通用模型 + 外部技能 + 反馈」的形态。</div>'
      '<div><b>2023–2025：新 seat 依次出现</b>REFLECT 监督失败，SUDD 生成经检验的示范，Eureka 迭代奖励，'
      'RoboMorph 改造身体本身。</div>'
      '<div><b>2026：agent 退到身体后面</b>VLA 成了被调用的工具，coding agent 改写策略与系统（ENPIRE、PhysEvo），'
      '通用模型也能直接当策略。</div></div>')
    a('</section>')

    # ------------------------------------------------------------------ page 4: seat cards
    a('<section class="page">')
    a('<div class="kicker">03 <span>· 五个 Seat 与两个专题</span></div>')
    a('<h2>谁在什么时候、对身体做什么</h2>')
    a('<p class="lead">每张卡片：这个位置的 agent 何时起作用、产出交给谁；代表性的源头与 2026 年工作；一句话的变化。'
      '底部条形是它在 2026 年全部 core 论文（全量检索）中所占的比例。</p>')
    cs = [scard(rows, "Controller", "Controller", "控制者", "运行时，每一步；产出由机器人直接执行",
                ["SayCan", "Code as Policies", "ReKep"], ["Thea", "Show-Harness", "Astra on RoboDojo"],
                "三条支线：<b>编排型</b>从选技能走到编排 VLA 与 coding-agent harness；<b>直接驱动型</b>从写程序、写约束走到"
                "通用模型直接当策略；<b>lifelong</b> 从技能库与记忆走到和所调用的 VLA 共同进化（Robo-COP）。",
                share26["Controller"]),
          scard(rows, "Supervisor", "Supervisor", "监督者", "运行时，只在异常时介入；门控、否决或恢复",
                ["REFLECT", "Safety Chip", "Code-as-Monitor"], ["Agentic Task Graph", "Zetta"],
                "从事后解释失败，到把自然语言安全规范译成时序逻辑在运行时强制执行，再到预先写好恢复分支（Agentic Task Graph）、"
                "从 rollout 中进化监控器并经验证才保留（Zetta）。", share26["Supervisor"]),
          scard(rows, "Teacher", "Teacher", "教师", "部署前，亲自执行；经检验的经验成为训练目标",
                ["SUDD", "RobotGPT", "RoboTwin 2.0"], ["GUAVA", "CAPEX"],
                "先是 LLM 规划并检验、生成示范数据蒸馏成策略；2026 年出现 agent 教 agent：前沿 VLM 在 harness 中的轨迹"
                "蒸馏成同一套接口的 4B agent（GUAVA）。", share26["Teacher"]),
          scard(rows, "Designer", "Designer", "设计者", "部署前，设计学习问题：奖励、任务、场景、课程",
                ["Eureka", "RoboGen", "OMNI-EPIC"], ["SceneSmith", "FIND"],
                "从一次写出奖励，到依训练结果迭代奖励与课程，再到多个 agent 协作搭建可仿真的场景，"
                "以及在真机上依成功率挑选练习任务（FIND）。", share26["Designer"]),
          scard(rows, "Developer", "Developer", "开发者", "部署前，修改系统本身；自己的试验决定保留或回滚",
                ["RoboMorph", "RobotSmith"], ["ENPIRE", "PhysEvo", "AdaHVLA"],
                "最晚出现、2026 年增长最快的 seat：先驱在设计形态与工具，2026 年的 coding agent 改写策略与训练代码、"
                f"编辑协调 VLA 的 harness，真机试验决定去留。占比从 2024 年的 {dev['2024']:.0f}% 升到 {dev['2026']:.0f}%。",
                share26["Developer"]),
          scard(rows, None, ("vln",), "VLN 与具身导航", "专题：以导航为主任务的 agent（seat 照常标注）",
                ["LM-Nav", "NavGPT", "CA-Nav"], ["HarnessVLN", "OnFly", "Air-Ground VLN"],
                "从 LLM 抽取地标、在离散图上逐步推理，到连续环境与真机上的零样本导航；2026 年导航 agent 也 harness 化，"
                "并上了无人机、走向空地协同。", col=MUTED),
          scard(rows, None, tuple(R.R2S_THEMES), "Real2Sim / Sim2Real", "子方向：agent 自己搭练习场，只收代表作",
                ["DrEureka", "Articulate AnyMesh"], ["Agentic Real2Sim", "RPG", "SimEX"],
                "agent 从真实录像重建可仿真的孪生，在里面练习、诊断、改进，再把技能带回真机（Real2Sim2Real）；"
                "与 Designer、Developer 交叉。", col=MUTED)]
    iface = Counter(r["interface"] for r in csv.DictReader(open(os.path.join(R.ROOT, "data/core/fine_labels.csv")))
                    if r["verdict"] == "core" and r.get("pass") in R.STRONG and R.year_of(r) == "2026")
    tot = sum(iface.values())
    ib = [("skill-call", "技能调用"), ("code", "代码"), ("problem-spec", "问题规格"), ("constraint", "约束"),
          ("system-edit", "系统编辑"), ("micro-action", "语义微动作"), ("vla-call", "VLA 调用")]
    bars = "".join(f'<div class="ibar"><span>{zh}</span><span class="tr"><span class="fl" style="width:{100 * iface[k] / iface["skill-call"]:.0f}%">'
                   f'</span></span><span class="n">{iface[k]}</span></div>' for k, zh in ib)
    cs.append('<div class="scard" style="--c:#0b0b0b"><div class="hd"><span class="nm">每篇还记四个维度</span></div>'
              '<div class="when">接口 · 闭环形式 · 拓扑（单 agent、1:N 调度多机、×N 多 agent）· carrier（G 原样 / C 微调）</div>'
              f'<p style="margin-bottom:3pt">harness 与 multi-agent 不是类别，而是这些维度上的取值。下图：2026 年 {tot} 篇 core 论文的接口分布，'
              'VLA 调用与系统编辑是两年间增长最快的两类。</p>' + bars + '</div>')
    a('<div class="cards">' + "".join(cs) + '</div>')
    a('</section>')

    # ------------------------------------------------------------------ page 5: trends and open problems
    a('<section class="page">')
    a('<div class="kicker">04 <span>· 趋势与开放问题</span></div>')
    a('<h2>seat 在增加，而不是迁移</h2>')
    a(f'<p class="lead">核心表按名额挑选，不能当趋势证据；这里用全部经 Sonnet 判定或复核为 core、有日期的 {sum(x["n"] for x in trend)} 篇论文。'
      '2026 年是全量检索；2022–2025 年来自种子论文的引用邻域与联网补漏，所以只比较各年内部的结构。</p>')
    a('<div class="tiles">'
      f'<div class="tile"><div class="v">{eff0:.2f}<span>→</span>{eff1:.2f}</div><div class="l">有效 seat 数，2022 → 2026</div>'
      '<div class="s">各 seat 论文数分布的熵取指数；逐年上升：' + "、".join(f"{t[y]['eff']:.2f}" for y in YEARS) + '</div></div>'
      f'<div class="tile"><div class="v">{100 * ctl["2023"]:.0f}%<span>→</span>{100 * ctl["2026"]:.0f}%</div>'
      '<div class="l">含 Controller 的论文占比，2023 → 2026</div><div class="s">逐年下降，但始终是多数：新 seat 出现时，旧的没有被取代</div></div>'
      f'<div class="tile"><div class="v">{dev["2024"]:.0f}%<span>→</span>{dev["2026"]:.0f}%</div>'
      '<div class="l">以 Developer 为主 seat 的占比，2024 → 2026</div><div class="s">2026 年与 Designer 并列第二大 seat，各占约十分之一</div></div>'
      '</div>')
    a(f'<figure>{R.fig_share(trend)}<figcaption><b>图 2　各年份主 seat 的占比。</b>每篇论文按主 seat 计一次；n 为该年的论文数。'
      '2022 年全部是 Controller；Supervisor、Teacher、Designer 在 2023 年出现，Developer 在 2024 年后成形。</figcaption></figure>')
    a('<h2 style="margin-top:6pt">开放问题</h2>')
    probs = [("评测", "agent 与策略怎么比", "RoboDojo 让通用模型当策略、与公开策略同榜；闭环质量、token 成本与延迟还没有统一的度量。"),
             ("边界", "通用模型还是 VLA", "通用模型直接出动作与 VLA 越来越像。现在按「模型是什么」判定，需要更可操作的标准。"),
             ("安全", "监督者太少", f"Supervisor 只占 2026 年 core 论文的 {share26['Supervisor']:.0f}%；运行时护栏、越狱攻击下的物理风险刚开始被研究。"),
             ("自我改进", "保留还是回滚", "Developer 与 Designer 用试验决定去留（ENPIRE、PhysEvo）；试验成本、统计可靠性与回滚本身的安全缺少研究。"),
             ("练习场", "自己搭的仿真可信吗", "agent 从录像重建仿真并在其中练习（RPG、Agentic RSR）；重建的保真度决定技能能否回到真机。"),
             ("教给谁", "从教策略到教 agent", "GUAVA 把前沿 VLM 蒸馏成 4B agent；小模型是否保留了 agency、能否跨身体迁移，尚无答案。")]
    a('<div class="probs">' + "".join(f'<div class="prob"><div class="k">{k}</div><h4>{h}</h4><p>{esc(p)}</p></div>'
                                      for k, h, p in probs) + '</div>')
    steps = [(f"{c['cand']:,}", "篇引用收割候选<br>（14 篇种子论文）"), (f"+{c['s2']:,}", "篇 2026 关键词检索命中<br>+ 三轮联网补漏"),
             (f"{c['judged']:,}", "篇逐篇判定<br>Haiku 初判、Sonnet 复核"), (f"{c['strong26'] + c['strong_pre']:,}", "篇满足定义<br>（2022–2026）"),
             (f"{n_pio + n_core + n_res}", "篇核心表<br>全部经 arXiv 核验")]
    a('<div class="method"><div class="mflow">' + '<div class="a">→</div>'.join(
        f'<div class="m{" last" if k == len(steps) - 1 else ""}"><b>{v}</b>{l}</div>' for k, (v, l) in enumerate(steps)) + '</div>'
      f'<div class="fine">凡 Haiku 判为 core、先驱或边界的论文都由 Sonnet 从头复核（{c["ver"]:,} 篇）；抽查 Haiku 判为 out 的 {c["audit"]} 篇，'
      f'漏判 core 约 {100 * c["audit_core"] / max(c["audit"], 1):.1f}%。满足定义但未入表的论文列在 README 的扩展列表'
      f'（2026 年 {c["ext"]} 篇、2022–2025 年 {c["ext_pre"]} 篇）。待定：主线措辞；副轴（Carrier 只剩 G / C，建议改用接口）；'
      f'规模（先驱 {n_pio} + 2026 年 {n_core}）。</div></div>')
    a('</section>')

    css = (R.CSS + CSS).replace("FONTDIR", "file://" + os.path.abspath(fontdir)) if fontdir else \
        re.sub(r"@font-face[^}]*}", "", R.CSS + CSS)
    return (f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>Agentic Embodiment 综述预览</title>'
            f'<style>{css}</style></head><body>{"".join(H)}</body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", default=os.path.join(os.path.expanduser("~"), ".cache", "aae-report-fonts"))
    ap.add_argument("--out", default=os.path.join(R.ROOT, "docs", "survey_brief.pdf"))
    ap.add_argument("--html", default=None, help="also keep the intermediate HTML here")
    args = ap.parse_args()
    page = build_html(R.ensure_fonts(args.fonts))
    tmp = args.html or os.path.join(tempfile.mkdtemp(), "brief.html")
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
