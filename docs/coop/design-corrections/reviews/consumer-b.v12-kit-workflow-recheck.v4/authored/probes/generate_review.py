#!/usr/bin/env python3
"""Emit workflow-review.md/json from independent measurements + original 134 IDs."""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v4/output")
REQ = json.loads(Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/requirements.json").read_text())
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-workflow-recheck.v4/consumer-snapshot")
author = json.loads((SNAP / "workflow-completion-review.json").read_text())

EST48 = [d["id"] for d in author["all48Disposition"]]
assert len(EST48) == 48

INCOMPLETE = {
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
    "R-CHAIN-ZERO-CONFIG-TO-RECEIPT",
}

# 134 by id
all_ids = []
for r in REQ["standing"] + REQ["requirements"] + REQ["futureQualification"]:
    all_ids.append(r)
assert len(all_ids) == 134

by_id = {r["id"]: r for r in all_ids}

STANDING_CONTINUATION = {
    "S-FRESH-ORIGIN", "S-NOT-PRODUCT", "S-KIT-ONLY", "S-MANIFEST-VERIFY", "S-NO-ORACLE",
    "S-MISSING-DEP-IS-CUSTODY", "S-PROFILE-CURRENT", "S-CONTINUATION",
    "R-FIVE-CONTRACTS-INDEX", "R-SOURCE-MAP-SCOPE", "R-CVE1-TYPES-AVAILABLE",
    "R-VALID-VS-INVALID-VS-EXPLANATORY", "R-MEASURED-NOT-COUNTS", "R-NEGATIVE-FIRST-REFUSAL",
    "R-DISTINGUISH-FOUR-BOUNDARIES", "R-HELPER-KIT-ONLY",
    "R-IDENTIFY-GAPS", "R-FREEDOM-VS-MISSING", "R-BLOCKER-NOT-ADJUST",
    "R-DELIVER-MD-JSON", "R-VERDICT-ENUM", "R-MUST-SHOULD-ADVISORY",
    "R-NO-ACCEPT-IF-INCOMPLETE", "R-NO-QUALIFICATION-CLAIM",
}

FROZEN_RUN = {
    "R-RUN-TS", "R-RUN-TS-NODE-MODULES", "R-RUN-TS-CONFIG-DEPS",
    "R-RUN-RUST", "R-RUN-RUST-MIXED-EDITION", "R-RUN-RUST-TARGET-EDITION",
    "R-RUN-RUST-BODY-DIALECT", "R-RUN-RUST-SAME-FILE-TWO-EDITIONS",
    "R-RUN-RUST-PARTIAL-EMPTY-CLONES", "R-RUN-RUST-HASH-MARKER",
    "R-RUN-RUST-LARGE-EDITION-MAP", "R-RUN-RUST-VERSION-COMPONENT",
    "R-RUN-FILE-FACT-INVENTORY", "R-RUN-CLONES-L0-AND-NORMALIZED", "R-RUN-CLONES-CUSTODY",
    "R-RUN-SYNTAX-CODE", "R-RUN-SYNTAX-DATA", "R-RUN-NO-COMPILER-UNIT",
    "R-RUN-UNAVAILABLE-SEMANTIC", "R-RUN-NONCEMPTY-CONTEXT",
    "R-SCOPEDOCUMENT-IN-ANALYSIS-SPEC", "R-IMPORTED-PAYLOAD-IN-GRAPH",
    "R-CLONE-DEFICIENCY-PAIRING", "R-NATIVE-PREIMAGE-JOINS",
}

FROZEN_REPLAY = {
    "R-VALIDATE-OWNING-SCHEMA", "R-INDEPENDENT-CLOSURE-JOINS",
    "R-RETAINED-ARTIFACTS-IN-CLOSURE", "R-SELECTED-PROVIDER-CONTEXT",
    "R-REPLAY-AFTER-ADMISSION", "R-REPLAY-ENUM-AND-IDS",
    "R-REPLAY-PREDICATE-WITNESS-VERDICT", "R-REPLAY-NO-CALLER-TRUTH",
    "R-REPLAY-COMPARE-BUNDLE", "R-REPLAY-EXPORT", "R-REPLAY-TAMPER",
    "R-ROOT-ADMISSION-EXPORT",
}

FUTURE = {"F-OS-COMPILER-CRYPTO-SQLITE", "F-SYNTHETIC-TCB", "F-AUTH-HOST"}

# artifacts for 48
ART = {d["id"]: d.get("artifact") for d in author["all48Disposition"]}

MEASURE = {
    "R-ENVELOPE-CONFIG-INPUT": "CommandEnvelope major3 kind=failure schema-valid; no run field; errors nonempty; requestId req1_+32hex. Selector: evaluator3 command-envelope.schema.json.",
    "R-ENVELOPE-EXTERNAL-INPUT": "Same failure composition on envelopes/retained-external-input.json; stock schema PASS.",
    "R-ENVELOPE-HOST-INVALID": "Same failure composition on envelopes/host-invalid-internal.json; stock schema PASS.",
    "R-ENVELOPE-PRODUCER-BOUNDARY": "Same failure composition on envelopes/producer-boundary.json; stock schema PASS.",
    "R-PUBLIC-FROM-INTERNAL-REFUSAL": "Public failure envelope projected from internal refusal; termination.domainDetail.code ENVELOPE.KIND; kind=failure prohibits run. Schema PASS.",
    "R-PINNED-PURGE": "Pinned-purge refusal envelope schema-valid CommandEnvelope failure.",
    "R-PURGE-REPLAY-OUTPUT-FAILURE": "Purge/replay required-output failure envelope schema-valid.",
    "R-FAILURE-ENVELOPES-D9": "Complete D9 composition: schemaFamily/schemaMajor/kind/requestId/termination/exitCode/errors; policy-failed exitCode=1 matches inherited classToExitCode; no run field. errorCode omitted is lawful for policy-failed (runId present).",
    "R-PUBLIC-TERMINATION-EXAMPLES": "Six StepTermination examples (success, policy-failed, request-rejected, indeterminate, operational-failed, interrupted) each stock-valid against common.schema.json#/$defs/StepTermination. Wrapper is examples+owningRecord, not a CommandEnvelope.",
    "R-D9-EXTENSION-PRECEDENCE": "Independent kit d9-exit-contract.v1.14.json classToExitCode equals vector inherited and selected tables {0,1,2,3,4,130}.",
    "R-SINGLE-STEP": "InvocationRecord major3 analyze single orderedSteps[0] schema-valid against evaluator3 invocation-record.",
    "R-MULTI-STEP-DIFFERENT-SELECTIONS": "Two orderedSteps with distinct params (uniqueParams=2); invocation-record schema PASS.",
    "R-INVOCATION-DISCLOSURE": "command-inventory.v3.json counted 45 commands independently; claimed commandCount=45. Query parityFields match kit: resolved-view, availability, truncated, total-items, termination-class, query-response.",
    "R-DURABLE-RECEIPT-AVAILABILITY": "Receipt+availability records joined to frozen syntax-code run3:f2542b3a…; syntheticHostObservation=true. close_run of that Run is not claimed.",
    "R-CONFIG-SYNTHESIZED": "TypeScriptConfigGraphV1 entryConfigPath=null nodes=[]; independently reminted graphDigestSha256 via raw SHA-256 of C(graph) matches vector.",
    "R-CONFIG-CUSTOM-MULTI-BASE": "extendsResolved sequence [base, strict, base] retained; later-wins; entry kind=other; nodes unique-by-path ascending; graphDigestSha256 independently reminted e434c76f… matches. Prior selfaudit withdrawal of this ID is itself withdrawn.",
    "R-CONFIG-JS-SHARED-BASE": "jsconfig entry extending shared base; entry kind=jsconfig; digest independently reminted b4249ca9… matches.",
    "R-MUTATION-REPLAY-SCOPE": "MutationReplayScopeV1 operation=purge; repair-apply excluded (MUTATION_SCOPE_REPAIR_APPLY). Intent key independently H(workflow.mutation-intent, scope)=6a2921ca….",
    "R-REPAIR-DESCRIPTOR": "repairplan2 identity independently reminted H(workflow.repair-plan, descriptor)=repairplan2:d1c17ff9… matches vector.",
    "R-REPAIR-APPLY-KEY": "Independently SHA-256(C({operation,projectId,repairPlanId,baseSnapshotId}))=206733ee… matches. Unequal to mutationIntentKey.",
    "R-REPAIR-AUTHORITY-PER-TARGET": "Executed repair_target_join unmatched fingerprint → REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE.",
    "R-MIN-RESOLUTION-THREE-LEVELS": "Independently executed eval_atom at syntactic/resolved/type × qualifying/insufficient. Values true/indeterminate, true/false, true/false. Facts/Coverage present. fact2 IDs are placeholder aaaa/bbbb/cccc (not H-derived); owning law is the three-valued predicates, which held.",
    "R-MIN-RESOLUTION-REPAIR-EVIDENCE": "Repair-evidence requirements tied to the min-resolution cases retained.",
    "R-RUN-UNSUPPORTED-GRAMMAR": "Independently executed admit_syntax_suffix('hello.rs')=rust-syntax; notes.unknownlang first-refusal unsupported-file. Did not assume a TypeScript compiler.",
    "R-HIDDEN-MISMATCH-PER-LANGUAGE": "Independently executed admit_config_path missing.tsconfig.json → CONFIG.CUSTODY_REFUSED; admit_edition_map_crate ghost-crate → native.capability-spec-invalid. Positives pass.",
    "R-CLONES-NEGATIVE-VECTORS": "Independently executed first refusals FACT_ANCHOR_CARDINALITY, CLONE_LEVEL_SPEC_MISSING, BODY_LANGUAGE_MISMATCH.",
    "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": "Independently rebuilt FACT-IDENTITY L0 frame from kit recipe (double length-prefix, languageVersion=raw SHA-256(C(BLV)), ownership excluded from BLV). Same edition across two owner sets → sha256:82e8a6b5…; edition 2015 changes identity. Kind is completeRunProperty: this is the standalone identity recipe, not exhibition on a close_run-admitted rust Run.",
    "R-JS-CLONE-BODY-THROUGH-TS": "languageId=javascript ≠ provider typescript. Independent L0 over same bytes differs by languageId. admit_clones_fact javascript-through-ts positive.",
    "R-REPLAY-THREE-VALUED": "Independently eval_atom exists with no facts and no Coverage → indeterminate + missing-relation-coverage. Kind is evaluatorReplay: standalone Kleene vector, not whole-Run replay.",
    "R-CMP-EMPTY-RESULT": "comparison2 identity independently reminted comparison2:c7ee4632… matches.",
    "R-CMP-MISSING": "comparison2:ef8b548a… independently reminted; comparisonPerformed=false; wholeIndeterminateReason required-evidence-unavailable.",
    "R-CMP-EVIDENCE-CHANGED": "comparison2:c7d81009… independently reminted.",
    "R-SCOPE-POLICY-ONLY-COMPARISON": "comparison2:dd74ca1f… independently reminted. contextDelta.scopeChanged=true and all other delta flags false.",
    "R-PIVOT-ONLY-FINGERPRINTS": "comparison2:f454b4fd… independently reminted. Presence B=false, E0=true, E4=false; classify_presence → CODE-NET-NEW.",
    "R-E0-VS-E1-E3": "Vector distinguishes E0 prior detector execution from E1–E3 re-evaluation of current retained evidence.",
    "R-BASELINE-AUDIT": "baseline2 identity independently reminted baseline2:cf4a3a8f… matches.",
    "R-TEST-PREP-REPAIR-AUTH": "Three authorization-failure envelopes (test/preparation/repair) each CommandEnvelope schema-valid; not host execution.",
    "R-MULTI-UNIT-MISSING-CAPS": "Zero-config multi-unit cells with missing advertised capabilities retained.",
    "R-CANDIDATE-ONLY-CLONES": "cells[].selectedCompleteClones=false for clones-near and clones-cross-tsjs; notSelectedCompleteClones=true.",
    "R-HOST-CAPTURED-VS-CANDIDATE": "hostCaptured stage-return vs selectedRefs vs candidateResultRefs distinct; syntheticHostObservation=true.",
    "R-CHAIN-ZERO-CONFIG-TO-RECEIPT": "INCOMPLETE. Arrows map config/envelopes/traces/receipts to frozen Run store hashes, but closeRun=pending on frozen syntax-code/ts/rust stores. Charter requires the chain exhibited by executed traces, envelopes, and complete Runs together. close_run of retained Run bytes is not executed in this snapshot.",
    "R-SUBSYSTEM-OWNERS": "Owner map cites kit documents per envelope/comparison/config/query/repair class.",
    "R-PROMISE-VS-AVAILABILITY": "Four-way distinction productPromise / installedAvailability / explicitOverrides / semanticPrerequisites retained with kit selectors.",
    "R-SEMANTIC-VS-OPERATIONAL-AUTHORITY": "Semantic C/H identities ≠ operational host receipts/grants; selector identity-and-evidence §3.",
    "R-MUTATION-VS-ANALYSIS-STEPS": "analysisSealsRun3=true; mutation/repair-apply do not seal; verify-after-apply seals a new Run.",
    "R-DETECTOR-COMPAT-FILE": "Listing file .opensip/detector-compatibility.json distinguished from component-manifest body; kit owner workflows-and-surfaces §2.",
    "R-EMPTY-PARTIAL-UNAVAILABLE-MISSING": "Four distinct records: complete-empty inventory (state=complete, rows=[]), partial (state=partial, rows nonempty), unavailable (state=unavailable), missing committed bytes EXECUTION_INPUTS_REF_LOST_BYTES with blobPresent=false. Three inventories stock-valid against subject-inventory.schema.v1.json. Not a single narrative label.",
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": "INCOMPLETE pending admitted-Run close_run. Algorithmic adapter independently exercised against reviewer-chosen endpoints Entry.main/Lib.helper/Lib.leaf (not author mod.a fixtures). See queryLawCoverage. Public wrapper is not reported completed.",
}

EXPECTED_DERIVATION = {
    "R-CONFIG-CUSTOM-MULTI-BASE": "native-evidence.schemas.v2 TypeScriptConfigGraphV1: extendsResolved is sequence, later entry wins, repeated edges retained; tsconfigGraphHash = raw SHA-256 of C({schemaVersion,entryConfigPath,nodes}).",
    "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": "identity-and-evidence.md clones body recipe + identity-schemas.v3 languageVersionBindingLaw: frame u8len‖opensip.fact-identity.v1 ‖ u8len‖L0-verbatim ‖ u8len‖SHA-256(level-spec) ‖ u8len‖rust ‖ u8len‖SHA-256(C(BLV)) ‖ u32be payload_len ‖ (u32be raw_len ‖ span). dialect.edition closed integer. Ownership never enters BLV.",
    "R-MIN-RESOLUTION-THREE-LEVELS": "atom-evaluation-contract.v1.md + composition-contract.v3 §3: exists with known match=true; missing Coverage and no match=indeterminate; complete Coverage and no match=false. Rung comparison uses relation ladders.",
    "R-REPAIR-APPLY-KEY": "raw SHA-256 of C({operation:repair-apply, projectId, repairPlanId, baseSnapshotId}); mutation-intent is H(workflow.mutation-intent, scope).",
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": "query-projection-contract.v3.md §§1–8 + graph-query.schema.json major3 + workflows-and-surfaces §8 six-field parity and QueryResult compact summary. Charter required query paragraph: reconstruction over already admitted retained Run(s).",
    "R-CHAIN-ZERO-CONFIG-TO-RECEIPT": "Original standing: exhibited by executed traces, envelopes, and complete Runs together.",
}

OWNER = {
    "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR": [
        "docs/coop/design-corrections/workflows/query-projection-contract.v3.md §§1–8",
        "docs/coop/design-corrections/workflows/schemas/evaluator3/graph-query.schema.json schemaMajor 3",
        "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8",
        "original-consumer-charter.txt Required query reconstruction paragraph",
    ],
    "R-CONFIG-CUSTOM-MULTI-BASE": ["native-evidence.schemas.v2.json TypeScriptConfigGraphV1.nodes[].extendsResolved x-opensip-order sequence"],
    "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE": ["identity-and-evidence.md clones body recipe", "identity-schemas.v3.json languageVersionBindingLaw"],
    "R-MIN-RESOLUTION-THREE-LEVELS": ["atom-evaluation-contract.v1.md", "evaluator-composition-contract.v3.md §3"],
    "R-EMPTY-PARTIAL-UNAVAILABLE-MISSING": ["subject-inventory.schema.v1.json", "execution-inputs-contract.v1.md §2"],
    "R-CHAIN-ZERO-CONFIG-TO-RECEIPT": ["original requirements R-CHAIN-ZERO-CONFIG-TO-RECEIPT observable: reconstruction section mapping each arrow to executed artifacts"],
}

QUERY_LAWS = [
    {"owner": "contract §1", "law": "projectId equals admitted Run; view {runId}|{snapshotId}|{latest:true}; resolvedView {runId} only; latest from host.latestRunId never static bytes; snapshot uniqueness via host.runsForSnapshot; factViewDigests admitted or QUERY.FACT_VIEW_UNAVAILABLE", "status": "algorithmic-measured", "note": "synthetic close_run; admitted-Run pending"},
    {"owner": "contract §2", "law": "vertex domain = inventory ∪ projected endpoints; malformed→PARAMS_MALFORMED; package without PMP or >1 match→ENDPOINT_AMBIGUOUS; zero match→ENDPOINT_UNKNOWN", "status": "reconstruction-gap", "note": "package without packageManifestPath was admitted (success) instead of QUERY.ENDPOINT_AMBIGUOUS. Endpoint unknown/malformed measured PASS."},
    {"owner": "contract §3", "law": "graph-projectable table; file@enumerated QUERY.RELATION_UNSUPPORTED; imports without TargetAttributionV1 omitted; UTF-8 tuple order", "status": "algorithmic-measured", "note": "reviewer facts Entry.main→Lib.helper/Lib.leaf; weaker rung request refused"},
    {"owner": "contract §4", "law": "closed params; neighbors/path/reach units; BFS fact2 order; includeStart default false; shortest hop-count path", "status": "algorithmic-measured"},
    {"owner": "contract §5", "law": "page fullness truncated-page truncated=false; operation bound truncated-bound truncated=true; continuation view.runId; cache ignored; cursor q3.runHex.sel.pos; completeness=required → QUERY.COMPLETENESS_UNMET", "status": "algorithmic-measured"},
    {"owner": "contract §6", "law": "totalItems qualified by countBasis; GraphEvidenceDisclosure; native-evidence-unavailable only when no selected view matches relation@rung; advisory const false", "status": "reconstruction-gap", "note": "empty neighbors with selected matching view2 still emitted native-evidence-unavailable (over-disclosure vs §6). No-selected-view case correctly discloses."},
    {"owner": "contract §7", "law": "failure kind=failure nonempty errors no run field; host.requestId req1_+32hex precondition; schemaMajor≠3 SCHEMA_MAJOR_UNSUPPORTED; availability purged/expired/unavailable/corrupt refuse HOST.IO_FAILURE", "status": "algorithmic-measured"},
    {"owner": "contract §8", "law": "execute_graph_query(request, run, objects, blobs, host) requires close_run then projects from admitted views/payloads; traverse_projected_graph algorithmic only", "status": "remaining-binding", "note": "close_run required PASS (without it QUERY.VIEW_UNKNOWN). Wrapper still takes caller projected_edges and does not project from objects/blobs. Public wrapper not completed."},
    {"owner": "workflows-and-surfaces §8", "law": "six parity fields resolved-view/availability/truncated/total-items/termination-class/query-response; query-response is complete GraphQueryResponseV1; compact QueryResult items=page count, truncated=context flag, completenessMet iff countBasis=exact, nextCursor iff context token", "status": "reconstruction-gap", "note": "six-field exact projections PASS on human/json/agent. Helper does not emit CommandEnvelope.query QueryResult / completenessMet. Independently derived QueryResult from context is well-formed; consumer does not produce it."},
    {"owner": "charter query paragraph", "law": "three operations over already admitted retained Run(s); retain executable vectors; pagination after newer latest or cache loss; evidence limitations ≠ stored-edge completion; operation bounds vs page; malformed/mismatched + lawful failure envelopes with synthetic host.requestId; complete parity with compact summary joins", "status": "INCOMPLETE", "note": "algorithmic cases exist; admitted-Run measured results do not. Frozen stores: no calls@resolved-callee; TS imports@resolved-target without TargetAttributionV1. Record executed only when retained vectors AND measured results exist over admitted Runs."},
    {"owner": "graph-query.schema.json major3", "law": "GraphQueryRequestV1 / GraphQueryResponseV1 / CommandEnvelope failure inhabitance", "status": "algorithmic-measured", "note": "independently produced request/response/failure stock-valid"},
]

REMAINING = [
    {
        "id": "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
        "acceptedFlag": False,
        "firstRemaining": "close_run of retained complete Run object-table + blob/frame bytes, then execute_graph_query over admitted views/facts/Coverage/TargetAttributionV1. Frozen stores currently lack calls@resolved-callee. Without close_run the public wrapper returns QUERY.VIEW_UNKNOWN.",
        "additionalAdapterGapsNotCompletedPublicWrapper": [
            "execute_graph_query accepts caller projected_edges instead of projecting from objects/blobs (contract §8 step 4)",
            "CommandEnvelope.query QueryResult compact summary (completenessMet, items=page count, nextCursor join) is not implemented in helper/query_projection.py or helper/workflow_laws.py",
            "native-evidence-unavailable emitted for empty neighbors even when a selected view matches relation@rung (contract §6)",
            "package endpoint without packageManifestPath admitted rather than QUERY.ENDPOINT_AMBIGUOUS (contract §2)",
        ],
        "doNotTreatStaleHashAsAccepted": "Successor corrected Run may supersede frozen hashes in frozen-run-hashes.json. Current syntax-code.store.json 2e74a6b2… is unlabeled unverified for close_run.",
    },
    {
        "id": "R-CHAIN-ZERO-CONFIG-TO-RECEIPT",
        "acceptedFlag": False,
        "firstRemaining": "close_run of retained complete Run bytes joined to executed traces/envelopes. Vector arrows currently mark closeRun=pending on frozen syntax-code/ts/rust stores.",
        "doNotTreatStaleHashAsAccepted": "Successor store may supersede syntax-code.store.json 2e74a6b2…",
    },
]

WITHDRAWALS = [
    {"prior": "kit-workflow-selfaudit.v4 withdrawal of R-CONFIG-CUSTOM-MULTI-BASE (no repeated later-wins)", "now": "WITHDRAW that refusal. Independently reminted repeated-base sequence and digest.", "id": "R-CONFIG-CUSTOM-MULTI-BASE"},
    {"prior": "kit-workflow-selfaudit.v4 withdrawal of R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE (identity not remintable)", "now": "WITHDRAW that refusal for the standalone identity recipe. Independently reminted L0 from retained span/BLV/frame. Whole-Run exhibition on frozen rust store remains out of this workflow scope.", "id": "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE"},
    {"prior": "kit-workflow-selfaudit.v4 withdrawal of R-MIN-RESOLUTION-THREE-LEVELS (no facts/Coverage)", "now": "WITHDRAW that refusal. Independently executed eval_atom over retained facts/Coverage at three levels.", "id": "R-MIN-RESOLUTION-THREE-LEVELS"},
    {"prior": "kit-workflow-selfaudit.v4 withdrawal of R-EMPTY-PARTIAL-UNAVAILABLE-MISSING (narrative strings)", "now": "WITHDRAW that refusal. Four distinct schema-valid / lost-bytes records.", "id": "R-EMPTY-PARTIAL-UNAVAILABLE-MISSING"},
    {"prior": "prior workflow PASS of R-GRAPH-QUERY", "now": "DO NOT restore executed. Charter requires admitted retained Run(s). Author marks INCOMPLETE; independent measurement agrees. Algorithmic cases are not Run admission.", "id": "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR"},
    {"prior": "R-CHAIN-ZERO-CONFIG-TO-RECEIPT INCOMPLETE", "now": "MAINTAIN INCOMPLETE. close_run still pending.", "id": "R-CHAIN-ZERO-CONFIG-TO-RECEIPT"},
]

def scope_for(i):
    iid = i["id"]
    kind = i["kind"]
    if iid in EST48:
        if iid in INCOMPLETE:
            return "in-scope-INCOMPLETE"
        return "in-scope-executed"
    if iid in FUTURE:
        return "futureQualification"
    if iid in FROZEN_RUN:
        return "out-of-scope-frozen-run"
    if iid in FROZEN_REPLAY:
        return "out-of-scope-frozen-run-replay"
    if iid in STANDING_CONTINUATION:
        return "standing-of-consumer-continuation-not-re-executed-here"
    if iid == "R-IMPORTED-OBSERVATION-BOUNDARY":
        return "measured-standalone-outside-established-48"
    return "notReached-historical-vector"

mapping = []
for i in all_ids:
    sc = scope_for(i)
    row = {
        "id": i["id"],
        "kind": i["kind"],
        "phase": i.get("phase"),
        "acceptBlocking": i.get("acceptBlocking"),
        "reviewedScope": sc,
        "established48": i["id"] in EST48,
    }
    if i["id"] in EST48:
        row["disposition"] = "INCOMPLETE" if i["id"] in INCOMPLETE else "executed"
        row["artifact"] = ART.get(i["id"])
        row["measurement"] = MEASURE.get(i["id"])
        row["expectedDerivation"] = EXPECTED_DERIVATION.get(i["id"])
        row["ownerSelectors"] = OWNER.get(i["id"])
    elif i["id"] == "R-IMPORTED-OBSERVATION-BOUNDARY":
        row["disposition"] = "executed-as-standalone-citation"
        row["artifact"] = "vectors/imported-observation-boundary.json"
        row["measurement"] = "Not in the established 48. Snapshot artifact present. mayProve runtime hit/miss/test/history; mayNotProve static Coverage completeness / native resolution completeness / universal non-use. Selector native-evidence §7; atom-evaluation-contract §6."
        row["note"] = "Included in 134 as measured-outside-established-48 so notReached is not used after this review actually read the vector."
    mapping.append(row)

from collections import Counter
counts = Counter(m["reviewedScope"] for m in mapping)
assert sum(counts.values()) == 134, counts

disp48 = []
for iid in EST48:
    rec = by_id[iid]
    disp48.append({
        "id": iid,
        "kind": rec["kind"],
        "phase": rec.get("phase"),
        "acceptBlocking": rec.get("acceptBlocking"),
        "disposition": "INCOMPLETE" if iid in INCOMPLETE else "executed",
        "artifact": ART[iid],
        "measurement": MEASURE[iid],
        "expectedDerivation": EXPECTED_DERIVATION.get(iid),
        "ownerSelectors": OWNER.get(iid),
        "wholeRunVsStandalone": (
            "completeRunProperty exhibited as standalone identity recipe; frozen rust Run close_run unverified"
            if iid == "R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE"
            else "evaluatorReplay exhibited as standalone Kleene vector; whole-Run replay out of scope"
            if iid == "R-REPLAY-THREE-VALUED"
            else "standalone/config/envelope/standing as original kind"
            if rec["kind"] not in ("completeRunProperty", "evaluatorReplay")
            else rec["kind"]
        ),
    })

review = {
    "role": "REVIEWER",
    "sessionStanding": "Same fresh-origin S kit-only team session. Reviewer of another actor's V-origin workflow snapshot. Not independent acceptance of this reviewer's prior pilot-corrections.v3. No prior positive/negative grade is authority.",
    "verdict": "WORKFLOW_SCOPE_INCOMPLETE",
    "verdictScope": "Original 48 workflow/config/standalone/envelope/standing IDs against full original charter kinds/quantifiers. 46 executed. 2 INCOMPLETE (R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR, R-CHAIN-ZERO-CONFIG-TO-RECEIPT). Frozen Run close_run unlabeled unverified. Not whole-consumer ACCEPT. Not ROOT-ADMISSION.",
    "wholeConsumerAcceptance": False,
    "rootAdmission": False,
    "newMustIssues": [
        {
            "id": "R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR",
            "severity": "remaining-binding",
            "selector": "original-consumer-charter.txt Required query reconstruction; query-projection-contract.v3.md §8",
            "text": "Public graph query is not executed over already admitted retained Run(s). execute_graph_query without close_run returns QUERY.VIEW_UNKNOWN. Frozen stores lack calls@resolved-callee.",
        }
    ],
    "newShouldIssues": [
        {
            "id": "query-adapter-QueryResult",
            "selector": "workflows-and-surfaces.md §8 QueryResult compact summary",
            "text": "Helper does not emit completenessMet / CommandEnvelope.query QueryResult. Independently derived from context; not produced.",
        },
        {
            "id": "query-adapter-native-evidence-overdisclosure",
            "selector": "query-projection-contract.v3.md §6",
            "text": "Empty neighbors with a selected matching view still emit native-evidence-unavailable.",
        },
        {
            "id": "query-adapter-package-PMP",
            "selector": "query-projection-contract.v3.md §2",
            "text": "Package identity without packageManifestPath was admitted instead of QUERY.ENDPOINT_AMBIGUOUS.",
        },
    ],
    "absentOrContradictoryLaws": [],
    "existingLawReconstructionGaps": [
        "Query adapter: compact QueryResult not implemented (existing workflows §8 law).",
        "Query adapter: native-evidence-unavailable over-disclosure when selected view matches (existing contract §6).",
        "Query adapter: package without PMP not AMBIGUOUS (existing contract §2).",
        "Query adapter: projection injected via projected_edges rather than objects/blobs (existing contract §8). Remaining final binding, not a completed wrapper.",
    ],
    "newMustIssuesEmptyJustification": "Not empty: remaining close_run binding is an existing-law reconstruction dependency, not a missing recipe. No extra per-language Run demand was invented. Query charter paragraph now supplied; conclusions reassessed.",
    "inputHashes": {
        "snapshotManifestSha256": "93926c8f2dbf1b45ab06e3479ad4e06ebf40405de0eef4a6a5ef6a040d773999",
        "snapshotFiles": "PASS 285/285",
        "originalCharterSha256": "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec",
        "consumerInputManifestSha256": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
        "requirementsJsonSha256": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
        "sourceProvenanceOnly": "consumer-b.v12-team-workflow-corrections.v3/output (not read)",
    },
    "frozenRunStores": {
        "verifiedByteIdenticalWithSnapshot": True,
        "closeRun": "unverified-out-of-scope",
        "runs": author["frozenRunStores"]["runs"],
        "graphProjectableProbe": {
            "callsResolvedCalleePresent": False,
            "tsImportsResolvedTargetWithoutTargetAttributionV1": True,
            "execute_graph_query_without_close_run": "QUERY.VIEW_UNKNOWN on all five stores",
        },
    },
    "execution": {
        "python": "/tmp/opensip-architecture-review-env/bin/python -I -B",
        "isolatedCopy": "output/isolated-work (ROOT/output/subject layout; hardcoded author paths redirected before execution)",
        "pathCorrection": "output/path-correction-record.json",
        "pathOnlyDiff": True,
        "originalSnapshotUntouched": True,
        "independentProbe": "output/probes/independent_measure.py",
        "independentResults": "output/probes/independent-measure.results.json",
        "authorTestsNotOracle": {
            "scripts/workflow_correct_test.py": {"exitCode": 0, "standing": "helper self-consistency, not expected-value authority"},
            "scripts/query_charter_test.py": {"exitCode": 0, "standing": "helper self-consistency, not expected-value authority"},
        },
        "discriminatingQueryInputs": {
            "universe": "sha256(opensip.reviewer.discriminating-universe.query-v4)",
            "endpoints": ["Entry.main", "Lib.helper", "Lib.leaf"],
            "notAuthorFixtures": True,
        },
    },
    "all48Disposition": disp48,
    "nExecutedComplete": 46,
    "nIncomplete": 2,
    "incompleteIds": sorted(INCOMPLETE),
    "remainingDependencies": REMAINING,
    "queryLawCoverage": QUERY_LAWS,
    "withdrawals": WITHDRAWALS,
    "reviewedScopeCounts": dict(counts),
    "originalRequirementIds": mapping,
    "unexecutedLimits": [
        "Frozen Run close_run / identity-and-evidence §3 closure admission / semantic proof replay are out of this workflow-scope review.",
        "Algorithmic query cases used labeled synthetic close_run and independently chosen projected edges. That is not retained Run admission.",
        "Real OS/compiler/product/cryptographic qualification remains futureQualification. Synthetic host.requestId / availability / latestRunId / runsForSnapshot / testBounds observations are explicit.",
        "R-OBJECT-TABLE-FRAMES and R-FROM-SCRATCH-COMMAND for complete Runs are notReached in this workflow-scope review.",
        "Min-resolution fact2/coverage2 IDs are placeholder hex, not H-derived. Atom evaluation over those local ids still held.",
        "Public wrapper is not completed except remaining final binding work listed under remainingDependencies.",
        "No whole-consumer ACCEPT. No root admission.",
    ],
    "kindsQuantifiersApplied": REQ["kinds"],
    "classificationRule": REQ["classificationRule"],
}

(OUT / "workflow-review.json").write_text(json.dumps(review, indent=2) + "\n")
print("json 48", len(disp48), "134", len(mapping), "counts", dict(counts))
print("verdict", review["verdict"])

# markdown
lines = []
A = lines.append
A("# Workflow-scope independent review")
A("")
A("**Verdict: `WORKFLOW_SCOPE_INCOMPLETE`**")
A("")
A("Same fresh-origin kit-only team session, **REVIEWER** of another actor's V-origin workflow snapshot. This session authored the syntax-code **pilot** examples, not this snapshot. This is not independent acceptance of that pilot, and no prior positive or negative grade is authority.")
A("")
A("Not whole-consumer ACCEPT. Not ROOT-ADMISSION. Frozen Run `close_run` remains unlabeled unverified.")
A("")
A("## Custody")
A("")
A("| Object | SHA-256 / result |")
A("|---|---|")
A("| snapshot-manifest.json | `93926c8f2dbf1b45ab06e3479ad4e06ebf40405de0eef4a6a5ef6a040d773999` MATCH 285/285 |")
A("| original-consumer-charter.txt | `57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec` |")
A("| kit consumer-input-manifest.json | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` |")
A("| original requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` |")
A("| source path (provenance only, not read) | `consumer-b.v12-team-workflow-corrections.v3/output` |")
A("")
A("Isolated execution copy: `output/isolated-work` with hardcoded author ROOT/OUT/KIT/requirements redirected **before** any consumer-code run. Path-only diff of 21 `.py` files: `output/path-correction-record.json` (`allPathOnly=true`). Original snapshot and five frozen Run stores were not rewritten.")
A("")
A("Independent probe: `output/probes/independent_measure.py` using `/tmp/opensip-architecture-review-env/bin/python -I -B`. Expected values derived from kit recipes and reviewer-chosen inputs (`Entry.main` / `Lib.helper` / `Lib.leaf`), not from consumer fixtures or key-presence assertions. Author `workflow_correct_test.py` / `query_charter_test.py` both exited 0 as helper self-consistency only, not expected-value authority.")
A("")
A("## Verdict")
A("")
A("46 of the established 48 workflow-scope IDs are **executed** under their original kinds. Two remain **INCOMPLETE**:")
A("")
A("1. `R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR` — charter requires reconstruction over **already admitted retained Run(s)**. The author marks this incomplete pending `close_run`. Independent measurement agrees. Algorithmic adapter coverage is not Run admission and is not reported as a completed public wrapper.")
A("2. `R-CHAIN-ZERO-CONFIG-TO-RECEIPT` — arrows join config/envelopes/traces to frozen store hashes with `closeRun=pending`. The standing requirement is exhibited by executed traces, envelopes, **and complete Runs** together.")
A("")
A("Missing/contradictory normative law: **none**. Adapter gaps below are **existing-law reconstruction** misses on the query helper, recorded as remaining binding under the already-incomplete query ID.")
A("")
A("## Query law coverage (full charter paragraph now supplied)")
A("")
A("The full original query paragraph (charter lines 209–212) was omitted from an earlier condensed handoff and is now actually supplied. Conclusions are reassessed without changing source semantics or inventing extra per-language Run demands.")
A("")
A("| Owner | Law | Independent status |")
A("|---|---|---|")
for q in QUERY_LAWS:
    note = q.get("note", "")
    A(f"| {q['owner']} | {q['law']} | **{q['status']}**{'; ' + note if note else ''} |")
A("")
A("Independent query first measurements (reviewer inputs, synthetic `close_run` labeled): three operations PASS; canonical UTF-8 order PASS; `file@enumerated` → `QUERY.RELATION_UNSUPPORTED` PASS; page fullness `truncated-page`/`truncated=false` PASS; operation bound `truncated-bound`/`truncated=true` PASS; `completeness=required` → `QUERY.COMPLETENESS_UNMET` PASS; historical pagination after newer `host.latestRunId` PASS; `{latest:true}` mismatch → `QUERY.VIEW_UNKNOWN` PASS; continuation requires `view.runId` PASS; `host.cache` ignored PASS; six-field human/json/agent exact projections PASS; wrapper without `close_run` → `QUERY.VIEW_UNKNOWN` PASS; `traverse_projected_graph` labeled `algorithmic` PASS; query does not seal a Run PASS.")
A("")
A("Remaining adapter work (not a completed public wrapper):")
A("")
A("- `execute_graph_query` still takes caller `projected_edges` instead of projecting from retained `objects`/`blobs` (contract §8).")
A("- Compact `QueryResult` (`completenessMet`, page `items`, `nextCursor` join) is not implemented in the helper. Independently derived from response context; consumer does not emit it.")
A("- Empty neighbors with a **selected** matching view still emit `native-evidence-unavailable` (contract §6 over-disclosure).")
A("- Package endpoint without `packageManifestPath` was admitted (contract §2 requires `QUERY.ENDPOINT_AMBIGUOUS`).")
A("")
A("Frozen-store probe (no fabricated edges): none of the five stores contain `calls@resolved-callee`. TS has `imports@resolved-target` without observed `TargetAttributionV1`. Do not treat a stale frozen hash as an accepted flag; a later corrected Run may supersede `2e74a6b2…`.")
A("")
A("## Previously withdrawn grades, reassessed")
A("")
A("| ID | Prior selfaudit | This review |")
A("|---|---|---|")
A("| R-CONFIG-CUSTOM-MULTI-BASE | refused (no repeated later-wins) | **executed** — sequence `[base, strict, base]`; digest `e434c76f…` independently reminted |")
A("| R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE | refused (identity not remintable) | **executed as standalone identity recipe** — independent FACT-IDENTITY L0 `sha256:82e8a6b5…`; ownership excluded from BLV; edition change changes identity. Not a close_run-admitted rust Run property |")
A("| R-MIN-RESOLUTION-THREE-LEVELS | refused (no facts/Coverage) | **executed** — `eval_atom` true/indeterminate, true/false, true/false at syntactic/resolved/type. Placeholder fact2 ids noted, not used as a refusal of the predicates |")
A("| R-EMPTY-PARTIAL-UNAVAILABLE-MISSING | refused (narrative strings) | **executed** — four distinct records; inventories schema-valid |")
A("| R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR | incomplete / refused parity | **INCOMPLETE** — do not restore executed |")
A("| R-CHAIN-ZERO-CONFIG-TO-RECEIPT | incomplete | **INCOMPLETE** |")
A("")
A("## All 48 dispositions")
A("")
A("| ID | Kind | Disposition | Artifact |")
A("|---|---|---|---|")
for d in disp48:
    A(f"| `{d['id']}` | {d['kind']} | **{d['disposition']}** | `{d['artifact']}` |")
A("")
A("Measurement, expected derivation, and owner selectors for every ID are in `workflow-review.json#/all48Disposition`.")
A("")
A("Standalone vs whole-Run: `R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE` is original kind `completeRunProperty` exhibited here as a reminted identity pair, not as a property of a `close_run`-admitted rust graph. `R-REPLAY-THREE-VALUED` is original kind `evaluatorReplay` exhibited as a standalone Kleene vector, not whole-Run semantic replay. Frozen completeRun / evaluatorReplay IDs remain out of this workflow scope.")
A("")
A("## 134 original ID mapping")
A("")
A("| reviewedScope | Count |")
A("|---|---:|")
for k, v in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
    A(f"| {k} | {v} |")
A(f"| **total** | **{sum(counts.values())}** |")
A("")
A("`R-IMPORTED-OBSERVATION-BOUNDARY` is a phase-6 standalone vector present in the snapshot and measured here, but it is not a member of the established 48. It is mapped `measured-standalone-outside-established-48` so this review does not call it `notReached` after reading it.")
A("")
A("## Remaining final binding")
A("")
A("See `remainingDependencies` in the JSON. Precise remaining work from actual code and existing laws:")
A("")
A("1. Implement/retain `close_run` over exported object table + all blob/frame bytes of a complete positive (identity-and-evidence §3). This is frozen-Run work, not invented query law.")
A("2. Bind `execute_graph_query(request, run, objects, blobs, host)` so step 4 projects from admitted views, retained TargetAttributionV1, and retained payloads — not caller-authored edges.")
A("3. If the admitted graph still lacks a projectable binary rung, refuse `QUERY.RELATION_UNSUPPORTED` / disclose `native-evidence-unavailable` rather than fabricating `calls` facts.")
A("4. Emit compact `QueryResult` summary joins and keep six-field parity.")
A("5. Join executed traces/envelopes to that admitted Run for `R-CHAIN-ZERO-CONFIG-TO-RECEIPT`.")
A("")
A("A successor corrected Run may supersede current frozen hashes. Do not keep a stale hash as an accepted flag.")
A("")
A("## Unexecuted limits")
A("")
for u in review["unexecutedLimits"]:
    A(f"- {u}")
A("")
A("## Author claims")
A("")
A("The author self-verdict is `WORKFLOWS_INCOMPLETE` with the same two incomplete IDs. This review independently remeasured rather than adopting that grade. Agreement on INCOMPLETE for those two IDs is a measurement result, not a waiver.")
A("")

(OUT / "workflow-review.md").write_text("\n".join(lines) + "\n")
print("wrote md", OUT/"workflow-review.md")
print("wrote json", OUT/"workflow-review.json")
