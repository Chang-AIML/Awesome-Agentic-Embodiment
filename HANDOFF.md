# 交接文档：Awesome Agentic Embodiment

> 最后更新：2026-10-09。全部工作已合并到 **main**（之前在分支 `claude/jolly-thompson-g43dno` 上做）。接手后从 main 拉新分支继续。
> 旧版交接（第一至三轮，按 Seat × Carrier 定义做的部分）原样保留在 `docs/history/HANDOFF_round3.md`，里面有更早的检索漏斗、各轮判定和踩坑的细节，需要时再查。

---

## 0. 现状

- **项目**：一个 awesome list 和一篇 survey，主题是 *agentic embodiment*，即通用大模型（LLM / VLM）作为 agent 做具身任务。
- **现阶段只做 list。** 用户原话：「之前survey的定义方式有问题，我们先把list做好」「给我csv就行」。旧的 survey 定义（Seat × Carrier、闭环判定）已经弃用，报告和简报暂时不要更新。
- **当前交付物**：`data/core/layer_classification.csv`，共 174 篇。
  - 保留 145 篇，其中 L1 43、L2 88、L3 14；
  - 资源 20 篇（benchmark 与评测研究）；
  - 剔除 9 篇。
  - 每篇都读了全文判定，附有决策模型和原文证据。可读版是 `docs/layer_classification.md`。
- **还没做完**：这 174 篇只是旧定义下挑出来的核心表。下面两批论文还没有按新标准判过（见 §4）：
  - 按旧定义判为合格、但没进核心表的约 1,732 篇；
  - 旧定义的边界论文 313 篇。

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
  - 通用模型自己当 agent 行动、再把它的经验蒸馏成小模型的，算 L2 经验迁移（如 GUAVA）。
- **规则 4**：主体是数据集、数据生成平台、资产流水线或 benchmark，LLM 只是其中一个模块的，不收。以通用大模型 agent 为对象的 benchmark 归「资源」。
- **规则 5**：VLA、分层 VLA、WAM、机器人基础模型直接出动作的不收，它们只能作为被 agent 调用的工具出现。通用模型直接出动作仍然算（L3）。

### 1.3 三层分类

三层是用户自己的划分。用户原话：
- L1：「给机器人创造环境，重建，设计reward（developer和designer），pre-exuction（preparation）」
- L2：「可以是policy的生产者（CAP），蒸馏 （experience transfer）LLM不直接控制robot，隔了一层（harness），runtime monitor（harness）（介于中间 exception）」
- L3：「General LLM as policy （during excution）」

各层子类：

| 层 | 子类 |
|---|---|
| L1 准备层 | 环境/重建 · 奖励/任务 · 本体/工具 · 系统/代码 |
| L2 中间层 | 策略生产者 · 编排者 · 经验迁移 · 运行时监控 |
| L3 执行层 | 直接动作 |

### 1.4 已经定下来的案例

这些案例可以当判例用：

| 论文 | 结论 | 依据 |
|---|---|---|
| RoboTwin 2.0、HumanoidGen | 剔除 | 数据生成器或 benchmark，MLLM 只是一个模块（用户直接否决了 RoboTwin） |
| RoboFAC、AgentVLN、Ludi | 剔除 | 决策者是作者微调的 Qwen 小模型（用户直接否决了 RoboFAC） |
| RoboTracer（不在表内） | 不算 | 专门训练的 3D 空间轨迹 VLM，没有 agent 角色 |
| RoboFind | 剔除 | 决策回路是 Uni-NaVid、DINO 验证和确定性恢复，通用模型只在示教阶段用到 |
| Code as Policies、ReKep、VoxPoser、SayCan 等开环先驱 | 保留 | 用户说过 CaP 是 L2 策略生产者、「rekep这一类的都算agent」，并确认箭头不必全有 |
| EmbodiedSmith | 保留，L1 环境/重建 | 用户追问过。它**不是 Real2Sim**（没有从真实数据重建），是生成式仿真，主体是 agent 循环 |
| agentic Real2Sim（RPG、SimEX、Real2Gym 等） | 保留 | 用户：「agentic real2sim … 都算」，但「只是一个子方向」 |

**用户点名必须收录的论文**：
- GUAVA、Harness VLA、Show-Harness、ENPIRE、Code-as-Monitor、ReKep、RPG、SimEX、EmbodiedSmith 都已保留。
- Video2World 是 benchmark，归资源。
- GPT-6 Astra on RoboDojo（2609.24170）是用户举的「LLM 直接出动作」的例子；全文判为评测研究，现在放在资源（评测 L3）。这一条要跟用户确认。

---

## 2. 文件

| 文件 | 状态 | 说明 |
|---|---|---|
| `data/core/layer_classification.csv` | **当前主文件** | list 本身。UTF-8 带 BOM，Excel 可直接打开。列见 §3 |
| `docs/layer_classification.md` | 当前 | 可读版，由 `scripts/build_layer_table.py` 从 CSV 生成，不要手改 |
| `docs/agent_loop_framework.png` | 当前 | 用户画的框架图 |
| `docs/list_summary.pdf` | 当前 | 5 页图文总结：框架、六条标准、三层九类的代表作、清单里的趋势、判例与下一步。由 `scripts/build_list_summary.py` 从 CSV 生成；改了 CSV 后重跑（代表作名单在脚本的 REPS 里，删掉的论文要同步去掉，否则会报错） |
| `screening/prompts/content_rejudge.txt` | 当前 | 读全文判定的提示词，即上面六条规则的执行版 |
| `scripts/judging/fetch_fulltext.sh`、`scripts/judging/content_rejudge.py` | 当前 | 下载全文、切分片、汇总、写回 CSV 的工具，用法见 §5 |
| `data/judging_runs/content_rejudge/` | 当前 | 这 174 篇全文判定的原始输出 |
| `data/core/core_selection.csv` → `core_table.csv` | 与 CSV 同步 | 核心表 165 行（保留 + 资源），带 layer、layer_sub、arrows 列。若有被判为剔除的论文混在其中，`build_core_table.py` 会报错 |
| `README.md` | 部分过时 | 英文 awesome list。核心部分的论文与 CSV 一致，但分节仍按旧的 Seat；末尾两份扩展列表是旧定义下的结果 |
| `data/core/extended_2026.csv`、`extended_2022_2025.csv` | **待补判** | 按旧定义合格、没进核心表的 830 + 902 篇，没有按新标准判过 |
| `data/core/fine_labels.csv` | 旧标准 | 12,230 篇候选按旧 rubric 的逐篇判定，verdict 为 core / precursor / boundary / resource / out |
| `data/candidates/candidates.csv` | 原始候选 | 14 篇种子论文的前向引用，13,579 篇 |
| `data/candidates/s2_sweep_2026.jsonl` | 原始候选 | 2026 年关键词检索，11,778 篇 |
| `docs/definition.md`、`screening/criteria_fine.md` | 过时，但记录了决策 | 旧定义，后面打了补丁（决策 16–19）。list 做完后要按 §1 重写 |
| `docs/progress_report.pdf`、`docs/survey_brief.pdf`、`docs/core_stats.md` | 过时 | 按旧 Seat 定义生成。`build_brief.py` 的 LINES 里还有已剔除的论文，重跑会报错 |
| `docs/history/` | 历史 | 旧交接文档 |

---

## 3. `layer_classification.csv` 的列

| 列 | 含义 |
|---|---|
| verdict | 保留 / 资源 / 剔除 |
| layer, subtype | 保留的论文：L1 / L2 / L3 及子类。资源：被评测的层和「评测Lx」。剔除：`-` |
| key, year, tier | 短名；arXiv 首版年份；tier 为 `2026` 或 `先驱`（2022–2025） |
| title, arxiv | 标题与 arXiv 编号 |
| decision_model | 读全文得到的决策模型，如 "GPT-4o"、"Qwen2.5-VL-3B fine-tuned on …" |
| model_status | G = 现成通用模型；FT = 作者训练或微调；SPEC = VLA 或专用模型；NONE = 没有 LLM / VLM 决策者 |
| contribution | 论文主体：AGENT / DATA / BENCH / OTHER |
| connection | agent 输出什么、交给谁 |
| arrows | 框架图里的箭头：A→M、A→E、M↔E、E→A。这一列来自之前的一次判定，没有逐篇读全文核对，仅供参考 |
| reason | 中文判定理由 |
| evidence | 论文原句，带节名 |
| note | 与上一版不同的地方，以及人工改判的说明 |
| old_seat | 旧定义下的 Seat，仅供参考 |

---

## 4. 下一步（按优先级）

### 4.1 把 list 补全

把 §0 提到的两批论文按同样的方法读全文判定：

| 来源 | 篇数 | 有 arXiv 号 | 没有 arXiv 号 |
|---|---|---|---|
| `extended_2026.csv` | 830 | 495 | 335 |
| `extended_2022_2025.csv` | 902 | 643 | 259 |
| `fine_labels.csv` 中强模型轮次判为 boundary 的 | 313 | 211 | 102 |

- **有 arXiv 号的约 1,350 篇**可以直接用 §5 的流程。
  - 下载约需 2.5 小时（每篇约 6 秒）。
  - 判定分成约 135 个 10 篇的分片。本轮用的是 Sonnet，每个分片约 2–3 分钟、15 万 token。
  - 想省钱，可以先让 Haiku 初判，再由 Sonnet 复核保留和边界的部分。用户一向的偏好是批量工作用最便宜的模型。
- **没有 arXiv 号的约 700 篇**多数有 DOI：`c` 开头的 id 查 `candidates.csv` 的 doi 列，`s` 开头的查 `s2_sweep_2026.jsonl`。
  - 需要另写下载：用 OpenAlex 的 open access 链接（本环境的代理已注入 OpenAlex 凭证）或 Unpaywall 拿 PDF。
  - 拿不到全文的，只能按摘要判，并在 note 里注明。
- **边界的 313 篇**在旧定义下被排除，原因是只在离散仿真（ALFRED、VirtualHome、R2R 离散图）里做实验，或者属于自动驾驶。新框架里 Env / Sim 是否包括这些，**要先问用户**。
- **补判出来的新论文没有短名**：`content_rejudge.py apply` 会用候选 id（如 `c01234`、`s05277`）当 key，之后可以再补短名。

### 4.2 等用户决定的事

1. 上面边界 313 篇的范围问题：离散仿真和自动驾驶算不算。
2. 几篇边界案例，用户还没表态：

   | 论文 | 现在的结论 | 理由 |
   |---|---|---|
   | Tool-Aligned VLA Agent | 剔除 | 主体是 VLA 后训练 |
   | AutoRT | 保留 | 原文写明 LLM 未微调，是系统核心 |
   | RoboGen、SUDD、RobotGPT | 保留 | 读全文后看主体是 agent 或经验迁移 |
   | GPT-6 Astra on RoboDojo | 资源 | 全文判为评测研究，但用户举它当 L3 的例子 |

3. list 做完后：README 是否改成按 L1 / L2 / L3 分节；survey 的定义和主线怎么重写。
4. 之前子 agent 误建了 3 个空会话，是否归档：
   - `session_013djFc2XBveZ6ad9rat1T8j`
   - `session_01L6M4LteFn1EGYUVGkBicSQ`
   - `session_01DcP3xf6pjhGHUGTtG2WJVr`

### 4.3 list 定稿之后

1. 按三层重排 README：改 `scripts/build_readme.py`，数据源用 `layer_classification.csv`。
2. 按 §1 重写 `docs/definition.md`。
3. 重做报告和简报：先改 `scripts/build_brief.py` 的 LINES。
4. 补代码和项目链接；可选做一个 GitHub Pages 浏览器。

---

## 5. 怎么跑

**依赖**：
- 生成表格的脚本只用 Python 3 标准库。
- 读全文需要 `curl` 和 `pdftotext`（poppler-utils）。
- 生成 PDF 才需要 Node.js 和 Playwright 的 Chromium，现阶段用不到。

**读全文判定的流程**（以补判 2026 扩展列表为例）：

```bash
# 1. 切分片（每片 10 篇），同时生成 ids.txt；没有 arXiv 号的论文会列出并跳过
python3 scripts/judging/content_rejudge.py shards data/core/extended_2026.csv work/text work/shards
# 2. 下载全文（后台跑，日志里每篇一行 ok / FAIL，最后一行 DONE）
scripts/judging/fetch_fulltext.sh work/shards/ids.txt work/text > work/fetch.log 2>&1 &
# 3. 每个分片交给一个子 agent，提示词如下：
#    Follow the instructions in screening/prompts/content_rejudge.txt exactly (read that file first).
#    INPUT = work/shards/kNN.tsv   OUTPUT = work/out/kNN.txt
#    Use only Read, Grep and Bash (Bash only to append output lines). Do not use any session, agent, web or
#    messaging tool. Final reply only: "done <number of lines>".
# 4. 检查完整性并逐条看改动（全部、只看结论变化、或只看与 CSV 不同的）
python3 scripts/judging/content_rejudge.py review work/out verdict
# 5. 人工复核后写回 CSV：新论文追加；已有的只有加 --update 才会覆盖
python3 scripts/judging/content_rejudge.py apply work/out work/shards
python3 scripts/build_layer_table.py
```

- **不要用 `--update` 重新应用 `data/judging_runs/content_rejudge/`**。那一轮写回时有人工改判（如 EmbodiedSmith 后来恢复了），原始输出里还是旧结论。
- 判完一批，把 `work/out/` 和分片复制到 `data/judging_runs/<轮次名>/` 存档。全文文本不要提交，太大。

**改了 CSV 之后，同步核心表和 README**：
- 先改 `core_selection.csv`：
  - 去掉判为剔除的行；
  - 判为资源的，tier 改成 resource。
- 然后依次运行：

```bash
python3 scripts/build_core_table.py && python3 scripts/build_extended.py && python3 scripts/build_readme.py
```

**子 agent 的坑**：
- 最多同时跑 20 个子 agent，超出会直接报错。
- 子 agent 偶尔会违反「只用 Read、Grep、Bash」：
  - 用 Write 写输出，无害；
  - Haiku 调用过会话工具，误建过空会话。
  - 提示词里要明确禁止。
- 有的子 agent 会把层写成「L1 准备层」之类。`content_rejudge.py` 已经做了归一化，但子类名必须是 §1.3 里的那些，否则 apply 会报错。
- Sonnet 子 agent 偶尔会卡住：转录文件十几分钟不更新，也不写输出。遇到时停掉，重启同一个分片，并在提示里说明「OUTPUT 已存在时只补缺的」。
- 分片输出只在本地。长任务要分批提交、推送：云端会话的容器会被回收，之前就因此丢过一次中间结果。
- arXiv 下载要保持每篇间隔 3 秒以上。
- Semantic Scholar 不带 key，常返回 429。OpenAlex 对 arXiv 预印本的引用覆盖很差，只适合补元数据。

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
3. **2026-10-09**：用户提出三层框架和 agent 回路图，规则依次改为：
   - 开环也算；
   - 数据平台不算；
   - 必须是现成通用大模型；
   - 读全文判定。

   旧定义因此弃用，工作重心转到 list。各条决策的完整记录见 `docs/definition.md` 开头（决策 1–19）和 `docs/history/HANDOFF_round3.md` §5。
