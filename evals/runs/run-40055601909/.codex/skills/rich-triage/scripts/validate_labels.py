#!/usr/bin/env python3
"""Validate a proposed label set before the agent emits add_labels.

Exit 0 and print {"ok": true} when valid; exit 1 with reasons otherwise.
The same allowlist is enforced again by safe-outputs in the workflow; this
check lets the agent correct itself instead of having labels silently dropped.

  python validate_labels.py bug "more information needed"
"""
import sys

from _common import emit, trace

ALLOWED = {
    "bug",
    "enhancement",
    "question",
    "documentation",
    "duplicate",
    "invalid",
    "upstream",
    "more information needed",
}
TYPE_LABELS = {"bug", "enhancement", "question", "documentation", "invalid"}
MAX_LABELS = 3


def validate(labels):
    errors = []
    for l in labels:
        if l not in ALLOWED:
            errors.append(f"'{l}' is not in the allowlist {sorted(ALLOWED)}")
    if len(labels) > MAX_LABELS:
        errors.append(f"{len(labels)} labels proposed; maximum is {MAX_LABELS}")
    types = [l for l in labels if l in TYPE_LABELS]
    if len(types) > 1:
        errors.append(f"pick one type label, got {types}")
    if "invalid" in labels and len(labels) > 1:
        errors.append("'invalid' must be the only label")
    if "duplicate" in labels and "more information needed" in labels:
        errors.append("'duplicate' and 'more information needed' are contradictory")
    return errors


def main():
    labels = sys.argv[1:]
    errors = validate(labels)
    trace("validate_labels", labels=labels, ok=not errors)
    emit({"ok": not errors, "labels": labels, "errors": errors})
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
