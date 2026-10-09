# Agentic Embodiment：定义与分类

> 2026-10-09 定稿。收录标准来自最后一轮筛选（每篇读全文判定）；分类回到两个阶段、五个 Seat。逐篇结果见 `paper_list.md`。
> 旧版（Seat × Carrier、闭环判定、决策 1–19 的完整记录）保留在 `history/definition_round3.md`。

---

## 1. 一句话定义

*Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs used as-is, not embodied action
models — acting as agents that make explicit decisions and are connected to a robot body, through the policy, code or
plans they produce, or by acting on the environment directly. Its organizing question is when and where such an agent
acts on the robot: before execution — designing its learning problem, teaching it, or developing its system — or at
runtime — controlling it or supervising it (**Seat**).*

中文：Agentic Embodiment 研究**现成的通用大模型**（LLM / VLM，而不是具身动作模型）作为 agent 做出的显式决策。这些决策经由它产出的策略、代码或计划，或者直接作用于环境，到达机器人身体。全文围绕一个问题组织：agent 在什么时候、什么位置作用于机器人——**执行前**（设计学习问题、当老师、改系统），还是**运行时**（控制、监督）。

---

## 2. 收录标准

回路图见 `agent_loop_framework.png`：Agent → Policy / Code / None → Env / Sim；agent 也可以直接作用于 Env / Sim；Env / Sim 的信息可以回到 agent。

| # | 标准 | 用户原话 |
|---|---|---|
| 1 | 通用大模型 agent 必须存在，并在回路里起作用：写计划、写代码或约束、调用技能或 VLA、设计环境，或直接出动作 | 「通用大语言模型agent必须存在，在里面扮演角色才行」 |
| 2 | agent 必须是**现成的**通用大模型（GPT、Claude、Gemini、Qwen-VL-Instruct 等，靠 prompt、工具、记忆或 harness 驱动）。作者训练、微调或蒸馏出的模型不算 agent，即使底座是通用模型 | 「我说的是通用大模型，而不是被训练过的小模型」 |
| 3 | 箭头不必全有：agent 连到 Policy / Code 或 Env / Sim 之一即可。闭环只记录（再决策 / 编写闭环 / 开环），不作门槛 | 「agent必须要和其中部件有所连接即可，无论是环境还是policy」 |
| 4 | 一眼看上去要是在讲 agent。主体是数据集、数据生成平台、资产流水线或 benchmark、LLM 只是其中一个模块的，不收；评测通用 agent 的 benchmark 归「资源」 | 「robotwin一眼看上去就不是agent」 |
| 5 | 通用大模型，不是具身大模型。VLA、分层 VLA、WAM、机器人基础模型做决策的不收；它们只能作为 agent 调用的工具 | （第三轮确定的范围） |
| 6 | 读全文判定：写明谁在做决策、是否经过作者训练、论文主体，并摘一句原文为证 | 「我建议你读读内容」 |

补充：
- 训练过的 VLA、技能、感知模型可以作为 agent 调用的**工具**（如 Harness VLA 调度冻结的 VLA）。
- 通用模型**自己当 agent 行动**、再把它的经验蒸馏成策略或小模型的，算 Teacher（如 GUAVA、SUDD）。
- Env / Sim 的范围（用户 2026-10-09 决定）：真机、物理仿真，以及离散具身仿真（ALFRED、VirtualHome、R2R 离散导航图等，agent 在三维场景里有身体）都算；纯文本世界（只有文字观察和动作的 ALFWorld、TextWorld）和自动驾驶（CARLA、nuScenes、highway-env 等）不算。无人机、多机器人调度按上面六条正常判。

---

## 3. 分类：两个阶段，五个 Seat

阶段由 agent 的产出**什么时候产生、什么时候被用**决定。

| 阶段 | Seat | agent 做什么 | 角色（`role` 列） |
|---|---|---|---|
| **执行前**：产出在机器人执行任务之前产生，冻结后交给部署的系统 | **Designer** | 设计学习问题 | 环境/重建 · 奖励/任务 |
| | **Teacher** | 自己先执行，经检验的示范或经验成为策略的训练目标 | 示范/蒸馏 |
| | **Developer** | 修改系统本身，按试验保留或回滚 | 系统/代码 · 本体/工具 |
| **运行时**：agent 在任务执行过程中起作用 | **Controller** | 每一步决定机器人做什么 | 编排 · 写策略 · 直接动作 |
| | **Supervisor** | 只在异常时介入 | 监控/恢复 |

角色说明：
- **环境/重建**：生成或重建环境、场景、仿真资产与数字孪生（SceneSmith、Agentic Real2Sim、EmbodiedSmith）。
- **奖励/任务**：设计奖励、成功判据、任务与课程（Eureka、GenSim、OMNI-EPIC）。
- **示范/蒸馏**：agent 自己执行，经验蒸馏成策略或小模型（SUDD、GUAVA）。
- **系统/代码**：改训练代码、技能库、harness 或规划域，按试验保留或回滚（ENPIRE、PhysEvo、RPG、SimEX）。
- **本体/工具**：设计机器人形态、硬件或工具（RoboMorph、RobotSmith）。
- **编排**：规划并调用技能、工具、运动规划器或 VLA（SayCan、Inner Monologue、Harness VLA）。
- **写策略**：写出当场运行的策略代码、约束或奖励（Code as Policies、VoxPoser、ReKep）。
- **直接动作**：通用大模型在执行中自己输出动作（Prompt a Robot to Walk、Show-Harness、Agent as Policy）。
- **监控/恢复**：失败检测、安全护栏、恢复与求助（REFLECT、Code-as-Monitor、RoboGuard）。

**归类规则**
- 每篇按主要贡献只归一个 Seat。兼有两个阶段的，看 agent 的产出主要在哪个阶段被用：
  - Agentic RSR、Real2Gym 在重建的仿真里练习、写出程序再带回真机，归 Developer；
  - Language to Rewards 的奖励参数当场交给 MPC 生成动作，归 Controller。
- 模型写出、在运行时执行的程序，算该模型在运行时起作用：
  - Code as Policies 归 Controller；
  - Beyond Human Demos 写的护栏代码在运行时过滤指令，归 Supervisor。
- 资源（benchmark 与评测研究）记录「被评测的 Seat」。

**三个专题**（横跨 Seat，每篇仍标 Seat）：
- **Real2Sim / Sim2Real**：agent 从真实数据重建仿真、在里面练习、再回到真机；只收代表作。
- **VLN 与具身导航**：以导航为主任务的 agent。
- **多智能体（multi-agent）**（用户 2026-10-09 要求单独成章）：多智能体是论文主系统的核心，满足其一即可：
  - 两个及以上机器人或具身智能体（含无人机 + 地面机器人这类异构团队），由通用大模型 agent 分配、规划或协调任务，集中式或每台一个 agent 都算（RoCo、SMART-LLM、AutoRT、ABot-Claw）；
  - 论文把系统呈现为两个及以上分工不同的通用大模型 agent，彼此对话、辩论、协商或交接工作（AdaHVLA 的多 agent 改进流程）。
  - 不算：单个机器人上由几次 prompt 调用拼成的流水线（规划器 + 校验器），论文没有称其为多智能体；只有人机对话；单个 agent 调用 subagent 工具（SPINE）。
  - CSV 里记在 `topic` 列（值为「多智能体」）。

---

## 4. 现状（2026-10-09）

**精选清单**（用户 2026-10-09 决定回到精选，只收 arXiv 论文）：`data/core/paper_list.csv` 共 186 篇，逐篇读全文判定，保留 157、资源 20、剔除 9。保留的论文单独导出为 `data/core/agent_pool.csv`。其中 12 篇 2025 年代表作是用户选定写法 A 后补的（「2025年补一下」），填先驱与 2026 年之间的断档。

| 阶段 | 篇数 | 各 Seat |
|---|---|---|
| 执行前 | 59 | Designer 22、Teacher 10、Developer 27 |
| 运行时 | 98 | Controller 84、Supervisor 14 |

保留的 157 篇中先驱（2022–2025）78 篇、2026 年 79 篇；多智能体专题 13 篇（保留 12、资源 1）。扩展列表中按同一标准补判过的其余 1,339 篇暂存在 `data/core/extended_judged.csv`，不进清单。

**主线（草案）**：*Agency spreads around the body: general models, not embodied action models, fill seat after seat.*
