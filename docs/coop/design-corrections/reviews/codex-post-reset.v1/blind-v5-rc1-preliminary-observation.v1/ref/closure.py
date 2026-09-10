"""Blind reconstruction of the Run closure: admission + joins, from contract prose.

Implements the joins identity-and-evidence section 3/4 and native-evidence sections 1.2,
2.x, 4.1a, 10, 11 name, over retained descriptors only.  Nothing is executed: no
compiler, cargo, provider, repository or filesystem operation.
"""

from __future__ import annotations

import hashlib
import struct

import opensip_ref as R
from opensip_ref import Refuse, C, H, ident, sha256_text, raw, raw_bytes


# ---------------------------------------------------------------------------
# The retained graph
# ---------------------------------------------------------------------------


class Graph:
    def __init__(self, name):
        self.name = name
        self.cas = R.CAS()
        self.snapshot = None
        self.snapshot_id = None
        self.inventory = None            # list of Blob rows
        self.blobs = {}                  # path -> bytes
        self.closures = {}               # closure2:<hex> -> closure descriptor
        self.contexts = {}               # bare hex -> (domain, descriptor)
        self.universes = {}              # bare hex -> (domain, descriptor)
        self.nested = {}                 # bare hex -> (domain, record)
        self.scopes = {}                 # scope2:<hex> -> descriptor
        self.facts = {}                  # fact2:<hex> -> (descriptor, payload)
        self.coverages = {}              # coverage2:<hex> -> (descriptor, payload)
        self.views = {}
        self.plan = None
        self.plan_id = None
        self.config = None
        self.analysis_spec = None
        self.scope_descriptor = None
        self.semantic_grant = None
        self.policy = None
        self.rule_program = None
        self.notes = []

    # -- retention helpers -------------------------------------------------
    def retain_blob(self, path, data):
        self.blobs[path] = data
        self.cas.put_bytes(data)
        return {"path": path, "sha256": raw_bytes(data), "bytes": len(data)}

    def add_closure(self, descriptor):
        R.validate("identity", "#/$defs/closure", descriptor)
        cid = ident("closure", descriptor)
        self.cas.put_frame("closure", descriptor)
        self.closures[cid] = descriptor
        return cid

    def add_nested(self, domain, record):
        self.cas.put_frame(domain, record)
        h = H(domain, record)
        self.nested[h] = (domain, record)
        return "sha256:" + h

    def add_context(self, domain, descriptor):
        self.cas.put_frame(domain, descriptor)
        h = H(domain, descriptor)
        self.contexts[h] = (domain, descriptor)
        return h

    def add_universe(self, domain, descriptor):
        self.cas.put_frame(domain, descriptor)
        h = H(domain, descriptor)
        self.universes[h] = (domain, descriptor)
        return h

    def add_scope(self, descriptor):
        R.validate("identity", "#/$defs/subject-scope", descriptor)
        sid = ident("subject-scope", descriptor)
        self.cas.put_frame("subject-scope", descriptor)
        self.scopes[sid] = descriptor
        return sid

    def add_fact(self, descriptor, payload):
        R.validate("identity", "#/$defs/fact", descriptor)
        self.cas.put_record(payload)
        fid = ident("fact", descriptor)
        self.cas.put_frame("fact", descriptor)
        self.facts[fid] = (descriptor, payload)
        return fid

    def add_coverage(self, descriptor, payload):
        R.validate("identity", "#/$defs/coverage", descriptor)
        self.cas.put_record(payload)
        cid = ident("coverage", descriptor)
        self.cas.put_frame("coverage", descriptor)
        self.coverages[cid] = (descriptor, payload)
        return cid

    def add_view(self, descriptor):
        R.validate("identity", "#/$defs/view", descriptor)
        vid = ident("view", descriptor)
        self.cas.put_frame("view", descriptor)
        self.views[vid] = descriptor
        return vid

    def inv_row(self, path):
        for row in self.inventory:
            if row["path"] == path:
                return row
        return None


# ---------------------------------------------------------------------------
# The closing digest law: every 64-hex field must carry an annotation
# ---------------------------------------------------------------------------

HEX64 = "^[0-9a-f]{64}(?![\\s\\S])"


def _resolve_local(schema, root):
    seen = 0
    while isinstance(schema, dict) and "$ref" in schema and schema["$ref"].startswith("#/"):
        node = root
        for part in schema["$ref"][2:].split("/"):
            node = node[part]
        merged = dict(node)
        for k, v in schema.items():
            if k != "$ref":
                merged[k] = v
        schema = merged
        seen += 1
        if seen > 32:
            raise Refuse("SCHEMA_REF_CYCLE", "")
    return schema


def unannotated_hex64_fields(bundle):
    """A 64-hex field carrying no x-opensip-digest annotation is inadmissible."""
    root = R.doc_json(R._PATHS[bundle])
    bad = []

    def walk(schema, path, inherited):
        if not isinstance(schema, dict):
            return
        schema = _resolve_local(schema, root)
        ann = schema.get("x-opensip-digest", inherited)
        if schema.get("type") == "string" and schema.get("pattern") == HEX64:
            if ann is None:
                bad.append(path)
            return
        for key in ("properties",):
            for name, sub in schema.get(key, {}).items():
                walk(sub, path + "/" + name, schema.get("x-opensip-digest"))
        if "items" in schema:
            walk(schema["items"], path + "/items", schema.get("x-opensip-digest"))
        if "additionalProperties" in schema and isinstance(schema["additionalProperties"], dict):
            walk(schema["additionalProperties"], path + "/*", schema.get("x-opensip-digest"))
        for kw in ("oneOf", "anyOf", "allOf"):
            for i, sub in enumerate(schema.get(kw, [])):
                walk(sub, f"{path}/{kw}[{i}]", ann)

    for name, sub in root.get("$defs", {}).items():
        walk(sub, "#/$defs/" + name, None)
    return sorted(set(bad))


# ---------------------------------------------------------------------------
# Native context / universe admission, re-run at Run closure
# ---------------------------------------------------------------------------


def _closure_of_kind(g, bare_hex, kind, why):
    cid = "closure2:" + bare_hex
    d = g.closures.get(cid)
    if d is None:
        raise Refuse("native.native-context-closure-unretained", why)
    if H("closure", d) != bare_hex:
        raise Refuse("native.native-context-closure-identity-mismatch", why)
    if d["kind"] != kind:
        raise Refuse("native.native-context-closure-kind-mismatch", f"{why}:{d['kind']}!={kind}")
    return d


def admit_native_context(g, domain, ctx):
    """native sections 2.3/2.4/1.2 admission, re-decided over retained descriptors."""
    if domain == "native.context.typescript.v2":
        R.validate("native", "#/$defs/TypeScriptNativeContextV2", ctx)
        tool = g.closures.get(ctx["toolClosure"]["closureId"])
        if tool is None:
            raise Refuse("native.native-context-closure-unretained", "toolClosure")
        if tool["kind"] != "toolchain":
            raise Refuse("native.native-context-closure-kind-mismatch", "toolClosure")
        members = {b["sha256"] for b in tool["tree"]}
        for f in ("compiler", "runtime"):
            if ctx["toolClosure"][f] not in members:
                raise Refuse("native.native-context-tool-not-in-closure", f)
        if ctx["toolchain"]["compilerPackageDigest"] not in members:
            raise Refuse("native.native-context-tool-not-in-closure", "compilerPackageDigest")
        if ctx["toolchain"]["compilerVersion"] != tool["semanticVersion"]:
            raise Refuse("native.native-context-compiler-version-not-from-manifest", "")
        stdlib = _closure_of_kind(
            g, ctx["toolchain"]["typescriptStdlibMerkleRoot"], "stdlib", "typescriptStdlibMerkleRoot"
        )
        # complete .d.ts inventory of the retained stdlib tree, one row per member,
        # component == basename, sorted by component; a shared basename is ambiguous.
        decls = [b for b in stdlib["tree"] if b["path"].endswith(".d.ts")]
        basenames = {}
        for b in decls:
            base = b["path"].rsplit("/", 1)[-1]
            if base in basenames:
                raise Refuse("native.native-context-stdlib-tree-ambiguous-basename", base)
            basenames[base] = b["sha256"]
        declared = {row["component"]: row["sha256"] for row in ctx["toolchain"]["standardLibraryComponentDigests"]}
        for base, dg in basenames.items():
            if base not in declared:
                raise Refuse("native.native-context-stdlib-inventory-incomplete", base)
            if declared[base] != dg:
                raise Refuse("native.native-context-stdlib-tree-mismatch", base)
        for base in declared:
            if base not in basenames:
                raise Refuse("native.native-context-stdlib-tree-mismatch", base)
        # UNDER-SPECIFIED JOIN (recorded as an advisory): the contract says each
        # libSelection name "must be covered by a retained component" but publishes
        # no name->component mapping.  The only mapping the corpus exhibits is the
        # TypeScript convention lib.<name>.d.ts, which is what is applied here.
        lower = {c.lower() for c in declared}
        for lib in ctx["toolchain"]["libSelection"]:
            if ("lib.%s.d.ts" % lib).lower() not in lower and lib.lower() not in lower:
                raise Refuse("native.native-context-lib-not-retained", lib)
        hon_lib = {x.lower() for x in ctx["configProjection"]["honoredOptions"]["lib"]}
        if {x.lower() for x in ctx["toolchain"]["libSelection"]} != hon_lib:
            raise Refuse("native.native-context-lib-selection-disagrees-with-honored", "")
        if ctx["moduleResolutionMode"] != ctx["configProjection"]["honoredOptions"]["moduleResolution"]:
            raise Refuse("native.universe-context-field-mismatch", "moduleResolutionMode")
        # every configuration path the context names must be inventoried
        for p in ctx["configProjection"]["configGraphPaths"]:
            if g.inv_row(p) is None:
                raise Refuse("native.native-context-config-path-outside-snapshot", p)
        lock = ctx.get("lockfileIdentity")
        if lock is not None:
            row = g.inv_row(lock["path"])
            if row is None or row["sha256"] != lock["contentSha256"]:
                raise Refuse("native.native-context-lockfile-outside-snapshot", lock["path"])
        return "ADMIT"

    if domain == "native.context.rust.v2":
        R.validate("native", "#/$defs/NativeContextV2", ctx)
        tool = g.closures.get(ctx["toolClosure"]["closureId"])
        if tool is None or tool["kind"] != "toolchain":
            raise Refuse("native.native-context-closure-kind-mismatch", "toolClosure")
        members = {b["sha256"] for b in tool["tree"]}
        for f in ("rustc", "cargo", "procMacroServer"):
            if ctx["toolClosure"][f] not in members:
                raise Refuse("native.native-context-tool-not-in-closure", f)
        for f in ("linker", "ar"):
            v = ctx["toolClosure"][f]
            if v is not None and v not in members:
                raise Refuse("native.native-context-tool-not-in-closure", f)
        if ctx["toolchain"]["rustcVersion"] != tool["semanticVersion"]:
            raise Refuse("native.native-context-compiler-version-not-from-manifest", "")
        _closure_of_kind(g, ctx["toolchain"]["rustcDevLlvmDigest"], "rust-dev-llvm", "rustcDevLlvmDigest")
        for p in ctx["configProjection"]["replacedSnapshotConfigs"]:
            if g.inv_row(p) is None:
                raise Refuse("native.native-context-config-path-outside-snapshot", p)
        return "ADMIT"

    if domain == "native.context.syntax.v2":
        R.validate("native", "#/$defs/SyntaxNativeContextV2", ctx)
        gb = ctx["grammarBundle"]
        gclos = g.closures.get(gb["closureId"])
        if gclos is None or gclos["kind"] != "grammar":
            raise Refuse("native.native-context-closure-kind-mismatch", "grammar closure")
        if gb["parserVersion"] != gclos["semanticVersion"]:
            raise Refuse("native.syntax-grammar-version-not-from-manifest", gb["parserVersion"])
        reg = R.GRAMMAR_REGISTRY["languages"]
        seen_suffix = {}
        for row in gb["grammars"]:
            lang = row["languageId"]
            if lang not in reg:
                raise Refuse("native.syntax-grammar-language-unregistered", lang)
            if row["syntaxClass"] != reg[lang]["syntaxClass"]:
                raise Refuse("native.syntax-grammar-class-mismatch", lang)
            for sfx in row["suffixes"]:
                if sfx not in reg[lang]["suffixes"]:
                    raise Refuse("native.syntax-grammar-suffix-not-of-language", f"{lang}{sfx}")
                if sfx in seen_suffix:
                    raise Refuse("native.syntax-grammar-suffix-ambiguous", sfx)
                seen_suffix[sfx] = row["grammarId"]
        return "ADMIT"

    raise Refuse("native.native-context-language-mismatch", domain)


def bind_universe(g, udomain, universe, cdomain, ctx, retained):
    """native section 11: a universe binds a context of its OWN language."""
    row = R.DOMAIN_SETS["native-semantic-universe"][udomain]
    if row["contextDomain"] != cdomain:
        raise Refuse("native.native-context-language-mismatch", f"{udomain}<-{cdomain}")
    R.validate("native", row["selector"], universe)
    if universe["nativeContextId"] != sha256_text(cdomain, ctx):
        raise Refuse(
            "native.universe-context-binding-mismatch", "context-bytes-are-not-the-admitted-ones"
        )

    if udomain == "native.semantic-universe.typescript.v2":
        cg = retained.get("configGraph")
        if cg is None:
            raise Refuse("native.universe-retained-inputs-not-supplied", "tsconfigGraph")
        R.validate("native", "#/$defs/TypeScriptConfigGraphV1", cg)
        if raw(cg) != universe["tsconfigGraphHash"]:
            raise Refuse("native.universe-context-field-mismatch", "tsconfigGraphHash")
        node_paths = [n["path"] for n in cg["nodes"]]
        if sorted(node_paths) != sorted(ctx["configProjection"]["configGraphPaths"]):
            raise Refuse("native.universe-context-field-mismatch", "configGraphPaths")
        by_path = {n["path"]: n for n in cg["nodes"]}
        for n in cg["nodes"]:
            row_inv = g.inv_row(n["path"])
            if row_inv is None or row_inv["sha256"] != n["contentSha256"]:
                raise Refuse("native.universe-config-node-outside-snapshot", n["path"])
            for e in n["extendsResolved"]:
                if e not in by_path:
                    raise Refuse("native.universe-config-edge-unknown", e)
        # reachability from the selected entry + acyclicity
        entry = cg["entryConfigPath"]
        if entry is None:
            if cg["nodes"]:
                raise Refuse("native.universe-config-origin-mismatch", "synthesized-with-nodes")
            derived_origin = "synthesized"
        else:
            if entry not in by_path:
                raise Refuse("native.universe-config-entry-unknown", entry)
            reach, stack = set(), [entry]
            order, temp = {}, set()

            def visit(p):
                if p in temp:
                    raise Refuse("native.universe-config-graph-cyclic", p)
                if p in reach:
                    return
                temp.add(p)
                for e in by_path[p]["extendsResolved"]:
                    visit(e)
                temp.discard(p)
                reach.add(p)

            visit(entry)
            if reach != set(by_path):
                raise Refuse("native.universe-config-node-unreachable", ",".join(sorted(set(by_path) - reach)))
            k = by_path[entry]["kind"]
            derived_origin = "jsconfig" if k == "jsconfig" else "tsconfig"
        if universe["configOrigin"] != derived_origin:
            raise Refuse("native.universe-context-field-mismatch", "configOrigin")
        for f in ("languageMode", "packageModuleType"):
            if universe[f] != ctx[f]:
                raise Refuse("native.universe-context-field-mismatch", f)
        if universe["allowJs"] != ctx["configProjection"]["honoredOptions"]["allowJs"]:
            raise Refuse("native.universe-context-field-mismatch", "allowJs")
        if universe["checkJs"] != ctx["configProjection"]["honoredOptions"]["checkJs"]:
            raise Refuse("native.universe-context-field-mismatch", "checkJs")
        if universe["jsAdmittedToProgram"] != universe["allowJs"]:
            raise Refuse("native.universe-context-field-mismatch", "jsAdmittedToProgram")
        if universe["jsDiagnosticsEnabled"] != universe["checkJs"]:
            raise Refuse("native.universe-context-field-mismatch", "jsDiagnosticsEnabled")
        lk = ctx["lockfileIdentity"]
        if universe["lockfileKind"] != (lk["kind"] if lk else "none"):
            raise Refuse("native.universe-context-field-mismatch", "lockfileKind")
        layout_digest = ctx["nodeModulesLayoutDigest"]
        if universe["nodeModulesInReadSet"] != (layout_digest is not None):
            raise Refuse("native.universe-context-field-mismatch", "nodeModulesInReadSet")
        if layout_digest is not None:
            layout = retained.get("nodeModulesLayout")
            if layout is None:
                raise Refuse("native.universe-retained-inputs-not-supplied", "nodeModulesLayout")
            R.validate("native", "#/$defs/ResolvedNodeModulesLayoutV1", layout)
            if raw(layout) != layout_digest:
                raise Refuse("native.universe-context-field-mismatch", "nodeModulesLayoutDigest")
        elif "nodeModulesLayout" in retained:
            raise Refuse("native.universe-retained-layout-unselected", "")
        if (universe["synthesizedOptions"] is None) != (universe["configOrigin"] != "synthesized"):
            raise Refuse("native.universe-context-field-mismatch", "synthesizedOptions")
        if universe["synthesizedOptions"] is not None:
            syn, hon = universe["synthesizedOptions"], ctx["configProjection"]["honoredOptions"]
            for k2, v2 in syn.items():
                if hon.get(k2) != v2:
                    raise Refuse("native.universe-context-field-mismatch", "synthesizedOptions." + k2)
            if "jsx" not in syn and hon["jsx"] is not None:
                raise Refuse("native.universe-context-field-mismatch", "synthesizedOptions.jsx")
        return "ADMIT"

    if udomain == "native.semantic-universe.rust.v2":
        for f in row["contextAgreementFields"]:
            if universe[f] != ctx[f]:
                raise Refuse("native.universe-context-field-mismatch", f)
        if universe["rustflags"] != ctx["configProjection"]["rustflags"]:
            raise Refuse("native.universe-context-field-mismatch", "rustflags")
        if universe["configProjectionSha256"] != H(
            "native.cargo-config-projection.v2", ctx["configProjection"]
        ):
            raise Refuse("native.universe-context-field-mismatch", "configProjectionSha256")
        if universe["executionCapableResolution"] != (universe["preparedResolution"] != "none"):
            raise Refuse("native.universe-context-field-mismatch", "executionCapableResolution")
        if (universe["preparedOutputSetId"] is None) != (universe["preparedResolution"] == "none"):
            raise Refuse("native.universe-context-field-mismatch", "preparedOutputSetId")
        base = ctx["baseCfg"]
        seen = set()
        for cs in universe["cfgSets"]:
            if cs["cfgSetId"] in seen:
                raise Refuse("native.universe-context-field-mismatch", "cfgSetId-duplicate")
            seen.add(cs["cfgSetId"])
            if not set(base).issubset(set(cs["cfg"])):
                raise Refuse("native.universe-context-field-mismatch", "cfgSets-drops-base-cfg")
        lock = universe["lockfileIdentity"]
        inv = g.inv_row(lock["path"])
        if inv is None or inv["sha256"] != lock["contentSha256"]:
            raise Refuse("native.universe-lockfile-outside-snapshot", lock["path"])
        for p in universe["crateRootPaths"]:
            if g.inv_row(p) is None:
                raise Refuse("native.universe-crate-root-outside-snapshot", p)
        for key, field in (("dependencySourceSet", "dependencySourceSetId"),
                           ("unifiedFeatures", "unifiedFeaturesId"),
                           ("preparedOutputSet", "preparedOutputSetId"),
                           ("sourceUnitOwnership", "sourceUnitOwnershipId")):
            want = universe[field]
            rec = retained.get(key)
            if want is None:
                if rec is not None:
                    raise Refuse("native.universe-retained-record-unselected", key)
                continue
            if rec is None:
                raise Refuse("native.universe-retained-inputs-not-supplied", key)
            dom = {
                "dependencySourceSet": "native.dependency-source-set.v1",
                "unifiedFeatures": "native.unified-features.rust.v1",
                "preparedOutputSet": "native.prepared-output-set.v3",
                "sourceUnitOwnership": "native.source-unit-ownership.v1",
            }[key]
            if sha256_text(dom, rec) != want:
                raise Refuse("native.universe-nested-identity-mismatch", field)
        dss = retained.get("dependencySourceSet")
        if dss is not None and dss["lockfileIdentity"] != universe["lockfileIdentity"]:
            raise Refuse("native.universe-nested-record-contradicts", "dependencySourceSet.lockfileIdentity")
        uf = retained.get("unifiedFeatures")
        if uf is not None:
            if uf["targetTriple"] != ctx["targetTriple"] or uf["resolverVersion"] != ctx["resolverVersion"]:
                raise Refuse("native.universe-nested-record-contradicts", "unifiedFeatures")
        own = retained.get("sourceUnitOwnership")
        if own is not None:
            admit_source_unit_ownership(g, universe, own)
        return "ADMIT"

    if udomain == "native.semantic-universe.syntax.v2":
        bundled = {r["grammarId"] for r in ctx["grammarBundle"]["grammars"]}
        for gid in universe["selectedGrammarIds"]:
            if gid not in bundled:
                raise Refuse("native.syntax-grammar-not-in-bundle", gid)
        return "ADMIT"

    raise Refuse("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", udomain)


def admit_source_unit_ownership(g, universe, own):
    R.validate("native", "#/$defs/SourceUnitOwnershipV1", own)
    ids = set()
    for u in own["units"]:
        recomputed = sha256_text(
            "native.compilation-unit.v1",
            {
                "schemaVersion": 1,
                "markerPath": u["markerPath"],
                "targetKind": u["targetKind"],
                "targetName": u["targetName"],
            },
        )
        if recomputed != u["unitId"]:
            raise Refuse("sourceUnitOwnership.unitId", u["targetName"])
        if g.inv_row(u["markerPath"]) is None:
            raise Refuse("sourceUnitOwnership.markerPath-outside-snapshot", u["markerPath"])
        if u["targetEdition"] is None and u["crateName"] not in universe["edition"]:
            raise Refuse("sourceUnitOwnership.deferring-unit-crate-unknown", u["crateName"])
        ids.add(u["unitId"])
    for s in own["selectedUnitIds"]:
        if s not in ids:
            raise Refuse("sourceUnitOwnership.selection-unbound", s)
    for o in own["ownership"]:
        if o["unitId"] not in ids:
            raise Refuse("sourceUnitOwnership.ownership-unbound", o["unitId"])
        if g.inv_row(o["path"]) is None:
            raise Refuse("sourceUnitOwnership.path-outside-snapshot", o["path"])
    return "ADMIT"


# ---------------------------------------------------------------------------
# body-language-version: DERIVED, recomputed at closure
# ---------------------------------------------------------------------------


def _longest_suffix(table, path):
    best = None
    for sfx in table:
        if path.endswith(sfx) and (best is None or len(sfx) > len(best)):
            best = sfx
    return best


def body_language_version(g, universe_hex, anchor_path, retained_by_universe):
    """Rebuild the closed body-language-version record from retained records only."""
    udomain, universe = g.universes[universe_hex]
    row = R.DOMAIN_SETS["native-semantic-universe"][udomain]
    lvb = row["languageVersionBinding"]
    cdomain = row["contextDomain"]
    ctx_hex = universe["nativeContextId"][len("sha256:"):]
    _, ctx = g.contexts[ctx_hex]

    def field(spec):
        if "const" in spec:
            return spec["const"]
        node = ctx
        for p in spec["path"]:
            node = node[p]
        return node

    rec = {
        "schemaVersion": 1,
        "compilerName": field(lvb["fields"]["compilerName"]),
        "compilerVersion": field(lvb["fields"]["compilerVersion"]),
        "compilerBuild": field(lvb["fields"]["compilerBuild"]),
    }
    d = lvb["dialect"]
    if d["form"] == "closed-suffix-table":
        sfx = _longest_suffix(d["table"], anchor_path)
        if sfx is None:
            raise Refuse(d["onUnknown"], anchor_path)
        variant = d["table"][sfx]
        rec["dialect"] = {d["key"]: variant}
        rec["languageId"] = lvb["bodyLanguageByVariant"][variant]
    elif d["form"] == "selected-compilation-target-edition":
        own = retained_by_universe.get("sourceUnitOwnership")
        if universe.get("sourceUnitOwnershipId") is None or own is None:
            raise Refuse(d["onOwnershipMissing"], anchor_path)          # (1)
        if own["enumeration"] == "partial":
            raise Refuse(d["onOwnerUnenumerated"], anchor_path)          # (2) before any row
        rows = [o for o in own["ownership"] if o["path"] == anchor_path]  # (3) EQUALS, never prefix
        if not rows:
            raise Refuse(d["onOwnerNotCompiled"], anchor_path)
        sel = [o for o in rows if o["unitId"] in own["selectedUnitIds"]]  # (4)
        if not sel:
            raise Refuse(d["onOwnerNotSelected"], anchor_path)
        units = {u["unitId"]: u for u in own["units"]}
        eds = set()
        for o in sel:
            u = units[o["unitId"]]
            eds.add(u["targetEdition"] if u["targetEdition"] is not None
                    else universe["edition"][u["crateName"]])
        if len(eds) > 1:                                                  # (6)
            raise Refuse(d["onOwnerAmbiguous"], anchor_path)
        rec["dialect"] = {d["key"]: sorted(eds)[0]}                       # (5)
        rec["languageId"] = lvb["bodyLanguage"]
    else:
        raise Refuse("BODY_LANGUAGE_DIALECT_FORM_UNKNOWN", d["form"])

    if rec["languageId"] not in lvb["bodyLanguages"]:
        raise Refuse("BODY_LANGUAGE_NOT_PRODUCED_BY_ENGINE", rec["languageId"])
    R.validate("identity", "#/$defs/body-language-version", rec)
    return rec


# ---------------------------------------------------------------------------
# Coverage producer boundary (native section 4.1a + section 10 cause registry)
# ---------------------------------------------------------------------------


def admit_coverage_result_v3(g, scope_id, payload):
    R.validate("native", "#/$defs/CoverageResultV3", payload)
    scope = g.scopes[scope_id]
    commitment = "sha256:" + scope_id[len("scope2:"):]
    key, entry = payload["key"], payload["entry"]
    for f in ("relation", "resolution", "sourceUniverse", "targetUniverse"):
        if key[f] != scope[f]:
            raise Refuse("native.coverage-key-scope-mismatch", f)
    if key["subjectScopeCommitment"] != commitment:
        raise Refuse("native.subject-scope-commitment-mismatch", scope_id)
    if entry["examinedUniverse"]["subjectScopeCommitment"] != key["subjectScopeCommitment"]:
        raise Refuse("native.examined-universe-commitment-mismatch", scope_id)
    if entry["examinedUniverse"]["subjectCount"] != len(scope["subjects"]):
        raise Refuse("native.examined-universe-subject-count-mismatch", scope_id)
    if entry["relation"] != key["relation"] or entry["resolution"] != key["resolution"]:
        raise Refuse("native.coverage-entry-key-mismatch", scope_id)
    check_rc2(g, scope, entry)
    check_cause_registry(entry)
    return True


ONE_RUNG = {"file", "package", "vcs-change", "declares", "literal", "control-flow", "clones"}
SYNTACTIC = {"syntactic"}


def check_rc2(g, scope, entry):
    rc = entry["resolutionCompleteness"]
    rel, rung = entry["relation"], entry["resolution"]
    # RC-1
    if rc["state"] == "not-applicable":
        if not (rel in ONE_RUNG or rung in SYNTACTIC):
            raise Refuse("RC1_NOT_APPLICABLE_ON_RESOLVED_RUNG", f"{rel}@{rung}")
    if rung in {"resolved-target", "resolved-binding", "resolved-callee", "checked",
                "from-resolved-calls"} and rc["state"] == "not-applicable":
        raise Refuse("RC1_NOT_APPLICABLE_ON_RESOLVED_RUNG", f"{rel}@{rung}")
    # RC-2
    subj = set(scope["subjects"])
    kind = R.RELATION_REGISTRY[rel].get("subjectKind")
    edges = [f for f, (d, p) in g.facts.items()
             if d["relation"] == "unresolved-edge"
             and d["sourceUniverse"] == scope["sourceUniverse"]
             and p["relation"] == rel
             and (kind != "symbol" or p["referrer"] in subj)]
    if rc["state"] == "complete":
        if not (rc["attempted"] and rc["examinedExhaustive"]
                and rc["stageTerminal"] == "complete" and not edges):
            raise Refuse("RC2_COMPLETE_PRECONDITION", f"{rel}@{rung}")
    if rc["state"] == "incomplete":
        if not (edges and rc["stageTerminal"] == "complete" and rc["examinedExhaustive"]):
            raise Refuse("RC2_INCOMPLETE_PRECONDITION", f"{rel}@{rung}")
    if rc["state"] == "not-attempted":
        if rc["attempted"] or rc["unresolvedEdgeCount"] != 0:
            raise Refuse("RC2_NOT_ATTEMPTED_PRECONDITION", f"{rel}@{rung}")
    if rc["state"] == "partial":
        if rc["stageTerminal"] == "complete" and rc["examinedExhaustive"]:
            raise Refuse("RC2_PARTIAL_PRECONDITION", f"{rel}@{rung}")
    return True


def check_cause_registry(entry):
    """native section 10 x-opensip-deficiency-cause-registry: derived, not merely expressible."""
    d, cause = entry["deficiency"], entry["nativeCause"]
    if d is None:
        if cause is not None:
            raise Refuse("native.coverage-cause-without-deficiency", str(cause))
        return True
    row = R.CAUSE_REGISTRY.get(d)
    if row is None:
        raise Refuse("native.coverage-cause-registry-row-missing", d)
    mode = row["nativeCause"]
    if mode == "required" and cause is None:
        raise Refuse("native.coverage-cause-required", d)
    if mode == "must-be-null" and cause is not None:
        raise Refuse("native.coverage-cause-must-be-null", f"{d}:{cause}")
    if cause is not None and "allowedCauses" in row and cause not in row["allowedCauses"]:
        raise Refuse("native.coverage-cause-not-for-deficiency", f"{d}:{cause}")
    if "relations" in row and entry["relation"] not in row["relations"]:
        raise Refuse("native.coverage-cause-relation-not-in-scope", f"{d}:{entry['relation']}")
    if "requires" in row:
        node = entry
        for p in row["requires"]["path"]:
            node = node[p]
        if node != row["requires"]["equals"]:
            raise Refuse("native.coverage-cause-carrier-unsupported", d)
    if "oneOf" in row:
        node = entry
        for p in row["oneOf"]["path"]:
            node = node[p]
        if node not in row["oneOf"]["members"]:
            raise Refuse("native.coverage-cause-carrier-unsupported", f"{d}:{node}")
    if "contains" in row:
        node = entry
        for p in row["contains"]["path"]:
            node = node[p]
        if row["contains"]["member"] not in node:
            raise Refuse("native.coverage-cause-carrier-unsupported", d)
    return True


# ---------------------------------------------------------------------------
# Syntax capability guard (native section 1.2 / grammar registry enforcementBoundaries)
# ---------------------------------------------------------------------------

INVENTORY_CAPS = {"file@enumerated", "package@manifest-declared", "vcs-change@vcs-reported"}


def selected_grammar_rows(g, universe_hex):
    udomain, u = g.universes[universe_hex]
    ctx_hex = u["nativeContextId"][len("sha256:"):]
    _, ctx = g.contexts[ctx_hex]
    sel = set(u["selectedGrammarIds"])
    return [r for r in ctx["grammarBundle"]["grammars"] if r["grammarId"] in sel]


def syntax_path_capability(rows, path):
    """Longest match over the union of the SELECTED rows' own suffixes."""
    best, best_row = None, None
    for r in rows:
        for sfx in r["suffixes"]:
            if path.endswith(sfx) and (best is None or len(sfx) > len(best)):
                best, best_row = sfx, r
    if best_row is None:
        return None
    return R.GRAMMAR_REGISTRY["languages"][best_row["languageId"]]["capabilities"]


def syntax_fact_guard(g, universe_hex, fact):
    coord = f"{fact['relation']}@{fact['resolution']}"
    if coord in INVENTORY_CAPS:
        return True  # exemption belongs to the RELATION, at every boundary
    rows = selected_grammar_rows(g, universe_hex)
    for a in fact["anchors"]:
        caps = syntax_path_capability(rows, a["path"])
        if caps is None or coord not in caps:
            raise Refuse("SYNTAX_CAPABILITY_UNSUPPORTED_FACT", f"{coord}:{a['path']}")
    return True


def syntax_scope_capability(g, universe_hex, scope, entry):
    coord = f"{scope['relation']}@{scope['resolution']}"
    if coord in INVENTORY_CAPS:
        return "available"
    rows = selected_grammar_rows(g, universe_hex)
    extent = [row["path"] for row in g.inventory]
    available = any((syntax_path_capability(rows, p) or []) and coord in (syntax_path_capability(rows, p) or [])
                    for p in extent)
    if available:
        return "available"
    if entry["coverage"] == "complete":
        raise Refuse("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE", coord)
    if entry["deficiency"] != "language-tier-unsupported":
        raise Refuse("SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH", str(entry["deficiency"]))
    if entry["nativeCause"] != "capability-missing":
        raise Refuse("SYNTAX_CAPABILITY_CAUSE_MISMATCH", str(entry["nativeCause"]))
    return "unavailable"


# ---------------------------------------------------------------------------
# Relation joins over every owning fact (relation registry snapshotJoins/anchorLaw)
# ---------------------------------------------------------------------------


def check_fact(g, fact, payload, retained_by_universe):
    rel = fact["relation"]
    if rel not in R.RELATION_REGISTRY:
        raise Refuse("RELATION_UNREGISTERED", rel)
    row = R.RELATION_REGISTRY[rel]
    if fact["payloadSchemaDigest"] != R.RELATION_DOC_DIGEST:
        raise Refuse("FACT_PAYLOAD_SCHEMA_NOT_REGISTERED", rel)
    R.validate("relation", row["selector"], payload)
    if raw(payload) != fact["payloadDigest"]:
        raise Refuse("FACT_PAYLOAD_DIGEST", rel)
    R.rung_index(rel, fact["resolution"])                       # ladder membership
    rr = row.get("rungs", {}).get(fact["resolution"])
    if rr:
        for f in rr.get("required", []):
            if f not in payload:
                raise Refuse("RUNG_REQUIRED_FIELD", f)
        for f in rr.get("forbidden", []):
            if f in payload:
                raise Refuse("RUNG_FORBIDDEN_FIELD", f)
    if row["universeRule"] == "same-only" and fact["sourceUniverse"] != fact["targetUniverse"]:
        raise Refuse("UNIVERSE_RULE_SAME_ONLY", rel)
    kind, n = R.anchor_cardinality(rel)
    if kind == "exact" and len(fact["anchors"]) != n:
        raise Refuse("FACT_ANCHOR_CARDINALITY", f"{rel}:{len(fact['anchors'])}!={n}")
    if kind == "min" and len(fact["anchors"]) < n:
        raise Refuse("FACT_ANCHOR_CARDINALITY", f"{rel}:{len(fact['anchors'])}<{n}")
    for a in fact["anchors"]:
        inv = g.inv_row(a["path"])
        if inv is None or inv["sha256"] != a["blobDigest"]:
            raise Refuse("ANCHOR_SOURCE", a["path"])
        data = g.blobs[a["path"]]
        if not (0 <= a["startByte"] <= a["endByte"] <= len(data)):
            raise Refuse("ANCHOR_RANGE", a["path"])
        span = data[a["startByte"]:a["endByte"]]
        try:
            span.decode("utf-8")
        except UnicodeDecodeError:
            raise Refuse("ANCHOR_UTF8", a["path"])
    for join in row.get("snapshotJoins", []):
        if join["form"] == "inventoried-file":
            p = payload[join["pathField"]]
            inv = g.inv_row(p)
            if inv is None:
                raise Refuse("FILE_PATH_NOT_INVENTORIED", p)
            if payload[join["digestField"]] != inv["sha256"]:
                raise Refuse("FILE_DIGEST_MISMATCH", p)
            if payload[join["lengthField"]] != inv["bytes"]:
                raise Refuse("FILE_LENGTH_MISMATCH", p)
            if p not in g.blobs or raw_bytes(g.blobs[p]) != inv["sha256"]:
                raise Refuse("EVIDENCE_MISSING", p)
            for a in fact["anchors"]:
                if a["path"] != p:
                    raise Refuse("FILE_ANCHOR_FOREIGN", a["path"])
        elif join["form"] == "inventoried-path":
            if "unless" in join and payload.get(join["unless"]["field"]) == join["unless"]["equals"]:
                continue
            p = payload[join["pathField"]]
            if g.inv_row(p) is None:
                raise Refuse("PATH_NOT_INVENTORIED", p)
    if rel == "clones":
        check_clone_body(g, fact, payload, retained_by_universe)
    return True


def check_clone_body(g, fact, payload, retained_by_universe):
    join = R.RELATION_REGISTRY["clones"]["bodyIdentityJoin"]
    if join["anchorCardinality"] != R.RELATION_REGISTRY["clones"]["anchorLaw"]["cardinality"]:
        raise Refuse("RELATION_ANCHOR_LAW_DRIFT", "clones")
    anchor = fact["anchors"][0]
    bl = body_language_version(g, fact["sourceUniverse"], anchor["path"],
                               retained_by_universe.get(fact["sourceUniverse"], {}))
    lv32 = R.language_version_raw32(bl)
    spec = g.cas.get(payload["normalisationVersion"])       # level spec bytes retained
    lev32 = hashlib.sha256(spec).digest()
    if lev32.hex() != payload["normalisationVersion"]:
        raise Refuse("BODY_LEVEL_VERSION_NOT_RETAINED", payload["normalisationVersion"])
    level = payload["normalisationLevel"]
    stated = payload["bodyIdentity"]
    retained_frame = g.cas.get(stated[len("sha256:"):])
    if "sha256:" + hashlib.sha256(retained_frame).hexdigest() != stated:
        raise Refuse("BODY_FRAME_DIGEST", stated)
    parsed = parse_body_frame(retained_frame)
    if parsed["domainTag"] != R.BODY_DOMAIN_TAG:
        raise Refuse("BODY_DOMAIN_TAG", "")
    if parsed["levelId"].decode() != level:
        raise Refuse("BODY_LEVEL_ID", level)
    if parsed["levelVersion"] != lev32:
        raise Refuse("BODY_LEVEL_VERSION", "")
    if parsed["languageId"].decode() != bl["languageId"]:
        raise Refuse("BODY_LANGUAGE_ID", parsed["languageId"].decode())
    if parsed["languageVersion"] != lv32:
        raise Refuse("BODY_LANGUAGE_VERSION", "")
    if level == "L0-verbatim":
        # a real source join: the host RECOMPUTES the payload from the fact's own anchor
        want = R.body_payload_L0(g.blobs[anchor["path"]][anchor["startByte"]:anchor["endByte"]])
        if parsed["payload"] != want:
            raise Refuse("BODY_L0_PAYLOAD_NOT_ANCHOR_SPAN", anchor["path"])
    else:
        # custody + framing only; no tokenisation is graded
        check_token_stream_framing(parsed["payload"])
    return bl


def parse_body_frame(b):
    o = 0

    def take_u8():
        nonlocal o
        n = b[o]
        o += 1
        v = b[o:o + n]
        o += n
        return v

    dom = take_u8()
    lid = take_u8()
    lv = take_u8()
    lang = take_u8()
    langv = take_u8()
    plen = struct.unpack(">I", b[o:o + 4])[0]
    o += 4
    payload = b[o:o + plen]
    o += plen
    if o != len(b):
        raise Refuse("BODY_FRAME_TRAILING_BYTES", str(len(b) - o))
    return {"domainTag": dom, "levelId": lid, "levelVersion": lv,
            "languageId": lang, "languageVersion": langv, "payload": payload}


def check_token_stream_framing(payload):
    n = struct.unpack(">I", payload[:4])[0]
    o = 4
    for _ in range(n):
        kl = struct.unpack(">H", payload[o:o + 2])[0]
        o += 2 + kl
        vl = struct.unpack(">I", payload[o:o + 4])[0]
        o += 4 + vl
    if o != len(payload):
        raise Refuse("BODY_TOKEN_STREAM_FRAMING", "")
    return n


# ---------------------------------------------------------------------------
# close_run: the complete closure over the retained graph
# ---------------------------------------------------------------------------

UNIVERSE_DOMAINS = set(R.DOMAIN_SETS["native-semantic-universe"])
CONTEXT_DOMAINS = set(R.DOMAIN_SETS["native-context"])


def close_run(g, retained_by_universe, view_ids, proof, evidence, seal, run):
    """Re-decide admission over the retained bytes.  Nothing is re-executed."""
    trace = []

    # -- 1. snapshot / configuration / spec / scope / grant -------------------
    R.validate("identity", "#/$defs/snapshot", g.snapshot)
    if ident("snapshot", g.snapshot) != g.snapshot_id:
        raise Refuse("SNAPSHOT_IDENTITY", "")
    if g.snapshot["sourceInventory"] != g.inventory:
        raise Refuse("SNAPSHOT_INVENTORY", "")
    paths = [row["path"] for row in g.inventory]
    if len(set(paths)) != len(paths):
        raise Refuse("INVENTORY_DUPLICATE_PATH", "")
    if paths != sorted(paths):
        raise Refuse("INVENTORY_ORDER_PATH", "")            # x-opensip-order: path
    R.validate("identity", "#/$defs/semantic-configuration", g.config)
    R.validate("identity", "#/$defs/analysis-spec", g.analysis_spec)
    R.validate("identity", "#/$defs/scope-descriptor", g.scope_descriptor)
    R.validate("identity", "#/$defs/semantic-grant", g.semantic_grant)
    R.validate("identity", "#/$defs/plan", g.plan)
    if ident("plan", g.plan) != g.plan_id:
        raise Refuse("PLAN_IDENTITY", "")
    if g.plan["snapshotId"] != g.snapshot_id:
        raise Refuse("REFERENCE_SOURCE_JOIN", "plan.snapshotId")
    if raw(g.config) != g.plan["resolvedConfigDigest"]:
        raise Refuse("PLAN_CONFIG_DIGEST", "")
    if raw(g.config) != g.snapshot["resolvedConfigDigest"]:
        raise Refuse("SNAPSHOT_PLAN_CONFIG_DISAGREE", "")
    if raw(g.analysis_spec) != g.plan["analysisSpecDigest"]:
        raise Refuse("PLAN_ANALYSIS_SPEC_DIGEST", "")
    if raw(g.scope_descriptor) != g.plan["scopeDigest"]:
        raise Refuse("PLAN_SCOPE_DIGEST", "")
    if raw(g.scope_descriptor) != g.snapshot["scopeDigest"]:
        raise Refuse("SNAPSHOT_PLAN_SCOPE_DISAGREE", "")
    if raw(g.semantic_grant) != g.plan["semanticGrantDigest"]:
        raise Refuse("PLAN_GRANT_DIGEST", "")
    # budget committed in two places; neither silently wins
    if g.plan["budget"] != g.config["analysis"]["budget"]:
        raise Refuse("PLAN_BUDGET_CONTRADICTS_CONFIGURATION", "")
    if g.semantic_grant["projectId"] != g.snapshot["projectId"]:
        raise Refuse("GRANT_PROJECT_JOIN", "")
    if g.semantic_grant["scopeDigest"] != g.plan["scopeDigest"]:
        raise Refuse("GRANT_SCOPE_JOIN", "")
    trace.append("plan-inputs-joined")

    # -- 2. analysis-spec capability vocabulary, re-closed over the RETAINED spec
    for reqc in g.analysis_spec["requestedCapabilities"]:
        if reqc["capabilityId"] not in R.CAPABILITY_IDS:
            raise Refuse("native.requested-capability-unregistered", reqc["capabilityId"])
        if reqc["languageMode"] not in R.LANGUAGE_MODES:
            raise Refuse("native.requested-capability-mode-unregistered", reqc["languageMode"])
        cell = R.CELLS[(reqc["capabilityId"], reqc["languageMode"])]
        if cell["state"] == "NOT-SELECTED":
            raise Refuse("native.requested-capability-mode-not-selected",
                         f"{reqc['capabilityId']}:{reqc['languageMode']}")
    for p in g.analysis_spec["parameters"]:
        rows = R.PAYLOAD_REGISTRY["classes"]["parameter"]["rows"]
        hit = [k for k, v in rows.items() if R.doc_digest(_param_path(v["document"])) == p["schemaDigest"]]
        if not hit:
            raise Refuse("PAYLOAD_PARAMETER_ROW_UNREGISTERED", p["schemaDigest"])
        if len(hit) > 1:
            raise Refuse("PAYLOAD_PARAMETER_AMBIGUOUS_ROW", p["schemaDigest"])
        row = rows[hit[0]]
        payload = R.parse(g.cas.get(p["payloadDigest"]))
        _validate_selector(row["document"], row["selector"], payload)
    trace.append("analysis-spec-capabilities-and-parameters-admitted")

    # -- 3. native contexts: frames retained, re-admitted, set-equal to the Plan
    plan_ctx = set(g.plan["nativeContextDigests"])
    if plan_ctx != set(g.contexts):
        raise Refuse("PLAN_CONTEXT_SET_MISMATCH",
                     f"plan={sorted(plan_ctx)} retained={sorted(g.contexts)}")
    for h, (dom, ctx) in g.contexts.items():
        g.cas.parse_frame(h, CONTEXT_DOMAINS)
        admit_native_context(g, dom, ctx)
    # -- 4. universes bind a Plan-selected context of their OWN language
    for h, (dom, u) in g.universes.items():
        g.cas.parse_frame(h, UNIVERSE_DOMAINS)
        cdomain = R.DOMAIN_SETS["native-semantic-universe"][dom]["contextDomain"]
        ctx_hex = u["nativeContextId"][len("sha256:"):]
        if ctx_hex not in plan_ctx:
            raise Refuse("UNIVERSE_CONTEXT_NOT_PLAN_SELECTED", ctx_hex)
        bind_universe(g, dom, u, cdomain, g.contexts[ctx_hex][1],
                      retained_by_universe.get(h, {}))
    trace.append(f"native-contexts={len(g.contexts)} universes={len(g.universes)}")

    # -- 5. scopes, facts, coverage ------------------------------------------
    for sid, scope in g.scopes.items():
        if scope["snapshotId"] != g.snapshot_id:
            raise Refuse("REFERENCE_SOURCE_JOIN", "scope.snapshotId")
        for f in ("sourceUniverse", "targetUniverse"):
            if scope[f] not in g.universes:
                raise Refuse("SCOPE_UNIVERSE_UNRETAINED", scope[f])
        if scope["enumeratorClosure"] not in g.plan["semanticClosures"]:
            raise Refuse("SCOPE_ENUMERATOR_NOT_PLAN_SELECTED", scope["enumeratorClosure"])
        if g.closures[scope["enumeratorClosure"]]["kind"] != "provider":
            raise Refuse("SCOPE_ENUMERATOR_KIND", scope["enumeratorClosure"])
        R.rung_index(scope["relation"], scope["resolution"])
        if scope["subjects"] != sorted(scope["subjects"]):
            raise Refuse("SCOPE_SUBJECTS_ORDER", sid)
        if len(set(scope["subjects"])) != len(scope["subjects"]):
            raise Refuse("SCOPE_SUBJECT_DUPLICATE", sid)

    for fid, (fact, payload) in g.facts.items():
        if fact["snapshotId"] != g.snapshot_id:
            raise Refuse("REFERENCE_SOURCE_JOIN", "fact.snapshotId")
        if fact["producerClosure"] not in g.plan["semanticClosures"]:
            raise Refuse("FACT_PRODUCER_NOT_PLAN_SELECTED", fact["producerClosure"])
        for f in ("sourceUniverse", "targetUniverse"):
            if fact[f] not in g.universes:
                raise Refuse("FACT_UNIVERSE_UNRETAINED", fact[f])
        check_fact(g, fact, payload, retained_by_universe)
        if g.universes[fact["sourceUniverse"]][0] == "native.semantic-universe.syntax.v2":
            syntax_fact_guard(g, fact["sourceUniverse"], fact)

    for cid, (cov, payload) in g.coverages.items():
        if cov["scopeId"] not in g.scopes:
            raise Refuse("COVERAGE_SCOPE_UNRETAINED", cov["scopeId"])
        if cov["payloadSchemaDigest"] != R.NATIVE_DOC_DIGEST:
            raise Refuse("native.coverage-payload-schema-not-registered", cid)
        if raw(payload) != cov["payloadDigest"]:
            raise Refuse("COVERAGE_PAYLOAD_DIGEST", cid)
        admit_coverage_result_v3(g, cov["scopeId"], payload)
        scope = g.scopes[cov["scopeId"]]
        if g.universes[scope["sourceUniverse"]][0] == "native.semantic-universe.syntax.v2":
            syntax_scope_capability(g, scope["sourceUniverse"], scope, payload["entry"])
        if scope["relation"] == "clones":
            check_clone_ownership_disclosure(
                g, scope, payload["entry"],
                retained_by_universe.get(scope["sourceUniverse"], {}))
    trace.append(f"scopes={len(g.scopes)} facts={len(g.facts)} coverage={len(g.coverages)}")

    # -- 6. views: fact/scope existential join + coverage-use + totality -------
    for vid in view_ids:
        view = g.views[vid]
        if view["planId"] != g.plan_id:
            raise Refuse("VIEW_PLAN_JOIN", vid)
        if view["producerClosure"] not in g.plan["semanticClosures"]:
            raise Refuse("VIEW_PRODUCER_NOT_PLAN_SELECTED", vid)
        for sd in view["schemaDigests"]:
            if sd not in (R.RELATION_DOC_DIGEST, R.NATIVE_DOC_DIGEST):
                raise Refuse("VIEW_SCHEMA_NOT_REGISTERED", sd)
        for fid in view["facts"]:
            fact = g.facts[fid][0]
            ok = any(
                g.scopes[s]["relation"] == fact["relation"]
                and g.scopes[s]["resolution"] == fact["resolution"]
                and g.scopes[s]["sourceUniverse"] == fact["sourceUniverse"]
                and g.scopes[s]["targetUniverse"] == fact["targetUniverse"]
                for s in view["scopeIds"]
            )
            if not ok:
                raise Refuse("VIEW_FACT_SCOPE_JOIN", fid)
        for cid in view["coverageIds"]:
            cov = g.coverages[cid][0]
            if cov["scopeId"] not in view["scopeIds"]:
                raise Refuse("native.coverage-subject-scope-outside-view", cid)
        # coverageTotality: only `file` carries a row
        for cid in view["coverageIds"]:
            cov, payload = g.coverages[cid]
            scope = g.scopes[cov["scopeId"]]
            tot = R.RELATION_REGISTRY[scope["relation"]].get("coverageTotality")
            if not tot or scope["resolution"] != tot["rung"]:
                continue
            if payload["entry"]["coverage"] != "complete":
                continue
            for subject in scope["subjects"]:
                if g.inv_row(subject) is None:
                    continue                        # a subject outside the inventory is owed nothing
                paid = False
                for fid in view["facts"]:
                    fd, fp = g.facts[fid]
                    if all(fd[k] == scope[k] for k in tot["matchOn"] if k in fd) \
                       and fd["snapshotId"] == scope["snapshotId"] \
                       and fp.get(tot["pathField"]) == subject:
                        paid = True
                        break
                if not paid:
                    raise Refuse(tot["refusal"], subject)
    trace.append(f"views={len(view_ids)}")

    # -- 7. proof / evidence / seal / run ------------------------------------
    R.validate("identity", "#/$defs/proof-bundle", proof)
    if proof["planId"] != g.plan_id:
        raise Refuse("PROOF_PLAN_JOIN", "")
    if proof["ruleProgramDigest"] != raw(g.rule_program):
        raise Refuse("PROOF_RULE_PROGRAM_DIGEST", "")
    if g.rule_program["policyDigest"] != g.plan["policyDigest"]:
        raise Refuse("RULE_PROGRAM_POLICY_DIGEST", "")
    projection = {
        "schemaVersion": 1,
        "policyDigest": g.plan["policyDigest"],
        "rules": [
            {"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]}
            for r in g.policy["rules"]
        ],
    }
    if g.rule_program != projection:
        raise Refuse("RULE_PROGRAM_NOT_POLICY_PROJECTION", "")
    for atom_rel, atom_rung in _atoms(g.policy):
        _admit_atom(atom_rel, atom_rung)
    for atom_rel, atom_rung in _atoms_program(g.rule_program):
        _admit_atom(atom_rel, atom_rung)
    for ref in proof["evaluationInputRefs"]:
        if ref["domain"] in ("coverage-payload", "import-payload", "fact-payload"):
            raise Refuse("PROOF_INPUT_NOT_AUTHORITATIVE_ROOT", ref["domain"])
        if ref["domain"] == "view" and ("view2:" + ref["digest"]) not in view_ids:
            raise Refuse("PROOF_INPUT_VIEW_UNKNOWN", ref["digest"])
    for pp in proof["predicateProofs"]:
        wit = R.parse(g.cas.get(pp["witnessDigest"]))
        R.validate("identity", "#/$defs/predicate-witness", wit)
        prog = R.parse(g.cas.get(wit["programPredicateDigest"]))
        R.validate("identity", "#/$defs/program-predicate", prog)
        if prog["ruleProgramDigest"] != proof["ruleProgramDigest"]:
            raise Refuse("PROGRAM_PREDICATE_RULE_PROGRAM", "")
        if prog["ruleId"] != pp["ruleId"] or prog["predicateId"] != pp["predicateId"]:
            raise Refuse("PROGRAM_PREDICATE_ADDRESS", "")
        if prog["operation"] != pp["operation"]:
            raise Refuse("PROGRAM_PREDICATE_OPERATION", "")
        node = _address(g.rule_program, prog["ruleId"], prog["predicateId"])
        if raw(node) != prog["nodeDigest"]:
            raise Refuse("PROGRAM_PREDICATE_NODE_DIGEST", prog["predicateId"])
        if node.get("op") != prog["operation"]:
            raise Refuse("PROGRAM_PREDICATE_NODE_OP", prog["predicateId"])
        expected_children = _child_addresses(node, prog["predicateId"])
        if sorted(wit["childPredicateIds"]) != sorted(expected_children):
            raise Refuse("WITNESS_CHILDREN", prog["predicateId"])
        want_limit = node.get("n") if node.get("op") == "count-at-most" else None
        if wit["countLimit"] != want_limit:
            raise Refuse("WITNESS_COUNT_LIMIT", prog["predicateId"])
        for ref in pp["inputRefs"]:
            if ref not in proof["evaluationInputRefs"]:
                raise Refuse("PREDICATE_INPUT_NOT_IN_EVALUATION_INPUTS", str(ref))

    R.validate("identity", "#/$defs/semantic-evidence", evidence)
    if evidence["planId"] != g.plan_id:
        raise Refuse("EVIDENCE_PLAN_JOIN", "")
    if sorted(evidence["viewIds"]) != sorted(view_ids):
        raise Refuse("EVIDENCE_VIEW_ROOTS", "")
    union = sorted({c for v in view_ids for c in g.views[v]["coverageIds"]})
    if sorted(evidence["coverageIds"]) != union:
        raise Refuse("EVIDENCE_COVERAGE_ROOTS", "")
    if evidence["proofBundleId"] != ident("proof-bundle", proof):
        raise Refuse("EVIDENCE_PROOF_JOIN", "")
    if sorted(evidence["importIds"]) != sorted(g.plan["importIds"]):
        raise Refuse("EVIDENCE_IMPORTS_NOT_PLAN_SELECTED", "")
    if g.plan["importIds"] and "read-import" not in g.semantic_grant["analysisOperations"]:
        raise Refuse("PLAN_IMPORT_WITHOUT_READ_IMPORT", "")

    R.validate("identity", "#/$defs/evaluation-seal", seal)
    if seal["evidenceId"] != ident("semantic-evidence", evidence):
        raise Refuse("SEAL_EVIDENCE_JOIN", "")
    if seal["proofBundleId"] != evidence["proofBundleId"]:
        raise Refuse("SEAL_PROOF_JOIN", "")
    if seal["policyDigest"] != g.plan["policyDigest"]:
        raise Refuse("SEAL_POLICY_JOIN", "")
    if seal["verdict"] != proof["verdict"]:
        raise Refuse("SEAL_VERDICT_JOIN", "")

    R.validate("identity", "#/$defs/run", run)
    if run["snapshotId"] != g.snapshot_id or run["planId"] != g.plan_id:
        raise Refuse("RUN_SOURCE_JOIN", "")
    if run["evidenceId"] != seal["evidenceId"]:
        raise Refuse("RUN_EVIDENCE_JOIN", "")
    if run["evaluationSealId"] != ident("evaluation-seal", seal):
        raise Refuse("RUN_SEAL_JOIN", "")
    if run["capabilityManifestId"] != g.plan["capabilityManifestId"]:
        raise Refuse("RUN_CAPABILITY_MANIFEST_JOIN", "")
    committed = g.cas.get(g.plan["capabilityManifestBytesDigest"])
    if hashlib.sha256(R.CAP_MANIFEST_DOMAIN + b"\x00" + committed).hexdigest() != run["capabilityManifestId"]:
        raise Refuse("CAPABILITY_MANIFEST_ID_NOT_DERIVED", "")

    # the graph is acyclic: proof carries no evidence/seal/run identity
    for k in ("evidenceId", "evaluationSealId", "runId"):
        if k in proof:
            raise Refuse("GRAPH_CYCLE", k)
    trace.append("proof/evidence/seal/run closed")
    return {"runId": ident("run", run), "trace": trace}


def _param_path(document):
    return {
        "foundation/import-source-context.schema.json": R._PATHS["import-source-context"],
        "workflows/schemas/policy-document.schema.json": R._PATHS["policy-document"],
    }[document]


def _validate_selector(document, selector, payload):
    bundle = {
        "foundation/import-source-context.schema.json": "import-source-context",
        "workflows/schemas/policy-document.schema.json": "policy-document",
    }[document]
    if selector == "#":
        R.validate(bundle, "#", payload)
    else:
        R.validate(bundle, selector, payload)


def _atoms(policy):
    out = []
    for rule in policy["rules"]:
        out.extend(_walk_atoms(rule["emitWhen"]))
    return out


def _atoms_program(prog):
    out = []
    for rule in prog["rules"]:
        out.extend(_walk_atoms(rule["emitWhen"]))
    return out


def _walk_atoms(node):
    if node.get("op") in ("and", "or"):
        out = []
        for o in node["operands"]:
            out.extend(_walk_atoms(o))
        return out
    if node.get("op") == "not":
        return _walk_atoms(node["operand"])
    return [(node["relation"], node["minResolution"])]


EVIDENCE_RELATIONS = None


def _evidence_registry():
    global EVIDENCE_RELATIONS
    if EVIDENCE_RELATIONS is None:
        d = R.doc_json(R._PATHS["imported-evidence"])
        EVIDENCE_RELATIONS = d["x-opensip-evidence-relation-registry"]
    return EVIDENCE_RELATIONS


def _admit_atom(rel, rung):
    """Membership of THIS atom's relation's ladder is the sufficient condition."""
    if rel in R.RELATION_REGISTRY:
        R.rung_index(rel, rung)
        return "native"
    reg = _evidence_registry()
    rows = reg.get("relations", reg)
    if rel in rows:
        lad = rows[rel].get("ladder") if isinstance(rows[rel], dict) else None
        if lad and rung not in lad:
            raise Refuse("RUNG_NOT_IN_RELATION_LADDER", f"{rel}@{rung}")
        return "evidence"
    raise Refuse("ATOM_RELATION_UNREGISTERED", rel)


def _address(prog, rule_id, addr):
    rule = next(r for r in prog["rules"] if r["ruleId"] == rule_id)
    node = rule["emitWhen"]
    parts = addr.split(".")
    if parts[0] != "p":
        raise Refuse("PREDICATE_ADDRESS_ROOT", addr)
    for p in parts[1:]:
        if node.get("op") in ("and", "or"):
            node = node["operands"][int(p)]
        elif node.get("op") == "not":
            if p != "0":
                raise Refuse("PREDICATE_ADDRESS_NOT_OPERAND", addr)
            node = node["operand"]
        else:
            raise Refuse("PREDICATE_ADDRESS_LEAF", addr)
    return node


def _child_addresses(node, addr):
    if node.get("op") in ("and", "or"):
        return [f"{addr}.{i}" for i in range(len(node["operands"]))]
    if node.get("op") == "not":
        return [f"{addr}.0"]
    return []


# ---------------------------------------------------------------------------
# Clones ownership disclosure: DERIVED and ENFORCED (native section 10, CB3-MUST-5)
# ---------------------------------------------------------------------------


def derive_clone_ownership_pair(g, scope, retained_for_universe):
    """The owed (deficiency, nativeCause) from the COMMITTED ownership record and
    THIS scope's subjects, in the selection law's own order.  None means nothing owed."""
    udomain, universe = g.universes[scope["sourceUniverse"]]
    if udomain != "native.semantic-universe.rust.v2":
        return None                       # only Rust has the ownership dialect axis
    own = retained_for_universe.get("sourceUnitOwnership")
    if universe.get("sourceUnitOwnershipId") is None or own is None:
        return ("input-closure-incomplete", "body-language-ownership-missing")
    if own["enumeration"] == "partial":
        return ("input-closure-incomplete", "body-language-owner-unenumerated")
    units = {u["unitId"]: u for u in own["units"]}
    for subject in scope["subjects"]:
        rows = [o for o in own["ownership"] if o["path"] == subject]
        sel = [o for o in rows if o["unitId"] in own["selectedUnitIds"]]
        eds = set()
        for o in sel:
            u = units[o["unitId"]]
            eds.add(u["targetEdition"] if u["targetEdition"] is not None
                    else universe["edition"][u["crateName"]])
        if len(eds) > 1:
            return ("input-closure-incomplete", "body-language-owner-ambiguous")
    return None


def check_clone_ownership_disclosure(g, scope, entry, retained_for_universe):
    owed = derive_clone_ownership_pair(g, scope, retained_for_universe)
    if owed is None:
        return "nothing-owed"
    if entry["coverage"] == "complete":
        raise Refuse("COVERAGE_DIALECT_PREREQUISITE", f"{owed[0]}/{owed[1]}")
    if entry["deficiency"] is None:
        raise Refuse("COVERAGE_DIALECT_UNDISCLOSED", f"{owed[0]}/{owed[1]}")
    if entry["deficiency"] != owed[0]:
        raise Refuse("COVERAGE_DIALECT_DEFICIENCY_MISMATCH",
                     f"{entry['deficiency']}!={owed[0]}")
    if entry["nativeCause"] != owed[1]:
        raise Refuse("COVERAGE_DIALECT_CAUSE_MISMATCH", f"{entry['nativeCause']}!={owed[1]}")
    return "disclosed"


# ---------------------------------------------------------------------------
# The array law: the x-opensip-order validator keyword (identity section 3)
# ---------------------------------------------------------------------------

ORDER_VOCABULARY = {"sequence", "canonical-set", "canonical-order", "utf8", "path",
                    "numeric", "ordinal", "predicate", "ruleId", "waiverId"}


def _sort_key(order, item):
    if order == "canonical-set" or order == "canonical-order":
        return C(item)
    if order == "utf8":
        if not isinstance(item, str):
            raise Refuse("ORDER_UTF8_NON_SCALAR", str(type(item)))
        return item.encode("utf-8")
    if order == "path":
        return item["path"].encode("utf-8")
    if order == "numeric":
        if not isinstance(item, int) or isinstance(item, bool):
            raise Refuse("ORDER_NUMERIC_NON_INTEGER", repr(item))
        return item
    if order == "predicate":
        return (",".join([item["ruleId"], item["subjectId"], item["predicateId"]])
                .encode("utf-8"))
    if order in ("ruleId", "waiverId"):
        return item[order].encode("utf-8")
    if isinstance(order, dict) and "by" in order:
        return tuple(item[k].encode("utf-8") for k in order["by"])
    raise Refuse("ORDER_ANNOTATION_OUTSIDE_VOCABULARY", json.dumps(order))


def check_order(order, array, where=""):
    """`sequence` is the closing default; every other order is enforced, and all
    except `sequence`/`canonical-order` also require UNIQUE sort keys."""
    if order == "sequence":
        return True
    if order == "ordinal":
        got = [i["ordinal"] for i in array]
        if got != list(range(len(array))):
            raise Refuse("ORDER_ORDINAL_NOT_CONTIGUOUS", where)
        return True
    if isinstance(order, str) and order not in ORDER_VOCABULARY:
        raise Refuse("ORDER_ANNOTATION_OUTSIDE_VOCABULARY", f"{where}:{order}")
    keys = [_sort_key(order, i) for i in array]
    strict = order != "canonical-order"
    for a, b in zip(keys, keys[1:]):
        if strict and not a < b:
            raise Refuse("ORDER_NOT_STRICTLY_ASCENDING", where)
        if not strict and a > b:
            raise Refuse("ORDER_NOT_NONDECREASING", where)
    if strict and len(set(keys)) != len(keys):
        raise Refuse("ORDER_DUPLICATE_SORT_KEY", where)
    return True


def check_document_orders(bundle, selector, instance):
    """Walk a schema and its instance together, enforcing every declared order."""
    root = R.doc_json(R._PATHS[bundle])
    node = root
    if selector.startswith("#/"):
        for part in selector[2:].split("/"):
            node = node[part]
    found = []

    def walk(schema, value, path):
        if not isinstance(schema, dict):
            return
        schema = _resolve_local(schema, root)
        if schema.get("type") == "array" and isinstance(value, list):
            order = schema.get("x-opensip-order")
            if order is None:
                raise Refuse("ARRAY_WITHOUT_DECLARED_ORDER", path)
            check_order(order, value, path)
            found.append((path, order if isinstance(order, str) else "by"))
            for i, v in enumerate(value):
                walk(schema.get("items", {}), v, f"{path}[{i}]")
            return
        if isinstance(value, dict):
            for name, sub in schema.get("properties", {}).items():
                if name in value:
                    walk(sub, value[name], path + "/" + name)
            ap = schema.get("additionalProperties")
            if isinstance(ap, dict):
                for k, v in value.items():
                    if k not in schema.get("properties", {}):
                        walk(ap, v, path + "/" + k)
        for kw in ("oneOf", "anyOf", "allOf"):
            for sub in schema.get(kw, []):
                try:
                    walk(sub, value, path)
                except Refuse:
                    pass

    walk(node, instance, selector)
    return found
