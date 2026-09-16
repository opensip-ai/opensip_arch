"""Phase 3 (source42.v3, HC-53): standalone FactBatch payload and request/batch correlation vectors.

Charter, 'Current incorporated correction owners': "When reconstructing the existing provider traces, apply the current negotiated
payload selection, exact payload-byte representation and request/batch correlation law." This file executes that law on
discriminating positive and negative payloads at the host ANALYZING entry (ref/factbatch.py). vectors/phase3_traces.py applies the
same entry inside the protocol exchanges.

Every expectation below is my own derivation from the cited kit selector, written before execution and asserted. No author output is
compared. The two fact-plane vectors are kit-published bytes and are used as a cross-check of the encoder.
Writes traces/payload-vectors.json; exits 1 on any assertion failure.
"""
import copy
import json
import sys

OUTP = '/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output/'
sys.path.insert(0, OUTP + 'ref')
sys.path.insert(0, OUTP + 'tools')
sys.path.insert(0, OUTP + 'vectors')
import factbatch as FB  # noqa: E402
import payload_fixtures as PF  # noqa: E402
import protocol3 as P  # noqa: E402
import status as S  # noqa: E402

failures = []


def check(cond, label):
    if not cond:
        failures.append(label)


SCHEMA, CBOR, UNNEG = "PROVIDER_RETURN_SCHEMA", "PROVIDER_RETURN_PAYLOAD_CBOR", "PROVIDER_RETURN_UNNEGOTIATED_V3"
L_NEG = "native-evidence.md s9.1 lines 2785-2791; native/fact-batch.schema.v3.json#/x-opensip-negotiation/whenPresent,whenAbsent; return-law invocation.inputs.batch"
L_V2 = "artifacts/rust-provider-protocol.v2.json FactBatchV2 (closed: analysisOrdinal, stageId, batchIndex, candidates); FactCandidateV1 closed"
L_BYTES = ("artifacts/fact-plane.v1.json candidateSchema.transportRepresentation and relationPayloadSchemaRegistryV1.canonicalPayloadEncoding; "
           "native/fact-batch.schema.v3.json#/properties/candidates/items/properties/canonicalRelationPayloadHex; native-evidence.md s9.6 lines 2901-2909")
L_REG = "artifacts/fact-plane.v1.json relationPayloadSchemaRegistryV1.schemas[relation] (closed fields, types, resolutionRules); negativeFixtures keys"
L_CORR = ("native/dispatch-binding.schema.v1.json#/x-opensip-wire/correlation; native/fact-batch.schema.v3.json#/x-opensip-negotiation/stageCorrelation; "
          "native-evidence.md s9.6 lines 2911-2931")
L_STAGEID = "native/fact-batch.schema.v3.json#/properties/stageId; delivery.v2.json StageRequestV1.stageId; rust-provider-protocol.v2.json StageRequestV2.planStage"
L_STREAM = ("native/dispatch-binding.schema.v1.json#/properties/expectedFirstCandidateOrdinal; occupancy-companion.schema.v1.json#/x-opensip-order-vocabulary/"
            "candidateOrdinal/not; delivery.v2.json FactCandidateV1.candidateOrdinal ('contiguous within its stage across FactBatch frames')")
L_ORDER = "native/occupancy-companion.schema.v1.json#/x-opensip-order-vocabulary/candidateOrdinal/law (HC-51)"
L_DISPATCH = "return-law invocation.inputs.dispatch/planId/execution_plan/stage_specs/closures; return-law joins[0..3]"
L_COMP = "native/occupancy-companion.schema.v1.json (required, additionalProperties false, allOf branches, $defs/LogicalPath)"
L_ASSOC = ("native/occupancy-companion.schema.v1.json#/properties/targetUniverseId,targetNativeId and #/x-opensip-order-vocabulary/candidateOrdinal/semanticJoin; "
           "foundation/evaluator-projection-registry.v1.json#/relations/*/targetNativeIdField,endpointTargetRungs; return-law missingAndIncomplete")
L_ATOMIC = "return-law order.atomic and errorHandling.atomicRefuse; native-evidence.md s9.6 lines 3006-3007"
HOST_ORIGIN_KEYS = {"PROVIDER_RETURN_DISPATCH", "PROVIDER_RETURN_PLAN_MISMATCH", "PROVIDER_RETURN_STAGE_NOT_IN_PLAN", "PROVIDER_RETURN_STAGE_SPEC",
                    "PROVIDER_RETURN_STAGE_PRODUCER", "PROVIDER_RETURN_PRODUCER_NOT_PROVIDER", "cb24.DISPATCH_BINDING_SCHEMA",
                    "cb24.DISPATCH_REQUEST_MISMATCH", "cb24.FACT_BATCH_V2_CORRELATION_UNOBSERVED"}
EXPECTED_TERMINATION = {"provider-return": ("operational-failed", "PROVIDER.PROTOCOL_VIOLATION"), "host-internal": ("operational-failed", "SYSTEM.OUTCOME.ILLEGAL_STATE")}

TS0, TS1 = FB.stage_request(PF.analyze("ts"), "ts", 0), FB.stage_request(PF.analyze("ts"), "ts", 1)
RS0 = FB.stage_request(PF.analyze("rust"), "rust", 0)
TSB = PF.v3("ts-calls", 0, PF.calls_b0())
RSB = PF.v3("rust-calls", 0, PF.rust_calls_b0())
IMP0 = PF.v3("ts-imports", 0, PF.imports_b0())
IMP1 = PF.v3("ts-imports", 1, PF.imports_b1())
STREAM1 = {}
FB.advance(STREAM1, IMP0)
check(STREAM1 == {"ts-imports": {"nextBatchIndex": 1, "nextCandidateOrdinal": 3}}, "host stream after ts-imports batch 0 is (batchIndex 1, first candidate 3)")
DELETE = object()
VECTORS = []


def with_(payload, *edits):
    p = copy.deepcopy(payload)
    for path, value in edits:
        cur = p
        for k in path[:-1]:
            cur = cur[k]
        if value is DELETE:
            del cur[path[-1]]
        else:
            cur[path[-1]] = value
    return p


def run(vid, group, cls, shape, payload, law, first=None, keys=(), request=None, dispatch="derive", stream=None, token=(True, True), note="", extra=None):
    request = request or (TS1 if shape == "ts" else RS0)
    d = FB.derive_dispatch(PF.RETAINED, request, copy.deepcopy(stream or {})) if dispatch == "derive" else dispatch
    res = FB.buffer_fact_batch_occupancy(copy.deepcopy(payload), PF.caps(shape, token[0]), PF.caps(shape, token[1]), d, PF.RETAINED, request, PF.HOST[shape])
    expected = {"result": "REFUSE" if first else "ADMIT", "firstRefusal": first, "violationKeys": list(keys) if first else []}
    observed = {"result": res["result"], "firstRefusal": res["firstRefusal"], "violationKeys": res["violationKeys"]}
    check(observed == expected, f"{vid}: expected {expected} observed {observed}")
    if first and res["violations"]:
        origin = "host-internal" if first in HOST_ORIGIN_KEYS else "provider-return"
        check(res["violations"][0]["origin"] == origin, f"{vid}: first refusal origin {res['violations'][0]['origin']} != {origin}")
        term = res["publicRoute"]["termination"]
        check((term["class"], term["errorCode"]) == EXPECTED_TERMINATION[origin], f"{vid}: public route {res['publicRoute']}")
        check(res["bufferedCompanions"] == [], f"{vid}: refusal buffered companions")
    elif not first:
        if res["negotiated"]:
            check(res["bufferedCompanions"] == payload.get("occupancyCompanions"), f"{vid}: admitted batch buffers exactly its companions")
        else:
            check(res["bufferedCompanions"] == [] and res["occupancy"].startswith("omitted"), f"{vid}: unnegotiated batch captures no occupancy")
    unchanged = None
    if res["negotiated"] and isinstance(payload, dict):
        b = FB.BASE.admit(payload, FB.FB3, "#")
        unchanged = {"ok": b["ok"], "order": b["order"], "stockErrorCount": len(b["stock"]), "typed": b["typed"]}
    rec = {"id": vid, "group": group, "class": cls, "provider": shape, "law": law, "note": note,
           "negotiation": {"helloCarriesToken": token[0], "helloAckCarriesToken": token[1]}, "request": request,
           "payload": payload, "expected": expected, "observed": res, "matches": observed == expected, "unchangedKitSchemaAdmission": unchanged}
    if isinstance(payload, dict) and len(payload.get("candidates") or []) > 64:
        rec["payload"] = {"summary": f"{len(payload['candidates'])} candidates; first {payload['candidates'][0]}", "stageId": payload["stageId"]}
        rec["observed"] = dict(res, exactBytes=f"{len(res['exactBytes'])} records", violations=res["violations"][:3])
    if extra:
        for label, cond, value in extra(res):
            check(cond, f"{vid}: {label}")
            rec.setdefault("extraChecks", []).append({"label": label, "ok": bool(cond), "value": value})
    VECTORS.append(rec)
    return res


# ================================================================================================ negotiated payload selection
run("SEL-ts-negotiated-v3", "selection", "valid", "ts", TSB, [L_NEG, L_CORR])
run("SEL-rust-negotiated-v3", "selection", "valid", "rust", RSB, [L_NEG, L_CORR])
run("SEL-ts-unnegotiated-v2", "selection", "valid", "ts", PF.v2(TSB), [L_NEG, L_V2], token=(False, False))
run("SEL-rust-unnegotiated-v2", "selection", "valid", "rust", PF.v2(RSB), [L_NEG, L_V2], token=(False, False))
run("SEL-ts-unnegotiated-v3", "selection", "invalid", "ts", TSB, [L_NEG], UNNEG, [UNNEG], token=(False, False))
run("SEL-rust-unnegotiated-v3", "selection", "invalid", "rust", RSB, [L_NEG], UNNEG, [UNNEG], token=(False, False))
run("SEL-ts-negotiated-v2", "selection", "invalid", "ts", PF.v2(TSB), [L_NEG, "fact-batch.schema.v3.json#/required"], SCHEMA, [SCHEMA])
run("SEL-rust-negotiated-v2", "selection", "invalid", "rust", PF.v2(RSB), [L_NEG, "fact-batch.schema.v3.json#/required"], SCHEMA, [SCHEMA])
run("SEL-token-on-hello-only", "selection", "explanatory", "ts", TSB, [L_NEG], UNNEG, [UNNEG], token=(True, False),
    note="negotiation needs the token on both Hello and HelloAck; in an exchange the HelloAck echo mismatch faults first (exchangeControls)")
run("SEL-negotiated-v3-empty-companions", "selection", "valid", "ts", with_(TSB, (("occupancyCompanions",), [])), [L_NEG, "fact-batch.schema.v3.json#/properties/occupancyCompanions/description ('Empty is lawful')"],
    extra=lambda r: [("occupancy states zero buffered companions", r["occupancy"].startswith("0 companion"), r["occupancy"])])
run("SEL-unnegotiated-v2-plus-schemaVersion", "selection", "invalid", "ts", with_(PF.v2(TSB), (("schemaVersion",), 3)), [L_NEG], UNNEG, [UNNEG], token=(False, False))
run("SEL-unnegotiated-v2-candidate-occupancy-member", "selection", "invalid", "ts", with_(PF.v2(TSB), (("candidates", 0, "occupancy"), "first-party")),
    [L_V2, "fact-plane.v1.json candidateSchema closed; occupancy-companion.schema.v1.json#/x-opensip-wire/historicalFactCandidateV1"],
    "cb24.FACT_BATCH_V2_SCHEMA", ["cb24.FACT_BATCH_V2_SCHEMA"], token=(False, False))
TS_FB1_SHAPE = {"analysisOrdinal": 0, "stageId": "ts-calls", "batchIndex": 0, "facts": copy.deepcopy(TSB["candidates"]), "batchCommitment": "sha256:" + PF.h("facts")}
run("SEL-ts-unnegotiated-delivery-v2-FactBatchV1-shape", "selection", "invalid", "ts", TS_FB1_SHAPE,
    [L_NEG, L_V2, "delivery.v2.json typescriptSemanticSubstrate payloadSchemas.FactBatchV1 (TS major 1)"], "cb24.FACT_BATCH_V2_SCHEMA", ["cb24.FACT_BATCH_V2_SCHEMA"],
    token=(False, False), note="advisory A-s42v3-1: s9.1 names historical FactBatchV2 for both majors; delivery.v2 publishes TS FactBatchV1 {facts, batchCommitment}",
    extra=lambda r: [("alternative reading: the payload's member set equals delivery.v2 FactBatchV1's closed required list",
                      sorted(TS_FB1_SHAPE) == sorted(FB.TS_FB1["required"]), sorted(FB.TS_FB1["required"]))])

# ================================================================================================ exact payload bytes
DEC0 = TSB["candidates"][0]["decodedRelationPayload"]
HEX0 = TSB["candidates"][0]["canonicalRelationPayloadHex"]


def tstr(s):
    b = s.encode("utf-8")
    return (bytes([0x60 | len(b)]) if len(b) < 24 else bytes([0x78, len(b)])) + b


PAIRS = {k: tstr(k) + tstr(DEC0[k]) for k in DEC0}
HAND = b"\xa3" + PAIRS["caller"] + PAIRS["calleeText"] + PAIRS["resolvedCallee"]
check(HAND.hex() == HEX0, "hand-assembled bytes (keys ordered caller(0x66) < calleeText(0x6a) < resolvedCallee(0x6e) by encoded key bytes) equal the encoder")
BYTES_CASES = [
    ("BYTES-hex-is-canonical-json-utf8", json.dumps(DEC0, sort_keys=True, separators=(",", ":")).encode("utf-8").hex(), "hex transcribes canonical JSON UTF-8, not CBOR"),
    ("BYTES-map-keys-alphabetical-not-deterministic", (b"\xa3" + PAIRS["calleeText"] + PAIRS["caller"] + PAIRS["resolvedCallee"]).hex(), "alphabetical key order is not encoded-key order"),
    ("BYTES-non-shortest-text-header", (b"\xa3" + b"\x78\x06caller" + tstr(DEC0["caller"]) + PAIRS["calleeText"] + PAIRS["resolvedCallee"]).hex(), "1-byte length for a 6-byte key"),
    ("BYTES-indefinite-length-map", (b"\xbf" + PAIRS["caller"] + PAIRS["calleeText"] + PAIRS["resolvedCallee"] + b"\xff").hex(), "indefinite map"),
    ("BYTES-trailing-byte", (HAND + b"\x00").hex(), "one trailing byte"),
    ("BYTES-hex-of-another-lawful-payload", FB.cbor_encode(dict(DEC0, resolvedCallee="sym:function:src/c.ts#other")).hex(), "valid deterministic CBOR of a different payload than the decoded observation")]
for vid, hx, note in BYTES_CASES:
    run(vid, "bytes", "invalid", "ts", with_(TSB, (("candidates", 0, "canonicalRelationPayloadHex"), hx)), [L_BYTES], CBOR, [CBOR], note=note)
run("BYTES-uppercase-hex-same-bytes", "bytes", "invalid", "ts", with_(TSB, (("candidates", 0, "canonicalRelationPayloadHex"), HEX0.upper())),
    [L_BYTES, "fact-plane.v1.json admittedRecordSchema.payload.fields.canonicalRelationPayload ('lowercase even-length')"], SCHEMA, [SCHEMA],
    note="the bytes are exact; only the JSON-vector transcription is wrong, so only the schema pattern refuses")
UNKNOWN_FIELD = dict(DEC0, futureField=True)
run("BYTES-deterministic-cbor-with-unknown-field", "bytes", "invalid", "ts",
    with_(TSB, (("candidates", 0, "decodedRelationPayload"), UNKNOWN_FIELD), (("candidates", 0, "canonicalRelationPayloadHex"), FB.cbor_encode(UNKNOWN_FIELD).hex())),
    [L_BYTES, L_REG], "FACT_RELATION_PAYLOAD_INVALID", ["FACT_RELATION_PAYLOAD_INVALID"], note="byte-exact CBOR is not sufficient: the closed relation schema refuses")
NO_TARGET = {k: v for k, v in DEC0.items() if k != "resolvedCallee"}
run("BYTES-rung-required-field-missing", "bytes", "invalid", "ts",
    with_(TSB, (("candidates", 0, "decodedRelationPayload"), NO_TARGET), (("candidates", 0, "canonicalRelationPayloadHex"), FB.cbor_encode(NO_TARGET).hex())),
    [L_REG, L_ASSOC], "FACT_RELATION_PAYLOAD_INVALID", ["FACT_RELATION_PAYLOAD_INVALID", "TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH"],
    note="resolved-callee requires resolvedCallee; the companion's targetNativeId then names no decoded field (masked later violation)")

DECODER = [("uint-direct-23", "17", 23), ("uint-one-byte-24", "1818", 24), ("uint-one-byte-non-shortest", "1817", "non-shortest-argument"),
           ("uint-two-byte-non-shortest", "1900ff", "non-shortest-argument"), ("uint64-max", "1b" + "ff" * 8, 2 ** 64 - 1),
           ("reserved-additional-information", "1c", "reserved-additional-information"), ("negative-integer", "20", "negative-integer"),
           ("float16", "f90000", "float"), ("float64", "fb" + "00" * 8, "float"), ("undefined", "f7", "simple-value"), ("break", "ff", "indefinite-length"),
           ("tag", "c06161", "tag"), ("byte-string", "4100", "byte-string"), ("indefinite-text", "7f6161ff", "indefinite-length"),
           ("indefinite-array", "9fff", "indefinite-length"), ("indefinite-map", "bfff", "indefinite-length"), ("duplicate-key", "a2616100616100", "duplicate-key"),
           ("map-key-order", "a2616200616100", "map-key-order"), ("shorter-key-first", "a2616200626161f6", {"b": 0, "aa": None}),
           ("longer-key-first", "a2626161f6616200", "map-key-order"), ("non-text-key", "a10000", "non-text-key"), ("non-nfc-text", "6365cc81", "non-nfc-text"),
           ("nfc-text", "62c3a9", "é"), ("malformed-utf8", "61ff", "malformed-utf8"), ("truncated", "6261", "truncated"), ("trailing-bytes", "f600", "trailing-bytes"),
           ("empty-map", "a0", {}), ("definite-array", "820102", [1, 2]), ("null-false-true", "83f6f4f5", [None, False, True])]
decoder_rows = []
for vid, hx, exp in DECODER:
    try:
        got, cls = FB.cbor_decode(bytes.fromhex(hx)), None
    except FB.CborError as exc:
        got, cls = None, exc.cls
    ok = (cls == exp) if isinstance(exp, str) and exp.islower() and "-" in exp or exp in ("tag", "float", "truncated") else (cls is None and FB.same(got, exp))
    check(ok, f"decoder {vid}: expected {exp!r} got {cls or got!r}")
    decoder_rows.append({"id": vid, "hex": hx, "expected": exp, "refusalClass": cls, "value": got, "ok": ok})
ENCODER = [("negative", -1, "negative-integer"), ("float", 1.5, "float"), ("byte-string", b"x", "byte-string"), ("non-nfc-text", "é", "non-nfc-text"),
           ("uint64-overflow", 2 ** 64, "uint64-range"), ("non-text-key", {1: "a"}, "non-text-key"), ("lone-surrogate", "\ud800", "malformed-utf8"),
           ("true", True, "=f5"), ("uint64-max", 2 ** 64 - 1, "=1bffffffffffffffff"), ("encoded-key-order", {"from": "a", "to": "b"}, "=a262746f61626466726f6d6161")]
encoder_rows = []
for vid, value, exp in ENCODER:
    try:
        got, cls = FB.cbor_encode(value).hex(), None
    except FB.CborError as exc:
        got, cls = None, exc.cls
    ok = (got == exp[1:]) if exp.startswith("=") else cls == exp
    check(ok, f"encoder {vid}: expected {exp} got {cls or got}")
    encoder_rows.append({"id": vid, "value": repr(value), "expected": exp, "refusalClass": cls, "hex": got, "ok": ok})
PROFILE_COVERAGE = {"negative integers": ["negative-integer"], "floating point": ["float16", "float64"], "byte strings inside relation payloads": ["byte-string"],
                    "tags": ["tag"], "indefinite lengths": ["indefinite-text", "indefinite-array", "indefinite-map", "break", "BYTES-indefinite-length-map"],
                    "duplicate keys": ["duplicate-key"], "non-NFC text": ["non-nfc-text"], "unknown fields": ["BYTES-deterministic-cbor-with-unknown-field"]}
check(set(PROFILE_COVERAGE) == set(FB.ENC["forbidden"]), "every published forbidden profile item has a vector")
known = {r["id"]: r["ok"] for r in decoder_rows} | {v["id"]: v["matches"] for v in VECTORS}
check(all(known.get(i) for ids in PROFILE_COVERAGE.values() for i in ids), "every profile-coverage vector executed and matched")
kit_cross = []
for v in FB.FP_VECTORS:
    c = v["candidate"]
    enc = FB.cbor_encode(c["decodedRelationPayload"]).hex()
    dec = FB.cbor_decode(bytes.fromhex(c["canonicalRelationPayloadHex"]))
    item = FB.K.admit(c, FB.FB3, "#/properties/candidates/items")
    row = {"vector": v["id"], "encoderEqualsKitHex": enc == c["canonicalRelationPayloadHex"], "decodeEqualsKitDecoded": FB.same(dec, c["decodedRelationPayload"]),
           "kitCandidateAdmitsAsFactBatchV3CandidateItem": item["ok"], "selector": FB.FACT_PLANE + FB.find_any(FB.FP, "vectors")[0]}
    check(row["encoderEqualsKitHex"] and row["decodeEqualsKitDecoded"] and row["kitCandidateAdmitsAsFactBatchV3CandidateItem"], f"kit vector {v['id']}: {row}")
    kit_cross.append(row)

# ================================================================================================ request/batch correlation
run("CORR-analyze-subset-dispatch", "correlation", "valid", "ts", TSB, [L_CORR, "dispatch-binding.schema.v1.json#/properties/retainedStageOrdinal,analyzeRequestOrdinal"],
    extra=lambda r: [("dispatch admits dispatch-binding.schema.v1.json", r["dispatchSchema"]["ok"], r["dispatchSchema"]),
                     ("retainedStageOrdinal 3 differs from analyzeRequestOrdinal 1", (r["dispatch"]["retainedStageOrdinal"], r["dispatch"]["analyzeRequestOrdinal"]) == (3, 1),
                      [r["dispatch"]["retainedStageOrdinal"], r["dispatch"]["analyzeRequestOrdinal"]])])
run("CORR-stage-batch0", "correlation", "valid", "ts", IMP0, [L_CORR, L_STREAM], request=TS0,
    extra=lambda r: [("dispatch (retained 1, request 0, batch 0, first 0)", [r["dispatch"][k] for k in ("retainedStageOrdinal", "analyzeRequestOrdinal", "expectedBatchIndex", "expectedFirstCandidateOrdinal")] == [1, 0, 0, 0], None)])
run("CORR-stage-batch1-continues-stream", "correlation", "valid", "ts", IMP1, [L_CORR, L_STREAM], request=TS0, stream=STREAM1,
    extra=lambda r: [("dispatch (retained 1, request 0, batch 1, first 3)", [r["dispatch"][k] for k in ("retainedStageOrdinal", "analyzeRequestOrdinal", "expectedBatchIndex", "expectedFirstCandidateOrdinal")] == [1, 0, 1, 3], None)])
STAGE_ID = "PROVIDER_RETURN_STAGE_ID"
run("CORR-stageId-echoes-analyzeRequestOrdinal-text", "correlation", "invalid", "ts", with_(TSB, (("stageId",), "1")), [L_CORR, L_STAGEID], STAGE_ID, [STAGE_ID])
run("CORR-stageId-echoes-retainedStageOrdinal-text", "correlation", "invalid", "ts", with_(TSB, (("stageId",), "3")), [L_CORR, L_STAGEID], STAGE_ID, [STAGE_ID])
run("CORR-stageId-integer", "correlation", "invalid", "ts", with_(TSB, (("stageId",), 3)), [L_STAGEID, "fact-batch.schema.v3.json#/x-opensip-negotiation/fieldChanges/stageId"],
    SCHEMA, [SCHEMA, STAGE_ID])
run("CORR-stageId-other-requested-stage", "correlation", "invalid", "ts", with_(TSB, (("stageId",), "ts-imports")), [L_CORR, L_STAGEID], STAGE_ID, [STAGE_ID])
run("CORR-rust-stageId-echoes-stageOrdinal", "correlation", "invalid", "rust", with_(RSB, (("stageId",), "0")), [L_CORR, L_STAGEID], STAGE_ID, [STAGE_ID])
run("CORR-analysisOrdinal-mismatch", "correlation", "invalid", "ts", with_(TSB, (("analysisOrdinal",), 1)), [L_CORR], "PROVIDER_RETURN_ANALYSIS_ORDINAL", ["PROVIDER_RETURN_ANALYSIS_ORDINAL"])
run("CORR-batchIndex-gap", "correlation", "invalid", "ts", with_(IMP1, (("batchIndex",), 2)), [L_CORR], "PROVIDER_RETURN_BATCH_INDEX", ["PROVIDER_RETURN_BATCH_INDEX"],
    request=TS0, stream=STREAM1)
run("CORR-batchIndex-replayed", "correlation", "invalid", "ts", with_(IMP1, (("batchIndex",), 0)), [L_CORR], "PROVIDER_RETURN_BATCH_INDEX", ["PROVIDER_RETURN_BATCH_INDEX"],
    request=TS0, stream=STREAM1)
STREAM = "PROVIDER_RETURN_CANDIDATE_STREAM"
run("CORR-stream-restarts-at-zero", "correlation", "invalid", "ts", PF.renumber(IMP1, 0), [L_STREAM], STREAM, [STREAM], request=TS0, stream=STREAM1)
run("CORR-stream-skips", "correlation", "invalid", "ts", PF.renumber(IMP1, 4), [L_STREAM], STREAM, [STREAM], request=TS0, stream=STREAM1)
run("CORR-internal-gap-schema-lawful-stream-unlawful", "correlation", "invalid", "ts", with_(TSB, (("candidates", 1, "candidateOrdinal"), 2)), [L_ORDER, L_STREAM], STREAM, [STREAM],
    note="gaps are lawful at the order annotation; the candidate-stream join refuses", extra=lambda r: [("payload schema admits", r["payloadSchema"]["ok"], None)])
run("CORR-duplicate-ordinal", "correlation", "invalid", "ts", with_(TSB, (("candidates", 1, "candidateOrdinal"), 0)), [L_ORDER, L_STREAM], SCHEMA, [SCHEMA, STREAM])
run("CORR-reverse-order", "correlation", "invalid", "ts", with_(TSB, (("candidates",), [TSB["candidates"][1], TSB["candidates"][0]])), [L_ORDER, L_STREAM], SCHEMA, [SCHEMA, STREAM],
    note="arrays are not silently sorted")
run("CORR-dispatch-omitted", "correlation", "invalid", "ts", TSB, [L_DISPATCH, "native-evidence.md s9.6 line 2931"], "PROVIDER_RETURN_DISPATCH", ["PROVIDER_RETURN_DISPATCH"], dispatch=None)
D1 = FB.derive_dispatch(PF.RETAINED, TS1, {})
run("CORR-dispatch-retainedStageOrdinal-equated-with-analyzeRequestOrdinal", "correlation", "invalid", "ts", TSB,
    [L_DISPATCH, "dispatch-binding.schema.v1.json#/description ('MUST NOT be equated')"], "PROVIDER_RETURN_STAGE_SPEC", ["PROVIDER_RETURN_STAGE_SPEC"],
    dispatch=dict(D1, retainedStageOrdinal=D1["analyzeRequestOrdinal"]), note="host mis-derivation: execution-plan row 1 is ts-imports, whose stageSpecDigest differs")
run("CORR-dispatch-extra-member", "correlation", "invalid", "ts", TSB, ["dispatch-binding.schema.v1.json (additionalProperties false)"],
    "cb24.DISPATCH_BINDING_SCHEMA", ["cb24.DISPATCH_BINDING_SCHEMA"], dispatch=dict(D1, stageOrdinal=1))
run("CORR-dispatch-plan-mismatch", "correlation", "invalid", "ts", TSB, [L_DISPATCH], "PROVIDER_RETURN_PLAN_MISMATCH", ["PROVIDER_RETURN_PLAN_MISMATCH"],
    dispatch=dict(D1, planId=PF.OTHER_PLAN_ID))
run("CORR-dispatch-producer-is-not-stage-producer", "correlation", "invalid", "ts", TSB, [L_DISPATCH, "native-evidence.md s9.6 lines 2941-2946"],
    "PROVIDER_RETURN_STAGE_PRODUCER", ["PROVIDER_RETURN_STAGE_PRODUCER"], dispatch=dict(D1, producerClosure=PF.CLOSURE["rust"]))
run("CORR-dispatch-derived-for-another-request", "correlation", "invalid", "ts", TSB, [L_DISPATCH, L_CORR], "cb24.DISPATCH_REQUEST_MISMATCH",
    ["cb24.DISPATCH_REQUEST_MISMATCH", STAGE_ID], dispatch=FB.derive_dispatch(PF.RETAINED, TS0, {}))
BIG = {"schemaVersion": 3, "analysisOrdinal": 0, "stageId": "ts-calls", "batchIndex": 0, "occupancyCompanions": [],
       "candidates": [PF.cand("ts", i, "calls", "syntactic-callee-name", {"caller": "sym:function:src/a.ts#main", "calleeText": f"f{i}"}) for i in range(FB.MAX_FB + 1)]}
run("CORR-over-maxFactBatchCandidates", "correlation", "invalid", "ts", BIG, ["fact-batch.schema.v3.json#/properties/candidates/maxItems", "rust-provider-protocol.v2.json limits.maxFactBatchCandidates"],
    SCHEMA, [SCHEMA])
check(FB.MAX_FB == 4096 == FB.K.doc(FB.FB3)["properties"]["candidates"]["maxItems"], "maxFactBatchCandidates equals the V3 maxItems")

explanatory = []
d = FB.derive_dispatch(PF.RETAINED, TS1, {})
try:
    int(TSB["stageId"])
    int_lookup = "int(batch.stageId) succeeded"
except ValueError as exc:
    int_lookup = f"ValueError: {exc}"


def spec_at(ordinal):
    row = next(s for s in PF.RETAINED["executionPlan"]["stages"] if s["ordinal"] == ordinal)
    return PF.RETAINED["stageSpecs"][row["stageSpecDigest"]]["stageId"]


row = {"id": "CORR-lookup-by-retainedStageOrdinal-not-integer-stageId", "integerStageIdLookup": int_lookup,
       "lookupByRetainedStageOrdinal": spec_at(d["retainedStageOrdinal"]), "lookupByAnalyzeRequestOrdinal": spec_at(d["analyzeRequestOrdinal"]),
       "law": "dispatch-binding.schema.v1.json#/x-opensip-wire/correlation[4..5]"}
check(row["integerStageIdLookup"].startswith("ValueError") and row["lookupByRetainedStageOrdinal"] == "ts-calls" and row["lookupByAnalyzeRequestOrdinal"] == "ts-imports", str(row))
explanatory.append(row)
row = {"id": "CORR-buffer-entry-does-not-require-receipts-or-views", "parameters": FB.BUFFER_PARAMETERS,
       "law": "native-evidence.md s9.6 lines 2933-2939; return-law invocation.when and inputs.stage_receipts"}
check("receipts" not in " ".join(FB.BUFFER_PARAMETERS) and "views" not in FB.BUFFER_PARAMETERS and "dispatch" in FB.BUFFER_PARAMETERS, str(row))
explanatory.append(row)
req_rows = {"ts-base": FB.analyze_request_faults(PF.analyze("ts"), "ts", PF.RETAINED, 2), "rust-base": FB.analyze_request_faults(PF.analyze("rust"), "rust", PF.RETAINED, 1),
            "ts-analysisOrdinal-1": FB.analyze_request_faults(PF.analyze("ts", 1), "ts", PF.RETAINED, 2),
            "ts-stageOrdinal-not-contiguous": FB.analyze_request_faults(with_(PF.analyze("ts"), (("stageRequests", 1, "stageOrdinal"), 2)), "ts", PF.RETAINED, 2),
            "ts-stage-not-in-plan": FB.analyze_request_faults(with_(PF.analyze("ts"), (("stageRequests", 1, "stageId"), "ts-references")), "ts", PF.RETAINED, 2)}
check(req_rows["ts-base"] == [] and req_rows["rust-base"] == [] and all(len(req_rows[k]) == 1 for k in req_rows if k not in ("ts-base", "rust-base")), f"analyze request law {req_rows}")
explanatory.append({"id": "CORR-analyze-request-law", "faults": req_rows,
                    "law": "delivery.v2.json AnalyzeV1.analysisOrdinal ('exactly 0'), StageRequestV1.stageOrdinal; rust-provider-protocol.v2.json StageRequestV2.stageOrdinal; s9.6 line 2916 (subset of Plan stages)"})

M = P.Protocol3()
exchange_controls = []
for vid, h_tok, a_tok in (("hello-and-ack-carry-token", True, True), ("neither-carries-token", False, False), ("hello-only", True, False), ("ack-only", False, True)):
    r = M.run([PF.hello("ts", h_tok), PF.ack("ts", a_tok)])
    rules = [t["rule"] for t in r["trace"]]
    exp = ["P3-01", "P3-02"] if h_tok == a_tok else ["P3-01", "payload:hello-ack-echo-mismatch(s9.1-step2)"]
    ok = rules == exp and (h_tok != a_tok or r["state"]["identityNegotiated"] is True) and FB.negotiated(PF.caps("ts", h_tok), PF.caps("ts", a_tok)) == (h_tok and a_tok)
    check(ok, f"exchange control {vid}: {rules} {r['state']}")
    exchange_controls.append({"id": vid, "rules": rules, "expectedRules": exp, "identityNegotiated": r["state"]["identityNegotiated"],
                              "payloadSelected": "FactBatchV3" if h_tok and a_tok else ("FactBatchV2" if h_tok == a_tok else "none: exchange faulted at HelloAck"), "ok": ok,
                              "law": "native-evidence.md s9.1 lines 2783-2791 and step 2 (exact echo); target-attribution-v2 is not an identity token"})

# ================================================================================================ companions
C0, C2 = IMP0["occupancyCompanions"]
C3, C4, C5 = IMP1["occupancyCompanions"]
run("COMP-partial-with-gap", "companions", "valid", "ts", IMP0, [L_ASSOC, L_ORDER, "return-law missingAndIncomplete.emptyOrPartialCompanions"], request=TS0,
    extra=lambda r: [("buffered ordinals [0, 2]", [c["candidateOrdinal"] for c in r["bufferedCompanions"]] == [0, 2], None)])
run("COMP-symbol-file-external-package-first-party", "companions", "valid", "ts", IMP1, [L_COMP, L_ASSOC], request=TS0, stream=STREAM1)
run("COMP-package-unknown-all-null", "companions", "valid", "ts", with_(IMP0, (("occupancyCompanions", 1), PF.comp(2, PF.UNIV["ts-external"], "pkg:npm/left-pad", "package", "unknown"))),
    [L_COMP], request=TS0)
UC = "PROVIDER_RETURN_UNKNOWN_CANDIDATE"
run("COMP-unknown-candidate-atomic", "companions", "invalid", "ts", with_(IMP0, (("occupancyCompanions",), [C0, C2, PF.comp(7, PF.UNIV["ts"], "file:src/z.ts", "file", "first-party", evaluation="src/z.ts")])),
    [L_ASSOC, L_ATOMIC], UC, [UC], request=TS0, note="two lawful companions and one extra ordinal: nothing is buffered")
run("COMP-ordinal-from-prior-batch", "companions", "invalid", "ts", with_(IMP1, (("occupancyCompanions",), [C0] + IMP1["occupancyCompanions"])),
    [L_ASSOC, "return-law invocation.inputs.minted_by_ordinal ('THIS batch only')"], UC, [UC], request=TS0, stream=STREAM1)
run("COMP-target-universe-not-byte-equal", "companions", "invalid", "ts", with_(IMP0, (("occupancyCompanions", 0, "targetUniverseId"), PF.UNIV["ts-external"])),
    [L_ASSOC], "PROVIDER_RETURN_UNIVERSE_MISMATCH", ["PROVIDER_RETURN_UNIVERSE_MISMATCH"], request=TS0)
NID = "TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH"
run("COMP-targetNativeId-other-payload-id", "companions", "invalid", "ts", with_(IMP0, (("occupancyCompanions", 0, "targetNativeId"), "file:src/other.ts")), [L_ASSOC], NID, [NID], request=TS0)
run("COMP-targetNativeId-is-inventory-spelling", "companions", "invalid", "ts", with_(IMP0, (("occupancyCompanions", 0, "targetNativeId"), "src/b.ts")),
    [L_ASSOC, "return-law producerSupply.modes fileFirstParty ('evaluationNativeId is the inventory spelling, NOT the opaque payload string')"], NID, [NID], request=TS0)
RUNG = "TARGET_ATTRIBUTION_FIELD_NOT_ON_RUNG"
run("COMP-imports-syntactic-specifier-rung", "companions", "invalid", "ts", with_(IMP0, (("occupancyCompanions",), [C0, PF.comp(1, PF.UNIV["ts"], "./missing", "file", "unknown"), C2])),
    [L_ASSOC, "return-law producerSupply.modes syntacticRungs ('omit')"], RUNG, [RUNG], request=TS0)
run("COMP-calls-syntactic-callee-name-rung", "companions", "invalid", "ts", with_(TSB, (("occupancyCompanions",), TSB["occupancyCompanions"] + [PF.comp(1, PF.UNIV["ts"], "dynamicThing", "unknown", "unknown")])),
    [L_ASSOC], RUNG, [RUNG])
SCHEMA_COMPANION_CASES = [
    ("COMP-carries-planId", IMP0, None, (("occupancyCompanions", 0, "planId"), PF.PLAN_ID)),
    ("COMP-carries-sourceFactId", IMP0, None, (("occupancyCompanions", 0, "sourceFactId"), "fact2:" + PF.h("f"))),
    ("COMP-carries-producerClosure", IMP0, None, (("occupancyCompanions", 0, "producerClosure"), PF.CLOSURE["ts"])),
    ("COMP-schemaVersion-2", IMP0, None, (("occupancyCompanions", 0, "schemaVersion"), 2)),
    ("COMP-first-party-with-logicalPath", IMP0, None, (("occupancyCompanions", 0, "logicalPath"), "src/b.ts")),
    ("COMP-first-party-without-evaluationNativeId", IMP0, None, (("occupancyCompanions", 0, "evaluationNativeId"), None)),
    ("COMP-file-with-exported", IMP0, None, (("occupancyCompanions", 0, "exported"), "exported")),
    ("COMP-file-with-packageManifestPath", IMP0, None, (("occupancyCompanions", 0, "packageManifestPath"), "package.json")),
    ("COMP-external-with-evaluationNativeId", IMP0, None, (("occupancyCompanions", 1, "evaluationNativeId"), "left-pad")),
    ("COMP-package-external-with-logicalPath", IMP0, None, (("occupancyCompanions", 1, "logicalPath"), "node_modules/left-pad")),
    ("COMP-package-first-party-without-manifest", IMP1, STREAM1, (("occupancyCompanions", 2, "packageManifestPath"), None)),
    ("COMP-symbol-exported-null", IMP1, STREAM1, (("occupancyCompanions", 0, "exported"), None)),
    ("COMP-logicalPath-dot-dot-segment", IMP1, STREAM1, (("occupancyCompanions", 1, "logicalPath"), "../outside.ts")),
    ("COMP-unknown-kind-with-logicalPath", TSB, None, (("occupancyCompanions", 0, "logicalPath"), "src/c.ts")),
    ("COMP-companions-reversed", IMP0, None, (("occupancyCompanions",), [C2, C0])),
    ("COMP-companions-duplicate-ordinal", IMP0, None, (("occupancyCompanions",), [C0, C0]))]
for vid, base, stream, edit in SCHEMA_COMPANION_CASES:
    run(vid, "companions", "invalid", "ts", with_(base, edit), [L_COMP, L_ORDER] if "companions-" in vid else [L_COMP], SCHEMA, [SCHEMA],
        request=TS1 if base is TSB else TS0, stream=stream)

# ================================================================================================ HC-51 census and pre/post column
census = []


def walk(node, rel, path):
    if isinstance(node, dict):
        if node.get("x-opensip-order") == "candidateOrdinal":
            census.append(rel + "#" + path)
        for k, v in node.items():
            walk(v, rel, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, rel, f"{path}/{i}")


for rel, doc in FB.K.docs.items():
    walk(doc, rel, "")
check(sorted(census) == ["coop/design-corrections/native/fact-batch.schema.v3.json#/properties/candidates",
                         "coop/design-corrections/native/fact-batch.schema.v3.json#/properties/occupancyCompanions"], f"candidateOrdinal token census {census}")
admitted_v3 = [v for v in VECTORS if v["unchangedKitSchemaAdmission"] is not None and v["observed"]["payloadSchema"] and v["observed"]["payloadSchema"]["ok"]]
unchanged_refused = [v["id"] for v in admitted_v3 if not v["unchangedKitSchemaAdmission"]["ok"]
                     and any(o["violation"] == "ORDER_ANNOTATION_UNKNOWN" for o in v["unchangedKitSchemaAdmission"]["order"])]
check(admitted_v3 and len(unchanged_refused) == len(admitted_v3), "unchanged ref/schemas.py refuses every FactBatchV3 the corrected token admits")
hc51 = {"tokenCensus": census, "correctedSchemaAdmitted": len(admitted_v3), "unchangedKitRefusedOrderAnnotationUnknown": len(unchanged_refused),
        "otherKitSchemasUsingToken": [], "law": L_ORDER}

groups = {}
for v in VECTORS:
    g = groups.setdefault(v["group"], {"valid": 0, "invalid": 0, "explanatory": 0, "matched": 0})
    g[v["class"]] += 1
    g["matched"] += v["matches"]
keys_exercised = sorted({k for v in VECTORS for k in v["observed"]["violationKeys"]})
out = {"standing": ("source42.v3 executed reference payload/trace reconstruction of the charter-incorporated provider-trace law (negotiated payload selection, exact "
                    "payload bytes, request/batch correlation) at the host ANALYZING entry. These are executed schema, byte and join checks on constructed payloads; "
                    "they are not OS/provider/compiler qualification and claim no actual worker-process enforcement."),
       "checkOrder": FB.__doc__.split("The check order")[1].split("\n\n")[0].strip(),
       "retainedPlanFragment": PF.RETAINED, "hostContexts": PF.HOST, "analyze": {"ts": PF.analyze("ts"), "rust": PF.analyze("rust")},
       "vectors": VECTORS, "groups": groups, "violationKeysExercised": keys_exercised,
       "keyBindings": {k: FB.key_binding(k) for k in keys_exercised},
       "decoderVectors": decoder_rows, "encoderVectors": encoder_rows, "profileCoverage": PROFILE_COVERAGE, "handAssembledBytesEqualEncoder": HAND.hex() == HEX0,
       "kitVectorCrossCheck": kit_cross, "exchangeControls": exchange_controls, "explanatoryControls": explanatory, "hc51": hc51,
       "executedVsHost": {"executed": ["negotiated payload selection from Hello/HelloAck tokens (FactBatchV3 iff target-attribution-v2 on both; historical FactBatchV2 otherwise)",
                                       "schema admission of the exact JSON-vector payload: fact-batch.schema.v3.json with registered occupancy-companion $ref, allOf branches, typed scalars and the candidateOrdinal order token; FactBatchV2 closed members with closed FactCandidateV1 items",
                                       "restricted deterministic-CBOR decode-once and re-encode of every candidate's canonicalRelationPayload bytes against canonicalRelationPayloadHex and decodedRelationPayload, and the closed relation payload schema",
                                       "DispatchBindingV1 derivation from the Analyze request and retained Plan fragment, its schema, Plan/stage-spec/producer joins, and stageId/analysisOrdinal/batchIndex/candidate-stream correlation across batches",
                                       "companion association: candidate in this batch, byte-equal target universe, targetNativeId equal to the decoded registry field at a target rung; atomic refusal; public route from x-opensip-routes"],
                          "futureHostAssumptions": ["actual worker process emission of these bytes and companions", "frame envelope byte framing"],
                          "notClaimed": ["actual worker-process enforcement", "post-terminal bind_worker_occupancy (fact2 minting, native views, stageReceipts, TargetAttributionV2 projection/capture, C15)",
                                         "anchor admission and fact identity of the constructed candidates"]},
       "assertionFailures": failures}
S.dump("traces/payload-vectors.json", out)
print(json.dumps({"vectors": len(VECTORS), "groups": groups, "decoder": len(decoder_rows), "encoder": len(encoder_rows), "keysExercised": keys_exercised,
                  "hc51": {k: hc51[k] for k in ("correctedSchemaAdmitted", "unchangedKitRefusedOrderAnnotationUnknown")}, "failures": failures}, indent=1))
sys.exit(1 if failures else 0)
