"""Load every current normative owner from the frozen 80-file kit."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-other-runs-full-review.v1/subject")
EXPORTS = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-other-runs-full-review.v1/exports")
EXPORT_MANIFEST = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-other-runs-full-review.v1/export-manifest.json")
REQUIREMENTS = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-other-runs-full-review.v1/requirements.json")
CHARTER = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-other-runs-full-review.v1/original-consumer-charter.txt")


def _load_json(rel: str) -> Any:
    return json.loads((KIT / rel).read_text())


class KitOwners:
    def __init__(self) -> None:
        self.manifest = json.loads((KIT / "consumer-input-manifest.json").read_text())
        self.identity_v3 = _load_json("docs/coop/design-corrections/foundation/identity-schemas.v3.json")
        self.identity_v2 = _load_json("docs/coop/design-corrections/foundation/identity-schemas.v2.json")
        self.relation = _load_json("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
        self.native = _load_json("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
        self.matrix = _load_json("docs/coop/design-corrections/native/native-capability-matrix.v2.json")
        self.cap_domains = _load_json("docs/coop/design-corrections/native/capability-manifest-domains.v2.json")
        self.enum_plan = _load_json("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json")
        self.subject_inv = _load_json("docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json")
        self.emission = _load_json("docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json")
        self.exec_inputs = _load_json("docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json")
        self.target_attr = _load_json("docs/coop/design-corrections/foundation/target-attribution.schema.v1.json")
        self.incoming = _load_json("docs/coop/design-corrections/foundation/incoming-search.schema.v1.json")
        self.proj_reg = _load_json("docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json")
        self.policy_v2 = _load_json("docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json")
        self.policy_v1 = _load_json("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json")
        self.imported = _load_json("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json")
        self.common = _load_json("docs/coop/design-corrections/workflows/schemas/common.schema.json")
        self.common_e3 = _load_json("docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json")
        self.fact_identity = _load_json("docs/coop/artifacts/fact-identity-policy.v2.json")
        self.resolved_inputs = _load_json("docs/coop/artifacts/resolved-inputs.v2.json")
        self.delivery_v4 = _load_json("docs/coop/artifacts/delivery.v4.json")
        self.requirements = json.loads(REQUIREMENTS.read_text())
        self.export_manifest = json.loads(EXPORT_MANIFEST.read_text())
        self.file_bytes: dict[str, bytes] = {}
        self.file_sha: dict[str, str] = {}
        for rec in self.manifest["files"]:
            raw = (KIT / rec["path"]).read_bytes()
            self.file_bytes[rec["path"]] = raw
            self.file_sha[rec["path"]] = hashlib.sha256(raw).hexdigest()

        self.digest_domains = self.identity_v3["x-opensip-digest-domains"]
        self.payload_registry = self.identity_v3["x-opensip-payload-registry"]
        self.relation_registry = self.relation["x-opensip-relation-registry"]["relations"]
        self.grammar_registry = self.native["x-opensip-grammar-capability-registry"]
        self.deficiency_cause = self.native["x-opensip-deficiency-cause-registry"]["deficiencies"]
        self.evaluator_deficiencies = self.identity_v3["x-opensip-evaluator-deficiency-registry"]
        self.policy_universe_map = self.identity_v3["x-opensip-evaluator-profile"]["policyUniverseMap"]
        self.language_modes = self.digest_domains["languageModes"]["map"]
        self.closure_kinds = self.digest_domains["closureKinds"]["byField"]
        self.atom_relations = self.proj_reg["relations"]
        self.capability_for_relation = self.proj_reg["capabilityForRelation"]
        self.subject_language_table = self.subject_inv.get("x-opensip-subject-language-table") or {}

        self.schemas_by_id: dict[str, dict[str, Any]] = {}
        self.schemas_by_rel: dict[str, dict[str, Any]] = {}
        for rec in self.manifest["files"]:
            if rec["path"].endswith(".json"):
                doc = json.loads(self.file_bytes[rec["path"]])
                if isinstance(doc, dict) and "$id" in doc:
                    self.schemas_by_id[doc["$id"]] = doc
                self.schemas_by_rel[rec["path"]] = doc

    def kit_sha(self, rel_under_docs: str) -> str:
        """rel like foundation/identity-schemas.v3.json relative to design-corrections or full kit path."""
        candidates = [
            f"docs/coop/design-corrections/{rel_under_docs}",
            f"docs/coop/{rel_under_docs}",
            rel_under_docs,
        ]
        for c in candidates:
            if c in self.file_sha:
                return self.file_sha[c]
        raise KeyError(rel_under_docs)

    def document_sha_for_payload_row(self, document: str) -> str:
        # payload registry documents are relative to design-corrections
        return self.kit_sha(document)

    def matrix_cell(self, mode: str, capability: str) -> dict[str, Any] | None:
        for cell in self.matrix["cells"]:
            if cell.get("mode") == mode and cell.get("capability") == capability:
                return cell
        return None

    def grammar_for_language(self, language_id: str) -> dict[str, Any] | None:
        return self.grammar_registry["languages"].get(language_id)

    def suffix_language(self, path: str) -> str:
        name = path.rsplit("/", 1)[-1]
        best = ""
        lang = "unspecified"
        members = []
        table = self.subject_language_table
        if isinstance(table, dict):
            members = table.get("members") or []
        for row in members:
            lg = row.get("languageId")
            for suf in row.get("suffixes") or []:
                if name.endswith(suf) and len(suf) > len(best):
                    best = suf
                    lang = lg
        if best:
            return lang
        for lg, row in self.grammar_registry["languages"].items():
            for suf in row.get("suffixes") or []:
                if name.endswith(suf) and len(suf) > len(best):
                    best = suf
                    lang = lg
        return lang if best else "unspecified"
