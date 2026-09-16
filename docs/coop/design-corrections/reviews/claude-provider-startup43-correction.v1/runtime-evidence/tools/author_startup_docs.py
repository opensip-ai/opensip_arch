"""Author native/provider-startup.schemas.v1.json and native/typescript-protocol2-order.v1.json in the work copy.

usage: author_startup_docs.py <work-candidate-root>

Member lists of the universe envelopes, inherited OpenUniverse/UniverseAccepted/Coverage/Unavailable/
BudgetExhausted wrappers and inherited Unavailable reasons are READ from the pinned inherited artifacts
(delivery.v2, rust-provider-protocol.v2, resolved-inputs.v2) and from the registered native bundle, so the
successor records cannot silently drop an inherited member. The native checker re-derives them.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
ART = ROOT / "docs" / "coop" / "artifacts"
NATIVE = ROOT / "docs" / "coop" / "design-corrections" / "native"
OUT_SCHEMA = NATIVE / "provider-startup.schemas.v1.json"
OUT_ORDER = NATIVE / "typescript-protocol2-order.v1.json"

delivery = json.loads((ART / "delivery.v2.json").read_text(encoding="utf-8"))
rust = json.loads((ART / "rust-provider-protocol.v2.json").read_text(encoding="utf-8"))
ri = json.loads((ART / "resolved-inputs.v2.json").read_text(encoding="utf-8"))
bundle = json.loads((NATIVE / "native-evidence.schemas.v2.json").read_text(encoding="utf-8"))
BUNDLE_ID = bundle["$id"]

ts_ps = delivery["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]["payloadSchemas"]
ts_limits = delivery["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]["limits"]
rs_ps = rust["wireSchema"]["payloadSchemas"]
su = ri["planIdContract"]["semanticUniverseSchemas"]

TS_INHERITED_REASONS = ts_ps["UnavailableV1"]["fields"]["reason"].removeprefix("enum ").split("|")
RS_INHERITED_REASONS = rs_ps["UnavailableV2"]["fields"]["reason"].split("|")
REASONS_V3 = bundle["$defs"]["UnavailableReasonV3"]["enum"]
TS_ADDED_REASONS = ["capability-missing", "identity-version-mismatch", "node-modules-outside-read-set"]  # native-evidence 9.4
assert set(TS_ADDED_REASONS) <= set(REASONS_V3)
TS_POST_REASONS = sorted(set(TS_INHERITED_REASONS) | set(TS_ADDED_REASONS))
RS_POST_REASONS = sorted((set(RS_INHERITED_REASONS) | set(REASONS_V3)) - {"native-context-mismatch"})
assert "native-context-mismatch" not in TS_POST_REASONS
BUDGET_DIMENSIONS = ts_ps["BudgetExhaustedV1"]["fields"]["dimension"].removeprefix("enum ").split("|")
RS_BUDGET_UNITS = ["work-units", "bytes", "items"]  # rust-provider-protocol.v2 BudgetExhaustedV2.fields.unit


def ref(name):
    return {"$ref": "#/$defs/" + name}


def bref(name):
    return {"$ref": BUNDLE_ID + "#/$defs/" + name}


def closed(required, properties, description):
    assert list(required) == list(properties), (required, list(properties))
    return {"type": "object", "additionalProperties": False, "required": list(required),
            "properties": properties, "description": description}


def envelope(row, protocol_major, resolved_def, language_text):
    props = {}
    for member in row["required"]:
        if member in row["constants"]:
            props[member] = {"const": row["constants"][member]}
        elif member == "protocolMajor":
            props[member] = {"const": protocol_major}
        elif member == "resolvedInputs":
            props[member] = bref(resolved_def)
        elif member == "standardLibraryComponentDigests":
            props[member] = {"type": "object", "additionalProperties": ref("DigestHex"), "required": [], "properties": {},
                             "description": "component name -> 64-hex digest (rust-v1 digestRepresentation)"}
        elif member in row["digestFields"]:
            props[member] = ref("DigestHex")
        else:
            props[member] = ref("NfcText")
    return closed(row["required"], props,
                  f"The resolved-inputs.v2 {language_text} map with resolvedInputs replaced by {resolved_def} "
                  f"and protocolMajor {protocol_major}; every other member, constant and digest representation unchanged.")


def wrapper(inherited_required, overrides, description):
    props = {m: overrides[m] for m in inherited_required}
    return closed(inherited_required, props, description)


COVERAGE_ENTRIES = {"type": "array", "minItems": 1, "maxItems": ts_limits["maxCoverageEntriesPerFrame"],
                    "items": bref("CoverageResultV3"), "x-opensip-order": "sequence",
                    "description": "entries[i] answers requestedCoverageDomain.keys[i] of the attributed stage; CoverageResultV3 is the entry type, never the frame."}
TERMINAL_COVERAGE = {"type": "array", "minItems": 0, "items": bref("CoverageResultV3"), "x-opensip-order": "sequence",
                     "description": "CoverageResultV3 in stage-major/key order; entry k belongs to the stage whose cumulative requested-key range contains k."}
STAGE_IDS = {"type": "array", "minItems": 1, "items": ref("StageIdText"), "x-opensip-order": "sequence",
             "description": "all requested stageIds in request order (inherited)"}

law = {
    "standing": "NORMATIVE field-level successor publication for native-evidence section 9.7: typescript-semantic major-2 and rust-semantic major-3 OpenUniverse, UniverseAccepted, NativeContextVerified, pre-Analyze Unavailable, Coverage and terminal coverage payloads. Registered and historical artifacts are unchanged; section 0 names every superseded selector. Cross-record joins a schema cannot express are executed by native/provider_startup_model.v1.py and native_evidence_model.v2.provider_startup_exchange within their stated scope.",
    "identityMembers": "Inherited OpenUniverse member names are unchanged. executionId keeps its owner (host-allocated ExecutionId, exact AttemptRecord value; rust-semantic IdentityText). planIntentCommitment keeps its owner (exact AttemptRecord/ExecutionPlan value). snapshotId carries the foundation snapshot2 identity text of the verified Plan (^snapshot2:[0-9a-f]{64}$), replacing the v1 SnapshotId text; planId carries the verified plan2 identity text (^plan2:[0-9a-f]{64}$), replacing plan1. Every later member whose inherited rule is an exact echo of the OpenUniverse executionId, snapshotId or planId (UniverseAccepted; SnapshotManifest/SnapshotSeal/SnapshotAccepted and SubjectScopeV1 snapshotId; Analyze; PreparedOutputManifest/PreparedOutputAccepted planId; Cancel/Cancelled executionId; PreAnalyzeUnavailableV1) carries the same text.",
    "universeIdentity": "A wire universe coordinate carries the native semantic-universe identity of the selected v2 universe: sha256:hex(H(native.semantic-universe.<language>.v2, universe.resolvedInputs)) under the foundation identity recipe (native-evidence section 11; foundation identity-schemas.v3 native-semantic-universe domain rows). This supersedes delivery.v2 definitions.TypeScriptSemanticUniverseKey (the opensip.typescript-universe.v1 recipe) wherever that type is used - OpenUniverse.universeKey, CoverageKeyV1.sourceUniverseId/targetUniverseId, FactCandidateV1.sourceUniverseId/targetUniverseId - and rust-provider-protocol.v2 planAndDomainProjection.sourceUniverseIdAlgorithm and allSemanticUniverseIdAlgorithm. CoverageKeyV2, subject-scope and fact2 carry its 64-hex suffix; foundation provider_attribution_return_model.v2 _mint_correspondence already joins candidate universe ids to fact2 by that suffix.",
    "typescriptOpenUniverse": {
        "payload": "TypeScriptOpenUniverseV2",
        "universe": "TypeScriptSemanticUniverseV2",
        "nativeContext": "carried inside the universe descriptor as universe.resolvedInputs.nativeContextId (no separate member); its 64-hex suffix is a member of the verified plan.nativeContextDigests",
        "universeKey": "the universe identity of universeIdentity, recomputed by host and worker",
        "handshakeJoin": ["providerBuildId", "providerDescriptorSha256", "runtimeDescriptorSha256", "protocolMajor", "nodeVersion", "v8Version", "modulesAbi", "typescriptVersion", "typescriptCompilerSha256", "typescriptStdlibMerkleRoot", "platformId"],
        "handshakeJoinRule": "each listed universe member equals the same member of the admitted TypeScriptHelloAckV2 (resolved-inputs.v2 typescript-v1 deliveryJoin)",
        "absent": "no repositoryResolution member; no dependency-source or prepared custody frame",
        "accepted": "TypeScriptUniverseAcceptedV2 = {executionId, snapshotId, planId, universeKey}, each equal to OpenUniverse; universeKey is the worker's own recomputation",
    },
    "rustOpenUniverse": {
        "payload": "OpenUniverseV3",
        "universe": "RustSemanticUniverseV2",
        "nativeContext": "carried inside the universe descriptor as universe.resolvedInputs.nativeContextId (no separate member); its 64-hex suffix is a member of the verified plan.nativeContextDigests",
        "handshakeJoin": ["protocolMajor", "providerBuildId", "rustCommitHash", "hostTriple", "targetTriple", "sysrootDigest"],
        "handshakeJoinRule": "each listed universe member equals the same member of the admitted HelloV3.expectedIdentity (resolved-inputs.v2 rust-v1 deliveryJoin; native-evidence 9.1)",
        "repositoryResolution": "RepositoryResolutionV3. dependencySourceSetId and preparedOutputSetId equal universe.resolvedInputs. authorizationId and effects are both null when preparedOutputSetId is null; otherwise authorizationId is the admitted preparation.authorizationId of the selected PreparedOutputSetV3 (null for an imported-descriptor preparation) and effects are the effects of the AuthorizedExecutionV2 it names, null exactly when authorizationId is null.",
        "accepted": "UniverseAcceptedV3 = {executionId, snapshotId, planId, providerId, universe, repositoryResolution}, exact recursive equality with OpenUniverse (UniverseAcceptedV2 rule)",
        "derivedModes": "dependencyMode and preparedMode are HOST-DERIVED OBSERVATIONS of the admitted OpenUniverseV3, never wire members. dependencyMode is true for every admitted OpenUniverseV3: RepositoryResolutionV3.dependencySourceSetId is required and non-null, and an empty DependencySourceSetV1 (packages []) still takes DependencySourceManifest (entries []), DependencySourceSeal (entryCount 0, totalBytes 0, totalChunkCount 0) and DependencySourceAccepted, with no chunk. preparedMode is preparedOutputSetId != null. protocol3-transitions rows P3-09 and P3-10 (dependencyMode false) are therefore unreachable from an admitted major-3 OpenUniverse and remain only as the abstract table's closed guard partition.",
    },
    "nativeContextVerified": "NativeContextVerifiedV1 = {nativeContextId, recomputedNativeContextId, equal: true}; nativeContextId and recomputedNativeContextId both equal OpenUniverse.universe.resolvedInputs.nativeContextId.",
    "preAnalyzeUnavailable": {
        "payload": "PreAnalyzeUnavailableV1",
        "frame": "Unavailable, worker->host, worker terminal (terminalKind unavailable)",
        "phase": "Admissible only while the host waits for NativeContextVerified: typescript-semantic phase WAIT_NATIVE_CONTEXT_VERIFIED of native/typescript-protocol2-order.v1.json (after SnapshotAccepted, before NativeContextVerified and Analyze) and rust-semantic protocol3-transitions row P3-21. Outside that phase this payload is PROVIDER.PROTOCOL_VIOLATION; inside it the post-Analyze payloads TypeScriptUnavailableV2 and UnavailableV3 are PROVIDER.PROTOCOL_VIOLATION.",
        "reason": "exactly native-context-mismatch. No other inherited or UnavailableReasonV3 reason is admitted before Analyze, and native-context-mismatch is not admitted after Analyze.",
        "correlation": "executionId, snapshotId and planId equal the admitted OpenUniverse; nativeContextId equals OpenUniverse.universe.resolvedInputs.nativeContextId; recomputedNativeContextId is the worker's recomputation (native-evidence 9.5) and differs from nativeContextId. No analysisOrdinal, affectedStageIds, coverage or coverageCommitment: the worker has received no Analyze.",
        "afterTerminal": "WAIT_ZERO_EXIT, zero-exit, WAIT_EOF, eof, DONE. Any other frame is a post-terminal FAULT; a nonzero exit, signal death, deadline or stdout byte is FAULT.",
        "fault": "A malformed payload, a failed correlation, recomputedNativeContextId equal to nativeContextId, any other reason, or the payload outside its phase is PROVIDER.PROTOCOL_VIOLATION and FAULT: no facts, no Coverage, no Run (stage_authority fault law). A later post-terminal or process fault also converts the exchange to FAULT.",
        "hostConversion": "Only after DONE is the clean terminal converted: stage_authority('unavailable') (authoritative, indeterminate 3, COVERAGE.PROVIDER_UNAVAILABLE). Affected domains are every stage the host would have placed in this Analyze (typescript-semantic multiStageAnalyze.selection/stageRequestProjection; rust-semantic planAndDomainProjection.selectedStageRule) with the requested coverage domains the host derived before spawn (coverageDomain.authority; StageAnalysisDomainV2). For every requested key the host mints one CoverageResultV3: key = that key's subject-scope coordinates; entry.coverage unknown; examinedUniverse = the host subject-scope commitment and count; resolutionCompleteness = completeness_from_stage(attempted=false, stageTerminal=unavailable, examinedExhaustive=false), i.e. not-attempted on a resolved rung and not-applicable otherwise; closedWorld = closed_world_v2(no manifest, entry points none, no edges, externalConsumers unknown); derivationKinds []; confidenceMillionths 0; deficiency provider-unavailable; nativeCause null. It admits each through admit_coverage_result_v3 and then applies run_termination. No stage id or coverage is taken from the worker.",
    },
    "coverageFrames": {
        "typescript-semantic": "Frame name Coverage is unchanged. Its payload is TypeScriptCoverageV2 = the CoverageV1 wrapper {analysisOrdinal (exactly 0), stageId, entries, coverageCommitment} with entries a non-empty array of CoverageResultV3, length <= maxCoverageEntriesPerFrame.",
        "rust-semantic": "Frame name is CoverageV3 (native-evidence 9.2 frame table; protocol3-transitions P3-24), superseding rust-provider-protocol.v2 frameSchemas.Coverage. Its payload is CoverageV3 = the CoverageV2 wrapper {analysisOrdinal, stageId, entries, coverageCommitment} with entries CoverageResultV3.",
        "entries": "CoverageResultV3 {schemaVersion 3, key CoverageKeyV2, entry ViewEntryV3} is the ENTRY type, never a frame. It carries no stageId and no entryOrdinal: the wrapper stageId attributes every entry and entries[i] answers requestedCoverageDomain.keys[i] of that stage (the inherited entryOrdinal is the array index). entries[i].key.relation, resolution and subjectScopeCommitment equal keys[i]; entries[i].key.sourceUniverse and targetUniverse are the 64-hex suffixes of keys[i].sourceUniverseId and targetUniverseId; the request key's producer, producerVersion and schemaVersion remain request coordinates that CoverageKeyV2 does not restate. The entry count equals the requested key count.",
        "commitments": "The recipes and domains of the wrapper coverageCommitment, typescript-semantic StageResultV1.coverageCommitment and CompleteV1.coverageStreamCommitment, and rust-semantic commitments.stageCoverage, commitments.coverageStream and StageResultV2.coverageCommitment are unchanged; the values they commit are the ordered CoverageResultV3 values.",
        "terminals": "TypeScriptBudgetExhaustedV2 / BudgetExhaustedV3 and post-Analyze TypeScriptUnavailableV2 / UnavailableV3 keep their inherited members; their coverage arrays hold CoverageResultV3 in stage-major/key order, so entry k belongs to the stage whose cumulative requested-key range contains k. The unknown entries carry deficiency budget-exhausted or provider-unavailable respectively.",
        "ordering": "delivery.v2 ordering.stageOrder and multiStageAnalyze.stageOutputOrder (zero or more FactBatch, then exactly one Coverage per requested stage) and protocol3-transitions P3-24 are unchanged.",
    },
    "postAnalyzeReasons": {"typescript-semantic": TS_POST_REASONS, "rust-semantic": RS_POST_REASONS},
    "cancellation": {
        "typescript-semantic": "CancelledV1.observedPhase is snapshot for a Cancel the worker receives after emitting SnapshotAccepted and before receiving Analyze: the inserted NativeContextVerified interval, including after its NativeContextVerified emission (host phases WAIT_NATIVE_CONTEXT_VERIFIED and READY_ANALYZE at Cancel). No enum member or terminal route is added. delivery.v2 ordering.cancelTransition and supervision.userCancellation precedence are unchanged, and the observedPhase meaning of every other interval is inherited and not restated here.",
        "hostPhasesAtCancel": ["WAIT_NATIVE_CONTEXT_VERIFIED", "READY_ANALYZE"],
        "observedPhase": "snapshot",
        "rust-semantic": "CancelledV2.observedPhase remains the exact concrete phase at Cancel receipt; unchanged.",
    },
}

defs = {
    "Uint64": {"type": "integer", "minimum": 0, "maximum": 18446744073709551615},
    "DigestHex": {"type": "string", "pattern": "^[0-9a-f]{64}(?![\\s\\S])"},
    "Sha256Text": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}(?![\\s\\S])"},
    "NfcText": {"type": "string", "minLength": 1, "description": "non-empty text; NFC is checked by admission"},
    "ExecutionIdText": {"type": "string", "minLength": 1, "description": "host-allocated ExecutionId text, exact AttemptRecord value (rust-semantic IdentityText rules checked by admission)"},
    "SnapshotId2": {"type": "string", "pattern": "^snapshot2:[0-9a-f]{64}(?![\\s\\S])"},
    "PlanId2": {"type": "string", "pattern": "^plan2:[0-9a-f]{64}(?![\\s\\S])"},
    "StageIdText": {"type": "string", "minLength": 1, "maxLength": 255, "description": "C-2 stageId text"},
    "TypeScriptSemanticUniverseV2": envelope(su["typescript-v1"], 2, "TypeScriptUniverseV2ResolvedInputs", "typescript-v1"),
    "RustSemanticUniverseV2": envelope(su["rust-v1"], 3, "RustUniverseV2ResolvedInputs", "rust-v1"),
    "TypeScriptOpenUniverseV2": wrapper(ts_ps["OpenUniverseV1"]["required"], {
        "executionId": ref("ExecutionIdText"), "snapshotId": ref("SnapshotId2"), "planId": ref("PlanId2"),
        "planIntentCommitment": ref("Sha256Text"), "providerId": {"const": "typescript-semantic"},
        "universe": ref("TypeScriptSemanticUniverseV2"), "universeKey": ref("Sha256Text")},
        "typescript-semantic major-2 OpenUniverse: OpenUniverseV1 members with successor types."),
    "TypeScriptUniverseAcceptedV2": wrapper(ts_ps["UniverseAcceptedV1"]["required"], {
        "executionId": ref("ExecutionIdText"), "snapshotId": ref("SnapshotId2"), "planId": ref("PlanId2"),
        "universeKey": ref("Sha256Text")},
        "typescript-semantic major-2 UniverseAccepted: UniverseAcceptedV1 members; universeKey is the worker recomputation."),
    "OpenUniverseV3": wrapper(rs_ps["OpenUniverseV2"]["required"], {
        "executionId": ref("ExecutionIdText"), "snapshotId": ref("SnapshotId2"), "planId": ref("PlanId2"),
        "planIntentCommitment": ref("Sha256Text"), "providerId": {"const": "rust-semantic"},
        "universe": ref("RustSemanticUniverseV2"), "repositoryResolution": bref("RepositoryResolutionV3")},
        "rust-semantic major-3 OpenUniverse: OpenUniverseV2 members with successor types; no mode booleans."),
    "UniverseAcceptedV3": wrapper(rs_ps["UniverseAcceptedV2"]["required"], {
        "executionId": ref("ExecutionIdText"), "snapshotId": ref("SnapshotId2"), "planId": ref("PlanId2"),
        "providerId": {"const": "rust-semantic"}, "universe": ref("RustSemanticUniverseV2"),
        "repositoryResolution": bref("RepositoryResolutionV3")},
        "rust-semantic major-3 UniverseAccepted: exact recursive echo of OpenUniverseV3 members."),
    "NativeContextVerifiedV1": closed(["nativeContextId", "recomputedNativeContextId", "equal"], {
        "nativeContextId": ref("Sha256Text"), "recomputedNativeContextId": ref("Sha256Text"), "equal": {"const": True}},
        "native-evidence 9.2 NativeContextVerified payload, both languages."),
    "PreAnalyzeUnavailableV1": closed(
        ["executionId", "snapshotId", "planId", "reason", "nativeContextId", "recomputedNativeContextId"], {
            "executionId": ref("ExecutionIdText"), "snapshotId": ref("SnapshotId2"), "planId": ref("PlanId2"),
            "reason": {"const": "native-context-mismatch"}, "nativeContextId": ref("Sha256Text"),
            "recomputedNativeContextId": ref("Sha256Text")},
        "Pre-Analyze Unavailable payload, both languages; only in the NativeContextVerified interval; carries no requested stage or coverage."),
    "TypeScriptCoverageV2": wrapper(ts_ps["CoverageV1"]["required"], {
        "analysisOrdinal": {"const": 0}, "stageId": ref("StageIdText"), "entries": COVERAGE_ENTRIES,
        "coverageCommitment": ref("Sha256Text")},
        "typescript-semantic frame Coverage payload: CoverageV1 wrapper with CoverageResultV3 entries."),
    "CoverageV3": wrapper(rs_ps["CoverageV2"]["required"], {
        "analysisOrdinal": ref("Uint64"), "stageId": ref("StageIdText"), "entries": COVERAGE_ENTRIES,
        "coverageCommitment": ref("Sha256Text")},
        "rust-semantic frame CoverageV3 payload: CoverageV2 wrapper with CoverageResultV3 entries."),
    "TypeScriptUnavailableV2": wrapper(ts_ps["UnavailableV1"]["required"], {
        "analysisOrdinal": {"const": 0}, "affectedStageIds": STAGE_IDS, "reason": {"type": "string", "enum": TS_POST_REASONS},
        "coverage": TERMINAL_COVERAGE, "coverageCommitment": ref("Sha256Text")},
        "typescript-semantic post-Analyze Unavailable (immediately after Analyze): UnavailableV1 members, CoverageResultV3 coverage, reason never native-context-mismatch."),
    "UnavailableV3": wrapper(rs_ps["UnavailableV2"]["required"], {
        "analysisOrdinal": ref("Uint64"), "affectedStageIds": STAGE_IDS, "reason": {"type": "string", "enum": RS_POST_REASONS},
        "coverage": TERMINAL_COVERAGE, "coverageCommitment": ref("Sha256Text")},
        "rust-semantic post-Analyze Unavailable (P3-25): UnavailableV2 members, CoverageResultV3 coverage, reason never native-context-mismatch."),
    "TypeScriptBudgetExhaustedV2": wrapper(ts_ps["BudgetExhaustedV1"]["required"], {
        "analysisOrdinal": {"const": 0}, "triggerStageId": ref("StageIdText"),
        "dimension": {"type": "string", "enum": BUDGET_DIMENSIONS}, "limit": ref("Uint64"), "observed": ref("Uint64"),
        "coverage": TERMINAL_COVERAGE, "coverageCommitment": ref("Sha256Text")},
        "typescript-semantic BudgetExhausted: BudgetExhaustedV1 members, CoverageResultV3 coverage."),
    "BudgetExhaustedV3": wrapper(rs_ps["BudgetExhaustedV2"]["required"], {
        "analysisOrdinal": ref("Uint64"), "triggerStageId": ref("StageIdText"),
        "unit": {"type": "string", "enum": RS_BUDGET_UNITS}, "limit": ref("Uint64"), "observed": ref("Uint64"),
        "coverage": TERMINAL_COVERAGE, "coverageCommitment": ref("Sha256Text")},
        "rust-semantic BudgetExhausted: BudgetExhaustedV2 members, CoverageResultV3 coverage."),
}

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensip.product.provider-startup.1",
    "title": "Provider startup and coverage successors: typescript-semantic major 2 and rust-semantic major 3",
    "description": "Closed JSON-vector records of deterministic-CBOR wire maps for OpenUniverse, UniverseAccepted, NativeContextVerified, pre-Analyze Unavailable, Coverage and terminal coverage payloads. Entry records CoverageResultV3, RepositoryResolutionV3 and the v2 resolvedInputs are referenced from the registered bundle by $id and are not redefined.",
    "x-opensip-startup-law": law,
    "$defs": defs,
}

PHASES = ["START", "WAIT_HELLO_ACK", "READY_OPEN_UNIVERSE", "WAIT_UNIVERSE_ACCEPTED", "READY_SNAPSHOT_MANIFEST",
          "RECEIVING_SNAPSHOT", "WAIT_SNAPSHOT_ACCEPTED", "WAIT_NATIVE_CONTEXT_VERIFIED", "READY_ANALYZE", "ANALYZING",
          "READY_COMPLETE", "WAIT_CANCELLED", "WAIT_ZERO_EXIT", "WAIT_EOF", "DONE", "FAULT"]
ORD = "delivery.v2 $.typescriptSemanticSubstrate.providerProtocol.ordering"


def rule(rid, phase, frame, nxt, source, guard=None, terminal=None):
    row = {"id": rid, "phase": phase, "frame": frame}
    if guard:
        row["guard"] = guard
    row["next"] = nxt
    if terminal:
        row["terminal"] = terminal
    row["source"] = source
    return row


rules = [
    rule("T2-01", "START", "Hello", "WAIT_HELLO_ACK", ORD + ".normalPhases[0]"),
    rule("T2-02", "WAIT_HELLO_ACK", "HelloAck", "READY_OPEN_UNIVERSE", ORD + ".normalPhases[0]"),
    rule("T2-03", "READY_OPEN_UNIVERSE", "OpenUniverse", "WAIT_UNIVERSE_ACCEPTED", ORD + ".normalPhases[1]; native-evidence 9.1 step 3", guard={"identityNegotiated": True}),
    rule("T2-04", "WAIT_UNIVERSE_ACCEPTED", "UniverseAccepted", "READY_SNAPSHOT_MANIFEST", ORD + ".normalPhases[1]"),
    rule("T2-05", "READY_SNAPSHOT_MANIFEST", "SnapshotManifest", "RECEIVING_SNAPSHOT", ORD + ".normalPhases[2]"),
    rule("T2-06", "RECEIVING_SNAPSHOT", "SnapshotFileChunk", "RECEIVING_SNAPSHOT", ORD + ".normalPhases[2]"),
    rule("T2-07", "RECEIVING_SNAPSHOT", "SnapshotSeal", "WAIT_SNAPSHOT_ACCEPTED", ORD + ".normalPhases[2]"),
    rule("T2-08", "WAIT_SNAPSHOT_ACCEPTED", "SnapshotAccepted", "WAIT_NATIVE_CONTEXT_VERIFIED", ORD + ".normalPhases[2]; native-evidence 9.4 insertion"),
    rule("T2-09", "WAIT_NATIVE_CONTEXT_VERIFIED", "NativeContextVerified", "READY_ANALYZE", "native-evidence 9.4 insertion"),
    rule("T2-10", "WAIT_NATIVE_CONTEXT_VERIFIED", "Unavailable", "WAIT_ZERO_EXIT", "native-evidence 9.7 pre-Analyze Unavailable", guard={"unavailablePayload": "pre-analyze"}, terminal="unavailable"),
    rule("T2-11", "READY_ANALYZE", "Analyze", "ANALYZING", ORD + ".normalPhases[3]"),
    rule("T2-12", "ANALYZING", "FactBatch", "ANALYZING", ORD + ".stageOrder"),
    rule("T2-13", "ANALYZING", "Coverage", "ANALYZING_OR_READY_COMPLETE", ORD + ".stageOrder"),
    rule("T2-14", "ANALYZING", "Unavailable", "WAIT_ZERO_EXIT", ORD + ".unavailableTerminal", guard={"unavailablePayload": "post-analyze", "outputSeen": False}, terminal="unavailable"),
    rule("T2-15", "ANALYZING", "BudgetExhausted", "WAIT_ZERO_EXIT", ORD + ".budgetTerminal", terminal="budget-exhausted"),
    rule("T2-16", "READY_COMPLETE", "BudgetExhausted", "WAIT_ZERO_EXIT", ORD + ".budgetTerminal", terminal="budget-exhausted"),
    rule("T2-17", "READY_COMPLETE", "Complete", "WAIT_ZERO_EXIT", ORD + ".normalTerminal", terminal="complete"),
    rule("T2-18", "*PRE_TERMINAL", "Cancel", "WAIT_CANCELLED", ORD + ".cancelTransition"),
    rule("T2-19", "WAIT_CANCELLED", "Cancelled", "WAIT_EOF", ORD + ".cancelTransition", terminal="cancelled"),
    rule("T2-20", "WAIT_ZERO_EXIT", "zero-exit", "WAIT_EOF", ORD + ".normalTerminal"),
    rule("T2-21", "WAIT_EOF", "eof", "DONE", ORD + ".normalTerminal"),
    rule("T2-22", "*ANY", "*PROCESS_FAULT", "FAULT", "delivery.v2 $.typescriptSemanticSubstrate.supervision.protocolOrCrash"),
    rule("T2-23", "*ANY", "*", "FAULT", ORD + ".unknownOrContradictory"),
]
order = {
    "artifact": "opensip.native-evidence.typescript-protocol2-order",
    "version": 1,
    "status": "PROPOSED",
    "standing": "NORMATIVE and CLOSED abstract host event machine for typescript-semantic protocol major 2. It transcribes the inherited delivery.v2 providerProtocol.ordering and supervision terminal rules, adding exactly the native-evidence 9.4/9.7 successor insertions: NativeContextVerified between SnapshotAccepted and Analyze, and the pre-Analyze Unavailable(native-context-mismatch) terminal inside that interval. Payload validation is owned by native/provider-startup.schemas.v1.json, native/provider-handshake.schemas.v1.json and section 9 prose and is executed per frame by native_evidence_model.v2.provider_startup_exchange before an event reaches this table. It adds no frame and no terminal kind and changes no rust-semantic rule. Framing bytes, byte limits and exit-status policy after Cancelled are not modeled; supervision.userCancellation D9 precedence governs any process observation after Cancel.",
    "consumedBy": "docs/coop/design-corrections/native/provider_startup_model.v1.py (typescript_protocol2_run)",
    "phases": PHASES,
    "initialState": {"phase": "START", "identityNegotiated": False, "stageIndex": 0, "stageCount": 0, "stagesCompleted": 0,
                     "outputSeen": False, "terminalKind": None, "sourceBytesSent": False, "cancelPhase": None},
    "matchLaw": "FIRST MATCH WINS in the declared rules order. A row matches when its phase equals the current phase (or the current phase is a member of the *PRE_TERMINAL wildcard), its frame equals the event frame, and every guard key equals the named host state field or derived event observation. The rows are pairwise disjoint.",
    "guardLaw": "Guard keys name host state fields or the derived event observations listed in eventObservations; comparison is exact equality.",
    "eventObservations": {
        "unavailablePayload": "derived by provider_startup_model.admit_unavailable from the admitted payload: pre-analyze (PreAnalyzeUnavailableV1) or post-analyze (TypeScriptUnavailableV2); never a wire member",
        "capabilities": "the admitted TypeScriptHelloAckV2 token array",
    },
    "wildcards": {
        "*ANY": "phase wildcard of the two catch-all rows; applied by preMatchLaw and noMatchLaw only",
        "*PRE_TERMINAL": {"phases": PHASES[:11], "meaning": "START through READY_COMPLETE: any nonterminal state (ordering.cancelTransition)"},
        "*": "frame wildcard of the final fallback row",
        "*PROCESS_FAULT": {"frames": ["deadline", "nonzero-exit", "signal-death", "stdout-byte"]},
    },
    "preMatchLaw": [
        "FAULT is absorbing: every further event is traced FAULT-absorb.",
        "In WAIT_ZERO_EXIT, WAIT_EOF or DONE any frame other than zero-exit, eof or a *PROCESS_FAULT member is a post-terminal frame: FAULT, trace post-terminal-frame.",
        "Any *PROCESS_FAULT member goes to FAULT with trace T2-22.",
    ],
    "noMatchLaw": "An event matching no row goes to FAULT with trace T2-23.",
    "stateUpdates": [
        {"onFrame": "HelloAck", "sets": "identityNegotiated = every identity token is present in the admitted capabilities"},
        {"onFrame": "Analyze", "sets": "stageCount = the invocation's stage count; stageIndex = 0; outputSeen = false"},
        {"onFrames": ["FactBatch", "Coverage"], "sets": "outputSeen = true"},
        {"onFrame": "Cancel", "sets": "cancelPhase = the phase in which Cancel was sent"},
        {"onFrames": ["OpenUniverse", "SnapshotFileChunk", "SnapshotManifest"], "sets": "sourceBytesSent = true"},
    ],
    "stageDependentTransitions": {"ANALYZING_OR_READY_COMPLETE": "The next of T2-13 increments stageIndex and stagesCompleted and resolves to READY_COMPLETE when stageIndex equals stageCount, otherwise ANALYZING."},
    "terminalLaw": "A row carrying terminal records terminalKind. After unavailable, budget-exhausted or complete the worker must still reach zero-exit then eof; after cancelled only eof is required (ordering.cancelTransition).",
    "cancellationObservedPhase": {"hostPhasesAtCancel": law["cancellation"]["hostPhasesAtCancel"], "observedPhase": "snapshot",
                                  "rule": law["cancellation"]["typescript-semantic"]},
    "ruleCount": len(rules),
    "rules": rules,
}

for path, doc in ((OUT_SCHEMA, schema), (OUT_ORDER, order)):
    if path.exists():
        raise SystemExit("refusing to overwrite " + str(path))
    path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote", path.name, hashlib.sha256(path.read_bytes()).hexdigest())
print(json.dumps({"tsPostAnalyzeReasons": TS_POST_REASONS, "rustPostAnalyzeReasons": RS_POST_REASONS,
                  "budgetDimensions": BUDGET_DIMENSIONS}))
