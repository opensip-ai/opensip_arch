#!/usr/bin/env python
"""P10 - NEW finding: identity-bearing digest fields with no producing recipe.

v6 closed the ARRAY ordering law with an explicit closing default ("the closing
default for any array in a registered payload is an ordered sequence"). The
AUXILIARY DIGEST law has an enumeration plus class rules but NO closing default.
Five required 64-hex fields in identity-schemas.v2 fall outside both:

    programPredicateDigest  predicate-witness  -> witnessDigest -> proof2 -> run2
    parameterDigest         finding            -> finding2 -> evidence2 -> run2
    stageSpecDigest         execution-plan, cache-key
    outputSchemaDigest      cache-key
    inventoryDigest         commit-receipt

None is named in any of the five product contracts; none carries a schema
description. This probe demonstrates that two defensible readings of
programPredicateDigest diverge run2 for identical source, which is the exact
property FW-06 and identity 3 exist to prevent.
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

DC = Path("/tmp/opensip-design-corrections/candidate-subject.v6/docs/coop/design-corrections")
sys.path.insert(0, str(DC / "foundation"))


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


C = load("canon", DC / "foundation/canonical.py")
IM = load("idm", DC / "foundation/identity-model.py")
SCH = json.loads((DC / "foundation/identity-schemas.v2.json").read_text())

out = {"probe": "P10-auxiliary-digest-recipe-gap"}

# --- 1. establish the gap textually ------------------------------------------
CONTRACTS = Path("/tmp/opensip-design-corrections/candidate-subject.v6/docs/v2/contracts/product-v1")
prose = "".join(f.read_text() for f in sorted(CONTRACTS.glob("*.md")))
FIELDS = ["programPredicateDigest", "parameterDigest", "stageSpecDigest",
          "outputSchemaDigest", "inventoryDigest"]
# controls: fields that DO have an enumerated recipe
CONTROLS = ["resolvedConfigDigest", "scopeDigest", "analysisSpecDigest",
            "semanticGrantDigest", "vcsDigest"]


def described(field):
    hits = []

    def walk(n, path="$"):
        if isinstance(n, dict):
            for k, v in n.get("properties", {}).items():
                if k == field and isinstance(v, dict) and v.get("description"):
                    hits.append(v["description"])
            for k, v in n.items():
                walk(v, path + "/" + str(k))
        elif isinstance(n, list):
            for v in n:
                walk(v, path)
    walk(SCH)
    return hits


out["gapTable"] = {f: {"namedInAnyContract": f in prose,
                       "schemaDescription": described(f)} for f in FIELDS}
out["controlTable"] = {f: {"namedInAnyContract": f in prose} for f in CONTROLS}
out["allFiveUnnamed"] = not any(out["gapTable"][f]["namedInAnyContract"] for f in FIELDS)
out["allControlsNamed"] = all(out["controlTable"][f]["namedInAnyContract"] for f in CONTROLS)

# --- 2. the divergence, through the real identity model ----------------------
# One compiled predicate program record, three defensible readings of its digest.
predicate_program = {"operation": "none", "relation": "references",
                     "field": "target", "value": "foo"}

readings = {
    "rawSha256OfCanonicalRecord":
        hashlib.sha256(C.canonical(predicate_program)).hexdigest(),
    "H_rule_program_domain": None,
    "rawSha256OfCompiledProgramTextForm":
        hashlib.sha256(json.dumps(predicate_program, sort_keys=True,
                                  separators=(",", ":")).encode()).hexdigest(),
}
# H over a non-registered domain may refuse; fall back to the frame directly
if readings["H_rule_program_domain"] is None:
    c = C.canonical(predicate_program)
    readings["H_rule_program_domain"] = hashlib.sha256(
        b"opensip.product.v1\x00rule-program\x00"
        + len(c).to_bytes(8, "big") + c).hexdigest()

out["readingsOfProgramPredicateDigest"] = readings
out["readingsAllDistinct"] = len(set(readings.values())) == len(readings)

FACT = "fact2:" + "1" * 64
COV = "coverage2:" + "2" * 64


def witness_for(digest):
    return {"schemaVersion": 2, "programPredicateDigest": digest,
            "matchingFactIds": [FACT], "coverageIds": [COV],
            "countLimit": None, "childPredicateIds": []}


chain = {}
for label, dg in readings.items():
    w = witness_for(dg)
    C.validate(dict(SCH, **{"$ref": "#/$defs/predicate-witness"}), w)
    wd = hashlib.sha256(C.canonical(w)).hexdigest()          # witnessDigest: raw SHA256
    proof = IM.identifier("proof-bundle", {
        "schemaVersion": 2, "planId": "plan2:" + "a" * 64,
        "executionPlanId": "exec-plan2:" + "c" * 64,
        "evaluatorClosure": "closure2:" + "d" * 64,
        "ruleProgramDigest": "e" * 64,
        "evaluationInputRefs": [{"domain": "view", "digest": "b" * 64}],
        "predicateProofs": [{"ruleId": "r.one", "subjectId": "s",
                             "predicateId": "p", "operation": "none",
                             "inputRefs": [], "scopeIds": [],
                             "value": "true", "witnessDigest": wd}],
        "findingIds": [], "verdict": "pass"})
    chain[label] = {"programPredicateDigest": dg, "witnessDigest": wd,
                    "proof2": proof}

out["propagation"] = chain
out["proof2AllDistinct"] = len({v["proof2"] for v in chain.values()}) == len(chain)
out["conclusion"] = ("Identical source and identical compiled predicate yield "
                     + str(len({v['proof2'] for v in chain.values()}))
                     + " different proof2 values under defensible readings; "
                       "proof2 enters evidence2 -> seal2 -> run2.")
print(json.dumps(out, indent=1))
