# Upstream snapshot

The sandbox contains a copy of [Textualize/rich](https://github.com/Textualize/rich)
at commit `fc41075a3206d2a5fd846c6f41c4d2becab814fa` (2026-02-26, "Merge pull request #4026").
Rich is MIT licensed; see `LICENSE`.

This is the last upstream commit before the golden-case window (issues filed
2026-03-01 to 2026-09-30), so the agent never sees repository files that were
written after an evaluated issue was filed. The FAQ, `AI_POLICY.md`,
`CONTRIBUTING.md` and issue templates did not change upstream between this
commit and 2026-09-30 (checked with `git log` on those paths); later code
changes (e.g. Rich 15.0.0 dropping Python 3.8) are absent.

Removed from the snapshot: upstream `README.md` (replaced), `.github/dependabot.yml`,
`.github/FUNDING.yml`, and the `codeql`, `codespell`, `readmechanged` and
`comment` workflows (noise in a sandbox). `newissue.yml` (the FAQtory bot) is
kept on purpose, with its checkout ref changed from `master` to `main`: it is the conventional-automation baseline the agent is
compared against.
