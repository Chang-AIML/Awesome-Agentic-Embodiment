# Agentic Embodiment 综述写作方案

> Claude Doc「Agentic Embodiment 综述写作方案」的快照（2026-10-10 导出）。讨论和修改在原文档里进行：https://claude.ai/code/artifact/3814a79d-0de1-4954-9f8f-025f386674c9 。两者不一致时以原文档为准。

## 一、定义与主线

这篇综述只回答一个问题：**现成的通用大模型作为 agent，在什么时候、什么位置作用于机器人。** 以精选清单 186 篇为底稿，按「两个阶段、五个 Seat」组织全文。

**定义。** Agentic Embodiment 研究现成的通用大模型（LLM / VLM，不是具身动作模型）作为 agent 做出的显式决策；这些决策经由它产出的策略、代码或计划，或者直接作用于环境，到达机器人身体。

> *Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs used as-is, not embodied action models — acting as agents that make explicit decisions and are connected to a robot body, through the policy, code or plans they produce, or by acting on the environment directly.*

**主线（草案）。** *Agency spreads around the body*：通用模型不再只坐在「运行时编排技能」这一个位置，而是一个位置接一个位置地占据机器人系统：执行前设计学习问题、当老师、改系统，运行时控制和监督。全文用 2022–2025 年的先驱和 2026 年的新工作对照，展示这种扩散。

**和其他综述的区别。** 现有综述多按「LLM for robotics」的任务类型，或按 VLA / 具身基础模型来组织。本文有两点不同：

- 范围更窄：只看现成通用模型当 agent，作者训练的模型、VLA 只作为被调用的工具出现；
- 组织方式不同：按 agent 在系统中的位置（Seat）分章，而不是按任务或模型结构。

## 二、范围与收录标准

综述的「方法」一节直接用清单的收录标准。判定以一张回路图为准：**Agent → Policy / Code / None → Env / Sim**。agent 也可以直接作用于 Env / Sim，Env / Sim 的信息可以回到 agent。

| # | 标准 | 在综述里怎么写 |
| --- | --- | --- |
| 1 | 通用大模型 agent 必须存在，并在回路里起作用 | 写计划、写代码或约束、调用技能或 VLA、设计环境，或直接出动作，都算起作用 |
| 2 | agent 必须是**现成的**通用大模型 | 作者训练、微调或蒸馏的模型不算 agent，即使底座是通用模型 |
| 3 | 连到 Policy / Code 或 Env / Sim 之一即可 | 开环也算（Code as Policies、ReKep）；是否闭环只记录，不作门槛 |
| 4 | 论文主体必须是 agent | 数据平台、资产流水线不算（RoboTwin 2.0、HumanoidGen）；评测通用 agent 的 benchmark 归「资源」 |
| 5 | 通用大模型，不是具身大模型 | VLA、分层 VLA、机器人基础模型只能作为被调用的工具（Harness VLA） |
| 6 | 读全文判定 | 每篇写明谁在做决策、有没有训练，并摘一句原文为证 |

**环境范围。** 算：真机、物理仿真、离散具身仿真（ALFRED、VirtualHome、R2R 离散导航图）。不算：纯文本世界（ALFWorld 文字版、TextWorld）和自动驾驶。无人机和多机器人调度按六条规则正常判。

**在正文里的用法。** 这六条写成一个框，放在引言之后。每条配一个「收」的例子和一个「不收」的例子，都取自已经定下的判例：

- RoboFAC、AgentVLN 的决策者是微调过的 Qwen，不收；
- GUAVA 是通用模型自己行动、再把经验蒸馏成小模型，收为 Teacher。

这样读者能自己判断一篇新论文算不算。另外单列一个「不在范围内」的小节，简要交代 VLA 和具身基础模型这条相邻路线，并指向已有综述。

## 三、分类框架：两个阶段，五个 Seat

阶段由 agent 的产出**什么时候产生、什么时候被用**决定。每篇按主要贡献只归一个 Seat，再用「角色」细分 agent 在这个 Seat 里具体做什么。这就是正文的章节骨架。

（原文档这里是一张图，内容如下。标题：2026 年，agent 从运行时扩散到执行前；Developer 从 7 篇增至 20 篇。执行前的占比：先驱 29%，2026 年 46%。）

| 阶段 | Seat（篇数） | agent 做什么 | 角色 | 先驱 → 2026 | 例子 |
|---|---|---|---|---|---|
| 执行前（59） | Designer（22） | 设计学习问题 | 环境/重建 · 奖励/任务 | 12 → 10 | Eureka、RoboGen、SceneSmith |
| | Teacher（10） | 自己先执行，经验蒸馏成策略 | 示范/蒸馏 | 4 → 6 | RobotGPT、SUDD、GUAVA |
| | Developer（27） | 改系统本身，按试验保留或回滚 | 系统/代码 · 本体/工具 | 7 → 20 | RoboMorph、ENPIRE、RPG |
| 运行时（98） | Controller（84） | 每一步决定机器人做什么 | 编排 49 · 写策略 20 · 直接动作 15 | 47 → 37 | SayCan、Code as Policies、Show-Harness |
| | Supervisor（14） | 只在异常时介入 | 监控/恢复：失败检测、护栏、求助 | 8 → 6 | REFLECT、Code-as-Monitor、RoboGuard |

执行前的产出（环境、奖励、示范、代码、硬件）冻结后交给部署的系统；运行时 agent 的计划、代码、动作或干预作用于机器人身体（真机、物理仿真、离散具身仿真）。

图中每个框的第三行对照了先驱和 2026 年的篇数：Controller 一直最多，但 2026 年的新增主要落在执行前，尤其是 Developer。这是主线「agency spreads around the body」的数据依据，但样本是精选的，不能当作领域的真实分布，正文里只当趋势描述。

**归类规则**（写进正文的方法一节）：

- 兼有两个阶段的，看产出主要在哪个阶段被用。Agentic RSR、Real2Gym 在重建的仿真里练习、写出程序再带回真机，归 Developer；Language to Rewards 的奖励当场交给 MPC 生成动作，归 Controller。
- 模型写出、在运行时执行的程序算运行时。Code as Policies 归 Controller；Beyond Human Demos 的护栏代码在运行时过滤指令，归 Supervisor。
- Benchmark 和评测研究单列为「资源」，只记录被评测的 Seat。

**三个横跨 Seat 的专题。** 每篇仍有自己的 Seat，在正文里各写一节：

- **Real2Sim / Sim2Real**：agent 从真实数据重建仿真、在里面练习，再回到真机（RPG、SimEX、Agentic Real2Sim）。
- **VLN 与具身导航**：以导航为主任务的 agent（NavGPT、SayNav、HarnessVLN）。
- **多智能体**：通用模型 agent 协调多个机器人，或系统由分工不同、互相交接工作的多个通用模型 agent 组成（RoCo、SMART-LLM、AutoRT）。

## 四、文献概况：精选清单 186 篇

**来源。** 候选来自三处：

- 14 篇种子论文的前向引用；
- 2026 年的关键词检索；
- 三轮联网补漏。

按摘要粗筛了 12,230 篇，挑出核心表，再对其中 174 篇逐篇读全文判定。之后为了补齐 2025 年，又从扩展列表里挑了 12 篇代表作；扩展列表也是按同一标准读全文补判过的。只收 arXiv 论文。

| 结论 | 篇数 | 说明 |
| --- | --- | --- |
| 保留 | 157 | 先驱（2022–2025）78 篇，其中 2025 年 21 篇；2026 年 79 篇 |
| 资源 | 20 | 以通用 agent 为对象的 benchmark 与评测研究；其中 15 篇评测的是 Controller |
| 剔除 | 9 | 读全文后发现决策者是微调模型（RoboFAC、AgentVLN、Ludi），或主体是数据平台（RoboTwin 2.0、HumanoidGen） |

**保留的 157 篇按 Seat 和角色分：**

| Seat | 角色（篇数） | 先驱 | 2026 |
| --- | --- | --- | --- |
| Designer | 环境/重建 9 · 奖励/任务 13 | 12 | 10 |
| Teacher | 示范/蒸馏 10 | 4 | 6 |
| Developer | 系统/代码 21 · 本体/工具 6 | 7 | 20 |
| Controller | 编排 49 · 写策略 20 · 直接动作 15 | 47 | 37 |
| Supervisor | 监控/恢复 14 | 8 | 6 |

**补的 12 篇 2025 年代表作**（每个角色一两篇，按引用数和对主线的作用挑）：

- Designer：LAMARL、GROVE；
- Teacher：BLAZER；
- Developer：NeSyC、SkillWrapper、RoboMoRe；
- Controller：Manual2Skill、Chain-of-Modality、GenSwarm、SPF；
- Supervisor：FORTRESS、RoboSafe。

**三个专题：**

- Real2Sim / Sim2Real：保留 10 篇（另有 1 篇资源 Video2World）；
- VLN：保留 19 篇；
- 多智能体：13 篇（保留 12、资源 1）。

**可以写进正文的三个观察：**

1. **位置在扩散。** 先驱里六成是 Controller（47/78），并以编排为主，即 SayCan 一类。到了 2026 年，执行前的占比从 29% 升到 46%，Developer 从 7 篇增到 20 篇（ENPIRE、RPG、SimEX 这类 agent 改系统、按试验保留或回滚的工作）。
2. **通用模型开始自己出动作。** 「直接动作」从 6 篇增到 9 篇（Show-Harness、Agent as Policy）。通用模型正在与 VLA 抢同一个位置，这是正文值得展开的争议点。
3. **决策模型变多样。** 先驱大多用 GPT 系列；2026 年 Qwen、Claude、Gemini、Astra 各有约 20 篇用到。开源模型和 harness（工具、记忆、技能库）成为新的变量。

**关于覆盖面。** 按同一套规则补判过扩展列表，会有约一千篇合格；除了补进来的 12 篇，其余都已暂存、先不管。所以正文的措辞应该是「按 Seat 挑选代表作」，而不是「穷尽检索」；上面的篇数只用来描述趋势。

## 五、综述章节结构

正文预计约 20 页（不含参考文献）。每个 Seat 一章，写法统一：

- 先给定义和一张小图：agent 在这个位置产出什么，交给谁；
- 再讲先驱，只讲奠定做法的 2–3 篇；
- 然后讲 2026 年的新工作，按角色分段；
- 最后一张对照表：论文、决策模型、连到 Policy/Code 还是 Env/Sim、是否闭环。

这张表可以直接从清单的 CSV 生成。

| 章 | 内容 | 代表作（先驱 → 2026） | 页数 |
| --- | --- | --- | --- |
| 1 引言 | 从 SayCan、Code as Policies 到 2026：通用模型不再只坐在运行时；本文的三个贡献（定义与收录标准、Seat 框架、公开清单） | — | 1.5 |
| 2 定义与范围 | 回路图、六条标准、不在范围内的（VLA、自动驾驶、纯文本世界）、与相关综述的对比 | — | 1.5 |
| 3 分类框架 | 两个阶段、五个 Seat、归类规则、统计概览 | — | 1 |
| 4 Designer | 环境/重建；奖励/任务 | RoboGen、Eureka → SceneSmith、EmbodiedSmith、RF-Agent | 2 |
| 5 Teacher | 通用模型自己做，经验蒸馏给策略 | RobotGPT、SUDD → GUAVA、CAPEX、SkillWeaver | 1 |
| 6 Developer | 系统/代码（改 harness、技能库、训练代码）；本体/工具 | RoboMorph、PDDLLM → ENPIRE、PhysEvo、Zetta | 2 |
| 7 Controller | 编排；写策略；直接动作 | SayCan、Code as Policies、ReKep → Harness VLA、RoboClaw、Show-Harness | 3.5 |
| 8 Supervisor | 失败检测、安全护栏、恢复与求助 | REFLECT、Code-as-Monitor、RoboGuard → FRAMES、Agentic Task Graph | 1 |
| 9 三个专题 | Real2Sim / Sim2Real；VLN；多智能体 | RPG、SimEX；NavGPT → HarnessVLN；RoCo → ABot-Claw | 2 |
| 10 评测与资源 | 20 个 benchmark 按被评测的 Seat 整理 | EmbodiedBench、SafeAgentBench、ASIMOV | 1 |
| 11 讨论与开放问题 | 见下 | — | 1.5 |
| 12 结论 | — | — | 0.5 |

**第 11 章打算写的四个问题**（都能从清单里找到依据）：

- **通用模型和 VLA 的边界。** 「直接动作」一类在增加，而 Harness VLA 又把 VLA 当工具。两条路线会不会合并？
- **Harness 是新的研究对象。** 2026 年不少工作改的不是模型，而是工具、记忆和技能库（Developer 的增长就在这里）。
- **评测的缺口。** 20 个资源里 15 个评测 Controller；Designer、Developer 各只有 1 个，Teacher 没有。执行前的 Seat 几乎无人评测。
- **安全与闭环。** Supervisor 只有 14 篇；开环的 Controller 在真机上怎么兜底。

## 六、待讨论的问题

下面这些会影响正文怎么写。每条写了我的建议，等你定。

1. **主线。** 建议用「Agency spreads around the body」，第三、四节的数字能支撑它。备选是不提论点、只按 Seat 中性梳理，更稳妥，但读起来像目录。
2. **写多深（已定：A）。** 建议每个角色详写 3–5 篇代表作，其余进对照表，正文约 20 页。备选 B 是全部论文都在正文里讨论，篇幅大约翻倍。
3. **2025 年的断档（已补）。** 从暂存的 291 篇 2025 年保留论文里，按引用数和对主线的作用，每个角色挑一两篇，复查判定后补了 12 篇（名单见第四节）。精选现在 186 篇，其中 2025 年 21 篇。另有 3 篇看过后没收：GenDexHand 的主体接近数据生成平台；UAV-VLA 只离线生成飞行计划；Agentic Robot 运行时的进度判断和恢复由微调的验证器做。
4. **边界案例**（上一轮留下的）：
   - GPT-6 Astra on RoboDojo：全文判为评测研究、放在资源；但你举过它做「直接动作」的例子，要不要改为保留？
   - AutoRT、RoboGen、SUDD、RobotGPT：现在保留；
   - Tool-Aligned VLA Agent：现在剔除；
   - VLABench、ASIMOV：两个模型给过相反的结论，值得你看一眼。
5. **多智能体的定义。** 现在「多个分工不同的通用模型 agent」也算。精选里只有 13 篇，影响不大；但在扩展列表里这条会收进一两百篇。建议收紧到「协调多个机器人」为主。
6. **游戏环境**（Minecraft、Overcooked）算不算具身。我按六条规则正常判了，你还没表态。
7. **发表形式。** 是 arXiv 英文综述，还是投期刊？这决定篇幅上限，以及要不要与相关综述做系统对比。

## 七、下一步

讨论定下第六节的问题之后，按这个顺序推进：

1. **生成论文卡片。** 从清单的 CSV 为每篇保留的论文生成一张卡片，内容包括：
   - 做了什么；
   - agent 在哪个位置；
   - 决策模型；
   - 连到哪里；
   - 一句原文证据。

   写正文时从卡片里取材，不重新读。
2. **先写两章样章。** Controller 最大、先驱最熟；Developer 增长最快，最能体现主线。你确认写法和深度后再铺开其余各章。
3. **画图。** 回路图（你手绘的版本重绘）、Seat 图（第三节这张的正式版）、先驱到 2026 的代表作时间线。
4. **补文献信息。** 发表场所、BibTeX、代码和项目链接；同步更新 README 的 awesome list。
5. **其余各章、引言和讨论。** 最后统一术语（Seat、角色的中英文对照），再通读一遍。

清单现在是精选的 186 篇，含补的 12 篇 2025 年代表作（`data/core/paper_list.csv`）。补判过的其余 1,339 篇暂存在 `data/core/extended_judged.csv`，先不动。
