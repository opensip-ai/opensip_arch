"""Native closures, contexts, nested records and universe binding (independent reconstruction).

Sources: identity-and-evidence s3 (closure recipe, closing digest law, domainSets rows), native-evidence
s1.2 (syntax context/universe), s2.1-2.4 (rust-v2, typescript-v2, NativeContextV2, TypeScriptNativeContextV2),
s3 (dependency source set, cargo projection, unified features, prepared set), s11 (domains, SourceUnitOwnershipV1),
native-evidence.schemas.v2.json (#/x-opensip-grammar-capability-registry, #/x-opensip-config-node-kind-law) and
identity-schemas.v3.json#/x-opensip-digest-domains (domainSets, closureKinds, languageVersionBinding).

Refusal keys: names quoted by the kit are used verbatim; keys this reconstruction had to name itself carry the
prefix 'cb24.' so they are never mistaken for published vocabulary.
"""
import hashlib
import unicodedata

import canonical as K
import schemas

KIT = schemas.kit()
NE = "native/native-evidence.schemas.v2.json"
ID = "foundation/identity-schemas.v3.json"
DOMAINS = KIT.doc(ID)["x-opensip-digest-domains"]
CTX_SET = set(DOMAINS["domainSets"]["native-context"].keys())
UNI_SET = set(DOMAINS["domainSets"]["native-semantic-universe"].keys())
NESTED_SET = set(DOMAINS["domainSets"]["native-nested"].keys())
GRAMMAR_REG = KIT.doc(NE)["x-opensip-grammar-capability-registry"]
KIND_LAW = KIT.doc(NE)["x-opensip-config-node-kind-law"]


class Refusal(Exception):
    def __init__(self, key, detail=""):
        super().__init__(f"{key}:{detail}" if detail else key)
        self.key = key
        self.detail = detail


def inv_map(inventory):
    return {row["path"]: row for row in inventory}


def schema_or_refuse(value, rel, selector, key):
    r = KIT.admit(value, rel, selector)
    if not r["ok"]:
        raise Refusal(key, f"{selector}:{(r['typed'] or '')}{r['stock'][:2]}{r['order'][:2]}")
    return r


# ------------------------------------------------------------------ closures
def admit_closure(store, closure_id, want_kind=None, refusal_prefix="native.native-context-closure"):
    """closure2 identity recomputed from the retained frame; kind checked; every tree blob retained at its
    declared length (BLOB_LENGTH); manifest body bytes retained (raw-artifact preimage)."""
    if not isinstance(closure_id, str) or not closure_id.startswith("closure2:"):
        raise Refusal(f"{refusal_prefix}-unretained", str(closure_id))
    hx = closure_id.split(":", 1)[1]
    if hx not in store.blobs:
        raise Refusal(f"{refusal_prefix}-unretained", closure_id)
    try:
        domain, desc = store.get_frame(hx, {"closure"})
    except K.AdmissionError as exc:
        raise Refusal(f"{refusal_prefix}-identity-mismatch", exc.boundary)
    if K.H("closure", desc) != hx:
        raise Refusal(f"{refusal_prefix}-identity-mismatch", closure_id)
    schema_or_refuse(desc, ID, "#/$defs/closure", "cb24.closure-schema")
    if want_kind is not None and desc["kind"] != want_kind:
        raise Refusal(f"{refusal_prefix}-kind-mismatch", f"{closure_id}:{desc['kind']}!={want_kind}")
    for row in desc["tree"]:
        b = store.blobs.get(row["sha256"])
        if b is None:
            raise Refusal("EVIDENCE_UNAVAILABLE", f"closure-tree:{row['path']}")
        if len(b) != row["bytes"]:
            raise Refusal("BLOB_LENGTH", row["path"])
    if desc["manifestDigest"] not in store.blobs:
        raise Refusal("EVIDENCE_UNAVAILABLE", "closure.manifestDigest")
    return desc


def tree_digests(desc):
    return {row["sha256"] for row in desc["tree"]}


# ------------------------------------------------------------------ frames of native records
def get_native_frame(store, hexdigest, allowed, missing_key):
    if hexdigest not in store.blobs:
        raise Refusal(missing_key, hexdigest)
    try:
        return store.get_frame(hexdigest, allowed)
    except K.AdmissionError as exc:
        raise Refusal("cb24.native-frame-invalid", f"{hexdigest}:{exc.boundary}")


def nested_identity(store, sha256_text_or_hex, domain, selector):
    hx = sha256_text_or_hex[7:] if sha256_text_or_hex.startswith("sha256:") else sha256_text_or_hex
    d, rec = get_native_frame(store, hx, {domain}, "EVIDENCE_UNAVAILABLE")
    if d != domain:
        raise Refusal("cb24.nested-identity-domain", f"{d}!={domain}")
    schema_or_refuse(rec, NE, selector, "cb24.nested-record-schema")
    if K.H(domain, rec) != hx:
        raise Refusal("cb24.nested-identity-mismatch", domain)
    return rec


def canonical_record(store, hexdigest, selector, rel=NE):
    if hexdigest not in store.blobs:
        raise Refusal("EVIDENCE_UNAVAILABLE", hexdigest)
    rec = store.get_record(hexdigest)
    schema_or_refuse(rec, rel, selector, "cb24.canonical-record-schema")
    return rec


# ------------------------------------------------------------------ TypeScript context
def lib_fold(name):
    # Unicode default full, non-tailored, context-sensitive lowercase (Python str.lower implements
    # SpecialCasing and Final_Sigma). Case-data version is reported by unicode_case_data_version().
    return name.lower()


def unicode_case_data_version():
    return unicodedata.unidata_version


def admit_typescript_context(store, ctx, inventory):
    schema_or_refuse(ctx, NE, "#/$defs/TypeScriptNativeContextV2", "cb24.ts-context-schema")
    refusals = []
    inv = inv_map(inventory)
    tool = admit_closure(store, ctx["toolClosure"]["closureId"], "toolchain")
    stdlib = admit_closure(store, "closure2:" + ctx["toolchain"]["typescriptStdlibMerkleRoot"], "stdlib")
    tc = ctx["toolchain"]
    if tc["compilerVersion"] != tool["semanticVersion"]:
        refusals.append("native.native-context-compiler-version-not-from-manifest")
    td = tree_digests(tool)
    for field in ("compiler", "runtime"):
        if ctx["toolClosure"][field] not in td:
            refusals.append(f"native.native-context-tool-not-in-closure:{field}")
    if tc["compilerPackageDigest"] not in td:
        refusals.append("native.native-context-tool-not-in-closure:compilerPackageDigest")
    # complete declaration-file inventory of the stdlib tree, by basename
    dts = {}
    for row in stdlib["tree"]:
        base = row["path"].split("/")[-1]
        if base.endswith(".d.ts"):
            if base in dts:
                refusals.append(f"native.native-context-stdlib-tree-ambiguous-basename:{base}")
            dts[base] = row["sha256"]
    declared = {c["component"]: c["sha256"] for c in tc["standardLibraryComponentDigests"]}
    for base in sorted(dts):
        if base not in declared:
            refusals.append(f"native.native-context-stdlib-inventory-incomplete:{base}")
        elif declared[base] != dts[base]:
            refusals.append(f"native.native-context-stdlib-tree-mismatch:{base}")
    for base in declared:
        if base not in dts:
            refusals.append(f"native.native-context-stdlib-tree-mismatch:{base}")
    honored = ctx["configProjection"]["honoredOptions"]
    folds = [lib_fold(n) for n in tc["libSelection"]]
    if len(set(folds)) != len(folds):
        refusals.append("native.native-context-field-mismatch:duplicate-lib-selection")
    if set(folds) != {lib_fold(m) for m in honored["lib"]}:
        refusals.append("native.native-context-field-mismatch:libSelection")
    for n in tc["libSelection"]:
        if "lib." + lib_fold(n) + ".d.ts" not in declared:
            refusals.append(f"native.native-context-lib-not-retained:{n}")
    if ctx["moduleResolutionMode"] != honored["moduleResolution"]:
        refusals.append("native.native-context-field-mismatch:moduleResolutionMode")
    mode = ctx["languageMode"]
    if mode == "ts-tsconfig" and honored["allowJs"]:
        refusals.append("native.native-context-field-mismatch:languageMode-allowJs")
    if mode in ("js-allowjs", "js-synthesized") and not honored["allowJs"]:
        refusals.append("native.native-context-field-mismatch:languageMode-allowJs")
    if mode == "js-synthesized" and ctx["configProjection"]["configGraphPaths"]:
        refusals.append("native.native-context-field-mismatch:synthesized-config-graph")
    for p in ctx["configProjection"]["configGraphPaths"]:
        if p not in inv:
            refusals.append(f"cb24.snapshot-join:configGraphPaths:{p}")
    lf = ctx["lockfileIdentity"]
    if lf is not None:
        row = inv.get(lf["path"])
        if row is None or row["sha256"] != lf["contentSha256"]:
            refusals.append(f"cb24.snapshot-join:lockfileIdentity:{lf['path']}")
    layout = None
    if ctx["nodeModulesLayoutDigest"] is not None:
        layout = canonical_record(store, ctx["nodeModulesLayoutDigest"], "#/$defs/ResolvedNodeModulesLayoutV1")
        install = {e["installPath"] for e in layout["entries"]}
        for e in layout["entries"]:
            if e["contentSha256"] not in store.blobs:
                refusals.append(f"EVIDENCE_UNAVAILABLE:nodeModulesLayout:{e['installPath']}")
            if e["realPath"] != e["installPath"] and e["realPath"] not in install:
                refusals.append(f"cb24.node-modules-realpath-unbound:{e['installPath']}")
    return {"closures": {"toolchain": tool, "stdlib": stdlib}, "layout": layout, "refusals": refusals}


# ------------------------------------------------------------------ Rust context
def admit_rust_context(store, ctx, inventory):
    schema_or_refuse(ctx, NE, "#/$defs/NativeContextV2", "cb24.rust-context-schema")
    refusals = []
    inv = inv_map(inventory)
    tool = admit_closure(store, ctx["toolClosure"]["closureId"], "toolchain")
    llvm = admit_closure(store, "closure2:" + ctx["toolchain"]["rustcDevLlvmDigest"], "rust-dev-llvm")
    tc = ctx["toolchain"]
    if tc["rustcVersion"] != tool["semanticVersion"]:
        refusals.append("native.native-context-compiler-version-not-from-manifest")
    if tc["targetTriple"] != ctx["targetTriple"]:
        refusals.append("native.native-context-field-mismatch:targetTriple")
    td = tree_digests(tool)
    for field in ("rustc", "cargo", "procMacroServer", "linker", "ar"):
        v = ctx["toolClosure"][field]
        if v is not None and v not in td:
            refusals.append(f"native.native-context-tool-not-in-closure:{field}")
    ld = tree_digests(llvm)
    for comp in tc["standardLibraryComponentDigests"]:
        if comp["sha256"] not in ld:
            refusals.append(f"native.native-context-stdlib-tree-mismatch:{comp['component']}")
    if tc["sysrootDigest"] not in store.blobs:
        refusals.append("EVIDENCE_UNAVAILABLE:sysrootDigest")
    dep = nested_identity(store, ctx["dependencySourceSetId"], "native.dependency-source-set.v1", "#/$defs/DependencySourceSetV1")
    for pkg in dep["packages"]:
        rows = get_native_frame(store, pkg["fileManifestSha256"], {"native.dependency-file-manifest.v1"}, "EVIDENCE_UNAVAILABLE")[1]
        schema_or_refuse(rows, NE, "#/$defs/DependencyFileManifestV1", "cb24.file-manifest-schema")
        if K.H("native.dependency-file-manifest.v1", rows) != pkg["fileManifestSha256"]:
            refusals.append(f"cb24.file-manifest-identity:{pkg['name']}")
        if pkg["fileCount"] != len(rows) or pkg["totalBytes"] != sum(r["byteLength"] for r in rows):
            refusals.append(f"cb24.file-manifest-counts:{pkg['name']}")
        for r in rows:
            b = store.blobs.get(r["contentSha256"])
            if b is None:
                refusals.append(f"EVIDENCE_UNAVAILABLE:dependency:{pkg['name']}:{r['path']}")
            elif len(b) != r["byteLength"]:
                refusals.append(f"BLOB_LENGTH:dependency:{pkg['name']}:{r['path']}")
        if pkg["checksumVerification"] == "mismatch":
            refusals.append(f"cb24.dependency-checksum-mismatch:{pkg['name']}")
    feats = nested_identity(store, ctx["unifiedFeaturesId"], "native.unified-features.rust.v1", "#/$defs/UnifiedFeaturesV1")
    if feats["targetTriple"] != ctx["targetTriple"] or feats["resolverVersion"] != ctx["resolverVersion"]:
        refusals.append("native.native-context-field-mismatch:unifiedFeatures")
    prepared = None
    if ctx["preparedOutputSetId"] is not None:
        prepared = nested_identity(store, ctx["preparedOutputSetId"], "native.prepared-output-set.v3", "#/$defs/PreparedOutputSetV3")
        for row in prepared["rows"]:
            if row["kind"] in ("proc-macro-dylib", "build-script-binary"):
                refusals.append("native.prepared-output-not-inert")
            b = store.blobs.get(row["blob"]["sha256"])
            if b is None or len(b) != row["blob"]["byteLength"]:
                refusals.append(f"EVIDENCE_UNAVAILABLE:prepared:{row['ownerKey']}")
    cp = ctx["configProjection"]
    for p in cp["replacedSnapshotConfigs"]:
        if p not in inv:
            refusals.append(f"cb24.snapshot-join:replacedSnapshotConfigs:{p}")
    if cp["projectionSha256"] not in store.blobs:
        refusals.append("EVIDENCE_UNAVAILABLE:configProjection.projectionSha256")
    return {"closures": {"toolchain": tool, "rust-dev-llvm": llvm}, "dependencySourceSet": dep, "unifiedFeatures": feats,
            "preparedOutputSet": prepared, "refusals": refusals}


# ------------------------------------------------------------------ Syntax context
def admit_syntax_context(store, ctx, inventory):
    schema_or_refuse(ctx, NE, "#/$defs/SyntaxNativeContextV2", "cb24.syntax-context-schema")
    refusals = []
    gb = ctx["grammarBundle"]
    grammar = admit_closure(store, gb["closureId"], "grammar")
    if gb["parserVersion"] != grammar["semanticVersion"]:
        refusals.append("native.syntax-grammar-version-not-from-manifest")
    td = tree_digests(grammar)
    if gb["bundleDigest"] not in td:
        refusals.append("cb24.syntax-bundle-manifest-not-in-tree")
    if gb["normalizer"]["specificationDigest"] not in td:
        refusals.append("cb24.syntax-normalizer-spec-not-in-tree")
    seen_suffix = {}
    langs = GRAMMAR_REG["languages"]
    for g in gb["grammars"]:
        if g["grammarDigest"] not in td:
            refusals.append(f"cb24.syntax-grammar-definition-not-in-tree:{g['grammarId']}")
        reg = langs.get(g["languageId"])
        if reg is None:
            refusals.append(f"cb24.syntax-grammar-language-unbundled:{g['languageId']}")
            continue
        if g["syntaxClass"] != reg["syntaxClass"]:
            refusals.append(f"cb24.syntax-grammar-class-contradicts-registry:{g['grammarId']}")
        for s in g["suffixes"]:
            if s not in reg["suffixes"]:
                refusals.append(f"cb24.syntax-grammar-suffix-not-of-language:{g['grammarId']}:{s}")
            if s in seen_suffix:
                refusals.append(f"native.syntax-grammar-suffix-ambiguous:{s}")
            seen_suffix[s] = g["grammarId"]
    return {"closures": {"grammar": grammar}, "refusals": refusals}


def admit_native_context(store, context_hex, inventory):
    """Retained-frame admission entry point dispatched on the frame's H domain."""
    domain, ctx = get_native_frame(store, context_hex, CTX_SET, "EVIDENCE_UNAVAILABLE")
    if K.H(domain, ctx) != context_hex:
        raise Refusal("cb24.native-context-identity-mismatch", context_hex)
    if domain == "native.context.typescript.v2":
        detail = admit_typescript_context(store, ctx, inventory)
        lang = "typescript"
    elif domain == "native.context.rust.v2":
        detail = admit_rust_context(store, ctx, inventory)
        lang = "rust"
    else:
        detail = admit_syntax_context(store, ctx, inventory)
        lang = "syntax"
    return {"language": lang, "domain": domain, "context": ctx, "nativeContextId": "sha256:" + context_hex,
            "planNativeContextDigest": context_hex, "refusals": detail.pop("refusals"), "detail": detail}


# ------------------------------------------------------------------ universe binding
def config_graph_faults(graph, ctx, inventory):
    faults = []
    inv = inv_map(inventory)
    paths = [n["path"] for n in graph["nodes"]]
    if set(paths) != set(ctx["configProjection"]["configGraphPaths"]):
        faults.append("cb24.config-graph-paths-contradict-context")
    byp = {n["path"]: n for n in graph["nodes"]}
    for n in graph["nodes"]:
        base = n["path"].split("/")[-1]
        want = KIND_LAW["basenames"].get(base, KIND_LAW["otherwise"])
        if n["kind"] != want:
            faults.append(f"native.config-graph-kind-contradicts-path:{n['path']}")
        row = inv.get(n["path"])
        if row is None or row["sha256"] != n["contentSha256"]:
            faults.append(f"cb24.config-graph-node-not-inventoried:{n['path']}")
        for e in n["extendsResolved"]:
            if e not in byp:
                faults.append(f"cb24.config-graph-edge-unbound:{n['path']}->{e}")
    entry = graph["entryConfigPath"]
    if entry is None:
        if graph["nodes"]:
            faults.append("cb24.config-graph-synthesized-with-nodes")
    else:
        if entry not in byp:
            faults.append("cb24.config-graph-entry-not-a-node")
        else:
            seen, stack, onstack = set(), [], set()

            def dfs(p):
                if p in onstack:
                    faults.append(f"cb24.config-graph-cycle:{p}")
                    return
                if p in seen:
                    return
                seen.add(p)
                onstack.add(p)
                for e in byp[p]["extendsResolved"]:
                    if e in byp:
                        dfs(e)
                onstack.discard(p)
            dfs(entry)
            for p in byp:
                if p not in seen:
                    faults.append(f"cb24.config-graph-node-unreachable:{p}")
    return faults


def derived_config_origin(graph):
    if graph["entryConfigPath"] is None and not graph["nodes"]:
        return "synthesized"
    entry = next(n for n in graph["nodes"] if n["path"] == graph["entryConfigPath"])
    return "jsconfig" if entry["kind"] == "jsconfig" else "tsconfig"


def bind_typescript_universe(store, uni, admission, context, inventory):
    if context is None:
        raise Refusal("native.universe-context-not-supplied")
    schema_or_refuse(uni, NE, "#/$defs/TypeScriptUniverseV2ResolvedInputs", "cb24.ts-universe-schema")
    faults = []
    if admission["domain"] != "native.context.typescript.v2":
        raise Refusal("native.native-context-language-mismatch")
    if uni["nativeContextId"] != admission["nativeContextId"]:
        raise Refusal("native.universe-context-binding-mismatch")
    if "sha256:" + K.H("native.context.typescript.v2", context) != admission["nativeContextId"]:
        raise Refusal("native.universe-context-binding-mismatch", "context-bytes-are-not-the-admitted-ones")
    honored = context["configProjection"]["honoredOptions"]
    graph = canonical_record(store, uni["tsconfigGraphHash"], "#/$defs/TypeScriptConfigGraphV1")
    faults += config_graph_faults(graph, context, inventory)
    expect = {
        "languageMode": context["languageMode"],
        "packageModuleType": context["packageModuleType"],
        "allowJs": honored["allowJs"],
        "checkJs": honored["checkJs"],
        "lockfileKind": context["lockfileIdentity"]["kind"] if context["lockfileIdentity"] else "none",
        "nodeModulesInReadSet": context["nodeModulesLayoutDigest"] is not None,
        # HC-20: native s2.2 lines 538-540
        "jsAdmittedToProgram": honored["allowJs"] and len(uni["jsRootFiles"]) > 0,
        "jsDiagnosticsEnabled": honored["checkJs"],
        "configOrigin": derived_config_origin(graph),
    }
    for f, v in expect.items():
        if uni[f] != v:
            faults.append(f"native.universe-context-field-mismatch:{f}")
    synthesized = uni["languageMode"] == "js-synthesized"
    if synthesized != (uni["synthesizedOptions"] is not None) or synthesized != (uni["synthesizerVersion"] is not None):
        faults.append("native.universe-context-field-mismatch:synthesizedOptions")
    if uni["synthesizedOptions"] is not None:
        for k, v in uni["synthesizedOptions"].items():
            if honored.get(k) != v:
                faults.append(f"native.universe-context-field-mismatch:synthesizedOptions.{k}")
        if "jsx" not in uni["synthesizedOptions"] and honored["jsx"] is not None:
            faults.append("native.universe-context-field-mismatch:synthesizedOptions.jsx")
    if (graph["entryConfigPath"] is None) != (not context["configProjection"]["configGraphPaths"]):
        faults.append("native.universe-context-field-mismatch:extends-graph-emptiness")
    inv = inv_map(inventory)
    for p in uni["programRootFiles"]:
        if p not in inv:
            faults.append(f"cb24.snapshot-join:programRootFiles:{p}")
    if not set(uni["jsRootFiles"]) <= set(uni["programRootFiles"]):
        faults.append("cb24.jsRootFiles-not-program-roots")
    return {"language": "typescript", "configGraph": graph, "faults": faults}


def compilation_unit_id(row):
    return "sha256:" + K.H("native.compilation-unit.v1", {"schemaVersion": 1, "markerPath": row["markerPath"],
                                                           "targetKind": row["targetKind"], "targetName": row["targetName"]})


def bind_rust_universe(store, uni, admission, context, inventory, ctx_detail):
    if context is None:
        raise Refusal("native.universe-retained-inputs-not-supplied")
    schema_or_refuse(uni, NE, "#/$defs/RustUniverseV2ResolvedInputs", "cb24.rust-universe-schema")
    faults = []
    if admission["domain"] != "native.context.rust.v2":
        raise Refusal("native.native-context-language-mismatch")
    if uni["nativeContextId"] != admission["nativeContextId"]:
        raise Refusal("native.universe-context-binding-mismatch")
    for f in DOMAINS["domainSets"]["native-semantic-universe"]["native.semantic-universe.rust.v2"]["contextAgreementFields"]:
        if uni[f] != context[f]:
            faults.append(f"native.universe-context-field-mismatch:{f}")
    if uni["rustflags"] != context["configProjection"]["rustflags"]:
        faults.append("native.universe-context-field-mismatch:rustflags")
    if uni["configProjectionSha256"] != K.H("native.cargo-config-projection.v2", context["configProjection"]):
        faults.append("native.universe-context-field-mismatch:configProjectionSha256")
    # the retained nested projection frame must exist under the suffix (preimage-frame)
    try:
        nested = get_native_frame(store, uni["configProjectionSha256"], {"native.cargo-config-projection.v2"}, "EVIDENCE_UNAVAILABLE")[1]
        if nested != context["configProjection"]:
            faults.append("cb24.cargo-config-projection-frame-contradicts-context")
    except Refusal as r:
        faults.append(r.key)
    if uni["executionCapableResolution"] != (uni["preparedResolution"] != "none"):
        faults.append("native.universe-context-field-mismatch:executionCapableResolution")
    if (uni["preparedOutputSetId"] is None) != (uni["preparedResolution"] == "none"):
        faults.append("native.universe-context-field-mismatch:preparedResolution")
    base = context["baseCfg"]
    ids = [c["cfgSetId"] for c in uni["cfgSets"]]
    if len(set(ids)) != len(ids):
        faults.append("native.universe-context-field-mismatch:cfgSets-duplicate-id")
    for c in uni["cfgSets"]:
        if not set(base) <= set(c["cfg"]):
            faults.append(f"native.universe-context-field-mismatch:cfgSets-drops-base-cfg:{c['cfgSetId']}")
    inv = inv_map(inventory)
    lf = uni["lockfileIdentity"]
    row = inv.get(lf["path"])
    if row is None or row["sha256"] != lf["contentSha256"]:
        faults.append("cb24.snapshot-join:lockfileIdentity")
    if ctx_detail["dependencySourceSet"]["lockfileIdentity"] != lf:
        faults.append("cb24.dependency-set-lockfile-contradicts-universe")
    for p in uni["crateRootPaths"]:
        if p not in inv:
            faults.append(f"cb24.snapshot-join:crateRootPaths:{p}")
    ownership = None
    if uni["sourceUnitOwnershipId"] is not None:
        ownership = nested_identity(store, uni["sourceUnitOwnershipId"], "native.source-unit-ownership.v1", "#/$defs/SourceUnitOwnershipV1")
        unit_ids = set()
        for u in ownership["units"]:
            if compilation_unit_id(u) != u["unitId"]:
                faults.append(f"cb24.sourceUnitOwnership.unitId-not-derived:{u['unitId']}")
            unit_ids.add(u["unitId"])
            if u["markerPath"] not in inv:
                faults.append(f"cb24.snapshot-join:ownership-marker:{u['markerPath']}")
            if u["crateName"] not in uni["edition"]:
                faults.append(f"cb24.ownership-crate-not-in-edition-map:{u['crateName']}")
        for s in ownership["selectedUnitIds"]:
            if s not in unit_ids:
                faults.append(f"cb24.ownership-selection-unbound:{s}")
        for o in ownership["ownership"]:
            if o["unitId"] not in unit_ids:
                faults.append(f"cb24.ownership-row-unbound:{o['unitId']}")
            if o["path"] not in inv:
                faults.append(f"cb24.snapshot-join:ownership-path:{o['path']}")
    return {"language": "rust", "sourceUnitOwnership": ownership, "faults": faults}


def bind_syntax_universe(store, uni, admission, context, inventory):
    if context is None:
        raise Refusal("native.universe-context-not-supplied")
    schema_or_refuse(uni, NE, "#/$defs/SyntaxUniverseV2ResolvedInputs", "cb24.syntax-universe-schema")
    faults = []
    if admission["domain"] != "native.context.syntax.v2":
        raise Refusal("native.native-context-language-mismatch")
    if uni["nativeContextId"] != admission["nativeContextId"]:
        raise Refusal("native.universe-context-binding-mismatch")
    ids = {g["grammarId"] for g in context["grammarBundle"]["grammars"]}
    for g in uni["selectedGrammarIds"]:
        if g not in ids:
            faults.append(f"native.syntax-grammar-not-in-bundle:{g}")
    return {"language": "syntax", "faults": faults}


def bind_universe(store, universe_hex, admissions_by_context_hex, inventory):
    domain, uni = get_native_frame(store, universe_hex, UNI_SET, "EVIDENCE_UNAVAILABLE")
    if K.H(domain, uni) != universe_hex:
        raise Refusal("cb24.universe-identity-mismatch", universe_hex)
    row = DOMAINS["domainSets"]["native-semantic-universe"][domain]
    ctx_hex = uni["nativeContextId"][7:]
    adm = admissions_by_context_hex.get(ctx_hex)
    if adm is None:
        raise Refusal("cb24.universe-context-not-plan-selected", uni["nativeContextId"])
    if adm["domain"] != row["contextDomain"]:
        raise Refusal("native.native-context-language-mismatch", f"{domain}->{adm['domain']}")
    if domain == "native.semantic-universe.typescript.v2":
        b = bind_typescript_universe(store, uni, adm, adm["context"], inventory)
    elif domain == "native.semantic-universe.rust.v2":
        b = bind_rust_universe(store, uni, adm, adm["context"], inventory, adm["detail"])
    else:
        b = bind_syntax_universe(store, uni, adm, adm["context"], inventory)
    b.update({"domain": domain, "universe": uni, "universeHex": universe_hex, "contextAdmission": adm, "row": row})
    return b


# ------------------------------------------------------------------ body-language-version (derived)
def suffix_select(table, path):
    best = None
    for suf in table:
        if path.endswith(suf) and (best is None or len(suf) > len(best)):
            best = suf
    return best


def rust_dialect(bound, path):
    """Rust languageVersionBinding decision order (identity digest-domains rust row selectionLaw)."""
    uni = bound["universe"]
    own = bound["sourceUnitOwnership"]
    if own is None:
        return None, "BODY_LANGUAGE_OWNERSHIP_REQUIRED"
    if own["enumeration"] == "partial":
        return None, "BODY_LANGUAGE_OWNER_UNENUMERATED"
    units = {u["unitId"]: u for u in own["units"]}
    rows = [o for o in own["ownership"] if o["path"] == path]
    if not rows:
        return None, "BODY_LANGUAGE_OWNER_NOT_COMPILED"
    sel = [o for o in rows if o["unitId"] in set(own["selectedUnitIds"])]
    if not sel:
        return None, "BODY_LANGUAGE_OWNER_NOT_SELECTED"
    eds = set()
    for o in sel:
        u = units[o["unitId"]]
        eds.add(u["targetEdition"] if u["targetEdition"] is not None else uni["edition"].get(u["crateName"]))
    if None in eds:
        return None, "BODY_LANGUAGE_DIALECT_ABSENT"
    if len(eds) != 1:
        return None, "BODY_LANGUAGE_OWNER_AMBIGUOUS"
    return {"edition": eds.pop()}, None


def body_language_version(bound, path):
    """Returns (record, languageId, refusalKey)."""
    row = bound["row"]
    lvb = row["languageVersionBinding"]
    ctx = bound["contextAdmission"]["context"]
    dialect = lvb["dialect"]
    if dialect["form"] == "closed-suffix-table":
        suf = suffix_select(dialect["table"], path)
        if suf is None:
            return None, None, dialect["onUnknown"]
        variant = dialect["table"][suf]
        lang = lvb["bodyLanguageByVariant"][variant]
        dvalue = {dialect["key"]: variant}
    else:
        dvalue, refusal = rust_dialect(bound, path)
        if refusal:
            return None, None, refusal
        lang = lvb["bodyLanguage"]
    fields = {}
    for name, spec in lvb["fields"].items():
        if "const" in spec:
            fields[name] = spec["const"]
        else:
            cur = ctx
            for p in spec["path"]:
                cur = cur[p]
            fields[name] = cur
    rec = {"schemaVersion": 1, "languageId": lang, "compilerName": fields["compilerName"],
           "compilerVersion": fields["compilerVersion"], "compilerBuild": fields["compilerBuild"], "dialect": dvalue}
    r = KIT.admit(rec, ID, "#/$defs/body-language-version")
    if not r["ok"]:
        return None, None, "cb24.body-language-version-schema"
    return rec, lang, None
