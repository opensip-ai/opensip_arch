#!/usr/bin/env python3
"""Total retained checker for the Evidence v3 contract.

Evidence v3 closes the seven findings in the independent reviewer-10 report:

  E-SCHEMA  recursive, named, exact schemas; all parsed JSON values are total
  E-META    RequestId/attempt/time/process/cache/lifetime/producer shortcuts
            are forbidden at every semantic boundary
  E1        exact unique activation and member-set identity
  E2        typed proof unions, canonical relationship edges and full refs
  E3        host-derived proof-obligation identity
  E4        authoritative no-match derives Coverage and partition completeness
  E5        evaluation-proof.v2 commitments/verdict are consumed injectively
  E6        storage admission is resolved before durable evidence
  E7        retention-tiers.v7 owns exact minimum-capability closure validation
  E8        replay closure is non-empty, unique, CAS-resolved and unit-owned
  E9        indeterminate/error never becomes an authoritative pass
  E10       closed CAS binds full SHA-256 identity to canonical retained bytes
  E11       historical semantics/verifier availability consumes VERSIONING v3
  E12       sealed capability is immutable; effective capability is derived by
            retention-tiers.v7 and partial/purged/missing units confer no authority

No capability rank or retention state machine is implemented here. The checker
imports the exact Phase-1A public helpers and refuses a missing or drifted seam.

Usage: python3 artifacts/check-evidence.py [contract] [--selftest]
Exit: 0 clean; 1 findings; 2 I/O or JSON syntax error.
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import sys
import unicodedata
from typing import Any, Callable

BINDING = "evidence.v3.json"
PROOF = "evaluation-proof.v2.json"
RETENTION = "retention-tiers.v7.json"
VERSIONING = "versioning-policy.v3.json"
FACT_PLANE = "fact-plane.v1.json"
HERE = pathlib.Path(__file__).resolve().parent

REF_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PROJECT_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
RUN_RE = re.compile(r"^run1:[0-9a-f]{64}$")
EVALUATION_RE = re.compile(r"^eval1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
PREDICATE_RE = re.compile(r"^predicate1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
SUBJECT_RE = re.compile(r"^[a-z][a-z0-9-]*:[^\x00-\x1f\x7f]+$")
GENERIC_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._:#/-][a-z0-9]+)*$")

PAIRING = {
    "local-match": "match",
    "relationship-match": "match",
    "aggregate-match": "match",
    "no-match": "no-match",
    "indeterminate": "indeterminate",
    "error": "error",
}
PROOF_TAGS = {
    "local-match": "local-match-proof",
    "relationship-match": "relationship-match-proof",
    "aggregate-match": "aggregate-match-proof",
    "no-match": "no-match-proof",
    "indeterminate": "indeterminate-proof",
    "error": "error-proof",
}
CAS_SCHEMA_BY_KIND = {
    "predicate-semantics": "PredicateSemantics",
    "policy-semantics": "PolicySemantics",
    "coverage": "Coverage",
    "fact-partition": "FactPartition",
    "fact": "RelationshipFact",
    "relation-semantics": "RelationSemantics",
    "verifier-artifact": "VerifierArtifact",
    "replay-closure": "ReplayInput",
    "reason": "ReasonObject",
    "baseline": "BaselineObject",
    "waiver": "WaiverObject",
}
RAW_CAS_KINDS = {"bundle-signature"}

# Exact normalized names forbidden recursively. This is deliberately a key scan,
# not a handful of top-level schema exclusions.
FORBIDDEN_METADATA_KEYS = {
    "requestid", "executionid", "attemptid", "correlationid",
    "timestamp", "createdat", "updatedat", "sealedat", "producedat",
    "processid", "pid", "cachestate", "lifetimestate", "cachelifetime",
    "producerdeclaredobligation", "producerassertedadequacy",
    "factpartitionpinned", "regenerationclosureretained", "locallyresolvable",
}


def _load_module(filename: str, module_name: str):
    path = HERE / filename
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {filename}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256_ref(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _path(parent: str, child: str | int) -> str:
    return f"{parent}[{child}]" if isinstance(child, int) else f"{parent}.{child}"


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _nfc(value: str) -> bool:
    return unicodedata.normalize("NFC", value) == value


def _key_norm(key: str) -> str:
    return re.sub(r"[^a-z0-9]", "", key.lower())


def _metadata_findings(value: Any, path: str = "$bundle") -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    try:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = _path(path, str(key))
                if isinstance(key, str) and _key_norm(key) in FORBIDDEN_METADATA_KEYS:
                    out.append(("E-META", f"{child_path}: forbidden operational/producer "
                                          "metadata or removed boolean shortcut"))
                out.extend(_metadata_findings(child, child_path))
        elif isinstance(value, list):
            for i, child in enumerate(value):
                out.extend(_metadata_findings(child, _path(path, i)))
    except Exception as exc:
        out.append(("E-SCHEMA-TOTAL", f"{path}: metadata traversal controlled "
                                      f"{type(exc).__name__}: {exc}"))
    return out


def _primitive(value: Any, spec: dict[str, Any], path: str,
               type_outcome: str, constraint_outcome: str) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    typ = spec.get("type")
    ok = False
    if typ == "string":
        ok = isinstance(value, str)
    elif typ == "integer":
        ok = _is_int(value)
    elif typ == "boolean":
        ok = isinstance(value, bool)
    elif typ == "null":
        ok = value is None
    else:
        return [("E-SCHEMA-TOTAL", f"{path}: schema field has unknown primitive "
                                    f"type {typ!r}")]
    if not ok:
        return [(type_outcome, f"{path}: expected {typ}, got {type(value).__name__}")]
    if "const" in spec and value != spec["const"]:
        out.append((constraint_outcome, f"{path}: expected constant {spec['const']!r}"))
    enum = spec.get("enum")
    if enum is not None and value not in enum:
        out.append((constraint_outcome, f"{path}: {value!r} outside closed enum {enum!r}"))
    if isinstance(value, str):
        if spec.get("nfc", True) and not _nfc(value):
            out.append((constraint_outcome, f"{path}: string is not NFC"))
        if spec.get("nonempty") and not value:
            out.append((constraint_outcome, f"{path}: empty string forbidden"))
        if "minLength" in spec and len(value.encode("utf-8")) < spec["minLength"]:
            out.append((constraint_outcome, f"{path}: shorter than minimum UTF-8 length"))
        if "maxLength" in spec and len(value.encode("utf-8")) > spec["maxLength"]:
            out.append((constraint_outcome, f"{path}: exceeds maximum UTF-8 length"))
        pattern = spec.get("pattern")
        if pattern is not None:
            try:
                if re.fullmatch(pattern, value) is None:
                    out.append((constraint_outcome, f"{path}: value violates pattern {pattern!r}"))
            except re.error as exc:
                out.append(("E-SCHEMA-TOTAL", f"{path}: invalid schema pattern ({exc})"))
    if _is_int(value):
        if "minimum" in spec and value < spec["minimum"]:
            out.append((constraint_outcome, f"{path}: {value} below minimum "
                                            f"{spec['minimum']}"))
        if "maximum" in spec and value > spec["maximum"]:
            out.append((constraint_outcome, f"{path}: {value} above maximum "
                                            f"{spec['maximum']}"))
    return out


def _schema_validate(value: Any, schema_name: str, schemas: dict[str, Any],
                     path: str = "$bundle", depth: int = 0) -> list[tuple[str, str]]:
    """Validate one node under the declared named schema. Total by construction."""
    out: list[tuple[str, str]] = []
    if depth > 256:
        return [("E-SCHEMA-TOTAL", f"{path}: schema/value nesting exceeds 256")]
    schema = schemas.get(schema_name)
    if not isinstance(schema, dict):
        return [("E-SCHEMA-TOTAL", f"{path}: missing named schema {schema_name!r}")]
    type_outcome = schema.get("typeOutcome", "EVIDENCE_TYPE_MISMATCH")
    constraint_outcome = schema.get("constraintOutcome", "EVIDENCE_CONSTRAINT_VIOLATION")
    kind = schema.get("kind")
    try:
        if kind == "object":
            if not isinstance(value, dict):
                return [(type_outcome, f"{path}: expected {schema_name} object, got "
                                       f"{type(value).__name__}")]
            required = set(schema.get("required", []))
            optional = set(schema.get("optional", []))
            forbidden = set(schema.get("forbiddenFields", []))
            allowed = required | optional
            unknown_outcome = schema.get("unknownFieldOutcome",
                                         "EVIDENCE_RECORD_UNKNOWN_FIELD")
            for key in sorted((str(k) for k in value.keys())):
                if key in forbidden:
                    out.append((unknown_outcome, f"{_path(path, key)}: forbidden field in "
                                                   f"closed {schema_name}"))
                elif key not in allowed:
                    out.append((unknown_outcome, f"{_path(path, key)}: unknown field in "
                                                   f"closed {schema_name}"))
            for key in sorted(required):
                if key not in value:
                    out.append((type_outcome, f"{path}: missing required field {key!r}"))
            fields = schema.get("fields")
            if not isinstance(fields, dict):
                return out + [("E-SCHEMA-TOTAL", f"{path}: {schema_name}.fields missing")]
            for key in sorted(allowed & set(value)):
                spec = fields.get(key)
                if not isinstance(spec, dict):
                    out.append(("E-SCHEMA-TOTAL", f"{_path(path, key)}: no exact field schema"))
                elif "schema" in spec:
                    out.extend(_schema_validate(value[key], spec["schema"], schemas,
                                                _path(path, key), depth + 1))
                else:
                    out.extend(_primitive(value[key], spec, _path(path, key),
                                          type_outcome, constraint_outcome))
            return out
        if kind == "array":
            if not isinstance(value, list):
                return [(type_outcome, f"{path}: expected {schema_name} array, got "
                                       f"{type(value).__name__}")]
            if len(value) < schema.get("minItems", 0):
                out.append((constraint_outcome, f"{path}: requires at least "
                                                f"{schema.get('minItems')} items"))
            if "maxItems" in schema and len(value) > schema["maxItems"]:
                out.append((constraint_outcome, f"{path}: exceeds maxItems"))
            item_schema = schema.get("items")
            if not isinstance(item_schema, str):
                return out + [("E-SCHEMA-TOTAL", f"{path}: array has no named item schema")]
            canonical_seen: set[str] = set()
            for i, item in enumerate(value):
                out.extend(_schema_validate(item, item_schema, schemas, _path(path, i),
                                            depth + 1))
                if schema.get("uniqueItems"):
                    encoded = _canonical_json(item)
                    if encoded in canonical_seen:
                        out.append((constraint_outcome, f"{_path(path, i)}: duplicate item"))
                    canonical_seen.add(encoded)
            return out
        if kind == "taggedUnion":
            if not isinstance(value, dict):
                return [(type_outcome, f"{path}: expected tagged object, got "
                                       f"{type(value).__name__}")]
            discriminator = schema.get("discriminator")
            variants = schema.get("variants")
            tag = value.get(discriminator) if isinstance(discriminator, str) else None
            target = variants.get(tag) if isinstance(variants, dict) else None
            if not isinstance(target, str):
                return [(constraint_outcome, f"{path}: unknown {discriminator} tag {tag!r}")]
            return _schema_validate(value, target, schemas, path, depth + 1)
        if kind == "primitive":
            spec = schema.get("value")
            if not isinstance(spec, dict):
                return [("E-SCHEMA-TOTAL", f"{path}: primitive schema has no value rule")]
            return _primitive(value, spec, path, type_outcome, constraint_outcome)
        return [("E-SCHEMA-TOTAL", f"{path}: schema {schema_name!r} has unknown kind {kind!r}")]
    except Exception as exc:
        out.append(("E-SCHEMA-TOTAL", f"{path}: controlled schema failure "
                                      f"{type(exc).__name__}: {exc}"))
        return out


def _ref_id(value: Any, kind: str | None = None) -> str | None:
    if not isinstance(value, dict) or set(value) != {"kind", "id"}:
        return None
    if not isinstance(value.get("kind"), str) or not isinstance(value.get("id"), str):
        return None
    if kind is not None and value["kind"] != kind:
        return None
    return value["id"] if REF_RE.fullmatch(value["id"]) else None


def _cas(bundle: dict[str, Any], contract: dict[str, Any],
         out: list[tuple[str, str]]) -> dict[str, dict[str, Any]]:
    """Resolve full ContentRef -> canonical bytes/parsed object with digest checks."""
    schemas = contract.get("recordSchemas") if isinstance(contract, dict) else {}
    result: dict[str, dict[str, Any]] = {}
    records = bundle.get("casOracle")
    if not isinstance(records, list):
        return result
    for i, record in enumerate(records):
        path = f"$bundle.casOracle[{i}]"
        if not isinstance(record, dict):
            continue
        ref = record.get("ref")
        rid = _ref_id(ref)
        bytes_record = record.get("bytes")
        raw = bytes_record.get("canonical") if isinstance(bytes_record, dict) else None
        media = record.get("mediaType")
        if rid is None or not isinstance(raw, str) or not isinstance(media, str):
            continue
        if rid in result:
            relation = "same-id/different-bytes" if result[rid]["canonicalBytes"] != raw \
                else "duplicate CAS entry"
            out.append(("E10", f"{path}: {relation} for {rid}"))
            continue
        if _sha256_ref(raw) != rid:
            out.append(("E10", f"{path}: ContentRef does not equal SHA-256 of retained bytes"))
        kind = ref.get("kind") if isinstance(ref, dict) else None
        parsed: Any = None
        if media == "application/json":
            try:
                parsed = json.loads(raw)
            except (TypeError, ValueError, json.JSONDecodeError) as exc:
                out.append(("E10", f"{path}: canonical JSON bytes do not parse ({exc})"))
            else:
                if _canonical_json(parsed) != raw:
                    out.append(("E10", f"{path}: JSON bytes are not canonical"))
                target_schema = CAS_SCHEMA_BY_KIND.get(kind)
                if target_schema is None:
                    out.append(("E10", f"{path}: no parsed-object schema for kind {kind!r}"))
                else:
                    out.extend(_schema_validate(parsed, target_schema, schemas,
                                                path + ".parsedBytes"))
                    out.extend(_metadata_findings(parsed, path + ".parsedBytes"))
        elif kind not in RAW_CAS_KINDS:
            out.append(("E10", f"{path}: only bundle-signature may use non-JSON bytes"))
        result[rid] = {"kind": kind, "canonicalBytes": raw, "mediaType": media,
                       "parsed": parsed, "record": record}
    return result


def _resolve(ref: Any, expected_kind: str, store: dict[str, dict[str, Any]],
             path: str, out: list[tuple[str, str]], invariant: str = "E10") -> Any:
    rid = _ref_id(ref, expected_kind)
    if rid is None:
        out.append((invariant, f"{path}: expected full {expected_kind} ContentRef"))
        return None
    record = store.get(rid)
    if record is None:
        out.append((invariant, f"{path}: {rid} does not resolve to retained bytes"))
        return None
    if record.get("kind") != expected_kind:
        out.append((invariant, f"{path}: CAS kind {record.get('kind')!r} != "
                               f"{expected_kind!r}"))
        return None
    return record.get("parsed")


def _sorted_unique_strings(values: Any) -> bool:
    return (isinstance(values, list) and all(isinstance(x, str) for x in values)
            and values == sorted(set(values), key=lambda x: x.encode("utf-8")))


def _anchor_key(anchor: Any) -> str:
    return _canonical_json(anchor)


def _proof_obligation_id(ep, predicate_id: str, claim_shape: str,
                         coverage_ref: str) -> str:
    payload = (b"opensip.proof-obligation.v1\x00"
               + ep.frame_component(0x02, predicate_id)
               + ep.frame_component(0x08, claim_shape)
               + ep.frame_component(0x09, coverage_ref))
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _unit_views(bundle: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, list[str]],
                                                  dict[str, str]]:
    """Project typed Evidence units to Phase-1A's canonical unit input shape."""
    units: list[dict[str, Any]] = []
    owners: dict[str, list[str]] = {}
    states: dict[str, str] = {}
    closure = bundle.get("capabilityClosure")
    raw_units = closure.get("units") if isinstance(closure, dict) else []
    if not isinstance(raw_units, list):
        return units, owners, states
    for unit in raw_units:
        if not isinstance(unit, dict):
            continue
        refs_raw = unit.get("objectRefs")
        state_raw = unit.get("objectStates")
        refs = [_ref_id(x) for x in refs_raw] if isinstance(refs_raw, list) else []
        refs = [x for x in refs if x is not None]
        state_entries: list[dict[str, Any]] = []
        if isinstance(state_raw, list):
            for entry in state_raw:
                if not isinstance(entry, dict):
                    continue
                rid = _ref_id(entry.get("ref"))
                if rid is not None and isinstance(entry.get("state"), str):
                    state_entries.append({"ref": rid,
                                          "projectId": entry.get("projectId"),
                                          "state": entry["state"]})
                    states[rid] = entry["state"]
        uid = unit.get("unitId")
        for rid in refs:
            owners.setdefault(rid, []).append(uid if isinstance(uid, str) else "?")
        units.append({"unitId": uid,
                      "projectId": unit.get("projectId"),
                      "runId": unit.get("runId"),
                      "requiredForCapability": unit.get("requiredForCapability"),
                      "objectRefs": [{"ref": rid, "projectId": unit.get("projectId")}
                                     for rid in refs],
                      "objectStates": state_entries})
    return units, owners, states


def _coverage_binding(evaluation: dict[str, Any], store: dict[str, dict[str, Any]],
                      out: list[tuple[str, str]], path: str, project_id: Any) -> bool:
    """Resolve the exact Coverage/predicate/partition join for every claim shape."""
    valid = True
    coverage_ref = evaluation.get("coverageRef")
    coverage_id = _ref_id(coverage_ref, "coverage")
    coverage = _resolve(coverage_ref, "coverage", store, path + ".coverageRef", out, "E4")
    predicate_ref = evaluation.get("predicateSemanticsRef")
    predicate_id = _ref_id(predicate_ref, "predicate-semantics")
    semantics = _resolve(predicate_ref, "predicate-semantics", store,
                         path + ".predicateSemanticsRef", out, "E4")
    if evaluation.get("coverageId") != coverage_id:
        out.append(("E4", f"{path}.coverageId: must equal coverageRef.id exactly"))
        valid = False
    if not isinstance(coverage, dict) or not isinstance(semantics, dict):
        return False
    partition_ref = coverage.get("factPartitionRef")
    partition = _resolve(partition_ref, "fact-partition", store,
                         path + ".coverage.factPartitionRef", out, "E4")
    if not isinstance(partition, dict):
        return False
    if coverage.get("projectId") != project_id or partition.get("projectId") != project_id:
        out.append(("E4", f"{path}: Coverage/fact partition crosses ProjectId"))
        valid = False
    if _ref_id(coverage.get("predicateSemanticsRef"), "predicate-semantics") != predicate_id:
        out.append(("E4", f"{path}: Coverage substitutes predicateSemanticsRef"))
        valid = False
    if semantics.get("predicateId") != evaluation.get("predicateId"):
        out.append(("E4", f"{path}: predicate semantics identity substitution"))
        valid = False
    requirement = coverage.get("verificationRequirement")
    if requirement != semantics.get("verificationRequirement"):
        out.append(("E4", f"{path}: Coverage requirement differs from predicate semantics"))
        valid = False
    entries = partition.get("entries")
    subjects: list[str] = []
    if not isinstance(entries, list):
        return False
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict) or not isinstance(entry.get("subjectId"), str):
            valid = False
            continue
        subjects.append(entry["subjectId"])
        refs = entry.get("factRefs")
        if isinstance(refs, list):
            for j, fact_ref in enumerate(refs):
                if _resolve(fact_ref, "fact", store,
                            f"{path}.coverage.partition.entries[{i}].factRefs[{j}]",
                            out, "E4") is None:
                    valid = False
    if subjects != sorted(set(subjects), key=lambda x: x.encode("utf-8")):
        out.append(("E4", f"{path}: fact partition subjects are not canonical unique"))
        valid = False
    covered = coverage.get("coveredSubjectIds")
    domain = requirement.get("subjectDomain") if isinstance(requirement, dict) else None
    if not _sorted_unique_strings(covered) or not _sorted_unique_strings(domain):
        out.append(("E4", f"{path}: Coverage/requirement domain is not canonical unique"))
        valid = False
    if covered != domain or covered != subjects:
        out.append(("E4", f"{path}: covered, required, and partition subject domains differ"))
        valid = False
    return valid


def _coverage_analysis(evaluation: dict[str, Any], store: dict[str, dict[str, Any]], ep,
                       out: list[tuple[str, str]], path: str,
                       project_id: Any) -> tuple[list[str], bool]:
    """Resolve and derive exact no-match Coverage; trust no completeness boolean."""
    coverage_ref = evaluation.get("coverageRef")
    coverage_id = _ref_id(coverage_ref, "coverage")
    coverage = _resolve(coverage_ref, "coverage", store, path + ".coverageRef", out, "E4")
    predicate_ref = evaluation.get("predicateSemanticsRef")
    predicate_id = _ref_id(predicate_ref, "predicate-semantics")
    semantics = _resolve(predicate_ref, "predicate-semantics", store,
                         path + ".predicateSemanticsRef", out, "E4")
    proof = evaluation.get("proof") if isinstance(evaluation.get("proof"), dict) else {}
    partition_ref = proof.get("factPartitionRef")
    partition_id = _ref_id(partition_ref, "fact-partition")
    partition = _resolve(partition_ref, "fact-partition", store,
                         path + ".proof.factPartitionRef", out, "E4")
    complete = True
    if evaluation.get("coverageId") != coverage_id:
        out.append(("E4", f"{path}.coverageId: must equal coverageRef.id exactly"))
        complete = False
    if not all(isinstance(x, dict) for x in (coverage, semantics, partition)):
        return [], False
    if coverage.get("projectId") != project_id or partition.get("projectId") != project_id:
        out.append(("E4", f"{path}: Coverage crosses ProjectId"))
        complete = False
    if _ref_id(coverage.get("predicateSemanticsRef"), "predicate-semantics") != predicate_id:
        out.append(("E4", f"{path}: Coverage substitutes predicateSemanticsRef"))
        complete = False
    if _ref_id(coverage.get("factPartitionRef"), "fact-partition") != partition_id:
        out.append(("E4", f"{path}: Coverage substitutes factPartitionRef"))
        complete = False
    requirement = coverage.get("verificationRequirement")
    semantic_requirement = semantics.get("verificationRequirement")
    if requirement != semantic_requirement:
        out.append(("E4", f"{path}: Coverage requirement differs from predicate semantics"))
        complete = False
    if semantics.get("predicateId") != evaluation.get("predicateId"):
        out.append(("E4", f"{path}: predicate semantics identity substitution"))
        complete = False

    entries = partition.get("entries")
    entry_subjects: list[str] = []
    if isinstance(entries, list):
        for i, entry in enumerate(entries):
            if not isinstance(entry, dict) or not isinstance(entry.get("subjectId"), str):
                complete = False
                continue
            entry_subjects.append(entry["subjectId"])
            refs = entry.get("factRefs")
            if isinstance(refs, list):
                for j, ref in enumerate(refs):
                    _resolve(ref, "fact", store,
                             f"{path}.partition.entries[{i}].factRefs[{j}]", out, "E4")
        if entry_subjects != sorted(set(entry_subjects), key=lambda x: x.encode("utf-8")):
            out.append(("E4", f"{path}: fact partition entries are not canonical unique order"))
            complete = False
    else:
        complete = False
    covered = coverage.get("coveredSubjectIds")
    domain = requirement.get("subjectDomain") if isinstance(requirement, dict) else None
    if not _sorted_unique_strings(covered):
        out.append(("E4", f"{path}: Coverage coveredSubjectIds not canonical unique"))
        complete = False
    if not _sorted_unique_strings(domain):
        out.append(("E4", f"{path}: verificationRequirement subjectDomain not canonical unique"))
        complete = False
    if covered != domain or covered != entry_subjects:
        out.append(("E4", f"{path}: covered domain, required domain and partition subjects "
                          "must be exactly equal"))
        complete = False
    if not isinstance(requirement, dict) or requirement.get("completeness") != "complete":
        out.append(("E4", f"{path}: authoritative no-match requires complete domain"))
        complete = False
    if isinstance(semantics.get("expression"), dict) \
            and semantics["expression"].get("operator") != "none":
        out.append(("E4", f"{path}: no-match semantics must use the declarative none operator"))
        complete = False

    if entry_subjects:
        try:
            want = ep.commit("subject-set", [ep.encode_subject(x) for x in entry_subjects])
            if proof.get("subjectSetCommitment") != want:
                out.append(("E4", f"{path}.proof.subjectSetCommitment: does not recompute "
                                  "from resolved fact partition"))
                complete = False
        except Exception as exc:
            out.append(("E4", f"{path}: subject commitment derivation failed ({exc})"))
            complete = False
    if proof.get("subjectCount") != len(entry_subjects):
        out.append(("E4", f"{path}.proof.subjectCount: does not equal derived subject set"))
        complete = False
    return entry_subjects, complete


def _relationship_analysis(evaluation: dict[str, Any], store: dict[str, dict[str, Any]],
                           out: list[tuple[str, str]], path: str) -> None:
    proof = evaluation.get("proof") if isinstance(evaluation.get("proof"), dict) else {}
    semantics = _resolve(proof.get("relationSemanticsRef"), "relation-semantics", store,
                         path + ".proof.relationSemanticsRef", out, "E2")
    edges = proof.get("witnessEdges")
    if not isinstance(edges, list) or not edges:
        out.append(("E2", f"{path}: relationship proof requires a non-empty ordered edge list"))
        return
    edge_keys: list[str] = []
    fact_ref_ids: list[str] = []
    for i, edge in enumerate(edges):
        epath = f"{path}.proof.witnessEdges[{i}]"
        if not isinstance(edge, dict):
            continue
        relation_kind = edge.get("relationKind")
        if isinstance(semantics, dict) and relation_kind not in semantics.get("allowedKinds", []):
            out.append(("E2", f"{epath}.relationKind: outside resolved relation semantics"))
        fact_id = _ref_id(edge.get("factRef"), "fact")
        fact_ref_ids.append(fact_id or "")
        fact = _resolve(edge.get("factRef"), "fact", store, epath + ".factRef", out, "E2")
        if isinstance(fact, dict):
            for key in ("factId", "fromSubjectId", "toSubjectId", "relationKind", "anchors"):
                if edge.get(key) != fact.get(key):
                    out.append(("E2", f"{epath}.{key}: differs from resolved fact bytes"))
        anchors = edge.get("anchors")
        if not isinstance(anchors, list) or not anchors:
            out.append(("E2", f"{epath}.anchors: requires non-empty canonical anchors"))
        elif [_anchor_key(x) for x in anchors] != sorted(set(_anchor_key(x) for x in anchors)):
            out.append(("E2", f"{epath}.anchors: must be sorted and unique"))
        edge_keys.append(_canonical_json(edge))
    if edge_keys != sorted(set(edge_keys)):
        out.append(("E2", f"{path}.proof.witnessEdges: must be canonical ordered and unique"))
    proof_refs = [_ref_id(x, "fact") for x in proof.get("factRefs", [])] \
        if isinstance(proof.get("factRefs"), list) else []
    if sorted(proof_refs) != sorted(fact_ref_ids) or any(x is None for x in proof_refs):
        out.append(("E2", f"{path}.proof.factRefs: must exactly name the edge facts"))


def _derived_dependency_edges(bundle: dict[str, Any], store: dict[str, dict[str, Any]],
                              versioning: dict[str, Any],
                              out: list[tuple[str, str]]) -> list[dict[str, Any]]:
    project_id = bundle.get("projectId")
    edges: list[dict[str, Any]] = []

    def add(source: str | None, target: str | None, role: str, path: str) -> None:
        if source is None or target is None:
            out.append(("E7", f"{path}: dependency endpoint is not a full ContentRef"))
            return
        edges.append({"fromRef": source, "toRef": target,
                      "projectId": project_id, "role": role})

    manifests = ((versioning.get("historicalSemanticsPolicy") or {})
                 .get("trustedVerifierManifest", [])) if isinstance(versioning, dict) else []
    signature_by_verifier: dict[str, str] = {}
    if isinstance(manifests, list):
        for manifest in manifests:
            if not isinstance(manifest, dict):
                continue
            aid = _ref_id(manifest.get("verifierArtifactRef"), "verifier-artifact")
            sid = _ref_id(manifest.get("signatureRef"), "bundle-signature")
            if aid and sid:
                signature_by_verifier[aid] = sid

    for rid, record in store.items():
        obj, kind = record.get("parsed"), record.get("kind")
        if not isinstance(obj, dict):
            continue
        if kind == "coverage":
            add(rid, _ref_id(obj.get("factPartitionRef"), "fact-partition"),
                "coverage-fact-partition", f"CAS[{rid}]")
            add(rid, _ref_id(obj.get("predicateSemanticsRef"), "predicate-semantics"),
                "coverage-predicate-semantics", f"CAS[{rid}]")
        elif kind == "fact-partition":
            entries = obj.get("entries")
            if isinstance(entries, list):
                for entry in entries:
                    if not isinstance(entry, dict) or not isinstance(entry.get("factRefs"), list):
                        continue
                    for ref in entry["factRefs"]:
                        add(rid, _ref_id(ref, "fact"), "partition-fact", f"CAS[{rid}]")
        elif kind == "predicate-semantics":
            add(rid, _ref_id(obj.get("verifierArtifactRef"), "verifier-artifact"),
                "predicate-verifier", f"CAS[{rid}]")
        elif kind == "policy-semantics":
            add(rid, _ref_id(obj.get("verifierArtifactRef"), "verifier-artifact"),
                "policy-verifier", f"CAS[{rid}]")
        elif kind == "verifier-artifact":
            add(rid, signature_by_verifier.get(rid), "verifier-signature", f"CAS[{rid}]")
        elif kind == "fact":
            anchors = obj.get("anchors")
            if isinstance(anchors, list):
                for anchor in anchors:
                    if isinstance(anchor, dict) and anchor.get("kind") == "fact-ref":
                        add(rid, _ref_id(anchor.get("factRef"), "fact"), "fact-anchor",
                            f"CAS[{rid}]")
        elif kind == "replay-closure":
            deps = obj.get("dependencyRefs")
            if isinstance(deps, list):
                for ref in deps:
                    target = _ref_id(ref)
                    add(rid, target, "replay-input", f"CAS[{rid}]")
    canonical = sorted(edges, key=lambda x: (x["fromRef"], x["toRef"], x["role"]))
    if len(canonical) != len({(x["fromRef"], x["toRef"], x["role"])
                              for x in canonical}):
        out.append(("E7", "derived dependency graph contains duplicate edges"))
    for i, edge in enumerate(canonical):
        if edge["toRef"] not in store:
            out.append(("E7", f"dependencyEdges[{i}]: target has no CAS bytes"))
    return canonical


def _declared_dependency_edges(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    closure = bundle.get("capabilityClosure")
    raw = closure.get("dependencyEdges") if isinstance(closure, dict) else None
    if not isinstance(raw, list):
        return []
    clean = [x for x in raw if isinstance(x, dict)]
    return sorted(clean, key=lambda x: (str(x.get("fromRef")), str(x.get("toRef")),
                                        str(x.get("role"))))


def _ep_projection(bundle: dict[str, Any], store: dict[str, dict[str, Any]], ep,
                   coverage_status: str) -> dict[str, Any]:
    project_id = bundle.get("projectId")
    direct: dict[str, str] = {}
    evaluations_out: list[dict[str, Any]] = []

    def add_ref(ref: Any, kind: str) -> str | None:
        rid = _ref_id(ref, kind)
        if rid is not None:
            direct[rid] = kind
        return rid

    for evaluation in bundle.get("activatedEvaluations", []) \
            if isinstance(bundle.get("activatedEvaluations"), list) else []:
        if not isinstance(evaluation, dict):
            continue
        pred = add_ref(evaluation.get("predicateSemanticsRef"), "predicate-semantics")
        cov = add_ref(evaluation.get("coverageRef"), "coverage")
        proof = evaluation.get("proof") if isinstance(evaluation.get("proof"), dict) else {}
        shape = evaluation.get("claimShape")
        projected_proof: dict[str, Any] = {"kind": proof.get("kind")}
        if shape == "local-match":
            projected_proof.update(subjectId=proof.get("subjectId"),
                                   factRefs=[add_ref(x, "fact") for x in proof.get("factRefs", [])]
                                   if isinstance(proof.get("factRefs"), list) else [])
        elif shape == "relationship-match":
            projected_proof.update(
                relationSemanticsRef=add_ref(proof.get("relationSemanticsRef"),
                                             "relation-semantics"),
                factRefs=[add_ref(x, "fact") for x in proof.get("factRefs", [])]
                         if isinstance(proof.get("factRefs"), list) else [],
                witnessEdges=[{
                    "fromSubjectId": x.get("fromSubjectId"),
                    "toSubjectId": x.get("toSubjectId"),
                    "relationKind": x.get("relationKind"),
                    "factRef": add_ref(x.get("factRef"), "fact"),
                } for x in proof.get("witnessEdges", []) if isinstance(x, dict)]
                         if isinstance(proof.get("witnessEdges"), list) else [],
            )
        elif shape == "aggregate-match":
            projected_proof.update(
                memberSetCommitment=proof.get("memberSetCommitment"),
                memberCount=proof.get("memberCount"),
                factPartitionRef=add_ref(proof.get("factPartitionRef"), "fact-partition"),
                foldSpec=proof.get("foldSpec"),
                factRefs=[add_ref(x, "fact") for x in proof.get("factRefs", [])]
                         if isinstance(proof.get("factRefs"), list) else [],
            )
        elif shape == "no-match":
            projected_proof.update(
                subjectSetCommitment=proof.get("subjectSetCommitment"),
                subjectCount=proof.get("subjectCount"),
                factPartitionRef=add_ref(proof.get("factPartitionRef"), "fact-partition"),
            )
        elif isinstance(shape, str) and shape in {"indeterminate", "error"}:
            projected_proof.update(reasonRef=add_ref(proof.get("reasonRef"), "reason"))
            if "partialSubjectCount" in proof:
                projected_proof["partialSubjectCount"] = proof["partialSubjectCount"]
            if isinstance(proof.get("factRefs"), list):
                projected_proof["factRefs"] = [add_ref(x, "fact") for x in proof["factRefs"]]
        evaluations_out.append({
            "evaluationId": evaluation.get("evaluationId"),
            "predicateId": evaluation.get("predicateId"),
            "outcome": evaluation.get("outcome"),
            "claimShape": shape,
            "predicateSemanticsRef": pred,
            "coverageRef": cov,
            "proof": projected_proof,
        })

    vd = bundle.get("verdictDerivation") if isinstance(bundle.get("verdictDerivation"), dict) else {}
    verdict_cov = add_ref(vd.get("coverageRef"), "coverage")
    policy_ref = _ref_id(vd.get("policyRef"), "policy-semantics")
    if policy_ref is not None:
        direct[policy_ref] = "policy"
    baseline_in = vd.get("baseline")
    if isinstance(baseline_in, dict) and baseline_in.get("kind") == "comparison":
        baseline = {"kind": "comparison",
                    "baselineRef": add_ref(baseline_in.get("baselineRef"), "baseline"),
                    "projectId": project_id,
                    "matchedMembers": baseline_in.get("matchedMembers")}
    else:
        baseline = {"kind": "none"}
    waivers = []
    for waiver in vd.get("waivers", []) if isinstance(vd.get("waivers"), list) else []:
        if not isinstance(waiver, dict):
            continue
        waivers.append({"waiverId": waiver.get("waiverId"),
                        "waiverRef": add_ref(waiver.get("waiverRef"), "waiver"),
                        "projectId": project_id,
                        "target": waiver.get("target"),
                        "disposition": waiver.get("disposition")})
    replay_refs = []
    replay = bundle.get("replayClosure")
    if isinstance(replay, dict) and isinstance(replay.get("objects"), list):
        for obj in replay["objects"]:
            if isinstance(obj, dict):
                rid = add_ref(obj.get("ref"), "replay-closure")
                replay_refs.append({"ref": rid, "projectId": project_id})

    partition_records = []
    for rid, kind in direct.items():
        if kind != "fact-partition" or rid not in store:
            continue
        obj = store[rid].get("parsed")
        entries = obj.get("entries") if isinstance(obj, dict) else []
        partition_records.append({"partitionRef": rid, "projectId": project_id,
                                  "members": [x.get("subjectId") for x in entries
                                              if isinstance(x, dict)]
                                  if isinstance(entries, list) else []})
    object_store = [{"ref": rid, "projectId": project_id, "kind": kind,
                     "dependencies": []}
                    for rid, kind in sorted(direct.items()) if rid in store]
    projection = {
        "schemaVersion": 2,
        "projectId": project_id,
        "runId": bundle.get("runId"),
        "objectStore": object_store,
        "partitionContents": partition_records,
        "requiredUniverse": copy.deepcopy(bundle.get("requiredUniverse")),
        "evaluations": evaluations_out,
        "replayClosureRefs": replay_refs,
        "verdictProof": {
            "verdict": bundle.get("verdict"),
            "outcomeSetCommitment": vd.get("outcomeSetCommitment"),
            "coverage": {"status": coverage_status,
                         "coverageRef": verdict_cov, "projectId": project_id},
            "baseline": baseline,
            "waivers": waivers,
            "waiverSetCommitment": vd.get("waiverSetCommitment"),
            "policy": {
                "policyRef": policy_ref,
                "projectId": project_id,
                "semanticsVersion": "policy-ir-1",
                "matchDisposition": "fail-unless-baselined-or-waived",
                "baselineDisposition": "advisory",
                "waivedDisposition": "ignored",
                "noMatchDisposition": "pass",
                "incompleteDisposition": "indeterminate",
            },
            "derivationCommitment": vd.get("derivationCommitment"),
        },
    }
    return projection


def _retention_projection(projection: dict[str, Any], store: dict[str, dict[str, Any]],
                          edges: list[dict[str, Any]]) -> dict[str, Any]:
    result = copy.deepcopy(projection)
    project_id = result.get("projectId")
    edge_by_source: dict[str, list[dict[str, Any]]] = {}
    for edge in edges:
        edge_by_source.setdefault(edge["fromRef"], []).append({
            "ref": edge["toRef"], "projectId": edge["projectId"], "role": edge["role"]})
    kind_map = {"bundle-signature": "reason", "verifier-artifact": "reason",
                "policy-semantics": "policy"}
    result["objectStore"] = [{
        "ref": rid,
        "projectId": project_id,
        "kind": kind_map.get(record.get("kind"), record.get("kind")),
        "dependencies": sorted(edge_by_source.get(rid, []),
                               key=lambda x: (x["ref"], x["role"])),
    } for rid, record in sorted(store.items())]
    return result


def _dependency_context():
    ep = _load_module("check-evaluation-proof.py", "opensip_check_evaluation_proof_v2")
    rt = _load_module("check-retention-custody.py", "opensip_check_retention_v7")
    ver = _load_module("check-versioning.py", "opensip_check_versioning_v3")
    proof = json.loads((HERE / PROOF).read_text())
    retention = json.loads((HERE / RETENTION).read_text())
    versioning = json.loads((HERE / VERSIONING).read_text())
    return ep, rt, ver, proof, retention, versioning


def _validate_impl(bundle: Any, contract: dict[str, Any], deps) -> list[tuple[str, str]]:
    ep, rt, ver, proof_contract, retention_contract, versioning_contract = deps
    schemas = contract.get("recordSchemas") if isinstance(contract, dict) else {}
    out = _schema_validate(bundle, "EvidenceBundle", schemas)
    out.extend(_metadata_findings(bundle))
    if not isinstance(bundle, dict):
        return out

    store = _cas(bundle, contract, out)
    project_id = bundle.get("projectId")
    units, owners, states = _unit_views(bundle)

    # E6: resolved storage admission is typed by the schema and semantically non-empty.
    admission = bundle.get("storageAdmission")
    if isinstance(admission, dict):
        for field in ("storageRoot", "privacyClass", "retentionPolicy"):
            if not isinstance(admission.get(field), str) or not admission[field]:
                out.append(("E6", f"$bundle.storageAdmission.{field}: unresolved"))

    evaluations_raw = bundle.get("activatedEvaluations")
    evaluations = evaluations_raw if isinstance(evaluations_raw, list) else []
    keys: list[tuple[str, str]] = []
    coverage_complete = True
    for i, evaluation in enumerate(evaluations):
        path = f"$bundle.activatedEvaluations[{i}]"
        if not isinstance(evaluation, dict):
            continue
        eid, pid = evaluation.get("evaluationId"), evaluation.get("predicateId")
        if isinstance(eid, str) and isinstance(pid, str):
            keys.append((eid, pid))
        outcome, shape = evaluation.get("outcome"), evaluation.get("claimShape")
        if isinstance(shape, str) and shape in PAIRING and outcome != PAIRING[shape]:
            out.append(("E2", f"{path}: outcome {outcome!r} is incoherent with "
                              f"claimShape {shape!r}"))
        proof_value = evaluation.get("proof")
        if isinstance(proof_value, dict) and isinstance(shape, str) and shape in PROOF_TAGS \
                and proof_value.get("kind") != PROOF_TAGS[shape]:
            out.append(("E2", f"{path}.proof.kind: wrong tagged-union variant"))
        cov_id = _ref_id(evaluation.get("coverageRef"), "coverage")
        if isinstance(pid, str) and isinstance(shape, str) and cov_id is not None:
            try:
                obligation = _proof_obligation_id(ep, pid, shape, cov_id)
                if evaluation.get("proofObligationId") != obligation:
                    out.append(("E3", f"{path}.proofObligationId: host derivation differs"))
            except Exception as exc:
                out.append(("E3", f"{path}: proof-obligation derivation failed ({exc})"))
        if shape == "no-match":
            subjects, complete = _coverage_analysis(evaluation, store, ep, out, path,
                                                    project_id)
            coverage_complete = coverage_complete and complete and bool(subjects)
        else:
            _coverage_binding(evaluation, store, out, path, project_id)
        if shape == "relationship-match":
            _relationship_analysis(evaluation, store, out, path)
        elif shape == "local-match":
            proof_value = proof_value if isinstance(proof_value, dict) else {}
            refs = proof_value.get("factRefs")
            if not isinstance(refs, list) or not refs:
                out.append(("E2", f"{path}: local match needs at least one fact"))
            elif isinstance(refs, list):
                for j, ref in enumerate(refs):
                    _resolve(ref, "fact", store, f"{path}.proof.factRefs[{j}]", out, "E2")
        elif isinstance(shape, str) and shape in {"indeterminate", "error"}:
            proof_value = proof_value if isinstance(proof_value, dict) else {}
            _resolve(proof_value.get("reasonRef"), "reason", store,
                     f"{path}.proof.reasonRef", out, "E2")

    # E1: reject duplicate keys before applying the set commitment grammar.
    if len(keys) != len(set(keys)):
        out.append(("E1", "$bundle.activatedEvaluations: duplicate evaluationId/predicateId "
                          "key (including same-key/different-outcome)"))
    universe = bundle.get("requiredUniverse")
    if isinstance(universe, dict):
        canonical_members = [{"evaluationId": e, "predicateId": p}
                             for e, p in sorted(set(keys), key=lambda x: ep.encode_member(*x))]
        if universe.get("memberIds") != canonical_members:
            out.append(("E1", "$bundle.requiredUniverse.memberIds: must exactly equal the "
                              "canonical activated member set"))
        if universe.get("declaredCount") != len(keys):
            out.append(("E1", "$bundle.requiredUniverse.declaredCount: disagrees with "
                              "activated evaluations"))
        try:
            wanted = ep.commit("universe", [ep.encode_member(e, p) for e, p in keys])
            if universe.get("universeCommitment") != wanted:
                out.append(("E1", "$bundle.requiredUniverse.universeCommitment: does not "
                                  "recompute under evaluation-proof.v2"))
        except Exception as exc:
            out.append(("E1", f"$bundle.requiredUniverse: commitment failed ({exc})"))
    if bundle.get("authoritative") is True and bundle.get("verdict") == "pass" and not keys:
        out.append(("E1", "authoritative pass cannot have an empty required universe"))

    vd = bundle.get("verdictDerivation")
    if isinstance(vd, dict):
        cov_id = _ref_id(vd.get("coverageRef"), "coverage")
        eval_covs = {_ref_id(x.get("coverageRef"), "coverage") for x in evaluations
                     if isinstance(x, dict)}
        if cov_id is None or cov_id not in eval_covs:
            out.append(("E11", "$bundle.verdictDerivation.coverageRef: not an exact "
                               "activated Coverage identity"))
        _resolve(vd.get("coverageRef"), "coverage", store,
                 "$bundle.verdictDerivation.coverageRef", out, "E11")
        _resolve(vd.get("policyRef"), "policy-semantics", store,
                 "$bundle.verdictDerivation.policyRef", out, "E11")
        waivers = vd.get("waivers")
        if isinstance(waivers, list):
            for i, waiver in enumerate(waivers):
                if isinstance(waiver, dict):
                    _resolve(waiver.get("waiverRef"), "waiver", store,
                             f"$bundle.verdictDerivation.waivers[{i}].waiverRef", out, "E11")

    projection = _ep_projection(bundle, store, ep,
                                "complete" if coverage_complete else "incomplete")
    try:
        ep_hits = ep.validate_bundle(projection)
    except Exception as exc:
        ep_hits = [("EP-TOTALITY", f"cross-lane validator raised {type(exc).__name__}: {exc}")]
    ep_map = {"EP-10": "E1", "EP-1": "E2", "EP-2": "E2", "EP-3": "E11",
              "EP-4": "E4", "EP-5": "E5", "EP-6": "E11", "EP-7": "E9",
              "EP-8": "E5", "EP-9": "E10", "EP-11": "E-SCHEMA-TOTAL",
              "EP-TOTALITY": "E-SCHEMA-TOTAL"}
    for code, message in ep_hits:
        out.append((ep_map.get(code, "E5"), f"evaluation-proof.v2/{code}: {message}"))
    try:
        if isinstance(vd, dict) and vd.get("derivationCommitment") \
                != ep.derive_verdict_commitment(projection):
            out.append(("E5", "$bundle.verdictDerivation.derivationCommitment: does not "
                              "recompute through evaluation-proof.v2"))
        derived_verdict = ep.derive_verdict(projection)
        if bundle.get("verdict") != derived_verdict:
            out.append(("E5", f"$bundle.verdict: asserted {bundle.get('verdict')!r}, "
                              f"evaluation-proof.v2 derives {derived_verdict!r}"))
    except Exception as exc:
        out.append(("E5", f"$bundle.verdictDerivation: derivation failed ({exc})"))
    if bundle.get("verdict") == "pass" and any(
            isinstance(e, dict) and e.get("outcome") in {"indeterminate", "error"}
            for e in evaluations):
        out.append(("E9", "indeterminate/error outcome cannot be absorbed into pass"))

    # E7: Evidence resolves bytes into typed edges; Phase1A alone propagates minima.
    edges = _derived_dependency_edges(bundle, store, versioning_contract, out)
    declared_edges = _declared_dependency_edges(bundle)
    if declared_edges != edges:
        out.append(("E7", "$bundle.capabilityClosure.dependencyEdges: must exactly equal "
                          "the CAS-derived typed dependency graph"))
    requirements: dict[str, str] = {}
    retention_projection = _retention_projection(projection, store, edges)
    try:
        requirements = ep.derive_proof_requirements(projection, edges)
    except Exception as exc:
        out.append(("E7", f"evaluation-proof.v2 transitive requirement derivation "
                          f"rejected: {exc}"))
    closure = bundle.get("capabilityClosure")
    declared_refs = closure.get("proofReferences") if isinstance(closure, dict) else None
    wanted_refs = [{"ref": ref, "projectId": project_id,
                    "neededAtCapability": capability}
                   for ref, capability in sorted(requirements.items())]
    if declared_refs != wanted_refs:
        out.append(("E7", "$bundle.capabilityClosure.proofReferences: must exactly equal "
                          "Phase1A-derived minimum-capability references"))
    if set(requirements) != set(store):
        out.append(("E7", "CAS oracle must equal the reachable proof dependency closure; "
                          f"missing={sorted(set(requirements)-set(store))}, "
                          f"injected={sorted(set(store)-set(requirements))}"))

    closure_input = {
        "schemaVersion": 1,
        "projectId": project_id,
        "runId": bundle.get("runId"),
        "sealedCapability": bundle.get("sealedCapability"),
        "proofRefs": [{"ref": x["ref"], "projectId": x["projectId"],
                       "requiredForCapability": x["neededAtCapability"]}
                      for x in wanted_refs],
        "dependencyEdges": edges,
        "units": units,
        "closureCommitment": closure.get("closureCommitment")
        if isinstance(closure, dict) else None,
        "expectedEffectiveCapability": bundle.get("effectiveCapability"),
    }
    validate_closure = getattr(rt, "validate_capability_closure", None)
    effective_fn = getattr(rt, "derive_effective_capability", None)
    closure_fn = getattr(rt, "closure_commitment", None)
    if not all(callable(x) for x in (validate_closure, effective_fn, closure_fn)):
        out.append(("E7", "retention-tiers.v7 canonical closure/effective APIs unavailable"))
    else:
        try:
            retention_hits = validate_closure(retention_projection, closure_input)
            for code, message in retention_hits:
                out.append(("E12" if code in {"RC-12", "RC-13"} else "E7",
                            f"retention-tiers.v7/{code}: {message}"))
        except Exception as exc:
            out.append(("E7", f"retention-tiers.v7 closure validation rejected: {exc}"))
        try:
            wanted_closure = closure_fn(units)
            if not isinstance(closure, dict) or closure.get("closureCommitment") != wanted_closure:
                out.append(("E7", "capability closure commitment does not recompute through "
                                  "retention-tiers.v7"))
        except Exception as exc:
            out.append(("E7", f"retention-tiers.v7 closure commitment failed: {exc}"))
        try:
            effective = effective_fn(bundle.get("sealedCapability"), units)
            if bundle.get("effectiveCapability") != effective:
                out.append(("E12", f"effectiveCapability {bundle.get('effectiveCapability')!r} "
                                   f"!= retention-tiers.v7 derivation {effective!r}; "
                                   "sealedCapability remains immutable"))
        except Exception as exc:
            out.append(("E12", f"retention-tiers.v7 effective derivation failed: {exc}"))

    # Object-state representation must be total and exactly cover each unit.
    for i, unit in enumerate(units):
        refs = [x.get("ref") for x in unit.get("objectRefs", [])
                if isinstance(x, dict)] if isinstance(unit.get("objectRefs"), list) else []
        state_refs = [x.get("ref") for x in unit.get("objectStates", [])
                      if isinstance(x, dict)] \
            if isinstance(unit.get("objectStates"), list) else []
        if set(refs) != set(state_refs) or len(refs) != len(state_refs):
            out.append(("E12", f"$bundle.capabilityClosure.units[{i}]: objectStates must "
                               "map each unit ref exactly once"))

    # E11 consumes the VERSIONING v3 decision for predicate and policy semantics.
    runtime = bundle.get("verifierRuntime")
    abis = runtime.get("supportedVerifierAbis") if isinstance(runtime, dict) else []
    default_major = runtime.get("defaultIrMajor") if isinstance(runtime, dict) else None
    available_refs = sorted(rid for rid in store if states.get(rid) == "AVAILABLE")
    semantic_refs: list[tuple[str, str]] = []
    for evaluation in evaluations:
        if isinstance(evaluation, dict):
            rid = _ref_id(evaluation.get("predicateSemanticsRef"), "predicate-semantics")
            if rid:
                semantic_refs.append(("predicate", rid))
    if isinstance(vd, dict):
        rid = _ref_id(vd.get("policyRef"), "policy-semantics")
        if rid:
            semantic_refs.append(("policy", rid))
    hist_policy = versioning_contract.get("historicalSemanticsPolicy") \
        if isinstance(versioning_contract, dict) else None
    decide = getattr(ver, "_historical_decision", None)
    if not isinstance(hist_policy, dict) or not callable(decide):
        out.append(("E11", "VERSIONING v3 historical-semantics decision API unavailable"))
    else:
        for semantics_kind, rid in sorted(set(semantic_refs)):
            obj = store.get(rid, {}).get("parsed")
            if not isinstance(obj, dict):
                continue
            verifier_ref = obj.get("verifierArtifactRef")
            fixture = {
                "id": f"evidence-{rid}",
                "binding": {
                    "semanticsKind": semantics_kind,
                    "scope": "trusted-bundled-declarative-v1",
                    "irFamily": obj.get("irFamily"),
                    "irMajor": obj.get("irMajor"),
                    "verifierAbi": obj.get("verifierAbi"),
                    "semanticsRef": {"kind": "predicate-semantics" if semantics_kind == "predicate" else "policy-semantics", "id": rid},
                    "verifierArtifactRef": verifier_ref,
                },
                "availableRefs": available_refs,
                "hostDefaultIrMajor": default_major,
                "hostSupportedVerifierAbis": abis,
                "sealedRunId": bundle.get("runId"),
                "observedRunId": bundle.get("runId"),
                "sealedCapability": bundle.get("sealedCapability"),
                "observedSealedCapability": bundle.get("sealedCapability"),
            }
            decision = decide(hist_policy, fixture)
            if decision.get("capabilityDependencyState") != "AVAILABLE":
                out.append(("E11", f"historical semantics {rid} unavailable: "
                                   f"{decision.get('reason')}"))

    # E8 replay closure: no truthy flag; derive local resolution and ownership.
    replay = bundle.get("replayClosure")
    if bundle.get("effectiveCapability") == "replayable":
        if not isinstance(replay, dict):
            out.append(("E8", "effective replayable capability requires ReplayClosure"))
        else:
            objects = replay.get("objects")
            if not isinstance(objects, list) or not objects:
                out.append(("E8", "ReplayClosure.objects must be non-empty"))
            else:
                seen: set[str] = set()
                for i, obj in enumerate(objects):
                    path = f"$bundle.replayClosure.objects[{i}]"
                    if not isinstance(obj, dict):
                        continue
                    rid = _ref_id(obj.get("ref"), "replay-closure")
                    if rid is None:
                        out.append(("E8", f"{path}.ref: malformed/truncated replay ref"))
                        continue
                    if rid in seen:
                        out.append(("E8", f"{path}.ref: duplicate replay object"))
                    seen.add(rid)
                    if rid not in store:
                        out.append(("E8", f"{path}.ref: bytes unavailable"))
                    holders = owners.get(rid, [])
                    if len(holders) != 1 or holders[0] != obj.get("unitId"):
                        out.append(("E8", f"{path}: must map to exactly its declared unit"))
                    if states.get(rid) != "AVAILABLE":
                        out.append(("E8", f"{path}: replay unit is not AVAILABLE"))
    return out


def validate(bundle: Any, contract: dict[str, Any], deps=None) -> list[tuple[str, str]]:
    """Total public entry point. Any successfully parsed JSON value returns findings."""
    try:
        return _validate_impl(bundle, contract, deps or _dependency_context())
    except Exception as exc:
        return [("E-SCHEMA-TOTAL", f"$bundle: controlled validation failure "
                                   f"{type(exc).__name__}: {exc}")]


def _schema_audit(contract: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    schemas = contract.get("recordSchemas")
    if not isinstance(schemas, dict) or not schemas:
        return ["E-SCHEMA: named recordSchemas registry missing"]
    referenced: set[str] = {"EvidenceBundle", *CAS_SCHEMA_BY_KIND.values()}
    for name, schema in schemas.items():
        if not isinstance(schema, dict):
            findings.append(f"E-SCHEMA: schema {name!r} is not an object")
            continue
        kind = schema.get("kind")
        for required_key in ("typeOutcome", "constraintOutcome"):
            if not isinstance(schema.get(required_key), str):
                findings.append(f"E-SCHEMA: schema {name} lacks {required_key}")
        if kind == "object":
            if schema.get("closed") is not True or schema.get("additionalProperties") is not False:
                findings.append(f"E-SCHEMA: object schema {name} is not closed")
            for key in ("required", "optional", "forbiddenFields"):
                if not isinstance(schema.get(key), list) or any(
                        not isinstance(x, str) for x in schema.get(key, [])):
                    findings.append(f"E-SCHEMA: {name}.{key} is not an exact string array")
            required = set(schema.get("required", []))
            optional = set(schema.get("optional", []))
            forbidden = set(schema.get("forbiddenFields", []))
            if required & optional or required & forbidden or optional & forbidden:
                findings.append(f"E-SCHEMA: {name} required/optional/forbidden overlap")
            fields = schema.get("fields")
            if not isinstance(fields, dict) or set(fields) != required | optional:
                findings.append(f"E-SCHEMA: {name}.fields does not exactly type every field")
                fields = fields if isinstance(fields, dict) else {}
            if not isinstance(schema.get("unknownFieldOutcome"), str):
                findings.append(f"E-SCHEMA: {name} lacks deterministic unknownFieldOutcome")
            for field, spec in fields.items():
                if not isinstance(spec, dict):
                    findings.append(f"E-SCHEMA: {name}.{field} has no field schema")
                elif "schema" in spec:
                    if not isinstance(spec["schema"], str):
                        findings.append(f"E-SCHEMA: {name}.{field} schema ref malformed")
                    else:
                        referenced.add(spec["schema"])
                elif spec.get("type") not in {"string", "integer", "boolean", "null"}:
                    findings.append(f"E-SCHEMA: {name}.{field} lacks exact primitive type")
        elif kind == "array":
            if schema.get("closed") is not True:
                findings.append(f"E-SCHEMA: array schema {name} is not declared closed")
            if not isinstance(schema.get("items"), str):
                findings.append(f"E-SCHEMA: array schema {name} lacks named item schema")
            else:
                referenced.add(schema["items"])
            if "minItems" not in schema or "uniqueItems" not in schema:
                findings.append(f"E-SCHEMA: array schema {name} lacks cardinality/uniqueness rules")
        elif kind == "taggedUnion":
            variants = schema.get("variants")
            if not isinstance(schema.get("discriminator"), str) or not isinstance(variants, dict):
                findings.append(f"E-SCHEMA: tagged union {name} incomplete")
            else:
                referenced.update(x for x in variants.values() if isinstance(x, str))
        elif kind == "primitive":
            spec = schema.get("value")
            if not isinstance(spec, dict) or spec.get("type") not in {
                    "string", "integer", "boolean", "null"}:
                findings.append(f"E-SCHEMA: primitive schema {name} lacks exact value type")
        else:
            findings.append(f"E-SCHEMA: schema {name} has unknown kind {kind!r}")
    missing = referenced - set(schemas)
    if missing:
        findings.append(f"E-SCHEMA: referenced named schemas missing: {sorted(missing)}")
    unreachable = set(schemas) - referenced
    if unreachable:
        findings.append(f"E-SCHEMA: unreferenced schema definitions: {sorted(unreachable)}")
    required_children = {"WitnessEdge", "CanonicalAnchor", "FactPartitionEntry", "Coverage",
                         "CasObject", "RetainedBytes", "ObjectStateEntry", "ReplayObject",
                         "ProofReference", "DependencyEdge"}
    if not required_children <= set(schemas):
        findings.append(f"E-SCHEMA: reviewer-10 child schemas missing: "
                        f"{sorted(required_children-set(schemas))}")
    expected_cas_schemas = {**CAS_SCHEMA_BY_KIND, "bundle-signature": "RetainedBytes"}
    if contract.get("casSchemaByKind") != expected_cas_schemas:
        findings.append("E-SCHEMA: casSchemaByKind is not the exact closed CAS schema map")
    return findings


def _find_unit(bundle: dict[str, Any], rid: str) -> dict[str, Any] | None:
    closure = bundle.get("capabilityClosure")
    units = closure.get("units") if isinstance(closure, dict) else None
    if not isinstance(units, list):
        return None
    for unit in units:
        if not isinstance(unit, dict) or not isinstance(unit.get("objectRefs"), list):
            continue
        if any(_ref_id(x) == rid for x in unit["objectRefs"]):
            return unit
    return None


def _phase_units(bundle: dict[str, Any]) -> list[dict[str, Any]]:
    return _unit_views(bundle)[0]


def _recompute_closure(bundle: dict[str, Any], rt) -> None:
    fn = getattr(rt, "closure_commitment", getattr(rt, "closure_commit", None))
    if not callable(fn):
        raise RuntimeError("retention closure commitment API absent")
    bundle["capabilityClosure"]["closureCommitment"] = fn(_phase_units(bundle))


def _mutate_probe(base: dict[str, Any], mutation: str, deps) -> Any:
    """Apply one retained reviewer probe. Every branch must materially change input."""
    ep, rt, *_ = deps
    b = copy.deepcopy(base)
    eval0 = b.get("activatedEvaluations", [{}])[0] if isinstance(
        b.get("activatedEvaluations"), list) and b.get("activatedEvaluations") else {}
    if mutation == "root-null": return None
    if mutation == "root-number": return 7
    if mutation == "root-string": return "bundle"
    if mutation == "root-array": return []
    if mutation == "root-boolean": return True
    if mutation == "cas-bytes-object":
        b["casOracle"][0]["bytes"]["canonical"] = {"hostile": True}
    elif mutation == "claim-shape-array": eval0["claimShape"] = []
    elif mutation == "member-ids-scalar": b["requiredUniverse"]["memberIds"] = "claimed"
    elif mutation == "authoritative-string": b["authoritative"] = "false"
    elif mutation == "content-ref-kind-array": eval0["coverageRef"]["kind"] = []
    elif mutation == "evaluations-scalar": b["activatedEvaluations"] = "claimed"
    elif mutation == "storage-truthy-containers":
        b["storageAdmission"] = {"storageRoot": [], "privacyClass": {},
                                 "retentionPolicy": ["claimed"]}
    elif mutation == "top-request-id": b["requestId"] = "req-attacker"
    elif mutation == "nested-witness-metadata":
        edge = eval0["proof"]["witnessEdges"][0]
        edge.update(requestId="req-attacker", executionId="exec-attacker",
                    timestamp="later", factPartitionPinned=True,
                    regenerationClosureRetained=True,
                    producerDeclaredObligation="weaker")
    elif mutation == "nested-anchor-metadata":
        anchor = eval0["proof"]["witnessEdges"][0]["anchors"][0]
        anchor.update(requestId="req-attacker", cacheState="hot",
                      regenerationClosureRetained=True)
    elif mutation == "mistyped-witness-edge":
        edge = eval0["proof"]["witnessEdges"][0]
        edge["fromSubjectId"] = None; edge["toSubjectId"] = None
        edge["relationKind"] = {"claimed": True}
    elif mutation == "member-ids-omitted": b["requiredUniverse"]["memberIds"] = []
    elif mutation == "member-ids-substituted":
        b["requiredUniverse"]["memberIds"] = [{"evaluationId": "eval1:attacker",
                                                  "predicateId": "predicate1:attacker"}]
    elif mutation == "duplicate-evaluation-recomputed":
        b["activatedEvaluations"].append(copy.deepcopy(eval0))
        b["requiredUniverse"]["declaredCount"] = 2
        b["requiredUniverse"]["memberIds"].append(copy.deepcopy(
            b["requiredUniverse"]["memberIds"][0]))
        members = [(x["evaluationId"], x["predicateId"]) for x in b["activatedEvaluations"]]
        b["requiredUniverse"]["universeCommitment"] = ep.commit(
            "universe", [ep.encode_member(*x) for x in members])
        b["verdictDerivation"]["outcomeSetCommitment"] = ep.commit(
            "outcome-set", [ep.encode_outcome(x["evaluationId"], x["predicateId"], x["outcome"])
                            for x in b["activatedEvaluations"]])
    elif mutation == "same-key-different-outcome-recomputed":
        other = copy.deepcopy(eval0); other["outcome"] = "match"
        b["activatedEvaluations"].append(other)
        b["requiredUniverse"]["declaredCount"] = 2
        b["requiredUniverse"]["memberIds"].append(copy.deepcopy(
            b["requiredUniverse"]["memberIds"][0]))
        b["verdictDerivation"]["outcomeSetCommitment"] = ep.commit(
            "outcome-set", [ep.encode_outcome(x["evaluationId"], x["predicateId"], x["outcome"])
                            for x in b["activatedEvaluations"]])
    elif mutation == "outcome-shape-substitution-recomputed":
        eval0["outcome"] = "match"
        b["verdictDerivation"]["outcomeSetCommitment"] = ep.commit(
            "outcome-set", [ep.encode_outcome(eval0["evaluationId"], eval0["predicateId"], "match")])
    elif mutation == "outcome-substitution-unrecomputed": eval0["outcome"] = "match"
    elif mutation == "empty-outcome-commitment":
        b["verdictDerivation"]["outcomeSetCommitment"] = ep.commit("outcome-set", [])
    elif mutation == "unresolvable-full-ref":
        eval0["predicateSemanticsRef"]["id"] = "sha256:" + "d" * 64
    elif mutation == "truncated-ref": eval0["predicateSemanticsRef"]["id"] = "sha256:abcd"
    elif mutation == "indeterminate-absorbed-pass":
        eval0.update(outcome="indeterminate", claimShape="indeterminate",
                     proof={"kind": "indeterminate-proof",
                            "reasonRef": {"kind": "reason", "id": "sha256:" + "e" * 64}})
    elif mutation == "same-id-different-bytes":
        dup = copy.deepcopy(b["casOracle"][0])
        dup["bytes"]["canonical"] += " "
        b["casOracle"].append(dup)
    elif mutation == "same-id-different-partition-recomputed":
        proof = eval0["proof"]
        part_ref = proof["factPartitionRef"]["id"]
        coverage_ref = eval0["coverageRef"]["id"]
        predicate_ref = eval0["predicateSemanticsRef"]["id"]
        partition_record = next(x for x in b["casOracle"]
                                if x["ref"]["id"] == part_ref)
        coverage_record = next(x for x in b["casOracle"]
                               if x["ref"]["id"] == coverage_ref)
        predicate_record = next(x for x in b["casOracle"]
                                if x["ref"]["id"] == predicate_ref)
        partition = json.loads(partition_record["bytes"]["canonical"])
        coverage = json.loads(coverage_record["bytes"]["canonical"])
        predicate = json.loads(predicate_record["bytes"]["canonical"])
        partition["entries"] = partition["entries"][:1]
        subjects = [partition["entries"][0]["subjectId"]]
        coverage["coveredSubjectIds"] = subjects
        coverage["verificationRequirement"]["subjectDomain"] = subjects
        predicate["verificationRequirement"]["subjectDomain"] = subjects
        partition_record["bytes"]["canonical"] = _canonical_json(partition)
        coverage_record["bytes"]["canonical"] = _canonical_json(coverage)
        predicate_record["bytes"]["canonical"] = _canonical_json(predicate)
        proof["subjectCount"] = 1
        proof["subjectSetCommitment"] = ep.commit(
            "subject-set", [ep.encode_subject(subjects[0])])
    elif mutation == "coverage-id-mismatch": eval0["coverageId"] = "sha256:" + "a" * 64
    elif mutation == "producer-obligation": eval0["producerDeclaredObligation"] = "weak"
    elif mutation in {"downgrade-predicate-unit", "purged-downgraded-predicate"}:
        rid = _ref_id(eval0["predicateSemanticsRef"])
        unit = _find_unit(b, rid)
        unit["requiredForCapability"] = "replayable"
        if mutation == "purged-downgraded-predicate":
            unit["objectStates"][0]["state"] = "PURGED"
        _recompute_closure(b, rt)
    elif mutation == "replay-missing-dependency":
        robj = b["replayClosure"]["objects"][0]
        unit = _find_unit(b, _ref_id(robj["ref"]))
        unit["objectStates"][0]["state"] = "MISSING-DEPENDENCY"
    elif mutation == "malformed-replay-bag":
        b["replayClosure"] = {"objects": {"id": "sha256:abcd",
                                             "requestId": "req-attacker"},
                              "locallyResolvable": "claimed"}
    elif mutation == "alias-proof-ref":
        target = b["capabilityClosure"]["units"][0]
        alias = copy.deepcopy(target); alias["unitId"] = "unit1:alias"
        b["capabilityClosure"]["units"].append(alias); _recompute_closure(b, rt)
    elif mutation == "omit-proof-unit":
        b["capabilityClosure"]["units"].pop(0); _recompute_closure(b, rt)
    elif mutation == "invalid-relation-kind":
        eval0["proof"]["witnessEdges"][0]["relationKind"] = "attacker-kind"
    elif mutation == "span-only-relationship":
        eval0["proof"] = {"kind": "relationship-match-proof",
                          "spanAnchor": eval0["proof"]["witnessEdges"][0]["anchors"][0]}
    elif mutation == "proof-obligation-substitution":
        eval0["proofObligationId"] = "sha256:" + "b" * 64
    elif mutation == "incomplete-partition":
        part_ref = eval0["proof"]["factPartitionRef"]["id"]
        record = next(x for x in b["casOracle"] if x["ref"]["id"] == part_ref)
        obj = json.loads(record["bytes"]["canonical"]); obj["entries"].pop()
        record["bytes"]["canonical"] = _canonical_json(obj)
    elif mutation == "predicate-domain-omitted":
        pred_ref = eval0["predicateSemanticsRef"]["id"]
        record = next(x for x in b["casOracle"] if x["ref"]["id"] == pred_ref)
        obj = json.loads(record["bytes"]["canonical"])
        obj["verificationRequirement"]["subjectDomain"].pop()
        record["bytes"]["canonical"] = _canonical_json(obj)
    elif mutation == "coverage-substitution":
        cov_ref = eval0["coverageRef"]["id"]
        record = next(x for x in b["casOracle"] if x["ref"]["id"] == cov_ref)
        obj = json.loads(record["bytes"]["canonical"])
        obj["coveredSubjectIds"] = ["subject:attacker"]
        record["bytes"]["canonical"] = _canonical_json(obj)
    elif mutation == "replay-duplicate":
        b["replayClosure"]["objects"].append(copy.deepcopy(
            b["replayClosure"]["objects"][0]))
    elif mutation == "replay-wrong-unit": b["replayClosure"]["objects"][0]["unitId"] = "unit1:wrong"
    elif mutation == "nested-cas-request-id":
        record = b["casOracle"][0]; obj = json.loads(record["bytes"]["canonical"])
        obj["requestId"] = "req-attacker"; record["bytes"]["canonical"] = _canonical_json(obj)
    elif mutation == "nested-cas-removed-boolean":
        record = b["casOracle"][0]; obj = json.loads(record["bytes"]["canonical"])
        obj["factPartitionPinned"] = True; record["bytes"]["canonical"] = _canonical_json(obj)
    elif mutation == "sealed-effective-mismatch": b["effectiveCapability"] = "recorded"
    elif mutation == "nested-object-state-metadata":
        b["capabilityClosure"]["units"][0]["objectStates"][0]["timestamp"] = "later"
    elif mutation == "historical-verifier-unavailable":
        unit = _find_unit(b, next(x["ref"]["id"] for x in b["casOracle"]
                                  if x["ref"]["kind"] == "verifier-artifact"))
        unit["objectStates"][0]["state"] = "PURGED"
        _recompute_closure(b, rt)
    elif mutation == "historical-abi-unsupported":
        b["verifierRuntime"]["supportedVerifierAbis"] = [
            "opensip.offline-verifier-abi.v2"]
    else:
        raise KeyError(f"unknown retained probe mutation {mutation!r}")
    return b


def check(contract: Any, deps=None) -> list[str]:
    deps = deps or _dependency_context()
    ep, rt, ver, proof_contract, retention_contract, versioning_contract = deps
    findings: list[str] = []
    if not isinstance(contract, dict):
        return [f"E-SCHEMA: contract expected object, got {type(contract).__name__}"]
    if contract.get("artifact") != "opensip.evidence" or contract.get("version") != 3:
        findings.append("E-SCHEMA: checker is bound only to opensip.evidence v3")
    if contract.get("status") != "CANDIDATE-AWAITING-INDEPENDENT-REREVIEW":
        findings.append("assurance: Evidence v3 must await independent re-review")
    findings.extend(_schema_audit(contract))

    # Exact dependency artifact/hash/API bindings. No warning-only seams.
    consumed = contract.get("consumes")
    consumed_by_path = {x.get("artifact"): x for x in consumed if isinstance(x, dict)} \
        if isinstance(consumed, list) else {}
    expected_apis = {
        "artifacts/evaluation-proof.v2.json": [
            "frame_component", "encode_member", "encode_outcome", "encode_subject", "commit",
            "derive_verdict", "derive_verdict_commitment", "validate_bundle",
            "derive_proof_requirements"],
        "artifacts/retention-tiers.v7.json": [
            "encode_closure_unit", "closure_commitment", "validate_capability_closure",
            "derive_effective_capability"],
        "artifacts/versioning-policy.v3.json": [
            "historicalSemanticsPolicy", "_historical_decision"],
        "artifacts/fact-plane.v1.json": [
            "requirementSchema", "predicate-relative sufficiency"],
    }
    if set(consumed_by_path) != set(expected_apis):
        findings.append("E7: consumes must be the exact reviewed dependency set")
    for path, apis in expected_apis.items():
        declaration = consumed_by_path.get(path)
        if isinstance(declaration, dict) and declaration.get("api") != apis:
            findings.append(f"E7: {path} API binding differs from exact reviewed seam")
    for filename, module, artifact in ((PROOF, ep, proof_contract),
                                       (RETENTION, rt, retention_contract),
                                       (VERSIONING, ver, versioning_contract)):
        path = "artifacts/" + filename
        declaration = consumed_by_path.get(path)
        if not isinstance(declaration, dict):
            findings.append(f"E7: missing exact dependency declaration for {path}")
            continue
        actual_hash = hashlib.sha256((HERE / filename).read_bytes()).hexdigest()
        if declaration.get("sha256") != actual_hash:
            findings.append(f"E7: {path} hash {actual_hash} != declared "
                            f"{declaration.get('sha256')}")
        for api in declaration.get("api", []) if isinstance(declaration.get("api"), list) else []:
            if api.startswith("_"):
                present = hasattr(module, api)
            elif api == "historicalSemanticsPolicy":
                present = isinstance(artifact.get(api), dict)
            else:
                present = callable(getattr(module, api, None)) or api in artifact
            if not present:
                findings.append(f"E7: consumed API {filename}#{api} is absent")
    fact_path = "artifacts/" + FACT_PLANE
    fact_declaration = consumed_by_path.get(fact_path)
    if isinstance(fact_declaration, dict):
        actual_hash = hashlib.sha256((HERE / FACT_PLANE).read_bytes()).hexdigest()
        if fact_declaration.get("sha256") != actual_hash:
            findings.append(f"E7: {fact_path} hash {actual_hash} != declared "
                            f"{fact_declaration.get('sha256')}")

    positives = contract.get("positiveFixtures")
    if not isinstance(positives, list) or not positives:
        findings.append("E-SCHEMA: positiveFixtures absent")
        positives = []
    positive_by_id: dict[str, dict[str, Any]] = {}
    for i, fixture in enumerate(positives):
        if not isinstance(fixture, dict) or set(fixture) != {"id", "bundle"}:
            findings.append(f"E-SCHEMA: positiveFixtures[{i}] not closed")
            continue
        fid = fixture.get("id")
        if not isinstance(fid, str) or fid in positive_by_id:
            findings.append(f"E-SCHEMA: positive fixture id {fid!r} missing/duplicate")
            continue
        positive_by_id[fid] = fixture["bundle"]
        hits = validate(fixture["bundle"], contract, deps)
        if hits:
            findings.append(f"{fid}: positive fixture violates "
                            f"{sorted({x for x, _ in hits})}: {hits[0][1]}")

    negative_container = contract.get("counterexampleFixtures")
    negatives = negative_container.get("fixtures") if isinstance(negative_container, dict) else None
    if not isinstance(negatives, list) or not negatives:
        findings.append("E-SCHEMA: counterexample fixtures absent")
        negatives = []
    seen_negative: set[str] = set()
    exercised: set[str] = set()
    for i, fixture in enumerate(negatives):
        required = {"id", "baseId", "mutation", "mustRejectBy", "reviewProbe"}
        if not isinstance(fixture, dict) or set(fixture) != required:
            findings.append(f"E-SCHEMA: counterexampleFixtures[{i}] not closed")
            continue
        fid = fixture.get("id")
        if not isinstance(fid, str) or fid in seen_negative:
            findings.append(f"E-SCHEMA: counterexample id {fid!r} missing/duplicate")
            continue
        seen_negative.add(fid)
        base = positive_by_id.get(fixture.get("baseId"))
        if base is None:
            findings.append(f"{fid}: unknown base fixture {fixture.get('baseId')!r}")
            continue
        try:
            mutated = _mutate_probe(base, fixture["mutation"], deps)
        except Exception as exc:
            findings.append(f"{fid}: mutation failed to apply: {type(exc).__name__}: {exc}")
            continue
        if _canonical_json(mutated) == _canonical_json(base):
            findings.append(f"{fid}: mutation applied no change")
            continue
        hits = validate(mutated, contract, deps)
        codes = {code for code, _ in hits}
        wanted = fixture["mustRejectBy"]
        exercised.add(wanted)
        if wanted not in codes:
            findings.append(f"{fid}: NOT rejected by {wanted}; fired {sorted(codes) or 'nothing'}")

    # Every independent probe is retained; probe 23 is the selftest control below.
    represented = {x.get("reviewProbe") for x in negatives if isinstance(x, dict)}
    required_probes = {f"R10-PROBE-{i:02d}" for i in range(1, 23)}
    if not required_probes <= represented:
        findings.append(f"E-SCHEMA: retained reviewer probes missing: "
                        f"{sorted(required_probes-represented)}")
    dispositions = contract.get("reviewer10ProbeDisposition")
    disp_ids = {x.get("id") for x in dispositions if isinstance(x, dict)} \
        if isinstance(dispositions, list) else set()
    all_probe_ids = {f"R10-PROBE-{i:02d}" for i in range(1, 24)}
    if disp_ids != all_probe_ids:
        findings.append("E-SCHEMA: reviewer10ProbeDisposition must cover R10-PROBE-01..23")
    original_passes = {1, 5, 12, 13, 14, 17, 22, 23}
    negative_ids = {x.get("id") for x in negatives if isinstance(x, dict)}
    if isinstance(dispositions, list):
        for disposition in dispositions:
            if not isinstance(disposition, dict) or set(disposition) != {
                    "id", "originalResult", "repairedResult", "fixtures"}:
                findings.append("E-SCHEMA: reviewer10 probe disposition is not closed")
                continue
            match = re.fullmatch(r"R10-PROBE-(\d{2})", str(disposition.get("id")))
            if match is None:
                continue
            number = int(match.group(1))
            original = "PASS" if number in original_passes else "FAIL"
            repaired = "CONTROL_RETAINED" if number == 23 \
                else "REJECTED_WITH_STABLE_FINDINGS"
            if disposition.get("originalResult") != original \
                    or disposition.get("repairedResult") != repaired:
                findings.append(f"E-SCHEMA: {disposition.get('id')} disposition drifts "
                                "from reviewer-10 history/repair result")
            fixture_ids = disposition.get("fixtures")
            if not isinstance(fixture_ids, list) or not fixture_ids \
                    or any(not isinstance(x, str) for x in fixture_ids):
                findings.append(f"E-SCHEMA: {disposition.get('id')} has no exact fixtures")
            elif number != 23 and not set(fixture_ids) <= negative_ids:
                findings.append(f"E-SCHEMA: {disposition.get('id')} names unknown fixtures")

    finding_dispositions = contract.get("reviewer10FindingDisposition")
    expected_findings = {f"R10-EVD-{i:02d}" for i in range(1, 8)}
    got_findings = {x.get("id") for x in finding_dispositions if isinstance(x, dict)} \
        if isinstance(finding_dispositions, list) else set()
    if got_findings != expected_findings:
        findings.append("E-SCHEMA: reviewer10FindingDisposition must cover R10-EVD-01..07")
    if isinstance(finding_dispositions, list):
        for disposition in finding_dispositions:
            if not isinstance(disposition, dict) or set(disposition) != {
                    "id", "status", "repairEvidence"}:
                findings.append("E-SCHEMA: reviewer10 finding disposition is not closed")
            elif disposition.get("status") != "CLOSED_AWAITING_INDEPENDENT_REREVIEW" \
                    or not isinstance(disposition.get("repairEvidence"), str) \
                    or not disposition["repairEvidence"]:
                findings.append(f"assurance: {disposition.get('id')} disposition overclaims "
                                "or lacks repair evidence")
    expected_controls = {
        "dirtyBase": "REFUSE_BEFORE_MUTATION_LOOP",
        "nonApplyingMutation": "COUNT_AS_ESCAPE",
        "mutationException": "COUNT_AS_ESCAPE",
    }
    if contract.get("selftestControls") != expected_controls:
        findings.append("E-SCHEMA: reviewer-10 selftest controls are not exact")

    assurance = contract.get("assurance")
    expected_assurance = {"state": "SPECIFIED", "evidenceGrade": "IMPLEMENTABLE_UNEXECUTED",
                          "independentRereview": "REQUIRED", "qualified": False,
                          "demonstrated": False, "productReleaseQualified": False}
    if assurance != expected_assurance:
        findings.append("assurance: must remain SPECIFIED / IMPLEMENTABLE_UNEXECUTED, "
                        "unqualified and independent-rereview-required")
    residuals = {x.get("id"): x for x in contract.get("retainedResiduals", [])
                 if isinstance(x, dict)}
    if (residuals.get("A1-RTV4-02") or {}).get("status") != "UNMEASURED":
        findings.append("assurance: A1-RTV4-02 must remain UNMEASURED")
    if (residuals.get("CD-RT-5") or {}).get("status") != "BLOCKED_ON_PHASE_1A":
        findings.append("assurance: CD-RT-5 must remain BLOCKED_ON_PHASE_1A")
    if "DO NOT SEAL" not in str(contract.get("sealRecommendation", "")).upper():
        findings.append("assurance: Evidence v3 must remain DO NOT SEAL")
    future = contract.get("futureCrossSurfaceJoin")
    if "FORBIDDEN TO PROMOTE" not in json.dumps(future):
        findings.append("E-META: OPERABILITY RequestId promotion is not held pending re-review")
    return findings


def _open_witness_schema(contract: dict[str, Any]) -> None:
    contract["recordSchemas"]["WitnessEdge"]["closed"] = False


def _untype_witness_field(contract: dict[str, Any]) -> None:
    contract["recordSchemas"]["WitnessEdge"]["fields"].pop("relationKind")


def _drop_anchor_schema(contract: dict[str, Any]) -> None:
    contract["recordSchemas"].pop("CanonicalAnchor")


def _drop_probe_02(contract: dict[str, Any]) -> None:
    fixtures = contract["counterexampleFixtures"]["fixtures"]
    contract["counterexampleFixtures"]["fixtures"] = [
        x for x in fixtures if x["reviewProbe"] != "R10-PROBE-02"]


def _corrupt_positive_cas(contract: dict[str, Any]) -> None:
    contract["positiveFixtures"][0]["bundle"]["casOracle"][0]["bytes"]["canonical"] += " "


def _duplicate_positive_activation(contract: dict[str, Any]) -> None:
    bundle = contract["positiveFixtures"][0]["bundle"]
    bundle["activatedEvaluations"].append(copy.deepcopy(bundle["activatedEvaluations"][0]))


def _substitute_positive_coverage(contract: dict[str, Any]) -> None:
    contract["positiveFixtures"][0]["bundle"]["activatedEvaluations"][0][
        "coverageId"] = "sha256:" + "f" * 64


def _drift_dependency_hash(contract: dict[str, Any]) -> None:
    contract["consumes"][0]["sha256"] = "0" * 64


def _drop_dependency_api(contract: dict[str, Any]) -> None:
    contract["consumes"][0]["api"].remove("frame_component")


def _drop_probe_disposition(contract: dict[str, Any]) -> None:
    contract["reviewer10ProbeDisposition"].pop()


def _overclaim_finding_disposition(contract: dict[str, Any]) -> None:
    contract["reviewer10FindingDisposition"][0]["status"] = "QUALIFIED"


def _overclaim_assurance(contract: dict[str, Any]) -> None:
    contract["assurance"]["qualified"] = True


def _promote_operability_join(contract: dict[str, Any]) -> None:
    contract["futureCrossSurfaceJoin"] = {"OPERABILITY-RequestId": "mechanicallyJoined"}


def _weaken_selftest_controls(contract: dict[str, Any]) -> None:
    contract["selftestControls"]["nonApplyingMutation"] = "IGNORE"


CONTRACT_MUTATIONS: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
    ("reopen WitnessEdge schema", _open_witness_schema),
    ("remove WitnessEdge field type", _untype_witness_field),
    ("remove CanonicalAnchor schema", _drop_anchor_schema),
    ("remove retained R10-PROBE-02", _drop_probe_02),
    ("corrupt positive retained CAS bytes", _corrupt_positive_cas),
    ("duplicate positive activation", _duplicate_positive_activation),
    ("substitute positive Coverage identity", _substitute_positive_coverage),
    ("drift exact dependency hash", _drift_dependency_hash),
    ("drop required dependency API", _drop_dependency_api),
    ("drop reviewer probe disposition", _drop_probe_disposition),
    ("overclaim reviewer finding disposition", _overclaim_finding_disposition),
    ("overclaim assurance", _overclaim_assurance),
    ("prematurely promote OPERABILITY join", _promote_operability_join),
    ("weaken selftest controls", _weaken_selftest_controls),
]


def selftest(contract: Any, deps=None,
             mutations: list[tuple[str, Callable[[dict[str, Any]], None]]] | None = None) -> int:
    """Prove the checker path is load-bearing; dirty/no-op/raising controls fail."""
    deps = deps or _dependency_context()
    base_findings = check(contract, deps)
    if base_findings:
        print("base contract is dirty; refusing before mutation loop")
        for finding in base_findings[:10]:
            print(f"  {finding}")
        if len(base_findings) > 10:
            print(f"  ... {len(base_findings) - 10} more")
        return 1
    selected = CONTRACT_MUTATIONS if mutations is None else mutations
    escapes = 0
    for name, mutate in selected:
        candidate = copy.deepcopy(contract)
        before = _canonical_json(candidate)
        try:
            mutate(candidate)
        except Exception as exc:
            print(f"ESCAPED {name}: mutation failed to apply: {type(exc).__name__}: {exc}")
            escapes += 1
            continue
        after = _canonical_json(candidate)
        if before == after:
            print(f"ESCAPED {name}: mutation applied no change")
            escapes += 1
            continue
        try:
            findings = check(candidate, deps)
        except Exception as exc:
            print(f"ESCAPED {name}: checker raised {type(exc).__name__}: {exc}")
            escapes += 1
            continue
        if not findings:
            print(f"ESCAPED {name}: mutated contract remained clean")
            escapes += 1
        else:
            print(f"rejected {name}: {findings[0]}")
    if escapes:
        print(f"{escapes}/{len(selected)} mutations ESCAPED — Evidence v3 is not load-bearing")
        return 1
    print(f"all {len(selected)} mutations rejected — Evidence v3 is load-bearing")
    return 0


def _load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text())


def main() -> int:
    args = sys.argv[1:]
    selftest_mode = "--selftest" in args
    args = [x for x in args if x != "--selftest"]
    if len(args) > 1:
        print(f"usage: {pathlib.Path(sys.argv[0]).name} [contract] [--selftest]",
              file=sys.stderr)
        return 2
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    try:
        contract = _load_json(path)
        deps = _dependency_context()
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"cannot load Evidence v3 or exact dependencies: {exc}", file=sys.stderr)
        return 2
    if selftest_mode:
        return selftest(contract, deps)
    findings = check(contract, deps)
    if findings:
        for finding in findings:
            print(finding)
        print(f"{len(findings)} Evidence v3 finding(s)")
        return 1
    schemas = len(contract.get("recordSchemas", {}))
    positives = len(contract.get("positiveFixtures", []))
    negatives = len((contract.get("counterexampleFixtures") or {}).get("fixtures", []))
    print(f"Evidence v3 clean: {schemas} named schemas, {positives} positive vectors, "
          f"{negatives} retained counterexamples, R10-PROBE-01..23 and "
          "R10-EVD-01..07 dispositioned; assurance remains unqualified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
