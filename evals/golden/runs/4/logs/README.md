# Test logs of run 4

One folder per case, copied from the run's gh-aw artifacts (exported by
`.github/workflows/export-runs.yml` to the `data/runs` branch, under
`evals/runs/run-<run id>/`). Run ids are in `../<case>.json` and `../results.md`.

| File | What it shows |
| --- | --- |
| `aw_info.json` | Trigger, workflow, engine, pinned model and CLI version |
| `agent_model-resolution.json` | Model the run actually resolved to |
| `aw-prompts_prompt.txt` | Full prompt given to the agent |
| `agent-session.jsonl` | Agent transcript: messages, shell commands and their output |
| `skill-trace.jsonl` | One line per skill script run (evidence the skill was loaded and used) |
| `skill_inventory.json` | Skills installed in the agent container |
| `safeoutputs.jsonl` | Safe outputs the agent requested (labels, comment, noop) |
| `detection_detection_result.json` | Threat-detection verdict before any write |
| `detection_usage.json` | Tokens and AI credits used by threat detection |
| `agent_usage.json` | Tokens and AI credits used |
| `sandbox_firewall_logs_access.log` | Firewall log of all egress from the sandbox |

Apart from local `::1` health checks, every case's firewall log contains only `api.openai.com`
traffic from the AWF API proxy (`172.30.0.30`); the agent container made no other outbound connections.
