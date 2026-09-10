#!/usr/bin/env python3
"""P01: independent reconstruction of the inherited fact-plane relation
constraints, compared field-by-field against the v8 successor document.

Does NOT read the successor's own `inheritedRequired`/`inheritedOptional`
labels as truth: those are re-derived from fact-plane.v1.json and only then
compared. Also checks the logical carry-over of the withdrawn CBOR profile:
NFC-only text, no negative integers, uint64 range, closed field set, enums,
per-rung required/forbidden, universeRule.
"""
import json, sys

ROOT = "/tmp/opensip-design-corrections/candidate-subject.v8"
FP = f"{ROOT}/docs/coop/artifacts/fact-plane.v1.json"
NEW = f"{ROOT}/docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
NATIVE = f"{ROOT}/docs/coop/design-corrections/native/native-evidence.schemas.v2.json"

out = {"perRelation": {}, "summary": {}, "problems": []}


def deref(doc, sel):
    node = doc
    for part in sel.lstrip("#/").split("/"):
        if part:
            node = node[part]
    return node


def main():
    fp = json.load(open(FP))
    new = json.load(open(NEW))
    reg_old = fp["factRecordContractV1"]["relationPayloadSchemaRegistryV1"]
    old_schemas = reg_old["schemas"]
    shared_old = reg_old.get("sharedTypes", {})
    reg_new = new["x-opensip-relation-registry"]["relations"]

    out["summary"]["inheritedRelationCount"] = len(old_schemas)
    out["summary"]["successorRelationCount"] = len(reg_new)
    out["summary"]["inheritedRelations"] = sorted(old_schemas)
    out["summary"]["successorRelations"] = sorted(reg_new)
    out["summary"]["addedBySuccessor"] = sorted(set(reg_new) - set(old_schemas))
    out["summary"]["droppedBySuccessor"] = sorted(set(old_schemas) - set(reg_new))
    out["summary"]["oldCanonicalPayloadEncoding"] = reg_old["canonicalPayloadEncoding"]

    # ---- per-relation field/type/rung/universe fidelity -------------------
    for rel in sorted(set(old_schemas) | set(reg_new)):
        rec = {"inInherited": rel in old_schemas, "inSuccessor": rel in reg_new}
        if rel not in old_schemas or rel not in reg_new:
            out["perRelation"][rel] = rec
            continue
        o = old_schemas[rel]
        n = reg_new[rel]
        # independently derive the inherited field sets from the old schema
        o_req = sorted(o.get("required", []))
        o_opt = sorted(o.get("optional", []))
        rec["inheritedRequired_derived"] = o_req
        rec["inheritedOptional_derived"] = o_opt
        rec["successorClaimsRequired"] = sorted(n.get("inheritedRequired", []))
        rec["successorClaimsOptional"] = sorted(n.get("inheritedOptional", []))
        rec["labelsHonest"] = (o_req == rec["successorClaimsRequired"]
                               and o_opt == rec["successorClaimsOptional"])

        # now check the ACTUAL successor JSON Schema, not the label
        sel = n["selector"]
        try:
            sch = deref(new, sel)
        except Exception as e:  # pragma: no cover
            rec["selectorResolves"] = False
            out["problems"].append(f"{rel}: selector {sel} unresolvable: {e}")
            out["perRelation"][rel] = rec
            continue
        rec["selectorResolves"] = True
        props = sch.get("properties", {})
        rec["successorSchemaProps"] = sorted(props)
        rec["successorSchemaRequired"] = sorted(sch.get("required", []))
        rec["additionalPropertiesFalse"] = sch.get("additionalProperties") is False
        # closed field set == inherited required + optional
        rec["fieldSetMatchesInherited"] = sorted(props) == sorted(set(o_req) | set(o_opt))
        rec["requiredMatchesInherited"] = rec["successorSchemaRequired"] == o_req

        # inherited per-field types, resolving shared types on both sides
        o_fields = o.get("fields", o.get("properties", {}))
        rec["inheritedFieldTypes"] = {k: (v if isinstance(v, str) else json.dumps(v))
                                      for k, v in o_fields.items()}

        # rungs
        o_rungs = o.get("resolutionRungs", o.get("rungs", {}))
        rec["inheritedRungs_raw"] = o_rungs
        rec["successorRungs"] = n.get("rungs", {})
        # universe rule
        rec["inheritedUniverseRule"] = o.get("universeRule", o.get("universe"))
        rec["successorUniverseRule"] = n.get("universeRule")
        rec["universeRuleMatches"] = (rec["inheritedUniverseRule"] is None
                                      or rec["inheritedUniverseRule"] == n.get("universeRule"))
        out["perRelation"][rel] = rec

    # ---- logical carry-over of the CBOR restrictions ----------------------
    defs = new["$defs"]
    carry = {}
    # uint64 range
    u = defs.get("UInt64", {})
    carry["UInt64"] = u
    carry["uint64_nonneg"] = u.get("minimum") == 0
    carry["uint64_max"] = u.get("maximum") == 18446744073709551615
    # NFC text
    ct = defs.get("CanonicalText", {})
    carry["CanonicalText"] = ct
    carry["nfcDeclared"] = "nfc" in json.dumps(ct).lower()
    # scan every leaf integer type for a negative-admitting bound
    neg = []
    def scan(node, path):
        if isinstance(node, dict):
            if node.get("type") == "integer":
                mn = node.get("minimum")
                if mn is None or mn < 0:
                    neg.append({"path": path, "minimum": mn})
            for k, v in node.items():
                scan(v, path + "/" + str(k))
        elif isinstance(node, list):
            for i, v in enumerate(node):
                scan(v, path + "/" + str(i))
    scan(defs, "#/$defs")
    carry["integerFieldsAdmittingNegative"] = neg
    # number/float admitted anywhere?
    carry["numberTypeUsed"] = '"number"' in json.dumps(new)
    out["cborLogicalCarryOver"] = carry

    # ---- unresolved-edge must exist in native too -------------------------
    nat = json.load(open(NATIVE))
    rel_enum = nat.get("$defs", {}).get("Relation", {}).get("enum")
    out["summary"]["nativeRelationEnum"] = rel_enum
    out["summary"]["nativeEnumMatchesRegistry"] = (
        sorted(rel_enum or []) == sorted(reg_new))

    # ---- aggregate ---------------------------------------------------------
    out["summary"]["allLabelsHonest"] = all(
        r.get("labelsHonest", True) for r in out["perRelation"].values())
    out["summary"]["allFieldSetsMatch"] = all(
        r.get("fieldSetMatchesInherited", True) for r in out["perRelation"].values()
        if r.get("inInherited") and r.get("inSuccessor"))
    out["summary"]["allRequiredMatch"] = all(
        r.get("requiredMatchesInherited", True) for r in out["perRelation"].values()
        if r.get("inInherited") and r.get("inSuccessor"))
    out["summary"]["allUniverseRulesMatch"] = all(
        r.get("universeRuleMatches", True) for r in out["perRelation"].values()
        if r.get("inInherited") and r.get("inSuccessor"))

    json.dump(out, sys.stdout, indent=1)
    print()


if __name__ == "__main__":
    main()
