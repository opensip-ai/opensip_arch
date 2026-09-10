#!/usr/bin/env python
"""Reproduce all six final-reference.v17 reference-check commands inside a
disposable FULL exact copy, and compare exits, stdout and regenerated in-tree
reports against the frozen results.

usage: run_six_checks.py <copy-name> <out.json>
"""
import hashlib
import json
import os
import subprocess
import sys

REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"
FROZEN = "/tmp/opensip-design-corrections/candidate-subject.v17"
BASE = "/tmp/opensip-design-corrections/post-reset-review.v17/copies"
RCREL = ("docs/coop/design-corrections/reviews/codex-post-reset.v1/"
         "final-reference.v17/reference-checks.json")
REPORT_OF = {
    "foundation": "docs/coop/design-corrections/foundation/validation-report.json",
    "security": "docs/coop/design-corrections/security/security-lifecycle-report.v1.json",
    "native": "docs/coop/design-corrections/native/native-evidence-report.v2.json",
    "workflows": "docs/coop/design-corrections/workflows/workflows-validation-report.json",
    "workflow-surface": "docs/coop/design-corrections/workflows/workflows-report.v1.json",
    "integration": "docs/coop/design-corrections/integration-report.v1.json",
}


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    copy_name, out_path = sys.argv[1], sys.argv[2]
    root = os.path.join(BASE, copy_name)
    rc = json.load(open(os.path.join(FROZEN, RCREL)))
    frozen_logdir = os.path.join(
        FROZEN, "docs/coop/design-corrections/reviews/codex-post-reset.v1/"
                "final-reference.v17")

    results = []
    for cmd in rc["commands"]:
        name = cmd["name"]
        src_in_copy = os.path.join(root, cmd["source"])
        # PRE-EXECUTION pin re-verification inside the copy itself
        pin_ok = os.path.isfile(src_in_copy) and \
            sha_file(src_in_copy) == cmd["sourceSha256"]
        argv = list(cmd["command"])
        proc = subprocess.run(argv, cwd=root, capture_output=True)
        rel = REPORT_OF[name]
        report_path = os.path.join(root, rel)
        regenerated = sha_file(report_path) if os.path.isfile(report_path) else None
        frozen_report = os.path.join(FROZEN, rel)
        frozen_sha = sha_file(frozen_report) if os.path.isfile(frozen_report) else None

        flog = os.path.join(frozen_logdir, cmd["log"])
        frozen_log_bytes = open(flog, "rb").read() if os.path.isfile(flog) else None

        results.append({
            "name": name,
            "source": cmd["source"],
            "pinReverifiedInCopyBeforeExecution": pin_ok,
            "declaredExitCode": cmd["exitCode"],
            "actualExitCode": proc.returncode,
            "exitMatches": proc.returncode == cmd["exitCode"],
            "stdoutSha256": sha_bytes(proc.stdout),
            "frozenLogSha256": sha_bytes(frozen_log_bytes)
                if frozen_log_bytes is not None else None,
            "stdoutMatchesFrozenLog": frozen_log_bytes is not None
                and proc.stdout == frozen_log_bytes,
            "stdout": proc.stdout.decode("utf-8", "replace"),
            "stderr": proc.stderr.decode("utf-8", "replace")[:4000],
            "reportPath": rel,
            "regeneratedReportSha256": regenerated,
            "frozenReportSha256": frozen_sha,
            "reportByteIdentical": regenerated is not None
                and regenerated == frozen_sha,
        })

    # Post-execution delta of the whole copy versus the manifest
    m = json.load(open(os.path.join(REV, "candidate-subject.v17.json")))
    declared = {e["path"]: e for e in m["files"]}
    modified, missing, added = [], [], []
    for p, e in declared.items():
        full = os.path.join(root, p)
        if not os.path.isfile(full):
            missing.append(p)
        elif sha_file(full) != e["sha256"]:
            modified.append(p)
    for dp, _, fns in os.walk(root):
        for fn in fns:
            r = os.path.relpath(os.path.join(dp, fn), root)
            if r not in declared:
                added.append(r)

    report_paths = set(REPORT_OF.values())
    rep = {
        "copyName": copy_name,
        "copyRoot": root,
        "commandCount": len(results),
        "commands": results,
        "allExitsMatch": all(r["exitMatches"] for r in results),
        "allPinsReverifiedInCopy": all(
            r["pinReverifiedInCopyBeforeExecution"] for r in results),
        "allReportsByteIdentical": all(r["reportByteIdentical"] for r in results),
        "allStdoutMatchesFrozenLog": all(
            r["stdoutMatchesFrozenLog"] for r in results),
        "postRunModified": sorted(modified),
        "postRunMissing": sorted(missing),
        "postRunAdded": sorted(added),
        "postRunModifiedOutsideReports": sorted(
            p for p in modified if p not in report_paths),
        "noSourceMutated": not [p for p in modified if p not in report_paths]
                           and not missing,
    }
    with open(out_path, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)

    for r in results:
        print("%-17s exit=%s(%s) pin=%s report_identical=%s stdout_identical=%s"
              % (r["name"], r["actualExitCode"], r["exitMatches"],
                 r["pinReverifiedInCopyBeforeExecution"],
                 r["reportByteIdentical"], r["stdoutMatchesFrozenLog"]))
    print()
    for k in ("allExitsMatch", "allPinsReverifiedInCopy",
              "allReportsByteIdentical", "allStdoutMatchesFrozenLog",
              "noSourceMutated"):
        print(k, "=", rep[k])
    print("postRunModified:", len(modified), "added:", len(added),
          "missing:", len(missing))
    print("modifiedOutsideReports:", rep["postRunModifiedOutsideReports"])
    print("added:", rep["postRunAdded"][:20])


if __name__ == "__main__":
    main()
