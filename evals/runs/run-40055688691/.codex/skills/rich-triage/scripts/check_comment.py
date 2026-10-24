#!/usr/bin/env python3
"""Check a draft triage comment before the agent emits add_comment.

Checks only facts that code can decide:
- links point to github.com/Textualize/rich files that exist, on `master`,
  and never to an issue, PR or discussion by URL (use #NNNN instead);
- Python code blocks parse;
- styles and colours in code (style=..., Style.parse, Color.parse, and
  markup tags such as "[bold red]") are valid in this version of Rich;
- `from rich.x import Name` names exist in this repository's source;
- the comment ends with the required footer.

Exit 0 and print {"ok": true} when clean; exit 1 with the problems otherwise.

  python check_comment.py COMMENT_FILE      # or '-' to read stdin
"""
import ast
import os
import re
import sys

from _common import emit, trace

ROOT = os.getcwd()
FOOTER = "<sub>Automated first-response triage (rich-triage skill). A maintainer will review.</sub>"
REPO_URL = "https://github.com/Textualize/rich/"
STYLE_CALLS = {"parse"}  # Style.parse, Color.parse


def rich_parsers():
    """Rich's own parsers from this checkout (standard library only)."""
    sys.path.insert(0, ROOT)
    from rich.color import Color
    from rich.style import Style

    return Style.parse, Color.parse


def check_links(text, problems):
    for target in re.findall(r"\]\(([^)\s]+)\)", text):
        if not target.startswith("https://"):
            problems.append(
                f"relative link '{target}' does not resolve in an issue comment; use {REPO_URL}blob/master/<path>"
            )
    for url in re.findall(r"https?://[^\s)>\]`]+", text):
        if not url.startswith(REPO_URL):
            problems.append(f"link '{url}' is outside {REPO_URL}")
            continue
        rest = url[len(REPO_URL) :]
        if re.match(r"(issues|pull|discussions)/\d+", rest):
            problems.append(
                f"'{url}' links an issue, PR or discussion by URL; write #NNNN instead"
            )
        m = re.match(r"(blob|tree)/([^/]+)/([^#?]+)", rest)
        if m:
            if m.group(2) != "master":
                problems.append(
                    f"'{url}' uses branch '{m.group(2)}'; Rich's branch is 'master'"
                )
            if not os.path.exists(os.path.join(ROOT, m.group(3))):
                problems.append(
                    f"'{url}' points to '{m.group(3)}', which does not exist in this repository"
                )


def check_import(node, problems):
    """`from rich.x import Name`: the module file must exist and define Name."""
    if not (
        isinstance(node, ast.ImportFrom)
        and node.module
        and node.module.split(".")[0] == "rich"
    ):
        return
    path = os.path.join(ROOT, *node.module.split("."))
    path = (
        path + ".py"
        if os.path.exists(path + ".py")
        else os.path.join(path, "__init__.py")
    )
    if not os.path.exists(path):
        problems.append(f"module '{node.module}' does not exist in Rich")
        return
    source = open(path, encoding="utf-8").read()
    for alias in node.names:
        if alias.name != "*" and not re.search(
            rf"^\s*(def|class)\s+{alias.name}\b|^\s*{alias.name}\s*[:=]|import .*\b{alias.name}\b",
            source,
            re.M,
        ):
            problems.append(f"'{alias.name}' is not defined in {node.module}")


def check_code(text, problems):
    style_parse, color_parse = rich_parsers()
    for lang, code in re.findall(r"```[ \t]*(\w*)[^\n]*\n(.*?)```", text, re.S):
        if lang.lower() not in ("", "python", "py", "python3"):
            continue
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            problems.append(f"code block does not parse: {e.msg} (line {e.lineno})")
            continue
        for node in ast.walk(tree):
            check_import(node, problems)
            styles = []
            if isinstance(node, ast.keyword) and node.arg in (
                "style",
                "border_style",
                "title_style",
            ):
                styles.append((style_parse, node.value))
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in STYLE_CALLS
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id in ("Style", "Color")
                and node.args
            ):
                styles.append(
                    (
                        style_parse if node.func.value.id == "Style" else color_parse,
                        node.args[0],
                    )
                )
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                for tag in re.findall(r"\[([a-z][a-z0-9_ #(),.]*)\]", node.value):
                    if not tag.startswith(("link", "/")):
                        styles.append((style_parse, ast.Constant(tag)))
            for parse, value in styles:
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    try:
                        parse(value.value)
                    except Exception as e:  # StyleSyntaxError, ColorParseError
                        problems.append(f"invalid style or colour '{value.value}': {e}")
    # Inline code such as `style="orange"` outside a code block.
    for snippet in re.findall(
        r"`([^`\n]*style\s*=\s*[\"'][^\"']+[\"'][^`\n]*)`",
        re.sub(r"```.*?```", "", text, flags=re.S),
    ):
        for value in re.findall(r"style\s*=\s*[\"']([^\"']+)[\"']", snippet):
            try:
                style_parse(value)
            except Exception as e:
                problems.append(f"invalid style or colour '{value}': {e}")


def check(text):
    problems = []
    check_links(text, problems)
    check_code(text, problems)
    if not text.rstrip().endswith(FOOTER):
        problems.append("comment must end with the footer line from SKILL.md")
    return problems


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    problems = check(text)
    trace("check_comment", ok=not problems, problems=len(problems))
    emit({"ok": not problems, "problems": problems})
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
