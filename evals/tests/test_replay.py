"""Replayed issues must not notify the real upstream users they mention."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from replay import defuse  # noqa: E402


def test_defuse_mentions_outside_code():
    out = defuse("cc @willmcgugan\n```python\n@dataclass\nclass A: ...\n```\nthanks @bob")
    assert "@willmcgugan" not in out and "@bob" not in out
    assert "@dataclass" in out


def test_defuse_leaves_emails_and_paths():
    text = "mail a@b.com or see docs/@types"
    assert defuse(text) == text
