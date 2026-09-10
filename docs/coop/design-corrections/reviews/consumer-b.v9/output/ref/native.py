"""Native context admission and universe binding, reconstructed from prose.

Sources: native-evidence.md S1.2 (syntax universe + grammar capability law),
S2.1-S2.4 (contexts and universes), S3.3, S11; identity-and-evidence.md S3
(x-opensip-digest-domains.domainSets, languageVersionBinding, scopeCapabilityLaw).

Entry points named by the registry: admit_native_context, bind_typescript_universe,
bind_rust_universe, bind_syntax_universe.
"""
from __future__ import annotations

import hashlib
import unicodedata

import canon as K
import kit
from store import Refusal, split_id

CONTEXT_DOMAINS = set(kit.DOMAIN_SETS["native-context"])
UNIVERSE_DOMAINS = set(kit.DOMAIN_SETS["native-semantic-universe"])
NESTED_DOMAINS = set(kit.DOMAIN_SETS["native-nested"])

UNICODE_CASE_DATA_VERSION = unicodedata.unidata_version


def lib_name_fold(name: str) -> str:
    """Unicode Default Case Conversion toLowercase(X): full, non-tailored,
    context-sensitive.  NOT Simple_Lowercase_Mapping and NOT Case_Folding
    (native S2.4 discriminator table)."""
    return name.lower()


def lib_component(name: str) -> str:
    return "lib." + lib_name_fold(name) + ".d.ts"


def _basename(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def _closure(store, closure_id: str, expect_kind: str, where: str):
    """Fetch a retained closure2, recompute its identity, check its kind."""
    hexd = split_id(closure_id, "closure2")
    if not store.has_blob(hexd):
        raise Refusal("native.native-context-closure-unretained", f"{where} {closure_id}")
    domain, desc = store.load_frame(hexd, {"closure"}, where)
    kit.validate("identity", "#/$defs/closure", desc, where)
    if K.H("closure", desc) != hexd:
        raise Refusal("native.native-context-closure-identity-mismatch", where)
    if desc["kind"] != expect_kind:
        raise Refusal("native.native-context-closure-kind-mismatch",
                      f"{where}: {desc['kind']} != {expect_kind}")
    return desc


def _tree_digests(closure_desc):
    return {row["sha256"] for row in closure_desc["tree"]}


# ---------------------------------------------------------------------------
# admit_native_context
# ---------------------------------------------------------------------------

def admit_native_context(store, domain: str, ctx: dict, snapshot_inventory=None):
    """Re-decide the owning contract's own admission over retained bytes.

    Returns an "admission" record: {domain, contextId, closures}.
    """
    if domain not in CONTEXT_DOMAINS:
        raise Refusal("NATIVE_CONTEXT_DOMAIN_UNREGISTERED", domain)
    row = kit.DOMAIN_SETS["native-context"][domain]
    kit.validate("native", row["selector"], ctx, f"native-context {domain}")
    inv = {b["path"]: b for b in (snapshot_inventory or [])}

    if domain == "native.context.typescript.v2":
        _admit_ts_context(store, ctx, inv)
    elif domain == "native.context.rust.v2":
        _admit_rust_context(store, ctx, inv)
    elif domain == "native.context.syntax.v2":
        _admit_syntax_context(store, ctx)
    else:  # pragma: no cover - closed set
        raise Refusal("NATIVE_CONTEXT_DOMAIN_UNREGISTERED", domain)

    return {"domain": domain, "language": row["language"],
            "contextId": "sha256:" + K.H(domain, ctx), "context": ctx}


def _admit_ts_context(store, ctx, inv):
    tool = _closure(store, ctx["toolClosure"]["closureId"], "toolchain", "ts.toolClosure")
    tc = ctx["toolchain"]
    if tc["compilerVersion"] != tool["semanticVersion"]:
        raise Refusal("native.native-context-compiler-version-not-from-manifest",
                      f"{tc['compilerVersion']} != {tool['semanticVersion']}")
    members = _tree_digests(tool)
    for field in ("compiler", "runtime"):
        if ctx["toolClosure"][field] not in members:
            raise Refusal("native.native-context-tool-not-in-closure", field)
    if tc["compilerPackageDigest"] not in members:
        raise Refusal("native.native-context-tool-not-in-closure", "compilerPackageDigest")

    stdlib = _closure(store, "closure2:" + tc["typescriptStdlibMerkleRoot"],
                      "stdlib", "ts.stdlib")
    # complete .d.ts inventory of the retained stdlib tree, keyed by basename
    by_base: dict[str, list] = {}
    for rowb in stdlib["tree"]:
        if rowb["path"].endswith(".d.ts"):
            by_base.setdefault(_basename(rowb["path"]), []).append(rowb)
    for base, rows in by_base.items():
        if len(rows) > 1:
            raise Refusal("native.native-context-stdlib-tree-ambiguous-basename", base)
    declared = {r["component"]: r["sha256"] for r in tc["standardLibraryComponentDigests"]}
    for base, rows in by_base.items():
        if base not in declared:
            raise Refusal("native.native-context-stdlib-inventory-incomplete", base)
        if declared[base] != rows[0]["sha256"]:
            raise Refusal("native.native-context-stdlib-tree-mismatch", base)
    for base in declared:
        if base not in by_base:
            raise Refusal("native.native-context-stdlib-tree-mismatch",
                          f"declared component {base} is not in the retained tree")

    honored = ctx["configProjection"]["honoredOptions"]
    folds = [lib_name_fold(n) for n in tc["libSelection"]]
    if len(set(folds)) != len(folds):
        raise Refusal("native.native-context-field-mismatch", "duplicate-lib-selection")
    for n in tc["libSelection"]:
        if lib_component(n) not in declared:
            raise Refusal("native.native-context-lib-not-retained", n)
    if set(folds) != {lib_name_fold(m) for m in honored["lib"]}:
        raise Refusal("native.native-context-field-mismatch", "libSelection")
    if tc["libSelection"] != sorted(tc["libSelection"], key=lambda s: s.encode("utf-8")):
        raise Refusal("native.native-context-field-mismatch", "libSelection-order")
    comps = [r["component"] for r in tc["standardLibraryComponentDigests"]]
    if comps != sorted(comps, key=lambda s: s.encode("utf-8")) or len(set(comps)) != len(comps):
        raise Refusal("native.native-context-field-mismatch",
                      "standardLibraryComponentDigests-order")

    if ctx["moduleResolutionMode"] != honored["moduleResolution"]:
        raise Refusal("native.native-context-field-mismatch", "moduleResolutionMode")

    # snapshotJoins from the registry row
    if inv:
        for p in ctx["configProjection"]["configGraphPaths"]:
            if p not in inv:
                raise Refusal("native.native-context-config-path-outside-snapshot", p)
        lf = ctx.get("lockfileIdentity")
        if lf is not None:
            if lf["path"] not in inv:
                raise Refusal("native.native-context-lockfile-outside-snapshot", lf["path"])
            if inv[lf["path"]]["sha256"] != lf["contentSha256"]:
                raise Refusal("native.native-context-lockfile-digest-mismatch", lf["path"])

    # nestedRecords: the node_modules layout is a required binding input when non-null
    nml = ctx["nodeModulesLayoutDigest"]
    if nml is not None:
        layout = store.get_record(nml, "native", "#/$defs/ResolvedNodeModulesLayoutV1",
                                  "nodeModulesLayout")
        for e in layout["entries"]:
            if not store.has_blob(e["contentSha256"]):
                raise Refusal("EVIDENCE_UNAVAILABLE",
                              f"node_modules manifest blob {e['installPath']}")
            rp = e["realPath"]
            if rp != e["installPath"] and rp not in {x["installPath"] for x in layout["entries"]}:
                raise Refusal("native.node-modules-realpath-not-an-installpath", rp)


def _admit_rust_context(store, ctx, inv):
    tool = _closure(store, ctx["toolClosure"]["closureId"], "toolchain", "rust.toolClosure")
    tc = ctx["toolchain"]
    if tc["rustcVersion"] != tool["semanticVersion"]:
        raise Refusal("native.native-context-compiler-version-not-from-manifest",
                      f"{tc['rustcVersion']} != {tool['semanticVersion']}")
    members = _tree_digests(tool)
    for field in ("rustc", "cargo", "procMacroServer", "linker", "ar"):
        v = ctx["toolClosure"][field]
        if v is not None and v not in members:
            raise Refusal("native.native-context-tool-not-in-closure", field)
    _closure(store, "closure2:" + tc["rustcDevLlvmDigest"], "rust-dev-llvm", "rust.devllvm")

    proj = ctx["configProjection"]
    if not store.has_blob(proj["projectionSha256"]):
        raise Refusal("EVIDENCE_UNAVAILABLE", "projected .cargo/config.toml bytes")
    if inv:
        for p in proj["replacedSnapshotConfigs"]:
            if p not in inv:
                raise Refusal("native.native-context-config-path-outside-snapshot", p)

    for field, domain in (("dependencySourceSetId", "native.dependency-source-set.v1"),
                          ("unifiedFeaturesId", "native.unified-features.rust.v1"),
                          ("preparedOutputSetId", "native.prepared-output-set.v3")):
        val = ctx[field]
        if val is None:
            continue
        hexd = split_id(val, "sha256")
        dom, payload = store.load_frame(hexd, NESTED_DOMAINS, field)
        if dom != domain:
            raise Refusal("NATIVE_NESTED_DOMAIN_MISMATCH", f"{field}: {dom}")
        srow = kit.DOMAIN_SETS["native-nested"][dom]
        kit.validate("native", srow["selector"], payload, field)
        if K.H(dom, payload) != hexd:
            raise Refusal("NATIVE_NESTED_IDENTITY_MISMATCH", field)
        if dom == "native.dependency-source-set.v1":
            _admit_dependency_set(store, payload)


def _admit_dependency_set(store, dss):
    """The nested chain continues to raw bytes (identity S3)."""
    for pkg in dss["packages"]:
        fm_hex = pkg["fileManifestSha256"]
        dom, manifest = store.load_frame(fm_hex, NESTED_DOMAINS,
                                         f"fileManifest {pkg['name']}")
        if dom != "native.dependency-file-manifest.v1":
            raise Refusal("NATIVE_NESTED_DOMAIN_MISMATCH", dom)
        kit.validate("native", "#/$defs/DependencyFileManifestV1", manifest,
                     f"fileManifest {pkg['name']}")
        if K.H(dom, manifest) != fm_hex:
            raise Refusal("NATIVE_NESTED_IDENTITY_MISMATCH", "fileManifestSha256")
        total = 0
        for row in manifest:
            blob = store.get_blob(row["contentSha256"])
            if len(blob) != row["byteLength"]:
                raise Refusal("DEPENDENCY_MEMBER_LENGTH_MISMATCH", row["path"])
            total += row["byteLength"]
        if pkg["fileCount"] != len(manifest):
            raise Refusal("DEPENDENCY_FILE_COUNT_MISMATCH", pkg["name"])
        if pkg["totalBytes"] != total:
            raise Refusal("DEPENDENCY_TOTAL_BYTES_MISMATCH", pkg["name"])
        if pkg["checksumVerification"] == "mismatch":
            raise Refusal("native.dependency-source-checksum-mismatch", pkg["name"])


def _admit_syntax_context(store, ctx):
    bundle = ctx["grammarBundle"]
    cl = _closure(store, bundle["closureId"], "grammar", "syntax.grammarBundle")
    if bundle["parserVersion"] != cl["semanticVersion"]:
        raise Refusal("native.syntax-grammar-version-not-from-manifest",
                      f"{bundle['parserVersion']} != {cl['semanticVersion']}")
    members = _tree_digests(cl)
    # "every grammar definition, the bundle manifest and the normalizer
    #  specification present in the retained tree"
    if bundle["bundleDigest"] not in members:
        raise Refusal("native.syntax-grammar-bundle-not-in-closure", "bundleDigest")
    if bundle["normalizer"]["specificationDigest"] not in members:
        raise Refusal("native.syntax-grammar-bundle-not-in-closure", "normalizer")
    seen_suffix = {}
    for g in bundle["grammars"]:
        if g["grammarDigest"] not in members:
            raise Refusal("native.syntax-grammar-bundle-not-in-closure", g["grammarId"])
        reg = kit.GRAMMAR_CAPS["languages"].get(g["languageId"])
        if reg is None:
            raise Refusal("native.syntax-grammar-language-unregistered", g["languageId"])
        if g["syntaxClass"] != reg["syntaxClass"]:
            raise Refusal("native.syntax-grammar-class-contradicts-registry",
                          f"{g['languageId']}:{g['syntaxClass']}")
        for suf in g["suffixes"]:
            if suf not in reg["suffixes"]:
                raise Refusal("native.syntax-grammar-suffix-not-of-language",
                              f"{g['languageId']}:{suf}")
            if suf in seen_suffix:
                raise Refusal("native.syntax-grammar-suffix-ambiguous", suf)
            seen_suffix[suf] = g["grammarId"]


# ---------------------------------------------------------------------------
# universe bindings
# ---------------------------------------------------------------------------

def bind_universe(store, domain: str, universe: dict, admission: dict | None,
                  context: dict | None, retained: dict | None,
                  snapshot_inventory=None):
    if domain not in UNIVERSE_DOMAINS:
        raise Refusal("NATIVE_UNIVERSE_DOMAIN_UNREGISTERED", domain)
    row = kit.DOMAIN_SETS["native-semantic-universe"][domain]
    if "binding" not in row:
        raise Refusal("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", domain)
    kit.validate("native", row["selector"], universe, f"universe {domain}")
    if context is None:
        raise Refusal("native.universe-context-not-supplied", domain)
    if admission is None:
        raise Refusal("native.universe-retained-inputs-not-supplied", domain)
    # "a universe must bind a context of its OWN language"
    if admission["domain"] != row["contextDomain"]:
        raise Refusal("native.native-context-language-mismatch",
                      f"{admission['domain']} for {domain}")
    ctx_hex = K.H(row["contextDomain"], context)
    if universe["nativeContextId"] != "sha256:" + ctx_hex:
        raise Refusal("native.universe-context-binding-mismatch",
                      "context-bytes-are-not-the-admitted-ones")
    if admission["contextId"] != universe["nativeContextId"]:
        raise Refusal("native.universe-context-binding-mismatch", domain)

    if domain == "native.semantic-universe.typescript.v2":
        _bind_ts(store, universe, context, snapshot_inventory)
    elif domain == "native.semantic-universe.rust.v2":
        _bind_rust(store, universe, context, retained or {}, snapshot_inventory)
    elif domain == "native.semantic-universe.syntax.v2":
        _bind_syntax(universe, context)
    return "sha256:" + K.H(domain, universe)


def config_node_kind(path: str) -> str:
    """native S2.2 / x-opensip-config-node-kind-law: exact, case-sensitive
    basename table; every other basename -> other."""
    base = _basename(path)
    if base == "tsconfig.json":
        return "tsconfig"
    if base == "jsconfig.json":
        return "jsconfig"
    return "other"


def _bind_ts(store, u, ctx, inventory):
    inv = {b["path"]: b for b in (inventory or [])}
    graph = store.get_record(u["tsconfigGraphHash"], "native",
                             "#/$defs/TypeScriptConfigGraphV1", "tsconfigGraph")
    node_paths = [n["path"] for n in graph["nodes"]]
    if set(node_paths) != set(ctx["configProjection"]["configGraphPaths"]):
        raise Refusal("native.universe-context-field-mismatch", "configGraphPaths")
    for n in graph["nodes"]:
        if config_node_kind(n["path"]) != n["kind"]:
            raise Refusal("native.config-graph-kind-contradicts-path", n["path"])
        if inv and n["path"] not in inv:
            raise Refusal("native.config-graph-path-outside-snapshot", n["path"])
        if inv and inv[n["path"]]["sha256"] != n["contentSha256"]:
            raise Refusal("native.config-graph-digest-mismatch", n["path"])
        for e in n["extendsResolved"]:
            if e not in set(node_paths):
                raise Refusal("native.config-graph-edge-names-no-node", e)
    entry = graph["entryConfigPath"]
    if entry is None:
        derived = "synthesized"
        if graph["nodes"]:
            raise Refusal("native.config-graph-synthesized-with-nodes", "")
    else:
        if entry not in set(node_paths):
            raise Refusal("native.config-graph-entry-not-a-node", entry)
        k = config_node_kind(entry)
        derived = "jsconfig" if k == "jsconfig" else "tsconfig"
        # reachability from the entry + acyclicity
        seen, stack = set(), [entry]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            node = next(n for n in graph["nodes"] if n["path"] == cur)
            stack.extend(node["extendsResolved"])
        if seen != set(node_paths):
            raise Refusal("native.config-graph-node-unreachable",
                          ",".join(sorted(set(node_paths) - seen)))
        _acyclic(graph)
    if u["configOrigin"] != derived:
        raise Refusal("native.universe-context-field-mismatch", "configOrigin")

    for field in ("languageMode", "packageModuleType"):
        if u[field] != ctx[field]:
            raise Refusal("native.universe-context-field-mismatch", field)
    honored = ctx["configProjection"]["honoredOptions"]
    for uf, cf in (("allowJs", "allowJs"), ("checkJs", "checkJs")):
        if u[uf] != honored[cf]:
            raise Refusal("native.universe-context-field-mismatch", uf)
    if u["jsAdmittedToProgram"] != honored["allowJs"]:
        raise Refusal("native.universe-context-field-mismatch", "jsAdmittedToProgram")
    if u["jsDiagnosticsEnabled"] != honored["checkJs"]:
        raise Refusal("native.universe-context-field-mismatch", "jsDiagnosticsEnabled")
    lk = "none" if ctx["lockfileIdentity"] is None else ctx["lockfileIdentity"]["kind"]
    if u["lockfileKind"] != lk:
        raise Refusal("native.universe-context-field-mismatch", "lockfileKind")
    if u["nodeModulesInReadSet"] != (ctx["nodeModulesLayoutDigest"] is not None):
        raise Refusal("native.universe-context-field-mismatch", "nodeModulesInReadSet")
    empty_graph = not ctx["configProjection"]["configGraphPaths"]
    if (u["configOrigin"] == "synthesized") != empty_graph:
        raise Refusal("native.universe-context-field-mismatch", "extends-graph-emptiness")
    if (u["synthesizedOptions"] is not None) != (u["configOrigin"] == "synthesized"):
        raise Refusal("native.universe-context-field-mismatch", "synthesized-options-presence")
    if u["synthesizedOptions"] is not None:
        so = u["synthesizedOptions"]
        for k, v in so.items():
            if k == "types":
                if honored["types"] != v:
                    raise Refusal("native.universe-context-field-mismatch", "synth:types")
            elif honored.get(k) != v:
                raise Refusal("native.universe-context-field-mismatch", f"synth:{k}")
        if "jsx" not in so and honored["jsx"] is not None:
            raise Refusal("native.universe-context-field-mismatch", "synth:jsx-absent")
    if inv:
        for p in u["programRootFiles"] + u["jsRootFiles"]:
            if p not in inv:
                raise Refusal("native.program-root-outside-snapshot", p)


def _acyclic(graph):
    edges = {n["path"]: list(n["extendsResolved"]) for n in graph["nodes"]}
    state = {}

    def visit(p):
        st = state.get(p)
        if st == 1:
            raise Refusal("native.config-graph-cyclic", p)
        if st == 2:
            return
        state[p] = 1
        for q in edges.get(p, []):
            visit(q)
        state[p] = 2

    for p in edges:
        visit(p)


def _bind_rust(store, u, ctx, retained, inventory):
    inv = {b["path"]: b for b in (inventory or [])}
    for field in ("dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"):
        if u[field] != ctx[field]:
            raise Refusal("native.universe-context-field-mismatch", field)
    if u["rustflags"] != ctx["configProjection"]["rustflags"]:
        raise Refusal("native.universe-context-field-mismatch", "rustflags")
    proj_hex = K.H("native.cargo-config-projection.v2", ctx["configProjection"])
    if u["configProjectionSha256"] != proj_hex:
        raise Refusal("native.universe-context-field-mismatch", "configProjectionSha256")
    if u["executionCapableResolution"] != (u["preparedResolution"] != "none"):
        raise Refusal("native.universe-context-field-mismatch", "executionCapableResolution")
    if (u["preparedOutputSetId"] is None) != (u["preparedResolution"] == "none"):
        raise Refusal("native.universe-context-field-mismatch", "preparedResolution")
    base = set(ctx["baseCfg"])
    ids = set()
    for cs in u["cfgSets"]:
        if not base <= set(cs["cfg"]):
            raise Refusal("native.universe-cfgset-drops-base-cfg", cs["cfgSetId"])
        if cs["cfgSetId"] in ids:
            raise Refusal("native.universe-cfgset-duplicate-id", cs["cfgSetId"])
        ids.add(cs["cfgSetId"])
    if inv:
        for p in u["crateRootPaths"]:
            if p not in inv:
                raise Refusal("native.crate-root-outside-snapshot", p)
        lf = u["lockfileIdentity"]
        if lf["path"] not in inv:
            raise Refusal("native.lockfile-outside-snapshot", lf["path"])
        if inv[lf["path"]]["sha256"] != lf["contentSha256"]:
            raise Refusal("native.lockfile-digest-mismatch", lf["path"])
    dss = retained.get("dependencySourceSet")
    if dss is not None and dss["lockfileIdentity"] != u["lockfileIdentity"]:
        raise Refusal("native.dependency-set-lockfile-mismatch", "")
    uf = retained.get("unifiedFeatures")
    if uf is not None:
        if uf["targetTriple"] != ctx["targetTriple"]:
            raise Refusal("native.unified-features-target-mismatch", uf["targetTriple"])
        if uf["resolverVersion"] != ctx["resolverVersion"]:
            raise Refusal("native.unified-features-resolver-mismatch", "")
    sou_id = u["sourceUnitOwnershipId"]
    if sou_id is not None:
        hexd = split_id(sou_id, "sha256")
        dom, payload = store.load_frame(hexd, NESTED_DOMAINS, "sourceUnitOwnership")
        if dom != "native.source-unit-ownership.v1":
            raise Refusal("NATIVE_NESTED_DOMAIN_MISMATCH", dom)
        kit.validate("native", "#/$defs/SourceUnitOwnershipV1", payload, "sourceUnitOwnership")
        if K.H(dom, payload) != hexd:
            raise Refusal("NATIVE_NESTED_IDENTITY_MISMATCH", "sourceUnitOwnershipId")
        admit_source_unit_ownership(payload, u["edition"], inv)


def admit_source_unit_ownership(sou, edition_map, inv):
    """native S11: unitId is DERIVED; selection/ownership must name declared
    units; markers and owned paths must be snapshot sources; a deferring unit
    must name a crate the same edition map declares."""
    declared = {}
    for unit in sou["units"]:
        preimage = {"schemaVersion": 1, "markerPath": unit["markerPath"],
                    "targetKind": unit["targetKind"], "targetName": unit["targetName"]}
        expect = "sha256:" + K.H("native.compilation-unit.v1", preimage)
        if unit["unitId"] != expect:
            raise Refusal("native.compilation-unit-id-not-derived", unit["unitId"])
        if unit["unitId"] in declared:
            raise Refusal("native.compilation-unit-duplicate", unit["unitId"])
        declared[unit["unitId"]] = unit
        if inv and unit["markerPath"] not in inv:
            raise Refusal("native.compilation-unit-marker-outside-snapshot",
                          unit["markerPath"])
        if unit["targetEdition"] is None and unit["crateName"] not in edition_map:
            raise Refusal("native.compilation-unit-crate-not-in-edition-map",
                          unit["crateName"])
    for uid in sou["selectedUnitIds"]:
        if uid not in declared:
            raise Refusal("native.selection-names-undeclared-unit", uid)
    for own in sou["ownership"]:
        if own["unitId"] not in declared:
            raise Refusal("native.ownership-names-undeclared-unit", own["unitId"])
        if inv and own["path"] not in inv:
            raise Refusal("native.ownership-path-outside-snapshot", own["path"])
    return declared


def _bind_syntax(u, ctx):
    have = {g["grammarId"] for g in ctx["grammarBundle"]["grammars"]}
    for gid in u["selectedGrammarIds"]:
        if gid not in have:
            raise Refusal("native.syntax-grammar-not-in-bundle", gid)


# ---------------------------------------------------------------------------
# body-language-version: DERIVED, recomputed by closure (identity S3).
# ---------------------------------------------------------------------------

def _longest_suffix(table, path):
    best = None
    for suf in table:
        if path.endswith(suf) and (best is None or len(suf) > len(best)):
            best = suf
    return best


def derive_body_language_version(universe_domain, universe, context, anchor_path,
                                 retained=None):
    """Rebuild the closed body-language-version record from the registry row's
    languageVersionBinding.  Returns (record, languageId)."""
    row = kit.DOMAIN_SETS["native-semantic-universe"][universe_domain]
    lvb = row.get("languageVersionBinding")
    if lvb is None:
        raise Refusal("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", universe_domain)
    fields = {}
    for name, spec in lvb["fields"].items():
        if "const" in spec:
            fields[name] = spec["const"]
        elif spec.get("source") == "native-context":
            node = context
            for part in spec["path"]:
                node = node[part]
            fields[name] = node
        else:
            raise Refusal("BODY_LANGUAGE_FIELD_SOURCE_UNKNOWN", name)

    d = lvb["dialect"]
    if d["form"] == "closed-suffix-table":
        suf = _longest_suffix(d["table"], anchor_path)
        if suf is None:
            raise Refusal(d["onUnknown"], anchor_path)
        variant = d["table"][suf]
        dialect = {d["key"]: variant}
        language_id = lvb["bodyLanguageByVariant"][variant]
    elif d["form"] == "selected-compilation-target-edition":
        dialect, language_id = _rust_dialect(d, universe, anchor_path, retained or {}, lvb)
    else:
        raise Refusal("BODY_LANGUAGE_DIALECT_FORM_UNKNOWN", d["form"])

    rec = {"schemaVersion": 1, "languageId": language_id,
           "compilerName": fields["compilerName"],
           "compilerVersion": fields["compilerVersion"],
           "compilerBuild": fields["compilerBuild"],
           "dialect": dialect}
    kit.validate("identity", "#/$defs/body-language-version", rec, "body-language-version")
    return rec, language_id


def _rust_dialect(d, universe, anchor_path, retained, lvb):
    own = d["ownership"]
    sou = retained.get("sourceUnitOwnership")
    # (1) no committed ownership refuses
    if universe.get("sourceUnitOwnershipId") is None or sou is None:
        raise Refusal(d["onOwnershipMissing"], anchor_path)
    # (2) partial enumeration refuses BEFORE any row is read
    if sou[own["enumerationField"]] == "partial":
        raise Refusal(d["onOwnerUnenumerated"], anchor_path)
    units = {u["unitId"]: u for u in sou[own["unitsField"]]}
    # (3) rows whose path EQUALS the anchor path
    owners = [r[own["unitField"]] for r in sou["ownership"]
              if r[own["pathField"]] == anchor_path]
    if not owners:
        raise Refusal(d["onOwnerNotCompiled"], anchor_path)
    # (4) restrict to the explicit selection
    selected = [uid for uid in owners if uid in set(sou[own["selectionField"]])]
    if not selected:
        raise Refusal(d["onOwnerNotSelected"], anchor_path)
    # effective edition = target edition, else the universe edition map entry
    eds = set()
    for uid in selected:
        u = units[uid]
        te = u[own["targetEditionField"]]
        if te is None:
            crate = u[own["crateField"]]
            if crate not in universe["edition"]:
                raise Refusal(d["onEmpty"], crate)
            te = universe["edition"][crate]
        eds.add(te)
    if len(eds) > 1:
        raise Refusal(d["onOwnerAmbiguous"], f"{anchor_path}: {sorted(eds)}")
    return {d["key"]: eds.pop()}, lvb["bodyLanguage"]


def language_version_raw32(record) -> bytes:
    """raw 32 bytes of SHA-256(C(body-language-version))."""
    return hashlib.sha256(K.C(record)).digest()
