"""Independent Run-graph builder and retained-closure checker (blind consumer B).

Everything here is derived from the normative kit prose/schemas cited inline.
No author reference implementation exists in the kit and none was consulted.
"""

import copy
import hashlib

import oslib as O
from oslib import C, H, Refused, raw_digest, sha256hex

# ---------------------------------------------------------------------------
# registries loaded from the kit
# ---------------------------------------------------------------------------
REL = O.doc("relation")["x-opensip-relation-registry"]
RELATIONS = REL["relations"]
DOMAINS = O.doc("identity")["x-opensip-digest-domains"]
UNIVERSE_ROWS = DOMAINS["domainSets"]["native-semantic-universe"]
CONTEXT_ROWS = DOMAINS["domainSets"]["native-context"]
LANGMODE_MAP = DOMAINS["languageModes"]["map"]
GRAMMAR_REG = O.doc("native")["x-opensip-grammar-capability-registry"]
MATRIX = O.doc("matrix")
CAUSE_REG = O.doc("native")["x-opensip-deficiency-cause-registry"]

RESOLVED_RUNGS = {"resolved-target", "resolved-binding", "resolved-callee",
                  "checked", "from-resolved-calls"}          # native S4.3 RC-1

REL_DOC_DIGEST = O.doc_digest("relation")
NATIVE_DOC_DIGEST = O.doc_digest("native")


class World(object):
    """One project store: CAS, typed object table, snapshot inventory."""

    def __init__(self, project_id):
        self.projectId = project_id
        self.cas = O.CAS()
        self.objects = {}          # typed identity -> descriptor
        self.frames = {}           # bare hex -> (domain, descriptor)  [h-identity]
        self.inventory = []        # snapshot source inventory rows (Blob)
        self.notes = []

    # --- retention helpers -------------------------------------------------
    def blob(self, path, data):
        d = self.cas.put(data)
        row = {"path": path, "sha256": d, "bytes": len(data)}
        self.inventory.append(row)
        return row

    def raw(self, data):
        return self.cas.put(data)

    def record(self, value):
        """canonical-record retention: retain C(record) under raw SHA-256."""
        return self.cas.put_record(value)

    def mint(self, domain, descriptor):
        """h-identity retention: retain the exact H preimage FRAME."""
        hx = H(domain, descriptor)
        self.cas.put(O.h_frame(domain, descriptor))
        self.frames[hx] = (domain, descriptor)
        ident = O.IDENTITY_PREFIX.get(domain)
        key = (ident + ":" + hx) if ident else ("sha256:" + hx)
        self.objects[key] = descriptor
        return key, hx


# ---------------------------------------------------------------------------
# derived-record recipes
# ---------------------------------------------------------------------------
def unit_id(marker_path, target_kind, target_name):
    """native S11: unitId = H(native.compilation-unit.v1, UnitIdentityV1)."""
    rec = {"schemaVersion": 1, "markerPath": marker_path,
           "targetKind": target_kind, "targetName": target_name}
    return "sha256:" + H("native.compilation-unit.v1", rec), rec


def longest_suffix(table, path):
    best = None
    for suf in table:
        if path.endswith(suf) and (best is None or len(suf) > len(best)):
            best = suf
    return best


class DialectRefusal(Refused):
    pass


def body_language_version(world, universe_domain, universe, context, anchor_path,
                          retained):
    """Recompute the DERIVED body-language-version record.

    identity-and-evidence S3 + the universe domain row's languageVersionBinding.
    Returns (record, languageId).  Raises DialectRefusal with the row's own
    typed cause name where the binding cannot SELECT.
    """
    row = UNIVERSE_ROWS[universe_domain]
    lb = row["languageVersionBinding"]
    fields = lb["fields"]

    def src(spec):
        if "const" in spec:
            return spec["const"]
        assert spec["source"] == "native-context"
        v = context
        for p in spec["path"]:
            v = v[p]
        return v

    rec = {"schemaVersion": 1,
           "compilerName": src(fields["compilerName"]),
           "compilerVersion": src(fields["compilerVersion"]),
           "compilerBuild": src(fields["compilerBuild"])}

    d = lb["dialect"]
    if d["form"] == "closed-suffix-table":
        suf = longest_suffix(d["table"], anchor_path)
        if suf is None:
            raise DialectRefusal(d["onUnknown"], anchor_path)
        variant = d["table"][suf]
        rec["dialect"] = {d["key"]: variant}
        language_id = lb["bodyLanguageByVariant"][variant]
    elif d["form"] == "selected-compilation-target-edition":
        own = retained.get("sourceUnitOwnership")
        if own is None:
            raise DialectRefusal(d["onOwnershipMissing"], anchor_path)
        # (2) enumeration partial refuses BEFORE any row is read
        if own["enumeration"] == "partial":
            raise DialectRefusal(d["onOwnerUnenumerated"], anchor_path)
        rows = [r for r in own["ownership"] if r["path"] == anchor_path]
        if not rows:
            raise DialectRefusal(d["onOwnerNotCompiled"], anchor_path)
        sel = set(own["selectedUnitIds"])
        chosen = [r for r in rows if r["unitId"] in sel]
        if not chosen:
            raise DialectRefusal(d["onOwnerNotSelected"], anchor_path)
        units = {u["unitId"]: u for u in own["units"]}
        eff = set()
        for r in chosen:
            u = units[r["unitId"]]
            e = u["targetEdition"]
            if e is None:
                e = universe["edition"][u["crateName"]]
            eff.add(e)
        if len(eff) != 1:
            raise DialectRefusal(d["onOwnerAmbiguous"], anchor_path)
        rec["dialect"] = {d["key"]: sorted(eff)[0]}
        language_id = lb["bodyLanguage"]
    else:
        raise Refused("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", universe_domain)

    if language_id not in ("typescript", "javascript", "rust"):
        raise Refused("BODY_LANGUAGE_ID_NOT_IN_ENUM", str(language_id))
    rec["languageId"] = language_id
    return rec, language_id


# ---------------------------------------------------------------------------
# The retained-closure checker
# ---------------------------------------------------------------------------
class Closure(object):
    """close_run: validate every retained record, recompute every identity,
    and re-run the owning contract admissions over the retained bytes."""

    def __init__(self, world):
        self.w = world
        self.errs = []
        self.checks = 0

    def bad(self, code, detail=""):
        self.errs.append(code + ((": " + detail) if detail else ""))

    def ok(self):
        self.checks += 1

    # -- schema validation --------------------------------------------------
    def schema(self, document, selector, instance, label):
        """Exact typed admission, then JSON Schema, then the DECLARED
        x-opensip-order of every array (identity S3: "Schema admission checks
        the declared order; the shared encoder does not infer sets or reorder
        inputs")."""
        e = O.validate(document, selector, instance)
        self.checks += 1
        for m in e:
            self.bad("SCHEMA[%s]" % label, m)
        try:
            for m in O.admit_ordered(document, selector, instance):
                self.bad("ORDER[%s]" % label, m)
        except Exception as ex:
            self.bad("ORDER_ADMISSION_FAULT[%s]" % label, str(ex))
        return not e

    # -- retained frame admission ------------------------------------------
    def frame(self, bare_hex, domain_set, label):
        """Fetch the retained H preimage frame, admit it exactly, return value."""
        self.checks += 1
        try:
            raw = self.w.cas.get(bare_hex)
        except Refused:
            self.bad("MISSING_PREIMAGE[%s]" % label, bare_hex)
            return None
        try:
            dom, val = O.parse_h_frame(raw)
        except Refused as r:
            self.bad("FRAME[%s]" % label, r.code)
            return None
        if sha256hex(raw) != bare_hex:
            self.bad("FRAME_DIGEST[%s]" % label, bare_hex)
            return None
        rows = DOMAINS["domainSets"].get(domain_set, {})
        if dom not in rows:
            self.bad("UNREGISTERED_H_DOMAIN[%s]" % label, dom)
            return None
        row = rows[dom]
        self.schema(_docname(row["document"]), row["selector"], val,
                    label + "/" + dom)
        return dom, val

    def canonical_record(self, digest, document, selector, label):
        self.checks += 1
        try:
            raw = self.w.cas.get(digest)
        except Refused:
            self.bad("MISSING_PREIMAGE[%s]" % label, digest)
            return None
        try:
            val = O.parse_exact(raw)
        except Refused as r:
            self.bad("PREIMAGE_NOT_ADMISSIBLE[%s]" % label, r.code)
            return None
        if C(val) != raw:
            self.bad("PREIMAGE_NOT_CANONICAL[%s]" % label, digest)
            return None
        if document:
            self.schema(document, selector, val, label)
        return val

    # ---------------------------------------------------------------------
    def close_run(self, run_id):
        w = self.w
        run = w.objects.get(run_id)
        if run is None:
            self.bad("RUN_NOT_RETAINED", run_id)
            return self.errs
        self.schema("identity", "#/$defs/run", run, "run")
        if run["projectId"] != w.projectId:
            self.bad("RUN_PROJECT_MISMATCH", run["projectId"])

        # --- identity recomputation for every typed object ----------------
        for key, desc in sorted(w.objects.items()):
            if ":" not in key:
                continue
            pre = key.split(":", 1)[0]
            dom = {v: k for k, v in O.IDENTITY_PREFIX.items()}.get(pre)
            if dom is None:
                continue
            self.checks += 1
            if H(dom, desc) != key.split(":", 1)[1]:
                self.bad("IDENTITY_MISMATCH", key)

        snap = w.objects[run["snapshotId"]]
        plan = w.objects[run["planId"]]
        ev = w.objects[run["evidenceId"]]
        seal = w.objects[run["evaluationSealId"]]
        self.schema("identity", "#/$defs/snapshot", snap, "snapshot")
        self.schema("identity", "#/$defs/plan", plan, "plan")
        self.schema("identity", "#/$defs/semantic-evidence", ev, "evidence")
        self.schema("identity", "#/$defs/evaluation-seal", seal, "seal")

        # --- acyclicity of the semantic graph -----------------------------
        proof = w.objects[ev["proofBundleId"]]
        self.schema("identity", "#/$defs/proof-bundle", proof, "proof")
        for k in ("planId",):
            pass
        if seal["evidenceId"] != run["evidenceId"]:
            self.bad("SEAL_EVIDENCE_JOIN")
        if seal["proofBundleId"] != ev["proofBundleId"]:
            self.bad("SEAL_PROOF_JOIN")
        if ev["planId"] != run["planId"] or proof["planId"] != run["planId"]:
            self.bad("PLAN_JOIN")
        if proof["verdict"] != seal["verdict"]:
            self.bad("VERDICT_JOIN")
        # proof must not reach evidence/seal/run outputs
        for r in proof["evaluationInputRefs"]:
            if r["domain"] in ("run", "semantic-evidence", "evaluation-seal",
                               "proof-bundle"):
                self.bad("PROOF_INPUT_DOMAIN_FORBIDDEN", r["domain"])
            if r["domain"] in ("coverage-payload", "import-payload", "fact-payload"):
                self.bad("PROOF_INPUT_NOT_AUTHORITATIVE_ROOT", r["domain"])

        # --- snapshot inventory / vcs -------------------------------------
        inv = self.canonical_record(
            snap["sourceInventory"] if isinstance(snap["sourceInventory"], str)
            else None, None, None, "inventory") if isinstance(
            snap["sourceInventory"], str) else snap["sourceInventory"]
        inv = snap["sourceInventory"]
        self.schema("identity", "#/$defs/source-inventory", inv, "source-inventory")
        inv_by_path = {}
        for row in inv:
            if row["path"] in inv_by_path:
                self.bad("INVENTORY_DUPLICATE_PATH", row["path"])
            inv_by_path[row["path"]] = row
            self.checks += 1
            try:
                b = w.cas.get(row["sha256"])
            except Refused:
                self.bad("MISSING_SOURCE_BLOB", row["path"])
                continue
            if len(b) != row["bytes"]:
                self.bad("INVENTORY_LENGTH", row["path"])
        vcs = self.canonical_record(snap["vcsDigest"], "identity",
                                    "#/$defs/vcs-observation", "vcs")
        if vcs and vcs["sourceInventoryDigest"] != raw_digest(inv):
            self.bad("VCS_INVENTORY_DIGEST")

        # --- configuration / scope / spec / grant -------------------------
        cfg = self.canonical_record(plan["resolvedConfigDigest"], "identity",
                                    "#/$defs/semantic-configuration", "config")
        scope = self.canonical_record(plan["scopeDigest"], "identity",
                                      "#/$defs/scope-descriptor", "scope")
        spec = self.canonical_record(plan["analysisSpecDigest"], "identity",
                                     "#/$defs/analysis-spec", "analysis-spec")
        grant = self.canonical_record(plan["semanticGrantDigest"], "identity",
                                      "#/$defs/semantic-grant", "semantic-grant")
        if snap["resolvedConfigDigest"] != plan["resolvedConfigDigest"]:
            self.bad("SNAPSHOT_PLAN_CONFIG_DISAGREE")
        if snap["scopeDigest"] != plan["scopeDigest"]:
            self.bad("SNAPSHOT_PLAN_SCOPE_DISAGREE")
        # budget equality, exactly and by type
        if cfg is not None:
            self.checks += 1
            b1, b2 = plan["budget"], cfg["analysis"]["budget"]
            if C(b1) != C(b2):
                self.bad("PLAN_BUDGET_CONTRADICTS_CONFIGURATION",
                         "%s vs %s" % (C(b1), C(b2)))
        if grant is not None:
            self.checks += 1
            if grant["projectId"] != w.projectId:
                self.bad("GRANT_PROJECT_JOIN")
            if grant["scopeDigest"] != plan["scopeDigest"]:
                self.bad("GRANT_SCOPE_JOIN")
            if plan["importIds"] and "read-import" not in grant["analysisOperations"]:
                self.bad("PLAN_IMPORT_WITHOUT_READ_IMPORT")

        # --- capability manifest ------------------------------------------
        self.checks += 1
        try:
            cm_bytes = w.cas.get(plan["capabilityManifestBytesDigest"])
        except Refused:
            self.bad("MISSING_CAPABILITY_MANIFEST_ARTIFACT")
            cm_bytes = None
        if cm_bytes is not None:
            if O.capability_manifest_id(cm_bytes) != plan["capabilityManifestId"]:
                self.bad("CAPABILITY_MANIFEST_ID_MISMATCH")
            if run["capabilityManifestId"] != plan["capabilityManifestId"]:
                self.bad("RUN_PLAN_CAPABILITY_MANIFEST_DISAGREE")
            try:
                cm = O.cve1_decode(cm_bytes)
                if O.cve1(cm) != cm_bytes:
                    self.bad("CAPABILITY_MANIFEST_NOT_CANONICAL_CVE1")
                for v in O.admit_capability_manifest(cm):
                    self.bad("CAPABILITY_MANIFEST_ADMISSION", v)
            except Refused as r:
                self.bad("CAPABILITY_MANIFEST_DECODE", r.code)

        # --- registered schema documents ----------------------------------
        for d in (REL_DOC_DIGEST, NATIVE_DOC_DIGEST):
            self.checks += 1
            if d not in w.cas:
                self.bad("REGISTERED_SCHEMA_DOCUMENT_NOT_RETAINED", d)

        # --- closures ------------------------------------------------------
        closures = {}
        for cid in plan["semanticClosures"]:
            c = w.objects.get(cid)
            if c is None:
                self.bad("CLOSURE_NOT_RETAINED", cid)
                continue
            self.schema("identity", "#/$defs/closure", c, "closure")
            closures[cid] = c

        def retained_closure(cid, kind, label):
            c = self.w.objects.get(cid)
            self.checks += 1
            if c is None:
                self.bad("NATIVE_CONTEXT_CLOSURE_UNRETAINED[%s]" % label, cid)
                return None
            if H("closure", c) != cid.split(":", 1)[1]:
                self.bad("NATIVE_CONTEXT_CLOSURE_IDENTITY_MISMATCH[%s]" % label, cid)
            if c["kind"] != kind:
                self.bad("NATIVE_CONTEXT_CLOSURE_KIND_MISMATCH[%s]" % label,
                         "%s!=%s" % (c["kind"], kind))
            for row in c["tree"]:
                if row["sha256"] not in self.w.cas:
                    self.bad("CLOSURE_TREE_MEMBER_NOT_RETAINED[%s]" % label,
                             row["path"])
            return c

        # --- native contexts: frames + owning admission --------------------
        contexts = {}
        for hx in plan["nativeContextDigests"]:
            got = self.frame(hx, "native-context", "native-context")
            if got is None:
                continue
            dom, ctx = got
            contexts[hx] = (dom, ctx)
            row = CONTEXT_ROWS[dom]
            # admit_native_context re-run: closure joins
            for cj in row.get("closureJoins", []):
                v = ctx
                for p in cj["path"]:
                    v = v[p]
                cid = v if cj["form"] == "closure2-identity" else "closure2:" + v
                retained_closure(cid, cj["kind"], dom + "/" + "/".join(cj["path"]))
            # compiler version must come from the admitted tool closure manifest
            if dom == "native.context.typescript.v2":
                tc = self.w.objects.get(ctx["toolClosure"]["closureId"])
                if tc and tc["semanticVersion"] != ctx["toolchain"]["compilerVersion"]:
                    self.bad("native.native-context-compiler-version-not-from-manifest",
                             ctx["toolchain"]["compilerVersion"])
                if tc:
                    members = {r["sha256"] for r in tc["tree"]}
                    for f in ("compiler", "runtime"):
                        if ctx["toolClosure"][f] not in members:
                            self.bad("native.native-context-tool-not-in-closure", f)
                    if ctx["toolchain"]["compilerPackageDigest"] not in members:
                        self.bad("native.native-context-tool-not-in-closure",
                                 "compilerPackageDigest")
                # stdlib inventory completeness + basename ambiguity + lib join
                std = self.w.objects.get(
                    "closure2:" + ctx["toolchain"]["typescriptStdlibMerkleRoot"])
                if std:
                    basenames = {}
                    for r in std["tree"]:
                        bn = r["path"].rsplit("/", 1)[-1]
                        if not bn.endswith(".d.ts"):
                            continue
                        if bn in basenames:
                            self.bad("native.native-context-stdlib-tree-ambiguous-basename",
                                     bn)
                        basenames[bn] = r["sha256"]
                    declared = {r["component"]: r["sha256"]
                                for r in ctx["toolchain"]["standardLibraryComponentDigests"]}
                    for bn, dg in basenames.items():
                        if bn not in declared:
                            self.bad("native.native-context-stdlib-inventory-incomplete", bn)
                        elif declared[bn] != dg:
                            self.bad("native.native-context-stdlib-component-digest-mismatch", bn)
                    for n in ctx["toolchain"]["libSelection"]:
                        comp = "lib." + _fold(n) + ".d.ts"
                        if comp not in declared:
                            self.bad("native.native-context-lib-not-retained", n)
                    folded_sel = [_fold(n) for n in ctx["toolchain"]["libSelection"]]
                    if len(set(folded_sel)) != len(folded_sel):
                        self.bad("native.native-context-field-mismatch",
                                 "duplicate-lib-selection")
                    if set(folded_sel) != {
                            _fold(n) for n in
                            ctx["configProjection"]["honoredOptions"]["lib"]}:
                        self.bad("native.native-context-field-mismatch", "libSelection")
                if ctx["moduleResolutionMode"] != \
                        ctx["configProjection"]["honoredOptions"]["moduleResolution"]:
                    self.bad("native.native-context-field-mismatch",
                             "moduleResolutionMode")
                if (ctx["nodeModulesLayoutDigest"] is not None):
                    lay = self.canonical_record(
                        ctx["nodeModulesLayoutDigest"], "native",
                        "#/$defs/ResolvedNodeModulesLayoutV1", "nodeModulesLayout")
                    if lay:
                        for e in lay["entries"]:
                            if e["contentSha256"] not in self.w.cas:
                                self.bad("NODE_MODULES_MANIFEST_NOT_RETAINED",
                                         e["installPath"])
            if dom == "native.context.syntax.v2":
                gb = ctx["grammarBundle"]
                gc = retained_closure(gb["closureId"], "grammar", "grammarBundle")
                if gc and gc["semanticVersion"] != gb["parserVersion"]:
                    self.bad("native.syntax-grammar-version-not-from-manifest",
                             gb["parserVersion"])
                if gb["bundleDigest"] not in self.w.cas:
                    self.bad("SYNTAX_GRAMMAR_BUNDLE_NOT_RETAINED")
                for g in gb["grammars"]:
                    if g["grammarDigest"] not in self.w.cas:
                        self.bad("SYNTAX_GRAMMAR_DEFINITION_NOT_RETAINED",
                                 g["grammarId"])
                    reg = GRAMMAR_REG["languages"].get(g["languageId"])
                    if reg is None:
                        self.bad("SYNTAX_GRAMMAR_LANGUAGE_UNREGISTERED", g["languageId"])
                    else:
                        if g["syntaxClass"] != reg["syntaxClass"]:
                            self.bad("SYNTAX_GRAMMAR_CLASS_CONTRADICTS_REGISTRY",
                                     g["languageId"])
                        for s in g["suffixes"]:
                            if s not in reg["suffixes"]:
                                self.bad("SYNTAX_GRAMMAR_SUFFIX_NOT_OWNED",
                                         "%s %s" % (g["languageId"], s))
                if gb["normalizer"]["specificationDigest"] not in self.w.cas:
                    self.bad("SYNTAX_NORMALIZER_SPEC_NOT_RETAINED")
            if dom == "native.context.rust.v2":
                tc = self.w.objects.get(ctx["toolClosure"]["closureId"])
                if tc and tc["semanticVersion"] != ctx["toolchain"]["rustcVersion"]:
                    self.bad("native.native-context-compiler-version-not-from-manifest",
                             ctx["toolchain"]["rustcVersion"])
                if tc:
                    members = {r["sha256"] for r in tc["tree"]}
                    for f in ("rustc", "cargo", "procMacroServer"):
                        if ctx["toolClosure"][f] not in members:
                            self.bad("native.native-context-tool-not-in-closure", f)
                proj = ctx["configProjection"]
                if proj["projectionSha256"] not in self.w.cas:
                    self.bad("CARGO_PROJECTION_FILE_NOT_RETAINED")
            # snapshot joins for the context's own paths
            for sj in row.get("snapshotJoins", []):
                v = ctx
                for p in sj["path"]:
                    v = v[p]
                if v is None and sj.get("nullable"):
                    continue
                if sj["form"] == "inventoried-paths":
                    for p in v:
                        if p not in inv_by_path:
                            self.bad("CONTEXT_PATH_OUTSIDE_SNAPSHOT", p)
                elif sj["form"] == "inventoried-path-and-digest":
                    p = v[sj["pathField"]]
                    if p not in inv_by_path:
                        self.bad("CONTEXT_LOCKFILE_OUTSIDE_SNAPSHOT", p)
                    elif inv_by_path[p]["sha256"] != v[sj["digestField"]]:
                        self.bad("CONTEXT_LOCKFILE_DIGEST_MISMATCH", p)
            # nested semantic identities are records, not opaque strings
            for ni in row.get("nestedIdentities", []):
                v = ctx
                for p in ni["path"]:
                    v = v[p]
                if v is None and ni.get("nullable"):
                    continue
                bare = v.split(":", 1)[-1] if ni["form"] == "sha256-text" else v
                self.frame(bare, ni["domainSet"], "nested/" + "/".join(ni["path"]))

        # --- universes: frames, binding, context-of-own-language -----------
        universes = {}
        retained_nested = {}
        for hx, (dom, ctx) in list(contexts.items()):
            pass
        # gather every universe named by any fact or scope
        named = set()
        for key, desc in w.objects.items():
            if key.startswith("fact2:") or key.startswith("scope2:"):
                named.add(desc["sourceUniverse"])
                named.add(desc["targetUniverse"])
        for uhx in sorted(named):
            got = self.frame(uhx, "native-semantic-universe", "universe")
            if got is None:
                continue
            udom, uni = got
            urow = UNIVERSE_ROWS[udom]
            cfield = uni
            for p in urow["contextField"]:
                cfield = cfield[p]
            cbare = cfield.split(":", 1)[-1]
            if cbare not in plan["nativeContextDigests"]:
                self.bad("UNIVERSE_CONTEXT_NOT_PLAN_SELECTED", uhx)
                continue
            if cbare not in contexts:
                self.bad("UNIVERSE_CONTEXT_NOT_ADMITTED", uhx)
                continue
            cdom, ctx = contexts[cbare]
            if cdom != urow["contextDomain"]:
                self.bad("native.native-context-language-mismatch",
                         "%s/%s" % (udom, cdom))
                continue
            nested = {}
            for ni in urow.get("nestedIdentities", []):
                v = uni
                for p in ni["path"]:
                    v = v[p]
                if v is None and ni.get("nullable"):
                    continue
                bare = v.split(":", 1)[-1] if ni["form"] == "sha256-text" else v
                g = self.frame(bare, ni["domainSet"], "nested/" + "/".join(ni["path"]))
                if g and "retainedAs" in ni:
                    nested[ni["retainedAs"]] = g[1]
            for nr in urow.get("nestedRecords", []):
                v = uni
                for p in nr["path"]:
                    v = v[p]
                if v is None and nr.get("nullable"):
                    continue
                rec = self.canonical_record(v, _docname(nr["document"]),
                                            nr["selector"], nr["retainedAs"])
                if rec is not None:
                    nested[nr["retainedAs"]] = rec
            # overlapping identifiers must be equal
            for f in urow.get("contextAgreementFields", []):
                if f in uni and f in ctx and uni[f] != ctx[f]:
                    self.bad("native.universe-context-field-mismatch", f)
            for sj in urow.get("snapshotJoins", []):
                v = uni
                for p in sj["path"]:
                    v = v[p]
                if sj["form"] == "inventoried-paths":
                    for p in v:
                        if p not in inv_by_path:
                            self.bad("UNIVERSE_PATH_OUTSIDE_SNAPSHOT", p)
                elif sj["form"] == "inventoried-path-and-digest":
                    p = v[sj["pathField"]]
                    if p not in inv_by_path:
                        self.bad("UNIVERSE_LOCKFILE_OUTSIDE_SNAPSHOT", p)
                    elif inv_by_path[p]["sha256"] != v[sj["digestField"]]:
                        self.bad("UNIVERSE_LOCKFILE_DIGEST_MISMATCH", p)
            # TypeScript config-graph derivation
            if udom == "native.semantic-universe.typescript.v2":
                cg = nested.get("configGraph")
                if cg is not None:
                    paths = [n["path"] for n in cg["nodes"]]
                    if sorted(paths) != sorted(ctx["configProjection"]["configGraphPaths"]):
                        self.bad("CONFIG_GRAPH_PATHS_DISAGREE_WITH_CONTEXT", uhx)
                    for n in cg["nodes"]:
                        if n["path"] not in inv_by_path:
                            self.bad("CONFIG_GRAPH_NODE_OUTSIDE_SNAPSHOT", n["path"])
                        elif inv_by_path[n["path"]]["sha256"] != n["contentSha256"]:
                            self.bad("CONFIG_GRAPH_NODE_DIGEST_MISMATCH", n["path"])
                        if n["kind"] != _config_node_kind(n["path"]):
                            self.bad("native.config-graph-kind-contradicts-path",
                                     n["path"])
                        for e in n["extendsResolved"]:
                            if e not in paths:
                                self.bad("CONFIG_GRAPH_EDGE_UNKNOWN_NODE", e)
                    derived = ("synthesized"
                               if cg["entryConfigPath"] is None and not cg["nodes"]
                               else _config_node_kind(cg["entryConfigPath"]))
                    if derived == "other":
                        derived = "tsconfig"
                    if uni["configOrigin"] != derived:
                        self.bad("CONFIG_ORIGIN_NOT_DERIVED",
                                 "%s!=%s" % (uni["configOrigin"], derived))
                    if raw_digest(cg) != uni["tsconfigGraphHash"]:
                        self.bad("TSCONFIG_GRAPH_HASH_MISMATCH", uhx)
                for f in ("languageMode", "packageModuleType"):
                    if uni[f] != ctx[f]:
                        self.bad("native.universe-context-field-mismatch", f)
                if uni["allowJs"] != ctx["configProjection"]["honoredOptions"]["allowJs"]:
                    self.bad("native.universe-context-field-mismatch", "allowJs")
                if uni["checkJs"] != ctx["configProjection"]["honoredOptions"]["checkJs"]:
                    self.bad("native.universe-context-field-mismatch", "checkJs")
                if uni["nodeModulesInReadSet"] != (ctx["nodeModulesLayoutDigest"] is not None):
                    self.bad("native.universe-context-field-mismatch",
                             "nodeModulesInReadSet")
                lk = "none" if ctx["lockfileIdentity"] is None else ctx["lockfileIdentity"]["kind"]
                if uni["lockfileKind"] != lk:
                    self.bad("native.universe-context-field-mismatch", "lockfileKind")
            if udom == "native.semantic-universe.syntax.v2":
                have = {g["grammarId"] for g in ctx["grammarBundle"]["grammars"]}
                for gid in uni["selectedGrammarIds"]:
                    if gid not in have:
                        self.bad("native.syntax-grammar-not-in-bundle", gid)
            if udom == "native.semantic-universe.rust.v2":
                base = set(ctx["baseCfg"])
                seen = set()
                for cs in uni["cfgSets"]:
                    if cs["cfgSetId"] in seen:
                        self.bad("RUST_CFGSET_DUPLICATE", cs["cfgSetId"])
                    seen.add(cs["cfgSetId"])
                    if not base <= set(cs["cfg"]):
                        self.bad("RUST_CFGSET_DROPS_BASE", cs["cfgSetId"])
                for f in ("rustflags", "preparedResolution", "executionCapableResolution"):
                    pass
                if uni["configProjectionSha256"] != H(
                        "native.cargo-config-projection.v2", ctx["configProjection"]):
                    self.bad("native.universe-context-field-mismatch",
                             "configProjectionSha256")
                if uni["executionCapableResolution"] != (uni["preparedResolution"] != "none"):
                    self.bad("RUST_EXECUTION_CAPABLE_RESOLUTION_INCONSISTENT")
                need = UNIVERSE_ROWS[udom]["preparedResolutionGrantOperations"][
                    uni["preparedResolution"]]
                if need and grant and need not in grant["analysisOperations"]:
                    self.bad("PREPARED_RESOLUTION_WITHOUT_GRANT_OPERATION", need)
                dss = nested.get("dependencySourceSet")
                if dss is not None:
                    if C(dss["lockfileIdentity"]) != C(uni["lockfileIdentity"]):
                        self.bad("DEPENDENCY_SET_LOCKFILE_DISAGREES")
                    for pkg in dss["packages"]:
                        fm = self.frame(pkg["fileManifestSha256"], "native-nested",
                                        "dependency-file-manifest")
                        if fm:
                            for r in fm[1]:
                                if r["contentSha256"] not in self.w.cas:
                                    self.bad("DEPENDENCY_MEMBER_NOT_RETAINED", r["path"])
                                elif len(self.w.cas[r["contentSha256"]]) != r["byteLength"]:
                                    self.bad("DEPENDENCY_MEMBER_LENGTH", r["path"])
                uf = nested.get("unifiedFeatures")
                if uf is not None and uf["targetTriple"] != ctx["targetTriple"]:
                    self.bad("UNIFIED_FEATURES_TARGET_MISMATCH")
                own = nested.get("sourceUnitOwnership")
                if own is not None:
                    declared = set()
                    for u in own["units"]:
                        got_id, pre = unit_id(u["markerPath"], u["targetKind"],
                                              u["targetName"])
                        if got_id != u["unitId"]:
                            self.bad("SOURCE_UNIT_OWNERSHIP_UNIT_ID_NOT_DERIVED",
                                     u["unitId"])
                        declared.add(u["unitId"])
                        if u["markerPath"] not in inv_by_path:
                            self.bad("OWNERSHIP_MARKER_OUTSIDE_SNAPSHOT", u["markerPath"])
                        if u["targetEdition"] is None and \
                                u["crateName"] not in uni["edition"]:
                            self.bad("OWNERSHIP_DEFERRING_UNIT_CRATE_NOT_IN_EDITION_MAP",
                                     u["crateName"])
                    for s in own["selectedUnitIds"]:
                        if s not in declared:
                            self.bad("OWNERSHIP_SELECTION_UNDECLARED_UNIT", s)
                    for r in own["ownership"]:
                        if r["unitId"] not in declared:
                            self.bad("OWNERSHIP_ROW_UNDECLARED_UNIT", r["unitId"])
                        if r["path"] not in inv_by_path:
                            self.bad("OWNERSHIP_PATH_OUTSIDE_SNAPSHOT", r["path"])
            universes[uhx] = (udom, uni, cbare, ctx, nested)

        # --- context set equality: the set of RETAINED context frames must
        # equal plan.nativeContextDigests exactly (identity S3).
        self.checks += 1
        retained_ctx = {hx for hx, (dom, _) in w.frames.items()
                        if dom in CONTEXT_ROWS}
        if retained_ctx != set(plan["nativeContextDigests"]):
            self.bad("PLAN_CONTEXT_SET_MISMATCH",
                     "retained=%d plan=%d" % (len(retained_ctx),
                                              len(plan["nativeContextDigests"])))

        # --- facts ---------------------------------------------------------
        facts = {}
        for key, desc in sorted(w.objects.items()):
            if not key.startswith("fact2:"):
                continue
            facts[key] = desc
            self.schema("identity", "#/$defs/fact", desc, "fact")
            self.check_fact(key, desc, plan, run, inv_by_path, universes,
                            closures)

        # --- subject scopes -------------------------------------------------
        scopes = {}
        for key, desc in sorted(w.objects.items()):
            if not key.startswith("scope2:"):
                continue
            scopes[key] = desc
            self.schema("identity", "#/$defs/subject-scope", desc, "subject-scope")
            self.checks += 1
            if desc["snapshotId"] != run["snapshotId"]:
                self.bad("REFERENCE_SOURCE_JOIN", key)
            if desc["enumeratorClosure"] not in plan["semanticClosures"]:
                self.bad("SCOPE_ENUMERATOR_NOT_PLAN_SELECTED", key)
            elif closures.get(desc["enumeratorClosure"], {}).get("kind") != "provider":
                self.bad("SCOPE_ENUMERATOR_CLOSURE_KIND", key)
            self.check_pair(desc["relation"], desc["resolution"], "scope " + key)
            if len(set(desc["subjects"])) != len(desc["subjects"]):
                self.bad("SUBJECT_SCOPE_DUPLICATE_SUBJECT", key)
            # syntax-universe capability guard, boundary (3)
            self.syntax_scope_guard(desc, universes, inv_by_path, key)

        # --- coverage -------------------------------------------------------
        coverages = {}
        for key, desc in sorted(w.objects.items()):
            if not key.startswith("coverage2:"):
                continue
            coverages[key] = desc
            self.schema("identity", "#/$defs/coverage", desc, "coverage")
            payload = self.canonical_record(desc["payloadDigest"], "native",
                                            "#/$defs/CoverageResultV3",
                                            "coverage-payload")
            if payload is None:
                continue
            self.checks += 1
            if desc["payloadSchemaDigest"] != NATIVE_DOC_DIGEST:
                self.bad("native.coverage-payload-schema-not-registered", key)
            sc = scopes.get(desc["scopeId"])
            if sc is None:
                self.bad("COVERAGE_SCOPE_NOT_RETAINED", key)
                continue
            self.check_coverage(key, desc, payload, sc, universes, facts,
                                inv_by_path)

        # --- views ----------------------------------------------------------
        for key, desc in sorted(w.objects.items()):
            if not key.startswith("view2:"):
                continue
            self.schema("identity", "#/$defs/view", desc, "view")
            self.checks += 1
            if desc["planId"] != run["planId"]:
                self.bad("VIEW_PLAN_JOIN", key)
            if desc["producerClosure"] not in plan["semanticClosures"]:
                self.bad("VIEW_PRODUCER_NOT_PLAN_SELECTED", key)
            for d in desc["schemaDigests"]:
                if d not in w.cas:
                    self.bad("VIEW_SCHEMA_DOCUMENT_NOT_RETAINED", d)
            for cid in desc["coverageIds"]:
                cov = coverages.get(cid)
                if cov is None:
                    self.bad("native.coverage-not-admitted-at-producer-boundary", cid)
                elif cov["scopeId"] not in desc["scopeIds"]:
                    self.bad("native.coverage-subject-scope-outside-view", cid)
            # existential fact/scope join
            for fid in desc["facts"]:
                f = facts.get(fid)
                if f is None:
                    self.bad("VIEW_FACT_NOT_RETAINED", fid)
                    continue
                if not any(scopes[s]["relation"] == f["relation"]
                           and scopes[s]["resolution"] == f["resolution"]
                           and scopes[s]["sourceUniverse"] == f["sourceUniverse"]
                           and scopes[s]["targetUniverse"] == f["targetUniverse"]
                           for s in desc["scopeIds"] if s in scopes):
                    self.bad("VIEW_FACT_HAS_NO_MATCHING_SCOPE", fid)
            # coveragePartitionLaw: disjointness within the full owning tuple
            byk = {}
            for s in desc["scopeIds"]:
                sc = scopes.get(s)
                if sc is None:
                    self.bad("VIEW_SCOPE_NOT_RETAINED", s)
                    continue
                k = tuple(sc[f] for f in REL["coveragePartitionLaw"]["partitionKey"])
                for other in byk.get(k, []):
                    ov = set(other["subjects"]) & set(sc["subjects"])
                    if ov:
                        self.bad("SUBJECT_SCOPE_PARTITION_OVERLAP",
                                 "%s %s %s" % (sc["relation"], sc["resolution"],
                                               sorted(ov)[0]))
                byk.setdefault(k, []).append(sc)
            # coverageTotalityLaw over this view's own facts
            for cid in desc["coverageIds"]:
                cov = coverages.get(cid)
                if not cov:
                    continue
                pl = self.canonical_record(cov["payloadDigest"], None, None, "cov")
                sc = scopes.get(cov["scopeId"])
                if not pl or not sc:
                    continue
                row = RELATIONS.get(sc["relation"], {})
                tot = row.get("coverageTotality")
                if not tot or sc["resolution"] != tot["rung"]:
                    continue
                if pl["entry"]["coverage"] != "complete":
                    continue
                for subj in sc["subjects"]:
                    if subj not in inv_by_path:
                        continue
                    found = False
                    for fid in desc["facts"]:
                        f = facts.get(fid)
                        if not f:
                            continue
                        if all(f[c] == sc[c] for c in tot["matchOn"]
                               if c in f and c in sc):
                            fp = self.canonical_record(f["payloadDigest"], None,
                                                       None, "fp")
                            if fp and fp.get(tot["pathField"]) == subj:
                                found = True
                                break
                    if not found:
                        self.bad("COVERAGE_INVENTORY_TOTALITY_OMITS_PATH", subj)

        # --- evidence / seal roots -----------------------------------------
        view_cov = set()
        for vid in ev["viewIds"]:
            v = w.objects.get(vid)
            if v is None:
                self.bad("EVIDENCE_VIEW_NOT_RETAINED", vid)
                continue
            view_cov |= set(v["coverageIds"])
        self.checks += 1
        if set(ev["coverageIds"]) != view_cov:
            self.bad("EVIDENCE_COVERAGE_ROOTS_NOT_VIEW_UNION")
        if set(ev["importIds"]) != set(plan["importIds"]):
            self.bad("EVIDENCE_IMPORTS_NOT_PLAN_SELECTED")

        # --- proof / witnesses / rule program ------------------------------
        self.check_proof(proof, plan, w, facts, coverages)
        return self.errs

    # ------------------------------------------------------------------
    def check_pair(self, relation, rung, label):
        self.checks += 1
        row = RELATIONS.get(relation)
        if row is None:
            self.bad("RELATION_NOT_REGISTERED", "%s (%s)" % (relation, label))
            return False
        if not row.get("ladder"):
            self.bad("RELATION_LADDER_MISSING", relation)
            return False
        if rung not in row["ladder"]:
            self.bad("RELATION_RUNG_NOT_ON_LADDER",
                     "%s@%s (%s)" % (relation, rung, label))
            return False
        return True

    def check_fact(self, key, f, plan, run, inv_by_path, universes, closures):
        self.checks += 1
        if f["snapshotId"] != run["snapshotId"]:
            self.bad("REFERENCE_SOURCE_JOIN", key)
        if f["producerClosure"] not in plan["semanticClosures"]:
            self.bad("FACT_PRODUCER_NOT_PLAN_SELECTED", key)
        elif closures.get(f["producerClosure"], {}).get("kind") != "provider":
            self.bad("FACT_PRODUCER_CLOSURE_KIND", key)
        if not self.check_pair(f["relation"], f["resolution"], "fact " + key):
            return
        row = RELATIONS[f["relation"]]
        if f["payloadSchemaDigest"] != REL_DOC_DIGEST:
            self.bad("FACT_PAYLOAD_SCHEMA_NOT_THE_RELATION_DOCUMENT", key)
        payload = self.canonical_record(f["payloadDigest"], "relation",
                                        row["selector"], "payload " + key)
        if payload is None:
            return
        # per-rung required/forbidden payload fields
        rr = row.get("rungs", {}).get(f["resolution"])
        if rr:
            for need in rr.get("required", []):
                if need not in payload:
                    self.bad("FACT_RUNG_REQUIRED_FIELD_MISSING",
                             "%s %s" % (key, need))
            for forb in rr.get("forbidden", []):
                if forb in payload:
                    self.bad("FACT_RUNG_FORBIDDEN_FIELD_PRESENT",
                             "%s %s" % (key, forb))
        if row["universeRule"] == "same-only" and \
                f["sourceUniverse"] != f["targetUniverse"]:
            self.bad("FACT_UNIVERSE_RULE_SAME_ONLY", key)
        # anchorLaw
        al = row["anchorLaw"]
        n = len(f["anchors"])
        if "cardinality" in al and n != al["cardinality"]:
            self.bad("FACT_ANCHOR_CARDINALITY",
                     "%s %s expected %d got %d" % (key, f["relation"],
                                                   al["cardinality"], n))
        if "minimum" in al and n < al["minimum"]:
            self.bad("FACT_ANCHOR_CARDINALITY",
                     "%s %s expected >=%d got %d" % (key, f["relation"],
                                                     al["minimum"], n))
        # anchors must name inventoried blobs and lie inside them
        for a in f["anchors"]:
            if a["path"] not in inv_by_path:
                self.bad("ANCHOR_SOURCE", a["path"])
                continue
            if inv_by_path[a["path"]]["sha256"] != a["blobDigest"]:
                self.bad("ANCHOR_SOURCE", a["path"] + " digest")
                continue
            b = self.w.cas.get(a["blobDigest"])
            if not (a["startByte"] <= a["endByte"] <= len(b)):
                self.bad("ANCHOR_RANGE", a["path"])
                continue
            try:
                b[a["startByte"]:a["endByte"]].decode("utf-8")
            except UnicodeDecodeError:
                self.bad("ANCHOR_UTF8", a["path"])
        # snapshotJoins
        for sj in row.get("snapshotJoins", []):
            if "unless" in sj and payload.get(sj["unless"]["field"]) == \
                    sj["unless"]["equals"]:
                continue
            p = payload[sj["pathField"]]
            if p not in inv_by_path:
                self.bad("RELATION_SNAPSHOT_JOIN_PATH", "%s %s" % (key, p))
                continue
            if sj["form"] == "inventoried-file":
                if payload[sj["digestField"]] != inv_by_path[p]["sha256"]:
                    self.bad("RELATION_SNAPSHOT_JOIN_DIGEST", "%s %s" % (key, p))
                if payload[sj["lengthField"]] != inv_by_path[p]["bytes"]:
                    self.bad("RELATION_SNAPSHOT_JOIN_LENGTH", "%s %s" % (key, p))
                if payload[sj["digestField"]] not in self.w.cas:
                    self.bad("RELATION_SNAPSHOT_JOIN_BYTES_NOT_RETAINED", p)
                if "anchorPathField" in sj:
                    for a in f["anchors"]:
                        if a["path"] != payload[sj["anchorPathField"]]:
                            self.bad("RELATION_ANCHOR_PATH_FIELD", key)
        # syntax-universe capability guard, boundary (2)
        u = universes.get(f["sourceUniverse"])
        if u and u[0] == "native.semantic-universe.syntax.v2":
            self.syntax_fact_guard(f, u, key)
        # clones body-identity join
        if f["relation"] == "clones":
            self.check_clone_body(key, f, payload, universes, inv_by_path)

    # ------------------------------------------------------------------
    def syntax_fact_guard(self, f, u, key):
        udom, uni, cbare, ctx, nested = u
        cap = "%s@%s" % (f["relation"], f["resolution"])
        if f["relation"] in ("file", "package", "vcs-change"):
            return                        # inventory relations are exempt
        selected = [g for g in ctx["grammarBundle"]["grammars"]
                    if g["grammarId"] in uni["selectedGrammarIds"]]
        for a in f["anchors"]:
            owners = [g for g in selected
                      if longest_suffix(g["suffixes"], a["path"]) is not None]
            if not owners:
                self.bad("SYNTAX_CAPABILITY_UNSUPPORTED_FACT",
                         "%s no selected grammar reads %s" % (key, a["path"]))
                continue
            best = max(owners,
                       key=lambda g: len(longest_suffix(g["suffixes"], a["path"])))
            caps = GRAMMAR_REG["languages"][best["languageId"]]["capabilities"]
            if cap not in caps:
                self.bad("SYNTAX_CAPABILITY_UNSUPPORTED_FACT",
                         "%s %s on %s (%s)" % (key, cap, a["path"],
                                               best["languageId"]))

    def syntax_scope_guard(self, sc, universes, inv_by_path, key):
        u = universes.get(sc["sourceUniverse"])
        if not u or u[0] != "native.semantic-universe.syntax.v2":
            return
        udom, uni, cbare, ctx, nested = u
        cap = "%s@%s" % (sc["relation"], sc["resolution"])
        if sc["relation"] in ("file", "package", "vcs-change"):
            return                        # always available, never grammar-gated
        selected = [g for g in ctx["grammarBundle"]["grammars"]
                    if g["grammarId"] in uni["selectedGrammarIds"]]
        code = [g for g in selected if g["syntaxClass"] == "code"]
        row = RELATIONS[sc["relation"]]
        available = False
        if row.get("subjectKind") == "source-path" or sc["relation"] in (
                "clones", "file", "vcs-change"):
            # judged on the scope's OWN named paths: every one must be supported
            available = bool(sc["subjects"]) and all(
                any(longest_suffix(g["suffixes"], p) is not None
                    and cap in GRAMMAR_REG["languages"][g["languageId"]]["capabilities"]
                    for g in selected)
                for p in sc["subjects"])
        else:
            # symbol relations: coarser question over the committed extent
            available = any(
                longest_suffix(g["suffixes"], p) is not None
                and cap in GRAMMAR_REG["languages"][g["languageId"]]["capabilities"]
                for g in code for p in inv_by_path)
        self._syntax_available = getattr(self, "_syntax_available", {})
        self._syntax_available[key] = available

    def check_coverage(self, cid, cov, payload, sc, universes, facts, inv_by_path):
        entry = payload["entry"]
        keyrec = payload["key"]
        self.checks += 1
        # commitment == the scope2 identity, in native Sha256Text form
        commit = "sha256:" + H("subject-scope", sc)
        if keyrec["subjectScopeCommitment"] != commit:
            self.bad("native.subject-scope-commitment-mismatch", cid)
        for f in ("relation", "resolution", "sourceUniverse", "targetUniverse"):
            if keyrec[f] != sc[f]:
                self.bad("native.coverage-key-scope-mismatch", f)
        if entry["examinedUniverse"]["subjectScopeCommitment"] != commit:
            self.bad("native.examined-universe-commitment-mismatch", cid)
        if entry["examinedUniverse"]["subjectCount"] != len(sc["subjects"]):
            self.bad("native.examined-universe-subject-count-mismatch", cid)
        if entry["relation"] != sc["relation"] or entry["resolution"] != sc["resolution"]:
            self.bad("native.coverage-entry-key-mismatch", cid)
        # RC-0
        if not self.check_pair(entry["relation"], entry["resolution"],
                               "coverage " + cid):
            return
        rc = entry["resolutionCompleteness"]
        resolved = entry["resolution"] in RESOLVED_RUNGS
        # RC-1
        if resolved:
            if rc["state"] == "not-applicable":
                self.bad("RC1_NOT_APPLICABLE_ON_RESOLVED_RUNG", cid)
        else:
            if rc["state"] != "not-applicable":
                self.bad("RC1_NON_RESOLVED_RUNG_STATE", "%s %s" % (cid, rc["state"]))
            if rc["attempted"] is not False:
                self.bad("RC1_NON_RESOLVED_RUNG_ATTEMPTED", cid)
            if rc["unresolvedEdgeCount"] != 0:
                self.bad("RC1_NON_RESOLVED_RUNG_EDGE_COUNT", cid)
            if rc["unresolvedEdgeClasses"]:
                self.bad("RC1_NON_RESOLVED_RUNG_EDGE_CLASSES", cid)
        # RC-2
        if resolved:
            edges = [f for f in facts.values()
                     if f["relation"] == "unresolved-edge"
                     and f["sourceUniverse"] == sc["sourceUniverse"]]
            matching = []
            for f in edges:
                p = self.canonical_record(f["payloadDigest"], None, None, "ue")
                if p and p["relation"] == entry["relation"]:
                    matching.append(p)
            if rc["state"] == "complete":
                if not (rc["attempted"] and rc["examinedExhaustive"]
                        and rc["stageTerminal"] == "complete" and not matching):
                    self.bad("RC2_COMPLETE_PRECONDITIONS", cid)
            if rc["state"] == "incomplete" and not matching:
                self.bad("RC2_INCOMPLETE_NEEDS_AN_EDGE", cid)
            if set(rc["unresolvedEdgeClasses"]) != {p["edgeKind"] for p in matching}:
                self.bad("RC2_EDGE_CLASSES_NOT_EQUAL_TO_ADMITTED_EDGES", cid)
            if rc["state"] == "not-attempted" and (
                    rc["attempted"] or rc["unresolvedEdgeCount"] != 0):
                self.bad("RC2_NOT_ATTEMPTED_PRECONDITIONS", cid)
        # deficiency/cause pairing
        self.check_cause(cid, entry)
        # clones ownership disclosure (native S10 / S11 scopeVersusEnumeration):
        # Run closure RE-DERIVES the owed (deficiency, nativeCause) from the
        # committed ownership record and THIS scope's own subjects, in the
        # selection law's order, and refuses a mismatch.
        self.check_clone_dialect_prerequisite(cid, entry, sc, universes)

        # syntax capability disclosure
        av = getattr(self, "_syntax_available", {}).get(cov["scopeId"])
        if av is not None and av is False:
            if entry["coverage"] != "unknown":
                self.bad("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE", cid)
            if entry["deficiency"] != "language-tier-unsupported":
                self.bad("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE_DEFICIENCY_MISMATCH", cid)
            if entry["nativeCause"] != "capability-missing":
                self.bad("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE_CAUSE_MISMATCH", cid)

    def check_clone_dialect_prerequisite(self, cid, entry, sc, universes):
        if sc["relation"] != "clones":
            return
        u = universes.get(sc["sourceUniverse"])
        if u is None:
            return
        udom, uni, cbare, ctx, nested = u
        d = UNIVERSE_ROWS[udom]["languageVersionBinding"]["dialect"]
        if d["form"] != "selected-compilation-target-edition":
            return
        self.checks += 1
        owed = None
        own = nested.get("sourceUnitOwnership")
        if own is None:
            owed = ("input-closure-incomplete", "body-language-ownership-missing")
        elif own["enumeration"] == "partial":
            owed = ("input-closure-incomplete", "body-language-owner-unenumerated")
        else:
            sel = set(own["selectedUnitIds"])
            units = {x["unitId"]: x for x in own["units"]}
            for subj in sc["subjects"]:
                rows = [r for r in own["ownership"]
                        if r["path"] == subj and r["unitId"] in sel]
                eff = set()
                for r in rows:
                    x = units[r["unitId"]]
                    eff.add(x["targetEdition"] if x["targetEdition"] is not None
                            else uni["edition"].get(x["crateName"]))
                if len(eff) > 1:
                    owed = ("input-closure-incomplete",
                            "body-language-owner-ambiguous")
                    break
        if owed is None:
            return
        if entry["coverage"] != "unknown":
            self.bad("COVERAGE_DIALECT_PREREQUISITE",
                     "%s claims %s while a body dialect is undeterminable"
                     % (cid, entry["coverage"]))
        if entry["deficiency"] is None:
            self.bad("COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED", cid)
        elif entry["deficiency"] != owed[0]:
            self.bad("COVERAGE_DIALECT_DEFICIENCY_MISMATCH",
                     "%s %s != %s" % (cid, entry["deficiency"], owed[0]))
        if entry["nativeCause"] != owed[1]:
            self.bad("COVERAGE_DIALECT_CAUSE_MISMATCH",
                     "%s %s != %s" % (cid, entry["nativeCause"], owed[1]))

    def check_cause(self, cid, entry):
        """native S10 + native-evidence.schemas.v2 #/x-opensip-deficiency-cause-registry."""
        self.checks += 1
        d, c = entry["deficiency"], entry["nativeCause"]
        if d is None:
            if c is not None:
                self.bad("native.coverage-cause-without-deficiency", cid)
            return
        row = CAUSE_REG["deficiencies"].get(d)
        if row is None:
            self.bad("native.coverage-cause-registry-row-missing", d)
            return
        mode = row["nativeCause"]
        if mode == "required":
            if c is None:
                self.bad("native.coverage-cause-required", "%s:%s" % (cid, d))
            elif c not in row["allowedCauses"]:
                self.bad("native.coverage-cause-not-for-deficiency", "%s:%s" % (d, c))
        elif mode == "optional":
            if c is not None and c not in row["allowedCauses"]:
                self.bad("native.coverage-cause-not-for-deficiency", "%s:%s" % (d, c))
        elif mode == "must-be-null":
            if c is not None:
                self.bad("native.coverage-cause-must-be-null", "%s:%s" % (cid, d))
        if "relations" in row and entry["relation"] not in row["relations"]:
            self.bad("native.coverage-cause-relation-not-in-scope",
                     "%s on %s" % (d, entry["relation"]))
        req = row.get("requires")
        if req:
            v = entry
            for p in req["path"]:
                v = v[p]
            if v != req["equals"]:
                self.bad("native.coverage-cause-carrier-unsupported", d)
        one = row.get("oneOf")
        if one:
            v = entry
            for p in one["path"]:
                v = v[p]
            if v not in one["members"]:
                self.bad("native.coverage-cause-carrier-unsupported", d)
        con = row.get("contains")
        if con:
            v = entry
            for p in con["path"]:
                v = v[p]
            if con["member"] not in v:
                self.bad("native.coverage-cause-carrier-unsupported", d)

    # ------------------------------------------------------------------
    def check_clone_body(self, key, f, payload, universes, inv_by_path):
        self.checks += 1
        u = universes.get(f["sourceUniverse"])
        if u is None:
            self.bad("CLONE_UNIVERSE_NOT_RETAINED", key)
            return
        udom, uni, cbare, ctx, nested = u
        if len(f["anchors"]) != 1:
            return                      # already reported by anchorLaw
        a = f["anchors"][0]
        # the frame is retained under the 64-hex suffix
        suffix = payload["bodyIdentity"].split(":", 1)[1]
        try:
            fr = self.w.cas.get(suffix)
        except Refused:
            self.bad("CLONE_BODY_FRAME_NOT_RETAINED", key)
            return
        if sha256hex(fr) != suffix:
            self.bad("CLONE_BODY_FRAME_DIGEST", key)
            return
        comps, payload_bytes = _parse_body_frame(fr)
        if comps is None:
            self.bad("CLONE_BODY_FRAME_MALFORMED", key)
            return
        tag, level_id, level_ver, lang_id, lang_ver = comps
        if tag != b"opensip.fact-identity.v1":
            self.bad("CLONE_BODY_FRAME_DOMAIN_TAG", key)
        if level_id.decode() != payload["normalisationLevel"]:
            self.bad("CLONE_BODY_LEVEL_ID_MISMATCH", key)
        if level_ver != bytes.fromhex(payload["normalisationVersion"]):
            self.bad("CLONE_BODY_LEVEL_VERSION_MISMATCH", key)
        if payload["normalisationVersion"] not in self.w.cas:
            self.bad("CLONE_LEVEL_SPECIFICATION_NOT_RETAINED", key)
        try:
            blv, language_id = body_language_version(
                self.w, udom, uni, ctx, a["path"], nested)
        except DialectRefusal as r:
            self.bad(r.code, "%s %s" % (key, a["path"]))
            return
        if lang_id.decode() != language_id:
            self.bad("CLONE_BODY_LANGUAGE_ID_MISMATCH",
                     "%s %s!=%s" % (key, lang_id.decode(), language_id))
        want_lv = hashlib.sha256(C(blv)).digest()
        if lang_ver != want_lv:
            self.bad("CLONE_BODY_LANGUAGE_VERSION_MISMATCH", key)
        # body-language-version is a DERIVED record and is retained too
        if raw_digest(blv) not in self.w.cas:
            self.bad("BODY_LANGUAGE_VERSION_RECORD_NOT_RETAINED", key)
        else:
            self.schema("identity", "#/$defs/body-language-version", blv, "blv")
        # L0: the host RECOMPUTES the payload from the enclosing fact anchor
        if payload["normalisationLevel"] == "L0-verbatim":
            span = self.w.cas.get(a["blobDigest"])[a["startByte"]:a["endByte"]]
            if payload_bytes != O.body_payload_L0(span):
                self.bad("CLONE_L0_PAYLOAD_NOT_THE_ANCHOR_SPAN", key)
        else:
            # L1-L3: custody + framing only
            if not _wellformed_token_stream(payload_bytes):
                self.bad("CLONE_TOKEN_STREAM_FRAMING", key)

    # ------------------------------------------------------------------
    def check_proof(self, proof, plan, w, facts, coverages):
        rp = self.canonical_record(proof["ruleProgramDigest"], "policy-document",
                                   "#/$defs/RuleProgramV1", "rule-program")
        pol = self.canonical_record(plan["policyDigest"], "policy-document",
                                    "#/$defs/PolicyDocumentV1", "policy")
        self.canonical_record(plan["waiverDigest"], "policy-document",
                              "#/$defs/WaiverSetV1", "waivers")
        if rp is None or pol is None:
            return
        self.checks += 1
        if rp["policyDigest"] != plan["policyDigest"]:
            self.bad("RULE_PROGRAM_POLICY_DIGEST")
        expect = {"schemaVersion": 1, "policyDigest": plan["policyDigest"],
                  "rules": [{"ruleId": r["ruleId"],
                             "ruleProgramRef": r["ruleProgramRef"],
                             "emitWhen": r["emitWhen"]} for r in pol["rules"]]}
        if C(rp) != C(expect):
            self.bad("RULE_PROGRAM_NOT_THE_POLICY_PROJECTION")
        # minResolution must be a rung of THAT atom's relation ladder
        for src, label in ((pol, "policy"), (rp, "rule-program")):
            for r in src["rules"]:
                for addr, node in _walk_predicate(r["emitWhen"], "p"):
                    if node["op"] in ("and", "or", "not"):
                        continue
                    self.checks += 1
                    rel, mr = node["relation"], node["minResolution"]
                    row = RELATIONS.get(rel)
                    if row is None:
                        if rel not in ("runtime-observation", "history-change"):
                            self.bad("ATOM_RELATION_UNREGISTERED",
                                     "%s %s" % (label, rel))
                        continue
                    if mr not in row["ladder"]:
                        self.bad("ATOM_MIN_RESOLUTION_NOT_ON_RELATION_LADDER",
                                 "%s %s@%s" % (label, rel, mr))
        # predicate proofs address real nodes
        by_rule = {r["ruleId"]: r for r in rp["rules"]}
        proven = set()
        for pp in proof["predicateProofs"]:
            self.checks += 1
            r = by_rule.get(pp["ruleId"])
            if r is None:
                self.bad("PREDICATE_PROOF_UNKNOWN_RULE", pp["ruleId"])
                continue
            node = _address(r["emitWhen"], pp["predicateId"])
            if node is None:
                self.bad("PREDICATE_PROOF_UNADDRESSABLE_NODE", pp["predicateId"])
                continue
            if node["op"] != pp["operation"]:
                self.bad("PREDICATE_PROOF_OPERATION_MISMATCH", pp["predicateId"])
            wit = self.canonical_record(pp["witnessDigest"], "identity",
                                        "#/$defs/predicate-witness", "witness")
            if wit is None:
                continue
            ppd = {"schemaVersion": 2,
                   "ruleProgramDigest": proof["ruleProgramDigest"],
                   "ruleId": pp["ruleId"], "predicateId": pp["predicateId"],
                   "operation": pp["operation"],
                   "nodeDigest": raw_digest(node)}
            self.schema("identity", "#/$defs/program-predicate", ppd, "program-predicate")
            if raw_digest(ppd) != wit["programPredicateDigest"]:
                self.bad("PROGRAM_PREDICATE_DIGEST_MISMATCH", pp["predicateId"])
            if raw_digest(ppd) not in self.w.cas:
                self.bad("PROGRAM_PREDICATE_RECORD_NOT_RETAINED", pp["predicateId"])
            want_children = _child_addresses(node, pp["predicateId"])
            if sorted(wit["childPredicateIds"]) != sorted(want_children):
                self.bad("WITNESS_CHILDREN_NOT_THE_OPERAND_ADDRESSES",
                         pp["predicateId"])
            if pp["operation"] == "count-at-most":
                if wit["countLimit"] != node.get("n"):
                    self.bad("WITNESS_COUNT_LIMIT", pp["predicateId"])
            elif wit["countLimit"] is not None:
                self.bad("WITNESS_COUNT_LIMIT_NOT_NULL", pp["predicateId"])
            for fid in wit["matchingFactIds"]:
                if fid not in facts:
                    self.bad("WITNESS_FACT_NOT_RETAINED", fid)
            for cid in wit["coverageIds"]:
                if cid not in coverages:
                    self.bad("WITNESS_COVERAGE_NOT_RETAINED", cid)
            for r2 in pp["inputRefs"]:
                if r2 not in proof["evaluationInputRefs"]:
                    self.bad("PREDICATE_INPUT_NOT_IN_EVALUATION_INPUTS",
                             pp["predicateId"])
            proven.add((pp["ruleId"], pp["predicateId"]))
        for pp in proof["predicateProofs"]:
            wit = self.canonical_record(pp["witnessDigest"], None, None, "w2")
            if not wit:
                continue
            for ch in wit["childPredicateIds"]:
                if (pp["ruleId"], ch) not in proven:
                    self.bad("WITNESS_CHILD_NOT_PROVEN_FOR_SAME_RULE", ch)


# ---------------------------------------------------------------------------
def _docname(document):
    m = {"native/native-evidence.schemas.v2.json": "native",
         "foundation/relation-payload-schemas.v2.json": "relation",
         "foundation/identity-schemas.v2.json": "identity",
         "workflows/schemas/policy-document.schema.json": "policy-document",
         "workflows/schemas/imported-evidence.schema.json": "imported-evidence",
         "workflows/schemas/test-execution.schema.json": "test-execution",
         "foundation/import-source-context.schema.json": "import-source-context"}
    return m[document]


def _config_node_kind(path):
    """native S2.2 / x-opensip-config-node-kind-law: exact basename table."""
    base = path.rsplit("/", 1)[-1]
    if base == "tsconfig.json":
        return "tsconfig"
    if base == "jsconfig.json":
        return "jsconfig"
    return "other"


def _fold(n):
    """The published fold is Unicode Default Case Conversion toLowercase(X).
    Every lib name in the pinned compiler's option vocabulary is ASCII, where
    the three candidate operations coincide; Python's str.lower() implements
    the full, non-tailored default lowercase mapping (including the U+0130 and
    Final_Sigma cases the contract's discriminator table names)."""
    return n.lower()


def _parse_body_frame(fr):
    i = 0
    comps = []
    try:
        for _ in range(5):
            n = fr[i]
            i += 1
            comps.append(fr[i:i + n])
            i += n
        plen = int.from_bytes(fr[i:i + 4], "big")
        i += 4
        payload = fr[i:i + plen]
        if i + plen != len(fr):
            return None, None
        return tuple(comps), payload
    except Exception:
        return None, None


def _wellformed_token_stream(b):
    try:
        n = int.from_bytes(b[:4], "big")
        i = 4
        for _ in range(n):
            kl = int.from_bytes(b[i:i + 2], "big")
            i += 2 + kl
            vl = int.from_bytes(b[i:i + 4], "big")
            i += 4 + vl
        return i == len(b)
    except Exception:
        return False


def _walk_predicate(node, addr):
    yield addr, node
    if node["op"] in ("and", "or"):
        for i, o in enumerate(node["operands"]):
            for x in _walk_predicate(o, "%s.%d" % (addr, i)):
                yield x
    elif node["op"] == "not":
        for x in _walk_predicate(node["operand"], addr + ".0"):
            yield x


def _address(root, addr):
    for a, n in _walk_predicate(root, "p"):
        if a == addr:
            return n
    return None


def _child_addresses(node, addr):
    if node["op"] in ("and", "or"):
        return ["%s.%d" % (addr, i) for i in range(len(node["operands"]))]
    if node["op"] == "not":
        return [addr + ".0"]
    return []
