"""Admit every retained record of a Run store against its owning schema."""
from __future__ import annotations

import json
from typing import Any

from . import admit, canonical, kit_schemas, store


class GraphAdmitError(Exception):
    def __init__(self, code: str, message: str, path: str = "", failures: list | None = None):
        super().__init__(f"{code}:{path}: {message}")
        self.code = code
        self.message = message
        self.path = path
        self.firstRefusal = code
        self.failures = failures or []


def _load_c(st: store.Store, digest: str):
    bare = digest.split(":")[-1]
    raw = st.blobs.get(bare) or st.blobs.get(digest)
    if raw is None:
        raise GraphAdmitError("MISSING_PREIMAGE", digest, digest)
    return json.loads(raw.decode("utf-8"))


CLASS_TO_DOMAIN = {
    "TypeScriptNativeContextV2": ("native-context", "native.context.typescript.v2"),
    "NativeContextV2": ("native-context", "native.context.rust.v2"),
    "SyntaxNativeContextV2": ("native-context", "native.context.syntax.v2"),
    "TypeScriptUniverseV2ResolvedInputs": ("native-semantic-universe", "native.semantic-universe.typescript.v2"),
    "RustUniverseV2ResolvedInputs": ("native-semantic-universe", "native.semantic-universe.rust.v2"),
    "SyntaxUniverseV2ResolvedInputs": ("native-semantic-universe", "native.semantic-universe.syntax.v2"),
    "DependencySourceSetV1": ("native-context", "native.dependency-source-set.v1"),
    "UnifiedFeaturesV1": ("native-context", "native.unified-features.rust.v1"),
    "SourceUnitOwnershipV1": ("native-context", "native.source-unit-ownership.v1"),
    "CargoConfigProjectionV2": ("native-context", "native.cargo-config-projection.v2"),
}

NATIVE_SCHEMA_ID = "urn:opensip:product-v1:native:evidence-schemas:v2"


def classify_sha256_object(obj: Any) -> tuple[str, str] | None:
    """Return (schema_id, def_name) or None."""
    if not isinstance(obj, dict):
        return None
    if obj.get("schemaVersion") == 2 and "languageMode" in obj and "toolchain" in obj:
        tc = obj.get("toolchain") or {}
        if "compilerName" in tc:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "TypeScriptNativeContextV2")
        if "rustcVersion" in tc or "targetTriple" in obj:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "NativeContextV2")
    if obj.get("schemaVersion") == 2 and "targetTriple" in obj and "toolchain" in obj:
        tc = obj.get("toolchain") or {}
        if "rustcVersion" in tc:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "NativeContextV2")
    if obj.get("schemaVersion") == 2 and "grammarBundle" in obj:
        return ("urn:opensip:product-v1:native:evidence-schemas:v2", "SyntaxNativeContextV2")
    if obj.get("schemaVersion") == 2 and "tsconfigGraphHash" in obj:
        return ("urn:opensip:product-v1:native:evidence-schemas:v2", "TypeScriptUniverseV2ResolvedInputs")
    if obj.get("schemaVersion") == 2 and "crateRootPaths" in obj:
        return ("urn:opensip:product-v1:native:evidence-schemas:v2", "RustUniverseV2ResolvedInputs")
    if obj.get("schemaVersion") == 2 and "selectedGrammarIds" in obj:
        return ("urn:opensip:product-v1:native:evidence-schemas:v2", "SyntaxUniverseV2ResolvedInputs")
    if obj.get("schemaVersion") == 1 and "packages" in obj and obj.get("language") == "rust":
        return ("urn:opensip:product-v1:native:evidence-schemas:v2", "DependencySourceSetV1")
    if obj.get("schemaVersion") == 1 and "activated" in obj and "computedBy" in obj:
        return ("urn:opensip:product-v1:native:evidence-schemas:v2", "UnifiedFeaturesV1")
    if obj.get("schemaVersion") == 1 and "ownership" in obj and "selectedUnitIds" in obj:
        return ("urn:opensip:product-v1:native:evidence-schemas:v2", "SourceUnitOwnershipV1")
    if obj.get("schemaVersion") == 2 and "replacedSnapshotConfigs" in obj and "projectionSha256" in obj:
        return ("urn:opensip:product-v1:native:evidence-schemas:v2", "CargoConfigProjectionV2")
    return None


def object_ident_for_digest(st: store.Store, digest: str) -> str | None:
    if not digest:
        return None
    bare = digest.split(":")[-1]
    for cand in (digest, bare, "sha256:" + bare):
        if cand in st.objects:
            return cand
    return None


def classify_canonical_object(ident: str, obj: Any) -> tuple[str, str | None] | None:
    """Owning schema for retained canonical-record objects (prefixed or bare hex)."""
    if not isinstance(obj, dict):
        return None
    if ident.startswith("sha256:") or (len(ident) == 64 and all(c in "0123456789abcdef" for c in ident)):
        cls = classify_sha256_object(obj)
        if cls:
            return cls
        if obj.get("schemaVersion") == 1 and "entries" in obj and obj.get("entries") and "packageName" in (obj["entries"][0] or {}):
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "ResolvedNodeModulesLayoutV1")
        if obj.get("schemaVersion") == 1 and "entryConfigPath" in obj and "nodes" in obj:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "TypeScriptConfigGraphV1")
        if obj.get("schemaVersion") == 1 and "units" in obj and "rows" in obj and "erasedFiles" in obj:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "UnitMembershipV1")
        if obj.get("schemaVersion") == 1 and "cells" in obj and "membershipDigest" in obj:
            return ("opensip.product.enumeration-plan.1", None)
        if obj.get("schemaVersion") == 1 and "rules" in obj and "detectorClosure" in ((obj.get("rules") or [{}])[0] or {}):
            return ("urn:opensip:product-v1:evaluator-emission-plan:1", None)
        if obj.get("schemaVersion") == 1 and "selectedRefs" in obj and "cellOutcomes" in obj:
            return ("opensip.product.execution-inputs.1", None)
        if obj.get("schemaVersion") == 1 and "cellOrdinal" in obj and "rows" in obj and "kind" in obj:
            return ("opensip.product.subject-inventory.1", None)
        if obj.get("schemaVersion") == 2 and "occupancy" in obj and "sourceFactId" in obj:
            return ("opensip.product.target-attribution.2", None)
        if obj.get("schemaFamily") == "opensip.product.policy":
            return ("urn:opensip:product-v1:policy-document:2", "PolicyDocumentV2")
        if obj.get("schemaFamily") == "opensip.product.waivers":
            return ("urn:opensip:product-v1:workflows:policy-document", "WaiverSetV1")
        if obj.get("schemaFamily") == "opensip.product.scope":
            return ("urn:opensip:product-v1:workflows:policy-document", "ScopeDocumentV1")
        if obj.get("payloadDomain") == "workflow.import-payload.runtime.v1":
            return ("urn:opensip:product-v1:workflows:imported-evidence", "RuntimePayloadV1")
        if obj.get("schemaVersion") == 2 and "requestedCapabilities" in obj:
            return ("urn:opensip:product-v1:identity:v3", "analysis-spec")
        if obj.get("schemaVersion") == 2 and "analysis" in obj and ("capabilities" in (obj.get("analysis") or {}) or "components" in obj):
            return ("urn:opensip:product-v1:identity:v3", "semantic-configuration")
        if obj.get("schemaVersion") == 1 and "pathPrefixes" in obj and "workspaceRoots" in obj:
            return ("urn:opensip:product-v1:identity:v3", "scope-descriptor")
        if obj.get("schemaVersion") == 2 and "rules" in obj and "policyDigest" in obj:
            return ("urn:opensip:product-v1:policy-document:2", "RuleProgramV2")
        if obj.get("schemaVersion") == 1 and "messageCode" in obj and "parameters" in obj:
            return ("urn:opensip:product-v1:identity:v3", "finding-parameters")
        if "childPredicateIds" in obj and "matchingFactIds" in obj and "kind" in obj:
            return ("urn:opensip:product-v1:identity:v3", "predicate-witness")
        if obj.get("schemaVersion") == 1 and "commitId" in obj and "sourceInventoryDigest" in obj:
            return ("urn:opensip:product-v1:identity:v3", "vcs-observation")
        if obj.get("schemaVersion") == 1 and obj.get("kind") in {"exact-snapshot"} and "snapshotId" in obj:
            return ("urn:opensip:product-v1:workflows:common", "SourceCorrespondence")
        if obj.get("schemaVersion") == 1 and "window" in obj and "population" in obj:
            return ("urn:opensip:product-v1:workflows:imported-evidence", "ImportObservationV1")
        if obj.get("schemaVersion") == 1 and "buildIdentity" in obj and set(obj.keys()) <= {"schemaVersion", "buildIdentity"}:
            return ("urn:opensip:product-v1:workflows:imported-evidence", "BuildIdentityV1")
        if obj.get("schemaVersion") == 3 and "entry" in obj and "key" in obj:
            return ("urn:opensip:product-v1:native:evidence-schemas:v2", "CoverageResultV3")
        if obj.get("schemaVersion") == 1 and "authority" in obj and obj.get("authority") == "candidate-only":
            return ("opensip.product.execution-inputs.1", "CandidateProducerResultV1")
        if obj.get("schemaVersion") == 2 and "producerClosure" in obj and "operation" in obj and "planId" in obj:
            return ("urn:opensip:product-v1:identity:v3", "stage-spec")
    return None


def public_record(obj: Any) -> Any:
    """Strip helper-only keys (e.g. _digest) that are not part of C(X)."""
    if not isinstance(obj, dict):
        return obj
    return {k: v for k, v in obj.items() if not str(k).startswith("_")}


def admit_store(st: store.Store) -> dict:
    log = []
    failures = []
    admit.set_graph_context(st)

    def rec(path, fn):
        try:
            r = fn()
            log.append({"path": path, "admitted": True})
            return r
        except admit.AdmitError as e:
            failures.append({"path": path, "code": e.code, "message": e.message, "firstRefusal": e.code})
            log.append({"path": path, "admitted": False, "code": e.code, "message": e.message})
            return None

    for ident, obj in list(st.objects.items()):
        prefix = ident.split(":")[0] if ":" in ident else ""
        defn = kit_schemas.PREFIX_TO_IDENTITY_DEF.get(prefix)
        if defn:
            rec(ident, lambda d=defn, o=public_record(obj), i=ident: admit.admit_identity_record(o, d, st, i))
            continue
        cls = classify_canonical_object(ident, obj)
        if cls:
            sid, dname = cls
            rec(ident, lambda s=sid, d=dname, o=public_record(obj), i=ident: admit.admit_document(o, s, st, i, d))
            continue
        if prefix == "sha256":
            keys = list(obj)[:12] if isinstance(obj, dict) else type(obj).__name__
            log.append({"path": ident, "admitted": False, "note": "unclassified sha256 object; not skipped silently", "classification": "unknown"})
            failures.append(
                {
                    "path": ident,
                    "code": "UNCLASSIFIED_RETAINED_OBJECT",
                    "message": f"unclassified sha256 object keys={keys}",
                    "firstRefusal": "UNCLASSIFIED_RETAINED_OBJECT",
                }
            )

    # digest-domain nestedRecords: admit retained canonical nested records against their selectors
    idsch = kit_schemas.identity_schema()
    domain_sets = (idsch.get("x-opensip-digest-domains") or {}).get("domainSets") or {}
    for ident, obj in list(st.objects.items()):
        if not ident.startswith("sha256:"):
            continue
        cls = classify_sha256_object(obj)
        if not cls:
            continue
        _sid, dname = cls
        mapped = CLASS_TO_DOMAIN.get(dname)
        if not mapped:
            continue
        set_name, domain = mapped
        row = (domain_sets.get(set_name) or {}).get(domain) or {}
        for nr in row.get("nestedRecords") or []:
            cur = obj
            for p in nr.get("path") or []:
                cur = cur.get(p) if isinstance(cur, dict) else None
            if cur is None:
                continue
            if nr.get("form") != "canonical-record" or not isinstance(cur, str):
                continue
            selector = nr.get("selector") or ""
            defn = selector.rsplit("/", 1)[-1] if selector else None
            document = nr.get("document")
            sid = kit_schemas.schema_id_for_document(document) or NATIVE_SCHEMA_ID
            label = f"nested:{domain}:{'.'.join(nr.get('path') or [])}"
            try:
                payload = _load_c(st, cur)
            except GraphAdmitError as e:
                failures.append({"path": label, "code": e.code, "message": e.message, "firstRefusal": e.code})
                continue
            rec(label, lambda p=payload, s=sid, d=defn, lb=label: admit.admit_document(p, s, st, lb, d))

    # nested canonical records named by identity fields
    extra = []
    for ident, obj in list(st.objects.items()):
        if ident.startswith("plan2:"):
            extra.append(("analysis-spec", "urn:opensip:product-v1:identity:v3", "analysis-spec", obj["analysisSpecDigest"]))
            extra.append(("semantic-configuration", "urn:opensip:product-v1:identity:v3", "semantic-configuration", obj["resolvedConfigDigest"]))
            extra.append(("scope-descriptor", "urn:opensip:product-v1:identity:v3", "scope-descriptor", obj["scopeDigest"]))
            extra.append(("semantic-grant", "urn:opensip:product-v1:identity:v3", "semantic-grant", obj["semanticGrantDigest"]))
            extra.append(("policy", "urn:opensip:product-v1:policy-document:2", "PolicyDocumentV2", obj["policyDigest"]))
            extra.append(("waiver", "urn:opensip:product-v1:workflows:policy-document", "WaiverSetV1", obj["waiverDigest"]))
        if ident.startswith("proof3:"):
            extra.append(("execution-inputs", "opensip.product.execution-inputs.1", None, obj["executionInputsDigest"]))
            extra.append(("rule-program", "urn:opensip:product-v1:policy-document:2", "RuleProgramV2", obj["ruleProgramDigest"]))
        if ident.startswith("fact2:"):
            extra.append((ident, None, None, obj["payloadDigest"]))
        if ident.startswith("coverage2:"):
            extra.append((ident, "urn:opensip:product-v1:native:evidence-schemas:v2", "CoverageResultV3", obj["payloadDigest"]))
        if ident.startswith("import2:"):
            extra.append((ident, "urn:opensip:product-v1:workflows:imported-evidence", "RuntimePayloadV1", obj["payloadDigest"]))

    seen = set()
    for label, sid, dname, digest in extra:
        if digest in seen:
            continue
        seen.add(digest)
        try:
            payload = _load_c(st, digest)
        except GraphAdmitError as e:
            failures.append({"path": label, "code": e.code, "message": e.message, "firstRefusal": e.code})
            continue
        if label.startswith("fact2:"):
            fact = st.objects[label]
            rec(label, lambda p=payload, r=fact["relation"], lb=label: admit.admit_relation_payload(p, r, st, lb))
            continue
        if sid is None:
            continue
        owner = object_ident_for_digest(st, digest) or label
        rec(owner, lambda p=payload, s=sid, d=dname, lb=owner: admit.admit_document(p, s, st, lb, d))

    # execution-inputs named nested
    proofs = [o for i, o in st.objects.items() if i.startswith("proof3:")]
    if proofs:
        ei = _load_c(st, proofs[0]["executionInputsDigest"])
        ep_id = object_ident_for_digest(st, ei["enumerationPlanDigest"]) or "enumeration-plan"
        rec(
            ep_id,
            lambda: admit.admit_document(
                _load_c(st, ei["enumerationPlanDigest"]),
                "opensip.product.enumeration-plan.1",
                st,
                ep_id,
            ),
        )
        inv_digest = next(r["digest"] for r in ei["selectedRefs"] if r["domain"] == "subject-inventory")
        inv_id = object_ident_for_digest(st, inv_digest) or "subject-inventory"
        rec(
            inv_id,
            lambda: admit.admit_document(
                _load_c(st, inv_digest),
                "opensip.product.subject-inventory.1",
                st,
                inv_id,
            ),
        )

    if failures:
        first = failures[0]
        raise GraphAdmitError(
            first["code"],
            f"{len(failures)} record(s) refused; first={first['path']}: {first['message']}",
            first["path"],
            failures=failures,
        )
    return {"admitted": True, "records": log, "failures": []}
