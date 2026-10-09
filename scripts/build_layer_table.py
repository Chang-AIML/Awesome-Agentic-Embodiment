#!/usr/bin/env python3
"""Render the three-layer classification (data/core/layer_classification.csv) as docs/layer_classification.md.

The CSV is the source of truth: change a paper's layer, subtype, reason or note there (UTF-8 with BOM so Excel
shows Chinese), then re-run this script.  Layers (user's framework, 2026-10-09):
  L1 preparation before execution, L2 harness between the LLM and the robot, L3 general LLM as policy,
  plus 资源 (benchmarks) and 剔除 (does not fit).

Usage: python3 scripts/build_layer_table.py
"""
import csv, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data/core/layer_classification.csv")
LAYERS = ["L1", "L2", "L3", "资源", "剔除"]
SUBS = ["环境/重建", "奖励/任务", "本体/工具", "系统/代码", "策略生产者", "编排者", "经验迁移", "运行时监控", "直接动作",
        "评测L1", "评测L2", "评测L3", "评测多层", "—"]
DESC = {"L1": "准备层（pre-execution）：执行之前，为机器人创造或重建环境、设计奖励 / 任务、设计本体与工具、修改系统与训练代码；产物在部署前冻结",
        "L2": "中间层（harness）：LLM 不直接出低层动作，隔着一层影响机器人——写出策略代码 / 约束、编排技能或 VLA、把经验迁移 / 蒸馏给策略、在运行时只在异常时介入",
        "L3": "执行层（General LLM as policy）：执行过程中由通用大模型自己逐步输出动作（关节、位姿、航点、离散动作或语义微动作）",
        "资源": "benchmark、评测研究：不分层，子类写它主要评测哪一层",
        "剔除": "不符合框架：决策者主要是专门训练的模型，LLM 作用很弱，主体是数据生成或评测平台，或主题在三层之外"}
SUBD = {"环境/重建": "生成或重建环境、场景、仿真资产、数字孪生（Real2Sim）", "奖励/任务": "设计奖励、成功判据、任务与课程",
        "本体/工具": "设计机器人形态、硬件或工具", "系统/代码": "修改训练代码、策略代码库、技能库或 harness，按试验保留或回滚",
        "策略生产者": "写出在机器人上运行的策略代码、约束或程序（Code as Policies 一类）", "编排者": "规划并调用技能、工具、运动规划器或 VLA",
        "经验迁移": "agent 的经验、示范或轨迹被蒸馏成策略或更小的模型", "运行时监控": "运行时只在异常时介入：失败检测、安全护栏、恢复、求助",
        "直接动作": "通用大模型在执行中直接输出动作"}
SEATS = ["Controller·orchestrator", "Controller·direct", "Controller·lifelong", "Supervisor", "Teacher", "Designer", "Developer"]


def seat_of(r):
    x = r["old_seat"].split("·")
    return "·".join(x[:2]) if x[0] == "Controller" and len(x) > 1 and x[1] in ("orchestrator", "direct", "lifelong") else x[0]


def main():
    recs = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    recs.sort(key=lambda r: (LAYERS.index(r["layer"]), SUBS.index(r["subtype"]), r["tier"] != "先驱", r["year"], r["key"]))
    cnt = Counter(r["layer"] for r in recs)
    n_t = Counter(r["tier"] for r in recs)
    L = ["# 按三层框架给核心表分类\n",
         f"对 `data/core/core_table.csv` 的 {len(recs)} 篇（先驱 {n_t['先驱']}、2026 年 {n_t['2026']}、资源 {n_t['资源']}）逐篇按三层框架归类，每篇写了理由。"
         "Haiku 逐篇初判（提示词 `screening/prompts/layer_classify.txt`，原始输出 `data/judging_runs/layers/`），之后人工逐条复核；"
         "复核改判和边界情况写在「备注」里。机器可读版本：`data/core/layer_classification.csv`（带 BOM，Excel 可直接打开），"
         "改分类就改这个 CSV，再运行 `python3 scripts/build_layer_table.py`。\n",
         "## 三层定义\n"]
    L += [f"- **{k}**（{cnt[k]} 篇）：{DESC[k]}" for k in LAYERS]
    L += ["\n## 总览\n", "| 层 | 子类 | 篇数 | 含义 |", "|---|---|---|---|"]
    sc = Counter((r["layer"], r["subtype"]) for r in recs)
    for t in sorted(sc, key=lambda t: (LAYERS.index(t[0]), SUBS.index(t[1]))):
        L.append(f"| {t[0]} | {t[1]} | {sc[t]} | {SUBD.get(t[1], '')} |")
    cols = ["L1", "L2", "L3", "剔除"]
    ct = Counter((seat_of(r), r["layer"]) for r in recs if r["tier"] != "资源")
    L += ["\n## 原 Seat 与三层的对应\n", f"不含 {n_t['资源']} 篇资源；Real2Sim 与 VLN 两章的论文按原 Seat 计入。\n",
          "| 原 Seat | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    L += [f"| {s} | " + " | ".join(str(ct[(s, c)] or "·") for c in cols) + " |" for s in SEATS]
    L += ["\n大致对应：Designer、Developer（含 Real2Sim）→ L1；Controller、Supervisor、Teacher → L2；"
          "L3 只来自 Controller 的直接驱动型和导航。\n", "## 需要你确认的边界情况\n"]
    L += [f"- **{r['key']}**（{r['layer']} · {r['subtype']}）：{r['note']}" for r in recs if r["note"]]
    for k in LAYERS:
        L.append(f"\n## {k}\n\n{DESC[k]}\n")
        for s in [x for x in SUBS if any(r["layer"] == k and r["subtype"] == x for r in recs)]:
            xs = [r for r in recs if r["layer"] == k and r["subtype"] == s]
            if s != "—":
                L.append(f"### {s}（{len(xs)}）\n")
            L += ["| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |", "|---|---|---|---|---|---|"]
            for r in xs:
                name = f"[{r['key']}](https://arxiv.org/abs/{r['arxiv']})" if r["arxiv"] else r["key"]
                L.append(f"| {name} | {r['year']}{'（先驱）' if r['tier'] == '先驱' else ''} | {r['old_seat']} | {r['conf']} | "
                         f"{r['reason']} | {r['note']} |")
            L.append("")
    open(os.path.join(ROOT, "docs/layer_classification.md"), "w").write("\n".join(L) + "\n")
    print("docs/layer_classification.md:", dict(cnt))


if __name__ == "__main__":
    main()
