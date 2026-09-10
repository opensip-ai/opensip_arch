"""Full-scan atom reference (isolated successor). Not product runtime. Not full Run replay.

Consumes owner-admitted native/import records. Reuses native_evidence_model.v2.sufficiency_v2.
Refuses oracle/callback/expected-match flags. Root composes boolean nodes, findings, gating.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
NATIVE = HERE.parent / "native" / "native_evidence_model.v2.py"
REGISTRY = json.loads((HERE / "evaluator-projection-registry.v1.json").read_text(encoding="utf-8"))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


N = _load("native_evidence_model_v2_atom", NATIVE)

TRUE, FALSE, UNK = "true", "false", "indeterminate"
MATCH, NOMATCH, FUNK = "match", "nomatch", "unknown"
ABSENT = object()
ORACLE_KEYS = frozenset({
    "expectedValue", "expectedMatches", "oracle", "callback", "expectedFindings",
    "producerExpected", "trustedComplete",
})
PORTABLE_DOMAINS = tuple(REGISTRY["engineFamilies"]["portableUniverseDomains"])
RESOLVED_RUNGS = frozenset(REGISTRY["resolvedRungs"])
CAUSE_CODES = frozenset(REGISTRY["$defs"]["AtomCauseCodeV1"]["enum"])
LANG_FAMILY = {}
for fam, row in REGISTRY["engineFamilies"]["families"].items():
    for mode in row["languageModes"]:
        LANG_FAMILY[mode] = fam
DOMAIN_FAMILY = {
    row["universeDomain"]: fam
    for fam, row in REGISTRY["engineFamilies"]["families"].items()
}


class AtomAdmissionError(Exception):
    def __init__(self, key: str, detail: str = ""):
        self.key = key
        self.detail = detail
        super().__init__(key + (": " + detail if detail else ""))


def evaluate_atom(atom: dict, subject: dict, inputs: dict) -> dict:
    """Evaluate one atom at one evaluation-subject over admitted inputs.

    subject: {universe, kind, nativeSubjectId}  # E=(U,K,N)
    inputs: record maps documented in atom-evaluation-contract.v1.md §8
    """
    if not isinstance(inputs, dict):
        raise AtomAdmissionError("ATOM_INPUTS_NOT_RECORD")
    bad = sorted(ORACLE_KEYS.intersection(inputs))
    if bad:
        raise AtomAdmissionError("ATOM_ORACLE_FLAG_REFUSED", ",".join(bad))
    _admit_subject(subject)
    spec = _admit_atom(atom)
    plane = spec["plane"]
    if plane == "native":
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
    u = subject["universe"]
    if not isinstance(u, str) or not re.fullmatch(r"[0-9a-f]{64}", u):
        raise AtomAdmissionError("ATOM_SUBJECT_UNIVERSE")


def _admit_atom(atom: dict) -> dict:
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
    else:
        if evidence != spec.get("evidenceKind"):
            raise AtomAdmissionError("ATOM_EVIDENCE_KIND_MISMATCH", str(evidence))
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
    if not isinstance(flt, dict) or "field" not in flt or "cmp" not in flt or "value" not in flt:
        raise AtomAdmissionError("ATOM_FILTER_SHAPE")
    field, cmp, value = flt["field"], flt["cmp"], flt["value"]
    table = REGISTRY["comparatorTable"].get(field)
    if table is None:
        raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", field)
    proj = _proj(spec, field, min_rung)
    if proj == "forbidden":
        raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", rel + "." + field)
    allowed = []
    for c in ("eq", "neq", "in", "prefix", "glob", "gte", "lte"):
        v = table.get(c)
        if v:
            allowed.append(c)
    if cmp not in allowed:
        raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", field + " " + cmp)
    enum = table.get("enum")
    if field == "testResult":
        enum = (table.get("enumByRelation") or {}).get(rel)
    if field == "universe":
        enum = list(PORTABLE_DOMAINS)
    if cmp in ("eq", "neq") and enum is not None:
        if value not in enum:
            raise AtomAdmissionError("ATOM_FILTER_ENUM_LITERAL_UNKNOWN", str(value))
    if cmp == "in" and enum is not None:
        if type(value) is not list:
            raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", "in type")
        for item in value:
            if item not in enum:
                raise AtomAdmissionError("ATOM_FILTER_ENUM_LITERAL_UNKNOWN", str(item))
    if field == "exitStatus":
        if cmp == "in":
            if type(value) is not list or any(type(x) is not int for x in value):
                raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", "exitStatus in")
        elif type(value) is not int:
            raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", "exitStatus scalar")
    if field == "confidenceMillionths" and type(value) is not int:
        raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", "confidence")
    if cmp in ("prefix", "glob") and type(value) is not str:
        raise AtomAdmissionError("ATOM_FILTER_COMPARATOR_ILLEGAL", cmp)


def _result(**kwargs) -> dict:
    base = {
        "value": UNK,
        "kind": None,
        "knownFactIds": [],
        "uncertainFactIds": [],
        "knownObservationAddresses": [],
        "uncertainObservationAddresses": [],
        "coverageIds": [],
        "scopeIds": [],
        "evaluationInputRefs": [],
        "causes": [],
        "nativeDeficiencies": [],
        "disclosures": [],
        "usedInputDigests": [],
    }
    base.update(kwargs)
    base["causes"] = _uniq_causes(base["causes"])
    base["knownFactIds"] = sorted(set(base["knownFactIds"]))
    base["uncertainFactIds"] = sorted(set(base["uncertainFactIds"]))
    return base


def _uniq_causes(causes: list) -> list:
    seen = set()
    out = []
    for c in causes:
        code = c["code"] if isinstance(c, dict) else c
        if code not in CAUSE_CODES:
            raise AtomAdmissionError("ATOM_CAUSE_UNREGISTERED", str(code))
        key = json.dumps(c, sort_keys=True, separators=(",", ":"))
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


def _cause(code: str, **extra) -> dict:
    rec = {"code": code}
    rec.update(extra)
    return rec


# --- glob / compare ----------------------------------------------------------

def glob_match(pattern: str, value: str) -> bool:
    """*, ? (no slash), ** any including slashes. Explicit; not fnmatch."""
    def trans(p: str) -> str:
        out = []
        i = 0
        while i < len(p):
            if p.startswith("**", i):
                out.append(".*")
                i += 2
                continue
            ch = p[i]
            if ch == "*":
                out.append("[^/]*")
            elif ch == "?":
                out.append("[^/]")
            else:
                out.append(re.escape(ch))
            i += 1
        return "^" + "".join(out) + "$"
    return re.match(trans(pattern), value) is not None


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
        return MATCH if glob_match(value, projected) else NOMATCH
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


def _kleene_or_true(value: str) -> bool:
    return value == TRUE


# --- inventory / attribution -------------------------------------------------

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
        return None
    return b.get("universe")


def _distinct_identities(native_id: str, universe: str, inventories: list, plan: dict | None):
    triples = set()
    rows = []
    for inv in inventories:
        u = _inventory_universe(inv, plan)
        if u != universe:
            continue
        for row in inv.get("rows") or []:
            if row.get("nativeSubjectId") == native_id:
                triples.add((u, row["kind"], native_id))
                rows.append(row)
    return triples, rows


def _lookup_row(native_id: str, universe: str, kind: str | None, inventories: list, plan: dict | None):
    hits = []
    for inv in inventories:
        u = _inventory_universe(inv, plan)
        if u != universe:
            continue
        for row in inv.get("rows") or []:
            if row.get("nativeSubjectId") != native_id:
                continue
            if kind is not None and row.get("kind") != kind:
                continue
            hits.append(row)
    if not hits:
        return None
    # equivalent observations of the same triple collapse
    kinds = {h["kind"] for h in hits}
    if len(kinds) != 1:
        return None
    return hits[0]


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
        exported = row.get("exported") if row["kind"] == "symbol" else None
        return {
            "kind": row["kind"],
            "occupancy": "first-party",
            "exported": exported,
            "nativeId": nid,
        }
    if len(triples) == 0:
        return {"kind": "unknown", "occupancy": "unknown", "nativeId": nid, "exported": None}
    return {"kind": "unknown", "occupancy": "unknown", "nativeId": nid, "exported": None, "ambiguous": True}


def _reconcile_attribution(fact: dict, spec: dict, inputs: dict) -> dict:
    eph = _ephemeral_target(fact, spec, inputs)
    sidecar = (inputs.get("targetAttributions") or {}).get(fact["factId"])
    closures = inputs.get("closures") or {}
    if sidecar is not None:
        pc = sidecar.get("producerClosure")
        if pc != fact.get("producerClosure"):
            raise AtomAdmissionError("TARGET_ATTRIBUTION_PRODUCER_MISMATCH")
        ck = (closures.get(pc) or {}).get("kind")
        if ck != "provider":
            raise AtomAdmissionError("TARGET_ATTRIBUTION_PRODUCER_NOT_PROVIDER", str(ck))
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
        # unknown cannot override known
        kind = ek if ek != "unknown" else sk
        occ = eph["occupancy"] if eph.get("occupancy") != "unknown" else sidecar.get("occupancy")
        exported = ee if ee not in (None, "unknown") else se
        return {"kind": kind, "occupancy": occ, "exported": exported, "nativeId": eph.get("nativeId")}
    return eph


def _source_value(fact: dict, spec: dict):
    field = spec.get("sourceField")
    if field == "anchors[0].path":
        anchors = fact.get("anchors") or []
        if not anchors:
            return ABSENT
        return anchors[0].get("path", ABSENT)
    payload = fact.get("payload") or {}
    if field not in payload:
        return ABSENT
    return payload[field]


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
    plan = inputs.get("enumerationPlan")
    cap = REGISTRY["capabilityForRelation"].get(rel)
    available, unavailable = [], []
    if not plan:
        return available, unavailable
    for cell in plan.get("cells") or []:
        if cell.get("capabilityId") != cap:
            continue
        for b in cell.get("programBindings") or []:
            if b.get("universe") is None:
                unavailable.append(b)
            else:
                rec = dict(b)
                rec["_languageMode"] = cell.get("languageMode")
                rec["_family"] = LANG_FAMILY.get(cell.get("languageMode"))
                available.append(rec)
    return available, unavailable


# --- native filters / occupancy ---------------------------------------------

def _native_occupancy(fact: dict, subject: dict, spec: dict, atom: dict, inputs: dict) -> str:
    endpoint = atom.get("endpoint", "source")
    u, k, n = subject["universe"], subject["kind"], subject["nativeSubjectId"]
    if endpoint == "source":
        src_kinds = spec.get("sourceSubjectKinds") or [spec.get("sourceSubjectKind")]
        if k not in src_kinds:
            return NOMATCH
        if fact.get("sourceUniverse") != u:
            return NOMATCH
        val = _source_value(fact, spec)
        if val is ABSENT:
            return NOMATCH
        return MATCH if val == n else NOMATCH
    # target
    field = spec.get("targetNativeIdField")
    if not field:
        return NOMATCH
    payload = fact.get("payload") or {}
    tid = payload.get(field)
    if tid is None:
        return NOMATCH
    if tid != n:
        return NOMATCH  # known nonmatch even if kind unknown
    if fact.get("targetUniverse") != u:
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
    row = _lookup_row(val, fact["sourceUniverse"], spec.get("sourceSubjectKind"),
                      inputs.get("inventories") or [], inputs.get("enumerationPlan"))
    if row is None:
        return spec.get("sourceSubjectKind")
    return row.get("kind")


def _apply_native_filters(fact: dict, subject: dict, spec: dict, atom: dict, inputs: dict) -> str:
    acc = MATCH
    endpoint = atom.get("endpoint", "source")
    min_rung = atom["minResolution"]
    for flt in atom.get("filters") or []:
        field, cmp, value = flt["field"], flt["cmp"], flt["value"]
        proj = _proj(spec, field, min_rung)
        if proj == "forbidden":
            raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", field)
        got = FUNK
        if field == "resolution":
            got = _cmp_string(cmp, fact["resolution"], value)
        elif field == "universe":
            coord = fact["sourceUniverse"] if endpoint == "source" else fact["targetUniverse"]
            dom = _domain_of(coord, inputs)
            if dom is None:
                got = FUNK
            else:
                got = _cmp_string(cmp, dom, value)
        elif field == "confidenceMillionths":
            got = _cmp_int(cmp, fact.get("confidenceMillionths", 1000000), value)
        elif field == "subjectKind":
            sk = _source_kind_of_fact(fact, spec, inputs)
            if sk is None:
                got = FUNK
            else:
                got = _cmp_string(cmp, sk, value)
        elif field == "targetKind":
            attr = _reconcile_attribution(fact, spec, inputs)
            if attr.get("kind") == "unknown":
                got = FUNK
            else:
                got = _cmp_string(cmp, attr["kind"], value)
        elif field == "subject":
            val = _source_value(fact, spec)
            if val is ABSENT:
                got = FUNK
            else:
                got = _cmp_string(cmp, val, value)
        elif field == "target":
            tfield = spec.get("targetField")
            if spec.get("targetNativeIdField") and atom["minResolution"] in (spec.get("endpointTargetRungs") or []):
                tfield = spec["targetNativeIdField"]
            if tfield is None:
                # unresolved-edge text
                raw = (fact.get("payload") or {}).get("targetModule", ABSENT)
                if raw is ABSENT or raw is None:
                    got = FUNK
                else:
                    got = _cmp_string(cmp, raw, value)
            else:
                raw = (fact.get("payload") or {}).get(tfield, ABSENT)
                if raw is ABSENT or raw is None:
                    got = FUNK
                else:
                    got = _cmp_string(cmp, raw, value)
        else:
            raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", field)
        acc = _and_fr(acc, got)
        if acc == NOMATCH:
            return NOMATCH
    return acc


# --- coverage / sufficiency --------------------------------------------------

def _coverages_for(inputs: dict, rel: str, source_u: str | None = None) -> list[tuple[str, dict]]:
    out = []
    for cid, cov in (inputs.get("coverages") or {}).items():
        key = cov.get("key") or {}
        if key.get("relation") != rel:
            continue
        if source_u is not None and key.get("sourceUniverse") != source_u:
            continue
        out.append((cid, cov))
    return out


def _scopes_for(inputs: dict, rel: str, source_u: str | None = None) -> list[tuple[str, dict]]:
    out = []
    for sid, sc in (inputs.get("scopes") or {}).items():
        if sc.get("relation") != rel:
            continue
        if source_u is not None and sc.get("sourceUniverse") != source_u:
            continue
        out.append((sid, sc))
    return out


def _view_from_coverage(rel: str, cov: dict) -> dict:
    entry = cov.get("entry") or {}
    key = cov.get("key") or {}
    rc = entry.get("resolutionCompleteness") or {
        "state": "not-applicable", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": [],
    }
    return {rel: {
        "resolution": key.get("resolution") or entry.get("resolution"),
        "coverage": entry.get("coverage", "unknown"),
        "confidenceMillionths": entry.get("confidenceMillionths", 1000000),
        "resolutionCompleteness": rc,
        "closedWorld": entry.get("closedWorld") or {"exportsClosed": "unknown"},
        "derivationKinds": entry.get("derivationKinds") or [],
        "deficiency": entry.get("deficiency"),
        "rungUnavailableBecause": entry.get("rungUnavailableBecause", ""),
    }}


def _view_from_attestation(rel: str, att: dict, min_rung: str) -> dict:
    rc = att.get("resolutionCompleteness") or {
        "state": "not-applicable" if min_rung not in RESOLVED_RUNGS else "not-attempted",
        "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": [],
    }
    return {rel: {
        "resolution": min_rung,
        "coverage": att.get("coverage", "unknown"),
        "confidenceMillionths": 1000000,
        "resolutionCompleteness": rc,
        "closedWorld": att.get("closedWorld") or {"exportsClosed": "unknown"},
        "derivationKinds": [],
        "deficiency": None,
    }}


def _target_affected(facts: dict, subject: dict, source_u: str) -> bool:
    n = subject["nativeSubjectId"]
    for fact in facts.values():
        if fact.get("relation") != "unresolved-edge":
            continue
        if fact.get("sourceUniverse") != source_u:
            continue
        ts = (fact.get("payload") or {}).get("targetScope")
        if ts in ("universe", "unknown", "external"):
            return True
        if ts == "module" and (fact.get("payload") or {}).get("targetModule") in (n, None):
            return True
    return False


def _sufficiency(rel: str, min_rung: str, view: dict, subject: dict, quantifier: str, inputs: dict, source_u: str) -> dict:
    req = {
        "relation": rel,
        "minResolution": min_rung,
        "completeness": "complete",
        "quantifier": quantifier,
        "minConfidenceMillionths": 0,
        "derivationPolicy": "any",
        "unresolvedEdgePolicy": "forbid",
        "externalConsumerPolicy": "forbid",
    }
    exported = False
    row = _lookup_row(subject["nativeSubjectId"], subject["universe"], subject["kind"],
                      inputs.get("inventories") or [], inputs.get("enumerationPlan"))
    if row is not None and row.get("exported") == "exported":
        exported = True
    affected = _target_affected(inputs.get("facts") or {}, subject, source_u)
    return N.sufficiency_v2(req, view, target_exported=exported, target_affected=affected)


def _expected_source_ids(binding: dict, kind: str, inventories: list, plan: dict) -> set[str]:
    expected = set()
    for inv in inventories:
        b = _plan_binding(plan, inv["cellOrdinal"], inv["programOrdinal"])
        if b is None or b.get("universe") != binding.get("universe"):
            continue
        if inv.get("kind") != kind:
            continue
        for row in inv.get("rows") or []:
            expected.add(row["nativeSubjectId"])
        for p in inv.get("examinedPaths") or []:
            if kind == "file":
                expected.add(p)
    for ext in binding.get("extents") or []:
        if ext.get("kind") == kind:
            expected.update(ext.get("paths") or [])
    return expected


def _union_scoped_sources(rel: str, source_u: str, min_rung: str, inputs: dict) -> tuple[set[str], list[str]]:
    present = set()
    scope_ids = []
    for sid, sc in _scopes_for(inputs, rel, source_u):
        if not _rung_ge(rel, sc.get("resolution", min_rung), min_rung):
            continue
        scope_ids.append(sid)
        present.update(sc.get("subjects") or [])
    return present, scope_ids


def _attestation_for(inputs: dict, s: str, rel: str, min_rung: str, u: str) -> dict | None:
    for att in inputs.get("incomingSearchAttestations") or []:
        if (att.get("sourceUniverse") == s and att.get("targetUniverse") == u
                and att.get("relation") == rel and att.get("minResolution") == min_rung):
            return att
    return None


def _native_completeness(atom: dict, subject: dict, spec: dict, inputs: dict, need_absence: bool) -> dict:
    """Return {complete: bool, unknown: bool, causes, coverageIds, scopeIds, nativeDeficiencies}."""
    rel = atom["relation"]
    min_rung = atom["minResolution"]
    endpoint = atom.get("endpoint", "source")
    u = subject["universe"]
    causes = []
    cov_ids = []
    scope_ids = []
    defs = []
    available, unavailable = _owed_source_bindings(rel, inputs)
    if unavailable:
        causes.append(_cause("unavailable-program-binding"))
    if not available and not unavailable:
        causes.append(_cause("missing-relation-coverage"))
        return {"complete": False, "unknown": True, "causes": causes,
                "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}

    src_kind = spec.get("sourceSubjectKind") or "symbol"
    resolved = min_rung in RESOLVED_RUNGS
    quant_all = "universal-negative" if resolved else "existential"
    quant_none = "universal-negative" if resolved else "existential"

    def run_suff(view, source_u, quant):
        su = _sufficiency(rel, min_rung, view, subject, quant, inputs, source_u)
        if not su.get("satisfied"):
            if su.get("deficiency"):
                defs.append(su["deficiency"])
            causes.append(_cause("coverage-unknown", universe=source_u))
            return False
        return True

    if endpoint == "source":
        # owed examination of current U as source; do not invent target-universe keys
        if not any(b.get("universe") == u for b in available):
            causes.append(_cause("selector-unbound"))
            return {"complete": False, "unknown": True, "causes": causes,
                    "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}
        present, sids = _union_scoped_sources(rel, u, min_rung, inputs)
        scope_ids.extend(sids)
        binding = next(b for b in available if b.get("universe") == u)
        expected = _expected_source_ids(binding, src_kind, inputs.get("inventories") or [],
                                        inputs.get("enumerationPlan") or {"cells": []})
        if subject["nativeSubjectId"] not in present and expected and subject["nativeSubjectId"] in expected:
            # current source not in union of scopes
            causes.append(_cause("uncovered-expected-source-subject", universe=u))
        elif expected - present:
            causes.append(_cause("uncovered-expected-source-subject", universe=u))
        covs = [c for c in _coverages_for(inputs, rel, u) if _rung_ge(rel, c[1]["key"].get("resolution", min_rung), min_rung)]
        cov_ids.extend(c[0] for c in covs)
        if not covs:
            causes.append(_cause("missing-relation-coverage", universe=u))
            return {"complete": False, "unknown": True, "causes": causes,
                    "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}
        # represented partitions only; pick those covering current source
        ok = True
        q = quant_none if need_absence else quant_all
        if atom["op"] == "all-covered":
            q = quant_all
        elif need_absence:
            q = quant_none
        else:
            q = "existential"
        for cid, cov in covs:
            if not run_suff(_view_from_coverage(rel, cov), u, q):
                ok = False
        unknown = bool(causes)
        return {"complete": ok and not unknown, "unknown": unknown or not ok,
                "causes": causes, "coverageIds": cov_ids, "scopeIds": scope_ids, "nativeDeficiencies": defs}

    # incoming: every same-family owed S, scopes regardless of targetUniverse
    subj_fam = _family_of_universe(u, inputs)
    ok_all = True
    unknown = False
    plan = inputs.get("enumerationPlan") or {"cells": []}
    inventories = inputs.get("inventories") or []
    for b in available:
        s = b["universe"]
        fam = b.get("_family") or _family_of_universe(s, inputs)
        if subj_fam and fam and fam != subj_fam:
            if need_absence or atom["op"] in ("none", "all-covered", "count-at-most"):
                causes.append(_cause("cross-family-edge-not-owed", universe=s))
            continue
        present, sids = _union_scoped_sources(rel, s, min_rung, inputs)
        scope_ids.extend(sids)
        expected = _expected_source_ids(b, src_kind, inventories, plan)
        missed = expected - present
        if missed:
            causes.append(_cause("uncovered-expected-source-subject", universe=s))
            unknown = True
        covs_s = [c for c in _coverages_for(inputs, rel, s)
                  if _rung_ge(rel, c[1]["key"].get("resolution", min_rung), min_rung)]
        cov_ids.extend(c[0] for c in covs_s)
        covs_u = [c for c in covs_s if c[1]["key"].get("targetUniverse") == u]
        att = _attestation_for(inputs, s, rel, min_rung, u)
        if need_absence or atom["op"] == "all-covered":
            if not covs_u and att is None:
                causes.append(_cause("source-target-search-unattested", universe=s))
                unknown = True
                ok_all = False
                continue
            views = [_view_from_coverage(rel, c[1]) for c in covs_u]
            if att is not None and not covs_u:
                views.append(_view_from_attestation(rel, att, min_rung))
            q = quant_all if atom["op"] == "all-covered" else quant_none
            for view in views:
                if not run_suff(view, s, q):
                    ok_all = False
                    unknown = True
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
    used_refs = list(inputs.get("evaluationInputRefs") or [])
    op = atom["op"]
    nlimit = atom.get("n")
    need_absence = op in ("none", "count-at-most", "all-covered")
    # Kleene dominance first
    if op == "exists" and known:
        comp = _native_completeness(atom, subject, spec, inputs, False) if uncertain else {
            "complete": True, "unknown": False, "causes": [], "coverageIds": [], "scopeIds": [], "nativeDeficiencies": [],
        }
        return _result(value=TRUE, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                       coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                       causes=comp["causes"], nativeDeficiencies=comp["nativeDeficiencies"],
                       evaluationInputRefs=used_refs)
    if op == "none" and known:
        comp = _native_completeness(atom, subject, spec, inputs, True)
        return _result(value=FALSE, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                       coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                       causes=comp["causes"], nativeDeficiencies=comp["nativeDeficiencies"],
                       evaluationInputRefs=used_refs)
    if op == "count-at-most" and len(set(known)) > nlimit:
        comp = _native_completeness(atom, subject, spec, inputs, True)
        return _result(value=FALSE, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                       coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                       causes=comp["causes"], nativeDeficiencies=comp["nativeDeficiencies"],
                       evaluationInputRefs=used_refs)
    if op == "exists":
        if uncertain:
            return _result(value=UNK, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                           causes=[_cause("target-metadata-unknown")], evaluationInputRefs=used_refs)
        comp = _native_completeness(atom, subject, spec, inputs, True)
        if comp["unknown"] or not comp["complete"]:
            return _result(value=UNK, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                           coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                           causes=comp["causes"] or [_cause("coverage-unknown")],
                           nativeDeficiencies=comp["nativeDeficiencies"], evaluationInputRefs=used_refs)
        return _result(value=FALSE, kind="native-atom", knownFactIds=known,
                       coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                       nativeDeficiencies=comp["nativeDeficiencies"], evaluationInputRefs=used_refs)
    if op == "none":
        if uncertain:
            return _result(value=UNK, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                           causes=[_cause("target-metadata-unknown")], evaluationInputRefs=used_refs)
        comp = _native_completeness(atom, subject, spec, inputs, True)
        if comp["unknown"] or not comp["complete"]:
            return _result(value=UNK, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                           coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                           causes=comp["causes"] or [_cause("coverage-unknown")],
                           nativeDeficiencies=comp["nativeDeficiencies"], evaluationInputRefs=used_refs)
        return _result(value=TRUE, kind="native-atom", knownFactIds=known,
                       coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                       nativeDeficiencies=comp["nativeDeficiencies"], evaluationInputRefs=used_refs)
    if op == "count-at-most":
        if uncertain:
            return _result(value=UNK, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                           causes=[_cause("target-metadata-unknown")], evaluationInputRefs=used_refs)
        comp = _native_completeness(atom, subject, spec, inputs, True)
        if comp["unknown"] or not comp["complete"]:
            return _result(value=UNK, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                           coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                           causes=comp["causes"] or [_cause("coverage-unknown")],
                           nativeDeficiencies=comp["nativeDeficiencies"], evaluationInputRefs=used_refs)
        return _result(value=TRUE, kind="native-atom", knownFactIds=known,
                       coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                       nativeDeficiencies=comp["nativeDeficiencies"], evaluationInputRefs=used_refs)
    # all-covered
    comp = _native_completeness(atom, subject, spec, inputs, True)
    val = TRUE if comp["complete"] and not comp["unknown"] else UNK
    return _result(value=val, kind="native-atom", knownFactIds=known, uncertainFactIds=uncertain,
                   coverageIds=comp["coverageIds"], scopeIds=comp["scopeIds"],
                   causes=comp["causes"], nativeDeficiencies=comp["nativeDeficiencies"],
                   evaluationInputRefs=used_refs)


# --- imports -----------------------------------------------------------------

def _addr(import_id: str, selector: str, ordinal) -> dict:
    return {"importId": import_id, "selector": selector, "ordinal": ordinal}


def _wrapper_relevant(wrapper: dict, subject: dict, spec: dict, payload: dict) -> bool:
    """Declared coverage BEFORE listed-row selection."""
    scope = wrapper.get("scope") or {}
    path = subject.get("logicalPath")
    if path is None:
        path = subject["nativeSubjectId"] if subject["kind"] == "file" else None
    prefixes = scope.get("pathPrefixes") or scope.get("workspaceRoots") or []
    if not prefixes:
        return True
    if path is None:
        return True
    for p in prefixes:
        if p in (".", "") or path == p or path.startswith(str(p).rstrip("/") + "/"):
            return True
    return False


def _history_in_extent(payload: dict, wrapper: dict, path: str) -> str:
    """Return in-scope | outside | listed-missing."""
    cs = payload.get("collectionScope")
    if cs == "listed-paths":
        rows = payload.get("subjects") or []
        if any(r.get("path") == path for r in rows):
            return "in-scope"
        return "listed-missing"
    if cs in ("all-paths", "in-scope-paths"):
        if _wrapper_relevant(wrapper, {"kind": "file", "nativeSubjectId": path, "universe": ""}, {}, payload):
            return "in-scope"
        return "outside"
    return "outside"


def _runtime_occupancy(row: dict, subject: dict, inventory_row: dict | None) -> str:
    k, n = subject["kind"], subject["nativeSubjectId"]
    if k == "file":
        if "symbol" in row and row["symbol"] is not None:
            return NOMATCH
        return MATCH if row.get("path") == n else NOMATCH
    if k == "symbol":
        if "symbol" not in row or row.get("symbol") is None:
            return NOMATCH
        path = inventory_row["path"] if inventory_row else None
        qn = inventory_row.get("qualifiedName") if inventory_row else None
        if path is None or qn is None:
            return FUNK
        if row.get("path") == path and row.get("symbol") == qn:
            return MATCH
        return NOMATCH
    return NOMATCH


def _runtime_subject_scalar(row: dict, subject: dict):
    if subject["kind"] == "file":
        return row.get("path", ABSENT)
    if subject["kind"] == "symbol":
        if "symbol" not in row:
            return ABSENT
        return row.get("symbol")
    return ABSENT


def _import_complete_runtime(wrapper: dict, obs: dict) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    if not obs or obs.get("window") is None:
        return False
    pop = obs.get("population")
    if pop in (None, "unknown"):
        return False
    return True


def _import_complete_history(wrapper: dict, payload: dict) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    rr = payload.get("revisionRange") or {}
    if rr.get("truncated") is True:
        return False
    return True


def _import_complete_test(wrapper: dict, payload: dict, obs: dict) -> bool:
    if wrapper.get("completeness") != "complete":
        return False
    if wrapper.get("staleness") not in (None, "current"):
        return False
    sel = (obs or {}).get("selection") or payload.get("selection")
    if not sel or sel.get("completenessEstablished") is not True:
        return False
    return True


def _test_process_result(payload: dict) -> str:
    if payload.get("timedOut") is True:
        return "error"
    if payload.get("signal") is not None:
        return "error"
    if payload.get("exitStatus") is None:
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
    eval_refs = set()
    for ref in inputs.get("evaluationInputRefs") or []:
        if isinstance(ref, dict) and ref.get("domain") == "import":
            eval_refs.add(ref.get("digest") or ref.get("id"))
        elif isinstance(ref, str):
            eval_refs.add(ref)
    inventories = inputs.get("inventories") or []
    plan = inputs.get("enumerationPlan")
    inv_row = _lookup_row(subject["nativeSubjectId"], subject["universe"], subject["kind"], inventories, plan)

    owed = []
    for iid in selected:
        w = wrappers.get(iid)
        if w is None or w.get("kind") != kind:
            continue
        p = payloads.get(iid) or {}
        if not _wrapper_relevant(w, subject, spec, p):
            continue
        owed.append(iid)
    if not owed:
        return _result(value=UNK, kind="imported-atom",
                       causes=[_cause("zero-owed-wrappers"), _cause("evidence-kind-unavailable")])

    known, uncertain = [], []
    causes = []
    omitted = []
    for iid in owed:
        digest = iid.split(":")[-1] if ":" in iid else iid
        if eval_refs and digest not in eval_refs and iid not in eval_refs:
            omitted.append(iid)
            causes.append(_cause("omitted-selected-wrapper", importId=iid))
        w = wrappers[iid]
        p = payloads.get(iid) or {}
        obs = observations.get(iid)
        if w.get("consumable") is False or w.get("staleness") not in (None, "current"):
            causes.append(_cause("import-unmapped-only", importId=iid))
            continue
        if kind == "runtime":
            rows = p.get("subjects") or []
            matches = []
            for i, row in enumerate(rows):
                occ = _runtime_occupancy(row, subject, inv_row)
                if occ == NOMATCH:
                    continue
                fr = MATCH
                for flt in atom.get("filters") or []:
                    field, cmp, value = flt["field"], flt["cmp"], flt["value"]
                    if field == "observability":
                        obs_v = row.get("observability")
                        if obs_v is None:
                            fr = _and_fr(fr, FUNK)
                        else:
                            fr = _and_fr(fr, _cmp_string(cmp, obs_v, value))
                    elif field == "subject":
                        sc = _runtime_subject_scalar(row, subject)
                        if sc is ABSENT:
                            fr = _and_fr(fr, FUNK)
                        else:
                            fr = _and_fr(fr, _cmp_string(cmp, sc, value))
                    elif field == "resolution":
                        fr = _and_fr(fr, _cmp_string(cmp, "observed", value))
                    elif field == "subjectKind":
                        fr = _and_fr(fr, _cmp_string(cmp, subject["kind"], value))
                    elif field in ("target", "targetKind", "universe", "confidenceMillionths",
                                   "testResult", "exitStatus"):
                        raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", field)
                status = _and_fr(occ, fr)
                obs_v = row.get("observability")
                addr = _addr(iid, "runtime-subject", i)
                if status == NOMATCH:
                    continue
                if obs_v in ("unobservable", "unmapped"):
                    uncertain.append(addr)
                    causes.append(_cause("unobservable-subject" if obs_v == "unobservable" else "unmapped-subject",
                                         importId=iid))
                    continue
                if obs_v in ("observed-hit", "observable-unhit") and status == MATCH:
                    matches.append(addr)
                elif status == FUNK:
                    uncertain.append(addr)
            if len(matches) > 1:
                raise AtomAdmissionError("ATOM_RUNTIME_ROW_AMBIGUOUS", iid)
            known.extend(matches)
            if not matches:
                if not _import_complete_runtime(w, obs or {}):
                    causes.append(_cause("incomplete-observation", importId=iid))
                else:
                    causes.append(_cause("no-consumable-row", importId=iid))
        elif kind == "history":
            path = inv_row["path"] if inv_row else (subject["nativeSubjectId"] if subject["kind"] == "file" else None)
            if path is None:
                uncertain.append(_addr(iid, "history-subject", 0))
                causes.append(_cause("target-metadata-unknown", importId=iid))
                continue
            extent = _history_in_extent(p, w, path)
            if extent == "listed-missing":
                causes.append(_cause("history-outside-collection-scope", importId=iid))
                continue
            if extent == "outside":
                causes.append(_cause("history-outside-collection-scope", importId=iid))
                continue
            rows = p.get("subjects") or []
            hit = None
            for i, row in enumerate(rows):
                if row.get("path") == path:
                    hit = _addr(iid, "history-subject", i)
                    break
            complete = _import_complete_history(w, p)
            if hit is not None:
                known.append(hit)
            elif not complete:
                causes.append(_cause("incomplete-observation", importId=iid))
                if p.get("revisionRange", {}).get("truncated"):
                    causes.append(_cause("history-truncated", importId=iid))
            # complete + in extent + no row: examined absence (not a known polarity match)
        elif kind == "test":
            if spec.get("observationAddressSelector") == "test-execution":
                addr = _addr(iid, "test-execution", None)
                pr = _test_process_result(p)
                fr = MATCH
                for flt in atom.get("filters") or []:
                    field, cmp, value = flt["field"], flt["cmp"], flt["value"]
                    if field == "testResult":
                        fr = _and_fr(fr, _cmp_string(cmp, pr, value))
                    elif field == "exitStatus":
                        ex = p.get("exitStatus")
                        if ex is None:
                            fr = _and_fr(fr, FUNK)
                            causes.append(_cause("null-exit-status", importId=iid))
                        else:
                            fr = _and_fr(fr, _cmp_int(cmp, ex, value))
                    elif field == "resolution":
                        fr = _and_fr(fr, _cmp_string(cmp, "observed", value))
                    elif field == "subjectKind":
                        fr = _and_fr(fr, _cmp_string(cmp, subject["kind"], value))
                    elif field == "subject":
                        # coarse: inventory logicalPath vs wrapper — occupancy already via relevance
                        sc = (inv_row or {}).get("path") or subject["nativeSubjectId"]
                        fr = _and_fr(fr, _cmp_string(cmp, sc, value))
                    else:
                        raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", field)
                if fr == MATCH:
                    known.append(addr)
                elif fr == FUNK:
                    uncertain.append(addr)
                if not _import_complete_test(w, p, obs or {}):
                    if w.get("completeness") == "partial":
                        causes.append(_cause("wrapper-partial", importId=iid))
                    causes.append(_cause("test-completeness-not-established", importId=iid))
            else:
                tests = p.get("tests") or []
                path = (inv_row or {}).get("path")
                hits = []
                for i, row in enumerate(tests):
                    if "subjectPath" not in row:
                        continue
                    if subject["kind"] != "file" or row.get("subjectPath") != (path or subject["nativeSubjectId"]):
                        continue
                    fr = MATCH
                    for flt in atom.get("filters") or []:
                        field, cmp, value = flt["field"], flt["cmp"], flt["value"]
                        if field == "testResult":
                            fr = _and_fr(fr, _cmp_string(cmp, row.get("outcome"), value))
                        elif field == "subject":
                            fr = _and_fr(fr, _cmp_string(cmp, row.get("subjectPath"), value))
                        elif field == "resolution":
                            fr = _and_fr(fr, _cmp_string(cmp, "observed", value))
                        else:
                            raise AtomAdmissionError("ATOM_FILTER_FIELD_FORBIDDEN", field)
                    if fr == MATCH:
                        hits.append(_addr(iid, "test-case", i))
                    elif fr == FUNK:
                        uncertain.append(_addr(iid, "test-case", i))
                known.extend(hits)
                if not _import_complete_test(w, p, obs or {}):
                    causes.append(_cause("test-completeness-not-established", importId=iid))

    op = atom["op"]
    nlimit = atom.get("n")
    used_refs = list(inputs.get("evaluationInputRefs") or [])
    # dominance
    if op == "exists" and known:
        return _result(value=TRUE, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=used_refs)
    if op == "none" and known:
        return _result(value=FALSE, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=used_refs)
    if op == "count-at-most" and len(known) > nlimit:
        return _result(value=FALSE, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=used_refs)

    incomplete = any(c["code"] in {
        "incomplete-observation", "omitted-selected-wrapper", "unobservable-subject",
        "unmapped-subject", "no-consumable-row", "import-unmapped-only",
        "history-outside-collection-scope", "history-truncated",
        "test-completeness-not-established", "wrapper-partial", "null-exit-status",
        "zero-owed-wrappers", "evidence-kind-unavailable",
    } for c in causes)

    if op == "exists":
        if uncertain or incomplete:
            return _result(value=UNK, kind="imported-atom", knownObservationAddresses=known,
                           uncertainObservationAddresses=uncertain, causes=causes or [_cause("incomplete-observation")],
                           evaluationInputRefs=used_refs)
        return _result(value=FALSE, kind="imported-atom", causes=causes, evaluationInputRefs=used_refs)
    if op == "none":
        if uncertain or incomplete:
            return _result(value=UNK, kind="imported-atom", knownObservationAddresses=known,
                           uncertainObservationAddresses=uncertain, causes=causes,
                           evaluationInputRefs=used_refs)
        return _result(value=TRUE, kind="imported-atom", causes=causes, evaluationInputRefs=used_refs)
    if op == "count-at-most":
        if uncertain or incomplete:
            return _result(value=UNK, kind="imported-atom", knownObservationAddresses=known,
                           uncertainObservationAddresses=uncertain, causes=causes,
                           evaluationInputRefs=used_refs)
        return _result(value=TRUE, kind="imported-atom", knownObservationAddresses=known,
                       evaluationInputRefs=used_refs)
    # all-covered
    if incomplete or uncertain:
        return _result(value=UNK, kind="imported-atom", knownObservationAddresses=known,
                       uncertainObservationAddresses=uncertain, causes=causes,
                       evaluationInputRefs=used_refs)
    # history examined absence with no row is covering
    if kind == "history":
        return _result(value=TRUE, kind="imported-atom", knownObservationAddresses=known,
                       causes=causes, evaluationInputRefs=used_refs)
    if kind == "runtime" and not known:
        return _result(value=UNK, kind="imported-atom", causes=causes or [_cause("no-consumable-row")],
                       evaluationInputRefs=used_refs)
    return _result(value=TRUE, kind="imported-atom", knownObservationAddresses=known,
                   causes=causes, evaluationInputRefs=used_refs)
