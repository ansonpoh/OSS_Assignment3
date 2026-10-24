#!/usr/bin/env python3
"""Deterministic completeness checks on an issue report.

Reports facts only (no judgement): which template was used, whether the
template was left unfilled, whether there is a code block, whether that code
is a runnable example, a traceback, version/platform information, and the
template's own checkboxes.

  python check_report.py ISSUE_JSON
"""
import argparse
import ast
import re

from _common import emit, load_issue, trace

FEATURE_TEMPLATE_MARKERS = [
    "Give as much detail as you can. Example code of how you would like it to work would help.",
    "What problem do you have that this feature would solve? I may be able to suggest an existing way of solving it.",
]


def runnable_example(body):
    """True if a Python code block parses, imports Rich and has no `...`
    placeholders: something a maintainer could paste and run."""
    for lang, code in re.findall(r"```[ \t]*(\w*)[^\n]*\n(.*?)```", body, re.S):
        if lang.lower() not in ("", "python", "py", "python3", "pycon"):
            continue
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        imports_rich = any(
            (isinstance(n, ast.ImportFrom) and (n.module or "").split(".")[0] == "rich")
            or (
                isinstance(n, ast.Import)
                and any(a.name.split(".")[0] == "rich" for a in n.names)
            )
            for n in ast.walk(tree)
        )
        placeholder = any(
            isinstance(n, ast.Expr)
            and isinstance(n.value, ast.Constant)
            and n.value.value is Ellipsis
            for n in ast.walk(tree)
        )
        if imports_rich and not placeholder:
            return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue")
    a = ap.parse_args()
    issue = load_issue(a.issue)
    title, body = issue["title"], issue.get("body") or ""
    template = (
        "bug"
        if title.startswith("[BUG]") or "Describe the bug" in body
        else "feature"
        if title.startswith("[REQUEST]") or "How would you improve Rich?" in body
        else "none"
    )
    stripped = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    facts = {
        "template": template,
        "body_chars": len(stripped.strip()),
        "has_code_block": "```" in stripped,
        "runnable_example": runnable_example(stripped),
        "has_traceback": "Traceback (most recent call last)" in stripped,
        "mentions_rich_version": bool(
            re.search(
                r"rich[ =:v]*\d+\.\d+|python -m rich.diagnose|\brich\s*==",
                stripped,
                re.I,
            )
        ),
        "mentions_platform": bool(
            re.search(
                r"\b(windows|linux|macos|mac os|ubuntu|debian|wsl|jupyter|vs ?code)\b",
                stripped,
                re.I,
            )
        ),
        "checkboxes_ticked": len(re.findall(r"- \[x\]", stripped, re.I)),
        "checkboxes_unticked": len(re.findall(r"- \[ \]", stripped)),
        "feature_template_unfilled": template == "feature"
        and all(m in stripped for m in FEATURE_TEMPLATE_MARKERS),
        "has_hidden_html_comment": "<!--" in body
        and bool(re.search(r"<!--(?!\s*\nWAIT!).*?-->", body, re.S)),
        "links": re.findall(r"https?://[^\s)>\]]+", stripped)[:10],
    }
    trace("check_report", template=template)
    emit(facts)


if __name__ == "__main__":
    main()
