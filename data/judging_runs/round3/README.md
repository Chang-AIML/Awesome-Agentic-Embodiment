# Raw judging outputs, round 3

One directory per judging pass; the directory name is the `pass` value in `data/core/fine_labels.csv`.
Each `kNN.txt` is one sub-agent's output for one shard, one line per paper:

- fine judging: `id|verdict|seat|seat2|carrier|sub|interface|topo|closure|body|rep|conf|loop|reason`
  (`screening/prompts/fine_judge.txt`, rubric `screening/criteria_fine.md`)
- `coarse_prefilter/`: `id|label|type|role|reason` (`screening/prompts/coarse_screen.txt`), imported with
  `scripts/build_completion_pools.py prefilter data/judging_runs/round3/coarse_prefilter`

| pass | model | what it judged |
|---|---|---|
| `s2` | Haiku | S2 keyword-sweep pool (`pool_s2.jsonl`) |
| `verify_s2` | Sonnet | Haiku core / precursor / boundary of the S2 pool (k00-k03 and the later k100-k101) |
| `recheck_r3b` | Sonnet | constraint-programming and agentic Real2Sim candidates under decisions 8-9 |
| `recheck_scope` | Sonnet | general vs embodied foundation models (decision 12) |
| `pre2026` | Haiku | 3,003 never fine-judged candidates (`pool_pre2026.jsonl`) |
| `pf` | Haiku | 961 candidates kept by the completion coarse pass (`pool_prefilter.jsonl`) |
| `verify_pre`, `verify_pf` | Sonnet | Haiku core / precursor / boundary of the two completion pools |
| `verify` | Sonnet | 268 bulk-pool verdicts the earlier verification had missed |
| `audit_out` | Sonnet | random sample of 300 Haiku `out` verdicts (2 flipped to core) |
| `recheck_direct` | Sonnet | 7 papers where a general model emits actions directly |

Earlier passes (`out`, `recheck`, `bulk`, the first `verify`) were run in sessions whose raw outputs are gone;
their results survive only in `fine_labels.csv` (columns and the `prev` chain). `merge_fine_labels.py --base`
adds new directories on top of the merged file.
