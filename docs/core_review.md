# 核心表审阅清单

由 `scripts/build_core_table.py` 从 `data/core/core_selection.csv` 生成。要增删或改判，改 selection 文件后重新运行脚本。

## Controller · 编排型（11）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [NovaPlan](https://arxiv.org/abs/2602.20119) | 2026 | Controller | G | 再决策 | 判定池 | 闭环视频-语言规划：VLM 分解子目标、监控执行、失败时重规划，零样本长程真机操作 |
| [Cybo-Waiter](https://arxiv.org/abs/2603.10675) | 2026 | Controller | G | 编写闭环 | 判定池 | 人形全身移动操作：VLM 编译带谓词前置条件与成功条件的子任务，3D 检查驱动推进与恢复；覆盖人形 |
| [RoboClaw](https://arxiv.org/abs/2603.11558) | 2026 | Controller | G | 再决策 | 判定池 | 单 VLM 控制器统一数据采集、策略学习与执行，编排学习型原语并自复位（43 引） |
| [ABot-Claw](https://arxiv.org/abs/2604.10096) | 2026 | Controller | G | 再决策 | 判定池 | 基于 OpenClaw 的具身 agent 调度异构机器人，持久 memory 与 critic 驱动的局部纠正；1:N 拓扑代表 |
| [SpaceMind](https://arxiv.org/abs/2604.14399) | 2026 | Controller | G | 再决策 | 判定池 | 卫星在轨服务：VLM agent 调度技能与 MCP 工具并自我进化，UE5 仿真与物理实验室验证；覆盖太空机器人 |
| [Tool-Aligned VLA Agent](https://arxiv.org/abs/2605.13119) | 2026 | Controller | G | 再决策 | 判定池 | VLM agent 规划并挑选专用 VLA 作为工具，依事件触发的进度反馈与失败重规划；VLA-as-tool 编排的代表 |
| [AerialClaw](https://arxiv.org/abs/2606.12142) | 2026 | Controller | G | 再决策 | 判定池 | LLM agent 调用无人机的硬技能与 Markdown 软技能，依运行反馈迭代；开源空中 agent 框架 |
| [Physical Agency](https://arxiv.org/abs/2607.21725) | 2026 | Controller | G | 再决策 | 判定池 | LLM 编排者规划、调用 VLA 与参数化技能，从观测核验结果后重规划，针对通用机器人的「编排缺口」 |
| [Thea](https://arxiv.org/abs/2608.11246) | 2026 | Controller | G | 再决策 | 判定池 | 把 coding-agent harness 范式迁移到具身：工具化能力 + 场景图上下文；2026 harness 浪潮代表 |
| [Smart-Agriculture Engine](https://arxiv.org/abs/2609.00106) | 2026 | Controller | G | 再决策 | 判定池 | 事件驱动的 LLM agent 经农机、无人机与传感器 API 管理整季大豆种植，真实农场部署；覆盖农业 |
| [AGRO-SUVIDE](https://arxiv.org/abs/2609.34823) | 2026 | Controller | G | 编写闭环 | 判定池 | 手术清创：coding agent 由一次示范构建技能，运行时监控按前后条件组合循环图；覆盖手术机器人 |

## Controller · 直接驱动型（11）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [FAEA](https://arxiv.org/abs/2601.20334) | 2026 | Controller | G | 再决策 | 判定池 | 软件工程 agent 框架不改动直接用于操作（LIBERO 等），robot-use agent 代表 |
| [VLS](https://arxiv.org/abs/2602.03973) | 2026 | Controller | G | 编写闭环 | 判定池 | VLM 写分阶段可微奖励引导冻结策略的采样，执行反馈触发阶段切换并重新查询 VLM（编写闭环） |
| [CaP-X](https://arxiv.org/abs/2603.22435) | 2026 | Controller | G | 再决策 | 判定池 | coding agent 写当下执行的控制代码并依视觉差分反馈修正；CaP 的闭环继承者与评测框架 |
| [Embodiment Meets Environment](https://arxiv.org/abs/2606.28592) | 2026 | Controller | G | 编写闭环 | 判定池 | 约束编程类：LLM 在 3D 动态场景图上合成任务约束，执行时强制满足并重塑照护技能模板（编写闭环）；覆盖照护机器人 |
| [VIA](https://arxiv.org/abs/2607.11119) | 2026 | Controller | G | 再决策 | 判定池 | FM 通过浏览器式 3D 界面像操作软件一样驱动机械臂；接口新颖 |
| [GTA-2](https://arxiv.org/abs/2609.09808) | 2026 | Controller | G | 开环 | 判定池 | 约束编程类：四个角色 VLM 分解任务并写出关键点、轴、控制器组合与参数，控制器零样本执行（一次求解，开环） |
| [Show-Harness](https://arxiv.org/abs/2609.10522) | 2026 | Controller | G | 再决策 | 判定池 | 用户点名：前沿 VLM 输出语义微动作由确定性解释器执行，零样本真机 |
| [Agent as Policy](https://arxiv.org/abs/2609.12541) | 2026 | Controller | G | 再决策 | 判定池 | 通用 agent 写程序、发运动指令并依物理结果修订，直接驱动真机 |
| [AquaCap](https://arxiv.org/abs/2609.23133) | 2026 | Controller | G | 再决策 | 判定池 | 训练无关的水下 agent 写条件感知的计划与控制程序，配失败感知 memory；覆盖水下机器人 |
| [KPI](https://arxiv.org/abs/2609.36151) | 2026 | Controller | G | 编写闭环 | 判定池 | 人形：VLM 写轨迹与「跟踪 / 柔顺 / 保持力」契约，固定内核依接触调整刚度（编写闭环） |
| [OpenRUA](https://arxiv.org/abs/2610.02459) | 2026 | Controller | G | 再决策 | 判定池 | 现成 coding agent 在终端工作区写 ROS 2 代码并当场运行；robot-use agent 本身就是零样本视觉运动策略 |

## Controller · lifelong / memory 型（5）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [PhysMem](https://arxiv.org/abs/2602.20323) | 2026 | Controller | G | 再决策 | 判定池 | VLM 规划者记录经验、提出物理原理假设并用针对性试验验证，测试时 memory 扩展物理推理 |
| [Harness VLA](https://arxiv.org/abs/2607.08448) | 2026 | Controller | G | 再决策 | 判定池 | 用户点名：冻结 VLA 作为工具，agent 重落地与重摆放，memory 跨 episode 学习 |
| [Teach and Grow](https://arxiv.org/abs/2608.17209) | 2026 | Controller | G | 编写闭环 | 判定池 | coding agent 把少量示范变成带物理反馈的闭环技能块，技能库随使用增长 |
| [MessyMem](https://arxiv.org/abs/2609.15976) | 2026 | Controller | G | 再决策 | 判定池 | 持久 3D 场景图 memory 随交互结果更新的移动操作 agent |
| [CaP Great Again](https://arxiv.org/abs/2609.39018) | 2026 | Controller | G | 再决策 | 判定池 | 编程 agent 依执行反馈编写、进化机器人工具，执行 agent 调用；Code as Policies 的 2026 版 |

## Controller · 训练过的 carrier（6）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [Steerable VLA](https://arxiv.org/abs/2602.13193) | 2026 | Controller | H | 再决策 | 判定池 | 学习得到的具身推理者（或提示 VLM）发出子任务、运动与像素指令，驱动协同训练的 VLA（H） |
| [MEM](https://arxiv.org/abs/2603.03596) | 2026 | Controller | I | 再决策 | 判定池 | VLA 输出子任务语言并更新自身文本记忆（多尺度记忆，76 引） |
| [Trace-Conditioned VLA](https://arxiv.org/abs/2604.21924) | 2026 | Controller | H | 再决策 | 判定池 | 任务管理 VLM 以滚动时域被反复调用，输出已完成 / 剩余子任务与视觉轨迹（H） |
| [Sentinel-VLA](https://arxiv.org/abs/2605.01191) | 2026 | Controller | I | 再决策 | 判定池 | 单一 VLA 在规划时和检测到错误时推理，先输出恢复计划再出动作（I） |
| [τ0-VLA](https://arxiv.org/abs/2608.16885) | 2026 | Controller | H | 再决策 | 判定池 | 分层机器人基础模型：高层依执行 memory 生成子任务并由世界模型引导，低层协同训练（H） |
| [Ludi](https://arxiv.org/abs/2608.22035) | 2026 | Controller | C | 再决策 | 判定池 | 微调的 VLM 决策核心配工具循环 harness，处理澄清、纠正与社交互动（C）；覆盖社交机器人 |

## Supervisor（8）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [CycleVLA](https://arxiv.org/abs/2601.02295) | 2026 | Supervisor | G | 再决策 | 判定池 | VLM 预测失败并触发子任务回退与重试，主动自纠正的 VLA 监督 |
| [Contextual Safety Reasoning](https://arxiv.org/abs/2602.19983) | 2026 | Supervisor | G | 编写闭环 | 判定池 | VLM 从图像推断依情境而变的安全规则并落到地图上，运行时约束开放世界机器人（编写闭环） |
| [Agentic Task Graph](https://arxiv.org/abs/2605.11951) | 2026 | Supervisor | G | 编写闭环 | 判定池 | 三个 agent 预先写出任务图、恢复分支与可执行监控，从被动恢复转向预判（编写闭环） |
| [UAV Selective Recovery](https://arxiv.org/abs/2606.14219) | 2026 | Supervisor | G | 再决策 | 判定池 | 无人机任务运行时只在受阻或无进展时调用外部推理者，选择预定义恢复技能；覆盖空中 |
| [Zetta](https://arxiv.org/abs/2608.16590) | 2026 | Supervisor | G | 再决策 | 判定池 | agent 从 rollout 进化代码化的运行时 critic 与恢复技能，经验证门控保留或回滚 |
| [FRAMES](https://arxiv.org/abs/2609.22538) | 2026 | Supervisor | G | 再决策 | 判定池 | 人形机器人多视角技能监测与恢复（×R） |
| [WhenToAsk](https://arxiv.org/abs/2609.21942) | 2026 | Supervisor | G | 再决策 | 判定池 | 失败后在恢复、补充感知和向人求助之间选择；人机对话式恢复 |
| [Future-Anchored Verification](https://arxiv.org/abs/2610.06280) | 2026 | Supervisor | G | 再决策 | 判定池 | 锚点验证器发现偏离 WAM 预测未来的执行，VLM 转为在线恢复指令；WAM 的监督者 |

## Teacher（6）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [GUAVA](https://arxiv.org/abs/2606.18363) | 2026 | Teacher | G→C | 再决策 | 判定池 | 用户点名：前沿 VLM 在 harness 中行动的轨迹蒸馏为 4B agent，同接口 agent→agent 迁移 |
| [EmbodiedSWE](https://arxiv.org/abs/2609.27308) | 2026 | Teacher | G | 再决策 | 判定池 | coding agent 迭代编写调试灵巧操作程序，经验证解扩展为训练示范 |
| [CAPEX](https://arxiv.org/abs/2609.33007) | 2026 | Teacher | G | 再决策 | 判定池 | 基础模型作为自主示范者，依执行经验重规划并自适应调用频率，行为蒸馏为可部署策略 |
| [RHD](https://arxiv.org/abs/2609.33378) | 2026 | Teacher | G | 再决策 | 判定池 | 强 agent 的经验提炼成 playbook 供轻量 agent 使用（in-context 迁移） |
| [SkillWeaver](https://arxiv.org/abs/2609.36171) | 2026 | Teacher | G | 再决策 | 判定池 | VLM agent 调用并参数化 RL 训练的神经交互技能、观察结果后探索，产出的轨迹用于训练 |
| [Frontier Demo Generation](https://arxiv.org/abs/2610.03615) | 2026 | Teacher | G | 再决策 | 判定池 | 前沿模型自主生成示范，累积纠错的上下文示例，训练出快速的学习策略 |

## Designer（6）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [SceneSmith](https://arxiv.org/abs/2602.09153) | 2026 | Designer | G | 再决策 | 判定池 | 设计者、评审与编排三个 VLM agent 迭代搭建可仿真的室内场景，供机器人学习与评测（47 引） |
| [RF-Agent](https://arxiv.org/abs/2602.23876) | 2026 | Designer | G | 再决策 | 判定池 | LLM agent 用蒙特卡洛树搜索迭代写、改奖励代码，以训练结果为反馈 |
| [QD Red-Teaming](https://arxiv.org/abs/2603.12510) | 2026 | Designer | G | 再决策 | 判定池 | VLM 驱动的质量多样性搜索依 VLA 失败生成对抗指令；评测套件型 Designer |
| [RDA](https://arxiv.org/abs/2606.01672) | 2026 | Designer | G | 再决策 | 判定池 | VLM agent 观看轨迹、总结失败模式并迭代修改奖励 |
| [FIND](https://arxiv.org/abs/2609.32069) | 2026 | Designer | G | 再决策 | 判定池 | 真机 agentic RL：VLM 依近期成功率选择练习任务并自评结果 |
| [ROOT](https://arxiv.org/abs/2610.04250) | 2026 | Designer | G | 再决策 | 判定池 | 在奖励程序、策略与 rollout 的持久实验树上搜索奖励，实现用户指定的足式行为 |

## Developer（9）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [HARBOR](https://arxiv.org/abs/2606.08610) | 2026 | Developer | G | 再决策 | 判定池 | 专职 coding agent 搭环境、塑奖励、调超参、训练 RL 策略（Developer|Designer） |
| [RHO](https://arxiv.org/abs/2606.16458) | 2026 | Developer | G | 再决策 | 判定池 | coding agent 依奖励与执行反馈搜索修改多文件策略代码库 |
| [RATs (Playful)](https://arxiv.org/abs/2606.19419) | 2026 | Developer | G | 再决策 | 补漏 | 游玩阶段自提任务、执行、验证并蒸馏成冻结的代码技能库，测试时复用；Developer 的 skill-library 型 |
| [ENPIRE](https://arxiv.org/abs/2606.19980) | 2026 | Developer | G | 再决策 | 判定池 | 用户点名：多个 coding agent 修改策略与训练代码，真机试验决定保留或回滚 |
| [SPINE](https://arxiv.org/abs/2607.13049) | 2026 | Developer | G | 再决策 | 判定池 | 子 agent 建立机器人档案并调试双臂遥操作栈（驱动、接口、控制）；真机系统工程 |
| [ASPIRE](https://arxiv.org/abs/2607.00272) | 2026 | Developer | G | 再决策 | 判定池 | coding agent 编写并精炼控制程序，从执行轨迹诊断失败，验证后入技能库（56 引） |
| [Skill-Harness Evolution](https://arxiv.org/abs/2608.11350) | 2026 | Developer | G | 再决策 | 判定池 | 冻结模型从 rollout 进化技能与上下文代码 harness，只保留带来提升的修改 |
| [Continuum Robot Design](https://arxiv.org/abs/2609.08220) | 2026 | Developer | G | 再决策 | 判定池 | LLM 设计者与评审依物理仿真结果迭代修改腱驱动连续体机器人的设计；硬件侧 Developer |
| [AdaHVLA](https://arxiv.org/abs/2609.29204) | 2026 | Developer | G | 再决策 | 判定池 | 多 agent 分析 / 修订循环依 rollout 证据编辑协调 VLA 的代码 harness |

## Real2Sim / Sim2Real（17）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [Scene2Demo](https://arxiv.org/abs/2602.12065) | 2026 | Teacher | G | 再决策 | 判定池 | 单张真实图像变成仿真场景与任务，反馈 agent 检查 rollout 并自我进化地生成示范 |
| [Vid2Sid](https://arxiv.org/abs/2602.19359) | 2026 | Designer | G | 再决策 | 判定池 | VLM 对比仿真与真实视频、诊断差异并提出物理参数修改，缩小 sim2real 差距 |
| [MotionDisco](https://arxiv.org/abs/2606.06139) | 2026 | Teacher | G | 再决策 | 判定池 | LLM 引导的进化搜索提出交互序列，经轨迹优化细化，为极限人形移动操作生成参考并迁移到真机 |
| [GaP](https://arxiv.org/abs/2607.05369) | 2026 | Developer | G | 再决策 | 判定池 | 多 agent coding harness 把机器人策略写成计算图，在仿真中自学习改进后部署到真机（Graph-as-Policy） |
| [Agentic Real2Sim](https://arxiv.org/abs/2607.19190) | 2026 | Designer | G | 再决策 | 判定池 | VLM agent 从真实录像出发，迭代调用工具构建可仿真的物理孪生；agentic Real2Sim 的代表 |
| [DREAM](https://arxiv.org/abs/2608.29078) | 2026 | Designer | G | 开环 | 判定池 | 部署时 real-to-sim：LLM 在重建的工作区上把指令写成符号目标与成功判据，生成示范微调真机 VLA（一次构建） |
| [Lucida](https://arxiv.org/abs/2608.30821) | 2026 | Designer | G | 再决策 | 判定池 | agentic Real2Sim：VLM 策略经多轮 GUI 操作摆放生成的资产，组合出真实场景的可仿真复本 |
| [SUN](https://arxiv.org/abs/2608.31167) | 2026 | Designer | G | 再决策 | 判定池 | agent 依程序反馈修复带类型的任务程序（目标、谓词、奖励），训练出可迁移到真机的策略 |
| [GPT-6-Astra XLeRobot](https://arxiv.org/abs/2609.31770) | 2026 | Controller | G | 再决策 | 判定池 | GPT-6-Astra 写控制程序驱动 XLeRobot，复用身体知识、经验与技能，并从仿真迁移到真实电梯按钮任务 |
| [CoDimRecon](https://arxiv.org/abs/2609.36024) | 2026 | Designer | G | 再决策 | 判定池 | agentic Real2Sim：agent 会话从多视角 RGB 重建可仿真的刚体、铰接与可变形曲线场景，行为测试暴露差异后针对性修正 |
| [DexAgent](https://arxiv.org/abs/2609.35318) | 2026 | Teacher | G | 再决策 | 判定池 | agent 从人类视频重建仿真、挑选或编写工具，生成灵巧操作数据并迁移到机器人 |
| [F4R](https://arxiv.org/abs/2609.35575) | 2026 | Designer | G | 再决策 | 判定池 | agent 诊断真机失败、把失败场景重建为可交互仿真，在其中修正后重新部署 |
| [Real2Gym](https://arxiv.org/abs/2609.37089) | 2026 | Developer | G | 再决策 | 判定池 | agent 从示范视频重建场景、写阶段代码，依仿真结果诊断修正后把技能带回真机 |
| [SimEX](https://arxiv.org/abs/2609.38982) | 2026 | Developer | G | 再决策 | 判定池 | 用户点名：coding agent 在仿真中迭代机器人工具箱代码，再借少量真机试验同时修正工具箱与仿真器（robotics AutoResearch） |
| [RPG](https://arxiv.org/abs/2610.02204) | 2026 | Developer | G | 再决策 | 判定池 | 用户点名：从数据集重建练习任务，在仿真中诊断失败、写新技能并修改 system prompt，经跨任务评测保留后回到真机 |
| [Skill2Real](https://arxiv.org/abs/2610.02788) | 2026 | Developer | G | 再决策 | 判定池 | Proposer-Verifier-Governor 依仿真结果保留或回滚技能代码，零样本 sim-to-real |
| [EmbodiedSmith](https://arxiv.org/abs/2610.07969) | 2026 | Designer | G | 再决策 | 判定池 | 用户点名：场景生成与任务生成互相编辑的递归自改进飞轮，规模化产出仿真数据与评测环境 |

## VLN 与具身导航（15）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [LM-Nav](https://arxiv.org/abs/2207.04429) | 2022 | Controller | G | 开环 | 判定池 | LLM 抽取地标、VLM 定位、导航模型执行的真机长程导航；VLN agent 的开环起点 |
| [NavGPT](https://arxiv.org/abs/2305.16986) | 2023 | Controller | G | 再决策 | 判定池 | 第一个纯 LLM 的 VLN agent，在 R2R 离散图上逐步推理并决策（离散仿真，正文在边界一节讨论） |
| [InstructNav](https://arxiv.org/abs/2406.04882) | 2024 | Controller | G | 再决策 | 判定池 | 零样本通用指令导航，LLM 反复重规划 Dynamic Chain-of-Navigation；覆盖 nav |
| [One Agent to Guide Them All](https://arxiv.org/abs/2602.15400) | 2026 | Controller | G | 再决策 | 判定池 | MLLM 在可交互的度量世界表示上推理并做反事实检查，统一多种 VLN 任务，仿真与真机 |
| [OnFly](https://arxiv.org/abs/2603.10682) | 2026 | Controller | G | 再决策 | 判定池 | 机载零样本空中 VLN：一个 VLM 生成导航目标，另一个依关键帧监控进度与安全；覆盖无人机 |
| [AgentVLN](https://arxiv.org/abs/2603.17670) | 2026 | Controller | C | 再决策 | 判定池 | 训练过的 VLM 作大脑调用导航技能库，带自我纠错与主动探索（C） |
| [NORM-Nav](https://arxiv.org/abs/2605.16979) | 2026 | Controller | G | 编写闭环 | 判定池 | 约束编程类导航：LLM 把指令解析成结构化行为约束，依实时感知落成代价地图层由规划器执行并在线重规划 |
| [AgenticNav](https://arxiv.org/abs/2606.10577) | 2026 | Controller | G | 再决策 | 判定池 | VLM 在 harness 中调用动作、深度与 memory 工具，带着自己的推理历史选择目标像素；VLN-CE 闭环 |
| [AllDayNav](https://arxiv.org/abs/2606.10927) | 2026 | Designer | G | 再决策 | 判定池 | 真机终身导航 RL：VLM 写 memory 描述、自提任务并检索视觉目标，持续出题 |
| [LocalNav](https://arxiv.org/abs/2606.27871) | 2026 | Teacher | G→C | 再决策 | 判定池 | 前沿 VLM 导航 agent 轨迹蒸馏到端侧 4B VLM；覆盖 nav 的 Teacher |
| [Embodied Agents Take Control](https://arxiv.org/abs/2607.26148) | 2026 | Controller | G | 再决策 | 判定池 | 通用 coding-agent harness 掌管每一步导航动作并自我纠错，零样本可比工业级系统 |
| [HAM-VLN](https://arxiv.org/abs/2607.29600) | 2026 | Controller | G | 再决策 | 判定池 | MLLM 选择下一个路点并写分层 memory（含失败记录），后续调用再读入 |
| [Air-Ground VLN](https://arxiv.org/abs/2609.03483) | 2026 | Controller | G | 再决策 | 判定池 | 无人机与地面车的 VLM 在共享鸟瞰地图上推理并互相下发子目标，空地协同 VLN；×N 拓扑 |
| [RoboFind](https://arxiv.org/abs/2609.20330) | 2026 | Controller | G | 再决策 | 判定池 | 导航、验证、恢复三个 agent 驱动四足为视障用户找物，验证候选并触发恢复 |
| [ASENA](https://arxiv.org/abs/2609.39207) | 2026 | Controller | G | 再决策 | 判定池 | coding agent 写并运行程序、调用导航 VLA 工具、检查结果并修复，经验随任务积累 |

## 先驱（2022–2025）（31）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [ZS-Planners](https://arxiv.org/abs/2201.07207) | 2022 | Controller | G | 开环 | 种子 | LLM 作零样本规划者的起点：把高层指令分解为可执行步骤；开环 |
| [SayCan](https://arxiv.org/abs/2204.01691) | 2022 | Controller | G | 再决策 | 种子 | 奠基作：LLM 与 affordance 组合，逐步在异质 skill 中选择，执行后重新调用；Controller 的起点 |
| [Inner Monologue](https://arxiv.org/abs/2207.05608) | 2022 | Controller | G | 再决策 | 种子 | 奠基作：成功检测与人类反馈回灌提示，典型闭环规划者 |
| [Code as Policies](https://arxiv.org/abs/2209.07753) | 2022 | Controller | G | 编写闭环 | 种子 | 用户认定的奠基作：LLM 写出带感知反馈循环的策略程序（编写闭环）；coding agent 一脉的源头 |
| [ProgPrompt](https://arxiv.org/abs/2209.11302) | 2022 | Controller | G | 编写闭环 | 种子 | 程序化提示生成带断言与恢复动作的任务程序（编写闭环） |
| [PaLM-E](https://arxiv.org/abs/2303.03378) | 2023 | Controller | C | 再决策 | 种子 | 训练过的 carrier（C）奠基作：多模态 LLM 输出计划供低层策略执行；种子论文 |
| [REFLECT](https://arxiv.org/abs/2306.15724) | 2023 | Supervisor | G | 再决策 | 判定池 | 奠基 Supervisor：总结机器人经验解释失败，解释驱动纠正（296 引） |
| [DoReMi](https://arxiv.org/abs/2307.00329) | 2023 | Supervisor | G | 再决策 | 判定池 | LLM 写约束、VLM 持续监测违例并触发恢复与重规划 |
| [KnowNo](https://arxiv.org/abs/2307.01928) | 2023 | Controller | G | 开环 | 判定池 | 不确定时向人求助的起点；人挑选选项替代了模型决策 |
| [RoCo](https://arxiv.org/abs/2307.04738) | 2023 | Controller | G | 再决策 | 种子 | 多机器人对话协商（×N）的代表；种子论文 |
| [VoxPoser](https://arxiv.org/abs/2307.05973) | 2023 | Controller | G | 编写闭环 | 种子 | LLM 写代码组合 3D 价值图，由 MPC 闭环执行、对扰动鲁棒（编写闭环）；约束编程一支的起点 |
| [SUDD](https://arxiv.org/abs/2307.14535) | 2023 | Teacher | G | 编写闭环 | 判定池 | LLM 规划并写成功检查代码，检查失败触发重试，经验证的数据蒸馏成策略；Teacher 的起点（编写闭环） |
| [Eureka](https://arxiv.org/abs/2310.12931) | 2023 | Designer | G | 再决策 | 种子 | 奠基 Designer：LLM 写奖励代码并依 RL 训练统计反思进化 |
| [DROC](https://arxiv.org/abs/2311.10678) | 2023 | Controller | G | 再决策 | 判定池 | 整合在线语言纠正修订计划与技能代码，并蒸馏检索知识（H closure） |
| [MOKA](https://arxiv.org/abs/2403.03174) | 2024 | Controller | G | 开环 | 判定池 | VLM 在标记过的图像上预测关键点可供性与路点，规划器转成动作；一次求解（开环），约束编程的代表 |
| [CoPa](https://arxiv.org/abs/2403.08248) | 2024 | Controller | G | 开环 | 判定池 | VLM 写出部件级空间约束、由求解器求出位姿；一次求解（开环），约束编程的代表 |
| [DrEureka](https://arxiv.org/abs/2406.01967) | 2024 | Designer | G | 再决策 | 判定池 | 奖励 + domain randomization 设计，四足 sim-to-real |
| [ECoT](https://arxiv.org/abs/2407.08693) | 2024 | Controller | I | 开环 | 种子 | 显式推理 VLA 的起点；每步推理但无自身记录 |
| [RoboMorph](https://arxiv.org/abs/2407.08626) | 2024 | Developer | G | 再决策 | 判定池 | LLM 进化机器人形态（硬件），最早的 Developer |
| [ReKep](https://arxiv.org/abs/2409.01652) | 2024 | Controller | G | 编写闭环 | 判定池 | VLM 写出关键点约束，求解器约 10 Hz 重解、约束破坏时回溯阶段；用户点名的「编写闭环」范例 |
| [BUMBLE](https://arxiv.org/abs/2410.06237) | 2024 | Controller | G | 再决策 | 补漏 | VLM 统一感知、粗到细技能与双层 memory，楼宇级长程移动操作，90+ 小时真机评测 |
| [Code-as-Monitor](https://arxiv.org/abs/2412.04455) | 2024 | Supervisor | G | 再决策 | 判定池 | 用户点名：VLM 编写约束监测代码逐帧执行，违例或预测违例时重规划 |
| [OmniManip](https://arxiv.org/abs/2501.03841) | 2025 | Controller | G | 编写闭环 | 判定池 | 以物体为中心的交互基元作空间约束，在 6D 位姿跟踪下闭环重解（编写闭环） |
| [Articulate AnyMesh](https://arxiv.org/abs/2502.02590) | 2025 | Designer | G | 开环 | 判定池 | VLM 视觉提示分割部件并构建关节，把刚体网格变成可仿真的铰接资产；agentic Real2Sim 的先驱（开环） |
| [Video2Policy](https://arxiv.org/abs/2502.09886) | 2025 | Designer | G | 再决策 | 判定池 | 从视频重建仿真任务并依 RL 反馈迭代奖励代码 |
| [Hi Robot](https://arxiv.org/abs/2502.19417) | 2025 | Controller | H | 再决策 | 判定池 | 分层 H 的代表：高层 VLM 输出下一步指令并响应用户反馈，低层协同设计 |
| [π0.5](https://arxiv.org/abs/2504.16054) | 2025 | Controller | I | 开环 | 判定池 | 预测子任务文本再出动作的 VLA；Harness VLA 所包装的底座（2186 引） |
| [OneTwoVLA](https://arxiv.org/abs/2505.11917) | 2025 | Controller | I | 再决策 | 判定池 | 内化 I 的代表：单一 VLA 自适应地决定何时推理、维护历史并从错误恢复 |
| [RoboTwin 2.0](https://arxiv.org/abs/2506.18088) | 2025 | Teacher | G | 再决策 | 判定池 | MLLM 写任务代码并经仿真闭环修正，合成经验证的示范（571 引） |
| [VLMgineer](https://arxiv.org/abs/2507.12644) | 2025 | Developer | G | 再决策 | 判定池 | VLM 协同设计工具与动作并以仿真进化评估；硬件侧 Developer |
| [Gemini Robotics 1.5](https://arxiv.org/abs/2510.03342) | 2025 | Controller | H | 再决策 | 判定池 | 厂商 ER 编排者 + 自家 VLA（协同设计），规划、估计进度并调用工具 |

## Benchmark 与资源（18）

| 短名 | 年份 | Seat | Carrier | 闭环 | 来源 | 入选理由 |
|---|---|---|---|---|---|---|
| [Embodied Agent Interface](https://arxiv.org/abs/2410.07166) | 2024 | Controller | - | – | 补漏 | 把 LLM 具身决策拆成目标解释、子目标分解、动作序列、转移建模四个模块逐项评测 |
| [PARTNR](https://arxiv.org/abs/2411.00081) | 2024 | Controller | - | – | 判定池 | 人机协作规划与推理 benchmark（F1，作为资源收录） |
| [SafeAgentBench](https://arxiv.org/abs/2412.13178) | 2024 | Controller | - | – | 补漏 | 750 个危险/安全任务，测试具身 LLM agent 是否拒绝危险指令 |
| [VLABench](https://arxiv.org/abs/2412.18194) | 2024 | Controller | - | – | 判定池 | 语言条件操作的大规模长程推理 benchmark（228 引） |
| [EmbodiedEval](https://arxiv.org/abs/2501.11858) | 2025 | Controller | - | 再决策 | 判定池 | 交互式评测 MLLM 作为具身 agent（导航、交互、问答） |
| [EmbodiedBench](https://arxiv.org/abs/2502.09560) | 2025 | Controller | - | – | 补漏 | 24 个 MLLM 作为视觉驱动具身 agent 的综合评测，从高层规划到低层操作 |
| [ASIMOV](https://arxiv.org/abs/2503.08663) | 2025 | Supervisor | - | – | 补漏 | 自动生成机器人宪章与语义安全 benchmark |
| [RoboCerebra](https://arxiv.org/abs/2506.06677) | 2025 | Controller | - | – | 补漏 | 评测 VLM 规划者编排 VLA 控制器的长程 benchmark |
| [IS-Bench](https://arxiv.org/abs/2506.16402) | 2025 | Supervisor | - | – | 判定池 | 交互式安全评测：VLM 驱动家务 agent 在过程中是否规避风险 |
| [EmboCoach-Bench](https://arxiv.org/abs/2601.21570) | 2026 | Developer | - | – | 补漏 | 32 个 RL/IL 任务，LLM agent 迭代编写、调试训练代码 |
| [Orchestration Study](https://arxiv.org/abs/2606.10267) | 2026 | Controller | - | – | 判定池 | 对 VLM 规划者 + VLA 分层 agent 的系统性受控研究 |
| [MLLM Drone Agents Eval](https://arxiv.org/abs/2609.01404) | 2026 | Controller | - | 再决策 | 判定池 | 评测 MLLM 作为无人机的通用视觉-语言-动作 agent；覆盖空中 |
| [Astra on RoboDojo](https://arxiv.org/abs/2609.24170) | 2026 | Controller | - | 再决策 | 判定池 | 用户点名：GPT-6 Astra 等 LLM 不经微调直接作为操作策略（LLM as policy），在 RoboDojo 全部 42 个任务上评测 |
| [CodeActionBench](https://arxiv.org/abs/2609.33807) | 2026 | Controller | - | – | 补漏 | agentic Code-as-Policy 的 25 任务 benchmark，含隐藏物理结果 |
| [RLE-Bench](https://arxiv.org/abs/2609.34210) | 2026 | Developer | - | – | 判定池 | coding agent 作为机器人学习工程师的资格考试 |
| [LIBERO-Agent](https://arxiv.org/abs/2609.39507) | 2026 | Controller | - | – | 判定池 | 评测通用 agent 直接发出原生动作指令操作机器人 |
| [Frontier VLM Agents Study](https://arxiv.org/abs/2610.00854) | 2026 | Controller | - | 再决策 | 判定池 | 七个前沿 VLM agent 在几何、空间与操作任务上的实证研究：它们离机器人通才还有多远 |
| [Video2World](https://arxiv.org/abs/2610.04432) | 2026 | Designer | - | 再决策 | 判定池 | 用户点名：评测 coding agent 能否从具身视频端到端构建可交互仿真（222 个重建实例）；与 Real2Sim 章交叉引用 |
