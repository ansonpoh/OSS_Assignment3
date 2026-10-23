"""Minimal GitHub API access through the gh CLI (uses the caller's auth)."""
import json
import subprocess


def api(path, method="GET", fields=None, paginate=False):
    cmd = ["gh", "api", "-X", method, path, "-H", "Accept: application/vnd.github+json"]
    if paginate:
        cmd += ["--paginate", "--slurp"]
    inp = None
    if fields is not None:
        cmd += ["--input", "-"]
        inp = json.dumps(fields)
    out = subprocess.run(cmd, input=inp, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(
            f"gh api {method} {path} failed: {out.stderr.strip() or out.stdout.strip()}"
        )
    text = out.stdout.strip()
    if not text:
        return None
    data = json.loads(text)
    if paginate:  # --slurp wraps the pages in an outer list
        data = [item for page in data for item in page]
    return data
