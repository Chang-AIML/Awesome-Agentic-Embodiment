# Agentic Embodiment：定义与分类（正文版）

> 本文是正文用的简化版。细则（A0–A3 全文、Λ 阶梯、E/H/M closure、tier 规则、逐案例论证）保留在
> `definition_draft.md`，作为附录和标注指南。两者冲突时，以本文为准。
>
> 2026-10-07 用户确认的四项决策：
> 1. 主框架采用 **Seat × Carrier**；
> 2. 开环奠基作进入核心表，标为 **前驱（precursor）**；
> 3. 核心集约 **60 篇**，benchmark 与资源另列一张表；
> 4. 自动驾驶与离散仿真**不进核心**，只在边界一节讨论。

---

## 1. 一句话定义

*Agentic Embodiment studies foundation-model-driven processes that make explicit decisions whose
consequences reach a robot body, and that re-decide on evidence of those consequences. Its organizing
question is where such a process sits relative to the body's deployed policy — steering it, guarding
it, teaching it, designing its learning problem, or building its system (**Seat**) — and which weights
carry it (**Carrier**).*

中文：Agentic Embodiment 研究的是由基础模型驱动、能做出显式决策的过程。这些决策的后果会作用到机器人身体上，而过程会依据后果的证据重新决策。全文围绕一个问题组织：这个过程相对于机器人部署的策略坐在哪里（**Seat**），由哪类权重承载（**Carrier**）。

**推论**：agentic embodiment 不等于 agentic robot。ENPIRE 部署出去的策略里没有 agent，但它仍是核心样本，因为 agent 坐在 Developer 的位置。

---

## 2. 什么算 agent：三条判定

三条**全部满足**才算 agent。判定对象是「模型 + harness + 环」构成的过程，不是权重本身。

1. **显式决策**：输出可检查的离散决策，如计划、子任务、带参数的 skill / tool / VLA 调用、代码、约束、verdict（continue / stop / retry / ask / keep / revert）、对系统的编辑。
   标量分数、embedding、latent、action chunk 都不算。只输出这些的模型是「器官」（organ），如奖励模型、价值模型、打分器。
2. **决策权**：满足其一即可。
   - 备选项由模型自己生成，如计划、代码、调用参数。
   - 或者模型在选项中做选择，且其中至少有一个**控制行为**：stop、retry、replan、ask、keep / revert，或在异质 skill 之间切换。
   只在代码枚举的同类候选（哪个 frontier、哪个采样点）上打分，控制流归代码，不算。
3. **闭环**：同一次运行中，模型至少被再次调用一次；再次调用时，输入里有它**自己先前的决策记录**和这些决策的**后果证据**，并且可以修订先前的决策。
   后果证据须来自执行后的观测、工具返回、verifier 事件、训练或评测统计，或人类反馈。只来自模型自己的预测（world model、可行性检查）不够。

**三个常见误区**
- RL 微调不等于 agency：SimpleVLA-RL 一类判 OUT。
- 架构内的 memory 不等于 agency：MemoryVLA 一类判 OUT。agent 自己读写的 memory 才计入。
- 多机器人不等于 multi-agent：一个 LLM 调度多台机器人（SMART-LLM），topology 记为 1:N。

---

## 3. 主轴：Seat（agent 坐在哪里）

判定依据是 agent 输出**在什么阶段产生**、**由谁消费**。

| Seat | 阶段 | 判定规则 | 代表论文 |
|---|---|---|---|
| **Controller** | 评测时 | agent 在评测 episode 中被调用，直接决定机器人下一步做什么。检验方法：假如什么失败都没发生，它的输出是否仍然改变机器人的行为？是 → Controller。 | SayCan、Inner Monologue、RoCo、Harness VLA、Show-Harness、OneTwoVLA |
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

## 4. 副轴：Carrier（决策由哪类权重承载）

找到掌握任务级控制流的最高层决策者，然后依次判断：

| Carrier | 含义 | 例子 |
|---|---|---|
| **G** | 作者没有对其权重做具身训练的通用模型（GPT、Gemini、Claude、开源 LLM / VLM 原样使用） | SayCan、CaM、Harness VLA |
| **I** | 同一个训练过的模型既输出显式决策，又输出动作 | OneTwoVLA |
| **H** | 训练过的决策者，配一个**为它协同设计**的学习型执行器（执行器的输入接口就是决策者的输出词表，且在同一工作中训练） | Hi Robot |
| **C** | 训练过的决策者，配通用执行器（现成 skill、规划器、通用速度接口） | PaLM-E、Guava-4B |

**中心图**是 Seat × Carrier 网格。用户最初的「agency 在哪里」四类，对应 Controller 一行的四列：

| 最初四类 | 现在的位置 |
|---|---|
| 外部编排 | Controller-G / C |
| 分层双系统 | Controller-H（只收显式决策的版本，潜变量双系统判 OUT） |
| 内化 | Controller-I |
| multi-agent | 不再是类别，改为 Topology 列，可出现在任何 seat |

---

## 5. Controller 的四个子章

Controller 在候选中占一半以上，正文按以下四类拆分：

1. **编排型**（orchestrator）：调用 skill、tool 或 VLA-as-tool。例：SayCan、Harness VLA。
2. **直接驱动型**（direct driver）：输出语义微动作、原生指令或当下执行的代码。例：Show-Harness、CaP-X。这一子章也承接 robot-use agent 社区的命名。
3. **lifelong / memory 型**：评测期间写入并读取 memory、skill 库或 harness，越用越好。
4. **训练过的 carrier**：Carrier 为 C / H / I。例：PaLM-E、Hi Robot、OneTwoVLA。

---

## 6. 核心表的层级

| 层级 | 条件 | 去向 |
|---|---|---|
| **CORE** | 满足 §2 三条判定；有机器人身体；至少一个主要实验在真机或物理仿真中进行（失败可能由接触、滑动、碰撞等物理原因引起）；agentic 部分是论文 headline 的自变量 | 核心表 |
| **PRECURSOR** | 奠基或高影响的工作，满足判定 1 和 2，但不满足闭环（判定 3）：一次写出程序或约束后模型不再被调用、每步决策但没有自身记录、或只有模型预测的后果 | 核心表，标 precursor，趋势统计时单列 |
| **BOUNDARY** | agent 成立，但只在离散或脚本化仿真中（ALFRED、AI2-THOR、VirtualHome、TDW、R2R 离散图、Habitat magic grasp）；或属于自动驾驶 | 边界一节讨论，lineage 表 |
| **RESOURCE** | benchmark、testbed、能力研究，被测对象是 agent | 单独的资源表 |
| **OUT** | 其余全部 | 不收录 |

**PRECURSOR 的典型成员**：Code as Policies、VoxPoser、ReKep、ProgPrompt、Socratic Models、ZS-Planners（Language Models as Zero-Shot Planners）、ECoT、π0.5、KnowNo、AutoRT、Text2Motion。核心表只收其中约 6 篇最奠基的；其余不满足闭环的工作进入 lineage 表，或不收录。

---

## 7. 明确不算

| 情形 | 例子 |
|---|---|
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
| Carrier | G / C / H / I；可用箭头表示迁移，如 GUAVA 记作 G→C |
| Interface | skill-tool 调用 / VLA-as-tool / 微动作 / 代码 / 约束与 objective / verdict 与纠正 / 执行轨迹与 playbook / 问题规格（reward、env、task）/ 系统编辑 |
| Topology | ×1 单 agent / ×R 多角色共享一个任务 / ×N 每个身体一个 agent / 1:N 一个决策者对多个身体 / ×O 多 agent 分头负责 |
| Closure | 证据来源：E 执行观测、H 人类反馈；cadence：step / subgoal / episode / training-run / experiment |
| Body | 形态与领域：manip / nav / mobile-manip / loco-humanoid / aerial / multi-robot；sim / real |

harness 和 multi-agent 都不是类别：harness 属于 Interface，multi-agent 属于 Topology。

---

## 9. 主线

***"Agency spreads around the body — and loop closure, not weights, makes a carrier an agent."***

agency 没有从机器人身上迁走，而是在身体周围逐个占据新的 seat：

| 年份 | 新出现的 seat |
|---|---|
| 2022 | Controller |
| 2023 | Supervisor、Designer |
| 2024 | Developer |
| 2025 | Teacher |
| 2026 | 五个 seat 全部有人占据 |

一个模型能不能坐进某个 seat，取决于它是否闭合了「带着自身记录、依据后果再决策」的环，与它是哪套权重、多大规模无关。

> 注：上述时间线与比例来自有偏的测试集（按方向搜集，2026 年偏多），**必须在最终核心集上重算**后才能写进正文。

---

## 10. 边界一节要讨论的内容

- **自动驾驶**：闭环驾驶 agent（CARLA、实车）和 open-loop 日志评测的工作，都只在边界一节讨论，不进核心。
- **离散仿真**：ALFRED、AI2-THOR、VirtualHome、TDW、R2R 离散图上的 agent（LLM-Planner、CoELA、NavGPT 等）进入 lineage 表。正文需明说：这使 multi-agent 方向在核心集中偏薄。
- **与 WAM 的分界**：中间表示是对世界的预测，归 WAM；是决策，归本文。world model 作为 agent 的工具、同时有执行闭环的系统，归本文。
