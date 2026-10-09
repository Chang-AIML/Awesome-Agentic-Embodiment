# Awesome Agentic Embodiment

> *Agentic Embodiment studies general-purpose foundation models — LLMs and VLMs, not embodied action models — used as-is, acting as agents that make explicit decisions and are connected to a robot body — through the policy, code or plans they produce, or by acting on the environment directly. Its organizing question is when and where such an agent acts on the robot: **before execution** — designing its learning problem, teaching it, or developing its system — or **at runtime** — controlling it or supervising it (**Seat**).*

**Thesis (draft, under revision).** *Agency spreads around the body: general models, not embodied action models, fill seat after seat.*

Each seat is traced from its **66 pioneers (2022–2025)** to **79 papers from 2026**, the year most of the field's papers appeared; VLN / embodied navigation (11 from 2026) and multi-agent systems (7 from 2026) have their own chapters and the Real2Sim / Sim2Real sub-direction a short section (8), plus **20 benchmarks and resources**. Definition and inclusion rules: [docs/definition.md](docs/definition.md); the judged list with evidence: [docs/paper_list.md](docs/paper_list.md) (both in Chinese).

## Scope and what counts as an agent

**Scope.** General-purpose foundation models (LLMs / VLMs such as GPT, Gemini, Claude, Qwen-VL, GPT-6 Astra) doing embodied work as agents. They may plan, call skills, tools or VLAs, write code or constraints, or emit actions directly (LLM-as-policy, e.g. GPT-6 Astra evaluated as a robot policy on RoboDojo). The agent must be a general model used as-is: a model the authors trained or fine-tuned does not count; trained VLAs, skills and perception models appear only as tools the agent calls, and a general agent's own experience may be distilled into a smaller model (e.g. GUAVA). **Embodied foundation models that produce actions are not included** — VLAs (also with reasoning, memory or self-correction), hierarchical VLAs, world action models, robot foundation models (π0.5, ECoT, OneTwoVLA, Hi Robot, Gemini Robotics, PaLM-E); they appear here only as tools called by an agent.

**Inclusion** (every paper judged from its full text): (1) a **general model used as-is** is the agent and plays a real role — models the authors trained, fine-tuned or distilled do not count; (2) the agent is **connected** to the policy / code layer or to the environment — closing the loop is recorded, not required (*Loop* = re-decide, authored, or none); (3) at a glance the paper is **about the agent** — datasets, data-generation platforms and asset pipelines with an LLM inside are not included, benchmarks of general agents are listed as resources; (4) general models, not embodied foundation models.

Environments: real robots, physics simulators and discrete embodied simulators (ALFRED, VirtualHome, R2R navigation graphs) count; pure text worlds and autonomous driving do not. Also not included: scalar reward/value models, one-shot annotators, world-model foresight, purely digital agents.

## Seat by period

| Phase | Seat | Pioneers 2022–2025 | 2026 |
|---|---|---|---|
| pre-execution | Designer | 10 | 10 |
| pre-execution | Teacher | 3 | 6 |
| pre-execution | Developer | 4 | 20 |
| runtime | Controller | 43 | 37 |
| runtime | Supervisor | 6 | 6 |

Counts include the papers of the Real2Sim / Sim2Real, VLN and multi-agent chapters under their seats.

**Legend.** *Carrier* — **G** general model used as-is (models the authors fine-tuned are no longer included). *Topology* — ×1 single agent, ×R role agents on one task, ×N one agent per robot, 1:N one decider for many robots, ×O agents owning branches of a campaign. *Loop* — **re-decide**: the model is called again with its own decisions and their consequences; **authored**: constraints or a program written by the model read live perception and adapt while the robot acts (e.g. ReKep re-solves its keypoint constraints and backtracks when one breaks); **none**: written once (open loop, included). *Closure* — evidence the loop uses: E execution, H human.

## Contents

- [Pre-execution](#pre-execution)
  - [Designer](#designer)
  - [Teacher](#teacher)
  - [Developer](#developer)
- [Runtime](#runtime)
  - [Controller · Orchestrators](#controller--orchestrators)
  - [Controller · Direct drivers](#controller--direct-drivers)
  - [Controller · Lifelong / memory agents](#controller--lifelong--memory-agents)
  - [Supervisor](#supervisor)
- [Sub-direction: Real2Sim / Sim2Real](#sub-direction-real2sim--sim2real)
- [VLN and embodied navigation](#vln-and-embodied-navigation)
- [Multi-agent systems](#multi-agent-systems)
- [Benchmarks and resources](#benchmarks-and-resources)
- [More 2026 papers (436)](#more-2026-papers)
- [More papers from 2022–2025 (610)](#more-papers-from-20222025)

## Pre-execution

The agent's output is produced before the robot executes the task and is frozen into the deployed system.

### Designer

Designs the learning problem: environments and scenes, simulation, rewards, tasks, curricula.

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
| **EmbodiedSmith** | [EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation](https://arxiv.org/abs/2610.07969) | 2026 | arXiv | G | problem-spec | ×R | re-decide | E | manip/sim | – |

### Teacher

Executes the task itself; its verified demonstrations or experience become training targets for a policy or a smaller model.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **SUDD** | [Scaling Up and Distilling Down: Language-Guided Robot Skill Acquisition](https://arxiv.org/abs/2307.14535) [[project]](https://www.cs.columbia.edu/~huy/scalingup/) | 2023 | CoRL | G | skill-call | ×1 | authored | E | manip/sim | Designer |
| **RobotGPT** | [RobotGPT: Robot Manipulation Learning from ChatGPT](https://arxiv.org/abs/2312.01421) | 2023 | RA-L | G | code | ×1 | re-decide | E | manip/sim+real | – |
| **Manipulate-Anything** | [Manipulate-Anything: Automating Real-World Robots using Vision-Language Models](https://arxiv.org/abs/2406.18915) [[project]](https://robot-ma.github.io/) | 2024 | CoRL | G | skill-call | ×1 | re-decide | E | manip/sim+real | Controller |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **GUAVA** | [Guava: Distilling Frontier VLMs into a Compact Agent through a Robotic Manipulation Harness](https://arxiv.org/abs/2606.18363) | 2026 | arXiv | G | trace | ×1 | re-decide | E | manip/sim+real | Controller |
| **EmbodiedSWE** | [EmbodiedSWE: Coding Agents for Long Horizon Dexterous Robotics](https://arxiv.org/abs/2609.27308) | 2026 | arXiv | G | trace | ×1 | re-decide | E | manip/sim+real | Controller |
| **CAPEX** | [CAPEX: Efficiently Distilling Foundation Model Behavior into Deployable Robot Policies through Experience-Adaptive Reasoning](https://arxiv.org/abs/2609.33007) | 2026 | arXiv | G | trace | ×1 | re-decide | E | manip/sim+real | – |
| **SkillWeaver** | [SkillWeaver: Agentic Exploration over Neural Interaction Skills for Scalable Robot Data Generation](https://arxiv.org/abs/2609.36171) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | manip/sim | – |
| **Frontier Demo Generation** | [Bridging Frontier Reasoning and Robot Execution: From Autonomous Demonstration Generation to Dense Language Supervision](https://arxiv.org/abs/2610.03615) | 2026 | arXiv | G | trace | ×1 | re-decide | E | manip/sim+real | Controller |

### Developer

Modifies the system itself: training code, skill libraries, harnesses, planning domains, hardware and tools; keeps or reverts by its own trials.

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
| **EmboCoach-Bench** | [From Digital to Physical: Digital Agents as Autonomous Coaches for Physical Intelligence](https://arxiv.org/abs/2601.21570) | 2026 | arXiv | - | system-edit | ×1 | re-decide | E | manip/sim | Designer |
| **HARBOR** | [HARBOR: A Harness Framework for Agentic Robot Reinforcement Learning](https://arxiv.org/abs/2606.08610) | 2026 | arXiv | G | system-edit | ×R | re-decide | E | manip/sim | Designer |
| **RHO** | [RHO: Your Coding Agent is Secretly a Roboticist](https://arxiv.org/abs/2606.16458) [[project]](https://rho-robotics.github.io) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim | – |
| **RATs (Playful)** | [Playful Agentic Robot Learning](https://arxiv.org/abs/2606.19419) [[project]](https://playful-rats.github.io/) | 2026 | arXiv | G | system-edit | ×R | re-decide | E | manip/sim+real | Controller |
| **SPINE** | [SPINE: Bridging the Cyber-Physical Gap with Agentic AI](https://arxiv.org/abs/2607.13049) | 2026 | arXiv | G | system-edit | ×R | re-decide | E+H | manip/real | – |
| **ASPIRE** | [ASPIRE: Agentic /Skills Discovery for Robotics](https://arxiv.org/abs/2607.00272) [[project]](https://research.nvidia.com/labs/gear/aspire/) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim+real | Controller |
| **Skill-Harness Evolution** | [Self-Evolving Embodied Agents via Skill-Harness Evolution](https://arxiv.org/abs/2608.11350) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim | Controller |
| **Zetta** | [Zetta $ζ$: An Efficient Closed-Loop Embodied Harness for Self-Evolving Physical Intelligence](https://arxiv.org/abs/2608.16590) | 2026 | arXiv | G | system-edit | ×1 | re-decide | E | manip/sim | Developer |
| **Continuum Robot Design** | [Bridging Language and Physics: Automated Design of Continuum Robots with Large Language Models](https://arxiv.org/abs/2609.08220) | 2026 | Robotics | G | system-edit | ×R | re-decide | E+H | other/sim | – |
| **RHD** | [Recursive Harness Distillation across Agents for Robot Manipulation](https://arxiv.org/abs/2609.33378) | 2026 | arXiv | G | trace | ×R | re-decide | E | manip/sim+real | Controller |
| **AGRO-SUVIDE** | [AGRO-SUVIDE: Agentic Robotics for Surgical Viscoelastic Debridement](https://arxiv.org/abs/2609.34823) | 2026 | arXiv | G | skill-call | ×1 | authored | E | manip/real | Developer |
| **PhysEvo** | [PhysEvo: Astra Can Act, Let It](https://arxiv.org/abs/2610.08995) | 2026 | arXiv | G | system-edit | ×R | re-decide | E | manip/sim+real | Controller |

## Runtime

The agent acts while the robot executes the task.

### Controller · Orchestrators

Decides at each step by planning and calling skills, tools or VLAs-as-tools.

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
| **SayPlan** | [SayPlan: Grounding Large Language Models using 3D Scene Graphs for Scalable Robot Task Planning](https://arxiv.org/abs/2307.06135) [[project]](https://sayplan.github.io) | 2023 | CoRL | G | skill-call | ×1 | re-decide | E | mobile-manip/sim+real | – |
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
| **SpaceMind** | [SpaceMind: A Modular and Self-Evolving Embodied Vision-Language Agent Framework for Autonomous On-orbit Servicing](https://arxiv.org/abs/2604.14399) [[code]](https://github.com/wuaodi/SpaceMind) | 2026 | Acta Astronautica | G | skill-call | ×1 | re-decide | E | other/sim+real | – |
| **Orchestration Study** | [What Matters in Orchestrating Robot Policies: A Systematic Study of Hierarchical VLA Agents](https://arxiv.org/abs/2606.10267) | 2026 | arXiv | - | vla-call | ×1 | - | E | manip/sim+real | – |
| **AerialClaw** | [AerialClaw: An Open-Source Framework for LLM-Driven Autonomous Aerial Agents](https://arxiv.org/abs/2606.12142) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | aerial/sim | – |
| **Physical Agency** | [Addressing the Orchestration Gap in Generalist Robots via Physical Agency](https://arxiv.org/abs/2607.21725) | 2026 | arXiv | G | vla-call | ×1 | re-decide | E | manip/sim+real | – |
| **Thea** | [Towards the Harness of Embodied Agents](https://arxiv.org/abs/2608.11246) [[project]](https://eit-hai.github.io/thea) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | mobile-manip/real | Supervisor |
| **Astra Robot Agents** | [Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens](https://arxiv.org/abs/2610.01939) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim | – |

### Controller · Direct drivers

Writes the code, constraints or rewards executed now, or emits the actions itself.

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
| **Embodiment Meets Environment** | [Embodiment Meets Environment: Toward Context-Aware, Safe Physical Caregiving Robots](https://arxiv.org/abs/2606.28592) | 2026 | Robotics | G | constraint | ×1 | authored | E | manip/sim+real | – |
| **VIA** | [VIA: Visual Interface Agent for Robot Control](https://arxiv.org/abs/2607.11119) | 2026 | arXiv | G | micro-action | ×1 | re-decide | E | manip/sim+real | – |
| **GTA-2** | [GTA-2: A Multi-VLM Framework for Synthesizing Robot Manipulation Skills via Grounded Task Axes](https://arxiv.org/abs/2609.09808) | 2026 | arXiv | G | constraint | ×R | none | none | manip/real | – |
| **Show-Harness** | [Show-Harness: Just a VLM Agent Can Play Robots](https://arxiv.org/abs/2609.10522) [[project]](https://showlab.github.io/Show-Harness) | 2026 | arXiv | G | micro-action | ×1 | re-decide | E | manip/sim+real | – |
| **Agent as Policy** | [Agent as Policy for Robotic Manipulation](https://arxiv.org/abs/2609.12541) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/real | – |
| **AquaCap** | [AquaCap: A Training-Free Underwater Embodied Agent with Code-as-Policy](https://arxiv.org/abs/2609.23133) | 2026 | arXiv | G | code | ×1 | re-decide | E | other/sim+real | – |
| **KPI** | [KPI: A Promptable Kernel for Physical Interaction on Humanoids](https://arxiv.org/abs/2609.36151) [[project]](https://kpi-robot.github.io/) | 2026 | arXiv | G | constraint | ×1 | authored | E | humanoid/sim+real | – |
| **OpenRUA** | [OpenRUA: Robot-Use Agents Are Zero-Shot Visuomotor Policies](https://arxiv.org/abs/2610.02459) | 2026 | arXiv | G | code | ×1 | re-decide | E | manip/sim+real | – |

### Controller · Lifelong / memory agents

Improves memory, skill libraries or harness across episodes while acting.

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

### Supervisor

Acts only on anomalies: failure detection, safety guardrails, recovery, asking for help.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **REFLECT** | [REFLECT: Summarizing Robot Experiences for Failure Explanation and Correction](https://arxiv.org/abs/2306.15724) [[project]](https://robot-reflect.github.io/) | 2023 | CoRL | G | verdict | ×1 | re-decide | E | manip/sim+real | Controller |
| **DoReMi** | [DoReMi: Grounding Language Model by Detecting and Recovering from Plan-Execution Misalignment](https://arxiv.org/abs/2307.00329) | 2023 | IROS | G | verdict | ×R | re-decide | E | manip/sim+real | Controller |
| **Safety Chip** | [Plug in the Safety Chip: Enforcing Constraints for LLM-driven Robot Agents](https://arxiv.org/abs/2309.09919) | 2023 | ICRA | G | constraint | ×1 | authored | E | mobile-manip/sim+real | – |
| **Real-Time Anomaly Detection** | [Real-Time Anomaly Detection and Reactive Planning with Large Language Models](https://arxiv.org/abs/2407.08735) | 2024 | RSS | G | verdict | ×1 | none | none | aerial/sim+real | – |
| **Code-as-Monitor** | [Code-as-Monitor: Constraint-aware Visual Programming for Reactive and Proactive Robotic Failure Detection](https://arxiv.org/abs/2412.04455) [[project]](https://zhoues.github.io/Code-as-Monitor/) | 2024 | CVPR | G | verdict | ×1 | re-decide | E | manip/sim+real | Controller |
| **RoboGuard** | [Safety Guardrails for LLM-Enabled Robots](https://arxiv.org/abs/2503.07885) | 2025 | RA-L | G | constraint | ×1 | authored | E | nav/sim+real | – |

**2026**

| Name | Paper | Year | Venue | Carrier | Interface | Topo | Loop | Closure | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|---|
| **Contextual Safety Reasoning** | [Contextual Safety Reasoning and Grounding for Open-World Robots](https://arxiv.org/abs/2602.19983) | 2026 | arXiv | G | constraint | ×1 | authored | E | nav/sim+real | – |
| **When to Act, Ask, or Learn** | [When to Act, Ask, or Learn: Uncertainty-Aware Policy Steering](https://arxiv.org/abs/2602.22474) | 2026 | Robotics | G | verdict | ×1 | re-decide | E+H | manip/sim+real | Controller |
| **Agentic Task Graph** | [From Reaction to Anticipation: Proactive Failure Recovery through Agentic Task Graph for Robotic Manipulation](https://arxiv.org/abs/2605.11951) | 2026 | Robotics | G | code | ×R | authored | E | manip/sim+real | Controller |
| **UAV Selective Recovery** | [Selective Agentic Recovery for UAV Autonomy with a Persistent Mission Runtime](https://arxiv.org/abs/2606.14219) | 2026 | arXiv | G | skill-call | ×1 | re-decide | E | aerial/sim+real | – |
| **FRAMES** | [FRAMES: Failure Recovery And Monitoring of Embodied Skills for Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.22538) | 2026 | arXiv | G | verdict | ×R | re-decide | E | humanoid/sim+real | Controller |
| **Beyond Human Demos** | [Learning Beyond What Humans Can Demonstrate](https://arxiv.org/abs/2609.24996) [[project]](http://guardrail-policy.github.io/) | 2026 | arXiv | G | constraint | ×1 | authored | E | manip/sim | Developer |

## Sub-direction: Real2Sim / Sim2Real

One sub-direction that cuts across Designer and Developer: agents that build or calibrate simulators from the real world (Real2Sim), transfer what they learned in simulation to the real robot (Sim2Real), or practise in a reconstructed simulator and go back to the real one (Real2Sim2Real). Only representative papers are listed here; further ones are in *More 2026 papers*.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **DrEureka** | [DrEureka: Language Model Guided Sim-To-Real Transfer](https://arxiv.org/abs/2406.01967) [[project]](https://eureka-research.github.io/dr-eureka/) | 2024 | RSS | Designer | G | problem-spec | re-decide | loco/sim+real | – |
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
| **HaltNav** | [HaltNav: Reactive Visual Halting over Lightweight Topological Priors for Robust Vision-Language Navigation](https://arxiv.org/abs/2603.12696) | 2026 | arXiv | Controller | G | skill-call | re-decide | nav/sim+real | Supervisor |
| **NORM-Nav** | [NORM-Nav: Zero-Shot Mobile Robot Navigation with Natural Language Behavioral Constraints](https://arxiv.org/abs/2605.16979) | 2026 | ICRA | Controller | G | constraint | authored | nav/sim+real | – |
| **AgenticNav** | [AgenticNav: Zero-Shot Vision-and-Language Navigation as a Tool-Calling Harness](https://arxiv.org/abs/2606.10577) | 2026 | arXiv | Controller | G | skill-call | re-decide | nav/sim | – |
| **LocalNav** | [LocalNav: Distilling Frontier VLMs and Embodied RL for On-Device Object Goal Navigation](https://arxiv.org/abs/2606.27871) | 2026 | arXiv | Teacher | G | skill-call | re-decide | nav/sim | Controller |
| **Embodied Agents Take Control** | [Embodied Agents Take Control: Minimal-Interface Zero-Shot Agents Rival Industrial-Scale Policies in Vision-and-Language Navigation](https://arxiv.org/abs/2607.26148) | 2026 | arXiv | Controller | G | micro-action | re-decide | nav/sim | – |
| **HAM-VLN** | [HAM-VLN: Harnessing Hierarchical Agentic Memory for Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2607.29600) | 2026 | arXiv | Controller | G | micro-action | re-decide | nav/sim | – |
| **Air-Ground VLN** | [Air-Ground Collaborative Vision-and-Language Navigation via Shared Bird's-Eye Maps](https://arxiv.org/abs/2609.03483) | 2026 | arXiv | Controller | G | skill-call | re-decide | multi-robot/sim | – |
| **HarnessVLN** | [HarnessVLN: Unifying Training-Free Embodied Navigation through an Agent Harness](https://arxiv.org/abs/2609.15195) | 2026 | arXiv | Controller | G | skill-call | re-decide | nav/sim | – |
| **ASENA** | [ASENA: Self-evolving Agents for Embodied Navigation](https://arxiv.org/abs/2609.39207) [[project]](https://asena-bot.github.io) | 2026 | arXiv | Controller | G | code | re-decide | nav/sim | Developer |

## Multi-agent systems

Systems where multiple agents are the point: general-model agents that allocate, plan or coordinate the work of two or more robots (including heterogeneous teams such as drones with ground robots), or a team of general-model agents with distinct roles that talk, debate or hand work to each other. A single robot driven by a pipeline of prompted calls is not listed here. Seats are kept; multi-agent navigation papers also appear in the VLN chapter.

**Pioneers (2022–2025)**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **RoCo** | [RoCo: Dialectic Multi-Robot Collaboration with Large Language Models](https://arxiv.org/abs/2307.04738) | 2023 | ICRA | Controller | G | skill-call | re-decide | multi-robot/sim+real | – |
| **SMART-LLM** | [SMART-LLM: Smart Multi-Agent Robot Task Planning using Large Language Models](https://arxiv.org/abs/2309.10062) | 2023 | IROS | Controller | G | code | none | multi-robot/sim+real | – |
| **AutoRT** | [AutoRT: Embodied Foundation Models for Large Scale Orchestration of Robotic Agents](https://arxiv.org/abs/2401.12963) | 2024 | arXiv | Controller | G | problem-spec | none | multi-robot/real | Supervisor |

**2026**

| Name | Paper | Year | Venue | Seat | Carrier | Interface | Loop | Body | Other seats |
|---|---|---|---|---|---|---|---|---|---|
| **ABot-Claw** | [ABot-Claw: A Foundation for Persistent, Cooperative, and Self-Evolving Robotic Agents](https://arxiv.org/abs/2604.10096) | 2026 | arXiv | Controller | G | skill-call | re-decide | multi-robot/real | Supervisor |
| **ENPIRE** | [ENPIRE: Agentic Robot Policy Self-Improvement in the Real World](https://arxiv.org/abs/2606.19980) | 2026 | arXiv | Developer | G | system-edit | re-decide | manip/real | – |
| **Air-Ground VLN** | [Air-Ground Collaborative Vision-and-Language Navigation via Shared Bird's-Eye Maps](https://arxiv.org/abs/2609.03483) | 2026 | arXiv | Controller | G | skill-call | re-decide | multi-robot/sim | – |
| **AdaHVLA** | [AdaHVLA: Adaptive Harnesses for Long-Horizon Vision-Language-Action Execution](https://arxiv.org/abs/2609.29204) | 2026 | arXiv | Developer | G | system-edit | re-decide | manip/sim+real | Controller |
| **Skill2Real** | [Skill2Real: Agentic Skill Learning for Zero-Shot Sim-to-Real Robot Manipulation](https://arxiv.org/abs/2610.02788) | 2026 | arXiv | Developer | G | system-edit | re-decide | manip/sim+real | Controller |
| **ROOT** | [ROOT: Discovering Rewards for User-Specified Embodied Behaviors](https://arxiv.org/abs/2610.04250) | 2026 | arXiv | Designer | G | problem-spec | re-decide | loco/sim | – |
| **LACE-CRAFT** | [LACE-CRAFT: Robot Co-Design with Actor Inheritance and Blackboard Collaboration](https://arxiv.org/abs/2610.09283) [[project]](https://deemostech.github.io/lace-craft/) | 2026 | arXiv | Developer | G | system-edit | re-decide | loco/sim+real | Designer |

Multi-agent benchmarks (listed under *Benchmarks and resources*): **PARTNR**.

<details><summary><b>More multi-agent papers</b> (200)</summary>

| Paper | Year | Seat · role |
|---|---|---|
| [Building Cooperative Embodied Agents Modularly with Large Language Models](https://arxiv.org/abs/2307.02485) | 2023 | Controller · Orchestration |
| [CoPAL: Corrective Planning of Robot Actions with Large Language Models](https://arxiv.org/abs/2310.07263) | 2023 | Controller · Orchestration |
| [Discuss Before Moving: Visual Language Navigation via Multi-expert Discussions](https://arxiv.org/abs/2309.11382) | 2023 | Controller · Direct action |
| [From text to motion: grounding GPT-4 in a humanoid robot “Alter3”](https://arxiv.org/abs/2312.06571) | 2023 | Controller · Direct action |
| [Scalable Multi-Robot Collaboration with Large Language Models: Centralized or Decentralized Systems?](https://arxiv.org/abs/2309.15943) | 2023 | Controller · Orchestration |
| [A Prompt-Driven Task Planning Method for Multi-Drones Based on Large Language Model](https://arxiv.org/abs/2406.00006) | 2024 | Controller · Orchestration |
| [AI-Gadget Kit: Integrating Swarm User Interfaces with LLM-driven Agents for Rich Tabletop Game Applications](https://arxiv.org/abs/2407.17086) | 2024 | Controller · Direct action |
| [Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model](https://arxiv.org/abs/2410.13882) | 2024 | Designer · Environments / reconstruction |
| [AssistantX: An LLM-Powered Proactive Assistant in Collaborative Human-Populated Environments](https://arxiv.org/abs/2409.17655) | 2024 | Controller · Orchestration |
| [Automatic Robotic Development through Collaborative Framework by Large Language Models](https://arxiv.org/abs/2402.03699) | 2024 | Developer · System / code |
| [Bi-VLA: Vision-Language-Action Model-Based System for Bimanual Robotic Dexterous Manipulations](https://arxiv.org/abs/2405.06039) | 2024 | Controller · Orchestration |
| [CAMON: Cooperative Agents for Multi-Object Navigation with LLM-based Conversations](https://arxiv.org/abs/2407.00632) | 2024 | Controller · Orchestration |
| [CaPo: Cooperative Plan Optimization for Efficient Embodied Multi-Agent Cooperation](https://arxiv.org/abs/2411.04679) | 2024 | Controller · Orchestration |
| [COHERENT: Collaboration of Heterogeneous Multi-Robot System with Large Language Models](https://arxiv.org/abs/2409.15146) | 2024 | Controller · Orchestration |
| [Conversational Language Models for Human-in-the-Loop Multi-Robot Coordination](https://arxiv.org/abs/2402.19166) | 2024 | Controller · Orchestration |
| [DART-LLM: Dependency-Aware Multi-Robot Task Decomposition and Execution using Large Language Models](https://arxiv.org/abs/2411.09022) | 2024 | Controller · Orchestration |
| [Embodied LLM Agents Learn to Cooperate in Organized Teams](https://arxiv.org/abs/2403.12482) | 2024 | Controller · Direct action |
| [EMOS: Embodiment-aware Heterogeneous Multi-robot Operating System with LLM Agents](https://arxiv.org/abs/2410.22662) | 2024 | Controller · Orchestration |
| [EMPOWER: Embodied Multi-role Open-vocabulary Planning with Online Grounding and Execution](https://arxiv.org/abs/2408.17379) | 2024 | Controller · Orchestration |
| [FlockGPT: Guiding UAV Flocking with Linguistic Orchestration](https://arxiv.org/abs/2405.05872) | 2024 | Controller · Policy writing |
| [Foundation Models to the Rescue: Deadlock Resolution in Connected Multi-Robot Systems](https://arxiv.org/abs/2404.06413) | 2024 | Supervisor · Monitoring / recovery |
| [GameVLM: A Decision-making Framework for Robotic Task Planning Based on Visual Language Models and Zero-sum Games](https://arxiv.org/abs/2405.13751) | 2024 | Controller · Orchestration |
| [GRAPPA: Generalizing and Adapting Robot Policies via Online Agentic Guidance](https://arxiv.org/abs/2410.06473) | 2024 | Controller · Policy writing |
| [Grounding LLMs For Robot Task Planning Using Closed-loop State Feedback](https://arxiv.org/abs/2402.08546) | 2024 | Controller · Orchestration |
| [Hazards in Daily Life? Enabling Robots to Proactively Detect and Resolve Anomalies](https://arxiv.org/abs/2411.00781) | 2024 | Designer · Environments / reconstruction |
| [Hierarchical Large Language Models in Cloud-Edge-End Architecture for Heterogeneous Robot Cluster Control](https://arxiv.org/abs/2402.03703) | 2024 | Controller · Orchestration |
| [Hierarchical LLMs in-the-Loop Optimization for Real-Time Multi-Robot Target Tracking Under Unknown Hazards](https://arxiv.org/abs/2409.12274) | 2024 | Controller · Orchestration |
| [Industry 6.0: New Generation of Industry driven by Generative AI and Swarm of Heterogeneous Robots](https://arxiv.org/abs/2409.10106) | 2024 | Controller · Orchestration |
| [LaMMA-P: Generalizable Multi-Agent Long-Horizon Task Allocation and Planning with LM-Driven PDDL Planner](https://arxiv.org/abs/2409.20560) | 2024 | Controller · Orchestration |
| [Leveraging Large Language Model for Heterogeneous Ad Hoc Teamwork Collaboration](https://arxiv.org/abs/2406.12224) | 2024 | Controller · Orchestration |
| [LiP-LLM: Integrating Linear Programming and Dependency Graph With Large Language Models for Multi-Robot Task Planning](https://arxiv.org/abs/2410.21040) | 2024 | Controller · Orchestration |
| [LLCoach: Generating Robot Soccer Plans using Multi-Role Large Language Models](https://arxiv.org/abs/2406.18285) | 2024 | Controller · Orchestration |
| [LLM-Based Cooperative Agents using Information Relevance and Plan Validation](https://arxiv.org/abs/2405.16751) | 2024 | Controller · Orchestration |
| [LLM2Swarm: Robot Swarms that Responsively Reason, Plan, and Collaborate through LLMs](https://arxiv.org/abs/2410.11387) | 2024 | Controller · Orchestration |
| [Long-horizon Locomotion and Manipulation on a Quadrupedal Robot with Large Language Models](https://arxiv.org/abs/2404.05291) | 2024 | Controller · Orchestration |
| [Long-Horizon Planning for Multi-Agent Robots in Partially Observable Environments](https://arxiv.org/abs/2407.10031) | 2024 | Controller · Orchestration |
| [MALMM: Multi-Agent Large Language Models for Zero-Shot Robotic Manipulation](https://arxiv.org/abs/2411.17636) | 2024 | Controller · Policy writing |
| [MARLIN: Multi-Agent Reinforcement Learning Guided by Language-Based Inter-Robot Negotiation](https://arxiv.org/abs/2410.14383) | 2024 | Teacher · Demonstration / distillation |
| [MHRC: Closed-loop Decentralized Multi-Heterogeneous Robot Collaboration with Large Language Models](https://arxiv.org/abs/2409.16030) | 2024 | Controller · Orchestration |
| [MOSAIC: Modular Foundation Models for Assistive and Interactive Cooking](https://arxiv.org/abs/2402.18796) | 2024 | Controller · Orchestration |
| [MultiTalk: Introspective and Extrospective Dialogue for Human-Environment-LLM Alignment](https://arxiv.org/abs/2409.16455) | 2024 | Controller · Orchestration |
| [Probabilistically Correct Language-Based Multi-Robot Planning Using Conformal Prediction](https://arxiv.org/abs/2402.15368) | 2024 | Controller · Orchestration |
| [REBEL: Rule-based and Experience-enhanced Learning with LLMs for Initial Task Allocation in Multi-Human Multi-Robot Teaming](https://arxiv.org/abs/2409.16266) | 2024 | Controller · Orchestration |
| [SDS - See it, Do it, Sorted: Quadruped Skill Synthesis from Single Video Demonstration](https://arxiv.org/abs/2410.11571) | 2024 | Designer · Rewards / tasks |
| [SwarmGPT: Combining Large Language Models With Safe Motion Planning for Drone Swarm Choreography](https://arxiv.org/abs/2412.08428) | 2024 | Controller · Orchestration |
| [Toward Automated Programming for Robotic Assembly Using ChatGPT](https://arxiv.org/abs/2405.08216) | 2024 | Controller · Policy writing |
| [Towards Efficient LLM Grounding for Embodied Multi-Agent Collaboration](https://arxiv.org/abs/2405.14314) | 2024 | Controller · Orchestration |
| [VADER: Visual Affordance Detection and Error Recovery for Multi Robot Human Collaboration](https://arxiv.org/abs/2405.16021) | 2024 | Controller · Orchestration |
| [Validation of the Scientific Literature via Chemputation Augmented by Large Language Models](https://arxiv.org/abs/2410.06384) | 2024 | Controller · Policy writing |
| [We Choose to Go to Space: Agent-driven Human and Multi-Robot Collaboration in Microgravity](https://arxiv.org/abs/2402.14299) | 2024 | Controller · Orchestration |
| [Wonderful Team: Zero-Shot Physical Task Planning with Visual LLMs](https://arxiv.org/abs/2407.19094) | 2024 | Controller · Direct action |
| [ZeroCAP: Zero-Shot Multi-Robot Context Aware Pattern Formation via Large Language Models](https://arxiv.org/abs/2404.02318) | 2024 | Controller · Orchestration |
| [A Hierarchical Agentic Framework for Autonomous Drone-Based Visual Inspection](https://arxiv.org/abs/2510.00259) | 2025 | Controller · Orchestration |
| [Adaptive Domain Modeling with Language Models: A Multi-Agent Approach to Task Planning](https://arxiv.org/abs/2506.19592) | 2025 | Controller · Orchestration |
| [Air-Ground Collaboration for Language-Specified Missions in Unknown Environments](https://arxiv.org/abs/2505.09108) | 2025 | Controller · Orchestration |
| [AquaChat++: LLM-Assisted Multi-ROV Inspection for Aquaculture Net Pens with Integrated Battery Management and Thruster Fault Tolerance](https://arxiv.org/abs/2508.06554) | 2025 | Controller · Orchestration |
| [AURA: Autonomous Upskilling with Retrieval-Augmented Agents](https://arxiv.org/abs/2506.02507) | 2025 | Designer · Rewards / tasks |
| [AutoMisty: A Multi-Agent LLM Framework for Automated Code Generation in the Misty Social Robot](https://arxiv.org/abs/2503.06791) | 2025 | Controller · Policy writing |
| [BioMARS: A Multi-Agent Robotic System for Autonomous Biological Experiments](https://arxiv.org/abs/2507.01485) | 2025 | Controller · Orchestration |
| [CGoT: A Novel Inference Mechanism for Embodied Multi-Agent Systems Using Composable Graphs of Thoughts](https://arxiv.org/abs/2510.22235) | 2025 | Controller · Orchestration |
| [Chat with UAV – human-UAV interaction based on large language models](https://arxiv.org/abs/2512.08145) | 2025 | Controller · Orchestration |
| [CLEA: Closed-Loop Embodied Agent for Enhancing Task Execution in Dynamic Environments](https://arxiv.org/abs/2503.00729) | 2025 | Controller · Orchestration |
| [Code-as-Symbolic-Planner: Foundation Model-Based Robot Planning via Symbolic Code Generation](https://arxiv.org/abs/2503.01700) | 2025 | Controller · Policy writing |
| [Compositional Coordination for Multi-Robot Teams with Large Language Models](https://arxiv.org/abs/2507.16068) | 2025 | Controller · Policy writing |
| [CRAFT: Coaching Reinforcement Learning Autonomously using Foundation Models for Multi-Robot Coordination Tasks](https://arxiv.org/abs/2509.14380) | 2025 | Designer · Rewards / tasks |
| [Debate2Create: Robot Co-design via Multi-Agent LLM Debate](https://arxiv.org/abs/2510.25850) | 2025 | Developer · Embodiment / tools |
| [DEXTER-LLM: Dynamic and Explainable Coordination of Multi-Robot Systems in Unknown Environments via Large Language Models](https://arxiv.org/abs/2508.14387) | 2025 | Controller · Orchestration |
| [Distributed AI Agents for Cognitive Underwater Robot Autonomy](https://arxiv.org/abs/2507.23735) | 2025 | Controller · Orchestration |
| [Dynamic Task Adaptation for Multi-Robot Manufacturing Systems with Large Language Models](https://arxiv.org/abs/2505.22804) | 2025 | Supervisor · Monitoring / recovery |
| [E-SDS: Environment-aware See it, Do it, Sorted - Automated Environment-Aware Reinforcement Learning for Humanoid Locomotion](https://arxiv.org/abs/2512.16446) | 2025 | Designer · Rewards / tasks |
| [ELHPlan: Efficient Long-Horizon Task Planning for Multi-Agent Collaboration](https://arxiv.org/abs/2509.24230) | 2025 | Controller · Orchestration |
| [Enhancing Multi-Agent Systems via Reinforcement Learning with LLM-Based Planner and Graph-Based Policy](https://arxiv.org/abs/2503.10049) | 2025 | Controller · Orchestration |
| [FLEET: Formal Language-Grounded Scheduling for Heterogeneous Robot Teams](https://arxiv.org/abs/2510.07417) | 2025 | Controller · Orchestration |
| [GameChat: Multi-LLM Dialogue for Safe, Agile, and Socially Optimal Multi-Agent Navigation in Constrained Environments](https://arxiv.org/abs/2503.12333) | 2025 | Controller · Orchestration |
| [GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models](https://arxiv.org/abs/2503.23875) | 2025 | Controller · Policy writing |
| [GestOS: Advanced Hand Gesture Interpretation via Large Language Models to control Any Type of Robot](https://arxiv.org/abs/2509.14412) | 2025 | Controller · Orchestration |
| [HELP: Hierarchical Embodied Language Planner for Household Tasks](https://arxiv.org/abs/2512.21723) | 2025 | Controller · Orchestration |
| [Heterogeneous Robot Collaboration in Unstructured Environments with Grounded Generative Intelligence](https://arxiv.org/abs/2510.26915) | 2025 | Controller · Orchestration |
| [Hierarchical Language Models for Semantic Navigation and Manipulation in an Aerial‐Ground Robotic System](https://arxiv.org/abs/2506.05020) | 2025 | Controller · Orchestration |
| [Integrating Retrospective Framework in Multi-Robot Collaboration](https://arxiv.org/abs/2502.11227) | 2025 | Controller · Orchestration |
| [Intent-Driven LLM Ensemble Planning for Flexible Multi-Robot Disassembly: Demonstration on EV Batteries](https://arxiv.org/abs/2510.17576) | 2025 | Controller · Orchestration |
| [LA-RCS: LLM-Agent-Based Robot Control System](https://arxiv.org/abs/2505.18214) | 2025 | Controller · Direct action |
| [LAMARL: LLM-Aided Multi-Agent Reinforcement Learning for Cooperative Policy Generation](https://arxiv.org/abs/2506.01538) | 2025 | Designer · Rewards / tasks |
| [Language-Grounded Hierarchical Planning and Execution with Multi-Robot 3D Scene Graphs](https://arxiv.org/abs/2506.07454) | 2025 | Controller · Orchestration |
| [Learn as Individuals, Evolve as a Team: Multi-agent LLMs Adaptation in Embodied Environments](https://arxiv.org/abs/2506.07232) | 2025 | Controller · Orchestration |
| [Learning a High-Quality Robotic Wiping Policy Using Systematic Reward Analysis and Visual-Language Model Based Curriculum](https://arxiv.org/abs/2502.12599) | 2025 | Designer · Rewards / tasks |
| [Leveraging LLMs for reward function design in reinforcement learning control tasks](https://arxiv.org/abs/2511.19355) | 2025 | Designer · Rewards / tasks |
| [LLM-Based Generalizable Hierarchical Task Planning and Execution for Heterogeneous Robot Teams with Event-Driven Replanning](https://arxiv.org/abs/2511.22354) | 2025 | Controller · Orchestration |
| [LLM-Empowered Embodied Agent for Memory-Augmented Task Planning in Household Robotics](https://arxiv.org/abs/2504.21716) | 2025 | Controller · Orchestration |
| [LLM-Flock: Decentralized Multi-Robot Flocking via Large Language Models and Influence-Based Consensus](https://arxiv.org/abs/2505.06513) | 2025 | Controller · Direct action |
| [LLM-HBT: Dynamic Behavior Tree Construction for Adaptive Coordination in Heterogeneous Robots](https://arxiv.org/abs/2510.09963) | 2025 | Controller · Orchestration |
| [MADRA: Multi-Agent Debate for Risk-Aware Embodied Planning](https://arxiv.org/abs/2511.21460) | 2025 | Supervisor · Monitoring / recovery |
| [ManiAgent: An Agentic Framework for General Robotic Manipulation](https://arxiv.org/abs/2510.11660) | 2025 | Controller · Direct action |
| [Multi-Agent LLM Actor-Critic Framework for Social Robot Navigation](https://arxiv.org/abs/2503.09758) | 2025 | Controller · Direct action |
| [Multi-robot task planning for multi-object retrieval tasks with distributed on-site knowledge via large language models](https://arxiv.org/abs/2509.12838) | 2025 | Controller · Orchestration |
| [Online automatic code generation for robot swarms: LLMs and self-organizing hierarchy](https://arxiv.org/abs/2510.04774) | 2025 | Supervisor · Monitoring / recovery |
| [PIP-LLM: Integrating PDDL-Integer Programming with LLMs for Coordinating Multi-Robot Teams Using Natural Language](https://arxiv.org/abs/2510.22784) | 2025 | Controller · Orchestration |
| [Plantbot: Integrating Plant and Robot through LLM Modular Agent Networks](https://arxiv.org/abs/2509.05338) | 2025 | Controller · Direct action |
| [RALLY: Role-Adaptive LLM-Driven Yoked Navigation for Agentic UAV Swarms](https://arxiv.org/abs/2507.01378) | 2025 | Teacher · Demonstration / distillation |
| [REFLEX: Metacognitive Reasoning for Reflective Zero-Shot Robotic Planning with Large Language Models](https://arxiv.org/abs/2505.14899) | 2025 | Controller · Orchestration |
| [REMAC: Self-Reflective and Self-Evolving Multi-Agent Collaboration for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2503.22122) | 2025 | Controller · Orchestration |
| [RobotFleet: An Open-Source Framework for Centralized Multi-Robot Task Planning](https://arxiv.org/abs/2510.10379) | 2025 | Controller · Orchestration |
| [Safety Aware Task Planning via Large Language Models in Robotics](https://arxiv.org/abs/2503.15707) | 2025 | Controller · Orchestration |
| [TACOS: Task Agnostic COordinator of a multi-drone System](https://arxiv.org/abs/2510.01869) | 2025 | Controller · Orchestration |
| [Transforming Monolithic Foundation Models into Embodied Multi-Agent Architectures for Human-Robot Collaboration](https://arxiv.org/abs/2512.00797) | 2025 | Controller · Orchestration |
| [Triple-S: A Collaborative Multi-LLM Framework for Solving Long-Horizon Implicative Tasks in Robotics](https://arxiv.org/abs/2508.07421) | 2025 | Controller · Policy writing |
| [VIRAL: Vision-grounded Integration for Reward design And Learning](https://arxiv.org/abs/2505.22092) | 2025 | Designer · Rewards / tasks |
| [A Closed-Loop Multi-Agent Framework for Robust Multi-Robot Manipulation](https://arxiv.org/abs/2607.06990) | 2026 | Controller · Orchestration |
| [A Conversational Framework for Human-Robot Collaborative Manipulation with Distributed Generative AI models](https://arxiv.org/abs/2606.06061) | 2026 | Controller · Orchestration |
| [A Glimpse into Long-term Physical Coexistence with Intelligent Robots](https://arxiv.org/abs/2607.11377) | 2026 | Controller · Orchestration |
| [A Multimodal Framework for Human-Multi-Agent Interaction](https://arxiv.org/abs/2603.23271) | 2026 | Controller · Orchestration |
| [A Schema Bounded Language Model for Refining Robot Policies Without Destabilizing Local Learning](https://arxiv.org/abs/2609.05133) | 2026 | Controller · Policy writing |
| [ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking](https://arxiv.org/abs/2602.21161) | 2026 | Controller · Direct action |
| [Aerial Agentic AI: Synergizing LLM and SLM for Low-Altitude Wireless Networks](https://arxiv.org/abs/2603.22866) | 2026 | Controller · Orchestration |
| [AeroWeaver: An Embodied-Agent Harness for Weaving Aerial Skills into Distributed, Adaptive Swarm Execution](https://arxiv.org/abs/2609.18520) | 2026 | Controller · Orchestration |
| [Agentic Neuro-Symbolic Planning and Commissioning for Human-in-the-Loop Industrial Robotics with Digital Twins](https://arxiv.org/abs/2606.08214) | 2026 | Controller · Orchestration |
| [AgenticCache: Cache-Driven Asynchronous Planning for Embodied AI Agents](https://arxiv.org/abs/2604.24039) | 2026 | Controller · Orchestration |
| [AgenticRL: Agentic Reinforcement Learning with Self-Refinement for Complex UAV Navigation](https://arxiv.org/abs/2606.03963) | 2026 | Designer · Rewards / tasks |
| [AgenticSwarm: Semantic Perception and Adaptive Task Allocation for Heterogeneous Multi-UAV Missions](https://arxiv.org/abs/2609.21716) | 2026 | Controller · Orchestration |
| [AgentRob: From Virtual Forum Agents to Hijacked Physical Robots](https://arxiv.org/abs/2602.13591) | 2026 | Controller · Orchestration |
| [ALRM: Agentic LLM for Robotic Manipulation](https://arxiv.org/abs/2601.19510) | 2026 | Controller · Orchestration |
| [An AI Scientist that Doesn't Drift: Taste, Structure, and Falsifiable Findings in a Quadruped Navigation Research Loop](https://arxiv.org/abs/2608.07542) | 2026 | Developer · System / code |
| [ARSTAG: An Agentic Real2Sim2Real System for Task-Specific Robot Data Generation](https://arxiv.org/abs/2609.24563) | 2026 | Designer · Environments / reconstruction |
| [As You Wish: Mission Planning with Formal Verification using LLMs in Precision Agriculture](https://arxiv.org/abs/2606.18519) | 2026 | Controller · Orchestration |
| [Auto-HSI: Personalized human control of a robot swarm on demand by using LLMs for online automatic code generation](https://arxiv.org/abs/2609.16346) | 2026 | Controller · Policy writing |
| [BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation](https://arxiv.org/abs/2605.07306) | 2026 | Controller · Orchestration |
| [Can a Robot Walk the Robotic Dog: Triple-Zero Collaborative Navigation for Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2603.21723) | 2026 | Controller · Orchestration |
| [CoEnv: Driving Embodied Multi-Agent Collaboration via Compositional Environment](https://arxiv.org/abs/2604.05484) | 2026 | Controller · Orchestration |
| [CommCP: Efficient Multi-Agent Coordination via LLM-Based Communication with Conformal Prediction](https://arxiv.org/abs/2602.06038) | 2026 | Controller · Orchestration |
| [Containing Behavioral Cascades from Manipulated Claims in LLM-Powered Multi-Robot Systems](https://arxiv.org/abs/2609.30523) | 2026 | Supervisor · Monitoring / recovery |
| [Coordinated Control of Multiple Construction Machines Using LLM-Generated Behavior Trees with Flag-Based Synchronization](https://arxiv.org/abs/2602.01041) | 2026 | Controller · Orchestration |
| [D-VLC: Decentralized Vision-Language Collaboration for Heterogeneous Embodied Multi-Robot Systems in Unknown Environments](https://arxiv.org/abs/2607.29009) | 2026 | Controller · Orchestration |
| [Decentralized LLM-Driven Coordination of Acoustic Robots for Contactless Object Manipulation](https://arxiv.org/abs/2605.29378) | 2026 | Controller · Orchestration |
| [DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation](https://arxiv.org/abs/2609.18620) | 2026 | Designer · Environments / reconstruction |
| [DiagGen: Agentic Generation of Deformable Assets with Sim-based Diagnostics for Robotic Simulation](https://arxiv.org/abs/2609.23103) | 2026 | Designer · Environments / reconstruction |
| [Dual-Agent Framework for Cross-Model Verified Translation of Natural-Language Protocols into Robotic Laboratory Platform](https://arxiv.org/abs/2606.20120) | 2026 | Controller · Orchestration |
| [DuoMind: Enabling Distributed Multi-Robot Coordination with Semantic Communication](https://arxiv.org/abs/2610.02161) | 2026 | Controller · Orchestration |
| [DynaHMRC: Decentralized Heterogeneous Multi-Robot Collaboration for Dynamic Tasks with Large Language Models](https://arxiv.org/abs/2606.14882) | 2026 | Controller · Orchestration |
| [EFLUX: Elastic Multi-Robot Formation Navigation and Adaptation with Agentic LLMs](https://arxiv.org/abs/2607.12050) | 2026 | Controller · Orchestration |
| [Embedding Large Language Models into Flow Controls: An Agentic Framework for Adaptive and Trustworthy Automated Cooking](https://arxiv.org/abs/2608.04768) | 2026 | Controller · Policy writing |
| [EmboTeam: Grounding LLM Reasoning into Reactive Behavior Trees via PDDL for Embodied Multi-Robot Collaboration](https://arxiv.org/abs/2601.11063) | 2026 | Controller · Orchestration |
| [EMERGE-Policy: A Robot Mind Emerges Beyond a Single Policy](https://arxiv.org/abs/2608.29896) | 2026 | Controller · Orchestration |
| [Engagement-Aware Agentic Pursuit-Evasion](https://arxiv.org/abs/2607.10986) | 2026 | Controller · Orchestration |
| [From Assumptions to Actions: Turning LLM Reasoning into Uncertainty-Aware Planning for Embodied Agents](https://arxiv.org/abs/2602.04326) | 2026 | Controller · Orchestration |
| [From Dialogue to Execution: Mixture-of-Agents Assisted Interactive Planning for Behavior Tree-Based Long-Horizon Robot Execution](https://arxiv.org/abs/2603.01113) | 2026 | Controller · Orchestration |
| [GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks](https://arxiv.org/abs/2607.05369) | 2026 | Developer · System / code |
| [GenPHRI: Agentic Generative Simulation for Physical Human-Robot Interaction](https://arxiv.org/abs/2604.08664) | 2026 | Teacher · Demonstration / distillation |
| [Global Commander and Local Operative: A Dual-Agent Framework for Scene Navigation](https://arxiv.org/abs/2602.18941) | 2026 | Controller · Direct action |
| [GuideFetch: A Task Coordination Framework for Concurrent Navigation and Object Retrieval in Assistive Robot Dogs](https://arxiv.org/abs/2608.18292) | 2026 | Controller · Orchestration |
| [Hierarchical LLM-Based Multi-Agent Framework with Prompt Optimization for Multi-Robot Task Planning](https://arxiv.org/abs/2602.21670) | 2026 | Controller · Orchestration |
| [Humanoid Whole-Body Manipulation via Active Spatial Brain and Generalizable Action Cerebellum](https://arxiv.org/abs/2605.21133) | 2026 | Controller · Orchestration |
| [Hybrid LLM-based Intelligent Framework for Robot Task Scheduling](https://arxiv.org/abs/2605.15486) | 2026 | Controller · Orchestration |
| [IMR-LLM: Industrial Multi-Robot Task Planning and Program Generation using Large Language Models](https://arxiv.org/abs/2603.02669) | 2026 | Controller · Orchestration |
| [Intelligent Multi-UAV Navigation in ITNTNs: A Hierarchical LLM Approach](https://arxiv.org/abs/2607.18604) | 2026 | Controller · Policy writing |
| [KGLAMP: Knowledge Graph-guided Language model for Adaptive Multi-robot Planning and Replanning](https://arxiv.org/abs/2602.04129) | 2026 | Controller · Orchestration |
| [LabEvolver: Training-Free Experience Evolution for Safe and Grounded Wet-Lab Agents](https://arxiv.org/abs/2607.27690) | 2026 | Controller · Orchestration |
| [Leveraging Adaptive Group Negotiation for Heterogeneous Multi-Robot Collaboration with Large Language Models](https://arxiv.org/abs/2602.06967) | 2026 | Controller · Orchestration |
| [LLawCo: Learning Laws of Cooperation for Modeling Embodied Multi-Agent Behavior](https://arxiv.org/abs/2606.28182) | 2026 | Teacher · Demonstration / distillation |
| [LLM-Foraging: Large Language Models for Decentralized Swarm Robot Foraging](https://arxiv.org/abs/2605.01461) | 2026 | Controller · Orchestration |
| [LLM-VLM Fusion Framework for Autonomous Maritime Port Inspection using a Heterogeneous UAV-USV System](https://arxiv.org/abs/2601.13096) | 2026 | Controller · Orchestration |
| [Logic-Based Verification of Task Allocation for LLM-Enabled Multi-Agent Manufacturing Systems](https://arxiv.org/abs/2604.17142) | 2026 | Controller · Orchestration |
| [Long-Term Memory for VLA-based Agents in Open-World Task Execution](https://arxiv.org/abs/2604.15671) | 2026 | Controller · Orchestration |
| [MA-CoNav: A Master-Slave Multi-Agent Framework with Hierarchical Collaboration and Dual-Level Reflection for Long-Horizon Embodied VLN](https://arxiv.org/abs/2603.03024) | 2026 | Controller · Direct action |
| [MALLVI: A Multi-Agent Framework for Integrated Generalized Robotics Manipulation](https://arxiv.org/abs/2602.16898) | 2026 | Controller · Orchestration |
| [Managing Context and Communication in Distributed Agentic UAV Swarms](https://arxiv.org/abs/2610.01569) | 2026 | Controller · Orchestration |
| [MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models](https://arxiv.org/abs/2606.24815) | 2026 | Designer · Rewards / tasks |
| [MeCo: Enhancing LLM-Empowered Multi-Robot Collaboration via Similar Task Memoization](https://arxiv.org/abs/2601.20577) | 2026 | Controller · Orchestration |
| [Melding LLM and temporal logic for reliable human-swarm collaboration in complex scenarios](https://arxiv.org/abs/2605.07877) | 2026 | Controller · Orchestration |
| [MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation](https://arxiv.org/abs/2609.24145) | 2026 | Teacher · Demonstration / distillation |
| [MistyPilot: An Agentic Fast-Slow Thinking LLM Framework for Misty Social Robots](https://arxiv.org/abs/2603.03640) | 2026 | Controller · Orchestration |
| [MistyPilot: Enabling Social-Robot Control through Multi-Agent LLM Skill Orchestration](https://arxiv.org/abs/2608.15549) | 2026 | Controller · Orchestration |
| [MiTa: A Hierarchical Multi-Agent Collaboration Framework with Memory-integrated and Task Allocation](https://arxiv.org/abs/2601.22974) | 2026 | Controller · Orchestration |
| [Mosaic: Runtime-Efficient Multi-Agent Embodied Planning](https://arxiv.org/abs/2607.09603) | 2026 | Controller · Orchestration |
| [NavHarness: Adaptive Goals for Agentic Vision-Language Navigation](https://arxiv.org/abs/2609.39915) | 2026 | Controller · Direct action |
| [On-Demand Human Assistance for Task Continuation under Physical Action Failures in LLM-based Planning](https://arxiv.org/abs/2603.28156) | 2026 | Supervisor · Monitoring / recovery |
| [OntoPlan: An Ontology-Grounded Scene Representation and Agentic Framework for Scalable Robot Task Planning](https://arxiv.org/abs/2610.07649) | 2026 | Controller · Orchestration |
| [Organizational Principles Enable Collective Intelligence in Embodied AI](https://arxiv.org/abs/2609.11737) | 2026 | Controller · Orchestration |
| [OSDAG: Online Scheduling for Efficient Multi-Robot Collaboration](https://arxiv.org/abs/2606.15255) | 2026 | Controller · Orchestration |
| [PhysCaP: Grounding Code-as-Policy Agent with Physics-Informed Exploration](https://arxiv.org/abs/2608.21031) | 2026 | Controller · Policy writing |
| [Physical Agentic AI: An Architecture for Orchestrating a Robot Crew with LLMs](https://arxiv.org/abs/2608.22657) | 2026 | Controller · Orchestration |
| [QuadAgent: A Responsive Agent System for Vision-Language Guided Quadrotor Agile Flight](https://arxiv.org/abs/2604.02786) | 2026 | Controller · Orchestration |
| [Qumus: Realization of An Embodied AI Quantum Material Experimentalist](https://arxiv.org/abs/2605.18407) | 2026 | Controller · Orchestration |
| [RACAS: Controlling Diverse Robots With a Single Agentic System](https://arxiv.org/abs/2603.05621) | 2026 | Controller · Direct action |
| [RoboRouter: Training-Free Policy Routing for Robotic Manipulation](https://arxiv.org/abs/2603.07892) | 2026 | Controller · Orchestration |
| [RoboSolver: A Multi-Agent Large Language Model Framework for Solving Robotic Arm Problems](https://arxiv.org/abs/2602.14438) | 2026 | Controller · Orchestration |
| [ROSClaw: A Hierarchical Semantic-Physical Framework for Heterogeneous Multi-Agent Collaboration](https://arxiv.org/abs/2604.04664) | 2026 | Controller · Orchestration |
| [Safe and Interpretable Multimodal Path Planning for Multi-Agent Cooperation](https://arxiv.org/abs/2602.19304) | 2026 | Controller · Policy writing |
| [Safe Multi-Robot Coordination via VLM–LLM Reasoning and Reachability Analysis](https://arxiv.org/abs/2609.27816) | 2026 | Controller · Orchestration |
| [Say the Mission, Execute the Swarm: Agent-Enhanced LLM Reasoning in the Web-of-Drones](https://arxiv.org/abs/2605.03788) | 2026 | Controller · Orchestration |
| [Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents](https://arxiv.org/abs/2609.39304) | 2026 | Developer · System / code |
| [Scale-Plan: Scalable Language-Enabled Task Planning for Heterogeneous Multi-Robot Teams](https://arxiv.org/abs/2603.08814) | 2026 | Controller · Orchestration |
| [Sentinel: Embodied Cooperative Spatial Reasoning and Planning](https://arxiv.org/abs/2605.26239) | 2026 | Controller · Orchestration |
| [SG-CoT: An Ambiguity-Aware Robotic Planning Framework using Scene Graph Representations](https://arxiv.org/abs/2603.18271) | 2026 | Controller · Orchestration |
| [SkySim: A ROS2-based Simulation Environment for Natural Language Control of Drone Swarms using Large Language Models](https://arxiv.org/abs/2602.01226) | 2026 | Controller · Orchestration |
| [Structured World-State Reasoning for Agentic Robotic Search](https://arxiv.org/abs/2609.23841) | 2026 | Controller · Orchestration |
| [TypeGo: An OS Runtime for Embodied Agents](https://arxiv.org/abs/2607.05482) | 2026 | Controller · Orchestration |
| [UAVGENT: A Language-Guided Distributed Control Framework](https://arxiv.org/abs/2602.13212) | 2026 | Controller · Orchestration |
| [What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery](https://arxiv.org/abs/2609.31760) | 2026 | Developer · System / code |
| [World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal](https://arxiv.org/abs/2609.29964) | 2026 | Controller · Direct action |
| [Zero-shot adaptable task planning for autonomous construction robots: a comparative study of lightweight single and multi-AI agent systems](https://arxiv.org/abs/2601.14091) | 2026 | Controller · Orchestration |

</details>

## Benchmarks and resources

| Name | Paper | Year | Venue | Evaluated seat | Body |
|---|---|---|---|---|---|
| **Embodied Agent Interface** | [Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making](https://arxiv.org/abs/2410.07166) | 2024 | NeurIPS | Controller | mobile-manip/sim |
| **PARTNR** | [PARTNR: A Benchmark for Planning and Reasoning in Embodied Multi-agent Tasks](https://arxiv.org/abs/2411.00081) | 2024 | arXiv | Controller | mobile-manip/sim |
| **SafeAgentBench** | [SafeAgentBench: A Benchmark for Safe Task Planning of Embodied LLM Agents](https://arxiv.org/abs/2412.13178) | 2024 | arXiv | Controller | mobile-manip/sim |
| **EmbodiedEval** | [EmbodiedEval: Evaluate Multimodal LLMs as Embodied Agents](https://arxiv.org/abs/2501.11858) | 2025 | arXiv | Controller | mobile-manip/sim |
| **EmbodiedBench** | [EmbodiedBench: Comprehensive Benchmarking Multi-modal Large Language Models for Vision-Driven Embodied Agents](https://arxiv.org/abs/2502.09560) | 2025 | ICML | Controller | mobile-manip/sim |
| **ASIMOV** | [Generating Robot Constitutions & Benchmarks for Semantic Safety](https://arxiv.org/abs/2503.08663) | 2025 | arXiv | Supervisor | other/real |
| **RoboCerebra** | [RoboCerebra: A Large-scale Benchmark for Long-horizon Robotic Manipulation Evaluation](https://arxiv.org/abs/2506.06677) | 2025 | NeurIPS | Controller | manip/sim |
| **IS-Bench** | [IS-Bench: Evaluating Interactive Safety of VLM-Driven Embodied Agents in Daily Household Tasks](https://arxiv.org/abs/2506.16402) | 2025 | AAAI | Supervisor | mobile-manip/sim |
| **CaP-X** | [CaP-X: A Framework for Benchmarking and Improving Coding Agents for Robot Manipulation](https://arxiv.org/abs/2603.22435) | 2026 | arXiv | Controller | manip/sim+real |
| **Smart-Agriculture Engine** | [Deploying and Evaluating a Smart-Agriculture Agentic Engine for Full-Season Soybean Farm Operations](https://arxiv.org/abs/2609.00106) | 2026 | arXiv | Controller | other/real |
| **MLLM Drone Agents Eval** | [Evaluating Multimodal LLMs as Generalist Vision-Language-Action Agents for Drone Control: Commanding, Approaching, Tracking and Searching](https://arxiv.org/abs/2609.01404) | 2026 | arXiv | Controller | aerial/sim |
| **Astra on VLN-CE** | [How Far Can GPT-6-Astra Go? Evaluating Capabilities in Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2609.20116) | 2026 | arXiv | Controller | nav/sim |
| **WhenToAsk** | [When Should a Failing Robot Ask? Initiating Corrective Human-Robot Dialogue from Audited Sensor Evidence](https://arxiv.org/abs/2609.21942) | 2026 | arXiv | Supervisor | manip/sim+real |
| **Astra on RoboDojo** | [An Unexpected Robot Policy: Early Evaluations of GPT-6 Astra on RoboDojo and Beyond](https://arxiv.org/abs/2609.24170) | 2026 | arXiv | Controller | manip/sim |
| **CodeActionBench** | [CodeActionBench: Evaluating Agentic Code-as-Policy for Embodied Manipulation](https://arxiv.org/abs/2609.33807) [[project]](https://codeactionbench.org) | 2026 | arXiv | Controller | manip/sim |
| **RLE-Bench** | [RLE-Bench: A Qualifying Exam for Coding Agents as Robot Learning Engineers](https://arxiv.org/abs/2609.34210) [[project]](https://rle-bench.github.io/) | 2026 | arXiv | Developer | manip/sim |
| **LIBERO-Agent** | [LIBERO-Agent: Evaluating General-Purpose Agents for Direct Embodied Manipulation](https://arxiv.org/abs/2609.39507) | 2026 | arXiv | Controller | manip/sim |
| **Frontier VLM Agents Study** | [Are Frontier VLM Agents Ready to Be Robot Generalists? An Empirical Study with the Embodied Agent Arena](https://arxiv.org/abs/2610.00854) [[project]](https://embodied-agent-arena.github.io/embodied-agent-arena/) | 2026 | arXiv | Controller | mobile-manip/sim |
| **Video2World** | [Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos](https://arxiv.org/abs/2610.04432) [[project]](https://aetherlabsai.github.io/Video2World) | 2026 | arXiv | Designer | manip/sim |
| **RobotWorld** | [RobotWorld: Benchmarking Multimodal Agents for Robot Use Across Diverse Tasks and Embodiments](https://arxiv.org/abs/2610.10409) | 2026 | arXiv | Controller | other/sim |

## More 2026 papers

436 further 2026 papers that meet the definition but are not in the curated tables above. Each was judged from its full text (a first pass, then a verification pass by a stronger model; papers off arXiv without an open-access PDF were judged from the abstract); the reasons and quotes are in [docs/paper_list.md](docs/paper_list.md). `MA` marks the multi-agent chapter.

<details><summary><b>Designer · Environments / reconstruction</b> (13)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [ARSTAG: An Agentic Real2Sim2Real System for Task-Specific Robot Data Generation](https://arxiv.org/abs/2609.24563) `MA` | 2026 | GPT-5.5 for coordinator and three subagents (agent decisions and multimodal reas |
| [Beyond Placement and Articulation: Usage-Driven Code Scenes for Embodied Interaction](https://arxiv.org/abs/2608.18840) | 2026 | GPT-5.4 (overall scene agent) + Claude Opus 4.8 (object code) |
| [DeformSmith: Physics Harness-Guided Hierarchical Generation of Deformable Assets for Robot Manipulation](https://arxiv.org/abs/2609.18620) `MA` | 2026 | GPT-5.6 Sol as Planner, Designer and Critic LLM agents with role-specific prompt |
| [DiagGen: Agentic Generation of Deformable Assets with Sim-based Diagnostics for Robotic Simulation](https://arxiv.org/abs/2609.23103) `MA` | 2026 | GPT-5.6 Luna for generation and diagnostic agents at Max reasoning, prompted |
| [EmbodiedClaw: Conversational Workflow Execution for Embodied AI Development](https://arxiv.org/abs/2604.13800) | 2026 | Unnamed LLM backend of the EmbodiedClaw agent |
| [FACT: Fidelity-Aware Construction of Articulated Twins](https://arxiv.org/abs/2609.37067) | 2026 | GPT-6 Astra (High reasoning) as the agent for articulated twin construction |
| [LiteReality-Agent: An Agentic System for Interactable 3D Indoor Scene Reconstruction](https://arxiv.org/abs/2610.01863) | 2026 | Unnamed general LLM coding agent (Algorithm 1 LLM call); paper compares GPT-6 As |
| [LogicEnvGen: Task-Logic Driven Generation of Diverse Simulated Environments for Embodied AI](https://arxiv.org/abs/2601.13556) | 2026 | DeepSeek-v3.2, Gemini-2.5-Flash, Qwen2.5-72B-Instruct (prompted, no training) |
| [NeoWorld-Pro: Programming Interactive Scenes from Monocular Images for Embodied Simulation](https://arxiv.org/abs/2608.24212) | 2026 | Qwen3.6-Plus (scene parser); GPT-5.5 (Blender programmer and semantic scorer) |
| [Real2Sim via Active Perception with Behavior Trees Automatically Generated by VLMs](https://arxiv.org/abs/2601.08454) | 2026 | GPT-4o or Gemini 1.5 Pro (Gemini 1.5 Pro in ablations), prompted with a fixed sy |
| [SimWorld Studio: Automatic Environment Generation with Evolving Coding Agent for Embodied Agent Learning](https://arxiv.org/abs/2605.09423) | 2026 | Claude Opus/Sonnet 4.6 and Qwen3.5 as SimCoder coding agent (via Claude Code) |
| [SR-Platform: An Agentic Pipeline for Natural Language-Driven Robot Simulation Environment Synthesis](https://arxiv.org/abs/2605.14700) | 2026 | venice/deepseek-v4-flash (general LLM for scene planning and CadQuery code; othe |
| [Swim2Real: VLM-Guided System Identification for Sim-to-Real Transfer](https://arxiv.org/abs/2603.20827) | 2026 | Gemini 2.5 Pro (proprietary VLM, prompted; ~15 calls per run) |

</details>

<details><summary><b>Designer · Rewards / tasks</b> (22)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Agent-Driven Autonomous Reinforcement Learning Research: Iterative Policy Improvement for Quadruped Locomotion](https://arxiv.org/abs/2603.27416) | 2026 | Claude (Anthropic) via OpenCode as research agent; no authors-trained LLM |
| [AgenticRL: Agentic Reinforcement Learning with Self-Refinement for Complex UAV Navigation](https://arxiv.org/abs/2606.03963) `MA` | 2026 | GPT-5.6-sol (reward generation, behavioral diagnosis and refinement agents); PPO |
| [Autonomously Acquiring Robot Manipulation Skills with Language-Driven Quality-Diversity](https://arxiv.org/abs/2608.30983) | 2026 | GPT-4o (temperature 0; success, fitness and behavior-descriptor code) |
| [Beyond Scripted Search: Sample-Efficient Reward Discovery via Agentic Black-box Optimization](https://arxiv.org/abs/2609.32394) | 2026 | MiniMax-M2.7 backbone of the ARBO LLM agent (other backbones ablated), prompted  |
| [Causal Reward World Models: Zero-shot Reward Design for Automated Skill Generation](https://arxiv.org/abs/2606.23280) | 2026 | DeepSeek-V3.2 (LLM reward writer, zero-shot; causal prior CRWM trained by author |
| [Chain of Uncertain Rewards with Large Language Models for Reinforcement Learning](https://arxiv.org/abs/2604.13504) | 2026 | Unnamed LLM (reward code generator; model not named) |
| [CoDex: Learning Compositional Dexterous Functional Manipulation without Demonstrations](https://arxiv.org/abs/2606.31909) | 2026 | unnamed off-the-shelf VLM (zero-shot prompting, model not named in paper); PPO p |
| [CoRe: Combined Rewards with Vision-Language Model Feedback for Preference-Aligned Reinforcement Learning](https://arxiv.org/abs/2607.01721) | 2026 | GPT-4.1 mini (reward code) + Gemini 2.0 Flash (preference labels) |
| [Discovering Reinforcement Learning Interfaces with Large Language Models](https://arxiv.org/abs/2605.03408) | 2026 | Claude Sonnet 4.6 (temperature 0.7, LLM mutation operator) |
| [EvoNav: Evolutionary Reward Function Design for Robot Navigation with Large Language Models](https://arxiv.org/abs/2605.11859) | 2026 | gpt-oss-120B (open-weight, used as-is via vLLM) as reward-code generator and ref |
| [From Ideal Motion to Flight-Executable Communications: LLM-Evolved Multi-UAV Deployment for Cell-Free Massive MIMO](https://arxiv.org/abs/2609.23992) | 2026 | GPT-5.4 as reward-design LLM via API; MADDPG UAV policies trained as tools |
| [From LLM-Generated Specifications to Learned Quadruped Locomotion](https://arxiv.org/abs/2609.07111) | 2026 | GPT-5.5 and Qwen 3.6 prompted to propose STL templates, not trained |
| [Interactive LLM-Assisted Curriculum Learning for Multi-Task Evolutionary Policy Search](https://arxiv.org/abs/2602.10891) | 2026 | Claude Sonnet 4.5 (extended thinking) as interactive curriculum designer |
| [LEACL: LLM-Enhanced Automatic Curriculum Learning for Reinforcement Learning in Long-Horizon Manipulation Tasks](https://arxiv.org/abs/2607.23515) | 2026 | ChatGPT 4o-mini (task decomposer, PDDL generator, meta-task generator) + PPO pol |
| [MANGO: Automated Multi-Agent Test Oracle Generation for Vision-Language-Action Models](https://arxiv.org/abs/2606.24815) `MA` | 2026 | Gemini Robotics-ER 1.5/1.6 (Generator), lightweight Gemini (Assessors), reasonin |
| [MLREF: Efficient Module Reuse for Reward Design in Reinforcement Learning via Large Language Models](https://arxiv.org/abs/2608.18827) | 2026 | DeepSeek-V4-Flash (reasoning mode, official API) |
| [PRISM: Personalized Refinement of Imitation Skills for Manipulation via Human Instructions](https://arxiv.org/abs/2603.05574) | 2026 | GPT-5 (Eureka-style reward generation); authors' BC plus PPO policy trained in I |
| [Prompt-Driven Exploration](https://arxiv.org/abs/2607.08837) | 2026 | unnamed VLM prompt sampler for VLA (VLA is an authors' pi0.5 SFT checkpoint) |
| [ReCoVLA: VLM-Guided Reward Compilation for Failure Recovery in Vision-Language-Action Policies](https://arxiv.org/abs/2606.09630) | 2026 | Qwen3-VL-8B-Instruct (external VLM failure analyzer, prompted, not trained) + fr |
| [RoboGene: Boosting VLA Pre-training via Diversity-Driven Agentic Framework for Real-World Task Generation](https://arxiv.org/abs/2602.16444) | 2026 | Unnamed LLM/VLM foundation models in an agent loop (baselines GPT-4o and Gemini  |
| [SUN: Agentic Robot Policy Learning with Persistent Task Programs](https://arxiv.org/abs/2608.31167) | 2026 | GPT-5.5 as the Kuafu task-level agent, used as-is with prompts |
| [Video2STL: Grounding VLM-Generated Temporal Specifications for Robot Learning](https://arxiv.org/abs/2609.37519) | 2026 | GPT-5.6 writes STL spec bank; Qwen 3.8 and Gemini 3.1 variants; PPO policy |

</details>

<details><summary><b>Teacher · Demonstration / distillation</b> (16)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [$R^3$: Training Robots to Reason in Natural Language via Reinforcement Learning](https://arxiv.org/abs/2608.26053) | 2026 | Gemini 3 Flash as expert reasoner (sim data); trained Qwen3.5-4B reasoner (SFT + |
| [Accelerating Robotic Reinforcement Learning with Agent Guidance](https://arxiv.org/abs/2602.11978) | 2026 | Qwen3-VL-235B-A22B-Instruct VLM agent with FLOAT DINOv2 trigger; RL policy train |
| [DexAgent: An Agentic Human2Sim2Robot Framework for Dexterous Manipulation with Self-Evolving Tool Library](https://arxiv.org/abs/2609.35318) | 2026 | Unnamed VLM via API (any VLM; GPT-6 Astra only as baseline) |
| [EmbodiRSI: Recursive Self-Improvement for Data-Efficient Robot Adaptation](https://arxiv.org/abs/2609.38905) | 2026 | GPT-5.5 agent system (scene, trajectory, monitor agents); pi0.5 policy trained o |
| [EXIMO: VLM Guided Exploration of VLA Policies](https://arxiv.org/abs/2608.19891) | 2026 | Gemini VLM orchestrator (version unspecified) prompting GROD-3B VLA |
| [GenPHRI: Agentic Generative Simulation for Physical Human-Robot Interaction](https://arxiv.org/abs/2604.08664) `MA` | 2026 | Gemini 3.7 Flash (generator, critic and orchestrator agents) |
| [InSight: Self-Guided Skill Acquisition via Steerable VLAs](https://arxiv.org/abs/2606.24884) | 2026 | Gemini 3 Flash (planner, gap parameterizer, oracle); pi0.5 LoRA-tuned as tool |
| [LLawCo: Learning Laws of Cooperation for Modeling Embodied Multi-Agent Behavior](https://arxiv.org/abs/2606.28182) `MA` | 2026 | Qwen-3-14B fine-tuned on law-guided traces; LLaMA-3.1-8B and 70B backbones |
| [MimicAgent: Quadruped Skills via Prompt-to-Trajectory Generation](https://arxiv.org/abs/2609.24145) `MA` | 2026 | Claude Fable 5.1 in an agentic harness (Sonnet 5 and Opus 5 also compared), prom |
| [MotionDisco: Motion Discovery for Extreme Humanoid Loco-Manipulation](https://arxiv.org/abs/2606.06139) | 2026 | Claude Opus 4.7 (prompted LLM mutating contact-plan programs) |
| [PRACTICE: From Experience to Expertise in Self-Evolving Embodied Agents](https://arxiv.org/abs/2608.30760) | 2026 | Frozen executors GPT-5.4, Gemini-3-Flash, Qwen3-VL-32B; trained Qwen3-VL-8B skil |
| [Practice Makes Policies: Bootstrapping and Consolidating Robotic Capabilities from Zero Human Demonstrations](https://arxiv.org/abs/2607.26809) | 2026 | Gemini-3-Flash (VLM for orchestrator and L1/L2 queries); pi0.5 fine-tuned as L3  |
| [RE-0: Verified Recursive Improvement of Embodied Code-as-Policy Agents through Local On-Policy Distillation](https://arxiv.org/abs/2609.32416) | 2026 | qwen3.8-max API teacher and diagnostic agents (prompted); student Qwen3.8-27B Lo |
| [Recursive Self-Improvement of Visuomotor Policies through Local Recovery Supervision](https://arxiv.org/abs/2610.05151) | 2026 | gpt-6.1-sol tool teacher (medium reasoning); student pi0 with LoRA |
| [Skill-Space Shooting for Autonomous Robot Policy Improvement](https://arxiv.org/abs/2609.38178) | 2026 | Gemini 2.5 Pro as VLM judge (picks skill, checks repair); trained value model tr |
| [Zero2Skill: Bootstrapping Robot Skills through Autonomous Data Collection, Training, and Deployment](https://arxiv.org/abs/2607.14047) | 2026 | OpenClaw embodied agent (backbone LLM unnamed); Seed1.8 verifier; DeepSeek-V3.2  |

</details>

<details><summary><b>Developer · System / code</b> (46)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Act-Observe-Rewrite: Multimodal Coding Agents as In-Context Policy Learners for Robot Manipulation](https://arxiv.org/abs/2603.04466) | 2026 | Claude Code coding agent (claude-sonnet-4-x family) rewriting controller code be |
| [Agentic AutoResearch forSpace Autonomy: An Auditable, LLM-Driven Research Agent for Aerospace Control Problems](https://arxiv.org/abs/2606.20394) | 2026 | Claude Sonnet 4.5 (proposer of train.py hyperparameter edits) |
| [AI Training Manager: Bounded Closed-Loop Control of Adaptive Training Recipes](https://arxiv.org/abs/2606.29871) | 2026 | GPT-5.4 (Stage 1 reasoning) + GPT-5.4-mini (Stage 2 action compiler) |
| [An AI Scientist that Doesn't Drift: Taste, Structure, and Falsifiable Findings in a Quadruped Navigation Research Loop](https://arxiv.org/abs/2608.07542) `MA` | 2026 | Claude (persistent orchestrator plus 10 subagents; version not stated) |
| [Automating the Design of Embodied AgentArchitectures](https://arxiv.org/abs/2606.30111) | 2026 | Claude Opus 4.7 orchestrating Claude Code optimizers; GPT-5-mini executor backbo |
| [CABTO: Context-Aware Behavior Tree Grounding for Robot Manipulation](https://arxiv.org/abs/2603.16809) | 2026 | GPT-4o as LLM (action models) and VLM (policy code sampling); Molmo and cuRobo a |
| [Discovering Diverse Planning Policies for Multimodal Embodied Agents with Quality-Diversity Optimization](https://arxiv.org/abs/2608.08523) | 2026 | GPT-4 default (also LLaMA-2, CoLLAMA-2); no training |
| [Don't Drop the BATON: Long-Horizon Robot Manipulation via Agentic Subtask Exploration and Transition-aware Memory](https://arxiv.org/abs/2608.16889) | 2026 | GPT-5.6-sol (coding-agent backbone) plus frozen pi-RLinf VLA used as a tool |
| [EmbodiedRSI: Active Continual Robot Learning Through Hypothesis-Guided Co-Evolution](https://arxiv.org/abs/2610.10498) | 2026 | Unnamed LLM in the Fast System / Skill Architect writes code and skills; frozen  |
| [EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents](https://arxiv.org/abs/2605.10332) | 2026 | Frozen Qwen2.5-14B / Qwen3.5-27B / Qwen3-VL executors; GPT-5.2 or Gemini-3-flash |
| [EMHO: EMbodied Agent Harness Optimization via Experience Traces](https://arxiv.org/abs/2610.08432) | 2026 | Qwen3.5-9B / Qwen3.8-27B-FP8 frozen; the same model serves as embodied agent and |
| [EMPIRIC: Experiment-Driven Learning of Residual World Models for Robot Planning](https://arxiv.org/abs/2609.35047) | 2026 | Claude Opus 5 (high effort) as coding agent; no training reported |
| [Encore: Few-Shot Agentic Discovery of Manipulation Strategies](https://arxiv.org/abs/2609.37359) | 2026 | opus-5 coding agent (writes and refines policy program over development rollouts |
| [From Sign Language Generation to Humanoid Execution: Vision-Language Guided Retargeting with Collision Mitigation](https://arxiv.org/abs/2607.17769) | 2026 | GPT-5.2 as VLM critic with fixed critique prompt (offline render-critique-re-sol |
| [GaP: A Graph-as-Policy Multi-Agent Self-Learning Harness For Variational Automation Tasks](https://arxiv.org/abs/2607.05369) `MA` | 2026 | Gemini-3.1-Flash-Lite (orchestration and skill agents; VLM) |
| [GUIDE: Guided Updates for In-context Decision Evolution in LLM-Driven Spacecraft Operations](https://arxiv.org/abs/2603.27306) | 2026 | Acting LLM (not named in text) for thrust commands + frontier Reflector LLM for  |
| [HarnessPAI: An Evolving Harness for Physical AI](https://arxiv.org/abs/2609.29166) | 2026 | GPT-5.6-sol (Codex) writes and synthesizes; Gemini-3.5-Flash video diagnoser; pi |
| [HuGo: LLMs as Whole-Body Policy Code Designers for Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.30594) | 2026 | gpt-5.4 (writes closed-loop high-level policy code; frozen low-level whole-body  |
| [Iterative Policy Refinement through Semantic Rollout Analysis](https://arxiv.org/abs/2610.01652) | 2026 | GPT-5-mini (high reasoning; writes structured policy code and analysis code) |
| [Kintsugi: Learning Policies by Repairing Executable Knowledge Bases](https://arxiv.org/abs/2605.09487) | 2026 | gpt-5.5 as offline KB editor (gpt-4o as weaker-editor diagnostic); zero LLM call |
| [Learning and Transferring Closed-Loop Robot Software](https://arxiv.org/abs/2609.19906) | 2026 | gpt-6-astra coding agent (high reasoning) writes closed-loop policy code; no run |
| [LEMCA: LLM-Guided Synthesis of Efficient Mode-Switching Control Architectures](https://arxiv.org/abs/2609.21319) | 2026 | gemini-3.1-pro as LLM design operator in genetic search; MSC-PPO RL trains each  |
| [MEMENTO: Memory-Guided Memetic Code-as-Policy Evolution](https://arxiv.org/abs/2607.22832) | 2026 | GPT-5.2 (evaluator and code-as-policy proposals) |
| [Nautilus: From One Prompt to Plug-and-Play Robot Learning](https://arxiv.org/abs/2605.11665) | 2026 | Claude Opus 4.7 / Claude Sonnet 4.6 inside a Claude Code harness (no authors' tr |
| [NEXUS: Continual Learning of Symbolic Constraints for Safe and Robust Embodied Planning](https://arxiv.org/abs/2605.09387) | 2026 | GPT-4 (backbone for all stages, no weight training) |
| [Novelty Adaptation Through Hybrid Large Language Model (LLM)-Symbolic Planning and LLM-guided Reinforcement Learning](https://arxiv.org/abs/2603.11351) | 2026 | GPT-o3 for PDDL operator discovery and planning; GPT-o4-mini for dense reward fu |
| [PDDL-ART: Autonomous Symbolic Abstraction From Demonstration For Long-Horizon Robotic Manipulation Using Vision-Language Models](https://arxiv.org/abs/2608.17146) | 2026 | GPT-o3 (reasoning VLM) and GPT-5.5 (general VLM), zero-shot |
| [Privacy-Preserving Prompted Policy Search for Robotic Control](https://arxiv.org/abs/2609.30554) | 2026 | gpt-oss-20b (open-weight reasoning LLM, prompted; proposes linear-policy paramet |
| [ProactiveVLA: Augmenting Embodied Memory through Proactive Environment Exploration](https://arxiv.org/abs/2610.06999) | 2026 | Codex as high-level agent (underlying model not named in the paper); frozen VLA  |
| [RACaP: Agentic Reasoning, Acting, and Coding as Policies for Evolvable Robot Learning](https://arxiv.org/abs/2609.29394) | 2026 | GPT-5.6 coding agent evolves Policy APIs, harness and memory; GPT-5.5 ReAct agen |
| [RAPID: Robot Agentic Programming from Demonstrations](https://arxiv.org/abs/2609.30249) | 2026 | Codex with GPT-5.6 Sol (high reasoning) as coding agent writing primitives and s |
| [Representation-Guided Generation and Integration of Executable Programs for Robot Manipulation](https://arxiv.org/abs/2609.31337) | 2026 | Claude Opus 5 (authors perception and planning programs offline) |
| [Retrieval-grounded robot program generation and simulation-based correction via Model Context Protocol](https://arxiv.org/abs/2608.21417) | 2026 | Unnamed general LLM client (model not named; RAG and MCP tool calls, no training |
| [Revisiting the"Push-T"Robot Manipulation Task with Agentic Robotics](https://arxiv.org/abs/2608.18227) | 2026 | Claude Code harness driving Fable 5 (frontier general model, size not given) |
| [RoboBridge: A Self-Evolving Embodied Agent Framework for Sim-to-Real Transfer](https://arxiv.org/abs/2610.02717) | 2026 | Codex with GPT-5.5 as coding-agent planner; pi0.5 checkpoints as frozen action t |
| [RoboFoundry: System-as-Policy Evolution for Self-Learning Embodied Agents](https://arxiv.org/abs/2609.32862) | 2026 | GPT-5.5 / Qwen3.7-Plus (frozen weights; evolved system around them) |
| [RoboHarn-Evo: Evolving Hierarchical Physical Knowledge for Self-Improving Robotic Manipulation](https://arxiv.org/abs/2609.37583) | 2026 | GPT-5.5 / GPT-6 as VLM planner (Qwen3.8-27B also tested); base VLM and executor  |
| [RoboReact: Agentic Skill Distillation from Generated Egocentric Videos for Generalizable Whole-Body Manipulation](https://arxiv.org/abs/2608.03387) | 2026 | GPT-5.6-ultra or GPT-5.1-mini as frozen Codex policy editor (VLM) |
| [Scale and Selection: What Makes Automatic Harness Evolution Work for Visual-Interface Robot Agents](https://arxiv.org/abs/2609.39304) `MA` | 2026 | Codex with GPT-5.6 Sol as task agent and as optimizer agent revising its harness |
| [Self-Evolving Scientific Agent Designs Physically Reasoned White-Box Fluid Control](https://arxiv.org/abs/2606.08405) | 2026 | gpt-5.6-sol via Codex (EvE design agents, xhigh reasoning) |
| [Test-Driven Agentic Framework for Reliable Robot Controller](https://arxiv.org/abs/2603.00455) | 2026 | GPT-5.2, GPT-4.1, Claude Sonnet/Opus-4.5 as Learner; GPT-4o as Optimizer (no fin |
| [VASO: Formally Verifiable Self-Evolving Skills for Physical AI Agents](https://arxiv.org/abs/2606.05395) | 2026 | GPT-5-nano (skill generator Fskill) + GPT-4o-mini (planner Fplan) |
| [VersualRL: Closed-Loop Verbal Reinforcement Learning with Visual Execution Feedback for Task-Level Robot Planning](https://arxiv.org/abs/2603.22169) | 2026 | LLM actor (model not named in text) + Gemini-3-Pro-Preview VLM critic (best conf |
| [What Stops Recursive Self-Improvement in Robotics? Lessons from 123 Rounds of Agentic Skill Discovery](https://arxiv.org/abs/2609.31760) `MA` | 2026 | GPT-5.6-sol then gpt-6-astra as Codex CLI orchestrator, proposer and research ag |
| [When are LLMs Sufficient Policy Optimizers for Sequential RL Tasks?](https://arxiv.org/abs/2605.30719) | 2026 | Gemini 3 Pro writing Python policies (PromptPO); PPO/SAC only as baselines |
| [You Don't Need To Stay in The Loop: An Agentic Robotics Loop for Robot-Policy Improvement](https://arxiv.org/abs/2608.07555) | 2026 | Unnamed LLM controller (Markdown protocol); SmolVLA and other VLA checkpoints as |

</details>

<details><summary><b>Developer · Embodiment / tools</b> (1)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [When Search Becomes Memory: Accelerating Robot Design Discovery with Self-Evolving Skills](https://arxiv.org/abs/2605.25832) | 2026 | gpt-5.5 for PROPOSE, ADD, DIAGNOSE and MERGE; PPO used only as fitness evaluator |

</details>

<details><summary><b>Controller · Orchestration</b> (234)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [2AM: Grounding Agent-Side Memory as Guidance for Steerable Action Models in Long-Horizon Manipulation](https://arxiv.org/abs/2609.11308) | 2026 | Qwen3.8-27B as Agent (off-the-shelf, not trained) + Qwen3-VL-4B flow-matching Ac |
| [3DGSNav: Enhancing Vision-Language Model Reasoning for Object Navigation via Active 3D Gaussian Splatting](https://arxiv.org/abs/2602.12159) | 2026 | Gemini3-Pro (frontier-selection planner VLM); GLM-4.5V (action-decision VLM); YO |
| [A Brain-inspired Hierarchical Framework for Zero-Shot Robot Task Reasoning and Execution](https://arxiv.org/abs/2609.05985) | 2026 | Qwen3 LLM backbone (written as qwen3.7 plus / Qwen3-7B), zero-shot; SAM 3 percep |
| [A Closed-Loop Multi-Agent Framework for Robust Multi-Robot Manipulation](https://arxiv.org/abs/2607.06990) `MA` | 2026 | Qwen3-Max planner and Qwen3-VL-Plus manipulation and verification agents via API |
| [A Conversational Framework for Human-Robot Collaborative Manipulation with Distributed Generative AI models](https://arxiv.org/abs/2606.06061) `MA` | 2026 | ministral-3:8b (LLM parser) + Qwen2.5-VL-32B (VLM grounding), both zero-shot |
| [A Framework for Low-Latency, LLM-Driven Multimodal Interaction on the Pepper Robot](https://arxiv.org/abs/2603.21013) | 2026 | General speech-to-speech LLMs via API (OpenAI gpt-realtime, Gemini Live, Grok, A |
| [A Framework for Seamless Physical, Verbal, and Graphical Robot Skill Learning and Adaptation](https://arxiv.org/abs/2604.20468) | 2026 | Qwen2.5-VL-72B-Instruct used as-is with tool calling for skill adaptation |
| [A Generative Partially Specified Finite State Machine Approach to Complex Behaviour Planning](https://arxiv.org/abs/2607.15674) | 2026 | GPT-4o, GPT-4.1 and GPT-5 (cloud, zero- and one-shot prompting); Llama-chat and  |
| [A Glimpse into Long-term Physical Coexistence with Intelligent Robots](https://arxiv.org/abs/2607.11377) `MA` | 2026 | claude-opus-4.6 (full routing) + Qwen3.5-4B (pre-filter) via OpenClaw; Astribot  |
| [A Multimodal Framework for Human-Multi-Agent Interaction](https://arxiv.org/abs/2603.23271) `MA` | 2026 | unnamed LLM + VLM (model not named in paper) |
| [A Semantic Autonomy Framework for VLM-Integrated Indoor Mobile Robots: Hybrid Deterministic Reasoning and Cross-Robot Adaptive Memory](https://arxiv.org/abs/2605.02525) | 2026 | Qwen 3.5:4b via Ollama (VLM, escalation only for ambiguous instructions, about 1 |
| [ABot-AgentOS: A General Robotic Agent OS with Lifelong Multi-modal Memory](https://arxiv.org/abs/2607.10350) | 2026 | Qwen3.6-Plus as single main LLM controller (DeepSeek-V4-Pro also tested), with Q |
| [ACE: Agentic Control for Embodied Manipulation via Zero-shot Workflow Reasoning](https://arxiv.org/abs/2607.04162) | 2026 | Qwen3.8-27B via Qwen-Agent (prompted); trained diffusion policy and SAM3 used as |
| [Active Perception for Embodied Disambiguation](https://arxiv.org/abs/2608.13605) | 2026 | Qwen3.7-Plus (API, general VLM) choosing observe / ask / select per step |
| [Actively Resolving Contextual Uncertainty for Underspecified Tasks in Natural Language](https://arxiv.org/abs/2609.30428) | 2026 | GPT-5.1 (low reasoning; pre-trained LLM policy with system prompt) |
| [AdaClearGrasp: Learning Adaptive Clearing for Zero-Shot Robust Dexterous Grasping in Densely Cluttered Environments](https://arxiv.org/abs/2603.10616) | 2026 | Qwen3-VL-32B-Instruct (prompted; MCP tool calls, GeoGrasp PPO policy as a skill) |
| [Adaptive Companionship for Group-Following Robots: Handling Dynamically Changing Group Formations](https://arxiv.org/abs/2607.01287) | 2026 | Gemini 2.5 Flash Lite (VLM, used as-is) |
| [ADM-Planner: LLM-Guided Long-Horizon Planning for Mobile Manipulators with Attention-Enhanced Dynamic Memory](https://arxiv.org/abs/2609.29212) | 2026 | Frozen GPT-5 Mini (gpt-5-mini-2025-08-07) planner; deterministic surrogate in th |
| [Advancing Omnimodal Embodied Agents from Isolated Skills to Everyday Physical Autonomy](https://arxiv.org/abs/2606.27251) | 2026 | Gemini-3.1-Pro planner (Gemini-3-Flash, Qwen3.6, Qwen3-VL also tested); Qwen3-VL |
| [Aerial Agentic AI: Synergizing LLM and SLM for Low-Altitude Wireless Networks](https://arxiv.org/abs/2603.22866) `MA` | 2026 | TinyLlama-1.1B on UAVs (SLM) and LLaMA2-7B at base station (LLM), off-the-shelf, |
| [AeroWeaver: An Embodied-Agent Harness for Weaving Aerial Skills into Distributed, Adaptive Swarm Execution](https://arxiv.org/abs/2609.18520) `MA` | 2026 | DeepSeek V4-flash (main; GPT-5.6 Luna, GLM-5.3-Flash, qwen3.8-flash as backbone  |
| [Affordance-Aware Interactive Decision-Making and Execution for Ambiguous Instructions](https://arxiv.org/abs/2602.05273) | 2026 | GPT-5 with prompt-engineered multimodal CoT, zero-shot; YOLO-World, SAM2, Mobile |
| [Agent Priors-guided Policy Learning](https://arxiv.org/abs/2609.35690) | 2026 | GPT-5.6 Sol runtime agent selecting and calling trained diffusion skill policies |
| [Agentic AI for Robot Control: Flexible but still Fragile](https://arxiv.org/abs/2602.13081) | 2026 | OpenAI o3 (planner/executor); gpt-5-mini (router, chatbot); o4-mini (goal-comple |
| [Agentic Neuro-Symbolic Planning and Commissioning for Human-in-the-Loop Industrial Robotics with Digital Twins](https://arxiv.org/abs/2606.08214) `MA` | 2026 | GPT-4o-mini (temperature 0.3) as Orchestrator and Designer agents; Inspector is  |
| [Agentic RAG-VLM: Affordance-Aware Retrieval-Augmented Generation with Self-Reflective Planning for Robotic Grasping](https://arxiv.org/abs/2606.31200) | 2026 | Qwen3-VL-8B as prompted ReAct planner (INT4 quantized, no training) |
| [AgenticCache: Cache-Driven Asynchronous Planning for Embodied AI Agents](https://arxiv.org/abs/2604.24039) `MA` | 2026 | GPT-5 / GPT-5-mini / GPT-5-nano作为规划器（现成模型，经OpenAI API调用） |
| [AgenticDiffusion: Multi-View Reasoning with View-Conditioned Diffusion Planning for Vision-Based UAV Navigation](https://arxiv.org/abs/2606.04111) | 2026 | Claude Sonnet 5 (VLM) orchestrated by OpenClaw |
| [AgenticSwarm: Semantic Perception and Adaptive Task Allocation for Heterogeneous Multi-UAV Missions](https://arxiv.org/abs/2609.21716) `MA` | 2026 | GPT-5.6-sol (VLM mission interpretation and perception; OR-Tools allocation) |
| [AgentRob: From Virtual Forum Agents to Hijacked Physical Robots](https://arxiv.org/abs/2602.13591) `MA` | 2026 | Doubao via Volcengine ARK API (forum LLM agents and VLM robot controllers) |
| [ALRM: Agentic LLM for Robotic Manipulation](https://arxiv.org/abs/2601.19510) `MA` | 2026 | Claude-4.1-Opus (top model); other off-the-shelf LLMs incl. GPT-5, Gemini-2.5-Pr |
| [An Approach to Combining Video and Speech with Large Language Models in Human-Robot Interaction](https://arxiv.org/abs/2602.20219) | 2026 | LLaMA 3.1 7B as language backbone, with Florence-2 and Whisper as tools |
| [An Embodied Companion for Visual Storytelling](https://arxiv.org/abs/2603.05511) | 2026 | Google Gemini API models via function calling (version varies; Gemini-2.5-pro be |
| [Analytic Concept-Centric Memory for Agentic Embodied Manipulation](https://arxiv.org/abs/2606.29774) | 2026 | GPT-5.5 (high-level reasoning LLM) with SAM, FoundationPose and finetuned VLA as |
| [AnchorVLN: Geometry-Anchored Vision-Language Grounding Reasoning for Open-Vocabulary Navigation](https://arxiv.org/abs/2609.12285) | 2026 | Claude Opus 5 (claude-opus-5), extended thinking off, as VLM client calling MCP  |
| [ARIS: Agentic and Relationship Intelligence System for Social Robots](https://arxiv.org/abs/2605.00943) | 2026 | Grok 2 (Reasoner and Speech LLM) with Grok-2-Vision captioner |
| [As You Wish: Mission Planning with Formal Verification using LLMs in Precision Agriculture](https://arxiv.org/abs/2606.18519) `MA` | 2026 | Claude Sonnet 4 (claude-sonnet-4-20250514) for the XML mission and LTL agents; g |
| [BioProVLA-Agent: An Affordable, Protocol-Driven, Vision-Enhanced VLA-Enabled Embodied Multi-Agent System with Closed-Loop-Capable Reasoning for Biological Laboratory Manipulation](https://arxiv.org/abs/2605.07306) `MA` | 2026 | Qwen3.6-Plus (protocol parsing); RAG-Doubao-Seed-2.0-Pro (VLM verification); Aug |
| [Bridging Semantics and Kinematics: A Modular Framework for Zero-Shot Robotic Manipulation](https://arxiv.org/abs/2606.23157) | 2026 | Molmo2 8B (open-weight VLM used zero-shot, training-free) |
| [Bridging Semantics and Physical Execution: A Neuro-Symbolic Framework for Multi-Pair Robotic Assembly](https://arxiv.org/abs/2606.10808) | 2026 | LLM (model not named; no fine-tuning described) |
| [Bridging Semantics and Physics with Constrained LLMs for Safe and Trustworthy Robotic Manipulation](https://arxiv.org/abs/2608.29379) | 2026 | Claude Sonnet 4 as reasoning backbone of semantic layer, prompted with MCP tools |
| [Bridging Speech, Emotion, and Motion: a VLM-based Multimodal Edge-deployable Framework for Humanoid Robots](https://arxiv.org/abs/2602.07434) | 2026 | GPT-4o (cloud SeM2 VLM with CoT prompt); MiniCPM-V-2.6 8B SFT student for the ed |
| [Bridging the 2D-3D Gap: A Hierarchical Semantic-Geometric Map for Vision Language Navigation](https://arxiv.org/abs/2606.00095) | 2026 | GPT-5 API (VLM high-level planner, zero-shot, training-free) |
| [Bridging Thought and Action: Taming Long-Horizon Instability in Open-Source LLM Agents with a MetaTool-Enhanced ROS Framework](https://arxiv.org/abs/2609.13335) | 2026 | GPT-OSS-120B as main LLM backbone via Groq API (also GPT-4o, GPT-OSS-20B, Kimi-K |
| [Bridging Values and Behavior: A Hierarchical Framework for Proactive Embodied Agents](https://arxiv.org/abs/2604.27699) | 2026 | gpt-4.1 Generator, Critic and Adjust modules with gpt-5-thinking Evaluator; PDDL |
| [Can a Robot Walk the Robotic Dog: Triple-Zero Collaborative Navigation for Heterogeneous Multi-Agent Systems](https://arxiv.org/abs/2603.21723) `MA` | 2026 | Doubao-vision-3.6 (general VLM) for humanoid and quadruped coordination |
| [CAPER: Constrained and Procedural Reasoning for Robotic Scientific Experiments](https://arxiv.org/abs/2602.09367) | 2026 | Meta-Llama-3.1-8B-Instruct (CoT task planner) and GPT-4o (VLM action-primitive m |
| [CAUSALNAV: A Long-Term Embodied Navigation System for Autonomous Mobile Robots in Dynamic Outdoor Scenarios](https://arxiv.org/abs/2601.01872) | 2026 | Locally deployed open-source 14B-class LLM (DeepSeek-R1-Distill-14B best open-so |
| [CGFM-Nav: Cognitive Graph-Field Memory for Semantic-Guided Lifelong Multimodal Embodied Navigation](https://arxiv.org/abs/2608.29114) | 2026 | Qwen3-VL-8B-Instruct as training-free VLM (GPT-4o only in MSGNav baseline) |
| [CIRRA: Dual-Level Continual Instruction Reconciliation with Ongoing Execution for Embodied Robot Agents in Interactive Household Tasks](https://arxiv.org/abs/2610.08862) | 2026 | Qwen3-8B (LLM compiler and conflict judge; no training described); Qwen3-VL-8B f |
| [CLASP: Language-Driven Robot Skill Selection and Composition using Task-Parameterized Learning](https://arxiv.org/abs/2606.08169) | 2026 | Qwen3-VL-32B-Instruct (pretrained, no VLM fine-tuning) |
| [Closing the Affective Loop: Multimodal Speaker-Listener Emotion-Dynamics-Aware Empathetic Social Robots](https://arxiv.org/abs/2608.16686) | 2026 | GPT-4.1-nano (LLM backbone, prompted) |
| [Coding Agents with Harness for Safe Robot Control](https://arxiv.org/abs/2609.20822) | 2026 | GPT-6-Astra coding agent (GPT-5.5 also reported) |
| [CoEnv: Driving Embodied Multi-Agent Collaboration via Compositional Environment](https://arxiv.org/abs/2604.05484) `MA` | 2026 | GPT-5 (VLM planner) and Claude Code (code agent), no training |
| [CommCP: Efficient Multi-Agent Coordination via LLM-Based Communication with Conformal Prediction](https://arxiv.org/abs/2602.06038) `MA` | 2026 | LLaMA3-8B-Instruct (LLM relevance and answers) plus Prismatic-VLM-13B (VLM perce |
| [Contract-Grounded Behavior Tree Synthesis via Coding Agents](https://arxiv.org/abs/2607.12220) | 2026 | Sonnet 4.6 and Gemma4:31b (Ollama), general LLMs as reasoning models inside Clau |
| [Coordinated Control of Multiple Construction Machines Using LLM-Generated Behavior Trees with Flag-Based Synchronization](https://arxiv.org/abs/2602.01041) `MA` | 2026 | GPT-5 (real excavator and dump truck); GPT-5.2 and Claude-Opus-4.6 (simulation) |
| [CORAL: COntextual Reasoning And Local Planning in A Hierarchical VLM Framework for Underwater Monitoring](https://arxiv.org/abs/2603.14786) | 2026 | GPT-5.2 (prompted; selects waypoints from a centroid chain) |
| [CoReLIN: Constraint-based Reasoning for Zero-shot Lifelong Interactive Navigation](https://arxiv.org/abs/2602.20055) | 2026 | Frozen general LLM (GPT-5, Gemini, DeepSeek compared) reasoning over scene graph |
| [D-VLC: Decentralized Vision-Language Collaboration for Heterogeneous Embodied Multi-Robot Systems in Unknown Environments](https://arxiv.org/abs/2607.29009) `MA` | 2026 | Five general VLM backbones: Qwen3.5-Flash, Doubao-Seed-2.1-Pro, Claude-Opus-4-8, |
| [Decentralized LLM-Driven Coordination of Acoustic Robots for Contactless Object Manipulation](https://arxiv.org/abs/2605.29378) `MA` | 2026 | LLM (model not named; prompted semantic parser) + Whisper ASR |
| [Demo: Vision-Language Model-Guided Online Calibration of an Electromagnetic Digital Twin](https://arxiv.org/abs/2610.07081) | 2026 | GPT-5.4 as VLM for material classification and waypoint planning, called online  |
| [Deploying Foundation Models for Embodied Navigation](https://arxiv.org/abs/2609.25666) | 2026 | LLM (unnamed; TAP-LLM) primed with learned transit model, zero-shot |
| [Design and Evaluation of LLM Chaining-Based Task Planning for General Purpose Service Robots](https://arxiv.org/abs/2609.29043) | 2026 | Qwen2.5-14B / Cogito-14B (local) and Claude Sonnet 4.6 (frontier), prompted two- |
| [Dual-Agent Framework for Cross-Model Verified Translation of Natural-Language Protocols into Robotic Laboratory Platform](https://arxiv.org/abs/2606.20120) `MA` | 2026 | GPT-5 (Parser Agent) + Claude Sonnet 4.6 (Validation Agent), prompted |
| [DualManip: Agentic Dynamic Manipulation via Dual-Path Semantic Reasoning and Geometric Adaptation](https://arxiv.org/abs/2609.31112) | 2026 | GPT-5.6 Terra (VLM semantic path; trained correspondence network is a tool) |
| [DuoMind: Enabling Distributed Multi-Robot Coordination with Semantic Communication](https://arxiv.org/abs/2610.02161) `MA` | 2026 | Qwen3-VL-4B-Instruct on each robot (off-the-shelf VLM orchestrator); pi0.5 LoRA- |
| [DynaHarness: A Dynamic Physical Harness for Self-Evolving Robot Agents](https://arxiv.org/abs/2609.40306) | 2026 | Qwen3-VL-4B-Instruct slow brain (off-the-shelf, served locally) plus determinist |
| [DynaHMRC: Decentralized Heterogeneous Multi-Robot Collaboration for Dynamic Tasks with Large Language Models](https://arxiv.org/abs/2606.14882) `MA` | 2026 | GPT-4o prompted (headline); also a fully fine-tuned Qwen3-4B-Instruct variant |
| [EFLUX: Elastic Multi-Robot Formation Navigation and Adaptation with Agentic LLMs](https://arxiv.org/abs/2607.12050) `MA` | 2026 | Gemini-3.1-Pro (LLM backbone for all planning stages) |
| [ELITE: Experiential Learning and Intent-Aware Transfer for Self-improving Embodied Agents](https://arxiv.org/abs/2603.24018) | 2026 | Qwen2.5-VL-72B-Instruct / InternVL3-78B as base VLMs (no fine-tuning) |
| [EmbodiedUS-FS: Fast Slow Intelligence for Ultrasound Robotics](https://arxiv.org/abs/2606.22319) | 2026 | LLaMA3 as base LLM (size unstated; not described as fine-tuned) |
| [EmboTeam: Grounding LLM Reasoning into Reactive Behavior Trees via PDDL for Embodied Multi-Robot Collaboration](https://arxiv.org/abs/2601.11063) `MA` | 2026 | GPT-4o (also Claude-3.5-Sonnet, Llama-3.1) parses instructions into PDDL and pla |
| [EMERGE-Policy: A Robot Mind Emerges Beyond a Single Policy](https://arxiv.org/abs/2608.29896) `MA` | 2026 | Codex (codex-5.6-sol) Main Agent with Sub Agents; VLA and WAM skills (pi0.5, Cos |
| [EmoPose: Vision-Language Model Guided Emotion-Aware Gesture Generation for Humanoid Robots](https://arxiv.org/abs/2609.23414) | 2026 | GPT-5.5 (prompted with in-context demonstrations; no training described) |
| [EndoNav: Semantic-to-Geometric Grounding for Language-Guided Robotic Endoscopic Examination](https://arxiv.org/abs/2608.22093) | 2026 | GPT-4.1 (viewpoint agent, prompted) |
| [Engagement-Aware Agentic Pursuit-Evasion](https://arxiv.org/abs/2607.10986) `MA` | 2026 | Zero-shot LLM planners: Claude Haiku 4.5, GPT-5 Nano, Gemini 2.5 Flash, DeepSeek |
| [ETA: A New Agentic Paradigm for Embodied Tasks](https://arxiv.org/abs/2608.03924) | 2026 | GPT-5.6 Luna / Terra / Sol as Planner (headline Sol, PASS@5 117/130 on LIBERO) |
| [Event-Driven Proactive Assistive Manipulation with Grounded Vision-Language Planning](https://arxiv.org/abs/2603.23950) | 2026 | Qwen3VL-Instruct-32B (cloud VLM with fixed output contract) |
| [Event-Driven Proactive Robot Assistance through Vision-Language Reasoning](https://arxiv.org/abs/2610.08344) | 2026 | Qwen3.5-122B-A10B-FP8 frozen VLM planner (used without task-specific fine-tuning |
| [Evidence-Gated Task and Motion Planning with Vision-Language Models](https://arxiv.org/abs/2608.20084) | 2026 | GPT-5.5 (gpt-5.5-2026-04-23) and Gemini-3.5-Flash as VLMs, prompted |
| [Evolvable Embodied Agent for Robotic Manipulation via Long Short-Term Reflection and Optimization](https://arxiv.org/abs/2604.13533) | 2026 | ChatGPT-4o (environment interpreter and policy planner) with SAM-huge tools |
| [EvolveNav: Proactive Preflection and Self-Evolving Memory for Zero-Shot Object Goal Navigation](https://arxiv.org/abs/2606.18235) | 2026 | Qwen3-8B (frozen LLM for frontier preflection and rule distillation), BLIP-2 vis |
| [EvoMemNav: Efficient Self-Evolving Fine-Grained Memory for Zero-Shot Embodied Navigation](https://arxiv.org/abs/2606.03509) | 2026 | Qwen3-VL-8B (VLM for shortlist selection and Stop verification), training-free |
| [EvoPlan: Evolutionary Neuro-Symbolic Robot Planning with Spatio-Temporal Guarantees](https://arxiv.org/abs/2607.06724) | 2026 | Qwen3-32B (locally hosted open-weight, prompted; gpt-oss-120b in ablation) |
| [ExpressMM: Expressive Mobile Manipulation Behaviors in Human-Robot Interactions](https://arxiv.org/abs/2604.05320) | 2026 | GPT-5.2 (VLM interaction planner); pi0.5 VLA as low-level tool |
| [FARE: Fast-Slow Agentic Robotic Exploration](https://arxiv.org/abs/2601.14681) | 2026 | Qwen3-14B as slow-thinking LLM producing global waypoint paths; RL policy as fas |
| [From Assumptions to Actions: Turning LLM Reasoning into Uncertainty-Aware Planning for Embodied Agents](https://arxiv.org/abs/2602.04326) `MA` | 2026 | GPT-4o mini (also Gemma3:4B, GPT-OSS:20B) prompted as Planner-Composer-Evaluator |
| [From Dialogue to Execution: Mixture-of-Agents Assisted Interactive Planning for Behavior Tree-Based Long-Horizon Robot Execution](https://arxiv.org/abs/2603.01113) `MA` | 2026 | Gemini 2.5 Flash planner (Gemini 2.0 Flash in Exp. 1); MoA expert agents LLM-bas |
| [From Language to Action: Can LLM-Based Agents Be Used for Embodied Robot Cognition?](https://arxiv.org/abs/2603.03148) | 2026 | GPT-4.1, Claude 4 Sonnet, Qwen3 Coder 480B and DeepSeek V3.1 as zero-shot cognit |
| [From Passive Execution to Active Exploration: Agentic Embodied Manipulation in Realistic Environments](https://arxiv.org/abs/2609.29091) | 2026 | OpenClaw agent framework as planner (base LLM/VLM not named) |
| [From Rollout to Reset: A Graph-Based Harness for Autonomous Long-Horizon Manipulation Evaluation](https://arxiv.org/abs/2609.19413) | 2026 | Qwen3.5-397B (task scoring, reset planning, reset verification) over a scene gra |
| [From Social Reasoning to Embodied Interaction: An Agentic Framework for Social Robots](https://arxiv.org/abs/2610.05964) | 2026 | Doubao-Seed-2.1-Pro (reactive planner, memory, social estimator); DeepSeek-V4 (g |
| [FSUNav: A Cerebrum-Cerebellum Architecture for Fast, Safe, and Universal Zero-Shot Goal-Oriented Navigation](https://arxiv.org/abs/2604.03139) | 2026 | Qwen3-VL-32B-Instruct (VLM, via Ollama) for semantic subgoals and verification;  |
| [GAVEL: Graph World Models for Verified and Efficient Long-Horizon LLM Task Planning](https://arxiv.org/abs/2609.19315) | 2026 | Qwen3-8B / Qwen3-4B planner (also GPT-5.6 Sol, Claude Sonnet 5) |
| [Goal2Skill: Long-Horizon Manipulation with Adaptive Planning and Reflection](https://arxiv.org/abs/2604.13942) | 2026 | Pre-trained VLM planner (unnamed, Φ) with diffusion skill library trained by the |
| [Grounding Generative Planners in Verifiable Logic: A Hybrid Architecture for Trustworthy Embodied AI](https://arxiv.org/abs/2602.08373) | 2026 | Gemini-2.5 as LLM apprentice planner (Qwen-72B and Qwen-7B also tested), no trai |
| [GuideFetch: A Task Coordination Framework for Concurrent Navigation and Object Retrieval in Assistive Robot Dogs](https://arxiv.org/abs/2608.18292) `MA` | 2026 | Qwen3.5-4B (local, general LLM) as schedule-conditioned planner for guider and f |
| [HarnessWAM: Bridging Prediction and Deliberation in World Action Models](https://arxiv.org/abs/2608.09516) | 2026 | Qwen3-VL-32B-Instruct as Task Manager (no task-specific fine-tuning); LingBot-VA |
| [Hierarchical Floorplan-Guided Vision-Language Exploration for Embodied Question Answering](https://arxiv.org/abs/2609.26360) | 2026 | GPT-5.5 (prompted high-level planner, real-world; other LLMs/VLMs only in sim) |
| [Hierarchical LLM-Based Multi-Agent Framework with Prompt Optimization for Multi-Robot Task Planning](https://arxiv.org/abs/2602.21670) `MA` | 2026 | GPT-4o as global, type-level and robot-level LLM agents (prompted; only prompts  |
| [Hierarchical Prompting with Dual LLM Modules for Robotic Task and Motion Planning](https://arxiv.org/abs/2605.08330) | 2026 | Llama3.2:70B ReAct task-planning agent plus Llama3.2:70B few-shot placing reason |
| [HiMe: Hierarchical Embodied Memory for Long-Horizon Vision-Language-Action Control](https://arxiv.org/abs/2607.03449) | 2026 | GPT-4o Planner with Qwen3-VL-8B Sentry; fine-tuned pi0.5 Executor used as VLA to |
| [HINT: Human-Intent Inception for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2609.02653) | 2026 | Qwen3-VL-8B-Instruct as task manager, used as-is; trained Pattern Router is a to |
| [HINT-Plan: Human Intention-Aware Robot Task Planning in Context-Rich Environments using Vision Language Models](https://arxiv.org/abs/2609.17771) | 2026 | GPT-5.6-Sol (intention inference and grounding) + FMAP multi-agent planner (symb |
| [HODAgent: Towards On-Demand, Responsive Humanoids for Physical World Human Interaction](https://arxiv.org/abs/2608.17584) | 2026 | Two unspecified VLM backbones inside HODAgent (Env-Interactor, Planner, Executor |
| [HoloAgent-0: A Unified Embodied Agent Framework with 3D Spatial Memory](https://arxiv.org/abs/2606.23565) | 2026 | Unnamed cloud LLM/VLM (no model named; no training described) |
| [Humanoid Whole-Body Manipulation via Active Spatial Brain and Generalizable Action Cerebellum](https://arxiv.org/abs/2605.21133) `MA` | 2026 | Unnamed mainstream VLM for the Brain (benchmark lists GPT-5.1, Gemini 3 Flash, G |
| [HUMEMBR: Learning Human Routines for Predictive Embodied Navigation](https://arxiv.org/abs/2606.30404) | 2026 | Gemini 3 Flash as reasoning model (real-world), with retrieval functions; Qwen3- |
| [Hybrid Framework for Robotic Manipulation: Integrating Reinforcement Learning and Large Language Models](https://arxiv.org/abs/2603.30022) | 2026 | GPT-based LLM (version and size not stated) as task planner; PPO/SAC RL policies |
| [Hybrid LLM-based Intelligent Framework for Robot Task Scheduling](https://arxiv.org/abs/2605.15486) `MA` | 2026 | GPT-4 (generator) + Gemma 3 / LLaMA 4 / Mistral-7B (supervisor), prompting only, |
| [Hypothesis-driven Model Expansion under Uncertainty for Open-World Robot Planning](https://arxiv.org/abs/2607.06501) | 2026 | gpt-4.1-2025-04-14 across all modules (hypotheses, planning, VLM verification);  |
| [IMR-LLM: Industrial Multi-Robot Task Planning and Program Generation using Large Language Models](https://arxiv.org/abs/2603.02669) `MA` | 2026 | GPT-4o (Qwen3-32B-thinking also tested) |
| [Integrated Exploration and Sequential Manipulation on Scene Graph with LLM-based Situated Replanning](https://arxiv.org/abs/2602.04419) | 2026 | Pretrained LLM (model not named) for belief-graph location priors and situated r |
| [IntenBot: Flexible and Imprecise Multimodal Input for LLMs to Understand User Intentions for Casual and Human-Like HRI](https://arxiv.org/abs/2605.04585) | 2026 | GPT-4o (intent disambiguation); builder LLM for behaviour tree (model not named) |
| [Intent at a Glance: Gaze-Guided Robotic Manipulation via Foundation Models](https://arxiv.org/abs/2601.05336) | 2026 | Gemini Pro as default intent VLM; Gemini 2.5 Pro for grasp selection |
| [IROSA: Interactive Robot Skill Adaptation Using Natural Language](https://arxiv.org/abs/2603.03897) | 2026 | Qwen2.5-VL-72B-Instruct as LLM backend selecting and parameterizing skill tools |
| [JOIN: Anchor-Grasp-Conditioned Joining via Opposition, Inference, and Navigation for Bimanual Assistive Manipulation](https://arxiv.org/abs/2606.11151) | 2026 | Gemini Robotics-ER 1.6 (prompted, zero-shot) |
| [KGLAMP: Knowledge Graph-guided Language model for Adaptive Multi-robot Planning and Replanning](https://arxiv.org/abs/2602.04129) `MA` | 2026 | GPT-5 as the base model of all LLM modules (goal, relation, property, reach, PDD |
| [Kinematics-Grounded Agentic AI for Robotic Additive Manufacturing Process Planning](https://arxiv.org/abs/2609.19347) | 2026 | Qwen3-8B (Triage Agent, no task-specific fine-tuning) |
| [KINO: A Keyframe Interface for VLM Planning and Whole-Body Control in Humanoid Loco-Manipulation](https://arxiv.org/abs/2609.18869) | 2026 | Qwen3.6:27B VLM (off-the-shelf) selects keyframes; authors' PPO keyframe-conditi |
| [LabEvolver: Training-Free Experience Evolution for Safe and Grounded Wet-Lab Agents](https://arxiv.org/abs/2607.27690) `MA` | 2026 | DeepSeek-V4-Pro (default backbone, no weight updates) |
| [Leveraging Adaptive Group Negotiation for Heterogeneous Multi-Robot Collaboration with Large Language Models](https://arxiv.org/abs/2602.06967) `MA` | 2026 | GPT-4 (gpt-4-0125-preview), one LLM agent per robot |
| [LLM-Based Agentic Exploration for Robot Navigation & Manipulation with Skill Orchestration](https://arxiv.org/abs/2601.00555) | 2026 | Unnamed general LLM (model not specified) producing direction and store-entry co |
| [LLM-Foraging: Large Language Models for Decentralized Swarm Robot Foraging](https://arxiv.org/abs/2605.01461) `MA` | 2026 | GPT-5-mini (OpenAI Responses API, reasoning low) |
| [LLM-Grounded Dynamic Task Planning with Hierarchical Temporal Logic for Human-Aware Multi-Robot Handover](https://arxiv.org/abs/2602.09472) | 2026 | GPT-4o-mini as instruction-to-H-LTLf grounding engine |
| [LLM-Powered Interactive Robotic Action Synthesis from Multimodal Speech, Gestures, and Music](https://arxiv.org/abs/2606.31158) | 2026 | Qwen3:0.6b via Ollama (off-the-shelf, prompted only) |
| [LLM-VLM Fusion Framework for Autonomous Maritime Port Inspection using a Heterogeneous UAV-USV System](https://arxiv.org/abs/2601.13096) `MA` | 2026 | GPT-4o (benchmarked vs GPT-4, GPT-3.5-Turbo, Gemini, LLaMA-3.3) as symbolic miss |
| [Logic-Based Verification of Task Allocation for LLM-Enabled Multi-Agent Manufacturing Systems](https://arxiv.org/abs/2604.17142) `MA` | 2026 | GPT-5 as product agent generating task plans and robot allocations, with verifie |
| [Long-Term Memory for VLA-based Agents in Open-World Task Execution](https://arxiv.org/abs/2604.15671) `MA` | 2026 | Qwen3-VL-Flash (general VLM planner with sub-agents); Skill-VLA (fine-tuned GR00 |
| [LUCID: An Agentic AI Framework on Digital-Twin in the Loop for QoS-Guaranteeing Robotic Control](https://arxiv.org/abs/2608.28437) | 2026 | Gemini 3.6 Flash as LLM agent, unmodified (Claude Sonnet 5, GPT-4.1 mini/nano, L |
| [MaCoPlanner: LLM-Assisted Manual-Compiled Task Planning with Proactive Safety Verification for Robotic Industrial Panel Operation](https://arxiv.org/abs/2608.28300) | 2026 | gpt-4o via OpenAI API as planner (GPT-5 and Gemma 3 27B-IT compared); e5-base-v2 |
| [MALLVI: A Multi-Agent Framework for Integrated Generalized Robotics Manipulation](https://arxiv.org/abs/2602.16898) `MA` | 2026 | GPT-4.1-mini default backbone, with four LLM agents and a VLM Reflector coordina |
| [Managing Context and Communication in Distributed Agentic UAV Swarms](https://arxiv.org/abs/2610.01569) `MA` | 2026 | Gemma 4 26B A4B IT as each UAV's agent (off-the-shelf, no fine-tuning reported) |
| [MeCo: Enhancing LLM-Empowered Multi-Robot Collaboration via Similar Task Memoization](https://arxiv.org/abs/2601.20577) `MA` | 2026 | DeepSeek-V3 (API) |
| [Melding LLM and temporal logic for reliable human-swarm collaboration in complex scenarios](https://arxiv.org/abs/2605.07877) `MA` | 2026 | Qwen3-8B on each edge tablet (group-level subtask LLM); cloud LTL planner (symbo |
| [Meta-Ctrl: Guaranteed Plan Generation by Decoupling Syntactic and Semantic Constraints](https://arxiv.org/abs/2608.22149) | 2026 | Llama-3-8B-Instruct (main; gpt-oss-20B on EAI, Llama-3.1-8B on WAH-NL) with cons |
| [Mimir: A Neuro-Symbolic Memory System with Dynamic Grounding for Embodied Agents in Interactive Environments](https://arxiv.org/abs/2608.04933) | 2026 | Open-source MLLM backbones (Qwen3-VL, InternVL3, Gemma-3 and others) with Mimir  |
| [MistyPilot: An Agentic Fast-Slow Thinking LLM Framework for Misty Social Robots](https://arxiv.org/abs/2603.03640) `MA` | 2026 | GPT-5-mini (prompted; Task Router, PIA and SIA agents) |
| [MistyPilot: Enabling Social-Robot Control through Multi-Agent LLM Skill Orchestration](https://arxiv.org/abs/2608.15549) `MA` | 2026 | GPT-5-mini backbone for Task Router, PIA and SIA LLM agents |
| [MiTa: A Hierarchical Multi-Agent Collaboration Framework with Memory-integrated and Task Allocation](https://arxiv.org/abs/2601.22974) `MA` | 2026 | GPT-4o / Qwen3-Plus / DeepSeek-V3.1 as manager and member LLMs |
| [MobiAgent: Dual-Loop Recursive Policy Self-Improvement for Long-Horizon Mobile Manipulation](https://arxiv.org/abs/2610.03476) | 2026 | GPT-5.4 (Task Planner and Reflection Critic); skill experts are authors-fine-tun |
| [MoMaStage: Skill-State Graph Guided Planning and Closed-Loop Execution for Long-Horizon Indoor Mobile Manipulation](https://arxiv.org/abs/2603.08383) | 2026 | Qwen3.6 Flash (frozen; ablations Gemini 3.6 Flash and GPT-5.4 nano) |
| [Mosaic: Runtime-Efficient Multi-Agent Embodied Planning](https://arxiv.org/abs/2607.09603) `MA` | 2026 | GPT-4o, Claude Sonnet 4.5 or Gemini 3 Flash as one planner/actor/verifier LLM, p |
| [Multi-Task Visual Perception Network with LLM Conditioning for Autonomous Navigation](https://arxiv.org/abs/2609.14297) | 2026 | Gemini Pro (prompted general LLM) + perception tools (YOLOv8, ESANet, OSNet) and |
| [Multimodal Large Language Models for Real-Time Situated Reasoning](https://arxiv.org/abs/2602.01880) | 2026 | GPT-4o with image and text prompts, step-by-step reasoning, choosing clean / obs |
| [Multimodal-Language-Model–Driven Interaction and Companionship for Service Robots in Elderly-Care Facilities](https://arxiv.org/abs/2608.21387) | 2026 | GPT-4o Realtime API (speech and tool calls); safety VLM model not named |
| [Navi-Agent: Unlocalized Monocular Navigation Agent](https://arxiv.org/abs/2609.20388) | 2026 | General VLM as semantic backbone (Qwen3.6-Plus, GPT-5.6-sol or GPT-5.5 in backbo |
| [Neurosymbolic Embodied Agents](https://arxiv.org/abs/2608.16794) | 2026 | Qwen3.5-4B / 9B / 27B VLM (headline 4B), same model for Phase I exploration and  |
| [Nutri-ATLAS: Embodied Agent for Tabulated Lookup and Assistance for Smarter nutrition](https://arxiv.org/abs/2609.32803) | 2026 | Qwen3.5-9B (4-bit quantized, off-the-shelf) as LLM planner and RAG reasoner |
| [OCC4M: Object-Centric 4D Memory for Spatiotemporal Reasoning in Long-Horizon Manipulation](https://arxiv.org/abs/2609.28798) | 2026 | Gemini 2.5 Flash (prompted, one call per episode; frozen pi0.5-LoRA executor as  |
| [OmniVLN: Omnidirectional 3D Perception and Token-Efficient LLM Reasoning for Visual-Language Navigation across Air and Ground Platforms](https://arxiv.org/abs/2603.17351) | 2026 | Unnamed remote LLM (prompted, zero-shot); Qwen2.5-VL used for edge verification  |
| [On-Device Robotic Planning: Eliminating Inference Redundancy for Efficient Decision-Making](https://arxiv.org/abs/2605.31460) | 2026 | Qwen3-VL-4B-Instruct (off-the-shelf; ALFRED backbone SFT-tuned) |
| [One MLLM, One Call: Efficient Zero-Shot Vision-and-Language Navigation via Spatial-Aware Waypoints](https://arxiv.org/abs/2609.06476) | 2026 | Qwen3-VL-235B as default single MLLM (also GPT-4o, Gemini-2.5-Pro, GPT-5.1), zer |
| [OntoPlan: An Ontology-Grounded Scene Representation and Agentic Framework for Scalable Robot Task Planning](https://arxiv.org/abs/2610.07649) `MA` | 2026 | GPT-4o (gpt-4o-2024-08-06, temperature 0) driving four LLM agents: Flow Orchestr |
| [OpenGo: An OpenClaw-Based Robotic Dog with Real-Time Skill Switching](https://arxiv.org/abs/2604.01708) | 2026 | Unnamed LLM dispatcher inside OpenClaw (model not named) |
| [OptiSight: Bridging Semantic Reasoning and Geometric Control for Embodied Navigation](https://arxiv.org/abs/2608.23354) | 2026 | Qwen3.5-2B (first 12 scenarios) and Moondream2-2B (other 12), zero-shot VLM; Gro |
| [ORCESTRA: VLM-driven Visual Robot programming in Mixed Reality](https://arxiv.org/abs/2608.00775) | 2026 | Qwen3-VL (size not stated, served via vLLM/SGLang) |
| [Organizational Principles Enable Collective Intelligence in Embodied AI](https://arxiv.org/abs/2609.11737) `MA` | 2026 | 8 general LLMs as each agent's base model (ChatGPT-5.4, Gemma-4, Llama-4-Scout,  |
| [OSDAG: Online Scheduling for Efficient Multi-Robot Collaboration](https://arxiv.org/abs/2606.15255) `MA` | 2026 | Gemini Flash (LLM backbone, prompted once per instruction) |
| [PanelShield: Verifiable Closed-Loop Safe Planning for Robotic Industrial Panel Operation](https://arxiv.org/abs/2608.28305) | 2026 | VLM planner (GPT-4o in real-world experiments; simulation VLM unnamed) |
| [PEACE: A Planner-Executor Agent with Constraint Enforcement for UAVs](https://arxiv.org/abs/2606.00104) | 2026 | off-the-shelf LLM (model not named in text) |
| [PerceptTwin: Semantic Scene Reconstruction for Iterative LLM Planning and Verification](https://arxiv.org/abs/2606.04226) | 2026 | GPT-5 / GPT-5 Mini as SMART-LLM planner and LLM judge |
| [Physical Agentic AI: An Architecture for Orchestrating a Robot Crew with LLMs](https://arxiv.org/abs/2608.22657) `MA` | 2026 | gpt-5.4-mini (Mission Planner, temperature 0.1, prompt-grounded on retrieved ski |
| [Plan Along the Way: Event-Triggered Foundation-Model Planning for TAMP Execution in Partially Observable Manipulation](https://arxiv.org/abs/2608.28075) | 2026 | Qwen3-4B/8B/32B LLM and Qwen3-VL-4B/8B/32B-Thinking VLM, zero-shot or ICL prompt |
| [PLanAR: Planning-Language-Grounded Agentic Reasoning for Robot Manipulation](https://arxiv.org/abs/2602.01662) | 2026 | Off-the-shelf VLM backends (Gemini Flash / Gemini 3 Pro, Qwen3-VL-Plus, Claude O |
| [PreAct-Nav: Agentic Reasoning Before Action for Urban Navigation](https://arxiv.org/abs/2610.04916) | 2026 | Qwen3.8-27B frozen VLM reasoner (default; GPT-5.6 Sol also tested) over a frozen |
| [ProAct-VLM: Pre-Failure Vision-Language Task Replanning with Continuous Perception Feedback](https://arxiv.org/abs/2609.37681) | 2026 | Pre-trained VLM as black-box planner; Gemini 2.5 Pro best, also GPT-4o, Claude O |
| [QuadAgent: A Responsive Agent System for Vision-Language Guided Quadrotor Agile Flight](https://arxiv.org/abs/2604.02786) `MA` | 2026 | Qwen-Max, Qwen-Plus, Qwen-VL-Plus, Qwen-VL-Max via API (training-free) |
| [Qumus: Realization of An Embodied AI Quantum Material Experimentalist](https://arxiv.org/abs/2605.18407) `MA` | 2026 | Claude Sonnet 4.6 (showcase run); GPT, Gemini Pro 3, Grok, Qwen, DeepSeek also t |
| [RAVEN: Long-Horizon Reasoning & Navigation with a Visuo-Spatio-Temporal Memory](https://arxiv.org/abs/2606.25206) | 2026 | Gemini-2.5-Flash VLM agent with QQMM-v2 embedder (GPT-5.2, Gemini-3-Pro also tes |
| [Recursive Video In-Context Learning for Agentic Robot](https://arxiv.org/abs/2610.06843) | 2026 | GPT-6 Astra (Codex CLI, low reasoning effort; training-free RV-ICL layer) |
| [RegenHarness: A Robot Agent Harness with Evidence-Gated Recursive Self-Improvement](https://arxiv.org/abs/2609.27612) | 2026 | Qwen3-VL-Plus (VLM goal selection) and Qwen-Plus (task planner), no training rep |
| [RePlan-Bot: Multi-Level Replanning for Embodied Instruction Following](https://arxiv.org/abs/2605.25851) | 2026 | GPT-4o as LLM auditor and location predictor; ViT corrector and detectors are tr |
| [Replanning Human-Robot Collaborative Tasks with Vision-Language Models via Semantic and Physical Dual-Correction](https://arxiv.org/abs/2602.14551) | 2026 | OpenAI o4-mini (zero-shot Action Target selector and verifiers); GPT-5.4-mini in |
| [RoboAssist: Interactive Human-Humanoid Planning for Long-Horizon Surgical Assistance](https://arxiv.org/abs/2609.39384) | 2026 | DeepSeek V4 Pro (task-level decision-making and replanning; no training describe |
| [RoboBRIDGE: A Modular Framework for Bridging Policies to Robust Real-World Robotic Agents](https://arxiv.org/abs/2607.27881) | 2026 | Claude Opus 4.6 (Planner and Phase-2 Monitor); VLA controllers SmolVLA / pi0.5 / |
| [RoboHarness: Memory-Driven Orchestration of Heterogeneous Robot Policies for Long-Horizon Planning](https://arxiv.org/abs/2607.18060) | 2026 | Codex with GPT-5.5 as coding agent orchestrating VLA, WAM, RL and TAMP policies |
| [RoboHarness: A Memory-Augmented Policy Harness for Vision-Language-Action Model Robustness via In-Context Adaptation](https://arxiv.org/abs/2603.24060) | 2026 | Qwen3-VL-32B orchestrator (no fine-tuning) over frozen VLA backbones (pi0, pi0.5 |
| [RoboNav-Arm: Agentic AI-Driven Navigation and Obstacle Avoidance for Robotic Manipulator in Cluttered Environments](https://arxiv.org/abs/2607.09716) | 2026 | Llama-3.1-70B-Instruct (prompted; chosen over DeepSeek-V4-Flash and Qwen-480B-A3 |
| [RoboRouter: Training-Free Policy Routing for Robotic Manipulation](https://arxiv.org/abs/2603.07892) `MA` | 2026 | GPT-4o (Router, Evaluator, Retriever VLM) |
| [RoboSolver: A Multi-Agent Large Language Model Framework for Solving Robotic Arm Problems](https://arxiv.org/abs/2602.14438) `MA` | 2026 | GPT-4o / DeepSeek-V3.2 / Claude-Sonnet-4.5 (Gemini 2.5 Pro as VLM), prompted wit |
| [RoboStream: Weaving Spatio-Temporal Reasoning with Memory in Vision-Language Models for Robotics](https://arxiv.org/abs/2603.12939) | 2026 | Qwen3-VL-8B / 32B / 235B (prompted, no fine-tuning) |
| [RobotUse: Allocating Computation, Context, and Decisions](https://arxiv.org/abs/2610.04929) | 2026 | Gemini-3.8-Flash (main agent and subagents, the evaluation-setup language model) |
| [ROSClaw: A Hierarchical Semantic-Physical Framework for Heterogeneous Multi-Agent Collaboration](https://arxiv.org/abs/2604.04664) `MA` | 2026 | Unnamed VLM/LLM API inside a single unified agent (model not named) |
| [RT-SHCUA: Real-Time Self-Hosted Computer-Use Agent for UAV Control](https://arxiv.org/abs/2607.17951) | 2026 | Qwen-Max via OpenClaw-style SHCUA (temperature 0), off-the-shelf |
| [Safe Multi-Robot Coordination via VLM–LLM Reasoning and Reachability Analysis](https://arxiv.org/abs/2609.27816) `MA` | 2026 | Qwen3 (LLM) + Qwen2.5-VL (VLM), both via Ollama, sizes not stated |
| [SafePilot: A Framework for Assuring LLM-enabled Cyber-Physical Systems](https://arxiv.org/abs/2603.21523) | 2026 | GPT-4o and GPT-3.5-turbo (prompted, with formal verifier loop) |
| [SAGE: Symbolic Action-Gating and Editing for LLM Task Planners](https://arxiv.org/abs/2609.34268) | 2026 | Five open-weight Ollama LLMs (llama3.2 3B to qwen2.5 14B), single planner |
| [SAGE-Nav: Leveraging LLM Planning and Alignment Fusion for Hierarchical Scene Graph-Guided Navigation](https://arxiv.org/abs/2606.25497) | 2026 | Qwen2.5-VL-7B frozen global planner plus A3C-trained HSGE/LSTM policy |
| [SAIN: Structure-Aware Interactive Navigation with Active Dialogue Grounding for Mobile Robot](https://arxiv.org/abs/2608.09196) | 2026 | Qwen3.5 (general VLM for multimodal reasoning) plus GroundingDINO / MobileSAM as |
| [Say the Mission, Execute the Swarm: Agent-Enhanced LLM Reasoning in the Web-of-Drones](https://arxiv.org/abs/2605.03788) `MA` | 2026 | GPT-5.2, DeepSeek V3.2, GLM 4.7, Grok 4.1 Fast, Claude Haiku 4.5, Qwen3 8B (each |
| [Scaffolding Foundation Models into Physical-World Agents Pushes the Frontier of Long-Horizon Navigation](https://arxiv.org/abs/2608.30396) | 2026 | Qwen3.6-Plus VLM agent (Qwen3.5-397B-A17B in ablations); Qwen-RobotNav-8B execut |
| [Scale-Plan: Scalable Language-Enabled Task Planning for Heterogeneous Multi-Robot Teams](https://arxiv.org/abs/2603.08814) `MA` | 2026 | GPT-5.2 (prompted; decomposition, allocation and plan integration) |
| [Search, Ground, Plan: Functional Sufficiency for Task and Motion Planning under Incomplete Scene Knowledge](https://arxiv.org/abs/2609.23113) | 2026 | Qwen3.5-9B (no fine-tuning reported; FM for spec and inspection order) |
| [Self-Evolving Coding Agents: From Digital Programs to Physical-World Intelligence](https://arxiv.org/abs/2609.35432) | 2026 | GPT-5.6-Sol (HexaAnything planner; also GPT-6-Astra and Qwen3.8-27B; the fine-tu |
| [Sentinel: Embodied Cooperative Spatial Reasoning and Planning](https://arxiv.org/abs/2605.26239) `MA` | 2026 | gpt-4o (backbone for all agents; Qwen3-VL-30B-A3B as ablation) |
| [Sequential Planning via Anchored Robotic Keypoints](https://arxiv.org/abs/2606.30613) | 2026 | Gemini 3.1 Pro (sim) / Gemini 3.5 Flash (hardware) writes behavior tree; SAM3 pe |
| [SFCo-Nav: Efficient Zero-Shot Visual Language Navigation via Collaboration of Slow LLM and Fast Attributed Graph Alignment](https://arxiv.org/abs/2603.01477) | 2026 | GPT-4o slow LLM planner plus non-LLM fast navigator using Grounding-DINO as a de |
| [SG-CoT: An Ambiguity-Aware Robotic Planning Framework using Scene Graph Representations](https://arxiv.org/abs/2603.18271) `MA` | 2026 | gemini-2.5-flash (also Qwen3-VL-2B-Instruct) as LLM planner with scene-graph ret |
| [SHRIMP: Iterative Refinement of Robot Task Plans](https://arxiv.org/abs/2608.08884) | 2026 | GPT 5.1 prompted to generate hierarchical primitive plans (no training described |
| [SkySim: A ROS2-based Simulation Environment for Natural Language Control of Drone Swarms using Large Language Models](https://arxiv.org/abs/2602.01226) `MA` | 2026 | Gemini 3.5 Pro via cloud API, system instruction only (no training) |
| [SOR-Nav: Search or Relocate? Context-Gated Exploration and Cross-Region Relocation for Object Navigation](https://arxiv.org/abs/2609.34707) | 2026 | LLM not named in paper (unnamed LLM supervisor) |
| [SparseNav: Instruction-conditioned Sparse Semantic Perception for Training-Free Vision-Language Navigation](https://arxiv.org/abs/2609.26408) | 2026 | GPT-5 (prompted, training-free; SAM 3 and classical planner as tools) |
| [Spatial and Semantic Reasoning for LLM-Driven Robot Navigation via MCP](https://arxiv.org/abs/2609.27340) | 2026 | Claude Sonnet 4.6 and GPT-5.5 (off-the-shelf LLM backends via MCP; no training) |
| [StageCraft: Execution Aware Mitigation of Distractor and Obstruction Failures in VLA Models](https://arxiv.org/abs/2603.20659) | 2026 | Gemini 3.1 Pro VLM as in-context planner (gemini-2.5-pro and gpt-5.2-pro ablatio |
| [STeP: Signal Temporal Logic for Precise Specifications for Action Generation with Vision Language Models](https://arxiv.org/abs/2607.18580) | 2026 | GPT-5.4 (VLM formalizer, prompted) |
| [STEP: State-Aware Task Estimation and Planning with Multi-Modal LLMs for Human-Robot Collaboration](https://arxiv.org/abs/2608.27225) | 2026 | GPT-4o via OpenAI API (in-context prompting, main results); GPT-4o mini, GPT-4.1 |
| [Stop Wandering: Efficient Vision-Language Navigation via Metacognitive Reasoning](https://arxiv.org/abs/2604.02318) | 2026 | GPT-4o as navigation VLM (frontier scoring) and reflection LLM; YOLOv8x-World an |
| [StretchBot: A Neuro-Symbolic Framework for Adaptive Guidance with Assistive Robots](https://arxiv.org/abs/2604.00628) | 2026 | DeepSeek-R1-0528-Qwen3-8B via OpenRouter (plus KG retrieval) |
| [Structured World-State Reasoning for Agentic Robotic Search](https://arxiv.org/abs/2609.23841) `MA` | 2026 | Inkling-Small-NVFP4 (frozen multimodal MoE, 276B total / 12B active) as Reasoner |
| [SysNav: Multi-Level Systematic Cooperation Enables Real-World, Cross-Embodiment Object Navigation](https://arxiv.org/abs/2603.06914) | 2026 | Gemini-2.5-flash (prompted; room-level decisions) |
| [TADreamer: Zero-Shot Language-Guided 3D Navigation for Terrestrial-Aerial Bimodal Robots via Video Imagination](https://arxiv.org/abs/2609.19824) | 2026 | ChatGPT Sol-5.6 (prompted, zero-shot; Wan2.7 video model as tool) |
| [Task Planning for Mobile Manipulation in Retail Stores using Foundation Models with Iterative Re-planning](https://arxiv.org/abs/2607.09962) | 2026 | Mixtral 8x22B (LLM) and Pixtral 12B (VLM), off-the-shelf |
| [Task-Aware Positioning for Improvisational Tasks in Mobile Construction Robots via an AI Agent with Multi-LMM Modules](https://arxiv.org/abs/2603.22903) | 2026 | GPT-4o as the LMM in the agent core, navigation and positioning modules |
| [TiPToP: A Modular Open-Vocabulary Robot Manipulation System That Plans](https://arxiv.org/abs/2603.09971) | 2026 | Gemini Robotics-ER 1.5 (prompted; one call for detection and symbolic goal) |
| [Towards Zero-Knowledge Task Planning via a Language-based Approach](https://arxiv.org/abs/2601.03398) | 2026 | GPT-4o (off-the-shelf, no fine-tuning) decomposing subtasks and generating behav |
| [TypeGo: An OS Runtime for Embodied Agents](https://arxiv.org/abs/2607.05482) `MA` | 2026 | GPT-5.4 on all planning layers; GPT-OSS-120B (Groq) on S1P fast path |
| [UAVGENT: A Language-Guided Distributed Control Framework](https://arxiv.org/abs/2602.13212) `MA` | 2026 | Unnamed LLM supervisor (model not specified; prompted) for drone swarm reference |
| [Uni-LaViRA: Language-Vision-Robot Actions Translation for Unified Embodied Navigation](https://arxiv.org/abs/2605.27582) | 2026 | Gemini-3.1-Pro (Language Action Model) and Qwen3.5-27B (Vision Action Model), ze |
| [UniManip: General-Purpose Zero-Shot Robotic Manipulation with Agentic Operational Graph](https://arxiv.org/abs/2602.13086) | 2026 | Qwen-3-VL-4B (high-level decomposition and verification VLM) |
| [Visual-Language-Guided Task Planning for Horticultural Robots](https://arxiv.org/abs/2601.11906) | 2026 | GPT-4.1 as zero-shot VLM agent via OpenAI API with tool calling |
| [ViTL: Temporal Logic-Guided Zero-Shot Natural Language Navigation via Vision-Language Models](https://arxiv.org/abs/2606.30696) | 2026 | LLaVA-NeXT-34B (VLM, 8-bit, no fine-tuning) for frontier scoring; GPT-5.2 compil |
| [VLM-DEWM: Dynamic External World Model for Verifiable and Resilient Vision-Language Planning in Manufacturing](https://arxiv.org/abs/2602.15549) | 2026 | Gemini 2.5 Pro as core VLM (GPT-5, Qwen3-VL-32B, GLM-4.5V as baselines) |
| [VoLo: A Physical Orchestrator for Open-Vocabulary Long-Horizon Manipulation](https://arxiv.org/abs/2606.07723) | 2026 | Claude Opus 4.6 (VLM orchestrator; GPT-5.5, Gemini 2.5 Flash, Qwen3-VL-8B as alt |
| [Walk With Me: Long-Horizon Social Navigation for Human-Centric Outdoor Assistance](https://arxiv.org/abs/2604.26839) | 2026 | High-Level VLM (unnamed in main system; ablated with GPT-5, Claude, Gemini, MiMo |
| [When Robots Do the Chores: A Benchmark and Agent for Long-Horizon Household Task Execution](https://arxiv.org/abs/2605.14504) | 2026 | GPT-5 (headline) and Qwen3-VL-2B/8B/32B backbones of the HoloMind agent |
| [Where Memory Belongs: Ledger, an Object Ledger for Memory-Augmented VLAs](https://arxiv.org/abs/2609.34554) | 2026 | Claude Sonnet 5 planner (prompted) over object ledger; fine-tuned pi0.5 VLA as e |
| [World Action Planner: Generalizable Robot Decision-Making with Action-Conditioned World Models](https://arxiv.org/abs/2607.27599) | 2026 | Gemini 3.0 Flash (VLM agent); Wan-T2V-1.3B world model and diffusion policy as t |
| [World-Model-Grounded LLM Planning for AUV and ASV Navigation Near Offshore Wind Farms](https://arxiv.org/abs/2608.19661) | 2026 | gemma4:26b (general LLM via Ollama, outputs macro-action sequence) |
| [Y-BotFrame: An Extensible Embodied Agent Framework for Quadruped Robot Assistants](https://arxiv.org/abs/2606.13049) | 2026 | Single LLM task planner (model not named; Qwen3-VL-Flash only for scene descript |
| [Zero-shot adaptable task planning for autonomous construction robots: a comparative study of lightweight single and multi-AI agent systems](https://arxiv.org/abs/2601.14091) `MA` | 2026 | Llama 3-8B (primary LLM) and MiniCPM-2.6-7B (primary VLM) as CrewAI agents in on |
| [Zero-shot Interactive Perception](https://arxiv.org/abs/2602.18374) | 2026 | GPT-4o as Perception Analyser and memory-guided action policy |
| [ZeroDex: Zero-Shot Long-Horizon Dexterous Manipulation via Multi-View 3D-Grounded VLM Reasoning](https://arxiv.org/abs/2606.19340) | 2026 | Gemini Robotics-ER 1.6 (gemini-robotics-er-1.6-preview), prompted zero-shot |

</details>

<details><summary><b>Controller · Policy writing</b> (49)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [A Few Words Go a Long Way: Language Guided Robot Policy Synthesis](https://arxiv.org/abs/2607.23784) | 2026 | Claude Opus 4.6 (orchestrator) |
| [A Schema Bounded Language Model for Refining Robot Policies Without Destabilizing Local Learning](https://arxiv.org/abs/2609.05133) `MA` | 2026 | Llama-3.3-70B-Instruct (quantized), Phi-4, Llama-3.1-70B-Instruct (quantized), o |
| [Adaptive Code Generation for Controlling Robots](https://arxiv.org/abs/2610.09588) | 2026 | Qwen3.5-122B-A10B / GPT-5-nano / Kimi-K2.5 (LLM cognition) + Qwen3-VL-8B-Instruc |
| [AeroEval: Staged Program and Execution Validation for AI-Generated Drone Missions](https://arxiv.org/abs/2610.09764) | 2026 | o3-mini for generation and validation (default); Gemini-3.1-Pro as sensitivity c |
| [AeroGen: Agentic Drone Autonomy through Single-Shot Structured Prompting & Drone SDK](https://arxiv.org/abs/2603.14236) | 2026 | GPT o3-mini by default (also Gemini 2.5 Pro, Llama3-70B, DeepSeek-Qwen-32B) |
| [APPROVE: Visual End-User-in-the-Loop Robot Programming with LLMs](https://arxiv.org/abs/2608.19281) | 2026 | GPT-5 (OpenAI API, prompted) |
| [Assisting for Open-Ended Tasks: Goal-Oriented Shared Autonomy as a Particle Filter](https://arxiv.org/abs/2609.32576) | 2026 | GPT-OSS-120B (off-the-shelf LLM): goal-set transition model and skill-code write |
| [AtomBridge: Agentic VLA Inference Plugin for Long-Horizon Tasks in Scientific Experiments](https://arxiv.org/abs/2602.09430) | 2026 | Qwen3.5-397B-A17B planning and coding agents (GPT-5.2 also tested) |
| [Auto-HSI: Personalized human control of a robot swarm on demand by using LLMs for online automatic code generation](https://arxiv.org/abs/2609.16346) `MA` | 2026 | DeepSeek v4 Pro / v4 Flash and Gemma 4 31B via OpenRouter (personalization-time  |
| [Automating Manual Tasks through Intuitive Robot Programming and Cognitive Robotics](https://arxiv.org/abs/2604.05978) | 2026 | unnamed LLM (no model named; prompted with function documentation) |
| [Bayesian Active Learning for Intent Disambiguation in Interactive Robot Planning](https://arxiv.org/abs/2609.34270) | 2026 | GPT-5.4 / Gemini-3.1 / Claude-4.6 LLMs as-is + Gaussian process and grammar VAE  |
| [Bidirectional Human-Robot Communication for Physical Human-Robot Interaction](https://arxiv.org/abs/2601.10796) | 2026 | GPT-4.1 with a structured zero-shot prompt (no fine-tuning) |
| [Bounding Boxes as Goals: Language-Conditioned Grasping via Neuro-Symbolic Planning](https://arxiv.org/abs/2606.12910) | 2026 | GPT-5.2 (goal-state parser); GroundingDINO detector as tool |
| [CodeGraphVLP: Code-as-Planner Meets Semantic-Graph State for Non-Markovian Vision-Language-Action Models](https://arxiv.org/abs/2604.22238) | 2026 | GPT-5 writes a Python planner once per task; π0 VLA executor fine-tuned by the a |
| [Confusion-Aware In-Context-Learning for Vision-Language Models in Robotic Manipulation](https://arxiv.org/abs/2603.15134) | 2026 | GPT-4o (VLM perception inside Instruct2Act code pipeline; Gemini 1.5 Pro, Qwen2- |
| [CoRAL: Contact-Rich Adaptive LLM-based Control for Robotic Manipulation](https://arxiv.org/abs/2605.02600) | 2026 | GPT-4o (VLM and LLM, zero-shot; FoundationPose and MPPI as tools) |
| [Cross-Domain Demo-to-Code via Neurosymbolic Counterfactual Reasoning](https://arxiv.org/abs/2603.18495) | 2026 | GPT-5 with stage-specific prompting plus a symbolic PDDL-style verifier |
| [Efficient Skill Grounding via Code Refactoring with Small Language Models](https://arxiv.org/abs/2606.07999) | 2026 | Qwen2.5-Coder-7B (off-the-shelf sLM, default, prompted and used for localized FI |
| [Embedding Large Language Models into Flow Controls: An Agentic Framework for Adaptive and Trustworthy Automated Cooking](https://arxiv.org/abs/2608.04768) `MA` | 2026 | Unnamed general LLMs (not fine-tuned) as recipe-to-code agents; LoRA-tuned LLM f |
| [EmboAlign: Aligning Video Generation with Compositional Constraints for Zero-Shot Manipulation](https://arxiv.org/abs/2603.05757) | 2026 | VLM (model not named in paper) writes keypoint constraints; VGM Wan2.2/LVP; V-JE |
| [Explore, Execute, Evolve: A Skill Acquisition and Reuse Loop for Embodied Agents](https://arxiv.org/abs/2609.37810) | 2026 | GPT-6 Astra / GPT-5.6 Sol / Fable 5.1 / Opus 5 (general agents writing code) |
| [From Language to Task Maps: Compiling Semantic Relations While Preserving Task-Relevant Freedom](https://arxiv.org/abs/2609.34412) | 2026 | gpt-5.6-sol as language planner writing Semantic Topology JSON (compiler is non- |
| [From Local Corrections to Generalized Skills: Improving Neuro-Symbolic Policies with MEMO](https://arxiv.org/abs/2603.04560) | 2026 | gemini-3-flash-preview (LLM policy writing skill code) |
| [Generalizing Manipulation Skills with a Local Coding Agent](https://arxiv.org/abs/2609.26499) | 2026 | Qwen3.8-27B (local open-weight VLM in pi coding-agent harness) |
| [Give me scissors: Collision-Free Dual-Arm Surgical Assistive Robot for Instrument Delivery](https://arxiv.org/abs/2603.02553) | 2026 | Unnamed general VLM, zero-shot (model not named in available text) |
| [Intelligent Multi-UAV Navigation in ITNTNs: A Hierarchical LLM Approach](https://arxiv.org/abs/2607.18604) `MA` | 2026 | Qwen3.5-122B (HAPS meta-controller) + Qwen3.5-9B 4-bit (per-UAV edge agents), ze |
| [InterEvolve: Test-Time Evolution of Reward Programs for Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.02196) | 2026 | DeepSeek-V4-Flash (LLM agent writing reward programs with weights fixed; the FB  |
| [Interpreting Context-Aware Human Preferences for Multi-Objective Robot Navigation](https://arxiv.org/abs/2603.17510) | 2026 | Gemini 2.0 Flash (VLM context) plus LLM rule updater and preference translator |
| [La Agente Óptima: Towards Agentic Self-Driving Laboratories](https://arxiv.org/abs/2609.04564) | 2026 | GPT-5.5 coordinating agent with GPT-5.4 BO-specialist subagent (BO-MCP / BayBE o |
| [Language-Guided Terrain-Adaptive Neural MPC for Autonomous Traversal of Articulated Tracked Robots](https://arxiv.org/abs/2609.13083) | 2026 | Qwen-Plus (DashScope) edits MPC weights, bounds and soft constraints; trained-ki |
| [LENS: LLM-guided Environment Simplification for Planning and Control in Clutter](https://arxiv.org/abs/2607.19633) | 2026 | GPT-4o (zero-shot VLM scene abstraction, re-prompted on failure) |
| [LMPath: Language-Mediated Priors and Path Generation for Aerial Exploration](https://arxiv.org/abs/2605.13782) | 2026 | GPT-4o-mini (LLM semantic labels) with SAM 3 (segmentation tool) |
| [Low-Burden LLM-Based Preference Learning: Personalizing Assistive Robots from Natural Language Feedback for Users with Paralysis](https://arxiv.org/abs/2604.01463) | 2026 | Gemini 2.5 Flash (clinical reasoning, policy mapping) and GPT-5.1 (LLM judge), u |
| [ManiSkillFormer: Demonstration-Free Compositional Manipulation via Geometric Contracts and Agentic Skill Graph](https://arxiv.org/abs/2609.16331) | 2026 | GPT-5.6-Sol contract and skill-template agents (plus GPT-5.6-Sol 2D keypoints) o |
| [ModuLoop: Low-Level Code Generation Using Modular Synthesizer and Closed-Loop Debugger for Robotic Control](https://arxiv.org/abs/2606.03047) | 2026 | GPT-4o (pre-trained, no fine-tuning; GPT-4.1-mini and Gemini also tested) |
| [Multi-modal Interactive Control of Robotic Arm based on Offline Large Language Models*](https://arxiv.org/abs/2608.08183) | 2026 | ChatGLM2-6B (open-source, self-deployed, prompted for code generation; 6.2B para |
| [NavPatch: Evidence-Guided Object-Level Costmap Correction with Vision-Language Models](https://arxiv.org/abs/2609.14543) | 2026 | Qwen3-VL-Flash (periodic scene proposals at 0.2 Hz) |
| [OrbitTAMP: Grounding Language Models for Task and Motion Planning in Spacecraft Rendezvous](https://arxiv.org/abs/2610.01093) | 2026 | GPT-5.6 Terra (frontier), Qwen3.5-9B and Ministral-8B as intent parsers feeding  |
| [PhotoAgent: A Robotic Photographer with Spatial and Aesthetic Understanding](https://arxiv.org/abs/2603.22796) | 2026 | GPT-4.1 as central LMM reasoning engine (CoT prompting + tools) |
| [PhysCaP: Grounding Code-as-Policy Agent with Physics-Informed Exploration](https://arxiv.org/abs/2608.21031) `MA` | 2026 | Gemini 3.1 Pro (Planner, Prioritizer and coding agents); Molmo2 for object groun |
| [RECAST: Recasting Vision-Language Semantics into an Actionable Cost Map for Robot Navigation](https://arxiv.org/abs/2609.32595) | 2026 | Gemini 3.5 Flash-Lite (VLM) + trained trajectory decoders (SCAND/GND/Vision60 da |
| [RelAfford6D: Relational 6D Affordance Graphs for Constraint-Driven Robotic Manipulation](https://arxiv.org/abs/2606.27036) | 2026 | Unnamed LLM (RAG-prompted, not named in paper), one-shot topology query |
| [RoboCritics: Enabling Reliable End-to-End LLM Robot Programming through Expert-Informed Critics](https://arxiv.org/abs/2603.06842) | 2026 | gpt-4o (program generation; text-embedding-ada-002 for RAG) |
| [Safe and Interpretable Multimodal Path Planning for Multi-Agent Cooperation](https://arxiv.org/abs/2602.19304) `MA` | 2026 | Gemini 3 Pro as best VLM (GPT-5.2, Claude Opus 4.5, Qwen2.5-72B also tested; fin |
| [SkillComposer: Learning Reusable Skills for Natural-Language Robot Programming](https://arxiv.org/abs/2608.14944) | 2026 | Unnamed coder LLM plus evaluator LLM (no model named; no training described) |
| [Skills in Weights, Memory in Code: Hybrid Learning for Memory-Dependent Robot Manipulation](https://arxiv.org/abs/2608.09410) | 2026 | Claude Opus 4.8 coding agent steering a fine-tuned pi0.5 VLA; Qwen3-VL-8B as ver |
| [The Robot’s Inner Critic: Self-Refinement of Social Behaviors through VLM-based Replanning](https://arxiv.org/abs/2603.20164) | 2026 | GPT-4o as both VLM and LLM (temperature 0), MuJoCo robot models |
| [V2-STRep: VLM-Grounded Structured Task Representations for Reusable Robot Skills Acquired from Generated Videos](https://arxiv.org/abs/2609.20582) | 2026 | GPT-6 Astra (VLM infers task representation; Wan 2.7 video generator) |
| [VLCP: Vision Language Control Policy Closed-Loop Code Replanning for Robot Manipulation](https://arxiv.org/abs/2608.16978) | 2026 | GPT-5.5 (frozen, replanning model) |

</details>

<details><summary><b>Controller · Direct action</b> (36)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [A.D.A.M.O. (Agent for language-Driven Actions with Multimodal Observations): A Visual-Symbolic Framework for Virtual Humans](https://arxiv.org/abs/2609.35463) | 2026 | GPT-4o-vision与Claude-Sonnet-3.5等预训练VLM，提示加工具调用，论文未做微调 |
| [ActionReasoning: Robot Action Reasoning in 3D Space with LLM for Robotic Brick Stacking](https://arxiv.org/abs/2602.21161) `MA` | 2026 | Unnamed off-the-shelf LLM as six prompted agents |
| [BrainMem: Brain-Inspired Evolving Memory for Embodied Agent Task Planning](https://arxiv.org/abs/2604.16331) | 2026 | GPT-4o / Claude-3.5-Sonnet / Gemini-1.5-Pro planners; Qwen2.5-VL-72B-Instruct fo |
| [CLOSER-VLN: Closed-Loop Self-Verified Retrieval-Augmented Reasoning for Aerial Vision-Language Navigation](https://arxiv.org/abs/2606.28397) | 2026 | GPT-4o (frozen hierarchical reasoner) + fine-tuned Qwen3-VL-8B as action verifie |
| [CMMR-VLN: Vision-and-Language Navigation via Continual Multimodal Memory Retrieval](https://arxiv.org/abs/2603.07997) | 2026 | GPT-4o (backbone LLM) |
| [Dive into the Scene: Breaking the Perceptual Bottleneck in Vision-Language Decision Making via Focus Plan Generation](https://arxiv.org/abs/2606.04046) | 2026 | Qwen2.5-VL-7B/32B-Instruct-AWQ, gpt-4o-mini, gemini-2.5-flash (prompted focus-pl |
| [FineCog-Nav: Integrating Fine-grained Cognitive Modules for Zero-shot Multimodal UAV Navigation](https://arxiv.org/abs/2604.16298) | 2026 | Qwen2.5-VL-32B (VLM) + Qwen2.5-72B-Instruct (LLM), zero-shot prompting |
| [Global Commander and Local Operative: A Dual-Agent Framework for Scene Navigation](https://arxiv.org/abs/2602.18941) `MA` | 2026 | GPT-4o for both Global Commander and Local Operative |
| [In-Context Robot Learning with VLM Agents](https://arxiv.org/abs/2609.19138) | 2026 | GPT-6 Astra (off-the-shelf VLM, parameters fixed, prompting and context only) |
| [IROS: A Dual-Process Architecture for Real-Time VLM-Based Indoor Navigation](https://arxiv.org/abs/2601.21506) | 2026 | Gemma3-4B VLM as System Two reasoner; segmentation and OCR perception as System  |
| [Know Your Body: A Harness for Direct and Self-Improving Robot Control with VLMs](https://arxiv.org/abs/2609.28530) | 2026 | GPT-6 (frozen weights, high reasoning effort) |
| [Language Movement Primitives: Grounding Language Models in Robot Motion](https://arxiv.org/abs/2602.02839) | 2026 | GPT-5.2 (DMP weight generator) with Gemini Robotics-ER 1.5 (decomposer and objec |
| [LAPF: LLM-Agent-Based Path Finder Using the UAVScenes Dataset](https://arxiv.org/abs/2608.15175) | 2026 | Qwen2-VL-7B-Instruct (off-the-shelf VLM, prompting + memory + tools) |
| [Learning to Retrieve Navigable Candidates for Efficient Vision-and-Language Navigation](https://arxiv.org/abs/2602.15724) | 2026 | Qwen3-8B as-is with retrieved exemplars and imitation-trained candidate pruner |
| [LightZeroNav: Zero-Shot Vision Language Navigation in Continuous Environments Based on Lightweight VLMs](https://arxiv.org/abs/2603.16947) | 2026 | Qwen3-VL-8B backbone (also 4B and 32B; GPT-4o baseline) |
| [MA-CoNav: A Master-Slave Multi-Agent Framework with Hierarchical Collaboration and Dual-Level Reflection for Long-Horizon Embodied VLN](https://arxiv.org/abs/2603.03024) `MA` | 2026 | GPT-5.2 Pro for observation MLLM and GPT-4-Turbo LLM via cloud API |
| [MemCompiler: Compile, Don't Inject - State-Conditioned Memory for Embodied Agents](https://arxiv.org/abs/2605.07594) | 2026 | Frozen general executor (Qwen-2.5-14B, Qwen3.5-27B, Qwen-VL-32B, GPT-5.2, Gemini |
| [MerNav: A Highly Generalizable Memory-Execute-Review Framework for Zero-Shot Object Goal Navigation](https://arxiv.org/abs/2602.05467) | 2026 | Qwen3-vl-plus (main; GPT-5.2 and Gemini 1.5 Pro also tested), prompted without t |
| [MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation](https://arxiv.org/abs/2609.38078) | 2026 | Qwen3.8-Flash-Next VLM as-is (GPT-6 Sol as stronger backbone) |
| [NavHarness: Towards Lifelong Embodied Navigation](https://arxiv.org/abs/2609.34276) | 2026 | Qwen3.8-27B / GPT-4o / Opus 5 / GPT-6 Astra as training-free reasoning cores |
| [NavHarness: Adaptive Goals for Agentic Vision-Language Navigation](https://arxiv.org/abs/2609.39915) `MA` | 2026 | GPT-6-Astra (closed-source backbone, prompted; GPT-5.6-Sol and Qwen-3.6-plus als |
| [Parse, Search, and Confirmation: Training-Free Aerial Vision-and-Dialog Navigation with Chain-of-Thought Reasoning and Structured Spatial Memory](https://arxiv.org/abs/2607.11529) | 2026 | Qwen-VL-Max (search and confirmation CoT) and DeepSeek-V3 (instruction parsing), |
| [Personalizing Embodied Multimodal Large Language Model Agents over Long-term User Interactions](https://arxiv.org/abs/2605.26256) | 2026 | Qwen3-VL-8B-Instruct / Qwen2.5-VL-8B-Instruct / GPT-5 / GPT-4o-mini / Gemini-2.5 |
| [RACAS: Controlling Diverse Robots With a Single Agentic System](https://arxiv.org/abs/2603.05621) `MA` | 2026 | GPT-4.1 / GPT-4.1-mini (Controller, Monitors, Memory Curator) |
| [Real-Time Synchronized Interaction Framework for Emotion-Aware Humanoid Robots](https://arxiv.org/abs/2601.17287) | 2026 | Qwen LLM (size not stated) for response text and NAO gesture keyframe code; Sens |
| [Robo-Cortex: A Self-Evolving Embodied Agent via Dual-Grain Cognitive Memory and Autonomous Knowledge Induction](https://arxiv.org/abs/2605.18729) | 2026 | Qwen2.5-VL-72B-Instruct-AWQ for planning, memory and AKI; Wan2.1 as imagination  |
| [Robo-Harness K1: Harnessing Robot-Use Agents via Perception Augmentation](https://arxiv.org/abs/2609.29389) | 2026 | Gemini 3.7 Flash + Robo-Harness K1 (frozen); GPT-6 Astra + K1 |
| [RoboICL: Embodied In-Context Learning with GPT-6 Astra](https://arxiv.org/abs/2609.34261) | 2026 | GPT-6 Astra (frozen, prompted with demonstrations and interaction memory) |
| [ROSClaw: An OpenClaw ROS 2 Framework for Agentic Robot Control and Interaction](https://arxiv.org/abs/2603.26997) | 2026 | Claude Opus 4.6 / GPT-5.2 / Gemini 3.1 Pro / Llama 4 Maverick (one backend per t |
| [SAGE-LLM: Towards Safe and Generalizable LLM Controller with Fuzzy-CBF Verification and Graph-Structured Knowledge Retrieval for UAV Decision](https://arxiv.org/abs/2602.23719) | 2026 | Unnamed general LLM backbone (Qwen-max, DeepSeek Chat, GLM-4.5, Qwen3 series tes |
| [SpaceVLN: A Zero-Shot Vision-and-Language Navigation Agent with Online Spatial Cognitive Memory and Reasoning](https://arxiv.org/abs/2606.08992) | 2026 | Qwen3.5-Plus (planner) and Qwen3.5-Flash (executor); GroundingDINO for landmark  |
| [Structured LLM Reasoning for Zero-Shot Human--Robot Coordination Under Hidden Goals](https://arxiv.org/abs/2608.04309) | 2026 | GPT-5.4 nano (hierarchical planner, ToM inference, replanning); gpt-4.1-nano (in |
| [TacZero: Training-Free Peg Insertion Using a General-Purpose Vision-Language Model with Tactile Feedback](https://arxiv.org/abs/2610.07621) | 2026 | GPT-6 Astra (primary; Claude Fable 5.1 on cylindrical peg) prompted with tactile |
| [Transferring the Intelligence of VLMs to Robotic Control](https://arxiv.org/abs/2609.22966) | 2026 | GPT-6 Astra (frozen VLM; Gemini-3.8-Flash also run) |
| [VLN-Pilot: Large Vision-Language Model as an Autonomous Indoor Drone Operator](https://arxiv.org/abs/2602.05552) | 2026 | GPT-4.1 as drone pilot (Gemini 2.5 Flash also tested) |
| [World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal](https://arxiv.org/abs/2609.29964) `MA` | 2026 | Gemini 3.7 Flash (WAA backbone; Qwen3.5-9B LoRA pilot is secondary) |

</details>

<details><summary><b>Supervisor · Monitoring / recovery</b> (16)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Body-Grounded Replanning for Physically Adaptive Manipulation](https://arxiv.org/abs/2609.30024) | 2026 | GPT-4o-mini (temperature 0) strategy replanner; linear Ridge predictor for body- |
| [Containing Behavioral Cascades from Manipulated Claims in LLM-Powered Multi-Robot Systems](https://arxiv.org/abs/2609.30523) `MA` | 2026 | gpt-oss-120b as operator and verification module (open-weight, used as-is); 2D g |
| [FORGE-plus: Force-Budgeted Recovery for Contact-Rich Assembly with a Frozen LLM Supervisor](https://arxiv.org/abs/2607.21227) | 2026 | Unnamed frozen text-only LLM (hosted API or local 7-8B instruct; backend not nam |
| [Hierarchical Fast-Slow ReAct Agent for Zero-Shot Object-Goal Navigation](https://arxiv.org/abs/2608.09816) | 2026 | external VLM service (model not named; ReAct deliberation loop over reactive val |
| [LASSA Architecture-Based Autonomous Fault-Tolerant Control of Unmanned Underwater Vehicles](https://arxiv.org/abs/2605.09494) | 2026 | Kimi K2.5 (LLM backbone, chosen over Qwen3-max, DeepSeek-V3.2, GPT-5.3) |
| [MaskHarness-WAM: Instance-Grounded Harnessing for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2609.19974) | 2026 | Qwen3.5 as mask-verification and subtask-completion gates (planner model not nam |
| [On-Demand Human Assistance for Task Continuation under Physical Action Failures in LLM-based Planning](https://arxiv.org/abs/2603.28156) `MA` | 2026 | OpenAI o3-2025-0416 (task decomposition, allocation, planning, state recognition |
| [Recova: Agent-Guided Failure Recovery for Autonomous Robotic Manipulation](https://arxiv.org/abs/2610.01178) | 2026 | Gemini 3.8 Flash as VLM monitor; coding agent LM (unnamed) builds twin and recov |
| [Robot Planning and Situation Handling with Active Perception](https://arxiv.org/abs/2604.26988) | 2026 | Gemini Vision VLM for goal parsing, predicate verification and view selection; P |
| [Safe Task Planning with Long-Term Graph Memory for Embodied Agents](https://arxiv.org/abs/2609.08444) | 2026 | GPT-4o (LLM risk predictor and VLM task planner); Gemini 2.5 Flash builds scene  |
| [Self-Evolutionary Replanning for Failure-Aware Motion Planning](https://arxiv.org/abs/2603.02772) | 2026 | Qwen3-VL-Plus (ILAD) and Qwen3.7-Plus (MARS candidates and selection), used as-i |
| [Self-Evolving Just-In-Time Memory for Proactive Embodied Safety](https://arxiv.org/abs/2607.16247) | 2026 | Qwen3-VL-8B planner (off-the-shelf) with Qwen3-VL-32B RSG updater; GPT-4o and ot |
| [Spotter: Let the Embodied Model Lead, and the VLM Reflect for It](https://arxiv.org/abs/2609.36808) | 2026 | GPT-6 Astra as VLM judge (Spotter GPT), Qwen3.8-27B screener; pi0.5 and Cosmos P |
| [Talk2Escape: Conversational Grounding for Vision-and-Language Navigation](https://arxiv.org/abs/2609.28296) | 2026 | Gemini 3.1 Pro (zero-shot MLLM) driving NavGPT and GTA base agents |
| [Toward Evidence-Driven Human-Agent-Robot Teaming for Earth-Independent Anomaly Triage](https://arxiv.org/abs/2610.08933) | 2026 | Gemma-4-26B-A4B-it (orchestrator for dialogue and tool use); Qwen3-VL-8B for vis |
| [WayFinder: Hierarchical Visual-Language-Action for Zero-Shot Waypoint Generation and Low-Level Kinematic Control](https://arxiv.org/abs/2609.37922) | 2026 | Gemma 3 (4B/12B/27B) zero-shot offboard MLLM for recovery waypoints, plus author |

</details>

<details><summary><b>Benchmarks and evaluation studies</b> (3)</summary>

| Paper | Year | Evaluated seat |
|---|---|---|
| [Coding Agents for Generalized Task and Motion Planning Problems](https://arxiv.org/abs/2609.30233) | 2026 | Developer |
| [Systematic Multi-Agent Vision-and-Language Navigation: Formulation, Benchmark, and Method](https://arxiv.org/abs/2609.35965) | 2026 | Controller |
| [Vision-Language Models as copilots for Autonomous UAV Navigation: Analysis of Latency and Reliability in Degraded Environments](https://arxiv.org/abs/2609.26084) | 2026 | Controller |

</details>


## More papers from 2022–2025

610 further papers from 2022–2025 that meet the definition but are not in the curated tables above. Each was judged from its full text (a first pass, then a verification pass by a stronger model; papers off arXiv without an open-access PDF were judged from the abstract); the reasons and quotes are in [docs/paper_list.md](docs/paper_list.md). `MA` marks the multi-agent chapter.

<details><summary><b>Designer · Environments / reconstruction</b> (6)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Holodeck: Language Guided Generation of 3D Embodied AI Environments](https://arxiv.org/abs/2312.09067) | 2023 | GPT-4 (layout constraints) and GPT-4V (asset annotation), used as-is |
| [Towards Generalist Robots: A Promising Paradigm via Generative Simulation](https://arxiv.org/abs/2305.10455) | 2023 | GPT-4 (prompted, zero prompt tuning) |
| [Articulate-Anything: Automatic Modeling of Articulated Objects via a Vision-Language Foundation Model](https://arxiv.org/abs/2410.13882) `MA` | 2024 | Gemini Flash-1.5 (VLM actors and critics, few-shot) |
| [GRS: Generating Robotic Simulation Tasks from Real-World Images](https://arxiv.org/abs/2410.15536) | 2024 | GPT-4o (VLM writes simulation and test code; Claude-3.5-Sonnet only in object ma |
| [Hazards in Daily Life? Enabling Robots to Proactively Detect and Resolve Anomalies](https://arxiv.org/abs/2411.00781) `MA` | 2024 | GPT-4-0314 (LLM agents) and BLIP-2 (VLM) |
| [GenDexHand: Generative Simulation for Dexterous Hands](https://arxiv.org/abs/2511.01791) | 2025 | Claude Sonnet 4.0 (task, scene, reward and subtask generation); Gemini 2.5 Pro ( |

</details>

<details><summary><b>Designer · Rewards / tasks</b> (53)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Bootstrap Your Own Skills: Learning to Solve New Tasks with Large Language Model Guidance](https://arxiv.org/abs/2310.10021) | 2023 | LLaMA-13B prompted as-is to choose next skill chains during bootstrapping; IQL s |
| [Gen2Sim: Scaling up Robot Learning in Simulation with Generative Models](https://arxiv.org/abs/2310.18308) | 2023 | GPT-4 (few-shot prompted; image diffusion models and PPO are tools or trained co |
| [LARG, Language-based Automatic Reward and Goal Generation](https://arxiv.org/abs/2306.10985) | 2023 | gpt-3.5-turbo (prompted; PPO policy trained separately) |
| [Learning Reward for Physical Skills using Large Language Model](https://arxiv.org/abs/2310.14092) | 2023 | unnamed pre-trained LLM (no model named; CoT prompting and trajectory ranking, n |
| [Self-Refined Large Language Model as Automated Reward Function Designer for Deep Reinforcement Learning in Robotics](https://arxiv.org/abs/2309.06687) | 2023 | GPT-4 (zero-shot, self-refinement loop) |
| [Towards A Unified Agent with Foundation Models](https://arxiv.org/abs/2307.09668) | 2023 | FLAN-T5 used off-the-shelf for sub-goal curriculum; fine-tuned CLIP as reward VL |
| [Words into Action: Learning Diverse Humanoid Robot Behaviors using Language Guided Iterative Motion Refinement](https://arxiv.org/abs/2310.06226) | 2023 | ChatGPT-4 (prompt generator and policy initializer; T2M-GPT motion model and AMP |
| [A Large Language Model-Driven Reward Design Framework via Dynamic Feedback for Reinforcement Learning](https://arxiv.org/abs/2410.14660) | 2024 | GPT-4-1106-preview (Coder; Evaluator is rule-based) |
| [Adaptive Language-Guided Abstraction from Contrastive Explanations](https://arxiv.org/abs/2409.08212) | 2024 | GPT-4o queried zero-shot to propose missing reward features from demonstrations |
| [Affordance-Guided Reinforcement Learning via Visual Prompting](https://arxiv.org/abs/2407.10341) | 2024 | GPT-4o (zero-shot waypoint selection); MiniGPT-4 fine-tuned classifier only for  |
| [AnyBipe: An End-to-End Framework for Training and Deploying Bipedal Robots Guided by Large Language Models](https://arxiv.org/abs/2409.08904) | 2024 | GPT-4o / Claude-3.5-Sonnet / DeepSeek-R1 (reward-code writer) |
| [ARO: Large Language Model Supervised Robotics Text2Skill Autonomous Learning](https://arxiv.org/abs/2403.15834) | 2024 | GPT-4 (generates reward, evaluation and suggestion code; SAC policy trained) |
| [Automated Rewards via LLM-Generated Progress Functions](https://arxiv.org/abs/2410.09187) | 2024 | GPT-4-Turbo (gpt-4-turbo-2024-04-09) |
| [Autonomous Improvement of Instruction Following Skills via Foundation Models](https://arxiv.org/abs/2407.20635) | 2024 | frozen CogVLM for task proposals and success labels; GPT-4 only translates task  |
| [BBSEA: An Exploration of Brain-Body Synchronization for Embodied Agents](https://arxiv.org/abs/2402.08212) | 2024 | GPT-4 (task proposer, success inference, task decomposition; GPT-4V only as base |
| [Diffusion Augmented Agents: A Framework for Efficient Exploration and Transfer Learning](https://arxiv.org/abs/2407.20798) | 2024 | Gemini Pro 1.0 as LLM orchestrator; CLIP ViT-B/32 finetuned as reward detector ( |
| [E2CFD: Towards Effective and Efficient Cost Function Design for Safe Reinforcement Learning via Large Language Model](https://arxiv.org/abs/2407.05580) | 2024 | unnamed LLM generates cost-function code via prompts; no model named |
| [Efficient Language-instructed Skill Acquisition via Reward-Policy Co-Evolution](https://arxiv.org/abs/2412.13492) | 2024 | GPT-4o (reward generation; PPO trains policies) |
| [ELEMENTAL: Interactive Learning from Demonstrations and Vision-Language Models for Reward Design in Robotics](https://arxiv.org/abs/2411.18825) | 2024 | GPT-4o (VLM drafts feature functions; IRL and PPO train reward and policy) |
| [Game On: Towards Language Models as RL Experimenters](https://arxiv.org/abs/2409.03402) | 2024 | standard Gemini 1.5 Pro (no fine-tuning) as curriculum, decomposition and analys |
| [ICPL: Few-shot In-context Preference Learning via LLMs](https://arxiv.org/abs/2410.17233) | 2024 | GPT-4 (GPT-4-0613) in proxy experiments; GPT-4o in human-in-the-loop |
| [Language-Model-Assisted Bi-Level Programming for Reward Learning from Internet Videos](https://arxiv.org/abs/2410.09286) | 2024 | GPT-4o (reward code) and Gemini 1.5-Pro (VLM video feedback) |
| [Learning Reward for Robot Skills Using Large Language Models via Self-Alignment](https://arxiv.org/abs/2405.07162) | 2024 | GPT-4 (gpt-4-0613, prompted; SAC/PPO policies trained) |
| [Learning with Language-Guided State Abstractions](https://arxiv.org/abs/2402.18759) | 2024 | GPT-4 (gpt-4-0613, prompted; CNN imitation policy trained on demonstrations) |
| [LLM-Empowered State Representation for Reinforcement Learning](https://arxiv.org/abs/2407.13237) | 2024 | gpt-4-1106-preview generates state-representation and intrinsic-reward code; no  |
| [REvolve: Reward Evolution with Large Language Models using Human Feedback](https://arxiv.org/abs/2406.01309) | 2024 | GPT-4 Turbo (1106-preview) as reward designer |
| [SDS - See it, Do it, Sorted: Quadruped Skill Synthesis from Single Video Demonstration](https://arxiv.org/abs/2410.11571) `MA` | 2024 | GPT-4o (VLM; reward-function writer and rollout evaluator) |
| [Training Fast Robot Policies with Slow Foundation Models](https://arxiv.org/abs/2406.05881) | 2024 | llama-3.3-70b-versatile as LLM + llama-4-scout-17b-16e-instruct as VLM, both fro |
| [Video2Reward: Generating Reward Function from Videos for Legged Robot Behavior Learning](https://arxiv.org/abs/2412.05515) | 2024 | LLM (model not named in main text; prompted only) |
| [AURA: Autonomous Upskilling with Retrieval-Augmented Agents](https://arxiv.org/abs/2506.02507) `MA` | 2025 | GPT o4-mini (high-level planner); GPT-4.1 (stage-level LLM and feedback) |
| [Automated Generation of MDPs Using Logic Programming and LLMs for Robotic Applications](https://arxiv.org/abs/2511.23143) | 2025 | GPT-4o and GPT-5-mini (few-shot KB, action and reward generation) + Storm policy |
| [Automated Hybrid Reward Scheduling Via Large Language Models for Robotic Skill Learning](https://arxiv.org/abs/2505.02483) | 2025 | GPT-4o selects reward-weight rules and writes auxiliary reward during RL trainin |
| [Boosting Universal LLM Reward Design through Heuristic Reward Observation Space Evolution](https://arxiv.org/abs/2504.07596) | 2025 | GPT-4 (gpt-4-0314) as reward designer LLM_R and mission reconciler LLM_C; PPO in |
| [CRAFT: Coaching Reinforcement Learning Autonomously using Foundation Models for Multi-Robot Coordination Tasks](https://arxiv.org/abs/2509.14380) `MA` | 2025 | gpt-4o-2024-08-06 (curriculum and reward LLM); o4-mini-2025-04-16 (evaluation an |
| [E-SDS: Environment-aware See it, Do it, Sorted - Automated Environment-Aware Reinforcement Learning for Humanoid Locomotion](https://arxiv.org/abs/2512.16446) `MA` | 2025 | GPT-5 (multi-agent VLM reward generation with environment, gait and feedback age |
| [Embodied Learning of Reward for Musculoskeletal Control with Vision Language Models](https://arxiv.org/abs/2512.23077) | 2025 | gemini-2.0-flash (VLM feedback) + Qwen2.5-Coder-32B-Instruct (reward writer), us |
| [GROVE: A Generalized Reward for Learning Open-Vocabulary Physical Skill](https://arxiv.org/abs/2504.04191) | 2025 | GPT-o1-preview writes task reward code; CLIP-based VLM reward; PPO humanoid skil |
| [Human-Object Interaction via Automatically Designed VLM-Guided Motion Policy](https://arxiv.org/abs/2503.18349) | 2025 | GPT-4V VLM planner outputs RMD plans; goal-conditioned PPO humanoid policy in Is |
| [LAMARL: LLM-Aided Multi-Agent Reinforcement Learning for Cooperative Policy Generation](https://arxiv.org/abs/2506.01538) `MA` | 2025 | OpenAI o1-preview (prior policy and reward code) |
| [LaMOuR: Leveraging Language Models for Out-of-Distribution Recovery in Reinforcement Learning](https://arxiv.org/abs/2503.17125) | 2025 | GPT-4o (LVLM) writes recovery reward and evaluation code; SAC retraining in MuJo |
| [Learning a High-Quality Robotic Wiping Policy Using Systematic Reward Analysis and Visual-Language Model Based Curriculum](https://arxiv.org/abs/2502.12599) `MA` | 2025 | GPT-4 (LLM) + gpt-4-vision-preview (VLM) curriculum; RL wiping policy trained in |
| [Leveraging LLMs for reward function design in reinforcement learning control tasks](https://arxiv.org/abs/2511.19355) `MA` | 2025 | gpt-4.1-nano (main; also gpt-4.1-mini, Gemini 2.5 Flash and Qwen3 tested) |
| [MA-ROESL: Motion-aware Rapid Reward Optimization for Efficient Robot Skill Learning from Single Videos](https://arxiv.org/abs/2505.08367) | 2025 | GPT-4V (reward generation and evaluation) |
| [Option Discovery Using LLM-guided Semantic Hierarchical Reinforcement Learning](https://arxiv.org/abs/2503.19007) | 2025 | ChatGPT-o1 (LLM subgoal generation before RL training) |
| [PROF: An LLM-based Reward Code Preference Optimization Framework for Offline Imitation Learning](https://arxiv.org/abs/2511.13765) | 2025 | GPT-4o-2024-11-20 (zero-shot reward code generation with TextGrad refinement) |
| [Rational Inverse Reasoning](https://arxiv.org/abs/2508.08983) | 2025 | Gemini VLM (gemini-3-flash-preview; Gemini-3-Pro on real robot) proposing Python |
| [Reward Evolution with Graph-of-Thoughts: A Bi-Level Language Model Framework for Reinforcement Learning](https://arxiv.org/abs/2509.16136) | 2025 | gpt-4o-2024-08-06 (graph and reward code); gemini-1.5-pro (VLM evaluator) |
| [RoboHorizon: An LLM-Assisted Multi-View World Model for Long-Horizon Robotic Manipulation](https://arxiv.org/abs/2501.06605) | 2025 | GPT-4o (plan descriptor and dense reward generator; RL trains the authors' world |
| [STRIDE: Automating Reward Design, Deep Reinforcement Learning Training and Feedback Optimization in Humanoid Robotics Locomotion](https://arxiv.org/abs/2502.04692) | 2025 | GPT-4o mini (LLM reward writer in STRIDE; PPO trains the humanoid policy) |
| [Text2Touch: Tactile In-Hand Manipulation with LLM-Designed Reward Functions](https://arxiv.org/abs/2509.07445) | 2025 | GPT-4o / o3-mini / Gemini-1.5-Flash / Llama3.1-405B / DeepSeek-R1-671B (reward w |
| [Towards Autonomous Reinforcement Learning for Real-World Robotic Manipulation With Large Language Models](https://arxiv.org/abs/2503.04280) | 2025 | GPT-4 writes reward and success/failure code; SAC trains ABB YuMi policies |
| [Uncertainty-aware Reward Design Process](https://arxiv.org/abs/2507.02256) | 2025 | DeepSeek-V3 (241226) as foundational LLM |
| [VIRAL: Vision-grounded Integration for Reward design And Learning](https://arxiv.org/abs/2505.22092) `MA` | 2025 | Qwen2.5-Coder-32B (coder) + Llama3.2-Vision-11B (critic) + Qwen2.5-VL-7B (video  |

</details>

<details><summary><b>Teacher · Demonstration / distillation</b> (13)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [AlphaBlock: Embodied Finetuning for Vision-Language Reasoning in Robot Manipulation](https://arxiv.org/abs/2305.18898) | 2023 | GPT-4 closed-loop plan generator with LAVA executing in tabletop sim (data-colle |
| [Octopus: Embodied Vision-Language Programmer from Environmental Feedback](https://arxiv.org/abs/2310.08588) | 2023 | Octopus VLM (SFT+RLEF, trained by authors) with GPT-4 as sim data-collecting age |
| [ExploRLLM: Guiding Exploration in Reinforcement Learning with Large Language Models](https://arxiv.org/abs/2403.09583) | 2024 | GPT-4 few-shot exploration code; SAC residual RL policy trained by authors |
| [MARLIN: Multi-Agent Reinforcement Learning Guided by Language-Based Inter-Robot Negotiation](https://arxiv.org/abs/2410.14383) `MA` | 2024 | Llama 3.1 8B Instruct (remote, off-the-shelf), one LLM per robot negotiating act |
| [RLingua: Improving Reinforcement Learning Sample Efficiency in Robotic Manipulations With Large Language Models](https://arxiv.org/abs/2403.06420) | 2024 | GPT-4 writes a Python rule-based Franka controller used to generate TD3 training |
| [VLM Agents Generate Their Own Memories: Distilling Experience into Embodied Programs of Thought](https://arxiv.org/abs/2406.14596) | 2024 | GPT-4V (gpt-4-1106-vision-preview) as in-context VLM agent; Qwen2-VL-7B and GPT- |
| [BLAZER: Bootstrapping LLM-based Manipulation Agents with Zero-Shot Data Generation](https://arxiv.org/abs/2510.08572) | 2025 | LLaMA3.3-70B (teacher, used as-is in sim); deployed LLaMA-3.1-8B LoRA-SFT on its |
| [Distilling On-device Language Models for Robot Planning with Minimal Human Intervention](https://arxiv.org/abs/2506.17486) | 2025 | GPT-4o teacher distilled into Llama-3.2-3B SLM |
| [Imagine, Verify, Execute: Memory-Guided Agentic Exploration with Vision-Language Models](https://arxiv.org/abs/2505.07815) | 2025 | GPT-4o as scene describer, explorer and verifier (Gemini, Qwen3, LLaMA-4 also te |
| [LLM Trainer: Automated Robotic Data Generating via Demonstration Augmentation using LLMs](https://arxiv.org/abs/2509.20070) | 2025 | GPT-4o annotates demos and proposes keypoints that warp demonstrations; optimize |
| [LLM-based Interactive Imitation Learning for Robotic Manipulation](https://arxiv.org/abs/2504.21769) | 2025 | Llama3-70b via API writes CodePolicy teacher; agent is a small Gaussian policy t |
| [RALLY: Role-Adaptive LLM-Driven Yoked Navigation for Agentic UAV Swarms](https://arxiv.org/abs/2507.01378) `MA` | 2025 | GPT-4o API as sim role/target prior and sample generator; deployed LoRA-tuned Qw |
| [Skypilot: Fine-Tuning LLM with Physical Grounding for AAV Coverage Search](https://arxiv.org/abs/2511.18270) | 2025 | Qwen3-4B full-parameter SFT on 23k GPT-4o MCTS trajectories (GPT-4o is the MCTS  |

</details>

<details><summary><b>Developer · System / code</b> (21)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Learning adaptive planning representations with natural language guidance](https://arxiv.org/abs/2312.08566) | 2023 | GPT-3.5 (gpt-3.5-turbo-16k), few-shot prompted |
| [Automatic Robotic Development through Collaborative Framework by Large Language Models](https://arxiv.org/abs/2402.03699) `MA` | 2024 | Three role-prompted ChatGPT agents (analyst, programmer, tester) |
| [CLIMB: Language-Guided Continual Learning for Task Planning with Iterative Model Building](https://arxiv.org/abs/2410.13756) | 2024 | gpt-4o-2024-08-06 (PDDL domain, predicate and grounding generation) + FastDownwa |
| [Growing from Exploration: A self-exploring framework for robots based on foundation models](https://arxiv.org/abs/2401.13462) | 2024 | Unnamed LLM planner (code skills) + GPT-4V verifier |
| [InterPreT: Interactive Predicate Learning from Language Feedback for Generalizable Task Planning](https://arxiv.org/abs/2405.19758) | 2024 | GPT-4 (prompted: Reasoner, Coder, Corrector, goal translator), used as-is |
| [RoboCoder: Robotic Learning from Basic Skills to General Tasks with Large Language Models](https://arxiv.org/abs/2406.03757) | 2024 | GPT-4 (Actor, default) + GPT-4V (Evaluator) + MiniLM searcher |
| [Vocal Sandbox: Continual Learning and Adaptation for Situated Human-Robot Collaboration](https://arxiv.org/abs/2411.02599) | 2024 | GPT-3.5 Turbo (function calling, prompted LM planner) |
| [Agent2: An Agent-Generates-Agent Framework for Reinforcement Learning Automation](https://arxiv.org/abs/2509.13368) | 2025 | Claude-Sonnet-3.7 (prompted Generator Agent) |
| [Growing with Your Embodied Agent: A Human-in-the-Loop Lifelong Code Generation Framework for Long-Horizon Manipulation Skills](https://arxiv.org/abs/2509.18597) | 2025 | Unnamed general LLM (model not named in text; in-context prompting; baselines us |
| [In-Context Iterative Policy Improvement for Dynamic Manipulation](https://arxiv.org/abs/2508.15021) | 2025 | Pre-trained gpt-4o used in-context, no fine-tuning (also gpt-3.5-turbo, gpt-4o-m |
| [LAD-VF: LLM-Automatic Differentiation Enables Fine-Tuning-Free Robot Planning from Formal Methods Feedback](https://arxiv.org/abs/2509.18384) | 2025 | GPT-4o-2024-08-16 (planner and prompt optimizer, prompted, no weight updates) |
| [NeSyC: A Neuro-symbolic Continual Learner For Complex Embodied Tasks In Open Domains](https://arxiv.org/abs/2503.00870) | 2025 | GPT-4o (hypothesis generator and semantic parser, temperature 0) |
| [Never too Prim to Swim: An LLM-Enhanced RL-based Adaptive S-Surface Controller for AUVs under Extreme Sea Conditions](https://arxiv.org/abs/2503.00527) | 2025 | GPT-4o (VLLM), deepseek-V3 (Textual) tune reward weights and S-surface gains; RL |
| [PSALM-V: Automating Symbolic Planning in Interactive Visual Environments with Large Language Models](https://arxiv.org/abs/2506.20097) | 2025 | GPT-4o (default LLM) |
| [Robot builds a robot's brain: AI generated drone command and control station hosted in the sky](https://arxiv.org/abs/2508.02962) | 2025 | Claude Sonnet 3.5/3.7, Gemini 2.5, ChatGPT 4.0 (prompted coding in IDEs), used a |
| [SAS-Prompt: Large Language Models as Numerical Optimizers for Robot Self-Improvement](https://arxiv.org/abs/2504.20459) | 2025 | LLM with SAS Prompt (unnamed in robot tests; Gemini 1.5 Pro in optimization test |
| [SkillWrapper: Generative Predicate Invention for Skill Abstraction](https://arxiv.org/abs/2511.18203) | 2025 | GPT-5 (off-the-shelf, prompted) |
| [UniDomain: Pretraining a Unified PDDL Domain from Real-World Demonstrations for Generalizable Robot Task Planning](https://arxiv.org/abs/2507.21545) | 2025 | GPT-4.1 via API (temp 0.0) in planning evaluation; domain-pretraining VLM/LLM no |
| [Unifying Deep Predicate Invention with Pre-trained Foundation Models](https://arxiv.org/abs/2512.17992) | 2025 | GPT-4o (default; proposes predicate effect hypotheses; Gemini 2.5 Flash-Lite and |
| [Using VLM Reasoning to Constrain Task and Motion Planning](https://arxiv.org/abs/2510.25548) | 2025 | Gemini 3.5 Flash (Shelf, Packing) and Gemini 3.6 Flash (Cooking) as VLM |
| [ViReSkill: Vision-Grounded Replanning with Skill Memory for LLM-Based Planning in Lifelong Robot Learning](https://arxiv.org/abs/2509.24219) | 2025 | GPT-4.1-mini (LLM for code and replanning); GPT-4o-mini (VLM for failure analysi |

</details>

<details><summary><b>Developer · Embodiment / tools</b> (3)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Debate2Create: Robot Co-design via Multi-Agent LLM Debate](https://arxiv.org/abs/2510.25850) `MA` | 2025 | GPT-5.2 (gpt-5.2-2025-12-11, prompted design and control agents) |
| [Lang2Morph: Language-Driven Morphological Design of Robotic Hands](https://arxiv.org/abs/2509.18937) | 2025 | GPT-4o-mini (ChatGPT, prompted, no training) |
| [RoboMoRe: LLM-based Robot Co-design via Joint Optimization of Morphology and Reward](https://arxiv.org/abs/2506.00276) | 2025 | GPT-4-turbo (foundation model, prompted, Eureka-style), used as-is |

</details>

<details><summary><b>Controller · Orchestration</b> (346)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [CAPE: Corrective Actions from Precondition Errors using Large Language Models](https://arxiv.org/abs/2211.09935) | 2022 | OpenAI davinci-instruct (GPT-3 family) LLM |
| [LLM-Planner: Few-Shot Grounded Planning for Embodied Agents with Large Language Models](https://arxiv.org/abs/2212.04088) | 2022 | GPT-3 (text-davinci-003) with 9 kNN-retrieved in-context examples; HLSM percepti |
| [Open-vocabulary Queryable Scene Representations for Real World Planning](https://arxiv.org/abs/2209.09874) | 2022 | PaLM 540B (LLM for object proposal and planning) with ViLD/CLIP scene representa |
| ["Tidy Up the Table": Grounding Common-sense Objective for Tabletop Object Rearrangement](https://arxiv.org/abs/2307.11319) | 2023 | GPT-4 (object-centric policy proposal); trained ResNet-18 tidiness critic as too |
| [A2Nav: Action-Aware Zero-Shot Robot Navigation by Exploiting Vision-and-Language Ability of Foundation Models](https://arxiv.org/abs/2308.07997) | 2023 | GPT-3 instruction parser (prompted); ZSON navigators fine-tuned by authors used  |
| [Agent as Cerebrum, Controller as Cerebellum: Implementing an Embodied LMM-based Agent on Drones](https://arxiv.org/abs/2311.15033) | 2023 | GPT-4V (gpt-4-vision-preview) as AeroAgent core |
| [Building Cooperative Embodied Agents Modularly with Large Language Models](https://arxiv.org/abs/2307.02485) `MA` | 2023 | GPT-4 (one CoELA cognitive-module agent per robot; LLaMA-2 and LoRA CoLLAMA only |
| [CARTIER: Cartographic lAnguage Reasoning Targeted at Instruction Execution for Robots](https://arxiv.org/abs/2307.11865) | 2023 | ChatGPT and GPT-4 prompted (temperature 0) to pick target object; no training |
| [Chat with the Environment: Interactive Multimodal Perception Using Large Language Models](https://arxiv.org/abs/2303.08268) | 2023 | OpenAI text-davinci-003 (5-shot prompt, no fine-tuning) |
| [ChatGPT Empowered Long-Step Robot Control in Various Environments: A Case Application](https://arxiv.org/abs/2304.03893) | 2023 | gpt-3.5-turbo via Azure OpenAI (few-shot prompts, no training) |
| [Collaborating with language models for embodied reasoning](https://arxiv.org/abs/2302.00763) | 2023 | Chinchilla 7B/70B frozen planner with few-shot prompting |
| [Conformal Temporal Logic Planning using Large Language Models](https://arxiv.org/abs/2309.10092) | 2023 | pre-trained GPT-3.5, Llama 2-13b, Llama 3-8b, Qwen 3-32b (neural planner; Llama  |
| [Cook2LTL: Translating Cooking Recipes to LTL Formulae using Large Language Models](https://arxiv.org/abs/2310.00163) | 2023 | gpt-3.5-turbo (reduces cooking actions to primitive-action functions); fine-tune |
| [CoPAL: Corrective Planning of Robot Actions with Large Language Models](https://arxiv.org/abs/2310.07263) `MA` | 2023 | GPT-4 (Travi, Ropa) and GPT-3.5 (Alex), prompted; no training |
| [CorNav: Autonomous Agent with Self-Corrected Planning for Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2306.10322) | 2023 | Vicuna v1.5-13B zero-shot as planner and decision expert; GPT-4 Turbo on a subse |
| [Dobby: A Conversational Service Robot Driven by GPT-4](https://arxiv.org/abs/2310.06303) | 2023 | GPT-4 (gpt-4-0613, prompted, native function calling; not trained by authors) |
| [DynaCon: Dynamic Robot Planner with Contextual Awareness via LLMs](https://arxiv.org/abs/2309.16031) | 2023 | GPT-3.5 (prompt engineering only) |
| [Errors are Useful Prompts: Instruction Guided Task Programming with Verifier-Assisted Iterative Prompting](https://arxiv.org/abs/2303.14100) | 2023 | GPT-3 prompted with XDL grammar and rules; rule-based verifier feeds errors back |
| [Foundation Model based Open Vocabulary Task Planning and Executive System for General Purpose Service Robots](https://arxiv.org/abs/2308.03357) | 2023 | GPT-3 text-davinci-003 few-shot prompted (temperature 0); Detic, OFA, YOLOv7 as  |
| [GPT-4V(ision) for Robotics: Multimodal Task Planning From Human Demonstration](https://arxiv.org/abs/2311.12015) | 2023 | GPT-4V + GPT-4 (off-the-shelf, prompt-only) |
| [Grounded Decoding: Guiding Text Generation with Grounded Models for Embodied Agents](https://arxiv.org/abs/2303.00855) | 2023 | InstructGPT (text-davinci-002, frozen) in sim domains; PaLM-540B plus InstructGP |
| [HiCRISP: An LLM-Based Hierarchical Closed-Loop Robotic Intelligent Self-Correction Planner](https://arxiv.org/abs/2309.12089) | 2023 | GPT-3.5 (planner) |
| [Improved Trust in Human-Robot Collaboration with ChatGPT](https://arxiv.org/abs/2304.12529) | 2023 | GPT-3.5 via OpenAI API ("fine-tuned" by prompt design only) |
| [Improving Knowledge Extraction from LLMs for Task Learning through Agent Analysis](https://arxiv.org/abs/2306.06770) | 2023 | GPT-3 (search and repair) and GPT-4 (selection) inside a cognitive agent, not tr |
| [Integration of Large Language Models within Cognitive Architectures for Autonomous Robots](https://arxiv.org/abs/2309.14945) | 2023 | Marcoroni-13B (4-bit quantized, via llama_ros), not trained by authors |
| [Interactive Planning Using Large Language Models for Partially Observable Robotic Tasks](https://arxiv.org/abs/2312.06876) | 2023 | GPT-4 (gpt-4-0314) planner and evaluator; fine-tuned Llama2-7B only as compariso |
| [Interactive Task Planning with Language Models](https://arxiv.org/abs/2310.10645) | 2023 | GPT-4 high-level planner plus GPT-4 low-level executor via function calling; tra |
| [LAN-grasp: Using Large Language Models for Semantic Object Grasping](https://arxiv.org/abs/2310.05239) | 2023 | GPT-4 (grasp-part choice); pretrained OWL-ViT as VLM grounding tool |
| [Language and Sketching: An LLM-driven Interactive Multimodal Multitask Robot Navigation Framework](https://arxiv.org/abs/2311.08244) | 2023 | Unnamed LLM backbone (prompt + function library, no training described) |
| [Lifelong Robot Learning with Human Assisted Language Planners](https://arxiv.org/abs/2309.14321) | 2023 | GPT-4 (prompted code planner) |
| [LLM+P: Empowering Large Language Models with Optimal Planning Proficiency](https://arxiv.org/abs/2304.11477) | 2023 | GPT-4 (OpenAI API, temperature 0, in-context example) |
| [LLM-State: Open World State Representation for Long-horizon Task Planning with Large Language Model](https://arxiv.org/abs/2311.17406) | 2023 | GPT-4 (gpt-4-0613) as attention, state estimator and policy |
| [Make a Donut: Hierarchical EMD-Space Planning for Zero-Shot Deformable Manipulation With Tools](https://arxiv.org/abs/2311.02787) | 2023 | GPT-4 (ChatGPT-4) |
| [March in Chat: Interactive Prompting for Remote Embodied Referring Expression](https://arxiv.org/abs/2308.10141) | 2023 | GPT-2 (public LM, in-context prompting) writes step-by-step instructions; traine |
| [Multimodal Grounding for Embodied AI via Augmented Reality Headsets for Natural Language Driven Task Planning](https://arxiv.org/abs/2304.13676) | 2023 | GPT-3 text-davinci-003 (5-shot UMRF prompting via OpenAI API) |
| [OceanChat: Piloting Autonomous Underwater Vehicles in Natural Language](https://arxiv.org/abs/2309.16052) | 2023 | GPT-4 (LLM planner, prompted with action set; no training) |
| [Open-Ended Instructable Embodied Agents with Memory-Augmented Large Language Models](https://arxiv.org/abs/2310.15127) | 2023 | GPT-4 (gpt-4-0613) with retrieved language-program memory as prompt examples |
| [Prompt, Plan, Perform: LLM-based Humanoid Control via Quantized Imitation Learning](https://arxiv.org/abs/2309.11359) | 2023 | Llama, GPT-4, Falcon prompted as planner (PPO-trained motion policy used as a to |
| [QwenGrasp: A Usage of Large Vision-Language Model for Target-Oriented Grasping](https://arxiv.org/abs/2309.16426) | 2023 | Qwen-VL (pre-trained, used as-is with preloaded prompts) + pre-trained REGNet gr |
| [Robot-Enabled Construction Assembly with Automated Sequence Planning based on ChatGPT: RoboGPT](https://arxiv.org/abs/2304.11018) | 2023 | ChatGPT-4 via API (prompting only, no training) |
| [SAGE: Bridging Semantic and Actionable Parts for GEneralizable Manipulation of Articulated Objects](https://arxiv.org/abs/2312.01307) | 2023 | GPT-4V (global planner and instruction interpreter, with GAPartNet and DINOv2 pe |
| [SayCanPay: Heuristic Planning with Large Language Models using Learnable Domain Knowledge](https://arxiv.org/abs/2308.12682) | 2023 | Vicuna-13B or Flan-T5-11B as Say model (no fine-tuning); trained Can and Pay sco |
| [Scalable Multi-Robot Collaboration with Large Language Models: Centralized or Decentralized Systems?](https://arxiv.org/abs/2309.15943) `MA` | 2023 | GPT-4 (gpt-4-0613) and GPT-3.5-turbo (gpt-3.5-turbo-0613) as per-robot or centra |
| [Self-Recovery Prompting: Promptable General Purpose Service Robot System with Foundation Models and Self-Recovery](https://arxiv.org/abs/2309.14425) | 2023 | GPT-4 (planning, function calling, prompt-only); Whisper, Detic, CLIP as percept |
| [Task and Motion Planning with Large Language Models for Object Rearrangement](https://arxiv.org/abs/2303.06247) | 2023 | GPT-3 text-davinci-003 (prompted) |
| [Think, Act, and Ask: Open-World Interactive Personalized Robot Navigation](https://arxiv.org/abs/2310.07968) | 2023 | GPT-4-8k-0613 as LLM controller over navigation, detection, memory and talk modu |
| [ThinkBot: Embodied Instruction Following with Thought Chain Reasoning](https://arxiv.org/abs/2312.07062) | 2023 | GPT-3.5-turbo instruction completer (prompted); trained object localizer as tool |
| [Toward Grounded Commonsense Reasoning](https://arxiv.org/abs/2306.08651) | 2023 | GPT-4 (temperature 0) as LLM and InstructBLIP Flan-T5-XXL as VLM, off-the-shelf |
| [Tree-Planner: Efficient Close-loop Task Planning with Large Language Models](https://arxiv.org/abs/2310.08582) | 2023 | GPT-3.5 (text-davinci-003) with Tree-Planner prompting (plan sampling + action t |
| [WALL-E: Embodied Robotic WAiter Load Lifting with Large Language Model](https://arxiv.org/abs/2308.15962) | 2023 | ChatGPT (gpt-3.5-turbo), prompting only |
| [A Prompt-Driven Task Planning Method for Multi-Drones Based on Large Language Model](https://arxiv.org/abs/2406.00006) `MA` | 2024 | Unnamed LLM (prompted, zero-shot; the paper never names the model) |
| [A Robotic Skill Learning System Built Upon Diffusion Policies and Foundation Models](https://arxiv.org/abs/2403.16730) | 2024 | GPT-4 (skill-selector LLM and VLM precondition check, prompted; Gemini compared) |
| [Action Contextualization: Adaptive Task Planning and Action Tuning Using Large Language Models](https://arxiv.org/abs/2404.13191) | 2024 | GPT-4-1106-preview (prompted; open-mixtral-8x22b and Llama-3-70B compared) |
| [AlignBot: Aligning VLM-Powered Customized Task Planning with User Reminders Through Fine-Tuning for Household Robots](https://arxiv.org/abs/2409.11905) | 2024 | GPT-4o (frozen planner) + fine-tuned LLaVA-7B cue adapter (LoRA) |
| [APRICOT: Active Preference Learning and Constraint-Aware Task Planning with LLMs](https://arxiv.org/abs/2410.19656) | 2024 | GPT-4-turbo for semantic plans and refinement (GPT-4o for questions; RL pick/pla |
| [AssistantX: An LLM-Powered Proactive Assistant in Collaborative Human-Populated Environments](https://arxiv.org/abs/2409.17655) `MA` | 2024 | ChatGPT-4o (GPT-4o) as the foundation LLM of four agents |
| [AToM-Bot: Embodied Fulfillment of Unspoken Human Needs with Affective Theory of Mind](https://arxiv.org/abs/2406.08455) | 2024 | GPT-4V (off-the-shelf VLM) |
| [AutoGPT+P: Affordance-based Task Planning with Large Language Models](https://arxiv.org/abs/2402.10778) | 2024 | GPT-4-0613 (LLM tool selection); ChatGPT for affordance mapping |
| [Autonomous Behavior Planning For Humanoid Loco-manipulation Through Grounded Language Model](https://arxiv.org/abs/2408.08282) | 2024 | GPT-4（经OpenAI API生成行为树XML任务图）；VLM用于失败检测 |
| [Behav: Behavioral Rule Guided Autonomy Using VLMs for Robot Navigation in Outdoor Scenes](https://arxiv.org/abs/2409.16484) | 2024 | GPT-4 (instruction decomposition, action desirability) and GPT-4o VLM (landmark  |
| [Behavior Tree Generation using Large Language Models for Sequential Manipulation Planning with Human Instructions and Feedback](https://arxiv.org/abs/2409.09435) | 2024 | GPT-4 (prompted for behavior tree generation; LLaMA2-13B and Mistral-7B fine-tun |
| [Bi-VLA: Vision-Language-Action Model-Based System for Bimanual Robotic Dexterous Manipulations](https://arxiv.org/abs/2405.06039) `MA` | 2024 | Starling-LM-7B-alpha (planner and code generator, as-is) with Qwen-VL (vision, a |
| [Blox-Net: Generative Design-for-Robot-Assembly Using VLM Supervision, Physics Simulation, and a Robot with Reset](https://arxiv.org/abs/2409.17126) | 2024 | GPT-4o (VLM for design, plan and order prompts) |
| [Bootstrapping Object-Level Planning with Large Language Models](https://arxiv.org/abs/2409.12262) | 2024 | ChatGPT (text says ChatGPT-3; footnote 3 says chatgpt-4o-latest gave best plans) |
| [CAMON: Cooperative Agents for Multi-Object Navigation with LLM-based Conversations](https://arxiv.org/abs/2407.00632) `MA` | 2024 | GPT-4o (room descriptions); general LLM for proposals and leader coordination (m |
| [CaPo: Cooperative Plan Optimization for Efficient Embodied Multi-Agent Cooperation](https://arxiv.org/abs/2411.04679) `MA` | 2024 | GPT-4 agents (GPT-3.5-turbo and Llama-2-13B-chat also tested) with multi-turn me |
| [CLMASP: Coupling Large Language Models with Answer Set Programming for Robotic Task Planning](https://arxiv.org/abs/2406.03367) | 2024 | gpt-4o-2024-08-06 with gpt-3.5-turbo-1106 and Llama3.1-8B as alternatives |
| [CogNav: Cognitive Process Modeling for Object Goal Navigation with LLMs](https://arxiv.org/abs/2412.10439) | 2024 | GPT-3 as LLM and GPT-4V as VLM, used as-is with cognitive-map prompting |
| [Cognitive Planning for Object Goal Navigation using Generative AI Models](https://arxiv.org/abs/2404.00318) | 2024 | GPT-4 (planner, in-context prompting); GPT-3.5 used as pruner; LLaVA for caption |
| [COHERENT: Collaboration of Heterogeneous Multi-Robot System with Large Language Models](https://arxiv.org/abs/2409.15146) `MA` | 2024 | gpt-4-0125-preview (centralized task assigner and per-robot executor LLMs) |
| [Combining Ontological Knowledge and Large Language Model for User-Friendly Service Robots](https://arxiv.org/abs/2410.16804) | 2024 | Llama 2 13B chat with LangChain prompting and dialog memory as commonsense locat |
| [ConceptAgent: LLM-Driven Precondition Grounding and Tree Search for Robust Task Planning and Execution](https://arxiv.org/abs/2410.06108) | 2024 | Llama 3.1 70B for all sim experiments (GPT-4 in real Spot trials), LLM-MCTS |
| [Continual Robot Skill and Task Learning via Dialogue](https://arxiv.org/abs/2409.03166) | 2024 | GPT-4.0 Turbo (dialog and skill sequencing) + ACT-LoRA skills (authors trained,  |
| [Conversational Language Models for Human-in-the-Loop Multi-Robot Coordination](https://arxiv.org/abs/2402.19166) `MA` | 2024 | GPT-4 vision preview (gpt-4-vision-preview), one agent per robot |
| [CoNVOI: Context-aware Navigation using Vision Language Models in Outdoor and Indoor Environments](https://arxiv.org/abs/2403.15637) | 2024 | GPT-4V and Gemini (large VLM, online API, no fine-tuning); CLIP for context clas |
| [Dadu‐E: Rethinking the Role of Large Language Model in Robotic Computing Pipelines](https://arxiv.org/abs/2412.01663) | 2024 | LLaMA 3.1-8B planner (used as-is); LLaVA-OneVision VLM for visual feedback |
| [DAG-Plan: Generating Directed Acyclic Dependency Graphs for Dual-Arm Cooperative Planning](https://arxiv.org/abs/2406.09953) | 2024 | GPT-4o (off-the-shelf) |
| [DART-LLM: Dependency-Aware Multi-Robot Task Decomposition and Execution using Large Language Models](https://arxiv.org/abs/2411.09022) `MA` | 2024 | Llama-3.1-8B, GPT-4o, GPT-3.5-turbo, Claude-3.5-Haiku, DeepSeek-r1-671B as QA LL |
| [DISCO: Language-Guided Manipulation With Diffusion Policies and Constrained Inpainting](https://arxiv.org/abs/2406.09767) | 2024 | ChatGPT-4 / 4o VLM writes 3D keyframes; authors' trained diffusion policy genera |
| [Dynamic Open-Vocabulary 3D Scene Graphs for Long-Term Language-Guided Mobile Manipulation](https://arxiv.org/abs/2410.11989) | 2024 | GPT-4o decomposes long-term tasks into subtasks (action and object names) |
| [Embodied AI with Two Arms: Zero-shot Learning, Safety and Modularity](https://arxiv.org/abs/2404.03570) | 2024 | PaLM-2 (340B) instruction-tuned LLM, in-context prompting; OWL-ViT VLM for perce |
| [EMOS: Embodiment-aware Heterogeneous Multi-robot Operating System with LLM Agents](https://arxiv.org/abs/2410.22662) `MA` | 2024 | GPT-4o (May 2024 API), one LLM agent per robot with robot resume, no training |
| [EMPOWER: Embodied Multi-role Open-vocabulary Planning with Online Grounding and Execution](https://arxiv.org/abs/2408.17379) `MA` | 2024 | GPT-4V (SMK and GMK agents) plus GPT-4 (Planner agent), multi-role prompting |
| [Enabling Novel Mission Operations and Interactions with ROSA: The Robot Operating System Agent](https://arxiv.org/abs/2410.06472) | 2024 | General tool-calling LLM in ReAct loop (GPT-4o recommended; Claude 3.5 Sonnet, L |
| [Enhancing Human-Robot Collaborative Assembly in Manufacturing Systems Using Large Language Models](https://arxiv.org/abs/2406.01915) | 2024 | GPT-4.0 (OpenAI pre-trained) |
| [Enhancing the LLM-Based Robot Manipulation Through Human-Robot Collaboration](https://arxiv.org/abs/2406.14097) | 2024 | GPT-4 Turbo (temperature 0), prompted |
| [Fast and Accurate Task Planning using Neuro-Symbolic Language Models and Multi-Level Goal Decomposition](https://arxiv.org/abs/2409.19250) | 2024 | GPT-4o (stated LLM; used as L-Model for subgoals and L-Policy in MCTS) |
| [FLAIR: Feeding via Long-horizon AcquIsition of Realistic dishes](https://arxiv.org/abs/2407.07561) | 2024 | GPT-4V（少样本提示，规划下一口喂食技能序列） |
| [FlexiFly: Interfacing the Physical World with Foundation Models Empowered by Reconfigurable Drone Systems](https://arxiv.org/abs/2403.12853) | 2024 | Llama-3.1-8B (LLM) and LLaVA 1.6-8b (VLM), off-the-shelf via Ollama; GPT-4 for t |
| [From Decision to Action in Surgical Autonomy: Multi-Modal Large Language Models for Robot-Assisted Blood Suction](https://arxiv.org/abs/2408.07806) | 2024 | GPT-4V（零样本多模态推理，给出吸血优先级顺序） |
| [GameVLM: A Decision-making Framework for Robotic Task Planning Based on Visual Language Models and Zero-sum Games](https://arxiv.org/abs/2405.13751) `MA` | 2024 | GPT-4V (two decision agents and one expert agent, prompted); YOLO-World detector |
| [General-Purpose Clothes Manipulation with Semantic Keypoints](https://arxiv.org/abs/2408.08160) | 2024 | LLM (unnamed in paper; prompted with CoT and few-shot examples, not fine-tuned) |
| [GraphEQA: Using 3D Semantic Scene Graphs for Real-time Embodied Question Answering](https://arxiv.org/abs/2412.14480) | 2024 | GPT-4o (also Gemini 2.5 Pro, Llama 4 Maverick) as VLM planner with scene-graph p |
| [Grounding Language Models in Autonomous Loco-manipulation Tasks](https://arxiv.org/abs/2409.01326) | 2024 | Unnamed LLM (prompted with function options and motion library) plus unnamed VLM |
| [Grounding LLMs For Robot Task Planning Using Closed-loop State Feedback](https://arxiv.org/abs/2402.08546) `MA` | 2024 | GPT-4 as Brain-LLM (planning) and Body-LLM (control statements) |
| [Guide-LLM: An Embodied LLM Agent and Text-Based Topological Map for Robotic Guidance of People with Visual Impairments](https://arxiv.org/abs/2410.20666) | 2024 | GPT-4o (central agent, prompted; no training) |
| [Guiding Long-Horizon Task and Motion Planning with Vision Language Models](https://arxiv.org/abs/2410.02193) | 2024 | gpt-4o-mini (temperature 0.2) as the VLM generating subgoals or actions |
| [HBTP: Heuristic Behavior Tree Planning with Large Language Model Reasoning](https://arxiv.org/abs/2406.00965) | 2024 | gpt-4o-mini (off-the-shelf, prompting only) |
| [HELPER-X: A Unified Instructable Embodied Agent to Tackle Four Interactive Vision-Language Domains with Memory-Augmented Language Models](https://arxiv.org/abs/2404.19065) | 2024 | GPT-4-0613 prompted with memory-retrieved language-program examples (no fine-tun |
| [Hierarchical Large Language Models in Cloud-Edge-End Architecture for Heterogeneous Robot Cluster Control](https://arxiv.org/abs/2402.03703) `MA` | 2024 | Unnamed cloud LLM (policy generation) plus unnamed visual and linguistic LLMs at |
| [Hierarchical LLMs in-the-Loop Optimization for Real-Time Multi-Robot Target Tracking Under Unknown Hazards](https://arxiv.org/abs/2409.12274) `MA` | 2024 | GPT-4o (sim headline), GPT-4.1-mini, LLaMA-3-70B, DeepSeek-V3; task and action L |
| [HYPERmotion: Learning Hybrid Behavior Planning for Autonomous Loco-manipulation](https://arxiv.org/abs/2406.14655) | 2024 | GPT-4o (LLM planner) + GPT-4V (VLM morphology selector) |
| [Industry 6.0: New Generation of Industry driven by Generative AI and Swarm of Heterogeneous Robots](https://arxiv.org/abs/2409.10106) `MA` | 2024 | OpenAI API LLMs via LangChain and LangGraph (GPT-4o recommended; o1-preview, Cla |
| [Integrating Disambiguation and User Preferences into Large Language Models for Robot Motion Planning](https://arxiv.org/abs/2404.14547) | 2024 | GPT-4 (disambiguation, preference memory, LTL translation); ada-002 plus random  |
| [Integrating Intent Understanding and Optimal Behavior Planning for Behavior Tree Generation from Human Instructions](https://arxiv.org/abs/2405.07474) | 2024 | GPT-3.5 Turbo (gpt-3.5-turbo, few-shot prompting plus reflective feedback, no fi |
| [Intelligent LiDAR Navigation: Leveraging External Information and Semantic Maps with LLM as Copilot](https://arxiv.org/abs/2409.08493) | 2024 | ChatGPT-4o (prompted for destination, passage costs and path approval; DeepSeek- |
| [ITCMA: A Generative Agent Based on a Computational Consciousness Structure](https://arxiv.org/abs/2403.20097) | 2024 | GPT-4 (action-selecting LLM, prompted); MiniGPT-v2 as VLM; fine-tuned ChatGLM3-6 |
| [KARMA: Augmenting Embodied AI Agents with Long-and-Short Term Memory Systems](https://arxiv.org/abs/2409.14908) | 2024 | GPT-4o as LLM planner, with GPT-4o as VLM for short-term memory state extraction |
| [LaMI: Large Language Models for Multi-Modal Human-Robot Interaction](https://arxiv.org/abs/2401.15174) | 2024 | GPT-4 (OpenAI tool API, prompted with guidance and examples) |
| [LaMMA-P: Generalizable Multi-Agent Long-Horizon Task Allocation and Planning with LM-Driven PDDL Planner](https://arxiv.org/abs/2409.20560) `MA` | 2024 | GPT-4o (headline system); Llama-3.1-8B and Llama-2-13B as alternative backends |
| [Language-Grounded Dynamic Scene Graphs for Interactive Object Search With Mobile Manipulation](https://arxiv.org/abs/2403.08605) | 2024 | gpt-4-1106-preview (high-level reasoning); gpt-3.5-turbo-1106 (room classificati |
| [Large Language Models for Orchestrating Bimanual Robots](https://arxiv.org/abs/2404.02018) | 2024 | GPT-4o (off-the-shelf via LangChain tool calls, prompted) |
| [LBAP: Improved Uncertainty Alignment of LLM Planners using Bayesian Inference](https://arxiv.org/abs/2403.13198) | 2024 | GPT-4 (off-the-shelf, MCQA prompting; GPT-3.5 fine-tuned only as baseline) |
| [LEMMo-Plan: LLM-Enhanced Learning from Multi-Modal Demonstration for Planning Sequential Contact-Rich Manipulation Tasks](https://arxiv.org/abs/2409.11863) | 2024 | GPT-4o (LLM analyzer and planner); fine-tuned TimeSformer only as tactile-event  |
| [Leveraging Large Language Model for Heterogeneous Ad Hoc Teamwork Collaboration](https://arxiv.org/abs/2406.12224) `MA` | 2024 | gpt-4-1106-preview (IRoT-LLM planner, training-free) |
| [LiP-LLM: Integrating Linear Programming and Dependency Graph With Large Language Models for Multi-Robot Task Planning](https://arxiv.org/abs/2410.21040) `MA` | 2024 | text-davinci-003 (LiP-LLM main system; GPT-4-0613 only in baselines) |
| [LIT: Large Language Model Driven Intention Tracking for Proactive Human-Robot Collaboration - A Robot Sous-Chef Application](https://arxiv.org/abs/2406.13787) | 2024 | LLaVA-13B (Vicuna backbone) used as both LLM and VLM |
| [LLCoach: Generating Robot Soccer Plans using Multi-Role Large Language Models](https://arxiv.org/abs/2406.18285) `MA` | 2024 | GPT-4 Turbo (vision coach) + GPT-3.5 Turbo (plan refinement and synchronization) |
| [LLM-as-BT-Planner: Leveraging LLMs for Behavior Tree Generation in Robot Task Planning](https://arxiv.org/abs/2409.10444) | 2024 | GPT-4 (in-context learning, main results); fine-tuned Mistral-7B, Llama2-13B, GP |
| [LLM-Based Cooperative Agents using Information Relevance and Plan Validation](https://arxiv.org/abs/2405.16751) `MA` | 2024 | GPT-4o-mini (also GPT-3.5, Llama-3.1-8B-Instruct as swappable backbones, no trai |
| [LLM-based Robot Task Planning with Exceptional Handling for General Purpose Service Robots](https://arxiv.org/abs/2405.15646) | 2024 | Baidu ERNIE-Bot 4.0 (off-the-shelf) |
| [LLM-BT: Performing Robotic Adaptive Tasks based on Large Language Models and Behavior Trees](https://arxiv.org/abs/2404.05134) | 2024 | ChatGPT (prompted for task steps) + authors' BERT keyword parser tool |
| [LLM-guided Task and Motion Planning using Knowledge-based Reasoning](https://arxiv.org/abs/2412.07493) | 2024 | GPT-4 used as-is with ontology-enriched prompts (also GPT, Gemini, LLaMA, Cohere |
| [LLM2Swarm: Robot Swarms that Responsively Reason, Plan, and Collaborate through LLMs](https://arxiv.org/abs/2410.11387) `MA` | 2024 | GPT-4o (one LLM instance per simulated robot; powerful LLM for controller synthe |
| [Long-horizon Locomotion and Manipulation on a Quadrupedal Robot with Large Language Models](https://arxiv.org/abs/2404.05291) `MA` | 2024 | GPT-4-turbo-preview as four prompted LLM agents (planner, calculator, coder, rep |
| [Long-Horizon Planning for Multi-Agent Robots in Partially Observable Environments](https://arxiv.org/abs/2407.10031) `MA` | 2024 | GPT-4V as underlying VLM for LLaMAR planner, actor, corrector and verifier modul |
| [MC-GPT: Empowering Vision-and-Language Navigation with Memory Map and Reasoning Chains](https://arxiv.org/abs/2405.10620) | 2024 | GPT-3.5-turbo与GPT-4o作为核心导航器（无需训练），InstructBLIP与检测器为工具 |
| [MEIA: Multimodal Embodied Perception and Interaction in Unknown Environments](https://arxiv.org/abs/2402.00290) | 2024 | GPT-4 Turbo (planning, with vision); GPT-3.5 Turbo (dialogue); zero-shot |
| [MHRC: Closed-loop Decentralized Multi-Heterogeneous Robot Collaboration with Large Language Models](https://arxiv.org/abs/2409.16030) `MA` | 2024 | GPT-4o (headline; GPT-3.5-turbo and Llama-3.1-8B also tested) as per-robot plann |
| [MOSAIC: Modular Foundation Models for Assistive and Interactive Cooking](https://arxiv.org/abs/2402.18796) `MA` | 2024 | GPT-4 API in behavior-tree Interactive Task Planner; trained RL and forecaster u |
| [Multi-Modal Grounded Planning and Efficient Replanning For Learning Embodied Agents with A Few Examples](https://arxiv.org/abs/2412.17288) | 2024 | GPT-4-0125-preview prompted with retrieved examples (GPT-3.5, LLaMA2-13B and Vic |
| [Multimodal Human-Autonomous Agents Interaction Using Pre-Trained Language and Visual Foundation Models](https://arxiv.org/abs/2403.12273) | 2024 | Off-the-shelf GPT-2 as LLMNode (BERT and LLaMA also tried) |
| [MultiTalk: Introspective and Extrospective Dialogue for Human-Environment-LLM Alignment](https://arxiv.org/abs/2409.16455) `MA` | 2024 | GPT-4o (Planner and Analyzer, two prompted instances) |
| [Nl2Hltl2Plan: Scaling Up Natural Language Understanding for Multi-Robots Through Hierarchical Temporal Logic Task Representation](https://arxiv.org/abs/2408.08188) | 2024 | GPT-4 (task tree, API action sequences); Mistral-7B-Instruct-v0.2 fine-tuned onl |
| [OceanPlan: Hierarchical Planning and Replanning for Natural Language AUV Piloting in Large-scale Unexplored Ocean Environments](https://arxiv.org/abs/2403.15369) | 2024 | Unnamed LLM planner and VLM (no model named) feeding HTN planner; DQN motion pol |
| [Open-Architecture End-to-End System for Real-World Autonomous Robot Navigation](https://arxiv.org/abs/2410.06239) | 2024 | GPT-4-Turbo high-level planner; LLaMA 3 4-bit labels rooms (component) |
| [Open-vocabulary Mobile Manipulation in Unseen Dynamic Environments with 3D Semantic Maps](https://arxiv.org/abs/2406.18115) | 2024 | GPT-4o (instruction parsing, region prioritization); InternVL 1.5 (VLM instance  |
| [OpenFMNav: Towards Open-Set Zero-Shot Object Navigation via Vision-Language Foundation Models](https://arxiv.org/abs/2402.10670) | 2024 | GPT-4 (text-only) for ProposeLLM and ReasonLLM; GPT-4V for DiscoverVLM |
| [Plan-Seq-Learn: Language Model Guided RL for Solving Long Horizon Robotics Tasks](https://arxiv.org/abs/2405.01534) | 2024 | GPT-4 as zero-shot LLM planner (prompted); RL policies trained per task by autho |
| [Planning and Reasoning with 3D Deformable Objects for Hierarchical Text-to-3D Robotic Shaping](https://arxiv.org/abs/2412.01765) | 2024 | Gemini 1.5 (segment planner and sub-goal generator, no finetuning) |
| [Polaris: Open-ended Interactive Robotic Manipulation via Syn2Real Visual Grounding and Large Language Models](https://arxiv.org/abs/2408.07975) | 2024 | GPT-4 (API, prompted as scene perception and interaction LLM) |
| [Policy Adaptation via Language Optimization: Decomposing Tasks for Few-Shot Imitation](https://arxiv.org/abs/2408.16228) | 2024 | GPT-4o (prompted backbone for subtask decompositions); ResNet-FiLM policy traine |
| [Probabilistically Correct Language-Based Multi-Robot Planning Using Conformal Prediction](https://arxiv.org/abs/2402.15368) `MA` | 2024 | GPT-3.5 (headline); Llama-2-7b and Llama-3-8b; one LLM per robot |
| [QuadrupedGPT: Towards a Versatile Quadruped Agent in Open-ended Worlds](https://arxiv.org/abs/2406.16578) | 2024 | GPT-4o (LMM for reasoning, gait parameters, cost-map segmentation) |
| [Real-world cooking robot system from recipes based on food state recognition using foundation models and PDDL](https://arxiv.org/abs/2410.02874) | 2024 | GPT-4 (gpt-4-0613, few-shot prompting) |
| [REBEL: Rule-based and Experience-enhanced Learning with LLMs for Initial Task Allocation in Multi-Human Multi-Robot Teaming](https://arxiv.org/abs/2409.16266) `MA` | 2024 | 未具名的通用LLM，以规则与经验检索提示推理（文中未点明型号） |
| [Remote Life Support Robot Interface System for Global Task Planning and Local Action Expansion Using Foundation Models](https://arxiv.org/abs/2411.10038) | 2024 | GPT-4 (LLM action sequence and JSON formatting); GPT-4V and GPT-4o (VLM info col |
| [RePLan: Robotic Replanning with Perception and Language Models](https://arxiv.org/abs/2401.04157) | 2024 | GPT-4 (high-level and low-level planner, verifier); Qwen-VL-Chat-7B (perceiver) |
| [ReplanVLM: Replanning Robotic Tasks With Visual Language Models](https://arxiv.org/abs/2407.21762) | 2024 | GPT-4V in Decision, Inner and Extra Bot prompt roles; YOLOv8 for detection |
| [Revolutionizing Battery Disassembly: The Design and Implementation of a Battery Disassembly Autonomous Mobile Manipulator Robot(BEAM-1)](https://arxiv.org/abs/2407.06590) | 2024 | LLM（未具名，提示+少样本示例）启发式搜索动作原语序列；神经谓词与RPSN为训练的工具 |
| [Robi Butler: Multimodal Remote Interaction with a Household Robot Assistant](https://arxiv.org/abs/2409.20548) | 2024 | GPT-4o-2024-05-13, prompted as a household robot assistant planner |
| [RoboEXP: Action-Conditioned Scene Graph via Interactive Exploration for Robotic Manipulation](https://arxiv.org/abs/2402.15487) | 2024 | GPT-4V (action proposer and action verifier) |
| [ROS-LLM: A ROS framework for embodied AI with task feedback and structured reasoning](https://arxiv.org/abs/2406.19741) | 2024 | DeepSeek 7B Coder (open-source, vLLM server, prompted) |
| [Safe Planner: Empowering Safety Awareness in Large Pre-Trained Models for Robot Task Planning](https://arxiv.org/abs/2411.06920) | 2024 | GPT-4v as VLM planner; GPT-4 as PDDL task translator; safety predictor and PPO s |
| [SARO: Space-Aware Robot System for Terrain Crossing via Vision-Language Model](https://arxiv.org/abs/2407.16412) | 2024 | LLaVA-34B（预训练VLM，零样本提示，负责子任务分解与视觉判别） |
| [SayComply: Grounding Field Robotic Tasks in Operational Compliance Through Retrieval-Based Language Models](https://arxiv.org/abs/2411.11323) | 2024 | GPT-4 (compliant task planner and LLM context retrieval) |
| [Semantic Skill Grounding for Embodied Instruction-Following in Cross-Domain Environments](https://arxiv.org/abs/2408.01024) | 2024 | GPT-3.5 Turbo（任务规划器与评判器的LM部分，上下文学习）；微调的InstructBLIP仅作感知工具 |
| [Semantic-Geometric-Physical-Driven Robot Manipulation Skill Transfer via Skill Library and Tactile Representation](https://arxiv.org/abs/2411.11714) | 2024 | GPT-4o (task-level subtask sequence planner over KG skill library) |
| [Sequential Discrete Action Selection via Blocking Conditions and Resolutions](https://arxiv.org/abs/2409.08410) | 2024 | GPT-3.5 Turbo, zero-shot prompting as the action selection engine |
| [ShapeGrasp: Zero-Shot Task-Oriented Grasping with Large Language Models through Geometric Decomposition](https://arxiv.org/abs/2403.18062) | 2024 | GPT-4 (multi-stage prompt chain; Starling as alternative backend) |
| [Sketch-MoMa: Teleoperation for Mobile Manipulator via Interpretation of Hand-Drawn Sketches](https://arxiv.org/abs/2412.19153) | 2024 | GPT-4V used as-is with few-shot prompts to infer task and sketch shape |
| [Socratic Planner: Self-QA-Based Zero-Shot Planning for Embodied Instruction Following](https://arxiv.org/abs/2404.15190) | 2024 | GPT-4o prompted zero-shot for self-QA decomposition, subgoal planning and MLLM v |
| [SPINE: Online Semantic Planning for Missions with Incomplete Natural Language Specifications in Unstructured Environments](https://arxiv.org/abs/2410.03035) | 2024 | GPT-4 base model as plan generator via in-context prompts |
| [SwarmGPT: Combining Large Language Models With Safe Motion Planning for Drone Swarm Choreography](https://arxiv.org/abs/2412.08428) `MA` | 2024 | GPT-4 used as-is to write drone swarm choreography (waypoints or motion primitiv |
| [TANGO: Training-free Embodied AI Agents for Open-world Tasks](https://arxiv.org/abs/2412.10402) | 2024 | GPT-4o as planner composing navigation and detection primitives |
| [Text2Interaction: Establishing Safe and Preferable Human-Robot Interaction](https://arxiv.org/abs/2408.06105) | 2024 | GPT-4 (gpt-4-0125-preview), prompted with in-context examples, no training |
| [The Conversation is the Command: Interacting with Real-World Autonomous Robots Through Natural Language](https://arxiv.org/abs/2401.11838) | 2024 | GPT-2 (off-the-shelf pre-trained, unmodified) |
| [ThinkGrasp: A Vision-Language System for Strategic Part Grasping in Clutter](https://arxiv.org/abs/2407.11298) | 2024 | GPT-4o, prompted, no training |
| [To Help or Not to Help: LLM-based Attentive Support for Human-Robot Group Interactions](https://arxiv.org/abs/2403.12533) | 2024 | gpt-4-1106-preview (off-the-shelf, tool use, temperature 1e-8) |
| [Towards Coarse-grained Visual Language Navigation Task Planning Enhanced by Event Knowledge Graph](https://arxiv.org/abs/2408.02535) | 2024 | ChatGPT（子任务规划，检索增强提示）+ 作者训练的Transformer动作模型 |
| [Towards Efficient LLM Grounding for Embodied Multi-Agent Collaboration](https://arxiv.org/abs/2405.14314) `MA` | 2024 | GPT-4-Turbo as LLM planner (prompted); critic network trained by authors as feed |
| [Towards Human Awareness in Robot Task Planning with Large Language Models](https://arxiv.org/abs/2404.11267) | 2024 | LLM (model not named; prompted, no training described) |
| [Trust the PRoC3S: Solving Long-Horizon Robotics Problems with LLMs and Constraint Satisfaction](https://arxiv.org/abs/2406.05572) | 2024 | GPT-4 (gpt-4-0125-preview), prompted |
| [TrustNavGPT: Modeling Uncertainty to Improve Trustworthiness of Audio-Guided LLM-Based Robot Navigation](https://arxiv.org/abs/2408.01867) | 2024 | 未具名的LLM（思维链+少样本上下文学习，选项对数概率）；Whisper与现成检测器为工具 |
| [VADER: Visual Affordance Detection and Error Recovery for Multi Robot Human Collaboration](https://arxiv.org/abs/2405.16021) `MA` | 2024 | PaLM (LMP planner, prompted) with PaLI/CLIP/ViLD VQA |
| [Verifiably Following Complex Robot Instructions with Foundation Models](https://arxiv.org/abs/2402.11498) | 2024 | GPT-4-0613 (in-context LTL translation) |
| [VeriGraph: Scene Graphs for Execution Verifiable Robot Planning](https://arxiv.org/abs/2411.10446) | 2024 | GPT-4 task planner P; GPT-4V scene graph generator |
| [VLM See, Robot Do: Human Demo Video to Robot Action Plan via Vision Language Model](https://arxiv.org/abs/2410.08792) | 2024 | GPT-4o (gpt-4o-2024-08-06) as VLM interpreter over keyframes |
| [VoicePilot: Harnessing LLMs as Speech Interfaces for Physically Assistive Robots](https://arxiv.org/abs/2404.04066) | 2024 | GPT-3.5 Turbo (OpenAI API, prompted, not trained) |
| [VoroNav: Voronoi-based Zero-shot Object Navigation with Large Language Model](https://arxiv.org/abs/2401.02695) | 2024 | GPT-3.5 (prompted waypoint selection; no training described) |
| [We Choose to Go to Space: Agent-driven Human and Multi-Robot Collaboration in Microgravity](https://arxiv.org/abs/2402.14299) `MA` | 2024 | Unnamed foundation model (cited as GPT-4 technical report) in DMA planner and SE |
| [When Robots Get Chatty: Grounding Multimodal Human-Robot Conversation and Collaboration](https://arxiv.org/abs/2407.00518) | 2024 | GPT-3.5 (robot demo, per text); GPT-4, GPT-3.5, Mistral-7B, Vicuna-13B and -33B  |
| [Words2Contact: Identifying Support Contacts from Verbal Instructions Using Foundation Models](https://arxiv.org/abs/2407.14229) | 2024 | GPT-3.5-turbo (best in benchmark) with GroundingDINO and CLIPSeg; Calme-7b and M |
| [ZeroCAP: Zero-Shot Multi-Robot Context Aware Pattern Formation via Large Language Models](https://arxiv.org/abs/2404.02318) `MA` | 2024 | GPT-4 (default LLM; llama-2-70b and claude-3-opus also run) |
| [A Hierarchical Agentic Framework for Autonomous Drone-Based Visual Inspection](https://arxiv.org/abs/2510.00259) `MA` | 2025 | GPT-4.1 Nano / GPT-4.1 / o4-mini / o3 (head agent and worker agents) |
| [A Pragmatist Robot: Learning to Plan Tasks by Experiencing the Real World](https://arxiv.org/abs/2507.16713) | 2025 | gpt-4o VLM as planner, success detector and experience summarizer, no weight upd |
| [Adaptive Domain Modeling with Language Models: A Multi-Agent Approach to Task Planning](https://arxiv.org/abs/2506.19592) `MA` | 2025 | GPT-4o without fine-tuning as multi-agent PDDL generators plus ReAct plan execut |
| [AdaptPNP: Integrating Prehensile and Non-Prehensile Skills for Adaptive Robotic Manipulation](https://arxiv.org/abs/2511.11052) | 2025 | VLM planner (unnamed in text, zero-shot); GPT-4o for region reasoning; Seed1.5-V |
| [AERMANI-VLM: Structured Prompting and Reasoning for Aerial Manipulation with Vision Language Models](https://arxiv.org/abs/2511.01472) | 2025 | Gemini 3-Pro (headline); GPT-4o, Claude 3.5 Sonnet, Qwen2-VL-7B, LLaVA-Next-13B  |
| [Agentic Aerial Cinematography: From Dialogue Cues to Cinematic Trajectories](https://arxiv.org/abs/2509.16176) | 2025 | Gemini 2.5 Pro (VLM for waypoint selection and preference-based pose refinement) |
| [Agentic Robot: A Brain-Inspired Framework for Vision-Language-Action Models in Embodied Agents](https://arxiv.org/abs/2505.23450) | 2025 | GPT-4o planner (subgoal decomposition) calling OpenVLA executor and fine-tuned Q |
| [Agentic Scene Policies: Unifying Space, Semantics, and Affordances for Robot Action](https://arxiv.org/abs/2509.19571) | 2025 | Gemini 2.5 (LLM agent via LangChain; also VLM classifier and affordance predicto |
| [AINav: Large Language Model-Based Adaptive Interactive Navigation](https://arxiv.org/abs/2503.22942) | 2025 | GPT-4o (LLM proposer, evaluator, advisor, arborist) + RL-pretrained skill librar |
| [Air-Ground Collaboration for Language-Specified Missions in Unknown Environments](https://arxiv.org/abs/2505.09108) `MA` | 2025 | GPT-4o (SPINE plan generator on UGV); LLaVA only as perception enrichment tool |
| [An LLM-powered Natural-to-Robotic Language Translation Framework with Correctness Guarantees](https://arxiv.org/abs/2508.19074) | 2025 | GPT-4o / Gemini-1.5-Flash / Llama-70B / Gemma2-2b and 9b (prompting only, no tra |
| [AquaChat++: LLM-Assisted Multi-ROV Inspection for Aquaculture Net Pens with Integrated Battery Management and Thruster Fault Tolerance](https://arxiv.org/abs/2508.06554) `MA` | 2025 | GPT-4o powering each LLM agent (central planner, human-in-the-loop, per-ROV mult |
| [Architecting Large Action Models for Human-in-the-Loop Intelligent Robots](https://arxiv.org/abs/2512.11620) | 2025 | Unnamed general LLM in LangChain agents (size not stated) |
| [ARRC: Advanced Reasoning Robot Control - Knowledge-Driven Autonomous Manipulation Using Retrieval-Augmented Generation](https://arxiv.org/abs/2510.05547) | 2025 | Unnamed cloud LLM (no version given; Gemini only cited as an example) |
| [ArtiBench and ArtiBrain: Benchmarking Generalizable Vision-Language Articulated Object Manipulation](https://arxiv.org/abs/2511.20330) | 2025 | GPT-4.1 as VLM Task Reasoner; authors' trained ArtiDiffusion and GeoKeyframe con |
| [AuDeRe: Automated Strategy Decision and Realization in Robot Planning and Control via LLMs](https://arxiv.org/abs/2504.03015) | 2025 | GPT-4o (selects planner/controller APIs and writes integration code) |
| [BINDER: Instantly Adaptive Mobile Manipulation with Open-Vocabulary Commands](https://arxiv.org/abs/2511.22364) | 2025 | GPT-5 as DRM planner; off-the-shelf Qwen2.5-VL-3B as IRM Video-LLM |
| [BioMARS: A Multi-Agent Robotic System for Autonomous Biological Experiments](https://arxiv.org/abs/2507.01485) `MA` | 2025 | GPT-4o (Biologist, Technician); VLM (Inspector) |
| [Bridging VLM and KMP: Enabling Fine-Grained Robotic Manipulation via Semantic Keypoints Representation](https://arxiv.org/abs/2503.02748) | 2025 | GPT-4o via OpenAI API (GI and DI prompt modules) |
| [Casper: Inferring Diverse Intents for Assistive Teleoperation with Vision Language Models](https://arxiv.org/abs/2506.14727) | 2025 | GPT-4o as VLM (intent inference, candidate generation, skill parameters) |
| [CGoT: A Novel Inference Mechanism for Embodied Multi-Agent Systems Using Composable Graphs of Thoughts](https://arxiv.org/abs/2510.22235) `MA` | 2025 | LLM (unnamed) used for graph-of-thoughts inference by each agent |
| [Chat with UAV – human-UAV interaction based on large language models](https://arxiv.org/abs/2512.08145) `MA` | 2025 | ERNIE-4.0 and GPT-4o as base LLMs in planning and execution agents |
| [CityNavAgent: Aerial Vision-and-Language Navigation with Hierarchical Semantic Planning and Global Memory](https://arxiv.org/abs/2505.05622) | 2025 | GPT-4V (object reasoning and landmark-level planning); GPT-3.5 and LLaVA-7B only |
| [CLASP: General-Purpose Clothes Manipulation with Semantic Keypoints](https://arxiv.org/abs/2507.19983) | 2025 | GPT-4o as VLM producing keypoint task plans; pre-built skills executed via motio |
| [CLEA: Closed-Loop Embodied Agent for Enhancing Task Execution in Dynamic Environments](https://arxiv.org/abs/2503.00729) `MA` | 2025 | Qwen2.5-72B-Instruct (LLM planner and summarizer) and Qwen2.5-VL-72B-Instruct (o |
| [ConceptBot: Enhancing Robot's Autonomy through Task Decomposition with Large Language Models and Knowledge Graph](https://arxiv.org/abs/2509.00570) | 2025 | gpt-4o-mini (ChatGPT API, prompt-only) with ConceptNet retrieval |
| [Constrained natural language action planning for resilient embodied systems](https://arxiv.org/abs/2510.06357) | 2025 | Off-the-shelf LLM backbones (GPT-4o, GPT-4o-mini, Llama 3B-70B) with a PDDL symb |
| [Context Matters! Relaxing Goals with LLMs for Feasible 3D Scene Planning](https://arxiv.org/abs/2506.15828) | 2025 | GPT-4o |
| [Cooking Task Planning using LLM and Verified by Graph Network](https://arxiv.org/abs/2503.21564) | 2025 | ChatGPT-4o (few-shot LLM generating action plans, validated by FOON graph) |
| [CoordField: Coordination Field for Agentic UAV Task Allocation in Low-Altitude Urban Scenarios](https://arxiv.org/abs/2505.00091) | 2025 | DeepSeek-v3 API for NL parsing (GPT-4o, Claude-3.7, Gemini-2.5-Pro, LLaMA-4 comp |
| [Deploying Foundation Model-Enabled Air and Ground Robots in the Field: Challenges and Opportunities](https://arxiv.org/abs/2505.09477) | 2025 | GPT-4o (SPINE task planner for UGV/UAV field deployments); distilled Llama-3.2 3 |
| [DEXTER-LLM: Dynamic and Explainable Coordination of Multi-Robot Systems in Unknown Environments via Large Language Models](https://arxiv.org/abs/2508.14387) `MA` | 2025 | DeepSeek-V3 (subtask generation via multi-stage prompting) |
| [Distributed AI Agents for Cognitive Underwater Robot Autonomy](https://arxiv.org/abs/2507.23735) `MA` | 2025 | Unnamed general LLM agents, each prompt-configured via a Modelfile SYSTEM prompt |
| [DynaMIC: Dynamic Multimodal In-Context Learning Enabled Embodied Robot Counterfactual Resistance Ability](https://arxiv.org/abs/2509.24413) | 2025 | GPT-4 Turbo (task coordinator); CogVLM-17B (visual grounding) |
| [ELHPlan: Efficient Long-Horizon Task Planning for Multi-Agent Collaboration](https://arxiv.org/abs/2509.24230) `MA` | 2025 | GPT-4o (headline; GPT-4o-mini and Llama 3.1 also tested) |
| [Embodied Tree of Thoughts: Deliberate Manipulation Planning With Embodied World Model](https://arxiv.org/abs/2512.08188) | 2025 | GPT-4o as VLM for scene parsing, branch generation and failure diagnosis; AnyGra |
| [Endowing GPT-4 with a Humanoid Body: Building the Bridge Between Off-the-Shelf VLMs and the Physical World](https://arxiv.org/abs/2511.00041) | 2025 | GPT-4o (off-the-shelf via API) with trained diffusion motion executor as tool |
| [Enhancing Multi-Agent Systems via Reinforcement Learning with LLM-Based Planner and Graph-Based Policy](https://arxiv.org/abs/2503.10049) `MA` | 2025 | GPT-4 (planner, critic, reward and graph generator) plus RL-trained MARL meta-po |
| [Enter the Mind Palace: Reasoning and Planning for Long-term Active Embodied Question Answering](https://arxiv.org/abs/2507.12846) | 2025 | GPT-4o as language and vision model, zero-shot prompted, plans search over scene |
| [Executable Analytic Concepts as the Missing Link Between VLM Insight and Precise Manipulation](https://arxiv.org/abs/2510.07975) | 2025 | GPT-4o (open-source Qwen2.5-VL as alternative backend) |
| [Exploratory Retrieval-Augmented Planning For Continual Embodied Instruction Following](https://arxiv.org/abs/2509.08222) | 2025 | Llama-3-8B (default; Gemma-2B and Llama-3-70B in ablation), prompted with RAG an |
| [ExploreVLM: Closed-Loop Robot Exploration Task Planning with Vision-Language Models](https://arxiv.org/abs/2508.11918) | 2025 | GPT-4o (VLM planner with self-reflection and step-wise validator) |
| [Exploring GPT-4 for Robotic Agent Strategy with Real-Time State Feedback and a Reactive Behaviour Framework](https://arxiv.org/abs/2503.23601) | 2025 | GPT-4 (zero temperature, prompted; picks Director behaviour tasks) |
| [FAM-HRI: Foundation-Model Assisted Multimodal Human–Robot Interaction Combining Gaze and Speech](https://arxiv.org/abs/2503.16492) | 2025 | GPT-4o frozen (2024-08-06 checkpoint), prompted for gaze-speech referent and JSO |
| [FCRF: Flexible Constructivism Reflection for Long-Horizon Robotic Task Planning with Large Language Models](https://arxiv.org/abs/2507.14975) | 2025 | GPT-4o mini as Actor and Mentor LLMs, prompted (Reflexion-style) |
| [FLEET: Formal Language-Grounded Scheduling for Heterogeneous Robot Teams](https://arxiv.org/abs/2510.07417) `MA` | 2025 | gpt-4o and open-weight gpt-oss-20b as LLM front-end; each Spot runs its own LLM  |
| [FlexVLN: Flexible Adaptation for Diverse Vision-and-Language Navigation Tasks](https://arxiv.org/abs/2503.13966) | 2025 | GPT-4o / GPT-4o-mini LLM Planner (+ Qwen2-VL-7B verifier; trained R2R Instructio |
| [FlowPlan: Zero-Shot Task Planning with LLM Flow Engineering for Robotic Instruction Following](https://arxiv.org/abs/2503.02698) | 2025 | GPT-4 (GPT-4-0125-preview), zero-shot multi-stage prompting, as-is |
| [FrankenBot: Brain-Morphic Modular Orchestration for Robotic Manipulation with Vision-Language Models](https://arxiv.org/abs/2506.21627) | 2025 | GPT-4.1 (single VLM call per task generating execution tree and code); locally f |
| [Free-form language-based robotic reasoning and grasping](https://arxiv.org/abs/2503.13082) | 2025 | GPT-4o (zero-shot, mark-prompted); Molmo, LangSAM and grasp estimator as tools |
| [From Vague Instructions to Task Plans: A Feedback-Driven HRC Task Planning Framework based on LLMs](https://arxiv.org/abs/2503.01007) | 2025 | GPT-4o (also GPT-4, GPT-3.5-turbo) prompted; no training |
| [GameChat: Multi-LLM Dialogue for Safe, Agile, and Socially Optimal Multi-Agent Navigation in Constrained Environments](https://arxiv.org/abs/2503.12333) `MA` | 2025 | gpt-4o-mini (one prompted instance per robot); no training |
| [General-Purpose Robotic Navigation via LVLM-Orchestrated Perception, Reasoning, and Acting](https://arxiv.org/abs/2506.17462) | 2025 | GPT-4o |
| [GestOS: Advanced Hand Gesture Interpretation via Large Language Models to control Any Type of Robot](https://arxiv.org/abs/2509.14412) `MA` | 2025 | LLM (not named in paper; prompted with robot metadata and few-shot memory) |
| [GET: Goal-directed Exploration and Targeting for Large-Scale Unknown Environments](https://arxiv.org/abs/2505.20828) | 2025 | GPT-4o-mini (LLM Proposer in DoUT reasoning search on a two-wheeled robot) |
| [GhostShell: Streaming LLM Function Calls for Concurrent Embodied Programming](https://arxiv.org/abs/2508.05298) | 2025 | 21 off-the-shelf LLMs/LMMs from 9 providers via official APIs; Claude-Sonnet-4 a |
| [Graphormer-Guided Task Planning: Beyond Static Rules with LLM Safety Perception](https://arxiv.org/abs/2503.06866) | 2025 | LLM (model not named in paper) for risk annotation and replanning; Graphormer as |
| [Grounded Vision-Language Interpreter for Long-Horizon Bimanual Task and Motion Planning](https://arxiv.org/abs/2506.03270) | 2025 | GPT-4o (ViLaIn PDDL generation and corrective planning); Qwen2.5-VL-7B-Instruct  |
| [Grounding Language Models with Semantic Digital Twins for Robotic Planning](https://arxiv.org/abs/2506.16493) | 2025 | LLM (model not named in paper) with semantic digital twin context |
| [HELP: Hierarchical Embodied Language Planner for Household Tasks](https://arxiv.org/abs/2512.21723) `MA` | 2025 | Open 7-13B LLMs (Vicuna-7B/13B) in HLP and LLP agents, in-context only |
| [Heterogeneous Robot Collaboration in Unstructured Environments with Grounded Generative Intelligence](https://arxiv.org/abs/2510.26915) `MA` | 2025 | GPT-4.1 (subtask generation LLM) |
| [Hierarchical DLO Routing with Reinforcement Learning and In-Context Vision-Language Models](https://arxiv.org/abs/2510.19268) | 2025 | GPT-5 (low reasoning effort) as in-context VLM planner |
| [Hierarchical Language Models for Semantic Navigation and Manipulation in an Aerial‐Ground Robotic System](https://arxiv.org/abs/2506.05020) `MA` | 2025 | Gemini-2.0-pro (prompted LLM for reasoning) + fine-tuned Gemini-2.0-flash VLM as |
| [Hierarchical Planning for Complex Tasks with Knowledge Graph-RAG and Symbolic Verification](https://arxiv.org/abs/2504.04578) | 2025 | Phi-3-mini-4k-instruct and gemini-1.5-flash (frozen, prompted LLM planners) |
| [Hierarchical Vision-Language Planning for Multi-Step Humanoid Manipulation](https://arxiv.org/abs/2506.22827) | 2025 | GPT-4o planner + Gemini-2.0-Flash-Lite monitor |
| [Human-like Navigation in a World Built for Humans](https://arxiv.org/abs/2509.21189) | 2025 | GPT-4.1 (VLM planner using landmark memory and map image, prompted zero-shot) |
| [Humanoid Agent via Embodied Chain-of-Action Reasoning with Multimodal Foundation Models for Zero-Shot Loco-Manipulation](https://arxiv.org/abs/2504.09532) | 2025 | GPT-4V (VLM scene description) + GPT-4 (LLM reasoning chains), prompted; trained |
| [IDfRA: Self-Verification for Iterative Design in Robotic Assembly](https://arxiv.org/abs/2509.16998) | 2025 | GPT-4o (Judge, three Replanner instances, Selector; accessed via OpenAI API) |
| [In-situ Value-aligned Human-Robot Interactions with Physical Constraints](https://arxiv.org/abs/2508.07606) | 2025 | GPT-3.5 Turbo as in-context LLM planner (no training) |
| [Instruction-Augmented Long-Horizon Planning: Embedding Grounding Mechanisms in Embodied Mobile Manipulation](https://arxiv.org/abs/2503.08084) | 2025 | GPT-4o (prompted, no training) |
| [Integrating LMM Planners and 3D Skill Policies for Generalizable Manipulation](https://arxiv.org/abs/2501.18733) | 2025 | GPT-4V (general LMM planner, prompted with critic and memory, not fine-tuned) +  |
| [Integrating Retrospective Framework in Multi-Robot Collaboration](https://arxiv.org/abs/2502.11227) `MA` | 2025 | Llama 3.1-70B (LLM1 discussion and planning) + Llama 3.1-8B (LLM2 retrospective  |
| [Intent-Driven LLM Ensemble Planning for Flexible Multi-Robot Disassembly: Demonstration on EV Batteries](https://arxiv.org/abs/2510.17576) `MA` | 2025 | Qwen3-32B ensemble (1/3/6 seeds) plus Qwen3-32B LLM verifier |
| [Intention: Inferring Tendencies of Humanoid Robot Motion Through Interactive Intuition and Grounded VLM](https://arxiv.org/abs/2508.04931) | 2025 | OpenAI o4-mini via API as Intuitive Perceptor, planner and evaluator; humanoid m |
| [Interleaved LLM and Motion Planning for Generalized Multi-Object Collection in Large Scene Graphs](https://arxiv.org/abs/2507.15782) | 2025 | Unnamed LLM, prompted for high-level graph-search task plans (no training descri |
| [KeyMPs: One-Shot Vision-Language Guided Motion Generation by Sequencing DMPs for Occlusion-Rich Tasks](https://arxiv.org/abs/2504.10011) | 2025 | GPT-4o (two VLM calls: keyword primitive selection and keypoint pairs) |
| [Kinodynamic Task and Motion Planning using VLM-guided and Interleaved Sampling](https://arxiv.org/abs/2510.26139) | 2025 | GPT-4o (VLM, temperature 0) |
| [L3M+P: Lifelong Planning with Large Language Models](https://arxiv.org/abs/2508.01917) | 2025 | GPT-4o (no fine-tuning; LAPKT SIW-THEN-BFSF planner) |
| [Lang2manip: A Tool for LLM-Based Symbolic-To-Geometric Planning for Manipulation](https://arxiv.org/abs/2512.17062) | 2025 | GPT-4 (text planner, prompted; framework claimed model-agnostic) |
| [LangPert: Detecting and Handling Task-level Perturbations for Robust Object Rearrangement](https://arxiv.org/abs/2504.09893) | 2025 | Llama 3.1-8B in-context planner + fine-tuned BLIP-3 monitor (VLM tool) |
| [Language-Grounded Hierarchical Planning and Execution with Multi-Robot 3D Scene Graphs](https://arxiv.org/abs/2506.07454) `MA` | 2025 | off-the-shelf LLM (end-to-end model not named; ablation covers GPT-4o, GPT-4.1,  |
| [Language-Guided Long Horizon Manipulation with LLM-based Planning and Visual Perception](https://arxiv.org/abs/2509.02324) | 2025 | GPT-4o task planner (in-context and CoT prompting) calling DoRA-tuned SigLIP2 pe |
| [Language-in-the-Loop Culvert Inspection on the Erie Canal](https://arxiv.org/abs/2509.21370) | 2025 | GPT-5 (ROI proposals and post-re-imaging assessment, via OpenAI API) |
| [Learn as Individuals, Evolve as a Team: Multi-agent LLMs Adaptation in Embodied Environments](https://arxiv.org/abs/2506.07232) `MA` | 2025 | LLaMA 3.1-70B and GPT-4o planners (two-agent LIET); LoRA-tuned LLaMA 3.2-1B util |
| [Learn from the Past: Language-conditioned Object Rearrangement with Large Language Models](https://arxiv.org/abs/2501.18516) | 2025 | ChatGPT-4 (headline; Mistral-7B and Llama3-8B as alternate backbones) with RAG o |
| [Learning Adaptive Dexterous Grasping from Single Demonstrations](https://arxiv.org/abs/2503.20208) | 2025 | GPT-4 as VLM skill selector; PPO-trained grasp skills as callable tools |
| [Learning Affordances at Inference-Time for Vision-Language-Action Models](https://arxiv.org/abs/2510.19752) | 2025 | GPT-5-mini (high-level VLM for reasoning and VLM judge); pi0.5-DROID VLA as low- |
| [Learning Generalizable Language-Conditioned Cloth Manipulation from Long Demonstrations](https://arxiv.org/abs/2503.04557) | 2025 | LLM planner (model unnamed; GPT-4o chosen for skill discovery) few-shot prompted |
| [LEO-RobotAgent: A General-purpose Robotic Agent for Language-driven Embodied Operator](https://arxiv.org/abs/2512.10605) | 2025 | Qwen3-Max as off-the-shelf LLM for all experiments |
| [Leveraging LLMs for Mission Planning in Precision Agriculture](https://arxiv.org/abs/2506.10093) | 2025 | GPT-4o (cloud mission planner producing L1 XML behavior-tree plans for a ClearPa |
| [LLM+MAP: Bimanual Robot Task Planning using Large Language Models and Planning Domain Definition Language](https://arxiv.org/abs/2503.17309) | 2025 | GPT-4o (PDDL writer; symbolic multi-agent planner solves) |
| [LLM-Based Generalizable Hierarchical Task Planning and Execution for Heterogeneous Robot Teams with Event-Driven Replanning](https://arxiv.org/abs/2511.22354) `MA` | 2025 | Central Task Manager LLM plus per-robot LLMs; GPT-4o in hardware runs, GPT-4.1 f |
| [LLM-Driven Self-Refinement for Embodied Drone Task Planning](https://arxiv.org/abs/2508.15501) | 2025 | Unnamed remote cloud LLM (GPT/Gemini/DeepSeek/Qwen listed as compatible), one-sh |
| [LLM-drone: aerial additive manufacturing with drones planned using large language models](https://arxiv.org/abs/2503.17566) | 2025 | Claude 3.5 Sonnet (best of Claude 3.5 Sonnet, GPT-4o, Gemini 1.5 Pro tested; har |
| [LLM-Empowered Embodied Agent for Memory-Augmented Task Planning in Household Robotics](https://arxiv.org/abs/2504.21716) `MA` | 2025 | Qwen2.5-32B (planning, KB), LLaMA3.1-8B (routing), Gemma2-27B; off the shelf |
| [LLM-GROP: Visually Grounded Robot Task and Motion Planning with Large Language Models](https://arxiv.org/abs/2511.07727) | 2025 | GPT-3 text-davinci-003 as LLM component (GROP FCN is a trained tool) |
| [LLM-Guided Task- and Affordance-Level Exploration in Reinforcement Learning](https://arxiv.org/abs/2509.16615) | 2025 | GPT-4o (task and affordance planning, queried before training) |
| [LLM-HBT: Dynamic Behavior Tree Construction for Adaptive Coordination in Heterogeneous Robots](https://arxiv.org/abs/2510.09963) `MA` | 2025 | LLM (model not named in text) |
| [LookPlanGraph: Embodied Instruction Following Method with VLM Graph Augmentation](https://arxiv.org/abs/2512.21243) | 2025 | GPT-4o (gpt-4o-2024-08-06) as LM planner and VLM; Llama models as alternatives |
| [LOVON: Legged Open-Vocabulary Object Navigator](https://arxiv.org/abs/2507.06747) | 2025 | DeepSeek-R1 task planner; trained L2MM and YOLO-11 as tools |
| [Manual2Skill: Learning to Read Manuals and Acquire Robotic Skills for Furniture Assembly Using Vision-Language Models](https://arxiv.org/abs/2502.10090) | 2025 | GPT-4o (prompted once per manual to output hierarchical assembly graph); trained |
| [Mindeye-Omniassist: A Gaze-Driven LLM-Enhanced Assistive Robot System for Implicit Intention Recognition and Task Execution](https://arxiv.org/abs/2503.13250) | 2025 | DeepSeek-R1 (intent inference and action-sequence LLM; action-generation model n |
| [Mitigating Cross-Modal Distraction and Ensuring Geometric Feasibility via Affordance-Guided and Self-Consistent MLLMs for Task Planning in Instruction-Following Manipulation](https://arxiv.org/abs/2503.13055) | 2025 | GPT-4o (in-context, CoT with self-consistency, no fine-tuning) |
| [MORE: Mobile Manipulation Rearrangement Through Grounded Language Reasoning](https://arxiv.org/abs/2505.03035) | 2025 | GPT-4o (LLM task planner over filtered scene-graph subgraph); GPT-3.5 Turbo for  |
| [Multi-robot task planning for multi-object retrieval tasks with distributed on-site knowledge via large language models](https://arxiv.org/abs/2509.12838) `MA` | 2025 | GPT-4 (API gpt-4) with spatial-concept place and object priors in prompts |
| [NVP-HRI: Zero shot natural voice and posture-based human-robot interaction via large language model](https://arxiv.org/abs/2503.09335) | 2025 | GPT-4-turbo (central processor, prompt-constrained) |
| [ODYSSEY: Open-World Quadrupeds Exploration and Manipulation for Long-Horizon Tasks](https://arxiv.org/abs/2508.08240) | 2025 | GPT-4.1 (global planner); Qwen2.5-VL-72B-Instruct (contact point and end-effecto |
| [One For All: LLM-based Heterogeneous Mission Planning in Precision Agriculture](https://arxiv.org/abs/2506.10106) | 2025 | GPT-4o-2024-11-20 (temp 0.2) |
| [Open Scene Graphs for Open World Object-Goal Navigation](https://arxiv.org/abs/2508.04678) | 2025 | GPT-3.5 (scene-graph organisation and reasoning); GroundingDINO and BLIP-2 (perc |
| [osmAG-LLM: Zero-Shot Open-Vocabulary Object Navigation via Semantic Maps and Large Language Models Reasoning](https://arxiv.org/abs/2507.12753) | 2025 | Unnamed LLM (prompted) for node retrieval; ChatGPT-4V map augmentation; StepFun  |
| [PFEA: An LLM-based High-Level Natural Language Planning and Feedback Embodied Agent for Human-Centered AI](https://arxiv.org/abs/2510.24109) | 2025 | ChatGLM (planner and converter); VLM evaluator (unnamed) |
| [PhysiAgent: An Embodied Agent Framework in Physical World](https://arxiv.org/abs/2509.24524) | 2025 | Gemini 2.0 Flash (Planner, Reflector) and Gemini 2.0 Flash Lite (Monitor), with  |
| [PhysicalAgent: Towards General Cognitive Robotics with Foundation World Models](https://arxiv.org/abs/2509.13903) | 2025 | Gemini Pro Flash (VLM for task decomposition, prompts and monitoring); Wan 2.2 I |
| [Physically Ground Commonsense Knowledge for Articulated Object Manipulation with Analytic Concepts](https://arxiv.org/abs/2503.23348) | 2025 | GPT-4o (selects analytic concept and grasp/force knowledge; trained networks as  |
| [PIP-LLM: Integrating PDDL-Integer Programming with LLMs for Coordinating Multi-Robot Teams Using Natural Language](https://arxiv.org/abs/2510.22784) `MA` | 2025 | GPT-4o and Qwen-32B (off-the-shelf LLMs) |
| [Prime the search: Using large language models for guiding geometric task and motion planning by warm-starting tree search](https://arxiv.org/abs/2506.07062) | 2025 | gpt-4-turbo-2024-04-09 (Llama3.1-8B-Instruct as ablation) |
| [ProVox: Personalization and Proactive Planning for Situated Human-Robot Collaboration](https://arxiv.org/abs/2506.12248) | 2025 | GPT-4 Turbo (gpt-4-turbo-2024-04-09) as LM planner |
| [Quadrupped-Legged Robot Movement Plan Generation using Large Language Model](https://arxiv.org/abs/2512.21293) | 2025 | Vertex AI Gemini (version unspecified) as motion planner via cloud API |
| [ReAcTree: Hierarchical LLM Agent Trees with Control Flow for Long-Horizon Task Planning](https://arxiv.org/abs/2511.02424) | 2025 | Qwen 2.5 72B (also 7B, LLaMA 3.1 8B/70B, Phi-4) as few-shot LLM agent nodes in a |
| [Reflective VLM Planning for Dual-Arm Desktop Cleaning: Bridging Open-Vocabulary Perception and Precise Manipulation](https://arxiv.org/abs/2506.17328) | 2025 | Gemini-2.0-flash |
| [REFLEX: Metacognitive Reasoning for Reflective Zero-Shot Robotic Planning with Large Language Models](https://arxiv.org/abs/2505.14899) `MA` | 2025 | GPT-4 or LLaMA-3.1-70B, zero-shot prompted, as multi-robot arm agents |
| [ReLI: Cross-Lingual Language-to-Action Grounding for Human-Robot Interaction](https://arxiv.org/abs/2505.01862) | 2025 | GPT-4o (instruction-reasoning backend, off the shelf) |
| [REMAC: Self-Reflective and Self-Evolving Multi-Agent Collaboration for Long-Horizon Robot Manipulation](https://arxiv.org/abs/2503.22122) `MA` | 2025 | gpt-4o (VLM checks) + DeepSeek-R1 (planning and reflection), prompted |
| [Research on Navigation Methods Based on LLMs](https://arxiv.org/abs/2504.15600) | 2025 | DeepSeek-v3 (headline), GPT-4o mini, Phi-4-14B (off the shelf, function calling) |
| [RoboChemist: Long-Horizon and Safety-Compliant Robotic Chemical Experimentation](https://arxiv.org/abs/2509.08820) | 2025 | Qwen2.5-VL (planner, visual-prompt generator, monitor) plus fine-tuned pi0 VLA a |
| [RoboDexVLM: Visual Language Model-Enabled Task Planning and Motion Control for Dexterous Robot Manipulation](https://arxiv.org/abs/2503.01616) | 2025 | GPT-4o zero-shot as-is |
| [RoboPARA: Dual-Arm Robot Planning with Parallel Allocation and Recomposition Across Tasks](https://arxiv.org/abs/2506.06683) | 2025 | GPT-4o / DeepSeek V3 (LLM dependency-graph planner); ACT, DP, pi0 as System-1 to |
| [RoboPilot: Generalizable Dynamic Robotic Manipulation with Dual-thinking Modes](https://arxiv.org/abs/2510.00154) | 2025 | GPT-4o (zero-shot prompting, temperature 0; GPT-5 and DeepSeek-R1 also tested) |
| [Robot guide with multi-agent control and automatic scenario generation with LLM](https://arxiv.org/abs/2509.10317) | 2025 | GPT-4o (base, non-fine-tuned) for narrative and action-tag scenario generation |
| [Robot Operation of Home Appliances by Reading User Manuals](https://arxiv.org/abs/2505.20424) | 2025 | GPT-4o (builds appliance state-machine model and macro-action policy); Claude-3. |
| [RobotFleet: An Open-Source Framework for Centralized Multi-Robot Task Planning](https://arxiv.org/abs/2510.10379) `MA` | 2025 | GPT-4 (per footnote; LLM-based planner and allocator) |
| [RobotIQ: Empowering mobile robots with human-level planning for real-world execution](https://arxiv.org/abs/2502.12862) | 2025 | GPT-4 via OpenAI API as AI assistant core; RL navigation policy as a tool |
| [Safety Aware Task Planning via Large Language Models in Robotics](https://arxiv.org/abs/2503.15707) `MA` | 2025 | GPT-4o and DeepSeek-R1 (multi-LLM: task planner, safety planner, robot execution |
| [SAGE: Scene Graph-Aware Guidance and Execution for Long-Horizon Manipulation Tasks](https://arxiv.org/abs/2509.21928) | 2025 | GPT-4o (VLM scene parsing) + DeepSeek-R1 (LLM scene-graph transition planning) |
| [Scaffolding Dexterous Manipulation with Vision-Language Models](https://arxiv.org/abs/2506.19212) | 2025 | Gemini 2.5 Flash Thinking (VLM high-level planner) |
| [Scalable, Training-Free Visual Language Robotics: a modular multi-model framework for consumer-grade GPUs](https://arxiv.org/abs/2502.01071) | 2025 | Phi-3-mini-4k-instruct (3.8B, 4-bit) LLM + Mini-InternVL-Chat-2B VLM + CLIPSeg + |
| [Scene-agnostic Hierarchical Bimanual Task Planning via Visual Affordance Reasoning](https://arxiv.org/abs/2512.09310) | 2025 | GPT-4.1 for all language and VLM modules (object identification, subgoal plannin |
| [SDA-PLANNER: State-Dependency Aware Adaptive Planner for Embodied Task Planning](https://arxiv.org/abs/2509.26375) | 2025 | GPT-4o-mini prompted planner (Sda-Planner, no training described) |
| [Searching in Space and Time: Unified Memory-Action Loops for Open-World Object Retrieval](https://arxiv.org/abs/2511.14004) | 2025 | GPTo3 (LLM backbone, queried each step) |
| [Self-Corrective Task Planning by Inverse Prompting with Large Language Models](https://arxiv.org/abs/2503.07317) | 2025 | GPT-4o-mini (about 8B per paper) and Gemini-1.5-Flash, few-shot prompted, as-is |
| [Semantic Intelligence: Integrating GPT-4 with A Planning in Low-Cost Robotics](https://arxiv.org/abs/2505.01931) | 2025 | GPT-4 prompted as high-level selector over A* candidate paths (no fine-tuning);  |
| [Shake-VLA: Vision-Language-Action Model-Based System for Bimanual Robotic Manipulations and Liquid Mixing](https://arxiv.org/abs/2501.06919) | 2025 | GPT-4o used as-is for RAG recipe answers and robot API instruction generation; Y |
| [SIL: Symbiotic Interactive Learning for Language-Conditioned Human-Agent Co-Adaptation](https://arxiv.org/abs/2511.05203) | 2025 | GPT-4o (LLM backbone for parsing and interpretation); author-trained triplet-los |
| [STAR: A Foundation Model-driven Framework for Robust Task Planning and Failure Recovery in Robotic Systems](https://arxiv.org/abs/2503.06060) | 2025 | GPT-4 (task-tree generation, PDDL conversion) and GPT-4 Vision (failure detectio |
| [STEP Planner: Constructing cross-hierarchical subgoal tree as an embodied long-horizon task planner](https://arxiv.org/abs/2506.21030) | 2025 | GPT-4o on real robot (LLM unnamed in VirtualHome) |
| [TACOS: Task Agnostic COordinator of a multi-drone System](https://arxiv.org/abs/2510.01869) `MA` | 2025 | gpt-oss (open-weight) as Coordinator and Supervisor LLMs in sim runs; real-fligh |
| [Toward Accurate Long-Horizon Robotic Manipulation: Language-to-Action with Foundation Models via Scene Graphs](https://arxiv.org/abs/2510.27558) | 2025 | GPT-4.1 (interaction, function calling); Gemini 2.5 Pro (planning); Qwen2.5-VL 3 |
| [TP-MDDN: Task-Preferenced Multi-Demand-Driven Navigation with Autonomous Decision-Making](https://arxiv.org/abs/2511.17225) | 2025 | General LLM/MLLM for BreakLLM, LocateLLM and StatusMLLM (ablation: Qwen2.5-VL-72 |
| [Transforming Monolithic Foundation Models into Embodied Multi-Agent Architectures for Human-Robot Collaboration](https://arxiv.org/abs/2512.00797) `MA` | 2025 | GPT-4o (Perceiver, Assigner); DeepSeek-R1 (Manager, Verifier); authors' Qwen3-8B |
| [Trinity: A Modular Humanoid Robot AI System](https://arxiv.org/abs/2503.08338) | 2025 | GPT-4 (LLM task planner); RL locomotion policy and ManipVQA VLM are trained tool |
| [UAV-VLA: Vision-Language-Action System for Large Scale Aerial Mission Generation](https://arxiv.org/abs/2501.05014) | 2025 | GPT (version unstated) plus Molmo-7B-D 4-bit for object search, zero-shot |
| [UAV-VLRR: Vision-Language Informed NMPC for Rapid Response in UAV Search and Rescue](https://arxiv.org/abs/2503.02465) | 2025 | ChatGPT-4o as LLM agent (as-is) and Molmo-7B-D 4-bit VLM (as-is) |
| [Understanding physical properties of unseen deformable objects by leveraging large-language models and robot actions](https://arxiv.org/abs/2506.03760) | 2025 | GPT-4o (temp 0.2, top-p 0.7) with VLM detector |
| [Video-to-BT: Generating Reactive Behavior Trees from Human Demonstration Videos for Robotic Assembly](https://arxiv.org/abs/2509.16611) | 2025 | GPT-4o (VLM planner generating behavior trees from demo video; Qwen2.5-VL-72B an |
| [Vision to Geometry: 3D Spatial Memory for Sequential Embodied MLLM Reasoning and Exploration](https://arxiv.org/abs/2512.02458) | 2025 | Qwen2.5-VL-72B (default, training-free MLLM; GPT-5 also used as backbone) |
| [Visual Environment-Interactive Planning for Embodied Complex-Question Answering](https://arxiv.org/abs/2504.00775) | 2025 | Qwen2.5-14B for LLM-based planning on the robot (ChatGPT-4o and Qwen2.5-72B/32B/ |
| [VL-Nav: Neuro-Symbolic Reasoning-based Vision-Language Navigation](https://arxiv.org/abs/2502.00931) | 2025 | Qwen3-VL-8B (off-the-shelf VLM planner) + YOLO-World/FastSAM detectors as tools |
| [VLA-Touch: Enhancing Vision-Language-Action Models with Dual-Level Tactile Feedback](https://arxiv.org/abs/2507.17294) | 2025 | GPT-4o (task planner); RDT-1B VLA called as a skill; trained interpolant control |
| [VLA^2: Empowering Vision-Language-Action Models with an Agentic Framework for Unseen Concept Manipulation](https://arxiv.org/abs/2510.14902) | 2025 | GLM-4.1V-9B-Thinking (planner and cognition) + fine-tuned Qwen2.5-VL-3B verifier |
| [VLM-driven Behavior Tree for Context-aware Task Planning](https://arxiv.org/abs/2501.03968) | 2025 | GPT-4o generating behavior trees and evaluating visual conditions |
| [VLM-Driven Skill Selection for Robotic Assembly Tasks](https://arxiv.org/abs/2511.05680) | 2025 | GPT-4.1 (2025-04-14); GPT-5-mini (both prompted as VLM) |
| [VLM-TDP: VLM-guided Trajectory-conditioned Diffusion Policy for Robust Long-Horizon Manipulation](https://arxiv.org/abs/2507.04524) | 2025 | GPT-4o (VLM planner); trained trajectory-conditioned diffusion policy as tool |

</details>

<details><summary><b>Controller · Policy writing</b> (84)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Visual Language Maps for Robot Navigation](https://arxiv.org/abs/2210.05714) | 2022 | code-writing LLM (model unnamed in text; Codex cited as example) prompted with f |
| [Conditionally Combining Robot Skills using Large Language Models](https://arxiv.org/abs/2310.17019) | 2023 | GPT-3.5 / PaLM 2 prompted once per task for conditional-plan code; authors' PCBC |
| [Creative Robot Tool Use with Large Language Models](https://arxiv.org/abs/2310.13065) | 2023 | GPT-4 (four LLM modules: Analyzer, Planner, Calculator, Coder) |
| [Demo2Code: From Summarizing Demonstrations to Synthesizing Code via Extended Chain-of-Thought](https://arxiv.org/abs/2305.16744) | 2023 | gpt-3.5-turbo-16k (prompted, temperature 0) |
| [Generalizable Long-Horizon Manipulations with Large Language Models](https://arxiv.org/abs/2310.02264) | 2023 | GPT-3.5 (generates task conditions); DMP trajectory control as tool |
| [Gesture-Informed Robot Assistance via Foundation Models](https://arxiv.org/abs/2309.02721) | 2023 | GPT-3.5 (text-davinci-003, temperature 0), prompting only |
| [Ground Manipulator Primitive Tasks to Executable Actions using Large Language Models](https://arxiv.org/abs/2308.06810) | 2023 | GPT-4 (best 5-shot, 0.83 correct); GPT-3.5-turbo, Bard and LLaMA-2-70B also prom |
| [Instruct2Act: Mapping Multi-modality Instructions to Robotic Actions with Large Language Model](https://arxiv.org/abs/2305.11176) | 2023 | text-davinci-003 (OpenAI API) and ChatGPT, prompted without training |
| [LGMCTS: Language-Guided Monte-Carlo Tree Search for Executable Semantic Object Rearrangement](https://arxiv.org/abs/2309.15821) | 2023 | GPT-4 (language parsing into goal distributions); RAM and color detector as tool |
| [Multimodal Pretrained Models for Verifiable Sequential Decision-Making: Planning, Grounding, and Perception](https://arxiv.org/abs/2308.05295) | 2023 | GPT-4 (controller construction and grounding) with Grounded-SAM as perception to |
| [SayTap: Language to Quadrupedal Locomotion](https://arxiv.org/abs/2306.07580) | 2023 | GPT-4 (prompt design, in-context examples, temperature 0.5) |
| [SOCRATES: Text-based Human Search and Approach using a Robot Dog](https://arxiv.org/abs/2302.05324) | 2023 | GPT-3 (search prior, prompting only); VLM for human localization; waypoint gener |
| [Statler: State-Maintaining Language Models for Embodied Reasoning](https://arxiv.org/abs/2306.17840) | 2023 | Unnamed prompted LLMs (world-state reader and writer, model not named); MDETR se |
| [Tell Me Where to Go: A Composable Framework for Context-Aware Embodied Robot Navigation](https://arxiv.org/abs/2306.09523) | 2023 | GPT-3.5 (prompted, writes Python navigation code); GLIP detector and graph plann |
| [AIR-Embodied: An Efficient Active 3DGS-based Interaction and Reconstruction Framework with Embodied Large Language Model](https://arxiv.org/abs/2409.16019) | 2024 | GPT-4o (VoxPoser-style code generation with recursive LLM calls) |
| [Automatic Behavior Tree Expansion with LLMs for Robotic Manipulation](https://arxiv.org/abs/2409.13356) | 2024 | GPT-4-1106 (GPT-4 Turbo, off-the-shelf) |
| [Context-aware LLM-based Safe Control Against Latent Risks](https://arxiv.org/abs/2403.11863) | 2024 | GPT-4o (LLM vision, coder, correction, latent-risk modules; no fine-tuning) |
| [Creating and Repairing Robot Programs in Open-World Domains](https://arxiv.org/abs/2410.18893) | 2024 | GPT-4o writes task and recovery programs (Llama 3.1 and DeepSeek-Coder also test |
| [Discovering Object Attributes by Prompting Large Language Models With Perception-Action Apis](https://arxiv.org/abs/2409.15505) | 2024 | GPT-4 / GPT-4o (prompted with perception-action API, no training); GLIP and BLIP |
| [Don’t Let Your Robot Be Harmful: Responsible Robotic Manipulation via Safety-As-Policy](https://arxiv.org/abs/2411.18289) | 2024 | GPT-4o as LMM generating TAMP code, with inspector and reflector loop (world mod |
| [Enabling robots to follow abstract instructions and complete complex dynamic tasks](https://arxiv.org/abs/2406.11231) | 2024 | GPT-4 with RAG over a curated code-example knowledge base, prompted |
| [Enhancing Robustness in Language-Driven Robotics: A Modular Approach to Failure Reduction](https://arxiv.org/abs/2411.05474) | 2024 | LLaMA3.1-8B run locally as planner and execution module (no training); Deepseek- |
| [EnvBridge: Bridging Diverse Environments with Cross-Environment Knowledge Transfer for Embodied AI](https://arxiv.org/abs/2410.16919) | 2024 | GPT-4o-mini (RLBench, CALVIN) and GPT-4o (MetaWorld), prompted code generation |
| [FlockGPT: Guiding UAV Flocking with Linguistic Orchestration](https://arxiv.org/abs/2405.05872) `MA` | 2024 | GPT-4 (OpenAI API, base model, no fine-tuning); SDF library few-shot prompting |
| [GenCHiP: Generating Robot Policy Code for High-Precision and Contact-Rich Manipulation Tasks](https://arxiv.org/abs/2404.06645) | 2024 | GPT-4 (gpt-4-0613, temperature 0, prompting only); trained pose estimator as a t |
| [Generative Expressive Robot Behaviors using Large Language Models](https://arxiv.org/abs/2401.14673) | 2024 | GPT-4 (gpt-4-0613, frozen, modular prompt chain) |
| [GRAPPA: Generalizing and Adapting Robot Policies via Online Agentic Guidance](https://arxiv.org/abs/2410.06473) `MA` | 2024 | gpt-4o-mini (API) in Advisor, Grounding, Monitor and Robotic agent roles |
| [Hey Robot! Personalizing Robot Navigation Through Model Predictive Control with a Large Language Model](https://arxiv.org/abs/2409.13393) | 2024 | GPT-4o-mini via public API (prompted assistants, no training) |
| [IVLMap: Instance-Aware Visual Language Grounding for Consumer Robot Navigation](https://arxiv.org/abs/2403.19336) | 2024 | ChatGPT API (version unspecified) and Llama-2-13b-chat (4-bit GPTQ quantized by  |
| [MALMM: Multi-Agent Large Language Models for Zero-Shot Robotic Manipulation](https://arxiv.org/abs/2411.17636) `MA` | 2024 | gpt-4-turbo driving three agents (planner, coder, supervisor); LLaMA-3.3-70B var |
| [Meta-Control: Automatic Model-based Control Synthesis for Heterogeneous Robot Skills](https://arxiv.org/abs/2405.11380) | 2024 | GPT-4 ("GPT 4.0", temperature 1.0; GPT-4o in appendix A.4), prompted only |
| [NARRATE: Versatile Language Architecture for Optimal Control in Robotics](https://arxiv.org/abs/2403.10762) | 2024 | GPT-4 (pre-trained, used as-is) writes CasADi cost and constraints for MPC |
| [Open-World Task and Motion Planning via Vision-Language Model Generated Constraints](https://arxiv.org/abs/2411.08253) | 2024 | GPT-4o (no fine-tuning) for plan sketches and constraint code |
| [RoboMP2: A Robotic Multimodal Perception-Planning Framework with Multimodal Large Language Models](https://arxiv.org/abs/2404.04929) | 2024 | GPT-4V planner (as-is) with GPT-4/GPT-3.5 rewriter; trained GCMP perceptor as a  |
| [RoboScript: Code Generation for Free-Form Manipulation Tasks across Real and Simulation](https://arxiv.org/abs/2402.14623) | 2024 | GPT-4 main (GPT-3.5-turbo, Gemini-pro also tested) via in-context learning |
| [Sampling-Based Model Predictive Control for Dexterous Manipulation on a Biomimetic Tendon-Driven Hand](https://arxiv.org/abs/2411.06183) | 2024 | GPT-4o as VLM tuning MPC objective weights from video feedback |
| [SuFIA: Language-Guided Augmented Dexterity for Robotic Surgical Assistants](https://arxiv.org/abs/2405.05226) | 2024 | GPT-4 Turbo (prompted code generation, no training); trained segmentation networ |
| [Toward Automated Programming for Robotic Assembly Using ChatGPT](https://arxiv.org/abs/2405.08216) `MA` | 2024 | GPT-4 via OpenAI API, two prompted agents (task decomposition, script generation |
| [Towards an LLM-Based Speech Interface for Robot-Assisted Feeding](https://arxiv.org/abs/2410.20624) | 2024 | GPT-3.5 Turbo with tailored prompt, writes Python code for Obi robot |
| [Validation of the Scientific Literature via Chemputation Augmented by Large Language Models](https://arxiv.org/abs/2410.06384) `MA` | 2024 | GPT-4o (critique, XDL and procedure agents); GPT-4o-mini (scraping agent); no tr |
| [VernaCopter: Disambiguated Natural-Language-Driven Robot via Formal Specifications](https://arxiv.org/abs/2409.09536) | 2024 | GPT-4o |
| [VLMimic: Vision Language Models are Visual Imitation Learner for Fine-grained Actions](https://arxiv.org/abs/2410.20927) | 2024 | Unnamed general VLM (prompted, no training) + SAM-Track / Grounding DINO for vid |
| ["Don't Do That!": Guiding Embodied Systems through Large Language Model-based Constraint Generation](https://arxiv.org/abs/2506.04500) | 2025 | Llama-3.1-70B-Instruct (primary; other code LLMs tested) writing constraint func |
| [3D-Grounded Vision-Language Framework for Robotic Task Planning: Automated Prompt Synthesis and Supervised Reasoning](https://arxiv.org/abs/2502.08903) | 2025 | Frozen VLM (not named in main text) + LoRA-tuned SLM supervisor |
| [A Real-to-Sim-to-Real Approach to Robotic Manipulation with VLM-Generated Iterative Keypoint Rewards](https://arxiv.org/abs/2502.08643) | 2025 | GPT-4o (VLM writes per-step keypoint reward code during the task) |
| [Adaptive Articulated Object Manipulation on the Fly with Foundation Model Reasoning and Part Grounding](https://arxiv.org/abs/2507.18276) | 2025 | GPT-4o (frozen, training-free) writes control code; GroundingDINO, SAM and a tra |
| [AutoMisty: A Multi-Agent LLM Framework for Automated Code Generation in the Misty Social Robot](https://arxiv.org/abs/2503.06791) `MA` | 2025 | Unnamed LLM/VLM agents (backbone not stated; baselines ChatGPT-4o and o1) |
| [Chain-of-Modality: Learning Manipulation Programs from Multimodal Human Videos with Vision-Language-Models](https://arxiv.org/abs/2504.13351) | 2025 | Gemini 1.5 Pro and GPT-4o (prompting only) |
| [Code-as-Symbolic-Planner: Foundation Model-Based Robot Planning via Symbolic Code Generation](https://arxiv.org/abs/2503.01700) `MA` | 2025 | GPT-4o, Claude 3.5 Sonnet, Mistral-Large (same LLM as TaskLLM, SteerLLM, CheckLL |
| [CodeDiffuser: Attention-Enhanced Diffusion Policy via VLM-Generated Code for Instruction Ambiguity](https://arxiv.org/abs/2506.16652) | 2025 | ChatGPT-4o-class VLM (in-context prompting) writes perception code; trained diff |
| [Compositional Coordination for Multi-Robot Teams with Large Language Models](https://arxiv.org/abs/2507.16068) `MA` | 2025 | GPT-4.1 (mission analysis, behavior trees, robot code generation) |
| [EmbodiedCoder: Parameterized Embodied Mobile Manipulation via Modern Coding Model](https://arxiv.org/abs/2510.06207) | 2025 | Claude Sonnet-4 as coding model; Qwen2.5-VL-7B for grounding and decomposition |
| [FMimic: Foundation Models are Fine-grained Action Learners from Human Videos](https://arxiv.org/abs/2507.20622) | 2025 | unnamed VLM accessed via online APIs (task planner, trajectory code, failure cor |
| [GELATO: Multi-Instruction Trajectory Reshaping via Geometry-Aware Multiagent-based Orchestration](https://arxiv.org/abs/2509.06031) | 2025 | GPT-4o (VLM registration); GPT-4 or DeepSeek-V3 (LLM constraint translation) |
| [GenSwarm: Scalable Multi-Robot Code-Policy Generation and Deployment via Language Models](https://arxiv.org/abs/2503.23875) `MA` | 2025 | GPT-4o (multi-LLM agent team plus VLM critic, used out-of-the-box) |
| [GeoManip: Geometric Constraints as General Interfaces for Robot Manipulation](https://arxiv.org/abs/2501.09783) | 2025 | GPT-4o as VLM constraint generator and cost-code writer |
| [GSCE: a Prompt Framework With Enhanced Reasoning for Reliable LLM-Driven Drone Control](https://arxiv.org/abs/2502.12531) | 2025 | GPT-4-Turbo and GPT-4o (prompted GSCE framework) |
| [HyCodePolicy: Hybrid Language Controllers for Multimodal Monitoring and Decision in Embodied Agents](https://arxiv.org/abs/2508.02629) | 2025 | DeepSeek-V3 (program synthesis); moonshot-v1-32k-vision-preview (VLM monitoring  |
| [IMPACT: Intelligent Motion Planning with Acceptable Contact Trajectories via Vision-Language Models](https://arxiv.org/abs/2503.10110) | 2025 | GPT-4o (zero-shot object-cost assigner) |
| [KUDA: Keypoints to Unify Dynamics Learning and Visual Prompting for Open-Vocabulary Robotic Manipulation](https://arxiv.org/abs/2503.10546) | 2025 | GPT-4o (VLM writes keypoint target-spec code, few-shot prompted; trained dynamic |
| [LAMS: LLM-Driven Automatic Mode Switching for Assistive Teleoperation](https://arxiv.org/abs/2501.08558) | 2025 | GPT-4o used as-is with prompts and user-generated mode-switch examples (no train |
| [Large Language Model-Driven Closed-Loop UAV Operation With Semantic Observations](https://arxiv.org/abs/2507.01930) | 2025 | OpenAI o3-mini (code generator and evaluator, two configurations) |
| [LLM-Driven Corrective Robot Operation Code Generation with Static Text-Based Simulation](https://arxiv.org/abs/2512.02002) | 2025 | OpenAI o3-mini and o4-mini (code generator, LLM simulator and evaluator, prompte |
| [LLMs-guided adaptive compensator: Bringing Adaptivity to Automatic Control Systems with Large Language Models](https://arxiv.org/abs/2507.20509) | 2025 | Unnamed LLM (prompted only) designs compensator code for PD control loop |
| [LMPVC and Policy Bank: Adaptive voice control for industrial robots with code generating LLMs and reusable Pythonic policies](https://arxiv.org/abs/2506.22028) | 2025 | StarCoder2-15B (local code LLM, prompted, off-the-shelf) writing Pythonic robot  |
| [Long-Horizon Visual Imitation Learning via Plan and Code Reflection](https://arxiv.org/abs/2509.05368) | 2025 | GPT-4o or Qwen-VL-Max as VLM in plan, reflection and code modules |
| [LTLCodeGen: Code Generation of Syntactically Correct Temporal Logic for Robot Task Planning](https://arxiv.org/abs/2503.07902) | 2025 | GPT-4o (and GPT-4o-mini) writing LTL-producing code |
| [Maestro: Orchestrating Robotics Modules with Vision-Language Models for Zero-Shot Generalist Robots](https://arxiv.org/abs/2511.00917) | 2025 | VLM coding agent (unspecified general VLM) composing perception/planning/control |
| [Memory Transfer Planning: LLM-driven Context-Aware Code Adaptation for Robot Manipulation](https://arxiv.org/abs/2509.24160) | 2025 | GPT-4.1-mini (LLM planner for RLBench and CALVIN; VoxPoser-style LMPs) |
| [Meta-Optimization and Program Search using Language Models for Task and Motion Planning](https://arxiv.org/abs/2505.03725) | 2025 | GPT-4o-mini (gpt-4o-mini-2024-07-18) as program-search FM; CMA-ES and NLP/trajec |
| [Mixed-Initiative Dialog for Human-Robot Collaborative Manipulation](https://arxiv.org/abs/2508.05535) | 2025 | GPT-4o as LLM meta-planner coder; sim-trained Q-function networks as tools |
| [OpenNav: Open-World Navigation with Multimodal Large Language Models](https://arxiv.org/abs/2507.18033) | 2025 | ChatGPT-4o as MLLM trajectory-code planner; RAM, Grounding DINO, TAP as percepti |
| [OVAL-Grasp: Open-Vocabulary Affordance Localization for Task Oriented Grasping](https://arxiv.org/abs/2511.20841) | 2025 | GPT-4o (zero-shot part decomposition) + PartGLEE segmentation + ContactGraspNet |
| [OVITA: Open-Vocabulary Interpretable Trajectory Adaptations](https://arxiv.org/abs/2508.17260) | 2025 | GPT-4o, Claude 3 Opus and Gemini 1.5 Pro (prompted, training-free) writing adapt |
| [Perceiving, Reasoning, Adapting: A Dual-Layer Framework for VLM-Guided Precision Robotic Manipulation](https://arxiv.org/abs/2503.05064) | 2025 | GPT-4o, Claude 3.5, MiniCPM-V 2.6 as-is, wrapped by a progressive VLM planning l |
| [Robotic Long-Horizon Manipulation with Progressive In-Context Code Generation and Episodic Feedback](https://arxiv.org/abs/2503.21969) | 2025 | GPT-4o-mini (planner and reporter, prompted) |
| [Structured Task Solving via Modular Embodied Intelligence: A Case Study on Rubik's Cube](https://arxiv.org/abs/2507.05607) | 2025 | GPT-4 via OpenAI API (task decomposition and code generation); OWL-ViT and SAM a |
| [T-Rex: Task-Adaptive Spatial Representation Extraction for Robotic Manipulation with Vision-Language Models](https://arxiv.org/abs/2506.19498) | 2025 | GPT-4.1 (chain-of-grounding tool selection, constraint code, policy script) |
| [T3 Planner: A Self-Correcting LLM Framework for Robotic Motion Planning with Temporal Logic](https://arxiv.org/abs/2510.16767) | 2025 | Gemini-2.5-Pro prompted with CoT and few-shot in cascaded T3 Planner; Qwen3-4B d |
| [Text to Robotic Assembly of Multi Component Objects using 3D Generative AI and Vision Language Models](https://arxiv.org/abs/2511.02162) | 2025 | Gemini 2.5 Pro (zero-shot; three prompted queries) |
| [Towards Reliable Code-as-Policies: A Neuro-Symbolic Framework for Embodied Task Planning](https://arxiv.org/abs/2510.21302) | 2025 | GPT-4o-mini (code generation and feedback); Llama-3.2-3B (CSC scoring tool) |
| [Trajectory Adaptation using Large Language Models](https://arxiv.org/abs/2504.12755) | 2025 | GPT-4o (temperature 0.1, prompted, no fine-tuning) |
| [Triple-S: A Collaborative Multi-LLM Framework for Solving Long-Horizon Implicative Tasks in Robotics](https://arxiv.org/abs/2508.07421) `MA` | 2025 | LLaMA3-8B-Instruct and GPT-3.5-Turbo-0613 in Simplification, Solution and Summar |
| [Xpress: A System for Dynamic, Context-Aware Robot Facial Expressions Using Language Models](https://arxiv.org/abs/2503.00283) | 2025 | GPT-4 (code generation); GPT-4o and GPT-4o-mini (conversation LMs) |

</details>

<details><summary><b>Controller · Direct action</b> (49)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Discuss Before Moving: Visual Language Navigation via Multi-expert Discussions](https://arxiv.org/abs/2309.11382) `MA` | 2023 | GPT-4 (prompted DiscussNav agent; ChatGPT and InstructBLIP as expert tools) |
| [From text to motion: grounding GPT-4 in a humanoid robot “Alter3”](https://arxiv.org/abs/2312.06571) `MA` | 2023 | GPT-4 (gpt4-0314), prompt-driven Python code generation |
| [Language Models as Zero-Shot Trajectory Generators](https://arxiv.org/abs/2310.11604) | 2023 | GPT-4 (Python code emitting end-effector poses); LangSAM detection as tool |
| [LLM as A Robotic Brain: Unifying Egocentric Memory and Control](https://arxiv.org/abs/2304.09349) | 2023 | Multiple multimodal language models used zero-shot, with an embodied LLM as the  |
| [VELMA: Verbalization Embodiment of LLM Agents for Vision and Language Navigation in Street View](https://arxiv.org/abs/2307.06082) | 2023 | GPT-4少样本（两个上下文示例，VELMA-GPT-4）为主系统，GPT-3抽取地标；LLaMA-7b LoRA微调变体另有报告 |
| [3P-LLM: Probabilistic Path Planning using Large Language Model for Autonomous Robot Navigation](https://arxiv.org/abs/2403.18778) | 2024 | GPT-3.5-turbo via OpenAI API with prompt tuning |
| [Affordances-Oriented Planning using Foundation Models for Continuous Vision-Language Navigation](https://arxiv.org/abs/2407.05890) | 2024 | Gemini-1.5-Pro (low-level waypoint and path selection); GPT-4o (high-level PathA |
| [AI-Gadget Kit: Integrating Swarm User Interfaces with LLM-driven Agents for Rich Tabletop Game Applications](https://arxiv.org/abs/2407.17086) `MA` | 2024 | GPT-4（两个提示的LLM智能体：协调者与控制者） |
| [D-RMGPT: Robot-assisted collaborative tasks driven by large multimodal models](https://arxiv.org/abs/2408.11761) | 2024 | Off-the-shelf GPT-4V (DetGPT-V) and GPT-4 (R-ManGPT) planner |
| [Egocentric Vision Language Planning](https://arxiv.org/abs/2408.05802) | 2024 | GPT-4V prompted as the one-step planner for subgoal decomposition and action sel |
| [Embodied LLM Agents Learn to Cooperate in Organized Teams](https://arxiv.org/abs/2403.12482) `MA` | 2024 | GPT-4 / GPT-3.5-turbo / Llama2-70B（现成模型，靠提示组织团队结构） |
| [EmbodiedRAG: Dynamic 3D Scene Graph Retrieval for Efficient and Scalable Robot Task Planning](https://arxiv.org/abs/2410.23968) | 2024 | GPT-4o-mini (sim); llama3.1:8b (onboard Spot); ReAct agent with subgraph retriev |
| [EMOTION: Expressive Motion Sequence Generation for Humanoid Robots With In-Context Learning](https://arxiv.org/abs/2410.23234) | 2024 | GPT-4o (gpt-4o-2024-0513) via API, in-context learning |
| [Empowering Large Language Models on Robotic Manipulation with Affordance Prompting](https://arxiv.org/abs/2404.11027) | 2024 | GPT-4 (June/July, OpenAI API, zero-shot prompting, training-free); Grounding DIN |
| [Exploring Spatial Representation to Enhance LLM Reasoning in Aerial Vision-Language Navigation](https://arxiv.org/abs/2410.08500) | 2024 | GPT-4o (LLM planner and landmark extractor, prompted, training-free) |
| [GPT-Fabric: Folding and Smoothing Fabric by Leveraging Pre-Trained Foundation Models](https://arxiv.org/abs/2406.09640) | 2024 | GPT-4V (smoothing, folding), GPT-4 / GPT-3.5 for folding, prompted |
| [Harmon: Whole-Body Motion Generation of Humanoid Robots from Language Descriptions](https://arxiv.org/abs/2410.12773) | 2024 | GPT-4 as VLM editing PhysDiff-generated humanoid motion |
| [InCoRo: In-Context Learning for Robotics Control with Feedback Loops](https://arxiv.org/abs/2402.05188) | 2024 | gpt-3.5-turbo-0613 (off-the-shelf, in-context) |
| [Language Models are Spacecraft Operators](https://arxiv.org/abs/2404.00413) | 2024 | GPT-3.5 Turbo via OpenAI API (prompt engineering, few-shot, CoT; fine-tuned vari |
| [LLM-Craft: Robotic Crafting of Elasto-Plastic Objects With Large Language Models](https://arxiv.org/abs/2406.08648) | 2024 | Gemini 1.0 Pro Vision and Gemini 2.0 Flash, prompted, no finetuning |
| [MapGPT: Map-Guided Prompting with Adaptive Path Planning for Vision-and-Language Navigation](https://arxiv.org/abs/2401.07314) | 2024 | GPT-4 / GPT-4V zero-shot with map-guided prompts; no training |
| [Nadine: An LLM-driven Intelligent Social Robot with Affective Capabilities and Human-like Memory](https://arxiv.org/abs/2405.20189) | 2024 | GPT-4 (SoR-ReAct agent with prompting, tools and memory) |
| [Natural Language as Policies: Reasoning for Coordinate-Level Embodied Control with LLMs](https://arxiv.org/abs/2403.13801) | 2024 | GPT-3.5-turbo-1106 primary; GPT-4 supplementary; via assistant APIs with in-cont |
| [Perceive, Reflect, and Plan: Designing LLM Agent for Goal-Directed City Navigation without Instructions](https://arxiv.org/abs/2408.04168) | 2024 | GPT-4-turbo as base LLM for reflection, planning and actions (LLaVA-7B LoRA-FT o |
| [PLATO: Planning with LLMs and Affordances for Tool Manipulation](https://arxiv.org/abs/2409.11580) | 2024 | GPT-4o (scene comprehension, overall planner, step planner and grasp-mapping LLM |
| [Scene Exploration by Vision-Language Models](https://arxiv.org/abs/2409.17641) | 2024 | GPT-4o (VLM as perception analyzer and viewpoint decision-maker, zero-shot) |
| [TalkWithMachines: Enhancing Human-Robot Interaction Through Large/Vision Language Models](https://arxiv.org/abs/2412.15462) | 2024 | GPT-4 with text and image prompts via Python client |
| [Training microrobots to swim by a large language model](https://arxiv.org/abs/2402.00044) | 2024 | GPT-4 (few-shot prompted, temperature 0) |
| [Wonderful Team: Zero-Shot Physical Task Planning with Visual LLMs](https://arxiv.org/abs/2407.19094) `MA` | 2024 | GPT-4o（零样本多智能体VLLM团队：监督、验证、搬运、检查、记忆） |
| [Communication-Efficient Desire Alignment for Embodied Agent-Human Adaptation](https://arxiv.org/abs/2505.22503) | 2025 | GPT-4o（作为FAMER的目标推断、沟通与规划核心；Mask R-CNN感知为工具） |
| [DREAM: Domain-aware Reasoning for Efficient Autonomous Underwater Monitoring](https://arxiv.org/abs/2509.13666) | 2025 | GPT-5 (hand-crafted chain-of-thought prompt, reasoning model choosing high-level |
| [DyNaVLM: Zero-Shot Vision-Language Navigation System with Dynamic Viewpoints and Self-Refining Graph Memory](https://arxiv.org/abs/2506.15096) | 2025 | Gemini 2.0 Flash-Lite, zero-shot prompted, selects navigation points each step |
| [Enhancing reliability in LLM-integrated robotic systems: A unified approach to security and safety](https://arxiv.org/abs/2509.02163) | 2025 | GPT-4o (Brain module, zero-shot prompted) |
| [LA-RCS: LLM-Agent-Based Robot Control System](https://arxiv.org/abs/2505.18214) `MA` | 2025 | GPT-4o and GPT-4-Turbo as dual Host and App agents (API-based, no training) |
| [Large Models in Dialogue for Active Perception and Anomaly Detection](https://arxiv.org/abs/2501.16300) | 2025 | GPT-3.5 (prompted, zero-shot) |
| [LLM-Flock: Decentralized Multi-Robot Flocking via Large Language Models and Influence-Based Consensus](https://arxiv.org/abs/2505.06513) `MA` | 2025 | o3-mini, Claude 3.5 Sonnet, Llama3.1-405B, Qwen-Max, DeepSeek-R1 via API, one LL |
| [ManiAgent: An Agentic Framework for General Robotic Manipulation](https://arxiv.org/abs/2510.11660) `MA` | 2025 | GPT-5, GPT-4o, Claude-4-sonnet, Grok-4 as LLM/VLM in perception, reasoning and c |
| [MaP-AVR: A Meta-Action Planner for Agents Leveraging Vision Language Models and Retrieval-Augmented Generation](https://arxiv.org/abs/2512.19453) | 2025 | GPT-4o (VLM planner with RAG, CoT prompts, VLM pose selection) |
| [Multi-Agent LLM Actor-Critic Framework for Social Robot Navigation](https://arxiv.org/abs/2503.09758) `MA` | 2025 | GPT-4o / LLaMA-405B (prompted actors and critics, no training) |
| [Plantbot: Integrating Plant and Robot through LLM Modular Agent Networks](https://arxiv.org/abs/2509.05338) `MA` | 2025 | GPT-4V (Vision Agent); GPT-3.5 Turbo (Sensor, Chat, Action agents), prompted |
| [Reducing Latency in LLM-Based Natural Language Commands Processing for Robot Navigation](https://arxiv.org/abs/2506.00075) | 2025 | GPT-3.5 Turbo / GPT-4.0 (ChatGPT via OpenAI API) |
| [Robust Mobile Robot Path Planning via LLM-Based Dynamic Waypoint Generation](https://arxiv.org/abs/2501.15901) | 2025 | Llama3.1 8B via Ollama (prompted; Qwen2.5 7B and Mathstral also compared) |
| [Safe LLM-Controlled Robots with Formal Guarantees via Reachability Analysis](https://arxiv.org/abs/2503.03911) | 2025 | GPT-4o (temperature 0.1; 3-step plans, 5 for JetRacer) |
| [See, Point, Fly: A Learning-Free VLM Framework for Universal Unmanned Aerial Navigation](https://arxiv.org/abs/2509.22653) | 2025 | Gemini 2.0 Flash (frozen VLM backend) |
| [Semantic Glitch: Agency and Artistry in an Autonomous Pixel Cloud](https://arxiv.org/abs/2511.16048) | 2025 | Gemini 2.5 Flash (prompted two-stage PREAMBLE and DIRECTIONAL prompts) |
| [SIMPACT: Simulation-Enabled Action Planning using Vision-Language Models](https://arxiv.org/abs/2512.05955) | 2025 | Gemini 2.5 Pro as zero-shot VLM planner (sampling, optimization, success check)  |
| [SmartWay: Enhanced Waypoint Prediction and Backtracking for Zero-Shot Vision-and-Language Navigation](https://arxiv.org/abs/2503.10069) | 2025 | GPT-4o (gpt-4o-2024-08-06, zero-shot navigator); trained waypoint predictor as t |
| [Taking Flight with Dialogue: Enabling Natural Language Control for PX4-based Drone Agent](https://arxiv.org/abs/2506.07509) | 2025 | Ollama-served open LLMs/VLMs: Gemma3 (4B/12B), Qwen2.5-3B, Llama-3.2-3B, DeepSee |
| [Unfettered Forceful Skill Acquisition with Physical Reasoning and Coordinate Frame Labeling](https://arxiv.org/abs/2505.09731) | 2025 | Gemini 2.0 Flash (zero-shot, off-the-shelf) produces grasp point and wrench plan |

</details>

<details><summary><b>Supervisor · Monitoring / recovery</b> (32)</summary>

| Paper | Year | Decision model |
|---|---|---|
| [Robot Task Planning and Situation Handling in Open Worlds](https://arxiv.org/abs/2210.01287) | 2022 | GPT-3 (text-davinci-002, prompt templates, no training) |
| [CLARA: Classifying and Disambiguating User Commands for Reliable Interactive Robotic Agents](https://arxiv.org/abs/2306.10376) | 2023 | GPT-3.5-turbo (ChatGPT) prompted; InstructGPT text-davinci-003 and LLaMA 30B in  |
| [Integrating action knowledge and LLMs for task planning and situation handling in open worlds](https://arxiv.org/abs/2305.17590) | 2023 | GPT-3 text-davinci-003 (prompted, no training) |
| [REAL: Resilience and Adaptation using Large Language Models on Autonomous Aerial Robots](https://arxiv.org/abs/2311.01403) | 2023 | GPT-4 via OpenAI API, zero-shot prompt, queried onboard at 0.1-1 Hz |
| [Addressing Failures in Robotics using Vision-Based Language Models (VLMs) and Behavior Trees (BT)](https://arxiv.org/abs/2411.01568) | 2024 | GPT-4 (OpenAI, prompted; no training) |
| [Collaborative Instance Object Navigation: Leveraging Uncertainty-Awareness to Minimize Human-Agent Dialogues](https://arxiv.org/abs/2412.01250) | 2024 | GPT-4o (LLM) + LLaVA-1.6-Mistral-7B (VLM), training-free |
| [DKPROMPT: Domain Knowledge Prompting Vision-Language Models for Open-World Planning](https://arxiv.org/abs/2406.17659) | 2024 | GPT-4-turbo (gpt-4-turbo, off-the-shelf) |
| [E2Map: Experience-and-Emotion Map for Self-Reflective Robot Navigation with Language Models](https://arxiv.org/abs/2409.10027) | 2024 | GPT-4o (event descriptor) + Llama3 (emotion evaluator and goal selector) |
| [Evaluating Uncertainty-based Failure Detection for Closed-Loop LLM Planners](https://arxiv.org/abs/2406.00430) | 2024 | ChatGPT-4 planner with ChatGPT-4V or LLaVA failure detector (prompted, uncertain |
| [Foundation Models to the Rescue: Deadlock Resolution in Connected Multi-Robot Systems](https://arxiv.org/abs/2404.06413) `MA` | 2024 | GPT4, GPT3.5, Claude2, Claude3-Opus, GPT-4o (VLM) as prompted high-level planner |
| [Language-Augmented Symbolic Planner for Open-World Task Planning](https://arxiv.org/abs/2407.09792) | 2024 | GPT-4 repairs PDDL preconditions, objects and properties after execution errors; |
| [Recover: A Neuro-Symbolic Framework for Failure Detection and Recovery](https://arxiv.org/abs/2404.00756) | 2024 | GPT-4 as recovery re-planner; ontology rules detect failures |
| [Robot Failure Recovery Using Vision-Language Models With Optimized Prompts](https://arxiv.org/abs/2409.03966) | 2024 | GPT-4o (zero-shot, off-the-shelf) |
| [Semantically Safe Robot Manipulation: From Semantic Scene Understanding to Motion Safeguards](https://arxiv.org/abs/2410.15185) | 2024 | GPT-4o (prompted with in-context examples, majority voting) |
| [A Unified Framework for Real-Time Failure Handling in Robotics Using Vision-Language Models, Reactive Planner and Behavior Trees](https://arxiv.org/abs/2503.15202) | 2025 | GPT-4o-based VLM (off-the-shelf) with reactive planner and BTs |
| [Conditional Multi-Stage Failure Recovery for Embodied Agents](https://arxiv.org/abs/2507.06016) | 2025 | GPT-4o (also o3-mini, Qwen2.5-7B, Llama-3.1-8B), zero-shot chain prompting |
| [Drones that Think on their Feet: Sudden Landing Decisions with Embodied AI](https://arxiv.org/abs/2510.00167) | 2025 | GPT-5 / GPT-5-mini / GPT-5-nano (landing-site ranking and confirmation); Gemini  |
| [Dynamic Task Adaptation for Multi-Robot Manufacturing Systems with Large Language Models](https://arxiv.org/abs/2505.22804) `MA` | 2025 | GPT-4o (central controller agent) |
| [Foundation models on the bridge: Semantic hazard detection and safety maneuvers for maritime autonomy with vision-language models](https://arxiv.org/abs/2512.24470) | 2025 | GPT-5 variants (gpt-5-low for FB-3, gpt-5-medium in sea trial) plus other off-th |
| [From Words to Safety: Language-Conditioned Safety Filtering for Robot Navigation](https://arxiv.org/abs/2511.05889) | 2025 | GPT-4o (language-to-safety-config parser) |
| [LERa: Replanning with Visual Feedback in Instruction Following](https://arxiv.org/abs/2507.05135) | 2025 | GPT-4o / GPT-4o-mini / Gemini-1.5 Flash and Pro VLMs via API, not trained |
| [Leveraging Pre-trained Large Language Models with Refined Prompting for Online Task and Motion Planning](https://arxiv.org/abs/2504.21596) | 2025 | GPT-4 (GPT-4.0, FLP prompting; GPT-3.5-turbo also tested) |
| [MADRA: Multi-Agent Debate for Risk-Aware Embodied Planning](https://arxiv.org/abs/2511.21460) `MA` | 2025 | GPT-4o as debate agents, critical evaluator and planner (training-free) |
| [Online automatic code generation for robot swarms: LLMs and self-organizing hierarchy](https://arxiv.org/abs/2510.04774) `MA` | 2025 | DeepSeek R1 (via OpenRouter API), writes Lua swarm code |
| [RAIDER: Tool-Equipped Large Language Model Agent for Robotic Action Issue Detection, Explanation and Recovery](https://arxiv.org/abs/2503.17703) | 2025 | GPT-4o (gpt-4o-2024-05-13) zero-shot LLM agent with grounded perception tools |
| [Real-Time Out-of-Distribution Failure Prevention via Multi-Modal Reasoning](https://arxiv.org/abs/2505.10547) | 2025 | Molmo (goal points); Gemini 2.0 Flash, Claude 3.7 Sonnet, DeepSeek-R1 (failure-m |
| [RisConFix: LLM-based Automated Repair of Risk-Prone Drone Configurations](https://arxiv.org/abs/2512.07122) | 2025 | DeepSeek and Qwen (sizes not given) prompted to output corrective ArduPilot para |
| [RoboReflect: A Robotic Reflective Reasoning Framework for Grasping Ambiguous-Condition Objects](https://arxiv.org/abs/2501.09307) | 2025 | GPT-4V via OpenAI API used as-is with no in-context examples; SAM as tool |
| [RoboSafe: Safeguarding Embodied Agents via Executable Safety Logic](https://arxiv.org/abs/2512.21220) | 2025 | Gemini-2.5-flash as guardrail VLM (agents built on GPT-4o) |
| [Robust and Resilient Soft Robotic Object Insertion with Compliance-Enabled Contact Formation and Failure Recovery](https://arxiv.org/abs/2509.17666) | 2025 | GPT-4o (pre-trained VLM; per-skill success check and recovery planning) |
| [Scene Graph-Guided Proactive Replanning for Failure-Resilient Embodied Agent](https://arxiv.org/abs/2508.11286) | 2025 | GPT-4o (reasoning and replanning, all methods) |
| [VLM Can Be a Good Assistant: Enhancing Embodied Visual Tracking with Self-Improving Vision-Language Models](https://arxiv.org/abs/2505.20718) | 2025 | GPT-4o (VLM recovery reasoner); RL tracking policy is a trained tool |

</details>

<details><summary><b>Benchmarks and evaluation studies</b> (3)</summary>

| Paper | Year | Evaluated seat |
|---|---|---|
| [Exploring Large Language Models to Facilitate Variable Autonomy for Human-Robot Teaming](https://arxiv.org/abs/2312.07214) | 2023 | Controller |
| [Thinking in 360°: Humanoid Visual Search in the Wild](https://arxiv.org/abs/2511.20351) | 2025 | Controller |
| [Using Vision Language Models as Closed-Loop Symbolic Planners for Robotic Applications: A Control-Theoretic Perspective](https://arxiv.org/abs/2511.07410) | 2025 | Controller |

</details>


---

Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.
