"""Merge a unified diff into a source tree by CHANGED SECTIONS, never by whole-file overwrite.

Each hunk's old block (context + removed lines) must occur EXACTLY ONCE in the target file's current text; it is
replaced by the hunk's new block (context + added lines). Line numbers in the diff are ignored, so sections edited
elsewhere by another author do not matter. Any hunk with zero or several matches aborts before any file is written.
The first path component after `---`/`+++` (e.g. `root-a5/`, `amended/`) is stripped.
Usage: apply_hunks.py DIFF SOURCE_ROOT
"""
import hashlib
import json
import sys
from pathlib import Path

diff_path, root = Path(sys.argv[1]), Path(sys.argv[2])
lines = diff_path.read_text().splitlines(keepends=True)
files, current, hunk = {}, None, None
for line in lines:
    if line.startswith("--- "):
        continue
    if line.startswith("+++ "):
        rel = line[4:].strip().split("/", 1)[1]
        current = files.setdefault(rel, [])
        continue
    if line.startswith("@@"):
        hunk = {"old": [], "new": [], "header": line.strip()}
        current.append(hunk)
        continue
    if hunk is None or line.startswith("\\"):
        continue
    tag, body = line[:1], line[1:]
    if tag in (" ", "-"):
        hunk["old"].append(body)
    if tag in (" ", "+"):
        hunk["new"].append(body)
plan, problems = {}, []
for rel, hunks in files.items():
    path = root / rel
    text = path.read_text()
    before = hashlib.sha256(text.encode()).hexdigest()
    for h in hunks:
        old, new = "".join(h["old"]), "".join(h["new"])
        count = text.count(old)
        if count != 1:
            problems.append({"file": rel, "hunk": h["header"], "matches": count})
            continue
        text = text.replace(old, new, 1)
    plan[rel] = (before, text)
if problems:
    print(json.dumps({"applied": False, "problems": problems}, indent=1))
    raise SystemExit(1)
report = []
for rel, (before, text) in plan.items():
    (root / rel).write_text(text)
    report.append({"path": rel, "hunks": len(files[rel]), "beforeSha256": before,
                   "afterSha256": hashlib.sha256(text.encode()).hexdigest()})
print(json.dumps({"applied": True, "diff": str(diff_path), "diffSha256": hashlib.sha256(diff_path.read_bytes()).hexdigest(),
                  "files": report}, indent=1))
