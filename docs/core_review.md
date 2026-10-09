# 核心表审阅清单

由 `scripts/build_core_table.py` 从 `data/core/core_selection.csv` 生成。要增删或改判，改 selection 文件后重新运行脚本。

## Controller · 编排型（10）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [NovaPlan](https://arxiv.org/abs/2602.20119) | 2026 | Controller | G | 再决策 | 判定池 | 闭环视频-语言规划：VLM 分解子目标、监控执行、失败时重规划，零样本长程真机操作 |
| [Cybo-Waiter](https://arxiv.org/abs/2603.10675) | 2026 | Controller | G | 编写闭环 | 判定池 | 人形全身移动操作：VLM 编译带谓词前置条件与成功条件的子任务，3D 检查驱动推进与恢复；覆盖人形 |
| [RoboClaw](https://arxiv.org/abs/2603.11558) | 2026 | Controller | G | 再决策 | 判定池 | 单 VLM 控制器统一数据采集、策略学习与执行，编排学习型原语并自复位（43 引） |
| [ABot-Claw](https://arxiv.org/abs/2604.10096) | 2026 | Controller | G | 再决策 | 判定池 | 基于 OpenClaw 的具身 agent 调度异构机器人，持久 memory 与 critic 驱动的局部纠正；1:N 拓扑代表 |
| [SpaceMind](https://arxiv.org/abs/2604.14399) | 2026 | Controller | G | 再决策 | 判定池 | 卫星在轨服务：VLM agent 调度技能与 MCP 工具并自我进化，UE5 仿真与物理实验室验证；覆盖太空机器人 |
| [AerialClaw](https://arxiv.org/abs/2606.12142) | 2026 | Controller | G | 再决策 | 判定池 | LLM agent 调用无人机的硬技能与 Markdown 软技能，依运行反馈迭代；开源空中 agent 框架 |
| [Physical Agency](https://arxiv.org/abs/2607.21725) | 2026 | Controller | G | 再决策 | 判定池 | LLM 编排者规划、调用 VLA 与参数化技能，从观测核验结果后重规划，针对通用机器人的「编排缺口」 |
| [Thea](https://arxiv.org/abs/2608.11246) | 2026 | Controller | G | 再决策 | 判定池 | 把 coding-agent harness 范式迁移到具身：工具化能力 + 场景图上下文；2026 harness 浪潮代表 |
| [AGRO-SUVIDE](https://arxiv.org/abs/2609.34823) | 2026 | Controller | G | 编写闭环 | 判定池 | 手术清创：coding agent 由一次示范构建技能，运行时监控按前后条件组合循环图；覆盖手术机器人 |
| [Astra Robot Agents](https://arxiv.org/abs/2610.01939) | 2026 | Controller | G | 再决策 | 判定池 | GPT-6 Astra 把原语与 VLA 组合成带检查和重试的 Python 单元，按需请求观测；少用 65% token、成功率高 14% |

## Controller · 直接驱动型（10）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [FAEA](https://arxiv.org/abs/2601.20334) | 2026 | Controller | G | 再决策 | 判定池 | 软件工程 agent 框架不改动直接用于操作（LIBERO 等），robot-use agent 代表 |
| [VLS](https://arxiv.org/abs/2602.03973) | 2026 | Controller | G | 编写闭环 | 判定池 | VLM 写分阶段可微奖励引导冻结策略的采样，执行反馈触发阶段切换并重新查询 VLM（编写闭环） |
| [Embodiment Meets Environment](https://arxiv.org/abs/2606.28592) | 2026 | Controller | G | 编写闭环 | 判定池 | 约束编程类：LLM 在 3D 动态场景图上合成任务约束，执行时强制满足并重塑照护技能模板（编写闭环）；覆盖照护机器人 |
| [VIA](https://arxiv.org/abs/2607.11119) | 2026 | Controller | G | 再决策 | 判定池 | FM 通过浏览器式 3D 界面像操作软件一样驱动机械臂；接口新颖 |
| [GTA-2](https://arxiv.org/abs/2609.09808) | 2026 | Controller | G | 开环 | 判定池 | 约束编程类：四个角色 VLM 分解任务并写出关键点、轴、控制器组合与参数，控制器零样本执行（一次求解，开环） |
| [Show-Harness](https://arxiv.org/abs/2609.10522) | 2026 | Controller | G | 再决策 | 判定池 | 用户点名：前沿 VLM 输出语义微动作由确定性解释器执行，零样本真机 |
| [Agent as Policy](https://arxiv.org/abs/2609.12541) | 2026 | Controller | G | 再决策 | 判定池 | 通用 agent 写程序、发运动指令并依物理结果修订，直接驱动真机 |
| [AquaCap](https://arxiv.org/abs/2609.23133) | 2026 | Controller | G | 再决策 | 判定池 | 训练无关的水下 agent 写条件感知的计划与控制程序，配失败感知 memory；覆盖水下机器人 |
| [KPI](https://arxiv.org/abs/2609.36151) | 2026 | Controller | G | 编写闭环 | 判定池 | 人形：VLM 写轨迹与「跟踪 / 柔顺 / 保持力」契约，固定内核依接触调整刚度（编写闭环） |
| [OpenRUA](https://arxiv.org/abs/2610.02459) | 2026 | Controller | G | 再决策 | 判定池 | 现成 coding agent 在终端工作区写 ROS 2 代码并当场运行；robot-use agent 本身就是零样本视觉运动策略 |

## Controller · lifelong / memory 型（7）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [PhysMem](https://arxiv.org/abs/2602.20323) | 2026 | Controller | G | 再决策 | 判定池 | VLM 规划者记录经验、提出物理原理假设并用针对性试验验证，测试时 memory 扩展物理推理 |
| [Harness VLA](https://arxiv.org/abs/2607.08448) | 2026 | Controller | G | 再决策 | 判定池 | 用户点名：冻结 VLA 作为工具，agent 重落地与重摆放，memory 跨 episode 学习 |
| [Teach and Grow](https://arxiv.org/abs/2608.17209) | 2026 | Controller | G | 编写闭环 | 判定池 | coding agent 把少量示范变成带物理反馈的闭环技能块，技能库随使用增长 |
| [MessyMem](https://arxiv.org/abs/2609.15976) | 2026 | Controller | G | 再决策 | 判定池 | 持久 3D 场景图 memory 随交互结果更新的移动操作 agent |
| [GPT-6-Astra XLeRobot](https://arxiv.org/abs/2609.31770) | 2026 | Controller | G | 再决策 | 判定池 | GPT-6-Astra 写控制程序驱动 XLeRobot，复用身体知识、经验与技能，并从仿真迁移到真实电梯按钮任务 |
| [CaP Great Again](https://arxiv.org/abs/2609.39018) | 2026 | Controller | G | 再决策 | 判定池 | 编程 agent 依执行反馈编写、进化机器人工具，执行 agent 调用；Code as Policies 的 2026 版 |
| [Robo-COP](https://arxiv.org/abs/2610.09228) | 2026 | Controller | G | 再决策 | 补漏 | VLM 编排者在部署中从自己的执行里整理示范、决定何时微调 VLA，只有经验证变好才采用新策略；编排者与策略共同进化 |

## Controller · 训练过的 carrier（0）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|

## Supervisor（7）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [Contextual Safety Reasoning](https://arxiv.org/abs/2602.19983) | 2026 | Supervisor | G | 编写闭环 | 判定池 | VLM 从图像推断依情境而变的安全规则并落到地图上，运行时约束开放世界机器人（编写闭环） |
| [When to Act, Ask, or Learn](https://arxiv.org/abs/2602.22474) | 2026 | Supervisor | G | 再决策 | 判定池 | VLM 验证者在策略的动作样本中挑选，或在不确定时决定澄清、请求人工干预 |
| [Agentic Task Graph](https://arxiv.org/abs/2605.11951) | 2026 | Supervisor | G | 编写闭环 | 判定池 | 三个 agent 预先写出任务图、恢复分支与可执行监控，从被动恢复转向预判（编写闭环） |
| [UAV Selective Recovery](https://arxiv.org/abs/2606.14219) | 2026 | Supervisor | G | 再决策 | 判定池 | 无人机任务运行时只在受阻或无进展时调用外部推理者，选择预定义恢复技能；覆盖空中 |
| [Zetta](https://arxiv.org/abs/2608.16590) | 2026 | Supervisor | G | 再决策 | 判定池 | agent 从 rollout 进化代码化的运行时 critic 与恢复技能，经验证门控保留或回滚 |
| [FRAMES](https://arxiv.org/abs/2609.22538) | 2026 | Supervisor | G | 再决策 | 判定池 | 人形机器人多视角技能监测与恢复（×R） |
| [Beyond Human Demos](https://arxiv.org/abs/2609.24996) | 2026 | Supervisor | G | 编写闭环 | 判定池 | LLM 写可执行的护栏代码，在运行时过滤遥操作与策略发出的危险指令（编写闭环） |

## Teacher（6）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [GUAVA](https://arxiv.org/abs/2606.18363) | 2026 | Teacher | G→C | 再决策 | 判定池 | 用户点名：前沿 VLM 在 harness 中行动的轨迹蒸馏为 4B agent，同接口 agent→agent 迁移 |
| [EmbodiedSWE](https://arxiv.org/abs/2609.27308) | 2026 | Teacher | G | 再决策 | 判定池 | coding agent 迭代编写调试灵巧操作程序，经验证解扩展为训练示范 |
| [CAPEX](https://arxiv.org/abs/2609.33007) | 2026 | Teacher | G | 再决策 | 判定池 | 基础模型作为自主示范者，依执行经验重规划并自适应调用频率，行为蒸馏为可部署策略 |
| [RHD](https://arxiv.org/abs/2609.33378) | 2026 | Teacher | G | 再决策 | 判定池 | 强 agent 的经验提炼成 playbook 供轻量 agent 使用（in-context 迁移） |
| [SkillWeaver](https://arxiv.org/abs/2609.36171) | 2026 | Teacher | G | 再决策 | 判定池 | VLM agent 调用并参数化 RL 训练的神经交互技能、观察结果后探索，产出的轨迹用于训练 |
| [Frontier Demo Generation](https://arxiv.org/abs/2610.03615) | 2026 | Teacher | G | 再决策 | 判定池 | 前沿模型自主生成示范，累积纠错的上下文示例，训练出快速的学习策略 |

## Designer（7）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [SceneSmith](https://arxiv.org/abs/2602.09153) | 2026 | Designer | G | 再决策 | 判定池 | 设计者、评审与编排三个 VLM agent 迭代搭建可仿真的室内场景，供机器人学习与评测（47 引） |
| [SAGE](https://arxiv.org/abs/2602.10116) | 2026 | Designer | G | 再决策 | 判定池 | agent 调用布局与物体生成器和评审，迭代产出可仿真的 3D 场景（56 引） |
| [RF-Agent](https://arxiv.org/abs/2602.23876) | 2026 | Designer | G | 再决策 | 判定池 | LLM agent 用蒙特卡洛树搜索迭代写、改奖励代码，以训练结果为反馈 |
| [RDA](https://arxiv.org/abs/2606.01672) | 2026 | Designer | G | 再决策 | 判定池 | VLM agent 观看轨迹、总结失败模式并迭代修改奖励 |
| [FIND](https://arxiv.org/abs/2609.32069) | 2026 | Designer | G | 再决策 | 判定池 | 真机 agentic RL：VLM 依近期成功率选择练习任务并自评结果 |
| [ROOT](https://arxiv.org/abs/2610.04250) | 2026 | Designer | G | 再决策 | 判定池 | 在奖励程序、策略与 rollout 的持久实验树上搜索奖励，实现用户指定的足式行为 |
| [EmbodiedSmith](https://arxiv.org/abs/2610.07969) | 2026 | Designer | G | 再决策 | 判定池 | 用户点名：场景生成 agent 与任务生成 agent 互相编辑、经仿真验证迭代的生成式仿真（不是 Real2Sim：没有真实数据重建） |

## Developer（12）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [EmboCoach-Bench](https://arxiv.org/abs/2601.21570) | 2026 | Developer | - | 再决策 | 补漏 | 32 个 RL/IL 任务，LLM agent 迭代编写、调试训练代码（stage-2 判为 resource，人工改判 core） |
| [HARBOR](https://arxiv.org/abs/2606.08610) | 2026 | Developer | G | 再决策 | 判定池 | 专职 coding agent 搭环境、塑奖励、调超参、训练 RL 策略（Developer|Designer） |
| [RHO](https://arxiv.org/abs/2606.16458) | 2026 | Developer | G | 再决策 | 判定池 | coding agent 依奖励与执行反馈搜索修改多文件策略代码库 |
| [RATs (Playful)](https://arxiv.org/abs/2606.19419) | 2026 | Developer | G | 再决策 | 补漏 | 游玩阶段自提任务、执行、验证并蒸馏成冻结的代码技能库，测试时复用；Developer 的 skill-library 型 |
| [ENPIRE](https://arxiv.org/abs/2606.19980) | 2026 | Developer | G | 再决策 | 判定池 | 用户点名：多个 coding agent 修改策略与训练代码，真机试验决定保留或回滚 |
| [SPINE](https://arxiv.org/abs/2607.13049) | 2026 | Developer | G | 再决策 | 判定池 | 子 agent 建立机器人档案并调试双臂遥操作栈（驱动、接口、控制）；真机系统工程 |
| [ASPIRE](https://arxiv.org/abs/2607.00272) | 2026 | Developer | G | 再决策 | 判定池 | coding agent 编写并精炼控制程序，从执行轨迹诊断失败，验证后入技能库（56 引） |
| [Skill-Harness Evolution](https://arxiv.org/abs/2608.11350) | 2026 | Developer | G | 再决策 | 判定池 | 冻结模型从 rollout 进化技能与上下文代码 harness，只保留带来提升的修改 |
| [Continuum Robot Design](https://arxiv.org/abs/2609.08220) | 2026 | Developer | G | 再决策 | 判定池 | LLM 设计者与评审依物理仿真结果迭代修改腱驱动连续体机器人的设计；硬件侧 Developer |
| [AdaHVLA](https://arxiv.org/abs/2609.29204) | 2026 | Developer | G | 再决策 | 判定池 | 多 agent 分析 / 修订循环依 rollout 证据编辑协调 VLA 的代码 harness |
| [PhysEvo](https://arxiv.org/abs/2610.08995) | 2026 | Developer | G | 再决策 | 补漏 | 冻结的 GPT-6 Astra 执行任务，meta-agent 依轨迹诊断失败、修改工具与技能并测试后保留；RoboDojo 42 任务，并在真机 PiPER 上继续 |
| [LACE-CRAFT](https://arxiv.org/abs/2610.09283) | 2026 | Developer | G | 再决策 | 补漏 | 反馈、形态、奖励、整合四个 LLM 角色共享实验记录，交叉评审形态-奖励提案，固定任务指标决定保留或回滚；机器人协同设计 |

## Real2Sim / Sim2Real（8）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [Vid2Sid](https://arxiv.org/abs/2602.19359) | 2026 | Designer | G | 再决策 | 判定池 | VLM 对比仿真与真实视频、诊断差异并提出物理参数修改，缩小 sim2real 差距 |
| [Agentic Real2Sim](https://arxiv.org/abs/2607.19190) | 2026 | Designer | G | 再决策 | 判定池 | VLM agent 从真实录像出发，迭代调用工具构建可仿真的物理孪生；agentic Real2Sim 的代表 |
| [CoDimRecon](https://arxiv.org/abs/2609.36024) | 2026 | Designer | G | 再决策 | 判定池 | agentic Real2Sim：agent 会话从多视角 RGB 重建可仿真的刚体、铰接与可变形曲线场景，行为测试暴露差异后针对性修正 |
| [Real2Gym](https://arxiv.org/abs/2609.37089) | 2026 | Developer | G | 再决策 | 判定池 | agent 从示范视频重建场景、写阶段代码，依仿真结果诊断修正后把技能带回真机 |
| [SimEX](https://arxiv.org/abs/2609.38982) | 2026 | Developer | G | 再决策 | 判定池 | 用户点名：coding agent 在仿真中迭代机器人工具箱代码，再借少量真机试验同时修正工具箱与仿真器（robotics AutoResearch） |
| [RPG](https://arxiv.org/abs/2610.02204) | 2026 | Developer | G | 再决策 | 判定池 | 用户点名：从数据集重建练习任务，在仿真中诊断失败、写新技能并修改 system prompt，经跨任务评测保留后回到真机 |
| [Skill2Real](https://arxiv.org/abs/2610.02788) | 2026 | Developer | G | 再决策 | 判定池 | Proposer-Verifier-Governor 依仿真结果保留或回滚技能代码，零样本 sim-to-real |
| [Agentic RSR](https://arxiv.org/abs/2610.10479) | 2026 | Developer | G | 再决策 | 补漏 | agent 从工作区视频恢复尺度、依视觉反馈迭代重建 MuJoCo 场景，coding agent 再开发策略并回到真机；Real2Sim2Real 全链路 |

## VLN 与具身导航（18）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [LM-Nav](https://arxiv.org/abs/2207.04429) | 2022 | Controller | G | 开环 | 判定池 | LLM 抽取地标、VLM 定位、导航模型执行的真机长程导航；VLN agent 的开环起点 |
| [NavGPT](https://arxiv.org/abs/2305.16986) | 2023 | Controller | G | 再决策 | 判定池 | 第一个纯 LLM 的 VLN agent，在 R2R 离散图上逐步推理并决策（离散仿真，正文在边界一节讨论） |
| [SayNav](https://arxiv.org/abs/2309.04077) | 2023 | Controller | G | 再决策 | 判定池 | LLM 基于逐步构建的 3D 场景图生成导航的高层计划，随新观测动态重规划（128 引） |
| [InstructNav](https://arxiv.org/abs/2406.04882) | 2024 | Controller | G | 再决策 | 判定池 | 零样本通用指令导航，LLM 反复重规划 Dynamic Chain-of-Navigation；覆盖 nav |
| [Open-Nav](https://arxiv.org/abs/2409.18794) | 2024 | Controller | G | 再决策 | 判定池 | 开源 LLM 的零样本 VLN-CE agent，连续环境与真机评测 |
| [VLMnav](https://arxiv.org/abs/2411.05755) | 2024 | Controller | G | 再决策 | 判定池 | 不做感知、规划、控制的分工，VLM 每一步直接选择导航动作，零样本当端到端导航策略；通用 VLM 直接出导航动作 |
| [CA-Nav](https://arxiv.org/abs/2412.10137) | 2024 | Controller | G | 编写闭环 | 补漏 | GPT-4 把指令拆成子指令并写成物体 / 位置 / 方向的完成约束，执行中依实时感知检查约束、切换阶段并塑造价值图；零样本 VLN-CE（含真机） |
| [One Agent to Guide Them All](https://arxiv.org/abs/2602.15400) | 2026 | Controller | G | 再决策 | 判定池 | MLLM 在可交互的度量世界表示上推理并做反事实检查，统一多种 VLN 任务，仿真与真机 |
| [OnFly](https://arxiv.org/abs/2603.10682) | 2026 | Controller | G | 再决策 | 判定池 | 机载零样本空中 VLN：一个 VLM 生成导航目标，另一个依关键帧监控进度与安全；覆盖无人机 |
| [HaltNav](https://arxiv.org/abs/2603.12696) | 2026 | Controller | C | 再决策 | 补漏 | MLLM 在轻量拓扑图（osmAG）上把路线拆成子指令，微调的 VLM 在门关闭、拥挤等情况下停止并触发重规划；仿真与真机 Fetch |
| [NORM-Nav](https://arxiv.org/abs/2605.16979) | 2026 | Controller | G | 编写闭环 | 判定池 | 约束编程类导航：LLM 把指令解析成结构化行为约束，依实时感知落成代价地图层由规划器执行并在线重规划 |
| [AgenticNav](https://arxiv.org/abs/2606.10577) | 2026 | Controller | G | 再决策 | 判定池 | VLM 在 harness 中调用动作、深度与 memory 工具，带着自己的推理历史选择目标像素；VLN-CE 闭环 |
| [LocalNav](https://arxiv.org/abs/2606.27871) | 2026 | Teacher | G→C | 再决策 | 判定池 | 前沿 VLM 导航 agent 轨迹蒸馏到端侧 4B VLM；覆盖 nav 的 Teacher |
| [Embodied Agents Take Control](https://arxiv.org/abs/2607.26148) | 2026 | Controller | G | 再决策 | 判定池 | 通用 coding-agent harness 掌管每一步导航动作并自我纠错，零样本可比工业级系统 |
| [HAM-VLN](https://arxiv.org/abs/2607.29600) | 2026 | Controller | G | 再决策 | 判定池 | MLLM 选择下一个路点并写分层 memory（含失败记录），后续调用再读入 |
| [Air-Ground VLN](https://arxiv.org/abs/2609.03483) | 2026 | Controller | G | 再决策 | 判定池 | 无人机与地面车的 VLM 在共享鸟瞰地图上推理并互相下发子目标，空地协同 VLN；×N 拓扑 |
| [HarnessVLN](https://arxiv.org/abs/2609.15195) | 2026 | Controller | G | 再决策 | 判定池 | 训练无关的 MLLM 规划提案经 harness 验证，执行反馈更新 memory 与拓扑图，统一多种导航任务 |
| [ASENA](https://arxiv.org/abs/2609.39207) | 2026 | Controller | G | 再决策 | 判定池 | coding agent 写并运行程序、调用导航 VLA 工具、检查结果并修复，经验随任务积累 |

## 先驱（2022–2025）（59）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [ZS-Planners](https://arxiv.org/abs/2201.07207) | 2022 | Controller | G | 开环 | 种子 | LLM 作零样本规划者的起点：把高层指令分解为可执行步骤；开环 |
| [Socratic Models](https://arxiv.org/abs/2204.00598) | 2022 | Controller | G | 开环 | 种子 | 多个预训练模型用语言组合推理，LLM 规划并调用感知与技能；通用模型组合做具身任务的起点（开环） |
| [SayCan](https://arxiv.org/abs/2204.01691) | 2022 | Controller | G | 再决策 | 种子 | 奠基作：LLM 与 affordance 组合，逐步在异质 skill 中选择，执行后重新调用；Controller 的起点 |
| [Inner Monologue](https://arxiv.org/abs/2207.05608) | 2022 | Controller | G | 再决策 | 种子 | 奠基作：成功检测与人类反馈回灌提示，典型闭环规划者 |
| [Code as Policies](https://arxiv.org/abs/2209.07753) | 2022 | Controller | G | 编写闭环 | 种子 | 用户认定的奠基作：LLM 写出带感知反馈循环的策略程序（编写闭环）；coding agent 一脉的源头 |
| [ProgPrompt](https://arxiv.org/abs/2209.11302) | 2022 | Controller | G | 编写闭环 | 种子 | 程序化提示生成带断言与恢复动作的任务程序（编写闭环） |
| [ChatGPT for Robotics](https://arxiv.org/abs/2306.17582) | 2023 | Controller | G | 编写闭环 | 判定池 | ChatGPT 依提示与人类反馈写机器人代码并迭代修改，覆盖操作、无人机与导航；把通用 LLM 直接用于机器人控制的代表作（755 引） |
| [Text2Motion](https://arxiv.org/abs/2303.12153) | 2023 | Controller | G | 开环 | 判定池 | LLM 生成技能序列并用学习的可行性模型在执行前检查几何可行性；只有预测性检查（开环） |
| [TidyBot](https://arxiv.org/abs/2305.05658) | 2023 | Controller | G | 开环 | 判定池 | LLM 从少量示例归纳用户偏好并给出整理计划，真机移动操作；个性化的早期代表（开环） |
| [AutoTAMP](https://arxiv.org/abs/2306.06531) | 2023 | Controller | G | 再决策 | 判定池 | LLM 把指令译成信号时序逻辑（STL）交给规划器求解，语法和语义检查失败时自动重提示；形式化语言接口的代表（215 引） |
| [Language to Rewards](https://arxiv.org/abs/2306.08647) | 2023 | Controller | G | 编写闭环 | 判定池 | LLM 把指令写成奖励参数，由 MPC 在线优化成动作；约束 / 目标编程一支的早期代表（编写闭环，461 引） |
| [REFLECT](https://arxiv.org/abs/2306.15724) | 2023 | Supervisor | G | 再决策 | 判定池 | 奠基 Supervisor：总结机器人经验解释失败，解释驱动纠正（296 引） |
| [DoReMi](https://arxiv.org/abs/2307.00329) | 2023 | Supervisor | G | 再决策 | 判定池 | LLM 写约束、VLM 持续监测违例并触发恢复与重规划 |
| [KnowNo](https://arxiv.org/abs/2307.01928) | 2023 | Controller | G | 开环 | 判定池 | 不确定时向人求助的起点；人挑选选项替代了模型决策 |
| [RoCo](https://arxiv.org/abs/2307.04738) | 2023 | Controller | G | 再决策 | 种子 | 多机器人对话协商（×N）的代表；种子论文 |
| [SayPlan](https://arxiv.org/abs/2307.06135) | 2023 | Controller | G | 再决策 | 判定池 | LLM 在 3D 场景图上做语义搜索并规划，场景图模拟器的反馈触发迭代重规划；大尺度环境规划的代表（530 引；证据主要在符号层面，按 rubric 属边界） |
| [VoxPoser](https://arxiv.org/abs/2307.05973) | 2023 | Controller | G | 编写闭环 | 种子 | LLM 写代码组合 3D 价值图，由 MPC 闭环执行、对扰动鲁棒（编写闭环）；约束编程一支的起点 |
| [SUDD](https://arxiv.org/abs/2307.14535) | 2023 | Teacher | G | 编写闭环 | 判定池 | LLM 规划并写成功检查代码，检查失败触发重试，经验证的数据蒸馏成策略；Teacher 的起点（编写闭环） |
| [Incremental Humanoid Learning](https://arxiv.org/abs/2309.04316) | 2023 | Controller | G | 再决策 | 判定池 | 人形机器人在与人的自然对话中，由 LLM 把纠正意见写成改进的行为代码并存入记忆，下次避免同样错误（真机） |
| [Prompt a Robot to Walk](https://arxiv.org/abs/2309.09969) | 2023 | Controller | G | 再决策 | 判定池 | LLM 以观测-动作历史为提示，逐步直接输出关节级动作让机器人行走（仿真）；通用模型直接当策略的早期尝试，与 2026 年 GPT-6 Astra 在 RoboDojo 上的直接控制一脉相承 |
| [SMART-LLM](https://arxiv.org/abs/2309.10062) | 2023 | Controller | G | 开环 | 判定池 | LLM 分解任务、组队并分配给多台机器人；多机器人任务规划的早期代表（1:N，开环） |
| [Safety Chip](https://arxiv.org/abs/2309.09919) | 2023 | Supervisor | G | 编写闭环 | 判定池 | LLM 把自然语言安全规范译成 LTL 约束，运行时强制执行；Supervisor 的约束式起点（编写闭环） |
| [Text2Reward](https://arxiv.org/abs/2309.11489) | 2023 | Designer | G | 开环 | 判定池 | LLM 一次写出稠密奖励代码，可加人类反馈修改；Designer 的开环起点（218 引） |
| [GenSim](https://arxiv.org/abs/2310.01361) | 2023 | Designer | G | 开环 | 判定池 | LLM 生成仿真任务与示范代码，扩展训练任务集；任务生成型 Designer 的起点（开环） |
| [Eureka](https://arxiv.org/abs/2310.12931) | 2023 | Designer | G | 再决策 | 种子 | 奠基 Designer：LLM 写奖励代码并依 RL 训练统计反思进化 |
| [RoboGen](https://arxiv.org/abs/2311.01455) | 2023 | Designer | G | 开环 | 判定池 | LLM 提出任务、生成场景与奖励并分解训练，自动化机器人学习流水线（开环，308 引） |
| [DROC](https://arxiv.org/abs/2311.10678) | 2023 | Controller | G | 再决策 | 判定池 | 整合在线语言纠正修订计划与技能代码，并蒸馏检索知识（H closure） |
| [Look Before You Leap](https://arxiv.org/abs/2311.17842) | 2023 | Controller | G | 再决策 | 判定池 | GPT-4V 看图规划、执行后依视觉反馈重新规划；多模态通用模型做闭环机器人规划的早期代表（258 引） |
| [RobotGPT](https://arxiv.org/abs/2312.01421) | 2023 | Teacher | G | 再决策 | 判定池 | ChatGPT 生成并在仿真中验证操作代码，用通过验证的执行数据训练更稳定的策略；Teacher 的早期代表（124 引） |
| [TypeFly](https://arxiv.org/abs/2312.14950) | 2023 | Controller | G | 编写闭环 | 判定池 | LLM 为无人机写小型脚本语言（MiniSpec）程序，程序读取实时感知并带条件与循环执行；空中机器人上的编写闭环 |
| [ORGANA](https://arxiv.org/abs/2401.06949) | 2024 | Controller | G | 再决策 | 判定池 | LLM 与化学家对话确定实验目标、规划并调度机器人和实验设备，依感知结果调整流程；实验室自动化场景（165 引） |
| [AutoRT](https://arxiv.org/abs/2401.12963) | 2024 | Controller | G | 开环 | 判定池 | VLM 描述场景、LLM 为机器人车队提出任务并按规则筛选，大规模调度真机采数据（1:N，开环） |
| [MOKA](https://arxiv.org/abs/2403.03174) | 2024 | Controller | G | 开环 | 判定池 | VLM 在标记过的图像上预测关键点可供性与路点，规划器转成动作；一次求解（开环），约束编程的代表 |
| [CoPa](https://arxiv.org/abs/2403.08248) | 2024 | Controller | G | 开环 | 判定池 | VLM 写出部件级空间约束、由求解器求出位姿；一次求解（开环），约束编程的代表 |
| [LLM3](https://arxiv.org/abs/2403.11552) | 2024 | Controller | G | 再决策 | 判定池 | LLM 提出符号动作与连续参数，运动规划失败的原因回传给 LLM 再推理；任务与运动规划（TAMP）一支的代表 |
| [COME-robot](https://arxiv.org/abs/2404.10220) | 2024 | Controller | G | 再决策 | 判定池 | GPT-4V 闭环开放词表移动操作，执行反馈驱动重规划；覆盖 mobile-manip |
| [Agentic Skill Discovery](https://arxiv.org/abs/2405.15019) | 2024 | Designer | G | 再决策 | 判定池 | LLM 提出新任务并写奖励，VLM 验证技能是否学会，学会的进入技能库、再据此提出下一个任务（仿真与真机） |
| [OMNI-EPIC](https://arxiv.org/abs/2405.15568) | 2024 | Designer | G | 再决策 | 判定池 | 基础模型按人类的「有趣」标准不断写出新环境与奖励代码，形成开放式课程训练智能体；Designer 的开放式学习一支 |
| [DrEureka](https://arxiv.org/abs/2406.01967) | 2024 | Designer | G | 再决策 | 判定池 | 奖励 + domain randomization 设计，四足 sim-to-real |
| [LRLL](https://arxiv.org/abs/2406.18746) | 2024 | Controller | G | 再决策 | 判定池 | LLM 写策略代码并在使用中不断扩充技能库（软记忆、自引导探索、技能抽象），任务越做越复杂；终身技能库的代表 |
| [Manipulate-Anything](https://arxiv.org/abs/2406.18915) | 2024 | Teacher | G | 再决策 | 判定池 | VLM 分解、执行、验证并重规划，经验证轨迹训练行为克隆策略（125 引） |
| [VLM-PC](https://arxiv.org/abs/2407.02666) | 2024 | Controller | G | 再决策 | 补漏 | 足式机器人：VLM 依上下文历史选择并重规划运动技能以应对障碍；覆盖 loco |
| [Real-Time Anomaly Detection](https://arxiv.org/abs/2407.08735) | 2024 | Supervisor | G | 开环 | 判定池 | 快慢两级：小模型实时判断观测是否异常，LLM 慢推理选择回退方案并接入安全控制；运行时监控的代表（107 引，开环） |
| [RoboMorph](https://arxiv.org/abs/2407.08626) | 2024 | Developer | G | 再决策 | 判定池 | LLM 进化机器人形态（硬件），最早的 Developer |
| [ReKep](https://arxiv.org/abs/2409.01652) | 2024 | Controller | G | 编写闭环 | 判定池 | VLM 写出关键点约束，求解器约 10 Hz 重解、约束破坏时回溯阶段；用户点名的「编写闭环」范例 |
| [ReMEmbR](https://arxiv.org/abs/2409.13682) | 2024 | Controller | G | 再决策 | 判定池 | VLM 把长时程的机器人观测写成时空记忆，LLM agent 迭代检索记忆后回答问题或给出导航目标；记忆型 agent 的代表（真机） |
| [CurricuLLM](https://arxiv.org/abs/2409.18382) | 2024 | Designer | G | 再决策 | 判定池 | LLM 生成子任务课程与奖励代码，依策略结果推进 |
| [BUMBLE](https://arxiv.org/abs/2410.06237) | 2024 | Controller | G | 再决策 | 补漏 | VLM 统一感知、粗到细技能与双层 memory，楼宇级长程移动操作，90+ 小时真机评测 |
| [Eurekaverse](https://arxiv.org/abs/2411.01775) | 2024 | Designer | G | 再决策 | 判定池 | LLM 写地形环境代码并依训练结果迭代课程 |
| [Code-as-Monitor](https://arxiv.org/abs/2412.04455) | 2024 | Supervisor | G | 再决策 | 判定池 | 用户点名：VLM 编写约束监测代码逐帧执行，违例或预测违例时重规划 |
| [OmniManip](https://arxiv.org/abs/2501.03841) | 2025 | Controller | G | 编写闭环 | 判定池 | 以物体为中心的交互基元作空间约束，在 6D 位姿跟踪下闭环重解（编写闭环） |
| [Video2Policy](https://arxiv.org/abs/2502.09886) | 2025 | Designer | G | 再决策 | 判定池 | 从视频重建仿真任务并依 RL 反馈迭代奖励代码 |
| [RoboGuard](https://arxiv.org/abs/2503.07885) | 2025 | Supervisor | G | 编写闭环 | 判定池 | 两级护栏：先用推理模型把安全规范落到当前场景，再把 LLM 机器人的计划与时序逻辑约束对照、在线修正；抵御越狱攻击（真机） |
| [Being-0](https://arxiv.org/abs/2503.12533) | 2025 | Controller | G | 再决策 | 判定池 | 基础模型作人形机器人的高层大脑，调用导航与灵巧操作等模块化技能，并依执行反馈调整；人形机器人 agent 的代表（真机） |
| [PDDLLM](https://arxiv.org/abs/2505.18382) | 2025 | Developer | G | 再决策 | 判定池 | LLM 结合物理仿真回放，从一条示范中归纳出符号谓词和动作，自动构建 TAMP 的规划域；Developer 构建系统组件的例子 |
| [RobotSmith](https://arxiv.org/abs/2506.14763) | 2025 | Developer | G | 再决策 | 补漏 | 提议者与评审者两个 LLM agent 依渲染反馈反复修改工具设计，再在仿真中优化几何与使用轨迹，3D 打印后真机使用；Developer 设计工具的代表 |
| [VLMgineer](https://arxiv.org/abs/2507.12644) | 2025 | Developer | G | 再决策 | 判定池 | VLM 协同设计工具与动作并以仿真进化评估；硬件侧 Developer |
| [AquaChat](https://arxiv.org/abs/2507.16841) | 2025 | Controller | G | 再决策 | 补漏 | GPT-4 把用户指令转成水下 ROV 的网箱巡检计划，任务出错时依底层控制反馈重规划（仿真与水池实测）；水下身体的先驱（2026 年有 AquaCap） |
| [RoboMemory](https://arxiv.org/abs/2508.01415) | 2025 | Controller | G | 再决策 | 判定池 | 统一空间、时间、情景与语义四类记忆的 agent 框架，闭环规划并在交互中持续学习（仿真与真机） |

## Benchmark 与资源（20）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [Embodied Agent Interface](https://arxiv.org/abs/2410.07166) | 2024 | Controller | - | – | 补漏 | 把 LLM 具身决策拆成目标解释、子目标分解、动作序列、转移建模四个模块逐项评测 |
| [PARTNR](https://arxiv.org/abs/2411.00081) | 2024 | Controller | - | – | 判定池 | 人机协作规划与推理 benchmark（F1，作为资源收录） |
| [SafeAgentBench](https://arxiv.org/abs/2412.13178) | 2024 | Controller | - | – | 补漏 | 750 个危险/安全任务，测试具身 LLM agent 是否拒绝危险指令 |
| [EmbodiedEval](https://arxiv.org/abs/2501.11858) | 2025 | Controller | - | 再决策 | 判定池 | 交互式评测 MLLM 作为具身 agent（导航、交互、问答） |
| [EmbodiedBench](https://arxiv.org/abs/2502.09560) | 2025 | Controller | - | – | 补漏 | 24 个 MLLM 作为视觉驱动具身 agent 的综合评测，从高层规划到低层操作 |
| [ASIMOV](https://arxiv.org/abs/2503.08663) | 2025 | Supervisor | - | – | 补漏 | 自动生成机器人宪章与语义安全 benchmark |
| [RoboCerebra](https://arxiv.org/abs/2506.06677) | 2025 | Controller | - | – | 补漏 | 评测 VLM 规划者编排 VLA 控制器的长程 benchmark |
| [IS-Bench](https://arxiv.org/abs/2506.16402) | 2025 | Supervisor | - | – | 判定池 | 交互式安全评测：VLM 驱动家务 agent 在过程中是否规避风险 |
| [CaP-X](https://arxiv.org/abs/2603.22435) | 2026 | Controller | G | 再决策 | 判定池 | coding agent 写当下执行的控制代码并依视觉差分反馈修正；CaP 的闭环继承者与评测框架 |
| [Smart-Agriculture Engine](https://arxiv.org/abs/2609.00106) | 2026 | Controller | G | 再决策 | 判定池 | 事件驱动的 LLM agent 经农机、无人机与传感器 API 管理整季大豆种植，真实农场部署；覆盖农业 |
| [MLLM Drone Agents Eval](https://arxiv.org/abs/2609.01404) | 2026 | Controller | - | 再决策 | 判定池 | 评测 MLLM 作为无人机的通用视觉-语言-动作 agent；覆盖空中 |
| [Astra on VLN-CE](https://arxiv.org/abs/2609.20116) | 2026 | Controller | - | 再决策 | 补漏 | GPT-6-Astra 在零样本 VLN-CE 闭环中的能力评测（R2R-CE 成功率 52%），与 RoboDojo 评测互补 |
| [WhenToAsk](https://arxiv.org/abs/2609.21942) | 2026 | Supervisor | G | 再决策 | 判定池 | 失败后在恢复、补充感知和向人求助之间选择；人机对话式恢复 |
| [Astra on RoboDojo](https://arxiv.org/abs/2609.24170) | 2026 | Controller | G | 再决策 | 判定池 | 用户点名：通用 LLM（GPT-6 Astra 等）不经微调直接当操作策略（LLM as policy），在 RoboDojo 全部 42 个任务上评测，排名超过 40 个公开策略 |
| [CodeActionBench](https://arxiv.org/abs/2609.33807) | 2026 | Controller | - | – | 补漏 | agentic Code-as-Policy 的 25 任务 benchmark，含隐藏物理结果 |
| [RLE-Bench](https://arxiv.org/abs/2609.34210) | 2026 | Developer | - | – | 判定池 | coding agent 作为机器人学习工程师的资格考试 |
| [LIBERO-Agent](https://arxiv.org/abs/2609.39507) | 2026 | Controller | - | – | 判定池 | 评测通用 agent 直接发出原生动作指令操作机器人 |
| [Frontier VLM Agents Study](https://arxiv.org/abs/2610.00854) | 2026 | Controller | - | 再决策 | 判定池 | 七个前沿 VLM agent 在几何、空间与操作任务上的实证研究：它们离机器人通才还有多远 |
| [Video2World](https://arxiv.org/abs/2610.04432) | 2026 | Designer | - | 再决策 | 判定池 | 用户点名：评测 coding agent 能否从具身视频端到端构建可交互仿真（222 个重建实例）；与 Real2Sim 章交叉引用 |
| [RobotWorld](https://arxiv.org/abs/2610.10409) | 2026 | Controller | - | 再决策 | 补漏 | 84 个机器人使用任务，覆盖操作、移动操作、足式、驾驶与空中控制，带交互预算与可执行成功检查 |
