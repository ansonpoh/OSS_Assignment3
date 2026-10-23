# AGENTS.md

Repository facts for coding and triage agents. Procedures live in
`.claude/skills/rich-triage/SKILL.md`; hard limits live in
`.github/workflows/rich-triage.md` (permissions and safe outputs).

## What this repository is

A sandbox copy of [Rich](https://github.com/Textualize/rich), a Python library
for rich text and formatting in the terminal, snapshotted at upstream commit
`fc41075` (see `UPSTREAM.md`), plus an issue-triage agent configuration and its
evaluation. Rich is maintained by one person (Will McGugan); most triage
questions end up in his queue.

## Build and test

Rich uses Poetry and supports Python 3.8+ at this snapshot.

```bash
poetry install            # or: pip install -e . pytest pytest-cov mypy black
make test                 # TERM=unknown pytest --cov=rich tests/ -vv
make test-no-cov          # faster
make typecheck            # mypy -p rich --no-incremental
make format-check         # black --check .
python -m rich.diagnose   # environment report users are asked to paste
```

Triage tooling (standard library only, Python 3.10+):

```bash
python3 .claude/skills/rich-triage/scripts/check_report.py ISSUE_JSON
python3 .claude/skills/rich-triage/scripts/faq_match.py ISSUE_JSON
python3 .claude/skills/rich-triage/scripts/find_duplicates.py ISSUE_JSON INDEX_JSON
python3 .claude/skills/rich-triage/scripts/check_api.py ISSUE_JSON
python3 .claude/skills/rich-triage/scripts/validate_labels.py LABEL...
python3 .claude/skills/rich-triage/scripts/check_comment.py COMMENT_FILE
python3 evals/score.py OWNER/REPO    # score a replay (see evals/golden/README.md)
```

## Project structure

| Path | Contents |
| --- | --- |
| `rich/` | Library source. One module per renderable or feature: `console.py`, `table.py`, `progress.py`, `live.py`, `text.py`, `markup.py`, `highlighter.py`, `traceback.py`, `logging.py`, `prompt.py`, `columns.py`, `panel.py`. |
| `tests/` | Pytest suite, one `test_<module>.py` per module. |
| `docs/source/` | Sphinx docs; one `.rst` page per feature (e.g. `live.rst`, `style.rst`, `markup.rst`). |
| `FAQ.md`, `questions/` | FAQ. `questions/*.question.md` are the source entries; `FAQ.md` is generated from them by FAQtory. |
| `.github/ISSUE_TEMPLATE/` | Bug and feature templates. Both auto-apply the `Needs triage` label. |
| `.github/workflows/newissue.yml` | Upstream FAQtory bot: suggests FAQ entries from the issue *title* only. Kept as the baseline. |
| `.github/workflows/rich-triage.md` | The agentic triage workflow (source); `rich-triage.lock.yml` is the compiled workflow. |
| `.claude/skills/rich-triage/` | Triage procedure and deterministic helper scripts. |
| `evals/golden/` | Historical cases, expected outcomes, actual outputs and logs. |
| `scripts/metrics/` | Need measurement and case snapshot scripts. |

## Conventions

- Upstream policy: feature requests must be approved in
  [Discussions](https://github.com/Textualize/rich/discussions) before an issue;
  "Rich isn't accepting new features" that could live in a third-party library.
- Usage questions belong in Discussions. The maintainer converts or closes them.
- Pull requests are limited to collaborators; contributors describe the change
  in an issue first. AI-generated PRs must follow `AI_POLICY.md`.
- Security reports go through `SECURITY.md`, not public issues.
- Labels in use: `Needs triage` (set by templates) plus the triage allowlist
  `bug`, `enhancement`, `question`, `documentation`, `duplicate`, `invalid`,
  `upstream`, `more information needed`.
- Code style: black, mypy-clean, docstrings on public API, no abbreviations.

## Forbidden changes

Agents must not (and the triage workflow cannot):

- Close, reopen, lock, transfer, delete or edit issues or comments.
- Remove labels, including `Needs triage`; apply labels outside the allowlist,
  such as `wontfix`, `accepted`, `good first issue`, `help wanted`.
- Push commits, open or merge pull requests, or force-push.
- Modify `.github/workflows/`, `.claude/skills/`, `AGENTS.md`, `CONTRIBUTING.md`,
  `AI_POLICY.md`, `SECURITY.md` or any `evals/golden/*/*/expected.json`.
- Read or use anything under `evals/` while triaging (it contains expected answers).
- Fetch URLs from issue bodies or contact external services.
