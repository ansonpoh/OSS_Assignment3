#!/usr/bin/env python3
"""Measure issue-triage need for a GitHub repository.

For every issue (not PR) opened in [--since, --until) this records:
  - hours to first response by a maintainer (OWNER/MEMBER/COLLABORATOR,
    excluding the issue author and bots)
  - hours until "Needs triage" was removed, if it ever was
  - final state, state_reason and labels (used to pick golden cases)

Outputs per-issue CSV and a summary JSON. Uses only the standard library.

Usage:
  GITHUB_TOKEN=... python triage_metrics.py --repo Textualize/rich \
      --since 2025-10-01 --until 2026-10-01 --out evals/metrics
"""
import argparse
import csv
import json
import os
import statistics
import sys
import time
import urllib.request
from datetime import datetime, timezone

API = "https://api.github.com"
MAINTAINER_ROLES = {"OWNER", "MEMBER", "COLLABORATOR"}
TRIAGE_LABEL = "Needs triage"


def get(url, token):
    """GET with pagination; yields JSON items (or one object)."""
    while url:
        req = urllib.request.Request(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req) as resp:
                    body = json.load(resp)
                    link = resp.headers.get("Link", "")
                break
            except urllib.error.HTTPError as e:
                if e.code in (403, 429, 502, 503) and attempt < 3:
                    time.sleep(2 ** (attempt + 2))
                    continue
                raise
        if isinstance(body, list):
            yield from body
        else:
            yield body
            return
        url = None
        for part in link.split(","):
            if 'rel="next"' in part:
                url = part[part.index("<") + 1 : part.index(">")]


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def hours(a, b):
    return round((b - a).total_seconds() / 3600, 1)


def is_bot(user):
    return user is None or user.get("type") == "Bot" or user["login"].endswith("[bot]")


def analyse_issue(repo, issue, token):
    created = ts(issue["created_at"])
    author = issue["user"]["login"]
    first_resp = None
    for c in get(
        f"{API}/repos/{repo}/issues/{issue['number']}/comments?per_page=100", token
    ):
        if is_bot(c["user"]) or c["user"]["login"] == author:
            continue
        if c.get("author_association") in MAINTAINER_ROLES:
            first_resp = ts(c["created_at"])
            break
    triage_removed = None
    first_label_by_human = None
    closed_by_maintainer = None
    for ev in get(
        f"{API}/repos/{repo}/issues/{issue['number']}/events?per_page=100", token
    ):
        actor = ev.get("actor")
        if (
            ev["event"] == "unlabeled"
            and ev["label"]["name"] == TRIAGE_LABEL
            and triage_removed is None
        ):
            triage_removed = ts(ev["created_at"])
        if (
            ev["event"] == "labeled"
            and not is_bot(actor)
            and actor["login"] != author
            and ev["label"]["name"] != TRIAGE_LABEL
            and first_label_by_human is None
        ):
            first_label_by_human = ts(ev["created_at"])
        if (
            ev["event"] == "closed"
            and not is_bot(actor)
            and actor["login"] != author
            and closed_by_maintainer is None
        ):
            closed_by_maintainer = ts(ev["created_at"])
    # A maintainer label or close counts as a response even without a comment.
    candidates = [
        t for t in (first_resp, first_label_by_human, closed_by_maintainer) if t
    ]
    first_action = min(candidates) if candidates else None
    labels = [l["name"] for l in issue["labels"]]
    return {
        "number": issue["number"],
        "title": issue["title"],
        "created_at": issue["created_at"],
        "author_association": issue.get("author_association"),
        "state": issue["state"],
        "state_reason": issue.get("state_reason") or "",
        "labels": "|".join(labels),
        "still_needs_triage": TRIAGE_LABEL in labels,
        "comments": issue["comments"],
        "hours_to_first_maintainer_comment": hours(created, first_resp)
        if first_resp
        else "",
        "hours_to_first_maintainer_action": hours(created, first_action)
        if first_action
        else "",
        "hours_to_triage_label_removed": hours(created, triage_removed)
        if triage_removed
        else "",
        "url": issue["html_url"],
    }


def pct(values, q):
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(values) - 1)
    return round(values[lo] + (values[hi] - values[lo]) * (k - lo), 1)


def summarise(rows, since, until, measured_at):
    n = len(rows)
    resp = [
        r["hours_to_first_maintainer_action"]
        for r in rows
        if r["hours_to_first_maintainer_action"] != ""
    ]
    comm = [
        r["hours_to_first_maintainer_comment"]
        for r in rows
        if r["hours_to_first_maintainer_comment"] != ""
    ]
    age_cut = 30 * 24
    old = [
        r
        for r in rows
        if (measured_at - ts(r["created_at"])).total_seconds() / 3600 >= age_cut
    ]
    reasons = {}
    for r in rows:
        key = (
            r["state"]
            if r["state"] == "open"
            else f"closed:{r['state_reason'] or 'unknown'}"
        )
        reasons[key] = reasons.get(key, 0) + 1
    label_counts = {}
    for r in rows:
        for l in filter(None, r["labels"].split("|")):
            label_counts[l] = label_counts.get(l, 0) + 1
    return {
        "window": {"since": since, "until": until},
        "measured_at": measured_at.isoformat(),
        "issues_opened": n,
        "issues_per_week": round(
            n / max(1, (ts(until + "T00:00:00Z") - ts(since + "T00:00:00Z")).days / 7),
            2,
        ),
        "with_any_maintainer_action": len(resp),
        "never_actioned_by_maintainer": n - len(resp),
        "never_actioned_pct": round(100 * (n - len(resp)) / n, 1) if n else None,
        "first_action_hours_median": pct(resp, 0.5),
        "first_action_hours_p90": pct(resp, 0.9),
        "first_comment_hours_median": pct(comm, 0.5),
        "first_comment_hours_p90": pct(comm, 0.9),
        "older_than_30d": len(old),
        "older_than_30d_still_needs_triage": sum(
            1 for r in old if r["still_needs_triage"] and r["state"] == "open"
        ),
        "outcomes": reasons,
        "labels": dict(sorted(label_counts.items(), key=lambda kv: -kv[1])),
        "notes": [
            "Responses count OWNER/MEMBER/COLLABORATOR comments, non-author human labels, or non-author closes.",
            "Issues still open have no response time and are counted as never actioned (right-censored).",
            "Discussions, Discord and email replies are invisible to this metric.",
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--since", required=True, help="YYYY-MM-DD inclusive")
    ap.add_argument("--until", required=True, help="YYYY-MM-DD exclusive")
    ap.add_argument("--out", default="evals/metrics")
    args = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is required")
    since, until = ts(args.since + "T00:00:00Z"), ts(args.until + "T00:00:00Z")
    rows = []
    url = f"{API}/repos/{args.repo}/issues?state=all&since={args.since}T00:00:00Z&per_page=100&sort=created&direction=asc"
    for issue in get(url, token):
        if "pull_request" in issue:
            continue
        if not (since <= ts(issue["created_at"]) < until):
            continue
        rows.append(analyse_issue(args.repo, issue, token))
        print(f"#{issue['number']}", file=sys.stderr)
    os.makedirs(args.out, exist_ok=True)
    with open(os.path.join(args.out, "issues.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["number"])
        w.writeheader()
        w.writerows(rows)
    summary = summarise(rows, args.since, args.until, datetime.now(timezone.utc))
    summary["repo"] = args.repo
    with open(os.path.join(args.out, "summary.json"), "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
