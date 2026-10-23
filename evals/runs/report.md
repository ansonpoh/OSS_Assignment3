# Audit Report — Cross-Run Analysis

## Executive Summary

| Metric | Value |
|--------|-------|
| Runs analyzed | 30 |
| Runs with firewall data | 30 |
| Runs without firewall data | 0 |
| Total requests | 835 |
| Allowed requests | 835 |
| Blocked requests | 0 |
| Overall denial rate | 0.0% |
| Unique domains | 1 |

## Metrics Trends

| Metric | Total | Avg/run | Min | Max | Spikes |
|--------|-------|---------|-----|-----|--------|
| Token Trend | 8638892 | 287963 | 153293 | 717931 | ⚠ #39923893693 |
| Turns | 30 | 1.0 | — | 1 | — |
| Duration | — | 8.2m | 5.1m | 11.5m | — |

## MCP Server Health (30 runs)

| Server | Connected | Error Rate | Total Calls | Errors | Status |
|--------|-----------|------------|-------------|--------|--------|
| `safeoutputs` | 30/30 | 0.0% | 48 | 0 | ✅ ok |

## Domain Inventory

| Domain | Status | Seen In | Allowed | Blocked |
|--------|--------|---------|---------|--------|
| `api.openai.com:443` | ✅ allowed | 30/30 runs | 835 | 0 |

## Agent Event Pattern Analysis

| Severity | Category | Title | Summary |
|----------|----------|-------|--------|
| ℹ info | execution | Cross-run log template patterns | Mined 2 distinct event templates across 6 pipeline stages from 60 events in 30 runs. (finish=1 plan=1) |

## Cluster Patterns

| Severity | Kind | Title | Description |
|----------|------|-------|-------------|
| 🟡 low | style_skew | Dominant execution_style: exploratory | 90% of runs share execution_style="exploratory" (27/30). Low diversity may indicate homogeneous workload or classification bias. |
| 🟡 low | style_skew | Dominant resource_profile: heavy | 90% of runs share resource_profile="heavy" (27/30). Low diversity may indicate homogeneous workload or classification bias. |
| 🟡 low | style_skew | Dominant graders: pass | 93% of runs share graders="pass" (28/30). Low diversity may indicate homogeneous workload or classification bias. |

## Run Clusters

| Dimension | Value | Runs | Avg Tokens | Avg Turns | Avg Duration | Success Rate |
|-----------|-------|------|------------|-----------|--------------|-------------|
| execution_style | adaptive | 3 | 175160 | 1.0 | 9.0m | 100% |
| execution_style | exploratory | 27 | 300496 | 1.0 | 8.1m | 100% |
| resource_profile | heavy | 27 | 300496 | 1.0 | 8.1m | 100% |
| resource_profile | moderate | 3 | 175160 | 1.0 | 9.0m | 100% |
| graders | mixed | 2 | 296295 | 1.0 | 9.2m | 100% |
| graders | pass | 28 | 287367 | 1.0 | 8.1m | 100% |

## Per-Run Breakdown

| Run ID | Workflow | Conclusion | Duration | Firewall | Tokens | Turns | MCP Err | Errors |
|--------|----------|------------|----------|----------|--------|-------|---------|--------|
| 39924044942 | Rich issue triage | success | 8.6m | 22/0 | 195.2K | 1 | 0 | 0 |
| 39924034889 | Rich issue triage | success | 10.7m | 28/0 | 237.0K | 1 | 0 | 0 |
| 39924022369 | Rich issue triage | success | 11.2m | 20/0 | 177.0K | 1 | 0 | 0 |
| 39924012648 | Rich issue triage | success | 10.3m | 33/0 | 328.9K | 1 | 0 | 0 |
| 39924001081 | Rich issue triage | success | 8.5m | 26/0 | 328.9K | 1 | 0 | 0 |
| 39923988855 | Rich issue triage | success | 6.8m | 20/0 | 183.0K | 1 | 0 | 0 |
| 39923977377 | Rich issue triage | success | 8.0m | 36/0 | 337.3K | 1 | 0 | 0 |
| 39923966963 | Rich issue triage | success | 7.7m | 28/0 | 358.5K | 1 | 0 | 0 |
| 39923955422 | Rich issue triage | success | 7.5m | 25/0 | 239.0K | 1 | 0 | 0 |
| 39923932900 | Rich issue triage | success | 6.4m | 33/0 | 320.5K | 1 | 0 | 0 |
| 39923918959 | Rich issue triage | success | 10.0m | 39/0 | 554.2K | 1 | 0 | 0 |
| 39923904973 | Rich issue triage | success | 11.5m | 23/0 | 246.9K | 1 | 0 | 0 |
| 39923893693 | Rich issue triage | success | 9.1m | 52/0 | 717.9K ⚠ | 1 | 0 | 0 |
| 39923886099 | Rich issue triage | success | 7.1m | 20/0 | 153.3K | 1 | 0 | 0 |
| 39923874287 | Rich issue triage | success | 5.8m | 36/0 | 346.1K | 1 | 0 | 0 |
| 39923864011 | Rich issue triage | success | 5.6m | 32/0 | 290.6K | 1 | 0 | 0 |
| 39923852434 | Rich issue triage | success | 5.3m | 19/0 | 155.6K | 1 | 0 | 0 |
| 39923842388 | Rich issue triage | success | 6.4m | 25/0 | 212.3K | 1 | 0 | 0 |
| 39923830583 | Rich issue triage | success | 5.1m | 28/0 | 307.7K | 1 | 0 | 0 |
| 39911695776 | Rich issue triage | success | 10.8m | 21/0 | 230.7K | 1 | 0 | 0 |
| 39911687908 | Rich issue triage | success | 8.0m | 21/0 | 177.9K | 1 | 0 | 0 |
| 39911677905 | Rich issue triage | success | 10.1m | 23/0 | 194.9K | 1 | 0 | 0 |
| 39911668874 | Rich issue triage | success | 10.7m | 38/0 | 340.2K | 1 | 0 | 0 |
| 39911657500 | Rich issue triage | success | 10.0m | 28/0 | 263.7K | 1 | 0 | 0 |
| 39911649232 | Rich issue triage | success | 6.3m | 24/0 | 276.9K | 1 | 0 | 0 |
| 39911637873 | Rich issue triage | success | 7.1m | 16/0 | 187.1K | 1 | 0 | 0 |
| 39911628498 | Rich issue triage | success | 9.5m | 32/0 | 317.4K | 1 | 0 | 0 |
| 39911598927 | Rich issue triage | success | 6.4m | 30/0 | 340.4K | 1 | 0 | 0 |
| 39911590068 | Rich issue triage | success | 8.4m | 27/0 | 354.7K | 1 | 0 | 0 |
| 39911578649 | Rich issue triage | success | 5.9m | 30/0 | 265.1K | 1 | 0 | 0 |

