"""Provider handshake and FactBatch wire reference v1 (design evidence only).

Standing: PROPOSED reference for native-evidence sections 9.1, 9.3, 9.4 and 9.6. It validates the
JSON-vector form of typescript-semantic major-2 and rust-semantic major-3 Hello / HelloAck and of
historical-versus-negotiated FactBatch payloads against native/provider-handshake.schemas.v1.json and
native/fact-batch.schema.v3.json, and it executes the cross-record joins a stock schema cannot
express: provider/runtime descriptor digests and descriptor-field echoes, Rust expected-identity
echoes, the selected inherited contract digest, token-array and identityVersions echoes, per-language
limit maps with deterministic-CBOR byte equality, the candidate CBOR projection and the TypeScript
per-batch commitment.

Scope limits. It frames nothing (no length prefix, frame digest or sequence number), runs no worker,
host process or compiler, validates no relation payload grammar or anchor (fact-plane admission owns
those) and qualifies nothing. Descriptor digests hash foundation canonical.py bytes, which equal
RFC 8785 for the integer/string value domain the fixtures use. This module carries a bytes-bearing
CBOR encoder for wire maps only because the fact-plane relation-payload encoder it reuses has no byte
string case; heads are the fact-plane `_cbor_head`. The occupancy entries of
foundation/provider_attribution_return_model.v2.py decide occupancy capture only; they are not
historical-payload validation and this module does not replace them.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import unicodedata
from pathlib import Path

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

HERE = Path(__file__).resolve().parent
CORRECTIONS = HERE.parent
REPO = HERE.parents[3]
ARTIFACTS = REPO / "docs" / "coop" / "artifacts"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


C = _load("wire_canonical", CORRECTIONS / "foundation" / "canonical.py")
FP = _load("wire_fact_plane", ARTIFACTS / "check-fact-plane.py")

HANDSHAKE = json.loads((HERE / "provider-handshake.schemas.v1.json").read_text(encoding="utf-8"))
FACT_BATCH_V3 = json.loads((HERE / "fact-batch.schema.v3.json").read_text(encoding="utf-8"))
COMPANION = json.loads((HERE / "occupancy-companion.schema.v1.json").read_text(encoding="utf-8"))
REGISTRY = Registry().with_resources(
    [(doc["$id"], Resource(contents=doc, specification=DRAFT202012)) for doc in (HANDSHAKE, FACT_BATCH_V3, COMPANION)])
LAW = HANDSHAKE["x-opensip-wire-law"]

DELIVERY_V2 = json.loads((ARTIFACTS / "delivery.v2.json").read_text(encoding="utf-8"))
TS_IDENTITY = DELIVERY_V2["typescriptSemanticSubstrate"]["identity"]
TS_WIRE = DELIVERY_V2["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]
RUST_PROTOCOL_V2_PATH = REPO / LAW["expectedProtocolContractSha256"]["artifact"]
RUST_PROTOCOL_V2 = json.loads(RUST_PROTOCOL_V2_PATH.read_text(encoding="utf-8"))

IDENTITY_TOKENS = ("source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3")
TARGET_ATTRIBUTION = "target-attribution-v2"
LANGUAGES = {
    "typescript-semantic": {
        "hello": "TypeScriptHelloV2", "helloAck": "TypeScriptHelloAckV2", "limits": "TypeScriptProtocolLimitsV1",
        "historical": "TypeScriptFactBatchV1Vector", "historicalPayload": "FactBatchV1", "candidateArray": "facts",
        "batchCap": "maxFactBatchFacts", "payloadBound": "maxFactCandidatePayloadBytes",
    },
    "rust-semantic": {
        "hello": "HelloV3", "helloAck": "HelloAckV3", "limits": "ProtocolLimitsV3",
        "historical": "RustFactBatchV2Vector", "historicalPayload": "FactBatchV2", "candidateArray": "candidates",
        "batchCap": "maxFactBatchCandidates", "payloadBound": "maxCanonicalRelationPayloadBytes",
    },
}


class ProviderWireRefusal(C.AdmissionError):
    """A provider wire record the host must refuse: PROVIDER.PROTOCOL_VIOLATION.

    At Hello/HelloAck the refusal precedes every source byte; at FactBatch it precedes candidate
    admission. `key` is an internal reference key, never a public D9 code."""

    def __init__(self, key: str, detail: str = ""):
        self.key = key
        self.detail = detail
        super().__init__("PROVIDER.PROTOCOL_VIOLATION:" + key + (":" + detail if detail else ""))


def _language(language: str) -> dict:
    if language not in LANGUAGES:
        raise ProviderWireRefusal("LANGUAGE", repr(language))
    return LANGUAGES[language]


def _refuse_schema(label: str, exc: Exception):
    path = "/".join(str(p) for p in (getattr(exc, "absolute_path", None) or []))
    message = getattr(exc, "message", None) or str(exc).splitlines()[0]
    raise ProviderWireRefusal("SCHEMA", f"{label}:/{path}:{message}") from exc


def validate_wire(def_name: str, value):
    """Exact typed admission of one provider-handshake.schemas.v1.json definition (no mutation)."""
    if def_name not in HANDSHAKE["$defs"]:
        raise ProviderWireRefusal("SCHEMA", "unknown definition " + def_name)
    try:
        return C.validate({"$ref": HANDSHAKE["$id"] + "#/$defs/" + def_name}, value, registry=REGISTRY)
    except Exception as exc:  # noqa: BLE001 - every schema refusal is one typed protocol violation
        _refuse_schema(def_name, exc)


def published_major(language: str) -> int:
    return HANDSHAKE["$defs"][_language(language)["helloAck"]]["properties"]["protocolMajor"]["const"]


def published_limits(language: str) -> dict:
    """The exact per-language Hello limit map, read from the published closed definition."""
    props = HANDSHAKE["$defs"][_language(language)["limits"]]["properties"]
    return {name: prop["const"] for name, prop in props.items()}


def wire_cbor(value) -> bytes:
    """Deterministic CBOR of a wire value with text-keyed maps (RFC 8949 core deterministic order)."""
    if value is None:
        return b"\xf6"
    if value is False:
        return b"\xf4"
    if value is True:
        return b"\xf5"
    if type(value) is int:
        if value < 0:
            raise ProviderWireRefusal("WIRE_CBOR", "negative integer")
        return FP._cbor_head(0, value)
    if type(value) is bytes:
        return FP._cbor_head(2, len(value)) + value
    if type(value) is str:
        if unicodedata.normalize("NFC", value) != value:
            raise ProviderWireRefusal("WIRE_CBOR", "non-NFC text")
        data = value.encode("utf-8")
        return FP._cbor_head(3, len(data)) + data
    if type(value) is list:
        return FP._cbor_head(4, len(value)) + b"".join(wire_cbor(item) for item in value)
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise ProviderWireRefusal("WIRE_CBOR", "non-text map key")
        pairs = sorted((wire_cbor(k), wire_cbor(v)) for k, v in value.items())
        return FP._cbor_head(5, len(pairs)) + b"".join(k + v for k, v in pairs)
    raise ProviderWireRefusal("WIRE_CBOR", "unsupported type " + type(value).__name__)


def _admit_text(def_name: str, value: dict, where: str) -> None:
    for key, prop in HANDSHAKE["$defs"][def_name]["properties"].items():
        target = prop.get("$ref", "").rsplit("/", 1)[-1]
        if target in ("NfcText", "IdentityText"):
            text = value[key]
            if unicodedata.normalize("NFC", text) != text:
                raise ProviderWireRefusal("TEXT_NOT_NFC", where + key)
            if target == "IdentityText" and len(text.encode("utf-8")) > 4096:
                raise ProviderWireRefusal("TEXT_BYTE_BOUND", where + key)
        elif target == "ExpectedRustIdentityV3":
            _admit_text(target, value[key], where + key + ".")


def _utf8_sorted(tokens) -> list:
    return sorted(tokens, key=lambda token: token.encode("utf-8"))


def _admit_descriptor(which: str, descriptor, major: int) -> dict:
    """A verified TypeScript identity descriptor, held to its delivery.v2 closed member list."""
    required = TS_IDENTITY[which + "Descriptor"]["closedRequired"]
    if not isinstance(descriptor, dict) or sorted(descriptor) != sorted(required):
        raise ProviderWireRefusal("DESCRIPTOR_SHAPE", which)
    if which == "provider":
        if not C.equal_typed(descriptor["protocolMajor"], major):
            raise ProviderWireRefusal("DESCRIPTOR_PROTOCOL_MAJOR", repr(descriptor["protocolMajor"]))
        budget = TS_IDENTITY["defaultWorkBudgetProfile"]
        if (descriptor["defaultWorkBudgetProfileId"] != budget["profile"]["profileId"]
                or descriptor["defaultWorkBudgetProfileSha256"] != budget["sha256"]):
            raise ProviderWireRefusal("DESCRIPTOR_WORK_BUDGET", "")
    return descriptor


def _descriptor_digest(descriptor: dict) -> str:
    return hashlib.sha256(C.canonical(descriptor)).hexdigest()


def _envelope(language: str, envelope_protocol_major) -> int:
    major = published_major(language)
    if type(envelope_protocol_major) is not int or envelope_protocol_major != major:
        raise ProviderWireRefusal("PROTOCOL_MAJOR", f"envelope {envelope_protocol_major!r} != {major}")
    return major


def admit_hello(language: str, hello, envelope_protocol_major, signed_row, expected: dict) -> dict:
    """Host-side Hello construction/admission. `signed_row` is the selected signed capability row's
    token list and `expected` the trusted verified inputs: TypeScript {hostBuildId, providerDescriptor,
    runtimeDescriptor}; Rust {hostBuildId, identity} where identity is the selected Plan rust-v1 row's
    protocolMajor/providerBuildId/rustCommitHash/hostTriple/targetTriple/sysrootDigest."""
    spec = _language(language)
    major = _envelope(language, envelope_protocol_major)
    validate_wire(spec["hello"], hello)
    _admit_text(spec["hello"], hello, "hello.")
    limits = published_limits(language)
    if not C.equal_typed(hello["limits"], limits) or wire_cbor(hello["limits"]) != wire_cbor(limits):
        raise ProviderWireRefusal("LIMITS", spec["limits"])
    row = list(signed_row)
    if len(set(row)) != len(row):
        raise ProviderWireRefusal("SIGNED_ROW", "duplicate token")
    missing = [token for token in IDENTITY_TOKENS if token not in row]
    if missing:
        raise ProviderWireRefusal("SIGNED_ROW", "identity tokens missing " + ",".join(missing))
    if hello["expectedCapabilities"] != _utf8_sorted(row):
        raise ProviderWireRefusal("CAPABILITIES", "Hello tokens differ from the selected signed row")
    if hello["hostBuildId"] != expected["hostBuildId"]:
        raise ProviderWireRefusal("HOST_BUILD_ID", "")
    if language == "typescript-semantic":
        for which, member in (("provider", "expectedProviderDescriptorSha256"),
                              ("runtime", "expectedRuntimeDescriptorSha256")):
            descriptor = _admit_descriptor(which, expected[which + "Descriptor"], major)
            if hello[member] != _descriptor_digest(descriptor):
                raise ProviderWireRefusal("DESCRIPTOR_DIGEST", which)
    else:
        contract = hashlib.sha256(RUST_PROTOCOL_V2_PATH.read_bytes()).hexdigest()
        if contract != LAW["expectedProtocolContractSha256"]["sha256"]:
            raise ProviderWireRefusal("CONTRACT_PIN", contract)
        if hello["expectedProtocolContractSha256"] != contract:
            raise ProviderWireRefusal("CONTRACT_DIGEST", hello["expectedProtocolContractSha256"])
        identity = expected["identity"]
        for member in LAW["rustIdentityBinding"]["identityFields"]:
            if member not in identity or not C.equal_typed(hello["expectedIdentity"][member], identity[member]):
                raise ProviderWireRefusal("EXPECTED_IDENTITY", member)
    return {"outcome": "hello-admitted", "language": language, "protocolMajor": major,
            "expectedCapabilities": list(hello["expectedCapabilities"]),
            "targetAttributionOffered": TARGET_ATTRIBUTION in hello["expectedCapabilities"],
            "sourceBytesSent": False}


def admit_hello_ack(language: str, hello, ack, envelope_protocol_major, expected: dict) -> dict:
    """Host-side HelloAck admission against the admitted Hello. `expected` carries the verified
    TypeScript descriptors {providerDescriptor, runtimeDescriptor}; Rust echoes Hello only."""
    spec = _language(language)
    major = _envelope(language, envelope_protocol_major)
    validate_wire(spec["hello"], hello)
    validate_wire(spec["helloAck"], ack)
    _admit_text(spec["helloAck"], ack, "helloAck.")
    if ack["capabilities"] != hello["expectedCapabilities"]:
        raise ProviderWireRefusal("CAPABILITY_ECHO", "")
    if not C.equal_typed(ack["identityVersions"], hello["identityVersions"]):
        raise ProviderWireRefusal("IDENTITY_VERSIONS_ECHO", "")
    if language == "typescript-semantic":
        binding = LAW["typescriptDescriptorBinding"]
        for which, hello_member, ack_member, fields in (
                ("provider", "expectedProviderDescriptorSha256", "providerDescriptorSha256",
                 binding["providerDescriptorFields"]),
                ("runtime", "expectedRuntimeDescriptorSha256", "runtimeDescriptorSha256",
                 binding["runtimeDescriptorFields"])):
            descriptor = _admit_descriptor(which, expected[which + "Descriptor"], major)
            if hello[hello_member] != _descriptor_digest(descriptor):
                raise ProviderWireRefusal("DESCRIPTOR_DIGEST", which)
            if ack[ack_member] != hello[hello_member]:
                raise ProviderWireRefusal("DESCRIPTOR_DIGEST_ECHO", which)
            for field in fields:
                if not C.equal_typed(ack[field], descriptor[field]):
                    raise ProviderWireRefusal("DESCRIPTOR_FIELD", field)
    else:
        identity = hello["expectedIdentity"]
        if not C.equal_typed(ack["protocolMajor"], identity["protocolMajor"]):
            raise ProviderWireRefusal("IDENTITY_ECHO", "protocolMajor")
        for field in LAW["rustIdentityBinding"]["echoFields"]:
            if not C.equal_typed(ack[field], identity[field]):
                raise ProviderWireRefusal("IDENTITY_ECHO", field)
    tokens = list(ack["capabilities"])
    return {"outcome": "accepted", "language": language, "protocolMajor": major,
            "identityNegotiated": all(token in tokens for token in IDENTITY_TOKENS),
            "targetAttributionNegotiated": TARGET_ATTRIBUTION in tokens,
            "negotiatedTokens": tokens, "sourceBytesSent": False, "next": "OpenUniverse"}


def admit_fact_batch(language: str, batch, negotiated_tokens, expected: dict | None = None) -> dict:
    """Wire admission of one FactBatch payload. Negotiated target-attribution-v2 selects FactBatchV3;
    otherwise the language's historical payload (TypeScript FactBatchV1 with batchCommitment, Rust
    FactBatchV2). `expected` optionally carries the DispatchBindingV1 correlation values
    {stageId, analysisOrdinal, batchIndex, firstCandidateOrdinal}."""
    spec = _language(language)
    if not isinstance(batch, dict):
        raise ProviderWireRefusal("FACT_BATCH_SHAPE", "not a map")
    negotiated = TARGET_ATTRIBUTION in list(negotiated_tokens)
    if negotiated:
        if "schemaVersion" not in batch:
            raise ProviderWireRefusal("HISTORICAL_WITH_TOKEN", spec["historicalPayload"])
        try:
            C.validate(FACT_BATCH_V3, batch, registry=REGISTRY)
        except Exception as exc:  # noqa: BLE001
            _refuse_schema("FactBatchV3", exc)
        payload, array = "FactBatchV3", "candidates"
        if language == "typescript-semantic" and batch["analysisOrdinal"] != 0:
            raise ProviderWireRefusal("ANALYSIS_ORDINAL", "typescript-semantic AnalyzeV1.analysisOrdinal is exactly 0")
    else:
        if batch.get("schemaVersion") == 3 or "occupancyCompanions" in batch:
            raise ProviderWireRefusal("UNNEGOTIATED_V3", TARGET_ATTRIBUTION)
        validate_wire(spec["historical"], batch)
        payload, array = spec["historicalPayload"], spec["candidateArray"]
    limits = published_limits(language)
    candidates = batch[array]
    if len(candidates) > limits[spec["batchCap"]]:
        raise ProviderWireRefusal("BATCH_CANDIDATE_CAP", spec["batchCap"])
    wire_candidates = []
    for candidate in candidates:
        ordinal = candidate["candidateOrdinal"]
        try:
            decoded_hex = FP._deterministic_cbor(candidate["decodedRelationPayload"]).hex()
        except ValueError as exc:
            raise ProviderWireRefusal("CANDIDATE_PAYLOAD_CBOR", f"{ordinal}:{exc}") from exc
        if decoded_hex != candidate["canonicalRelationPayloadHex"]:
            raise ProviderWireRefusal("CANDIDATE_PAYLOAD_CBOR", str(ordinal))
        raw = bytes.fromhex(candidate["canonicalRelationPayloadHex"])
        if len(raw) > limits[spec["payloadBound"]]:
            raise ProviderWireRefusal("CANDIDATE_PAYLOAD_BOUND", spec["payloadBound"])
        wire = {k: v for k, v in candidate.items() if k not in ("canonicalRelationPayloadHex", "decodedRelationPayload")}
        wire["canonicalRelationPayload"] = raw
        wire_candidates.append(wire)
    ordinals = [candidate["candidateOrdinal"] for candidate in candidates]
    if payload == "FactBatchV3":
        known = set(ordinals)
        companions = batch["occupancyCompanions"]
        if len(companions) > len(candidates) or any(c["candidateOrdinal"] not in known for c in companions):
            raise ProviderWireRefusal("COMPANION_CANDIDATE", "")
    if expected is not None:
        for member in ("stageId", "analysisOrdinal", "batchIndex"):
            if member in expected and not C.equal_typed(batch[member], expected[member]):
                raise ProviderWireRefusal("CORRELATION", member)
        if "firstCandidateOrdinal" in expected:
            first = expected["firstCandidateOrdinal"]
            if ordinals != list(range(first, first + len(ordinals))):
                raise ProviderWireRefusal("CANDIDATE_ORDINAL_CONTIGUITY", "")
    candidates_cbor = wire_cbor(wire_candidates)
    commitment, verified = None, None
    if payload == "FactBatchV1":
        domain = TS_WIRE["commitments"]["domains"]["factBatch"]
        commitment = "sha256:" + hashlib.sha256(domain.encode("utf-8") + b"\x00" + candidates_cbor).hexdigest()
        if batch["batchCommitment"] != commitment:
            raise ProviderWireRefusal("BATCH_COMMITMENT", batch["batchCommitment"])
        verified = True
    wire_batch = dict(batch)
    wire_batch[array] = wire_candidates
    return {"payload": payload, "language": language, "negotiated": negotiated, "candidateArray": array,
            "candidateCount": len(candidates), "candidateOrdinals": ordinals,
            "wireCandidatesCborHex": candidates_cbor.hex(),
            "wireBatchCborSha256": hashlib.sha256(wire_cbor(wire_batch)).hexdigest(),
            "perBatchCommitmentCarried": payload == "FactBatchV1",
            "batchCommitment": commitment, "batchCommitmentVerified": verified}
