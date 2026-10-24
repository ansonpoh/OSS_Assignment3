#!/usr/bin/env python3
"""Check whether the functions and classes an issue calls by name exist in Rich.

Collects names written as calls, `name()` or `obj.name()`, in the title and the
prose of the body (code blocks are skipped: they often call the reporter's own
helpers; Python builtins are ignored), then looks for `def <name>` or
`class <name>` under rich/. Reports facts only; a name in `missing` suggests
the issue is about another project.

  python check_api.py ISSUE_JSON [--src rich]
"""
import argparse
import builtins
import os
import re

from _common import emit, load_issue, trace

CALL = re.compile(r"\b([A-Za-z_][\w.]*)\([^()\n]{0,40}\)")


def names(issue):
    text = issue.get("title", "") + "\n" + (issue.get("body") or "")
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    found = []
    for m in CALL.findall(text):
        name = m.split(".")[-1]
        if len(name) > 2 and name not in found and not hasattr(builtins, name):
            found.append(name)
    return found


def definitions(src):
    defs = {}
    pattern = re.compile(r"^\s*(?:async\s+)?(?:def|class)\s+(\w+)", re.M)
    for root, _, files in os.walk(src):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path, encoding="utf-8") as fh:
                    for name in pattern.findall(fh.read()):
                        defs.setdefault(name, []).append(path)
    return defs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue")
    ap.add_argument("--src", default="rich")
    args = ap.parse_args()
    issue = load_issue(args.issue)
    defs = definitions(args.src)
    result = []
    for name in names(issue):
        where = sorted(set(defs.get(name, [])))[:3]
        result.append({"name": name, "defined_in_rich": bool(where), "where": where})
    missing = [r["name"] for r in result if not r["defined_in_rich"]]
    out = {"names": result, "missing": missing}
    trace("check_api.py", names=len(result), missing=missing)
    emit(out)


if __name__ == "__main__":
    main()
