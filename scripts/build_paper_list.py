#!/usr/bin/env python3
"""Render the paper list (data/core/paper_list.csv) as docs/paper_list.md.

The CSV is the source of truth (UTF-8 with BOM so Excel shows Chinese): change a paper's verdict, phase, seat, role,
reason or note there, then re-run this script.

Inclusion (user, 2026-10-09; docs/agent_loop_framework.png): a general large model used as-is must act as the agent and
connect to Policy / Code or to Env / Sim (closing the loop is not required); the paper must be about the agent, not a
data platform; every row was judged from the paper's full text (screening/prompts/content_rejudge.txt).
Classification (user, 2026-10-09, back to the earlier seats): two phases, pre-execution (Designer, Teacher, Developer)
and runtime (Controller, Supervisor); `role` says what the agent does within its seat.

Usage: python3 scripts/build_paper_list.py
"""
import csv, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, "data/core/paper_list.csv")
VERDICTS = ["保留", "资源", "剔除"]
PHASES = [("执行前", "pre-execution", "agent 的产出在机器人执行任务之前产生，冻结后交给部署的系统"),
          ("运行时", "runtime", "agent 在任务执行过程中起作用")]
SEATS = [("Designer", "执行前", "设计学习问题：环境与场景、仿真、奖励、任务与课程"),
         ("Teacher", "执行前", "自己先执行，经检验的示范或经验成为策略的训练目标"),
         ("Developer", "执行前", "修改系统本身：训练代码、技能库、harness、硬件与工具，按试验保留或回滚"),
         ("Controller", "运行时", "每一步决定机器人做什么：编排技能 / 工具 / VLA，当场写出策略代码或约束，或直接出动作"),
         ("Supervisor", "运行时", "只在异常时介入：失败检测、安全护栏、恢复、求助")]
ROLES = ["环境/重建", "奖励/任务", "示范/蒸馏", "系统/代码", "本体/工具", "编排", "写策略", "直接动作", "监控/恢复", "评测", ""]
ROLE_D = {"环境/重建": "生成或重建环境、场景、仿真资产与数字孪生", "奖励/任务": "设计奖励、成功判据、任务与课程",
          "示范/蒸馏": "agent 自己执行，经验蒸馏成策略或小模型", "系统/代码": "改训练代码、技能库或 harness，按试验保留或回滚",
          "本体/工具": "设计机器人形态、硬件或工具", "编排": "规划并调用技能、工具、运动规划器或 VLA",
          "写策略": "写出在机器人上运行的策略代码或约束", "直接动作": "通用大模型在执行中自己输出动作",
          "监控/恢复": "失败检测、安全护栏、恢复与求助"}
VERDICT_D = {"保留": "现成的通用大模型（未经作者训练或微调）作为 agent 存在并起作用，连到 Policy / Code 或 Env / Sim，且 agent 是论文的主体",
             "资源": "以通用大模型 agent 为对象的 benchmark 或评测研究（「Seat」为被评测的位置）",
             "剔除": "决策者是作者训练或微调的模型、VLA 或专用模型，或论文主体是数据生成平台、资产流水线或 VLA 训练"}
SEAT_ORDER = [s for s, _, _ in SEATS] + ["-"]


def table(rows, L):
    L += ["| 论文 | 年 | 角色 | 决策模型 | 理由 | 原文证据 | 备注 |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        name = f"[{r['key']}](https://arxiv.org/abs/{r['arxiv']})" if r["arxiv"] else r["key"]
        L.append(f"| {name} | {r['year']}{'（先驱）' if r['tier'] == '先驱' else ''} | {r['role']} | "
                 f"{r['decision_model']}（{r['model_status']}） | {r['reason']} | {r['evidence']} | {r['note']} |")
    L.append("")


def main():
    recs = list(csv.DictReader(open(CSV, encoding="utf-8-sig")))
    recs.sort(key=lambda r: (VERDICTS.index(r["verdict"]), SEAT_ORDER.index(r["seat"]), ROLES.index(r["role"]),
                             r["tier"] != "先驱", r["year"], r["key"]))
    vc = Counter(r["verdict"] for r in recs)
    kept = [r for r in recs if r["verdict"] == "保留"]
    sc, pc = Counter(r["seat"] for r in kept), Counter(r["phase"] for r in kept)
    L = ["# Agentic Embodiment 论文清单\n",
         "## 收录标准\n",
         "![agent 回路框架](agent_loop_framework.png)\n",
         "回路：Agent → Policy / Code / None → Env / Sim；agent 也可以直接作用于 Env / Sim；Env / Sim 的信息可以回到 agent。",
         "收录要求**现成的通用大模型**（未经作者训练或微调）作为 agent 存在并起作用，连到 Policy / Code 或 Env / Sim 其中之一即可"
         "（开环也算）；论文主体必须是 agent，数据生成平台、资产流水线不算；训练过的 VLA、技能、感知模型只能作为 agent 调用的工具。"
         "每篇都读了全文判定，「决策模型」一列写明谁在做决策，括号内 G = 现成通用模型、FT = 作者训练或微调、SPEC = VLA 或专用模型；"
         "「原文证据」是论文原句。\n",
         "## 分类：两个阶段，五个 Seat\n",
         "| 阶段 | Seat | 含义 | 篇数 |", "|---|---|---|---|"]
    L += [f"| {ph} | {s} | {d} | {sc[s]} |" for s, ph, d in SEATS]
    L += [f"\n执行前 {pc['执行前']} 篇，运行时 {pc['运行时']} 篇。「角色」一列是 agent 在 Seat 里具体做什么：\n",
          "| 角色 | 含义 |", "|---|---|"] + [f"| {k} | {v} |" for k, v in ROLE_D.items()]
    L += ["\n机器可读版本：`data/core/paper_list.csv`（带 BOM，Excel 可直接打开）；改它后运行 `python3 scripts/build_paper_list.py`。"
          "判定的提示词在 `screening/prompts/content_rejudge.txt`，原始输出在 `data/judging_runs/content_rejudge/`。\n",
          "## 结果\n", "| 结论 | 篇数 | 含义 |", "|---|---|---|"]
    L += [f"| {v} | {vc[v]} | {VERDICT_D[v]} |" for v in VERDICTS]
    L.append("")
    for ph, en, d in PHASES:
        L.append(f"## {ph}（{en}，{pc[ph]} 篇）\n\n{d}\n")
        for s, ph2, sd in SEATS:
            if ph2 != ph:
                continue
            xs = [r for r in kept if r["seat"] == s]
            L.append(f"### {s}（{len(xs)}）\n\n{sd}\n")
            table(xs, L)
    ma = [r for r in recs if r["verdict"] != "剔除" and "多智能体" in (r.get("topic") or "")]
    L.append(f"## 专题：多智能体（{len(ma)}）\n\n多智能体是主系统的核心：通用大模型 agent 协调两个及以上机器人，或系统由分工不同、"
             "彼此对话或交接工作的多个通用大模型 agent 组成（用户 2026-10-09 要求单独成章；定义见 `definition.md`）。"
             "这些论文同时列在各自的 Seat 下。\n")
    L += ["| 论文 | 年 | 结论 | Seat | 角色 | 理由 |", "|---|---|---|---|---|---|"]
    for r in ma:
        name = f"[{r['key']}](https://arxiv.org/abs/{r['arxiv']})" if r["arxiv"] else r["key"]
        L.append(f"| {name} | {r['year']} | {r['verdict']} | {r['seat']} | {r['role']} | {r['reason']} |")
    L.append("")
    for v in ("资源", "剔除"):
        xs = [r for r in recs if r["verdict"] == v]
        L.append(f"## {v}（{len(xs)}）\n\n{VERDICT_D[v]}\n")
        table(xs, L) if v == "剔除" else _res(xs, L)
    open(os.path.join(ROOT, "docs/paper_list.md"), "w").write("\n".join(L) + "\n")
    print("docs/paper_list.md:", dict(vc), dict(pc), dict(sc))


def _res(rows, L):
    L += ["| 论文 | 年 | 被评测的 Seat | 理由 |", "|---|---|---|---|"]
    for r in rows:
        name = f"[{r['key']}](https://arxiv.org/abs/{r['arxiv']})" if r["arxiv"] else r["key"]
        L.append(f"| {name} | {r['year']} | {r['seat']} | {r['reason']} |")
    L.append("")


if __name__ == "__main__":
    main()
