# Audit Report — Cross-Run Analysis

## Executive Summary

| Metric | Value |
|--------|-------|
| Runs analyzed | 30 |
| Runs with firewall data | 30 |
| Runs without firewall data | 0 |
| Total requests | 870 |
| Allowed requests | 870 |
| Blocked requests | 0 |
| Overall denial rate | 0.0% |
| Unique domains | 1 |

## Metrics Trends

| Metric | Total | Avg/run | Min | Max | Spikes |
|--------|-------|---------|-----|-----|--------|
| Token Trend | 8750991 | 291699 | 79842 | 708993 | ⚠ #40055609283, #40055595696 |
| Turns | 30 | 1.0 | — | 1 | — |
| Duration | — | 8.6m | 4.2m | 12.8m | — |

## MCP Server Health (30 runs)

| Server | Connected | Error Rate | Total Calls | Errors | Status |
|--------|-----------|------------|-------------|--------|--------|
| `safeoutputs` | 30/30 | 0.0% | 45 | 0 | ✅ ok |

## Domain Inventory

| Domain | Status | Seen In | Allowed | Blocked |
|--------|--------|---------|---------|--------|
| `api.openai.com:443` | ✅ allowed | 30/30 runs | 870 | 0 |

## Agent Event Pattern Analysis

| Severity | Category | Title | Summary |
|----------|----------|-------|--------|
| ℹ info | execution | Cross-run log template patterns | Mined 2 distinct event templates across 6 pipeline stages from 60 events in 30 runs. (finish=1 plan=1) |

## Cluster Patterns

| Severity | Kind | Title | Description |
|----------|------|-------|-------------|
| 🟡 low | style_skew | Dominant execution_style: exploratory | 87% of runs share execution_style="exploratory" (26/30). Low diversity may indicate homogeneous workload or classification bias. |
| 🟡 low | style_skew | Dominant resource_profile: heavy | 87% of runs share resource_profile="heavy" (26/30). Low diversity may indicate homogeneous workload or classification bias. |

## Run Clusters

| Dimension | Value | Runs | Avg Tokens | Avg Turns | Avg Duration | Success Rate |
|-----------|-------|------|------------|-----------|--------------|-------------|
| execution_style | adaptive | 4 | 96652 | 1.0 | 8.2m | 100% |
| execution_style | exploratory | 26 | 321707 | 1.0 | 8.7m | 100% |
| resource_profile | heavy | 26 | 321707 | 1.0 | 8.7m | 100% |
| resource_profile | moderate | 4 | 96652 | 1.0 | 8.2m | 100% |

## Per-Run Breakdown

| Run ID | Workflow | Conclusion | Duration | Firewall | Tokens | Turns | MCP Err | Errors |
|--------|----------|------------|----------|----------|--------|-------|---------|--------|
| 40055714887 | Rich issue triage | success | 12.4m | 27/0 | 249.1K | 1 | 0 | 0 |
| 40055707611 | Rich issue triage | success | 12.8m | 39/0 | 395.0K | 1 | 0 | 0 |
| 40055702078 | Rich issue triage | success | 12.1m | 27/0 | 224.3K | 1 | 0 | 0 |
| 40055694595 | Rich issue triage | success | 10.8m | 14/0 | 96.2K | 1 | 0 | 0 |
| 40055688691 | Rich issue triage | success | 11.5m | 11/0 | 80.1K | 1 | 0 | 0 |
| 40055681924 | Rich issue triage | success | 12.0m | 30/0 | 256.8K | 1 | 0 | 0 |
| 40055676238 | Rich issue triage | success | 9.7m | 37/0 | 395.0K | 1 | 0 | 0 |
| 40055669174 | Rich issue triage | success | 10.2m | 28/0 | 229.8K | 1 | 0 | 0 |
| 40055662746 | Rich issue triage | success | 10.8m | 35/0 | 352.4K | 1 | 0 | 0 |
| 40055655310 | Rich issue triage | success | 8.7m | 25/0 | 326.1K | 1 | 0 | 0 |
| 40055649260 | Rich issue triage | success | 10.7m | 28/0 | 254.9K | 1 | 0 | 0 |
| 40055641494 | Rich issue triage | success | 10.0m | 36/0 | 346.1K | 1 | 0 | 0 |
| 40055635434 | Rich issue triage | success | 9.7m | 36/0 | 388.9K | 1 | 0 | 0 |
| 40055629099 | Rich issue triage | success | 8.7m | 32/0 | 300.2K | 1 | 0 | 0 |
| 40055621670 | Rich issue triage | success | 7.5m | 36/0 | 350.1K | 1 | 0 | 0 |
| 40055615019 | Rich issue triage | success | 8.5m | 31/0 | 306.3K | 1 | 0 | 0 |
| 40055609283 | Rich issue triage | success | 9.7m | 42/0 | 709.0K ⚠ | 1 | 0 | 0 |
| 40055601909 | Rich issue triage | success | 7.3m | 37/0 | 356.9K | 1 | 0 | 0 |
| 40055595696 | Rich issue triage | success | 8.4m | 39/0 | 598.5K ⚠ | 1 | 0 | 0 |
| 40055588857 | Rich issue triage | success | 5.5m | 22/0 | 175.0K | 1 | 0 | 0 |
| 40055582392 | Rich issue triage | success | 6.2m | 20/0 | 219.9K | 1 | 0 | 0 |
| 40055576178 | Rich issue triage | success | 8.4m | 34/0 | 317.7K | 1 | 0 | 0 |
| 40055568828 | Rich issue triage | success | 6.7m | 29/0 | 247.2K | 1 | 0 | 0 |
| 40055563199 | Rich issue triage | success | 6.2m | 20/0 | 165.7K | 1 | 0 | 0 |
| 40055555847 | Rich issue triage | success | 7.6m | 38/0 | 377.6K | 1 | 0 | 0 |
| 40054887851 | Rich issue triage | success | 5.2m | 29/0 | 315.1K | 1 | 0 | 0 |
| 39930821237 | Rich issue triage | success | 4.2m | 16/0 | 130.4K | 1 | 0 | 0 |
| 39930813402 | Rich issue triage | success | 6.3m | 32/0 | 279.1K | 1 | 0 | 0 |
| 39930799732 | Rich issue triage | success | 4.7m | 28/0 | 228.1K | 1 | 0 | 0 |
| 39930787211 | Rich issue triage | success | 6.2m | 12/0 | 79.8K | 1 | 0 | 0 |

