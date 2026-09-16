"""Shared read-only loader for the view-attribution assessment probes.

Loads the frozen40 reference checker module (and through it the model, the owner fixture and the
host-capture fixture) straight from the verified snapshot. Nothing is written to the snapshot:
the interpreter runs with -I -B, and every output of these probes goes to this runtime only.

STANDING: every `admit(...)` call below is `admit_execution_inputs` on a reference-built graph.
That is reference self-consistency, not an independent reconstruction and not full Run admission.
Only a result recorded with standing `closed-run` went through the maintained `full_run` driver
(owner ADMIT -> R.derive -> seal -> IDENTITY.close_run).
"""
import hashlib
import importlib.util
import json
from pathlib import Path

FOUNDATION = Path("/tmp/opensip-design-corrections/candidate-subject.v40/docs/coop/design-corrections/foundation")
RUNTIME = Path("/private/tmp/opensip-design-corrections/claude-view-attribution-assessment.v1")


def load_checker():
    spec = importlib.util.spec_from_file_location("va_check_execution_inputs", FOUNDATION / "check-execution-inputs.v1.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


K = load_checker()
M, F, H = K.M, K.F, K.H


def short(x):
    if x is None:
        return None
    s = str(x)
    return s.split(":", 1)[-1][:10]


def matrix_rels(cap):
    return [list(p) for p in M._matrix_pairs(cap)]


def describe(kw):
    """Cells, bindings, the matrix relation filter, the host viewDigests and every resolved view."""
    objects = kw["objects"]
    ei = kw["execution_inputs"]
    enum = kw["enumeration_plan"]
    rows = {(r["cellOrdinal"], r["programOrdinal"]): r for r in ei["cellOutcomes"]}
    cells = []
    for ci, cell in enumerate(enum["cells"]):
        for b in cell["programBindings"]:
            row = rows.get((ci, b["ordinal"])) or {}
            cells.append({
                "cell": [ci, b["ordinal"]], "capabilityId": cell["capabilityId"],
                "languageMode": cell["languageMode"], "required": cell["required"],
                "matrixState": (M.CELL_STATE.get((cell["capabilityId"], cell["languageMode"])) or {}).get("state"),
                "matrixRelations": matrix_rels(cell["capabilityId"]),
                "universe": short(b.get("universe")),
                "enumerator": [(b.get("enumerator") or {}).get("status"), short((b.get("enumerator") or {}).get("closureId"))],
                "rowState": row.get("state"),
                "viewDigests": [short(v) for v in row.get("viewDigests") or []],
            })
    views = []
    for key, (dom, v) in sorted(objects.items()):
        if dom != "view":
            continue
        views.append({
            "view": short(key), "producer": short(v["producerClosure"]),
            "scopes": [
                [objects[s][1]["relation"], objects[s][1]["resolution"], short(objects[s][1]["sourceUniverse"])]
                for s in v["scopeIds"]
            ],
            "coverageCount": len(v["coverageIds"]), "factCount": len(v["facts"]),
            "inReceipt": any(r["digest"] == key.split(":", 1)[1]
                             for rc in ei["hostCapture"]["stageReceipts"] for r in rc["outputRefs"]),
            "inSelected": any(r["domain"] == "view" and r["digest"] == key.split(":", 1)[1] for r in ei["selectedRefs"]),
        })
    accounts = [
        [a["cellOrdinal"], a["programOrdinal"], a["relation"], a["resolution"], a["applicability"], len(a["coverageIds"])]
        for a in ei["nativeCoverageAccounts"]
    ]
    return {"cells": cells, "views": views, "accounts": accounts}


def admit_summary(kw):
    try:
        res = K.admit(kw)
    except Exception as exc:  # noqa: BLE001 - recorded, never swallowed silently
        return {"standing": "admission", "result": "EXCEPTION", "refusals": [type(exc).__name__ + ":" + str(exc)]}
    return {
        "standing": "admission", "result": res.get("result"),
        "refusals": res.get("refusals"),
        "derivedOutcomeStates": [d.get("state") for d in res.get("derivedOutcomes") or []],
        "derivedAccountStates": [[d.get("relation"), d.get("accountState")] for d in res.get("derivedAccounts") or []],
        "executionInputsDigest": M.raw_digest(kw["execution_inputs"]),
    }


def write_json(rel, value):
    path = RUNTIME / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(value, indent=2, sort_keys=True, default=str).encode() + b"\n"
    path.write_bytes(raw)
    return hashlib.sha256(raw).hexdigest()
