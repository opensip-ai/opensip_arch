#!/usr/bin/env python
"""Executable-line delta v16 -> v17 for the changed model/checker sources.

Comments and docstrings are stripped by TOKENIZING the source, so a wording
change cannot masquerade as a behaviour change and vice versa. For each file I
report the added and removed EXECUTABLE lines, and classify additions as
refusal-adding (a new raise/refuse/fault/check) or not.

The systemic question this answers: did any change WEAKEN an admission?
"""
import difflib
import io
import json
import os
import sys
import tokenize

V16 = "/tmp/opensip-design-corrections/post-reset-review.v17/copies/v16-extract"
V17 = "/tmp/opensip-design-corrections/candidate-subject.v17"
OUT = sys.argv[1]

FILES = [
    "docs/coop/design-corrections/workflows/workflows_model.v1.py",
    "docs/coop/design-corrections/native/native_evidence_model.v2.py",
    "docs/coop/design-corrections/foundation/identity-model.py",
    "docs/coop/design-corrections/foundation/check-identity.py",
    "docs/coop/design-corrections/workflows/check_workflows.v1.py",
    "docs/coop/design-corrections/check-integration.py",
]

REFUSAL_MARKS = ("raise", "refuse(", "Refusal(", "AdmissionError",
                 "faults.append", "check(", "rejects(", "assert ")


def executable_lines(path):
    """Return the source with comments and docstrings removed, as a line list."""
    with open(path, "rb") as fh:
        src = fh.read()
    text = src.decode("utf-8")
    out = []
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except Exception:
        return [l for l in text.splitlines() if l.strip()]
    # Identify docstring token positions (STRING that forms a whole statement)
    drop_rows = set()
    prev_meaningful = None
    for i, t in enumerate(toks):
        if t.type == tokenize.COMMENT:
            for r in range(t.start[0], t.end[0] + 1):
                pass
        if t.type == tokenize.STRING:
            # a docstring is a STRING whose previous meaningful token is
            # NEWLINE / INDENT / DEDENT / ENCODING (i.e. statement position)
            if prev_meaningful is None or prev_meaningful in (
                    tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
                    tokenize.ENCODING, tokenize.NL):
                for r in range(t.start[0], t.end[0] + 1):
                    drop_rows.add(r)
        if t.type not in (tokenize.NL, tokenize.COMMENT):
            prev_meaningful = t.type

    for n, line in enumerate(text.splitlines(), start=1):
        if n in drop_rows:
            continue
        # strip trailing comments crudely but safely: only when no quote present
        s = line
        if "#" in s and '"' not in s and "'" not in s:
            s = s.split("#", 1)[0]
        s = s.rstrip()
        if s.strip():
            out.append(s)
    return out


rep = {"files": []}
for rel in FILES:
    a_p, b_p = os.path.join(V16, rel), os.path.join(V17, rel)
    if not os.path.isfile(a_p):
        rep["files"].append({"path": rel, "v16Present": False})
        continue
    a, b = executable_lines(a_p), executable_lines(b_p)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    added, removed = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"):
            removed.extend(a[i1:i2])
        if tag in ("replace", "insert"):
            added.extend(b[j1:j2])
    rep["files"].append({
        "path": rel,
        "v16ExecutableLines": len(a),
        "v17ExecutableLines": len(b),
        "addedExecutableLines": len(added),
        "removedExecutableLines": len(removed),
        "added": added,
        "removed": removed,
        "addedRefusalBearing": [l for l in added
                                if any(m in l for m in REFUSAL_MARKS)],
        "addedNotRefusalBearing": [l for l in added
                                   if not any(m in l for m in REFUSAL_MARKS)],
        "removedRefusalBearing": [l for l in removed
                                  if any(m in l for m in REFUSAL_MARKS)],
        "executableUnchanged": not added and not removed,
    })

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True)

for f in rep["files"]:
    print("=" * 78)
    print(f["path"])
    if not f.get("v16Present", True):
        print("  not in v16")
        continue
    print("  executable lines %d -> %d | +%d / -%d"
          % (f["v16ExecutableLines"], f["v17ExecutableLines"],
             f["addedExecutableLines"], f["removedExecutableLines"]))
    print("  added refusal-bearing: %d | added other: %d | REMOVED refusal-bearing: %d"
          % (len(f["addedRefusalBearing"]), len(f["addedNotRefusalBearing"]),
             len(f["removedRefusalBearing"])))
    if f["removed"]:
        print("  --- REMOVED (%d) ---" % len(f["removed"]))
        for l in f["removed"][:40]:
            print("    -", l.strip()[:150])
