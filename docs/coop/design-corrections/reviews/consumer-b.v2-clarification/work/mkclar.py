"""Assemble clarification.json from the executed probe. Writes only under
/tmp/opensip-design-corrections/consumer-b.v2-clarification."""

import json
import os

OUT = "/tmp/opensip-design-corrections/consumer-b.v2-clarification"
ORIG = "/tmp/opensip-design-corrections/consumer-b.v2"

probe = json.load(open(os.path.join(OUT, "clarification-probe.json")))
orig_gaps = json.load(open(os.path.join(ORIG, "output", "gaps.json")))
orig_review = json.load(open(os.path.join(ORIG, "output", "blind-review.json")))
g8 = [f for f in orig_gaps["findings"] if f["id"] == "G8"][0]

d = probe["discriminatingCheck"]
fs = probe["frozenSubschema"]
res = probe["residualBudgetObservation"]

doc = {
    "artifact": "opensip.blind-review.consumer-b.v2.clarification",
    "kind": "bounded factual clarification of ONE finding",
    "isNewWholeReview": False,
    "isAcceptanceOfAnySuccessor": False,
    "authorImplementationCodeSupplied": False,
    "date": "2026-09-06",
    "reviewer": "actual Claude, the same blind consumer B (v2) who produced the "
                "frozen v7 CHANGES_REQUIRED review",

    "originalFindingReference": {
        "review": os.path.join(ORIG, "output", "blind-review.json"),
        "retainedImmutableAt": "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/"
                               "design-corrections/reviews/consumer-b.v2/",
        "findingId": "G8",
        "reportedInNarrativeAs": "S-4",
        "originalSeverity": g8["severity"],
        "originalStatement": g8["statement"],
        "originalObservedPlanBudgetSchema": g8["observed"]["planBudgetSchema"],
        "alsoCorrects": [
            "blind-review.json invented[] row 'plan.budget = {unit: work-units, "
            "limit: 100000}'",
            "blind-review.md section 7 closing clause 'an unconstrained object "
            "inside a PlanId'",
        ],
    },

    "inputCustody": probe["inputCustody"],

    "outcome": "RETRACTED",
    "outcomeStatement": "G8 / S-4 is erroneous and is retracted in full. Every "
                        "factual claim it makes is false against the frozen bytes. "
                        "plan.budget is a CLOSED unit/limit record.",

    "frozenBytes": {
        "selector": probe["inputCustody"]["selector"],
        "planBudgetSchema": fs["planBudgetSchema"],
        "isClosed": fs["planBudgetIsClosed"],
        "required": fs["planBudgetRequired"],
        "unitConst": fs["planBudgetUnitConst"],
        "limitBounds": fs["planBudgetLimitBounds"],
        "byteIdenticalToSemanticConfigurationAnalysisBudget":
            fs["twoSubschemasAreByteIdentical"],
    },

    "claimVsBytes": [
        {"g8Claimed": "a bare {\"type\": \"object\"}",
         "frozenBytes": "a closed record with type, additionalProperties, required "
                        "and properties"},
        {"g8Claimed": "no additionalProperties",
         "frozenBytes": "additionalProperties: false"},
        {"g8Claimed": "no required keys",
         "frozenBytes": "required: [unit, limit]"},
        {"g8Claimed": "the shape exists in the configuration; the Plan just does "
                      "not reference it",
         "frozenBytes": "the Plan carries a byte-identical copy of that shape inline"},
    ],

    "discriminatingCheck": {
        "validatedAgainst": d["validatedAgainst"],
        "casesTotal": d["casesTotal"],
        "casesAgreeing": d["casesAgreeingWithExpectation"],
        "disagreements": d["disagreements"],
        "cases": [{"case": r["case"], "observed": r["observed"],
                   "expected": r["expected"], "agrees": r["agrees"]}
                  for r in d["cases"]],
        "lexicalAdmissionPrecedingSchema": d["lexicalAdmissionPrecedingSchema"],
        "independentlyReproducesCodexResult": True,
    },

    "rootCause": {
        "what": "An early exploratory dump helper extracted only a whitelist of "
                "schema keywords (type, const, enum, pattern, minimum, maximum, "
                "x-opensip-digest, x-opensip-order, $ref, maxLength, minItems, "
                "maxItems). It did not extract required, additionalProperties or "
                "nested properties, so budget rendered as {\"type\": \"object\"}. "
                "The finding's statement was written from that truncated rendering.",
        "aggravating": "gaps.py::g8 later dumped the COMPLETE subschema into "
                       "observed.planBudgetSchema, so the finding shipped "
                       "self-refuting on its face: its own evidence field, in the "
                       "same JSON object, already showed additionalProperties:false "
                       "and required:[unit,limit]. I built the probe to carry the "
                       "observed bytes so a reader could check the claim, then did "
                       "not check it myself.",
        "classification": "reviewer process failure, not a disagreement about the "
                          "design",
    },

    "correctedCounts": {
        "mustBefore": 4, "mustAfter": 4,
        "shouldBefore": 6, "shouldAfter": 5,
        "advisoryBefore": 1, "advisoryAfter": 2,
        "openDesignGapsBefore": 10, "openDesignGapsAfter": 9,
        "note": "advisoryAfter counts A-1 plus the newly recorded ADV-B1.",
    },

    "newObservation": {
        "id": "ADV-B1",
        "severity": "advisory",
        "title": "The Plan commits two independent copies of the budget",
        "exactSelectors": res["exactSelectors"],
        "observation": res["observation"],
        "reproducer": res["reproducer"],
        "countervailingReading": res["countervailingReading"],
        "doesNotRestoreG8": True,
        "suggestedClosure": "One sentence either way: add 'and Plan budget' to "
                            "identity-and-evidence section 3's closure agreement "
                            "list, or state that plan.budget is a per-invocation "
                            "narrowing that may differ from the configured budget.",
    },

    "consideredAndNotRaised": [{
        "candidate": "identity-and-evidence section 4 names a 'deterministic work "
                     "bound ... for each predicate' and 'the rule program's "
                     "admitted work bound', while "
                     "policy-document.schema.json#/$defs/RuleProgramV1 carries no "
                     "work-bound field (schemaVersion, policyDigest, rules only) "
                     "and Atom.n is a count-at-most threshold.",
        "whyNotRaised": "workflows-and-surfaces.md section 5 supplies real "
                        "schema-enforced structural bounds (depth <= 8, <= 64 nodes "
                        "per rule, <= 512 rules), so the DAG IS bounded and the "
                        "phrase reads naturally as those admitted caps. Raising it "
                        "would be a conjecture about wording, not a reproducible "
                        "defect.",
    }],

    "untouchedFindings": {
        "must": ["M-1 (G1) payload schema document law",
                 "M-2 (G2) fact payload encoder and schema document",
                 "M-3 (G3) resolvedNodeModulesLayout",
                 "M-4 (G5) tsconfigGraphHash"],
        "should": ["S-1 (G4)", "S-2 (G6)", "S-3 (G7)", "S-5 (G9)", "S-6 (G10)"],
        "advisory": ["A-1 (G11)", "A-2", "A-3"],
        "confirmation": ["G12"],
        "statement": "Not re-examined in this bounded clarification. None of them "
                     "depends on G8.",
    },

    "verdict": {
        "overall": "CHANGES_REQUIRED",
        "unchanged": True,
        "basis": "The four MUST findings, which this clarification does not "
                 "revisit. The verdict is NOT changed merely because G8 was "
                 "erroneous, and it was never carried by G8.",
    },

    "claimsExplicitlyNotMade": [
        "no readiness grade or regrade",
        "no product qualification",
        "no implementation authorization",
        "no acceptance of any successor",
        "no commit, push, or access to current author changes",
    ],

    "custodyOfOriginals": {
        "originalKitReVerifiedAfterThisWork": "43/43 exact, 0 mismatches",
        "originalKitEdited": False,
        "originalOutputOrReviewEdited": False,
        "originalWorkFilesEdited": False,
        "originalToolsUsed": "imported read-only from output/work; their mains were "
                             "never run",
    },

    "newOutputs": {
        "clarification.md": "this clarification, narrative",
        "clarification.json": "this record",
        "clarification-probe.json": "executed probe output",
        "work/budget_probe.py": "the probe source",
        "work/mkclar.py": "this assembler",
    },
}

with open(os.path.join(OUT, "clarification.json"), "w") as fh:
    json.dump(doc, fh, indent=1)
    fh.write("\n")

print("outcome:", doc["outcome"])
print("matrix: %d/%d agree, disagreements=%s"
      % (doc["discriminatingCheck"]["casesAgreeing"],
         doc["discriminatingCheck"]["casesTotal"],
         doc["discriminatingCheck"]["disagreements"]))
print("counts:", doc["correctedCounts"])
print("verdict:", doc["verdict"]["overall"], "unchanged:", doc["verdict"]["unchanged"])
