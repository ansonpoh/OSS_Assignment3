# Evidence for tests that produce no gh-aw artifacts

Exported with `gh api` on 2026-10-23.

- `killswitch-*`: with the repository variable `TRIAGE_AGENT_ENABLED=false`, test issue #23 started
  triage run 39916646675; all six jobs (including `agent`) were skipped, and no label or comment was
  added (the one comment on #23 is the FAQtory bot's).
- `auth-failure-*`: the first attempt of run 39910044209 (issue #1) with an invalid OpenAI key. The agent
  got `401 Unauthorized` on every attempt, the `agent` job failed, and `safe_outputs` had nothing to
  apply. The excerpt is from the agent job log, with the key suffix redacted.
