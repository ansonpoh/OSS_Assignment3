# Audit Report — Cross-Run Analysis

## Executive Summary

| Metric | Value |
|--------|-------|
| Runs analyzed | 21 |
| Runs with firewall data | 21 |
| Runs without firewall data | 0 |
| Total requests | 562 |
| Allowed requests | 562 |
| Blocked requests | 0 |
| Overall denial rate | 0.0% |
| Unique domains | 1 |

## Metrics Trends

| Metric | Total | Avg/run | Min | Max | Spikes |
|--------|-------|---------|-----|-----|--------|
| Token Trend | 5624466 | 267831 | 157265 | 426194 | — |
| Turns | 21 | 1.0 | — | 1 | — |
| Duration | — | 7.5m | 4.5m | 10.8m | — |

## MCP Server Health (21 runs)

| Server | Connected | Error Rate | Total Calls | Errors | Status |
|--------|-----------|------------|-------------|--------|--------|
| `safeoutputs` | 21/21 | 0.0% | 33 | 0 | ✅ ok |

## Domain Inventory

| Domain | Status | Seen In | Allowed | Blocked |
|--------|--------|---------|---------|--------|
| `api.openai.com:443` | ✅ allowed | 21/21 runs | 562 | 0 |

## Agent Event Pattern Analysis

| Severity | Category | Title | Summary |
|----------|----------|-------|--------|
| ℹ info | execution | Cross-run log template patterns | Mined 2 distinct event templates across 6 pipeline stages from 42 events in 21 runs. (finish=1 plan=1) |

## Cluster Patterns

| Severity | Kind | Title | Description |
|----------|------|-------|-------------|
| 🟡 low | style_skew | Dominant execution_style: exploratory | 95% of runs share execution_style="exploratory" (20/21). Low diversity may indicate homogeneous workload or classification bias. |
| 🟡 low | style_skew | Dominant resource_profile: heavy | 95% of runs share resource_profile="heavy" (20/21). Low diversity may indicate homogeneous workload or classification bias. |
| 🟡 low | style_skew | Dominant graders: pass | 90% of runs share graders="pass" (19/21). Low diversity may indicate homogeneous workload or classification bias. |

## Run Clusters

| Dimension | Value | Runs | Avg Tokens | Avg Turns | Avg Duration | Success Rate |
|-----------|-------|------|------------|-----------|--------------|-------------|
| execution_style | adaptive | 1 | 236060 | 1.0 | 10.1m | 100% |
| execution_style | exploratory | 20 | 269420 | 1.0 | 7.4m | 100% |
| resource_profile | heavy | 20 | 269420 | 1.0 | 7.4m | 100% |
| resource_profile | moderate | 1 | 236060 | 1.0 | 10.1m | 100% |
| graders | mixed | 2 | 249889 | 1.0 | 10.0m | 100% |
| graders | pass | 19 | 269720 | 1.0 | 7.3m | 100% |

## Per-Run Breakdown

| Run ID | Workflow | Conclusion | Duration | Firewall | Tokens | Turns | MCP Err | Errors |
|--------|----------|------------|----------|----------|--------|-------|---------|--------|
| 39911695776 | Rich issue triage | success | 10.8m | 21/0 | 230.7K | 1 | 0 | 0 |
| 39911687908 | Rich issue triage | success | 8.0m | 21/0 | 177.9K | 1 | 0 | 0 |
| 39911677905 | Rich issue triage | success | 10.1m | 23/0 | 194.9K | 1 | 0 | 0 |
| 39911668874 | Rich issue triage | success | 10.7m | 38/0 | 340.2K | 1 | 0 | 0 |
| 39911657500 | Rich issue triage | success | 10.0m | 28/0 | 263.7K | 1 | 0 | 0 |
| 39911649232 | Rich issue triage | success | 6.3m | 24/0 | 276.9K | 1 | 0 | 0 |
| 39911637873 | Rich issue triage | success | 7.1m | 16/0 | 187.1K | 1 | 0 | 0 |
| 39911628498 | Rich issue triage | success | 9.5m | 32/0 | 317.4K | 1 | 0 | 0 |
| 39911618382 | Rich issue triage | success | 7.7m | 28/0 | 296.5K | 1 | 0 | 0 |
| 39911607645 | Rich issue triage | success | 10.1m | 30/0 | 298.7K | 1 | 0 | 0 |
| 39911598927 | Rich issue triage | success | 6.4m | 30/0 | 340.4K | 1 | 0 | 0 |
| 39911590068 | Rich issue triage | success | 8.4m | 27/0 | 354.7K | 1 | 0 | 0 |
| 39911578649 | Rich issue triage | success | 5.9m | 30/0 | 265.1K | 1 | 0 | 0 |
| 39911569744 | Rich issue triage | success | 6.3m | 37/0 | 426.2K | 1 | 0 | 0 |
| 39911560198 | Rich issue triage | success | 5.0m | 26/0 | 208.0K | 1 | 0 | 0 |
| 39911551289 | Rich issue triage | success | 5.8m | 33/0 | 330.9K | 1 | 0 | 0 |
| 39911542702 | Rich issue triage | success | 5.5m | 29/0 | 272.7K | 1 | 0 | 0 |
| 39911532377 | Rich issue triage | success | 4.9m | 20/0 | 157.3K | 1 | 0 | 0 |
| 39911523112 | Rich issue triage | success | 4.5m | 21/0 | 176.1K | 1 | 0 | 0 |
| 39911515194 | Rich issue triage | success | 10.1m | 20/0 | 236.1K | 1 | 0 | 0 |
| 39910044209 | Rich issue triage | success | 5.1m | 28/0 | 273.2K | 1 | 0 | 0 |

