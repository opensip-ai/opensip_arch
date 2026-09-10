"""Full-scan atom reference (isolated successor). Not product runtime. Not full Run replay.

Owner-admitted native/import records only. Reuses native_evidence_model.v2.sufficiency_v2
and workflows_model.v1.glob_match. Root composes boolean nodes, findings, gating.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError

HERE = Path(__file__).resolve().parent
NATIVE_PY = HERE.parent / "native" / "native_evidence_model.v2.py"
WORK_PY = HERE.parent / "workflows" / "workflows_model.v1.py"
CANON_PY = HERE / "canonical.py"
REGISTRY = json.loads((HERE / "evaluator-projection-registry.v1.json").read_text(encoding="utf-8"))
INCOMING_SEARCH_SCHEMA = json.loads((HERE / "incoming-search.schema.v1.json").read_text(encoding="utf-8"))
TARGET_ATTRIBUTION_SCHEMA = json.loads((HERE / "target-attribution.schema.v2.json").read_text(encoding="utf-8"))
TARGET_ATTRIBUTION_V1_SCHEMA = json.loads((HERE / "target-attribution.schema.v1.json").read_text(encoding="utf-8"))
LOGICAL_PATH_RE = re.compile(r"^[^/\\\u0000]{1,255}(/[^/\\\u0000]{1,255})*\Z")
SUBJECT_ID_RE = re.compile(r"^[a-z][a-z0-9-]*:[^\u0000-\u001f\u007f-\u009f]+\Z")
SCOPE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["schemaVersion", "workspaceRoots", "pathPrefixes", "excludedPathPrefixes"],
    "properties": {
        "schemaVersion": {"const": 2},
        "workspaceRoots": {"type": "array", "items": {"type": "string"}},
        "pathPrefixes": {"type": "array", "items": {"type": "string"}},
        "excludedPathPrefixes": {"type": "array", "items": {"type": "string"}},
    },
}
CLOSED_INPUT_KEYS = frozenset({
    "facts", "scopes", "coverages", "enumerationPlan", "inventories", "targetAttributions",
    "closures", "universeDomains", "imports", "importPayloads", "importObservations",
    "importScopes", "importScopeAdapter", "planSelectedImportIds", "evaluationInputRefs",
    "incomingSearchAttestations", "planId", "blobs", "coverageScopes", "importFlagsAdapter",
})
IMPORT_FLAG_KEYS = frozenset({"consumable", "staleness"})
INVENTORY_C_FIELDS = (
    "schemaVersion", "planId", "parameterDigest", "cellOrdinal", "programOrdinal",
    "kind", "state", "deficiency", "nativeCause", "examinedPaths", "rows",
)
SUBJECT_SCOPE_FIELDS = (
    "schemaVersion", "snapshotId", "sourceUniverse", "targetUniverse",
    "relation", "resolution", "enumeratorClosure", "subjects",
)


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


N = _load("native_evidence_model_v2_atom", NATIVE_PY)
W = _load("workflows_model_v1_atom", WORK_PY)
C = _load("identity_canonical_atom", CANON_PY)

TRUE, FALSE, UNK = "true", "false", "indeterminate"
MATCH, NOMATCH, FUNK = "match", "nomatch", "unknown"
ABSENT = object()
PORTABLE_DOMAINS = tuple(REGISTRY["engineFamilies"]["portableUniverseDomains"])
RESOLVED_RUNGS = frozenset(REGISTRY["resolvedRungs"])
CAUSE_CODES = frozenset(REGISTRY["$defs"]["AtomCauseCodeV1"]["enum"])
NATIVE_CAUSE_CODES = frozenset(REGISTRY["$defs"]["NativeCause"]["enum"])
FF_SCHEMA = REGISTRY["$defs"]["FieldFilterSuccessorV1"]
LANG_FAMILY = {}
for fam, row in REGISTRY["engineFamilies"]["families"].items():
    for mode in row["languageModes"]:
        LANG_FAMILY[mode] = fam
DOMAIN_FAMILY = {row["universeDomain"]: fam for fam, row in REGISTRY["engineFamilies"]["families"].items()}
GLOB_OK = re.compile(r"^[^\\\u0000]+$")
IMPORT_EVIDENCE = frozenset({"test", "runtime", "history", "dependency", "prepared"})


class AtomAdmissionError(Exception):
    def __init__(self, key: str, detail: str = ""):
        self.key = key
        self.detail = detail
        super().__init__(key + (": " + detail if detail else ""))


def evaluate_atom(atom: dict, subject: dict, inputs: dict) -> dict:
    admit_atom_inputs(inputs)
    _admit_subject(subject)
    spec = _admit_atom(atom, subject)
    if spec["plane"] == "native":
        return _eval_native(atom, subject, inputs, spec)
    return _eval_imported(atom, subject, inputs, spec)


def admit_atom_inputs(inputs: dict) -> None:
    """Global admission of closed inputs, including unused sidecars and selected imports.

    Root calls this even when the policy has no atoms. Missing selected wrappers, contrary
    observation/payload adapters, and TargetAttributionV2 joins refuse here.
    """
    if not isinstance(inputs, dict):
        raise AtomAdmissionError("ATOM_INPUTS_NOT_RECORD")
    extra = sorted(set(inputs) - CLOSED_INPUT_KEYS)
    if extra:
        raise AtomAdmissionError("ATOM_INPUT_KEY_UNKNOWN", ",".join(extra))
    adapter = inputs.get("importFlagsAdapter")
    if adapter is not None and not isinstance(adapter, dict):
        raise AtomAdmissionError("ATOM_IMPORT_FLAG_ADAPTER")
    mapping = inputs.get("coverageScopes")
    if mapping is not None and not isinstance(mapping, dict):
        raise AtomAdmissionError("ATOM_COVERAGE_SCOPES")
    _admit_incoming_searches(inputs)
    _admit_target_attributions(inputs)
    _admit_selected_imports(inputs)


def _admit_subject(subject: dict) -> None:
    if not isinstance(subject, dict):
        raise AtomAdmissionError("ATOM_SUBJECT_SHAPE")
    for k in ("universe", "kind", "nativeSubjectId"):
        if k not in subject:
            raise AtomAdmissionError("ATOM_SUBJECT_SHAPE", k)
    if subject["kind"] not in ("file", "symbol", "package"):
        raise AtomAdmissionError("ATOM_SUBJECT_KIND", str(subject["kind"]))
    if not isinstance(subject["universe"], str) or not re.fullmatch(r"[0-9a-f]{64}", subject["universe"]):
        raise AtomAdmissionError("ATOM_SUBJECT_UNIVERSE")
    if subject["kind"] == "package":
        p = subject.get("packageManifestPath")
        if not isinstance(p, str) or not p:
            raise AtomAdmissionError("ATOM_SUBJECT_SHAPE", "packageManifestPath")
    elif "packageManifestPath" in subject:
        raise AtomAdmissionError("ATOM_SUBJECT_SHAPE", "packageManifestPath")


def _applicable_kinds(spec: dict, endpoint: str, rule_sk: str | None) -> list[str]:
    if endpoint == "target":
        kinds = list(spec.get("targetKinds") or [])
    else:
        kinds = list(spec.get("sourceSubjectKinds") or ([spec.get("sourceSubjectKind")] if spec.get("sourceSubjectKind") else []))
    kinds = [k for k in kinds if k]
    if rule_sk == "export":
        if "symbol" not in kinds:
            raise AtomAdmissionError("ATOM_KIND_INCOMPATIBLE", "export")
        return ["symbol"]
    if rule_sk in ("file", "symbol", "package"):
        if rule_sk not in kinds:
            raise AtomAdmissionError("ATOM_KIND_INCOMPATIBLE", rule_sk)
        return [rule_sk]
    return kinds


def _admit_atom(atom: dict, subject: dict) -> dict:
    if not isinstance(atom, dict):
        raise AtomAdmissionError("ATOM_SHAPE")
    rel = atom.get("relation")
    if rel not in REGISTRY["relations"]:
        raise AtomAdmissionError("ATOM_RELATION_UNREGISTERED", str(rel))
    spec = REGISTRY["relations"][rel]
    op = atom.get("op")
    if op not in ("exists", "none", "count-at-most", "all-covered"):
        raise AtomAdmissionError("ATOM_OP", str(op))
    if op == "count-at-most":
        n = atom.get("n")
        if type(n) is not int or n < 0:
            raise AtomAdmissionError("ATOM_COUNT_N")
    endpoint = atom.get("endpoint", "source")
    if endpoint not in ("source", "target"):
        raise AtomAdmissionError("ATOM_ENDPOINT", str(endpoint))
    ladder = spec["ladder"]
    mn = atom.get("minResolution")
    if mn not in ladder:
        raise AtomAdmissionError("ATOM_MIN_RESOLUTION", str(mn))
    if endpoint == "target":
        if spec.get("endpointTarget") == "forbidden":
            raise AtomAdmissionError("ATOM_ENDPOINT_UNAVAILABLE", rel)
        rungs = spec.get("endpointTargetRungs")
        if rungs and mn not in rungs:
            raise AtomAdmissionError("ATOM_ENDPOINT_UNAVAILABLE", rel + "@" + mn)
    evidence = atom.get("evidence")
    if spec["plane"] == "native":
        if evidence is not None:
            raise AtomAdmissionError("ATOM_EVIDENCE_KIND_MISMATCH", "native")
    elif evidence != spec.get("evidenceKind"):
        raise AtomAdmissionError("ATOM_EVIDENCE_KIND_MISMATCH", str(evidence))
    kinds = _applicable_kinds(spec, endpoint, atom.get("subjectKind"))
    if subject["kind"] not in kinds:
        raise AtomAdmissionError("ATOM_KIND_INCOMPATIBLE", subject["kind"])
    filters = atom.get("filters") or []
    if type(filters) is not list or len(filters) > 16:
        raise AtomAdmissionError("ATOM_FILTERS")
    for flt in filters:
        _admit_filter(rel, mn, spec, flt)
    return spec


def _proj(spec: dict, field: str, min_rung: str):
    p = spec["filters"][field]
    if isinstance(p, dict) and min_rung in p:
        return p[min_rung]
    return p


def _admit_filter(rel: str, min_rung: str, spec: dict, flt: dict) -> None:
    if not isinstance(flt, dict):
        raise AtomAdmissionError("ATOM_FILTER_SHAPE")
    try:
        Draft202012Validator(FF_SCHEMA).validate(flt)
    except ValidationError as exc:
        raise AtomAdmissionError("ATOM_FILTER_SCHEMA", exc.message) from exc
    field, cmp, value = flt["field"], flt["cmp"], flt["value"]
    proj = _proj(spec, field, min_rung)
    if proj == "forbidden":
        raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", rel + "." + field)
    table = REGISTRY["comparatorTable"][field]
    allowed = [c for c in ("eq", "neq", "in", "prefix", "glob", "gte", "lte") if table.get(c)]
    if cmp not in allowed:
        raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", field + " " + cmp)
    enum = table.get("enum")
    if field == "testResult":
        enum = (table.get("enumByRelation") or {}).get(rel)
    if field == "universe":
        enum = list(PORTABLE_DOMAINS)
    if field == "resolution":
        enum = list(spec["ladder"])
    if cmp in ("eq", "neq") and enum is not None and value not in enum:
        raise AtomAdmissionError("ATOM_FILTER_ENUM_LITERAL_UNKNOWN", str(value))
    if cmp == "in" and enum is not None:
        if type(value) is not list:
            raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", "in type")
        for item in value:
            if item not in enum:
                raise AtomAdmissionError("ATOM_FILTER_ENUM_LITERAL_UNKNOWN", str(item))
    if cmp in ("prefix", "glob"):
        if type(value) is not str or not GLOB_OK.fullmatch(value):
            raise AtomAdmissionError("ATOM_GLOB_PATTERN", str(value))
        if cmp == "glob" and "\\" in value:
            raise AtomAdmissionError("ATOM_GLOB_PATTERN", value)


def _result(**kwargs) -> dict:
    base = {
        "value": UNK, "kind": None, "knownFactIds": [], "uncertainFactIds": [],
        "knownObservationAddresses": [], "uncertainObservationAddresses": [],
        "coverageIds": [], "scopeIds": [], "evaluationInputRefs": [],
        "causes": [], "nativeDeficiencies": [], "disclosures": [], "usedInputDigests": [],
    }
    base.update(kwargs)
    base["causes"] = _uniq_causes(base["causes"])
    base["knownFactIds"] = sorted(set(base["knownFactIds"]))
    base["uncertainFactIds"] = sorted(set(base["uncertainFactIds"]))
    base["coverageIds"] = sorted(set(base["coverageIds"]))
    base["scopeIds"] = sorted(set(base["scopeIds"]))
    base["nativeDeficiencies"] = sorted(set(base["nativeDeficiencies"]))
    base["knownObservationAddresses"] = _sort_addrs(base["knownObservationAddresses"])
    base["uncertainObservationAddresses"] = _sort_addrs(base["uncertainObservationAddresses"])
    base["evaluationInputRefs"] = sorted(set(base["evaluationInputRefs"]))
    return base


def _sort_addrs(xs: list) -> list:
    seen, out = set(), []
    def key(a):
        return (a["importId"], a["selector"], -1 if a["ordinal"] is None else a["ordinal"])
    for a in sorted(xs, key=key):
        t = (a["importId"], a["selector"], a["ordinal"])
        if t in seen:
            continue
        seen.add(t)
        out.append({"importId": a["importId"], "selector": a["selector"], "ordinal": a["ordinal"]})
    return out


def _uniq_causes(causes: list) -> list:
    seen, out = set(), []
    for c in causes:
        if not isinstance(c, dict) or c.get("code") not in CAUSE_CODES:
            raise AtomAdmissionError("ATOM_CAUSE_UNREGISTERED", str(c))
        if "evidenceKind" not in c or "nativeCause" not in c:
            raise AtomAdmissionError("ATOM_CAUSE_UNREGISTERED", "evidenceKind/nativeCause")
        ek, nc = c.get("evidenceKind"), c.get("nativeCause")
        if ek is not None and ek not in IMPORT_EVIDENCE:
            raise AtomAdmissionError("ATOM_CAUSE_UNREGISTERED", "evidenceKind")
        if nc is not None and nc not in NATIVE_CAUSE_CODES:
            raise AtomAdmissionError("ATOM_CAUSE_UNREGISTERED", "nativeCause")
        key = json.dumps(c, sort_keys=True, separators=(",", ":"))
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return sorted(out, key=lambda c: json.dumps(c, sort_keys=True, separators=(",", ":")))


def _typed_native_cause(value):
    if value is None:
        return None
    if value not in NATIVE_CAUSE_CODES:
        raise AtomAdmissionError("ATOM_NATIVE_CAUSE_UNTYPED", str(value))
    return value


def _cause(code: str, *, evidenceKind=None, nativeCause=None, **extra) -> dict:
    rec = {"code": code, "evidenceKind": evidenceKind, "nativeCause": _typed_native_cause(nativeCause)}
    rec.update({k: v for k, v in extra.items() if v is not None})
    return rec


def _cmp_string(cmp: str, projected: str, value) -> str:
    if cmp == "eq":
        return MATCH if projected == value else NOMATCH
    if cmp == "neq":
        return MATCH if projected != value else NOMATCH
    if cmp == "in":
        return MATCH if projected in value else NOMATCH
    if cmp == "prefix":
        return MATCH if projected.startswith(value) else NOMATCH
    if cmp == "glob":
        return MATCH if W.glob_match(value, projected) else NOMATCH
    raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", cmp)


def _cmp_int(cmp: str, projected: int, value) -> str:
    if cmp == "eq":
        return MATCH if projected == value else NOMATCH
    if cmp == "neq":
        return MATCH if projected != value else NOMATCH
    if cmp == "in":
        return MATCH if projected in value else NOMATCH
    if cmp == "gte":
        return MATCH if projected >= value else NOMATCH
    if cmp == "lte":
        return MATCH if projected <= value else NOMATCH
    raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", cmp)


def _and_fr(a: str, b: str) -> str:
    if a == NOMATCH or b == NOMATCH:
        return NOMATCH
    if a == FUNK or b == FUNK:
        return FUNK
    return MATCH


def _plan_binding(plan: dict, cell_ordinal: int, program_ordinal: int) -> dict | None:
    cells = plan.get("cells") or []
    if cell_ordinal >= len(cells):
        return None
    binds = cells[cell_ordinal].get("programBindings") or []
    for b in binds:
        if b.get("ordinal") == program_ordinal:
            return b
    if program_ordinal < len(binds):
        return binds[program_ordinal]
    return None


def _inventory_universe(inv: dict, plan: dict | None) -> str | None:
    if plan is None:
        return inv.get("universe")
    b = _plan_binding(plan, inv["cellOrdinal"], inv["programOrdinal"])
    if b is None:
        return inv.get("universe")
    return b.get("universe")


def _identity_key(universe: str, row: dict) -> tuple:
    if row.get("kind") == "package":
        return (universe, "package", row.get("nativeSubjectId"), row.get("path"))
    return (universe, row.get("kind"), row.get("nativeSubjectId"))


def _distinct_identities(native_id: str, universe: str, inventories: list, plan: dict | None,
                         kind: str | None = None, package_manifest_path: str | None = None):
    triples = set()
    rows = []
    for inv in inventories:
        u = _inventory_universe(inv, plan)
        if u != universe:
            continue
        for row in inv.get("rows") or []:
            if row.get("nativeSubjectId") != native_id:
                continue
            if kind is not None and row.get("kind") != kind:
                continue
            if row.get("kind") == "package" and package_manifest_path is not None:
                if row.get("path") != package_manifest_path:
                    continue
            triples.add(_identity_key(u, row))
            rows.append(row)
    return triples, rows


def _coherent_rows(rows: list) -> list:
    """Dedup equivalent observations of one identity. Distinct payloads stay distinct."""
    distinct = []
    for row in rows:
        if any(C.equal_typed(row, prev) for prev in distinct):
            continue
        distinct.append(row)
    return distinct


def _lookup_rows(native_id: str, universe: str, kind: str | None, inventories: list, plan: dict | None,
                 package_manifest_path: str | None = None) -> list:
    _, rows = _distinct_identities(native_id, universe, inventories, plan, kind, package_manifest_path)
    return _coherent_rows(rows)


def _symbol_rows_by_path_qn(path: str, qn: str, universe: str, inventories: list, plan: dict | None) -> list:
    hits = []
    seen = set()
    for inv in inventories:
        if inv.get("kind") != "symbol":
            continue
        u = _inventory_universe(inv, plan)
        if u != universe:
            continue
        for row in inv.get("rows") or []:
            if row.get("path") == path and row.get("qualifiedName") == qn:
                t = (u, "symbol", row["nativeSubjectId"])
                if t in seen:
                    continue
                seen.add(t)
                hits.append(row)
    return hits


def _inventory_c_record(inv: dict) -> dict:
    return {k: inv[k] for k in INVENTORY_C_FIELDS if k in inv}


def _inventory_raw_digest(inv: dict) -> str:
    return hashlib.sha256(C.canonical(_inventory_c_record(inv))).hexdigest()


def _ephemeral_target(fact: dict, spec: dict, inputs: dict) -> dict:
    field = spec.get("targetNativeIdField")
    if not field:
        return {"kind": "unknown", "occupancy": "unknown", "exported": None, "nativeId": None,
                "packageManifestPath": None, "identities": set()}
    nid = (fact.get("payload") or {}).get(field)
    if nid is None:
        return {"kind": "unknown", "occupancy": "unknown", "exported": None, "nativeId": None,
                "packageManifestPath": None, "identities": set()}
    plan = inputs.get("enumerationPlan")
    inventories = inputs.get("inventories") or []
    triples, rows = _distinct_identities(nid, fact["targetUniverse"], inventories, plan)
    triples = set(triples)
    if len(triples) == 1:
        row = _coherent_rows(rows)[0]
        return {
            "kind": row["kind"], "occupancy": "first-party",
            "exported": row.get("exported") if row["kind"] == "symbol" else None, "nativeId": nid,
            "packageManifestPath": row.get("path") if row["kind"] == "package" else None,
            "identities": triples,
        }
    if len(triples) == 0:
        return {"kind": "unknown", "occupancy": "unknown", "nativeId": nid, "exported": None,
                "packageManifestPath": None, "identities": triples}
    return {"kind": "unknown", "occupancy": "unknown", "nativeId": nid, "exported": None,
            "ambiguous": True, "packageManifestPath": None, "identities": triples}


def _sidecar_map(inputs: dict) -> dict:
    raw = inputs.get("targetAttributions") or {}
    if isinstance(raw, list):
        out = {}
        for sc in raw:
            fid = sc.get("sourceFactId")
            out.setdefault(fid, []).append(sc)
        return {k: v[0] if len(v) == 1 else v for k, v in out.items()}
    return raw


def _admit_target_attributions(inputs: dict) -> None:
    facts = inputs.get("facts") or {}
    plan_id = inputs.get("planId")
    closures = inputs.get("closures") or {}
    seen_fact = set()
    items = _sidecar_map(inputs)
    for key, sidecar in items.items():
        if isinstance(sidecar, list):
            raise AtomAdmissionError("TARGET_ATTRIBUTION_DUPLICATE_FACT")
        if sidecar.get("schemaVersion") != 2:
            raise AtomAdmissionError("TARGET_ATTRIBUTION_SCHEMA_VERSION")
        try:
            Draft202012Validator(TARGET_ATTRIBUTION_SCHEMA).validate(sidecar)
        except ValidationError as exc:
            raise AtomAdmissionError("TARGET_ATTRIBUTION_SCHEMA", exc.message) from exc
        fid = sidecar.get("sourceFactId")
        if fid in seen_fact or (key not in (fid, None) and key != fid):
            raise AtomAdmissionError("TARGET_ATTRIBUTION_DUPLICATE_FACT")
        seen_fact.add(fid)
        if plan_id and sidecar.get("planId") != plan_id:
            raise AtomAdmissionError("TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN", "planId")
        fact = facts.get(fid)
        if fact is None:
            raise AtomAdmissionError("TARGET_ATTRIBUTION_FACT_NOT_IN_PLAN", fid)
        spec = REGISTRY["relations"].get(fact.get("relation")) or {}
        _join_sidecar(fact, spec, sidecar, closures, inputs)
    _admit_provider_occupancy_conflicts(items, facts)


def _admit_selected_imports(inputs: dict) -> None:
    selected = list(inputs.get("planSelectedImportIds") or [])
    wrappers = inputs.get("imports") or {}
    payloads = inputs.get("importPayloads") or {}
    observations = inputs.get("importObservations") or {}
    for iid in selected:
        if iid not in wrappers:
            raise AtomAdmissionError("ATOM_IMPORT_WRAPPER_MISSING", iid)
        _require_wrapper_flags(wrappers[iid], iid, inputs)
        _import_scope(wrappers[iid], inputs)
        _join_observation_payload(wrappers[iid], payloads.get(iid), observations.get(iid), iid)


def _first_party_identities(evaluation_native_id, universe, kind, inventories, plan, package_manifest_path=None):
    triples, rows = _distinct_identities(
        evaluation_native_id, universe, inventories, plan, kind, package_manifest_path
    )
    return set(triples), _coherent_rows(rows)


def _join_sidecar(fact: dict, spec: dict, sidecar: dict, closures: dict, inputs: dict) -> None:
    pc = sidecar.get("producerClosure")
    if pc != fact.get("producerClosure"):
        raise AtomAdmissionError("TARGET_ATTRIBUTION_PRODUCER_MISMATCH")
    if (closures.get(pc) or {}).get("kind") != "provider":
        raise AtomAdmissionError("TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER")
    if sidecar.get("targetUniverse") != fact.get("targetUniverse"):
        raise AtomAdmissionError("TARGET_ATTRIBUTION_UNIVERSE_MISMATCH")
    field = spec.get("targetNativeIdField")
    rungs = spec.get("endpointTargetRungs")
    if not field or (rungs and fact.get("resolution") not in rungs):
        raise AtomAdmissionError("TARGET_ATTRIBUTION_FIELD_NOT_ON_RUNG")
    if sidecar.get("targetNativeId") != (fact.get("payload") or {}).get(field):
        raise AtomAdmissionError("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH")
    if sidecar.get("occupancy") == "first-party" and sidecar.get("logicalPath") is not None:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_LOGICAL_PATH_ON_FIRST_PARTY")
    if sidecar.get("kind") == "package" and sidecar.get("logicalPath") is not None:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_LOGICAL_PATH_ON_PACKAGE")
    if sidecar.get("kind") != "symbol" and sidecar.get("exported") is not None:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_EXPORTED_NOT_SYMBOL")
    if sidecar.get("kind") != "package" and sidecar.get("packageManifestPath") is not None:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_PACKAGE_MANIFEST_NOT_PACKAGE")
    if sidecar.get("kind") == "package" and sidecar.get("occupancy") in ("first-party", "external"):
        if not sidecar.get("packageManifestPath"):
            raise AtomAdmissionError("TARGET_ATTRIBUTION_PACKAGE_MANIFEST_REQUIRED")
    if sidecar.get("occupancy") == "unknown" and sidecar.get("packageManifestPath") is not None:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_PACKAGE_PATH_FORBIDDEN")
    occ = sidecar.get("occupancy")
    ev = sidecar.get("evaluationNativeId")
    if occ == "first-party":
        if ev is None:
            raise AtomAdmissionError("TARGET_ATTRIBUTION_EVALUATION_ID_REQUIRED")
        sk = sidecar.get("kind")
        if sk == "file" and not LOGICAL_PATH_RE.match(ev):
            raise AtomAdmissionError("TARGET_ATTRIBUTION_EVALUATION_GRAMMAR", "file")
        if sk == "symbol":
            if not SUBJECT_ID_RE.match(ev):
                raise AtomAdmissionError("TARGET_ATTRIBUTION_EVALUATION_GRAMMAR", "symbol")
            if ev != sidecar.get("targetNativeId"):
                raise AtomAdmissionError("TARGET_ATTRIBUTION_SYMBOL_EVALUATION_ID_MISMATCH")
        if sk == "package" and (not isinstance(ev, str) or not ev):
            raise AtomAdmissionError("TARGET_ATTRIBUTION_EVALUATION_GRAMMAR", "package")
        if sk not in ("file", "symbol", "package"):
            raise AtomAdmissionError("TARGET_ATTRIBUTION_EVALUATION_GRAMMAR", "kind")
    elif ev is not None:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_EVALUATION_ID_FORBIDDEN")
    eph = _ephemeral_target(fact, spec, inputs)
    identities = eph.get("identities") or set()
    sk, ek = sidecar.get("kind"), eph.get("kind")
    if sk in ("file", "symbol", "package") and ek in ("file", "symbol", "package") and sk != ek:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_KIND_INVENTORY_DISAGREEMENT")
    se, ee = sidecar.get("exported"), eph.get("exported")
    if se in ("exported", "not-exported") and ee in ("exported", "not-exported") and se != ee:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_EXPORTED_INVENTORY_DISAGREEMENT")
    if sidecar.get("occupancy") == "external" and eph.get("occupancy") == "first-party":
        raise AtomAdmissionError("TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY")
    if sidecar.get("occupancy") == "first-party":
        plan = inputs.get("enumerationPlan")
        inventories = inputs.get("inventories") or []
        pmp = sidecar.get("packageManifestPath") if sk == "package" else None
        matched, _rows = _first_party_identities(
            ev, fact["targetUniverse"], sk, inventories, plan, pmp
        )
        if sk == "package":
            matched = {i for i in matched if i[1] == "package" and i[2] == ev and i[3] == pmp}
        else:
            matched = {i for i in matched if i[1] == sk and i[2] == ev}
        if len(matched) != 1:
            raise AtomAdmissionError("TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY")
    if sidecar.get("occupancy") == "first-party" and eph.get("occupancy") == "first-party":
        eph_id = (eph.get("kind"), eph.get("nativeId"), eph.get("packageManifestPath") or "")
        sc_id = (sidecar.get("kind"), ev, sidecar.get("packageManifestPath") or "")
        if eph_id != sc_id:
            raise AtomAdmissionError("TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT")


def _occupancy_key(sidecar: dict) -> tuple:
    return (
        sidecar.get("kind"),
        sidecar.get("evaluationNativeId"),
        sidecar.get("packageManifestPath") or "",
    )


def _admit_provider_occupancy_conflicts(items: dict, facts: dict) -> None:
    seen = {}
    for sidecar in items.values():
        if not isinstance(sidecar, dict) or sidecar.get("occupancy") != "first-party":
            continue
        fact = facts.get(sidecar.get("sourceFactId")) or {}
        key = (
            sidecar.get("producerClosure"),
            sidecar.get("targetUniverse"),
            sidecar.get("targetNativeId"),
        )
        occ = _occupancy_key(sidecar)
        if key in seen and seen[key] != occ:
            raise AtomAdmissionError("TARGET_ATTRIBUTION_PROVIDER_OCCUPANCY_CONFLICT")
        seen[key] = occ
        _ = fact


def _reconcile_attribution(fact: dict, spec: dict, inputs: dict) -> dict:
    eph = _ephemeral_target(fact, spec, inputs)
    sidecar = _sidecar_map(inputs).get(fact.get("factId"))
    if sidecar is None or isinstance(sidecar, list):
        return {
            "kind": eph.get("kind") or "unknown",
            "occupancy": eph.get("occupancy") or "unknown",
            "exported": eph.get("exported"),
            "nativeId": eph.get("nativeId") if eph.get("occupancy") == "first-party" else None,
            "payloadNativeId": eph.get("nativeId"),
            "packageManifestPath": eph.get("packageManifestPath"),
            "source": "ephemeral" if eph.get("occupancy") == "first-party" else "absent",
        }
    closures = inputs.get("closures") or {}
    _join_sidecar(fact, spec, sidecar, closures, inputs)
    sk, ek = sidecar.get("kind"), eph.get("kind")
    se, ee = sidecar.get("exported"), eph.get("exported")
    kind = ek if ek != "unknown" else sk
    exported = ee if ee not in (None, "unknown") else se
    if eph.get("occupancy") == "first-party":
        occ = "first-party"
        native = eph.get("nativeId")
        pmp = eph.get("packageManifestPath")
        source = "ephemeral"
        if sidecar.get("occupancy") == "first-party":
            native = sidecar.get("evaluationNativeId")
            if sidecar.get("kind") == "package":
                pmp = sidecar.get("packageManifestPath")
            source = "sidecar+ephemeral"
        return {"kind": kind, "occupancy": occ, "exported": exported, "nativeId": native,
                "payloadNativeId": sidecar.get("targetNativeId"), "packageManifestPath": pmp,
                "source": source}
    occ = sidecar.get("occupancy") or "unknown"
    if occ == "first-party":
        pmp = sidecar.get("packageManifestPath") if kind == "package" else None
        return {"kind": sidecar.get("kind"), "occupancy": "first-party", "exported": exported,
                "nativeId": sidecar.get("evaluationNativeId"),
                "payloadNativeId": sidecar.get("targetNativeId"),
                "packageManifestPath": pmp, "source": "sidecar"}
    if occ == "external":
        pmp = sidecar.get("packageManifestPath") if sidecar.get("kind") == "package" else None
        return {"kind": sidecar.get("kind"), "occupancy": "external", "exported": exported,
                "nativeId": sidecar.get("targetNativeId"),
                "payloadNativeId": sidecar.get("targetNativeId"),
                "packageManifestPath": pmp, "source": "sidecar"}
    return {"kind": kind if kind != "unknown" else (sidecar.get("kind") or "unknown"),
            "occupancy": "unknown", "exported": exported, "nativeId": None,
            "payloadNativeId": sidecar.get("targetNativeId"),
            "packageManifestPath": None, "source": "sidecar-unknown"}


def _source_value(fact: dict, spec: dict):
    field = spec.get("sourceField")
    if field == "anchors[0].path":
        anchors = fact.get("anchors") or []
        return anchors[0].get("path", ABSENT) if anchors else ABSENT
    payload = fact.get("payload") or {}
    return payload[field] if field in payload else ABSENT


def _rung_eq(rel: str, have: str, need: str) -> bool:
    return have == need and have in REGISTRY["relations"][rel]["ladder"]


def _rung_ge(rel: str, have: str, need: str) -> bool:
    ladder = REGISTRY["relations"][rel]["ladder"]
    if have not in ladder or need not in ladder:
        return False
    return ladder.index(have) >= ladder.index(need)


def _domain_of(universe: str, inputs: dict) -> str | None:
    return (inputs.get("universeDomains") or {}).get(universe)


def _family_of_universe(universe: str, inputs: dict) -> str | None:
    d = _domain_of(universe, inputs)
    return DOMAIN_FAMILY.get(d) if d else None


def _owed_source_bindings(rel: str, inputs: dict) -> tuple[list[dict], list[dict]]:
    """Available selected bindings. Program identity is universe U; contributors are (U, provider).

    Same U may repeat across workspace cells with different enumerators. Native owner does not
    forbid multiple selected providers on one U (enumeration-plan ProgramBindingV1.enumerator is
    per-binding). Incoming obligations are per (U, provider); expected source IDs still union by U.
    """
    plan = inputs.get("enumerationPlan")
    cap = REGISTRY["capabilityForRelation"].get(rel)
    available, unavailable = [], []
    if not plan:
        return available, unavailable
    for cell in plan.get("cells") or []:
        if cell.get("capabilityId") != cap:
            continue
        fam = LANG_FAMILY.get(cell.get("languageMode"))
        for b in cell.get("programBindings") or []:
            rec = dict(b)
            rec["_languageMode"] = cell.get("languageMode")
            rec["_family"] = fam
            rec["_enumerator"] = (b.get("enumerator") or {}).get("closureId")
            rec["_workspaceRoot"] = cell.get("workspaceRoot")
            if rec.get("universe") is None:
                unavailable.append(rec)
                continue
            available.append(rec)
    return available, unavailable


def _family_owed(fam, subj_fam) -> bool:
    if subj_fam and fam and fam != subj_fam:
        return False
    return True


def _native_occupancy(fact: dict, subject: dict, spec: dict, atom: dict, inputs: dict) -> str:
    endpoint = atom.get("endpoint", "source")
    u, k, n = subject["universe"], subject["kind"], subject["nativeSubjectId"]
    if endpoint == "source":
        if fact.get("sourceUniverse") != u:
            return NOMATCH
        val = _source_value(fact, spec)
        if val is ABSENT:
            return NOMATCH
        if val != n:
            return NOMATCH
        if k == "package" or spec.get("sourceSubjectKind") == "package":
            mp = (fact.get("payload") or {}).get("manifestPath")
            if mp != subject.get("packageManifestPath"):
                return NOMATCH
        return MATCH
    field = spec.get("targetNativeIdField")
    if not field:
        return NOMATCH
    tid = (fact.get("payload") or {}).get(field)
    if tid is None:
        return NOMATCH
    if fact.get("targetUniverse") != u:
        return NOMATCH
    attr = _reconcile_attribution(fact, spec, inputs)
    if attr.get("kind") in ("file", "symbol", "package") and attr["kind"] != k:
        return NOMATCH
    if attr.get("occupancy") == "external":
        return NOMATCH
    if attr.get("occupancy") == "first-party" and attr.get("nativeId") is not None:
        if attr.get("nativeId") != n:
            return NOMATCH
        if k == "package":
            pmp = attr.get("packageManifestPath")
            if pmp is None:
                return FUNK
            if pmp != subject.get("packageManifestPath"):
                return NOMATCH
        return MATCH
    # Occupancy unknown. Same-grammar exact-id (symbols) remains known nomatch when payload != N
    # so unrelated symbol facts are not poisoned. File/package inventory grammar is not
    # SubjectIdV1: payload inequality is not occupancy nomatch.
    if k == "symbol" and tid != n:
        return NOMATCH
    return FUNK


def _source_kind_of_fact(fact: dict, spec: dict, inputs: dict) -> str | None:
    val = _source_value(fact, spec)
    if val is ABSENT:
        return None
    rows = _lookup_rows(val, fact["sourceUniverse"], spec.get("sourceSubjectKind"),
                        inputs.get("inventories") or [], inputs.get("enumerationPlan"))
    kinds = {r["kind"] for r in rows}
    if len(kinds) == 1:
        return next(iter(kinds))
    if not kinds:
        return spec.get("sourceSubjectKind")
    return None


def _apply_native_filters(fact: dict, subject: dict, spec: dict, atom: dict, inputs: dict) -> str:
    acc = MATCH
    endpoint = atom.get("endpoint", "source")
    for flt in atom.get("filters") or []:
        field, cmp, value = flt["field"], flt["cmp"], flt["value"]
        if field == "resolution":
            got = _cmp_string(cmp, fact["resolution"], value)
        elif field == "universe":
            coord = fact["sourceUniverse"] if endpoint == "source" else fact["targetUniverse"]
            dom = _domain_of(coord, inputs)
            got = FUNK if dom is None else _cmp_string(cmp, dom, value)
        elif field == "confidenceMillionths":
            got = _cmp_int(cmp, fact.get("confidenceMillionths", 1000000), value)
        elif field == "subjectKind":
            sk = _source_kind_of_fact(fact, spec, inputs)
            got = FUNK if sk is None else _cmp_string(cmp, sk, value)
        elif field == "targetKind":
            attr = _reconcile_attribution(fact, spec, inputs)
            got = FUNK if attr.get("kind") == "unknown" else _cmp_string(cmp, attr["kind"], value)
        elif field == "subject":
            val = _source_value(fact, spec)
            got = FUNK if val is ABSENT else _cmp_string(cmp, val, value)
        elif field == "target":
            tfield = spec.get("targetNativeIdField") if atom["minResolution"] in (spec.get("endpointTargetRungs") or []) else spec.get("targetField")
            if tfield is None:
                raw = (fact.get("payload") or {}).get("targetModule", ABSENT)
                got = FUNK if raw is ABSENT or raw is None else _cmp_string(cmp, raw, value)
            else:
                raw = (fact.get("payload") or {}).get(tfield, ABSENT)
                got = FUNK if raw is ABSENT or raw is None else _cmp_string(cmp, raw, value)
        else:
            raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", field)
        acc = _and_fr(acc, got)
        if acc == NOMATCH:
            return NOMATCH
    return acc


def _coverages_exact(inputs: dict, rel: str, rung: str, source_u: str, target_u: str | None = None) -> list[tuple[str, dict]]:
    out = []
    for cid, cov in (inputs.get("coverages") or {}).items():
        key = cov.get("key") or {}
        if key.get("relation") != rel or key.get("resolution") != rung:
            continue
        if key.get("sourceUniverse") != source_u:
            continue
        if target_u is not None and key.get("targetUniverse") != target_u:
            continue
        out.append((cid, cov))
    return out


def _scopes_exact(inputs: dict, rel: str, rung: str, source_u: str) -> list[tuple[str, dict]]:
    out = []
    for sid, sc in (inputs.get("scopes") or {}).items():
        if sc.get("relation") != rel or sc.get("resolution") != rung:
            continue
        if sc.get("sourceUniverse") != source_u:
            continue
        out.append((sid, sc))
    return out


def _scope_descriptor(sc: dict) -> dict | None:
    if not all(k in sc for k in SUBJECT_SCOPE_FIELDS):
        return None
    subjects = sc["subjects"]
    if type(subjects) is not list:
        return None
    return {
        "schemaVersion": sc["schemaVersion"],
        "snapshotId": sc["snapshotId"],
        "sourceUniverse": sc["sourceUniverse"],
        "targetUniverse": sc["targetUniverse"],
        "relation": sc["relation"],
        "resolution": sc["resolution"],
        "enumeratorClosure": sc["enumeratorClosure"],
        "subjects": sorted(subjects, key=C.canonical),
    }


def _is_owner_admission(exc: BaseException) -> bool:
    """Native and identity-model each load canonical.py; catch the owner AdmissionError class."""
    if isinstance(exc, N.AdmissionError):
        return True
    return type(exc).__name__ == "AdmissionError"


def _derive_scope_commitment(sc: dict) -> str | None:
    desc = _scope_descriptor(sc)
    if desc is None:
        return None
    try:
        return N.subject_scope_commitment(desc)["subjectScopeCommitment"]
    except ValidationError as exc:
        raise AtomAdmissionError("ATOM_NATIVE_CARRIER", exc.message) from exc
    except Exception as exc:
        if _is_owner_admission(exc):
            raise AtomAdmissionError("ATOM_NATIVE_CARRIER", str(exc)) from exc
        raise


def _coverage_commitment(cov: dict) -> str | None:
    return (cov.get("key") or {}).get("subjectScopeCommitment")


def _pair_scope_coverages(sid: str, sc: dict, covs_all: list, inputs: dict) -> list:
    mapping = inputs.get("coverageScopes") or {}
    derived = _derive_scope_commitment(sc)
    found, seen = [], set()
    for cid, cov in covs_all:
        mapped = mapping.get(cid) == sid
        committed = bool(derived) and _coverage_commitment(cov) == derived
        if mapped or committed:
            if cid not in seen:
                seen.add(cid)
                found.append((cid, cov))
    return found


def _selected_universes(inputs: dict) -> set:
    out = set()
    for cell in (inputs.get("enumerationPlan") or {}).get("cells") or []:
        for b in cell.get("programBindings") or []:
            if b.get("universe"):
                out.add(b["universe"])
    return out


def _contributor_ids(bindings: list) -> list:
    out = []
    for b in bindings:
        pc = b.get("_enumerator")
        if pc not in out:
            out.append(pc)
    return out


def _incoming_groups(bindings: list, source_scopes: list) -> dict:
    """Seed provider groups from selected program contributors, not only emitted scopes."""
    contributors = _contributor_ids(bindings)
    tagged = [(sid, sc) for sid, sc in source_scopes if sc.get("enumeratorClosure")]
    if contributors:
        groups = {pc: [] for pc in contributors}
        if tagged:
            for sid, sc in tagged:
                groups.setdefault(sc.get("enumeratorClosure"), []).append((sid, sc))
            for sid, sc in source_scopes:
                if not sc.get("enumeratorClosure"):
                    for pc in contributors:
                        groups[pc].append((sid, sc))
        else:
            for pc in groups:
                groups[pc] = list(source_scopes)
        return groups
    if tagged:
        groups = {}
        for sid, sc in tagged:
            groups.setdefault(sc.get("enumeratorClosure"), []).append((sid, sc))
        return groups
    return {None: list(source_scopes)}


def _pair_attestation_coverages(att: dict, covs_u: list, inputs: dict) -> list:
    own, seen = [], set()
    scopes = inputs.get("scopes") or {}
    for sid in att.get("scopeRefs") or []:
        sc = scopes.get(sid)
        if sc is None:
            continue
        for cid, cov in _pair_scope_coverages(sid, sc, covs_u, inputs):
            if cid not in seen:
                seen.add(cid)
                own.append((cid, cov))
    return own


def _entry_blocks_complete_search(entry: dict) -> bool:
    if (entry or {}).get("coverage") != "complete":
        return True
    return ((entry or {}).get("resolutionCompleteness") or {}).get("state") in (
        "partial", "incomplete", "not-attempted",
    )


def _entry_from_cov(rel: str, cov: dict) -> dict:
    entry = cov.get("entry") or {}
    key = cov.get("key") or {}
    rc = entry.get("resolutionCompleteness")
    if not isinstance(rc, dict):
        rc = {
            "state": "not-attempted", "attempted": False, "examinedExhaustive": False,
            "stageTerminal": None, "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": [],
        }
    cw = entry.get("closedWorld")
    if not isinstance(cw, dict):
        cw = {
            "exportsClosed": "unknown", "entryPointsRecognized": "none",
            "nonliteralLoading": "none", "externalConsumers": "unknown",
            "dynamicDispatch": "not-applicable", "reasons": [], "deadCodeRepairEligible": False,
        }
    return {
        "resolution": key.get("resolution") or entry.get("resolution"),
        "coverage": entry.get("coverage", "unknown"),
        "confidenceMillionths": entry.get("confidenceMillionths", 1000000),
        "resolutionCompleteness": rc,
        "closedWorld": cw,
        "derivationKinds": entry.get("derivationKinds") or [],
        "deficiency": entry.get("deficiency"),
        "nativeCause": _typed_native_cause(entry.get("nativeCause")),
        "rungUnavailableBecause": entry.get("rungUnavailableBecause", ""),
    }


def _depends_chain(rel: str) -> list[dict]:
    out, seen = [], set()
    stack = list(N.DEPENDS_ON.get(rel, []))
    while stack:
        dep = stack.pop(0)
        drel = dep["relation"]
        if drel in seen:
            continue
        seen.add(drel)
        out.append(dep)
        stack.extend(N.DEPENDS_ON.get(drel, []))
    return out


def _conservative_entry(rel: str, covs: list[tuple[str, dict]]) -> tuple[dict, list[str]]:
    """AND-compose several same-relation partitions: missing completeness cannot be healed."""
    cited = [c[0] for c in covs]
    entries = [_entry_from_cov(rel, c[1]) for c in covs]
    if len(entries) == 1:
        return entries[0], cited
    coverage_rank = {"complete": 0, "partial": 1, "unknown": 2}
    state_rank = {"complete": 0, "not-applicable": 0, "partial": 1, "incomplete": 2, "not-attempted": 3}
    export_rank = {"closed": 0, "open": 1, "unknown": 2}
    worst = entries[0]
    for e in entries[1:]:
        if coverage_rank.get(e.get("coverage"), 2) > coverage_rank.get(worst.get("coverage"), 2):
            worst["coverage"] = e.get("coverage")
        rc, wrc = e.get("resolutionCompleteness") or {}, worst.get("resolutionCompleteness") or {}
        if state_rank.get(rc.get("state"), 3) > state_rank.get(wrc.get("state"), 3):
            worst["resolutionCompleteness"] = rc
        if e.get("confidenceMillionths", 1000000) < worst.get("confidenceMillionths", 1000000):
            worst["confidenceMillionths"] = e.get("confidenceMillionths", 1000000)
        cw, wcw = e.get("closedWorld") or {}, worst.get("closedWorld") or {}
        if export_rank.get(cw.get("exportsClosed"), 2) > export_rank.get(wcw.get("exportsClosed"), 2):
            worst["closedWorld"] = cw
        if e.get("deficiency") and not worst.get("deficiency"):
            worst["deficiency"] = e.get("deficiency")
            worst["nativeCause"] = e.get("nativeCause")
        kinds = list(dict.fromkeys(list(worst.get("derivationKinds") or []) + list(e.get("derivationKinds") or [])))
        worst["derivationKinds"] = kinds
    return worst, cited


def _unique_pairs(pairs: list) -> list:
    seen, out = set(), []
    for cid, cov in pairs:
        if cid in seen:
            continue
        seen.add(cid)
        out.append((cid, cov))
    return out


def _select_dep_coverages(drel: str, drung: str, source_u: str, want_t: str | None,
                          inputs: dict, current_subjects: set[str] | None, current_kind: str | None) -> list:
    """Native DEPENDS_ON: reachability→calls@resolved-callee; clones→declares@syntactic.

    Same sourceSubjectKind as the current subject: pair dep Coverage to current-source scopes
    containing those native ids. Different native kind: whole-source search of (S, T) (all
    partitions). Never take covs[0]. Unrelated source-subject partitions are not AND-composed
    into the current view. current_subjects is None for whole-source attestation (all S owed).
    """
    covs = _coverages_exact(inputs, drel, drung, source_u, want_t)
    if not covs:
        return []
    dep_kind = _source_kind_for_relation(drel)
    if current_subjects is None or (current_kind and dep_kind != current_kind):
        return covs
    paired = []
    dep_scopes = _scopes_exact(inputs, drel, drung, source_u)
    for sid, sc in dep_scopes:
        if not any(_scope_contains(sc, nid) for nid in current_subjects):
            continue
        paired.extend(_pair_scope_coverages(sid, sc, covs, inputs))
    if dep_scopes:
        return _unique_pairs(paired)
    mapping = inputs.get("coverageScopes") or {}
    mapped = []
    for cid, cov in covs:
        sid = mapping.get(cid)
        sc = (inputs.get("scopes") or {}).get(sid) if sid else None
        if sc is not None and any(_scope_contains(sc, nid) for nid in current_subjects):
            mapped.append((cid, cov))
    return _unique_pairs(mapped)


def _build_sufficiency_view(rel: str, min_rung: str, source_u: str, target_u: str | None,
                            primary_cov: dict, inputs: dict,
                            current_subjects: set[str] | None = None,
                            current_kind: str | None = None) -> tuple[dict, list[str]]:
    """Primary coverage plus actual recursive DEPENDS_ON coverages of this (S, T) partition."""
    view = {rel: _entry_from_cov(rel, primary_cov)}
    cited: list[str] = []
    want_t = target_u if target_u is not None else (primary_cov.get("key") or {}).get("targetUniverse")
    for dep in _depends_chain(rel):
        drel, drung = dep["relation"], dep["minResolution"]
        covs = _select_dep_coverages(drel, drung, source_u, want_t, inputs, current_subjects, current_kind)
        if not covs:
            continue
        entry, ids = _conservative_entry(drel, covs)
        view[drel] = entry
        cited.extend(ids)
    return view, cited


def _entry_from_attestation(rel: str, min_rung: str, att: dict) -> dict:
    return {
        "resolution": min_rung,
        "coverage": att["coverage"],
        "confidenceMillionths": 1000000,
        "resolutionCompleteness": att["resolutionCompleteness"],
        "closedWorld": att["closedWorld"],
        "derivationKinds": [],
        "deficiency": None,
        "nativeCause": None,
        "rungUnavailableBecause": "",
    }


def _build_attestation_view(rel: str, min_rung: str, source_u: str, target_u: str,
                            att: dict, inputs: dict) -> tuple[dict, list[str]]:
    """Whole-source attestation owes every S partition of DEPENDS_ON at (S, T)."""
    view = {rel: _entry_from_attestation(rel, min_rung, att)}
    cited: list[str] = []
    for dep in _depends_chain(rel):
        drel, drung = dep["relation"], dep["minResolution"]
        covs = _select_dep_coverages(drel, drung, source_u, target_u, inputs, None, None)
        if not covs:
            continue
        entry, ids = _conservative_entry(drel, covs)
        view[drel] = entry
        cited.extend(ids)
    return view, cited


def _subject_module_path(subject: dict, inputs: dict) -> str | None:
    rows = _lookup_rows(subject["nativeSubjectId"], subject["universe"], subject["kind"],
                        inputs.get("inventories") or [], inputs.get("enumerationPlan"),
                        subject.get("packageManifestPath"))
    if len(rows) != 1:
        return None
    return rows[0].get("path")


def _target_affected(facts: dict, subject: dict, source_u: str, inputs: dict) -> tuple[bool, list]:
    """Conservative: unknown module spelling => affected True + cause, never 'unaffected' by id compare."""
    causes = []
    path = _subject_module_path(subject, inputs)
    affected = False
    unknown = False
    for fact in facts.values():
        if fact.get("relation") != "unresolved-edge" or fact.get("sourceUniverse") != source_u:
            continue
        ts = (fact.get("payload") or {}).get("targetScope")
        if ts in ("universe", "unknown", "external"):
            affected = True
            continue
        if ts == "module":
            tm = (fact.get("payload") or {}).get("targetModule")
            if tm is None:
                unknown = True
                continue
            if path is not None and (tm == path or (isinstance(tm, str) and (path == tm or path.startswith(str(tm).rstrip("/") + "/")))):
                affected = True
            else:
                unknown = True
    if unknown and not affected:
        causes.append(_cause("unresolved-edge-target-unattributed", universe=source_u))
        affected = True
    return affected, causes


def _export_flag(subject: dict, inputs: dict) -> tuple[bool, list]:
    rows = _lookup_rows(subject["nativeSubjectId"], subject["universe"], subject["kind"],
                        inputs.get("inventories") or [], inputs.get("enumerationPlan"),
                        subject.get("packageManifestPath"))
    if not rows:
        return True, [_cause("target-export-unknown", universe=subject["universe"])]
    flags = {r.get("exported") for r in rows if r.get("kind") == "symbol"}
    if subject["kind"] != "symbol":
        return False, []
    if flags == {"exported"}:
        return True, []
    if flags == {"not-exported"}:
        return False, []
    return True, [_cause("target-export-unknown", universe=subject["universe"])]


def _sufficiency(rel: str, min_rung: str, view: dict, subject: dict, quantifier: str,
                 inputs: dict, source_u: str, endpoint: str) -> dict:
    """target_exported / target_affected apply only to incoming (endpoint=target).

    Native sufficiency_v2 closed-world is unknown *incoming* use of an exported target.
    Outgoing source-partition RC-2 already counts that partition's own referrers; unknown
    external-consumer closure does not decide whether this source made an outgoing edge.
    """
    req = {
        "relation": rel, "minResolution": min_rung, "completeness": "complete",
        "quantifier": quantifier, "minConfidenceMillionths": 0, "derivationPolicy": "any",
        "unresolvedEdgePolicy": "forbid", "externalConsumerPolicy": "forbid",
    }
    if endpoint == "target":
        exported, extra = _export_flag(subject, inputs)
        affected, acauses = _target_affected(inputs.get("facts") or {}, subject, source_u, inputs)
    else:
        exported, extra, affected, acauses = False, [], False, []
    su = N.sufficiency_v2(req, view, target_exported=exported, target_affected=affected)
    su = dict(su)
    su["extraCauses"] = extra + acauses
    return su


def _inventory_population(kind: str, universe: str, inventories: list, plan: dict) -> dict:
    """ids from inventory rows only (file also examinedPaths). Extents never mint symbol/package IDs.
    Package ids stay nativeSubjectId (packageName) because native scope membership is packageName.
    partial/unavailable => population_unknown, no fake IDs."""
    ids = set()
    unknown = False
    saw = False
    for inv in inventories:
        if inv.get("kind") != kind:
            continue
        u = _inventory_universe(inv, plan)
        if u != universe:
            continue
        saw = True
        st = inv.get("state")
        if st == "unavailable":
            unknown = True
            continue
        if st == "partial":
            unknown = True
        for row in inv.get("rows") or []:
            ids.add(row["nativeSubjectId"])
        if kind == "file":
            for p in inv.get("examinedPaths") or []:
                ids.add(p)
    if not saw:
        unknown = True
    return {"ids": ids, "unknown": unknown}


def _file_extent_ids(binding: dict) -> set[str]:
    ids = set()
    for ext in binding.get("extents") or []:
        if ext.get("kind") == "file":
            ids.update(ext.get("paths") or [])
    return ids


def _expected_source_ids(binding: dict, kind: str, inventories: list, plan: dict) -> dict:
    pop = _inventory_population(kind, binding.get("universe"), inventories, plan)
    ids = set(pop["ids"])
    if kind == "file":
        ids |= _file_extent_ids(binding)
    return {"ids": ids, "unknown": pop["unknown"]}


def _scope_contains(sc: dict, native_id: str) -> bool:
    return native_id in (sc.get("subjects") or [])


def _coverages_for_current_source(inputs: dict, rel: str, rung: str, source_u: str, native_id: str) -> tuple[list, list, list]:
    """Coverages at EXACT rung whose associated scope contains current native_id only. No 1:1 fallback."""
    scopes = _scopes_exact(inputs, rel, rung, source_u)
    containing = [(sid, sc) for sid, sc in scopes if _scope_contains(sc, native_id)]
    covs_all = _coverages_exact(inputs, rel, rung, source_u, None)
    paired, unmatched = [], []
    for sid, sc in containing:
        found = _pair_scope_coverages(sid, sc, covs_all, inputs)
        if found:
            paired.extend(found)
        else:
            unmatched.append(sid)
    return paired, [s for s, _ in containing], unmatched


def _attestation_key(att: dict) -> tuple:
    return (att.get("planId"), att.get("providerClosure"), att.get("sourceUniverse"),
            att.get("targetUniverse"), att.get("relation"), att.get("minResolution"))


def _source_kind_for_relation(rel: str) -> str:
    spec = REGISTRY["relations"].get(rel) or {}
    return spec.get("sourceSubjectKind") or "symbol"


def _validate_incoming_rc_law(att: dict) -> None:
    try:
        N.validate_native("ResolutionCompletenessV2", att["resolutionCompleteness"])
        N.validate_native("ClosedWorldV2", att["closedWorld"])
    except ValidationError as exc:
        raise AtomAdmissionError("INCOMING_SEARCH_SCHEMA", exc.message) from exc
    except Exception as exc:
        if _is_owner_admission(exc):
            raise AtomAdmissionError("INCOMING_SEARCH_SCHEMA", str(exc)) from exc
        raise
    rc = att["resolutionCompleteness"]
    rung = att["minResolution"]
    resolved = rung in RESOLVED_RUNGS
    if not resolved:
        if rc["state"] != "not-applicable" or rc["unresolvedEdgeCount"] != 0 or rc.get("attempted") or rc.get("unresolvedEdgeClasses"):
            raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "resolutionCompleteness")
    elif rc["state"] == "not-applicable":
        raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "resolutionCompleteness")
    if att.get("coverage") == "complete" and rc.get("examinedExhaustive") is not True:
        raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "examinedExhaustive")


def _admit_incoming_searches(inputs: dict) -> None:
    atts = inputs.get("incomingSearchAttestations") or []
    if not atts:
        return
    seen = {}
    closures = inputs.get("closures") or {}
    plan_id = inputs.get("planId")
    inventories = inputs.get("inventories") or []
    plan = inputs.get("enumerationPlan")
    for att in atts:
        try:
            Draft202012Validator(INCOMING_SEARCH_SCHEMA).validate(att)
        except ValidationError as exc:
            raise AtomAdmissionError("INCOMING_SEARCH_SCHEMA", exc.message) from exc
        key = _attestation_key(att)
        if key in seen:
            raise AtomAdmissionError("INCOMING_SEARCH_DUPLICATE")
        seen[key] = att
        if plan_id and att["planId"] != plan_id:
            raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "planId")
        rel, rung = att["relation"], att["minResolution"]
        if rel not in REGISTRY["relations"]:
            raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "relation")
        if rung not in REGISTRY["relations"][rel]["ladder"]:
            raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "minResolution")
        _validate_incoming_rc_law(att)
        pc = att["providerClosure"]
        if (closures.get(pc) or {}).get("kind") != "provider":
            raise AtomAdmissionError("INCOMING_SEARCH_UNSELECTED_PROVIDER")
        available, _ = _owed_source_bindings(rel, inputs)
        candidates = [b for b in available if b.get("universe") == att["sourceUniverse"]]
        if not candidates:
            raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "sourceUniverse")
        tu = att["targetUniverse"]
        domains = inputs.get("universeDomains") or {}
        selected = _selected_universes(inputs)
        if tu not in selected and tu not in domains:
            raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "targetUniverse")
        if tu in domains and domains[tu] not in PORTABLE_DOMAINS:
            raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "targetUniverse")
        enumerators = {b.get("_enumerator") for b in candidates if b.get("_enumerator")}
        if enumerators and pc not in enumerators:
            raise AtomAdmissionError("INCOMING_SEARCH_UNSELECTED_PROVIDER")
        s_scopes = _scopes_exact(inputs, rel, rung, att["sourceUniverse"])
        tagged = [(sid, sc) for sid, sc in s_scopes if sc.get("enumeratorClosure")]
        if tagged:
            owed_scope_ids = {sid for sid, sc in tagged if sc.get("enumeratorClosure") == pc}
        else:
            owed_scope_ids = {sid for sid, _sc in s_scopes}
        if set(att["scopeRefs"]) != owed_scope_ids:
            raise AtomAdmissionError("INCOMING_SEARCH_SCOPE_MISJOIN", "union")
        for sid in att["scopeRefs"]:
            sc = (inputs.get("scopes") or {}).get(sid)
            if sc is None:
                raise AtomAdmissionError("INCOMING_SEARCH_SCOPE_MISJOIN", sid)
            if sc.get("sourceUniverse") != att["sourceUniverse"] or sc.get("relation") != rel:
                raise AtomAdmissionError("INCOMING_SEARCH_SCOPE_MISJOIN", sid)
            if sc.get("resolution") != rung:
                raise AtomAdmissionError("INCOMING_SEARCH_SCOPE_MISJOIN", sid)
            enc = sc.get("enumeratorClosure")
            if enc is not None and enc != pc:
                raise AtomAdmissionError("INCOMING_SEARCH_UNSELECTED_PROVIDER")
        src_kind = _source_kind_for_relation(rel)
        locators = []
        for inv in inventories:
            if inv.get("kind") != src_kind:
                continue
            u = _inventory_universe(inv, plan)
            if u != att["sourceUniverse"]:
                continue
            b = _plan_binding(plan, inv["cellOrdinal"], inv["programOrdinal"]) if plan else None
            enc = (b.get("enumerator") or {}).get("closureId") if b else None
            locators.append((enc, inv))
        if enumerators and any(enc is not None for enc, _inv in locators):
            expected = {_inventory_raw_digest(inv) for enc, inv in locators if enc == pc}
        else:
            expected = {_inventory_raw_digest(inv) for _enc, inv in locators}
        if set(att["expectedInventoryRefs"]) != expected:
            raise AtomAdmissionError("INCOMING_SEARCH_INVENTORY_MISJOIN")
        covs_u = _coverages_exact(inputs, rel, rung, att["sourceUniverse"], att["targetUniverse"])
        own_covs = _pair_attestation_coverages(att, covs_u, inputs)
        if own_covs and att.get("completeSearch") is True:
            for _, cov in own_covs:
                if _entry_blocks_complete_search(cov.get("entry") or {}):
                    raise AtomAdmissionError("INCOMING_SEARCH_CANNOT_OVERRIDE_PARTIAL")


def _attestation_proves_search(att: dict) -> bool:
    return (
        att.get("completeSearch") is True
        and att.get("coverage") == "complete"
        and att.get("examinedExhaustive") is True
        and (att.get("resolutionCompleteness") or {}).get("examinedExhaustive") is True
    )


def _native_completeness(atom: dict, subject: dict, spec: dict, inputs: dict) -> dict:
    rel = atom["relation"]
    min_rung = atom["minResolution"]
    endpoint = atom.get("endpoint", "source")
    u, n = subject["universe"], subject["nativeSubjectId"]
    causes, cov_ids, scope_ids, defs = [], [], [], []
    available, unavailable = _owed_source_bindings(rel, inputs)
    subj_fam = _family_of_universe(u, inputs)
    for ub in unavailable:
        if not _family_owed(ub.get("_family"), subj_fam):
            causes.append(_cause("cross-family-edge-not-owed", universe=ub.get("universe")))
            continue
        if endpoint == "target":
            causes.append(_cause("unavailable-program-binding"))
    if not available and not unavailable:
        causes.append(_cause("missing-relation-coverage"))
        return {"complete": False, "unknown": True, "causes": causes,
                "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}
    src_kind = spec.get("sourceSubjectKind") or "symbol"
    resolved = min_rung in RESOLVED_RUNGS
    q_abs = "universal-negative" if resolved else "existential"
    q_all = q_abs if atom["op"] == "all-covered" or resolved else "existential"
    if atom["op"] == "all-covered":
        q_use = q_all
    else:
        q_use = q_abs

    def run_suff(view, source_u, extra_cids):
        cov_ids.extend(extra_cids)
        su = _sufficiency(rel, min_rung, view, subject, q_use, inputs, source_u, endpoint)
        defs.extend(su.get("causes") or [])
        if su.get("deficiency"):
            defs.append(su["deficiency"])
        causes.extend(su.get("extraCauses") or [])
        if not su.get("satisfied"):
            nc = None
            for _rel, ent in view.items():
                if isinstance(ent, dict) and ent.get("nativeCause"):
                    nc = ent.get("nativeCause")
                    break
            causes.append(_cause("coverage-unknown", universe=source_u, nativeCause=nc))
            return False
        return True

    plan = inputs.get("enumerationPlan") or {"cells": []}
    inventories = inputs.get("inventories") or []
    cur_kind = subject["kind"]

    if endpoint == "source":
        if not any(b.get("universe") == u for b in available):
            causes.append(_cause("selector-unbound"))
            return {"complete": False, "unknown": True, "causes": causes,
                    "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}
        paired, sids, unmatched = _coverages_for_current_source(inputs, rel, min_rung, u, n)
        scope_ids.extend(sids)
        if not sids:
            causes.append(_cause("uncovered-expected-source-subject", universe=u))
            return {"complete": False, "unknown": True, "causes": causes,
                    "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}
        for sid in unmatched:
            causes.append(_cause("scope-without-coverage", universe=u))
        if unmatched or not paired:
            return {"complete": False, "unknown": True, "causes": causes,
                    "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}
        ok = True
        for cid, cov in paired:
            cov_ids.append(cid)
            tu = (cov.get("key") or {}).get("targetUniverse")
            view, extra = _build_sufficiency_view(rel, min_rung, u, tu, cov, inputs,
                                                 current_subjects={n}, current_kind=cur_kind)
            if not run_suff(view, u, extra):
                ok = False
        blocking = [c for c in causes if c.get("code") != "cross-family-edge-not-owed"]
        unknown = bool(blocking) or not ok
        return {"complete": ok and not unknown, "unknown": unknown,
                "causes": causes, "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}

    ok_all, unknown = True, False
    by_u: dict[str, list] = {}
    for b in available:
        by_u.setdefault(b["universe"], []).append(b)
    for ub in unavailable:
        if _family_owed(ub.get("_family"), subj_fam):
            unknown = True
    for s, bindings in by_u.items():
        fam = bindings[0].get("_family") or _family_of_universe(s, inputs)
        if not _family_owed(fam, subj_fam):
            causes.append(_cause("cross-family-edge-not-owed", universe=s))
            continue
        exp_ids, exp_unknown = set(), False
        for b in bindings:
            exp = _expected_source_ids(b, src_kind, inventories, plan)
            exp_ids |= exp["ids"]
            exp_unknown = exp_unknown or exp["unknown"]
        if exp_unknown:
            causes.append(_cause("population-unknown", universe=s))
            unknown = True
        present = set()
        source_scopes = _scopes_exact(inputs, rel, min_rung, s)
        covs_s = _coverages_exact(inputs, rel, min_rung, s, None)
        atts = inputs.get("incomingSearchAttestations") or []
        groups = _incoming_groups(bindings, source_scopes)

        def _att_for(pc):
            for a in atts:
                if (a.get("sourceUniverse") == s and a.get("targetUniverse") == u
                        and a.get("relation") == rel and a.get("minResolution") == min_rung
                        and (pc is None or a.get("providerClosure") == pc)):
                    return a
            return None

        for sid, sc in source_scopes:
            scope_ids.append(sid)
            present.update(sc.get("subjects") or [])
        if exp_ids - present:
            causes.append(_cause("uncovered-expected-source-subject", universe=s))
            unknown = True
        for pc, scs in groups.items():
            att = _att_for(pc)
            att_ok = att is not None and _attestation_proves_search(att)
            if att_ok:
                view, extra = _build_attestation_view(rel, min_rung, s, u, att, inputs)
                if not run_suff(view, s, extra):
                    ok_all = False
                    unknown = True
            if not scs:
                if not att_ok:
                    causes.append(_cause("source-target-search-unattested", universe=s))
                    unknown = True
                    ok_all = False
                continue
            for sid, sc in scs:
                found_all = _pair_scope_coverages(sid, sc, covs_s, inputs)
                found_u = [(cid, cov) for cid, cov in found_all
                           if (cov.get("key") or {}).get("targetUniverse") == u]
                for cid, cov in found_all:
                    cov_ids.append(cid)
                    tu = cov["key"].get("targetUniverse")
                    view, extra = _build_sufficiency_view(
                        rel, min_rung, s, tu, cov, inputs,
                        current_subjects=set(sc.get("subjects") or []), current_kind=src_kind)
                    if not run_suff(view, s, extra):
                        ok_all = False
                        unknown = True
                if found_u or att_ok:
                    continue
                if found_all:
                    causes.append(_cause("source-target-search-unattested", universe=s))
                else:
                    causes.append(_cause("scope-without-coverage", universe=s))
                unknown = True
                ok_all = False
    return {"complete": ok_all and not unknown, "unknown": unknown,
            "causes": causes, "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}


def _eval_native(atom: dict, subject: dict, inputs: dict, spec: dict) -> dict:
    known, uncertain = [], []
    for fid, fact in (inputs.get("facts") or {}).items():
        if fact.get("relation") != atom["relation"]:
            continue
        if not _rung_ge(atom["relation"], fact.get("resolution", ""), atom["minResolution"]):
            continue
        occ = _native_occupancy(fact, subject, spec, atom, inputs)
        if occ == NOMATCH:
            continue
        fr = _apply_native_filters(fact, subject, spec, atom, inputs)
        status = _and_fr(occ, fr)
        if status == MATCH:
            known.append(fid)
        elif status == FUNK:
            uncertain.append(fid)
    comp = _native_completeness(atom, subject, spec, inputs)
    op, nlimit = atom["op"], atom.get("n")
    consumed = list(comp["coverageIds"])
    if op == "all-covered" and (atom.get("filters") or []) and uncertain:
        comp["unknown"] = True
        comp["causes"] = list(comp["causes"]) + [_cause("target-metadata-unknown")]
    val = UNK
    if op == "exists":
        if known:
            val = TRUE
        elif uncertain or comp["unknown"] or not comp["complete"]:
            val = UNK
        else:
            val = FALSE
    elif op == "none":
        if known:
            val = FALSE
        elif uncertain or comp["unknown"] or not comp["complete"]:
            val = UNK
        else:
            val = TRUE
    elif op == "count-at-most":
        if len(set(known)) > nlimit:
            val = FALSE
        elif uncertain or comp["unknown"] or not comp["complete"]:
            val = UNK
        else:
            val = TRUE
    else:
        val = TRUE if comp["complete"] and not comp["unknown"] and not uncertain else UNK
    return _result(
        value=val, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
        coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
        causes=comp["causes"], nativeDeficiencies=comp["nativeDeficiencies"],
        evaluationInputRefs=sorted(set(consumed)),
    )


def _addr(import_id: str, selector: str, ordinal) -> dict:
    return {"importId": import_id, "selector": selector, "ordinal": ordinal}


def _import_scope(wrapper: dict, inputs: dict) -> dict:
    digest = wrapper.get("scopeDigest")
    scopes = inputs.get("importScopes") or {}
    if digest and digest in scopes:
        sc = scopes[digest]
        Draft202012Validator(SCOPE_SCHEMA).validate(sc)
        return sc
    if inputs.get("importScopeAdapter") == "normalized-import-scope-descriptor" and isinstance(wrapper.get("scope"), dict):
        sc = wrapper["scope"]
        try:
            Draft202012Validator(SCOPE_SCHEMA).validate(sc)
        except ValidationError as exc:
            raise AtomAdmissionError("ATOM_IMPORT_SCOPE_UNSTATED", exc.message) from exc
        return sc
    raise AtomAdmissionError("ATOM_IMPORT_SCOPE_UNSTATED")


def _under_prefix(path: str, root: str) -> bool:
    internal = "" if root in (".", "") else root
    return N._under_unit(path, internal)


def _path_in_scope(scope: dict, path: str) -> bool:
    """Owner import-scope law: excluded, then workspaceRoots AND pathPrefixes (enumeration _in_scope)."""
    excluded = scope.get("excludedPathPrefixes") or []
    if "." in excluded:
        return False
    for e in excluded:
        if _under_prefix(path, e):
            return False
    roots = scope.get("workspaceRoots") or []
    if not roots or not any(_under_prefix(path, r) for r in roots):
        return False
    prefixes = scope.get("pathPrefixes") or []
    if prefixes and not any(_under_prefix(path, p) for p in prefixes):
        return False
    return True


def _logical_path(subject: dict, inventory_row: dict | None) -> str | None:
    if inventory_row and inventory_row.get("path"):
        return inventory_row["path"]
    if subject["kind"] == "file":
        return subject["nativeSubjectId"]
    if subject["kind"] == "package":
        return subject.get("packageManifestPath")
    return None


def _wrapper_relevant(wrapper: dict, subject: dict, inputs: dict, inventory_row: dict | None) -> bool:
    scope = _import_scope(wrapper, inputs)
    path = _logical_path(subject, inventory_row)
    if path is None:
        return True
    return _path_in_scope(scope, path)


def _history_in_extent(payload: dict, wrapper: dict, path: str, inputs: dict) -> str:
    cs = payload.get("collectionScope")
    if cs == "listed-paths":
        rows = payload.get("subjects") or []
        if any(r.get("path") == path for r in rows):
            return "in-scope"
        return "listed-missing"
    if cs in ("all-paths", "in-scope-paths"):
        if _path_in_scope(_import_scope(wrapper, inputs), path):
            return "in-scope"
        return "outside"
    return "outside"


def _runtime_occupancy(row: dict, subject: dict, inputs: dict) -> str:
    k = subject["kind"]
    plan = inputs.get("enumerationPlan")
    inventories = inputs.get("inventories") or []
    u = subject["universe"]
    if k == "file":
        if row.get("symbol") not in (None, ABSENT) and "symbol" in row:
            return NOMATCH
        return MATCH if row.get("path") == subject["nativeSubjectId"] else NOMATCH
    if k == "symbol":
        if "symbol" not in row or row.get("symbol") is None:
            return NOMATCH
        hits = _symbol_rows_by_path_qn(row.get("path"), row.get("symbol"), u, inventories, plan)
        nids = {h["nativeSubjectId"] for h in hits}
        if subject["nativeSubjectId"] not in nids:
            return NOMATCH
        if len(hits) > 1:
            return FUNK
        return MATCH
    return NOMATCH


def _runtime_subject_scalar(row: dict, subject: dict):
    if subject["kind"] == "file":
        return row.get("path", ABSENT)
    if subject["kind"] == "symbol":
        return row.get("symbol") if "symbol" in row else ABSENT
    return ABSENT


def _apply_import_filters(atom: dict, spec: dict, projected: dict) -> str:
    acc = MATCH
    for flt in atom.get("filters") or []:
        field, cmp, value = flt["field"], flt["cmp"], flt["value"]
        if field not in projected:
            raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", field)
        raw = projected[field]
        if raw is ABSENT or raw is None:
            acc = _and_fr(acc, FUNK)
            continue
        if field == "exitStatus":
            acc = _and_fr(acc, _cmp_int(cmp, raw, value))
        else:
            acc = _and_fr(acc, _cmp_string(cmp, raw, value))
    return acc


def _wrapper_flag(wrapper: dict, iid: str, inputs: dict, field: str):
    if field in wrapper:
        return wrapper[field]
    adapter = inputs.get("importFlagsAdapter") or {}
    row = adapter.get(iid) if isinstance(adapter, dict) else None
    if isinstance(row, dict):
        extra = sorted(set(row) - IMPORT_FLAG_KEYS)
        if extra:
            raise AtomAdmissionError("ATOM_IMPORT_FLAG_ADAPTER", ",".join(extra))
        if field in row:
            return row[field]
    return ABSENT


def _require_wrapper_flags(wrapper: dict, iid: str, inputs: dict) -> tuple:
    consumable = _wrapper_flag(wrapper, iid, inputs, "consumable")
    staleness = _wrapper_flag(wrapper, iid, inputs, "staleness")
    if consumable is ABSENT:
        raise AtomAdmissionError("ATOM_IMPORT_CONSUMABLE_UNSTATED")
    if staleness is ABSENT:
        raise AtomAdmissionError("ATOM_IMPORT_STALENESS_UNSTATED")
    return consumable, staleness


def _obs_payload_joins(kind: str, payload: dict) -> dict:
    if not isinstance(payload, dict):
        return {}
    if kind == "runtime":
        out = {}
        if "observationWindow" in payload:
            out["window"] = payload["observationWindow"]
        if "observedPopulation" in payload:
            out["population"] = payload["observedPopulation"]
        return out
    if kind == "test":
        return {"selection": payload["selection"]} if "selection" in payload else {}
    if kind == "history":
        rr = payload.get("revisionRange")
        if isinstance(rr, dict) and "from" in rr and "to" in rr:
            return {"revisionRange": {"from": rr["from"], "to": rr["to"]}}
        return {}
    return {}


def _join_observation_payload(wrapper: dict, payload, obs, iid: str) -> None:
    """Nonnull observation claims must equal the payload owner fields. Contrary adapters refuse."""
    if not isinstance(obs, dict):
        return
    kind = wrapper.get("kind")
    joins = _obs_payload_joins(kind, payload or {})
    for field in ("window", "population", "selection", "revisionRange"):
        if field not in obs or obs[field] is None:
            continue
        if field not in joins or not C.equal_typed(obs[field], joins[field]):
            raise AtomAdmissionError("ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN", iid + ":" + field)


def _import_complete_runtime(wrapper: dict, payload: dict, obs: dict) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    window = payload.get("observationWindow") if isinstance(payload, dict) else None
    pop = payload.get("observedPopulation") if isinstance(payload, dict) else None
    if window is None or pop in (None, "unknown"):
        return False
    return True


def _import_complete_history(wrapper: dict, payload: dict) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    if (payload.get("revisionRange") or {}).get("truncated") is True:
        return False
    return True


def _import_complete_test(wrapper: dict, payload: dict, obs: dict, consumable, staleness) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    if staleness != "current" or consumable is not True:
        return False
    sel = payload.get("selection") if isinstance(payload, dict) else None
    return bool(sel and sel.get("completenessEstablished") is True)


def _test_process_result(payload: dict) -> str:
    if payload.get("timedOut") is True or payload.get("signal") is not None or payload.get("exitStatus") is None:
        return "error"
    tests = payload.get("tests") or []
    if any(t.get("outcome") == "error" for t in tests):
        return "error"
    if payload.get("exitStatus") != 0 or any(t.get("outcome") == "fail" for t in tests):
        return "failed"
    return "passed"


def _icause(code: str, kind: str, **extra) -> dict:
    return _cause(code, evidenceKind=kind, nativeCause=None, **extra)


def _eval_imported(atom: dict, subject: dict, inputs: dict, spec: dict) -> dict:
    kind = spec["evidenceKind"]
    selected = list(inputs.get("planSelectedImportIds") or [])
    wrappers = inputs.get("imports") or {}
    payloads = inputs.get("importPayloads") or {}
    observations = inputs.get("importObservations") or {}
    inventories = inputs.get("inventories") or []
    plan = inputs.get("enumerationPlan")
    inv_rows = _lookup_rows(subject["nativeSubjectId"], subject["universe"], subject["kind"], inventories, plan,
                            subject.get("packageManifestPath"))
    inv_row = inv_rows[0] if len(inv_rows) == 1 else None
    flag_by_id = {}
    for iid in selected:
        if iid not in wrappers:
            raise AtomAdmissionError("ATOM_IMPORT_WRAPPER_MISSING", iid)
        flag_by_id[iid] = _require_wrapper_flags(wrappers[iid], iid, inputs)
        _import_scope(wrappers[iid], inputs)

    owed = []
    for iid in selected:
        w = wrappers[iid]
        if w.get("kind") != kind:
            continue
        if not _wrapper_relevant(w, subject, inputs, inv_row):
            continue
        owed.append(iid)
    consumed = list(owed)
    if not owed:
        return _result(value=UNK, kind="imported-atom", evaluationInputRefs=consumed,
                       causes=[_icause("zero-owed-wrappers", kind), _icause("evidence-kind-unavailable", kind)])

    known, uncertain = [], []
    causes = []
    covering_complete = True

    for iid in owed:
        w = wrappers[iid]
        p = payloads.get(iid) or {}
        obs = observations.get(iid)
        consumable, staleness = flag_by_id[iid]
        if consumable is not True or staleness != "current":
            causes.append(_icause("import-unmapped-only", kind, importId=iid))
            covering_complete = False
            continue
        if kind == "runtime":
            wrap_complete = _import_complete_runtime(w, p, obs or {})
            if not wrap_complete:
                covering_complete = False
                if w.get("completeness") == "partial":
                    causes.append(_icause("wrapper-partial", kind, importId=iid))
                elif p.get("observationWindow") is None or p.get("observedPopulation") in (None, "unknown"):
                    causes.append(_icause("observation-window-insufficient", kind, importId=iid))
                else:
                    causes.append(_icause("incomplete-observation", kind, importId=iid))
            covering, matched, unobs = [], [], []
            rows = p.get("subjects") or []
            for i, row in enumerate(rows):
                occ = _runtime_occupancy(row, subject, inputs)
                if occ == NOMATCH:
                    continue
                if occ == FUNK:
                    uncertain.append(_addr(iid, "runtime-subject", i))
                    causes.append(_icause("overload-ambiguous", kind, importId=iid))
                    continue
                obs_v = row.get("observability")
                addr = _addr(iid, "runtime-subject", i)
                if obs_v in ("unobservable", "unmapped"):
                    unobs.append(addr)
                    uncertain.append(addr)
                    causes.append(_icause("unobservable-subject" if obs_v == "unobservable" else "unmapped-subject",
                                          kind, importId=iid))
                    continue
                if obs_v in ("observed-hit", "observable-unhit"):
                    covering.append(addr)
                    proj = {
                        "observability": obs_v,
                        "subject": _runtime_subject_scalar(row, subject),
                        "resolution": "observed",
                        "subjectKind": subject["kind"],
                    }
                    fr = _apply_import_filters(atom, spec, proj)
                    if fr == MATCH:
                        matched.append(addr)
                    elif fr == FUNK:
                        uncertain.append(addr)
            if len(matched) > 1:
                raise AtomAdmissionError("ATOM_RUNTIME_ROW_AMBIGUOUS", iid)
            known.extend(matched)
            if not covering and unobs:
                covering_complete = False
            elif not covering and wrap_complete:
                covering_complete = False
                causes.append(_icause("no-consumable-row", kind, importId=iid))
        elif kind == "history":
            wrap_complete = _import_complete_history(w, p)
            if not wrap_complete:
                covering_complete = False
                if w.get("completeness") == "partial":
                    causes.append(_icause("wrapper-partial", kind, importId=iid))
                if (p.get("revisionRange") or {}).get("truncated"):
                    causes.append(_icause("history-truncated", kind, importId=iid))
                else:
                    causes.append(_icause("incomplete-observation", kind, importId=iid))
            path = _logical_path(subject, inv_row)
            if path is None:
                causes.append(_icause("target-metadata-unknown", kind, importId=iid))
                covering_complete = False
                continue
            extent = _history_in_extent(p, w, path, inputs)
            if extent == "listed-missing":
                causes.append(_icause("history-outside-collection-scope", kind, importId=iid))
                covering_complete = False
                continue
            if extent == "outside":
                causes.append(_icause("history-outside-collection-scope", kind, importId=iid))
                covering_complete = False
                continue
            rows = p.get("subjects") or []
            for i, row in enumerate(rows):
                if row.get("path") != path:
                    continue
                proj = {
                    "subject": row.get("path"),
                    "resolution": "observed",
                    "subjectKind": subject["kind"],
                }
                fr = _apply_import_filters(atom, spec, proj)
                addr = _addr(iid, "history-subject", i)
                if fr == MATCH:
                    known.append(addr)
                elif fr == FUNK:
                    uncertain.append(addr)
        elif kind == "test":
            wrap_complete = _import_complete_test(w, p, obs or {}, consumable, staleness)
            if not wrap_complete:
                covering_complete = False
                if w.get("completeness") == "partial":
                    causes.append(_icause("wrapper-partial", kind, importId=iid))
                causes.append(_icause("test-completeness-not-established", kind, importId=iid))
            if spec.get("observationAddressSelector") == "test-execution":
                pr = _test_process_result(p)
                proj = {
                    "testResult": pr,
                    "exitStatus": p.get("exitStatus", ABSENT),
                    "resolution": "observed",
                    "subjectKind": subject["kind"],
                    "subject": _logical_path(subject, inv_row) or ABSENT,
                }
                fr = _apply_import_filters(atom, spec, proj)
                addr = _addr(iid, "test-execution", None)
                if fr == MATCH:
                    known.append(addr)
                elif fr == FUNK:
                    uncertain.append(addr)
                    if p.get("exitStatus") is None:
                        causes.append(_icause("null-exit-status", kind, importId=iid))
            else:
                tests = p.get("tests") or []
                path = _logical_path(subject, inv_row)
                for i, row in enumerate(tests):
                    if "subjectPath" not in row:
                        continue
                    if subject["kind"] != "file" or row.get("subjectPath") != path:
                        continue
                    proj = {
                        "testResult": row.get("outcome"),
                        "subject": row.get("subjectPath"),
                        "resolution": "observed",
                        "subjectKind": subject["kind"],
                    }
                    fr = _apply_import_filters(atom, spec, proj)
                    if fr == MATCH:
                        known.append(_addr(iid, "test-case", i))
                    elif fr == FUNK:
                        uncertain.append(_addr(iid, "test-case", i))

    op, nlimit = atom["op"], atom.get("n")
    if op == "exists" and known:
        return _result(value=TRUE, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=consumed)
    if op == "none" and known:
        return _result(value=FALSE, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=consumed)
    if op == "count-at-most" and len(known) > nlimit:
        return _result(value=FALSE, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=consumed)
    incomplete = (not covering_complete) or any(c["code"] in {
        "incomplete-observation", "unobservable-subject", "unmapped-subject", "no-consumable-row",
        "import-unmapped-only", "history-outside-collection-scope", "history-truncated",
        "test-completeness-not-established", "wrapper-partial", "null-exit-status",
        "overload-ambiguous", "target-metadata-unknown",
    } for c in causes) or bool(uncertain)
    if op == "exists":
        val = FALSE if not incomplete else UNK
        return _result(value=val, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=consumed)
    if op == "none":
        val = TRUE if not incomplete else UNK
        return _result(value=val, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=consumed)
    if op == "count-at-most":
        val = TRUE if not incomplete else UNK
        return _result(value=val, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=consumed)
    val = TRUE if not incomplete else UNK
    if kind == "runtime" and not known and any(c["code"] == "no-consumable-row" for c in causes):
        val = UNK
    return _result(value=val, kind="imported-atom", knownObservationAddresses=known,
                   uncertainObservationAddresses=uncertain, causes=causes,
                   evaluationInputRefs=consumed)
