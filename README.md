# Awesome Agentic Embodiment

> *Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs, not embodied action models — acting as agents that make explicit decisions whose consequences reach a robot body, and that re-decide on evidence of those consequences. Its organizing question is where such an agent sits relative to the body's deployed policy — steering it, guarding it, teaching it, designing its learning problem, or building its system (**Seat**).*

**Thesis (draft, under revision).** *Agency spreads around the body: general models, not embodied action models, fill seat after seat.*

Each seat is traced from its **67 pioneers (2022–2025)** to **85 papers from 2026**, the year most of the field's papers appeared; VLN / embodied navigation (13 from 2026) has its own chapter and the Real2Sim / Sim2Real sub-direction a short section (9), plus **19 benchmarks and resources**. Definition and inclusion rules: [docs/definition.md](docs/definition.md) (Chinese).

## Scope and what counts as an agent

**Scope.** General-purpose foundation models (LLMs / VLMs such as GPT, Gemini, Claude, Qwen-VL, GPT-6 Astra) doing embodied work as agents. They may plan, call skills, tools or VLAs, write code or constraints, or emit actions directly (LLM-as-policy, e.g. GPT-6 Astra evaluated as a robot policy on RoboDojo). A general model fine-tuned for an agent role still counts if it keeps acting through an agent interface (e.g. GUAVA). **Embodied foundation models that produce actions are not included** — VLAs (also with reasoning, memory or self-correction), hierarchical VLAs, world action models, robot foundation models (π0.5, ECoT, OneTwoVLA, Hi Robot, Gemini Robotics, PaLM-E); they appear here only as tools called by an agent.

**Agent tests** (all three): (1) **explicit decisions** — plans, skill/tool/VLA calls, code, constraints, verdicts, system edits, or actions chosen by the general model; (2) **decision authority** — the model writes its options, or picks among them with a control action (stop / retry / replan / ask / keep-revert); (3) **closed loop** — the model is called again with its own earlier decisions and evidence of their consequences, *or* the constraints or program it wrote read live perception and adapt while the robot acts (an *authored* loop, e.g. ReKep, VoxPoser, Code as Policies). Two families are included even when written once (*Loop* = none): **constraint / keypoint programming** (ReKep-type) and **agentic Real2Sim**.

Also not included: scalar reward/value models, one-shot annotators, world-model foresight, game/text worlds, purely digital agents.

## Seat by period

| Seat | Phase | Pioneers 2022–2025 | 2026 | of which fine-tuned (C) |
|---|---|---|---|---|
| Controller | runtime | 41 | 44 | 3 |
| Supervisor | runtime | 7 | 8 | 1 |
| Teacher | pre-deployment | 5 | 7 | 2 |
| Designer | pre-deployment | 11 | 10 | · |
| Developer | pre-deployment | 3 | 16 | · |

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
- [More 2026 papers (454)](#more-2026-papers)
- [More papers from 2022–2025 (384)](#more-papers-from-20222025)

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
| **AutoRT** | [AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963) | 2024 | arXiv | G | problem-spec | 1:N | none | none | multi-robot/real | Supervisor |
| **LLM3** | [LLM3:Large Language Model-based Task and Motion Planning with Motion Failure Reasoning](https://arxiv.org/abs/2403.11552) [[code]](https://github.com/AssassinWS/LLM-TAMP) | 2024 | IROS | G | skill-call | ×1 | re-decide | E | manip/sim | – |
| **COME-robot** | [Closed-Loop Open-Vocabulary Mobile Manipulation with GPT-4V](https://arxiv.org/abs/2404.10220) [[project]](https://come-robot.github.io/) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | mobile-manip/real | – |
| **VLM-PC** | [Commonsense Reasoning for Legged Robot Adaptation with Vision-Language Models](https://arxiv.org/abs/2407.02666) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | loco/real | – |
| **BUMBLE** | [BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | mobile-manip/real | – |
| **Being-0** | [Being-0: A Humanoid Robotic Agent with Vision-Language Models and Modular Skills](https://arxiv.org/abs/2503.12533) | 2025 | arXiv | G | skill-call | ×R | re-decide | E | humanoid/real | – |

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
| **FAEA** | [Demonstration-Free Robotic Control via LLM Agents](https://arxiv.org/abs/2601.20334) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim | – |
| **VLS** | [VLS: Steering Pretrained Robot Policies via Vision-Language Models](https://arxiv.org/abs/2602.03973) [[project]](https://vision-language-steering.github.io/webpage/) | 2026 | arXiv | G | constraint | ×1 | authored | E | manip/sim+real | – |
| **CaP-X** | [CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation](https://arxiv.org/abs/2603.22435) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim+real | Developer |
| **Embodiment Meets Environment** | [Embodiment Meets Environment: Toward Context-Aware, Safe Physical Caregiving Robots](https://arxiv.org/abs/2606.28592) | 2026 | Robotics | G | constraint | ×1 | authored | E | manip/sim+real | – |
| **VIA** | [VIA: Visual Interface Agent for Robot Control](https://arxiv.org/abs/2607.11119) | 2026 | arXiv | G | micro-action | ×1 | re-decide | E | manip/sim+real | – |
| **GTA-2** | [GTA-2: A Multi-VLM Framework for Synthesizing Robot Manipulation Skills via Grounded Task Axes](https://arxiv.org/abs/2609.09808) | 2026 | arXiv | G | constraint | ×R | none | none | manip/real | – |
| **Show-Harness** | [Show-Harness: Just a VLM Agent Can Play Robots](https://arxiv.org/abs/2609.10522) [[project]](https://showlab.github.io/Show-Harness) | 2026 | arXiv | G | micro-action | ×1 | re-decide | E | manip/sim+real | – |
| **Agent as Policy** | [Agent as Policy for Robotic Manipulation](https://arxiv.org/abs/2609.12541) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/real | – |
| **AquaCap** | [AquaCap: A Training-Free Underwater Embodied Agent with Code-as-Policy](https://arxiv.org/abs/2609.23133) | 2026 | arXiv | G | code | ×1 | re-decide | E | other/sim+real | – |
| **Astra on RoboDojo** | [An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170) | 2026 | arXiv | G | micro-action | ×1 | re-decide | E | manip/sim | – |
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
| **WhenToAsk** | [When Should a Failing Robot Ask? Initiating Corrective Human-Robot Dialogue from Audited Sensor Evidence](https://arxiv.org/abs/2609.21942) | 2026 | arXiv | G | verdict | ×1 | re-decide | E+H | manip/sim+real | – |
| **Beyond Human Demos** | [Learning Beyond What Humans Can Demonstrate](https://arxiv.org/abs/2609.24996) [[project]](http://guardrail-policy.github.io/) | 2026 | arXiv | G | constraint | ×1 | authored | E | manip/sim | Developer |

## Teacher

Before deployment, the agent acts; its outcome-checked behaviour becomes the deployed model's training target.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **SUDD** | [Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition](https://arxiv.org/abs/2307.14535) [[project]](https://www.cs.columbia.edu/~huy/scalingup/) | 2023 | CoRL | G | skill-call | ×1 | authored | E | manip/sim | Designer |
| **RobotGPT** | [RobotGPT: Robot Manipulation Learning from ChatGPT](https://arxiv.org/abs/2312.01421) | 2023 | RA-L | G | code | ×1 | re-decide | E | manip/sim+real | – |
| **Manipulate-Anything** | [Manipulate-Anything: Automating Real-World Robots using Vision-Language Models](https://arxiv.org/abs/2406.18915) [[project]](https://robot-ma.github.io/) | 2024 | CoRL | G | skill-call | ×1 | re-decide | E | manip/sim+real | Controller |
| **RoboTwin 2.0** | [RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation](https://arxiv.org/abs/2506.18088) [[project]](https://robotwin-platform.github.io/) [[code]](https://github.com/robotwin-Platform/robotwin) | 2025 | arXiv | G | code | ×1 | re-decide | E | manip/sim+real | Designer |
| **HumanoidGen** | [HumanoidGen: Data Generation for Bimanual Dexterous Manipulation via LLM Reasoning](https://arxiv.org/abs/2507.00833) [[project]](https://openhumanoidgen.github.io) | 2025 | NeurIPS | G | constraint | ×1 | re-decide | E | humanoid/sim | Designer |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **GUAVA** | [Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness](https://arxiv.org/abs/2606.18363) | 2026 | arXiv | G→C | trace | ×1 | re-decide | E | manip/sim+real | Controller |
| **EmbodiedSWE** | [EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics](https://arxiv.org/abs/2609.27308) | 2026 | arXiv | G | trace | ×1 | re-decide | E | manip/sim+real | Controller |
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
| **Embodied Agents Take Control** | [Embodied Agents Take Control: Minimal-Interface Zero-Shot Agents Rival Industrial-Scale Policies in Vision-and-Language Navigation](https://arxiv.org/abs/2607.26148) | 2026 | arXiv | Controller | G | micro-action | re-decide | nav/sim | – |
| **HAM-VLN** | [HAM-VLN: Harnessing Hierarchical Agentic Memory for Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2607.29600) | 2026 | arXiv | Controller | G | micro-action | re-decide | nav/sim | – |
| **Air-Ground VLN** | [Air-Ground Collaborative Vision-and-Language Navigation via Shared Bird's-Eye Maps](https://arxiv.org/abs/2609.03483) | 2026 | arXiv | Controller | G | skill-call | re-decide | multi-robot/sim | – |
| **HarnessVLN** | [HarnessVLN: Unifying Training-Free Embodied Navigation through an Agent Harness](https://arxiv.org/abs/2609.15195) | 2026 | arXiv | Controller | G | skill-call | re-decide | nav/sim | – |
| **RoboFind** | [RoboFind: Multi-Agent Personalized Object Search for People Who Are Blind or Have Low Vision](https://arxiv.org/abs/2609.20330) | 2026 | arXiv | Controller | G | skill-call | re-decide | nav/real | Supervisor |
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
| **EmboCoach-Bench** | [From Digital to Physical: Digital Agents as Autonomous Coaches for Physical Intelligence](https://arxiv.org/abs/2601.21570) | 2026 | arXiv | Developer | manip/sim |
| **Orchestration Study** | [What Matters in Orchestrating Robot Policies: A Systematic Study of Hierarchical VLA Agents](https://arxiv.org/abs/2606.10267) | 2026 | arXiv | Controller | manip/sim+real |
| **MLLM Drone Agents Eval** | [Evaluating Multimodal LLMs as Generalist Vision-Language-Action Agents for Drone Control: Commanding, Approaching, Tracking and Searching](https://arxiv.org/abs/2609.01404) | 2026 | arXiv | Controller | aerial/sim |
| **Astra on VLN-CE** | [How Far Can GPT-6-Astra Go? Evaluating Capabilities in Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2609.20116) | 2026 | arXiv | Controller | nav/sim |
| **CodeActionBench** | [CodeActionBench: Evaluating Agentic Code-as-Policy for Embodied Manipulation](https://arxiv.org/abs/2609.33807) [[project]](https://codeactionbench.org) | 2026 | arXiv | Controller | manip/sim |
| **RLE-Bench** | [RLE-Bench: A Qualifying Exam for Coding Agents as Robot Learning Engineers](https://arxiv.org/abs/2609.34210) [[project]](https://rle-bench.github.io/) | 2026 | arXiv | Developer | manip/sim |
| **LIBERO-Agent** | [LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507) | 2026 | arXiv | Controller | manip/sim |
| **Frontier VLM Agents Study** | [Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854) [[project]](https://embodied-agent-arena.github.io/embodied-agent-arena/) | 2026 | arXiv | Controller | mobile-manip/sim |
| **Video2World** | [Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos](https://arxiv.org/abs/2610.04432) [[project]](https://aetherlabsai.github.io/Video2World) | 2026 | arXiv | Designer | manip/sim |
| **RobotWorld** | [RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](https://arxiv.org/abs/2610.10409) | 2026 | arXiv | Controller | other/sim |

## More 2026 papers

454 further 2026 papers that meet the definition (judged `core` by a verification pass) but are not in the curated tables above. Tags come from the judging pass and are not hand-checked; generated by `scripts/build_extended.py`.

<details><summary><b>Controller · Orchestrators</b> (146)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Leveraging Adaptive Group Negotiation for Heterogeneous Multi-Robot Collaboration with Large Language Models](https://arxiv.org/abs/2602.06967) | 2025-12 | G | re-decide | multi-robot/sim |
| A Hierarchical Framework of Central-Distributed LLM Negotiation and Specialized Model Orchestration for Multi-Robot Collaborative Assembly | 2026 | G | re-decide | multi-robot/sim |
| AgenticDiffusion: Agentic Diffusion-based Path Planning for Vision-Based UAV Navigation | 2026 | G | re-decide | aerial/real |
| CoIN: Interactive Navigation With Counterfactual Reasoning via Vision–Language Models | 2026 | C | re-decide | mobile-manip/sim+real |
| [LLM-Based Agentic Exploration for Robot Navigation & Manipulation with Skill Orchestration](https://arxiv.org/abs/2601.00555) | 2026-01 | G | re-decide | mobile-manip/sim+real |
| [CoINS: Counterfactual Interactive Navigation via Skill-Aware VLM](https://arxiv.org/abs/2601.03956) | 2026-01 | C | re-decide | mobile-manip/sim+real |
| [A Framework for Low-Latency, LLM-Driven Multimodal Interaction on the Pepper Robot](https://arxiv.org/abs/2603.21013) | 2026-01 | G | re-decide | social/real |
| [An Embodied Companion for Visual Storytelling](https://arxiv.org/abs/2603.05511) | 2026-01 | G | re-decide | manip/real |
| [UAVGENT: A Language-Guided Distributed Control Framework](https://arxiv.org/abs/2602.13212) | 2026-01 | G | re-decide | aerial/sim |
| TRTP: a three-stage robust task planning framework for open worlds via visual-language models and digital twin simulation `real2sim2real` | 2026-02 | G | re-decide | manip/sim+real |
| [PLanAR: Planning-Language-Grounded Agentic Reasoning for Robot Manipulation](https://arxiv.org/abs/2602.01662) | 2026-02 | G | re-decide | manip/real |
| [Integrated Exploration and Sequential Manipulation on Scene Graph with LLM-based Situated Replanning](https://arxiv.org/abs/2602.04419) | 2026-02 | G | re-decide | mobile-manip/sim+real |
| [Affordance-Aware Interactive Decision-Making and Execution for Ambiguous Instructions](https://arxiv.org/abs/2602.05273) | 2026-02 | G | re-decide | mobile-manip/sim+real |
| [Agentic AI for Robot Control: Flexible but still Fragile](https://arxiv.org/abs/2602.13081) | 2026-02 | G | re-decide | mobile-manip/real |
| [UniManip: General-Purpose Zero-Shot Robotic Manipulation with Agentic Operational Graph](https://arxiv.org/abs/2602.13086) | 2026-02 | G | re-decide | manip/real |
| [AgentRob: From Virtual Forum Agents to Hijacked Physical Robots](https://arxiv.org/abs/2602.13591) | 2026-02 | G | re-decide | multi-robot/real |
| [Replanning Human-Robot Collaborative Tasks with Vision-Language Models via Semantic and Physical Dual-Correction](https://arxiv.org/abs/2602.14551) | 2026-02 | G | re-decide | humanoid/sim+real |
| [VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing](https://arxiv.org/abs/2602.15549) | 2026-02 | G | re-decide | manip/sim+real |
| [MALLVI: A Multi-Agent Framework for Integrated Generalized Robotics Manipulation](https://arxiv.org/abs/2602.16898) | 2026-02 | G | re-decide | manip/sim+real |
| [Zero-shot Interactive Perception](https://arxiv.org/abs/2602.18374) | 2026-02 | G | re-decide | manip/real |
| [CoReLIN: Constraint-based Reasoning for Zero-shot Lifelong Interactive Navigation](https://arxiv.org/abs/2602.20055) | 2026-02 | G | re-decide | mobile-manip/sim+real |
| ChainBot: An Agent System for Autonomous Robotic Object Manipulation by Dynamically Chaining Multiple Foundation Models | 2026-02 | G | re-decide | manip/real |
| [From Language to Action: Can LLM-Based Agents Be Used for Embodied Robot Cognition?](https://arxiv.org/abs/2603.03148) | 2026-03 | G | re-decide | mobile-manip/sim |
| [Critic in the Loop: A Tri-System VLA Framework for Robust Long-Horizon Manipulation](https://arxiv.org/abs/2603.05185) | 2026-03 | G | re-decide | manip/sim+real |
| Collaborative LLM-Based Agents for Autonomous Multi-UAV Mission Execution | 2026-03 | G | re-decide | multi-robot/sim+real |
| [MoMaStage: Skill-State Graph Guided Planning and Closed-Loop Execution for Long-Horizon Indoor Mobile Manipulation](https://arxiv.org/abs/2603.08383) | 2026-03 | G | re-decide | mobile-manip/sim+real |
| [SELF-VLA: A Skill Enhanced Agentic Vision-Language-Action Framework for Contact-Rich Disassembly](https://arxiv.org/abs/2603.11080) | 2026-03 | G | re-decide | manip/real |
| [AdaClearGrasp: Learning Adaptive Clearing for Zero-Shot Robust Dexterous Grasping in Densely Cluttered Environments](https://arxiv.org/abs/2603.10616) | 2026-03 | G | re-decide | manip/sim+real |
| [RoboStream: Weaving Spatio-Temporal Reasoning with Memory in Vision-Language Models for Robotics](https://arxiv.org/abs/2603.12939) | 2026-03 | G | re-decide | manip/sim+real |
| [From Scanning Guidelines to Action: A Robotic Ultrasound Agent with LLM-Based Reasoning](https://arxiv.org/abs/2603.14393) | 2026-03 | G | re-decide | manip/real |
| [CORAL: COntextual Reasoning And Local Planning in A Hierarchical VLM Framework for Underwater Monitoring](https://arxiv.org/abs/2603.14786) | 2026-03 | G | re-decide | other/sim |
| [DreamPlan: Efficient Reinforcement Fine-Tuning of Vision-Language Planners via Video World Models](https://arxiv.org/abs/2603.16860) | 2026-03 | C | re-decide | manip/real |
| AIR-Embodied: Active Interactive Reconstruction for 3D Gaussian Splatting with Embodied Multimodal Agents | 2026-03 | G | re-decide | manip/sim+real |
| Event-Triggered Closed-Loop Semantic Control for Zero-Shot Multi-Step Robotic Manipulation | 2026-03 | G | re-decide | manip/real |
| [Task-Aware Positioning for Improvisational Tasks in Mobile Construction Robots via an AI Agent with Multi-LMM Modules](https://arxiv.org/abs/2603.22903) | 2026-03 | G | re-decide | loco/real |
| [SafeGuard ASF: SR Agentic Humanoid Robot System for Autonomous Industrial Safety](https://arxiv.org/abs/2603.25353) | 2026-03 | G | re-decide | humanoid/sim+real |
| [ROSClaw: An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction](https://arxiv.org/abs/2603.26997) | 2026-03 | G | re-decide | loco/real |
| [On-Demand Human Assistance for Task Continuation under Physical Action Failures in LLM-based Planning](https://arxiv.org/abs/2603.28156) | 2026-03 | G | re-decide | mobile-manip/real |
| [OpenGo: An OpenClaw-Based Robotic Dog with Real-Time Skill Switching](https://arxiv.org/abs/2604.01708) | 2026-04 | G | re-decide | loco/real |
| [QuadAgent: A Responsive Agent System for Vision-Language Guided Quadrotor Agile Flight](https://arxiv.org/abs/2604.02786) | 2026-04 | G | re-decide | aerial/sim+real |
| [ROSClaw: A Hierarchical Semantic-Physical Framework for Heterogeneous Multi-Agent Collaboration](https://arxiv.org/abs/2604.04664) | 2026-04 | G | re-decide | multi-robot/sim+real |
| [ExpressMM: Expressive Mobile Manipulation Behaviors in Human-Robot Interactions](https://arxiv.org/abs/2604.05320) | 2026-04 | G | re-decide | mobile-manip/real |
| [AEROS: A Single-Agent Operating Architecture with Embodied Capability Modules](https://arxiv.org/abs/2604.07039) | 2026-04 | G | re-decide | manip/sim |
| [DeCoNav: Dialog enhanced Long-Horizon Collaborative Vision-Language Navigation](https://arxiv.org/abs/2604.12486) | 2026-04 | G | re-decide | multi-robot/sim |
| [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](https://arxiv.org/abs/2604.13942) | 2026-04 | G | re-decide | manip/sim+real |
| Graph-Based Task Allocation for Multi-Agent Fleet Management: A Genetic Algorithm Approach with LLM Integration | 2026-04 | G | re-decide | multi-robot/sim |
| [CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models](https://arxiv.org/abs/2604.22238) | 2026-04 | G | authored | manip/real |
| An Agentic Framework for Aerial Swarms: Integrating LLMs with the Crazyswarm2 | 2026-04 | G | re-decide | multi-robot/sim |
| [ANCHOR: A Physically Grounded Closed-Loop Framework for Robust Home-Service Mobile Manipulation](https://arxiv.org/abs/2604.25323) | 2026-04 | G | re-decide | mobile-manip/real |
| Integrating Advantage Actor-Critic in Multi-Robot Collaboration | 2026-05 | G | re-decide | multi-robot/sim |
| [LLM-Foraging: Large Language Models for Decentralized Swarm Robot Foraging](https://arxiv.org/abs/2605.01461) | 2026-05 | G | re-decide | multi-robot/sim |
| Towards Object-Level Multimodal Task Planning for Long-Term Robotic Manipulation with Vision Language Model and Behavior Tree | 2026-05 | G | authored | manip/real |
| [Say the Mission, Execute the Swarm: Agent-Enhanced LLM Reasoning in the Web-of-Drones](https://arxiv.org/abs/2605.03788) | 2026-05 | G | re-decide | aerial/sim |
| [BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation](https://arxiv.org/abs/2605.07306) | 2026-05 | G | re-decide | manip/real |
| [Melding LLM and temporal logic for reliable human-swarm collaboration in complex scenarios](https://arxiv.org/abs/2605.07877) | 2026-05 | G | re-decide | multi-robot/sim+real |
| Proactive collaboration via autonomous interaction | 2026-05 | G | re-decide | multi-robot/sim+real |
| [Qumus: Realization of An Embodied AI Quantum Material Experimentalist](https://arxiv.org/abs/2605.18407) | 2026-05 | G | re-decide | other/real |
| A cognitive synergetic hierarchical framework for UAV swarm combat via speculative inference and role-decoupled reinforcement learning | 2026-05 | G | re-decide | multi-robot/sim |
| Man-Machine Collaborative Task Planning Based on Visual Language Models | 2026-05 | C | re-decide | manip/sim+real |
| [Sentinel: Embodied Cooperative Spatial Reasoning and Planning](https://arxiv.org/abs/2605.26239) | 2026-05 | G | re-decide | multi-robot/sim |
| [PEACE: A Planner-Executor Agent with Constraint Enforcement for UAVs](https://arxiv.org/abs/2606.00104) | 2026-05 | G | re-decide | aerial/sim |
| [On-Device Robotic Planning: Eliminating Inference Redundancy for Efficient Decision-Making](https://arxiv.org/abs/2605.31460) | 2026-05 | G | re-decide | mobile-manip/sim+real |
| HiveNav: Hierarchical Semantic Planning for UAV Swarm Exploration | 2026-06 | G | re-decide | multi-robot/sim |
| Multi-Agent LLM Reasoning for Robotic Block Placement | 2026-06 | G | re-decide | manip/real |
| [PerceptTwin: Semantic Scene Reconstruction for Iterative LLM Planning and Verification](https://arxiv.org/abs/2606.04226) `real2sim2real` | 2026-06 | G | re-decide | mobile-manip/sim |
| [AgenticDiffusion: Multi-View Reasoning with View-Conditioned Diffusion Planning for Vision-Based UAV Navigation](https://arxiv.org/abs/2606.04111) | 2026-06 | G | re-decide | aerial/real |
| [A Conversational Framework for Human-Robot Collaborative Manipulation with Distributed Generative AI models](https://arxiv.org/abs/2606.06061) | 2026-06 | G | re-decide | manip/real |
| [A Systems Engineering Framework for Vision-Language-Enabled UAV Triage and Disaster Response](https://arxiv.org/abs/2607.27597) | 2026-06 | G | re-decide | aerial/sim |
| [VoLo: A Physical Orchestrator for Open-Vocabulary Long-Horizon Manipulation](https://arxiv.org/abs/2606.07723) | 2026-06 | G | re-decide | manip/sim |
| [Agentic Neuro-Symbolic Planning and Commissioning for Human-in-the-Loop Industrial Robotics with Digital Twins](https://arxiv.org/abs/2606.08214) | 2026-06 | G | re-decide | manip/sim+real |
| [Learning What to Say to Your VLA: Mostly Harmless Vision Language Action Model Steering](https://arxiv.org/abs/2606.12299) | 2026-06 | C | re-decide | manip/sim |
| [DynaHMRC: Decentralized Heterogeneous Multi-Robot Collaboration for Dynamic Tasks with Large Language Models](https://arxiv.org/abs/2606.14882) | 2026-06 | C | re-decide | multi-robot/sim |
| MAVE: An Augmented Multi-agent LLM System for Interactive Design and Robotic Fabrication | 2026-06 | G | re-decide | manip/real |
| [EmbodiedUS-FS: Fast Slow Intelligence for Ultrasound Robotics](https://arxiv.org/abs/2606.22319) | 2026-06 | G | re-decide | manip/real |
| [HoloAgent-0: A Unified Embodied Agent Framework with 3D Spatial Memory](https://arxiv.org/abs/2606.23565) | 2026-06 | G | re-decide | mobile-manip/real |
| RoDA: A Role-Playing Dual-Agent Framework to Drive Nursing Robots in Bimanual Coordination Tasks | 2026-06 | G | re-decide | manip/sim |
| [Advancing Omnimodal Embodied Agents from Isolated Skills to Everyday Physical Autonomy](https://arxiv.org/abs/2606.27251) | 2026-06 | G | re-decide | mobile-manip/real |
| [RoboNav-Arm: Agentic AI-Driven Navigation and Obstacle Avoidance for Robotic Manipulator in Cluttered Environments](https://arxiv.org/abs/2607.09716) | 2026-06 | G | re-decide | manip/real |
| [AERIS: Aerial-Edge Role-Driven Intelligence at Runtime via Orchestrated Language-Model Swarm](https://arxiv.org/abs/2606.30151) | 2026-06 | G | re-decide | aerial/sim |
| [Agentic RAG-VLM: Affordance-Aware Retrieval-Augmented Generation with Self-Reflective Planning for Robotic Grasping](https://arxiv.org/abs/2606.31200) | 2026-06 | G | re-decide | manip/real |
| Generation of Object Alignment Behavior Based on VLM Proposal and Verification Considering a Human-Robot Collaboration Interface | 2026-07 | G | re-decide | manip/real |
| RoboCleaner: Robotic Tabletop Cleaning via VLM-Powered Multi-Agent Collaboration | 2026-07 | G | re-decide | manip/real |
| Robust Assistive Mobile Manipulation via Structured LLM Programs, Confirmation Loops, and Hierarchical Skill Recovery * | 2026-07 | G | re-decide | mobile-manip/real |
| Twin-BT: An LLM-Based Behavior Tree Framework Integrating Digital Twin and Deterministic Semantic Verification for Robotics `real2sim2real` | 2026-07 | G | re-decide | manip/sim+real |
| VLA-Touch: Enhancing Vision-Language-Action Model With Dual-Level Tactile Feedback | 2026-07 | G | re-decide | manip/real |
| World-Model-Enhanced UAV Intelligent Inspection Method for Converter Station Valve Halls | 2026-07 | G | re-decide | aerial/real |
| [HiMe: Hierarchical Embodied Memory for Long-Horizon Vision-Language-Action Control](https://arxiv.org/abs/2607.03449) | 2026-07 | G | re-decide | manip/sim+real |
| [ACE: Agentic Control for Embodied Manipulation via Zero-shot Workflow Reasoning](https://arxiv.org/abs/2607.04162) | 2026-07 | G | re-decide | manip/real |
| Human–robot collaboration in building disassembly: a multi-agent LLM architecture | 2026-07 | G | re-decide | manip/sim |
| [TypeGo: An OS Runtime for Embodied Agents](https://arxiv.org/abs/2607.05482) | 2026-07 | G | re-decide | loco/real |
| [A Closed-Loop Multi-Agent Framework for Robust Multi-Robot Manipulation](https://arxiv.org/abs/2607.06990) | 2026-07 | G | re-decide | multi-robot/sim+real |
| [Multi-Agent Robotic Control with Onboard Vision-Language Models](https://arxiv.org/abs/2607.07403) | 2026-07 | G | re-decide | mobile-manip/sim |
| [Task Planning for Mobile Manipulation in Retail Stores using Foundation Models with Iterative Re-planning](https://arxiv.org/abs/2607.09962) | 2026-07 | G | re-decide | mobile-manip/sim |
| [A Glimpse into Long-term Physical Coexistence with Intelligent Robots](https://arxiv.org/abs/2607.11377) | 2026-07 | G | re-decide | multi-robot/real |
| [Engagement-Aware Agentic Pursuit-Evasion](https://arxiv.org/abs/2607.10986) | 2026-07 | G | re-decide | multi-robot/sim |
| Practical Human–Robot Interaction (HRI) through Large Language Model (LLM)-based Voice-to-Action Systems | 2026-07 | G | re-decide | mobile-manip/real |
| [Exploratory, Communicative, and Deployable: Vision-Driven Embodied Agents for Open-World Mobile Manipulation](https://arxiv.org/abs/2607.13653) | 2026-07 | C | re-decide | mobile-manip/sim+real |
| [LENS: LLM-guided Environment Simplification for Planning and Control in Clutter](https://arxiv.org/abs/2607.19633) | 2026-07 | G | re-decide | manip/sim+real |
| ReflectVLM+: Enhancing VLM-based Robotic Planning via Quantitative Stagnation Detection and Trajectory Refinement | 2026-07 | C | re-decide | manip/sim |
| [RoboBRIDGE: A Modular Framework for Bridging Policies to Robust Real-World Robotic Agents](https://arxiv.org/abs/2607.27881) | 2026-07 | G | re-decide | manip/sim+real |
| [D-VLC: Decentralized Vision-Language Collaboration for Heterogeneous Embodied Multi-Robot Systems in Unknown Environments](https://arxiv.org/abs/2607.29009) | 2026-07 | G | re-decide | multi-robot/sim |
| Dynamic Closed-Loop Grasping Via an Enhanced Thinkgrasp Framework | 2026-08 | G | re-decide | manip/sim |
| Embodied Intelligence Robots: Flexible Task Planning Framework and Multimodal Fusion Perception | 2026-08 | G | re-decide | manip/real |
| LLM-Based Hierarchical Control Architecture for Robotic Operation | 2026-08 | G | re-decide | manip/sim+real |
| [ETA: A New Agentic Paradigm for Embodied Tasks](https://arxiv.org/abs/2608.03924) | 2026-08 | G | re-decide | manip/sim+real |
| PFEA: a VLM-based high-level natural language planning and feedback embodied agent for human-centered AI | 2026-08 | G | re-decide | manip/real |
| [HarnessWAM: Bridging Prediction and Deliberation in World Action Models](https://arxiv.org/abs/2608.09516) | 2026-08 | G | re-decide | manip/sim |
| [Active Perception for Embodied Disambiguation](https://arxiv.org/abs/2608.13605) | 2026-08 | G | re-decide | mobile-manip/real |
| [MistyPilot: Enabling Social-Robot Control through Multi-Agent LLM Skill Orchestration](https://arxiv.org/abs/2608.15549) | 2026-08 | G | authored | social/real |
| [HODAgent: Towards On-Demand, Responsive Humanoids for Physical World Human Interaction](https://arxiv.org/abs/2608.17584) | 2026-08 | G | re-decide | humanoid/sim+real |
| MulPlanLM: multimodal robotic task planning with vision-language models and physical feedback | 2026-08 | C | re-decide | manip/sim+real |
| [Evidence-Gated Task and Motion Planning with Vision-Language Models](https://arxiv.org/abs/2608.20084) | 2026-08 | G | re-decide | manip/sim |
| A human-verifiable execution-time DAG refinement framework for LLM-driven multi-robot construction task planning | 2026-08 | G | re-decide | multi-robot/sim |
| [$R^3$: Training Robots to Reason in Natural Language via Reinforcement Learning](https://arxiv.org/abs/2608.26053) | 2026-08 | C | re-decide | manip/sim |
| [PanelShield: Verifiable Closed-Loop Safe Planning for Robotic Industrial Panel Operation](https://arxiv.org/abs/2608.28305) | 2026-08 | G | re-decide | manip/sim+real |
| [Plan Along the Way: Event-Triggered Foundation-Model Planning for TAMP Execution in Partially Observable Manipulation](https://arxiv.org/abs/2608.28075) | 2026-08 | G | re-decide | manip/sim |
| [EMERGE-Policy: A Robot Mind Emerges Beyond a Single Policy](https://arxiv.org/abs/2608.29896) | 2026-08 | G | re-decide | manip/sim+real |
| Adaptive Task Planning for Long-Horizon Robotic Manipulation Based on Video Priors and Dynamic Scene Graphs | 2026-09 | G | re-decide | manip/sim |
| [EmbodiedSkills: A Unified Framework for Orchestrating, Training, and Deploying VLA Agents](https://arxiv.org/abs/2609.01281) | 2026-09 | C | re-decide | manip/sim+real |
| Visual Storytelling: An Embodied Companion [Arts and Robotics] | 2026-09 | G | re-decide | manip/real |
| [HINT: Human-Intent Inception for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2609.02653) | 2026-09 | G | re-decide | manip/sim+real |
| [A Brain-inspired Hierarchical Framework for Zero-Shot Robot Task Reasoning and Execution](https://arxiv.org/abs/2609.05985) | 2026-09 | G | re-decide | manip/real |
| [2AM: Grounding Agent-Side Memory as Guidance for Steerable Action Models in Long-Horizon Manipulation](https://arxiv.org/abs/2609.11308) | 2026-09 | G | re-decide | manip/sim |
| [Harness Robotic OS: A Unified Embodied-Agent Runtime for Closed-Loop Quadruped Inspection](https://arxiv.org/abs/2609.11225) | 2026-09 | G | re-decide | loco/real |
| [AeroWeaver: An Embodied-Agent Harness for Weaving Aerial Skills into Distributed, Adaptive Swarm Execution](https://arxiv.org/abs/2609.18520) | 2026-09 | G | re-decide | multi-robot/sim |
| [From Rollout to Reset: A Graph-Based Harness for Autonomous Long-Horizon Manipulation Evaluation](https://arxiv.org/abs/2609.19413) | 2026-09 | G | re-decide | manip/real |
| [KINO: A Keyframe Interface for VLM Planning and Whole-Body Control in Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.18869) | 2026-09 | G | re-decide | humanoid/sim+real |
| [MaskHarness-WAM: Instance-Grounded Harnessing for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2609.19974) | 2026-09 | G | re-decide | manip/real |
| [StageGuard: Learning Stage Transitions for Long-Horizon Robot Tasks via Agentic Distillation](https://arxiv.org/abs/2609.20791) | 2026-09 | C | re-decide | manip/sim |
| SMaRTAban: a voice-controlled LLM agent for quadruped mobile robotics with integrated vision | 2026-09 | G | re-decide | loco/real |
| [MedVLA: A Hierarchical Vision-Language-Action Framework for Closed-Loop Precision Medical Robot Manipulation](https://arxiv.org/abs/2609.25756) | 2026-09 | C | re-decide | manip/sim |
| [From Passive Execution to Active Exploration: Agentic Embodied Manipulation in Realistic Environments](https://arxiv.org/abs/2609.29091) | 2026-09 | G | re-decide | manip/sim+real |
| [Robo-Harness K1: Harnessing Robot-Use Agents via Perception Augmentation](https://arxiv.org/abs/2609.29389) | 2026-09 | G | re-decide | manip/sim |
| [Assisting for Open-Ended Tasks: Goal-Oriented Shared Autonomy as a Particle Filter](https://arxiv.org/abs/2609.32576) | 2026-09 | G | re-decide | manip/real |
| LLM-driven embodied intelligent system for autonomous open-channel hydraulics: design and validation via long-duration PIV measurements | 2026-09 | G | re-decide | other/real |
| [Where Memory Belongs: Ledger, an Object Ledger for Memory-Augmented VLAs](https://arxiv.org/abs/2609.34554) | 2026-09 | G | re-decide | manip/sim |
| Agentic Preparative
Thin-Layer Chromatography System
for Autonomous Purification | 2026-09 | G | re-decide | manip/real |
| [Simple Agentic Memory for Generalist Robot Policies](https://arxiv.org/abs/2609.36595) | 2026-09 | G | re-decide | manip/sim |
| [RoboAssist: Interactive Human-Humanoid Planning for Long-Horizon Surgical Assistance](https://arxiv.org/abs/2609.39384) | 2026-09 | G | re-decide | humanoid/sim |
| [DuoMind: Enabling Distributed Multi-Robot Coordination with Semantic Communication](https://arxiv.org/abs/2610.02161) | 2026-10 | G | re-decide | multi-robot/sim |
| [ROMA: LLM System for Real-World Object-Centric Multi-Sensory Active Perception](https://arxiv.org/abs/2610.06955) | 2026-10 | C | re-decide | manip/real |
| [CIRRA: Dual-Level Continual Instruction Reconciliation with Ongoing Execution for Embodied Robot Agents in Interactive Household Tasks](https://arxiv.org/abs/2610.08862) | 2026-10 | G | re-decide | humanoid/real |
| [From Social Reasoning to Embodied Interaction: An Agentic Framework for Social Robots](https://arxiv.org/abs/2610.05964) | 2026-10 | G | re-decide | social/real |
| [Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843) | 2026-10 | G | re-decide | manip/sim+real |
| [Toward Evidence-Driven Human-Agent-Robot Teaming for Earth-Independent Anomaly Triage](https://arxiv.org/abs/2610.08933) | 2026-10 | G | re-decide | mobile-manip/real |
| CAD2Real: CAD-Grounded Skill Primitives and Vision-Language Planning for Precision Assembly `sim2real` | 2026-11 | G | re-decide | manip/sim+real |

</details>

<details><summary><b>Controller · Direct drivers</b> (83)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| From Ambiguous Language to Verifiable Plans: Integrating Formal Synthesis and Dynamic Affordance Reasoning | 2026 | G | authored | manip/sim |
| LLM-Grounded Dynamic Task Planning with Hierarchical Temporal Logic for Human-Aware Multi-Robot Collaboration | 2026 | G | re-decide | multi-robot/sim+real |
| Physical Simulation‐Based Correction of LLM‐Generated Tool‐Using Primitives `sim2real` | 2026-01 | G | re-decide | manip/sim+real |
| [Real2Sim via Active Perception with Behavior Trees Automatically Generated by VLMs](https://arxiv.org/abs/2601.08454) `real2sim` | 2026-01 | G | authored | manip/real |
| [Bidirectional Human-Robot Communication for Physical Human-Robot Interaction](https://arxiv.org/abs/2601.10796) | 2026-01 | G | re-decide | manip/real |
| [ALRM: Agentic LLM for Robotic Manipulation](https://arxiv.org/abs/2601.19510) | 2026-01 | G | re-decide | manip/sim |
| A Multimodal Adaptive Framework for Social Interaction with the MiRo-E Robot | 2026-02 | G | re-decide | social/real |
| [Coordinated Control of Multiple Construction Machines Using LLM-Generated Behavior Trees with Flag-Based Synchronization](https://arxiv.org/abs/2602.01041) | 2026-02 | G | authored | multi-robot/sim+real |
| [BTGenBot-2: Efficient Behavior Tree Generation with Small Language Models](https://arxiv.org/abs/2602.01870) | 2026-02 | C | re-decide | mobile-manip/sim+real |
| [VLN-Pilot: Large Vision-Language Model as an Autonomous Indoor Drone Operator](https://arxiv.org/abs/2602.05552) | 2026-02 | G | re-decide | aerial/sim |
| [AtomBridge: Agentic VLA Inference Plugin for Long-Horizon Tasks in Scientific Experiments](https://arxiv.org/abs/2602.09430) | 2026-02 | G | re-decide | manip/real |
| [LLM-Grounded Dynamic Task Planning with Hierarchical Temporal Logic for Human-Aware Multi-Robot Handover](https://arxiv.org/abs/2602.09472) | 2026-02 | G | authored | multi-robot/sim+real |
| LLM-Based Decision Making Framework for Autonomous Drone Navigation | 2026-02 | G | re-decide | aerial/sim |
| [Safe and Interpretable Multimodal Path Planning for Multi-Agent Cooperation](https://arxiv.org/abs/2602.19304) | 2026-02 | G | re-decide | multi-robot/sim+real |
| [ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking](https://arxiv.org/abs/2602.21161) | 2026-02 | G | re-decide | manip/sim |
| [SAGE-LLM: Towards Safe and Generalizable LLM Controller with Fuzzy-CBF Verification and Graph-Structured Knowledge Retrieval for UAV Decision](https://arxiv.org/abs/2602.23719) | 2026-02 | G | re-decide | aerial/sim |
| [From Dialogue to Execution: Mixture-of-Agents Assisted Interactive Planning for Behavior Tree-Based Long-Horizon Robot Execution](https://arxiv.org/abs/2603.01113) | 2026-03 | G | authored | manip/real |
| [EmboAlign: Aligning Video Generation with Compositional Constraints for Zero-Shot Manipulation](https://arxiv.org/abs/2603.05757) | 2026-03 | G | none | manip/real |
| [RACAS: Controlling Diverse Robots With a Single Agentic System](https://arxiv.org/abs/2603.05621) | 2026-03 | G | re-decide | other/real |
| [Reasoning Knowledge-Gap in Drone Planning via LLM-based Active Elicitation](https://arxiv.org/abs/2603.07824) | 2026-03 | G | re-decide | aerial/sim+real |
| Towards Autonomous UAV Visual Object Search in City Space: Benchmark and Agentic Methodology | 2026-03 | G | re-decide | aerial/sim |
| “I Loved How Pepper Talked About My Hoodie”: A Situated, MI-Grounded Multimodal Architecture for Engaging Conversation | 2026-03 | G | re-decide | social/real |
| [The Robot’s Inner Critic: Self-Refinement of Social Behaviors through VLM-based Replanning](https://arxiv.org/abs/2603.20164) | 2026-03 | G | re-decide | social/sim |
| [Can a Robot Walk the Robotic Dog: Triple-Zero Collaborative Navigation for Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2603.21723) | 2026-03 | G | re-decide | multi-robot/real |
| [A Multimodal Framework for Human-Multi-Agent Interaction](https://arxiv.org/abs/2603.23271) | 2026-03 | G | re-decide | social/real |
| [PhotoAgent: A Robotic Photographer with Spatial and Aesthetic Understanding](https://arxiv.org/abs/2603.22796) `real2sim2real` | 2026-03 | G | re-decide | other/sim+real |
| [Learning Structured Robot Policies from Vision-Language Models via Synthetic Neuro-Symbolic Supervision](https://arxiv.org/abs/2604.02812) | 2026-04 | C | authored | manip/sim+real |
| [CoEnv: Driving Embodied Multi-Agent Collaboration via Compositional Environment](https://arxiv.org/abs/2604.05484) `real2sim2real` | 2026-04 | G | re-decide | multi-robot/sim+real |
| [BLaDA: Bridging Language to Functional Dexterous Actions within 3DGS Fields](https://arxiv.org/abs/2604.08410) | 2026-04 | G | none | manip/real |
| [CLASP: Closed-loop Asynchronous Spatial Perception for Open-vocabulary Desktop Object Grasping](https://arxiv.org/abs/2604.11320) | 2026-04 | G | re-decide | manip/real |
| [FineCog-Nav: Integrating Fine-grained Cognitive Modules for Zero-shot Multimodal UAV Navigation](https://arxiv.org/abs/2604.16298) | 2026-04 | G | re-decide | aerial/sim |
| An Environment-Aware Verification Framework for LLM-Generated Robot Control Programs | 2026-04 | G | authored | manip/sim |
| Lingo2Action: Fusing Semantic Risk and Perceptual Uncertainty for Adaptive 3D Value Maps | 2026-04 | G | none | manip/sim+real |
| [CoRAL: Contact-Rich Adaptive LLM-based Control for Robotic Manipulation](https://arxiv.org/abs/2605.02600) | 2026-05 | G | re-decide | manip/sim+real |
| [LASSA Architecture-Based Autonomous Fault-Tolerant Control of Unmanned Underwater Vehicles](https://arxiv.org/abs/2605.09494) | 2026-05 | G | re-decide | other/sim+real |
| [LMPath: Language-Mediated Priors and Path Generation for Aerial Exploration](https://arxiv.org/abs/2605.13782) | 2026-05 | G | none | aerial/real |
| [Agentic Language-to-Objective Synthesis for Optofluidic Assembly](https://arxiv.org/abs/2605.27643) | 2026-05 | G | authored | other/sim+real |
| [GSAM: A Generalizable and Safe Robotic Framework for Articulated Object Manipulation](https://arxiv.org/abs/2605.30740) | 2026-05 | G | none | manip/sim+real |
| AGRI-BT Robot: LLM-Driven Behaviour Trees and VLM Perception for Intelligent Autonomous Greenhouse Operations | 2026-06 | G | authored | mobile-manip/real |
| Embodied SelfRect Robot: A Multi-Large-Model Control Framework with Iterative Self-Correction for Robotic Manipulation | 2026-06 | G | re-decide | manip/real |
| LLM-DTS: Resilience Formation Control Via Semantic Reasoning and Adaptive Topology Switching | 2026-06 | G | re-decide | multi-robot/sim |
| Towards Large-Model-Guided UAV Navigation in Complex Environments | 2026-06 | G | re-decide | aerial/sim |
| [Generating Natural and Expressive Robot Gestures through Iterative Reinforcement Learning with Human Feedback using LLMs](https://arxiv.org/abs/2606.18747) | 2026-06 | G | re-decide | social/real |
| [ZeroDex: Zero-Shot Long-Horizon Dexterous Manipulation via Multi-View 3D-Grounded VLM Reasoning](https://arxiv.org/abs/2606.19340) | 2026-06 | G | none | manip/real |
| [RelAfford6D: Relational 6D Affordance Graphs for Constraint-Driven Robotic Manipulation](https://arxiv.org/abs/2606.27036) | 2026-06 | G | authored | manip/real |
| [Embedding Large Language Models into Flow Controls: An Agentic Framework for Adaptive and Trustworthy Automated Cooking](https://arxiv.org/abs/2608.04768) | 2026-06 | G | authored | manip/real |
| [Hypothesis-driven Model Expansion under Uncertainty for Open-World Robot Planning](https://arxiv.org/abs/2607.06501) | 2026-07 | G | re-decide | mobile-manip/sim+real |
| A dual-agent framework for physically grounded and syntactically verifiable industrial robot programming | 2026-07 | G | re-decide | manip/sim+real |
| [A Generative Partially Specified Finite State Machine Approach to Complex Behaviour Planning](https://arxiv.org/abs/2607.15674) | 2026-07 | G | authored | mobile-manip/sim |
| [STeP: Signal Temporal Logic for Precise Specifications for Action Generation with Vision Language Models](https://arxiv.org/abs/2607.18580) | 2026-07 | G | authored | manip/sim+real |
| LLM-in-the-Loop Variable Impedance Control: Towards Safe Generalized and Personalized Robotic Interactions | 2026-08 | G | re-decide | manip/real |
| Talk-to-Fly: An Agentic LLM Runtime for Natural-Language UAV Task Control | 2026-08 | G | re-decide | aerial/sim+real |
| Zero-Shot Affordance Exposure for Robotic Manipulation Via Object Repositioning | 2026-08 | G | none | manip/real |
| CoMuRoS - An LLM-based generalizable hierarchical task planning and execution framework for heterogeneous robot teams with event-driven re-planning | 2026-08 | G | re-decide | multi-robot/sim+real |
| [Closing the Affective Loop: Multimodal Speaker-Listener Emotion-Dynamics-Aware Empathetic Social Robots](https://arxiv.org/abs/2608.16686) | 2026-08 | G | re-decide | social/real |
| [PDDL-ART: Autonomous Symbolic Abstraction From Demonstration For Long-Horizon Robotic Manipulation Using Vision-Language Models](https://arxiv.org/abs/2608.17146) | 2026-08 | G | re-decide | manip/sim+real |
| [VLCP: Vision Language Control Policy Closed-Loop Code Replanning for Robot Manipulation](https://arxiv.org/abs/2608.16978) | 2026-08 | G | re-decide | manip/sim |
| [PhysCaP: Grounding Code-as-Policy Agent with Physics-Informed Exploration](https://arxiv.org/abs/2608.21031) | 2026-08 | G | re-decide | manip/sim+real |
| [EndoNav: Semantic-to-Geometric Grounding for Language-Guided Robotic Endoscopic Examination](https://arxiv.org/abs/2608.22093) | 2026-08 | G | none | manip/sim+real |
| [Leveraging Inter-object Affordances for Efficient Planning in Contact-rich Tasks](https://arxiv.org/abs/2608.25641) | 2026-08 | G | none | manip/sim+real |
| Behavior-triggered self-reflection for zero-shot open-domain UAV target search | 2026-09 | G | re-decide | aerial/sim |
| Empowering Precise Embodied Agents with Executable Analytic Concepts as Semantic-Physical Blueprints | 2026-09 | G | none | manip/sim+real |
| [La Agente Óptima: Towards Agentic Self-Driving Laboratories](https://arxiv.org/abs/2609.04564) | 2026-09 | G | re-decide | other/real |
| [Language-Guided Terrain-Adaptive Neural MPC for Autonomous Traversal of Articulated Tracked Robots](https://arxiv.org/abs/2609.13083) | 2026-09 | G | re-decide | loco/sim+real |
| [ManiSkillFormer: Demonstration-Free Compositional Manipulation via Geometric Contracts and Agentic Skill Graph](https://arxiv.org/abs/2609.16331) | 2026-09 | G | none | manip/real |
| [In-Context Robot Learning with VLM Agents](https://arxiv.org/abs/2609.19138) | 2026-09 | G | re-decide | manip/sim+real |
| [Coding Agents with Harness for Safe Robot Control](https://arxiv.org/abs/2609.20822) | 2026-09 | G | re-decide | manip/sim+real |
| [V2-STRep: VLM-Grounded Structured Task Representations for Reusable Robot Skills Acquired from Generated Videos](https://arxiv.org/abs/2609.20582) | 2026-09 | G | none | manip/real |
| [AgenticSwarm: Semantic Perception and Adaptive Task Allocation for Heterogeneous Multi-UAV Missions](https://arxiv.org/abs/2609.21716) | 2026-09 | G | authored | multi-robot/sim+real |
| [Search, Ground, Plan: Functional Sufficiency for Task and Motion Planning under Incomplete Scene Knowledge](https://arxiv.org/abs/2609.23113) | 2026-09 | G | re-decide | mobile-manip/sim |
| [Transferring the Intelligence of VLMs to Robotic Control](https://arxiv.org/abs/2609.22966) | 2026-09 | G | re-decide | manip/sim |
| [Generalizing Manipulation Skills with a Local Coding Agent](https://arxiv.org/abs/2609.26499) | 2026-09 | G | re-decide | manip/real |
| Execution-aware agent harness for accessible and responsible synthetic biology automation | 2026-09 | G | re-decide | other/real |
| [World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal](https://arxiv.org/abs/2609.29964) | 2026-09 | G | re-decide | manip/real |
| [DualManip: Agentic Dynamic Manipulation via Dual-Path Semantic Reasoning and Geometric Adaptation](https://arxiv.org/abs/2609.31112) | 2026-09 | G | re-decide | manip/real |
| [Bayesian Active Learning for Intent Disambiguation in Interactive Robot Planning](https://arxiv.org/abs/2609.34270) | 2026-09 | G | none | manip/sim+real |
| [From Language to Task Maps: Compiling Semantic Relations While Preserving Task-Relevant Freedom](https://arxiv.org/abs/2609.34412) | 2026-09 | G | authored | manip/sim |
| [RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261) | 2026-09 | G | re-decide | manip/sim |
| [MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation](https://arxiv.org/abs/2609.38078) | 2026-09 | G | re-decide | manip/sim+real |
| [WayFinder: Hierarchical Visual-Language-Action for Zero-Shot Waypoint Generation and Low-Level Kinematic Control](https://arxiv.org/abs/2609.37922) | 2026-09 | G | re-decide | aerial/sim |
| [OrbitTAMP: Grounding Language Models for Task and Motion Planning in Spacecraft Rendezvous](https://arxiv.org/abs/2610.01093) | 2026-10 | G | none | other/sim |
| [TacZero: Training-Free Peg Insertion Using a General-Purpose Vision-Language Model with Tactile Feedback](https://arxiv.org/abs/2610.07621) | 2026-10 | G | re-decide | manip/real |
| [Adaptive Code Generation for Controlling Robots](https://arxiv.org/abs/2610.09588) | 2026-10 | G | re-decide | loco/sim |

</details>

<details><summary><b>Controller · Lifelong / memory agents</b> (33)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Learning Without Losing Identity: Capability Evolution for Embodied Agents](https://arxiv.org/abs/2604.07799) | 2026 | G | re-decide | manip/sim |
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

<details><summary><b>VLN and embodied navigation</b> (52)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| AgenticNav: A Hierarchical Multi-Agentic System for LLM-Driven Autonomous Problem-Solving in Robotics | 2026 | G | re-decide | nav/sim+real |
| EmergeNav: Structured Embodied Inference for Zero-Shot Vision-and-Language Navigation in Continuous Environments | 2026 | G | re-decide | nav/sim |
| From Natural Language to Nonlinear Programs: An Agentic Framework for Instruction-Guided Trajectory Planning of Wheeled Robots | 2026 | G | re-decide | nav/sim |
| VOCA: A VLM-Optimized Call Approach for Zero-Shot Navigation Using Target-Context Cues | 2026 | G | re-decide | nav/sim |
| [Visual-Language-Guided Task Planning for Horticultural Robots](https://arxiv.org/abs/2601.11906) | 2026-01 | G | re-decide | nav/sim |
| [IROS: A Dual-Process Architecture for Real-Time VLM-Based Indoor Navigation](https://arxiv.org/abs/2601.21506) | 2026-01 | G | re-decide | nav/real |
| [MerNav: A Highly Generalizable Memory-Execute-Review Framework for Zero-Shot Object Goal Navigation](https://arxiv.org/abs/2602.05467) | 2026-02 | G | re-decide | nav/sim+real |
| [3DGSNav: Enhancing Vision-Language Model Reasoning for Object Navigation via Active 3D Gaussian Splatting](https://arxiv.org/abs/2602.12159) | 2026-02 | G | re-decide | nav/sim+real |
| [Global Commander and Local Operative: A Dual-Agent Framework for Scene Navigation](https://arxiv.org/abs/2602.18941) | 2026-02 | G | re-decide | nav/sim |
| [SFCo-Nav: Efficient Zero-Shot Visual Language Navigation via Collaboration of Slow LLM and Fast Attributed Graph Alignment](https://arxiv.org/abs/2603.01477) | 2026-03 | G | re-decide | nav/sim |
| [MA-CoNav: A Master-Slave Multi-Agent Framework with Hierarchical Collaboration and Dual-Level Reflection for Long-Horizon Embodied VLN](https://arxiv.org/abs/2603.03024) | 2026-03 | G | re-decide | nav/sim |
| [CMMR-VLN: Vision-and-Language Navigation via Continual Multimodal Memory Retrieval](https://arxiv.org/abs/2603.07997) | 2026-03 | G | re-decide | nav/sim+real |
| [LightZeroNav: Zero-Shot Vision Language Navigation in Continuous Environments Based on Lightweight VLMs](https://arxiv.org/abs/2603.16947) | 2026-03 | G | re-decide | nav/sim |
| Perception–Awareness–Decision: Socially‑Aware Robot Navigation and Interaction | 2026-03 | G | re-decide | nav/real |
| [Interpreting Context-Aware Human Preferences for Multi-Objective Robot Navigation](https://arxiv.org/abs/2603.17510) | 2026-03 | G | re-decide | nav/sim |
| [OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms](https://arxiv.org/abs/2603.17351) | 2026-03 | G | re-decide | nav/real |
| A Generalised Robot Control Architecture with Large Language Model and Model Context Protocol | 2026-04 | G | re-decide | nav/sim |
| [Explore Like Humans: Autonomous Exploration with Online SG-Memo Construction for Embodied Agents](https://arxiv.org/abs/2604.19034) | 2026-04 | G | re-decide | nav/sim |
| [Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance](https://arxiv.org/abs/2604.26839) | 2026-04 | G | re-decide | nav/real |
| USV-3.0: Cognitive maritime navigation through vision-language models, Human-in-the-Loop learning, and spatio-temporal memory | 2026-05 | G | re-decide | nav/real |
| Agile assistive hospital robot for suboptimal Task execution in dynamic environments | 2026-05 | G | re-decide | nav/real |
| [Bridging the 2D-3D Gap: A Hierarchical Semantic-Geometric Map for Vision Language Navigation](https://arxiv.org/abs/2606.00095) | 2026-05 | G | re-decide | nav/sim |
| [Uni-LaViRA: Language-Vision-Robot Actions Translation for Unified Embodied Navigation](https://arxiv.org/abs/2605.27582) | 2026-05 | G | re-decide | nav/sim+real |
| Déjà Vu: Unlocking Transparent Action Reasoning for Object-Goal Navigation via Large Language Models | 2026-06 | G | re-decide | nav/sim |
| [EvoMemNav: Efficient Self-Evolving Fine-Grained Memory for Zero-Shot Embodied Navigation](https://arxiv.org/abs/2606.03509) | 2026-06 | G | re-decide | nav/sim |
| [SpaceVLN: A Zero-Shot Vision-and-Language Navigation Agent with Online Spatial Cognitive Memory and Reasoning](https://arxiv.org/abs/2606.08992) | 2026-06 | G | re-decide | nav/sim |
| [EvolveNav: Proactive Preflection and Self-Evolving Memory for Zero-Shot Object Goal Navigation](https://arxiv.org/abs/2606.18235) | 2026-06 | G | re-decide | nav/sim |
| [RAVEN: Long-Horizon Reasoning & Navigation with a Visuo-Spatio-Temporal Memory](https://arxiv.org/abs/2606.25206) | 2026-06 | G | re-decide | nav/real |
| [SAGE-Nav: Leveraging LLM Planning and Alignment Fusion for Hierarchical Scene Graph-Guided Navigation](https://arxiv.org/abs/2606.25497) | 2026-06 | G | re-decide | nav/sim |
| [ViTL: Temporal Logic-Guided Zero-Shot Natural Language Navigation via Vision-Language Models](https://arxiv.org/abs/2606.30696) | 2026-06 | G | authored | nav/sim |
| Agentic Llm-Driven Human-Robot Interaction | 2026-07 | G | re-decide | nav/sim |
| Safety-Aware Optimal Control With Language-Guided Online Parameter Adjustment via Large Language Models | 2026-07 | G | authored | nav/sim+real |
| Enabling reliable navigation for lightweight VLMs via a Semantically-Gated Visual servoing framework | 2026-08 | G | re-decide | nav/real |
| IRAZON: Iterative ReAct With LLMs for Adaptive Zero-Shot Object Goal Navigation | 2026-08 | G | re-decide | nav/sim |
| [Hierarchical Fast-Slow ReAct Agent for Zero-Shot Object-Goal Navigation](https://arxiv.org/abs/2608.09816) | 2026-08 | G | re-decide | nav/sim |
| [SAIN: Structure-Aware Interactive Navigation with Active Dialogue Grounding for Mobile Robot](https://arxiv.org/abs/2608.09196) | 2026-08 | G | re-decide | nav/sim |
| [Embodied-Navigator: Point, Think, Memorize, and Align for Efficient Navigation](https://arxiv.org/abs/2608.17512) | 2026-08 | C | re-decide | nav/sim+real |
| Open-Vocabulary, Context-Aware Robot Navigation on Construction Sites: Integrating LLM-Driven Value Map Composition with Hierarchical Scene Graphs | 2026-08 | G | none | nav/sim+real |
| [CGFM-Nav: Cognitive Graph-Field Memory for Semantic-Guided Lifelong Multimodal Embodied Navigation](https://arxiv.org/abs/2608.29114) | 2026-08 | G | re-decide | nav/sim |
| [Scaffolding Foundation Models into Physical-World Agents Pushes the Frontier of Long-Horizon Navigation](https://arxiv.org/abs/2608.30396) | 2026-08 | G | re-decide | nav/sim |
| [AnchorVLN: Geometry-Anchored Vision-Language Grounding Reasoning for Open-Vocabulary Navigation](https://arxiv.org/abs/2609.12285) | 2026-09 | G | re-decide | nav/sim+real |
| [Bridging Thought and Action: Taming Long-Horizon Instability in Open-Source LLM Agents with a MetaTool-Enhanced ROS Framework](https://arxiv.org/abs/2609.13335) | 2026-09 | G | re-decide | nav/real |
| [Navi-Agent: Unlocalized Monocular Navigation Agent](https://arxiv.org/abs/2609.20388) | 2026-09 | G | re-decide | nav/sim |
| [Deploying Foundation Models for Embodied Navigation](https://arxiv.org/abs/2609.25666) | 2026-09 | G | re-decide | nav/sim+real |
| [Hierarchical Floorplan-Guided Vision-Language Exploration for Embodied Question Answering](https://arxiv.org/abs/2609.26360) | 2026-09 | G | re-decide | nav/sim |
| [SparseNav: Instruction-conditioned Sparse Semantic Perception for Training-Free Vision-Language Navigation](https://arxiv.org/abs/2609.26408) | 2026-09 | G | re-decide | nav/sim |
| [Spatial and Semantic Reasoning for LLM-Driven Robot Navigation via MCP](https://arxiv.org/abs/2609.27340) | 2026-09 | G | re-decide | nav/sim |
| [Actively Resolving Contextual Uncertainty for Underspecified Tasks in Natural Language](https://arxiv.org/abs/2609.30428) | 2026-09 | G | re-decide | nav/real |
| [RECAST: Recasting Vision-Language Semantics into an Actionable Cost Map for Robot Navigation](https://arxiv.org/abs/2609.32595) | 2026-09 | G | none | nav/sim+real |
| [NavHarness: Towards Lifelong Embodied Navigation](https://arxiv.org/abs/2609.34276) | 2026-09 | G | re-decide | nav/sim |
| [NavHarness: Adaptive Goals for Agentic Vision-Language Navigation](https://arxiv.org/abs/2609.39915) | 2026-09 | G | re-decide | nav/sim |
| [PreAct-Nav: Agentic Reasoning Before Action for Urban Navigation](https://arxiv.org/abs/2610.04916) | 2026-10 | G | re-decide | nav/sim |

</details>

<details><summary><b>Supervisor</b> (27)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| Anomaly Management in Multi-Robot Coordination: Detection and Handling Framework for Self-Driving Laboratories | 2026 | G | re-decide | multi-robot/sim+real |
| IEI-TIA: Industrial Embodied Intelligence Trustworthy Interpretable Agent for Robotic Long-Horizon and Repetitive Tasks | 2026 | C | re-decide | manip/sim+real |
| Robust Task Planning via Failure Detection Using Scene Graph From Multi-View Images | 2026-02 | G | re-decide | manip/sim+real |
| [StageCraft: Execution Aware Mitigation of Distractor and Obstruction Failures in VLA Models](https://arxiv.org/abs/2603.20659) | 2026-03 | G | re-decide | manip/sim+real |
| [RoboHarness: A Memory-Augmented Policy Harness for Vision-Language-Action Model Robustness via In-Context Adaptation](https://arxiv.org/abs/2603.24060) | 2026-03 | G | re-decide | manip/sim |
| [Stop Wandering: Efficient Vision-Language Navigation via Metacognitive Reasoning](https://arxiv.org/abs/2604.02318) | 2026-04 | G | re-decide | nav/sim |
| LLM-Assisted Plan Execution for Robots in Dynamic Environments | 2026-04 | G | re-decide | nav/sim |
| [LLM-Guided Safety Agent for Edge Robotics with an ISO-Compliant Perception-Compute-Control Architecture](https://arxiv.org/abs/2604.20193) | 2026-04 | G | authored | manip/real |
| [Robot Planning and Situation Handling with Active Perception](https://arxiv.org/abs/2604.26988) | 2026-04 | G | re-decide | mobile-manip/sim+real |
| Failure Detection With Zero-Shot Error Correction in Robotic Manipulation | 2026-05 | G | re-decide | manip/sim+real |
| Grasp, Reason, Act: Tactile-Language Model for Zeroshot Sim2real Grasp Stability Prediction and Re-Grasping | 2026-05 | C | re-decide | manip/sim+real |
| Vision-Guided Recovery: Enhancing Robotic Manipulation through Intelligent Failure Detection | 2026-05 | G | re-decide | manip/sim |
| [Make Your VLA More Robust Without More Data By Interleaving Motion Planning](https://arxiv.org/abs/2606.00985) | 2026-05 | G | re-decide | mobile-manip/sim+real |
| VigiClaw: Action-Triggered State Verification for Robust Long-Horizon Robotic Manipulation | 2026-07 | G | re-decide | manip/sim |
| [Learning Robust Execution in Robotic Manipulation with Agentic Reinforcement Learning](https://arxiv.org/abs/2607.13818) | 2026-07 | C | re-decide | manip/sim |
| [From Sign Language Generation to Humanoid Execution: Vision-Language Guided Retargeting with Collision Mitigation](https://arxiv.org/abs/2607.17769) | 2026-07 | G | re-decide | humanoid/sim |
| [FORGE-plus: Force-Budgeted Recovery for Contact-Rich Assembly with a Frozen LLM Supervisor](https://arxiv.org/abs/2607.21227) | 2026-07 | G | re-decide | manip/sim |
| Predictive vision-language monitoring for proactive safety in robot task execution | 2026-08 | G | re-decide | mobile-manip/sim |
| [Safe Task Planning with Long-Term Graph Memory for Embodied Agents](https://arxiv.org/abs/2609.08444) | 2026-09 | G | re-decide | mobile-manip/sim+real |
| [REVOLVE: An Automated Closed-Loop Framework for Evolving Robot Manipulation with Minimal Human Intervention](https://arxiv.org/abs/2609.14633) | 2026-09 | G | re-decide | manip/real |
| [Talk2Escape: Conversational Grounding for Vision-and-Language Navigation](https://arxiv.org/abs/2609.28296) | 2026-09 | G | re-decide | nav/sim |
| [Body-Grounded Replanning for Physically Adaptive Manipulation](https://arxiv.org/abs/2609.30024) | 2026-09 | G | re-decide | manip/sim+real |
| [SOR-Nav: Search or Relocate? Context-Gated Exploration and Cross-Region Relocation for Object Navigation](https://arxiv.org/abs/2609.34707) | 2026-09 | G | re-decide | nav/sim |
| [ProAct-VLM: Pre-Failure Vision-Language Task Replanning with Continuous Perception Feedback](https://arxiv.org/abs/2609.37681) | 2026-09 | G | re-decide | manip/real |
| [Spotter: Let the Embodied Model Lead, and the VLM Reflect for It](https://arxiv.org/abs/2609.36808) | 2026-09 | G | re-decide | manip/sim+real |
| [AVERT-VLN: Abstention-aware Visual Error Recovery and Training for Vision-and-Language Navigation](https://arxiv.org/abs/2609.39579) | 2026-09 | C | re-decide | nav/sim |
| [AeroEval: Staged Program and Execution Validation for AI-Generated Drone Missions](https://arxiv.org/abs/2610.09764) | 2026-10 | G | re-decide | aerial/sim |

</details>

<details><summary><b>Teacher</b> (18)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [V-CAGE: Context-Aware Generation and Verification for Scalable Long-Horizon Embodied Tasks](https://arxiv.org/abs/2601.15164) | 2026-01 | G | re-decide | manip/sim |
| [Accelerating Robotic Reinforcement Learning with Agent Guidance](https://arxiv.org/abs/2602.11978) | 2026-02 | G | re-decide | manip/real |
| [Scene2Demo: Self-Evolving Embodied Data Generation via Object-Action Graph](https://arxiv.org/abs/2602.12065) `real2sim` | 2026-02 | G | re-decide | manip/sim |
| Gentle Manipulation of Long-Horizon Tasks Without Human Demonstrations | 2026-03 | G | re-decide | manip/sim+real |
| [MotionDisco: Motion Discovery for Extreme Humanoid Loco-Manipulation](https://arxiv.org/abs/2606.06139) `sim2real` | 2026-06 | G | re-decide | humanoid/sim+real |
| [HATS: A Human-Agent Teleoperation System for Multi-Arm Data Collection](https://arxiv.org/abs/2606.16491) | 2026-06 | G | re-decide | manip/real |
| [InSight: Self-Guided Skill Acquisition via Steerable VLAs](https://arxiv.org/abs/2606.24884) | 2026-06 | G | re-decide | manip/real |
| [Zero2Skill: Bootstrapping Robot Skills through Autonomous Data Collection, Training, and Deployment](https://arxiv.org/abs/2607.14047) | 2026-07 | G | re-decide | manip/real |
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

<details><summary><b>Designer</b> (51)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| AgenticRL: Self-Refining Agentic Reinforcement Learning for Vision-Conditioned UAV Navigation | 2026 | G | re-decide | aerial/sim |
| LLM-Based Dynamic Event-Triggered Communication for Multi-UAV Formation Control in Urban Environments | 2026 | G | re-decide | multi-robot/sim |
| Xmobot: Enabling Rapid Build-and-Train Robotics Education With Agentic AI | 2026 | G | re-decide | nav/sim+real |
| GAIA: Generating Task Instruction Aware Simulation Grounded in Real Contexts Using Vision-Language Models `real2sim` | 2026-01 | G | none | manip/sim |
| [AGILE: Hand-object Interaction Reconstruction from Video via Agentic Generation](https://arxiv.org/abs/2602.04672) `real2sim` | 2026-02 | G | none | manip/sim |
| [FATE: Closed-Loop Feasibility-Aware Task Generation with Active Repair for Physically Grounded Robotic Curricula](https://arxiv.org/abs/2603.01505) | 2026-03 | G | re-decide | manip/sim |
| [Tether: Autonomous Functional Play with Correspondence-Driven Trajectory Warping](https://arxiv.org/abs/2603.03278) | 2026-03 | G | re-decide | manip/real |
| [PRISM: Personalized Refinement of Imitation Skills for Manipulation via Human Instructions](https://arxiv.org/abs/2603.05574) | 2026-03 | G | re-decide | manip/sim |
| [RADAR: Closed-Loop Robotic Data Generation via Semantic Planning and Autonomous Causal Environment Reset](https://arxiv.org/abs/2603.11811) | 2026-03 | G | re-decide | manip/real |
| Clarifying Constraints in Interactive Robot Learning with Language Feedback | 2026-03 | G | re-decide | manip/sim |
| [Swim2Real: VLM-Guided System Identification for Sim-to-Real Transfer](https://arxiv.org/abs/2603.20827) `real2sim2real` | 2026-03 | G | re-decide | other/sim+real |
| Constraint-Aware LLM Pipeline for EvoGym Environment Generation with Fitness-Guided Prompt Refinement | 2026-03 | G | re-decide | other/sim |
| [GenPHRI: Agentic Generative Simulation for Physical Human-Robot Interaction](https://arxiv.org/abs/2604.08664) `sim2real` | 2026-04 | G | re-decide | manip/sim+real |
| [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](https://arxiv.org/abs/2604.09036) | 2026-04 | G | re-decide | manip/sim |
| CAAI-ST: Constraint-Aware AI-Guided Seed Generation and Mutation for CPS-UAV System Testing | 2026-04 | G | re-decide | aerial/sim |
| [Chain of Uncertain Rewards with Large Language Models for Reinforcement Learning](https://arxiv.org/abs/2604.13504) | 2026-04 | G | re-decide | manip/sim |
| [EmbodiedClaw: Conversational Workflow Execution for Embodied AI Development](https://arxiv.org/abs/2604.13800) | 2026-04 | G | re-decide | other/sim |
| MotionVL: Vision-Language Supervision for Reinforcement Learning of Humanoid Motion `sim2real` | 2026-05 | G | re-decide | humanoid/sim+real |
| [Discovering Reinforcement Learning Interfaces with Large Language Models](https://arxiv.org/abs/2605.03408) | 2026-05 | G | re-decide | loco/sim |
| [SimWorld Studio: Automatic Environment Generation with Evolving Coding Agent for Embodied Agent Learning](https://arxiv.org/abs/2605.09423) | 2026-05 | G | re-decide | other/sim |
| [JODA: Composable Joint Dynamics for Articulated Objects](https://arxiv.org/abs/2605.09954) `real2sim` | 2026-05 | G | none | manip/sim |
| [Agentic-VLA: Efficient Online Adaptation for Vision-Language-Action Models](https://arxiv.org/abs/2605.22896) | 2026-05 | G | re-decide | manip/sim |
| A VLM-Driven High-Fidelity Domain Randomization Framework for Imitation Learning `real2sim` | 2026-06 | G | none | manip/sim |
| LLM-Supervised Semantic Reward Adaptation for Reinforcement Learning-Based Robot Locomotion | 2026-06 | G | re-decide | loco/sim |
| [AgenticRL: Agentic Reinforcement Learning with Self-Refinement for Complex UAV Navigation](https://arxiv.org/abs/2606.03963) | 2026-06 | G | re-decide | aerial/sim |
| [RoboLineage: Agent-Native Data Lifecycle Governance Across Robot Policy Iterations](https://arxiv.org/abs/2606.22142) | 2026-06 | G | re-decide | manip/real |
| [CoRe: Combined Rewards with Vision-Language Model Feedback for Preference-Aligned Reinforcement Learning](https://arxiv.org/abs/2607.01721) | 2026-07 | G | re-decide | other/sim |
| [PRISM: Personalized Robotic Dataset Generation via Image-based Scene and Motion Synthesis](https://arxiv.org/abs/2607.04880) `real2sim2real` | 2026-07 | G | none | manip/sim+real |
| [EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI](https://arxiv.org/abs/2607.07459) | 2026-07 | G | re-decide | manip/sim+real |
| [Prompt-Driven Exploration](https://arxiv.org/abs/2607.08837) | 2026-07 | G | re-decide | manip/sim |
| [MLREF: Efficient Module Reuse for Reward Design in Reinforcement Learning via Large Language Models](https://arxiv.org/abs/2608.18827) | 2026-08 | G | re-decide | other/sim |
| [NeoWorld-Pro: Programming Interactive Scenes from Monocular Images for Embodied Simulation](https://arxiv.org/abs/2608.24212) `real2sim` | 2026-08 | G | re-decide | manip/sim |
| [DREAM: Deployment-Time Demonstration Generation via Real-to-Sim for Scalable Policy Adaptation](https://arxiv.org/abs/2608.29078) `real2sim2real` | 2026-08 | G | authored | manip/sim+real |
| [Autonomously Acquiring Robot Manipulation Skills with Language-Driven Quality-Diversity](https://arxiv.org/abs/2608.30983) | 2026-08 | G | re-decide | manip/sim |
| [Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling](https://arxiv.org/abs/2608.30821) `real2sim` | 2026-08 | C | re-decide | manip/sim |
| [SUN: Agentic Robot Policy Learning with Persistent Task Programs](https://arxiv.org/abs/2608.31167) `sim2real` | 2026-08 | G | re-decide | manip/sim+real |
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
| [Video2SwimFish: An Automated Pipeline for Reconstructing Controllable Fish Models and Biological Locomotion from Real Fish Videos](https://arxiv.org/abs/2609.38966) `real2sim` | 2026-09 | G | re-decide | other/sim |
| [Awomo-SimDataEngine: Agentic Simulation-ReadyWorld Generation](https://arxiv.org/abs/2610.02274) | 2026-10 | G | re-decide | manip/sim |
| [LiteReality-Agent: An Agentic System for Interactable 3D Indoor Scene Reconstruction](https://arxiv.org/abs/2610.01863) `real2sim` | 2026-10 | G | re-decide | other/sim |
| [EnvDreamer: Large-Scale Multimodal-to-Environment Generation for Embodied AI](https://arxiv.org/abs/2610.04301) `real2sim` | 2026-10 | G | re-decide | mobile-manip/sim |
| [Demo: Vision-Language Model-Guided Online Calibration of an Electromagnetic Digital Twin](https://arxiv.org/abs/2610.07081) `real2sim` | 2026-10 | G | re-decide | humanoid/real |

</details>

<details><summary><b>Developer</b> (44)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [ModuLoop: Low-Level Code Generation Using Modular Synthesizer and Closed-Loop Debugger for Robotic Control](https://arxiv.org/abs/2606.03047) | 2025-12 | G | re-decide | manip/real |
| RoboRSI: Stable, Efficient, and Reusable Robot Self-Evolution in Complex Real-World Environments | 2026 | G | re-decide | manip/sim+real |
| [Test-Driven Agentic Framework for Reliable Robot Controller](https://arxiv.org/abs/2603.00455) | 2026-02 | G | re-decide | nav/sim |
| [Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation](https://arxiv.org/abs/2603.04466) | 2026-03 | G | re-decide | manip/sim |
| [CABTO: Context-Aware Behavior Tree Grounding for Robot Manipulation](https://arxiv.org/abs/2603.16809) | 2026-03 | G | re-decide | manip/sim |
| [Agent-Driven Autonomous Reinforcement Learning Research: Iterative Policy Improvement for Quadruped Locomotion](https://arxiv.org/abs/2603.27416) | 2026-03 | G | re-decide | loco/sim |
| Hybrid LLM-Genetic Programming: Supervising and Generating Diverse Behavior Trees for Autonomous Robot Evolution | 2026-05 | G | re-decide | other/sim |
| [Nautilus: From One Prompt to Plug-and-Play Robot Learning](https://arxiv.org/abs/2605.11665) | 2026-05 | G | re-decide | manip/sim+real |
| [When Search Becomes Memory: Accelerating Robot Design Discovery with Self-Evolving Skills](https://arxiv.org/abs/2605.25832) | 2026-05 | G | re-decide | other/sim |
| [When are LLMs Sufficient Policy Optimizers for Sequential RL Tasks?](https://arxiv.org/abs/2605.30719) | 2026-05 | G | re-decide | manip/sim |
| [VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents](https://arxiv.org/abs/2606.05395) | 2026-06 | G | re-decide | manip/sim |
| [Self-Evolving Scientific Agent Designs Physically Reasoned White-Box Fluid Control](https://arxiv.org/abs/2606.08405) | 2026-06 | G | re-decide | other/sim |
| [Agentic AutoResearch forSpace Autonomy: An Auditable, LLM-Driven Research Agent for Aerospace Control Problems](https://arxiv.org/abs/2606.20394) | 2026-06 | G | re-decide | other/sim |
| [AI Training Manager: Bounded Closed-Loop Control of Adaptive Training Recipes](https://arxiv.org/abs/2606.29871) | 2026-06 | G | re-decide | manip/sim |
| [Automating the Design of Embodied AgentArchitectures](https://arxiv.org/abs/2606.30111) | 2026-06 | G | re-decide | mobile-manip/sim |
| Agents Trainer: Automatically Training Multi-Agent Reinforcement Learning Models for Drone Swarm Using Language Model-Based Agents | 2026-07 | G | re-decide | aerial/sim |
| Automated UAV Controller Synthesis via LLM-Generated Control Logic and Particle Swarm Optimization `sim2real` | 2026-07 | G | re-decide | aerial/sim+real |
| [GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks](https://arxiv.org/abs/2607.05369) `real2sim2real` | 2026-07 | G | re-decide | manip/sim+real |
| LLMigrate: Large Language Models as Migration Controllers in Island-Based Evolutionary Design of Soft Robots | 2026-07 | G | re-decide | other/sim |
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
| [Encore: Few-Shot Agentic Discovery of Manipulation Strategies](https://arxiv.org/abs/2609.37359) | 2026-09 | G | re-decide | manip/sim |
| [DynaHarness: A Dynamic Physical Harness for Self-Evolving Robot Agents](https://arxiv.org/abs/2609.40306) | 2026-09 | G | re-decide | manip/sim+real |
| [Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents](https://arxiv.org/abs/2609.39304) | 2026-09 | G | re-decide | manip/sim |
| [Iterative Policy Refinement through Semantic Rollout Analysis](https://arxiv.org/abs/2610.01652) | 2026-10 | G | re-decide | manip/sim |
| [EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432) | 2026-10 | G | re-decide | mobile-manip/sim |
| [PEARS: Physical-Prior-Guided Efficient Adaptation via Failure Reasoning and Diffusion Steering for Tactile Manipulation](https://arxiv.org/abs/2610.08784) | 2026-10 | G | re-decide | manip/real |
| [EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution](https://arxiv.org/abs/2610.10498) | 2026-10 | G | re-decide | manip/sim+real |

</details>


## More papers from 2022–2025

384 further papers from 2022–2025 that meet the definition (judged `core` by a verification pass) but are not in the curated tables above. Tags come from the judging pass and are not hand-checked; generated by `scripts/build_extended.py`.

<details><summary><b>Controller · Orchestrators</b> (156)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [CAPE: Corrective Actions from Precondition Errors using Large Language Models](https://arxiv.org/abs/2211.09935) | 2022-11 | G | re-decide | mobile-manip/sim+real |
| [Grounded Decoding: Guiding Text Generation with Grounded Models for Embodied Agents](https://arxiv.org/abs/2303.00855) | 2023-03 | G | re-decide | mobile-manip/sim+real |
| [Chat with the Environment: Interactive Multimodal Perception Using Large Language Models](https://arxiv.org/abs/2303.08268) | 2023-03 | G | re-decide | manip/real |
| [ERRA: An Embodied Representation and Reasoning Architecture for Long-Horizon Language-Conditioned Manipulation Tasks](https://arxiv.org/abs/2304.02251) | 2023-04 | G | re-decide | manip/sim+real |
| [AlphaBlock: Embodied Finetuning for Vision-Language Reasoning in Robot Manipulation](https://arxiv.org/abs/2305.18898) | 2023-05 | C | re-decide | manip/sim+real |
| [Toward Grounded Commonsense Reasoning](https://arxiv.org/abs/2306.08651) | 2023-06 | G | re-decide | manip/real |
| Grounded Decoding: Guiding Text Generation with Grounded Models for Robot Control | 2023-07 | G | re-decide | mobile-manip/sim+real |
| [HiCRISP: An LLM-Based Hierarchical Closed-Loop Robotic Intelligent Self-Correction Planner](https://arxiv.org/abs/2309.12089) | 2023-09 | G | re-decide | manip/sim+real |
| [Self-Recovery Prompting: Promptable General Purpose Service Robot System with Foundation Models and Self-Recovery](https://arxiv.org/abs/2309.14425) | 2023-09 | G | re-decide | mobile-manip/sim+real |
| [Dobby: A Conversational Service Robot Driven by GPT-4](https://arxiv.org/abs/2310.06303) | 2023-10 | G | re-decide | social/real |
| [CoPAL: Corrective Planning of Robot Actions with Large Language Models](https://arxiv.org/abs/2310.07263) | 2023-10 | G | re-decide | manip/sim+real |
| [Interactive Task Planning with Language Models](https://arxiv.org/abs/2310.10645) | 2023-10 | G | re-decide | manip/real |
| [REAL: Resilience and Adaptation using Large Language Models on Autonomous Aerial Robots](https://arxiv.org/abs/2311.01403) | 2023-11 | G | re-decide | aerial/real |
| [Agent as Cerebrum, Controller as Cerebellum: Implementing an Embodied LMM-based Agent on Drones](https://arxiv.org/abs/2311.15033) | 2023-11 | G | re-decide | aerial/sim+real |
| [LLM-State: Open World State Representation for Long-horizon Task Planning with Large Language Model](https://arxiv.org/abs/2311.17406) | 2023-11 | G | re-decide | manip/sim+real |
| [Interactive Planning Using Large Language Models for Partially Observable Robotic Tasks](https://arxiv.org/abs/2312.06876) | 2023-12 | G | re-decide | manip/sim+real |
| [MOSAIC: Modular Foundation Models for Assistive and Interactive Cooking](https://arxiv.org/abs/2402.18796) | 2024 | G | re-decide | multi-robot/real |
| Robi Butler: Remote Multimodal Interactions with Household Robot Assistant | 2024 | G | re-decide | mobile-manip/real |
| [RePLan: Robotic Replanning with Perception and Language Models](https://arxiv.org/abs/2401.04157) | 2024-01 | G | re-decide | manip/sim |
| [LaMI: Large Language Models for Multi-Modal Human-Robot Interaction](https://arxiv.org/abs/2401.15174) | 2024-01 | G | re-decide | social/real |
| [Grounding LLMs For Robot Task Planning Using Closed-loop State Feedback](https://arxiv.org/abs/2402.08546) | 2024-02 | G | re-decide | manip/sim+real |
| [AutoGPT+P: Affordance-based Task Planning with Large Language Models](https://arxiv.org/abs/2402.10778) | 2024-02 | G | re-decide | humanoid/real |
| [RoboEXP: Action-Conditioned Scene Graph via Interactive Exploration for Robotic Manipulation](https://arxiv.org/abs/2402.15487) | 2024-02 | G | re-decide | manip/real |
| [Conversational Language Models for Human-in-the-Loop Multi-Robot Coordination](https://arxiv.org/abs/2402.19166) | 2024-02 | G | re-decide | multi-robot/real |
| [Language-Grounded Dynamic Scene Graphs for Interactive Object Search With Mobile Manipulation](https://arxiv.org/abs/2403.08605) | 2024-03 | G | re-decide | mobile-manip/sim+real |
| [To Help or Not to Help: LLM-based Attentive Support for Human-Robot Group Interactions](https://arxiv.org/abs/2403.12533) | 2024-03 | G | re-decide | manip/real |
| [OceanPlan: Hierarchical Planning and Replanning for Natural Language AUV Piloting in Large-scale Unexplored Ocean Environments](https://arxiv.org/abs/2403.15369) | 2024-03 | G | re-decide | other/sim |
| [ITCMA: A Generative Agent Based on a Computational Consciousness Structure](https://arxiv.org/abs/2403.20097) | 2024-03 | G | re-decide | loco/real |
| [VoicePilot: Harnessing LLMs as Speech Interfaces for Physically Assistive Robots](https://arxiv.org/abs/2404.04066) | 2024-04 | G | re-decide | manip/real |
| [Long-horizon Locomotion and Manipulation on a Quadrupedal Robot with Large Language Models](https://arxiv.org/abs/2404.05291) | 2024-04 | G | re-decide | loco/sim+real |
| [Action Contextualization: Adaptive Task Planning and Action Tuning Using Large Language Models](https://arxiv.org/abs/2404.13191) | 2024-04 | G | re-decide | manip/real |
| [Closed Loop Interactive Embodied Reasoning for Robot Manipulation](https://arxiv.org/abs/2404.15194) | 2024-04 | G | re-decide | manip/sim+real |
| [Towards Efficient LLM Grounding for Embodied Multi-Agent Collaboration](https://arxiv.org/abs/2405.14314) | 2024-05 | G | re-decide | multi-robot/sim |
| [Nadine: An LLM-driven Intelligent Social Robot with Affective Capabilities and Human-like Memory](https://arxiv.org/abs/2405.20189) | 2024-05 | G | re-decide | social/real |
| [Leveraging Large Language Model for Heterogeneous Ad Hoc Teamwork Collaboration](https://arxiv.org/abs/2406.12224) | 2024-06 | G | re-decide | multi-robot/sim |
| [LIT: Large Language Model Driven Intention Tracking for Proactive Human-Robot Collaboration - A Robot Sous-Chef Application](https://arxiv.org/abs/2406.13787) | 2024-06 | G | re-decide | manip/real |
| [Towards Natural Language-Driven Assembly Using Foundation Models](https://arxiv.org/abs/2406.16093) | 2024-06 | G | re-decide | manip/sim |
| [QuadrupedGPT: Towards a Versatile Quadruped Agent in Open-ended Worlds](https://arxiv.org/abs/2406.16578) | 2024-06 | G | re-decide | loco/sim+real |
| [Open-vocabulary Mobile Manipulation in Unseen Dynamic Environments with 3D Semantic Maps](https://arxiv.org/abs/2406.18115) | 2024-06 | G | re-decide | mobile-manip/real |
| [ROS-LLM: A ROS framework for embodied AI with task feedback and structured reasoning](https://arxiv.org/abs/2406.19741) | 2024-06 | G | re-decide | manip/real |
| [When Robots Get Chatty: Grounding Multimodal Human-Robot Conversation and Collaboration](https://arxiv.org/abs/2407.00518) | 2024-06 | G | re-decide | social/real |
| [CAMON: Cooperative Agents for Multi-Object Navigation with LLM-based Conversations](https://arxiv.org/abs/2407.00632) | 2024-06 | G | re-decide | multi-robot/sim |
| Nadine: A large language model‐driven intelligent social robot with affective capabilities and human‐like memory | 2024-07 | G | re-decide | social/real |
| [FLAIR: Feeding via Long-horizon AcquIsition of Realistic dishes](https://arxiv.org/abs/2407.07561) | 2024-07 | G | re-decide | manip/real |
| From Perception to Action: Leveraging LLMs and Scene Graphs for Intuitive Robotic Task Execution | 2024-07 | G | re-decide | manip/sim |
| [SARO: Space-Aware Robot System for Terrain Crossing via Vision-Language Model](https://arxiv.org/abs/2407.16412) | 2024-07 | G | re-decide | loco/sim+real |
| Hierarchical Generation of Action Sequence for Service Rots Based on Scene Graph via Large Language Models | 2024-07 | G | re-decide | mobile-manip/sim+real |
| [From Decision to Action in Surgical Autonomy: Multi-Modal Large Language Models for Robot-Assisted Blood Suction](https://arxiv.org/abs/2408.07806) | 2024-08 | G | re-decide | manip/sim |
| [Autonomous Behavior Planning For Humanoid Loco-manipulation Through Grounded Language Model](https://arxiv.org/abs/2408.08282) | 2024-08 | G | re-decide | humanoid/sim+real |
| [EMPOWER: Embodied Multi-role Open-vocabulary Planning with Online Grounding and Execution](https://arxiv.org/abs/2408.17379) | 2024-08 | G | re-decide | mobile-manip/real |
| [Behavior Tree Generation using Large Language Models for Sequential Manipulation Planning with Human Instructions and Feedback](https://arxiv.org/abs/2409.09435) | 2024-09 | G | re-decide | manip/real |
| [PLATO: Planning with LLMs and Affordances for Tool Manipulation](https://arxiv.org/abs/2409.11580) | 2024-09 | G | re-decide | manip/sim |
| [InteLiPlan: An Interactive Lightweight LLM-Based Planner for Domestic Robot Autonomy](https://arxiv.org/abs/2409.14506) | 2024-09 | G | re-decide | mobile-manip/sim+real |
| [COHERENT: Collaboration of Heterogeneous Multi-Robot System with Large Language Models](https://arxiv.org/abs/2409.15146) | 2024-09 | G | re-decide | multi-robot/sim+real |
| [AIR-Embodied: An Efficient Active 3DGS-based Interaction and Reconstruction Framework with Embodied Large Language Model](https://arxiv.org/abs/2409.16019) | 2024-09 | G | re-decide | manip/sim+real |
| [MHRC: Closed-loop Decentralized Multi-Heterogeneous Robot Collaboration with Large Language Models](https://arxiv.org/abs/2409.16030) | 2024-09 | G | re-decide | multi-robot/sim |
| [Guiding Long-Horizon Task and Motion Planning with Vision Language Models](https://arxiv.org/abs/2410.02193) | 2024-10 | G | re-decide | mobile-manip/sim |
| [ConceptAgent: LLM-Driven Precondition Grounding and Tree Search for Robust Task Planning and Execution](https://arxiv.org/abs/2410.06108) | 2024-10 | G | re-decide | mobile-manip/sim+real |
| [Enabling Novel Mission Operations and Interactions with ROSA: The Robot Operating System Agent](https://arxiv.org/abs/2410.06472) | 2024-10 | G | re-decide | other/sim |
| [GRAPPA: Generalizing and Adapting Robot Policies via Online Agentic Guidance](https://arxiv.org/abs/2410.06473) | 2024-10 | G | re-decide | manip/sim+real |
| [EmbodiedRAG: Dynamic 3D Scene Graph Retrieval for Efficient and Scalable Robot Task Planning](https://arxiv.org/abs/2410.23968) | 2024-10 | G | re-decide | mobile-manip/sim+real |
| [Remote Life Support Robot Interface System for Global Task Planning and Local Action Expansion Using Foundation Models](https://arxiv.org/abs/2411.10038) | 2024-11 | G | re-decide | mobile-manip/real |
| [Dadu‐E: Rethinking the Role of Large Language Model in Robotic Computing Pipelines](https://arxiv.org/abs/2412.01663) | 2024-12 | G | re-decide | manip/sim+real |
| LAC: Using LLM-based Agents as the Controller to Realize Embodied Robot | 2024-12 | G | re-decide | other/sim |
| Dual-LLM Hierarchical Task Planning and Skill Grounding for Mobile Manipulation in Long-Horizon Restroom Cleaning | 2025 | G | re-decide | mobile-manip/real |
| LLM-Driven Pareto-Optimal Multi-Mode Reinforcement Learning for Adaptive UAV Navigation in Urban Wind Environments | 2025 | C | re-decide | aerial/sim |
| Mitigating Cross-Modal Distraction and Ensuring Geometric Feasibility via Affordance-Guided, Self-Consistent MLLMs for Food Preparation Task Planning | 2025 | G | re-decide | manip/sim |
| Using Vision Language Models as Closed-Loop Symbolic Planners for Robotic Applications: A Control-Theoretic Perspective | 2025 | G | re-decide | manip/sim |
| [LAMS: LLM-Driven Automatic Mode Switching for Assistive Teleoperation](https://arxiv.org/abs/2501.08558) | 2025-01 | G | re-decide | manip/sim |
| [RoboReflect: A Robotic Reflective Reasoning Framework for Grasping Ambiguous-Condition Objects](https://arxiv.org/abs/2501.09307) | 2025-01 | G | re-decide | manip/real |
| Integrating Multimodal Communication and Comprehension Evaluation during Human-Robot Collaboration for Increased Reliability of Foundation Model-based Task Planning Systems | 2025-01 | G | re-decide | manip/real |
| [Reflective Planning: Vision-Language Models for Multi-Stage Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2502.16707) | 2025-02 | G | re-decide | manip/real |
| Task Planning for a Factory Robot Using Large Language Model | 2025-03 | G | re-decide | mobile-manip/sim+real |
| [CLEA: Closed-Loop Embodied Agent for Enhancing Task Execution in Dynamic Environments](https://arxiv.org/abs/2503.00729) | 2025-03 | G | re-decide | multi-robot/real |
| [RoboDexVLM: Visual Language Model-Enabled Task Planning and Motion Control for Dexterous Robot Manipulation](https://arxiv.org/abs/2503.01616) | 2025-03 | G | re-decide | manip/real |
| [Perceiving, Reasoning, Adapting: A Dual-Layer Framework for VLM-Guided Precision Robotic Manipulation](https://arxiv.org/abs/2503.05064) | 2025-03 | G | re-decide | manip/real |
| A Multiagent-Driven Robotic AI Chemist Enabling Autonomous Chemical Research On Demand. | 2025-03 | G | re-decide | other/real |
| [Instruction-Augmented Long-Horizon Planning: Embedding Grounding Mechanisms in Embodied Mobile Manipulation](https://arxiv.org/abs/2503.08084) | 2025-03 | G | re-decide | humanoid/real |
| [LightPlanner: Unleashing the Reasoning Capabilities of Lightweight Large Language Models in Task Planning](https://arxiv.org/abs/2503.08508) | 2025-03 | G | re-decide | mobile-manip/sim+real |
| [Trinity: A Modular Humanoid Robot AI System](https://arxiv.org/abs/2503.08338) | 2025-03 | G | re-decide | humanoid/real |
| [Mitigating Cross-Modal Distraction and Ensuring Geometric Feasibility via Affordance-Guided and Self-Consistent MLLMs for Task Planning in Instruction-Following Manipulation](https://arxiv.org/abs/2503.13055) | 2025-03 | G | re-decide | manip/sim |
| GPTArm: An Autonomous Task Planning Manipulator Grasping System Based on Vision–Language Models | 2025-03 | G | re-decide | manip/real |
| [LLM-drone: aerial additive manufacturing with drones planned using large language models](https://arxiv.org/abs/2503.17566) | 2025-03 | G | re-decide | aerial/sim |
| [REMAC: Self-Reflective and Self-Evolving Multi-Agent Collaboration for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2503.22122) | 2025-03 | G | re-decide | multi-robot/sim+real |
| [Exploring GPT-4 for Robotic Agent Strategy with Real-Time State Feedback and a Reactive Behaviour Framework](https://arxiv.org/abs/2503.23601) | 2025-03 | G | re-decide | humanoid/sim+real |
| [AuDeRe: Automated Strategy Decision and Realization in Robot Planning and Control via LLMs](https://arxiv.org/abs/2504.03015) | 2025-04 | G | re-decide | other/sim |
| [Hierarchical Planning for Complex Tasks with Knowledge Graph-RAG and Symbolic Verification](https://arxiv.org/abs/2504.04578) | 2025-04 | G | re-decide | manip/sim+real |
| [EmbodiedAgent: A Scalable Hierarchical Approach to Overcome Practical Challenge in Multi-Robot Control](https://arxiv.org/abs/2504.10030) | 2025-04 | C | re-decide | multi-robot/real |
| [Robotic Task Ambiguity Resolution via Natural Language Interaction](https://arxiv.org/abs/2504.17748) | 2025-04 | C | re-decide | manip/sim+real |
| Research on Robot Action Planning Based on Chatcliport | 2025-04 | G | re-decide | manip/sim |
| [Leveraging Pre-trained Large Language Models with Refined Prompting for Online Task and Motion Planning](https://arxiv.org/abs/2504.21596) | 2025-04 | G | re-decide | manip/sim |
| [MORE: Mobile Manipulation Rearrangement Through Grounded Language Reasoning](https://arxiv.org/abs/2505.03035) | 2025-05 | G | re-decide | mobile-manip/sim+real |
| [Air-Ground Collaboration for Language-Specified Missions in Unknown Environments](https://arxiv.org/abs/2505.09108) | 2025-05 | G | re-decide | multi-robot/real |
| [Deploying Foundation Model-Enabled Air and Ground Robots in the Field: Challenges and Opportunities](https://arxiv.org/abs/2505.09477) | 2025-05 | G | re-decide | multi-robot/real |
| Autonomous Behavior Control for Quadruped Robots with Arms Based on MultiModal Large Language Model | 2025-05 | G | re-decide | mobile-manip/real |
| Emotion-Aware LLM Systems for Adaptive Human-Robot Interaction | 2025-05 | C | re-decide | manip/sim |
| [LA-RCS: LLM-Agent-Based Robot Control System](https://arxiv.org/abs/2505.18214) | 2025-05 | G | re-decide | other/real |
| [Robot Operation of Home Appliances by Reading User Manuals](https://arxiv.org/abs/2505.20424) | 2025-05 | G | re-decide | manip/sim+real |
| [Agentic Robot: A Brain-Inspired Framework for Vision-Language-Action Models in Embodied Agents](https://arxiv.org/abs/2505.23450) | 2025-05 | G | re-decide | manip/sim |
| [Visual Embodied Brain: Let Multimodal Large Language Models See, Think, and Control in Spaces](https://arxiv.org/abs/2506.00123) | 2025-05 | C |  | loco/real |
| TORNADO: Foundation Models for Robots that Handle Small, Soft and Deformable Objects | 2025-06 | G | re-decide | mobile-manip/real |
| [Understanding physical properties of unseen deformable objects by leveraging large-language models and robot actions](https://arxiv.org/abs/2506.03760) | 2025-06 | G | re-decide | manip/real |
| [Taking Flight with Dialogue: Enabling Natural Language Control for PX4-based Drone Agent](https://arxiv.org/abs/2506.07509) | 2025-06 | G | re-decide | aerial/sim+real |
| [ProVox: Personalization and Proactive Planning for Situated Human-Robot Collaboration](https://arxiv.org/abs/2506.12248) | 2025-06 | G | re-decide | manip/real |
| [Casper: Inferring Diverse Intents for Assistive Teleoperation with Vision Language Models](https://arxiv.org/abs/2506.14727) | 2025-06 | G | re-decide | manip/real |
| [Reflective VLM Planning for Dual-Arm Desktop Cleaning: Bridging Open-Vocabulary Perception and Precise Manipulation](https://arxiv.org/abs/2506.17328) | 2025-06 | G | re-decide | manip/sim |
| [Distilling On-device Language Models for Robot Planning with Minimal Human Intervention](https://arxiv.org/abs/2506.17486) | 2025-06 | C | re-decide | mobile-manip/sim+real |
| [STEP Planner: Constructing cross-hierarchical subgoal tree as an embodied long-horizon task planner](https://arxiv.org/abs/2506.21030) | 2025-06 | C | re-decide | mobile-manip/sim+real |
| Exploring Edge Inference Feasibility of Small Scale Deep Learning Models for Robotic Manipulation | 2025-06 | G | re-decide | manip/real |
| [Hierarchical Vision-Language Planning for Multi-Step Humanoid Manipulation](https://arxiv.org/abs/2506.22827) | 2025-06 | G | re-decide | humanoid/real |
| SURTR: Semantic Understanding and Reinforced Trajectory Robotics via Collaborative Multi-LLMs and Offline Reinforcement Learning | 2025-07 | G | re-decide | manip/sim+real |
| [VLA-Touch: Enhancing Vision-Language-Action Models with Dual-Level Tactile Feedback](https://arxiv.org/abs/2507.17294) | 2025-07 | G | re-decide | manip/real |
| [Adaptive Articulated Object Manipulation on the Fly with Foundation Model Reasoning and Part Grounding](https://arxiv.org/abs/2507.18276) | 2025-07 | G | re-decide | manip/sim+real |
| A Language Model-Based Framework for Task Planning and Execution in Real-World Service Robot | 2025-07 | G | re-decide | mobile-manip/real |
| [Distributed AI Agents for Cognitive Underwater Robot Autonomy](https://arxiv.org/abs/2507.23735) | 2025-07 | G | re-decide | other/sim+real |
| [Mixed-Initiative Dialog for Human-Robot Collaborative Manipulation](https://arxiv.org/abs/2508.05535) | 2025-08 | G | re-decide | manip/sim+real |
| [ExploreVLM: Closed-Loop Robot Exploration Task Planning with Vision-Language Models](https://arxiv.org/abs/2508.11918) | 2025-08 | G | re-decide | manip/real |
| [DEXTER-LLM: Dynamic and Explainable Coordination of Multi-Robot Systems in Unknown Environments via Large Language Models](https://arxiv.org/abs/2508.14387) | 2025-08 | G | re-decide | multi-robot/sim+real |
| [RoboChemist: Long-Horizon and Safety-Compliant Robotic Chemical Experimentation](https://arxiv.org/abs/2509.08820) | 2025-09 | G | re-decide | manip/real |
| [DREAM: Domain-aware Reasoning for Efficient Autonomous Underwater Monitoring](https://arxiv.org/abs/2509.13666) | 2025-09 | G | re-decide | other/sim |
| [PhysicalAgent: Towards General Cognitive Robotics with Foundation World Models](https://arxiv.org/abs/2509.13903) | 2025-09 | G | re-decide | manip/sim+real |
| [Video-to-BT: Generating Reactive Behavior Trees from Human Demonstration Videos for Robotic Assembly](https://arxiv.org/abs/2509.16611) | 2025-09 | G | re-decide | manip/real |
| [IDfRA: Self-Verification for Iterative Design in Robotic Assembly](https://arxiv.org/abs/2509.16998) | 2025-09 | G | re-decide | manip/real |
| [Language-in-the-Loop Culvert Inspection on the Erie Canal](https://arxiv.org/abs/2509.21370) | 2025-09 | G | re-decide | loco/real |
| [Agentic Scene Policies: Unifying Space, Semantics, and Affordances for Robot Action](https://arxiv.org/abs/2509.19571) | 2025-09 | G | re-decide | manip/sim+real |
| Zero-Shot Task Automation with Foundation Language Models | 2025-09 | G | re-decide | manip/sim |
| [PhysiAgent: An Embodied Agent Framework in Physical World](https://arxiv.org/abs/2509.24524) | 2025-09 | G | re-decide | manip/real |
| [A Hierarchical Agentic Framework for Autonomous Drone-Based Visual Inspection](https://arxiv.org/abs/2510.00259) | 2025-09 | G | re-decide | aerial/real |
| [RoboPilot: Generalizable Dynamic Robotic Manipulation with Dual-thinking Modes](https://arxiv.org/abs/2510.00154) | 2025-09 | G | re-decide | manip/sim+real |
| [TACOS: Task Agnostic COordinator of a multi-drone System](https://arxiv.org/abs/2510.01869) | 2025-10 | G | re-decide | multi-robot/sim+real |
| SkyNet: An Extensible Edge-Cloud Collaborative Framework for Robots in Long-Horizon Tasks | 2025-10 | G | re-decide | manip/real |
| [Constrained natural language action planning for resilient embodied systems](https://arxiv.org/abs/2510.06357) | 2025-10 | G | re-decide | loco/sim+real |
| [FLEET: Formal Language-Grounded Scheduling for Heterogeneous Robot Teams](https://arxiv.org/abs/2510.07417) | 2025-10 | G | re-decide | multi-robot/sim+real |
| [RobotFleet: An Open-Source Framework for Centralized Multi-Robot Task Planning](https://arxiv.org/abs/2510.10379) | 2025-10 | G | re-decide | multi-robot/sim |
| [VLA^2: Empowering Vision-Language-Action Models with an Agentic Framework for Unseen Concept Manipulation](https://arxiv.org/abs/2510.14902) | 2025-10 | G | re-decide | manip/sim |
| Autonomous Subtask Generation for Indoor Search and Rescue Mission via Large-Language-Model and Behavior-Tree Integration | 2025-10 | G | re-decide | mobile-manip/real |
| ROD-VLM: A Framework of Real-time Robotic Perception, Reasoning and Manipulation | 2025-10 | G | re-decide | manip/real |
| EmbodiedFly: Embodied LLM Agent with an Autonomous Reconfigurable Drone | 2025-10 | G | re-decide | aerial/real |
| [Hierarchical DLO Routing with Reinforcement Learning and In-Context Vision-Language Models](https://arxiv.org/abs/2510.19268) | 2025-10 | G | re-decide | manip/sim+real |
| [PFEA: An LLM-based High-Level Natural Language Planning and Feedback Embodied Agent for Human-Centered AI](https://arxiv.org/abs/2510.24109) | 2025-10 | G | re-decide | manip/real |
| [Heterogeneous Robot Collaboration in Unstructured Environments with Grounded Generative Intelligence](https://arxiv.org/abs/2510.26915) | 2025-10 | G | re-decide | multi-robot/sim+real |
| [Toward Accurate Long-Horizon Robotic Manipulation: Language-to-Action with Foundation Models via Scene Graphs](https://arxiv.org/abs/2510.27558) | 2025-10 | G | re-decide | manip/real |
| [Searching in Space and Time: Unified Memory-Action Loops for Open-World Object Retrieval](https://arxiv.org/abs/2511.14004) | 2025-11 | G | re-decide | mobile-manip/sim+real |
| [ArtiBench and ArtiBrain: Benchmarking Generalizable Vision-Language Articulated Object Manipulation](https://arxiv.org/abs/2511.20330) | 2025-11 | G | re-decide | manip/sim+real |
| Enhancing Collaborative Robotics through Large Language Model Integration: A Vision-Guided Approach Using ROS MCP Server | 2025-11 | G | re-decide | manip/real |
| A Resilient LLM-driven Agent Framework for Multi-UAV Mission Planning and Control | 2025-11 | G | re-decide | aerial/sim |
| [BINDER: Instantly Adaptive Mobile Manipulation with Open-Vocabulary Commands](https://arxiv.org/abs/2511.22364) | 2025-11 | G | re-decide | mobile-manip/sim+real |
| Embodied Multi-Agent Planning With LLMs: A Best-of-N Strategy for Efficient Cooperation | 2025-11 | G | re-decide | multi-robot/sim |
| [Transforming Monolithic Foundation Models into Embodied Multi-Agent Architectures for Human-Robot Collaboration](https://arxiv.org/abs/2512.00797) | 2025-11 | G | re-decide | mobile-manip/real |
| A Large Language Model-Driven Multi-Agent Human-Machine Interaction Framework | 2025-12 | G | re-decide | multi-robot/real |
| [Chat with UAV – human-UAV interaction based on large language models](https://arxiv.org/abs/2512.08145) | 2025-12 | G | re-decide | aerial/sim |
| [Embodied Tree of Thoughts: Deliberate Manipulation Planning With Embodied World Model](https://arxiv.org/abs/2512.08188) `real2sim2real` | 2025-12 | G | re-decide | manip/sim+real |
| [LEO-RobotAgent: A General-purpose Robotic Agent for Language-driven Embodied Operator](https://arxiv.org/abs/2512.10605) | 2025-12 | G | re-decide | other/sim+real |
| [Vision-Language-Policy Model for Dynamic Robot Task Planning](https://arxiv.org/abs/2512.19178) | 2025-12 | C | re-decide | manip/real |
| [LookPlanGraph: Embodied Instruction Following Method with VLM Graph Augmentation](https://arxiv.org/abs/2512.21243) | 2025-12 | G | re-decide | mobile-manip/sim |
| [D-RMGPT: Robot-assisted collaborative tasks driven by large multimodal models](https://arxiv.org/abs/2408.11761) | 2026-04 | G | re-decide | manip/real |

</details>

<details><summary><b>Controller · Direct drivers</b> (83)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| Leveraging Commonsense Knowledge from Large Language Models for Task and Motion Planning | 2023 | G | none | mobile-manip/sim+real |
| Make a Donut: Language-Guided Hierarchical EMD-Space Planning for Zero-shot Deformable Object Manipulation | 2023 | G | authored | manip/sim |
| [Task and Motion Planning with Large Language Models for Object Rearrangement](https://arxiv.org/abs/2303.06247) | 2023-03 | G | none | mobile-manip/sim+real |
| [Energy-based Models are Zero-Shot Planners for Compositional Scene Rearrangement](https://arxiv.org/abs/2304.14391) | 2023-04 | G | none | manip/sim+real |
| ProgPrompt: program generation for situated robot task planning using large language models | 2023-08 | G | authored | manip/sim+real |
| [Generalizable Long-Horizon Manipulations with Large Language Models](https://arxiv.org/abs/2310.02264) | 2023-10 | G | authored | manip/sim+real |
| [LAN-grasp: Using Large Language Models for Semantic Object Grasping](https://arxiv.org/abs/2310.05239) | 2023-10 | G | none | manip/real |
| [Make a Donut: Hierarchical EMD-Space Planning for Zero-Shot Deformable Manipulation With Tools](https://arxiv.org/abs/2311.02787) | 2023-11 | G | authored | manip/sim |
| [SAGE: Bridging Semantic and Actionable Parts for GEneralizable Manipulation of Articulated Objects](https://arxiv.org/abs/2312.01307) | 2023-12 | G | re-decide | manip/sim+real |
| [DiffVL: Scaling Up Soft Body Manipulation using Vision-Language Driven Differentiable Physics](https://arxiv.org/abs/2312.06408) | 2023-12 | G | none | manip/sim |
| [From text to motion: grounding GPT-4 in a humanoid robot “Alter3”](https://arxiv.org/abs/2312.06571) | 2023-12 | G | re-decide | humanoid/real |
| LLM-based Skill Diffusion for Zero-shot Policy Adaptation | 2024 | G | authored | manip/sim |
| Open-World Task and Motion Planning via Vision-Language Model Inferred Constraints | 2024 | G | none | manip/sim+real |
| [Generative Expressive Robot Behaviors using Large Language Models](https://arxiv.org/abs/2401.14673) | 2024-01 | G | re-decide | social/sim+real |
| [InCoRo: In-Context Learning for Robotics Control with Feedback Loops](https://arxiv.org/abs/2402.05188) | 2024-02 | G | re-decide | manip/sim |
| [Learning to Learn Faster from Human Feedback with Language Model Predictive Control](https://arxiv.org/abs/2402.11450) | 2024-02 | C | re-decide | mobile-manip/sim+real |
| [RoboCodeX: Multimodal Code Generation for Robotic Behavior Synthesis](https://arxiv.org/abs/2402.16117) | 2024-02 | C | none | manip/sim+real |
| Language, Camera, Autonomy! Prompt-engineered Robot Control for Rapidly Evolving Deployment | 2024-03 | G | re-decide | other/sim+real |
| [NARRATE: Versatile Language Architecture for Optimal Control in Robotics](https://arxiv.org/abs/2403.10762) | 2024-03 | G | authored | manip/sim |
| [Context-aware LLM-based Safe Control Against Latent Risks](https://arxiv.org/abs/2403.11863) | 2024-03 | G | re-decide | other/sim |
| [ShapeGrasp: Zero-Shot Task-Oriented Grasping with Large Language Models through Geometric Decomposition](https://arxiv.org/abs/2403.18062) | 2024-03 | G | none | manip/real |
| [GenCHiP: Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks](https://arxiv.org/abs/2404.06645) | 2024-04 | G | none | manip/sim+real |
| [SuFIA: Language-Guided Augmented Dexterity for Robotic Surgical Assistants](https://arxiv.org/abs/2405.05226) | 2024-05 | G | re-decide | manip/sim+real |
| [FlockGPT: Guiding UAV Flocking with Linguistic Orchestration](https://arxiv.org/abs/2405.05872) | 2024-05 | G | re-decide | multi-robot/sim |
| [Toward Automated Programming for Robotic Assembly Using ChatGPT](https://arxiv.org/abs/2405.08216) `sim2real` | 2024-05 | G | re-decide | manip/sim+real |
| [Meta-Control: Automatic Model-based Control Synthesis for Heterogeneous Robot Skills](https://arxiv.org/abs/2405.11380) | 2024-05 | G | authored | manip/sim+real |
| [Trust the PRoC3S: Solving Long-Horizon Robotics Problems with LLMs and Constraint Satisfaction](https://arxiv.org/abs/2406.05572) | 2024-06 | G | re-decide | manip/sim+real |
| [LLM-Craft: Robotic Crafting of Elasto-Plastic Objects With Large Language Models](https://arxiv.org/abs/2406.08648) | 2024-06 | G | re-decide | manip/sim |
| [GPT-Fabric: Folding and Smoothing Fabric by Leveraging Pre-Trained Foundation Models](https://arxiv.org/abs/2406.09640) | 2024-06 | G | re-decide | manip/sim+real |
| [ThinkGrasp: A Vision-Language System for Strategic Part Grasping in Clutter](https://arxiv.org/abs/2407.11298) | 2024-07 | G | re-decide | manip/sim+real |
| [Words2Contact: Identifying Support Contacts from Verbal Instructions Using Foundation Models](https://arxiv.org/abs/2407.14229) | 2024-07 | G | re-decide | humanoid/real |
| [ReplanVLM: Replanning Robotic Tasks With Visual Language Models](https://arxiv.org/abs/2407.21762) | 2024-07 | G | re-decide | manip/sim+real |
| [Text2Interaction: Establishing Safe and Preferable Human-Robot Interaction](https://arxiv.org/abs/2408.06105) | 2024-08 | G | none | manip/real |
| [Hierarchical LLMs in-the-Loop Optimization for Real-Time Multi-Robot Target Tracking Under Unknown Hazards](https://arxiv.org/abs/2409.12274) | 2024-09 | G | re-decide | multi-robot/sim |
| [Scene Exploration by Vision-Language Models](https://arxiv.org/abs/2409.17641) | 2024-09 | G | re-decide | manip/real |
| [UniAff: A Unified Representation of Affordances for Tool Usage and Articulation with Vision-Language Models](https://arxiv.org/abs/2409.20551) | 2024-09 | C | none | manip/sim+real |
| [Exploring Spatial Representation to Enhance LLM Reasoning in Aerial Vision-Language Navigation](https://arxiv.org/abs/2410.08500) | 2024-10 | G | re-decide | aerial/sim+real |
| [LLM2Swarm: Robot Swarms that Responsively Reason, Plan, and Collaborate through LLMs](https://arxiv.org/abs/2410.11387) | 2024-10 | G | re-decide | multi-robot/sim |
| [Sampling-Based Model Predictive Control for Dexterous Manipulation on a Biomimetic Tendon-Driven Hand](https://arxiv.org/abs/2411.06183) | 2024-11 | G | re-decide | manip/sim+real |
| [Open-World Task and Motion Planning via Vision-Language Model Generated Constraints](https://arxiv.org/abs/2411.08253) | 2024-11 | G | none | manip/sim+real |
| [MALMM: Multi-Agent Large Language Models for Zero-Shot Robotic Manipulation](https://arxiv.org/abs/2411.17636) | 2024-11 | G | re-decide | manip/sim+real |
| Grounded Vision-Language Interpreter for Integrated Task and Motion Planning | 2025 | G | re-decide | manip/sim |
| InstructFlow: Adaptive Symbolic Constraint-Guided Code Generation for Long-Horizon Planning | 2025 | G | re-decide | manip/sim |
| LLM-controller: Dynamic robot control adaptation using large language models | 2025-01 | G | re-decide | manip/sim |
| LLM Closed-Loop Application Framework for Industry Manipulator System | 2025-01 | G | re-decide | manip/real |
| [Code-as-Symbolic-Planner: Foundation Model-Based Robot Planning via Symbolic Code Generation](https://arxiv.org/abs/2503.01700) | 2025-03 | G | re-decide | manip/sim+real |
| [Bridging VLM and KMP: Enabling Fine-Grained Robotic Manipulation via Semantic Keypoints Representation](https://arxiv.org/abs/2503.02748) | 2025-03 | G | none | manip/real |
| [AutoMisty: A Multi-Agent LLM Framework for Automated Code Generation in the Misty Social Robot](https://arxiv.org/abs/2503.06791) | 2025-03 | G | re-decide | social/real |
| [Multi-Agent LLM Actor-Critic Framework for Social Robot Navigation](https://arxiv.org/abs/2503.09758) | 2025-03 | G | re-decide | multi-robot/sim |
| [IMPACT: Intelligent Motion Planning with Acceptable Contact Trajectories via Vision-Language Models](https://arxiv.org/abs/2503.10110) | 2025-03 | G | none | manip/sim+real |
| [KUDA: Keypoints to Unify Dynamics Learning and Visual Prompting for Open-Vocabulary Robotic Manipulation](https://arxiv.org/abs/2503.10546) | 2025-03 | G | authored | manip/real |
| Embodied large language models enable robots to complete complex tasks in unpredictable environments | 2025-03 | G | authored | manip/real |
| [Robotic Long-Horizon Manipulation with Progressive In-Context Code Generation and Episodic Feedback](https://arxiv.org/abs/2503.21969) | 2025-03 | G | re-decide | manip/sim+real |
| [GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models](https://arxiv.org/abs/2503.23875) | 2025-03 | G | authored | multi-robot/sim+real |
| [Robotic Visual Instruction](https://arxiv.org/abs/2505.00693) | 2025-05 | G | none | manip/sim+real |
| [Meta-Optimization and Program Search using Language Models for Task and Motion Planning](https://arxiv.org/abs/2505.03725) | 2025-05 | G | none | manip/sim+real |
| [Unfettered Forceful Skill Acquisition with Physical Reasoning and Coordinate Frame Labeling](https://arxiv.org/abs/2505.09731) | 2025-05 | G | re-decide | manip/real |
| Here's your PDDL Problem File! On Using VLMs for Generating Symbolic PDDL Problem Files | 2025-05 | G | re-decide | manip/sim+real |
| [Grounded Vision-Language Interpreter for Long-Horizon Bimanual Task and Motion Planning](https://arxiv.org/abs/2506.03270) | 2025-06 | G | re-decide | manip/sim+real |
| [FrankenBot: Brain-Morphic Modular Orchestration for Robotic Manipulation with Vision-Language Models](https://arxiv.org/abs/2506.21627) | 2025-06 | G | re-decide | manip/sim+real |
| [Large Language Model-Driven Closed-Loop UAV Operation With Semantic Observations](https://arxiv.org/abs/2507.01930) | 2025-07 | G | re-decide | aerial/sim |
| [Compositional Coordination for Multi-Robot Teams with Large Language Models](https://arxiv.org/abs/2507.16068) | 2025-07 | G | authored | multi-robot/sim+real |
| [FMimic: Foundation Models are Fine-grained Action Learners from Human Videos](https://arxiv.org/abs/2507.20622) | 2025-07 | G | none | manip/sim+real |
| Behavior tree generation and adaptation for a social robot control with LLMs | 2025-08 | G | re-decide | social/real |
| [HyCodePolicy: Hybrid Language Controllers for Multimodal Monitoring and Decision in Embodied Agents](https://arxiv.org/abs/2508.02629) | 2025-08 | G | re-decide | manip/sim |
| [Triple-S: A Collaborative Multi-LLM Framework for Solving Long-Horizon Implicative Tasks in Robotics](https://arxiv.org/abs/2508.07421) | 2025-08 | G | re-decide | manip/sim+real |
| [Rational Inverse Reasoning](https://arxiv.org/abs/2508.08983) | 2025-08 | G | re-decide | manip/sim |
| TypeFly: Low-Latency Drone Planning With Large Language Models | 2025-09 | G | authored | aerial/real |
| [GELATO: Multi-Instruction Trajectory Reshaping via Geometry-Aware Multiagent-based Orchestration](https://arxiv.org/abs/2509.06031) | 2025-09 | G | none | manip/sim+real |
| [LLM-GROP: Visually Grounded Robot Task and Motion Planning with Large Language Models](https://arxiv.org/abs/2511.07727) | 2025-10 | G | none | mobile-manip/sim+real |
| [Executable Analytic Concepts as the Missing Link Between VLM Insight and Precise Manipulation](https://arxiv.org/abs/2510.07975) | 2025-10 | G | none | manip/sim+real |
| [ManiAgent: An Agentic Framework for General Robotic Manipulation](https://arxiv.org/abs/2510.11660) | 2025-10 | G | re-decide | manip/sim+real |
| Keypoint-Aware RAG for Robotic Manipulation: In-Context Constraint Learning via Large-Scale Retrieval | 2025-10 | G | authored | manip/sim+real |
| LLM-CBT: LLM-Driven Closed-Loop Behavior Tree Planning for Heterogeneous UAV-UGV Swarm Collaboration | 2025-10 | G | re-decide | multi-robot/sim |
| PACR: Point-Axis Constraint Reasoning for Enhanced Robotic Manipulation with Dexterity and Compliance | 2025-10 | G | re-decide | manip/real |
| [Towards Reliable Code-as-Policies: A Neuro-Symbolic Framework for Embodied Task Planning](https://arxiv.org/abs/2510.21302) | 2025-10 | G | re-decide | manip/sim+real |
| [Maestro: Orchestrating Robotics Modules with Vision-Language Models for Zero-Shot Generalist Robots](https://arxiv.org/abs/2511.00917) | 2025-11 | G | re-decide | manip/real |
| [Semantic Glitch: Agency and Artistry in an Autonomous Pixel Cloud](https://arxiv.org/abs/2511.16048) | 2025-11 | G | re-decide | aerial/real |
| [LLM-Based Generalizable Hierarchical Task Planning and Execution for Heterogeneous Robot Teams with Event-Driven Replanning](https://arxiv.org/abs/2511.22354) | 2025-11 | G | re-decide | multi-robot/real |
| Generating joint sequences with pre-trained LLMs to drive dual-arm nursing robot to perform actions | 2025-12 | G | re-decide | manip/sim |
| Language-Guided Predictive Control: Synthesizing Semantic Safety Constraints for Adaptive Navigation | 2025-12 | G | none | multi-robot/sim |
| [SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models](https://arxiv.org/abs/2512.05955) `real2sim2real` | 2025-12 | G | re-decide | manip/sim+real |
| A Multi-Modal Robot Task Planning Framework Based on Environmental Feedback | 2025-12 | G | re-decide | manip/sim |

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

<details><summary><b>VLN and embodied navigation</b> (33)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Grounding Complex Natural Language Commands for Temporal Tasks in Unseen Environments](https://arxiv.org/abs/2302.11649) | 2023-02 | G | none | nav/real |
| [LLM as A Robotic Brain: Unifying Egocentric Memory and Control](https://arxiv.org/abs/2304.09349) | 2023-04 | G | re-decide | nav/sim |
| [Think, Act, and Ask: Open-World Interactive Personalized Robot Navigation](https://arxiv.org/abs/2310.07968) | 2023-10 | G | re-decide | nav/sim |
| [Verifiably Following Complex Robot Instructions with Foundation Models](https://arxiv.org/abs/2402.11498) | 2024-02 | G | authored | nav/real |
| [Cognitive Planning for Object Goal Navigation using Generative AI Models](https://arxiv.org/abs/2404.00318) | 2024-03 | G | re-decide | nav/sim |
| [Open Scene Graphs for Open World Object-Goal Navigation](https://arxiv.org/abs/2508.04678) | 2024-07 | G | re-decide | nav/sim+real |
| [TrustNavGPT: Modeling Uncertainty to Improve Trustworthiness of Audio-Guided LLM-Based Robot Navigation](https://arxiv.org/abs/2408.01867) | 2024-08 | G | re-decide | nav/sim+real |
| [E2Map: Experience-and-Emotion Map for Self-Reflective Robot Navigation with Language Models](https://arxiv.org/abs/2409.10027) | 2024-09 | G | re-decide | nav/sim+real |
| [Hey Robot! Personalizing Robot Navigation Through Model Predictive Control with a Large Language Model](https://arxiv.org/abs/2409.13393) | 2024-09 | G | authored | nav/sim+real |
| [Behav: Behavioral Rule Guided Autonomy Using VLMs for Robot Navigation in Outdoor Scenes](https://arxiv.org/abs/2409.16484) | 2024-09 | G | authored | nav/real |
| [AssistantX: An LLM-Powered Proactive Assistant in Collaborative Human-Populated Environments](https://arxiv.org/abs/2409.17655) | 2024-09 | G | re-decide | nav/real |
| [SPINE: Online Semantic Planning for Missions with Incomplete Natural Language Specifications in Unstructured Environments](https://arxiv.org/abs/2410.03035) | 2024-10 | G | re-decide | nav/sim+real |
| [Open-Architecture End-to-End System for Real-World Autonomous Robot Navigation](https://arxiv.org/abs/2410.06239) | 2024-10 | G | re-decide | nav/real |
| [TANGO: Training-free Embodied AI Agents for Open-world Tasks](https://arxiv.org/abs/2412.10402) | 2024-12 | G | authored | nav/sim |
| [GraphEQA: Using 3D Semantic Scene Graphs for Real-time Embodied Question Answering](https://arxiv.org/abs/2412.14480) | 2024-12 | G | re-decide | nav/sim+real |
| [Robust Mobile Robot Path Planning via LLM-Based Dynamic Waypoint Generation](https://arxiv.org/abs/2501.15901) | 2025-01 | G | re-decide | nav/sim |
| Enhancing Large Language Models with RAG for Visual Language Navigation in Continuous Environments | 2025-02 | G | re-decide | nav/sim |
| [LTLCodeGen: Code Generation of Syntactically Correct Temporal Logic for Robot Task Planning](https://arxiv.org/abs/2503.07902) | 2025-03 | G | none | nav/sim+real |
| Integration of Large Language Models for Autonomous Navigation of a Mobile Robot | 2025-04 | G | re-decide | nav/sim |
| [Research on Navigation Methods Based on LLMs](https://arxiv.org/abs/2504.15600) | 2025-04 | G | re-decide | nav/sim |
| [Semantic Intelligence: Integrating GPT-4 with A Planning in Low-Cost Robotics](https://arxiv.org/abs/2505.01931) | 2025-05 | G | none | nav/real |
| LLM-Guided Multi-Agent System for Natural Language-Based Robot Navigation | 2025-05 | G | re-decide | nav/sim |
| ["Don't Do That!": Guiding Embodied Systems through Large Language Model-based Constraint Generation](https://arxiv.org/abs/2506.04500) | 2025-06 | G | none | nav/sim |
| Leveraging Large Language Models for Modular Robot Navigation | 2025-06 | G | re-decide | nav/sim |
| [General-Purpose Robotic Navigation via LVLM-Orchestrated Perception, Reasoning, and Acting](https://arxiv.org/abs/2506.17462) | 2025-06 | G | re-decide | nav/sim |
| Smarter Robots, Fewer Queries: A Knowledge-Driven Approach to Reduce LLM Dependency | 2025-07 | G | re-decide | nav/sim |
| [OpenNav: Open-World Navigation with Multimodal Large Language Models](https://arxiv.org/abs/2507.18033) | 2025-07 | G | authored | nav/sim+real |
| DebateNav: Structured Multi-VLM Expert Debate for Robust Zero-Shot Object Navigation | 2025-08 | G | re-decide | nav/sim |
| [Plantbot: Integrating Plant and Robot through LLM Modular Agent Networks](https://arxiv.org/abs/2509.05338) | 2025-09 | G | re-decide | nav/real |
| [Human-like Navigation in a World Built for Humans](https://arxiv.org/abs/2509.21189) | 2025-09 | G | re-decide | nav/sim+real |
| Embodied Assistant: Robot Mobility Operations Guided by Open Vocabulary in Open Environments Utilizing LLM | 2025-10 | G | re-decide | nav/sim |
| [Multi-Step Reasoning for Embodied Question Answering via Tool Augmentation](https://arxiv.org/abs/2510.20310) | 2025-10 | C | re-decide | nav/sim |
| [TP-MDDN: Task-Preferenced Multi-Demand-Driven Navigation with Autonomous Decision-Making](https://arxiv.org/abs/2511.17225) | 2025-11 | G | re-decide | nav/sim |

</details>

<details><summary><b>Supervisor</b> (20)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| HiCRISP: A Hierarchical Closed-Loop Robotic Intelligent Self-Correction Planner | 2023 | G | re-decide | manip/sim+real |
| [VADER: Visual Affordance Detection and Error Recovery for Multi Robot Human Collaboration](https://arxiv.org/abs/2405.16021) | 2024-05 | G | re-decide | multi-robot/real |
| [Evaluating Uncertainty-based Failure Detection for Closed-Loop LLM Planners](https://arxiv.org/abs/2406.00430) | 2024-06 | G | re-decide | manip/sim |
| [DKPROMPT: Domain Knowledge Prompting Vision-Language Models for Open-World Planning](https://arxiv.org/abs/2406.17659) | 2024-06 | G | re-decide | mobile-manip/sim |
| [Robot Failure Recovery Using Vision-Language Models With Optimized Prompts](https://arxiv.org/abs/2409.03966) | 2024-09 | G | re-decide | manip/sim+real |
| [Automatic Behavior Tree Expansion with LLMs for Robotic Manipulation](https://arxiv.org/abs/2409.13356) | 2024-09 | G | re-decide | manip/sim |
| [Updating Robot Safety Representations Online From Natural Language Feedback](https://arxiv.org/abs/2409.14580) | 2024-09 | G | re-decide | nav/sim+real |
| Ensuring Safety in LLM-Driven Robotics: A Cross-Layer Sequence Supervision Mechanism | 2024-10 | G | re-decide | manip/sim+real |
| [Semantically Safe Robot Manipulation: From Semantic Scene Understanding to Motion Safeguards](https://arxiv.org/abs/2410.15185) | 2024-10 | G | authored | manip/real |
| [Collaborative Instance Object Navigation: Leveraging Uncertainty-Awareness to Minimize Human-Agent Dialogues](https://arxiv.org/abs/2412.01250) | 2024-12 | G | re-decide | nav/sim |
| Are We Close to Realizing Self-Programming Robots That Overcome the Unexpected? | 2025-01 | G | re-decide | nav/real |
| [Safety Aware Task Planning via Large Language Models in Robotics](https://arxiv.org/abs/2503.15707) | 2025-03 | G | re-decide | mobile-manip/sim |
| [LangPert: Detecting and Handling Task-level Perturbations for Robust Object Rearrangement](https://arxiv.org/abs/2504.09893) | 2025-04 | G | re-decide | manip/sim |
| [Real-Time Out-of-Distribution Failure Prevention via Multi-Modal Reasoning](https://arxiv.org/abs/2505.10547) | 2025-05 | G | authored | aerial/sim+real |
| [Enhancing reliability in LLM-integrated robotic systems: A unified approach to security and safety](https://arxiv.org/abs/2509.02163) | 2025-09 | G | re-decide | nav/sim+real |
| [A Collaborative Reasoning Framework for Anomaly Diagnostics in Underwater Robotics](https://arxiv.org/abs/2511.03075) | 2025-11 | G | re-decide | other/sim |
| [From Words to Safety: Language-Conditioned Safety Filtering for Robot Navigation](https://arxiv.org/abs/2511.05889) | 2025-11 | G | authored | nav/sim+real |
| Localization, inspection, and reasoning (LIRA) module for autonomous workflows in self-driving laboratories | 2025-11 | G | re-decide | manip/real |
| [Guardian: Detecting Robotic Planning and Execution Errors with Vision-Language Models](https://arxiv.org/abs/2512.01946) | 2025-12 | C | re-decide | manip/sim+real |
| [RoboSafe: Safeguarding Embodied Agents via Executable Safety Logic](https://arxiv.org/abs/2512.21220) | 2025-12 | G | re-decide | manip/sim+real |

</details>

<details><summary><b>Teacher</b> (5)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [MARLIN: Multi-Agent Reinforcement Learning Guided by Language-Based Inter-Robot Negotiation](https://arxiv.org/abs/2410.14383) | 2024-10 | G | re-decide | multi-robot/sim+real |
| [LLM-based Interactive Imitation Learning for Robotic Manipulation](https://arxiv.org/abs/2504.21769) | 2025-04 | G | authored | manip/sim |
| [Imagine, Verify, Execute: Memory-Guided Agentic Exploration with Vision-Language Models](https://arxiv.org/abs/2505.07815) | 2025-05 | G | re-decide | manip/sim+real |
| [BLAZER: Bootstrapping LLM-based Manipulation Agents with Zero-Shot Data Generation](https://arxiv.org/abs/2510.08572) | 2025-10 | G | re-decide | manip/sim |
| [AnyTask: an Automated Task and Data Generation Framework for Advancing Sim-to-Real Policy Learning](https://arxiv.org/abs/2512.17853) | 2025-12 | G | re-decide | manip/sim+real |

</details>

<details><summary><b>Designer</b> (47)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| Self-Refined Large Language Model as Automated Reward Function Designer for Deep Reinforcement Learning in Robotics | 2023 | G | re-decide | manip/sim |
| [Self-Refined Large Language Model as Automated Reward Function Designer for Deep Reinforcement Learning in Robotics](https://arxiv.org/abs/2309.06687) | 2023-09 | G | re-decide | manip/sim |
| [Words into Action: Learning Diverse Humanoid Robot Behaviors using Language Guided Iterative Motion Refinement](https://arxiv.org/abs/2310.06226) | 2023-10 | G | re-decide | humanoid/sim |
| [ARO: Large Language Model Supervised Robotics Text2Skill Autonomous Learning](https://arxiv.org/abs/2403.15834) | 2024-03 | G | re-decide | other/sim |
| [REvolve: Reward Evolution with Large Language Models using Human Feedback](https://arxiv.org/abs/2406.01309) | 2024-06 | G | re-decide | humanoid/sim |
| [Training Fast Robot Policies with Slow Foundation Models](https://arxiv.org/abs/2406.05881) | 2024-06 | G | re-decide | manip/sim |
| [LLM-Empowered State Representation for Reinforcement Learning](https://arxiv.org/abs/2407.13237) | 2024-07 | G | re-decide | loco/sim |
| [Diffusion Augmented Agents: A Framework for Efficient Exploration and Transfer Learning](https://arxiv.org/abs/2407.20798) | 2024-07 | G | re-decide | manip/sim |
| [RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins (early version)](https://arxiv.org/abs/2409.02920) `real2sim2real` | 2024-09 | G | none | manip/sim+real |
| [Game On: Towards Language Models as RL Experimenters](https://arxiv.org/abs/2409.03402) | 2024-09 | G | re-decide | manip/sim |
| [Adaptive Language-Guided Abstraction from Contrastive Explanations](https://arxiv.org/abs/2409.08212) | 2024-09 | G | re-decide | manip/sim |
| [AnyBipe: An End-to-End Framework for Training and Deploying Bipedal Robots Guided by Large Language Models](https://arxiv.org/abs/2409.08904) | 2024-09 | G | re-decide | loco/sim+real |
| [Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model](https://arxiv.org/abs/2410.13882) | 2024-10 | G |  | manip/sim+real |
| [Language-Model-Assisted Bi-Level Programming for Reward Learning from Internet Videos](https://arxiv.org/abs/2410.09286) | 2024-10 | G | re-decide | loco/sim |
| [SDS - See it, Do it, Sorted: Quadruped Skill Synthesis from Single Video Demonstration](https://arxiv.org/abs/2410.11571) `sim2real` | 2024-10 | G | re-decide | loco/sim+real |
| [A Large Language Model-Driven Reward Design Framework via Dynamic Feedback for Reinforcement Learning](https://arxiv.org/abs/2410.14660) | 2024-10 | G | re-decide | manip/sim |
| High-Precision Control of Humanoid Muscle-skeleton Robotic Arm Using Reinforcement Learning and Large Language Models | 2024-11 | G | re-decide | manip/sim |
| [ELEMENTAL: Interactive Learning from Demonstrations and Vision-Language Models for Reward Design in Robotics](https://arxiv.org/abs/2411.18825) | 2024-11 | G | re-decide | manip/sim |
| [Embodied Red Teaming for Auditing Robotic Foundation Models](https://arxiv.org/abs/2411.18676) | 2024-11 | G |  | manip/sim |
| [Video2Reward: Generating Reward Function from Videos for Legged Robot Behavior Learning](https://arxiv.org/abs/2412.05515) | 2024-12 | G | re-decide | loco/sim |
| [Efficient Language-instructed Skill Acquisition via Reward-Policy Co-Evolution](https://arxiv.org/abs/2412.13492) | 2024-12 | G | re-decide | manip/sim |
| TARG: Tree of Action-reward Generation With Large Language Model for Cabinet Opening Using Manipulator | 2025-02 | G | re-decide | manip/sim |
| [A Real-to-Sim-to-Real Approach to Robotic Manipulation with VLM-Generated Iterative Keypoint Rewards](https://arxiv.org/abs/2502.08643) `real2sim2real` | 2025-02 | G | re-decide | manip/sim+real |
| [Learning a High-Quality Robotic Wiping Policy Using Systematic Reward Analysis and Visual-Language Model Based Curriculum](https://arxiv.org/abs/2502.12599) | 2025-02 | G | re-decide | manip/sim |
| [Never too Prim to Swim: An LLM-Enhanced RL-based Adaptive S-Surface Controller for AUVs under Extreme Sea Conditions](https://arxiv.org/abs/2503.00527) | 2025-03 | G | re-decide | other/sim |
| [GROVE: A Generalized Reward for Learning Open-Vocabulary Physical Skill](https://arxiv.org/abs/2504.04191) | 2025-04 | G | re-decide | humanoid/sim |
| [RoboTwin: Dual-Arm Robot Benchmark with Generative Digital Twins](https://arxiv.org/abs/2504.13059) `real2sim2real` | 2025-04 | G | none | manip/sim+real |
| [Automated Hybrid Reward Scheduling Via Large Language Models for Robotic Skill Learning](https://arxiv.org/abs/2505.02483) | 2025-05 | G | re-decide | loco/sim |
| [MA-ROESL: Motion-aware Rapid Reward Optimization for Efficient Robot Skill Learning from Single Videos](https://arxiv.org/abs/2505.08367) `sim2real` | 2025-05 | G | re-decide | loco/sim+real |
| [VIRAL: Vision-grounded Integration for Reward design And Learning](https://arxiv.org/abs/2505.22092) | 2025-05 | G | re-decide | other/sim |
| [AURA: Autonomous Upskilling with Retrieval-Augmented Agents](https://arxiv.org/abs/2506.02507) `sim2real` | 2025-06 | G | re-decide | humanoid/sim+real |
| RoPESim: A Framework for Robot Manipulation Policy Evaluation via Simulation `real2sim` | 2025-08 | G | none | manip/sim |
| [Text2Touch: Tactile In-Hand Manipulation with LLM-Designed Reward Functions](https://arxiv.org/abs/2509.07445) `sim2real` | 2025-09 | G | re-decide | manip/sim+real |
| [CRAFT: Coaching Reinforcement Learning Autonomously using Foundation Models for Multi-Robot Coordination Tasks](https://arxiv.org/abs/2509.14380) `sim2real` | 2025-09 | G | re-decide | multi-robot/sim+real |
| [Reward Evolution with Graph-of-Thoughts: A Bi-Level Language Model Framework for Reinforcement Learning](https://arxiv.org/abs/2509.16136) | 2025-09 | G | re-decide | manip/sim |
| Where To Learn: Embodied Perception Learning Planned by Vision-Language Models | 2025-10 | G | re-decide | nav/sim |
| [High-Fidelity Simulated Data Generation for Real-World Zero-Shot Robotic Manipulation Learning With Gaussian Splatting](https://arxiv.org/abs/2510.10637) `real2sim2real` | 2025-10 | G | none | manip/sim+real |
| Simulation Verification Method for Robot Composite Task Planning in Open Environments `real2sim2real` | 2025-10 | G | re-decide | manip/sim+real |
| AnyBipe: An Automated End-to-End Framework for Training and Deploying Bipedal Robots Powered by Large Language Models `sim2real` | 2025-10 | G | re-decide | loco/sim+real |
| [GenDexHand: Generative Simulation for Dexterous Hands](https://arxiv.org/abs/2511.01791) | 2025-11 | G | re-decide | manip/sim |
| [Leveraging LLMs for reward function design in reinforcement learning control tasks](https://arxiv.org/abs/2511.19355) | 2025-11 | G | re-decide | other/sim |
| MoRE: Multi-Oracle Reward Evolution for Automated Reward Shaping in Reinforcement Learning | 2025-12 | G | re-decide | manip/sim |
| HicAgent: Hierarchical Iterative Cooperative Learning Reward Generation Guided by a Large Model | 2025-12 | G | re-decide | other/sim |
| MIRA: An LLM-Driven Dual-Loop Architecture for Metacognitive Reward Design | 2025-12 | G | re-decide | loco/sim |
| [E-SDS: Environment-aware See it, Do it, Sorted - Automated Environment-Aware Reinforcement Learning for Humanoid Locomotion](https://arxiv.org/abs/2512.16446) | 2025-12 | G | re-decide | humanoid/sim |
| [Unifying Deep Predicate Invention with Pre-trained Foundation Models](https://arxiv.org/abs/2512.17992) | 2025-12 | G | re-decide | manip/sim+real |
| [Embodied Learning of Reward for Musculoskeletal Control with Vision Language Models](https://arxiv.org/abs/2512.23077) | 2025-12 | G | re-decide | humanoid/sim |

</details>

<details><summary><b>Developer</b> (12)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Automatic Robotic Development through Collaborative Framework by Large Language Models](https://arxiv.org/abs/2402.03699) | 2023-11 | G | re-decide | other/real |
| [InterPreT: Interactive Predicate Learning from Language Feedback for Generalizable Task Planning](https://arxiv.org/abs/2405.19758) | 2024-05 | G | re-decide | manip/sim+real |
| Autonomous Discovery of Robot Structure and Motion Control Through Large Vision Models | 2024-08 | G | re-decide | other/sim |
| Debate2Create: Robot Co-design via Large Language Model Debates | 2025 | G | re-decide | loco/sim |
| SkillWrapper: Generative Predicate Invention for Skill Abstraction | 2025 | G | re-decide | mobile-manip/sim+real |
| [SAS-Prompt: Large Language Models as Numerical Optimizers for Robot Self-Improvement](https://arxiv.org/abs/2504.20459) | 2025-04 | G | re-decide | manip/sim+real |
| ASCENT: Autonomous Skill Learning Toward Complex Embodied Tasks With Foundation Models | 2025-05 | G | re-decide | manip/sim |
| [RoboMoRe: LLM-based Robot Co-design via Joint Optimization of Morphology and Reward](https://arxiv.org/abs/2506.00276) | 2025-05 | G | re-decide | loco/sim |
| [In-Context Iterative Policy Improvement for Dynamic Manipulation](https://arxiv.org/abs/2508.15021) | 2025-08 | G | re-decide | manip/sim+real |
| Human-in-the-loop Learning for Adaptive Robot Manipulation using Large Language Models and Behavior Trees | 2025-10 | G | re-decide | manip/sim+real |
| [Debate2Create: Robot Co-design via Multi-Agent LLM Debate](https://arxiv.org/abs/2510.25850) | 2025-10 | G | re-decide | loco/sim |
| LLM-Assisted Evolutionary Strategy for MuJoCo Control | 2025-11 | G | re-decide | loco/sim |

</details>


---

Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.
