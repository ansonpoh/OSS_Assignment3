#!/usr/bin/env python3
"""Create Rich's label set in the sandbox repository (idempotent).

  python evals/setup_sandbox.py OWNER/REPO
"""
import sys

from _gh import api

LABELS = {
    "Needs triage": "ededed",
    "bug": "d73a4a",
    "enhancement": "a2eeef",
    "question": "d876e3",
    "documentation": "0075ca",
    "duplicate": "cfd3d7",
    "invalid": "e4e669",
    "upstream": "fbca04",
    "more information needed": "c5def5",
    "wontfix": "ffffff",
    "accepted": "0e8a16",
    "good first issue": "7057ff",
    "help wanted": "008672",
    "Can't reproduce": "f9d0c4",
    "awaiting response": "bfdadc",
    "no work required": "c2e0c6",
}


def main():
    repo = sys.argv[1]
    existing = {
        l["name"] for l in api(f"repos/{repo}/labels?per_page=100", paginate=True)
    }
    for name, color in LABELS.items():
        if name not in existing:
            api(f"repos/{repo}/labels", "POST", {"name": name, "color": color})
            print("created", name)
    print("labels ready")


if __name__ == "__main__":
    main()
