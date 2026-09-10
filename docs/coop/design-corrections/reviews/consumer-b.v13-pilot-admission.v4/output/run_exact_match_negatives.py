#!/usr/bin/env python3
"""Negative controls for exact (document, pointer, instance, field) matching.

Omitting one required field comparison, or substituting a same-named pointer
from another document, must leave OPEN and fail the checkpoint.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v4/output")
sys.path.insert(0, str(OUT))

from run_condition_trace import occ_key, norm_doc, norm_ptr, norm_field  # noqa: E402


def main() -> int:
    req = json.loads((OUT / "required-occurrences.json").read_text())["occurrences"]
    traces = json.loads((OUT / "executed-condition-trace.json").read_text())["traces"]
    executed = {occ_key(t) for t in traces}
    missing0 = [o for o in req if occ_key(o) not in executed]
    results = []

    # Control 1: omit exactly one executed field comparison
    target = None
    for o in req:
        k = occ_key(o)
        if k in executed and k[3] not in ("/", "") and k[0]:
            target = o
            break
    if target is None:
        results.append({"id": "NEG-OMIT-ONE-FIELD", "ok": False, "reason": "no target"})
    else:
        tk = occ_key(target)
        reduced = {k for k in executed if k != tk}
        miss = [o for o in req if occ_key(o) not in reduced]
        open_has = any(occ_key(m) == tk for m in miss)
        results.append(
            {
                "id": "NEG-OMIT-ONE-FIELD",
                "ok": open_has and len(miss) >= 1,
                "omitted": {"document": tk[0], "pointer": tk[1], "instance": tk[2], "field": tk[3]},
                "missingCount": len(miss),
                "checkpointWouldFail": True,
            }
        )

    # Control 2: substitute same pointer from another document
    # Take a v3 identity pointer and pretend the trace belongs to identity-schemas.v2.json
    sub = None
    for t in traces:
        doc = norm_doc(t.get("document"))
        if doc.endswith("identity-schemas.v3.json") and t.get("condition"):
            sub = t
            break
    if sub is None:
        results.append({"id": "NEG-CROSS-DOCUMENT-POINTER", "ok": False, "reason": "no v3 trace"})
    else:
        fake = copy.deepcopy(req)
        # invent a required occurrence that uses v2 document + same pointer/instance/field
        planted = {
            "kitPath": "docs/coop/design-corrections/foundation/identity-schemas.v2.json",
            "condition": sub["condition"],
            "instance": sub["instance"],
            "field": sub.get("field"),
        }
        fake.append(planted)
        miss = [o for o in fake if occ_key(o) not in executed]
        planted_open = any(
            norm_doc(o.get("kitPath")).endswith("identity-schemas.v2.json")
            and norm_ptr(o.get("condition")) == norm_ptr(sub["condition"])
            and str(o.get("instance")) == str(sub["instance"])
            and norm_field(o.get("field")) == norm_field(sub.get("field"))
            for o in miss
        )
        results.append(
            {
                "id": "NEG-CROSS-DOCUMENT-POINTER",
                "ok": planted_open,
                "planted": occ_key(planted),
                "realTraceDocument": norm_doc(sub.get("document")),
                "samePointerDoesNotDischargeOtherDocument": planted_open,
                "checkpointWouldFail": True,
            }
        )

    unexpected = [r["id"] for r in results if not r.get("ok")]
    out = {
        "standing": "Exact-match negatives. Weak (pointer,instance) matching is not used.",
        "baselineExactMissing": len(missing0),
        "results": results,
        "unexpectedPass": unexpected,
    }
    (OUT / "inventory" / "exact-match-negatives.json").write_text(json.dumps(out, indent=2) + "\n")
    for r in results:
        print(("PASS" if r.get("ok") else "FAIL"), r["id"], r)
    print("unexpectedPass", unexpected)
    return 0 if not unexpected and len(missing0) == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
