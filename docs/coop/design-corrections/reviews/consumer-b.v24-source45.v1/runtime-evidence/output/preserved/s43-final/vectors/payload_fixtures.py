"""Own fixtures for the FactBatch payload/correlation vectors (source42.v3). Records are built from kit registries (ref/factbatch.py):
relation schema ids and layers come from fact-plane, and the payload hex is my deterministic-CBOR encoding of the decoded payload.

The retained Plan fragment is a host observation: execution-plan rows (ordinal, stageSpecDigest), stage specs (planId, stageId,
producerClosure) and closure kinds. It is not an admitted ExecutionPlan record. Analyze objects carry only the correlation members
of AnalyzeV1/StageRequestV1 (delivery.v2) and AnalyzeV2/StageRequestV2 (rust-provider-protocol.v2); the other closed members do
not enter FactBatch correlation and are not constructed here."""
import copy
import hashlib
import json
import sys

sys.path.insert(0, '/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/ref')
import factbatch as FB  # noqa: E402
import protocol3 as P  # noqa: E402


def h(label):
    return hashlib.sha256(label.encode()).hexdigest()


PLAN_ID = "plan2:" + h("cb24.source42.v3.payload-plan")
OTHER_PLAN_ID = "plan2:" + h("cb24.source42.v3.other-plan")
CLOSURE = {"syntax": "closure2:" + h("closure:syntax-provider"), "ts": "closure2:" + h("closure:typescript-semantic"),
           "rust": "closure2:" + h("closure:rust-semantic")}
UNIV = {"ts": "sha256:" + h("universe:ts"), "ts-external": "sha256:" + h("universe:npm-external"),
        "rust": "sha256:" + h("universe:rust"), "rust-dep": "sha256:" + h("universe:rust-dependency")}
# Plan stage order; TypeScript Analyze selects retained ordinals 1 and 3 as request ordinals 0 and 1; Rust Analyze selects 2 as 0.
PLAN_STAGES = [("syntax-declares", "syntax"), ("ts-imports", "ts"), ("rust-calls", "rust"), ("ts-calls", "ts")]


def retained():
    specs, rows = {}, []
    for ordinal, (sid, prov) in enumerate(PLAN_STAGES):
        spec = {"planId": PLAN_ID, "stageId": sid, "producerClosure": CLOSURE[prov]}
        d = h(json.dumps(spec, sort_keys=True))
        specs[d] = spec
        rows.append({"ordinal": ordinal, "stageSpecDigest": d})
    return {"planId": PLAN_ID, "executionPlan": {"planId": PLAN_ID, "stages": rows}, "stageSpecs": specs,
            "closures": {c: {"kind": "provider"} for c in CLOSURE.values()}}


RETAINED = retained()
HOST = {"ts": {"providerId": "typescript-semantic", "providerVersion": "typescript-provider:1", "language": "typescript",
               "sourceUniverseId": UNIV["ts"], "allowedTargetUniverseIds": [UNIV["ts"], UNIV["ts-external"]]},
        "rust": {"providerId": "rust-semantic", "providerVersion": "rust-provider:1", "language": "rust",
                 "sourceUniverseId": UNIV["rust"], "allowedTargetUniverseIds": [UNIV["rust"], UNIV["rust-dep"]]}}

LIMITS = {"maxDependencySourcePackages": 4096, "maxDependencySourceEntries": 1000000, "maxDependencySourceTotalBytes": 8589934592,
          "maxDependencySourceChunkBytes": 1048576, "maxUnresolvedEdgesPerStage": 1000000, "maxCfgSets": 4,
          "maxExpansionRows": 1000000, "maxGeneratedFileRows": 1000000}
CAPS = {"rust": P.IDENTITY_TOKENS + ["sealed-vfs-v1", "multi-stage-analyze-v1", "rust-semantic-facts-v1", "resolution-completeness-v2",
                                     "unresolved-edge-v1", "dependency-source-v1", "prepared-output-v3", "native-context-v2", FB.TOKEN],
        "ts": P.IDENTITY_TOKENS + ["sealed-vfs-v1", "multi-stage-analyze-v1", "typescript-semantic-facts-v1", "resolution-completeness-v2",
                                   "unresolved-edge-v1", "native-context-v2", FB.TOKEN]}
MAJOR = {"rust": 3, "ts": 2}


def caps(shape, token=True):
    return [c for c in CAPS[shape] if token or c != FB.TOKEN]


def hello(shape, token=True):
    return {"frame": "Hello", "protocolMajor": MAJOR[shape], "expectedCapabilities": caps(shape, token), "identityVersions": P.IDENTITY_VERSIONS, "limits": LIMITS}


def ack(shape, token=True):
    return {"frame": "HelloAck", "protocolMajor": MAJOR[shape], "capabilities": caps(shape, token), "identityVersions": P.IDENTITY_VERSIONS}


def analyze(shape, analysis_ordinal=0):
    if shape == "ts":
        return {"analysisOrdinal": analysis_ordinal, "stageRequests": [{"stageId": "ts-imports", "stageOrdinal": 0, "relations": ["imports"]},
                                                                       {"stageId": "ts-calls", "stageOrdinal": 1, "relations": ["calls"]}]}
    return {"analysisOrdinal": analysis_ordinal, "stages": [{"stageOrdinal": 0, "planStage": {"kind": "fact-derivation", "stageId": "rust-calls", "relations": ["calls"]}}]}


def analyze_event(shape):
    a = analyze(shape)
    return {"frame": "Analyze", "stageCount": len(a["stageRequests"] if shape == "ts" else a["stages"]), "analyze": a}


def anchor(shape):
    path = "src/a.ts" if shape == "ts" else "src/lib.rs"
    return {"kind": "source-span", "snapshotId": "snap1:sha256:" + h("snapshot"), "path": path, "contentSha256": h(path),
            "startByte": 0, "endByte": 10, "factId": None}


def cand(shape, ordinal, relation, resolution, decoded, target=None):
    ctx, s = HOST[shape], FB.REG["schemas"][relation]
    return {"candidateOrdinal": ordinal, "relation": relation, "resolution": resolution, "layer": FB.RELREG["relations"][relation]["layer"],
            "producer": ctx["providerId"], "producerVersion": ctx["providerVersion"], "schemaVersion": s["schemaVersion"], "language": ctx["language"],
            "sourceUniverseId": ctx["sourceUniverseId"], "targetUniverseId": target or ctx["sourceUniverseId"], "confidenceMillionths": 1000000,
            "relationSchemaId": s["schemaId"], "canonicalRelationPayloadHex": FB.cbor_encode(decoded).hex(), "decodedRelationPayload": decoded,
            "anchors": [anchor(shape)]}


def comp(ordinal, target_universe, target_native, kind, occupancy, exported=None, logical=None, manifest=None, evaluation=None):
    return {"schemaVersion": 1, "candidateOrdinal": ordinal, "targetUniverseId": target_universe, "targetNativeId": target_native, "kind": kind,
            "occupancy": occupancy, "exported": exported, "logicalPath": logical, "packageManifestPath": manifest, "evaluationNativeId": evaluation}


def imports_b0():
    return ([cand("ts", 0, "imports", "resolved-target", {"importer": "sym:module:src/a.ts", "specifier": "./b", "resolvedTarget": "file:src/b.ts"}),
             cand("ts", 1, "imports", "syntactic-specifier", {"importer": "sym:module:src/a.ts", "specifier": "./missing"}),
             cand("ts", 2, "imports", "resolved-target", {"importer": "sym:module:src/a.ts", "specifier": "left-pad", "resolvedTarget": "pkg:npm/left-pad"},
                  target=UNIV["ts-external"])],
            [comp(0, UNIV["ts"], "file:src/b.ts", "file", "first-party", evaluation="src/b.ts"),
             comp(2, UNIV["ts-external"], "pkg:npm/left-pad", "package", "external", manifest="node_modules/left-pad/package.json")])


def imports_b1():
    return ([cand("ts", 3, "imports", "resolved-target", {"importer": "sym:module:src/a.ts", "specifier": "./c", "resolvedTarget": "sym:function:src/c.ts#g"}),
             cand("ts", 4, "imports", "resolved-target", {"importer": "sym:module:src/a.ts", "specifier": "../vendor/outside", "resolvedTarget": "file:vendor/outside.ts"}),
             cand("ts", 5, "imports", "resolved-target", {"importer": "sym:module:src/a.ts", "specifier": "@ws/core", "resolvedTarget": "pkg:workspace/core"})],
            [comp(3, UNIV["ts"], "sym:function:src/c.ts#g", "symbol", "first-party", exported="exported", evaluation="sym:function:src/c.ts#g"),
             comp(4, UNIV["ts"], "file:vendor/outside.ts", "file", "external", logical="vendor/outside.ts"),
             comp(5, UNIV["ts"], "pkg:workspace/core", "package", "first-party", manifest="packages/core/package.json", evaluation="core")])


def calls_b0():
    return ([cand("ts", 0, "calls", "resolved-callee", {"caller": "sym:function:src/a.ts#main", "calleeText": "helper", "resolvedCallee": "sym:function:src/c.ts#helper"}),
             cand("ts", 1, "calls", "syntactic-callee-name", {"caller": "sym:function:src/a.ts#main", "calleeText": "dynamicThing"})],
            [comp(0, UNIV["ts"], "sym:function:src/c.ts#helper", "unknown", "unknown")])


def rust_calls_b0():
    return ([cand("rust", 0, "calls", "resolved-callee", {"caller": "sym:function:main", "calleeText": "helper", "resolvedCallee": "sym:function:helper"},
                  target=UNIV["rust-dep"]),
             cand("rust", 1, "calls", "resolved-callee", {"caller": "sym:function:main", "calleeText": "local", "resolvedCallee": "sym:function:local"})],
            [comp(0, UNIV["rust-dep"], "sym:function:helper", "symbol", "external", exported="unknown", logical="src/lib.rs"),
             comp(1, UNIV["rust"], "sym:function:local", "symbol", "first-party", exported="not-exported", evaluation="sym:function:local")])


def v3(stage_id, batch_index, pair, analysis_ordinal=0):
    cands, comps = copy.deepcopy(pair)
    return {"schemaVersion": 3, "analysisOrdinal": analysis_ordinal, "stageId": stage_id, "batchIndex": batch_index, "candidates": cands, "occupancyCompanions": comps}


def v2(batch):
    return {k: copy.deepcopy(batch[k]) for k in ("analysisOrdinal", "stageId", "batchIndex", "candidates")}


def renumber(batch, start):
    """Renumber candidates (and companions by the same offset) to begin at `start`."""
    b = copy.deepcopy(batch)
    off = start - b["candidates"][0]["candidateOrdinal"]
    for c in b["candidates"]:
        c["candidateOrdinal"] += off
    for c in b.get("occupancyCompanions", []):
        c["candidateOrdinal"] += off
    return b


def fb(payload):
    return {"frame": "FactBatch", "payload": payload}
