"""Author provider-startup fixtures and cases into the work copy's native-cases.v2.json.

usage: author_startup_cases.py <work-candidate-root>

Expected identities are computed here WITHOUT the model under test: the foundation H recipe is re-implemented
with hashlib over stdlib sorted compact JSON and first checked against an existing hand-spelled fixture
commitment. Fixtures and cases are spliced textually so every pre-existing byte is preserved; the result is
re-parsed and the prior content compared.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
CASES = ROOT / "docs" / "coop" / "design-corrections" / "native" / "native-cases.v2.json"
raw_before = CASES.read_bytes()
original = json.loads(raw_before)
fx = original["fixtures"]


def canon(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def h(domain, value):
    raw = canon(value)
    return hashlib.sha256(b"opensip.product.v1\0" + domain.encode("ascii") + b"\0" + len(raw).to_bytes(8, "big") + raw).hexdigest()


# Independent recipe check against the existing hand-spelled fixture pair before any value is derived from it.
assert "sha256:" + h("subject-scope", fx["scopeDescriptor"]) == fx["coveragePayload"]["key"]["subjectScopeCommitment"]

TS, RS = "typescript-semantic", "rust-semantic"
EXEC = "exec-2026-09-13-0001"
SNAP = "snapshot2:" + "5a" * 32
PLAN = "plan2:" + "5b" * 32
INTENT = "sha256:" + "5c" * 32
ts_ack = fx["wireTsHelloAck"]
rust_identity = fx["wireRustIdentity"]

ts_inputs_resolved = copy.deepcopy(fx["tsUniverse"])
ts_universe = {"schemaVersion": 1, "manifestId": "66" * 32, "capabilityManifestId": "77" * 32,
               "runtimeArtifactId": "typescript-runtime", "runtimeArtifactSha256": "16" * 32,
               "providerArtifactId": "typescript-provider", "providerArtifactSha256": "17" * 32,
               "runtimeDescriptorSha256": ts_ack["runtimeDescriptorSha256"],
               "providerDescriptorSha256": ts_ack["providerDescriptorSha256"], "protocolMajor": 2,
               "providerBuildId": ts_ack["providerBuildId"], "nodeVersion": ts_ack["nodeVersion"],
               "v8Version": ts_ack["v8Version"], "modulesAbi": ts_ack["modulesAbi"],
               "typescriptVersion": ts_ack["typescriptVersion"], "typescriptCompilerSha256": ts_ack["typescriptCompilerSha256"],
               "typescriptStdlibMerkleRoot": ts_ack["typescriptStdlibMerkleRoot"], "platformId": ts_ack["platformId"],
               "resolvedInputs": ts_inputs_resolved}
ts_hex = h("native.semantic-universe.typescript.v2", ts_inputs_resolved)
ts_key = "sha256:" + ts_hex
ts_context = ts_inputs_resolved["nativeContextId"]

rust_resolved = {"schemaVersion": 2, "edition": {"app": 2021},
                 "lockfileIdentity": {"path": "Cargo.lock", "contentSha256": "ab" * 32, "lockfileVersion": 4},
                 "dependencySourceSetId": "sha256:" + "44" * 32, "unifiedFeaturesId": "sha256:" + "45" * 32,
                 "nativeContextId": "sha256:" + "46" * 32, "cfgSets": [{"cfgSetId": "primary", "cfg": []}],
                 "rustflags": {"executableSelected": False, "honored": [], "stripped": []},
                 "crateRootPaths": ["src/lib.rs"], "configProjectionSha256": "47" * 32, "preparedResolution": "none",
                 "executionCapableResolution": False, "preparedOutputSetId": None, "sourceUnitOwnershipId": None}
rust_resolved_prepared = dict(copy.deepcopy(rust_resolved), preparedResolution="host-prepared",
                              executionCapableResolution=True, preparedOutputSetId="sha256:" + "48" * 32)


def rust_universe(resolved):
    return {"schemaVersion": 1, "manifestId": "66" * 32, "capabilityManifestId": "77" * 32,
            "providerArtifactId": "rust-provider", "providerArtifactSha256": "88" * 32,
            "toolchainArtifactId": "rust-toolchain-bundle", "toolchainArtifactSha256": "99" * 32, "protocolMajor": 3,
            "providerBuildId": rust_identity["providerBuildId"], "rustCommitHash": rust_identity["rustCommitHash"],
            "rustcVersion": "rustc 1.90.0", "cargoVersion": "cargo 1.90.0", "hostTriple": rust_identity["hostTriple"],
            "targetTriple": rust_identity["targetTriple"], "sysrootDigest": rust_identity["sysrootDigest"],
            "rustcDevLlvmDigest": "cc" * 32, "standardLibraryComponentDigests": {"core": "ee" * 32, "std": "ff" * 32},
            "providerBinarySha256": "12" * 32, "licenseNoticeBundleSha256": "13" * 32, "platformId": "macos-aarch64",
            "resolvedInputs": copy.deepcopy(resolved)}


rust_hex = h("native.semantic-universe.rust.v2", rust_resolved)
effects = copy.deepcopy(fx["auth"]["effects"])
AUTH_ID = "sha256:" + "49" * 32


def open_ts():
    return {"executionId": EXEC, "snapshotId": SNAP, "planId": PLAN, "planIntentCommitment": INTENT,
            "providerId": TS, "universe": copy.deepcopy(ts_universe), "universeKey": ts_key}


def open_rust(prepared=False):
    resolved = rust_resolved_prepared if prepared else rust_resolved
    return {"executionId": EXEC, "snapshotId": SNAP, "planId": PLAN, "planIntentCommitment": INTENT, "providerId": RS,
            "universe": rust_universe(resolved),
            "repositoryResolution": {"dependencySourceSetId": resolved["dependencySourceSetId"],
                                     "preparedOutputSetId": resolved["preparedOutputSetId"],
                                     "authorizationId": AUTH_ID if prepared else None,
                                     "workerExecutesRepositoryCode": False,
                                     "effects": copy.deepcopy(effects) if prepared else None}}


def descriptor(universe_hex, relation, resolution, subjects):
    return {"schemaVersion": 2, "snapshotId": SNAP, "sourceUniverse": universe_hex, "targetUniverse": universe_hex,
            "relation": relation, "resolution": resolution, "enumeratorClosure": "closure2:" + "e4" * 32,
            "subjects": sorted(subjects, key=canon)}


def commitment(desc):
    return "sha256:" + h("subject-scope", desc)


def coverage_result(desc, coverage="complete"):
    entry = copy.deepcopy(fx["coveragePayload"]["entry"])
    entry["relation"], entry["resolution"], entry["coverage"] = desc["relation"], desc["resolution"], coverage
    entry["examinedUniverse"] = {"subjectScopeCommitment": commitment(desc), "subjectCount": len(desc["subjects"])}
    return {"schemaVersion": 3, "key": {"relation": desc["relation"], "resolution": desc["resolution"],
                                        "sourceUniverse": desc["sourceUniverse"], "targetUniverse": desc["targetUniverse"],
                                        "subjectScopeCommitment": commitment(desc)}, "entry": entry}


def requested_key(desc, universe_key, producer, version):
    return {"relation": desc["relation"], "resolution": desc["resolution"], "sourceUniverseId": universe_key,
            "targetUniverseId": universe_key, "subjectScopeCommitment": commitment(desc), "producer": producer,
            "producerVersion": version, "schemaVersion": 1}


ts_refs = descriptor(ts_hex, "references", "resolved-binding", ["src/a.ts#bar", "src/a.ts#foo", "src/b.ts#main"])
ts_declares = descriptor(ts_hex, "declares", "syntactic", ["src/a.ts", "src/b.ts"])
rust_refs = descriptor(rust_hex, "references", "resolved-binding", ["src/lib.rs#main"])
unknown_entry = coverage_result(ts_refs, "unknown")
unknown_entry["entry"].update({"deficiency": "provider-unavailable", "confidenceMillionths": 0})
unknown_entry["entry"]["resolutionCompleteness"] = {"state": "partial", "attempted": True, "examinedExhaustive": False,
                                                    "stageTerminal": "unavailable", "unresolvedEdgeCount": 0,
                                                    "unresolvedEdgeClasses": []}
rust_unknown = coverage_result(rust_refs, "unknown")
rust_unknown["entry"].update({"deficiency": "provider-unavailable", "confidenceMillionths": 0})
rust_unknown["entry"]["resolutionCompleteness"] = dict(unknown_entry["entry"]["resolutionCompleteness"])

new_fixtures = {
    "startupTsOpenUniverse": open_ts(),
    "startupTsUniverseAccepted": {"executionId": EXEC, "snapshotId": SNAP, "planId": PLAN, "universeKey": ts_key},
    "startupTsNativeContextVerified": {"nativeContextId": ts_context, "recomputedNativeContextId": ts_context, "equal": True},
    "startupTsPreAnalyzeUnavailable": {"executionId": EXEC, "snapshotId": SNAP, "planId": PLAN,
                                       "reason": "native-context-mismatch", "nativeContextId": ts_context,
                                       "recomputedNativeContextId": "sha256:" + "0d" * 32},
    "startupTsPostAnalyzeUnavailable": {"analysisOrdinal": 0, "affectedStageIds": ["s-refs"],
                                        "reason": "semantic-universe-incomplete", "coverage": [unknown_entry],
                                        "coverageCommitment": "sha256:" + "c0" * 32},
    "startupTsCoverage": {"analysisOrdinal": 0, "stageId": "s-refs", "entries": [coverage_result(ts_refs)],
                          "coverageCommitment": "sha256:" + "c1" * 32},
    "startupTsCoverageResultV1Entry": {"stageId": "s-refs", "entryOrdinal": 0, "coverageState": "complete",
                                       "key": requested_key(ts_refs, ts_key, TS, ts_ack["providerBuildId"]), "deficiency": None},
    "startupTsInputs": {
        "envelopeProtocolMajor": 2, "signedRow": fx["ts2"],
        "helloExpected": {"hostBuildId": fx["wireTsHello"]["hostBuildId"], "providerDescriptor": fx["wireTsProviderDescriptor"],
                          "runtimeDescriptor": fx["wireTsRuntimeDescriptor"]},
        "ackExpected": {"providerDescriptor": fx["wireTsProviderDescriptor"], "runtimeDescriptor": fx["wireTsRuntimeDescriptor"]},
        "universeExpected": {"executionId": EXEC, "snapshotId": SNAP, "planId": PLAN, "planIntentCommitment": INTENT,
                             "planNativeContextDigests": [ts_context.removeprefix("sha256:")]},
        "analyzeStages": [{"stageId": "s-refs", "requestedKeys": [requested_key(ts_refs, ts_key, TS, ts_ack["providerBuildId"])]}],
        "plannedStages": [{"stageId": "s-refs", "scopeDescriptors": [ts_refs]},
                          {"stageId": "s-declares", "scopeDescriptors": [ts_declares]}]},
    "startupRustOpenUniverse": open_rust(),
    "startupRustOpenUniversePrepared": open_rust(prepared=True),
    "startupRustUniverseAccepted": {k: v for k, v in open_rust().items() if k != "planIntentCommitment"},
    "startupRustNativeContextVerified": {"nativeContextId": rust_resolved["nativeContextId"],
                                         "recomputedNativeContextId": rust_resolved["nativeContextId"], "equal": True},
    "startupRustPreAnalyzeUnavailable": {"executionId": EXEC, "snapshotId": SNAP, "planId": PLAN,
                                         "reason": "native-context-mismatch", "nativeContextId": rust_resolved["nativeContextId"],
                                         "recomputedNativeContextId": "sha256:" + "0e" * 32},
    "startupRustPostAnalyzeUnavailable": {"analysisOrdinal": 0, "affectedStageIds": ["s-refs"],
                                          "reason": "semantic-universe-incomplete", "coverage": [rust_unknown],
                                          "coverageCommitment": "sha256:" + "c2" * 32},
    "startupRustCoverage": {"analysisOrdinal": 0, "stageId": "s-refs", "entries": [coverage_result(rust_refs)],
                            "coverageCommitment": "sha256:" + "c3" * 32},
    "startupRustEmptyDependencyManifest": {"dependencySourceSetId": rust_resolved["dependencySourceSetId"],
                                           "manifestSha256": "d0" * 32, "entries": []},
    "startupRustEmptyDependencySeal": {"dependencySourceSetId": rust_resolved["dependencySourceSetId"],
                                       "manifestSha256": "d0" * 32, "entryCount": 0, "totalBytes": 0, "totalChunkCount": 0},
    "startupRustInputs": {
        "envelopeProtocolMajor": 3, "signedRow": fx["rust3"],
        "helloExpected": {"hostBuildId": fx["wireRustHello"]["hostBuildId"], "identity": rust_identity},
        "ackExpected": {},
        "universeExpected": {"executionId": EXEC, "snapshotId": SNAP, "planId": PLAN, "planIntentCommitment": INTENT,
                             "planNativeContextDigests": [rust_resolved["nativeContextId"].removeprefix("sha256:")],
                             "preparedAuthorization": {"authorizationId": AUTH_ID, "effects": effects}},
        "analyzeStages": [{"stageId": "s-refs", "requestedKeys": [requested_key(rust_refs, "sha256:" + rust_hex, RS, rust_identity["providerBuildId"])]}],
        "plannedStages": [{"stageId": "s-refs", "scopeDescriptors": [rust_refs]}]},
}
assert not set(new_fixtures) & set(fx)


def F(name, payload=None):
    row = {"frame": name}
    if payload is not None:
        row["payload"] = payload
    return row


TS_PREFIX = [F("Hello", "$fixtures.wireTsHello"), F("HelloAck", "$fixtures.wireTsHelloAck"),
             F("OpenUniverse", "$fixtures.startupTsOpenUniverse"), F("UniverseAccepted", "$fixtures.startupTsUniverseAccepted"),
             F("SnapshotManifest"), F("SnapshotSeal"), F("SnapshotAccepted")]
TS_NCV = [F("NativeContextVerified", "$fixtures.startupTsNativeContextVerified")]
TS_HAPPY = TS_PREFIX + TS_NCV + [F("Analyze"), F("Coverage", "$fixtures.startupTsCoverage"), F("Complete"), F("zero-exit"), F("eof")]
TS_PRE = TS_PREFIX + [F("Unavailable", "$fixtures.startupTsPreAnalyzeUnavailable"), F("zero-exit"), F("eof")]
RS_PREFIX = [F("Hello", "$fixtures.wireRustHello"), F("HelloAck", "$fixtures.wireRustHelloAck"),
             F("OpenUniverse", "$fixtures.startupRustOpenUniverse"), F("UniverseAccepted", "$fixtures.startupRustUniverseAccepted"),
             F("SnapshotManifest"), F("SnapshotSeal"), F("SnapshotAccepted"),
             F("DependencySourceManifest"), F("DependencySourceSeal"), F("DependencySourceAccepted")]
RS_HAPPY = RS_PREFIX + [F("NativeContextVerified", "$fixtures.startupRustNativeContextVerified"), F("Analyze"),
                        F("CoverageV3", "$fixtures.startupRustCoverage"), F("Complete"), F("zero-exit"), F("eof")]
RS_PRE = RS_PREFIX + [F("Unavailable", "$fixtures.startupRustPreAnalyzeUnavailable"), F("zero-exit"), F("eof")]


def merge(base, **with_):
    return {"$merge": base, "$with": with_}


def exchange(language, frames, inputs=None, bind="r"):
    return {"fn": "provider_startup_exchange",
            "args": {"language": language, "frames": frames,
                     "inputs": inputs or ("$fixtures.startupTsInputs" if language == TS else "$fixtures.startupRustInputs")},
            "bind": bind}


def replace(frames, index, **payload_with):
    out = copy.deepcopy(frames)
    out[index] = {"frame": out[index]["frame"], "payload": merge(out[index]["payload"], **payload_with)}
    return out


def refused(key, frame, detail_head=None):
    exp = {"$r.finalPhase": "FAULT", "$r.refusal.key": key, "$r.refusal.frame": frame,
           "$r.hostConversion.stageAuthority.authority": "none"}
    if detail_head is not None:
        exp["$r.refusal.detailHead"] = detail_head
    return exp


def case(cid, kind, steps, expect):
    return {"id": "startup-" + cid, "feedback": ["F1"], "kind": kind, "steps": steps, "expect": expect}


cases = [
    # ---- typescript-semantic major 2
    case("ts2-open-universe-accepted-native-context-verified-complete", "positive", [exchange(TS, TS_HAPPY)],
         {"$r.finalPhase": "DONE", "$r.terminalKind": "complete", "$r.identityNegotiated": True, "$r.refusal": None,
          "$r.hostConversion": None,
          "$r.trace": ["T2-01", "T2-02", "T2-03", "T2-04", "T2-05", "T2-07", "T2-08", "T2-09", "T2-11", "T2-13", "T2-17", "T2-20", "T2-21"]}),
    case("ts2-pre-analyze-unavailable-host-derives-provider-unavailable-coverage", "positive", [exchange(TS, TS_PRE)],
         {"$r.finalPhase": "DONE", "$r.terminalKind": "unavailable", "$r.refusal": None,
          "$r.trace": ["T2-01", "T2-02", "T2-03", "T2-04", "T2-05", "T2-07", "T2-08", "T2-10", "T2-20", "T2-21"],
          "$r.hostConversion.coverageSource": "host-derived", "$r.hostConversion.workerCoverageCarried": False,
          "$r.hostConversion.allAdmitted": True, "$r.hostConversion.affectedStageIds": ["s-refs", "s-declares"],
          "$r.hostConversion.stageAuthority.d9.code": "COVERAGE.PROVIDER_UNAVAILABLE",
          "$r.hostConversion.termination.d9.code": "COVERAGE.PROVIDER_UNAVAILABLE",
          "$r.hostConversion.stages.0.coverage.0.payload.entry.resolutionCompleteness.state": "not-attempted",
          "$r.hostConversion.stages.0.coverage.0.payload.entry.resolutionCompleteness.stageTerminal": "unavailable",
          "$r.hostConversion.stages.1.coverage.0.payload.entry.resolutionCompleteness.state": "not-applicable",
          "$r.hostConversion.stages.0.coverage.0.payload.key.subjectScopeCommitment": commitment(ts_refs)}),
    case("ts2-open-universe-plan1-plan-id-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 2, planId="plan1:sha256:" + "5b" * 32))],
         refused("SCHEMA", "OpenUniverse", "TypeScriptOpenUniverseV2:/planId")),
    case("ts2-open-universe-v1-snapshot-id-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 2, snapshotId="snap1:sha256:" + "5a" * 32))],
         refused("SCHEMA", "OpenUniverse", "TypeScriptOpenUniverseV2:/snapshotId")),
    case("ts2-open-universe-carrying-rust-repository-resolution-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 2, repositoryResolution="$fixtures.startupRustOpenUniverse.repositoryResolution"))],
         refused("SCHEMA", "OpenUniverse", "TypeScriptOpenUniverseV2:/")),
    case("ts2-open-universe-v1-universe-key-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 2, universeKey="sha256:" + "5d" * 32))],
         refused("UNIVERSE_KEY", "OpenUniverse")),
    case("ts2-open-universe-native-context-not-plan-bound-refused", "negative",
         [exchange(TS, TS_HAPPY, merge("$fixtures.startupTsInputs", **{"universeExpected.planNativeContextDigests": ["5e" * 32]}))],
         refused("NATIVE_CONTEXT_NOT_PLAN_BOUND", "OpenUniverse")),
    case("ts2-open-universe-universe-not-the-verified-handshake-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 2, **{"universe.nodeVersion": "22.9.1"}))],
         refused("UNIVERSE_HANDSHAKE_JOIN", "OpenUniverse", "nodeVersion")),
    case("ts2-open-universe-major-1-universe-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 2, **{"universe.protocolMajor": 1}))],
         refused("SCHEMA", "OpenUniverse", "TypeScriptOpenUniverseV2:/universe/protocolMajor")),
    case("ts2-open-universe-correlation-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 2, executionId="exec-other"))],
         refused("OPEN_UNIVERSE_CORRELATION", "OpenUniverse", "executionId")),
    case("ts2-universe-accepted-echo-mismatch-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 3, universeKey="sha256:" + "5d" * 32))],
         refused("UNIVERSE_ACCEPTED_ECHO", "UniverseAccepted", "universeKey")),
    case("ts2-native-context-verified-wrong-context-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 7, recomputedNativeContextId="sha256:" + "0d" * 32))],
         refused("NATIVE_CONTEXT_VERIFIED_JOIN", "NativeContextVerified", "recomputedNativeContextId")),
    case("ts2-pre-analyze-unavailable-other-reason-refused", "negative",
         [exchange(TS, replace(TS_PRE, 7, reason="capability-missing"))],
         refused("SCHEMA", "Unavailable", "PreAnalyzeUnavailableV1:/reason")),
    case("ts2-pre-analyze-unavailable-correlation-refused", "negative",
         [exchange(TS, replace(TS_PRE, 7, planId="plan2:" + "ee" * 32))],
         refused("PRE_ANALYZE_UNAVAILABLE_CORRELATION", "Unavailable", "planId")),
    case("ts2-pre-analyze-unavailable-equal-contexts-refused", "negative",
         [exchange(TS, replace(TS_PRE, 7, recomputedNativeContextId=ts_context))],
         refused("PRE_ANALYZE_UNAVAILABLE_NOT_A_MISMATCH", "Unavailable")),
    case("ts2-pre-analyze-payload-after-analyze-refused", "negative",
         [exchange(TS, TS_PREFIX + TS_NCV + [F("Analyze"), F("Unavailable", "$fixtures.startupTsPreAnalyzeUnavailable")])],
         refused("UNAVAILABLE_PHASE_PAYLOAD", "Unavailable")),
    case("ts2-post-analyze-payload-before-analyze-refused", "negative",
         [exchange(TS, TS_PREFIX + [F("Unavailable", "$fixtures.startupTsPostAnalyzeUnavailable")])],
         refused("UNAVAILABLE_PHASE_PAYLOAD", "Unavailable")),
    case("ts2-pre-analyze-unavailable-before-snapshot-accepted-faults", "negative",
         [exchange(TS, TS_PREFIX[:4] + [F("Unavailable", "$fixtures.startupTsPreAnalyzeUnavailable")])],
         {"$r.finalPhase": "FAULT", "$r.refusal": None, "$r.trace": ["T2-01", "T2-02", "T2-03", "T2-04", "T2-23"],
          "$r.hostConversion.stageAuthority.authority": "none"}),
    case("ts2-pre-analyze-unavailable-then-post-terminal-frame-faults", "negative",
         [exchange(TS, TS_PREFIX + [F("Unavailable", "$fixtures.startupTsPreAnalyzeUnavailable"), F("Analyze")])],
         {"$r.finalPhase": "FAULT", "$r.terminalKind": "unavailable", "$r.hostConversion.stages": [],
          "$r.hostConversion.stageAuthority.authority": "none"}),
    case("ts2-pre-analyze-unavailable-nonzero-exit-faults", "negative",
         [exchange(TS, TS_PREFIX + [F("Unavailable", "$fixtures.startupTsPreAnalyzeUnavailable"), F("nonzero-exit")])],
         {"$r.finalPhase": "FAULT", "$r.hostConversion.stageAuthority.authority": "none"}),
    case("ts2-post-analyze-unavailable-immediately-after-analyze", "positive",
         [exchange(TS, TS_PREFIX + TS_NCV + [F("Analyze"), F("Unavailable", "$fixtures.startupTsPostAnalyzeUnavailable"), F("zero-exit"), F("eof")])],
         {"$r.finalPhase": "DONE", "$r.terminalKind": "unavailable", "$r.hostConversion": None, "$r.refusal": None}),
    case("ts2-post-analyze-reason-native-context-mismatch-refused", "negative",
         [exchange(TS, TS_PREFIX + TS_NCV + [F("Analyze"), F("Unavailable", merge("$fixtures.startupTsPostAnalyzeUnavailable", reason="native-context-mismatch"))])],
         refused("UNAVAILABLE_PHASE_PAYLOAD", "Unavailable")),
    case("ts2-coverage-frame-with-coverage-result-v1-entry-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 9, entries=["$fixtures.startupTsCoverageResultV1Entry"]))],
         refused("SCHEMA", "Coverage", "TypeScriptCoverageV2:/entries/0")),
    case("ts2-coverage-entry-sent-as-the-whole-frame-refused", "negative",
         [exchange(TS, TS_PREFIX + TS_NCV + [F("Analyze"), F("Coverage", "$fixtures.startupTsCoverage.entries.0")])],
         refused("SCHEMA", "Coverage", "TypeScriptCoverageV2:/")),
    case("ts2-coverage-key-not-the-requested-key-refused", "negative",
         [exchange(TS, replace(TS_HAPPY, 9, **{"entries.0.key.subjectScopeCommitment": "sha256:" + "5f" * 32}))],
         refused("COVERAGE_KEY_CORRESPONDENCE", "Coverage", "0:subjectScopeCommitment")),
    case("ts2-frame-named-coverage-v3-faults", "negative",
         [exchange(TS, TS_PREFIX + TS_NCV + [F("Analyze"), F("CoverageV3", "$fixtures.startupTsCoverage")])],
         {"$r.finalPhase": "FAULT", "$r.refusal": None, "$r.hostConversion.stageAuthority.authority": "none"}),
    case("ts2-cancel-in-native-context-interval-observes-snapshot", "positive",
         [exchange(TS, TS_PREFIX + [F("Cancel"), F("Cancelled", {"executionId": EXEC, "analysisOrdinal": None, "observedPhase": "snapshot"}), F("eof")])],
         {"$r.finalPhase": "DONE", "$r.terminalKind": "cancelled", "$r.refusal": None}),
    case("ts2-cancel-after-native-context-verified-observes-snapshot", "positive",
         [exchange(TS, TS_PREFIX + TS_NCV + [F("Cancel"), F("Cancelled", {"executionId": EXEC, "analysisOrdinal": None, "observedPhase": "snapshot"}), F("eof")])],
         {"$r.finalPhase": "DONE", "$r.terminalKind": "cancelled", "$r.refusal": None}),
    case("ts2-cancel-in-native-context-interval-observing-analysis-refused", "negative",
         [exchange(TS, TS_PREFIX + [F("Cancel"), F("Cancelled", {"executionId": EXEC, "analysisOrdinal": None, "observedPhase": "analysis"})])],
         refused("CANCELLED_OBSERVED_PHASE", "Cancelled", "WAIT_NATIVE_CONTEXT_VERIFIED->analysis")),
    case("ts2-cancel-sent-twice-faults", "negative",
         [exchange(TS, TS_PREFIX + [F("Cancel"), F("Cancel")])],
         {"$r.finalPhase": "FAULT", "$r.refusal": None}),
    # ---- rust-semantic major 3
    case("rust3-empty-dependency-set-custody-then-complete", "positive", [exchange(RS, RS_HAPPY)],
         {"$r.finalPhase": "DONE", "$r.terminalKind": "complete", "$r.refusal": None, "$r.hostConversion": None,
          "$r.events.2": {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": False},
          "$r.trace": ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-07", "P3-08", "P3-11", "P3-13", "P3-15", "P3-20", "P3-22", "P3-24", "P3-27", "P3-31", "P3-32"]}),
    case("rust3-empty-dependency-manifest-and-seal-admit", "positive",
         [{"fn": "validate", "args": {"def": "DependencySourceManifestV3", "value": "$fixtures.startupRustEmptyDependencyManifest"}, "bind": "m"},
          {"fn": "validate", "args": {"def": "DependencySourceSealV3", "value": "$fixtures.startupRustEmptyDependencySeal"}, "bind": "s"}],
         {"$m.entries": [], "$s.totalChunkCount": 0}),
    case("rust3-skipping-empty-dependency-custody-faults", "negative",
         [exchange(RS, RS_PREFIX[:7] + [F("NativeContextVerified", "$fixtures.startupRustNativeContextVerified")])],
         {"$r.finalPhase": "FAULT", "$r.refusal": None,
          "$r.trace": ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-07", "P3-08", "P3-34"]}),
    case("rust3-prepared-universe-derives-prepared-mode", "positive",
         [{"fn": "protocol3_open_universe_event",
           "args": {"open_universe": "$fixtures.startupRustOpenUniversePrepared", "hello": "$fixtures.wireRustHello",
                    "hello_ack": "$fixtures.wireRustHelloAck", "expected": "$fixtures.startupRustInputs.universeExpected"},
           "bind": "e"}],
         {"$e": {"frame": "OpenUniverse", "dependencyMode": True, "preparedMode": True}}),
    case("rust3-prepared-authorization-not-the-selected-preparation-refused", "negative",
         [{"fn": "protocol3_open_universe_event",
           "args": {"open_universe": "$fixtures.startupRustOpenUniversePrepared", "hello": "$fixtures.wireRustHello",
                    "hello_ack": "$fixtures.wireRustHelloAck",
                    "expected": merge("$fixtures.startupRustInputs.universeExpected", **{"preparedAuthorization.authorizationId": "sha256:" + "4a" * 32})},
           "expectError": "REPOSITORY_RESOLUTION_JOIN:authorizationId", "bind": "e"}], {}),
    case("rust3-repository-resolution-dependency-set-mismatch-refused", "negative",
         [exchange(RS, replace(RS_HAPPY, 2, **{"repositoryResolution.dependencySourceSetId": "sha256:" + "4b" * 32}))],
         refused("REPOSITORY_RESOLUTION_JOIN", "OpenUniverse", "dependencySourceSetId")),
    case("rust3-open-universe-carrying-a-mode-boolean-refused", "negative",
         [exchange(RS, replace(RS_HAPPY, 2, dependencyMode=True))],
         refused("SCHEMA", "OpenUniverse", "OpenUniverseV3:/")),
    case("rust3-universe-not-the-hello-identity-refused", "negative",
         [exchange(RS, replace(RS_HAPPY, 2, **{"universe.sysrootDigest": "7c" * 32}))],
         refused("UNIVERSE_HANDSHAKE_JOIN", "OpenUniverse", "sysrootDigest")),
    case("rust3-open-universe-v1-snapshot-id-refused", "negative",
         [exchange(RS, replace(RS_HAPPY, 2, snapshotId="snap1:sha256:" + "5a" * 32))],
         refused("SCHEMA", "OpenUniverse", "OpenUniverseV3:/snapshotId")),
    case("rust3-open-universe-wrong-native-context-refused", "negative",
         [exchange(RS, RS_HAPPY, merge("$fixtures.startupRustInputs", **{"universeExpected.planNativeContextDigests": ["5e" * 32]}))],
         refused("NATIVE_CONTEXT_NOT_PLAN_BOUND", "OpenUniverse")),
    case("rust3-universe-accepted-partial-echo-refused", "negative",
         [exchange(RS, replace(RS_HAPPY, 3, **{"repositoryResolution.dependencySourceSetId": "sha256:" + "4b" * 32}))],
         refused("UNIVERSE_ACCEPTED_ECHO", "UniverseAccepted", "repositoryResolution")),
    case("rust3-pre-analyze-unavailable-host-derives-provider-unavailable-coverage", "positive", [exchange(RS, RS_PRE)],
         {"$r.finalPhase": "DONE", "$r.terminalKind": "unavailable", "$r.refusal": None,
          "$r.trace": ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-07", "P3-08", "P3-11", "P3-13", "P3-15", "P3-21", "P3-31", "P3-32"],
          "$r.hostConversion.allAdmitted": True, "$r.hostConversion.affectedStageIds": ["s-refs"],
          "$r.hostConversion.termination.d9.code": "COVERAGE.PROVIDER_UNAVAILABLE"}),
    case("rust3-post-analyze-payload-in-native-context-phase-refused", "negative",
         [exchange(RS, RS_PREFIX + [F("Unavailable", "$fixtures.startupRustPostAnalyzeUnavailable")])],
         refused("UNAVAILABLE_PHASE_PAYLOAD", "Unavailable")),
    case("rust3-post-analyze-reason-native-context-mismatch-refused", "negative",
         [exchange(RS, RS_HAPPY[:12] + [F("Unavailable", merge("$fixtures.startupRustPostAnalyzeUnavailable", reason="native-context-mismatch"))])],
         refused("UNAVAILABLE_PHASE_PAYLOAD", "Unavailable")),
    case("rust3-post-analyze-typescript-only-reason-refused", "negative",
         [exchange(RS, RS_HAPPY[:12] + [F("Unavailable", merge("$fixtures.startupRustPostAnalyzeUnavailable", reason="node-modules-outside-read-set"))])],
         refused("SCHEMA", "Unavailable", "UnavailableV3:/reason")),
    case("rust3-post-analyze-unavailable-lawful", "positive",
         [exchange(RS, RS_HAPPY[:12] + [F("Unavailable", "$fixtures.startupRustPostAnalyzeUnavailable"), F("zero-exit"), F("eof")])],
         {"$r.finalPhase": "DONE", "$r.terminalKind": "unavailable", "$r.hostConversion": None, "$r.refusal": None}),
    case("rust3-frame-named-coverage-faults", "negative",
         [exchange(RS, RS_HAPPY[:12] + [F("Coverage", "$fixtures.startupRustCoverage")])],
         {"$r.finalPhase": "FAULT", "$r.refusal": None, "$r.hostConversion.stageAuthority.authority": "none"}),
    case("rust3-coverage-v3-with-result-v1-entry-refused", "negative",
         [exchange(RS, replace(RS_HAPPY, 12, entries=["$fixtures.startupTsCoverageResultV1Entry"]))],
         refused("SCHEMA", "CoverageV3", "CoverageV3:/entries/0")),
    case("rust3-event-only-trace-without-booleans-stays-an-abstract-table-test", "positive",
         [{"fn": "protocol3_run", "args": {"events": [{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": "$fixtures.rust3"},
                                                     {"frame": "OpenUniverse"}, {"frame": "UniverseAccepted"},
                                                     {"frame": "SnapshotManifest"}, {"frame": "SnapshotSeal"},
                                                     {"frame": "SnapshotAccepted"}]}, "bind": "r"}],
         {"$r.trace": ["P3-01", "P3-02", "P3-03", "P3-04", "P3-05", "P3-07", "P3-10"]}),
]


def indent_block(text, prefix):
    lines = text.split("\n")
    return "\n".join([lines[0]] + [prefix + line for line in lines[1:]])


raw = raw_before.decode("utf-8")
fixture_anchor = "\n },\n \"cases\": [\n"
case_anchor = "\n ],\n \"revision\":"
assert raw.count(fixture_anchor) == 1 and raw.count(case_anchor) == 1
fixture_text = "".join(",\n  " + json.dumps(k) + ": " + indent_block(json.dumps(v, indent=1), "  ") for k, v in new_fixtures.items())
case_text = "".join(",\n  " + indent_block(json.dumps(c, indent=1), "  ") for c in cases)
raw = raw.replace(fixture_anchor, fixture_text + fixture_anchor, 1)
raw = raw.replace(case_anchor, case_text + case_anchor, 1)
updated = json.loads(raw)
assert updated["cases"][:len(original["cases"])] == original["cases"]
assert {k: updated["fixtures"][k] for k in original["fixtures"]} == original["fixtures"]
assert len({c["id"] for c in updated["cases"]}) == len(updated["cases"])
CASES.write_bytes(raw.encode("utf-8"))
print(json.dumps({"addedFixtures": len(new_fixtures), "addedCases": len(cases), "totalCases": len(updated["cases"]),
                  "tsUniverseKey": ts_key, "rustUniverse": rust_hex,
                  "sha256Before": hashlib.sha256(raw_before).hexdigest(), "sha256After": hashlib.sha256(raw.encode("utf-8")).hexdigest()}))
