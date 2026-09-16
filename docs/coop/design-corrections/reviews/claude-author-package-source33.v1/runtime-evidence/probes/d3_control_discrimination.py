"""Witness that the three semantic negatives again refuse for their OWN tamper.

In package9 the TS base proof was itself stale, so every one of these three refused with
EVALUATOR_COMPLETE_PROOF_REPLAY whether or not its mutation was present: the group reported
'pass' while having lost its discriminating power. With the source33 remint the untampered base
ADMITs, so each refusal is attributable to that control's own mutation. This probe states both
halves for v9 and for v10.
"""
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
SRC = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
F = SRC / "docs/coop/design-corrections/foundation"
V9 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v9")
V10 = Path("/tmp/opensip-design-corrections/claude-author-package-successor.v10")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("d3_identity", F / "identity-model.v3.py")
R = load("d3_replay", F / "evaluator_replay_model.v3.py")
T = load("d3_transport", V10 / "check-export.v4.py")


def semantic(pkg, group, name):
    claims = json.loads((pkg / group / "claims.json").read_text())
    row = next(c for c in claims if c["name"] == name)
    objects, blobs = T.decode_store((pkg / group / row["path"]).read_bytes(), M)
    run = objects[row["runId"]][1]
    try:
        M.open_run_closure(run, objects, blobs)
    except Exception as exc:  # noqa: BLE001
        return {"runId": row["runId"], "owner": "REFUSE", "semantic": None,
                "reason": f"{type(exc).__name__}: {exc}"}
    try:
        R.replay(run, objects, blobs)
        return {"runId": row["runId"], "owner": "ADMIT", "semantic": "ADMIT", "reason": None}
    except Exception as exc:  # noqa: BLE001
        return {"runId": row["runId"], "owner": "ADMIT", "semantic": "REFUSE", "reason": str(exc)}


out = {
    "standing": "Discriminating-power witness for the three semantic negative controls, replayed "
                "against frozen source33. Author evidence only.",
}
for label, pkg in (("package9-source30-construction", V9), ("package10-source33-remint", V10)):
    base = semantic(pkg, "checkpoint3", "author-ts")
    controls = {n: semantic(pkg, "semantic-controls1", n)
                for n in ("severity", "unrelated-scope", "collapsed-deficiencies")}
    out[label] = {
        "untamperedBase": base,
        "tamperedControls": controls,
        "baseAdmits": base["semantic"] == "ADMIT",
        "allControlsRefuse": all(c["semantic"] == "REFUSE" for c in controls.values()),
        "refusalsAttributableToTheirOwnMutation":
            base["semantic"] == "ADMIT" and all(c["semantic"] == "REFUSE" for c in controls.values()),
    }
out["conclusion"] = (
    "package9: the base itself refused, so each control would have refused with the SAME key "
    "without its mutation - the group still reported 'pass' but established nothing about the "
    "mutation. package10: the base admits, so every refusal isolates that control's own tamper."
)
print(json.dumps(out, indent=2, default=str))
