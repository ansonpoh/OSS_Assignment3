#!/usr/bin/env python3
"""Rank earlier issues by textual similarity to the new issue.

Only issues created strictly before the new issue's `created_at` are searched,
so a replayed historical case never sees the future.

  python find_duplicates.py ISSUE_JSON INDEX_JSON [--top 5]
"""
import argparse

from _common import emit, load_issue, tfidf_rank, trace

THRESHOLD = 0.35  # below this, candidates are reported but flagged weak


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue")
    ap.add_argument("index")
    ap.add_argument("--top", type=int, default=5)
    a = ap.parse_args()
    issue = load_issue(a.issue)
    index = load_issue(a.index)
    before = [
        r
        for r in index
        if r["created_at"] < issue["created_at"] and r["number"] != issue.get("number")
    ]
    docs = [(r["number"], f"{r['title']} {r['title']} {r['body']}") for r in before]
    ranked = tfidf_rank(
        f"{issue['title']} {issue['title']} {issue['body']}", docs, a.top
    )
    by_num = {r["number"]: r for r in before}
    out = [
        {
            "number": n,
            "score": s,
            "title": by_num[n]["title"],
            "state": "closed" if by_num[n]["closed_at"] else "open",
            "state_reason": by_num[n]["state_reason"],
            "strong": s >= THRESHOLD,
        }
        for n, s in ranked
    ]
    trace("find_duplicates", searched=len(before), top=[o["number"] for o in out])
    emit({"searched_issues": len(before), "threshold": THRESHOLD, "candidates": out})


if __name__ == "__main__":
    main()
