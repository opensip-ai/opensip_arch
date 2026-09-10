"""Blind-consumer construction of minimal positive Run descriptor graphs for
TypeScript and for Rust, plus the Run-closure re-admission the identity contract
requires, plus the refusal cases.

Everything here is authored by the blind consumer from the normative prose and
the machine-readable annotations.  Every OS/compiler/provider observation is a
SYNTHETIC TRUSTED OBSERVATION (a stated TCB assumption), never native
enforcement proof.
"""

import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import osref as O
from osref import C, H, RAW, REC, Refuse

SUBJECT = "/tmp/opensip-design-corrections/consumer-b.v2/subject"

NATIVE_SCHEMA_DOC = os.path.join(
    SUBJECT, "docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
IMPORT_SRC_CTX_DOC = os.path.join(
    SUBJECT, "docs/coop/design-corrections/foundation/import-source-context.schema.json")

NATIVE_DOC_BYTES = open(NATIVE_SCHEMA_DOC, "rb").read()
NATIVE_DOC_DIGEST = RAW(NATIVE_DOC_BYTES)


# ------------------------------------------------------------- CAS store ----

class Store(object):
    """One content-addressed store keyed by raw SHA256 (identity 3)."""

    def __init__(self):
        self.objects = {}
        self.kinds = {}
        # Registered schema documents are raw-artifact preimages of every
        # schema digest this graph names, so the closure can fetch them.
        self.put_raw(NATIVE_DOC_BYTES, "registered-schema-document")
        self.put_raw(open(IMPORT_SRC_CTX_DOC, "rb").read(), "registered-schema-document")

    def put_raw(self, blob, label=""):
        d = RAW(blob)
        self.objects[d] = blob
        self.kinds.setdefault(d, "raw-artifact:" + label)
        return d

    def put_record(self, record, label=""):
        return self.put_raw(C(record), "record:" + label)

    def put_frame(self, domain, descriptor, label=""):
        blob = O.frame(domain, descriptor)
        d = hashlib.sha256(blob).hexdigest()
        self.objects[d] = blob
        self.kinds.setdefault(d, "h-frame:" + domain + ":" + label)
        return d

    def get(self, digest):
        if digest not in self.objects:
            # identity 5: a missing promised object is EvidenceUnavailable, the
            # closed operational-failed / HOST.IO_FAILURE / host-io termination
            # with detail evidence.missing -- never a bare lookup error.
            raise Refuse("HOST.IO_FAILURE", "evidence.missing:" + digest)
        return self.objects[digest]


def bare(prefixed_id):
    return prefixed_id.split(":", 1)[1]


def sha_text(hexdigest):
    return "sha256:" + hexdigest


# ------------------------------------------------------------- closures -----

def make_tree(files):
    """files: {logical path: bytes}.  Closure tree hashing includes relative
    path, byte length and digest for every selected file (identity 3)."""
    rows = [{"path": p, "sha256": RAW(b), "bytes": len(b)} for p, b in files.items()]
    rows.sort(key=lambda r: r["path"].encode("utf-8"))
    O.check_order("path", rows, "closure.tree")
    return rows


def build_closure(store, kind, files, semantic_version, protocol_major, platform,
                  manifest_body):
    """closure2: role kind, signed manifest digest, exact executable/data tree,
    semantic version, protocol major and platform."""
    for path, blob in files.items():
        store.put_raw(blob, "closure-tree:" + path)
    manifest_digest = store.put_raw(manifest_body, "component-manifest-body")
    desc = {
        "schemaVersion": 2,
        "kind": kind,
        "manifestDigest": manifest_digest,
        "tree": make_tree(files),
        "semanticVersion": semantic_version,
        "protocolMajor": protocol_major,
        "platform": platform,
    }
    d = store.put_frame("closure", desc, kind)
    return "closure2:" + d, desc


# --------------------------------------------------- foundation aux records --

def build_snapshot(store, project_id, files, scope, vcs_kind, commit, dirty, config):
    inventory = [{"path": p, "sha256": RAW(b), "bytes": len(b)} for p, b in files.items()]
    inventory.sort(key=lambda r: r["path"].encode("utf-8"))
    O.check_order("path", inventory, "source-inventory")
    for p, b in files.items():
        store.put_raw(b, "source:" + p)
    inv_digest = store.put_record(inventory, "source-inventory")
    vcs = {"schemaVersion": 2, "kind": vcs_kind, "commitId": commit, "dirty": dirty,
           "sourceInventoryDigest": inv_digest}
    vcs_digest = store.put_record(vcs, "vcs-observation")
    scope_digest = store.put_record(scope, "scope-descriptor")
    config_digest = store.put_record(config, "semantic-configuration")
    desc = {"schemaVersion": 2, "projectId": project_id, "sourceInventory": inventory,
            "resolvedConfigDigest": config_digest, "scopeDigest": scope_digest,
            "vcsDigest": vcs_digest}
    sid = "snapshot2:" + store.put_frame("snapshot", desc, "snapshot")
    return sid, desc, inventory, scope_digest, config_digest


def inventory_map(inventory):
    return dict((row["path"], row) for row in inventory)


# ------------------------------------------- native context admission -------
# native-evidence sections 2.3 / 2.4 / 3 / 14, reference entry point
# admit_native_context.  Re-implemented by the blind consumer from the prose.

CONTEXT_DOMAIN = {"typescript": "native.context.typescript.v2",
                  "rust": "native.context.rust.v2"}
UNIVERSE_DOMAIN = {"typescript": "native.semantic-universe.typescript.v2",
                   "rust": "native.semantic-universe.rust.v2"}


def _retained_closure(retained, closure_id, want_kind, where):
    """closure2 join: retained, recomputed, right kind (native section 2.4)."""
    if closure_id not in retained["closures"]:
        raise Refuse("native.native-context-closure-unretained", where)
    desc = retained["closures"][closure_id]
    if "closure2:" + H("closure", desc) != closure_id:
        raise Refuse("native.native-context-closure-identity-mismatch", where)
    if desc["kind"] != want_kind:
        raise Refuse("native.native-context-closure-kind-mismatch",
                     "%s: %s != %s" % (where, desc["kind"], want_kind))
    return desc


def admit_native_context(language, ctx, retained, snapshot_inv):
    """Returns an admission record.  Refuses with the native contract's own
    typed refusal string.  Nothing is re-executed."""
    inv = inventory_map(snapshot_inv)
    if language == "typescript":
        tool = _retained_closure(retained, ctx["toolClosure"]["closureId"], "toolchain",
                                 "toolClosure")
        members = dict((r["path"], r["sha256"]) for r in tool["tree"])
        digests = set(members.values())
        for field in ("compiler", "runtime"):
            if ctx["toolClosure"][field] not in digests:
                raise Refuse("native.native-context-tool-not-in-closure", field)
        if ctx["toolchain"]["compilerPackageDigest"] not in digests:
            raise Refuse("native.native-context-tool-not-in-closure", "compilerPackageDigest")
        if ctx["toolchain"]["compilerVersion"] != tool["semanticVersion"]:
            raise Refuse("native.native-context-compiler-version-not-from-manifest",
                         ctx["toolchain"]["compilerVersion"])
        stdlib = _retained_closure(retained,
                                   "closure2:" + ctx["toolchain"]["typescriptStdlibMerkleRoot"],
                                   "stdlib", "typescriptStdlibMerkleRoot")
        # complete .d.ts inventory, basename keyed, no ambiguous basename
        basenames = {}
        for row in stdlib["tree"]:
            if not row["path"].endswith(".d.ts"):
                continue
            b = row["path"].rsplit("/", 1)[-1]
            if b in basenames:
                raise Refuse("native.native-context-stdlib-tree-ambiguous-basename", b)
            basenames[b] = row["sha256"]
        declared = dict((r["component"], r["sha256"])
                        for r in ctx["toolchain"]["standardLibraryComponentDigests"])
        for name in basenames:
            if name not in declared:
                raise Refuse("native.native-context-stdlib-inventory-incomplete", name)
        for name, dig in declared.items():
            if name not in basenames:
                raise Refuse("native.native-context-stdlib-tree-mismatch", name)
            if basenames[name] != dig:
                raise Refuse("native.native-context-stdlib-tree-mismatch", name)
        O.check_order({"by": ["component"]},
                      ctx["toolchain"]["standardLibraryComponentDigests"],
                      "standardLibraryComponentDigests")
        O.check_order("utf8", ctx["toolchain"]["libSelection"], "libSelection")
        sel = ctx["toolchain"]["libSelection"]
        if len(set(s.lower() for s in sel)) != len(sel):
            raise Refuse("native.native-context-lib-not-retained", "case-insensitive duplicate")
        honored_lib = ctx["configProjection"]["honoredOptions"]["lib"]
        if set(s.lower() for s in sel) != set(s.lower() for s in honored_lib):
            raise Refuse("native.native-context-lib-not-retained", "libSelection != honored lib")
        for name in sel:
            if ("lib.%s.d.ts" % name.lower()) not in basenames:
                raise Refuse("native.native-context-lib-not-retained", name)
        if ctx["moduleResolutionMode"] != ctx["configProjection"]["honoredOptions"]["moduleResolution"]:
            raise Refuse("native.universe-context-field-mismatch", "moduleResolutionMode")
        for p in ctx["configProjection"]["configGraphPaths"]:
            if p not in inv:
                raise Refuse("native.native-context-config-path-outside-snapshot", p)
        lock = ctx["lockfileIdentity"]
        if lock is not None:
            row = inv.get(lock["path"])
            if row is None or row["sha256"] != lock["contentSha256"]:
                raise Refuse("native.native-context-lockfile-outside-snapshot", lock["path"])
        dev = _retained_closure  # keep symmetry; TypeScript has no rust-dev-llvm join
    elif language == "rust":
        tool = _retained_closure(retained, ctx["toolClosure"]["closureId"], "toolchain",
                                 "toolClosure")
        members = dict((r["path"], r["sha256"]) for r in tool["tree"])
        digests = set(members.values())
        for field in ("rustc", "cargo", "linker", "ar", "procMacroServer"):
            v = ctx["toolClosure"][field]
            if v is None:
                continue
            if v not in digests:
                raise Refuse("native.native-context-tool-not-in-closure", field)
        if ctx["toolchain"]["rustcVersion"] != tool["semanticVersion"]:
            raise Refuse("native.native-context-compiler-version-not-from-manifest",
                         ctx["toolchain"]["rustcVersion"])
        _retained_closure(retained, "closure2:" + ctx["toolchain"]["rustcDevLlvmDigest"],
                          "rust-dev-llvm", "rustcDevLlvmDigest")
        for p in ctx["configProjection"]["replacedSnapshotConfigs"]:
            if p not in inv:
                raise Refuse("native.native-context-config-path-outside-snapshot", p)
        if ctx["configProjection"]["projectionSha256"] not in retained["blobs"]:
            raise Refuse("native.native-context-projection-bytes-unretained", "projectionSha256")
        for field, want in (("dependencySourceSetId", "native.dependency-source-set.v1"),
                            ("unifiedFeaturesId", "native.unified-features.rust.v1"),
                            ("preparedOutputSetId", "native.prepared-output-set.v3")):
            v = ctx[field]
            if v is None:
                continue
            rec = retained["nested"].get(v)
            if rec is None or rec["domain"] != want:
                raise Refuse("native.nested-identity-unretained", field)
            if sha_text(H(want, rec["record"])) != v:
                raise Refuse("native.nested-identity-mismatch", field)
    else:
        raise Refuse("native.native-context-language-mismatch", str(language))

    domain = CONTEXT_DOMAIN[language]
    ctx_id = H(domain, ctx)
    return {"language": language, "domain": domain, "contextId": ctx_id,
            "nativeContextId": sha_text(ctx_id)}


def bind_typescript_universe(universe, admission, context):
    """native 2.4 / 11.  The retained context bytes are a REQUIRED argument."""
    if context is None:
        raise Refuse("native.universe-context-not-supplied", "typescript")
    if admission is None or admission["language"] != "typescript":
        raise Refuse("native.native-context-language-mismatch", "admission")
    if H("native.context.typescript.v2", context) != admission["contextId"]:
        raise Refuse("native.universe-context-binding-mismatch",
                     "context-bytes-are-not-the-admitted-ones")
    if universe["nativeContextId"] != admission["nativeContextId"]:
        raise Refuse("native.universe-context-binding-mismatch", "nativeContextId")
    checks = {
        "languageMode": context["languageMode"],
        "packageModuleType": context["packageModuleType"],
        "allowJs": context["configProjection"]["honoredOptions"]["allowJs"],
        "checkJs": context["configProjection"]["honoredOptions"]["checkJs"],
        "jsAdmittedToProgram": context["configProjection"]["honoredOptions"]["allowJs"],
        "jsDiagnosticsEnabled": context["configProjection"]["honoredOptions"]["checkJs"],
        "lockfileKind": (context["lockfileIdentity"]["kind"]
                         if context["lockfileIdentity"] else "none"),
        "nodeModulesInReadSet": context["nodeModulesLayoutDigest"] is not None,
    }
    for field, expected in checks.items():
        if universe[field] != expected:
            raise Refuse("native.universe-context-field-mismatch", field)
    # configOrigin: only the synthesized/non-synthesized distinction is derivable
    # from the retained context (empty extends graph).  INVENTED: see report.
    synthesized = (context["configProjection"]["configGraphPaths"] == [])
    if (universe["configOrigin"] == "synthesized") != synthesized:
        raise Refuse("native.universe-context-field-mismatch", "configOrigin")
    if (universe["synthesizedOptions"] is not None) != synthesized:
        raise Refuse("native.universe-context-field-mismatch", "synthesizedOptions")
    if synthesized:
        syn = universe["synthesizedOptions"]
        hon = context["configProjection"]["honoredOptions"]
        for k in ("allowJs", "checkJs", "module", "moduleResolution", "target",
                  "strict", "skipLibCheck", "noEmit"):
            if syn[k] != hon[k]:
                raise Refuse("native.universe-context-field-mismatch", "synthesizedOptions." + k)
        if ("jsx" in syn) != (hon["jsx"] is not None):
            raise Refuse("native.universe-context-field-mismatch", "synthesizedOptions.jsx")
    return {"domain": UNIVERSE_DOMAIN["typescript"],
            "universeId": H(UNIVERSE_DOMAIN["typescript"], universe)}


def bind_rust_universe(universe, admission, context, retained, snapshot_inv):
    """native 2.1 / 11.  All three of context, retained inputs and snapshot
    inventory are REQUIRED: an optional join is not a rule."""
    if context is None or retained is None or snapshot_inv is None:
        raise Refuse("native.universe-retained-inputs-not-supplied", "rust")
    if admission is None or admission["language"] != "rust":
        raise Refuse("native.native-context-language-mismatch", "admission")
    if H("native.context.rust.v2", context) != admission["contextId"]:
        raise Refuse("native.universe-context-binding-mismatch",
                     "context-bytes-are-not-the-admitted-ones")
    if universe["nativeContextId"] != admission["nativeContextId"]:
        raise Refuse("native.universe-context-binding-mismatch", "nativeContextId")
    for field in ("dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"):
        if universe[field] != context[field]:
            raise Refuse("native.universe-context-field-mismatch", field)
    if universe["rustflags"] != context["configProjection"]["rustflags"]:
        raise Refuse("native.universe-context-field-mismatch", "rustflags")
    expected_proj = H("native.cargo-config-projection.v2", context["configProjection"])
    if universe["configProjectionSha256"] != expected_proj:
        raise Refuse("native.universe-context-field-mismatch", "configProjectionSha256")
    if universe["executionCapableResolution"] != (universe["preparedResolution"] != "none"):
        raise Refuse("native.universe-context-field-mismatch", "executionCapableResolution")
    if (universe["preparedOutputSetId"] is None) != (universe["preparedResolution"] == "none"):
        raise Refuse("native.universe-context-field-mismatch", "preparedOutputSetId")
    base = set(context["baseCfg"])
    seen = set()
    for s in universe["cfgSets"]:
        if s["cfgSetId"] in seen:
            raise Refuse("native.universe-context-field-mismatch", "cfgSets:duplicate-cfgSetId")
        seen.add(s["cfgSetId"])
        if not base.issubset(set(s["cfg"])):
            raise Refuse("native.universe-context-field-mismatch", "cfgSets:drops-base-cfg")
    # nested records must be the exact H identity of a retained record and must
    # not contradict the universe or the context
    dep = retained["nested"][universe["dependencySourceSetId"]]["record"]
    if dep["lockfileIdentity"] != universe["lockfileIdentity"]:
        raise Refuse("native.nested-record-contradicts-universe", "dependencySourceSet.lockfile")
    feats = retained["nested"][universe["unifiedFeaturesId"]]["record"]
    if feats["targetTriple"] != context["targetTriple"]:
        raise Refuse("native.nested-record-contradicts-universe", "unifiedFeatures.targetTriple")
    if feats["resolverVersion"] != context["resolverVersion"]:
        raise Refuse("native.nested-record-contradicts-universe", "unifiedFeatures.resolverVersion")
    inv = inventory_map(snapshot_inv)
    lock = universe["lockfileIdentity"]
    row = inv.get(lock["path"])
    if row is None or row["sha256"] != lock["contentSha256"]:
        raise Refuse("native.universe-lockfile-outside-snapshot", lock["path"])
    for p in universe["crateRootPaths"]:
        if p not in inv:
            raise Refuse("native.universe-crate-root-outside-snapshot", p)
    # prepared products are inert; the grant operation is projected by the Plan
    return {"domain": UNIVERSE_DOMAIN["rust"],
            "universeId": H(UNIVERSE_DOMAIN["rust"], universe),
            "requiredGrantOperation": {"host-prepared": "prepare-code",
                                       "imported-inert": "read-import",
                                       "none": None}[universe["preparedResolution"]]}


# ------------------------------------------- coverage producer boundary -----
# native 4.1a admit_coverage_result_v3

def admit_coverage_result_v3(store, host_scope_desc, payload, schema_doc_digest):
    scope_hex = H("subject-scope", host_scope_desc)
    commitment = sha_text(scope_hex)
    key = payload["key"]
    for field, expected in (("relation", host_scope_desc["relation"]),
                            ("resolution", host_scope_desc["resolution"]),
                            ("sourceUniverse", host_scope_desc["sourceUniverse"]),
                            ("targetUniverse", host_scope_desc["targetUniverse"])):
        if key[field] != expected:
            raise Refuse("native.coverage-key-scope-mismatch", field)
    if key["subjectScopeCommitment"] != commitment:
        raise Refuse("native.subject-scope-commitment-mismatch", key["subjectScopeCommitment"])
    entry = payload["entry"]
    if entry["examinedUniverse"]["subjectScopeCommitment"] != key["subjectScopeCommitment"]:
        raise Refuse("native.examined-universe-commitment-mismatch", "")
    if entry["examinedUniverse"]["subjectCount"] != len(host_scope_desc["subjects"]):
        raise Refuse("native.examined-universe-subject-count-mismatch",
                     str(entry["examinedUniverse"]["subjectCount"]))
    if entry["relation"] != key["relation"] or entry["resolution"] != key["resolution"]:
        raise Refuse("native.coverage-entry-key-mismatch", "")
    rc = entry["resolutionCompleteness"]
    if rc["state"] == "complete":
        if not (rc["attempted"] and rc["examinedExhaustive"]
                and rc["stageTerminal"] == "complete" and rc["unresolvedEdgeCount"] == 0):
            raise Refuse("PROVIDER.PROTOCOL_VIOLATION", "RC-2:complete-preconditions")
    if rc["state"] == "not-attempted" and (rc["attempted"] or rc["unresolvedEdgeCount"] != 0):
        raise Refuse("PROVIDER.PROTOCOL_VIOLATION", "RC-2:not-attempted")
    if rc["state"] == "incomplete" and not (rc["unresolvedEdgeCount"] >= 1
                                            and rc["stageTerminal"] == "complete"
                                            and rc["examinedExhaustive"]):
        raise Refuse("PROVIDER.PROTOCOL_VIOLATION", "RC-2:incomplete")
    ONE_RUNG = {"file", "package", "vcs-change", "declares", "literal", "control-flow", "clones"}
    RESOLVED_RUNGS = {"resolved-target", "resolved-binding", "resolved-callee",
                      "checked", "from-resolved-calls"}
    if rc["state"] == "not-applicable":
        if key["relation"] not in ONE_RUNG and key["resolution"] in RESOLVED_RUNGS:
            raise Refuse("PROVIDER.PROTOCOL_VIOLATION", "RC-1:resolved-rung-not-applicable")
    scope_id = "scope2:" + scope_hex
    store.put_frame("subject-scope", host_scope_desc, "subject-scope")
    payload_digest = store.put_record(payload, "CoverageResultV3")
    cov = {"schemaVersion": 2, "scopeId": scope_id,
           "payloadSchemaDigest": schema_doc_digest, "payloadDigest": payload_digest}
    cov_id = "coverage2:" + store.put_frame("coverage", cov, "coverage")
    return cov_id, cov, scope_id, host_scope_desc, commitment
