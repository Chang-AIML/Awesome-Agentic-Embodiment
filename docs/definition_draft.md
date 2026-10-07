# Agentic Embodiment：定义与分类（修订终稿）

> **主线不变**：问的仍是「agency 在哪里」。本稿把它落成一个可以逐条核对的坐标 **(Seat, Carrier)**：
> - **Seat**：agent 相对于目标策略，闭合的是哪一个环。
> - **Carrier**：决策由哪一类权重承载。
>
> 部署后执行器端还剩下什么（**Residual**），只作为一列记录，不再作为第二个视图。
>
> **本轮修订解决的问题**：
> - 用 *production phase* 判 seat；
> - 把 problem/solution 的切分写进判定程序；
> - 用一条统一原则判 A2；
> - 引入 E/H/M 三种 closure 类型；
> - 把 Λ 拆成两个字段：closure 强度和 cadence；
> - 新增 CORE-P 与 UNRESOLVED 两个层级；
> - 保真度改用 primitive-realization 判据；
> - 改用 seat 向量作为统计单位；
> - 主线论点收窄。
>
> 测试集共 353 条，去重后 350 条，全部按本稿规则重新判定。所有计数都由这份判定表算出。

---

## 1. 一句话定义

**Canonical (EN).** *Agentic Embodiment studies foundation-model-driven processes that make explicit decisions whose consequences reach a robot body, and that re-decide on evidence of those consequences. Its organizing question is where such a process sits relative to the body's deployed policy — steering it, guarding it, teaching it, designing its learning problem, or building its system (**Seat**) — and which weights carry it (**Carrier**).*

**中文解释**
- **Foundation-model-driven process**：判定对象是由模型、harness 和环共同构成的*过程*，而不是权重本身。同一族 Qwen3.5 小模型，放进 GUAVA 的 harness 是 agent（Guava-4B）；放在 Show-Harness 的单 token 模式下（0.8B–9B LoRA）就只是反应式策略。
- **Explicit decisions … re-decide on evidence**：§2 的 A1–A3 三条全部满足才算 agent。证据可以是执行后观测到的（E）、人提供的（H），或模型预测出来的（M）。进入 CORE 至少需要一次 E 或 H closure。
- **Robot body**：必须有机器人形态，至少一个 headline 实验达到 F2（失败可能由物理原因引起的仿真）或 F3（真机），见 §3 C4。
- **Seat**：按 agent 输出的*产生阶段*和*消费方式*确定（§5），一共 5 个：Controller、Supervisor、Teacher、Designer、Developer。
- **Carrier**：分四类，G（未经具身训练的通用模型）、C、H、I（§5.3）。初稿的四个 locus 就落在 Controller 这一行的四列里。
- **推论**：agentic embodiment 不等于 agentic robot。ENPIRE 部署出去的策略里没有 agent，但它仍属于本领域的核心样本。

**明确不算**（细则见 §4）：
- 反应式 VLA，包括经 RL 微调的；
- 潜变量形式的双系统；
- 只做一次标注或重标注的 FM（annotator ≠ teacher）；
- 输出只是标量的打分器、奖励模型、价值模型（organ）；
- 没有机器人身体的世界，如 Minecraft 或文本世界；
- 纯数字 agent；
- 把机器人当作仪器的系统；
- 中间表示只是对世界的预测（foresight），这部分归 WAM survey。

---

## 2. 什么是 "agent"（可操作判定）

**判定单位是 coupling**，即 (agent, output, consumer, production phase)。A1–A3 **逐个 coupling 检查**。承载 headline 的那个 coupling 本身必须满足这三条。系统中其他地方存在的 retry 不能拿来充数：RoboGen 只在资产验证环节有 retry，因此判 B-loop。

### 2.1 A0 输出类型检查（先于 A1）

模型输出若只是以下几类，它就是 **organ**（器官）或执行器，不是决策者：
- 标量、分数、偏好；
- embedding、latent；
- 电机指令或 action chunk。

**例**：RoboMonkey、V-GPS、GVL、VLAC、RL-VLM-F 都是 organ，判 OUT；只有当另一个 agent 消费它们时，才会出现在 anatomy 中。

**Decodable latent**：只有当解码后的形式正是消费方收到的内容，或者会作为决策记录重新输入模型时，才算显式决策。所以 Fast-ThinkAct 判 OUT，ThinkAct 的显式推理算数。

### 2.2 A1 Explicit decision

运行时输出可检查的离散决策。允许的形式：
- subtask 或指令；
- skill / tool / policy call（带参数）；
- 代码；
- 约束、spec、reward 程序；
- verdict，如 continue / stop / retry / ask / keep / revert；
- 发给他人的消息；
- memory 写入；
- 对系统的编辑；
- 命名的语义动作单元；
- 点或路点。

### 2.3 A2 Decision authority（统一原则）

下面两条**满足其一**即可：
- **(a) 生成式**：备选项由模型自己写出，例如计划、子任务文本、带参数的调用、代码、带理由的 verdict、编辑。
- **(b) 选择式 + 控制行为**：模型在枚举的选项中做选择，并且至少有一个选项或输出是**控制行为**：stop/done、retry、replan/abandon、ask/escalate、keep/revert、think-vs-act，或者在*异质能力*之间切换（选哪种 skill、tool 或 policy）。
  - 对模型自己给出的分数取 argmax 或阈值，算作模型的选择。分数与固定函数组合后再选（即 *composed decider*，如 SayCan 的 LLM×affordance）也算。

**判失败**：模型只在代码枚举的**同一类动作的参数**（哪个 frontier、哪个点、哪个采样候选）上打分或挑选，而循环的控制流完全归代码所有。此外，**人从模型给出的选项中挑选**时，这一步的决策归人，不归模型。

| 论文 | (a) 生成 | (b) 控制行为 | 判定 |
|---|---|---|---|
| SayCan | 否 | 在异质 skill 之间选择，且 'done' 是可选项 | 通过 |
| KnowNo / IntroPlan | 是，选项由 LLM 生成 | — | A2 通过；A3 失败，见 2.4 |
| Eureka / MEMENTO / REvolve / RoboMorph | 是，写出候选代码或形态 | — | 通过（即使外层脚手架是固定的） |
| SG-Nav / UniGoal / Co-NavGPT | 否，frontier 由代码生成 | 终止和阶段切换由代码决定 | **B-auth** |
| PIVOT | 否，候选点由代码采样 | CEM 的轮数固定 | **B-auth** |
| FOREWARN | 否，在策略的候选中挑选 | 没有 veto、stop 或 replan | **B-auth** |
| RoboMonkey | — | 输出是标量 | **A0 → OUT (organ)** |
| VLFM / OK-Robot | — | 输出是 value map，或属于固定管线 | **OUT** |

### 2.4 A3 Consequence-conditioned re-decision

- **Loop instance（环实例）**：agent 的决策记录持续存在的那段跨度，可以是一个 episode、一次训练或搜索 run、一个研究 campaign。
- **要求**：同一个环实例里，模型至少被调用两次。后一次调用必须同时满足：
  - **(i)** 模型输入中有一份可解码的**自身 A1 类决策记录**，例如计划、调用历史、verdict、子任务输出、memory 写入记录、编辑记录、git 历史。
    - 以下不算：只有过去的观测帧、架构内的 latent memory、KV cache、action chunk 历史，以及按定时器刷新的缓存思维（这一类记为 Λ1s）。
  - **(ii)** 关于这些决策**后果**的证据。证据可以直接写进模型输入，也可以通过 composed decider 在决策后的状态上计算。SayCan 属后一种：affordance 在执行后的新状态上计算。
  - **(iii)** 后一次输出能够修订先前的决策，例如 retry、replan、abandon、keep/revert。
- **证据（closure 类型）**：
  - **E (executed)**：执行后的观测；工具返回值（工具作用于真实世界，或作用于由本体自身感知构建的地图或记忆，记作 E-tool）；verifier 或 monitor 事件；训练或评测统计。
  - **H (human)**：模型*整合*的人类输入，包括执行报告、澄清、纠正。人类**直接替代**模型决策的情况不算，例如 YAY Robot、RT-H 中人直接覆盖输出，或 KnowNo 中由人挑选选项。
  - **M (model-predicted)**：执行前由模型预测的后果，例如 Q 值或可行性判断、motion planner 或约束采样器的检查、场景图模拟器、world-model 的想象。
  - **不算证据**：同伴 LLM 的意见或辩论消息本身。
- **CORE 门槛**：closure 强度 ≥2，并且在被评测的设置中至少有一次 E 或 H closure。只有 M 的论文判 **B-loop (M-only)**，如 Text2Motion、PRoC3S、LLM3、ReflectVLM。
- **与 WAM 的分界**：world model 作为 M 工具使用，同时又有 E 闭环的系统，归本文；执行器直接消费的中间表示是预测结果（HiP、CoT-VLA），或者只是在预测上做搜索、没有 FM 决策者的系统（Hume、VLA-Reasoner），归 WAM 或 VLA survey。

### 2.5 Closure 强度与 cadence 是两个字段

**Closure 强度**（决定 tier）

| 值 | 含义 | 例 |
|---|---|---|
| Λ0 | 每个环实例只做一次决策 | LM-Nav、TidyBot、HAMSTER、Mobility VLA |
| Λ1 | 每一步重新生成显式决策，但没有自身记录 | ECoT、π0.5、NaVILA、RT-H |
| Λ1s | 带着记录，但记录按计划刷新，不由结果驱动 | Fast ECoT |
| Λ1' | authored loop：模型一次写出闭环 artifact，之后不再被调用 | Code as Policies、VoxPoser、ReKep、RoboGuard、SUDD |
| Λ2 | 带自身记录、基于后果再决策 | SayCan（weak）、FIND、RoboMorph |
| Λ3 | 显式的成败或违例判断驱动 retry / replan / ask / revert | Inner Monologue、CaM、GUAVA、OneTwoVLA |

**Cadence**（单独记录，与强度无关）

| 取值 | 例 |
|---|---|
| step / primitive / subgoal / event | 运行时环 |
| episode | 逐 episode |
| training-run | Eureka |
| experiment | ENPIRE |

另加 **scaffold 标**：fixed（Eureka）或 open（ENPIRE）。初稿中的 Λ4 取消，原来的 Λ4a/4b 改写为「closure≥2，cadence = experiment，scaffold = fixed/open」。

### 2.6 三条裁定

- RL ≠ agency：SimpleVLA-RL、RoboCat、EVOLVE-VLA 判 OUT。
- memory ≠ agency：MemoryVLA、SAM2Act 判 OUT。由 agent 自己读写的 memory 计入 anatomy。
- multi-robot ≠ multi-agent：SMART-LLM 是 1:N（一个决策者对多个身体）。

---

## 3. 纳入契约（Inclusion contract）

1. **C1 FM decider.** A pretrained LLM/VLM/VLA, or a model fine-tuned/distilled/RL-trained from one, emits A1 decisions (after the A0 output-type check).
   中文：方法中要点名所用模型，并给出它的输出样例。
2. **C2 Authority.** A2 holds for the load-bearing coupling.
3. **C3 Loop.** A3 holds at closure ≥2 with ≥1 E or H closure *in the evaluated setting*, not merely in demos.
4. **C4 Robot body & fidelity.** The body has a robot morphology, and ≥1 headline experiment is F2 or F3.
   中文：
   - **机器人形态条款**：包括机械臂（含抽象为平面推杆的末端执行器，如 Push-T）、移动底盘、足式、人形、空中平台、在闭环中受控的道路车辆、社交机器人、多机器人。LunarLander、Minecraft 化身、文本或网格中的 token 都不算。
   - **F3**：真机。
   - **F2**：仿真，并且 agent 所选原语的**结果可能因 agent 未建模的物理原因偏离意图**，如接触、滑动、碰撞阻挡、动力学。允许使用 privileged state。
   - **F1**：有度量空间和类机器人身体，但原语结果是脚本化的，如瞬移、magic grasp、symbolic primitives、离散视点图。
   - **F0**：符号、文本、网格或 API，没有度量空间的具身。
   - **逐个判定**：
     - GUAVA（MuJoCo 中有注入的漏抓和掉落）判 F2+F3。
     - Show-Harness（interpreter → 阻抗或关节控制）判 F2+F3。
     - CaP-X（robosuite/LIBERO）判 F2。
     - FAEA（privileged-state API）判 F2，但原语是否物理实现待审计。
     - OmniGibson：motion-planned 的 semantic primitives 判 F2；symbolic primitives（Octopus、COHERENT）判 F1。
     - TDW transport（CoELA、COMBO）判 F1。
     - Habitat：VLN-CE 连续导航会被碰撞阻挡，判 F2；rearrangement 中的 magic grasp（EMOS、Ask-to-Act、Housekeep）判 F1。
     - AI2-THOR / ALFRED / TEACh / VirtualHome 判 F1。
     - R2R 离散图判 F1。
     - Ravens/CLIPort suction（PyBullet）判 F2。
     - 驾驶：open-loop 日志评测不满足 C5；CARLA 一类闭环评测判 F2。
5. **C5 Causal reach.** In reported experiments the agent's decisions change what the body does, at runtime or via artifacts the body later executes or is trained/evaluated on.
   中文：Designer 必须在论文中有一个作用在机器人身体上的消费者；SceneWeaver 没有，判 OUT。只在离线数据上评测的 judge 判 OUT。
6. **C6 Embodied objective.** The loop optimizes the body's own capability (success, robustness, efficiency, safety, generality, incl. information-seeking tasks the body performs).
   中文：Coscientist 把机器人当作仪器，判 OUT。
7. **C7 Centrality.** The agentic coupling is the independent variable of the headline claim (abstract / contribution list) or a primary evaluated condition.
   中文：只作为 baseline 出现，判 OUT。

**Tiers（每条论文只能取一个）**

| tier | 条件 | 计数 |
|---|---|---|
| **CORE** | C1–C7 全部满足，且关键细节由描述级以上的证据支持 | 70 |
| **CORE-P** (provisional) | 依据现有描述可以判通过，但至少有一个关键细节尚未确立（A2 控制行为、A3 自身记录或 closure 类型、原语实现、阶段划分、carrier）。所有表格都分开报告 | 55 |
| **BOUNDARY** | 有机器人身体，F≥1，C1/C5/C6/C7 满足，但存在短板：**B-auth**（A2 失败）、**B-loop**（A3 失败：Λ0/1/1s/1'、M-only，或单次调用的在环 judge）、**B-world**（agent 成立，但最好的实验只到 F1）。进入同列结构的 lineage/neighbour 表 | 76 / 7 / 17 |
| **RESOURCE** | 被测对象是 agent 的 benchmark、testbed、能力研究、受控设计空间研究，标出 evaluated seat 和保真度。论文自带方法满足 C1–C7 时，CORE 优先 | 7 |
| **UNRESOLVED** | 只有 list、title 或博客级证据，或者无法判断决策过程是否为 agent。进入审计队列，**保留在分母中**，不能判 CORE | 39 |
| **OUT** | 其余全部，标注排除类别；"history-only" 表示只在谱系叙事中引用 | 79 |

**其他记账规则**
- **证据等级列（必填）**：full-text / abstract / description / list / title / blog / memory。list 及以下的证据不得进入 CORE 或 CORE-P。
- **版本与年份**：seat 按钉住的 arXiv 版本判；年份一律取 arXiv v1。例如 CaM 记为 2024（会议是 CVPR 2025），两者都注明。
- **人在外环中的控制份额**：Teacher、Designer、Developer 判 CORE 时，至少要有一个被报告的 campaign 由 agent 在没有人选择的情况下自主选定下一个实验或编辑。ENPIRE 的第二阶段满足；Project Fetch 是能力研究，判 RESOURCE。

---

## 4. 边界：明确排除 / 边界案例

| 情形 | 判定 | 理由 | 例子 |
|---|---|---|---|
| 纯反应式 VLA（含 RL 微调） | OUT（作为执行器底座引用） | A1 不满足；RL ≠ agency | OpenVLA、π0、SimpleVLA-RL、RoboCat、EVOLVE-VLA |
| VLA 的 CoT 只是边缘实验条件 | OUT | 不满足 C7 | RT-2 |
| 潜变量双系统；只在网络结构或控制频率上叫 "hierarchical" | OUT | 没有可检查的决策 | GR00T N1、Helix、HiRT、RoboDual、LCB、OpenHelix、Fast-in-Slow、LeVERB、TriVLA、HiMoE-VLA、RDP |
| 运行时推理只以 latent 存在；架构内的 memory | OUT | 不满足 A0/A1 | Fast-ThinkAct、MemoryVLA、SAM2Act、RAEA |
| 中间表示是 foresight；world-model RL；没有 FM 决策者的搜索 | OUT，交给 WAM 或 VLA survey | 规则是 dream vs decide | CoT-VLA、FlowVLA、DreamVLA、HiP、WMPO、VLA-RFT、DreamGen、Hume、VLA-Reasoner、World-Env |
| world model 作 M 工具，同时有 E 闭环 | 本文范围，M 记入 closure 列 | 以决策者是否掌控环、是否有 E closure 为准 | Robo-Cortex（world-model 验证，属 M） |
| 无状态的推理 VLA；反应式显式层级 | B-loop，neighbour 章节 "reasoning-augmented policies" | A1、A2 满足，A3 不满足 | ECoT、π0.5、RT-H、MolmoAct(2)、DeepThinkVLA、EO-1、NaVILA、DualVLN、Fast ECoT、AutoVLA |
| 单次规划、单次程序或 spec（Λ0/Λ1'），F≥1 | B-loop，lineage 表 | 模型从未因后果被重新调用 | Code as Policies、VoxPoser、ReKep、ProgPrompt、Instruct2Act、RoboTool、LM-Nav、Socratic Models、SMART-LLM、LaMMA-P、ZSP（F1）、TidyBot |
| 只有 M closure（规划期可行性检查） | B-loop (M-only) | 没有 E 或 H closure | Text2Motion、PRoC3S、LLM3、ReflectVLM |
| 只在代码枚举的同类候选上选择，控制流归代码 | B-auth | A2 不满足 | SG-Nav、UniGoal、Co-NavGPT、PIVOT、FOREWARN、COMBO、VLA-Corrector |
| 输出是标量的打分器、奖励、价值或进度模型 | OUT (organ) | 先在 A0 判掉 | RoboMonkey、V-GPS、RoVer、GVL、VLAC、RL-VLM-F、RoboCLIP、VLM-RMs、ReWiND、Robometer、Robo-Dopamine、RoboFuME、SuccessVQA |
| 输出 verdict，但只在离线评测 | OUT (organ) | 不满足 C5 | AHA、Guardian、SAFE、Sentinel、LLM semantic anomaly monitor |
| 输出 verdict，单次调用，在环内门控执行 | B-loop（作为 organ-in-loop） | Λ0/1 | StageGuard、RoboFAC、FailSafe、FPC-VLA、AESOP、PROTEA、FLARE |
| 标注器、重标注器，或给生成模型写 prompt | OUT（annotator ≠ teacher） | 不行动，也不观察结果 | DIAL、SPRINT、CAST、VLM-HER、LucidSim；ECoT、Emma-X、Hi Robot、StageGuard 的 teacher 管线 |
| 一次生成**可执行**的 reward、env、task、cost 代码，或执行后由管线过滤 | B-loop，作为 Designer / Teacher 的 lineage | 产物是可执行代码，所以区别于 annotator；但没有 Λ2 | SUDD、BLAZER、GenSim(2)、RoboGen、Gen2Sim、Holodeck、ARCHIE、Text2Reward（主设置）、GRAPE、GenManip、AutoRT、SOAR |
| agent 成立，但只到 F1 | B-world，lineage 表 | 后果由脚本决定 | NavGPT、MapGPT、DiscussNav、LLM-Planner、HELPER、Embodied-Reasoner、CoELA、EMOS、COHERENT、Octopus、ICAL、RECOVER、NavCoT、LangNav |
| 没有机器人身体（游戏化身、文本、网格、LunarLander），或 F0 | OUT（history-only） | 不满足机器人形态条款 | Voyager、JARVIS-1、LEAP、Embodied Planner-R1、OMNI、HMAS-2、LLM+P、Robo-Instruct、Code Evolution for Control |
| 有 agent 的 builder，但论文内没有具身消费者 | OUT（一旦耦合到学习者即判 Designer） | 不满足 C5 | SceneWeaver |
| LLM 只辅助人类编写；治理层或 harness 中没有决策 agent | OUT（引用于 anatomy 和 permission surface） | 没有决策者 | RoboCasa、Harness Engineering for Physical AI、AEROS、AutoEval、Habitat 3.0 |
| embodied-brain FM 只在离线 benchmark 上评测 | OUT 或 UNRESOLVED（作为 carrier 底座） | 不满足 C5，除非论文自己做了作用在身体上的闭环实验 | ME-VLM（UNRESOLVED） |
| 人类参与闭环 | 人整合进来的输入记为 H，算证据；人替代模型决策不算 | integrate ≠ replace | H：L2R、REvolve、DROC、ChatGPT for Robotics；替代：YAY Robot、RT-H、KnowNo 由人挑选选项 |
| 只有人有 agency；只有 MARL、没有审议 | OUT | 不满足 C1–A3 | Interactive Language、GauDP |
| 机器人只是仪器 | OUT | 不满足 C6 | Coscientist precursor |
| 纯数字世界 | OUT | 不满足 C4 | Harness-Zero |
| benchmark、testbed、能力研究、设计空间研究 | RESOURCE（标 evaluated seat 和 F） | 没有自有方法 | RLE-Bench、LIBERO-Agent、PARTNR (F1)、Virtual Community (F1)、Project Fetch、Claude Plays Robotics、VLA-OS（controlled-study） |
| agent runtime 或 OS | 控制路径上有决策 agent，且报告了任务评测，按 seat 规则判；否则判 RESOURCE | 一条规则统一处理 | ROSClaw、RoboOS、ABot-Claw（均为 CORE-P Controller） |
| 驾驶 | 与其他领域用同一套规则：open-loop 日志判 OUT；闭环评测按 Λ 判 | 不再按领域直接排除 | AutoVLA、Alpamayo-R1（B-loop, Λ1）、AESOP（B-loop） |
| survey | OUT | 只用于和本文作区分 | No Free Checker、Self-evolving Embodied AI |

---

## 5. 主轴 taxonomy：Agency Locus = Seat × Carrier

### 5.1 判定单元

- **Target policy**：在 headline 评测中，其输出到达执行器的那个组件。
- **Deployed stack S**：位于确定性解释器之上的决策栈。确定性解释器包括 IK、阻抗或伺服控制、固定增量映射。
- **Production phase**（按 coupling 判；判的是 agent *何时被调用*来产出这个输出，不是这个输出何时被消费）：
  - **runtime**：agent 在报告的评测 episode 中被调用。lifelong 或 test-time 协议下，如果报告的指标是在改进过程中累积的，那么 episode 之间的调用也算 runtime。
  - **pre-evaluation**：agent 在与报告评测分离的 episode 或 run 中被调用，产物冻结后用于评测或部署。包括：采集数据、练习、测试候选版本、搜索奖励、研究迭代。agent 即使在这些 episode 里真的驱动了机器人，也算这一阶段（AutoRT 的采集、ENPIRE 的复位与练习）。
  - **默认值**：论文没有报告阶段划分时，按 **runtime** 处理。这是有意的保守选择，避免夸大外环 seat。DynaHarness、LRLL、RoboSkill、RoboFoundry 都按此处理。

### 5.2 五个 seat

| Seat | 定义（判定规则） | 常规的非 agent 填充者 | CORE（加粗）/ CORE-P 代表 |
|---|---|---|---|
| **Controller** | runtime。通过 **counterfactual 检验**：*「如果没有发生任何失败或例外，这个输出是否仍然改变身体或执行器的行为？」* 回答是。输出形式包括：下一个动作单元、调用、子目标、一直作用的 objective 或 guidance、当下执行的程序、消息。评测期间发生的自我改进也归这里，记 improvement locus（context/memory、code/skill library、harness、weights）并打 **lifelong** 标。 | 遥操作员、脚本序列器 | **SayCan、Inner Monologue、RoCo、Harness VLA、Show-Harness、OneTwoVLA、PaLM-E、Embodied-Navigator、CaP-X、MessyMem**；Hi Robot、ThinkAct、L2R、LRLL |
| **Supervisor** | runtime。counterfactual 检验回答否：输出只在事件、门控、否决、shield、中断、恢复触发、重规划请求时起作用（包括由 agent 合成的 monitor）。并且输出由一个**与名义决策过程分开**的检查过程产生（独立的模型、prompt、角色或编译后的 monitor）。名义行为来自另一个决策者 D，D 可以是策略、技能序列、另一个 agent 或人。如果只是在 D 的提议中做选择，又没有 veto、stop、replan 这类行为，则 A2 不满足，判 B-auth。 | 不设 monitor、固定阈值检测器、安全员 | **CaM、DoReMi、REFLECT、FRAMES、Recova、Phoenix、SOMA**；CycleVLA、WhenToAsk |
| **Teacher** | pre-evaluation。agent 亲自执行、并经结果检查的行为，被部署模型（另一个模型，或 agent 自己的后继，打 self 标）当作训练目标或冻结的上下文来消费。包括：轨迹、推理加调用的 trace、恢复分支、*只用于产出示范*的逐实例调试程序、playbook。对学生 rollout 的纠正（T-correct）只有在 teacher 本身满足 A2/A3 时才算。 | 人类示教、脚本示教 | **GUAVA、RoboTwin 2.0、EmbodiedSWE、HERO、RHD**；LocalNav、Frontier-to-Local、EXIMO |
| **Designer** | pre-evaluation。为一个独立的学习者、采集者或评测者指定**问题**：任务或任务分布、场景、资产、环境、仿真参数、DR 范围、仿真校准或数字孪生、reward / success / verifier 代码、课程、练习选择、数据选择。也包括评测套件，这是 **Examiner** 子型，红队测试和对抗性测试生成也归这里。**这类 artifact 即使经过 keep/revert 进化，也始终归 Designer。** | 奖励工程师、任务设计者 | **Eureka、DrEureka、CurricuLLM、Eurekaverse、OMNI-EPIC、REvolve、FIND、InterEvolve、EmbodiedGen V2、RDA、AnyBipe**；ASD、BOSS |
| **Developer** | pre-evaluation。修改部署系统**执行来求解任务**的持久机制：在 ≥2 个评测实例中复用的策略或程序代码、skill/tool 库、harness / 工具 / 控制代码、学习算法、训练代码、超参、硬件或形态。每次修改保留还是回滚，由 agent 自己运行的实验决定。 | 机器人工程师、研究员 | **ENPIRE、HARBOR、SimEX、RHO、HarnessPAI、RAPID、MEMENTO、Push-T、RoboMorph、Skill2Real**；ASPIRE、AdaHVLA、RegenHarness、URAI |

**problem / solution 切分的样例**

| 论文 | 判定 | 理由 |
|---|---|---|
| Eureka | Designer | reward 代码，取最优候选 |
| HARBOR | Developer \| Designer | 算法和超参属 solution；环境和奖励属 problem |
| SimEX | Developer \| Designer | toolbox 代码属 solution；仿真器与真机的协同校准属 problem |
| ENPIRE | Developer \| Designer(Examiner) | 修改 CaP、skill、PLD 代码属 solution；reset.py / verify.py 属 problem |
| RAPID | Developer | 程序在多次试验中复用 |
| EmbodiedSWE | Teacher | 逐任务程序只用于产出示范 |
| RPG | Developer \| Designer | 技能改进属 solution；孪生重建属 problem |
| RoboMorph | Developer | 形态属于 solution 侧的硬件 |

### 5.3 Carrier（Controller 内的四个子类；其他 seat 也记录 carrier）

先找到掌握任务级控制流的最高层决策者，再依次判断：

- **Q6**：作者是否没有对其权重做具身训练？是 → **G**。第三方原样调用厂商的具身 checkpoint 时也判 G，加 vendor 标。
- **Q7**：是否由同一个训练过的模型同时给出显式决策和执行器级指令，且下游只有确定性、无状态的重编码？是 → **I**。
- **Q8**：执行器是否是**协同设计**的学习型策略？是 → **H**；否 → **C**。
  - 协同设计的含义：执行器的输入接口就是决策者输出的词表（标签、子任务、点、latent），并且执行器是在同一工作中为它训练或后训练的，或与决策者联合训练。
  - 判 H：Hi Robot、MemER、DualVLN、HAMSTER、RACER、YAY Robot、Phoenix、Gemini Robotics 1.5（厂商自己的论文）。
  - 判 C：PaLM-E、Robix、RoboOS（技能来自其他工作）；NaVILA（执行器是通用的速度接口）；Embodied-Navigator、VLA-R1、Embodied-R1（执行器是规划器）。

**Topology 列**

| 取值 | 含义 | 例 |
|---|---|---|
| ×1 | 单个 agent | — |
| ×R | 多个角色化的决策上下文共享同一个任务实例（一个身体，或一个正在修订的 artifact） | FRAMES、HARBOR、AdaHVLA、NavHarness |
| ×N | 每个身体一个决策上下文 | RoCo、CoELA、AeroWeaver |
| ×O | 多个 agent 各自负责一个分支或工位，覆盖整个 campaign，靠选择与共享来协调 | ENPIRE |
| 1:N | 一个决策者对多个身体 | SMART-LLM、AutoRT、RoboOS |
| +h | 有人类共同占位 | — |

### 5.4 容易混淆的界线

| 两边 | 规则 | 例 |
|---|---|---|
| Controller vs Supervisor | 用 counterfactual 检验，并要求检查过程与名义决策分开 | VLS、ReKep 的约束一直起作用，判 Controller；RoboGuard 的 shield、CaM 的 monitor 在没有违例时什么都不改变，判 Supervisor。Inner Monologue 的 success detector 只是 organ，名义重规划归 Controller |
| Controller(lifelong) vs Developer | 看 production phase：评测期间的改进归 Controller 并记 locus；有独立的开发阶段、产物冻结后再评测，才归 Developer | DynaHarness / LRLL / RoboSkill 判 Controller；HarnessPAI（运行时没有 LLM）、Skill2Real 判 Developer |
| Developer vs Teacher | 程序在 ≥2 个评测实例中复用或被部署，判 Developer；只用于产出示范，判 Teacher | RAPID → Dv；EmbodiedSWE → T |
| Developer vs Designer | solution 侧还是 problem 侧 | 见 5.2 的样例 |
| Teacher vs Designer | 学生模仿的是 agent 自己做出的、依赖状态的选择 → Teacher；agent 只决定练什么、留哪些数据，示范来自策略、oracle 或人 → Designer | RoboTwin 2.0 → T；GenSim、AutoRT、RoboClaw 的采集 → Ds |
| Teacher vs Controller-memory | 在独立阶段产出、冻结后由另一个 agent 或后继 agent 读取的 playbook → Teacher；评测期间自己写、自己读的 memory → Controller | RHD → T；ExpTeach、DROC → C |

### 5.5 Decision procedure（按顺序回答的是/否问题）

**STEP 0：Tier**

- **Q0a**：是否有 FM 输出 A1 决策（先过 A0）？否 → **OUT**（organ 或执行器）。
- **Q0b**：是否满足机器人形态条款？是否满足 C5（因果可达）和 C6（具身目标）？任何一条不满足 → **OUT**（标注排除类别）。
- **Q0c**：论文是否只是评测别人的 agent，没有自有方法？是 → **RESOURCE**，标 evaluated seat、F 和子型。但若论文自有方法满足 C1–C7，CORE 优先。
- **Q0d**：证据是否只有 list、title 或博客级，或者无法判断决策过程是不是 agent？是 → **UNRESOLVED**。
- **Q0e**：在承载 headline 的 coupling 上检查：
  - A2 不满足 → **B-auth**
  - A3 不满足（Λ0/1/1s/1'、M-only、单次调用的在环 judge）→ **B-loop**
  - agent 成立但只到 F1 → **B-world**
  - F0 → **OUT**
  - 全部满足 → 进入 Q0f
- **Q0f**：是否满足 C7？否 → **OUT**。是 → **CORE**；若有关键细节未确立，判 **CORE-P**。
- **fallback**：如果承载 headline 的 coupling 不是 agent（例如 annotator 或非 agent 的 curator），就改用论文中最好的那个 agentic coupling（通常是部署端的 agent）走 Q0e。例：DEDER、MobiAgent。

**STEP 1：列出 coupling**

为每个 coupling 写出 (agent, output, consumer, production phase)。

**STEP 2：逐个 coupling 判 seat**

- **Q1**：agent 是否在报告的评测 episode 中被调用（production phase = runtime）？
  - 是 → Q2。
  - 否 → Q3。
- **Q2**：做 counterfactual 检验。如果没有发生例外，这个输出是否仍然改变身体或执行器的行为？
  - 是 → **CONTROLLER**。评测期间的改进记 locus。
  - 否，且输出只在事件、门控、否决、恢复时起作用，由独立的检查过程产生 → **SUPERVISOR**。
  - 否，且只是在 D 的提议中做选择 → A2 不满足，回到 STEP 0。
- **Q3**：输出是否修改部署系统执行来求解任务的持久机制（策略或程序在 ≥2 个实例中复用、skill/tool 库、harness、学习算法、训练代码、超参、硬件），并由 agent 自己的实验决定保留或回滚？是 → **DEVELOPER**。
- **Q4**：输出是否是 agent 亲自执行、经结果检查的行为（或由此提炼的 playbook），被部署模型当作训练目标或冻结的上下文使用？是 → **TEACHER**。
- **Q5**：输出是否为独立的学习者、采集者或评测者指定任务、环境、仿真参数或孪生、reward / success / verifier、课程、练习选择、数据选择，或评测套件？
  - 是 → **DESIGNER**。
  - 否 → 回到 Q0b，重新检查 C5。

**STEP 3：主 seat（只作展示标签）**

- 主 seat 取**其消融承载 headline 主张的那个 coupling**，依据摘要或贡献列表判断，而不是看第一张表。
- 如果摘要中两个 coupling 地位相当，取先列出的那一个，并打 `dual-seat` 标。
- 所有 coupling 都写入 **seat 向量**。图表和趋势统计**以 seat 向量为单位**（all-seat counting）；主 seat 只用于章节归属。

**STEP 4：判 carrier（5.3），并填写 §6 的各列。**

### 5.6 示意图：Seat × Carrier 网格

每格写作 CORE / +CORE-P。Controller 行按主 seat 计数；其他 seat 行记录的是源 carrier，括号内为迁移目标。

```
                       Carrier →   G untouched     C trained,        H trained,          I one model      ?
Seat ↓                             general         generic exec.     co-designed exec.   decides+acts
───────────────────────────────────────────────────────────────────────────────────────────────────────────
CONTROLLER  runtime, nominal       33 / +25        3 / +2            0 / +5              1 / +4           0 / +2
SUPERVISOR  runtime, on exception   6 / +0         –                 1 / +0              –                0 / +2
TEACHER     pre-eval, acted traces  5 / +3   ──►  (targets: C GUAVA·LocalNav | G-light RHD | I EXIMO | ∅ RoboTwin·EmbodiedSWE·HERO)
DESIGNER    pre-eval, problem      11 / +5         –                 –                   –                –
DEVELOPER   pre-eval, solution     10 / +7         –                 –                   –                –
───────────────────────────────────────────────────────────────────────────────────────────────────────────
phase:  development/training ◄────────────── pre-evaluation ──────────────►│◄──── runtime (evaluated episodes) ────►
residual at actuator (column): A agent-in-loop (same | compressed | other) · P compiled · W weights-only · N none
```

**读法**：外环 seat（T、Ds、Dv）里只出现 G 作源 carrier。训练过的 carrier（C、H、I）只出现在运行时 seat 中，通常是 Teacher 箭头的落点。Controller 行的 H 与 I 在 CORE 中合计只有 1 篇（OneTwoVLA），其余全部是 CORE-P；Supervisor 行的 H 为 Phoenix。

### 5.7 初稿四类在新框架中的位置

| 初稿 | 现在的位置 |
|---|---|
| (1) external orchestration | Controller-G / C |
| (2) hierarchical dual-system | Controller-H（只收显式决策的版本；潜变量版本判 OUT） |
| (3) internalized | Controller-I（CORE 1 篇 + CORE-P 4 篇，对比 B-loop 19 篇） |
| (4) multi-agent | 不再是一个类别，改为 topology 列 ×R / ×N / ×O，可横跨所有 seat（RoCo 为 C×N，FRAMES 为 S×R，ENPIRE 为 Dv×O） |

Supervisor、Teacher、Designer、Developer 这四个 seat 是初稿没有覆盖到的。

---

## 6. 正交的 anatomy 轴（主表的列）

| 列 | 取值 | 作用 |
|---|---|---|
| **Tier + 证据等级** | CORE / CORE-P / B-auth / B-loop / B-world / RESOURCE / UNRESOLVED / OUT；证据等级：full-text / abstract / description / list / title / blog / memory | 让审计状态可见 |
| **Seat 向量** | 主 seat 加粗，dual-seat 标；每个 coupling 写成 (seat, production phase) | 统计单位 |
| **Carrier（按阶段，用箭头）+ topology** | G / C / H / I / ∅；×1 / ×R / ×N / ×O / 1:N / +h；vendor 标；co-designed-executor 标。例：GUAVA G→C；EmbodiedSWE G→∅；RHD G→G(light, in-context)；ENPIRE G×O(8:8:1)+h | 保留初稿的 locus 视角，并显示迁移 |
| **Interface / emission**（按离执行器从近到远排序） | motor（只在 I 中出现）/ semantic micro-actions / geometric targets / skill-tool calls / policy calls（VLA-as-tool）/ programs run now / objectives-constraints-guidance / verdicts-corrections-messages / acted traces & playbooks / problem specs / system edits；另加 harness 子标签 O/A/C/M/V 和 frozen surface | harness 是 anatomy 对象，不是类别 |
| **Closure 签名** | 强度 Λ0/1/1s/1'/2/3；closure 类型 E / E-tool / H / M（可多选）；cadence（step / primitive / subgoal / event / episode / training-run / experiment）；谁闭合快环；scaffold（fixed/open） | 慢 agent 与快 artifact 之间的分工 |
| **Residual** | A-same / A-compressed / A-other / P / W / N（可组合）；迁移路径（same-interface agent→agent / lowered-interface agent→policy / in-context playbook / compile / dissolve）；improvement locus；lifelong 标 | 区分「谁产生了行为」和「谁执行行为」 |
| **Provenance**（决策权重的来源） | prompted / agent-distilled / annotator-distilled / demo-trained / agentic-RL / action-aligned co-training / self-evolved / n/a | 把 GUAVA 和 ECoT 之间的界线编码进来 |
| **Verifier 与 permission surface** | 反馈来源；verifier 所有权：frozen-external（ENPIRE、GUAVA 的标签）/ agent-authored-then-frozen（CaM）/ agent-mutable（MEMENTO）/ human / none；可变与冻结的 artifact 清单；外环中人类控制流的份额 | 外环自主性的安全与有效性 |
| **Body** | 形态类别；F0–F3；领域（manip / nav / mobile-manip / loco-humanoid / aerial / driving / multi-robot / social）；sim 或 real | — |

**两个视图**
- **中心图**是 Seat × Carrier 网格（§5.6），直接对应用户的主线。
- **第二视图（View B）**是 Carrier × Interface × Cadence，即组件 anatomy。

**为什么 Residual 降为一列**：测试集上 Seat × Residual 的列联表（CORE+CORE-P，按主 seat）显示，它与 seat 并不正交：

| seat | Residual 分布 |
|---|---|
| Controller | A 74、A+W 1（结构上被强制） |
| Designer | W 16（结构上被强制） |
| Supervisor | A 7、A+P 2 |
| Teacher | A 4、W 3、A+W 1 |
| Developer | A 8、P 5、W 3、P+W 1 |

只有 Teacher 和 Developer 两行有信息量，所以 Residual 作为列和迁移箭头记录，不再单独构成视图。

---

## 7. 用户点名案例的定位

### 7.1 GUAVA（2606.18363；按 v3 判）→ **CORE，Teacher** | Controller-C

**两个 coupling**
1. GPT-5.4 ReAct teacher 在随机化的 robosuite/MuJoCo 场景中亲自行动，每轮输出一个 JSON tool call，自行宣告 "Task complete/failed"，属 Λ3 + E。
   - 产出约 2,268 条轨迹（v1 报告的是 1,191 个成功 episode）。
   - 轨迹包含 6 类注入扰动后的恢复分支。
   - 标签由仿真结果给出，再经自动一致性检查和人工目视复核。
   - 这些轨迹**只作为 Qwen3.5-4B 全参 SFT 的目标**。
   - **GRPO 是另行的在线 RL 后训练**，只在两个长程任务上做：shell game 63.3→90.0，red objects 80.0→86.7。
   - 这个 coupling 判 **Teacher**。
2. Guava-4B 部署后在**同一个 harness** 中发出 tool call，判 Controller-C。

**为什么主 seat 是 Teacher**：v3 的标题和摘要把蒸馏作为 headline。本稿用 STEP 3 的 headline 规则判定。项目页的第一张表是 harness study，其自变量是 harness，按旧的「第一张表」规则会判成 Controller-G，这正是废弃旧规则的原因。按探索记录，v1 的标题为 "An Effective and Universal Harness…"，按 headline 规则应判 Controller-G，所以必须钉住版本。这一点只核对到标题层面。

**数字及其出处**
- 15 任务主表（仿真，各 30 次试验）：Guava-4B 87.1；GPT-5.4 90.4；base 22.2。
- 真机 Franka（9 任务 × 10 次）：90.0 / 93.3 / 28.9。
- 7 任务 harness study：full 88.6 / 22.9；low-level tools 73.3 / 4.8；image-only 56.2 / 3.8。
- 效率：延迟 4.168s→0.587s（7.10×）；每 episode 生成的 token 2,389→795。
- 未见任务：用扰动数据训练 90.8，不用 77.1。

**Anatomy**
- Carrier G→C，迁移类型为 same-interface agent→agent。
- Interface：语义 tool（grasp / align / move / rotate），两个阶段完全相同。
- Residual：A-compressed。
- Provenance：agent-distilled，加上 agentic-RL。
- Verifier：训练标签 frozen-external；运行时由 agent 依据观测自行宣告结果。
- 保真度：F2（MuJoCo 中漏抓、掉落是物理性的失败）+ F3。

**对照**
- ECoT 的管线是 annotator，判 OUT。
- SUDD 的 teacher 是 Λ1'，判 B-loop。
- EmbodiedSWE 同属 Teacher，但 residual 为 W。
- RHD 同属 Teacher，但是 in-context 迁移。

### 7.2 「harness VLA」「show harness」最可能指什么

| 用户说法 | 最可能的论文 | 置信度 |
|---|---|---|
| show harness | **Show-Harness: Just a VLM Agent Can Play Robots**（2609.10522，NUS Show Lab） | 约 95% |
| harness VLA | **Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents**（2607.08448，RLinf/RPent） | 约 90% |
| harness VLA（另一种读法） | AdaHVLA（2609.29204，仓库名为 "Adaptive_Harness_VLA"） | 约 10% |
| 注意同名 | RoboHarness 有两篇：2603.24060（现标题为 SOMA）和 2607.18060 | — |

**Harness VLA → CORE，Controller-G**
- 冻结的 π0.5 / RLDX-1 / LingBot-VLA 作为 `VLA_ACT` 工具，与解析式原语并列。
- agent 负责语义重落地（re-grounding）和重新摆放到 VLA 熟悉的起始状态（re-staging）。
- 每次原语调用后闭环一次，Λ3、E；locus = memory。
- VLA 冻结，也没有为 agent 做后训练，所以判 G，不判 H。
- 「在权重不变的情况下 LIBERO-Pro +38.6pp，RoboCasa365 +25.4pp」：*未独立核实*。

**Show-Harness → CORE，Controller-G**
- headline 是 zero-shot：前沿 VLM 输出 semantic micro-actions，由确定性 interpreter 执行，F2/F3。
- GUMI 里由 GUI agent 采集的数据记为次 Teacher 边，G→I。只算次要，因为换成人类示范，主张依然成立。
- 微调后的单 token 模式若单独评估，属 B-loop Controller-I（Λ1）。
- 结论：同一套动作词表既能承载 agent，也能承载反应式策略；是 agent 还是策略，**由环决定，不由词表或权重决定**。

**2026 年 harness 浪潮**：harness 是 anatomy 对象，不构成类别。

| 定位 | 论文 |
|---|---|
| Controller-G，CORE | Harness VLA、Show-Harness、Robo-Harness K1、Thea、OpenETA、PyRUA-Lean、SafeHarness、MotorMind、RoboHarness(2607.18060)、AgenticNav、NavHarness(2609.39915) |
| Controller-G，lifelong，CORE-P | NavHarness-lifelong、DynaHarness、RoboHarn-Evo、RoboFoundry |
| Controller-I，CORE-P | ART |
| Controller-H，CORE-P | Gemini Robotics 1.5 |
| Supervisor，CORE | SOMA |
| Teacher，CORE | GUAVA、RHD |
| Developer | HarnessPAI、RHO（CORE）；AdaHVLA、RegenHarness（CORE-P） |
| UNRESOLVED | HarnessVLN |
| OUT | Harness Engineering for Physical AI（没有决策者）；Harness-Zero（纯数字） |

### 7.3 ENPIRE（2606.19980，NVIDIA GEAR）→ **CORE，Developer** | Designer(Examiner)

- **为什么是 Developer**：被评测的 episode 中不调用 agent，Q1 否。agent 修改会被执行的 CaP 程序、skill 库、PLD 训练代码和配置，并依据真机试验的成功与回归门槛，用 git 保留或回滚，Q3 是。
- **复位与练习**：agent 在复位和练习时发出的机器人动作属于 pre-evaluation，不构成 Controller coupling。
- **Designer(Examiner) 次 seat**：第一阶段在人参与下编写 reset.py、verify.py 和安全边界，然后冻结。
- **满足人类控制份额规则**：第二阶段完全自主。
- **Anatomy**：
  - Carrier：G×O(8:8:1)+h，使用 Codex / Claude Code / Kimi Code。
  - Closure：Λ3，E，cadence = experiment，scaffold = open。
  - Residual：P（Push-T 的 CaP 程序）+ W（PLD 训练出的 JAX actor）。
  - Permission surface：frozen-external。可以修改奖励塑形；score、verifier、安全限位和 eval seeds 冻结。
- **为什么不是其他三类**：不是 multi-agent（多个 agent 是 topology，不是 seat）；不是 orchestration（从不在被评测的 episode 内排序技能）；不是 internalized（RL 训练出的策略里没有推理）。
- 「约 99%」来自搜索摘要，*未经核实*。

### 7.4 Code-as-Monitor（2412.04455；年份 2024，会议 CVPR 2025）→ **CORE，Supervisor** | Controller-G

- **为什么是 Supervisor**：VLM 编写几何谓词程序，由编译后的代码每帧执行；没有违例时不改变名义动作，counterfactual 检验为否，且这是一个独立的检查过程。发生违例（reactive）或预测到违例（proactive）时，返回原因并重新调用 VLM 做 replanning，属 Λ3、E。
- **次 seat**：子目标规划记为 Controller-G 次 seat。
- **Residual**：A（按事件）+ P（按帧）。
- **Verifier**：agent-authored-then-frozen。
- **数字**：在严重扰动下，成功率 +28.7%，执行时间 −31.8%。来自项目页源码，*未独立核实*。
- **对照**：
  - VoxPoser、ReKep 是同一机制，但模型不再被调用，属 Λ1'，判 B-loop。
  - DoReMi 每一步都查询 VLM，判 CORE Supervisor。
  - StageGuard 是单次调用的 judge，判 B-loop。
  - VLS 的 guidance 一直作用，判 Controller。

### 7.5 经典锚点

| 论文 | 定位 | 一句话理由 |
|---|---|---|
| SayCan（2204.01691） | CORE Controller-G，Λ2 (weak, E) | 满足 A2(b)：异质 skill 中选择，'done' 也是选项。affordance 在执行后的状态上计算，skill 历史写在 prompt 中 |
| Inner Monologue（2207.05608） | CORE Controller-G，Λ3 | 典型的闭环规划者；success detector 是 organ |
| Code as Policies（2209.07753） | B-loop（Λ1'） | 一次写出闭环程序 |
| VoxPoser（2307.05973）/ ReKep（2409.01652） | B-loop（Λ1'），名义 Controller | 约束一直作用（counterfactual 判 Controller），但模型不再被调用 |
| KnowNo（2307.01928） | B-loop | A2 通过（选项由 LLM 生成）；但人挑选选项替代了这一步的决策，之后没有执行证据 |
| π0.5（2504.16054） | B-loop Controller-I（Λ1） | 无记忆的子任务调度；Harness VLA 所包装的底座 |
| Hi Robot（2502.19417） | CORE-P Controller-H | 与 ThinkAct 是**同一个**审计问题：高层输入是否含有自身先前的指令；若没有，判 B-loop |
| ThinkAct（2507.16815） | CORE-P Controller-H | 同上。显式推理，以 latent 交接给执行器 |
| ECoT（2407.08693） | B-loop Controller-I | Λ1；teacher 是 annotator |
| OneTwoVLA（2505.11917） | CORE Controller-I | 自己决定何时思考，维护历史摘要，能从错误中恢复 |
| RoCo（2307.04738） | CORE Controller-G ×N | 对话协商；执行后在新观测上进入下一轮 |
| Eureka（2310.12931） | CORE Designer | 基于训练统计反思，cadence = training-run，scaffold 固定 |
| AutoRT（2401.12963） | B-loop Designer | 按场景重新提议，没有自身记录 |
| SUDD（2307.14535） | B-loop Teacher | 管线执行重试，LLM 不再被调用 |
| Manipulate-Anything（2406.18915） | CORE-P Controller-G \| Teacher | dual-seat；verifier 判失败后是否带着上下文重新调用 VLM，待审计 |
| Language to Rewards（2306.08647） | CORE-P Controller-G (H) | 一直作用的 objective，并整合用户纠正 |
| Voyager（2305.16291） | OUT（history-only） | 没有机器人身体；物理世界的继承者是 LRLL、RoboSkill、Skill2Real |
| OpenVLA / π0 | OUT（执行器底座） | A1 不满足 |
| Coscientist precursor（2304.05332） | OUT | 不满足 C6 |

### 7.6 critic 指出的缺失方向及其规则位置

标「*」的例子来自 critic 的列举，不在测试集中；收录前需要单独审计，此处不给 ID。

| 缺失方向 | 规则位置 |
|---|---|
| world model 作为规划工具，同时有执行闭环（VLMPC*、Video Language Planning*） | 若显式决策者掌控环且有 E closure，归本文，world model 记 M。若 VLM 只在采样候选中打分 → B-auth。若执行器消费的是视频计划 → WAM |
| embodied-brain FM（RoboBrain*、Cosmos-Reason1*、Magma*、Gemini Robotics-ER* 单独使用、VeBrain*） | 只在离线评测时判 OUT（carrier 底座，进入 Provenance 和 Carrier 列）；论文自己做了作用在身体上的闭环实验时，按 seat 规则判；无法确认时判 UNRESOLVED（ME-VLM） |
| EQA 与主动探索（Explore-until-Confident*、OpenEQA*、3D-Mem*） | 只要身体在环中移动或观察以获取信息，C6 就成立（信息获取也是身体的任务）。如果只对预录记忆做 QA，不满足 C5，ReMEmbR 因此判 CORE-P 并待审计 |
| benchmark（EmbodiedBench*、Embodied Agent Interface*、VLABench*、RoboCerebra*、LoTa-Bench*、SafeAgentBench*、IS-Bench*） | RESOURCE，标 evaluated seat、F、子型 |
| 安全、红队、攻击（RoboPAIR*、BadRobot*、ASIMOV*、Safety Chip*） | 攻击者 agent 迭代攻击结果，判 Designer-Examiner（adversarial）；攻击 benchmark 判 RESOURCE；一次写成的 LTL 转换器判 B-loop Supervisor（同 RoboGuard） |
| 在线 VLM-as-reward（SOAR、Self-Improving Embodied FMs*） | 区分 **authored artifact** 与 **evaluated function**：写出可执行 reward 或 success 代码属 A1 决策，可进 Designer；模型本身就是 reward（按样本调用，输出标量或 judgment）则是 organ |
| LLM 计划既塑造训练又在运行时执行（Plan-Seq-Learn*、SayTap*） | 逐 coupling 判：训练期被消费 → Designer；运行时被消费 → Controller；主 seat 按 headline。多数是单次计划，判 B-loop |
| real-to-sim 与数字孪生（RPG、SimEX、DrEureka） | 孪生构建、仿真校准、DR 范围属 problem，归 Designer；只有 solution 侧的 artifact 归 Developer |
| HRI 中澄清以外的方向（GenEM*、解释生成、shared autonomy） | 人类迭代反馈记 H；表达性行为属 Controller（消息或动作）；VLM 辅助遥操作时，人是 D，VLM 对人的动作做门控或提示 → Supervisor（+h）。Auto-HSI 判 B-loop Controller |
| 单 UAV 和闭环驾驶 agent（TypeFly*、Agent-Driver*、CARLA 中的 DriveLM*） | 按同一套规则判（§4 驾驶行；AeroWeaver 为 CORE-P） |
| 机器人软件工程 agent（ROS 代码生成、程序修复、MCP 服务器） | 只有当修改在机器人身体上执行、并按任务能力实验决定去留时，才归 Developer。只评测代码正确性的判 OUT 或 RESOURCE |
| agent 编写的评测（Examiner） | Designer-Examiner：GenManip（单次生成，判 B-loop）；ENPIRE 的 verify.py（次 seat）；AutoEval 没有 agent，判 OUT |
| 人与 agent 协作的研究环 | 外环的人类控制份额规则（§3）：Project Fetch 判 RESOURCE；Agent-Driven RL Research 判 CORE-P 并待审计 |
| 独立的随机样本验证 | 见 §10 的验证方案 |

---

## 8. 叙事主线

**One line：** ***"Agency spreads around the body — and loop closure, not weights, makes a carrier an agent."***

**中文：** agency 没有从机器人身上迁走，而是在身体周围逐个占据新的 seat；而一个模型能不能坐进任何一个 seat，取决于它是否闭合了「带着自身记录、依据后果再决策」的环，与它是哪套权重、多大规模无关。

**论证段**

2022 年，CORE 只占据 Controller 一个 seat（SayCan、Inner Monologue）。此后各 seat 依次出现：
- 2023 年：Supervisor（DoReMi、REFLECT）和 Designer（Eureka）；
- 2024 年：Designer 成为这一年的峰值（Eureka 浪潮），并首次出现 Developer（RoboMorph）；
- 2025 年：Teacher（RoboTwin 2.0）；
- 2026 年：五个 seat 全部有人占据，Developer 大量出现（ENPIRE、HARBOR、HarnessPAI 等）。

但驾驶位并没有被腾空：
- 2026 年，63% 的 CORE 论文仍含有 Controller coupling；
- Developer 论文中约一半（CORE+P 中 17 篇里有 8 篇）在执行器端仍保留一个 agent（ASPIRE、RHO、AdaHVLA 等）。

所以这是 seat 的**增加**，不是**迁移**。

决定一个 carrier 能否进入某个 seat 的是环：
- 同一族 Qwen3.5 小模型，在 GUAVA 的 harness 中是 agent，在 Show-Harness 的单 token 模式下不是；
- 在「内化」路线上，显式推理的 VLA 中有 19 篇判 B-loop，只有 1 篇判 CORE、4 篇判 CORE-P；
- 外环 seat 至今只由 G 类 carrier 占据。训练过的 carrier（C、H、I）只出现在运行时 seat：经 Teacher 箭头（agent 蒸馏）进入的目前只有 GUAVA、LocalNav，其余来自 annotator 数据、示范或 RL（OneTwoVLA、Embodied-Navigator、PaLM-E）。

**测试集证据**（350 条去重后；按主 seat 计数，括号内为 all-seat，即「含有该 seat 的论文数」）

| 年 | CORE n | Controller | Supervisor | Teacher | Designer | Developer | Controller 占比（all-seat） | 有效 seat 数 e^H |
|---|---|---|---|---|---|---|---|---|
| 2022 | 2 | 2 (2) | 0 | 0 | 0 | 0 | 100% (100%) | 1.00 |
| 2023 | 9 | 6 (8) | 2 (2) | 0 | 1 (1) | 0 | 67% (89%) | 2.14 |
| 2024 | 13 | 5 (6) | 1 (1) | 0 | 6 (6) | 1 (1) | 38% (46%) | 3.01 |
| 2025 | 5 | 3 (4) | 1 (2) | 1 (1) | 0 (1) | 0 | 60% (80%) | 3.36 |
| 2026 | 41 | 21 (26) | 3 (4) | 4 (6) | 4 (9) | 9 (10) | 51% (63%) | 4.03 |
| **含 CORE-P** | 125 | 75 | 9 | 8 | 16 | 17 | 2026：55% (71%) | 2022–26：1.00 / 2.37 / 3.20 / 2.35 / 3.79 |

**稳健性说明**
- **Developer**：2026 年含 Developer coupling 的论文，CORE 为 24%，CORE+P 为 29%；2022–2024 年 CORE 中只有 1 篇（4%）。按主 seat 算，2026 年为 22%。改用 innermost tie-break 后，2026 年只剩 3/41（7%）。因此这个结论**只在 all-seat 计数下稳健**，正文必须写明统计单位。
- **Spread（有效 seat 数）**：只看 CORE 时单调上升（1.0→4.0）；把 CORE-P 也算进来，2025 年会回落到 2.35（因为 2025 年的 CORE-P 主要是 Controller）。
- **「steer less, shape more」不成立**：Controller 占比不单调。2024 年 Designer（6）略多于 Controller（5），是唯一不由 Controller 占多数的年份。
- **Carrier**：CORE 的 Controller 中，G 占 33/37（89%）；CORE+P 中为 58/75。

**接口主张单独列为受控证据**（不作为主线）：
- **GUAVA 的 harness study**：GPT-5.4 用最差的接口（56.2）也优于 4B 模型用最好的接口（22.9），所以**模型能力占主导**。接口的相对作用随 carrier 变小而变大：4B 从 4.8 升到 22.9（约 4.8×），GPT-5.4 从 73.3 升到 88.6（约 1.2×）。
- **PyRUA-Lean**：固定模型，code-cell 对 tool-call，标题称成功率 +14%、token −65%（*标题级*）。
- **Harness VLA**：VLA 权重冻结时 +38.6pp（*未核实*）。
- **结论**：「在权重固定时，接口是一阶变量，carrier 越小作用越大。」**不能**写成「接口比模型大小更重要」。

**可证伪预测**：先固定计数规则（seat 向量、CORE；同时报告含 CORE-P 的结果），然后在独立随机样本上检验。测试集上的数值只作 sanity check。

| 编号 | 预测 | 测试集（CORE / 含 P） |
|---|---|---|
| P1 spread | 2026 年有效 seat 数 ≥3.5，且比 2023 年至少高 1.0 | 4.03 vs 2.14 ✓ / 3.79 vs 2.37 ✓ |
| P2 no-migration | 从 2023 年起，每年 ≥40% 的 CORE 论文含 Controller coupling | 最低为 2024 年的 46% ✓ / 62% ✓ |
| P3 Developer opening | 2026 年起含 Developer coupling 的论文 ≥15%，2024 年及以前 ≤5% | 24% vs 4% ✓ / 29% vs 6% ✗（2024 年有 RoboMorph 和 LRLL 次 seat） |
| P4 loop-not-weights | 显式推理的 Controller-I 中，boundary : core ≥2:1，除非模型带显式的自身决策状态 | 19:1 / 19:5 ✓。这一条部分是定义的推论；经验支撑来自 masked-CoT 消融：ECoT-Lite，以及 DeepThinkVLA 的 README 所称在 0.175× 延迟下保持 96.5%（*未核实*） |
| P5 agent-distilled | 在训练过的 carrier（C/H/I）中，agent-distilled 占比相对 annotator-distilled 上升 | **当前无法检验**。只有在每个时期有 ≥20 篇来源已知的论文时才计数；测试集中只有 GUAVA、LocalNav |

如果 P1 或 P2 在独立样本上被推翻，主线必须改写。测试集按家族收集，2026 年的论文占 CORE 的 59%，而它们的一手来源多为 list，因此上表**不是**趋势证据。

---

## 9. 与已有 survey 的区别

| 已有工作 | 它的组织方式 | 本文多出的东西 |
|---|---|---|
| Towards Embodied Agentic AI（2508.05294） | 按 LLM/VLM 在运行时如何集成来分类 | 给出 A0–A3 的可操作判定和 E/H/M closure。它的范围大致等于本文的 Controller + Supervisor；Teacher、Designer、Developer 它放不下（GUAVA、Eureka、ENPIRE） |
| Large Model Empowered Embodied AI（2508.10399） | 分为 decision-making 和 embodied learning | 把 learning 切成 Teacher、Designer、Developer，并在 agent、annotator、单次 builder 之间画界：Eureka 判 CORE，Text2Reward 判 B-loop，DIAL 判 OUT |
| Embodied AI: From LLMs to World Models（2509.20021） | 按模型族组织 | 规则是 dream vs decide；同时给 world model 作 M 工具的情形留出位置 |
| VLA surveys（2405.14093、2508.15201） | 架构、数据、训练 | 层级 vs 端到端对应本文的 H vs I；收入时要求满足 A3；VLA-OS 作为受控证据 |
| Landscape of Agentic RL（2509.02547） | 数字世界的 agent，以 RL 为机制 | 增加具身底线；agentic RL 只作为 Provenance 的一个取值；RL ≠ agency |
| Show Lab Awesome-Multimodal-Embodied-Agent（PAPAV） | 能力视角，刻意不看架构 | 给出 Seat × Carrier 坐标、production phase 和 residual |
| Awesome-Robot-Use-Agent | 按系统类型分节，没有判定规则 | 有序的判定程序和逐耦合检查；harness 作为横跨各 seat 的 anatomy |
| No Free Checker（2609.09250） | 按 judge 的来源分类 verifier | 先用 A0 区分 organ 与 agent；Supervisor 只收作为 agent 的 verifier；增加 verifier 所有权这一维 |
| Self-evolving Embodied AI（2602.04411）、Weights or Skills?（2608.01851） | 以自我改进为分类标准 | 以 agency 为标准，并用 production phase 区分 lifelong Controller 和 Developer。Residual（A/P/W）推广了 weights-vs-skills 的二分 |
| WAM survey（2606.20781） | 「dream less, act more」 | 两篇共享一条边界：中间表示是对世界的预测归 WAM，是决策归本文；world model 作为 M 工具时归本文 |

**只有本文有的东西**
1. A0–A3 判定，加 E/H/M closure；
2. 以 production phase 判定的五个 seat，并且 problem/solution 的切分写进了判定程序；
3. Seat × Carrier 网格，直接对应「agency 在哪里」；
4. 每一行都填写 Provenance、Residual 和 permission surface。

---

## 10. 已知弱点与待决策问题

**已知弱点**

1. **证据层**
   - CORE 的判定依据是测试集描述（约相当于摘要级），没有做全文审计。
   - 125 篇 CORE+P 中有 55 篇是 CORE-P；另有 39 篇 UNRESOLVED，其中 24 篇是 2026 年的论文。
   - 测试集有三组重复：WALL-OSS [195]/[218]、SC-VLA [113]/[239]、ReMEmbR [289]/[322]。已去重。
2. **主 seat 仍要靠判断。** 有 30% 的 CORE 论文属于 multi-seat（21/70），例如 RoboClaw、Manipulate-Anything、AdaHVLA、Recova。正因如此，统计一律以 seat 向量为单位。
3. **阶段默认值的影响。** 把「未报告的阶段划分」默认为 runtime，会把一批 2026 年的自进化 harness 计为 Controller-lifelong（DynaHarness、RoboSkill、LRLL、RoboFoundry），从而压低 Developer 计数。这是有意的保守选择，但会因审计结果而变动。
4. **Controller 规模过大。** Controller 占 CORE 的 53%，加上 CORE-P 后占 60%，并且 G 占绝对多数。章节必须按 Interface 再分，例如：
   - 编排者：skill、tool、policy 调用；
   - 直接驱动者：micro-actions、native commands、code；
   - lifelong / memory agent；
   - 训练过的 carrier（C/H/I）。
5. **严格的 A3 会把名作降为 boundary。** CaP、VoxPoser、ReKep、π0.5、ECoT、SUDD、AutoRT、KnowNo 都受影响；Hi Robot 和 ThinkAct 取决于未报告的上下文构造。
6. **几条界线仍然精细。**
   - M 与 E-tool：对由自身感知构建的地图做检索算 E-tool，规划期的场景图模拟算 M。
   - counterfactual 检验需要知道「名义运行」时系统是什么样子。
7. **人只作为证据来源，不作为 seat 的占有者**（D 可以是人），因此 shared autonomy 的工作仍会被低估。
8. **趋势结论依赖测试集的采集偏差**，必须用独立样本复核。

**验证方案（抽样框架）**

- **抽样**：从仓库 `data/candidates` 的引用收割中，按年份分层随机抽取 150 篇，另加本稿列出的约 40 篇难例作为压力子集。
- **标注**：两名标注者盲标，对 Q0a–Q0f、Q1–Q5、Q6–Q8 **逐步**报告 Cohen's κ，并单独报告 tier 和主 seat 的 κ。
- **记录**：公开判定日志。
- **审计优先级**：先审计 UNRESOLVED 和 CORE-P，再计算正文中的数字。

**待决策问题**（详见结构化输出 open_decisions）：
- 驾驶领域；
- F1 的处理；
- 是否对 Λ1' 放宽；
- 人类 closure 的计数规则；
- 阶段默认值；
- 统计单位；
- CORE-P 是否进入正文计数；
- 章节结构；
- 主线措辞；
- Examiner 的地位；
- memory、playbook 与 Developer 的界线；
- 与 robot-use agent 社区命名的关系。