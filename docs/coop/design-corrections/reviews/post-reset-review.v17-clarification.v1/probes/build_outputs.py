#!/usr/bin/env python
"""Build clarification.json and the FULL corrected successor review.json.

The successor carries every element of the original report forward, correcting
only reporting claims. Original evidence and verdict chronology are preserved by
reference; the original bytes are untouched in
reviews/post-reset-review.v17 (review.json aa3cfd5e..., review.md 1ec8a56f...).
"""
import hashlib
import json
import os

OLD = "/tmp/opensip-design-corrections/post-reset-review.v17"
NEW = "/tmp/opensip-design-corrections/post-reset-review.v17-clarification.v1"
SHA = "8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c"


def J(p):
    with open(p) as fh:
        return json.load(fh)


def L(n):
    return J(os.path.join(NEW, "logs", n))


orig = J(os.path.join(OLD, "review.json"))
c01 = L("c01-owner-docs.json")
c02 = L("c02-admitted-domain.json")
c02b = L("c02b-authority-anchors.json")
c07 = L("c07-harness-nullable-refusal.json")
c07b = L("c07b-execute-repair-cases.json")
c345 = L("c345-probe-scope-audit.json")

cw = c01["crosswalkComparison"]

# ---------------------------------------------------------------- corrections
CORRECTIONS = [
 {
  "id": "CL-1",
  "point": 1,
  "target": "arDispositions[].basis (all 16), review.md section 11, "
            "registers.owningDocumentsByteIdenticalToV16",
  "originalClaim": "The owning document docs/coop/architecture-depth-review/"
                   "REVIEW.md and the correction crosswalk are BYTE-IDENTICAL "
                   "to the v16 manifest entry, so no row moved.",
  "status": "FACTUALLY WRONG, CORRECTED",
  "whatIsTrue": "correction-crosswalk.proposed.json DID change: v16 %s -> v17 "
                "%s. My own delta section already listed it as changed "
                "(+10464 bytes), so the report contradicted itself."
                % (cw["v16ExtractedSha256"] if cw.get("v16ExtractedSha256") else
                   "d2423ea249973bc6620b0624bd6b8043e090f46815aa32f21d665f310cb21438",
                   "9a52657622cdb0bf5268044635c94498af76fa9b0d456f5a8b7ae43407095aa3"),
  "independentMeasurement": {
      "v16Sha256": "d2423ea249973bc6620b0624bd6b8043e090f46815aa32f21d665f310cb21438",
      "v17Sha256": "9a52657622cdb0bf5268044635c94498af76fa9b0d456f5a8b7ae43407095aa3",
      "itemCount": {"v16": cw["v16ItemCount"], "v17": cw["v17ItemCount"]},
      "itemIdsEqual": cw["itemIdsEqual"],
      "changedFieldHistogram": cw["changedFieldHistogram"],
      "rowsWithNoChange": cw["rowsWithNoChange"],
      "everyRowChangedOnlyRoutingFields": cw["everyRowChangedOnlyRoutingFields"],
      "substantiveFieldsChanged": cw["substantiveFieldsChanged"],
      "allSubstantiveFieldsUnchanged": cw["allSubstantiveFieldsUnchanged"],
  },
  "correctedBasis": "The AR OWNING document (architecture-depth-review/REVIEW.md) "
                    "IS byte-identical to its v16 manifest entry. The crosswalk "
                    "CHANGED, on all 16 rows, in exactly two fields - "
                    "latestCompletedReview and historicalReviews - which are "
                    "review-ROUTING/provenance pointers. Every obligation, "
                    "selector, owner, unit, contract, evidence, ownerRows and "
                    "status field is unchanged. So the ORIGINAL OBLIGATION AND "
                    "CONTRACT are preserved while the ROUTING moved; those are "
                    "different things and the original report conflated them.",
  "otherOwnerDocsReVerified": [
      {"path": d["path"], "byteIdenticalPerManifest": d["byteIdenticalPerManifest"],
       "inV17Manifest": d["inV17Manifest"]}
      for d in c01["documents"]],
  "gradeEffect": "None. CARRIED-UNCHANGED stands for all 16 AR rows on the "
                 "corrected basis, and no grade is granted or inferred.",
 },
 {
  "id": "CL-2",
  "point": 2,
  "target": "structuralAssessment.structuralPointersChangedAcrossAllDocuments, "
            "structuralAssessment.conclusion, review.md section 8",
  "originalClaim": "'zero structural pointers changed' / 'No grammar, authority "
                   "or admission was widened' / 'Every executable change is "
                   "additive strictness'.",
  "status": "OVERBROAD, CORRECTED",
  "whatIsTrue": {
      "p02MetricScope": c02["p02MetricRestated"]["whatItMeasured"],
      "intersectionLeafValuesChanged":
          c02["p02MetricRestated"]["intersectionLeafValuesChanged"],
      "structuralPointersRemoved": c02["p02MetricRestated"]["pointersOnlyInV16"],
      "structuralPointersADDED": c02["p02MetricRestated"]["pointersOnlyInV17"],
      "additionsAreStructuralChanges": True,
      "examplesOfStructuralAdditions": [
          "a new presence conditional (allOf/if/then/else) on EvidenceRequirement",
          "two new enum definitions (NativeSufficiencyDeficiency, "
          "ImportedRequirementDeficiency)",
          "new relation-registry laws (coveragePartitionLaw)",
          "new required/annotation blocks (x-opensip-config-node-kind-law, "
          "x-opensip-imported-requirement-law, x-opensip-mutation-operation-map)"],
      "p08IsAHeuristic": True,
      "p08Scope": c02["p08MetricRestated"]["whatItMeasured"],
      "noRemovedRaiseLineIsNotAProof": True,
  },
  "theAdmittedDomainActuallyChanged": {
      "field": "repair.schema.json#/$defs/EvidenceRequirement/properties/deficiency",
      "v16FieldSchema": "$ref D9Deficiency",
      "v17FieldSchema": "oneOf [NativeSufficiencyDeficiency, "
                        "ImportedRequirementDeficiency]",
      "tokensAdmittedByV16Field": c02["admittedByV16Count"],
      "tokensAdmittedByV17Field": c02["admittedByV17Count"],
      "newlyAdmitted": c02["newlyAdmitted"],
      "noLongerAdmitted": c02["noLongerAdmitted"],
      "theFourBlindNamedOutcomesWereRefusedByV16Field":
          c02["allFourWereRefusedByV16Field"],
      "andAreAdmittedByV17Field": c02["allFourAreAdmittedByV17Field"],
      "characterisation": "The field's admitted VALUE DOMAIN was deliberately "
                          "REPLACED, not widened and not narrowed: 11 tokens "
                          "newly admit and 5 no longer admit. That replacement "
                          "IS the CB6-MUST-1 correction. Describing it as 'no "
                          "widening' or as 'additive strictness' misdescribes "
                          "the change.",
  },
  "intendedAuthorityAssessedSEPARATELY": {
      "method": "byte comparison of the owning guard blocks, v16 vs v17",
      "closedWorldGateBlockByteIdentical":
          c02b.get("closedWorldGateBlockByteIdentical"),
      "repairApplyBodyByteIdentical": c02b.get("repairApplyBodyByteIdentical"),
      "anchorCounts": {k: v for k, v in c02b.items() if isinstance(v, dict)},
      "conclusion": "The AUTHORITY is preserved and this is now measured rather "
                    "than inferred from the admission-set claim: the "
                    "closed-world gate block and the entire repair_apply body "
                    "are byte-identical between v16 and v17. Preservation of "
                    "authority and change of the admitted deficiency domain are "
                    "separate findings and are now reported separately.",
  },
  "correctedConclusion": "No leaf value at any pointer common to both versions "
                         "changed, and registry MEMBERSHIP (relations, ladder "
                         "rungs, coverage states, D9Deficiency, DeficiencyV2) is "
                         "unchanged. 321 structural pointers were ADDED and one "
                         "removed. The removed one retypes EvidenceRequirement."
                         "deficiency, deliberately changing its admitted domain. "
                         "The repair AUTHORITY - closed-world gate and apply "
                         "authorization - is byte-identical.",
 },
 {
  "id": "CL-3",
  "point": 3,
  "target": "priorFindingDispositions[CB6-MUST-1].evidence, review.md section 5",
  "originalClaim": "'191 executable cases spanning the full cross-product of "
                   "relations and vocabularies'; ROUNDTRIP described as the "
                   "producer's outcome round-tripping; the copiedBoolean note "
                   "pointed at p06 as an authorization probe.",
  "status": "OVERSTATED SCOPE, CORRECTED",
  "actualComposition": c345["p03Composition"],
  "arithmetic": c345["p03Arithmetic"],
  "isAFullCrossProduct": c345["p03IsFullCrossProduct"],
  "fullCrossProductWouldBe": c345["p03FullCrossProductWouldBe"],
  "crossPlaneCoveredNativeRelations": c345["p03CrossPlaneCoveredNativeRelations"],
  "crossPlaneCoverageNote": "cross-plane negatives were run for only the FIRST 4 "
                            "of 13 native relations, so 191 of a possible 240.",
  "sufficiencyInputs": {
      "areValidatedAdmittedRecords":
          c345["p03SufficiencyInputsAreValidatedRecords"],
      "note": c345["p03SufficiencyInputNote"],
  },
  "roundtripCorrected": {
      "forwardsTheProducedRecord": c345["p03RoundtripForwardsProducedRecord"],
      "usesFixedRelation": "references, for all four - including "
                           "derivation-policy-unmet, which was PRODUCED from a "
                           "`types` requirement",
      "relationMismatchRows": [r["target"] for r in
                               c345["p03RoundtripRelationMismatch"]],
      "allFourProducersEmittedThatSameSoleToken":
          c345["allFourProducersEmittedTheSameSoleToken"],
      "whatItSupports": "TOKEN preservation - the producer really does emit each "
                        "of the four outcomes as its sole deficiency, and each "
                        "token is carryable and admissible at the consumer and "
                        "the schema. It is NOT an end-to-end native-to-authorized"
                        "-repair proof.",
  },
  "authorizationCrossReferenceCorrected": {
      "originalNoteSaid": c345["p03CopiedBooleanNoteText"],
      "pointedTo": "p06",
      "butP06Is": c345["p06IsActually"],
      "truth": "No executed authorization or target-projection control was run "
               "in this review. Every statement I made about authorization "
               "separation - the sealed Run remaining authority, the "
               "closed-world gate running before any descriptor, apply requiring "
               "an authorization bound to repairPlanId - is CODE AND CONTRACT "
               "INSPECTION, now supplemented by the byte-identity measurement in "
               "CL-2. It is not an executed authorization control.",
  },
 },
 {
  "id": "CL-4",
  "point": 4,
  "target": "priorFindingDispositions[CB6-MUST-2 / SHOULD-1 / SHOULD-2].evidence, "
            "review.md sections 5 and the closing paragraph",
  "originalClaim": "p04's controls called 'admission'; 'two readings mint two "
                   "RunIds'; 'the key I recomputed'; and 'all findings corrected "
                   "in the admission, not merely in prose'.",
  "status": "OVERSTATED, CORRECTED",
  "p04": {
      "actualBoundary": c345["p04ControlBoundary"],
      "usesFillerContentDigests": c345["p04UsesFillerDigests"],
      "callsFullNativeContextAdmission": c345["p04CallsFullNativeContextAdmission"],
      "runsConstructed": c345["p04ConstructedRuns"],
      "measured": c345["p04IdentityConsequenceMeasured"],
      "correctedStatement": "13 controls at the graph-fault boundary, not full "
                            "NativeContext or retained-Run admission. Two "
                            "DIFFERENT tsconfigGraphHash values were computed and "
                            "do differ; the step from there to two RunIds is the "
                            "PUBLISHED derivation chain read from the law and the "
                            "contract, not two constructed Runs.",
      "configOriginClaim": c345["p04ConfigOriginClaimSource"],
  },
  "p05": {
      "usedAuthorKeyFunctions": c345["p05UsesAuthorKeyFunctions"],
      "independentlyReimplementedH": c345["p05IndependentlyReimplementedH"],
      "correctedStatement": c345["p05WhatItActuallyEstablished"],
  },
  "p06": {
      "fullRunControls": c345["p06FullRunControls"],
      "positives": c345["p06Positives"],
      "typedRefusals": c345["p06TypedRefusals"],
      "confirmed": "p06 DOES execute 7 full Run controls. That claim stands.",
      "qualifications": [
          "the fixture is the author's own check-identity build(), a shared "
          "trusted construction, not an independently built Run",
          "the different-RELATION branch never executed: otherRelationChosen was "
          "null, so the tuple-difference dimension was exercised only by RUNG",
          "totality-only-`file` is a STATIC registry read, not an executed "
          "totality control",
          "each overlap control has exactly ONE overlapping subject, so the "
          "UTF-8 byte-order tie-break rule is NOT discriminated"],
  },
  "remedyClassificationCorrected": c345["findingRemedyClassification"],
 },
 {
  "id": "CL-5",
  "point": 5,
  "target": "governanceCrossReferences, registers.advisoryAccount, "
            "registers.gatesDemonstrated/gatesQualified",
  "originalClaim": "'522 current pins resolved / 22 historical' presented "
                   "without scope; 'advisory account 50 -> 55, five added'; "
                   "gates reported only on demonstrated/qualified.",
  "status": "SCOPE AND LINEAGE CORRECTED",
  "scannerScope": {
      "recordsScanned": c345["p10RecordsScanned"],
      "isWholeRepositoryOrCorpusProof": c345["p10IsWholeCorpusProof"],
      "rawCounts": c345["p10RawCounts"],
      "problemTriage": {
          "240": "crosswalk historicalReviews rows where my scanner mis-paired a "
                 "review PATH with a subjectManifestSha256 - a manifest digest, "
                 "not that file's digest",
          "18": "handoff before-version pins (frozen16Sha256 / finalV5Sha256), "
                "self-labelling as-of pins",
          "42": "21 external live files named by the preservation report, each "
                "counted twice (openingSha256 and currentSha256)",
          "4": "advisory-account rows needing context; only V14-ADV-2 lacks it",
      },
      "historicalClassificationCaveat": c345["p10HistoricalClassificationNote"],
      "myRetainedEvidenceLimit": "10 of the 31 preservation-report files lie "
                                 "inside the frozen slice and all 10 match. Root "
                                 "independently verified all 31 live protected "
                                 "files; that verification is root's, not mine, "
                                 "and I retain my stated limit.",
      "phraseHitCaveat": "a phrase match inside an explicitly preserved finding "
                         "quotation is not live law; the 7 retired-rationale "
                         "occurrences are quotations in `finding` fields.",
  },
  "advisoryAccountLineageCorrected": {
      "proposedV16AccountItems": 50,
      "completedV16AssentAccountItems": 52,
      "completedV16AssentSelector":
          "design-assent.v16.json#/advisoryApplicationAccount",
      "v16NewAdvisoriesRecordedSeparately": {
          "selector": "review-assessment.v16.json#/newAdvisoryApplicationAccount",
          "items": ["V16-ADV-1", "V16-ADV-2"]},
      "proposedV17AccountItems": 55,
      "addedRelativeToProposedV16": ["CB6-ADV-1", "CB6-ADV-2", "CB6-ADV-3",
                                     "V16-ADV-1", "V16-ADV-2"],
      "addedRelativeToCompletedV16Assent": ["CB6-ADV-1", "CB6-ADV-2", "CB6-ADV-3"],
      "correctedStatement": "The lineage is 52 -> 55, adding exactly the three "
                            "CB6 advisories. My '50 -> 55, five added' was "
                            "measured against the PROPOSED v16 account file and "
                            "mislabelled as the lineage; the two extra items are "
                            "V16-ADV-1/2, which the completed v16 assent had "
                            "already recorded.",
      "severitiesChanged": 0,
      "removed": 0,
  },
  "qualificationGateFlagsCorrected": {
      "gateCount": c345["qualificationGateCount"],
      "booleanFlags": c345["qualificationGateBooleanFlags"],
      "allFlagsFalseOnAll32": c345["allGateBooleanFlagsFalse"],
      "correctedStatement": "All THREE per-gate boolean flags are false on all "
                            "32 gates - demonstrated, qualified AND "
                            "implementationHarnessAuthored. My original report "
                            "named only the first two.",
  },
 },
 {
  "id": "CL-6",
  "point": 6,
  "target": "newAdvisories[V17-ADV-1, V17-ADV-2].repair",
  "status": "ROOT DISPOSITIONS ASSESSED AND ACCEPTED AS SUFFICIENT",
  "v17Adv1": {
      "rootDisposition": "Retain the accepted schema bytes now. Record an "
                         "explicit application disposition that consumers "
                         "enumerate admitted kinds from the imported relation "
                         "REGISTRY and select perKindApplicability by that "
                         "validated key; `rule` is documentation metadata, not a "
                         "relation. Structural relocation is optional future "
                         "versioned cleanup, never a silent patch.",
      "myIndependentTest": {
          "importedRelationRegistryKeys": ["history-change", "runtime-observation"],
          "perKindApplicabilityKeys": ["history-change", "rule",
                                       "runtime-observation"],
          "everyRegistryRelationHasAWellTypedRow": True,
          "mapIsTotalOverTheRegistry": True,
          "bogusKeyUnreachableUnderThatRule": True,
          "extraNonRelationKeys": ["rule"],
      },
      "sufficient": True,
      "why": "The disposition names the correct DERIVATION ORDER - enumerate "
             "from the registry, then index - which is exactly what both model "
             "sites and the checker already do. Under it the map is total over "
             "the two real relations, both rows are well-typed, and `rule` is "
             "never reached. The failure mode I identified is removed without "
             "touching accepted bytes.",
      "anIndependentReasonNotToPatchNow": "Editing this registered schema "
             "document would change its committed digest and MOVE the retained-"
             "Run identities of every fixture that commits it - the CB6-NEW-4 "
             "consequence. A silent patch would therefore be worse than the "
             "defect. Deferring to a versioned cleanup is the right call.",
      "doesAnyNormativeClarificationRequireANewSubject": False,
      "whyNot": "No admission outcome changes, no identity moves, and no "
                "published law is wrong - only an annotation is mistyped. A new "
                "frozen subject is not warranted at this severity.",
  },
  "v17Adv2": {
      "rootDisposition": "Label item 44's existing ef0c... pin as historical "
                         "as-of-v16 and bind current 53380... in the separately "
                         "reviewed application/advisory record, preserving "
                         "frozen v17 unchanged.",
      "myIndependentCheck": {
          "currentFrozenDigestOfTheNamedFile":
              "53380a2455490e07028e1872557044fb1b69d062143deeeec0f44006f0b2be9a",
          "matchesRootsTargetDigest": True,
          "isExactlyTheItem43PatternAlreadyInTheSameDocument": True,
      },
      "sufficient": True,
      "why": "It is precisely the remedy I proposed and precisely the pattern "
             "item 43 already implements. Doing it in the separately reviewed "
             "application/advisory record rather than by editing the account is "
             "correct: the account is itself inside the frozen subject, so "
             "editing it now would move the frozen manifest for a nonblocking "
             "provenance issue.",
  },
 },
 {
  "id": "CL-7",
  "point": 7,
  "target": "structuralAssessment.whatTheThreeRemovalsWere[2] and the "
            "'stricter harness' characterisation",
  "status": "ROOT OBSERVATION CONFIRMED; NEW ADVISORY V17-ADV-3 RAISED; "
            "MY 'STRICTER' CLAIM NARROWED",
  "rootObservationIsCorrect": True,
  "mechanism": "check_workflows.v1.py line 1112: "
               "`check(cid, case['expect'].get('refusal') == r.detail, r.detail)` "
               "followed by `continue`. Refusal.detail defaults to None and "
               "`.get('refusal')` is None for a case expecting SUCCESS, so "
               "None == None passes and the `continue` skips every later "
               "assertion for that case.",
  "measured": {
      "refusalRaiseSitesInModel": c07["totalRefusalRaiseSitesInModel"],
      "detailFreeRaiseSites": c07["detailFreeRaiseSiteCount"],
      "functionsWithDetailFreeRefusals": c07["functionsWithDetailFreeRefusals"],
      "repairPreviewItselfHasOne": c07["repairPreviewItselfHasDetailFreeRaise"],
      "criticalNote": "`refuse` is the inner helper of "
                      "admit_evidence_requirement, so EVERY CB6-MUST-1 "
                      "per-requirement refusal is detail-free. The masking "
                      "surface sits directly on the finding this candidate "
                      "exists to fix.",
      "truthTable": c07["truthTable"],
      "misPassingRows": len(c07["misPassingRows"]),
      "comparisonSites": c07["sameComparisonSites"],
      "guardedSites": 1,
      "unguardedSites": len(c07["unguardedSites"]),
  },
  "isItMaskingAnythingToday": {
      "method": "I replicated the checker's repair loop over all 37 cases and "
                "recorded whether repair_preview raised at all.",
      "repairCases": c07b["caseCount"],
      "positiveCases": c07b["positiveCases"],
      "negativeCases": c07b["negativeCases"],
      "positivesThatRaised": len(c07b["positivesThatRaised"]),
      "positivesSilentlyMasked": len(c07b["positivesSilentlyMasked"]),
      "answer": "NO. 0 of 25 positive repair cases raises, so no case is masked "
                "and the reported 1787 is not inflated by this defect.",
  },
  "mitigations": [
      "The three CB6-MUST-1 controls that DO rely on the null comparison "
      "(expect.refusal = null) each additionally carry expectRemedyContains "
      "naming the exact internal decision key, so a DIFFERENT detail-free "
      "refusal would fail their .refusal-reason check. The candidate already "
      "recognised and mitigated the discrimination problem in the negative "
      "direction.",
      "A masked positive would skip its downstream check() calls, LOWERING "
      "checkCount below 1787 and therefore breaking the byte-identical report "
      "comparison that the freeze discipline performs. The masking is not fully "
      "silent under that discipline.",
      "The equivalent comparison at line 384 (import cases) IS guarded by an "
      "errorCode conjunct, so the pattern is known to the authors.",
  ],
  "severityDecision": {
      "grade": "advisory (nonblocking)",
      "id": "V17-ADV-3",
      "reasoning": "It is a real defect in reviewed reference source and it sits "
                   "on a load-bearing path. But it causes no current wrong "
                   "result (measured 0/25), the controls I relied on for "
                   "CB6-MUST-1 are independently discriminated by "
                   "expectRemedyContains, and a regression would perturb "
                   "checkCount and be caught by the existing byte-identity "
                   "comparison. On this review chain's own scale - where "
                   "SHOULD has meant a real underdetermination in PUBLISHED LAW "
                   "(SHOULD-1, SHOULD-2) - a latent robustness gap in the "
                   "evidence harness that changes no outcome is an advisory.",
      "theCounterArgumentIRejected": "A control that can pass for the wrong "
                   "reason is not a valid control, and the 'it does not fire "
                   "today' defence is exactly the contingency argument I used to "
                   "RAISE V17-ADV-2. I record this counter-argument explicitly "
                   "so root can overrule me on the record. I did not escalate "
                   "because, unlike V14-ADV-2's pin, this one is additionally "
                   "backstopped by expectRemedyContains and by checkCount "
                   "sensitivity, and because inventing a blocking finding to "
                   "appear rigorous would be its own failure of judgement.",
      "verdictEffect": "None. No unresolved MUST or SHOULD arises from it.",
  },
  "myOriginalClaimNarrowed": "My 'the checker's two removed lines were replaced "
                             "by STRICTER versions' is true of the IMPORT "
                             "harness at line 384 (which gained an errorCode "
                             "conjunct) and of the added expectRemedyContains "
                             "assertions. It is NOT a universal guarantee about "
                             "the repair harness, and I withdraw it as stated.",
  "suggestedCorrection": "At lines 1112 and 1320, require the case to have "
                         "OPTED IN to a refusal before accepting one - e.g. "
                         "`check(cid, 'refusal' in case['expect'] and "
                         "case['expect']['refusal'] == r.detail, r.detail)` - "
                         "which preserves the three deliberate null-refusal "
                         "cases while failing an unexpected detail-free refusal "
                         "on a positive. NO SOURCE FIX IS MADE IN THIS REPORT.",
 },
 {
  "id": "CL-8",
  "point": 8,
  "target": "failedAttempts and the concurrent-file observation",
  "status": "ATTRIBUTION AND ARTIFACT SCOPE CORRECTED",
  "concurrentFiles": {
      "originalStatement": "I listed 12 files modified outside my directory and "
                           "attributed them to 'the concurrent Codex/root "
                           "orchestration' on the basis of filenames and mtimes.",
      "correction": "Those files are ROOT's work (apply-v17-advisory-records.py, "
                    "the monitor/reading-notes/prepared-assent recorders and the "
                    "mutable NEXT updates). No frozen byte changed. File mtimes "
                    "alone cannot attribute authorship to or away from any "
                    "process, and I should not have used them as attribution "
                    "evidence even though my conclusion happened to be right.",
      "accurateScope": "REVIEW-AUTHORED ARTIFACTS are exactly the files I "
                       "created under my own output directories. Ordinary Claude "
                       "runtime, session and shell metadata also exists outside "
                       "those directories and is not a review artifact.",
      "frozenBytesUnaffected": True,
  },
  "failedArtifactPreservation": {
      "correction": "My original report implied I preserved every failed byte. "
                    "I did not: my successful p06 rerun OVERWROTE my own "
                    "p06 result log. What is preserved is the failed SOURCE.",
      "failedSourcesRetainedByMe": [
          {"file": "probes/failed-attempt-01-p04-wrong-graph-key.py",
           "sha256": "480e1e7494f4d736719219599691bd790013d46004ee94a213a65705ff4c0644",
           "bytes": 11049},
          {"file": "probes/failed-attempt-02-p04-unsorted-nodes-array.py",
           "sha256": "742b9cd25d9f47cca8e6c4c69353887329b030f1bb58b44f0cf0c0ba2d3b45e5",
           "bytes": 11413},
          {"file": "probes/failed-attempt-03-p06-wrong-ladder-module.py",
           "sha256": "cd1521d450347e32ac8bb5abc1d95c379fefc05e791adbc805130eb1a246c124",
           "bytes": 7921},
          {"file": "probes/failed-attempt-04-p06-degenerate-identical-scope.py",
           "sha256": "f02b93c2c5bdc143a07ca514f1a409da928d9f5fc9d02eac58f939cc7bc05860",
           "bytes": 8172}],
      "failedRESULTCapturedByRoot": {
          "path": "/tmp/opensip-design-corrections/codex-post-reset.v1/"
                  "independent-v17-p06-attempt2-report.json",
          "bytes": 3950,
          "sha256": "83fb1ab13913ed7f2a05089b1c6c80272f4db48b7fec0b6487547bc915a50b68",
          "note": "root captured the p06 attempt-2 raw report BEFORE my "
                  "successful rerun overwrote my own log. That capture is "
                  "root's artifact, not mine."},
      "otherFailedAttemptsRetainedIn": "tool outputs / transcript",
  },
  "distinctionsKeptSeparate": {
      "caseSelection": "which fixtures a probe chose to exercise",
      "correctedExpectation": "an expectation of mine that was wrong and was "
                              "fixed (failed attempts 01-04)",
      "staticCheck": "reading bytes, schemas or code without executing the "
                     "system under test",
      "actualProductEnforcement": "NONE of my work is this. No host, compiler, "
                                  "provider, repository, renderer, ledger or OS "
                                  "executed at any point.",
  },
 },
]

clar = {
  "report": "clarification and correction of post-reset-review.v17",
  "standing": "ADDITIVE report correction on the SAME frozen subject. It "
              "supersedes only REPORTING CLAIMS of the original. No design or "
              "reference source, no prior review, no snapshot, no live repo and "
              "no prior copy was edited.",
  "subjectManifestSha256": SHA,
  "originalReport": {
      "path": "docs/coop/design-corrections/reviews/post-reset-review.v17",
      "reviewJson": {"sha256": "aa3cfd5e94ff29de9af45441b41ac746cad030cde8c1451341c7f7ec6956e4d8",
                     "bytes": 75877},
      "reviewMd": {"sha256": "1ec8a56fb7577cf866d6ae83083286439b5011b7707034ae583481503ff1c8c7",
                   "bytes": 34592},
      "retainedVerbatim": True,
      "verdictChronologyPreserved": "v16 ACCEPT -> blind v6 CHANGES_REQUIRED -> "
                                    "v17 corrections -> original v17 ACCEPT "
                                    "(aa3cfd5e) -> this clarification, which "
                                    "does not alter that chronology.",
  },
  "corrections": CORRECTIONS,
  "correctionCount": len(CORRECTIONS),
  "newFindingsFromThisPass": ["V17-ADV-3"],
  "newMustIssues": [],
  "newShouldIssues": [],
  "sourceAcceptanceStillHolds": True,
  "whySourceAcceptanceHolds":
      "Every correction here is to my REPORTING, to probe-scope characterisation "
      "or to a governance-record provenance claim. None reaches the reviewed "
      "design or reference SOURCE except V17-ADV-3, which is a nonblocking "
      "harness robustness gap measured to mask nothing today. The four blind-v6 "
      "findings and the nineteen additional source findings remain resolved on "
      "the corrected and narrower evidential basis stated in the successor "
      "report, and the frozen bytes are unchanged.",
  "independence": "Correcting my own report does not make this review dependent "
                  "on the authored SOURCE. Every correction above was "
                  "independently measured against the frozen bytes before being "
                  "accepted, and points 1, 5 and 7 were verified rather than "
                  "taken on root's statement - including root's '52', which I "
                  "confirmed at design-assent.v16.json#/advisoryApplicationAccount.",
  "noAcceptanceInferred": {
      "blind": False, "application": False, "readiness": False,
      "productQualification": False, "implementationAuthorized": False,
  },
}

with open(os.path.join(NEW, "clarification.json"), "w") as fh:
    json.dump(clar, fh, indent=1, sort_keys=False)
    fh.write("\n")

# ------------------------------------------------- successor review.json
rev = json.loads(json.dumps(orig))   # deep copy, preserving every element

rev["review"] = ("fresh independent OpenSIP architecture/design/reference "
                 "review, v17 - CORRECTED SUCCESSOR")
rev["supersedes"] = {
    "path": "docs/coop/design-corrections/reviews/post-reset-review.v17",
    "reviewJsonSha256": "aa3cfd5e94ff29de9af45441b41ac746cad030cde8c1451341c7f7ec6956e4d8",
    "reviewMdSha256": "1ec8a56fb7577cf866d6ae83083286439b5011b7707034ae583481503ff1c8c7",
    "scope": "Supersedes ONLY reporting claims. The original evidence, its "
             "probe sources and results, its failed attempts and the verdict "
             "chronology are preserved verbatim and remain the historical record.",
    "clarification": "clarification.json / clarification.md in this directory",
}
rev["verdict"] = "ACCEPT"
rev["verdictScope"] = (
    "SOURCE AND DESIGN ONLY, bound to the exact frozen bytes, on the CORRECTED "
    "and narrower evidential basis recorded here. Not blind reconstructability, "
    "not application acceptance, not readiness, not product qualification, not "
    "implementation authorization.")

# --- corrected structural assessment (CL-2) ---
sa = rev["structuralAssessment"]
sa["metricScopeCorrection"] = c02["p02MetricRestated"]
sa["structuralPointersChangedAcrossAllDocuments"] = {
    "value": 0,
    "scope": "INTERSECTION-LEAF metric only: leaf values at pointers present in "
             "BOTH versions, after stripping a chosen prose key set. This is NOT "
             "a claim of zero structural schema change.",
}
sa["structuralPointersAdded"] = c02["p02MetricRestated"]["pointersOnlyInV17"]
sa["structuralPointersRemoved"] = c02["p02MetricRestated"]["pointersOnlyInV16"]
sa["additionsAreStructuralChanges"] = True
sa["admittedDomainChange"] = CORRECTIONS[1]["theAdmittedDomainActuallyChanged"]
sa["intendedAuthorityPreservedSeparately"] = \
    CORRECTIONS[1]["intendedAuthorityAssessedSEPARATELY"]
sa["conclusion"] = CORRECTIONS[1]["correctedConclusion"]
sa.pop("whatTheThreeRemovalsWere", None)
sa["whatTheThreeRemovalsWere"] = [
    "native model: an INLINE restatement of the kind rule, replaced by a read of "
    "the published table. Measured over 25 paths including edge cases: 0 "
    "disagreements, so publishing the authority moved no derived value.",
    "workflows model: an unmet-precondition append that now has a NEW admission "
    "gate (admit_evidence_requirement) ahead of it and carries the rung, plane "
    "and exact cause.",
    "checker harness: two lines replaced. The IMPORT site (line 384) genuinely "
    "gained an errorCode conjunct and is stricter. The REPAIR site (line 1112) "
    "did not gain that guard - see V17-ADV-3. My original universal 'stricter' "
    "characterisation is withdrawn.",
]
sa["refusalBearingLinesRemovedFromAnyModel"] = {
    "value": 0,
    "caveat": "p08 is a token/line heuristic, not an AST or semantic proof. The "
              "absence of a removed raise-line is not a proof that the refusal "
              "set is preserved.",
}
sa["everyExecutableChangeIsAdditiveStrictness"] = {
    "withdrawn": True,
    "why": "The EvidenceRequirement retype deliberately CHANGES the admitted "
           "deficiency domain (11 in, 5 out). That is a domain replacement, not "
           "strictness.",
}

# --- corrected evidence on the four findings (CL-3, CL-4) ---
pf = {d["id"]: d for d in rev["priorFindingDispositions"]}
pf["CB6-MUST-1"]["evidence"]["caseCompositionCorrected"] = CORRECTIONS[2]["actualComposition"]
pf["CB6-MUST-1"]["evidence"]["isAFullCrossProduct"] = False
pf["CB6-MUST-1"]["evidence"]["crossPlaneCoveredNativeRelations"] = \
    c345["p03CrossPlaneCoveredNativeRelations"]
pf["CB6-MUST-1"]["evidence"]["sufficiencyInputsAreHelperDicts"] = True
pf["CB6-MUST-1"]["evidence"]["roundTripIsTokenLevel"] = CORRECTIONS[2]["roundtripCorrected"]
pf["CB6-MUST-1"]["evidence"]["authorizationWasInspectedNotExecuted"] = \
    CORRECTIONS[2]["authorizationCrossReferenceCorrected"]["truth"]
pf["CB6-MUST-1"]["basis"] += (
    " CORRECTED SCOPE: the 191 cases are not a full cross-product (240 would be); "
    "cross-plane negatives cover 4 of 13 native relations; the sufficiency inputs "
    "are partial helper dicts, not validated admitted records; and the round-trip "
    "is token-level, not an end-to-end native-to-authorized-repair proof.")

pf["CB6-MUST-2"]["evidence"]["controlBoundaryCorrected"] = CORRECTIONS[3]["p04"]
pf["CB6-MUST-2"]["basis"] += (
    " CORRECTED SCOPE: the 13 controls run at the graph-fault boundary with "
    "filler content digests, not full NativeContext or retained-Run admission; "
    "no Run was constructed; two differing tsconfigGraphHash values were "
    "measured and the RunId consequence is the published derivation chain read "
    "from the law, not two constructed Runs; the configOrigin statement is "
    "normative inspection.")

pf["CB6-SHOULD-1"]["evidence"]["keyRecomputationCorrected"] = CORRECTIONS[3]["p05"]
pf["CB6-SHOULD-1"]["basis"] = pf["CB6-SHOULD-1"]["basis"].replace(
    "the key I recomputed is deterministic and moves with "
    "both operation and requestId",
    "the author's own key function is deterministic and moves with both "
    "operation and requestId (I did NOT independently reimplement the H "
    "encoding; I verified the preimage FIELD SET against the published recipe)")

pf["CB6-SHOULD-2"]["evidence"]["qualifications"] = CORRECTIONS[3]["p06"]["qualifications"]
pf["CB6-SHOULD-2"]["basis"] += (
    " CORRECTED SCOPE: the 7 full-Run controls stand, but they use the author's "
    "own check-identity build() fixture; the different-RELATION branch never "
    "executed (otherRelationChosen was null), so tuple-difference was exercised "
    "only by rung; totality-only-`file` is a static registry read; and with one "
    "overlapping subject per control the UTF-8 tie-break rule is not "
    "discriminated.")

rev["findingRemedyClassification"] = c345["findingRemedyClassification"]

# --- corrected governance section (CL-5) ---
gx = rev["governanceCrossReferences"]
gx["scannerScope"] = CORRECTIONS[4]["scannerScope"]
gx["isWholeCorpusProof"] = False
rev["registers"]["advisoryAccount"] = CORRECTIONS[4]["advisoryAccountLineageCorrected"]
rev["registers"]["advisoryAccount"]["myTwoNewAdvisoriesAreNotInThisAccount"] = True
rev["registers"]["advisoryAccount"]["norIsV17ADV3"] = True
rev["registers"]["qualificationGateFlags"] = \
    CORRECTIONS[4]["qualificationGateFlagsCorrected"]
rev["registers"]["owningDocumentsByteIdenticalToV16"] = {
    "value": False,
    "correction": "correction-crosswalk.proposed.json CHANGED (routing fields "
                  "only, all 16 rows). Every OTHER owner document I cite is "
                  "byte-identical to its v16 manifest entry.",
    "perDocument": CORRECTIONS[0]["otherOwnerDocsReVerified"],
}

# --- ID-KEYED disposition objects with corrected basis ---
AR_BASIS = (
    "The AR owning document docs/coop/architecture-depth-review/REVIEW.md is "
    "BYTE-IDENTICAL to its v16 manifest entry. correction-crosswalk.proposed.json "
    "DID change (v16 d2423ea2... -> v17 9a526576...), but the exact field "
    "comparison shows all 16 rows differ ONLY in latestCompletedReview and "
    "historicalReviews - review-ROUTING pointers. Every obligation, selector, "
    "owner, unit, contract, evidence, ownerRows and status field is unchanged. "
    "Original obligation and contract are PRESERVED; only routing moved.")
rev["arDispositions"] = {
    d["id"]: {**d, "basis": AR_BASIS,
              "routingChangedFields": ["latestCompletedReview", "historicalReviews"],
              "substantiveFieldsChanged": [],
              "appliedByThisReview": False,
              "finalApplicationOutcomeGranted": False}
    for d in orig["arDispositions"]}
rev["fwDispositions"] = {
    d["id"]: {**d, "appliedByThisReview": False,
              "finalApplicationOutcomeGranted": False,
              "basisVerified": "current-source-map.proposed.md byte-identical to "
                               "its v16 manifest entry (re-verified in this pass)"}
    for d in orig["fwDispositions"]}
rev["inheritedResidualDispositions"] = {
    d["id"]: {**d, "appliedByThisReview": False,
              "finalApplicationOutcomeGranted": False,
              "basisVerified": "inherited-residuals.proposed.md and "
                               "inherited-row-sources.proposed.json byte-identical "
                               "to their v16 manifest entries (re-verified)"}
    for d in orig["inheritedResidualDispositions"]}
rev["scopedReviewOwnerDispositions"] = {
    d["id"]: {**d, "appliedByThisReview": False,
              "finalApplicationOutcomeGranted": False,
              "basisVerified": "08-decision-and-readiness-register.md "
                               "byte-identical to its v16 manifest entry "
                               "(re-verified)"}
    for d in orig["scopedReviewOwnerDispositions"]}

# --- new advisory V17-ADV-3 ---
rev["newAdvisories"].append({
    "id": "V17-ADV-3",
    "severity": "advisory (nonblocking)",
    "title": "The repair-case harness accepts an unexpected detail-free Refusal "
             "on a case that expects success, then skips its remaining assertions",
    "selector": "docs/coop/design-corrections/workflows/check_workflows.v1.py "
                "lines 1112 and 1320",
    "raisedBy": "root observation, independently confirmed and measured in this "
                "clarification pass",
    "finding": CORRECTIONS[6]["mechanism"],
    "measured": CORRECTIONS[6]["measured"],
    "isItMaskingAnythingToday": CORRECTIONS[6]["isItMaskingAnythingToday"],
    "mitigations": CORRECTIONS[6]["mitigations"],
    "whyNotMustOrShould": CORRECTIONS[6]["severityDecision"]["reasoning"],
    "counterArgumentRecorded": CORRECTIONS[6]["severityDecision"][
        "theCounterArgumentIRejected"],
    "repair": CORRECTIONS[6]["suggestedCorrection"],
    "noSourceFixMadeInThisPass": True,
})
for a in rev["newAdvisories"]:
    if a["id"] == "V17-ADV-1":
        a["rootProposedDisposition"] = CORRECTIONS[5]["v17Adv1"]
    if a["id"] == "V17-ADV-2":
        a["rootProposedDisposition"] = CORRECTIONS[5]["v17Adv2"]

# --- corrected failed-attempt / artifact scope (CL-8) ---
rev["reviewAuthoredArtifactScope"] = CORRECTIONS[7]["concurrentFiles"]
rev["failedArtifactPreservation"] = CORRECTIONS[7]["failedArtifactPreservation"]
rev["evidenceKindDistinctions"] = CORRECTIONS[7]["distinctionsKeptSeparate"]

rev["priorFindingAccounting"]["unresolvedMustCount"] = 0
rev["priorFindingAccounting"]["unresolvedShouldCount"] = 0
rev["priorFindingAccounting"]["newAdvisoriesRaisedAcrossBothPasses"] = 3

rev["correctionsAppliedInThisSuccessor"] = [c["id"] for c in CORRECTIONS]

with open(os.path.join(NEW, "review.json"), "w") as fh:
    json.dump(rev, fh, indent=1, sort_keys=False)
    fh.write("\n")

for n in ("clarification.json", "review.json"):
    p = os.path.join(NEW, n)
    print("%-22s %8d bytes  sha256=%s" % (n, os.path.getsize(p),
          hashlib.sha256(open(p, "rb").read()).hexdigest()))
print("corrections:", len(CORRECTIONS))
print("advisories in successor:", [a["id"] for a in rev["newAdvisories"]])
print("AR keys:", len(rev["arDispositions"]), "FW:", len(rev["fwDispositions"]),
      "inherited:", len(rev["inheritedResidualDispositions"]),
      "owners:", len(rev["scopedReviewOwnerDispositions"]))
print("prior dispositions:", len(rev["priorFindingDispositions"]),
      "additional:", len(rev["additionalSourceFindingDispositions"]))
