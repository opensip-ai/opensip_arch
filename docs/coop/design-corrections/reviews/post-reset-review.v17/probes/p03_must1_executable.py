#!/usr/bin/env python
"""CB6-MUST-1 executable boundary probe, run inside the disposable copy.

Exercises the ACTUAL consumer (workflows_model.admit_evidence_requirement)
against the ACTUAL owning schema (repair.schema.json EvidenceRequirement) over
the full cross-product of planes and vocabularies, and asserts the two
boundaries deciding one law AGREE on every case.

Also exercises the ACTUAL native producer (native_evidence_model.sufficiency_v2)
to establish that the four outcomes blind v6 named inexpressible are now
produced, carried and admitted LOSSLESSLY, and that satisfied positives remain
usable.

Every expectation is authored here from the published law, not from the
candidate's own report.
"""
import importlib.util
import json
import os
import sys
from pathlib import Path

COPY = sys.argv[1]
OUT = sys.argv[2]
DC = Path(COPY) / "docs/coop/design-corrections"
sys.path.insert(0, str(DC / "foundation"))
import canonical  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402
from referencing import Registry, Resource  # noqa: E402
from referencing.jsonschema import DRAFT202012  # noqa: E402


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


M = load("workflows_model", DC / "workflows/workflows_model.v1.py")
N = load("native_model", DC / "native/native_evidence_model.v2.py")

# --- schema registry, exactly as the owning checker builds it ---
import glob
SCHEMAS = {}
for p in sorted(glob.glob(str(DC / "workflows/schemas/*.schema.json"))):
    s = canonical.parse(Path(p).read_bytes())
    SCHEMAS[s["$id"]] = s
FOUND = canonical.parse((DC / "foundation/identity-schemas.v2.json").read_bytes())
REG = Registry().with_resources(
    [(k, Resource(contents=v, specification=DRAFT202012)) for k, v in SCHEMAS.items()]
    + [(FOUND["$id"], Resource(contents=FOUND, specification=DRAFT202012))])
REPAIR = SCHEMAS["urn:opensip:product-v1:workflows:repair"]
ER_VALIDATOR = Draft202012Validator(
    {"$ref": "urn:opensip:product-v1:workflows:repair#/$defs/EvidenceRequirement"},
    registry=REG)

rep = {"probe": "p03-must1-executable", "copy": COPY}
results = []


def schema_ok(rec):
    return not list(ER_VALIDATOR.iter_errors(rec))


def consumer(rec):
    """Return ('ADMIT', plane, value) or ('REFUSE', errclass, key)."""
    try:
        plane, val = M.admit_evidence_requirement(rec)
        return ("ADMIT", plane, val)
    except Exception as e:
        cls = getattr(e, "code", None) or getattr(e, "error_class", None)
        # Refusal signature varies; capture its string form
        return ("REFUSE", type(e).__name__ + ":" + str(getattr(e, "args", ("",))[0]),
                str(e))


def case(cid, rec, expect, why):
    """expect: 'ADMIT' or 'REFUSE' - my OWN expectation from the published law."""
    c = consumer(rec)
    s = schema_ok(rec)
    got = c[0]
    agree = (got == "ADMIT") == s
    results.append({
        "id": cid,
        "record": rec,
        "myExpectation": expect,
        "consumerOutcome": got,
        "consumerDetail": c[1] if got == "REFUSE" else {"plane": c[1], "value": c[2]},
        "schemaValid": s,
        "consumerMatchesMyExpectation": got == expect,
        "consumerAndSchemaAgree": agree,
        "why": why,
    })


# ---- 0. vocabulary joins (the drift risk) ----
law = M.IMPORTED_REQUIREMENT_LAW
common = SCHEMAS["urn:opensip:product-v1:workflows:common"]
native_schema = canonical.parse(
    (DC / "native/native-evidence.schemas.v2.json").read_bytes())
joins = {
    "modelNativeVocabReadFromDeficiencyV2":
        list(M.NATIVE_SUFFICIENCY_DEFICIENCIES)
        == list(native_schema["$defs"]["DeficiencyV2"]["enum"]),
    "modelNativeVocabEqualsCommonDef":
        set(M.NATIVE_SUFFICIENCY_DEFICIENCIES)
        == set(common["$defs"]["NativeSufficiencyDeficiency"]["enum"]),
    "modelImportedVocabFromPrecedence": list(M.IMPORTED_REQUIREMENT_DEFICIENCIES),
    "lawPrecedenceEqualsLawOutcomes":
        set(law["precedence"]) == set(law["outcomes"]),
    "lawOutcomesEqualCommonImportedEnum":
        set(law["outcomes"])
        == set(common["$defs"]["ImportedRequirementDeficiency"]["enum"]),
    "modelImportedEqualsCommonImportedEnum":
        set(M.IMPORTED_REQUIREMENT_DEFICIENCIES)
        == set(common["$defs"]["ImportedRequirementDeficiency"]["enum"]),
    "perKindApplicabilityRelations": sorted(law["perKindApplicability"]),
    "importedRegistryRelations": sorted(M.EVIDENCE_RELATIONS),
    "perKindCoversEveryImportedRelation":
        set(law["perKindApplicability"]) == set(M.EVIDENCE_RELATIONS),
    "everyPerKindOutcomeIsInTheImportedVocabulary": all(
        set(v) <= set(law["outcomes"]) for v in law["perKindApplicability"].values()),
    "unionOfPerKindEqualsWholeImportedVocabulary":
        set().union(*law["perKindApplicability"].values()) == set(law["outcomes"]),
}
rep["vocabularyJoins"] = joins

NATIVE_V = list(M.NATIVE_SUFFICIENCY_DEFICIENCIES)
IMP_V = list(M.IMPORTED_REQUIREMENT_DEFICIENCIES)
IMPORTED_RELATIONS = sorted(M.EVIDENCE_RELATIONS)
NATIVE_RELATIONS = sorted(
    r for r in M.RELATION_LADDERS if r not in M.EVIDENCE_RELATIONS)
rep["nativeRelations"] = NATIVE_RELATIONS
rep["importedRelations"] = IMPORTED_RELATIONS


def base(rel, satisfied, deficiency=..., rung=None):
    r = {"relation": rel,
         "minResolution": rung or M.RELATION_LADDERS[rel][0],
         "completeness": "complete",
         "satisfied": satisfied}
    if deficiency is not ...:
        r["deficiency"] = deficiency
    return r


# ---- 1. native plane: every native outcome admits on every native relation ----
for rel in NATIVE_RELATIONS:
    for d in NATIVE_V:
        case("N-admit/%s/%s" % (rel, d), base(rel, False, d), "ADMIT",
             "a native relation carrying its own plane's outcome must admit")

# ---- 2. native relation carrying an IMPORTED outcome must refuse (cross-plane) ----
for rel in NATIVE_RELATIONS[:4]:
    for d in IMP_V:
        case("N-crossplane/%s/%s" % (rel, d), base(rel, False, d), "REFUSE",
             "cross-plane value on a native relation is a category error")

# ---- 3. imported plane: per-KIND applicability decides, not merely per-plane ----
for rel in IMPORTED_RELATIONS:
    applicable = set(law["perKindApplicability"][rel])
    for d in IMP_V:
        exp = "ADMIT" if d in applicable else "REFUSE"
        case("I-perkind/%s/%s" % (rel, d), base(rel, False, d), exp,
             "the consumer must decide the SAME per-kind law the producer does")
    for d in NATIVE_V:
        case("I-crossplane/%s/%s" % (rel, d), base(rel, False, d), "REFUSE",
             "native outcome on an imported relation is a category error")

# ---- 4. presence / typing law, both branches ----
rel0 = NATIVE_RELATIONS[0]
imp0 = IMPORTED_RELATIONS[0]
case("P-satisfied-no-key", base(rel0, True), "ADMIT",
     "POSITIVE CONTROL: a satisfied requirement with no deficiency key admits")
case("P-satisfied-with-value", base(rel0, True, NATIVE_V[0]), "REFUSE",
     "deficiency FORBIDDEN when satisfied is true")
case("P-satisfied-explicit-null", base(rel0, True, None), "REFUSE",
     "a present key with a null value is not an absent key")
case("P-unsatisfied-no-key", base(rel0, False), "REFUSE",
     "deficiency REQUIRED when satisfied is false")
case("P-unsatisfied-explicit-null", base(rel0, False, None), "REFUSE",
     "explicit null is not an outcome in the failing branch either")
case("P-satisfied-int-1", base(rel0, 1), "REFUSE",
     "satisfied must be an actual bool; 1 is not True here")
case("P-satisfied-int-0-with-value", base(rel0, 0, NATIVE_V[0]), "REFUSE",
     "0 is not False; truthiness must not decide the branch")
case("P-satisfied-string", base(rel0, "false", NATIVE_V[0]), "REFUSE",
     "a string is not a boolean")
case("P-unknown-value", base(rel0, False, "not-a-real-outcome"), "REFUSE",
     "a value in neither vocabulary refuses")
case("P-imported-satisfied-positive", base(imp0, True), "ADMIT",
     "POSITIVE CONTROL: imported plane satisfied requirement admits")

# ---- 5. the four formerly-inexpressible outcomes, produced by the REAL producer ----
FOUR = ["derivation-policy-unmet", "external-consumers-unknown",
        "input-closure-incomplete", "resolution-incomplete"]
producer_cases = []

def view_entry(**kw):
    e = {"resolution": "enumerated", "coverage": "complete",
         "confidenceMillionths": 1000000,
         "resolutionCompleteness": {"state": "complete",
                                    "unresolvedEdgeCount": 0,
                                    "unresolvedEdgeClasses": []},
         "closedWorld": {"exportsClosed": "closed"}}
    e.update(kw)
    return e

# resolution-incomplete: universal-negative over a partial resolution state
try:
    req = {"relation": "references", "minResolution":
           M.RELATION_LADDERS["references"][0], "completeness": "partial-ok",
           "quantifier": "universal-negative", "unresolvedEdgePolicy": "forbid"}
    view = {"references": view_entry(
        resolution=M.RELATION_LADDERS["references"][0],
        resolutionCompleteness={"state": "partial", "unresolvedEdgeCount": 2,
                                "unresolvedEdgeClasses": ["dynamic-import"]})}
    r = N.sufficiency_v2(req, view)
    producer_cases.append({"target": "resolution-incomplete", "result": r,
                           "producedExpected": r.get("deficiency") == "resolution-incomplete"})
except Exception as e:
    producer_cases.append({"target": "resolution-incomplete",
                           "error": type(e).__name__ + ": " + str(e)})

# external-consumers-unknown: universal-negative, exported target, exports not closed
try:
    req = {"relation": "references", "minResolution":
           M.RELATION_LADDERS["references"][0], "completeness": "partial-ok",
           "quantifier": "universal-negative", "externalConsumerPolicy": "forbid"}
    view = {"references": view_entry(
        resolution=M.RELATION_LADDERS["references"][0],
        closedWorld={"exportsClosed": "open"})}
    r = N.sufficiency_v2(req, view, target_exported=True)
    producer_cases.append({"target": "external-consumers-unknown", "result": r,
                           "producedExpected":
                               "external-consumers-unknown" in r.get("causes", [])})
except Exception as e:
    producer_cases.append({"target": "external-consumers-unknown",
                           "error": type(e).__name__ + ": " + str(e)})

# derivation-policy-unmet: types relation, declared-only, compiler-inferred present
try:
    req = {"relation": "types", "minResolution": M.RELATION_LADDERS["types"][0],
           "completeness": "partial-ok", "derivationPolicy": "declared-only"}
    view = {"types": view_entry(resolution=M.RELATION_LADDERS["types"][0],
                                derivationKinds=["compiler-inferred"])}
    r = N.sufficiency_v2(req, view)
    producer_cases.append({"target": "derivation-policy-unmet", "result": r,
                           "producedExpected":
                               "derivation-policy-unmet" in r.get("causes", [])})
except Exception as e:
    producer_cases.append({"target": "derivation-policy-unmet",
                           "error": type(e).__name__ + ": " + str(e)})

# input-closure-incomplete: carried by the entry's own deficiency under complete
try:
    req = {"relation": "references",
           "minResolution": M.RELATION_LADDERS["references"][0],
           "completeness": "complete"}
    view = {"references": view_entry(
        resolution=M.RELATION_LADDERS["references"][0],
        coverage="partial", deficiency="input-closure-incomplete")}
    r = N.sufficiency_v2(req, view)
    producer_cases.append({"target": "input-closure-incomplete", "result": r,
                           "producedExpected":
                               "input-closure-incomplete" in r.get("causes", [])})
except Exception as e:
    producer_cases.append({"target": "input-closure-incomplete",
                           "error": type(e).__name__ + ": " + str(e)})

rep["producerCases"] = producer_cases

# Now carry each produced value into a real EvidenceRequirement and admit it.
for pc in producer_cases:
    v = pc.get("target")
    case("ROUNDTRIP-%s" % v, base("references", False, v), "ADMIT",
         "LOSSLESS: the producer's own outcome must be carriable and admissible")

# ---- 6. a copied boolean alone is not authorization ----
copied_bool_only = {"relation": rel0,
                    "minResolution": M.RELATION_LADDERS[rel0][0],
                    "completeness": "complete", "satisfied": True}
rep["copiedBooleanAloneNote"] = {
    "record": copied_bool_only,
    "schemaValid": schema_ok(copied_bool_only),
    "consumerAdmits": consumer(copied_bool_only)[0],
    "butThisIsNotAuthorization":
        "admit_evidence_requirement returns (plane, None) and grants nothing; "
        "authorization is asserted separately and is probed in p06.",
}

rep["cases"] = results
rep["caseCount"] = len(results)
rep["casesMatchingMyExpectation"] = sum(
    1 for r in results if r["consumerMatchesMyExpectation"])
rep["disagreementsWithMyExpectation"] = [
    r for r in results if not r["consumerMatchesMyExpectation"]]
rep["consumerSchemaDisagreements"] = [
    r for r in results if not r["consumerAndSchemaAgree"]]
rep["admitCount"] = sum(1 for r in results if r["consumerOutcome"] == "ADMIT")
rep["refuseCount"] = sum(1 for r in results if r["consumerOutcome"] == "REFUSE")

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("vocabulary joins:")
for k, v in joins.items():
    print("  %-46s %s" % (k, json.dumps(v)[:120]))
print()
print("cases:", rep["caseCount"], "admit:", rep["admitCount"],
      "refuse:", rep["refuseCount"])
print("matching my expectation:", rep["casesMatchingMyExpectation"])
print("DISAGREEMENTS with my expectation:",
      len(rep["disagreementsWithMyExpectation"]))
for d in rep["disagreementsWithMyExpectation"][:15]:
    print("   ", d["id"], "expected", d["myExpectation"], "got",
          d["consumerOutcome"], "|", str(d["consumerDetail"])[:150])
print("consumer/schema DISAGREEMENTS:", len(rep["consumerSchemaDisagreements"]))
for d in rep["consumerSchemaDisagreements"][:15]:
    print("   ", d["id"], "consumer", d["consumerOutcome"], "schemaValid",
          d["schemaValid"])
print()
print("producer cases:")
for pc in producer_cases:
    print("  ", pc.get("target"), "->",
          json.dumps(pc.get("result", pc.get("error")))[:200])
