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

---

Selection pipeline, labels and scripts: see [HANDOFF.md](HANDOFF.md) and `data/core/`.
