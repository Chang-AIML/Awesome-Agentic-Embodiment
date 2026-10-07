# 核心表审阅清单

由 `scripts/build_core_table.py` 从 `data/core/core_selection.csv` 生成。要增删或改判，改 selection 文件后重新运行脚本。

## Controller · 编排型（11）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [SayCan](https://arxiv.org/abs/2204.01691) | 2022 | G | 种子 | 奠基作：LLM 与 affordance 组合，逐步在异质 skill 中选择，执行后重新调用；Controller 的起点 |
| [Inner Monologue](https://arxiv.org/abs/2207.05608) | 2022 | G | 种子 | 奠基作：成功检测与人类反馈回灌提示，典型闭环规划者 |
| [RoCo](https://arxiv.org/abs/2307.04738) | 2023 | G | 种子 | 多机器人对话协商（×N）的代表；种子论文 |
| [MOSAIC](https://arxiv.org/abs/2402.18796) | 2024 | G | 判定池 | 1:N 拓扑代表：LLM 规划者与用户对话并调度两台机器人协作烹饪 |
| [COME-robot](https://arxiv.org/abs/2404.10220) | 2024 | G | 判定池 | GPT-4V 闭环开放词表移动操作，执行反馈驱动重规划；覆盖 mobile-manip |
| [VLM-PC](https://arxiv.org/abs/2407.02666) | 2024 | G | 补漏 | 足式机器人：VLM 依上下文历史选择并重规划运动技能以应对障碍；覆盖 loco |
| [BUMBLE](https://arxiv.org/abs/2410.06237) | 2024 | G | 补漏 | VLM 统一感知、粗到细技能与双层 memory，楼宇级长程移动操作，90+ 小时真机评测 |
| [Being-0](https://arxiv.org/abs/2503.12533) | 2025 | G | 判定池 | 人形机器人 agent：FM 规划 + VLM connector 调用技能；覆盖 humanoid |
| [Agentic Robot](https://arxiv.org/abs/2505.23450) | 2025 | G | 判定池 | 推理模型分解子目标、VLA 执行、verifier 逐子目标检查；VLA-as-tool 编排（2025） |
| [RoboClaw](https://arxiv.org/abs/2603.11558) | 2026 | G | 判定池 | 单 VLM 控制器统一数据采集、策略学习与执行，编排学习型原语并自复位（43 引） |
| [Thea](https://arxiv.org/abs/2608.11246) | 2026 | G | 判定池 | 把 coding-agent harness 范式迁移到具身：工具化能力 + 场景图上下文；2026 harness 浪潮代表 |

## Controller · 直接驱动型（6）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [InstructNav](https://arxiv.org/abs/2406.04882) | 2024 | G | 判定池 | 零样本通用指令导航，LLM 反复重规划 Dynamic Chain-of-Navigation；覆盖 nav |
| [FAEA](https://arxiv.org/abs/2601.20334) | 2026 | G | 判定池 | 软件工程 agent 框架不改动直接用于操作（LIBERO 等），robot-use agent 代表 |
| [CaP-X](https://arxiv.org/abs/2603.22435) | 2026 | G | 判定池 | coding agent 写当下执行的控制代码并依视觉差分反馈修正；CaP 的闭环继承者与评测框架 |
| [VIA](https://arxiv.org/abs/2607.11119) | 2026 | G | 判定池 | FM 通过浏览器式 3D 界面像操作软件一样驱动机械臂；接口新颖 |
| [Show-Harness](https://arxiv.org/abs/2609.10522) | 2026 | G | 判定池 | 用户点名：前沿 VLM 输出语义微动作由确定性解释器执行，零样本真机 |
| [Agent as Policy](https://arxiv.org/abs/2609.12541) | 2026 | G | 判定池 | 通用 agent 写程序、发运动指令并依物理结果修订，直接驱动真机 |

## Controller · lifelong / memory 型（4）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [DROC](https://arxiv.org/abs/2311.10678) | 2023 | G | 判定池 | 整合在线语言纠正修订计划与技能代码，并蒸馏检索知识（H closure） |
| [LRLL](https://arxiv.org/abs/2406.18746) | 2024 | G | 判定池 | LLM 在技能库上写策略代码并通过 memory 与自提任务扩库；lifelong 早期代表 |
| [Harness VLA](https://arxiv.org/abs/2607.08448) | 2026 | G | 判定池 | 用户点名：冻结 VLA 作为工具，agent 重落地与重摆放，memory 跨 episode 学习 |
| [MessyMem](https://arxiv.org/abs/2609.15976) | 2026 | G | 判定池 | 持久 3D 场景图 memory 随交互结果更新的移动操作 agent |

## Controller · 训练过的 carrier（5）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [PaLM-E](https://arxiv.org/abs/2303.03378) | 2023 | C | 种子 | 训练过的 carrier（C）奠基作：多模态 LLM 输出计划供低层策略执行；种子论文 |
| [Hi Robot](https://arxiv.org/abs/2502.19417) | 2025 | H | 判定池 | 分层 H 的代表：高层 VLM 输出下一步指令并响应用户反馈，低层协同设计 |
| [OneTwoVLA](https://arxiv.org/abs/2505.11917) | 2025 | I | 判定池 | 内化 I 的代表：单一 VLA 自适应地决定何时推理、维护历史并从错误恢复 |
| [Gemini Robotics 1.5](https://arxiv.org/abs/2510.03342) | 2025 | H | 判定池 | 厂商 ER 编排者 + 自家 VLA（协同设计），规划、估计进度并调用工具 |
| [MEM](https://arxiv.org/abs/2603.03596) | 2026 | I | 判定池 | VLA 输出子任务语言并更新自身文本记忆（多尺度记忆，76 引） |

## Supervisor（8）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [REFLECT](https://arxiv.org/abs/2306.15724) | 2023 | G | 判定池 | 奠基 Supervisor：总结机器人经验解释失败，解释驱动纠正（296 引） |
| [DoReMi](https://arxiv.org/abs/2307.00329) | 2023 | G | 判定池 | LLM 写约束、VLM 持续监测违例并触发恢复与重规划 |
| [Code-as-Monitor](https://arxiv.org/abs/2412.04455) | 2024 | G | 判定池 | 用户点名：VLM 编写约束监测代码逐帧执行，违例或预测违例时重规划 |
| [Phoenix](https://arxiv.org/abs/2504.14588) | 2025 | H | 判定池 | 运动级自我反思：MLLM 输出运动纠正指令给协同训练的执行器；Supervisor 中的 H |
| [RoboSafe](https://arxiv.org/abs/2512.21220) | 2025 | G | 判定池 | 可执行安全谓词在运行时拦截危险动作并触发重规划；安全方向代表 |
| [CycleVLA](https://arxiv.org/abs/2601.02295) | 2026 | G | 判定池 | VLM 预测失败并触发子任务回退与重试，主动自纠正的 VLA 监督 |
| [FRAMES](https://arxiv.org/abs/2609.22538) | 2026 | G | 判定池 | 人形机器人多视角技能监测与恢复（×R） |
| [WhenToAsk](https://arxiv.org/abs/2609.21942) | 2026 | G | 判定池 | 失败后在恢复、补充感知和向人求助之间选择；人机对话式恢复 |

## Teacher（6）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [Manipulate-Anything](https://arxiv.org/abs/2406.18915) | 2024 | G | 判定池 | VLM 分解、执行、验证并重规划，经验证轨迹训练行为克隆策略（125 引） |
| [RoboTwin 2.0](https://arxiv.org/abs/2506.18088) | 2025 | G | 判定池 | MLLM 写任务代码并经仿真闭环修正，合成经验证的示范（571 引） |
| [GUAVA](https://arxiv.org/abs/2606.18363) | 2026 | G→C | 判定池 | 用户点名：前沿 VLM 在 harness 中行动的轨迹蒸馏为 4B agent，同接口 agent→agent 迁移 |
| [LocalNav](https://arxiv.org/abs/2606.27871) | 2026 | G→C | 判定池 | 前沿 VLM 导航 agent 轨迹蒸馏到端侧 4B VLM；覆盖 nav 的 Teacher |
| [EmbodiedSWE](https://arxiv.org/abs/2609.27308) | 2026 | G | 判定池 | coding agent 迭代编写调试灵巧操作程序，经验证解扩展为训练示范 |
| [RHD](https://arxiv.org/abs/2609.33378) | 2026 | G | 判定池 | 强 agent 的经验提炼成 playbook 供轻量 agent 使用（in-context 迁移） |

## Designer（8）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [Eureka](https://arxiv.org/abs/2310.12931) | 2023 | G | 种子 | 奠基 Designer：LLM 写奖励代码并依 RL 训练统计反思进化 |
| [OMNI-EPIC](https://arxiv.org/abs/2405.15568) | 2024 | G | 判定池 | FM 写环境、奖励与成功代码，开放式任务生成 |
| [REvolve](https://arxiv.org/abs/2406.01309) | 2024 | G | 判定池 | 人类反馈 + 训练结果驱动奖励进化（H closure） |
| [DrEureka](https://arxiv.org/abs/2406.01967) | 2024 | G | 判定池 | 奖励 + domain randomization 设计，四足 sim-to-real |
| [CurricuLLM](https://arxiv.org/abs/2409.18382) | 2024 | G | 判定池 | LLM 生成子任务课程与奖励代码，依策略结果推进 |
| [Eurekaverse](https://arxiv.org/abs/2411.01775) | 2024 | G | 判定池 | LLM 写地形环境代码并依训练结果迭代课程 |
| [Video2Policy](https://arxiv.org/abs/2502.09886) | 2025 | G | 判定池 | 从视频重建仿真任务并依 RL 反馈迭代奖励代码 |
| [FIND](https://arxiv.org/abs/2609.32069) | 2026 | G | 判定池 | 真机 agentic RL：VLM 依近期成功率选择练习任务并自评结果 |

## Developer（9）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [RoboMorph](https://arxiv.org/abs/2407.08626) | 2024 | G | 判定池 | LLM 进化机器人形态（硬件），最早的 Developer |
| [VLMgineer](https://arxiv.org/abs/2507.12644) | 2025 | G | 判定池 | VLM 协同设计工具与动作并以仿真进化评估；硬件侧 Developer |
| [HARBOR](https://arxiv.org/abs/2606.08610) | 2026 | G | 判定池 | 专职 coding agent 搭环境、塑奖励、调超参、训练 RL 策略（Developer|Designer） |
| [RHO](https://arxiv.org/abs/2606.16458) | 2026 | G | 判定池 | coding agent 依奖励与执行反馈搜索修改多文件策略代码库 |
| [RATs (Playful)](https://arxiv.org/abs/2606.19419) | 2026 | G | 补漏 | 游玩阶段自提任务、执行、验证并蒸馏成冻结的代码技能库，测试时复用；Developer 的 skill-library 型 |
| [ENPIRE](https://arxiv.org/abs/2606.19980) | 2026 | G | 判定池 | 用户点名：多个 coding agent 修改策略与训练代码，真机试验决定保留或回滚 |
| [ASPIRE](https://arxiv.org/abs/2607.00272) | 2026 | G | 判定池 | coding agent 编写并精炼控制程序，从执行轨迹诊断失败，验证后入技能库（56 引） |
| [SimEX](https://arxiv.org/abs/2609.38982) | 2026 | G | 判定池 | coding agent 在仿真中迭代工具箱代码并经少量真机试验校准 |
| [Skill2Real](https://arxiv.org/abs/2610.02788) | 2026 | G | 判定池 | Proposer-Verifier-Governor 依仿真结果保留或回滚技能代码，零样本 sim-to-real |

## 前驱（precursor）（8）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [ZS-Planners](https://arxiv.org/abs/2201.07207) | 2022 | G | 种子 | LLM 作零样本规划者的起点 |
| [Code as Policies](https://arxiv.org/abs/2209.07753) | 2022 | G | 种子 | 用户认定的奠基作：LLM 一次写出策略程序；不再因后果重新调用 |
| [ProgPrompt](https://arxiv.org/abs/2209.11302) | 2022 | G | 种子 | 程序化提示生成带断言的任务程序 |
| [KnowNo](https://arxiv.org/abs/2307.01928) | 2023 | G | 判定池 | 不确定时向人求助的起点；人挑选选项替代了模型决策 |
| [VoxPoser](https://arxiv.org/abs/2307.05973) | 2023 | G | 种子 | LLM 写代码组合 3D 价值图约束，持续作用但不再调用模型 |
| [SUDD](https://arxiv.org/abs/2307.14535) | 2023 | G | 判定池 | LLM 规划并写成功检查代码生成数据再蒸馏；Teacher 的前驱 |
| [ECoT](https://arxiv.org/abs/2407.08693) | 2024 | I | 种子 | 显式推理 VLA 的起点；每步推理但无自身记录 |
| [π0.5](https://arxiv.org/abs/2504.16054) | 2025 | I | 判定池 | 预测子任务文本再出动作的 VLA；Harness VLA 所包装的底座（2186 引） |

## Benchmark 与资源（14）

| 短名 | 年份 | Carrier | 来源 | 入选理由 |
|---|---|---|---|---|
| [Embodied Agent Interface](https://arxiv.org/abs/2410.07166) | 2024 | - | 补漏 | 把 LLM 具身决策拆成目标解释、子目标分解、动作序列、转移建模四个模块逐项评测 |
| [PARTNR](https://arxiv.org/abs/2411.00081) | 2024 | - | 判定池 | 人机协作规划与推理 benchmark（F1，作为资源收录） |
| [SafeAgentBench](https://arxiv.org/abs/2412.13178) | 2024 | - | 补漏 | 750 个危险/安全任务，测试具身 LLM agent 是否拒绝危险指令 |
| [VLABench](https://arxiv.org/abs/2412.18194) | 2024 | - | 判定池 | 语言条件操作的大规模长程推理 benchmark（228 引） |
| [EmbodiedEval](https://arxiv.org/abs/2501.11858) | 2025 | - | 判定池 | 交互式评测 MLLM 作为具身 agent（导航、交互、问答） |
| [EmbodiedBench](https://arxiv.org/abs/2502.09560) | 2025 | - | 补漏 | 24 个 MLLM 作为视觉驱动具身 agent 的综合评测，从高层规划到低层操作 |
| [ASIMOV](https://arxiv.org/abs/2503.08663) | 2025 | - | 补漏 | 自动生成机器人宪章与语义安全 benchmark |
| [RoboCerebra](https://arxiv.org/abs/2506.06677) | 2025 | - | 补漏 | 评测 VLM 规划者编排 VLA 控制器的长程 benchmark |
| [IS-Bench](https://arxiv.org/abs/2506.16402) | 2025 | - | 判定池 | 交互式安全评测：VLM 驱动家务 agent 在过程中是否规避风险 |
| [EmboCoach-Bench](https://arxiv.org/abs/2601.21570) | 2026 | - | 补漏 | 32 个 RL/IL 任务，LLM agent 迭代编写、调试训练代码 |
| [Orchestration Study](https://arxiv.org/abs/2606.10267) | 2026 | - | 判定池 | 对 VLM 规划者 + VLA 分层 agent 的系统性受控研究 |
| [CodeActionBench](https://arxiv.org/abs/2609.33807) | 2026 | - | 补漏 | agentic Code-as-Policy 的 25 任务 benchmark，含隐藏物理结果 |
| [RLE-Bench](https://arxiv.org/abs/2609.34210) | 2026 | - | 判定池 | coding agent 作为机器人学习工程师的资格考试 |
| [LIBERO-Agent](https://arxiv.org/abs/2609.39507) | 2026 | - | 判定池 | 评测通用 agent 直接发出原生动作指令操作机器人 |
