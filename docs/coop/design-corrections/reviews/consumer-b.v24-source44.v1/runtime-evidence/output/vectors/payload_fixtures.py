"""Own fixtures for the provider payload and trace vectors.

source42.v3: FactBatch records are built from kit registries (ref/factbatch.py). Relation schema ids and layers come from fact-plane, and the payload
hex is my deterministic-CBOR encoding of the decoded payload.

The retained Plan fragment is a host observation: execution-plan rows (ordinal, stageSpecDigest), stage specs (planId, stageId, producerClosure)
and closure kinds. It is not an admitted ExecutionPlan record. Analyze objects carry only the correlation members of AnalyzeV1/StageRequestV1
(delivery.v2) and AnalyzeV2/StageRequestV2 (rust-provider-protocol.v2).

source44 (HC-58) adds handshake, startup, coverage, terminal and cancellation payload fixtures (native/provider-handshake.schemas.v1.json,
native/provider-startup.schemas.v1.json). Sources:
  - resolvedInputs, native context ids, snapshot2 ids and CoverageResultV3 records come from my own retained ts-pass and rust-mixed Run stores
    (runs/<name>.store.json), read through ref/store.py;
  - descriptors, the rust-v1 identity row, artifact digests and the host build id are synthetic trusted host inputs;
  - the fixture Plan of an exchange is the retained Plan fragment's PLAN_ID with that language's retained snapshot2 and nativeContextDigests.
    It is a host input, not a verified Plan (native-evidence s9.7 reference scope);
  - every Analyze event carries hostDomains, the host-derived requested coverage domain per stage (keys in relation-ladder order plus the host subject
    count). This is a host observation. The keys of a rung other than the retained one reuse the retained scope commitment as a placeholder;
  - wrapper coverageCommitment values are placeholders: s9.7 Coverage checks do not recompute commitments.
The source43 bytes of this file are preserved at preserved/s43-final/vectors/payload_fixtures.py.
"""
import copy
import hashlib
import json
import sys

OUTP = '/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/'
sys.path.insert(0, OUTP + 'ref')
import canonical as K  # noqa: E402
import factbatch as FB  # noqa: E402
import native_facts as NF  # noqa: E402
import protocol3 as P  # noqa: E402
import provider_wire as W  # noqa: E402
from store import Store  # noqa: E402


def h(label):
    return hashlib.sha256(label.encode()).hexdigest()


PLAN_ID = "plan2:" + h("cb24.source42.v3.payload-plan")
OTHER_PLAN_ID = "plan2:" + h("cb24.source42.v3.other-plan")
CLOSURE = {"syntax": "closure2:" + h("closure:syntax-provider"), "ts": "closure2:" + h("closure:typescript-semantic"),
           "rust": "closure2:" + h("closure:rust-semantic")}

# ------------------------------------------------------------------------------------------------ retained Run values (source44)
FRAME_DOMAINS = {"native.semantic-universe.typescript.v2", "native.semantic-universe.rust.v2", "native.context.typescript.v2", "native.context.rust.v2",
                 "coverage"}


def _retained_run(name, word):
    exp = json.load(open(f"{OUTP}runs/{name}.store.json"))
    s = Store.load(exp)
    run = s.get_object(exp["runId"])
    plan = s.get_object(run["planId"])
    all_by_label = {}
    for hx, lab in exp["blobLabels"].items():
        all_by_label.setdefault(lab, []).append(hx)
    # only the labels read here must be unique in the store
    used = [lab for lab in all_by_label if lab.startswith(("native-universe:", "native-context:", "coverage-payload:", "coverage:"))]
    assert all(len(all_by_label[lab]) == 1 for lab in used), {lab: len(all_by_label[lab]) for lab in used if len(all_by_label[lab]) != 1}
    by_label = {lab: all_by_label[lab][0] for lab in used}
    uhex, chex = by_label[f"native-universe:{word}"], by_label[f"native-context:{word}"]
    udom, universe = s.get_frame(uhex, FRAME_DOMAINS)
    cdom, context = s.get_frame(chex, FRAME_DOMAINS)
    assert K.H(udom, universe) == uhex and K.H(cdom, context) == chex and universe["nativeContextId"] == "sha256:" + chex
    coverage = {}
    for lab, hx in by_label.items():
        if lab.startswith("coverage-payload:"):
            rel = lab.split(":", 1)[1]
            _, desc = s.get_frame(by_label["coverage:" + rel], FRAME_DOMAINS)
            coverage[rel] = {"payload": s.get_record(hx), "descriptor": desc, "coverageId": "coverage2:" + by_label["coverage:" + rel]}
    return {"run": name, "store": f"runs/{name}.store.json", "runId": exp["runId"],
            "plan": {"planId": run["planId"], "snapshotId": plan["snapshotId"], "nativeContextDigests": list(plan["nativeContextDigests"])},
            "universeDomain": udom, "universeHex": uhex, "universe": universe, "contextDomain": cdom, "contextHex": chex, "context": context,
            "coverage": coverage}


RET = {"ts": _retained_run("ts-pass", "typescript"), "rust": _retained_run("rust-mixed", "rust")}
UNIV = {"ts": "sha256:" + RET["ts"]["universeHex"], "ts-external": "sha256:" + h("universe:npm-external"),
        "rust": "sha256:" + RET["rust"]["universeHex"], "rust-dep": "sha256:" + h("universe:rust-dependency")}
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

# ------------------------------------------------------------------------------------------------ trusted host inputs (synthetic)
HS_DEFS = FB.K.doc(W.HS)["$defs"]
TS_PROVIDER_DESCRIPTOR = {"providerBuildId": "typescript-provider:cb24-source44", "protocolMajor": 2, "typescriptVersion": "5.4.5",
                          "typescriptCompilerSha256": h("typescript-compiler"), "typescriptStdlibMerkleRoot": h("typescript-stdlib"),
                          "defaultWorkBudgetProfileId": HS_DEFS["TypeScriptHelloAckV2"]["properties"]["defaultWorkBudgetProfileId"]["const"],
                          "defaultWorkBudgetProfileSha256": HS_DEFS["TypeScriptHelloAckV2"]["properties"]["defaultWorkBudgetProfileSha256"]["const"]}
TS_RUNTIME_DESCRIPTOR = {"nodeVersion": "20.11.1", "v8Version": "11.3.244.8", "modulesAbi": "115", "platformId": "darwin-arm64"}
RUST_V1_ROW = {"providerBuildId": "rust-provider:cb24-source44", "rustCommitHash": h("rust-commit"), "hostTriple": "aarch64-apple-darwin",
               "targetTriple": "aarch64-apple-darwin", "sysrootDigest": h("rust-sysroot")}
HOST_BUILD_ID = "opensip-host:cb24-source44"
HOST = {"ts": {"providerId": "typescript-semantic", "providerVersion": TS_PROVIDER_DESCRIPTOR["providerBuildId"], "language": "typescript",
               "sourceUniverseId": UNIV["ts"], "allowedTargetUniverseIds": [UNIV["ts"], UNIV["ts-external"]]},
        "rust": {"providerId": "rust-semantic", "providerVersion": RUST_V1_ROW["providerBuildId"], "language": "rust",
                 "sourceUniverseId": UNIV["rust"], "allowedTargetUniverseIds": [UNIV["rust"], UNIV["rust-dep"]]}}

CAPS = {"rust": P.IDENTITY_TOKENS + ["sealed-vfs-v1", "multi-stage-analyze-v1", "rust-semantic-facts-v1", "resolution-completeness-v2",
                                     "unresolved-edge-v1", "dependency-source-v1", "prepared-output-v3", "native-context-v2", FB.TOKEN],
        "ts": P.IDENTITY_TOKENS + ["sealed-vfs-v1", "multi-stage-analyze-v1", "typescript-semantic-facts-v1", "resolution-completeness-v2",
                                   "unresolved-edge-v1", "native-context-v2", FB.TOKEN]}


def caps(shape, token=True):
    """The selected signed capability row's tokens in strictly ascending UTF-8 byte order (provider-handshake x-opensip-wire-law capabilityArrays)."""
    return sorted((c for c in CAPS[shape] if token or c != FB.TOKEN), key=lambda t: t.encode("utf-8"))


def trusted(shape, token=True):
    t = {"hostBuildId": HOST_BUILD_ID, "signedRowTokens": caps(shape, token)}
    if shape == "ts":
        t.update(providerDescriptor=TS_PROVIDER_DESCRIPTOR, runtimeDescriptor=TS_RUNTIME_DESCRIPTOR)
    else:
        t["rustV1Row"] = RUST_V1_ROW
    return t


def hello_payload(shape, token=True):
    if shape == "ts":
        return {"hostBuildId": HOST_BUILD_ID, "expectedProviderDescriptorSha256": W.descriptor_digest(TS_PROVIDER_DESCRIPTOR),
                "expectedRuntimeDescriptorSha256": W.descriptor_digest(TS_RUNTIME_DESCRIPTOR), "limits": dict(W.TS_LIMITS),
                "expectedCapabilities": caps(shape, token), "identityVersions": dict(P.IDENTITY_VERSIONS)}
    return {"protocolMajor": 3, "hostBuildId": HOST_BUILD_ID, "expectedProtocolContractSha256": W.CONTRACT_SHA256,
            "expectedIdentity": dict({"protocolMajor": 3}, **RUST_V1_ROW), "expectedCapabilities": caps(shape, token),
            "identityVersions": dict(P.IDENTITY_VERSIONS), "limits": dict(W.LIMITS_V3)}


def ack_payload(shape, token=True):
    if shape == "ts":
        pd, rd = TS_PROVIDER_DESCRIPTOR, TS_RUNTIME_DESCRIPTOR
        return {"protocolMajor": 2, "providerBuildId": pd["providerBuildId"], "providerDescriptorSha256": W.descriptor_digest(pd),
                "runtimeDescriptorSha256": W.descriptor_digest(rd), "nodeVersion": rd["nodeVersion"], "v8Version": rd["v8Version"],
                "modulesAbi": rd["modulesAbi"], "typescriptVersion": pd["typescriptVersion"], "typescriptCompilerSha256": pd["typescriptCompilerSha256"],
                "typescriptStdlibMerkleRoot": pd["typescriptStdlibMerkleRoot"], "defaultWorkBudgetProfileId": pd["defaultWorkBudgetProfileId"],
                "defaultWorkBudgetProfileSha256": pd["defaultWorkBudgetProfileSha256"], "platformId": rd["platformId"],
                "capabilities": caps(shape, token), "identityVersions": dict(P.IDENTITY_VERSIONS)}
    return dict({"protocolMajor": 3}, **RUST_V1_ROW, capabilities=caps(shape, token), identityVersions=dict(P.IDENTITY_VERSIONS))


def hello(shape, token=True, payload=None):
    return {"frame": "Hello", "payload": payload if payload is not None else hello_payload(shape, token)}


def ack(shape, token=True, payload=None):
    return {"frame": "HelloAck", "payload": payload if payload is not None else ack_payload(shape, token)}


# ------------------------------------------------------------------------------------------------ startup payloads
EXECUTION_ID = {"ts": "exec-cb24-source44-typescript", "rust": "exec-cb24-source44-rust"}
PLAN_INTENT = {"ts": "sha256:" + h("plan-intent:typescript"), "rust": "sha256:" + h("plan-intent:rust")}
PREPARED_OUTPUT_SET_ID = "sha256:" + h("prepared-output-set:cb24-source44")


def _prepared_context():
    ctx = copy.deepcopy(RET["rust"]["context"])
    ctx["preparedOutputSetId"] = PREPARED_OUTPUT_SET_ID
    return ctx


PREPARED_CONTEXT_ID = "sha256:" + K.H(RET["rust"]["contextDomain"], _prepared_context())


def resolved_inputs(shape, prepared=False):
    ri = copy.deepcopy(RET[shape]["universe"])
    if prepared:
        assert shape == "rust"
        ri.update(preparedOutputSetId=PREPARED_OUTPUT_SET_ID, preparedResolution="imported-inert", executionCapableResolution=True,
                  nativeContextId=PREPARED_CONTEXT_ID)
    return ri


def ts_universe():
    pd, rd = TS_PROVIDER_DESCRIPTOR, TS_RUNTIME_DESCRIPTOR
    return {"schemaVersion": 1, "manifestId": h("ts:manifest"), "capabilityManifestId": h("ts:capability-manifest"),
            "runtimeArtifactId": "typescript-runtime", "runtimeArtifactSha256": h("ts:runtime-artifact"), "providerArtifactId": "typescript-provider",
            "providerArtifactSha256": h("ts:provider-artifact"), "runtimeDescriptorSha256": W.descriptor_digest(rd),
            "providerDescriptorSha256": W.descriptor_digest(pd), "protocolMajor": 2, "providerBuildId": pd["providerBuildId"],
            "nodeVersion": rd["nodeVersion"], "v8Version": rd["v8Version"], "modulesAbi": rd["modulesAbi"], "typescriptVersion": pd["typescriptVersion"],
            "typescriptCompilerSha256": pd["typescriptCompilerSha256"], "typescriptStdlibMerkleRoot": pd["typescriptStdlibMerkleRoot"],
            "platformId": rd["platformId"], "resolvedInputs": resolved_inputs("ts")}


def rust_universe(prepared=False):
    return dict({"schemaVersion": 1, "manifestId": h("rust:manifest"), "capabilityManifestId": h("rust:capability-manifest"),
                 "providerArtifactId": "rust-provider", "providerArtifactSha256": h("rust:provider-artifact"), "toolchainArtifactId": "rust-toolchain-bundle",
                 "toolchainArtifactSha256": h("rust:toolchain-artifact"), "protocolMajor": 3},
                **RUST_V1_ROW, rustcVersion="1.79.0", cargoVersion="1.79.0", rustcDevLlvmDigest=h("rust:rustc-dev-llvm"),
                standardLibraryComponentDigests={"core": h("rust:core"), "std": h("rust:std")}, providerBinarySha256=h("rust:provider-binary"),
                licenseNoticeBundleSha256=h("rust:license-notices"), platformId="darwin-arm64", resolvedInputs=resolved_inputs("rust", prepared))


def open_universe_payload(shape, prepared=False):
    base = {"executionId": EXECUTION_ID[shape], "snapshotId": RET[shape]["plan"]["snapshotId"], "planId": PLAN_ID, "planIntentCommitment": PLAN_INTENT[shape]}
    if shape == "ts":
        u = ts_universe()
        return dict(base, providerId="typescript-semantic", universe=u, universeKey=W.universe_identity("ts", u["resolvedInputs"]))
    u = rust_universe(prepared)
    ri = u["resolvedInputs"]
    return dict(base, providerId="rust-semantic", universe=u,
                repositoryResolution={"authorizationId": None, "dependencySourceSetId": ri["dependencySourceSetId"], "effects": None,
                                      "preparedOutputSetId": ri["preparedOutputSetId"], "workerExecutesRepositoryCode": False})


def universe_accepted_payload(shape, ou):
    if shape == "ts":
        return {k: copy.deepcopy(ou[k]) for k in ("executionId", "snapshotId", "planId", "universeKey")}
    return {k: copy.deepcopy(ou[k]) for k in ("executionId", "snapshotId", "planId", "providerId", "universe", "repositoryResolution")}


def ncv_payload(ou):
    cid = ou["universe"]["resolvedInputs"]["nativeContextId"]
    return {"nativeContextId": cid, "recomputedNativeContextId": cid, "equal": True}


def pre_unavailable_payload(shape, ou):
    return {"executionId": ou["executionId"], "snapshotId": ou["snapshotId"], "planId": ou["planId"], "reason": "native-context-mismatch",
            "nativeContextId": ou["universe"]["resolvedInputs"]["nativeContextId"], "recomputedNativeContextId": "sha256:" + h("worker-recomputed-context")}


def exchange_ctx(shape, token=True, prepared=False):
    plan = {"planId": PLAN_ID, "snapshotId": RET[shape]["plan"]["snapshotId"],
            "nativeContextDigests": [PREPARED_CONTEXT_ID[7:]] if prepared else list(RET[shape]["plan"]["nativeContextDigests"])}
    preparation = {"kind": "imported-descriptor", "authorizationId": None, "effects": None} if prepared else None
    return {"trusted": trusted(shape, token), "retained": RETAINED, "host": HOST[shape],
            "startup": {"executionId": EXECUTION_ID[shape], "planIntentCommitment": PLAN_INTENT[shape], "plan": plan, "preparation": preparation}}


def startup_events(shape, prepared=False):
    ou = open_universe_payload(shape, prepared)
    return ou, {"OpenUniverse": {"frame": "OpenUniverse", "payload": ou},
                "UniverseAccepted": {"frame": "UniverseAccepted", "payload": universe_accepted_payload(shape, ou)},
                "NativeContextVerified": {"frame": "NativeContextVerified", "payload": ncv_payload(ou)},
                "PreAnalyzeUnavailable": {"frame": "Unavailable", "payload": pre_unavailable_payload(shape, ou)}}


# ------------------------------------------------------------------------------------------------ Analyze, host domains, coverage
def analyze(shape, analysis_ordinal=0):
    if shape == "ts":
        return {"analysisOrdinal": analysis_ordinal, "stageRequests": [{"stageId": "ts-imports", "stageOrdinal": 0, "relations": ["imports"]},
                                                                       {"stageId": "ts-calls", "stageOrdinal": 1, "relations": ["calls"]}]}
    return {"analysisOrdinal": analysis_ordinal, "stages": [{"stageOrdinal": 0, "planStage": {"kind": "fact-derivation", "stageId": "rust-calls", "relations": ["calls"]}}]}


def host_domain(shape, relation):
    ret = RET[shape]["coverage"][relation]
    key, entry = ret["payload"]["key"], ret["payload"]["entry"]
    keys = [{"relation": relation, "resolution": rung, "sourceUniverseId": "sha256:" + key["sourceUniverse"], "targetUniverseId": "sha256:" + key["targetUniverse"],
             "subjectScopeCommitment": key["subjectScopeCommitment"], "producer": HOST[shape]["providerId"], "producerVersion": HOST[shape]["providerVersion"],
             "schemaVersion": FB.REG["schemas"][relation]["schemaVersion"]} for rung in NF.RELS[relation]["ladder"]]
    return {"relation": relation, "keys": keys, "subjectCounts": [entry["examinedUniverse"]["subjectCount"]] * len(keys),
            "scopeId": ret["descriptor"]["scopeId"], "retainedRung": entry["resolution"], "retainedCoverageId": ret["coverageId"]}


def stage_relations(shape, a):
    return [s["relations"][0] for s in a["stageRequests"]] if shape == "ts" else [s["planStage"]["relations"][0] for s in a["stages"]]


def analyze_event(shape, analysis_ordinal=0):
    a = analyze(shape, analysis_ordinal)
    rels = stage_relations(shape, a)
    return {"frame": "Analyze", "stageCount": len(rels), "analyze": a, "hostDomains": [host_domain(shape, r) for r in rels]}


def wire_key(k):
    return {"relation": k["relation"], "resolution": k["resolution"], "sourceUniverse": k["sourceUniverseId"][7:],
            "subjectScopeCommitment": k["subjectScopeCommitment"], "targetUniverse": k["targetUniverseId"][7:]}


def worker_entry(shape, k):
    ret = RET[shape]["coverage"][k["relation"]]["payload"]
    if k["resolution"] == ret["entry"]["resolution"]:
        return copy.deepcopy(ret)
    resolved = k["resolution"] in NF.RESOLVED
    rc = {"state": "complete" if resolved else "not-applicable", "attempted": resolved, "examinedExhaustive": True, "stageTerminal": "complete",
          "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
    return {"schemaVersion": 3, "key": wire_key(k), "entry": dict(copy.deepcopy(ret["entry"]), resolution=k["resolution"], resolutionCompleteness=rc)}


WORKER_TERMINAL_CLOSED_WORLD = {"deadCodeRepairEligible": False, "dynamicDispatch": "not-applicable", "entryPointsRecognized": "none", "exportsClosed": "unknown",
                                "externalConsumers": "unknown", "nonliteralLoading": "none", "reasons": []}


def terminal_entry(k, count, deficiency, stage_terminal):
    resolved = k["resolution"] in NF.RESOLVED
    rc = {"state": "not-attempted" if resolved else "not-applicable", "attempted": False, "examinedExhaustive": False, "stageTerminal": stage_terminal,
          "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
    return {"schemaVersion": 3, "key": wire_key(k),
            "entry": {"relation": k["relation"], "resolution": k["resolution"], "coverage": "unknown",
                      "examinedUniverse": {"subjectScopeCommitment": k["subjectScopeCommitment"], "subjectCount": count}, "resolutionCompleteness": rc,
                      "closedWorld": copy.deepcopy(WORKER_TERMINAL_CLOSED_WORLD), "derivationKinds": [], "confidenceMillionths": 0, "deficiency": deficiency,
                      "nativeCause": None}}


def coverage_payload(shape, stage_index, analysis_ordinal=0):
    ev = analyze_event(shape, analysis_ordinal)
    dom = ev["hostDomains"][stage_index]
    stage_id = FB.stage_request(ev["analyze"], shape, stage_index)["stageId"]
    return {"analysisOrdinal": analysis_ordinal, "stageId": stage_id, "entries": [worker_entry(shape, k) for k in dom["keys"]],
            "coverageCommitment": "sha256:" + h("placeholder-coverage-commitment:" + stage_id)}


def coverage(shape, stage_index, payload=None):
    return {"frame": "Coverage" if shape == "ts" else "CoverageV3", "payload": payload if payload is not None else coverage_payload(shape, stage_index)}


def terminal_coverage(shape, deficiency, stage_terminal):
    ev = analyze_event(shape)
    return [terminal_entry(k, n, deficiency, stage_terminal) for d in ev["hostDomains"] for k, n in zip(d["keys"], d["subjectCounts"])]


def post_unavailable(shape, reason="capability-missing"):
    ev = analyze_event(shape)
    return {"frame": "Unavailable", "payload": {"analysisOrdinal": 0, "affectedStageIds": [FB.stage_request(ev["analyze"], shape, i)["stageId"] for i in range(ev["stageCount"])],
                                                "reason": reason, "coverage": terminal_coverage(shape, "provider-unavailable", "unavailable"),
                                                "coverageCommitment": "sha256:" + h("placeholder-unavailable-commitment")}}


def budget_exhausted(shape, trigger_stage):
    base = {"analysisOrdinal": 0, "triggerStageId": trigger_stage, "limit": 10, "observed": 11,
            "coverage": terminal_coverage(shape, "budget-exhausted", "budget-exhausted"), "coverageCommitment": "sha256:" + h("placeholder-budget-commitment")}
    base.update({"dimension": "factsEmitted"} if shape == "ts" else {"unit": "items"})
    return {"frame": "BudgetExhausted", "payload": base}


def cancel(shape, analysis_ordinal=0):
    return {"frame": "Cancel", "payload": {"executionId": EXECUTION_ID[shape], "analysisOrdinal": analysis_ordinal, "reason": "user-interrupt"}}


def cancelled(shape, observed_phase, analysis_ordinal=0):
    return {"frame": "Cancelled", "payload": {"executionId": EXECUTION_ID[shape], "analysisOrdinal": analysis_ordinal, "observedPhase": observed_phase}}


# ------------------------------------------------------------------------------------------------ FactBatch candidates (source42.v3, universes rebound in source44)
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
    """rust-semantic historical FactBatchV2 JSON vector (provider-handshake.schemas.v1.json#/$defs/RustFactBatchV2Vector)."""
    return {k: copy.deepcopy(batch[k]) for k in ("analysisOrdinal", "stageId", "batchIndex", "candidates")}


def v1_ts(batch, commitment=None):
    """typescript-semantic historical delivery.v2 FactBatchV1 JSON vector (#/$defs/TypeScriptFactBatchV1Vector); batchCommitment recomputed over the wire facts."""
    arr = batch["candidates"] if "candidates" in batch else batch["facts"]
    facts = copy.deepcopy(arr)
    return {"analysisOrdinal": batch["analysisOrdinal"], "stageId": batch["stageId"], "batchIndex": batch["batchIndex"], "facts": facts,
            "batchCommitment": commitment if commitment is not None else FB.ts_batch_commitment(facts)}


def historical(shape, batch):
    return v1_ts(batch) if shape == "ts" else v2(batch)


def renumber(batch, start):
    """Renumber candidates (and companions by the same offset) to begin at `start`."""
    b = copy.deepcopy(batch)
    arr = b["candidates"] if "candidates" in b else b["facts"]
    off = start - arr[0]["candidateOrdinal"]
    for c in arr:
        c["candidateOrdinal"] += off
    for c in b.get("occupancyCompanions", []):
        c["candidateOrdinal"] += off
    return b


def fb(payload):
    return {"frame": "FactBatch", "payload": payload}
