#!/usr/bin/env python3
"""Render the agent-loop judgement of the core table (data/core/layer_classification.csv) as
docs/layer_classification.md.

The CSV is the source of truth (UTF-8 with BOM so Excel shows Chinese): change a paper's verdict, layer,
subtype, reason or note there, then re-run this script.

Framework (user, 2026-10-09, docs/agent_loop_framework.png): Agent -> Policy / Code / None -> Env / Sim, the agent
may also act on Env / Sim directly, and information from Env / Sim flows back to the agent. A general-purpose
LLM / VLM agent must exist and play a role. Not every arrow has to be present: the agent only has to connect to
Policy / Code or to Env / Sim (user, same day), so open-loop papers are kept. The agent must be a general large model
used as-is: a model the authors trained or fine-tuned does not count (user, on RoboFAC), and the paper must be about
the agent, not a data platform (user, on RoboTwin 2.0). Since 2026-10-09 every row was judged from the paper's full
text (prompt screening/prompts/content_rejudge.txt, raw output data/judging_runs/content_rejudge/), with the decision
model, its status and a quoted line as evidence. Verdicts: 保留 (kept, with layer L1 / L2 / L3), 资源 (benchmarks), 剔除.

Usage: python3 scripts/build_layer_table.py
"""
import csv, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data/core/layer_classification.csv")
VERDICTS = ["保留", "资源", "剔除"]
LAYERS = ["L1", "L2", "L3", "-"]
SUBS = ["环境/重建", "奖励/任务", "本体/工具", "系统/代码", "策略生产者", "编排者", "经验迁移", "运行时监控", "直接动作",
        "评测L1", "评测L2", "评测L3", ""]
LAYER_D = {"L1": "准备层：执行之前，agent 为机器人创造或重建环境、设计奖励 / 任务、设计本体与工具、修改系统与训练代码；反馈是训练或仿真结果",
           "L2": "中间层（harness）：agent 经由中间的 Policy / Code 影响机器人——写出运行的策略代码、调用技能或 VLA、把经验蒸馏给策略、在运行时监控与恢复",
           "L3": "执行层：中间为 None，通用大模型在执行中自己逐步输出动作"}
SUBD = {"环境/重建": "生成或重建环境、场景、仿真资产、数字孪生", "奖励/任务": "设计奖励、成功判据、任务与课程",
        "本体/工具": "设计机器人形态、硬件或工具", "系统/代码": "修改训练代码、策略代码库、技能库或 harness，按试验保留或回滚",
        "策略生产者": "写出在机器人上运行的策略代码或约束（Code as Policies 一类）", "编排者": "规划并调用技能、工具、运动规划器或 VLA",
        "经验迁移": "agent 的经验、示范或轨迹被蒸馏成策略或更小的模型", "运行时监控": "运行时只在异常时介入：失败检测、安全护栏、恢复、求助",
        "直接动作": "通用大模型在执行中直接输出动作"}
VERDICT_D = {"保留": "现成的通用大模型（未经作者训练或微调）作为 agent 存在并起作用（连到 Policy / Code 或 Env / Sim），且 agent 是论文的主体",
             "资源": "以通用大模型 agent 为对象的 benchmark 或评测研究",
             "剔除": "决策者是作者训练或微调的模型、VLA 或专用模型，或论文主体是数据生成平台、资产流水线或 VLA 训练"}


def table(rows, L):
    L += ["| 论文 | 年 | 决策模型 | 理由 | 原文证据 | 备注 |", "|---|---|---|---|---|---|"]
    for r in rows:
        name = f"[{r['key']}](https://arxiv.org/abs/{r['arxiv']})" if r["arxiv"] else r["key"]
        L.append(f"| {name} | {r['year']}{'（先驱）' if r['tier'] == '先驱' else ''} | {r['decision_model']}（{r['model_status']}） | "
                 f"{r['reason']} | {r['evidence']} | {r['note']} |")
    L.append("")


def main():
    recs = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    recs.sort(key=lambda r: (VERDICTS.index(r["verdict"]), LAYERS.index(r["layer"]), SUBS.index(r["subtype"]),
                             r["tier"] != "先驱", r["year"], r["key"]))
    vc = Counter(r["verdict"] for r in recs)
    kept = [r for r in recs if r["verdict"] == "保留"]
    L = ["# 按 agent 回路框架重判核心表\n",
         "![agent 回路框架](agent_loop_framework.png)\n",
         "框架（2026-10-09）：Agent → Policy / Code / None → Env / Sim；agent 也可以直接作用于 Env / Sim；"
         "Env / Sim 的信息回到 agent。箭头表示信息流动，**通用大模型 agent 必须存在，并在其中扮演角色**；"
         "箭头不必全部存在，agent 只要连到 Policy / Code 或 Env / Sim 其中之一即可，所以开环（没有 E→A）的论文也保留。"
         "agent 必须是**现成的通用大模型**：作者训练或微调过的模型不算（AgentVLN、Ludi、RoboFAC 因此剔除），训练过的 VLA、"
         "技能或感知模型只能作为 agent 调用的工具；论文主体必须是 agent，数据生成平台不算。\n",
         "每篇都读了全文（方法与实验设置），「决策模型」一列写明谁在做决策，括号内 G = 现成通用模型、FT = 作者训练或微调、"
         "SPEC = VLA 或专用模型；「原文证据」是论文原句。\n",
         f"对 `data/core/core_table.csv` 的 {len(recs)} 篇逐篇重判：读全文判定（提示词 `screening/prompts/content_rejudge.txt`，"
         "原始输出 `data/judging_runs/content_rejudge/`），人工逐条复核，与上一版不同的写在「备注」里。机器可读版本："
         "`data/core/layer_classification.csv`（带 BOM，Excel 可直接打开）；改它后运行 `python3 scripts/build_layer_table.py`。"
         "CSV 的「箭头」一列：A→M agent 写出 / 选择 / 修改中间层，A→E agent 直接作用于环境，M↔E 中间层在环境中运行，E→A 环境信息回到 agent。\n",
         "## 结果\n", "| 结论 | 篇数 | 含义 |", "|---|---|---|"]
    L += [f"| {v} | {vc[v]} | {VERDICT_D[v]} |" for v in VERDICTS]
    lc = Counter((r["layer"], r["subtype"]) for r in kept)
    L += ["\n保留的论文按三层分：\n", "| 层 | 子类 | 篇数 | 含义 |", "|---|---|---|---|"]
    L += [f"| {t[0]} | {t[1]} | {lc[t]} | {SUBD.get(t[1], '')} |"
          for t in sorted(lc, key=lambda t: (LAYERS.index(t[0]), SUBS.index(t[1])))]
    n_open = sum(1 for r in kept if "E→A" not in r["arrows"])
    L.append(f"\n保留的 {len(kept)} 篇中，{n_open} 篇开环（「箭头」一列没有 E→A，多为 2022–2024 的先驱，如 Code as Policies、"
             f"ReKep）。\n")
    for ly in ("L1", "L2", "L3"):
        xs = [r for r in kept if r["layer"] == ly]
        L.append(f"## 保留 · {ly}（{len(xs)}）\n\n{LAYER_D[ly]}\n")
        for s in [x for x in SUBS if any(r["subtype"] == x for r in xs)]:
            ys = [r for r in xs if r["subtype"] == s]
            L.append(f"### {s}（{len(ys)}）\n")
            table(ys, L)
    for v in ("资源", "剔除"):
        xs = [r for r in recs if r["verdict"] == v]
        L.append(f"## {v}（{len(xs)}）\n\n{VERDICT_D[v]}\n")
        table(xs, L)
    open(os.path.join(ROOT, "docs/layer_classification.md"), "w").write("\n".join(L) + "\n")
    print("docs/layer_classification.md:", dict(vc), dict(Counter(r["layer"] for r in kept)))


if __name__ == "__main__":
    main()
