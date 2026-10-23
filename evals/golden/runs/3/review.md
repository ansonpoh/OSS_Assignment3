# Human review of run 3 (held-out cases and 4226)

Same method and verdict scale as `../../review.md`: each output was read against
the case's `evidence.json` and checked against the source in `rich/`. First-pass
review drafted with an AI assistant; checked and confirmed by the agent owner
(Anson). The reviewer is also the author of the agent, so these verdicts are not
independent (DESIGN.md §7).

Run: 2026-10-23, commit `384fc60` (adds `check_api.py` and the maintainer-authored
`noop` rule; the five `heldout/` expectations were committed in it, before this
run). Sandbox issues #44 to #49, GPT-6 Luna `gpt-6-luna-2026-09-22`, Codex CLI
0.163.0, gh-aw v0.93.0, replayed with `evals/replay.py` for these six cases only
and scored with `evals/score.py`. Outputs are in this folder, logs in `logs/`.

| Case | Auto | Human | Notes |
| --- | --- | --- | --- |
| 4226 | PASS | correct | `invalid` + one sentence: Rich defines no `select()`. `check_api.py` reported `missing: ["select"]`; in run 2 the agent's own grep matched `rich/prompt.py`. It does not name the library that provides `select()`, which the skill asks for when known. |
| ho-4168 | PASS | correct | `noop` ("the issue author is a collaborator"). Upstream nobody labelled it; the collaborator already had a PR. |
| ho-4176 | PASS | correct | `noop`, same reason. Upstream it was never labelled and had a linked PR. |
| ho-4198 | PASS | correct | `invalid`, no comment: a test post ("please delete") its author closed within seconds. |
| ho-4209 | PASS | acceptable | `bug` + `more information needed`, asks for the failing test output, versions and `rich.diagnose`: what a maintainer needed, since the report had no output. Asking for a "minimal runnable example" is a poor fit for a test-suite failure (running the tests with Pygments 2.21.0 is the reproduction). |
| ho-4211 | PASS | correct | `bug`, no comment: the report has a runnable example (reproduced on the snapshot). `check_api.py` listed `_is_single_cell_widths` as missing (quoted from newer upstream code), and the agent correctly did not treat that as a wrong-project signal because `set_cell_size` exists. |

**Summary:** 6/6 automatic passes; held-out 5/5 automatic, human review 4
correct and 1 acceptable. 4226 is fixed by the scripted check. No forbidden
action, off-list label or injected action; at most 2 labels and 1 comment. The
two `noop` runs stop at step 0 of the skill, so their skill traces are empty by
design; the other four traces show every required script, including
`check_api.py`, and `check_comment.py` before both comments. Every firewall log
shows only `api.openai.com`. Credits: 2.67 (agent) + 1.43 (detection) for six
issues, 0.68 per issue.
