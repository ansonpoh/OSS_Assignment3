#!/usr/bin/env python3
"""Keep a scored run: copy results.md and every case's actual/actual.json into
evals/golden/runs/LABEL/ (each case's actual/ folder holds only the latest run).

  python evals/snapshot.py LABEL
"""
import glob
import os
import shutil
import sys

ROOT = os.path.join(os.path.dirname(__file__), "golden")


def main():
    out = os.path.join(ROOT, "runs", sys.argv[1])
    os.makedirs(out, exist_ok=True)
    shutil.copy(os.path.join(ROOT, "results.md"), out)
    for path in glob.glob(os.path.join(ROOT, "*", "*", "actual", "actual.json")):
        case = path.split(os.sep)[-3]
        shutil.copy(path, os.path.join(out, f"{case}.json"))
    print("saved", out)


if __name__ == "__main__":
    main()
