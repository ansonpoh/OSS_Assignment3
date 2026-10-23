# Audit Report — Cross-Run Analysis

## Executive Summary

| Metric | Value |
|--------|-------|
| Runs analyzed | 6 |
| Runs with firewall data | 6 |
| Runs without firewall data | 0 |
| Total requests | 133 |
| Allowed requests | 133 |
| Blocked requests | 0 |
| Overall denial rate | 0.0% |
| Unique domains | 1 |

## Metrics Trends

| Metric | Total | Avg/run | Min | Max | Spikes |
|--------|-------|---------|-----|-----|--------|
| Token Trend | 1102500 | 183750 | 79495 | 305546 | — |
| Turns | 6 | 1.0 | — | 1 | — |
| Duration | — | 5.4m | 4.2m | 7.0m | — |

## MCP Server Health (6 runs)

| Server | Connected | Error Rate | Total Calls | Errors | Status |
|--------|-----------|------------|-------------|--------|--------|
| `safeoutputs` | 6/6 | 0.0% | 8 | 0 | ✅ ok |

## Domain Inventory

| Domain | Status | Seen In | Allowed | Blocked |
|--------|--------|---------|---------|--------|
| `api.openai.com:443` | ✅ allowed | 6/6 runs | 133 | 0 |

## Agent Event Pattern Analysis

| Severity | Category | Title | Summary |
|----------|----------|-------|--------|
| ℹ info | execution | Cross-run log template patterns | Mined 2 distinct event templates across 6 pipeline stages from 12 events in 6 runs. (finish=1 plan=1) |

## Run Clusters

| Dimension | Value | Runs | Avg Tokens | Avg Turns | Avg Duration | Success Rate |
|-----------|-------|------|------------|-----------|--------------|-------------|
| execution_style | adaptive | 3 | 96588 | 1.0 | 4.8m | 100% |
| execution_style | exploratory | 3 | 270912 | 1.0 | 6.0m | 100% |
| resource_profile | heavy | 3 | 270912 | 1.0 | 6.0m | 100% |
| resource_profile | moderate | 3 | 96588 | 1.0 | 4.8m | 100% |

## Per-Run Breakdown

| Run ID | Workflow | Conclusion | Duration | Firewall | Tokens | Turns | MCP Err | Errors |
|--------|----------|------------|----------|----------|--------|-------|---------|--------|
| 39930821237 | Rich issue triage | success | 4.2m | 16/0 | 130.4K | 1 | 0 | 0 |
| 39930813402 | Rich issue triage | success | 6.3m | 32/0 | 279.1K | 1 | 0 | 0 |
| 39930799732 | Rich issue triage | success | 4.7m | 28/0 | 228.1K | 1 | 0 | 0 |
| 39930787211 | Rich issue triage | success | 6.2m | 12/0 | 79.8K | 1 | 0 | 0 |
| 39930776447 | Rich issue triage | success | 4.2m | 12/0 | 79.5K | 1 | 0 | 0 |
| 39930766480 | Rich issue triage | success | 7.0m | 33/0 | 305.5K | 1 | 0 | 0 |

