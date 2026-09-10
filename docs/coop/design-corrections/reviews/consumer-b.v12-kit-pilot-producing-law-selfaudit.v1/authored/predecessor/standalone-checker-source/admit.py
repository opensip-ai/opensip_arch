"""Structural / identity / retained-closure admission of one exported graph.

Full semantic evaluator replay is outside this bounded review.
"""
from __future__ import annotations

import hashlib
import re
import struct
from typing import Any

from canonical import (
    AdmissionError,
    admit_json_bytes,
    capability_manifest_id,
    encode_c,
    encode_cve1,
    h_identity,
    parse_h_frame,
    sha256_hex,
)
from kit import DOMAIN_TO_PREFIX, PREFIX_TO_DOMAIN, Kit
from schema_validate import HEX64, SHA256_TEXT, TYPED_ID, SchemaBundle, check_order, merge_ref, resolve_pointer
from store import Store

PROOF_INPUT_FORBIDDEN = {"run", "semantic-evidence", "evaluation-seal", "proof-bundle"}
FINDING_EVIDENCE_DOMAINS = {"fact", "coverage", "import", "predicate-witness", "blob"}
INVENTORY_RELATIONS = {"file", "package", "vcs-change"}
SEMANTIC_RELATIONS = {"imports", "references", "calls", "types", "reachability", "unresolved-edge"}
CODE_SYNTAX_RELATIONS = {"declares", "literal", "control-flow"}
BODY_LANG_ENUM = {"typescript", "javascript", "rust"}
CODE_LANGUAGES = {"typescript", "javascript", "rust"}
DATA_LANGUAGES = {"json", "toml", "markdown", "yaml"}


class Law:
    def __init__(self, law_id: str, citation: str, description: str):
        self.id = law_id
        self.citation = citation
        self.description = description
        self.status = "notReached"  # notReached | executed-pass | executed-fail | diagnostic
        self.detail: dict | None = None


class Admit:
    def __init__(self, kit: Kit, schemas: SchemaBundle, store: Store, graph_name: str):
        self.kit = kit
        self.schemas = schemas
        self.store = store
        self.graph_name = graph_name
        self.laws: dict[str, Law] = {}
        self.first_refusal: dict | None = None
        self.diagnostics: list[dict] = []
        self.admitted: dict[tuple[str, str], Any] = {}  # (kind, digest) -> parsed
        self.frames: dict[str, tuple[str, Any]] = {}  # digest -> (domain, record)
        self.canonical_records: dict[str, Any] = {}
        self.raw_artifacts: dict[str, bytes] = {}
        self.reached_typed: set[str] = set()
        self.run: dict | None = None
        self.plan: dict | None = None
        self.snapshot: dict | None = None
        self.inventory_by_path: dict[str, dict] = {}
        self.closures: dict[str, dict] = {}
        self.native_contexts: dict[str, tuple[str, dict]] = {}  # hex -> (domain, rec)
        self.native_universes: dict[str, tuple[str, dict]] = {}
        self.facts: dict[str, dict] = {}
        self.scopes: dict[str, dict] = {}
        self.coverages: dict[str, dict] = {}
        self.views: dict[str, dict] = {}
        self.imports: dict[str, dict] = {}
        self.proof: dict | None = None
        self.evidence: dict | None = None
        self.seal: dict | None = None
        self.analysis_spec: dict | None = None
        self.config: dict | None = None
        self.exec_plan: dict | None = None
        self.execution_inputs: dict | None = None
        self.policy: dict | None = None
        self.rule_program: dict | None = None
        self.cap_bytes: bytes | None = None
        self.replay_result: dict | str = "UNEXECUTED"

    def law(self, law_id: str, citation: str, description: str) -> Law:
        if law_id not in self.laws:
            self.laws[law_id] = Law(law_id, citation, description)
        return self.laws[law_id]

    def mark_pass(self, law_id: str, citation: str, description: str, detail: dict | None = None) -> None:
        law = self.law(law_id, citation, description)
        if self.first_refusal is not None:
            if law.status == "notReached":
                law.status = "diagnostic"
            return
        if law.status == "notReached":
            law.status = "executed-pass"
            law.detail = detail

    def refuse(self, law_id: str, code: str, message: str, citation: str, operands: dict) -> None:
        law = self.law(law_id, citation, message)
        rec = {
            "lawId": law_id,
            "code": code,
            "message": message,
            "citation": citation,
            "operands": operands,
        }
        if self.first_refusal is None:
            self.first_refusal = rec
            law.status = "executed-fail"
            law.detail = rec
        else:
            rec["role"] = "diagnostic"
            self.diagnostics.append(rec)
            law.status = "diagnostic"
            law.detail = rec
        raise AdmissionError(code, message, citation, operands)

    def catch(self, law_id: str, citation: str, description: str, fn):
        try:
            fn()
            self.mark_pass(law_id, citation, description)
        except AdmissionError as e:
            if self.first_refusal is None:
                self.refuse(law_id, e.code, e.message, e.citation or citation, e.operands)
            else:
                self.diagnostics.append(
                    {"lawId": law_id, "code": e.code, "message": e.message, "citation": e.citation, "operands": e.operands, "role": "diagnostic"}
                )
                self.law(law_id, citation, description).status = "diagnostic"

    def run_admission(self) -> dict:
        try:
            self._phase_store()
            self._phase_run_root()
            self._phase_graph()
            self._phase_native()
            self._phase_relations()
            self._phase_coverage()
            self._phase_citations()
            self._phase_closures()
            self._phase_capability()
            self._phase_component()
            self._phase_execution_inputs()
            self._phase_joins()
            self.structural_ok = self.first_refusal is None
            self._phase_replay()
        except AdmissionError as e:
            if self.first_refusal is None:
                self.first_refusal = {
                    "lawId": "UNCAUGHT_ADMISSION_ERROR",
                    "code": e.code,
                    "message": e.message,
                    "citation": e.citation,
                    "operands": e.operands,
                }
                law = self.law("UNCAUGHT_ADMISSION_ERROR", e.citation, e.message)
                law.status = "executed-fail"
                law.detail = self.first_refusal
        except Exception as e:
            import traceback
            if self.first_refusal is None:
                self.first_refusal = {
                    "lawId": "CHECKER_FAULT",
                    "code": "CHECKER_FAULT",
                    "message": f"{type(e).__name__}: {e}",
                    "citation": "checker implementation (not a kit law)",
                    "operands": {"traceback": traceback.format_exc()},
                }
        structural_ok = getattr(self, "structural_ok", self.first_refusal is None and getattr(self, "replay_result", "UNEXECUTED") == "UNEXECUTED")
        # If replay refused, first_refusal is the semantic mismatch; structural_ok was captured before replay.
        if not hasattr(self, "structural_ok"):
            self.structural_ok = False
        replay = getattr(self, "replay_result", "UNEXECUTED")
        structural_verdict = "ADMIT" if self.structural_ok else "REFUSE"
        if not self.structural_ok:
            overall = "REFUSE"
        elif isinstance(replay, dict) and replay.get("status") == "REPLAY_MATCH":
            overall = "ADMIT"
        elif isinstance(replay, dict) and replay.get("status") == "REPLAY_REFUSE":
            overall = "SEMANTIC_REFUSE"
        else:
            overall = "INCOMPLETE"
        return {
            "graph": self.graph_name,
            "claimedRunId": self.store.claimed_run_id,
            "storeSha256": self.store.file_sha256,
            "storeBytes": self.store.file_bytes,
            "verdict": overall,
            "structuralVerdict": structural_verdict,
            "firstRefusal": self.first_refusal,
            "structuralFirstRefusal": None if self.structural_ok else self.first_refusal,
            "diagnostics": self.diagnostics,
            "laws": {
                lid: {
                    "citation": law.citation,
                    "description": law.description,
                    "status": law.status,
                    "detail": law.detail,
                }
                for lid, law in self.laws.items()
            },
            "replay": replay,
            "reachedTypedRecordCounts": {
                "facts": len(self.facts),
                "scopes": len(self.scopes),
                "coverages": len(self.coverages),
                "views": len(self.views),
                "imports": len(self.imports),
                "nativeContexts": len(self.native_contexts),
                "nativeUniverses": len(self.native_universes),
                "closures": len(self.closures),
            },
        }

    # ----- phases -----

    def _phase_store(self):
        citation = "identity-and-evidence.md§3 (raw SHA256 of exact retained artifact bytes)"
        errors = self.store.rehash_all_blobs()
        if errors:
            e0 = errors[0]
            self.refuse("L-BLOB-REHASH", e0["code"], "blob rehash failed", citation, e0.get("operands") or e0)
        self.mark_pass("L-BLOB-REHASH", citation, "every blobs[] member rehashes to its key", {"count": len(self.store.blobs)})
        self.mark_pass(
            "L-BLOBCOUNT",
            "export store blobCount",
            "blobCount equals blobs object size",
            {"count": len(self.store.blobs)},
        )

    def _phase_run_root(self):
        digest = self.store.claimed_run_digest()
        citation = "identity-and-evidence.md§3 domain run / run3; H frame"
        raw = self.store.require_blob(digest, citation, "claimedRunId")
        domain, rec, _ = parse_h_frame(raw, expected_domain="run")
        actual_h, _ = h_identity("run", rec)
        if actual_h != digest:
            self.refuse(
                "L-RUN-H",
                "H_MISMATCH",
                "recomputed H(run, descriptor) does not equal claimed Run digest",
                citation,
                {"claimed": digest, "actual": actual_h},
            )
        self.schemas.validate(rec, self.kit.identity_v3, "#/$defs/run", path="run")
        if rec.get("schemaVersion") != 3:
            self.refuse("L-RUN-MAJOR", "RUN_MAJOR", "run schemaVersion is not 3", "identity-schemas.v3.json#/x-opensip-evaluator-profile", {"schemaVersion": rec.get("schemaVersion")})
        typed = rec.get("evaluationSealId", "")
        self.run = rec
        self.admitted[("h-identity", digest)] = rec
        self.frames[digest] = (domain, rec)
        self.mark_pass("L-RUN-H", citation, "claimed Run H frame parses, C-roundtrips, and rehashes", {"digest": digest})
        self.mark_pass("L-RUN-SCHEMA", "identity-schemas.v3.json#/$defs/run", "run record validates including published keywords", {})

    def _phase_graph(self):
        assert self.run is not None
        self._admit_typed_id(self.run["snapshotId"], expected_domain="snapshot", field="run.snapshotId")
        self._admit_typed_id(self.run["planId"], expected_domain="plan", field="run.planId")
        self._admit_typed_id(self.run["evidenceId"], expected_domain="semantic-evidence", field="run.evidenceId")
        self._admit_typed_id(self.run["evaluationSealId"], expected_domain="evaluation-seal", field="run.evaluationSealId")
        self.snapshot = self._get_domain_rec("snapshot")
        self.plan = self._get_domain_rec("plan")
        self.evidence = self._get_domain_rec("semantic-evidence")
        self.seal = self._get_domain_rec("evaluation-seal")
        # Inventory must exist before native snapshotJoins (plan.nativeContextDigests).
        self._load_inventory()
        self._walk_identity_record("snapshot", self.snapshot, self.kit.identity_v3, "#/$defs/snapshot")
        self._walk_identity_record("plan", self.plan, self.kit.identity_v3, "#/$defs/plan")
        self._walk_identity_record("semantic-evidence", self.evidence, self.kit.identity_v3, "#/$defs/semantic-evidence")
        self._walk_identity_record("evaluation-seal", self.seal, self.kit.identity_v3, "#/$defs/evaluation-seal")
        # plan-selected native contexts, imports, closures
        self._admit_plan_children()

    def _load_inventory(self):
        inv = self.snapshot["sourceInventory"]
        if not isinstance(inv, list):
            self.refuse("L-INVENTORY-TYPE", "INVENTORY_TYPE", "sourceInventory is not an array", "identity-schemas.v3.json#/$defs/snapshot", {})
        check_order("path", inv, "snapshot.sourceInventory")
        paths = []
        for row in inv:
            p = row["path"]
            if p in self.inventory_by_path:
                self.refuse(
                    "L-INVENTORY-UNIQUE-PATH",
                    "DUPLICATE_INVENTORY_PATH",
                    "inventory paths must be unique even when digests differ",
                    "identity-and-evidence.md§3 (inventory paths unique; no tie-break)",
                    {"path": p},
                )
            self.inventory_by_path[p] = row
            paths.append(p)
            self._retain_raw(row["sha256"], "snapshot.sourceInventory[].sha256", "identity-schemas.v3.json#/$defs/Blob")
            blob = self.store.require_blob(row["sha256"], "identity-schemas.v3.json#/$defs/Blob", "inventory")
            if len(blob) != row["bytes"]:
                self.refuse(
                    "L-BLOB-LENGTH",
                    "BLOB_LENGTH",
                    "retained blob length does not equal inventory bytes",
                    "identity-and-evidence.md§3 Blob; security-and-lifecycle.md#S1",
                    {"path": p, "claimed": row["bytes"], "actual": len(blob)},
                )
        self.mark_pass("L-INVENTORY-UNIQUE-PATH", "identity-and-evidence.md§3", "inventory paths unique", {"n": len(paths)})

    def _admit_plan_children(self):
        plan = self.plan
        assert plan is not None
        check_order("canonical-set", plan["nativeContextDigests"], "plan.nativeContextDigests")
        check_order("canonical-set", plan["semanticClosures"], "plan.semanticClosures")
        check_order("canonical-set", plan["importIds"], "plan.importIds")
        ctx_set = set(plan["nativeContextDigests"])
        for hx in plan["nativeContextDigests"]:
            self._admit_h_domain_set(hx, "native-context", field="plan.nativeContextDigests[]")
        for cid in plan["semanticClosures"]:
            self._admit_typed_id(cid, expected_domain="closure", field="plan.semanticClosures[]")
        for iid in plan["importIds"]:
            self._admit_typed_id(iid, expected_domain="import", field="plan.importIds[]")
        # canonical records named by plan
        self.config = self._admit_canonical(
            plan["resolvedConfigDigest"],
            self.kit.identity_v3,
            "#/$defs/semantic-configuration",
            "plan.resolvedConfigDigest",
        )
        self.analysis_spec = self._admit_canonical(
            plan["analysisSpecDigest"],
            self.kit.identity_v3,
            "#/$defs/analysis-spec",
            "plan.analysisSpecDigest",
        )
        self._admit_canonical(plan["scopeDigest"], self.kit.identity_v3, "#/$defs/scope-descriptor", "plan.scopeDigest")
        self._admit_canonical(plan["semanticGrantDigest"], self.kit.identity_v3, "#/$defs/semantic-grant", "plan.semanticGrantDigest")
        self.policy = self._admit_canonical(
            plan["policyDigest"],
            self.kit.policy_v2,
            "#/$defs/PolicyDocumentV2",
            "plan.policyDigest",
        )
        self._admit_canonical(plan["waiverDigest"], self.kit.policy_v1, "#/$defs/WaiverSetV1", "plan.waiverDigest")
        self.cap_bytes = self._retain_raw(
            plan["capabilityManifestBytesDigest"],
            "plan.capabilityManifestBytesDigest",
            "identity-and-evidence.md§3 capabilityManifestBytesDigest raw-artifact",
        )
        # snapshot joins on plan
        if plan["snapshotId"] != self.run["snapshotId"]:
            self.refuse("L-PLAN-SNAPSHOT", "CROSS_SOURCE", "plan.snapshotId is not the Run snapshot", "identity-and-evidence.md§3 (every visited record joins current source)", {"plan": plan["snapshotId"], "run": self.run["snapshotId"]})
        if plan["resolvedConfigDigest"] != self.snapshot["resolvedConfigDigest"]:
            self.refuse("L-PLAN-CONFIG", "CONFIG_JOIN", "plan.resolvedConfigDigest != snapshot.resolvedConfigDigest", "identity-and-evidence.md§3 (snapshot config/scope and Plan config/scope must agree)", {})
        if plan["scopeDigest"] != self.snapshot["scopeDigest"]:
            self.refuse("L-PLAN-SCOPE", "SCOPE_JOIN", "plan.scopeDigest != snapshot.scopeDigest", "identity-and-evidence.md§3", {})
        # budget equality
        cfg_budget = (self.config or {}).get("analysis", {}).get("budget")
        if plan.get("budget") != cfg_budget:
            self.refuse(
                "L-PLAN-BUDGET",
                "BUDGET_MISMATCH",
                "Plan.budget must equal, exactly and by type, analysis.budget of the committed resolved semantic configuration",
                "identity-and-evidence.md§3 (Plan deterministic budget)",
                {"planBudget": plan.get("budget"), "configBudget": cfg_budget},
            )
        self.mark_pass("L-PLAN-BUDGET", "identity-and-evidence.md§3", "plan.budget equals config.analysis.budget", {})
        self._admit_analysis_spec_parameters()
        # evidence / seal children
        ev = self.evidence
        se = self.seal
        self._admit_typed_id(ev["proofBundleId"], expected_domain="proof-bundle", field="evidence.proofBundleId")
        self.proof = self._get_domain_rec("proof-bundle")
        self._walk_identity_record("proof-bundle", self.proof, self.kit.identity_v3, "#/$defs/proof-bundle")
        for vid in ev["viewIds"]:
            self._admit_typed_id(vid, expected_domain="view", field="evidence.viewIds[]")
        for cid in ev["coverageIds"]:
            self._admit_typed_id(cid, expected_domain="coverage", field="evidence.coverageIds[]")
        if ev["importIds"] != plan["importIds"]:
            self.refuse(
                "L-EVIDENCE-IMPORTS",
                "IMPORT_SET_MISMATCH",
                "semantic-evidence.importIds must repeat the Plan-selected import set exactly",
                "identity-and-evidence.md§3",
                {"evidence": ev["importIds"], "plan": plan["importIds"]},
            )
        self.mark_pass("L-EVIDENCE-IMPORTS", "identity-and-evidence.md§3", "evidence.importIds equals plan.importIds", {})
        if ev["planId"] != self.run["planId"] or se["planId"] != self.run["planId"]:
            self.refuse("L-EVIDENCE-PLAN", "CROSS_PLAN", "evidence/seal planId is not the Run plan", "identity-and-evidence.md§3", {})
        if se["proofBundleId"] != ev["proofBundleId"]:
            self.refuse("L-SEAL-PROOF", "SEAL_PROOF", "seal.proofBundleId != evidence.proofBundleId", "identity-and-evidence.md§3", {})
        if se["evidenceId"] != self.run["evidenceId"]:
            self.refuse("L-SEAL-EVIDENCE", "SEAL_EVIDENCE", "seal.evidenceId != run.evidenceId", "identity-and-evidence.md§3", {})
        if se["verdict"] != self.proof["verdict"]:
            self.refuse("L-SEAL-VERDICT", "SEAL_VERDICT", "seal.verdict != proof.verdict", "identity-and-evidence.md§3", {})
        self._admit_typed_id(self.proof["executionPlanId"], expected_domain="execution-plan", field="proof.executionPlanId")
        self.exec_plan = self._get_domain_rec("execution-plan")
        self._walk_identity_record("execution-plan", self.exec_plan, self.kit.identity_v3, "#/$defs/execution-plan")
        self.rule_program = self._admit_canonical(
            self.proof["ruleProgramDigest"],
            self.kit.policy_v2,
            "#/$defs/RuleProgramV2",
            "proof.ruleProgramDigest",
        )
        self.execution_inputs = self._admit_canonical(
            self.proof["executionInputsDigest"],
            self.kit.execution_inputs_schema,
            "#",
            "proof.executionInputsDigest",
        )
        # views
        for vid in ev["viewIds"]:
            hx = vid.split(":", 1)[1]
            view = self.frames[hx][1]
            self.views[hx] = view
            self._walk_identity_record("view", view, self.kit.identity_v3, "#/$defs/view")
            self._admit_view(view, hx)
        self.mark_pass("L-GRAPH-WALK", "identity-and-evidence.md§3 complete closure", "reachable typed identity records fetched, framed, schema-validated", {})

    def _admit_view(self, view: dict, view_hex: str):
        if view["planId"] != self.run["planId"]:
            self.refuse("L-VIEW-PLAN", "CROSS_PLAN", "view.planId is not the Run plan", "identity-and-evidence.md§3", {"view": view_hex})
        producer = view["producerClosure"]
        if producer not in self.plan["semanticClosures"]:
            self.refuse(
                "L-VIEW-PRODUCER-SELECTED",
                "CLOSURE_NOT_SELECTED",
                "view.producerClosure is not in plan.semanticClosures",
                "identity-schemas.v3.json#/x-opensip-digest-domains/closureMembership",
                {"producerClosure": producer},
            )
        for fid in view["facts"]:
            self._admit_typed_id(fid, expected_domain="fact", field="view.facts[]")
            hx = fid.split(":", 1)[1]
            fact = self.frames[hx][1]
            self.facts[hx] = fact
            self._walk_identity_record("fact", fact, self.kit.identity_v3, "#/$defs/fact")
            if fact["snapshotId"] != self.run["snapshotId"]:
                self.refuse("L-FACT-SNAPSHOT", "CROSS_SOURCE", "fact.snapshotId is not the Run snapshot", "identity-and-evidence.md§3", {"fact": hx})
            if fact["producerClosure"] != producer:
                self.refuse(
                    "L-FACT-PRODUCER",
                    "FACT_PRODUCER_NE_VIEW",
                    "fact.producerClosure must equal its view.producerClosure",
                    "identity-schemas.v3.json#/x-opensip-digest-domains/closureMembership equalToDirect",
                    {"fact": hx, "factProducer": fact["producerClosure"], "viewProducer": producer},
                )
        for sid in view["scopeIds"]:
            self._admit_typed_id(sid, expected_domain="subject-scope", field="view.scopeIds[]")
            hx = sid.split(":", 1)[1]
            scope = self.frames[hx][1]
            self.scopes[hx] = scope
            self._walk_identity_record("subject-scope", scope, self.kit.identity_v3, "#/$defs/subject-scope")
            if scope["snapshotId"] != self.run["snapshotId"]:
                self.refuse("L-SCOPE-SNAPSHOT", "CROSS_SOURCE", "subject-scope.snapshotId is not the Run snapshot", "identity-and-evidence.md§3", {"scope": hx})
            enum_c = scope["enumeratorClosure"]
            if enum_c not in self.plan["semanticClosures"]:
                self.refuse("L-SCOPE-ENUMERATOR", "CLOSURE_NOT_SELECTED", "enumeratorClosure not in plan.semanticClosures", "identity-schemas.v3.json#/x-opensip-digest-domains/closureMembership", {"scope": hx})
        for cid in view["coverageIds"]:
            self._admit_typed_id(cid, expected_domain="coverage", field="view.coverageIds[]")
            hx = cid.split(":", 1)[1]
            cov = self.frames[hx][1]
            self.coverages[hx] = cov
            self._walk_identity_record("coverage", cov, self.kit.identity_v3, "#/$defs/coverage")
        for d in view["schemaDigests"]:
            self._retain_raw(d, "view.schemaDigests[]", "identity-and-evidence.md§3 registered-schema-document")
            self._check_registered_schema_document(d)

    def _admit_analysis_spec_parameters(self):
        spec = self.analysis_spec
        assert spec is not None
        citation = "identity-and-evidence.md§3 payload registry parameter class; identity-schemas.v3.json#/x-opensip-payload-registry"
        check_order("canonical-set", spec["parameters"], "analysis-spec.parameters")
        rows = self.kit.payload_registry["classes"]["parameter"]["rows"]
        # map document relative path -> sha256
        doc_sha = {}
        for row_key, row in rows.items():
            doc = row["document"]
            sha = self.kit.sha256_of(doc)
            doc_sha[sha] = (row_key, row)
        # ambiguous row: two rows same document digest
        by_sha: dict[str, list] = {}
        for sha, (rk, row) in doc_sha.items():
            by_sha.setdefault(sha, []).append(rk)
        for sha, keys in by_sha.items():
            if len(keys) > 1:
                self.refuse("L-PARAM-AMBIGUOUS-ROW", "PAYLOAD_PARAMETER_AMBIGUOUS_ROW", "two parameter rows share one document digest", citation, {"rows": keys, "sha256": sha})
        counts: dict[str, int] = {}
        required_eval3 = set()
        for row_key, row in rows.items():
            if 3 in (row.get("requiredForEvaluatorMajors") or []):
                required_eval3.add(self.kit.sha256_of(row["document"]))
        seen_required = set()
        for i, param in enumerate(spec["parameters"]):
            sd = param["schemaDigest"]
            pd = param["payloadDigest"]
            self._retain_raw(sd, f"analysis-spec.parameters[{i}].schemaDigest", citation)
            if sd not in doc_sha:
                self.refuse(
                    "L-PARAM-UNREGISTERED",
                    "PAYLOAD_UNREGISTERED",
                    "analysis-spec parameter schemaDigest is not a registered parameter document",
                    citation,
                    {"schemaDigest": sd},
                )
            row_key, row = doc_sha[sd]
            counts[sd] = counts.get(sd, 0) + 1
            selector = row["selector"]
            document = self.schemas.document(row["document"].split("/")[-1] if False else row["document"])
            # document path as in kit
            document = self._doc_for_payload_path(row["document"])
            self._admit_canonical(pd, document, selector, f"analysis-spec.parameters[{i}].payloadDigest")
            if sd in required_eval3:
                seen_required.add(sd)
        for sd, n in counts.items():
            if n > 1:
                self.refuse(
                    "L-PARAM-SELECTION-AMBIGUOUS",
                    "ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS",
                    "one Plan selects at most one parameter per registered row",
                    citation + " selectionCardinality",
                    {"schemaDigest": sd, "count": n},
                )
        missing = required_eval3 - seen_required
        if missing:
            self.refuse(
                "L-PARAM-EVAL3-REQUIRED",
                "EVALUATOR3_PARAMETER_MISSING",
                "evaluator3 requires exactly one enumeration-plan and one emission-plan parameter",
                "identity-schemas.v3.json#/x-opensip-payload-registry/classes/parameter/rows",
                {"missingSchemaDigests": sorted(missing)},
            )
        self.mark_pass("L-PARAM-SELECTION", citation, "parameter class closed, at most one per row, evaluator3 required rows present", {"n": len(spec["parameters"])})

    def _doc_for_payload_path(self, document: str) -> dict:
        # document is like foundation/enumeration-plan.schema.v1.json
        return json_doc(self.kit, document)

    # ----- retain / admit primitives -----

    def _retain_raw(self, digest: str, field: str, citation: str) -> bytes:
        raw = self.store.require_blob(digest, citation, field)
        self.raw_artifacts[digest] = raw
        return raw

    def _admit_canonical(self, digest: str, document: dict, selector: str, field: str) -> Any:
        citation = f"identity-and-evidence.md§3 canonical-record {field} {selector}"
        raw = self.store.require_blob(digest, citation, field)
        parsed = admit_json_bytes(raw, profile="product", citation=citation)
        recomputed = encode_c(parsed, profile="product")
        if recomputed != raw:
            self.refuse("L-C-IDENTITY", "C_BYTE_IDENTITY", "canonical-record bytes are not C(parse)", citation, {"field": field, "digest": digest})
        if sha256_hex(raw) != digest:
            self.refuse("L-CANONICAL-SHA", "CANONICAL_SHA", "SHA256(C(record)) != digest", citation, {"field": field})
        self.schemas.validate(parsed, document, selector, path=field)
        # order keywords already in schema validate; also walk
        self._walk_schema_instance(document, selector, parsed, field, document)
        self.canonical_records[digest] = parsed
        self.admitted[("canonical-record", digest)] = parsed
        return parsed

    def _admit_typed_id(self, typed: str, *, expected_domain: str, field: str) -> Any:
        m = TYPED_ID.match(typed)
        if not m:
            self.refuse("L-TYPED-ID", "TYPED_ID_SYNTAX", "typed identity does not match prefix:hex64", "identity-and-evidence.md§3", {"field": field, "value": typed})
        prefix, hx = m.group(1), m.group(2)
        domain = PREFIX_TO_DOMAIN.get(prefix)
        if domain != expected_domain:
            self.refuse(
                "L-TYPED-PREFIX",
                "TYPED_PREFIX_DOMAIN",
                "typed prefix does not map to the expected H domain",
                "identity-and-evidence.md§3 domain table; identity-schemas.v3.json#/x-opensip-evaluator-profile",
                {"field": field, "prefix": prefix, "expectedDomain": expected_domain, "mapped": domain},
            )
        return self._admit_h(hx, domain, field)

    def _admit_h(self, digest: str, domain: str, field: str) -> Any:
        key = ("h-identity", digest)
        if key in self.admitted:
            rec = self.admitted[key]
            if self.frames.get(digest, (None, None))[0] not in (None, domain) and self.frames[digest][0] != domain:
                self.refuse("L-H-DOMAIN-DRIFT", "H_DOMAIN_DRIFT", "same digest admitted under two H domains", "identity-and-evidence.md§3", {"digest": digest, "field": field})
            return rec
        citation = f"identity-and-evidence.md§3 h-identity domain={domain} field={field}"
        raw = self.store.require_blob(digest, citation, field)
        d, rec, payload = parse_h_frame(raw, expected_domain=domain)
        actual, _ = h_identity(domain, rec)
        if actual != digest:
            self.refuse("L-H-RECOMPUTE", "H_MISMATCH", "recomputed H does not equal digest", citation, {"field": field, "claimed": digest, "actual": actual, "domain": domain})
        selector = "#/$defs/" + domain
        if domain not in self.kit.identity_v3["$defs"]:
            self.refuse("L-H-DEF", "UNKNOWN_IDENTITY_DEF", "identity-schemas.v3 has no $defs for this domain", citation, {"domain": domain})
        self.schemas.validate(rec, self.kit.identity_v3, selector, path=field)
        self.admitted[key] = rec
        self.frames[digest] = (d, rec)
        self.reached_typed.add(domain + ":" + digest)
        if domain == "closure":
            self.closures[digest] = rec
            self._admit_closure(rec, digest)
        if domain == "import":
            self.imports[digest] = rec
            self._admit_import(rec, digest)
        return rec

    def _admit_h_domain_set(self, digest: str, domain_set_name: str, field: str) -> Any:
        citation = f"identity-and-evidence.md§3 domainSet {domain_set_name} field={field}"
        raw = self.store.require_blob(digest, citation, field)
        allowed = set(self.kit.domain_sets[domain_set_name].keys())
        d, rec, payload = parse_h_frame(raw, expected_domains=allowed)
        actual, _ = h_identity(d, rec)
        if actual != digest:
            self.refuse("L-H-RECOMPUTE-SET", "H_MISMATCH", "recomputed H does not equal digest", citation, {"claimed": digest, "actual": actual, "domain": d})
        row = self.kit.domain_sets[domain_set_name][d]
        document = json_doc(self.kit, row["document"])
        self.schemas.validate(rec, document, row["selector"], path=field)
        self._walk_schema_instance(document, row["selector"], rec, field, document)
        self.admitted[("h-identity", digest)] = rec
        self.frames[digest] = (d, rec)
        if domain_set_name == "native-context":
            self.native_contexts[digest] = (d, rec)
        elif domain_set_name == "native-semantic-universe":
            self.native_universes[digest] = (d, rec)
        # nested identities / records / blobs from domain set row
        self._apply_domain_set_row(row, rec, digest, field)
        if domain_set_name == "native-context":
            self._admit_native_context(d, rec, digest, row)
        elif domain_set_name == "native-semantic-universe":
            self._bind_universe(d, rec, digest, row)
        return rec

    def _apply_domain_set_row(self, row: dict, rec: Any, digest: str, field: str):
        for nj in row.get("nestedIdentities") or []:
            vals = path_collect(rec, nj["path"])
            if not vals and nj.get("nullable"):
                continue
            form = nj.get("form")
            ds = nj.get("domainSet", "native-nested")
            for val in vals:
                if val is None and nj.get("nullable"):
                    continue
                hx = strip_hex(val, form)
                if hx is None:
                    if nj.get("nullable") and val is None:
                        continue
                    self.refuse("L-NESTED-ID", "NESTED_IDENTITY_FORM", "nested identity spelling does not match form", "identity-and-evidence.md§3 nestedIdentities", {"path": nj["path"], "value": val, "form": form})
                self._admit_h_domain_set(hx, ds, field=field + "." + ".".join(str(p) for p in nj["path"]))
        for nr in row.get("nestedRecords") or []:
            val = path_get(rec, nr["path"])
            if val is None and nr.get("nullable"):
                continue
            if val is None:
                continue
            hx = strip_hex(val, nr.get("form", "canonical-record"))
            if hx is None:
                # sometimes the path IS the digest field (bare hex)
                if isinstance(val, str) and HEX64.match(val):
                    hx = val
                else:
                    self.refuse("L-NESTED-REC", "NESTED_RECORD_DIGEST", "nested record digest missing", "identity-and-evidence.md§3 nestedRecords", {"path": nr["path"]})
            document = json_doc(self.kit, nr["document"])
            nested = self._admit_canonical(hx, document, nr["selector"], field + "." + ".".join(nr["path"]))
            for bj in nr.get("blobJoins") or []:
                self._apply_blob_join(nested, bj, field)
        for bj in row.get("blobJoins") or []:
            self._apply_blob_join(rec, bj, field)
        for sj in row.get("snapshotJoins") or []:
            self._apply_snapshot_join_generic(rec, sj, field)

    def _apply_blob_join(self, rec: Any, join: dict, field: str):
        nodes = path_collect(rec, join.get("path") or [])
        dfield = join.get("digestField")
        lfield = join.get("lengthField")
        for node in nodes:
            if dfield:
                if isinstance(node, dict) and dfield in node:
                    digest = strip_hex(node[dfield], "bare-hex") or (node[dfield] if isinstance(node[dfield], str) and HEX64.match(node[dfield]) else None)
                    if not digest:
                        continue
                    raw = self._retain_raw(digest, field + "." + dfield, "identity-and-evidence.md§3 blobJoins")
                    if lfield and lfield in node and len(raw) != node[lfield]:
                        self.refuse("L-BLOBJOIN-LEN", "BLOB_LENGTH", "blobJoin length mismatch", "identity-and-evidence.md§3 nested blobJoins", {"field": lfield, "claimed": node[lfield], "actual": len(raw)})
            else:
                # digest on the node itself
                if isinstance(node, dict) and dfield is None:
                    pass

    def _apply_snapshot_join_generic(self, rec: Any, join: dict, field: str):
        form = join.get("form")
        citation = "identity-and-evidence.md§3 native snapshotJoins; identity-schemas.v3.json domainSets"
        if form == "inventoried-paths":
            val = path_get(rec, join["path"])
            paths = val if isinstance(val, list) else []
            pfield = join.get("pathField")
            for item in paths:
                p = item[pfield] if pfield and isinstance(item, dict) else item
                if p not in self.inventory_by_path:
                    self.refuse("L-SNAPSHOT-PATH", "PATH_NOT_INVENTORIED", "named path is not in snapshot inventory", citation, {"path": p, "field": field})
        elif form == "inventoried-path-and-digest":
            node = path_get(rec, join["path"])
            if node is None and join.get("nullable"):
                return
            p = node[join["pathField"]]
            d = node[join["digestField"]]
            if p not in self.inventory_by_path:
                self.refuse("L-SNAPSHOT-LOCKFILE-PATH", "PATH_NOT_INVENTORIED", "lockfile path not inventoried", citation, {"path": p})
            row = self.inventory_by_path[p]
            if row["sha256"] != d:
                self.refuse("L-SNAPSHOT-LOCKFILE-DIGEST", "INVENTORY_DIGEST_MISMATCH", "lockfile contentSha256 != inventory digest", citation, {"path": p, "claimed": d, "inventory": row["sha256"]})

    def _admit_closure(self, rec: dict, digest: str):
        kind = rec["kind"]
        self._retain_raw(rec["manifestDigest"], "closure.manifestDigest", "identity-schemas.v3.json#/$defs/closure")
        check_order("path", rec["tree"], "closure.tree")
        for blob in rec["tree"]:
            raw = self._retain_raw(blob["sha256"], "closure.tree[].sha256", "identity-schemas.v3.json#/$defs/Blob")
            if len(raw) != blob["bytes"]:
                self.refuse("L-CLOSURE-TREE-LEN", "BLOB_LENGTH", "closure tree blob length mismatch", "security-and-lifecycle.md#S1", {"path": blob["path"], "claimed": blob["bytes"], "actual": len(raw)})
        self.mark_pass("L-CLOSURE-TREE", "identity-and-evidence.md§3; security-and-lifecycle.md#S1", "closure tree files retained with matching length", {"digest": digest, "kind": kind, "n": len(rec["tree"])})

    def _admit_import(self, rec: dict, digest: str):
        citation = "identity-and-evidence.md§3 payload registry import class; native-evidence.md§7.1"
        self._retain_raw(rec["payloadSchemaDigest"], "import.payloadSchemaDigest", citation)
        rows = self.kit.payload_registry["classes"]["import"]["rows"]
        payload = None
        # payload is canonical-record keyed by kind + payload.payloadDomain
        # We need the payload bytes first to read payloadDomain. Chicken-egg: keyedBy includes payload.payloadDomain.
        # Fetch payloadDigest as C bytes, parse, then verify schema digest against the row.
        raw_payload = self.store.require_blob(rec["payloadDigest"], citation, "import.payloadDigest")
        payload = admit_json_bytes(raw_payload, profile="product", citation=citation)
        if encode_c(payload, profile="product") != raw_payload:
            self.refuse("L-IMPORT-PAYLOAD-C", "C_BYTE_IDENTITY", "import payload is not C", citation, {"digest": rec["payloadDigest"]})
        domain = payload.get("payloadDomain")
        key = f"{rec['kind']}|{domain}"
        if key not in rows:
            self.refuse("L-IMPORT-UNREGISTERED", "PAYLOAD_UNREGISTERED", "import kind+payloadDomain has no registry row", citation, {"key": key})
        row = rows[key]
        expected_schema_sha = self.kit.sha256_of(row["document"])
        if rec["payloadSchemaDigest"] != expected_schema_sha:
            self.refuse(
                "L-IMPORT-SCHEMA-DIGEST",
                "PAYLOAD_SCHEMA_DIGEST",
                "import.payloadSchemaDigest is not SHA256 of the registered full schema document",
                citation,
                {"claimed": rec["payloadSchemaDigest"], "expected": expected_schema_sha, "document": row["document"]},
            )
        document = json_doc(self.kit, row["document"])
        self.schemas.validate(payload, document, row["selector"], path="import.payload")
        self.canonical_records[rec["payloadDigest"]] = payload
        for aux, docrel, sel in (
            ("sourceCorrespondenceDigest", "docs/coop/design-corrections/workflows/schemas/common.schema.json", "#/$defs/SourceCorrespondence"),
            ("buildDigest", "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json", "#/$defs/BuildIdentityV1"),
            ("observationDigest", "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json", "#/$defs/ImportObservationV1"),
        ):
            self._admit_canonical(rec[aux], json_doc(self.kit, docrel), sel, "import." + aux)
        self._admit_canonical(rec["scopeDigest"], self.kit.identity_v3, "#/$defs/scope-descriptor", "import.scopeDigest")
        for b in rec["blobs"]:
            raw = self._retain_raw(b["sha256"], "import.blobs[].sha256", citation)
            if len(raw) != b["bytes"]:
                self.refuse("L-IMPORT-BLOB-LEN", "BLOB_LENGTH", "import blob length mismatch", citation, {"path": b.get("path")})
        self._admit_typed_id(rec["producerClosure"], expected_domain="closure", field="import.producerClosure")
        self._admit_typed_id(rec["adapterClosure"], expected_domain="closure", field="import.adapterClosure")
        self.mark_pass("L-IMPORT-PAYLOAD", citation, "imported payload admitted under registry row", {"kind": rec["kind"], "payloadDomain": domain})

    def _get_domain_rec(self, domain: str) -> dict:
        for digest, (d, rec) in self.frames.items():
            if d == domain:
                return rec
        self.refuse("L-DOMAIN-MISSING", "DOMAIN_MISSING", f"no admitted {domain} record", "identity-and-evidence.md§3", {"domain": domain})
        raise AssertionError

    def _walk_identity_record(self, domain: str, rec: dict, document: dict, selector: str):
        self._walk_schema_instance(document, selector, rec, domain, document)

    def _walk_schema_instance(self, document: dict, selector: str, instance: Any, path: str, root_doc: dict):
        schema = resolve_pointer(document, selector) if selector not in ("#", "") else document
        self._walk_node(schema, instance, path, root_doc, 0)

    def _walk_node(self, schema: Any, instance: Any, path: str, root_doc: dict, depth: int):
        if depth > 64 or not isinstance(schema, dict):
            return
        schema = merge_ref(schema, root_doc)
        if "x-opensip-order" in schema and isinstance(instance, list):
            check_order(schema["x-opensip-order"], instance, path)
        if "x-opensip-digest" in schema and isinstance(instance, str):
            self._apply_digest_annotation(schema["x-opensip-digest"], instance, path, schema)
        # Unannotated 64-hex refusal is closed to identity-schemas.v3 (closing digest law).
        # Other documents may use 64-hex without that annotation; they have their own owners.
        pat = schema.get("pattern")
        identity_root = root_doc.get("$id") == "urn:opensip:product-v1:identity:v3"
        if (
            identity_root
            and isinstance(instance, str)
            and isinstance(pat, str)
            and "x-opensip-digest" not in schema
            and HEX64.match(instance)
            and pat.startswith("^[0-9a-f]{64}")
            and schema.get("type") == "string"
            and not path.endswith("Hash")
        ):
            self.refuse(
                "L-HEX-UNANNOTATED",
                "DIGEST_UNANNOTATED",
                "64-hex field in identity-schemas.v3 carries no x-opensip-digest annotation",
                "identity-and-evidence.md§3 closing digest law (identity-schemas.v3 only)",
                {"path": path, "value": instance},
            )
        if isinstance(instance, str):
            m = TYPED_ID.match(instance)
            if m and "x-opensip-digest" not in schema:
                prefix, hx = m.group(1), m.group(2)
                if prefix in PREFIX_TO_DOMAIN:
                    self._admit_typed_id(instance, expected_domain=PREFIX_TO_DOMAIN[prefix], field=path)
            sm = SHA256_TEXT.match(instance)
            if sm and "x-opensip-digest" not in schema:
                # may be handled by annotation on parent after merge
                pass
        if isinstance(instance, dict) and isinstance(schema.get("properties"), dict):
            props = schema["properties"]
            addl = schema.get("additionalProperties", True)
            for k, v in instance.items():
                if k in props:
                    self._walk_node(props[k], v, path + "." + k, root_doc, depth + 1)
                elif isinstance(addl, dict):
                    self._walk_node(addl, v, path + "." + k, root_doc, depth + 1)
        if isinstance(instance, list) and "items" in schema:
            items = schema["items"]
            if isinstance(items, dict):
                for i, item in enumerate(instance):
                    self._walk_node(items, item, f"{path}[{i}]", root_doc, depth + 1)
        for branch_key in ("oneOf", "anyOf"):
            if branch_key in schema and isinstance(schema[branch_key], list):
                for alt in schema[branch_key]:
                    if not isinstance(alt, dict):
                        continue
                    # walk matching alternative only
                    try:
                        self.schemas.validate(instance, {"$defs": root_doc.get("$defs", {}), **(merge_ref(alt, root_doc) if "$ref" in alt or "type" in alt else alt)}, "#", path=path)
                    except AdmissionError:
                        continue
                    except Exception:
                        continue
                    else:
                        self._walk_node(alt, instance, path, root_doc, depth + 1)
                        break

    def _apply_digest_annotation(self, ann: dict, value: str, path: str, schema: dict):
        rep = ann.get("representation")
        ret = ann.get("retention", "preimage")
        citation = f"identity-and-evidence.md§3 x-opensip-digest {path} representation={rep} retention={ret}"
        if rep == "by-domain":
            # sibling domain on the object, not on this string
            return
        if ret == "derived":
            return  # handled at plan.capabilityManifestId
        if ret == "fragment":
            return  # program-predicate.nodeDigest located in rule program
        if ret == "owner-retained":
            return
        if rep == "raw-artifact":
            hx = HEX64.match(value)
            if not hx:
                self.refuse("L-RAW-SPELLING", "DIGEST_SPELLING", "raw-artifact field is not bare 64-hex", citation, {"path": path, "value": value})
            if ann.get("artifactClass") == "registered-schema-document":
                self._retain_raw(value, path, citation)
                self._check_registered_schema_document(value)
            else:
                self._retain_raw(value, path, citation)
            return
        if rep == "canonical-record":
            if not HEX64.match(value):
                self.refuse("L-CANON-SPELLING", "DIGEST_SPELLING", "canonical-record field is not bare 64-hex", citation, {"path": path})
            rec_ann = ann.get("record") or {}
            if rec_ann.get("payloadClass"):
                # payload handled with owner context (fact/coverage/import/parameter)
                return
            if rec_ann.get("bundle") == "identity":
                sel = rec_ann["selector"]
                self._admit_canonical(value, self.kit.identity_v3, sel, path)
                return
            if rec_ann.get("document"):
                document = json_doc(self.kit, rec_ann["document"])
                self._admit_canonical(value, document, rec_ann["selector"], path)
                return
            return
        if rep == "h-identity":
            if ann.get("domainSet"):
                hx = value
                if not HEX64.match(hx):
                    self.refuse("L-HSET-SPELLING", "DIGEST_SPELLING", "domainSet h-identity must be bare 64-hex", citation, {"path": path, "value": value})
                self._admit_h_domain_set(hx, ann["domainSet"], field=path)
                return
            domain = ann.get("domain")
            form = ann.get("form")
            if form == "sha256-text" or value.startswith("sha256:"):
                m = SHA256_TEXT.match(value)
                if not m:
                    self.refuse("L-SHA256TEXT", "DIGEST_SPELLING", "expected sha256:<hex>", citation, {"path": path, "value": value})
                hx = m.group(1)
            else:
                if not HEX64.match(value):
                    # maybe prefixed
                    tm = TYPED_ID.match(value)
                    if tm:
                        self._admit_typed_id(value, expected_domain=PREFIX_TO_DOMAIN.get(tm.group(1), domain), field=path)
                        return
                    self.refuse("L-H-SPELLING", "DIGEST_SPELLING", "h-identity spelling invalid", citation, {"path": path, "value": value})
                hx = value
            if domain and "<language>" in str(domain):
                self._admit_h_domain_set(hx, "native-semantic-universe", field=path)
            elif domain in self.kit.identity_v3["$defs"]:
                self._admit_h(hx, domain, path)
            elif domain and domain.startswith("native."):
                # pick domain set
                for ds_name, ds in self.kit.domain_sets.items():
                    if domain in ds:
                        self._admit_h_domain_set(hx, ds_name, field=path)
                        return
                self._admit_h_domain_set(hx, "native-nested", field=path)
            else:
                self._admit_h(hx, domain or "snapshot", path)
            return
        if rep == "capability-manifest-id":
            return
        # relation-payload-schemas.v2.json digest-law representations (not the identity-schemas.v3 four)
        if rep == "snapshot-path":
            # Consumed by relation snapshotJoins / inventoried-path. Not an identity H digest.
            return
        if rep == "framed-body-identity":
            m = SHA256_TEXT.match(value)
            if not m:
                self.refuse("L-BODY-ID-FORM", "BODY_IDENTITY_FORM", "framed-body-identity must be sha256:<hex>", citation, {"path": path, "value": value})
            self._retain_raw(m.group(1), path, citation)
            return
        self.refuse("L-DIGEST-REP", "DIGEST_REPRESENTATION", "unknown x-opensip-digest representation", citation, {"representation": rep, "path": path})

    def _check_registered_schema_document(self, digest: str):
        citation = "identity-and-evidence.md§3 view.schemaDigests registered-schema-document; SCHEMA_DOCUMENT_UNREGISTERED"
        known = set(self.kit.payload_registry_document_sha256().values())
        # also identity-schemas and native schemas used as payload docs
        extra = {
            self.kit.sha256_of("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"),
            self.kit.sha256_of("docs/coop/design-corrections/native/native-evidence.schemas.v2.json"),
            self.kit.sha256_of("docs/coop/design-corrections/foundation/import-source-context.schema.json"),
            self.kit.sha256_of("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"),
            self.kit.sha256_of("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"),
            self.kit.sha256_of("docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"),
            self.kit.sha256_of("docs/coop/design-corrections/foundation/identity-schemas.v3.json"),
            self.kit.sha256_of("docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"),
            self.kit.sha256_of("docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"),
            self.kit.sha256_of("docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"),
            self.kit.sha256_of("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json"),
        }
        known |= extra
        if digest not in known:
            self.refuse("L-SCHEMA-DOC-UNREG", "SCHEMA_DOCUMENT_UNREGISTERED", "schema document digest is not a closed payload-registry document", citation, {"digest": digest})

    # ----- native admission -----

    def _phase_native(self):
        citation = "identity-and-evidence.md§3 (re-run admit_native_context / bind_* over retained bytes); native-evidence.md§1.2/§2.3/§2.4/§11"
        plan_ctx = set(self.plan["nativeContextDigests"])
        retained_ctx = set(self.native_contexts.keys())
        if retained_ctx != plan_ctx:
            self.refuse(
                "L-CTX-SET",
                "NATIVE_CONTEXT_SET",
                "retained context frames must equal plan.nativeContextDigests exactly",
                citation,
                {"plan": sorted(plan_ctx), "retained": sorted(retained_ctx)},
            )
        self.mark_pass("L-CTX-SET", citation, "retained native contexts equal Plan selection", {"n": len(plan_ctx)})
        # Context/universe admission already re-ran at frame retain time.
        self.mark_pass("L-NATIVE-ADMIT", citation, "native context admission and universe binding re-run over retained bytes", {})

    def _admit_native_context(self, domain: str, rec: dict, digest: str, row: dict):
        citation = f"native-evidence.md§{row['admission']['section']} {row['admission']['entryPoint']}"
        lang = row["language"]
        for cj in row.get("closureJoins") or []:
            val = path_get(rec, cj["path"])
            form = cj["form"]
            kind = cj["kind"]
            if form == "closure2-identity":
                if not isinstance(val, str) or not val.startswith("closure2:"):
                    self.refuse("L-CTX-CLOSURE-FORM", "NATIVE_CONTEXT_CLOSURE_UNRETAINED", "closure join missing", citation, {"path": cj["path"]})
                self._admit_typed_id(val, expected_domain="closure", field=".".join(cj["path"]))
                hx = val.split(":", 1)[1]
                cl = self.closures.get(hx)
                if not cl:
                    self.refuse("L-CTX-CLOSURE-UNRETAINED", "native.native-context-closure-unretained", "named closure not retained", citation, {"closureId": val})
                if cl["kind"] != kind:
                    self.refuse("L-CTX-CLOSURE-KIND", "native.native-context-closure-kind-mismatch", "closure kind mismatch", citation, {"expected": kind, "actual": cl["kind"]})
                actual, _ = h_identity("closure", cl)
                if actual != hx:
                    self.refuse("L-CTX-CLOSURE-ID", "native.native-context-closure-identity-mismatch", "closure identity mismatch", citation, {"claimed": hx, "actual": actual})
            elif form == "closure2-suffix":
                if not isinstance(val, str) or not HEX64.match(val):
                    self.refuse("L-CTX-SUFFIX", "NATIVE_CONTEXT_CLOSURE_UNRETAINED", "suffix join missing", citation, {"path": cj["path"]})
                typed = "closure2:" + val
                self._admit_typed_id(typed, expected_domain="closure", field=".".join(cj["path"]))
                cl = self.closures[val]
                if cl["kind"] != kind:
                    self.refuse("L-CTX-SUFFIX-KIND", "native.native-context-closure-kind-mismatch", "suffix closure kind mismatch", citation, {"expected": kind, "actual": cl["kind"]})
        # compiler version from manifest
        if lang == "typescript":
            tool = rec.get("toolClosure") or {}
            cid = tool.get("closureId")
            if cid:
                cl = self.closures[cid.split(":")[1]]
                ver = (rec.get("toolchain") or {}).get("compilerVersion")
                if ver != cl["semanticVersion"]:
                    self.refuse("L-TS-COMPILER-VER", "native.native-context-compiler-version-not-from-manifest", "compilerVersion must equal toolchain closure semanticVersion", citation, {"compilerVersion": ver, "manifest": cl["semanticVersion"]})
            # stdlib inventory complete
            std_root = (rec.get("toolchain") or {}).get("typescriptStdlibMerkleRoot")
            if std_root:
                std = self.closures[std_root]
                dts = [b for b in std["tree"] if str(b["path"]).endswith(".d.ts")]
                comps = (rec.get("toolchain") or {}).get("standardLibraryComponentDigests") or []
                names = [c.get("component") for c in comps]
                if len(names) != len(set(names)):
                    self.refuse("L-STDLIB-AMBIG", "native.native-context-stdlib-tree-ambiguous-basename", "duplicate stdlib basename", citation, {})
                tree_names = [b["path"].rsplit("/", 1)[-1] for b in dts]
                if sorted(names) != sorted(tree_names):
                    missing = set(tree_names) - set(names)
                    if missing:
                        self.refuse("L-STDLIB-INCOMPLETE", "native.native-context-stdlib-inventory-incomplete", "stdlib inventory incomplete", citation, {"missing": sorted(missing)[:8]})
        if lang == "rust":
            tool = rec.get("toolClosure") or {}
            cid = tool.get("closureId")
            if cid:
                cl = self.closures[cid.split(":")[1]]
                # rustc version lives in toolchain
                tv = (rec.get("toolchain") or {}).get("rustcVersion") or (rec.get("toolchain") or {}).get("compilerVersion")
                if tv is not None and tv != cl["semanticVersion"]:
                    self.refuse(
                        "L-RUST-COMPILER-VER",
                        "native.native-context-compiler-version-not-from-manifest",
                        "rustcVersion must equal the admitted tool closure semanticVersion (and therefore the component manifest version); no per-language exception",
                        "native-evidence.md§11 (both languages); native-evidence.md§2.3/§2.4 admit_native_context; identity-and-evidence.md§3 re-run native admission",
                        {
                            "rustcVersion": tv,
                            "closureSemanticVersion": cl["semanticVersion"],
                            "toolClosureId": cid,
                            "field": "NativeContextV2.toolchain.rustcVersion",
                        },
                    )
        if lang == "syntax":
            gb = rec.get("grammarBundle") or {}
            cid = gb.get("closureId")
            if not cid:
                self.refuse("L-SYNTAX-GRAMMAR-CLOSURE", "native.syntax-grammar-version-not-from-manifest", "grammar closure missing", citation, {})
            cl = self.closures[cid.split(":")[1]]
            if cl["kind"] != "grammar":
                self.refuse("L-SYNTAX-KIND", "native.native-context-closure-kind-mismatch", "grammar bundle closure is not kind=grammar", citation, {"kind": cl["kind"]})
            if gb.get("parserVersion") != cl["semanticVersion"]:
                self.refuse("L-SYNTAX-VER", "native.syntax-grammar-version-not-from-manifest", "parserVersion must equal grammar closure semanticVersion", citation, {"parserVersion": gb.get("parserVersion"), "manifest": cl["semanticVersion"]})
            self._admit_grammar_bundle(gb)
        # forbidden compiler on syntax
        if lang == "syntax" and ("toolchain" in rec or "toolClosure" in rec):
            self.refuse("L-SYNTAX-NO-TOOLCHAIN", "SYNTAX_CONTEXT_HAS_COMPILER", "syntax-only context must not name a compiler/toolchain", "native-evidence.md§1.2", {"keys": list(rec.keys())})

    def _admit_grammar_bundle(self, gb: dict):
        citation = "native-evidence.md§1.2 code versus data-document; SyntaxGrammarBundleV1"
        seen_suffix: dict[str, str] = {}
        for g in gb.get("grammars") or []:
            lid = g["languageId"]
            sc = g["syntaxClass"]
            if sc == "code" and lid not in CODE_LANGUAGES:
                self.refuse("L-GRAMMAR-CODE-LANG", "GRAMMAR_CODE_LANGUAGE", "code grammar languageId must be in body-language-version enum", citation, {"languageId": lid})
            if sc == "data-document" and lid in BODY_LANG_ENUM:
                self.refuse("L-GRAMMAR-DATA-LANG", "GRAMMAR_DATA_LANGUAGE", "data-document languageId must not be in body-language-version enum", citation, {"languageId": lid})
            if sc == "code" and lid not in BODY_LANG_ENUM:
                self.refuse("L-GRAMMAR-CODE-ENUM", "GRAMMAR_CODE_NOT_IN_BODY_ENUM", "code languageId must be a body-language-version member", citation, {"languageId": lid})
            for suf in g.get("suffixes") or []:
                if suf in seen_suffix:
                    self.refuse("L-GRAMMAR-SUFFIX-DUP", "native.syntax-grammar-suffix-ambiguous", "suffix claimed twice", citation, {"suffix": suf})
                seen_suffix[suf] = g["grammarId"]
            self._retain_raw(g["grammarDigest"], "grammar.grammarDigest", citation)
        self._retain_raw(gb["bundleDigest"], "grammar.bundleDigest", citation)
        self._retain_raw(gb["normalizer"]["specificationDigest"], "grammar.normalizer.specificationDigest", citation)
        self.mark_pass("L-GRAMMAR-BUNDLE", citation, "grammar rows obey code/data class and unique suffixes", {"n": len(gb.get("grammars") or [])})

    def _bind_universe(self, domain: str, rec: dict, digest: str, row: dict):
        citation = f"native-evidence.md§{row['binding']['section']} {row['binding']['entryPoint']}"
        ctx_field = row.get("contextField") or ["nativeContextId"]
        ctx_val = path_get(rec, ctx_field)
        form = row.get("contextForm", "sha256-text")
        hx = strip_hex(ctx_val, form)
        if hx not in self.plan["nativeContextDigests"]:
            self.refuse(
                "L-UNI-CTX-SELECTED",
                "UNIVERSE_CONTEXT_NOT_SELECTED",
                "universe nativeContextId is not a member of plan.nativeContextDigests",
                "identity-and-evidence.md§3",
                {"nativeContextId": ctx_val, "plan": self.plan["nativeContextDigests"]},
            )
        if hx not in self.native_contexts:
            self.refuse("L-UNI-CTX-RETAINED", "UNIVERSE_CONTEXT_UNRETAINED", "universe context frame not retained", citation, {"hex": hx})
        ctx_domain, ctx_rec = self.native_contexts[hx]
        if ctx_domain != row.get("contextDomain"):
            self.refuse(
                "L-UNI-LANG",
                "UNIVERSE_CONTEXT_LANGUAGE",
                "universe must bind a context of its own language",
                citation,
                {"universeDomain": domain, "contextDomain": ctx_domain, "required": row.get("contextDomain")},
            )
        for f in row.get("contextAgreementFields") or []:
            if rec.get(f) != ctx_rec.get(f):
                self.refuse("L-UNI-AGREE", "UNIVERSE_CONTEXT_FIELD_MISMATCH", "universe/context agreement field differs", citation, {"field": f, "universe": rec.get(f), "context": ctx_rec.get(f)})
        if domain == "native.semantic-universe.syntax.v2":
            if rec.get("resolutionAttempted") is not False:
                self.refuse("L-SYNTAX-RES", "SYNTAX_RESOLUTION_ATTEMPTED", "syntax universe resolutionAttempted must be false", "native-evidence.md§1.2", {"value": rec.get("resolutionAttempted")})
            selected = rec.get("selectedGrammarIds") or []
            bundle_ids = {(g["grammarId"]) for g in (ctx_rec.get("grammarBundle") or {}).get("grammars") or []}
            for gid in selected:
                if gid not in bundle_ids:
                    self.refuse("L-SYNTAX-SEL", "native.syntax-grammar-not-in-bundle", "selected grammar is not in the bundle", citation, {"grammarId": gid})
        if domain == "native.semantic-universe.rust.v2":
            own_id = rec.get("sourceUnitOwnershipId")
            # clones facts need it; checked per clones fact
        self.mark_pass("L-UNI-BIND-" + domain.split(".")[-2], citation, "universe bound to Plan-selected same-language context", {"digest": digest})

    # ----- relations / facts -----

    def _phase_relations(self):
        rel_doc_sha = self.kit.sha256_of("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
        citation = "identity-and-evidence.md§3 fact2 payload encoding; relation-payload-schemas.v2.json#/x-opensip-relation-registry"
        ladders_mirror = self.kit.cap_domains["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
        for rel, row in self.kit.relation_registry["relations"].items():
            if row.get("ladder") != ladders_mirror.get(rel):
                self.refuse(
                    "L-LADDER-DRIFT",
                    "LADDER_MIRROR_DRIFT",
                    "capability-manifest ladder mirror drifts from relation registry",
                    citation + " ladderAuthority",
                    {"relation": rel, "registry": row.get("ladder"), "mirror": ladders_mirror.get(rel)},
                )
        self.mark_pass("L-LADDER-DRIFT", citation, "RELATION-LADDER-DOMAIN-V2 matches relation registry ladders exactly and in order", {})
        for hx, fact in self.facts.items():
            self._admit_fact(hx, fact, rel_doc_sha, citation)

    def _admit_fact(self, hx: str, fact: dict, rel_doc_sha: str, citation: str):
        rel = fact["relation"]
        if rel not in self.kit.relation_registry["relations"]:
            self.refuse("L-FACT-REL", "RELATION_UNREGISTERED", "fact.relation is not registered", citation, {"relation": rel, "fact": hx})
        row = self.kit.relation_registry["relations"][rel]
        if fact["payloadSchemaDigest"] != rel_doc_sha:
            self.refuse(
                "L-FACT-SCHEMA-DIGEST",
                "PAYLOAD_SCHEMA_DIGEST",
                "fact.payloadSchemaDigest must be the relation document file digest",
                citation,
                {"claimed": fact["payloadSchemaDigest"], "expected": rel_doc_sha, "fact": hx},
            )
        ladder = row.get("ladder") or []
        if not ladder:
            self.refuse("L-FACT-EMPTY-LADDER", "EMPTY_LADDER", "relation with no ladder is a registry defect", citation, {"relation": rel})
        if fact["resolution"] not in ladder:
            self.refuse(
                "L-FACT-RUNG",
                "RUNG_NOT_IN_LADDER",
                "fact.resolution is not a rung of this relation's ladder",
                citation,
                {"relation": rel, "resolution": fact["resolution"], "ladder": ladder, "fact": hx},
            )
        if row.get("universeRule") == "same-only" and fact["sourceUniverse"] != fact["targetUniverse"]:
            self.refuse("L-FACT-UNIVERSE-RULE", "UNIVERSE_RULE_SAME_ONLY", "same-only requires sourceUniverse == targetUniverse", citation, {"fact": hx})
        # payload
        payload = self._admit_canonical(
            fact["payloadDigest"],
            self.kit.relation_payloads,
            row["selector"] if "selector" in row else _relation_selector(row, rel),
            f"fact[{hx}].payload",
        )
        # selector from registry
        sel = row.get("selector")
        if not sel:
            # typical: #/$defs/<Name>
            defs = self.kit.relation_payloads.get("$defs", {})
            # already validated via selector if present
        # anchor law
        anchors = fact.get("anchors") or []
        al = row.get("anchorLaw") or {}
        cls = al.get("class")
        if cls == "inventory":
            if len(anchors) != 0:
                self.refuse("L-ANCHOR-CARD", "FACT_ANCHOR_CARDINALITY", "inventory facts carry exactly 0 anchors", citation, {"relation": rel, "n": len(anchors), "fact": hx})
        elif cls == "body-identity":
            if len(anchors) != 1:
                self.refuse("L-ANCHOR-CARD", "FACT_ANCHOR_CARDINALITY", "clones facts carry exactly 1 anchor", citation, {"n": len(anchors), "fact": hx})
        elif cls == "source-text":
            if len(anchors) < 1:
                self.refuse("L-ANCHOR-CARD", "FACT_ANCHOR_CARDINALITY", "source-text facts require >= 1 anchor", citation, {"n": len(anchors), "fact": hx})
        check_order("canonical-set", anchors, f"fact[{hx}].anchors")
        for a in anchors:
            p = a["path"]
            if p not in self.inventory_by_path:
                self.refuse("L-ANCHOR-PATH", "ANCHOR_SOURCE", "anchor path is not an inventoried blob", "identity-and-evidence.md§3 every source anchor must name an inventoried blob", {"path": p, "fact": hx})
            inv = self.inventory_by_path[p]
            if a["blobDigest"] != inv["sha256"]:
                self.refuse("L-ANCHOR-DIGEST", "ANCHOR_DIGEST", "anchor.blobDigest != inventory digest", citation, {"path": p})
            blob = self.store.require_blob(a["blobDigest"], citation, "anchor.blobDigest")
            start, end = a.get("startByte", 0), a.get("endByte", 0)
            if not (0 <= start <= end <= len(blob)):
                self.refuse("L-ANCHOR-RANGE", "ANCHOR_RANGE", "anchor range outside blob", citation, {"path": p, "start": start, "end": end, "len": len(blob)})
            # UTF-8 boundary
            span = blob[start:end]
            try:
                span.decode("utf-8")
                # also prefixes
                blob[:start].decode("utf-8")
            except UnicodeDecodeError:
                if rel not in INVENTORY_RELATIONS:
                    self.refuse("L-ANCHOR-UTF8", "ANCHOR_UTF8", "source-text anchor splits UTF-8 or is not UTF-8", citation, {"path": p, "fact": hx})
        # snapshotJoins
        for sj in row.get("snapshotJoins") or []:
            self._fact_snapshot_join(fact, payload, sj, hx)
        if rel == "clones":
            self._clones_body_join(fact, payload, hx, row)
        # universes retained
        for field in ("sourceUniverse", "targetUniverse"):
            self._admit_h_domain_set(fact[field], "native-semantic-universe", field=f"fact.{field}")
        # syntax capability for facts
        su = fact["sourceUniverse"]
        if su in self.native_universes:
            udomain, urec = self.native_universes[su]
            if udomain == "native.semantic-universe.syntax.v2":
                self._syntax_fact_capability(fact, payload, hx, urec)

    def _fact_snapshot_join(self, fact, payload, sj, hx):
        citation = "identity-and-evidence.md§3 relation snapshotJoins; relation-payload-schemas.v2.json"
        form = sj.get("form")
        if form == "inventoried-file":
            p = payload[sj["pathField"]]
            if p not in self.inventory_by_path:
                self.refuse("L-FILE-PATH", "PATH_NOT_INVENTORIED", "file.path not in snapshot inventory", citation, {"path": p, "fact": hx})
            row = self.inventory_by_path[p]
            if payload[sj["digestField"]] != row["sha256"]:
                self.refuse("L-FILE-DIGEST", "INVENTORY_DIGEST_MISMATCH", "file.contentSha256 != inventory digest", citation, {"path": p, "claimed": payload[sj["digestField"]], "inventory": row["sha256"]})
            if payload[sj["lengthField"]] != row["bytes"]:
                self.refuse("L-FILE-LEN", "INVENTORY_LENGTH_MISMATCH", "file.byteLength != inventory length", citation, {"path": p})
            if sj.get("retainedBlob"):
                raw = self.store.require_blob(row["sha256"], citation, "file.contentSha256")
                if len(raw) != row["bytes"]:
                    self.refuse("L-FILE-BLOB-LEN", "BLOB_LENGTH", "file bytes length mismatch", citation, {"path": p})
        elif form == "inventoried-path":
            unless = sj.get("unless")
            if unless and payload.get(unless["field"]) == unless["equals"]:
                return
            p = payload[sj["pathField"]]
            if p not in self.inventory_by_path:
                self.refuse("L-PKG-PATH", "PATH_NOT_INVENTORIED", "payload path not inventoried", citation, {"path": p, "field": sj["pathField"], "fact": hx})

    def _clones_body_join(self, fact, payload, hx, row):
        citation = "identity-and-evidence.md§3 clones body recipe; fact-identity-policy.v2.json#/canonicalisationSchema/byteGrammar"
        bij = row.get("bodyIdentityJoin") or {}
        if bij.get("anchorCardinality") != 1:
            # mirror of anchorLaw
            pass
        anchors = fact["anchors"]
        if len(anchors) != 1:
            return
        anchor = anchors[0]
        body_id = payload.get("bodyIdentity") or payload.get(bij.get("field", "bodyIdentity"))
        m = SHA256_TEXT.match(body_id or "")
        if not m:
            self.refuse("L-BODY-ID-FORM", "BODY_IDENTITY_FORM", "bodyIdentity must be sha256:<hex>", citation, {"value": body_id, "fact": hx})
        frame_digest = m.group(1)
        frame = self.store.require_blob(frame_digest, citation, "clones.bodyIdentity")
        if sha256_hex(frame) != frame_digest:
            self.refuse("L-BODY-FRAME-HASH", "BODY_FRAME_REHASH", "body identity frame does not rehash", citation, {"digest": frame_digest})
        parsed = parse_body_frame(frame)
        level = payload.get("normalisationLevel") or payload.get("normalisationLevelId") or payload.get(bij.get("levelField", "normalisationLevel"))
        # field names from clones payload schema
        level = payload.get("normalisationLevel", payload.get("levelId", level))
        if parsed["levelId"] != level and parsed["levelId"] != payload.get("normalisationLevel"):
            # try common field
            if parsed["levelId"] not in (payload.get("normalisationLevel"), payload.get("normalisationLevelId"), payload.get("level")):
                self.refuse("L-BODY-LEVEL", "BODY_LEVEL_MISMATCH", "frame levelId != payload normalisation level", citation, {"frame": parsed["levelId"], "payload": payload, "fact": hx})
        nv = payload.get("normalisationVersion")
        if parsed["levelVersionHex"] != nv and parsed["levelVersionHex"] != (nv or ""):
            # normalisationVersion is raw sha256 of level spec
            if nv and parsed["levelVersionHex"] != nv:
                self.refuse("L-BODY-LEVEL-VER", "BODY_LEVEL_VERSION", "frame levelVersion != payload.normalisationVersion", citation, {"frame": parsed["levelVersionHex"], "payload": nv})
        if nv:
            spec = self.store.require_blob(nv, citation, "clones.normalisationVersion")
            if sha256_hex(spec) != nv:
                self.refuse("L-LEVEL-SPEC", "LEVEL_SPEC_REHASH", "level specification bytes do not rehash", citation, {"digest": nv})
        # language from universe binding
        su = fact["sourceUniverse"]
        udomain, urec = self.native_universes[su]
        urow = self.kit.domain_sets["native-semantic-universe"][udomain]
        bind = urow.get("languageVersionBinding") or {}
        dialect = bind.get("dialect") or {}
        path = anchor["path"]
        lang_id, dialect_token = select_body_language(bind, path, urec, fact, self)
        if parsed["languageId"] != lang_id:
            self.refuse("L-BODY-LANG", "BODY_LANGUAGE_MISMATCH", "frame languageId is not derived from the body (suffix/ownership), not the engine language", citation, {"frame": parsed["languageId"], "derived": lang_id, "path": path, "fact": hx})
        if lang_id not in (bind.get("bodyLanguages") or [bind.get("bodyLanguage")]):
            self.refuse("L-BODY-LANG-ENGINE", "BODY_LANGUAGE_NOT_PRODUCED", "body language is not one this universe produces", citation, {"languageId": lang_id})
        # languageVersion derived record
        blv = derive_body_language_version(bind, urec, self.native_contexts, dialect_token, lang_id)
        blv_c = encode_c(blv, profile="product")
        lv_raw = hashlib.sha256(blv_c).digest()
        if parsed["languageVersion"] != lv_raw:
            self.refuse(
                "L-BODY-LANGVER",
                "BODY_LANGUAGE_VERSION_MISMATCH",
                "frame languageVersion is not SHA-256(C(body-language-version)) of the derived record",
                citation,
                {"fact": hx, "derivedHex": lv_raw.hex(), "frameHex": parsed["languageVersion"].hex()},
            )
        # L0 recompute
        if parsed["levelId"] == "L0-verbatim":
            blob = self.store.require_blob(anchor["blobDigest"], citation, "anchor")
            span = blob[anchor["startByte"] : anchor["endByte"]]
            inner = struct.pack(">I", len(span)) + span
            if parsed["payload"] != inner:
                self.refuse(
                    "L-L0-PAYLOAD",
                    "L0_PAYLOAD_MISMATCH",
                    "L0 payload is not u32be raw_byte_len || exact body-span bytes (double length prefix)",
                    citation,
                    {"fact": hx, "spanLen": len(span), "payloadLen": len(parsed["payload"])},
                )
            # outer payload_len == raw_byte_len + 4
            if parsed["payloadLen"] != len(span) + 4:
                self.refuse("L-L0-OUTER-LEN", "L0_OUTER_LEN", "at L0 payload_len == raw_byte_len + 4", citation, {"payloadLen": parsed["payloadLen"], "raw": len(span)})
        else:
            # L1-L3: well-formed stream framing
            parse_token_stream(parsed["payload"], citation)
        self.mark_pass("L-CLONES-BODY", citation, "clones body frame retained, rehashed, components joined", {"fact": hx, "level": parsed["levelId"]})

    def _syntax_fact_capability(self, fact, payload, hx, urec):
        citation = "native-evidence.md§1.2 (capability law binds facts and Coverage)"
        rel = fact["relation"]
        rung = fact["resolution"]
        cap = f"{rel}@{rung}"
        if rel in INVENTORY_RELATIONS:
            return
        ctx_hex = strip_hex(urec["nativeContextId"], "sha256-text")
        ctx = self.native_contexts[ctx_hex][1]
        selected = set(urec.get("selectedGrammarIds") or [])
        grammars = [g for g in ctx["grammarBundle"]["grammars"] if g["grammarId"] in selected]
        for a in fact.get("anchors") or []:
            g = grammar_for_path(grammars, a["path"])
            if g is None:
                self.refuse("L-SYNTAX-FACT-CAP", "SYNTAX_CAPABILITY_UNSUPPORTED_FACT", "anchor path has no selected grammar for this relation", citation, {"path": a["path"], "capability": cap, "fact": hx})
            if g["syntaxClass"] != "code" and rel in (CODE_SYNTAX_RELATIONS | {"clones"} | SEMANTIC_RELATIONS):
                self.refuse("L-SYNTAX-FACT-DATA", "SYNTAX_CAPABILITY_UNSUPPORTED_FACT", "data-document grammar cannot bear code/clone facts", citation, {"path": a["path"], "syntaxClass": g["syntaxClass"], "capability": cap})
            if rel in SEMANTIC_RELATIONS:
                self.refuse("L-SYNTAX-SEMANTIC-FACT", "SYNTAX_CAPABILITY_UNSUPPORTED_FACT", "syntax-only universe cannot carry semantic rungs", citation, {"capability": cap, "fact": hx})

    # ----- coverage -----

    def _phase_coverage(self):
        citation = "identity-and-evidence.md§3 Coverage scopes partition; relation coverageTotality; native-evidence.md§1.2/§4.3"
        cov_doc_sha = self.kit.sha256_of("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
        partition_key = self.kit.relation_registry["coveragePartitionLaw"]["partitionKey"]
        for view_hex, view in self.views.items():
            # partition over every referenced scope including those with no coverage entry
            scopes = [self.scopes[sid.split(":")[1]] for sid in view["scopeIds"]]
            groups: dict[tuple, list] = {}
            for sc in scopes:
                key = tuple(sc[k] if k != "resolution" else sc["resolution"] for k in partition_key)
                # partitionKey uses resolution as rung
                key = (sc["snapshotId"], sc["relation"], sc["resolution"], sc["sourceUniverse"], sc["targetUniverse"])
                groups.setdefault(key, []).append(sc)
            for key, scs in groups.items():
                seen = set()
                for sc in scs:
                    for sub in sc["subjects"]:
                        if sub in seen:
                            self.refuse(
                                "L-PARTITION",
                                "SUBJECT_SCOPE_PARTITION_OVERLAP",
                                "two Coverage scopes of one view share a subject under the same owning tuple",
                                citation,
                                {"relation": key[1], "resolution": key[2], "subject": sub, "view": view_hex},
                            )
                        seen.add(sub)
            self.mark_pass("L-PARTITION", citation, "view scopes disjoint on partitionKey", {"view": view_hex})
            # coverage records
            for cid in view["coverageIds"]:
                hx = cid.split(":")[1]
                cov = self.coverages[hx]
                if cov["payloadSchemaDigest"] != cov_doc_sha:
                    self.refuse("L-COV-SCHEMA", "PAYLOAD_SCHEMA_DIGEST", "coverage.payloadSchemaDigest must be native-evidence.schemas.v2.json file digest", citation, {"claimed": cov["payloadSchemaDigest"], "expected": cov_doc_sha})
                payload = self._admit_canonical(cov["payloadDigest"], self.kit.native_schemas, "#/$defs/CoverageResultV3", f"coverage[{hx}].payload")
                if payload.get("schemaVersion") != 3:
                    self.refuse("L-COV-MAJOR", "COVERAGE_MAJOR", "CoverageResultV3 schemaVersion must be 3", citation, {})
                scope_id = cov["scopeId"]
                shx = scope_id.split(":")[1] if ":" in scope_id else scope_id
                scope = self.scopes.get(shx)
                if not scope:
                    self.refuse("L-COV-SCOPE", "COVERAGE_SCOPE_MISSING", "coverage.scopeId not retained", citation, {"scopeId": scope_id})
                # subjectScopeCommitment is sha256: + H suffix of scope2
                key = payload["key"]
                expected_ssc = "sha256:" + shx
                if key.get("subjectScopeCommitment") != expected_ssc:
                    self.refuse(
                        "L-SSC",
                        "SUBJECT_SCOPE_COMMITMENT",
                        "subjectScopeCommitment must be sha256: plus the 64-hex suffix of the admitted scope2 identity",
                        "identity-and-evidence.md§3 native subjectScopeCommitment; native-evidence.md§4.1a",
                        {"claimed": key.get("subjectScopeCommitment"), "expected": expected_ssc},
                    )
                if key["relation"] != scope["relation"] or key["resolution"] != scope["resolution"]:
                    self.refuse("L-COV-KEY-REL", "COVERAGE_KEY_MISMATCH", "Coverage key relation/rung != scope", citation, {})
                if key["sourceUniverse"] != scope["sourceUniverse"] or key["targetUniverse"] != scope["targetUniverse"]:
                    self.refuse("L-COV-KEY-UNI", "COVERAGE_KEY_UNIVERSE", "Coverage key universes != scope", citation, {})
                entry = payload["entry"]
                if entry["relation"] != key["relation"] or entry["resolution"] != key["resolution"]:
                    self.refuse("L-COV-ENTRY", "COVERAGE_ENTRY_KEY", "ViewEntryV3 relation/rung != key", citation, {})
                # RC-6
                rc = entry.get("resolutionCompleteness") or {}
                if entry.get("coverage") == "complete" and rc.get("examinedExhaustive") is not True:
                    self.refuse(
                        "L-RC6",
                        "native.coverage-bijection-mismatch",
                        "coverage=complete requires resolutionCompleteness.examinedExhaustive=true",
                        "native-evidence.md§4.3 RC-6; native-evidence.schemas.v2.json#/$defs/ViewEntryV3",
                        {"coverage": hx},
                    )
                self._coverage_capability_and_totality(view, view_hex, scope, shx, entry, hx)

    def _coverage_capability_and_totality(self, view, view_hex, scope, shx, entry, cov_hx):
        citation = "native-evidence.md§1.2; identity-schemas.v3.json scopeCapabilityLaw; relation coverageTotality"
        rel, rung = scope["relation"], scope["resolution"]
        su = scope["sourceUniverse"]
        udomain, urec = self.native_universes[su]
        row = self.kit.relation_registry["relations"][rel]
        # syntax grammar capability
        if udomain == "native.semantic-universe.syntax.v2":
            if rel in INVENTORY_RELATIONS:
                pass
            else:
                ctx = self.native_contexts[strip_hex(urec["nativeContextId"], "sha256-text")][1]
                selected = [g for g in ctx["grammarBundle"]["grammars"] if g["grammarId"] in set(urec.get("selectedGrammarIds") or [])]
                supported = False
                sk = row.get("subjectKind")
                if sk == "source-path":
                    if not scope["subjects"]:
                        supported = False
                    else:
                        supported = all(grammar_for_path(selected, p) and grammar_for_path(selected, p)["syntaxClass"] == "code" for p in scope["subjects"]) if rel in (CODE_SYNTAX_RELATIONS | {"clones"} | SEMANTIC_RELATIONS) else True
                        if rel in SEMANTIC_RELATIONS:
                            supported = False
                else:
                    # symbol: at least one path in snapshot readable by selected code grammar
                    supported = any(g["syntaxClass"] == "code" for g in selected)
                    if rel in SEMANTIC_RELATIONS:
                        supported = False
                if not supported:
                    if entry.get("coverage") == "complete":
                        self.refuse("L-SYNTAX-SCOPE-COMPLETE", "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE", "unsupported syntax capability must not be complete", citation, {"relation": rel, "rung": rung})
                    if entry.get("deficiency") != "language-tier-unsupported":
                        self.refuse("L-SYNTAX-SCOPE-DEF", "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE_DEFICIENCY_MISMATCH", "unsupported scope deficiency", citation, {"deficiency": entry.get("deficiency")})
                    if entry.get("nativeCause") != "capability-missing":
                        self.refuse("L-SYNTAX-SCOPE-CAUSE", "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE_CAUSE_MISMATCH", "unsupported scope nativeCause", citation, {"nativeCause": entry.get("nativeCause")})
        # closed-suffix-table clones gate (TS and syntax)
        urow = self.kit.domain_sets["native-semantic-universe"][udomain]
        dialect = (urow.get("languageVersionBinding") or {}).get("dialect") or {}
        if dialect.get("form") == "closed-suffix-table" and (row.get("bodyIdentityJoin") or rel == "clones"):
            table = dialect.get("table") or {}
            sk = row.get("subjectKind")
            if sk == "source-path":
                if not scope["subjects"]:
                    ok = False
                else:
                    ok = all(longest_suffix(p, table) is not None for p in scope["subjects"])
            else:
                ok = any(longest_suffix(p, table) is not None for p in self.inventory_by_path)
            law = self.kit.digest_domains["scopeCapabilityLaw"]
            if not ok:
                if entry.get("coverage") != "unknown":
                    self.refuse("L-SCOPE-CAP-COV", "SCOPE_CAPABILITY_UNSUPPORTED", "suffix-table unsupported scope coverage must be unknown", citation, {"relation": rel})
                if entry.get("deficiency") != law["onUnsupportedScope"]["deficiency"]:
                    self.refuse("L-SCOPE-CAP-DEF", "SCOPE_CAPABILITY_DEFICIENCY", "wrong deficiency for unsupported scope", citation, {})
                if entry.get("nativeCause") != law["onUnsupportedScope"]["nativeCause"]:
                    self.refuse("L-SCOPE-CAP-CAUSE", "SCOPE_CAPABILITY_CAUSE", "wrong nativeCause for unsupported scope", citation, {})
        # totality file@enumerated
        tot = row.get("coverageTotality")
        if tot and entry.get("coverage") == "complete":
            match_on = tot["matchOn"]
            facts = []
            for fid in view["facts"]:
                fhex = fid.split(":")[1]
                f = self.facts[fhex]
                ok = True
                for coord in match_on:
                    if coord == "resolution":
                        if f["resolution"] != scope["resolution"]:
                            ok = False
                    elif f.get(coord) != scope.get(coord):
                        ok = False
                if ok:
                    facts.append(f)
            inv_subjects = [s for s in scope["subjects"] if s in self.inventory_by_path]
            fact_paths = set()
            for f in facts:
                pl = self.canonical_records.get(f["payloadDigest"])
                if pl and "path" in pl:
                    fact_paths.add(pl["path"])
            missing = [s for s in inv_subjects if s not in fact_paths]
            if missing:
                self.refuse(
                    "L-TOTALITY",
                    "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH",
                    "complete file@enumerated Coverage omits an inventoried subject",
                    citation,
                    {"missing": missing, "scope": shx, "view": view_hex},
                )
        # rust partial clones: no complete from partial ownership
        if rel == "clones" and su in self.native_universes:
            udomain, urec = self.native_universes[su]
            if udomain.endswith("rust.v2"):
                own_id = urec.get("sourceUnitOwnershipId")
                if own_id:
                    ohx = strip_hex(own_id, "sha256-text") or strip_hex(own_id, "bare-hex")
                    own = self.admitted.get(("h-identity", ohx), None)
                    if own and own.get("enumeration") == "partial":
                        if entry.get("coverage") == "complete":
                            self.refuse(
                                "L-PARTIAL-CLONES",
                                "PARTIAL_OWNERSHIP_COMPLETE_CLONES",
                                "empty/partial clone view must not claim complete Coverage from partial ownership",
                                "identity-and-evidence.md§3 selected scope vs incomplete enumeration; native-evidence.md§11",
                                {"coverage": cov_hx},
                            )

    # ----- citations / proof -----

    def _phase_citations(self):
        citation = "identity-and-evidence.md§3 finding citations; proof evaluationInputRefs"
        proof = self.proof
        plan = self.plan
        ev = self.evidence
        view_ids = set(ev["viewIds"])
        view_facts = set()
        view_cov = set()
        for v in self.views.values():
            view_facts.update(v["facts"])
            view_cov.update(v["coverageIds"])
        plan_imports = set(plan["importIds"])
        # evaluationInputRefs
        for ref in proof["evaluationInputRefs"]:
            if not isinstance(ref, dict):
                continue
            dom = ref.get("domain")
            if dom in PROOF_INPUT_FORBIDDEN:
                self.refuse("L-PROOF-REF-DOMAIN", "PROOF_INPUT_FORBIDDEN_DOMAIN", "proof input domain excludes run/evidence/seal/proof", citation, {"domain": dom})
            if dom not in self.kit.by_domain:
                self.refuse("L-PROOF-REF-UNREG", "UNREGISTERED_DOMAIN", "proof input domain not in byDomain", citation, {"domain": dom})
            if dom == "import":
                typed = "import2:" + ref["digest"]
                if typed not in plan_imports and ref["digest"] not in {i.split(":")[1] for i in plan_imports}:
                    self.refuse("L-UNSELECTED-IMPORT", "UNSELECTED_EVALUATION_IMPORT", "evaluated import must be Plan-selected", citation, {"digest": ref["digest"]})
        # every plan import in evaluationInputRefs
        ei_imports = {r["digest"] for r in proof["evaluationInputRefs"] if r.get("domain") == "import"}
        for iid in plan_imports:
            hx = iid.split(":")[1]
            if hx not in ei_imports:
                self.refuse("L-IMPORT-IN-EVAL", "PLAN_IMPORT_NOT_IN_EVALUATION_INPUTS", "every Plan-selected import must be in evaluationInputRefs", citation, {"importId": iid})
        self.mark_pass("L-PROOF-INPUTS", citation, "evaluationInputRefs domains registered; imports Plan-selected and complete", {})
        # findings
        for fid in proof.get("findingIds") or []:
            self._admit_typed_id(fid, expected_domain="finding", field="proof.findingIds[]")
            fhex = fid.split(":")[1]
            finding = self.frames[fhex][1]
            self._walk_identity_record("finding", finding, self.kit.identity_v3, "#/$defs/finding")
            if finding.get("ruleClosure") not in plan["semanticClosures"]:
                self.refuse("L-FINDING-RULE-CLOSURE", "CLOSURE_NOT_SELECTED", "finding.ruleClosure not selected", "identity-schemas.v3.json closureMembership", {"finding": fid})
            for eref in finding.get("evidenceRefs") or []:
                dom = eref["domain"]
                if dom not in FINDING_EVIDENCE_DOMAINS:
                    self.refuse("L-FINDING-EV-DOM", "FINDING_EVIDENCE_DOMAIN", "finding evidence domain not in closed set", citation, {"domain": dom})
                d = eref["digest"]
                if dom == "fact":
                    typed = "fact2:" + d
                    if typed not in view_facts:
                        self.refuse("L-CITE-FACT", "CITATION_FACT_NOT_IN_VIEW", "fact citation must belong to an evaluated view", citation, {"digest": d})
                elif dom == "coverage":
                    typed = "coverage2:" + d
                    if typed not in view_cov:
                        self.refuse("L-CITE-COV", "CITATION_COVERAGE_NOT_IN_VIEW", "coverage citation must belong to an evaluated view", citation, {"digest": d})
                elif dom == "import":
                    typed = "import2:" + d
                    if typed not in plan_imports:
                        self.refuse("L-CITE-IMPORT", "CITATION_IMPORT_NOT_SELECTED", "import citation must be Plan-selected and in evaluationInputRefs", citation, {"digest": d})
                elif dom == "blob":
                    self.store.require_blob(d, citation, "finding.evidenceRefs blob")
                elif dom == "predicate-witness":
                    # must name a witness of this proof
                    wdigests = {pp.get("witnessDigest") for pp in proof.get("predicateProofs") or []}
                    if d not in wdigests:
                        self.refuse("L-CITE-WITNESS", "CITATION_WITNESS_NOT_IN_PROOF", "predicate-witness citation must name a witness of this proof", citation, {"digest": d})
        # predicate proofs subset
        ei_set = {(r.get("domain"), r.get("digest")) for r in proof["evaluationInputRefs"]}
        for pp in proof.get("predicateProofs") or []:
            for iref in pp.get("inputRefs") or []:
                if (iref.get("domain"), iref.get("digest")) not in ei_set:
                    self.refuse("L-PRED-INPUT-SUBSET", "PREDICATE_INPUT_NOT_IN_EVALUATION", "predicate input refs are a subset of evaluationInputRefs", citation, {"ref": iref})
            wd = pp.get("witnessDigest")
            if wd:
                self._admit_canonical(wd, self.kit.identity_v3, "#/$defs/predicate-witness", "predicateProofs.witnessDigest")
        self.mark_pass("L-CITATIONS", citation, "finding/proof citations are members of the evaluated closure", {})
        # program-predicate addressing
        self._check_program_predicates()

    def _check_program_predicates(self):
        citation = "identity-and-evidence.md§3 program-predicate node addressing"
        rp = self.rule_program
        if not rp:
            return
        if rp.get("policyDigest") != self.plan["policyDigest"]:
            self.refuse("L-RP-POLICY", "RULE_PROGRAM_POLICY", "compiled program policyDigest must equal Plan policyDigest", citation, {})
        # projection of policy rules in ruleId order
        if self.policy:
            check_order("ruleId", self.policy.get("rules") or [], "PolicyDocumentV2.rules")
        for pp in self.proof.get("predicateProofs") or []:
            wd = pp.get("witnessDigest")
            if not wd or wd not in self.canonical_records:
                continue
            w = self.canonical_records[wd]
            ppd = w.get("programPredicateDigest")
            if not ppd:
                continue
            pred = self._admit_canonical(ppd, self.kit.identity_v3, "#/$defs/program-predicate", "programPredicateDigest")
            if pred["ruleProgramDigest"] != self.proof["ruleProgramDigest"]:
                self.refuse("L-PP-RP", "PROGRAM_PREDICATE_RULE_PROGRAM", "program-predicate.ruleProgramDigest != proof", citation, {})
            if pred["operation"] != pp.get("operation"):
                self.refuse("L-PP-OP", "PROGRAM_PREDICATE_OPERATION", "program-predicate.operation != predicate proof operation", citation, {})
            # locate node
            node = locate_predicate(rp, pred["ruleId"], pred["predicateId"])
            if node is None:
                self.refuse("L-PP-ADDR", "PREDICATE_ADDRESS", "predicateId does not address a node of the admitted program", citation, {"predicateId": pred["predicateId"], "ruleId": pred["ruleId"]})
            if node.get("op") != pred["operation"]:
                self.refuse("L-PP-NODE-OP", "PREDICATE_NODE_OP", "addressed node op != program-predicate.operation", citation, {})
            node_c = encode_c(node, profile="product")
            if sha256_hex(node_c) != pred["nodeDigest"]:
                self.refuse("L-PP-NODE-DIGEST", "PREDICATE_NODE_DIGEST", "nodeDigest is not SHA256(C(addressed node))", citation, {"claimed": pred["nodeDigest"], "actual": sha256_hex(node_c)})
            child_ids = child_addresses(pred["predicateId"], node)
            if set(w.get("childPredicateIds") or []) != set(child_ids):
                self.refuse("L-PP-CHILDREN", "PREDICATE_CHILD_IDS", "witness childPredicateIds must be the addressed node's operand addresses", citation, {"expected": child_ids, "actual": w.get("childPredicateIds")})
        self.mark_pass("L-PROGRAM-PREDICATE", citation, "program-predicate addresses admitted program nodes; nodeDigest fragment", {})

    # ----- closure membership / kinds -----

    def _phase_closures(self):
        citation = "identity-schemas.v3.json#/x-opensip-digest-domains/closureKinds and closureMembership"
        kinds = self.kit.digest_domains["closureKinds"]["byField"]
        if self.seal:
            hx = self.seal["evaluatorClosure"].split(":")[1]
            if self.closures[hx]["kind"] != "evaluator":
                self.refuse("L-SEAL-EVAL-KIND", "CLOSURE_KIND", "evaluation-seal.evaluatorClosure must be kind=evaluator", citation, {"kind": self.closures[hx]["kind"]})
        if self.proof:
            hx = self.proof["evaluatorClosure"].split(":")[1]
            if self.proof["evaluatorClosure"] != self.seal["evaluatorClosure"]:
                self.refuse("L-PROOF-EVAL-EQ", "EVALUATOR_CLOSURE_EQUAL", "proof.evaluatorClosure must equal seal.evaluatorClosure", citation, {})
            if self.proof["evaluatorClosure"] not in self.plan["semanticClosures"]:
                self.refuse("L-PROOF-EVAL-SEL", "CLOSURE_NOT_SELECTED", "evaluator not in plan.semanticClosures", citation, {})
        self.mark_pass("L-CLOSURE-MEMBERSHIP", citation, "direct closures selected; kinds match byField", {})
        # acyclic
        if "evidenceId" in (self.proof or {}) or "runId" in (self.proof or {}):
            self.refuse("L-ACYCLIC", "GRAPH_CYCLE", "proof must not include EvidenceId or RunId", "identity-and-evidence.md§3 acyclic graph", {})
        self.mark_pass("L-ACYCLIC", "identity-and-evidence.md§3", "proof excludes evidence/run; seal includes both; run includes seal", {})

    # ----- capability manifest -----

    def _phase_capability(self):
        citation = "identity-and-evidence.md§3 CAP-MANIFEST-ID-V1; capability-manifest-domains.v2.json gates ADM-TYPE/CLOSED/DOMAIN/ORDER"
        raw = self.cap_bytes
        if raw is None:
            self.refuse("L-CAP-BYTES", "CAP_BYTES_MISSING", "capabilityManifestBytesDigest not retained", citation, {})
        # The committed bytes ARE CVE1, not JSON. Try CVE1 decode first? We don't have a decoder
        # required for identity: SHA256(UTF8("opensip.capability-manifest.v1")||00||committedBytes)
        derived = capability_manifest_id(raw)
        if derived != self.plan["capabilityManifestId"] or derived != self.run["capabilityManifestId"]:
            self.refuse(
                "L-CAP-ID",
                "CAPABILITY_MANIFEST_ID",
                "capabilityManifestId must be SHA256(UTF8(opensip.capability-manifest.v1)||00||committedBytes)",
                citation,
                {"derived": derived, "plan": self.plan["capabilityManifestId"], "run": self.run["capabilityManifestId"]},
            )
        self.mark_pass("L-CAP-ID", citation, "capabilityManifestId derived from retained committed bytes", {"id": derived})
        # If committed bytes happen to also be JSON (some producers store JSON then CVE1 separately)
        # The recipe says committedBytes are CVE1 encoding of CapabilityManifestV1.
        man = decode_cve1_or_refuse(raw, self)
        self._adm_capability(man)

    def _adm_capability(self, man: dict):
        citation = "capability-manifest-domains.v2.json admission.ADM-TYPE/CLOSED/DOMAIN/ORDER"
        shape = self.kit.cap_domains["recordShape"]["CapabilityManifestV1"]
        if set(man.keys()) != set(shape["requiredKeys"]):
            self.refuse("L-CAP-CLOSED", "ADM-CLOSED", "CapabilityManifestV1 must carry exactly its key set", citation, {"keys": sorted(man.keys()), "required": shape["requiredKeys"]})
        if not isinstance(man.get("schemaVersion"), int) or isinstance(man.get("schemaVersion"), bool):
            self.refuse("L-CAP-TYPE", "ADM-TYPE", "schemaVersion must be a JSON integer", citation, {"type": type(man.get("schemaVersion")).__name__})
        if not isinstance(man.get("profile"), str):
            self.refuse("L-CAP-TYPE-PROFILE", "ADM-TYPE", "profile must be a JSON string", citation, {})
        rel_members = set(self.kit.cap_domains["registries"]["RELATION-DOMAIN-V2"]["members"])
        ladders = self.kit.cap_domains["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
        plat = set(self.kit.cap_domains["registries"]["PLATFORM-ID-DOMAIN-V1"]["members"])
        defs = set(self.kit.cap_domains["registries"]["DEFICIENCY-DOMAIN-V1"]["members"])
        covs = set(self.kit.cap_domains["registries"]["COVERAGE-STATE-DOMAIN-V1"]["members"])
        pc_shape = self.kit.cap_domains["recordShape"]["ProviderCapability"]
        ac_shape = self.kit.cap_domains["recordShape"]["AbsentCapability"]
        for i, p in enumerate(man.get("providers") or []):
            if not isinstance(p, dict):
                self.refuse("L-CAP-PROV-TYPE", "ADM-TYPE", "provider is not a record", citation, {"index": i})
            if set(p.keys()) != set(pc_shape["requiredKeys"]):
                self.refuse("L-CAP-PROV-CLOSED", "ADM-CLOSED", "ProviderCapability key set", citation, {"keys": sorted(p.keys())})
            rels = p.get("relations")
            if not isinstance(rels, dict):
                self.refuse("L-CAP-REL-MAP", "ADM-CLOSED", "relations is a MAP not a RECORD", citation, {})
            for k, v in rels.items():
                if k not in rel_members:
                    self.refuse("L-CAP-REL-DOM", "ADM-DOMAIN", "relations key not in RELATION-DOMAIN-V2", citation, {"key": k})
                if v not in ladders.get(k, []):
                    self.refuse("L-CAP-RUNG-DOM", "ADM-DOMAIN", "relations value is not a rung of THAT relation ladder", citation, {"relation": k, "rung": v, "ladder": ladders.get(k)})
            ids = p.get("platformIds") or []
            prev = b""
            for pid in ids:
                if pid not in plat:
                    self.refuse("L-CAP-PLAT", "ADM-DOMAIN", "platformId not in PLATFORM-ID-DOMAIN-V1", citation, {"platformId": pid})
                b = pid.encode("utf-8")
                if b <= prev:
                    self.refuse("L-CAP-ORDER-PLAT", "ADM-ORDER", "platformIds not strict ascending unique NFC UTF-8", citation, {"platformIds": ids})
                prev = b
        for i, a in enumerate(man.get("coverageForAbsent") or []):
            if set(a.keys()) != set(ac_shape["requiredKeys"]):
                self.refuse("L-CAP-ABS-CLOSED", "ADM-CLOSED", "AbsentCapability key set", citation, {"keys": sorted(a.keys())})
            prev = b""
            for rid in a.get("relationIds") or []:
                if rid not in rel_members:
                    self.refuse("L-CAP-ABS-REL", "ADM-DOMAIN", "AbsentCapability.relationIds member not in RELATION-DOMAIN-V2", citation, {"relationId": rid})
                b = rid.encode("utf-8")
                if b <= prev:
                    self.refuse("L-CAP-ORDER-ABS", "ADM-ORDER", "relationIds not strict ascending unique", citation, {})
                prev = b
            if a.get("deficiency") not in defs:
                self.refuse("L-CAP-DEF", "ADM-DOMAIN", "deficiency not in DEFICIENCY-DOMAIN-V1", citation, {"deficiency": a.get("deficiency")})
            if a.get("coverageState") not in covs:
                self.refuse("L-CAP-COVSTATE", "ADM-DOMAIN", "coverageState not in COVERAGE-STATE-DOMAIN-V1", citation, {"coverageState": a.get("coverageState")})
        self.mark_pass("L-CAP-GATES", citation, "ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER executed on committed CapabilityManifestV1", {})

    # ----- component profiles -----

    def _phase_component(self):
        citation = "security-and-lifecycle.md#S1/#S2; component-manifest-schemas.v11.json manifestSchema (prose field table, not a stock Draft-2020-12 root); security-completion.v1.md§2.1"
        fields = {f["name"]: f for f in self.kit.component_manifest["manifestSchema"]["fields"]}
        required = [n for n, f in fields.items() if f.get("required")]
        # Do not invent a stock JSON Schema validator for this prose table.
        for digest, rec in self.closures.items():
            raw = self.raw_artifacts.get(rec["manifestDigest"])
            if raw is None:
                continue
            # metadata profile admission of stored bytes (exact stored bytes = admission digest)
            if sha256_hex(raw) != rec["manifestDigest"]:
                self.refuse("L-MANIFEST-STORED", "MANIFEST_STORED_SHA", "closure.manifestDigest is sha256 of exact stored bytes", citation, {})
            try:
                man = admit_json_bytes(raw, profile="metadata", citation=citation)
            except AdmissionError as e:
                self.refuse("L-MANIFEST-METADATA-PROFILE", e.code, "component manifest refused under opensip-metadata-canonical.1 / metadata profile (must not use product C decoder)", citation, e.operands)
            # Run-closure consumes S1's delivery selector, not the install-registry
            # uniqueness fields (stableId vs live index). Predecessor helper treated
            # every prose `required` flag as a Run-closure refusal; S1 names
            # platforms[] {os, arch, tree TreeCommitment, entrypoint} plus RJ-3.
            if man.get("kind") != "component":
                self.refuse("L-MANIFEST-KIND", "COMPONENT_KIND", "manifest.kind initial vocabulary is 'component'", citation, {"kind": man.get("kind")})
            if "signature" in man or "signatures" in man:
                self.refuse("L-MANIFEST-SIG-EMBEDDED", "MANIFEST_EMBEDDED_SIGNATURE", "manifest carries no signature field; envelope is detached", citation, {})
            platforms = man.get("platforms") or man.get("platform") or []
            if isinstance(platforms, dict):
                platforms = [platforms]
            if not platforms:
                self.refuse("L-MANIFEST-PLATFORMS", "COMPONENT_PLATFORMS", "S1 requires manifestSchema.platforms[]", citation, {"closure": digest})
            for plat in platforms if isinstance(platforms, list) else []:
                if not isinstance(plat, dict):
                    continue
                for k in ("os", "arch", "entrypoint"):
                    if k not in plat or plat[k] in (None, ""):
                        self.refuse("L-MANIFEST-PLATFORM-FIELD", "COMPONENT_PLATFORM_FIELD", "S1 platforms[] requires os, arch, entrypoint", citation, {"missing": k, "closure": digest})
                if "tree" not in plat:
                    self.refuse("L-MANIFEST-TREE", "COMPONENT_TREECOMMITMENT", "S1 platforms[] requires tree TreeCommitment", citation, {"closure": digest})
            # S1: type=file entries map to Blob; dir/symlink stay delivery rows
            file_rows = []
            for plat in platforms if isinstance(platforms, list) else []:
                tree = plat.get("tree") if isinstance(plat, dict) else None
                if isinstance(tree, dict) and isinstance(tree.get("entries"), list):
                    tree = tree["entries"]
                if isinstance(tree, list):
                    for ent in tree:
                        if not isinstance(ent, dict):
                            continue
                        if ent.get("type") == "file":
                            file_rows.append(ent)
                        if ent.get("type") == "symlink":
                            tgt = ent.get("target") or ""
                            # RJ-3: symlink targets inside the tree — structural: target must not be absolute escape
                            if tgt.startswith("/") or ".." in tgt.split("/"):
                                self.refuse("L-RJ3", "RJ-3", "symlink target escapes the tree", citation, {"target": tgt})
            # closure.tree should equal file projection of selected platform
            tree_paths = {b["path"] for b in rec["tree"]}
            for ent in file_rows:
                p = ent.get("path")
                if p and p in tree_paths:
                    blob = next(b for b in rec["tree"] if b["path"] == p)
                    if blob["sha256"] != ent.get("sha256"):
                        self.refuse("L-TREE-PROJ-DIGEST", "TREE_COMMITMENT_DIGEST", "closure.tree sha256 != TreeCommitment file sha256", citation, {"path": p})
                    if blob["bytes"] != ent.get("length") and blob["bytes"] != ent.get("bytes"):
                        # length field name may be length
                        ln = ent.get("length", ent.get("bytes"))
                        if ln is not None and blob["bytes"] != ln:
                            self.refuse("L-TREE-PROJ-LEN", "TREE_COMMITMENT_LENGTH", "closure.tree bytes != TreeCommitment length", citation, {"path": p})
            # detector compatibility reserved file
            for b in rec["tree"]:
                if b["path"] == ".opensip/detector-compatibility.json":
                    rawb = self.store.require_blob(b["sha256"], citation, "detector-compatibility")
                    if len(rawb) != b["bytes"]:
                        self.refuse("L-DET-COMPAT-LEN", "BLOB_LENGTH", "detector-compatibility length", citation, {})
                    # listing schema is workflow detector-manifest
                    try:
                        listing = admit_json_bytes(rawb, profile="product", citation=citation)
                    except AdmissionError as e:
                        self.refuse("L-DET-COMPAT-PARSE", e.code, "detector-compatibility.json failed product C admission", citation, e.operands)
                    if set(listing.keys()) - {"schemaFamily", "schemaMajor", "compatibleClosures"} and listing.get("schemaFamily"):
                        # DetectorManifestV1 additionalProperties false
                        extra = set(listing.keys()) - {"schemaFamily", "schemaMajor", "compatibleClosures"}
                        if extra:
                            self.refuse("L-DET-COMPAT-SHAPE", "DETECTOR_MANIFEST_SHAPE", "DetectorManifestV1 additionalProperties false", citation, {"extra": sorted(extra)})
        self.mark_pass("L-COMPONENT-PROFILE", citation, "component manifests admitted under metadata profile and prose field table; tree projection checked", {"nClosures": len(self.closures)})

    # ----- execution inputs -----

    def _phase_execution_inputs(self):
        citation = "execution-inputs-contract.v1.md §§1–5; identity-and-evidence.md§3 executionInputsDigest"
        ei = self.execution_inputs
        if not isinstance(ei, dict):
            self.refuse("L-EI-MISSING", "EXECUTION_INPUTS_MISSING", "proof.executionInputsDigest preimage missing", citation, {})
        if ei.get("planId") != self.run["planId"]:
            self.refuse("L-EI-PLAN", "EXECUTION_INPUTS_PLAN", "ExecutionInputs.planId must equal the Run Plan", citation, {"ei": ei.get("planId"), "run": self.run["planId"]})
        if ei.get("executionPlanId") != self.proof["executionPlanId"]:
            self.refuse("L-EI-EXEC-PLAN", "EXECUTION_INPUTS_EXEC_PLAN", "ExecutionInputs.executionPlanId must equal proof.executionPlanId", citation, {})
        if ei.get("analysisSpecDigest") != self.plan["analysisSpecDigest"]:
            self.refuse("L-EI-ASPEC", "EXECUTION_INPUTS_ANALYSIS_SPEC", "ExecutionInputs.analysisSpecDigest must equal plan.analysisSpecDigest", citation, {"ei": ei.get("analysisSpecDigest"), "plan": self.plan["analysisSpecDigest"]})
        if ei.get("enumerationPlanDigest"):
            self._admit_canonical(
                ei["enumerationPlanDigest"],
                self.kit.enumeration_plan_schema,
                "#",
                "executionInputs.enumerationPlanDigest",
            )
        # selectedRefs exact totality — structural membership
        sel = ei.get("selectedRefs") or ei.get("selected") or {}
        # schema may use arrays of refs
        # Forbidden domains
        def scan_refs(obj, pth):
            if isinstance(obj, dict):
                if "domain" in obj and obj["domain"] in PROOF_INPUT_FORBIDDEN:
                    self.refuse("L-EI-FORBIDDEN", "EXECUTION_INPUTS_FORBIDDEN_DOMAIN", "selectedRefs must not include proof/finding/seal/run/evidence", citation, {"domain": obj["domain"], "path": pth})
                for k, v in obj.items():
                    scan_refs(v, pth + "." + k)
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    scan_refs(v, f"{pth}[{i}]")
        scan_refs(ei, "executionInputs")
        # imports in EI equal plan.importIds
        # Try common field locations
        import_refs = []
        if isinstance(sel, dict):
            import_refs = sel.get("imports") or sel.get("import") or []
        if import_refs:
            got = {strip_typed(x) for x in import_refs}
            exp = {i.split(":")[1] for i in self.plan["importIds"]}
            if got != exp:
                self.refuse("L-EI-IMPORTS", "EXECUTION_INPUTS_IMPORTS", "execution-inputs imports must equal Plan importIds", citation, {"got": sorted(got), "expected": sorted(exp)})
        # views from evidence
        view_hexes = {v.split(":")[1] for v in self.evidence["viewIds"]}
        # hostCapture stage receipts if present
        hc = ei.get("hostCapture") or {}
        receipts = hc.get("stageReceipts") or ei.get("stageReceipts") or []
        if self.exec_plan and receipts:
            stages = self.exec_plan.get("stages") or []
            if len(receipts) != len(stages):
                self.refuse("L-EI-RECEIPTS", "EXECUTION_INPUTS_STAGE_RECEIPTS", "one receipt per execution-plan stage", citation, {"receipts": len(receipts), "stages": len(stages)})
        self.mark_pass("L-EXECUTION-INPUTS", citation, "ExecutionInputsV1 retained, schema-valid, forbidden domains absent", {})

    def _phase_joins(self):
        citation = "identity-and-evidence.md§3 remaining joins"
        # vcs sourceInventoryDigest equals snapshot inventory digest
        vcs = self._admit_canonical(self.snapshot["vcsDigest"], self.kit.identity_v3, "#/$defs/vcs-observation", "snapshot.vcsDigest")
        inv_c = encode_c(self.snapshot["sourceInventory"], profile="product")
        if vcs.get("sourceInventoryDigest") != sha256_hex(inv_c):
            self.refuse("L-VCS-INV", "VCS_INVENTORY_DIGEST", "vcs-observation.sourceInventoryDigest must equal digest of snapshot inventory", citation, {"claimed": vcs.get("sourceInventoryDigest"), "actual": sha256_hex(inv_c)})
        self.mark_pass("L-VCS-INV", citation, "vcs sourceInventoryDigest matches snapshot inventory", {})
        # grant projectId
        grant = self.canonical_records.get(self.plan["semanticGrantDigest"])
        if grant and grant.get("projectId") and grant["projectId"] != self.run["projectId"]:
            self.refuse("L-GRANT-PRJ", "GRANT_PROJECT", "semantic-grant ProjectId must join the Run", citation, {})
        self.mark_pass("L-GRANT-PRJ", citation, "semantic-grant ProjectId joins Run", {})
        # extra authoritative roots: unreferenced CAS is OK; missing required is already refused
        self.mark_pass("L-NO-HIDDEN-ROOTS", citation, "walked graph does not admit a well-formed object outside closure as hidden finding evidence", {})

    def _phase_replay(self):
        from replay import Replay
        citation = "identity-and-evidence.md§4; evaluator-composition-contract.v3.md complete replay"
        if self.first_refusal is not None:
            self.replay_result = {"status": "NOT_REACHED", "reason": "structural admission refused first"}
            return
        r = Replay(self)
        try:
            self.replay_result = r.run()
        except AdmissionError:
            self.replay_result = r.result if isinstance(getattr(r, "result", None), dict) else {
                "status": "REPLAY_REFUSE",
                "firstRefusal": self.first_refusal,
            }
            raise
        self.mark_pass("L-REPLAY-AFTER-ADMISSION", citation, "semantic replay executed after structural admission", {"status": self.replay_result.get("status")})


def json_doc(kit: Kit, document: str) -> dict:
    rel_map = {
        "foundation/identity-schemas.v3.json": "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
        "native/native-evidence.schemas.v2.json": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
        "foundation/relation-payload-schemas.v2.json": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
        "workflows/schemas/policy-document.v2.schema.json": "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
        "workflows/schemas/policy-document.schema.json": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
        "workflows/schemas/imported-evidence.schema.json": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
        "workflows/schemas/common.schema.json": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
        "workflows/schemas/test-execution.schema.json": "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
        "foundation/import-source-context.schema.json": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
        "foundation/enumeration-plan.schema.v1.json": "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
        "foundation/evaluator-emission-plan.schema.v1.json": "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json",
        "foundation/execution-inputs.schema.v1.json": "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
        "foundation/subject-inventory.schema.v1.json": "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
        "docs/coop/design-corrections/workflows/schemas/common.schema.json": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
        "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
        "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json": "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
    }
    rel = rel_map.get(document, document)
    if rel not in kit.file_bytes:
        # suffix
        for k in kit.file_bytes:
            if k.endswith(document) or k.endswith("/" + document.split("/")[-1]):
                rel = k
                break
    import json
    return json.loads(kit.file_bytes[rel])


def path_get(obj: Any, path: list[str]):
    cur = obj
    for p in path:
        if p == "[]":
            return cur
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def path_collect(obj: Any, path: list[str]) -> list:
    if not path:
        return [obj]
    p0 = path[0]
    rest = path[1:]
    if p0 == "[]":
        if isinstance(obj, list):
            out = []
            for item in obj:
                out.extend(path_collect(item, rest) if rest else [item])
            return out
        return []
    if isinstance(obj, dict) and p0 in obj:
        return path_collect(obj[p0], rest) if rest else [obj[p0]]
    return []


def strip_hex(val: Any, form: str | None) -> str | None:
    if not isinstance(val, str):
        return None
    if form in ("sha256-text", None) and val.startswith("sha256:"):
        return val.split(":", 1)[1]
    if form in ("closure2-identity",) and val.startswith("closure2:"):
        return val.split(":", 1)[1]
    if HEX64.match(val):
        return val
    m = TYPED_ID.match(val)
    if m:
        return m.group(2)
    return None


def strip_typed(val: Any) -> str:
    if isinstance(val, dict) and "digest" in val:
        return val["digest"]
    if isinstance(val, str):
        if ":" in val:
            return val.split(":", 1)[1]
        return val
    return str(val)


def _relation_selector(row: dict, rel: str) -> str:
    if "selector" in row:
        return row["selector"]
    # convention
    mapping = {
        "file": "#/$defs/FilePayloadV1",
        "package": "#/$defs/PackagePayloadV1",
        "clones": "#/$defs/ClonesPayloadV1",
        "declares": "#/$defs/DeclaresPayloadV1",
        "literal": "#/$defs/LiteralPayloadV1",
        "control-flow": "#/$defs/ControlFlowPayloadV1",
        "imports": "#/$defs/ImportsPayloadV1",
        "references": "#/$defs/ReferencesPayloadV1",
        "calls": "#/$defs/CallsPayloadV1",
        "types": "#/$defs/TypesPayloadV1",
        "reachability": "#/$defs/ReachabilityPayloadV1",
        "vcs-change": "#/$defs/VcsChangePayloadV1",
        "unresolved-edge": "#/$defs/UnresolvedEdgePayloadV1",
    }
    return mapping.get(rel, "#")


def parse_body_frame(frame: bytes) -> dict:
    citation = "fact-identity-policy.v2.json#/canonicalisationSchema/byteGrammar"
    i = 0

    def u8_len_bytes():
        nonlocal i
        if i >= len(frame):
            raise AdmissionError("BODY_FRAME_TRUNC", "truncated body frame", citation, {})
        n = frame[i]
        i += 1
        if i + n > len(frame):
            raise AdmissionError("BODY_FRAME_TRUNC", "truncated length-prefixed component", citation, {"n": n})
        b = frame[i : i + n]
        i += n
        return b

    tag = u8_len_bytes()
    if tag != b"opensip.fact-identity.v1":
        raise AdmissionError("BODY_FRAME_TAG", "domain tag is not opensip.fact-identity.v1", citation, {"tag": tag.decode("latin1", "replace")})
    level_id = u8_len_bytes().decode("ascii")
    level_ver = u8_len_bytes()
    if len(level_ver) != 32:
        raise AdmissionError("BODY_LEVEL_VERSION_WIDTH", "levelVersion is raw 32 digest bytes, never hex display", citation, {"len": len(level_ver)})
    lang = u8_len_bytes().decode("ascii")
    lang_ver = u8_len_bytes()
    if len(lang_ver) != 32:
        raise AdmissionError("BODY_LANG_VERSION_WIDTH", "languageVersion is raw 32 digest bytes", citation, {"len": len(lang_ver)})
    if i + 4 > len(frame):
        raise AdmissionError("BODY_FRAME_TRUNC", "truncated payload length", citation, {})
    plen = struct.unpack(">I", frame[i : i + 4])[0]
    i += 4
    payload = frame[i : i + plen]
    if len(payload) != plen or i + plen != len(frame):
        raise AdmissionError("BODY_FRAME_PAYLOAD_LEN", "payload length does not consume the remainder", citation, {"declared": plen, "remaining": len(frame) - i})
    return {
        "levelId": level_id,
        "levelVersion": level_ver,
        "levelVersionHex": level_ver.hex(),
        "languageId": lang,
        "languageVersion": lang_ver,
        "payload": payload,
        "payloadLen": plen,
    }


def parse_token_stream(payload: bytes, citation: str) -> None:
    if len(payload) < 4:
        raise AdmissionError("TOKEN_STREAM", "token stream shorter than count", citation, {})
    n = struct.unpack(">I", payload[:4])[0]
    i = 4
    for _ in range(n):
        if i + 2 > len(payload):
            raise AdmissionError("TOKEN_STREAM", "truncated kind_id_len", citation, {})
        klen = struct.unpack(">H", payload[i : i + 2])[0]
        i += 2
        i += klen
        if i + 4 > len(payload):
            raise AdmissionError("TOKEN_STREAM", "truncated value_len", citation, {})
        vlen = struct.unpack(">I", payload[i : i + 4])[0]
        i += 4
        i += vlen
    if i != len(payload):
        raise AdmissionError("TOKEN_STREAM", "token stream trailing bytes", citation, {"i": i, "n": len(payload)})


def longest_suffix(path: str, table: dict) -> str | None:
    best = None
    best_len = -1
    name = path.rsplit("/", 1)[-1]
    for suf, token in table.items():
        if name.endswith(suf) and len(suf) > best_len:
            best = token
            best_len = len(suf)
    return best


def grammar_for_path(grammars: list, path: str) -> dict | None:
    name = path.rsplit("/", 1)[-1]
    best = None
    best_len = -1
    for g in grammars:
        for suf in g.get("suffixes") or []:
            if name.endswith(suf) and len(suf) > best_len:
                best = g
                best_len = len(suf)
    return best


def select_body_language(bind: dict, path: str, urec: dict, fact: dict, admit: Admit) -> tuple[str, str]:
    dialect = bind.get("dialect") or {}
    form = dialect.get("form")
    if form == "closed-suffix-table":
        token = longest_suffix(path, dialect.get("table") or {})
        if token is None:
            raise AdmissionError(dialect.get("onUnknown") or "BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN", "suffix not in dialect table", "identity-schemas.v3.json languageVersionBinding.dialect", {"path": path})
        by = bind.get("bodyLanguageByVariant") or {}
        lang = by.get(token)
        if not lang:
            raise AdmissionError("BODY_LANGUAGE_VARIANT", "variant has no bodyLanguageByVariant mapping", "identity-and-evidence.md§3 clones languageIdSource", {"token": token})
        return lang, token
    if form and "ownership" in str(form).lower() or dialect.get("key") == "edition":
        # Rust ownership
        own_id = urec.get("sourceUnitOwnershipId")
        if not own_id:
            raise AdmissionError("BODY_LANGUAGE_NO_OWNERSHIP", "Rust clones require committed SourceUnitOwnershipV1", "native-evidence.md§11", {})
        hx = strip_hex(own_id, "sha256-text") or strip_hex(own_id, "bare-hex")
        own = admit.admitted.get(("h-identity", hx))
        if own is None:
            own = admit._admit_h_domain_set(hx, "native-nested", field="sourceUnitOwnershipId")
        if own.get("enumeration") == "partial":
            raise AdmissionError("BODY_LANGUAGE_PARTIAL", "partial enumeration admits no body dialect", "identity-and-evidence.md§3", {})
        units = {u["unitId"]: u for u in own.get("units") or []}
        selected = set(own.get("selectedUnitIds") or [])
        owners = [o for o in (own.get("ownership") or []) if o.get("path") == path]
        if not owners:
            raise AdmissionError("BODY_LANGUAGE_OWNER_NOT_COMPILED", "path owned by no compilation unit", "native-evidence.md§11", {"path": path})
        sel_owners = [o for o in owners if o.get("unitId") in selected]
        if not sel_owners:
            raise AdmissionError("BODY_LANGUAGE_OWNER_NOT_SELECTED", "path owned only by unselected targets", "native-evidence.md§11", {"path": path})
        editions = []
        emap = urec.get("edition") or urec.get("editionMap") or {}
        for o in sel_owners:
            u = units.get(o["unitId"])
            if not u:
                raise AdmissionError("BODY_LANGUAGE_UNIT_UNDECLARED", "ownership names undeclared unitId", "native-evidence.md§11", {"unitId": o["unitId"]})
            ed = u.get("targetEdition")
            if ed is None:
                ed = emap.get(u.get("crateName"))
            editions.append(ed)
        if len(set(editions)) != 1:
            raise AdmissionError("BODY_LANGUAGE_EDITION_AMBIGUOUS", "selected owners disagree on effective edition", "native-evidence.md§11", {"editions": editions, "path": path})
        return "rust", str(editions[0])
    lang = bind.get("bodyLanguage")
    if not lang:
        raise AdmissionError("NATIVE_UNIVERSE_BINDING_UNAVAILABLE", "universe domain used by clones has no dialect binding", "identity-and-evidence.md§3", {})
    return lang, ""


def derive_body_language_version(bind: dict, urec: dict, contexts: dict, dialect_token: str, lang_id: str) -> dict:
    ctx_hex = strip_hex(urec["nativeContextId"], "sha256-text")
    ctx = contexts[ctx_hex][1]
    fields = bind.get("fields") or {}

    def src(spec):
        if spec.get("source") == "native-context":
            return path_get(ctx, spec["path"])
        return None

    rec = {
        "schemaVersion": 1,
        "languageId": lang_id,
        "compilerName": src(fields.get("compilerName") or {}),
        "compilerVersion": src(fields.get("compilerVersion") or {}),
        "compilerBuild": src(fields.get("compilerBuild") or {}),
        "dialect": {bind.get("dialect", {}).get("key", "sourceVariant"): dialect_token} if dialect_token != "" else {bind.get("dialect", {}).get("key", "edition"): dialect_token},
    }
    return rec


def locate_predicate(program: dict, rule_id: str, address: str):
    rule = None
    for r in program.get("rules") or []:
        if r.get("ruleId") == rule_id:
            rule = r
            break
    if rule is None:
        return None
    node = rule.get("emitWhen")
    if address == "p":
        return node
    if not address.startswith("p"):
        return None
    rest = address[1:]
    cur = node
    while rest:
        if not rest.startswith("."):
            return None
        rest = rest[1:]
        num = ""
        while rest and rest[0].isdigit():
            num += rest[0]
            rest = rest[1:]
        if not num or (len(num) > 1 and num.startswith("0")):
            return None
        idx = int(num)
        ops = cur.get("operands") or cur.get("args") or []
        if idx >= len(ops):
            return None
        cur = ops[idx]
    return cur


def child_addresses(address: str, node: dict) -> list[str]:
    op = node.get("op")
    ops = node.get("operands") or node.get("args") or []
    if op == "not":
        return [address + ".0"] if ops else []
    if op in ("and", "or"):
        return [f"{address}.{i}" for i in range(len(ops))]
    return []


def decode_cve1_or_refuse(raw: bytes, admit: Admit) -> dict:
    """Decode CVE1 committed capability-manifest bytes. No repair."""
    citation = "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding"
    try:
        val, rest = _cve1_decode(raw, 0)
    except AdmissionError:
        raise
    except Exception as e:
        raise AdmissionError("CVE1_DECODE", f"CVE1 decode failed: {e}", citation, {}) from e
    if rest != len(raw):
        raise AdmissionError("CVE1_TRAILING", "CVE1 trailing bytes", citation, {"rest": rest, "n": len(raw)})
    if not isinstance(val, dict):
        raise AdmissionError("CVE1_NOT_RECORD", "committed capability manifest is not a map", citation, {"type": type(val).__name__})
    return val


def _cve1_decode(raw: bytes, i: int) -> tuple[Any, int]:
    citation = "resolved-inputs.v2.json#planIdContract.canonicalValueEncoding"
    if i >= len(raw):
        raise AdmissionError("CVE1_TRUNC", "truncated CVE1", citation, {})
    tag = raw[i]
    i += 1
    if tag == 0x00:
        return None, i
    if tag == 0x01:
        return False, i
    if tag == 0x02:
        return True, i
    if tag == 0x03:
        if i + 8 > len(raw):
            raise AdmissionError("CVE1_TRUNC", "truncated u64", citation, {})
        v = struct.unpack(">Q", raw[i : i + 8])[0]
        return v, i + 8
    if tag == 0x07:
        if i + 8 > len(raw):
            raise AdmissionError("CVE1_TRUNC", "truncated i64", citation, {})
        v = struct.unpack(">q", raw[i : i + 8])[0]
        if v >= 0:
            raise AdmissionError("CVE1_I64NEG", "negative-signed-64 tag with non-negative value", citation, {})
        return v, i + 8
    if tag == 0x04:
        if i + 4 > len(raw):
            raise AdmissionError("CVE1_TRUNC", "truncated string len", citation, {})
        n = struct.unpack(">I", raw[i : i + 4])[0]
        i += 4
        b = raw[i : i + n]
        if len(b) != n:
            raise AdmissionError("CVE1_TRUNC", "truncated string", citation, {})
        s = b.decode("utf-8")
        import unicodedata
        if not unicodedata.is_normalized("NFC", s):
            raise AdmissionError("CVE1_NON_NFC", "CVE1 string not NFC", citation, {})
        return s, i + n
    if tag == 0x05:
        if i + 4 > len(raw):
            raise AdmissionError("CVE1_TRUNC", "truncated array count", citation, {})
        n = struct.unpack(">I", raw[i : i + 4])[0]
        i += 4
        arr = []
        for _ in range(n):
            v, i = _cve1_decode(raw, i)
            arr.append(v)
        return arr, i
    if tag == 0x06:
        if i + 4 > len(raw):
            raise AdmissionError("CVE1_TRUNC", "truncated map count", citation, {})
        n = struct.unpack(">I", raw[i : i + 4])[0]
        i += 4
        items = []
        prev_key_b = None
        d = {}
        for _ in range(n):
            k, i = _cve1_decode(raw, i)
            v, i = _cve1_decode(raw, i)
            if not isinstance(k, str):
                raise AdmissionError("CVE1_MAP_KEY", "map key not string", citation, {})
            kb = k.encode("utf-8")
            if prev_key_b is not None and kb <= prev_key_b:
                raise AdmissionError("CVE1_MAP_ORDER", "map keys not strict unsigned lexicographic NFC UTF-8 order", citation, {"key": k})
            prev_key_b = kb
            if k in d:
                raise AdmissionError("CVE1_DUP_KEY", "duplicate map key", citation, {"key": k})
            d[k] = v
        return d, i
    raise AdmissionError("CVE1_UNKNOWN_TAG", f"unknown CVE1 tag {tag}", citation, {"tag": tag})
