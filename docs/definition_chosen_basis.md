基础方案取 **"Five Seats Around the Body"**，即以角色为中心的 Seat 主轴。这个选择依据的是 stress test 的结果，不是个人偏好：
- 两轮 stress test 中，它的 crispness 都最高（6/5，另外两套方案为 5/5 和 5/4）。
- novelty 并列最高（8/6）。
- 它能把用户点名的四个案例全部干净地放进各自的 seat：GUAVA 为 T|C，ENPIRE 为 Dv|Ds，CaM 为 S|C，Harness VLA 和 Show-Harness 为 C。
- 它的失败都出在 agent 判定和判定程序的措辞上，可以逐条修复。另外两套方案的失败则是结构性的。

**为什么不选 Loop-of-Influence 作主轴**
- 它的 C/T 划分实际上重新引入了模块 locus。stress test 发现 Embodied-Navigator 与 RoCo、π0.5 与 Hi Robot 两组判定互相矛盾。
- 它的 L/D 划分对「产出数据的代码」没有定义。
- 它的主线论点被时间线（Eureka 早于 CaM）和语料计数同时推翻。

**为什么不选 AMM 作主轴**
- 先问 P7（Q1 优先）会让 P7 成为吸收一切的类别。
- 它的主轴混合了 ring、carrier 和贡献类型三种东西。
- 依照它字面的 fixed-scheduler ablation，Λ1 这一 boundary 层根本无法到达。
- 它约一半的样例经不起自身规则的检验。

为保留用户「agency 在哪里」这条主线，中心图采用 **Seat × Carrier 网格**。这一点回应了 stress test 中「demoted locus」的批评。

**从 AMM 嫁接**
- carrier 阶梯 G/C/H/I，并把「协同设计」写成可操作的检验。
- Provenance 列。
- Residual 列（降为一列，并用列联表说明为什么降级）。
- F0–F3 保真度编码，并按 critic 的要求改为 primitive-realization 检验。
- 迁移箭头作为 anatomy 的一部分。
- Λ 闭环强度阶梯，拆成「强度」和「cadence」两个字段，并去掉 Λ4。
- 结构化的 Supervisor 定义：检查过程必须与名义决策过程分开。

**从 Loop-of-Influence 嫁接**
- 用 production phase、而不是 consumption 来判定 seat。
- 持久性条款：Developer 的 artifact 必须在 ≥2 个评测实例中被复用。
- 把 closure 与 consumption 分开。
- 单列 RESOURCE/BENCH 层，并标注 evaluated seat。
- organ 层：A0 输出类型检查。
- verifier 所有权 / permission surface。
- 「dream vs decide」的 WAM 边界。

**本轮针对 critic 的修复**
- Q1 改为按 production phase 判断。Q2 采用 counterfactual 检验，并对 Supervisor 加上「检查过程需独立」的条件。
- problem/solution 划分写进 Q3 和 Q5：reward、env、success、curriculum 即使经过 keep/revert，也一律归 Designer。
- A2 统一为「生成式」或「选择式 + 控制行为」，并在 SayCan、KnowNo、SG-Nav、Co-NavGPT、PIVOT、FOREWARN、RoboMonkey、Eureka、MEMENTO 上一并应用。
- A3 定义了环实例，并要求输入中包含自身记录。
- 引入 E/H/M 三类 closure：CORE 需要至少一个 E 或 H closure，M-only 判 B-loop。
- 新增 CORE-P 和 UNRESOLVED 两个 tier。
- 机器人形态条款与 F 判据。
- 人类证据区分「整合」与「替代」，并对外环中人类控制流的份额定下规则。
- 用 headline 消融取代「第一张表」规则；统计以 seat 向量为单位。
- 主线收窄为「spread + loop-not-weights」，接口主张降为受控证据。
- 所有计数都从 350 条去重后的逐条判定中算出，并同时报告含与不含 CORE-P 的数字。