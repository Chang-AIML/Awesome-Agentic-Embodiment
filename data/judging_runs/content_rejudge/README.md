# Full-text re-judge of the core table (2026-10-09)

After the user's rules "the agent must be a general large model, not a model the authors trained" and "the paper must
be about the agent, not a data platform", all 174 rows of `data/core/layer_classification.csv` were re-judged from the
papers' full text (arXiv PDF → pdftotext; the texts are not stored here).

- `k00.tsv` … `k17.tsv`: input shards (key, arXiv id, title).
- `k00.txt` … `k17.txt`: one line per paper from Sonnet subagents following `screening/prompts/content_rejudge.txt`:
  `key|arxiv|decision_model|model_status|main_contribution|connection|verdict|layer|subtype|evidence|reason`.
  model_status: G general model used as-is, FT trained / fine-tuned by the authors, SPEC VLA or specialist, NONE.

All verdicts were applied to the CSV unchanged; layer labels such as "L1 准备层" were normalised to "L1", and for
resources the evaluated layer went to `layer` with `评测Lx` in `subtype`.
