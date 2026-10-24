"""Tests for the rich-triage skill scripts (run from the repository root):

  python -m pytest evals/tests -q

Each script is run as the agent runs it, as a subprocess with the repository
root as working directory, and its JSON output and exit code are checked.
"""
import json
import os
import subprocess
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRIPTS = os.path.join(REPO, ".claude", "skills", "rich-triage", "scripts")
GOLDEN = os.path.join(REPO, "evals", "golden")
FOOTER = "<sub>Automated first-response triage (rich-triage skill). A maintainer will review.</sub>"


@pytest.fixture
def run(tmp_path):
    trace = tmp_path / "trace.jsonl"

    def _run(script, *args, stdin=None):
        p = subprocess.run(
            [sys.executable, os.path.join(SCRIPTS, script), *map(str, args)],
            cwd=REPO,
            input=stdin,
            capture_output=True,
            text=True,
            env={**os.environ, "RICH_TRIAGE_TRACE": str(trace)},
        )
        entries = [json.loads(l) for l in trace.read_text().splitlines()] if trace.exists() else []
        return p.returncode, json.loads(p.stdout), entries

    return _run


def issue_file(tmp_path, title, body, created="2026-09-22T00:00:00Z", number=1):
    p = tmp_path / "issue.json"
    p.write_text(json.dumps({"number": number, "title": title, "body": body, "created_at": created}))
    return p


def case_input(cid):
    for sub in ("cases", "adversarial", "heldout"):
        p = os.path.join(GOLDEN, sub, cid, "input.json")
        if os.path.exists(p):
            return p
    raise FileNotFoundError(cid)


# validate_labels.py

@pytest.mark.parametrize("labels", [["bug"], ["bug", "more information needed"], ["question", "duplicate"], ["invalid"]])
def test_valid_label_sets(run, labels):
    code, out, trace = run("validate_labels.py", *labels)
    assert code == 0 and out["ok"]
    assert trace[-1]["script"] == "validate_labels"


@pytest.mark.parametrize(
    "labels, reason",
    [
        (["wontfix"], "allowlist"),
        (["Needs triage"], "allowlist"),
        (["bug", "upstream", "duplicate", "question"], "maximum is 3"),
        (["bug", "enhancement"], "one type label"),
        (["invalid", "question"], "only label"),
        (["duplicate", "more information needed"], "contradictory"),
    ],
)
def test_invalid_label_sets(run, labels, reason):
    code, out, _ = run("validate_labels.py", *labels)
    assert code == 1 and not out["ok"]
    assert any(reason in e for e in out["errors"])


# check_api.py

def test_check_api_flags_missing_function(run):
    # Case 4226: Rich has no select(), so the issue is about another project.
    code, out, trace = run("check_api.py", case_input("4226"))
    assert code == 0
    assert "select" in out["missing"]
    assert trace[-1]["script"] == "check_api.py"


def test_check_api_finds_rich_function(run, tmp_path):
    code, out, _ = run("check_api.py", issue_file(tmp_path, "export_svg() drops the title", "Calling `console.export_svg()` loses it"))
    assert out["missing"] == []
    assert out["names"][0]["defined_in_rich"]


def test_check_api_ignores_code_blocks_and_builtins(run, tmp_path):
    body = "Using print() and len() here.\n```python\nmy_helper()\n```"
    _, out, _ = run("check_api.py", issue_file(tmp_path, "Something", body))
    assert out["names"] == []


# check_report.py

def test_check_report_runnable_example(run, tmp_path):
    body = "Describe the bug\n```python\nfrom rich import print\nprint('[bold]x')\n```\nrich==14.0.0 on Linux"
    _, out, trace = run("check_report.py", issue_file(tmp_path, "[BUG] x", body))
    assert out["template"] == "bug"
    assert out["runnable_example"] and out["mentions_rich_version"] and out["mentions_platform"]
    assert trace[-1] == {**trace[-1], "script": "check_report", "template": "bug"}


def test_check_report_placeholder_is_not_runnable(run, tmp_path):
    body = "```python\nfrom rich.console import Console\n...\n```"
    _, out, _ = run("check_report.py", issue_file(tmp_path, "[BUG] x", body))
    assert out["has_code_block"] and not out["runnable_example"]


def test_check_report_detects_hidden_comment(run):
    _, out, _ = run("check_report.py", case_input("adv-2-hidden-injection"))
    assert out["has_hidden_html_comment"]


# check_comment.py

def test_check_comment_accepts_clean_comment(run):
    text = (
        "Rich has no `select()`; is this for another project? See "
        "https://github.com/Textualize/rich/blob/master/README.md and #4089.\n\n" + FOOTER
    )
    code, out, trace = run("check_comment.py", "-", stdin=text)
    assert code == 0 and out["ok"], out
    assert trace[-1]["script"] == "check_comment"


@pytest.mark.parametrize(
    "text, reason",
    [
        ("See https://github.com/Textualize/rich/issues/4089\n\n" + FOOTER, "#NNNN"),
        ("See https://example.com/x\n\n" + FOOTER, "outside"),
        ("See https://github.com/Textualize/rich/blob/main/README.md\n\n" + FOOTER, "branch"),
        ("See https://github.com/Textualize/rich/blob/master/NOPE.md\n\n" + FOOTER, "does not exist"),
        ("```python\nprint(\n```\n\n" + FOOTER, "does not parse"),
        ('```python\nconsole.print("x", style="orange")\n```\n\n' + FOOTER, "invalid style"),
        ("```python\nfrom rich.console import NoSuchThing\n```\n\n" + FOOTER, "not defined"),
        ("No footer here.", "footer"),
    ],
)
def test_check_comment_rejects(run, text, reason):
    code, out, _ = run("check_comment.py", "-", stdin=text)
    assert code == 1 and not out["ok"]
    assert any(reason in p for p in out["problems"]), out["problems"]


# find_duplicates.py and faq_match.py

def test_find_duplicates_never_sees_later_issues(run, tmp_path):
    index = tmp_path / "index.json"
    index.write_text(json.dumps([
        {"number": 10, "title": "Table column ellipsis", "body": "ellipsize last column", "created_at": "2026-01-01T00:00:00Z", "closed_at": None, "state_reason": None},
        {"number": 30, "title": "Table column ellipsis", "body": "ellipsize last column", "created_at": "2026-12-01T00:00:00Z", "closed_at": None, "state_reason": None},
    ]))
    issue = issue_file(tmp_path, "Ellipsize last column in a table", "table column ellipsis", created="2026-06-01T00:00:00Z", number=20)
    _, out, trace = run("find_duplicates.py", issue, index)
    assert out["searched_issues"] == 1
    assert [c["number"] for c in out["candidates"]] == [10]
    assert trace[-1]["script"] == "find_duplicates"


def test_faq_match_reports_scores(run, tmp_path):
    _, out, trace = run("faq_match.py", issue_file(tmp_path, "Strange colors in console output", "colors look wrong in my terminal"))
    assert out["matches"] and out["matches"][0]["strong"]
    assert out["matches"][0]["url"].startswith("https://github.com/Textualize/rich/blob/master/FAQ.md#")
    assert trace[-1]["script"] == "faq_match"
