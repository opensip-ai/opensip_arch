"""Author native/provider-handshake.schemas.v1.json in the work copy from published inputs.

usage: author_handshake_schema.py <work-candidate-root>

The TypeScript limit map and the 24 inherited Rust limits are copied from the pinned inherited
artifacts (delivery.v2, rust-provider-protocol.v2); the eight rust-semantic successor limits are the
native-evidence section 9.3 values. The native checker re-derives all three from those published
inputs and fails on any drift, so this script is a typing aid, not an authority.
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
ARTIFACTS = ROOT / "docs" / "coop" / "artifacts"
OUT = ROOT / "docs" / "coop" / "design-corrections" / "native" / "provider-handshake.schemas.v1.json"

delivery = json.loads((ARTIFACTS / "delivery.v2.json").read_text(encoding="utf-8"))
rust_bytes = (ARTIFACTS / "rust-provider-protocol.v2.json").read_bytes()
rust = json.loads(rust_bytes)
RUST_SHA = hashlib.sha256(rust_bytes).hexdigest()
assert RUST_SHA == "6308a98c1183d75d671655b2a351334b62f4f2c00316983731ceabb86e90793b", RUST_SHA

ts_sub = delivery["typescriptSemanticSubstrate"]
ts_wire = ts_sub["providerProtocol"]["wireSchema"]
ts_limits = {k: v for k, v in ts_wire["limits"].items() if k != "limitRule"}
assert all(type(v) is int for v in ts_limits.values()) and len(ts_limits) == 10
rust_limits = dict(rust["limits"])
assert all(type(v) is int for v in rust_limits.values()) and len(rust_limits) == 24
SUCCESSOR8 = [
    ("maxDependencySourcePackages", 4096),
    ("maxDependencySourceEntries", 1000000),
    ("maxDependencySourceTotalBytes", 8589934592),
    ("maxDependencySourceChunkBytes", 1048576),
    ("maxUnresolvedEdgesPerStage", 1000000),
    ("maxCfgSets", 4),
    ("maxExpansionRows", 1000000),
    ("maxGeneratedFileRows", 1000000),
]
assert not set(rust_limits) & {k for k, _ in SUCCESSOR8}
budget = ts_sub["identity"]["defaultWorkBudgetProfile"]

IDENTITY = ["source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3"]
TS_TOKENS = sorted(IDENTITY + ["sealed-vfs-v1", "multi-stage-analyze-v1", "typescript-semantic-facts-v1",
                               "resolution-completeness-v2", "unresolved-edge-v1", "native-context-v2",
                               "target-attribution-v2"])
RUST_TOKENS = sorted(IDENTITY + ["sealed-vfs-v1", "multi-stage-analyze-v1", "rust-semantic-facts-v1",
                                 "resolution-completeness-v2", "unresolved-edge-v1", "dependency-source-v1",
                                 "prepared-output-v3", "native-context-v2", "target-attribution-v2"])


def ref(name):
    return {"$ref": "#/$defs/" + name}


def closed(required, properties, description):
    return {"type": "object", "additionalProperties": False, "required": list(required),
            "properties": properties, "description": description}


def consts(mapping):
    return {k: {"const": v} for k, v in mapping.items()}


def token_array(token_def, count, description):
    return {"type": "array", "minItems": 4, "maxItems": count, "uniqueItems": True, "items": ref(token_def),
            "x-opensip-order": "utf8",
            "allOf": [{"contains": {"const": t}} for t in IDENTITY],
            "description": description}


TS_PROVIDER_FIELDS = ["providerBuildId", "protocolMajor", "typescriptVersion", "typescriptCompilerSha256",
                      "typescriptStdlibMerkleRoot", "defaultWorkBudgetProfileId", "defaultWorkBudgetProfileSha256"]
TS_RUNTIME_FIELDS = ["nodeVersion", "v8Version", "modulesAbi", "platformId"]
RUST_IDENTITY_FIELDS = ["protocolMajor", "providerBuildId", "rustCommitHash", "hostTriple", "targetTriple", "sysrootDigest"]
RUST_ECHO_FIELDS = RUST_IDENTITY_FIELDS[1:]

rust_limit_map = dict(rust_limits)
rust_limit_map.update(SUCCESSOR8)

doc = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "opensip.product.provider-handshake.1",
    "title": "Provider handshake successors: typescript-semantic major 2 and rust-semantic major 3 Hello/HelloAck, limits and historical FactBatch vectors",
    "description": "NORMATIVE field-level publication for native-evidence sections 9.1, 9.3, 9.4 and 9.6. HelloV3, HelloAckV3 and ProtocolLimitsV3 here SUPERSEDE the same-named $defs of native/native-evidence.schemas.v2.json, whose registered bytes are kept unchanged because that document's raw SHA-256 is a registered payloadSchemaDigest (native-evidence section 10); a byte change there would be a schema-document successor with re-registration. TypeScriptProtocolLimitsV1, TypeScriptHelloV2 and TypeScriptHelloAckV2 publish the typescript-semantic major-2 handshake. Every record is the JSON-vector form of a closed deterministic-CBOR map; handshake payloads carry no byte strings. Cross-record joins that a stock schema cannot express (descriptor digests and fields, identity and token echoes, contract digest, limit CBOR byte equality, candidate CBOR projection, TypeScript batch commitment) are executed by native/provider_wire_model.v1.py within that module's stated scope.",
    "x-opensip-wire-law": {
        "supersedes": [
            "native/native-evidence.schemas.v2.json#/$defs/HelloV3",
            "native/native-evidence.schemas.v2.json#/$defs/HelloAckV3",
            "native/native-evidence.schemas.v2.json#/$defs/ProtocolLimitsV3",
        ],
        "frameAndMajor": {
            "typescript-semantic": "Frame names Hello and HelloAck are unchanged. delivery.v2 typescriptSemanticSubstrate.providerProtocol.major is 2 and wireSchema.frameEnvelope.fields.protocolMajor is exactly 2. TypeScriptHelloV2 carries no payload protocolMajor, as HelloV1 did not. TypeScriptHelloAckV2.protocolMajor is exactly 2 and equals the verified provider descriptor protocolMajor.",
            "rust-semantic": "Frame names Hello and HelloAck are unchanged. rust-provider-protocol.v2 protocolIdentity.protocolMajor is 3 and wireSchema.envelope.fields.protocolMajor is exactly 3. HelloV3.protocolMajor (kept from the superseded HelloV3 definition), HelloV3.expectedIdentity.protocolMajor (kept from ExpectedRustIdentityV2) and HelloAckV3.protocolMajor (kept from HelloAckV2) are each exactly 3.",
        },
        "capabilityArrays": "HelloV3.expectedCapabilities, HelloAckV3.capabilities, TypeScriptHelloV2.expectedCapabilities and TypeScriptHelloAckV2.capabilities are strictly unique arrays in ascending UTF-8 byte order (x-opensip-order utf8), drawn only from that language's tokens and containing the four identity tokens. Hello carries exactly the selected signed capability row's tokens for that worker; HelloAck echoes the Hello array exactly (same members in the same order). typescript-semantic inherits the rule from HelloAckV1 'exact sorted array'; for rust-semantic it replaces the unordered 'sequence' annotation of the superseded HelloV3 definition, so exact recursive equality and token-set equality coincide.",
        "identityVersions": "Hello carries {snapshot:2, plan:2, fact:2, coverage:3}; HelloAck echoes it exactly.",
        "limits": {
            "typescript-semantic": "TypeScriptHelloV2.limits is TypeScriptProtocolLimitsV1: the closed map of exactly the ten numeric members of delivery.v2 typescriptSemanticSubstrate.providerProtocol.wireSchema.limits with identical values. limitRule is policy text, never a member. No ProtocolLimitsV3 member applies.",
            "rust-semantic": "HelloV3.limits is ProtocolLimitsV3: the closed map of the 24 rust-provider-protocol.v2 limits members with identical values plus the eight native-evidence section 9.3 members, 32 in all. rust-provider-protocol.v2 limitsHandshake (exact semantic and deterministic-CBOR byte equality) and limitPolicy apply unchanged to this value.",
            "refusal": "A missing, extra, renamed, retyped or changed member refuses Hello before HelloAck (PROVIDER.PROTOCOL_VIOLATION).",
        },
        "typescriptDescriptorBinding": {
            "digests": "expectedProviderDescriptorSha256 and expectedRuntimeDescriptorSha256 are the raw SHA-256 of the RFC 8785 bytes of the verified signed typescript-provider/identity.json and typescript-runtime/identity.json descriptors (delivery.v2 typescriptSemanticSubstrate.identity; resolved-inputs.v2 typescript-v1 deliveryJoin). HelloAck providerDescriptorSha256 and runtimeDescriptorSha256 equal those Hello values.",
            "providerDescriptorFields": TS_PROVIDER_FIELDS,
            "runtimeDescriptorFields": TS_RUNTIME_FIELDS,
            "rule": "Each providerDescriptorFields member of HelloAck equals the same-named member of the verified provider descriptor and each runtimeDescriptorFields member equals the verified runtime descriptor (delivery.v2 identity.hostValidation). Any mismatch is PROVIDER.PROTOCOL_VIOLATION before a source byte. The verified providerBuildId remains the source of FactCandidateV1.producerVersion.",
        },
        "rustIdentityBinding": {
            "identityFields": RUST_IDENTITY_FIELDS,
            "echoFields": RUST_ECHO_FIELDS,
            "source": "HelloV3.expectedIdentity members are the selected Plan semantic-universe row's same-named members of resolved-inputs.v2 planIdContract.semanticUniverseSchemas.rust-v1 (retained; only rust-v1.resolvedInputs is superseded, by rust-v2), whose deliveryJoin binds them to the verified signed release (rust-provider-protocol.v2 requestProjection.identity). HelloV3.hostBuildId is the host build identity, unchanged from HelloV2.",
            "rule": "HelloAckV3 echoFields equal Hello expectedIdentity exactly and HelloAckV3.protocolMajor equals expectedIdentity.protocolMajor (HelloAckV2 'exact Hello expectedIdentity value'). Any mismatch is PROVIDER.PROTOCOL_VIOLATION before a source byte.",
        },
        "expectedProtocolContractSha256": {
            "artifact": "docs/coop/artifacts/rust-provider-protocol.v2.json",
            "sha256": RUST_SHA,
            "rule": "Raw SHA-256 (DigestHex) of the exact bytes of the selected inherited contract that HelloV2 names ('exact selected v2 artifact bytes'), pinned in native/source-pins.v2.json. It authenticates the retained inherited base only. The major-3 successor law is identified on the wire by protocolMajor 3, the identity token set, identityVersions and the exact ProtocolLimitsV3 map; no digest of the successor documents is a Hello member, because selecting one would be a new digest input rather than an inherited one.",
        },
        "factBatch": {
            "negotiated": "FactBatchV3 (native/fact-batch.schema.v3.json) for either language iff target-attribution-v2 is in both the Hello and the HelloAck token arrays.",
            "typescript-semantic": "Not negotiated: delivery.v2 FactBatchV1 {analysisOrdinal, stageId, batchIndex, facts, batchCommitment}, unchanged (JSON vector: TypeScriptFactBatchV1Vector).",
            "rust-semantic": "Not negotiated: rust-provider-protocol.v2 FactBatchV2 {analysisOrdinal, stageId, batchIndex, candidates}, unchanged (JSON vector: RustFactBatchV2Vector).",
            "violation": "A FactBatchV3 payload without the token, or that language's historical payload with the token, is PROVIDER.PROTOCOL_VIOLATION.",
            "candidateCap": "typescript-semantic maxFactBatchFacts 4096; rust-semantic maxFactBatchCandidates 4096. occupancyCompanions length is at most len(candidates) under either name.",
        },
        "commitments": {
            "typescript-semantic": "FactBatchV1.batchCommitment = sha256:hex(SHA-256(UTF8(opensip.ts-provider.fact-batch.v1) || 0x00 || deterministic-CBOR(facts))) under delivery.v2 wireSchema.commitments.domainRule, over the wire FactCandidateV1 array. Negotiated FactBatchV3 carries no batchCommitment: commitments.domains.factBatch applies to FactBatchV1 only. StageResultV1.factCommitment (stageFacts) and CompleteV1.factStreamCommitment (factStream) remain over the ordered FactCandidateV1 stream whichever payload carried it.",
            "rust-semantic": "Neither FactBatchV2 nor FactBatchV3 carries a per-batch commitment; rust-provider-protocol.v2 commitments.stageFacts and factStream remain over the ordered candidates.",
        },
        "candidateCborProjection": "In every FactBatch JSON vector a candidate's canonicalRelationPayloadHex is the lowercase hex of the wire FactCandidateV1.canonicalRelationPayload CBOR byte string and decodedRelationPayload is a verified observation, not a wire member. The wire candidate is the vector candidate with decodedRelationPayload removed and canonicalRelationPayloadHex replaced by canonicalRelationPayload = bytes(hex); admission requires hex == deterministic-CBOR(decodedRelationPayload). Wire maps are deterministic CBOR (delivery.v2 wireSchema.canonicalCbor; rust-provider-protocol.v2 canonicalCbor); with text keys only, the two inherited map-order rules select the same order.",
    },
    "$defs": {
        "Uint64": {"type": "integer", "minimum": 0, "maximum": 18446744073709551615},
        "DigestHex": {"type": "string", "pattern": "^[0-9a-f]{64}(?![\\s\\S])"},
        "Sha256Text": {"type": "string", "pattern": "^sha256:[0-9a-f]{64}(?![\\s\\S])"},
        "NfcText": {"type": "string", "minLength": 1,
                    "description": "delivery.v2 'non-empty NFC text' / 'verified descriptor text'. NFC is checked by admission."},
        "IdentityText": {"type": "string", "minLength": 1, "maxLength": 4096,
                         "pattern": "^[^\\u0000-\\u001f\\u0080-\\u009f]+(?![\\s\\S])",
                         "description": "rust-provider-protocol.v2 IdentityText: NFC, 1..4096 UTF-8 bytes, no C0/C1 control. NFC and the UTF-8 byte bound are checked by admission."},
        "StageIdText": {"type": "string", "minLength": 1, "maxLength": 255,
                        "description": "C-2 stageId text, the historical FactBatchV1/V2 stageId type preserved on FactBatchV3."},
        "IdentityVersionsV1": closed(["snapshot", "plan", "fact", "coverage"],
                                     consts({"snapshot": 2, "plan": 2, "fact": 2, "coverage": 3}),
                                     "native-evidence section 9.1 identity versions; HelloAck echoes the Hello value exactly."),
        "TypeScriptCapabilityToken": {"type": "string", "enum": TS_TOKENS,
                                      "description": "The typescript-semantic members of native-evidence.schemas.v2.json#/$defs/CapabilityToken (section 9.1); the Rust-only dependency-source-v1, prepared-output-v3 and rust-semantic-facts-v1 are excluded (section 9.4)."},
        "RustCapabilityToken": {"type": "string", "enum": RUST_TOKENS,
                                "description": "The rust-semantic members of native-evidence.schemas.v2.json#/$defs/CapabilityToken (section 9.1); typescript-semantic-facts-v1 is excluded."},
        "TypeScriptCapabilitiesV2": token_array("TypeScriptCapabilityToken", len(TS_TOKENS),
                                                "typescript-semantic token array: strictly unique ascending UTF-8 order, the four identity tokens present."),
        "RustCapabilitiesV3": token_array("RustCapabilityToken", len(RUST_TOKENS),
                                          "rust-semantic token array: strictly unique ascending UTF-8 order, the four identity tokens present."),
        "TypeScriptProtocolLimitsV1": closed(list(ts_limits), consts(ts_limits),
                                             "Exactly the ten numeric members of delivery.v2 typescriptSemanticSubstrate.providerProtocol.wireSchema.limits with identical values; limitRule is policy text and never a member."),
        "ProtocolLimitsV3": closed(list(rust_limit_map), consts(rust_limit_map),
                                   "rust-semantic HelloV3.limits: the 24 rust-provider-protocol.v2 limits members with identical values plus the eight native-evidence section 9.3 members (32). limitsHandshake semantic and deterministic-CBOR byte equality and limitPolicy apply unchanged."),
        "TypeScriptHelloV2": closed(
            ["hostBuildId", "expectedProviderDescriptorSha256", "expectedRuntimeDescriptorSha256", "limits",
             "expectedCapabilities", "identityVersions"],
            {
                "hostBuildId": {"$ref": "#/$defs/NfcText", "description": "HelloV1 hostBuildId, unchanged."},
                "expectedProviderDescriptorSha256": {"$ref": "#/$defs/DigestHex", "description": "HelloV1, unchanged: raw SHA-256 of the RFC 8785 bytes of the verified signed typescript-provider/identity.json."},
                "expectedRuntimeDescriptorSha256": {"$ref": "#/$defs/DigestHex", "description": "HelloV1, unchanged: raw SHA-256 of the RFC 8785 bytes of the verified signed typescript-runtime/identity.json."},
                "limits": {"$ref": "#/$defs/TypeScriptProtocolLimitsV1", "description": "HelloV1 'closed map equal to wireSchema.limits numeric fields', unchanged."},
                "expectedCapabilities": {"$ref": "#/$defs/TypeScriptCapabilitiesV2", "description": "Added: the selected signed capability row's tokens (section 9.1)."},
                "identityVersions": {"$ref": "#/$defs/IdentityVersionsV1", "description": "Added (section 9.1)."},
            },
            "typescript-semantic major-2 Hello. Every HelloV1 member unchanged plus expectedCapabilities and identityVersions. No payload protocolMajor; the envelope protocolMajor is exactly 2."),
        "TypeScriptHelloAckV2": closed(
            ["protocolMajor", "providerBuildId", "providerDescriptorSha256", "runtimeDescriptorSha256", "nodeVersion",
             "v8Version", "modulesAbi", "typescriptVersion", "typescriptCompilerSha256", "typescriptStdlibMerkleRoot",
             "defaultWorkBudgetProfileId", "defaultWorkBudgetProfileSha256", "platformId", "capabilities",
             "identityVersions"],
            {
                "protocolMajor": {"const": 2, "description": "HelloAckV1 'uint64 exactly 1' replaced by exactly 2; equals the verified provider descriptor protocolMajor."},
                "providerBuildId": {"$ref": "#/$defs/NfcText", "description": "HelloAckV1, unchanged: verified provider descriptor value."},
                "providerDescriptorSha256": {"$ref": "#/$defs/DigestHex", "description": "HelloAckV1, unchanged: equals Hello expectedProviderDescriptorSha256."},
                "runtimeDescriptorSha256": {"$ref": "#/$defs/DigestHex", "description": "HelloAckV1, unchanged: equals Hello expectedRuntimeDescriptorSha256."},
                "nodeVersion": {"$ref": "#/$defs/NfcText", "description": "HelloAckV1, unchanged: verified runtime descriptor value."},
                "v8Version": {"$ref": "#/$defs/NfcText", "description": "HelloAckV1, unchanged: verified runtime descriptor value."},
                "modulesAbi": {"$ref": "#/$defs/NfcText", "description": "HelloAckV1, unchanged: verified runtime descriptor value."},
                "typescriptVersion": {"$ref": "#/$defs/NfcText", "description": "HelloAckV1, unchanged: verified provider descriptor value."},
                "typescriptCompilerSha256": {"$ref": "#/$defs/DigestHex", "description": "HelloAckV1, unchanged: verified provider descriptor value."},
                "typescriptStdlibMerkleRoot": {"$ref": "#/$defs/DigestHex", "description": "HelloAckV1, unchanged: verified provider descriptor value."},
                "defaultWorkBudgetProfileId": {"const": budget["profile"]["profileId"], "description": "HelloAckV1, unchanged."},
                "defaultWorkBudgetProfileSha256": {"const": budget["sha256"], "description": "HelloAckV1, unchanged."},
                "platformId": {"$ref": "#/$defs/NfcText", "description": "HelloAckV1, unchanged: selected release platformId, equal to the verified runtime descriptor value."},
                "capabilities": {"$ref": "#/$defs/TypeScriptCapabilitiesV2", "description": "HelloAckV1 fixed three-token array replaced by the exact echo of Hello expectedCapabilities."},
                "identityVersions": {"$ref": "#/$defs/IdentityVersionsV1", "description": "Added: exact echo of Hello identityVersions."},
            },
            "typescript-semantic major-2 HelloAck. Every HelloAckV1 member kept, including all provider/runtime descriptor verification; protocolMajor 1 -> 2 and the fixed capability array -> the negotiated echo; identityVersions added."),
        "ExpectedRustIdentityV3": closed(
            RUST_IDENTITY_FIELDS,
            {
                "protocolMajor": {"const": 3, "description": "ExpectedRustIdentityV2 'uint64 exactly 2' replaced by exactly 3."},
                "providerBuildId": {"$ref": "#/$defs/IdentityText", "description": "Selected Plan rust-v1 row providerBuildId (verified signed release)."},
                "rustCommitHash": {"$ref": "#/$defs/DigestHex", "description": "Selected Plan rust-v1 row rustCommitHash (resolved-inputs.v2 rust-v1 digestFields representation)."},
                "hostTriple": {"$ref": "#/$defs/IdentityText", "description": "Selected Plan rust-v1 row hostTriple."},
                "targetTriple": {"$ref": "#/$defs/IdentityText", "description": "Selected Plan rust-v1 row targetTriple."},
                "sysrootDigest": {"$ref": "#/$defs/DigestHex", "description": "Selected Plan rust-v1 row sysrootDigest."},
            },
            "ExpectedRustIdentityV2 members unchanged except protocolMajor 3."),
        "HelloV3": closed(
            ["protocolMajor", "hostBuildId", "expectedProtocolContractSha256", "expectedIdentity", "expectedCapabilities",
             "identityVersions", "limits"],
            {
                "protocolMajor": {"const": 3, "description": "Kept from the superseded HelloV3 definition."},
                "hostBuildId": {"$ref": "#/$defs/IdentityText", "description": "HelloV2, unchanged."},
                "expectedProtocolContractSha256": {"$ref": "#/$defs/DigestHex", "description": "HelloV2, unchanged: raw SHA-256 of the exact bytes of docs/coop/artifacts/rust-provider-protocol.v2.json (x-opensip-wire-law expectedProtocolContractSha256)."},
                "expectedIdentity": {"$ref": "#/$defs/ExpectedRustIdentityV3", "description": "HelloV2 expectedIdentity, protocolMajor 3."},
                "expectedCapabilities": {"$ref": "#/$defs/RustCapabilitiesV3", "description": "Replaces HelloV2 RustProviderCapabilityV2 with the section 9.1 token array (kept from the superseded HelloV3 definition)."},
                "identityVersions": {"$ref": "#/$defs/IdentityVersionsV1", "description": "Kept from the superseded HelloV3 definition."},
                "limits": {"$ref": "#/$defs/ProtocolLimitsV3", "description": "32-member closed map (section 9.3)."},
            },
            "rust-semantic major-3 Hello. Every HelloV2 member kept, capability record replaced by the token array, identityVersions added, limits ProtocolLimitsV3."),
        "HelloAckV3": closed(
            ["protocolMajor", "providerBuildId", "rustCommitHash", "hostTriple", "targetTriple", "sysrootDigest",
             "capabilities", "identityVersions"],
            {
                "protocolMajor": {"const": 3, "description": "HelloAckV2 'uint64 exactly 2' replaced by exactly 3; equals Hello expectedIdentity.protocolMajor."},
                "providerBuildId": {"$ref": "#/$defs/IdentityText", "description": "HelloAckV2, unchanged: exact Hello expectedIdentity value."},
                "rustCommitHash": {"$ref": "#/$defs/DigestHex", "description": "HelloAckV2, unchanged: exact Hello expectedIdentity value."},
                "hostTriple": {"$ref": "#/$defs/IdentityText", "description": "HelloAckV2, unchanged: exact Hello expectedIdentity value."},
                "targetTriple": {"$ref": "#/$defs/IdentityText", "description": "HelloAckV2, unchanged: exact Hello expectedIdentity value."},
                "sysrootDigest": {"$ref": "#/$defs/DigestHex", "description": "HelloAckV2, unchanged: exact Hello expectedIdentity value."},
                "capabilities": {"$ref": "#/$defs/RustCapabilitiesV3", "description": "Exact echo of Hello expectedCapabilities."},
                "identityVersions": {"$ref": "#/$defs/IdentityVersionsV1", "description": "Exact echo of Hello identityVersions."},
            },
            "rust-semantic major-3 HelloAck. Every HelloAckV2 identity echo kept; protocolMajor 3; token array and identityVersions echoes."),
        "TypeScriptFactBatchV1Vector": closed(
            ["analysisOrdinal", "stageId", "batchIndex", "facts", "batchCommitment"],
            {
                "analysisOrdinal": {"const": 0, "description": "delivery.v2 FactBatchV1 'uint64 exactly 0'."},
                "stageId": {"$ref": "#/$defs/StageIdText", "description": "Current requested stage (StageRequestV1.stageId)."},
                "batchIndex": {"$ref": "#/$defs/Uint64", "description": "Contiguous from 0 for the stage."},
                "facts": {"type": "array", "minItems": 1, "maxItems": ts_limits["maxFactBatchFacts"],
                          "items": {"$ref": "opensip.product.fact-batch.3#/properties/candidates/items"},
                          "x-opensip-order": "candidateOrdinal",
                          "description": "Non-empty ordered FactCandidateV1 JSON vectors, length <= maxFactBatchFacts."},
                "batchCommitment": {"$ref": "#/$defs/Sha256Text", "description": "sha256 under domain opensip.ts-provider.fact-batch.v1 over deterministic-CBOR of the wire facts array."},
            },
            "JSON vector of the unchanged typescript-semantic historical payload delivery.v2 FactBatchV1, admitted when target-attribution-v2 is not negotiated."),
        "RustFactBatchV2Vector": closed(
            ["analysisOrdinal", "stageId", "batchIndex", "candidates"],
            {
                "analysisOrdinal": {"$ref": "#/$defs/Uint64", "description": "Exact Analyze analysisOrdinal echo."},
                "stageId": {"$ref": "#/$defs/StageIdText", "description": "StageRequestV2.planStage.stageId."},
                "batchIndex": {"$ref": "#/$defs/Uint64", "description": "Contiguous from 0 for the stage."},
                "candidates": {"type": "array", "minItems": 1, "maxItems": rust_limits["maxFactBatchCandidates"],
                               "items": {"$ref": "opensip.product.fact-batch.3#/properties/candidates/items"},
                               "x-opensip-order": "candidateOrdinal",
                               "description": "Non-empty FactCandidateV1 JSON vectors with contiguous candidateOrdinal, length <= maxFactBatchCandidates."},
            },
            "JSON vector of the unchanged rust-semantic historical payload rust-provider-protocol.v2 FactBatchV2, admitted when target-attribution-v2 is not negotiated."),
    },
}

if OUT.exists():
    raise SystemExit("refusing to overwrite " + str(OUT))
OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print("wrote", OUT, hashlib.sha256(OUT.read_bytes()).hexdigest())
