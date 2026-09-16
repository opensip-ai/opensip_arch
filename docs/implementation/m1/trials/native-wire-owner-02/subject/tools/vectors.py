#!/usr/bin/env python3
"""Emit admission-vectors.json: id-bound accept/refuse vectors for handwritten admission rules.

Markers expanded by check_reference.py: {"$bytesHex": hex}, {"$repeat": {"n": N, "item": X}} (list of N shared items),
{"$concat": [list, ...]} (concatenated lists), {"$fixture": key} (native-cases.v2.json fixtures), {"$scopeDescriptor": {...overrides}} (fixture descriptor with
overrides, commitment computed by the pinned owner model), {"$ownerCommit": {...}} (commitment computed from owner
recipe text, never from the carrier map).

    PYTHONDONTWRITEBYTECODE=1 python3 -B tools/vectors.py
"""
import hashlib
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent
H = "0" * 64
SNAP = "snapshot2:" + "a" * 64
PLAN = "plan2:" + "b" * 64
EXEC = "exec1_" + "0" * 32
BYTES = lambda b: {"$bytesHex": b.hex()}
REP = lambda n, item: {"$repeat": {"n": n, "item": item}}


def v(id_, kind, input_, expect=None):
    return {"id": id_, "kind": kind, "input": input_, "expect": expect}


def sha(b):
    return hashlib.sha256(b).hexdigest()


VECTORS = {}

VECTORS["CANONICAL-PATH-ADMISSION"] = [v("canon-" + str(i), "accept", {"path": p}) for i, p in enumerate(["a/b", "a\nb", "b/C:x", "src/lib.rs", "a" * 4096])] + \
    [v("canon-refuse-" + str(i), "refuse", {"path": p}, "PATH_LEXICAL") for i, p in enumerate(
        ["a\n/../b", "a\n//b", "x\n/..", "a\n/.", "a//b", "a/", "C:x", "c:/x", "./a", "/a", "a\\b", "a\u0000b", "", ".", ".."])]
VECTORS["TS2-LOGICAL-PATH-ADMISSION"] = [v("logical-" + str(i), "accept", {"path": p}) for i, p in enumerate(["src/a.ts", "a\nb", "C:x", "x" * 255 + "/y"])] + \
    [v("logical-refuse-" + str(i), "refuse", {"path": p}, "PATH_LEXICAL") for i, p in enumerate(
        ["a/../b", "a\n/../b", "a//b", "x" * 256, "/a", "a\\b", "a/", "."])]

PKG = [{"name": "serde", "version": "1.0.200", "sourceId": "registry+https://github.com/rust-lang/crates.io-index", "fileCount": 1, "totalBytes": 3, "fileManifestSha256": H},
       {"name": "my-proj", "version": "0.1.0", "sourceId": "path+file:///my proj", "fileCount": 1, "totalBytes": 3, "fileManifestSha256": H},
       {"name": "p", "version": "1", "sourceId": "", "fileCount": 1, "totalBytes": 3, "fileManifestSha256": H}]
VECTORS["PACKAGE-KEY-JOIN"] = [
    v("key-registry", "accept", {"packages": PKG, "key": "serde 1.0.200 registry+https://github.com/rust-lang/crates.io-index"}),
    v("key-sourceid-with-space", "accept", {"packages": PKG, "key": "my-proj 0.1.0 path+file:///my proj"}),
    v("key-empty-sourceid", "accept", {"packages": PKG, "key": "p 1 "}),
    v("key-dash-form", "refuse", {"packages": PKG, "key": "serde-1.0.200"}, "PACKAGE_KEY_JOIN"),
    v("key-trailing-space-missing", "refuse", {"packages": PKG, "key": "p 1"}, "PACKAGE_KEY_JOIN"),
    v("key-unknown-package", "refuse", {"packages": PKG, "key": "serde 1.0.201 registry+https://github.com/rust-lang/crates.io-index"}, "PACKAGE_KEY_JOIN"),
]
LONG_OK = [{"name": "a" * 256, "version": "b" * 256, "sourceId": "c" * 3582}]
LONG_BAD = [{"name": "a" * 256, "version": "b" * 256, "sourceId": "c" * 3583}]
DETAIL_KEY = "REQUEST.PRECONDITION_FAILED:native.dependency-source-package-key-invalid"
VECTORS["DEPSRC-SET-KEY-CONSTRAINTS"] = [
    v("set-cargo-names", "accept", {"packages": PKG}),
    v("set-key-4096-scalars", "accept", {"packages": LONG_OK}),
    v("set-key-4097-scalars", "refuse", {"packages": LONG_BAD}, DETAIL_KEY),
    v("set-name-control-byte", "refuse", {"packages": [{"name": "a\u0001", "version": "1", "sourceId": "x"}]}, DETAIL_KEY),
    v("set-name-space", "refuse", {"packages": [{"name": "a b", "version": "1", "sourceId": "x"}]}, DETAIL_KEY),
    v("set-version-space-0x20", "refuse", {"packages": [{"name": "a", "version": "1 2", "sourceId": "x"}]}, DETAIL_KEY),
]

A_ROW = {"name": "a", "version": "1.0.0", "sourceId": "registry+x", "fileCount": 1, "totalBytes": 3, "fileManifestSha256": H}
B_ROW = {"name": "a-b", "version": "1.0.0", "sourceId": "registry+x", "fileCount": 1, "totalBytes": 3, "fileManifestSha256": H}
E_A = {"packageKey": "a 1.0.0 registry+x", "path": "z.rs", "byteLength": 3, "contentSha256": H}
E_B = {"packageKey": "a-b 1.0.0 registry+x", "path": "a.rs", "byteLength": 3, "contentSha256": H}


def manifest(entries):
    from wirecodec import encode
    return {"dependencySourceSetId": "sha256:" + H, "manifestSha256": sha(encode(entries)), "entries": entries}


def build_depsrc():
    ok = manifest([E_A, E_B])
    return [
        v("depsrc-tuple-order", "accept", {"packages": [A_ROW, B_ROW], "manifest": ok}),
        v("depsrc-path-first-order", "refuse", {"packages": [A_ROW, B_ROW], "manifest": manifest([E_B, E_A])}, "DEPSRC_ORDER"),
        v("depsrc-missing-package", "refuse", {"packages": [A_ROW, B_ROW], "manifest": manifest([E_A])}, "DEPSRC_PACKAGE_MISSING"),
        v("depsrc-count-mismatch", "refuse", {"packages": [dict(A_ROW, fileCount=2), B_ROW], "manifest": ok}, "DEPSRC_FILE_COUNTS"),
        v("depsrc-digest-mismatch", "refuse", {"packages": [A_ROW, B_ROW], "manifest": dict(ok, manifestSha256=H)}, "MANIFEST_DIGEST"),
        v("depsrc-path-newline-dotdot", "refuse", {"packages": [A_ROW], "manifest": manifest([dict(E_A, path="x\n/../y")])}, "PATH_LEXICAL"),
        v("depsrc-key-not-joined", "refuse", {"packages": [A_ROW], "manifest": manifest([dict(E_A, packageKey="a-1.0.0-registry+x")])}, "PACKAGE_KEY_JOIN"),
        v("depsrc-empty-set", "accept", {"packages": [], "manifest": {"dependencySourceSetId": "sha256:" + H, "manifestSha256": sha(b"\x80"), "entries": []}}),
        v("depsrc-empty-set-wrong-digest", "refuse", {"packages": [], "manifest": {"dependencySourceSetId": "sha256:" + H, "manifestSha256": H, "entries": []}}, "DEPSRC_EMPTY_SET"),
    ]


def prow(kind, size=3, config=None):
    blob = {"sha256": H, "byteLength": size, "mediaType": {"build-script-directives": "text/x-cargo-directives", "macro-expansion": "text/x-rust-expansion", "generated-file": "text/plain"}[kind]}
    return {"kind": kind, "ownerKey": "o", "configuration": config if config is not None else [], "site": None,
            "generated": {"logicalPath": "g.rs", "blob": blob} if kind == "generated-file" else None,
            "inputBinding": {"ownerFileManifestSha256": H, "dependencySourceSetId": "sha256:" + H, "toolchainDigest": H, "cfgSetId": "primary"},
            "blob": blob, "status": "ok", "failureDetail": None}


DETAIL_PREP = "REQUEST.PRECONDITION_FAILED:native.prepared-output-exceeds-wire-limit"
VECTORS["PREPARED-V3-WIRE-LIMIT"] = [
    v("prepared-256-rows", "accept", {"set": {"rows": REP(256, prow("macro-expansion"))}}),
    v("prepared-257-rows-mixed-kinds", "refuse", {"set": {"rows": {"$concat": [[prow("build-script-directives")], REP(256, prow("macro-expansion"))]}}}, DETAIL_PREP + ":entries"),
    v("prepared-blob-bytes-over", "refuse", {"set": {"rows": [prow("generated-file", 1073741824), prow("macro-expansion", 1)]}}, DETAIL_PREP + ":blob-bytes"),
    v("prepared-blob-bytes-at-limit", "accept", {"set": {"rows": [prow("generated-file", 1073741823), prow("macro-expansion", 1)]}}),
    v("prepared-manifest-over-frame", "refuse", {"set": {"rows": REP(256, prow("macro-expansion", 3, REP(1024, "c" * 256)))}}, DETAIL_PREP + ":manifest-bytes"),
    v("prepared-manifest-under-frame", "accept", {"set": {"rows": REP(256, prow("macro-expansion", 3, REP(1000, "c" * 256)))}}),
]
VECTORS["PREPARED-V3-ENTRY"] = [
    v("prepared-entries-from-fixture", "accept", {"setFixture": "prepGenerated"}),
    v("prepared-entry-content-differs", "refuse", {"setFixture": "prepGenerated", "mutate": {"entry": 0, "contentSha256": "f" * 64}}, "PREPARED_ENTRY_JOIN"),
    v("prepared-generated-blob-mismatch", "refuse", {"setFixture": "prepGenerated", "mutate": {"generatedBlobSha256": "e" * 64}}, "PREPARED_GENERATED_BLOB"),
]

CAPS = ["coverage-v3", "fact-identity-fact2", "plan-identity-plan2", "source-identity-snapshot2"]
BASE = [{"frame": "Hello"}, {"frame": "HelloAck", "capabilities": CAPS},
        {"frame": "OpenUniverse", "payload": {"executionId": EXEC}, "dependencyMode": True, "preparedMode": False}]
AFTER_UA = BASE + [{"frame": "UniverseAccepted"}, {"frame": "SnapshotManifest"}]
TO_ANALYZE = BASE + [{"frame": "UniverseAccepted"}, {"frame": "SnapshotManifest"}, {"frame": "SnapshotSeal"}, {"frame": "SnapshotAccepted"},
                     {"frame": "DependencySourceManifest"}, {"frame": "DependencySourceSeal"}, {"frame": "DependencySourceAccepted"},
                     {"frame": "NativeContextVerified"}, {"frame": "Analyze", "payload": {"analysisOrdinal": 0}}]
F = lambda phase, e, a: {"executionId": e, "analysisOrdinal": a, "phase": phase, "faultKind": "compiler-crash", "detailCode": "x"}
VECTORS["RUST3-PROVIDER-FAULT"] = [
    v("fault-inflight-snapshot-manifest-unread", "accept", {"events": AFTER_UA, "fault": F("READY_SNAPSHOT_MANIFEST", EXEC, None)}),
    v("fault-inflight-snapshot-manifest-read", "accept", {"events": AFTER_UA, "fault": F("RECEIVING_SNAPSHOT", EXEC, None)}),
    v("fault-phase-before-provably-read-openuniverse", "refuse", {"events": AFTER_UA, "fault": F("READY_OPEN_UNIVERSE", None, None)}, "PROVIDER_FAULT_OBSERVATION"),
    v("fault-null-execution-after-universe-accepted", "refuse", {"events": AFTER_UA, "fault": F("READY_SNAPSHOT_MANIFEST", None, None)}, "PROVIDER_FAULT_OBSERVATION"),
    v("fault-inflight-analyze-unread", "accept", {"events": TO_ANALYZE, "fault": F("READY_ANALYZE", EXEC, None)}),
    v("fault-inflight-analyze-read", "accept", {"events": TO_ANALYZE, "fault": F("ANALYZING", EXEC, 0)}),
    v("fault-analyzing-without-ordinal", "refuse", {"events": TO_ANALYZE, "fault": F("ANALYZING", EXEC, None)}, "PROVIDER_FAULT_OBSERVATION"),
    v("fault-ready-analyze-with-ordinal", "refuse", {"events": TO_ANALYZE, "fault": F("READY_ANALYZE", EXEC, 0)}, "PROVIDER_FAULT_OBSERVATION"),
    v("fault-inflight-openuniverse-unread-null", "accept", {"events": BASE, "fault": F("READY_OPEN_UNIVERSE", None, None)}),
    v("fault-inflight-openuniverse-read-echo", "accept", {"events": BASE, "fault": F("WAIT_UNIVERSE_ACCEPTED", EXEC, None)}),
    v("fault-inflight-openuniverse-read-null", "refuse", {"events": BASE, "fault": F("WAIT_UNIVERSE_ACCEPTED", None, None)}, "PROVIDER_FAULT_OBSERVATION"),
    v("fault-wait-hello-ack", "accept", {"events": [{"frame": "Hello"}], "fault": F("WAIT_HELLO_ACK", None, None)}),
    v("fault-before-hello", "refuse", {"events": [], "fault": F("WAIT_HELLO_ACK", None, None)}, "PROVIDER_FAULT_BEFORE_HELLO"),
]

VECTORS["P3-OVERLAY"] = [
    v("overlay-factbatch-then-unavailable", "refuse", {"events": TO_ANALYZE + [{"frame": "FactBatch"}, {"frame": "Unavailable"}], "stageCount": 1}, "P3-34"),
    v("overlay-coverage-then-unavailable", "refuse", {"events": TO_ANALYZE + [{"frame": "CoverageV3"}, {"frame": "Unavailable"}], "stageCount": 2}, "P3-34"),
    v("overlay-unavailable-before-output", "accept", {"events": TO_ANALYZE + [{"frame": "Unavailable"}, {"frame": "zero-exit"}, {"frame": "eof"}], "stageCount": 1, "tail": "P3-25"}),
    v("overlay-cancel-in-start", "refuse", {"events": [{"frame": "Cancel"}], "stageCount": 1}, "P3-34"),
    v("overlay-cancel-after-hello", "accept", {"events": [{"frame": "Hello"}, {"frame": "Cancel"}], "stageCount": 1, "tail": "P3-29"}),
]

TWO_STAGES = [[{"k": "s1e0"}, {"k": "s1e1"}], [{"k": "s2e0"}]]
VECTORS["COMMIT-MAP"] = []
for field, owner in [("Startup1UnavailableV3.coverageCommitment", {"doc": "rust2", "recipe": "coverageStream", "value": "stage-major"}),
                     ("Startup1BudgetExhaustedV3.coverageCommitment", {"doc": "rust2", "recipe": "coverageStream", "value": "stage-major"}),
                     ("Rust3CompleteV2.coverageStreamCommitment", {"doc": "rust2", "recipe": "coverageStream", "value": "stage-major"}),
                     ("Startup1CoverageV3.coverageCommitment", {"doc": "rust2", "recipe": "stageCoverage", "value": "stage"}),
                     ("Rust3StageResultV2.coverageCommitment", {"doc": "rust2", "recipe": "stageCoverage", "value": "stage"}),
                     ("Startup1TypeScriptUnavailableV2.coverageCommitment", {"doc": "delivery2", "recipe": "coverageStream", "value": "stage-major"}),
                     ("Startup1TypeScriptCoverageV2.coverageCommitment", {"doc": "delivery2", "recipe": "stageCoverage", "value": "stage"})]:
    other = dict(owner, recipe="stageCoverage" if owner["recipe"] == "coverageStream" else "coverageStream",
                 value="stage" if owner["value"] == "stage-major" else "stage-major")
    VECTORS["COMMIT-MAP"].append(v("commit-" + field, "accept", {"field": field, "stages": TWO_STAGES, "commitment": {"$ownerCommit": owner}}))
    VECTORS["COMMIT-MAP"].append(v("commit-wrong-domain-" + field, "refuse", {"field": field, "stages": TWO_STAGES, "commitment": {"$ownerCommit": other}}, "COMMIT_MISMATCH"))

SPAN = {"kind": "source-span", "snapshotId": SNAP, "path": "src/a.rs", "contentSha256": "1" * 64, "startByte": 0, "endByte": 1, "factId": None}
A1 = dict(SPAN, path="b", contentSha256="f" * 64)
A2 = dict(SPAN, path="aa", contentSha256="0" * 64)
MAN = {"src/a.rs": {"kind": "file", "byteLength": 10, "contentSha256": "1" * 64},
       "b": {"kind": "file", "byteLength": 1, "contentSha256": "f" * 64}, "aa": {"kind": "file", "byteLength": 1, "contentSha256": "0" * 64}}
VECTORS["ANCHOR-WIRE-SPAN"] = [
    v("anchor-ts2-cbor-order", "accept", {"language": "typescript-semantic", "anchors": [A1, A2], "manifest": MAN}),
    v("anchor-rust3-cve1-order", "accept", {"language": "rust-semantic", "anchors": [A2, A1], "manifest": MAN}),
    v("anchor-ts2-cve1-order-refused", "refuse", {"language": "typescript-semantic", "anchors": [A2, A1], "manifest": MAN}, "ANCHOR_ORDER"),
    v("anchor-rust3-cbor-order-refused", "refuse", {"language": "rust-semantic", "anchors": [A1, A2], "manifest": MAN}, "ANCHOR_ORDER"),
    v("anchor-empty-interval", "refuse", {"language": "rust-semantic", "anchors": [dict(SPAN, endByte=0)], "manifest": MAN}, "ANCHOR_EMPTY_OR_OUT_OF_BOUNDS"),
    v("anchor-out-of-bounds", "refuse", {"language": "typescript-semantic", "anchors": [dict(SPAN, endByte=11)], "manifest": MAN}, "ANCHOR_EMPTY_OR_OUT_OF_BOUNDS"),
    v("anchor-digest-join", "refuse", {"language": "typescript-semantic", "anchors": [dict(SPAN, contentSha256="2" * 64)], "manifest": MAN}, "ANCHOR_SOURCE_JOIN"),
    v("anchor-count-100001", "refuse", {"language": "rust-semantic", "anchors": REP(100001, SPAN), "manifest": MAN}, "ANCHOR_COUNT"),
    v("anchor-path-lexical", "refuse", {"language": "rust-semantic", "anchors": [dict(SPAN, path="src//a.rs")], "manifest": MAN}, "PATH_LEXICAL"),
]
VECTORS["ANCHOR-FACT-REF-REFUSED"] = [
    v("anchor-source-span", "accept", {"language": "typescript-semantic", "anchors": [SPAN], "manifest": MAN}),
    v("anchor-fact-ref", "refuse", {"language": "rust-semantic", "anchors": [{"kind": "fact-ref", "snapshotId": None, "path": None, "contentSha256": None, "startByte": None, "endByte": None, "factId": "fact1:x"}], "manifest": MAN}, "ANCHOR_FACT_REF_UNDER_FACT2"),
]

ENTRIES = [{"path": "src/a.ts", "kind": "file", "byteLength": 3, "contentSha256": sha(b"abc"), "linkTarget": None}]
for rid in ("TS2-MANIFEST-DIGEST", "RAW-MANIFEST-DIGEST"):
    from wirecodec import encode as _enc
    VECTORS[rid] = [v(rid.lower() + "-raw", "accept", {"manifest": {"manifestSha256": sha(_enc(ENTRIES)), "entries": ENTRIES}}),
                    v(rid.lower() + "-domain-form", "refuse", {"manifest": {"manifestSha256": "sha256:" + sha(_enc(ENTRIES)), "entries": ENTRIES}}, "MANIFEST_DIGEST")]
SEAL = {"snapshotId": SNAP, "manifestSha256": H, "entryCount": 1, "totalFileBytes": 3, "totalChunkCount": 1}
VECTORS["ACCEPTED-EQUALS-SEAL"] = [v("accepted-echo", "accept", {"seal": SEAL, "accepted": SEAL}),
                                   v("accepted-differs", "refuse", {"seal": SEAL, "accepted": dict(SEAL, totalChunkCount=2)}, "ACCEPTED_NOT_SEAL")]
ENTRY = ENTRIES[0]
CH = lambda i, off, b: {"path": "src/a.ts", "chunkIndex": i, "byteOffset": off, "bytes": BYTES(b)}
VECTORS["CHUNK-CUSTODY"] = [v("chunks-two", "accept", {"entry": ENTRY, "chunks": [CH(0, 0, b"ab"), CH(1, 2, b"c")]}),
                            v("chunks-gap-offset", "refuse", {"entry": ENTRY, "chunks": [CH(0, 0, b"ab"), CH(1, 1, b"c")]}, "CHUNK_ORDER"),
                            v("chunks-wrong-bytes", "refuse", {"entry": ENTRY, "chunks": [CH(0, 0, b"abd")]}, "CHUNK_DIGEST_OR_LENGTH"),
                            v("chunks-for-empty-entry", "refuse", {"entry": dict(ENTRY, byteLength=0), "chunks": [CH(0, 0, b"a")]}, "CHUNK_FOR_EMPTY_ENTRY")]
VECTORS["SEAL-AGGREGATES"] = [v("seal-ok", "accept", {"entries": ENTRIES, "chunkCount": 1, "seal": SEAL, "total": "totalFileBytes"}),
                              v("seal-bytes-wrong", "refuse", {"entries": ENTRIES, "chunkCount": 1, "seal": dict(SEAL, totalFileBytes=4), "total": "totalFileBytes"}, "SEAL_AGGREGATES")]
OU = {"frame": "OpenUniverse", "payload": {"executionId": EXEC}}
AN = {"frame": "Analyze", "payload": {"analysisOrdinal": 0}}
VECTORS["CANCEL-NULLABILITY"] = [v("cancel-before-open", "accept", {"sent": [{"frame": "Hello"}], "cancel": {"executionId": None, "analysisOrdinal": None}}),
                                 v("cancel-after-analyze", "accept", {"sent": [OU, AN], "cancel": {"executionId": EXEC, "analysisOrdinal": 0}}),
                                 v("cancel-open-sent-null", "refuse", {"sent": [OU], "cancel": {"executionId": None, "analysisOrdinal": None}}, "CANCEL_EXECUTION_ID")]
CAN = {"executionId": EXEC, "analysisOrdinal": None}
VECTORS["CANCELLED-ECHO"] = [v("cancelled-echo", "accept", {"cancel": CAN, "cancelled": dict(CAN, observedPhase="READY_ANALYZE")}),
                             v("cancelled-differs", "refuse", {"cancel": CAN, "cancelled": dict(CAN, executionId=None, observedPhase="READY_ANALYZE")}, "CANCELLED_ECHO")]
VECTORS["RUST3-CANCEL-TYPES"] = [v("cancelled-send-phase", "accept", {"cancel": CAN, "cancelled": dict(CAN, observedPhase="RECEIVING_SNAPSHOT"), "hostSendPhase": "RECEIVING_SNAPSHOT"}),
                                 v("cancelled-other-phase", "refuse", {"cancel": CAN, "cancelled": dict(CAN, observedPhase="WAIT_SNAPSHOT_ACCEPTED"), "hostSendPhase": "RECEIVING_SNAPSHOT"}, "CANCELLED_OBSERVED_PHASE")]
BE = {"unit": "work-units", "limit": 7, "observed": 8}
VECTORS["RUST3-BUDGET-EXHAUSTED"] = [v("budget-limit-plus-one", "accept", {"payload": BE, "planBudget": {"unit": "work-units", "limit": 7}}),
                                     v("budget-observed-equal-limit", "refuse", {"payload": dict(BE, observed=7), "planBudget": {"unit": "work-units", "limit": 7}}, "BUDGET_OBSERVED"),
                                     v("budget-no-plan-budget", "refuse", {"payload": BE, "planBudget": None}, "BUDGET_NOT_EXHAUSTIBLE"),
                                     v("budget-milliseconds", "refuse", {"payload": dict(BE, unit="milliseconds"), "planBudget": {"unit": "milliseconds", "limit": 7}}, "BUDGET_NOT_EXHAUSTIBLE")]
TU = "sha256:" + "1" * 64
VECTORS["OCCUPANCY-JOIN"] = [v("occupancy-join", "accept", {"batch": {"candidates": [{"candidateOrdinal": 0, "targetUniverseId": TU}, {"candidateOrdinal": 1, "targetUniverseId": TU}], "occupancyCompanions": [{"candidateOrdinal": 1, "targetUniverseId": TU}]}}),
                             v("occupancy-unknown-ordinal", "refuse", {"batch": {"candidates": [{"candidateOrdinal": 0, "targetUniverseId": TU}], "occupancyCompanions": [{"candidateOrdinal": 5, "targetUniverseId": TU}]}}, "OCCUPANCY_JOIN"),
                             v("occupancy-target-differs", "refuse", {"batch": {"candidates": [{"candidateOrdinal": 0, "targetUniverseId": TU}], "occupancyCompanions": [{"candidateOrdinal": 0, "targetUniverseId": "sha256:" + "2" * 64}]}}, "OCCUPANCY_JOIN")]
VECTORS["PER-KEY-SCOPE2"] = [
    v("scope2-key-own-descriptor", "accept", {"descriptor": {"$scopeDescriptor": {}}, "commitmentOf": {"$scopeDescriptor": {}}}),
    v("scope2-other-rung", "refuse", {"descriptor": {"$scopeDescriptor": {}}, "commitmentOf": {"$scopeDescriptor": {"resolution": "syntactic-name-match"}}}, "SCOPE2_MISMATCH"),
    v("scope2-other-target", "refuse", {"descriptor": {"$scopeDescriptor": {}}, "commitmentOf": {"$scopeDescriptor": {"targetUniverse": "f" * 64}}}, "SCOPE2_MISMATCH"),
    v("scope2-other-enumerator", "refuse", {"descriptor": {"$scopeDescriptor": {}}, "commitmentOf": {"$scopeDescriptor": {"enumeratorClosure": "closure2:" + "9" * 64}}}, "SCOPE2_MISMATCH"),
    v("scope2-inherited-ts-per-stage", "refuse", {"descriptor": {"$scopeDescriptor": {}}, "commitment": {"$inheritedTsPerStage": True}}, "SCOPE2_MISMATCH"),
]

EXEMPT = {
    "FRAME-LIMIT": "carrier bounds executed by wire examples (wire-bytes-empty, json-schema-maxlength-not-byte-bound) and codec length checks",
    "TS2-ENV-MAJOR": "wire-ts2-envelope-major-refused", "TS2-ENV-DIRECTION-BY-FRAME": "ts2-frame-set", "TS2-ENV-SEQUENCE": "inherited delivery2 law, M2 implementation; no new semantics authored",
    "RUST3-FRAME-PRECHECK": "wire-rust3-envelope and rust3-frame-directions-terminals; retained rust2 framePrecheck, M2 implementation",
    "ECHO-SNAPSHOT2": "echo-rules-present and manifest/seal vectors", "ECHO-PLAN2": "echo-rules-present", "ECHO-OPEN-UNIVERSE": "echo-rules-present",
    "TS2-SNAPSHOT-ORDER": "inherited delivery2 order; M2 implementation", "RUST3-SNAPSHOT-ENTRY-TYPES": "wire-rust3-snapshot-variants",
    "PREPARED-V3-SET-JOIN": "prepared-v3-set-identity-join executes native_evidence_model.v2 prepared_output_set_identity",
    "TS2-BUDGET-PROJECTION": "inherited delivery2 projection; M2", "TS2-STAGE-PROJECTION": "inherited delivery2 projection; M2",
    "DISPATCH-STAGE-CORRELATION": "commit-ts2-fact-batch-matches-wire-model executes provider_wire_model admit_fact_batch; dispatch correlation is M2",
    "TS2-SUBJECT-SCOPE-RETAINED": "retained inherited recipe; M2", "TS2-DOMAIN-COMMITMENT": "retained inherited recipe; M2", "RUST3-DOMAIN-COMMITMENT": "retained inherited recipe; M2",
    "RUST3-SUBJECTS": "retained inherited algorithm; M2", "RUST3-PLAN-STAGE-BYTES": "retained inherited rule; M2",
    "UNIVERSE-NATIVE-IDENTITY": "scope2-ts2-admits/scope2-rust3-admits execute provider_startup_model admit_coverage_frame suffix joins",
    "FP-CANDIDATE": "retained fact-plane law; M2", "RELATION-PAYLOAD-CBOR": "commit-ts2-fact-batch-matches-wire-model (CBOR projection)",
    "RUST3-SPOOL": "retained rust2 limitPolicy; M2", "COMMIT-TS2-FACT-BATCH": "commit-ts2-fact-batch-matches-wire-model",
    "TS2-OBSERVED-PHASE": "retained startup cancellation law executed by provider_startup_model cancelled_observed_phase; M2",
}

if __name__ == "__main__":
    VECTORS["DEPSRC-CUSTODY"] = build_depsrc()
    doc = {"artifact": "opensip.m1.native-wire-admission-vectors", "version": "1",
           "standing": "AUTHOR candidate 02 reference vectors for handwritten admission rules; executed by check.py against tools/admission_ref.py and wire-carriers.v1.json params; not admission code.",
           "vectors": VECTORS, "exempt": EXEMPT}
    (OUT / "admission-vectors.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print({k: len(x) for k, x in VECTORS.items()})
