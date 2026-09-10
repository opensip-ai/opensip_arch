"""Load the 80-file normative kit: schemas, registries, file bytes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from canonical import AdmissionError


KIT_ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-review.v1/subject")
EXPORTS_ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-pilot-checker-peer-review.v1/exports")

PREFIX_TO_DOMAIN = {
    "snapshot2": "snapshot",
    "closure2": "closure",
    "import2": "import",
    "plan2": "plan",
    "scope2": "subject-scope",
    "fact2": "fact",
    "coverage2": "coverage",
    "view2": "view",
    "exec-plan2": "execution-plan",
    "finding-key2": "finding-fingerprint",
    "subject3": "evaluation-subject",
    "finding3": "finding",
    "proof3": "proof-bundle",
    "evidence3": "semantic-evidence",
    "seal3": "evaluation-seal",
    "run3": "run",
    "cache2": "cache-key",
    "regen2": "regeneration-key",
    "policy-derivation3": "policy-derivation",
}

DOMAIN_TO_PREFIX = {v: k for k, v in PREFIX_TO_DOMAIN.items()}

UNCHANGED_MAJOR2_PREFIX = {
    "snapshot": "snapshot2",
    "closure": "closure2",
    "import": "import2",
    "plan": "plan2",
    "subject-scope": "scope2",
    "fact": "fact2",
    "coverage": "coverage2",
    "view": "view2",
    "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2",
    "cache-key": "cache2",
    "regeneration-key": "regen2",
}


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest(), path.stat().st_size


class Kit:
    def __init__(self, root: Path = KIT_ROOT):
        self.root = root
        self.docs = root / "docs"
        self.coop = self.docs / "coop"
        self.dc = self.coop / "design-corrections"
        self.foundation = self.dc / "foundation"
        self.native = self.dc / "native"
        self.workflows = self.dc / "workflows"
        self.wf_schemas = self.workflows / "schemas"
        self.artifacts = self.coop / "artifacts"
        self.file_bytes: dict[str, bytes] = {}
        self.file_sha256: dict[str, str] = {}
        self._load_files()
        self.identity_v3 = self._json("docs/coop/design-corrections/foundation/identity-schemas.v3.json")
        self.identity_v2 = self._json("docs/coop/design-corrections/foundation/identity-schemas.v2.json")
        self.native_schemas = self._json("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
        self.relation_payloads = self._json("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
        self.cap_domains = self._json("docs/coop/design-corrections/native/capability-manifest-domains.v2.json")
        self.cap_matrix = self._json("docs/coop/design-corrections/native/native-capability-matrix.v2.json")
        self.execution_inputs_schema = self._json("docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json")
        self.enumeration_plan_schema = self._json("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json")
        self.emission_plan_schema = self._json("docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json")
        self.subject_inventory_schema = self._json("docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json")
        self.policy_v2 = self._json("docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json")
        self.policy_v1 = self._json("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json")
        self.imported_evidence = self._json("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json")
        self.common_schema = self._json("docs/coop/design-corrections/workflows/schemas/common.schema.json")
        self.component_manifest = self._json("docs/coop/artifacts/component-manifest-schemas.v11.json")
        self.fact_identity_policy = self._json("docs/coop/artifacts/fact-identity-policy.v2.json")
        self.resolved_inputs = self._json("docs/coop/artifacts/resolved-inputs.v2.json")
        self.delivery_v4 = self._json("docs/coop/artifacts/delivery.v4.json")
        self.security_lifecycle = self._json("docs/coop/design-corrections/security/security-lifecycle.schemas.v1.json")
        self.digest_domains = self.identity_v3["x-opensip-digest-domains"]
        self.payload_registry = self.identity_v3["x-opensip-payload-registry"]
        self.evaluator_profile = self.identity_v3["x-opensip-evaluator-profile"]
        self.relation_registry = self.relation_payloads["x-opensip-relation-registry"]
        self.domain_sets = self.digest_domains["domainSets"]
        self.by_domain = self.digest_domains["byDomain"]
        self.schema_documents: dict[str, dict] = {}
        self._register_schema_docs()
        self.kit_document_sha256 = {
            rel: self.file_sha256[rel]
            for rel in self.file_sha256
            if rel.endswith(".json") or rel.endswith(".md")
        }

    def _load_files(self) -> None:
        man_path = self.root / "consumer-input-manifest.json"
        man = json.loads(man_path.read_text())
        for rec in man["files"]:
            rel = rec["path"]
            p = self.root / rel
            raw = p.read_bytes()
            actual = hashlib.sha256(raw).hexdigest()
            if actual != rec["sha256"] or len(raw) != rec["bytes"]:
                raise AdmissionError(
                    "KIT_HASH_MISMATCH",
                    "kit file hash/size mismatch",
                    "consumer-input-manifest.json",
                    {"path": rel, "actual": actual, "expected": rec["sha256"]},
                )
            self.file_bytes[rel] = raw
            self.file_sha256[rel] = actual

    def _json(self, rel: str) -> Any:
        return json.loads(self.file_bytes[rel])

    def bytes_of(self, rel: str) -> bytes:
        # callers pass kit-relative paths with various prefixes
        candidates = [
            rel,
            "docs/coop/design-corrections/" + rel,
            "docs/coop/" + rel,
        ]
        for c in candidates:
            if c in self.file_bytes:
                return self.file_bytes[c]
        # suffix match
        for k, v in self.file_bytes.items():
            if k.endswith("/" + rel) or k.endswith(rel):
                return v
        raise AdmissionError("KIT_FILE_MISSING", f"kit file not found: {rel}", "S-MISSING-DEP-IS-CUSTODY", {"path": rel})

    def sha256_of(self, rel: str) -> str:
        raw = self.bytes_of(rel)
        return hashlib.sha256(raw).hexdigest()

    def _register_schema_docs(self) -> None:
        mapping = {
            "identity": "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
            "native": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
            "relation": "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
            "execution-inputs": "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
            "enumeration-plan": "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
            "emission-plan": "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json",
            "subject-inventory": "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
            "policy-v2": "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
            "policy-v1": "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
            "imported-evidence": "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
            "common": "docs/coop/design-corrections/workflows/schemas/common.schema.json",
            "import-source-context": "docs/coop/design-corrections/foundation/import-source-context.schema.json",
            "target-attribution": "docs/coop/design-corrections/foundation/target-attribution.schema.v1.json",
            "incoming-search": "docs/coop/design-corrections/foundation/incoming-search.schema.v1.json",
        }
        for name, rel in mapping.items():
            self.schema_documents[name] = json.loads(self.file_bytes[rel])

    def payload_registry_document_sha256(self) -> dict[str, str]:
        """Raw SHA-256 of documents named by the payload registry (full file bytes)."""
        docs = {
            "foundation/relation-payload-schemas.v2.json": self.sha256_of(
                "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
            ),
            "native/native-evidence.schemas.v2.json": self.sha256_of(
                "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
            ),
            "workflows/schemas/imported-evidence.schema.json": self.sha256_of(
                "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json"
            ),
            "workflows/schemas/test-execution.schema.json": self.sha256_of(
                "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json"
            ),
            "workflows/schemas/policy-document.schema.json": self.sha256_of(
                "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"
            ),
            "workflows/schemas/policy-document.v2.schema.json": self.sha256_of(
                "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"
            ),
            "foundation/import-source-context.schema.json": self.sha256_of(
                "docs/coop/design-corrections/foundation/import-source-context.schema.json"
            ),
            "foundation/enumeration-plan.schema.v1.json": self.sha256_of(
                "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"
            ),
            "foundation/evaluator-emission-plan.schema.v1.json": self.sha256_of(
                "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"
            ),
            "foundation/execution-inputs.schema.v1.json": self.sha256_of(
                "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
            ),
            "foundation/subject-inventory.schema.v1.json": self.sha256_of(
                "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"
            ),
            "foundation/identity-schemas.v3.json": self.sha256_of(
                "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
            ),
        }
        return docs

    def resolve_selector(self, document: dict, selector: str) -> dict:
        if selector in ("#", ""):
            return document
        if not selector.startswith("#/"):
            raise AdmissionError("SELECTOR", f"unsupported selector {selector}", "identity-and-evidence.md§3 payload registry", {"selector": selector})
        cur: Any = document
        for part in selector[2:].split("/"):
            part = part.replace("~1", "/").replace("~0", "~")
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                raise AdmissionError("SELECTOR", f"selector {selector} not found", "identity-and-evidence.md§3", {"part": part})
        if not isinstance(cur, dict):
            raise AdmissionError("SELECTOR", f"selector {selector} is not an object schema", "identity-and-evidence.md§3", {})
        return cur
