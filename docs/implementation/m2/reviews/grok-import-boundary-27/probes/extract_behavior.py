"""Local probes for import correspondence / parameter selection. Not product admission."""
from __future__ import annotations

import json
from pathlib import Path

ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
SRC = (
    ARCH
    / "docs/implementation/m2/predicate-matching-reference-selection-v1/reference/workflows_model.v1.py"
).read_text()
START = SRC.index("STALENESS_TABLE = [")
END = SRC.index("\ndef consumable_runtime_subjects")
NS: dict = {}
exec(SRC[START:END], NS)
classify = NS["classify_staleness"]
ST = NS["STALENESS_TABLE"]

snap = "snapshot2:" + "a" * 64
other = "snapshot2:" + "b" * 64
commit = "c" * 40
otherc = "d" * 40
mapping = "m" * 64


def add(cases, name, corr, bind, corrupt=False, expect_cond=None, expect_use=None):
    try:
        result = classify(corr, bind, corrupt=corrupt)
        rec = {"name": name, "result": result, "ok": True, "err": None}
    except Exception as exc:
        rec = {
            "name": name,
            "result": None,
            "ok": False,
            "err": type(exc).__name__ + ":" + str(exc),
        }
        result = None
    if expect_cond is not None and result:
        rec["cond_ok"] = result["condition"] == expect_cond and result["usable"] == expect_use
    cases.append(rec)


bind_eq = {
    "snapshotId": snap,
    "vcsRevision": {"system": "git", "commit": commit, "dirty": False},
    "declaredBuildIds": ["build-1"],
    "admittedSourceMappings": [mapping],
}
cases = []
add(
    cases,
    "exact-equal",
    {"kind": "exact-snapshot", "snapshotId": snap},
    bind_eq,
    expect_cond="snapshot-equal",
    expect_use="consumable",
)
add(
    cases,
    "vcs-mapped",
    {
        "kind": "vcs-revision",
        "vcsRevision": {"system": "git", "commit": commit, "dirty": False},
        "buildIdentity": None,
        "sourceMappingDigest": mapping,
    },
    bind_eq,
    expect_cond="commit-equal-clean-mapped",
    expect_use="consumable",
)


def mapping_extra(mapping_doc, inventory, expected):
    if mapping_doc["snapshotId"] != expected:
        return "IMPORT.SOURCE_MAPPING_REQUIRED:snapshot"
    inv = {b["path"]: b["sha256"] for b in inventory}
    paths = [e["generatedPath"] for e in mapping_doc["entries"]]
    if paths != sorted(paths, key=lambda s: s.encode()) or len(set(paths)) != len(paths):
        return "IMPORT.ARTIFACT_CORRUPT:order"
    for entry in mapping_doc["entries"]:
        if inv.get(entry["sourcePath"]) != entry["sourceSha256"]:
            return "IMPORT.SOURCE_MAPPING_REQUIRED:inventory:" + entry["generatedPath"]
    return "ok"


class AdmissionError(Exception):
    pass


ROWS = {
    "foundation/import-source-context.schema.json": {"requiredForEvaluatorMajors": []},
    "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1": {
        "requiredForEvaluatorMajors": []
    },
    "foundation/enumeration-plan.schema.v1.json": {"requiredForEvaluatorMajors": [3]},
    "foundation/evaluator-emission-plan.schema.v1.json": {"requiredForEvaluatorMajors": [3]},
    "foundation/framework-recognition-plan.schema.v1.json": {"requiredForEvaluatorMajors": []},
}
ROW_OF = {
    "51cdca8bd3c9212d11982416b9101be96bdcf47db22efb0098b39c7850ae6518": "foundation/import-source-context.schema.json",
    "012505da479197875602899c027b3d0daea9e23e01e490e3dc94bbe3d7062e18": "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1",
    "10627cb6a22a9ff1674c16c5fa4863a58dc86e5df8ac7ae55c45747b0e60197c": "foundation/enumeration-plan.schema.v1.json",
    "ac9ae438ca3e1a94e257209c460cd7beed5047e0d9d0a7bf49a94b637dd3198e": "foundation/evaluator-emission-plan.schema.v1.json",
    "49aacd8607e3f3195ac350b678f318388a5faf8f56f42e52087ec9ebe57ef822": "foundation/framework-recognition-plan.schema.v1.json",
}


def admit_parameter_selection(parameters):
    seen = {}
    for entry in parameters:
        row = ROW_OF.get(entry["schemaDigest"])
        if row is None:
            continue
        seen[row] = seen.get(row, 0) + 1
    for row in sorted(seen):
        if seen[row] > 1:
            raise AdmissionError("ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:" + row)
    for row, record in ROWS.items():
        if 3 in record.get("requiredForEvaluatorMajors", []) and seen.get(row) != 1:
            raise AdmissionError("EVALUATOR_REQUIRED_PARAMETER_MISSING:" + row)
    return parameters


if __name__ == "__main__":
    print(json.dumps({"staleness_table_rows": len(ST), "sample": cases[0]}, indent=2))
