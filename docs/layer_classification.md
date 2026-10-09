# 按三层框架给核心表分类

对 `data/core/core_table.csv` 的 174 篇（先驱 70、2026 年 85、资源 19）逐篇按三层框架归类，每篇写了理由。Haiku 逐篇初判（提示词 `screening/prompts/layer_classify.txt`，原始输出 `data/judging_runs/layers/`），之后人工逐条复核；复核改判和边界情况写在「备注」里。机器可读版本：`data/core/layer_classification.csv`（带 BOM，Excel 可直接打开），改分类就改这个 CSV，再运行 `python3 scripts/build_layer_table.py`。

## 三层定义

- **L1**（42 篇）：准备层（pre-execution）：执行之前，为机器人创造或重建环境、设计奖励 / 任务、设计本体与工具、修改系统与训练代码；产物在部署前冻结
- **L2**（101 篇）：中间层（harness）：LLM 不直接出低层动作，隔着一层影响机器人——写出策略代码 / 约束、编排技能或 VLA、把经验迁移 / 蒸馏给策略、在运行时只在异常时介入
- **L3**（7 篇）：执行层（General LLM as policy）：执行过程中由通用大模型自己逐步输出动作（关节、位姿、航点、离散动作或语义微动作）
- **资源**（19 篇）：benchmark、评测研究：不分层，子类写它主要评测哪一层
- **剔除**（5 篇）：不符合框架：决策者主要是专门训练的模型，LLM 作用很弱，主体是数据生成或评测平台，或主题在三层之外

## 总览

| 层 | 子类 | 篇数 | 含义 |
|---|---|---|---|
| L1 | 环境/重建 | 11 | 生成或重建环境、场景、仿真资产、数字孪生（Real2Sim） |
| L1 | 奖励/任务 | 12 | 设计奖励、成功判据、任务与课程 |
| L1 | 本体/工具 | 5 | 设计机器人形态、硬件或工具 |
| L1 | 系统/代码 | 14 | 修改训练代码、策略代码库、技能库或 harness，按试验保留或回滚 |
| L2 | 策略生产者 | 28 | 写出在机器人上运行的策略代码、约束或程序（Code as Policies 一类） |
| L2 | 编排者 | 48 | 规划并调用技能、工具、运动规划器或 VLA |
| L2 | 经验迁移 | 13 | agent 的经验、示范或轨迹被蒸馏成策略或更小的模型 |
| L2 | 运行时监控 | 12 | 运行时只在异常时介入：失败检测、安全护栏、恢复、求助 |
| L3 | 直接动作 | 7 | 通用大模型在执行中直接输出动作 |
| 资源 | 评测L1 | 3 |  |
| 资源 | 评测L2 | 8 |  |
| 资源 | 评测L3 | 4 |  |
| 资源 | 评测多层 | 4 |  |
| 剔除 | — | 5 |  |

## 原 Seat 与三层的对应

不含 19 篇资源；Real2Sim 与 VLN 两章的论文按原 Seat 计入。

| 原 Seat | L1 | L2 | L3 | 剔除 |
|---|---|---|---|---|
| Controller·orchestrator | · | 37 | · | 3 |
| Controller·direct | · | 27 | 7 | · |
| Controller·lifelong | · | 13 | · | · |
| Supervisor | 1 | 13 | · | 1 |
| Teacher | · | 11 | · | 1 |
| Designer | 21 | · | · | · |
| Developer | 20 | · | · | · |

大致对应：Designer、Developer（含 Real2Sim）→ L1；Controller、Supervisor、Teacher → L2；L3 只来自 Controller 的直接驱动型和导航。

## 需要你确认的边界情况

- **Zetta**（L1 · 系统/代码）：兼 L2 运行时监控：产物是运行时 critic 与恢复技能
- **Language to Rewards**（L2 · 策略生产者）：写的是奖励参数，但由 MPC 在执行中在线优化（不是训练前的 reward 设计），故归 L2
- **LRLL**（L2 · 策略生产者）：复核改判（原 L1 系统/代码）：技能库在运行中增长，与 Teach and Grow 一致；兼 L1
- **NORM-Nav**（L2 · 策略生产者）：若 LLM 只做一次指令解析，可剔除
- **ReMEmbR**（L2 · 编排者）：主体是记忆问答，导航只是输出之一
- **AgenticNav**（L2 · 编排者）：边界 L2/L3：每步选目标像素，由 harness 转成运动
- **HaltNav**（L2 · 编排者）：含微调 VLM（停止判断），全局路线由 MLLM 拆分；若严格只收通用模型，可剔除
- **Smart-Agriculture Engine**（L2 · 编排者）：偏基础设施，LLM 作用较弱，可剔除
- **HumanoidGen**（L2 · 经验迁移）：与 RoboTwin 2.0 同类（以数据生成框架为主体），待你决定是否一并剔除
- **NavGPT**（L3 · 直接动作）：边界 L3/L2：离散图上逐步选下一视点（相当于直接移动）；若看作选路点则归 L2
- **Agent as Policy**（L3 · 直接动作）：复核改判（原 L2 策略生产者）：论文主张 agent 本身就是策略；也写程序，兼 L2
- **Astra on RoboDojo**（L3 · 直接动作）：同时是一项评测研究（可放资源）；按其主张归 L3
- **Embodied Agents Take Control**（L3 · 直接动作）：边界 L3/L2：有航点工具的混合版本兼 L2
- **Show-Harness**（L3 · 直接动作）：边界 L3/L2：VLM 逐步出语义微动作，中间只有确定性解释器；若把解释器看作 harness 则归 L2
- **ASIMOV**（资源 · 评测L2）：复核改判（原 剔除）：按规则 benchmark 归资源；对应运行时监控
- **VLABench**（资源 · 评测多层）：主要评测训练好的 VLA；在只收通用模型的口径下可删去
- **LM-Nav**（剔除 · —）：规则 (b)：LLM 只解析一次地标；若把开环先驱都保留，可归 L2 编排者
- **RoboFAC**（剔除 · —）：规则 (a)；若接受为 agent 角色微调的 VLM，可归 L2 运行时监控
- **RoboTwin 2.0**（剔除 · —）：用户指出不算（2026-10-09，原 L2 经验迁移）
- **AgentVLN**（剔除 · —）：复核改判（原 L2 编排者），规则 (a)；若接受微调模型，可归 L2 编排者
- **Ludi**（剔除 · —）：复核改判（原 L2 编排者），规则 (a)；若接受为 agent 角色微调的通用 VLM，可归 L2 编排者

## L1

准备层（pre-execution）：执行之前，为机器人创造或重建环境、设计奖励 / 任务、设计本体与工具、修改系统与训练代码；产物在部署前冻结

### 环境/重建（11）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [Eurekaverse](https://arxiv.org/abs/2411.01775) | 2024（先驱） | Designer | high | LLM 写地形环境代码，依四足训练结果迭代课程，训练前生成环境 |  |
| [OMNI-EPIC](https://arxiv.org/abs/2405.15568) | 2024（先驱） | Designer | med | LLM写仿真环境与奖励/成功检测代码，经兴趣判据筛选后供RL课程训练 |  |
| [Articulate AnyMesh](https://arxiv.org/abs/2502.02590) | 2025（先驱） | Designer·real2sim | high | VLM 以视觉提示分割部件并构建关节，把刚体网格转为仿真铰接资产 |  |
| [Agentic RSR](https://arxiv.org/abs/2610.10479) | 2026 | Developer·real2sim2real | med | LLM代理从视频恢复尺度并迭代重建MuJoCo场景，编码代理另写可执行策略；兼L2 |  |
| [Agentic Real2Sim](https://arxiv.org/abs/2607.19190) | 2026 | Designer·real2sim | high | VLM代理迭代调用工具，从真实录像构建可仿真的物理孪生，供部署前策略微调与评测 |  |
| [CoDimRecon](https://arxiv.org/abs/2609.36024) | 2026 | Designer·real2sim | high | LLM代理从多视角RGB重建可仿真的刚体、铰接与可变形场景，行为测试失配后定向修正 |  |
| [EmbodiedSmith](https://arxiv.org/abs/2610.07969) | 2026 | Designer·real2sim | high | LLM场景与任务生成互相编辑，产出仿真场景与评测环境供部署前训练使用 |  |
| [Real2Gym](https://arxiv.org/abs/2609.37089) | 2026 | Developer·real2sim2real | med | LLM从示范视频重建可交互仿真环境并写阶段代码，技能经仿真诊断后带回真机；兼L2 |  |
| [SAGE](https://arxiv.org/abs/2602.10116) | 2026 | Designer | high | 智能体调用布局与物体生成器，经语义、外观与物理评审迭代生成可仿真3D场景 |  |
| [SceneSmith](https://arxiv.org/abs/2602.09153) | 2026 | Designer | high | 设计、评审与编排三个VLM迭代搭建可仿真室内场景，供机器人学习与评测 |  |
| [Vid2Sid](https://arxiv.org/abs/2602.19359) | 2026 | Designer·real2sim | med | VLM对比仿真与真实视频，提出物理参数修改以校准仿真器，部署前完成 |  |

### 奖励/任务（12）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [Eureka](https://arxiv.org/abs/2310.12931) | 2023（先驱） | Designer | high | LLM 写奖励代码，依 RL 训练统计反思进化，交 RL 训练后部署 |  |
| [GenSim](https://arxiv.org/abs/2310.01361) | 2023（先驱） | Designer | med | LLM 写仿真任务环境与示范代码，训练前生成；兼 L2 |  |
| [RoboGen](https://arxiv.org/abs/2311.01455) | 2023（先驱） | Designer | high | LLM 提出任务并生成场景、奖励与训练监督，训练前自动化生成 |  |
| [Text2Reward](https://arxiv.org/abs/2309.11489) | 2023（先驱） | Designer | high | LLM 一次写出稠密奖励代码，交 RL 训练，可加人类反馈修改 |  |
| [Agentic Skill Discovery](https://arxiv.org/abs/2405.15019) | 2024（先驱） | Designer | high | LLM提出任务并写奖励供RL学技能，VLM判成功后入库，部署前定型 |  |
| [CurricuLLM](https://arxiv.org/abs/2409.18382) | 2024（先驱） | Designer | high | LLM 生成子任务课程与奖励代码，依策略结果推进，交 RL 训练 |  |
| [DrEureka](https://arxiv.org/abs/2406.01967) | 2024（先驱） | Designer·sim2real | high | LLM 写奖励函数与域随机化分布代码，供 sim-to-real 训练 |  |
| [Video2Policy](https://arxiv.org/abs/2502.09886) | 2025（先驱） | Designer·real2sim | high | LLM 写奖励代码迭代 RL，并从视频重建仿真任务，训练前生成 |  |
| [FIND](https://arxiv.org/abs/2609.32069) | 2026 | Designer | med | VLM依近期成功率挑选练习任务并自评结果，为残差强化学习提供任务与奖励信号 |  |
| [RDA](https://arxiv.org/abs/2606.01672) | 2026 | Designer | high | VLM观看轨迹并总结失败模式，迭代修改奖励代码，供RL训练使用 |  |
| [RF-Agent](https://arxiv.org/abs/2602.23876) | 2026 | Designer | high | LLM在蒙特卡洛树搜索中迭代改写奖励代码，以训练结果为反馈，供RL训练使用 |  |
| [ROOT](https://arxiv.org/abs/2610.04250) | 2026 | Designer | high | LLM在持久实验树中改写奖励程序，由视频语言模型提炼行为洞察指导下一轮修改 |  |

### 本体/工具（5）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [RoboMorph](https://arxiv.org/abs/2407.08626) | 2024（先驱） | Developer | high | LLM 生成模块化机器人形态语法，进化搜索并以 RL 评估，输出硬件设计 |  |
| [RobotSmith](https://arxiv.org/abs/2506.14763) | 2025（先驱） | Developer | high | VLM代理迭代提出工具设计，仿真联合优化后3D打印，部署前定型 |  |
| [VLMgineer](https://arxiv.org/abs/2507.12644) | 2025（先驱） | Developer | med | VLM 写代码联合设计工具与动作计划，仿真进化评估后输出工具；兼 L2 |  |
| [Continuum Robot Design](https://arxiv.org/abs/2609.08220) | 2026 | Developer | high | LLM依仿真物理反馈迭代生成连续体机器人结构设计，部署前交RL训练评估 |  |
| [LACE-CRAFT](https://arxiv.org/abs/2610.09283) | 2026 | Developer | high | LLM形态与奖励角色交叉评审成对提案，RL训练后按固定指标保留或回滚 |  |

### 系统/代码（14）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [PDDLLM](https://arxiv.org/abs/2505.18382) | 2025（先驱） | Developer | med | LLM从一条示范归纳PDDL谓词与动作，仿真回放校验后交TAMP规划器，部署前定型 |  |
| [ASPIRE](https://arxiv.org/abs/2607.00272) | 2026 | Developer | low | 编码代理精炼控制程序，验证后的修复入技能库复用（程序亦可归L2） |  |
| [AdaHVLA](https://arxiv.org/abs/2609.29204) | 2026 | Developer | med | 多代理分析与修订循环依rollout证据编辑VLA协调代码harness，保留替代版本 |  |
| [ENPIRE](https://arxiv.org/abs/2606.19980) | 2026 | Developer | high | 多个编码代理修改策略与训练代码，真机试验结果决定保留或回滚 |  |
| [HARBOR](https://arxiv.org/abs/2606.08610) | 2026 | Developer | med | 专职编码代理搭环境、改奖励与超参并训练RL策略，经可执行门控决定保留 |  |
| [PhysEvo](https://arxiv.org/abs/2610.08995) | 2026 | Developer | med | 元智能体依轨迹修改工具与技能并测试保留，产物为部署harness；兼L2 |  |
| [RATs (Playful)](https://arxiv.org/abs/2606.19419) | 2026 | Developer | med | 游玩阶段自提任务、生成并验证代码技能，冻结成技能库供测试时检索复用 |  |
| [RHO](https://arxiv.org/abs/2606.16458) | 2026 | Developer | med | 编码代理训练时搜索多文件策略代码库，依奖励与执行反馈保留改进版本 |  |
| [RPG](https://arxiv.org/abs/2610.02204) | 2026 | Developer·real2sim2real | high | LLM在仿真练习中改写技能库与system prompt，经跨任务评测保留；测试时兼L2 |  |
| [SPINE](https://arxiv.org/abs/2607.13049) | 2026 | Developer | low | 子agent改写驱动与接口配置并验证至遥操作成功；部署前调试，非训练代码 |  |
| [SimEX](https://arxiv.org/abs/2609.38982) | 2026 | Developer·real2sim2real | med | LLM编码代理在仿真中迭代改进机器人工具箱代码，少量真机试验后修正工具箱与仿真器 |  |
| [Skill-Harness Evolution](https://arxiv.org/abs/2608.11350) | 2026 | Developer | high | 冻结模型依目标环境rollout改写技能与上下文代码harness，只保留有提升的修改 |  |
| [Skill2Real](https://arxiv.org/abs/2610.02788) | 2026 | Developer·sim2real | high | LLM提议技能代码修改，仿真证据验证后保留或回滚，冻结技能库迁移真机；兼L2 |  |
| [Zetta](https://arxiv.org/abs/2608.16590) | 2026 | Supervisor | med | rollout后提出代码化运行时critic与恢复技能，经验证门控保留或回滚 | 兼 L2 运行时监控：产物是运行时 critic 与恢复技能 |


## L2

中间层（harness）：LLM 不直接出低层动作，隔着一层影响机器人——写出策略代码 / 约束、编排技能或 VLA、把经验迁移 / 蒸馏给策略、在运行时只在异常时介入

### 策略生产者（28）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [Code as Policies](https://arxiv.org/abs/2209.07753) | 2022（先驱） | Controller·direct | high | LLM 写出带感知反馈循环的 Python 策略程序，直接在机器人上运行 |  |
| [ProgPrompt](https://arxiv.org/abs/2209.11302) | 2022（先驱） | Controller·direct | high | LLM 生成带断言与恢复分支的任务程序，程序直接调用技能执行 |  |
| [AutoTAMP](https://arxiv.org/abs/2306.06531) | 2023（先驱） | Controller·direct | med | LLM 把指令译为 STL 约束交 TAMP 求解，语法语义失败时重提示 |  |
| [ChatGPT for Robotics](https://arxiv.org/abs/2306.17582) | 2023（先驱） | Controller·direct | high | ChatGPT 依提示写机器人代码调用高层函数库，代码直接在机器人上运行 |  |
| [Incremental Humanoid Learning](https://arxiv.org/abs/2309.04316) | 2023（先驱） | Controller·lifelong | med | LLM 在交互控制台逐句生成调用感知与动作的 Python，纠正写入记忆 |  |
| [Language to Rewards](https://arxiv.org/abs/2306.08647) | 2023（先驱） | Controller·direct | med | LLM 写奖励参数，MPC 执行时在线优化为动作，LLM 不逐步出动作 | 写的是奖励参数，但由 MPC 在执行中在线优化（不是训练前的 reward 设计），故归 L2 |
| [SMART-LLM](https://arxiv.org/abs/2309.10062) | 2023（先驱） | Controller·orchestrator | med | LLM 分解任务并分配多机器人，输出可执行 Python 计划代码，开环 |  |
| [TypeFly](https://arxiv.org/abs/2312.14950) | 2023（先驱） | Controller·direct | high | LLM 为无人机写 MiniSpec 小程序，程序读取实时感知并带分支循环执行 |  |
| [VoxPoser](https://arxiv.org/abs/2307.05973) | 2023（先驱） | Controller·direct | high | LLM 写代码组合三维价值图，交 MPC 闭环执行，属约束式策略 |  |
| [CoPa](https://arxiv.org/abs/2403.08248) | 2024（先驱） | Controller·direct | med | VLM 输出部件级空间约束，求解器一次求出末端位姿序列，开环 |  |
| [LRLL](https://arxiv.org/abs/2406.18746) | 2024（先驱） | Controller·lifelong | med | LLM 写调用技能库的策略代码，并在使用中把经验抽象成新技能、不断扩充技能库 | 复核改判（原 L1 系统/代码）：技能库在运行中增长，与 Teach and Grow 一致；兼 L1 |
| [MOKA](https://arxiv.org/abs/2403.03174) | 2024（先驱） | Controller·direct | low | VLM 在标记图上选关键点与路点，规划器转位姿执行，拿不准时保守归L2 |  |
| [ReKep](https://arxiv.org/abs/2409.01652) | 2024（先驱） | Controller·direct | high | VLM 写出关键点约束的 Python 函数，求解器实时求解末端位姿，闭环 |  |
| [OmniManip](https://arxiv.org/abs/2501.03841) | 2025（先驱） | Controller·direct | med | VLM 输出交互基元形式的空间约束，求解器双闭环求位姿 |  |
| [AGRO-SUVIDE](https://arxiv.org/abs/2609.34823) | 2026 | Controller·orchestrator | med | 编码agent据单次示范写出技能代码，运行时组合循环图并按前后条件推进或重试 |  |
| [Agentic Task Graph](https://arxiv.org/abs/2605.11951) | 2026 | Supervisor | med | 执行前写出可编译的任务图与恢复分支，交给运行时执行器与低延迟监控 |  |
| [AquaCap](https://arxiv.org/abs/2609.23133) | 2026 | Controller·direct | high | 双层代理写条件感知计划与可执行控制程序，失败记忆驱动代码修订 |  |
| [Astra Robot Agents](https://arxiv.org/abs/2610.01939) | 2026 | Controller·orchestrator | med | GPT-6 Astra写Python单元串联原语与VLA，含条件检查与局部重试后直接执行 |  |
| [CaP-X](https://arxiv.org/abs/2603.22435) | 2026 | Controller·direct | med | 编码agent写当下执行的控制代码，依视觉差分反馈修正；另有GRPO训练的编码模型 |  |
| [Embodiment Meets Environment](https://arxiv.org/abs/2606.28592) | 2026 | Controller·direct | med | LLM在3D动态场景图上合成任务约束，运行时强制执行并重塑照护技能模板 |  |
| [FAEA](https://arxiv.org/abs/2601.20334) | 2026 | Controller·direct | low | 通用软件agent在仿真中迭代推理驱动操作，输出形式摘要未写明，保守判L2 |  |
| [GPT-6-Astra XLeRobot](https://arxiv.org/abs/2609.31770) | 2026 | Controller·lifelong | med | GPT-6-Astra写控制程序驱动机器人执行，复用身体知识、经验与技能；程序本身即执行策略 |  |
| [GTA-2](https://arxiv.org/abs/2609.09808) | 2026 | Controller·direct | high | 四个VLM分工写关键点、轴、控制器组合与参数，零样本一次生成后开环执行 |  |
| [KPI](https://arxiv.org/abs/2609.36151) | 2026 | Controller·direct | med | VLM写参考轨迹与跟踪/柔顺/保持力契约，固定内核据接触误差实时调刚度 |  |
| [NORM-Nav](https://arxiv.org/abs/2605.16979) | 2026 | Controller·direct·vln | low | LLM逐条把指令解析为结构化约束，编码为代价地图交规划器执行；若只当解析则应剔除 | 若 LLM 只做一次指令解析，可剔除 |
| [OpenRUA](https://arxiv.org/abs/2610.02459) | 2026 | Controller·direct | high | 现成编码agent在ROS 2终端写运动客户端与闭环控制器代码并当场运行 |  |
| [Teach and Grow](https://arxiv.org/abs/2608.17209) | 2026 | Controller·lifelong | med | GPT-6 Astra与Codex把示范归纳为闭环技能块代码，入库后按场景接地执行 |  |
| [VLS](https://arxiv.org/abs/2602.03973) | 2026 | Controller·direct | med | VLM写分阶段可微奖励函数引导冻结扩散策略采样，执行反馈触发阶段切换并重问VLM |  |

### 编排者（48）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [Inner Monologue](https://arxiv.org/abs/2207.05608) | 2022（先驱） | Controller·orchestrator | high | LLM 依成功检测与人类反馈，每步输出下一技能指令，闭环 |  |
| [SayCan](https://arxiv.org/abs/2204.01691) | 2022（先驱） | Controller·orchestrator | high | LLM 按语言与可行性打分选下一技能，执行后依新状态重选 |  |
| [Socratic Models](https://arxiv.org/abs/2204.00598) | 2022（先驱） | Controller·orchestrator | med | LLM 经语言组合感知模型生成步骤并调用技能，开环无反馈 |  |
| [ZS-Planners](https://arxiv.org/abs/2201.07207) | 2022（先驱） | Controller·orchestrator | high | LLM 把指令分解为动作步骤，映射到可执行动作集后交底层执行，开环无反馈 |  |
| [DROC](https://arxiv.org/abs/2311.10678) | 2023（先驱） | Controller·lifelong | med | LLM 依语言纠正修订计划与技能参数，检索记忆，经技能执行 |  |
| [KnowNo](https://arxiv.org/abs/2307.01928) | 2023（先驱） | Controller·orchestrator | high | LLM 对候选技能打分选下一步，共形预测不确定时请人选择 |  |
| [Look Before You Leap](https://arxiv.org/abs/2311.17842) | 2023（先驱） | Controller·orchestrator | high | GPT-4V 看图生成可执行步骤，交技能执行，依视觉反馈重新规划 |  |
| [RoCo](https://arxiv.org/abs/2307.04738) | 2023（先驱） | Controller·orchestrator | med | 多 LLM 智能体对话协商，输出技能级指令，由运动规划器执行，闭环重规划 |  |
| [SayNav](https://arxiv.org/abs/2309.04077) | 2023（先驱） | Controller·orchestrator·vln | high | LLM 基于 3D 场景图输出导航子目标，交预训练底层规划器执行 |  |
| [SayPlan](https://arxiv.org/abs/2307.06135) | 2023（先驱） | Controller·orchestrator | med | LLM 在3D场景图上语义搜索并输出动作序列，路径规划与模拟反馈重规划 |  |
| [Text2Motion](https://arxiv.org/abs/2303.12153) | 2023（先驱） | Controller·orchestrator | high | LLM 生成技能序列，经可行性模型检查后交技能库执行，开环 |  |
| [TidyBot](https://arxiv.org/abs/2305.05658) | 2023（先驱） | Controller·orchestrator | med | LLM 从示例归纳偏好，并为每件物品给出放置位置，交拾放技能执行 |  |
| [BUMBLE](https://arxiv.org/abs/2410.06237) | 2024（先驱） | Controller·orchestrator | high | VLM 依感知与双层记忆选粗到细技能，逐步重规划，楼宇级移动操作 |  |
| [CA-Nav](https://arxiv.org/abs/2412.10137) | 2024（先驱） | Controller·direct·vln | high | GPT-4拆分子指令并维护完成约束、切换阶段，导航计划由价值图生成 |  |
| [COME-robot](https://arxiv.org/abs/2404.10220) | 2024（先驱） | Controller·orchestrator | high | GPT-4V 选探索目标与技能，执行后闭环核验并恢复失败 |  |
| [InstructNav](https://arxiv.org/abs/2406.04882) | 2024（先驱） | Controller·direct·vln | med | LLM 反复重规划导航链，输出子目标交价值图局部规划器执行 |  |
| [LLM3](https://arxiv.org/abs/2403.11552) | 2024（先驱） | Controller·orchestrator | high | LLM 输出符号动作与连续参数交运动规划器执行，失败原因回传迭代 |  |
| [ORGANA](https://arxiv.org/abs/2401.06949) | 2024（先驱） | Controller·orchestrator | high | LLM 与化学家对话定目标，规划并调度机器人与实验设备技能 |  |
| [Open-Nav](https://arxiv.org/abs/2409.18794) | 2024（先驱） | Controller·orchestrator·vln | med | 开源 LLM 从候选路点选子目标，交局部控制器执行，每步重决策 |  |
| [ReMEmbR](https://arxiv.org/abs/2409.13682) | 2024（先驱） | Controller·lifelong | low | LLM 检索时空记忆后输出导航目标交导航栈，主体为记忆问答 | 主体是记忆问答，导航只是输出之一 |
| [VLM-PC](https://arxiv.org/abs/2407.02666) | 2024（先驱） | Controller·orchestrator | high | VLM 依交互历史选运动技能并重规划，足式机器人越障，闭环 |  |
| [AquaChat](https://arxiv.org/abs/2507.16841) | 2025（先驱） | Controller·orchestrator | high | GPT-4把指令转为符号任务计划，中层调用ROV控制序列，失败时据反馈重规划 |  |
| [Being-0](https://arxiv.org/abs/2503.12533) | 2025（先驱） | Controller·orchestrator | high | 基础模型输出任务计划，经 Connector 转为导航与操作技能调用 |  |
| [RoboMemory](https://arxiv.org/abs/2508.01415) | 2025（先驱） | Controller·lifelong | high | VLM 闭环规划器输出高层动作，经 critic 与多类记忆修正，交底层技能 |  |
| [ABot-Claw](https://arxiv.org/abs/2604.10096) | 2026 | Controller·orchestrator | med | OpenClaw式代理按能力调度异构机器人，记忆检索后由critic驱动局部纠正与重规划 |  |
| [ASENA](https://arxiv.org/abs/2609.39207) | 2026 | Controller·lifelong·vln | med | 编码代理写程序调用导航VLA工具并检查修复，跨任务积累笔记与技能；兼L1 |  |
| [AerialClaw](https://arxiv.org/abs/2606.12142) | 2026 | Controller·orchestrator | high | LLM代理调用无人机硬技能与Markdown软技能，依运行反馈闭环更新决策 |  |
| [AgenticNav](https://arxiv.org/abs/2606.10577) | 2026 | Controller·direct·vln | med | VLM每步经动作工具选RGB目标像素，由harness转为运动；工具调用属L2，兼L3 | 边界 L2/L3：每步选目标像素，由 harness 转成运动 |
| [Air-Ground VLN](https://arxiv.org/abs/2609.03483) | 2026 | Controller·orchestrator·vln | med | 无人机与地面车的VLM在共享鸟瞰图上推理，互相下发子目标，几何模块执行 |  |
| [CaP Great Again](https://arxiv.org/abs/2609.39018) | 2026 | Controller·lifelong | med | 执行agent在回路中选择并参数化编程agent写好的工具，修订跨回合保留（兼 L1） |  |
| [Cybo-Waiter](https://arxiv.org/abs/2603.10675) | 2026 | Controller·orchestrator | med | VLM输出带谓词前后条件的JSON子任务序列，交运动原语执行并经3D核验推进 |  |
| [HAM-VLN](https://arxiv.org/abs/2607.29600) | 2026 | Controller·direct·vln | med | MLLM每步选下一路点并同时写分层记忆（含失败记录），路点由底层执行 |  |
| [HaltNav](https://arxiv.org/abs/2603.12696) | 2026 | Controller·orchestrator·vln | med | 微调MLLM大脑把osmAG全局路线拆为子指令，异常时视觉中止并重规划；兼运行时监控 | 含微调 VLM（停止判断），全局路线由 MLLM 拆分；若严格只收通用模型，可剔除 |
| [Harness VLA](https://arxiv.org/abs/2607.08448) | 2026 | Controller·lifelong | med | LLM代理以记忆调度冻结VLA原语与解析原语，据执行轨迹学习各原语操作范围 |  |
| [HarnessVLN](https://arxiv.org/abs/2609.15195) | 2026 | Controller·orchestrator·vln | high | MLLM每步提出子目标，harness校验证据与几何可行性后调度感知、记忆与执行工具 |  |
| [MessyMem](https://arxiv.org/abs/2609.15976) | 2026 | Controller·lifelong | med | VLM规划者读写持久3D场景图记忆，据此调用移动操作技能完成多任务 |  |
| [NovaPlan](https://arxiv.org/abs/2602.20119) | 2026 | Controller·orchestrator | med | VLM拆分子目标并闭环监控、失败时重规划，低层动作由视频关键点几何推算 |  |
| [OnFly](https://arxiv.org/abs/2603.10682) | 2026 | Controller·direct·vln | high | 机载VLM每步输出导航目标交轨迹规划器，另一VLM依关键帧监控进度与安全 |  |
| [One Agent to Guide Them All](https://arxiv.org/abs/2602.15400) | 2026 | Controller·direct·vln | low | MLLM在度量世界表示上推理并做反事实检查后输出导航决策；摘要未说明动作粒度，取保守L2 |  |
| [PhysMem](https://arxiv.org/abs/2602.20323) | 2026 | Controller·lifelong | med | VLM规划者记录经验并做定向试验验证物理假设，验证后据此选择技能执行 |  |
| [Physical Agency](https://arxiv.org/abs/2607.21725) | 2026 | Controller·orchestrator | med | LLM编排者拆分子目标、调用VLA与参数化技能，核验观测结果后重规划 |  |
| [RoboClaw](https://arxiv.org/abs/2603.11558) | 2026 | Controller·orchestrator | med | VLM控制器调用学习到的策略原语完成长程任务，并用EAP自复位循环自主采数 |  |
| [RoboFind](https://arxiv.org/abs/2609.20330) | 2026 | Controller·orchestrator·vln | med | 导航智能体提候选目标，验证智能体比对参考库，协调智能体定恢复与续搜，交四足执行 |  |
| [Smart-Agriculture Engine](https://arxiv.org/abs/2609.00106) | 2026 | Controller·orchestrator | low | LLM代理经API下发农机、无人机与传感器作业，事件驱动流程引擎为主，偏基础设施 | 偏基础设施，LLM 作用较弱，可剔除 |
| [SpaceMind](https://arxiv.org/abs/2604.14399) | 2026 | Controller·orchestrator | med | VLM代理按动态路由调用技能模块与MCP工具，逐步发出工具调用指令 |  |
| [Thea](https://arxiv.org/abs/2608.11246) | 2026 | Controller·orchestrator | high | agent循环调用封装为工具的机器人能力，以场景图作上下文并用退出码判定结果 |  |
| [Tool-Aligned VLA Agent](https://arxiv.org/abs/2605.13119) | 2026 | Controller·orchestrator | high | VLM代理挑选专用VLA工具并下发子任务，依进度反馈事件触发重规划 |  |
| [VIA](https://arxiv.org/abs/2607.11119) | 2026 | Controller·direct | low | FM看截图后在3D网页界面发直观指令驱动机械臂，摘要截断，保守判L2 |  |

### 经验迁移（13）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [RobotGPT](https://arxiv.org/abs/2312.01421) | 2023（先驱） | Teacher | med | ChatGPT 写操作代码并经仿真验证，验证通过的执行数据训练策略 |  |
| [SUDD](https://arxiv.org/abs/2307.14535) | 2023（先驱） | Teacher | high | LLM 规划并写成功检查代码，经验证示范蒸馏为多任务扩散策略 |  |
| [AutoRT](https://arxiv.org/abs/2401.12963) | 2024（先驱） | Controller·orchestrator | med | LLM 提任务指挥机器人队列采数，数据供训练策略，兼 L1 任务设计 |  |
| [Manipulate-Anything](https://arxiv.org/abs/2406.18915) | 2024（先驱） | Teacher | high | VLM 分解任务并执行、验证、重规划，经验证轨迹训练行为克隆策略 |  |
| [HumanoidGen](https://arxiv.org/abs/2507.00833) | 2025（先驱） | Teacher | med | LLM 规划空间约束，采集双臂灵巧操作示范，检查回溯后供策略训练 | 与 RoboTwin 2.0 同类（以数据生成框架为主体），待你决定是否一并剔除 |
| [CAPEX](https://arxiv.org/abs/2609.33007) | 2026 | Teacher | high | 基础模型按执行经验调整观察与重规划频率，产出示范蒸馏为DP与ACT策略 |  |
| [EmbodiedSWE](https://arxiv.org/abs/2609.27308) | 2026 | Teacher | med | 编码代理在仿真中迭代写灵巧操作程序，验证通过的解扩展为示范训练VLA |  |
| [Frontier Demo Generation](https://arxiv.org/abs/2610.03615) | 2026 | Teacher | med | 前沿模型生成含纠错片段的示范训练本地快速策略，部署时把指令交给本地策略执行 |  |
| [GUAVA](https://arxiv.org/abs/2606.18363) | 2026 | Teacher | high | 前沿VLM在harness中输出语义动作，其轨迹蒸馏为4B代理，接口不变 |  |
| [LocalNav](https://arxiv.org/abs/2606.27871) | 2026 | Teacher·vln | high | 前沿VLM导航推理轨迹用于微调端侧4B模型，部署时由小模型逐步决策 |  |
| [RHD](https://arxiv.org/abs/2609.33378) | 2026 | Teacher | med | 强代理把经验提炼为playbook供轻量代理在上下文中使用，依其执行反馈迭代修订 |  |
| [Robo-COP](https://arxiv.org/abs/2610.09228) | 2026 | Controller·lifelong | med | VLM编排者整理自身执行的示范，交给VLA微调，验证变好后才替换策略 |  |
| [SkillWeaver](https://arxiv.org/abs/2609.36171) | 2026 | Teacher | med | VLM在仿真中调用并参数化RL技能、观察结果后继续探索，产出的轨迹用于训练 |  |

### 运行时监控（12）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [DoReMi](https://arxiv.org/abs/2307.00329) | 2023（先驱） | Supervisor | med | LLM 写执行约束，VLM 持续检测违例并触发恢复与重规划，仅异常时介入 |  |
| [REFLECT](https://arxiv.org/abs/2306.15724) | 2023（先驱） | Supervisor | high | 执行失败后 LLM 依经验摘要解释原因，回馈规划器纠正，仅异常时介入 |  |
| [Safety Chip](https://arxiv.org/abs/2309.09919) | 2023（先驱） | Supervisor | med | LLM 把自然语言安全规范译为 LTL 约束，运行时检查并拦截违规动作 |  |
| [Code-as-Monitor](https://arxiv.org/abs/2412.04455) | 2024（先驱） | Supervisor | high | VLM 写约束监测代码逐帧运行，违例或预测违例时触发重规划 |  |
| [Real-Time Anomaly Detection](https://arxiv.org/abs/2407.08735) | 2024（先驱） | Supervisor | med | 快速分类器在 LLM 嵌入上判异常，慢速 LLM 选择回退方案交安全控制 |  |
| [RoboGuard](https://arxiv.org/abs/2503.07885) | 2025（先驱） | Supervisor | high | LLM 生成情境化安全时序逻辑规范，在线对照并修正计划，属安全护栏 |  |
| [Beyond Human Demos](https://arxiv.org/abs/2609.24996) | 2026 | Supervisor | med | LLM写护栏代码，在采集与部署时过滤遥操作和策略指令中的危险动作 |  |
| [Contextual Safety Reasoning](https://arxiv.org/abs/2602.19983) | 2026 | Supervisor | med | VLM从图像推断情境安全规则并落到地图，输出安全集交给CBF实时约束 |  |
| [FRAMES](https://arxiv.org/abs/2609.22538) | 2026 | Supervisor | med | VLM监测代理逐技能判定失败并停止，把证据交给恢复代理，规划代理仍调用技能 |  |
| [UAV Selective Recovery](https://arxiv.org/abs/2606.14219) | 2026 | Supervisor | high | 受阻或无进展时，外部推理者从预定义恢复技能中择一，经校验才影响飞行 |  |
| [When to Act, Ask, or Learn](https://arxiv.org/abs/2602.22474) | 2026 | Supervisor | med | VLM从扩散策略的候选动作中筛选，不确定时改为提问或请求人工干预 |  |
| [WhenToAsk](https://arxiv.org/abs/2609.21942) | 2026 | Supervisor | low | 失败后选择自主恢复、补充感知或发起人机对话，交给恢复层执行；模型未核实 |  |


## L3

执行层（General LLM as policy）：执行过程中由通用大模型自己逐步输出动作（关节、位姿、航点、离散动作或语义微动作）

### 直接动作（7）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [NavGPT](https://arxiv.org/abs/2305.16986) | 2023（先驱） | Controller·direct·vln | med | 每步从候选方向中选下一视点，离散图直接移动，属离散运动步（边界，可保守归L2） | 边界 L3/L2：离散图上逐步选下一视点（相当于直接移动）；若看作选路点则归 L2 |
| [Prompt a Robot to Walk](https://arxiv.org/abs/2309.09969) | 2023（先驱） | Controller·direct | high | LLM 以少样本提示逐步直接输出关节级动作，驱动机器人行走 |  |
| [VLMnav](https://arxiv.org/abs/2411.05755) | 2024（先驱） | Controller·direct·vln | high | VLM 每步直接选择移动或转向动作，零样本作端到端导航策略 |  |
| [Agent as Policy](https://arxiv.org/abs/2609.12541) | 2026 | Controller·direct | med | 通用 agent 在整个执行过程中亲自驱动真机：看视觉证据、下发运动指令、写程序并依物理结果修订 | 复核改判（原 L2 策略生产者）：论文主张 agent 本身就是策略；也写程序，兼 L2 |
| [Astra on RoboDojo](https://arxiv.org/abs/2609.24170) | 2026 | Controller·direct | high | GPT-6 Astra不经微调直接逐步输出动作作操作策略，RoboDojo 42任务评测 | 同时是一项评测研究（可放资源）；按其主张归 L3 |
| [Embodied Agents Take Control](https://arxiv.org/abs/2607.26148) | 2026 | Controller·direct·vln | high | 编码代理每步直接输出离散动作原语控制机器人，无技能层；加航点工具的混合版兼L2 | 边界 L3/L2：有航点工具的混合版本兼 L2 |
| [Show-Harness](https://arxiv.org/abs/2609.10522) | 2026 | Controller·direct | med | VLM逐步输出离散语义微动作，确定性解释器直接落为局部机器人动作 | 边界 L3/L2：VLM 逐步出语义微动作，中间只有确定性解释器；若把解释器看作 harness 则归 L2 |


## 资源

benchmark、评测研究：不分层，子类写它主要评测哪一层

### 评测L1（3）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [EmboCoach-Bench](https://arxiv.org/abs/2601.21570) | 2026 | Developer | high | 评测LLM代理迭代编写、调试RL/IL训练代码与奖励，部署前完成 |  |
| [RLE-Bench](https://arxiv.org/abs/2609.34210) | 2026 | Developer | med | 评测编码代理编写训练代码、harness与机械结构等L1工程产物 |  |
| [Video2World](https://arxiv.org/abs/2610.04432) | 2026 | Designer·real2sim | high | 评测编码代理从具身视频写出仿真环境与机器人行为代码，属环境重建 |  |

### 评测L2（8）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [Embodied Agent Interface](https://arxiv.org/abs/2410.07166) | 2024 | Controller | high | 评测LLM输出目标解释、子目标与高层动作序列等规划模块 |  |
| [PARTNR](https://arxiv.org/abs/2411.00081) | 2024 | Controller | high | 评测LLM规划者调用技能与世界图完成人机协作家务，含错误恢复 |  |
| [SafeAgentBench](https://arxiv.org/abs/2412.13178) | 2024 | Controller | high | 评测LLM规划者以高层动作生成计划，检验是否拒绝危险任务 |  |
| [ASIMOV](https://arxiv.org/abs/2503.08663) | 2025 | Supervisor | med | 语义安全 benchmark：评测基础模型作为机器人大脑时能否判断场景与动作是否安全 | 复核改判（原 剔除）：按规则 benchmark 归资源；对应运行时监控 |
| [IS-Bench](https://arxiv.org/abs/2506.16402) | 2025 | Supervisor | med | 评测VLM代理在家务执行中识别风险，并按序调用缓解技能 |  |
| [RoboCerebra](https://arxiv.org/abs/2506.06677) | 2025 | Controller | high | 评测VLM规划者向VLA控制器分派子任务的规划、反思与记忆能力 |  |
| [CodeActionBench](https://arxiv.org/abs/2609.33807) | 2026 | Controller | high | 评测通用模型写可执行代码作为运行策略并迭代修订，代码即策略 |  |
| [Orchestration Study](https://arxiv.org/abs/2606.10267) | 2026 | Controller | high | 系统研究VLM规划者向VLA控制器分派子目标的分层设计选择 |  |

### 评测L3（4）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [Astra on VLN-CE](https://arxiv.org/abs/2609.20116) | 2026 | Controller | med | 评测GPT-6-Astra每步提出转向与前进等微动作，若为航点则归L2 |  |
| [LIBERO-Agent](https://arxiv.org/abs/2609.39507) | 2026 | Controller | high | 评测通用agent每步直接发出原生机械臂动作指令，无技能层居中 |  |
| [MLLM Drone Agents Eval](https://arxiv.org/abs/2609.01404) | 2026 | Controller | high | 评测MLLM每步直接输出飞行与偏航控制指令，无技能库居中 |  |
| [RobotWorld](https://arxiv.org/abs/2610.10409) | 2026 | Controller | med | 评测通用agent经机器人接口下达位姿等动作指令并完成多类任务 |  |

### 评测多层（4）

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [VLABench](https://arxiv.org/abs/2412.18194) | 2024 | Controller | low | 评测训练好的VLA直出动作与LLM语言能力，VLA为专门训练模型，归属存疑 | 主要评测训练好的 VLA；在只收通用模型的口径下可删去 |
| [EmbodiedBench](https://arxiv.org/abs/2502.09560) | 2025 | Controller | high | 评测24个MLLM从高层规划到低层操作的视觉具身agent表现 |  |
| [EmbodiedEval](https://arxiv.org/abs/2501.11858) | 2025 | Controller | low | 评测MLLM逐步输出导航与交互动作，动作粒度跨层，归属存疑 |  |
| [Frontier VLM Agents Study](https://arxiv.org/abs/2610.00854) | 2026 | Controller | med | 评测7个前沿VLM直接选择动作完成几何、规划与操作等跨层任务 |  |


## 剔除

不符合框架：决策者主要是专门训练的模型，LLM 作用很弱，主体是数据生成或评测平台，或主题在三层之外

| 论文 | 年 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|
| [LM-Nav](https://arxiv.org/abs/2207.04429) | 2022（先驱） | Controller·orchestrator·vln | high | LLM 仅一次解析指令为地标，其余打分与图搜索由代码决定（作用边缘） | 规则 (b)：LLM 只解析一次地标；若把开环先驱都保留，可归 L2 编排者 |
| [RoboFAC](https://arxiv.org/abs/2505.12224) | 2025（先驱） | Supervisor | high | 核心是在失败数据上微调的轻量多模态模型，非通用 LLM/VLM 决策 | 规则 (a)；若接受为 agent 角色微调的 VLM，可归 L2 运行时监控 |
| [RoboTwin 2.0](https://arxiv.org/abs/2506.18088) | 2025（先驱） | Teacher | high | 主体是双臂操作的仿真数据生成器与 benchmark（物体库、域随机化、评测协议），MLLM 写专家代码只是数据流水线中的一环 | 用户指出不算（2026-10-09，原 L2 经验迁移） |
| [AgentVLN](https://arxiv.org/abs/2603.17670) | 2026 | Controller·orchestrator·vln | low | 以训练过的端侧 VLM 作导航大脑并配技能库，主要贡献是这个专门训练的模型与表示映射 | 复核改判（原 L2 编排者），规则 (a)；若接受微调模型，可归 L2 编排者 |
| [Ludi](https://arxiv.org/abs/2608.22035) | 2026 | Controller·orchestrator | med | 决策核心是在多轮交互数据上微调的 VLM，论文主体是这个训练出的模型 | 复核改判（原 L2 编排者），规则 (a)；若接受为 agent 角色微调的通用 VLM，可归 L2 编排者 |

