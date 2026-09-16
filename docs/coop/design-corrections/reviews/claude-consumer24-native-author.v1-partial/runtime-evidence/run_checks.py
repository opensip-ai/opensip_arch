"""Run the focused maintained reference checkers against THIS runtime's working source, one receipt each.

Usage: run_checks.py SUFFIX [name ...]
Every report path is inside this runtime (receipts/), never inside the source tree. check_native_evidence main()
writes into the native directory, so native cases run through probes/native_cases.py (run_case, no main()).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import runner  # noqa: E402

PY = "/tmp/opensip-architecture-review-env/bin/python"
SRC = HERE / "source"
DC = SRC / "docs/coop/design-corrections"
R = HERE / "receipts"
suffix = sys.argv[1]
only = set(sys.argv[2:])
JOBS = [
    ("current-profile", DC / "foundation/check-current-profile.v3.py", [], None),
    ("enumeration", DC / "foundation/check-enumeration.v1.py", ["--receipt", str(R / f"enumeration-{suffix}.receipt.json"), "--stdout"], None),
    ("atoms", DC / "foundation/check-atoms.v1.py", [], None),
    ("execution-inputs", DC / "foundation/check-execution-inputs.v1.py", [], None),
    ("composition", DC / "foundation/check-composition.v3.py", [], None),
    ("full-replay", DC / "foundation/check-replay.v3.py", [], None),
    ("semantic-replay", DC / "foundation/check-semantic-replay.v3.py", [], None),
    ("execution-replay", DC / "foundation/check-execution-replay.v3.py", [], None),
    ("candidate-replay", DC / "foundation/check-candidate-replay.v3.py", [], None),
    ("policy-derivation", DC / "foundation/check-policy-derivation.v3.py", [], None),
    ("evaluator-faults", DC / "foundation/check-evaluator-faults.v3.py", [], None),
    ("provider-attribution", DC / "foundation/check-provider-attribution-return.v2.py", [], None),
    ("identity", DC / "foundation/check-identity.py", ["--report", str(R / f"identity-{suffix}.report.json")], None),
    ("workflow-projection", DC / "workflows/check-workflow-projection.v3.py", [], None),
    ("query-projection", DC / "workflows/check-query-projection.v3.py", ["--report", str(R / f"query-projection-{suffix}.report.json")], None),
    ("comparison-knowledge", DC / "workflows/check-comparison-knowledge.v3.py", [], None),
    ("workflows", DC / "workflows/check_workflows.v1.py", ["--report", str(R / f"workflows-{suffix}.report.json")], DC / "workflows"),
    ("analysis-seal", DC / "security/check-analysis-seal-adapter.v1.py", [], None),
    ("security", DC / "security/check-security-lifecycle.v1.py", ["--report", str(R / f"security-{suffix}.report.json")], None),
    ("integration", DC / "check-integration.py", ["--report", str(R / f"integration-{suffix}.report.json")], None),
    ("native-cases", HERE / "probes/native_cases.py", [str(SRC)], None),
    ("corrections", DC / "foundation/check-native-consumer24-corrections.v1.py", [], None),
]
rows = []
for name, script, args, cwd in JOBS:
    if only and name not in only:
        continue
    if not Path(script).is_file():
        rows.append({"name": name, "skipped": "script absent"})
        continue
    res = runner.run(f"{name}-{suffix}", [PY, "-I", "-B", str(script)] + args, cwd=cwd, timeout=3000)
    rows.append({"name": name, "label": res["label"], "exit": res["exit"], "seconds": res["seconds"], "stdoutSha256": res["stdoutSha256"]})
    print(name, res["exit"], res["seconds"], flush=True)
(R / f"checks-{suffix}.summary.txt").write_text("\n".join(str(r) for r in rows) + "\n")
