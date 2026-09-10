#!/usr/bin/env python
"""P2 - M-3 regression: schema-valid two-rule policy where canonical object
order differs from ruleId order.

Blind finding M-3 showed set-reading and declared-order reading minted different
policyDigest. v6 claims PolicyDocumentV1/RuleProgramV1 `rules` are `ruleId`
ordered, never canonical rule-object order. This probe:
  1. builds two SCHEMA-VALID rules whose canonical-bytes order is the REVERSE of
     their ruleId order (so the two readings genuinely disagree),
  2. validates both orderings under the foundation ExactValidator with the real
     x-opensip-order keyword,
  3. shows exactly one ordering admits, so exactly one policyDigest exists.
Also checks RuleProgramV1 and WaiverSetV1, and that a generic `sequence` array
is NOT reordered (no uniqueItems / field-name heuristic).
"""
import json, os, sys, hashlib, importlib.util

DC = "/tmp/opensip-design-corrections/candidate-subject.v6/docs/coop/design-corrections"
sys.path.insert(0, os.path.join(DC, "foundation"))
spec = importlib.util.spec_from_file_location("canonical", os.path.join(DC, "foundation", "canonical.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)

POL = json.load(open(os.path.join(DC, "workflows/schemas/policy-document.schema.json")))

HEX = "a" * 64


def rule(rid, emit_when):
    return {
        "ruleId": rid,
        "ruleProgramRef": {"contributionId": "opensip.core", "ruleStableId": "r-" + rid,
                           "semanticsMajor": 1, "programDigest": HEX},
        "enabled": True, "severity": "warning", "gate": False,
        "subjectEnumeration": {"universe": "ts-universe", "subjectKind": "file"},
        "emitWhen": emit_when,
        "evidenceUse": [],
    }


# 'a.first' gets an emitWhen sorting LATE; 'b.second' gets one sorting EARLY,
# so canonical-object order is the reverse of ruleId order.
r_a = rule("a.first", {"kind": "exists"})
r_b = rule("b.second", {"kind": "count-at-most", "bound": 3})

by_rule_id = [r_a, r_b]
by_canonical = sorted([r_a, r_b], key=C.canonical)

out = {"probe": "P2-M3-policy-array-order"}
out["ruleIdOrder"] = [r["ruleId"] for r in by_rule_id]
out["canonicalObjectOrder"] = [r["ruleId"] for r in by_canonical]
out["orderingsGenuinelyDisagree"] = out["ruleIdOrder"] != out["canonicalObjectOrder"]

arr_schema = POL["$defs"]["PolicyDocumentV1"]["properties"]["rules"]
out["policyRulesAnnotation"] = arr_schema.get("x-opensip-order")


def try_order(schema, value):
    try:
        C.validate(schema, value)
        return {"admitted": True}
    except Exception as e:
        return {"admitted": False, "error": str(e).splitlines()[0][:160]}


# Validate ONLY the array against the annotated array schema (items $ref out of
# scope here; we test the order keyword, which is the finding).
order_only = {"type": "array", "x-opensip-order": arr_schema["x-opensip-order"]}
out["policyRules"] = {
    "ruleIdOrder": try_order(order_only, by_rule_id),
    "canonicalObjectOrder": try_order(order_only, by_canonical),
}
out["policyDigest_ruleIdOrder"] = hashlib.sha256(C.canonical(by_rule_id)).hexdigest()
out["policyDigest_canonicalOrder"] = hashlib.sha256(C.canonical(by_canonical)).hexdigest()
out["digestsDiffer"] = out["policyDigest_ruleIdOrder"] != out["policyDigest_canonicalOrder"]
out["exactlyOneAdmits"] = (out["policyRules"]["ruleIdOrder"]["admitted"] !=
                           out["policyRules"]["canonicalObjectOrder"]["admitted"])

# RuleProgramV1
rp = POL["$defs"]["RuleProgramV1"]["properties"]["rules"]
out["ruleProgramAnnotation"] = rp.get("x-opensip-order")
rp_only = {"type": "array", "x-opensip-order": rp["x-opensip-order"]}
prog = [{"ruleId": "a.first", "ruleProgramRef": {}, "emitWhen": {}},
        {"ruleId": "b.second", "ruleProgramRef": {}, "emitWhen": {}}]
out["ruleProgram"] = {"ruleIdOrder": try_order(rp_only, prog),
                      "reversed": try_order(rp_only, list(reversed(prog)))}

# WaiverSetV1
wv = POL["$defs"]["WaiverSetV1"]["properties"]["waivers"]
out["waiverAnnotation"] = wv.get("x-opensip-order")
wv_only = {"type": "array", "x-opensip-order": wv["x-opensip-order"]}
ws = [{"waiverId": "a1"}, {"waiverId": "b2"}]
out["waiverSet"] = {"waiverIdOrder": try_order(wv_only, ws),
                    "reversed": try_order(wv_only, list(reversed(ws)))}

# Generic encoder must NOT reorder a sequence array, must NOT use uniqueItems or
# field names as a heuristic, and must preserve nested arrays + repeated tokens.
seq = ["z", "a", "z"]
out["sequenceDefault"] = {
    "unannotated": try_order({"type": "array"}, seq),
    "uniqueItemsTrueButNoOrder": try_order({"type": "array", "uniqueItems": True}, ["z", "a"]),
    "explicitSequence": try_order({"type": "array", "x-opensip-order": "sequence"}, seq),
    "encoderPreservesOrder": C.canonical(seq) == b'["z","a","z"]',
    "encoderPreservesRepeatedTokens": C.canonical(["t", "t"]) == b'["t","t"]',
    "encoderPreservesNestedArrays": C.canonical([["b", "a"], ["d", "c"]]) == b'[["b","a"],["d","c"]]',
}
# A field literally named "rules"/"set" must get no special treatment.
out["noFieldNameSemantics"] = C.canonical({"rules": ["z", "a"], "set": ["z", "a"]}) == b'{"rules":["z","a"],"set":["z","a"]}'

# An unregistered annotation must refuse rather than silently pass.
out["unregisteredAnnotationRefuses"] = not try_order(
    {"type": "array", "x-opensip-order": "made-up"}, ["a"])["admitted"]

print(json.dumps(out, indent=1))
