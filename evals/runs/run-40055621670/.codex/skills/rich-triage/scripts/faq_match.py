#!/usr/bin/env python3
"""Match the issue (title AND body) against Rich's FAQ entries in questions/.

Unlike the upstream FAQtory bot, which matches the title only, this uses the
full text, and reports a score so the agent can ignore weak matches.

  python faq_match.py ISSUE_JSON [--questions questions/] [--top 3]
"""
import argparse
import glob
import os
import re

from _common import emit, load_issue, tfidf_rank, trace

THRESHOLD = 0.25
FAQ_URL = "https://github.com/Textualize/rich/blob/master/FAQ.md#"


def parse(path):
    text = open(path).read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    head, body = (m.group(1), m.group(2)) if m else ("", text)
    title = re.search(r'title:\s*"?(.*?)"?\s*$', head, re.M)
    alts = re.findall(r'^\s*-\s*"?(.*?)"?\s*$', head, re.M)
    title = title.group(1) if title else os.path.basename(path)
    anchor = re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")
    return title, " ".join([title] * 2 + alts + [body]), anchor


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("issue")
    ap.add_argument("--questions", default="questions")
    ap.add_argument("--top", type=int, default=3)
    a = ap.parse_args()
    issue = load_issue(a.issue)
    entries = {
        p: parse(p)
        for p in sorted(glob.glob(os.path.join(a.questions, "*.question.md")))
    }
    ranked = tfidf_rank(
        f"{issue['title']} {issue['body']}",
        [(p, e[1]) for p, e in entries.items()],
        a.top,
    )
    out = [
        {
            "title": entries[p][0],
            "url": FAQ_URL + entries[p][2],
            "score": s,
            "strong": s >= THRESHOLD,
        }
        for p, s in ranked
    ]
    trace("faq_match", top=[o["title"] for o in out if o["strong"]])
    emit({"threshold": THRESHOLD, "matches": out})


if __name__ == "__main__":
    main()
