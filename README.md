# Awesome Agentic Embodiment

> *Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs, not embodied action models — acting as agents that make explicit decisions whose consequences reach a robot body, and that re-decide on evidence of those consequences. Its organizing question is where such an agent sits relative to the body's deployed policy — steering it, guarding it, teaching it, designing its learning problem, or building its system (**Seat**).*

**Thesis (draft, under revision).** *Agency spreads around the body: general models, not embodied action models, fill seat after seat.*

Each seat is traced from its **46 pioneers (2022–2025)** to **93 papers from 2026**, the year most of the field's papers appeared; Real2Sim / Sim2Real (18 from 2026) and VLN / embodied navigation (13 from 2026) have their own chapters, plus **19 benchmarks and resources**. Definition and inclusion rules: [docs/definition.md](docs/definition.md) (Chinese).

## Scope and what counts as an agent

**Scope.** General-purpose foundation models (LLMs / VLMs such as GPT, Gemini, Claude, Qwen-VL, GPT-6 Astra) doing embodied work as agents. They may plan, call skills, tools or VLAs, write code or constraints, or emit actions directly (LLM-as-policy, e.g. GPT-6 Astra evaluated as a robot policy on RoboDojo). A general model fine-tuned for an agent role still counts if it keeps acting through an agent interface (e.g. GUAVA). **Embodied foundation models that produce actions are not included** — VLAs (also with reasoning, memory or self-correction), hierarchical VLAs, world action models, robot foundation models (π0.5, ECoT, OneTwoVLA, Hi Robot, Gemini Robotics, PaLM-E); they appear here only as tools called by an agent.

**Agent tests** (all three): (1) **explicit decisions** — plans, skill/tool/VLA calls, code, constraints, verdicts, system edits, or actions chosen by the general model; (2) **decision authority** — the model writes its options, or picks among them with a control action (stop / retry / replan / ask / keep-revert); (3) **closed loop** — the model is called again with its own earlier decisions and evidence of their consequences, *or* the constraints or program it wrote read live perception and adapt while the robot acts (an *authored* loop, e.g. ReKep, VoxPoser, Code as Policies). Two families are included even when written once (*Loop* = none): **constraint / keypoint programming** (ReKep-type) and **agentic Real2Sim**.

Also not included: scalar reward/value models, one-shot annotators, world-model foresight, game/text worlds, purely digital agents.

## Seat by period

| Seat | Phase | Pioneers 2022–2025 | 2026 | of which fine-tuned (C) |
|---|---|---|---|---|
| Controller | runtime | 28 | 44 | 3 |
| Supervisor | runtime | 4 | 8 | · |
| Teacher | pre-deployment | 3 | 10 | 2 |
| Designer | pre-deployment | 9 | 14 | · |
| Developer | pre-deployment | 2 | 17 | · |

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
- [Real2Sim / Sim2Real](#real2sim--sim2real)
- [VLN and embodied navigation](#vln-and-embodied-navigation)
- [Benchmarks and resources](#benchmarks-and-resources)
- [More 2026 papers (387)](#more-2026-papers)

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
| **SMART-LLM** | [SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models](https://arxiv.org/abs/2309.10062) | 2023 | IROS | G | code | 1:N | none | none | multi-robot/sim+real | – |
| **Look Before You Leap** | [Look Before You Leap: Unveiling the Power of GPT-4V in Robotic Vision-Language Planning](https://arxiv.org/abs/2311.17842) | 2023 | arXiv | G | skill-call | ×1 | re-decide | E | manip/sim+real | – |
| **AutoRT** | [AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963) | 2024 | arXiv | G | problem-spec | 1:N | none | none | multi-robot/real | Supervisor |
| **COME-robot** | [Closed-Loop Open-Vocabulary Mobile Manipulation with GPT-4V](https://arxiv.org/abs/2404.10220) [[project]](https://come-robot.github.io/) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | mobile-manip/real | – |
| **VLM-PC** | [Commonsense Reasoning for Legged Robot Adaptation with Vision-Language Models](https://arxiv.org/abs/2407.02666) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | loco/real | – |
| **BUMBLE** | [BUMBLE: Unifying Reasoning and Acting with Vision-Language Models for Building-wide Mobile Manipulation](https://arxiv.org/abs/2410.06237) | 2024 | ICRA | G | skill-call | ×1 | re-decide | E | mobile-manip/real | – |

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
| **Language to Rewards** | [Language to Rewards for Robotic Skill Synthesis](https://arxiv.org/abs/2306.08647) [[project]](https://language-to-reward.github.io/) | 2023 | CoRL | G | constraint | ×1 | authored | E | manip/sim+real | – |
| **VoxPoser** | [VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973) | 2023 | CoRL | G | constraint | ×1 | authored | E | manip/sim+real | – |
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
| **DROC** | [Distilling and Retrieving Generalizable Knowledge for Robot Manipulation via Language Corrections](https://arxiv.org/abs/2311.10678) [[project]](https://sites.google.com/stanford.edu/droc) | 2023 | ICRA | G | code | ×1 | re-decide | H | manip/real | – |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **PhysMem** | [PhysMem: Scaling Test-Time Memory for Embodied Physical Reasoning](https://arxiv.org/abs/2602.20323) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | manip/sim+real | – |
| **Harness VLA** | [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](https://arxiv.org/abs/2607.08448) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim | – |
| **Teach and Grow** | [Teach and Grow: An Agent-Centered Architecture for General Robot Learning](https://arxiv.org/abs/2608.17209) [[project]](https://tgl.changnie.top) | 2026 | arXiv | G | code | ×1 | authored | E+H | manip/real | – |
| **MessyMem** | [MessyMem: Learning-from-Doing Memory for Mobile Manipulation](https://arxiv.org/abs/2609.15976) [[project]](https://messymem.github.io) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | mobile-manip/sim+real | – |
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
| **Code-as-Monitor** | [Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection](https://arxiv.org/abs/2412.04455) [[project]](https://zhoues.github.io/Code-as-Monitor/) | 2024 | CVPR | G | verdict | ×1 | re-decide | E | manip/sim+real | Controller |

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
| **Manipulate-Anything** | [Manipulate-Anything: Automating Real-World Robots using Vision-Language Models](https://arxiv.org/abs/2406.18915) [[project]](https://robot-ma.github.io/) | 2024 | CoRL | G | skill-call | ×1 | re-decide | E | manip/sim+real | Controller |
| **RoboTwin 2.0** | [RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation](https://arxiv.org/abs/2506.18088) [[project]](https://robotwin-platform.github.io/) [[code]](https://github.com/robotwin-Platform/robotwin) | 2025 | arXiv | G | code | ×1 | re-decide | E | manip/sim+real | Designer |

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

## Real2Sim / Sim2Real

Agents that build or calibrate simulators from the real world (Real2Sim), transfer or adapt what they learned in simulation to the real robot (Sim2Real), or practise in a reconstructed simulator and go back to the real one (Real2Sim2Real). Each paper keeps its Seat: building the simulator is the problem side (Designer), adapting the solution is Developer.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **DrEureka** | [DrEureka: Language Model Guided Sim-To-Real Transfer](https://arxiv.org/abs/2406.01967) [[project]](https://eureka-research.github.io/dr-eureka/) | 2024 | RSS | Designer | G | problem-spec | re-decide | loco/sim+real | – |
| **Articulate AnyMesh** | [Articulate AnyMesh: Open-Vocabulary 3D Articulated Objects Modeling](https://arxiv.org/abs/2502.02590) | 2025 | arXiv | Designer | G | problem-spec | none | manip/sim+real | – |
| **Video2Policy** | [Video2Policy: Scaling up Manipulation Tasks in Simulation through Internet Videos](https://arxiv.org/abs/2502.09886) | 2025 | arXiv | Designer | G | problem-spec | re-decide | manip/sim | – |

**2026**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **Scene2Demo** | [Scene2Demo: Self-Evolving Embodied Data Generation via Object-Action Graph](https://arxiv.org/abs/2602.12065) | 2026 | arXiv | Teacher | G | skill-call | re-decide | manip/sim | Designer |
| **Vid2Sid** | [Vid2Sid: Videos Can Help Close the Sim2Real Gap](https://arxiv.org/abs/2602.19359) | 2026 | arXiv | Designer | G | problem-spec | re-decide | other/sim+real | – |
| **MotionDisco** | [MotionDisco: Motion Discovery for Extreme Humanoid Loco-Manipulation](https://arxiv.org/abs/2606.06139) | 2026 | arXiv | Teacher | G | trace | re-decide | humanoid/sim+real | – |
| **GaP** | [GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks](https://arxiv.org/abs/2607.05369) | 2026 | arXiv | Developer | G | code | re-decide | manip/sim+real | Designer |
| **Agentic Real2Sim** | [Agentic Real2Sim: Physics-based World Modeling with Vision-Language Agents](https://arxiv.org/abs/2607.19190) | 2026 | arXiv | Designer | G | problem-spec | re-decide | manip/sim+real | – |
| **DREAM** | [DREAM: Deployment-Time Demonstration Generation via Real-to-Sim for Scalable Policy Adaptation](https://arxiv.org/abs/2608.29078) | 2026 | arXiv | Designer | G | problem-spec | authored | manip/sim+real | Teacher |
| **Lucida** | [Lucida: Parse, Generate, and Place for Composable Real-to-Sim Scene Modeling](https://arxiv.org/abs/2608.30821) [[project]](https://lucida-r2s.github.io/) | 2026 | arXiv | Designer | G | problem-spec | re-decide | manip/sim | – |
| **SUN** | [SUN: Agentic Robot Policy Learning with Persistent Task Programs](https://arxiv.org/abs/2608.31167) | 2026 | arXiv | Designer | G | problem-spec | re-decide | manip/sim+real | Teacher |
| **GPT-6-Astra XLeRobot** | [Robot Manipulation with GPT-6-Astra: Body Knowledge, Experience Reuse, Emergent Skills, and Sim2Real Transfer](https://arxiv.org/abs/2609.31770) [[code]](https://github.com/hesd10/astra-robot-sim2real) | 2026 | arXiv | Controller | G | code | re-decide | mobile-manip/sim+real | – |
| **CoDimRecon** | [CoDimRecon: Agentic Reconstruction of Sim-Ready 3D Scenes with Deformable Curves, Surfaces, and Volumes](https://arxiv.org/abs/2609.36024) [[project]](https://shuzhaoxie.github.io/CoDimRecon/) | 2026 | arXiv | Designer | G | problem-spec | re-decide | manip/sim | – |
| **DexAgent** | [DexAgent: An Agentic Human2Sim2Robot Framework for Dexterous Manipulation with Self-Evolving Tool Library](https://arxiv.org/abs/2609.35318) [[project]](https://dexagent123.github.io/) | 2026 | arXiv | Teacher | G | code | re-decide | manip/sim+real | Developer |
| **F4R** | [F4R: Failure-Driven Recognition, Reconstruction, Refinement, and Redeployment for Continual Robot Self-Improvement](https://arxiv.org/abs/2609.35575) | 2026 | arXiv | Designer | G | problem-spec | re-decide | manip/sim+real | – |
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
| **InstructNav** | [InstructNav: Zero-shot System for Generic Instruction Navigation in Unexplored Environment](https://arxiv.org/abs/2406.04882) | 2024 | CoRL | Controller | G | constraint | re-decide | nav/sim | – |
| **Open-Nav** | [Open-Nav: Exploring Zero-Shot Vision-and-Language Navigation in Continuous Environment with Open-Source LLMs](https://arxiv.org/abs/2409.18794) | 2024 | ICRA | Controller | G | skill-call | re-decide | nav/sim+real | – |

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

387 further 2026 papers that meet the definition (judged `core` by a verification pass) but are not in the curated tables above. Tags come from the judging pass and are not hand-checked; generated by `scripts/build_extended.py`.

<details><summary><b>Controller · Orchestrators</b> (128)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| A Hierarchical Framework of Central-Distributed LLM Negotiation and Specialized Model Orchestration for Multi-Robot Collaborative Assembly | 2026 | G | re-decide | multi-robot/sim |
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
| [SafeGuard ASF: SR Agentic Humanoid Robot System for Autonomous Industrial Safety](https://arxiv.org/abs/2603.25353) | 2026-03 | G | re-decide | humanoid/sim+real |
| [ROSClaw: An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction](https://arxiv.org/abs/2603.26997) | 2026-03 | G | re-decide | loco/real |
| [On-Demand Human Assistance for Task Continuation under Physical Action Failures in LLM-based Planning](https://arxiv.org/abs/2603.28156) | 2026-03 | G | re-decide | mobile-manip/real |
| [OpenGo: An OpenClaw-Based Robotic Dog with Real-Time Skill Switching](https://arxiv.org/abs/2604.01708) | 2026-04 | G | re-decide | loco/real |
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
| [Say the Mission, Execute the Swarm: Agent-Enhanced LLM Reasoning in the Web-of-Drones](https://arxiv.org/abs/2605.03788) | 2026-05 | G | re-decide | aerial/sim |
| [BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation](https://arxiv.org/abs/2605.07306) | 2026-05 | G | re-decide | manip/real |
| [Melding LLM and temporal logic for reliable human-swarm collaboration in complex scenarios](https://arxiv.org/abs/2605.07877) | 2026-05 | G | re-decide | multi-robot/sim+real |
| [Qumus: Realization of An Embodied AI Quantum Material Experimentalist](https://arxiv.org/abs/2605.18407) | 2026-05 | G | re-decide | other/real |
| Man-Machine Collaborative Task Planning Based on Visual Language Models | 2026-05 | C | re-decide | manip/sim+real |
| [Sentinel: Embodied Cooperative Spatial Reasoning and Planning](https://arxiv.org/abs/2605.26239) | 2026-05 | G | re-decide | multi-robot/sim |
| [PEACE: A Planner-Executor Agent with Constraint Enforcement for UAVs](https://arxiv.org/abs/2606.00104) | 2026-05 | G | re-decide | aerial/sim |
| HiveNav: Hierarchical Semantic Planning for UAV Swarm Exploration | 2026-06 | G | re-decide | multi-robot/sim |
| Multi-Agent LLM Reasoning for Robotic Block Placement | 2026-06 | G | re-decide | manip/real |
| [PerceptTwin: Semantic Scene Reconstruction for Iterative LLM Planning and Verification](https://arxiv.org/abs/2606.04226) `real2sim2real` | 2026-06 | G | re-decide | mobile-manip/sim |
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
| Twin-BT: An LLM-Based Behavior Tree Framework Integrating Digital Twin and Deterministic Semantic Verification for Robotics `real2sim2real` | 2026-07 | G | re-decide | manip/sim+real |
| VLA-Touch: Enhancing Vision-Language-Action Model With Dual-Level Tactile Feedback | 2026-07 | G | re-decide | manip/real |
| World-Model-Enhanced UAV Intelligent Inspection Method for Converter Station Valve Halls | 2026-07 | G | re-decide | aerial/real |
| [HiMe: Hierarchical Embodied Memory for Long-Horizon Vision-Language-Action Control](https://arxiv.org/abs/2607.03449) | 2026-07 | G | re-decide | manip/sim+real |
| [ACE: Agentic Control for Embodied Manipulation via Zero-shot Workflow Reasoning](https://arxiv.org/abs/2607.04162) | 2026-07 | G | re-decide | manip/real |
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
| [ETA: A New Agentic Paradigm for Embodied Tasks](https://arxiv.org/abs/2608.03924) | 2026-08 | G | re-decide | manip/sim+real |
| PFEA: a VLM-based high-level natural language planning and feedback embodied agent for human-centered AI | 2026-08 | G | re-decide | manip/real |
| [HarnessWAM: Bridging Prediction and Deliberation in World Action Models](https://arxiv.org/abs/2608.09516) | 2026-08 | G | re-decide | manip/sim |
| [MistyPilot: Enabling Social-Robot Control through Multi-Agent LLM Skill Orchestration](https://arxiv.org/abs/2608.15549) | 2026-08 | G | authored | social/real |
| [HODAgent: Towards On-Demand, Responsive Humanoids for Physical World Human Interaction](https://arxiv.org/abs/2608.17584) | 2026-08 | G | re-decide | humanoid/sim+real |
| MulPlanLM: multimodal robotic task planning with vision-language models and physical feedback | 2026-08 | C | re-decide | manip/sim+real |
| [Evidence-Gated Task and Motion Planning with Vision-Language Models](https://arxiv.org/abs/2608.20084) | 2026-08 | G | re-decide | manip/sim |
| A human-verifiable execution-time DAG refinement framework for LLM-driven multi-robot construction task planning | 2026-08 | G | re-decide | multi-robot/sim |
| [$R^3$: Training Robots to Reason in Natural Language via Reinforcement Learning](https://arxiv.org/abs/2608.26053) | 2026-08 | C | re-decide | manip/sim |
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
| [Where Memory Belongs: Ledger, an Object Ledger for Memory-Augmented VLAs](https://arxiv.org/abs/2609.34554) | 2026-09 | G | re-decide | manip/sim |
| Agentic Preparative
Thin-Layer Chromatography System
for Autonomous Purification | 2026-09 | G | re-decide | manip/real |
| [Simple Agentic Memory for Generalist Robot Policies](https://arxiv.org/abs/2609.36595) | 2026-09 | G | re-decide | manip/sim |
| [RoboAssist: Interactive Human-Humanoid Planning for Long-Horizon Surgical Assistance](https://arxiv.org/abs/2609.39384) | 2026-09 | G | re-decide | humanoid/sim |
| [DuoMind: Enabling Distributed Multi-Robot Coordination with Semantic Communication](https://arxiv.org/abs/2610.02161) | 2026-10 | G | re-decide | multi-robot/sim |
| [ROMA: LLM System for Real-World Object-Centric Multi-Sensory Active Perception](https://arxiv.org/abs/2610.06955) | 2026-10 | C | re-decide | manip/real |
| [CIRRA: Dual-Level Continual Instruction Reconciliation with Ongoing Execution for Embodied Robot Agents in Interactive Household Tasks](https://arxiv.org/abs/2610.08862) | 2026-10 | G | re-decide | humanoid/real |
| [Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843) | 2026-10 | G | re-decide | manip/sim+real |
| [Toward Evidence-Driven Human-Agent-Robot Teaming for Earth-Independent Anomaly Triage](https://arxiv.org/abs/2610.08933) | 2026-10 | G | re-decide | mobile-manip/real |

</details>

<details><summary><b>Controller · Direct drivers</b> (70)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| From Ambiguous Language to Verifiable Plans: Integrating Formal Synthesis and Dynamic Affordance Reasoning | 2026 | G | authored | manip/sim |
| Physical Simulation‐Based Correction of LLM‐Generated Tool‐Using Primitives `sim2real` | 2026-01 | G | re-decide | manip/sim+real |
| [Real2Sim via Active Perception with Behavior Trees Automatically Generated by VLMs](https://arxiv.org/abs/2601.08454) `real2sim` | 2026-01 | G | authored | manip/real |
| [Bidirectional Human-Robot Communication for Physical Human-Robot Interaction](https://arxiv.org/abs/2601.10796) | 2026-01 | G | re-decide | manip/real |
| [ALRM: Agentic LLM for Robotic Manipulation](https://arxiv.org/abs/2601.19510) | 2026-01 | G | re-decide | manip/sim |
| A Multimodal Adaptive Framework for Social Interaction with the MiRo-E Robot | 2026-02 | G | re-decide | social/real |
| [BTGenBot-2: Efficient Behavior Tree Generation with Small Language Models](https://arxiv.org/abs/2602.01870) | 2026-02 | C | re-decide | mobile-manip/sim+real |
| [VLN-Pilot: Large Vision-Language Model as an Autonomous Indoor Drone Operator](https://arxiv.org/abs/2602.05552) | 2026-02 | G | re-decide | aerial/sim |
| [AtomBridge: Agentic VLA Inference Plugin for Long-Horizon Tasks in Scientific Experiments](https://arxiv.org/abs/2602.09430) | 2026-02 | G | re-decide | manip/real |
| [LLM-Grounded Dynamic Task Planning with Hierarchical Temporal Logic for Human-Aware Multi-Robot Handover](https://arxiv.org/abs/2602.09472) | 2026-02 | G | authored | multi-robot/sim+real |
| LLM-Based Decision Making Framework for Autonomous Drone Navigation | 2026-02 | G | re-decide | aerial/sim |
| [Safe and Interpretable Multimodal Path Planning for Multi-Agent Cooperation](https://arxiv.org/abs/2602.19304) | 2026-02 | G | re-decide | multi-robot/sim+real |
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
| Embodied SelfRect Robot: A Multi-Large-Model Control Framework with Iterative Self-Correction for Robotic Manipulation | 2026-06 | G | re-decide | manip/real |
| [Generating Natural and Expressive Robot Gestures through Iterative Reinforcement Learning with Human Feedback using LLMs](https://arxiv.org/abs/2606.18747) | 2026-06 | G | re-decide | social/real |
| [ZeroDex: Zero-Shot Long-Horizon Dexterous Manipulation via Multi-View 3D-Grounded VLM Reasoning](https://arxiv.org/abs/2606.19340) | 2026-06 | G | none | manip/real |
| [RelAfford6D: Relational 6D Affordance Graphs for Constraint-Driven Robotic Manipulation](https://arxiv.org/abs/2606.27036) | 2026-06 | G | authored | manip/real |
| [Hypothesis-driven Model Expansion under Uncertainty for Open-World Robot Planning](https://arxiv.org/abs/2607.06501) | 2026-07 | G | re-decide | mobile-manip/sim+real |
| A dual-agent framework for physically grounded and syntactically verifiable industrial robot programming | 2026-07 | G | re-decide | manip/sim+real |
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
| [Transferring the Intelligence of VLMs to Robotic Control](https://arxiv.org/abs/2609.22966) | 2026-09 | G | re-decide | manip/sim |
| [Generalizing Manipulation Skills with a Local Coding Agent](https://arxiv.org/abs/2609.26499) | 2026-09 | G | re-decide | manip/real |
| Execution-aware agent harness for accessible and responsible synthetic biology automation | 2026-09 | G | re-decide | other/real |
| [World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal](https://arxiv.org/abs/2609.29964) | 2026-09 | G | re-decide | manip/real |
| [DualManip: Agentic Dynamic Manipulation via Dual-Path Semantic Reasoning and Geometric Adaptation](https://arxiv.org/abs/2609.31112) | 2026-09 | G | re-decide | manip/real |
| [From Language to Task Maps: Compiling Semantic Relations While Preserving Task-Relevant Freedom](https://arxiv.org/abs/2609.34412) | 2026-09 | G | authored | manip/sim |
| [RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261) | 2026-09 | G | re-decide | manip/sim |
| [MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation](https://arxiv.org/abs/2609.38078) | 2026-09 | G | re-decide | manip/sim+real |
| [OrbitTAMP: Grounding Language Models for Task and Motion Planning in Spacecraft Rendezvous](https://arxiv.org/abs/2610.01093) | 2026-10 | G | none | other/sim |
| [Adaptive Code Generation for Controlling Robots](https://arxiv.org/abs/2610.09588) | 2026-10 | G | re-decide | loco/sim |

</details>

<details><summary><b>Controller · Lifelong / memory agents</b> (31)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Learning Without Losing Identity: Capability Evolution for Embodied Agents](https://arxiv.org/abs/2604.07799) | 2026 | G | re-decide | manip/sim |
| [Learning from Trials and Errors: Reflective Test-Time Planning for Embodied LLMs](https://arxiv.org/abs/2602.21198) | 2026-02 | C | re-decide | mobile-manip/sim |
| [Uni-Skill: Building Self-Evolving Skill Repository for Generalizable Robotic Manipulation](https://arxiv.org/abs/2603.02623) | 2026-03 | G | re-decide | manip/sim+real |
| [From Local Corrections to Generalized Skills: Improving Neuro-Symbolic Policies with MEMO](https://arxiv.org/abs/2603.04560) | 2026-03 | G | re-decide | manip/real |
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

<details><summary><b>VLN and embodied navigation</b> (42)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| AgenticNav: A Hierarchical Multi-Agentic System for LLM-Driven Autonomous Problem-Solving in Robotics | 2026 | G | re-decide | nav/sim+real |
| From Natural Language to Nonlinear Programs: An Agentic Framework for Instruction-Guided Trajectory Planning of Wheeled Robots | 2026 | G | re-decide | nav/sim |
| [Visual-Language-Guided Task Planning for Horticultural Robots](https://arxiv.org/abs/2601.11906) | 2026-01 | G | re-decide | nav/sim |
| [MerNav: A Highly Generalizable Memory-Execute-Review Framework for Zero-Shot Object Goal Navigation](https://arxiv.org/abs/2602.05467) | 2026-02 | G | re-decide | nav/sim+real |
| [3DGSNav: Enhancing Vision-Language Model Reasoning for Object Navigation via Active 3D Gaussian Splatting](https://arxiv.org/abs/2602.12159) | 2026-02 | G | re-decide | nav/sim+real |
| [SFCo-Nav: Efficient Zero-Shot Visual Language Navigation via Collaboration of Slow LLM and Fast Attributed Graph Alignment](https://arxiv.org/abs/2603.01477) | 2026-03 | G | re-decide | nav/sim |
| [MA-CoNav: A Master-Slave Multi-Agent Framework with Hierarchical Collaboration and Dual-Level Reflection for Long-Horizon Embodied VLN](https://arxiv.org/abs/2603.03024) | 2026-03 | G | re-decide | nav/sim |
| [CMMR-VLN: Vision-and-Language Navigation via Continual Multimodal Memory Retrieval](https://arxiv.org/abs/2603.07997) | 2026-03 | G | re-decide | nav/sim+real |
| [LightZeroNav: Zero-Shot Vision Language Navigation in Continuous Environments Based on Lightweight VLMs](https://arxiv.org/abs/2603.16947) | 2026-03 | G | re-decide | nav/sim |
| Perception–Awareness–Decision: Socially‑Aware Robot Navigation and Interaction | 2026-03 | G | re-decide | nav/real |
| [Interpreting Context-Aware Human Preferences for Multi-Objective Robot Navigation](https://arxiv.org/abs/2603.17510) | 2026-03 | G | re-decide | nav/sim |
| [OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms](https://arxiv.org/abs/2603.17351) | 2026-03 | G | re-decide | nav/real |
| [Explore Like Humans: Autonomous Exploration with Online SG-Memo Construction for Embodied Agents](https://arxiv.org/abs/2604.19034) | 2026-04 | G | re-decide | nav/sim |
| [Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance](https://arxiv.org/abs/2604.26839) | 2026-04 | G | re-decide | nav/real |
| USV-3.0: Cognitive maritime navigation through vision-language models, Human-in-the-Loop learning, and spatio-temporal memory | 2026-05 | G | re-decide | nav/real |
| Agile assistive hospital robot for suboptimal Task execution in dynamic environments | 2026-05 | G | re-decide | nav/real |
| [Bridging the 2D-3D Gap: A Hierarchical Semantic-Geometric Map for Vision Language Navigation](https://arxiv.org/abs/2606.00095) | 2026-05 | G | re-decide | nav/sim |
| [Uni-LaViRA: Language-Vision-Robot Actions Translation for Unified Embodied Navigation](https://arxiv.org/abs/2605.27582) | 2026-05 | G | re-decide | nav/sim+real |
| [EvoMemNav: Efficient Self-Evolving Fine-Grained Memory for Zero-Shot Embodied Navigation](https://arxiv.org/abs/2606.03509) | 2026-06 | G | re-decide | nav/sim |
| [SpaceVLN: A Zero-Shot Vision-and-Language Navigation Agent with Online Spatial Cognitive Memory and Reasoning](https://arxiv.org/abs/2606.08992) | 2026-06 | G | re-decide | nav/sim |
| [EvolveNav: Proactive Preflection and Self-Evolving Memory for Zero-Shot Object Goal Navigation](https://arxiv.org/abs/2606.18235) | 2026-06 | G | re-decide | nav/sim |
| [RAVEN: Long-Horizon Reasoning & Navigation with a Visuo-Spatio-Temporal Memory](https://arxiv.org/abs/2606.25206) | 2026-06 | G | re-decide | nav/real |
| [SAGE-Nav: Leveraging LLM Planning and Alignment Fusion for Hierarchical Scene Graph-Guided Navigation](https://arxiv.org/abs/2606.25497) | 2026-06 | G | re-decide | nav/sim |
| [ViTL: Temporal Logic-Guided Zero-Shot Natural Language Navigation via Vision-Language Models](https://arxiv.org/abs/2606.30696) | 2026-06 | G | authored | nav/sim |
| Agentic Llm-Driven Human-Robot Interaction | 2026-07 | G | re-decide | nav/sim |
| Safety-Aware Optimal Control With Language-Guided Online Parameter Adjustment via Large Language Models | 2026-07 | G | authored | nav/sim+real |
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
| [Hierarchical Floorplan-Guided Vision-Language Exploration for Embodied Question Answering](https://arxiv.org/abs/2609.26360) | 2026-09 | G | re-decide | nav/sim |
| [Spatial and Semantic Reasoning for LLM-Driven Robot Navigation via MCP](https://arxiv.org/abs/2609.27340) | 2026-09 | G | re-decide | nav/sim |
| [Actively Resolving Contextual Uncertainty for Underspecified Tasks in Natural Language](https://arxiv.org/abs/2609.30428) | 2026-09 | G | re-decide | nav/real |
| [RECAST: Recasting Vision-Language Semantics into an Actionable Cost Map for Robot Navigation](https://arxiv.org/abs/2609.32595) | 2026-09 | G | none | nav/sim+real |
| [NavHarness: Towards Lifelong Embodied Navigation](https://arxiv.org/abs/2609.34276) | 2026-09 | G | re-decide | nav/sim |
| [NavHarness: Adaptive Goals for Agentic Vision-Language Navigation](https://arxiv.org/abs/2609.39915) | 2026-09 | G | re-decide | nav/sim |

</details>

<details><summary><b>Supervisor</b> (23)</summary>

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
| Grasp, Reason, Act: Tactile-Language Model for Zeroshot Sim2real Grasp Stability Prediction and Re-Grasping | 2026-05 | C | re-decide | manip/sim+real |
| [Make Your VLA More Robust Without More Data By Interleaving Motion Planning](https://arxiv.org/abs/2606.00985) | 2026-05 | G | re-decide | mobile-manip/sim+real |
| VigiClaw: Action-Triggered State Verification for Robust Long-Horizon Robotic Manipulation | 2026-07 | G | re-decide | manip/sim |
| [Learning Robust Execution in Robotic Manipulation with Agentic Reinforcement Learning](https://arxiv.org/abs/2607.13818) | 2026-07 | C | re-decide | manip/sim |
| [From Sign Language Generation to Humanoid Execution: Vision-Language Guided Retargeting with Collision Mitigation](https://arxiv.org/abs/2607.17769) | 2026-07 | G | re-decide | humanoid/sim |
| [FORGE-plus: Force-Budgeted Recovery for Contact-Rich Assembly with a Frozen LLM Supervisor](https://arxiv.org/abs/2607.21227) | 2026-07 | G | re-decide | manip/sim |
| Predictive vision-language monitoring for proactive safety in robot task execution | 2026-08 | G | re-decide | mobile-manip/sim |
| [REVOLVE: An Automated Closed-Loop Framework for Evolving Robot Manipulation with Minimal Human Intervention](https://arxiv.org/abs/2609.14633) | 2026-09 | G | re-decide | manip/real |
| [Talk2Escape: Conversational Grounding for Vision-and-Language Navigation](https://arxiv.org/abs/2609.28296) | 2026-09 | G | re-decide | nav/sim |
| [Body-Grounded Replanning for Physically Adaptive Manipulation](https://arxiv.org/abs/2609.30024) | 2026-09 | G | re-decide | manip/sim+real |
| [SOR-Nav: Search or Relocate? Context-Gated Exploration and Cross-Region Relocation for Object Navigation](https://arxiv.org/abs/2609.34707) | 2026-09 | G | re-decide | nav/sim |
| [ProAct-VLM: Pre-Failure Vision-Language Task Replanning with Continuous Perception Feedback](https://arxiv.org/abs/2609.37681) | 2026-09 | G | re-decide | manip/real |
| [AVERT-VLN: Abstention-aware Visual Error Recovery and Training for Vision-and-Language Navigation](https://arxiv.org/abs/2609.39579) | 2026-09 | C | re-decide | nav/sim |
| [AeroEval: Staged Program and Execution Validation for AI-Generated Drone Missions](https://arxiv.org/abs/2610.09764) | 2026-10 | G | re-decide | aerial/sim |

</details>

<details><summary><b>Teacher</b> (13)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
| [Accelerating Robotic Reinforcement Learning with Agent Guidance](https://arxiv.org/abs/2602.11978) | 2026-02 | G | re-decide | manip/real |
| Gentle Manipulation of Long-Horizon Tasks Without Human Demonstrations | 2026-03 | G | re-decide | manip/sim+real |
| [HATS: A Human-Agent Teleoperation System for Multi-Arm Data Collection](https://arxiv.org/abs/2606.16491) | 2026-06 | G | re-decide | manip/real |
| [InSight: Self-Guided Skill Acquisition via Steerable VLAs](https://arxiv.org/abs/2606.24884) | 2026-06 | G | re-decide | manip/real |
| [Zero2Skill: Bootstrapping Robot Skills through Autonomous Data Collection, Training, and Deployment](https://arxiv.org/abs/2607.14047) | 2026-07 | G | re-decide | manip/real |
| [EXIMO: VLM Guided Exploration of VLA Policies](https://arxiv.org/abs/2608.19891) | 2026-08 | G | re-decide | manip/sim+real |
| [SafeBranch: Branch-Pair Safety Alignment for Embodied Agents](https://arxiv.org/abs/2608.19729) | 2026-08 | C | re-decide | mobile-manip/sim |
| [MAGMA-GEN: Validated Recovery Supervision from Ambiguous Failures via Counterfactual Re-Execution](https://arxiv.org/abs/2609.20056) | 2026-09 | G | re-decide | manip/sim |
| [TANDEM: Task and Motion Planning with As-Needed Demonstrations for Efficient Vision-Language-Action Model Fine-tuning](https://arxiv.org/abs/2609.28314) | 2026-09 | G | authored | manip/sim+real |
| [RE-0: Verified Recursive Improvement of Embodied Code-as-Policy Agents through Local On-Policy Distillation](https://arxiv.org/abs/2609.32416) | 2026-09 | G | re-decide | manip/sim |
| [EmbodiRSI: Recursive Self-Improvement for Data-Efficient Robot Adaptation](https://arxiv.org/abs/2609.38905) `real2sim2real` | 2026-09 | G | re-decide | manip/sim+real |
| [Recova: Agent-Guided Failure Recovery for Autonomous Robotic Manipulation](https://arxiv.org/abs/2610.01178) | 2026-10 | G | re-decide | manip/sim+real |
| [Recursive Self-Improvement of Visuomotor Policies through Local Recovery Supervision](https://arxiv.org/abs/2610.05151) | 2026-10 | G | re-decide | manip/sim |

</details>

<details><summary><b>Designer</b> (41)</summary>

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
| Constraint-Aware LLM Pipeline for EvoGym Environment Generation with Fitness-Guided Prompt Refinement | 2026-03 | G | re-decide | other/sim |
| [GenPHRI: Agentic Generative Simulation for Physical Human-Robot Interaction](https://arxiv.org/abs/2604.08664) `sim2real` | 2026-04 | G | re-decide | manip/sim+real |
| [V-CAGE: Vision-Closed-Loop Agentic Generation Engine for Robotic Manipulation](https://arxiv.org/abs/2604.09036) | 2026-04 | G | re-decide | manip/sim |
| CAAI-ST: Constraint-Aware AI-Guided Seed Generation and Mutation for CPS-UAV System Testing | 2026-04 | G | re-decide | aerial/sim |
| [Chain of Uncertain Rewards with Large Language Models for Reinforcement Learning](https://arxiv.org/abs/2604.13504) | 2026-04 | G | re-decide | manip/sim |
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
| [EmbodiedGen V2: An Agentic, Simulation-Ready 3D World Engine for Embodied AI](https://arxiv.org/abs/2607.07459) | 2026-07 | G | re-decide | manip/sim+real |
| [Prompt-Driven Exploration](https://arxiv.org/abs/2607.08837) | 2026-07 | G | re-decide | manip/sim |
| [MLREF: Efficient Module Reuse for Reward Design in Reinforcement Learning via Large Language Models](https://arxiv.org/abs/2608.18827) | 2026-08 | G | re-decide | other/sim |
| [NeoWorld-Pro: Programming Interactive Scenes from Monocular Images for Embodied Simulation](https://arxiv.org/abs/2608.24212) `real2sim` | 2026-08 | G | re-decide | manip/sim |
| [DISEIL: Demonstration Distillation for Sample-Efficient Imitation Learning](https://arxiv.org/abs/2609.08123) | 2026-09 | G | re-decide | manip/sim |
| [DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation](https://arxiv.org/abs/2609.18620) | 2026-09 | G | re-decide | manip/sim |
| [DiagGen: Agentic Generation of Deformable Assets with Sim-based Diagnostics for Robotic Simulation](https://arxiv.org/abs/2609.23103) `real2sim` | 2026-09 | G | re-decide | manip/sim |
| [MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation](https://arxiv.org/abs/2609.24145) `sim2real` | 2026-09 | G | re-decide | loco/sim+real |
| [Beyond Scripted Search: Sample-Efficient Reward Discovery via Agentic Black-box Optimization](https://arxiv.org/abs/2609.32394) | 2026-09 | G | re-decide | other/sim |
| [Test-Time Spatial Reasoning for Robot Manipulation Using Generative Real-to-Sim](https://arxiv.org/abs/2609.33982) `real2sim2real` | 2026-09 | G | none | manip/sim+real |
| [FACT: Fidelity-Aware Construction of Articulated Twins](https://arxiv.org/abs/2609.37067) `real2sim` | 2026-09 | G | re-decide | manip/sim |
| [Video2SwimFish: An Automated Pipeline for Reconstructing Controllable Fish Models and Biological Locomotion from Real Fish Videos](https://arxiv.org/abs/2609.38966) `real2sim` | 2026-09 | G | re-decide | other/sim |
| [Awomo-SimDataEngine: Agentic Simulation-ReadyWorld Generation](https://arxiv.org/abs/2610.02274) | 2026-10 | G | re-decide | manip/sim |
| [LiteReality-Agent: An Agentic System for Interactable 3D Indoor Scene Reconstruction](https://arxiv.org/abs/2610.01863) `real2sim` | 2026-10 | G | re-decide | other/sim |
| [EnvDreamer: Large-Scale Multimodal-to-Environment Generation for Embodied AI](https://arxiv.org/abs/2610.04301) `real2sim` | 2026-10 | G | re-decide | mobile-manip/sim |
| [Demo: Vision-Language Model-Guided Online Calibration of an Electromagnetic Digital Twin](https://arxiv.org/abs/2610.07081) `real2sim` | 2026-10 | G | re-decide | humanoid/real |

</details>

<details><summary><b>Developer</b> (39)</summary>

| Paper | Month | Carrier | Loop | Body |
|---|---|---|---|---|
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
| LLMigrate: Large Language Models as Migration Controllers in Island-Based Evolutionary Design of Soft Robots | 2026-07 | G | re-decide | other/sim |
| [MEMENTO: Memory-Guided Memetic Code-as-Policy Evolution](https://arxiv.org/abs/2607.22832) | 2026-07 | G | re-decide | manip/sim |
| [A Few Words Go a Long Way: Language Guided Robot Policy Synthesis](https://arxiv.org/abs/2607.23784) | 2026-07 | G | re-decide | manip/sim+real |
| [An AI Scientist that Doesn't Drift: Taste, Structure, and Falsifiable Findings in a Quadruped Navigation Research Loop](https://arxiv.org/abs/2608.07542) | 2026-07 | G | re-decide | loco/sim |
| [You Don't Need To Stay in The Loop: An Agentic Robotics Loop for Robot-Policy Improvement](https://arxiv.org/abs/2608.07555) | 2026-08 | G | re-decide | manip/sim |
| [RoboReact: Agentic Skill Distillation from Generated Egocentric Videos for Generalizable Whole-Body Manipulation](https://arxiv.org/abs/2608.03387) | 2026-08 | G | re-decide | humanoid/sim+real |
| [Skills in Weights, Memory in Code: Hybrid Learning for Memory-Dependent Robot Manipulation](https://arxiv.org/abs/2608.09410) | 2026-08 | G | re-decide | manip/sim+real |
| [Revisiting the"Push-T"Robot Manipulation Task with Agentic Robotics](https://arxiv.org/abs/2608.18227) | 2026-08 | G | re-decide | manip/sim |
| [LEMCA: LLM-Guided Synthesis of Efficient Mode-Switching Control Architectures](https://arxiv.org/abs/2609.21319) | 2026-09 | G | re-decide | other/sim |
| [From Ideal Motion to Flight-Executable Communications: LLM-Evolved Multi-UAV Deployment for Cell-Free Massive MIMO](https://arxiv.org/abs/2609.23992) | 2026-09 | G | re-decide | multi-robot/sim |
| [What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery](https://arxiv.org/abs/2609.31760) | 2026-09 | G | re-decide | manip/sim |
| [Coding Agents for Generalized Task and Motion Planning Problems](https://arxiv.org/abs/2609.30233) | 2026-09 | G | re-decide | manip/sim |
| [HarnessPAI: An Evolving Harness for Physical AI](https://arxiv.org/abs/2609.29166) | 2026-09 | G | re-decide | manip/sim+real |
| [HuGo: LLMs as Whole-Body Policy Code Designers for Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.30594) | 2026-09 | G |  | humanoid/sim+real |
| [RACaP: Agentic Reasoning, Acting, and Coding as Policies for Evolvable Robot Learning](https://arxiv.org/abs/2609.29394) | 2026-09 | G | re-decide | manip/sim |
| [RAPID: Robot Agentic Programming from Demonstrations](https://arxiv.org/abs/2609.30249) | 2026-09 | G | re-decide | manip/sim+real |
| [Encore: Few-Shot Agentic Discovery of Manipulation Strategies](https://arxiv.org/abs/2609.37359) | 2026-09 | G | re-decide | manip/sim |
| [DynaHarness: A Dynamic Physical Harness for Self-Evolving Robot Agents](https://arxiv.org/abs/2609.40306) | 2026-09 | G | re-decide | manip/sim+real |
| [Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents](https://arxiv.org/abs/2609.39304) | 2026-09 | G |  | manip/sim |
| [Iterative Policy Refinement through Semantic Rollout Analysis](https://arxiv.org/abs/2610.01652) | 2026-10 | G | re-decide | manip/sim |
| [EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432) | 2026-10 | G | re-decide | mobile-manip/sim |
| [PEARS: Physical-Prior-Guided Efficient Adaptation via Failure Reasoning and Diffusion Steering for Tactile Manipulation](https://arxiv.org/abs/2610.08784) | 2026-10 | G | re-decide | manip/real |
| [EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution](https://arxiv.org/abs/2610.10498) | 2026-10 | G | re-decide | manip/sim+real |

</details>


---

Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.
