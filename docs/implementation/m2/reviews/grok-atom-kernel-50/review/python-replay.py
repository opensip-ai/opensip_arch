"""EXTRA CONTROL only: inlined/AST-isolated copies of selected helper text.

Not the selected-module comparison. Use selected-module-replay.py with
native-case15-reference-env for actual atom_model.v1.py and N.sufficiency_v2.
"""
from __future__ import annotations

import json
from pathlib import Path

FOUND = Path(
    "/tmp/opensip-implementation/m2-reconstruction-subject-48/reference/archroot/docs/coop/design-corrections/foundation"
)
NATIVE_SRC = FOUND.parent / "native" / "native_evidence_model.v2.py"
ATOM_REG = Path("/tmp/opensip-implementation/m2-grok-atom-kernel-50-advisory/source/atom-registry.json")
TRIAL = Path("/tmp/opensip-implementation/m2-composition-trial-50")

MATCH, NOMATCH, FUNK = "match", "nomatch", "unknown"
ABSENT = object()

LADDERS = {
    name: list(row["ladder"])
    for name, row in json.loads((FOUND / "relation-payload-schemas.v2.json").read_text())[
        "x-opensip-relation-registry"
    ]["relations"].items()
}
DEPENDS_ON = {
    "reachability": [{"relation": "calls", "minResolution": "resolved-callee"}],
    "clones": [{"relation": "declares", "minResolution": "syntactic"}],
}
PRECEDENCE_V2 = [
    "language-tier-unsupported",
    "provider-unavailable",
    "input-closure-incomplete",
    "budget-exhausted",
    "confidence-floor-unmet",
    "derivation-policy-unmet",
    "resolution-incomplete",
    "external-consumers-unknown",
    "required-relation-missing",
]
RUNG_CAUSE = {
    "language-tier": "language-tier-unsupported",
    "provider-not-installed": "provider-unavailable",
    "budget": "budget-exhausted",
    "input-closure": "input-closure-incomplete",
}
REG = json.loads(ATOM_REG.read_text())
NATIVE_CAUSE_CODES = set(REG["scanner"]["nativeCauseCodes"])
CAUSE_CODES = set(REG["scanner"]["atomCauseCodes"])
IMPORT_EVIDENCE = set(REG["scanner"]["importEvidenceKinds"])


def _rung_index(relation: str, rung: str):
    ladder = LADDERS.get(relation)
    return None if ladder is None or rung not in ladder else ladder.index(rung)


def sufficiency_v2(req, view, target_exported=False, target_affected=False, depth=0):
    rel = req["relation"]
    quantifier = req.get("quantifier", "existential")
    disclosures = []
    causes = []
    entry = view.get(rel)
    if entry is None:
        return {
            "satisfied": False,
            "deficiency": "required-relation-missing",
            "disclosures": [],
            "causes": ["required-relation-missing"],
        }
    have_i, need_i = _rung_index(rel, entry["resolution"]), _rung_index(rel, req["minResolution"])
    if have_i is None or need_i is None:
        return {
            "satisfied": False,
            "deficiency": "required-relation-missing",
            "disclosures": [],
            "causes": ["required-relation-missing"],
        }
    if have_i < need_i:
        causes.append(RUNG_CAUSE.get(entry.get("rungUnavailableBecause", ""), "required-relation-missing"))
    if entry.get("confidenceMillionths", 1000000) < req.get("minConfidenceMillionths", 0):
        causes.append("confidence-floor-unmet")
    if rel == "types" and req.get("derivationPolicy", "any") == "declared-only":
        kinds = set(entry.get("derivationKinds", []))
        if "compiler-inferred" in kinds:
            causes.append("derivation-policy-unmet")
    if req["completeness"] == "complete" and entry.get("coverage") != "complete":
        causes.append(
            entry.get("deficiency")
            or RUNG_CAUSE.get(entry.get("rungUnavailableBecause", ""), "required-relation-missing")
        )
    rc = entry.get(
        "resolutionCompleteness",
        {"state": "not-applicable", "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
    )
    if quantifier == "universal-negative":
        if rc["state"] in ("partial", "not-attempted"):
            causes.append("resolution-incomplete")
        elif rc["state"] == "incomplete" or target_affected:
            if req.get("unresolvedEdgePolicy", "forbid") == "forbid":
                causes.append("resolution-incomplete")
            else:
                disclosures.append(
                    {
                        "kind": "unresolved-edges",
                        "count": rc.get("unresolvedEdgeCount", 0),
                        "classes": list(rc.get("unresolvedEdgeClasses", [])),
                    }
                )
        cw = entry.get("closedWorld", {"exportsClosed": "unknown"})
        if target_exported and cw.get("exportsClosed") != "closed":
            if req.get("externalConsumerPolicy", "forbid") == "forbid":
                causes.append("external-consumers-unknown")
            else:
                disclosures.append(
                    {"kind": "external-consumers-assumed-closed", "exportsClosed": cw.get("exportsClosed")}
                )
    if depth < 4:
        for dep in DEPENDS_ON.get(rel, []):
            sub_req = {
                **dep,
                "completeness": "partial-ok" if quantifier == "existential" else "complete",
                "quantifier": quantifier,
                "unresolvedEdgePolicy": req.get("unresolvedEdgePolicy", "forbid"),
                "externalConsumerPolicy": req.get("externalConsumerPolicy", "forbid"),
            }
            sub = sufficiency_v2(sub_req, view, target_exported, target_affected, depth + 1)
            causes.extend(sub["causes"])
            disclosures.extend(sub["disclosures"])
    if not causes:
        return {"satisfied": True, "disclosures": disclosures, "causes": []}
    return {
        "satisfied": False,
        "deficiency": min(causes, key=PRECEDENCE_V2.index),
        "disclosures": disclosures,
        "causes": causes,
    }


def _under_unit(path, root):
    return root == "" or path == root or path.startswith(root.rstrip("/") + "/")


def _under_prefix(path, root):
    internal = "" if root in (".", "") else root
    return _under_unit(path, internal)


def _path_in_scope(scope, path):
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


def glob_match(pattern, path):
    def seg_match(p, s):
        if p == "*":
            return True
        i = j = 0
        star = -1
        mark = 0
        while j < len(s):
            if i < len(p) and (p[i] == "?" or (p[i] != "*" and p[i] == s[j])):
                i += 1
                j += 1
            elif i < len(p) and p[i] == "*":
                star = i
                i += 1
                mark = j
            elif star >= 0:
                i = star + 1
                mark += 1
                j = mark
            else:
                return False
        while i < len(p) and p[i] == "*":
            i += 1
        return i == len(p)

    ps, ss = pattern.split("/"), path.split("/")

    def rec(pi, si):
        if pi == len(ps):
            return si == len(ss)
        if ps[pi] == "**":
            if pi == len(ps) - 1:
                return True
            for k in range(si, len(ss) + 1):
                if rec(pi + 1, k):
                    return True
            return False
        if si == len(ss):
            return False
        return seg_match(ps[pi], ss[si]) and rec(pi + 1, si + 1)

    return rec(0, 0)


def _cmp_string(cmp, projected, value):
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
    raise KeyError("ATOM_FILTER_COMPARATOR_ILLEGAL")


def _cmp_int(cmp, projected, value):
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
    raise KeyError("ATOM_FILTER_COMPARATOR_ILLEGAL")


def _and_fr(a, b):
    if a == NOMATCH or b == NOMATCH:
        return NOMATCH
    if a == FUNK or b == FUNK:
        return FUNK
    return MATCH


def _import_complete_runtime(wrapper, payload):
    if wrapper.get("completeness") != "complete":
        return False
    window = payload.get("observationWindow") if isinstance(payload, dict) else None
    pop = payload.get("observedPopulation") if isinstance(payload, dict) else None
    if window is None or pop in (None, "unknown"):
        return False
    return True


def _import_complete_history(wrapper, payload):
    if wrapper.get("completeness") != "complete":
        return False
    if (payload.get("revisionRange") or {}).get("truncated") is True:
        return False
    return True


def _import_complete_test(wrapper, payload, consumable, staleness):
    if wrapper.get("completeness") != "complete":
        return False
    if staleness != "current" or consumable is not True:
        return False
    sel = payload.get("selection") if isinstance(payload, dict) else None
    return bool(sel and sel.get("completenessEstablished") is True)


def _test_process_result(payload):
    if payload.get("timedOut") is True or payload.get("signal") is not None or payload.get("exitStatus") is None:
        return "error"
    tests = payload.get("tests") or []
    if any(t.get("outcome") == "error" for t in tests):
        return "error"
    if payload.get("exitStatus") != 0 or any(t.get("outcome") == "fail" for t in tests):
        return "failed"
    return "passed"


def _apply_import_filters(atom, projected):
    acc = MATCH
    for flt in atom.get("filters") or []:
        field, cmp, value = flt["field"], flt["cmp"], flt["value"]
        if field not in projected:
            raise KeyError("ATOM_FILTER_FIELD_FORBIDDEN")
        raw = projected[field]
        if raw is ABSENT or raw is None:
            acc = _and_fr(acc, FUNK)
            continue
        if field == "exitStatus":
            acc = _and_fr(acc, _cmp_int(cmp, raw, value))
        else:
            acc = _and_fr(acc, _cmp_string(cmp, raw, value))
    return acc


def _plan_binding(plan, cell_ordinal, program_ordinal):
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


def _inventory_universe(inv, plan):
    if plan is None:
        return inv.get("universe")
    b = _plan_binding(plan, inv["cellOrdinal"], inv["programOrdinal"])
    if b is None:
        return inv.get("universe")
    return b.get("universe")


def _lookup_rows(native_id, universe, kind, inventories, plan, package_manifest_path=None):
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
            if row not in rows:
                rows.append(row)
    return rows


def _symbol_rows_by_path_qn(path, qn, universe, inventories, plan):
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


def _runtime_occupancy(row, subject, inventories, plan):
    k = subject["kind"]
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


def _typed_native_cause(value):
    if value is None:
        return None
    if value not in NATIVE_CAUSE_CODES:
        raise KeyError("ATOM_NATIVE_CAUSE_UNTYPED")
    return value


def _entry_from_cov(cov):
    entry = cov.get("entry") or {}
    key = cov.get("key") or {}
    rc = entry.get("resolutionCompleteness")
    if not isinstance(rc, dict):
        rc = {
            "state": "not-attempted",
            "attempted": False,
            "examinedExhaustive": False,
            "stageTerminal": None,
            "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": [],
        }
    cw = entry.get("closedWorld")
    if not isinstance(cw, dict):
        cw = {
            "exportsClosed": "unknown",
            "entryPointsRecognized": "none",
            "nonliteralLoading": "none",
            "externalConsumers": "unknown",
            "dynamicDispatch": "not-applicable",
            "reasons": [],
            "deadCodeRepairEligible": False,
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


def _conservative_entry(covs):
    cited = [c[0] for c in covs]
    entries = [_entry_from_cov(c[1]) for c in covs]
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


def _uniq_causes(causes):
    seen, out = set(), []
    for c in causes:
        if not isinstance(c, dict) or c.get("code") not in CAUSE_CODES:
            raise KeyError("ATOM_CAUSE_UNREGISTERED")
        if "evidenceKind" not in c or "nativeCause" not in c:
            raise KeyError("ATOM_CAUSE_UNREGISTERED")
        ek, nc = c.get("evidenceKind"), c.get("nativeCause")
        if ek is not None and ek not in IMPORT_EVIDENCE:
            raise KeyError("ATOM_CAUSE_UNREGISTERED")
        if nc is not None and nc not in NATIVE_CAUSE_CODES:
            raise KeyError("ATOM_CAUSE_UNREGISTERED")
        key = json.dumps(c, sort_keys=True, separators=(",", ":"))
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return sorted(out, key=lambda c: json.dumps(c, sort_keys=True, separators=(",", ":")))


def _sort_addrs(xs):
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


def _result(**kwargs):
    base = {
        "value": "indeterminate",
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
    base["knownObservationAddresses"] = _sort_addrs(base["knownObservationAddresses"])
    base["uncertainObservationAddresses"] = _sort_addrs(base["uncertainObservationAddresses"])
    base["evaluationInputRefs"] = sorted(set(base["evaluationInputRefs"]))
    return base


def _logical_path(subject, inventory_row):
    if inventory_row and inventory_row.get("path"):
        return inventory_row["path"]
    if subject["kind"] == "file":
        return subject["nativeSubjectId"]
    if subject["kind"] == "package":
        return subject.get("packageManifestPath")
    return None


def _import_scope(wrapper, inputs):
    digest = wrapper.get("scopeDigest")
    scopes = inputs.get("importScopes") or {}
    if digest and digest in scopes:
        return scopes[digest]
    raise KeyError("ATOM_IMPORT_SCOPE_UNSTATED")


def _wrapper_relevant(wrapper, subject, inputs, inventory_row):
    scope = _import_scope(wrapper, inputs)
    path = _logical_path(subject, inventory_row)
    if path is None:
        return True
    return _path_in_scope(scope, path)


def _history_in_extent(payload, wrapper, path, inputs):
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


def _runtime_subject_scalar(row, subject):
    if subject["kind"] == "file":
        return row.get("path", ABSENT)
    if subject["kind"] == "symbol":
        return row.get("symbol") if "symbol" in row else ABSENT
    return ABSENT


def _wrapper_flag(wrapper, iid, inputs, field):
    if field in wrapper:
        return wrapper[field]
    adapter = inputs.get("importFlagsAdapter") or {}
    row = adapter.get(iid) if isinstance(adapter, dict) else None
    if isinstance(row, dict):
        extra = sorted(set(row) - {"consumable", "staleness"})
        if extra:
            raise KeyError("ATOM_IMPORT_FLAG_ADAPTER")
        if field in row:
            return row[field]
    return ABSENT


def _require_wrapper_flags(wrapper, iid, inputs):
    consumable = _wrapper_flag(wrapper, iid, inputs, "consumable")
    staleness = _wrapper_flag(wrapper, iid, inputs, "staleness")
    if consumable is ABSENT:
        raise KeyError("ATOM_IMPORT_CONSUMABLE_UNSTATED")
    if staleness is ABSENT:
        raise KeyError("ATOM_IMPORT_STALENESS_UNSTATED")
    return consumable, staleness


def _addr(import_id, selector, ordinal):
    return {"importId": import_id, "selector": selector, "ordinal": ordinal}


def _icause(code, kind, **extra):
    rec = {"code": code, "evidenceKind": kind, "nativeCause": None}
    rec.update({k: v for k, v in extra.items() if v is not None})
    return rec


def _eval_imported(atom, subject, inputs, spec):
    kind = spec["evidenceKind"]
    selected = list(inputs.get("planSelectedImportIds") or [])
    wrappers = inputs.get("imports") or {}
    payloads = inputs.get("importPayloads") or {}
    inventories = inputs.get("inventories") or []
    plan = inputs.get("enumerationPlan")
    inv_rows = _lookup_rows(
        subject["nativeSubjectId"],
        subject["universe"],
        subject["kind"],
        inventories,
        plan,
        subject.get("packageManifestPath"),
    )
    inv_row = inv_rows[0] if len(inv_rows) == 1 else None
    flag_by_id = {}
    for iid in selected:
        if iid not in wrappers:
            raise KeyError("ATOM_IMPORT_WRAPPER_MISSING")
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
        return _result(
            value="indeterminate",
            kind="imported-atom",
            evaluationInputRefs=consumed,
            causes=[_icause("zero-owed-wrappers", kind), _icause("evidence-kind-unavailable", kind)],
        )

    known, uncertain, causes = [], [], []
    covering_complete = True
    for iid in owed:
        w = wrappers[iid]
        p = payloads.get(iid) or {}
        consumable, staleness = flag_by_id[iid]
        if consumable is not True or staleness != "current":
            causes.append(_icause("import-unmapped-only", kind, importId=iid))
            covering_complete = False
            continue
        if kind == "runtime":
            wrap_complete = _import_complete_runtime(w, p)
            if not wrap_complete:
                covering_complete = False
                if w.get("completeness") == "partial":
                    causes.append(_icause("wrapper-partial", kind, importId=iid))
                elif p.get("observationWindow") is None or p.get("observedPopulation") in (None, "unknown"):
                    causes.append(_icause("observation-window-insufficient", kind, importId=iid))
                else:
                    causes.append(_icause("incomplete-observation", kind, importId=iid))
            covering, matched, unobs = [], [], []
            for i, row in enumerate(p.get("subjects") or []):
                occ = _runtime_occupancy(row, subject, inventories, plan)
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
                    causes.append(
                        _icause(
                            "unobservable-subject" if obs_v == "unobservable" else "unmapped-subject",
                            kind,
                            importId=iid,
                        )
                    )
                    continue
                if obs_v in ("observed-hit", "observable-unhit"):
                    covering.append(addr)
                    proj = {
                        "observability": obs_v,
                        "subject": _runtime_subject_scalar(row, subject),
                        "resolution": "observed",
                        "subjectKind": subject["kind"],
                    }
                    fr = _apply_import_filters(atom, proj)
                    if fr == MATCH:
                        matched.append(addr)
                    elif fr == FUNK:
                        uncertain.append(addr)
            if len(matched) > 1:
                raise KeyError("ATOM_RUNTIME_ROW_AMBIGUOUS")
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
            if extent in ("listed-missing", "outside"):
                causes.append(_icause("history-outside-collection-scope", kind, importId=iid))
                covering_complete = False
                continue
            for i, row in enumerate(p.get("subjects") or []):
                if row.get("path") != path:
                    continue
                proj = {
                    "subject": row.get("path"),
                    "resolution": "observed",
                    "subjectKind": subject["kind"],
                }
                fr = _apply_import_filters(atom, proj)
                addr = _addr(iid, "history-subject", i)
                if fr == MATCH:
                    known.append(addr)
                elif fr == FUNK:
                    uncertain.append(addr)
        elif kind == "test":
            wrap_complete = _import_complete_test(w, p, consumable, staleness)
            if not wrap_complete:
                covering_complete = False
                if w.get("completeness") == "partial":
                    causes.append(_icause("wrapper-partial", kind, importId=iid))
                causes.append(_icause("test-completeness-not-established", kind, importId=iid))
            if spec.get("observationAddressSelector") == "test-execution":
                pr = _test_process_result(p)
                path = _logical_path(subject, inv_row)
                proj = {
                    "testResult": pr,
                    "exitStatus": p.get("exitStatus", ABSENT),
                    "resolution": "observed",
                    "subjectKind": subject["kind"],
                    "subject": path or ABSENT,
                }
                fr = _apply_import_filters(atom, proj)
                addr = _addr(iid, "test-execution", None)
                if fr == MATCH:
                    known.append(addr)
                elif fr == FUNK:
                    uncertain.append(addr)
                    if p.get("exitStatus") is None:
                        causes.append(_icause("null-exit-status", kind, importId=iid))
            else:
                path = _logical_path(subject, inv_row)
                for i, row in enumerate(p.get("tests") or []):
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
                    fr = _apply_import_filters(atom, proj)
                    if fr == MATCH:
                        known.append(_addr(iid, "test-case", i))
                    elif fr == FUNK:
                        uncertain.append(_addr(iid, "test-case", i))

    op = atom["op"]
    nlimit = atom.get("n")
    if op == "exists" and known:
        return _result(
            value="true",
            kind="imported-atom",
            knownObservationAddresses=known,
            uncertainObservationAddresses=uncertain,
            causes=causes,
            evaluationInputRefs=consumed,
        )
    if op == "none" and known:
        return _result(
            value="false",
            kind="imported-atom",
            knownObservationAddresses=known,
            uncertainObservationAddresses=uncertain,
            causes=causes,
            evaluationInputRefs=consumed,
        )
    if op == "count-at-most" and len(known) > nlimit:
        return _result(
            value="false",
            kind="imported-atom",
            knownObservationAddresses=known,
            uncertainObservationAddresses=uncertain,
            causes=causes,
            evaluationInputRefs=consumed,
        )
    incomplete = (not covering_complete) or any(
        c["code"]
        in {
            "incomplete-observation",
            "unobservable-subject",
            "unmapped-subject",
            "no-consumable-row",
            "import-unmapped-only",
            "history-outside-collection-scope",
            "history-truncated",
            "test-completeness-not-established",
            "wrapper-partial",
            "null-exit-status",
            "overload-ambiguous",
            "target-metadata-unknown",
        }
        for c in causes
    ) or bool(uncertain)
    if op == "exists":
        val = "false" if not incomplete else "indeterminate"
    elif op in ("none", "count-at-most"):
        val = "true" if not incomplete else "indeterminate"
    else:
        val = "true" if not incomplete else "indeterminate"
        if kind == "runtime" and not known and any(c["code"] == "no-consumable-row" for c in causes):
            val = "indeterminate"
    return _result(
        value=val,
        kind="imported-atom",
        knownObservationAddresses=known,
        uncertainObservationAddresses=uncertain,
        causes=causes,
        evaluationInputRefs=consumed,
    )


def replay_line(kind_set, path):
    ok = fail = 0
    fails = []
    for i, line in enumerate(path.read_text().splitlines()):
        c = json.loads(line)
        kind = c.get("kind")
        exp = c.get("expected")
        try:
            actual = None
            refused = None
            if kind == "scope":
                q = c["input"]
                actual = _path_in_scope(q["scope"], q["path"])
            elif kind == "string":
                q = c["input"]
                try:
                    actual = _cmp_string(q["cmp"], q["projected"], q["value"])
                except KeyError as e:
                    refused = e.args[0]
            elif kind == "int":
                q = c["input"]
                try:
                    actual = _cmp_int(q["cmp"], q["projected"], q["value"])
                except KeyError as e:
                    refused = e.args[0]
            elif kind == "completeness":
                q = c["input"]
                actual = [
                    _import_complete_runtime(q["wrapper"], q["payload"]),
                    _import_complete_history(q["wrapper"], q["payload"]),
                    _import_complete_test(q["wrapper"], q["payload"], q["consumable"], q["staleness"]),
                ]
            elif kind == "process":
                actual = _test_process_result(c["input"])
            elif kind == "filters":
                q = c["input"]
                try:
                    actual = _apply_import_filters(q["atom"], q["projected"])
                except KeyError as e:
                    refused = e.args[0]
            elif kind == "lookup":
                q = c["input"]
                s = q["subject"]
                plan = None if q["plan"] is None else q["plan"]
                actual = _lookup_rows(
                    s["nativeSubjectId"],
                    s["universe"],
                    s["kind"],
                    q["inventories"],
                    plan,
                    s.get("packageManifestPath"),
                )
            elif kind == "occupancy":
                q = c["input"]
                s = q["subject"]
                plan = None if q["plan"] is None else q["plan"]
                actual = _runtime_occupancy(q["row"], s, q["inventories"], plan)
            elif kind == "causes":
                try:
                    actual = _uniq_causes(c["input"])
                except KeyError as e:
                    refused = e.args[0]
            elif kind == "addresses":
                actual = _sort_addrs(c["input"])
            elif kind == "result":
                q = c["input"]
                try:
                    actual = _result(
                        value=q["value"],
                        kind="imported-atom",
                        knownObservationAddresses=q["known"],
                        uncertainObservationAddresses=q["uncertain"],
                        causes=q["causes"],
                        evaluationInputRefs=q["consumed"],
                    )
                except KeyError as e:
                    refused = e.args[0]
            elif kind == "entry":
                try:
                    actual = _entry_from_cov(c["input"])
                except KeyError as e:
                    refused = e.args[0]
            elif kind == "fold":
                try:
                    e, ids = _conservative_entry([(a[0], a[1]) for a in c["input"]])
                    actual = [e, ids]
                except KeyError as e:
                    refused = e.args[0]
            elif kind == "sufficiency":
                q = c["input"]
                actual = sufficiency_v2(q["req"], q["view"], bool(q["exported"]), bool(q["affected"]), int(q["depth"]))
            elif c.get("label") and "atom" in c and "spec" in c:
                kind = c.get("label")
                try:
                    actual = _eval_imported(c["atom"], c["subject"], c["inputs"], c["spec"])
                except KeyError as e:
                    refused = e.args[0]
            else:
                raise RuntimeError("unhandled " + str(kind))
            if isinstance(exp, dict) and "refused" in exp:
                if refused != exp["refused"]:
                    fail += 1
                    if len(fails) < 8:
                        fails.append((i, kind, refused, exp["refused"]))
                else:
                    ok += 1
            else:
                expected = exp.get("value") if isinstance(exp, dict) and "value" in exp else exp
                if refused is not None or actual != expected:
                    fail += 1
                    if len(fails) < 8:
                        fails.append((i, kind, actual if refused is None else refused, expected))
                else:
                    ok += 1
        except Exception as e:
            fail += 1
            if len(fails) < 8:
                fails.append((i, kind, type(e).__name__ + ":" + str(e)[:180], exp))
    return ok, fail, fails


def main():
    native_src = NATIVE_SRC.read_text()
    assert "def sufficiency_v2(" in native_src
    assert json.dumps(DEPENDS_ON, separators=(",", ":")) in json.dumps(
        {"reachability": [{"relation": "calls", "minResolution": "resolved-callee"}], "clones": [{"relation": "declares", "minResolution": "syntactic"}]},
        separators=(",", ":"),
    )
    assert REG["scanner"]["dependsOn"] == DEPENDS_ON
    assert REG["scanner"]["sufficiencyPrecedence"] == PRECEDENCE_V2
    assert REG["scanner"]["rungCause"] == RUNG_CAUSE
    for name, ladder in LADDERS.items():
        assert REG["relations"][name]["ladder"] == ladder, name

    reports = {}
    for label, rel in [
        ("helpers", "atom-helper-check/cases.ndjson"),
        ("inventory", "atom-inventory-check/cases.ndjson"),
        ("results", "atom-result-check/cases.ndjson"),
        ("native-sufficiency", "native-sufficiency-check/cases.ndjson"),
        ("imported", "imported-atom-check/cases.ndjson"),
    ]:
        ok, fail, fails = replay_line(label, TRIAL / rel)
        reports[label] = {"ok": ok, "fail": fail, "fails": fails}
        print(label, "ok", ok, "fail", fail)
        for row in fails:
            print(" ", row)
    Path("/tmp/opensip-implementation/m2-grok-atom-kernel-50-advisory/review/python-replay.json").write_text(
        json.dumps(reports, indent=2, default=str) + "\n"
    )
    if any(v["fail"] for v in reports.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
