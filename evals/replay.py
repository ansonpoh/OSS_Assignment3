#!/usr/bin/env python3
"""Replay golden cases as new issues in the sandbox so the triage workflow runs.

Each issue body gets a hidden marker with the case id, original filing time and
original author role. The workflow honours the marker only for OWNER-authored
issues: it strips it, restores the author role, and hides later issues (and
later closes) from duplicate search. Template labels present at filing
(e.g. "Needs triage") are applied at creation, as the template would.

  python evals/replay.py OWNER/REPO [case ...]      # default: all cases
Writes evals/golden/replay_map.json  {case_id: sandbox_issue_number}.
"""
import glob
import json
import os
import sys
import time

from _gh import api

ROOT = os.path.join(os.path.dirname(__file__), "golden")
MAP = os.path.join(ROOT, "replay_map.json")


def case_dirs(selected):
    dirs = [
        d
        for sub in ("cases", "adversarial", "heldout")
        for d in sorted(glob.glob(os.path.join(ROOT, sub, "*")))
    ]
    return [d for d in dirs if not selected or os.path.basename(d) in selected]


def main():
    repo, selected = sys.argv[1], set(sys.argv[2:])
    mapping = json.load(open(MAP)) if os.path.exists(MAP) else {}
    for d in case_dirs(selected):
        cid = os.path.basename(d)
        inp = json.load(open(os.path.join(d, "input.json")))
        body = (inp["body"] or "") + (
            f"\n\n<!-- golden-case: {cid} filed: {inp['created_at']}"
            f" as: {inp.get('author_association') or 'NONE'} -->"
        )
        issue = api(
            f"repos/{repo}/issues",
            "POST",
            {"title": inp["title"], "body": body, "labels": inp.get("labels", [])},
        )
        mapping[cid] = issue["number"]
        json.dump(mapping, open(MAP, "w"), indent=2, sort_keys=True)
        print(f"{cid} -> #{issue['number']}")
        time.sleep(5)  # spread triggers; runs queue anyway (concurrency queue: max)


if __name__ == "__main__":
    main()
