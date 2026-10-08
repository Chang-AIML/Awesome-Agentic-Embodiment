# Fine screening (stage 2): placement against the survey definition

Main-text definition: `docs/definition.md`. This file is the compact rubric used to judge one paper
from its title + abstract (+ your own knowledge of well-known papers). Judge what the abstract
supports; when a detail is unclear, pick the most likely reading and lower `conf`.

Revision 2026-10-08 (user decision): step A.3 accepts an **authored closed loop** as well as
re-decision by the model. Papers first judged with the strict A.3 were re-judged with this version.

## Step A — is there an agent? (all three must hold)

1. **Explicit decision**: the foundation model (LLM / VLM / VLA or a model trained from one) emits
   inspectable discrete decisions — plans, subtasks, skill/tool/VLA calls with arguments, code,
   constraints, verdicts (continue/stop/retry/ask/keep/revert), edits to a system.
   Scalars, scores, embeddings, latents, action chunks do NOT count (that model is an *organ*:
   reward model, value model, success scorer, progress estimator).
2. **Authority**: the model writes its own options (plans, code, call arguments), OR picks among
   options where at least one is a control action (stop / retry / replan / ask / keep-revert /
   switch between heterogeneous skills). Scoring code-enumerated candidates of one kind
   (frontiers, sampled points) while code owns the control flow does NOT count.
3. **Closed loop** — either form counts:
   - **re-decide**: within one run the model is called again with (i) its own earlier decisions and
     (ii) evidence of their consequences from execution, tools, verifiers, training/eval stats, or a
     human; and it can revise.
   - **authored**: the model writes an executable artifact (constraints, program, cost/objective for an
     online optimizer, monitor conditions, success checks) that, while the body acts, reads live
     perception and changes the behaviour according to the outcome — re-solving on tracked state,
     moving to or backtracking between stages, recovery after a failed assertion, vetoing an unsafe
     action, retrying after a failed success check. The outcome-dependent logic (conditions,
     constraints, checks) must be written by the model; the trigger machinery (solver, backtracking,
     retry loop) may be a fixed scaffold. Examples: ReKep (keypoint constraints re-solved at ~10 Hz,
     backtracks when a path constraint breaks), VoxPoser (value maps drive closed-loop MPC robust to
     perturbations), Code as Policies programs with perception feedback loops, ProgPrompt programs with
     assertions and recovery actions, Language to Rewards (reward code optimised online by MPC),
     OmniManip (constraints re-solved under 6D pose tracking), SUDD (LLM-written success checks trigger
     retries while collecting data), RoboGuard-style LLM-written safety specs enforced at runtime.
   - **Neither** (step fails): the artifact's content does not depend on the live state during
     execution — a skill or landmark list, a one-shot grasp pose or waypoint sequence, a single plan
     handed to skills that close their own loops (that loop is not authored by the model);
     per-step reasoning that never sees its own earlier decisions (ECoT, pi0.5); consequences that are
     only model-predicted before execution (world-model imagination, Text2Motion feasibility checks).
   - For Designer and Developer the loop must still be closed by re-design / re-edit from training or
     trial outcomes (Eureka iterates; one-shot reward or task code such as Text2Reward, RoboGen,
     GenSim does not).

## Constraint / keypoint programming (user decision 2026-10-08, second batch)

"ReKep-type papers all count as agents." A foundation model that writes spatial constraints, keypoints,
affordance or contact specifications, value maps, or cost / objective functions that a solver, optimizer
or motion planner turns into robot motion (ReKep, VoxPoser, OmniManip, CoPa, MOKA, Language to Rewards,
...) counts as **core** (if step B's body and experiment conditions hold) with seat `Controller`, sub
`direct`, interface `constraint`.
- `loop` = authored when the constraints are re-solved on live tracked state or stage transitions /
  backtracking depend on them; re-decide when the model is re-queried with outcomes; none when the
  constraints are solved once (still core: the loop column keeps the distinction).
- Still `out`: models that output only grasp poses, waypoints or action chunks directly (no constraint or
  objective that a solver consumes), and fixed perception pipelines with no foundation-model decision.

## Agentic Real2Sim (user decision 2026-10-08, second batch)

A foundation-model agent that **reconstructs or builds an interactive simulation of a real robot scene**
(scene / asset / articulation reconstruction from real images, video or scans; layout; physics parameters;
simulation code) and the result is used for robot learning, data generation or evaluation counts as
**core** with seat `Designer` (or `Developer` when it then improves the robot's solution) and the reason
tag `[real2sim]` (or `[real2sim2real]`). The agent's explicit decisions are its construction choices.
- The usual build → render/simulate → compare with the real observation or check executability → revise
  cycle satisfies step A.3 (`loop` = re-decide or authored).
- A one-shot agentic pipeline still counts: verdict core, `loop` = none.
- Reconstruction without a foundation-model decider (Gaussian splatting, NeRF, classical system
  identification, learned asset generators run as fixed pipelines) stays `out`.
- Physical-experiment requirement: the reconstructed scene must be a physics simulation used by a robot
  (sim policy training, data generation or evaluation); real-robot transfer is welcome but not required.

## Step B — verdict (pick one)

- **core**: Step A holds; robot body (arm, mobile base, legged, humanoid, drone, multi-robot,
  social robot); ≥1 headline experiment on a real robot or in physics simulation where outcomes can
  deviate for physical reasons (MuJoCo, Isaac, PyBullet, robosuite, LIBERO, ManiSkill, Habitat
  continuous nav, OmniGibson with motion-planned primitives); the agentic part is the paper's
  headline contribution.
- **precursor**: Step A.1 and A.2 hold but A.3 fails (open-loop plan/program/constraint, per-step
  decisions without own history, prediction-only checks), with a robot body. Typical: ZS-Planners,
  Socratic Models, LM-Nav, TidyBot, CoPa, MOKA, Instruct2Act, SMART-LLM, ECoT, pi0.5, KnowNo, AutoRT,
  Text2Motion, Text2Reward, RoboGen, GenSim.
- **boundary**: an agent holds but the best experiment is only in discrete/scripted simulation
  (ALFRED, AI2-THOR, VirtualHome, TEACh, TDW transport, R2R discrete graph, Habitat magic-grasp
  rearrangement, symbolic primitives), OR the domain is autonomous driving.
- **resource**: benchmark, testbed, dataset, capability study or survey whose subject is embodied
  agents (no own method, or the method is secondary).
- **out**: everything else — reactive VLA / visuomotor policy (incl. RL-finetuned), latent
  dual-system, organ-only (reward / value / score / success models, offline-only judges or
  failure detectors), one-shot annotators/relabelers, world models / video prediction, games
  (Minecraft), text/grid worlds, web/GUI/OS agents, perception or grounding models evaluated offline.

## Step C — fields (fill for core / precursor / boundary / resource; use `-` otherwise)

- **seat** (primary; for resource = the seat it evaluates):
  - `Controller` — called during the evaluated episodes and changes what the robot does even when
    nothing fails (plans, calls skills/tools/VLAs, writes code run now, emits micro-actions,
    always-on constraints/objectives). Self-improvement during evaluation (memory, skill library,
    harness updated across episodes) stays Controller with subclass `lifelong`.
  - `Supervisor` — runtime, acts only on exceptions: gates, vetoes, interrupts, failure detection +
    recovery / replanning trigger, produced by a check process separate from the nominal decider.
  - `Teacher` — before deployment; the agent itself acts, its outcome-checked behaviour (trajectories,
    recovery branches, playbooks) becomes the training target / frozen context of the deployed model.
  - `Designer` — before deployment; designs the *problem* for a learner: reward / success / verifier
    code, tasks, environments, scenes, curricula, sim parameters, eval suites, data selection.
  - `Developer` — before deployment; modifies the *solution*: reused policy code, skill/tool
    libraries, harness, training code, hyper-parameters, hardware/morphology; keeps or reverts based
    on its own experiments.
- **seat2**: secondary seats separated by `+` (or `-`).
- **carrier** of the top-level decider: `G` general model used as-is (GPT, Gemini, Claude, Llama,
  Qwen-VL off the shelf); `C` embodied-trained decider + generic executor (existing skills, planner);
  `H` trained decider + co-designed learned low-level policy trained for its outputs; `I` one trained
  model emits both explicit decisions and actions.
- **sub** (Controller only, else `-`): `orchestrator` (calls skills/tools/VLAs), `direct` (micro-actions,
  native commands, code executed now), `lifelong` (memory/skill/harness improved across episodes),
  `trained` (carrier C/H/I). Pick the dominant one.
- **interface**: one of `skill-call`, `vla-call`, `micro-action`, `code`, `constraint`, `verdict`,
  `trace`, `problem-spec`, `system-edit`, `message`.
- **topo**: `x1` single agent; `xR` several role agents on one task; `xN` one agent per robot;
  `1:N` one decider for many robots; `xO` many agents owning branches of a campaign.
- **closure**: evidence the loop uses: `E` (execution), `H` (human), `E+H`, `M` (prediction only), `none`.
- **loop** (only in re-judging runs): `re-decide`, `authored` or `none` (see step A.3); `-` for out.
- **body**: `manip`, `mobile-manip`, `nav`, `loco`, `humanoid`, `aerial`, `multi-robot`, `driving`,
  `social`, `other`; append `/real`, `/sim` or `/sim+real`.
- **rep** (1–5): how representative / important this paper is for its seat in a ~60-paper survey core
  table. 5 = defining or field-shaping work; 4 = strong, widely cited or clearly novel exemplar;
  3 = solid typical member; 2 = incremental; 1 = marginal. Judge novelty of the agentic idea and
  influence, not only citations.
- **conf**: `high` / `med` / `low` confidence in verdict + seat.
- **reason**: ≤ 25 words; say what the agent outputs, who consumes it, and why the verdict.

## Anchors

| paper | verdict | seat | carrier | sub |
|---|---|---|---|---|
| SayCan | core | Controller | G | orchestrator |
| Inner Monologue | core | Controller | G | orchestrator |
| RoCo (multi-arm dialogue) | core | Controller | G | orchestrator (topo xN) |
| PaLM-E | core | Controller | C | trained |
| Hi Robot | core | Controller | H | trained |
| OneTwoVLA | core | Controller | I | trained |
| Code-as-Monitor | core | Supervisor | G | - |
| REFLECT / DoReMi | core | Supervisor | G | - |
| GUAVA (frontier agent trajectories distilled into 4B agent) | core | Teacher (seat2 Controller) | G | - |
| Eureka / DrEureka | core | Designer | G | - |
| ENPIRE (coding agents edit robot policy code, keep/revert by real trials) | core | Developer | G | - |
| Code as Policies / VoxPoser / ReKep (authored loop) | core | Controller | G | direct |
| CoPa / MOKA (one-shot constraints or keypoints, open loop) | precursor | Controller | G | direct |
| ECoT / pi0.5 | precursor | Controller | I | trained |
| LLM-Planner on ALFRED, CoELA on TDW | boundary | Controller | G | - |
| OpenVLA, pi0, RT-1, GR00T N1 | out | - | - | - |
| RoboMonkey, GVL, VLAC (scorers) | out | - | - | - |
| Voyager (Minecraft) | out | - | - | - |
| EmbodiedBench, Embodied Agent Interface | resource | Controller | - | - |
