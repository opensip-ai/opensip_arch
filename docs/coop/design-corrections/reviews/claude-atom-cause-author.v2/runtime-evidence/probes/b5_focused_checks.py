"""Run the checks justified by the v2 atom-model edit, and compare to the v1-final stdout.

Justification: `_unique_pairs` and `_coverages_for_current_source` changed, so every checker that
imports atom_model.v1.py (directly or through evaluator_replay_model.v3.py /
provider_attribution_return_model.v2.py) is affected. The contract .md is executed by no checker.
The six broad reference groups are deliberately NOT run; root runs those after pin reconciliation.

v1's retained stdout is read only, never rewritten.
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, "/private/tmp/opensip-design-corrections/claude-atom-cause-author.v2")
import runner  # noqa: E402

NEW = ("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/"
       "docs/coop/design-corrections/foundation")
V1R = Path("/tmp/opensip-design-corrections/claude-atom-cause-author.v1/probes/receipts")
PY = "/tmp/opensip-architecture-review-env/bin/python"

CHECKS = [
    ("check-replay.v3.py", "focused-check-replay.v3"),
    ("check-semantic-replay.v3.py", "focused-check-semantic-replay.v3"),
    ("check-candidate-replay.v3.py", "focused-check-candidate-replay.v3"),
    ("check-execution-replay.v3.py", "focused-check-execution-replay.v3"),
    ("check-execution-inputs.v1.py", "focused-check-execution-inputs.v1"),
    ("check-provider-attribution-return.v2.py", "focused-check-provider-attribution-return.v2"),
]

rows = []
for name, v1_label in CHECKS:
    r = runner.run("v2-" + name.replace(".py", ""), [PY, "-I", "-B", NEW + "/" + name])
    new = Path(r["stdoutPath"]).read_bytes()
    old_path = V1R / v1_label / "stdout.txt"
    old = old_path.read_bytes() if old_path.exists() else None
    rows.append({
        "check": name, "exit": r["exit"], "receipt": r["label"],
        "v2StdoutSha256": hashlib.sha256(new).hexdigest(),
        "v1StdoutSha256": hashlib.sha256(old).hexdigest() if old is not None else None,
        "identicalToV1Final": (old == new) if old is not None else None,
        "stderrTail": r["stderrTail"][-300:] if r["exit"] != 0 else "",
    })

print(json.dumps({
    "standing": "Focused affected checks only; the six broad groups were not run.",
    "checks": rows,
    "allExitZero": all(r["exit"] == 0 for r in rows),
    "allIdenticalToV1Final": all(r["identicalToV1Final"] for r in rows),
}, indent=2, default=str))
