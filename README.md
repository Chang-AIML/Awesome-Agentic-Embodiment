# Awesome Agentic Embodiment

> *Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs, not embodied action models — acting as agents that make explicit decisions and are connected to a robot body — through the policy, code or plans they produce, or by acting on the environment directly. Its organizing question is where such an agent sits relative to the body's deployed policy — steering it, guarding it, teaching it, designing its learning problem, or building its system (**Seat**).*

**Thesis (draft, under revision).** *Agency spreads around the body: general models, not embodied action models, fill seat after seat.*

Each seat is traced from its **67 pioneers (2022–2025)** to **79 papers from 2026**, the year most of the field's papers appeared; VLN / embodied navigation (11 from 2026) has its own chapter and the Real2Sim / Sim2Real sub-direction a short section (9), plus **24 benchmarks and resources**. Definition and inclusion rules: [docs/definition.md](docs/definition.md) (Chinese).

## Scope and what counts as an agent

**Scope.** General-purpose foundation models (LLMs / VLMs such as GPT, Gemini, Claude, Qwen-VL, GPT-6 Astra) doing embodied work as agents. They may plan, call skills, tools or VLAs, write code or constraints, or emit actions directly (LLM-as-policy, e.g. GPT-6 Astra evaluated as a robot policy on RoboDojo). A general model fine-tuned for an agent role still counts if it keeps acting through an agent interface (e.g. GUAVA). **Embodied foundation models that produce actions are not included** — VLAs (also with reasoning, memory or self-correction), hierarchical VLAs, world action models, robot foundation models (π0.5, ECoT, OneTwoVLA, Hi Robot, Gemini Robotics, PaLM-E); they appear here only as tools called by an agent.

**Agent tests**: (1) **a general model is the agent** and makes **explicit decisions** — plans, skill/tool/VLA calls, code, constraints, verdicts, system edits, or actions; (2) **decision authority** — the model writes its options, or picks among them with a control action (stop / retry / replan / ask / keep-revert); (3) **it is connected to the body** — what it decides reaches the policy / code layer or the environment, and the agent loop is the paper's main contribution (data-generation platforms are not included). Closing the loop is **recorded, not required**: *Loop* = re-decide (the model is called again with its earlier decisions and their consequences), authored (the constraints or program it wrote read live perception and adapt, e.g. ReKep, VoxPoser, Code as Policies) or none (open loop, e.g. ZS-Planners, CoPa). The share of closed-loop papers rises every year (see `docs/core_stats.md`).

Also not included: scalar reward/value models, one-shot annotators, world-model foresight, game/text worlds, purely digital agents.

## Seat by period

| Seat | Phase | Pioneers 2022–2025 | 2026 | of which fine-tuned (C) |
|---|---|---|---|---|
| Controller | runtime | 42 | 40 | 3 |
| Supervisor | runtime | 7 | 7 | 1 |
| Teacher | pre-deployment | 3 | 6 | 2 |
| Designer | pre-deployment | 11 | 10 | · |
| Developer | pre-deployment | 4 | 16 | · |

Counts include the papers of the Real2Sim / Sim2Real and VLN chapters under their seats.

**Legend.** *Carrier* — **G** general model used as-is, **C** general model fine-tuned or distilled for an agent role, still acting through tools, skills, code or plans (→ marks migration, e.g. G→C). *Topology* — ×1 single agent, ×R role agents on one task, ×N one agent per robot, 1:N one decider for many robots, ×O agents owning branches of a campaign. *Loop* — **re-decide**: the model is called again with its own decisions and their consequences; **authored**: constraints or a program written by the model read live perception and adapt while the robot acts (e.g. ReKep re-solves its keypoint constraints and backtracks when one breaks); **none**: written once (kept for pioneers and for the two exceptions). *Closure* — evidence the loop uses: E execution, H human.

## Contents

- [Controller · Orchestrators](#controller--orchestrators)
- [Controller · Direct drivers](#controller--direct-drivers)
- [Controller · Lifelong / memory agents](#controller--lifelong--memory-agents)
- [Supervisor](#supervisor)
- [Teacher](#teacher)
- [Designer](#designer)
- [Developer](#developer)
- [Sub-direction: Real2Sim / Sim2Real](#sub-direction-real2sim--sim2real)
- [VLN and embodied navigation](#vln-and-embodied-navigation)
- [Benchmarks and resources](#benchmarks-and-resources)
- [More 2026 papers (830)](#more-2026-papers)
- [More papers from 2022–2025 (902)](#more-papers-from-20222025)

## Controller · Orchestrators

Called during evaluated episodes; sequence skills, tools or VLAs-as-tools.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **ZS-Planners** | [Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents](https://arxiv.org/abs/2201.07207) [[project]](https://huangwl18.github.io/language-planner) | 2022 | ICML | G | skill-call | ×1 | none | none | other/sim | – |
| **Socratic Models** | [Socratic Models: Composing Zero-Shot Multimodal Reasoning with Language](https://arxiv.org/abs/2204.00598) [[project]](https://socraticmodels.github.io/) | 2022 | ICLR | G | skill-call | ×1 | none | none | manip/sim+real | – |
| **SayCan** | [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691) [[project]](https://say-can.github.io/) | 2022 | CoRL | G | skill-call | ×1 | re-decide | E | mobile-manip/real | – |
| **Inner Monologue** | [Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608) [[project]](https://innermonologue.github.io) | 2022 | CoRL | G | skill-call | ×1 | re-decide | E+H | manip/sim+real | – |
| **Text2Motion** | [Text2Motion: From Natural Language Instructions to Feasible Plans](https://arxiv.org/abs/2303.12153) [[project]](https://sites.google.com/stanford.edu/text2motion) | 2023 | Autonomous Robots | G | skill-call | ×1 | none | M | manip/sim+real | – |
| **TidyBot** | [TidyBot: Personalized Robot Assistance with Large Language Models](https://arxiv.org/abs/2305.05658) [[project]](https://tidybot.cs.princeton.edu) | 2023 | IROS | G | skill-call | ×1 | none | none | mobile-manip/real | – |
| **KnowNo** | [Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners](https://arxiv.org/abs/2307.01928) | 2023 | CoRL | G | skill-call | ×1 | none | M | mobile-manip/sim+real | Supervisor |
| **RoCo** | [RoCo: Dialectic Multi-Robot Collaboration with Large Language Models](https://arxiv.org/abs/2307.04738) | 2023 | ICRA | G | skill-call | ×N | re-decide | E | multi-robot/sim+real | – |
| **SayPlan** | [SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135) [[project]](https://sayplan.github.io) | 2023 | CoRL | G | skill-call | ×1 | re-decide | E | mobile-manip/sim+real | – |
| **SMART-LLM** | [SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models](https://arxiv.org/abs/2309.10062) | 2023 | IROS | G | code | 1:N | none | none | multi-robot/sim+real | – |
| **Look Before You Leap** | [Look Before You Leap: Unveiling the Power of GPT-4V in Robotic Vision-Language Planning](https://arxiv.org/abs/2311.17842) | 2023 | arXiv | G | skill-call | ×1 | re-decide | E | manip/sim+real | – |
| **ORGANA** | [ORGANA: A Robotic Assistant for Automated Chemistry Experimentation and Characterization](https://arxiv.org/abs/2401.06949) | 2024 | Matter | G | skill-call | ×1 | re-decide | E+H | manip/real | – |
| **LLM3** | [LLM3:Large Language Model-based Task and Motion Planning with Motion Failure Reasoning](https://arxiv.org/abs/2403.11552) [[code]](https://github.com/AssassinWS/LLM-TAMP) | 2024 | IROS | G | skill-call | ×1 | re-decide | E | manip/sim | – |
| **COME-robot** | [Closed-Loop Open-Vocabulary Mobile Manipulation with GPT-4V](https://arxiv.org/abs/2404.10220) [[project]](https://come-robot.github.io/) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | mobile-manip/real | – |
| **VLM-PC** | [Commonsense Reasoning for Legged Robot Adaptation with Vision-Language Models](https://arxiv.org/abs/2407.02666) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | loco/real | – |
| **BUMBLE** | [BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | mobile-manip/real | – |
| **Being-0** | [Being-0: A Humanoid Robotic Agent with Vision-Language Models and Modular Skills](https://arxiv.org/abs/2503.12533) | 2025 | arXiv | G | skill-call | ×R | re-decide | E | humanoid/real | – |
| **AquaChat** | [AquaChat: An LLM-Guided ROV Framework for Adaptive Inspection of Aquaculture Net Pens](https://arxiv.org/abs/2507.16841) | 2025 | Aquacultural Engineering | G | skill-call | ×1 | re-decide | E | other/sim+real | – |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **NovaPlan** | [NovaPlan: Zero-Shot Long-Horizon Manipulation via Closed-Loop Video Language Planning](https://arxiv.org/abs/2602.20119) [[project]](https://nova-plan.github.io/) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | manip/real | – |
| **Cybo-Waiter** | [Cybo-Waiter: A Physical Agentic Framework for Humanoid Whole-Body Locomotion-Manipulation](https://arxiv.org/abs/2603.10675) | 2026 | arXiv | G | skill-call | ×1 | authored | E | humanoid/real | – |
| **RoboClaw** | [RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks](https://arxiv.org/abs/2603.11558) [[code]](https://github.com/RoboClaw-Robotics/RoboClaw) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | manip/real | Teacher |
| **ABot-Claw** | [ABot-Claw: A Foundation for Persistent, Cooperative, and Self-Evolving Robotic Agents](https://arxiv.org/abs/2604.10096) | 2026 | arXiv | G | skill-call | 1:N | re-decide | E | multi-robot/real | Supervisor |
| **SpaceMind** | [SpaceMind: A Modular and Self-Evolving Embodied Vision-Language Agent Framework for Autonomous On-orbit Servicing](https://arxiv.org/abs/2604.14399) [[code]](https://github.com/wuaodi/SpaceMind) | 2026 | Acta Astronautica | G | skill-call | ×1 | re-decide | E | other/sim+real | – |
| **Tool-Aligned VLA Agent** | [Towards Long-horizon Embodied Agents with Tool-Aligned Vision-Language-Action Models](https://arxiv.org/abs/2605.13119) | 2026 | arXiv | G | vla-call | ×1 | re-decide | E | manip/sim+real | – |
| **AerialClaw** | [AerialClaw: An Open-Source Framework for LLM-Driven Autonomous Aerial Agents](https://arxiv.org/abs/2606.12142) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | aerial/sim | – |
| **Physical Agency** | [Addressing the Orchestration Gap in Generalist Robots via Physical Agency](https://arxiv.org/abs/2607.21725) | 2026 | arXiv | G | vla-call | ×1 | re-decide | E | manip/sim+real | – |
| **Thea** | [Towards the Harness of Embodied Agents](https://arxiv.org/abs/2608.11246) [[project]](https://eit-hai.github.io/thea) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | mobile-manip/real | Supervisor |
| **Ludi** | [Ludi${}_{\scriptscriptstyle 0.1}$: An Agentic System for Socially Intelligent Robots](https://arxiv.org/abs/2608.22035) | 2026 | arXiv | C | skill-call | ×1 | re-decide | E+H | mobile-manip/real | – |
| **Smart-Agriculture Engine** | [Deploying and Evaluating a Smart-Agriculture Agentic Engine for Full-Season Soybean Farm Operations](https://arxiv.org/abs/2609.00106) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | other/real | – |
| **AGRO-SUVIDE** | [AGRO-SUVIDE: Agentic Robotics for Surgical Viscoelastic Debridement](https://arxiv.org/abs/2609.34823) | 2026 | arXiv | G | skill-call | ×1 | authored | E | manip/real | Developer |
| **Astra Robot Agents** | [Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens](https://arxiv.org/abs/2610.01939) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim | – |

## Controller · Direct drivers

Called during evaluated episodes; emit actions, semantic micro-actions, native commands, or code and constraints executed now.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **Code as Policies** | [Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753) | 2022 | ICRA | G | code | ×1 | authored | E | manip/sim+real | – |
| **ProgPrompt** | [ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302) | 2022 | ICRA | G | code | ×1 | authored | E | manip/sim+real | – |
| **ChatGPT for Robotics** | [ChatGPT for Robotics: Design Principles and Model Abilities](https://arxiv.org/abs/2306.17582) | 2023 | IEEE Access | G | code | ×1 | authored | E+H | aerial/sim+real | – |
| **AutoTAMP** | [AutoTAMP: Autoregressive Task and Motion Planning with LLMs as Translators and Checkers](https://arxiv.org/abs/2306.06531) | 2023 | ICRA | G | constraint | ×1 | re-decide | E | manip/sim | – |
| **Language to Rewards** | [Language to Rewards for Robotic Skill Synthesis](https://arxiv.org/abs/2306.08647) [[project]](https://language-to-reward.github.io/) | 2023 | CoRL | G | constraint | ×1 | authored | E | manip/sim+real | – |
| **VoxPoser** | [VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973) | 2023 | CoRL | G | constraint | ×1 | authored | E | manip/sim+real | – |
| **Prompt a Robot to Walk** | [Prompt a Robot to Walk with Large Language Models](https://arxiv.org/abs/2309.09969) | 2023 | IEEE Conference on Decision and Control | G | micro-action | ×1 | re-decide | E | loco/sim | – |
| **TypeFly** | [TypeFly: Flying Drones with Large Language Model](https://arxiv.org/abs/2312.14950) | 2023 | arXiv | G | code | ×1 | authored | E | aerial/real | – |
| **MOKA** | [MOKA: Open-World Robotic Manipulation through Mark-Based Visual Prompting](https://arxiv.org/abs/2403.03174) | 2024 | RSS | G | constraint | ×1 | none | none | manip/real | – |
| **CoPa** | [CoPa: General Robotic Manipulation through Spatial Constraints of Parts with Foundation Models](https://arxiv.org/abs/2403.08248) | 2024 | IROS | G | constraint | ×1 | none | none | manip/real | – |
| **ReKep** | [ReKep: Spatio-Temporal Reasoning of Relational Keypoint Constraints for Robotic Manipulation](https://arxiv.org/abs/2409.01652) | 2024 | CoRL | G | constraint | ×1 | authored | E | mobile-manip/real | – |
| **OmniManip** | [OmniManip: Towards General Robotic Manipulation via Object-Centric Interaction Primitives as Spatial Constraints](https://arxiv.org/abs/2501.03841) | 2025 | CVPR | G | constraint | ×1 | authored | E | manip/real | – |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **VLS** | [VLS: Steering Pretrained Robot Policies via Vision-Language Models](https://arxiv.org/abs/2602.03973) [[project]](https://vision-language-steering.github.io/webpage/) | 2026 | arXiv | G | constraint | ×1 | authored | E | manip/sim+real | – |
| **CaP-X** | [CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation](https://arxiv.org/abs/2603.22435) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim+real | Developer |
| **Embodiment Meets Environment** | [Embodiment Meets Environment: Toward Context-Aware, Safe Physical Caregiving Robots](https://arxiv.org/abs/2606.28592) | 2026 | Robotics | G | constraint | ×1 | authored | E | manip/sim+real | – |
| **VIA** | [VIA: Visual Interface Agent for Robot Control](https://arxiv.org/abs/2607.11119) | 2026 | arXiv | G | micro-action | ×1 | re-decide | E | manip/sim+real | – |
| **GTA-2** | [GTA-2: A Multi-VLM Framework for Synthesizing Robot Manipulation Skills via Grounded Task Axes](https://arxiv.org/abs/2609.09808) | 2026 | arXiv | G | constraint | ×R | none | none | manip/real | – |
| **Show-Harness** | [Show-Harness: Just a VLM Agent Can Play Robots](https://arxiv.org/abs/2609.10522) [[project]](https://showlab.github.io/Show-Harness) | 2026 | arXiv | G | micro-action | ×1 | re-decide | E | manip/sim+real | – |
| **Agent as Policy** | [Agent as Policy for Robotic Manipulation](https://arxiv.org/abs/2609.12541) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/real | – |
| **AquaCap** | [AquaCap: A Training-Free Underwater Embodied Agent with Code-as-Policy](https://arxiv.org/abs/2609.23133) | 2026 | arXiv | G | code | ×1 | re-decide | E | other/sim+real | – |
| **KPI** | [KPI: A Promptable Kernel for Physical Interaction on Humanoids](https://arxiv.org/abs/2609.36151) [[project]](https://kpi-robot.github.io/) | 2026 | arXiv | G | constraint | ×1 | authored | E | humanoid/sim+real | – |
| **OpenRUA** | [OpenRUA: Robot-Use Agents Are Zero-Shot Visuomotor Policies](https://arxiv.org/abs/2610.02459) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim+real | – |

## Controller · Lifelong / memory agents

Improve memory, skill libraries or harness across evaluated episodes.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **Incremental Humanoid Learning** | [Incremental Learning of Humanoid Robot Behavior from Natural Interaction and Large Language Models](https://arxiv.org/abs/2309.04316) [[project]](https://youtu.be/y5O2mRGtsLM) | 2023 | Frontiers Robotics AI | G | code | ×1 | re-decide | E+H | humanoid/real | – |
| **DROC** | [Distilling and Retrieving Generalizable Knowledge for Robot Manipulation via Language Corrections](https://arxiv.org/abs/2311.10678) [[project]](https://sites.google.com/stanford.edu/droc) | 2023 | ICRA | G | code | ×1 | re-decide | H | manip/real | – |
| **LRLL** | [Lifelong Robot Library Learning: Bootstrapping Composable and Generalizable Skills for Embodied Control with Language Models](https://arxiv.org/abs/2406.18746) | 2024 | ICRA | G | code | ×1 | re-decide | E | manip/sim | Developer |
| **ReMEmbR** | [ReMEmbR: Building and Reasoning Over Long-Horizon Spatio-Temporal Memory for Robot Navigation](https://arxiv.org/abs/2409.13682) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | nav/real | – |
| **RoboMemory** | [RoboMemory: A Brain-inspired Multi-memory Agentic Framework for Interactive Environmental Learning in Physical Embodied Systems](https://arxiv.org/abs/2508.01415) | 2025 | arXiv | G | skill-call | ×1 | re-decide | E | mobile-manip/sim+real | – |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **PhysMem** | [PhysMem: Scaling Test-Time Memory for Embodied Physical Reasoning](https://arxiv.org/abs/2602.20323) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | manip/sim+real | – |
| **Harness VLA** | [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](https://arxiv.org/abs/2607.08448) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim | – |
| **Teach and Grow** | [Teach and Grow: An Agent-Centered Architecture for General Robot Learning](https://arxiv.org/abs/2608.17209) [[project]](https://tgl.changnie.top) | 2026 | arXiv | G | code | ×1 | authored | E+H | manip/real | – |
| **MessyMem** | [MessyMem: Learning-from-Doing Memory for Mobile Manipulation](https://arxiv.org/abs/2609.15976) [[project]](https://messymem.github.io) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | mobile-manip/sim+real | – |
| **GPT-6-Astra XLeRobot** | [Robot Manipulation with GPT-6-Astra: Body Knowledge, Experience Reuse, Emergent Skills, and Sim2Real Transfer](https://arxiv.org/abs/2609.31770) [[code]](https://github.com/hesd10/astra-robot-sim2real) | 2026 | arXiv | G | code | ×1 | re-decide | E | mobile-manip/sim+real | – |
| **CaP Great Again** | [Make Code as Policy Great Again: Frontier Agents Write, Call, and Evolve Robot Tools](https://arxiv.org/abs/2609.39018) | 2026 | arXiv | G | skill-call | ×R | re-decide | E+H | manip/sim+real | Developer |
| **Robo-COP** | [Co-Evolving Robot Orchestrators and Policies through Deployment](https://arxiv.org/abs/2610.09228) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim+real | Developer |

## Supervisor

Runtime, acts only on exceptions: gates, vetoes, failure detection and recovery, by a separate check process.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **REFLECT** | [REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction](https://arxiv.org/abs/2306.15724) [[project]](https://robot-reflect.github.io/) | 2023 | CoRL | G | verdict | ×1 | re-decide | E | manip/sim+real | Controller |
| **DoReMi** | [DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329) | 2023 | IROS | G | verdict | ×R | re-decide | E | manip/sim+real | Controller |
| **Safety Chip** | [Plug in the Safety Chip: Enforcing Constraints for LLM-driven Robot Agents](https://arxiv.org/abs/2309.09919) | 2023 | ICRA | G | constraint | ×1 | authored | E | mobile-manip/sim+real | – |
| **Real-Time Anomaly Detection** | [Real-Time Anomaly Detection and Reactive Planning with Large Language Models](https://arxiv.org/abs/2407.08735) | 2024 | RSS | G | verdict | ×1 | none | none | aerial/sim+real | – |
| **Code-as-Monitor** | [Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection](https://arxiv.org/abs/2412.04455) [[project]](https://zhoues.github.io/Code-as-Monitor/) | 2024 | CVPR | G | verdict | ×1 | re-decide | E | manip/sim+real | Controller |
| **RoboGuard** | [Safety Guardrails for LLM-Enabled Robots](https://arxiv.org/abs/2503.07885) | 2025 | RA-L | G | constraint | ×1 | authored | E | nav/sim+real | – |
| **RoboFAC** | [RoboFAC: A Comprehensive Framework for Robotic Failure Analysis and Correction](https://arxiv.org/abs/2505.12224) | 2025 | arXiv | C | verdict | ×1 | re-decide | E | manip/sim+real | – |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **Contextual Safety Reasoning** | [Contextual Safety Reasoning and Grounding for Open-World Robots](https://arxiv.org/abs/2602.19983) | 2026 | arXiv | G | constraint | ×1 | authored | E | nav/sim+real | – |
| **When to Act, Ask, or Learn** | [When to Act, Ask, or Learn: Uncertainty-Aware Policy Steering](https://arxiv.org/abs/2602.22474) | 2026 | Robotics | G | verdict | ×1 | re-decide | E+H | manip/sim+real | Controller |
| **Agentic Task Graph** | [From Reaction to Anticipation: Proactive Failure Recovery through Agentic Task Graph for Robotic Manipulation](https://arxiv.org/abs/2605.11951) | 2026 | Robotics | G | code | ×R | authored | E | manip/sim+real | Controller |
| **UAV Selective Recovery** | [Selective Agentic Recovery for UAV Autonomy with a Persistent Mission Runtime](https://arxiv.org/abs/2606.14219) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | aerial/sim+real | – |
| **Zetta** | [Zetta $ζ$: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence](https://arxiv.org/abs/2608.16590) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim | Developer |
| **FRAMES** | [FRAMES: Failure Recovery And Monitoring of Embodied Skills for Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.22538) | 2026 | arXiv | G | verdict | ×R | re-decide | E | humanoid/sim+real | Controller |
| **Beyond Human Demos** | [Learning Beyond What Humans Can Demonstrate](https://arxiv.org/abs/2609.24996) [[project]](http://guardrail-policy.github.io/) | 2026 | arXiv | G | constraint | ×1 | authored | E | manip/sim | Developer |

## Teacher

Before deployment, the agent acts; its outcome-checked behaviour becomes the deployed model's training target.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **SUDD** | [Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition](https://arxiv.org/abs/2307.14535) [[project]](https://www.cs.columbia.edu/~huy/scalingup/) | 2023 | CoRL | G | skill-call | ×1 | authored | E | manip/sim | Designer |
| **RobotGPT** | [RobotGPT: Robot Manipulation Learning from ChatGPT](https://arxiv.org/abs/2312.01421) | 2023 | RA-L | G | code | ×1 | re-decide | E | manip/sim+real | – |
| **Manipulate-Anything** | [Manipulate-Anything: Automating Real-World Robots using Vision-Language Models](https://arxiv.org/abs/2406.18915) [[project]](https://robot-ma.github.io/) | 2024 | CoRL | G | skill-call | ×1 | re-decide | E | manip/sim+real | Controller |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **GUAVA** | [Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness](https://arxiv.org/abs/2606.18363) | 2026 | arXiv | G→C | trace | ×1 | re-decide | E | manip/sim+real | Controller |
| **CAPEX** | [CAPEX: Efficiently Distilling Foundation Model Behavior into Deployable Robot Policies through Experience-Adaptive Reasoning](https://arxiv.org/abs/2609.33007) | 2026 | arXiv | G | trace | ×1 | re-decide | E | manip/sim+real | – |
| **RHD** | [Recursive Harness Distillation across Agents for Robot Manipulation](https://arxiv.org/abs/2609.33378) | 2026 | arXiv | G | trace | ×R | re-decide | E | manip/sim+real | Controller |
| **SkillWeaver** | [SkillWeaver: Agentic Exploration over Neural Interaction Skills for Scalable Robot Data Generation](https://arxiv.org/abs/2609.36171) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | manip/sim | – |
| **Frontier Demo Generation** | [Bridging Frontier Reasoning and Robot Execution: From Autonomous Demonstration Generation to Dense Language Supervision](https://arxiv.org/abs/2610.03615) | 2026 | arXiv | G | trace | ×1 | re-decide | E | manip/sim+real | Controller |

## Designer

Before deployment, the agent designs the learning problem: rewards, tasks, environments, curricula, eval suites.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **Text2Reward** | [Text2Reward: Reward Shaping with Language Models for Reinforcement Learning](https://arxiv.org/abs/2309.11489) | 2023 | ICLR | G | problem-spec | ×1 | none | none | manip/sim+real | – |
| **GenSim** | [GenSim: Generating Robotic Simulation Tasks via Large Language Models](https://arxiv.org/abs/2310.01361) [[project]](https://liruiw.github.io/gensim) [[code]](https://github.com/liruiw/GenSim) | 2023 | ICLR | G | problem-spec | ×1 | none | none | manip/sim+real | – |
| **Eureka** | [Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931) [[project]](https://eureka-research.github.io/) | 2023 | ICLR | G | problem-spec | ×1 | re-decide | E | manip/sim | – |
| **RoboGen** | [RoboGen: Towards Unleashing Infinite Data for Automated Robot Learning via Generative Simulation](https://arxiv.org/abs/2311.01455) | 2023 | ICML | G | problem-spec | ×1 | none | none | manip/sim | – |
| **Agentic Skill Discovery** | [Agentic Skill Discovery](https://arxiv.org/abs/2405.15019) [[project]](https://agentic-skill-discovery.github.io/) | 2024 | Robotics Auton. Syst. | G | problem-spec | ×R | re-decide | E | manip/sim+real | Developer |
| **OMNI-EPIC** | [OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code](https://arxiv.org/abs/2405.15568) | 2024 | arXiv | G | problem-spec | ×R | re-decide | E | loco/sim | – |
| **CurricuLLM** | [CurricuLLM: Automatic Task Curricula Design for Learning Complex Robot Skills using Large Language Models](https://arxiv.org/abs/2409.18382) | 2024 | ICRA | G | problem-spec | ×1 | re-decide | E | humanoid/sim | – |
| **Eurekaverse** | [Eurekaverse: Environment Curriculum Generation via Large Language Models](https://arxiv.org/abs/2411.01775) [[project]](https://eureka-research.github.io/eurekaverse) | 2024 | CoRL | G | problem-spec | ×1 | re-decide | E | loco/sim+real | – |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **SceneSmith** | [SceneSmith: Agentic Generation of Simulation-Ready Indoor Scenes](https://arxiv.org/abs/2602.09153) [[project]](https://scenesmith.github.io/) | 2026 | arXiv | G | problem-spec | ×R | re-decide | E | manip/sim | – |
| **SAGE** | [SAGE: Scalable Agentic 3D Scene Generation for Embodied AI](https://arxiv.org/abs/2602.10116) [[project]](https://research.nvidia.com/labs/dir/sage/) | 2026 | arXiv | G | problem-spec | ×1 | re-decide | E | manip/sim | – |
| **RF-Agent** | [RF-Agent: Automated Reward Function Design via Language Agent Tree Search](https://arxiv.org/abs/2602.23876) [[code]](https://github.com/deng-ai-lab/RF-Agent) | 2026 | NeurIPS | G | problem-spec | ×1 | re-decide | E | manip/sim | – |
| **RDA** | [RDA: Reward Design Agent for Reinforcement Learning](https://arxiv.org/abs/2606.01672) | 2026 | arXiv | G | problem-spec | ×1 | re-decide | E | manip/sim | – |
| **FIND** | [Find Something You Can't Do: Agentic Real-World Reinforcement Learning for Self-Improving VLA Models](https://arxiv.org/abs/2609.32069) | 2026 | arXiv | G | problem-spec | ×1 | re-decide | E | manip/real | – |
| **ROOT** | [ROOT: Discovering Rewards for User-Specified Embodied Behaviors](https://arxiv.org/abs/2610.04250) | 2026 | arXiv | G | problem-spec | ×1 | re-decide | E | loco/sim | – |

## Developer

Before deployment, the agent edits the solution: policy code, skill libraries, harness, training code, hardware; keeps or reverts by its own experiments.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **RoboMorph** | [RoboMorph: Evolving Robot Morphology using Large Language Models](https://arxiv.org/abs/2407.08626) | 2024 | ICRA | G | system-edit | ×1 | re-decide | E | loco/sim | – |
| **PDDLLM** | [One Demo Is All It Takes: Planning Domain Derivation with LLMs from A Single Demonstration](https://arxiv.org/abs/2505.18382) | 2025 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim | – |
| **RobotSmith** | [RobotSmith: Generative Robotic Tool Design for Acquisition of Complex Manipulation Skills](https://arxiv.org/abs/2506.14763) | 2025 | NeurIPS | G | system-edit | ×R | re-decide | E | manip/sim+real | Designer |
| **VLMgineer** | [VLMgineer: Vision Language Models as Robotic Toolsmiths](https://arxiv.org/abs/2507.12644) [[project]](https://vlmgineer.github.io/release) | 2025 | arXiv | G | code | ×1 | re-decide | E | manip/sim | – |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **HARBOR** | [HARBOR: A Harness Framework for Agentic Robot Reinforcement Learning](https://arxiv.org/abs/2606.08610) | 2026 | arXiv | G | system-edit | ×R | re-decide | E | manip/sim | Designer |
| **RHO** | [RHO: Your Coding Agent is Secretly a Roboticist](https://arxiv.org/abs/2606.16458) [[project]](https://rho-robotics.github.io) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim | – |
| **RATs (Playful)** | [Playful Agentic Robot Learning](https://arxiv.org/abs/2606.19419) [[project]](https://playful-rats.github.io/) | 2026 | arXiv | G | system-edit | ×R | re-decide | E | manip/sim+real | Controller |
| **ENPIRE** | [ENPIRE: Agentic Robot Policy Self-Improvement in the Real World](https://arxiv.org/abs/2606.19980) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/real | – |
| **SPINE** | [SPINE: Bridging the Cyber-Physical Gap with Agentic AI](https://arxiv.org/abs/2607.13049) | 2026 | arXiv | G | system-edit | ×R | re-decide | E+H | manip/real | – |
| **ASPIRE** | [ASPIRE: Agentic /Skills Discovery for Robotics](https://arxiv.org/abs/2607.00272) [[project]](https://research.nvidia.com/labs/gear/aspire/) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim+real | Controller |
| **Skill-Harness Evolution** | [Self-Evolving Embodied Agents via Skill-Harness Evolution](https://arxiv.org/abs/2608.11350) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim | Controller |
| **Continuum Robot Design** | [Bridging Language and Physics: Automated Design of Continuum Robots with Large Language Models](https://arxiv.org/abs/2609.08220) | 2026 | Robotics | G | system-edit | ×R | re-decide | E+H | other/sim | – |
| **AdaHVLA** | [AdaHVLA: Adaptive Harnesses for Long-Horizon Vision-Language-Action Execution](https://arxiv.org/abs/2609.29204) | 2026 | arXiv | G | system-edit | ×R | re-decide | E | manip/sim+real | Controller |
| **PhysEvo** | [PhysEvo: Astra Can Act, Let It](https://arxiv.org/abs/2610.08995) | 2026 | arXiv | G | system-edit | ×R | re-decide | E | manip/sim+real | Controller |
| **LACE-CRAFT** | [LACE-CRAFT: Robot Co-Design with Actor Inheritance and Blackboard Collaboration](https://arxiv.org/abs/2610.09283) [[project]](https://deemostech.github.io/lace-craft/) | 2026 | arXiv | G | system-edit | ×R | re-decide | E | loco/sim+real | Designer |

## Sub-direction: Real2Sim / Sim2Real

One sub-direction that cuts across Designer and Developer: agents that build or calibrate simulators from the real world (Real2Sim), transfer what they learned in simulation to the real robot (Sim2Real), or practise in a reconstructed simulator and go back to the real one (Real2Sim2Real). Only representative papers are listed here; further ones are in *More 2026 papers*.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **DrEureka** | [DrEureka: Language Model Guided Sim-To-Real Transfer](https://arxiv.org/abs/2406.01967) [[project]](https://eureka-research.github.io/dr-eureka/) | 2024 | RSS | Designer | G | problem-spec | re-decide | loco/sim+real | – |
| **Articulate AnyMesh** | [Articulate AnyMesh: Open-Vocabulary 3D Articulated Objects Modeling](https://arxiv.org/abs/2502.02590) | 2025 | arXiv | Designer | G | problem-spec | none | manip/sim+real | – |
| **Video2Policy** | [Video2Policy: Scaling up Manipulation Tasks in Simulation through Internet Videos](https://arxiv.org/abs/2502.09886) | 2025 | arXiv | Designer | G | problem-spec | re-decide | manip/sim | – |

**2026**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **Vid2Sid** | [Vid2Sid: Videos Can Help Close the Sim2Real Gap](https://arxiv.org/abs/2602.19359) | 2026 | arXiv | Designer | G | problem-spec | re-decide | other/sim+real | – |
| **Agentic Real2Sim** | [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](https://arxiv.org/abs/2607.19190) | 2026 | arXiv | Designer | G | problem-spec | re-decide | manip/sim+real | – |
| **CoDimRecon** | [CoDimRecon: Agentic Reconstruction of Sim-Ready 3D Scenes with Deformable Curves, Surfaces, and Volumes](https://arxiv.org/abs/2609.36024) [[project]](https://shuzhaoxie.github.io/CoDimRecon/) | 2026 | arXiv | Designer | G | problem-spec | re-decide | manip/sim | – |
| **Real2Gym** | [Real2Gym: Building Gyms from Videos, Bringing Skills to Robots](https://arxiv.org/abs/2609.37089) [[project]](https://real2gym.github.io/) | 2026 | arXiv | Developer | G | code | re-decide | manip/sim+real | Designer |
| **SimEX** | [SimEX: Simulation-Integrated Robotics AutoResearch](https://arxiv.org/abs/2609.38982) | 2026 | arXiv | Developer | G | system-edit | re-decide | manip/sim+real | Designer |
| **RPG** | [Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents](https://arxiv.org/abs/2610.02204) | 2026 | arXiv | Developer | G | system-edit | re-decide | manip/sim+real | Controller |
| **Skill2Real** | [Skill2Real: Agentic Skill Learning for Zero-Shot Sim-to-Real Robot Manipulation](https://arxiv.org/abs/2610.02788) | 2026 | arXiv | Developer | G | system-edit | re-decide | manip/sim+real | Controller |
| **EmbodiedSmith** | [EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation](https://arxiv.org/abs/2610.07969) | 2026 | arXiv | Designer | G | problem-spec | re-decide | manip/sim | – |
| **Agentic RSR** | [Agentic RSR: Real-to-Sim-to-Real through Scene Reconstruction and Execution-Grounded Robot Policies](https://arxiv.org/abs/2610.10479) | 2026 | arXiv | Developer | G | system-edit | re-decide | manip/sim+real | Designer |

## VLN and embodied navigation

Agents whose main task is navigation: vision-and-language navigation in continuous environments or on real robots, object-goal and instance navigation, long-range exploration. 2026 papers are evaluated in continuous simulation (e.g. Habitat VLN-CE) or on real robots; earlier agents on the discrete R2R graph appear only among the pioneers. Seats are kept, so the chapter mixes Controllers with a few Teachers and Designers.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **LM-Nav** | [LM-Nav: Robotic Navigation with Large Pre-Trained Models of Language, Vision, and Action](https://arxiv.org/abs/2207.04429) [[project]](https://sites.google.com/view/lmnav) | 2022 | CoRL | Controller | G | skill-call | none | nav/real | – |
| **NavGPT** | [NavGPT: Explicit Reasoning in Vision-and-Language Navigation with Large Language Models](https://arxiv.org/abs/2305.16986) | 2023 | AAAI | Controller | G | micro-action | re-decide | nav/sim | – |
| **SayNav** | [SayNav: Grounding Large Language Models for Dynamic Planning to Navigation in New Environments](https://arxiv.org/abs/2309.04077) | 2023 | International Conference on Automated Planning and Scheduling | Controller | G | skill-call | re-decide | nav/sim | – |
| **InstructNav** | [InstructNav: Zero-shot System for Generic Instruction Navigation in Unexplored Environment](https://arxiv.org/abs/2406.04882) | 2024 | CoRL | Controller | G | constraint | re-decide | nav/sim | – |
| **Open-Nav** | [Open-Nav: Exploring Zero-Shot Vision-and-Language Navigation in Continuous Environment with Open-Source LLMs](https://arxiv.org/abs/2409.18794) | 2024 | ICRA | Controller | G | skill-call | re-decide | nav/sim+real | – |
| **VLMnav** | [End-to-End Navigation with Vision Language Models: Transforming Spatial Reasoning into Question-Answering](https://arxiv.org/abs/2411.05755) | 2024 | arXiv | Controller | G | micro-action | re-decide | nav/sim | – |
| **CA-Nav** | [Constraint-Aware Zero-Shot Vision-Language Navigation in Continuous Environments](https://arxiv.org/abs/2412.10137) | 2024 | IEEE Transactions on Pattern Analysis and Machine Intelligence | Controller | G | constraint | authored | nav/sim+real | – |

**2026**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **One Agent to Guide Them All** | [One Agent to Guide Them All: Empowering MLLMs for Vision-and-Language Navigation via Explicit World Representation](https://arxiv.org/abs/2602.15400) | 2026 | arXiv | Controller | G | micro-action | re-decide | nav/sim+real | – |
| **OnFly** | [OnFly: Onboard Zero-Shot Aerial Vision-Language Navigation toward Safety and Efficiency](https://arxiv.org/abs/2603.10682) | 2026 | arXiv | Controller | G | micro-action | re-decide | aerial/sim+real | Supervisor |
| **HaltNav** | [HaltNav: Reactive Visual Halting over Lightweight Topological Priors for Robust Vision-Language Navigation](https://arxiv.org/abs/2603.12696) | 2026 | arXiv | Controller | C | skill-call | re-decide | nav/sim+real | Supervisor |
| **AgentVLN** | [AgentVLN: Towards Agentic Vision-and-Language Navigation](https://arxiv.org/abs/2603.17670) | 2026 | arXiv | Controller | C | skill-call | re-decide | nav/sim+real | – |
| **NORM-Nav** | [NORM-Nav: Zero-Shot Mobile Robot Navigation with Natural Language Behavioral Constraints](https://arxiv.org/abs/2605.16979) | 2026 | ICRA | Controller | G | constraint | authored | nav/sim+real | – |
| **AgenticNav** | [AgenticNav: Zero-Shot Vision-and-Language Navigation as a Tool-Calling Harness](https://arxiv.org/abs/2606.10577) | 2026 | arXiv | Controller | G | skill-call | re-decide | nav/sim | – |
| **LocalNav** | [LocalNav: Distilling Frontier VLMs and Embodied RL for On-Device Object Goal Navigation](https://arxiv.org/abs/2606.27871) | 2026 | arXiv | Teacher | G→C | skill-call | re-decide | nav/sim | Controller |
| **HAM-VLN** | [HAM-VLN: Harnessing Hierarchical Agentic Memory for Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2607.29600) | 2026 | arXiv | Controller | G | micro-action | re-decide | nav/sim | – |
| **Air-Ground VLN** | [Air-Ground Collaborative Vision-and-Language Navigation via Shared Bird's-Eye Maps](https://arxiv.org/abs/2609.03483) | 2026 | arXiv | Controller | G | skill-call | re-decide | multi-robot/sim | – |
| **HarnessVLN** | [HarnessVLN: Unifying Training-Free Embodied Navigation through an Agent Harness](https://arxiv.org/abs/2609.15195) | 2026 | arXiv | Controller | G | skill-call | re-decide | nav/sim | – |
| **ASENA** | [ASENA: Self-evolving Agents for Embodied Navigation](https://arxiv.org/abs/2609.39207) [[project]](https://asena-bot.github.io) | 2026 | arXiv | Controller | G | code | re-decide | nav/sim | Developer |

## Benchmarks and resources

| Name | Paper | Year | Venue | Evaluated seat | Body |
|---|---|---|---|---|---|
| **Embodied Agent Interface** | [Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making](https://arxiv.org/abs/2410.07166) | 2024 | NeurIPS | Controller | mobile-manip/sim |
| **PARTNR** | [PARTNR: A Benchmark for Planning and Reasoning in Embodied Multi-agent Tasks](https://arxiv.org/abs/2411.00081) | 2024 | arXiv | Controller | mobile-manip/sim |
| **SafeAgentBench** | [SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents](https://arxiv.org/abs/2412.13178) | 2024 | arXiv | Controller | mobile-manip/sim |
| **VLABench** | [VLABench: A Large-Scale Benchmark for Language-Conditioned Robotics Manipulation with Long-Horizon Reasoning Tasks](https://arxiv.org/abs/2412.18194) | 2024 | ICCV | Controller | manip/sim |
| **EmbodiedEval** | [EmbodiedEval: Evaluate Multimodal LLMs as Embodied Agents](https://arxiv.org/abs/2501.11858) | 2025 | arXiv | Controller | mobile-manip/sim |
| **EmbodiedBench** | [EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents](https://arxiv.org/abs/2502.09560) | 2025 | ICML | Controller | mobile-manip/sim |
| **ASIMOV** | [Generating Robot Constitutions & Benchmarks for Semantic Safety](https://arxiv.org/abs/2503.08663) | 2025 | arXiv | Supervisor | other/real |
| **RoboCerebra** | [RoboCerebra: A Large-scale Benchmark for Long-horizon Robotic Manipulation Evaluation](https://arxiv.org/abs/2506.06677) | 2025 | NeurIPS | Controller | manip/sim |
| **IS-Bench** | [IS-Bench: Evaluating Interactive Safety of VLM-Driven Embodied Agents in Daily Household Tasks](https://arxiv.org/abs/2506.16402) | 2025 | AAAI | Supervisor | mobile-manip/sim |
| **FAEA** | [Demonstration-Free Robotic Control via LLM Agents](https://arxiv.org/abs/2601.20334) | 2026 | arXiv | Controller | manip/sim |
| **EmboCoach-Bench** | [From Digital to Physical: Digital Agents as Autonomous Coaches for Physical Intelligence](https://arxiv.org/abs/2601.21570) | 2026 | arXiv | Developer | manip/sim |
| **Orchestration Study** | [What Matters in Orchestrating Robot Policies: A Systematic Study of Hierarchical VLA Agents](https://arxiv.org/abs/2606.10267) | 2026 | arXiv | Controller | manip/sim+real |
| **Embodied Agents Take Control** | [Embodied Agents Take Control: Minimal-Interface Zero-Shot Agents Rival Industrial-Scale Policies in Vision-and-Language Navigation](https://arxiv.org/abs/2607.26148) | 2026 | arXiv | Controller | nav/sim |
| **MLLM Drone Agents Eval** | [Evaluating Multimodal LLMs as Generalist Vision-Language-Action Agents for Drone Control: Commanding, Approaching, Tracking and Searching](https://arxiv.org/abs/2609.01404) | 2026 | arXiv | Controller | aerial/sim |
| **Astra on VLN-CE** | [How Far Can GPT-6-Astra Go? Evaluating Capabilities in Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2609.20116) | 2026 | arXiv | Controller | nav/sim |
| **WhenToAsk** | [When Should a Failing Robot Ask? Initiating Corrective Human-Robot Dialogue from Audited Sensor Evidence](https://arxiv.org/abs/2609.21942) | 2026 | arXiv | Supervisor | manip/sim+real |
| **Astra on RoboDojo** | [An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170) | 2026 | arXiv | Controller | manip/sim |
| **EmbodiedSWE** | [EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics](https://arxiv.org/abs/2609.27308) | 2026 | arXiv | Teacher | manip/sim+real |
| **CodeActionBench** | [CodeActionBench: Evaluating Agentic Code-as-Policy for Embodied Manipulation](https://arxiv.org/abs/2609.33807) [[project]](https://codeactionbench.org) | 2026 | arXiv | Controller | manip/sim |
| **RLE-Bench** | [RLE-Bench: A Qualifying Exam for Coding Agents as Robot Learning Engineers](https://arxiv.org/abs/2609.34210) [[project]](https://rle-bench.github.io/) | 2026 | arXiv | Developer | manip/sim |
| **LIBERO-Agent** | [LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507) | 2026 | arXiv | Controller | manip/sim |
| **Frontier VLM Agents Study** | [Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854) [[project]](https://embodied-agent-arena.github.io/embodied-agent-arena/) | 2026 | arXiv | Controller | mobile-manip/sim |
| **Video2World** | [Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos](https://arxiv.org/abs/2610.04432) [[project]](https://aetherlabsai.github.io/Video2World) | 2026 | arXiv | Designer | manip/sim |
| **RobotWorld** | [RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](https://arxiv.org/abs/2610.10409) | 2026 | arXiv | Controller | other/sim |

## More 2026 papers

830 further 2026 papers that meet the definition (judged by a verification pass; open-loop ones have *Loop* = none) but are not in the curated tables above. Tags come from the judging pass and are not hand-checked; generated by `scripts/build_extended.py`.

<details><summary><b>Controller · Orchestrators</b> (355)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Hybrid Framework for Robotic Manipulation: Integrating Reinforcement Learning and Large Language Models](https://arxiv.org/abs/2603.30022) | 2025-11 | G | none | manip/sim |
| [Multi-modal Interactive Control of Robotic Arm based on Offline Large Language Models*](https://arxiv.org/abs/2608.08183) | 2025-12 | G | none | manip/sim |
| [Leveraging Adaptive Group Negotiation for Heterogeneous Multi-Robot Collaboration with Large Language Models](https://arxiv.org/abs/2602.06967) | 2025-12 | G | re-decide | multi-robot/sim |
| A Hierarchical Framework of Central-Distributed LLM Negotiation and Specialized Model Orchestration for Multi-Robot Collaborative Assembly | 2026 | G | re-decide | multi-robot/sim |
| A Hierarchical LLM-Based Framework for Heterogeneous Multi-Robot Orchestration in High-Risk Energy Facility Maintenance | 2026 | G | none | multi-robot/sim |
| A Multi-Expert VLM Framework for Cognitive Robotic Manipulation in semi-structured Manufacturing | 2026 | G | none | manip/real |
| A Vision-Language Based Framework for Context-Aware Task Planning in Human-Robot Collaborative Assembly | 2026 | G | none | manip/real |
| AgenticDiffusion: Agentic Diffusion-based Path Planning for Vision-Based UAV Navigation | 2026 | G | re-decide | aerial/real |
| An MVUN-DP skill library-driven Embodied AI robotic assembly method with LLMs | 2026 | G | none | manip/real |
| CoIN: Interactive Navigation With Counterfactual Reasoning via Vision–Language Models | 2026 | C | re-decide | mobile-manip/sim+real |
| CogAssem: A VLM-Driven Architecture Bridging Cognition and Execution for Intelligent Robotic Assembly in Flexible Manufacturing | 2026 | G | none | manip/real |
| Cooperative Control Framework for Dual-Arm Robot Enhanced by Vision Language Model and Reinforcement Learning | 2026 | G | none | manip/sim+real |
| Embodied multi-agent system integrating VLA for AR-assisted HRC assembly task reasoning and autonomous execution | 2026 | G | none | manip/real |
| From Assistant to Agent: A State-Aware VLM Framework for Intelligent Human-Robot Collaboration System | 2026 | G | none | manip/real |
| GLaMP: A Grounded Language Model-Based Multiagent System for Long-Horizon Robotic Task Planning in Industrial Settings | 2026 | G | none | manip/sim |
| GNN-LLM hybrid cognitive architectures for generative task adaptation in multi-human multi-robot collaborative disassembly | 2026 | G | none | multi-robot/sim |
| Hallucination-Aware Hierarchical LLM for Autonomous UAV Mobility Control: A Safe Reinforcement Learning Approach | 2026 | G | none | aerial/sim |
| LMUCS: Lightweight LLM-driven UAV control system with multimodal perception for autonomous material search and localization | 2026 | G | none | aerial/real |
| Language-Driven Bimanual Cloth Manipulation With LLM Planning and Part-Aware Perception | 2026 | G | none | manip/real |
| PolyFold: A Generalizable Framework for Language-Conditioned Bimanual Cloth Folding | 2026 | G | none | manip/real |
| Probing a multi-agent and industrial language model framework of digital twin for human-robot collaborative assembly | 2026 | G | none | manip/sim |
| Synergizing Multimodal Large Language Models and GRPO-based Physics-Guided DRL for UAV Swarm Navigation in Dynamic Environments | 2026 | G | none | aerial/sim |
| Task Assignment Control of Autonomous Cooperative Mobile Robots via Large Language Models: A Proof-of-concept Study | 2026 | G | none | multi-robot/sim |
| The Perception, Decision-Making, and Execution of the Centipede-Like Rescue Robot | 2026 | G | none | other/real |
| VOICE CONTROL OF UNMANNED SYSTEMS USING A LARGE LANGUAGE MODEL | 2026 | G | none | multi-robot/sim |
| World Models as Constraints: Heterogeneous Rail Robot Coordination via CA-JEPA and LLM-Based Planning | 2026 | G | none | multi-robot/sim |
| A Hierarchical Vision-Language and Reinforcement Learning Framework for Robotic Task and Motion Planning in Collaborative Manipulation | 2026-01 | G | none | multi-robot/sim |
| [LLM-Based Agentic Exploration for Robot Navigation & Manipulation with Skill Orchestration](https://arxiv.org/abs/2601.00555) | 2026-01 | G | re-decide | mobile-manip/sim+real |
| [CoINS: Counterfactual Interactive Navigation via Skill-Aware VLM](https://arxiv.org/abs/2601.03956) | 2026-01 | C | re-decide | mobile-manip/sim+real |
| Intelligent Disassembly System for PCB Components Integrating Multimodal Large Language Model and Multi-Agent Framework | 2026-01 | G | none | manip/real |
| [Intent at a Glance: Gaze-Guided Robotic Manipulation via Foundation Models](https://arxiv.org/abs/2601.05336) | 2026-01 | G | none | manip/real |
| [A Framework for Low-Latency, LLM-Driven Multimodal Interaction on the Pepper Robot](https://arxiv.org/abs/2603.21013) | 2026-01 | G | re-decide | social/real |
| Distributed Brain-Cerebellum Architecture for Robotic Arm Control via Vision-Language Models and Generative Policies | 2026-01 | G | none | manip/real |
| [EmboTeam: Grounding LLM Reasoning into Reactive Behavior Trees via PDDL for Embodied Multi-Robot Collaboration](https://arxiv.org/abs/2601.11063) | 2026-01 | G | none | multi-robot/sim |
| [An Embodied Companion for Visual Storytelling](https://arxiv.org/abs/2603.05511) | 2026-01 | G | re-decide | manip/real |
| [UAVGENT: A Language-Guided Distributed Control Framework](https://arxiv.org/abs/2602.13212) | 2026-01 | G | re-decide | aerial/sim |
| [LLM-VLM Fusion Framework for Autonomous Maritime Port Inspection using a Heterogeneous UAV-USV System](https://arxiv.org/abs/2601.13096) | 2026-01 | G | none | multi-robot/sim |
| [DroneVLA: VLA-Based Aerial Manipulation](https://arxiv.org/abs/2601.13809) | 2026-01 | G | none | aerial/real |
| [Zero-shot adaptable task planning for autonomous construction robots: a comparative study of lightweight single and multi-AI agent systems](https://arxiv.org/abs/2601.14091) | 2026-01 | G | none | other/sim |
| [Real-Time Synchronized Interaction Framework for Emotion-Aware Humanoid Robots](https://arxiv.org/abs/2601.17287) | 2026-01 | G | none | social/real |
| Interactive Construction Robots for Timber Truss Assembly via Vision-Language Model and Mark-Based Visual Prompting | 2026-01 | G | none | manip/real |
| RAGLRO: Retrieval-Augmented Generation With Large Language Models for Robotic Operations | 2026-01 | G | none | manip/real |
| AR-assisted human-robot collaborative assembly system: Integrating visual language model and deep reinforcement learning for task planning and seamless interactive guidance | 2026-02 | G | none | manip/real |
| Enhancing stability and reliability in LLM-driven robotic manipulation through human skill demonstration and visual tracking | 2026-02 | G | none | manip/real |
| Robotic arm visual-servoing for AI-driven chess gameplay using LLM-based plannner | 2026-02 | G | none | manip/real |
| TRTP: a three-stage robust task planning framework for open worlds via visual-language models and digital twin simulation `real2sim2real` | 2026-02 | G | re-decide | manip/sim+real |
| [PLanAR: Planning-Language-Grounded Agentic Reasoning for Robot Manipulation](https://arxiv.org/abs/2602.01662) | 2026-02 | G | re-decide | manip/real |
| [Integrated Exploration and Sequential Manipulation on Scene Graph with LLM-based Situated Replanning](https://arxiv.org/abs/2602.04419) | 2026-02 | G | re-decide | mobile-manip/sim+real |
| [Affordance-Aware Interactive Decision-Making and Execution for Ambiguous Instructions](https://arxiv.org/abs/2602.05273) | 2026-02 | G | re-decide | mobile-manip/sim+real |
| Toward Embodied Intelligence: An Architecture for Natural Dialogue and Action Execution in Assistive Robots | 2026-02 | G | none | mobile-manip/real |
| [Bridging Speech, Emotion, and Motion: a VLM-based Multimodal Edge-deployable Framework for Humanoid Robots](https://arxiv.org/abs/2602.07434) | 2026-02 | G | none | humanoid/real |
| [Decentralized Intent-Based Multi-Robot Task Planner with LLM Oracles on Hyperledger Fabric](https://arxiv.org/abs/2602.08421) | 2026-02 | G | none | multi-robot/sim |
| [CAPER: Constrained and Procedural Reasoning for Robotic Scientific Experiments](https://arxiv.org/abs/2602.09367) | 2026-02 | G | none | manip/sim+real |
| Research on a Robotic Natural Language Intelligent Decision-Making Framework Based on Large Language Models, Thinking Chain Reasoning, and Multi-Agent Collaboration | 2026-02 | G | none | other/sim |
| [LocoVLM: Grounding Vision and Language for Adapting Versatile Legged Locomotion Policies](https://arxiv.org/abs/2602.10399) | 2026-02 | G | none | loco/real |
| [Agentic AI for Robot Control: Flexible but still Fragile](https://arxiv.org/abs/2602.13081) | 2026-02 | G | re-decide | mobile-manip/real |
| [UniManip: General-Purpose Zero-Shot Robotic Manipulation with Agentic Operational Graph](https://arxiv.org/abs/2602.13086) | 2026-02 | G | re-decide | manip/real |
| [AgentRob: From Virtual Forum Agents to Hijacked Physical Robots](https://arxiv.org/abs/2602.13591) | 2026-02 | G | re-decide | multi-robot/real |
| [Replanning Human-Robot Collaborative Tasks with Vision-Language Models via Semantic and Physical Dual-Correction](https://arxiv.org/abs/2602.14551) | 2026-02 | G | re-decide | humanoid/sim+real |
| [VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing](https://arxiv.org/abs/2602.15549) | 2026-02 | G | re-decide | manip/sim+real |
| [MALLVI: A Multi-Agent Framework for Integrated Generalized Robotics Manipulation](https://arxiv.org/abs/2602.16898) | 2026-02 | G | re-decide | manip/sim+real |
| From Language to Action: Small Language Model—Driven Humanoid Control with Visual Grounding Under the Model Context Protocol | 2026-02 | G | none | humanoid/real |
| [Zero-shot Interactive Perception](https://arxiv.org/abs/2602.18374) | 2026-02 | G | re-decide | manip/real |
| [Seeing Farther and Smarter: Value-Guided Multi-Path Reflection for VLM Policy Optimization](https://arxiv.org/abs/2602.19372) | 2026-02 | G | none | manip/sim |
| VLM-RLPGS: A Cognitive Framework Using Vision–Language Model and Reinforcement Learning for Push–Grasp Synergy | 2026-02 | G | none | manip/sim |
| [An Approach to Combining Video and Speech with Large Language Models in Human-Robot Interaction](https://arxiv.org/abs/2602.20219) | 2026-02 | G | none | manip/real |
| [CoReLIN: Constraint-based Reasoning for Zero-shot Lifelong Interactive Navigation](https://arxiv.org/abs/2602.20055) | 2026-02 | G | re-decide | mobile-manip/sim+real |
| STRAP-LLM: structured task allocation and planning for heterogeneous robots using large language models | 2026-02 | G | none | multi-robot/sim |
| Proposal for a real-world cooking robot based on the integration of LLM and visual information | 2026-02 | G | none | manip/real |
| ChainBot: An Agent System for Autonomous Robotic Object Manipulation by Dynamically Chaining Multiple Foundation Models | 2026-02 | G | re-decide | manip/real |
| A Multimodal Agentic AI Framework for Intuitive Human–Robot Collaboration | 2026-03 | G | none | mobile-manip/real |
| A Multimodal LLM-Driven Robotic Control System for Adaptive Industrial Manipulation: Integrating Vision-Language Models for Enhanced Manufacturing Flexibility | 2026-03 | G | none | manip/real |
| Active Obstacle Separation: Vision-Language Model (VLM) Driven Clearing Decisions for Robotic Harvesting | 2026-03 | G | none | manip/real |
| Enhanced reasoning and task planning for surgical autonomy using multi-modal large language models with gradual learning | 2026-03 | G | none | other/sim |
| Human-Robot Communication using Large Language Models for Automated Kitting | 2026-03 | G | none | manip/real |
| LLM-Based Natural Language Interface for Robotic Control in Mixed Reality | 2026-03 | G | none | manip/real |
| Large-Language-Model-Aided Assistive Robot for Single-Operator Bimanual Teleoperation: Introduction and Validation of a Flexible Assistance System | 2026-03 | G | none | manip/real |
| Onto-LLM-TAMP: Knowledge-oriented Task and Motion Planning using Large Language Models | 2026-03 | G | none | manip/sim |
| Streamlining Human–Robot Interaction: Integrating LLM-Based Planning into Modular Robotic Frameworks | 2026-03 | G | none | manip/real |
| [From Language to Action: Can LLM-Based Agents Be Used for Embodied Robot Cognition?](https://arxiv.org/abs/2603.03148) | 2026-03 | G | re-decide | mobile-manip/sim |
| [IROSA: Interactive Robot Skill Adaptation Using Natural Language](https://arxiv.org/abs/2603.03897) | 2026-03 | G | none | manip/real |
| [MistyPilot: An Agentic Fast-Slow Thinking LLM Framework for Misty Social Robots](https://arxiv.org/abs/2603.03640) | 2026-03 | G | none | social/real |
| [Critic in the Loop: A Tri-System VLA Framework for Robust Long-Horizon Manipulation](https://arxiv.org/abs/2603.05185) | 2026-03 | G | re-decide | manip/sim+real |
| A Large-Language-Model-Enabled Robotic System with Application to Power Cable Manipulation | 2026-03 | G | none | manip/real |
| [Multimodal Behavior Tree Generation: A Small Vision-Language Model for Robot Task Planning](https://arxiv.org/abs/2603.06084) | 2026-03 | C | none | mobile-manip/sim |
| Collaborative LLM-Based Agents for Autonomous Multi-UAV Mission Execution | 2026-03 | G | re-decide | multi-robot/sim+real |
| EXAONE-VLA: A Unified Vision–Language Framework for Mobile Manipulation via Semantic Topology and Hierarchical LLM Reasoning | 2026-03 | G | none | mobile-manip/real |
| [MoMaStage: Skill-State Graph Guided Planning and Closed-Loop Execution for Long-Horizon Indoor Mobile Manipulation](https://arxiv.org/abs/2603.08383) | 2026-03 | G | re-decide | mobile-manip/sim+real |
| [Scale-Plan: Scalable Language-Enabled Task Planning for Heterogeneous Multi-Robot Teams](https://arxiv.org/abs/2603.08814) | 2026-03 | G | none | multi-robot/sim |
| [SELF-VLA: A Skill Enhanced Agentic Vision-Language-Action Framework for Contact-Rich Disassembly](https://arxiv.org/abs/2603.11080) | 2026-03 | G | re-decide | manip/real |
| [TiPToP: A Modular Open-Vocabulary Robot Manipulation System That Plans](https://arxiv.org/abs/2603.09971) | 2026-03 | G | none | manip/sim+real |
| [AdaClearGrasp: Learning Adaptive Clearing for Zero-Shot Robust Dexterous Grasping in Densely Cluttered Environments](https://arxiv.org/abs/2603.10616) | 2026-03 | G | re-decide | manip/sim+real |
| [CoViLLM: An Adaptive Human-Robot Collaborative Assembly Framework Using Large Language Models](https://arxiv.org/abs/2603.11461) | 2026-03 | G | none | manip/real |
| [RoboStream: Weaving Spatio-Temporal Reasoning with Memory in Vision-Language Models for Robotics](https://arxiv.org/abs/2603.12939) | 2026-03 | G | re-decide | manip/sim+real |
| Multi-Modal Interactive Control of Robotic Arm Based on Offline Large Language Models (Student Abstract) | 2026-03 | G | none | manip/sim |
| [From Scanning Guidelines to Action: A Robotic Ultrasound Agent with LLM-Based Reasoning](https://arxiv.org/abs/2603.14393) | 2026-03 | G | re-decide | manip/real |
| [CORAL: COntextual Reasoning And Local Planning in A Hierarchical VLM Framework for Underwater Monitoring](https://arxiv.org/abs/2603.14786) | 2026-03 | G | re-decide | other/sim |
| Facilitating Co-regulation: An LLM-Powered Multimodal Social Robot for Parent-Child Dyads | 2026-03 | G | none | social/real |
| [DreamPlan: Efficient Reinforcement Fine-Tuning of Vision-Language Planners via Video World Models](https://arxiv.org/abs/2603.16860) | 2026-03 | C | re-decide | manip/real |
| AIR-Embodied: Active Interactive Reconstruction for 3D Gaussian Splatting with Embodied Multimodal Agents | 2026-03 | G | re-decide | manip/sim+real |
| [Robotic Agentic Platform for Intelligent Electric Vehicle Disassembly](https://arxiv.org/abs/2603.18520) | 2026-03 | G | none | manip/real |
| Event-Triggered Closed-Loop Semantic Control for Zero-Shot Multi-Step Robotic Manipulation | 2026-03 | G | re-decide | manip/real |
| LocationRAG: A Hierarchical Spatial Knowledge Graph Approach with LLM-Driven Multi-Agent Framework for Location-Constrained Multi-UAV Task Allocation | 2026-03 | G | none | multi-robot/sim |
| Service Embodied Intelligent Agent Framework for Multi-User Personalized Preferences | 2026-03 | G | none | mobile-manip/real |
| Development of a robotic arm grasping system using generative artificial intelligence | 2026-03 | C | none | manip/real |
| From Text to Movement: LLM-driven Swarm User Interfaces for Embodied and Interactive Storytelling | 2026-03 | G | none | multi-robot/real |
| [SafePilot: A Framework for Assuring LLM-enabled Cyber-Physical Systems](https://arxiv.org/abs/2603.21523) | 2026-03 | G | none | other/sim |
| [Task-Aware Positioning for Improvisational Tasks in Mobile Construction Robots via an AI Agent with Multi-LMM Modules](https://arxiv.org/abs/2603.22903) | 2026-03 | G | re-decide | loco/real |
| [Event-Driven Proactive Assistive Manipulation with Grounded Vision-Language Planning](https://arxiv.org/abs/2603.23950) | 2026-03 | G | none | manip/real |
| [SafeGuard ASF: SR Agentic Humanoid Robot System for Autonomous Industrial Safety](https://arxiv.org/abs/2603.25353) | 2026-03 | G | re-decide | humanoid/sim+real |
| Hierarchical Zero-Shot Robotic Manipulation Framework in Unstructured Environments Via Semantic-Geometric Alignment | 2026-03 | G | none | manip/real |
| Intent-driven LLM ensemble planning for flexible multi-robot manipulation | 2026-03 | G | none | multi-robot/sim |
| [ROSClaw: An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction](https://arxiv.org/abs/2603.26997) | 2026-03 | G | re-decide | loco/real |
| Improving Autonomy and Natural Interaction of Pepper Robot via Large Language Models | 2026-03 | G | none | social/real |
| [On-Demand Human Assistance for Task Continuation under Physical Action Failures in LLM-based Planning](https://arxiv.org/abs/2603.28156) | 2026-03 | G | re-decide | mobile-manip/real |
| CCM-FCC: LLM-powered cognition-centered AI agent framework for proactive human-robot collaboration | 2026-04 | G | none | manip/real |
| From insight to action: Embodied multi-agent system integrating vision language model for digital twin-assisted human-robot collaborative assembly | 2026-04 | G | none | manip/real |
| From insight to autonomous execution: VLM-enhanced embodied agents towards digital twin-assisted human-robot collaborative assembly | 2026-04 | G | none | manip/real |
| LLMQDelivery: An LLM-Guided Autonomous Quadcopter Delivery System for Minimizing Human Contact in Quarantine Zone Logistics | 2026-04 | G | none | aerial/sim |
| PLAN-MVP: Planning for Learning-Enabled Autonomous Navigation and Manipulation via Perception | 2026-04 | G | none | mobile-manip/sim |
| Robot Active Task Cognition: Situation-Aware Task Planning With Large Language Models | 2026-04 | G | none | manip/real |
| Scene graph-driven reasoning for action planning of humanoid robot | 2026-04 | G | none | humanoid/sim |
| [StretchBot: A Neuro-Symbolic Framework for Adaptive Guidance with Assistive Robots](https://arxiv.org/abs/2604.00628) | 2026-04 | G | none | social/real |
| [OpenGo: An OpenClaw-Based Robotic Dog with Real-Time Skill Switching](https://arxiv.org/abs/2604.01708) | 2026-04 | G | re-decide | loco/real |
| Autonomous Robot for General Urban Surveillance | 2026-04 | G | none | multi-robot/sim |
| [QuadAgent: A Responsive Agent System for Vision-Language Guided Quadrotor Agile Flight](https://arxiv.org/abs/2604.02786) | 2026-04 | G | re-decide | aerial/sim+real |
| [ROSClaw: A Hierarchical Semantic-Physical Framework for Heterogeneous Multi-Agent Collaboration](https://arxiv.org/abs/2604.04664) | 2026-04 | G | re-decide | multi-robot/sim+real |
| [ExpressMM: Expressive Mobile Manipulation Behaviors in Human-Robot Interactions](https://arxiv.org/abs/2604.05320) | 2026-04 | G | re-decide | mobile-manip/real |
| [AEROS: A Single-Agent Operating Architecture with Embodied Capability Modules](https://arxiv.org/abs/2604.07039) | 2026-04 | G | re-decide | manip/sim |
| Grounding Constraint-Specific Language Commands for Heterogeneous Multi-Robot Collaboration With Large Language Models | 2026-04 | G | none | multi-robot/sim |
| Reasoning Meets Adaptation: Bridging Global LLM Planning and Distributed UAV Control | 2026-04 | G | none | aerial/sim |
| Towards LLM-powered Assistive Drone for Blind and Low Vision Users | 2026-04 | G | none | aerial/real |
| [DeCoNav: Dialog enhanced Long-Horizon Collaborative Vision-Language Navigation](https://arxiv.org/abs/2604.12486) | 2026-04 | G | re-decide | multi-robot/sim |
| [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](https://arxiv.org/abs/2604.13942) | 2026-04 | G | re-decide | manip/sim+real |
| Graph-Based Task Allocation for Multi-Agent Fleet Management: A Genetic Algorithm Approach with LLM Integration | 2026-04 | G | re-decide | multi-robot/sim |
| A Reasoning-Based Robotic Bolt Fastening System with a Dexterous Hand | 2026-04 | G | none | manip/real |
| An Intent-Driven Task Graph Framework for Safe Long-Horizon Execution in Embodied Agents | 2026-04 | G | none | humanoid/sim+real |
| [Logic-Based Verification of Task Allocation for LLM-Enabled Multi-Agent Manufacturing Systems](https://arxiv.org/abs/2604.17142) | 2026-04 | G | none | multi-robot/sim |
| SafeTune: An LLM-Driven Parameter Self-tuner for UAV Inspections in Power Grid Scenarios | 2026-04 | G | none | aerial/sim |
| [Intent-aligned Autonomous Spacecraft Guidance via Reasoning Models](https://arxiv.org/abs/2604.17176) | 2026-04 | C | none | other/sim |
| [A Framework for Seamless Physical, Verbal, and Graphical Robot Skill Learning and Adaptation](https://arxiv.org/abs/2604.20468) | 2026-04 | G | none | manip/real |
| [Navigating the Clutter: Waypoint-Based Bi-Level Planning for Multi-Robot Systems](https://arxiv.org/abs/2604.21138) | 2026-04 | C | none | multi-robot/sim |
| BT-Planner: A Hierarchical Task Planning Framework for Robot using Large Language Models and Behavior Trees | 2026-04 | G | none | manip/sim+real |
| [CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models](https://arxiv.org/abs/2604.22238) | 2026-04 | G | authored | manip/real |
| Visual Task Modeling and Automated Planning for Humanoid Robots in Education of Individuals with Autism Spectrum Disorder | 2026-04 | G | none | social/real |
| An Agentic Framework for Aerial Swarms: Integrating LLMs with the Crazyswarm2 | 2026-04 | G | re-decide | multi-robot/sim |
| [ANCHOR: A Physically Grounded Closed-Loop Framework for Robust Home-Service Mobile Manipulation](https://arxiv.org/abs/2604.25323) | 2026-04 | G | re-decide | mobile-manip/real |
| A Lightweight Modular Vision-Language-Action Framework for Real-Time Closed-Loop Robotic Manipulation | 2026-05 | G | none | manip/real |
| A cloud-edge collaborative framework with confidence-aware perception and cognitive dual-stream memory for proactive service robot decision-making | 2026-05 | G | none | mobile-manip/real |
| Act or ask: Interactive construction robots via vision-language models with confidence-guided decision deferral | 2026-05 | G | none | manip/real |
| CDP: Composable Diffusion Policy for Manipulation | 2026-05 | G | none | manip/sim |
| Integrating Advantage Actor-Critic in Multi-Robot Collaboration | 2026-05 | G | re-decide | multi-robot/sim |
| LLM-BT-Grasp: Large Language Model to Behavior Tree for Grasping | 2026-05 | G | none | manip/real |
| LLM-Guided Bi-Objective Planning for Energy-Constrained AUV Fleets | 2026-05 | G | none | multi-robot/sim |
| Language-Driven Multi-Task Manipulation With Action-Mask-Enhanced Multimodal Learning | 2026-05 | G | none | manip/real |
| VLM-Driven Task Planning for Industrial Robot Workcells with Multiple Identical Targets | 2026-05 | G | none | manip/real |
| Vision-language guided planning and control for humanoid whole-body manipulation | 2026-05 | G | none | humanoid/sim+real |
| [Action Agent: Agentic Video Generation Meets Flow-Constrained Diffusion](https://arxiv.org/abs/2605.01477) | 2026-05 | G | none | humanoid/sim |
| [LLM-Foraging: Large Language Models for Decentralized Swarm Robot Foraging](https://arxiv.org/abs/2605.01461) | 2026-05 | G | re-decide | multi-robot/sim |
| Towards Object-Level Multimodal Task Planning for Long-Term Robotic Manipulation with Vision Language Model and Behavior Tree | 2026-05 | G | authored | manip/real |
| [Say the Mission, Execute the Swarm: Agent-Enhanced LLM Reasoning in the Web-of-Drones](https://arxiv.org/abs/2605.03788) | 2026-05 | G | re-decide | aerial/sim |
| [IntenBot: Flexible and Imprecise Multimodal Input for LLMs to Understand User Intentions for Casual and Human-Like HRI](https://arxiv.org/abs/2605.04585) | 2026-05 | G | none | other/sim |
| [BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation](https://arxiv.org/abs/2605.07306) | 2026-05 | G | re-decide | manip/real |
| Enhancing End-user Engagement in Human–Robot Interaction by Performing LLM-driven Expressive Behaviors | 2026-05 | G | none | humanoid/real |
| [Melding LLM and temporal logic for reliable human-swarm collaboration in complex scenarios](https://arxiv.org/abs/2605.07877) | 2026-05 | G | re-decide | multi-robot/sim+real |
| Proactive collaboration via autonomous interaction | 2026-05 | G | re-decide | multi-robot/sim+real |
| Large Language Model and Knowledge Graph-Based Intelligent Control Framework for Smart Manufacturing | 2026-05 | G | none | mobile-manip/real |
| [Qumus: Realization of An Embodied AI Quantum Material Experimentalist](https://arxiv.org/abs/2605.18407) | 2026-05 | G | re-decide | other/real |
| Repair2Skill: A Vision-Language-Action Framework for Robotic Furniture Repair | 2026-05 | G | none | manip/sim |
| A cognitive synergetic hierarchical framework for UAV swarm combat via speculative inference and role-decoupled reinforcement learning | 2026-05 | G | re-decide | multi-robot/sim |
| [Humanoid Whole-Body Manipulation via Active Spatial Brain and Generalizable Action Cerebellum](https://arxiv.org/abs/2605.21133) | 2026-05 | G | none | humanoid/real |
| Task2Mission: language-driven task-to-mission mapping for adaptive water quality monitoring | 2026-05 | G | none | other/sim |
| A2C-LLM: An Actor-Critic-Enhanced Large Language Model for UAV Swarm Multi-Target Task Allocation | 2026-05 | C | none | multi-robot/sim |
| Adaptive Multi-Plan Semantic Graph Task Planning for Embodied Robots | 2026-05 | G | none | mobile-manip/sim |
| Demand-Driven Robotic Grasping With Large Language Models and Open-Vocabulary Detection | 2026-05 | G | none | manip/real |
| Design and Research of an Intelligent Package Station Entry Robot System Based on Jetson Orin Nano | 2026-05 | G | none | mobile-manip/real |
| Man-Machine Collaborative Task Planning Based on Visual Language Models | 2026-05 | C | re-decide | manip/sim+real |
| Robotic assembly via self-prompt Segment Anything Model and discrete prompt optimization | 2026-05 | G | none | manip/real |
| HAMMR: A Human-Aligned Multi-Agent Framework for Language-Guided Robotic Manipulation | 2026-05 | G | none | manip/sim |
| [Sentinel: Embodied Cooperative Spatial Reasoning and Planning](https://arxiv.org/abs/2605.26239) | 2026-05 | G | re-decide | multi-robot/sim |
| LLM-Orchestrated Framework for Multifunctional Robotic Health Attendant (RHA) in Healthcare Environments | 2026-05 | G | none | mobile-manip/real |
| [PEACE: A Planner-Executor Agent with Constraint Enforcement for UAVs](https://arxiv.org/abs/2606.00104) | 2026-05 | G | re-decide | aerial/sim |
| [Decentralized LLM-Driven Coordination of Acoustic Robots for Contactless Object Manipulation](https://arxiv.org/abs/2605.29378) | 2026-05 | G | none | multi-robot/real |
| Elderly and disabled care robot system based on VLA large model | 2026-05 | G | none | mobile-manip/real |
| [On-Device Robotic Planning: Eliminating Inference Redundancy for Efficient Decision-Making](https://arxiv.org/abs/2605.31460) | 2026-05 | G | re-decide | mobile-manip/sim+real |
| A Hybrid Computing Framework For LLM-based Human-robot Interaction: Generating Action Plans for Robotic Arms | 2026-05 | G | none | manip/real |
| A Hierarchical DRL-Based Planning and Navigation Framework for Complex Multi-Robot Missions Leveraging LLMs | 2026-06 | G | none | multi-robot/sim |
| A Multi-Agent Framework for Task Planning and Execution in Robotic Perception and Manipulation | 2026-06 | G | none | manip/real |
| A Vision-Guided Autonomous Robotic Arm for Intelligent Object Sorting | 2026-06 | G | none | manip/sim+real |
| Can Robots Understand Indirect Speech Acts in Task Planning? | 2026-06 | C | none | manip/sim |
| EduBot-LLM: An LLM-Driven Educational Robot Agent with Unified Dialogue and Action Planning | 2026-06 | G | none | social/real |
| HiveNav: Hierarchical Semantic Planning for UAV Swarm Exploration | 2026-06 | G | re-decide | multi-robot/sim |
| Integrating Vision-Language Planning and Closed-Loop Control for Robust Bimanual Robotic Manipulation | 2026-06 | G | none | manip/real |
| Introducing JARVIS: An LLM based Autonomous Robotic Agent for Near Real-Time Planning and Execution of Novel ADL Tasks | 2026-06 | G | none | mobile-manip/real |
| Modeling Self-Awareness in Embodied Task Planning with LLM-Driven Heuristics | 2026-06 | G | none | mobile-manip/sim |
| Modular Framework for Responsive and Explainable Robotic Assistance with Intention Prediction Using Human-Centric Digital Twins | 2026-06 | G | none | manip/real |
| Multi-Agent LLM Reasoning for Robotic Block Placement | 2026-06 | G | re-decide | manip/real |
| [PerceptTwin: Semantic Scene Reconstruction for Iterative LLM Planning and Verification](https://arxiv.org/abs/2606.04226) `real2sim2real` | 2026-06 | G | re-decide | mobile-manip/sim |
| Privacy-aware LLM-assisted Task Planning for Home Robots | 2026-06 | G | none | mobile-manip/sim |
| SafeNet: A Neural-Symbolic Network for Safe Planning in Robotic Systems using Formal Method-Guided LLM Fine-Tuning | 2026-06 | C | none | manip/sim |
| Tool-augmented LLM planning and decoupled scheduling for heterogeneous multi-agent lunar missions: A three-layer architecture | 2026-06 | G | none | multi-robot/sim |
| VLION: Vision-Language Guided Interactive Object Navigation with Mobile Manipulation | 2026-06 | G | none | mobile-manip/sim+real |
| VLM Controlled Teleoperation of Heterogeneous Agents | 2026-06 | G | none | multi-robot/real |
| [AgenticDiffusion: Multi-View Reasoning with View-Conditioned Diffusion Planning for Vision-Based UAV Navigation](https://arxiv.org/abs/2606.04111) | 2026-06 | G | re-decide | aerial/real |
| Natural language control of UAVs using large language models with robust semantic interpretation and logic-guided task planning | 2026-06 | G | none | aerial/sim |
| Reinforcement-Enhanced LLM-based Intelligent Robotics Programming for Autonomous Industrial Automation Systems | 2026-06 | G | none | manip/sim |
| [A Conversational Framework for Human-Robot Collaborative Manipulation with Distributed Generative AI models](https://arxiv.org/abs/2606.06061) | 2026-06 | G | re-decide | manip/real |
| [A Systems Engineering Framework for Vision-Language-Enabled UAV Triage and Disaster Response](https://arxiv.org/abs/2607.27597) | 2026-06 | G | re-decide | aerial/sim |
| LLM-driven semantic planning and embodied control for an integrated mobile dual-arm robot | 2026-06 | G | none | mobile-manip/real |
| [VoLo: A Physical Orchestrator for Open-Vocabulary Long-Horizon Manipulation](https://arxiv.org/abs/2606.07723) | 2026-06 | G | re-decide | manip/sim |
| [Agentic Neuro-Symbolic Planning and Commissioning for Human-in-the-Loop Industrial Robotics with Digital Twins](https://arxiv.org/abs/2606.08214) | 2026-06 | G | re-decide | manip/sim+real |
| [CLASP: Language-Driven Robot Skill Selection and Composition using Task-Parameterized Learning](https://arxiv.org/abs/2606.08169) | 2026-06 | G | none | manip/real |
| [Bridging Semantics and Physical Execution: A Neuro-Symbolic Framework for Multi-Pair Robotic Assembly](https://arxiv.org/abs/2606.10808) | 2026-06 | G | none | manip/real |
| [JOIN: Anchor-Grasp-Conditioned Joining via Opposition, Inference, and Navigation for Bimanual Assistive Manipulation](https://arxiv.org/abs/2606.11151) | 2026-06 | G | none | multi-robot/real |
| [Learning What to Say to Your VLA: Mostly Harmless Vision Language Action Model Steering](https://arxiv.org/abs/2606.12299) | 2026-06 | C | re-decide | manip/sim |
| [Y-BotFrame: An Extensible Embodied Agent Framework for Quadruped Robot Assistants](https://arxiv.org/abs/2606.13049) | 2026-06 | G | none | loco/real |
| [DynaHMRC: Decentralized Heterogeneous Multi-Robot Collaboration for Dynamic Tasks with Large Language Models](https://arxiv.org/abs/2606.14882) | 2026-06 | C | re-decide | multi-robot/sim |
| MAVE: An Augmented Multi-agent LLM System for Interactive Design and Robotic Fabrication | 2026-06 | G | re-decide | manip/real |
| [OSDAG: Online Scheduling for Efficient Multi-Robot Collaboration](https://arxiv.org/abs/2606.15255) | 2026-06 | G | none | multi-robot/sim |
| LLM-Enabled Human-in-the-Loop Control of Multi-UAV Teams under Communication Constraints | 2026-06 | G | none | multi-robot/sim |
| Swarm-Steward: Scalable and Reliable Natural-Language Coordination of Autonomous Aerial and Ground Robots | 2026-06 | G | none | multi-robot/sim |
| [OmniDroneX: An LLM-Assisted Holistic Drone-as-a-Service Ecosystem](https://arxiv.org/abs/2606.17510) | 2026-06 | G | none | aerial/real |
| A Prompt-Driven Vision-Language Framework for Deictic Interpretation in Human-Robot Handover | 2026-06 | G | none | manip/real |
| [One-to-Two Acting: A Novel Framework for Single-arm Agent Action Expansion to Dual Arms](https://arxiv.org/abs/2606.19897) | 2026-06 | G | none | manip/sim+real |
| [EmbodiedUS-FS: Fast Slow Intelligence for Ultrasound Robotics](https://arxiv.org/abs/2606.22319) | 2026-06 | G | re-decide | manip/real |
| [Bridging Semantics and Kinematics: A Modular Framework for Zero-Shot Robotic Manipulation](https://arxiv.org/abs/2606.23157) | 2026-06 | G | none | manip/real |
| [HoloAgent-0: A Unified Embodied Agent Framework with 3D Spatial Memory](https://arxiv.org/abs/2606.23565) | 2026-06 | G | re-decide | mobile-manip/real |
| Phase-Adaptive Large Language Models for Multi-Robot Task Allocation in Dynamic Construction Environments | 2026-06 | G | none | multi-robot/sim |
| RoDA: A Role-Playing Dual-Agent Framework to Drive Nursing Robots in Bimanual Coordination Tasks | 2026-06 | G | re-decide | manip/sim |
| [Advancing Omnimodal Embodied Agents from Isolated Skills to Everyday Physical Autonomy](https://arxiv.org/abs/2606.27251) | 2026-06 | G | re-decide | mobile-manip/real |
| [RoboNav-Arm: Agentic AI-Driven Navigation and Obstacle Avoidance for Robotic Manipulator in Cluttered Environments](https://arxiv.org/abs/2607.09716) | 2026-06 | G | re-decide | manip/real |
| [AERIS: Aerial-Edge Role-Driven Intelligence at Runtime via Orchestrated Language-Model Swarm](https://arxiv.org/abs/2606.30151) | 2026-06 | G | re-decide | aerial/sim |
| [Sequential Planning via Anchored Robotic Keypoints](https://arxiv.org/abs/2606.30613) | 2026-06 | G | none | manip/sim |
| [Agentic RAG-VLM: Affordance-Aware Retrieval-Augmented Generation with Self-Reflective Planning for Robotic Grasping](https://arxiv.org/abs/2606.31200) | 2026-06 | G | re-decide | manip/real |
| [LLM-Powered Interactive Robotic Action Synthesis from Multimodal Speech, Gestures, and Music](https://arxiv.org/abs/2606.31158) | 2026-06 | G | none | loco/real |
| A Multimodal Emotional Interaction Framework Driven by Large Language Models | 2026-07 | G | none | social/real |
| [Adaptive Companionship for Group-Following Robots: Handling Dynamically Changing Group Formations](https://arxiv.org/abs/2607.01287) | 2026-07 | G | none | social/real |
| Generation of Object Alignment Behavior Based on VLM Proposal and Verification Considering a Human-Robot Collaboration Interface | 2026-07 | G | re-decide | manip/real |
| LLM-Guided Adaptive Gait Control for Humanoid Robots via Multi-Modal State Reasoning | 2026-07 | C | none | humanoid/sim |
| LLM-Guided Distributed Model Predictive Control for Decentralized UAV Formations | 2026-07 | C | none | multi-robot/sim |
| Perception-decision-execution coordination mechanism driven dynamic autonomous collaboration method for human-like collaborative robot based on multimodal large language model | 2026-07 | G | none | manip/real |
| RoboCleaner: Robotic Tabletop Cleaning via VLM-Powered Multi-Agent Collaboration | 2026-07 | G | re-decide | manip/real |
| Robust Assistive Mobile Manipulation via Structured LLM Programs, Confirmation Loops, and Hierarchical Skill Recovery * | 2026-07 | G | re-decide | mobile-manip/real |
| SafeTap: Trustworthy Neurosymbolic Language to Quadrupedal Locomotion via Shield Synthesis Modulo Bitvectors | 2026-07 | G | none | loco/sim |
| Structured and Unstructured Speech2Action Frameworks for Human–Robot Collaboration: A User Study | 2026-07 | G | none | mobile-manip/real |
| Twin-BT: An LLM-Based Behavior Tree Framework Integrating Digital Twin and Deterministic Semantic Verification for Robotics `real2sim2real` | 2026-07 | G | re-decide | manip/sim+real |
| VLA-Touch: Enhancing Vision-Language-Action Model With Dual-Level Tactile Feedback | 2026-07 | G | re-decide | manip/real |
| Voice-Controlled Robotic Arm System for Tabletop Manipulation via Large Language Model and 3D Vision | 2026-07 | G | none | manip/real |
| World-Model-Enhanced UAV Intelligent Inspection Method for Converter Station Valve Halls | 2026-07 | G | re-decide | aerial/real |
| [HiMe: Hierarchical Embodied Memory for Long-Horizon Vision-Language-Action Control](https://arxiv.org/abs/2607.03449) | 2026-07 | G | re-decide | manip/sim+real |
| [ACE: Agentic Control for Embodied Manipulation via Zero-shot Workflow Reasoning](https://arxiv.org/abs/2607.04162) | 2026-07 | G | re-decide | manip/real |
| Human–robot collaboration in building disassembly: a multi-agent LLM architecture | 2026-07 | G | re-decide | manip/sim |
| [TypeGo: An OS Runtime for Embodied Agents](https://arxiv.org/abs/2607.05482) | 2026-07 | G | re-decide | loco/real |
| [A Closed-Loop Multi-Agent Framework for Robust Multi-Robot Manipulation](https://arxiv.org/abs/2607.06990) | 2026-07 | G | re-decide | multi-robot/sim+real |
| [Multi-Agent Robotic Control with Onboard Vision-Language Models](https://arxiv.org/abs/2607.07403) | 2026-07 | G | re-decide | mobile-manip/sim |
| [APIVOT: Adaptive Planning with Interleaved Vision-Language Thoughts](https://arxiv.org/abs/2607.08024) | 2026-07 | C | none | manip/sim |
| [Task Planning for Mobile Manipulation in Retail Stores using Foundation Models with Iterative Re-planning](https://arxiv.org/abs/2607.09962) | 2026-07 | G | re-decide | mobile-manip/sim |
| [A Glimpse into Long-term Physical Coexistence with Intelligent Robots](https://arxiv.org/abs/2607.11377) | 2026-07 | G | re-decide | multi-robot/real |
| [EFLUX: Elastic Multi-Robot Formation Navigation and Adaptation with Agentic LLMs](https://arxiv.org/abs/2607.12050) | 2026-07 | G | none | multi-robot/sim |
| [Engagement-Aware Agentic Pursuit-Evasion](https://arxiv.org/abs/2607.10986) | 2026-07 | G | re-decide | multi-robot/sim |
| Practical Human–Robot Interaction (HRI) through Large Language Model (LLM)-based Voice-to-Action Systems | 2026-07 | G | re-decide | mobile-manip/real |
| [Think When It Matters: Conditional VLM Reasoning for Social Navigation with RL Policies](https://arxiv.org/abs/2607.10991) | 2026-07 | C | none | social/sim |
| [Exploratory, Communicative, and Deployable: Vision-Driven Embodied Agents for Open-World Mobile Manipulation](https://arxiv.org/abs/2607.13653) | 2026-07 | C | re-decide | mobile-manip/sim+real |
| Knowledge-augmented embodied exploration for robotic grasping in constrained environments | 2026-07 | G | none | manip/sim+real |
| [RT-SHCUA: Real-Time Self-Hosted Computer-Use Agent for UAV Control](https://arxiv.org/abs/2607.17951) | 2026-07 | G | none | aerial/sim |
| [LENS: LLM-guided Environment Simplification for Planning and Control in Clutter](https://arxiv.org/abs/2607.19633) | 2026-07 | G | re-decide | manip/sim+real |
| ReflectVLM+: Enhancing VLM-based Robotic Planning via Quantitative Stagnation Detection and Trajectory Refinement | 2026-07 | C | re-decide | manip/sim |
| [RoboBRIDGE: A Modular Framework for Bridging Policies to Robust Real-World Robotic Agents](https://arxiv.org/abs/2607.27881) | 2026-07 | G | re-decide | manip/sim+real |
| [D-VLC: Decentralized Vision-Language Collaboration for Heterogeneous Embodied Multi-Robot Systems in Unknown Environments](https://arxiv.org/abs/2607.29009) | 2026-07 | G | re-decide | multi-robot/sim |
| Cost-Aware LLM-Based Task and Motion Planning with Learned Feasibility Checks | 2026-08 | G | none | manip/sim |
| Dynamic Closed-Loop Grasping Via an Enhanced Thinkgrasp Framework | 2026-08 | G | re-decide | manip/sim |
| Dynamic Object Tracking and Recovery for Language-Conditioned Mobile Manipulation | 2026-08 | G | none | mobile-manip/real |
| Embodied Intelligence Robots: Flexible Task Planning Framework and Multimodal Fusion Perception | 2026-08 | G | re-decide | manip/real |
| Energy-Aware Task Planning for Industrial Robots via Large Language Models | 2026-08 | G | none | manip/real |
| LLM-Based Hierarchical Control Architecture for Robotic Operation | 2026-08 | G | re-decide | manip/sim+real |
| [ORCESTRA: VLM-driven Visual Robot programming in Mixed Reality](https://arxiv.org/abs/2608.00775) | 2026-08 | G | none | manip/sim |
| [ETA: A New Agentic Paradigm for Embodied Tasks](https://arxiv.org/abs/2608.03924) | 2026-08 | G | re-decide | manip/sim+real |
| PFEA: a VLM-based high-level natural language planning and feedback embodied agent for human-centered AI | 2026-08 | G | re-decide | manip/real |
| [Representation Handoffs for OpenArm-Based Laboratory Mobile Manipulation](https://arxiv.org/abs/2608.07154) | 2026-08 | G | none | mobile-manip/real |
| A multimodal foundation model-enabled agent for human–robot collaboration in construction | 2026-08 | G | none | other/sim |
| [HarnessWAM: Bridging Prediction and Deliberation in World Action Models](https://arxiv.org/abs/2608.09516) | 2026-08 | G | re-decide | manip/sim |
| ActivAsk: Free-Energy-Guided Clarification for Robotic Grasping Under Ambiguous Instructions | 2026-08 | G | none | manip/real |
| [Active Perception for Embodied Disambiguation](https://arxiv.org/abs/2608.13605) | 2026-08 | G | re-decide | mobile-manip/real |
| Large Language Model-Driven Symbolic Planning for Long-Horizon Robotic Manipulation Tasks | 2026-08 | G | none | manip/real |
| [MistyPilot: Enabling Social-Robot Control through Multi-Agent LLM Skill Orchestration](https://arxiv.org/abs/2608.15549) | 2026-08 | G | authored | social/real |
| Autonomous post-typhoon structural inspection and damage assessment: an agentic AI and aerial robotics-enabled model | 2026-08 | G | none | aerial/sim |
| [GuideFetch: A Task Coordination Framework for Concurrent Navigation and Object Retrieval in Assistive Robot Dogs](https://arxiv.org/abs/2608.18292) | 2026-08 | G | none | multi-robot/sim |
| [HODAgent: Towards On-Demand, Responsive Humanoids for Physical World Human Interaction](https://arxiv.org/abs/2608.17584) | 2026-08 | G | re-decide | humanoid/sim+real |
| [Safe Multi-Robot Coordination via VLM–LLM Reasoning and Reachability Analysis](https://arxiv.org/abs/2609.27816) | 2026-08 | G | none | multi-robot/real |
| MulPlanLM: multimodal robotic task planning with vision-language models and physical feedback | 2026-08 | C | re-decide | manip/sim+real |
| Priority-Driven Hierarchical Multi-Agent Systems with Fine-Tuned LLMs | 2026-08 | C | none | social/real |
| [Evidence-Gated Task and Motion Planning with Vision-Language Models](https://arxiv.org/abs/2608.20084) | 2026-08 | G | re-decide | manip/sim |
| [World-Model-Grounded LLM Planning for AUV and ASV Navigation Near Offshore Wind Farms](https://arxiv.org/abs/2608.19661) | 2026-08 | G | none | other/sim |
| A human-verifiable execution-time DAG refinement framework for LLM-driven multi-robot construction task planning | 2026-08 | G | re-decide | multi-robot/sim |
| SkyAgent: A lightweight LLM-driven reinforcement learning framework for adaptive cooperative path planning of two UAVs | 2026-08 | G | none | multi-robot/sim |
| LLM‐Based Multimodal Robotic Endoscope Control Framework for Enhancing Human–Robot Interaction in Minimally Invasive Surgery | 2026-08 | G | none | other/real |
| [Meta-Ctrl: Guaranteed Plan Generation by Decoupling Syntactic and Semantic Constraints](https://arxiv.org/abs/2608.22149) | 2026-08 | G | none | manip/sim+real |
| [Physical Agentic AI: An Architecture for Orchestrating a Robot Crew with LLMs](https://arxiv.org/abs/2608.22657) | 2026-08 | G | none | multi-robot/sim |
| [TONAV: Task-Oriented Navigation and Action-Velocity Chunk Learning for Articulated Object Quadrupedal Mobile Manipulation](https://arxiv.org/abs/2608.22296) | 2026-08 | G | none | mobile-manip/real |
| [$R^3$: Training Robots to Reason in Natural Language via Reinforcement Learning](https://arxiv.org/abs/2608.26053) | 2026-08 | C | re-decide | manip/sim |
| Embodied AI in the operating room: a voice-interactive robotic scrub nurse for surgical instrument handoffs | 2026-08 | G | none | manip/real |
| [STEP: State-Aware Task Estimation and Planning with Multi-Modal LLMs for Human-Robot Collaboration](https://arxiv.org/abs/2608.27225) | 2026-08 | G | none | manip/real |
| [MaCoPlanner: LLM-Assisted Manual-Compiled Task Planning with Proactive Safety Verification for Robotic Industrial Panel Operation](https://arxiv.org/abs/2608.28300) | 2026-08 | G | none | manip/sim |
| [PanelShield: Verifiable Closed-Loop Safe Planning for Robotic Industrial Panel Operation](https://arxiv.org/abs/2608.28305) | 2026-08 | G | re-decide | manip/sim+real |
| [Plan Along the Way: Event-Triggered Foundation-Model Planning for TAMP Execution in Partially Observable Manipulation](https://arxiv.org/abs/2608.28075) | 2026-08 | G | re-decide | manip/sim |
| [Bridging Semantics and Physics with Constrained LLMs for Safe and Trustworthy Robotic Manipulation](https://arxiv.org/abs/2608.29379) | 2026-08 | G | none | manip/real |
| [EMERGE-Policy: A Robot Mind Emerges Beyond a Single Policy](https://arxiv.org/abs/2608.29896) | 2026-08 | G | re-decide | manip/sim+real |
| Adaptive Task Planning for Long-Horizon Robotic Manipulation Based on Video Priors and Dynamic Scene Graphs | 2026-09 | G | re-decide | manip/sim |
| Control semántico de un robot rehabilitador mediante modelos de lenguaje | 2026-09 | G | none | other/sim+real |
| [EmbodiedSkills: A Unified Framework for Orchestrating, Training, and Deploying VLA Agents](https://arxiv.org/abs/2609.01281) | 2026-09 | C | re-decide | manip/sim+real |
| LG-HSS: Language-Guided Hybrid Skill Scheduling for embodied manipulation | 2026-09 | G | none | manip/sim |
| Reinforcement Learning-Based Routing Framework Guided by Vision-Language Model. | 2026-09 | G | none | manip/real |
| Visual Storytelling: An Embodied Companion [Arts and Robotics] | 2026-09 | G | re-decide | manip/real |
| [HINT: Human-Intent Inception for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2609.02653) | 2026-09 | G | re-decide | manip/sim+real |
| [A computable representation of the physical laboratory enables verifiable workflows](https://arxiv.org/abs/2609.03621) | 2026-09 | G | none | other/real |
| [A Brain-inspired Hierarchical Framework for Zero-Shot Robot Task Reasoning and Execution](https://arxiv.org/abs/2609.05985) | 2026-09 | G | re-decide | manip/real |
| [2AM: Grounding Agent-Side Memory as Guidance for Steerable Action Models in Long-Horizon Manipulation](https://arxiv.org/abs/2609.11308) | 2026-09 | G | re-decide | manip/sim |
| [Harness Robotic OS: A Unified Embodied-Agent Runtime for Closed-Loop Quadruped Inspection](https://arxiv.org/abs/2609.11225) | 2026-09 | G | re-decide | loco/real |
| A reasoning-LLM-based high-level planning framework for robotic shelf-stocking and disposal tasks | 2026-09 | G | none | mobile-manip/real |
| [AeroWeaver: An Embodied-Agent Harness for Weaving Aerial Skills into Distributed, Adaptive Swarm Execution](https://arxiv.org/abs/2609.18520) | 2026-09 | G | re-decide | multi-robot/sim |
| [From Rollout to Reset: A Graph-Based Harness for Autonomous Long-Horizon Manipulation Evaluation](https://arxiv.org/abs/2609.19413) | 2026-09 | G | re-decide | manip/real |
| [KINO: A Keyframe Interface for VLM Planning and Whole-Body Control in Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.18869) | 2026-09 | G | re-decide | humanoid/sim+real |
| [MaskHarness-WAM: Instance-Grounded Harnessing for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2609.19974) | 2026-09 | G | re-decide | manip/real |
| [StageGuard: Learning Stage Transitions for Long-Horizon Robot Tasks via Agentic Distillation](https://arxiv.org/abs/2609.20791) | 2026-09 | C | re-decide | manip/sim |
| [TADreamer: Zero-Shot Language-Guided 3D Navigation for Terrestrial-Aerial Bimodal Robots via Video Imagination](https://arxiv.org/abs/2609.19824) | 2026-09 | G | none | aerial/real |
| [EmoPose: Vision-Language Model Guided Emotion-Aware Gesture Generation for Humanoid Robots](https://arxiv.org/abs/2609.23414) | 2026-09 | G | none | social/sim |
| SMaRTAban: a voice-controlled LLM agent for quadruped mobile robotics with integrated vision | 2026-09 | G | re-decide | loco/real |
| [MedVLA: A Hierarchical Vision-Language-Action Framework for Closed-Loop Precision Medical Robot Manipulation](https://arxiv.org/abs/2609.25756) | 2026-09 | C | re-decide | manip/sim |
| [OCC4M: Object-Centric 4D Memory for Spatiotemporal Reasoning in Long-Horizon Manipulation](https://arxiv.org/abs/2609.28798) | 2026-09 | G | none | manip/sim+real |
| [Design and Evaluation of LLM Chaining-Based Task Planning for General Purpose Service Robots](https://arxiv.org/abs/2609.29043) | 2026-09 | G | none | mobile-manip/real |
| [From Passive Execution to Active Exploration: Agentic Embodied Manipulation in Realistic Environments](https://arxiv.org/abs/2609.29091) | 2026-09 | G | re-decide | manip/sim+real |
| [GraspTwin: Zero-Shot Task-Oriented Grasp Optimization via a Digital Twin](https://arxiv.org/abs/2609.30543) `real2sim2real` | 2026-09 | G | none | manip/sim+real |
| [Robo-Harness K1: Harnessing Robot-Use Agents via Perception Augmentation](https://arxiv.org/abs/2609.29389) | 2026-09 | G | re-decide | manip/sim |
| [CoralPlan: Observation Skill Selection and Execution for Underwater Robotic Inspection](https://arxiv.org/abs/2609.31211) | 2026-09 | G | none | other/sim+real |
| [Assisting for Open-Ended Tasks: Goal-Oriented Shared Autonomy as a Particle Filter](https://arxiv.org/abs/2609.32576) | 2026-09 | G | re-decide | manip/real |
| [Robot-GST: geometry-aware spatial-temporal robot policy representation and evaluation](https://arxiv.org/abs/2609.33872) `real2sim2real` | 2026-09 | G | none | manip/real |
| LLM-driven embodied intelligent system for autonomous open-channel hydraulics: design and validation via long-duration PIV measurements | 2026-09 | G | re-decide | other/real |
| [Where Memory Belongs: Ledger, an Object Ledger for Memory-Augmented VLAs](https://arxiv.org/abs/2609.34554) | 2026-09 | G | re-decide | manip/sim |
| Agentic Preparative
Thin-Layer Chromatography System
for Autonomous Purification | 2026-09 | G | re-decide | manip/real |
| [Simple Agentic Memory for Generalist Robot Policies](https://arxiv.org/abs/2609.36595) | 2026-09 | G | re-decide | manip/sim |
| Physical AI for Autonomous Manufacturing: A Dual Process VLM-VLA Framework for Task Assistant Robots | 2026-09 | G | none | manip/real |
| [RoboAssist: Interactive Human-Humanoid Planning for Long-Horizon Surgical Assistance](https://arxiv.org/abs/2609.39384) | 2026-09 | G | re-decide | humanoid/sim |
| [DuoMind: Enabling Distributed Multi-Robot Coordination with Semantic Communication](https://arxiv.org/abs/2610.02161) | 2026-10 | G | re-decide | multi-robot/sim |
| Robot Independent Intelligence: When Language Vanishes in Vision-Language-Action Models | 2026-10 | G | none | manip/sim |
| Vision language model-enhanced embodied intelligence for AR-assisted HRC assembly: Multimodal cognition, task reasoning, and autonomous execution | 2026-10 | G | none | manip/real |
| A Neuro-Symbolic Framework for LLM-Driven Task Planning and Execution in Industrial Assembly | 2026-10 | G | none | manip/real |
| [ROMA: LLM System for Real-World Object-Centric Multi-Sensory Active Perception](https://arxiv.org/abs/2610.06955) | 2026-10 | C | re-decide | manip/real |
| [CIRRA: Dual-Level Continual Instruction Reconciliation with Ongoing Execution for Embodied Robot Agents in Interactive Household Tasks](https://arxiv.org/abs/2610.08862) | 2026-10 | G | re-decide | humanoid/real |
| [From Social Reasoning to Embodied Interaction: An Agentic Framework for Social Robots](https://arxiv.org/abs/2610.05964) | 2026-10 | G | re-decide | social/real |
| [Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843) | 2026-10 | G | re-decide | manip/sim+real |
| [Event-Driven Proactive Robot Assistance through Vision-Language Reasoning](https://arxiv.org/abs/2610.08344) | 2026-10 | G | none | manip/real |
| [Toward Evidence-Driven Human-Agent-Robot Teaming for Earth-Independent Anomaly Triage](https://arxiv.org/abs/2610.08933) | 2026-10 | G | re-decide | mobile-manip/real |
| CAD2Real: CAD-Grounded Skill Primitives and Vision-Language Planning for Precision Assembly `sim2real` | 2026-11 | G | re-decide | manip/sim+real |
| LLM-augmented progressive search for efficient multi-robot task planning | 2026-11 | G | none | multi-robot/sim |
| Speech-guided unmanned aerial vehicle control system based on large language model-structured execution graphs with expert rule constraints | 2026-11 | G | none | aerial/sim+real |

</details>

<details><summary><b>Controller · Direct drivers</b> (160)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| Adaptive Painting Strategy Generation for Embodied Robotic Painting via LLM-Based AI Agents | 2026 | G | none | manip/real |
| Embodied AI Agent Framework for (Re)Programming Robotic Tasks in Flexible Assembly using LLMs and VLMs | 2026 | G | none | manip/real |
| From Ambiguous Language to Verifiable Plans: Integrating Formal Synthesis and Dynamic Affordance Reasoning | 2026 | G | authored | manip/sim |
| Hierarchical Generation of Robot Programs Based on the Integration of Visual Affordance Recognition and Language Model | 2026 | G | none | manip/real |
| LLM-Grounded Dynamic Task Planning with Hierarchical Temporal Logic for Human-Aware Multi-Robot Collaboration | 2026 | G | re-decide | multi-robot/sim+real |
| LLM-Guided Human-Drone Interaction for Autonomous Mission Execution | 2026 | G | none | aerial/real |
| LLM-Guided Scene Graph-Conditioned Diffusion for Robotic Autonomous Tabletop Arrangement | 2026 | G | none | manip/sim+real |
| Llm and nlp-based drone control: A distributed edge computing architecture for Vietnamese | 2026 | G | none | aerial/real |
| Natural Language to Code: A Lightweight QLoRA-Tuned LLM for Multitask UAV Control | 2026 | C | none | aerial/sim |
| Physical Simulation‐Based Correction of LLM‐Generated Tool‐Using Primitives `sim2real` | 2026-01 | G | re-decide | manip/sim+real |
| [Hybrid Distillation with CoT Guidance for Edge-Drone Control Code Generation](https://arxiv.org/abs/2601.08412) | 2026-01 | C | none | aerial/sim |
| [Large Language Models to Enhance Multi-task Drone Operations in Simulated Environments](https://arxiv.org/abs/2601.08405) | 2026-01 | C | none | aerial/sim |
| [Real2Sim via Active Perception with Behavior Trees Automatically Generated by VLMs](https://arxiv.org/abs/2601.08454) `real2sim` | 2026-01 | G | authored | manip/real |
| [Bidirectional Human-Robot Communication for Physical Human-Robot Interaction](https://arxiv.org/abs/2601.10796) | 2026-01 | G | re-decide | manip/real |
| [ALRM: Agentic LLM for Robotic Manipulation](https://arxiv.org/abs/2601.19510) | 2026-01 | G | re-decide | manip/sim |
| Enhancing the Worker–Robot Interaction for Construction Task Operation: A Preliminary Study Using Large Language Model-Based Methods | 2026-01 | G | none | other/sim |
| Leveraging Large Language Models for Voice-Activated Robotic Teleoperation in Construction | 2026-01 | G | none | other/real |
| A Multimodal Adaptive Framework for Social Interaction with the MiRo-E Robot | 2026-02 | G | re-decide | social/real |
| [Coordinated Control of Multiple Construction Machines Using LLM-Generated Behavior Trees with Flag-Based Synchronization](https://arxiv.org/abs/2602.01041) | 2026-02 | G | authored | multi-robot/sim+real |
| [SkySim: A ROS2-based Simulation Environment for Natural Language Control of Drone Swarms using Large Language Models](https://arxiv.org/abs/2602.01226) | 2026-02 | G | none | multi-robot/sim |
| [BTGenBot-2: Efficient Behavior Tree Generation with Small Language Models](https://arxiv.org/abs/2602.01870) | 2026-02 | C | re-decide | mobile-manip/sim+real |
| [Language Movement Primitives: Grounding Language Models in Robot Motion](https://arxiv.org/abs/2602.02839) | 2026-02 | G | none | manip/real |
| [VLN-Pilot: Large Vision-Language Model as an Autonomous Indoor Drone Operator](https://arxiv.org/abs/2602.05552) | 2026-02 | G | re-decide | aerial/sim |
| [AtomBridge: Agentic VLA Inference Plugin for Long-Horizon Tasks in Scientific Experiments](https://arxiv.org/abs/2602.09430) | 2026-02 | G | re-decide | manip/real |
| [LLM-Grounded Dynamic Task Planning with Hierarchical Temporal Logic for Human-Aware Multi-Robot Handover](https://arxiv.org/abs/2602.09472) | 2026-02 | G | authored | multi-robot/sim+real |
| LLM-Based Decision Making Framework for Autonomous Drone Navigation | 2026-02 | G | re-decide | aerial/sim |
| [Safe and Interpretable Multimodal Path Planning for Multi-Agent Cooperation](https://arxiv.org/abs/2602.19304) | 2026-02 | G | re-decide | multi-robot/sim+real |
| [ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking](https://arxiv.org/abs/2602.21161) | 2026-02 | G | re-decide | manip/sim |
| [SAGE-LLM: Towards Safe and Generalizable LLM Controller with Fuzzy-CBF Verification and Graph-Structured Knowledge Retrieval for UAV Decision](https://arxiv.org/abs/2602.23719) | 2026-02 | G | re-decide | aerial/sim |
| Integrating Soft Gripper and Gripping Agent for Universal Robotic Grasping | 2026-02 | G | none | manip/real |
| Developing RAGs for robot code generation | 2026-03 | G | none | manip/sim |
| [From Dialogue to Execution: Mixture-of-Agents Assisted Interactive Planning for Behavior Tree-Based Long-Horizon Robot Execution](https://arxiv.org/abs/2603.01113) | 2026-03 | G | authored | manip/real |
| [Give me scissors: Collision-Free Dual-Arm Surgical Assistive Robot for Instrument Delivery](https://arxiv.org/abs/2603.02553) | 2026-03 | G | none | manip/real |
| [IMR-LLM: Industrial Multi-Robot Task Planning and Program Generation using Large Language Models](https://arxiv.org/abs/2603.02669) | 2026-03 | G | none | multi-robot/sim |
| [EmboAlign: Aligning Video Generation with Compositional Constraints for Zero-Shot Manipulation](https://arxiv.org/abs/2603.05757) | 2026-03 | G | none | manip/real |
| [RACAS: Controlling Diverse Robots With a Single Agentic System](https://arxiv.org/abs/2603.05621) | 2026-03 | G | re-decide | other/real |
| [RoboCritics: Enabling Reliable End-to-End LLM Robot Programming through Expert-Informed Critics](https://arxiv.org/abs/2603.06842) | 2026-03 | G | none | manip/real |
| RoboTheater: A Multi-Robot Storytelling Platform from LLM Scripts to Stage Performance | 2026-03 | G | none | multi-robot/real |
| [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824) | 2026-03 | G | re-decide | aerial/sim+real |
| Towards Autonomous UAV Visual Object Search in City Space: Benchmark and Agentic Methodology | 2026-03 | G | re-decide | aerial/sim |
| [AeroGen: Agentic Drone Autonomy through Single-Shot Structured Prompting & Drone SDK](https://arxiv.org/abs/2603.14236) | 2026-03 | G | none | aerial/sim+real |
| Communicating Object Relations through Robot Gestures | 2026-03 | G | none | social/real |
| [Confusion-Aware In-Context-Learning for Vision-Language Models in Robotic Manipulation](https://arxiv.org/abs/2603.15134) | 2026-03 | G | none | manip/sim |
| Context-Aware Generation and Modulation of Expressive Motion Behavior using Multimodal Foundation Models | 2026-03 | G | none | humanoid/real |
| Expressive Furhat: Generating Real-Time Facial Expressions for Human-Robot Dialogue with LLMs | 2026-03 | G | none | social/real |
| Holistic LLM-Based Expressive Behavior Generation for Robots | 2026-03 | G | none | social/real |
| Winnie-the-Pooh-Powered: How LLMs and Well-Known Characters Can Create Adaptive Personalities for Aquatic Social Robot Interactions | 2026-03 | G | none | social/real |
| “I Loved How Pepper Talked About My Hoodie”: A Situated, MI-Grounded Multimodal Architecture for Engaging Conversation | 2026-03 | G | re-decide | social/real |
| [Cross-Domain Demo-to-Code via Neurosymbolic Counterfactual Reasoning](https://arxiv.org/abs/2603.18495) | 2026-03 | G | none | manip/sim |
| [The Robot’s Inner Critic: Self-Refinement of Social Behaviors through VLM-based Replanning](https://arxiv.org/abs/2603.20164) | 2026-03 | G | re-decide | social/sim |
| [Can a Robot Walk the Robotic Dog: Triple-Zero Collaborative Navigation for Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2603.21723) | 2026-03 | G | re-decide | multi-robot/real |
| [A Multimodal Framework for Human-Multi-Agent Interaction](https://arxiv.org/abs/2603.23271) | 2026-03 | G | re-decide | social/real |
| [PhotoAgent: A Robotic Photographer with Spatial and Aesthetic Understanding](https://arxiv.org/abs/2603.22796) `real2sim2real` | 2026-03 | G | re-decide | other/sim+real |
| Intent-Driven Cooperative Control of UAV Swarms: An LLM-Based Approach | 2026-03 | G | none | aerial/sim |
| [Fine-Tuning Large Language Models for Cooperative Tactical Deconfliction of Small Unmanned Aerial Systems](https://arxiv.org/abs/2603.28561) | 2026-03 | C | none | aerial/sim |
| [Learning Structured Robot Policies from Vision-Language Models via Synthetic Neuro-Symbolic Supervision](https://arxiv.org/abs/2604.02812) | 2026-04 | C | authored | manip/sim+real |
| VLM-Nav: Mapless UAV navigation using monocular vision driven by vision-language models | 2026-04 | G | none | aerial/sim |
| Verification and execution of the scientific literature via chemputation augmented by large language models | 2026-04 | G | none | other/real |
| [Automating Manual Tasks through Intuitive Robot Programming and Cognitive Robotics](https://arxiv.org/abs/2604.05978) | 2026-04 | G | none | manip/real |
| [CoEnv: Driving Embodied Multi-Agent Collaboration via Compositional Environment](https://arxiv.org/abs/2604.05484) `real2sim2real` | 2026-04 | G | re-decide | multi-robot/sim+real |
| [BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields](https://arxiv.org/abs/2604.08410) | 2026-04 | G | none | manip/real |
| Real-Time UAV Swarm Autonomy Using Edge-Deployed Small Language Models | 2026-04 | G | none | aerial/real |
| Visual scene drawing through human–robot natural language interactions using lightweight large language models | 2026-04 | G | none | manip/real |
| [CLASP: Closed-loop Asynchronous Spatial Perception for Open-vocabulary Desktop Object Grasping](https://arxiv.org/abs/2604.11320) | 2026-04 | G | re-decide | manip/real |
| [Ro-SLM: Onboard Small Language Models for Robot Task Planning and Operation Code Generation](https://arxiv.org/abs/2604.10929) | 2026-04 | C | none | aerial/sim+real |
| Rob2HanD: LLM-Driven Robotic Arm for IMU Interaction Dataset Generation | 2026-04 | G | none | manip/real |
| Semi-Automated Programming of Industrial Robotic Systems Using Large Language Models and Standardized Data Model | 2026-04 | G | none | manip/sim |
| LLM-Based Adaptive Control Code Generation Framework with Digital Twin-Integrated Verification for Heterogeneous Robot Systems `sim2real` | 2026-04 | G | none | multi-robot/sim |
| [FineCog-Nav: Integrating Fine-grained Cognitive Modules for Zero-shot Multimodal UAV Navigation](https://arxiv.org/abs/2604.16298) | 2026-04 | G | re-decide | aerial/sim |
| An Environment-Aware Verification Framework for LLM-Generated Robot Control Programs | 2026-04 | G | authored | manip/sim |
| Lingo2Action: Fusing Semantic Risk and Perceptual Uncertainty for Adaptive 3D Value Maps | 2026-04 | G | none | manip/sim+real |
| [CoRAL: Contact-Rich Adaptive LLM-based Control for Robotic Manipulation](https://arxiv.org/abs/2605.02600) | 2026-05 | G | re-decide | manip/sim+real |
| [LASSA Architecture-Based Autonomous Fault-Tolerant Control of Unmanned Underwater Vehicles](https://arxiv.org/abs/2605.09494) | 2026-05 | G | re-decide | other/sim+real |
| [LMPath: Language-Mediated Priors and Path Generation for Aerial Exploration](https://arxiv.org/abs/2605.13782) | 2026-05 | G | none | aerial/real |
| Natural Language-Based Control of Integrated Aerial Platform Using Large Language Models | 2026-05 | G | none | aerial/sim |
| Zero-Fine-Tuning Safety-First Closed-Loop Decision Making for UAVs | 2026-05 | G | none | aerial/sim |
| Intelligent Control System for a Collaborative Robot Based on Large Language Models | 2026-05 | G | none | manip/sim+real |
| Adaptive Human-machine Systems with Automated Control of Large Language Models for Unmanned Aerial Vehicle Control | 2026-05 | G | none | aerial/sim |
| Behavior Tree Generation with LLM-MCTS-BT as a Pre-Planner Bridging Priors and Uncertainty | 2026-05 | G | none | other/sim |
| [Agentic Language-to-Objective Synthesis for Optofluidic Assembly](https://arxiv.org/abs/2605.27643) | 2026-05 | G | authored | other/sim+real |
| [GSAM: A Generalizable and Safe Robotic Framework for Articulated Object Manipulation](https://arxiv.org/abs/2605.30740) | 2026-05 | G | none | manip/sim+real |
| AGRI-BT Robot: LLM-Driven Behaviour Trees and VLM Perception for Intelligent Autonomous Greenhouse Operations | 2026-06 | G | authored | mobile-manip/real |
| Embodied SelfRect Robot: A Multi-Large-Model Control Framework with Iterative Self-Correction for Robotic Manipulation | 2026-06 | G | re-decide | manip/real |
| From Language to Deployment: Oﬄine Optimization and Ontology-Guided Behavior Tree Generation for Transparent Robot Applications | 2026-06 | G | none | other/sim |
| LLM-DTS: Resilience Formation Control Via Semantic Reasoning and Adaptive Topology Switching | 2026-06 | G | re-decide | multi-robot/sim |
| TACSEM: Tactile Sensing, 3-D State Estimation and In-Hand Manipulation of a Soft Hand | 2026-06 | G | none | manip/real |
| Towards Large-Model-Guided UAV Navigation in Complex Environments | 2026-06 | G | re-decide | aerial/sim |
| A Robotic Disassembly Planning Method for Retired Batteries Based on a Long Short-Term Memory Collaborative Framework | 2026-06 | G | none | manip/real |
| [Efficient Skill Grounding via Code Refactoring with Small Language Models](https://arxiv.org/abs/2606.07999) | 2026-06 | G | none | manip/sim |
| Feasibility Study of Programming Compliant Bimanual Tasks with Reasoning LLMs | 2026-06 | G | none | manip/sim+real |
| [Bounding Boxes as Goals: Language-Conditioned Grasping via Neuro-Symbolic Planning](https://arxiv.org/abs/2606.12910) | 2026-06 | G | none | manip/real |
| CoStage: An Embodied AI Co-Creation System for Children’s Performative Storytelling with Robots | 2026-06 | G | none | multi-robot/real |
| LLM‐Integrated Human–Robot Interaction System for Microrobots | 2026-06 | G | none | other/real |
| Robotics and ChatGPT: Educational Application | 2026-06 | G | none | manip/real |
| [Generating Natural and Expressive Robot Gestures through Iterative Reinforcement Learning with Human Feedback using LLMs](https://arxiv.org/abs/2606.18747) | 2026-06 | G | re-decide | social/real |
| [ZeroDex: Zero-Shot Long-Horizon Dexterous Manipulation via Multi-View 3D-Grounded VLM Reasoning](https://arxiv.org/abs/2606.19340) | 2026-06 | G | none | manip/real |
| [Dual-Agent Framework for Cross-Model Verified Translation of Natural-Language Protocols into Robotic Laboratory Platform](https://arxiv.org/abs/2606.20120) | 2026-06 | G | none | other/real |
| [CLOSER-VLN: Closed-Loop Self-Verified Retrieval-Augmented Reasoning for Aerial Vision-Language Navigation](https://arxiv.org/abs/2606.28397) | 2026-06 | G | none | aerial/sim |
| [RelAfford6D: Relational 6D Affordance Graphs for Constraint-Driven Robotic Manipulation](https://arxiv.org/abs/2606.27036) | 2026-06 | G | authored | manip/real |
| [Embedding Large Language Models into Flow Controls: An Agentic Framework for Adaptive and Trustworthy Automated Cooking](https://arxiv.org/abs/2608.04768) | 2026-06 | G | authored | manip/real |
| LLM-Based Active Perception Control for Occlusion Avoidance and Safe Approach in Harvesting Robots | 2026-06 | G | none | manip/real |
| Prompt Optimization Through Reinforcement Learning for Generative Language Model Code Synthesis in Multi-Robot Systems | 2026-07 | G | none | multi-robot/sim |
| Robotic Arm Motion Planning and Task Execution by Using Vision Language Models | 2026-07 | G | none | manip/real |
| [Hypothesis-driven Model Expansion under Uncertainty for Open-World Robot Planning](https://arxiv.org/abs/2607.06501) | 2026-07 | G | re-decide | mobile-manip/sim+real |
| A dual-agent framework for physically grounded and syntactically verifiable industrial robot programming | 2026-07 | G | re-decide | manip/sim+real |
| [Contract-Grounded Behavior Tree Synthesis via Coding Agents](https://arxiv.org/abs/2607.12220) | 2026-07 | G | none | manip/sim |
| [A Generative Partially Specified Finite State Machine Approach to Complex Behaviour Planning](https://arxiv.org/abs/2607.15674) | 2026-07 | G | authored | mobile-manip/sim |
| [FARO: Feasibility-Aware Robot Motion Optimization](https://arxiv.org/abs/2607.18362) | 2026-07 | G | none | humanoid/sim+real |
| [STeP: Signal Temporal Logic for Precise Specifications for Action Generation with Vision Language Models](https://arxiv.org/abs/2607.18580) | 2026-07 | G | authored | manip/sim+real |
| [No Training, Better Flights: Test-Time Scaled VLMs for UAV Navigation](https://arxiv.org/abs/2607.19288) | 2026-07 | G | none | aerial/sim |
| [World Action Planner: Generalizable Robot Decision-Making with Action-Conditioned World Models](https://arxiv.org/abs/2607.27599) | 2026-07 | G | none | manip/sim+real |
| CityFly: Signmark-guided autonomous UAV navigation with vision language model | 2026-08 | G | none | aerial/sim |
| LLM-in-the-Loop Variable Impedance Control: Towards Safe Generalized and Personalized Robotic Interactions | 2026-08 | G | re-decide | manip/real |
| LVR-Draw: A Language-Vision Pipeline for Robotic Drawing with Interactive Scene Verification and Correction | 2026-08 | G | none | manip/real |
| PCK-RL: A Unified Framework for Vision-Language Model and Reinforcement Learning-Based Robotic Manipulation | 2026-08 | G | none | manip/sim+real |
| Talk-to-Fly: An Agentic LLM Runtime for Natural-Language UAV Task Control | 2026-08 | G | re-decide | aerial/sim+real |
| Zero-Shot Affordance Exposure for Robotic Manipulation Via Object Repositioning | 2026-08 | G | none | manip/real |
| CoMuRoS - An LLM-based generalizable hierarchical task planning and execution framework for heterogeneous robot teams with event-driven re-planning | 2026-08 | G | re-decide | multi-robot/sim+real |
| [Vision-Language Models as copilots for Autonomous UAV Navigation: Analysis of Latency and Reliability in Degraded Environments](https://arxiv.org/abs/2609.26084) | 2026-08 | G | none | aerial/sim |
| [Closing the Affective Loop: Multimodal Speaker-Listener Emotion-Dynamics-Aware Empathetic Social Robots](https://arxiv.org/abs/2608.16686) | 2026-08 | G | re-decide | social/real |
| [PDDL-ART: Autonomous Symbolic Abstraction From Demonstration For Long-Horizon Robotic Manipulation Using Vision-Language Models](https://arxiv.org/abs/2608.17146) | 2026-08 | G | re-decide | manip/sim+real |
| [VLCP: Vision Language Control Policy Closed-Loop Code Replanning for Robot Manipulation](https://arxiv.org/abs/2608.16978) | 2026-08 | G | re-decide | manip/sim |
| [APPROVE: Visual End-User-in-the-Loop Robot Programming with LLMs](https://arxiv.org/abs/2608.19281) | 2026-08 | G | none | manip/real |
| [PhysCaP: Grounding Code-as-Policy Agent with Physics-Informed Exploration](https://arxiv.org/abs/2608.21031) | 2026-08 | G | re-decide | manip/sim+real |
| [EndoNav: Semantic-to-Geometric Grounding for Language-Guided Robotic Endoscopic Examination](https://arxiv.org/abs/2608.22093) | 2026-08 | G | none | manip/sim+real |
| [Leveraging Inter-object Affordances for Efficient Planning in Contact-rich Tasks](https://arxiv.org/abs/2608.25641) | 2026-08 | G | none | manip/sim+real |
| Neuroergonomic signatures of improved human–robot collaboration in LLM-supported industrial workflows | 2026-08 | G | none | manip/sim |
| Behavior-triggered self-reflection for zero-shot open-domain UAV target search | 2026-09 | G | re-decide | aerial/sim |
| Empowering Precise Embodied Agents with Executable Analytic Concepts as Semantic-Physical Blueprints | 2026-09 | G | none | manip/sim+real |
| Structured LLM-to-action grounding for a dual-wheel-legged robot: A modular real-robot study | 2026-09 | G | none | loco/real |
| A Hybrid LLM/Model-Based Architecture for Flexible and Adaptive Robot Coaching | 2026-09 | G | none | social/real |
| [La Agente Óptima: Towards Agentic Self-Driving Laboratories](https://arxiv.org/abs/2609.04564) | 2026-09 | G | re-decide | other/real |
| [Language-Guided Terrain-Adaptive Neural MPC for Autonomous Traversal of Articulated Tracked Robots](https://arxiv.org/abs/2609.13083) | 2026-09 | G | re-decide | loco/sim+real |
| [Auto-HSI: Personalized human control of a robot swarm on demand by using LLMs for online automatic code generation](https://arxiv.org/abs/2609.16346) | 2026-09 | G | none | multi-robot/sim |
| [ManiSkillFormer: Demonstration-Free Compositional Manipulation via Geometric Contracts and Agentic Skill Graph](https://arxiv.org/abs/2609.16331) | 2026-09 | G | none | manip/real |
| [Quantitative control and recording of materials-synthesis processes using an automated experimentation platform](https://arxiv.org/abs/2609.14928) | 2026-09 | G | none | manip/real |
| [HINT-Plan: Human Intention-Aware Robot Task Planning in Context-Rich Environments using Vision Language Models](https://arxiv.org/abs/2609.17771) | 2026-09 | G | none | mobile-manip/sim |
| [In-Context Robot Learning with VLM Agents](https://arxiv.org/abs/2609.19138) | 2026-09 | G | re-decide | manip/sim+real |
| [Kinematics-Grounded Agentic AI for Robotic Additive Manufacturing Process Planning](https://arxiv.org/abs/2609.19347) | 2026-09 | G | none | manip/sim |
| [Coding Agents with Harness for Safe Robot Control](https://arxiv.org/abs/2609.20822) | 2026-09 | G | re-decide | manip/sim+real |
| [V2-STRep: VLM-Grounded Structured Task Representations for Reusable Robot Skills Acquired from Generated Videos](https://arxiv.org/abs/2609.20582) | 2026-09 | G | none | manip/real |
| [AgenticSwarm: Semantic Perception and Adaptive Task Allocation for Heterogeneous Multi-UAV Missions](https://arxiv.org/abs/2609.21716) | 2026-09 | G | authored | multi-robot/sim+real |
| [Search, Ground, Plan: Functional Sufficiency for Task and Motion Planning under Incomplete Scene Knowledge](https://arxiv.org/abs/2609.23113) | 2026-09 | G | re-decide | mobile-manip/sim |
| [Transferring the Intelligence of VLMs to Robotic Control](https://arxiv.org/abs/2609.22966) | 2026-09 | G | re-decide | manip/sim |
| [Generalizing Manipulation Skills with a Local Coding Agent](https://arxiv.org/abs/2609.26499) | 2026-09 | G | re-decide | manip/real |
| Execution-aware agent harness for accessible and responsible synthetic biology automation | 2026-09 | G | re-decide | other/real |
| [World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal](https://arxiv.org/abs/2609.29964) | 2026-09 | G | re-decide | manip/real |
| [DualManip: Agentic Dynamic Manipulation via Dual-Path Semantic Reasoning and Geometric Adaptation](https://arxiv.org/abs/2609.31112) | 2026-09 | G | re-decide | manip/real |
| [Representation-Guided Generation and Integration of Executable Programs for Robot Manipulation](https://arxiv.org/abs/2609.31337) | 2026-09 | G | none | manip/sim |
| [Bayesian Active Learning for Intent Disambiguation in Interactive Robot Planning](https://arxiv.org/abs/2609.34270) | 2026-09 | G | none | manip/sim+real |
| [From Language to Task Maps: Compiling Semantic Relations While Preserving Task-Relevant Freedom](https://arxiv.org/abs/2609.34412) | 2026-09 | G | authored | manip/sim |
| [RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261) | 2026-09 | G | re-decide | manip/sim |
| [MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation](https://arxiv.org/abs/2609.38078) | 2026-09 | G | re-decide | manip/sim+real |
| [WayFinder: Hierarchical Visual-Language-Action for Zero-Shot Waypoint Generation and Low-Level Kinematic Control](https://arxiv.org/abs/2609.37922) | 2026-09 | G | re-decide | aerial/sim |
| GAS-Robo: Converting Scene Into a Grid-Action Space for LLM-Driven Open-Ended Robotic Manipulation | 2026-10 | G | none | manip/sim |
| [OrbitTAMP: Grounding Language Models for Task and Motion Planning in Spacecraft Rendezvous](https://arxiv.org/abs/2610.01093) | 2026-10 | G | none | other/sim |
| Video-Grounded Verification for Long-Horizon Visual Imitation Learning | 2026-10 | G | none | manip/sim+real |
| [TacZero: Training-Free Peg Insertion Using a General-Purpose Vision-Language Model with Tactile Feedback](https://arxiv.org/abs/2610.07621) | 2026-10 | G | re-decide | manip/real |
| [Adaptive Code Generation for Controlling Robots](https://arxiv.org/abs/2610.09588) | 2026-10 | G | re-decide | loco/sim |
| LLM-Assisted Emotional Expressive Behavior Generation for Engagement Enhancements in Human-Robot Interaction | 2026-11 | G | none | social/real |

</details>

<details><summary><b>Controller · Lifelong / memory agents</b> (36)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| Agentic HRC: Achieving context alignment via memory for Human-Robot Collaboration | 2026 | G | none | manip/real |
| Agentic Memory: Enabling Situational Resonance in Human-Robot Collaboration | 2026 | G | none | manip/real |
| [Learning Without Losing Identity: Capability Evolution for Embodied Agents](https://arxiv.org/abs/2604.07799) | 2026 | G | re-decide | manip/sim |
| [MeCo: Enhancing LLM-Empowered Multi-Robot Collaboration via Similar Task Memoization](https://arxiv.org/abs/2601.20577) | 2026-01 | G | none | multi-robot/sim |
| [Learning from Trials and Errors: Reflective Test-Time Planning for Embodied LLMs](https://arxiv.org/abs/2602.21198) | 2026-02 | C | re-decide | mobile-manip/sim |
| [Uni-Skill: Building Self-Evolving Skill Repository for Generalizable Robotic Manipulation](https://arxiv.org/abs/2603.02623) | 2026-03 | G | re-decide | manip/sim+real |
| [From Local Corrections to Generalized Skills: Improving Neuro-Symbolic Policies with MEMO](https://arxiv.org/abs/2603.04560) | 2026-03 | G | re-decide | manip/real |
| [RoboRouter: Training-Free Policy Routing for Robotic Manipulation](https://arxiv.org/abs/2603.07892) | 2026-03 | G | re-decide | manip/sim+real |
| [BrainMem: Brain-Inspired Evolving Memory for Embodied Agent Task Planning](https://arxiv.org/abs/2604.16331) | 2026-03 | G | re-decide | mobile-manip/sim |
| [VersualRL: Closed-Loop Verbal Reinforcement Learning with Visual Execution Feedback for Task-Level Robot Planning](https://arxiv.org/abs/2603.22169) | 2026-03 | G | re-decide | mobile-manip/real |
| [GUIDE: Guided Updates for In-context Decision Evolution in LLM-Driven Spacecraft Operations](https://arxiv.org/abs/2603.27306) | 2026-03 | G | re-decide | other/sim |
| [Evolvable Embodied Agent for Robotic Manipulation via Long Short-Term Reflection and Optimization](https://arxiv.org/abs/2604.13533) | 2026-04 | G | re-decide | manip/sim |
| [Long-Term Memory for VLA-based Agents in Open-World Task Execution](https://arxiv.org/abs/2604.15671) | 2026-04 | G | re-decide | manip/real |
| [ARIS: Agentic and Relationship Intelligence System for Social Robots](https://arxiv.org/abs/2605.00943) | 2026-05 | G | re-decide | social/real |
| [Analytic Concept-Centric Memory for Agentic Embodied Manipulation](https://arxiv.org/abs/2606.29774) | 2026-06 | G | re-decide | manip/sim+real |
| [A Self-Evolving Agentic System for Automated Generation and Execution of Biological Protocols](https://arxiv.org/abs/2606.31763) | 2026-06 | G | re-decide | other/real |
| SRDrone: LLM-Driven Self-Refinement for Embodied Drone Task Planning | 2026-07 | G | re-decide | aerial/sim+real |
| [PhyAgentOS: A Self-Evolving Operating System for Embodied Agents with Decoupled Cognitive Planning and Physical Execution](https://arxiv.org/abs/2607.16636) | 2026-07 | G | re-decide | multi-robot/sim+real |
| [RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning](https://arxiv.org/abs/2607.18060) | 2026-07 | G | re-decide | manip/sim+real |
| [WCM: World-Cognition Model for Generalizable Human-Robot Interaction](https://arxiv.org/abs/2607.22999) | 2026-07 | C | re-decide | manip/sim+real |
| [Practice Makes Policies: Bootstrapping and Consolidating Robotic Capabilities from Zero Human Demonstrations](https://arxiv.org/abs/2607.26809) | 2026-07 | G | re-decide | manip/sim+real |
| [LabEvolver: Training-Free Experience Evolution for Safe and Grounded Wet-Lab Agents](https://arxiv.org/abs/2607.27690) | 2026-07 | G | re-decide | manip/real |
| [SkillComposer: Learning Reusable Skills for Natural-Language Robot Programming](https://arxiv.org/abs/2608.14944) | 2026-08 | G | re-decide | manip/sim |
| [Don't Drop the BATON: Long-Horizon Robot Manipulation via Agentic Subtask Exploration and Transition-aware Memory](https://arxiv.org/abs/2608.16889) | 2026-08 | G | re-decide | manip/sim+real |
| [Know Your Body: A Harness for Direct and Self-Improving Robot Control with VLMs](https://arxiv.org/abs/2609.28530) | 2026-09 | G | re-decide | manip/real |
| [RegenHarness: A Robot Agent Harness with Evidence-Gated Recursive Self-Improvement](https://arxiv.org/abs/2609.27612) | 2026-09 | G | re-decide | manip/sim+real |
| [RoboFoundry: System-as-Policy Evolution for Self-Learning Embodied Agents](https://arxiv.org/abs/2609.32862) | 2026-09 | G | re-decide | manip/sim+real |
| [EMPIRIC: Experiment-Driven Learning of Residual World Models for Robot Planning](https://arxiv.org/abs/2609.35047) `real2sim` | 2026-09 | G | re-decide | manip/sim+real |
| [Self-Evolving Coding Agents: From Digital Programs to Physical-World Intelligence](https://arxiv.org/abs/2609.35432) | 2026-09 | G | re-decide | manip/real |
| [Explore, Execute, Evolve: A Skill Acquisition and Reuse Loop for Embodied Agents](https://arxiv.org/abs/2609.37810) | 2026-09 | G | re-decide | manip/sim |
| [RoboHarn-Evo: Evolving Hierarchical Physical Knowledge for Self-Improving Robotic Manipulation](https://arxiv.org/abs/2609.37583) | 2026-09 | G | re-decide | manip/sim |
| [InterEvolve: Test-Time Evolution of Reward Programs for Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.02196) | 2026-10 | G | re-decide | humanoid/sim |
| [MobiAgent: Dual-Loop Recursive Policy Self-Improvement for Long-Horizon Mobile Manipulation](https://arxiv.org/abs/2610.03476) | 2026-10 | G | re-decide | mobile-manip/real |
| [RoboBridge: A Self-Evolving Embodied Agent Framework for Sim-to-Real Transfer](https://arxiv.org/abs/2610.02717) | 2026-10 | G | re-decide | manip/sim+real |
| [ProactiveVLA: Augmenting Embodied Memory through Proactive Environment Exploration](https://arxiv.org/abs/2610.06999) | 2026-10 | G | re-decide | manip/sim |
| [RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929) | 2026-10 | G | re-decide | manip/sim+real |

</details>

<details><summary><b>VLN and embodied navigation</b> (96)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| AgenticNav: A Hierarchical Multi-Agentic System for LLM-Driven Autonomous Problem-Solving in Robotics | 2026 | G | re-decide | nav/sim+real |
| EmergeNav: Structured Embodied Inference for Zero-Shot Vision-and-Language Navigation in Continuous Environments | 2026 | G | re-decide | nav/sim |
| From Natural Language to Nonlinear Programs: An Agentic Framework for Instruction-Guided Trajectory Planning of Wheeled Robots | 2026 | G | re-decide | nav/sim |
| VOCA: A VLM-Optimized Call Approach for Zero-Shot Navigation Using Target-Context Cues | 2026 | G | re-decide | nav/sim |
| LLM-KGFP: A Chain-of-Thought-Driven Knowledge Graph Planner for Autonomous Rover Operations in Lunar Polar Shadowed Regions | 2026-01 | G | none | nav/sim |
| Socially-Aware Robot Navigation Using Large Language Models: System and Evaluation | 2026-01 | G | none | nav/sim |
| [CAUSALNAV: A Long-Term Embodied Navigation System for Autonomous Mobile Robots in Dynamic Outdoor Scenarios](https://arxiv.org/abs/2601.01872) | 2026-01 | G | none | nav/sim+real |
| NAIS: A Modular ROS 2 Framework for Real-Time Scene Graph Construction and Language-Guided Navigation | 2026-01 | G | none | nav/real |
| [Visual-Language-Guided Task Planning for Horticultural Robots](https://arxiv.org/abs/2601.11906) | 2026-01 | G | re-decide | nav/sim |
| [FARE: Fast-Slow Agentic Robotic Exploration](https://arxiv.org/abs/2601.14681) | 2026-01 | G | none | nav/sim |
| [IROS: A Dual-Process Architecture for Real-Time VLM-Based Indoor Navigation](https://arxiv.org/abs/2601.21506) | 2026-01 | G | re-decide | nav/real |
| [Multimodal Large Language Models for Real-Time Situated Reasoning](https://arxiv.org/abs/2602.01880) | 2026-02 | G | none | nav/real |
| Retrieval-Augmented Large Language Model Implementation for Context-Aware Robotic Task Execution | 2026-02 | G | none | nav/real |
| [MerNav: A Highly Generalizable Memory-Execute-Review Framework for Zero-Shot Object Goal Navigation](https://arxiv.org/abs/2602.05467) | 2026-02 | G | re-decide | nav/sim+real |
| [3DGSNav: Enhancing Vision-Language Model Reasoning for Object Navigation via Active 3D Gaussian Splatting](https://arxiv.org/abs/2602.12159) | 2026-02 | G | re-decide | nav/sim+real |
| [Global Commander and Local Operative: A Dual-Agent Framework for Scene Navigation](https://arxiv.org/abs/2602.18941) | 2026-02 | G | re-decide | nav/sim |
| Self-hosted multimodal large language models for speech-driven perception and navigation in construction robotics | 2026-03 | G | none | nav/real |
| [SFCo-Nav: Efficient Zero-Shot Visual Language Navigation via Collaboration of Slow LLM and Fast Attributed Graph Alignment](https://arxiv.org/abs/2603.01477) | 2026-03 | G | re-decide | nav/sim |
| [MA-CoNav: A Master-Slave Multi-Agent Framework with Hierarchical Collaboration and Dual-Level Reflection for Long-Horizon Embodied VLN](https://arxiv.org/abs/2603.03024) | 2026-03 | G | re-decide | nav/sim |
| [MRPoS: Mixed Reality-Based Robot Navigation Interface Using Spatial Pointing and Speech with Large Language Model](https://arxiv.org/abs/2603.13313) | 2026-03 | G | none | nav/real |
| [SysNav: Multi-Level Systematic Cooperation Enables Real-World, Cross-Embodiment Object Navigation](https://arxiv.org/abs/2603.06914) | 2026-03 | G | none | nav/real |
| [CMMR-VLN: Vision-and-Language Navigation via Continual Multimodal Memory Retrieval](https://arxiv.org/abs/2603.07997) | 2026-03 | G | re-decide | nav/sim+real |
| Flexible LLM-Based Voice Assistance for Mobile Robots | 2026-03 | G | none | nav/real |
| [LightZeroNav: Zero-Shot Vision Language Navigation in Continuous Environments Based on Lightweight VLMs](https://arxiv.org/abs/2603.16947) | 2026-03 | G | re-decide | nav/sim |
| Perception–Awareness–Decision: Socially‑Aware Robot Navigation and Interaction | 2026-03 | G | re-decide | nav/real |
| RBTLR: A Framework for Safe Social Robot Navigation in Novel Human-Centric Environments | 2026-03 | G | none | nav/sim |
| [Interpreting Context-Aware Human Preferences for Multi-Objective Robot Navigation](https://arxiv.org/abs/2603.17510) | 2026-03 | G | re-decide | nav/sim |
| [OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms](https://arxiv.org/abs/2603.17351) | 2026-03 | G | re-decide | nav/real |
| [FSUNav: A Cerebrum-Cerebellum Architecture for Fast, Safe, and Universal Zero-Shot Goal-Oriented Navigation](https://arxiv.org/abs/2604.03139) | 2026-04 | G | none | nav/sim+real |
| Map-Free Robot Navigation via Episodic Semantic Reasoning with Vision–Language and Large Language Models | 2026-04 | G | none | nav/real |
| A Generalised Robot Control Architecture with Large Language Model and Model Context Protocol | 2026-04 | G | re-decide | nav/sim |
| [Explore Like Humans: Autonomous Exploration with Online SG-Memo Construction for Embodied Agents](https://arxiv.org/abs/2604.19034) | 2026-04 | G | re-decide | nav/sim |
| Multimodal Human–Robot Interaction Using Human Pose Estimation and Local Large Language Models | 2026-04 | G | none | nav/real |
| [Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance](https://arxiv.org/abs/2604.26839) | 2026-04 | G | re-decide | nav/real |
| Constrained Behavior Tree Generation for Safe LLM-Driven Robot Navigation | 2026-05 | G | none | nav/sim |
| Design and deployment of an large language model-enhanced autonomous robot for intelligent operation and maintenance in data centers | 2026-05 | G | none | nav/real |
| USV-3.0: Cognitive maritime navigation through vision-language models, Human-in-the-Loop learning, and spatio-temporal memory | 2026-05 | G | re-decide | nav/real |
| [A Semantic Autonomy Framework for VLM-Integrated Indoor Mobile Robots: Hybrid Deterministic Reasoning and Cross-Robot Adaptive Memory](https://arxiv.org/abs/2605.02525) | 2026-05 | G | none | nav/real |
| Integrating Large Language Models with ROS 2 for Waypoint-Based Mobile Robot Navigation | 2026-05 | G | none | nav/sim |
| Vision Language Action for TurtleBot Mobile Robot Path Planning | 2026-05 | G | none | nav/real |
| HOSG-Nav: Hierarchical Open-Vocabulary Semantic Graph Navigation for Language-Guided Global Planning in 3D Gaussian Scenes | 2026-05 | G | none | nav/sim+real |
| Agile assistive hospital robot for suboptimal Task execution in dynamic environments | 2026-05 | G | re-decide | nav/real |
| [Bridging the 2D-3D Gap: A Hierarchical Semantic-Geometric Map for Vision Language Navigation](https://arxiv.org/abs/2606.00095) | 2026-05 | G | re-decide | nav/sim |
| [Uni-LaViRA: Language-Vision-Robot Actions Translation for Unified Embodied Navigation](https://arxiv.org/abs/2605.27582) | 2026-05 | G | re-decide | nav/sim+real |
| Design and Implementation of a Natural Language-Based Autonomous Robot Control System Using Large Language Models | 2026-05 | G | none | nav/real |
| Déjà Vu: Unlocking Transparent Action Reasoning for Object-Goal Navigation via Large Language Models | 2026-06 | G | re-decide | nav/sim |
| Multimodal Navigation Assistance for Older Adults: Combining Generative AI and Augmented Reality in a Robotic Walker | 2026-06 | G | none | nav/real |
| Navigation for Unmanned Ground Vehicles in Low-Altitude Logistics: A Hierarchical Visual Language Navigation Approach `sim2real` | 2026-06 | G | none | nav/sim+real |
| SenseNav: A Hybrid LiDAR-to-Language Navigation Framework for Autonomous Guided Vehicles | 2026-06 | G | none | nav/sim+real |
| [EvoMemNav: Efficient Self-Evolving Fine-Grained Memory for Zero-Shot Embodied Navigation](https://arxiv.org/abs/2606.03509) | 2026-06 | G | re-decide | nav/sim |
| [SpaceVLN: A Zero-Shot Vision-and-Language Navigation Agent with Online Spatial Cognitive Memory and Reasoning](https://arxiv.org/abs/2606.08992) | 2026-06 | G | re-decide | nav/sim |
| [Foresight: Iterative Reasoning About Clues that Matter for Navigation](https://arxiv.org/abs/2606.12550) | 2026-06 | C | none | nav/sim+real |
| Linguistically optimized operational teaming (LOOT): a natural language command and control framework for unmanned ground vehicles using real-time aerial drone imagery | 2026-06 | G | none | nav/real |
| Autonomous Navigation AGV Using Vision-Language Models for Natural Language Guided Indoor Navigation | 2026-06 | G | none | nav/real |
| [EvolveNav: Proactive Preflection and Self-Evolving Memory for Zero-Shot Object Goal Navigation](https://arxiv.org/abs/2606.18235) | 2026-06 | G | re-decide | nav/sim |
| [RAVEN: Long-Horizon Reasoning & Navigation with a Visuo-Spatio-Temporal Memory](https://arxiv.org/abs/2606.25206) | 2026-06 | G | re-decide | nav/real |
| [SAGE-Nav: Leveraging LLM Planning and Alignment Fusion for Hierarchical Scene Graph-Guided Navigation](https://arxiv.org/abs/2606.25497) | 2026-06 | G | re-decide | nav/sim |
| Brain-inspired spatial intelligence for embodied agents | 2026-06 | G | none | nav/sim+real |
| [HUMEMBR: Learning Human Routines for Predictive Embodied Navigation](https://arxiv.org/abs/2606.30404) | 2026-06 | G | none | nav/real |
| [ViTL: Temporal Logic-Guided Zero-Shot Natural Language Navigation via Vision-Language Models](https://arxiv.org/abs/2606.30696) | 2026-06 | G | authored | nav/sim |
| Agentic Llm-Driven Human-Robot Interaction | 2026-07 | G | re-decide | nav/sim |
| [Multimodal-Language-Model–Driven Interaction and Companionship for Service Robots in Elderly-Care Facilities](https://arxiv.org/abs/2608.21387) | 2026-07 | G | none | nav/real |
| Safety-Aware Optimal Control With Language-Guided Online Parameter Adjustment via Large Language Models | 2026-07 | G | authored | nav/sim+real |
| Standards-Aligned Ethical Gating and Decision Telemetry for LLM-Assisted Mobile Robot Navigation: A Simulation Study | 2026-07 | G | none | nav/sim |
| [Offline Vision-Language Navigation with Geometric Goal Localization for Outdoor Environments](https://arxiv.org/abs/2607.22226) | 2026-07 | G | none | nav/real |
| Enabling reliable navigation for lightweight VLMs via a Semantically-Gated Visual servoing framework | 2026-08 | G | re-decide | nav/real |
| IRAZON: Iterative ReAct With LLMs for Adaptive Zero-Shot Object Goal Navigation | 2026-08 | G | re-decide | nav/sim |
| RO-VLMap: Real-Time Occupancy-Aware Visual Language Mapping for Robust Robot Navigation | 2026-08 | G | none | nav/sim |
| Robust Autonomous Navigation in Dynamic Environments with a Modular Multi-Agent AI Architecture for Mobile Robots | 2026-08 | G | none | nav/real |
| Speak2move: a Vision-Language-Based Semantic Mapping Framework for Autonomous Navigation in Assistive Robots | 2026-08 | G | none | nav/real |
| [Hierarchical Fast-Slow ReAct Agent for Zero-Shot Object-Goal Navigation](https://arxiv.org/abs/2608.09816) | 2026-08 | G | re-decide | nav/sim |
| [SAIN: Structure-Aware Interactive Navigation with Active Dialogue Grounding for Mobile Robot](https://arxiv.org/abs/2608.09196) | 2026-08 | G | re-decide | nav/sim |
| LLM-Based Semantic Navigation on a Low-Cost ROS Mobile Robot: A Hybrid Edge–Cloud Architecture | 2026-08 | G | none | nav/real |
| [Embodied-Navigator: Point, Think, Memorize, and Align for Efficient Navigation](https://arxiv.org/abs/2608.17512) | 2026-08 | C | re-decide | nav/sim+real |
| [OptiSight: Bridging Semantic Reasoning and Geometric Control for Embodied Navigation](https://arxiv.org/abs/2608.23354) | 2026-08 | G | none | nav/sim |
| Open-Vocabulary, Context-Aware Robot Navigation on Construction Sites: Integrating LLM-Driven Value Map Composition with Hierarchical Scene Graphs | 2026-08 | G | none | nav/sim+real |
| Hybrid Zero-Shot Interactive Navigation with LLMs: Path Planning Under Dual Constraints of Speech and Environment | 2026-08 | G | none | nav/real |
| [CGFM-Nav: Cognitive Graph-Field Memory for Semantic-Guided Lifelong Multimodal Embodied Navigation](https://arxiv.org/abs/2608.29114) | 2026-08 | G | re-decide | nav/sim |
| [Scaffolding Foundation Models into Physical-World Agents Pushes the Frontier of Long-Horizon Navigation](https://arxiv.org/abs/2608.30396) | 2026-08 | G | re-decide | nav/sim |
| [One MLLM, One Call: Efficient Zero-Shot Vision-and-Language Navigation via Spatial-Aware Waypoints](https://arxiv.org/abs/2609.06476) | 2026-09 | G | none | nav/sim |
| [AnchorVLN: Geometry-Anchored Vision-Language Grounding Reasoning for Open-Vocabulary Navigation](https://arxiv.org/abs/2609.12285) | 2026-09 | G | re-decide | nav/sim+real |
| [Bridging Thought and Action: Taming Long-Horizon Instability in Open-Source LLM Agents with a MetaTool-Enhanced ROS Framework](https://arxiv.org/abs/2609.13335) | 2026-09 | G | re-decide | nav/real |
| [Multi-Task Visual Perception Network with LLM Conditioning for Autonomous Navigation](https://arxiv.org/abs/2609.14297) | 2026-09 | G | none | nav/sim+real |
| [NavPatch: Evidence-Guided Object-Level Costmap Correction with Vision-Language Models](https://arxiv.org/abs/2609.14543) | 2026-09 | G | none | nav/real |
| [Navi-Agent: Unlocalized Monocular Navigation Agent](https://arxiv.org/abs/2609.20388) | 2026-09 | G | re-decide | nav/sim |
| [Deploying Foundation Models for Embodied Navigation](https://arxiv.org/abs/2609.25666) | 2026-09 | G | re-decide | nav/sim+real |
| [Hierarchical Floorplan-Guided Vision-Language Exploration for Embodied Question Answering](https://arxiv.org/abs/2609.26360) | 2026-09 | G | re-decide | nav/sim |
| [SparseNav: Instruction-conditioned Sparse Semantic Perception for Training-Free Vision-Language Navigation](https://arxiv.org/abs/2609.26408) | 2026-09 | G | re-decide | nav/sim |
| [Spatial and Semantic Reasoning for LLM-Driven Robot Navigation via MCP](https://arxiv.org/abs/2609.27340) | 2026-09 | G | re-decide | nav/sim |
| [Actively Resolving Contextual Uncertainty for Underspecified Tasks in Natural Language](https://arxiv.org/abs/2609.30428) | 2026-09 | G | re-decide | nav/real |
| [Nutri-ATLAS: Embodied Agent for Tabulated Lookup and Assistance for Smarter nutrition](https://arxiv.org/abs/2609.32803) | 2026-09 | G | none | nav/real |
| [RECAST: Recasting Vision-Language Semantics into an Actionable Cost Map for Robot Navigation](https://arxiv.org/abs/2609.32595) | 2026-09 | G | none | nav/sim+real |
| [NavHarness: Towards Lifelong Embodied Navigation](https://arxiv.org/abs/2609.34276) | 2026-09 | G | re-decide | nav/sim |
| [NavHarness: Adaptive Goals for Agentic Vision-Language Navigation](https://arxiv.org/abs/2609.39915) | 2026-09 | G | re-decide | nav/sim |
| [PreAct-Nav: Agentic Reasoning Before Action for Urban Navigation](https://arxiv.org/abs/2610.04916) | 2026-10 | G | re-decide | nav/sim |
| Noise-Invariant Agentic Human-Robot Interaction GenAI System Using a Dual-Encoder Contrastive ASR Architecture and VLMs for Robot Control and Navigation in Acoustically Challenging Jobsites | 2026-11 | G | none | nav/real |

</details>

<details><summary><b>Supervisor</b> (39)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| Anomaly Management in Multi-Robot Coordination: Detection and Handling Framework for Self-Driving Laboratories | 2026 | G | re-decide | multi-robot/sim+real |
| IEI-TIA: Industrial Embodied Intelligence Trustworthy Interpretable Agent for Robotic Long-Horizon and Repetitive Tasks | 2026 | C | re-decide | manip/sim+real |
| [Goal-Oriented Communication for Fast and Robust Robotic Fault Detection and Recovery](https://arxiv.org/abs/2601.18765) | 2026-01 | C | none | manip/sim+real |
| Robust Task Planning via Failure Detection Using Scene Graph From Multi-View Images | 2026-02 | G | re-decide | manip/sim+real |
| Semantic–Physical Sensor Fusion for Safe Physical Human–Robot Interaction in Dual-Arm Rehabilitation | 2026-02 | C | none | manip/real |
| [Self-Evolutionary Replanning for Failure-Aware Motion Planning](https://arxiv.org/abs/2603.02772) | 2026-03 | G | re-decide | other/sim+real |
| [StageCraft: Execution Aware Mitigation of Distractor and Obstruction Failures in VLA Models](https://arxiv.org/abs/2603.20659) | 2026-03 | G | re-decide | manip/sim+real |
| [RoboHarness: A Memory-Augmented Policy Harness for Vision-Language-Action Model Robustness via In-Context Adaptation](https://arxiv.org/abs/2603.24060) | 2026-03 | G | re-decide | manip/sim |
| [Stop Wandering: Efficient Vision-Language Navigation via Metacognitive Reasoning](https://arxiv.org/abs/2604.02318) | 2026-04 | G | re-decide | nav/sim |
| LLM-Assisted Plan Execution for Robots in Dynamic Environments | 2026-04 | G | re-decide | nav/sim |
| [LLM-Guided Safety Agent for Edge Robotics with an ISO-Compliant Perception-Compute-Control Architecture](https://arxiv.org/abs/2604.20193) | 2026-04 | G | authored | manip/real |
| [Robot Planning and Situation Handling with Active Perception](https://arxiv.org/abs/2604.26988) | 2026-04 | G | re-decide | mobile-manip/sim+real |
| Failure Detection With Zero-Shot Error Correction in Robotic Manipulation | 2026-05 | G | re-decide | manip/sim+real |
| Grasp, Reason, Act: Tactile-Language Model for Zeroshot Sim2real Grasp Stability Prediction and Re-Grasping | 2026-05 | C | re-decide | manip/sim+real |
| SURF: Selective Uncertainty Reasoning for Robust Embodied Navigation | 2026-05 | G | none | nav/sim |
| Vision-Language-Guided UAV Navigation in Dynamic Coastline Environments | 2026-05 | G | none | aerial/sim |
| Vision-Guided Recovery: Enhancing Robotic Manipulation through Intelligent Failure Detection | 2026-05 | G | re-decide | manip/sim |
| [Make Your VLA More Robust Without More Data By Interleaving Motion Planning](https://arxiv.org/abs/2606.00985) | 2026-05 | G | re-decide | mobile-manip/sim+real |
| A Safe Hierarchical Framework for Embodied AI with Multi-Layer Safety Filtering and Recovery Mechanisms | 2026-06 | G | none | mobile-manip/sim |
| [Event-Adaptive Motion Planning with Distilled Vision-Language Model in Safety-Critical Situations](https://arxiv.org/abs/2606.25629) | 2026-06 | C | none | nav/sim+real |
| DS-LABRNav: Land-Air Bimodal Robot Navigation With Traversable Obstacles Base on Vision-Language Model | 2026-07 | G | none | other/real |
| VigiClaw: Action-Triggered State Verification for Robust Long-Horizon Robotic Manipulation | 2026-07 | G | re-decide | manip/sim |
| [Learning Robust Execution in Robotic Manipulation with Agentic Reinforcement Learning](https://arxiv.org/abs/2607.13818) | 2026-07 | C | re-decide | manip/sim |
| [From Sign Language Generation to Humanoid Execution: Vision-Language Guided Retargeting with Collision Mitigation](https://arxiv.org/abs/2607.17769) | 2026-07 | G | re-decide | humanoid/sim |
| [FORGE-plus: Force-Budgeted Recovery for Contact-Rich Assembly with a Frozen LLM Supervisor](https://arxiv.org/abs/2607.21227) | 2026-07 | G | re-decide | manip/sim |
| Predictive vision-language monitoring for proactive safety in robot task execution | 2026-08 | G | re-decide | mobile-manip/sim |
| [Agentic Harnesses: LLM-Driven Verification Layers for Robot Autonomy](https://arxiv.org/abs/2608.09857) | 2026-08 | G | none | other/sim |
| Integrating large language models for context-aware decision making in autonomous mobile robots | 2026-09 | G | none | nav/real |
| [Safe Task Planning with Long-Term Graph Memory for Embodied Agents](https://arxiv.org/abs/2609.08444) | 2026-09 | G | re-decide | mobile-manip/sim+real |
| [REVOLVE: An Automated Closed-Loop Framework for Evolving Robot Manipulation with Minimal Human Intervention](https://arxiv.org/abs/2609.14633) | 2026-09 | G | re-decide | manip/real |
| [Talk2Escape: Conversational Grounding for Vision-and-Language Navigation](https://arxiv.org/abs/2609.28296) | 2026-09 | G | re-decide | nav/sim |
| [Body-Grounded Replanning for Physically Adaptive Manipulation](https://arxiv.org/abs/2609.30024) | 2026-09 | G | re-decide | manip/sim+real |
| [SOR-Nav: Search or Relocate? Context-Gated Exploration and Cross-Region Relocation for Object Navigation](https://arxiv.org/abs/2609.34707) | 2026-09 | G | re-decide | nav/sim |
| [ProAct-VLM: Pre-Failure Vision-Language Task Replanning with Continuous Perception Feedback](https://arxiv.org/abs/2609.37681) | 2026-09 | G | re-decide | manip/real |
| [Risk-Aware Semantic Grounding for Trustworthy LLM-Based Robot Planning](https://arxiv.org/abs/2609.37554) | 2026-09 | G | none | nav/sim |
| [Spotter: Let the Embodied Model Lead, and the VLM Reflect for It](https://arxiv.org/abs/2609.36808) | 2026-09 | G | re-decide | manip/sim+real |
| [AVERT-VLN: Abstention-aware Visual Error Recovery and Training for Vision-and-Language Navigation](https://arxiv.org/abs/2609.39579) | 2026-09 | C | re-decide | nav/sim |
| [CORNAV: Construction-Aware Reasoning for Robot Navigation on Active Worksites](https://arxiv.org/abs/2610.03622) | 2026-10 | G | none | nav/sim+real |
| [AeroEval: Staged Program and Execution Validation for AI-Generated Drone Missions](https://arxiv.org/abs/2610.09764) | 2026-10 | G | re-decide | aerial/sim |

</details>

<details><summary><b>Teacher</b> (21)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [V-CAGE: Context-Aware Generation and Verification for Scalable Long-Horizon Embodied Tasks](https://arxiv.org/abs/2601.15164) | 2026-01 | G | re-decide | manip/sim |
| [Accelerating Robotic Reinforcement Learning with Agent Guidance](https://arxiv.org/abs/2602.11978) | 2026-02 | G | re-decide | manip/real |
| [Scene2Demo: Self-Evolving Embodied Data Generation via Object-Action Graph](https://arxiv.org/abs/2602.12065) `real2sim` | 2026-02 | G | re-decide | manip/sim |
| Gentle Manipulation of Long-Horizon Tasks Without Human Demonstrations | 2026-03 | G | re-decide | manip/sim+real |
| Teaching the Teacher: Live Foundation Model and Augmented Reality Feedback for Human-to-Robot Skill Transfer | 2026-03 | G | none | manip/real |
| [VLAMotor: Test-Guided Enhancement of Vision-Language-Action Models via Agent-BasedData Synthesis](https://arxiv.org/abs/2606.00053) | 2026-05 | G | none | manip/sim |
| [MotionDisco: Motion Discovery for Extreme Humanoid Loco-Manipulation](https://arxiv.org/abs/2606.06139) `sim2real` | 2026-06 | G | re-decide | humanoid/sim+real |
| [HATS: A Human-Agent Teleoperation System for Multi-Arm Data Collection](https://arxiv.org/abs/2606.16491) | 2026-06 | G | re-decide | manip/real |
| [InSight: Self-Guided Skill Acquisition via Steerable VLAs](https://arxiv.org/abs/2606.24884) | 2026-06 | G | re-decide | manip/real |
| [Zero2Skill: Bootstrapping Robot Skills through Autonomous Data Collection, Training, and Deployment](https://arxiv.org/abs/2607.14047) | 2026-07 | G | re-decide | manip/real |
| Prompted to Explore: Training-Time-Only LLM Proposals for Sample-Efficient Pushing Grasping Policies | 2026-08 | G | none | manip/sim |
| [EXIMO: VLM Guided Exploration of VLA Policies](https://arxiv.org/abs/2608.19891) | 2026-08 | G | re-decide | manip/sim+real |
| [SafeBranch: Branch-Pair Safety Alignment for Embodied Agents](https://arxiv.org/abs/2608.19729) | 2026-08 | C | re-decide | mobile-manip/sim |
| [MAGMA-GEN: Validated Recovery Supervision from Ambiguous Failures via Counterfactual Re-Execution](https://arxiv.org/abs/2609.20056) | 2026-09 | G | re-decide | manip/sim |
| [TANDEM: Task and Motion Planning with As-Needed Demonstrations for Efficient Vision-Language-Action Model Fine-tuning](https://arxiv.org/abs/2609.28314) | 2026-09 | G | authored | manip/sim+real |
| [RE-0: Verified Recursive Improvement of Embodied Code-as-Policy Agents through Local On-Policy Distillation](https://arxiv.org/abs/2609.32416) | 2026-09 | G | re-decide | manip/sim |
| [DexAgent: An Agentic Human2Sim2Robot Framework for Dexterous Manipulation with Self-Evolving Tool Library](https://arxiv.org/abs/2609.35318) `real2sim2real` | 2026-09 | G | re-decide | manip/sim+real |
| [Skill-Space Shooting for Autonomous Robot Policy Improvement](https://arxiv.org/abs/2609.38178) | 2026-09 | G | re-decide | manip/real |
| [EmbodiRSI: Recursive Self-Improvement for Data-Efficient Robot Adaptation](https://arxiv.org/abs/2609.38905) `real2sim2real` | 2026-09 | G | re-decide | manip/sim+real |
| [Recova: Agent-Guided Failure Recovery for Autonomous Robotic Manipulation](https://arxiv.org/abs/2610.01178) | 2026-10 | G | re-decide | manip/sim+real |
| [Recursive Self-Improvement of Visuomotor Policies through Local Recovery Supervision](https://arxiv.org/abs/2610.05151) | 2026-10 | G | re-decide | manip/sim |

</details>

<details><summary><b>Designer</b> (70)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| AgenticRL: Self-Refining Agentic Reinforcement Learning for Vision-Conditioned UAV Navigation | 2026 | G | re-decide | aerial/sim |
| [AllDayNav: Lifelong Navigation via Real-World Reinforcement Learning](https://arxiv.org/abs/2606.10927) | 2026 | G | none | nav/real |
| LLM-Based Dynamic Event-Triggered Communication for Multi-UAV Formation Control in Urban Environments | 2026 | G | re-decide | multi-robot/sim |
| Xmobot: Enabling Rapid Build-and-Train Robotics Education With Agentic AI | 2026 | G | re-decide | nav/sim+real |
| GAIA: Generating Task Instruction Aware Simulation Grounded in Real Contexts Using Vision-Language Models `real2sim` | 2026-01 | G | none | manip/sim |
| [LogicEnvGen: Task-Logic Driven Generation of Diverse Simulated Environments for Embodied AI](https://arxiv.org/abs/2601.13556) | 2026-01 | G | none | other/sim |
| [AGILE: Hand-object Interaction Reconstruction from Video via Agentic Generation](https://arxiv.org/abs/2602.04672) `real2sim` | 2026-02 | G | none | manip/sim |
| [RoboGene: Boosting VLA Pre-training via Diversity-Driven Agentic Framework for Real-World Task Generation](https://arxiv.org/abs/2602.16444) | 2026-02 | G | none | manip/real |
| [FATE: Closed-Loop Feasibility-Aware Task Generation with Active Repair for Physically Grounded Robotic Curricula](https://arxiv.org/abs/2603.01505) | 2026-03 | G | re-decide | manip/sim |
| [Tether: Autonomous Functional Play with Correspondence-Driven Trajectory Warping](https://arxiv.org/abs/2603.03278) | 2026-03 | G | re-decide | manip/real |
| [PRISM: Personalized Refinement of Imitation Skills for Manipulation via Human Instructions](https://arxiv.org/abs/2603.05574) | 2026-03 | G | re-decide | manip/sim |
| [Novelty Adaptation Through Hybrid Large Language Model (LLM)-Symbolic Planning and LLM-guided Reinforcement Learning](https://arxiv.org/abs/2603.11351) | 2026-03 | G | none | manip/sim |
| [RADAR: Closed-Loop Robotic Data Generation via Semantic Planning and Autonomous Causal Environment Reset](https://arxiv.org/abs/2603.11811) | 2026-03 | G | re-decide | manip/real |
| [Red-Teaming Vision-Language-Action Models via Quality Diversity Prompt Generation for Robust Robot Policies](https://arxiv.org/abs/2603.12510) | 2026-03 | G | none | manip/sim |
| Clarifying Constraints in Interactive Robot Learning with Language Feedback | 2026-03 | G | re-decide | manip/sim |
| [Swim2Real: VLM-Guided System Identification for Sim-to-Real Transfer](https://arxiv.org/abs/2603.20827) `real2sim2real` | 2026-03 | G | re-decide | other/sim+real |
| Constraint-Aware LLM Pipeline for EvoGym Environment Generation with Fitness-Guided Prompt Refinement | 2026-03 | G | re-decide | other/sim |
| [RoboPlayground: Democratizing Robotic Evaluation through Structured Physical Domains](https://arxiv.org/abs/2604.05226) | 2026-04 | G | none | manip/sim |
| [GenPHRI: Agentic Generative Simulation for Physical Human-Robot Interaction](https://arxiv.org/abs/2604.08664) `sim2real` | 2026-04 | G | re-decide | manip/sim+real |
| [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](https://arxiv.org/abs/2604.09036) | 2026-04 | G | re-decide | manip/sim |
| CAAI-ST: Constraint-Aware AI-Guided Seed Generation and Mutation for CPS-UAV System Testing | 2026-04 | G | re-decide | aerial/sim |
| [AffordSim: A Scalable Data Generator and Benchmark for Affordance-Aware Robotic Manipulation](https://arxiv.org/abs/2604.11674) `sim2real` | 2026-04 | G | none | manip/sim+real |
| [Chain of Uncertain Rewards with Large Language Models for Reinforcement Learning](https://arxiv.org/abs/2604.13504) | 2026-04 | G | re-decide | manip/sim |
| [EmbodiedClaw: Conversational Workflow Execution for Embodied AI Development](https://arxiv.org/abs/2604.13800) | 2026-04 | G | re-decide | other/sim |
| MotionVL: Vision-Language Supervision for Reinforcement Learning of Humanoid Motion `sim2real` | 2026-05 | G | re-decide | humanoid/sim+real |
| [Discovering Reinforcement Learning Interfaces with Large Language Models](https://arxiv.org/abs/2605.03408) | 2026-05 | G | re-decide | loco/sim |
| [SimWorld Studio: Automatic Environment Generation with Evolving Coding Agent for Embodied Agent Learning](https://arxiv.org/abs/2605.09423) | 2026-05 | G | re-decide | other/sim |
| [JODA: Composable Joint Dynamics for Articulated Objects](https://arxiv.org/abs/2605.09954) `real2sim` | 2026-05 | G | none | manip/sim |
| [SR-Platform: An Agentic Pipeline for Natural Language-Driven Robot Simulation Environment Synthesis](https://arxiv.org/abs/2605.14700) | 2026-05 | G | none | manip/sim |
| [FlyMirage: A Fully Automated Generation Pipeline for Diverse and Scalable UAV Flight Data via Generative World Model](https://arxiv.org/abs/2605.19600) | 2026-05 | G | none | aerial/sim |
| [Agentic-VLA: Efficient Online Adaptation for Vision-Language-Action Models](https://arxiv.org/abs/2605.22896) | 2026-05 | G | re-decide | manip/sim |
| A VLM-Driven High-Fidelity Domain Randomization Framework for Imitation Learning `real2sim` | 2026-06 | G | none | manip/sim |
| [CoDex: Learning Compositional Dexterous Functional Manipulation without Demonstrations](https://arxiv.org/abs/2606.31909) `sim2real` | 2026-06 | G | none | manip/sim+real |
| LLM-Supervised Semantic Reward Adaptation for Reinforcement Learning-Based Robot Locomotion | 2026-06 | G | re-decide | loco/sim |
| [AgenticRL: Agentic Reinforcement Learning with Self-Refinement for Complex UAV Navigation](https://arxiv.org/abs/2606.03963) | 2026-06 | G | re-decide | aerial/sim |
| [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630) | 2026-06 | G | none | manip/sim+real |
| [RoboLineage: Agent-Native Data Lifecycle Governance Across Robot Policy Iterations](https://arxiv.org/abs/2606.22142) | 2026-06 | G | re-decide | manip/real |
| [Causal Reward World Models: Zero-shot Reward Design for Automated Skill Generation](https://arxiv.org/abs/2606.23280) | 2026-06 | G | none | other/sim |
| [MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models](https://arxiv.org/abs/2606.24815) | 2026-06 | G | none | manip/sim |
| [Unleashing Infinite Motion: Scaling Expressive Quadrupedal Motion via Generative Video Priors](https://arxiv.org/abs/2606.28237) | 2026-06 | G | none | loco/real |
| [CoRe: Combined Rewards with Vision-Language Model Feedback for Preference-Aligned Reinforcement Learning](https://arxiv.org/abs/2607.01721) | 2026-07 | G | re-decide | other/sim |
| [PRISM: Personalized Robotic Dataset Generation via Image-based Scene and Motion Synthesis](https://arxiv.org/abs/2607.04880) `real2sim2real` | 2026-07 | G | none | manip/sim+real |
| [EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI](https://arxiv.org/abs/2607.07459) | 2026-07 | G | re-decide | manip/sim+real |
| [Prompt-Driven Exploration](https://arxiv.org/abs/2607.08837) | 2026-07 | G | re-decide | manip/sim |
| [LEACL: LLM-Enhanced Automatic Curriculum Learning for Reinforcement Learning in Long-Horizon Manipulation Tasks](https://arxiv.org/abs/2607.23515) | 2026-07 | G | none | manip/sim |
| [Beyond Placement and Articulation: Usage-Driven Code Scenes for Embodied Interaction](https://arxiv.org/abs/2608.18840) | 2026-08 | G | none | manip/sim |
| [MLREF: Efficient Module Reuse for Reward Design in Reinforcement Learning via Large Language Models](https://arxiv.org/abs/2608.18827) | 2026-08 | G | re-decide | other/sim |
| [NeoWorld-Pro: Programming Interactive Scenes from Monocular Images for Embodied Simulation](https://arxiv.org/abs/2608.24212) `real2sim` | 2026-08 | G | re-decide | manip/sim |
| [DREAM: Deployment-Time Demonstration Generation via Real-to-Sim for Scalable Policy Adaptation](https://arxiv.org/abs/2608.29078) `real2sim2real` | 2026-08 | G | authored | manip/sim+real |
| [Autonomously Acquiring Robot Manipulation Skills with Language-Driven Quality-Diversity](https://arxiv.org/abs/2608.30983) | 2026-08 | G | re-decide | manip/sim |
| [Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling](https://arxiv.org/abs/2608.30821) `real2sim` | 2026-08 | C | re-decide | manip/sim |
| [SUN: Agentic Robot Policy Learning with Persistent Task Programs](https://arxiv.org/abs/2608.31167) `sim2real` | 2026-08 | G | re-decide | manip/sim+real |
| [From LLM-Generated Specifications to Learned Quadruped Locomotion](https://arxiv.org/abs/2609.07111) | 2026-09 | G | none | loco/sim |
| [DISEIL: Demonstration Distillation for Sample-Efficient Imitation Learning](https://arxiv.org/abs/2609.08123) | 2026-09 | G | re-decide | manip/sim |
| [DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation](https://arxiv.org/abs/2609.18620) | 2026-09 | G | re-decide | manip/sim |
| [DiagGen: Agentic Generation of Deformable Assets with Sim-based Diagnostics for Robotic Simulation](https://arxiv.org/abs/2609.23103) `real2sim` | 2026-09 | G | re-decide | manip/sim |
| [ARSTAG: An Agentic Real2Sim2Real System for Task-Specific Robot Data Generation](https://arxiv.org/abs/2609.24563) `real2sim2real` | 2026-09 | G | re-decide | manip/sim+real |
| [MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation](https://arxiv.org/abs/2609.24145) `sim2real` | 2026-09 | G | re-decide | loco/sim+real |
| [SciHorizon-eLab: An Agentic Protocol-to-Task Compiler for Scalable Benchmarking of Scientific Embodied Agents](https://arxiv.org/abs/2609.30971) | 2026-09 | G | re-decide | manip/sim |
| [Beyond Scripted Search: Sample-Efficient Reward Discovery via Agentic Black-box Optimization](https://arxiv.org/abs/2609.32394) | 2026-09 | G | re-decide | other/sim |
| [Test-Time Spatial Reasoning for Robot Manipulation Using Generative Real-to-Sim](https://arxiv.org/abs/2609.33982) `real2sim2real` | 2026-09 | G | none | manip/sim+real |
| [F4R: Failure-Driven Recognition, Reconstruction, Refinement, and Redeployment for Continual Robot Self-Improvement](https://arxiv.org/abs/2609.35575) `real2sim2real` | 2026-09 | G | re-decide | manip/sim+real |
| [FACT: Fidelity-Aware Construction of Articulated Twins](https://arxiv.org/abs/2609.37067) `real2sim` | 2026-09 | G | re-decide | manip/sim |
| [Video2STL: Grounding VLM-Generated Temporal Specifications for Robot Learning](https://arxiv.org/abs/2609.37519) | 2026-09 | G | none | manip/sim |
| [Video2SwimFish: An Automated Pipeline for Reconstructing Controllable Fish Models and Biological Locomotion from Real Fish Videos](https://arxiv.org/abs/2609.38966) `real2sim` | 2026-09 | G | re-decide | other/sim |
| [Awomo-SimDataEngine: Agentic Simulation-ReadyWorld Generation](https://arxiv.org/abs/2610.02274) | 2026-10 | G | re-decide | manip/sim |
| [LiteReality-Agent: An Agentic System for Interactable 3D Indoor Scene Reconstruction](https://arxiv.org/abs/2610.01863) `real2sim` | 2026-10 | G | re-decide | other/sim |
| [EnvDreamer: Large-Scale Multimodal-to-Environment Generation for Embodied AI](https://arxiv.org/abs/2610.04301) `real2sim` | 2026-10 | G | re-decide | mobile-manip/sim |
| [Demo: Vision-Language Model-Guided Online Calibration of an Electromagnetic Digital Twin](https://arxiv.org/abs/2610.07081) `real2sim` | 2026-10 | G | re-decide | humanoid/real |
| [SMART: Zero-Shot Sim-to-Real Articulated Object Manipulation via Large-Scale Synthetic Pretraining](https://arxiv.org/abs/2610.07652) `sim2real` | 2026-10 | G | none | manip/sim+real |

</details>

<details><summary><b>Developer</b> (53)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [ModuLoop: Low-Level Code Generation Using Modular Synthesizer and Closed-Loop Debugger for Robotic Control](https://arxiv.org/abs/2606.03047) | 2025-12 | G | re-decide | manip/real |
| ECHO: A Natural Language-Enabled Cognitive Framework for Human-Centric Energy Optimization of Industrial Robots | 2026 | G | none | manip/real |
| LLM-Guided Adaptive Compensator: Bringing Adaptivity to Robotic Feedback Control With Large Language Model | 2026 | G | none | other/sim+real |
| RoboRSI: Stable, Efficient, and Reusable Robot Self-Evolution in Complex Real-World Environments | 2026 | G | re-decide | manip/sim+real |
| [Test-Driven Agentic Framework for Reliable Robot Controller](https://arxiv.org/abs/2603.00455) | 2026-02 | G | re-decide | nav/sim |
| [Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation](https://arxiv.org/abs/2603.04466) | 2026-03 | G | re-decide | manip/sim |
| [CABTO: Context-Aware Behavior Tree Grounding for Robot Manipulation](https://arxiv.org/abs/2603.16809) | 2026-03 | G | re-decide | manip/sim |
| [Agent-Driven Autonomous Reinforcement Learning Research: Iterative Policy Improvement for Quadruped Locomotion](https://arxiv.org/abs/2603.27416) | 2026-03 | G | re-decide | loco/sim |
| [Low-Burden LLM-Based Preference Learning: Personalizing Assistive Robots from Natural Language Feedback for Users with Paralysis](https://arxiv.org/abs/2604.01463) | 2026-04 | G | none | manip/sim |
| AI generated drone command and control station hosted in the sky | 2026-04 | G | none | aerial/real |
| [An LLM-Driven Closed-Loop Autonomous Learning Framework for Robots Facing Uncovered Tasks in Open Environments](https://arxiv.org/abs/2604.22199) | 2026-04 | G | none | manip/real |
| Hybrid LLM-Genetic Programming: Supervising and Generating Diverse Behavior Trees for Autonomous Robot Evolution | 2026-05 | G | re-decide | other/sim |
| [Nautilus: From One Prompt to Plug-and-Play Robot Learning](https://arxiv.org/abs/2605.11665) | 2026-05 | G | re-decide | manip/sim+real |
| [When Search Becomes Memory: Accelerating Robot Design Discovery with Self-Evolving Skills](https://arxiv.org/abs/2605.25832) | 2026-05 | G | re-decide | other/sim |
| [When are LLMs Sufficient Policy Optimizers for Sequential RL Tasks?](https://arxiv.org/abs/2605.30719) | 2026-05 | G | re-decide | manip/sim |
| [VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents](https://arxiv.org/abs/2606.05395) | 2026-06 | G | re-decide | manip/sim |
| [Self-Evolving Scientific Agent Designs Physically Reasoned White-Box Fluid Control](https://arxiv.org/abs/2606.08405) | 2026-06 | G | re-decide | other/sim |
| Neuro-symbolic Hierarchical Learning for Long-Horizon Robotic Tasks | 2026-06 | G | none | manip/sim |
| [Agentic AutoResearch forSpace Autonomy: An Auditable, LLM-Driven Research Agent for Aerospace Control Problems](https://arxiv.org/abs/2606.20394) | 2026-06 | G | re-decide | other/sim |
| [AI Training Manager: Bounded Closed-Loop Control of Adaptive Training Recipes](https://arxiv.org/abs/2606.29871) | 2026-06 | G | re-decide | manip/sim |
| [Automating the Design of Embodied AgentArchitectures](https://arxiv.org/abs/2606.30111) | 2026-06 | G | re-decide | mobile-manip/sim |
| Agents Trainer: Automatically Training Multi-Agent Reinforcement Learning Models for Drone Swarm Using Language Model-Based Agents | 2026-07 | G | re-decide | aerial/sim |
| Automated UAV Controller Synthesis via LLM-Generated Control Logic and Particle Swarm Optimization `sim2real` | 2026-07 | G | re-decide | aerial/sim+real |
| [GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks](https://arxiv.org/abs/2607.05369) `real2sim2real` | 2026-07 | G | re-decide | manip/sim+real |
| LLMigrate: Large Language Models as Migration Controllers in Island-Based Evolutionary Design of Soft Robots | 2026-07 | G | re-decide | other/sim |
| Mission-Driven UAV Conceptual Design Using LLM and RAG with Preliminary CFD and Closed-Loop Feasibility Assessment | 2026-07 | G | none | aerial/sim |
| [MEMENTO: Memory-Guided Memetic Code-as-Policy Evolution](https://arxiv.org/abs/2607.22832) | 2026-07 | G | re-decide | manip/sim |
| [A Few Words Go a Long Way: Language Guided Robot Policy Synthesis](https://arxiv.org/abs/2607.23784) | 2026-07 | G | re-decide | manip/sim+real |
| [An AI Scientist that Doesn't Drift: Taste, Structure, and Falsifiable Findings in a Quadruped Navigation Research Loop](https://arxiv.org/abs/2608.07542) | 2026-07 | G | re-decide | loco/sim |
| [You Don't Need To Stay in The Loop: An Agentic Robotics Loop for Robot-Policy Improvement](https://arxiv.org/abs/2608.07555) | 2026-08 | G | re-decide | manip/sim |
| [RoboReact: Agentic Skill Distillation from Generated Egocentric Videos for Generalizable Whole-Body Manipulation](https://arxiv.org/abs/2608.03387) | 2026-08 | G | re-decide | humanoid/sim+real |
| [Skills in Weights, Memory in Code: Hybrid Learning for Memory-Dependent Robot Manipulation](https://arxiv.org/abs/2608.09410) | 2026-08 | G | re-decide | manip/sim+real |
| [Retrieval-grounded robot program generation and simulation-based correction via Model Context Protocol](https://arxiv.org/abs/2608.21417) | 2026-08 | G | re-decide | manip/sim |
| [Revisiting the"Push-T"Robot Manipulation Task with Agentic Robotics](https://arxiv.org/abs/2608.18227) | 2026-08 | G | re-decide | manip/sim |
| [Learning and Transferring Closed-Loop Robot Software](https://arxiv.org/abs/2609.19906) | 2026-09 | G | re-decide | manip/sim |
| [LEMCA: LLM-Guided Synthesis of Efficient Mode-Switching Control Architectures](https://arxiv.org/abs/2609.21319) | 2026-09 | G | re-decide | other/sim |
| [From Ideal Motion to Flight-Executable Communications: LLM-Evolved Multi-UAV Deployment for Cell-Free Massive MIMO](https://arxiv.org/abs/2609.23992) | 2026-09 | G | re-decide | multi-robot/sim |
| [What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery](https://arxiv.org/abs/2609.31760) | 2026-09 | G | re-decide | manip/sim |
| [Coding Agents for Generalized Task and Motion Planning Problems](https://arxiv.org/abs/2609.30233) | 2026-09 | G | re-decide | manip/sim |
| [HarnessPAI: An Evolving Harness for Physical AI](https://arxiv.org/abs/2609.29166) | 2026-09 | G | re-decide | manip/sim+real |
| [HuGo: LLMs as Whole-Body Policy Code Designers for Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.30594) | 2026-09 | G | re-decide | humanoid/sim |
| [Privacy-Preserving Prompted Policy Search for Robotic Control](https://arxiv.org/abs/2609.30554) | 2026-09 | G | re-decide | other/sim |
| [RACaP: Agentic Reasoning, Acting, and Coding as Policies for Evolvable Robot Learning](https://arxiv.org/abs/2609.29394) | 2026-09 | G | re-decide | manip/sim |
| [RAPID: Robot Agentic Programming from Demonstrations](https://arxiv.org/abs/2609.30249) | 2026-09 | G | re-decide | manip/sim+real |
| [Large Language Models for Model-Based Robot Design](https://arxiv.org/abs/2609.33423) | 2026-09 | G | none | other/sim |
| [Agent Priors-guided Policy Learning](https://arxiv.org/abs/2609.35690) | 2026-09 | G | none | manip/sim+real |
| [Encore: Few-Shot Agentic Discovery of Manipulation Strategies](https://arxiv.org/abs/2609.37359) | 2026-09 | G | re-decide | manip/sim |
| [DynaHarness: A Dynamic Physical Harness for Self-Evolving Robot Agents](https://arxiv.org/abs/2609.40306) | 2026-09 | G | re-decide | manip/sim+real |
| [Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents](https://arxiv.org/abs/2609.39304) | 2026-09 | G | re-decide | manip/sim |
| [Iterative Policy Refinement through Semantic Rollout Analysis](https://arxiv.org/abs/2610.01652) | 2026-10 | G | re-decide | manip/sim |
| [EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432) | 2026-10 | G | re-decide | mobile-manip/sim |
| [PEARS: Physical-Prior-Guided Efficient Adaptation via Failure Reasoning and Diffusion Steering for Tactile Manipulation](https://arxiv.org/abs/2610.08784) | 2026-10 | G | re-decide | manip/real |
| [EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution](https://arxiv.org/abs/2610.10498) | 2026-10 | G | re-decide | manip/sim+real |

</details>


## More papers from 2022–2025

902 further papers from 2022–2025 that meet the definition (judged by a verification pass; open-loop ones have *Loop* = none) but are not in the curated tables above. Tags come from the judging pass and are not hand-checked; generated by `scripts/build_extended.py`.

<details><summary><b>Controller · Orchestrators</b> (448)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| D O A S I C AN , N OT A S I S AY : G ROUNDING L ANGUAGE IN R OBOTIC A FFORDANCES | 2022 | G | re-decide | mobile-manip/real |
| [Open-vocabulary Queryable Scene Representations for Real World Planning](https://arxiv.org/abs/2209.09874) | 2022-09 | G | none | mobile-manip/real |
| [CAPE: Corrective Actions from Precondition Errors using Large Language Models](https://arxiv.org/abs/2211.09935) | 2022-11 | G | re-decide | mobile-manip/sim+real |
| From Words to Flight: Integrating OpenAI ChatGPT with PX4/Gazebo for Natural Language-Based Drone Control | 2023 | G | none | aerial/sim |
| [SOCRATES: Text-based Human Search and Approach using a Robot Dog](https://arxiv.org/abs/2302.05324) | 2023-02 | G | none | loco/sim+real |
| [Grounded Decoding: Guiding Text Generation with Grounded Models for Embodied Agents](https://arxiv.org/abs/2303.00855) | 2023-03 | G | re-decide | mobile-manip/sim+real |
| A Voice-Controlled Motion Reproduction Using Large Language Models for Polishing Robots | 2023-03 | G | none | manip/real |
| [Chat with the Environment: Interactive Multimodal Perception Using Large Language Models](https://arxiv.org/abs/2303.08268) | 2023-03 | G | re-decide | manip/real |
| [ERRA: An Embodied Representation and Reasoning Architecture for Long-Horizon Language-Conditioned Manipulation Tasks](https://arxiv.org/abs/2304.02251) | 2023-04 | G | re-decide | manip/sim+real |
| [ChatGPT Empowered Long-Step Robot Control in Various Environments: A Case Application](https://arxiv.org/abs/2304.03893) | 2023-04 | G | none | manip/sim |
| [Robot-Enabled Construction Assembly with Automated Sequence Planning based on ChatGPT: RoboGPT](https://arxiv.org/abs/2304.11018) | 2023-04 | G | none | manip/sim+real |
| [Improved Trust in Human-Robot Collaboration with ChatGPT](https://arxiv.org/abs/2304.12529) | 2023-04 | G | none | manip/real |
| [Multimodal Grounding for Embodied AI via Augmented Reality Headsets for Natural Language Driven Task Planning](https://arxiv.org/abs/2304.13676) | 2023-04 | G | none | other/real |
| [Language Models Meet World Models: Embodied Experiences Enhance Language Models](https://arxiv.org/abs/2305.10626) | 2023-05 | C | none | other/sim |
| [AlphaBlock: Embodied Finetuning for Vision-Language Reasoning in Robot Manipulation](https://arxiv.org/abs/2305.18898) | 2023-05 | C | re-decide | manip/sim+real |
| [Toward Grounded Commonsense Reasoning](https://arxiv.org/abs/2306.08651) | 2023-06 | G | re-decide | manip/real |
| [CLARA: Classifying and Disambiguating User Commands for Reliable Interactive Robotic Agents](https://arxiv.org/abs/2306.10376) | 2023-06 | G | none | manip/sim |
| Grounded Decoding: Guiding Text Generation with Grounded Models for Robot Control | 2023-07 | G | re-decide | mobile-manip/sim+real |
| [Embodied Task Planning with Large Language Models](https://arxiv.org/abs/2307.01848) | 2023-07 | C | none | mobile-manip/sim |
| [Towards A Unified Agent with Foundation Models](https://arxiv.org/abs/2307.09668) | 2023-07 | G | none | manip/sim |
| Grounding Language for Robotic Manipulation via Skill Library | 2023-07 | G | none | manip/sim |
| [Foundation Model based Open Vocabulary Task Planning and Executive System for General Purpose Service Robots](https://arxiv.org/abs/2308.03357) | 2023-08 | G | none | mobile-manip/real |
| [SayCanPay: Heuristic Planning with Large Language Models using Learnable Domain Knowledge](https://arxiv.org/abs/2308.12682) | 2023-08 | G | none | manip/sim |
| [ISR-LLM: Iterative Self-Refined Large Language Model for Long-Horizon Sequential Task Planning](https://arxiv.org/abs/2308.13724) | 2023-08 | G | none | manip/sim |
| [LLM-Based Human-Robot Collaboration Framework for Manipulation Tasks](https://arxiv.org/abs/2308.14972) | 2023-08 | G | none | manip/real |
| [WALL-E: Embodied Robotic WAiter Load Lifting with Large Language Model](https://arxiv.org/abs/2308.15962) | 2023-08 | G | none | manip/real |
| [Gesture-Informed Robot Assistance via Foundation Models](https://arxiv.org/abs/2309.02721) | 2023-09 | G | none | manip/real |
| [From Cooking Recipes to Robot Task Trees – Improving Planning Correctness and Task Efficiency by Leveraging LLMs with a Knowledge Network](https://arxiv.org/abs/2309.09181) | 2023-09 | C | none | manip/sim |
| [Conformal Temporal Logic Planning using Large Language Models](https://arxiv.org/abs/2309.10092) | 2023-09 | G | none | mobile-manip/sim+real |
| [Prompt, Plan, Perform: LLM-based Humanoid Control via Quantized Imitation Learning](https://arxiv.org/abs/2309.11359) | 2023-09 | G | none | humanoid/sim |
| [HiCRISP: An LLM-Based Hierarchical Closed-Loop Robotic Intelligent Self-Correction Planner](https://arxiv.org/abs/2309.12089) | 2023-09 | G | re-decide | manip/sim+real |
| [Self-Recovery Prompting: Promptable General Purpose Service Robot System with Foundation Models and Self-Recovery](https://arxiv.org/abs/2309.14425) | 2023-09 | G | re-decide | mobile-manip/sim+real |
| [Integration of Large Language Models within Cognitive Architectures for Autonomous Robots](https://arxiv.org/abs/2309.14945) | 2023-09 | G | none | mobile-manip/sim |
| [OceanChat: Piloting Autonomous Underwater Vehicles in Natural Language](https://arxiv.org/abs/2309.16052) | 2023-09 | G | none | other/sim |
| [QwenGrasp: A Usage of Large Vision-Language Model for Target-Oriented Grasping](https://arxiv.org/abs/2309.16426) | 2023-09 | G | none | manip/real |
| [Dobby: A Conversational Service Robot Driven by GPT-4](https://arxiv.org/abs/2310.06303) | 2023-10 | G | re-decide | social/real |
| [CoPAL: Corrective Planning of Robot Actions with Large Language Models](https://arxiv.org/abs/2310.07263) | 2023-10 | G | re-decide | manip/sim+real |
| [Hierarchical Large Language Models in Cloud-Edge-End Architecture for Heterogeneous Robot Cluster Control](https://arxiv.org/abs/2402.03703) | 2023-10 | G | none | multi-robot/real |
| [Interactive Task Planning with Language Models](https://arxiv.org/abs/2310.10645) | 2023-10 | G | re-decide | manip/real |
| [Conditionally Combining Robot Skills using Large Language Models](https://arxiv.org/abs/2310.17019) | 2023-10 | G | none | manip/sim |
| Large language models for chemistry robotics | 2023-10 | G | none | manip/sim+real |
| [REAL: Resilience and Adaptation using Large Language Models on Autonomous Aerial Robots](https://arxiv.org/abs/2311.01403) | 2023-11 | G | re-decide | aerial/real |
| [LLM Augmented Hierarchical Agents](https://arxiv.org/abs/2311.05596) | 2023-11 | G | none | other/real |
| [GPT-4V(ision) for Robotics: Multimodal Task Planning From Human Demonstration](https://arxiv.org/abs/2311.12015) | 2023-11 | G | none | manip/real |
| [Agent as Cerebrum, Controller as Cerebellum: Implementing an Embodied LMM-based Agent on Drones](https://arxiv.org/abs/2311.15033) | 2023-11 | G | re-decide | aerial/sim+real |
| [LLM-State: Open World State Representation for Long-horizon Task Planning with Large Language Model](https://arxiv.org/abs/2311.17406) | 2023-11 | G | re-decide | manip/sim+real |
| [Interactive Planning Using Large Language Models for Partially Observable Robotic Tasks](https://arxiv.org/abs/2312.06876) | 2023-12 | G | re-decide | manip/sim+real |
| [ThinkBot: Embodied Instruction Following with Thought Chain Reasoning](https://arxiv.org/abs/2312.07062) | 2023-12 | G | none | mobile-manip/sim |
| [DriveMLM: aligning multi-modal large language models with behavioral planning states for autonomous driving](https://arxiv.org/abs/2312.09245) | 2023-12 | C | none | driving/sim |
| [LLM-MARS: Large Language Model for Behavior Tree Generation and NLP-enhanced Dialogue in Multi-Agent Robot Systems](https://arxiv.org/abs/2312.09348) | 2023-12 | C | none | multi-robot/real |
| Don't Let Your Robot be Harmful: Responsible Robotic Manipulation | 2024 | G | none | manip/sim+real |
| Experimenting with Planning and Reasoning in Ad Hoc Teamwork Environments with Large Language Models | 2024 | G | none | other/sim |
| Introspective Planning: Guiding Language-Enabled Agents to Refine Their Own Uncertainty | 2024 | G | none | mobile-manip/sim |
| [MOSAIC: Modular Foundation Models for Assistive and Interactive Cooking](https://arxiv.org/abs/2402.18796) | 2024 | G | re-decide | multi-robot/real |
| REBEL: Rule-based and Experience-enhanced Learning with LLMs for Initial Task Allocation in Multi-Human Multi-Robot Teams | 2024 | G | none | multi-robot/sim |
| Robi Butler: Remote Multimodal Interactions with Household Robot Assistant | 2024 | G | re-decide | mobile-manip/real |
| Safe Task Planning for Language-Instructed Multi-Robot Systems using Conformal Prediction | 2024 | G | none | multi-robot/sim |
| [RePLan: Robotic Replanning with Perception and Language Models](https://arxiv.org/abs/2401.04157) | 2024-01 | G | re-decide | manip/sim |
| [Consolidating Trees of Robotic Plans Generated Using Large Language Models to Improve Reliability](https://arxiv.org/abs/2401.07868) | 2024-01 | G | none | other/sim |
| [CognitiveDog: Large Multimodal Model Based System to Translate Vision and Language into Action of Quadruped Robot](https://arxiv.org/abs/2401.09388) | 2024-01 | C | none | mobile-manip/real |
| [LaMI: Large Language Models for Multi-Modal Human-Robot Interaction](https://arxiv.org/abs/2401.15174) | 2024-01 | G | re-decide | social/real |
| [CognitiveOS: Large Multimodal Model Based System to Endow Any Type of Robot with Generative AI](https://arxiv.org/abs/2401.16205) | 2024-01 | G | none | other/real |
| [MEIA: Multimodal Embodied Perception and Interaction in Unknown Environments](https://arxiv.org/abs/2402.00290) | 2024-02 | G | none | mobile-manip/sim |
| [Introspective Planning: Aligning Robots' Uncertainty with Inherent Task Ambiguity](https://arxiv.org/abs/2402.06529) | 2024-02 | G | none | mobile-manip/sim |
| [SemTra: A Semantic Skill Translator for Cross-Domain Zero-Shot Policy Adaptation](https://arxiv.org/abs/2402.07418) | 2024-02 | C | none | manip/sim |
| [Grounding LLMs For Robot Task Planning Using Closed-loop State Feedback](https://arxiv.org/abs/2402.08546) | 2024-02 | G | re-decide | manip/sim+real |
| [AutoGPT+P: Affordance-based Task Planning with Large Language Models](https://arxiv.org/abs/2402.10778) | 2024-02 | G | re-decide | humanoid/real |
| Development of A SayCan-based Task Planning System Capable of Handling Abstract Nouns | 2024-02 | G | re-decide | mobile-manip/real |
| [We Choose to Go to Space: Agent-driven Human and Multi-Robot Collaboration in Microgravity](https://arxiv.org/abs/2402.14299) | 2024-02 | G | re-decide | multi-robot/sim |
| [Probabilistically Correct Language-Based Multi-Robot Planning Using Conformal Prediction](https://arxiv.org/abs/2402.15368) | 2024-02 | G | none | multi-robot/sim |
| [RoboEXP: Action-Conditioned Scene Graph via Interactive Exploration for Robotic Manipulation](https://arxiv.org/abs/2402.15487) | 2024-02 | G | re-decide | manip/real |
| [Conversational Language Models for Human-in-the-Loop Multi-Robot Coordination](https://arxiv.org/abs/2402.19166) | 2024-02 | G | re-decide | multi-robot/real |
| Enhancing Robot Task Planning and Execution through Multi-Layer Large Language Models | 2024-03 | G | none | manip/real |
| [Language-Grounded Dynamic Scene Graphs for Interactive Object Search With Mobile Manipulation](https://arxiv.org/abs/2403.08605) | 2024-03 | G | re-decide | mobile-manip/sim+real |
| [FlexiFly: Interfacing the Physical World with Foundation Models Empowered by Reconfigurable Drone Systems](https://arxiv.org/abs/2403.12853) | 2024-03 | G | none | aerial/real |
| [LBAP: Improved Uncertainty Alignment of LLM Planners using Bayesian Inference](https://arxiv.org/abs/2403.13198) | 2024-03 | G | none | manip/sim+real |
| [To Help or Not to Help: LLM-based Attentive Support for Human-Robot Group Interactions](https://arxiv.org/abs/2403.12533) | 2024-03 | G | re-decide | manip/real |
| [OceanPlan: Hierarchical Planning and Replanning for Natural Language AUV Piloting in Large-scale Unexplored Ocean Environments](https://arxiv.org/abs/2403.15369) | 2024-03 | G | re-decide | other/sim |
| [A Robotic Skill Learning System Built Upon Diffusion Policies and Foundation Models](https://arxiv.org/abs/2403.16730) | 2024-03 | G | none | manip/sim+real |
| ATOM: Leveraging Large Language Models for Adaptive Task Object Motion Strategies in Object Rearrangement for Service Robotics | 2024-03 | G | none | manip/sim+real |
| [ITCMA: A Generative Agent Based on a Computational Consciousness Structure](https://arxiv.org/abs/2403.20097) | 2024-03 | G | re-decide | loco/real |
| [Large Language Models for Orchestrating Bimanual Robots](https://arxiv.org/abs/2404.02018) | 2024-04 | G | none | humanoid/sim |
| [ZeroCAP: Zero-Shot Multi-Robot Context Aware Pattern Formation via Large Language Models](https://arxiv.org/abs/2404.02318) | 2024-04 | G | none | multi-robot/sim+real |
| [DELTA: Decomposed Efficient Long-Term Robot Task Planning Using Large Language Models](https://arxiv.org/abs/2404.03275) | 2024-04 | G | none | mobile-manip/sim |
| [Embodied AI with Two Arms: Zero-shot Learning, Safety and Modularity](https://arxiv.org/abs/2404.03570) | 2024-04 | G | none | manip/real |
| [VoicePilot: Harnessing LLMs as Speech Interfaces for Physically Assistive Robots](https://arxiv.org/abs/2404.04066) | 2024-04 | G | re-decide | manip/real |
| [LLM-BT: Performing Robotic Adaptive Tasks based on Large Language Models and Behavior Trees](https://arxiv.org/abs/2404.05134) | 2024-04 | G | none | mobile-manip/sim |
| [Long-horizon Locomotion and Manipulation on a Quadrupedal Robot with Large Language Models](https://arxiv.org/abs/2404.05291) | 2024-04 | G | re-decide | loco/sim+real |
| [Towards Human Awareness in Robot Task Planning with Large Language Models](https://arxiv.org/abs/2404.11267) | 2024-04 | G | none | mobile-manip/sim |
| [Action Contextualization: Adaptive Task Planning and Action Tuning Using Large Language Models](https://arxiv.org/abs/2404.13191) | 2024-04 | G | re-decide | manip/real |
| [Closed Loop Interactive Embodied Reasoning for Robot Manipulation](https://arxiv.org/abs/2404.15194) | 2024-04 | G | re-decide | manip/sim+real |
| [Plan-Seq-Learn: Language Model Guided RL for Solving Long Horizon Robotics Tasks](https://arxiv.org/abs/2405.01534) | 2024-05 | G | none | manip/sim |
| Using LLMs for Augmenting Hierarchical Agents with Common Sense Priors | 2024-05 | G | none | other/sim+real |
| An LLM-driven Framework for Multiple-Vehicle Dispatching and Navigation in Smart City Landscapes | 2024-05 | G | none | driving/sim |
| PlanCollabNL: Leveraging Large Language Models for Adaptive Plan Generation in Human-Robot Collaboration | 2024-05 | G | none | mobile-manip/sim |
| [A Prompt-Driven Task Planning Method for Multi-Drones Based on Large Language Model](https://arxiv.org/abs/2406.00006) | 2024-05 | G | none | aerial/sim |
| [GameVLM: A Decision-making Framework for Robotic Task Planning Based on Visual Language Models and Zero-sum Games](https://arxiv.org/abs/2405.13751) | 2024-05 | G | none | manip/real |
| [Towards Efficient LLM Grounding for Embodied Multi-Agent Collaboration](https://arxiv.org/abs/2405.14314) | 2024-05 | G | re-decide | multi-robot/sim |
| [LLM-based Robot Task Planning with Exceptional Handling for General Purpose Service Robots](https://arxiv.org/abs/2405.15646) | 2024-05 | G | none | mobile-manip/sim |
| [Safety Control of Service Robots with LLMs and Embodied Knowledge Graphs](https://arxiv.org/abs/2405.17846) | 2024-05 | G | none | mobile-manip/real |
| [Nadine: An LLM-driven Intelligent Social Robot with Affective Capabilities and Human-like Memory](https://arxiv.org/abs/2405.20189) | 2024-05 | G | re-decide | social/real |
| [HBTP: Heuristic Behavior Tree Planning with Large Language Model Reasoning](https://arxiv.org/abs/2406.00965) | 2024-06 | G | none | mobile-manip/sim |
| [Enhancing Human-Robot Collaborative Assembly in Manufacturing Systems Using Large Language Models](https://arxiv.org/abs/2406.01915) | 2024-06 | G | none | manip/real |
| [CLMASP: Coupling Large Language Models with Answer Set Programming for Robotic Task Planning](https://arxiv.org/abs/2406.03367) | 2024-06 | G | none | mobile-manip/sim |
| [AToM-Bot: Embodied Fulfillment of Unspoken Human Needs with Affective Theory of Mind](https://arxiv.org/abs/2406.08455) | 2024-06 | G | none | manip/real |
| [DAG-Plan: Generating Directed Acyclic Dependency Graphs for Dual-Arm Cooperative Planning](https://arxiv.org/abs/2406.09953) | 2024-06 | G | none | manip/sim |
| [Leveraging Large Language Model for Heterogeneous Ad Hoc Teamwork Collaboration](https://arxiv.org/abs/2406.12224) | 2024-06 | G | re-decide | multi-robot/sim |
| [LIT: Large Language Model Driven Intention Tracking for Proactive Human-Robot Collaboration - A Robot Sous-Chef Application](https://arxiv.org/abs/2406.13787) | 2024-06 | G | re-decide | manip/real |
| [HYPERmotion: Learning Hybrid Behavior Planning for Autonomous Loco-manipulation](https://arxiv.org/abs/2406.14655) | 2024-06 | G | none | humanoid/sim+real |
| [Towards Natural Language-Driven Assembly Using Foundation Models](https://arxiv.org/abs/2406.16093) | 2024-06 | G | re-decide | manip/sim |
| [QuadrupedGPT: Towards a Versatile Quadruped Agent in Open-ended Worlds](https://arxiv.org/abs/2406.16578) | 2024-06 | G | re-decide | loco/sim+real |
| Research on Robot’s Understanding of Different Concepts and Autonomous Planning | 2024-06 | G | none | manip/real |
| The Power of Atmosphere: LLM-Based Social Task Generation of Robots | 2024-06 | G | none | social/real |
| [LLCoach: Generating Robot Soccer Plans using Multi-Role Large Language Models](https://arxiv.org/abs/2406.18285) | 2024-06 | G | none | multi-robot/sim |
| [Open-vocabulary Mobile Manipulation in Unseen Dynamic Environments with 3D Semantic Maps](https://arxiv.org/abs/2406.18115) | 2024-06 | G | re-decide | mobile-manip/real |
| [ROS-LLM: A ROS framework for embodied AI with task feedback and structured reasoning](https://arxiv.org/abs/2406.19741) | 2024-06 | G | re-decide | manip/real |
| [When Robots Get Chatty: Grounding Multimodal Human-Robot Conversation and Collaboration](https://arxiv.org/abs/2407.00518) | 2024-06 | G | re-decide | social/real |
| [CAMON: Cooperative Agents for Multi-Object Navigation with LLM-based Conversations](https://arxiv.org/abs/2407.00632) | 2024-06 | G | re-decide | multi-robot/sim |
| Nadine: A large language model‐driven intelligent social robot with affective capabilities and human‐like memory | 2024-07 | G | re-decide | social/real |
| [Revolutionizing Battery Disassembly: The Design and Implementation of a Battery Disassembly Autonomous Mobile Manipulator Robot(BEAM-1)](https://arxiv.org/abs/2407.06590) | 2024-07 | G | none | mobile-manip/real |
| [FLAIR: Feeding via Long-horizon AcquIsition of Realistic dishes](https://arxiv.org/abs/2407.07561) | 2024-07 | G | re-decide | manip/real |
| Demonstrating Event-Triggered Investigation and Sample Collection for Human Scientists using Field Robots and Large Foundation Models | 2024-07 | G | none | multi-robot/real |
| From Perception to Action: Leveraging LLMs and Scene Graphs for Intuitive Robotic Task Execution | 2024-07 | G | re-decide | manip/sim |
| [SARO: Space-Aware Robot System for Terrain Crossing via Vision-Language Model](https://arxiv.org/abs/2407.16412) | 2024-07 | G | re-decide | loco/sim+real |
| [AI-Gadget Kit: Integrating Swarm User Interfaces with LLM-driven Agents for Rich Tabletop Game Applications](https://arxiv.org/abs/2407.17086) | 2024-07 | G | none | multi-robot/real |
| Hierarchical Generation of Action Sequence for Service Rots Based on Scene Graph via Large Language Models | 2024-07 | G | re-decide | mobile-manip/sim+real |
| [Wonderful Team: Zero-Shot Physical Task Planning with Visual LLMs](https://arxiv.org/abs/2407.19094) | 2024-07 | G | none | manip/real |
| Fine-Grained Task Planning for Service Robots Based on Object Ontology Knowledge via Large Language Models | 2024-08 | G | none | mobile-manip/real |
| [Semantic Skill Grounding for Embodied Instruction-Following in Cross-Domain Environments](https://arxiv.org/abs/2408.01024) | 2024-08 | G | none | mobile-manip/sim |
| [From Decision to Action in Surgical Autonomy: Multi-Modal Large Language Models for Robot-Assisted Blood Suction](https://arxiv.org/abs/2408.07806) | 2024-08 | G | re-decide | manip/sim |
| [Autonomous Behavior Planning For Humanoid Loco-manipulation Through Grounded Language Model](https://arxiv.org/abs/2408.08282) | 2024-08 | G | re-decide | humanoid/sim+real |
| [General-Purpose Clothes Manipulation with Semantic Keypoints](https://arxiv.org/abs/2408.08160) | 2024-08 | G | none | manip/sim+real |
| [Polaris: Open-ended Interactive Robotic Manipulation via Syn2Real Visual Grounding and Large Language Models](https://arxiv.org/abs/2408.07975) | 2024-08 | G | none | manip/real |
| Towards Text-based Human Search and Approach using a Robot Dog | 2024-08 | G | none | loco/sim+real |
| [Points2Plans: From Point Clouds to Long-Horizon Plans with Composable Relational Dynamics](https://arxiv.org/abs/2408.14769) | 2024-08 | G | none | manip/sim+real |
| Large Language Model for Humanoid Cognition in Proactive Human-Robot Collaboration | 2024-08 | G | none | manip/real |
| Large Language Model for Intuitive Control of Robots in Micro-Assembly | 2024-08 | G | none | manip/real |
| [Policy Adaptation via Language Optimization: Decomposing Tasks for Few-Shot Imitation](https://arxiv.org/abs/2408.16228) | 2024-08 | G | none | manip/real |
| [EMPOWER: Embodied Multi-role Open-vocabulary Planning with Online Grounding and Execution](https://arxiv.org/abs/2408.17379) | 2024-08 | G | re-decide | mobile-manip/real |
| [Grounding Language Models in Autonomous Loco-manipulation Tasks](https://arxiv.org/abs/2409.01326) | 2024-09 | G | none | humanoid/sim |
| [DexDiff: Towards Extrinsic Dexterity Manipulation of Ungraspable Objects in Unrestricted Environments](https://arxiv.org/abs/2409.05493) | 2024-09 | G | none | manip/sim+real |
| [Behavior Tree Generation using Large Language Models for Sequential Manipulation Planning with Human Instructions and Feedback](https://arxiv.org/abs/2409.09435) | 2024-09 | G | re-decide | manip/real |
| [Industry 6.0: New Generation of Industry driven by Generative AI and Swarm of Heterogeneous Robots](https://arxiv.org/abs/2409.10106) | 2024-09 | G | none | multi-robot/real |
| [LLM-as-BT-Planner: Leveraging LLMs for Behavior Tree Generation in Robot Task Planning](https://arxiv.org/abs/2409.10444) | 2024-09 | G | none | manip/sim+real |
| [Real-world cooking robot system from recipes based on food state recognition using foundation models and PDDL](https://arxiv.org/abs/2410.02874) | 2024-09 | G | none | mobile-manip/real |
| [PLATO: Planning with LLMs and Affordances for Tool Manipulation](https://arxiv.org/abs/2409.11580) | 2024-09 | G | re-decide | manip/sim |
| [Bootstrapping Object-Level Planning with Large Language Models](https://arxiv.org/abs/2409.12262) | 2024-09 | G | none | manip/sim |
| [LEMMo-Plan: LLM-Enhanced Learning from Multi-Modal Demonstration for Planning Sequential Contact-Rich Manipulation Tasks](https://arxiv.org/abs/2409.11863) | 2024-09 | G | none | manip/real |
| [InteLiPlan: An Interactive Lightweight LLM-Based Planner for Domestic Robot Autonomy](https://arxiv.org/abs/2409.14506) | 2024-09 | G | re-decide | mobile-manip/sim+real |
| [COHERENT: Collaboration of Heterogeneous Multi-Robot System with Large Language Models](https://arxiv.org/abs/2409.15146) | 2024-09 | G | re-decide | multi-robot/sim+real |
| ExTraCT – Explainable trajectory corrections for language-based human-robot interaction using textual feature descriptions | 2024-09 | G | none | manip/real |
| [Skills Made to Order: Efficient Acquisition of Robot Cooking Skills Guided by Multiple Forms of Internet Data](https://arxiv.org/abs/2409.15172) | 2024-09 | G | none | manip/real |
| [AIR-Embodied: An Efficient Active 3DGS-based Interaction and Reconstruction Framework with Embodied Large Language Model](https://arxiv.org/abs/2409.16019) | 2024-09 | G | re-decide | manip/sim+real |
| AirVista: Empowering UAVs with 3D Spatial Reasoning Abilities Through a Multimodal Large Language Model Agent | 2024-09 | C | none | aerial/sim |
| [MHRC: Closed-loop Decentralized Multi-Heterogeneous Robot Collaboration with Large Language Models](https://arxiv.org/abs/2409.16030) | 2024-09 | G | re-decide | multi-robot/sim |
| [MultiTalk: Introspective and Extrospective Dialogue for Human-Environment-LLM Alignment](https://arxiv.org/abs/2409.16455) | 2024-09 | G | none | manip/sim |
| [REBEL: Rule-based and Experience-enhanced Learning with LLMs for Initial Task Allocation in Multi-Human Multi-Robot Teaming](https://arxiv.org/abs/2409.16266) | 2024-09 | G | none | multi-robot/sim |
| [Fast and Accurate Task Planning using Neuro-Symbolic Language Models and Multi-Level Goal Decomposition](https://arxiv.org/abs/2409.19250) | 2024-09 | G | none | manip/sim+real |
| [SELP: Generating Safe and Efficient Task Plans for Robot Agents with Large Language Models](https://arxiv.org/abs/2409.19471) | 2024-09 | C | none | aerial/sim |
| [Helpful DoggyBot: Open-World Object Fetching using Legged Robots and Vision-Language Models](https://arxiv.org/abs/2410.00231) | 2024-09 | G | none | mobile-manip/real |
| [LaMMA-P: Generalizable Multi-Agent Long-Horizon Task Allocation and Planning with LM-Driven PDDL Planner](https://arxiv.org/abs/2409.20560) | 2024-09 | G | none | multi-robot/sim |
| [Robi Butler: Multimodal Remote Interaction with a Household Robot Assistant](https://arxiv.org/abs/2409.20548) | 2024-09 | G | none | mobile-manip/real |
| FlingFlow: LLM-Driven Dynamic Strategies for Efficient Cloth Flattening | 2024-10 | G | none | manip/real |
| [Towards Generalizable Vision-Language Robotic Manipulation: A Benchmark and LLM-Guided 3D Policy](https://arxiv.org/abs/2410.01345) | 2024-10 | G | none | manip/sim |
| [Guiding Long-Horizon Task and Motion Planning with Vision Language Models](https://arxiv.org/abs/2410.02193) | 2024-10 | G | re-decide | mobile-manip/sim |
| [ConceptAgent: LLM-Driven Precondition Grounding and Tree Search for Robust Task Planning and Execution](https://arxiv.org/abs/2410.06108) | 2024-10 | G | re-decide | mobile-manip/sim+real |
| [Enabling Novel Mission Operations and Interactions with ROSA: The Robot Operating System Agent](https://arxiv.org/abs/2410.06472) | 2024-10 | G | re-decide | other/sim |
| [GRAPPA: Generalizing and Adapting Robot Policies via Online Agentic Guidance](https://arxiv.org/abs/2410.06473) | 2024-10 | G | re-decide | manip/sim+real |
| [VLM See, Robot Do: Human Demo Video to Robot Action Plan via Vision Language Model](https://arxiv.org/abs/2410.08792) | 2024-10 | G | none | manip/sim+real |
| [Neuro-Symbolic Skill Discovery for Conditional Multi-Level Planning](https://arxiv.org/abs/2410.10045) | 2024-10 | G | none | manip/sim+real |
| [Towards an LLM-Based Speech Interface for Robot-Assisted Feeding](https://arxiv.org/abs/2410.20624) | 2024-10 | G | none | manip/real |
| Behavior-Actor: Behavioral Decomposition and Efficient-Training for Robotic Manipulation | 2024-10 | G | none | manip/real |
| [Combining Ontological Knowledge and Large Language Model for User-Friendly Service Robots](https://arxiv.org/abs/2410.16804) | 2024-10 | G | none | mobile-manip/sim |
| Fly by Book: How to Train a Humanoid Robot to Fly an Airplane using Large Language Models | 2024-10 | G | none | humanoid/sim |
| [Dynamic Open-Vocabulary 3D Scene Graphs for Long-Term Language-Guided Mobile Manipulation](https://arxiv.org/abs/2410.11989) | 2024-10 | G | none | mobile-manip/real |
| [Task-oriented Robotic Manipulation with Vision Language Models](https://arxiv.org/abs/2410.15863) | 2024-10 | G | none | manip/sim |
| ViLaBot: Connecting Vision and Language for Robots That Assist Humans at Home | 2024-10 | G | none | mobile-manip/sim |
| Foundation models assist in human–robot collaboration assembly | 2024-10 | G | none | manip/real |
| SortingBot: Leveraging Large Language Models and 3D Vision for Multi-Category Material Sorting | 2024-10 | G | none | manip/sim |
| [APRICOT: Active Preference Learning and Constraint-Aware Task Planning with LLMs](https://arxiv.org/abs/2410.19656) | 2024-10 | G | re-decide | mobile-manip/real |
| [LiP-LLM: Integrating Linear Programming and Dependency Graph With Large Language Models for Multi-Robot Task Planning](https://arxiv.org/abs/2410.21040) | 2024-10 | G | none | multi-robot/sim |
| [Local Policies Enable Zero-Shot Long-Horizon Manipulation](https://arxiv.org/abs/2410.22332) | 2024-10 | G | none | manip/sim+real |
| [EmbodiedRAG: Dynamic 3D Scene Graph Retrieval for Efficient and Scalable Robot Task Planning](https://arxiv.org/abs/2410.23968) | 2024-10 | G | re-decide | mobile-manip/sim+real |
| Task Planning for Dual-Arm Robot Empowered by Large Language Model | 2024-11 | G | none | manip/real |
| [Know Where You're Uncertain When Planning with Multimodal Foundation Models: A Formal Framework](https://arxiv.org/abs/2411.01639) | 2024-11 | G | none | manip/sim+real |
| Empowering Robots with Multimodal Language Models for Task Planning with Interaction | 2024-11 | G | none | mobile-manip/real |
| [Enhancing Robustness in Language-Driven Robotics: A Modular Approach to Failure Reduction](https://arxiv.org/abs/2411.05474) | 2024-11 | G | none | manip/sim |
| [Safe Planner: Empowering Safety Awareness in Large Pre-Trained Models for Robot Task Planning](https://arxiv.org/abs/2411.06920) `sim2real` | 2024-11 | G | none | manip/sim+real |
| [DART-LLM: Dependency-Aware Multi-Robot Task Decomposition and Execution using Large Language Models](https://arxiv.org/abs/2411.09022) | 2024-11 | G | none | multi-robot/sim |
| [Remote Life Support Robot Interface System for Global Task Planning and Local Action Expansion Using Foundation Models](https://arxiv.org/abs/2411.10038) | 2024-11 | G | re-decide | mobile-manip/real |
| [VeriGraph: Scene Graphs for Execution Verifiable Robot Planning](https://arxiv.org/abs/2411.10446) | 2024-11 | G | none | manip/sim+real |
| [SayComply: Grounding Field Robotic Tasks in Operational Compliance Through Retrieval-Based Language Models](https://arxiv.org/abs/2411.11323) | 2024-11 | G | none | other/sim+real |
| [Semantic-Geometric-Physical-Driven Robot Manipulation Skill Transfer via Skill Library and Tactile Representation](https://arxiv.org/abs/2411.11714) | 2024-11 | G | none | manip/real |
| [WildLMa: Long Horizon Loco-Manipulation in the Wild](https://arxiv.org/abs/2411.15131) | 2024-11 | G | none | mobile-manip/real |
| [Don’t Let Your Robot Be Harmful: Responsible Robotic Manipulation via Safety-As-Policy](https://arxiv.org/abs/2411.18289) | 2024-11 | G | none | manip/sim+real |
| [Dadu‐E: Rethinking the Role of Large Language Model in Robotic Computing Pipelines](https://arxiv.org/abs/2412.01663) | 2024-12 | G | re-decide | manip/sim+real |
| Implementation of Natural Language UAV Control Using OpenAI's ChatGPT in a Simulated University Environment | 2024-12 | G | none | aerial/sim |
| [Planning and Reasoning with 3D Deformable Objects for Hierarchical Text-to-3D Robotic Shaping](https://arxiv.org/abs/2412.01765) | 2024-12 | G | re-decide | manip/real |
| [CALMM-Drive: Confidence-Aware Autonomous Driving with Large Multimodal Model](https://arxiv.org/abs/2412.04209) | 2024-12 | G | none | driving/sim |
| Integrating Large Language Models for Task Planning in Robots ‐ A case Study with NAO | 2024-12 | G | none | humanoid/real |
| [Non-Prehensile Tool-Object Manipulation by Integrating LLM-Based Planning and Manoeuvrability-Driven Controls](https://arxiv.org/abs/2412.06931) | 2024-12 | G | none | manip/real |
| 3C Assembly Methods and Systems Based on Large Language Models | 2024-12 | G | none | manip/real |
| Enhancing Household Service Robots with a Dual-Arm Mobile Manipulator and Multimodal Large Language Models | 2024-12 | G | none | mobile-manip/real |
| Instruction-Following Long-Horizon Manipulation by LLM-Empowered Symbolic Planner | 2024-12 | G | none | mobile-manip/real |
| LAC: Using LLM-based Agents as the Controller to Realize Embodied Robot | 2024-12 | G | re-decide | other/sim |
| [LLM-guided Task and Motion Planning using Knowledge-based Reasoning](https://arxiv.org/abs/2412.07493) | 2024-12 | G | none | manip/sim |
| Think Before Execute: Embodied Reasoning of Supportive Tools for Robot Service with Large Language Models | 2024-12 | G | none | mobile-manip/sim+real |
| ECRAP: Exophora Resolution and Classifying User Commands for Robot Action Planning by Large Language Models | 2024-12 | G | none | mobile-manip/real |
| [SwarmGPT: Combining Large Language Models With Safe Motion Planning for Drone Swarm Choreography](https://arxiv.org/abs/2412.08428) | 2024-12 | G | none | aerial/sim+real |
| [Sketch-MoMa: Teleoperation for Mobile Manipulator via Interpretation of Hand-Drawn Sketches](https://arxiv.org/abs/2412.19153) | 2024-12 | G | none | mobile-manip/real |
| Dual-LLM Hierarchical Task Planning and Skill Grounding for Mobile Manipulation in Long-Horizon Restroom Cleaning | 2025 | G | re-decide | mobile-manip/real |
| Enhancing LLM Planning for Robotics Manipulation through Hierarchical Procedural Knowledge Graphs | 2025 | G | none | manip/sim |
| LLM-Driven Pareto-Optimal Multi-Mode Reinforcement Learning for Adaptive UAV Navigation in Urban Wind Environments | 2025 | C | re-decide | aerial/sim |
| Language-Guided Dexterous Functional Grasping by LLM Generated Grasp Functionality and Synergy for Humanoid Manipulation | 2025 | G | none | humanoid/sim |
| Learn-Gen-Plan: Bridging the Gap Between Vision Language Models and Real-World Long-Horizon Dexterous Manipulations | 2025 | G | none | manip/real |
| Mitigating Cross-Modal Distraction and Ensuring Geometric Feasibility via Affordance-Guided, Self-Consistent MLLMs for Food Preparation Task Planning | 2025 | G | re-decide | manip/sim |
| Spatial Concepts-Based Prompts With Large Language Models for Robot Action Planning | 2025 | G | none | mobile-manip/sim |
| Using Vision Language Models as Closed-Loop Symbolic Planners for Robotic Applications: A Control-Theoretic Perspective | 2025 | G | re-decide | manip/sim |
| [UAV-VLA: Vision-Language-Action System for Large Scale Aerial Mission Generation](https://arxiv.org/abs/2501.05014) | 2025-01 | G | none | aerial/sim |
| [Shake-VLA: Vision-Language-Action Model-Based System for Bimanual Robotic Manipulations and Liquid Mixing](https://arxiv.org/abs/2501.06919) | 2025-01 | G | none | manip/real |
| [LAMS: LLM-Driven Automatic Mode Switching for Assistive Teleoperation](https://arxiv.org/abs/2501.08558) | 2025-01 | G | re-decide | manip/sim |
| [RoboReflect: A Robotic Reflective Reasoning Framework for Grasping Ambiguous-Condition Objects](https://arxiv.org/abs/2501.09307) | 2025-01 | G | re-decide | manip/real |
| Human–robot interaction through joint robot planning with large language models | 2025-01 | G | none | manip/real |
| Integrating Multimodal Communication and Comprehension Evaluation during Human-Robot Collaboration for Increased Reliability of Foundation Model-based Task Planning Systems | 2025-01 | G | re-decide | manip/real |
| [Scalable, Training-Free Visual Language Robotics: a modular multi-model framework for consumer-grade GPUs](https://arxiv.org/abs/2502.01071) | 2025-01 | G | none | manip/sim |
| [Think Small, Plan Smart: Minimalist Symbolic Abstraction and Heuristic Subspace Search for LLM-Guided Task Planning](https://arxiv.org/abs/2501.15214) | 2025-01 | G | none | mobile-manip/sim |
| Toward Universal Embodied Planning in Scalable Heterogeneous Field Robots Collaboration and Control | 2025-01 | C | none | multi-robot/sim |
| [Integrating LMM Planners and 3D Skill Policies for Generalizable Manipulation](https://arxiv.org/abs/2501.18733) | 2025-01 | G | re-decide | manip/real |
| [Learn from the Past: Language-conditioned Object Rearrangement with Large Language Models](https://arxiv.org/abs/2501.18516) | 2025-01 | G | none | manip/sim+real |
| [Neuro-LIFT: A Neuromorphic, LLM-based Interactive Framework for Autonomous Drone FlighT at the Edge](https://arxiv.org/abs/2501.19259) | 2025-01 | G | none | aerial/sim+real |
| Achieving adaptive tasks from human instructions for robots using large language models and behavior trees | 2025-02 | G | none | manip/sim+real |
| [Manual2Skill: Learning to Read Manuals and Acquire Robotic Skills for Furniture Assembly Using Vision-Language Models](https://arxiv.org/abs/2502.10090) | 2025-02 | G | none | manip/real |
| GPT Voice-Driven Natural Language Control for ArduPilot-Guided UAVs | 2025-02 | G | none | aerial/sim |
| [RobotIQ: Empowering mobile robots with human-level planning for real-world execution](https://arxiv.org/abs/2502.12862) | 2025-02 | G | none | mobile-manip/sim+real |
| [USPilot: An Embodied Robotic Assistant Ultrasound System With a Large Language Model Enhanced Graph Planner](https://arxiv.org/abs/2502.12498) | 2025-02 | C | none | manip/real |
| [Reflective Planning: Vision-Language Models for Multi-Stage Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2502.16707) | 2025-02 | G | re-decide | manip/real |
| [Evolution 6.0: Robot Evolution through Generative Design](https://arxiv.org/abs/2502.17034) | 2025-02 | G | none | manip/real |
| LLM-RSPF: Large Language Model-Based Robotic System Planning Framework for Domain Specific Use-cases | 2025-02 | G | none | manip/sim |
| Task Planning for a Factory Robot Using Large Language Model | 2025-03 | G | re-decide | mobile-manip/sim+real |
| [CLEA: Closed-Loop Embodied Agent for Enhancing Task Execution in Dynamic Environments](https://arxiv.org/abs/2503.00729) | 2025-03 | G | re-decide | multi-robot/real |
| [RoboDexVLM: Visual Language Model-Enabled Task Planning and Motion Control for Dexterous Robot Manipulation](https://arxiv.org/abs/2503.01616) | 2025-03 | G | re-decide | manip/real |
| [FlowPlan: Zero-Shot Task Planning with LLM Flow Engineering for Robotic Instruction Following](https://arxiv.org/abs/2503.02698) | 2025-03 | G | none | mobile-manip/sim+real |
| [UAV-VLPA*: A Vision-Language-Path-Action System for Optimal Route Generation on a Large Scales](https://arxiv.org/abs/2503.02454) | 2025-03 | G | none | aerial/sim |
| [UAV-VLRR: Vision-Language Informed NMPC for Rapid Response in UAV Search and Rescue](https://arxiv.org/abs/2503.02465) | 2025-03 | G | none | aerial/real |
| [Learning Generalizable Language-Conditioned Cloth Manipulation from Long Demonstrations](https://arxiv.org/abs/2503.04557) | 2025-03 | G | none | manip/sim |
| [Perceiving, Reasoning, Adapting: A Dual-Layer Framework for VLM-Guided Precision Robotic Manipulation](https://arxiv.org/abs/2503.05064) | 2025-03 | G | re-decide | manip/real |
| A Multiagent-Driven Robotic AI Chemist Enabling Autonomous Chemical Research On Demand. | 2025-03 | G | re-decide | other/real |
| [Self-Corrective Task Planning by Inverse Prompting with Large Language Models](https://arxiv.org/abs/2503.07317) | 2025-03 | G | none | manip/sim |
| [FAM-HRI: Foundation-Model Assisted Multimodal Human–Robot Interaction Combining Gaze and Speech](https://arxiv.org/abs/2503.16492) | 2025-03 | G | none | manip/real |
| [Instruction-Augmented Long-Horizon Planning: Embedding Grounding Mechanisms in Embodied Mobile Manipulation](https://arxiv.org/abs/2503.08084) | 2025-03 | G | re-decide | humanoid/real |
| [LightPlanner: Unleashing the Reasoning Capabilities of Lightweight Large Language Models in Task Planning](https://arxiv.org/abs/2503.08508) | 2025-03 | G | re-decide | mobile-manip/sim+real |
| [Trinity: A Modular Humanoid Robot AI System](https://arxiv.org/abs/2503.08338) | 2025-03 | G | re-decide | humanoid/real |
| [NVP-HRI: Zero shot natural voice and posture-based human-robot interaction via large language model](https://arxiv.org/abs/2503.09335) | 2025-03 | G | none | manip/real |
| [Enhancing Multi-Agent Systems via Reinforcement Learning with LLM-Based Planner and Graph-Based Policy](https://arxiv.org/abs/2503.10049) | 2025-03 | G | none | multi-robot/sim |
| [Free-form language-based robotic reasoning and grasping](https://arxiv.org/abs/2503.13082) | 2025-03 | G | none | manip/real |
| [Mindeye-Omniassist: A Gaze-Driven LLM-Enhanced Assistive Robot System for Implicit Intention Recognition and Task Execution](https://arxiv.org/abs/2503.13250) | 2025-03 | G | none | manip/real |
| [Mitigating Cross-Modal Distraction and Ensuring Geometric Feasibility via Affordance-Guided and Self-Consistent MLLMs for Task Planning in Instruction-Following Manipulation](https://arxiv.org/abs/2503.13055) | 2025-03 | G | re-decide | manip/sim |
| GPTArm: An Autonomous Task Planning Manipulator Grasping System Based on Vision–Language Models | 2025-03 | G | re-decide | manip/real |
| [LLM-drone: aerial additive manufacturing with drones planned using large language models](https://arxiv.org/abs/2503.17566) | 2025-03 | G | re-decide | aerial/sim |
| Large Language Modeling and Visual Perception Based Home Service Robot Research | 2025-03 | C | none | manip/real |
| Multi-Object Grasp Planning with Vision-Language Models for Laboratory Automation | 2025-03 | G | none | manip/real |
| LMD-FISH: Language Model Driven - Framework for Intelligent Scheduling of Heterogenous Systems | 2025-03 | G | none | multi-robot/real |
| [Option Discovery Using LLM-guided Semantic Hierarchical Reinforcement Learning](https://arxiv.org/abs/2503.19007) | 2025-03 | G | none | other/sim |
| [Learning Adaptive Dexterous Grasping from Single Demonstrations](https://arxiv.org/abs/2503.20208) | 2025-03 | G | none | manip/sim+real |
| [Cooking Task Planning using LLM and Verified by Graph Network](https://arxiv.org/abs/2503.21564) | 2025-03 | G | none | manip/sim |
| [REMAC: Self-Reflective and Self-Evolving Multi-Agent Collaboration for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2503.22122) | 2025-03 | G | re-decide | multi-robot/sim+real |
| [AINav: Large Language Model-Based Adaptive Interactive Navigation](https://arxiv.org/abs/2503.22942) | 2025-03 | G | re-decide | loco/sim+real |
| An Interactive Autonomous Forklift Robot Based on Large Language Models | 2025-03 | G | none | mobile-manip/sim |
| [Exploring GPT-4 for Robotic Agent Strategy with Real-Time State Feedback and a Reactive Behaviour Framework](https://arxiv.org/abs/2503.23601) | 2025-03 | G | re-decide | humanoid/sim+real |
| [Neuro-Symbolic Control with Large Language Models for Language-Guided Spatial Tasks](https://arxiv.org/abs/2512.17321) | 2025-04 | G | none | manip/sim |
| [AuDeRe: Automated Strategy Decision and Realization in Robot Planning and Control via LLMs](https://arxiv.org/abs/2504.03015) | 2025-04 | G | re-decide | other/sim |
| [Hierarchical Planning for Complex Tasks with Knowledge Graph-RAG and Symbolic Verification](https://arxiv.org/abs/2504.04578) | 2025-04 | G | re-decide | manip/sim+real |
| [Humanoid Agent via Embodied Chain-of-Action Reasoning with Multimodal Foundation Models for Zero-Shot Loco-Manipulation](https://arxiv.org/abs/2504.09532) | 2025-04 | G | none | humanoid/real |
| [EmbodiedAgent: A Scalable Hierarchical Approach to Overcome Practical Challenge in Multi-Robot Control](https://arxiv.org/abs/2504.10030) | 2025-04 | C | re-decide | multi-robot/real |
| [Chain-of-Modality: Learning Manipulation Programs from Multimodal Human Videos with Vision-Language-Models](https://arxiv.org/abs/2504.13351) | 2025-04 | G | none | manip/real |
| [Robotic Task Ambiguity Resolution via Natural Language Interaction](https://arxiv.org/abs/2504.17748) | 2025-04 | C | re-decide | manip/sim+real |
| The Multi-Agentization of a Dual-Arm Nursing Robot Based on Large Language Models | 2025-04 | G | none | manip/real |
| ACKnowledge: A Computational Framework for Human Compatible Affordance-based Interaction Planning in Real-world Contexts | 2025-04 | G | none | mobile-manip/sim |
| Research on Robot Action Planning Based on Chatcliport | 2025-04 | G | re-decide | manip/sim |
| [CoordField: Coordination Field for Agentic UAV Task Allocation in Low-Altitude Urban Scenarios](https://arxiv.org/abs/2505.00091) | 2025-04 | G | none | multi-robot/sim |
| [LLM-Empowered Embodied Agent for Memory-Augmented Task Planning in Household Robotics](https://arxiv.org/abs/2504.21716) | 2025-04 | G | none | mobile-manip/real |
| [Leveraging Pre-trained Large Language Models with Refined Prompting for Online Task and Motion Planning](https://arxiv.org/abs/2504.21596) | 2025-04 | G | re-decide | manip/sim |
| [DeCo: Task Decomposition and Skill Composition for Zero-Shot Generalization in Long-Horizon 3D Manipulation](https://arxiv.org/abs/2505.00527) | 2025-05 | G | none | manip/sim+real |
| [DriveAgent: Multi-Agent Structured Reasoning With LLM and Multimodal Sensor Fusion for Autonomous Driving](https://arxiv.org/abs/2505.02123) | 2025-05 | G | none | driving/real |
| [MORE: Mobile Manipulation Rearrangement Through Grounded Language Reasoning](https://arxiv.org/abs/2505.03035) | 2025-05 | G | re-decide | mobile-manip/sim+real |
| [CityNavAgent: Aerial Vision-and-Language Navigation with Hierarchical Semantic Planning and Global Memory](https://arxiv.org/abs/2505.05622) `vln` | 2025-05 | G | authored | aerial/sim |
| [Air-Ground Collaboration for Language-Specified Missions in Unknown Environments](https://arxiv.org/abs/2505.09108) | 2025-05 | G | re-decide | multi-robot/real |
| [Deploying Foundation Model-Enabled Air and Ground Robots in the Field: Challenges and Opportunities](https://arxiv.org/abs/2505.09477) | 2025-05 | G | re-decide | multi-robot/real |
| An Efficient Voice-Interactive Grasping Method for Humanoid Robots Based on LLM | 2025-05 | G | none | humanoid/real |
| Autonomous Behavior Control for Quadruped Robots with Arms Based on MultiModal Large Language Model | 2025-05 | G | re-decide | mobile-manip/real |
| Emotion-Aware LLM Systems for Adaptive Human-Robot Interaction | 2025-05 | C | re-decide | manip/sim |
| Hierarchical Task Scheduling and Robotic Manipulation for Autonomous Materials Discovery | 2025-05 | G | none | mobile-manip/sim+real |
| Industrial Assembly Autonomous Decision-Making Solution Based on Large Language Model and Vision-Motion Fusion | 2025-05 | G | none | manip/real |
| Goal-Guided Reinforcement Learning: Leveraging Large Language Models for Long-Horizon Task Decomposition | 2025-05 | G | none | manip/sim |
| IntelliRMS: A Robotic Manipulation System for Domain-Specific Tasks Using Vision and Language Foundational Models | 2025-05 | G | none | manip/real |
| Large Language Model Based Autonomous Task Planning for Abstract Commands | 2025-05 | G | none | mobile-manip/sim |
| Task-Aware Semantic Map: Autonomous Robot Task Assignment Beyond Commands | 2025-05 | G | none | mobile-manip/sim+real |
| [LA-RCS: LLM-Agent-Based Robot Control System](https://arxiv.org/abs/2505.18214) | 2025-05 | G | re-decide | other/real |
| VST-LLM HRI: Multimodal Human-Robot Interaction via Large Language Model Prompts | 2025-05 | G | none | loco/real |
| [Collision- and Reachability-Aware Multi-Robot Control with Grounded LLM Planners](https://arxiv.org/abs/2505.20573) | 2025-05 | C | none | multi-robot/sim |
| [Robot Operation of Home Appliances by Reading User Manuals](https://arxiv.org/abs/2505.20424) | 2025-05 | G | re-decide | manip/sim+real |
| [Agentic Robot: A Brain-Inspired Framework for Vision-Language-Action Models in Embodied Agents](https://arxiv.org/abs/2505.23450) | 2025-05 | G | re-decide | manip/sim |
| [Visual Embodied Brain: Let Multimodal Large Language Models See, Think, and Control in Spaces](https://arxiv.org/abs/2506.00123) | 2025-05 | C |  | loco/real |
| LL-MAROCO: A Large Language Model-Assisted Robotic System for Oral and Craniomaxillofacial Osteotomy | 2025-06 | G | none | manip/real |
| [OWMM-Agent: Open World Mobile Manipulation With Multi-modal Agentic Data Synthesis](https://arxiv.org/abs/2506.04217) | 2025-06 | C | re-decide | mobile-manip/sim+real |
| TORNADO: Foundation Models for Robots that Handle Small, Soft and Deformable Objects | 2025-06 | G | re-decide | mobile-manip/real |
| [Understanding physical properties of unseen deformable objects by leveraging large-language models and robot actions](https://arxiv.org/abs/2506.03760) | 2025-06 | G | re-decide | manip/real |
| [Hierarchical Language Models for Semantic Navigation and Manipulation in an Aerial‐Ground Robotic System](https://arxiv.org/abs/2506.05020) | 2025-06 | G | none | multi-robot/sim+real |
| [Prime the search: Using large language models for guiding geometric task and motion planning by warm-starting tree search](https://arxiv.org/abs/2506.07062) | 2025-06 | G | none | manip/sim |
| [RoboPARA: Dual-Arm Robot Planning with Parallel Allocation and Recomposition Across Tasks](https://arxiv.org/abs/2506.06683) | 2025-06 | G | none | manip/sim |
| [Taking Flight with Dialogue: Enabling Natural Language Control for PX4-based Drone Agent](https://arxiv.org/abs/2506.07509) | 2025-06 | G | re-decide | aerial/sim+real |
| [One For All: LLM-based Heterogeneous Mission Planning in Precision Agriculture](https://arxiv.org/abs/2506.10106) | 2025-06 | G | none | multi-robot/real |
| LLM and VLM-Assisted Human-Robot Collaboration Framework for Smart Assembly Cells | 2025-06 | G | none | manip/real |
| [ProVox: Personalization and Proactive Planning for Situated Human-Robot Collaboration](https://arxiv.org/abs/2506.12248) | 2025-06 | G | re-decide | manip/real |
| [Casper: Inferring Diverse Intents for Assistive Teleoperation with Vision Language Models](https://arxiv.org/abs/2506.14727) | 2025-06 | G | re-decide | manip/real |
| [Context Matters! Relaxing Goals with LLMs for Feasible 3D Scene Planning](https://arxiv.org/abs/2506.15828) | 2025-06 | G | none | mobile-manip/sim |
| [Reflective VLM Planning for Dual-Arm Desktop Cleaning: Bridging Open-Vocabulary Perception and Precise Manipulation](https://arxiv.org/abs/2506.17328) | 2025-06 | G | re-decide | manip/sim |
| [Distilling On-device Language Models for Robot Planning with Minimal Human Intervention](https://arxiv.org/abs/2506.17486) | 2025-06 | C | re-decide | mobile-manip/sim+real |
| Fuzzy-LLM: Multi-Agent Task Planning with Large Language Models | 2025-06 | G | none | multi-robot/sim |
| [STEP Planner: Constructing cross-hierarchical subgoal tree as an embodied long-horizon task planner](https://arxiv.org/abs/2506.21030) | 2025-06 | C | re-decide | mobile-manip/sim+real |
| Exploring Edge Inference Feasibility of Small Scale Deep Learning Models for Robotic Manipulation | 2025-06 | G | re-decide | manip/real |
| Hover-Bvi: Handover Vision-Language Embodied Robot System for Bvi Users | 2025-06 | G | none | manip/real |
| [Hierarchical Vision-Language Planning for Multi-Step Humanoid Manipulation](https://arxiv.org/abs/2506.22827) | 2025-06 | G | re-decide | humanoid/real |
| Decision-Making Algorithm Based on Multiple Context-Aware Agents for Human-Robot Interaction | 2025-06 | G | none | social/real |
| Bimanual Long-Horizon Lifecare Robotics with Temporal Context LLM Planner and Transformer Reinforcement Learning | 2025-07 | G | none | manip/sim |
| [BioMARS: A Multi-Agent Robotic System for Autonomous Biological Experiments](https://arxiv.org/abs/2507.01485) | 2025-07 | G | re-decide | manip/real |
| [VLM-TDP: VLM-guided Trajectory-conditioned Diffusion Policy for Robust Long-Horizon Manipulation](https://arxiv.org/abs/2507.04524) | 2025-07 | G | none | manip/sim |
| [LOVON: Legged Open-Vocabulary Object Navigator](https://arxiv.org/abs/2507.06747) | 2025-07 | G | none | loco/real |
| Minimalist Tooling and "Aim-and-Shoot" Skills for AI-Powered Robotic Manipulation | 2025-07 | G | none | manip/real |
| SURTR: Semantic Understanding and Reinforced Trajectory Robotics via Collaborative Multi-LLMs and Offline Reinforcement Learning | 2025-07 | G | re-decide | manip/sim+real |
| [VLA-Touch: Enhancing Vision-Language-Action Models with Dual-Level Tactile Feedback](https://arxiv.org/abs/2507.17294) | 2025-07 | G | re-decide | manip/real |
| [Adaptive Articulated Object Manipulation on the Fly with Foundation Model Reasoning and Part Grounding](https://arxiv.org/abs/2507.18276) | 2025-07 | G | re-decide | manip/sim+real |
| [CLASP: General-Purpose Clothes Manipulation with Semantic Keypoints](https://arxiv.org/abs/2507.19983) | 2025-07 | G | none | manip/sim+real |
| A Language Model-Based Framework for Task Planning and Execution in Real-World Service Robot | 2025-07 | G | re-decide | mobile-manip/real |
| [UniDomain: Pretraining a Unified PDDL Domain from Real-World Demonstrations for Generalizable Robot Task Planning](https://arxiv.org/abs/2507.21545) | 2025-07 | G | none | manip/real |
| [Distributed AI Agents for Cognitive Underwater Robot Autonomy](https://arxiv.org/abs/2507.23735) | 2025-07 | G | re-decide | other/sim+real |
| Scene Graph-Based Spatial Reasoning with VLM for High-Level Robotic Tasks | 2025-08 | G | none | manip/real |
| [AquaChat++: LLM-Assisted Multi-ROV Inspection for Aquaculture Net Pens with Integrated Battery Management and Thruster Fault Tolerance](https://arxiv.org/abs/2508.06554) | 2025-08 | G | none | multi-robot/sim |
| [Intention: Inferring Tendencies of Humanoid Robot Motion Through Interactive Intuition and Grounded VLM](https://arxiv.org/abs/2508.04931) | 2025-08 | G | none | humanoid/real |
| [GhostShell: Streaming LLM Function Calls for Concurrent Embodied Programming](https://arxiv.org/abs/2508.05298) | 2025-08 | G | none | social/real |
| [Mixed-Initiative Dialog for Human-Robot Collaborative Manipulation](https://arxiv.org/abs/2508.05535) | 2025-08 | G | re-decide | manip/sim+real |
| CL-RAG: A Closed-Loop Multimodal Retrieval-Augmented Generation Architecture for Robust Human-Robot Control Interaction | 2025-08 | G | none | loco/sim |
| [ODYSSEY: Open-World Quadrupeds Exploration and Manipulation for Long-Horizon Tasks](https://arxiv.org/abs/2508.08240) | 2025-08 | G | none | mobile-manip/sim+real |
| [A Semantic-Aware Framework for Safe and Intent-Integrative Assistance in Upper-Limb Exoskeletons](https://arxiv.org/abs/2508.10378) | 2025-08 | G | none | other/real |
| [ExploreVLM: Closed-Loop Robot Exploration Task Planning with Vision-Language Models](https://arxiv.org/abs/2508.11918) | 2025-08 | G | re-decide | manip/real |
| Learning Machine Tending from Demonstration with Multimodal LLMs | 2025-08 | G | none | mobile-manip/real |
| Multimodal Interaction for Human-Robot Collaboration in Assembly: An LLM-Enhanced Approach | 2025-08 | G | none | manip/real |
| [DEXTER-LLM: Dynamic and Explainable Coordination of Multi-Robot Systems in Unknown Environments via Large Language Models](https://arxiv.org/abs/2508.14387) | 2025-08 | G | re-decide | multi-robot/sim+real |
| Multi-Agent Collaborative Closed-Loop Planning - Evaluation - Assessment Framework: Optimization and Interpretability Evaluation | 2025-08 | G | none | mobile-manip/sim |
| Lang2Pose: Language-Based Visual Servoing and Pose Control for Autonomous Pick-and-Place in Real and Simulated Environments | 2025-08 | G | none | manip/sim+real |
| [ConceptBot: Enhancing Robot's Autonomy through Task Decomposition with Large Language Models and Knowledge Graph](https://arxiv.org/abs/2509.00570) | 2025-08 | G | none | manip/sim |
| From Demand to Grounded Plan: Task Customization and Planning for Service Robots With Deep Learning and LLMs | 2025-09 | G | none | mobile-manip/sim |
| Improving Efficiency of Answer Set Planning with Rough Solutions from Large Language Models for Robotic Task Planning | 2025-09 | G | none | mobile-manip/sim |
| L2M2: A Hierarchical Framework Integrating Large Language Model and Multi-agent Reinforcement Learning | 2025-09 | G | none | multi-robot/sim |
| Language-Conditioned Open-Vocabulary Mobile Manipulation with Pretrained Models | 2025-09 | G | none | mobile-manip/sim |
| [Language-Guided Long Horizon Manipulation with LLM-based Planning and Visual Perception](https://arxiv.org/abs/2509.02324) | 2025-09 | G | none | manip/sim+real |
| [Shared Autonomy through LLMs and Reinforcement Learning for Applications to Ship Hull Inspections](https://arxiv.org/abs/2509.05042) | 2025-09 | G | none | multi-robot/sim+real |
| Toward Co-Working with Autonomous Agents: Rethinking Operations of Automation Systems | 2025-09 | G | none | manip/real |
| [RoboChemist: Long-Horizon and Safety-Compliant Robotic Chemical Experimentation](https://arxiv.org/abs/2509.08820) | 2025-09 | G | re-decide | manip/real |
| Efficient Long-Horizon Mobile Manipulation with RAG-Assisted Vision Language Models | 2025-09 | G | none | mobile-manip/sim |
| [Robot guide with multi-agent control and automatic scenario generation with LLM](https://arxiv.org/abs/2509.10317) | 2025-09 | G | none | social/real |
| [AssemMate: Graph-Based LLM for Robotic Assembly Assistance](https://arxiv.org/abs/2509.11617) | 2025-09 | C | none | manip/real |
| [Multi-robot task planning for multi-object retrieval tasks with distributed on-site knowledge via large language models](https://arxiv.org/abs/2509.12838) | 2025-09 | G | none | multi-robot/sim |
| [DREAM: Domain-aware Reasoning for Efficient Autonomous Underwater Monitoring](https://arxiv.org/abs/2509.13666) | 2025-09 | G | re-decide | other/sim |
| [GestOS: Advanced Hand Gesture Interpretation via Large Language Models to control Any Type of Robot](https://arxiv.org/abs/2509.14412) | 2025-09 | G | none | multi-robot/real |
| [PhysicalAgent: Towards General Cognitive Robotics with Foundation World Models](https://arxiv.org/abs/2509.13903) | 2025-09 | G | re-decide | manip/sim+real |
| [Agentic Aerial Cinematography: From Dialogue Cues to Cinematic Trajectories](https://arxiv.org/abs/2509.16176) | 2025-09 | G | none | aerial/sim |
| [Video-to-BT: Generating Reactive Behavior Trees from Human Demonstration Videos for Robotic Assembly](https://arxiv.org/abs/2509.16611) | 2025-09 | G | re-decide | manip/real |
| [IDfRA: Self-Verification for Iterative Design in Robotic Assembly](https://arxiv.org/abs/2509.16998) | 2025-09 | G | re-decide | manip/real |
| [Language-in-the-Loop Culvert Inspection on the Erie Canal](https://arxiv.org/abs/2509.21370) | 2025-09 | G | re-decide | loco/real |
| [Agentic Scene Policies: Unifying Space, Semantics, and Affordances for Robot Action](https://arxiv.org/abs/2509.19571) | 2025-09 | G | re-decide | manip/sim+real |
| Zero-Shot Task Automation with Foundation Language Models | 2025-09 | G | re-decide | manip/sim |
| [SAGE: Scene Graph-Aware Guidance and Execution for Long-Horizon Manipulation Tasks](https://arxiv.org/abs/2509.21928) | 2025-09 | G | none | manip/sim+real |
| [UML-CoT: Structured Reasoning and Planning with Unified Modeling Language for Robotic Room Cleaning](https://arxiv.org/abs/2509.22628) | 2025-09 | C | none | mobile-manip/sim |
| PuppetLine: An Interactive System for Embodied Storytelling with LLM-driven Swarm Robots | 2025-09 | G | none | multi-robot/real |
| [PhysiAgent: An Embodied Agent Framework in Physical World](https://arxiv.org/abs/2509.24524) | 2025-09 | G | re-decide | manip/real |
| [Preference-Based Long-Horizon Robotic Stacking with Multimodal Large Language Models](https://arxiv.org/abs/2509.24163) | 2025-09 | C | none | manip/real |
| [A Hierarchical Agentic Framework for Autonomous Drone-Based Visual Inspection](https://arxiv.org/abs/2510.00259) | 2025-09 | G | re-decide | aerial/real |
| [RoboPilot: Generalizable Dynamic Robotic Manipulation with Dual-thinking Modes](https://arxiv.org/abs/2510.00154) | 2025-09 | G | re-decide | manip/sim+real |
| SynPolDex: Synergizing Fingers via Bi-Level Policy Learning for Dexterous Robotic Hands | 2025-09 | G | none | manip/sim |
| [LangGrasp: Leveraging Fine-Tuned LLMs for Language Interactive Robot Grasping with Ambiguous Instructions](https://arxiv.org/abs/2510.02104) | 2025-10 | C | none | manip/real |
| [TACOS: Task Agnostic COordinator of a multi-drone System](https://arxiv.org/abs/2510.01869) | 2025-10 | G | re-decide | multi-robot/sim+real |
| SkyNet: An Extensible Edge-Cloud Collaborative Framework for Robots in Long-Horizon Tasks | 2025-10 | G | re-decide | manip/real |
| A Hands-on Workshop on Designing LLM-Powered Context-Aware Behavior for Companion Robots | 2025-10 | G | none | social/real |
| [ARRC: Advanced Reasoning Robot Control - Knowledge-Driven Autonomous Manipulation Using Retrieval-Augmented Generation](https://arxiv.org/abs/2510.05547) | 2025-10 | G | none | manip/real |
| [Constrained natural language action planning for resilient embodied systems](https://arxiv.org/abs/2510.06357) | 2025-10 | G | re-decide | loco/sim+real |
| [FLEET: Formal Language-Grounded Scheduling for Heterogeneous Robot Teams](https://arxiv.org/abs/2510.07417) | 2025-10 | G | re-decide | multi-robot/sim+real |
| Implicit instruction reasoning by fine-tuning VLM for robotic manipulation | 2025-10 | C | none | manip/real |
| [LLM-HBT: Dynamic Behavior Tree Construction for Adaptive Coordination in Heterogeneous Robots](https://arxiv.org/abs/2510.09963) | 2025-10 | G | re-decide | multi-robot/sim+real |
| [RobotFleet: An Open-Source Framework for Centralized Multi-Robot Task Planning](https://arxiv.org/abs/2510.10379) | 2025-10 | G | re-decide | multi-robot/sim |
| [VLA^2: Empowering Vision-Language-Action Models with an Agentic Framework for Unseen Concept Manipulation](https://arxiv.org/abs/2510.14902) | 2025-10 | G | re-decide | manip/sim |
| A Modular Vision-Language-Action Framework for Autonomous Pressure Ulcer Care | 2025-10 | G | none | manip/real |
| LLM-Based Human-Robot Collaboration Task Sequence Optimization Method Fusing Scene Semantics and Object Attributes | 2025-10 | G | none | manip/real |
| [Manual2Skill++: Connector-Aware General Robotic Assembly from Instruction Manuals via Vision–Language Models](https://arxiv.org/abs/2510.16344) | 2025-10 | G | none | manip/real |
| Autonomous Subtask Generation for Indoor Search and Rescue Mission via Large-Language-Model and Behavior-Tree Integration | 2025-10 | G | re-decide | mobile-manip/real |
| LLM-Driven Hierarchical Planning: Long-horizon Task Allocation for Multi-Robot Systems in Cross-Regional Environments | 2025-10 | G | none | multi-robot/real |
| Large Language Model-Based Robot Task Planning from Voice Command Transcriptions | 2025-10 | C | none | mobile-manip/real |
| ROD-VLM: A Framework of Real-time Robotic Perception, Reasoning and Manipulation | 2025-10 | G | re-decide | manip/real |
| Towards Extrinsic Dexterity Grasping in Unrestricted Environments | 2025-10 | G | none | manip/sim+real |
| VLIN-RL: A Unified Vision-Language Interpreter and Reinforcement Learning Motion Planner Framework for Robot Dynamic Tasks | 2025-10 | G | none | manip/sim |
| AI-Enhanced Rescue Drone with Multi-Modal Vision and Cognitive Agentic Architecture | 2025-10 | G | none | aerial/real |
| [Intent-Driven LLM Ensemble Planning for Flexible Multi-Robot Disassembly: Demonstration on EV Batteries](https://arxiv.org/abs/2510.17576) | 2025-10 | G | none | multi-robot/real |
| LLMs augmented hierarchical reinforcement learning with action primitives for long-horizon manipulation tasks | 2025-10 | G | none | manip/sim |
| EmbodiedFly: Embodied LLM Agent with an Autonomous Reconfigurable Drone | 2025-10 | G | re-decide | aerial/real |
| [Hierarchical DLO Routing with Reinforcement Learning and In-Context Vision-Language Models](https://arxiv.org/abs/2510.19268) | 2025-10 | G | re-decide | manip/sim+real |
| [CGoT: A Novel Inference Mechanism for Embodied Multi-Agent Systems Using Composable Graphs of Thoughts](https://arxiv.org/abs/2510.22235) | 2025-10 | G | none | multi-robot/sim |
| [PIP-LLM: Integrating PDDL-Integer Programming with LLMs for Coordinating Multi-Robot Teams Using Natural Language](https://arxiv.org/abs/2510.22784) | 2025-10 | G | none | multi-robot/sim |
| [Endowing GPT-4 with a Humanoid Body: Building the Bridge Between Off-the-Shelf VLMs and the Physical World](https://arxiv.org/abs/2511.00041) | 2025-10 | G | none | humanoid/sim |
| [PFEA: An LLM-based High-Level Natural Language Planning and Feedback Embodied Agent for Human-Centered AI](https://arxiv.org/abs/2510.24109) | 2025-10 | G | re-decide | manip/real |
| Large language model-based copilot for planning and executing of co-active USAR missions using actionable semantic scene graphs | 2025-10 | G | none | mobile-manip/sim+real |
| [Heterogeneous Robot Collaboration in Unstructured Environments with Grounded Generative Intelligence](https://arxiv.org/abs/2510.26915) | 2025-10 | G | re-decide | multi-robot/sim+real |
| [Kinodynamic Task and Motion Planning using VLM-guided and Interleaved Sampling](https://arxiv.org/abs/2510.26139) | 2025-10 | G | none | manip/sim+real |
| [Toward Accurate Long-Horizon Robotic Manipulation: Language-to-Action with Foundation Models via Scene Graphs](https://arxiv.org/abs/2510.27558) | 2025-10 | G | re-decide | manip/real |
| DreamArrangement: Learning Language-Conditioned Robotic Rearrangement of Objects via Denoising Diffusion and VLM Planner | 2025-11 | G | none | manip/sim |
| LLM-MTMP: A large language model-based multi-agent task and motion planning framework for power inspection robots | 2025-11 | G | none | mobile-manip/real |
| Prompt2Act: Mapping prompts into sequence of robotic actions with large foundation models | 2025-11 | G | none | manip/sim |
| [AERMANI-VLM: Structured Prompting and Reasoning for Aerial Manipulation with Vision Language Models](https://arxiv.org/abs/2511.01472) | 2025-11 | G | none | aerial/sim+real |
| [Text to Robotic Assembly of Multi Component Objects using 3D Generative AI and Vision Language Models](https://arxiv.org/abs/2511.02162) | 2025-11 | G | none | manip/real |
| [VLM-Driven Skill Selection for Robotic Assembly Tasks](https://arxiv.org/abs/2511.05680) | 2025-11 | G | none | manip/sim |
| [CoFineLLM: Conformal Finetuning of LLMs for Language-Instructed Robot Planning](https://arxiv.org/abs/2511.06575) | 2025-11 | C | none | manip/sim |
| A Framework for Embodied Intelligence Assembly Robots Co-driven by Large-scale Model and Small-scale Models | 2025-11 | G | none | manip/real |
| [AdaptPNP: Integrating Prehensile and Non-Prehensile Skills for Adaptive Robotic Manipulation](https://arxiv.org/abs/2511.11052) | 2025-11 | G | none | manip/sim+real |
| [Searching in Space and Time: Unified Memory-Action Loops for Open-World Object Retrieval](https://arxiv.org/abs/2511.14004) | 2025-11 | G | re-decide | mobile-manip/sim+real |
| [ArtiBench and ArtiBrain: Benchmarking Generalizable Vision-Language Articulated Object Manipulation](https://arxiv.org/abs/2511.20330) | 2025-11 | G | re-decide | manip/sim+real |
| Enhancing Collaborative Robotics through Large Language Model Integration: A Vision-Guided Approach Using ROS MCP Server | 2025-11 | G | re-decide | manip/real |
| [Quadrupped-Legged Robot Movement Plan Generation using Large Language Model](https://arxiv.org/abs/2512.21293) | 2025-11 | G | none | loco/real |
| A Resilient LLM-driven Agent Framework for Multi-UAV Mission Planning and Control | 2025-11 | G | re-decide | aerial/sim |
| [BINDER: Instantly Adaptive Mobile Manipulation with Open-Vocabulary Commands](https://arxiv.org/abs/2511.22364) | 2025-11 | G | re-decide | mobile-manip/sim+real |
| Embodied Multi-Agent Planning With LLMs: A Best-of-N Strategy for Efficient Cooperation | 2025-11 | G | re-decide | multi-robot/sim |
| [Transforming Monolithic Foundation Models into Embodied Multi-Agent Architectures for Human-Robot Collaboration](https://arxiv.org/abs/2512.00797) | 2025-11 | G | re-decide | mobile-manip/real |
| A Large Language Model-Driven Multi-Agent Human-Machine Interaction Framework | 2025-12 | G | re-decide | multi-robot/real |
| From Speech to Action: Design and Implementation of a Multimodal Robotic Grasping System Driven by Large Language Models | 2025-12 | G | none | manip/real |
| Joint Knowledge Graph Reasoning and Large Language Models for Hierarchical Task Planning | 2025-12 | G | none | other/sim |
| Multimodal-Driven Intelligent Grasping Decision System: A Semantic-Visual-Physical End-to-End Collaborative Architecture | 2025-12 | G | none | manip/real |
| VLC: A Human-Robot-Collaboration Framework with Vision-Language-Model | 2025-12 | G | none | manip/real |
| [Chat with UAV – human-UAV interaction based on large language models](https://arxiv.org/abs/2512.08145) | 2025-12 | G | re-decide | aerial/sim |
| [Embodied Tree of Thoughts: Deliberate Manipulation Planning With Embodied World Model](https://arxiv.org/abs/2512.08188) `real2sim2real` | 2025-12 | G | re-decide | manip/sim+real |
| [Scene-agnostic Hierarchical Bimanual Task Planning via Visual Affordance Reasoning](https://arxiv.org/abs/2512.09310) | 2025-12 | G | none | manip/sim+real |
| [LEO-RobotAgent: A General-purpose Robotic Agent for Language-driven Embodied Operator](https://arxiv.org/abs/2512.10605) | 2025-12 | G | re-decide | other/sim+real |
| [Architecting Large Action Models for Human-in-the-Loop Intelligent Robots](https://arxiv.org/abs/2512.11620) | 2025-12 | G | none | mobile-manip/real |
| [Towards Logic-Aware Manipulation: A Knowledge Primitive for VLM-Based Assistants in Smart Manufacturing](https://arxiv.org/abs/2512.11275) | 2025-12 | G | none | manip/real |
| A framework for reconfigurable production line changeover task planning based on large language model | 2025-12 | G | none | manip/sim |
| [Lang2manip: A Tool for LLM-Based Symbolic-To-Geometric Planning for Manipulation](https://arxiv.org/abs/2512.17062) | 2025-12 | G | none | manip/sim |
| [Vision-Language-Policy Model for Dynamic Robot Task Planning](https://arxiv.org/abs/2512.19178) | 2025-12 | C | re-decide | manip/real |
| [LookPlanGraph: Embodied Instruction Following Method with VLM Graph Augmentation](https://arxiv.org/abs/2512.21243) | 2025-12 | G | re-decide | mobile-manip/sim |
| [HELP: Hierarchical Embodied Language Planner for Household Tasks](https://arxiv.org/abs/2512.21723) | 2025-12 | G | none | mobile-manip/sim+real |
| [D-RMGPT: Robot-assisted collaborative tasks driven by large multimodal models](https://arxiv.org/abs/2408.11761) | 2026-04 | G | re-decide | manip/real |
| [Can only LLMs do Reasoning?: Potential of Small Language Models in Task Planning](https://arxiv.org/abs/2404.03891) | 2026-06 | C | none | manip/real |

</details>

<details><summary><b>Controller · Direct drivers</b> (177)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| How to Tidy Up a Table: Fusing Visual and Semantic Commonsense Reasoning for Robotic Tasks with Vague Objectives | 2023 | G | none | manip/sim+real |
| Integrating Common Sense and Planning with Large Language Models for Room Tidying | 2023 | G | none | mobile-manip/sim |
| Leveraging Commonsense Knowledge from Large Language Models for Task and Motion Planning | 2023 | G | none | mobile-manip/sim+real |
| Make a Donut: Language-Guided Hierarchical EMD-Space Planning for Zero-shot Deformable Object Manipulation | 2023 | G | authored | manip/sim |
| [Robot Behavior-Tree-Based Task Generation with Large Language Models](https://arxiv.org/abs/2302.12927) | 2023-02 | G | none | manip/sim |
| [Task and Motion Planning with Large Language Models for Object Rearrangement](https://arxiv.org/abs/2303.06247) | 2023-03 | G | none | mobile-manip/sim+real |
| [LLM+P: Empowering Large Language Models with Optimal Planning Proficiency](https://arxiv.org/abs/2304.11477) | 2023-04 | G | none | manip/sim |
| [Energy-based Models are Zero-Shot Planners for Compositional Scene Rearrangement](https://arxiv.org/abs/2304.14391) | 2023-04 | G | none | manip/sim+real |
| [Instruct2Act: Mapping Multi-modality Instructions to Robotic Actions with Large Language Model](https://arxiv.org/abs/2305.11176) | 2023-05 | G | none | manip/sim+real |
| [Demo2Code: From Summarizing Demonstrations to Synthesizing Code via Extended Chain-of-Thought](https://arxiv.org/abs/2305.16744) | 2023-05 | G | none | manip/sim |
| [SayTap: Language to Quadrupedal Locomotion](https://arxiv.org/abs/2306.07580) | 2023-06 | G | none | loco/sim+real |
| [Statler: State-Maintaining Language Models for Embodied Reasoning](https://arxiv.org/abs/2306.17840) | 2023-06 | G | none | manip/sim |
| ["Tidy Up the Table": Grounding Common-sense Objective for Tabletop Object Rearrangement](https://arxiv.org/abs/2307.11319) | 2023-07 | G | none | manip/sim+real |
| [Ground Manipulator Primitive Tasks to Executable Actions using Large Language Models](https://arxiv.org/abs/2308.06810) | 2023-08 | G | none | manip/sim |
| ProgPrompt: program generation for situated robot task planning using large language models | 2023-08 | G | authored | manip/sim+real |
| [LGMCTS: Language-Guided Monte-Carlo Tree Search for Executable Semantic Object Rearrangement](https://arxiv.org/abs/2309.15821) | 2023-09 | G | none | manip/sim+real |
| [Cook2LTL: Translating Cooking Recipes to LTL Formulae using Large Language Models](https://arxiv.org/abs/2310.00163) | 2023-09 | G | none | manip/sim |
| [Generalizable Long-Horizon Manipulations with Large Language Models](https://arxiv.org/abs/2310.02264) | 2023-10 | G | authored | manip/sim+real |
| [LAN-grasp: Using Large Language Models for Semantic Object Grasping](https://arxiv.org/abs/2310.05239) | 2023-10 | G | none | manip/real |
| [Language Models as Zero-Shot Trajectory Generators](https://arxiv.org/abs/2310.11604) | 2023-10 | G | none | manip/real |
| [Creative Robot Tool Use with Large Language Models](https://arxiv.org/abs/2310.13065) | 2023-10 | G | none | manip/sim+real |
| [Make a Donut: Hierarchical EMD-Space Planning for Zero-Shot Deformable Manipulation With Tools](https://arxiv.org/abs/2311.02787) | 2023-11 | G | authored | manip/sim |
| Boosting Robot Intelligence in Practice: Enhancing Robot Task Planning with Large Language Models | 2023-11 | G | none | manip/real |
| [SAGE: Bridging Semantic and Actionable Parts for GEneralizable Manipulation of Articulated Objects](https://arxiv.org/abs/2312.01307) | 2023-12 | G | re-decide | manip/sim+real |
| A Smart Interactive Camera Robot Based on Large Language Models | 2023-12 | G | none | manip/real |
| Robot Behavior Tree Manipulation Using Language Models | 2023-12 | G | none | manip/real |
| [DiffVL: Scaling Up Soft Body Manipulation using Vision-Language Driven Differentiable Physics](https://arxiv.org/abs/2312.06408) | 2023-12 | G | none | manip/sim |
| [From text to motion: grounding GPT-4 in a humanoid robot “Alter3”](https://arxiv.org/abs/2312.06571) | 2023-12 | G | re-decide | humanoid/real |
| LLM-based Skill Diffusion for Zero-shot Policy Adaptation | 2024 | G | authored | manip/sim |
| Open-World Task and Motion Planning via Vision-Language Model Inferred Constraints | 2024 | G | none | manip/sim+real |
| Teaching Robots with Show and Tell: Using Foundation Models to Synthesize Robot Policies from Language and Visual Demonstration | 2024 | G | none | manip/real |
| Embodied intelligence in manufacturing: leveraging large language models for autonomous industrial robotics | 2024-01 | G | none | manip/sim+real |
| [A Study on Training and Developing Large Language Models for Behavior Tree Generation](https://arxiv.org/abs/2401.08089) | 2024-01 | C | none | manip/sim |
| [Training microrobots to swim by a large language model](https://arxiv.org/abs/2402.00044) | 2024-01 | G | re-decide | other/sim |
| [Generative Expressive Robot Behaviors using Large Language Models](https://arxiv.org/abs/2401.14673) | 2024-01 | G | re-decide | social/sim+real |
| [InCoRo: In-Context Learning for Robotics Control with Feedback Loops](https://arxiv.org/abs/2402.05188) | 2024-02 | G | re-decide | manip/sim |
| [Learning to Learn Faster from Human Feedback with Language Model Predictive Control](https://arxiv.org/abs/2402.11450) | 2024-02 | C | re-decide | mobile-manip/sim+real |
| [RoboScript: Code Generation for Free-Form Manipulation Tasks across Real and Simulation](https://arxiv.org/abs/2402.14623) `sim2real` | 2024-02 | G | none | manip/sim+real |
| [RoboCodeX: Multimodal Code Generation for Robotic Behavior Synthesis](https://arxiv.org/abs/2402.16117) | 2024-02 | C | none | manip/sim+real |
| Integrating ChatGPT with Blockly for End-User Development of Robot Tasks | 2024-03 | G | none | manip/real |
| Language, Camera, Autonomy! Prompt-engineered Robot Control for Rapidly Evolving Deployment | 2024-03 | G | re-decide | other/sim+real |
| ChatSTL: A Framework of Translation from Natural Language to Signal Temporal Logic Specifications for Autonomous Vehicle Navigation out of Blocked Scenarios | 2024-03 | G | none | driving/sim |
| [ExploRLLM: Guiding Exploration in Reinforcement Learning with Large Language Models](https://arxiv.org/abs/2403.09583) `sim2real` | 2024-03 | G | none | manip/sim+real |
| [NARRATE: Versatile Language Architecture for Optimal Control in Robotics](https://arxiv.org/abs/2403.10762) | 2024-03 | G | authored | manip/sim |
| [Context-aware LLM-based Safe Control Against Latent Risks](https://arxiv.org/abs/2403.11863) | 2024-03 | G | re-decide | other/sim |
| [Natural Language as Policies: Reasoning for Coordinate-Level Embodied Control with LLMs](https://arxiv.org/abs/2403.13801) | 2024-03 | G | none | manip/sim |
| [ShapeGrasp: Zero-Shot Task-Oriented Grasping with Large Language Models through Geometric Decomposition](https://arxiv.org/abs/2403.18062) | 2024-03 | G | none | manip/real |
| [Language Models are Spacecraft Operators](https://arxiv.org/abs/2404.00413) | 2024-03 | C | re-decide | other/sim |
| [RoboMP2: A Robotic Multimodal Perception-Planning Framework with Multimodal Large Language Models](https://arxiv.org/abs/2404.04929) | 2024-04 | G | none | manip/sim+real |
| [GenCHiP: Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks](https://arxiv.org/abs/2404.06645) | 2024-04 | G | none | manip/sim+real |
| [Empowering Large Language Models on Robotic Manipulation with Affordance Prompting](https://arxiv.org/abs/2404.11027) | 2024-04 | G | none | manip/sim |
| Implementation method of collaborative unmanned aerial vehicle simulation system for large language model construction | 2024-05 | G | none | multi-robot/sim |
| [SuFIA: Language-Guided Augmented Dexterity for Robotic Surgical Assistants](https://arxiv.org/abs/2405.05226) | 2024-05 | G | re-decide | manip/sim+real |
| [Bi-VLA: Vision-Language-Action Model-Based System for Bimanual Robotic Dexterous Manipulations](https://arxiv.org/abs/2405.06039) | 2024-05 | G | none | manip/real |
| [FlockGPT: Guiding UAV Flocking with Linguistic Orchestration](https://arxiv.org/abs/2405.05872) | 2024-05 | G | re-decide | multi-robot/sim |
| How to Prompt Your Robot: A PromptBook for Manipulation Skills with Code as Policies | 2024-05 | G | none | mobile-manip/real |
| [Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human Instructions](https://arxiv.org/abs/2405.07474) | 2024-05 | G | none | mobile-manip/sim+real |
| [Toward Automated Programming for Robotic Assembly Using ChatGPT](https://arxiv.org/abs/2405.08216) `sim2real` | 2024-05 | G | re-decide | manip/sim+real |
| [Meta-Control: Automatic Model-based Control Synthesis for Heterogeneous Robot Skills](https://arxiv.org/abs/2405.11380) | 2024-05 | G | authored | manip/sim+real |
| Complex Motion Planning for Quadruped Robots Using Large Language Models | 2024-05 | G | none | loco/real |
| [Trust the PRoC3S: Solving Long-Horizon Robotics Problems with LLMs and Constraint Satisfaction](https://arxiv.org/abs/2406.05572) | 2024-06 | G | re-decide | manip/sim+real |
| [LLM-Craft: Robotic Crafting of Elasto-Plastic Objects With Large Language Models](https://arxiv.org/abs/2406.08648) | 2024-06 | G | re-decide | manip/sim |
| [DISCO: Language-Guided Manipulation With Diffusion Policies and Constrained Inpainting](https://arxiv.org/abs/2406.09767) | 2024-06 | G | none | manip/sim+real |
| [GPT-Fabric: Folding and Smoothing Fabric by Leveraging Pre-Trained Foundation Models](https://arxiv.org/abs/2406.09640) | 2024-06 | G | re-decide | manip/sim+real |
| [Enabling robots to follow abstract instructions and complete complex dynamic tasks](https://arxiv.org/abs/2406.11231) | 2024-06 | G | none | manip/real |
| TPML: Task Planning for Multi-UAV System with Large Language Models `sim2real` | 2024-06 | G | none | aerial/sim+real |
| [Enhancing the LLM-Based Robot Manipulation Through Human-Robot Collaboration](https://arxiv.org/abs/2406.14097) | 2024-06 | G | none | mobile-manip/real |
| [ThinkGrasp: A Vision-Language System for Strategic Part Grasping in Clutter](https://arxiv.org/abs/2407.11298) | 2024-07 | G | re-decide | manip/sim+real |
| [Words2Contact: Identifying Support Contacts from Verbal Instructions Using Foundation Models](https://arxiv.org/abs/2407.14229) | 2024-07 | G | re-decide | humanoid/real |
| [ReplanVLM: Replanning Robotic Tasks With Visual Language Models](https://arxiv.org/abs/2407.21762) | 2024-07 | G | re-decide | manip/sim+real |
| [Text2Interaction: Establishing Safe and Preferable Human-Robot Interaction](https://arxiv.org/abs/2408.06105) | 2024-08 | G | none | manip/real |
| [Nl2Hltl2Plan: Scaling Up Natural Language Understanding for Multi-Robots Through Hierarchical Temporal Logic Task Representation](https://arxiv.org/abs/2408.08188) | 2024-08 | G | none | multi-robot/sim |
| Vision-language model-driven scene understanding and robotic object manipulation | 2024-08 | G | none | manip/real |
| Formal Instruction Convertor Using Large Language Models for Task Execution in Robotic Environments | 2024-09 | G | none | other/sim |
| [Hierarchical LLMs in-the-Loop Optimization for Real-Time Multi-Robot Target Tracking Under Unknown Hazards](https://arxiv.org/abs/2409.12274) | 2024-09 | G | re-decide | multi-robot/sim |
| [Discovering Object Attributes by Prompting Large Language Models With Perception-Action Apis](https://arxiv.org/abs/2409.15505) | 2024-09 | G | none | mobile-manip/sim+real |
| [Scene Exploration by Vision-Language Models](https://arxiv.org/abs/2409.17641) | 2024-09 | G | re-decide | manip/real |
| [UniAff: A Unified Representation of Affordances for Tool Usage and Articulation with Vision-Language Models](https://arxiv.org/abs/2409.20551) | 2024-09 | C | none | manip/sim+real |
| Leveraging large language models for comprehensive locomotion control in humanoid robots design | 2024-10 | G | none | humanoid/sim |
| [Validation of the Scientific Literature via Chemputation Augmented by Large Language Models](https://arxiv.org/abs/2410.06384) `sim2real` | 2024-10 | G | none | other/real |
| [Exploring Spatial Representation to Enhance LLM Reasoning in Aerial Vision-Language Navigation](https://arxiv.org/abs/2410.08500) | 2024-10 | G | re-decide | aerial/sim+real |
| [LLM2Swarm: Robot Swarms that Responsively Reason, Plan, and Collaborate through LLMs](https://arxiv.org/abs/2410.11387) | 2024-10 | G | re-decide | multi-robot/sim |
| [Harmon: Whole-Body Motion Generation of Humanoid Robots from Language Descriptions](https://arxiv.org/abs/2410.12773) | 2024-10 | G | none | humanoid/sim+real |
| Paraphrasing Method for Controlling a Robotic Arm Using a Large Language Model | 2024-10 | G | none | manip/sim |
| [EMOTION: Expressive Motion Sequence Generation for Humanoid Robots With In-Context Learning](https://arxiv.org/abs/2410.23234) | 2024-10 | G | none | social/real |
| [Sampling-Based Model Predictive Control for Dexterous Manipulation on a Biomimetic Tendon-Driven Hand](https://arxiv.org/abs/2411.06183) | 2024-11 | G | re-decide | manip/sim+real |
| [Open-World Task and Motion Planning via Vision-Language Model Generated Constraints](https://arxiv.org/abs/2411.08253) | 2024-11 | G | none | manip/sim+real |
| [MALMM: Multi-Agent Large Language Models for Zero-Shot Robotic Manipulation](https://arxiv.org/abs/2411.17636) | 2024-11 | G | re-decide | manip/sim+real |
| [TalkWithMachines: Enhancing Human-Robot Interaction Through Large/Vision Language Models](https://arxiv.org/abs/2412.15462) | 2024-12 | G | none | manip/sim+real |
| Improving Few-Shot Code Generation with Prompt Selection and Augmentation Techniques in Large Language Models | 2024-12 | G | none | manip/sim |
| Embodied large language models enable robots to complete long-horizon tasks in unpredictable settings | 2025 | G | none | manip/real |
| Grounded Vision-Language Interpreter for Integrated Task and Motion Planning | 2025 | G | re-decide | manip/sim |
| InstructFlow: Adaptive Symbolic Constraint-Guided Code Generation for Long-Horizon Planning | 2025 | G | re-decide | manip/sim |
| Task Decomposition and Self-Evaluation Mechanisms for Home Healthcare Robots Using Large Language Models | 2025 | G | none | manip/real |
| ZLATTE: A Geometry-Aware, Learning-Free Framework for Language-Driven Trajectory Reshaping in Human-Robot Interaction | 2025 | G | none | manip/real |
| LLM-controller: Dynamic robot control adaptation using large language models | 2025-01 | G | re-decide | manip/sim |
| [VLM-driven Behavior Tree for Context-aware Task Planning](https://arxiv.org/abs/2501.03968) | 2025-01 | G | authored | humanoid/real |
| LLM Closed-Loop Application Framework for Industry Manipulator System | 2025-01 | G | re-decide | manip/real |
| [GeoManip: Geometric Constraints as General Interfaces for Robot Manipulation](https://arxiv.org/abs/2501.09783) | 2025-01 | G | re-decide | manip/sim+real |
| [Large Models in Dialogue for Active Perception and Anomaly Detection](https://arxiv.org/abs/2501.16300) | 2025-01 | G | re-decide | aerial/sim |
| [3D-Grounded Vision-Language Framework for Robotic Task Planning: Automated Prompt Synthesis and Supervised Reasoning](https://arxiv.org/abs/2502.08903) | 2025-02 | G | none | manip/real |
| [GSCE: a Prompt Framework With Enhanced Reasoning for Reliable LLM-Driven Drone Control](https://arxiv.org/abs/2502.12531) | 2025-02 | G | none | aerial/sim |
| [Xpress: A System for Dynamic, Context-Aware Robot Facial Expressions Using Language Models](https://arxiv.org/abs/2503.00283) | 2025-03 | G | none | social/real |
| [Code-as-Symbolic-Planner: Foundation Model-Based Robot Planning via Symbolic Code Generation](https://arxiv.org/abs/2503.01700) | 2025-03 | G | re-decide | manip/sim+real |
| [Bridging VLM and KMP: Enabling Fine-Grained Robotic Manipulation via Semantic Keypoints Representation](https://arxiv.org/abs/2503.02748) | 2025-03 | G | none | manip/real |
| MARCER: Multimodal Augmented Reality for Composing and Executing Robot Tasks | 2025-03 | G | none | mobile-manip/real |
| [AutoMisty: A Multi-Agent LLM Framework for Automated Code Generation in the Misty Social Robot](https://arxiv.org/abs/2503.06791) | 2025-03 | G | re-decide | social/real |
| [Multi-Agent LLM Actor-Critic Framework for Social Robot Navigation](https://arxiv.org/abs/2503.09758) | 2025-03 | G | re-decide | multi-robot/sim |
| [IMPACT: Intelligent Motion Planning with Acceptable Contact Trajectories via Vision-Language Models](https://arxiv.org/abs/2503.10110) | 2025-03 | G | none | manip/sim+real |
| [KUDA: Keypoints to Unify Dynamics Learning and Visual Prompting for Open-Vocabulary Robotic Manipulation](https://arxiv.org/abs/2503.10546) | 2025-03 | G | authored | manip/real |
| Embodied large language models enable robots to complete complex tasks in unpredictable environments | 2025-03 | G | authored | manip/real |
| [LLM+MAP: Bimanual Robot Task Planning using Large Language Models and Planning Domain Definition Language](https://arxiv.org/abs/2503.17309) | 2025-03 | G | none | manip/sim |
| Text2RLab: No-Code Methodology for Robotic Programming and Interaction in Laboratory Tasks | 2025-03 | G | none | manip/real |
| [Robotic Long-Horizon Manipulation with Progressive In-Context Code Generation and Episodic Feedback](https://arxiv.org/abs/2503.21969) | 2025-03 | G | re-decide | manip/sim+real |
| [Physically Ground Commonsense Knowledge for Articulated Object Manipulation with Analytic Concepts](https://arxiv.org/abs/2503.23348) | 2025-03 | G | none | manip/sim+real |
| [GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models](https://arxiv.org/abs/2503.23875) | 2025-03 | G | authored | multi-robot/sim+real |
| [KeyMPs: One-Shot Vision-Language Guided Motion Generation by Sequencing DMPs for Occlusion-Rich Tasks](https://arxiv.org/abs/2504.10011) | 2025-04 | G | none | manip/sim+real |
| [Trajectory Adaptation using Large Language Models](https://arxiv.org/abs/2504.12755) | 2025-04 | G | none | manip/sim |
| Formation control and path planning of multi-robot systems via large language models | 2025-04 | G | none | multi-robot/sim |
| [Robotic Visual Instruction](https://arxiv.org/abs/2505.00693) | 2025-05 | G | none | manip/sim+real |
| [Meta-Optimization and Program Search using Language Models for Task and Motion Planning](https://arxiv.org/abs/2505.03725) | 2025-05 | G | none | manip/sim+real |
| An End-to-End GPT-4o Informed Pipeline for Manipulation Task Planning with Sim2Real Validation `sim2real` | 2025-05 | G | none | manip/sim+real |
| [Unfettered Forceful Skill Acquisition with Physical Reasoning and Coordinate Frame Labeling](https://arxiv.org/abs/2505.09731) | 2025-05 | G | re-decide | manip/real |
| Here's your PDDL Problem File! On Using VLMs for Generating Symbolic PDDL Problem Files | 2025-05 | G | re-decide | manip/sim+real |
| [Grounded Vision-Language Interpreter for Long-Horizon Bimanual Task and Motion Planning](https://arxiv.org/abs/2506.03270) | 2025-06 | G | re-decide | manip/sim+real |
| [Language-Grounded Hierarchical Planning and Execution with Multi-Robot 3D Scene Graphs](https://arxiv.org/abs/2506.07454) | 2025-06 | G | none | multi-robot/real |
| Robots reading recipes: large language models as translators between humans and machines | 2025-06 | G | none | manip/sim |
| [CodeDiffuser: Attention-Enhanced Diffusion Policy via VLM-Generated Code for Instruction Ambiguity](https://arxiv.org/abs/2506.16652) | 2025-06 | G | none | manip/sim+real |
| [FrankenBot: Brain-Morphic Modular Orchestration for Robotic Manipulation with Vision-Language Models](https://arxiv.org/abs/2506.21627) | 2025-06 | G | re-decide | manip/sim+real |
| [T-Rex: Task-Adaptive Spatial Representation Extraction for Robotic Manipulation with Vision-Language Models](https://arxiv.org/abs/2506.19498) | 2025-06 | G | none | manip/sim+real |
| [An LLM-powered Natural-to-Robotic Language Translation Framework with Correctness Guarantees](https://arxiv.org/abs/2508.19074) | 2025-06 | C | none | manip/sim |
| [Large Language Model-Driven Closed-Loop UAV Operation With Semantic Observations](https://arxiv.org/abs/2507.01930) | 2025-07 | G | re-decide | aerial/sim |
| [Structured Task Solving via Modular Embodied Intelligence: A Case Study on Rubik's Cube](https://arxiv.org/abs/2507.05607) `sim2real` | 2025-07 | G | none | manip/sim+real |
| Empowering Universal Robot Programming with Fine-Tuned Large Language Models | 2025-07 | C | none | manip/real |
| [Compositional Coordination for Multi-Robot Teams with Large Language Models](https://arxiv.org/abs/2507.16068) | 2025-07 | G | authored | multi-robot/sim+real |
| [FMimic: Foundation Models are Fine-grained Action Learners from Human Videos](https://arxiv.org/abs/2507.20622) | 2025-07 | G | none | manip/sim+real |
| Behavior tree generation and adaptation for a social robot control with LLMs | 2025-08 | G | re-decide | social/real |
| Context-Aware Autonomous Drone Navigation Using Large Language Models (LLMs) | 2025-08 | G | none | aerial/sim |
| [HyCodePolicy: Hybrid Language Controllers for Multimodal Monitoring and Decision in Embodied Agents](https://arxiv.org/abs/2508.02629) | 2025-08 | G | re-decide | manip/sim |
| [Triple-S: A Collaborative Multi-LLM Framework for Solving Long-Horizon Implicative Tasks in Robotics](https://arxiv.org/abs/2508.07421) | 2025-08 | G | re-decide | manip/sim+real |
| [Rational Inverse Reasoning](https://arxiv.org/abs/2508.08983) | 2025-08 | G | re-decide | manip/sim |
| Empowered Smart Manufacturing Based on an Intelligent Robotic Workcell Assistant | 2025-08 | G | none | manip/real |
| A framework for robotic manipulation tasks based on multiple zero shot models | 2025-08 | G | none | manip/sim+real |
| [OVITA: Open-Vocabulary Interpretable Trajectory Adaptations](https://arxiv.org/abs/2508.17260) | 2025-08 | G | none | manip/sim+real |
| Code-BT: A Code-Driven Approach to Behavior Tree Generation for Robot Tasks Planning with Large Language Models | 2025-09 | G | none | manip/sim |
| TypeFly: Low-Latency Drone Planning With Large Language Models | 2025-09 | G | authored | aerial/real |
| [Long-Horizon Visual Imitation Learning via Plan and Code Reflection](https://arxiv.org/abs/2509.05368) | 2025-09 | G | none | manip/sim+real |
| [GELATO: Multi-Instruction Trajectory Reshaping via Geometry-Aware Multiagent-based Orchestration](https://arxiv.org/abs/2509.06031) | 2025-09 | G | none | manip/sim+real |
| [See, Point, Fly: A Learning-Free VLM Framework for Universal Unmanned Aerial Navigation](https://arxiv.org/abs/2509.22653) | 2025-09 | G | none | aerial/sim+real |
| [LLM-GROP: Visually Grounded Robot Task and Motion Planning with Large Language Models](https://arxiv.org/abs/2511.07727) | 2025-10 | G | none | mobile-manip/sim+real |
| [EmbodiedCoder: Parameterized Embodied Mobile Manipulation via Modern Coding Model](https://arxiv.org/abs/2510.06207) | 2025-10 | G | none | mobile-manip/real |
| [Executable Analytic Concepts as the Missing Link Between VLM Insight and Precise Manipulation](https://arxiv.org/abs/2510.07975) | 2025-10 | G | none | manip/sim+real |
| [ManiAgent: An Agentic Framework for General Robotic Manipulation](https://arxiv.org/abs/2510.11660) | 2025-10 | G | re-decide | manip/sim+real |
| Keypoint-Aware RAG for Robotic Manipulation: In-Context Constraint Learning via Large-Scale Retrieval | 2025-10 | G | authored | manip/sim+real |
| LLM-CBT: LLM-Driven Closed-Loop Behavior Tree Planning for Heterogeneous UAV-UGV Swarm Collaboration | 2025-10 | G | re-decide | multi-robot/sim |
| Language-Guided Hierarchical Planning with Scene Graphs for Tabletop Object Rearrangement | 2025-10 | G | none | manip/sim+real |
| Multimodal Autonomous Robotic Long-Horizon Task Planning via Embodied Language Model and Behavior Trees | 2025-10 | G | none | manip/real |
| PACR: Point-Axis Constraint Reasoning for Enhanced Robotic Manipulation with Dexterity and Compliance | 2025-10 | G | re-decide | manip/real |
| [Towards Reliable Code-as-Policies: A Neuro-Symbolic Framework for Embodied Task Planning](https://arxiv.org/abs/2510.21302) | 2025-10 | G | re-decide | manip/sim+real |
| Zero-Shot Robotic Control via Custom LLM Agents: A Lightweight Framework for Embodied Learning | 2025-10 | G | none | manip/real |
| [Using VLM Reasoning to Constrain Task and Motion Planning](https://arxiv.org/abs/2510.25548) | 2025-10 | G | re-decide | manip/sim |
| [Maestro: Orchestrating Robotics Modules with Vision-Language Models for Zero-Shot Generalist Robots](https://arxiv.org/abs/2511.00917) | 2025-11 | G | re-decide | manip/real |
| A Lightweight and Deployable Language-To-Robot Control System Using Modular Llms and Vision Model | 2025-11 | G | none | manip/sim+real |
| [Semantic Glitch: Agency and Artistry in an Autonomous Pixel Cloud](https://arxiv.org/abs/2511.16048) | 2025-11 | G | re-decide | aerial/real |
| [Skypilot: Fine-Tuning LLM with Physical Grounding for AAV Coverage Search](https://arxiv.org/abs/2511.18270) | 2025-11 | C | none | aerial/sim+real |
| [OVAL-Grasp: Open-Vocabulary Affordance Localization for Task Oriented Grasping](https://arxiv.org/abs/2511.20841) | 2025-11 | G | none | mobile-manip/real |
| [LLM-Based Generalizable Hierarchical Task Planning and Execution for Heterogeneous Robot Teams with Event-Driven Replanning](https://arxiv.org/abs/2511.22354) | 2025-11 | G | re-decide | multi-robot/real |
| [Automated Generation of MDPs Using Logic Programming and LLMs for Robotic Applications](https://arxiv.org/abs/2511.23143) | 2025-11 | G | none | social/sim |
| Generating joint sequences with pre-trained LLMs to drive dual-arm nursing robot to perform actions | 2025-12 | G | re-decide | manip/sim |
| [LLM-Driven Corrective Robot Operation Code Generation with Static Text-Based Simulation](https://arxiv.org/abs/2512.02002) | 2025-12 | G | none | manip/sim |
| Language-Guided Predictive Control: Synthesizing Semantic Safety Constraints for Adaptive Navigation | 2025-12 | G | none | multi-robot/sim |
| [Prompt2Craft: Generating Functional Craft Assemblies With LLMs](https://arxiv.org/abs/2512.04568) | 2025-12 | G | none | manip/sim |
| [SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models](https://arxiv.org/abs/2512.05955) `real2sim2real` | 2025-12 | G | re-decide | manip/sim+real |
| MauBa: A Multi-Agent Coordination Framework for Vision-Language-Guided Zero-Shot Control of Unmanned Aerial Vehicles | 2025-12 | G | none | aerial/sim |
| A Multi-Modal Robot Task Planning Framework Based on Environmental Feedback | 2025-12 | G | re-decide | manip/sim |
| Preliminary Study of Automating Spot Control with Large Language Models (LLMs) | 2025-12 | G | none | loco/real |
| [MaP-AVR: A Meta-Action Planner for Agents Leveraging Vision Language Models and Retrieval-Augmented Generation](https://arxiv.org/abs/2512.19453) | 2025-12 | G | none | manip/sim |

</details>

<details><summary><b>Controller · Lifelong / memory agents</b> (28)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| Human-Assisted Continual Robot Learning with Foundation Models | 2023 | G | re-decide | manip/sim+real |
| [Lifelong Robot Learning with Human Assisted Language Planners](https://arxiv.org/abs/2309.14321) | 2023-09 | G | re-decide | manip/sim+real |
| [Growing from Exploration: A self-exploring framework for robots based on foundation models](https://arxiv.org/abs/2401.13462) | 2024-01 | G | re-decide | manip/sim+real |
| [RoboCoder: Robotic Learning from Basic Skills to General Tasks with Large Language Models](https://arxiv.org/abs/2406.03757) | 2024-06 | G | re-decide | other/sim |
| [Continual Robot Skill and Task Learning via Dialogue](https://arxiv.org/abs/2409.03166) | 2024-09 | G | re-decide | manip/sim+real |
| [AlignBot: Aligning VLM-Powered Customized Task Planning with User Reminders Through Fine-Tuning for Household Robots](https://arxiv.org/abs/2409.11905) | 2024-09 | G | re-decide | mobile-manip/real |
| [CLIMB: Language-Guided Continual Learning for Task Planning with Iterative Model Building](https://arxiv.org/abs/2410.13756) | 2024-10 | G | re-decide | manip/sim+real |
| [EnvBridge: Bridging Diverse Environments with Cross-Environment Knowledge Transfer for Embodied AI](https://arxiv.org/abs/2410.16919) | 2024-10 | G | re-decide | manip/sim |
| [VLMimic: Vision Language Models are Visual Imitation Learner for Fine-grained Actions](https://arxiv.org/abs/2410.20927) | 2024-10 | G | re-decide | manip/sim+real |
| [Vocal Sandbox: Continual Learning and Adaptation for Situated Human-Robot Collaboration](https://arxiv.org/abs/2411.02599) | 2024-11 | G | re-decide | manip/real |
| TALKER: A Task-Activated Language Model Based Knowledge-Extension Reasoning System | 2025-02 | G | re-decide | multi-robot/sim |
| [STAR: A Foundation Model-driven Framework for Robust Task Planning and Failure Recovery in Robotic Systems](https://arxiv.org/abs/2503.06060) | 2025-03 | G | re-decide | manip/sim+real |
| UJI-Butler: A Symbolic/Non-symbolic Robotic System that Learns Through Multi-modal Interaction | 2025-03 | G | re-decide | multi-robot/real |
| [REFLEX: Metacognitive Reasoning for Reflective Zero-Shot Robotic Planning with Large Language Models](https://arxiv.org/abs/2505.14899) | 2025-05 | G | re-decide | multi-robot/sim |
| [ILearnRobot: An Interactive Learning-Based Multi-modal Robot with Continuous Improvement](https://arxiv.org/abs/2507.22896) | 2025-06 | G | re-decide | mobile-manip/real |
| [LMPVC and Policy Bank: Adaptive voice control for industrial robots with code generating LLMs and reusable Pythonic policies](https://arxiv.org/abs/2506.22028) | 2025-06 | G | re-decide | manip/sim+real |
| RoboMemory: A Brain-inspired Multi-memory Agentic Framework for Lifelong Learning in Physical Embodied Systems | 2025-07 | G | re-decide | mobile-manip/sim+real |
| [FCRF: Flexible Constructivism Reflection for Long-Horizon Robotic Task Planning with Large Language Models](https://arxiv.org/abs/2507.14975) | 2025-07 | G | re-decide | mobile-manip/sim+real |
| [A Pragmatist Robot: Learning to Plan Tasks by Experiencing the Real World](https://arxiv.org/abs/2507.16713) | 2025-07 | G | re-decide | manip/real |
| [Think, Act, Learn: A Framework for Autonomous Robotic Agents using Closed-Loop Large Language Models](https://arxiv.org/abs/2507.19854) | 2025-07 | G | re-decide | manip/sim |
| [LLM-Driven Self-Refinement for Embodied Drone Task Planning](https://arxiv.org/abs/2508.15501) | 2025-08 | G | re-decide | aerial/sim+real |
| [Growing with Your Embodied Agent: A Human-in-the-Loop Lifelong Code Generation Framework for Long-Horizon Manipulation Skills](https://arxiv.org/abs/2509.18597) | 2025-09 | G | re-decide | manip/sim+real |
| [Memory Transfer Planning: LLM-driven Context-Aware Code Adaptation for Robot Manipulation](https://arxiv.org/abs/2509.24160) | 2025-09 | G | re-decide | manip/sim+real |
| [ViReSkill: Vision-Grounded Replanning with Skill Memory for LLM-Based Planning in Lifelong Robot Learning](https://arxiv.org/abs/2509.24219) | 2025-09 | G | re-decide | manip/sim+real |
| AutoSkill: Hierarchical Open-Ended Skill Acquisition for Long-Horizon Manipulation Tasks via Language-Modulated Rewards | 2025-10 | G | re-decide | manip/sim+real |
| [Learning Affordances at Inference-Time for Vision-Language-Action Models](https://arxiv.org/abs/2510.19752) | 2025-10 | G | re-decide | manip/real |
| [RoboOS-NeXT: A Unified Memory-based Framework for Lifelong, Scalable, and Robust Multi-Robot Collaboration](https://arxiv.org/abs/2510.26536) | 2025-10 | G | re-decide | multi-robot/sim+real |
| [SIL: Symbiotic Interactive Learning for Language-Conditioned Human-Agent Co-Adaptation](https://arxiv.org/abs/2511.05203) | 2025-11 | G | re-decide | manip/sim+real |

</details>

<details><summary><b>VLN and embodied navigation</b> (88)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714) | 2022-10 | G | none | nav/sim+real |
| Lang2LTL: Translating Natural Language Commands to Temporal Robot Task Specification | 2023 | G | none | nav/real |
| [ANSEL Photobot: A Robot Event Photographer with Semantic Intelligence](https://arxiv.org/abs/2302.07931) | 2023-02 | G | none | nav/real |
| [Grounding Complex Natural Language Commands for Temporal Tasks in Unseen Environments](https://arxiv.org/abs/2302.11649) | 2023-02 | G | none | nav/real |
| [LLM as A Robotic Brain: Unifying Egocentric Memory and Control](https://arxiv.org/abs/2304.09349) | 2023-04 | G | re-decide | nav/sim |
| [Tell Me Where to Go: A Composable Framework for Context-Aware Embodied Robot Navigation](https://arxiv.org/abs/2306.09523) | 2023-06 | G | none | nav/real |
| [CorNav: Autonomous Agent with Self-Corrected Planning for Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2306.10322) `vln` | 2023-06 | G | re-decide | nav/sim |
| [DRAGON: A Dialogue-Based Robot for Assistive Navigation With Visual Language Grounding](https://arxiv.org/abs/2307.06924) | 2023-07 | G | none | nav/real |
| [CARTIER: Cartographic lAnguage Reasoning Targeted at Instruction Execution for Robots](https://arxiv.org/abs/2307.11865) | 2023-07 | G | none | nav/sim |
| [A2Nav: Action-Aware Zero-Shot Robot Navigation by Exploiting Vision-and-Language Ability of Foundation Models](https://arxiv.org/abs/2308.07997) | 2023-08 | G | none | nav/sim |
| [DynaCon: Dynamic Robot Planner with Contextual Awareness via LLMs](https://arxiv.org/abs/2309.16031) | 2023-09 | G | none | nav/real |
| [Think, Act, and Ask: Open-World Interactive Personalized Robot Navigation](https://arxiv.org/abs/2310.07968) | 2023-10 | G | re-decide | nav/sim |
| [Language and Sketching: An LLM-driven Interactive Multimodal Multitask Robot Navigation Framework](https://arxiv.org/abs/2311.08244) | 2023-11 | G | none | nav/sim+real |
| [VoroNav: Voronoi-based Zero-shot Object Navigation with Large Language Model](https://arxiv.org/abs/2401.02695) `vln` | 2024-01 | G | none | nav/sim |
| [The Conversation is the Command: Interacting with Real-World Autonomous Robots Through Natural Language](https://arxiv.org/abs/2401.11838) | 2024-01 | G | none | nav/sim+real |
| [OpenFMNav: Towards Open-Set Zero-Shot Object Navigation via Vision-Language Foundation Models](https://arxiv.org/abs/2402.10670) `vln` | 2024-02 | G | none | nav/sim+real |
| [Verifiably Following Complex Robot Instructions with Foundation Models](https://arxiv.org/abs/2402.11498) | 2024-02 | G | authored | nav/real |
| [Multimodal Human-Autonomous Agents Interaction Using Pre-Trained Language and Visual Foundation Models](https://arxiv.org/abs/2403.12273) | 2024-03 | G | none | nav/real |
| [BTGenBot: Behavior Tree Generation for Robotic Tasks with Lightweight LLMs](https://arxiv.org/abs/2403.12761) | 2024-03 | C | none | nav/sim+real |
| [CoNVOI: Context-aware Navigation using Vision Language Models in Outdoor and Indoor Environments](https://arxiv.org/abs/2403.15637) | 2024-03 | G | none | nav/real |
| [3P-LLM: Probabilistic Path Planning using Large Language Model for Autonomous Robot Navigation](https://arxiv.org/abs/2403.18778) | 2024-03 | G | none | nav/sim |
| [IVLMap: Instance-Aware Visual Language Grounding for Consumer Robot Navigation](https://arxiv.org/abs/2403.19336) | 2024-03 | G | none | nav/sim+real |
| [Cognitive Planning for Object Goal Navigation using Generative AI Models](https://arxiv.org/abs/2404.00318) | 2024-03 | G | re-decide | nav/sim |
| [Integrating Disambiguation and User Preferences into Large Language Models for Robot Motion Planning](https://arxiv.org/abs/2404.14547) | 2024-04 | G | none | nav/sim |
| [Open Scene Graphs for Open World Object-Goal Navigation](https://arxiv.org/abs/2508.04678) | 2024-07 | G | re-decide | nav/sim+real |
| [Affordances-Oriented Planning using Foundation Models for Continuous Vision-Language Navigation](https://arxiv.org/abs/2407.05890) `vln` | 2024-07 | G | re-decide | nav/sim |
| [TrustNavGPT: Modeling Uncertainty to Improve Trustworthiness of Audio-Guided LLM-Based Robot Navigation](https://arxiv.org/abs/2408.01867) | 2024-08 | G | re-decide | nav/sim+real |
| [Towards Coarse-grained Visual Language Navigation Task Planning Enhanced by Event Knowledge Graph](https://arxiv.org/abs/2408.02535) | 2024-08 | G | none | nav/sim |
| [Intelligent LiDAR Navigation: Leveraging External Information and Semantic Maps with LLM as Copilot](https://arxiv.org/abs/2409.08493) | 2024-09 | G | none | nav/sim+real |
| [E2Map: Experience-and-Emotion Map for Self-Reflective Robot Navigation with Language Models](https://arxiv.org/abs/2409.10027) | 2024-09 | G | re-decide | nav/sim+real |
| [Hey Robot! Personalizing Robot Navigation Through Model Predictive Control with a Large Language Model](https://arxiv.org/abs/2409.13393) | 2024-09 | G | authored | nav/sim+real |
| [Behav: Behavioral Rule Guided Autonomy Using VLMs for Robot Navigation in Outdoor Scenes](https://arxiv.org/abs/2409.16484) | 2024-09 | G | authored | nav/real |
| [AssistantX: An LLM-Powered Proactive Assistant in Collaborative Human-Populated Environments](https://arxiv.org/abs/2409.17655) | 2024-09 | G | re-decide | nav/real |
| Next‐generation human‐robot interaction with ChatGPT and robot operating system | 2024-09 | G | none | nav/sim |
| [SPINE: Online Semantic Planning for Missions with Incomplete Natural Language Specifications in Unstructured Environments](https://arxiv.org/abs/2410.03035) | 2024-10 | G | re-decide | nav/sim+real |
| [Open-Architecture End-to-End System for Real-World Autonomous Robot Navigation](https://arxiv.org/abs/2410.06239) | 2024-10 | G | re-decide | nav/real |
| Lang2LTL-2: Grounding Spatiotemporal Navigation Commands Using Large Language and Vision-Language Models | 2024-10 | G | none | nav/real |
| [Guide-LLM: An Embodied LLM Agent and Text-Based Topological Map for Robotic Guidance of People with Visual Impairments](https://arxiv.org/abs/2410.20666) | 2024-10 | G | none | nav/sim |
| [FASTNav: Fine-Tuned Adaptive Small-Language- Models Trained for Multi-Point Robot Navigation](https://arxiv.org/abs/2411.13262) | 2024-11 | C | none | nav/sim+real |
| Natural Language Navigation Task Allocation for Robot Based on Agents | 2024-11 | G | none | nav/sim |
| [TANGO: Training-free Embodied AI Agents for Open-world Tasks](https://arxiv.org/abs/2412.10402) | 2024-12 | G | authored | nav/sim |
| Ambiguity Resolution in Vision-and-Language Navigation with Large Language Models | 2024-12 | G | none | nav/sim |
| [CogNav: Cognitive Process Modeling for Object Goal Navigation with LLMs](https://arxiv.org/abs/2412.10439) `vln` | 2024-12 | G | re-decide | nav/sim+real |
| [GraphEQA: Using 3D Semantic Scene Graphs for Real-time Embodied Question Answering](https://arxiv.org/abs/2412.14480) | 2024-12 | G | re-decide | nav/sim+real |
| Embodied AI in Mobile Robot Simulation with EyeSim: Coverage Path Planning with Large Language Models | 2025 | G | none | nav/sim |
| Opportunistic collaboration between heterogeneous agents using an unstructured ontology via GenAI | 2025-01 | G | none | nav/real |
| [Robust Mobile Robot Path Planning via LLM-Based Dynamic Waypoint Generation](https://arxiv.org/abs/2501.15901) | 2025-01 | G | re-decide | nav/sim |
| Enhancing Robotic Navigation with Large Language Models | 2025-02 | G | none | nav/real |
| [VL-Nav: Neuro-Symbolic Reasoning-based Vision-Language Navigation](https://arxiv.org/abs/2502.00931) `vln` | 2025-02 | G | re-decide | nav/sim+real |
| Enhancing Large Language Models with RAG for Visual Language Navigation in Continuous Environments | 2025-02 | G | re-decide | nav/sim |
| Leveraging large language models for autonomous robotic mapping and navigation | 2025-03 | G | none | nav/sim |
| [Safe LLM-Controlled Robots with Formal Guarantees via Reachability Analysis](https://arxiv.org/abs/2503.03911) | 2025-03 | G | none | nav/sim+real |
| [LTLCodeGen: Code Generation of Syntactically Correct Temporal Logic for Robot Task Planning](https://arxiv.org/abs/2503.07902) | 2025-03 | G | none | nav/sim+real |
| [SmartWay: Enhanced Waypoint Prediction and Backtracking for Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2503.10069) `vln` | 2025-03 | G | re-decide | nav/sim+real |
| Integration of Large Language Models for Autonomous Navigation of a Mobile Robot | 2025-04 | G | re-decide | nav/sim |
| [Research on Navigation Methods Based on LLMs](https://arxiv.org/abs/2504.15600) | 2025-04 | G | re-decide | nav/sim |
| [ReLI: Cross-Lingual Language-to-Action Grounding for Human-Robot Interaction](https://arxiv.org/abs/2505.01862) | 2025-05 | C | none | nav/sim+real |
| [Semantic Intelligence: Integrating GPT-4 with A Planning in Low-Cost Robotics](https://arxiv.org/abs/2505.01931) | 2025-05 | G | none | nav/real |
| Fine-Tuning Large Language Models for Mobile Robot Navigation | 2025-05 | C | none | nav/real |
| [Leveraging LLMs for Mission Planning in Precision Agriculture](https://arxiv.org/abs/2506.10093) | 2025-05 | G | none | nav/sim+real |
| [GET: Goal-directed Exploration and Targeting for Large-Scale Unknown Environments](https://arxiv.org/abs/2505.20828) | 2025-05 | G | none | nav/sim |
| LLM-Guided Multi-Agent System for Natural Language-Based Robot Navigation | 2025-05 | G | re-decide | nav/sim |
| [Reducing Latency in LLM-Based Natural Language Commands Processing for Robot Navigation](https://arxiv.org/abs/2506.00075) | 2025-05 | G | none | nav/sim |
| ["Don't Do That!": Guiding Embodied Systems through Large Language Model-based Constraint Generation](https://arxiv.org/abs/2506.04500) | 2025-06 | G | none | nav/sim |
| Leveraging Large Language Models for Modular Robot Navigation | 2025-06 | G | re-decide | nav/sim |
| [Multimodal Spatial Language Maps for Robot Navigation and Manipulation](https://arxiv.org/abs/2506.06862) | 2025-06 | G | none | nav/sim+real |
| [DyNaVLM: Zero-Shot Vision-Language Navigation System with Dynamic Viewpoints and Self-Refining Graph Memory](https://arxiv.org/abs/2506.15096) `vln` | 2025-06 | G | re-decide | nav/sim+real |
| [General-Purpose Robotic Navigation via LVLM-Orchestrated Perception, Reasoning, and Acting](https://arxiv.org/abs/2506.17462) | 2025-06 | G | re-decide | nav/sim |
| Smarter Robots, Fewer Queries: A Knowledge-Driven Approach to Reduce LLM Dependency | 2025-07 | G | re-decide | nav/sim |
| [Enter the Mind Palace: Reasoning and Planning for Long-term Active Embodied Question Answering](https://arxiv.org/abs/2507.12846) | 2025-07 | G | re-decide | nav/sim+real |
| [osmAG-LLM: Zero-Shot Open-Vocabulary Object Navigation via Semantic Maps and Large Language Models Reasoning](https://arxiv.org/abs/2507.12753) | 2025-07 | G | none | nav/sim+real |
| [OpenNav: Open-World Navigation with Multimodal Large Language Models](https://arxiv.org/abs/2507.18033) | 2025-07 | G | authored | nav/sim+real |
| DebateNav: Structured Multi-VLM Expert Debate for Robust Zero-Shot Object Navigation | 2025-08 | G | re-decide | nav/sim |
| Intelligent Indoor Navigation for Home Robots based on Large Language Models | 2025-08 | G | none | nav/real |
| LLM-Powered Embodied Intelligence for Socially-Aware Robot Navigation in Human-Robot Interaction | 2025-08 | C | none | nav/sim |
| ElevNav: Large Language Model-Guided Robot Navigation via 3D Scene Graphs in Elevator Environments | 2025-09 | G | none | nav/real |
| [Plantbot: Integrating Plant and Robot through LLM Modular Agent Networks](https://arxiv.org/abs/2509.05338) | 2025-09 | G | re-decide | nav/real |
| Metareasoning for Edge-Cloud Collaborative LLM Planning for Efficient Autonomous Navigation | 2025-09 | G | none | nav/real |
| Design and Implementation of a Delivery Robot System for Natural Language Interaction | 2025-09 | G | none | nav/real |
| [Human-like Navigation in a World Built for Humans](https://arxiv.org/abs/2509.21189) | 2025-09 | G | re-decide | nav/sim+real |
| Embodied Assistant: Robot Mobility Operations Guided by Open Vocabulary in Open Environments Utilizing LLM | 2025-10 | G | re-decide | nav/sim |
| Generating Robotic Control Strategies With LLMs: Via Human–Robot Voice Interaction | 2025-10 | G | none | nav/real |
| [Multi-Step Reasoning for Embodied Question Answering via Tool Augmentation](https://arxiv.org/abs/2510.20310) | 2025-10 | C | re-decide | nav/sim |
| Instance-Aware Visual Language Grounding for Consumer Robot Navigation | 2025-11 | G | none | nav/sim |
| Large Language Model as a Strategic Brain: Autonomous Selection of Path-Planning Algorithms for Mobile Robots | 2025-11 | G | none | nav/sim |
| [TP-MDDN: Task-Preferenced Multi-Demand-Driven Navigation with Autonomous Decision-Making](https://arxiv.org/abs/2511.17225) | 2025-11 | G | re-decide | nav/sim |
| [Vision to Geometry: 3D Spatial Memory for Sequential Embodied MLLM Reasoning and Exploration](https://arxiv.org/abs/2512.02458) | 2025-12 | G | none | nav/sim |
| GROOT: GPT-based Human-RObOT Interface | 2025-12 | G | none | nav/sim |

</details>

<details><summary><b>Supervisor</b> (36)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Robot Task Planning and Situation Handling in Open Worlds](https://arxiv.org/abs/2210.01287) | 2022-10 | G | none | mobile-manip/sim+real |
| HiCRISP: A Hierarchical Closed-Loop Robotic Intelligent Self-Correction Planner | 2023 | G | re-decide | manip/sim+real |
| [Integrating action knowledge and LLMs for task planning and situation handling in open worlds](https://arxiv.org/abs/2305.17590) | 2023-05 | G | none | mobile-manip/sim+real |
| Large Language Models to the Rescue: Deadlock Resolution in Multi-Robot Systems | 2024 | G | none | multi-robot/sim |
| [Foundation Models to the Rescue: Deadlock Resolution in Connected Multi-Robot Systems](https://arxiv.org/abs/2404.06413) | 2024-04 | G | none | multi-robot/sim |
| [VADER: Visual Affordance Detection and Error Recovery for Multi Robot Human Collaboration](https://arxiv.org/abs/2405.16021) | 2024-05 | G | re-decide | multi-robot/real |
| [Evaluating Uncertainty-based Failure Detection for Closed-Loop LLM Planners](https://arxiv.org/abs/2406.00430) | 2024-06 | G | re-decide | manip/sim |
| [DKPROMPT: Domain Knowledge Prompting Vision-Language Models for Open-World Planning](https://arxiv.org/abs/2406.17659) | 2024-06 | G | re-decide | mobile-manip/sim |
| [Robot Failure Recovery Using Vision-Language Models With Optimized Prompts](https://arxiv.org/abs/2409.03966) | 2024-09 | G | re-decide | manip/sim+real |
| [Automatic Behavior Tree Expansion with LLMs for Robotic Manipulation](https://arxiv.org/abs/2409.13356) | 2024-09 | G | re-decide | manip/sim |
| [Updating Robot Safety Representations Online From Natural Language Feedback](https://arxiv.org/abs/2409.14580) | 2024-09 | G | re-decide | nav/sim+real |
| Ensuring Safety in LLM-Driven Robotics: A Cross-Layer Sequence Supervision Mechanism | 2024-10 | G | re-decide | manip/sim+real |
| [Semantically Safe Robot Manipulation: From Semantic Scene Understanding to Motion Safeguards](https://arxiv.org/abs/2410.15185) | 2024-10 | G | authored | manip/real |
| [Addressing Failures in Robotics using Vision-Based Language Models (VLMs) and Behavior Trees (BT)](https://arxiv.org/abs/2411.01568) | 2024-11 | G | none | manip/sim |
| [Collaborative Instance Object Navigation: Leveraging Uncertainty-Awareness to Minimize Human-Agent Dialogues](https://arxiv.org/abs/2412.01250) | 2024-12 | G | re-decide | nav/sim |
| Large Language Models in Human-Robot Collaboration With Cognitive Validation Against Context-Induced Hallucinations | 2025 | G | none | manip/real |
| Are We Close to Realizing Self-Programming Robots That Overcome the Unexpected? | 2025-01 | G | re-decide | nav/real |
| GPTAlly: A Safety-Oriented System for Human-Robot Collaboration Based on Foundation Models | 2025-01 | G | none | manip/real |
| [A Unified Framework for Real-Time Failure Handling in Robotics Using Vision-Language Models, Reactive Planner and Behavior Trees](https://arxiv.org/abs/2503.15202) | 2025-03 | G | re-decide | manip/sim+real |
| [Safety Aware Task Planning via Large Language Models in Robotics](https://arxiv.org/abs/2503.15707) | 2025-03 | G | re-decide | mobile-manip/sim |
| [LangPert: Detecting and Handling Task-level Perturbations for Robust Object Rearrangement](https://arxiv.org/abs/2504.09893) | 2025-04 | G | re-decide | manip/sim |
| [Real-Time Out-of-Distribution Failure Prevention via Multi-Modal Reasoning](https://arxiv.org/abs/2505.10547) | 2025-05 | G | authored | aerial/sim+real |
| [VLM Can Be a Good Assistant: Enhancing Embodied Visual Tracking with Self-Improving Vision-Language Models](https://arxiv.org/abs/2505.20718) | 2025-05 | G | re-decide | nav/sim |
| [Dynamic Task Adaptation for Multi-Robot Manufacturing Systems with Large Language Models](https://arxiv.org/abs/2505.22804) | 2025-05 | G | re-decide | multi-robot/real |
| [Enhancing reliability in LLM-integrated robotic systems: A unified approach to security and safety](https://arxiv.org/abs/2509.02163) | 2025-09 | G | re-decide | nav/sim+real |
| [Robust and Resilient Soft Robotic Object Insertion with Compliance-Enabled Contact Formation and Failure Recovery](https://arxiv.org/abs/2509.17666) | 2025-09 | G | re-decide | manip/sim+real |
| [DynaMIC: Dynamic Multimodal In-Context Learning Enabled Embodied Robot Counterfactual Resistance Ability](https://arxiv.org/abs/2509.24413) | 2025-09 | G | none | manip/sim+real |
| [Drones that Think on their Feet: Sudden Landing Decisions with Embodied AI](https://arxiv.org/abs/2510.00167) | 2025-09 | G | re-decide | aerial/sim |
| [Online automatic code generation for robot swarms: LLMs and self-organizing hierarchy](https://arxiv.org/abs/2510.04774) | 2025-10 | G | re-decide | multi-robot/sim+real |
| [A Collaborative Reasoning Framework for Anomaly Diagnostics in Underwater Robotics](https://arxiv.org/abs/2511.03075) | 2025-11 | G | re-decide | other/sim |
| [From Words to Safety: Language-Conditioned Safety Filtering for Robot Navigation](https://arxiv.org/abs/2511.05889) | 2025-11 | G | authored | nav/sim+real |
| Localization, inspection, and reasoning (LIRA) module for autonomous workflows in self-driving laboratories | 2025-11 | G | re-decide | manip/real |
| [Guardian: Detecting Robotic Planning and Execution Errors with Vision-Language Models](https://arxiv.org/abs/2512.01946) | 2025-12 | C | re-decide | manip/sim+real |
| [RisConFix: LLM-based Automated Repair of Risk-Prone Drone Configurations](https://arxiv.org/abs/2512.07122) | 2025-12 | G | re-decide | aerial/sim |
| [RoboSafe: Safeguarding Embodied Agents via Executable Safety Logic](https://arxiv.org/abs/2512.21220) | 2025-12 | G | re-decide | manip/sim+real |
| [Foundation models on the bridge: Semantic hazard detection and safety maneuvers for maritime autonomy with vision-language models](https://arxiv.org/abs/2512.24470) | 2025-12 | G | none | other/real |

</details>

<details><summary><b>Teacher</b> (10)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [RLingua: Improving Reinforcement Learning Sample Efficiency in Robotic Manipulations With Large Language Models](https://arxiv.org/abs/2403.06420) | 2024-03 | G | re-decide | manip/sim+real |
| [Joint Verification and Refinement of Language Models for Safety-Constrained Planning](https://arxiv.org/abs/2410.14865) | 2024-10 | C | none | manip/sim |
| [MARLIN: Multi-Agent Reinforcement Learning Guided by Language-Based Inter-Robot Negotiation](https://arxiv.org/abs/2410.14383) | 2024-10 | G | re-decide | multi-robot/sim+real |
| [LLM-based Interactive Imitation Learning for Robotic Manipulation](https://arxiv.org/abs/2504.21769) | 2025-04 | G | authored | manip/sim |
| [Imagine, Verify, Execute: Memory-Guided Agentic Exploration with Vision-Language Models](https://arxiv.org/abs/2505.07815) | 2025-05 | G | re-decide | manip/sim+real |
| [LLM Trainer: Automated Robotic Data Generating via Demonstration Augmentation using LLMs](https://arxiv.org/abs/2509.20070) | 2025-09 | G | none | manip/sim+real |
| TARAD: Task-Aware Robot Affordance-Centric Diffusion Policy Learned From LLM-Generated Demonstrations | 2025-10 | G | none | manip/sim |
| [BLAZER: Bootstrapping LLM-based Manipulation Agents with Zero-Shot Data Generation](https://arxiv.org/abs/2510.08572) | 2025-10 | G | re-decide | manip/sim |
| [Gentle Manipulation Policy Learning via Demonstrations from VLM Planned Atomic Skills](https://arxiv.org/abs/2511.05855) `sim2real` | 2025-11 | G | none | manip/sim+real |
| [AnyTask: an Automated Task and Data Generation Framework for Advancing Sim-to-Real Policy Learning](https://arxiv.org/abs/2512.17853) | 2025-12 | G | re-decide | manip/sim+real |

</details>

<details><summary><b>Designer</b> (92)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Holodeck: Language Guided Generation of 3D Embodied AI Environments](https://arxiv.org/abs/2312.09067) | 2023 | G | none | nav/sim |
| Self-Refined Large Language Model as Automated Reward Function Designer for Deep Reinforcement Learning in Robotics | 2023 | G | re-decide | manip/sim |
| Towards A Foundation Model for Generalist Robots: Diverse Skill Learning at Scale via Automated Task and Scene Generation | 2023 | G | none | manip/sim |
| [Towards Generalist Robots: A Promising Paradigm via Generative Simulation](https://arxiv.org/abs/2305.10455) | 2023-05 | G | none | manip/sim |
| [LARG, Language-based Automatic Reward and Goal Generation](https://arxiv.org/abs/2306.10985) | 2023-06 | G | none | manip/sim |
| Text2Reward: Automated Dense Reward Function Generation for Reinforcement Learning | 2023-07 | G | none | manip/sim+real |
| [Self-Refined Large Language Model as Automated Reward Function Designer for Deep Reinforcement Learning in Robotics](https://arxiv.org/abs/2309.06687) | 2023-09 | G | re-decide | manip/sim |
| [Words into Action: Learning Diverse Humanoid Robot Behaviors using Language Guided Iterative Motion Refinement](https://arxiv.org/abs/2310.06226) | 2023-10 | G | re-decide | humanoid/sim |
| [Learning Reward for Physical Skills using Large Language Model](https://arxiv.org/abs/2310.14092) | 2023-10 | G | none | loco/sim |
| [Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models](https://arxiv.org/abs/2310.18308) `real2sim` | 2023-10 | G | none | manip/sim |
| [BBSEA: An Exploration of Brain-Body Synchronization for Embodied Agents](https://arxiv.org/abs/2402.08212) | 2024-02 | G | none | manip/sim |
| [Learning with Language-Guided State Abstractions](https://arxiv.org/abs/2402.18759) | 2024-02 | G | none | manip/sim |
| [ARO: Large Language Model Supervised Robotics Text2Skill Autonomous Learning](https://arxiv.org/abs/2403.15834) | 2024-03 | G | re-decide | other/sim |
| [Learning Reward for Robot Skills Using Large Language Models via Self-Alignment](https://arxiv.org/abs/2405.07162) | 2024-05 | G | none | manip/sim |
| [REvolve: Reward Evolution with Large Language Models using Human Feedback](https://arxiv.org/abs/2406.01309) | 2024-06 | G | re-decide | humanoid/sim |
| [Training Fast Robot Policies with Slow Foundation Models](https://arxiv.org/abs/2406.05881) | 2024-06 | G | re-decide | manip/sim |
| [E2CFD: Towards Effective and Efficient Cost Function Design for Safe Reinforcement Learning via Large Language Model](https://arxiv.org/abs/2407.05580) | 2024-07 | G | re-decide | nav/sim |
| [Affordance-Guided Reinforcement Learning via Visual Prompting](https://arxiv.org/abs/2407.10341) | 2024-07 | G | none | manip/real |
| [LLM-Empowered State Representation for Reinforcement Learning](https://arxiv.org/abs/2407.13237) | 2024-07 | G | re-decide | loco/sim |
| [Autonomous Improvement of Instruction Following Skills via Foundation Models](https://arxiv.org/abs/2407.20635) | 2024-07 | G | none | manip/real |
| [Diffusion Augmented Agents: A Framework for Efficient Exploration and Transfer Learning](https://arxiv.org/abs/2407.20798) | 2024-07 | G | re-decide | manip/sim |
| Multi-modal LLM-enabled Long-horizon Skill Learning for Robotic Manipulation | 2024-08 | G | none | manip/sim |
| [RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins (early version)](https://arxiv.org/abs/2409.02920) `real2sim2real` | 2024-09 | G | none | manip/sim+real |
| [Game On: Towards Language Models as RL Experimenters](https://arxiv.org/abs/2409.03402) | 2024-09 | G | re-decide | manip/sim |
| [Adaptive Language-Guided Abstraction from Contrastive Explanations](https://arxiv.org/abs/2409.08212) | 2024-09 | G | re-decide | manip/sim |
| [AnyBipe: An End-to-End Framework for Training and Deploying Bipedal Robots Guided by Large Language Models](https://arxiv.org/abs/2409.08904) | 2024-09 | G | re-decide | loco/sim+real |
| [Blox-Net: Generative Design-for-Robot-Assembly Using VLM Supervision, Physics Simulation, and a Robot with Reset](https://arxiv.org/abs/2409.17126) | 2024-09 | G | none | manip/sim+real |
| [Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model](https://arxiv.org/abs/2410.13882) | 2024-10 | G |  | manip/sim+real |
| [GenSim2: Scaling Robot Data Generation with Multi-modal and Reasoning LLMs](https://arxiv.org/abs/2410.03645) `sim2real` | 2024-10 | G | none | manip/sim+real |
| [Automated Creation of Digital Cousins for Robust Policy Learning](https://arxiv.org/abs/2410.07408) `real2sim2real` | 2024-10 | G | none | manip/sim+real |
| [Automated Rewards via LLM-Generated Progress Functions](https://arxiv.org/abs/2410.09187) | 2024-10 | G | none | manip/sim |
| [Language-Model-Assisted Bi-Level Programming for Reward Learning from Internet Videos](https://arxiv.org/abs/2410.09286) | 2024-10 | G | re-decide | loco/sim |
| [SDS - See it, Do it, Sorted: Quadruped Skill Synthesis from Single Video Demonstration](https://arxiv.org/abs/2410.11571) `sim2real` | 2024-10 | G | re-decide | loco/sim+real |
| [Hazards in Daily Life? Enabling Robots to Proactively Detect and Resolve Anomalies](https://arxiv.org/abs/2411.00781) | 2024-10 | G | none | mobile-manip/sim |
| [A Large Language Model-Driven Reward Design Framework via Dynamic Feedback for Reinforcement Learning](https://arxiv.org/abs/2410.14660) | 2024-10 | G | re-decide | manip/sim |
| [GRS: Generating Robotic Simulation Tasks from Real-World Images](https://arxiv.org/abs/2410.15536) `real2sim` | 2024-10 | G | re-decide | manip/sim |
| [LASER: Script Execution by Autonomous Agents for On-demand Traffic Simulation](https://arxiv.org/abs/2410.16197) | 2024-10 | G | none | driving/sim |
| [ICPL: Few-shot In-context Preference Learning via LLMs](https://arxiv.org/abs/2410.17233) | 2024-10 | G | re-decide | loco/sim |
| High-Precision Control of Humanoid Muscle-skeleton Robotic Arm Using Reinforcement Learning and Large Language Models | 2024-11 | G | re-decide | manip/sim |
| [ELEMENTAL: Interactive Learning from Demonstrations and Vision-Language Models for Reward Design in Robotics](https://arxiv.org/abs/2411.18825) | 2024-11 | G | re-decide | manip/sim |
| [Embodied Red Teaming for Auditing Robotic Foundation Models](https://arxiv.org/abs/2411.18676) | 2024-11 | G |  | manip/sim |
| [Video2Reward: Generating Reward Function from Videos for Legged Robot Behavior Learning](https://arxiv.org/abs/2412.05515) | 2024-12 | G | re-decide | loco/sim |
| [Efficient Language-instructed Skill Acquisition via Reward-Policy Co-Evolution](https://arxiv.org/abs/2412.13492) | 2024-12 | G | re-decide | manip/sim |
| Reward Design Framework Based on Reward Components and Large Language Models | 2024-12 | C | none | manip/sim |
| Progress Reward Model for Reinforcement Learning via Large Language Models | 2025 | G | none | manip/sim |
| Facilitating Autonomous Driving Tasks With Large Language Models | 2025-01 | G | none | driving/sim |
| [RoboHorizon: An LLM-Assisted Multi-View World Model for Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2501.06605) | 2025-01 | G | none | manip/sim+real |
| TARG: Tree of Action-reward Generation With Large Language Model for Cabinet Opening Using Manipulator | 2025-02 | G | re-decide | manip/sim |
| [STRIDE: Automating Reward Design, Deep Reinforcement Learning Training and Feedback Optimization in Humanoid Robotics Locomotion](https://arxiv.org/abs/2502.04692) | 2025-02 | G | re-decide | humanoid/sim |
| [A Real-to-Sim-to-Real Approach to Robotic Manipulation with VLM-Generated Iterative Keypoint Rewards](https://arxiv.org/abs/2502.08643) `real2sim2real` | 2025-02 | G | re-decide | manip/sim+real |
| [Learning a High-Quality Robotic Wiping Policy Using Systematic Reward Analysis and Visual-Language Model Based Curriculum](https://arxiv.org/abs/2502.12599) | 2025-02 | G | re-decide | manip/sim |
| [Never too Prim to Swim: An LLM-Enhanced RL-based Adaptive S-Surface Controller for AUVs under Extreme Sea Conditions](https://arxiv.org/abs/2503.00527) | 2025-03 | G | re-decide | other/sim |
| [Towards Autonomous Reinforcement Learning for Real-World Robotic Manipulation With Large Language Models](https://arxiv.org/abs/2503.04280) | 2025-03 | G | none | manip/sim+real |
| [LaMOuR: Leveraging Language Models for Out-of-Distribution Recovery in Reinforcement Learning](https://arxiv.org/abs/2503.17125) | 2025-03 | G | none | loco/sim |
| [Human-Object Interaction via Automatically Designed VLM-Guided Motion Policy](https://arxiv.org/abs/2503.18349) | 2025-03 | G | none | humanoid/sim |
| [GROVE: A Generalized Reward for Learning Open-Vocabulary Physical Skill](https://arxiv.org/abs/2504.04191) | 2025-04 | G | re-decide | humanoid/sim |
| [Boosting Universal LLM Reward Design through Heuristic Reward Observation Space Evolution](https://arxiv.org/abs/2504.07596) | 2025-04 | G | re-decide | other/sim |
| [GenTe: Generative Real-world Terrains for General Legged Robot Locomotion Control](https://arxiv.org/abs/2504.09997) | 2025-04 | G | none | loco/sim |
| [RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins](https://arxiv.org/abs/2504.13059) `real2sim2real` | 2025-04 | G | none | manip/sim+real |
| LLM-Based Reward Engineering for Reinforcement Learning: A Chain of Thought Approach | 2025-04 | G | none | loco/sim |
| [Automated Hybrid Reward Scheduling Via Large Language Models for Robotic Skill Learning](https://arxiv.org/abs/2505.02483) | 2025-05 | G | re-decide | loco/sim |
| [MA-ROESL: Motion-aware Rapid Reward Optimization for Efficient Robot Skill Learning from Single Videos](https://arxiv.org/abs/2505.08367) `sim2real` | 2025-05 | G | re-decide | loco/sim+real |
| [VIRAL: Vision-grounded Integration for Reward design And Learning](https://arxiv.org/abs/2505.22092) | 2025-05 | G | re-decide | other/sim |
| [LAMARL: LLM-Aided Multi-Agent Reinforcement Learning for Cooperative Policy Generation](https://arxiv.org/abs/2506.01538) | 2025-06 | G | none | multi-robot/sim+real |
| [AURA: Autonomous Upskilling with Retrieval-Augmented Agents](https://arxiv.org/abs/2506.02507) `sim2real` | 2025-06 | G | re-decide | humanoid/sim+real |
| [Scaffolding Dexterous Manipulation with Vision-Language Models](https://arxiv.org/abs/2506.19212) | 2025-06 | G | none | manip/sim+real |
| [Uncertainty-aware Reward Design Process](https://arxiv.org/abs/2507.02256) | 2025-07 | G | re-decide | manip/sim |
| [AGENTS-LLM: Augmentative GENeration of Challenging Traffic Scenarios with an Agentic LLM Framework](https://arxiv.org/abs/2507.13729) | 2025-07 | G | none | driving/sim |
| RoPESim: A Framework for Robot Manipulation Policy Evaluation via Simulation `real2sim` | 2025-08 | G | none | manip/sim |
| [Text2Touch: Tactile In-Hand Manipulation with LLM-Designed Reward Functions](https://arxiv.org/abs/2509.07445) `sim2real` | 2025-09 | G | re-decide | manip/sim+real |
| [CRAFT: Coaching Reinforcement Learning Autonomously using Foundation Models for Multi-Robot Coordination Tasks](https://arxiv.org/abs/2509.14380) `sim2real` | 2025-09 | G | re-decide | multi-robot/sim+real |
| [Reward Evolution with Graph-of-Thoughts: A Bi-Level Language Model Framework for Reinforcement Learning](https://arxiv.org/abs/2509.16136) | 2025-09 | G | re-decide | manip/sim |
| [LLM-Guided Task- and Affordance-Level Exploration in Reinforcement Learning](https://arxiv.org/abs/2509.16615) `sim2real` | 2025-09 | G | none | manip/sim+real |
| [Self-CriTeach: LLM Self-Teaching and Self-Critiquing for Improving Robotic Planning via Automated Domain Generation](https://arxiv.org/abs/2509.21543) | 2025-09 | C | none | manip/sim |
| Policy Generating and Value Shaping via Large Language Model for Long-Horizon Manipulation | 2025-09 | G | none | manip/sim |
| Where To Learn: Embodied Perception Learning Planned by Vision-Language Models | 2025-10 | G | re-decide | nav/sim |
| [High-Fidelity Simulated Data Generation for Real-World Zero-Shot Robotic Manipulation Learning With Gaussian Splatting](https://arxiv.org/abs/2510.10637) `real2sim2real` | 2025-10 | G | none | manip/sim+real |
| Simulation Verification Method for Robot Composite Task Planning in Open Environments `real2sim2real` | 2025-10 | G | re-decide | manip/sim+real |
| AnyBipe: An Automated End-to-End Framework for Training and Deploying Bipedal Robots Powered by Large Language Models `sim2real` | 2025-10 | G | re-decide | loco/sim+real |
| Application of LLM Guided Reinforcement Learning in Formation Control with Collision Avoidance `sim2real` | 2025-10 | G | re-decide | multi-robot/sim+real |
| Using LLM to Design Reward Function for Bipedal Walker-v3 | 2025-10 | G | none | loco/sim |
| [GenDexHand: Generative Simulation for Dexterous Hands](https://arxiv.org/abs/2511.01791) | 2025-11 | G | re-decide | manip/sim |
| [ReGen: Generative Robot Simulation via Inverse Design](https://arxiv.org/abs/2511.04769) | 2025-11 | G | none | other/sim |
| [PROF: An LLM-based Reward Code Preference Optimization Framework for Offline Imitation Learning](https://arxiv.org/abs/2511.13765) | 2025-11 | G | none | loco/sim |
| [Leveraging LLMs for reward function design in reinforcement learning control tasks](https://arxiv.org/abs/2511.19355) | 2025-11 | G | re-decide | other/sim |
| MoRE: Multi-Oracle Reward Evolution for Automated Reward Shaping in Reinforcement Learning | 2025-12 | G | re-decide | manip/sim |
| [PerFACT: Motion Policy with LLM-Powered Dataset Synthesis and Fusion Action-Chunking Transformers](https://arxiv.org/abs/2512.03444) | 2025-12 | G | none | manip/sim |
| HicAgent: Hierarchical Iterative Cooperative Learning Reward Generation Guided by a Large Model | 2025-12 | G | re-decide | other/sim |
| MIRA: An LLM-Driven Dual-Loop Architecture for Metacognitive Reward Design | 2025-12 | G | re-decide | loco/sim |
| [E-SDS: Environment-aware See it, Do it, Sorted - Automated Environment-Aware Reinforcement Learning for Humanoid Locomotion](https://arxiv.org/abs/2512.16446) | 2025-12 | G | re-decide | humanoid/sim |
| [Unifying Deep Predicate Invention with Pre-trained Foundation Models](https://arxiv.org/abs/2512.17992) | 2025-12 | G | re-decide | manip/sim+real |
| [Embodied Learning of Reward for Musculoskeletal Control with Vision Language Models](https://arxiv.org/abs/2512.23077) | 2025-12 | G | re-decide | humanoid/sim |

</details>

<details><summary><b>Developer</b> (23)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Evolution through Large Models](https://arxiv.org/abs/2206.08896) | 2022-06 | G | none | other/sim |
| [Automatic Robotic Development through Collaborative Framework by Large Language Models](https://arxiv.org/abs/2402.03699) | 2023-11 | G | re-decide | other/real |
| [InterPreT: Interactive Predicate Learning from Language Feedback for Generalizable Task Planning](https://arxiv.org/abs/2405.19758) | 2024-05 | G | re-decide | manip/sim+real |
| Autonomous Discovery of Robot Structure and Motion Control Through Large Vision Models | 2024-08 | G | re-decide | other/sim |
| Debate2Create: Robot Co-design via Large Language Model Debates | 2025 | G | re-decide | loco/sim |
| SkillWrapper: Generative Predicate Invention for Skill Abstraction | 2025 | G | re-decide | mobile-manip/sim+real |
| [SAS-Prompt: Large Language Models as Numerical Optimizers for Robot Self-Improvement](https://arxiv.org/abs/2504.20459) | 2025-04 | G | re-decide | manip/sim+real |
| ASCENT: Autonomous Skill Learning Toward Complex Embodied Tasks With Foundation Models | 2025-05 | G | re-decide | manip/sim |
| [Learning Compositional Behaviors from Demonstration and Language](https://arxiv.org/abs/2505.21981) | 2025-05 | G | none | manip/sim+real |
| [RoboMoRe: LLM-based Robot Co-design via Joint Optimization of Morphology and Reward](https://arxiv.org/abs/2506.00276) | 2025-05 | G | re-decide | loco/sim |
| [LLMs-guided adaptive compensator: Bringing Adaptivity to Automatic Control Systems with Large Language Models](https://arxiv.org/abs/2507.20509) | 2025-07 | G | re-decide | humanoid/sim+real |
| [Robot builds a robot's brain: AI generated drone command and control station hosted in the sky](https://arxiv.org/abs/2508.02962) | 2025-08 | G | re-decide | aerial/sim+real |
| [In-Context Iterative Policy Improvement for Dynamic Manipulation](https://arxiv.org/abs/2508.15021) | 2025-08 | G | re-decide | manip/sim+real |
| Experience-Driven NeuroSymbolic System for Efficient Robotic Bolt Disassembly | 2025-09 | G | none | manip/real |
| [Agent2: An Agent-Generates-Agent Framework for Reinforcement Learning Automation](https://arxiv.org/abs/2509.13368) | 2025-09 | G | re-decide | other/sim |
| [LAD-VF: LLM-Automatic Differentiation Enables Fine-Tuning-Free Robot Planning from Formal Methods Feedback](https://arxiv.org/abs/2509.18384) | 2025-09 | G | none | mobile-manip/sim |
| [Lang2Morph: Language-Driven Morphological Design of Robotic Hands](https://arxiv.org/abs/2509.18937) | 2025-09 | G | none | manip/real |
| [On Discovering Algorithms for Adversarial Imitation Learning](https://arxiv.org/abs/2510.00922) | 2025-10 | G | re-decide | loco/sim |
| Towards Autonomous Design of UAV Path Planning Algorithms via DeepSeek | 2025-10 | G | none | aerial/sim |
| ChatBuilder: LLM-assisted Modular Robot Creation | 2025-10 | G | none | other/sim+real |
| Human-in-the-loop Learning for Adaptive Robot Manipulation using Large Language Models and Behavior Trees | 2025-10 | G | re-decide | manip/sim+real |
| [Debate2Create: Robot Co-design via Multi-Agent LLM Debate](https://arxiv.org/abs/2510.25850) | 2025-10 | G | re-decide | loco/sim |
| LLM-Assisted Evolutionary Strategy for MuJoCo Control | 2025-11 | G | re-decide | loco/sim |

</details>


---

Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.
