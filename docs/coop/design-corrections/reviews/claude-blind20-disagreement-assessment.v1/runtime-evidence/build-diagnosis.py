#!/usr/bin/env python3
"""Assemble diagnosis.json from the recorded probe receipts."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RC = HERE / "probes" / "receipts"


def j(label):
    return json.loads((RC / label / "stdout.txt").read_text())


custody = j("p0-custody")
fam = j("p1-difference-families")
wit = j("p2b-witness-preimages")
cov = j("p3b-coverage-selection")
oth = j("p4-other-families")
root = j("p5b-root-causes")
down = j("p6-downstream")
par = j("p7-parameters")
pair = j("p8b-pairing-inputs")
surf = j("p9-surface-claims")
tok = j("p10-final20-token-control")
mut = j("p11-mutation-admissibility")
wf = j("p12-workflow-availability")
bind = j("p13-binding-facts")

receipts = []
for d in sorted(RC.iterdir()):
    if not d.is_dir() or not (d / "command.json").is_file():
        continue
    receipts.append({"label": d.name, "argv": json.loads((d / "command.json").read_text())["argv"],
                     "exit": int((d / "exit.txt").read_text().strip())})

out = {
    "standing": "READ-ONLY diagnosis by the actual Claude SOURCE AUTHOR origin "
                "823bf66b-e92a-4789-ab81-63a1a9dc371d. NOT the independent reviewer, NOT the blind "
                "consumer. Grants NO acceptance of the design, of consumer20, or of the final "
                "application. No source, consumer or live file was modified. The consumer Run was "
                "never reminted and no consumer code was executed.",
    "frozenSource": {
        "manifestSha256": custody["manifestSha256"],
        "manifestMatchesDeclared": custody["manifestMatchesDeclared"],
        "declaredFileCount": custody["declaredFileCount"],
        "verifiedFileCount": custody["verifiedFileCount"],
        "declaredTotalBytes": custody["declaredTotalBytes"],
        "verifiedTotalBytes": custody["verifiedTotalBytes"],
        "mismatchedManifestFiles": custody["mismatched"],
        "missingManifestFiles": custody["missing"],
        "everyManifestRowVerifiedByteExact":
            not custody["mismatched"] and not custody["missing"]
            and custody["verifiedFileCount"] == custody["declaredFileCount"]
            and custody["verifiedTotalBytes"] == custody["declaredTotalBytes"],
        "extraUntrackedOnDisk": custody["extraOnDisk"],
        "extraUntrackedNote":
            "One untracked __pycache__ .pyc compiled by a cpython-3.14 interpreter. The interpreter "
            "used here is 3.12.13 run with -B, which does not write bytecode, so this is not mine. "
            "It is not a manifest row and changes no manifest row.",
    },
    "inputHashes": custody["inputHashes"],
    "method": {
        "semanticHalf": "Root's root-blind20-proof-differences33.v1 derived the frozen reference "
                        "proof on the exact structurally admitted consumer inputs "
                        "(diagnose.py: transport decode -> open_run_closure -> R.derive with the "
                        "CONSUMER's own evaluationInputRefs -> structural diff). I re-ran the same "
                        "derivation to recover witness PREIMAGES, coverage payloads, atom inputs "
                        "and enumeration bindings, and compared at SET level where the field is a "
                        "canonical set.",
        "whySetLevel": "Index-aligned diffs over canonical sets overstate the disagreement: a "
                       "member present on both sides at a different position reads as several "
                       "field differences. rust-partial's 36 reported deficiency field differences "
                       "are one substitution of 4 records plus re-sorting.",
        "surfaceHalf": "Inert AST literals from consumer20's own final files; the FROZEN reference "
                       "protocol machine and the FROZEN owning schemas were executed. No consumer "
                       "code was run.",
    },
    "firstRefusalAndMasking": {
        "refusal": "EVALUATOR_COMPLETE_PROOF_REPLAY",
        "raisedBy": "evaluator_composition_model.v3.py compare_complete_replay, called from "
                    "evaluator_replay_model.v3.py replay() line 59",
        "masks": "replay() checks compare_complete_replay BEFORE the proofBundleId identity check "
                 "(line 60) and before EVALUATOR_EVIDENCE_REPLAY (66), EVALUATOR_SEAL_REPLAY (71) "
                 "and EVALUATOR_RUN_REPLAY (75). Those four joins are therefore UNESTABLISHED for "
                 "all five Runs - neither confirmed nor refuted.",
        "allFiveRuns": True,
        "transportAndStructuralAdmission": "ADMIT on all five (root replay summary).",
        "executionInputsLayer": "executionDeficiencies, evaluationInputRefs and "
                                "executionInputsDigest are EQUAL on all five. The disagreement has "
                                "moved entirely into the atom/witness/finding layer.",
    },
    "measuredDifferenceFamilies": {
        "reportedFieldPathTotals": fam["familyTotals"],
        "perRun": {n: {"differenceCount": r["differenceCount"],
                       "familyCounts": r["familyCounts"],
                       "consumerVerdict": r["consumerVerdict"],
                       "referenceVerdict": r["referenceVerdict"],
                       "findingCounts": [r["consumerFindingCount"], r["referenceFindingCount"]],
                       "predicateProofCounts": r["predicateProofCount"],
                       "executionDeficienciesEqual": r["executionDeficienciesEqual"]}
                 for n, r in fam["runs"].items()},
        "witnessFieldsThatEverDiffer": wit["differingWitnessFieldTotals"],
        "witnessFieldsThatNeverDiffer": [
            "schemaVersion", "programPredicateDigest", "matchingFactIds", "uncertainFactIds",
            "matchingImportRows", "uncertainImportRows", "countLimit", "childPredicateIds", "kind",
        ],
        "setLevelCauseSubstitution": root["causeSubstitutionTally"],
    },
    "rootCauses": [
        {
            "id": "RC-1",
            "title": "Atom sufficiency view omits the published recursive DEPENDS_ON dependency",
            "observedIn": ["syntax-data", "syntax-code", "rust", "rust-partial"],
            "evidence": {
                "atomNode": cov["syntax-data"]["differingPredicates"][0]["atomNode"],
                "consumerCitedCoverages":
                    cov["syntax-data"]["differingPredicates"][0]["consumerCoverageIds"],
                "referenceCitedCoverages":
                    cov["syntax-data"]["differingPredicates"][0]["referenceCoverageIds"],
                "partitionTheConsumerOmitted":
                    cov["syntax-data"]["differingPredicates"][0]["coverageDetail"],
                "consumerCauses":
                    cov["syntax-data"]["differingPredicates"][0]["consumerDeficiencyCauses"],
                "referenceCauses":
                    cov["syntax-data"]["differingPredicates"][0]["referenceDeficiencyCauses"],
            },
            "publishedLaw": {
                "selector": "docs/coop/design-corrections/foundation/"
                            "atom-evaluation-contract.v1.md line 88",
                "quote": "sufficiency_v2 view includes actual recursive native DEPENDS_ON "
                         "(reachability->calls@resolved-callee; clones->declares@syntactic) of the "
                         "same (S, T). ... Unrelated S->V coverage cannot heal a missing S->U "
                         "dependency. All su.causes are retained.",
                "registry": "docs/coop/design-corrections/native/native_evidence_model.v2.py:670-671 "
                            "DEPENDS_ON = {reachability: [calls@resolved-callee], "
                            "clones: [declares@syntactic]}",
                "referenceImplementation":
                    "atom_model.v1.py _build_sufficiency_view (primary + _depends_chain) and "
                    "_native_completeness run_suff, which emits coverage-unknown when the view is "
                    "unsatisfied",
            },
            "classification": "CONSUMER VIOLATED EXPLICIT PUBLISHED LAW",
            "consequence": "Consumer loses the coverage-unknown disclosure and the dependency "
                           "partition's own language-tier-unsupported record. In syntax-data the "
                           "consumer's deficiency set is a STRICT SUBSET of the reference's "
                           "(12 of 24); it never over-discloses here.",
            "requiredRemedy": "Consumer-side: include the recursive DEPENDS_ON partitions of the "
                              "same (S,T) in the sufficiency view, cite them, and retain the "
                              "resulting coverage-unknown. NO source change.",
            "remainingUncertainty": "I did not read the consumer's atom implementation, so I "
                                    "establish the OUTPUT deviation, not the line that causes it.",
        },
        {
            "id": "RC-2",
            "title": "Outgoing scope/coverage pairing finds no containing scope where the "
                     "reference finds one",
            "observedIn": ["syntax-code", "typescript", "rust", "rust-partial"],
            "evidence": {
                "consumerOnlyCauseTotal": root["causeSubstitutionTally"].get(
                    "consumer-only:uncovered-expected-source-subject"),
                "perRule": {n: {rid: {"consumerOnly": row["consumerOnlyCauses"],
                                      "referenceOnly": row["referenceOnlyCauses"]}
                                for rid, row in r["ruleLevel"].items()}
                            for n, r in root["runs"].items()},
                "inputsWerePresent": {n: {k: v for k, v in r.items() if k != "runId"}
                                      for n, r in pair.items() if n != "standing"},
            },
            "publishedLaw": {
                "selector": "atom-evaluation-contract.v1.md line 74",
                "quote": "Outgoing: only scopes/coverages at exact rung whose associated scope "
                         "contains the current source subject. Pairing is native "
                         "subject_scope_commitment of the actual subject-scope2 descriptor (no "
                         "invented commitment field) or explicit owner-derived coverageScopes "
                         "mapping. No one-scope/one-coverage fallback.",
                "referenceImplementation":
                    "atom_model.v1.py _coverages_for_current_source; empty sids -> "
                    "uncovered-expected-source-subject at line 1479",
            },
            "classification": "CONSUMER DEVIATION (high confidence); the pairing law is published "
                              "and every input it needs was present in the consumer's own export",
            "consequence": "19 spurious uncovered-expected-source-subject records across four "
                           "Runs; these are blocking causes, so they also drive RC-5.",
            "requiredRemedy": "Consumer-side pairing must use subject_scope_commitment or the "
                              "owner-derived coverageScopes mapping. NO source change.",
            "remainingUncertainty":
                "My own commitment-recomputation column returned 0 matches because I serialised "
                "subject_scope_commitment's return shape incorrectly; that column is a PROBE "
                "ARTIFACT and proves nothing. The load-bearing evidence is that every scope "
                "descriptor was in the consumer's export and the coverageScopes mapping was "
                "present and full-size (5/5, 5/5, 6/6).",
        },
        {
            "id": "RC-3",
            "title": "Binding availability: consumer reports no bindings where its own retained "
                     "plan has them",
            "observedIn": ["syntax-code", "rust"],
            "evidence": {n: {k: v for k, v in r.items() if k != "runId"}
                         for n, r in bind.items() if n != "standing"},
            "publishedLaw": {
                "causeVocabulary": "atom-evaluation-contract.v1.md line 147 registers both "
                                   "missing-relation-coverage and selector-unbound",
                "owedPrograms": "line 76 publishes owed programs = EnumerationPlan bindings for "
                                "capabilityForRelation[relation] (stated for the INCOMING "
                                "direction)",
                "referenceImplementation":
                    "atom_model.v1.py:1437 missing-relation-coverage only when there are NO "
                    "bindings at all; :1472 selector-unbound when bindings exist but none at the "
                    "subject universe",
            },
            "classification": "CONSUMER DEVIATION, factually settled",
            "factualSettlement":
                "In every case the consumer's OWN retained EnumerationPlan contains bindings for "
                "that capability - syntax-code/unresolved-edge: 1 unavailable binding at universe "
                "null; rust/clones -> clones-fact: 2 available; typescript: 1 available. "
                "missing-relation-coverage is therefore factually wrong on the consumer's own "
                "inputs, independent of any publication question.",
            "requiredRemedy": "Consumer-side. NO source change.",
            "narrowPublicationObservation":
                "The OUTGOING selection predicate between selector-unbound and "
                "missing-relation-coverage is published explicitly only for the incoming direction "
                "(line 76) and implied for outgoing (line 74). Root may wish to state it for "
                "outgoing too. This is a clarity point, NOT the cause of this disagreement, which "
                "is settled on the facts above.",
        },
        {
            "id": "RC-4",
            "title": "Composite predicate scopeIds are not the union of children",
            "observedIn": ["typescript"],
            "evidence": {
                "compositeNodes": root["runs"]["typescript"]["compositeNodes"],
                "consumerEmptyOnAll": root["runs"]["typescript"][
                    "compositeNodesWithEmptyConsumerScopeIds"],
                "referenceEqualsUnionOfTheConsumersOwnChildren": root["runs"]["typescript"][
                    "compositeNodesWhereReferenceIsChildUnion"],
                "consumerEqualsThatUnion": root["runs"]["typescript"][
                    "compositeNodesWhereConsumerIsChildUnion"],
            },
            "publishedLaw": {
                "selector": "evaluator-composition-contract.v3.md line 121",
                "quote": "scopeIds on predicateProof (not on witness) | Cset of scope2 ids the atom "
                         "completeness law returned | Cset of union of children's scopeIds",
                "referenceImplementation": "evaluator_composition_model.v3.py:135",
            },
            "classification": "CONSUMER VIOLATED EXPLICIT PUBLISHED LAW",
            "decisiveDetail": "On all 6 composite nodes the reference's scopeIds equal the union "
                              "of the CONSUMER'S OWN children's scopeIds. The two sides agree on "
                              "every leaf; only the propagation is missing.",
            "requiredRemedy": "Consumer-side. NO source change.",
            "remainingUncertainty": "None material.",
        },
        {
            "id": "RC-5",
            "title": "rust count-at-most indeterminate where the reference is true; 4 findings lost",
            "observedIn": ["rust"],
            "evidence": {
                "predicates": down["rustCountAtMost"]["predicates"],
                "everyValueDifferenceAlsoHasAWitnessDifference":
                    down["rustCountAtMost"]["everyValueDifferenceAlsoHasAWitnessDifference"],
                "findingCounts": [oth["rust"]["consumerFindingCount"],
                                  oth["rust"]["referenceFindingCount"]],
                "findingsOnlyInReference": oth["rust"]["findingsOnlyInReference"],
                "ruleResultOutcomes": oth["rust"]["ruleResultOutcomes"],
            },
            "publishedLaw": {
                "referenceImplementation":
                    "atom_model.v1.py:1616-1622 count-at-most is symmetric with none/exists: "
                    "FALSE if known > n, else UNK if uncertain or unknown or not complete, else "
                    "TRUE",
                "contract": "atom-evaluation-contract.v1.md line 105 and 129",
            },
            "classification": "DOWNSTREAM of RC-2/RC-3, not an independent count-at-most defect",
            "decisiveDetail":
                "Every count-at-most value difference coincides with a witness difference, and the "
                "consumer's extra blocking causes (uncovered-expected-source-subject, "
                "missing-relation-coverage) force unknown. Four other count-at-most predicates are "
                "indeterminate on BOTH sides, so the consumer is not uniformly wrong about the "
                "operator.",
            "consequence": "The consumer SUPPRESSES 4 findings the reference emits. This is the "
                           "only family where the consumer's output is materially weaker than the "
                           "reference's beyond disclosure loss.",
            "requiredRemedy": "Fixing RC-2/RC-3 is expected to resolve this; it should be "
                              "re-measured, not assumed.",
            "remainingUncertainty":
                "I did not independently confirm that repairing RC-2/RC-3 alone flips all four; "
                "the linkage is established by coincidence of witness differences, not by "
                "counterfactual execution.",
        },
        {
            "id": "RC-6",
            "title": "matchingImportCount under-reported in finding parameters",
            "observedIn": ["typescript"],
            "evidence": {"pairs": par["pairs"],
                         "consumerOnlyFindingIds": par["consumerOnlyFindingIds"],
                         "referenceOnlyFindingIds": par["referenceOnlyFindingIds"]},
            "publishedLaw": {
                "witnessField": "evaluator-composition-contract.v3.md line 119 - "
                                "matchingImportRows is the Cset of atom known ObservationAddressV1",
                "referenceImplementation":
                    "evaluator_composition_model.v3.py:172 matching_imports unions "
                    "matchingImportRows over all descendants; that count reaches the finding "
                    "parameter record",
            },
            "classification": "CONSUMER DEVIATION, independent of RC-1..RC-5",
            "decisiveDetail":
                "Both sides EMIT the finding (the import atom is true on both), the subject, "
                "messageCode, severity and citations agree, and the ONLY differing field is "
                "parameters.matchingImportCount: consumer 0, reference 1. An atom that evaluated "
                "true on an observed hit cannot have zero matching import rows.",
            "requiredRemedy": "Consumer-side. NO source change.",
            "remainingUncertainty":
                "Whether the consumer's atom returned no addresses or the composition failed to "
                "union them over descendants is not distinguishable from the outputs alone.",
        },
    ],
    "surfaceClaims": {
        "S-1": {
            "title": "Protocol capability tokens: blind19 finding PERSISTS in final20",
            "notInferred": "Root's control ran on consumer19. I repeated it on FINAL20's own bytes "
                           "rather than assuming it carries over.",
            "final20Phase3Sha256": tok["phase3Sha256"],
            "final20HelloAckLiteral": tok["helloAckFullLiteral"],
            "owningIdentityTokens": tok["owningIdentityTokens"],
            "publishedIn": {
                "nativeContract": surf["owningTokensInNativeContract"]["tokens"],
                "nativeContractSha256": surf["owningTokensInNativeContract"]["sha256"],
                "frozenModelHitCount": surf["owningTokensInFrozenModel"]["hitCount"],
            },
            "frozenMachineOnFinal20Bytes": tok["asFinal20Wrote"],
            "frozenMachineWithOwningTokensOnly": tok["withOwningTokensOnly"],
            "final20OwnClaim": tok["final20OwnClaim"],
            "frameSequenceMatchesFinal20Claim": tok["frameSequenceMatchesFinal20Claim"],
            "tokenListIsTheOnlyChange": tok["tokenListIsTheOnlyChange"],
            "firstRuleTraceDivergence": tok["firstRuleTraceDivergence"],
            "classification": "CONSUMER VIOLATED EXPLICIT PUBLISHED LAW",
            "masking": "The FAULT occurs at event index 2 (OpenUniverse, rule P3-34) with NO "
                       "source disclosure. Every later protocol phase becomes FAULT-absorb, so "
                       "final20's DONE/complete/stagesCompleted=1 claim and all later frame "
                       "semantics are UNESTABLISHED.",
            "requiredRemedy": "Consumer-side: HelloAck must advertise the four owning tokens. NO "
                              "source change - changing only the token list completes the trace.",
        },
        "S-2": {
            "title": "Mutation replay-scope ids: original vector still inadmissible; new probe is "
                     "admissible; the two retained artifacts disagree",
            "publishedRequestId": mut["publishedRequestId"],
            "publishedStepId": mut["publishedStepId"],
            "cases": mut["cases"],
            "admitCount": mut["admitCount"], "refuseCount": mut["refuseCount"],
            "olderVectorGenericKey": mut["declaredKeyInOlderVector"],
            "newerProbeKeys": mut["measuredKeysInNewProbe"],
            "twoRetainedArtifactsPublishDifferentGenericKeys":
                mut["twoRetainedArtifactsPublishDifferentGenericKeys"],
            "classification": "CONSUMER VIOLATED EXPLICIT PUBLISHED LAW in "
                              "output/vectors/mutation-keys.json; the newer "
                              "output/vectors/indep-mutation-surface.json is admissible",
            "fairCharacterisation":
                "The consumer DID correct the surface in the new probe (req1_7b31d0c4..., integer "
                "stepId 2, which ADMITS) but left the old vector in the final public retention "
                "unrepaired. Both are retained, and they publish DIFFERENT generic "
                "mutation-intent keys (20cbbcc1... vs f0ccf0a6...). Only the newer rests on an "
                "admissible preimage.",
            "requiredRemedy": "Consumer-side: withdraw or correct mutation-keys.json and "
                              "repair-descriptor.json, and state which key is authoritative. NO "
                              "source change.",
        },
        "S-3": {
            "title": "Multistep availability and aggregate termination are absent from retention",
            "artifactsMentioningAvailabilityOrMultistep":
                wf["artifactsMentioningAvailabilityOrMultistep"],
            "artifactsWithAggregateTermination": wf["artifactsWithAggregateTermination"],
            "phase7StandingRules": wf.get("phase7-standing-rules.json"),
            "classification": "UNDISCHARGED CHARTER AREA, not a demonstrated defect on either side",
            "detail": "phase7-standing-rules.json carries a single-step availability rule "
                      "(hasMultistepAvailability false) and NO retained artifact contains an "
                      "aggregateTermination record. I can neither confirm nor refute a multistep "
                      "availability or indeterminate-aggregation claim from the retained bytes.",
            "requiredRemedy": "Consumer-side evidence, or an explicit consumer statement that the "
                              "area is not discharged.",
        },
        "S-4": {
            "title": "Envelope schema-only results are not semantic joins",
            "rootReport": {
                "records": 20, "claimedSchemaAdmitContradictions": 0,
                "standing": "Bounded schema checks only, no semantic response/projection/host "
                            "conformance",
            },
            "classification": "SCOPE STATEMENT, not a finding",
            "detail": "20 CommandEnvelope records admitted against the frozen owning schema with "
                      "the exact validator establishes SHAPE only. It does not establish the "
                      "response/projection joins, host conformance, or that any envelope is "
                      "answerable by an admitted Run. Count checks and fragment-only laws do not "
                      "discharge the charter.",
        },
        "S-5": {
            "title": "Complete exact query execution remains BLOCKED",
            "detail": "Query execution through the public reference requires an admitted Run. All "
                      "five consumer Runs refuse semantic replay (see firstRefusalAndMasking), so "
                      "the query surface cannot be exercised on consumer20's own evidence. I did "
                      "NOT remint the consumer Run, and a reminted Run would not be their "
                      "acceptance.",
            "classification": "BLOCKED - no claim either way",
        },
    },
    "doesSource33NeedADesignChange": {
        "answer": "No design change is demonstrated as required by anything in this diagnosis.",
        "basis": "Every substantive discrepancy resolves to a consumer deviation from a published "
                 "law with a named selector, or is downstream of one, or is an undischarged "
                 "evidence area. RC-1 and RC-4 are explicit contract clauses; RC-3 is settled on "
                 "the consumer's own retained plan; RC-2's law is published and its inputs were "
                 "present; S-1 completes on the frozen machine when only the token list changes.",
        "narrowClarityCandidates": [
            "atom-evaluation-contract.v1.md: state the selector-unbound vs "
            "missing-relation-coverage predicate for the OUTGOING direction as explicitly as line "
            "76 states owed programs for incoming (RC-3). This is clarity, not a defect - the "
            "disagreement is already settled on the facts.",
        ],
        "noBlanketConformanceClaim": "I make no stage-count or suite-count conformance claim.",
    },
    "limitations": [
        "I am the SOURCE AUTHOR origin. This is diagnosis only. No acceptance of the design, of "
        "consumer20, or of the final application is given or implied.",
        "I did not read consumer20's atom or composition implementation. Every consumer "
        "classification is established from its OUTPUTS against published law, not from its code.",
        "The five Runs' proofBundleId, evidence, seal and run replay joins are UNESTABLISHED "
        "because compare_complete_replay refuses first.",
        "I did not remint any consumer Run and executed no consumer code. Complete query execution "
        "stays blocked (S-5).",
        "The charter (123+8+3) was NOT read in full. I assessed the specific surface claims named "
        "in my task plus the five proof disagreements. No full-charter claim is made.",
        "Root's blind19 controls (surface-parity, termination-joins, mutation-fields, "
        "query-record-assessment) were treated as diagnosis to assess, not authority. I re-measured "
        "the protocol-token claim on final20's own bytes (S-1) rather than inheriting it; I did "
        "NOT independently re-measure the other three, so they remain unconfirmed for final20.",
        "MISSING EVIDENCE: consumer-b.v20/final-public-artifact-manifest.json, named in my task as "
        "the exact public retention, DOES NOT EXIST at that path. I used "
        "consumer-b.v20/output/** directly and hashed every file I read. No substitute manifest was "
        "treated as authoritative.",
        "My p8 commitment-recomputation column is a probe artifact (wrong serialisation of "
        "subject_scope_commitment's return shape) and supports nothing; RC-2 rests on the other "
        "columns.",
        "I did not open independent33 or its reconciliation runtime, and did not contact or modify "
        "the blind origin.",
    ],
    "receipts": receipts,
    "nonZeroExitReceipts": [r["label"] for r in receipts if r["exit"] != 0],
    "nonZeroExitExplanation":
        "Authoring iterations kept rather than discarded: p2 (wrong witness source key), p3 and p5 "
        "(probe coding errors), p8 (unhashable dict). Each was corrected and re-run under a "
        "'b' label; both runs are retained.",
    "acceptance": None,
}

(HERE / "diagnosis.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
print(json.dumps({
    "frozenVerified": out["frozenSource"]["everyManifestRowVerifiedByteExact"],
    "rootCauses": [rc["id"] + ": " + rc["classification"] for rc in out["rootCauses"]],
    "surface": {k: v["classification"] for k, v in out["surfaceClaims"].items()},
    "designChangeNeeded": out["doesSource33NeedADesignChange"]["answer"],
    "receipts": len(receipts),
    "nonZero": out["nonZeroExitReceipts"],
}, indent=2))
sys.exit(0)
