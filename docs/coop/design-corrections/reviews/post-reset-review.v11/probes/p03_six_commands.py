#!/usr/bin/env python3
"""p03: reproduce all SIX reference commands inside the disposable full-subject copy.

The declared commands hardcode the ORIGINAL repository path. Regenerating reports there is
forbidden, so each command is rewritten to the disposable copy and executed with cwd set to
the copy. Reports are captured BEFORE the run, then compared byte-identically after.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

PY = "/tmp/opensip-architecture-review-env/bin/python"
COPY = "/tmp/opensip-design-corrections/post-reset-review.v11/copies/subject-v11"
ORIG_PREFIX = "/Users/sb/code/opensip-ai/opensip_arch/"
SPEC = os.path.join(
    COPY,
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v11/reference-checks.json",
)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


spec = json.load(open(SPEC))
results = []

for entry in spec["commands"]:
    name = entry["name"]
    # verify the pinned source bytes in the copy match the declared producer digest
    src_rel = entry["source"]
    src_abs = os.path.join(COPY, src_rel)
    src_sha = sha(src_abs)

    cmd = []
    report_rel = None
    for i, tok in enumerate(entry["command"]):
        if tok.startswith(ORIG_PREFIX):
            cmd.append(os.path.join(COPY, tok[len(ORIG_PREFIX):]))
        else:
            cmd.append(tok)
        if entry["command"][i - 1] == "--report" if i else False:
            report_rel = tok

    before_sha = before_bytes = None
    if report_rel:
        rp = os.path.join(COPY, report_rel)
        if os.path.isfile(rp):
            before_sha = sha(rp)
            before_bytes = open(rp, "rb").read()

    proc = subprocess.run(cmd, cwd=COPY, capture_output=True, text=True)

    after_sha = None
    identical = None
    if report_rel:
        rp = os.path.join(COPY, report_rel)
        if os.path.isfile(rp):
            after_sha = sha(rp)
            identical = (before_bytes == open(rp, "rb").read())

    results.append({
        "name": name,
        "source": src_rel,
        "declaredSourceSha256": entry["sourceSha256"],
        "observedSourceSha256": src_sha,
        "sourceShaMatches": src_sha == entry["sourceSha256"],
        "declaredExitCode": entry["exitCode"],
        "observedExitCode": proc.returncode,
        "exitMatches": proc.returncode == entry["exitCode"],
        "report": report_rel,
        "reportShaBefore": before_sha,
        "reportShaAfter": after_sha,
        "reportByteIdentical": identical,
        "stdoutTail": proc.stdout[-1500:],
        "stderrTail": proc.stderr[-1500:],
    })

summary = {
    "allSourceShasMatch": all(r["sourceShaMatches"] for r in results),
    "allExitCodesMatch": all(r["exitMatches"] for r in results),
    "allReportsByteIdentical": all(
        r["reportByteIdentical"] for r in results if r["report"]),
    "commandCount": len(results),
    "results": results,
}
print(json.dumps(summary, indent=2))
