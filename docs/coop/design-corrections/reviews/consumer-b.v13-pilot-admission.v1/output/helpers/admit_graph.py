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


def admit_store(st: store.Store) -> dict:
    log = []
    failures = []

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
            rec(ident, lambda d=defn, o=obj, i=ident: admit.admit_identity_record(o, d, st, i))
            continue
        if prefix == "sha256":
            cls = classify_sha256_object(obj)
            if cls:
                sid, dname = cls
                rec(ident, lambda s=sid, d=dname, o=obj, i=ident: admit.admit_document(o, s, st, i, d))
            else:
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
            extra.append((f"fact-payload:{ident}", None, None, obj["payloadDigest"]))
        if ident.startswith("coverage2:"):
            extra.append((f"coverage-payload:{ident}", "urn:opensip:product-v1:native:evidence-schemas:v2", "CoverageResultV3", obj["payloadDigest"]))
        if ident.startswith("import2:"):
            extra.append((f"import-payload:{ident}", "urn:opensip:product-v1:workflows:imported-evidence", "RuntimePayloadV1", obj["payloadDigest"]))

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
        if label.startswith("fact-payload:"):
            fact = st.objects[label.split(":", 1)[1]] if False else None
            # find fact
            fact = next(o for i, o in st.objects.items() if i.startswith("fact2:") and o.get("payloadDigest") == digest)
            rec(label, lambda p=payload, r=fact["relation"], lb=label: admit.admit_relation_payload(p, r, st, lb))
            continue
        if sid is None:
            continue
        rec(label, lambda p=payload, s=sid, d=dname, lb=label: admit.admit_document(p, s, st, lb, d))

    # execution-inputs named nested
    proofs = [o for i, o in st.objects.items() if i.startswith("proof3:")]
    if proofs:
        ei = _load_c(st, proofs[0]["executionInputsDigest"])
        rec(
            "enumeration-plan",
            lambda: admit.admit_document(
                _load_c(st, ei["enumerationPlanDigest"]),
                "opensip.product.enumeration-plan.1",
                st,
                "enumeration-plan",
            ),
        )
        rec(
            "subject-inventory",
            lambda: admit.admit_document(
                _load_c(st, next(r["digest"] for r in ei["selectedRefs"] if r["domain"] == "subject-inventory")),
                "opensip.product.subject-inventory.1",
                st,
                "subject-inventory",
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
