"""Shared helpers for the rich-triage skill scripts (standard library only)."""
import json
import math
import os
import re
import sys
import time
from collections import Counter

TRACE = os.environ.get("RICH_TRIAGE_TRACE", "/tmp/gh-aw/agent/skill-trace.jsonl")
STOP = set(
    """a an and are as at be but by can do does for from has have how i if in is it its
me my not of on or so that the this to was were what when which with you your rich please
would should could bug issue request feature using use used get""".split()
)


def trace(script, **fields):
    """Append one line per script run. The workflow uploads this file as
    evidence that the agent actually used the skill."""
    try:
        os.makedirs(os.path.dirname(TRACE), exist_ok=True)
        with open(TRACE, "a") as f:
            f.write(
                json.dumps(
                    {
                        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "skill": "rich-triage",
                        "script": script,
                        **fields,
                    }
                )
                + "\n"
            )
    except OSError:
        pass


def tokens(text):
    text = re.sub(
        r"```.*?```", " ", text or "", flags=re.S
    )  # code blocks dominate otherwise
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_]+", text.lower())
    return [w for w in words if w not in STOP and len(w) > 2]


def tfidf_rank(query, docs, top=5):
    """docs: list of (key, text). Returns [(key, score)] by cosine similarity."""
    tok_docs = [(k, Counter(tokens(t))) for k, t in docs]
    df = Counter()
    for _, c in tok_docs:
        df.update(c.keys())
    n = len(tok_docs) or 1
    idf = {w: math.log((n + 1) / (d + 1)) + 1 for w, d in df.items()}

    def vec(c):
        v = {w: tf * idf.get(w, math.log(n + 1) + 1) for w, tf in c.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1
        return {w: x / norm for w, x in v.items()}

    q = vec(Counter(tokens(query)))
    scored = []
    for k, c in tok_docs:
        d = vec(c)
        scored.append((k, round(sum(q[w] * d.get(w, 0) for w in q), 3)))
    scored.sort(key=lambda kv: -kv[1])
    return scored[:top]


def load_issue(path):
    with open(path) as f:
        return json.load(f)


def emit(obj):
    json.dump(obj, sys.stdout, indent=2)
    sys.stdout.write("\n")
