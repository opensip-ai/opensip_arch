#!/usr/bin/env python3
"""Emit successor workflow-review + self-audit JSON from v1 rows and this audit."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from copy import deepcopy
from pathlib import Path

V1 = json.loads(
    Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1/output/workflow-review.json").read_text()
)
REQ = json.loads(
    Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/requirements.json").read_text()
)
PROBES = json.loads(
    Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v2/output/diagnostics/self_audit_probes.json").read_text()
)
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v2/output")

# Withdrawals of v1 reconstructed ADMITS. Historical v1 files are not edited.
WITHDRAW_TO_REFUSED = {
    "R-REPAIR-APPLY-KEY": {
        "semanticBehavior": "refused",
        "validatorDisposition": "refused",
        "schemaInhabitance": "not-the-selected-recipe",
        "owningSelector": "workflows-and-surfaces.md §1; repair.schema.json receiptIdempotencyKeyByStepKind/recipes/repair-apply: raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId})",
        "note": "WITHDRAWAL of v1 admitted-schema-or-digest. applyKey is {kind, repairPlanId, snapshotId, requestId, stepId}, not the published preimage. v1 accepted SHA-256 inequality of two arbitrary records. Invalid produced key, not unexercised behavior.",
        "evidenceClass": "invalid-produced-value",
        "v1Disposition": "admitted-schema-or-digest",
        "selfAudit": "withdrawal",
    },
    "R-PIVOT-ONLY-FINGERPRINTS": {
        "semanticBehavior": "refused",
        "validatorDisposition": "refused",
        "schemaInhabitance": "pass",
        "owningSelector": "workflows-and-surfaces.md §3 fingerprint population is the union of B and admitted E0–E4, including fingerprints present only in a pivot",
        "note": "WITHDRAWAL of v1 admitted-schema-inhabitance. Schema pass. Entry presence B=true and E0=true, so the fingerprint is not pivot-only. counts.DETECTION-DELTA=0 while classification is DETECTION-DELTA. Distinguishing fields do not substantiate the promised example.",
        "evidenceClass": "invalid-produced-value",
        "v1Disposition": "admitted-schema-inhabitance",
        "selfAudit": "withdrawal",
    },
    "R-CHAIN-ZERO-CONFIG-TO-RECEIPT": {
        "semanticBehavior": "refused",
        "validatorDisposition": "refused",
        "schemaInhabitance": "not-applicable",
        "owningSelector": "R-CHAIN-ZERO-CONFIG-TO-RECEIPT original verb: exhibited by executed traces, envelopes, and complete Runs together, not by a checklist sentence",
        "note": "WITHDRAWAL of v1 admitted-as-cited-standing-vector. The artifact is exactly a four-arrow checklist mapping to other files. Presence of those files is not the required exhibited chain.",
        "evidenceClass": "checklist-not-exhibition",
        "v1Disposition": "admitted-as-cited-standing-vector",
        "selfAudit": "withdrawal",
    },
    "R-MULTI-UNIT-MISSING-CAPS": {
        "semanticBehavior": "refused",
        "validatorDisposition": "refused",
        "schemaInhabitance": "not-applicable",
        "owningSelector": "native-capability-matrix.v2.json; enumeration-contract.v1.md; R-MULTI-UNIT-MISSING-CAPS zero-config selection over multiple workspace units",
        "note": "WITHDRAWAL of v1 admitted-as-cited-standing-vector. Kind is standaloneConfigVector. Vector lists units/advertised/missing names; it is not an executed zero-config selection. Citation is not the required reconstruction.",
        "evidenceClass": "citation-not-reconstruction",
        "v1Disposition": "admitted-as-cited-standing-vector",
        "selfAudit": "withdrawal",
    },
    "R-CANDIDATE-ONLY-CLONES": {
        "semanticBehavior": "refused",
        "validatorDisposition": "refused",
        "schemaInhabitance": "not-applicable",
        "owningSelector": "enumeration-contract.v1.md candidate-only cells store kinds=[] and must name candidateSourcePaths",
        "note": "WITHDRAWAL of v1 admitted-as-cited-standing-vector. Kind is standaloneConfigVector. Flags (cellKindsMustBeEmpty=true) are not a candidate-only cell representation with kinds=[] and candidateSourcePaths.",
        "evidenceClass": "citation-not-reconstruction",
        "v1Disposition": "admitted-as-cited-standing-vector",
        "selfAudit": "withdrawal",
    },
    "R-HOST-CAPTURED-VS-CANDIDATE": {
        "semanticBehavior": "refused",
        "validatorDisposition": "refused",
        "schemaInhabitance": "not-applicable",
        "owningSelector": "execution-inputs-contract.v1.md; enumeration-contract.v1.md candidate-only vs host-captured required work",
        "note": "WITHDRAWAL of v1 admitted-as-required-kind. Two gloss strings plus a selector are not host-captured vs candidate-only returns from retained observations. Kit content of the cited law exists; the consumer vector does not exhibit it.",
        "evidenceClass": "citation-not-reconstruction",
        "v1Disposition": "admitted-as-required-kind",
        "selfAudit": "withdrawal",
    },
}

# Keep refused; refine unexercised vs invalid and withdraw overstated grounds.
REFUSAL_REFINEMENTS = {
    "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": {
        "owningSelector": "identity-schemas.v3.json rust languageVersionBinding selectionLaw (committed SourceUnitOwnershipV1; ownership maps never enter body-language-version)",
        "note": "KEEP refused. Produced pair stamps two selection labels onto one already-equal L0 (edition 2018). No retained SourceUnitOwnershipV1 / ownership-map preimages, so the equality is tautological under the published exclusion of ownership from BLV. Insufficient produced pair, not merely unexercised.",
        "evidenceClass": "invalid-or-insufficient-produced-value",
        "selfAudit": "kept-refused-refined",
    },
    "R-RUN-UNSUPPORTED-GRAMMAR": {
        "owningSelector": "native-evidence.md §1.2 / identity-schemas.v3.json syntax languageVersionBinding: suffix with no bundled grammar refuses",
        "note": "KEEP refused as UNEXERCISED. Declared unsupported-file / no-bundled-grammar flag. Suffix/grammar-bundle admission was not run. Not an invalid produced admission value.",
        "evidenceClass": "unexercised-declared-firstRefusal",
        "selfAudit": "kept-refused-refined",
    },
    "R-HIDDEN-MISMATCH-PER-LANGUAGE": {
        "owningSelector": "R-HIDDEN-MISMATCH-PER-LANGUAGE first-refusal boundary per language",
        "note": "KEEP refused as UNEXERCISED. firstRefusal dicts for TypeScript and Rust; native context/universe admission not executed. Not an invalid produced admission value.",
        "evidenceClass": "unexercised-declared-firstRefusal",
        "selfAudit": "kept-refused-refined",
    },
    "R-CLONES-NEGATIVE-VECTORS": {
        "owningSelector": "relation-payload-schemas.v2.json anchorLaw / bodyIdentityJoin",
        "note": "KEEP refused as UNEXERCISED. firstRefusal values are hand-raised AdmissionError wrappers / assigned dicts, not executed body-identity or fact admission.",
        "evidenceClass": "unexercised-declared-firstRefusal",
        "selfAudit": "kept-refused-refined",
    },
    "R-REPAIR-AUTHORITY-PER-TARGET": {
        "owningSelector": "evaluator-composition-contract.v3.md unmatched; RepairPlanDescriptor unmatched findings are not lawful targets (REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE)",
        "note": "KEEP refused as UNEXERCISED. Negative is a constructed firstRefusal dict; positive is a matched:true flag. Not an executed fingerprint correspondence join.",
        "evidenceClass": "unexercised-declared-firstRefusal",
        "selfAudit": "kept-refused-refined",
    },
    "R-MIN-RESOLUTION-THREE-LEVELS": {
        "owningSelector": "atom-evaluation-contract.v1.md; identity-and-evidence.md §4",
        "note": "KEEP refused. Type level lacks qualifying. Resolved measured insufficientValue=false agrees with kit complete-absence; insufficientExpected=indeterminate is an incorrect produced label. Incomplete implementation of existing law, plus one invalid expected.",
        "evidenceClass": "incomplete-existing-law-plus-invalid-expected",
        "selfAudit": "kept-refused-refined",
    },
    "R-MIN-RESOLUTION-REPAIR-EVIDENCE": {
        "owningSelector": "atom-evaluation-contract.v1.md; identity-and-evidence.md §4; RepairPlanV1 evidenceRequirements",
        "note": "KEEP refused. Vector is prose tiedTo min-resolution.json, not repair-evidence records. Incomplete implementation of existing law.",
        "evidenceClass": "incomplete-existing-law",
        "selfAudit": "kept-refused-refined",
    },
    "R-SCOPE-POLICY-ONLY-COMPARISON": {
        "owningSelector": "evaluator3/comparison-result.schema.json; R-SCOPE-POLICY-ONLY-COMPARISON only bound ScopeDocumentV1 changes",
        "note": "KEEP refused as INVALID PRODUCED VALUE. Schema pass. baselineContext.scopeDigest equals currentContext.scopeDigest (both 5abc279f…) while contextDelta.scopeChanged=true. Not unexercised.",
        "evidenceClass": "invalid-produced-value",
        "selfAudit": "kept-refused-refined",
    },
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": {
        "owningSelector": "query-projection-contract.v3.md §§3,5,6,7; evaluator3/graph-query.schema.json; workflows-and-surfaces.md §8",
        "note": "KEEP refused as INVALID PRODUCED VALUES: all four graph ops request file@enumerated (graph-projectable no) and were answered as GraphQueryResponseV1 success; failure envelope is QUERY.VIEW_UNKNOWN, not QUERY.RELATION_UNSUPPORTED. WITHDRAW v1 cursor-'c1' claim: artifact nextCursor is null, which §5 allows for a complete page. WITHDRAW v1 empty-coverageIds independent ground: §6 derives coverageIds from selected views, not a universal nonempty rule. underlyingRunAdmissionUnverified remains correctly labelled and does not license answering an unsupported relation.",
        "evidenceClass": "invalid-produced-value",
        "selfAudit": "kept-refused-with-withdrawn-grounds",
    },
}

ADMIT_CORRECTIONS = {
    "R-REPAIR-DESCRIPTOR": {
        "semanticBehavior": "schema-inhabitance-identity-not-selected-H",
        "validatorDisposition": "admitted-schema-inhabitance",
        "schemaInhabitance": "pass",
        "owningSelector": "evaluator3/repair.schema.json#/$defs/RepairPlanV1; H('workflow.repair-plan', descriptor)",
        "note": "CORRECTION of v1 admitted-schema-or-digest. RepairPlanV1/RepairPlanDescriptor inhabitance and five-field closedWorld projection shape pass. repairPlanId is not H('workflow.repair-plan', descriptor) (claimed b4ab1ea5…, selected d1c17ff9…). Stock identity string, not the committed recipe. Not refused: original verb is the descriptor projection, which inhabits the selected schema.",
        "selfAudit": "grade-correction",
    },
    "R-MUTATION-REPLAY-SCOPE": {
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-schema-inhabitance",
        "schemaInhabitance": "pass",
        "owningSelector": "invocation-record.schema.json#/$defs/MutationReplayScopeV1; repair.schema.json admissibleGenericFieldDomain excludes repair-apply",
        "note": "KEEP admitted as reconstructed MutationReplayScopeV1 with operation=purge (not repair-apply). CORRECTION: v1 paired this with SHA-256 inequality against an arbitrary applyKey; that pairing is withdrawn with R-REPAIR-APPLY-KEY. H('workflow.mutation-intent', scope) is the receipt key, not a requirement that this vector mint it.",
        "selfAudit": "grade-correction",
    },
    "R-CMP-MISSING": {
        "owningSelector": "evaluator3/comparison-result.schema.json; comparisonPerformed=false, pivots unavailable, wholeIndeterminateReason=required-evidence-unavailable",
        "note": "KEEP admitted as schema inhabitance of the missing-evidence case. Distinguishing fields substantiate the example vs evidence-changed. CORRECTION: comparisonResultId is not H('workflow.comparison', descriptor).",
        "selfAudit": "grade-correction",
        "semanticBehavior": "schema-inhabitance-not-full-comparison-engine",
        "validatorDisposition": "admitted-schema-inhabitance",
    },
    "R-CMP-EVIDENCE-CHANGED": {
        "owningSelector": "evaluator3/comparison-result.schema.json; comparisonPerformed=true, evidenceAvailabilityChanged=true, wholeIndeterminateReason=evidence-availability-changed",
        "note": "KEEP admitted as schema inhabitance of the evidence-changed case. Distinguishing fields substantiate the example vs missing. CORRECTION: comparisonResultId is not H('workflow.comparison', descriptor).",
        "selfAudit": "grade-correction",
        "semanticBehavior": "schema-inhabitance-not-full-comparison-engine",
        "validatorDisposition": "admitted-schema-inhabitance",
    },
    "R-CMP-EMPTY-RESULT": {
        "owningSelector": "evaluator3/comparison-result.schema.json; entries=[], zeroFindings=true, verdict=pass",
        "note": "KEEP admitted as schema inhabitance of the empty-result case. CORRECTION: comparisonResultId is not H('workflow.comparison', descriptor).",
        "selfAudit": "grade-correction",
        "semanticBehavior": "schema-inhabitance-not-full-comparison-engine",
        "validatorDisposition": "admitted-schema-inhabitance",
    },
    "R-BASELINE-AUDIT": {
        "owningSelector": "evaluator3/baseline-artifact.schema.json; workflows-and-surfaces.md §2 embedded contextDocuments",
        "note": "KEEP admitted as schema inhabitance of BaselineArtifact with embedded contextDocuments. CORRECTION: baselineId is not H('workflow.baseline', descriptor).",
        "selfAudit": "grade-correction",
        "semanticBehavior": "schema-inhabitance-not-full-comparison-engine",
        "validatorDisposition": "admitted-schema-inhabitance",
    },
    "R-E0-VS-E1-E3": {
        "owningSelector": "workflows-and-surfaces.md §3 E0 prior detector vs E1–E3 re-evaluation of current retained evidence",
        "note": "KEEP admitted as schema inhabitance. pivotsAvailable and presence fields distinguish E0-available from E1–E3-available. Not a comparison engine. counts.UNCHANGED=0 against UNCHANGED entries is noted and does not erase the pivot distinction.",
        "selfAudit": "kept-admitted-with-limitation",
        "semanticBehavior": "schema-inhabitance-not-full-comparison-engine",
        "validatorDisposition": "admitted-schema-inhabitance",
    },
    "R-INVOCATION-DISCLOSURE": {
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-as-required-kind",
        "schemaInhabitance": "not-a-command-envelope",
        "owningSelector": "command-inventory.v3.json commands[] (45), query formats/parityFields",
        "note": "CORRECTION of v1 admitted-schema-envelope. Artifact is an inventory-derived disclosure (commandCount=45, query formats from command-inventory.v3), not a CommandEnvelope instance. Meets the original disclosure verb.",
        "selfAudit": "grade-correction",
        "consumerArtifact": "envelopes/invocation-disclosure.json",
    },
    "R-FAILURE-ENVELOPES-D9": {
        "consumerArtifact": "envelopes/failure-d9-complete.json",
        "owningSelector": "evaluator3/command-envelope.schema.json; d9-exit-contract.v1.14.json#/classToExitCode",
        "note": "KEEP admitted as complete CommandEnvelope kind=failure (not a termination fragment). CORRECTION of v1 consumerArtifact path envelopes/d9-complete.json → actual envelopes/failure-d9-complete.json. exitCode 1 derives from policy-failed.",
        "selfAudit": "path-correction",
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-schema-envelope",
        "schemaInhabitance": "pass",
    },
    "R-PROMISE-VS-AVAILABILITY": {
        "owningSelector": "native-evidence.md advertised cells vs capability-manifest / release declaration",
        "note": "KEEP admitted-as-cited-standing-vector AFTER content review of native-evidence.md (product promise of cells vs installed capabilities). Not mere file presence.",
        "selfAudit": "content-reviewed",
        "semanticBehavior": "cited-distinction-content-reviewed",
        "validatorDisposition": "admitted-as-cited-standing-vector",
    },
    "R-SEMANTIC-VS-OPERATIONAL-AUTHORITY": {
        "owningSelector": "identity-and-evidence.md §3; workflows-and-surfaces.md operational receipts / grants",
        "note": "KEEP admitted-as-cited-standing-vector AFTER content review. Semantic identities ≠ operational authority is in the cited kit text.",
        "selfAudit": "content-reviewed",
        "semanticBehavior": "cited-distinction-content-reviewed",
        "validatorDisposition": "admitted-as-cited-standing-vector",
    },
    "R-MUTATION-VS-ANALYSIS-STEPS": {
        "owningSelector": "workflows-and-surfaces.md analysis may seal run3; mutation/repair-apply/import/native-preparation/test-execution follow published non-seal rules",
        "note": "KEEP admitted-as-cited-standing-vector AFTER content review of workflows-and-surfaces.md / repair.schema.json step-kind bindings.",
        "selfAudit": "content-reviewed",
        "semanticBehavior": "cited-distinction-content-reviewed",
        "validatorDisposition": "admitted-as-cited-standing-vector",
    },
    "R-SUBSYSTEM-OWNERS": {
        "owningSelector": "owner map citing evaluator3 comparison-result, baseline-artifact, command-envelope, TypeScriptConfigGraphV1, query-projection-contract.v3, RepairPlanV1",
        "note": "KEEP admitted-as-cited-standing-vector AFTER content review of the owner map against kit schema owners. Observable is an owner map cited to kit.",
        "selfAudit": "content-reviewed",
        "semanticBehavior": "cited-distinction-content-reviewed",
        "validatorDisposition": "admitted-as-cited-standing-vector",
    },
    "R-EMPTY-PARTIAL-UNAVAILABLE-MISSING": {
        "owningSelector": "enumeration-contract.v1.md complete-empty vs partial vs missing retained bytes; candidate-only kinds=[] is not complete-empty",
        "note": "KEEP admitted-as-cited-standing-vector AFTER content review. Four named states match kit distinctions. Exhibition is by citation to other artifacts, which the standingRule observable allows; a single label for all four was not used.",
        "selfAudit": "content-reviewed",
        "semanticBehavior": "cited-distinction-content-reviewed",
        "validatorDisposition": "admitted-as-cited-standing-vector",
    },
    "R-DETECTOR-COMPAT-FILE": {
        "owningSelector": "workflows-and-surfaces.md §2 `.opensip/detector-compatibility.json` vs closure.manifestDigest component manifest body",
        "note": "KEEP admitted-as-required-kind. Vector distinguishes listing file vs manifest body; cited kit owners were read and contain that split. Observable is that distinction, not a signed-tree execution.",
        "selfAudit": "content-reviewed",
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-as-required-kind",
    },
    "R-CONFIG-SYNTHESIZED": {
        "owningSelector": "native-evidence.schemas.v2.json#/$defs/TypeScriptConfigGraphV1 entryConfigPath null exactly when synthesized; tsconfigGraphHash=SHA-256(C(graph))",
        "note": "KEEP admitted-config-vector. Independently recomputed digest; entryConfigPath=null, nodes=[].",
        "selfAudit": "reverified",
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-config-vector",
    },
    "R-CONFIG-CUSTOM-MULTI-BASE": {
        "owningSelector": "native-evidence.schemas.v2.json#/x-opensip-config-node-kind-law; TypeScriptConfigGraphV1 extendsResolved sequence later-wins; repeated bases retained",
        "note": "KEEP admitted-config-vector. Custom entry tsconfig.app.json kind=other; extendsResolved [strict, base]; base also reached via strict. Digest independently recomputed.",
        "selfAudit": "reverified",
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-config-vector",
    },
    "R-CONFIG-JS-SHARED-BASE": {
        "owningSelector": "native-evidence.schemas.v2.json jsconfig.json kind=jsconfig inheriting another filename (tsconfig.shared.json kind=other)",
        "note": "KEEP admitted-config-vector. Digest independently recomputed.",
        "selfAudit": "reverified",
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-config-vector",
    },
    "R-JS-CLONE-BODY-THROUGH-TS": {
        "owningSelector": "relation-payload-schemas.v2.json languageIdIsNotTheProviderLanguage",
        "note": "KEEP admitted-computed-identity. Independently rebuilt L0 identities; javascript ≠ typescript over the same bytes.",
        "selfAudit": "reverified",
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-computed-identity",
    },
    "R-REPLAY-THREE-VALUED": {
        "owningSelector": "identity-and-evidence.md §4 exists otherwise indeterminate",
        "note": "KEEP admitted-atom-evaluation. exists with no Coverage independently indeterminate.",
        "selfAudit": "reverified",
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-atom-evaluation",
    },
    "R-D9-EXTENSION-PRECEDENCE": {
        "owningSelector": "d9-exit-contract.v1.14.json#/classToExitCode; CommandEnvelope stores derived exitCode",
        "note": "KEEP admitted. Selected map equals inherited classToExitCode.",
        "selfAudit": "reverified",
        "semanticBehavior": "admitted",
        "validatorDisposition": "admitted-schema-envelope",
        "schemaInhabitance": "pass",
    },
}

rows = []
for r in V1["originalRequirementIds"]:
    nr = deepcopy(r)
    rid = nr["id"]
    if rid in WITHDRAW_TO_REFUSED:
        nr.update(WITHDRAW_TO_REFUSED[rid])
        nr["v1ValidatorDisposition"] = WITHDRAW_TO_REFUSED[rid]["v1Disposition"]
    elif rid in REFUSAL_REFINEMENTS:
        nr.update({k: v for k, v in REFUSAL_REFINEMENTS[rid].items() if k != "selfAudit"})
        nr["v1ValidatorDisposition"] = "refused"
        nr["selfAudit"] = REFUSAL_REFINEMENTS[rid]["selfAudit"]
        nr["evidenceClass"] = REFUSAL_REFINEMENTS[rid]["evidenceClass"]
    elif rid in ADMIT_CORRECTIONS:
        nr.update({k: v for k, v in ADMIT_CORRECTIONS[rid].items() if k != "selfAudit"})
        nr["selfAudit"] = ADMIT_CORRECTIONS[rid]["selfAudit"]
        nr["v1ValidatorDisposition"] = r["validatorDisposition"]
    else:
        nr["v1ValidatorDisposition"] = r["validatorDisposition"]
        nr["selfAudit"] = "unchanged-this-audit" if r["consumerThisPassStatus"] != "reconstructed-this-pass" else "reverified-or-unchanged-admit"
        if r["consumerThisPassStatus"] == "reconstructed-this-pass" and r["validatorDisposition"] != "refused":
            if not nr.get("owningSelector"):
                nr["owningSelector"] = r.get("owningSelector") or r.get("consumerArtifact")
    rows.append(nr)

assert [r["id"] for r in rows] == [r["id"] for r in V1["originalRequirementIds"]]
assert len(rows) == 134

recon = [r for r in rows if r["consumerThisPassStatus"] == "reconstructed-this-pass"]
refused = [r for r in recon if r["validatorDisposition"] == "refused"]
admitted = [r for r in recon if r["validatorDisposition"] != "refused"]
withdrawals = [r for r in recon if r.get("selfAudit") == "withdrawal"]

scope_counts = Counter(r["reviewedScope"] for r in rows)
disp_counts = Counter(r["validatorDisposition"] for r in rows)
pass_counts = Counter(r["consumerThisPassStatus"] for r in rows)

charter_ids = [r["id"] for r in REQ["standing"]] + [r["id"] for r in REQ["requirements"]] + [r["id"] for r in REQ["futureQualification"]]
assert [r["id"] for r in rows] == charter_ids

first_refused = refused[0]["id"] if refused else None  # charter order among reconstructed

new_review = {
    "validatorId": "consumer-b.v12-kit-validator.v1",
    "continuation": "same-session bounded self-audit of workflow-review.v1; not a new origin; not a pilot admission review; does not reaffirm prior PILOT_ADMITS",
    "standing": "Kit-only reconstruction validator. Not root admission oracle. Not product qualification. Not whole-consumer ACCEPT.",
    "outcome": "WORKFLOW_SCOPE_REFUSED",
    "outcomeScope": "Self-audit of the completed scope-v2 workflow/vector reconstruction (48 claimed reconstructed IDs). Frozen Run admission and other-Run replay remain out of scope and were not used as admission or refusal of those Runs.",
    "historicalV1": {
        "path": "/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1/output/workflow-review.json",
        "outcome": "WORKFLOW_SCOPE_REFUSED",
        "notEdited": True,
        "retainedCopy": "diagnostics/v1-originals/workflow-review.json",
    },
    "newMustIssues": [],
    "newShouldIssues": [],
    "newMustIssuesEmptyJustification": "All refusals and withdrawals are consumer missing-law implementations or overstated grades of existing published selectors. No absent or contradictory normative law blocked reconstruction. Genuinely absent/contradictory laws: none.",
    "absentOrContradictoryLaws": [],
    "incompleteConsumerImplementationOfExistingLaws": [r["id"] for r in refused],
    "inputHashes": {
        "consumerInputManifestSha256": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
        "parentSubjectSha256": "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb",
        "subjectFiles": "PASS 80/80",
        "requirementsJsonSha256": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
        "snapshotManifest": {
            "path": "/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v1/snapshot-manifest.json",
            "sha256": "9fb3d13f0d58a65bea8aae46600ceeff12842e7f46c8b94b59214c831f23051c",
            "expected": "9fb3d13f0d58a65bea8aae46600ceeff12842e7f46c8b94b59214c831f23051c",
            "fileCount": 224,
            "hashVerification": "PASS",
        },
    },
    "consumerSelfVerdict": "SCOPE_INCOMPLETE",
    "consumerSelfVerdictNotOracle": True,
    "executedProbes": {
        "path": "diagnostics/self_audit_probes.json",
        "probeCount": PROBES["probeCount"],
        "passCount": PROBES["passCount"],
        "failCount": PROBES["failCount"],
        "note": "Probe counts are not conformance counts. Historical v1 114/101/13 likewise.",
        "v1ProbesRetained": "diagnostics/v1-originals/workflow_scope_probes.json",
        "diagnosticCorrection": "D-CORR-SA-1: detector-compat kit substring initially omitted markdown backticks around closure.manifestDigest; original fail preserved in diagnostics/self_audit_probes.original-detector-backtick-fail.json. Kit text does contain the listing-vs-manifest split.",
    },
    "firstActualRefusal": {
        "id": first_refused,
        "order": "first refused reconstructed ID in original charter order",
        "selector": refused[0]["owningSelector"] if refused else None,
        "observed": refused[0]["note"] if refused else None,
    },
    "refusedReconstructedIds": [r["id"] for r in refused],
    "withdrawnV1Admits": [r["id"] for r in withdrawals],
    "admittedReconstructedIds": [r["id"] for r in admitted],
    "v1AggregateCorrection": {
        "v1MarkdownTableSummedTo": 137,
        "v1MarkdownClaimedTotal": 134,
        "error": "v1 table listed out-of-scope frozen Run/property/replay as 39 AND futureQualification as 3. validatorDisposition out-of-scope already included the 3 futureQualification rows (24 frozen-run + 12 frozen-replay + 3 future = 39). Double-count of 3.",
        "correctedReviewedScope": {
            "in-scope-reconstructed-claim": 48,
            "standing-of-consumer-continuation-not-re-executed-here": 24,
            "out-of-scope-frozen-run": 24,
            "notReached-historical-vector": 23,
            "out-of-scope-frozen-run-replay": 12,
            "futureQualification": 3,
            "total": 134,
        },
    },
    "originalRequirementIds": rows,
    "notReached": V1.get("notReached"),
    "reproductionCommand": "/tmp/opensip-architecture-review-env/bin/python -I -B /tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-review.v2/output/diagnostics/self_audit_probes.py",
    "limitations": [
        "Frozen Run admission is out of scope; store hashes verified unchanged.",
        "Probe counts are not conformance counts.",
        "Comparison/baseline/repairPlan committed ids were measured against H recipes; mismatch is recorded. Comparison CASE rows remain schema-inhabitance where distinguishing fields hold.",
        "No whole-consumer ACCEPT.",
    ],
}

disp = {
    "count": 134,
    "rows": rows,
    "validatorDisposition": dict(disp_counts),
    "reviewedScope": dict(scope_counts),
    "consumerThisPassStatus": dict(pass_counts),
    "reconstructed": {
        "n": 48,
        "refused": len(refused),
        "admitted": len(admitted),
        "withdrawnV1Admits": [r["id"] for r in withdrawals],
    },
}

(OUT / "diagnostics" / "id-dispositions.json").write_text(json.dumps(disp, indent=2) + "\n")
(OUT / "workflow-review.json").write_text(json.dumps(new_review, indent=2) + "\n")

audit = {
    "validatorId": "consumer-b.v12-kit-validator.v1",
    "kind": "bounded-self-audit-of-workflow-review.v1",
    "historicalV1NotEdited": True,
    "outcomeAfterAudit": "WORKFLOW_SCOPE_REFUSED",
    "snapshotVerification": "PASS 224/224",
    "kitVerification": "PASS 80/80",
    "probeCountsAreNotConformanceCounts": True,
    "probes": {
        "path": "diagnostics/self_audit_probes.json",
        "probeCount": PROBES["probeCount"],
        "passCount": PROBES["passCount"],
        "failCount": PROBES["failCount"],
    },
    "withdrawalsOfV1Admits": [
        {
            "id": k,
            "v1Disposition": v["v1Disposition"],
            "v2Disposition": "refused",
            "evidenceClass": v["evidenceClass"],
            "reason": v["note"],
        }
        for k, v in WITHDRAW_TO_REFUSED.items()
    ],
    "keptRefusalsRefined": [
        {
            "id": k,
            "evidenceClass": v["evidenceClass"],
            "reason": v["note"],
        }
        for k, v in REFUSAL_REFINEMENTS.items()
    ],
    "withdrawnV1RefusalGroundsNotWholeRow": [
        {
            "id": "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
            "withdrawnGrounds": [
                "cursor token 'c1' — artifact nextCursor is null; §5 empty nextCursor is lawful for a complete page",
                "empty coverageIds as independent defect — §6 derives coverageIds from selected views, not a universal nonempty rule",
            ],
            "remainingGrounds": [
                "file@enumerated is not graph-projectable; success responses are invalid produced values",
                "failure envelope domainDetail is QUERY.VIEW_UNKNOWN not QUERY.RELATION_UNSUPPORTED",
            ],
        }
    ],
    "overstatedV1GradesCorrectedWithoutRefusal": [
        {
            "id": k,
            "correction": v["note"],
        }
        for k, v in ADMIT_CORRECTIONS.items()
        if v.get("selfAudit") in ("grade-correction", "path-correction")
    ],
    "identityRecipes": {
        "repairApplyKey": "consumer applyKey is not C({operation, projectId, repairPlanId, baseSnapshotId}); row refused",
        "mutationReplayScope": "schema-valid MutationReplayScopeV1 operation=purge; selected generic record, not an H digest of an arbitrary pair",
        "repairPlanId": "not H('workflow.repair-plan', descriptor); schema inhabitance retained",
        "comparison2AndBaseline2": "claimed ids are not H of the descriptors; CASE distinguishing fields still hold for missing/evidence-changed/empty/E0-vs-E1-E3/baseline-audit",
    },
    "v1AggregateCorrection": new_review["v1AggregateCorrection"],
    "absentOrContradictoryLaws": [],
    "counts": {
        "reconstructedRefused": len(refused),
        "reconstructedAdmitted": len(admitted),
        "reviewedScope": dict(scope_counts),
        "validatorDisposition": dict(disp_counts),
        "total": 134,
    },
}
(OUT / "review-self-audit.json").write_text(json.dumps(audit, indent=2) + "\n")

print(json.dumps({
    "reconstructed": len(recon),
    "refused": [r["id"] for r in refused],
    "admittedN": len(admitted),
    "withdrawals": [r["id"] for r in withdrawals],
    "disp": dict(disp_counts),
    "scope": dict(scope_counts),
    "firstRefused": first_refused,
    "ids134": len(rows),
}, indent=2))
