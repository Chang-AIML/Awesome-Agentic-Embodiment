#!/usr/bin/env python3
"""Build the Chinese progress report (PDF with figures) from the core-table data.

Reads data/core/{core_table.csv, core_meta.json, fine_labels.csv, pool.jsonl, gap*_candidates.jsonl}
plus the screening files, draws the figures as inline SVG / HTML, and prints the page with headless
Chromium (Playwright, scripts/print_pdf.cjs). Font: Noto Sans SC TTFs in --fonts (downloaded from
Google Fonts into that directory when missing); falls back to an installed CJK sans.

Usage: python3 scripts/build_report.py [--fonts DIR] [--out docs/progress_report.pdf] [--html PATH]
"""
import argparse, csv, html, json, math, os, re, subprocess, sys, tempfile, urllib.request
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
SUB_ZH = {"orchestrator": "编排型", "direct": "直接驱动型", "lifelong": "lifelong / memory 型"}
IFACE_ZH = {"skill-call": "技能调用", "vla-call": "VLA 调用", "micro-action": "语义微动作", "code": "代码",
            "constraint": "约束", "verdict": "裁决", "trace": "执行轨迹", "problem-spec": "问题规格",
            "system-edit": "系统编辑", "message": "消息", "-": "–", "": "–"}
LOOP_ZH = {"re-decide": "再决策", "authored": "编写闭环", "none": "开环", "-": "–", "": "–"}
THEME_ZH = {"real2sim": "Real2Sim", "sim2real": "Sim2Real", "real2sim2real": "Real2Sim2Real"}
R2S_THEMES = set(THEME_ZH)  # theme "vln" marks the VLN chapter instead
BODY_ZH = {"manip": "操作", "mobile-manip": "移动操作", "nav": "导航", "loco": "足式", "humanoid": "人形",
           "multi-robot": "多机器人", "aerial": "空中", "driving": "驾驶", "social": "社交", "other": "其他"}
FID_ZH = {"real": "真机", "sim": "仿真", "sim+real": "仿真+真机"}
CITATION_RECORDS = 34300  # forward-citation records before dedup (harvest log, HANDOFF.md §2)
ALTERNATES_FILE = os.path.join(ROOT, "data/core/alternates.csv")  # id,key,seat,why — left out for quota


# ------------------------------------------------------------------ data

def norm_arxiv(a):
    return re.sub(r"v\d+$", "", (a or "").strip().lower().replace("arxiv:", ""))


STRONG = {"out", "recheck", "verify", "verify_s2", "recheck_r3b", "recheck_scope", "verify_pre", "verify_pf", "audit_out",
          "recheck_direct"}  # judging passes run with the strong model (see build_extended.py)


def year_of(r):
    """arXiv v1 year from the id (YYMM.nnnnn) when there is one, else the Semantic Scholar date."""
    m = re.match(r"(\d{2})\d{2}\.\d{4,5}$", norm_arxiv(r.get("arxiv")))
    return "20" + m.group(1) if m else (r.get("date") or "????")[:4]


def hist(r):
    """Judgment history of a paper, oldest first: [(pass, verdict), ...] from the prev chain plus the current row."""
    return [tuple(x.split(":", 1)) for x in (r.get("prev") or "").split(";") if x] + [(r.get("pass"), r["verdict"])]


def load():
    p = lambda *x: os.path.join(ROOT, *x)
    rows = list(csv.DictReader(open(p("data/core/core_table.csv"))))
    meta = json.load(open(p("data/core/core_meta.json")))
    fine = list(csv.DictReader(open(p("data/core/fine_labels.csv"))))
    gaps = {}
    for name in ("gap_candidates.jsonl", "gap2_candidates.jsonl", "gap3_candidates.jsonl"):
        if os.path.exists(p("data/core", name)):
            gaps[name] = {"gap:" + norm_arxiv(o["arxiv"]): o for o in map(json.loads, open(p("data/core", name)))}
    gap = {k: v for g in gaps.values() for k, v in g.items()}
    pool = [json.loads(l) for l in open(p("data/core/pool.jsonl"))]
    for r in rows:
        m = meta.get(r["arxiv"], {})
        r["date"] = (m.get("published") or r["date"] or "")[:10]
        r["year"] = r["date"][:4]
        r["venue"] = venue_of(r, m)
        r["cites"] = m.get("citations")
        r["named"] = r["key"] in NAMED
        r["new"] = bool(r.get("added"))
    with open(p("data/candidates/candidates.csv")) as f:
        n_cand = sum(1 for _ in csv.reader(f)) - 1
    coarse = Counter(r["label"] for r in csv.DictReader(open(p("data/screening/coarse_labels.csv"))))
    src = Counter(o["source"].split(";")[0] for o in pool)
    re_rows = [r for r in fine if any(p_ == "recheck" for p_, _ in hist(r))]
    re_core = [r for r in re_rows if dict(hist(r))["recheck"] == "core"]
    # round 3: bulk pool (every 2026 harvest candidate), S2 keyword sweep, strong-model verification
    n_bulk = sum(1 for _ in open(p("data/core/pool_bulk.jsonl")))
    s2_rows = sum(1 for _ in open(p("data/candidates/s2_sweep_2026.jsonl")))
    s2_lab = Counter(r["label"] for r in csv.DictReader(open(p("data/candidates/s2_coarse_2026.csv"))))
    n_s2pool = sum(1 for _ in open(p("data/core/pool_s2.jsonl")))
    ver, ver_core, ver_core_kept = [], 0, 0  # Sonnet verification of cheap-model verdicts (the step before it is Haiku's)
    for r in fine:
        h = hist(r)
        k = next((i for i, (p_, _) in enumerate(h) if p_ in ("verify", "verify_s2", "verify_pre", "verify_pf")), None)
        if k:
            ver.append(r)
            ver_core += h[k - 1][1] == "core"
            ver_core_kept += h[k - 1][1] == "core" and h[k][1] == "core"
    r3b = [r for r in fine if r.get("pass") == "recheck_r3b"]  # ReKep-type and agentic Real2Sim re-judged as agents
    scope = [r for r in fine if any(p_ == "recheck_scope" for p_, _ in hist(r))]  # general vs embodied model (decision 12)
    strong26 = [r for r in fine if r["verdict"] == "core" and r.get("pass") in STRONG and year_of(r) == "2026"]
    strong_pre = [r for r in fine if r["verdict"] == "core" and r.get("pass") in STRONG
                  and year_of(r) in ("2022", "2023", "2024", "2025")]
    # coverage completion (round 3, after "is the coverage complete?"): never fine-judged and never coarse-screened
    # candidates, an audit of cheap-model out verdicts, and a re-judge of general models that emit actions directly
    n_pre = sum(1 for _ in open(p("data/core/pool_pre2026.jsonl")))
    lp = p("data/screening/coarse_labels_completion.csv")
    pf_lab = Counter(r["label"] for r in csv.DictReader(open(lp))) if os.path.exists(lp) else Counter()
    audit = [dict(hist(r))["audit_out"] for r in fine if any(p_ == "audit_out" for p_, _ in hist(r))]
    direct = [dict(hist(r))["recheck_direct"] for r in fine if any(p_ == "recheck_direct" for p_, _ in hist(r))]
    ep = p("data/core/extended_2026.csv")
    n_ext = sum(1 for _ in csv.DictReader(open(ep))) if os.path.exists(ep) else 0
    ep = p("data/core/extended_2022_2025.csv")
    n_ext_pre = sum(1 for _ in csv.DictReader(open(ep))) if os.path.exists(ep) else 0
    c = dict(records=CITATION_RECORDS, cand=n_cand, prefilter=sum(coarse.values()), relevant=coarse["relevant"],
             maybe=coarse["maybe"], pool=len(pool), shortlist=len(pool) - src["supplement"] - src["testset"],
             supplement=src["supplement"], testset=src["testset"], verdict=Counter(r["verdict"] for r in fine),
             recheck=len(re_rows), recheck_core=len(re_core),
             recheck_authored=sum(1 for r in re_core if r["pass"] == "recheck" and r["loop"] == "authored"),
             gap1=len(gaps.get("gap_candidates.jsonl", {})), gap2=len(gaps.get("gap2_candidates.jsonl", {})),
             gap3=len(gaps.get("gap3_candidates.jsonl", {})),
             tier=Counter(r["tier"] for r in rows), seat=Counter(r["seat"] for r in rows if r["tier"] == "core"),
             verified=sum(1 for r in rows if meta.get(r["arxiv"], {}).get("verified")),
             links=sum(1 for r in rows if re.search(r"https?://", meta.get(r["arxiv"], {}).get("comment", ""))),
             new=sum(1 for r in rows if r["new"]), bulk=n_bulk, s2=s2_rows, s2_screen=sum(s2_lab.values()),
             s2_keep=s2_lab["relevant"] + s2_lab["maybe"], s2_pool=n_s2pool, judged=len(fine),
             ver=len(ver), ver_core=ver_core, ver_core_kept=ver_core_kept,
             strong26=len(strong26), ext=n_ext, ext_pre=n_ext_pre, strong_pre=len(strong_pre),
             pre=n_pre, pf_screen=sum(pf_lab.values()), pf_keep=pf_lab["relevant"] + pf_lab["maybe"],
             audit=len(audit), audit_core=sum(v == "core" for v in audit), audit_in=sum(v != "out" for v in audit),
             direct=len(direct), direct_core=sum(v == "core" for v in direct), r3b=len(r3b), r3b_core=sum(1 for r in r3b if r["verdict"] == "core"),
             scope=len(scope), scope_out=sum(1 for r in scope if r["verdict"] == "out"),
             scope_core_out=sum(1 for r in scope if r["verdict"] == "out" and len(hist(r)) > 1 and hist(r)[-2][1] == "core"),
             r3b_con=sum(1 for r in r3b if r["verdict"] == "core" and r["interface"] == "constraint"),
             r3b_r2s=sum(1 for r in r3b if r["verdict"] == "core" and re.match(r"\s*\[real2sim", r["reason"])))
    # trend corpus: every stage-2 core verdict in the judging pool
    prim, alls, n = defaultdict(Counter), defaultdict(Counter), Counter()
    for r in fine:
        if r["verdict"] != "core" or r.get("pass") not in STRONG:
            continue
        y = year_of(r)
        n[y] += 1
        prim[y][r["seat"]] += 1
        for s in {r["seat"]} | {x for x in re.split(r"[+,;/ ]+", r["seat2"]) if x in SEATS}:
            alls[y][s] += 1
    trend = []
    for y in sorted(n):
        tot = sum(alls[y].values())
        eff = math.exp(-sum(v / tot * math.log(v / tot) for v in alls[y].values() if v))
        trend.append(dict(year=y, n=n[y], prim=prim[y], alls=alls[y], eff=eff))
    # agreement with the first-round test-set placements (first pass only)
    agree = defaultdict(Counter)
    for r in fine:
        if r["testset_tier"] and hist(r)[0][0] == "out":  # the first stage-2 pass, before any re-judging
            agree[r["testset_tier"].split(" ")[0]][hist(r)[0][1]] += 1
    both = [r for r in fine if r["testset_tier"] == "CORE" and hist(r)[0] == ("out", "core") and r["verdict"] == "core"]
    seat_same = sum(1 for r in both if r["testset_primary"].split("-")[0].split(" ")[0] == r["seat"])
    alt = []
    fine_by_id = {r["id"]: r for r in fine}
    if os.path.exists(ALTERNATES_FILE):
        for a in csv.DictReader(open(ALTERNATES_FILE)):
            a["arxiv"] = norm_arxiv((gap.get(a["id"]) or fine_by_id.get(a["id"]) or {}).get("arxiv", ""))
            alt.append(a)
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


def svg(w, h, body, label, width="100%"):
    return (f'<svg viewBox="0 0 {w} {h}" width="{width}" role="img" aria-label="{esc(label)}" '
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


def chip(r, col=None, year=False):
    """A paper card. Fill = re-decide; outline = authored loop; dashed grey = open loop (pioneers)."""
    col = col or COLOR.get(r["seat"], MUTED)
    cls = {"authored": "chip au", "none": "chip op"}.get(r.get("loop"), "chip")
    mark = (" ★" if r["named"] else "") + (" ◆" if r.get("theme") in R2S_THEMES and r["tier"] == "core" else "") + \
           (" △" if r.get("theme") == "vln" else "")
    yr = f'<span class="cy">{r["year"][2:]}</span>' if year else ""
    return f'<span class="{cls}" style="--c:{col}">{esc(r["key"])}{mark}{yr}</span>'


def examples(rows, seat, limit=250):
    xs = sorted([r for r in rows if r["tier"] == "core" and r["seat"] == seat],
                key=lambda r: (not r["named"], -int(r.get("rep") or 0) if str(r.get("rep", "")).isdigit() else 0,
                               -(r["cites"] or 0)))
    names, s = [], "例："
    for r in xs:
        cand = s + ("、" if names else "") + r["key"] + (" ★" if r["named"] else "")
        if text_w(cand, 9.8) > limit:
            break
        names.append(r["key"])
        s = cand
    return s


# ------------------------------------------------------------------ figures

def fig_pipeline(c):
    t = c["tier"]
    steps = [
        (f"{c['records']:,}", "条引用记录", f"14 篇种子论文的前向引用（Semantic Scholar），去重后 {c['cand']:,} 篇候选", "脚本"),
        (f"{c['relevant'] + c['maybe']:,}", "篇粗筛保留",
         f"{c['prefilter']:,} 篇进入粗筛；判「相关」{c['relevant']:,}、「可能」{c['maybe']:,}；全部「无关」经 Sonnet 复核",
         "Haiku + Sonnet"),
        (f"{c['pool']:,}", "篇第一轮判定池",
         f"短名单 {c['shortlist']} + 小 seat 补充 {c['supplement']} + 测试集 {c['testset']}，逐篇判定；"
         f"按「编写闭环」新规则复核 {c['recheck']} 篇前驱，{c['recheck_core']} 篇改判 core", "Sonnet"),
        (f"{c['bulk']:,}", "篇批量判定池", "收割候选中的全部 2026 年论文，加 2022–2025 年的高被引论文，逐篇判定", "Haiku"),
        (f"{c['s2']:,}", "篇 2026 关键词检索",
         f"Semantic Scholar 检索「机器人 × agent」，补上没引用种子的论文：{c['s2_screen']:,} 篇新论文提到基础模型，"
         f"粗筛保留 {c['s2_keep']:,} 篇，逐篇判定", "脚本 + Haiku"),
        (f"{c['pre']:,}", "篇补判（多为 2022–2025）",
         "粗筛保留、但此前从未逐篇判定的候选，多是被引较少的 2022–2025 年论文；全部逐篇判定", "Haiku"),
        (f"{c['pf_screen']:,}", "篇补粗筛",
         f"引用收割中从未粗筛过的 2022 年后候选（标题和摘要里没有具身关键词）补做粗筛，保留 {c['pf_keep']} 篇逐篇判定", "Haiku"),
        (f"{c['ver']:,}", "篇 Sonnet 复核",
         f"Haiku 判为 core、前驱或边界的论文全部由 Sonnet 从头重判；Haiku 判 core 的 {c['ver_core']} 篇中 "
         f"{c['ver_core_kept']} 篇维持 core", "Sonnet"),
        (f"{c['audit']}", "篇出局抽查",
         f"随机抽 Haiku 判为 out 的论文由 Sonnet 重判，{c['audit_core']} 篇改判 core、{c['audit_in'] - c['audit_core']} 篇改判先驱、"
         f"边界或资源；Haiku 漏判 core 的比例约 {round(100 * c['audit_core'] / max(c['audit'], 1), 1)}%", "Sonnet"),
        (f"{c['r3b']:,}", "篇按新规则重判",
         f"「ReKep 这一类都算」和「agentic Real2Sim 都算」：命中约束 / 关键点或 Real2Sim 特征、之前未判 core 的论文由 Sonnet 重判，"
         f"{c['r3b_core']} 篇改判 core（约束编程 {c['r3b_con']}、Real2Sim {c['r3b_r2s']}）", "Sonnet"),
        (f"{c['scope']:,}", "篇按范围重判",
         f"只收通用大模型做具身任务：训练过的决策者与涉及 VLA / WAM 的论文由 Sonnet 重判，{c['scope_out']} 篇判为具身大模型等而排除",
         "Sonnet"),
        (f"{c['gap1'] + c['gap2'] + c['gap3']}", "篇联网补漏",
         f"公认工作 {c['gap1']} 篇；2026 年少见身体形态、小 seat 与 Real2Sim {c['gap2']} 篇；"
         f"2022–2025 年先驱 {c['gap3']} 篇；全部经 arXiv 核验", "联网 agent"),
        (f"{c['strong26']}", "篇 2026 年 core",
         f"经 Sonnet 判定或复核为 core 的 2026 年论文；{t['core']} 篇进核心表，其余 {c['ext']} 篇列入 README 的扩展列表",
         "Sonnet"),
        (f"{c['strong_pre']}", "篇 2022–2025 年 core",
         f"经 Sonnet 判定或复核为 core 的 2022–2025 年论文；挑出的先驱进核心表，其余 {c['ext_pre']} 篇列入 README 的 "
         "2022–2025 扩展列表", "Sonnet"),
        (f"{t['pioneer']} + {t['core']} + {t['resource']}", "先驱 + 2026 + 资源",
         f"人工挑选；{c['verified']} 篇全部经 arXiv 核验，标题一致", "人工"),
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
    W = 680
    b = [box(20, 8, 330, 38, "一篇论文：标题 + 摘要", [], fill="#ffffff"),
         box(410, 8, 255, 38, "benchmark、数据集、能力研究 → 资源表", [], fill="#f4f3ef", title_size=10.5),
         arrow("M350,27 L407,27")]
    qs = [("⓪ 通用大模型做具身任务", ["决策者是 LLM / VLM（GPT、Gemini、Claude、Astra），", "原样使用或为 agent 角色微调；直接出动作也算"]),
          ("① 显式决策", ["输出可检查的决策：计划、技能 / 工具 / VLA", "调用、代码、约束、裁决、系统编辑或动作"]),
          ("② 决策权", ["自己写出选项；或在含 stop / retry / replan /", "ask 等控制行为的选项中做选择"]),
          ("③ 闭环（满足其一，或属两个例外）", ["再决策；或编写闭环（写的约束 / 程序依结果调整）。", "例外：约束编程、agentic Real2Sim 一次写成也收"]),
          ("④ 机器人身体与保真度", ["真机，或失败可能由物理原因引起的仿真", "（接触、滑动、碰撞）"])]
    exits = [("OUT · 具身大模型", ["VLA、分层 VLA、WAM、机器人基础模型", "（π0.5、Hi Robot、MEM、PaLM-E）"], "#f4f3ef", BASE),
             ("OUT · 器官", ["打分器、奖励 / 价值模型、一次性标注、", "world model 预测"], "#f4f3ef", BASE),
             ("OUT · 没有决策权", ["只给代码枚举的同类候选打分，", "控制流归代码（SG-Nav、PIVOT）"], "#f4f3ef", BASE),
             ("先驱（若为 2025 年前的奠基作）", ["开环计划、无自身记录的逐步推理：", "ZS-Planners、Socratic、KnowNo"],
              tint(MUTED, 0.16), MUTED),
             ("BOUNDARY · 边界", ["离散或脚本化仿真（ALFRED、AI2-THOR）、", "自动驾驶；进 lineage 表"], "#f4f3ef", BASE)]
    y = 66
    b.append(arrow("M185,46 L185,63"))
    for (qt, ql), (et, el, ef, es) in zip(qs, exits):
        b.append(box(20, y, 330, 64, qt, ql))
        b.append(box(410, y, 255, 64, et, el, fill=ef, stroke=es, title_size=10.8))
        b.append(arrow(f"M350,{y + 32} L407,{y + 32}", "否", 372, y + 26))
        b.append(arrow(f"M185,{y + 64} L185,{y + 85}", "是", 193, y + 79))
        y += 88
    b.append(box(20, y, 330, 64, "全部满足", ["2022–2025 年的代表作 → 先驱；2026 年 → 2026 论文", "两者按 Seat 一起讲「先驱 → 2026」"],
                 fill=tint(COLOR["Controller"], 0.12), stroke=COLOR["Controller"]))
    return svg(W, y + 70, "".join(b), "agent 判定流程图", width="72%")


def fig_seats(rows):
    W, H = 680, 388
    b = [T(150, 16, "部署前 · pre-deployment", 11.5, 700, INK, "middle"),
         T(150, 31, "agent 的产出冻结后，再交给部署的系统", 9.5, 400, MUTED, "middle"),
         T(525, 16, "评测 / 部署时 · runtime", 11.5, 700, INK, "middle"),
         T(525, 31, "agent 在评测 episode 中被调用", 9.5, 400, MUTED, "middle"),
         f'<line x1="338" y1="6" x2="338" y2="{H - 26}" stroke="{BASE}" stroke-width="1"/>']
    left = [("Designer", 44, ["为学习者设计问题：reward、成功判据、", "任务、环境与仿真、课程、评测套件"]),
            ("Teacher", 162, ["亲自执行、经结果检验的轨迹或 playbook，", "成为部署模型的训练目标"]),
            ("Developer", 280, ["修改系统本身：策略代码、技能库、harness、", "训练代码、硬件；自己的实验决定保留或回滚"])]
    for seat, y, lines in left:
        b.append(box(8, y, 286, 88, f"{seat} · {SEAT_ZH[seat]}", lines + [examples(rows, seat, 250)],
                     stripe=COLOR[seat], fill=tint(COLOR[seat], 0.07)))
    b.append(box(380, 44, 292, 88, "Controller · 控制者",
                 ["每一步决定机器人做什么：计划、调用技能或", "VLA、写当下执行的代码或约束、发语义微动作",
                  examples(rows, "Controller", 258)], stripe=COLOR["Controller"], fill=tint(COLOR["Controller"], 0.07)))
    b.append(box(380, 280, 292, 88, "Supervisor · 监督者",
                 ["只在异常时介入：门控、否决、失败检测与", "恢复；检查过程独立于名义决策者",
                  examples(rows, "Supervisor", 258)], stripe=COLOR["Supervisor"], fill=tint(COLOR["Supervisor"], 0.07)))
    b.append(f'<rect x="446" y="176" width="158" height="64" rx="8" fill="#ffffff" stroke="{INK2}" stroke-width="1.4"/>')
    b.append(T(525, 202, "机器人身体", 13, 700, INK, "middle"))
    b.append(T(525, 222, "+ 部署的策略", 10, 400, INK2, "middle"))
    b.append(arrow("M525,132 L525,173", "持续驱动", 533, 157))
    b.append(arrow("M525,280 L525,243", "仅在异常时", 533, 266))
    b.append(arrow("M294,88 C360,88 380,190 443,192"))
    b.append(arrow("M294,206 C360,206 380,208 443,208"))
    b.append(arrow("M294,324 C360,324 380,226 443,224"))
    b.append(T(8, H - 8, "例子均为 2026 年的核心论文，★ 为用户点名。Carrier（G / C / H / I）是第二个维度：每个 seat 都记录决策由哪类权重承载。",
               9.0, 400, MUTED))
    return svg(W, H, "".join(b), "五个 Seat 围绕机器人身体的示意图", width="93%")


def fig_grid(rows):
    """Seat x period: pioneers (2022-2025) next to 2026, with the strongest examples of each cell."""
    heads = [("pioneer", "先驱 · 2022–2025", "每个 seat 的源头"), ("core", "2026", "范式铺开的一年")]
    bins = [(1, 2, SEQ[0]), (3, 5, SEQ[1]), (6, 12, SEQ[2]), (13, 999, SEQ[3])]
    fill = lambda n: next(c for lo, hi, c in bins if lo <= n <= hi)
    out = ['<table class="grid"><tr><th class="seatcol">Seat</th>']
    out += [f'<th><b>{t}</b><br><span>{esc(d)}</span></th>' for _, t, d in heads] + ['<th class="tot">合计</th></tr>']
    for s in SEATS:
        out.append(f'<tr><td class="seatcol"><span class="sw" style="background:{COLOR[s]}"></span>'
                   f'<b>{s}</b><br><span class="zh">{SEAT_ZH[s]}</span></td>')
        tot = 0
        for tier, _, _ in heads:
            xs = sorted([r for r in rows if r["tier"] == tier and r["seat"] == s],
                        key=lambda r: (not r["named"], -(r["cites"] or 0)))
            tot += len(xs)
            if not xs:
                out.append('<td class="empty">·</td>')
                continue
            f = fill(len(xs))
            names = "、".join(r["key"] + (" ★" if r["named"] else "") for r in xs[:3]) + ("…" if len(xs) > 3 else "")
            ft = sum(1 for r in xs if r["carrier"].split("→")[-1].strip() == "C")
            extra = f"<br>其中 {ft} 篇为微调过的通用模型（C）" if ft else ""
            out.append(f'<td style="background:{f};color:{on(f)}"><b class="n">{len(xs)}</b>'
                       f'<span class="ex">{esc(names)}{extra}</span></td>')
        out.append(f'<td class="tot">{tot}</td></tr>')
    out.append("</table>")
    out.append('<div class="binlegend">篇数：' + "".join(
        f'<span><i style="background:{c}"></i>{lo}–{hi}</span>' if hi < 999 else f'<span><i style="background:{c}"></i>≥{lo}</span>'
        for lo, hi, c in bins) + '<span>★ 用户点名；计数含 Real2Sim 与 VLN 两章</span></div>')
    return "".join(out)


def lanes_core():
    lanes = [(("Controller", SUB_ZH[s].replace(" / memory", "")), "Controller",
              lambda r, s=s: r["tier"] == "core" and r["seat"] == "Controller" and r["sub"] == s)
             for s in ("orchestrator", "direct", "lifelong")]
    lanes += [((s, SEAT_ZH[s]), s, lambda r, s=s: r["tier"] == "core" and r["seat"] == s) for s in SEATS[1:]]
    return lanes


def fig_quarters(rows):
    qs = [("1", "Q1 · 1–3 月"), ("2", "Q2 · 4–6 月"), ("3", "Q3 · 7–9 月"), ("4", "Q4 · 10 月")]
    q = lambda r: str((int(r["date"][5:7]) - 1) // 3 + 1) if len(r["date"]) >= 7 else "1"
    out = ['<table class="matrix"><colgroup><col style="width:14%"><col style="width:18%"><col style="width:20%">'
           '<col style="width:29%"><col style="width:19%"></colgroup><tr><th></th>']
    out += [f"<th>{t}</th>" for _, t in qs] + ["</tr>"]
    for label, seat, f in lanes_core():
        xs = [r for r in rows if f(r)]
        out.append(f'<tr><td class="lane"><span class="sw" style="background:{COLOR[seat]}"></span>'
                   f'<b>{esc(label[0])}</b><br><span class="lsub">{esc(label[1])} · {len(xs)}</span></td>')
        for k, _ in qs:
            out.append("<td>" + "".join(chip(r) for r in sorted([r for r in xs if q(r) == k], key=lambda r: r["date"])) + "</td>")
        out.append("</tr>")
    out.append("</table>")
    out.append('<div class="binlegend"><span class="chip" style="--c:#2a78d6">实心</span>再决策　'
               '<span class="chip au" style="--c:#2a78d6">空心</span>编写闭环　'
               '<span class="chip op" style="--c:#2a78d6">虚线</span>开环（约束编程、Real2Sim 例外）　'
               '★ 用户点名　◆ Real2Sim / Sim2Real 章　△ VLN 章</div>')
    return "".join(out)


def fig_pioneers(rows):
    years = ["2022", "2023", "2024", "2025"]
    out = ['<table class="matrix"><colgroup><col style="width:14%"><col style="width:21.5%"><col style="width:21.5%">'
           '<col style="width:21.5%"><col style="width:21.5%"></colgroup><tr><th></th>']
    out += [f"<th>{y}</th>" for y in years] + ["</tr>"]
    for s in SEATS:
        xs = [r for r in rows if r["tier"] == "pioneer" and r["seat"] == s]
        out.append(f'<tr><td class="lane"><span class="sw" style="background:{COLOR[s]}"></span>'
                   f'<b>{s}</b><br><span class="lsub">{SEAT_ZH[s]} · {len(xs)}</span></td>')
        for y in years:
            out.append("<td>" + "".join(chip(r) for r in sorted([r for r in xs if r["year"] == y], key=lambda r: r["date"]))
                       + "</td>")
        out.append("</tr>")
    out.append("</table>")
    out.append('<div class="binlegend"><span class="chip" style="--c:#2a78d6">实心</span>再决策　'
               '<span class="chip au" style="--c:#2a78d6">空心</span>编写闭环　'
               '<span class="chip op" style="--c:#2a78d6">虚线</span>开环（开创了方向，但不满足闭环）　★ 用户点名</div>')
    return "".join(out)


def fig_r2s(rows):
    cols = [("real2sim", "Real2Sim · 从真实到仿真", "从视频、扫描、数据集构建可交互的仿真世界、资产与物理参数"),
            ("real2sim2real", "Real2Sim2Real · 练习后回到真机", "在重建的仿真里练习、诊断、改进，再迁移到真机"),
            ("sim2real", "Sim2Real · 从仿真到真机", "设计 domain randomization、依真机试验修正仿真器、迁移与适配技能")]
    W, H = 680, 74
    b = []
    nodes = [(8, "真实世界", "视频、扫描、真机试验"), (250, "仿真", "可交互的世界、资产、参数"), (492, "真机部署", "迁移后的技能与策略")]
    for x, t, s in nodes:
        b.append(f'<rect x="{x}" y="8" width="180" height="46" rx="8" fill="#ffffff" stroke="{INK2}" stroke-width="1.2"/>')
        b.append(T(x + 90, 28, t, 11.5, 700, INK, "middle"))
        b.append(T(x + 90, 44, s, 9.2, 400, MUTED, "middle"))
    b.append(arrow("M188,31 L247,31"))
    b.append(T(217, 24, "Real2Sim", 9, 500, MUTED, "middle"))
    b.append(arrow("M430,31 L489,31"))
    b.append(T(459, 24, "Sim2Real", 9, 500, MUTED, "middle"))
    head = svg(W, H, "".join(b), "Real2Sim 与 Sim2Real 的流程")
    out = [f'<div class="r2s">{head}<div class="r2s-cols">']
    for th, title, desc in cols:
        core = sorted([r for r in rows if r["tier"] == "core" and r.get("theme") == th], key=lambda r: r["date"])
        pio = sorted([r for r in rows if r["tier"] == "pioneer" and r.get("theme") == th], key=lambda r: r["date"])
        res = sorted([r for r in rows if r["tier"] == "resource" and r.get("theme") == th], key=lambda r: r["date"])
        out.append(f'<div class="r2s-col"><h4>{esc(title)}</h4><div class="s">{esc(desc)}</div>'
                   f'<div class="grp">2026 · {len(core)}</div>' + "".join(chip(r) for r in core))
        if pio:
            out.append('<div class="grp">先驱</div>' + "".join(chip(r, MUTED, year=True) for r in pio))
        if res:
            out.append('<div class="grp">评测</div>' + "".join(
                f'<span class="chip op" style="--c:{MUTED}">{esc(r["key"])}</span>' for r in res))
        out.append("</div>")
    out.append("</div></div>")
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
            if ww >= 34:  # label only where it fits with padding
                b.append(T(x + ww / 2, y + 12.8, f"{round(100 * v / t['n'])}%", 9.2, 500, on(COLOR[s]), "middle"))
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
    new = ' <span class="new">新</span>' if r.get("new") else ""
    return f'<a href="https://arxiv.org/abs/{r["arxiv"]}">{esc(r["key"])}</a>{star}{new}'


def table_core(rows, title, pred, show_seat=False):
    xs = sorted([r for r in rows if pred(r)], key=lambda r: (r["date"], r["key"]))
    if not xs:
        return ""
    third = ("Seat", lambda r: r["seat"]) if show_seat else ("会议", lambda r: r["venue"])
    out = [f'<h3>{esc(title)}（{len(xs)}）</h3><table class="tbl"><colgroup><col style="width:15%"><col style="width:6.5%">'
           f'<col style="width:{10 if show_seat else 8}%"><col style="width:6%"><col style="width:8%"><col style="width:7%">'
           '<col style="width:13%"><col>'
           f'</colgroup><tr><th>短名</th><th>月份</th><th>{third[0]}</th><th>Carrier</th><th>接口</th><th>闭环</th><th>身体</th>'
           '<th>入选理由</th></tr>']
    for r in xs:
        out.append(f'<tr><td>{link(r)}</td><td>{r["date"][:7]}</td><td>{esc(third[1](r))}</td><td>{esc(r["carrier"])}</td>'
                   f'<td>{esc(IFACE_ZH.get(r["interface"], r["interface"]))}</td><td>{LOOP_ZH.get(r["loop"], "–")}</td>'
                   f'<td>{esc(body_zh(r["body"]))}</td><td>{esc(r["why"])}</td></tr>')
    out.append("</table>")
    return "".join(out)


def table_pioneers(rows, title="先驱 · 2022–2025", pred=lambda r: True):
    xs = sorted([r for r in rows if r["tier"] == "pioneer" and pred(r)], key=lambda r: (SEATS.index(r["seat"]), r["date"]))
    if not xs:
        return ""
    out = [f'<h3>{esc(title)}（{len(xs)}）</h3><table class="tbl"><colgroup><col style="width:17%"><col style="width:6%">'
           '<col style="width:11%"><col style="width:8%"><col style="width:9%"><col></colgroup>'
           '<tr><th>短名</th><th>年份</th><th>Seat</th><th>Carrier</th><th>闭环</th><th>为什么列为先驱</th></tr>']
    for r in xs:
        out.append(f'<tr><td>{link(r)}</td><td>{r["year"]}</td><td>{r["seat"]}</td><td>{esc(r["carrier"])}</td>'
                   f'<td>{LOOP_ZH.get(r["loop"], "–")}</td><td>{esc(r["why"])}</td></tr>')
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
.kpis { display: grid; grid-template-columns: repeat(6, 1fr); gap: 7pt; margin: 10pt 0 12pt; }
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
.step { display: grid; grid-template-columns: 14pt 160pt 1fr 80pt; align-items: center; min-height: 29pt; }
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
.binlegend .chip { margin-right: 3pt; }
.matrix { table-layout: fixed; font-size: 7.3pt; }
.matrix th { font-size: 9pt; color: #52514e; font-weight: 700; text-align: left; padding: 2pt 4pt; border-bottom: 1px solid #c3c2b7; }
.matrix td { border-bottom: 1px solid #e1e0d9; padding: 3pt 3pt; vertical-align: top; }
.matrix td.lane { font-size: 8pt; color: #0b0b0b; line-height: 1.35; padding-top: 4pt; }
.matrix .lsub { color: #52514e; margin-left: 12pt; font-size: 7.4pt; }
.chip { display: inline-block; line-height: 1.3; padding: 1.2pt 4pt 1.2pt 4pt; margin: 1.3pt 2pt 1.3pt 0; font-size: 7.3pt;
        border-radius: 3px; border-left: 3px solid var(--c); background: color-mix(in srgb, var(--c) 13%, white); white-space: nowrap; }
.matrix .chip { white-space: normal; max-width: 100%; box-sizing: border-box; }
.chip.au { background: #ffffff; box-shadow: inset 0 0 0 1px var(--c); }
.chip.op { background: #ffffff; color: #52514e; border-left: 3px dashed var(--c); box-shadow: inset 0 0 0 1px #d6d4cc; }
.chip .cy { color: #898781; margin-left: 3pt; font-size: 6.6pt; }
.new { display: inline-block; font-size: 6.6pt; color: #ffffff; background: #1c5cab; border-radius: 3px; padding: 0 3pt; margin-left: 2pt; vertical-align: 0.5pt; }
.r2s { border: 1px solid #e1e0d9; border-radius: 8px; padding: 6pt 8pt 8pt; background: #fcfcfb; }
.r2s-cols { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8pt; margin-top: 2pt; }
.r2s-col { border-top: 2px solid #e1e0d9; padding-top: 4pt; }
.r2s-col h4 { font-size: 9pt; margin: 0 0 1pt; }
.r2s-col .s { font-size: 7.6pt; color: #52514e; line-height: 1.4; margin-bottom: 3pt; }
.r2s-col .grp { font-size: 7.2pt; color: #898781; margin: 4pt 0 1pt; }
.charts2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14pt; }
.charts2 h4 { font-size: 9.4pt; margin: 0 0 1pt; font-weight: 700; }
.charts2 .s { font-size: 8pt; color: #52514e; margin-bottom: 2pt; }
.tbl { font-size: 7.8pt; line-height: 1.45; table-layout: fixed; }
.tbl th { text-align: left; font-weight: 500; color: #52514e; border-bottom: 1px solid #c3c2b7; padding: 3pt 4pt; }
.tbl td { border-bottom: 1px solid #e1e0d9; padding: 3pt 4pt; vertical-align: top; overflow-wrap: anywhere; }
.tbl tr { break-inside: avoid; }
.tbl .num { text-align: right; font-variant-numeric: tabular-nums; }
.small { font-size: 8.4pt; }
"""


def build_html(fontdir):
    rows, c, trend, agree, (seat_same, seat_n), alt = load()
    seat = c["seat"]
    core = [r for r in rows if r["tier"] == "core"]
    pio = [r for r in rows if r["tier"] == "pioneer"]
    r2s = [r for r in core if r.get("theme") in R2S_THEMES]
    vln = [r for r in core if r.get("theme") == "vln"]
    vln_pio = [r for r in pio if r.get("theme") == "vln"]
    res = [r for r in rows if r["tier"] == "resource"]
    sub = Counter(r["sub"] for r in core if r["seat"] == "Controller" and not r.get("theme"))
    themed_ctl = sum(1 for r in core if r["seat"] == "Controller" and r.get("theme"))
    n_core, n_pio, n_res = len(core), len(pio), len(res)
    t = {x["year"]: x for x in trend}
    dev = {y: x["alls"]["Developer"] / x["n"] for y, x in t.items()}
    ctl = {y: x["alls"]["Controller"] / x["n"] for y, x in t.items()}
    late = [y for y in ("2023", "2024", "2025", "2026") if y in ctl]
    pct = lambda f: f"{round(100 * f)}%"
    authored_core = [r for r in core if r["loop"] == "authored"]
    authored_pio = [r for r in pio if r["loop"] == "authored"]
    open_core = [r for r in core if r["loop"] == "none"]  # admitted by the two exceptions (decisions 8 and 9)
    bodies = Counter((r["body"] or "").split("/")[0] for r in core)
    body_txt = "、".join(f"{BODY_ZH.get(k, k)} {n}" for k, n in bodies.most_common() if k)
    q = Counter(str((int(r["date"][5:7]) - 1) // 3 + 1) for r in core if len(r["date"]) >= 7)
    H = []
    a = H.append

    # ---------------------------------------------------------- page 1: summary
    a('<h1>Agentic Embodiment 综述 · 第三轮进展</h1>')
    a('<div class="sub">从先驱到 2026：定义、分类与核心论文表 · 2026-10-08 · 分支 claude/jolly-thompson-g43dno</div>')
    a('<div class="defn"><b>一句话定义</b>　Agentic Embodiment 研究通用基础模型（LLM / VLM，而不是具身动作模型）作为 agent 做出的显式决策：'
      '决策的后果作用到机器人身体上，agent 再依据后果的证据重新决策。全文围绕一个问题组织：这个 agent 相对于机器人部署的策略坐在哪里'
      '（<b>Seat</b>）。'
      '<div class="en">Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs, not embodied action models — '
      'acting as agents that make explicit decisions whose consequences reach a robot body, and that re-decide on evidence of those '
      'consequences. Its organizing question is where such an agent sits relative to the body\'s deployed policy — steering it, '
      'guarding it, teaching it, designing its learning problem, or building its system (Seat).</div></div>')
    a('<div class="thesis">主线（草案，待你确认）：Agency spreads around the body — general models, not embodied action models, '
      'fill seat after seat.</div>')
    a('<p class="note">研究对象是通用大模型做具身任务；agency 没有离开机器人，而是从 2022 年的先驱开始，在身体周围逐个占据新的位置，'
      '到 2026 年铺满五个 seat。具身大模型（VLA、WAM）直接出动作的路线不收，只作对照。</p>')
    kpis = [(f"{n_pio}", "篇先驱<br>（2022–2025）"), (f"{n_core}", "篇 2026 年<br>论文"),
            (f"{len(r2s)}", "篇 Real2Sim /<br>Sim2Real 章"), (f"{len(vln)}", "篇 VLN /<br>具身导航章"), (f"{n_res}", "个 benchmark<br>与资源"),
            (f"{c['verified']}/{len(rows)}", "篇经 arXiv 核验<br>（标题全部一致）")]
    a('<div class="kpis">' + "".join(f'<div class="kpi"><div class="v">{k}</div><div class="l">{l}</div></div>' for k, l in kpis)
      + '</div>')
    added = [r["key"] for r in rows if r["tier"] == "pioneer" and r.get("added") == "r3c"]
    a('<div class="callout"><h3>这一轮按你的意见做的改动</h3><ul>'
      f'<li><b>只收通用大模型做具身任务</b>：VLA、分层 VLA、WAM、机器人基础模型直接出动作的工作删除（重判 {c["scope"]} 篇，'
      f'{c["scope_out"]} 篇排除）；通用模型直接出动作仍算（如 GPT-6 Astra 在 RoboDojo 上当策略）。</li>'
      f'<li><b>覆盖补全</b>：从未细判的 {c["pre"]:,} 篇、从未粗筛的 {c["pf_screen"]:,} 篇（{c["pf_keep"]} 篇进入判定）全部补判；'
      f'Haiku 的 core / 先驱 / 边界全部经 Sonnet 复核；抽查 {c["audit"]} 篇 Haiku 判 out 的论文，{c["audit_core"]} 篇改判 core；'
      f'第三轮联网补漏 {c["gap3"]} 篇。</li>'
      f'<li><b>先驱补到 {n_pio} 篇</b>，各 seat 均衡、多补 2025 年'
      + (f'（本次新增 {len(added)} 篇，如 {"、".join(added[:6])}）' if added else '') + '。</li>'
      f'<li><b>ReKep 一类、agentic Real2Sim 都算</b>；Real2Sim 只是子方向，只收 {len(r2s)} 篇代表作；VLN 单列一章（{len(vln)} 篇）。</li>'
      f'<li><b>规模</b>：先驱 {n_pio} + 2026 年 {n_core} = {n_pio + n_core} 篇，资源 {n_res} 个；表外满足定义的论文列在 README '
      f'扩展列表（2026 年 {c["ext"]} 篇，2022–2025 年 {c["ext_pre"]} 篇）。</li></ul></div>')
    a('<div class="callout ask"><h3>需要你决定</h3><ol>'
      '<li><b>主线的措辞</b>：只收通用大模型之后，原主线里的「not weights」不再成立。候选：'
      '「Agency spreads around the body — general models, not embodied action models, fill seat after seat」；'
      '或「General models become embodied agents through the loops built around them」。</li>'
      '<li><b>副轴</b>：Carrier 只剩 G（原样使用）和 C（为 agent 角色微调）两类，信息量很小。建议改用 Interface（技能调用 / 冻结 VLA / '
      '代码 / 约束 / 直接动作 / 问题规格 / 系统编辑）做副轴。</li>'
      '<li><b>审阅新增论文</b>：附录 A 中标「新」的论文都是这一轮加入的，有不同意的告诉我。</li>'
      '<li><b>自动驾驶</b>：按你第一次的决定，自动驾驶仍只在边界一节讨论。你说「很多别的 embodiment 都可以放进去」，'
      '如果也想收闭环驾驶 agent，我可以单独补一组。</li>'
      '<li><b>合并到 main</b>：所有内容目前在工作分支上，需要的话我开 PR。</li></ol></div>')

    # ---------------------------------------------------------- 1 pipeline
    a('<div class="section"><h2>1　这一轮做了什么</h2>')
    a('<p>第一轮收割了 14 篇种子论文的前向引用，并做了粗筛和短名单；第二轮逐篇判定并挑出了第一版核心表。这一轮按你的意见改了闭环判定，'
      '对 2026 年做了全量检索（2026 年论文最多）：收割候选中的 2026 年论文全部判定，再用关键词检索补上没引用种子的论文；'
      '另有两轮联网搜索。之后按「ReKep 这一类都算」「agentic Real2Sim 都算」重判了相关论文，把 VLN 单列一章，'
      '最后按「只收通用大模型」删去具身大模型，并补全 2022–2025 年的先驱。下图是完整的筛选漏斗，右栏标出每一步由谁完成。</p>')
    a(f'<figure>{fig_pipeline(c)}<figcaption><b>图 1　筛选漏斗。</b>引用收割只能找到引用了种子论文的工作，'
      '很多 2026 年的新论文不在里面，所以加了 2026 年关键词检索和两轮联网搜索。批量判定用便宜的 Haiku，凡是 Haiku 判为 core、'
      '前驱或边界的都由 Sonnet 从头重判；核心表的论文都用 arXiv API 核对过编号和标题。</figcaption></figure>')
    a('<h3>五个关键做法</h3><ul>'
      f'<li><b>补判定池</b>：短名单按被引数和新兴度取样，会漏掉被引中等、但属于小 seat 的论文，例如 Code-as-Monitor；'
      f'所以补了 {c["supplement"]} 篇小 seat 论文和 {c["testset"]} 篇第一轮测试集论文。</li>'
      f'<li><b>2026 年不抽样</b>：收割候选中的 2026 年论文全部判定（批量判定池 {c["bulk"]:,} 篇）；引用收割漏掉的论文，'
      f'用 Semantic Scholar 关键词检索补齐（{c["s2"]:,} 篇命中，新论文中 {c["s2_keep"]:,} 篇进入判定）。</li>'
      f'<li><b>逐篇判定，两级模型</b>：共 {c["judged"]:,} 篇按 rubric 逐篇判定（verdict、seat、carrier、子类、接口、闭环形式、'
      '代表性 1–5 分和一句理由），合并时校验枚举值和完整性。批量部分由 Haiku 初判，所有 Haiku 判为 core、前驱或边界的论文再由 '
      f'Sonnet 不看初判结果从头重判（{c["ver"]:,} 篇）；Haiku 的 core 有 {round(100 * c["ver_core_kept"] / max(c["ver_core"], 1))}% 被 Sonnet 维持。'
      '统计和扩展列表只用 Sonnet 的判定。</li>'
      f'<li><b>联网补漏</b>：第一轮找公认工作（{c["gap1"]} 篇，如 EmbodiedBench、BUMBLE）；第二轮专找 2026 年、'
      f'Real2Sim / Sim2Real 和少见的身体形态（{c["gap2"]} 篇）；第三轮按十条脉络均衡地找没有引用种子论文的 2022–2025 年先驱'
      f'（{c["gap3"]} 篇）。</li>'
      '<li><b>人工挑选</b>：每个 seat 内按代表性和影响力排序，兼顾子类、身体形态和 carrier 的覆盖；每篇写了中文入选理由。</li></ul>')
    a('</div>')

    # ---------------------------------------------------------- 2 definition
    a('<div class="section"><h2>2　定义：什么算 agent</h2>')
    a('<p>先看<b>模型是什么</b>：研究对象是通用大模型（LLM / VLM）做具身任务，它可以出计划、调工具、写代码，也可以直接出动作；'
      '具身大模型（VLA、分层 VLA、WAM、机器人基础模型）直接出动作的工作不收。界线确实模糊，所以判断看模型是不是通用大模型，'
      '不看输出是计划还是动作。再看<b>过程</b>：「模型 + harness + 环」是否满足三条判定。下图是逐篇判定时的顺序：</p>')
    a(f'<figure>{fig_flow()}<figcaption><b>图 2　agent 判定流程。</b>⓪ 是范围，①–③ 是三条 agent 判定，必须全部满足；'
      '④ 决定进核心还是只作边界讨论。最后按 arXiv 首版年份分为先驱（2022–2025）和 2026，两者按 seat 一起呈现。</figcaption></figure>')
    a('<div class="callout"><h3>「编写闭环」：以 ReKep 为例</h3>'
      '<p class="small">GPT-4o 只被调用一次，写出各阶段的子目标约束和路径约束（Python 函数）。执行时求解器以约 10 Hz 依跟踪到的关键点重解；'
      '路径约束被破坏时回溯到前面的阶段。随结果而变的逻辑是 VLM 写的，触发机制是固定框架。表中用「闭环」一列区分再决策与编写闭环。</p>'
      f'<p class="small" style="margin:0">核心表中的编写闭环：2026 年 {len(authored_core)} 篇'
      + (f'（{"、".join(r["key"] for r in authored_core[:6])}{"等" if len(authored_core) > 6 else ""}）' if authored_core else '')
      + f'；先驱 {len(authored_pio)} 篇（{"、".join(r["key"] for r in authored_pio)}）。</p></div>')
    a('<div class="callout"><h3>两个例外：约束编程与 agentic Real2Sim</h3>'
      '<p class="small">下面两类即使模型只写一次、不再闭环，也按 agent 收录，「闭环」一列记开环：（1）<b>约束 / 关键点编程</b>：'
      'VLM 写出约束、关键点、可供性或代价函数，由求解器转成动作（CoPa、MOKA 一类）；（2）<b>agentic Real2Sim</b>：agent 从真实数据重建'
      '可交互的仿真场景，自己决定资产、位姿、铰接、物理参数或仿真代码。没有基础模型做决策的重建方法（NeRF、经典辨识）仍不算。</p>'
      f'<p class="small" style="margin:0">2026 核心中开环的 {len(open_core)} 篇'
      + (f'：{"、".join(r["key"] for r in open_core[:8])}{"等" if len(open_core) > 8 else ""}' if open_core else '') + '。</p></div>')
    a('<p class="small"><b>三个常见误区</b>：RL 微调不等于 agency（SimpleVLA-RL 一类没有显式决策，判 OUT）；'
      '架构内的 memory 不等于 agency（MemoryVLA 一类判 OUT，agent 自己读写的 memory 才计入）；'
      '多机器人不等于 multi-agent（一个 LLM 调度多台机器人，如 SMART-LLM，topology 记为 1:N）。</p>')
    a('</div>')

    # ---------------------------------------------------------- 3 taxonomy
    a('<div class="section"><h2>3　分类：五个 Seat，从先驱到 2026</h2>')
    a('<p><b>主轴 Seat</b> 回答「agent 坐在哪里」。判定依据是 agent 的输出<b>在什么阶段产生</b>、<b>由谁消费</b>：'
      '评测时被调用的是 Controller 或 Supervisor；部署前产出、冻结后再交给系统的是 Teacher、Designer 或 Developer。</p>')
    a(f'<figure>{fig_seats(rows)}<figcaption><b>图 3　五个 Seat 围绕机器人身体。</b>右侧两个 seat 在评测时工作：Controller 持续驱动，'
      'Supervisor 只在异常时介入。左侧三个 seat 在部署前工作，产出冻结后进入部署的系统。Real2Sim / Sim2Real 不是新的 seat，'
      '而是横跨 Designer 与 Developer 的专题（第 5 节）。</figcaption></figure>')
    a('<p><b>副轴 Carrier</b> 现在只剩两类：G（通用模型原样使用）和 C（为 agent 角色微调或蒸馏、仍通过工具 / 技能 / 代码行动）。'
      '原来的 H（分层双系统）和 I（一个模型既决策又出动作）属于具身大模型路线，按你的决定不收；你最初「agency 在哪里」四类中的'
      '「分层双系统」「内化」因此只在正文作为对照，「外部编排」对应 G / C，「multi-agent」改为 Topology 列。下图按时期展开五个 seat：</p>')
    a(f'<figure>{fig_grid(rows)}<figcaption><b>图 4　Seat × 时期。</b>左列是 2022–2025 年的先驱，右列是 2026 年的论文；格中是篇数和代表论文，'
      '颜色越深篇数越多。Controller 从 2022 年起就有大量先驱；Supervisor、Designer、Teacher、Developer 的源头在 2023–2025 年，'
      '到 2026 年各自成群。</figcaption></figure>')
    a('</div>')

    # ---------------------------------------------------------- 4 overview
    a('<div class="section"><h2>4　核心论文全景：从先驱到 2026</h2>')
    a(f'<p>{n_pio} 篇先驱是每个 seat 的源头：2022 年只有 Controller（SayCan、Code as Policies、Inner Monologue），'
      '之后 Supervisor、Designer、Teacher、Developer 依次出现。虚线卡片是开创了方向、但不满足闭环判定的工作。</p>')
    a(f'<figure>{fig_pioneers(rows)}<figcaption><b>图 5　先驱按 Seat 与年份分布。</b>2022 年只有 Controller；'
      '之后 Supervisor、Designer、Teacher、Developer 依次出现。</figcaption></figure>')
    a(f'<p>2026 年论文最多：{n_core} 篇按 seat 和季度排开（Q1 {q["1"]}、Q2 {q["2"]}、Q3 {q["3"]}、Q4 {q["4"]} 篇）。'
      f'Controller 拆为三个子章：编排型 {sub["orchestrator"]}、直接驱动型 {sub["direct"]}、lifelong / memory 型 {sub["lifelong"]}，'
      f'另有 {themed_ctl} 篇 Controller 在 Real2Sim 与 VLN 两章。图中 ◆ / △ 标出两个专题章，完整表格见附录 A。</p>')
    a(f'<figure>{fig_quarters(rows)}<figcaption><b>图 6　2026 年论文按 Seat 与季度分布。</b>下半年明显加速；'
      'Developer 和 lifelong 型 Controller 几乎都出现在 Q3 以后，对应 coding agent 和 harness 进化的浪潮。</figcaption></figure>')
    a('</div>')

    # ---------------------------------------------------------- 5 real2sim
    a('<div class="section"><h2>5　子方向：Real2Sim / Sim2Real</h2>')
    a('<p>这是横跨 Designer 与 Developer 的一个子方向，表中只收代表作，其余列在 README 的扩展列表。内容是 agent 自己搭建、校准、利用仿真：从真实视频或数据集重建可交互的仿真世界，在里面练习、诊断失败、'
      '改进技能，再借少量真机试验修正仿真器并迁移回真机。按 Seat 规则，构建「题目」（仿真世界、资产、参数）归 Designer，'
      '改进「解法」（技能、代码、prompt）归 Developer，所以这一节横跨两个 seat，每篇仍标出 seat 颜色。'
      '按你的决定，agent 重建机器人操作场景的工作一律收录，一次构建的在「闭环」一列记开环。</p>')
    a(f'<figure>{fig_r2s(rows)}<figcaption><b>图 7　Real2Sim / Sim2Real 板块。</b>彩色卡片是 2026 年的核心论文，颜色表示 seat；'
      '灰色卡片是更早的先驱（右下角为年份）和评测资源。</figcaption></figure>')
    a(table_core(rows, "Real2Sim / Sim2Real · 2026", lambda r: r["tier"] == "core" and r.get("theme") in R2S_THEMES,
                 show_seat=True))
    a('</div>')

    # ---------------------------------------------------------- 6 VLN
    a('<div class="section"><h2>6　VLN 与具身导航</h2>')
    a('<p>以导航为主任务的 agent 单列一章：连续环境（Habitat VLN-CE 等）或真机上的 vision-and-language navigation、'
      'object-goal 与实例导航、长程探索。2026 年的论文须在连续环境或真机上评测；R2R 离散图上的开创性 VLN agent 只作为先驱，'
      '正文在边界一节讨论。导航中顺带操作的移动操作任务仍归 Controller 各子章。</p>')
    if vln_pio:
        a('<p class="small"><b>先驱：</b>' + "".join(chip(r, MUTED, year=True) for r in sorted(vln_pio, key=lambda r: r["date"]))
          + '</p>')
    a(table_core(rows, "VLN 与具身导航 · 2026", lambda r: r["tier"] == "core" and r.get("theme") == "vln", show_seat=True))
    a('</div>')

    # ---------------------------------------------------------- 6 trends
    a('<div class="section"><h2>7　趋势证据</h2>')
    a(f'<p>核心表是按名额挑的，不能当趋势证据。所以下面用全部经 Sonnet 判定或复核为 core 的论文统计（{sum(x["n"] for x in trend)} 篇，'
      f'年份取 arXiv 首版）。2026 年是全量检索（{t["2026"]["n"]} 篇），2022–2025 年只含种子邻域和高被引论文，'
      '所以只看各年内部的结构，不比较绝对数量。</p>')
    a(f'<figure>{fig_share(trend)}<figcaption><b>图 8　各年份主 seat 的占比。</b>每篇论文按主 seat 计一次。'
      f'Controller 一直是多数；2026 年 Developer 占到 {pct(t["2026"]["prim"]["Developer"] / t["2026"]["n"])}。'
      '不足以放下标签的色块，数值见下表。</figcaption></figure>')
    eff_pts = [(x["year"], x["eff"]) for x in trend]
    ctl_pts = [(x["year"], 100 * ctl[x["year"]]) for x in trend]
    a('<figure><div class="charts2">'
      f'<div><h4>有效 seat 数</h4><div class="s">把每年各 seat 的论文数当成分布，取熵的指数；1 表示只有一个 seat</div>'
      f'{fig_line(eff_pts, 4, [0, 1, 2, 3, 4], lambda v, l=False: f"{v:.2f}" if l else f"{v:.0f}", "有效 seat 数")}</div>'
      f'<div><h4>含 Controller 的论文占比</h4><div class="s">主 seat 或次 seat 含 Controller 的论文 ÷ 该年论文数</div>'
      f'{fig_line(ctl_pts, 100, [0, 25, 50, 75, 100], lambda v, l=False: f"{v:.0f}%", "含 Controller 的论文占比")}</div>'
      f'</div><figcaption><b>图 9　主线的两个支撑。</b>左：seat 越来越分散（{trend[0]["eff"]:.2f} → {trend[-1]["eff"]:.2f}）。'
      f'右：含 Controller 的论文占比在 2023 年后保持在 {pct(min(ctl[y] for y in late))}–{pct(max(ctl[y] for y in late))}。'
      '两者合起来就是「seat 在增加，而不是迁移」。</figcaption></figure>')
    th = "".join(f"<th class='num'>{s}</th>" for s in SEATS)
    tr = "".join(
        f"<tr><td>{x['year']}</td><td class='num'>{x['n']}</td>"
        + "".join(f"<td class='num'>{x['prim'][s]}（{x['alls'][s]}）</td>" for s in SEATS)
        + f"<td class='num'>{pct(ctl[x['year']])}</td><td class='num'>{pct(dev[x['year']])}</td>"
          f"<td class='num'>{x['eff']:.2f}</td></tr>" for x in trend)
    a('<table class="tbl"><colgroup><col style="width:7%"><col style="width:6%"></colgroup>'
      f'<tr><th>年份</th><th class="num">n</th>{th}<th class="num">含 Controller</th><th class="num">含 Developer</th>'
      f'<th class="num">有效 seat 数</th></tr>{tr}</table>')
    a('<p class="note" style="margin-top:4pt">各 seat 一栏：主 seat 篇数（括号内为主 seat 或次 seat 含该 seat 的篇数）。'
      '投稿前仍应按草稿 §10 的方案，从候选中分层随机抽样、两人盲标后复核这两个趋势。</p>')
    a('<div style="break-inside: avoid"><h2 style="margin-top:14pt">8　下一步</h2><ol>'
      '<li><b>冻结核心表</b>：你审阅后，我按你的意见改 <code>core_selection.csv</code> 并重新生成 README 和这份报告。</li>'
      f'<li><b>补全链接</b>：目前只有 {c["links"]}/{len(rows)} 篇能从 arXiv comment 中提取到项目或代码链接，其余需要联网逐篇查。</li>'
      f'<li><b>全文审计</b>：2026 年的核心论文大多只按摘要判过，先核实 seat 与闭环形式有争议的几篇。</li>'
      '<li><b>写正文</b>：按 Seat 分章，每章先讲先驱再讲 2026；Controller 拆三个子章，VLN 单独一章，Real2Sim / Sim2Real 作为子方向一小节；'
      '第 7 节的数字作为趋势证据。</li>'
      '<li><b>可选</b>：做一个类似 WAM survey 的 GitHub Pages 浏览器；对已有 survey 做反向滚雪球，进一步提高查全率。</li></ol></div>')
    a('</div>')

    # ---------------------------------------------------------- appendix A
    a('<div class="section"><h2>附录 A　按 Seat 的论文表：先驱与 2026</h2>')
    a('<p class="note">短名链接到 arXiv；月份为 arXiv 首版；会议来自 Semantic Scholar，未发表的记为 arXiv；★ 为用户点名；'
      '<span class="new">新</span> 为这一轮新增。Real2Sim / Sim2Real 章见第 5 节，VLN 章见第 6 节，这里不重复。</p>')
    for s_ in ("orchestrator", "direct", "lifelong"):
        f_ = lambda r, s_=s_: r["seat"] == "Controller" and r["sub"] == s_ and not r.get("theme")
        a(table_pioneers(rows, f"Controller · {SUB_ZH[s_]} · 先驱", f_))
        a(table_core(rows, f"Controller · {SUB_ZH[s_]} · 2026", lambda r, f_=f_: r["tier"] == "core" and f_(r)))
    for s_ in SEATS[1:]:
        f_ = lambda r, s_=s_: r["seat"] == s_ and not r.get("theme")
        a(table_pioneers(rows, f"{s_} · {SEAT_ZH[s_]} · 先驱", f_))
        a(table_core(rows, f"{s_} · {SEAT_ZH[s_]} · 2026", lambda r, f_=f_: r["tier"] == "core" and f_(r)))
    a(table_pioneers(rows, "Real2Sim / Sim2Real 与 VLN 两章的先驱", lambda r: bool(r.get("theme"))))
    a('</div>')

    # ---------------------------------------------------------- appendix B
    a('<div class="section"><h2>附录 B　资源、候补与质量控制</h2>')
    resx = sorted(res, key=lambda r: (SEATS.index(r["seat"]) if r["seat"] in SEATS else 9, r["date"]))
    a(f'<h3>Benchmark 与资源（{len(resx)}）</h3><table class="tbl"><colgroup><col style="width:20%"><col style="width:6%">'
      '<col style="width:9%"><col style="width:11%"><col></colgroup>'
      '<tr><th>短名</th><th>年份</th><th>会议</th><th>评测的 seat</th><th>说明</th></tr>'
      + "".join(f'<tr><td>{link(r)}</td><td>{r["year"]}</td><td>{esc(r["venue"])}</td><td>{r["seat"]}</td>'
                f'<td>{esc(r["why"])}</td></tr>' for r in resx) + '</table>')
    if alt:
        a(f'<h3>候补：因名额没收的论文（{len(alt)}）</h3><table class="tbl"><colgroup><col style="width:22%"><col style="width:20%">'
          '<col></colgroup><tr><th>短名</th><th>Seat</th><th>说明</th></tr>'
          + "".join(f'<tr><td><a href="https://arxiv.org/abs/{x["arxiv"]}">{esc(x["key"])}</a></td><td>{esc(x["seat"])}</td>'
                    f'<td>{esc(x["why"])}</td></tr>' for x in alt) + '</table>')
    cols = ["core", "precursor", "boundary", "resource", "out"]
    a('<div style="break-inside: avoid"><h3>第一遍 Sonnet 判定与第一轮测试集判定的对照</h3>'
      '<p class="small">第一轮的测试集判定用的是复杂版规则（含 CORE-P、UNRESOLVED 等层级）。下表按第一轮的层级分行，'
      '看这一轮第一遍（严格闭环规则下）Sonnet 怎么判。Sonnet 对 CORE-P 和 BOUNDARY 偏宽，人工挑选时已按定义纠正。</p>'
      '<table class="tbl"><tr><th>第一轮层级</th><th class="num">篇数</th>'
      + "".join(f"<th class='num'>判 {x}</th>" for x in cols) + "</tr>"
      + "".join(f"<tr><td>{k}</td><td class='num'>{sum(agree[k].values())}</td>"
                + "".join(f"<td class='num'>{agree[k][x] or '·'}</td>" for x in cols) + "</tr>"
                for k in ("CORE", "CORE-P", "BOUNDARY", "UNRESOLVED", "RESOURCE", "OUT")) + "</table>"
      + f'<p class="small" style="margin-top:4pt">第一轮 CORE 中，两边都判 core 的 {seat_n} 篇里有 {seat_same} 篇主 seat 一致。</p></div>')
    a('<h3>文件位置</h3><table class="tbl"><colgroup><col style="width:36%"><col></colgroup>'
      '<tr><th>文件</th><th>内容</th></tr>'
      '<tr><td>docs/definition.md</td><td>正文版定义（通用大模型范围、三条判定与两个例外、先驱与 2026、Real2Sim / Sim2Real 与 VLN 章）</td></tr>'
      '<tr><td>docs/definition_draft.md</td><td>完整细则，作为附录和标注指南</td></tr>'
      '<tr><td>data/core/core_selection.csv</td><td>人工挑选的核心表输入；增删论文改这个文件</td></tr>'
      '<tr><td>data/core/core_table.csv</td><td>生成的核心表（含全部标签）</td></tr>'
      f'<tr><td>data/core/fine_labels.csv</td><td>{c["judged"]:,} 篇的逐篇判定（pass 列标出判定轮次，prev 列保留被复核前的判定）</td></tr>'
      '<tr><td>data/core/extended_2026.csv、extended_2022_2025.csv</td><td>核心表之外、满足定义的 2026 年与 2022–2025 年论文（README 扩展列表）</td></tr>'
      '<tr><td>data/candidates/s2_sweep_2026.jsonl、s2_coarse_2026.csv</td><td>2026 年关键词检索结果与粗筛标签</td></tr>'
      '<tr><td>data/core/gap_candidates.jsonl、gap2_ / gap3_candidates.jsonl</td><td>三轮联网补漏的结果</td></tr>'
      '<tr><td>docs/core_review.md</td><td>中文审阅清单</td></tr>'
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
