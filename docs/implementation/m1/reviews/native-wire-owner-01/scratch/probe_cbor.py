"""Independent probes of the declared CBOR grammar and carrier typing, using the frozen scaffolding codec from the
scratch copy (run1). Hand-built byte strings, not the author's vectors."""
import json, sys
sys.path.insert(0, "/tmp/opensip-implementation/m1-native-wire-owner-review-01/scratch/run1/tools")
import wirecodec as W

IDL = json.load(open("/tmp/opensip-implementation/m1-native-wire-owner-review-01/scratch/run1/wire-carriers.v1.json"))
C = W.Carriers(IDL, lambda gt, v, where: None)
res = {}


def dec(name, hexs, profile):
    try:
        v = W.decode(bytes.fromhex(hexs), profile)
        res[profile + ":" + name] = {"decoded": repr(v)[:80]}
    except W.Refuse as e:
        res[profile + ":" + name] = {"refused": e.code}


for prof in ("ts2-cbor", "rust3-cbor"):
    dec("uint64-max", "1bffffffffffffffff", prof)
    dec("neg-minus1", "20", prof)
    dec("neg-minus-2^63", "3b7fffffffffffffff", prof)
    dec("neg-below-minus-2^63", "3b8000000000000000", prof)
    dec("undefined-f7", "f7", prof)
    dec("simple-f8-20", "f814", prof)
    dec("half-float", "f90000", prof)
    dec("bytes-nonshortest-len", "580161", prof)
    dec("bytes-indefinite", "5f4161ff", prof)
    dec("map-bytes-key", "a14161 01".replace(" ", ""), prof)
    dec("map-len-first-vs-bytewise", "a2616201626161 02".replace(" ", ""), prof)  # {"b":1,"aa":2}
    dec("empty-bytes", "40", prof)
    dec("tag-bignum", "c249010000000000000000", prof)


def carrier(name, protocol, frame, value, selector=None):
    try:
        C.frame_payload(protocol, frame, value, selector)
        res[name] = "admitted-by-carrier"
    except W.Refuse as e:
        res[name] = "refused:" + e.code


h64 = "0" * 64
carrier("ts2-cancel-analysisOrdinal-1", "typescript-semantic", "Cancel", {"executionId": None, "analysisOrdinal": 1, "reason": "user-interrupt"})
carrier("ts2-cancel-negative-analysisOrdinal", "typescript-semantic", "Cancel", {"executionId": None, "analysisOrdinal": -1, "reason": "user-interrupt"})
carrier("ts2-cancel-exec-uppercase-hex", "typescript-semantic", "Cancel", {"executionId": "exec1_" + "A" * 32, "analysisOrdinal": None, "reason": "user-interrupt"})
carrier("rust3-fault-START-phase", "rust-semantic", "ProviderFault", {"executionId": None, "analysisOrdinal": None, "phase": "START", "faultKind": "compiler-crash", "detailCode": "x"})
carrier("rust3-fault-WAIT_CANCELLED-phase", "rust-semantic", "ProviderFault", {"executionId": None, "analysisOrdinal": None, "phase": "WAIT_CANCELLED", "faultKind": "compiler-crash", "detailCode": "x"})
carrier("rust3-fault-detailCode-4097-bytes", "rust-semantic", "ProviderFault", {"executionId": None, "analysisOrdinal": None, "phase": "ANALYZING", "faultKind": "compiler-crash", "detailCode": "é" * 2049})
carrier("rust3-depsrc-chunk-empty-sourceId-key", "rust-semantic", "DependencySourceChunk",
        {"dependencySourceSetId": "sha256:" + h64, "packageKey": "a 1 ", "path": "src/lib.rs", "chunkIndex": 0, "byteOffset": 0, "bytes": b"x"})
chunk = {"dependencySourceSetId": "sha256:" + h64, "packageKey": "serde 1.0.0 registry+x", "path": "src/lib.rs", "chunkIndex": 0, "byteOffset": 0, "bytes": b"x"}
carrier("rust3-depsrc-chunk-empty-sourceId-key", "rust-semantic", "DependencySourceChunk", chunk)
chunk2 = dict(chunk, bytes=bytes.fromhex(""))
carrier("rust3-depsrc-chunk-empty-bytes", "rust-semantic", "DependencySourceChunk", chunk2)
chunk3 = dict(chunk, bytes="78")
carrier("rust3-depsrc-chunk-bytes-as-hex-text", "rust-semantic", "DependencySourceChunk", chunk3)


def entry(i, kind):
    return {"outputOrdinal": i, "kind": kind, "planRow": {}, "logicalPath": ".opensip/prepared/v3/%d-%s.blob" % (i, h64),
            "blobByteLength": 0, "blobSha256": h64, "contentByteLength": 0, "contentSha256": h64}


carrier("rust3-prepared-257-directive-entries", "rust-semantic", "PreparedOutputManifest",
        {"planId": "plan2:" + h64, "manifestSha256": h64, "entries": [entry(i, "build-script-directives") for i in range(257)]})
carrier("rust3-prepared-proc-macro-dylib-kind", "rust-semantic", "PreparedOutputManifest",
        {"planId": "plan2:" + h64, "manifestSha256": h64, "entries": [entry(0, "proc-macro-dylib")]})
span = {"kind": "source-span", "snapshotId": "snapshot2:" + h64, "path": "a", "contentSha256": h64, "startByte": 0, "endByte": 1, "factId": None}
empty_span = dict(span, endByte=0)
cand = {"candidateOrdinal": 0, "relation": "calls", "resolution": "x", "layer": "semantic", "producer": "rust-semantic", "producerVersion": "v",
        "schemaVersion": 1, "language": "rust", "sourceUniverseId": "sha256:" + h64, "targetUniverseId": "sha256:" + h64,
        "confidenceMillionths": 0, "relationSchemaId": "s", "canonicalRelationPayload": b"\xa0", "anchors": [empty_span]}
try:
    C.check_record("Rust3FactCandidateV1", cand)
    res["rust3-empty-span-carrier-level"] = "admitted-by-carrier (non-empty is handwritten ANCHOR-WIRE-SPAN)"
except W.Refuse as e:
    res["rust3-empty-span-carrier-level"] = "refused:" + e.code
res["cve1-vs-cbor-anchor-order"] = {
    "cbor": [a["path"] for a in sorted([dict(span, path="b"), dict(span, path="aa")], key=W.encode)],
    "cve1": [a["path"] for a in sorted([dict(span, path="b"), dict(span, path="aa")], key=W.cve1)]}
json.dump(res, sys.stdout, indent=1)
