# Full-text re-judge of the core table (2026-10-09)

After the user's rules "the agent must be a general large model, not a model the authors trained" and "the paper must
be about the agent, not a data platform", all 174 rows of `data/core/paper_list.csv` were re-judged from the
papers' full text (arXiv PDF → pdftotext; the texts are not stored here).

- `k00.tsv` … `k17.tsv`: input shards (key, arXiv id, title).
- `k00.txt` … `k17.txt`: one line per paper from Sonnet subagents following `screening/prompts/content_rejudge.txt`:
  `key|arxiv|decision_model|model_status|main_contribution|connection|verdict|layer|subtype|evidence|reason`.
  model_status: G general model used as-is, FT trained / fine-tuned by the authors, SPEC VLA or specialist, NONE.

All verdicts were applied to the CSV unchanged; layer labels such as "L1 准备层" were normalised to "L1", and for
resources the evaluated layer went to `layer` with `评测Lx` in `subtype`.

Later the same day the user went back to two phases and five seats (pre-execution: Designer, Teacher, Developer;
runtime: Controller, Supervisor). The three-layer labels in these outputs were mapped to seats in
`data/core/paper_list.csv` (layer/subtype → seat/role, with 12 papers decided by hand; see each row's note), so these
files are a record of the reading, not something to re-apply.
