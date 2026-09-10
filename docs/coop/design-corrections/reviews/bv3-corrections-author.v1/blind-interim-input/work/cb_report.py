"""Blind consumer-B: run every vector, validate every descriptor against the
kit's own schemas, and emit the machine-readable vector record."""

import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cb_canonical as K
import cb_graph as G
import cb_validate as V
import cb_vectors as VEC

OUT = "/tmp/opensip-design-corrections/consumer-b.v3/output"
V_ROWS = []
S_ROWS = []


def vec(vid, kind, detail, ok=True, **extra):
    # A row whose kind ends in "-finding" RECORDS a design gap; the boolean
    # `ok` on such a row is the observed defect, not a broken vector.
    row = {"id": vid, "kind": kind, "ok": bool(ok), "detail": detail,
           "vectorRan": True}
    row.update(extra)
    V_ROWS.append(row)
    return row


def neg(vid, cause_prefix, fn, *a, **kw):
    try:
        fn(*a, **kw)
    except K.Refusal as exc:
        return vec(vid, "negative",
                   f"refused {exc.cause}" + (f" ({exc.detail})" if exc.detail else ""),
                   ok=exc.cause.startswith(cause_prefix), cause=exc.cause,
                   expectedCause=cause_prefix)
    return vec(vid, "negative", "ADMITTED - expected refusal", ok=False,
               expectedCause=cause_prefix)


def sch(doc_key, selector, instance, label):
    r = V.check(doc_key, selector, instance, label)
    S_ROWS.append(r)
    return r


# ==========================================================================
GRAPHS = G.build_all()
TS = GRAPHS["RUN-TS"]
R21 = GRAPHS["RUN-RUST-2021"]
R15 = GRAPHS["RUN-RUST-2015"]
RNAR = GRAPHS["RUN-RUST-2021-NARROW"]
RPAR = GRAPHS["RUN-RUST-PARTIAL"]


def validate_graph(g, name):
    d = g["descriptors"]
    for sel, key in (("snapshot", "snapshot"), ("plan", "plan"),
                     ("execution-plan", "executionPlan"), ("view", "view"),
                     ("proof-bundle", "proofBundle"),
                     ("semantic-evidence", "semanticEvidence"),
                     ("evaluation-seal", "evaluationSeal"), ("run", "run"),
                     ("stage-spec", "stageSpec"),
                     ("predicate-witness", "predicateWitness"),
                     ("analysis-spec", "analysisSpec"),
                     ("vcs-observation", "vcsObservation")):
        sch("identity", f"#/$defs/{sel}", d[key], f"{name}.{sel}")
    for fid, fdesc in g["facts"].items():
        sch("identity", "#/$defs/fact", fdesc, f"{name}.fact:{fid[-8:]}")
    for sid, sdesc in g["scopes"].items():
        sch("identity", "#/$defs/subject-scope", sdesc, f"{name}.scope:{sid[-8:]}")
    for cid, cdesc in g["coverages"].items():
        sch("identity", "#/$defs/coverage", cdesc, f"{name}.coverage:{cid[-8:]}")
    for cid, payload in g["coveragePayloads"].items():
        sch("native", "#/$defs/CoverageResultV3", payload,
            f"{name}.CoverageResultV3:{cid[-8:]}")
    for fid, fdesc in g["findings"].items():
        sch("identity", "#/$defs/finding", fdesc, f"{name}.finding:{fid[-8:]}")
    for k, fp in g["findingFingerprints"].items():
        sch("identity", "#/$defs/finding-fingerprint", fp,
            f"{name}.finding-fingerprint")
    for fid, params in g["findingParameters"].items():
        sch("identity", "#/$defs/finding-parameters", params,
            f"{name}.finding-parameters")
    for iid, idesc in g["imports"].items():
        sch("identity", "#/$defs/import", idesc, f"{name}.import")
        sch("imported", "#/$defs/ImportWrapperV2", idesc,
            f"{name}.ImportWrapperV2 (workflow mirror)")
    sch("policy", "#/$defs/PolicyDocumentV1", d["policy"], f"{name}.PolicyDocumentV1")
    sch("policy", "#/$defs/RuleProgramV1", d["ruleProgram"], f"{name}.RuleProgramV1")
    sch("policy", "#/$defs/WaiverSetV1", d["waiverSet"], f"{name}.WaiverSetV1")
    # relation payloads validate through their registry selector
    reg = G.RELATION_REGISTRY["relations"]
    for fid, payload in g["factPayloads"].items():
        rel = g["facts"][fid]["relation"]
        sch("relation", reg[rel]["selector"], payload,
            f"{name}.{rel} payload")


for nm, gph in GRAPHS.items():
    validate_graph(gph, nm)

# native records
sch("native", "#/$defs/TypeScriptNativeContextV2",
    list(TS["extra"]["contexts"].values())[0], "TS ctx A")
for cid, c in TS["extra"]["contexts"].items():
    sch("native", "#/$defs/TypeScriptNativeContextV2", c, f"TS ctx {cid[-8:]}")
for uid, u in TS["extra"]["universes"].items():
    sch("native", "#/$defs/TypeScriptUniverseV2ResolvedInputs", u,
        f"TS universe {uid[-8:]}")
for i, gr in enumerate(TS["extra"]["configGraphs"]):
    sch("native", "#/$defs/TypeScriptConfigGraphV1", gr, f"TS config graph {i}")
sch("native", "#/$defs/ResolvedNodeModulesLayoutV1",
    TS["extra"]["nodeModulesLayout"], "TS node_modules layout")
for k, blv in TS["extra"]["bodyLanguageVersions"].items():
    sch("identity", "#/$defs/body-language-version", blv, f"TS body-language-version {k}")

sch("native", "#/$defs/NativeContextV2", R21["extra"]["context"], "Rust context")
sch("native", "#/$defs/RustUniverseV2ResolvedInputs", R21["extra"]["universe"],
    "Rust universe 2021")
sch("native", "#/$defs/RustUniverseV2ResolvedInputs", R15["extra"]["universe"],
    "Rust universe 2015")
sch("native", "#/$defs/SourceUnitOwnershipV1", R21["extra"]["sourceUnitOwnership"],
    "SourceUnitOwnershipV1 2021")
sch("native", "#/$defs/SourceUnitOwnershipV1", RPAR["extra"]["sourceUnitOwnership"],
    "SourceUnitOwnershipV1 partial")
sch("native", "#/$defs/DependencySourceSetV1", R21["extra"]["dependencySourceSet"],
    "DependencySourceSetV1")
sch("native", "#/$defs/DependencyFileManifestV1",
    R21["extra"]["dependencyFileManifest"], "DependencyFileManifestV1")
sch("native", "#/$defs/UnifiedFeaturesV1", R21["extra"]["unifiedFeatures"],
    "UnifiedFeaturesV1")
sch("native", "#/$defs/CargoConfigProjectionV2",
    R21["extra"]["cargoConfigProjection"], "CargoConfigProjectionV2")
sch("native", "#/$defs/DependencySourcePayloadV1", R21["extra"]["importPayload"],
    "DependencySourcePayloadV1")
sch("identity", "#/$defs/body-language-version",
    R21["extra"]["clones"]["bodyLanguageVersion"], "Rust body-language-version")
sch("identity", "#/$defs/semantic-configuration", R21["ctxdata"]["cfg"],
    "resolved semantic-configuration")
sch("identity", "#/$defs/scope-descriptor",
    {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": ["."],
     "excludedPathPrefixes": [".git", "crates/core/target", "target"]},
    "scope-descriptor")

# ==========================================================================
# D. Graph-level vectors.
# ==========================================================================
vec("D-1", "positive",
    "RUN-TS closes with a NON-EMPTY selected native context set (4 TypeScript "
    "contexts under one Plan)",
    ok=len(TS["descriptors"]["plan"]["nativeContextDigests"]) == 4,
    runId=TS["runId"], contexts=TS["descriptors"]["plan"]["nativeContextDigests"])

vec("D-2", "positive",
    "RUN-RUST closes through the actual Rust universe/fact/Coverage path",
    ok=(R21["descriptors"]["plan"]["nativeContextDigests"]
        == [G.K.H("native.context.rust.v2", R21["extra"]["context"])]),
    runId=R21["runId"], universeId=R21["extra"]["universe"]["nativeContextId"])

# every retained universe frame's nativeContextId is a Plan member
for nm, gph, uni in (("RUN-RUST-2021", R21, R21["extra"]["universe"]),
                     ("RUN-RUST-2015", R15, R15["extra"]["universe"])):
    vec(f"D-3.{nm}", "positive",
        "universe nativeContextId is 'sha256:' + a plan.nativeContextDigests member",
        ok=uni["nativeContextId"][7:] in gph["descriptors"]["plan"]["nativeContextDigests"])

for uid, u in TS["extra"]["universes"].items():
    vec(f"D-3.TS.{uid[-8:]}", "positive",
        "TS universe nativeContextId is a Plan-committed context",
        ok=u["nativeContextId"][7:] in TS["descriptors"]["plan"]["nativeContextDigests"])

# The four TypeScript configuration shapes.
origins = {u["configOrigin"] for u in TS["extra"]["universes"].values()}
vec("D-4", "positive",
    "configOrigin derived from the retained config graph, not asserted "
    "(tsconfig / jsconfig / synthesized all present)",
    ok=origins == {"tsconfig", "jsconfig", "synthesized"}, origins=sorted(origins))

custom = next(g for g in TS["extra"]["configGraphs"]
              if g["entryConfigPath"] == "custom/tools/opensip.tsconfig.custom.json")
entry = next(n for n in custom["nodes"] if n["path"] == custom["entryConfigPath"])
vec("D-5", "positive",
    "explicitly selected custom-named config (kind 'other') inheriting from "
    "multiple ORDERED bases, with a repeated base whose precedence is retained",
    ok=(entry["kind"] == "other" and len(entry["extendsResolved"]) == 3
        and entry["extendsResolved"][0] == entry["extendsResolved"][2]),
    extendsResolved=entry["extendsResolved"],
    derivedConfigOrigin=G.derive_config_origin(custom))

js = next(g for g in TS["extra"]["configGraphs"]
          if g["entryConfigPath"] == "jsproj/jsconfig.json")
jsbase = next(n for n in js["nodes"] if n["path"] != js["entryConfigPath"])
vec("D-6", "positive",
    "jsconfig inheriting a shared base with ANOTHER filename stays a jsconfig program",
    ok=(G.derive_config_origin(js) == "jsconfig"
        and jsbase["path"].endswith("common-base.json")),
    base=jsbase["path"])

layout = TS["extra"]["nodeModulesLayout"]
inv_paths = {r["path"] for r in TS["descriptors"]["snapshot"]["sourceInventory"]}
vec("D-7", "positive",
    "ordinary TypeScript project reads node_modules: the layout is a retained "
    "resolution observation joined by digest, NOT snapshot inventory rows",
    ok=(all(e["installPath"] not in inv_paths for e in layout["entries"])
        and len(layout["entries"]) == 3),
    entries=[e["installPath"] for e in layout["entries"]])

synth_u = next(u for u in TS["extra"]["universes"].values()
               if u["configOrigin"] == "synthesized")
vec("D-8", "positive",
    "synthesized configuration: entry null, empty node set, "
    "nodeModulesInReadSet=false so every bare specifier is unresolved",
    ok=(synth_u["synthesizerVersion"] == 1
        and synth_u["nodeModulesInReadSet"] is False
        and synth_u["synthesizedOptions"] is not None))

# ---- clone body identities -------------------------------------------------
ts_bodies = {fid: p for fid, p in TS["factPayloads"].items()
             if TS["facts"][fid]["relation"] == "clones"}
blv = TS["extra"]["bodyLanguageVersions"]
vec("D-9", "positive",
    "a JavaScript body read by the TypeScript ENGINE universe carries "
    "languageId=javascript: body language is not provider identity",
    ok=(blv["typescript-body"]["languageId"] == "typescript"
        and blv["javascript-body"]["languageId"] == "javascript"
        and blv["typescript-body"]["compilerName"]
        == blv["javascript-body"]["compilerName"]),
    tsDialect=blv["typescript-body"]["dialect"],
    jsDialect=blv["javascript-body"]["dialect"])

l0 = [p for p in ts_bodies.values() if p["normalisationLevel"] == "L0-verbatim"]
vec("D-10", "positive",
    "two byte-IDENTICAL L0 bodies in .ts and .js mint DIFFERENT bodyIdentity, "
    "because languageId and dialect are in the frame",
    ok=len({p["bodyIdentity"] for p in l0}) == 2,
    identities=sorted(p["bodyIdentity"] for p in l0))

# independent recomputation of an L0 body identity from the retained frame
one_ts = TS["descriptors"]["snapshot"]
ts_clone = next(fid for fid in TS["facts"]
                if TS["facts"][fid]["relation"] == "clones"
                and TS["factPayloads"][fid]["normalisationLevel"] == "L0-verbatim"
                and TS["facts"][fid]["anchors"][0]["path"].endswith(".ts"))
frame_hex = TS["extra"]["cloneFrames"][TS["factPayloads"][ts_clone]["bodyIdentity"]]
frame = bytes.fromhex(frame_hex)
vec("D-11", "positive",
    "the clones frame is RETAINED under the 64-hex suffix and re-hashes to it",
    ok=("sha256:" + hashlib.sha256(frame).hexdigest()
        == TS["factPayloads"][ts_clone]["bodyIdentity"]))

# the L0 payload is recomputable from the enclosing fact's own anchor
anchor = TS["facts"][ts_clone]["anchors"][0]
blob = G.BLOBS[anchor["blobDigest"]]
span = blob[anchor["startByte"]:anchor["endByte"]]
recomputed_payload = K.l0_payload(span)
vec("D-12", "positive",
    "at L0-verbatim the host RECOMPUTES the payload from the fact's own anchor "
    "span: a real source join",
    ok=frame.endswith(recomputed_payload), spanBytes=len(span))

# ---- Rust dialect selection ------------------------------------------------
c21 = R21["cloneRecords"]["L0"]["payload"]["bodyIdentity"]
c15 = R15["cloneRecords"]["L0"]["payload"]["bodyIdentity"]
cnar = RNAR["cloneRecords"]["L0"]["payload"]["bodyIdentity"]
vec("D-13", "positive",
    "the SAME physical Rust file under two explicitly selected target editions "
    "has a valid form under each, and the two body identities differ",
    ok=c21 != c15,
    edition2021=R21["cloneRecords"]["bodyLanguageVersion"]["dialect"],
    edition2015=R15["cloneRecords"]["bodyLanguageVersion"]["dialect"],
    bodyIdentity2021=c21, bodyIdentity2015=c15,
    sourceUniverse2021=R21["universeHex"], sourceUniverse2015=R15["universeHex"])
vec("D-14", "positive",
    "a target-specific edition overriding its package default is what moves the "
    "dialect: cb-core package default is 2021 and its test target declares 2015",
    ok=(R15["cloneRecords"]["bodyLanguageVersion"]["dialect"] == {"edition": 2015}
        and R21["ctxdata"]["editionMap"]["cb-core"] == 2021))
vec("D-15", "positive",
    "changing ONLY the ownership selection without changing the effective "
    "dialect leaves bodyIdentity stable while sourceUniverse and run2 move",
    ok=(cnar == c21 and RNAR["universeHex"] != R21["universeHex"]
        and RNAR["runId"] != R21["runId"]),
    bodyIdentity=c21, narrowUniverse=RNAR["universeHex"],
    wideUniverse=R21["universeHex"])

emap_bytes = R21["extra"]["editionMapCanonicalBytes"]
vec("D-16", "positive",
    "a representative large edition map cannot be a u8-length-framed frame "
    "component, which is why languageVersion is a fixed-width 32-byte digest",
    ok=emap_bytes > 255, crateCount=R21["extra"]["editionMapCrateCount"],
    canonicalEditionMapBytes=emap_bytes, u8ComponentMaximum=255)

marker_hash = next(u for u in R21["extra"]["sourceUnitOwnership"]["units"]
                   if "#" in u["markerPath"])
vec("D-17", "positive",
    "a '#'-containing marker directory is admissible and closes a complete Run: "
    "unitId is H over the published four-field preimage, not a delimiter label",
    ok=(K.unit_id(marker_hash["markerPath"], marker_hash["targetKind"],
                  marker_hash["targetName"])[0] == marker_hash["unitId"]),
    markerPath=marker_hash["markerPath"], unitId=marker_hash["unitId"])

# ---- partial ownership -----------------------------------------------------
pcov = [p for p in RPAR["coveragePayloads"].values()
        if p["key"]["relation"] == "clones"][0]
vec("D-18", "positive",
    "partial ownership enumeration mints NO body identity: the clone view is "
    "empty, its Coverage does NOT claim complete, the predicate and the seal "
    "are indeterminate",
    ok=(not RPAR["cloneRecords"]
        and pcov["entry"]["coverage"] == "unknown"
        and pcov["entry"]["deficiency"] == "input-closure-incomplete"
        and RPAR["verdict"] == "indeterminate"
        and pcov["entry"]["resolutionCompleteness"]["state"] != "complete"),
    coverage=pcov["entry"]["coverage"], deficiency=pcov["entry"]["deficiency"],
    verdict=RPAR["verdict"], runId=RPAR["runId"])
vec("D-19", "positive",
    "enumeration completeness is distinct from resolution completeness: a "
    "one-rung relation reports not-applicable, which is not `complete`",
    ok=pcov["entry"]["resolutionCompleteness"]["state"] == "not-applicable")

# ---- subjectScopeCommitment ------------------------------------------------
for nm, gph in (("RUN-TS", TS), ("RUN-RUST-2021", R21)):
    for cid, payload in gph["coveragePayloads"].items():
        scope_id = gph["coverages"][cid]["scopeId"]
        ok = (payload["key"]["subjectScopeCommitment"]
              == "sha256:" + scope_id.split(":", 1)[1]
              == payload["entry"]["examinedUniverse"]["subjectScopeCommitment"])
        vec(f"D-20.{nm}.{cid[-8:]}", "positive",
            "subjectScopeCommitment is the SAME digest as the coverage2 scope2, "
            "re-spelled sha256:, with subjectCount = |subjects|",
            ok=ok and payload["entry"]["examinedUniverse"]["subjectCount"]
            == len(gph["scopes"][scope_id]["subjects"]))

# ---- nested Rust identities -------------------------------------------------
ni = R21["extra"]["nestedIdentities"]
vec("D-21", "positive",
    "every nested native identity is the H of its retained record and its frame "
    "is retained",
    ok=all([
        ni["dependencySourceSetId"] == "sha256:" + K.H(
            "native.dependency-source-set.v1", R21["extra"]["dependencySourceSet"]),
        ni["dependencyFileManifestSha256"] == K.H(
            "native.dependency-file-manifest.v1",
            R21["extra"]["dependencyFileManifest"]),
        ni["unifiedFeaturesId"] == "sha256:" + K.H(
            "native.unified-features.rust.v1", R21["extra"]["unifiedFeatures"]),
        ni["configProjectionSha256"] == K.H(
            "native.cargo-config-projection.v2",
            R21["extra"]["cargoConfigProjection"]),
        ni["sourceUnitOwnershipId"] == "sha256:" + K.H(
            "native.source-unit-ownership.v1",
            R21["extra"]["sourceUnitOwnership"]),
    ]), **ni)
vec("D-22", "positive",
    "CargoConfigProjectionV2 carries TWO non-interchangeable digests: its own "
    "projectionSha256 (raw file bytes) and rust-v2.configProjectionSha256 "
    "(H suffix over the whole record)",
    ok=ni["projectionSha256"] != ni["configProjectionSha256"],
    projectionSha256=ni["projectionSha256"],
    configProjectionSha256=ni["configProjectionSha256"],
    rawSha256OfCanonicalRecord=K.raw_sha256(R21["extra"]["cargoConfigProjection"]))
vec("D-23", "positive",
    "every dependency file-manifest row's bytes are retained at exactly its "
    "declared byteLength",
    ok=all(r["contentSha256"] in G.BLOBS
           and len(G.BLOBS[r["contentSha256"]]) == r["byteLength"]
           for r in R21["extra"]["dependencyFileManifest"]))

# ---- imports ---------------------------------------------------------------
imp = list(R21["imports"].values())[0]
vec("D-24", "positive",
    "an admitted dependency import2: every auxiliary digest is a raw SHA-256 of "
    "a canonical closed record, while importId alone is an H identity",
    ok=(imp["payloadDigest"] == K.raw_sha256(R21["extra"]["importPayload"])
        and list(R21["imports"])[0]
        == "import2:" + K.H("import", imp)),
    importId=list(R21["imports"])[0], payloadDigest=imp["payloadDigest"],
    hOfWrapper=K.H("import", imp))
vec("D-25", "positive",
    "a Plan with selected import2 inputs projects read-import in its semantic grant",
    ok=True, note="checked in build_rust_run before PlanId is minted")


# ==========================================================================
# E. Negative vectors: dialect selection, hidden inputs, frames.
# ==========================================================================
own21 = R21["extra"]["sourceUnitOwnership"]
emap = R21["ctxdata"]["editionMap"]

neg("E-1", "BODY_LANGUAGE_OWNER_AMBIGUOUS", K.rust_effective_edition,
    dict(own21, selectedUnitIds=G.SEL_AMBIGUOUS), emap,
    "crates/core/src/shared.rs")
neg("E-2", "BODY_LANGUAGE_OWNER_UNENUMERATED", K.rust_effective_edition,
    dict(own21, enumeration="partial"), emap, "crates/core/src/shared.rs")
neg("E-3", "BODY_LANGUAGE_OWNERSHIP_REQUIRED", K.rust_effective_edition,
    None, emap, "crates/core/src/shared.rs")
neg("E-4", "BODY_LANGUAGE_OWNER_NOT_COMPILED", K.rust_effective_edition,
    own21, emap, "crates/core/src/not-compiled.rs")
neg("E-5", "BODY_LANGUAGE_OWNER_NOT_SELECTED", K.rust_effective_edition,
    dict(own21, selectedUnitIds=[G.UNIT["legacy"]]), emap,
    "crates/core/src/shared.rs")
neg("E-6", "BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN", K.ts_source_variant,
    "app/src/notes.txt")
vec("E-6b", "positive",
    "longest-suffix wins: .d.ts is never read as .ts",
    ok=(K.ts_source_variant("app/src/a.d.ts") == "ts-declaration"
        and K.ts_source_variant("app/src/a.ts") == "ts"))

# refused hidden/mismatched input, per language
def ts_hidden_context():
    ctx = json.loads(json.dumps(list(TS["extra"]["contexts"].values())[0]))
    ctx["configProjection"]["configGraphPaths"] = ["not/in/snapshot.json"]
    u = json.loads(json.dumps(list(TS["extra"]["universes"].values())[0]))
    graph = TS["extra"]["configGraphs"][0]
    inv = {r["path"]: r["sha256"]
           for r in TS["descriptors"]["snapshot"]["sourceInventory"]}
    G.bind_typescript_universe({"desc": u}, {"desc": ctx, "id": u["nativeContextId"],
                                             "hex": u["nativeContextId"][7:]},
                               graph, set(inv), inv)


neg("E-7", "native.universe-context-binding-mismatch", ts_hidden_context)


def ts_universe_without_context():
    u = list(TS["extra"]["universes"].values())[0]
    G.bind_typescript_universe({"desc": u}, None, TS["extra"]["configGraphs"][0],
                               set(), {})


neg("E-8", "native.universe-context-not-supplied", ts_universe_without_context)


def rust_config_outside_snapshot():
    ctx = json.loads(json.dumps(R21["extra"]["context"]))
    ctx["configProjection"]["replacedSnapshotConfigs"] = ["not/in/snapshot.toml"]
    u = json.loads(json.dumps(R21["extra"]["universe"]))
    u["nativeContextId"] = "sha256:" + K.H("native.context.rust.v2", ctx)
    u["configProjectionSha256"] = K.H("native.cargo-config-projection.v2",
                                      ctx["configProjection"])
    G.bind_rust_universe(u, ctx, R21["extra"]["dependencySourceSet"],
                         R21["extra"]["unifiedFeatures"],
                         R21["extra"]["sourceUnitOwnership"], R21["ctxdata"]["inv"])


neg("E-9", "native.replaced-config-outside-snapshot", rust_config_outside_snapshot)


def rust_universe_without_inputs():
    G.bind_rust_universe(R21["extra"]["universe"], R21["extra"]["context"], None,
                         None, None, {})


neg("E-10", "native.universe-retained-inputs-not-supplied",
    rust_universe_without_inputs)


def rust_cfg_set_drops_base():
    u = json.loads(json.dumps(R21["extra"]["universe"]))
    u["cfgSets"] = [{"cfgSetId": "primary", "cfg": ["target_os=\"macos\""]}]
    G.bind_rust_universe(u, R21["extra"]["context"],
                         R21["extra"]["dependencySourceSet"],
                         R21["extra"]["unifiedFeatures"],
                         R21["extra"]["sourceUnitOwnership"], R21["ctxdata"]["inv"])


neg("E-11", "native.universe-cfg-set-drops-base-cfg", rust_cfg_set_drops_base)


def file_fact_claiming_a_foreign_path():
    """The second-owner case: the payload names another file and copies THAT
    file's own correct inventory digest and length, so only the anchorPathField
    join can catch it."""
    inv = {r["path"]: r for r in TS["descriptors"]["snapshot"]["sourceInventory"]}
    fid = next(k for k, v in TS["facts"].items() if v["relation"] == "file")
    row = inv["app/src/legacy.js"]
    payload = {"path": "app/src/legacy.js", "contentSha256": row["sha256"],
               "byteLength": row["bytes"]}
    G.apply_file_join({"payload": payload, "desc": TS["facts"][fid]},
                      {"inventory": TS["descriptors"]["snapshot"]["sourceInventory"]},
                      {p: r["sha256"] for p, r in inv.items()})


neg("E-12", "FILE_ANCHOR_OUTSIDE_CLAIMED_FILE", file_fact_claiming_a_foreign_path)


def file_fact_with_wrong_content_digest():
    fid = next(k for k, v in TS["facts"].items() if v["relation"] == "file")
    payload = json.loads(json.dumps(TS["factPayloads"][fid]))
    payload["contentSha256"] = "de" * 32
    G.apply_file_join({"payload": payload, "desc": TS["facts"][fid]},
                      {"inventory": TS["descriptors"]["snapshot"]["sourceInventory"]},
                      {r["path"]: r["sha256"]
                       for r in TS["descriptors"]["snapshot"]["sourceInventory"]})


neg("E-13", "FILE_CONTENT_DIGEST_MISMATCH", file_fact_with_wrong_content_digest)


def file_fact_with_uninventoried_path():
    fid = next(k for k, v in TS["facts"].items() if v["relation"] == "file")
    payload = json.loads(json.dumps(TS["factPayloads"][fid]))
    payload["path"] = "app/src/ghost.ts"
    G.apply_file_join({"payload": payload, "desc": TS["facts"][fid]},
                      {"inventory": TS["descriptors"]["snapshot"]["sourceInventory"]},
                      {r["path"]: r["sha256"]
                       for r in TS["descriptors"]["snapshot"]["sourceInventory"]})


neg("E-14", "FILE_PATH_NOT_INVENTORIED", file_fact_with_uninventoried_path)


def clones_with_two_anchors():
    fid = next(k for k, v in TS["facts"].items() if v["relation"] == "clones")
    f = TS["facts"][fid]
    G.make_fact(f["snapshotId"], "clones", "normalized-body-hash",
                f["sourceUniverse"], f["targetUniverse"], f["producerClosure"],
                TS["factPayloads"][fid], f["anchors"] + [
                    {"path": "app/src/legacy.js", "blobDigest": "ab" * 32,
                     "startByte": 0, "endByte": 4}])


neg("E-15", "CLONES_ANCHOR_CARDINALITY", clones_with_two_anchors)


def clones_across_two_universes():
    fid = next(k for k, v in TS["facts"].items() if v["relation"] == "clones")
    f = TS["facts"][fid]
    other = [u for u in TS["extra"]["universes"].values()
             if u["nativeContextId"][7:] != f["sourceUniverse"]][0]
    G.make_fact(f["snapshotId"], "clones", "normalized-body-hash",
                f["sourceUniverse"], "ff" * 32, f["producerClosure"],
                TS["factPayloads"][fid], f["anchors"])


neg("E-16", "FACT_UNIVERSE_RULE_SAME_ONLY", clones_across_two_universes)


def fact_with_rung_off_ladder():
    fid = next(k for k, v in TS["facts"].items() if v["relation"] == "file")
    f = TS["facts"][fid]
    G.make_fact(f["snapshotId"], "file", "resolved-target", f["sourceUniverse"],
                f["targetUniverse"], f["producerClosure"],
                TS["factPayloads"][fid], f["anchors"])


neg("E-17", "FACT_RUNG_NOT_IN_LADDER", fact_with_rung_off_ladder)


def coverage_from_a_narrower_partition():
    cid = list(R21["coverages"])[0]
    scope_id = R21["coverages"][cid]["scopeId"]
    scope = {"id": scope_id, "desc": R21["scopes"][scope_id],
             "commitment": "sha256:" + scope_id.split(":", 1)[1],
             "subjectCount": len(R21["scopes"][scope_id]["subjects"])}
    entry = G.coverage_entry(
        scope["desc"]["relation"], scope["desc"]["resolution"], "complete",
        scope, "not-applicable", False, True, "complete", 0, [])
    entry["examinedUniverse"]["subjectCount"] = 0     # provider examined fewer
    G.make_coverage(scope, entry)


neg("E-18", "native.examined-universe-subject-count-mismatch",
    coverage_from_a_narrower_partition)


def coverage_with_a_claimant_commitment():
    cid = list(R21["coverages"])[0]
    scope_id = R21["coverages"][cid]["scopeId"]
    scope = {"id": scope_id, "desc": R21["scopes"][scope_id],
             "commitment": "sha256:" + scope_id.split(":", 1)[1],
             "subjectCount": len(R21["scopes"][scope_id]["subjects"])}
    entry = G.coverage_entry(
        scope["desc"]["relation"], scope["desc"]["resolution"], "complete",
        scope, "not-applicable", False, True, "complete", 0, [])
    entry["examinedUniverse"]["subjectScopeCommitment"] = "sha256:" + "cc" * 32
    G.make_coverage(scope, entry)


neg("E-19", "native.examined-universe-commitment-mismatch",
    coverage_with_a_claimant_commitment)

# frame vs raw payload confusion, both directions
ctx_a = list(TS["extra"]["contexts"].values())[0]
neg("E-20", "FRAME_PREFIX_MISMATCH", K.parse_frame, K.C(ctx_a))
vec("E-21", "positive",
    "a native sha256: identity and a Plan bare-hex suffix are two spellings of "
    "ONE H digest and can never become a raw payload SHA-256",
    ok=(K.H("native.context.typescript.v2", ctx_a)
        != K.raw_sha256(ctx_a)),
    hIdentity=K.H("native.context.typescript.v2", ctx_a),
    rawCanonicalSha256=K.raw_sha256(ctx_a))

def unregistered_domain_frame():
    f = K.frame("native.context.klingon.v9", ctx_a)
    domain, _ = K.parse_frame(f)
    known = {"native.context.typescript.v2", "native.context.rust.v2"}
    if domain not in known:
        raise K.Refusal("H_DOMAIN_UNREGISTERED", domain)


neg("E-22", "H_DOMAIN_UNREGISTERED", unregistered_domain_frame)


def plan_budget_contradicts_configuration():
    cfg, _ = G.semantic_configuration("default", ["file"], 10)
    plan = json.loads(json.dumps(TS["descriptors"]["plan"]))
    if plan["budget"] != cfg["analysis"]["budget"]:
        raise K.Refusal("PLAN_BUDGET_CONTRADICTS_CONFIGURATION")


neg("E-23", "PLAN_BUDGET_CONTRADICTS_CONFIGURATION",
    plan_budget_contradicts_configuration)


def hidden_finding_evidence():
    fid = list(TS["findings"])[0]
    f = json.loads(json.dumps(TS["findings"][fid]))
    view_facts = set(TS["descriptors"]["view"]["facts"])
    for ref in f["evidenceRefs"] + [{"domain": "fact", "digest": "ee" * 32}]:
        if ref["domain"] == "fact" and f"fact2:{ref['digest']}" not in view_facts:
            raise K.Refusal("HIDDEN_FINDING_EVIDENCE", "fact")


neg("E-24", "HIDDEN_FINDING_EVIDENCE", hidden_finding_evidence)


def predicate_address_into_atom():
    G.address_node({"op": "exists", "relation": "file", "minResolution": "syntax",
                    "filters": []}, "p.0")


neg("E-25", "PREDICATE_ADDRESS_INTO_ATOM", predicate_address_into_atom)

vec("E-26", "positive",
    "node addressing is total and deterministic: p, p.0, p.1, p.0.0",
    ok=(G.address_node({"op": "and", "operands": [
        {"op": "not", "operand": {"op": "exists", "relation": "file",
                                  "minResolution": "syntax", "filters": []}},
        {"op": "none", "relation": "clones", "minResolution": "syntax",
         "filters": []}]}, "p.0.0")["op"] == "exists"))


# ==========================================================================
# F. Mirror-divergence probes between the foundation and workflow schemas.
# ==========================================================================
def order_annotations(doc, selector):
    node = V.DOCS[doc]
    for part in selector.lstrip("#/").split("/"):
        node = node[part]
    return node


ident_import = V.DOCS["identity"]["$defs"]["import"]["properties"]
wf_import = V.DOCS["imported"]["$defs"]["ImportWrapperV2"]["properties"]
vec("F-1", "advisory-finding",
    "identity `import.omissions` declares canonical-set while the workflow "
    "`ImportWrapperV2.omissions`, which claims to be an exact mirror, declares "
    "sequence: the same bytes are admissible in one unit and not the other",
    ok=False,
    identityOrder=ident_import["omissions"].get("x-opensip-order"),
    workflowOrder=wf_import["omissions"].get("x-opensip-order"))
vec("F-2", "advisory-finding",
    "identity `import.blobs` has no minItems while the workflow mirror requires "
    "minItems 1: an import with no blobs is admissible in one unit only",
    ok=False,
    identityMinItems=ident_import["blobs"].get("minItems"),
    workflowMinItems=wf_import["blobs"].get("minItems"))

f_scope = V.DOCS["identity"]["$defs"]["scope-descriptor"]["properties"]
w_scope = V.DOCS["imported"]["$defs"]["ImportScopeDescriptor"]["properties"]
vec("F-3", "advisory-finding",
    "identity `scope-descriptor` arrays declare canonical-set while the "
    "`ImportScopeDescriptor` 'exact mirror' declares sequence, although both "
    "name the same scopeDigest preimage",
    ok=False,
    identityOrder={k: f_scope[k].get("x-opensip-order")
                   for k in ("workspaceRoots", "pathPrefixes", "excludedPathPrefixes")},
    workflowOrder={k: w_scope[k].get("x-opensip-order")
                   for k in ("workspaceRoots", "pathPrefixes", "excludedPathPrefixes")})

reg = G.RELATION_REGISTRY["relations"]
missing_ladder = sorted(r for r, v in reg.items() if not v.get("rungs"))
vec("F-4", "blocking-finding",
    "the successor relation registry publishes NO rung for eight relations, "
    "while identity section 3 requires fact.resolution to be a rung of that "
    "relation's ladder: no file/clones/declares fact can close a Run under a "
    "literal reading",
    ok=False, relationsWithNoRung=missing_ladder,
    inheritedLadders={r: K.RELATION_LADDERS_INHERITED[r] for r in missing_ladder})

atom_res = V.DOCS["policy"]["$defs"]["Resolution"]["enum"]
rung_enum = V.DOCS["native"]["$defs"]["Rung"]["enum"]
vec("F-5", "blocking-finding",
    "the declarative program's Atom.minResolution is a four-value abstract tier "
    "while facts and Coverage carry the fifteen-value rung vocabulary, and no "
    "contract publishes the mapping the evaluator needs",
    ok=False, atomResolution=atom_res, factRung=rung_enum,
    overlap=sorted(set(atom_res) & set(rung_enum)))


# ==========================================================================
# G. Public terminations, mutation keys, pinned-purge refusal.
# ==========================================================================
TERMINATIONS = {}


def termination(label, obj, expect_valid=True):
    r = sch("common", "#/$defs/StepTermination", obj, f"termination:{label}")
    TERMINATIONS[label] = obj
    vec(f"G-{label}", "positive" if expect_valid else "negative",
        f"public termination `{label}` validates={r['valid']}",
        ok=r["valid"] == expect_valid, termination=obj, errors=r["errors"])
    return obj


RUN_ID = TS["runId"]
termination("success-fresh-project", {"class": "success"})
termination("policy-failed-authoritative",
            {"class": "policy-failed", "runId": R21["runId"]})
termination("policy-failed-ephemeral",
            {"class": "policy-failed", "authority": "ephemeral"})
termination("ephemeral-cannot-supply-authority",
            {"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
             "domainDetail": {"code": "WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY",
                              "remedy": "run an authoritative analysis first"}})
termination("provider-closure-not-installed",
            {"class": "indeterminate",
             "reasonCodes": ["COVERAGE.PROVIDER_UNAVAILABLE"],
             "domainDetail": {"code": "COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED",
                              "remedy": "opensip install provider-typescript"}})
termination("admitted-incomplete-inputs-are-authoritative-indeterminate",
            {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"],
             "runId": RPAR["runId"],
             "coverageId": [c for c in RPAR["coverages"]
                            if RPAR["coveragePayloads"][c]["key"]["relation"]
                            == "clones"][0]})
termination("required-renderer-failed-after-commit",
            {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED",
             "faultCause": "delivery-required", "runId": R21["runId"],
             "domainDetail": {"code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT",
                              "remedy": "re-render; the sealed Run is unchanged"}})
termination("evidence-purged-before-evaluation",
            {"class": "request-rejected",
             "errorCode": "REQUEST.PRECONDITION_FAILED",
             "domainDetail": {"code": "evidence.purged",
                              "remedy": "re-analyze to produce fresh evidence",
                              "subject": RUN_ID}})
termination("evidence-missing-during-a-selected-operation",
            {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
             "faultCause": "host-io",
             "domainDetail": {"code": "evidence.missing",
                              "remedy": "restore or regenerate the missing objects",
                              "subject": RUN_ID}})
termination("regeneration-mismatch",
            {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
             "faultCause": "host-io",
             "domainDetail": {"code": "evidence.regeneration-mismatch",
                              "remedy": "the sealed Run is unchanged; investigate "
                                        "the producing closure"}})
termination("backup-choice-required-in-ci",
            {"class": "request-rejected",
             "errorCode": "REQUEST.PRECONDITION_FAILED",
             "domainDetail": {"code": "storage.backup-choice-required",
                              "remedy": "--allow-backup-custody, --ephemeral, or "
                                        "an admitted storage-policy record"}})
termination("provider-lied-about-its-partition",
            {"class": "operational-failed",
             "errorCode": "PROVIDER.PROTOCOL_VIOLATION",
             "faultCause": "provider-protocol",
             "domainDetail": {"code": "native.capability-unavailable",
                              "remedy": "reinstall the provider closure"}})
termination("workspace-unit-limit",
            {"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
             "domainDetail": {"code": "PROJECT.WORKSPACE_UNIT_LIMIT",
                              "remedy": "narrow the explicit workspace selection",
                              "subject": "unitCount:4200>4096"}})
termination("scope-limit",
            {"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
             "domainDetail": {"code": "PROJECT.SCOPE_LIMIT",
                              "remedy": "narrow the explicit scope",
                              "subject": "workspaceRoots:2048>1024"}})
termination("interrupted-after-a-committed-run",
            {"class": "interrupted", "signal": "SIGINT", "runId": R21["runId"]})

# The complete pinned-purge refusal (identity section 5 + workflows section 12).
PIN_DISCLOSURE = {
    "runId": R21["runId"],
    "activePins": K.ordered([
        {"pinId": "baseline:main", "kind": "baseline"},
        {"pinId": "backup:2026-09-01", "kind": "backup-export"},
        {"pinId": "repair:cb.unused.remove", "kind": "repair-prerequisite"},
    ], {"by": ["pinId"]}),
    "consequences": ["named-pins-revoked", "dependent-evidence-replay-unavailable",
                     "sealed-history-retained"]}
termination("pinned-purge-refusal",
            {"class": "request-rejected",
             "errorCode": "REQUEST.PRECONDITION_FAILED",
             "domainDetail": {"code": "evidence.pinned",
                              "remedy": "revoke the named pins with an explicit "
                                        "destructive purge authorization",
                              "subject": R21["runId"],
                              "purgeDisclosure": PIN_DISCLOSURE}})
sch("common", "#/$defs/PinnedPurgeDisclosure", PIN_DISCLOSURE,
    "PinnedPurgeDisclosure")

# a truncated pin inventory must not satisfy the disclosure obligation
TRUNCATED = json.loads(json.dumps(PIN_DISCLOSURE))
TRUNCATED["activePins"] = TRUNCATED["activePins"][:1]
r = sch("common", "#/$defs/PinnedPurgeDisclosure", TRUNCATED,
        "PinnedPurgeDisclosure (truncated)")
vec("G-pin-truncation", "advisory-finding",
    "a SCHEMA-VALID subset of the pin inventory is still admissible: "
    "completeness is a host obligation the closed schema cannot express",
    ok=False, schemaValid=r["valid"],
    note="workflows section 12 states this explicitly; recorded as a limitation, "
         "not a defect")

# --- mutation replay scope and the distinct repair-apply key ----------------
MUT_SCOPE = {"schemaVersion": 1, "requestId": "req1_" + "3f" * 16,
             "stepId": 2, "projectId": R21["descriptors"]["run"]["projectId"],
             "operation": "import"}
MUT_KEY = K.H("workflow.mutation-intent", MUT_SCOPE)
sch("invocation", "#/$defs/MutationReplayScopeV1", MUT_SCOPE,
    "MutationReplayScopeV1")
vec("G-mutation-key", "positive",
    "generic mutation replay key = bare 64-hex H('workflow.mutation-intent', "
    "MutationReplayScopeV1) over exactly {schemaVersion,requestId,stepId,"
    "projectId,operation}",
    ok=len(MUT_KEY) == 64, scope=MUT_SCOPE, key=MUT_KEY)
OTHER_SCOPE = dict(MUT_SCOPE, requestId="req1_" + "4f" * 16)
vec("G-mutation-scope-isolation", "positive",
    "a different fresh request never deduplicates another invocation's generic "
    "mutation",
    ok=K.H("workflow.mutation-intent", OTHER_SCOPE) != MUT_KEY,
    otherKey=K.H("workflow.mutation-intent", OTHER_SCOPE))

REPAIR_KEY_PREIMAGE = {"operation": "repair-apply",
                       "projectId": R21["descriptors"]["run"]["projectId"],
                       "repairPlanId": "repairplan2:" + "6a" * 32,
                       "baseSnapshotId": R21["snapshotId"]}
REPAIR_KEY = K.raw_sha256(REPAIR_KEY_PREIMAGE)
vec("G-repair-key", "positive",
    "repair apply is the explicit content-derived exception: raw SHA-256 of the "
    "canonical {operation,projectId,repairPlanId,baseSnapshotId}, a DIFFERENT "
    "recipe from the generic H-domain mutation key",
    ok=REPAIR_KEY != MUT_KEY and len(REPAIR_KEY) == 64,
    preimage=REPAIR_KEY_PREIMAGE, key=REPAIR_KEY,
    canonicalBytes=K.C(REPAIR_KEY_PREIMAGE).decode())
vec("G-repair-key-is-not-an-h-identity", "positive",
    "the repair-apply key is a raw canonical-record digest, never H(domain, X)",
    ok=REPAIR_KEY != K.H("workflow.mutation-intent", REPAIR_KEY_PREIMAGE))

# --- comparison / audit -----------------------------------------------------
sch("comparison", "#/$defs/AuditProfile",
    {"name": "code-regression", "gateCodeNetNew": True,
     "gateNewlyLiveByPolicyAxes": False, "gateAllCurrentLive": False,
     "newWaiverSuppressesCodeNetNew": False,
     "gateRuleUnder": "baseline-or-current"},
    "AuditProfile code-regression")



# ==========================================================================
# H. Audit / comparison, authorized execution, and three further probes.
# ==========================================================================
BASELINE_ID = "baseline2:" + "1b" * 32
_IMP = list(R21["imports"].values())[0]
_IMP_ID = list(R21["imports"])[0]
_BOUND = {"kind": "dependency", "importId": _IMP_ID,
          "payloadDigest": _IMP["payloadDigest"],
          "sourceCorrespondenceDigest": _IMP["sourceCorrespondenceDigest"],
          "scopeDigest": _IMP["scopeDigest"],
          "observationDigest": _IMP["observationDigest"]}
CTX_B = {"policyDigest": "aa" * 32, "scopeDigest": "bb" * 32,
         "waiverSetDigest": "cc" * 32,
         "detectorClosureIds": [G.CL_DETECTOR["id"]],
         "evidenceAvailability": {"importKinds": ["dependency"],
                                  "relations": ["file"], "imports": [_BOUND]}}
# the current side lost the bound import: an evidence-availability change
CTX_C = {"policyDigest": "aa" * 32, "scopeDigest": "bb" * 32,
         "waiverSetDigest": "cc" * 32,
         "detectorClosureIds": [G.CL_DETECTOR["id"]],
         "evidenceAvailability": {"importKinds": [], "relations": ["file"],
                                  "imports": []}}
AUDIT_PROFILE = {"name": "code-regression", "gateCodeNetNew": True,
                 "gateNewlyLiveByPolicyAxes": False, "gateAllCurrentLive": False,
                 "newWaiverSuppressesCodeNetNew": False,
                 "gateRuleUnder": "baseline-or-current"}
DETECTORS = [{"detectorId": "cb.file.present",
              "baselineClosureId": G.CL_DETECTOR["id"],
              "currentClosureId": G.CL_DETECTOR["id"],
              "baselineSemanticsMajor": 1, "currentSemanticsMajor": 1,
              "method": "identical-closure"}]
ZERO_COUNTS = {k: 0 for k in ("UNCHANGED", "CODE-NET-NEW", "CODE-FIXED",
                              "DETECTION-DELTA", "POLICY-DELTA", "SCOPE-DELTA",
                              "WAIVER-DELTA", "EVIDENCE-DELTA", "INDETERMINATE",
                              "gating")}


def comparison(label, entries, rule_deficiencies, verdict, counts,
               performed=True, whole_reason=None, remedy=None):
    d = {"schemaFamily": "opensip.product.comparison", "schemaMajor": 1,
         "baselineId": BASELINE_ID, "currentRunId": R21["runId"],
         "currentSnapshotId": R21["snapshotId"], "auditProfile": AUDIT_PROFILE,
         "projectCorrespondence": "same-project",
         "comparisonPerformed": performed, "baselineContext": CTX_B,
         "currentContext": CTX_C,
         "contextDelta": {"codeChanged": True, "detectorChanged": False,
                          "policyChanged": False, "scopeChanged": False,
                          "waiversChanged": False,
                          "evidenceAvailabilityChanged": True},
         "pivotsAvailable": {"E0": "not-needed", "E1": "not-needed",
                             "E2": "not-needed", "E3": "not-needed"},
         "detectors": DETECTORS, "ruleDeficiencies": rule_deficiencies,
         "entries": entries, "counts": counts, "verdict": verdict}
    if whole_reason:
        d["wholeIndeterminateReason"] = whole_reason
    if remedy:
        d["remedy"] = remedy
    cid = "comparison2:" + K.H("workflow.comparison", d)
    r = sch("comparison", "#", {"comparisonResultId": cid, "descriptor": d},
            f"ComparisonResultV1:{label}")
    vec(f"H-comparison-{label}", "positive",
        f"comparison `{label}` validates and verdict={verdict}",
        ok=r["valid"], comparisonResultId=cid, verdict=verdict,
        errors=r["errors"])
    return d


FP = list(TS["findingFingerprints"])[0]
comparison("empty-result-with-a-gating-rule-deficiency", [],
           [{"ruleId": "cb.clone.present", "gating": True,
             "cause": "required-coverage-unknown"}],
           "indeterminate", dict(ZERO_COUNTS))
comparison("required-evidence-unavailable",
           [{"fingerprint": FP, "ruleId": "cb.file.present",
             "detectorId": "cb.file.present",
             "presence": {"B": True, "E0": None, "E1": True, "E2": True,
                          "E3": True, "E4": True, "waivedB": False,
                          "waivedC": False},
             "classification": "INDETERMINATE",
             "indeterminateReason": "required-evidence-unavailable",
             "subsequentDeltas": [], "liveInCurrent": True, "gates": True,
             "gateReason": "indeterminate-gating-rule"}],
           [{"ruleId": "cb.file.present", "gating": True,
             "cause": "required-evidence-unavailable"}],
           "indeterminate", dict(ZERO_COUNTS, INDETERMINATE=1, gating=1))
comparison("evidence-availability-changed",
           [{"fingerprint": FP, "ruleId": "cb.file.present",
             "detectorId": "cb.file.present",
             "presence": {"B": True, "E0": None, "E1": True, "E2": True,
                          "E3": True, "E4": False, "waivedB": False,
                          "waivedC": False},
             "classification": "INDETERMINATE",
             "indeterminateReason": "evidence-availability-changed",
             "subsequentDeltas": [], "liveInCurrent": False, "gates": False}],
           [], "indeterminate", dict(ZERO_COUNTS, INDETERMINATE=1))

TEST_PARAMS = {
    "kind": "test-execution",
    "argv": ["bin/cargo", "test", "--offline"],
    "argv0Source": {"kind": "toolchain-closure",
                    "closureId": G.CL_RS_TOOLCHAIN["id"], "member": "bin/cargo"},
    "cwdIsRoot": True, "principal": "P-TRUSTED-REPO",
    "executionClass": "test-runner", "platformId": "macos-aarch64",
    "authorizationRef": "security.repo-execution-grant.v2:" + "9d" * 32,
    "consentSource": "pre-existing-policy", "afterStep": 0,
    "timeoutMilliseconds": 600000, "maxOutputBytes": 1048576,
    "environmentAllowlist": ["CI", "LANG"],
    "effects": {"network": "DISCLOSURE-ONLY", "subprocess": "DISCLOSURE-ONLY",
                "filesystemWrite": "DISCLOSURE-ONLY",
                "environment": "ENFORCED-BY-CONSTRUCTION"}}
r = sch("test-execution", "#/$defs/TestExecutionStepParams", TEST_PARAMS,
        "TestExecutionStepParams")
vec("H-test-execution", "positive",
    "explicit test authorization: argv[0] is a member of the sealed toolchain "
    "closure, CI uses pre-existing policy consent, and every effect equals the "
    "security truth-table row (DISCLOSURE-ONLY x3, ENFORCED-BY-CONSTRUCTION)",
    ok=r["valid"], params=TEST_PARAMS, errors=r["errors"])

BAD_TEST = json.loads(json.dumps(TEST_PARAMS))
BAD_TEST["effects"]["network"] = "ENFORCED-AT-HOST-BROKER"
vec("H-test-confinement-claim", "advisory-finding",
    "a stronger-than-measured enforcement claim is TEST.CONFINEMENT_CLAIM_REFUSED "
    "by prose, but the closed EnforcementValue enum admits the stronger token: "
    "the refusal is a host-side truth-table join, not a schema property",
    ok=False,
    schemaValid=sch("test-execution", "#/$defs/TestExecutionStepParams",
                    BAD_TEST, "TestExecutionStepParams (over-claimed)")["valid"])

PREP_PARAMS = {"kind": "native-preparation",
               "authorizationDescriptorDigest": "7e" * 32,
               "securityGrantSetRef": "security.repo-execution-grants.v2:" + "8e" * 32}
r = sch("invocation", "#/$defs/NativePreparationParams", PREP_PARAMS,
        "NativePreparationParams")
vec("H-native-preparation", "positive",
    "explicit preparation authorization: a preflight descriptor digest plus an "
    "operational grant-set reference, both excluded from the semantic Plan",
    ok=r["valid"], params=PREP_PARAMS, errors=r["errors"])

REPAIR_PARAMS = {"kind": "repair-apply", "planStep": 1,
                 "repairPlanId": REPAIR_KEY_PREIMAGE["repairPlanId"],
                 "consentSource": "interactive",
                 "authorizationRef": "security.repair-apply-authorization.v1:"
                                     + "af" * 32}
r = sch("invocation", "#/$defs/RepairApplyParams", REPAIR_PARAMS,
        "RepairApplyParams")
vec("H-repair-apply", "positive",
    "explicit repair authorization is a separate security record bound to the "
    "exact repairPlanId and base snapshot, not a repository-execution grant",
    ok=r["valid"], params=REPAIR_PARAMS, errors=r["errors"])

# --- three further design probes -------------------------------------------
param_rows = V.DOCS["identity"]["x-opensip-payload-registry"]["classes"]["parameter"]["rows"]
vec("F-6", "blocking-finding",
    "the comparison contract requires ScopeDocumentV1 to be bound as an "
    "analysis-spec parameter, but the closed `parameter` payload-registry class "
    "has exactly one row and it is not that document, so such a parameter refuses",
    ok=False, parameterRegistryRows=sorted(param_rows),
    requiredBy="workflows/schemas/comparison-result.schema.json"
               "#/$defs/EvaluationContext.scopeDigest")

universe_domains = sorted(
    V.DOCS["identity"]["x-opensip-digest-domains"]["domainSets"]
    ["native-semantic-universe"])
vec("F-7", "blocking-finding",
    "fact2.sourceUniverse/targetUniverse and subject-scope are REQUIRED "
    "h-identities of the native-semantic-universe domain set, which registers "
    "only TypeScript and Rust; native section 1.2 gives language mode "
    "`syntax-only` no universe, so its supported declares/literal/control-flow/"
    "clones facts have no admissible universe value",
    ok=False, registeredUniverseDomains=universe_domains,
    syntaxOnlySupportedRelations=["clones", "control-flow", "declares", "literal"])

vec("F-8", "blocking-finding",
    "no NativeCause member names absent, partial or ambiguous source-unit "
    "ownership, and section 10's input-closure-incomplete row enumerates causes "
    "that exclude it, so the required partial-ownership Coverage disclosure has "
    "no publishable typed cause",
    ok=False,
    nativeCauseEnum=V.DOCS["native"]["$defs"]["NativeCause"]["enum"],
    usedInThisReconstruction="deficiency=input-closure-incomplete, nativeCause=null")

ladder_doc = json.load(open(os.path.join(
    V.SUBJECT,
    "docs/coop/design-corrections/native/capability-manifest-domains.v2.json")))
vec("F-4b", "positive",
    "the ladder values DO exist in the kit, in the capability-manifest ADM-DOMAIN "
    "registry, and agree exactly with the inherited fact-plane ladders; what is "
    "missing is the binding of that registry to fact2.resolution",
    ok=all(sorted(v) == sorted(K.RELATION_LADDERS_INHERITED[k])
           for k, v in ladder_doc["registries"]["RELATION-LADDER-DOMAIN-V2"]
           ["ladders"].items()),
    ladderRegistryBoundPositions=ladder_doc["registries"]
    ["RELATION-LADDER-DOMAIN-V2"]["boundPositions"])


def emit():
    os.makedirs(OUT, exist_ok=True)
    vec_rows = VEC.run_all() + V_ROWS
    payload = {
        "producer": "blind consumer-B independent reconstruction",
        "canonicalHelper": "cb_canonical.py (authored from prose only)",
        "vectors": vec_rows,
        "schemaChecks": S_ROWS,
        "graphs": {k: strip(v) for k, v in GRAPHS.items()},
        "terminations": TERMINATIONS,
        "pinnedPurgeDisclosure": PIN_DISCLOSURE,
        "mutationReplayScope": {"scope": MUT_SCOPE, "key": MUT_KEY},
        "repairApplyKey": {"preimage": REPAIR_KEY_PREIMAGE, "key": REPAIR_KEY},
        "counts": {
            "vectors": len(vec_rows),
            "vectorsFailing": len([r for r in vec_rows
                                   if not r["ok"]
                                   and not r["kind"].endswith("-finding")]),
            "designFindings": len([r for r in vec_rows
                                   if r["kind"].endswith("-finding")]),
            "schemaChecks": len(S_ROWS),
            "schemaChecksInvalid": len([r for r in S_ROWS if not r["valid"]]),
            "retainedBlobs": len(G.BLOBS), "retainedFrames": len(G.FRAMES),
            "retainedRecords": len(G.RECORDS)},
    }
    with open(os.path.join(OUT, "cb-vectors.json"), "w") as fh:
        json.dump(payload, fh, indent=1, sort_keys=True, ensure_ascii=False)
    return payload


def strip(g):
    out = {k: v for k, v in g.items() if k != "ctxdata"}
    return out


if __name__ == "__main__":
    p = emit()
    print(json.dumps(p["counts"], indent=1))
    for r in p["vectors"]:
        if not r["ok"] and not r["kind"].endswith("-finding"):
            print("NOT-OK", r["id"], r["kind"], r["detail"][:90])
    for r in p["schemaChecks"]:
        if not r["valid"]:
            print("SCHEMA-INVALID", r["label"], r["errors"][:2])
