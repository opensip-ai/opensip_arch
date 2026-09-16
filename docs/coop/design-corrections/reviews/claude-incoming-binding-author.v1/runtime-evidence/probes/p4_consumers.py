"""P4 — atom-model consumers on frozen34 and on the successor, stdout compared byte for byte.

Justification: atom_model.v1.py changed (incoming I1; subject-scope carrier pass-through), and these
checkers import it directly or through evaluator_replay_model.v3.py /
provider_attribution_return_model.v2.py. All run with NO arguments; every write in them is gated on
an explicit flag, so neither tree is written. These are reference checker executions, not the six
broad groups, not pin validation, not a retained-corpus replay.
"""
import hashlib
import json
import subprocess
from pathlib import Path

PY = "/tmp/opensip-architecture-review-env/bin/python"
TREES = {
    "frozen34": "/tmp/opensip-design-corrections/candidate-subject.v34/docs/coop/design-corrections/foundation",
    "successor": "/tmp/opensip-design-corrections/incoming-binding-successor.v1/source/docs/coop/design-corrections/foundation",
}
CHECKS = ["check-replay.v3.py", "check-semantic-replay.v3.py", "check-candidate-replay.v3.py",
          "check-execution-replay.v3.py", "check-execution-inputs.v1.py",
          "check-provider-attribution-return.v2.py", "check-composition.v3.py"]
OUT = Path(__file__).resolve().parent / "receipts" / "p4-consumer-streams"
OUT.mkdir(parents=True, exist_ok=True)
rows = []
for name in CHECKS:
    row = {"check": name}
    streams = {}
    for label, root in TREES.items():
        argv = [PY, "-I", "-B", f"{root}/{name}"]
        p = subprocess.run(argv, capture_output=True, timeout=900)
        stdout = p.stdout.replace(root.encode(), b"<FOUNDATION>")
        streams[label] = stdout
        (OUT / f"{label}__{name}.stdout").write_bytes(p.stdout)
        (OUT / f"{label}__{name}.stderr").write_bytes(p.stderr)
        row[label] = {"argv": argv, "exit": p.returncode, "stdoutSha256": hashlib.sha256(stdout).hexdigest(),
                      "stderrTail": p.stderr.decode("utf-8", "replace")[-300:] if p.returncode else ""}
    row["identicalStdout"] = streams["frozen34"] == streams["successor"]
    rows.append(row)
print(json.dumps({"checks": rows,
                  "allExitZero": all(r[t]["exit"] == 0 for r in rows for t in TREES),
                  "allIdentical": all(r["identicalStdout"] for r in rows)}, indent=1))
