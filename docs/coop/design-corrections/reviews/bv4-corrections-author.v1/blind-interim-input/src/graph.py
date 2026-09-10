"""Descriptor-graph builders reconstructed from the five contracts.

Everything here is derived from prose + the kit's normative schemas/registries.
Every trusted observation (file bytes, compiler identity, provider enumeration,
OS custody) is a SYNTHETIC ASSUMPTION and is labelled as such: it is never
native enforcement proof.
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import osip  # noqa: E402

PROJECT_ID = "prj1-" + hashlib.sha256(b"blind-consumer-b.v4/project").hexdigest()


class Refusal(Exception):
    def __init__(self, cause, detail=""):
        super().__init__("%s%s" % (cause, (": " + detail) if detail else ""))
        self.cause = cause
        self.detail = detail


class Store:
    """One content-addressed store keyed by raw SHA-256.

    It retains raw artifacts, canonical records and H preimage frames alike,
    exactly as identity section 3's closing digest law says one store can.
    """

    def __init__(self):
        self.objects = {}
        self.kinds = {}

    def put_blob(self, data):
        d = osip.raw_sha256(data)
        self.objects[d] = data
        self.kinds.setdefault(d, "raw-artifact")
        return d

    def put_record(self, record):
        b = osip.c_encode(record)
        d = osip.raw_sha256(b)
        self.objects[d] = b
        self.kinds.setdefault(d, "canonical-record")
        return d

    def put_frame(self, domain, descriptor):
        frame = osip.h_frame(domain, descriptor)
        d = osip.raw_sha256(frame)
        self.objects[d] = frame
        self.kinds[d] = "h-identity"
        return d

    def get(self, digest):
        if digest not in self.objects:
            raise Refusal("EvidenceUnavailable",
                          "evidence.missing %s (HOST.IO_FAILURE/host-io, exit 4)" % digest)
        return self.objects[digest]

    def rehash(self, digest):
        return osip.raw_sha256(self.get(digest)) == digest


# --------------------------------------------------------------------------
# closures
# --------------------------------------------------------------------------

def make_closure(store, kind, files, semantic_version, protocol_major, platform,
                 manifest_body=None):
    """files: {path: bytes}. Tree hashing includes relative path, length, digest."""
    tree = []
    for p in sorted(files):
        data = files[p]
        tree.append({"path": p, "sha256": store.put_blob(data), "bytes": len(data)})
    osip.check_order(tree, "path")
    if manifest_body is None:
        manifest_body = ("component-manifest:%s:%s:%s" % (kind, semantic_version, platform)
                         ).encode("utf-8")
    desc = {
        "schemaVersion": 2,
        "kind": kind,
        "manifestDigest": store.put_blob(manifest_body),
        "tree": tree,
        "semanticVersion": semantic_version,
        "protocolMajor": protocol_major,
        "platform": platform,
    }
    kit.validate("identity", "#/$defs/closure", desc)
    d = store.put_frame("closure", desc)
    return {"id": "closure2:" + d, "hex": d, "descriptor": desc,
            "members": {r["path"]: r["sha256"] for r in tree}}


# --------------------------------------------------------------------------
# snapshot
# --------------------------------------------------------------------------

def make_snapshot(store, files, scope, config, vcs_kind="git", commit=None, dirty=False):
    inventory = []
    for p in sorted(files):
        data = files[p]
        inventory.append({"path": p, "sha256": store.put_blob(data), "bytes": len(data)})
    osip.check_order(inventory, "path")
    kit.validate("identity", "#/$defs/source-inventory", inventory)
    inv_digest = store.put_record(inventory)

    kit.validate("identity", "#/$defs/scope-descriptor", scope)
    scope_digest = store.put_record(scope)
    kit.validate("identity", "#/$defs/semantic-configuration", config)
    config_digest = store.put_record(config)

    vcs = {"schemaVersion": 2, "kind": vcs_kind,
           "commitId": commit if vcs_kind != "none" else None,
           "dirty": dirty, "sourceInventoryDigest": inv_digest}
    kit.validate("identity", "#/$defs/vcs-observation", vcs)
    vcs_digest = store.put_record(vcs)

    desc = {"schemaVersion": 2, "projectId": PROJECT_ID, "sourceInventory": inventory,
            "resolvedConfigDigest": config_digest, "scopeDigest": scope_digest,
            "vcsDigest": vcs_digest}
    kit.validate("identity", "#/$defs/snapshot", desc)
    d = store.put_frame("snapshot", desc)
    return {"id": "snapshot2:" + d, "hex": d, "descriptor": desc,
            "inventory": {r["path"]: r for r in inventory},
            "bytes": dict(files),
            "scopeDigest": scope_digest, "configDigest": config_digest,
            "vcsDigest": vcs_digest, "inventoryDigest": inv_digest, "scope": scope,
            "config": config}


# --------------------------------------------------------------------------
# native contexts and universes
# --------------------------------------------------------------------------

TS_CONTEXT_DOMAIN = "native.context.typescript.v2"
RS_CONTEXT_DOMAIN = "native.context.rust.v2"
SX_CONTEXT_DOMAIN = "native.context.syntax.v2"
TS_UNIVERSE_DOMAIN = "native.semantic-universe.typescript.v2"
RS_UNIVERSE_DOMAIN = "native.semantic-universe.rust.v2"
SX_UNIVERSE_DOMAIN = "native.semantic-universe.syntax.v2"

CONTEXT_DOMAINS = {TS_CONTEXT_DOMAIN, RS_CONTEXT_DOMAIN, SX_CONTEXT_DOMAIN}
UNIVERSE_DOMAINS = {TS_UNIVERSE_DOMAIN, RS_UNIVERSE_DOMAIN, SX_UNIVERSE_DOMAIN}

CONTEXT_SELECTOR = {
    TS_CONTEXT_DOMAIN: "#/$defs/TypeScriptNativeContextV2",
    RS_CONTEXT_DOMAIN: "#/$defs/NativeContextV2",
    SX_CONTEXT_DOMAIN: "#/$defs/SyntaxNativeContextV2",
}
UNIVERSE_SELECTOR = {
    TS_UNIVERSE_DOMAIN: "#/$defs/TypeScriptUniverseV2ResolvedInputs",
    RS_UNIVERSE_DOMAIN: "#/$defs/RustUniverseV2ResolvedInputs",
    SX_UNIVERSE_DOMAIN: "#/$defs/SyntaxUniverseV2ResolvedInputs",
}
UNIVERSE_CONTEXT_DOMAIN = {
    TS_UNIVERSE_DOMAIN: TS_CONTEXT_DOMAIN,
    RS_UNIVERSE_DOMAIN: RS_CONTEXT_DOMAIN,
    SX_UNIVERSE_DOMAIN: SX_CONTEXT_DOMAIN,
}


def mint_context(store, domain, descriptor):
    kit.validate("native", CONTEXT_SELECTOR[domain], descriptor)
    d = store.put_frame(domain, descriptor)
    return {"domain": domain, "hex": d, "sha256text": "sha256:" + d,
            "descriptor": descriptor}


def mint_universe(store, domain, descriptor):
    kit.validate("native", UNIVERSE_SELECTOR[domain], descriptor)
    d = store.put_frame(domain, descriptor)
    return {"domain": domain, "hex": d, "sha256text": "sha256:" + d,
            "descriptor": descriptor}


# --- admit_native_context (my reconstruction of native 2.3/2.4/1.2/14) ----

def admit_native_context(store, ctx, closures, snapshot, retained=None):
    """Re-decided over retained descriptors alone. Nothing is re-executed."""
    dom = ctx["domain"]
    D = ctx["descriptor"]
    retained = retained or {}

    def closure_by_hex(h, kind, causeprefix):
        c = closures.get(h)
        if c is None:
            raise Refusal("native.native-context-closure-unretained", h)
        if osip.raw_sha256(osip.h_frame("closure", c["descriptor"])) != h:
            raise Refusal("native.native-context-closure-identity-mismatch", h)
        if c["descriptor"]["kind"] != kind:
            raise Refusal("native.native-context-closure-kind-mismatch",
                          "%s wanted %s got %s" % (causeprefix, kind, c["descriptor"]["kind"]))
        return c

    if dom == TS_CONTEXT_DOMAIN:
        tool = closure_by_hex(D["toolClosure"]["closureId"].split(":")[1], "toolchain", "toolClosure")
        std = closure_by_hex(D["toolchain"]["typescriptStdlibMerkleRoot"], "stdlib",
                             "typescriptStdlibMerkleRoot")
        if D["toolchain"]["compilerVersion"] != tool["descriptor"]["semanticVersion"]:
            raise Refusal("native.native-context-compiler-version-not-from-manifest",
                          D["toolchain"]["compilerVersion"])
        for k in ("compiler", "runtime"):
            if D["toolClosure"][k] not in tool["members"].values():
                raise Refusal("native.native-context-tool-not-in-closure", k)
        if D["toolchain"]["compilerPackageDigest"] not in tool["members"].values():
            raise Refusal("native.native-context-tool-not-in-closure", "compilerPackageDigest")
        # complete .d.ts inventory of the retained stdlib tree, one row per member
        dts = [r for r in std["descriptor"]["tree"] if r["path"].endswith(".d.ts")]
        base = {}
        for r in dts:
            b = os.path.basename(r["path"])
            if b in base:
                raise Refusal("native.native-context-stdlib-tree-ambiguous-basename", b)
            base[b] = r["sha256"]
        got = {c["component"]: c["sha256"] for c in D["toolchain"]["standardLibraryComponentDigests"]}
        for b, sha in base.items():
            if b not in got:
                raise Refusal("native.native-context-stdlib-inventory-incomplete", b)
            if got[b] != sha:
                raise Refusal("native.native-context-stdlib-tree-mismatch", b)
        for b in got:
            if b not in base:
                raise Refusal("native.native-context-stdlib-tree-mismatch", b)
        libsel = D["toolchain"]["libSelection"]
        osip.check_order(libsel, "utf8")
        if len({x.lower() for x in libsel}) != len(libsel):
            raise Refusal("native.native-context-lib-case-duplicate")
        if not libsel:
            raise Refusal("native.native-context-lib-selection-empty")
        for lib in libsel:
            if not any(b.lower().startswith(("lib." + lib + ".").lower()) or
                       b.lower() == ("lib." + lib + ".d.ts").lower() for b in base):
                raise Refusal("native.native-context-lib-not-retained", lib)
        honored_lib = D["configProjection"]["honoredOptions"]["lib"]
        if {x.lower() for x in honored_lib} != {x.lower() for x in libsel}:
            raise Refusal("native.native-context-lib-selection-disagrees-with-honored")
        if D["moduleResolutionMode"] != D["configProjection"]["honoredOptions"]["moduleResolution"]:
            raise Refusal("native.native-context-module-resolution-mismatch")
        for p in D["configProjection"]["configGraphPaths"]:
            if p not in snapshot["inventory"]:
                raise Refusal("native.native-context-config-graph-path-outside-snapshot", p)
        lf = D["lockfileIdentity"]
        if lf is not None:
            row = snapshot["inventory"].get(lf["path"])
            if row is None or row["sha256"] != lf["contentSha256"]:
                raise Refusal("native.native-context-lockfile-outside-snapshot", lf["path"])
        if D["nodeModulesLayoutDigest"] is not None:
            layout = retained.get("nodeModulesLayout")
            if layout is None:
                raise Refusal("native.universe-retained-inputs-not-supplied", "nodeModulesLayout")
            if osip.canonical_record_digest(layout) != D["nodeModulesLayoutDigest"]:
                raise Refusal("native.native-context-node-modules-layout-mismatch")
            kit.validate("native", "#/$defs/ResolvedNodeModulesLayoutV1", layout)
            osip.check_order(layout["entries"], {"by": ["installPath"]})
            paths = {e["installPath"] for e in layout["entries"]}
            for e in layout["entries"]:
                if e["realPath"] != e["installPath"] and e["realPath"] not in paths:
                    raise Refusal("native.node-modules-real-path-not-in-layout", e["realPath"])
                store.get(e["contentSha256"])      # retained-byte custody
        return {"language": "typescript", "admitted": True}

    if dom == RS_CONTEXT_DOMAIN:
        tool = closure_by_hex(D["toolClosure"]["closureId"].split(":")[1], "toolchain", "toolClosure")
        closure_by_hex(D["toolchain"]["rustcDevLlvmDigest"], "rust-dev-llvm", "rustcDevLlvmDigest")
        if D["toolchain"]["rustcVersion"] != tool["descriptor"]["semanticVersion"]:
            raise Refusal("native.native-context-compiler-version-not-from-manifest",
                          D["toolchain"]["rustcVersion"])
        for k in ("rustc", "cargo", "procMacroServer"):
            if D["toolClosure"][k] not in tool["members"].values():
                raise Refusal("native.native-context-tool-not-in-closure", k)
        for k in ("linker", "ar"):
            v = D["toolClosure"][k]
            if v is not None and v not in tool["members"].values():
                raise Refusal("native.native-context-tool-not-in-closure", k)
        for p in D["configProjection"]["replacedSnapshotConfigs"]:
            if p not in snapshot["inventory"]:
                raise Refusal("native.native-context-config-outside-snapshot", p)
        store.get(D["configProjection"]["projectionSha256"])   # projected config file bytes
        for nested, key, dom2 in (("dependencySourceSet", "dependencySourceSetId",
                                   "native.dependency-source-set.v1"),
                                  ("unifiedFeatures", "unifiedFeaturesId",
                                   "native.unified-features.rust.v1"),
                                  ("preparedOutputSet", "preparedOutputSetId",
                                   "native.prepared-output-set.v3")):
            val = D[key]
            if val is None:
                continue
            rec = retained.get(nested)
            if rec is None:
                raise Refusal("native.universe-retained-inputs-not-supplied", nested)
            if "sha256:" + osip.H(dom2, rec) != val:
                raise Refusal("native.nested-identity-mismatch", nested)
        return {"language": "rust", "admitted": True}

    if dom == SX_CONTEXT_DOMAIN:
        gb = D["grammarBundle"]
        gc = closure_by_hex(gb["closureId"].split(":")[1], "grammar", "grammarBundle")
        if gb["parserVersion"] != gc["descriptor"]["semanticVersion"]:
            raise Refusal("native.syntax-grammar-version-not-from-manifest", gb["parserVersion"])
        osip.check_order(gb["grammars"], {"by": ["grammarId"]})
        reg = kit.doc("native")["x-opensip-grammar-capability-registry"]["languages"]
        seen_suffix = {}
        for g in gb["grammars"]:
            row = reg.get(g["languageId"])
            if row is None:
                raise Refusal("native.syntax-grammar-language-not-registered", g["languageId"])
            if g["syntaxClass"] != row["syntaxClass"]:
                raise Refusal("native.syntax-grammar-class-mismatch",
                              "%s declared %s, registry says %s"
                              % (g["languageId"], g["syntaxClass"], row["syntaxClass"]))
            for s in g["suffixes"]:
                if s not in row["suffixes"]:
                    raise Refusal("native.syntax-grammar-suffix-not-of-language",
                                  "%s / %s" % (g["languageId"], s))
                if s in seen_suffix:
                    raise Refusal("native.syntax-grammar-suffix-ambiguous", s)
                seen_suffix[s] = g["grammarId"]
            osip.check_order(g["suffixes"], "utf8")
            store.get(g["grammarDigest"])
        store.get(gb["bundleDigest"])
        store.get(gb["normalizer"]["specificationDigest"])
        return {"language": "syntax", "admitted": True}

    raise Refusal("native.native-context-language-mismatch", dom)


def bind_universe(store, universe, context, admission, snapshot, retained=None):
    """bind_typescript_universe / bind_rust_universe / bind_syntax_universe."""
    retained = retained or {}
    udom = universe["domain"]
    U = universe["descriptor"]
    if context is None:
        raise Refusal("native.universe-context-not-supplied")
    if context["domain"] != UNIVERSE_CONTEXT_DOMAIN[udom]:
        raise Refusal("native.native-context-language-mismatch",
                      "%s bound to %s" % (udom, context["domain"]))
    if U["nativeContextId"] != context["sha256text"]:
        raise Refusal("native.universe-context-binding-mismatch",
                      "context-bytes-are-not-the-admitted-ones")
    if osip.raw_sha256(osip.h_frame(context["domain"], context["descriptor"])) \
            != context["hex"]:
        raise Refusal("native.universe-context-binding-mismatch", "recomputed context differs")
    C = context["descriptor"]

    if udom == TS_UNIVERSE_DOMAIN:
        graph = retained.get("configGraph")
        if graph is None:
            raise Refusal("native.universe-retained-inputs-not-supplied", "configGraph")
        kit.validate("native", "#/$defs/TypeScriptConfigGraphV1", graph)
        if osip.canonical_record_digest(graph) != U["tsconfigGraphHash"]:
            raise Refusal("native.universe-config-graph-hash-mismatch")
        osip.check_order(graph["nodes"], {"by": ["path"]})
        node_paths = [n["path"] for n in graph["nodes"]]
        if sorted(node_paths) != sorted(C["configProjection"]["configGraphPaths"]):
            raise Refusal("native.universe-config-graph-paths-disagree-with-context")
        for n in graph["nodes"]:
            row = snapshot["inventory"].get(n["path"])
            if row is None or row["sha256"] != n["contentSha256"]:
                raise Refusal("native.universe-config-node-not-inventoried", n["path"])
            for e in n["extendsResolved"]:
                if e not in node_paths:
                    raise Refusal("native.universe-config-edge-not-a-node", e)
        # reachability from the selected entry + acyclicity
        entry = graph["entryConfigPath"]
        if entry is None:
            if graph["nodes"]:
                raise Refusal("native.universe-config-origin-not-derivable")
            derived_origin = "synthesized"
        else:
            if entry not in node_paths:
                raise Refusal("native.universe-config-entry-not-a-node", entry)
            seen, stack = set(), [entry]
            while stack:
                cur = stack.pop()
                if cur in seen:
                    continue
                seen.add(cur)
                node = next(n for n in graph["nodes"] if n["path"] == cur)
                stack.extend(node["extendsResolved"])
            if seen != set(node_paths):
                raise Refusal("native.universe-config-node-unreachable",
                              ",".join(sorted(set(node_paths) - seen)))
            _acyclic_check(graph)
            entry_kind = next(n["kind"] for n in graph["nodes"] if n["path"] == entry)
            # an explicitly selected custom-named configuration derives tsconfig
            derived_origin = "jsconfig" if entry_kind == "jsconfig" else "tsconfig"
        if U["configOrigin"] != derived_origin:
            raise Refusal("native.universe-context-field-mismatch", "configOrigin")
        for f in ("languageMode", "packageModuleType"):
            if U[f] != C[f]:
                raise Refusal("native.universe-context-field-mismatch", f)
        ho = C["configProjection"]["honoredOptions"]
        if U["allowJs"] != ho["allowJs"] or U["jsAdmittedToProgram"] != ho["allowJs"]:
            raise Refusal("native.universe-context-field-mismatch", "allowJs")
        if U["checkJs"] != ho["checkJs"] or U["jsDiagnosticsEnabled"] != ho["checkJs"]:
            raise Refusal("native.universe-context-field-mismatch", "checkJs")
        want_kind = "none" if C["lockfileIdentity"] is None else C["lockfileIdentity"]["kind"]
        if U["lockfileKind"] != want_kind:
            raise Refusal("native.universe-context-field-mismatch", "lockfileKind")
        if U["nodeModulesInReadSet"] != (C["nodeModulesLayoutDigest"] is not None):
            raise Refusal("native.universe-context-field-mismatch", "nodeModulesInReadSet")
        if (U["synthesizedOptions"] is not None) != (derived_origin == "synthesized"):
            raise Refusal("native.universe-context-field-mismatch", "synthesizedOptions")
        if U["synthesizedOptions"] is not None:
            for k, v in U["synthesizedOptions"].items():
                if k in ho and ho[k] != v:
                    raise Refusal("native.universe-context-field-mismatch",
                                  "synthesizedOptions." + k)
        return True

    if udom == RS_UNIVERSE_DOMAIN:
        for f in ("dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"):
            if U[f] != C[f]:
                raise Refusal("native.universe-context-field-mismatch", f)
        if U["rustflags"] != C["configProjection"]["rustflags"]:
            raise Refusal("native.universe-context-field-mismatch", "rustflags")
        want = osip.H("native.cargo-config-projection.v2", C["configProjection"])
        if U["configProjectionSha256"] != want:
            raise Refusal("native.universe-context-field-mismatch", "configProjectionSha256")
        if U["executionCapableResolution"] != (U["preparedResolution"] != "none"):
            raise Refusal("native.universe-execution-capable-resolution-mismatch")
        if (U["preparedOutputSetId"] is None) != (U["preparedResolution"] == "none"):
            raise Refusal("native.universe-prepared-output-set-mismatch")
        seen_cfg = set()
        for cs in U["cfgSets"]:
            if cs["cfgSetId"] in seen_cfg:
                raise Refusal("native.universe-cfg-set-id-repeated", cs["cfgSetId"])
            seen_cfg.add(cs["cfgSetId"])
            if not set(C["baseCfg"]).issubset(set(cs["cfg"])):
                raise Refusal("native.universe-cfg-set-drops-base-cfg", cs["cfgSetId"])
        lf = U["lockfileIdentity"]
        row = snapshot["inventory"].get(lf["path"])
        if row is None or row["sha256"] != lf["contentSha256"]:
            raise Refusal("native.universe-lockfile-outside-snapshot", lf["path"])
        for p in U["crateRootPaths"]:
            if p not in snapshot["inventory"]:
                raise Refusal("native.universe-crate-root-outside-snapshot", p)
        if U["sourceUnitOwnershipId"] is not None:
            own = retained.get("sourceUnitOwnership")
            if own is None:
                raise Refusal("native.universe-retained-inputs-not-supplied",
                              "sourceUnitOwnership")
            kit.validate("native", "#/$defs/SourceUnitOwnershipV1", own)
            if "sha256:" + osip.H("native.source-unit-ownership.v1", own) \
                    != U["sourceUnitOwnershipId"]:
                raise Refusal("native.nested-identity-mismatch", "sourceUnitOwnership")
            declared = {}
            for u in own["units"]:
                uid = "sha256:" + osip.H("native.compilation-unit.v1", {
                    "schemaVersion": 1, "markerPath": u["markerPath"],
                    "targetKind": u["targetKind"], "targetName": u["targetName"]})
                if u["unitId"] != uid:
                    raise Refusal("native.compilation-unit-id-not-derived", u["unitId"])
                if uid in declared:
                    raise Refusal("native.compilation-unit-duplicate", uid)
                declared[uid] = u
                if u["markerPath"] not in snapshot["inventory"]:
                    raise Refusal("native.ownership-marker-outside-snapshot", u["markerPath"])
                if u["targetEdition"] is None and u["crateName"] not in U["edition"]:
                    raise Refusal("native.ownership-crate-not-in-edition-map", u["crateName"])
            for s in own["selectedUnitIds"]:
                if s not in declared:
                    raise Refusal("native.ownership-selection-names-undeclared-unit", s)
            for o in own["ownership"]:
                if o["unitId"] not in declared:
                    raise Refusal("native.ownership-row-names-undeclared-unit", o["unitId"])
                if o["path"] not in snapshot["inventory"]:
                    raise Refusal("native.ownership-path-outside-snapshot", o["path"])
        return True

    if udom == SX_UNIVERSE_DOMAIN:
        have = {g["grammarId"] for g in C["grammarBundle"]["grammars"]}
        for gid in U["selectedGrammarIds"]:
            if gid not in have:
                raise Refusal("native.syntax-grammar-not-in-bundle", gid)
        osip.check_order(U["selectedGrammarIds"], "utf8")
        return True
    raise Refusal("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", udom)


def _acyclic_check(graph):
    color = {}

    def visit(p):
        if color.get(p) == 1:
            raise Refusal("native.universe-config-graph-cyclic", p)
        if color.get(p) == 2:
            return
        color[p] = 1
        node = next(n for n in graph["nodes"] if n["path"] == p)
        for e in node["extendsResolved"]:
            visit(e)
        color[p] = 2

    for n in graph["nodes"]:
        visit(n["path"])


# --------------------------------------------------------------------------
# body-language-version (DERIVED; recomputed, never accepted)
# --------------------------------------------------------------------------

def _domain_row(domain):
    ds = kit.doc("identity")["x-opensip-digest-domains"]["domainSets"]
    for setname in ds:
        if domain in ds[setname]:
            return ds[setname][domain]
    raise Refusal("unregistered-domain", domain)


def longest_suffix(table, path):
    best = None
    for suf in table:
        if path.endswith(suf) and (best is None or len(suf) > len(best)):
            best = suf
    return best


def derive_body_language_version(universe, context, anchor_path, retained=None):
    """Rebuild the closed body-language-version record from named source paths."""
    retained = retained or {}
    row = _domain_row(universe["domain"])
    lvb = row["languageVersionBinding"]
    C = context["descriptor"]
    fields = {}
    for name, spec in lvb["fields"].items():
        if "const" in spec:
            fields[name] = spec["const"]
        else:
            node = C
            for step in spec["path"]:
                node = node[step]
            fields[name] = node
    dspec = lvb["dialect"]
    if dspec["source"] == "anchor-path-suffix":
        suf = longest_suffix(dspec["table"], anchor_path)
        if suf is None:
            raise Refusal(dspec["onUnknown"], anchor_path)
        variant = dspec["table"][suf]
        dialect = {dspec["key"]: variant}
        language_id = lvb["bodyLanguageByVariant"][variant]
    else:
        own = retained.get("sourceUnitOwnership")
        if own is None:
            raise Refusal(dspec["onOwnershipMissing"], anchor_path)
        if own["enumeration"] == "partial":
            raise Refusal(dspec["onOwnerUnenumerated"], anchor_path)
        rows = [o for o in own["ownership"] if o["path"] == anchor_path]
        if not rows:
            raise Refusal(dspec["onOwnerNotCompiled"], anchor_path)
        selected = [o for o in rows if o["unitId"] in own["selectedUnitIds"]]
        if not selected:
            raise Refusal(dspec["onOwnerNotSelected"], anchor_path)
        units = {u["unitId"]: u for u in own["units"]}
        editions = set()
        for o in selected:
            u = units[o["unitId"]]
            editions.add(u["targetEdition"] if u["targetEdition"] is not None
                         else universe["descriptor"]["edition"][u["crateName"]])
        if len(editions) > 1:
            raise Refusal(dspec["onOwnerAmbiguous"],
                          "%s: %s" % (anchor_path, sorted(editions)))
        dialect = {dspec["key"]: sorted(editions)[0]}
        language_id = lvb["bodyLanguage"]
    record = {"schemaVersion": 1, "languageId": language_id,
              "compilerName": fields["compilerName"],
              "compilerVersion": fields["compilerVersion"],
              "compilerBuild": fields["compilerBuild"],
              "dialect": dialect}
    kit.validate("identity", "#/$defs/body-language-version", record)
    if language_id not in lvb["bodyLanguages"]:
        raise Refusal("native.body-language-not-produced-by-this-engine", language_id)
    return record


def clone_body_fact_parts(store, universe, context, anchor_path, body_bytes,
                          level_id, level_spec_bytes, tokens=None, retained=None):
    """Returns (payload, retained frame digest, derived body-language-version)."""
    blv = derive_body_language_version(universe, context, anchor_path, retained)
    lv32 = osip.body_language_version_bytes(blv)
    level_version_hex = store.put_blob(level_spec_bytes)
    lvbytes = bytes.fromhex(level_version_hex)
    if level_id == "L0-verbatim":
        if tokens is not None:
            raise Refusal("tokenisation-forbidden-at-L0")
        payload = osip.body_payload_L0(body_bytes)
    else:
        if tokens is None:
            raise Refusal("normalized-level-requires-a-token-stream")
        payload = osip.framed_token_stream(tokens)
    ident, frame = osip.body_identity(level_id, lvbytes, blv["languageId"], lv32, payload)
    store.put_blob(frame)
    payload_rec = {"bodyIdentity": ident, "normalisationLevel": level_id,
                   "normalisationVersion": level_version_hex}
    return payload_rec, ident, blv


# --------------------------------------------------------------------------
# facts, scopes, coverage, views
# --------------------------------------------------------------------------

RELREG = kit.doc("relation")["x-opensip-relation-registry"]["relations"]
RELATION_DOC_DIGEST = kit.doc_digest("relation")
NATIVE_DOC_DIGEST = kit.doc_digest("native")


def make_fact(store, snapshot, relation, resolution, universe_hex, target_hex,
              producer_closure, payload, anchors, confidence=1000000):
    row = RELREG.get(relation)
    if row is None:
        raise Refusal("relation-not-registered", relation)
    if resolution not in row["ladder"]:
        raise Refusal("rung-not-a-member-of-this-relations-ladder",
                      "%s@%s; ladder=%s" % (relation, resolution, row["ladder"]))
    rr = (row.get("rungs") or {}).get(resolution)
    if rr:
        for f in rr.get("required", []):
            if f not in payload:
                raise Refusal("rung-required-field-missing", f)
        for f in rr.get("forbidden", []):
            if f in payload:
                raise Refusal("rung-forbidden-field-present", f)
    if row["universeRule"] == "same-only" and universe_hex != target_hex:
        raise Refusal("universeRule-same-only-violated", relation)
    kit.validate("relation", row["selector"], payload)
    osip.check_order(anchors, "canonical-set")
    desc = {"schemaVersion": 2, "snapshotId": snapshot["id"], "relation": relation,
            "resolution": resolution, "sourceUniverse": universe_hex,
            "targetUniverse": target_hex, "producerClosure": producer_closure,
            "payloadSchemaDigest": RELATION_DOC_DIGEST,
            "payloadDigest": store.put_record(payload),
            "anchors": anchors, "confidenceMillionths": confidence}
    kit.validate("identity", "#/$defs/fact", desc)
    d = store.put_frame("fact", desc)
    return {"id": "fact2:" + d, "hex": d, "descriptor": desc, "payload": payload}


def make_subject_scope(store, snapshot, relation, resolution, universe_hex, target_hex,
                       enumerator_closure, subjects):
    osip.check_order(subjects, "canonical-set")
    desc = {"schemaVersion": 2, "snapshotId": snapshot["id"],
            "sourceUniverse": universe_hex, "targetUniverse": target_hex,
            "relation": relation, "resolution": resolution,
            "enumeratorClosure": enumerator_closure, "subjects": subjects}
    kit.validate("identity", "#/$defs/subject-scope", desc)
    d = store.put_frame("subject-scope", desc)
    return {"id": "scope2:" + d, "hex": d, "commitment": "sha256:" + d,
            "descriptor": desc, "subjectCount": len(subjects)}


def make_coverage(store, scope, entry):
    """admit_coverage_result_v3: host builds the key from its OWN enumeration."""
    D = scope["descriptor"]
    key = {"relation": D["relation"], "resolution": D["resolution"],
           "sourceUniverse": D["sourceUniverse"], "targetUniverse": D["targetUniverse"],
           "subjectScopeCommitment": scope["commitment"]}
    payload = {"schemaVersion": 3, "key": key, "entry": entry}
    kit.validate("native", "#/$defs/CoverageResultV3", payload)
    if entry["relation"] != key["relation"] or entry["resolution"] != key["resolution"]:
        raise Refusal("native.coverage-entry-key-mismatch")
    if entry["examinedUniverse"]["subjectScopeCommitment"] != key["subjectScopeCommitment"]:
        raise Refusal("native.examined-universe-commitment-mismatch")
    if entry["examinedUniverse"]["subjectCount"] != scope["subjectCount"]:
        raise Refusal("native.examined-universe-subject-count-mismatch")
    check_rc2(entry)
    desc = {"schemaVersion": 2, "scopeId": scope["id"],
            "payloadSchemaDigest": NATIVE_DOC_DIGEST,
            "payloadDigest": store.put_record(payload)}
    kit.validate("identity", "#/$defs/coverage", desc)
    d = store.put_frame("coverage", desc)
    return {"id": "coverage2:" + d, "hex": d, "descriptor": desc, "payload": payload,
            "scope": scope}


ONE_RUNG = {"file", "package", "vcs-change", "declares", "literal", "control-flow", "clones"}
RESOLVED_RUNGS = {"resolved-target", "resolved-binding", "resolved-callee", "checked",
                  "from-resolved-calls"}


def check_rc2(entry, unresolved_edge_count=None):
    rc = entry["resolutionCompleteness"]
    st = rc["state"]
    if st == "not-applicable":
        if entry["resolution"] in RESOLVED_RUNGS:
            raise Refusal("RC-1", "a resolved rung must never claim not-applicable")
        return True
    if st == "complete":
        if not (rc["attempted"] and rc["examinedExhaustive"]
                and rc["stageTerminal"] == "complete" and rc["unresolvedEdgeCount"] == 0):
            raise Refusal("RC-2", "complete requires attempted+exhaustive+stage complete+0 edges")
    elif st == "incomplete":
        if not (rc["attempted"] and rc["examinedExhaustive"]
                and rc["stageTerminal"] == "complete" and rc["unresolvedEdgeCount"] >= 1):
            raise Refusal("RC-2", "incomplete requires >=1 edge with a complete stage over "
                                  "an exhaustive partition")
    elif st == "partial":
        if rc["stageTerminal"] == "complete" and rc["examinedExhaustive"]:
            raise Refusal("RC-2", "partial requires a non-complete stage or a "
                                  "non-exhaustive partition")
    elif st == "not-attempted":
        if rc["attempted"] or rc["unresolvedEdgeCount"] != 0:
            raise Refusal("RC-2", "not-attempted is a skipped stage: attempted=false, count 0")
    return True


def make_view(store, plan_id, scopes, facts, coverages, producer_closure, schema_digests):
    scope_ids = sorted({s["id"] for s in scopes})
    fact_ids = sorted({f["id"] for f in facts})
    cov_ids = sorted({c["id"] for c in coverages})
    for c in coverages:
        if c["scope"]["id"] not in scope_ids:
            raise Refusal("native.coverage-subject-scope-outside-view", c["id"])
    desc = {"schemaVersion": 2, "planId": plan_id, "scopeIds": scope_ids,
            "facts": fact_ids, "coverageIds": cov_ids,
            "producerClosure": producer_closure,
            "schemaDigests": sorted(set(schema_digests))}
    kit.validate("identity", "#/$defs/view", desc)
    d = store.put_frame("view", desc)
    return {"id": "view2:" + d, "hex": d, "descriptor": desc}


# --------------------------------------------------------------------------
# capability manifest (CVE1, delivery v4 recipe)
# --------------------------------------------------------------------------

def make_capability_manifest(store, manifest):
    cid, committed = osip.capability_manifest_id(manifest)
    bytes_digest = store.put_blob(committed)      # the committed artifact bytes
    return {"capabilityManifestId": cid, "capabilityManifestBytesDigest": bytes_digest,
            "manifest": manifest, "committedBytes": committed}


# --------------------------------------------------------------------------
# Plan
# --------------------------------------------------------------------------

def make_plan(store, snapshot, cap, semantic_closures, analysis_spec, native_contexts,
              import_ids, policy_doc, waiver_set, scope, budget, semantic_grant):
    kit.validate("identity", "#/$defs/analysis-spec", analysis_spec)
    spec_digest = store.put_record(analysis_spec)
    kit.validate("identity", "#/$defs/semantic-grant", semantic_grant)
    grant_digest = store.put_record(semantic_grant)
    kit.validate("identity", "#/$defs/scope-descriptor", scope)
    scope_digest = store.put_record(scope)
    policy_digest = store.put_record(policy_doc)
    waiver_digest = store.put_record(waiver_set)
    if budget != snapshot["config"]["analysis"]["budget"]:
        raise Refusal("plan-budget-contradicts-resolved-configuration",
                      "%r vs %r" % (budget, snapshot["config"]["analysis"]["budget"]))
    desc = {"schemaVersion": 2, "snapshotId": snapshot["id"],
            "capabilityManifestId": cap["capabilityManifestId"],
            "semanticClosures": sorted(set(semantic_closures)),
            "analysisSpecDigest": spec_digest,
            "resolvedConfigDigest": snapshot["configDigest"],
            "nativeContextDigests": sorted({c["hex"] for c in native_contexts}),
            "importIds": sorted(set(import_ids)),
            "policyDigest": policy_digest, "waiverDigest": waiver_digest,
            "scopeDigest": scope_digest, "budget": budget,
            "semanticGrantDigest": grant_digest,
            "capabilityManifestBytesDigest": cap["capabilityManifestBytesDigest"]}
    kit.validate("identity", "#/$defs/plan", desc)
    d = store.put_frame("plan", desc)
    return {"id": "plan2:" + d, "hex": d, "descriptor": desc,
            "policy": policy_doc, "waivers": waiver_set, "analysisSpec": analysis_spec,
            "semanticGrant": semantic_grant, "scope": scope}


# --------------------------------------------------------------------------
# derivation plan / stage specs
# --------------------------------------------------------------------------

def make_execution_plan(store, plan, stages):
    """stages: [{producerClosure, operation, parameters, outputDomains,
                 outputSchemaDigest, requires}]"""
    rows = []
    for i, s in enumerate(stages):
        spec = {"schemaVersion": 2, "planId": plan["id"],
                "producerClosure": s["producerClosure"], "operation": s["operation"],
                "parameters": s["parameters"], "outputDomains": sorted(s["outputDomains"]),
                "outputSchemaDigest": s["outputSchemaDigest"]}
        kit.validate("identity", "#/$defs/stage-spec", spec)
        for p in spec["parameters"]:
            if p not in plan["analysisSpec"]["parameters"]:
                raise Refusal("stage-takes-a-hidden-input", str(p))
        if spec["producerClosure"] not in plan["descriptor"]["semanticClosures"]:
            raise Refusal("stage-producer-not-plan-selected", spec["producerClosure"])
        rows.append({"ordinal": i, "stageSpecDigest": store.put_record(spec),
                     "requires": sorted(s.get("requires", [])),
                     "outputDomains": sorted(s["outputDomains"])})
        for r in rows[-1]["requires"]:
            if r >= i:
                raise Refusal("derivation-dag-not-acyclic", "%d requires %d" % (i, r))
    desc = {"schemaVersion": 2, "planId": plan["id"], "stages": rows}
    kit.validate("identity", "#/$defs/execution-plan", desc)
    d = store.put_frame("execution-plan", desc)
    return {"id": "exec-plan2:" + d, "hex": d, "descriptor": desc}


# --------------------------------------------------------------------------
# proof / findings / evidence / seal / run
# --------------------------------------------------------------------------

def node_addresses(pred, addr="p"):
    """Total, deterministic node addressing (identity section 3)."""
    out = {addr: pred}
    op = pred["op"]
    if op in ("and", "or"):
        for i, k in enumerate(pred["operands"]):
            out.update(node_addresses(k, "%s.%d" % (addr, i)))
    elif op == "not":
        out.update(node_addresses(pred["operand"], addr + ".0"))
    return out


def make_program_predicate(store, rule_program_digest, rule_id, predicate_id, node):
    rec = {"schemaVersion": 2, "ruleProgramDigest": rule_program_digest,
           "ruleId": rule_id, "predicateId": predicate_id, "operation": node["op"],
           "nodeDigest": osip.canonical_record_digest(node)}
    kit.validate("identity", "#/$defs/program-predicate", rec)
    return store.put_record(rec), rec


def make_witness(store, program_predicate_digest, fact_ids, coverage_ids,
                 count_limit=None, child_ids=()):
    rec = {"schemaVersion": 2, "programPredicateDigest": program_predicate_digest,
           "matchingFactIds": sorted(set(fact_ids)),
           "coverageIds": sorted(set(coverage_ids)),
           "countLimit": count_limit, "childPredicateIds": sorted(set(child_ids))}
    kit.validate("identity", "#/$defs/predicate-witness", rec)
    return store.put_record(rec), rec


def make_finding(store, rule_stable_id, detector_major, subject_key, related,
                 rule_closure, message_code, parameters, severity, evidence_refs):
    fp_desc = {"schemaVersion": 2, "ruleStableId": rule_stable_id,
               "detectorSemanticsMajor": detector_major, "subjectKey": subject_key,
               "relatedSubjectKeys": sorted(set(related))}
    kit.validate("identity", "#/$defs/finding-fingerprint", fp_desc)
    fp = "finding-key2:" + store.put_frame("finding-fingerprint", fp_desc)
    params = {"schemaVersion": 2, "messageCode": message_code, "parameters": parameters}
    kit.validate("identity", "#/$defs/finding-parameters", params)
    desc = {"schemaVersion": 2, "fingerprint": fp, "ruleClosure": rule_closure,
            "subjectId": subject_key["qualifiedName"], "messageCode": message_code,
            "parameterDigest": store.put_record(params), "severity": severity,
            "evidenceRefs": sorted(evidence_refs,
                                   key=lambda r: osip.c_encode(r))}
    kit.validate("identity", "#/$defs/finding", desc)
    d = store.put_frame("finding", desc)
    return {"id": "finding2:" + d, "hex": d, "descriptor": desc, "fingerprint": fp}


def make_proof(store, plan, exec_plan, evaluator_closure, rule_program_digest,
               input_refs, predicate_proofs, finding_ids, verdict):
    refs = sorted(input_refs, key=lambda r: osip.c_encode(r))
    osip.check_order(refs, "canonical-set")
    pp = sorted(predicate_proofs,
                key=lambda p: (p["ruleId"], p["subjectId"], p["predicateId"]))
    osip.check_order(pp, "predicate")
    desc = {"schemaVersion": 2, "planId": plan["id"], "executionPlanId": exec_plan["id"],
            "evaluatorClosure": evaluator_closure,
            "ruleProgramDigest": rule_program_digest,
            "evaluationInputRefs": refs, "predicateProofs": pp,
            "findingIds": sorted(set(finding_ids)), "verdict": verdict}
    kit.validate("identity", "#/$defs/proof-bundle", desc)
    forbidden = {"run", "semantic-evidence", "evaluation-seal", "proof-bundle"}
    for r in refs:
        if r["domain"] in forbidden:
            raise Refusal("proof-ref-domain-excludes-run-evidence-seal-proof", r["domain"])
    d = store.put_frame("proof-bundle", desc)
    return {"id": "proof2:" + d, "hex": d, "descriptor": desc}


def make_evidence(store, plan, views, coverages, import_ids, finding_ids, proof):
    desc = {"schemaVersion": 2, "planId": plan["id"],
            "viewIds": sorted({v["id"] for v in views}),
            "coverageIds": sorted({c["id"] for c in coverages}),
            "importIds": sorted(set(import_ids)),
            "findingIds": sorted(set(finding_ids)), "proofBundleId": proof["id"]}
    kit.validate("identity", "#/$defs/semantic-evidence", desc)
    d = store.put_frame("semantic-evidence", desc)
    return {"id": "evidence2:" + d, "hex": d, "descriptor": desc}


def make_seal(store, plan, exec_plan, evidence, evaluator_closure, proof, verdict):
    desc = {"schemaVersion": 2, "planId": plan["id"],
            "executionPlanId": exec_plan["id"], "evidenceId": evidence["id"],
            "evaluatorClosure": evaluator_closure,
            "policyDigest": plan["descriptor"]["policyDigest"],
            "proofBundleId": proof["id"], "verdict": verdict}
    kit.validate("identity", "#/$defs/evaluation-seal", desc)
    d = store.put_frame("evaluation-seal", desc)
    return {"id": "seal2:" + d, "hex": d, "descriptor": desc}


def make_run(store, snapshot, plan, evidence, seal, cap):
    desc = {"schemaVersion": 2, "projectId": PROJECT_ID, "snapshotId": snapshot["id"],
            "planId": plan["id"], "evidenceId": evidence["id"],
            "evaluationSealId": seal["id"],
            "capabilityManifestId": cap["capabilityManifestId"]}
    kit.validate("identity", "#/$defs/run", desc)
    d = store.put_frame("run", desc)
    return {"id": "run2:" + d, "hex": d, "descriptor": desc}


# --------------------------------------------------------------------------
# close_run: my reconstruction of the identity section 3/5 Run closure
# --------------------------------------------------------------------------

GRAMMAR_REG = kit.doc("native")["x-opensip-grammar-capability-registry"]["languages"]
INVENTORY_CAPS = {"file@enumerated", "package@manifest-declared", "vcs-change@vcs-reported"}


def syntax_selected_rows(universe, context):
    sel = set(universe["descriptor"]["selectedGrammarIds"])
    return [g for g in context["descriptor"]["grammarBundle"]["grammars"]
            if g["grammarId"] in sel]


def syntax_path_capability(rows, path, cap):
    """Path support is decided by the SELECTED ROWS and their own suffixes."""
    owned = {}
    for g in rows:
        for s in g["suffixes"]:
            owned[s] = g
    suf = longest_suffix(owned, path)
    if suf is None:
        return False
    g = owned[suf]
    return cap in GRAMMAR_REG[g["languageId"]]["capabilities"]


def close_run(store, run, plan, snapshot, seal, evidence, proof, views, facts,
              coverages, scopes, contexts, universes, closures, retained,
              cap, imports=()):
    """Re-decides admission over retained descriptors. Nothing is re-executed."""
    notes = []
    P = plan["descriptor"]

    # --- Plan / configuration / budget -----------------------------------
    if P["snapshotId"] != snapshot["id"]:
        raise Refusal("plan-snapshot-mismatch")
    if P["resolvedConfigDigest"] != snapshot["configDigest"]:
        raise Refusal("plan-config-disagrees-with-snapshot")
    if P["budget"] != snapshot["config"]["analysis"]["budget"]:
        raise Refusal("plan-budget-contradicts-its-own-configuration")
    if P["capabilityManifestId"] != osip.capability_manifest_id(cap["manifest"])[0]:
        raise Refusal("capability-manifest-id-not-derived-from-committed-bytes")
    if osip.raw_sha256(store.get(P["capabilityManifestBytesDigest"])) \
            != P["capabilityManifestBytesDigest"]:
        raise Refusal("capability-manifest-artifact-not-retained")

    # --- native contexts: the frame proves retention, admission is re-run --
    retained_ctx = {c["hex"]: c for c in contexts}
    if set(retained_ctx) != set(P["nativeContextDigests"]):
        raise Refusal("plan-native-context-set-mismatch",
                      "a context reached by no Plan, or a Plan naming an unretained context")
    for c in contexts:
        dom, parsed = osip.parse_frame(store.get(c["hex"]), CONTEXT_DOMAINS)
        if parsed != c["descriptor"]:
            raise Refusal("retained-context-frame-is-not-the-admitted-descriptor")
        admit_native_context(store, c, closures, snapshot, retained)
        notes.append("re-admitted %s over retained bytes" % dom)

    for u in universes:
        dom, parsed = osip.parse_frame(store.get(u["hex"]), UNIVERSE_DOMAINS)
        if parsed != u["descriptor"]:
            raise Refusal("retained-universe-frame-is-not-the-admitted-descriptor")
        cid = u["descriptor"]["nativeContextId"]
        if not cid.startswith("sha256:") or cid.split(":")[1] not in P["nativeContextDigests"]:
            raise Refusal("universe-binds-a-context-this-plan-did-not-select", cid)
        ctx = retained_ctx[cid.split(":")[1]]
        bind_universe(store, u, ctx, None, snapshot, retained)
        notes.append("re-bound %s to %s" % (dom, ctx["domain"]))

    uni_by_hex = {u["hex"]: u for u in universes}
    ctx_of = {u["hex"]: retained_ctx[u["descriptor"]["nativeContextId"].split(":")[1]]
              for u in universes}

    # --- facts: registry joins, snapshot joins, syntax capability guard ----
    for f in facts:
        F = f["descriptor"]
        if F["snapshotId"] != snapshot["id"]:
            raise Refusal("fact-wrong-source-join")
        row = RELREG[F["relation"]]
        if F["payloadSchemaDigest"] != RELATION_DOC_DIGEST:
            raise Refusal("fact-payload-schema-not-the-relation-document-digest")
        if F["resolution"] not in row["ladder"]:
            raise Refusal("fact-rung-not-in-this-relations-ladder",
                          "%s@%s" % (F["relation"], F["resolution"]))
        if row["universeRule"] == "same-only" and F["sourceUniverse"] != F["targetUniverse"]:
            raise Refusal("universeRule-same-only-violated")
        if F["sourceUniverse"] not in uni_by_hex:
            raise Refusal("fact-universe-not-retained")
        payload = osip.admit_bytes(store.get(F["payloadDigest"]))
        kit.validate("relation", row["selector"], payload)
        for a in F["anchors"]:
            inv = snapshot["inventory"].get(a["path"])
            if inv is None or inv["sha256"] != a["blobDigest"]:
                raise Refusal("anchor-does-not-name-an-inventoried-blob", a["path"])
            if a["endByte"] > inv["bytes"] or a["startByte"] > a["endByte"]:
                raise Refusal("anchor-span-outside-the-named-blob", a["path"])
        for j in row.get("snapshotJoins", []):
            _apply_snapshot_join(store, snapshot, j, payload, F)
        if F["relation"] == "clones":
            _close_clone(store, row, payload, F, uni_by_hex, ctx_of, retained, snapshot)
        u = uni_by_hex[F["sourceUniverse"]]
        if u["domain"] == SX_UNIVERSE_DOMAIN:
            rows = syntax_selected_rows(u, ctx_of[u["hex"]])
            capname = "%s@%s" % (F["relation"], F["resolution"])
            if not F["anchors"] and capname not in INVENTORY_CAPS:
                raise Refusal("SYNTAX_CAPABILITY_UNSUPPORTED_FACT",
                              "an unanchored code fact is not vacuously supported")
            for a in F["anchors"]:
                if not syntax_path_capability(rows, a["path"], capname):
                    raise Refusal("SYNTAX_CAPABILITY_UNSUPPORTED_FACT",
                                  "%s at %s" % (capname, a["path"]))

    # --- scopes: syntax capability guard on the committed examined extent --
    for s in scopes:
        S = s["descriptor"]
        if S["snapshotId"] != snapshot["id"]:
            raise Refusal("scope-wrong-source-join")
        if S["enumeratorClosure"] not in P["semanticClosures"]:
            raise Refusal("enumerator-closure-not-plan-selected")
        ec = closures.get(S["enumeratorClosure"].split(":")[1])
        if ec is None or ec["descriptor"]["kind"] != "provider":
            raise Refusal("enumerator-closure-kind-must-be-provider")

    for c in coverages:
        entry = c["payload"]["entry"]
        s = c["scope"]
        u = uni_by_hex.get(s["descriptor"]["sourceUniverse"])
        if u is None:
            raise Refusal("coverage-universe-not-retained")
        capname = "%s@%s" % (entry["relation"], entry["resolution"])
        if u["domain"] == SX_UNIVERSE_DOMAIN:
            rows = syntax_selected_rows(u, ctx_of[u["hex"]])
            available = _syntax_scope_capability(rows, capname,
                                                 s, snapshot, entry["relation"])
            if not available:
                if entry["coverage"] == "complete":
                    raise Refusal("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE",
                                  "false complete for %s" % capname)
                if entry["deficiency"] != "language-tier-unsupported":
                    raise Refusal("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE_DEFICIENCY_MISMATCH",
                                  str(entry["deficiency"]))
                if entry["nativeCause"] != "capability-missing":
                    raise Refusal("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE_CAUSE_MISMATCH",
                                  str(entry["nativeCause"]))
                notes.append("disclosed-unavailable %s" % capname)
        if entry["relation"] == "clones" and u["domain"] == RS_UNIVERSE_DOMAIN:
            owed_d, owed_c = owed_clone_disclosure(
                retained.get("sourceUnitOwnership"), s["descriptor"]["subjects"],
                u["descriptor"]["edition"])
            if owed_d is not None:
                if entry["coverage"] == "complete":
                    raise Refusal("COVERAGE_DIALECT_PREREQUISITE",
                                  "false complete under %s" % owed_c)
                if entry["deficiency"] is None:
                    raise Refusal("COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED")
                if entry["deficiency"] != owed_d:
                    raise Refusal("COVERAGE_DIALECT_DEFICIENCY_MISMATCH",
                                  str(entry["deficiency"]))
                if entry["nativeCause"] != owed_c:
                    raise Refusal("COVERAGE_DIALECT_CAUSE_MISMATCH",
                                  str(entry["nativeCause"]))
                notes.append("clones ownership disclosure %s/%s" % (owed_d, owed_c))
        check_rc2(entry)

    # --- views ------------------------------------------------------------
    for v in views:
        V = v["descriptor"]
        if V["planId"] != plan["id"]:
            raise Refusal("view-cross-plan")
        for fid in V["facts"]:
            if fid not in {f["id"] for f in facts}:
                raise Refusal("view-names-an-unretained-fact", fid)
        for cid in V["coverageIds"]:
            cov = next((c for c in coverages if c["id"] == cid), None)
            if cov is None:
                raise Refusal("native.coverage-not-admitted-at-producer-boundary", cid)
            if cov["scope"]["id"] not in V["scopeIds"]:
                raise Refusal("native.coverage-subject-scope-outside-view", cid)

    # --- proof ------------------------------------------------------------
    PB = proof["descriptor"]
    if PB["planId"] != plan["id"]:
        raise Refusal("proof-cross-plan")
    import_refs = {r["digest"] for r in PB["evaluationInputRefs"] if r["domain"] == "import"}
    plan_imports = {i.split(":")[1] for i in P["importIds"]}
    if not import_refs <= plan_imports:
        raise Refusal("import-cited-but-not-plan-selected")
    if not plan_imports <= import_refs:
        raise Refusal("every-evaluated-import-must-belong-to-plan-and-inputrefs")
    if plan_imports and "read-import" not in plan["semanticGrant"]["analysisOperations"]:
        raise Refusal("plan-with-imports-requires-read-import-in-the-semantic-grant")
    for pp in PB["predicateProofs"]:
        w = osip.admit_bytes(store.get(pp["witnessDigest"]))
        kit.validate("identity", "#/$defs/predicate-witness", w)
        prog = osip.admit_bytes(store.get(w["programPredicateDigest"]))
        kit.validate("identity", "#/$defs/program-predicate", prog)
        if prog["ruleProgramDigest"] != PB["ruleProgramDigest"]:
            raise Refusal("witness-names-another-rule-program")
        if prog["operation"] != pp["operation"] or prog["predicateId"] != pp["predicateId"]:
            raise Refusal("program-predicate-does-not-address-this-proof-node")
        for r in pp["inputRefs"]:
            if r not in PB["evaluationInputRefs"]:
                raise Refusal("predicate-input-refs-must-be-a-subset-of-evaluationInputRefs")
        for fid in w["matchingFactIds"]:
            if fid not in {f["id"] for f in facts}:
                raise Refusal("witness-fact-outside-the-named-input-views", fid)

    # --- evidence / seal / run and acyclicity ------------------------------
    E = evidence["descriptor"]
    if E["proofBundleId"] != proof["id"]:
        raise Refusal("evidence-proof-mismatch")
    if set(E["viewIds"]) != {v["id"] for v in views}:
        raise Refusal("evidence-view-roots-must-equal-the-named-views")
    view_cov = set()
    for v in views:
        view_cov |= set(v["descriptor"]["coverageIds"])
    if set(E["coverageIds"]) != view_cov:
        raise Refusal("evidence-coverage-roots-must-equal-their-coverage-union")
    S = seal["descriptor"]
    if (S["planId"], S["evidenceId"], S["proofBundleId"]) != (plan["id"], evidence["id"],
                                                              proof["id"]):
        raise Refusal("seal-join-mismatch")
    if S["verdict"] != PB["verdict"]:
        raise Refusal("seal-verdict-differs-from-proof")
    R = run["descriptor"]
    if (R["planId"], R["evidenceId"], R["evaluationSealId"], R["snapshotId"]) != \
            (plan["id"], evidence["id"], seal["id"], snapshot["id"]):
        raise Refusal("run-join-mismatch")
    for blob in (osip.c_encode(PB),):
        if b"run2:" in blob or b"evidence2:" in blob or b"seal2:" in blob:
            raise Refusal("proof-includes-a-downstream-identity", "graph must stay acyclic")
    return {"closed": True, "runId": run["id"], "notes": notes}


def _apply_snapshot_join(store, snapshot, join, payload, fact):
    form = join["form"]
    if form == "inventoried-file":
        p = payload[join["pathField"]]
        row = snapshot["inventory"].get(p)
        if row is None:
            raise Refusal("file-payload-path-not-in-snapshot-inventory", p)
        if payload[join["digestField"]] != row["sha256"]:
            raise Refusal("file-payload-content-digest-differs-from-inventory-row", p)
        if payload[join["lengthField"]] != row["bytes"]:
            raise Refusal("file-payload-byte-length-differs-from-inventory-row", p)
        data = store.get(row["sha256"])
        if osip.raw_sha256(data) != row["sha256"]:
            raise Refusal("retained-bytes-do-not-re-hash", p)
        for a in fact["anchors"]:
            if a["path"] != p:
                raise Refusal("anchor-outside-the-file-the-payload-claims", a["path"])
    elif form == "inventoried-path":
        p = payload[join["pathField"]]
        if p not in snapshot["inventory"]:
            raise Refusal("payload-path-not-in-snapshot-inventory", p)
    elif form == "inventoried-path-unless":
        p = payload[join["pathField"]]
        if payload.get(join["unlessField"]) != join["unlessValue"]:
            if p not in snapshot["inventory"]:
                raise Refusal("payload-path-not-in-snapshot-inventory", p)
    else:
        raise Refusal("unknown-snapshot-join-form", form)


def _close_clone(store, row, payload, fact, uni_by_hex, ctx_of, retained, snapshot):
    j = row["bodyIdentityJoin"]
    if len(fact["anchors"]) != j["anchorCardinality"]:
        raise Refusal("clones-fact-must-carry-exactly-one-anchor",
                      str(len(fact["anchors"])))
    a = fact["anchors"][0]
    u = uni_by_hex[fact["sourceUniverse"]]
    ctx = ctx_of[u["hex"]]
    blv = derive_body_language_version(u, ctx, a["path"], retained)
    lv32 = osip.body_language_version_bytes(blv)
    lvspec = bytes.fromhex(payload["normalisationVersion"])
    store.get(payload["normalisationVersion"])       # level spec retained + re-hashed
    frame = store.get(payload["bodyIdentity"].split(":")[1])
    if "sha256:" + osip.raw_sha256(frame) != payload["bodyIdentity"]:
        raise Refusal("clone-body-frame-does-not-rehash")
    # parse the framed preimage back into its five components + payload
    i = 0

    def take():
        nonlocal i
        n = frame[i]
        i += 1
        v = frame[i:i + n]
        i += n
        return v

    tag, level_id, level_ver, lang_id, lang_ver = (take(), take(), take(), take(), take())
    plen = int.from_bytes(frame[i:i + 4], "big")
    body = frame[i + 4:]
    if len(body) != plen:
        raise Refusal("clone-frame-payload-length-mismatch")
    if tag != j["domainTag"].encode():
        raise Refusal("clone-frame-domain-tag-mismatch")
    if level_id.decode() != payload["normalisationLevel"]:
        raise Refusal("clone-frame-levelId-differs-from-payload-normalisationLevel")
    if level_ver != lvspec:
        raise Refusal("clone-frame-levelVersion-is-not-the-retained-specification-digest")
    if lang_id.decode() != blv["languageId"]:
        raise Refusal("clone-frame-languageId-differs-from-the-derived-body-language")
    if lang_ver != lv32:
        raise Refusal("clone-frame-languageVersion-is-not-the-recomputed-projection")
    if payload["normalisationLevel"] in j["recomputableAt"]:
        blob = store.get(a["blobDigest"])
        span = blob[a["startByte"]:a["endByte"]]
        if body != osip.body_payload_L0(span):
            raise Refusal("L0-payload-is-not-the-recomputed-anchor-span")
    else:
        n = int.from_bytes(body[:4], "big")
        k, cnt = 4, 0
        while k < len(body):
            kl = int.from_bytes(body[k:k + 2], "big")
            k += 2 + kl
            vl = int.from_bytes(body[k:k + 4], "big")
            k += 4 + vl
            cnt += 1
        if cnt != n or k != len(body):
            raise Refusal("normalized-token-stream-framing-invalid")
    return True


def _syntax_scope_capability(rows, capname, scope, snapshot, relation):
    if capname in INVENTORY_CAPS:
        return True                     # never grammar-gated
    subject_kind = RELREG[relation]["subjectKind"]
    extent = scope["descriptor"]["subjects"] if subject_kind == "source-path" \
        else list(snapshot["inventory"])
    if subject_kind == "source-path":
        return bool(extent) and all(syntax_path_capability(rows, p, capname) for p in extent)
    return any(syntax_path_capability(rows, p, capname) for p in extent)


def owed_clone_disclosure(own, subjects, editions):
    """Re-derived independently at Run closure so a claim cannot define its own
    correctness (native section 10). Order is the selection law's own order."""
    if own is None:
        return "input-closure-incomplete", "body-language-ownership-missing"
    if own["enumeration"] == "partial":
        return "input-closure-incomplete", "body-language-owner-unenumerated"
    by_id = {u["unitId"]: u for u in own["units"]}
    for p in subjects:
        eds = set()
        for r in own["ownership"]:
            if r["path"] == p and r["unitId"] in own["selectedUnitIds"]:
                u = by_id[r["unitId"]]
                eds.add(u["targetEdition"] if u["targetEdition"] is not None
                        else editions[u["crateName"]])
        if len(eds) > 1:
            return "input-closure-incomplete", "body-language-owner-ambiguous"
    return None, None
