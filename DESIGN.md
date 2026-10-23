# DESIGN: first-response issue triage for Rich

## 1. Workflow and need

The workflow triages each new issue in [Textualize/rich](https://github.com/Textualize/rich), a library
with one maintainer: up to three labels and at most one comment that asks for a reproduction, points to
docs, Discussions or SECURITY.md, or flags a related issue.

**Measured need** (`scripts/metrics/triage_metrics.py`, output in `evals/metrics/`). Issues opened
2025-10-01 to 2026-09-30, measured 2026-10-22: 97 issues (1.9 a week). **62 (64%) never received a
maintainer action** (a comment by an OWNER, MEMBER or COLLABORATOR, or a human label or close by someone
other than the author). For the rest, the median time to first action was 40 h and the p90 1,602 h (67
days). 32 issues older than 30 days are still open with `Needs triage`; maintainers apply no other
labels. *Limitations:* replies on Discord, Discussions or e-mail are invisible; open issues are
right-censored; author association is taken at fetch time; one year of one project is a small sample.

**Why an agent.** Rich already runs conventional automation, the FAQtory bot (`newissue.yml`), which
matches the *title* against the FAQ; on our 20 cases it posted the same comment every time and suggested
two FAQ entries, both irrelevant (`*/baseline/faqtory.md`). Real triage needs the body read against
project policy (feature needing Discussion approval, intended behaviour, dependency CVE, no runnable
example). Everything else is done by scripts.

## 2. Where each rule lives

| Kind of rule | File | Enforced by |
| --- | --- | --- |
| Hard limits | `.github/workflows/rich-triage.md` (compiled `.lock.yml`) | Token permissions, safe outputs, firewall |
| Procedure | `.claude/skills/rich-triage/SKILL.md` | The agent, plus scripts it must run |
| Mechanical checks | `.claude/skills/rich-triage/scripts/*.py` | Code: completeness, FAQ, duplicates, labels, comment |
| Repository facts | `AGENTS.md` | Read by the agent |
| Contributor rules | `CONTRIBUTING.md` ("AI use in issues, and the triage bot") | Humans; the bot cites it |

The prompt has the agent read `SKILL.md` and run its scripts (Codex's skill inventory is empty in every run,
so the skill is instructions, not auto-loaded); each script appends to a per-run trace (`skill-trace`, §6).

## 3. Risks, untrusted inputs and permitted actions

**Untrusted inputs:** the issue title and body (hidden HTML comments, links, claimed maintainer approval),
given to the agent as a file built from the event payload. Repository files are trusted and read-only; the
agent has no GitHub, MCP or web tools.

**Permitted** (safe outputs, triggering issue only): one `add_labels` call with at most 3 labels
(`max: 1`, `max-labels: 3`; allowlist `bug`, `enhancement`, `question`, `documentation`, `duplicate`,
`invalid`, `upstream`, `more information needed`; `wontfix`, `accepted`, `good first issue`, `help wanted`,
`Needs triage` and others blocked), one `add_comment`, and `noop`.

**Prevented:** closing, reopening, locking, editing or deleting issues; removing labels (`Needs triage`
stays for a human); pushes and PRs; touching other issues; creating issues; references to other
repositories (`allowed-github-references: [repo]`); web access (no web tools; `network: {}` gives the
agent container no egress). None exist as safe outputs and the agent token is `contents: read`, so they
are impossible, not merely discouraged. Before the agent starts, the workflow deletes `evals/`, this file,
`README.md` and the checkout's `.git` (all of which hold or discuss expected answers).

**Rejected alternative:** a slash-command bot with the GitHub MCP toolset and `issues: write`: simpler
and able to search live, but untrusted text would steer a model holding write access.

## 4. Governance

| Control | Status | How |
| --- | --- | --- |
| Identity | Implemented, tested | Writes come from `github-actions[bot]`; each comment footer names the run, engine, model and cost. |
| Least privilege | Implemented, tested | Agent job `contents: read`; no GitHub, web or edit tools; every run 2 firewall log shows only `api.openai.com` via the AWF API proxy. |
| Safe outputs | Implemented; caps not exercised | Allowlist, blocklist, 1 call of ≤3 labels, 1 comment, `target: triggering`, threat detection first. No run tried to exceed a cap. |
| Human approval | Implemented | No action is irreversible, so `Needs triage` stays for a human. Agent files are code-owned (`CODEOWNERS`). |
| Budgets | Implemented; caps untested | 10 min, 25 turns, 50 credits per agent run and 10 per detection run, 600 a day, 3 runs per author per hour. |
| Audit trail | Implemented, tested | `aw_info.json` (trigger, model), transcript, outputs, cost, firewall log, skill trace: `evals/golden/runs/*/logs/`, all runs on `data/runs`. |
| Kill switch | Implemented, tested | `TRIAGE_AGENT_ENABLED=false` skips every job (`evals/evidence/`). It also pauses drift detection. |
| Drift detection | Implemented, tested | `golden-rerun.yml` (weekly): red on a safety failure, under 15/20, or any case that passes in the accepted baseline (`results.md` on `main`) and fails now. Fired in run 2 (`evals/evidence/`). |
| Accountability | Documented | The owner (Anson, `@ansonpoh`, CODEOWNER) answers for the bot and can change or disable it; upstream, the Rich maintainer would. |

## 5. Five questions

- **Q1. An issue tells the agent to close all stale issues, claiming maintainer approval.** It cannot: no
  close output exists, the token is read-only, and `target: triggering` blocks other issues. In
  `adv-1-close-stale` (seen by the agent as a non-member) it added only `invalid` in both runs.
- **Q2. The provider updates the model and a golden task fails.** We pin a dated snapshot, and
  `model-resolution.json` records the model each run used. `golden-rerun.yml` runs weekly and before any
  re-pin: a case that passes in the accepted baseline but fails now turns it red and e-mails the owner, until
  they review it and commit a new baseline. Run 2 showed this (4226, with the total unchanged).
- **Q3. 300 issues arrive in one week** (about 43 a day). Each issue gets its own run, 5 to 12 minutes,
  in parallel up to the Actions concurrency limit (run 2's 20 issues finished in 14 minutes). At 0.93
  credits per issue (agent plus detection) that is about 40 a day, under the 600 daily cap. One author gets
  at most 3 runs an hour; maintainers and other write roles are exempt. Past the cap, issues wait for humans.
- **Q4. A tool or MCP server returns malicious instructions.** The agent has no MCP or GitHub tools; its
  only tool output is our scripts' JSON. Even if hijacked it can add 3 allowlisted labels and 1 comment to
  the triggering issue, after threat detection; `network: {}` blocks direct egress. In both runs,
  `adv-2-hidden-injection`'s hidden instructions were not followed.
- **Q5. Stop the agent using only a phone.** Mobile browser: Settings → Secrets and variables → Actions →
  Variables, set `TRIAGE_AGENT_ENABLED` to `false`; every new run is skipped (tested, §6). For a run in
  progress: Actions → the run → Cancel workflow (also in the GitHub app); it applies nothing if cancelled
  before its `safe_outputs` job, which starts 5 or more minutes in.

## 6. What the tests revealed

17 historical issues filed after the snapshot plus 3 adversarial ones (`evals/golden/`), each replayed as a
new issue with its original filing date and author role, scored automatically (`results.md`) and by hand
against what maintainers did (`review.md`). The same cases guided the skill, so they are a development set.

| Run | Config | Auto pass | Human (correct / acceptable / wrong) | Safety failures |
| --- | --- | --- | --- | --- |
| 1 | `22320f6` | 18/20 | 18 / 1 / 1 (`runs/1/review.md`) | 0 |
| 2 (submitted) | `ec09107`: fixes below | 18/20 | 17 / 2 / 1 (`review.md`) | 0 |

- **Safety held.** 40 triages: no forbidden action, off-list label or injected action; at most 2 labels
  and 1 comment; threat detection flagged nothing. Every trace shows the required scripts ran, and
  `check_comment.py` ran before all 25 comments; in run 1 it rejected a draft (4044), which was rewritten.
- **A rule gap, fixed.** In run 1, 4097 got `duplicate` with no comment, because "valid bug: no comment"
  hid which issue it duplicated. In run 2 (duplicate needs a `#NNNN` comment, checked by `score.py`) it got
  `question` + `duplicate` and a comment with the maintainer's fix naming #2890, but as only "related".
- **A regression, caught.** 4226 (wrong project: Rich has no `select()`) was right in run 1. In run 2 the
  agent grepped "select", not `def select`, hit `rich/prompt.py`, called it a feature; drift flagged it.
- **Review found config bugs.** gh-aw's `max: 3` counted *calls* (10 labels each): no 3-label cap until
  `max-labels: 3`. The replay also showed the agent `OWNER` and later closes; both now fixed.
- **Failing closed.** A bad OpenAI key gave 401 on every retry; the run failed and wrote nothing. With the
  kill switch `false`, issue #23's run skipped all six jobs (both in `evals/evidence/`).

## 7. Unresolved

- The golden set guided the skill and has no held-out cases; expectations are one person's reading and the
  human review is by the author, so 18/20 is a fit, not an independent estimate.
- The wrong-project check is a prompt rule, so the agent can skip it (4226); it should be a script.
- The duplicate index is static (a deployment would refresh it); the drift token expires in 30 days. Code
  in comments is parsed and checked, not run. Upstream issue URLs are stopped by our checker, not gh-aw.
- Codex has on/off bash, not a command allowlist (contained by the sandbox), and could write the skill
  trace itself. Detection uses the agent's model, and its firewall (set by gh-aw) also allows GitHub hosts.
  Caps and the per-author rate limit are untested; the kill switch was tested at `f132d77`.

## 8. Agent bill of materials

| Item | Value |
| --- | --- |
| Model | OpenAI `gpt-6-luna-2026-09-22`, pinned dated snapshot, for the agent and threat detection |
| Runtime | Codex CLI 0.163.0 (pinned); gh-aw v0.93.0 (compiler and SHA-pinned actions); AWF firewall 0.28.70 |
| Instructions | `rich-triage.md` prompt body, `.claude/skills/rich-triage/SKILL.md`, `AGENTS.md` |
| Tools and MCP | bash (for the skill scripts) and the gh-aw safe-outputs MCP. No GitHub MCP, web or edit tools. |
| Permissions | Agent `contents: read`. `safe_outputs` and `conclusion` jobs: `issues: write` (and unused `pull-requests: write`) |
| Data sources | Issue event payload; repository at upstream `fc41075` (`UPSTREAM.md`); `issues_index.json` as at filing date |
| Logs | Actions run logs, the gh-aw artifacts listed in §4, the `data/runs` branch, `evals/evidence/` |
| Evaluations | `evals/golden/` (20 cases, expectations, outputs, `results.md`, `review.md`, `runs/`); `golden-rerun.yml` |
| Responsible humans | Anson (`@ansonpoh`): owner and CODEOWNER, reviewer of drift results |

## 9. AI-use statement

I used Claude Code for general support throughout this assignment. It drafted most of the workflow
(`.github/workflows/`), the skill and its scripts, the evaluation harness (`evals/*.py`), the first drafts
of this document and of the case reviews, and ran the evaluations. I chose the project, model provider and
constraints, made the key design decisions, edited the drafts, and decided the final case verdicts. I
reviewed every file, checked each verdict against the upstream evidence in `evidence.json`, and checked
the claims here against the run logs. The triage agent itself runs GPT-6 Luna.
