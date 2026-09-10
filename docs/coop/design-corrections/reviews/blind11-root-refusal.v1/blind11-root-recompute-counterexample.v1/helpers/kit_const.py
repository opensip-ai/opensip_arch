"""Kit file digests and closed vocabularies used by reconstruction."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from helpers.paths import KIT

def file_sha(rel: str) -> str:
    return hashlib.sha256((KIT / rel).read_bytes()).hexdigest()

RELATION_PAYLOAD_DOC = "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
NATIVE_SCHEMA_DOC = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
IDENTITY_SCHEMA_DOC = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
POLICY_V2_DOC = "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"
POLICY_V1_DOC = "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"
ENUM_PLAN_DOC = "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"
EMISSION_DOC = "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"
EXEC_INPUTS_DOC = "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
SUBJECT_INV_DOC = "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"
IMPORT_EV_DOC = "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json"
COMMON3_DOC = "docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json"

RELATION_PAYLOAD_SHA = file_sha(RELATION_PAYLOAD_DOC.replace("docs/coop/design-corrections/", "docs/coop/design-corrections/"))
# paths under KIT already include docs/...
RELATION_PAYLOAD_SHA = file_sha("docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json")
NATIVE_SCHEMA_SHA = file_sha("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
IDENTITY_SCHEMA_SHA = file_sha("docs/coop/design-corrections/foundation/identity-schemas.v3.json")
POLICY_V2_SHA = file_sha("docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json")
POLICY_V1_SHA = file_sha("docs/coop/design-corrections/workflows/schemas/policy-document.schema.json")
ENUM_PLAN_SHA = file_sha("docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json")
EMISSION_SHA = file_sha("docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json")
IMPORT_EV_SHA = file_sha("docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json")
COMMON3_SHA = file_sha("docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json")
SUBJECT_INV_SHA = file_sha("docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json")
EXEC_INPUTS_SHA = file_sha("docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json")

SUFFIX_TABLE = {
    ".d.ts": "ts-declaration",
    ".ts": "ts",
    ".tsx": "tsx",
    ".mts": "mts",
    ".cts": "cts",
    ".js": "js",
    ".jsx": "jsx",
    ".mjs": "mjs",
    ".cjs": "cjs",
}
BODY_LANGUAGE_BY_VARIANT = {
    "ts": "typescript",
    "tsx": "typescript",
    "ts-declaration": "typescript",
    "mts": "typescript",
    "cts": "typescript",
    "js": "javascript",
    "jsx": "javascript",
    "mjs": "javascript",
    "cjs": "javascript",
}

def load(rel: str):
    return json.loads((KIT / rel).read_text())
