#!/usr/bin/env python3
"""Independent selected-helper required_parameters vs rust expected/actual."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

OVERLAY = Path(
    "/tmp/opensip-implementation/m2-enumeration-join-trial-41/reference/"
    "archroot/docs/coop/design-corrections/foundation/evaluator_input_model.v3.py"
)
REQ = Path("/tmp/opensip-implementation/m2-evaluator-parameters-trial-43/reference-check/requests.ndjson")
EXP = Path("/tmp/opensip-implementation/m2-evaluator-parameters-trial-43/reference-check/expected.ndjson")
OUT = Path("/tmp/opensip-implementation/m2-grok-evaluator-parameters-43/review/probe/e39_parameters.json")


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def packet_maps(req: dict):
    objects = {r["id"]: (r["domain"], r["descriptor"]) for r in req["objects"]}
    blobs = {r["digest"]: bytes.fromhex(r["hex"]) for r in req["blobs"]}
    return objects, blobs


def main() -> int:
    if sys.flags.int_max_str_digits != 0 or sys.get_int_max_str_digits() != 0:
        print("integer profile required", file=sys.stderr)
        return 2
    model = load(OVERLAY, "evaluator_input_v3")
    mismatches = []
    rows = []
    for i, (req_line, exp_line) in enumerate(zip(REQ.read_text().splitlines(), EXP.read_text().splitlines())):
        req = json.loads(req_line)
        expected = json.loads(exp_line)
        objects, blobs = packet_maps(req)
        plan_id = req["planId"]
        plan = objects[plan_id][1]
        spec_digest = plan["analysisSpecDigest"]
        spec = json.loads(blobs[spec_digest].decode("utf-8")) if False else None
        # analysis spec is a canonical record blob keyed by digest
        spec = model.C.parse(blobs[spec_digest])
        try:
            selected, policy, emission = model.required_parameters(plan, spec, blobs, objects, model.E.M)
            got = {
                "selected": {k: v[1] for k, v in selected.items()},
                "policy": policy,
                "emission": emission,
            }
            equal = model.C.equal_typed(got, expected)
            rows.append({"case": i, "label": req.get("label"), "match": equal, "error": None})
            if not equal:
                mismatches.append({"case": i, "label": req.get("label"), "kind": "value"})
        except Exception as exc:
            rows.append({"case": i, "label": req.get("label"), "match": False, "error": f"{type(exc).__name__}:{exc}"})
            mismatches.append({"case": i, "label": req.get("label"), "kind": "exception", "error": str(exc), "trace": traceback.format_exc(limit=6)})
    report = {
        "python": sys.version,
        "overlaySha256": hashlib.sha256(OVERLAY.read_bytes()).hexdigest(),
        "overlayBytes": OVERLAY.stat().st_size,
        "cases": len(rows),
        "matches": sum(1 for r in rows if r["match"]),
        "mismatches": mismatches,
        "rows": rows,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("cases", "matches")} | {"mismatchCount": len(mismatches)}, indent=2))
    if mismatches:
        print(json.dumps(mismatches, indent=2)[:4000])
    return 0 if not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
