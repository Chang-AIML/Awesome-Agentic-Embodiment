# 交接文档：Awesome Agentic Embodiment

> 最后更新：2026-10-09（第三次）。本轮在分支 `claude/extended-rejudge` 上：补判了扩展列表和边界论文、加了多智能体专题；随后用户决定**回到精选清单**（决策 24），补判结果暂存一边，并开始写综述方案。
> 旧版交接（第一至三轮，按 Seat × Carrier 定义做的部分）原样保留在 `docs/history/HANDOFF_round3.md`，里面有更早的检索漏斗、各轮判定和踩坑的细节，需要时再查。

---

## 0. 现状

- **项目**：一个 awesome list 和一篇 survey，主题是 *agentic embodiment*，即通用大模型（LLM / VLM）作为 agent 做具身任务。
- **现阶段以 list 为主。** 用户原话：「之前survey的定义方式有问题，我们先把list做好」「给我csv就行」。
- **分类**：两个阶段、五个 Seat（§1.3），外加三个横跨 Seat 的专题：Real2Sim / Sim2Real、VLN、**多智能体**（用户 2026-10-09 要求单独成章，§1.5）。
- **只收 arXiv 论文**（用户 2026-10-09：「你不用管这些期刊，可以主要focus在arxiv」）。不在 arXiv 上的期刊 / 会议论文移到 `data/core/non_arxiv_papers.csv`（528 篇，多按摘要判过，留作参考），`unjudged_no_text.csv` 的 119 篇也不再追。
- **回到精选清单**（用户 2026-10-09：「太多了，不可能有这么多的，我心目中总共最多也就100多篇」「可以回到之前的精选吧，剩余的先不管了」）。
- **当前交付物**：
  - `data/core/paper_list.csv`：精选清单 186 篇（保留 157、资源 20、剔除 9），逐篇读全文判定，带决策模型、理由和原文证据。其中 12 篇是补的 2025 年代表作（决策 25），带原扩展列表的 `id`，其余行 `id` 为空。
  - `data/core/agent_pool.csv`：保留的 157 篇，按阶段 → Seat → 角色 → 年份排好。
  - 保留的按 Seat：Designer 22、Teacher 10、Developer 27、Controller 84、Supervisor 14（先驱 78、2026 年 79）；多智能体 13 篇（保留 12、资源 1）。
  - **综述写作方案**（中文，约 5 页，Claude Doc「Agentic Embodiment 综述写作方案」：https://claude.ai/code/artifact/3814a79d-0de1-4954-9f8f-025f386674c9）：七节，包括定义与主线、收录标准、Seat 框架图、文献概况、12 章结构、7 个待讨论问题、下一步。用户已选写法 A；其余问题等用户讨论。
- **暂存、先不管的**：`data/core/extended_judged.csv`，扩展列表和边界论文按同一标准补判过的 1,351 篇 arXiv 论文（其中判保留 1,040 篇；补进精选的 12 篇 2025 年代表作已移出，现余 1,339 篇）。用户觉得数量远超预期，可能是收录规则偏宽或误判（抽样约一成边缘误判，见 §7 第 5 条），以后要用时先收紧规则再挑。
- **还没做完 / 需要用户看的**：见 §4。

---

## 1. 用户的判定标准（以此为准）

### 1.1 框架图

框架图见 `docs/agent_loop_framework.png`：Agent → Policy / Code / None → Env / Sim。agent 也可以直接作用于 Env / Sim，Env / Sim 的信息再回到 agent。箭头表示信息流动。

### 1.2 六条规则

| # | 规则 | 用户原话 |
|---|---|---|
| 1 | 通用大模型 agent 必须存在，并在回路里起作用 | 「通用大语言模型agent必须存在，在里面扮演角色才行」 |
| 2 | agent 必须是**现成的通用大模型**（GPT、Gemini、Claude、Qwen-VL-72B-Instruct 等，靠 prompt、工具、记忆或 harness 驱动） | 「我说的是通用大模型，而不是被训练过的小模型」 |
| 3 | 箭头不必全有：agent 只要连到 Policy / Code 或 Env / Sim 之一即可，开环也算 | 「只是agent必须要和其中部件有所连接即可，无论是环境还是policy」 |
| 4 | 一眼看上去要是在讲 agent | 「robotwin一眼看上去就不是agent」 |
| 5 | 范围是通用大模型做具身任务，不是具身大模型 | — |
| 6 | 判定要读论文内容，不能只看摘要 | 「我建议你读读内容」 |

各条的细则：
- **规则 2**：
  - 作者训练、微调或蒸馏出的模型都不算 agent，即使底座是通用模型。
  - 训练过的 VLA、技能和感知模型可以作为 agent 调用的工具。
  - 通用模型自己当 agent 行动、再把它的经验蒸馏成小模型的，算 Teacher（如 GUAVA）。
- **规则 4**：主体是数据集、数据生成平台、资产流水线或 benchmark，LLM 只是其中一个模块的，不收。以通用大模型 agent 为对象的 benchmark 归「资源」。
- **规则 5**：VLA、分层 VLA、WAM、机器人基础模型直接出动作的不收，它们只能作为被 agent 调用的工具出现。通用模型直接出动作仍然算（Controller · 直接动作）。
- **Env / Sim 的范围**（用户 2026-10-09 选定）：真机、物理仿真、离散具身仿真（ALFRED、VirtualHome、R2R 离散图）都算；纯文本世界（只有文字的 ALFWorld、TextWorld）和自动驾驶不算。Minecraft、Overcooked 这类有化身的游戏按六条规则正常判（这一点是我定的，用户没表态）。

### 1.3 分类：两个阶段，五个 Seat

阶段由 agent 的产出什么时候产生、什么时候被用决定。每篇只归一个 Seat；`role` 列写 agent 在 Seat 里具体做什么。

| 阶段 | Seat | 含义 | role |
|---|---|---|---|
| 执行前（pre-execution） | Designer | 设计学习问题 | 环境/重建 · 奖励/任务 |
| | Teacher | 自己先执行，经验蒸馏成策略或小模型 | 示范/蒸馏 |
| | Developer | 修改系统本身，按试验保留或回滚 | 系统/代码 · 本体/工具 |
| 运行时（runtime） | Controller | 每一步决定机器人做什么 | 编排 · 写策略 · 直接动作 |
| | Supervisor | 只在异常时介入 | 监控/恢复 |

- **从三层到 Seat 的映射**：全文判定时用的是三层子类，回到 Seat 时按子类映射：
  - 环境/重建、奖励/任务 → Designer；
  - 系统/代码、本体/工具 → Developer；
  - 经验迁移 → Teacher；
  - 策略生产者、编排者、直接动作 → Controller；
  - 运行时监控 → Supervisor。
- **12 篇与旧 Seat 不一致的，逐条决定**：看 agent 的产出主要在哪个阶段被用；拿不准的沿用旧 Seat，理由写在 CSV 的 note 里。
  - 归 Developer：Agentic RSR、Real2Gym（在重建的仿真里练习、写程序再带回真机）；AGRO-SUVIDE、RHD、Zetta（执行前改技能库或 harness）；PDDLLM。
  - 归 Controller：Language to Rewards（奖励当场交给 MPC）、LRLL、KnowNo。
  - 归 Supervisor：Beyond Human Demos（护栏代码在运行时过滤指令）。
  - 沿用旧分类归 Teacher：Manipulate-Anything、Frontier Demo Generation。
- **两个专题**横跨 Seat：Real2Sim / Sim2Real（只收代表作）、VLN 与具身导航。

### 1.4 已经定下来的案例

这些案例可以当判例用：

| 论文 | 结论 | 依据 |
|---|---|---|
| RoboTwin 2.0、HumanoidGen | 剔除 | 数据生成器或 benchmark，MLLM 只是一个模块（用户直接否决了 RoboTwin） |
| RoboFAC、AgentVLN、Ludi | 剔除 | 决策者是作者微调的 Qwen 小模型（用户直接否决了 RoboFAC） |
| RoboTracer（不在表内） | 不算 | 专门训练的 3D 空间轨迹 VLM，没有 agent 角色 |
| RoboFind | 剔除 | 决策回路是 Uni-NaVid、DINO 验证和确定性恢复，通用模型只在示教阶段用到 |
| Code as Policies、ReKep、VoxPoser、SayCan 等开环先驱 | 保留，Controller | 用户说过 CaP 是策略的生产者、「rekep这一类的都算agent」，并确认箭头不必全有 |
| EmbodiedSmith | 保留，Designer（环境/重建） | 用户追问过。它**不是 Real2Sim**（没有从真实数据重建），是生成式仿真，主体是 agent 循环 |
| agentic Real2Sim（RPG、SimEX、Real2Gym 等） | 保留 | 用户：「agentic real2sim … 都算」，但「只是一个子方向」 |

**用户点名必须收录的论文**：
- GUAVA、Harness VLA、Show-Harness、ENPIRE、Code-as-Monitor、ReKep、RPG、SimEX、EmbodiedSmith 都已保留。
- Video2World 是 benchmark，归资源。
- GPT-6 Astra on RoboDojo（2609.24170）是用户举的「LLM 直接出动作」的例子；全文判为评测研究，现在放在资源（被评测的 Seat 为 Controller）。这一条要跟用户确认。

### 1.5 多智能体专题（用户 2026-10-09：「你可以再单独造一个multi-agent的章节」）

- 和 Real2Sim、VLN 一样横跨 Seat，每篇仍有自己的 Seat；CSV 的 `topic` 列写「多智能体」。
- 定义（我拟的，用户还没确认）：多智能体是主系统的核心，满足其一：
  - 通用大模型 agent 分配、规划或协调两个及以上机器人（含异构团队）；
  - 论文把系统呈现为两个及以上分工不同、互相对话或交接工作的通用大模型 agent。
  - 单个机器人上的几次 prompt 调用流水线、只有人机对话、单 agent 调 subagent 工具，都不算。
- 结果：精选清单里 11 篇（RoCo、SMART-LLM、AutoRT、ABot-Claw、Air-Ground VLN、AdaHVLA、ENPIRE、LACE-CRAFT、ROOT、Skill2Real、PARTNR）；补判的扩展论文里有 210 篇，第二条标准偏宽，按「多个角色 agent」收进来的论文不少，用户可能想收紧。

---

## 2. 文件

| 文件 | 状态 | 说明 |
|---|---|---|
| `data/core/agent_pool.csv` | **当前** | 保留的 157 篇，由 `build_paper_list.py` 生成，不要手改 |
| `data/core/extended_judged.csv` | 暂存 | 补判过、未进清单的 1,351 篇 arXiv 论文（列同 `paper_list.csv`，`id` 列为扩展列表的原始 id）。用户决定先不管（决策 24） |
| `data/core/non_arxiv_papers.csv` | 参考 | 不在 arXiv 上的 528 篇（用户决定不收），保留原判定 |
| `data/core/paper_list.csv` | **当前主文件** | list 本身，精选的 186 篇。UTF-8 带 BOM，Excel 可直接打开。列见 §3。注意 `content_rejudge.py apply` 默认写进这个文件，补判的新结果要先写到别处 |
| `data/core/unjudged_no_text.csv` | 参考 | 119 篇没判的（无全文、无摘要），带 DOI，以后可以手动找全文 |
| `docs/paper_list.md` | 当前 | 可读版，由 `scripts/build_paper_list.py` 从 CSV 生成，不要手改 |
| `docs/definition.md` | 当前 | 定义：收录标准六条 + 两个阶段、五个 Seat。旧版在 `docs/history/definition_round3.md` |
| `docs/agent_loop_framework.png` | 当前 | 用户画的回路图（收录标准） |
| `docs/list_summary.pdf` | 当前 | 5 页图文总结：五个 Seat、收录标准、每个 Seat 的代表作、清单里的趋势、判例与下一步。由 `scripts/build_list_summary.py` 从 CSV 生成；改了 CSV 后重跑（代表作名单在脚本的 REPS 里，改了 Seat 或删了论文要同步，否则会报错） |
| `screening/prompts/content_rejudge.txt` | 当前 | 读全文判定的提示词（六条规则 + Env/Sim 范围 + Seat 易错点 + multi_agent 字段），初判用 |
| `screening/prompts/content_verify.txt` | 当前 | 复核提示词：拿初判结果对照全文改错，复核用 |
| `scripts/judging/fetch_fulltext.sh`、`content_rejudge.py`、`resolve_fulltext.py` | 当前 | 下载全文；切分片、复核分片、合并、写回 CSV；找不在 arXiv 上的论文的全文。用法见 §5 |
| `data/judging_runs/content_rejudge/` | 当前 | 核心表 174 篇全文判定的原始输出 |
| `data/judging_runs/extended_2026/`、`extended_2022_2025/`、`boundary/` | 暂存 | 本轮补判：`shards`（分片）、`out_haiku`（初判）、`vshards` + `out_verify`（复核）、`out_final`（合并后，写回 CSV 的就是它） |
| `data/judging_runs/abstract_only/`、`boundary_driving_by_title/`、`redo/` | 当前 | 按摘要判的 538 篇；按标题排除的 36 篇驾驶论文；5 篇无全文重判 |
| `data/core/core_selection.csv` → `core_table.csv` | 与 CSV 同步 | 核心表 177 行（保留 + 资源），带 phase、role 列。若有被判为剔除的论文混在其中，或 Seat 与 `paper_list.csv` 不一致，`build_core_table.py` 会报错 |
| `README.md` | 当前 | 英文 awesome list：核心表各节 + Real2Sim / VLN / Multi-agent 三章 + 资源；末尾「More papers」两节由 `paper_list.csv` 里不在核心表的保留论文生成，回到精选后为空、不显示 |
| `data/core/extended_2026.csv`、`extended_2022_2025.csv` | 补判的输入 | 按旧定义合格、没进核心表的 830 + 902 篇；新结论在 `extended_judged.csv`，这两个文件只作来源 |
| `data/core/fine_labels.csv` | 旧标准 | 12,230 篇候选按旧 rubric 的逐篇判定，verdict 为 core / precursor / boundary / resource / out |
| `data/candidates/candidates.csv` | 原始候选 | 14 篇种子论文的前向引用，13,579 篇 |
| `data/candidates/s2_sweep_2026.jsonl` | 原始候选 | 2026 年关键词检索，11,778 篇 |
| `screening/criteria_fine.md` | 旧标准 | 旧 rubric（摘要级判定），后面打了补丁；补判请用 `content_rejudge.txt` |
| `docs/progress_report.pdf`、`docs/survey_brief.pdf`、`docs/core_stats.md` | 过时 | 按旧收录标准生成，已被 `list_summary.pdf` 取代。`build_brief.py` 的 LINES 里还有已剔除的论文，重跑会报错 |
| `docs/history/` | 历史 | 旧交接文档与旧定义 |

---

## 3. `paper_list.csv` 的列

| 列 | 含义 |
|---|---|
| verdict | 保留 / 资源 / 剔除 |
| topic | 横跨 Seat 的专题；目前只写「多智能体」（Real2Sim、VLN 仍在 `core_selection.csv` 的 theme 列） |
| id | 补判新加论文的候选 id（`c…` / `s…` / `t…` / `gap:…`）；最初的 174 篇为空，补的 12 篇 2025 年代表作保留原 id |
| phase, seat, role | 阶段（执行前 / 运行时）、Seat、角色（§1.3）。资源：被评测的 Seat，role 为「评测」。剔除：`-` |
| key, year, tier | 短名（补判论文的短名由标题自动生成：冒号前 ≤3 个词，否则取前 6 个词）；arXiv 首版年份；tier 为 `2026` 或 `先驱`（2022–2025） |
| title, arxiv | 标题与 arXiv 编号 |
| decision_model | 读全文得到的决策模型，如 "GPT-4o"、"Qwen2.5-VL-3B fine-tuned on …" |
| model_status | G = 现成通用模型；FT = 作者训练或微调；SPEC = VLA 或专用模型；NONE = 没有 LLM / VLM 决策者 |
| contribution | 论文主体：AGENT / DATA / BENCH / OTHER |
| connection | agent 输出什么、交给谁 |
| arrows | 回路图里的箭头：A→M、A→E、M↔E、E→A。来自之前的一次判定，没有逐篇读全文核对，仅供参考 |
| reason | 中文判定理由；「仅摘要：」开头的是按摘要判的，「复核改：」开头的是 Sonnet 复核时改过的 |
| evidence | 论文原句，带节名 |
| note | 与上一版不同的地方，以及人工改判（含 Seat）的说明 |

---

## 4. 下一步（按优先级）

### 4.1 需要用户看、或等用户决定的

0. **综述写作方案**：用户已定写法 A（每个角色详写 3–5 篇，其余进对照表，正文约 20 页），并补了 2025 年代表作（决策 25）。方案第六节其余几条（主线、边界案例、多智能体定义、游戏环境、发表形式）还等用户定。
1. **多智能体的定义**（§1.5）：精选里 11 篇；在补判的扩展论文里这条标准判出了 210 篇，第二条（多个角色 agent）偏宽，用户可能想收紧成「多机器人」为主。
2. （已按用户决定处理）期刊论文不收；按摘要判的、没判的都移出了主清单。
3. Minecraft / Overcooked 这类游戏环境我按六条规则正常判了，用户没表态。
4. 上一轮留下的边界案例，用户还没表态：

   | 论文 | 现在的结论 | 理由 |
   |---|---|---|
   | Tool-Aligned VLA Agent | 剔除 | 主体是 VLA 后训练（本轮 Sonnet 复核也判剔除） |
   | AutoRT | 保留 | 原文写明 LLM 未微调，是系统核心 |
   | RoboGen、SUDD、RobotGPT | 保留 | 读全文后看主体是 agent 或经验迁移 |
   | GPT-6 Astra on RoboDojo | 资源 | 全文判为评测研究，但用户举它当「LLM 直接出动作」的例子 |
   | VLABench、ASIMOV | 剔除 / 资源 | 本轮校准时 Haiku 和 Sonnet 都给了相反结论（VLABench→资源，ASIMOV→剔除），核心表没改，值得再看一眼 |

5. 12 篇 Seat 逐条决定的（§1.3），用户还没看过；主线措辞（草案见 `docs/definition.md` 末尾）。
6. 之前子 agent 误建了 3 个空会话，是否归档：`session_013djFc2XBveZ6ad9rat1T8j`、`session_01L6M4LteFn1EGYUVGkBicSQ`、`session_01DcP3xf6pjhGHUGTtG2WJVr`。

### 4.2 list 定稿之后

1. （用户要时再做）从暂存的 `extended_judged.csv` 里挑代表作进核心表（`core_selection.csv`，记得 theme 列），先写进 `paper_list.csv` 再重跑 README。
2. 补判论文的短名是从标题自动生成的，进核心表的要手工起短名。
3. 按讨论后的写作方案写综述正文：先讲收录标准，再按两个阶段、五个 Seat 分章，每章先讲先驱再讲 2026。
4. 更新 `docs/list_summary.pdf`（`scripts/build_list_summary.py`；用户现阶段不要 PDF，等用户要了再做）。
5. 补代码和项目链接；可选做一个 GitHub Pages 浏览器。

---

## 5. 怎么跑

**依赖**：
- 生成表格的脚本只用 Python 3 标准库。
- 读全文需要 `curl` 和 `pdftotext`（poppler-utils）。
- 生成 PDF 才需要 Node.js 和 Playwright 的 Chromium，现阶段用不到。

**读全文判定的流程**（本轮做法：Haiku 初判 + Sonnet 复核）：

```bash
# 1. 切分片（每片 10 篇），同时生成 ids.txt；没有 arXiv 号、也没有 text 列的论文会列出并跳过
python3 scripts/judging/content_rejudge.py shards data/core/extended_2026.csv work/text work/e26/shards
# 2. 下载全文（后台跑，日志每篇一行 ok / FAIL，最后一行 DONE）
scripts/judging/fetch_fulltext.sh work/e26/shards/ids.txt work/text > work/fetch.log 2>&1 &
# 3. 初判：每个分片一个 Haiku 子 agent，提示词：
#    Follow the instructions in <repo>/screening/prompts/content_rejudge.txt exactly (read that file first).
#    INPUT = <repo>/work/e26/shards/kNN.tsv   OUTPUT = <repo>/work/e26/out_haiku/kNN.txt
#    Use only Read, Grep and Bash (...). Do not use any session, agent, task, web, artifact, scheduling or messaging
#    tool, and do not create any session. Do not edit any file other than OUTPUT.
#    Each line has 12 fields ending with multi_agent (Y or N). ... Final reply only: "done <number of lines>".
# 4. 复核分片：每个初判完成的分片生成一个（明确的 FT/SPEC/NONE 剔除只抽 1/10）
python3 scripts/judging/content_rejudge.py verify work/e26/out_haiku work/e26/shards work/e26/vshards
# 5. 复核：每个复核分片一个 Sonnet 子 agent，提示词同上，换成 content_verify.txt，并给 INPUT / PRIOR / OUTPUT
#    （INPUT = vshards/kNN.tsv，PRIOR = vshards/kNN.prior.txt，OUTPUT = out_verify/kNN.txt）
# 6. 合并（有复核用复核，没有用初判），看改动，写回 CSV
python3 scripts/judging/content_rejudge.py merge work/e26/out_haiku work/e26/out_verify work/e26/out_final
python3 scripts/judging/content_rejudge.py review work/e26/out_final verdict
python3 scripts/judging/content_rejudge.py apply work/e26/out_final work/e26/shards
python3 scripts/build_paper_list.py && python3 scripts/build_core_table.py && python3 scripts/build_readme.py
```

- 校准（`data/judging_runs/calibration/`，20 篇已知结论的核心表论文）：Haiku 结论一致 17/20，常把「为当前任务写的规约 / 约束」误归 Designer；Sonnet 复核纠正了关键错误。正式补判里复核了 1,165 篇，改结论 32 篇（2.7%）、改 Seat 或 role 84 篇（7.2%）、改多智能体标记 10 篇。
- 成本：Haiku 每片（10 篇）约 20 万 token，Sonnet 复核每片约 12 万 token。按摘要判的直接用 Sonnet，每片 20 篇约 8 万 token。
- **不在 arXiv 上的论文**：`scripts/judging/resolve_fulltext.py` 先按标题查 arXiv API，再查 Semantic Scholar 拿开放获取 PDF。但本机没有 OpenAlex / Semantic Scholar 的 key，两者都很快限流（429），arXiv API 在大量下载 PDF 之后也会限流。本轮最后放弃查找，直接按摘要判（`resolve_fulltext.py` 的 `csv` 格式：key, arxiv, title, year, text；`shards` 会用 text 列的路径和 year）。以后有 key 或订阅时再补全文。
- 无全文的行（reason 以「无全文」开头）`apply` 会跳过；补好文本后重判，把结果放进复核目录并命名为 `zz_redo.txt`，`merge` 会让它覆盖前面的行。
- 不要用 `--update` 重新应用 `data/judging_runs/content_rejudge/`（那一轮写回时有人工改判）。
- 判完一批，把分片和输出复制到 `data/judging_runs/<轮次名>/` 存档。全文文本不要提交，太大。

**改了 CSV 之后，同步核心表和 README**：
- 先改 `core_selection.csv`：去掉判为剔除的行；判为资源的，tier 改成 resource。
- 然后依次运行：

```bash
python3 scripts/build_paper_list.py && python3 scripts/build_core_table.py && python3 scripts/build_readme.py
```

（`build_extended.py` 生成的旧扩展列表已经不用了，README 的「More papers」直接读 `paper_list.csv`。）

**子 agent 和下载的坑**：
- 最多同时跑 20 个子 agent，超出会直接报错。
- 提示词里要明确禁止会话工具（Haiku 误建过空会话）；本轮加了禁令后没再出现。
- role 必须是 §1.3 里对应 Seat 的那些，否则 apply 会报错；`content_rejudge.py` 已对 Seat 大小写做归一化。
- **两个下载流不能共用临时文件**：早期两个下载流在同一目录写 `tmp.pdf`，导致一篇论文的文本被换成另一篇（c00628 拿到了 HumanoidGen 的内容，已修正）。`fetch_fulltext.sh` 现在用 `tmp.<pid>.pdf`。下载后可以用标题词核对文本开头。
- **后台等待别用 `pgrep -f`**：它会匹配到等待命令自己，导致永远等下去。改用检查日志里的 DONE。
- arXiv 下载要保持每篇间隔 3 秒以上；两路并发时 arXiv API 会开始返回 429。
- Semantic Scholar、OpenAlex 不带 key 都会限流。

---

## 6. 和用户合作

- 用户用中文交流，做 survey 的经验不多。先给明确建议，再请他们决定；不要一次抛出很多选项。
- 用户看到「一眼就不是 agent」的论文会直接指出来。判定宁可先读全文、给出原文证据，也不要凭摘要或标题猜。
- 用户现阶段只要 CSV，不要主动生成报告或 PDF。
- 用户说过的话就是规则（§1）。有冲突时，先指出冲突，再按新说法执行，并在 note 和本文件里记下来。

---

## 7. 历史（一段话）

1. **第一、二轮**：收集 14 篇种子论文的前向引用，加上 2026 年关键词检索和三轮联网补漏，逐篇判定了 12,230 篇候选（`fine_labels.csv`）。
2. **第三轮**：按 Seat × Carrier 定义挑出核心表，并出了报告和 5 页简报。
3. **2026-10-09**：用户提出 agent 回路图（和一度的三层框架），收录规则依次改为：
   - 开环也算；
   - 数据平台不算；
   - 必须是现成通用大模型；
   - 读全文判定。

   174 篇读全文重判后，用户又把分类改回两个阶段、五个 Seat（决策 20），收录标准保持最后一轮的。各条决策的完整记录见 `docs/history/definition_round3.md` 开头（决策 1–19）和 `docs/history/HANDOFF_round3.md` §5。
4. **2026-10-09（第二次）**：用户决定离散具身仿真算、纯文本世界和自动驾驶不算（决策 21），并要求单独建多智能体章节（决策 22）。补判了两份扩展列表和边界论文共 1,890 篇（有 arXiv 的读全文，Haiku 初判 + Sonnet 复核；其余按摘要），清单扩到 2,053 篇（含去重）。随后用户决定只收 arXiv 论文（决策 23），主清单变为 1,525 篇，agent 池子 1,185 篇。
5. **2026-10-09（第三次）**：用户看了 agent 池子后认为数量远超预期（「心目中总共最多也就100多篇」），决定回到精选清单 174 篇（决策 24）。补判的 1,351 篇移到 `data/core/extended_judged.csv` 暂存。那次补判的经验：六条规则本身偏宽，几乎所有「LLM 调技能」的论文都能进；Sonnet 复核抽 40 篇约一成边缘误判；只看摘要的判定不可靠（同一论文的重复记录有 3 对结论相反）。之后开始写综述方案。
6. **2026-10-09（第四次）**：用户看了综述写作方案，选写法 A（每个角色详写 3–5 篇代表作，其余进对照表），并要求「2025年补一下」（决策 25）。从暂存的 291 篇 2025 年保留论文里，按引用数和对主线的作用每个角色挑一两篇，复查判定后补了 12 篇进精选（`core_selection.csv` 的 added 为 `r4-2025`）：
   - Designer：LAMARL、GROVE；
   - Teacher：BLAZER；
   - Developer：NeSyC、SkillWrapper、RoboMoRe；
   - Controller：Manual2Skill、Chain-of-Modality、GenSwarm、SPF（VLN）；
   - Supervisor：FORTRESS、RoboSafe。

   另有三篇看过后没收：GenDexHand（复核从剔除改判保留，主体接近数据生成平台）、UAV-VLA（只离线生成飞行计划）、Agentic Robot（运行时的进度判断和恢复由微调的 Qwen 验证器做）。
