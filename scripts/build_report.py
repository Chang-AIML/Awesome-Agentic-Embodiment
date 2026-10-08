#!/usr/bin/env python3
"""Build the Chinese progress report (PDF with figures) from the core-table data.

Reads data/core/{core_table.csv, core_meta.json, fine_labels.csv, pool.jsonl} plus the screening
files, draws the figures as inline SVG / HTML, and prints the page with headless Chromium
(Playwright, scripts/print_pdf.cjs). Font: Noto Sans SC TTFs in --fonts (downloaded from Google
Fonts into that directory when missing); falls back to an installed CJK sans.

Usage: python3 scripts/build_report.py [--fonts DIR] [--out docs/progress_report.pdf] [--html PATH]
"""
import argparse, csv, html, json, os, re, subprocess, sys, tempfile, urllib.request
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_readme import venue_of  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
esc = html.escape

SEATS = ["Controller", "Supervisor", "Teacher", "Designer", "Developer"]
SEAT_ZH = {"Controller": "控制者", "Supervisor": "监督者", "Teacher": "教师", "Designer": "设计者", "Developer": "开发者"}
# Categorical slots 1-5 of the dataviz reference palette (validated: adjacent CVD/normal-vision pass;
# slots 3-5 are below 3:1 on the surface, so every chart carries labels and a table twin).
COLOR = {"Controller": "#2a78d6", "Supervisor": "#eb6834", "Teacher": "#1baf7a", "Designer": "#eda100",
         "Developer": "#e87ba4"}
INK, INK2, MUTED, GRID, BASE, SURFACE = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
SEQ = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5"]  # sequential blue steps 100/200/300/400
NAMED = {"GUAVA", "Harness VLA", "Show-Harness", "ENPIRE", "Code-as-Monitor"}
SUB_ZH = {"orchestrator": "编排型", "direct": "直接驱动型", "lifelong": "lifelong / memory 型", "trained": "训练过的 carrier"}
IFACE_ZH = {"skill-call": "技能调用", "vla-call": "VLA 调用", "micro-action": "语义微动作", "code": "代码",
            "constraint": "约束", "verdict": "裁决", "trace": "执行轨迹", "problem-spec": "问题规格",
            "system-edit": "系统编辑", "message": "消息", "-": "–", "": "–"}
BODY_ZH = {"manip": "操作", "mobile-manip": "移动操作", "nav": "导航", "loco": "足式", "humanoid": "人形",
           "multi-robot": "多机器人", "aerial": "空中", "driving": "驾驶", "social": "社交", "other": "其他"}
FID_ZH = {"real": "真机", "sim": "仿真", "sim+real": "仿真+真机"}
CITATION_RECORDS = 34300  # forward-citation records before dedup (harvest log, HANDOFF.md §2)

# Papers considered but left out for quota (id in fine_labels or gap:<arxiv>), with the reason.
ALTERNATES = [
    ("c00013", "Look Before You Leap", "Controller · 编排型", "早期 GPT-4V 闭环规划（258 引）；与 COME-robot 重叠"),
    ("c02290", "MoMa-LLM", "Controller · 编排型", "动态场景图移动操作（141 引）；与 BUMBLE、COME-robot 同类"),
    ("c01673", "Robix", "Controller · 训练过的", "C 型 carrier，已有 PaLM-E；名额给了 I 型的 MEM"),
    ("c01104", "AgenticNav", "Controller · 直接驱动型", "工具调用式导航；导航方向已有 InstructNav"),
    ("gap:2411.17636", "MALMM", "Controller · 直接驱动型", "多 agent 写代码（×R）；×R 已有 Agentic Robot、Being-0"),
    ("gap:2311.01403", "REAL", "Controller · 直接驱动型", "唯一的无人机候选；想补 aerial 方向可换入"),
    ("c01195", "HarnessPAI", "Developer", "harness 进化；2026 年 Developer 已有 7 篇"),
    ("c00954", "RAPID", "Developer", "从演示做 agentic 编程；同上"),
    ("c00744", "AdaHVLA", "Developer", "自适应 harness（「harness VLA」的另一种读法）；同上"),
    ("gap:2411.18676", "Embodied Red Teaming", "Designer · Examiner", "红队评测子型；是否闭环待全文核实"),
    ("c11104", "RDA", "Designer", "reward 设计 agent；Designer 名额已满"),
    ("c08743", "SAGE", "Designer", "agentic 场景生成；同上"),
    ("gap:2609.33007", "CAPEX", "Teacher", "与 GUAVA 同型的蒸馏"),
    ("c01582", "Zetta", "Supervisor", "进化运行时 critic；seat 介于 Supervisor 与 Developer 之间"),
]
TRIM_TO_60 = ["Agent as Policy", "VIA", "VLMgineer", "Skill2Real", "SUDD"]


# ------------------------------------------------------------------ data

def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


def load():
    p = lambda *x: os.path.join(ROOT, *x)
    rows = list(csv.DictReader(open(p("data/core/core_table.csv"))))
    meta = json.load(open(p("data/core/core_meta.json")))
    fine = list(csv.DictReader(open(p("data/core/fine_labels.csv"))))
    gap = {"gap:" + norm_arxiv(o["arxiv"]): o for o in map(json.loads, open(p("data/core/gap_candidates.jsonl")))}
    pool = [json.loads(l) for l in open(p("data/core/pool.jsonl"))]
    for r in rows:
        m = meta.get(r["arxiv"], {})
        r["year"] = (m.get("published") or r["date"] or "")[:4]
        r["venue"] = venue_of(r, m)
        r["cites"] = m.get("citations")
        r["named"] = r["key"] in NAMED
    year = lambda r: (meta.get(norm_arxiv(r["arxiv"]), {}).get("published") or r["date"] or "????")[:4]
    with open(p("data/candidates/candidates.csv")) as f:
        n_cand = sum(1 for _ in csv.reader(f)) - 1
    coarse = Counter(r["label"] for r in csv.DictReader(open(p("data/screening/coarse_labels.csv"))))
    src = Counter(o["source"].split(";")[0] for o in pool)
    c = dict(records=CITATION_RECORDS, cand=n_cand, prefilter=sum(coarse.values()), relevant=coarse["relevant"],
             maybe=coarse["maybe"], irrelevant=coarse["irrelevant"], pool=len(pool),
             shortlist=len(pool) - src["supplement"] - src["testset"], supplement=src["supplement"],
             testset=src["testset"], verdict=Counter(r["verdict"] for r in fine), gap=len(gap),
             gap_verdict=Counter(o["verdict"] for o in gap.values()),
             tier=Counter(r["tier"] for r in rows), seat=Counter(r["seat"] for r in rows if r["tier"] == "core"),
             verified=sum(1 for r in rows if meta.get(r["arxiv"], {}).get("verified")),
             links=sum(1 for r in rows if re.search(r"https?://", meta.get(r["arxiv"], {}).get("comment", ""))))
    # trend corpus: every stage-2 core verdict
    prim, alls, n = defaultdict(Counter), defaultdict(Counter), Counter()
    for r in fine:
        if r["verdict"] != "core":
            continue
        y = year(r)
        n[y] += 1
        prim[y][r["seat"]] += 1
        for s in {r["seat"]} | {x for x in re.split(r"[+,;/ ]+", r["seat2"]) if x in SEATS}:
            alls[y][s] += 1
    import math
    trend = []
    for y in sorted(n):
        tot = sum(alls[y].values())
        eff = math.exp(-sum(v / tot * math.log(v / tot) for v in alls[y].values() if v))
        trend.append(dict(year=y, n=n[y], prim=prim[y], alls=alls[y], eff=eff))
    # agreement with the first-round test-set placements
    agree = defaultdict(Counter)
    for r in fine:
        if r["testset_tier"]:
            agree[r["testset_tier"].split(" ")[0]][r["verdict"]] += 1
    both = [r for r in fine if r["testset_tier"].startswith("CORE ") or r["testset_tier"] == "CORE"]
    both = [r for r in both if r["verdict"] == "core"]
    seat_same = sum(1 for r in both if r["testset_primary"].split("-")[0].split(" ")[0] == r["seat"])
    alt = []
    fine_by_id = {r["id"]: r for r in fine}
    for i, key, seat, why in ALTERNATES:
        a = norm_arxiv((gap.get(i) or fine_by_id.get(i) or {}).get("arxiv", ""))
        alt.append(dict(key=key, seat=seat, why=why, arxiv=a))
    return rows, c, trend, agree, (seat_same, len(both)), alt


# ------------------------------------------------------------------ drawing helpers

def lum(hexc):
    v = [int(hexc[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    v = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in v]
    return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]


def on(hexc):
    """Label colour inside a fill, by the fill's luminance: white on dark fills (both clear 4.4:1 on the
    mid-blue, white reads better there), ink on everything lighter."""
    return "#ffffff" if lum(hexc) < 0.2 else INK


def text_w(s, size):
    """Rough rendered width: CJK glyphs are 1em, Latin ~0.56em."""
    return sum(size if ord(ch) > 0x2e80 else 0.56 * size for ch in s)


def tint(hexc, a):
    v = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(round(255 - (255 - x) * a) for x in v)


def T(x, y, s, size=10, weight=400, fill=INK2, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}">{esc(s)}</text>')


ARROW_DEFS = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
              f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{INK2}"/></marker></defs>')


def svg(w, h, body, label):
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" role="img" aria-label="{esc(label)}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="NotoSC, \'WenQuanYi Zen Hei\', sans-serif">'
            f'{ARROW_DEFS}{body}</svg>')


def box(x, y, w, h, title, lines, stripe=None, fill="#ffffff", stroke=BASE, title_size=11.5, line_gap=14.5):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1"/>']
    pad = 12
    if stripe:
        out.append(f'<rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{stripe}"/>')
        pad = 16
    out.append(T(x + pad, y + 19, title, title_size, 700, INK))
    for k, ln in enumerate(lines):
        out.append(T(x + pad, y + 19 + 16 + k * line_gap, ln, 9.8, 400, INK2))
    return "".join(out)


def arrow(d, label=None, lx=0, ly=0):
    s = f'<path d="{d}" fill="none" stroke="{INK2}" stroke-width="1.3" marker-end="url(#ah)"/>'
    return s + (T(lx, ly, label, 9.5, 500, MUTED) if label else "")


# ------------------------------------------------------------------ figures

def fig_pipeline(c):
    v = c["verdict"]
    steps = [
        (f"{c['records']:,}", "条引用记录", "14 篇种子论文的前向引用（Semantic Scholar）", "脚本"),
        (f"{c['cand']:,}", "篇去重候选", "合并去重，按引用了几篇种子排序", "脚本"),
        (f"{c['prefilter']:,}", "篇进入粗筛", "关键词或种子重叠预筛", "脚本"),
        (f"{c['relevant'] + c['maybe']:,}", "篇粗筛保留",
         f"判为「相关」{c['relevant']:,} 篇、「可能」{c['maybe']:,} 篇；全部「无关」都经 Sonnet 复核", "Haiku + Sonnet"),
        (f"{c['pool']:,}", "篇判定池",
         f"短名单 {c['shortlist']}（影响力、新兴度）+ 小 seat 补充 {c['supplement']} + 测试集 {c['testset']}", "脚本"),
        (f"{v['core']}", "篇判为 core",
         f"15 个 Sonnet agent 逐篇判定；另有前驱 {v['precursor']}、边界 {v['boundary']}、资源 {v['resource']}、排除 {v['out']}",
         "Sonnet"),
        (f"{c['tier']['core']} + {c['tier']['precursor']} + {c['tier']['resource']}", "核心 + 前驱 + 资源",
         f"人工挑选；联网补漏 {c['gap']} 篇；{c['verified']} 篇全部经 arXiv 核验", "人工 + 联网 agent"),
    ]
    out = ['<div class="flow">']
    for k, (num, unit, desc, who) in enumerate(steps):
        last = " last" if k == len(steps) - 1 else ""
        out.append(f'<div class="step{last}"><div class="rail"><span class="dot"></span></div>'
                   f'<div class="num">{esc(num)}<span class="unit">{esc(unit)}</span></div>'
                   f'<div class="desc">{esc(desc)}</div><div class="who">{esc(who)}</div></div>')
    out.append("</div>")
    return "".join(out)


def fig_flow():
    W, H = 680, 470
    b = []
    b.append(box(20, 8, 330, 38, "一篇论文：标题 + 摘要", [], fill="#ffffff"))
    b.append(box(410, 8, 255, 38, "benchmark、数据集、能力研究 → 资源表", [], fill="#f4f3ef", title_size=10.5))
    b.append(arrow("M350,27 L407,27"))
    qs = [("① 显式决策", ["输出可检查的离散决策：计划、技能 / 工具 / VLA", "调用、代码、裁决、对系统的编辑"]),
          ("② 决策权", ["自己写出选项；或在含 stop / retry / replan /", "ask 等控制行为的选项中做选择"]),
          ("③ 闭环", ["带着自己先前的决策记录和执行后果被再次调用，", "并能修订先前的决策"]),
          ("④ 机器人身体与保真度", ["真机，或失败可能由物理原因引起的仿真", "（接触、滑动、碰撞）"])]
    exits = [("OUT · 器官或执行器", ["反应式 VLA（OpenVLA、π0）、打分器 / 奖励", "模型、world model 预测（归 WAM）"], "#f4f3ef", BASE),
             ("OUT · 没有决策权", ["只给代码枚举的同类候选打分，", "控制流归代码（SG-Nav、PIVOT）"], "#f4f3ef", BASE),
             ("PRECURSOR · 前驱（若为奠基作）", ["一次写出程序或约束后不再调用：", "Code as Policies、VoxPoser、ECoT、π0.5"],
              tint(MUTED, 0.16), MUTED),
             ("BOUNDARY · 边界", ["离散或脚本化仿真（ALFRED、AI2-THOR）、", "自动驾驶；进 lineage 表"], "#f4f3ef", BASE)]
    y = 66
    b.append(arrow("M185,46 L185,63"))
    for k, ((qt, ql), (et, el, ef, es)) in enumerate(zip(qs, exits)):
        b.append(box(20, y, 330, 64, qt, ql))
        b.append(box(410, y, 255, 64, et, el, fill=ef, stroke=es, title_size=10.8))
        b.append(arrow(f"M350,{y + 32} L407,{y + 32}", "否", 372, y + 26))
        b.append(arrow(f"M185,{y + 64} L185,{y + 85}", "是", 193, y + 79))
        y += 88
    b.append(box(20, y, 330, 54, "CORE · 核心", ["接着判 Seat（坐在哪里）与 Carrier（谁的权重）"],
                 fill=tint(COLOR["Controller"], 0.12), stroke=COLOR["Controller"]))
    return svg(W, max(H, y + 60), "".join(b), "agent 判定流程图")


def fig_seats():
    W, H = 680, 388
    b = [T(150, 16, "部署前 · pre-deployment", 11.5, 700, INK, "middle"),
         T(150, 31, "agent 的产出冻结后，再交给部署的系统", 9.5, 400, MUTED, "middle"),
         T(525, 16, "评测 / 部署时 · runtime", 11.5, 700, INK, "middle"),
         T(525, 31, "agent 在评测 episode 中被调用", 9.5, 400, MUTED, "middle"),
         f'<line x1="338" y1="6" x2="338" y2="{H - 26}" stroke="{BASE}" stroke-width="1"/>']
    left = [("Designer", 44, ["为学习者设计问题：reward、成功判据、", "任务、环境、课程、评测套件",
                              "例：Eureka、DrEureka、Eurekaverse、FIND"]),
            ("Teacher", 162, ["亲自执行、经结果检验的轨迹或 playbook，", "成为部署模型的训练目标",
                              "例：GUAVA ★、RoboTwin 2.0、Manipulate-Anything"]),
            ("Developer", 280, ["修改系统本身：策略代码、技能库、harness、", "训练代码、硬件；自己的实验决定保留或回滚",
                                "例：ENPIRE ★、RHO、ASPIRE、RoboMorph"])]
    for seat, y, lines in left:
        b.append(box(8, y, 286, 88, f"{seat} · {SEAT_ZH[seat]}", lines, stripe=COLOR[seat], fill=tint(COLOR[seat], 0.07)))
    b.append(box(380, 44, 292, 88, "Controller · 控制者",
                 ["每一步决定机器人做什么：计划、调用技能或", "VLA、写当下执行的代码、发语义微动作",
                  "例：SayCan、Harness VLA ★、Show-Harness ★"], stripe=COLOR["Controller"],
                 fill=tint(COLOR["Controller"], 0.07)))
    b.append(box(380, 280, 292, 88, "Supervisor · 监督者",
                 ["只在异常时介入：门控、否决、失败检测与", "恢复；检查过程独立于名义决策者",
                  "例：Code-as-Monitor ★、REFLECT、DoReMi"], stripe=COLOR["Supervisor"],
                 fill=tint(COLOR["Supervisor"], 0.07)))
    b.append(f'<rect x="446" y="176" width="158" height="64" rx="8" fill="#ffffff" stroke="{INK2}" stroke-width="1.4"/>')
    b.append(T(525, 202, "机器人身体", 13, 700, INK, "middle"))
    b.append(T(525, 222, "+ 部署的策略", 10, 400, INK2, "middle"))
    b.append(arrow("M525,132 L525,173", "持续驱动", 533, 157))
    b.append(arrow("M525,280 L525,243", "仅在异常时", 533, 266))
    b.append(arrow("M294,88 C360,88 380,190 443,192"))
    b.append(arrow("M294,206 C360,206 380,208 443,208"))
    b.append(arrow("M294,324 C360,324 380,226 443,224"))
    b.append(T(8, H - 8, "★ 用户点名的案例。Carrier（G / C / H / I）是第二个维度：每个 seat 都记录决策由哪类权重承载。",
               9.3, 400, MUTED))
    return svg(W, H, "".join(b), "五个 Seat 围绕机器人身体的示意图").replace('width="100%"', 'width="93%"', 1)


def fig_grid(rows):
    core = [r for r in rows if r["tier"] == "core"]
    cells = defaultdict(list)
    for r in core:
        cells[(r["seat"], r["carrier"].split("→")[0].strip())].append(r)
    heads = [("G", "作者未做具身训练的通用模型"), ("C", "训练过的决策者 + 通用执行器"),
             ("H", "训练过的决策者 + 协同设计的执行器"), ("I", "同一个模型既决策又出动作")]
    bins = [(1, 2, SEQ[0]), (3, 5, SEQ[1]), (6, 9, SEQ[2]), (10, 999, SEQ[3])]
    fill = lambda n: next(c for lo, hi, c in bins if lo <= n <= hi)
    out = ['<table class="grid"><tr><th class="seatcol">Seat</th>']
    out += [f'<th><b>{k}</b><br><span>{esc(d)}</span></th>' for k, d in heads] + ['<th class="tot">合计</th></tr>']
    for s in SEATS:
        out.append(f'<tr><td class="seatcol"><span class="sw" style="background:{COLOR[s]}"></span>'
                   f'<b>{s}</b><br><span class="zh">{SEAT_ZH[s]}</span></td>')
        for k, _ in heads:
            xs = sorted(cells[(s, k)], key=lambda r: (not r["named"], -(r["cites"] or 0)))
            if not xs:
                out.append('<td class="empty">·</td>')
                continue
            f = fill(len(xs))
            names = "、".join(r["key"] + (" ★" if r["named"] else "") for r in xs[:2]) + ("…" if len(xs) > 2 else "")
            mig = sum(1 for r in xs if "→" in r["carrier"])
            extra = f"<br>含 {mig} 篇 G→C 迁移" if mig else ""
            out.append(f'<td style="background:{f};color:{on(f)}"><b class="n">{len(xs)}</b>'
                       f'<span class="ex">{esc(names)}{extra}</span></td>')
        out.append(f'<td class="tot">{sum(len(cells[(s, k)]) for k, _ in heads)}</td></tr>')
    out.append("</table>")
    out.append('<div class="binlegend">篇数：' + "".join(
        f'<span><i style="background:{c}"></i>{lo}–{hi}</span>' if hi < 999 else f'<span><i style="background:{c}"></i>≥{lo}</span>'
        for lo, hi, c in bins) + '<span>★ 用户点名</span></div>')
    return "".join(out)


def fig_matrix(rows):
    years = ["2022", "2023", "2024", "2025", "2026"]
    lanes = [(("Controller", SUB_ZH[s].replace(" / memory", "")), "Controller", lambda r, s=s: r["tier"] == "core" and r["seat"] == "Controller"
              and r["sub"] == s) for s in ("orchestrator", "direct", "lifelong", "trained")]
    lanes += [((s, SEAT_ZH[s]), s, lambda r, s=s: r["tier"] == "core" and r["seat"] == s) for s in SEATS[1:]]
    lanes.append((("前驱", "precursor"), None, lambda r: r["tier"] == "precursor"))
    out = ['<table class="matrix"><colgroup><col style="width:15%"><col style="width:15%"><col style="width:12%">'
           '<col style="width:18%"><col style="width:17%"><col style="width:23%"></colgroup><tr><th></th>']
    out += [f"<th>{y}</th>" for y in years] + ["</tr>"]
    for label, seat, f in lanes:
        xs = [r for r in rows if f(r)]
        col = COLOR[seat] if seat else MUTED
        out.append(f'<tr class="{"pre" if seat is None else ""}"><td class="lane"><span class="sw" style="background:{col}"></span>'
                   f'<b>{esc(label[0])}</b><br><span class="lsub">{esc(label[1])} · {len(xs)}</span></td>')
        for y in years:
            chips = sorted([r for r in xs if r["year"] == y], key=lambda r: r["date"])
            out.append("<td>" + "".join(
                f'<span class="chip" style="--c:{col}">{esc(r["key"])}{" ★" if r["named"] else ""}</span>' for r in chips)
                + "</td>")
        out.append("</tr>")
    out.append("</table>")
    return "".join(out)


def fig_share(trend):
    W, x0, bw, top, rowh, bh = 680, 128, 532, 40, 31, 18
    H = top + rowh * len(trend) + 24
    b = []
    lx = x0
    for s in SEATS:  # legend (always present for >= 2 series)
        b.append(f'<rect x="{lx}" y="10" width="11" height="11" rx="2" fill="{COLOR[s]}"/>')
        b.append(T(lx + 16, 20, f"{s} {SEAT_ZH[s]}", 9.6, 400, INK2))
        lx += 16 + text_w(f"{s} {SEAT_ZH[s]}", 9.6) + 20
    for t in (0, 25, 50, 75, 100):
        x = x0 + bw * t / 100
        b.append(f'<line x1="{x}" y1="{top - 8}" x2="{x}" y2="{top + rowh * len(trend) - 10}" stroke="{GRID}" stroke-width="1"/>')
        b.append(T(x, top + rowh * len(trend) + 4, f"{t}%", 9, 400, MUTED, "middle"))
    for k, t in enumerate(trend):
        y = top + k * rowh
        b.append(T(10, y + 13, f"{t['year']}", 11, 700, INK))
        b.append(T(52, y + 13, f"n = {t['n']}", 9.6, 400, MUTED))
        x = x0
        segs = [(s, t["prim"][s]) for s in SEATS if t["prim"][s]]
        for j, (s, v) in enumerate(segs):
            w = bw * v / t["n"]
            last = j == len(segs) - 1
            ww = w - (0 if last else 2)  # 2px surface gap between touching segments
            if last:  # 4px rounded data-end, square at the baseline side
                r = min(4, ww / 2)
                b.append(f'<path d="M{x},{y} h{ww - r} a{r},{r} 0 0 1 {r},{r} v{bh - 2 * r} a{r},{r} 0 0 1 -{r},{r} '
                         f'h-{ww - r} z" fill="{COLOR[s]}"/>')
            else:
                b.append(f'<rect x="{x}" y="{y}" width="{max(ww, 0.5)}" height="{bh}" fill="{COLOR[s]}"/>')
            pct = round(100 * v / t["n"])
            if ww >= 34:  # label only where it fits with padding
                b.append(T(x + ww / 2, y + 12.8, f"{pct}%", 9.2, 500, on(COLOR[s]), "middle"))
            x += w
    return svg(W, H, "".join(b), "各年份主 seat 占比")


def fig_line(points, ymax, ticks, fmt, label):
    W, H, x0, x1, y0, y1 = 320, 150, 44, 300, 20, 118
    xs = [x0 + (x1 - x0) * k / (len(points) - 1) for k in range(len(points))]
    Y = lambda v: y1 - (y1 - y0) * v / ymax
    b = []
    for t in ticks:
        b.append(f'<line x1="{x0}" y1="{Y(t)}" x2="{x1}" y2="{Y(t)}" stroke="{GRID}" stroke-width="1"/>')
        b.append(T(x0 - 8, Y(t) + 3.5, fmt(t), 9, 400, MUTED, "end"))
    b.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{BASE}" stroke-width="1"/>')
    for x, (yr, _) in zip(xs, points):
        b.append(T(x, y1 + 16, yr, 9, 400, MUTED, "middle"))
    d = " ".join(f"{'M' if k == 0 else 'L'}{x:.1f},{Y(v):.1f}" for k, (x, (_, v)) in enumerate(zip(xs, points)))
    c = COLOR["Controller"]
    b.append(f'<path d="{d}" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>')
    for x, (_, v) in zip(xs, points):
        b.append(f'<circle cx="{x}" cy="{Y(v)}" r="4.5" fill="{c}" stroke="{SURFACE}" stroke-width="2"/>')
    for k in (0, len(points) - 1):  # label the endpoints only
        x, v = xs[k], points[k][1]
        b.append(T(x, Y(v) - 10, fmt(v, True), 10, 700, INK, "middle"))
    return svg(W, H, "".join(b), label)


# ------------------------------------------------------------------ tables

def body_zh(b):
    dom, _, fid = (b or "").partition("/")
    return BODY_ZH.get(dom, dom or "–") + (" · " + FID_ZH.get(fid, fid) if fid else "")


def link(r):
    star = " ★" if r.get("named") else ""
    return f'<a href="https://arxiv.org/abs/{r["arxiv"]}">{esc(r["key"])}</a>{star}'


def table_core(rows, title, pred):
    xs = sorted([r for r in rows if pred(r)], key=lambda r: (r["date"], r["key"]))
    out = [f'<h3>{esc(title)}（{len(xs)}）</h3><table class="tbl"><colgroup><col style="width:15%"><col style="width:5.5%">'
           '<col style="width:7%"><col style="width:6.5%"><col style="width:8.5%"><col style="width:15%"><col></colgroup>'
           '<tr><th>短名</th><th>年份</th><th>会议</th><th>Carrier</th><th>接口</th><th>身体</th><th>入选理由</th></tr>']
    for r in xs:
        out.append(f'<tr><td>{link(r)}</td><td>{r["year"]}</td><td>{esc(r["venue"])}</td><td>{esc(r["carrier"])}</td>'
                   f'<td>{esc(IFACE_ZH.get(r["interface"], r["interface"]))}</td><td>{esc(body_zh(r["body"]))}</td>'
                   f'<td>{esc(r["why"])}</td></tr>')
    out.append("</table>")
    return "".join(out)


# ------------------------------------------------------------------ page

CSS = """
@font-face { font-family: NotoSC; font-weight: 400; src: url("FONTDIR/NotoSansSC-400.ttf"); }
@font-face { font-family: NotoSC; font-weight: 500; src: url("FONTDIR/NotoSansSC-500.ttf"); }
@font-face { font-family: NotoSC; font-weight: 700; src: url("FONTDIR/NotoSansSC-700.ttf"); }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: NotoSC, "WenQuanYi Zen Hei", sans-serif; font-size: 9.4pt; line-height: 1.62; color: #0b0b0b;
       margin: 0; background: #ffffff; }
a { color: #1c5cab; text-decoration: none; }
h1 { font-size: 21pt; line-height: 1.3; margin: 0 0 2pt; font-weight: 700; }
h2 { font-size: 13.5pt; font-weight: 700; margin: 0 0 8pt; padding-bottom: 4pt; border-bottom: 1px solid #e1e0d9; }
h3 { font-size: 10.6pt; font-weight: 700; margin: 12pt 0 5pt; }
h2, h3 { break-after: avoid; page-break-after: avoid; }
p { margin: 0 0 6pt; }
ul, ol { margin: 0 0 6pt; padding-left: 15pt; }
li { margin: 1.5pt 0; }
.section { break-before: page; }
.sub { color: #52514e; font-size: 10pt; margin-bottom: 10pt; }
.defn { border-left: 4px solid #2a78d6; background: #f5f9fe; padding: 8pt 11pt; margin: 8pt 0 10pt; border-radius: 0 6px 6px 0; }
.defn .en { color: #52514e; font-size: 8.6pt; line-height: 1.5; margin-top: 4pt; }
.thesis { font-weight: 700; font-size: 10.6pt; margin: 6pt 0 2pt; }
.kpis { display: grid; grid-template-columns: repeat(5, 1fr); gap: 7pt; margin: 10pt 0 12pt; }
.kpi { border: 1px solid #e1e0d9; border-radius: 8px; padding: 7pt 9pt; background: #fcfcfb; }
.kpi .v { font-size: 17pt; font-weight: 700; line-height: 1.15; }
.kpi .l { font-size: 8.3pt; color: #52514e; line-height: 1.35; margin-top: 2pt; }
.callout { border: 1px solid #e1e0d9; border-radius: 8px; padding: 8pt 11pt; background: #fcfcfb; margin: 8pt 0; break-inside: avoid; }
.callout h3 { margin-top: 0; }
.ask { border-color: #eb6834; background: #fff8f4; }
figure { margin: 8pt 0 10pt; break-inside: avoid; text-align: left; }
figcaption { font-size: 8.4pt; color: #52514e; line-height: 1.5; margin-top: 5pt; }
figcaption b { color: #0b0b0b; }
.note { font-size: 8.4pt; color: #52514e; }
.flow { border: 1px solid #e1e0d9; border-radius: 8px; padding: 6pt 10pt; background: #fcfcfb; }
.step { display: grid; grid-template-columns: 14pt 152pt 1fr 80pt; align-items: center; min-height: 30pt; }
.step .rail { align-self: stretch; position: relative; }
.step .rail::before { content: ""; position: absolute; left: 4pt; top: 0; bottom: 0; width: 1.5px; background: #c3c2b7; }
.step:first-child .rail::before { top: 50%; }
.step.last .rail::before { bottom: 50%; }
.step .dot { position: absolute; left: 1pt; top: calc(50% - 4pt); width: 8pt; height: 8pt; border-radius: 50%;
             background: #9ec5f4; border: 2px solid #fcfcfb; }
.step.last .dot { background: #2a78d6; }
.step .num { font-size: 14pt; font-weight: 700; white-space: nowrap; }
.step .unit { font-size: 8.4pt; font-weight: 400; color: #52514e; margin-left: 3pt; }
.step .desc { font-size: 8.6pt; color: #52514e; padding-right: 6pt; line-height: 1.45; }
.step .who { font-size: 7.8pt; color: #52514e; text-align: center; border: 1px solid #e1e0d9; border-radius: 10px; padding: 1pt 4pt; background: #fff; }
.step.last .num { color: #1c5cab; }
table { border-collapse: collapse; width: 100%; }
.grid { table-layout: fixed; font-size: 8.2pt; }
.grid th { font-weight: 400; color: #52514e; text-align: left; vertical-align: bottom; padding: 3pt 5pt; border-bottom: 1px solid #c3c2b7; line-height: 1.35; }
.grid th b { color: #0b0b0b; font-size: 11pt; }
.grid th span { font-size: 7.6pt; }
.grid td { padding: 4pt 6pt; vertical-align: top; border: 2px solid #ffffff; line-height: 1.32; height: 31pt; }
.grid td.empty { color: #c3c2b7; text-align: center; vertical-align: middle; background: #fcfcfb; }
.grid .n { font-size: 13pt; display: block; line-height: 1.2; }
.grid .ex { font-size: 7.4pt; }
.grid .seatcol { width: 15%; }
.grid .tot { width: 7%; text-align: center; vertical-align: middle; font-weight: 700; font-size: 11pt; color: #0b0b0b; }
.grid th.tot { font-size: 8.2pt; font-weight: 400; color: #52514e; vertical-align: bottom; }
.sw { display: inline-block; width: 8pt; height: 8pt; border-radius: 2px; margin-right: 4pt; vertical-align: -0.5pt; }
.zh { color: #52514e; font-size: 7.8pt; margin-left: 12pt; }
.binlegend { font-size: 7.8pt; color: #52514e; margin-top: 4pt; }
.binlegend span { margin-right: 10pt; }
.binlegend i { display: inline-block; width: 9pt; height: 9pt; border-radius: 2px; vertical-align: -1pt; margin-right: 3pt; }
.matrix { table-layout: fixed; font-size: 7.3pt; }
.matrix th { font-size: 9pt; color: #52514e; font-weight: 700; text-align: left; padding: 2pt 4pt; border-bottom: 1px solid #c3c2b7; }
.matrix td { border-bottom: 1px solid #e1e0d9; padding: 3pt 3pt; vertical-align: top; }
.matrix td.lane { font-size: 8pt; color: #0b0b0b; line-height: 1.35; padding-top: 4pt; }
.matrix .lsub { color: #52514e; margin-left: 12pt; font-size: 7.4pt; }
.matrix tr.pre td { border-top: 1px solid #c3c2b7; }
.chip { display: inline-block; line-height: 1.3; padding: 1.2pt 4pt 1.2pt 4pt; margin: 1.3pt 2pt 1.3pt 0;
        border-radius: 3px; border-left: 3px solid var(--c); background: color-mix(in srgb, var(--c) 13%, white); white-space: nowrap; }
.charts2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14pt; }
.charts2 h4 { font-size: 9.4pt; margin: 0 0 1pt; font-weight: 700; }
.charts2 .s { font-size: 8pt; color: #52514e; margin-bottom: 2pt; }
.tbl { font-size: 7.9pt; line-height: 1.45; table-layout: fixed; }
.tbl th { text-align: left; font-weight: 500; color: #52514e; border-bottom: 1px solid #c3c2b7; padding: 3pt 4pt; }
.tbl td { border-bottom: 1px solid #e1e0d9; padding: 3pt 4pt; vertical-align: top; overflow-wrap: anywhere; }
.tbl tr { break-inside: avoid; }
.tbl .num { text-align: right; font-variant-numeric: tabular-nums; }
.small { font-size: 8.4pt; }
"""


def build_html(fontdir):
    rows, c, trend, agree, (seat_same, seat_n), alt = load()
    v = c["verdict"]
    seat = c["seat"]
    core = [r for r in rows if r["tier"] == "core"]
    sub = Counter(r["sub"] for r in core if r["seat"] == "Controller")
    n_core, n_pre, n_res = c["tier"]["core"], c["tier"]["precursor"], c["tier"]["resource"]
    t = {x["year"]: x for x in trend}
    dev = {y: x["alls"]["Developer"] / x["n"] for y, x in t.items()}
    ctl = {y: x["alls"]["Controller"] / x["n"] for y, x in t.items()}
    y26 = sum(1 for r in core if r["year"] == "2026")
    pct = lambda f: f"{round(100 * f)}%"
    H = []
    a = H.append

    # ---------------------------------------------------------- page 1: summary
    a('<h1>Agentic Embodiment 综述 · 第二轮进展</h1>')
    a('<div class="sub">定义、分类与核心论文表 · 2026-10-08 · 分支 claude/compassionate-sagan-wklsz6</div>')
    a('<div class="defn"><b>一句话定义</b>　Agentic Embodiment 研究由基础模型驱动、做出显式决策的过程：决策的后果作用到机器人身体上，'
      '过程再依据后果的证据重新决策。全文围绕一个问题组织：这个过程相对于机器人部署的策略坐在哪里（<b>Seat</b>），'
      '由哪类权重承载（<b>Carrier</b>）。'
      '<div class="en">Agentic Embodiment studies foundation-model-driven processes that make explicit decisions whose consequences '
      'reach a robot body, and that re-decide on evidence of those consequences. Its organizing question is where such a process '
      'sits relative to the body\'s deployed policy — steering it, guarding it, teaching it, designing its learning problem, or '
      'building its system (Seat) — and which weights carry it (Carrier).</div></div>')
    a('<div class="thesis">主线：Agency spreads around the body — and loop closure, not weights, makes a carrier an agent.</div>')
    a('<p class="note">agency 没有离开机器人，而是在身体周围占据越来越多的位置；一个模型算不算 agent，取决于它是否闭合了'
      '「带着自身记录、依据后果再决策」的环，而不是它用的是哪套权重。</p>')
    kpis = [(f"{c['cand']:,}", "篇候选论文<br>（种子的前向引用）"), (f"{c['pool']:,}", "篇逐篇判定<br>（15 个 Sonnet agent）"),
            (f"{n_core} + {n_pre}", "篇核心 + 前驱<br>（人工挑选）"), (f"{n_res}", "个 benchmark<br>与资源"),
            (f"{c['verified']}/{len(rows)}", "篇经 arXiv 核验<br>（标题全部一致）")]
    a('<div class="kpis">' + "".join(f'<div class="kpi"><div class="v">{k}</div><div class="l">{l}</div></div>' for k, l in kpis)
      + '</div>')
    a('<div class="callout"><h3>本轮结论</h3><ul>'
      '<li><b>框架已定</b>：你确认了四项决策：采用 Seat × Carrier；开环奠基作作为「前驱」进核心表；核心集约 60 篇；'
      '自动驾驶与离散仿真只作边界讨论。</li>'
      f'<li><b>核心表</b>：Controller {seat["Controller"]}、Supervisor {seat["Supervisor"]}、Teacher {seat["Teacher"]}、'
      f'Designer {seat["Designer"]}、Developer {seat["Developer"]}；前驱 {n_pre}；资源 {n_res}。'
      '你点名的 5 篇（GUAVA、Harness VLA、Show-Harness、ENPIRE、Code-as-Monitor）都在表内。</li>'
      f'<li><b>主线有数据支撑</b>：在全部 {v["core"]} 篇判为 core 的论文上，有效 seat 数从 {t["2022"]["eff"]:.2f}（2022）'
      f'升到 {t["2026"]["eff"]:.2f}（2026）；含 Controller 的论文占比 2023–2026 年一直在 '
      f'{pct(min(ctl[y] for y in ("2023", "2024", "2025", "2026")))}–{pct(max(ctl[y] for y in ("2023", "2024", "2025", "2026")))}。'
      'seat 在增加，而不是从 Controller 迁走。</li>'
      f'<li><b>判定可靠</b>：第一轮测试集里判为 CORE 的 {sum(agree["CORE"].values())} 篇，Sonnet 判 core 的有 '
      f'{agree["CORE"]["core"]} 篇，其中 {seat_same} 篇主 seat 一致。</li></ul></div>')
    a('<div class="callout ask"><h3>需要你决定</h3><ol>'
      f'<li><b>规模</b>：现在核心 {n_core} + 前驱 {n_pre} = {n_core + n_pre} 篇，比约定的 60 篇多 {n_core + n_pre - 60} 篇。'
      f'我建议保留，因为仍在「约 60」的范围内；如果要压到 60，建议去掉 {"、".join(TRIM_TO_60)}。</li>'
      '<li><b>候补</b>：附录 B 列了因名额没收的论文。有想换进来的告诉我。</li>'
      '<li><b>合并到 main</b>：所有内容目前在工作分支上，main 上的 README 还是空的。需要的话我开 PR。</li></ol></div>')

    # ---------------------------------------------------------- 1 pipeline
    a('<div class="section"><h2>1　这一轮做了什么</h2>')
    a('<p>第一轮已经把 14 篇种子论文的前向引用收割完，并做了粗筛和短名单。这一轮在此基础上逐篇判定、挑出核心表，并补全元数据。'
      '下图是完整的筛选漏斗，右栏标出每一步由谁完成。</p>')
    a(f'<figure>{fig_pipeline(c)}<figcaption><b>图 1　筛选漏斗。</b>前四步是第一轮的工作，后三步是这一轮。'
      '粗筛用最便宜的 Haiku；逐篇判定要套用细致的定义，所以用 Sonnet；最后一步由人工挑选。</figcaption></figure>')
    a('<h3>这一轮的四个关键做法</h3><ul>'
      f'<li><b>补判定池</b>：短名单按被引数和新兴度取样，会漏掉被引中等、但属于小 seat 的论文，例如 Code-as-Monitor（83 引，2024 年 12 月）。'
      f'所以补了 {c["supplement"]} 篇小 seat 论文（monitor、teacher、developer 等的门槛更低）和 {c["testset"]} 篇第一轮测试集论文。</li>'
      '<li><b>逐篇判定</b>：每个 Sonnet agent 读约 94 篇的标题和摘要，按 rubric 给出 verdict、seat、carrier、子类、接口、'
      '代表性（1–5 分）和一句理由；合并时校验了枚举值和完整性，没有漏标。</li>'
      f'<li><b>联网补漏</b>：一个 agent 用 WebSearch 和 arXiv API 查找池中缺失的公认工作，找到 {c["gap"]} 篇，全部经 arXiv 核验'
      f'（core {c["gap_verdict"]["core"]}、资源 {c["gap_verdict"]["resource"]}、前驱 {c["gap_verdict"]["precursor"]}）。'
      'EmbodiedBench、Embodied Agent Interface 等 benchmark 和 BUMBLE、VLM-PC 由此补入。</li>'
      '<li><b>人工挑选</b>：每个 seat 内按代表性和影响力排序，再兼顾年份、领域（操作、移动操作、导航、足式、人形、多机器人）'
      '和 carrier 的覆盖。每篇写了中文入选理由，见附录 A。</li></ul>')
    a('</div>')

    # ---------------------------------------------------------- 2 definition
    a('<div class="section"><h2>2　定义：什么算 agent</h2>')
    a('<p>判定对象是「模型 + harness + 环」构成的过程，不是权重本身。同一族小模型放进 GUAVA 的 harness 里是 agent，'
      '在 Show-Harness 的单 token 模式下就只是反应式策略。下图是逐篇判定时的顺序：</p>')
    a(f'<figure>{fig_flow()}<figcaption><b>图 2　agent 判定流程。</b>①–③ 是三条 agent 判定，必须全部满足；'
      '④ 决定进核心还是只作边界讨论。③ 不满足的奠基作，按你的决定作为「前驱」进核心表。</figcaption></figure>')
    a('<h3>三个常见误区</h3><ul>'
      '<li><b>RL 微调不等于 agency</b>：SimpleVLA-RL 一类判 OUT，因为没有显式决策。</li>'
      '<li><b>架构内的 memory 不等于 agency</b>：MemoryVLA 一类判 OUT。agent 自己读写的 memory 才计入。</li>'
      '<li><b>多机器人不等于 multi-agent</b>：一个 LLM 调度多台机器人（SMART-LLM），topology 记为 1:N。</li></ul>')
    a('</div>')

    # ---------------------------------------------------------- 3 taxonomy
    a('<div class="section"><h2>3　分类：五个 Seat × 四类 Carrier</h2>')
    a('<p><b>主轴 Seat</b> 回答「agent 坐在哪里」。判定依据是 agent 的输出<b>在什么阶段产生</b>、<b>由谁消费</b>：'
      '评测时被调用的是 Controller 或 Supervisor；部署前产出、冻结后再交给系统的是 Teacher、Designer 或 Developer。</p>')
    a(f'<figure>{fig_seats()}<figcaption><b>图 3　五个 Seat 围绕机器人身体。</b>右侧两个 seat 在评测时工作：Controller 持续驱动，'
      'Supervisor 只在异常时介入。左侧三个 seat 在部署前工作，产出冻结后进入部署的系统。'
      'ENPIRE 部署出去的策略里没有 agent，但它仍是核心样本，因为 agent 坐在 Developer 的位置。</figcaption></figure>')
    a('<p><b>副轴 Carrier</b> 回答「决策由哪类权重承载」。你最初的「agency 在哪里」四类，正好对应 Controller 一行的四列：'
      '外部编排 → G / C；分层双系统 → H；内化 → I；multi-agent 不再是类别，改为 Topology 列。</p>')
    a(f'<figure>{fig_grid(rows)}<figcaption><b>图 4　核心表的 Seat × Carrier 网格。</b>格中是篇数和代表论文，颜色越深篇数越多。'
      '规律很明显：外环的三个 seat（Teacher、Designer、Developer）全部由 G 类通用模型承担；训练过的 carrier（C / H / I）'
      '只出现在评测时的 seat。GUAVA 和 LocalNav 把 G 的行为蒸馏成 C，是目前仅有的跨格迁移。</figcaption></figure>')
    a('</div>')

    # ---------------------------------------------------------- 4 overview
    a('<div class="section"><h2>4　核心论文全景</h2>')
    a(f'<p>下图把 {n_core} 篇核心论文和 {n_pre} 篇前驱按 seat 和 arXiv 首版年份排开。每个色块是一篇论文，★ 是你点名的案例。'
      '完整的表格（会议、carrier、接口、身体、入选理由）见附录 A。</p>')
    a('<h3>Controller 的四个子章</h3>')
    a(f'<p>Controller 在核心表中有 {seat["Controller"]} 篇，正文按接口拆为四个子章：'
      f'<b>编排型</b> {sub["orchestrator"]} 篇（调用技能、工具或 VLA，如 SayCan、BUMBLE）；'
      f'<b>直接驱动型</b> {sub["direct"]} 篇（输出语义微动作或当下执行的代码，如 Show-Harness、CaP-X，对应 robot-use agent 社区）；'
      f'<b>lifelong / memory 型</b> {sub["lifelong"]} 篇（评测期间写入并读取 memory 或技能库，如 Harness VLA、DROC）；'
      f'<b>训练过的 carrier</b> {sub["trained"]} 篇（PaLM-E、Hi Robot、OneTwoVLA 等）。'
      'harness 和 multi-agent 都不是类别：harness 属于接口，multi-agent 属于 topology。</p>')
    a(f'<figure>{fig_matrix(rows)}<figcaption><b>图 5　核心论文按 Seat 与年份分布。</b>从左往右看，2022 年只有 Controller；'
      '2023 年出现 Supervisor 和 Designer；2024 年出现 Teacher 和 Developer；2026 年五个 seat 都很密集。'
      '这只是挑选结果的分布，有名额的影响，趋势证据见第 5 节。</figcaption></figure>')
    a('</div>')

    # ---------------------------------------------------------- 5 trends
    a('<div class="section"><h2>5　趋势证据</h2>')
    a(f'<p>核心表是按名额挑的，不能当趋势证据。所以下面用全部 {v["core"]} 篇判为 core 的论文统计。'
      f'需要注意：判定池按影响力和新兴度取样，2026 年占一半（{t["2026"]["n"]} 篇），所以只看各年内部的结构，不看绝对数量。</p>')
    a(f'<figure>{fig_share(trend)}<figcaption><b>图 6　各年份主 seat 的占比。</b>每篇论文按主 seat 计一次。'
      'Controller 一直是多数，但 2026 年 Developer 一下子占到约五分之一。不足以放下标签的色块，数值见下表。</figcaption></figure>')
    eff_pts = [(x["year"], x["eff"]) for x in trend]
    ctl_pts = [(x["year"], 100 * ctl[x["year"]]) for x in trend]
    a('<figure><div class="charts2">'
      f'<div><h4>有效 seat 数</h4><div class="s">把每年各 seat 的论文数当成分布，取熵的指数；1 表示只有一个 seat</div>'
      f'{fig_line(eff_pts, 4, [0, 1, 2, 3, 4], lambda v, l=False: f"{v:.2f}" if l else f"{v:.0f}", "有效 seat 数")}</div>'
      f'<div><h4>含 Controller 的论文占比</h4><div class="s">主 seat 或次 seat 含 Controller 的论文 ÷ 该年论文数</div>'
      f'{fig_line(ctl_pts, 100, [0, 25, 50, 75, 100], lambda v, l=False: f"{v:.0f}%", "含 Controller 的论文占比")}</div>'
      '</div><figcaption><b>图 7　主线的两个支撑。</b>左：seat 越来越分散（1.00 → 3.60）。'
      '右：含 Controller 的论文占比基本不变（2023 年后在 71%–76%）。两者合起来就是「seat 在增加，而不是迁移」。</figcaption></figure>')
    th = "".join(f"<th class='num'>{s}</th>" for s in SEATS)
    tr = "".join(
        f"<tr><td>{x['year']}</td><td class='num'>{x['n']}</td>"
        + "".join(f"<td class='num'>{x['prim'][s]}（{x['alls'][s]}）</td>" for s in SEATS)
        + f"<td class='num'>{pct(ctl[x['year']])}</td><td class='num'>{pct(dev[x['year']])}</td>"
          f"<td class='num'>{x['eff']:.2f}</td></tr>" for x in trend)
    a('<table class="tbl"><colgroup><col style="width:7%"><col style="width:6%"></colgroup>'
      f'<tr><th>年份</th><th class="num">n</th>{th}<th class="num">含 Controller</th><th class="num">含 Developer</th>'
      f'<th class="num">有效 seat 数</th></tr>{tr}</table>')
    a('<p class="note" style="margin-top:4pt">各 seat 一栏：主 seat 篇数（括号内为主 seat 或次 seat 含该 seat 的篇数）。</p>')
    a('<h3>怎么读这些数字</h3><ul>'
      f'<li><b>Developer 是 2026 年的新现象</b>：含 Developer 的论文 2022–2023 年为 0，2024 年 {pct(dev["2024"])}、2025 年 '
      f'{pct(dev["2025"])}，2026 年 {pct(dev["2026"])}。2024 年的数字来自 RoboMorph、InterPreT、LRLL 等 '
      f'{t["2024"]["alls"]["Developer"]} 篇。</li>'
      '<li><b>结论只在「全部 seat」口径下稳健</b>：一篇论文常有多个 seat，正文必须写明统计单位。</li>'
      '<li><b>还不是独立样本</b>：投稿前应按草稿 §10 的方案，从候选中分层随机抽样，两人盲标后复核这两个趋势。</li></ul>')
    a('</div>')

    # ---------------------------------------------------------- 6 decisions / next
    a('<div style="break-inside: avoid"><h2 style="margin-top:14pt">6　下一步</h2>')
    a(f'<p>需要你决定的三件事见第 1 页。其中规模一项：压到 60 篇时建议去掉 {"、".join(TRIM_TO_60)}，'
      f'这五篇所在的子类里都还有其他代表作；候补的 {len(alt)} 篇见附录 B，比如想补无人机方向，可以把 REAL 换进来。</p>')
    a('<ol>'
      '<li><b>冻结核心表</b>：你审阅后，我按你的意见改 <code>core_selection.csv</code> 并重新生成 README 和这份报告。</li>'
      f'<li><b>补全链接</b>：目前只有 {c["links"]}/{len(rows)} 篇能从 arXiv comment 中提取到项目或代码链接，其余需要联网逐篇查。</li>'
      f'<li><b>全文审计</b>：{y26} 篇 2026 年的核心论文只按摘要判过。优先核实 Agent as Policy、VIA、FAEA、Thea、RATs、Skill2Real '
      '的 seat 和闭环判定。</li>'
      '<li><b>写正文</b>：按 Seat 分章，Controller 拆四个子章；第 5 节的数字作为趋势证据。</li>'
      '<li><b>可选</b>：做一个类似 WAM survey 的 GitHub Pages 浏览器；对已有 survey 做反向滚雪球，进一步提高查全率。</li></ol></div>')

    # ---------------------------------------------------------- appendix A
    a('<div><h2 style="margin-top:16pt">附录 A　核心论文表</h2>')
    a('<p class="note">短名链接到 arXiv；年份为 arXiv 首版；会议来自 Semantic Scholar，未发表的记为 arXiv；★ 为用户点名。'
      'Carrier 中的 G→C 表示从通用模型蒸馏到训练过的模型。</p>')
    for s in ("orchestrator", "direct", "lifelong", "trained"):
        a(table_core(rows, f"Controller · {SUB_ZH[s]}",
                     lambda r, s=s: r["tier"] == "core" and r["seat"] == "Controller" and r["sub"] == s))
    for s in SEATS[1:]:
        a(table_core(rows, f"{s} · {SEAT_ZH[s]}", lambda r, s=s: r["tier"] == "core" and r["seat"] == s))
    a(table_core(rows, "前驱 · precursor", lambda r: r["tier"] == "precursor"))
    a('</div>')

    # ---------------------------------------------------------- appendix B
    a('<div class="section"><h2>附录 B　资源、候补与质量控制</h2>')
    res = sorted([r for r in rows if r["tier"] == "resource"], key=lambda r: (r["seat"] != "Controller", r["date"]))
    a(f'<h3>Benchmark 与资源（{len(res)}）</h3><table class="tbl"><colgroup><col style="width:20%"><col style="width:6%">'
      '<col style="width:9%"><col style="width:11%"><col></colgroup>'
      '<tr><th>短名</th><th>年份</th><th>会议</th><th>评测的 seat</th><th>说明</th></tr>'
      + "".join(f'<tr><td>{link(r)}</td><td>{r["year"]}</td><td>{esc(r["venue"])}</td><td>{r["seat"]}</td>'
                f'<td>{esc(r["why"])}</td></tr>' for r in res) + '</table>')
    a(f'<h3>候补：因名额没收的论文（{len(alt)}）</h3><table class="tbl"><colgroup><col style="width:20%"><col style="width:22%">'
      '<col></colgroup><tr><th>短名</th><th>Seat</th><th>说明</th></tr>'
      + "".join(f'<tr><td><a href="https://arxiv.org/abs/{x["arxiv"]}">{esc(x["key"])}</a></td><td>{esc(x["seat"])}</td>'
                f'<td>{esc(x["why"])}</td></tr>' for x in alt) + '</table>')
    a('<div style="break-inside: avoid"><h3>Sonnet 判定与第一轮测试集判定的对照</h3>')
    a('<p class="small">第一轮的测试集判定用的是复杂版规则（含 CORE-P、UNRESOLVED 等层级）。下表按第一轮的层级分行，'
      '看这一轮 Sonnet 怎么判。Sonnet 对 CORE-P 和 BOUNDARY 偏宽，人工挑选时已按定义纠正。</p>')
    cols = ["core", "precursor", "boundary", "resource", "out"]
    a('<table class="tbl"><tr><th>第一轮层级</th><th class="num">篇数</th>'
      + "".join(f"<th class='num'>判 {x}</th>" for x in cols) + "</tr>"
      + "".join(f"<tr><td>{k}</td><td class='num'>{sum(agree[k].values())}</td>"
                + "".join(f"<td class='num'>{agree[k][x] or '·'}</td>" for x in cols) + "</tr>"
                for k in ("CORE", "CORE-P", "BOUNDARY", "UNRESOLVED", "RESOURCE", "OUT")) + "</table>")
    a(f'<p class="small" style="margin-top:4pt">第一轮 CORE 中，两边都判 core 的 {seat_n} 篇里有 {seat_same} 篇主 seat 一致。</p></div>')
    a('<h3>文件位置</h3><table class="tbl"><colgroup><col style="width:36%"><col></colgroup>'
      '<tr><th>文件</th><th>内容</th></tr>'
      '<tr><td>docs/definition.md</td><td>正文版定义（简化）</td></tr>'
      '<tr><td>docs/definition_draft.md</td><td>完整细则，作为附录和标注指南</td></tr>'
      '<tr><td>data/core/core_selection.csv</td><td>人工挑选的核心表输入；增删论文改这个文件</td></tr>'
      '<tr><td>data/core/core_table.csv</td><td>生成的核心表（含全部标签）</td></tr>'
      '<tr><td>data/core/fine_labels.csv</td><td>1,406 篇的逐篇判定</td></tr>'
      '<tr><td>docs/core_review.md</td><td>中文审阅清单（与附录 A 相同的入选理由）</td></tr>'
      '<tr><td>docs/core_stats.md</td><td>按年份统计 seat 的全部数字</td></tr>'
      '<tr><td>README.md</td><td>awesome list（英文）</td></tr>'
      '<tr><td>HANDOFF.md</td><td>交接文档：流程、文件地图、待办与踩过的坑</td></tr>'
      '<tr><td>scripts/build_report.py</td><td>生成这份报告</td></tr></table>')
    a('</div>')
    css = CSS.replace("FONTDIR", "file://" + os.path.abspath(fontdir)) if fontdir else re.sub(r"@font-face[^}]*}", "", CSS)
    return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>Agentic Embodiment 进展报告</title>' \
           f'<style>{css}</style></head><body>{"".join(H)}</body></html>'


def ensure_fonts(d):
    """Noto Sans SC 400/500/700 TTFs in d; fetched from the Google Fonts CSS API when missing."""
    want = {w: os.path.join(d, f"NotoSansSC-{w}.ttf") for w in (400, 500, 700)}
    if all(os.path.exists(p) for p in want.values()):
        return d
    try:
        os.makedirs(d, exist_ok=True)
        css = urllib.request.urlopen("https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700",
                                     timeout=60).read().decode()
        for w, url in re.findall(r"font-weight: (\d+);\s*src: url\((\S+?\.ttf)\)", css):
            if int(w) in want and not os.path.exists(want[int(w)]):
                with urllib.request.urlopen(url, timeout=300) as r, open(want[int(w)], "wb") as f:
                    f.write(r.read())
        return d if all(os.path.exists(p) for p in want.values()) else None
    except Exception as e:
        print("font download failed, using system CJK font:", e)
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", default=os.path.join(os.path.expanduser("~"), ".cache", "aae-report-fonts"))
    ap.add_argument("--out", default=os.path.join(ROOT, "docs", "progress_report.pdf"))
    ap.add_argument("--html", default=None, help="also keep the intermediate HTML here")
    args = ap.parse_args()
    page = build_html(ensure_fonts(args.fonts))
    tmp = args.html or os.path.join(tempfile.mkdtemp(), "report.html")
    open(tmp, "w").write(page)
    env = dict(os.environ)
    try:
        env["NODE_PATH"] = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip() + \
                           (os.pathsep + env["NODE_PATH"] if env.get("NODE_PATH") else "")
    except FileNotFoundError:
        pass
    subprocess.run(["node", os.path.join(ROOT, "scripts", "print_pdf.cjs"), tmp, args.out], check=True, env=env)
    print(f"wrote {args.out} (html: {tmp})")


if __name__ == "__main__":
    main()
