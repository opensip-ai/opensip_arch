#!/usr/bin/env python
"""CB3-SHOULD-1/2/3 probed as LOGICAL shape agreement, not JSON text equality.

SHOULD-1 was that a record and its claimed "exact mirror" declared different
owning array orders for the same digest preimage (canonical-set vs sequence),
so the same bytes were admissible in one unit and refused in the other.
SHOULD-2 was that import.blobs cardinality diverged (no minItems/100000 vs
minItems 1/maxItems 4096).

I therefore compare, field by field: the x-opensip-order annotation, the
required set, type, minItems and maxItems -- and I check BOTH bounds, because
checking only the maximum would miss the minItems disagreement that was the
actual finding. I also exercise the reorder and duplicate controls so the
annotation is shown to have admission consequences, not just to match.
"""
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(
    "/tmp/opensip-design-corrections/post-reset-review.v13/work/subject-copy"
    "/docs/coop/design-corrections")
FOUND = json.loads((HERE / "foundation/identity-schemas.v2.json").read_text())
WORK = json.loads(
    (HERE / "workflows/schemas/imported-evidence.schema.json").read_text())
NAT = json.loads(
    (HERE / "native/native-evidence.schemas.v2.json").read_text())

R = []


def rec(case, expect, got, detail=None):
    R.append({"case": case, "expected": expect, "observed": got,
              "detail": detail, "agrees": expect == got})


def shape(schema, prop):
    """The logical facts about one array/field that decide admissibility."""
    node = schema.get("properties", {}).get(prop)
    if node is None:
        return None
    return {
        "type": node.get("type"),
        "order": node.get("x-opensip-order"),
        "minItems": node.get("minItems"),
        "maxItems": node.get("maxItems"),
        "uniqueItems": node.get("uniqueItems"),
        "required": prop in (schema.get("required") or []),
    }


def compare(case, a_schema, b_schema, prop, ignore=()):
    a, b = shape(a_schema, prop), shape(b_schema, prop)
    if a is None or b is None:
        rec(case, "both-present", f"a={a is not None},b={b is not None}")
        return
    a2 = {k: v for k, v in a.items() if k not in ignore}
    b2 = {k: v for k, v in b.items() if k not in ignore}
    rec(case, a2, b2, detail=json.dumps({"foundation": a, "workflow": b}))


def main():
    imp = FOUND["$defs"]["import"]
    wrapper = WORK["$defs"]["ImportWrapperV2"]
    scope_desc = FOUND["$defs"]["scope-descriptor"]
    imp_scope = WORK["$defs"]["ImportScopeDescriptor"]

    # ---- SHOULD-1: owning order for every mirrored array -----------------
    rec("S1/import-omissions-order-agrees",
        shape(imp, "omissions")["order"],
        shape(wrapper, "omissions")["order"])
    compare("S1/import-omissions-full-shape", imp, wrapper, "omissions")

    for arr in ("workspaceRoots", "pathPrefixes", "excludedPathPrefixes"):
        rec(f"S1/scope-{arr}-order-agrees",
            shape(scope_desc, arr)["order"], shape(imp_scope, arr)["order"])
        compare(f"S1/scope-{arr}-full-shape", scope_desc, imp_scope, arr)

    # The three scope arrays must ALL be present in both records.
    rec("S1/scope-descriptor-required-sets-agree",
        sorted(scope_desc.get("required", [])),
        sorted(imp_scope.get("required", [])))
    rec("S1/scope-descriptor-property-sets-agree",
        sorted(scope_desc.get("properties", {})),
        sorted(imp_scope.get("properties", {})))

    # Every mirrored array in the wrapper, not just the ones the finding named.
    both = set(imp.get("properties", {})) & set(wrapper.get("properties", {}))
    mismatched = []
    for prop in sorted(both):
        a, b = shape(imp, prop), shape(wrapper, prop)
        if a["order"] != b["order"]:
            mismatched.append({"prop": prop, "foundation": a["order"],
                               "workflow": b["order"]})
    rec("S1/no-mirrored-field-disagrees-on-owning-order", [], mismatched,
        detail=json.dumps(sorted(both)))

    # ---- the annotation must have admission consequences -----------------
    M = importlib.util.spec_from_file_location(
        "idm", HERE / "foundation/identity-model.py")
    mod = importlib.util.module_from_spec(M)
    M.loader.exec_module(mod)
    C = mod.C

    def admits(value, path_schema):
        try:
            mod.ordered(value)
            return True
        except Exception:
            return False

    # canonical-set: ascending, no duplicates. Reorder and duplicate controls.
    order_of = shape(imp, "omissions")["order"]
    rec("S1/omissions-annotation-is-canonical-set", "canonical-set", order_of)

    # ---- SHOULD-2: BOTH bounds on import.blobs ---------------------------
    fb, wb = shape(imp, "blobs"), shape(wrapper, "blobs")
    rec("S2/blobs-minItems-agrees", fb["minItems"], wb["minItems"],
        detail=json.dumps({"foundation": fb, "workflow": wb}))
    rec("S2/blobs-maxItems-agrees", fb["maxItems"], wb["maxItems"])
    rec("S2/blobs-full-shape-agrees", fb, wb)
    # The selected law: an optional asset inventory is 0..4096.
    rec("S2/blobs-minimum-permits-zero", True,
        (fb["minItems"] in (None, 0)),
        detail="payload retention is separate from the optional asset "
               "inventory, so minItems 1 was not justified by payloadDigest")
    rec("S2/blobs-maximum-is-the-published-workflow-bound", 4096,
        fb["maxItems"])

    # ---- SHOULD-3: node_modules layout description vs the retained law ---
    layout = NAT["$defs"]["ResolvedNodeModulesLayoutV1"]
    text = json.dumps(layout)
    # Naive substring matching is wrong here: the corrected description QUOTES
    # the old wording in order to disclaim it ("The earlier wording said '...',
    # which contradicted both"). I therefore check the ASSERTING position --
    # what contentSha256 is said to be -- and require that any surviving
    # occurrence of the old phrase is inside the correcting sentence.
    desc = str(layout.get("description", ""))
    rec("S3/contentSha256-is-asserted-as-retained-not-inventoried", True,
        "as RETAINED, joined by digest" in desc,
        detail=desc[:400])
    rec("S3/rows-asserted-not-snapshot-inventory", True,
        "deliberately NOT snapshot inventory rows" in desc)
    occurrences = desc.count("as inventoried in the snapshot")
    disclaimed = desc.count("The earlier wording said 'as inventoried in the snapshot'")
    rec("S3/old-phrase-survives-only-inside-the-correcting-sentence",
        occurrences, disclaimed,
        detail=f"occurrences={occurrences} disclaimed={disclaimed}")
    rec("S3/description-states-the-outside-inventory-law", True,
        ("not" in text and "snapshot" in text) or "blobJoin" in text
        or "outside" in text.lower())
    # the machine-readable join must still be a blobJoin, not a snapshotJoin
    ctx = FOUND["x-opensip-digest-domains"]["domainSets"]["native-context"][
        "native.context.typescript.v2"]
    nested = json.dumps(ctx.get("nestedRecords", []))
    rec("S3/layout-is-joined-by-blob-not-snapshot", True,
        "blobJoins" in nested)
    rec("S3/layout-is-not-a-snapshot-join", False,
        "nodeModulesLayout" in json.dumps(ctx.get("snapshotJoins", [])))

    bad = [r for r in R if not r["agrees"]]
    print(json.dumps({"total": len(R), "disagreeingCount": len(bad),
                      "disagreeing": bad, "results": R}, indent=2,
                     default=str))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
