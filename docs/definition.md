# Agentic Embodiment：定义与分类（正文版）

> 本文是正文用的简化版。细则（A0–A3 全文、Λ 阶梯、E/H/M closure、tier 规则、逐案例论证）保留在
> `definition_draft.md`，作为附录和标注指南。两者冲突时，以本文为准。
>
> 2026-10-07 用户确认的四项决策：
> 1. 主框架采用 **Seat × Carrier**；
> 2. 开环奠基作进入核心表，标为 **前驱（precursor）**；
> 3. 核心集约 **60 篇**，benchmark 与资源另列一张表；
> 4. 自动驾驶与离散仿真**不进核心**，只在边界一节讨论。
>
> 2026-10-08 用户追加的决策：
> 5. 闭环判定（§2 第 3 条）承认**编写闭环**：模型写出的约束或程序在执行时读取实时感知、依据结果调整行为，即使模型不再被调用，也算 agent。ReKep、VoxPoser、Code as Policies 等因此进入核心。
> 6. 核心表扩大到约 **100 篇**，并**聚焦 2026 年**：2026 年的论文进 CORE（约 75 篇）；2022–2025 年的代表作只简要提及，作为**先驱**（约 25 篇）。
> 7. 新增 **Real2Sim / Sim2Real** 专题板块（§6.1），收 agent 搭建、校准、利用仿真并迁移到真机的工作。
>
> 2026-10-08 用户第二次追加的决策（覆盖第 6 条的数字）：
> 8. **ReKep 这一类都算 agent**：VLM 写出空间约束、关键点、可供性或代价函数，交给求解器或规划器执行的工作（ReKep、VoxPoser、OmniManip、CoPa、MOKA 等）一律算 agent，归 Controller · 直接驱动型。执行中依跟踪状态重解的记「编写闭环」，一次求解的记「开环」，仍收录。
> 9. **agentic Real2Sim 都算核心**：由 agent 重建机器人操作场景（3D 场景、资产、铰接、物理参数、仿真代码）的工作，按 §6.1 的规则直接进 CORE，不因「一次构建、不再调用模型」而降级。
> 10. 规模放宽到约 **120 篇**（不是硬指标），仍聚焦 2026 年；2022–2025 年的奠基作与代表作作为先驱一并收录。
> 11. **VLN 单独成章**（§6.2）。
>
> 2026-10-08 用户第三次追加的决策（覆盖第 6、10 条中「聚焦 2026」的说法）：
> 12. **研究对象是通用大模型做具身任务**：LLM / VLM（GPT、Gemini、Claude、Qwen-VL、GPT-6 Astra 等）作为 agent 完成具身任务。它可以输出计划、调用技能 / 工具 / VLA、写代码或约束，也可以直接输出动作，例如 GPT-6 Astra 在 RoboDojo 上直接当策略。**具身大模型直接做动作的工作不收**：VLA（含带推理、子任务、memory、自我纠错的 VLA）、分层 VLA、WAM、机器人基础模型，只能作为被 agent 调用的工具出现。见 §2.0。
> 13. **论文故事不只聚焦 2026**：2026 年论文最多，但 2022–2025 年的先驱同样重要，是每个 seat 的源头。核心表与正文按 seat 讲「先驱 → 2026」的脉络。

---

## 1. 一句话定义

*Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs, not embodied action
models — acting as agents that make explicit decisions whose consequences reach a robot body, and that
re-decide on evidence of those consequences. Its organizing question is where such an agent sits relative
to the body's deployed policy — steering it, guarding it, teaching it, designing its learning problem, or
building its system (**Seat**).*

中文：Agentic Embodiment 研究通用基础模型（LLM / VLM，而不是具身动作模型）作为 agent 做出的显式决策。这些决策的后果会作用到机器人身体上，agent 会依据后果的证据重新决策。全文围绕一个问题组织：这个 agent 相对于机器人部署的策略坐在哪里（**Seat**）。

**推论**：agentic embodiment 不等于 agentic robot。ENPIRE 部署出去的策略里没有 agent，但它仍是核心样本，因为 agent 坐在 Developer 的位置。

---

## 2. 什么算 agent：范围 + 三条判定

### 2.0 范围：通用大模型，不是具身大模型（决策 12）

- **收**：通用大模型（LLM / VLM / MLLM，如 GPT、Gemini、Claude、Qwen-VL、GPT-6 Astra）作为 agent 做具身任务。它输出什么都可以：计划、技能 / 工具 / VLA 调用、代码、约束，或者直接输出动作（LLM-as-policy，如 Agent as Policy、Show-Harness、GPT-6 Astra 在 RoboDojo 上直接当策略）。通用模型为某个 agent 角色微调或蒸馏、但仍通过 agent 接口（工具、技能、代码、计划）行动的，也收，例如 GUAVA 把前沿 VLM agent 蒸馏成使用同一套工具的 4B agent。
- **不收**：具身大模型直接做动作，以及以这类模型为主要贡献的论文，不论其内部有没有推理链、子任务文本、memory 或自我纠错：VLA（OpenVLA、π0 / π0.5、ECoT、OneTwoVLA、MEM、Sentinel-VLA）、为低层策略协同训练的分层 VLA（Hi Robot、Steerable VLA、τ0-VLA、Gemini Robotics 1.5）、WAM、机器人或具身基础模型（PaLM-E、RoboBrain、GR00T）。它们只能作为被 agent 调用的工具出现，例如 Harness VLA 里 coding agent 调度冻结的 VLA。
- LLM 直接出动作和 VLA 的界线确实模糊，判断看**模型是什么**，不看输出是什么：通用模型直接出动作算，具身大模型出计划也不算。

### 2.1 三条判定

三条**全部满足**才算 agent。判定对象是「模型 + harness + 环」构成的过程，不是权重本身。

1. **显式决策**：输出可检查的离散决策，如计划、子任务、带参数的 skill / tool / VLA 调用、代码、约束、verdict（continue / stop / retry / ask / keep / revert）、对系统的编辑。
   标量分数、embedding、latent、action chunk 都不算。只输出这些的模型是「器官」（organ），如奖励模型、价值模型、打分器。
2. **决策权**：满足其一即可。
   - 备选项由模型自己生成，如计划、代码、调用参数。
   - 或者模型在选项中做选择，且其中至少有一个**控制行为**：stop、retry、replan、ask、keep / revert，或在异质 skill 之间切换。
   只在代码枚举的同类候选（哪个 frontier、哪个采样点）上打分，控制流归代码，不算。
3. **闭环**：满足下面两种形式之一。
   - **再决策**（re-decide）：同一次运行中，模型至少被再次调用一次；再次调用时，输入里有它**自己先前的决策记录**和这些决策的**后果证据**，并且可以修订先前的决策。例：Inner Monologue、Code-as-Monitor。
   - **编写闭环**（authored loop）：模型写出的可执行 artifact（约束、程序、在线优化的目标函数、监控条件、成功判据）在机器人执行时读取实时感知，并依据结果改变行为：重新求解、在阶段之间前进或回溯、断言失败后执行恢复动作、否决危险动作、检查失败后重试。随结果而变的那部分逻辑必须由模型写出；触发它的机制（求解器、回溯、重试循环）可以是固定框架。例：ReKep 的关键点约束以约 10 Hz 重新求解，路径约束被破坏时回溯到前一阶段；VoxPoser、Code as Policies（带感知反馈循环的程序）、ProgPrompt（带断言和恢复动作的程序）、Language to Rewards。
   后果证据须来自执行后的观测、工具返回、verifier 事件、训练或评测统计，或人类反馈。只来自模型自己的预测（world model、执行前的可行性检查）不够。
   **两种都不算**：artifact 的内容不随执行时的状态改变，例如一串技能名或地标、一次算出的抓取位姿或路点；一个计划交给各自闭环的技能去执行（那个环不是模型写的）；每步重新推理、但看不到自己先前决策的模型。（VLA 本身已按 §2.0 排除。）
   **两个例外（决策 8、9）**：约束 / 关键点编程类（模型写约束或代价函数交给求解器）和 agentic Real2Sim（模型重建可交互仿真场景）即使一次写成、不再闭环，也按 agent 收录，「闭环」一列记开环。见 §5 和 §6.1。
   Designer 和 Developer 的闭环仍要求依据训练或试验结果重新设计、重新修改（Eureka 迭代；一次写成的奖励或任务代码不算）。

**三个常见误区**
- RL 微调不等于 agency：SimpleVLA-RL 一类判 OUT。
- 架构内的 memory 不等于 agency：MemoryVLA 一类判 OUT。agent 自己读写的 memory 才计入。
- 多机器人不等于 multi-agent：一个 LLM 调度多台机器人（SMART-LLM），topology 记为 1:N。

---

## 3. 主轴：Seat（agent 坐在哪里）

判定依据是 agent 输出**在什么阶段产生**、**由谁消费**。

| Seat | 阶段 | 判定规则 | 代表论文 |
|---|---|---|---|
| **Controller** | 评测时 | agent 在评测 episode 中被调用，直接决定机器人下一步做什么。检验方法：假如什么失败都没发生，它的输出是否仍然改变机器人的行为？是 → Controller。 | SayCan、Inner Monologue、RoCo、Harness VLA、Show-Harness、Agent as Policy |
| **Supervisor** | 评测时 | 上述检验回答「否」：输出只在异常时起作用，如门控、否决、中断、恢复、重规划请求；并且检查过程独立于名义决策者。 | Code-as-Monitor、REFLECT、DoReMi |
| **Teacher** | 部署前 | agent 亲自执行、并经结果检验的行为（轨迹、恢复分支、playbook），成为部署模型的训练目标或冻结上下文。只做一次标注的模型不算 Teacher。 | GUAVA、RoboTwin 2.0 |
| **Designer** | 部署前 | agent 为学习者设计**问题**：reward、success、任务、环境、课程、评测套件。即使这些 artifact 经过迭代进化，也一律归 Designer。 | Eureka、DrEureka |
| **Developer** | 部署前 | agent 修改系统**本身**，即解题的一侧：被反复执行的策略代码、skill 库、harness、训练代码、超参、硬件。保留还是回滚，由它自己运行的实验决定。 | ENPIRE、RHO、HarnessPAI |

**容易混淆的三条界线**
- **Controller（lifelong）还是 Developer**：评测期间的自我改进归 Controller，打 lifelong 标；有独立的开发阶段，产物冻结后再评测，才归 Developer。论文没有报告阶段划分时，默认按 Controller 处理。
- **Developer 还是 Designer**：改「解法」归 Developer，改「题目」归 Designer。
- **Teacher 还是 Designer**：学生模仿的是 agent 自己做出的选择 → Teacher；agent 只决定练什么、留哪些数据 → Designer。

一篇论文可以有多个 seat。**主 seat** 取 headline 主张所依赖的那个，只用于章节归属；趋势统计以全部 seat 为单位。

---

## 4. 副轴：Carrier（通用模型原样使用还是改造过）

决策 12 之后，Carrier 只剩两类：

| Carrier | 含义 | 例子 |
|---|---|---|
| **G** | 通用模型原样使用（GPT、Gemini、Claude、开源 LLM / VLM），作者没有改它的权重 | SayCan、CaM、Harness VLA |
| **C** | 通用模型为某个 agent 角色微调或蒸馏，仍通过 agent 接口行动 | GUAVA 的 4B 学生（记作 G→C）、AgentVLN |

原来的 **H**（分层双系统、为低层协同训练）和 **I**（一个模型既决策又出动作）都属于具身大模型路线，按决策 12 不收。用户最初的「agency 在哪里」四类中，「外部编排」对应 G / C；「分层双系统」「内化」不再收录，只在正文作为对照；「multi-agent」改为 Topology 列。

Carrier 只剩两列后，Seat × Carrier 网格的信息量很小，副轴是否改用 Interface（技能调用 / 冻结 VLA / 代码 / 约束 / 直接动作 / 问题规格 / 系统编辑）待用户决定。

---

## 5. Controller 的三个子章

Controller 在候选中占一半以上，正文按以下三类拆分（原「训练过的 carrier」子章随决策 12 取消，C 类论文按功能归入下面三类）：

1. **编排型**（orchestrator）：调用 skill、tool 或 VLA-as-tool。例：SayCan、Harness VLA。
2. **直接驱动型**（direct driver）：输出语义微动作、原生指令、当下执行的代码或约束。例：Show-Harness、CaP-X、ReKep。这一子章也承接 robot-use agent 社区的命名。子章内部按闭环形式再分组：编写闭环（Code as Policies → VoxPoser → ReKep，模型写一次，程序或约束在执行中闭环）、再决策（CaP-X、Show-Harness，模型被反复调用），以及一次求解的约束 / 关键点编程（CoPa、MOKA 一类，决策 8 收录，闭环一列记开环）。
3. **lifelong / memory 型**：评测期间写入并读取 memory、skill 库或 harness，越用越好。

---

## 6. 核心表的层级

| 层级 | 条件 | 去向 |
|---|---|---|
| **CORE** | arXiv 首版在 **2026 年**；满足 §2 三条判定；有机器人身体；至少一个主要实验在真机或物理仿真中进行（失败可能由接触、滑动、碰撞等物理原因引起）；agentic 部分是论文 headline 的自变量。agentic Real2Sim 按 §6.1 的规则判定 | 核心表，按 Seat 分节；Real2Sim / Sim2Real 与 VLN 各自成章 |
| **先驱**（PIONEER） | arXiv 首版在 2022–2025 年的奠基作或代表作。满足 §2 三条判定的（如 SayCan、Code-as-Monitor、ReKep），和只满足判定 1、2 的开环工作（如 ZS-Planners、Socratic Models、CoPa）都可以收，用「闭环」一列区分 | 与 2026 年论文一起按 seat 呈现（决策 13）：每个 seat 先讲先驱，再讲 2026 |
| **BOUNDARY** | agent 成立，但只在离散或脚本化仿真中（ALFRED、AI2-THOR、VirtualHome、TDW、R2R 离散图、Habitat magic grasp）；或属于自动驾驶 | 边界一节讨论，lineage 表 |
| **RESOURCE** | benchmark、testbed、能力研究，被测对象是 agent | 单独的资源表 |
| **OUT** | 其余全部 | 不收录 |

**先驱的典型成员**：满足闭环的有 SayCan、Inner Monologue、Code as Policies、VoxPoser、ReKep、Eureka、REFLECT、Code-as-Monitor；不满足闭环、但开创了方向的有 ZS-Planners、Socratic Models、KnowNo、CoPa、RoboGen。具身大模型（PaLM-E、RT-2、ECoT、π0.5、Hi Robot）按决策 12 不收，只在正文作为对照。2026 年不满足闭环的论文不收录（约束编程与 agentic Real2Sim 两个例外除外）。

### 6.1 Real2Sim / Sim2Real 专题板块（子方向）

Real2Sim / Sim2Real 只是 Designer 与 Developer 下的一个子方向（用户 2026-10-08 指出）。核心表只收代表作，其余满足定义的论文进 README 的扩展列表。

agent 搭建、校准、利用仿真并把结果迁移到真机的工作，单独成节，但每篇仍标 Seat：

| 方向 | 做什么 | 通常的 Seat |
|---|---|---|
| Real2Sim | 从真实视频、扫描或数据集构建可交互的仿真世界、资产、铰接结构与物理参数（system identification） | Designer（构建「题目」） |
| Sim2Real | 设计 domain randomization、依据真机试验修正仿真器、把仿真中得到的技能或策略迁移并适配到真机 | Designer 或 Developer |
| Real2Sim2Real | 在重建的仿真里练习、自我改进，再回到真机（如 RPG、SimEX） | Developer（修改「解法」），次 seat Designer |

这类工作的评测（如 Video2World）进资源表，并在本节交叉引用。

**agentic Real2Sim 的判定（决策 9）**：基础模型 agent 为机器人任务重建或搭建可交互仿真，即从真实图像、视频或扫描出发，自己决定选哪些资产、摆放位姿、铰接结构、物理参数，或直接写仿真代码，重建结果用于机器人学习、数据生成或评测。这类工作一律进 CORE，Seat 记 Designer（重建后再改进解法的记 Developer），theme 记 real2sim。
- 构建过程通常是「渲染或仿真 → 与真实观测比对或检查可执行性 → 修改」，这本身满足 §2 第 3 条的闭环。
- 一次构建、不再迭代的 agentic 管线也收，「闭环」一列记 none，读者可以区分。
- 没有基础模型做构建决策的重建方法（Gaussian splatting、NeRF、经典 system identification）不算。

### 6.2 VLN 与具身导航章节（决策 11）

以导航为主任务的 agent 单独成章：vision-and-language navigation（VLN-CE、真机 VLN）、object-goal / instance 导航、长程导航与探索，Seat 多为 Controller。
- 2026 年的核心论文须在连续环境（Habitat VLN-CE、Isaac 等）或真机上评测。
- R2R 离散图上的开创性 VLN agent（如 NavGPT、MapGPT）只作为先驱收录，「Body」一列标出离散仿真，正文在边界一节讨论。
- 导航中顺带有操作的移动操作任务仍归 Controller 各子章。

---

## 7. 明确不算

| 情形 | 例子 |
|---|---|
| 具身大模型直接做动作（决策 12）：VLA，包括带推理链、子任务、memory、自我纠错的；为低层协同训练的分层 VLA；WAM；机器人或具身基础模型 | π0.5、ECoT、OneTwoVLA、MEM、Sentinel-VLA、Hi Robot、Steerable VLA、τ0-VLA、Gemini Robotics 1.5、PaLM-E、RoboBrain |
| 反应式 VLA，包括 RL 微调的 | OpenVLA、π0、RT-1、SimpleVLA-RL |
| 潜变量双系统；只在网络结构或控制频率上叫 hierarchical | GR00T N1、Helix、HiRT、RoboDual |
| 输出是标量的打分器、奖励模型、价值或进度模型 | RoboMonkey、GVL、VLAC、RL-VLM-F |
| 只做一次标注或重标注的 FM（annotator ≠ teacher） | DIAL、ECoT 的标注管线 |
| 中间表示是对世界的预测（归 WAM survey） | CoT-VLA、DreamGen、HiP |
| 没有机器人身体的世界 | Voyager（Minecraft）、文本世界、网格世界 |
| 纯数字 agent、机器人只是仪器 | Web / GUI / OS agent；Coscientist |
| 只在离线数据上评测的 judge 或 embodied-brain 模型 | AHA、RoboBrain（无闭环实验时） |

---

## 8. 正交的 anatomy 列（核心表的列）

| 列 | 取值 |
|---|---|
| Seat | 主 seat 加粗，另列次 seat |
| Carrier | G / C；可用箭头表示迁移，如 GUAVA 记作 G→C |
| Interface | skill-tool 调用 / VLA-as-tool / 微动作 / 代码 / 约束与 objective / verdict 与纠正 / 执行轨迹与 playbook / 问题规格（reward、env、task）/ 系统编辑 |
| Topology | ×1 单 agent / ×R 多角色共享一个任务 / ×N 每个身体一个 agent / 1:N 一个决策者对多个身体 / ×O 多 agent 分头负责 |
| Closure | 闭环形式：再决策 / 编写闭环；证据来源：E 执行观测、H 人类反馈；cadence：step / subgoal / episode / training-run / experiment |
| Body | 形态与领域：manip / nav / mobile-manip / loco-humanoid / aerial / multi-robot；sim / real |

harness 和 multi-agent 都不是类别：harness 属于 Interface，multi-agent 属于 Topology。

---

## 9. 主线

原主线：***"Agency spreads around the body — and loop closure, not weights, makes a carrier an agent."***

决策 12 之后，「not weights」不再成立：研究对象限定为通用大模型。主线待用户确认，候选：

- ***"General models become embodied agents through the loops built around them — and agency spreads around the body, seat by seat."***
- ***"Agency spreads around the body: general models, not embodied action models, fill seat after seat."***

agency 没有从机器人身上迁走，而是在身体周围逐个占据新的 seat：

| 年份 | 新出现的 seat |
|---|---|
| 2022 | Controller |
| 2023 | Supervisor、Designer |
| 2024 | Developer |
| 2025 | Teacher |
| 2026 | 五个 seat 全部有人占据 |

一个通用模型能不能坐进某个 seat，取决于它在 harness 里是否做显式决策、并且闭环：要么带着自身记录、依据后果再决策，要么它写出的约束或程序在执行时依据后果调整。这条脉络从 2022 年的先驱开始（SayCan、Code as Policies、Inner Monologue），在 2026 年铺满五个 seat。

> 注：上述时间线与比例来自有偏的测试集（按方向搜集，2026 年偏多），**必须在最终核心集上重算**后才能写进正文。

---

## 10. 边界一节要讨论的内容

- **自动驾驶**：闭环驾驶 agent（CARLA、实车）和 open-loop 日志评测的工作，都只在边界一节讨论，不进核心。
- **离散仿真**：ALFRED、AI2-THOR、VirtualHome、TDW、R2R 离散图上的 agent（LLM-Planner、CoELA、NavGPT 等）进入 lineage 表。正文需明说：这使 multi-agent 方向在核心集中偏薄。
- **与 WAM / VLA 的分界**：决策者是具身大模型（VLA、WAM、机器人基础模型）的，归 WAM / VLA 方向，本文只作对照；决策者是通用大模型、把 VLA 或 world model 当工具调用的，归本文。
