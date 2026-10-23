#!/usr/bin/env python3
"""Snapshot historical issues as golden-case inputs, separated from their outcomes.

For each issue number this writes:
  evals/golden/cases/<n>/input.json      what was knowable when the issue was filed
                                         (title, body, author association, labels
                                         applied within 2 minutes of creation)
  evals/golden/cases/<n>/evidence.json   what happened later (maintainer comments,
                                         label/close events, final state). Never
                                         shown to the agent; used only to justify
                                         the expected outcome.

With --index it also writes data/issues_index.json: every issue in the repository
(number, title, created_at, closed_at, state_reason, first 2000 body chars). The
duplicate-search script filters this by created_at so a case never sees issues
filed after it.

Usage:
  GITHUB_TOKEN=... python collect_cases.py --repo Textualize/rich --issues 3917,4205 \
      --out evals/golden/cases --index data/issues_index.json
"""
import argparse
import json
import os
from datetime import timedelta

from triage_metrics import API, MAINTAINER_ROLES, get, is_bot, ts

BODY_CHARS = 2000


def snapshot(repo, number, token):
    issue = next(get(f"{API}/repos/{repo}/issues/{number}", token))
    created = ts(issue["created_at"])
    events = list(get(f"{API}/repos/{repo}/issues/{number}/events?per_page=100", token))
    comments = list(
        get(f"{API}/repos/{repo}/issues/{number}/comments?per_page=100", token)
    )
    # Labels present at filing time = labels added within 2 minutes of creation
    # (issue templates apply them immediately).
    initial = sorted(
        {
            e["label"]["name"]
            for e in events
            if e["event"] == "labeled"
            and ts(e["created_at"]) - created < timedelta(minutes=2)
        }
    )
    inp = {
        "repo": repo,
        "number": issue["number"],
        "title": issue["title"],
        "body": issue["body"] or "",
        "author": issue["user"]["login"],
        "author_association": issue.get("author_association"),
        "created_at": issue["created_at"],
        "labels": initial,
        "source_url": issue["html_url"],
    }
    evidence = {
        "final_state": issue["state"],
        "state_reason": issue.get("state_reason"),
        "closed_at": issue.get("closed_at"),
        "final_labels": [l["name"] for l in issue["labels"]],
        "events": [
            {
                "event": e["event"],
                "actor": (e.get("actor") or {}).get("login"),
                "label": (e.get("label") or {}).get("name"),
                "at": e["created_at"],
            }
            for e in events
            if e["event"]
            in (
                "labeled",
                "unlabeled",
                "closed",
                "reopened",
                "marked_as_duplicate",
                "transferred",
                "converted_to_discussion",
                "locked",
            )
        ],
        "comments": [
            {
                "author": c["user"]["login"],
                "association": c.get("author_association"),
                "is_maintainer": c.get("author_association") in MAINTAINER_ROLES
                and not is_bot(c["user"]),
                "at": c["created_at"],
                "body": c["body"],
            }
            for c in comments
        ],
    }
    return inp, evidence


def build_index(repo, token):
    rows = []
    for i in get(
        f"{API}/repos/{repo}/issues?state=all&per_page=100&sort=created&direction=asc",
        token,
    ):
        if "pull_request" in i:
            continue
        rows.append(
            {
                "number": i["number"],
                "title": i["title"],
                "created_at": i["created_at"],
                "closed_at": i.get("closed_at"),
                "state_reason": i.get("state_reason"),
                "body": (i["body"] or "")[:BODY_CHARS],
            }
        )
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--issues", default="", help="comma-separated issue numbers")
    ap.add_argument("--out", default="evals/golden/cases")
    ap.add_argument("--index", help="also write a full issue index to this path")
    args = ap.parse_args()
    token = os.environ["GITHUB_TOKEN"]
    for n in filter(None, args.issues.split(",")):
        inp, ev = snapshot(args.repo, int(n), token)
        d = os.path.join(args.out, str(n))
        os.makedirs(d, exist_ok=True)
        json.dump(inp, open(os.path.join(d, "input.json"), "w"), indent=2)
        json.dump(ev, open(os.path.join(d, "evidence.json"), "w"), indent=2)
        print(f"case #{n}: {inp['title']}")
    if args.index:
        os.makedirs(os.path.dirname(args.index) or ".", exist_ok=True)
        rows = build_index(args.repo, token)
        json.dump(rows, open(args.index, "w"), indent=1)
        print(f"index: {len(rows)} issues")


if __name__ == "__main__":
    main()
