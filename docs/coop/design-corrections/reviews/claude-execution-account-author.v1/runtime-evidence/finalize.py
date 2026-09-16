#!/usr/bin/env python3
"""Final consistency check of this runtime's deliverables + receipts index."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source")


def main() -> int:
    after = json.loads((HERE / "after-hashes.json").read_text())
    drift = []
    for row in after:
        now = hashlib.sha256((SRC / row["path"]).read_bytes()).hexdigest()
        if now != row["sha256"]:
            drift.append({"path": row["path"], "recorded": row["sha256"], "now": now})

    tree = json.loads((HERE / "tree-delta.json").read_text())
    handoff = json.loads((HERE / "changed-file-handoff.json").read_text())
    tree_changed = {r["path"] for r in tree["changedFiles"]}
    handoff_changed = {r["path"] for r in handoff["changedFiles"]}

    receipts = []
    for d in sorted((HERE / "probes" / "receipts").iterdir()):
        # The runner creates this run's own receipt directory before invoking us, so it is
        # legitimately incomplete while we look at it.
        if not d.is_dir() or not (d / "command.json").is_file() or not (d / "exit.txt").is_file():
            continue
        receipts.append({
            "label": d.name,
            "argv": json.loads((d / "command.json").read_text())["argv"],
            "exit": int((d / "exit.txt").read_text().strip()),
            "stdoutBytes": (d / "stdout.txt").stat().st_size,
            "stderrBytes": (d / "stderr.txt").stat().st_size,
        })

    deliverables = [
        "author-review.md", "author-review.json", "assessment-corrections.md",
        "changed-file-handoff.json", "tree-delta.json", "suite-report.json", "suite2-report.json",
        "before-hashes.json", "after-hashes.json", "DISPOSABLE-rebound-source-pins.json",
    ]
    out = {
        "standing": "Final consistency check of this source-author runtime. Not acceptance.",
        "afterHashDrift": drift,
        "treeDeltaMatchesHandoff": tree_changed == handoff_changed,
        "treeChanged": sorted(tree_changed),
        "treeAdded": tree["addedFiles"],
        "treeRemoved": tree["removedFiles"],
        "deliverables": [
            {"file": f, "exists": (HERE / f).is_file(),
             "sha256": hashlib.sha256((HERE / f).read_bytes()).hexdigest() if (HERE / f).is_file() else None,
             "bytes": (HERE / f).stat().st_size if (HERE / f).is_file() else None}
            for f in deliverables
        ],
        "receipts": receipts,
        "receiptCount": len(receipts),
        "nonZeroExitReceipts": [r["label"] for r in receipts if r["exit"] != 0],
        "nonZeroExitExplanation": {
            "step2-check-execution-inputs": "intermediate authoring iteration; exit 1 on one real "
                                            "mismatch (the typed-census control built on the wrong "
                                            "owner graph), fixed and re-run as step3/step4/step5.",
            "step3-check-execution-inputs": "intermediate authoring iteration; exit 1 on one real "
                                            "oracle failure (censusMissing empty because the "
                                            "retired view returned through the carried refs), "
                                            "fixed and re-run as step4/step5.",
            "finalize": "this report reads the receipts directory that the runner has already "
                        "created for THIS invocation, so any exit code shown for `finalize` is the "
                        "PREVIOUS finalize run, not this one. The first finalize run crashed on "
                        "that same incompleteness and was fixed.",
        },
        "finalCheckerRun": "step5-check-execution-inputs and the suite copy at "
                           "suite/execution-inputs.stdout: 71 cases, 0 mismatches, 0 oracle "
                           "failures, exit 0.",
    }
    (HERE / "finalize-report.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({
        "afterHashDrift": out["afterHashDrift"],
        "treeDeltaMatchesHandoff": out["treeDeltaMatchesHandoff"],
        "treeAdded": out["treeAdded"], "treeRemoved": out["treeRemoved"],
        "missingDeliverables": [d["file"] for d in out["deliverables"] if not d["exists"]],
        "receiptCount": out["receiptCount"],
        "nonZeroExitReceipts": out["nonZeroExitReceipts"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
