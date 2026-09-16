"""Author provider-wire fixtures and cases into the work copy's native-cases.v2.json.

usage: author_wire_cases.py <work-candidate-root>

Expected values are produced here WITHOUT the model under test: descriptor digests with hashlib over
stdlib sorted-key compact JSON (RFC 8785 for this ASCII/integer value domain), candidate payload and
wire candidate CBOR with the third-party cbor2 canonical encoder, and the TypeScript batch commitment
with hashlib under the delivery.v2 domain. Fixtures and cases are spliced textually so every
pre-existing byte of the file is preserved; the result is re-parsed and the prior content compared.
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

import cbor2

ROOT = Path(sys.argv[1])
ART = ROOT / "docs" / "coop" / "artifacts"
CASES = ROOT / "docs" / "coop" / "design-corrections" / "native" / "native-cases.v2.json"

delivery = json.loads((ART / "delivery.v2.json").read_text(encoding="utf-8"))
rust_bytes = (ART / "rust-provider-protocol.v2.json").read_bytes()
rust = json.loads(rust_bytes)
original_raw = CASES.read_bytes()
original = json.loads(original_raw)
fx = original["fixtures"]

ts_sub = delivery["typescriptSemanticSubstrate"]
ts_limits = {k: v for k, v in ts_sub["providerProtocol"]["wireSchema"]["limits"].items() if k != "limitRule"}
successor8 = {"maxDependencySourcePackages": 4096, "maxDependencySourceEntries": 1000000,
              "maxDependencySourceTotalBytes": 8589934592, "maxDependencySourceChunkBytes": 1048576,
              "maxUnresolvedEdgesPerStage": 1000000, "maxCfgSets": 4, "maxExpansionRows": 1000000,
              "maxGeneratedFileRows": 1000000}
rust_limits = dict(rust["limits"])
rust_limits.update(successor8)
budget = ts_sub["identity"]["defaultWorkBudgetProfile"]
versions = {"snapshot": 2, "plan": 2, "fact": 2, "coverage": 3}


def jcs_sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def srt(tokens):
    return sorted(tokens, key=lambda t: t.encode("utf-8"))


HOST = "opensip-host-2026.09.1"
ts_provider = {"schemaVersion": 1, "providerBuildId": "ts-provider-2026.09.1", "protocolMajor": 2,
               "entrypointRelativePath": "dist/worker.js", "entrypointSha256": "a1" * 32,
               "typescriptVersion": "5.6.3", "typescriptCompilerSha256": "b2" * 32,
               "typescriptStdlibMerkleRoot": "c3" * 32,
               "defaultWorkBudgetProfileId": budget["profile"]["profileId"],
               "defaultWorkBudgetProfileSha256": budget["sha256"], "licenseNoticeSha256": "d4" * 32}
ts_runtime = {"schemaVersion": 1, "nodeVersion": "22.9.0", "v8Version": "12.4.254.21-node.19", "modulesAbi": "127",
              "platformId": "macos-aarch64", "executableRelativePath": "bin/node", "executableSha256": "e5" * 32,
              "runtimePayloadSha256": "f6" * 32, "licenseNoticeSha256": "07" * 32}
assert sorted(ts_provider) == sorted(ts_sub["identity"]["providerDescriptor"]["closedRequired"])
assert sorted(ts_runtime) == sorted(ts_sub["identity"]["runtimeDescriptor"]["closedRequired"])


def ts_hello(row):
    return {"hostBuildId": HOST, "expectedProviderDescriptorSha256": jcs_sha(ts_provider),
            "expectedRuntimeDescriptorSha256": jcs_sha(ts_runtime), "limits": dict(ts_limits),
            "expectedCapabilities": srt(row), "identityVersions": dict(versions)}


def ts_ack(row):
    return {"protocolMajor": 2, "providerBuildId": ts_provider["providerBuildId"],
            "providerDescriptorSha256": jcs_sha(ts_provider), "runtimeDescriptorSha256": jcs_sha(ts_runtime),
            "nodeVersion": ts_runtime["nodeVersion"], "v8Version": ts_runtime["v8Version"],
            "modulesAbi": ts_runtime["modulesAbi"], "typescriptVersion": ts_provider["typescriptVersion"],
            "typescriptCompilerSha256": ts_provider["typescriptCompilerSha256"],
            "typescriptStdlibMerkleRoot": ts_provider["typescriptStdlibMerkleRoot"],
            "defaultWorkBudgetProfileId": ts_provider["defaultWorkBudgetProfileId"],
            "defaultWorkBudgetProfileSha256": ts_provider["defaultWorkBudgetProfileSha256"],
            "platformId": ts_runtime["platformId"], "capabilities": srt(row), "identityVersions": dict(versions)}


rust_identity = {"protocolMajor": 3, "providerBuildId": "rust-provider-2026.09.1", "rustCommitHash": "9a" * 32,
                 "hostTriple": "aarch64-apple-darwin", "targetTriple": "aarch64-apple-darwin", "sysrootDigest": "8b" * 32}


def rust_hello(row):
    return {"protocolMajor": 3, "hostBuildId": HOST,
            "expectedProtocolContractSha256": hashlib.sha256(rust_bytes).hexdigest(),
            "expectedIdentity": dict(rust_identity), "expectedCapabilities": srt(row),
            "identityVersions": dict(versions), "limits": dict(rust_limits)}


def rust_ack(row):
    ack = {"protocolMajor": 3, "capabilities": srt(row), "identityVersions": dict(versions)}
    for k in ("providerBuildId", "rustCommitHash", "hostTriple", "targetTriple", "sysrootDigest"):
        ack[k] = rust_identity[k]
    return ack


def candidate(ordinal, language, producer, build, target):
    decoded = {"resolvedTarget": target, "specifier": "./" + target.rsplit("/", 1)[-1]}
    return {"candidateOrdinal": ordinal, "relation": "imports", "resolution": "resolved-target", "layer": "semantic",
            "producer": producer, "producerVersion": build, "schemaVersion": 1, "language": language,
            "sourceUniverseId": "u-src", "targetUniverseId": "u-src", "confidenceMillionths": 1000000,
            "relationSchemaId": "opensip.relation.imports.v1",
            "canonicalRelationPayloadHex": cbor2.dumps(decoded, canonical=True).hex(),
            "decodedRelationPayload": decoded,
            "anchors": [{"path": "src/a", "startByte": 0, "endByte": 10}]}


def wire(c):
    w = {k: v for k, v in c.items() if k not in ("canonicalRelationPayloadHex", "decodedRelationPayload")}
    w["canonicalRelationPayload"] = bytes.fromhex(c["canonicalRelationPayloadHex"])
    return w


ts_cands = [candidate(0, "typescript", "typescript-semantic", ts_provider["providerBuildId"], "src/b.ts"),
            candidate(1, "typescript", "typescript-semantic", ts_provider["providerBuildId"], "src/c.ts")]
rust_cands = [candidate(0, "rust", "rust-semantic", rust_identity["providerBuildId"], "src/b.rs"),
              candidate(1, "rust", "rust-semantic", rust_identity["providerBuildId"], "src/c.rs")]
ts_facts_cbor = cbor2.dumps([wire(c) for c in ts_cands], canonical=True)
domain = ts_sub["providerProtocol"]["wireSchema"]["commitments"]["domains"]["factBatch"]
ts_commitment = "sha256:" + hashlib.sha256(domain.encode("utf-8") + b"\x00" + ts_facts_cbor).hexdigest()

hello_missing_limit = ts_hello(fx["ts2"])
del hello_missing_limit["limits"]["maxStderrBytes"]
ack_missing_digest = ts_ack(fx["ts2"])
del ack_missing_digest["typescriptCompilerSha256"]
rust_wrong_token_row = [t for t in fx["rust3"] if t != "rust-semantic-facts-v1"] + ["typescript-semantic-facts-v1"]

new_fixtures = {
    "wireTsProviderDescriptor": ts_provider,
    "wireTsRuntimeDescriptor": ts_runtime,
    "wireTsProtocolLimits": dict(ts_limits),
    "wireRustProtocolLimitsV3": dict(rust_limits),
    "wireTsHello": ts_hello(fx["ts2"]),
    "wireTsHelloAck": ts_ack(fx["ts2"]),
    "wireTsHelloAttribution": ts_hello(fx["ts2Attribution"]),
    "wireTsHelloAckAttribution": ts_ack(fx["ts2Attribution"]),
    "wireTsHelloAsSupersededRustShape": {"protocolMajor": 2, "expectedCapabilities": srt(fx["ts2"]),
                                         "identityVersions": dict(versions), "limits": dict(successor8)},
    "wireTsHelloMissingLegacyLimit": hello_missing_limit,
    "wireTsHelloAckMissingCompilerDigest": ack_missing_digest,
    "wireRustIdentity": rust_identity,
    "wireRustHello": rust_hello(fx["rust3"]),
    "wireRustHelloAck": rust_ack(fx["rust3"]),
    "wireRustHelloAttribution": rust_hello(fx["rust3Attribution"]),
    "wireRustHelloAckAttribution": rust_ack(fx["rust3Attribution"]),
    "wireRustHelloSupersededShape": {"protocolMajor": 3, "expectedCapabilities": srt(fx["rust3"]),
                                     "identityVersions": dict(versions), "limits": dict(successor8)},
    "wireRustHelloEightLimits": dict(rust_hello(fx["rust3"]), limits=dict(successor8)),
    "wireRustHelloTypeScriptToken": dict(rust_hello(fx["rust3"]), expectedCapabilities=srt(rust_wrong_token_row)),
    "wireTsFactBatchV1": {"analysisOrdinal": 0, "stageId": "s-imports", "batchIndex": 0, "facts": ts_cands,
                          "batchCommitment": ts_commitment},
    "wireTsFactsWireCborHex": ts_facts_cbor.hex(),
    "wireRustFactBatchV2": {"analysisOrdinal": 0, "stageId": "s-imports", "batchIndex": 0, "candidates": rust_cands},
    "wireTsFactBatchV3": {"schemaVersion": 3, "analysisOrdinal": 0, "stageId": "s-imports", "batchIndex": 0,
                          "candidates": ts_cands, "occupancyCompanions": []},
    "wireRustFactBatchV3": {"schemaVersion": 3, "analysisOrdinal": 0, "stageId": "s-imports", "batchIndex": 0,
                            "candidates": rust_cands, "occupancyCompanions": []},
}
assert not set(new_fixtures) & set(fx)

TS, RS = "typescript-semantic", "rust-semantic"
TS_EXP = {"hostBuildId": HOST, "providerDescriptor": "$fixtures.wireTsProviderDescriptor",
          "runtimeDescriptor": "$fixtures.wireTsRuntimeDescriptor"}
TS_ACK_EXP = {"providerDescriptor": "$fixtures.wireTsProviderDescriptor",
              "runtimeDescriptor": "$fixtures.wireTsRuntimeDescriptor"}
RS_EXP = {"hostBuildId": HOST, "identity": "$fixtures.wireRustIdentity"}
DISPATCH = {"stageId": "s-imports", "analysisOrdinal": 0, "batchIndex": 0, "firstCandidateOrdinal": 0}


def hello_step(language, hello, row, expected, major, bind="r", error=None):
    step = {"fn": "admit_provider_hello", "args": {"language": language, "hello": hello, "envelope_protocol_major": major,
                                                   "signed_row": row, "expected": expected}, "bind": bind}
    if error:
        step["expectError"] = error
    return step


def ack_step(language, hello, ack, expected, major, bind="r", error=None):
    step = {"fn": "admit_provider_hello_ack", "args": {"language": language, "hello": hello, "ack": ack,
                                                       "envelope_protocol_major": major, "expected": expected},
            "bind": bind}
    if error:
        step["expectError"] = error
    return step


def batch_step(language, batch, tokens, bind="r", error=None, expected=DISPATCH):
    step = {"fn": "admit_provider_fact_batch", "args": {"language": language, "batch": batch,
                                                        "negotiated_tokens": tokens, "expected": expected},
            "bind": bind}
    if error:
        step["expectError"] = error
    return step


def merge(base, **with_):
    return {"$merge": base, "$with": with_}


def case(cid, kind, steps, expect=None):
    return {"id": "provider-wire-" + cid, "feedback": ["F1"], "kind": kind, "steps": steps, "expect": expect or {}}


cases = [
    case("ts2-hello-admits-inherited-descriptor-digests-and-ten-legacy-limits", "positive",
         [hello_step(TS, "$fixtures.wireTsHello", "$fixtures.ts2", TS_EXP, 2)],
         {"$r.outcome": "hello-admitted", "$r.protocolMajor": 2, "$r.sourceBytesSent": False,
          "$r.targetAttributionOffered": False}),
    case("ts2-hello-ack-echoes-descriptors-tokens-and-identity-versions", "positive",
         [ack_step(TS, "$fixtures.wireTsHello", "$fixtures.wireTsHelloAck", TS_ACK_EXP, 2)],
         {"$r.outcome": "accepted", "$r.identityNegotiated": True, "$r.targetAttributionNegotiated": False,
          "$r.sourceBytesSent": False, "$r.next": "OpenUniverse"}),
    case("rust3-hello-admits-identity-contract-digest-and-32-limits", "positive",
         [hello_step(RS, "$fixtures.wireRustHello", "$fixtures.rust3", RS_EXP, 3)],
         {"$r.outcome": "hello-admitted", "$r.protocolMajor": 3, "$r.sourceBytesSent": False}),
    case("rust3-hello-ack-echoes-expected-identity", "positive",
         [ack_step(RS, "$fixtures.wireRustHello", "$fixtures.wireRustHelloAck", {}, 3)],
         {"$r.outcome": "accepted", "$r.identityNegotiated": True, "$r.targetAttributionNegotiated": False}),
    case("target-attribution-negotiated-in-both-languages", "positive",
         [hello_step(TS, "$fixtures.wireTsHelloAttribution", "$fixtures.ts2Attribution", TS_EXP, 2, bind="th"),
          ack_step(TS, "$fixtures.wireTsHelloAttribution", "$fixtures.wireTsHelloAckAttribution", TS_ACK_EXP, 2, bind="ta"),
          hello_step(RS, "$fixtures.wireRustHelloAttribution", "$fixtures.rust3Attribution", RS_EXP, 3, bind="rh"),
          ack_step(RS, "$fixtures.wireRustHelloAttribution", "$fixtures.wireRustHelloAckAttribution", {}, 3, bind="ra")],
         {"$th.targetAttributionOffered": True, "$ta.targetAttributionNegotiated": True,
          "$rh.targetAttributionOffered": True, "$ra.targetAttributionNegotiated": True}),
    case("per-language-limit-maps-equal-the-published-inherited-values", "positive",
         [{"fn": "provider_wire_limits", "args": {"language": TS}, "bind": "t"},
          {"fn": "provider_wire_limits", "args": {"language": RS}, "bind": "u"}],
         {"$t": "$fixtures.wireTsProtocolLimits", "$u": "$fixtures.wireRustProtocolLimitsV3",
          "$t.maxFactBatchFacts": 4096, "$u.maxFactBatchCandidates": 4096}),
    case("ts-unnegotiated-fact-batch-v1-admits-with-hashlib-cbor2-commitment-oracle", "positive",
         [{"fn": "domainSha256Hex", "args": {"domain": domain, "hex": "$fixtures.wireTsFactsWireCborHex"}, "bind": "o"},
          batch_step(TS, "$fixtures.wireTsFactBatchV1", "$fixtures.ts2")],
         {"$r.payload": "FactBatchV1", "$r.candidateArray": "facts", "$r.batchCommitment": "$o",
          "$r.batchCommitmentVerified": True, "$r.perBatchCommitmentCarried": True,
          "$r.wireCandidatesCborHex": "$fixtures.wireTsFactsWireCborHex", "$r.candidateOrdinals": [0, 1]}),
    case("rust-unnegotiated-fact-batch-v2-admits-without-per-batch-commitment", "positive",
         [batch_step(RS, "$fixtures.wireRustFactBatchV2", "$fixtures.rust3")],
         {"$r.payload": "FactBatchV2", "$r.candidateArray": "candidates", "$r.batchCommitment": None,
          "$r.perBatchCommitmentCarried": False}),
    case("negotiated-fact-batch-v3-admits-in-both-languages-without-batch-commitment", "positive",
         [batch_step(TS, "$fixtures.wireTsFactBatchV3", "$fixtures.ts2Attribution", bind="t"),
          batch_step(RS, "$fixtures.wireRustFactBatchV3", "$fixtures.rust3Attribution", bind="u")],
         {"$t.payload": "FactBatchV3", "$t.batchCommitment": None, "$t.perBatchCommitmentCarried": False,
          "$u.payload": "FactBatchV3", "$u.negotiated": True}),
    # ---- TypeScript Hello / HelloAck refusals
    case("ts2-hello-in-the-superseded-major-3-shape-refused", "negative",
         [hello_step(TS, "$fixtures.wireTsHelloAsSupersededRustShape", "$fixtures.ts2", TS_EXP, 2,
                     error="SCHEMA:TypeScriptHelloV2")]),
    case("ts2-hello-omitting-a-legacy-limit-refused", "negative",
         [hello_step(TS, "$fixtures.wireTsHelloMissingLegacyLimit", "$fixtures.ts2", TS_EXP, 2,
                     error="'maxStderrBytes' is a required property")]),
    case("ts2-hello-carrying-limit-rule-as-a-member-refused", "negative",
         [hello_step(TS, merge("$fixtures.wireTsHello", **{"limits.limitRule": "policy text"}), "$fixtures.ts2", TS_EXP, 2,
                     error="Additional properties are not allowed")]),
    case("ts2-hello-changed-limit-value-refused", "negative",
         [hello_step(TS, merge("$fixtures.wireTsHello", **{"limits.maxAnalyzeStages": 256}), "$fixtures.ts2", TS_EXP, 2,
                     error="SCHEMA:TypeScriptHelloV2:/limits/maxAnalyzeStages")]),
    case("ts2-hello-token-array-out-of-utf8-order-refused", "negative",
         [hello_step(TS, merge("$fixtures.wireTsHello", expectedCapabilities=list(reversed(srt(fx["ts2"])))),
                     "$fixtures.ts2", TS_EXP, 2, error="array order utf8")]),
    case("ts2-hello-under-envelope-major-1-refused", "negative",
         [hello_step(TS, "$fixtures.wireTsHello", "$fixtures.ts2", TS_EXP, 1, error="PROTOCOL_MAJOR")]),
    case("ts2-hello-descriptor-digest-not-the-verified-descriptor-refused", "negative",
         [hello_step(TS, "$fixtures.wireTsHello", "$fixtures.ts2",
                     dict(TS_EXP, providerDescriptor=merge("$fixtures.wireTsProviderDescriptor", typescriptVersion="5.6.4")),
                     2, error="DESCRIPTOR_DIGEST:provider")]),
    case("ts2-hello-tokens-not-the-signed-row-refused", "negative",
         [hello_step(TS, "$fixtures.wireTsHello", "$fixtures.ts2Attribution", TS_EXP, 2, error="CAPABILITIES")]),
    case("ts2-hello-ack-changed-runtime-descriptor-echo-refused", "negative",
         [ack_step(TS, "$fixtures.wireTsHello", merge("$fixtures.wireTsHelloAck", nodeVersion="22.9.1"), TS_ACK_EXP, 2,
                   error="DESCRIPTOR_FIELD:nodeVersion")]),
    case("ts2-hello-ack-changed-provider-build-echo-refused", "negative",
         [ack_step(TS, "$fixtures.wireTsHello", merge("$fixtures.wireTsHelloAck", providerBuildId="ts-provider-other"),
                   TS_ACK_EXP, 2, error="DESCRIPTOR_FIELD:providerBuildId")]),
    case("ts2-hello-ack-dropping-a-descriptor-member-refused", "negative",
         [ack_step(TS, "$fixtures.wireTsHello", "$fixtures.wireTsHelloAckMissingCompilerDigest", TS_ACK_EXP, 2,
                   error="'typescriptCompilerSha256' is a required property")]),
    case("ts2-hello-ack-major-1-refused", "negative",
         [ack_step(TS, "$fixtures.wireTsHello", merge("$fixtures.wireTsHelloAck", protocolMajor=1), TS_ACK_EXP, 2,
                   error="SCHEMA:TypeScriptHelloAckV2:/protocolMajor")]),
    case("ts2-hello-ack-token-echo-mismatch-refused", "negative",
         [ack_step(TS, "$fixtures.wireTsHello", "$fixtures.wireTsHelloAckAttribution", TS_ACK_EXP, 2,
                   error="CAPABILITY_ECHO")]),
    case("ts2-hello-ack-extra-member-refused", "negative",
         [ack_step(TS, "$fixtures.wireTsHello", merge("$fixtures.wireTsHelloAck", hostBuildId=HOST), TS_ACK_EXP, 2,
                   error="Additional properties are not allowed")]),
    case("ts2-hello-ack-runtime-descriptor-digest-echo-mismatch-refused", "negative",
         [ack_step(TS, "$fixtures.wireTsHello", merge("$fixtures.wireTsHelloAck", runtimeDescriptorSha256="00" * 32),
                   TS_ACK_EXP, 2, error="DESCRIPTOR_DIGEST_ECHO:runtime")]),
    # ---- Rust Hello / HelloAck refusals
    case("rust3-hello-in-the-superseded-four-member-shape-refused", "negative",
         [hello_step(RS, "$fixtures.wireRustHelloSupersededShape", "$fixtures.rust3", RS_EXP, 3,
                     error="SCHEMA:HelloV3")]),
    case("rust3-hello-with-only-the-eight-successor-limits-refused", "negative",
         [hello_step(RS, "$fixtures.wireRustHelloEightLimits", "$fixtures.rust3", RS_EXP, 3,
                     error="SCHEMA:HelloV3:/limits")]),
    case("rust3-hello-with-a-typescript-token-refused", "negative",
         [hello_step(RS, "$fixtures.wireRustHelloTypeScriptToken", "$fixtures.rust3", RS_EXP, 3,
                     error="SCHEMA:HelloV3:/expectedCapabilities")]),
    case("rust3-hello-contract-digest-not-the-selected-artifact-refused", "negative",
         [hello_step(RS, merge("$fixtures.wireRustHello", expectedProtocolContractSha256="00" * 32), "$fixtures.rust3",
                     RS_EXP, 3, error="CONTRACT_DIGEST")]),
    case("rust3-hello-identity-not-the-plan-row-refused", "negative",
         [hello_step(RS, "$fixtures.wireRustHello", "$fixtures.rust3",
                     dict(RS_EXP, identity=merge("$fixtures.wireRustIdentity", sysrootDigest="7c" * 32)), 3,
                     error="EXPECTED_IDENTITY:sysrootDigest")]),
    case("rust3-hello-under-envelope-major-2-refused", "negative",
         [hello_step(RS, "$fixtures.wireRustHello", "$fixtures.rust3", RS_EXP, 2, error="PROTOCOL_MAJOR")]),
    case("rust3-hello-ack-changed-identity-echo-refused", "negative",
         [ack_step(RS, "$fixtures.wireRustHello", merge("$fixtures.wireRustHelloAck", rustCommitHash="6d" * 32), {}, 3,
                   error="IDENTITY_ECHO:rustCommitHash")]),
    case("rust3-hello-ack-major-2-refused", "negative",
         [ack_step(RS, "$fixtures.wireRustHello", merge("$fixtures.wireRustHelloAck", protocolMajor=2), {}, 3,
                   error="SCHEMA:HelloAckV3:/protocolMajor")]),
    case("rust3-hello-ack-identity-versions-changed-refused", "negative",
         [ack_step(RS, "$fixtures.wireRustHello", merge("$fixtures.wireRustHelloAck", **{"identityVersions.coverage": 2}),
                   {}, 3, error="SCHEMA:HelloAckV3:/identityVersions/coverage")]),
    # ---- FactBatch refusals
    case("ts-fact-batch-v1-wrong-batch-commitment-refused", "negative",
         [batch_step(TS, merge("$fixtures.wireTsFactBatchV1", batchCommitment="sha256:" + "00" * 32), "$fixtures.ts2",
                     error="BATCH_COMMITMENT")]),
    case("ts-unnegotiated-rust-v2-shape-refused", "negative",
         [batch_step(TS, "$fixtures.wireRustFactBatchV2", "$fixtures.ts2", error="SCHEMA:TypeScriptFactBatchV1Vector")]),
    case("rust-unnegotiated-ts-v1-shape-refused", "negative",
         [batch_step(RS, "$fixtures.wireTsFactBatchV1", "$fixtures.rust3", error="SCHEMA:RustFactBatchV2Vector")]),
    case("fact-batch-v3-without-token-refused", "negative",
         [batch_step(TS, "$fixtures.wireTsFactBatchV3", "$fixtures.ts2", error="UNNEGOTIATED_V3")]),
    case("historical-fact-batch-with-token-refused-in-both-languages", "negative",
         [batch_step(TS, "$fixtures.wireTsFactBatchV1", "$fixtures.ts2Attribution", bind="t",
                     error="HISTORICAL_WITH_TOKEN:FactBatchV1"),
          batch_step(RS, "$fixtures.wireRustFactBatchV2", "$fixtures.rust3Attribution", bind="u",
                     error="HISTORICAL_WITH_TOKEN:FactBatchV2")]),
    case("candidate-payload-hex-not-cbor-of-decoded-payload-refused", "negative",
         [batch_step(TS, merge("$fixtures.wireTsFactBatchV1", **{"facts.0.canonicalRelationPayloadHex": "a0"}),
                     "$fixtures.ts2", error="CANDIDATE_PAYLOAD_CBOR:0")]),
    case("ts-fact-batch-v3-nonzero-analysis-ordinal-refused", "negative",
         [batch_step(TS, merge("$fixtures.wireTsFactBatchV3", analysisOrdinal=1), "$fixtures.ts2Attribution",
                     error="ANALYSIS_ORDINAL", expected=None)]),
]


def indent_block(text, prefix):
    lines = text.split("\n")
    return "\n".join([lines[0]] + [prefix + line for line in lines[1:]])


raw = original_raw.decode("utf-8")
fixture_anchor = "\n },\n \"cases\": [\n"
case_anchor = "\n ],\n \"revision\":"
assert raw.count(fixture_anchor) == 1 and raw.count(case_anchor) == 1
fixture_text = "".join(",\n  " + json.dumps(k) + ": " + indent_block(json.dumps(v, indent=1), "  ")
                       for k, v in new_fixtures.items())
case_text = "".join(",\n  " + indent_block(json.dumps(c, indent=1), "  ") for c in cases)
raw = raw.replace(fixture_anchor, fixture_text + fixture_anchor, 1)
raw = raw.replace(case_anchor, case_text + case_anchor, 1)
updated = json.loads(raw)
assert updated["cases"][:len(original["cases"])] == original["cases"]
assert {k: updated["fixtures"][k] for k in original["fixtures"]} == original["fixtures"]
assert len(updated["cases"]) == len(original["cases"]) + len(cases)
assert {k: v for k, v in updated.items() if k not in ("cases", "fixtures")} == \
    {k: v for k, v in original.items() if k not in ("cases", "fixtures")}
CASES.write_bytes(raw.encode("utf-8"))
print(json.dumps({"addedFixtures": len(new_fixtures), "addedCases": len(cases), "totalCases": len(updated["cases"]),
                  "sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest()}))
