#!/usr/bin/env python3
"""Replay golden cases as new issues in the sandbox so the triage workflow runs.

Each issue body gets a hidden marker with the case id, original filing time and
original author role. The workflow honours the marker only for OWNER-authored
issues: it strips it, restores the author role, and hides later issues (and
later closes) from duplicate search. Template labels present at filing
(e.g. "Needs triage") are applied at creation, as the template would.
@mentions outside code are defused (a zero-width space after the @) so
replays never notify the real upstream users named in the original issues.

  python evals/replay.py OWNER/REPO [case ...]      # default: all cases
Writes evals/golden/replay_map.json  {case_id: sandbox_issue_number}.
"""
import glob
import json
import os
import re
import sys
import time

from _gh import api

ROOT = os.path.join(os.path.dirname(__file__), "golden")
MAP = os.path.join(ROOT, "replay_map.json")
MENTION = re.compile(r"(?<![\w`/])@(?=[A-Za-z0-9])")


def defuse(text):
    # GitHub does not notify from fenced code, so leave code (decorators) as is.
    parts = (text or "").split("```")
    return "```".join(p if i % 2 else MENTION.sub("@\u200b", p) for i, p in enumerate(parts))


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
        body = defuse(inp["body"]) + (
            f"\n\n<!-- golden-case: {cid} filed: {inp['created_at']}"
            f" as: {inp.get('author_association') or 'NONE'} -->"
        )
        issue = api(
            f"repos/{repo}/issues",
            "POST",
            {"title": defuse(inp["title"]), "body": body, "labels": inp.get("labels", [])},
        )
        mapping[cid] = issue["number"]
        json.dump(mapping, open(MAP, "w"), indent=2, sort_keys=True)
        print(f"{cid} -> #{issue['number']}")
        time.sleep(5)  # spread triggers; runs queue anyway (concurrency queue: max)


if __name__ == "__main__":
    main()
