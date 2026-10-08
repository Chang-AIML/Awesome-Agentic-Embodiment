#!/usr/bin/env python3
"""Round-3 curated selection -> data/core/core_selection.csv (run from the repo root). KEPT FOR THE RECORD.

data/core/core_selection.csv is the source of truth: edit the CSV directly. Re-running this script overwrites
the CSV and discards any edit made there since. It shows how round 3 was assembled (grouping by chapter and the
Chinese reasons); rows already in the round-2 selection (data/core/history/core_selection.r2.csv) keep their
reason unless overridden, new rows get added=r3, the coverage-completion batch added=r3c.
"""
import csv, os, sys

OLD = {r["id"]: r for r in csv.DictReader(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "data/core/history/core_selection.r2.csv")))}
FIELDS = ["id", "key", "tier", "seat", "sub", "carrier", "why", "arxiv", "loop", "theme", "added"]
rows = []
TAG = "r3"  # `added` value for rows that were not in the round-2 selection; r3c = coverage-completion batch


def add(id, key, tier, seat="", sub="", carrier="", why=None, loop="", theme="", arxiv=""):
    if why is None:
        why = OLD[id]["why"]
    old = OLD.get(id)
    if old and not arxiv:
        arxiv = old.get("arxiv", "")
    rows.append(dict(id=id, key=key, tier=tier, seat=seat, sub=sub, carrier=carrier, why=why, arxiv=arxiv, loop=loop,
                     theme=theme, added="" if old else TAG))


C, S, T, D, V = "Controller", "Supervisor", "Teacher", "Designer", "Developer"

# ============================================================ 2026 core
# ---- Controller · orchestrator
add("c00168", "RoboClaw", "core", C, "orchestrator", "G")
add("c00811", "Thea", "core", C, "orchestrator", "G")
add("c00904", "Tool-Aligned VLA Agent", "core", C, "orchestrator", "G",
    "VLM agent 规划并挑选专用 VLA 作为工具，依事件触发的进度反馈与失败重规划；VLA-as-tool 编排的代表")
add("c00256", "Physical Agency", "core", C, "orchestrator", "G",
    "LLM 编排者规划、调用 VLA 与参数化技能，从观测核验结果后重规划，针对通用机器人的「编排缺口」")
add("c00150", "Astra Robot Agents", "core", C, "orchestrator", "G",
    "GPT-6 Astra 把原语与 VLA 组合成带检查和重试的 Python 单元，按需请求观测；少用 65% token、成功率高 14%")
add("s00392", "NovaPlan", "core", C, "orchestrator", "G",
    "闭环视频-语言规划：VLM 分解子目标、监控执行、失败时重规划，零样本长程真机操作")
add("c00196", "Cybo-Waiter", "core", C, "orchestrator", "G",
    "人形全身移动操作：VLM 编译带谓词前置条件与成功条件的子任务，3D 检查驱动推进与恢复；覆盖人形")
add("c01120", "ABot-Claw", "core", C, "orchestrator", "G",
    "基于 OpenClaw 的具身 agent 调度异构机器人，持久 memory 与 critic 驱动的局部纠正；1:N 拓扑代表")
add("c01553", "SpaceMind", "core", C, "orchestrator", "G",
    "卫星在轨服务：VLM agent 调度技能与 MCP 工具并自我进化，UE5 仿真与物理实验室验证；覆盖太空机器人")
add("s05604", "AerialClaw", "core", C, "orchestrator", "G",
    "LLM agent 调用无人机的硬技能与 Markdown 软技能，依运行反馈迭代；开源空中 agent 框架")
add("c13403", "Smart-Agriculture Engine", "core", C, "orchestrator", "G",
    "事件驱动的 LLM agent 经农机、无人机与传感器 API 管理整季大豆种植，真实农场部署；覆盖农业")
add("c06162", "AGRO-SUVIDE", "core", C, "orchestrator", "G",
    "手术清创：coding agent 由一次示范构建技能，运行时监控按前后条件组合循环图；覆盖手术机器人")

# ---- Controller · direct
add("c00180", "Show-Harness", "core", C, "direct", "G")
add("t076", "CaP-X", "core", C, "direct", "G")
add("c00453", "Agent as Policy", "core", C, "direct", "G")
add("c00191", "FAEA", "core", C, "direct", "G")
add("c01718", "VIA", "core", C, "direct", "G")
add("t128", "OpenRUA", "core", C, "direct", "G",
    "现成 coding agent 在终端工作区写 ROS 2 代码并当场运行；robot-use agent 本身就是零样本视觉运动策略")
add("c00452", "Astra on RoboDojo", "core", C, "direct", "G",
    "用户点名：通用 LLM（GPT-6 Astra 等）不经微调直接当操作策略（LLM as policy），在 RoboDojo 全部 42 个任务上评测，排名超过 40 个公开策略")
add("c01680", "VLS", "core", C, "direct", "G",
    "VLM 写分阶段可微奖励引导冻结策略的采样，执行反馈触发阶段切换并重新查询 VLM（编写闭环）")
add("c01490", "AquaCap", "core", C, "direct", "G",
    "训练无关的水下 agent 写条件感知的计划与控制程序，配失败感知 memory；覆盖水下机器人")
add("c02710", "KPI", "core", C, "direct", "G",
    "人形：VLM 写轨迹与「跟踪 / 柔顺 / 保持力」契约，固定内核依接触调整刚度（编写闭环）")
add("c00610", "GTA-2", "core", C, "direct", "G",
    "约束编程类：四个角色 VLM 分解任务并写出关键点、轴、控制器组合与参数，控制器零样本执行（一次求解，开环）")
add("c13093", "Embodiment Meets Environment", "core", C, "direct", "G",
    "约束编程类：LLM 在 3D 动态场景图上合成任务约束，执行时强制满足并重塑照护技能模板（编写闭环）；覆盖照护机器人")

# ---- Controller · lifelong / memory
add("c00028", "Harness VLA", "core", C, "lifelong", "G")
add("c01841", "MessyMem", "core", C, "lifelong", "G")
add("c00595", "Teach and Grow", "core", C, "lifelong", "G",
    "coding agent 把少量示范变成带物理反馈的闭环技能块，技能库随使用增长")
add("c01216", "CaP Great Again", "core", C, "lifelong", "G",
    "编程 agent 依执行反馈编写、进化机器人工具，执行 agent 调用；Code as Policies 的 2026 版")
add("s01312", "PhysMem", "core", C, "lifelong", "G",
    "VLM 规划者记录经验、提出物理原理假设并用针对性试验验证，测试时 memory 扩展物理推理")
add("gap:2610.09228", "Robo-COP", "core", C, "lifelong", "G",
    "VLM 编排者在部署中从自己的执行里整理示范、决定何时微调 VLA，只有经验证变好才采用新策略；编排者与策略共同进化")

add("c00981", "Ludi", "core", C, "orchestrator", "C",
    "微调的 VLM 决策核心配工具循环 harness，处理澄清、纠正与社交互动（C）；覆盖社交机器人")

# ---- Supervisor
add("c02774", "FRAMES", "core", S, "-", "G")
add("t270", "WhenToAsk", "core", S, "-", "G")
add("c00702", "Agentic Task Graph", "core", S, "-", "G",
    "三个 agent 预先写出任务图、恢复分支与可执行监控，从被动恢复转向预判（编写闭环）")
add("c01582", "Zetta", "core", S, "-", "G",
    "agent 从 rollout 进化代码化的运行时 critic 与恢复技能，经验证门控保留或回滚")
add("c00958", "UAV Selective Recovery", "core", S, "-", "G",
    "无人机任务运行时只在受阻或无进展时调用外部推理者，选择预定义恢复技能；覆盖空中")
add("s08158", "Contextual Safety Reasoning", "core", S, "-", "G",
    "VLM 从图像推断依情境而变的安全规则并落到地图上，运行时约束开放世界机器人（编写闭环）")
add("s07595", "When to Act, Ask, or Learn", "core", S, "-", "G",
    "VLM 验证者在策略的动作样本中挑选，或在不确定时决定澄清、请求人工干预")
add("c01196", "Beyond Human Demos", "core", S, "-", "G",
    "LLM 写可执行的护栏代码，在运行时过滤遥操作与策略发出的危险指令（编写闭环）")

# ---- Teacher
add("c01707", "GUAVA", "core", T, "-", "G→C")
add("c00481", "RHD", "core", T, "-", "G")
add("t014", "EmbodiedSWE", "core", T, "-", "G")
add("c06161", "Frontier Demo Generation", "core", T, "-", "G",
    "前沿模型自主生成示范，累积纠错的上下文示例，训练出快速的学习策略")
add("c00281", "CAPEX", "core", T, "-", "G",
    "基础模型作为自主示范者，依执行经验重规划并自适应调用频率，行为蒸馏为可部署策略")
add("s06667", "SkillWeaver", "core", T, "-", "G",
    "VLM agent 调用并参数化 RL 训练的神经交互技能、观察结果后探索，产出的轨迹用于训练")

# ---- Designer
add("c00497", "FIND", "core", D, "-", "G")
add("c00812", "RF-Agent", "core", D, "-", "G",
    "LLM agent 用蒙特卡洛树搜索迭代写、改奖励代码，以训练结果为反馈")
add("c11104", "RDA", "core", D, "-", "G",
    "VLM agent 观看轨迹、总结失败模式并迭代修改奖励")
add("c12114", "ROOT", "core", D, "-", "G",
    "在奖励程序、策略与 rollout 的持久实验树上搜索奖励，实现用户指定的足式行为")
add("s10781", "SceneSmith", "core", D, "-", "G",
    "设计者、评审与编排三个 VLM agent 迭代搭建可仿真的室内场景，供机器人学习与评测（47 引）")
add("c08743", "SAGE", "core", D, "-", "G",
    "agent 调用布局与物体生成器和评审，迭代产出可仿真的 3D 场景（56 引）")

# ---- Developer
add("c00802", "ENPIRE", "core", V, "-", "G")
add("c00371", "ASPIRE", "core", V, "-", "G")
add("c00138", "RHO", "core", V, "-", "G")
add("c10397", "HARBOR", "core", V, "-", "G")
add("gap:2606.19419", "RATs (Playful)", "core", V, "-", "G")
add("c00911", "Skill-Harness Evolution", "core", V, "-", "G",
    "冻结模型从 rollout 进化技能与上下文代码 harness，只保留带来提升的修改")
add("c00744", "AdaHVLA", "core", V, "-", "G",
    "多 agent 分析 / 修订循环依 rollout 证据编辑协调 VLA 的代码 harness")
add("c01817", "SPINE", "core", V, "-", "G",
    "子 agent 建立机器人档案并调试双臂遥操作栈（驱动、接口、控制）；真机系统工程")
add("s04167", "Continuum Robot Design", "core", V, "-", "G",
    "LLM 设计者与评审依物理仿真结果迭代修改腱驱动连续体机器人的设计；硬件侧 Developer")
add("gap:2610.08995", "PhysEvo", "core", V, "-", "G",
    "冻结的 GPT-6 Astra 执行任务，meta-agent 依轨迹诊断失败、修改工具与技能并测试后保留；RoboDojo 42 任务，并在真机 PiPER 上继续")
add("gap:2610.09283", "LACE-CRAFT", "core", V, "-", "G",
    "反馈、形态、奖励、整合四个 LLM 角色共享实验记录，交叉评审形态-奖励提案，固定任务指标决定保留或回滚；机器人协同设计")

# ---- Real2Sim / Sim2Real: one sub-direction, representative papers only (seat kept)
add("c00155", "RPG", "core", V, "-", "G",
    "用户点名：从数据集重建练习任务，在仿真中诊断失败、写新技能并修改 system prompt，经跨任务评测保留后回到真机",
    theme="real2sim2real")
add("c00495", "SimEX", "core", V, "-", "G", theme="real2sim2real",
    why="用户点名：coding agent 在仿真中迭代机器人工具箱代码，再借少量真机试验同时修正工具箱与仿真器（robotics AutoResearch）")
add("s11012", "EmbodiedSmith", "core", D, "-", "G", theme="real2sim",
    why="用户点名：场景生成与任务生成互相编辑的递归自改进飞轮，规模化产出仿真数据与评测环境")
add("s00077", "Agentic Real2Sim", "core", D, "-", "G", theme="real2sim",
    why="VLM agent 从真实录像出发，迭代调用工具构建可仿真的物理孪生；agentic Real2Sim 的代表")
add("c00201", "Real2Gym", "core", V, "-", "G", theme="real2sim2real",
    why="agent 从示范视频重建场景、写阶段代码，依仿真结果诊断修正后把技能带回真机")
add("c03222", "Vid2Sid", "core", D, "-", "G", theme="real2sim",
    why="VLM 对比仿真与真实视频、诊断差异并提出物理参数修改，缩小 sim2real 差距")
add("c01489", "Skill2Real", "core", V, "-", "G", theme="sim2real")
add("s03101", "CoDimRecon", "core", D, "-", "G", theme="real2sim",
    why="agentic Real2Sim：agent 会话从多视角 RGB 重建可仿真的刚体、铰接与可变形曲线场景，行为测试暴露差异后针对性修正")
add("c00362", "GPT-6-Astra XLeRobot", "core", C, "lifelong", "G",
    why="GPT-6-Astra 写控制程序驱动 XLeRobot，复用身体知识、经验与技能，并从仿真迁移到真实电梯按钮任务")
add("gap:2610.10479", "Agentic RSR", "core", V, "-", "G", theme="real2sim2real",
    why="agent 从工作区视频恢复尺度、依视觉反馈迭代重建 MuJoCo 场景，coding agent 再开发策略并回到真机；Real2Sim2Real 全链路")

# ---- VLN and embodied navigation
add("c01104", "AgenticNav", "core", C, "direct", "G", theme="vln",
    why="VLM 在 harness 中调用动作、深度与 memory 工具，带着自己的推理历史选择目标像素；VLN-CE 闭环")
add("c01426", "HarnessVLN", "core", C, "orchestrator", "G", theme="vln",
    why="训练无关的 MLLM 规划提案经 harness 验证，执行反馈更新 memory 与拓扑图，统一多种导航任务")
add("c06679", "Embodied Agents Take Control", "core", C, "direct", "G", theme="vln",
    why="通用 coding-agent harness 掌管每一步导航动作并自我纠错，零样本可比工业级系统")
add("c04069", "ASENA", "core", C, "lifelong", "G", theme="vln",
    why="coding agent 写并运行程序、调用导航 VLA 工具、检查结果并修复，经验随任务积累")
add("s03802", "One Agent to Guide Them All", "core", C, "direct", "G", theme="vln",
    why="MLLM 在可交互的度量世界表示上推理并做反事实检查，统一多种 VLN 任务，仿真与真机")
add("s11144", "HAM-VLN", "core", C, "direct", "G", theme="vln",
    why="MLLM 选择下一个路点并写分层 memory（含失败记录），后续调用再读入")
add("s06980", "OnFly", "core", C, "direct", "G", theme="vln",
    why="机载零样本空中 VLN：一个 VLM 生成导航目标，另一个依关键帧监控进度与安全；覆盖无人机")
add("s05277", "AgentVLN", "core", C, "orchestrator", "C", theme="vln",
    why="训练过的 VLM 作大脑调用导航技能库，带自我纠错与主动探索（C）")
add("c03976", "LocalNav", "core", T, "-", "G→C", theme="vln")
add("c06226", "RoboFind", "core", C, "orchestrator", "G", theme="vln",
    why="导航、验证、恢复三个 agent 驱动四足为视障用户找物，验证候选并触发恢复")
add("c05659", "NORM-Nav", "core", C, "direct", "G", theme="vln",
    why="约束编程类导航：LLM 把指令解析成结构化行为约束，依实时感知落成代价地图层由规划器执行并在线重规划")
add("s11075", "Air-Ground VLN", "core", C, "orchestrator", "G", theme="vln",
    why="无人机与地面车的 VLM 在共享鸟瞰地图上推理并互相下发子目标，空地协同 VLN；×N 拓扑")
add("gap:2603.12696", "HaltNav", "core", C, "orchestrator", "C", theme="vln",
    why="MLLM 在轻量拓扑图（osmAG）上把路线拆成子指令，微调的 VLM 在门关闭、拥挤等情况下停止并触发重规划；仿真与真机 Fetch")

# ============================================================ pioneers 2022-2025
add("seed:zero-shot-planners", "ZS-Planners", "pioneer", C, "orchestrator", "G",
    "LLM 作零样本规划者的起点：把高层指令分解为可执行步骤；开环", loop="none")
add("seed:socratic-models", "Socratic Models", "pioneer", C, "orchestrator", "G",
    "多个预训练模型用语言组合推理，LLM 规划并调用感知与技能；通用模型组合做具身任务的起点（开环）", loop="none")
add("c00091", "TidyBot", "pioneer", C, "orchestrator", "G",
    "LLM 从少量示例归纳用户偏好并给出整理计划，真机移动操作；个性化的早期代表（开环）", loop="none")
add("seed:saycan", "SayCan", "pioneer", C, "orchestrator", "G", loop="re-decide")
add("seed:inner-monologue", "Inner Monologue", "pioneer", C, "orchestrator", "G", loop="re-decide")
add("c00089", "ChatGPT for Robotics", "pioneer", C, "direct", "G",
    "ChatGPT 依提示与人类反馈写机器人代码并迭代修改，覆盖操作、无人机与导航；把通用 LLM 直接用于机器人控制的代表作（755 引）",
    loop="authored")
add("c00073", "Text2Motion", "pioneer", C, "orchestrator", "G",
    "LLM 生成技能序列并用学习的可行性模型在执行前检查几何可行性；只有预测性检查（开环）", loop="none")
add("c00023", "Language to Rewards", "pioneer", C, "direct", "G",
    "LLM 把指令写成奖励参数，由 MPC 在线优化成动作；约束 / 目标编程一支的早期代表（编写闭环，461 引）", loop="authored")
add("c00642", "SMART-LLM", "pioneer", C, "orchestrator", "G",
    "LLM 分解任务、组队并分配给多台机器人；多机器人任务规划的早期代表（1:N，开环）", loop="none")
add("seed:code-as-policies", "Code as Policies", "pioneer", C, "direct", "G",
    "用户认定的奠基作：LLM 写出带感知反馈循环的策略程序（编写闭环）；coding agent 一脉的源头", loop="authored")
add("seed:progprompt", "ProgPrompt", "pioneer", C, "direct", "G",
    "程序化提示生成带断言与恢复动作的任务程序（编写闭环）", loop="authored")
add("seed:voxposer", "VoxPoser", "pioneer", C, "direct", "G",
    "LLM 写代码组合 3D 价值图，由 MPC 闭环执行、对扰动鲁棒（编写闭环）；约束编程一支的起点", loop="authored")
add("seed:roco", "RoCo", "pioneer", C, "orchestrator", "G", loop="re-decide")
add("c00013", "Look Before You Leap", "pioneer", C, "orchestrator", "G",
    "GPT-4V 看图规划、执行后依视觉反馈重新规划；多模态通用模型做闭环机器人规划的早期代表（258 引）", loop="re-decide")
add("c00092", "KnowNo", "pioneer", C, "orchestrator", "G", loop="none")
add("c00050", "CoPa", "pioneer", C, "direct", "G",
    "VLM 写出部件级空间约束、由求解器求出位姿；一次求解（开环），约束编程的代表", loop="none")
add("c00035", "MOKA", "pioneer", C, "direct", "G",
    "VLM 在标记过的图像上预测关键点可供性与路点，规划器转成动作；一次求解（开环），约束编程的代表", loop="none")
add("c03370", "ReKep", "pioneer", C, "direct", "G",
    "VLM 写出关键点约束，求解器约 10 Hz 重解、约束破坏时回溯阶段；用户点名的「编写闭环」范例", loop="authored")
add("c01632", "OmniManip", "pioneer", C, "direct", "G",
    "以物体为中心的交互基元作空间约束，在 6D 位姿跟踪下闭环重解（编写闭环）", loop="authored")
add("gap:2410.06237", "BUMBLE", "pioneer", C, "orchestrator", "G", loop="re-decide")
add("c00860", "COME-robot", "pioneer", C, "orchestrator", "G", loop="re-decide")
add("c01563", "AutoRT", "pioneer", C, "orchestrator", "G",
    "VLM 描述场景、LLM 为机器人车队提出任务并按规则筛选，大规模调度真机采数据（1:N，开环）", loop="none")
add("gap:2407.02666", "VLM-PC", "pioneer", C, "orchestrator", "G", loop="re-decide")
add("c00019", "DROC", "pioneer", C, "lifelong", "G", loop="re-decide")
add("c01282", "LM-Nav", "pioneer", C, "orchestrator", "G",
    "LLM 抽取地标、VLM 定位、导航模型执行的真机长程导航；VLN agent 的开环起点", loop="none", theme="vln")
add("c03369", "NavGPT", "pioneer", C, "direct", "G",
    "第一个纯 LLM 的 VLN agent，在 R2R 离散图上逐步推理并决策（离散仿真，正文在边界一节讨论）",
    loop="re-decide", theme="vln")
add("t313", "InstructNav", "pioneer", C, "direct", "G", loop="re-decide", theme="vln")
add("c04543", "Open-Nav", "pioneer", C, "orchestrator", "G",
    "开源 LLM 的零样本 VLN-CE agent，连续环境与真机评测", loop="re-decide", theme="vln")
add("c00093", "REFLECT", "pioneer", S, "-", "G", loop="re-decide")
add("c00163", "DoReMi", "pioneer", S, "-", "G", loop="re-decide")
add("c00305", "Safety Chip", "pioneer", S, "-", "G",
    "LLM 把自然语言安全规范译成 LTL 约束，运行时强制执行；Supervisor 的约束式起点（编写闭环）", loop="authored")
add("c01901", "Code-as-Monitor", "pioneer", S, "-", "G", loop="re-decide")
add("c00212", "SUDD", "pioneer", T, "-", "G",
    "LLM 规划并写成功检查代码，检查失败触发重试，经验证的数据蒸馏成策略；Teacher 的起点（编写闭环）",
    loop="authored")
add("c00306", "Manipulate-Anything", "pioneer", T, "-", "G", loop="re-decide")
add("c08231", "RoboTwin 2.0", "pioneer", T, "-", "G", loop="re-decide")
add("seed:eureka", "Eureka", "pioneer", D, "-", "G", loop="re-decide")
add("c00014", "Text2Reward", "pioneer", D, "-", "G",
    "LLM 一次写出稠密奖励代码，可加人类反馈修改；Designer 的开环起点（218 引）", loop="none")
add("c00855", "GenSim", "pioneer", D, "-", "G",
    "LLM 生成仿真任务与示范代码，扩展训练任务集；任务生成型 Designer 的起点（开环）", loop="none")
add("c00364", "RoboGen", "pioneer", D, "-", "G",
    "LLM 提出任务、生成场景与奖励并分解训练，自动化机器人学习流水线（开环，308 引）", loop="none")
add("c00434", "CurricuLLM", "pioneer", D, "-", "G", loop="re-decide")
add("c00809", "Eurekaverse", "pioneer", D, "-", "G", loop="re-decide")
add("c00791", "DrEureka", "pioneer", D, "-", "G", loop="re-decide", theme="sim2real")
add("c00870", "Video2Policy", "pioneer", D, "-", "G", loop="re-decide", theme="real2sim")
add("c08731", "Articulate AnyMesh", "pioneer", D, "-", "G",
    "VLM 视觉提示分割部件并构建关节，把刚体网格变成可仿真的铰接资产；agentic Real2Sim 的先驱（开环）",
    loop="none", theme="real2sim")
add("c01684", "RoboMorph", "pioneer", V, "-", "G", loop="re-decide")
add("c09484", "VLMgineer", "pioneer", V, "-", "G", loop="re-decide")

TAG = "r3c"
# ---- pioneers added after the 2022-2025 completion sweep (3,003 never-judged + 961 never-screened candidates,
#      Sonnet-verified); balanced across seats, with more 2025 papers (decision 13: pioneers are co-equal)
add("c01022", "SayPlan", "pioneer", C, "orchestrator", "G",
    "LLM 在 3D 场景图上做语义搜索并规划，场景图模拟器的反馈触发迭代重规划；大尺度环境规划的代表（530 引；证据主要在符号层面，"
    "按 rubric 属边界）", loop="re-decide")
add("c00216", "LLM3", "pioneer", C, "orchestrator", "G",
    "LLM 提出符号动作与连续参数，运动规划失败的原因回传给 LLM 再推理；任务与运动规划（TAMP）一支的代表", loop="re-decide")
add("c02956", "ORGANA", "pioneer", C, "orchestrator", "G",
    "LLM 与化学家对话确定实验目标、规划并调度机器人和实验设备，依感知结果调整流程；实验室自动化场景（165 引）",
    loop="re-decide")
add("c01072", "Being-0", "pioneer", C, "orchestrator", "G",
    "基础模型作人形机器人的高层大脑，调用导航与灵巧操作等模块化技能，并依执行反馈调整；人形机器人 agent 的代表（真机）",
    loop="re-decide")
add("c00165", "Prompt a Robot to Walk", "pioneer", C, "direct", "G",
    "LLM 以观测-动作历史为提示，逐步直接输出关节级动作让机器人行走（仿真）；通用模型直接当策略的早期尝试，"
    "与 2026 年 GPT-6 Astra 在 RoboDojo 上的直接控制一脉相承", loop="re-decide")
add("c00301", "AutoTAMP", "pioneer", C, "direct", "G",
    "LLM 把指令译成信号时序逻辑（STL）交给规划器求解，语法和语义检查失败时自动重提示；形式化语言接口的代表（215 引）",
    loop="re-decide")
add("c03000", "TypeFly", "pioneer", C, "direct", "G",
    "LLM 为无人机写小型脚本语言（MiniSpec）程序，程序读取实时感知并带条件与循环执行；空中机器人上的编写闭环",
    loop="authored")
add("c00009", "LRLL", "pioneer", C, "lifelong", "G",
    "LLM 写策略代码并在使用中不断扩充技能库（软记忆、自引导探索、技能抽象），任务越做越复杂；终身技能库的代表",
    loop="re-decide")
add("c00076", "Incremental Humanoid Learning", "pioneer", C, "lifelong", "G",
    "人形机器人在与人的自然对话中，由 LLM 把纠正意见写成改进的行为代码并存入记忆，下次避免同样错误（真机）",
    loop="re-decide")
add("c00533", "ReMEmbR", "pioneer", C, "lifelong", "G",
    "VLM 把长时程的机器人观测写成时空记忆，LLM agent 迭代检索记忆后回答问题或给出导航目标；记忆型 agent 的代表（真机）",
    loop="re-decide")
add("c07101", "RoboMemory", "pioneer", C, "lifelong", "G",
    "统一空间、时间、情景与语义四类记忆的 agent 框架，闭环规划并在交互中持续学习（仿真与真机）", loop="re-decide")
add("c01030", "SayNav", "pioneer", C, "orchestrator", "G",
    "LLM 基于逐步构建的 3D 场景图生成导航的高层计划，随新观测动态重规划（128 引）", loop="re-decide", theme="vln")
add("c08742", "VLMnav", "pioneer", C, "direct", "G",
    "不做感知、规划、控制的分工，VLM 每一步直接选择导航动作，零样本当端到端导航策略；通用 VLM 直接出导航动作",
    loop="re-decide", theme="vln")
add("c00859", "RoboGuard", "pioneer", S, "-", "G",
    "两级护栏：先用推理模型把安全规范落到当前场景，再把 LLM 机器人的计划与时序逻辑约束对照、在线修正；抵御越狱攻击（真机）",
    loop="authored")
add("c00656", "Real-Time Anomaly Detection", "pioneer", S, "-", "G",
    "快慢两级：小模型实时判断观测是否异常，LLM 慢推理选择回退方案并接入安全控制；运行时监控的代表（107 引，开环）",
    loop="none")
add("c08846", "RoboFAC", "pioneer", S, "-", "C",
    "在大规模失败轨迹上微调的 VLM 分析失败原因并给出纠正指令，在真机上纠正 VLA 的执行；Supervisor 中 carrier C 的例子",
    loop="re-decide")
add("c01293", "RobotGPT", "pioneer", T, "-", "G",
    "ChatGPT 生成并在仿真中验证操作代码，用通过验证的执行数据训练更稳定的策略；Teacher 的早期代表（124 引）",
    loop="re-decide")
add("c04904", "HumanoidGen", "pioneer", T, "-", "G",
    "LLM 推理生成双臂灵巧操作的关系约束与任务，自动采集人形机器人示范数据，带检查与回溯", loop="re-decide")
add("c00810", "Agentic Skill Discovery", "pioneer", D, "-", "G",
    "LLM 提出新任务并写奖励，VLM 验证技能是否学会，学会的进入技能库、再据此提出下一个任务（仿真与真机）",
    loop="re-decide")
add("t336", "OMNI-EPIC", "pioneer", D, "-", "G",
    "基础模型按人类的「有趣」标准不断写出新环境与奖励代码，形成开放式课程训练智能体；Designer 的开放式学习一支",
    loop="re-decide", arxiv="2405.15568")
add("c00909", "PDDLLM", "pioneer", V, "-", "G",
    "LLM 结合物理仿真回放，从一条示范中归纳出符号谓词和动作，自动构建 TAMP 的规划域；Developer 构建系统组件的例子",
    loop="re-decide")

# ---- from the third web gap search (2022-2025 pioneers that do not cite the seeds)
add("gap:2412.10137", "CA-Nav", "pioneer", C, "direct", "G",
    "GPT-4 把指令拆成子指令并写成物体 / 位置 / 方向的完成约束，执行中依实时感知检查约束、切换阶段并塑造价值图；"
    "零样本 VLN-CE（含真机）", loop="authored", theme="vln")
add("gap:2506.14763", "RobotSmith", "pioneer", V, "-", "G",
    "提议者与评审者两个 LLM agent 依渲染反馈反复修改工具设计，再在仿真中优化几何与使用轨迹，3D 打印后真机使用；"
    "Developer 设计工具的代表", loop="re-decide")
add("gap:2507.16841", "AquaChat", "pioneer", C, "orchestrator", "G",
    "GPT-4 把用户指令转成水下 ROV 的网箱巡检计划，任务出错时依底层控制反馈重规划（仿真与水池实测）；"
    "水下身体的先驱（2026 年有 AquaCap）", loop="re-decide")

TAG = "r3"
# ============================================================ resources
for i in ("gap:2502.09560", "gap:2410.07166", "c01624", "gap:2506.06677", "c06897", "t279", "c02705", "gap:2609.33807",
          "c03076", "gap:2412.13178", "c01650", "gap:2503.08663", "c02169", "gap:2601.21570"):
    o = OLD[i]
    add(i, o["key"], "resource", o["seat"], o["sub"], o["carrier"])
add("s04733", "Video2World", "resource", D, "-", "-", theme="real2sim",
    why="用户点名：评测 coding agent 能否从具身视频端到端构建可交互仿真（222 个重建实例）；与 Real2Sim 章交叉引用")
add("c00279", "Frontier VLM Agents Study", "resource", C, "-", "-",
    why="七个前沿 VLM agent 在几何、空间与操作任务上的实证研究：它们离机器人通才还有多远")
add("gap:2610.10409", "RobotWorld", "resource", C, "-", "-",
    why="84 个机器人使用任务，覆盖操作、移动操作、足式、驾驶与空中控制，带交互预算与可执行成功检查")
add("gap:2609.20116", "Astra on VLN-CE", "resource", C, "-", "-",
    why="GPT-6-Astra 在零样本 VLN-CE 闭环中的能力评测（R2R-CE 成功率 52%），与 RoboDojo 评测互补")
add("s10690", "MLLM Drone Agents Eval", "resource", C, "-", "-",
    why="评测 MLLM 作为无人机的通用视觉-语言-动作 agent；覆盖空中")

if __name__ == "__main__":
    seen = set()
    for r in rows:
        assert r["id"] not in seen, r["id"]
        seen.add(r["id"])
    with open("data/core/core_selection.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print(len(rows), Counter(r["tier"] for r in rows), Counter((r["tier"], r["theme"]) for r in rows if r["theme"]))
