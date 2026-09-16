"""Baseline failure map BEFORE migration, on the captured source (no package or source edits).

A. Old package15 exports (immutable historical inputs) through check-export.v4.py: structural owner + full close_run.
B. Old package15 constructors, unmodified, building fresh exports into work/baseline/construct/.
Each job is receipted; a failing job is recorded, never retried under the same label.
Usage: baseline.py
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import runner  # noqa: E402

SRC, PKG, W = HERE / "source", HERE / "package15", HERE / "work/baseline"
rows = []
for group in ["checkpoint3", "normalized-examples6", "rust-selection-examples1", "semantic-controls1", "binding-controls"]:
    rows.append(runner.run("baseline-old-export-" + group, [runner.PY, "-I", "-B", PKG / "check-export.v4.py", "--input", PKG / group,
                                                           "--claims", PKG / group / "claims.json", "--source", SRC,
                                                           "--out", W / "old-exports" / group]))
    print(rows[-1]["label"], rows[-1]["exit"], flush=True)
for script, label in [("build-checkpoint3.py", "checkpoint"), ("build-normalized-examples6.py", "normalized"),
                      ("build-rust-selection-examples.py", "selection"), ("build-binding-controls.py", "binding")]:
    rows.append(runner.run("baseline-old-construct-" + label, [runner.PY, "-I", "-B", PKG / script, "--source", SRC,
                                                               "--package", PKG, "--out", W / "construct" / label]))
    print(rows[-1]["label"], rows[-1]["exit"], flush=True)
(HERE / "work/baseline-summary.json").write_text(json.dumps([{k: r[k] for k in ("label", "exit", "seconds")} for r in rows], indent=1) + "\n")
