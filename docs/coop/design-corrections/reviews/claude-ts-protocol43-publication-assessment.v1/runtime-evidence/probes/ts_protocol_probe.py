"""Reference-only probe on frozen43. Reads frozen bytes; writes nothing there.

Not compiler/worker qualification. Shows only what the design reference
models and schemas do and do not discriminate for typescript-semantic major 2.
"""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/candidate-subject.v43/docs/coop/design-corrections")
OUT = Path(__file__).resolve().parent / "probe-output.json"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("probe_return", ROOT / "foundation" / "provider_attribution_return_model.v2.py")
N = load("probe_native", ROOT / "native" / "native_evidence_model.v2.py")

results = {}


def outcome(fn):
    try:
        return {"ok": True, "value": fn()}
    except Exception as exc:  # reference refusal is the observation
        return {"ok": False, "error": type(exc).__name__, "detail": str(exc)[:300]}


cand = {
    "candidateOrdinal": 0, "relation": "imports", "resolution": "semantic-resolved",
    "layer": "semantic", "producer": "typescript-semantic", "producerVersion": "b",
    "schemaVersion": 1, "language": "typescript", "sourceUniverseId": "u",
    "targetUniverseId": "u", "confidenceMillionths": 1000000, "relationSchemaId": "x",
    "canonicalRelationPayloadHex": "a0", "decodedRelationPayload": {}, "anchors": [{}],
}
ts_v1 = {"analysisOrdinal": 0, "stageId": "s", "batchIndex": 0, "facts": [cand],
         "batchCommitment": "sha256:" + "00" * 32}
rust_v2 = {"analysisOrdinal": 0, "stageId": "s", "batchIndex": 0, "candidates": [cand]}
v3 = dict(rust_v2, schemaVersion=3, occupancyCompanions=[])
junk = {"not": "a batch"}

TS_NO_TOKEN = list(N.TS2_TOKENS)

for label, batch in (("tsFactBatchV1Shape", ts_v1), ("factBatchV2Shape", rust_v2), ("junk", junk)):
    results["tokenAbsent." + label] = outcome(lambda b=batch: M._token_gate(b, TS_NO_TOKEN))
results["tokenAbsent.factBatchV3"] = outcome(lambda: M._token_gate(v3, TS_NO_TOKEN))

for label, batch in (("tsFactBatchV1Shape", ts_v1), ("factBatchV2Shape", rust_v2), ("factBatchV3", v3)):
    results["v3Schema." + label] = outcome(lambda b=batch: (M.validate_schema(M.BATCH_SCHEMA, b), "valid")[1])

hello_ids = {"snapshot": 2, "plan": 2, "fact": 2, "coverage": 3}
limits3 = {"maxDependencySourcePackages": 4096, "maxDependencySourceEntries": 1000000,
           "maxDependencySourceTotalBytes": 8589934592, "maxDependencySourceChunkBytes": 1048576,
           "maxUnresolvedEdgesPerStage": 1000000, "maxCfgSets": 4, "maxExpansionRows": 1000000,
           "maxGeneratedFileRows": 1000000}
for major in (2, 3):
    hello = {"protocolMajor": major, "expectedCapabilities": TS_NO_TOKEN,
             "identityVersions": hello_ids, "limits": limits3}
    ack = {"protocolMajor": major, "capabilities": TS_NO_TOKEN, "identityVersions": hello_ids}
    results["HelloV3.major%d" % major] = outcome(lambda h=hello: (N.validate_native("HelloV3", h), "valid")[1])
    results["HelloAckV3.major%d" % major] = outcome(lambda a=ack: (N.validate_native("HelloAckV3", a), "valid")[1])

ts_limits = json.loads((ROOT.parents[1] / "coop" / "artifacts" / "delivery.v2.json").read_text(encoding="utf-8"))
ts_limits = {k: v for k, v in ts_limits["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]["limits"].items()
             if k != "limitRule"}
results["ProtocolLimitsV3.tsDeliveryV2Limits"] = outcome(lambda: (N.validate_native("ProtocolLimitsV3", ts_limits), "valid")[1])
results["negotiate.ts2"] = outcome(lambda: N.negotiate(TS_NO_TOKEN, TS_NO_TOKEN, TS_NO_TOKEN))

OUT.write_text(json.dumps(results, indent=1, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(results, indent=1, sort_keys=True))
sys.exit(0)
