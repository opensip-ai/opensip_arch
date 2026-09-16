"""FactBatch payload law for the provider traces: negotiated payload selection, exact relation-payload bytes and request/batch
correlation, reconstructed as the host ANALYZING entry buffer_fact_batch_occupancy (source42.v3, HC-53).

Normative sources (kit bytes only; no author code consulted):
  native-evidence.md s9.1 lines 2785-2794 (optional token target-attribution-v2; FactBatchV3 iff present on Hello and HelloAck; a
    FactBatchV3 payload without the token or a FactBatchV2 payload with it is PROVIDER.PROTOCOL_VIOLATION), s9.2 line 2828, s9.6 lines
    2896-3018 (the wrapper writes deterministic-CBOR bytes and the JSON-vector hex transcribes the same bytes; DispatchBindingV1
    correlation; buffer timing without receipts/views; companion association; atomic refusal)
  native/fact-batch.schema.v3.json (whole document including #/x-opensip-negotiation)
  native/occupancy-companion.schema.v1.json (allOf, #/x-opensip-order-vocabulary, #/x-opensip-wire)
  native/dispatch-binding.schema.v1.json (#/x-opensip-wire/correlation)
  foundation/provider-target-attribution-return.schema.v2.json (#/x-opensip-return-law, #/x-opensip-new-internal-faults)
  foundation/evaluator-fault-observation.schema.v3.json#/x-opensip-routes (public route)
  foundation/evaluator-projection-registry.v1.json#/relations/*/targetNativeIdField, endpointTargetRungs
  artifacts/fact-plane.v1.json candidateSchema.transportRepresentation, relationPayloadSchemaRegistryV1 (canonicalPayloadEncoding,
    sharedTypes, schemas), relationRegistry, negativeFixtures keys
  artifacts/rust-provider-protocol.v2.json FactBatchV2, AnalyzeV2, StageRequestV2, FactCandidateV1.wireAdjustment, maxFactBatchCandidates
  artifacts/delivery.v2.json AnalyzeV1 (analysisOrdinal exactly 0), StageRequestV1 (stageId text; stageOrdinal contiguous)

The check order is this reconstruction's own; the kit publishes no order for this entry. The order is: selection, payload schema,
dispatch observation, dispatch/Plan joins, request/batch correlation, exact payload bytes, candidate registry admission, companion joins.
Every check runs without short-circuit, so firstRefusal is the first listed violation and the full list shows what it masks.

Each internal key records how it was bound:
  kit-text  a kit sentence names the key for this check;
  key-name  the check is the one the published key name denotes;
  cb24      no published key exists (advisory A-c1).

source44 (HC-57): when target-attribution-v2 is not negotiated, the historical payload is per language (native-evidence s9.1 lines 2801-2810,
s9.4 lines 2986-2990; fact-batch.schema.v3.json#/x-opensip-negotiation/whenAbsent; native/provider-handshake.schemas.v1.json
#/x-opensip-wire-law/factBatch and #/x-opensip-wire-law/commitments):
  - typescript-semantic: delivery.v2 FactBatchV1 {analysisOrdinal, stageId, batchIndex, facts, batchCommitment}, JSON vector
    TypeScriptFactBatchV1Vector, batchCommitment = sha256(UTF8(opensip.ts-provider.fact-batch.v1) || 0x00 || deterministic-CBOR(wire facts));
  - rust-semantic: rust-provider-protocol.v2 FactBatchV2, JSON vector RustFactBatchV2Vector.
The source42.v3/source43 helper applied FactBatchV2 to both languages (reading A-s42v3-1). That reading is withdrawn: the source44 bytes decide the other
way. The exchange runner moved to ref/provider_exchange.py; the source43 bytes of this file are preserved at preserved/s43-final/ref/factbatch.py.
"""
import copy
import hashlib
import inspect
import re
import unicodedata

import schemas
import wirecbor as WC

TOKEN = "target-attribution-v2"
FB3 = "native/fact-batch.schema.v3.json"
OCC = "native/occupancy-companion.schema.v1.json"
DISP = "native/dispatch-binding.schema.v1.json"
RET = "foundation/provider-target-attribution-return.schema.v2.json"
TA2 = "foundation/target-attribution.schema.v2.json"
ROUTES_DOC = "foundation/evaluator-fault-observation.schema.v3.json"
PROJ_DOC = "foundation/evaluator-projection-registry.v1.json"
FACT_PLANE = "coop/artifacts/fact-plane.v1.json"
RUST = "coop/artifacts/rust-provider-protocol.v2.json"
DELIVERY = "coop/artifacts/delivery.v2.json"
HS = "native/provider-handshake.schemas.v1.json"
HISTORICAL_VECTOR = {"ts": "#/$defs/TypeScriptFactBatchV1Vector", "rust": "#/$defs/RustFactBatchV2Vector"}
HISTORICAL_NAME = {"ts": "FactBatchV1", "rust": "FactBatchV2"}
HISTORICAL_ARRAY = {"ts": "facts", "rust": "candidates"}


def find_any(node, name, path="#"):
    """First value stored under key `name` in document order (depth-first), with its JSON pointer."""
    if isinstance(node, dict):
        if name in node:
            return path + "/" + name, node[name]
        for k, v in node.items():
            r = find_any(v, name, path + "/" + k)
            if r:
                return r
    elif isinstance(node, list):
        for i, v in enumerate(node):
            r = find_any(v, name, f"{path}/{i}")
            if r:
                return r
    return None


class PayloadKit(schemas.Kit):
    """HC-51. ref/schemas.py enforces only the identity section 3 x-opensip-order vocabulary. occupancy-companion.schema.v1.json
    publishes one more array-order token, candidateOrdinal, in #/x-opensip-order-vocabulary. It is used by FactBatchV3.candidates
    and FactBatchV3.occupancyCompanions, and no other kit schema uses it. For that token the unchanged Kit refuses
    ORDER_ANNOTATION_UNKNOWN on every lawful FactBatchV3. The published law is: integer, unique and strictly increasing; gaps
    lawful; empty admits; reverse, duplicate and non-integer refuse. This subclass adds exactly that token and leaves ref/schemas.py
    byte-unchanged for every earlier execution."""

    def __init__(self, base):
        self.__dict__.update(base.__dict__)
        vocab = self.doc(OCC)["x-opensip-order-vocabulary"]
        law = vocab["candidateOrdinal"]["law"]
        assert "unique strictly increasing" in law and "Gaps are lawful" in law, law
        self.published_tokens = {k: OCC + "#/x-opensip-order-vocabulary/" + k for k in vocab}

    def _check_order(self, ann, arr, path, viol):
        if isinstance(ann, str) and ann in self.published_tokens:
            prev = None
            for i, it in enumerate(arr):
                v = it.get(ann) if isinstance(it, dict) else None
                if type(v) is not int:
                    viol.append({"path": path, "order": ann, "violation": f"ORDER_KEY_NOT_INTEGER_AT:{i}"})
                    return
                if prev is not None and v <= prev:
                    viol.append({"path": path, "order": ann, "violation": f"ORDER_OR_DUPLICATE_AT:{i}"})
                    return
                prev = v
            return
        return super()._check_order(ann, arr, path, viol)


BASE = schemas.kit()
K = PayloadKit(BASE)

FP = K.doc(FACT_PLANE)
REG_PATH, REG = find_any(FP, "relationPayloadSchemaRegistryV1")
RELREG_PATH, RELREG = find_any(FP, "relationRegistry")
CAND_PATH, CAND_SCHEMA = find_any(FP, "candidateSchema")
ENC = REG["canonicalPayloadEncoding"]
_, FP_NEGATIVES = find_any(FP, "negativeFixtures")
_, FP_VECTORS = find_any(FP, "vectors")
PROJ = K.doc(PROJ_DOC)["relations"]
assert isinstance(PROJ, dict) and "imports" in PROJ and "targetNativeIdField" in PROJ["imports"]
V2_PATH, V2_SPEC = find_any(K.doc(RUST), "FactBatchV2")
_, RUST_CAND = find_any(K.doc(RUST), "FactCandidateV1")
_, MAX_FB = find_any(K.doc(RUST), "maxFactBatchCandidates")
_, TS_ANALYZE = find_any(K.doc(DELIVERY), "AnalyzeV1")
_, TS_FB1 = find_any(K.doc(DELIVERY), "FactBatchV1")
ROUTES = K.doc(ROUTES_DOC)["x-opensip-routes"]
RETLAW = K.doc(RET)
PUBLISHED_KEYS = (set(RETLAW["x-opensip-new-internal-faults"]["schemaKeys"]) | set(RETLAW["x-opensip-new-internal-faults"]["joinKeys"])
                  | set(K.doc(TA2)["x-opensip-new-internal-faults"]["keys"]) | {n["expected"] for n in FP_NEGATIVES})

# fact-plane canonicalPayloadEncoding: the decoder below maps every forbidden item to one refusal class. An unmapped kit item raises at import.
PROFILE_TYPES = {"null", "false", "true", "uint64", "NFC UTF-8 text", "definite array", "definite text-keyed map"}
PROFILE_FORBIDDEN = {"negative integers": "negative-integer", "floating point": "float", "byte strings inside relation payloads": "byte-string",
                     "tags": "tag", "indefinite lengths": "indefinite-length", "duplicate keys": "duplicate-key", "non-NFC text": "non-nfc-text",
                     "unknown fields": "relation payload schema (FACT_RELATION_PAYLOAD_INVALID), not a CBOR decode class"}
assert "deterministic CBOR" in ENC["standard"] and set(ENC["types"]) == PROFILE_TYPES and set(ENC["forbidden"]) == set(PROFILE_FORBIDDEN), ENC
assert "ascending unsigned lexicographic" in ENC["mapOrder"] and "re-encode" in ENC["admission"]
assert set(V2_SPEC["required"]) == {"analysisOrdinal", "stageId", "batchIndex", "candidates"} and V2_SPEC["optional"] == [] and V2_SPEC["closed"] is True
assert RUST_CAND.get("wireAdjustment") == "canonicalRelationPayload is a byte string"
assert "deterministic-CBOR" in CAND_SCHEMA["transportRepresentation"] and "canonicalRelationPayloadHex" in CAND_SCHEMA["transportRepresentation"]
TS_WIRE = K.doc(DELIVERY)["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]
FACT_BATCH_DOMAIN = TS_WIRE["commitments"]["domains"]["factBatch"]
assert TS_WIRE["commitments"]["domainRule"].startswith("Each commitment is SHA-256(UTF8(domain) || 0x00 || deterministic-CBOR(value))")
assert FACT_BATCH_DOMAIN == "opensip.ts-provider.fact-batch.v1"
assert "delivery.v2 FactBatchV1" in K.doc(FB3)["x-opensip-negotiation"]["whenAbsent"]


# ------------------------------------------------------------------------------------------------ deterministic CBOR (restricted)
class CborError(Exception):
    def __init__(self, cls, at=None):
        super().__init__(cls if at is None else f"{cls}@{at}")
        self.cls = cls


def cbor_encode(value):
    out = bytearray()
    _enc(value, out)
    return bytes(out)


def _head(major, n, out):
    if n < 24:
        out.append((major << 5) | n)
    elif n < 0x100:
        out += bytes([(major << 5) | 24, n])
    elif n < 0x10000:
        out.append((major << 5) | 25)
        out += n.to_bytes(2, "big")
    elif n < 0x100000000:
        out.append((major << 5) | 26)
        out += n.to_bytes(4, "big")
    elif n < 0x10000000000000000:
        out.append((major << 5) | 27)
        out += n.to_bytes(8, "big")
    else:
        raise CborError("uint64-range")


def _enc(v, out):
    if v is None:
        out.append(0xf6)
    elif v is False:
        out.append(0xf4)
    elif v is True:
        out.append(0xf5)
    elif type(v) is int:
        if v < 0:
            raise CborError("negative-integer")
        _head(0, v, out)
    elif type(v) is float:
        raise CborError("float")
    elif type(v) in (bytes, bytearray):
        raise CborError("byte-string")
    elif type(v) is str:
        try:
            b = v.encode("utf-8")
        except UnicodeEncodeError:
            raise CborError("malformed-utf8")
        if not unicodedata.is_normalized("NFC", v):
            raise CborError("non-nfc-text")
        _head(3, len(b), out)
        out += b
    elif type(v) is list:
        _head(4, len(v), out)
        for x in v:
            _enc(x, out)
    elif type(v) is dict:
        items = []
        for k, x in v.items():
            if type(k) is not str:
                raise CborError("non-text-key")
            items.append((cbor_encode(k), x))
        items.sort(key=lambda t: t[0])
        _head(5, len(items), out)
        for kb, x in items:
            out += kb
            _enc(x, out)
    else:
        raise CborError("unsupported-type:" + type(v).__name__)


def cbor_decode(data):
    data = bytes(data)
    value, i = _dec(data, 0, 0)
    if i != len(data):
        raise CborError("trailing-bytes", i)
    return value


def _need(data, i, n):
    if i + n > len(data):
        raise CborError("truncated", i)


def _dec(data, i, depth):
    if depth > 64:
        raise CborError("depth", i)
    _need(data, i, 1)
    ib = data[i]
    major, ai = ib >> 5, ib & 0x1f
    if major == 7:
        if ai in (20, 21, 22):
            return {20: False, 21: True, 22: None}[ai], i + 1
        if ai in (25, 26, 27):
            raise CborError("float", i)
        if ai == 31:
            raise CborError("indefinite-length", i)
        raise CborError("simple-value", i)
    if major == 6:
        raise CborError("tag", i)
    if major == 1:
        raise CborError("negative-integer", i)
    if ai == 31:
        raise CborError("indefinite-length", i)
    if ai > 27:
        raise CborError("reserved-additional-information", i)
    start = i
    i += 1
    if ai < 24:
        arg = ai
    else:
        n = {24: 1, 25: 2, 26: 4, 27: 8}[ai]
        _need(data, i, n)
        arg = int.from_bytes(data[i:i + n], "big")
        i += n
        if arg < {24: 24, 25: 0x100, 26: 0x10000, 27: 0x100000000}[ai]:
            raise CborError("non-shortest-argument", start)
    if major == 0:
        return arg, i
    if major == 2:
        raise CborError("byte-string", start)
    if major == 3:
        _need(data, i, arg)
        try:
            s = data[i:i + arg].decode("utf-8", errors="strict")
        except UnicodeDecodeError:
            raise CborError("malformed-utf8", start)
        if not unicodedata.is_normalized("NFC", s):
            raise CborError("non-nfc-text", start)
        return s, i + arg
    if major == 4:
        out = []
        for _ in range(arg):
            v, i = _dec(data, i, depth + 1)
            out.append(v)
        return out, i
    out, prev = {}, None
    for _ in range(arg):
        _need(data, i, 1)
        if data[i] >> 5 != 3:
            raise CborError("non-text-key", i)
        ks = i
        k, i = _dec(data, i, depth + 1)
        kb = data[ks:i]
        if prev is not None and kb == prev:
            raise CborError("duplicate-key", ks)
        if prev is not None and kb < prev:
            raise CborError("map-key-order", ks)
        prev = kb
        v, i = _dec(data, i, depth + 1)
        out[k] = v
    return out, i


def same(a, b):
    """Typed structural equality (bool is not int)."""
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(same(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))
    return a == b


# ------------------------------------------------------------------------------------------------ relation payload registry (fact-plane)
_C0C1 = re.compile("[\x00-\x1f\x7f-\x9f]")


def _canonical_text(v):
    return type(v) is str and v != "" and unicodedata.is_normalized("NFC", v) and not _C0C1.search(v)


def _canonical_path(v):
    return (_canonical_text(v) and not v.startswith("/") and "\\" not in v
            and all(seg not in ("", ".", "..") for seg in v.split("/")))


TYPE_CHECK = {"CanonicalText": _canonical_text, "CanonicalPath": _canonical_path,
              "SubjectIdV1": lambda v: _canonical_text(v) and re.fullmatch(r"[a-z]+:.+", v, re.S) is not None,
              "DigestHex": lambda v: type(v) is str and re.fullmatch(r"[0-9a-f]{64}", v) is not None,
              "Sha256Text": lambda v: type(v) is str and re.fullmatch(r"sha256:[0-9a-f]{64}", v) is not None,
              "UInt64": lambda v: type(v) is int and 0 <= v <= 0xFFFFFFFFFFFFFFFF}
assert set(TYPE_CHECK) == set(REG["sharedTypes"]), sorted(REG["sharedTypes"])


def payload_schema_faults(relation, resolution, payload):
    s = REG["schemas"][relation]
    if type(payload) is not dict:
        return ["not-a-map"]
    faults = []
    allowed = set(s["required"]) | set(s["optional"])
    faults += [f"unknown-field:{k}" for k in payload if k not in allowed]
    faults += [f"missing-field:{k}" for k in s["required"] if k not in payload]
    for k, v in payload.items():
        t = s["fields"].get(k)
        if t is None:
            continue
        ok = (type(v) is str and v in s["enums"][t]) if t in s.get("enums", {}) else TYPE_CHECK[t](v)
        if not ok:
            faults.append(f"type:{k}:{t}")
    rule = s.get("resolutionRules", {}).get(resolution)
    if rule:
        faults += [f"rung-required:{k}" for k in rule["required"] if k not in payload]
        faults += [f"rung-forbidden:{k}" for k in rule["forbidden"] if k in payload]
    return faults


# ------------------------------------------------------------------------------------------------ keys and routes
KIT_TEXT_KEYS = {
    "PROVIDER_RETURN_DISPATCH": "native-evidence.md s9.6 line 2931; " + RET + "#/x-opensip-return-law/invocation/inputs/dispatch",
    "PROVIDER_RETURN_UNKNOWN_CANDIDATE": OCC + "#/x-opensip-order-vocabulary/candidateOrdinal/semanticJoin",
    "PROVIDER_RETURN_UNNEGOTIATED_V3": RET + "#/x-opensip-return-law/invocation/inputs/batch ('V3 without token refuses'); key in #/x-opensip-new-internal-faults/joinKeys",
    "FACT_RELATION_UNKNOWN": FACT_PLANE + " negativeFixtures reject-unknown-relation",
    "FACT_RELATION_SCHEMA_MISMATCH": FACT_PLANE + " negativeFixtures reject-schema-version-mismatch, reject-relation-schema-cross-wire",
    "FACT_RELATION_PAYLOAD_INVALID": FACT_PLANE + " negativeFixtures reject-payload-unknown-field, reject-payload-malformed-field",
    "FACT_SOURCE_UNIVERSE_MISMATCH": FACT_PLANE + " negativeFixtures reject-source-universe-substitution",
    "FACT_TARGET_UNIVERSE_NOT_ADMITTED": FACT_PLANE + " negativeFixtures reject-target-outside-admitted-domain",
    "FACT_TARGET_UNIVERSE_MISMATCH": FACT_PLANE + " negativeFixtures reject-same-only-cross-universe"}


def key_binding(key):
    if key in KIT_TEXT_KEYS:
        return {"binding": "kit-text", "selector": KIT_TEXT_KEYS[key]}
    if key.startswith("cb24."):
        return {"binding": "cb24", "selector": None}
    if key not in PUBLISHED_KEYS:
        raise KeyError(f"reconstruction used an unpublished non-cb24 key {key}")
    return {"binding": "key-name", "selector": "published internal key list (" + RET + ", " + TA2 + ")"}


def violation(key, cls, origin, detail):
    return {"key": key, "class": cls, "origin": origin, "detail": detail, **key_binding(key)}


def public_route(v):
    cond = "input-schema-invalid" if v["class"] == "schema" else "input-join-invalid"
    rk = f"{cond}:{v['origin']}"
    r = ROUTES[rk]
    return {"routeKey": rk, "termination": r["termination"], "detail": r["detail"], "selector": ROUTES_DOC + "#/x-opensip-routes/" + rk}


def _summary(r):
    parts = []
    if r.get("typed"):
        parts.append("typed " + r["typed"])
    parts += [f"{e['path']} {e['keyword']}: {e['message'][:140]}" for e in r.get("stock", [])[:4]]
    parts += [f"order {o['path']} {o['violation']}" for o in r.get("order", [])]
    return "; ".join(parts)


# ------------------------------------------------------------------------------------------------ requests, Plan fragment, dispatch
def negotiated(hello_caps, ack_caps):
    return TOKEN in (hello_caps or []) and TOKEN in (ack_caps or [])


def stage_request(analyze, shape, index):
    if shape == "ts":
        r = analyze["stageRequests"][index]
        return {"stageId": r["stageId"], "stageOrdinal": r["stageOrdinal"], "relations": r["relations"], "analysisOrdinal": analyze["analysisOrdinal"],
                "selector": DELIVERY + " AnalyzeV1.stageRequests[].StageRequestV1.stageId/stageOrdinal"}
    r = analyze["stages"][index]
    return {"stageId": r["planStage"]["stageId"], "stageOrdinal": r["stageOrdinal"], "relations": r["planStage"]["relations"],
            "analysisOrdinal": analyze["analysisOrdinal"], "selector": RUST + " AnalyzeV2.stages[].StageRequestV2.planStage.stageId/stageOrdinal"}


def analyze_request_faults(analyze, shape, retained, stage_count):
    faults = []
    reqs = analyze.get("stageRequests" if shape == "ts" else "stages", [])
    if shape == "ts" and analyze.get("analysisOrdinal") != 0:
        faults.append("AnalyzeV1.analysisOrdinal is not exactly 0 (delivery.v2 AnalyzeV1.fields.analysisOrdinal)")
    if len(reqs) != stage_count:
        faults.append(f"stageCount {stage_count} != {len(reqs)} stage requests")
    ids = []
    for i in range(len(reqs)):
        r = stage_request(analyze, shape, i)
        if r["stageOrdinal"] != i:
            faults.append(f"request {i}: stageOrdinal {r['stageOrdinal']} is not contiguous Analyze order")
        ids.append(r["stageId"])
        if sum(1 for s in retained["executionPlan"]["stages"] if retained["stageSpecs"][s["stageSpecDigest"]]["stageId"] == r["stageId"]) != 1:
            faults.append(f"request {i}: stageId {r['stageId']!r} names no unique retained Plan stage")
    if len(set(ids)) != len(ids):
        faults.append("duplicate requested stageId")
    return faults


def derive_dispatch(retained, request, stream):
    """Host TCB observation at Analyze dispatch for the current requested stage (dispatch-binding.schema.v1.json)."""
    rows = [s for s in retained["executionPlan"]["stages"] if retained["stageSpecs"][s["stageSpecDigest"]]["stageId"] == request["stageId"]]
    if len(rows) != 1:
        raise ValueError(f"requested stage {request['stageId']!r} is not exactly one retained Plan stage")
    row = rows[0]
    spec = retained["stageSpecs"][row["stageSpecDigest"]]
    cur = stream.get(request["stageId"], {"nextBatchIndex": 0, "nextCandidateOrdinal": 0})
    return {"schemaVersion": 1, "planId": retained["planId"], "retainedStageOrdinal": row["ordinal"], "analyzeRequestOrdinal": request["stageOrdinal"],
            "expectedStageId": request["stageId"], "expectedAnalysisOrdinal": request["analysisOrdinal"],
            "expectedBatchIndex": cur["nextBatchIndex"], "expectedFirstCandidateOrdinal": cur["nextCandidateOrdinal"],
            "producerClosure": spec["producerClosure"], "stageSpecDigest": row["stageSpecDigest"]}


def advance(stream, batch):
    arr = batch["candidates"] if "candidates" in batch else batch["facts"]
    stream[batch["stageId"]] = {"nextBatchIndex": batch["batchIndex"] + 1, "nextCandidateOrdinal": arr[-1]["candidateOrdinal"] + 1}


def dispatch_plan_faults(d, retained):
    out = []
    if d.get("planId") != retained["planId"] or d.get("planId") != retained["executionPlan"]["planId"]:
        out.append(violation("PROVIDER_RETURN_PLAN_MISMATCH", "join", "host-internal", "dispatch.planId != retained Plan / execution-plan planId"))
    row = next((s for s in retained["executionPlan"]["stages"] if same(s["ordinal"], d.get("retainedStageOrdinal"))), None)
    if row is None:
        out.append(violation("PROVIDER_RETURN_STAGE_NOT_IN_PLAN", "join", "host-internal", f"no execution-plan stage at retainedStageOrdinal {d.get('retainedStageOrdinal')!r}"))
    elif row["stageSpecDigest"] != d.get("stageSpecDigest"):
        out.append(violation("PROVIDER_RETURN_STAGE_SPEC", "join", "host-internal",
                             f"execution-plan.stages[{row['ordinal']}].stageSpecDigest != dispatch.stageSpecDigest (lookup is by retainedStageOrdinal)"))
    spec = retained["stageSpecs"].get(d.get("stageSpecDigest"))
    if spec is None:
        out.append(violation("PROVIDER_RETURN_STAGE_SPEC", "join", "host-internal", "no retained stage spec at dispatch.stageSpecDigest"))
    else:
        if spec["planId"] != d.get("planId"):
            out.append(violation("PROVIDER_RETURN_PLAN_MISMATCH", "join", "host-internal", "stage-spec planId != dispatch.planId"))
        if spec["stageId"] != d.get("expectedStageId"):
            out.append(violation("PROVIDER_RETURN_STAGE_SPEC", "join", "host-internal", "stage-spec stageId != dispatch.expectedStageId"))
        if spec["producerClosure"] != d.get("producerClosure"):
            out.append(violation("PROVIDER_RETURN_STAGE_PRODUCER", "join", "host-internal", "stage-spec producerClosure != dispatch.producerClosure"))
        elif retained["closures"].get(spec["producerClosure"], {}).get("kind") != "provider":
            out.append(violation("PROVIDER_RETURN_PRODUCER_NOT_PROVIDER", "join", "host-internal", "closures[producerClosure].kind != provider"))
    return out


def dispatch_request_faults(d, request):
    diffs = [f"{a} {d.get(a)!r} != request {b} {request[b]!r}" for a, b in
             (("expectedStageId", "stageId"), ("analyzeRequestOrdinal", "stageOrdinal"), ("expectedAnalysisOrdinal", "analysisOrdinal"))
             if not same(d.get(a), request[b])]
    return [violation("cb24.DISPATCH_REQUEST_MISMATCH", "join", "host-internal", "; ".join(diffs))] if diffs else []


# ------------------------------------------------------------------------------------------------ payload checks
def wire_candidate(c):
    """native/provider-handshake.schemas.v1.json#/x-opensip-wire-law/candidateCborProjection: the wire FactCandidateV1 drops decodedRelationPayload and carries
    canonicalRelationPayload = bytes(canonicalRelationPayloadHex)."""
    w = {k: v for k, v in c.items() if k not in ("canonicalRelationPayloadHex", "decodedRelationPayload")}
    w["canonicalRelationPayload"] = bytes.fromhex(c["canonicalRelationPayloadHex"])
    return w


def ts_batch_commitment(facts):
    body = WC.encode([wire_candidate(c) for c in facts], allow_negative=True)
    return "sha256:" + hashlib.sha256(FACT_BATCH_DOMAIN.encode("utf-8") + b"\x00" + body).hexdigest()


def admit_historical(p, language):
    """Token-absent historical payload of the negotiating language, admitted as the published JSON vector (provider-handshake.schemas.v1.json). For
    typescript-semantic the batchCommitment is recomputed over the wire FactCandidateV1 array."""
    sel = HISTORICAL_VECTOR[language]
    r = K.admit(p, HS, sel)
    out = {"ok": r["ok"], "document": HS, "selector": sel, "typed": r["typed"], "stock": r["stock"][:8], "order": r["order"],
           "faults": [] if r["ok"] else [_summary(r)], "recomputedBatchCommitment": None}
    if language == "ts" and isinstance(p, dict) and isinstance(p.get("facts"), list) and p["facts"]:
        try:
            out["recomputedBatchCommitment"] = ts_batch_commitment(p["facts"])
        except (WC.WireCborError, ValueError, TypeError, KeyError, AttributeError) as exc:
            out["recomputedBatchCommitment"] = f"not computable: {type(exc).__name__}: {exc}"
    return out


def payload_bytes(c):
    hx, dec = c.get("canonicalRelationPayloadHex"), c.get("decodedRelationPayload")
    rec = {"candidateOrdinal": c.get("candidateOrdinal"), "hex": hx}
    if type(hx) is not str or not re.fullmatch(r"(?:[0-9a-fA-F]{2})+", hx):
        return rec, ["canonicalRelationPayloadHex does not transcribe a byte string"]
    b = bytes.fromhex(hx)
    rec.update(byteLength=len(b), sha256=hashlib.sha256(b).hexdigest())
    faults = []
    try:
        decoded = cbor_decode(b)
        rec["decodeOnce"] = "ok"
    except CborError as exc:
        rec["decodeOnce"] = str(exc)
        faults.append(f"payload bytes are not restricted deterministic CBOR: {exc}")
        decoded = None
    if decoded is not None and not same(decoded, dec):
        faults.append("decoded bytes differ from decodedRelationPayload")
    try:
        re_bytes = cbor_encode(dec)
        rec["reencodedHexEqual"] = re_bytes == b
        if re_bytes != b:
            faults.append("deterministic_cbor(decodedRelationPayload) != canonicalRelationPayload bytes")
    except CborError as exc:
        rec["reencodedHexEqual"] = False
        faults.append(f"decodedRelationPayload is not encodable under the profile: {exc}")
    return rec, faults


def candidate_registry_faults(c, host, request):
    out = []
    rel = c.get("relation")
    if rel not in REG["schemas"] or rel not in RELREG["relations"]:
        return [violation("FACT_RELATION_UNKNOWN", "schema", "provider-return", f"relation {rel!r}")]
    s, rr = REG["schemas"][rel], RELREG["relations"][rel]
    if not same(c.get("relationSchemaId"), s["schemaId"]) or not same(c.get("schemaVersion"), s["schemaVersion"]):
        out.append(violation("FACT_RELATION_SCHEMA_MISMATCH", "join", "provider-return", f"{c.get('relationSchemaId')!r}/{c.get('schemaVersion')!r}"))
    if c.get("layer") != rr["layer"]:
        out.append(violation("cb24.FACT_LAYER_MISMATCH", "join", "provider-return", f"layer {c.get('layer')!r} != {rr['layer']}"))
    if c.get("resolution") not in rr["ladder"]:
        out.append(violation("cb24.FACT_RESOLUTION_NOT_ON_LADDER", "join", "provider-return", f"resolution {c.get('resolution')!r}"))
    if rel not in request["relations"]:
        out.append(violation("cb24.FACT_RELATION_NOT_REQUESTED", "join", "provider-return", f"{rel} not requested by stage {request['stageId']}"))
    if (c.get("producer"), c.get("producerVersion"), c.get("language")) != (host["providerId"], host["providerVersion"], host["language"]):
        out.append(violation("cb24.FACT_PRODUCER_CONTEXT", "join", "provider-return", "producer/producerVersion/language != admitted host context"))
    if c.get("sourceUniverseId") != host["sourceUniverseId"]:
        out.append(violation("FACT_SOURCE_UNIVERSE_MISMATCH", "join", "provider-return", "sourceUniverseId"))
    if c.get("targetUniverseId") not in host["allowedTargetUniverseIds"]:
        out.append(violation("FACT_TARGET_UNIVERSE_NOT_ADMITTED", "join", "provider-return", "targetUniverseId"))
    elif s["universeRule"] == "same-only" and c.get("targetUniverseId") != c.get("sourceUniverseId"):
        out.append(violation("FACT_TARGET_UNIVERSE_MISMATCH", "join", "provider-return", "same-only relation crosses universes"))
    pf = payload_schema_faults(rel, c.get("resolution"), c.get("decodedRelationPayload"))
    if pf:
        out.append(violation("FACT_RELATION_PAYLOAD_INVALID", "schema", "provider-return", f"candidate {c.get('candidateOrdinal')!r}: {pf}"))
    return out


def target_field(relation, resolution):
    pr = PROJ.get(relation)
    if pr is None:
        return None, False
    f = pr.get("targetNativeIdField")
    if isinstance(f, dict):
        f = f.get(resolution)
    if not f:
        return None, False
    return f, resolution in pr.get("endpointTargetRungs", pr.get("ladder", []))


# ------------------------------------------------------------------------------------------------ the ANALYZING entry
def buffer_fact_batch_occupancy(payload, hello_caps, ack_caps, dispatch, retained, request, host, language):
    """Host ANALYZING entry. Receipts and views are deliberately not parameters (s9.6 Timing; return-law invocation.when)."""
    neg = negotiated(hello_caps, ack_caps)
    pfx = "PROVIDER_RETURN_" if neg else f"cb24.FACT_BATCH_{HISTORICAL_NAME[language][-2:]}_"
    array_key = "candidates" if neg else HISTORICAL_ARRAY[language]
    V = []
    schema = None
    v3_shaped = isinstance(payload, dict) and ("schemaVersion" in payload or "occupancyCompanions" in payload)
    if not neg and v3_shaped:
        V.append(violation("PROVIDER_RETURN_UNNEGOTIATED_V3", "join", "provider-return",
                           "target-attribution-v2 not on both Hello and HelloAck, payload carries FactBatchV3 members "
                           + str(sorted(k for k in ("schemaVersion", "occupancyCompanions") if k in payload))))
    elif neg:
        r = K.admit(payload, FB3, "#")
        schema = {"document": FB3, "ok": r["ok"], "typed": r["typed"], "stock": r["stock"][:8], "order": r["order"]}
        if not r["ok"]:
            V.append(violation("PROVIDER_RETURN_SCHEMA", "schema", "provider-return", _summary(r)))
    else:
        schema = admit_historical(payload, language)
        if not schema["ok"]:
            V.append(violation(pfx + "SCHEMA", "schema", "provider-return", "; ".join(schema["faults"][:6])))
        recomputed = schema["recomputedBatchCommitment"]
        if language == "ts" and isinstance(payload, dict) and recomputed is not None and not same(recomputed, payload.get("batchCommitment")):
            V.append(violation(pfx + "BATCH_COMMITMENT", "join", "provider-return",
                               f"batchCommitment {payload.get('batchCommitment')!r} != recomputed {recomputed!r} (delivery.v2 commitments.domains.factBatch)"))
    batch = payload if isinstance(payload, dict) else {}
    cands = [c for c in batch[array_key] if isinstance(c, dict)] if isinstance(batch.get(array_key), list) else []

    dispatch_schema = None
    if dispatch is None:
        V.append(violation("PROVIDER_RETURN_DISPATCH" if neg else pfx + "CORRELATION_UNOBSERVED", "join", "host-internal",
                           "no DispatchBindingV1 host observation supplied"))
    else:
        d = K.admit(dispatch, DISP, "#")
        dispatch_schema = {"document": DISP, "ok": d["ok"], "stock": d["stock"][:4]}
        if not d["ok"]:
            V.append(violation("cb24.DISPATCH_BINDING_SCHEMA", "schema", "host-internal", _summary(d)))
        if neg:
            V += dispatch_plan_faults(dispatch, retained)
        V += dispatch_request_faults(dispatch, request)
        for field, exp, key in (("stageId", "expectedStageId", "STAGE_ID"), ("analysisOrdinal", "expectedAnalysisOrdinal", "ANALYSIS_ORDINAL"),
                                ("batchIndex", "expectedBatchIndex", "BATCH_INDEX")):
            if not same(batch.get(field), dispatch.get(exp)):
                V.append(violation(pfx + key, "join", "provider-return", f"batch.{field} {batch.get(field)!r} != dispatch.{exp} {dispatch.get(exp)!r}"))
        first = dispatch.get("expectedFirstCandidateOrdinal")
        ords = [c.get("candidateOrdinal") for c in cands]
        if cands and type(first) is int and not same(ords, list(range(first, first + len(ords)))):
            V.append(violation(pfx + "CANDIDATE_STREAM", "join", "provider-return",
                               f"candidate ordinals {ords[:8]} are not the contiguous stream from expectedFirstCandidateOrdinal {first}"))

    exact = []
    for c in cands:
        rec, faults = payload_bytes(c)
        exact.append(rec)
        for f in faults:
            V.append(violation(pfx + "PAYLOAD_CBOR", "join", "provider-return", f"candidate {c.get('candidateOrdinal')!r}: {f}"))
    for c in cands:
        V += candidate_registry_faults(c, host, request)

    comps = batch.get("occupancyCompanions") if neg and isinstance(batch.get("occupancyCompanions"), list) else []
    by_ord = {}
    for c in cands:
        if type(c.get("candidateOrdinal")) is int:
            by_ord.setdefault(c["candidateOrdinal"], c)  # first occurrence; a duplicate ordinal is already refused by the order token
    for comp in comps:
        if not isinstance(comp, dict):
            continue
        o = comp.get("candidateOrdinal")
        if type(o) is not int or o not in by_ord:
            V.append(violation("PROVIDER_RETURN_UNKNOWN_CANDIDATE", "join", "provider-return", f"companion candidateOrdinal {o!r} names no candidate in this batch"))
            continue
        c = by_ord[o]
        if comp.get("targetUniverseId") != c.get("targetUniverseId"):
            V.append(violation("PROVIDER_RETURN_UNIVERSE_MISMATCH", "join", "provider-return", f"companion {o}: targetUniverseId is not byte-equal to the candidate's"))
        field, on_rung = target_field(c.get("relation"), c.get("resolution"))
        if field is None or not on_rung:
            V.append(violation("TARGET_ATTRIBUTION_FIELD_NOT_ON_RUNG", "join", "provider-return",
                               f"companion {o}: {c.get('relation')}@{c.get('resolution')} has no targetNativeIdField at that rung"))
        else:
            dec = c.get("decodedRelationPayload")
            if not isinstance(dec, dict) or not same(dec.get(field), comp.get("targetNativeId")):
                V.append(violation("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH", "join", "provider-return",
                                   f"companion {o}: targetNativeId {comp.get('targetNativeId')!r} != decoded payload {field} {dec.get(field) if isinstance(dec, dict) else None!r}"))

    first_v = V[0] if V else None
    if V:
        occupancy = "none captured: atomic refusal of this batch"
    elif neg:
        occupancy = f"{len(comps)} companion(s) buffered; unlisted candidates occupancy-unknown except exact-id ephemeral"
    else:
        occupancy = f"omitted: token absent (historical {HISTORICAL_NAME[language]}); occupancy unknown except exact-id ephemeral"
    return {"entry": "buffer_fact_batch_occupancy", "negotiated": neg, "language": language,
            "selectedPayload": "FactBatchV3" if neg else HISTORICAL_NAME[language],
            "result": "REFUSE" if V else "ADMIT", "firstRefusal": first_v["key"] if first_v else None,
            "violationKeys": list(dict.fromkeys(v["key"] for v in V)), "violations": V,
            "publicRoute": public_route(first_v) if first_v else None, "payloadSchema": schema, "dispatch": dispatch, "dispatchSchema": dispatch_schema,
            "exactBytes": exact, "bufferedCompanions": copy.deepcopy(comps) if not V else [], "occupancy": occupancy}


BUFFER_PARAMETERS = list(inspect.signature(buffer_fact_batch_occupancy).parameters)
# The source43 PayloadExchange (Rust protocol3 table for both languages, FactBatch payloads only) is superseded by ref/provider_exchange.py (HC-58).
