#!/usr/bin/env python3
"""Assemble assessment.json from the recorded probe receipts."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent
RC = H / "probes" / "receipts"


def j(label):
    return json.loads((RC / label / "stdout.txt").read_text())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


q1, q2, q3, q4 = j("q1-normative-clauses"), j("q2-enum-context"), j("q3-enum-membership"), j("q4-records-vs-95")
S = Path("/tmp/opensip-design-corrections/candidate-subject.v33/docs/coop/design-corrections")
LIVE = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/"
            "consumer-b.v20/final-public-artifact-manifest.json")

out = {
    "standing": "READ-ONLY bounded normative-publication check by the source-author origin "
                "823bf66b-... NOT independent review, NOT blind acceptance, NO acceptance of any "
                "kind. No source edit, no consumer contact, no remint, no freeze.",
    "question": "Is the outgoing missing-relation-coverage vs selector-unbound choice determined "
                "from published clauses alone, without atom_model.v1.py? And is the outgoing "
                "native-completeness branch publishable as one clarification?",
    "normativeOnlyKit": {
        "fileCount": q1["kitFileCount"], "roots": q1["kitRoots"], "excluded": q1["excluded"],
        "note": "All reference Python excluded, per root: a consumer must derive proof causes from "
                "published clauses alone.",
    },
    "rootObjectionAccepted": {
        "objection": "A binding is not itself Coverage; absent a normative discriminator the "
                     "spelling of a cause cannot establish its meaning. Code results alone cannot "
                     "settle a missing normative choice.",
        "myPriorClaim": "RC-3: missing-relation-coverage is 'factually wrong regardless of any "
                        "publication question'.",
        "howIReachedIt": "via atom_model.v1.py:1437, which is reference Python outside the "
                         "normative-only kit.",
        "verdict": "RETRACTED. The objection is correct.",
    },
    "censusOfDisputedCauses": {
        "hitCounts": q1["hitCounts"],
        "missingRelationCoverageOccurrences": q1["hits"]["missing-relation-coverage"],
        "selectorUnboundOccurrences": q1["hits"]["selector-unbound"],
        "everyOccurrenceIsBareEnumMembership": True,
        "owningRegistry": {
            "selector": "foundation/identity-schemas.v3.json#/x-opensip-evaluator-deficiency-registry",
            "sourcesAreFlatStringLists": q2["evaluatorDeficiencyRegistry"]["sourcesIsFlatStringLists"],
            "anyPerCauseConditionObject": q2["evaluatorDeficiencyRegistry"]["anyPerCauseConditionObject"],
            "causeLaw": q2["evaluatorDeficiencyRegistry"]["causeLaw"],
        },
        "atomCauseCodeV1Description": q3["atomCauseCodeV1Description"],
        "conclusion": "No clause in the normative-only kit states the emission condition for "
                      "either cause.",
    },
    "twoRecordsConsistentWithProse": {
        "input": "syntax-code, relation unresolved-edge, capability unresolved-edge: one owed "
                 "binding with universe null; no Coverage for that relation at that rung.",
        "eliminatedByProse": {
            "cause": "unavailable-program-binding",
            "selector": "atom-evaluation-contract.v1.md:74",
            "quote": "unavailable-program-binding is an incoming/global search concern",
        },
        "notApplicable": {
            "cause": "scope-without-coverage",
            "selector": "atom-evaluation-contract.v1.md:74",
            "why": "conditioned on a CONTAINING scope without a paired Coverage; here no "
                   "containing scope exists.",
        },
        "consistentCandidates": [
            {"cause": "missing-relation-coverage", "reading": "no Coverage exists for this relation"},
            {"cause": "selector-unbound", "reading": "no available binding at the subject universe"},
            {"cause": "uncovered-expected-source-subject",
             "reading": "the expected source subject is uncovered", "strength": "arguable"},
        ],
        "determinedWithoutReferencePython": False,
        "classification": "GENUINE NORMATIVE UNDERSPECIFICATION",
    },
    "whatIsFullyPublished": {
        "causesVsNativeDeficienciesDiscriminator": {
            "selectors": ["atom-evaluation-contract.v1.md:137",
                          "evaluator-projection-registry.v1.json#/$defs/AtomCauseCodeV1.description"],
            "atomCauseCodeV1Size": q3["atomCauseCodeV1Size"],
            "deficiencyV2Size": q3["deficiencyV2Size"],
            "intersection": q3["inBothEnums"],
            "partitionsCleanly": q3["discriminatorPartitionsCleanly"],
            "perCode": q3["perCode"],
            "rootQuestionAnswered":
                "RC-1 bound check: coverage-unknown is an AtomCauseCodeV1 member and NOT a "
                "DeficiencyV2 member, so it belongs in atom causes. The reference is consistent "
                "with published law on that axis; NO reference correction is indicated there.",
        },
        "recordFieldDerivation": {
            "selector": "evaluator-composition-contract.v3.md section 9.5 items 1-3",
            "channels": ["atom causes[]", "atom nativeDeficiencies[] (DeficiencyV2)",
                         "per-Coverage entry.deficiency"],
            "complete": True,
        },
        "measuredRecordTest": {
            "disputedRecordCount": q4["disputedRecordCount"],
            "everyDisputedRecordIsSection95ShapeLegal":
                q4["everyDisputedRecordIsSection95ShapeLegal"],
            "channelsUsed": q4["channelsUsed"],
            "syntaxCode": q4["syntax-code"],
            "rustPartial": q4["rust-partial"],
            "conclusion": "Shape is published and both sides obey it. The disagreement is entirely "
                          "in the atom causes[] CONTENT - the unpublished part.",
        },
    },
    "branchBoundCheck": {
        "published": [
            {"point": "partition pairing (containment; subject_scope_commitment or coverageScopes; "
                      "no fallback)", "selector": "atom §4 L74"},
            {"point": "containing scope without paired Coverage -> scope-without-coverage, "
                      "accumulating", "selector": "atom §4 L74"},
            {"point": "unavailable-program-binding excluded outgoing", "selector": "atom §4 L74"},
            {"point": "cross-family unavailable -> cross-family-edge-not-owed, non-blocking",
             "selector": "atom §4 L74, L92"},
            {"point": "recursive DEPENDS_ON in the sufficiency view; all su.causes retained",
             "selector": "atom §4 L88"},
            {"point": "causes vs nativeDeficiencies array",
             "selector": "atom §7 L137; AtomCauseCodeV1.description"},
            {"point": "record field derivation, all three channels",
             "selector": "composition §9.5 items 1-3"},
        ],
        "unpublished": [
            "cause when no owed binding exists / no available binding at U",
            "cause when no containing scope exists at all",
            "cause when sufficiency is unsatisfied (coverage-unknown), and its nativeCause/universe",
            "branch order: early-return vs accumulate",
        ],
        "whyOneClarificationSuffices":
            "All four omissions are in a single branch (endpoint=source native completeness), so "
            "one ordered table closes them together rather than fixing causes one at a time.",
        "observableOrderingConsequence":
            "syntax-code rule.unresolved-edge-advisory: consumer 4 records, reference 2, 1 shared.",
        "noMeasuredReferenceInstance":
            ["missing-relation-coverage", "uncovered-expected-source-subject"],
    },
    "effectOnPriorFindings": {
        "RC-1-coverageIds": "UNCHANGED consumer violation (atom §4 L88 explicit; root agrees)",
        "RC-1-coverageUnknownRecord": "SPLIT OUT as underspecified",
        "RC-2": "Underspecified for the 'no containing scope' branch; the L74 pairing rule it "
                "rests on remains published",
        "RC-3": "RETRACTED - genuine underspecification, not a consumer violation",
        "RC-4": "UNCHANGED consumer violation (composition L121; root agrees)",
        "RC-6": "STRENGTHENED - composition L44 and L261 publish the count law exactly: counts = "
                "distinct union of descendant atom KNOWN matches (not uncertain)",
    },
    "sourceConclusion": {
        "amendmentRequired": True,
        "kind": "publication gap, not a semantic defect",
        "referenceCorrectionIndicated": False,
        "referenceCorrectionBasis": "The reference's behaviour is self-consistent and this check "
                                    "found no point where it contradicts explicit law.",
        "draft": "amendment-draft.md",
        "placement": "atom-evaluation-contract.v1.md section 4, immediately after the Outgoing "
                     "paragraph (line 74), before Incoming owed programs (line 76)",
        "noNewSemantics": "No new cause name, no new field; only the selection and order needed to "
                          "make the existing branch derivable.",
    },
    "independentSemanticDecisionsRequiringReview": [
        "Whether 'no owed binding at all' and 'no available binding at U' are one cause or two.",
        "Which cause the second takes; the two names are near-synonyms on their face.",
        "Whether the branch short-circuits or accumulates (changes record cardinality).",
        "The nativeCause carried by coverage-unknown, and which view entry supplies it when "
        "several could (measured reference value: body-language-owner-unenumerated).",
        "Whether uncovered-expected-source-subject carries universe U or null.",
    ],
    "correctionsToMyPriorDiagnosis": {
        "S-3": {
            "withdrawn": True,
            "why": "rested on an invented key-name search ('aggregateTermination'), not on actual "
                   "envelope fields. It establishes nothing. Root holds exact final20 "
                   "multistep/termination controls and owns that assessment; I make no claim.",
        },
        "publicManifestPath": {
            "myPriorObservation": "consumer-b.v20/final-public-artifact-manifest.json does not "
                                  "exist - that was the RUNTIME path.",
            "actualLiveRetention": str(LIVE),
            "exists": LIVE.is_file(),
            "sha256": sha(LIVE) if LIVE.is_file() else None,
            "bytes": LIVE.stat().st_size if LIVE.is_file() else None,
            "correction": "My earlier observation was a wrong path on my part and must NOT be "
                          "relabelled as absent retention.",
        },
    },
    "limits": [
        "No acceptance of any kind. Not the independent reviewer, not the blind consumer.",
        "No suite was re-run and the five proofs were not re-derived; the record test uses the "
        "preserved root derivation.",
        "I read the atom contract in full plus targeted composition sections and the registries. "
        "'No clause anywhere' is scoped to the 169-file normative-only kit and the eight cause "
        "tokens censused; I did not re-read the whole charter or native chapter.",
        "Array placement inside the consumer's atom result is NOT observable from "
        "ruleResults[].deficiencies, where section 9.5 merges all three channels; I make no claim "
        "about the consumer's internal placement.",
        "missing-relation-coverage and uncovered-expected-source-subject have no measured "
        "reference instance, so the amendment's fields for them are proposals, not observations.",
        "The amendment is a DRAFT in this runtime. Source33 is untouched and nothing is frozen.",
    ],
    "acceptance": None,
}

(H / "assessment.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
print(json.dumps({
    "kitFiles": out["normativeOnlyKit"]["fileCount"],
    "rc3": out["twoRecordsConsistentWithProse"]["classification"],
    "determinedWithoutPython": out["twoRecordsConsistentWithProse"]["determinedWithoutReferencePython"],
    "discriminatorPartitionsCleanly":
        out["whatIsFullyPublished"]["causesVsNativeDeficienciesDiscriminator"]["partitionsCleanly"],
    "disputedRecordsAllShapeLegal":
        out["whatIsFullyPublished"]["measuredRecordTest"]["everyDisputedRecordIsSection95ShapeLegal"],
    "unpublishedPoints": len(out["branchBoundCheck"]["unpublished"]),
    "amendmentRequired": out["sourceConclusion"]["amendmentRequired"],
    "referenceCorrectionIndicated": out["sourceConclusion"]["referenceCorrectionIndicated"],
    "decisionsForRoot": len(out["independentSemanticDecisionsRequiringReview"]),
}, indent=2))
