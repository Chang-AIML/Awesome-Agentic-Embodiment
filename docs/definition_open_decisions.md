# 定义稿的待决策问题

## 1. 自动驾驶是否纳入？

- 选项：(a) 用同一套规则处理：open-loop 日志评测不满足 C5，判 OUT；闭环评测（CARLA、实车）按 Λ 判定。(b) 直接把驾驶领域整体排除，作为单列例外，并点名 AESOP。(c) 单开一个驾驶附表。
- 推荐：选 (a)。规则保持一致，不需要额外的 fiat。按这套规则，测试集中的 AutoVLA、Alpamayo-R1、AESOP 都落在 B-loop，不会让驾驶论文占满 CORE。前提是正文的 domain 列明确标出 driving。

## 2. agent 判定成立、但实验只到 F1 的工作（AI2-THOR、ALFRED、TDW、R2R 离散图、Habitat magic grasp）放在哪里？

- 选项：(a) 维持 B-world，放进 lineage 表。(b) 并入 CORE，另打 F1 标。(c) 只把 F1 下的 multi-agent 工作放宽进 CORE。
- 推荐：选 (a)。F2 判据本来就是为了让 consequence 真正由物理决定。选 (b) 会把 CoELA、EMOS、NavGPT 这批工作放回 CORE，主线就变得不可证伪。代价是 multi-agent 这一章在 CORE 中偏薄，正文需要明说这一点。

## 3. 是否放宽 Λ1'（authored loop），让 Code as Policies、VoxPoser、ReKep 进入 CORE？

- 选项：(a) 维持严格规则，把它们归入 B-loop 的 lineage 表。(b) 放宽规则，把它们并入 CORE。(c) 采用严格规则，但同时报告一份宽松口径下的敏感性计数。
- 推荐：选 (c)。CORE 按严格规则判；另附一张敏感性表，列出放宽 Λ1' 后各年份 seat 分布的变化。正文中要明说 boundary 指的是前驱或近邻，并不意味着这些工作不重要。

## 4. 人类参与形成的 closure（H）怎样计数？

- 选项：(a) 模型整合进来的人类输入（执行报告、澄清、纠正）都算 E/H 证据，人直接替代模型决策的不算。(b) 只有执行报告算。(c) 人类输入一律不算。
- 推荐：选 (a)，同时加上一条外环人类控制流份额规则：Teacher、Designer、Developer 进入 CORE 时，必须至少有一个 campaign 是 agent 在没有人挑选的情况下自主选择下一步的。这样 L2R、REvolve、DROC、ENPIRE 留在 CORE，Project Fetch 划入 RESOURCE，KnowNo 划入 B-loop。

## 5. 论文没有报告阶段划分时，默认按 runtime（Controller-lifelong）还是 development（Developer）处理？

- 选项：(a) 默认 runtime。(b) 默认 development。(c) 默认判 UNRESOLVED。
- 推荐：选 (a)。这是对「Developer 席位已经打开」这一论点不利的保守方向，可以防止外环 seat 被高估。审计后逐篇改判，涉及 DynaHarness、LRLL、RoboSkill、RoboFoundry、RoboHarn-Evo，并报告改判前后的计数。

## 6. 趋势统计以什么为单位？

- 选项：(a) 主 seat。(b) seat 向量（all-seat counting）。(c) 两种都报告。
- 推荐：选 (b) 作为主统计单位，主 seat 只用于章节归属，附录同时给出 innermost 和 outermost tie-break 的结果。Developer 2026 这一结论只在 all-seat 下稳健：all-seat 为 24%，innermost 下只有 7%。

## 7. CORE-P（55 篇）是否进入正文计数？

- 选项：(a) 正文只计 CORE，CORE-P 放附录。(b) 合并计数。(c) 两套数字并列报告。
- 推荐：选 (c)：图表中 CORE-P 用阴影区分。投稿前先完成 CORE-P 与 UNRESOLVED 的审计，再冻结数字。

## 8. 章节怎样组织？

- 选项：(a) 每个 seat 一章，Controller 按 Interface 或 carrier 再拆。(b) 运行时（Controller + Supervisor）与外环（Teacher + Designer + Developer）两部分。(c) 按 carrier 组织。
- 推荐：选 (a)。Controller 拆成四个子章：编排者（skill/tool/policy 调用）；直接驱动者（micro-actions、native commands、code）；lifelong/memory agent；训练过的 carrier（C/H/I，含内化）。multi-agent 和 harness 作为横跨各章的专题框。

## 9. 主线一句话怎么写？

- 选项：(a) 'Agency spreads around the body — and loop closure, not weights, makes a carrier an agent.'（b）'Steer and shape'，即双环论点。(c) 'Deliberate outside, compile inside'。
- 推荐：选 (a)。(c) 与测试集不符：2026 年仍有 63% 的 CORE 含 Controller coupling，且约一半 Developer 论文保留运行时 agent。(b) 可以作为副标题。接口主张只作为受控证据单列。

## 10. Examiner（agent 编写评测、对抗测试、红队）是否独立成 seat？

- 选项：(a) 作为 Designer 的子型。(b) 设为第六个 seat。
- 推荐：选 (a)。测试集中只有 GenManip（B-loop）和 ENPIRE 的次 seat 属于这一类，样本太少，不足以撑起一个主类别。等安全或红队方向的文献补齐后再评估。

## 11. memory、playbook 与 Developer、Teacher 之间的界线怎么划？

- 选项：(a) 评测期间自己写、自己读的 memory 归 Controller（记 locus）；独立阶段产出、冻结后被另一个 agent 或后继读取的 playbook 归 Teacher；被执行、并在至少两个实例中复用的代码归 Developer。(b) 所有持久 artifact 一律归 Developer。
- 推荐：选 (a)。按这条规则，RHD 归 Teacher，ExpTeach 和 DROC 归 Controller，RHO 和 HarnessPAI 归 Developer。仅优化 prompt 的工作按「是否在独立阶段产出并冻结」判定。

## 12. 如何对接 robot-use agent 社区的命名？

- 选项：(a) 直接采用 'robot-use agent'，作为 Controller-G 中直接驱动者子类的别名。(b) 不采用。
- 推荐：选 (a)。在 Controller 章开头说明 robot-use agent = Controller-G × {micro-actions、native commands、code}，并在差异化表中写明与 Show Lab 列表、Awesome-Robot-Use-Agent 的映射。

## 13. 验证与审计流程怎么定？

- 选项：(a) 从 data/candidates 按年份分层随机抽 150 篇，加约 40 篇难例压力子集，两人盲标，逐步报告 κ。(b) 只对难例做审计。
- 推荐：选 (a)。逐步报告 Q0a–Q0f、Q1–Q5、Q6–Q8 的 κ，并单独报告 tier 和主 seat 的 κ。P1 与 P2 只在独立样本上检验。如果独立样本推翻 P1 或 P2，就改写主线。

