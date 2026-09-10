"""Meta-check isolated G3/G4/G5 draft schemas. Not Run replay. Not product execution."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

PY = sys.executable
ROOT = Path("/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections/foundation")
HELPER = Path("/tmp/opensip-design-corrections/grok-atom-contract.v3")
FROZEN_CANON = Path(
    "/tmp/opensip-design-corrections/candidate-subject.v21/docs/coop/design-corrections/foundation/canonical.py"
)

FILES = {
    "registry": ROOT / "evaluator-projection-registry.v1.json",
    "attribution": ROOT / "target-attribution.schema.v1.json",
    "contract": ROOT / "atom-evaluation-contract.v1.md",
}

NATIVE = [
    "file",
    "package",
    "vcs-change",
    "clones",
    "declares",
    "literal",
    "types",
    "control-flow",
    "reachability",
    "calls",
    "references",
    "imports",
    "unresolved-edge",
]
IMPORTED = [
    "runtime-observation",
    "history-change",
    "test-execution",
    "test-result",
]
FILTER_FIELDS = [
    "subject",
    "target",
    "resolution",
    "universe",
    "confidenceMillionths",
    "subjectKind",
    "targetKind",
    "observability",
    "testResult",
    "exitStatus",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    raw = path.read_bytes()
    return json.loads(raw.decode("utf-8")), raw


def check_metaschema(name: str, doc: dict, errors: list[str]) -> None:
    try:
        Draft202012Validator.check_schema(doc)
    except Exception as exc:  # noqa: BLE001 — report
        errors.append(f"{name}: metaschema: {exc}")


def validate_instance(schema: dict, instance: object, label: str, errors: list[str]) -> None:
    try:
        Draft202012Validator(schema).validate(instance)
    except ValidationError as exc:
        errors.append(f"{label}: {exc.message} at {list(exc.path)}")


def main() -> int:
    errors: list[str] = []
    notes: list[str] = []
    hashes = {k: sha256(p) for k, p in FILES.items()}

    registry, _ = load_json(FILES["registry"])
    attrib, _ = load_json(FILES["attribution"])

    check_metaschema("registry", registry, errors)
    check_metaschema("attribution", attrib, errors)

    rels = registry.get("relations") or {}
    missing = [r for r in NATIVE + IMPORTED if r not in rels]
    extra = [r for r in rels if r not in NATIVE + IMPORTED]
    if missing:
        errors.append(f"registry missing relations: {missing}")
    if extra:
        errors.append(f"registry extra relations: {extra}")

    for name, row in rels.items():
        filters = row.get("filters") or {}
        for field in FILTER_FIELDS:
            if field not in filters:
                errors.append(f"{name}: missing filter {field}")
        if row.get("plane") == "native" and "ladder" not in row:
            errors.append(f"{name}: native missing ladder")
        if name in ("calls", "references", "imports"):
            if row.get("universeRule") != "admitted-target":
                errors.append(f"{name}: expected admitted-target")
            if "symbol" not in (row.get("targetKinds") or []) and name != "imports":
                errors.append(f"{name}: targetKinds should include symbol")
        if name == "imports":
            kinds = set(row.get("targetKinds") or [])
            if kinds != {"file", "symbol", "package"}:
                errors.append(f"imports targetKinds {kinds} != file|symbol|package")
            if row.get("sourceSubjectKind") != "symbol":
                errors.append("imports sourceSubjectKind must remain symbol")

    if registry.get("exportLaw", {}).get("exportIsNotAKind") is not True:
        errors.append("exportIsNotAKind must be true")
    if "export" in registry.get("exportLaw", {}).get("subjectKindFilterTokens", []):
        errors.append("subjectKindFilterTokens must not include export")

    repair = set(registry.get("repairVsPolicy", {}).get("repairImportedRequirementProducers") or [])
    if repair != {"runtime-observation", "history-change"}:
        errors.append(f"repair producers {repair}")
    if rels["test-execution"].get("repairRequirementProducer") is not False:
        errors.append("test-execution must not be a repair producer")
    if rels["test-result"].get("repairRequirementProducer") is not False:
        errors.append("test-result must not be a repair producer")

    if registry.get("runtimeSubjectOrder", {}).get("notCanonicalSetOfWholeRows") is None:
        errors.append("must keep runtime order warning")

    # TargetAttribution examples
    good_first_party = {
        "schemaVersion": 1,
        "planId": "plan2:" + "a" * 64,
        "sourceFactId": "fact2:" + "b" * 64,
        "producerClosure": "closure2:" + "c" * 64,
        "targetUniverse": "d" * 64,
        "targetNativeId": "src/a.ts",
        "kind": "file",
        "occupancy": "first-party",
        "exported": None,
        "logicalPath": None,
    }
    validate_instance(attrib, good_first_party, "attr-first-party-file", errors)

    good_symbol = dict(good_first_party)
    good_symbol["kind"] = "symbol"
    good_symbol["targetNativeId"] = "ts-symbol:src/a.ts#f"
    good_symbol["exported"] = "exported"
    validate_instance(attrib, good_symbol, "attr-first-party-symbol", errors)

    good_external = dict(good_first_party)
    good_external["occupancy"] = "external"
    good_external["kind"] = "package"
    good_external["targetNativeId"] = "lodash"
    good_external["logicalPath"] = None
    validate_instance(attrib, good_external, "attr-external-package", errors)

    bad_export_kind = dict(good_first_party)
    bad_export_kind["kind"] = "export"
    try:
        Draft202012Validator(attrib).validate(bad_export_kind)
        errors.append("attr-kind-export should refuse")
    except ValidationError:
        notes.append("attr-kind-export refused as required")

    bad_path_on_fp = dict(good_first_party)
    bad_path_on_fp["logicalPath"] = "src/a.ts"
    try:
        Draft202012Validator(attrib).validate(bad_path_on_fp)
        errors.append("logicalPath on first-party should refuse")
    except ValidationError:
        notes.append("logicalPath on first-party refused as required")

    bad_exported_file = dict(good_first_party)
    bad_exported_file["exported"] = "exported"
    try:
        Draft202012Validator(attrib).validate(bad_exported_file)
        errors.append("exported on file should refuse")
    except ValidationError:
        notes.append("exported on file refused as required")

    # FieldFilterSuccessor examples
    ff = registry["$defs"]["FieldFilterSuccessorV1"]
    validate_instance(
        ff,
        {"field": "exitStatus", "cmp": "in", "value": [0, 1, 2]},
        "ff-exit-in-ints",
        errors,
    )
    validate_instance(
        ff,
        {"field": "exitStatus", "cmp": "eq", "value": 1},
        "ff-exit-eq",
        errors,
    )
    validate_instance(
        ff,
        {"field": "subject", "cmp": "in", "value": ["src/a.ts", "src/b.ts"]},
        "ff-subject-in-strings",
        errors,
    )
    try:
        Draft202012Validator(ff).validate({"field": "exitStatus", "cmp": "in", "value": ["0"]})
        errors.append("exitStatus in should refuse string array")
    except ValidationError:
        notes.append("exitStatus in string array refused as required")
    try:
        Draft202012Validator(ff).validate({"field": "subject", "cmp": "in", "value": [1, 2]})
        errors.append("subject in should refuse integer array")
    except ValidationError:
        notes.append("subject in integer array refused as required")
    try:
        Draft202012Validator(ff).validate({"field": "confidenceMillionths", "cmp": "eq", "value": 1})
        errors.append("confidenceMillionths eq should refuse")
    except ValidationError:
        notes.append("confidenceMillionths eq refused as required")
    validate_instance(
        ff,
        {"field": "targetKind", "cmp": "eq", "value": "file"},
        "ff-targetKind-file",
        errors,
    )

    addr = registry["$defs"]["ObservationAddressV1"]
    validate_instance(
        addr,
        {
            "importId": "import2:" + "e" * 64,
            "selector": "test-execution",
            "ordinal": None,
        },
        "addr-execution",
        errors,
    )
    validate_instance(
        addr,
        {
            "importId": "import2:" + "e" * 64,
            "selector": "runtime-subject",
            "ordinal": 0,
        },
        "addr-runtime",
        errors,
    )
    try:
        Draft202012Validator(addr).validate(
            {
                "importId": "import2:" + "e" * 64,
                "selector": "test-execution",
                "ordinal": 0,
            }
        )
        errors.append("test-execution ordinal must be null")
    except ValidationError:
        notes.append("test-execution non-null ordinal refused as required")

    # Contract mentions
    md = FILES["contract"].read_text(encoding="utf-8")
    for needle in [
        "G3–G5 are not closed",
        "Export is not a kind token",
        "`none` **false**",
        "ObservationAddressV1",
        "notCanonicalSetOfWholeRows" if False else "absent-symbol before present",
        "REPAIR.EVIDENCE_RELATION_NO_PRODUCER",
        "no backlink",
        "ATOM_CROSS_FAMILY_EDGE_NOT_OWED",
        "tests=[]",
        "completenessEstablished",
    ]:
        if needle not in md:
            errors.append(f"contract missing phrase: {needle}")

    # Frozen canonical typed admission of attribution example
    if FROZEN_CANON.is_file():
        sys.path.insert(0, str(FROZEN_CANON.parent))
        import canonical as C  # type: ignore

        try:
            C.typed(good_first_party)
            digest = hashlib.sha256(C.canonical(good_first_party)).hexdigest()
            notes.append(f"canonical TargetAttributionV1 example digest {digest}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f"canonical admission of attribution example: {exc}")
    else:
        errors.append("frozen canonical.py missing; skipped typed admission")

    report = {
        "standing": "draft meta-check only; not Run replay; not product execution",
        "python": PY,
        "files": {k: {"path": str(p), "sha256": hashes[k], "bytes": p.stat().st_size} for k, p in FILES.items()},
        "errors": errors,
        "notes": notes,
        "ok": not errors,
    }
    out = HELPER / "check-atom-drafts.report.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
