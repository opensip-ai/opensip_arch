"""From-scratch layered replay of one exported Run.

Truth is derived from retained program/views/facts/Coverage/scopes/imports
and current owners. Claimed proof/witness/verdict flags are comparison
targets only.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from .canonical import (
    encode_c,
    glob_match,
    path_in_scope,
    LexicalRefusal,
)
from .identity import (
    H,
    TYPED_PREFIX,
    PREFIX_TO_DOMAIN,
    capability_manifest_id,
    clone_l0_body_identity,
    parse_h_frame,
    parse_typed_id,
    sha256,
    sha256_text_to_hex,
    typed_id,
)
from .kit_owners import KitOwners
from .schema_validate import (
    build_registry,
    schema_for_identity_def,
    schema_for_native_def,
    validate_against,
)
from .store import Store, decode_record

DOMAIN_TO_DEF = {
    "snapshot": "snapshot",
    "closure": "closure",
    "import": "import",
    "plan": "plan",
    "subject-scope": "subject-scope",
    "fact": "fact",
    "coverage": "coverage",
    "view": "view",
    "execution-plan": "execution-plan",
    "finding-fingerprint": "finding-fingerprint",
    "evaluation-subject": "evaluation-subject",
    "finding": "finding",
    "proof-bundle": "proof-bundle",
    "semantic-evidence": "semantic-evidence",
    "evaluation-seal": "evaluation-seal",
    "run": "run",
    "cache-key": "cache-key",
    "regeneration-key": "regeneration-key",
    "policy-derivation": "policy-derivation",
}

NATIVE_CONTEXT_DEFS = {
    "native.context.typescript.v2": "TypeScriptNativeContextV2",
    "native.context.rust.v2": "NativeContextV2",
    "native.context.syntax.v2": "SyntaxNativeContextV2",
}
NATIVE_UNIVERSE_DEFS = {
    "native.semantic-universe.typescript.v2": "TypeScriptUniverseV2ResolvedInputs",
    "native.semantic-universe.rust.v2": "RustUniverseV2ResolvedInputs",
    "native.semantic-universe.syntax.v2": "SyntaxUniverseV2ResolvedInputs",
}
NATIVE_NESTED_DEFS = {
    "native.dependency-source-set.v1": "DependencySourceSetV1",
    "native.dependency-file-manifest.v1": "DependencyFileManifestV1",
    "native.unified-features.rust.v1": "UnifiedFeaturesV1",
    "native.prepared-output-set.v3": "PreparedOutputSetV3",
    "native.cargo-config-projection.v2": "CargoConfigProjectionV2",
    "native.source-unit-ownership.v1": "SourceUnitOwnershipV1",
}

POLICY_UNIVERSE_DEFAULT = {
    "typescript": "native.semantic-universe.typescript.v2",
    "rust": "native.semantic-universe.rust.v2",
    "syntax": "native.semantic-universe.syntax.v2",
}

SEV_RANK = {"note": 0, "warning": 1, "error": 2}


@dataclass
class LayerResult:
    name: str
    status: str  # PASS | REFUSED | notReached | DIAGNOSTIC
    first_refusal: dict[str, Any] | None = None
    faults: list[dict[str, Any]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    operands: dict[str, Any] = field(default_factory=dict)

    def refuse(self, code: str, message: str, **extra: Any) -> None:
        rec = {"code": code, "message": message, **extra}
        self.faults.append(rec)
        if self.first_refusal is None:
            self.first_refusal = rec
            self.status = "REFUSED"

    def note(self, s: str) -> None:
        self.notes.append(s)


class IndependentReplay:
    def __init__(self, owners: KitOwners, store: Store, registry):
        self.owners = owners
        self.store = store
        self.registry = registry
        self.records: dict[str, Any] = {}  # digest -> decoded payload/meta
        self.by_typed: dict[str, Any] = {}
        self.by_domain: dict[str, list[tuple[str, Any]]] = {}
        self.canonical_by_digest: dict[str, Any] = {}
        self.raw_artifacts: dict[str, bytes] = {}
        self.snapshot_paths: dict[str, dict[str, Any]] = {}
        self.claimed_proof: Any = None
        self.claimed_run: Any = None

    def run(self) -> dict[str, Any]:
        raw = self.layer_raw()
        structural = LayerResult("structural", "notReached")
        semantic = LayerResult("fullsemantic", "notReached")
        if raw.status == "REFUSED":
            return self._finish(raw, structural, semantic)
        structural = self.layer_structural()
        if structural.status == "REFUSED":
            # later layer is diagnostic only; never PASS through failed admission
            try:
                semantic = self.layer_semantic()
                if semantic.status == "PASS":
                    semantic.status = "DIAGNOSTIC"
                    semantic.note("structural refused; semantic results are diagnostic and not admission")
            except Exception as e:
                semantic.status = "notReached"
                semantic.note(f"semantic notReached after structural refusal: {type(e).__name__}: {e}")
            return self._finish(raw, structural, semantic)
        semantic = self.layer_semantic()
        return self._finish(raw, structural, semantic)

    def _finish(self, raw, structural, semantic) -> dict[str, Any]:
        statuses = [raw.status, structural.status, semantic.status]
        if "REFUSED" in statuses:
            scoped = "FOUR_RUN_REFUSED"
        elif "notReached" in statuses:
            scoped = "FOUR_RUN_INCOMPLETE"
        elif all(s == "PASS" for s in statuses):
            scoped = "FOUR_RUN_FULL_ADMIT"
        else:
            scoped = "FOUR_RUN_INCOMPLETE"
        first = raw.first_refusal or structural.first_refusal or semantic.first_refusal
        return {
            "exportName": self.store.name,
            "exportPath": self.store.path,
            "exportSha256": self.store.sha256,
            "exportBytes": self.store.bytes_len,
            "runId": next((k for k in self.store.object_table if k.startswith("run3:")), None),
            "layers": {
                "raw": _layer_dict(raw),
                "structural": _layer_dict(structural),
                "fullsemantic": _layer_dict(semantic),
            },
            "scopedRunVerdict": scoped,
            "firstRefusal": first,
            "notReached": [n for n, s in (("structural", structural.status), ("fullsemantic", semantic.status)) if s == "notReached"],
        }

    # ----- RAW -----
    def layer_raw(self) -> LayerResult:
        L = LayerResult("raw", "PASS")
        L.operands["objectTableCount"] = len(self.store.object_table)
        L.operands["blobCount"] = len(self.store.blobs)
        for f in self.store.raw_faults:
            L.refuse(f.get("code", "RAW"), json.dumps(f), **f)
            if L.status == "REFUSED" and L.first_refusal:
                # keep collecting
                pass
        prefixes = {}
        for key in self.store.object_table:
            p = key.split(":", 1)[0] if ":" in key else "barehex"
            prefixes[p] = prefixes.get(p, 0) + 1
        L.operands["keyPrefixes"] = prefixes
        if not any(k.startswith("run3:") for k in self.store.object_table):
            L.refuse("NO_RUN3", "object table has no run3: key")
        if L.first_refusal:
            L.status = "REFUSED"
        return L

    # ----- STRUCTURAL -----
    def layer_structural(self) -> LayerResult:
        L = LayerResult("structural", "PASS")
        owners = self.owners
        kinds_by_digest: dict[str, set[str]] = {}
        labels_by_digest: dict[str, set[str]] = {}
        for meta in self.store.meta.values():
            kinds_by_digest.setdefault(meta.digest, set()).add(meta.kind)
            if meta.label:
                labels_by_digest.setdefault(meta.digest, set()).add(meta.label)
        L.operands["kindsByDigestSample"] = {k: sorted(v) for k, v in list(kinds_by_digest.items())[:8]}

        # decode every blob
        for digest, raw in self.store.blobs.items():
            dec = decode_record(raw)
            self.records[digest] = {"raw": raw, **dec}
            kinds = kinds_by_digest.get(digest) or set()
            if dec.get("form") == "raw-artifact" or (dec.get("form") == "canonical-record-or-json" and dec.get("json_error")):
                self.raw_artifacts[digest] = raw
            if dec.get("form") == "h-identity" and "payload" in dec:
                self.by_domain.setdefault(dec["domain"], []).append((digest, dec["payload"]))
                if not dec.get("c_matches"):
                    L.refuse(
                        "H_PAYLOAD_NOT_C",
                        f"H({dec['domain']}) payload is not C of its parse",
                        digest=digest,
                    )
                expected = sha256(raw)
                if expected != digest:
                    L.refuse("H_DIGEST", f"frame sha {expected} != key {digest}")
            elif dec.get("form") == "canonical-record-or-json" and "payload" in dec:
                self.canonical_by_digest[digest] = dec["payload"]
                # raw-artifact schema/source documents may be pretty-printed JSON;
                # C-byte identity is required only of canonical-record retention.
                if "canonical-record" in kinds and not dec.get("c_matches"):
                    L.refuse(
                        "CANONICAL_NOT_C",
                        "retained canonical-record JSON bytes are not C(record)",
                        digest=digest,
                        labels=sorted(labels_by_digest.get(digest) or []),
                    )
                if kinds <= {"raw-artifact"} or (not kinds and "canonical-record" not in kinds):
                    self.raw_artifacts[digest] = raw

        # index typed object-table keys
        for key, meta in self.store.meta.items():
            if ":" in key:
                self.by_typed[key] = self.records.get(meta.digest)

        run_keys = [k for k in self.store.object_table if k.startswith("run3:")]
        if len(run_keys) != 1:
            L.refuse("RUN_COUNT", f"expected one run3, found {run_keys}")
            return L
        run_dec = self.by_typed[run_keys[0]]
        if not run_dec or run_dec.get("domain") != "run":
            L.refuse("RUN_DOMAIN", f"run frame domain {run_dec.get('domain') if run_dec else None}")
            return L
        run = run_dec["payload"]
        self.claimed_run = run
        L.operands["run"] = run
        self._validate_identity_def(L, "run", run, run_keys[0])

        # recompute run identity
        recomputed_run = typed_id("run", run)
        if recomputed_run != run_keys[0]:
            L.refuse("RUN_IDENTITY", f"recomputed {recomputed_run} claimed {run_keys[0]}")

        # follow Run graph
        for field, domain_prefix in [
            ("snapshotId", "snapshot2"),
            ("planId", "plan2"),
            ("evidenceId", "evidence3"),
            ("evaluationSealId", "seal3"),
        ]:
            ref = run[field]
            if ref not in self.store.object_table:
                L.refuse("RUN_REF_MISSING", f"{field} {ref} not in object table")
                continue
            rec = self.by_typed.get(ref)
            if not rec or rec.get("form") != "h-identity":
                L.refuse("RUN_REF_NOT_FRAME", field, ref=ref)
                continue
            want_domain = PREFIX_TO_DOMAIN[domain_prefix]
            if rec["domain"] != want_domain:
                L.refuse("RUN_REF_DOMAIN", f"{field} domain {rec['domain']} want {want_domain}")
            ident = f"{domain_prefix}:{H(want_domain, rec['payload'])}"
            if ident != ref:
                L.refuse("RUN_REF_IDENTITY", f"{field} recomputed {ident} claimed {ref}")
            defn = DOMAIN_TO_DEF[want_domain]
            self._validate_identity_def(L, defn, rec["payload"], ref)

        if L.first_refusal:
            return L

        plan_id = run["planId"]
        plan = self.by_typed[plan_id]["payload"]
        snap = self.by_typed[run["snapshotId"]]["payload"]
        evidence = self.by_typed[run["evidenceId"]]["payload"]
        seal = self.by_typed[run["evaluationSealId"]]["payload"]
        L.operands["planId"] = plan_id
        L.operands["capabilityManifestId"] = run["capabilityManifestId"]

        if plan.get("snapshotId") != run["snapshotId"]:
            L.refuse("PLAN_SNAPSHOT", "plan.snapshotId != run.snapshotId")
        if seal.get("planId") != plan_id:
            L.refuse("SEAL_PLAN", "seal.planId != run.planId")
        if evidence.get("planId") != plan_id:
            L.refuse("EVIDENCE_PLAN", "evidence.planId != run.planId")
        if seal.get("evidenceId") != run["evidenceId"]:
            L.refuse("SEAL_EVIDENCE", "seal.evidenceId != run.evidenceId")
        if seal.get("proofBundleId") != evidence.get("proofBundleId"):
            L.refuse("SEAL_PROOF", "seal.proofBundleId != evidence.proofBundleId")
        if run["capabilityManifestId"] != plan["capabilityManifestId"]:
            L.refuse("CAP_ID_JOIN", "run vs plan capabilityManifestId")

        # capability manifest derived
        cap_bytes_digest = plan["capabilityManifestBytesDigest"]
        cap_bytes = self.store.blob(cap_bytes_digest)
        if cap_bytes is None:
            L.refuse("CAP_BYTES_MISSING", cap_bytes_digest)
        else:
            derived = capability_manifest_id(cap_bytes)
            if derived != plan["capabilityManifestId"]:
                L.refuse("CAP_ID_DERIVE", f"derived {derived} claimed {plan['capabilityManifestId']}")

        # snapshot inventory join
        inv = snap.get("sourceInventory")
        L.operands["snapshotInventoryType"] = type(inv).__name__
        self._ingest_snapshot_inventory(L, snap, inv)

        # canonical-record joins named by plan
        self._join_plan_canonicals(L, plan)
        self._join_closures(L, plan)
        self._join_native_contexts(L, plan)
        self._join_facts_coverage_view(L, evidence, plan)
        self._join_import(L, plan, evidence)
        self._acyclic_check(L, run, evidence, seal, plan)

        proof_id = evidence.get("proofBundleId")
        if proof_id not in self.by_typed:
            L.refuse("PROOF_MISSING", str(proof_id))
        else:
            proof_dec = self.by_typed[proof_id]
            if proof_dec.get("domain") != "proof-bundle":
                L.refuse("PROOF_DOMAIN", str(proof_dec.get("domain")))
            else:
                proof = proof_dec["payload"]
                self.claimed_proof = proof
                self._validate_identity_def(L, "proof-bundle", proof, proof_id)
                recomputed_p = typed_id("proof-bundle", proof)
                if recomputed_p != proof_id:
                    L.refuse("PROOF_IDENTITY", f"{recomputed_p} vs {proof_id}")
                if proof.get("planId") != plan_id:
                    L.refuse("PROOF_PLAN", "proof.planId != run.planId")
                if "verdict" in proof:
                    L.operands["claimedVerdict"] = proof["verdict"]
                # proof must not contain evidenceId/runId
                dumped = json.dumps(proof)
                if '"evidenceId"' in dumped or run_keys[0] in dumped:
                    # only refuse if fields exist
                    if "evidenceId" in proof or "runId" in proof:
                        L.refuse("ACYCLIC_PROOF_CONTAINS_EVIDENCE_OR_RUN", "proof names evidence/run")
                exec_in = proof.get("executionInputsDigest")
                if not exec_in or exec_in not in self.store.blobs:
                    L.refuse("EXECUTION_INPUTS_MISSING", str(exec_in))
                else:
                    ei_dec = self.records.get(exec_in) or decode_record(self.store.blobs[exec_in])
                    if "payload" not in ei_dec:
                        L.refuse("EXECUTION_INPUTS_PARSE", str(exec_in))
                    else:
                        ei = ei_dec["payload"]
                        if encode_c(ei) != self.store.blobs[exec_in] and not ei_dec.get("c_matches"):
                            L.refuse("EXECUTION_INPUTS_NOT_C", exec_in)
                        self._validate_document(L, owners.exec_inputs, ei, "execution-inputs")
                        if sha256(encode_c(ei)) != exec_in:
                            # if stored bytes are C, digest is sha of stored
                            if sha256(self.store.blobs[exec_in]) != exec_in:
                                L.refuse("EXECUTION_INPUTS_DIGEST", exec_in)
                        L.operands["executionInputsDigest"] = exec_in
                        self.canonical_by_digest[exec_in] = ei

        if L.first_refusal:
            L.status = "REFUSED"
        return L

    def _validate_identity_def(self, L: LayerResult, def_name: str, instance: Any, loc: str) -> None:
        schema = schema_for_identity_def(self.owners, def_name)
        faults = validate_against(instance, schema, self.registry, self.owners.identity_v3.get("$id"))
        for f in faults:
            L.refuse("IDENTITY_SCHEMA", f, defName=def_name, loc=loc)

    def _validate_native_def(self, L: LayerResult, def_name: str, instance: Any, loc: str) -> None:
        schema = schema_for_native_def(self.owners, def_name)
        faults = validate_against(instance, schema, self.registry, self.owners.native.get("$id"))
        for f in faults:
            L.refuse("NATIVE_SCHEMA", f, defName=def_name, loc=loc)

    def _validate_document(self, L: LayerResult, schema: dict[str, Any], instance: Any, loc: str) -> None:
        faults = validate_against(instance, schema, self.registry, schema.get("$id"))
        for f in faults:
            L.refuse("DOCUMENT_SCHEMA", f, loc=loc)

    def _ingest_snapshot_inventory(self, L: LayerResult, snap: dict[str, Any], inv: Any) -> None:
        # identity-schemas snapshot.sourceInventory is Blob[] (path, sha256, bytes)
        if isinstance(inv, str) and len(inv) == 64:
            rec = self.canonical_by_digest.get(inv) or (self.records.get(inv) or {}).get("payload")
            if rec is None:
                raw = self.store.blob(inv)
                if raw:
                    d = decode_record(raw)
                    rec = d.get("payload")
                    if rec is not None:
                        self.canonical_by_digest[inv] = rec
            if isinstance(rec, (dict, list)):
                self._rows_from_source_inventory(L, rec)
            else:
                L.refuse("SNAPSHOT_INVENTORY_PREIMAGE", inv)
            return
        if isinstance(inv, (dict, list)):
            self._rows_from_source_inventory(L, inv)
            return
        L.refuse("SNAPSHOT_INVENTORY_SHAPE", type(inv).__name__)

    def _rows_from_source_inventory(self, L: LayerResult, rec: dict[str, Any] | list) -> None:
        if isinstance(rec, list):
            rows = rec
        else:
            rows = rec.get("files") or rec.get("entries") or rec.get("rows") or rec.get("blobs") or rec.get("paths")
            if rows is None and "path" in rec:
                rows = [rec]
            if not isinstance(rows, list):
                L.operands["sourceInventoryShape"] = list(rec.keys())
                for key in ("inventory", "members"):
                    if isinstance(rec.get(key), list):
                        rows = rec[key]
                        break
            if not isinstance(rows, list):
                L.refuse("SOURCE_INVENTORY_ROWS", f"keys={list(rec.keys())}")
                return
        for row in rows:
            if not isinstance(row, dict):
                continue
            path = row.get("path")
            if not path:
                continue
            self.snapshot_paths[path] = row
            digest = row.get("digest") or row.get("contentSha256") or row.get("sha256")
            length = row.get("byteLength") or row.get("length") or row.get("size") or row.get("bytes")
            if digest:
                blob = self.store.blob(digest)
                if blob is None:
                    L.refuse("SNAPSHOT_BLOB_MISSING", path, digest=digest)
                else:
                    if length is not None and len(blob) != length:
                        L.refuse("SNAPSHOT_BLOB_LENGTH", path, declared=length, actual=len(blob))
                    if sha256(blob) != digest:
                        L.refuse("SNAPSHOT_BLOB_SHA", path, digest=digest)
        L.operands["snapshotPathCount"] = len(self.snapshot_paths)
        L.operands["snapshotPaths"] = sorted(self.snapshot_paths)

    def _join_plan_canonicals(self, L: LayerResult, plan: dict[str, Any]) -> None:
        owners = self.owners
        mapping = [
            ("analysisSpecDigest", owners.identity_v3["$defs"]["analysis-spec"], "analysis-spec"),
            ("resolvedConfigDigest", owners.identity_v3["$defs"]["semantic-configuration"], "semantic-configuration"),
            ("scopeDigest", owners.identity_v3["$defs"]["scope-descriptor"], "scope-descriptor"),
            ("policyDigest", None, "policy"),
            ("waiverDigest", None, "waiver"),
            ("semanticGrantDigest", owners.identity_v3["$defs"]["semantic-grant"], "semantic-grant"),
        ]
        for field, defn, loc in mapping:
            digest = plan.get(field)
            if not digest:
                L.refuse("PLAN_FIELD_MISSING", field)
                continue
            raw = self.store.blob(digest)
            if raw is None:
                L.refuse("PLAN_PREIMAGE_MISSING", field, digest=digest)
                continue
            dec = self.records.get(digest) or decode_record(raw)
            payload = dec.get("payload")
            if payload is None:
                L.refuse("PLAN_PREIMAGE_PARSE", field, digest=digest)
                continue
            self.canonical_by_digest[digest] = payload
            if field == "policyDigest":
                self._validate_document(L, owners.policy_v2, payload, "PolicyDocumentV2")
            elif field == "waiverDigest":
                # WaiverSetV1 lives in policy-document.schema.json
                schema = dict(owners.policy_v1)
                schema["$ref"] = "#/$defs/WaiverSetV1"
                self._validate_document(L, schema, payload, "WaiverSetV1")
            elif defn is not None:
                sch = schema_for_identity_def(owners, loc)
                faults = validate_against(payload, sch, self.registry)
                for f in faults:
                    L.refuse("PLAN_CANONICAL_SCHEMA", f, field=field)
            if sha256(raw) != digest:
                L.refuse("PLAN_PREIMAGE_SHA", field, digest=digest)

        # analysis-spec parameters: enumeration + emission (+ optional ScopeDocument)
        aspec = self.canonical_by_digest.get(plan["analysisSpecDigest"])
        if isinstance(aspec, dict):
            params = aspec.get("parameters") or []
            L.operands["analysisSpecParameterCount"] = len(params)
            enum_sha = owners.file_sha["docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"]
            emis_sha = owners.file_sha["docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"]
            scope_schema_sha = owners.file_sha["docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"]
            found_enum = found_emis = found_scope = False
            for p in params:
                sd = p.get("schemaDigest")
                pd = p.get("payloadDigest")
                if sd not in self.store.blobs:
                    L.refuse("PARAM_SCHEMA_MISSING", sd)
                else:
                    if sha256(self.store.blobs[sd]) != sd:
                        L.refuse("PARAM_SCHEMA_SHA", sd)
                rawp = self.store.blob(pd) if pd else None
                if rawp is None:
                    L.refuse("PARAM_PAYLOAD_MISSING", str(pd))
                    continue
                dec = decode_record(rawp)
                payload = dec.get("payload")
                if payload is None:
                    L.refuse("PARAM_PAYLOAD_PARSE", pd)
                    continue
                self.canonical_by_digest[pd] = payload
                if sd == enum_sha:
                    found_enum = True
                    self._validate_document(L, owners.enum_plan, payload, "EnumerationPlanV1")
                    L.operands["enumerationPlanDigest"] = pd
                elif sd == emis_sha:
                    found_emis = True
                    self._validate_document(L, owners.emission, payload, "EvaluatorEmissionPlanV1")
                    L.operands["emissionPlanDigest"] = pd
                elif sd == scope_schema_sha:
                    found_scope = True
                    schema = dict(owners.policy_v1)
                    schema["$ref"] = "#/$defs/ScopeDocumentV1"
                    self._validate_document(L, schema, payload, "ScopeDocumentV1")
                    L.operands["scopeDocumentDigest"] = pd
            if not found_enum:
                L.refuse("ENUMERATION_PLAN_PARAM_MISSING", "analysis-spec lacks EnumerationPlanV1 parameter")
            if not found_emis:
                L.refuse("EMISSION_PLAN_PARAM_MISSING", "analysis-spec lacks EvaluatorEmissionPlanV1 parameter")
            L.operands["hasScopeDocumentV1"] = found_scope

    def _join_closures(self, L: LayerResult, plan: dict[str, Any]) -> None:
        closures = plan.get("semanticClosures") or []
        kinds = {}
        for cid in closures:
            rec = self.by_typed.get(cid)
            if not rec or rec.get("domain") != "closure":
                L.refuse("CLOSURE_MISSING", cid)
                continue
            payload = rec["payload"]
            ident = typed_id("closure", payload)
            if ident != cid:
                L.refuse("CLOSURE_IDENTITY", f"{ident} vs {cid}")
            self._validate_identity_def(L, "closure", payload, cid)
            kinds[cid] = payload.get("kind")
            # tree blobs
            for entry in payload.get("tree") or []:
                if not isinstance(entry, dict):
                    continue
                d = entry.get("digest")
                ln = entry.get("byteLength")
                if d:
                    blob = self.store.blob(d)
                    if blob is None:
                        L.refuse("CLOSURE_TREE_BLOB", entry.get("path"), digest=d)
                    elif ln is not None and len(blob) != ln:
                        L.refuse("CLOSURE_TREE_LEN", entry.get("path"), declared=ln, actual=len(blob))
            md = payload.get("manifestDigest")
            if md and md not in self.store.blobs:
                L.refuse("CLOSURE_MANIFEST_MISSING", md, closure=cid)
        L.operands["closureKinds"] = kinds

    def _join_native_contexts(self, L: LayerResult, plan: dict[str, Any]) -> None:
        owners = self.owners
        named = list(plan.get("nativeContextDigests") or [])
        if not named:
            L.refuse("NATIVE_CONTEXT_EMPTY", "plan.nativeContextDigests is empty")
            return
        # retained context frames whose H suffix is in the set
        found = []
        domain_sets = owners.digest_domains["domainSets"]
        ctx_set = domain_sets["native-context"]
        uni_set = domain_sets["native-semantic-universe"]
        nested_set = domain_sets["native-nested"]
        for domain, items in self.by_domain.items():
            if domain in ctx_set:
                for digest, payload in items:
                    h = H(domain, payload)
                    if h in named:
                        found.append((h, domain, payload, digest))
        found_hex = sorted({h for h, _, _, _ in found})
        if found_hex != sorted(set(named)):
            L.refuse(
                "NATIVE_CONTEXT_SET",
                "retained context frames != plan.nativeContextDigests",
                retained=found_hex,
                plan=sorted(set(named)),
            )
        for h, domain, payload, digest in found:
            defn = NATIVE_CONTEXT_DEFS.get(domain)
            if not defn:
                L.refuse("NATIVE_CONTEXT_DEF", domain)
                continue
            self._validate_native_def(L, defn, payload, domain)
            row = ctx_set[domain]
            self._apply_closure_joins(L, payload, row.get("closureJoins") or [], loc=domain)
            self._apply_snapshot_joins(L, payload, row.get("snapshotJoins") or [], loc=domain)
            self._apply_nested_records(L, payload, row.get("nestedRecords") or [], loc=domain)
            # language-specific extra agreements
            if domain == "native.context.typescript.v2":
                self._admit_ts_context(L, payload)
            elif domain == "native.context.rust.v2":
                self._admit_rust_context(L, payload)
            elif domain == "native.context.syntax.v2":
                self._admit_syntax_context(L, payload)

        # universes
        for domain, items in list(self.by_domain.items()):
            if domain not in uni_set:
                continue
            row = uni_set[domain]
            for digest, payload in items:
                defn = NATIVE_UNIVERSE_DEFS.get(domain)
                if defn:
                    self._validate_native_def(L, defn, payload, domain)
                ident = H(domain, payload)
                # nativeContextId must be sha256: + plan member
                ncid = payload.get("nativeContextId")
                if not ncid:
                    L.refuse("UNIVERSE_NO_CONTEXT", domain)
                    continue
                try:
                    hexd = sha256_text_to_hex(ncid)
                except LexicalRefusal as e:
                    L.refuse("UNIVERSE_CONTEXT_SPELLING", str(e))
                    continue
                if hexd not in named:
                    L.refuse("UNIVERSE_CONTEXT_NOT_PLAN_SELECTED", hexd, domain=domain)
                ctx_domain = row.get("contextDomain")
                # find matching context payload
                ctx_payload = None
                for h, d, p, _ in found:
                    if h == hexd:
                        ctx_payload = p
                        if d != ctx_domain:
                            L.refuse("UNIVERSE_CONTEXT_LANGUAGE_MISMATCH", f"universe {domain} bound {d}")
                        break
                if ctx_payload is None:
                    L.refuse("UNIVERSE_CONTEXT_BYTES_MISSING", hexd)
                else:
                    if H(ctx_domain, ctx_payload) != hexd:
                        L.refuse("UNIVERSE_CONTEXT_BINDING_MISMATCH", "context-bytes-are-not-the-admitted-ones")
                    if domain == "native.semantic-universe.typescript.v2":
                        self._bind_ts_universe(L, payload, ctx_payload)
                    elif domain == "native.semantic-universe.rust.v2":
                        self._bind_rust_universe(L, payload, ctx_payload)
                    elif domain == "native.semantic-universe.syntax.v2":
                        self._bind_syntax_universe(L, payload, ctx_payload)
                self._apply_nested_records(L, payload, row.get("nestedRecords") or [], loc=domain)
                self._apply_snapshot_joins(L, payload, row.get("snapshotJoins") or [], loc=domain)
                L.operands.setdefault("universes", []).append({"domain": domain, "h": ident, "nativeContextId": ncid})

        # nested identity frames
        for domain, items in self.by_domain.items():
            if domain in nested_set:
                defn = NATIVE_NESTED_DEFS.get(domain)
                for digest, payload in items:
                    if defn:
                        self._validate_native_def(L, defn, payload, domain)
                    recomputed = H(domain, payload)
                    if recomputed != digest and sha256(self.store.blobs[digest]) != digest:
                        L.refuse("NESTED_H", domain, digest=digest)
                    row = nested_set[domain]
                    self._apply_snapshot_joins(L, payload, row.get("snapshotJoins") or [], loc=domain)
                    self._apply_blob_joins(L, payload, row.get("blobJoins") or [], loc=domain)

    def _apply_closure_joins(self, L, payload, joins, loc):
        for j in joins:
            path = j.get("path") or []
            val = _get_path(payload, path)
            form = j.get("form")
            kind = j.get("kind")
            if val is None:
                L.refuse("CLOSURE_JOIN_MISSING", f"{loc}.{'.'.join(path)}")
                continue
            cid = val
            if form == "closure2-suffix":
                cid = "closure2:" + val
            if cid not in self.by_typed:
                L.refuse("CLOSURE_JOIN_UNRETAINED", cid, loc=loc, kind=kind)
                continue
            rec = self.by_typed[cid]
            if rec.get("domain") != "closure":
                L.refuse("CLOSURE_JOIN_DOMAIN", cid)
                continue
            if kind and rec["payload"].get("kind") != kind:
                L.refuse("CLOSURE_JOIN_KIND", f"{cid} kind {rec['payload'].get('kind')} want {kind}")
            ident = typed_id("closure", rec["payload"])
            if ident != cid:
                L.refuse("CLOSURE_JOIN_IDENTITY", ident)

    def _apply_snapshot_joins(self, L, payload, joins, loc):
        for j in joins:
            form = j.get("form")
            path = j.get("path") or []
            val = _get_path(payload, path) if path else payload
            if form == "inventoried-paths":
                path_field = j.get("pathField") or "path"
                paths = val if isinstance(val, list) else []
                for p in paths:
                    if isinstance(p, dict):
                        p = p.get(path_field)
                    if p not in self.snapshot_paths:
                        L.refuse("SNAPSHOT_JOIN_PATH", str(p), loc=loc, pathField=path_field)
            elif form == "inventoried-path-and-digest":
                if val is None and j.get("nullable"):
                    continue
                if not isinstance(val, dict):
                    L.refuse("SNAPSHOT_JOIN_LOCKFILE_SHAPE", loc)
                    continue
                p = val.get(j.get("pathField") or "path")
                d = val.get(j.get("digestField") or "contentSha256")
                row = self.snapshot_paths.get(p)
                if row is None:
                    L.refuse("SNAPSHOT_JOIN_LOCKFILE_PATH", p, loc=loc)
                else:
                    rd = row.get("digest") or row.get("contentSha256") or row.get("sha256")
                    if d and rd and d != rd:
                        L.refuse("SNAPSHOT_JOIN_LOCKFILE_DIGEST", p, claimed=d, inventory=rd)

    def _apply_nested_records(self, L, payload, specs, loc):
        for spec in specs:
            path = spec.get("path") or []
            digest = _get_path(payload, path)
            if digest is None and spec.get("nullable"):
                continue
            if not digest:
                L.refuse("NESTED_RECORD_MISSING", f"{loc}.{'.'.join(path)}")
                continue
            hexd = digest
            if isinstance(digest, str) and digest.startswith("sha256:"):
                try:
                    hexd = sha256_text_to_hex(digest)
                except LexicalRefusal as e:
                    L.refuse("NESTED_RECORD_SPELLING", str(e))
                    continue
            raw = self.store.blob(hexd)
            if raw is None:
                L.refuse("NESTED_RECORD_UNRETAINED", hexd, loc=loc)
                continue
            dec = self.records.get(hexd) or decode_record(raw)
            obj = dec.get("payload")
            if obj is None:
                # maybe H frame of nested domain
                if dec.get("form") == "h-identity":
                    obj = dec.get("payload")
                else:
                    L.refuse("NESTED_RECORD_PARSE", hexd, loc=loc)
                    continue
            self.canonical_by_digest[hexd] = obj
            sel = spec.get("selector")
            if sel and spec.get("document"):
                doc = spec["document"]
                if "native-evidence" in doc:
                    def_name = sel.split("/")[-1]
                    self._validate_native_def(L, def_name, obj, f"{loc}.{'.'.join(path)}")
            for bj in spec.get("blobJoins") or []:
                self._apply_blob_joins(L, obj, [bj], loc=f"{loc}.nested")

    def _apply_blob_joins(self, L, payload, joins, loc):
        for j in joins:
            path = j.get("path") or []
            digest_field = j.get("digestField")
            length_field = j.get("lengthField")
            target = payload
            # path may include []
            seq = [payload]
            for part in path:
                nxt = []
                for cur in seq:
                    if part == "[]":
                        if isinstance(cur, list):
                            nxt.extend(cur)
                    else:
                        if isinstance(cur, dict) and part in cur:
                            nxt.append(cur[part])
                seq = nxt
            if not path:
                seq = [payload]
            for item in seq:
                if not isinstance(item, dict):
                    continue
                d = item.get(digest_field) if digest_field else None
                if not d:
                    continue
                blob = self.store.blob(d)
                if blob is None:
                    L.refuse("BLOB_JOIN_MISSING", d, loc=loc)
                    continue
                if length_field and item.get(length_field) is not None and len(blob) != item[length_field]:
                    L.refuse("BLOB_JOIN_LENGTH", d, declared=item[length_field], actual=len(blob))

    def _admit_ts_context(self, L, ctx):
        hon = ((ctx.get("configProjection") or {}).get("honoredOptions")) or {}
        if ctx.get("moduleResolutionMode") != hon.get("moduleResolution"):
            L.refuse(
                "TS_MODULE_RESOLUTION_MISMATCH",
                f"context {ctx.get('moduleResolutionMode')} honored {hon.get('moduleResolution')}",
            )
        libs = (ctx.get("toolchain") or {}).get("libSelection") or []
        honored_lib = hon.get("lib") or []
        if sorted(libs) != sorted(honored_lib):
            L.refuse("TS_LIB_SELECTION", f"{libs} vs {honored_lib}")
        if libs != sorted(libs):
            L.refuse("TS_LIB_NOT_SORTED", libs)

    def _admit_rust_context(self, L, ctx):
        for field in ("dependencySourceSetId", "unifiedFeaturesId"):
            val = ctx.get(field)
            if val:
                try:
                    hexd = sha256_text_to_hex(val) if str(val).startswith("sha256:") else val
                except LexicalRefusal as e:
                    L.refuse("RUST_NESTED_ID", str(e), field=field)
                    continue
                if hexd not in self.store.blobs and f"native.dependency-source-set.v1" not in str(self.by_domain.keys()):
                    if hexd not in self.store.blobs:
                        L.refuse("RUST_NESTED_UNRETAINED", field, digest=hexd)

    def _admit_syntax_context(self, L, ctx):
        gb = ctx.get("grammarBundle") or {}
        cid = gb.get("closureId")
        if cid:
            rec = self.by_typed.get(cid)
            if not rec:
                L.refuse("GRAMMAR_CLOSURE_MISSING", cid)
            elif rec["payload"].get("kind") != "grammar":
                L.refuse("GRAMMAR_CLOSURE_KIND", rec["payload"].get("kind"))
        for g in gb.get("grammars") or []:
            lang = g.get("languageId")
            sclass = g.get("syntaxClass")
            row = self.owners.grammar_for_language(lang) if lang else None
            if row:
                if sclass and sclass != row.get("syntaxClass"):
                    L.refuse("GRAMMAR_CLASS_DRIFT", f"{lang} declared {sclass} registry {row.get('syntaxClass')}")
            L.operands.setdefault("grammars", []).append({"languageId": lang, "syntaxClass": sclass, "suffixes": g.get("suffixes")})

    def _bind_ts_universe(self, L, uni, ctx):
        checks = [
            ("languageMode", uni.get("languageMode"), ctx.get("languageMode")),
            ("packageModuleType", uni.get("packageModuleType"), ctx.get("packageModuleType")),
        ]
        for name, a, b in checks:
            if a != b:
                L.refuse("native.universe-context-field-mismatch:" + name, f"{a} vs {b}")
        hon = ((ctx.get("configProjection") or {}).get("honoredOptions")) or {}
        if uni.get("allowJs") != hon.get("allowJs"):
            L.refuse("native.universe-context-field-mismatch:allowJs", f"{uni.get('allowJs')} vs {hon.get('allowJs')}")
        if uni.get("checkJs") != hon.get("checkJs"):
            L.refuse("native.universe-context-field-mismatch:checkJs", f"{uni.get('checkJs')} vs {hon.get('checkJs')}")
        lf = ctx.get("lockfileIdentity") or {}
        if uni.get("lockfileKind") != lf.get("kind"):
            L.refuse("native.universe-context-field-mismatch:lockfileKind", f"{uni.get('lockfileKind')} vs {lf.get('kind')}")

    def _bind_rust_universe(self, L, uni, ctx):
        for field in ("dependencySourceSetId", "unifiedFeaturesId", "preparedOutputSetId"):
            if uni.get(field) != ctx.get(field):
                L.refuse("RUST_UNIVERSE_FIELD", field, universe=uni.get(field), context=ctx.get(field))
        for p in uni.get("crateRootPaths") or []:
            if p not in self.snapshot_paths:
                L.refuse("RUST_CRATE_ROOT_NOT_INVENTORIED", p)
        lf = uni.get("lockfileIdentity") or {}
        p = lf.get("path")
        if p and p not in self.snapshot_paths:
            L.refuse("RUST_LOCKFILE_NOT_INVENTORIED", p)
        elif p:
            row = self.snapshot_paths[p]
            rd = row.get("digest") or row.get("contentSha256")
            if lf.get("contentSha256") and rd and lf["contentSha256"] != rd:
                L.refuse("RUST_LOCKFILE_DIGEST", p)

    def _bind_syntax_universe(self, L, uni, ctx):
        selected = set(uni.get("selectedGrammarIds") or [])
        available = {g.get("grammarId") for g in ((ctx.get("grammarBundle") or {}).get("grammars") or [])}
        extra = selected - available
        if extra:
            L.refuse("SYNTAX_UNIVERSE_GRAMMAR", f"selected {sorted(extra)} not in context bundle")

    def _join_facts_coverage_view(self, L, evidence, plan):
        owners = self.owners
        view_ids = evidence.get("viewIds") or []
        cov_ids = evidence.get("coverageIds") or []
        if len(view_ids) < 1:
            L.refuse("NO_VIEW", "evidence.viewIds empty")
            return
        all_view_facts = []
        all_view_cov = []
        for vid in view_ids:
            rec = self.by_typed.get(vid)
            if not rec:
                L.refuse("VIEW_MISSING", vid)
                continue
            view = rec["payload"]
            self._validate_identity_def(L, "view", view, vid)
            if typed_id("view", view) != vid:
                L.refuse("VIEW_IDENTITY", vid)
            if view.get("planId") != plan and view.get("planId") != (self.claimed_run or {}).get("planId"):
                if view.get("planId") != (self.claimed_run or {}).get("planId"):
                    L.refuse("VIEW_PLAN", view.get("planId"))
            prod = view.get("producerClosure")
            kinds = (L.operands.get("closureKinds") or {})
            if prod and kinds.get(prod) not in (None, "provider"):
                if prod not in kinds:
                    L.refuse("VIEW_PRODUCER_UNSELECTED", prod)
                elif kinds[prod] != "provider":
                    L.refuse("VIEW_PRODUCER_KIND", kinds[prod])
            for fid in view.get("facts") or []:
                all_view_facts.append(fid)
                self._admit_fact(L, fid, plan)
            for cid in view.get("coverageIds") or []:
                all_view_cov.append(cid)
                self._admit_coverage(L, cid)
            for sid in view.get("scopeIds") or []:
                self._admit_scope(L, sid, plan)
        # evidence coverage set = union of views plus explicit
        extra_cov = set(cov_ids) - set(all_view_cov)
        if extra_cov:
            L.refuse("EVIDENCE_COVERAGE_NOT_IN_VIEW", sorted(extra_cov))
        L.operands["factIds"] = all_view_facts
        L.operands["coverageIds"] = all_view_cov
        L.operands["viewIds"] = view_ids

    def _admit_fact(self, L, fid, plan):
        rec = self.by_typed.get(fid)
        if not rec:
            L.refuse("FACT_MISSING", fid)
            return
        fact = rec["payload"]
        self._validate_identity_def(L, "fact", fact, fid)
        if typed_id("fact", fact) != fid:
            L.refuse("FACT_IDENTITY", fid)
        rel = fact.get("relation")
        rung = fact.get("resolution")
        row = self.owners.relation_registry.get(rel)
        if not row:
            L.refuse("FACT_RELATION_UNREGISTERED", rel, fact=fid)
            return
        ladder = row.get("ladder") or []
        if rung not in ladder:
            L.refuse("FACT_RUNG_NOT_ON_LADDER", f"{rel}@{rung} ladder={ladder}", fact=fid)
        rungs = row.get("rungs") or {}
        rule = rungs.get(rung) or {}
        payload = self._load_fact_payload(L, fact)
        if payload is None:
            return
        for req in rule.get("required") or []:
            if payload.get(req) in (None,):
                L.refuse("FACT_RUNG_REQUIRED_FIELD", req, relation=rel, rung=rung)
        for forb in rule.get("forbidden") or []:
            if payload.get(forb) not in (None,):
                L.refuse("FACT_RUNG_FORBIDDEN_FIELD", forb, relation=rel, rung=rung)
        # universe rule
        if row.get("universeRule") == "same-only":
            if fact.get("sourceUniverse") != fact.get("targetUniverse"):
                L.refuse("FACT_UNIVERSE_SAME_ONLY", fid)
        # schema digest of relation document
        rel_sha = self.owners.file_sha["docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"]
        if fact.get("payloadSchemaDigest") != rel_sha:
            L.refuse("FACT_PAYLOAD_SCHEMA_DIGEST", fact.get("payloadSchemaDigest"), want=rel_sha)
        # anchors
        self._anchor_law(L, fact, row, payload)
        for sj in row.get("snapshotJoins") or []:
            self._fact_snapshot_join(L, fact, payload, sj)
        if rel == "clones":
            self._clones_body_identity(L, fact, payload, row)
        # producer kind
        pc = fact.get("producerClosure")
        kinds = L.operands.get("closureKinds") or {}
        if pc in kinds and kinds[pc] != "provider":
            L.refuse("FACT_PRODUCER_NOT_PROVIDER", pc)

    def _load_fact_payload(self, L, fact):
        d = fact.get("payloadDigest")
        raw = self.store.blob(d)
        if raw is None:
            L.refuse("FACT_PAYLOAD_MISSING", d)
            return None
        dec = self.records.get(d) or decode_record(raw)
        payload = dec.get("payload")
        if payload is None:
            L.refuse("FACT_PAYLOAD_PARSE", d)
            return None
        if encode_c(payload) != raw:
            L.refuse("FACT_PAYLOAD_NOT_C", d)
        self.canonical_by_digest[d] = payload
        return payload

    def _anchor_law(self, L, fact, row, payload):
        law = row.get("anchorLaw") or {}
        anchors = fact.get("anchors") or []
        cls = law.get("class")
        if "cardinality" in law:
            if len(anchors) != law["cardinality"]:
                L.refuse("ANCHOR_CARDINALITY", f"{fact.get('relation')} want {law['cardinality']} got {len(anchors)}")
        if law.get("minimum") is not None and len(anchors) < law["minimum"]:
            L.refuse("ANCHOR_MINIMUM", f"{fact.get('relation')} want>={law['minimum']} got {len(anchors)}")
        if cls == "source-text":
            for a in anchors:
                if not isinstance(a, dict):
                    continue
                p = a.get("path")
                if p not in self.snapshot_paths:
                    L.refuse("ANCHOR_PATH_NOT_INVENTORIED", p)
                else:
                    blob = self._blob_for_path(p)
                    start = a.get("start") if "start" in a else a.get("startOffset")
                    end = a.get("end") if "end" in a else a.get("endOffset")
                    if blob is not None and start is not None and end is not None:
                        if not (0 <= start <= end <= len(blob)):
                            L.refuse("ANCHOR_SPAN", p, start=start, end=end, len=len(blob))

    def _blob_for_path(self, path: str) -> bytes | None:
        row = self.snapshot_paths.get(path)
        if not row:
            return None
        d = row.get("digest") or row.get("contentSha256") or row.get("sha256")
        return self.store.blob(d) if d else None

    def _fact_snapshot_join(self, L, fact, payload, sj):
        form = sj.get("form")
        if form == "inventoried-file":
            p = payload.get(sj.get("pathField") or "path")
            d = payload.get(sj.get("digestField") or "contentSha256")
            ln = payload.get(sj.get("lengthField") or "byteLength")
            row = self.snapshot_paths.get(p)
            if row is None:
                L.refuse("FILE_SNAPSHOT_PATH", p)
                return
            rd = row.get("digest") or row.get("contentSha256") or row.get("sha256")
            rl = row.get("byteLength") or row.get("length") or row.get("size")
            if d != rd:
                L.refuse("FILE_SNAPSHOT_DIGEST", p, payload=d, inventory=rd)
            if ln is not None and rl is not None and ln != rl:
                L.refuse("FILE_SNAPSHOT_LENGTH", p, payload=ln, inventory=rl)
            blob = self.store.blob(d)
            if blob is None:
                L.refuse("FILE_SNAPSHOT_BLOB", p, digest=d)
            elif ln is not None and len(blob) != ln:
                L.refuse("FILE_SNAPSHOT_BLOB_LEN", p)
            # anchorPathField: every anchor in the same file
            apf = sj.get("anchorPathField")
            if apf:
                for a in fact.get("anchors") or []:
                    if isinstance(a, dict) and a.get(apf) != p:
                        L.refuse("FILE_ANCHOR_PATH", f"anchor {a.get(apf)} payload {p}")
        elif form == "inventoried-path":
            p = payload.get(sj.get("pathField"))
            unless = sj.get("unless")
            if unless and payload.get(unless.get("field")) == unless.get("equals"):
                return
            if p and p not in self.snapshot_paths:
                L.refuse("INVENTORIED_PATH", p, relation=fact.get("relation"))

    def _clones_body_identity(self, L, fact, payload, row):
        join = row.get("bodyIdentityJoin") or {}
        level = payload.get(join.get("levelField") or "normalisationLevel")
        claimed = payload.get("bodyIdentity")
        anchors = fact.get("anchors") or []
        if len(anchors) != 1:
            L.refuse("CLONES_ANCHOR_CARDINALITY", len(anchors))
            return
        a = anchors[0]
        path = a.get("path")
        blob = self._blob_for_path(path)
        if blob is None:
            L.refuse("CLONES_BODY_BLOB", path)
            return
        start = a.get("start") if "start" in a else a.get("startOffset", 0)
        end = a.get("end") if "end" in a else a.get("endOffset", len(blob))
        if start is None:
            start = 0
        if end is None:
            end = len(blob)
        body = blob[start:end]
        nv = payload.get(join.get("levelVersionField") or "normalisationVersion")
        nv_raw = self.store.blob(nv)
        if nv_raw is None:
            L.refuse("CLONES_LEVEL_SPEC_MISSING", nv)
            return
        if len(nv_raw) != 32 and hashlib.sha256(nv_raw).digest() or True:
            level_version_raw32 = hashlib.sha256(nv_raw).digest()
            # law: normalisationVersion names the retained level specification bytes;
            # languageVersion is raw 32 bytes of SHA-256(C(body-language-version))
        # find body-language-version records
        lang_id = self._body_language_id(L, fact, path)
        blv = self._derive_body_language_version(L, fact, lang_id, path)
        if blv is None:
            L.note(f"body-language-version derivation incomplete for {path}")
            L.operands.setdefault("cloneBodyUnchecked", []).append(path)
            return
        lang_ver = hashlib.sha256(encode_c(blv)).digest()
        if level != "L0-verbatim":
            L.note(f"clone level {level} is not L0; L1-L3 tokenisation not recomputed (custody only)")
            if claimed and not str(claimed).startswith("sha256:"):
                L.refuse("CLONE_IDENTITY_SPELLING", claimed)
            return
        try:
            recomputed = clone_l0_body_identity(
                body_span=body,
                level_id=level,
                level_version_raw32=level_version_raw32,
                language_id=lang_id,
                language_version_raw32=lang_ver,
            )
        except LexicalRefusal as e:
            L.refuse("CLONE_L0_FRAME", str(e), path=path)
            return
        if claimed != recomputed:
            L.refuse("CLONE_L0_IDENTITY", f"path={path} claimed={claimed} recomputed={recomputed}")
        L.operands.setdefault("cloneL0", []).append({"path": path, "bodyIdentity": recomputed, "languageId": lang_id})

    def _body_language_id(self, L, fact, path: str) -> str:
        # dialect form closed-suffix-table from universe domain row
        uni_hex = fact.get("sourceUniverse")
        uni_domain, uni_payload = self._universe_by_hex(uni_hex)
        if not uni_domain:
            return self.owners.suffix_language(path) if hasattr(self.owners, "suffix_language") else "unspecified"
        row = self.owners.digest_domains["domainSets"]["native-semantic-universe"].get(uni_domain) or {}
        lvb = row.get("languageVersionBinding") or {}
        dialect = lvb.get("dialect") or {}
        if dialect.get("form") == "closed-suffix-table":
            table = dialect.get("table") or {}
            name = path.rsplit("/", 1)[-1]
            best = ""
            variant = None
            for suf, var in table.items():
                if name.endswith(suf) and len(suf) > len(best):
                    best = suf
                    variant = var
            blmap = lvb.get("bodyLanguageByVariant") or dialect.get("bodyLanguageByVariant") or {}
            if variant and variant in blmap:
                return blmap[variant]
            if variant in ("typescript", "javascript", "rust"):
                return variant
        # rust edition dialect
        if uni_domain == "native.semantic-universe.rust.v2":
            return "rust"
        if uni_domain == "native.semantic-universe.syntax.v2":
            # body language from grammar suffix; json is NOT in languageId enum
            lang = self.owners.suffix_language(path)
            return lang
        lang = self.owners.suffix_language(path)
        if lang == "json":
            return lang
        return lang

    def _universe_by_hex(self, hex_or_id: str | None) -> tuple[str | None, Any]:
        if not hex_or_id:
            return None, None
        h = hex_or_id
        if h.startswith("sha256:"):
            h = h[7:]
        for domain, items in self.by_domain.items():
            if domain.startswith("native.semantic-universe"):
                for digest, payload in items:
                    if H(domain, payload) == h or digest == h:
                        return domain, payload
        return None, None

    def _derive_body_language_version(self, L, fact, lang_id: str, path: str) -> dict[str, Any] | None:
        uni_domain, uni = self._universe_by_hex(fact.get("sourceUniverse"))
        if not uni:
            return None
        ncid = uni.get("nativeContextId")
        try:
            hexd = sha256_text_to_hex(ncid) if ncid else None
        except LexicalRefusal:
            return None
        ctx = None
        ctx_domain = None
        for domain, items in self.by_domain.items():
            if domain.startswith("native.context"):
                for digest, payload in items:
                    if H(domain, payload) == hexd:
                        ctx = payload
                        ctx_domain = domain
                        break
        if not ctx:
            return None
        row = self.owners.digest_domains["domainSets"]["native-semantic-universe"].get(uni_domain) or {}
        binding = row.get("languageVersionBinding") or {}
        fields = binding.get("fields") or {}
        rec = {"schemaVersion": 1, "languageId": lang_id, "dialect": {}}
        # compiler fields from context
        toolchain = ctx.get("toolchain") or {}
        rec["compilerName"] = toolchain.get("compilerName") or ((ctx.get("grammarBundle") or {}).get("parserName"))
        rec["compilerVersion"] = toolchain.get("compilerVersion") or ((ctx.get("grammarBundle") or {}).get("parserVersion"))
        rec["compilerBuild"] = toolchain.get("compilerPackageDigest") or ((ctx.get("grammarBundle") or {}).get("bundleDigest"))
        dialect_spec = binding.get("dialect") or {}
        if dialect_spec.get("form") == "closed-suffix-table":
            table = dialect_spec.get("table") or {}
            name = path.rsplit("/", 1)[-1]
            best = ""
            variant = None
            for suf, var in table.items():
                if name.endswith(suf) and len(suf) > len(best):
                    best = suf
                    variant = var
            rec["dialect"] = {"sourceVariant": variant} if variant else {}
            # keep only if schema allows
        if uni_domain == "native.semantic-universe.rust.v2":
            edition_map = uni.get("edition") or {}
            # body-specific edition from ownership
            rec["dialect"] = {"edition": self._rust_body_edition(uni, path)}
        if uni_domain == "native.semantic-universe.syntax.v2":
            rec["dialect"] = {"grammarId": ((uni.get("selectedGrammarIds") or ["?"])[0])}
        # Prefer retained blv records that match
        for d, obj in self.canonical_by_digest.items():
            if isinstance(obj, dict) and obj.get("languageId") == lang_id and obj.get("schemaVersion") == 1 and "compilerName" in obj:
                if obj.get("dialect") == rec.get("dialect") or lang_id != "rust":
                    if obj.get("compilerName") == rec.get("compilerName"):
                        return obj
        # validate derived against schema
        try:
            sch = schema_for_identity_def(self.owners, "body-language-version")
            faults = validate_against(rec, sch, self.registry)
            if faults:
                L.operands.setdefault("blvDeriveFaults", []).append({"path": path, "faults": faults[:5], "rec": rec})
                # use retained if any
                for obj in self.canonical_by_digest.values():
                    if isinstance(obj, dict) and obj.get("languageId") == lang_id and "dialect" in obj and "compilerName" in obj:
                        return obj
                return None
        except Exception:
            return rec
        return rec

    def _rust_body_edition(self, uni, path: str) -> int | None:
        own_id = uni.get("sourceUnitOwnershipId")
        if not own_id:
            return (uni.get("edition") or {}).get(list((uni.get("edition") or {}) or [None])[0]) if uni.get("edition") else None
        hexd = own_id[7:] if str(own_id).startswith("sha256:") else own_id
        # find ownership record
        own = None
        for domain, items in self.by_domain.items():
            if domain == "native.source-unit-ownership.v1":
                for digest, payload in items:
                    if H(domain, payload) == hexd or digest == hexd:
                        own = payload
        if own is None:
            own = self.canonical_by_digest.get(hexd)
        if not isinstance(own, dict):
            return None
        unit_id = None
        for row in own.get("ownership") or []:
            if row.get("path") == path:
                unit_id = row.get("unitId")
                break
        for u in own.get("units") or []:
            if unit_id and u.get("unitId") == unit_id:
                te = u.get("targetEdition")
                if te is not None:
                    return te
        # package default from universe edition map keyed by crate
        ed = uni.get("edition")
        if isinstance(ed, dict) and ed:
            return next(iter(ed.values())) if len(ed) == 1 else None
        if isinstance(ed, int):
            return ed
        return None

    def _admit_coverage(self, L, cid):
        rec = self.by_typed.get(cid)
        if not rec:
            L.refuse("COVERAGE_MISSING", cid)
            return
        cov = rec["payload"]
        self._validate_identity_def(L, "coverage", cov, cid)
        if typed_id("coverage", cov) != cid:
            L.refuse("COVERAGE_IDENTITY", cid)
        nat_sha = self.owners.file_sha["docs/coop/design-corrections/native/native-evidence.schemas.v2.json"]
        if cov.get("payloadSchemaDigest") != nat_sha:
            L.refuse("COVERAGE_PAYLOAD_SCHEMA", cov.get("payloadSchemaDigest"), want=nat_sha)
        pd = cov.get("payloadDigest")
        raw = self.store.blob(pd)
        if raw is None:
            L.refuse("COVERAGE_PAYLOAD_MISSING", pd)
            return
        dec = self.records.get(pd) or decode_record(raw)
        payload = dec.get("payload")
        if payload is None:
            L.refuse("COVERAGE_PAYLOAD_PARSE", pd)
            return
        self.canonical_by_digest[pd] = payload
        self._validate_native_def(L, "CoverageResultV3", payload, cid)
        entry = payload.get("entry") or {}
        key = payload.get("key") or {}
        # RC-6: coverage=complete REQUIRES examinedExhaustive=true
        rc = entry.get("resolutionCompleteness") or {}
        if entry.get("coverage") == "complete" and rc.get("examinedExhaustive") is not True:
            L.refuse("RC6_COMPLETE_WITHOUT_EXHAUSTIVE", cid)
        # deficiency pairing
        defic = entry.get("deficiency")
        cause = entry.get("nativeCause")
        if defic:
            row = self.owners.deficiency_cause.get(defic)
            if not row:
                L.refuse("DEFICIENCY_UNREGISTERED", defic, coverage=cid)
            else:
                nc_law = row.get("nativeCause")
                allowed = row.get("allowedCauses") or []
                if nc_law == "must-be-null" and cause is not None:
                    L.refuse("DEFICIENCY_CAUSE_MUST_BE_NULL", defic, nativeCause=cause)
                if nc_law == "required" and cause is None:
                    L.refuse("DEFICIENCY_CAUSE_REQUIRED", defic)
                if nc_law in ("required", "optional") and cause is not None and allowed and cause not in allowed:
                    L.refuse("DEFICIENCY_CAUSE_NOT_ALLOWED", f"{defic}+{cause} allowed={allowed}")
        elif cause is not None:
            # noDeficiencyNoCause
            L.refuse("CAUSE_WITHOUT_DEFICIENCY", cause, coverage=cid)
        # scope commitment join
        scope_id = cov.get("scopeId")
        commit = (entry.get("examinedUniverse") or {}).get("subjectScopeCommitment") or key.get("subjectScopeCommitment")
        if scope_id and commit:
            want = "sha256:" + scope_id.split(":", 1)[1]
            if commit != want:
                L.refuse("COVERAGE_SCOPE_COMMITMENT", f"{commit} vs {want}")
        L.operands.setdefault("coverageEntries", []).append(
            {
                "id": cid,
                "relation": entry.get("relation") or key.get("relation"),
                "resolution": entry.get("resolution") or key.get("resolution"),
                "coverage": entry.get("coverage"),
                "deficiency": defic,
                "nativeCause": cause,
                "subjectCount": (entry.get("examinedUniverse") or {}).get("subjectCount"),
                "examinedExhaustive": rc.get("examinedExhaustive"),
            }
        )

    def _admit_scope(self, L, sid, plan):
        rec = self.by_typed.get(sid)
        if not rec:
            L.refuse("SCOPE_MISSING", sid)
            return
        scope = rec["payload"]
        self._validate_identity_def(L, "subject-scope", scope, sid)
        if typed_id("subject-scope", scope) != sid:
            L.refuse("SCOPE_IDENTITY", sid)
        if scope.get("snapshotId") != (self.claimed_run or {}).get("snapshotId"):
            L.refuse("SCOPE_SNAPSHOT", sid)
        enumc = scope.get("enumeratorClosure")
        kinds = L.operands.get("closureKinds") or {}
        if enumc in kinds and kinds[enumc] != "provider":
            L.refuse("SCOPE_ENUMERATOR_KIND", kinds.get(enumc))
        rel = scope.get("relation")
        rung = scope.get("resolution")
        row = self.owners.relation_registry.get(rel)
        if row and rung not in (row.get("ladder") or []):
            L.refuse("SCOPE_RUNG", f"{rel}@{rung}")
        L.operands.setdefault("scopes", []).append(
            {
                "id": sid,
                "relation": rel,
                "resolution": rung,
                "subjectCount": len(scope.get("subjects") or []),
                "subjects": scope.get("subjects"),
            }
        )

    def _join_import(self, L, plan, evidence):
        import_ids = plan.get("importIds") or []
        ev_imports = evidence.get("importIds") or []
        if sorted(import_ids) != sorted(ev_imports):
            # evidence may list the same set
            extra = set(ev_imports) - set(import_ids)
            if extra:
                L.refuse("UNSELECTED_EVALUATION_IMPORT", sorted(extra))
        L.operands["importIds"] = import_ids
        for iid in import_ids:
            rec = self.by_typed.get(iid)
            if not rec:
                L.refuse("IMPORT_MISSING", iid)
                continue
            imp = rec["payload"]
            self._validate_identity_def(L, "import", imp, iid)
            if typed_id("import", imp) != iid:
                L.refuse("IMPORT_IDENTITY", iid)
            kinds = L.operands.get("closureKinds") or {}
            pc = imp.get("producerClosure")
            ac = imp.get("adapterClosure")
            if pc in kinds and kinds[pc] != "provider":
                L.refuse("IMPORT_PRODUCER_KIND", kinds.get(pc))
            if ac in kinds and kinds[ac] != "adapter":
                L.refuse("IMPORT_ADAPTER_KIND", kinds.get(ac))
            for field in ("payloadDigest", "sourceCorrespondenceDigest", "buildDigest", "observationDigest", "scopeDigest"):
                d = imp.get(field)
                if d and d not in self.store.blobs:
                    L.refuse("IMPORT_PREIMAGE_MISSING", field, digest=d)
            # payload schema
            psd = imp.get("payloadSchemaDigest")
            want = self.owners.file_sha["docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json"]
            if psd and psd != want:
                L.note(f"import payloadSchemaDigest {psd} vs imported-evidence.schema.json {want}")
            L.operands.setdefault("imports", []).append({"id": iid, "kind": imp.get("kind"), "completeness": imp.get("completeness")})

    def _acyclic_check(self, L, run, evidence, seal, plan):
        if "runId" in evidence or "evaluationSealId" in evidence:
            L.refuse("ACYCLIC_EVIDENCE", "evidence names run/seal illegally")
        if "runId" in seal:
            L.refuse("ACYCLIC_SEAL", "seal names run")

    # ----- FULL SEMANTIC -----
    def layer_semantic(self) -> LayerResult:
        L = LayerResult("fullsemantic", "PASS")
        plan_id = self.claimed_run["planId"]
        plan = self.by_typed[plan_id]["payload"]
        proof = self.claimed_proof
        if proof is None:
            L.refuse("NO_CLAIMED_PROOF", "structural layer did not expose a proof")
            return L
        aspec = self.canonical_by_digest.get(plan["analysisSpecDigest"])
        policy = self.canonical_by_digest.get(plan["policyDigest"])
        enum_digest = (L.operands.get("enumerationPlanDigest") if False else None)
        enum_digest = None
        for p in (aspec or {}).get("parameters") or []:
            if p.get("schemaDigest") == self.owners.file_sha["docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"]:
                enum_digest = p.get("payloadDigest")
        enum_plan = self.canonical_by_digest.get(enum_digest) if enum_digest else None
        if enum_plan is None:
            L.refuse("ENUM_PLAN_NOT_BOUND", str(enum_digest))
            return L
        emission_digest = None
        for p in (aspec or {}).get("parameters") or []:
            if p.get("schemaDigest") == self.owners.file_sha["docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"]:
                emission_digest = p.get("payloadDigest")
        emission = self.canonical_by_digest.get(emission_digest) if emission_digest else None
        scope_doc = None
        for p in (aspec or {}).get("parameters") or []:
            if p.get("schemaDigest") == self.owners.file_sha["docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"]:
                scope_doc = self.canonical_by_digest.get(p.get("payloadDigest"))

        inventories = self._collect_inventories(L)
        L.operands["inventoryCount"] = len(inventories)
        self._check_enumeration_joins(L, plan, aspec, enum_plan, inventories)
        if L.first_refusal:
            return L

        ei_digest = proof.get("executionInputsDigest")
        ei = self.canonical_by_digest.get(ei_digest)
        if ei is None:
            L.refuse("EI_NOT_BOUND", ei_digest)
            return L
        self._check_execution_inputs(L, plan, enum_plan, ei, inventories)
        if L.first_refusal:
            return L

        # program
        rp_digest = proof.get("ruleProgramDigest")
        rp_raw = self.store.blob(rp_digest)
        if rp_raw is None:
            L.refuse("RULE_PROGRAM_MISSING", rp_digest)
            return L
        rp_dec = self.records.get(rp_digest) or decode_record(rp_raw)
        program = rp_dec.get("payload")
        if program is None:
            L.refuse("RULE_PROGRAM_PARSE", rp_digest)
            return L
        schema = dict(self.owners.policy_v2)
        schema["$ref"] = "#/$defs/RuleProgramV2"
        faults = validate_against(program, schema, self.registry)
        for f in faults:
            L.refuse("RULE_PROGRAM_SCHEMA", f)
        if program.get("policyDigest") != plan["policyDigest"]:
            L.refuse("RULE_PROGRAM_POLICY", "program.policyDigest != plan.policyDigest")

        # grammar / matrix for syntax clones
        self._matrix_and_grammar_accounts(L, enum_plan, ei)

        computed_proof = self._compose(L, plan, policy, program, emission, enum_plan, inventories, scope_doc, ei, proof)
        L.operands["computedProof"] = _proof_summary(computed_proof)
        L.operands["claimedProof"] = _proof_summary(proof)
        # compare complete proof fields (not counts-only)
        mismatches = _proof_compare(computed_proof, proof)
        L.operands["proofCompare"] = mismatches
        if mismatches:
            L.refuse("PROOF_MISMATCH", mismatches[0], all=mismatches[:20])
        if L.first_refusal:
            L.status = "REFUSED"
        return L

    def _collect_inventories(self, L) -> list[dict[str, Any]]:
        out = []
        for digest, obj in self.canonical_by_digest.items():
            if isinstance(obj, dict) and obj.get("schemaVersion") == 1 and "cellOrdinal" in obj and "rows" in obj and "kind" in obj and "planId" in obj:
                out.append({"digest": digest, **obj})
        out.sort(key=lambda r: (r.get("cellOrdinal", 0), r.get("programOrdinal", 0), r.get("kind") or ""))
        return out

    def _check_enumeration_joins(self, L, plan, aspec, enum_plan, inventories):
        if enum_plan.get("snapshotId") != plan.get("snapshotId"):
            L.refuse("ENUM_SNAPSHOT", "enumeration-plan.snapshotId != plan.snapshotId")
        if enum_plan.get("scopeDigest") != plan.get("scopeDigest"):
            L.refuse("ENUM_SCOPE", "enumeration-plan.scopeDigest != plan.scopeDigest")
        req = (aspec or {}).get("requestedCapabilities") or []
        cells = enum_plan.get("cells") or []
        if len(cells) != len(req):
            L.refuse("ENUM_CELL_COUNT", f"cells {len(cells)} requested {len(req)}")
        # sort law
        def tup(c):
            return (c.get("capabilityId"), c.get("languageMode"), c.get("workspaceRoot"))
        if [tup(c) for c in cells] != sorted([tup(c) for c in cells]):
            L.refuse("ENUM_CELL_ORDER", "cells not ordered by capabilityId,languageMode,workspaceRoot")
        req_t = sorted(tup(c) + (c.get("required"),) for c in req)
        cell_t = sorted(tup(c) + (c.get("required"),) for c in cells)
        if req_t != cell_t:
            L.refuse("ENUMERATION_PLAN_CELL_TUPLE_MISMATCH", f"{cell_t} vs {req_t}")
        expected = []
        for ci, cell in enumerate(cells):
            kinds = cell.get("kinds") or []
            if not kinds:
                continue  # candidate-only: zero inventories
            for pb in cell.get("programBindings") or []:
                po = pb.get("ordinal")
                for kind in kinds:
                    expected.append((ci, po, kind))
                if pb.get("enumerator", {}).get("status") == "selected":
                    cid = pb["enumerator"].get("closureId")
                    if cid not in (plan.get("semanticClosures") or []):
                        L.refuse("ENUM_CLOSURE", cid)
                    ncd = pb.get("nativeContextDigest")
                    if ncd not in (plan.get("nativeContextDigests") or []):
                        L.refuse("ENUM_CONTEXT_NOT_PLAN", ncd)
                    if pb.get("universe") is None:
                        L.refuse("ENUM_SELECTED_NULL_UNIVERSE", ci)
                if pb.get("provenance") == "default-unit" and pb.get("ordinal") != 0:
                    L.refuse("ENUM_DEFAULT_UNIT_ORDINAL", pb.get("ordinal"))
        have = {(i["cellOrdinal"], i["programOrdinal"], i["kind"]) for i in inventories}
        for exp in expected:
            if exp not in have:
                L.refuse("ENUMERATION_INVENTORY_MISSING_RECORD", f"cell={exp[0]} program={exp[1]} kind={exp[2]}")
        param_digest = None
        # inventory parameterDigest = C(enum_plan)
        want_param = sha256(encode_c(enum_plan))
        for inv in inventories:
            if inv.get("planId") != self.claimed_run["planId"]:
                L.refuse("INV_PLAN", inv.get("planId"))
            if inv.get("parameterDigest") != want_param:
                L.refuse("INV_PARAMETER_DIGEST", inv.get("parameterDigest"), want=want_param)
            # file totality
            cell = (enum_plan.get("cells") or [None])[inv["cellOrdinal"]] if inv["cellOrdinal"] < len(enum_plan.get("cells") or []) else None
            if cell:
                bindings = cell.get("programBindings") or []
                pb = next((b for b in bindings if b.get("ordinal") == inv["programOrdinal"]), None)
                if pb:
                    ext = None
                    for e in pb.get("extents") or []:
                        if e.get("kind") == inv["kind"]:
                            ext = set(e.get("paths") or [])
                    if inv["kind"] == "file" and inv.get("state") == "complete" and ext is not None:
                        paths = {r.get("path") for r in inv.get("rows") or []}
                        if paths != ext:
                            L.refuse("ENUMERATION_INVENTORY_FILE_TOTALITY", f"rows={sorted(paths)} extent={sorted(ext)}")
                    if inv.get("state") == "unavailable":
                        if inv.get("rows"):
                            L.refuse("INV_UNAVAILABLE_ROWS", inv["digest"])
                    if inv.get("state") == "partial" and not inv.get("deficiency"):
                        L.refuse("INV_PARTIAL_NO_DEFICIENCY", inv["digest"])
        L.operands["enumerationExpected"] = [list(x) for x in expected]
        L.operands["enumerationHave"] = [list(x) for x in sorted(have)]

    def _check_execution_inputs(self, L, plan, enum_plan, ei, inventories):
        if ei.get("planId") != self.claimed_run["planId"]:
            L.refuse("EI_PLAN", ei.get("planId"))
        if ei.get("evaluatorClosure") != self.claimed_proof.get("evaluatorClosure"):
            L.refuse("EI_EVALUATOR", ei.get("evaluatorClosure"))
        # selectedRefs must not include proof/finding/seal/run/evidence
        forbidden = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}
        for ref in ei.get("selectedRefs") or []:
            if ref.get("domain") in forbidden:
                L.refuse("EI_FORBIDDEN_REF", ref)
        # evaluationInputRefs = selectedRefs + execution-inputs
        claimed_refs = self.claimed_proof.get("evaluationInputRefs") or []
        ei_ref = {"domain": "execution-inputs", "digest": self.claimed_proof.get("executionInputsDigest")}
        selected = ei.get("selectedRefs") or []
        # compare as canonical sets
        def key(r):
            return (r.get("domain"), r.get("digest"))
        want = sorted([key(r) for r in selected] + [key(ei_ref)])
        have = sorted(key(r) for r in claimed_refs)
        if want != have:
            L.refuse("EVALUATION_INPUT_REFS", f"claimed {have} want selected+exec {want}")
        # cell outcomes derived
        cells = enum_plan.get("cells") or []
        outcomes = ei.get("cellOutcomes") or []
        L.operands["cellOutcomes"] = [
            {
                "capabilityId": o.get("capabilityId"),
                "state": o.get("state"),
                "deficiency": o.get("deficiency"),
                "nativeCause": o.get("nativeCause"),
                "required": o.get("required"),
            }
            for o in outcomes
        ]
        # required cell deficiencies
        for o in outcomes:
            if o.get("required") and o.get("state") != "complete":
                L.operands.setdefault("requiredIncompleteCells", []).append(
                    {"capabilityId": o.get("capabilityId"), "state": o.get("state"), "deficiency": o.get("deficiency"), "nativeCause": o.get("nativeCause")}
                )
            # pairing on outcome
            if o.get("deficiency"):
                row = self.owners.deficiency_cause.get(o["deficiency"])
                if row and row.get("nativeCause") == "required":
                    allowed = row.get("allowedCauses") or []
                    if o.get("nativeCause") not in allowed:
                        L.refuse("EI_OUTCOME_CAUSE_PAIR", f"{o.get('deficiency')}+{o.get('nativeCause')}")

    def _matrix_and_grammar_accounts(self, L, enum_plan, ei):
        for cell in enum_plan.get("cells") or []:
            mode = cell.get("languageMode")
            cap = cell.get("capabilityId")
            mcell = self.owners.matrix_cell(mode, cap)
            L.operands.setdefault("matrixCells", []).append(
                {
                    "mode": mode,
                    "capability": cap,
                    "matrix": None
                    if mcell is None
                    else {"state": mcell.get("state"), "deficiency": mcell.get("deficiency")},
                }
            )
            if mcell is None:
                L.refuse("MATRIX_CELL_MISSING", f"{mode}/{cap}")
                continue
            if mcell.get("state") == "NOT-SELECTED":
                L.refuse("NOT_SELECTED_CELL_MINTED", f"{mode}/{cap}")
        # syntax data-document clones
        grammars = []
        for domain, items in self.by_domain.items():
            if domain == "native.context.syntax.v2":
                for _, payload in items:
                    for g in ((payload.get("grammarBundle") or {}).get("grammars") or []):
                        grammars.append(g)
        L.operands["syntaxGrammars"] = grammars
        for g in grammars:
            lang = g.get("languageId")
            row = self.owners.grammar_for_language(lang) or {}
            caps = set(row.get("capabilities") or [])
            if "clones@normalized-body-hash" not in caps:
                # owed clones work must be unavailable, not complete-empty
                for cov in L.operands.get("coverageEntries") or []:
                    pass
                # check store coverage entries already collected in structural operands? use self
        cov_entries = []
        # pull from structural via self.canonical
        for digest, obj in self.canonical_by_digest.items():
            if isinstance(obj, dict) and obj.get("schemaVersion") == 3 and "entry" in obj and "key" in obj:
                e = obj["entry"]
                if e.get("relation") == "clones":
                    cov_entries.append(e)
        for e in cov_entries:
            for g in grammars:
                lang = g.get("languageId")
                row = self.owners.grammar_for_language(lang) or {}
                if row.get("syntaxClass") == "data-document":
                    if e.get("coverage") == "complete" and e.get("deficiency") is None:
                        L.refuse(
                            "DATA_GRAMMAR_COMPLETE_EMPTY_CLONES",
                            "data-document grammar must not conceal unsupported clones as complete-empty",
                        )
                    if e.get("deficiency") != "language-tier-unsupported":
                        L.refuse(
                            "DATA_GRAMMAR_CLONES_DEFICIENCY",
                            f"want language-tier-unsupported got {e.get('deficiency')}",
                        )
                    if e.get("nativeCause") != "capability-missing":
                        L.refuse(
                            "DATA_GRAMMAR_CLONES_CAUSE",
                            f"want capability-missing got {e.get('nativeCause')}",
                        )

        # rust partial: ownership enumeration partial must not claim complete clones
        for domain, items in self.by_domain.items():
            if domain == "native.source-unit-ownership.v1":
                for _, payload in items:
                    if payload.get("enumeration") == "partial":
                        for e in cov_entries:
                            if e.get("coverage") == "complete":
                                L.refuse(
                                    "PARTIAL_OWNERSHIP_COMPLETE_CLONES",
                                    "partial source-unit ownership cannot claim complete clones Coverage",
                                )
                            pair_ok = e.get("deficiency") == "input-closure-incomplete" and e.get("nativeCause") == "body-language-owner-unenumerated"
                            if e.get("relation") == "clones" and not pair_ok:
                                L.refuse(
                                    "PARTIAL_CLONES_PAIRING",
                                    f"got {e.get('deficiency')}+{e.get('nativeCause')}",
                                )

    def _compose(self, L, plan, policy, program, emission, enum_plan, inventories, scope_doc, ei, claimed_proof):
        universe_map = self.owners.policy_universe_map or POLICY_UNIVERSE_DEFAULT
        if isinstance(universe_map, dict) and "typescript" not in universe_map:
            # maybe nested
            universe_map = universe_map.get("map") or POLICY_UNIVERSE_DEFAULT
        rules = (policy or {}).get("rules") or []
        gate_at = (policy or {}).get("gateSeverityAtLeast") or "error"
        facts = []
        for key, rec in self.by_typed.items():
            if key.startswith("fact2:") and rec and rec.get("payload"):
                facts.append((key, rec["payload"], self.canonical_by_digest.get(rec["payload"].get("payloadDigest"))))
        coverages = []
        for key, rec in self.by_typed.items():
            if key.startswith("coverage2:") and rec and rec.get("payload"):
                pd = rec["payload"].get("payloadDigest")
                coverages.append((key, rec["payload"], self.canonical_by_digest.get(pd)))
        scopes = []
        for key, rec in self.by_typed.items():
            if key.startswith("scope2:") and rec and rec.get("payload"):
                scopes.append((key, rec["payload"]))
        imports = []
        for iid in plan.get("importIds") or []:
            rec = self.by_typed.get(iid)
            if rec:
                imports.append((iid, rec["payload"]))

        predicate_proofs = []
        findings = []
        rule_results = []
        exec_defs = self._execution_deficiencies(ei)

        for rule in rules:
            if not rule.get("enabled", True):
                rule_results.append(
                    {
                        "ruleId": rule["ruleId"],
                        "outcome": "disabled",
                        "findingIds": [],
                        "deficiencies": [],
                        "enumeration": {"state": "disabled", "selectedSubjectIds": [], "unresolvedSubjectIds": [], "relevantInventoryRefs": [], "incompleteInventoryRefs": []},
                    }
                )
                continue
            se = rule.get("subjectEnumeration") or {}
            token = se.get("universe")
            domain = universe_map.get(token)
            if domain is None:
                L.refuse("POLICY_UNIVERSE_TOKEN", str(token))
                continue
            kind = se.get("subjectKind")
            selected, unresolved, relevant, incomplete = self._enumerate_subjects(
                L, domain, kind, se, scope_doc, enum_plan, inventories
            )
            enum_rec = {
                "state": "complete" if not incomplete and not unresolved else "incomplete",
                "selectedSubjectIds": [s["subjectId"] for s in selected],
                "unresolvedSubjectIds": unresolved,
                "relevantInventoryRefs": relevant,
                "incompleteInventoryRefs": incomplete,
            }
            atom = rule.get("emitWhen") or {}
            # program-predicate identity from the admitted RuleProgramV2 node
            prog_rule = None
            for pr in (program or {}).get("rules") or []:
                if pr.get("ruleId") == rule["ruleId"]:
                    prog_rule = pr
                    break
            node = (prog_rule or {}).get("emitWhen") or atom
            node_digest = sha256(encode_c(node))
            program_predicate = {
                "nodeDigest": node_digest,
                "operation": node.get("op") or atom.get("op"),
                "predicateId": "p",
                "ruleId": rule["ruleId"],
                "ruleProgramDigest": claimed_proof.get("ruleProgramDigest"),
                "schemaVersion": 2,
            }
            program_predicate_digest = sha256(encode_c(program_predicate))
            rule_defs = []
            finding_ids = []
            outcomes_truth = []
            for subj in selected:
                value, witness, causes = self._eval_atom(L, atom, subj, facts, coverages, scopes, imports, enum_plan)
                outcomes_truth.append(value)
                witness_rec = {
                    "schemaVersion": 3,
                    "programPredicateDigest": program_predicate_digest,
                    "matchingFactIds": sorted(witness.get("matchingFactIds") or []),
                    "coverageIds": sorted(witness.get("coverageIds") or []),
                    "countLimit": atom.get("n") if atom.get("op") == "count-at-most" else None,
                    "childPredicateIds": [],
                    "matchingImportRows": [],
                    "uncertainFactIds": sorted(witness.get("uncertainFactIds") or []),
                    "uncertainImportRows": [],
                    "deficiencies": witness.get("deficiencies") or [],
                    "kind": "native-atom",
                }
                pred = {
                    "ruleId": rule["ruleId"],
                    "subjectId": subj["subjectId"],
                    "predicateId": "p",
                    "operation": atom.get("op"),
                    "value": _kleene_str(value),
                    "scopeIds": witness.get("scopeIds") or [],
                    "inputRefs": witness.get("inputRefs") or [],
                    "witnessDigest": sha256(encode_c(witness_rec)),
                    "programPredicateDigest": program_predicate_digest,
                    "matchingFactIds": witness_rec["matchingFactIds"],
                    "coverageIds": witness_rec["coverageIds"],
                }
                predicate_proofs.append(pred)
                # claimed witness comparison is later via proof fields
                emit = value is True
                if emit:
                    # finding would be emitted; we still compute identity if possible
                    findings.append({"ruleId": rule["ruleId"], "subjectId": subj["subjectId"]})
                rule_defs.extend(causes)
            # rule outcome
            sev = rule.get("severity") or "error"
            gating = bool(rule.get("gate")) and SEV_RANK.get(sev, 0) >= SEV_RANK.get(gate_at, 2)
            live_findings = [f for f in findings if f["ruleId"] == rule["ruleId"]]
            if gating and live_findings:
                outcome = "fail"
            elif gating and (incomplete or unresolved or any(t is None for t in outcomes_truth)):
                # indeterminate if blocking causes
                blocking = [c for c in rule_defs if c.get("source") in ("native", "enumeration") or c.get("gating")]
                if any(t is None for t in outcomes_truth) and blocking or incomplete or unresolved:
                    outcome = "indeterminate"
                else:
                    outcome = "pass"
            else:
                outcome = "pass"
            rule_results.append(
                {
                    "ruleId": rule["ruleId"],
                    "outcome": outcome,
                    "findingIds": finding_ids,
                    "deficiencies": rule_defs,
                    "enumeration": enum_rec,
                }
            )

        # verdict
        if any(r["outcome"] == "fail" for r in rule_results if r["outcome"] != "disabled"):
            verdict = "fail"
        elif any(r["outcome"] == "indeterminate" for r in rule_results) or exec_defs:
            verdict = "indeterminate"
        else:
            verdict = "pass"

        computed = {
            "schemaVersion": 3,
            "planId": self.claimed_run["planId"],
            "executionPlanId": claimed_proof.get("executionPlanId"),
            "evaluatorClosure": claimed_proof.get("evaluatorClosure"),
            "ruleProgramDigest": claimed_proof.get("ruleProgramDigest"),
            "evaluationInputRefs": claimed_proof.get("evaluationInputRefs"),
            "executionInputsDigest": claimed_proof.get("executionInputsDigest"),
            "predicateProofs": predicate_proofs,
            "findingIds": [],
            "verdict": verdict,
            "evaluationState": "evaluated",
            "ruleResults": rule_results,
            "waivedFindingIds": [],
            "executionDeficiencies": exec_defs,
        }
        L.operands["computedVerdict"] = verdict
        L.operands["computedPredicateProofs"] = predicate_proofs
        L.operands["computedRuleResults"] = [
            {"ruleId": r["ruleId"], "outcome": r["outcome"], "enumState": r["enumeration"]["state"], "selected": r["enumeration"]["selectedSubjectIds"]}
            for r in rule_results
        ]
        L.operands["computedExecutionDeficiencies"] = exec_defs
        return computed

    def _execution_deficiencies(self, ei) -> list[dict[str, Any]]:
        out = []
        seen = []
        for o in ei.get("cellOutcomes") or []:
            if not o.get("required"):
                continue
            if o.get("state") == "complete":
                continue
            rec = {
                "source": "native" if o.get("deficiency") in self.owners.evaluator_deficiencies.get("sources", {}).get("native", []) or True else "execution",
                "cause": o.get("deficiency") or "required-cell-unsatisfied",
                "nativeCause": o.get("nativeCause"),
                "evidenceKind": None,
                "universe": o.get("universe"),
                "predicateId": None,
                "subjectId": None,
                "inputRefs": [],
            }
            # required-cell-unsatisfied is execution source
            if rec["cause"] not in (self.owners.evaluator_deficiencies.get("sources") or {}).get("native", []):
                rec["source"] = "execution"
                if o.get("deficiency"):
                    rec["cause"] = o["deficiency"]
                    rec["source"] = "native" if o["deficiency"] in ((self.owners.evaluator_deficiencies.get("sources") or {}).get("native") or []) else "execution"
            out.append(rec)
        # also nativeCoverageAccounts
        for acc in ei.get("nativeCoverageAccounts") or []:
            if acc.get("required") and acc.get("accountState") not in ("complete", "inapplicable", "unsupported-typed"):
                # unsupported-typed of required still requiredCellDeficiencies
                pass
            if acc.get("applicability") == "unsupported-typed" and acc.get("required"):
                d = acc.get("deficiency") or "language-tier-unsupported"
                rec = {
                    "source": "native",
                    "cause": d,
                    "nativeCause": acc.get("nativeCause") or ((acc.get("nativeCauses") or [None])[0]),
                    "evidenceKind": None,
                    "universe": acc.get("universe"),
                    "predicateId": None,
                    "subjectId": None,
                    "inputRefs": [],
                }
                if rec not in out:
                    out.append(rec)
        return out

    def _enumerate_subjects(self, L, domain, kind, se, scope_doc, enum_plan, inventories):
        # covering programs
        covering = []
        for cell in enum_plan.get("cells") or []:
            mode = cell.get("languageMode")
            mapped = self.owners.language_modes.get(mode)
            want_lang = None
            for tok, dom in (self.owners.policy_universe_map or POLICY_UNIVERSE_DEFAULT).items():
                if dom == domain or (isinstance(dom, str) and dom == domain):
                    want_lang = {"typescript": "typescript", "rust": "rust", "syntax": "syntax"}.get(tok, tok)
            lang_of_mode = mapped
            if lang_of_mode in ("typescript", "rust", "syntax"):
                domain_of_mode = {
                    "typescript": "native.semantic-universe.typescript.v2",
                    "rust": "native.semantic-universe.rust.v2",
                    "syntax": "native.semantic-universe.syntax.v2",
                }[lang_of_mode]
            else:
                domain_of_mode = None
            if domain_of_mode != domain:
                continue
            kinds = cell.get("kinds") or []
            inv_kind = "symbol" if kind == "export" else kind
            if inv_kind not in kinds and kinds:
                continue
            covering.append(cell)
        selected = []
        unresolved = []
        relevant = []
        incomplete = []
        include = se.get("include") or []
        exclude = se.get("exclude") or []
        sd_inc = (scope_doc or {}).get("include") or []
        sd_exc = (scope_doc or {}).get("exclude") or []
        if not covering:
            incomplete.append({"reason": "no-covering-program"})
            L.operands.setdefault("noCoveringProgram", []).append({"domain": domain, "kind": kind})
            return selected, unresolved, relevant, incomplete
        seen = set()
        for inv in inventories:
            cell = (enum_plan.get("cells") or [None])[inv["cellOrdinal"]] if inv["cellOrdinal"] < len(enum_plan.get("cells") or []) else None
            if not cell:
                continue
            mode = cell.get("languageMode")
            lang_of_mode = self.owners.language_modes.get(mode)
            domain_of_mode = {
                "typescript": "native.semantic-universe.typescript.v2",
                "rust": "native.semantic-universe.rust.v2",
                "syntax": "native.semantic-universe.syntax.v2",
            }.get(lang_of_mode)
            if domain_of_mode != domain:
                continue
            inv_kind = inv.get("kind")
            want_kind = "symbol" if kind == "export" else kind
            if inv_kind != want_kind:
                continue
            relevant.append(inv["digest"])
            if inv.get("state") != "complete":
                incomplete.append(inv["digest"])
            pb = None
            for b in cell.get("programBindings") or []:
                if b.get("ordinal") == inv.get("programOrdinal"):
                    pb = b
                    break
            uni = pb.get("universe") if pb else None
            for row in inv.get("rows") or []:
                path = row.get("path")
                if kind == "export":
                    exp = row.get("exported")
                    if exp == "unknown":
                        unresolved.append(row.get("nativeSubjectId"))
                        continue
                    if exp != "exported":
                        continue
                if not _path_selected(path, include, exclude, sd_inc, sd_exc):
                    continue
                native = row.get("nativeSubjectId")
                subj_obj = {"schemaVersion": 3, "universe": uni, "kind": "symbol" if kind == "export" else kind, "nativeSubjectId": native}
                if (subj_obj["kind"] == "package"):
                    subj_obj["packageManifestPath"] = path
                sid = typed_id("evaluation-subject", subj_obj)
                key = (uni, subj_obj["kind"], native, subj_obj.get("packageManifestPath"))
                if key in seen:
                    continue
                seen.add(key)
                selected.append({"subjectId": sid, "descriptor": subj_obj, "path": path, "row": row, "universe": uni})
        return selected, unresolved, relevant, incomplete

    def _eval_atom(self, L, atom, subj, facts, coverages, scopes, imports, enum_plan):
        op = atom.get("op")
        relation = atom.get("relation")
        min_res = atom.get("minResolution")
        filters = atom.get("filters") or []
        endpoint = atom.get("endpoint") or "source"
        rel_row = self.owners.atom_relations.get(relation) or {}
        ladder = (self.owners.relation_registry.get(relation) or {}).get("ladder") or rel_row.get("ladder") or []
        try:
            min_idx = ladder.index(min_res)
        except ValueError:
            L.refuse("ATOM_RUNG", f"{relation}@{min_res} not on {ladder}")
            return None, {}, [{"cause": "selector-unbound"}]
        matching = []
        uncertain = []
        used_cov = []
        used_scopes = []
        native_id = subj["descriptor"]["nativeSubjectId"]
        uni = subj["universe"]
        kind = subj["descriptor"]["kind"]
        path = subj.get("path")
        # wrong kind
        src_kind = rel_row.get("sourceSubjectKind")
        if src_kind and kind != src_kind and not (src_kind == "file" and kind == "file"):
            # file relation sourceSubjectKind file; inventory kind file
            if kind != src_kind:
                return None, {"kind": "native-atom", "matchingFactIds": [], "coverageIds": [], "deficiencies": []}, [
                    {"cause": "ATOM_KIND_INCOMPATIBLE"}
                ]
        for fid, fact, payload in facts:
            if fact.get("relation") != relation:
                continue
            rung = fact.get("resolution")
            try:
                if ladder.index(rung) < min_idx:
                    continue
            except ValueError:
                continue
            if fact.get("sourceUniverse") != uni and rel_row.get("universeRule") == "same-only":
                # still allow cross-family match for positives; skip if universes differ for same-only
                if fact.get("sourceUniverse") != uni:
                    continue
            if not payload:
                continue
            if not _atom_occupancy(rel_row, endpoint, fact, payload, native_id, path, kind, subj):
                continue
            if not _atom_filters(rel_row, filters, fact, payload, native_id, path):
                continue
            matching.append(fid)
        # coverage at exact rung whose scope contains source subject
        for cid, cov, cp in coverages:
            if not cp:
                continue
            key = cp.get("key") or {}
            entry = cp.get("entry") or {}
            if (entry.get("relation") or key.get("relation")) != relation:
                continue
            if (entry.get("resolution") or key.get("resolution")) != min_res:
                continue
            if key.get("sourceUniverse") != uni:
                continue
            sid = cov.get("scopeId")
            scope = None
            for scid, sc in scopes:
                if scid == sid:
                    scope = sc
                    break
            if scope and _scope_contains(scope, native_id, path, kind):
                used_cov.append(cid)
                used_scopes.append(sid)
        # completeness for none/exists
        known = list(dict.fromkeys(matching))
        value: bool | None
        causes = []
        if op == "exists":
            value = True if known else _completeness_unknown_or_false(used_cov, coverages, False, causes)
            if not known and value is not True:
                # no match: if complete coverage then false else unknown
                value = _none_or_exists_without_hit(used_cov, coverages, want_exists=True, causes=causes)
        elif op == "none":
            if known:
                value = False
            else:
                value = _none_or_exists_without_hit(used_cov, coverages, want_exists=False, causes=causes)
        elif op == "count-at-most":
            n = atom.get("n") or 0
            if len(known) > n:
                value = False
            else:
                # need completeness to say true
                value = _none_or_exists_without_hit(used_cov, coverages, want_exists=False, causes=causes)
                if value is True:
                    value = len(known) <= n
        elif op == "all-covered":
            value = _all_covered(used_cov, coverages, causes)
        else:
            L.refuse("ATOM_OP", str(op))
            value = None
        witness = {
            "schemaVersion": 3,
            "programPredicateDigest": None,
            "matchingFactIds": sorted(known),
            "coverageIds": sorted(set(used_cov)),
            "countLimit": atom.get("n") if op == "count-at-most" else None,
            "childPredicateIds": [],
            "matchingImportRows": [],
            "uncertainFactIds": [],
            "uncertainImportRows": [],
            "deficiencies": causes,
            "kind": "native-atom",
            "scopeIds": sorted(set(used_scopes)),
            "inputRefs": sorted(set(used_cov + known)),
        }
        return value, witness, causes


def _path_selected(path, include, exclude, sd_inc, sd_exc) -> bool:
    def match_any(pats, p):
        if not pats:
            return True
        return any(glob_match(g, p) for g in pats)
    if include and not match_any(include, path):
        return False
    if exclude and match_any(exclude, path):
        return False
    if sd_inc and not match_any(sd_inc, path):
        return False
    if sd_exc and match_any(sd_exc, path):
        return False
    return True


def _atom_occupancy(rel_row, endpoint, fact, payload, native_id, path, kind, subj):
    if endpoint == "source":
        field = rel_row.get("sourceField")
        if field == "path" or field == "payload.path":
            return payload.get("path") == native_id or payload.get("path") == path
        if field == "packageName":
            return payload.get("packageName") == native_id and (
                not subj["descriptor"].get("packageManifestPath")
                or payload.get("manifestPath") == subj["descriptor"].get("packageManifestPath")
            )
        if field in ("declared", "payload.declared"):
            return payload.get("declared") == native_id
        if field in ("owner", "from", "importer", "referrer", "caller", "subject", "origin"):
            key = field.split(".")[-1]
            return payload.get(key) == native_id
        if field == "anchors[0].path" or field == "fact.anchors[0].path":
            anchors = fact.get("anchors") or []
            return bool(anchors) and anchors[0].get("path") in (path, native_id)
        # default file
        if rel_row.get("sourceSubjectKind") == "file":
            return payload.get("path") in (path, native_id) or (fact.get("anchors") or [{}])[0].get("path") in (path, native_id)
        return payload.get("path") in (path, native_id)
    return False


def _atom_filters(rel_row, filters, fact, payload, native_id, path) -> bool:
    for fl in filters:
        field = fl.get("field")
        cmpop = fl.get("cmp")
        val = fl.get("value")
        actual = None
        fmap = (rel_row.get("filters") or {})
        src = fmap.get(field)
        if src == "payload.path" or field == "subject":
            actual = payload.get("path") or native_id
            if field == "subject":
                actual = payload.get("path") or payload.get("packageName") or payload.get("declared") or native_id
        elif src == "fact.resolution" or field == "resolution":
            actual = fact.get("resolution")
        elif src == "fact.confidenceMillionths" or field == "confidenceMillionths":
            actual = fact.get("confidenceMillionths")
        else:
            if field in payload:
                actual = payload[field]
            elif field in fact:
                actual = fact[field]
        if cmpop == "eq":
            if actual != val:
                return False
        elif cmpop == "neq":
            if actual == val:
                return False
        elif cmpop == "in":
            if actual not in (val or []):
                return False
        else:
            return False
    return True


def _scope_contains(scope, native_id, path, kind) -> bool:
    subs = scope.get("subjects") or []
    return native_id in subs or path in subs


def _coverage_complete(used_cov, coverages) -> bool | None:
    if not used_cov:
        return None
    states = []
    for cid, cov, cp in coverages:
        if cid not in used_cov or not cp:
            continue
        states.append((cp.get("entry") or {}).get("coverage"))
    if any(s == "unknown" for s in states):
        return None
    if states and all(s == "complete" for s in states):
        return True
    return None


def _none_or_exists_without_hit(used_cov, coverages, want_exists: bool, causes) -> bool | None:
    st = _coverage_complete(used_cov, coverages)
    if st is True:
        return False if want_exists else True
    causes.append({"cause": "missing-relation-coverage" if not used_cov else "coverage-unknown", "source": "native"})
    return None


def _all_covered(used_cov, coverages, causes) -> bool | None:
    st = _coverage_complete(used_cov, coverages)
    if st is True:
        return True
    causes.append({"cause": "coverage-unknown" if used_cov else "missing-relation-coverage", "source": "native"})
    return None


def _kleene_str(v: bool | None) -> str:
    if v is True:
        return "true"
    if v is False:
        return "false"
    return "indeterminate"


def _get_path(obj, path):
    cur = obj
    for p in path:
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return None
    return cur


def _layer_dict(L: LayerResult) -> dict[str, Any]:
    return {
        "name": L.name,
        "status": L.status,
        "firstRefusal": L.first_refusal,
        "faultCount": len(L.faults),
        "faults": L.faults[:80],
        "notes": L.notes[:40],
        "operands": _jsonable(L.operands),
    }


def _jsonable(o):
    if isinstance(o, (str, int, float, bool)) or o is None:
        return o
    if isinstance(o, bytes):
        return {"bytes": len(o), "sha256": hashlib.sha256(o).hexdigest()}
    if isinstance(o, dict):
        return {str(k): _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_jsonable(v) for v in o]
    return str(o)


def _proof_summary(p):
    if not isinstance(p, dict):
        return p
    return {
        "verdict": p.get("verdict"),
        "evaluationState": p.get("evaluationState"),
        "findingIds": p.get("findingIds"),
        "waivedFindingIds": p.get("waivedFindingIds"),
        "executionDeficiencies": p.get("executionDeficiencies"),
        "predicateProofs": [
            {k: v for k, v in rec.items() if k != "inputRefs"} | {"inputRefsCount": len(rec.get("inputRefs") or [])}
            if isinstance(rec, dict)
            else rec
            for rec in (p.get("predicateProofs") or [])
        ],
        "ruleResults": [
            {
                "ruleId": r.get("ruleId"),
                "outcome": r.get("outcome"),
                "findingIds": r.get("findingIds"),
                "enumeration": {
                    "state": (r.get("enumeration") or {}).get("state"),
                    "selectedSubjectIds": (r.get("enumeration") or {}).get("selectedSubjectIds"),
                    "incompleteInventoryRefs": (r.get("enumeration") or {}).get("incompleteInventoryRefs"),
                },
            }
            for r in (p.get("ruleResults") or [])
            if isinstance(r, dict)
        ],
    }


def _proof_compare(computed, claimed) -> list[str]:
    mismatches = []
    for field in ("verdict", "evaluationState"):
        if computed.get(field) != claimed.get(field):
            mismatches.append(f"{field}: computed={computed.get(field)} claimed={claimed.get(field)}")
    # predicate proofs by (ruleId,subjectId,predicateId)
    def pkey(p):
        return (p.get("ruleId"), p.get("subjectId"), p.get("predicateId"))
    c_map = {pkey(p): p for p in computed.get("predicateProofs") or []}
    k_map = {pkey(p): p for p in claimed.get("predicateProofs") or []}
    if set(c_map) != set(k_map):
        mismatches.append(f"predicateProofKeys computed={sorted(c_map)} claimed={sorted(k_map)}")
    for k, cp in c_map.items():
        kp = k_map.get(k)
        if not kp:
            continue
        for f in ("operation", "value", "witnessDigest"):
            if cp.get(f) != kp.get(f):
                mismatches.append(f"predicate {k} {f}: computed={cp.get(f)} claimed={kp.get(f)}")
        if sorted(cp.get("scopeIds") or []) != sorted(kp.get("scopeIds") or []):
            mismatches.append(f"predicate {k} scopeIds")
        if sorted(cp.get("matchingFactIds") or []) != sorted(kp.get("matchingFactIds") or []) and "matchingFactIds" in kp:
            mismatches.append(f"predicate {k} matchingFactIds")
        if sorted(cp.get("coverageIds") or []) != sorted(kp.get("coverageIds") or []) and "coverageIds" in kp:
            mismatches.append(f"predicate {k} coverageIds")
    # rule outcomes
    cr = {r["ruleId"]: r for r in computed.get("ruleResults") or []}
    kr = {r.get("ruleId"): r for r in claimed.get("ruleResults") or []}
    if set(cr) != set(kr):
        mismatches.append(f"ruleIds computed={sorted(cr)} claimed={sorted(kr)}")
    for rid, r in cr.items():
        oth = kr.get(rid)
        if not oth:
            continue
        if r.get("outcome") != oth.get("outcome"):
            mismatches.append(f"rule {rid} outcome computed={r.get('outcome')} claimed={oth.get('outcome')}")
        csel = sorted((r.get("enumeration") or {}).get("selectedSubjectIds") or [])
        ksel = sorted((oth.get("enumeration") or {}).get("selectedSubjectIds") or [])
        if csel != ksel:
            mismatches.append(f"rule {rid} selectedSubjectIds computed={csel} claimed={ksel}")
    # execution deficiencies causes
    cc = sorted((d.get("cause"), d.get("nativeCause")) for d in computed.get("executionDeficiencies") or [])
    kc = sorted((d.get("cause"), d.get("nativeCause")) for d in claimed.get("executionDeficiencies") or [])
    if cc != kc:
        mismatches.append(f"executionDeficiencies computed={cc} claimed={kc}")
    cf = sorted(computed.get("findingIds") or [])
    kf = sorted(claimed.get("findingIds") or [])
    if cf != kf:
        mismatches.append(f"findingIds computed={cf} claimed={kf}")
    return mismatches
