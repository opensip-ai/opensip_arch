"""Full-scan atom reference (isolated successor). Not product runtime. Not full Run replay.

Owner-admitted native/import records only. Reuses native_evidence_model.v2.sufficiency_v2
and workflows_model.v1.glob_match. Root composes boolean nodes, findings, gating.
"""
from __future__ import annotations

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
    "incomingSearchAttestations", "planId", "blobs",
})


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
FF_SCHEMA = REGISTRY["$defs"]["FieldFilterSuccessorV1"]
LANG_FAMILY = {}
for fam, row in REGISTRY["engineFamilies"]["families"].items():
    for mode in row["languageModes"]:
        LANG_FAMILY[mode] = fam
DOMAIN_FAMILY = {row["universeDomain"]: fam for fam, row in REGISTRY["engineFamilies"]["families"].items()}
GLOB_OK = re.compile(r"^[^\\\u0000]+$")


class AtomAdmissionError(Exception):
    def __init__(self, key: str, detail: str = ""):
        self.key = key
        self.detail = detail
        super().__init__(key + (": " + detail if detail else ""))


def evaluate_atom(atom: dict, subject: dict, inputs: dict) -> dict:
    if not isinstance(inputs, dict):
        raise AtomAdmissionError("ATOM_INPUTS_NOT_RECORD")
    extra = sorted(set(inputs) - CLOSED_INPUT_KEYS)
    if extra:
        raise AtomAdmissionError("ATOM_INPUT_KEY_UNKNOWN", ",".join(extra))
    _admit_subject(subject)
    spec = _admit_atom(atom, subject)
    _admit_incoming_searches(atom, inputs)
    if spec["plane"] == "native":
        return _eval_native(atom, subject, inputs, spec)
    return _eval_imported(atom, subject, inputs, spec)


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
        key = json.dumps(c, sort_keys=True, separators=(",", ":"))
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return sorted(out, key=lambda c: json.dumps(c, sort_keys=True, separators=(",", ":")))


def _cause(code: str, **extra) -> dict:
    rec = {"code": code}
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


def _distinct_identities(native_id: str, universe: str, inventories: list, plan: dict | None, kind: str | None = None):
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
            triples.add((u, row["kind"], native_id))
            rows.append(row)
    return triples, rows


def _lookup_rows(native_id: str, universe: str, kind: str | None, inventories: list, plan: dict | None) -> list:
    _, rows = _distinct_identities(native_id, universe, inventories, plan, kind)
    return rows


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


def _ephemeral_target(fact: dict, spec: dict, inputs: dict) -> dict:
    field = spec.get("targetNativeIdField")
    if not field:
        return {"kind": "unknown", "occupancy": "unknown", "exported": None, "nativeId": None}
    nid = (fact.get("payload") or {}).get(field)
    if nid is None:
        return {"kind": "unknown", "occupancy": "unknown", "exported": None, "nativeId": None}
    plan = inputs.get("enumerationPlan")
    inventories = inputs.get("inventories") or []
    triples, rows = _distinct_identities(nid, fact["targetUniverse"], inventories, plan)
    if len(triples) == 1:
        row = rows[0]
        return {
            "kind": row["kind"], "occupancy": "first-party",
            "exported": row.get("exported") if row["kind"] == "symbol" else None, "nativeId": nid,
        }
    if len(triples) == 0:
        return {"kind": "unknown", "occupancy": "unknown", "nativeId": nid, "exported": None}
    return {"kind": "unknown", "occupancy": "unknown", "nativeId": nid, "exported": None, "ambiguous": True}


def _reconcile_attribution(fact: dict, spec: dict, inputs: dict) -> dict:
    eph = _ephemeral_target(fact, spec, inputs)
    sidecar = (inputs.get("targetAttributions") or {}).get(fact["factId"])
    closures = inputs.get("closures") or {}
    if sidecar is None:
        return eph
    pc = sidecar.get("producerClosure")
    if pc != fact.get("producerClosure"):
        raise AtomAdmissionError("TARGET_ATTRIBUTION_PRODUCER_MISMATCH")
    if (closures.get(pc) or {}).get("kind") != "provider":
        raise AtomAdmissionError("TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER")
    if sidecar.get("targetUniverse") != fact.get("targetUniverse"):
        raise AtomAdmissionError("TARGET_ATTRIBUTION_UNIVERSE_MISMATCH")
    field = spec.get("targetNativeIdField")
    if field and sidecar.get("targetNativeId") != (fact.get("payload") or {}).get(field):
        raise AtomAdmissionError("TARGET_ATTRIBUTION_NATIVE_ID_MISMATCH")
    sk, ek = sidecar.get("kind"), eph.get("kind")
    if sk in ("file", "symbol", "package") and ek in ("file", "symbol", "package") and sk != ek:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_KIND_INVENTORY_DISAGREEMENT")
    se, ee = sidecar.get("exported"), eph.get("exported")
    if se in ("exported", "not-exported") and ee in ("exported", "not-exported") and se != ee:
        raise AtomAdmissionError("TARGET_ATTRIBUTION_EXPORTED_INVENTORY_DISAGREEMENT")
    if sidecar.get("occupancy") == "external" and eph.get("occupancy") == "first-party":
        raise AtomAdmissionError("TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY")
    kind = ek if ek != "unknown" else sk
    occ = eph["occupancy"] if eph.get("occupancy") != "unknown" else sidecar.get("occupancy")
    exported = ee if ee not in (None, "unknown") else se
    return {"kind": kind, "occupancy": occ, "exported": exported, "nativeId": eph.get("nativeId")}


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
    """Dedup available bindings by universe across cells of the atom capability."""
    plan = inputs.get("enumerationPlan")
    cap = REGISTRY["capabilityForRelation"].get(rel)
    available, unavailable = [], []
    seen_u = set()
    if not plan:
        return available, unavailable
    for cell in plan.get("cells") or []:
        if cell.get("capabilityId") != cap:
            continue
        for b in cell.get("programBindings") or []:
            u = b.get("universe")
            if u is None:
                unavailable.append(b)
                continue
            if u in seen_u:
                continue
            seen_u.add(u)
            rec = dict(b)
            rec["_languageMode"] = cell.get("languageMode")
            rec["_family"] = LANG_FAMILY.get(cell.get("languageMode"))
            rec["_enumerator"] = (b.get("enumerator") or {}).get("closureId")
            available.append(rec)
    return available, unavailable


def _native_occupancy(fact: dict, subject: dict, spec: dict, atom: dict, inputs: dict) -> str:
    endpoint = atom.get("endpoint", "source")
    u, k, n = subject["universe"], subject["kind"], subject["nativeSubjectId"]
    if endpoint == "source":
        if fact.get("sourceUniverse") != u:
            return NOMATCH
        val = _source_value(fact, spec)
        if val is ABSENT:
            return NOMATCH
        return MATCH if val == n else NOMATCH
    field = spec.get("targetNativeIdField")
    if not field:
        return NOMATCH
    tid = (fact.get("payload") or {}).get(field)
    if tid is None or tid != n or fact.get("targetUniverse") != u:
        return NOMATCH
    attr = _reconcile_attribution(fact, spec, inputs)
    if attr.get("occupancy") == "external":
        return NOMATCH
    if attr.get("kind") in ("file", "symbol", "package") and attr["kind"] != k:
        return NOMATCH
    if attr.get("kind") == "unknown" or attr.get("occupancy") == "unknown":
        return FUNK
    return MATCH


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
    min_rung = atom["minResolution"]
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


def _entry_from_cov(rel: str, cov: dict) -> dict:
    entry = cov.get("entry") or {}
    key = cov.get("key") or {}
    rc = entry.get("resolutionCompleteness") or {
        "state": "not-applicable", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": [],
    }
    return {
        "resolution": key.get("resolution") or entry.get("resolution"),
        "coverage": entry.get("coverage", "unknown"),
        "confidenceMillionths": entry.get("confidenceMillionths", 1000000),
        "resolutionCompleteness": rc,
        "closedWorld": entry.get("closedWorld") or {"exportsClosed": "unknown"},
        "derivationKinds": entry.get("derivationKinds") or [],
        "deficiency": entry.get("deficiency"),
        "rungUnavailableBecause": entry.get("rungUnavailableBecause", ""),
    }


def _build_sufficiency_view(rel: str, min_rung: str, source_u: str, target_u: str | None, primary_cov: dict, inputs: dict) -> tuple[dict, list[str]]:
    """Primary coverage plus exact DEPENDS_ON coverages. No fictional complete entries."""
    view = {rel: _entry_from_cov(rel, primary_cov)}
    cited = []
    want_t = target_u if target_u is not None else (primary_cov.get("key") or {}).get("targetUniverse")
    for dep in N.DEPENDS_ON.get(rel, []):
        drel, drung = dep["relation"], dep["minResolution"]
        covs = _coverages_exact(inputs, drel, drung, source_u, want_t)
        if not covs:
            covs = _coverages_exact(inputs, drel, drung, source_u, None)
        if not covs:
            continue
        view[drel] = _entry_from_cov(drel, covs[0][1])
        cited.extend(c[0] for c in covs)
    return view, cited


def _subject_module_path(subject: dict, inputs: dict) -> str | None:
    rows = _lookup_rows(subject["nativeSubjectId"], subject["universe"], subject["kind"],
                        inputs.get("inventories") or [], inputs.get("enumerationPlan"))
    if not rows:
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
                        inputs.get("inventories") or [], inputs.get("enumerationPlan"))
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


def _sufficiency(rel: str, min_rung: str, view: dict, subject: dict, quantifier: str, inputs: dict, source_u: str) -> dict:
    req = {
        "relation": rel, "minResolution": min_rung, "completeness": "complete",
        "quantifier": quantifier, "minConfidenceMillionths": 0, "derivationPolicy": "any",
        "unresolvedEdgePolicy": "forbid", "externalConsumerPolicy": "forbid",
    }
    exported, extra = _export_flag(subject, inputs)
    affected, acauses = _target_affected(inputs.get("facts") or {}, subject, source_u, inputs)
    su = N.sufficiency_v2(req, view, target_exported=exported, target_affected=affected)
    su = dict(su)
    su["extraCauses"] = extra + acauses
    return su


def _inventory_population(kind: str, universe: str, inventories: list, plan: dict) -> dict:
    """ids from inventory rows only (file also examinedPaths). Extents never mint symbol/package IDs.
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


def _coverage_commitment(cov: dict) -> str | None:
    return (cov.get("key") or {}).get("subjectScopeCommitment")


def _scope_commitment(sc: dict) -> str | None:
    return sc.get("commitment") or sc.get("subjectScopeCommitment")


def _coverages_for_current_source(inputs: dict, rel: str, rung: str, source_u: str, native_id: str) -> tuple[list, list, list]:
    """Coverages at EXACT rung whose associated scope contains current native_id only."""
    scopes = _scopes_exact(inputs, rel, rung, source_u)
    containing = [(sid, sc) for sid, sc in scopes if _scope_contains(sc, native_id)]
    covs_all = _coverages_exact(inputs, rel, rung, source_u, None)
    paired = []
    for sid, sc in containing:
        cm = _scope_commitment(sc)
        found = [(cid, cov) for cid, cov in covs_all
                 if cm and _coverage_commitment(cov) == cm]
        paired.extend(found)
    if containing and not paired and len(containing) == 1 and len(covs_all) == 1:
        paired = list(covs_all)
    unmatched = [sid for sid, _ in containing] if containing and not paired else []
    return paired, [s for s, _ in containing], unmatched


def _attestation_key(att: dict) -> tuple:
    return (att.get("planId"), att.get("providerClosure"), att.get("sourceUniverse"),
            att.get("targetUniverse"), att.get("relation"), att.get("minResolution"))


def _admit_incoming_searches(atom: dict, inputs: dict) -> None:
    atts = inputs.get("incomingSearchAttestations") or []
    if not atts:
        return
    seen = {}
    plan = inputs.get("enumerationPlan") or {"cells": []}
    closures = inputs.get("closures") or {}
    plan_id = inputs.get("planId")
    available, _ = _owed_source_bindings(atom["relation"], inputs)
    by_u = {b["universe"]: b for b in available}
    inventories = inputs.get("inventories") or []
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
        pc = att["providerClosure"]
        if (closures.get(pc) or {}).get("kind") != "provider":
            raise AtomAdmissionError("INCOMING_SEARCH_UNSELECTED_PROVIDER")
        b = by_u.get(att["sourceUniverse"])
        if b is None or b.get("_enumerator") not in (None, pc) and b.get("_enumerator") != pc:
            if b is None:
                raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "sourceUniverse")
            if b.get("_enumerator") and b.get("_enumerator") != pc:
                raise AtomAdmissionError("INCOMING_SEARCH_UNSELECTED_PROVIDER")
        if att["relation"] != atom["relation"] or att["minResolution"] != atom["minResolution"]:
            raise AtomAdmissionError("INCOMING_SEARCH_JOIN", "relation/rung")
        for sid in att["scopeRefs"]:
            sc = (inputs.get("scopes") or {}).get(sid)
            if sc is None:
                raise AtomAdmissionError("INCOMING_SEARCH_SCOPE_MISJOIN", sid)
            if sc.get("sourceUniverse") != att["sourceUniverse"] or sc.get("relation") != att["relation"]:
                raise AtomAdmissionError("INCOMING_SEARCH_SCOPE_MISJOIN", sid)
            if sc.get("resolution") != att["minResolution"]:
                raise AtomAdmissionError("INCOMING_SEARCH_SCOPE_MISJOIN", sid)
        inv_digests = {inv.get("inventoryDigest") for inv in inventories if inv.get("inventoryDigest")}
        for d in att["expectedInventoryRefs"]:
            if inv_digests and d not in inv_digests:
                raise AtomAdmissionError("INCOMING_SEARCH_INVENTORY_MISJOIN", d)
        covs_u = _coverages_exact(inputs, att["relation"], att["minResolution"],
                                  att["sourceUniverse"], att["targetUniverse"])
        if covs_u and att.get("completeSearch") is True:
            for _, cov in covs_u:
                entry = cov.get("entry") or {}
                if entry.get("coverage") != "complete" or (entry.get("resolutionCompleteness") or {}).get("state") in (
                    "partial", "incomplete", "not-attempted",
                ):
                    raise AtomAdmissionError("INCOMING_SEARCH_CANNOT_OVERRIDE_PARTIAL")


def _native_completeness(atom: dict, subject: dict, spec: dict, inputs: dict) -> dict:
    rel = atom["relation"]
    min_rung = atom["minResolution"]
    endpoint = atom.get("endpoint", "source")
    u, n = subject["universe"], subject["nativeSubjectId"]
    causes, cov_ids, scope_ids, defs = [], [], [], []
    available, unavailable = _owed_source_bindings(rel, inputs)
    if unavailable:
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

    def run_suff(cov, source_u, target_u):
        view, extra_cids = _build_sufficiency_view(rel, min_rung, source_u, target_u, cov, inputs)
        cov_ids.extend(extra_cids)
        su = _sufficiency(rel, min_rung, view, subject, q_use, inputs, source_u)
        defs.extend(su.get("causes") or [])
        if su.get("deficiency"):
            defs.append(su["deficiency"])
        causes.extend(su.get("extraCauses") or [])
        if not su.get("satisfied"):
            causes.append(_cause("coverage-unknown", universe=source_u))
            return False
        return True

    plan = inputs.get("enumerationPlan") or {"cells": []}
    inventories = inputs.get("inventories") or []

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
        if unmatched or not paired:
            causes.append(_cause("scope-without-coverage", universe=u))
            return {"complete": False, "unknown": True, "causes": causes,
                    "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}
        ok = True
        for cid, cov in paired:
            cov_ids.append(cid)
            tu = (cov.get("key") or {}).get("targetUniverse")
            if not run_suff(cov, u, tu):
                ok = False
        unknown = bool(causes) or not ok
        return {"complete": ok and not unknown, "unknown": unknown,
                "causes": causes, "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}

    subj_fam = _family_of_universe(u, inputs)
    ok_all, unknown = True, False
    for b in available:
        s = b["universe"]
        fam = b.get("_family") or _family_of_universe(s, inputs)
        if subj_fam and fam and fam != subj_fam:
            causes.append(_cause("cross-family-edge-not-owed", universe=s))
            continue
        exp = _expected_source_ids(b, src_kind, inventories, plan)
        if exp["unknown"]:
            causes.append(_cause("population-unknown", universe=s))
            unknown = True
        present = set()
        for sid, sc in _scopes_exact(inputs, rel, min_rung, s):
            scope_ids.append(sid)
            present.update(sc.get("subjects") or [])
        if exp["ids"] - present:
            causes.append(_cause("uncovered-expected-source-subject", universe=s))
            unknown = True
        covs_s = _coverages_exact(inputs, rel, min_rung, s, None)
        cov_ids.extend(c[0] for c in covs_s)
        covs_u = [c for c in covs_s if c[1]["key"].get("targetUniverse") == u]
        # account EVERY represented partition S->V, not only S->U
        for cid, cov in covs_s:
            tu = cov["key"].get("targetUniverse")
            if not run_suff(cov, s, tu):
                ok_all = False
                unknown = True
        if not covs_u:
            att = None
            for a in inputs.get("incomingSearchAttestations") or []:
                if (a.get("sourceUniverse") == s and a.get("targetUniverse") == u
                        and a.get("relation") == rel and a.get("minResolution") == min_rung):
                    att = a
                    break
            if att is None or att.get("completeSearch") is not True or att.get("coverage") != "complete":
                causes.append(_cause("source-target-search-unattested", universe=s))
                unknown = True
                ok_all = False
            else:
                view = {rel: {
                    "resolution": min_rung,
                    "coverage": att["coverage"],
                    "confidenceMillionths": 1000000,
                    "resolutionCompleteness": att.get("resolutionCompleteness") or {
                        "state": "not-applicable" if min_rung not in RESOLVED_RUNGS else "complete",
                        "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": [],
                    },
                    "closedWorld": att.get("closedWorld") or {"exportsClosed": "unknown"},
                    "derivationKinds": [],
                    "deficiency": None,
                }}
                su = _sufficiency(rel, min_rung, view, subject, q_use, inputs, s)
                defs.extend(su.get("causes") or [])
                causes.extend(su.get("extraCauses") or [])
                if not su.get("satisfied"):
                    ok_all = False
                    unknown = True
                    causes.append(_cause("coverage-unknown", universe=s))
    if unavailable:
        unknown = True
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
    # all-covered + uncertain matching evidence cannot pretend coverage proves those matches
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


def _path_in_scope(scope: dict, path: str) -> bool:
    excluded = scope.get("excludedPathPrefixes") or []
    for e in excluded:
        if e in (".", "") or path == e or path.startswith(str(e).rstrip("/") + "/"):
            return False
    prefixes = list(scope.get("pathPrefixes") or []) + list(scope.get("workspaceRoots") or [])
    if not prefixes:
        return False
    for p in prefixes:
        if p in (".", "") or path == p or path.startswith(str(p).rstrip("/") + "/"):
            return True
    return False


def _logical_path(subject: dict, inventory_row: dict | None) -> str | None:
    if inventory_row and inventory_row.get("path"):
        return inventory_row["path"]
    if subject["kind"] == "file":
        return subject["nativeSubjectId"]
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
        if len(hits) > 1:
            return FUNK
        if not hits:
            return NOMATCH
        return MATCH if hits[0]["nativeSubjectId"] == subject["nativeSubjectId"] else NOMATCH
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


def _require_wrapper_flags(wrapper: dict) -> None:
    if "consumable" not in wrapper:
        raise AtomAdmissionError("ATOM_IMPORT_CONSUMABLE_UNSTATED")
    if "staleness" not in wrapper:
        raise AtomAdmissionError("ATOM_IMPORT_STALENESS_UNSTATED")


def _import_complete_runtime(wrapper: dict, obs: dict) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    if not obs or obs.get("window") is None:
        return False
    if obs.get("population") in (None, "unknown"):
        return False
    return True


def _import_complete_history(wrapper: dict, payload: dict) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    if (payload.get("revisionRange") or {}).get("truncated") is True:
        return False
    return True


def _import_complete_test(wrapper: dict, payload: dict, obs: dict) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    if wrapper.get("staleness") != "current" or wrapper.get("consumable") is not True:
        return False
    sel = (obs or {}).get("selection") or payload.get("selection")
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


def _eval_imported(atom: dict, subject: dict, inputs: dict, spec: dict) -> dict:
    kind = spec["evidenceKind"]
    selected = list(inputs.get("planSelectedImportIds") or [])
    wrappers = inputs.get("imports") or {}
    payloads = inputs.get("importPayloads") or {}
    observations = inputs.get("importObservations") or {}
    inventories = inputs.get("inventories") or []
    plan = inputs.get("enumerationPlan")
    inv_rows = _lookup_rows(subject["nativeSubjectId"], subject["universe"], subject["kind"], inventories, plan)
    inv_row = inv_rows[0] if len(inv_rows) == 1 else None
    for iid in selected:
        if iid not in wrappers:
            raise AtomAdmissionError("ATOM_IMPORT_WRAPPER_MISSING", iid)
        _require_wrapper_flags(wrappers[iid])
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
                       causes=[_cause("zero-owed-wrappers"), _cause("evidence-kind-unavailable")])

    known, uncertain = [], []
    causes = []
    covering_complete = True

    for iid in owed:
        w = wrappers[iid]
        p = payloads.get(iid) or {}
        obs = observations.get(iid)
        if w.get("consumable") is not True or w.get("staleness") != "current":
            causes.append(_cause("import-unmapped-only", importId=iid))
            covering_complete = False
            continue
        if kind == "runtime":
            wrap_complete = _import_complete_runtime(w, obs or {})
            if not wrap_complete:
                covering_complete = False
                if w.get("completeness") == "partial":
                    causes.append(_cause("wrapper-partial", importId=iid))
                else:
                    causes.append(_cause("incomplete-observation", importId=iid))
            covering, matched, unobs = [], [], []
            rows = p.get("subjects") or []
            occupancies = []
            for i, row in enumerate(rows):
                occ = _runtime_occupancy(row, subject, inputs)
                if occ == NOMATCH:
                    continue
                occupancies.append(i)
                if occ == FUNK:
                    uncertain.append(_addr(iid, "runtime-subject", i))
                    causes.append(_cause("overload-ambiguous", importId=iid))
                    continue
                obs_v = row.get("observability")
                addr = _addr(iid, "runtime-subject", i)
                if obs_v in ("unobservable", "unmapped"):
                    unobs.append(addr)
                    uncertain.append(addr)
                    causes.append(_cause("unobservable-subject" if obs_v == "unobservable" else "unmapped-subject",
                                         importId=iid))
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
                causes.append(_cause("no-consumable-row", importId=iid))
            elif covering and wrap_complete:
                pass
        elif kind == "history":
            wrap_complete = _import_complete_history(w, p)
            if not wrap_complete:
                covering_complete = False
                if w.get("completeness") == "partial":
                    causes.append(_cause("wrapper-partial", importId=iid))
                if (p.get("revisionRange") or {}).get("truncated"):
                    causes.append(_cause("history-truncated", importId=iid))
                else:
                    causes.append(_cause("incomplete-observation", importId=iid))
            path = _logical_path(subject, inv_row)
            if path is None:
                causes.append(_cause("target-metadata-unknown", importId=iid))
                covering_complete = False
                continue
            extent = _history_in_extent(p, w, path, inputs)
            if extent == "listed-missing":
                causes.append(_cause("history-outside-collection-scope", importId=iid))
                covering_complete = False
                continue
            if extent == "outside":
                causes.append(_cause("history-outside-collection-scope", importId=iid))
                covering_complete = False
                continue
            rows = p.get("subjects") or []
            hit = None
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
                    hit = addr
                elif fr == FUNK:
                    uncertain.append(addr)
            if hit is not None:
                known.append(hit)
        elif kind == "test":
            wrap_complete = _import_complete_test(w, p, obs or {})
            if not wrap_complete:
                covering_complete = False
                if w.get("completeness") == "partial":
                    causes.append(_cause("wrapper-partial", importId=iid))
                causes.append(_cause("test-completeness-not-established", importId=iid))
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
                        causes.append(_cause("null-exit-status", importId=iid))
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
