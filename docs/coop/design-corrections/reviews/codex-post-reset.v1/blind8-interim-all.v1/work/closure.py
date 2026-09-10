"""Independently reconstructed retained-Run closure.

Reconstructed from, and citing, only:
  identity-and-evidence.md sections 3, 4, 5
  identity-schemas.v2.json #/x-opensip-digest-domains, #/x-opensip-payload-registry
  relation-payload-schemas.v2.json #/x-opensip-relation-registry
  native-evidence.md sections 1.2, 2.x, 4.x, 10, 11
  native-evidence.schemas.v2.json #/x-opensip-grammar-capability-registry,
      #/x-opensip-deficiency-cause-registry, #/x-opensip-config-node-kind-law
  native-capability-matrix.v2.json #/capabilityIdLaw
"""
from __future__ import annotations

import hashlib
import json
import struct

import osip
import schemas
from osip import C, H, admit_raw, frame, ident, raw_sha256, record_digest

IDENT = schemas.LOADED["identity"]
RELDOC = schemas.LOADED["relation"]
NATIVE = schemas.LOADED["native"]
MATRIX = json.loads(osip.doc_bytes(
    "docs/coop/design-corrections/native/native-capability-matrix.v2.json").decode())

DIGEST_DOMAINS = IDENT["x-opensip-digest-domains"]
DOMAIN_SETS = DIGEST_DOMAINS["domainSets"]
BY_DOMAIN = DIGEST_DOMAINS["byDomain"]
CLOSURE_KINDS = DIGEST_DOMAINS["closureKinds"]["byField"]
SCOPE_CAP_LAW = DIGEST_DOMAINS["scopeCapabilityLaw"]
LANGUAGE_MODES = DIGEST_DOMAINS["languageModes"]["map"]
PAYLOAD_REG = IDENT["x-opensip-payload-registry"]["classes"]
RELREG = RELDOC["x-opensip-relation-registry"]
RELATIONS = RELREG["relations"]
GRAMMAR_CAP = NATIVE["x-opensip-grammar-capability-registry"]
DEF_CAUSE = NATIVE["x-opensip-deficiency-cause-registry"]["deficiencies"]
CONFIG_KIND_LAW = NATIVE["x-opensip-config-node-kind-law"]

RELATION_DOC = "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
NATIVE_DOC = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
POLICY_DOC = "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"
RELATION_DOC_DIGEST = osip.doc_digest(RELATION_DOC)
NATIVE_DOC_DIGEST = osip.doc_digest(NATIVE_DOC)
POLICY_DOC_DIGEST = osip.doc_digest(POLICY_DOC)

RESOLVED_RUNGS = {"resolved-target", "resolved-binding", "resolved-callee",
                  "checked", "from-resolved-calls"}
INVENTORY_CAPS = {("file", "enumerated"), ("package", "manifest-declared"),
                  ("vcs-change", "vcs-reported")}

# native section 10 precedence, most specific first
DEFICIENCY_PRECEDENCE = [
    "language-tier-unsupported", "provider-unavailable", "input-closure-incomplete",
    "budget-exhausted", "confidence-floor-unmet", "derivation-policy-unmet",
    "resolution-incomplete", "external-consumers-unknown", "required-relation-missing",
]


class EvidenceUnavailable(Exception):
    """identity-and-evidence section 5 / the reference closure entry point:
    a missing promised object is retention loss, not a false predicate."""


class Store:
    """The ONE content-addressed store keyed by raw SHA-256 (identity section 3)."""

    def __init__(self):
        self.blobs = {}
        self.labels = {}

    def put_raw(self, b: bytes, label=None) -> str:
        h = raw_sha256(b)
        if h in self.blobs and self.blobs[h] != b:
            raise AssertionError("CAS collision")
        self.blobs[h] = b
        if label:
            self.labels.setdefault(h, label)
        return h

    def put_record(self, rec, label=None) -> str:
        return self.put_raw(C(rec), label)

    def put_h(self, domain: str, desc, label=None) -> str:
        """Retains the exact H preimage frame under the bare-hex h-identity."""
        fr = frame(domain, desc)
        h = raw_sha256(fr)
        self.blobs[h] = fr
        if label:
            self.labels.setdefault(h, label)
        return h

    def get(self, h: str) -> bytes:
        if h not in self.blobs:
            raise EvidenceUnavailable(h)
        return self.blobs[h]

    def has(self, h: str) -> bool:
        return h in self.blobs


def suffix(typed: str) -> str:
    return typed.split(":", 1)[1]


class Closure:
    def __init__(self, store: Store):
        self.s = store
        self.faults = []          # ordered, first is the first observed refusal
        self.checks = 0
        self.notes = []

    # -- fault plumbing ----------------------------------------------------
    def fault(self, code, detail=""):
        self.faults.append((code, detail))
        return False

    def need(self, cond, code, detail=""):
        self.checks += 1
        if not cond:
            return self.fault(code, detail)
        return True

    # -- typed object fetch ------------------------------------------------
    def h_object(self, digest_hex, expect_domain=None, domain_set=None,
                 fault_code="H_FRAME"):
        """Fetch the retained frame under a bare-hex h-identity, admit it exactly,
        validate the payload under the record its domain registers, and re-hash."""
        try:
            blob = self.s.get(digest_hex)
        except EvidenceUnavailable:
            self.fault("EVIDENCE_UNAVAILABLE", "missing preimage " + digest_hex)
            return None, None
        try:
            dom, val = osip.parse_frame(blob)
        except osip.AdmissionError as e:
            self.fault(fault_code, "%s %s" % (e.code, digest_hex))
            return None, None
        if expect_domain and dom != expect_domain:
            self.fault("H_DOMAIN_MISMATCH", "%s != %s" % (dom, expect_domain))
            return None, None
        if domain_set is not None and dom not in DOMAIN_SETS[domain_set]:
            self.fault("H_DOMAIN_UNREGISTERED", "%s not in %s" % (dom, domain_set))
            return None, None
        if raw_sha256(frame(dom, val)) != digest_hex:
            self.fault("H_IDENTITY_MISMATCH", digest_hex)
            return None, None
        if domain_set is not None:
            row = DOMAIN_SETS[domain_set][dom]
            errs = schemas.validate(val, "native", row["selector"])
            if errs:
                self.fault("H_PAYLOAD_SCHEMA", "%s %s" % (dom, errs[:2]))
                return None, None
        return dom, val

    def h_record(self, digest_hex, domain, doc, selector, code):
        """A foundation semantic identity is retained as its exact H preimage
        FRAME under the bare hex (identity section 3, the closing digest law)."""
        dom, val = self.h_object(digest_hex, expect_domain=domain,
                                 fault_code=code + "_FRAME")
        if val is None:
            return None
        errs = schemas.validate(val, doc, selector)
        if errs:
            self.fault(code + "_SCHEMA", "%s %s" % (selector, errs[:2]))
            return None
        return val

    def record(self, digest_hex, doc, selector, code="RECORD"):
        try:
            blob = self.s.get(digest_hex)
        except EvidenceUnavailable:
            self.fault("EVIDENCE_UNAVAILABLE", "missing record " + digest_hex)
            return None
        try:
            val, _ = admit_raw(blob)
        except osip.AdmissionError as e:
            self.fault(code + "_LEXICAL", "%s %s" % (e.code, digest_hex))
            return None
        if C(val) != blob:
            self.fault(code + "_NOT_CANONICAL", digest_hex)
            return None
        errs = schemas.validate(val, doc, selector)
        if errs:
            self.fault(code + "_SCHEMA", "%s %s" % (selector, errs[:2]))
            return None
        return val

    # ======================================================================
    def close_run(self, run_id):
        """Re-decide admission over retained bytes alone.  No compiler, cargo,
        provider, repository or filesystem operation runs here
        (identity-and-evidence section 3)."""
        R = {}
        run = self.h_record(suffix(run_id), "run", "identity", "#/$defs/run", "RUN")
        if run is None:
            return self.report()
        # a typed identity is re-derived, never trusted
        self.need(ident("run", run) == run_id, "RUN_IDENTITY", run_id)
        R["run"] = run

        seal = self.h_record(suffix(run["evaluationSealId"]), "evaluation-seal",
                             "identity", "#/$defs/evaluation-seal", "SEAL")
        if seal is None:
            return self.report()
        self.need(ident("evaluation-seal", seal) == run["evaluationSealId"], "SEAL_IDENTITY")
        R["seal"] = seal

        ev = self.h_record(suffix(seal["evidenceId"]), "semantic-evidence",
                           "identity", "#/$defs/semantic-evidence", "EVIDENCE")
        if ev is None:
            return self.report()
        self.need(ident("semantic-evidence", ev) == seal["evidenceId"], "EVIDENCE_IDENTITY")
        self.need(ev["planId"] == seal["planId"], "EVIDENCE_PLAN_JOIN")
        self.need(run["evidenceId"] == seal["evidenceId"], "RUN_EVIDENCE_JOIN")
        R["evidence"] = ev

        proof = self.h_record(suffix(seal["proofBundleId"]), "proof-bundle",
                              "identity", "#/$defs/proof-bundle", "PROOF")
        if proof is None:
            return self.report()
        self.need(ident("proof-bundle", proof) == seal["proofBundleId"], "PROOF_IDENTITY")
        self.need(ev["proofBundleId"] == seal["proofBundleId"], "PROOF_SEAL_JOIN")
        self.need(proof["planId"] == seal["planId"], "PROOF_PLAN_JOIN")
        self.need(seal["verdict"] == proof["verdict"], "SEAL_VERDICT_JOIN")
        self.need(seal["executionPlanId"] == proof["executionPlanId"], "SEAL_EXECPLAN_JOIN")
        R["proof"] = proof

        # ACYCLIC: proof carries no evidence/seal/run reference (identity section 3)
        proof_bytes = C(proof)
        for forbidden, name in ((suffix(seal["evidenceId"]), "evidence"),
                                (suffix(run["evaluationSealId"]), "seal"),
                                (suffix(run_id), "run")):
            self.need(forbidden.encode() not in proof_bytes,
                      "PROOF_ACYCLIC", "proof references " + name)

        execplan = self.h_record(suffix(proof["executionPlanId"]), "execution-plan",
                                 "identity", "#/$defs/execution-plan", "EXECPLAN")
        if execplan is None:
            return self.report()
        self.need(ident("execution-plan", execplan) == proof["executionPlanId"],
                  "EXECPLAN_IDENTITY")
        R["execution-plan"] = execplan

        plan = self.h_record(suffix(seal["planId"]), "plan", "identity", "#/$defs/plan", "PLAN")
        if plan is None:
            return self.report()
        self.need(ident("plan", plan) == seal["planId"], "PLAN_IDENTITY")
        self.need(run["planId"] == seal["planId"], "RUN_PLAN_JOIN")
        self.need(execplan["planId"] == seal["planId"], "EXECPLAN_PLAN_JOIN")
        R["plan"] = plan

        snap = self.h_record(suffix(plan["snapshotId"]), "snapshot", "identity",
                             "#/$defs/snapshot", "SNAPSHOT")
        if snap is None:
            return self.report()
        self.need(ident("snapshot", snap) == plan["snapshotId"], "SNAPSHOT_IDENTITY")
        self.need(run["snapshotId"] == plan["snapshotId"], "RUN_SNAPSHOT_JOIN")
        self.need(run["projectId"] == snap["projectId"], "RUN_PROJECT_JOIN")
        R["snapshot"] = snap
        inv = {row["path"]: row for row in snap["sourceInventory"]}
        self.need(len(inv) == len(snap["sourceInventory"]),
                  "INVENTORY_DUPLICATE_PATH",
                  "inventory paths must be unique even at differing digests")
        for f in osip.check_order(snap["sourceInventory"], "path", "snapshot.sourceInventory"):
            self.fault("ORDER", str(f))
        for p, row in inv.items():
            if not self.s.has(row["sha256"]):
                self.fault("EVIDENCE_UNAVAILABLE", "source blob for " + p)
            elif len(self.s.get(row["sha256"])) != row["bytes"]:
                self.fault("INVENTORY_LENGTH", p)

        self._plan_joins(plan, snap, run)
        ctxs = self._native_contexts(plan, snap)
        unis = self._universes(plan, snap, ctxs)
        R["contexts"], R["universes"] = ctxs, unis

        scopes = self._scopes(plan, snap, unis)
        facts = self._facts(plan, snap, unis, scopes)
        covs = self._coverage(plan, snap, unis, scopes, facts)
        self._views(plan, ev, scopes, facts, covs, unis, snap)
        self._proof(plan, proof, ev, covs, facts)
        R["scopes"], R["facts"], R["coverage"] = scopes, facts, covs
        self.resolved = R
        return self.report()

    # ------------------------------------------------------------------
    def _plan_joins(self, plan, snap, run):
        cfg = self.record(plan["resolvedConfigDigest"], "identity",
                          "#/$defs/semantic-configuration", "CONFIG")
        if cfg is not None:
            # identity section 3: plan.budget equals analysis.budget EXACTLY and BY TYPE
            self.need(cfg["analysis"]["budget"] == plan["budget"]
                      and type(cfg["analysis"]["budget"]["limit"])
                      is type(plan["budget"]["limit"]),
                      "PLAN_BUDGET_CONTRADICTS_CONFIG",
                      "%r vs %r" % (plan["budget"], cfg["analysis"]["budget"]))
            for sec in ("analysis", "components", "discovery", "policy", "evidence"):
                self.need(sec in cfg, "CONFIG_SECTION_ABSENT", sec)
        self.need(snap["resolvedConfigDigest"] == plan["resolvedConfigDigest"],
                  "SNAPSHOT_PLAN_CONFIG_DISAGREE")
        self.need(snap["scopeDigest"] == plan["scopeDigest"],
                  "SNAPSHOT_PLAN_SCOPE_DISAGREE")

        scope = self.record(plan["scopeDigest"], "identity",
                            "#/$defs/scope-descriptor", "SCOPE_DESCRIPTOR")
        vcs = self.record(snap["vcsDigest"], "identity",
                          "#/$defs/vcs-observation", "VCS")
        if vcs is not None:
            self.need(vcs["sourceInventoryDigest"] == record_digest(snap["sourceInventory"]),
                      "VCS_INVENTORY_DIGEST")
            if not self.s.has(vcs["sourceInventoryDigest"]):
                self.fault("EVIDENCE_UNAVAILABLE", "source-inventory record blob")

        spec = self.record(plan["analysisSpecDigest"], "identity",
                           "#/$defs/analysis-spec", "ANALYSIS_SPEC")
        if spec is not None:
            self._analysis_spec(spec)

        grant = self.record(plan["semanticGrantDigest"], "identity",
                            "#/$defs/semantic-grant", "GRANT")
        if grant is not None:
            self.need(grant["projectId"] == run["projectId"], "GRANT_PROJECT_JOIN")
            self.need(grant["scopeDigest"] == plan["scopeDigest"], "GRANT_SCOPE_JOIN")
            ops = set(grant["analysisOperations"])
            # identity section 6: every Plan with selected import2 inputs also
            # requires read-import in its semantic grant
            self.need(("read-import" in ops) or not plan["importIds"],
                      "GRANT_READ_IMPORT_MISSING")
            for pr in grant["principals"]:
                if pr["kind"] == "first-party":
                    self.need(pr["ownerSourceDigest"] is None,
                              "GRANT_FIRST_PARTY_OWNER_SOURCE")
                else:
                    self.need(pr["ownerSourceDigest"] is not None,
                              "GRANT_REPO_PRINCIPAL_WITHOUT_OWNER_SOURCE")
                    if pr["ownerSourceDigest"]:
                        oss = self.record(pr["ownerSourceDigest"], "identity",
                                          "#/$defs/owner-source-set", "OWNER_SOURCE_SET")
                        if oss is not None:
                            for f in osip.check_order(oss, {"by": ["ownerKey"]},
                                                      "owner-source-set"):
                                self.fault("ORDER", str(f))
            self.need(("prepare-code" in ops) == any(
                p["kind"] == "trusted-repository-code" for p in grant["principals"]),
                "GRANT_PREPARE_CODE_PRINCIPAL_JOIN")

        # capability manifest: derived retention, recomputed never trusted
        try:
            committed = self.s.get(plan["capabilityManifestBytesDigest"])
        except EvidenceUnavailable:
            self.fault("EVIDENCE_UNAVAILABLE", "capability manifest artifact")
            committed = None
        if committed is not None:
            self.need(osip.capability_manifest_id(committed) == plan["capabilityManifestId"],
                      "CAPABILITY_MANIFEST_ID_MISMATCH")
            self.need(run["capabilityManifestId"] == plan["capabilityManifestId"],
                      "RUN_CAPABILITY_MANIFEST_JOIN")
            import capman
            faults = capman.admit_committed(committed)
            for f in faults:
                self.fault("CAPABILITY_MANIFEST_" + f[0], f[1])

        for d, sel in ((plan["policyDigest"], "#/$defs/PolicyDocumentV1"),
                       (plan["waiverDigest"], "#/$defs/WaiverSetV1")):
            self.record(d, "policy-document", sel, "POLICY")
        for cl in plan["semanticClosures"]:
            self._closure(cl)
        for d in plan["nativeContextDigests"]:
            pass  # walked in _native_contexts

    def _analysis_spec(self, spec):
        caps = {c["id"] for c in MATRIX["capabilities"]}
        cells = {(c["capability"], c["mode"]): c["state"] for c in MATRIX["cells"]}
        for row in spec["requestedCapabilities"]:
            cid, mode = row["capabilityId"], row["languageMode"]
            if cid not in caps:
                self.fault("ANALYSIS_SPEC_CAPABILITY",
                           "native.requested-capability-unregistered:" + cid)
                continue
            if mode not in LANGUAGE_MODES:
                self.fault("ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED", mode)
                continue
            st = cells.get((cid, mode))
            if st is None:
                self.fault("ANALYSIS_SPEC_CELL_ABSENT", "%s/%s" % (cid, mode))
            elif st == "NOT-SELECTED":
                self.fault("ANALYSIS_SPEC_CAPABILITY",
                           "native.requested-capability-mode-not-selected:%s/%s" % (cid, mode))
        for f in osip.check_order(spec["requestedCapabilities"], "canonical-set",
                                  "analysis-spec.requestedCapabilities"):
            self.fault("ORDER", str(f))
        # the closed parameter class
        rows = PAYLOAD_REG["parameter"]["rows"]
        allowed = {}
        for key, row in rows.items():
            path = "docs/coop/design-corrections/" + row["document"]
            allowed[osip.doc_digest(path)] = (row["document"], row["selector"])
        for p in spec["parameters"]:
            if p["schemaDigest"] not in allowed:
                self.fault("PAYLOAD_PARAMETER_UNREGISTERED", p["schemaDigest"])
                continue
            doc, sel = allowed[p["schemaDigest"]]
            name = {"foundation/import-source-context.schema.json": "import-source-context",
                    "workflows/schemas/policy-document.schema.json": "policy-document"}[doc]
            self.record(p["payloadDigest"], name, sel, "PARAMETER")
            if not self.s.has(p["schemaDigest"]):
                self.fault("EVIDENCE_UNAVAILABLE", "parameter schema document bytes")

    def _closure(self, closure_id):
        dom, val = self.h_object(suffix(closure_id), expect_domain="closure",
                                 fault_code="CLOSURE_FRAME")
        if val is None:
            return None
        errs = schemas.validate(val, "identity", "#/$defs/closure")
        if errs:
            self.fault("CLOSURE_SCHEMA", str(errs[:2]))
            return None
        for f in osip.check_order(val["tree"], "path", "closure.tree"):
            self.fault("ORDER", str(f))
        for row in val["tree"]:
            if not self.s.has(row["sha256"]):
                self.fault("EVIDENCE_UNAVAILABLE", "closure tree member " + row["path"])
            elif len(self.s.get(row["sha256"])) != row["bytes"]:
                self.fault("CLOSURE_TREE_LENGTH", row["path"])
        if not self.s.has(val["manifestDigest"]):
            self.fault("EVIDENCE_UNAVAILABLE", "closure manifest body bytes")
        return val

    # ------------------------------------------------------------------
    def _native_contexts(self, plan, snap):
        """Re-run the owning contract's own admission over the retained bytes
        (identity section 3; native sections 2.3/2.4/1.2)."""
        out = {}
        inv = {r["path"]: r for r in snap["sourceInventory"]}
        for hexd in plan["nativeContextDigests"]:
            dom, ctx = self.h_object(hexd, domain_set="native-context",
                                     fault_code="NATIVE_CONTEXT_FRAME")
            if ctx is None:
                continue
            row = DOMAIN_SETS["native-context"][dom]
            out[hexd] = (dom, ctx)
            # closure joins
            for cj in row["closureJoins"]:
                v = ctx
                for step in cj["path"]:
                    v = v.get(step) if isinstance(v, dict) else None
                if v is None:
                    self.fault("NATIVE_CONTEXT_CLOSURE_FIELD_ABSENT", str(cj["path"]))
                    continue
                cid = v if cj["form"] == "closure2-identity" else "closure2:" + v
                cl = self._closure(cid)
                if cl is None:
                    self.fault("native.native-context-closure-unretained", cid)
                    continue
                if cl["kind"] != cj["kind"]:
                    self.fault("native.native-context-closure-kind-mismatch",
                               "%s != %s" % (cl["kind"], cj["kind"]))
            for sj in row.get("snapshotJoins", []):
                v = ctx
                for step in sj["path"]:
                    v = v.get(step) if isinstance(v, dict) else None
                if sj["form"] == "inventoried-paths":
                    for p in (v or []):
                        if p not in inv:
                            self.fault("NATIVE_CONTEXT_PATH_OUTSIDE_SNAPSHOT", p)
                elif sj["form"] == "inventoried-path-and-digest":
                    if v is None:
                        if not sj.get("nullable"):
                            self.fault("NATIVE_CONTEXT_LOCKFILE_ABSENT", str(sj["path"]))
                    else:
                        p = v[sj["pathField"]]
                        if p not in inv:
                            self.fault("NATIVE_CONTEXT_LOCKFILE_OUTSIDE_SNAPSHOT", p)
                        elif inv[p]["sha256"] != v[sj["digestField"]]:
                            self.fault("NATIVE_CONTEXT_LOCKFILE_DIGEST", p)
            for ni in row.get("nestedIdentities", []):
                v = ctx
                for step in ni["path"]:
                    v = v.get(step) if isinstance(v, dict) else None
                if v is None:
                    if not ni.get("nullable"):
                        self.fault("NATIVE_NESTED_ABSENT", str(ni["path"]))
                    continue
                self._nested(v, ni["form"])
            for nr in row.get("nestedRecords", []):
                v = ctx
                for step in nr["path"]:
                    v = v.get(step) if isinstance(v, dict) else None
                if v is None:
                    if not nr.get("nullable"):
                        self.fault("NATIVE_NESTED_RECORD_ABSENT", str(nr["path"]))
                    continue
                rec = self.record(v, "native", nr["selector"], "NATIVE_NESTED_RECORD")
                if rec is not None:
                    for bj in nr.get("blobJoins", []):
                        self._blob_join(rec, bj)
            for bj in row.get("blobJoins", []):
                v = ctx
                for step in bj["path"]:
                    v = v.get(step) if isinstance(v, dict) else None
                self._blob_join(v, bj)
            # language-specific admission
            if dom == "native.context.typescript.v2":
                self._admit_ts_context(ctx)
            elif dom == "native.context.rust.v2":
                self._admit_rust_context(ctx)
            elif dom == "native.context.syntax.v2":
                self._admit_syntax_context(ctx)
        # The retained context frame SET must EQUAL plan.nativeContextDigests
        # exactly: a context reached by no Plan is refused, and a Plan naming an
        # unretained context cannot close.  The set is taken from the STORE.
        retained = set()
        for hexd, blob in list(self.s.blobs.items()):
            if not blob.startswith(osip.FRAME_PREFIX + b"\x00"):
                continue
            try:
                dom, _ = osip.parse_frame(blob)
            except osip.AdmissionError:
                continue
            if dom in DOMAIN_SETS["native-context"]:
                retained.add(hexd)
        self.need(retained == set(plan["nativeContextDigests"]),
                  "PLAN_CONTEXT_SET_MISMATCH",
                  "retained %s vs plan %s" % (sorted(retained),
                                              sorted(plan["nativeContextDigests"])))
        return out

    def _blob_join(self, holder, bj):
        if holder is None:
            return
        d = holder.get(bj["digestField"]) if isinstance(holder, dict) else None
        if d is None:
            return
        if not self.s.has(d):
            self.fault("EVIDENCE_UNAVAILABLE", "blob " + bj["digestField"])
        elif bj.get("lengthField") and len(self.s.get(d)) != holder[bj["lengthField"]]:
            self.fault("BLOB_LENGTH", bj["digestField"])

    def _nested(self, value, form):
        hexd = suffix(value) if form == "sha256-text" else value
        dom, val = self.h_object(hexd, domain_set="native-nested",
                                 fault_code="NATIVE_NESTED_FRAME")
        if val is None:
            return None
        row = DOMAIN_SETS["native-nested"][dom]
        for ni in row.get("nestedIdentities", []):
            for v in _walk(val, ni["path"]):
                if v is not None:
                    self._nested(v, ni["form"])
        for bj in row.get("blobJoins", []):
            for holder in _walk_holder(val, bj["path"]):
                self._blob_join(holder, bj)
        return val

    def _admit_ts_context(self, ctx):
        """native section 2.4 admit_native_context (TypeScript)."""
        tc = ctx["toolchain"]
        cl = self._closure(ctx["toolClosure"]["closureId"])
        if cl is not None:
            members = {r["sha256"] for r in cl["tree"]}
            for f in ("compiler", "runtime"):
                self.need(ctx["toolClosure"][f] in members,
                          "native.native-context-tool-not-in-closure", f)
            self.need(tc["compilerPackageDigest"] in members,
                      "native.native-context-tool-not-in-closure", "compilerPackageDigest")
            self.need(tc["compilerVersion"] == cl["semanticVersion"],
                      "native.native-context-compiler-version-not-from-manifest",
                      "%s != %s" % (tc["compilerVersion"], cl["semanticVersion"]))
        std = self._closure("closure2:" + tc["typescriptStdlibMerkleRoot"])
        if std is not None:
            base = {}
            for r in std["tree"]:
                b = r["path"].rsplit("/", 1)[-1]
                if b in base:
                    self.fault("native.native-context-stdlib-tree-ambiguous-basename", b)
                base[b] = r["sha256"]
            declared = {c["component"]: c["sha256"]
                        for c in tc["standardLibraryComponentDigests"]}
            for b in base:
                if b.endswith(".d.ts") and b not in declared:
                    self.fault("native.native-context-stdlib-inventory-incomplete", b)
            for comp, dg in declared.items():
                if base.get(comp) != dg:
                    self.fault("native.native-context-stdlib-tree-mismatch", comp)
            for n in tc["libSelection"]:
                comp = "lib." + _fold(n) + ".d.ts"
                if comp not in declared:
                    self.fault("native.native-context-lib-not-retained", n)
            folds = [_fold(n) for n in tc["libSelection"]]
            if len(set(folds)) != len(folds):
                self.fault("native.native-context-field-mismatch", "duplicate-lib-selection")
            hon = ctx["configProjection"]["honoredOptions"]["lib"]
            if set(folds) != {_fold(m) for m in hon}:
                self.fault("native.native-context-field-mismatch", "libSelection")
        self.need(ctx["moduleResolutionMode"]
                  == ctx["configProjection"]["honoredOptions"]["moduleResolution"],
                  "native.native-context-field-mismatch", "moduleResolutionMode")
        for f in osip.check_order(tc["libSelection"], "utf8", "libSelection"):
            self.fault("ORDER", str(f))
        for f in osip.check_order(tc["standardLibraryComponentDigests"],
                                  {"by": ["component"]}, "standardLibraryComponentDigests"):
            self.fault("ORDER", str(f))
        self.need((ctx["nodeModulesLayoutDigest"] is not None)
                  == (ctx["nodeModulesLayoutDigest"] is not None), "TS_LAYOUT")

    def _admit_rust_context(self, ctx):
        cl = self._closure(ctx["toolClosure"]["closureId"])
        if cl is not None:
            members = {r["sha256"] for r in cl["tree"]}
            for f in ("rustc", "cargo", "procMacroServer"):
                self.need(ctx["toolClosure"][f] in members,
                          "native.native-context-tool-not-in-closure", f)
            for f in ("linker", "ar"):
                if ctx["toolClosure"][f] is not None:
                    self.need(ctx["toolClosure"][f] in members,
                              "native.native-context-tool-not-in-closure", f)
            self.need(ctx["toolchain"]["rustcVersion"] == cl["semanticVersion"],
                      "native.native-context-compiler-version-not-from-manifest")
        self.need(ctx["toolchain"]["targetTriple"] == ctx["targetTriple"],
                  "native.native-context-field-mismatch", "targetTriple")

    def _admit_syntax_context(self, ctx):
        """native section 1.2: the syntax-only native context."""
        gb = ctx["grammarBundle"]
        cl = self._closure(gb["closureId"])
        if cl is not None:
            self.need(cl["kind"] == "grammar",
                      "native.native-context-closure-kind-mismatch", cl["kind"])
            self.need(gb["parserVersion"] == cl["semanticVersion"],
                      "native.syntax-grammar-version-not-from-manifest")
            members = {r["sha256"] for r in cl["tree"]}
            for g in gb["grammars"]:
                self.need(g["grammarDigest"] in members,
                          "native.syntax-grammar-not-in-retained-tree", g["grammarId"])
            self.need(gb["bundleDigest"] in members,
                      "native.syntax-bundle-manifest-not-in-retained-tree")
            self.need(gb["normalizer"]["specificationDigest"] in members,
                      "native.syntax-normalizer-spec-not-in-retained-tree")
        # syntaxClass is not caller selected: both directions enforced
        reg = GRAMMAR_CAP["languages"]
        seen_suffix = {}
        for g in gb["grammars"]:
            lang = g["languageId"]
            if lang not in reg:
                self.fault("native.syntax-grammar-language-unregistered", lang)
                continue
            if g["syntaxClass"] != reg[lang]["syntaxClass"]:
                self.fault("native.syntax-grammar-class-mismatch",
                           "%s declared %s" % (lang, g["syntaxClass"]))
            for sfx in g["suffixes"]:
                if sfx not in reg[lang]["suffixes"]:
                    self.fault("native.syntax-grammar-suffix-not-of-language",
                               "%s %s" % (lang, sfx))
                if sfx in seen_suffix:
                    self.fault("native.syntax-grammar-suffix-ambiguous", sfx)
                seen_suffix[sfx] = g["grammarId"]
        blv_enum = IDENT["$defs"]["body-language-version"]["properties"]["languageId"]["enum"]
        for lang, r in reg.items():
            if r["syntaxClass"] == "code":
                self.need(lang in blv_enum, "GRAMMAR_CODE_LANGUAGE_NOT_IN_BLV_ENUM", lang)
            else:
                self.need(lang not in blv_enum, "GRAMMAR_DATA_LANGUAGE_IN_BLV_ENUM", lang)

    # ------------------------------------------------------------------
    def referenced_universes(self):
        """The universe digests the retained scopes and facts actually name."""
        refs = set()
        for hexd, blob in list(self.s.blobs.items()):
            if not blob.startswith(osip.FRAME_PREFIX + b"\x00"):
                continue
            try:
                dom, val = osip.parse_frame(blob)
            except osip.AdmissionError:
                continue
            if dom in ("fact", "subject-scope") and isinstance(val, dict):
                refs.add(val.get("sourceUniverse"))
                refs.add(val.get("targetUniverse"))
        refs.discard(None)
        return refs

    def _universes(self, plan, snap, ctxs):
        """Every retained universe frame's nativeContextId must be sha256: plus a
        member of plan.nativeContextDigests (identity section 3)."""
        out = {}
        inv = {r["path"]: r for r in snap["sourceInventory"]}
        for hexd in sorted(self.referenced_universes()):
            dom, val = self.h_object(hexd, domain_set="native-semantic-universe",
                                     fault_code="UNIVERSE_FRAME")
            if val is None:
                continue
            row = DOMAIN_SETS["native-semantic-universe"][dom]
            if "binding" not in row:
                self.fault("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", dom)
                continue
            cid = val["nativeContextId"]
            self.need(cid.startswith("sha256:") and suffix(cid) in plan["nativeContextDigests"],
                      "UNIVERSE_CONTEXT_NOT_PLAN_SELECTED", cid)
            got = ctxs.get(suffix(cid))
            if got is None:
                self.fault("native.universe-context-not-supplied", cid)
                continue
            cdom, ctx = got
            self.need(cdom == row["contextDomain"],
                      "native.native-context-language-mismatch",
                      "%s bound to %s" % (dom, cdom))
            out[hexd] = (dom, val, cdom, ctx)
            for sj in row.get("snapshotJoins", []):
                v = _first(_walk(val, sj["path"]))
                if sj["form"] == "inventoried-paths":
                    for p in (v or []):
                        if p not in inv:
                            self.fault("UNIVERSE_PATH_OUTSIDE_SNAPSHOT", p)
                elif sj["form"] == "inventoried-path-and-digest" and v is not None:
                    p = v[sj["pathField"]]
                    if p not in inv:
                        self.fault("UNIVERSE_LOCKFILE_OUTSIDE_SNAPSHOT", p)
                    elif inv[p]["sha256"] != v[sj["digestField"]]:
                        self.fault("UNIVERSE_LOCKFILE_DIGEST", p)
            for f in row.get("contextAgreementFields", []):
                self.need(val.get(f) == ctx.get(f),
                          "native.universe-context-field-mismatch", f)
            for ni in row.get("nestedIdentities", []):
                v = _first(_walk(val, ni["path"]))
                if v is None:
                    if not ni.get("nullable"):
                        self.fault("UNIVERSE_NESTED_ABSENT", str(ni["path"]))
                    continue
                self._nested(v, ni["form"])
            for nr in row.get("nestedRecords", []):
                v = _first(_walk(val, nr["path"]))
                rec = self.record(v, "native", nr["selector"], "UNIVERSE_NESTED_RECORD")
                if rec is not None and nr["selector"] == "#/$defs/TypeScriptConfigGraphV1":
                    self._ts_config_graph(rec, val, ctx, inv)
            if dom == "native.semantic-universe.typescript.v2":
                self._bind_ts_universe(val, ctx)
            elif dom == "native.semantic-universe.rust.v2":
                self._bind_rust_universe(val, ctx, inv)
            elif dom == "native.semantic-universe.syntax.v2":
                self._bind_syntax_universe(val, ctx)
        return out

    def _ts_config_graph(self, g, uni, ctx, inv):
        paths = [n["path"] for n in g["nodes"]]
        self.need(sorted(paths) == sorted(ctx["configProjection"]["configGraphPaths"]),
                  "native.universe-context-field-mismatch", "configGraphPaths")
        for n in g["nodes"]:
            if n["path"] not in inv:
                self.fault("CONFIG_GRAPH_PATH_OUTSIDE_SNAPSHOT", n["path"])
            elif inv[n["path"]]["sha256"] != n["contentSha256"]:
                self.fault("CONFIG_GRAPH_DIGEST", n["path"])
            base = n["path"].rsplit("/", 1)[-1]
            derived = CONFIG_KIND_LAW["basenames"].get(base, CONFIG_KIND_LAW["otherwise"])
            self.need(n["kind"] == derived,
                      "native.config-graph-kind-contradicts-path",
                      "%s declared %s derived %s" % (n["path"], n["kind"], derived))
            for e in n["extendsResolved"]:
                self.need(e in paths, "CONFIG_GRAPH_EDGE_UNKNOWN_NODE", e)
        # reachable from the selected entry, acyclic
        if g["entryConfigPath"] is not None:
            byp = {n["path"]: n for n in g["nodes"]}
            seen, stack = set(), [g["entryConfigPath"]]
            order = []
            while stack:
                p = stack.pop()
                if p in seen:
                    continue
                seen.add(p)
                order.append(p)
                stack.extend(byp.get(p, {}).get("extendsResolved", []))
            self.need(seen == set(paths), "CONFIG_GRAPH_UNREACHABLE_NODE",
                      str(sorted(set(paths) - seen)))
            colour = {}

            def dfs(p):
                colour[p] = 1
                for q in byp.get(p, {}).get("extendsResolved", []):
                    if colour.get(q) == 1:
                        return False
                    if colour.get(q) is None and not dfs(q):
                        return False
                colour[p] = 2
                return True
            self.need(dfs(g["entryConfigPath"]), "CONFIG_GRAPH_CYCLIC")
            entry_kind = byp[g["entryConfigPath"]]["kind"]
            derived_origin = "jsconfig" if entry_kind == "jsconfig" else "tsconfig"
        else:
            derived_origin = "synthesized"
            self.need(g["nodes"] == [], "CONFIG_GRAPH_SYNTHESIZED_WITH_NODES")
        self.need(uni["configOrigin"] == derived_origin,
                  "native.universe-config-origin-not-derived",
                  "%s vs %s" % (uni["configOrigin"], derived_origin))
        self.need(uni["tsconfigGraphHash"] == record_digest(g),
                  "TS_CONFIG_GRAPH_HASH")

    def _bind_ts_universe(self, uni, ctx):
        for f in ("languageMode", "packageModuleType"):
            self.need(uni[f] == ctx[f], "native.universe-context-field-mismatch", f)
        hon = ctx["configProjection"]["honoredOptions"]
        for f in ("allowJs", "checkJs"):
            self.need(uni[f] is hon[f], "native.universe-context-field-mismatch", f)
        self.need(uni["jsAdmittedToProgram"] is hon["allowJs"],
                  "native.universe-context-field-mismatch", "jsAdmittedToProgram")
        self.need(uni["jsDiagnosticsEnabled"] is hon["checkJs"],
                  "native.universe-context-field-mismatch", "jsDiagnosticsEnabled")
        lk = ctx["lockfileIdentity"]
        self.need(uni["lockfileKind"] == (lk["kind"] if lk else "none"),
                  "native.universe-context-field-mismatch", "lockfileKind")
        self.need(uni["nodeModulesInReadSet"]
                  is (ctx["nodeModulesLayoutDigest"] is not None),
                  "native.universe-context-field-mismatch", "nodeModulesInReadSet")
        self.need((uni["synthesizedOptions"] is not None)
                  == (uni["configOrigin"] == "synthesized"),
                  "native.universe-context-field-mismatch", "synthesizedOptions")
        self.need((uni["synthesizerVersion"] is not None)
                  == (uni["configOrigin"] == "synthesized"),
                  "native.universe-context-field-mismatch", "synthesizerVersion")
        if uni["synthesizedOptions"] is not None:
            for k, v in uni["synthesizedOptions"].items():
                if k in hon:
                    self.need(hon[k] == v or (hon[k] is v),
                              "native.universe-context-field-mismatch",
                              "synthesizedOptions." + k)
            if "jsx" not in uni["synthesizedOptions"]:
                self.need(hon["jsx"] is None,
                          "native.universe-context-field-mismatch", "jsx")
        self.need(uni["configOrigin"] != "synthesized"
                  or ctx["configProjection"]["configGraphPaths"] == [],
                  "native.universe-context-field-mismatch", "extends-graph-emptiness")

    def _bind_rust_universe(self, uni, ctx, inv):
        for f in ("dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"):
            self.need(uni[f] == ctx[f], "native.universe-context-field-mismatch", f)
        self.need(uni["rustflags"] == ctx["configProjection"]["rustflags"],
                  "native.universe-context-field-mismatch", "rustflags")
        self.need(uni["configProjectionSha256"]
                  == H("native.cargo-config-projection.v2", ctx["configProjection"]),
                  "native.universe-context-field-mismatch", "configProjectionSha256")
        self.need(uni["executionCapableResolution"]
                  is (uni["preparedResolution"] != "none"),
                  "native.universe-context-field-mismatch", "executionCapableResolution")
        self.need((uni["preparedOutputSetId"] is None)
                  == (uni["preparedResolution"] == "none"),
                  "native.universe-context-field-mismatch", "preparedOutputSetId/none")
        base = set(ctx["baseCfg"])
        ids = set()
        for cs in uni["cfgSets"]:
            self.need(base <= set(cs["cfg"]), "native.universe-cfgset-drops-base-cfg",
                      cs["cfgSetId"])
            self.need(cs["cfgSetId"] not in ids, "native.universe-cfgset-duplicate",
                      cs["cfgSetId"])
            ids.add(cs["cfgSetId"])
        if uni["sourceUnitOwnershipId"] is not None:
            own = self._nested(uni["sourceUnitOwnershipId"], "sha256-text")
            if own is not None:
                self._admit_ownership(own, uni, inv)

    def _admit_ownership(self, own, uni, inv):
        declared = {}
        for u in own["units"]:
            expect = "sha256:" + H("native.compilation-unit.v1",
                                   {"schemaVersion": 1, "markerPath": u["markerPath"],
                                    "targetKind": u["targetKind"],
                                    "targetName": u["targetName"]})
            self.need(u["unitId"] == expect, "sourceUnitOwnership.unitId",
                      "%s != %s" % (u["unitId"], expect))
            declared[u["unitId"]] = u
            if u["markerPath"] not in inv:
                self.fault("OWNERSHIP_MARKER_OUTSIDE_SNAPSHOT", u["markerPath"])
            if u["targetEdition"] is None:
                self.need(u["crateName"] in uni["edition"],
                          "OWNERSHIP_DEFERRING_UNIT_CRATE_NOT_IN_EDITION_MAP",
                          u["crateName"])
        for sid in own["selectedUnitIds"]:
            self.need(sid in declared, "OWNERSHIP_SELECTION_UNDECLARED_UNIT", sid)
        for o in own["ownership"]:
            self.need(o["unitId"] in declared, "OWNERSHIP_ROW_UNDECLARED_UNIT", o["unitId"])
            if o["path"] not in inv:
                self.fault("OWNERSHIP_PATH_OUTSIDE_SNAPSHOT", o["path"])
        for f in osip.check_order(own["units"], {"by": ["unitId"]}, "ownership.units"):
            self.fault("ORDER", str(f))
        for f in osip.check_order(own["ownership"], {"by": ["path", "unitId"]},
                                  "ownership.ownership"):
            self.fault("ORDER", str(f))
        for f in osip.check_order(own["selectedUnitIds"], "utf8", "selectedUnitIds"):
            self.fault("ORDER", str(f))

    def _bind_syntax_universe(self, uni, ctx):
        have = {g["grammarId"] for g in ctx["grammarBundle"]["grammars"]}
        for gid in uni["selectedGrammarIds"]:
            self.need(gid in have, "native.syntax-grammar-not-in-bundle", gid)

    # ------------------------------------------------------------------
    def _scopes(self, plan, snap, unis):
        out = {}
        for hexd, blob in list(self.s.blobs.items()):
            if not blob.startswith(osip.FRAME_PREFIX + b"\x00"):
                continue
            try:
                dom, val = osip.parse_frame(blob)
            except osip.AdmissionError:
                continue
            if dom != "subject-scope":
                continue
            errs = schemas.validate(val, "identity", "#/$defs/subject-scope")
            if errs:
                self.fault("SCOPE_SCHEMA", str(errs[:2]))
                continue
            self.need(val["snapshotId"] == plan["snapshotId"], "SCOPE_SOURCE_JOIN")
            rel = val["relation"]
            if rel not in RELATIONS:
                self.fault("SUBJECT_SCOPE_RELATION_UNREGISTERED", rel)
                continue
            ladder = RELATIONS[rel]["ladder"]
            self.need(val["resolution"] in ladder,
                      "SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER",
                      "%s@%s (ladder %s)" % (rel, val["resolution"], ladder))
            for u in (val["sourceUniverse"], val["targetUniverse"]):
                self.need(u in unis, "SCOPE_UNIVERSE_NOT_RETAINED", u)
            cl = self._closure(val["enumeratorClosure"])
            if cl is not None:
                self.need(cl["kind"] == "provider", "SCOPE_ENUMERATOR_CLOSURE_KIND",
                          cl["kind"])
            self.need(val["enumeratorClosure"] in plan["semanticClosures"],
                      "SCOPE_ENUMERATOR_NOT_PLAN_SELECTED")
            for f in osip.check_order(val["subjects"], "canonical-set", "scope.subjects"):
                self.fault("ORDER", str(f))
            out["scope2:" + hexd] = val
        return out

    # ------------------------------------------------------------------
    def _facts(self, plan, snap, unis, scopes):
        out = {}
        inv = {r["path"]: r for r in snap["sourceInventory"]}
        for hexd, blob in list(self.s.blobs.items()):
            if not blob.startswith(osip.FRAME_PREFIX + b"\x00"):
                continue
            try:
                dom, val = osip.parse_frame(blob)
            except osip.AdmissionError:
                continue
            if dom != "fact":
                continue
            errs = schemas.validate(val, "identity", "#/$defs/fact")
            if errs:
                self.fault("FACT_SCHEMA", str(errs[:2]))
                continue
            fid = "fact2:" + hexd
            out[fid] = val
            self.need(val["snapshotId"] == plan["snapshotId"], "FACT_SOURCE_JOIN")
            rel = val["relation"]
            if rel not in RELATIONS:
                self.fault("FACT_RELATION_UNREGISTERED", rel)
                continue
            row = RELATIONS[rel]
            self.need(val["resolution"] in row["ladder"],
                      "FACT_RUNG_NOT_IN_RELATION_LADDER",
                      "%s@%s" % (rel, val["resolution"]))
            self.need(val["payloadSchemaDigest"] == RELATION_DOC_DIGEST,
                      "FACT_PAYLOAD_SCHEMA_NOT_REGISTERED_DOCUMENT")
            if not self.s.has(val["payloadSchemaDigest"]):
                self.fault("EVIDENCE_UNAVAILABLE", "relation schema document bytes")
            if row["universeRule"] == "same-only":
                self.need(val["sourceUniverse"] == val["targetUniverse"],
                          "FACT_UNIVERSE_RULE_SAME_ONLY", rel)
            for u in (val["sourceUniverse"], val["targetUniverse"]):
                self.need(u in unis, "FACT_UNIVERSE_NOT_RETAINED", u)
            cl = self._closure(val["producerClosure"])
            if cl is not None:
                self.need(cl["kind"] == "provider", "FACT_PRODUCER_CLOSURE_KIND", cl["kind"])
            self.need(val["producerClosure"] in plan["semanticClosures"],
                      "FACT_PRODUCER_NOT_PLAN_SELECTED")

            # anchorLaw
            al = row["anchorLaw"]
            n = len(val["anchors"])
            if al["class"] == "inventory":
                self.need(n == 0, "FACT_ANCHOR_CARDINALITY",
                          "%s inventory class requires exactly 0, saw %d" % (rel, n))
            elif al["class"] == "body-identity":
                self.need(n == 1, "FACT_ANCHOR_CARDINALITY",
                          "%s body-identity requires exactly 1, saw %d" % (rel, n))
            else:
                self.need(n >= 1, "FACT_ANCHOR_CARDINALITY",
                          "%s source-text requires at least 1, saw %d" % (rel, n))
            for a in val["anchors"]:
                if a["path"] not in inv:
                    self.fault("ANCHOR_SOURCE", a["path"])
                    continue
                if inv[a["path"]]["sha256"] != a["blobDigest"]:
                    self.fault("ANCHOR_SOURCE", "blobDigest " + a["path"])
                    continue
                try:
                    b = self.s.get(a["blobDigest"])
                except EvidenceUnavailable:
                    self.fault("EVIDENCE_UNAVAILABLE", "anchor blob " + a["path"])
                    continue
                if not (0 <= a["startByte"] <= a["endByte"] <= len(b)):
                    self.fault("ANCHOR_RANGE", a["path"])
                    continue
                if al["class"] != "inventory":
                    try:
                        b[a["startByte"]:a["endByte"]].decode("utf-8")
                        b[:a["startByte"]].decode("utf-8")
                    except UnicodeDecodeError:
                        self.fault("ANCHOR_UTF8", a["path"])
            for f in osip.check_order(val["anchors"], "canonical-set", "fact.anchors"):
                self.fault("ORDER", str(f))

            payload = self.record(val["payloadDigest"], "relation", row["selector"],
                                  "FACT_PAYLOAD")
            if payload is None:
                continue
            # rung required/forbidden payload field rules
            rr = row["rungs"].get(val["resolution"])
            if rr:
                for f in rr["required"]:
                    self.need(f in payload, "FACT_RUNG_REQUIRED_FIELD", f)
                for f in rr["forbidden"]:
                    self.need(f not in payload, "FACT_RUNG_FORBIDDEN_FIELD", f)
            self._snapshot_joins(rel, row, val, payload, inv)
            self._syntax_capability_fact(val, unis, rel)
            if rel == "clones":
                self._clone_body(val, payload, unis, inv)
        return out

    def _snapshot_joins(self, rel, row, fact, payload, inv):
        for j in row["snapshotJoins"]:
            if "unless" in j and payload.get(j["unless"]["field"]) == j["unless"]["equals"]:
                continue
            p = payload[j["pathField"]]
            if p not in inv:
                self.fault("SNAPSHOT_JOIN_PATH_NOT_INVENTORIED", "%s %s" % (rel, p))
                continue
            if j["form"] == "inventoried-file":
                if inv[p]["sha256"] != payload[j["digestField"]]:
                    self.fault("SNAPSHOT_JOIN_DIGEST", p)
                elif inv[p]["bytes"] != payload[j["lengthField"]]:
                    self.fault("SNAPSHOT_JOIN_LENGTH", p)
                elif not self.s.has(payload[j["digestField"]]):
                    self.fault("EVIDENCE_UNAVAILABLE", "file bytes " + p)
                elif raw_sha256(self.s.get(payload[j["digestField"]])) != payload[j["digestField"]]:
                    self.fault("SNAPSHOT_JOIN_REHASH", p)
                for a in fact["anchors"]:
                    if a["path"] != p:
                        self.fault("SNAPSHOT_JOIN_ANCHOR_PATH", a["path"])

    def _syntax_capability_fact(self, fact, unis, rel):
        """native section 1.2 boundary (2): every anchor path of a fact under a
        syntax universe must be read by a SELECTED grammar bearing relation@rung.
        Inventory relations are exempt from grammar ownership at BOTH boundaries."""
        u = unis.get(fact["sourceUniverse"])
        if u is None or u[0] != "native.semantic-universe.syntax.v2":
            return
        key = (rel, fact["resolution"])
        if key in INVENTORY_CAPS:
            return
        uni, ctx = u[1], u[3]
        sel = set(uni["selectedGrammarIds"])
        rows = [g for g in ctx["grammarBundle"]["grammars"] if g["grammarId"] in sel]
        cap = "%s@%s" % key
        for a in fact["anchors"]:
            owner = _longest_suffix_owner(a["path"], rows)
            if owner is None or cap not in GRAMMAR_CAP["languages"][owner["languageId"]]["capabilities"]:
                self.fault("SYNTAX_CAPABILITY_UNSUPPORTED_FACT",
                           "%s %s" % (cap, a["path"]))

    def _clone_body(self, fact, payload, unis, inv):
        """The framed body-identity join (relation registry clones.bodyIdentityJoin)."""
        u = unis.get(fact["sourceUniverse"])
        if u is None:
            return
        dom, uni, cdom, ctx = u
        row = DOMAIN_SETS["native-semantic-universe"][dom]
        lvb = row.get("languageVersionBinding")
        if lvb is None:
            self.fault("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", dom)
            return
        anchor = fact["anchors"][0]
        blv, cause = derive_body_language_version(lvb, ctx, uni, anchor["path"], self)
        if blv is None:
            self.fault("BODY_LANGUAGE_" + cause, anchor["path"])
            return
        errs = schemas.validate(blv, "identity", "#/$defs/body-language-version")
        if errs:
            self.fault("BODY_LANGUAGE_VERSION_SCHEMA", str(errs))
            return
        try:
            fr = self.s.get(suffix(payload["bodyIdentity"]))
        except EvidenceUnavailable:
            self.fault("EVIDENCE_UNAVAILABLE", "clone body frame")
            return
        if raw_sha256(fr) != suffix(payload["bodyIdentity"]):
            self.fault("BODY_FRAME_IDENTITY", payload["bodyIdentity"])
            return
        comps, err = _parse_body_frame(fr)
        if err:
            self.fault("BODY_FRAME_" + err, payload["bodyIdentity"])
            return
        tag, level_id, level_ver, lang_id, lang_ver, body_payload = comps
        self.need(tag == b"opensip.fact-identity.v1", "BODY_FRAME_DOMAIN_TAG")
        self.need(level_id.decode() == payload["normalisationLevel"],
                  "BODY_FRAME_LEVEL_ID")
        self.need(level_ver == bytes.fromhex(payload["normalisationVersion"]),
                  "BODY_FRAME_LEVEL_VERSION")
        if not self.s.has(payload["normalisationVersion"]):
            self.fault("EVIDENCE_UNAVAILABLE", "level specification bytes")
        self.need(lang_id.decode() == blv["languageId"], "BODY_FRAME_LANGUAGE_ID",
                  "%s vs derived %s" % (lang_id.decode(), blv["languageId"]))
        self.need(lang_ver == hashlib.sha256(C(blv)).digest(),
                  "BODY_FRAME_LANGUAGE_VERSION")
        self.need(blv["languageId"] in lvb["bodyLanguages"],
                  "BODY_FRAME_LANGUAGE_NOT_PRODUCED_BY_UNIVERSE", blv["languageId"])
        if payload["normalisationLevel"] == "L0-verbatim":
            src = self.s.get(anchor["blobDigest"])
            span = src[anchor["startByte"]:anchor["endByte"]]
            self.need(body_payload == struct.pack(">I", len(span)) + span,
                      "BODY_L0_PAYLOAD_NOT_ANCHOR_SPAN")
        else:
            self.need(_well_framed_token_stream(body_payload),
                      "BODY_TOKEN_STREAM_FRAMING")

    # ------------------------------------------------------------------
    def _coverage(self, plan, snap, unis, scopes, facts):
        out = {}
        for hexd, blob in list(self.s.blobs.items()):
            if not blob.startswith(osip.FRAME_PREFIX + b"\x00"):
                continue
            try:
                dom, val = osip.parse_frame(blob)
            except osip.AdmissionError:
                continue
            if dom != "coverage":
                continue
            errs = schemas.validate(val, "identity", "#/$defs/coverage")
            if errs:
                self.fault("COVERAGE_SCHEMA", str(errs[:2]))
                continue
            out["coverage2:" + hexd] = val
            self.need(val["payloadSchemaDigest"] == NATIVE_DOC_DIGEST,
                      "native.coverage-payload-schema-not-registered")
            if not self.s.has(val["payloadSchemaDigest"]):
                self.fault("EVIDENCE_UNAVAILABLE", "coverage payload schema document")
            payload = self.record(val["payloadDigest"], "native",
                                  "#/$defs/CoverageResultV3", "COVERAGE_PAYLOAD")
            if payload is None:
                continue
            scope = scopes.get(val["scopeId"])
            if scope is None:
                self.fault("COVERAGE_SCOPE_NOT_RETAINED", val["scopeId"])
                continue
            self._admit_coverage(val, payload, scope, unis, facts, snap)
        return out

    def _admit_coverage(self, cov, payload, scope, unis, facts, snap):
        """admit_coverage_result_v3, re-run at retained closure (native 4.1a/4.3/10)."""
        key, entry = payload["key"], payload["entry"]
        scope_hex = suffix(cov["scopeId"])
        for f, sv in (("relation", scope["relation"]), ("resolution", scope["resolution"]),
                      ("sourceUniverse", scope["sourceUniverse"]),
                      ("targetUniverse", scope["targetUniverse"])):
            self.need(key[f] == sv, "native.coverage-key-scope-mismatch:" + f,
                      "%r vs %r" % (key[f], sv))
        self.need(key["subjectScopeCommitment"] == "sha256:" + scope_hex,
                  "native.subject-scope-commitment-mismatch")
        self.need(entry["examinedUniverse"]["subjectScopeCommitment"]
                  == key["subjectScopeCommitment"],
                  "native.examined-universe-commitment-mismatch")
        self.need(entry["examinedUniverse"]["subjectCount"] == len(scope["subjects"]),
                  "native.examined-universe-subject-count-mismatch",
                  "%d vs %d" % (entry["examinedUniverse"]["subjectCount"],
                                len(scope["subjects"])))
        self.need(entry["relation"] == key["relation"]
                  and entry["resolution"] == key["resolution"],
                  "native.coverage-entry-key-mismatch")

        rel, rung = entry["relation"], entry["resolution"]
        # RC-0 : registered pair, decided before any fact is read
        if rel not in RELATIONS or rung not in RELATIONS[rel]["ladder"]:
            self.fault("RC0_PAIR_NOT_REGISTERED", "%s@%s" % (rel, rung))
            return
        rc = entry["resolutionCompleteness"]
        # RC-1
        if rung in RESOLVED_RUNGS:
            self.need(rc["state"] != "not-applicable", "RC1_RESOLVED_RUNG_NOT_APPLICABLE",
                      "%s@%s" % (rel, rung))
        else:
            self.need(rc["state"] == "not-applicable", "RC1_NON_RESOLVED_RUNG_STATE",
                      "%s@%s state=%s" % (rel, rung, rc["state"]))
            self.need(rc["attempted"] is False, "RC1_NON_RESOLVED_RUNG_ATTEMPTED")
            self.need(rc["unresolvedEdgeCount"] == 0, "RC1_NON_RESOLVED_RUNG_COUNT")
            self.need(rc["unresolvedEdgeClasses"] == [], "RC1_NON_RESOLVED_RUNG_CLASSES")
        # RC-2
        matching = [f for f in facts.values()
                    if f["relation"] == "unresolved-edge"
                    and f["sourceUniverse"] == key["sourceUniverse"]
                    and f["snapshotId"] == scope["snapshotId"]]
        if rc["state"] == "complete":
            self.need(rc["attempted"] is True and rc["examinedExhaustive"] is True
                      and rc["stageTerminal"] == "complete"
                      and rc["unresolvedEdgeCount"] == 0,
                      "RC2_COMPLETE_PRECONDITIONS")
        if rc["state"] == "incomplete":
            self.need(rc["unresolvedEdgeCount"] >= 1 and rc["stageTerminal"] == "complete"
                      and rc["examinedExhaustive"] is True, "RC2_INCOMPLETE_PRECONDITIONS")
        if rc["state"] == "not-attempted":
            self.need(rc["attempted"] is False and rc["unresolvedEdgeCount"] == 0,
                      "RC2_NOT_ATTEMPTED_PRECONDITIONS")
        if rc["state"] == "partial":
            self.need(rc["stageTerminal"] in ("unavailable", "budget-exhausted",
                                              "provider-fault", "cancelled", "crash")
                      or rc["examinedExhaustive"] is False,
                      "RC2_PARTIAL_PRECONDITIONS")

        self._deficiency_cause(entry)
        # guardOrder (identity-schemas scopeCapabilityLaw.guardOrder): the
        # PRODUCER boundary's suffix law first, then closure's own prerequisites
        # in their order - compilation ownership, then the syntax grammar
        # registry, then the suffix law as the backstop.
        self._scope_capability(entry, scope, unis, snap)
        self._dialect_prerequisite(entry, scope, unis)
        self._syntax_capability_scope(entry, scope, unis, snap)

    def _dialect_prerequisite(self, entry, scope, unis):
        """native section 10 clones-ownership disclosure: the owed
        (deficiency, nativeCause) is DERIVED from the committed ownership record
        and THIS scope's subjects, in the selection law's own order, and
        re-derived here independently of the claim."""
        if "bodyIdentityJoin" not in RELATIONS.get(entry["relation"], {}):
            return
        u = unis.get(scope["sourceUniverse"])
        if u is None:
            return
        dom, uni, cdom, ctx = u
        row = DOMAIN_SETS["native-semantic-universe"][dom]
        lvb = row.get("languageVersionBinding")
        if not lvb or lvb["dialect"].get("form") != "selected-compilation-target-edition":
            return
        owed = None
        own_ref = uni.get("sourceUnitOwnershipId")
        if own_ref is None:
            owed = ("input-closure-incomplete", "body-language-ownership-missing")
        else:
            own = self._nested(own_ref, "sha256-text")
            if own is None:
                owed = ("input-closure-incomplete", "body-language-ownership-missing")
            elif own["enumeration"] == "partial":
                # decided BEFORE any row is read
                owed = ("input-closure-incomplete", "body-language-owner-unenumerated")
            else:
                byid = {x["unitId"]: x for x in own["units"]}
                selected = set(own["selectedUnitIds"])
                for subj in scope["subjects"]:
                    eds = set()
                    for o in own["ownership"]:
                        if o["path"] != subj or o["unitId"] not in selected:
                            continue
                        un = byid.get(o["unitId"])
                        if un is None:
                            continue
                        eds.add(un["targetEdition"] if un["targetEdition"] is not None
                                else uni["edition"].get(un["crateName"]))
                    if len(eds) > 1:
                        owed = ("input-closure-incomplete", "body-language-owner-ambiguous")
                        break
        if owed is None:
            return
        if entry["coverage"] == "complete":
            self.fault("COVERAGE_DIALECT_PREREQUISITE",
                       "%s claimed complete while %s" % (entry["relation"], owed[1]))
        elif entry["deficiency"] is None:
            self.fault("COVERAGE_DIALECT_PREREQUISITE_UNDISCLOSED", str(owed))
        elif entry["deficiency"] != owed[0]:
            self.fault("COVERAGE_DIALECT_DEFICIENCY_MISMATCH",
                       "%s vs owed %s" % (entry["deficiency"], owed[0]))
        elif entry["nativeCause"] != owed[1]:
            self.fault("COVERAGE_DIALECT_CAUSE_MISMATCH",
                       "%s vs owed %s" % (entry["nativeCause"], owed[1]))

    def _deficiency_cause(self, entry):
        d, cause = entry["deficiency"], entry["nativeCause"]
        if d is None:
            self.need(cause is None, "native.coverage-cause-without-deficiency", str(cause))
            return
        row = DEF_CAUSE.get(d)
        if row is None:
            self.fault("native.coverage-cause-registry-row-missing", d)
            return
        mode = row["nativeCause"]
        if mode == "required":
            self.need(cause is not None, "native.coverage-cause-required", d)
            if cause is not None:
                self.need(cause in row["allowedCauses"],
                          "native.coverage-cause-not-for-deficiency", "%s:%s" % (d, cause))
        elif mode == "optional":
            if cause is not None:
                self.need(cause in row["allowedCauses"],
                          "native.coverage-cause-not-for-deficiency", "%s:%s" % (d, cause))
        elif mode == "must-be-null":
            self.need(cause is None, "native.coverage-cause-must-be-null",
                      "%s:%s" % (d, cause))
        if "relations" in row:
            self.need(entry["relation"] in row["relations"],
                      "native.coverage-cause-relation-not-in-scope",
                      "%s on %s" % (d, entry["relation"]))
        if "requires" in row:
            v = _first(_walk(entry, row["requires"]["path"]))
            self.need(v == row["requires"]["equals"],
                      "native.coverage-cause-carrier-unsupported", d)
        if "oneOf" in row:
            v = _first(_walk(entry, row["oneOf"]["path"]))
            self.need(v in row["oneOf"]["members"],
                      "native.coverage-cause-carrier-unsupported", "%s carrier=%r" % (d, v))
        if "contains" in row:
            v = _first(_walk(entry, row["contains"]["path"])) or []
            self.need(row["contains"]["member"] in v,
                      "native.coverage-cause-carrier-unsupported", d)

    def _scope_capability(self, entry, scope, unis, snap):
        """identity-schemas x-opensip-digest-domains/scopeCapabilityLaw."""
        u = unis.get(scope["sourceUniverse"])
        if u is None:
            return
        dom = u[0]
        row = DOMAIN_SETS["native-semantic-universe"][dom]
        lvb = row.get("languageVersionBinding")
        if not lvb or lvb["dialect"].get("form") != SCOPE_CAP_LAW["appliesToDialectForm"]:
            return
        rel = entry["relation"]
        if (rel, entry["resolution"]) in INVENTORY_CAPS:
            return
        if "bodyIdentityJoin" not in RELATIONS[rel]:
            return
        table = lvb["dialect"]["table"]
        if RELATIONS[rel]["subjectKind"] == "source-path":
            subjects = scope["subjects"]
            supported = bool(subjects) and all(
                _longest_suffix(p, table) is not None for p in subjects)
        else:
            supported = any(_longest_suffix(r["path"], table) is not None
                            for r in snap["sourceInventory"])
        if supported:
            return
        want = SCOPE_CAP_LAW["onUnsupportedScope"]
        if entry["coverage"] != want["coverage"]:
            self.fault("COVERAGE_SOURCE_VARIANT_UNSUPPORTED_SCOPE",
                       "%s@%s claimed %s" % (rel, entry["resolution"], entry["coverage"]))
        elif entry["deficiency"] != want["deficiency"]:
            self.fault("COVERAGE_SOURCE_VARIANT_DEFICIENCY_MISMATCH", str(entry["deficiency"]))
        elif entry["nativeCause"] != want["nativeCause"]:
            self.fault("COVERAGE_SOURCE_VARIANT_CAUSE_MISMATCH", str(entry["nativeCause"]))

    def _syntax_capability_scope(self, entry, scope, unis, snap):
        """native section 1.2 boundary (3)."""
        u = unis.get(scope["sourceUniverse"])
        if u is None or u[0] != "native.semantic-universe.syntax.v2":
            return
        uni, ctx = u[1], u[3]
        cap = "%s@%s" % (entry["relation"], entry["resolution"])
        if (entry["relation"], entry["resolution"]) in INVENTORY_CAPS:
            return
        sel = set(uni["selectedGrammarIds"])
        rows = [g for g in ctx["grammarBundle"]["grammars"] if g["grammarId"] in sel]
        available = False
        for r in snap["sourceInventory"]:
            owner = _longest_suffix_owner(r["path"], rows)
            if owner and cap in GRAMMAR_CAP["languages"][owner["languageId"]]["capabilities"]:
                available = True
                break
        if available:
            return
        if entry["coverage"] != "unknown":
            self.fault("SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE",
                       "%s claimed %s" % (cap, entry["coverage"]))
        elif entry["deficiency"] != "language-tier-unsupported":
            self.fault("SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH", str(entry["deficiency"]))
        elif entry["nativeCause"] != "capability-missing":
            self.fault("SYNTAX_CAPABILITY_CAUSE_MISMATCH", str(entry["nativeCause"]))

    # ------------------------------------------------------------------
    def _views(self, plan, ev, scopes, facts, covs, unis, snap):
        cov_roots = set()
        for vid in ev["viewIds"]:
            dom, view = self.h_object(suffix(vid), expect_domain="view",
                                      fault_code="VIEW_FRAME")
            if view is None:
                continue
            errs = schemas.validate(view, "identity", "#/$defs/view")
            if errs:
                self.fault("VIEW_SCHEMA", str(errs[:2]))
                continue
            self.need(view["planId"] == ev["planId"], "VIEW_PLAN_JOIN")
            cl = self._closure(view["producerClosure"])
            if cl is not None:
                self.need(cl["kind"] == "provider", "VIEW_PRODUCER_CLOSURE_KIND")
            self.need(view["producerClosure"] in plan["semanticClosures"],
                      "VIEW_PRODUCER_NOT_PLAN_SELECTED")
            for sid in view["scopeIds"]:
                self.need(sid in scopes, "VIEW_SCOPE_NOT_RETAINED", sid)
            for fid in view["facts"]:
                self.need(fid in facts, "VIEW_FACT_NOT_RETAINED", fid)
            for cid in view["coverageIds"]:
                self.need(cid in covs, "VIEW_COVERAGE_NOT_RETAINED", cid)
                if cid in covs:
                    cov_roots.add(cid)
                    self.need(covs[cid]["scopeId"] in view["scopeIds"],
                              "native.coverage-subject-scope-outside-view", cid)
            for sd in view["schemaDigests"]:
                if not self.s.has(sd):
                    self.fault("EVIDENCE_UNAVAILABLE", "view schema document " + sd)
            # every registered document a view admitted must be a member
            need_docs = set()
            if view["facts"]:
                need_docs.add(RELATION_DOC_DIGEST)
            if view["coverageIds"]:
                need_docs.add(NATIVE_DOC_DIGEST)
            self.need(need_docs <= set(view["schemaDigests"]),
                      "VIEW_SCHEMA_DIGESTS_INCOMPLETE",
                      str(sorted(need_docs - set(view["schemaDigests"]))))

            # existential fact/scope join
            for fid in view["facts"]:
                f = facts[fid]
                ok = any(scopes[s]["relation"] == f["relation"]
                         and scopes[s]["resolution"] == f["resolution"]
                         and scopes[s]["sourceUniverse"] == f["sourceUniverse"]
                         and scopes[s]["targetUniverse"] == f["targetUniverse"]
                         for s in view["scopeIds"] if s in scopes)
                self.need(ok, "VIEW_FACT_NO_MATCHING_SCOPE", fid)

            # coveragePartitionLaw: disjointness within one partition key, PER VIEW,
            # over EVERY referenced scope including scopes with no Coverage entry
            pkey = RELREG["coveragePartitionLaw"]["partitionKey"]
            parts = {}
            for sid in view["scopeIds"]:
                if sid not in scopes:
                    continue
                sc = scopes[sid]
                k = tuple(sc[x] for x in pkey)
                for other in parts.get(k, []):
                    inter = set(sc["subjects"]) & set(scopes[other]["subjects"])
                    if inter:
                        self.fault("SUBJECT_SCOPE_PARTITION_OVERLAP",
                                   "%s@%s subject %s" % (sc["relation"], sc["resolution"],
                                                         sorted(inter)[0]))
                parts.setdefault(k, []).append(sid)

            # coverageTotality (file@enumerated only)
            inv = {r["path"] for r in snap["sourceInventory"]}
            for cid in view["coverageIds"]:
                if cid not in covs:
                    continue
                payload = self.record(covs[cid]["payloadDigest"], "native",
                                      "#/$defs/CoverageResultV3", "COVERAGE_PAYLOAD")
                if payload is None:
                    continue
                entry = payload["entry"]
                relrow = RELATIONS.get(entry["relation"], {})
                tot = relrow.get("coverageTotality")
                if not tot or entry["resolution"] != tot["rung"]:
                    continue
                if entry["coverage"] != "complete":
                    continue
                sc = scopes.get(covs[cid]["scopeId"])
                if sc is None:
                    continue
                match_on = tot["matchOn"]
                paid = set()
                for fid in view["facts"]:
                    f = facts[fid]
                    if all(f[m] == sc[m] for m in match_on if m in f):
                        p = self.record(f["payloadDigest"], "relation",
                                        relrow["selector"], "FACT_PAYLOAD")
                        if p:
                            paid.add(p[tot["pathField"]])
                for subj in sc["subjects"]:
                    if subj in inv and subj not in paid:
                        self.fault("COVERAGE_INVENTORY_TOTALITY_OMITS_PATH", subj)
        self.need(set(ev["coverageIds"]) == cov_roots,
                  "EVIDENCE_COVERAGE_ROOTS_NOT_VIEW_UNION",
                  "%s vs %s" % (sorted(ev["coverageIds"]), sorted(cov_roots)))

    # ------------------------------------------------------------------
    def _proof(self, plan, proof, ev, covs, facts):
        pol = self.record(plan["policyDigest"], "policy-document",
                          "#/$defs/PolicyDocumentV1", "POLICY")
        prog = self.record(proof["ruleProgramDigest"], "policy-document",
                           "#/$defs/RuleProgramV1", "RULE_PROGRAM")
        if pol is not None and prog is not None:
            self.need(prog["policyDigest"] == plan["policyDigest"],
                      "RULE_PROGRAM_POLICY_DIGEST")
            expect = {"schemaVersion": 1, "policyDigest": plan["policyDigest"],
                      "rules": [{"ruleId": r["ruleId"],
                                 "ruleProgramRef": r["ruleProgramRef"],
                                 "emitWhen": r["emitWhen"]} for r in pol["rules"]]}
            self.need(C(prog) == C(expect), "RULE_PROGRAM_NOT_POLICY_PROJECTION")
            # CB3-MUST-2: minResolution is a rung of THIS atom's relation ladder,
            # over BOTH the Plan policy and the proof's compiled program
            for doc, name in ((pol, "policy"), (prog, "ruleProgram")):
                for r in doc["rules"]:
                    for addr, node in _address_nodes(r["emitWhen"]):
                        if node["op"] in ("and", "or", "not"):
                            continue
                        rel = node["relation"]
                        if rel in RELATIONS:
                            self.need(node["minResolution"] in RELATIONS[rel]["ladder"],
                                      "ATOM_MIN_RESOLUTION_NOT_IN_RELATION_LADDER",
                                      "%s %s %s@%s" % (name, r["ruleId"], rel,
                                                       node["minResolution"]))
                            self.need("evidence" not in node,
                                      "ATOM_NATIVE_RELATION_DECLARES_EVIDENCE_KIND", rel)
                        else:
                            self.need("evidence" in node,
                                      "ATOM_EVIDENCE_RELATION_WITHOUT_KIND", rel)
        for f in osip.check_order(proof["predicateProofs"], "predicate",
                                  "proof.predicateProofs"):
            self.fault("ORDER", str(f))
        input_refs = {(r["domain"], r["digest"]) for r in proof["evaluationInputRefs"]}
        for r in proof["evaluationInputRefs"]:
            self.need(r["domain"] in BY_DOMAIN, "PROOF_INPUT_DOMAIN_UNREGISTERED",
                      r["domain"])
            self.need(r["domain"] not in ("coverage-payload", "import-payload",
                                          "fact-payload"),
                      "PROOF_INPUT_PAYLOAD_DOMAIN_AS_ROOT", r["domain"])
        for imp in plan["importIds"]:
            self.need(("import", suffix(imp)) in input_refs,
                      "PROOF_PLAN_IMPORT_NOT_EVALUATED", imp)
        node_index = {}
        if prog is not None:
            for r in prog["rules"]:
                for addr, node in _address_nodes(r["emitWhen"]):
                    node_index[(r["ruleId"], addr)] = node
        for pp in proof["predicateProofs"]:
            for r in pp["inputRefs"]:
                self.need((r["domain"], r["digest"]) in input_refs,
                          "PREDICATE_INPUT_NOT_IN_EVALUATION_INPUTS", str(r))
            w = self.record(pp["witnessDigest"], "identity",
                            "#/$defs/predicate-witness", "WITNESS")
            if w is None:
                continue
            gp = self.record(w["programPredicateDigest"], "identity",
                             "#/$defs/program-predicate", "PROGRAM_PREDICATE")
            if gp is None:
                continue
            self.need(gp["ruleProgramDigest"] == proof["ruleProgramDigest"],
                      "PROGRAM_PREDICATE_RULE_PROGRAM")
            self.need(gp["ruleId"] == pp["ruleId"], "PROGRAM_PREDICATE_RULE_ID")
            self.need(gp["predicateId"] == pp["predicateId"], "PROGRAM_PREDICATE_ADDRESS")
            self.need(gp["operation"] == pp["operation"], "PROGRAM_PREDICATE_OPERATION")
            node = node_index.get((gp["ruleId"], gp["predicateId"]))
            if node is None:
                self.fault("PROGRAM_PREDICATE_NODE_NOT_IN_PROGRAM",
                           "%s@%s" % (gp["ruleId"], gp["predicateId"]))
                continue
            self.need(node["op"] == gp["operation"], "PROGRAM_PREDICATE_OP_MISMATCH")
            self.need(gp["nodeDigest"] == record_digest(node), "PROGRAM_PREDICATE_NODE_DIGEST")
            kids = _child_addresses(gp["predicateId"], node)
            self.need(sorted(w["childPredicateIds"]) == sorted(kids),
                      "WITNESS_CHILD_ADDRESSES", "%s vs %s" % (w["childPredicateIds"], kids))
            self.need(w["countLimit"] == (node.get("n") if node["op"] == "count-at-most"
                                          else None),
                      "WITNESS_COUNT_LIMIT")
            for fid in w["matchingFactIds"]:
                self.need(fid in facts, "WITNESS_FACT_NOT_RETAINED", fid)
            for cid in w["coverageIds"]:
                self.need(cid in covs, "WITNESS_COVERAGE_NOT_RETAINED", cid)
        for fid in proof["findingIds"]:
            self.need(fid in ev["findingIds"], "PROOF_FINDING_NOT_IN_EVIDENCE", fid)

    def report(self):
        return {"ok": not self.faults, "checks": self.checks,
                "faults": [{"code": c, "detail": d} for c, d in self.faults],
                "firstFault": (self.faults[0][0] if self.faults else None)}


# ---------------------------------------------------------------------------
def _walk(obj, path):
    cur = [obj]
    for step in path:
        nxt = []
        for c in cur:
            if step == "[]":
                if isinstance(c, list):
                    nxt.extend(c)
            elif isinstance(c, dict):
                if step in c:
                    nxt.append(c[step])
        cur = nxt
    return cur


def _walk_holder(obj, path):
    if not path:
        return [obj]
    return _walk(obj, path)


def _first(lst):
    return lst[0] if lst else None


def _fold(n: str) -> str:
    """native section 2.4: Unicode Default Case Conversion toLowercase(X), full,
    non-tailored, context-sensitive.  Python's str.lower() implements the full
    default lowercase mapping including Final_Sigma and U+0130 -> U+0069 U+0307."""
    return n.lower()


def _longest_suffix(path, table):
    best = None
    for sfx in table:
        if path.endswith(sfx) and (best is None or len(sfx) > len(best)):
            best = sfx
    return best


def _longest_suffix_owner(path, rows):
    best, owner = None, None
    for g in rows:
        for sfx in g["suffixes"]:
            if path.endswith(sfx) and (best is None or len(sfx) > len(best)):
                best, owner = sfx, g
    return owner


def _parse_body_frame(fr: bytes):
    i = 0
    comps = []
    try:
        for _ in range(5):
            n = fr[i]
            comps.append(fr[i + 1:i + 1 + n])
            i += 1 + n
        (plen,) = struct.unpack(">I", fr[i:i + 4])
        i += 4
        payload = fr[i:]
        if len(payload) != plen:
            return None, "PAYLOAD_LENGTH"
        comps.append(payload)
        return tuple(comps), None
    except Exception:
        return None, "MALFORMED"


def _well_framed_token_stream(payload: bytes) -> bool:
    try:
        (n,) = struct.unpack(">I", payload[:4])
        i = 4
        for _ in range(n):
            (kl,) = struct.unpack(">H", payload[i:i + 2])
            i += 2 + kl
            (vl,) = struct.unpack(">I", payload[i:i + 4])
            i += 4 + vl
        return i == len(payload)
    except Exception:
        return False


def _address_nodes(node, addr="p"):
    """identity section 3 node addressing: root 'p'; i-th operand of and/or at a
    is a.i (zero-based, shortest decimal); the operand of not at a is a.0."""
    yield addr, node
    if node.get("op") in ("and", "or"):
        for i, ch in enumerate(node["operands"]):
            yield from _address_nodes(ch, "%s.%d" % (addr, i))
    elif node.get("op") == "not":
        yield from _address_nodes(node["operand"], addr + ".0")


def _child_addresses(addr, node):
    if node.get("op") in ("and", "or"):
        return ["%s.%d" % (addr, i) for i in range(len(node["operands"]))]
    if node.get("op") == "not":
        return [addr + ".0"]
    return []


def derive_body_language_version(lvb, ctx, uni, anchor_path, cl=None):
    """The DERIVED body-language-version record (identity section 3;
    languageVersionBinding of the fact's sourceUniverse domain row)."""
    rec = {"schemaVersion": 1}
    for field, spec in lvb["fields"].items():
        if "const" in spec:
            rec[field] = spec["const"]
        else:
            v = ctx
            for step in spec["path"]:
                v = v.get(step) if isinstance(v, dict) else None
            if v is None:
                return None, "FIELD_ABSENT"
            rec[field] = v
    dial = lvb["dialect"]
    if dial["form"] == "closed-suffix-table":
        sfx = _longest_suffix(anchor_path, dial["table"])
        if sfx is None:
            return None, dial["onUnknown"].replace("BODY_LANGUAGE_", "")
        variant = dial["table"][sfx]
        rec["dialect"] = {dial["key"]: variant}
        rec["languageId"] = lvb["bodyLanguageByVariant"][variant]
    elif dial["form"] == "selected-compilation-target-edition":
        own_ref = uni.get("sourceUnitOwnershipId")
        if own_ref is None:
            return None, "OWNERSHIP_REQUIRED"
        own = cl._nested(own_ref, "sha256-text") if cl else None
        if own is None:
            return None, "OWNERSHIP_REQUIRED"
        # order of decision is fixed; each step has its own cause
        if own["enumeration"] == "partial":
            return None, "OWNER_UNENUMERATED"
        rows = [o for o in own["ownership"] if o["path"] == anchor_path]
        if not rows:
            return None, "OWNER_NOT_COMPILED"
        selected = set(own["selectedUnitIds"])
        sel_rows = [o for o in rows if o["unitId"] in selected]
        if not sel_rows:
            return None, "OWNER_NOT_SELECTED"
        byid = {u["unitId"]: u for u in own["units"]}
        eds = set()
        for o in sel_rows:
            u = byid.get(o["unitId"])
            if u is None:
                return None, "OWNER_NOT_COMPILED"
            eds.add(u["targetEdition"] if u["targetEdition"] is not None
                    else uni["edition"].get(u["crateName"]))
        if len(eds) != 1 or None in eds:
            return None, "OWNER_AMBIGUOUS"
        rec["dialect"] = {dial["key"]: eds.pop()}
        rec["languageId"] = lvb["bodyLanguage"]
    else:
        return None, "DIALECT_ABSENT"
    return rec, None
