# Awesome Agentic Embodiment

> *Agentic Embodiment studies foundation-model-driven processes that make explicit decisions whose consequences reach a robot body, and that re-decide on evidence of those consequences. Its organizing question is where such a process sits relative to the body's deployed policy — steering it, guarding it, teaching it, designing its learning problem, or building its system (**Seat**) — and which weights carry it (**Carrier**).*

**Thesis.** *Agency spreads around the body — and loop closure, not weights, makes a carrier an agent.*

This list holds the survey's core table: **57 core papers**, **8 precursors** and **0 resources**, organized by Seat. Definition and inclusion rules: [docs/definition.md](docs/definition.md) (Chinese).

## What counts as an agent

All three must hold: (1) **explicit decisions** — plans, skill/tool/VLA calls, code, verdicts, system edits (not scores, latents or action chunks); (2) **decision authority** — the model writes its options, or picks among them with a control action (stop / retry / replan / ask / keep-revert); (3) **closed loop** — the model is called again with its own earlier decisions and evidence of their consequences, and can revise them.

Not included: reactive VLAs (incl. RL-finetuned), latent dual-systems, scalar reward/value models, one-shot annotators, world-model foresight (see the WAM survey), game/text worlds, purely digital agents.

## Seat × Carrier

Core papers per cell (carrier of the source decider; Teacher rows count the teacher).

| Seat | Phase | G | C | H | I | Total |
|---|---|---|---|---|---|---|
| Controller | runtime | 21 | 2 | 2 | 2 | 27 |
| Supervisor | runtime | 7 | · | 1 | · | 8 |
| Teacher | pre-deployment | 6 | · | · | · | 6 |
| Designer | pre-deployment | 8 | · | · | · | 8 |
| Developer | pre-deployment | 8 | · | · | · | 8 |

**Legend.** *Carrier* — weights of the top-level decider: **G** general model used as-is, **C** embodied-trained decider + generic executor, **H** trained decider + co-designed learned executor, **I** one model decides and acts (→ marks migration, e.g. G→C). *Topology* — ×1 single agent, ×R role agents on one task, ×N one agent per robot, 1:N one decider for many robots, ×O agents owning branches of a campaign. *Closure* — evidence used to re-decide: E execution, H human.

## Contents

- [Controller · Orchestrators](#controller--orchestrators)
- [Controller · Direct drivers](#controller--direct-drivers)
- [Controller · Lifelong / memory agents](#controller--lifelong--memory-agents)
- [Controller · Trained carriers (C / H / I)](#controller--trained-carriers-c--h--i)
- [Supervisor](#supervisor)
- [Teacher](#teacher)
- [Designer](#designer)
- [Developer](#developer)
- [Precursors](#precursors)
- [Benchmarks and resources](#benchmarks-and-resources)

## Controller · Orchestrators

Called during evaluated episodes; sequence skills, tools or VLAs-as-tools.

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **SayCan** | [Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691) | 2022 | CoRL | G | skill-call | ×1 | E | mobile-manip/real | – |
| **Inner Monologue** | [Inner Monologue: Embodied Reasoning through Planning with Language Models](https://arxiv.org/abs/2207.05608) | 2022 | CoRL | G | skill-call | ×1 | E+H | manip/sim+real | – |
| **RoCo** | [RoCo: Dialectic Multi-Robot Collaboration with Large Language Models](https://arxiv.org/abs/2307.04738) | 2023 | ICRA | G | skill-call | ×N | E | multi-robot/sim+real | – |
| **GPT-4V Look Before You Leap** | [Look Before You Leap: Unveiling the Power of GPT-4V in Robotic Vision-Language Planning](https://arxiv.org/abs/2311.17842) | 2023 | arXiv | G | skill-call | ×1 | E | manip/sim+real | – |
| **MOSAIC** | [MOSAIC: Modular Foundation Models for Assistive and Interactive Cooking](https://arxiv.org/abs/2402.18796) | 2024 | CoRL | G | skill-call | 1:N | E+H | multi-robot/real | – |
| **Dynamic Scene Graph Search** | [Language-Grounded Dynamic Scene Graphs for Interactive Object Search with Mobile Manipulation](https://arxiv.org/abs/2403.08605) | 2024 | IEEE Robotics and Automation Letters | G | skill-call | ×1 | E | mobile-manip/sim+real | – |
| **COME-robot** | [Closed-Loop Open-Vocabulary Mobile Manipulation with GPT-4V](https://arxiv.org/abs/2404.10220) | 2024 | ICRA | G | skill-call | ×1 | E | mobile-manip/real | – |
| **Being-0** | [Being-0: A Humanoid Robotic Agent with Vision-Language Models and Modular Skills](https://arxiv.org/abs/2503.12533) | 2025 | arXiv | G | skill-call | ×R | E | humanoid/real | – |
| **Agentic Robot** | [Agentic Robot: A Brain-Inspired Framework for Vision-Language-Action Models in Embodied Agents](https://arxiv.org/abs/2505.23450) | 2025 | arXiv | G | vla-call | ×R | E | manip/sim | Supervisor |
| **RoboClaw** | [RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks](https://arxiv.org/abs/2603.11558) | 2026 | arXiv | G | skill-call | ×1 | E | manip/real | Teacher |
| **Thea** | [Towards the Harness of Embodied Agents](https://arxiv.org/abs/2608.11246) | 2026 | arXiv | G | skill-call | ×1 | E | mobile-manip/real | Supervisor |

## Controller · Direct drivers

Called during evaluated episodes; emit semantic micro-actions, native commands or code executed now.

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **InstructNav** | [InstructNav: Zero-shot System for Generic Instruction Navigation in Unexplored Environment](https://arxiv.org/abs/2406.04882) | 2024 | CoRL | G | constraint | ×1 | E | nav/sim | – |
| **FAEA** | [Demonstration-Free Robotic Control via LLM Agents](https://arxiv.org/abs/2601.20334) | 2026 | arXiv | G | code | ×1 | E | manip/sim | – |
| **CaP-X** | [CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation](https://arxiv.org/abs/2603.22435) | 2026 | arXiv | G | code | ×1 | E | manip/sim+real | Developer |
| **VIA** | [VIA: Visual Interface Agent for Robot Control](https://arxiv.org/abs/2607.11119) | 2026 | arXiv | G | micro-action | ×1 | E | manip/sim+real | – |
| **Show-Harness** | [Show-Harness: Just a VLM Agent Can Play Robots](https://arxiv.org/abs/2609.10522) | 2026 | arXiv | G | micro-action | ×1 | E | manip/sim+real | – |
| **Agent as Policy** | [Agent as Policy for Robotic Manipulation](https://arxiv.org/abs/2609.12541) | 2026 | arXiv | G | code | ×1 | E | manip/real | – |

## Controller · Lifelong / memory agents

Improve memory, skill libraries or harness across evaluated episodes.

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **DROC** | [Distilling and Retrieving Generalizable Knowledge for Robot Manipulation via Language Corrections](https://arxiv.org/abs/2311.10678) | 2023 | ICRA | G | code | ×1 | H | manip/real | – |
| **LRLL** | [Lifelong Robot Library Learning: Bootstrapping Composable and Generalizable Skills for Embodied Control with Language Models](https://arxiv.org/abs/2406.18746) | 2024 | ICRA | G | code | ×1 | E | manip/sim | Developer |
| **Harness VLA** | [Harness VLA: Steering Frozen VLAs into Reliable Manipulation Primitives via Memory-Guided Agents](https://arxiv.org/abs/2607.08448) | 2026 | arXiv | G | code | ×1 | E | manip/sim+real | – |
| **MessyMem** | [MessyMem: Learning-from-Doing Memory for Mobile Manipulation](https://arxiv.org/abs/2609.15976) | 2026 | arXiv | G | skill-call | ×1 | E | mobile-manip/sim+real | – |

## Controller · Trained carriers (C / H / I)

The decider itself is embodied-trained: generic executor (C), co-designed executor (H) or one model (I).

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **PaLM-E** | [PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378) | 2023 | ICML | C | skill-call | ×1 | E | mobile-manip/real | – |
| **Hi Robot** | [Hi Robot: Open-Ended Instruction Following with Hierarchical Vision-Language-Action Models](https://arxiv.org/abs/2502.19417) | 2025 | ICML | H | vla-call | ×1 | E+H | mobile-manip/real | – |
| **OneTwoVLA** | [OneTwoVLA: A Unified Vision-Language-Action Model with Adaptive Reasoning](https://arxiv.org/abs/2505.11917) | 2025 | arXiv | I | micro-action | ×1 | E+H | manip/real | – |
| **Robix** | [Robix: A Unified Model for Robot Interaction, Reasoning and Planning](https://arxiv.org/abs/2509.01106) | 2025 | arXiv | C | skill-call | ×1 | E+H | manip/real | – |
| **Gemini Robotics 1.5** | [Gemini Robotics 1.5: Pushing the Frontier of Generalist Robots with Advanced Embodied Reasoning, Thinking, and Motion Transfer](https://arxiv.org/abs/2510.03342) | 2025 | arXiv | H | vla-call | ×1 | E | manip/real | – |
| **MEM** | [MEM: Multi-Scale Embodied Memory for Vision Language Action Models](https://arxiv.org/abs/2603.03596) | 2026 | arXiv | I | skill-call | ×1 | E | mobile-manip/real | – |

## Supervisor

Runtime, acts only on exceptions: gates, vetoes, failure detection and recovery, by a separate check process.

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **REFLECT** | [REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction](https://arxiv.org/abs/2306.15724) | 2023 | CoRL | G | verdict | ×1 | E | manip/sim+real | Controller |
| **DoReMi** | [DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329) | 2023 | IROS | G | verdict | ×R | E | manip/sim+real | Controller |
| **Code-as-Monitor** | [Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection](https://arxiv.org/abs/2412.04455) | 2024 | CVPR | G | verdict | ×1 | E | manip/sim+real | Controller |
| **Phoenix** | [Phoenix: A Motion-based Self-Reflection Framework for Fine-grained Robotic Action Correction](https://arxiv.org/abs/2504.14588) | 2025 | CVPR | H | vla-call | ×1 | E | manip/sim+real | – |
| **RoboSafe** | [RoboSafe: Safeguarding Embodied Agents via Executable Safety Logic](https://arxiv.org/abs/2512.21220) | 2025 | arXiv | G | verdict | ×1 | E | manip/sim+real | – |
| **CycleVLA** | [CycleVLA: Proactive Self-Correcting Vision-Language-Action Models via Subtask Backtracking and Minimum Bayes Risk Decoding](https://arxiv.org/abs/2601.02295) | 2026 | arXiv | G | verdict | ×1 | E | manip/sim | Controller |
| **FRAMES** | [FRAMES: Failure Recovery And Monitoring of Embodied Skills for Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.22538) | 2026 | arXiv | G | verdict | ×R | E | humanoid/sim+real | Controller |
| **WhenToAsk** | [When Should a Failing Robot Ask? Initiating Corrective Human-Robot Dialogue from Audited Sensor Evidence](https://arxiv.org/abs/2609.21942) | 2026 | arXiv | G | verdict | ×1 | E+H | manip/sim+real | – |

## Teacher

Before deployment, the agent acts; its outcome-checked behaviour becomes the deployed model's training target.

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **Manipulate-Anything** | [Manipulate-Anything: Automating Real-World Robots using Vision-Language Models](https://arxiv.org/abs/2406.18915) | 2024 | CoRL | G | skill-call | ×1 | E | manip/sim+real | Controller |
| **RoboTwin 2.0** | [RoboTwin 2.0: A Scalable Data Generator and Benchmark with Strong Domain Randomization for Robust Bimanual Robotic Manipulation](https://arxiv.org/abs/2506.18088) | 2025 | arXiv | G | code | ×1 | E | manip/sim+real | Designer |
| **GUAVA** | [Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness](https://arxiv.org/abs/2606.18363) | 2026 | arXiv | G→C | trace | ×1 | E | manip/sim+real | Controller |
| **LocalNav** | [LocalNav: Distilling Frontier VLMs and Embodied RL for On-Device Object Goal Navigation](https://arxiv.org/abs/2606.27871) | 2026 | arXiv | G→C | skill-call | ×1 | E | nav/sim | Controller |
| **EmbodiedSWE** | [EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics](https://arxiv.org/abs/2609.27308) | 2026 | arXiv | G | code | ×1 | E | manip/sim+real | Controller |
| **RHD** | [Recursive Harness Distillation across Agents for Robot Manipulation](https://arxiv.org/abs/2609.33378) | 2026 | arXiv | G | trace | ×R | E | manip/sim+real | Controller |

## Designer

Before deployment, the agent designs the learning problem: rewards, tasks, environments, curricula, eval suites.

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **Eureka** | [Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931) | 2023 | ICLR | G | problem-spec | ×1 | E | manip/sim | – |
| **OMNI-EPIC** | [OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code](https://arxiv.org/abs/2405.15568) | 2024 | arXiv | G | problem-spec | ×R | E | loco/sim | – |
| **REvolve** | [REvolve: Reward Evolution with Large Language Models using Human Feedback](https://arxiv.org/abs/2406.01309) | 2024 | ICLR | G | problem-spec | ×1 | E+H | humanoid/sim | – |
| **DrEureka** | [DrEureka: Language Model Guided Sim-To-Real Transfer](https://arxiv.org/abs/2406.01967) | 2024 | Robotics: Science and Systems Conference | G | problem-spec | ×1 | E | loco/sim+real | – |
| **CurricuLLM** | [CurricuLLM: Automatic Task Curricula Design for Learning Complex Robot Skills using Large Language Models](https://arxiv.org/abs/2409.18382) | 2024 | ICRA | G | problem-spec | ×1 | E | humanoid/sim | – |
| **Eurekaverse** | [Eurekaverse: Environment Curriculum Generation via Large Language Models](https://arxiv.org/abs/2411.01775) | 2024 | CoRL | G | problem-spec | ×1 | E | loco/sim+real | – |
| **Video2Policy** | [Video2Policy: Scaling up Manipulation Tasks in Simulation through Internet Videos](https://arxiv.org/abs/2502.09886) | 2025 | arXiv | G | problem-spec | ×1 | E | manip/sim | – |
| **FIND** | [Find Something You Can't Do: Agentic Real-World Reinforcement Learning for Self-Improving VLA Models](https://arxiv.org/abs/2609.32069) | 2026 | arXiv | G | problem-spec | ×1 | E | manip/real | – |

## Developer

Before deployment, the agent edits the solution: policy code, skill libraries, harness, training code, hardware; keeps or reverts by its own experiments.

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **RoboMorph** | [RoboMorph: Evolving Robot Morphology using Large Language Models](https://arxiv.org/abs/2407.08626) | 2024 | ICRA | G | system-edit | ×1 | E | loco/sim | – |
| **VLMgineer** | [VLMgineer: Vision Language Models as Robotic Toolsmiths](https://arxiv.org/abs/2507.12644) | 2025 | arXiv | G | code | ×1 | E | manip/sim | – |
| **HARBOR** | [HARBOR: A Harness Framework for Agentic Robot Reinforcement Learning](https://arxiv.org/abs/2606.08610) | 2026 | arXiv | G | system-edit | ×R | E | manip/sim | Designer |
| **RHO** | [RHO: Your Coding Agent is Secretly a Roboticist](https://arxiv.org/abs/2606.16458) | 2026 | arXiv | G | system-edit | ×1 | E | manip/sim | – |
| **ENPIRE** | [ENPIRE: Agentic Robot Policy Self-Improvement in the Real World](https://arxiv.org/abs/2606.19980) | 2026 | arXiv | G | system-edit | ×1 | E | manip/real | – |
| **ASPIRE** | [ASPIRE: Agentic /Skills Discovery for Robotics](https://arxiv.org/abs/2607.00272) | 2026 | arXiv | G | system-edit | ×1 | E | manip/sim+real | Controller |
| **SimEX** | [SimEX: Simulation-Integrated Robotics AutoResearch](https://arxiv.org/abs/2609.38982) | 2026 | arXiv | G | system-edit | ×1 | E | manip/sim+real | Designer |
| **Skill2Real** | [Skill2Real: Agentic Skill Learning for Zero-Shot Sim-to-Real Robot Manipulation](https://arxiv.org/abs/2610.02788) | 2026 | arXiv | G | system-edit | ×R | E | manip/sim+real | Controller |

## Precursors

Foundational works that make explicit decisions with authority but do not close the loop on their own decisions (one-shot plans or programs, per-step decisions without own history). Kept as lineage.

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **ZS-Planners** | [Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents](https://arxiv.org/abs/2201.07207) | 2022 | ICML | G | skill-call | ×1 | none | other/sim | – |
| **Code as Policies** | [Code as Policies: Language Model Programs for Embodied Control](https://arxiv.org/abs/2209.07753) | 2022 | ICRA | G | code | ×1 | none | manip/real | – |
| **ProgPrompt** | [ProgPrompt: Generating Situated Robot Task Plans using Large Language Models](https://arxiv.org/abs/2209.11302) | 2022 | ICRA | G | code | ×1 | none | mobile-manip/sim+real | – |
| **KnowNo** | [Robots That Ask For Help: Uncertainty Alignment for Large Language Model Planners](https://arxiv.org/abs/2307.01928) | 2023 | CoRL | G | skill-call | ×1 | H | mobile-manip/sim+real | – |
| **VoxPoser** | [VoxPoser: Composable 3D Value Maps for Robotic Manipulation with Language Models](https://arxiv.org/abs/2307.05973) | 2023 | CoRL | G | code | ×1 | none | manip/sim+real | – |
| **SUDD** | [Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition](https://arxiv.org/abs/2307.14535) | 2023 | CoRL | G | skill-call | ×1 | E | manip/sim | Designer |
| **ECoT** | [Robotic Control via Embodied Chain-of-Thought Reasoning](https://arxiv.org/abs/2407.08693) | 2024 | CoRL | I | trace | ×1 | none | manip/real | – |
| **π0.5** | [$π_{0.5}$: a Vision-Language-Action Model with Open-World Generalization](https://arxiv.org/abs/2504.16054) | 2025 | arXiv | I | skill-call | ×1 | none | mobile-manip/real | – |

## Benchmarks and resources

| Name | Paper | Year | Venue | Evaluated seat | Body |
|---|---|---|---|---|---|

---

Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.
