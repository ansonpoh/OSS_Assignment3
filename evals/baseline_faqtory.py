#!/usr/bin/env python3
"""Run the upstream conventional-automation baseline (FAQtory, as used by
.github/workflows/newissue.yml) on every golden case and save its output.

FAQtory sees only the issue title, exactly as in the upstream workflow.

  pip install FAQtory==<version>   # see evals/golden/README.md
  python evals/baseline_faqtory.py
"""
import glob
import os
import subprocess

ROOT = os.path.join(os.path.dirname(__file__), "golden")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import json

for d in sorted(glob.glob(os.path.join(ROOT, "cases", "*"))) + sorted(
    glob.glob(os.path.join(ROOT, "adversarial", "*"))
):
    title = json.load(open(os.path.join(d, "input.json")))["title"]
    out = subprocess.run(
        ["faqtory", "suggest", title], cwd=REPO, capture_output=True, text=True
    ).stdout
    os.makedirs(os.path.join(d, "baseline"), exist_ok=True)
    open(os.path.join(d, "baseline", "faqtory.md"), "w").write(out)
    first = [l for l in out.splitlines() if l.startswith("- [")]
    print(
        f"{os.path.basename(d):24} {'; '.join(first) or '(generic thank-you, no FAQ match)'}"
    )
