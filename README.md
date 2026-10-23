# Rich issue-triage agent (OSS Assignment 3)

A GitHub Agentic Workflow (gh-aw) that does first-response triage of new issues
for a sandbox copy of [Textualize/rich](https://github.com/Textualize/rich)
(snapshot details in `UPSTREAM.md`). It proposes up to three allowlisted labels
and at most one comment, and can do nothing else. **`DESIGN.md` is the main
write-up.**

| What | Where |
| --- | --- |
| Workflow source and compiled lock file | `.github/workflows/rich-triage.md`, `rich-triage.lock.yml` |
| Triage procedure and scripts | `.claude/skills/rich-triage/` |
| Repository facts for agents | `AGENTS.md` |
| Contributor rules, AI use, the bot | `CONTRIBUTING.md` (last section) |
| Golden set, actual outputs, results | `evals/golden/` (`README.md`, `results.md`, `review.md`) |
| Need measurement | `scripts/metrics/`, output in `evals/metrics/` |
| Run logs and audit exports | `data/runs` branch (from `export-runs.yml`), `data/golden-runs` |

## Rebuilding the lock file

```bash
gh extension install github/gh-aw --pin v0.93.0
gh aw compile rich-triage --action-mode action --action-tag v0.93.0
```

## Reproducing the evaluation

See `evals/golden/README.md` ("Reproducing"). In short: create a repository
from this one, add the `OPENAI_API_KEY` secret, then run
`evals/setup_sandbox.py`, `evals/replay.py` and `evals/score.py` against it.
