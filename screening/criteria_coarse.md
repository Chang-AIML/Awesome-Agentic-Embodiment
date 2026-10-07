# Coarse relevance screening (stage 1)

Goal: high-recall triage of citation-harvested candidates by title + abstract.
Fine-grained inclusion against the survey definition happens in stage 2.

## Labels

**relevant** — the paper proposes, studies, benchmarks, or surveys a system in which a
foundation-model-driven *agentic process* is coupled to a *physical or physically simulated
embodiment*.

- Agentic process (any of): task planning / decomposition, explicit reasoning (incl. chain-of-thought
  inside a VLA), tool / skill / API / VLA calling, code generation for control, memory, reflection,
  failure detection / monitoring / recovery, clarification or dialogue with humans, multi-agent
  communication, or autonomous improvement of a robot system (generating data, rewards, tasks,
  environments, or policy code; distilling an agent into a smaller model).
- Embodiment: robot arm, mobile robot, humanoid, quadruped, drone, dexterous hand, or an agent acting
  in a 3D physical simulator (household, navigation, manipulation benchmarks).

**maybe** — embodied foundation models with no explicit agentic process (pure VLA / visuomotor policy,
world model, embodied perception or grounding model); agentic systems with weak or unclear physical
embodiment (Minecraft / games, autonomous driving, 2D gridworlds, AR/VR); embodied-AI surveys,
position papers, datasets, or safety studies; anything ambiguous from the title alone.

**irrelevant** — no embodiment at all (web / GUI / OS / code / QA / chat / math agents, generic LLM
reasoning or alignment, pure NLP or vision), or an unrelated application domain.

When torn between two labels, pick the more inclusive one (recall first).

## Extra fields

- **type**: method | benchmark | dataset | survey | position | other
- **role** (coarse, for relevant/maybe): controller (LLM/VLM plans or calls skills/code/tools at run time),
  hierarchical (high-level VLM + low-level policy), reasoning-vla (reasoning/memory inside one policy),
  monitor (failure detection, verification, recovery, safety), teacher (data generation, distillation,
  demonstrations), developer (reward / environment / task / policy-code design, autonomous research),
  multi-agent (multi-robot or human-robot collaboration, dialogue), self-evolving (memory, skill
  libraries, lifelong learning), navigation (VLN / object navigation agents), other
- **reason**: at most 12 words
