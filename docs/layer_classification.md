# 按 agent 回路框架重判核心表

![agent 回路框架](agent_loop_framework.png)

框架（2026-10-09）：Agent → Policy / Code / None → Env / Sim；agent 也可以直接作用于 Env / Sim；Env / Sim 的信息回到 agent。箭头表示信息流动，**通用大模型 agent 必须存在，并在其中扮演角色**。

对 `data/core/core_table.csv` 的 174 篇逐篇重判：Haiku 初判（提示词 `screening/prompts/loop_rejudge.txt`，原始输出 `data/judging_runs/loop_rejudge/`），人工逐条复核，改动写在「备注」里。机器可读版本：`data/core/layer_classification.csv`（带 BOM，Excel 可直接打开）；改它后运行 `python3 scripts/build_layer_table.py`。「箭头」一列：A→M agent 写出 / 选择 / 修改中间层，A→E agent 直接作用于环境，M↔E 中间层在环境中运行，E→A 环境信息回到 agent。

## 结果

| 结论 | 篇数 | 含义 |
|---|---|---|
| 保留 | 113 | 通用大模型 agent 存在并起作用，环境信息回到 agent，且 agent 回路是论文的主体 |
| 待定·开环 | 28 | agent 确实起作用（写出计划、程序或约束），但环境信息不回到 agent，图中左侧的箭头缺失；其中包括 Code as Policies、ReKep 这一类和多数开环先驱，保留与否由你决定 |
| 资源 | 20 | 以通用大模型 agent 为对象的 benchmark 或评测研究 |
| 剔除 | 13 | 决策者不是通用大模型，agent 作用太弱，主体是数据生成平台或离线评测，或摘要无法确认决策者 |

保留的论文按三层分：

| 层 | 子类 | 篇数 | 含义 |
|---|---|---|---|
| L1 | 环境/重建 | 10 | 生成或重建环境、场景、仿真资产、数字孪生 |
| L1 | 奖励/任务 | 11 | 设计奖励、成功判据、任务与课程 |
| L1 | 本体/工具 | 5 | 设计机器人形态、硬件或工具 |
| L1 | 系统/代码 | 13 | 修改训练代码、策略代码库、技能库或 harness，按试验保留或回滚 |
| L2 | 策略生产者 | 13 | 写出在机器人上运行的策略代码或约束（Code as Policies 一类） |
| L2 | 编排者 | 38 | 规划并调用技能、工具、运动规划器或 VLA |
| L2 | 经验迁移 | 8 | agent 的经验、示范或轨迹被蒸馏成策略或更小的模型 |
| L2 | 运行时监控 | 9 | 运行时只在异常时介入：失败检测、安全护栏、恢复、求助 |
| L3 | 直接动作 | 6 | 通用大模型在执行中直接输出动作 |

## 需要你决定：图左侧那条 Env/Sim → Agent 的箭头是否必需

下面这些论文里 agent 确实写出了计划、程序或约束，但执行结果不再回到 agent（闭环只在中间层和环境之间，或根本没有闭环）。如果这条箭头必需，它们全部剔除；如果只要求 agent 存在并起作用，它们按「层」一列保留。你之前说过 Code as Policies 属于 L2 的策略生产者、ReKep 这一类都算，这两点和严格读法冲突。

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [Articulate AnyMesh](https://arxiv.org/abs/2502.02590) | 2025（先驱） | - | A→E | Designer·real2sim | med | VLM 一次性分割部件并建关节，无 E→A；主体为资产建模 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [RoboGen](https://arxiv.org/abs/2311.01455) | 2023（先驱） | Code | A→M,A→E,M↔E | Designer | med | 提议-生成-学习单向流水线，无明确 E→A，主体偏数据生成 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [Code as Policies](https://arxiv.org/abs/2209.07753) | 2022（先驱） | Code | A→M,M↔E | Controller·direct | med | LLM 一次写出策略程序，感知反馈在程序内部，LLM 不再被调用，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [ProgPrompt](https://arxiv.org/abs/2209.11302) | 2022（先驱） | Code | A→M,M↔E | Controller·direct | high | LLM 一次生成带断言与恢复动作的程序，执行中不再调用 LLM，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [SMART-LLM](https://arxiv.org/abs/2309.10062) | 2023（先驱） | Code | A→M,M↔E | Controller·orchestrator | med | LLM 一次生成多机器人任务计划代码，执行后不回馈，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [TypeFly](https://arxiv.org/abs/2312.14950) | 2023（先驱） | Code | A→M,M↔E | Controller·direct | med | 无 E→A：LLM 一次写出 MiniSpec 程序，条件分支由程序运行时读感知完成 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [VoxPoser](https://arxiv.org/abs/2307.05973) | 2023（先驱） | Code | A→M,M↔E | Controller·direct | med | LLM 写值图组合代码，MPC 在环内闭环但不再调用 LLM，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [CoPa](https://arxiv.org/abs/2403.08248) | 2024（先驱） | Code | A→M,M↔E | Controller·direct | high | VLM 一次输出部件空间约束，求解后开环执行，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [MOKA](https://arxiv.org/abs/2403.03174) | 2024（先驱） | Policy | A→M,M↔E | Controller·direct | med | VLM 一次预测关键点与路点，规划器转动作后开环执行，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [ReKep](https://arxiv.org/abs/2409.01652) | 2024（先驱） | Code | A→M,M↔E | Controller·direct | high | VLM 一次写出关键点约束，求解器运行时重解，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [OmniManip](https://arxiv.org/abs/2501.03841) | 2025（先驱） | Code | A→M,M↔E | Controller·direct | low | VLM 写空间约束，求解器在位姿跟踪下重解，无 VLM 执行反馈 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [AGRO-SUVIDE](https://arxiv.org/abs/2609.34823) | 2026 | Code | A→M | Controller·orchestrator | med | 无 E→A：编码智能体一次构建技能，运行时由确定性监控模块判断推进或重试 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [Agentic Task Graph](https://arxiv.org/abs/2605.11951) | 2026 | Code | A→M,M↔E | Supervisor | med | 无 E→A：任务图与恢复分支执行前一次写定，运行时只触发不再回调 agent | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [Embodiment Meets Environment](https://arxiv.org/abs/2606.28592) | 2026 | Code | A→M,M↔E | Controller·direct | med | 无 E→A：LLM 合成任务约束，运行时由求解器强制执行，agent 不基于反馈再决策 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [GTA-2](https://arxiv.org/abs/2609.09808) | 2026 | Code | A→M | Controller·direct | med | 无 E→A：多 VLM 一次求解技能与控制器参数，零样本开环执行，执行结果不回传 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [KPI](https://arxiv.org/abs/2609.36151) | 2026 | Code | A→M | Controller·direct | med | 无 E→A：VLM 一次写出轨迹与契约，接触刚度由固定内核自适应，agent 不再决策 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [NORM-Nav](https://arxiv.org/abs/2605.16979) | 2026 | - | A→M | Controller·direct·vln | high | 无 E→A：LLM 仅一次解析指令为约束，之后由规划器执行，不再依结果决策 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [SayCan](https://arxiv.org/abs/2204.01691) | 2022（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | LLM 在异质技能间打分选择、逐步调用；执行结果只进入 affordance 值函数，不回到 LLM（Inner Monologue 才补上反馈） | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需；另：LLM 只给代码列出的技能打分，决策权也偏弱 |
| [Socratic Models](https://arxiv.org/abs/2204.00598) | 2022（先驱） | Policy | A→M,M↔E | Controller·orchestrator | high | 多模型语言组合的开环规划，LLM 一次规划后调用技能，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [ZS-Planners](https://arxiv.org/abs/2201.07207) | 2022（先驱） | None | A→E | Controller·orchestrator | high | LLM 一次生成动作计划后开环执行，执行结果不回馈，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [KnowNo](https://arxiv.org/abs/2307.01928) | 2023（先驱） | Policy | A→M,M↔E | Controller·orchestrator | med | LLM 对代码枚举的选项打分，共形预测不确定时由人替代决策 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需；不确定时由人挑选选项 |
| [Text2Motion](https://arxiv.org/abs/2303.12153) | 2023（先驱） | Policy | A→M,M↔E | Controller·orchestrator | high | LLM 生成技能序列，执行前预测可行性，无 E→A（开环） | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [TidyBot](https://arxiv.org/abs/2305.05658) | 2023（先驱） | Policy | A→M,M↔E | Controller·orchestrator | high | LLM 归纳偏好并一次性决定摆放位置，执行结果不回馈，无 E→A | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [CA-Nav](https://arxiv.org/abs/2412.10137) | 2024（先驱） | Code | A→M,M↔E | Controller·direct·vln | med | 无 E→A：GPT-4 一次拆解指令并写约束，执行中靠感知检查切换子指令 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [RobotGPT](https://arxiv.org/abs/2312.01421) | 2023（先驱） | Code | A→M,M↔E | Teacher | med | 最终由训练策略执行，LLM 仅生成并验证示范代码，不在闭环内 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [SUDD](https://arxiv.org/abs/2307.14535) | 2023（先驱） | Code | A→M,M↔E | Teacher | med | LLM 写计划与成功检查代码，主体为数据生成与策略蒸馏，失败重试不回馈 LLM | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [Real-Time Anomaly Detection](https://arxiv.org/abs/2407.08735) | 2024（先驱） | Policy | A→M,M↔E | Supervisor | med | 异常分类器为专用模型，LLM 仅触发时选回退方案，无 E→A 重决策 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |
| [RoboGuard](https://arxiv.org/abs/2503.07885) | 2025（先驱） | Code | A→M,M↔E | Supervisor | med | 无 E→A：安全规范一次生成，控制综合在线修正计划，LLM 不因结果重决策 | agent 有作用，但环境信息不回到 agent（图中左侧箭头缺失）；保留与否取决于这条箭头是否必需 |

## 保留 · L1（39）

准备层：执行之前，agent 为机器人创造或重建环境、设计奖励 / 任务、设计本体与工具、修改系统与训练代码；反馈是训练或仿真结果

### 环境/重建（10）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [Eurekaverse](https://arxiv.org/abs/2411.01775) | 2024（先驱） | Code | A→M,M↔E,E→A | Designer | med | LLM 写地形环境生成代码，依 RL 训练结果迭代更难的课程 |  |
| [OMNI-EPIC](https://arxiv.org/abs/2405.15568) | 2024（先驱） | Code | A→E,A→M,M↔E,E→A | Designer | med | 基础模型写环境与奖励代码，按归档与有趣性回传生成下一任务，形成开放课程 |  |
| [Agentic RSR](https://arxiv.org/abs/2610.10479) | 2026 | Code | A→E,A→M,M↔E,E→A | Developer·real2sim2real | med | agent 迭代修正 MuJoCo 场景，编码 agent 依仿真执行反馈开发策略后再上真机 |  |
| [Agentic Real2Sim](https://arxiv.org/abs/2607.19190) | 2026 | Code | A→M,M↔E,E→A | Designer·real2sim | med | VLM agent 迭代调用工具从录像重建可仿真孪生，依中间结果修正，环境构建属 L1 |  |
| [CoDimRecon](https://arxiv.org/abs/2609.36024) | 2026 | Code | A→M,M↔E,E→A | Designer·real2sim | med | agent 会话重建可仿真的可变形场景，行为测试暴露失配后针对性修正，闭环成立 |  |
| [EmbodiedSmith](https://arxiv.org/abs/2610.07969) | 2026 | - | A→E,E→A | Designer·real2sim | med | 场景生成与任务生成两个 agent 互相编辑、依结果迭代，产出仿真场景与评测环境 | 复核改判（原 剔除）：你点名的论文，agent 循环正是主体 |
| [Real2Gym](https://arxiv.org/abs/2609.37089) | 2026 | Code | A→M,M↔E,E→A | Developer·real2sim2real | med | agent 在仿真中写阶段代码、观察结果并提炼技能与恢复策略，闭环在仿真内成立 |  |
| [SAGE](https://arxiv.org/abs/2602.10116) | 2026 | None | A→E,E→A | Designer | med | agent 调用布局与物体生成器搭场景，评审物理与语义检查后自我修正 |  |
| [SceneSmith](https://arxiv.org/abs/2602.09153) | 2026 | None | A→E,E→A | Designer | med | 设计者与评审 VLM agent 迭代搭建可仿真室内场景，评审结果回传修改 |  |
| [Vid2Sid](https://arxiv.org/abs/2602.19359) | 2026 | None | A→E,E→A | Designer·real2sim | med | VLM 对比仿真与真实视频、诊断差异并直接修改物理参数，迭代闭环 |  |

### 奖励/任务（11）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [Eureka](https://arxiv.org/abs/2310.12931) | 2023（先驱） | Code | A→M,M↔E,E→A | Designer | high | LLM 写奖励代码，训练统计回传后反思进化，闭环在 agent 内 |  |
| [GenSim](https://arxiv.org/abs/2310.01361) | 2023（先驱） | Code | A→M,A→E,M↔E | Designer | med | LLM 写仿真任务与示范代码，探索模式下从已验证的任务库出发迭代提出新任务 | 复核改判（原 剔除）：属 L1「给机器人创造环境」，任务库验证结果回到 LLM |
| [Text2Reward](https://arxiv.org/abs/2309.11489) | 2023（先驱） | Code | A→M,M↔E,E→A | Designer | med | LLM 写奖励代码，人类反馈回传后迭代修改，回路靠人工触发 |  |
| [Agentic Skill Discovery](https://arxiv.org/abs/2405.15019) | 2024（先驱） | Code | A→M,M↔E,E→A | Designer | high | LLM写奖励函数与任务提案，训练与VLM验证结果回传LLM再提下一任务 |  |
| [CurricuLLM](https://arxiv.org/abs/2409.18382) | 2024（先驱） | Code | A→M,M↔E,E→A | Designer | med | LLM 设计子任务课程与奖励代码，依策略结果推进课程 |  |
| [DrEureka](https://arxiv.org/abs/2406.01967) | 2024（先驱） | Code | A→M,A→E,M↔E,E→A | Designer·sim2real | high | LLM 写奖励与域随机化分布，依训练结果迭代 sim-to-real 配置 |  |
| [Video2Policy](https://arxiv.org/abs/2502.09886) | 2025（先驱） | Code | A→M,A→E,M↔E,E→A | Designer·real2sim | med | 从视频重建仿真任务，LLM 写奖励代码并依 RL 结果迭代 | 复核改判（原 剔除）：奖励迭代有 E→A，属 L1 |
| [FIND](https://arxiv.org/abs/2609.32069) | 2026 | Policy | A→M,M↔E,E→A | Designer | med | VLM 依近期成功率选练习任务并自评结果，驱动真机残差 RL 改进冻结的 VLA |  |
| [RDA](https://arxiv.org/abs/2606.01672) | 2026 | Code | A→M,M↔E,E→A | Designer | high | VLM 观看轨迹、总结失败模式并迭代修改奖励代码，训练反馈回传 |  |
| [RF-Agent](https://arxiv.org/abs/2602.23876) | 2026 | Code | A→M,M↔E,E→A | Designer | high | LLM 语言智能体经 MCTS 迭代改写奖励代码，训练结果回传驱动下一轮 |  |
| [ROOT](https://arxiv.org/abs/2610.04250) | 2026 | Code | A→M,M↔E,E→A | Designer | med | LLM 在持久实验树上搜索奖励程序，依视频观测诊断行为并回传修订 |  |

### 本体/工具（5）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [RoboMorph](https://arxiv.org/abs/2407.08626) | 2024（先驱） | Code | A→M,M↔E,E→A | Developer | med | LLM 以语法生成机器人形态，RL 控制评估结果回传后进化迭代 |  |
| [RobotSmith](https://arxiv.org/abs/2506.14763) | 2025（先驱） | Policy | A→E,M↔E,E→A | Developer | med | VLM 提议者与评审者依渲染反馈迭代设计工具，仿真中联合优化几何与使用轨迹 |  |
| [VLMgineer](https://arxiv.org/abs/2507.12644) | 2025（先驱） | Code | A→M,A→E,M↔E,E→A | Developer | high | VLM 写工具设计与动作代码，仿真评估结果回传后进化协同设计 |  |
| [Continuum Robot Design](https://arxiv.org/abs/2609.08220) | 2026 | Policy | A→E,M↔E,E→A | Developer | med | LLM 设计者依仿真物理状态反馈迭代连续体机器人形态，设计闭环成立 |  |
| [LACE-CRAFT](https://arxiv.org/abs/2610.09283) | 2026 | Code | A→M,A→E,M↔E,E→A | Developer | med | LLM 角色依共享实验记录与回放交叉评审形态与奖励提案，训练结果反馈后再决策 |  |

### 系统/代码（13）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [PDDLLM](https://arxiv.org/abs/2505.18382) | 2025（先驱） | Code | A→M,M↔E | Developer | low | LLM 结合仿真回放从示范归纳规划域，交给运动规划器执行 | 复核改判（原 剔除，low）：仿真回放校验谓词，视为有反馈；仍存疑 |
| [AdaHVLA](https://arxiv.org/abs/2609.29204) | 2026 | Code | A→M,M↔E,E→A | Developer | med | 多 agent 依 rollout 证据修订协调 VLA 的代码 harness，修订图迭代 | 层级复核（Haiku 判 L2）：依 rollout 证据编辑 harness，属 L1 系统/代码 |
| [ENPIRE](https://arxiv.org/abs/2606.19980) | 2026 | Code | A→M,M↔E,E→A | Developer | med | coding agent 依日志修改策略与训练代码，真机结果决定保留或回滚 |  |
| [HARBOR](https://arxiv.org/abs/2606.08610) | 2026 | Code | A→E,A→M,M↔E,E→A | Developer | med | 专职 coding agent 搭环境、写奖励、调参训练 RL，门控与经验回传迭代 |  |
| [PhysEvo](https://arxiv.org/abs/2610.08995) | 2026 | Code | A→M,M↔E,E→A | Developer | high | 冻结通用模型的元智能体依轨迹诊断失败、改写工具与技能，测试后保留并再循环 |  |
| [RATs (Playful)](https://arxiv.org/abs/2606.19419) | 2026 | Code | A→M,M↔E,E→A | Developer | med | 编码 agent 游玩中自提任务、执行验证并蒸馏代码技能库，测试时复用 | 层级复核（Haiku 判 L2）：游玩阶段构建并冻结技能库，测试时复用，属 L1 |
| [RHO](https://arxiv.org/abs/2606.16458) | 2026 | Code | A→M,M↔E,E→A | Developer | high | coding agent 训练期搜索多文件策略仓库，依环境奖励与执行反馈迭代 |  |
| [RPG](https://arxiv.org/abs/2610.02204) | 2026 | Policy | A→M,M↔E,E→A | Developer·real2sim2real | high | LLM 依仿真失败诊断改写技能与系统提示，跨任务评测后保留，循环闭合 |  |
| [SPINE](https://arxiv.org/abs/2607.13049) | 2026 | Code | A→M,M↔E,E→A | Developer | low | 子 agent 调试遥操作栈，诊断、修复、验证迭代并依真机结果再决策，闭环成立 | 层级复核（Haiku 判 L2）：部署前调试遥操作栈，属 L1 系统/代码 |
| [SimEX](https://arxiv.org/abs/2609.38982) | 2026 | Code | A→M,A→E,M↔E,E→A | Developer·real2sim2real | high | 编码 agent 在仿真中迭代机器人工具箱，少量真机试验反馈后同时修正工具箱与仿真器 |  |
| [Skill-Harness Evolution](https://arxiv.org/abs/2608.11350) | 2026 | Code | A→M,M↔E,E→A | Developer | med | 冻结 LLM 依目标环境 rollout 进化技能与代码 harness，仅保留有效修改 | 层级复核（Haiku 判 L2）：依 rollout 改写 harness 只保留提升，属 L1 系统/代码 |
| [Skill2Real](https://arxiv.org/abs/2610.02788) | 2026 | Policy | A→M,M↔E,E→A | Developer·sim2real | high | LLM 依特权仿真证据经 PVG 循环诊断并保留或回滚技能代码，零样本迁移真机 |  |
| [Zetta](https://arxiv.org/abs/2608.16590) | 2026 | Code | A→M,M↔E,E→A | Supervisor | med | agent 在滚动中提出并验证可执行的运行时 critic 与恢复技能，结果回传迭代 | 层级复核（Haiku 判 L2）：依 rollout 改写 critic 与恢复技能并验证后保留，属 L1 系统/代码；兼 L2 运行时监控 |

## 保留 · L2（68）

中间层（harness）：agent 经由中间的 Policy / Code 影响机器人——写出运行的策略代码、调用技能或 VLA、把经验蒸馏给策略、在运行时监控与恢复

### 策略生产者（13）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [AutoTAMP](https://arxiv.org/abs/2306.06531) | 2023（先驱） | Code | A→M,M↔E,E→A | Controller·direct | med | LLM 将指令译为时序逻辑约束交规划器，检查失败时回传重新翻译 |  |
| [ChatGPT for Robotics](https://arxiv.org/abs/2306.17582) | 2023（先驱） | Code | A→M,M↔E,E→A | Controller·direct | med | ChatGPT 写机器人代码并依执行与人反馈迭代修正，闭环在对话中 |  |
| [Incremental Humanoid Learning](https://arxiv.org/abs/2309.04316) | 2023（先驱） | Code | A→M,M↔E,E→A | Controller·lifelong | high | LLM 在交互控制台生成 Python 语句调用感知与动作，人类纠正回传后写入记忆 |  |
| [Language to Rewards](https://arxiv.org/abs/2306.08647) | 2023（先驱） | Code | A→M,M↔E,E→A | Controller·direct | med | LLM 写奖励参数，仿真结果与人反馈回流后迭代修订奖励 | 层级复核（Haiku 判 L1）：奖励参数由 MPC 在执行中在线优化，不是训练前的 reward 设计 |
| [LRLL](https://arxiv.org/abs/2406.18746) | 2024（先驱） | Code | A→M,M↔E,E→A | Controller·lifelong | med | LLM 写策略代码并扩充技能库，仿真探索与经验蒸馏回传，技能库终身增长 |  |
| [ASPIRE](https://arxiv.org/abs/2607.00272) | 2026 | Code | A→M,M↔E,E→A | Developer | high | coding agent 写控制程序，依执行轨迹诊断修复并验证后入技能库 |  |
| [AquaCap](https://arxiv.org/abs/2609.23133) | 2026 | Code | A→M,M↔E,E→A | Controller·direct | high | 双层 agent 生成控制程序，失败感知 memory 诊断后闭环重规划并改写代码 |  |
| [Astra Robot Agents](https://arxiv.org/abs/2610.01939) | 2026 | Code | A→M,M↔E,E→A | Controller·orchestrator | high | GPT-6 Astra 编写调用原语与 VLA 的代码单元，执行反馈回传后再规划 |  |
| [CaP-X](https://arxiv.org/abs/2603.22435) | 2026 | Code | A→M,M↔E,E→A | Controller·direct | low | 通用编码 agent 写控制代码并依视觉差分反馈修订；另含基准与 GRPO 训练，主体存疑 |  |
| [GPT-6-Astra XLeRobot](https://arxiv.org/abs/2609.31770) | 2026 | Code | A→M,M↔E,E→A | Controller·lifelong | med | GPT-6-Astra 写控制程序驱动机器人，跨试验复用经验与技能，执行结果回传后再写 |  |
| [OpenRUA](https://arxiv.org/abs/2610.02459) | 2026 | Code | A→M,M↔E,E→A | Controller·direct | med | 现成编码 agent 在终端写 ROS 2 控制代码并运行，文件与运行输出回传后迭代 |  |
| [Teach and Grow](https://arxiv.org/abs/2608.17209) | 2026 | Code | A→M,M↔E,E→A | Controller·lifelong | med | Astra 与 Codex 把示范编成闭环技能块，物理反馈指导后续动作与恢复，验证后入库 |  |
| [VLS](https://arxiv.org/abs/2602.03973) | 2026 | Code | A→M,M↔E,E→A | Controller·direct | med | VLM 编写可微奖励引导冻结策略采样，执行反馈触发阶段切换并重新查询 VLM |  |

### 编排者（38）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [Inner Monologue](https://arxiv.org/abs/2207.05608) | 2022（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | LLM 生成语言步骤调用技能，成功检测与人反馈回灌形成闭环 |  |
| [DROC](https://arxiv.org/abs/2311.10678) | 2023（先驱） | Code | A→M,M↔E,E→A | Controller·lifelong | high | LLM 依人类语言纠正修订计划与技能代码，蒸馏检索经验后再执行 |  |
| [Look Before You Leap](https://arxiv.org/abs/2311.17842) | 2023（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | GPT-4V 看图规划并调用技能，执行后依视觉反馈重新规划 |  |
| [RoCo](https://arxiv.org/abs/2307.04738) | 2023（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | 多 LLM 智能体对话协商计划，IK 等执行失败反馈后重规划 |  |
| [SayNav](https://arxiv.org/abs/2309.04077) | 2023（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator·vln | high | LLM 基于增量 3D 场景图生成导航子目标，新观测回传后动态重规划 |  |
| [SayPlan](https://arxiv.org/abs/2307.06135) | 2023（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | LLM 在 3D 场景图上语义搜索并调用规划器与技能，仿真反馈触发重规划 |  |
| [BUMBLE](https://arxiv.org/abs/2410.06237) | 2024（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | VLM 统一感知与技能选择，依执行反馈与双层记忆重规划 |  |
| [COME-robot](https://arxiv.org/abs/2404.10220) | 2024（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | GPT-4V 闭环开放词表移动操作，执行监测失败后回溯重规划 |  |
| [InstructNav](https://arxiv.org/abs/2406.04882) | 2024（先驱） | Policy | A→M,M↔E,E→A | Controller·direct·vln | high | LLM 生成导航链并反复重规划，价值图引导的局部规划器执行 |  |
| [LLM3](https://arxiv.org/abs/2403.11552) | 2024（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | LLM 提出符号动作与连续参数调用运动规划，运动失败原因回传后重推理 |  |
| [ORGANA](https://arxiv.org/abs/2401.06949) | 2024（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | LLM 与化学家对话定目标并调度机器人与设备，感知结果回传后调整流程 |  |
| [Open-Nav](https://arxiv.org/abs/2409.18794) | 2024（先驱） | None | A→E,E→A | Controller·orchestrator·vln | med | 开源 LLM 每步依观测选路点并推进，观测回流后逐步决策 | 层级复核（Haiku 判 L3）：每步选路点交局部控制器执行，与 InstructNav、SayNav 同为 L2 |
| [VLM-PC](https://arxiv.org/abs/2407.02666) | 2024（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | VLM 依交互历史选择并规划未来技能，执行后持续重规划 |  |
| [AquaChat](https://arxiv.org/abs/2507.16841) | 2025（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | GPT-4 生成 ROV 巡检计划，任务出错时依底层控制反馈触发重规划 |  |
| [Being-0](https://arxiv.org/abs/2503.12533) | 2025（先驱） | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | 基础模型做高层规划并调用技能库，执行反馈回传后调整计划 |  |
| [RoboMemory](https://arxiv.org/abs/2508.01415) | 2025（先驱） | Policy | A→M,M↔E,E→A | Controller·lifelong | med | 通用 VLM 做闭环规划，批评模块回传执行结果，多类记忆辅助长时程决策 |  |
| [ABot-Claw](https://arxiv.org/abs/2604.10096) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | 通用 agent 调度异构机器人，批评家反馈驱动局部纠正与重规划；记忆为辅 |  |
| [ASENA](https://arxiv.org/abs/2609.39207) | 2026 | Code | A→M,M↔E,E→A | Controller·lifelong·vln | med | 编码 agent 写并运行程序、调用导航策略工具，依执行结果修复并复用经验 |  |
| [AerialClaw](https://arxiv.org/abs/2606.12142) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | LLM agent 调用无人机硬技能与软技能，运行反馈回传后迭代更新决策 |  |
| [AgenticNav](https://arxiv.org/abs/2606.10577) | 2026 | None | A→E,E→A | Controller·direct·vln | med | 零样本 VLM 直接选像素目标并输出运动，每步观测与深度反馈回传后再决策 | 层级复核（Haiku 判 L3）：选目标像素再由 harness 转成运动；兼 L3 |
| [Air-Ground VLN](https://arxiv.org/abs/2609.03483) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator·vln | med | 无人机与地面车的 VLM 在共享鸟瞰图上互下子目标，位姿与目标更新后再决策 |  |
| [CaP Great Again](https://arxiv.org/abs/2609.39018) | 2026 | Code | A→M,M↔E,E→A | Controller·lifelong | high | 编程 agent 编写机器人工具，执行 agent 调用并依每次执行结果保留模型级决策 |  |
| [Cybo-Waiter](https://arxiv.org/abs/2603.10675) | 2026 | Code | A→M,M↔E,E→A | Controller·orchestrator | high | VLM 编译带前后条件的子任务程序，3D 条件检查反馈驱动推进与重规划 |  |
| [HAM-VLN](https://arxiv.org/abs/2607.29600) | 2026 | None | A→E,E→A | Controller·direct·vln | med | MLLM 每个路点同时选下一动作并写分层记忆，观测与失败记录回传后再决策 | 层级复核（Haiku 判 L3）：路点由底层执行，同上 |
| [HaltNav](https://arxiv.org/abs/2603.12696) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator·vln | low | MLLM 大脑拆分子指令，执行中检测阻塞后更新拓扑并重规划；停止模块为微调，存疑 |  |
| [Harness VLA](https://arxiv.org/abs/2607.08448) | 2026 | Policy | A→M,M↔E,E→A | Controller·lifelong | med | 记忆增强的 LLM agent 调用冻结 VLA 原语并重试、重摆放，跨 episode 记忆回传 |  |
| [HarnessVLN](https://arxiv.org/abs/2609.15195) | 2026 | Code | A→M,M↔E,E→A | Controller·orchestrator·vln | high | MLLM 提出规划经 harness 验证后分派执行工具，执行反馈更新共享记忆与图 |  |
| [MessyMem](https://arxiv.org/abs/2609.15976) | 2026 | Policy | A→M,M↔E,E→A | Controller·lifelong | low | VLM 规划者调用技能，交互结果更新持久场景图并供后续决策；闭环经记忆间接成立 |  |
| [NovaPlan](https://arxiv.org/abs/2602.20119) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | VLM 规划者分解子目标并闭环监控执行，失败后重规划；视频关键点驱动底层动作 |  |
| [OnFly](https://arxiv.org/abs/2603.10682) | 2026 | Policy | A→M,M↔E,E→A | Controller·direct·vln | med | 机载 VLM 生成目标，另一 VLM 依关键帧监控进度并触发恢复，经规划器执行后闭环 |  |
| [One Agent to Guide Them All](https://arxiv.org/abs/2602.15400) | 2026 | None | A→E,E→A | Controller·direct·vln | med | MLLM 在度量世界表示上反事实推理后直接选动作，执行观测回传后再决策 | 层级复核（Haiku 判 L3）：动作粒度不明，按规则取保守的 L2 |
| [PhysMem](https://arxiv.org/abs/2602.20323) | 2026 | Policy | A→M,M↔E,E→A | Controller·lifelong | med | VLM 规划者记录经验并提出物理假设，经交互验证后再用于决策，闭环成立 |  |
| [Physical Agency](https://arxiv.org/abs/2607.21725) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | LLM 编排者调用 VLA 与参数化技能，观测核验结果后重规划并恢复失败 |  |
| [RoboClaw](https://arxiv.org/abs/2603.11558) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | 单 VLM 控制器编排学习型原语并依执行结果重新决策，闭环在执行与采集中 |  |
| [Smart-Agriculture Engine](https://arxiv.org/abs/2609.00106) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | low | 事件驱动 LLM agent 经农机与传感器 API 执行作业，事件回传后再决策；平台属性偏强 |  |
| [SpaceMind](https://arxiv.org/abs/2604.14399) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | VLM agent 调度技能与 MCP 工具，闭环运行结果回传并沉淀为技能文件 |  |
| [Thea](https://arxiv.org/abs/2608.11246) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | agent 循环调用机器人能力工具，场景图与执行评估结果回传后继续决策 |  |
| [Tool-Aligned VLA Agent](https://arxiv.org/abs/2605.13119) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | med | VLM agent 选择并调度 VLA 工具，进度反馈触发重规划；另含 VLA 后训练 |  |

### 经验迁移（8）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [Manipulate-Anything](https://arxiv.org/abs/2406.18915) | 2024（先驱） | Policy | A→M,M↔E,E→A | Teacher | med | VLM 分解任务、执行、验证并重规划，经验证的轨迹训练行为克隆策略；是 agent 方法而不是数据平台 | 复核改判（原 剔除）：属蒸馏 / 经验迁移，不是 RoboTwin 那样的平台 |
| [CAPEX](https://arxiv.org/abs/2609.33007) | 2026 | Policy | A→M,M↔E,E→A | Teacher | med | 基础模型作自主示范者，依前次执行经验自适应决定观察与重规划频率 |  |
| [Frontier Demo Generation](https://arxiv.org/abs/2610.03615) | 2026 | Policy | A→M,M↔E,E→A | Teacher | med | 前沿模型生成示范并累积纠错示例，执行结果回传，训练快速本地策略 |  |
| [GUAVA](https://arxiv.org/abs/2606.18363) | 2026 | Policy | A→M,M↔E,E→A | Teacher | low | 前沿通用 VLM 在感知-推理-动作循环中调用原语，4B 蒸馏版为次要验证 |  |
| [LocalNav](https://arxiv.org/abs/2606.27871) | 2026 | - | A→E,E→A | Teacher·vln | high | 前沿 VLM 导航 agent 的轨迹蒸馏到端侧 4B 模型，属你 L2 中的蒸馏（经验迁移） | 复核改判（原 剔除）：你把蒸馏列在 L2 |
| [RHD](https://arxiv.org/abs/2609.33378) | 2026 | Policy | A→M,M↔E,E→A | Teacher | med | 强 agent 把经验写成 playbook 指导轻量 agent 调用 VLA，执行反馈回传修订 |  |
| [Robo-COP](https://arxiv.org/abs/2610.09228) | 2026 | Policy | A→M,M↔E,E→A | Controller·lifelong | med | VLM 编排者依自身执行整理示范、决定微调 VLA，验证变好才采用，结果回传 |  |
| [SkillWeaver](https://arxiv.org/abs/2609.36171) | 2026 | Policy | A→M,M↔E,E→A | Teacher | med | VLM agent 调用并参数化 RL 技能，观察结果后反思、树搜索探索，轨迹用于训练 |  |

### 运行时监控（9）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [DoReMi](https://arxiv.org/abs/2307.00329) | 2023（先驱） | Code | A→M,M↔E,E→A | Supervisor | high | LLM 写计划与约束，VLM 监测违例后触发 LLM 重规划 |  |
| [REFLECT](https://arxiv.org/abs/2306.15724) | 2023（先驱） | Policy | A→M,M↔E,E→A | Supervisor | low | LLM 归因执行失败并指导规划器重规划，失败证据回流（事后重试） |  |
| [Safety Chip](https://arxiv.org/abs/2309.09919) | 2023（先驱） | Code | A→M,M↔E,E→A | Supervisor | low | LLM 把安全规范译为 LTL 约束，运行时违例推理回馈 LLM 修订 |  |
| [Code-as-Monitor](https://arxiv.org/abs/2412.04455) | 2024（先驱） | Code | A→M,M↔E,E→A | Supervisor | med | VLM 写监测代码逐帧检查约束，违例或预测违例时触发重规划 |  |
| [Beyond Human Demos](https://arxiv.org/abs/2609.24996) | 2026 | Code | A→M,M↔E,E→A | Supervisor | med | LLM 编写护栏代码过滤遥操作与策略指令，依轨迹反馈迭代修订 |  |
| [Contextual Safety Reasoning](https://arxiv.org/abs/2602.19983) | 2026 | Code | A→M,M↔E,E→A | Supervisor | med | VLM 随视觉观测持续推断情境安全规则并写成 CBF 约束，观测回传 |  |
| [FRAMES](https://arxiv.org/abs/2609.22538) | 2026 | Policy | A→M,M↔E,E→A | Supervisor | med | 规划与恢复 agent 选技能，监测失败后反馈恢复 agent 重新决策 |  |
| [UAV Selective Recovery](https://arxiv.org/abs/2606.14219) | 2026 | Policy | A→M,M↔E,E→A | Supervisor | med | 外部推理者仅在受阻时调用、选预定义恢复技能，执行结果回传再决策 |  |
| [When to Act, Ask, or Learn](https://arxiv.org/abs/2602.22474) | 2026 | Policy | A→M,M↔E,E→A | Supervisor | med | VLM 在策略采样的动作中挑选，或决定澄清、请求人工干预，属运行时监控 | 复核改判（原 剔除）：选项中含求助等控制行为，有决策权 |

## 保留 · L3（6）

执行层：中间为 None，通用大模型在执行中自己逐步输出动作

### 直接动作（6）

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [NavGPT](https://arxiv.org/abs/2305.16986) | 2023（先驱） | None | A→E,E→A | Controller·direct·vln | med | 纯 LLM 每步依观测从候选方向中选移动，新观测回流后再决策 |  |
| [Prompt a Robot to Walk](https://arxiv.org/abs/2309.09969) | 2023（先驱） | None | A→E,E→A | Controller·direct | med | LLM 以观测-动作历史为提示，逐步直接输出关节动作，闭环在 LLM 内 |  |
| [VLMnav](https://arxiv.org/abs/2411.05755) | 2024（先驱） | None | A→E,E→A | Controller·direct·vln | high | 通用 VLM 每步直接选导航动作，零样本当端到端策略，新观测回传后再决策 |  |
| [Agent as Policy](https://arxiv.org/abs/2609.12541) | 2026 | Code | A→M,M↔E,E→A | Controller·direct | high | 通用 agent 编写程序并发出运动指令，依物理结果修订，真机闭环 | 层级复核（Haiku 判 L2）：论文主张 agent 本身就是策略、直接下运动指令；也写程序，兼 L2 |
| [Show-Harness](https://arxiv.org/abs/2609.10522) | 2026 | None | A→E,E→A | Controller·direct | med | 前沿 VLM 直接输出语义微动作（解释器仅做落地），观测回传后逐步决策 |  |
| [VIA](https://arxiv.org/abs/2607.11119) | 2026 | None | A→E,E→A | Controller·direct | med | FM agent 经浏览器式 3D 界面下发直观指令，截图观察结果后调整，闭环在执行中 |  |

## 资源（20）

以通用大模型 agent 为对象的 benchmark 或评测研究

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [FAEA](https://arxiv.org/abs/2601.20334) | 2026 | Code | A→M,M↔E,E→A | Controller·direct | med | 未修改的通用 LLM agent 框架直接做操作，属无自有方法的评测；闭环存在 | 把现成软件工程 agent 框架原样用于操作，更像评测；也可作为 L2 方法保留 |
| [Astra on RoboDojo](https://arxiv.org/abs/2609.24170) | 2026 | None | A→E,E→A | Controller·direct | low | 通用 LLM 不经微调直接当操作策略并做 42 任务评测，无自有方法；E→A 摘要未明示 | 你举的「LLM 直接做动作」的例子；作为评测研究放资源，评测的是 L3 |
| [Embodied Agents Take Control](https://arxiv.org/abs/2607.26148) | 2026 | None | A→E,E→A | Controller·direct·vln | med | 通用编码 agent 逐步直接操控动作的评测研究，无自有方法，面向零样本导航 | 评测 coding agent 每步直接控制导航，评测的是 L3 |
| [PARTNR](https://arxiv.org/abs/2411.00081) | 2024 | Policy | A→M,M↔E,E→A | Controller | med | 评测 LLM 规划者调用技能与工具的人机协作闭环，含失败恢复 |  |
| [SafeAgentBench](https://arxiv.org/abs/2412.13178) | 2024 | Policy | A→M,M↔E,E→A | Controller | med | 750 个安全任务评测 LLM 具身 agent 的规划与拒绝危险指令能力 |  |
| [EmbodiedBench](https://arxiv.org/abs/2502.09560) | 2025 | Policy | A→M,A→E,M↔E,E→A | Controller | med | 评测 24 个 MLLM 作为视觉具身 agent 的高层规划与低层操作闭环表现 |  |
| [EmbodiedEval](https://arxiv.org/abs/2501.11858) | 2025 | None | A→E,E→A | Controller | med | 交互式评测 MLLM 具身 agent 的导航、交互与问答闭环表现 |  |
| [IS-Bench](https://arxiv.org/abs/2506.16402) | 2025 | Policy | A→M,M↔E,E→A | Supervisor | med | 评测 VLM 家务 agent 执行中能否按正确顺序规避动态风险 |  |
| [RoboCerebra](https://arxiv.org/abs/2506.06677) | 2025 | Policy | A→M,M↔E,E→A | Controller | med | 评测 VLM 规划者编排 VLA 控制器，含反思与记忆的闭环长程任务 |  |
| [Astra on VLN-CE](https://arxiv.org/abs/2609.20116) | 2026 | None | A→E,E→A | Controller | med | 评测 GPT-6-Astra 作为零样本 VLN-CE 决策者，观测与执行反馈闭环 |  |
| [CodeActionBench](https://arxiv.org/abs/2609.33807) | 2026 | Code | A→M,M↔E,E→A | Controller | high | 评测通用模型以代码为策略操作机器人，依执行反馈迭代修改程序 |  |
| [EmboCoach-Bench](https://arxiv.org/abs/2601.21570) | 2026 | Code | A→M,M↔E,E→A | Developer | high | 评测 LLM agent 以可执行代码迭代编写与调试具身策略的闭环 |  |
| [EmbodiedSWE](https://arxiv.org/abs/2609.27308) | 2026 | Code | A→M,M↔E,E→A | Teacher | low | 基准评测前沿编码 agent 的仿真反馈闭环，另含数据生成与 VLA 训练 |  |
| [Frontier VLM Agents Study](https://arxiv.org/abs/2610.00854) | 2026 | None | A→E,E→A | Controller | med | 评测七个前沿 VLM agent 的几何、空间与操作闭环表现，含多轮复查 |  |
| [LIBERO-Agent](https://arxiv.org/abs/2609.39507) | 2026 | None | A→E,E→A | Controller | high | 评测通用 agent 直接发出原生动作指令操作机器人，观测回传后再决策 |  |
| [MLLM Drone Agents Eval](https://arxiv.org/abs/2609.01404) | 2026 | None | A→E,E→A | Controller | high | 评测 MLLM 直接作为无人机控制闭环 agent，覆盖接近、跟踪、搜索与编队 |  |
| [Orchestration Study](https://arxiv.org/abs/2606.10267) | 2026 | Policy | A→M,M↔E,E→A | Controller | low | 对 VLM 规划者编排 VLA 控制器的设计做受控评测，主体为研究而非新方法 |  |
| [RLE-Bench](https://arxiv.org/abs/2609.34210) | 2026 | Code | A→M,A→E,M↔E,E→A | Developer | high | 评测编码 agent 作为机器人学习工程师，依多模态反馈迭代改进产物 |  |
| [RobotWorld](https://arxiv.org/abs/2610.10409) | 2026 | Code | A→M,M↔E,E→A | Controller | med | 评测通用多模态 agent 经机器人接口执行 84 个跨形态任务的闭环 |  |
| [Video2World](https://arxiv.org/abs/2610.04432) | 2026 | Code | A→E,A→M,M↔E,E→A | Designer·real2sim | med | 评测编码 agent 从具身视频端到端搭建可交互仿真，依执行反馈迭代 |  |

## 剔除（13）

决策者不是通用大模型，agent 作用太弱，主体是数据生成平台或离线评测，或摘要无法确认决策者

| 论文 | 年 | 中间层 | 箭头 | 原分类 | 置信 | 理由 | 备注 |
|---|---|---|---|---|---|---|---|
| [LM-Nav](https://arxiv.org/abs/2207.04429) | 2022（先驱） | Policy | A→M,M↔E | Controller·orchestrator·vln | high | LLM 只把指令解析为地标一次，导航由预训练模型完成，无 E→A |  |
| [AutoRT](https://arxiv.org/abs/2401.12963) | 2024（先驱） | Policy | A→M,M↔E | Controller·orchestrator | high | LLM 提议任务、大规模真机采数据，主体是数据采集平台 |  |
| [ReMEmbR](https://arxiv.org/abs/2409.13682) | 2024（先驱） | Policy | A→M,M↔E | Controller·lifelong | med | 以记忆检索问答为主，检索非执行结果，导航目标无回传，无 E→A |  |
| [HumanoidGen](https://arxiv.org/abs/2507.00833) | 2025（先驱） | Code | A→M,M↔E,E→A | Teacher | high | 主体是双臂灵巧操作的数据与任务生成框架，含基准，agent 循环非主贡献 |  |
| [RoboFAC](https://arxiv.org/abs/2505.12224) | 2025（先驱） | Policy | A→M,E→A | Supervisor | high | 决策者为在失败轨迹上微调的专用多模态模型，非通用 LLM/VLM |  |
| [RoboTwin 2.0](https://arxiv.org/abs/2506.18088) | 2025（先驱） | Code | A→M,M↔E,E→A | Teacher | high | MLLM 写任务代码并仿真修正，主体是数据生成器与基准（裁定剔除） |  |
| [Embodied Agent Interface](https://arxiv.org/abs/2410.07166) | 2024 | - | - | Controller | med | 无 E→A：LLM 各模块输出离线逐项评测，未在闭环中执行与回传 |  |
| [VLABench](https://arxiv.org/abs/2412.18194) | 2024 | None | A→E,E→A | Controller | high | 决策者为专用 VLA 而非通用 LLM/VLM，主体是操作评测基准 |  |
| [ASIMOV](https://arxiv.org/abs/2503.08663) | 2025 | Code | A→M | Supervisor | med | 无 E→A：宪章与安全数据离线生成与判定，主体是基准与数据集 |  |
| [AgentVLN](https://arxiv.org/abs/2603.17670) | 2026 | - | A→M,E→A | Controller·orchestrator·vln | low | 疑为任务训练的 VLM 作大脑（旧注与边缘部署表述），通用模型条件存疑 |  |
| [Ludi](https://arxiv.org/abs/2608.22035) | 2026 | Policy | A→M,M↔E,E→A | Controller·orchestrator | high | 决策核心是为社交多轮交互微调的 VLM，非通用 agent（条件1不符） |  |
| [RoboFind](https://arxiv.org/abs/2609.20330) | 2026 | - | A→M,E→A | Controller·orchestrator·vln | low | 摘要未见通用 LLM/VLM 决策者，候选验证或为参考库比对，决策主体存疑 | 摘要没写明各 agent 用的模型；若是通用 VLM，可保留为 L2 编排者 |
| [WhenToAsk](https://arxiv.org/abs/2609.21942) | 2026 | Policy | E→A,A→M | Supervisor | low | 摘要未说明决策者是否为通用 LLM/VLM（模型未核实），无法确认条件1 | 摘要只写了 agentic 失败处理层，没写明是不是通用大模型；若是，可归 L2 运行时监控 |

