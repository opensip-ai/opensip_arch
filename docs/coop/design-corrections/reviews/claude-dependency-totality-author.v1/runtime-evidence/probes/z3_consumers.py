"""Z3 — atom-model consumers on the PREVIOUS tree (dependency-scope-successor) and the successor, stdout compared.

Justification: atom_model.v1.py changed (_dependency_totality_gaps and run_suff), and these checkers
import it directly or through evaluator_replay_model.v3.py / provider_attribution_return_model.v2.py.
All run with NO arguments; their writes are flag-gated, so neither tree is written.
Not the integrated groups, not pin validation.
"""
import hashlib
import json
import subprocess
from pathlib import Path

PY = "/tmp/opensip-architecture-review-env/bin/python"
TREES = {
    "previous": "/tmp/opensip-design-corrections/dependency-scope-successor.v1/source/docs/coop/design-corrections/foundation",
    "successor": "/tmp/opensip-design-corrections/dependency-totality-successor.v1/source/docs/coop/design-corrections/foundation",
}
CHECKS = ["check-replay.v3.py", "check-semantic-replay.v3.py", "check-candidate-replay.v3.py",
          "check-execution-replay.v3.py", "check-execution-inputs.v1.py",
          "check-provider-attribution-return.v2.py", "check-composition.v3.py"]
OUT = Path(__file__).resolve().parent / "receipts" / "z3-consumer-streams"
OUT.mkdir(parents=True, exist_ok=True)
rows = []
for name in CHECKS:
    row = {"check": name}
    streams = {}
    for label, root in TREES.items():
        argv = [PY, "-I", "-B", f"{root}/{name}"]
        p = subprocess.run(argv, capture_output=True, timeout=1500)
        streams[label] = p.stdout.replace(root.encode(), b"<FOUNDATION>")
        (OUT / f"{label}__{name}.stdout").write_bytes(p.stdout)
        (OUT / f"{label}__{name}.stderr").write_bytes(p.stderr)
        row[label] = {"argv": argv, "exit": p.returncode, "stdoutSha256": hashlib.sha256(streams[label]).hexdigest(),
                      "stderrSha256": hashlib.sha256(p.stderr).hexdigest(),
                      "stderrTail": p.stderr.decode("utf-8", "replace")[-300:] if p.returncode else ""}
    row["identicalStdout"] = streams["previous"] == streams["successor"]
    rows.append(row)
print(json.dumps({"checks": rows, "allExitZero": all(r[t]["exit"] == 0 for r in rows for t in TREES),
                  "allIdentical": all(r["identicalStdout"] for r in rows)}, indent=1))
