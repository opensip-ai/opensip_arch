"""Independent evaluator3: population, atom evaluation (native endpoint=source; imported runtime/history), strong
Kleene composition, witnesses, predicate proofs, findings, waivers, rule results, execution deficiencies, verdict,
proof bundle, semantic evidence, seal, Run and policy derivation.

Sources: identity-and-evidence s4; enumeration-contract s1-s5; atom-evaluation-contract s1-s7;
evaluator-composition-contract.v3 s2-s5 and s9; evaluator-projection-registry.v1.json; native s4.6 (sufficiency_v2);
glob-pattern-contract.v1. Reads only admitted retained inputs; never a claimed finding/witness/verdict.

Not reconstructed here (refused, never guessed): endpoint=target atoms ('cb24.ATOM_ENDPOINT_TARGET_NOT_RECONSTRUCTED')
and test-plane atoms ('cb24.IMPORTED_ATOM_RELATION_NOT_RECONSTRUCTED'). No retained Run of this review uses them.
"""
import hashlib

import canonical as K
import schemas
import membership as M
from globmatch import glob_match, rule_enumeration_selects, scope_document_selects
from native_facts import RELS, sufficiency_v2, ladder_ok, ladder_index, RESOLVED, DEPENDS_ON
from execinputs import cset, bridge, sfx

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
PROJ = KIT.doc("foundation/evaluator-projection-registry.v1.json")
PROFILE = KIT.doc(ID)["x-opensip-evaluator-profile"]
DEFREG = KIT.doc(ID)["x-opensip-evaluator-deficiency-registry"]
LANGUAGE_MODES = KIT.doc(ID)["x-opensip-digest-domains"]["languageModes"]["map"]
SEV = {"note": 0, "warning": 1, "error": 2}
NONBLOCKING = set(DEFREG["nonBlockingDisclosures"])
ATOM_OPS = {"exists", "none", "count-at-most", "all-covered"}
FAMILY_OF_DOMAIN = {v["universeDomain"]: k for k, v in PROJ["engineFamilies"]["families"].items()}
FAMILY_OF_MODE = {m: k for k, v in PROJ["engineFamilies"]["families"].items() for m in v["languageModes"]}
U64_MAX = 2 ** 64 - 1
EMPTY_DISCRIMINATOR = hashlib.sha256(K.C([])).hexdigest()


class EvalRefusal(Exception):
    def __init__(self, key, detail=""):
        super().__init__(f"{key}:{detail}" if detail else key)
        self.key = key


class Inputs:
    """Admitted retained evaluation inputs (joined by closure). Attribute bag; see closure.build_inputs."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


def build_rule_program(policy):
    return {"schemaVersion": 2, "policyDigest": K.raw_digest(policy),
            "rules": [{"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]} for r in policy["rules"]]}


def node_list(pred, addr="p"):
    out = []
    if pred["op"] in ("and", "or"):
        for i, ch in enumerate(pred["operands"]):
            out += node_list(ch, f"{addr}.{i}")
    elif pred["op"] == "not":
        out += node_list(pred["operand"], f"{addr}.0")
    out.append((addr, pred))
    return out


def children_addrs(pred, addr):
    if pred["op"] in ("and", "or"):
        return [f"{addr}.{i}" for i in range(len(pred["operands"]))]
    if pred["op"] == "not":
        return [f"{addr}.0"]
    return []


def kleene(op, vals):
    if op == "not":
        return {"true": "false", "false": "true"}.get(vals[0], "indeterminate")
    if op == "and":
        if "false" in vals:
            return "false"
        return "true" if all(v == "true" for v in vals) else "indeterminate"
    if "true" in vals:
        return "true"
    return "false" if all(v == "false" for v in vals) else "indeterminate"


def ckey(x):
    return K.C(x)


# ------------------------------------------------------------------ enumeration (composition s2, s9.5)
def rule_enumeration(inp, rule):
    empty = {"state": "disabled", "inventoryRefs": [], "selectedSubjectIds": [], "unresolvedSubjectIds": [], "incompleteInventoryRefs": []}
    token = rule["subjectEnumeration"]["universe"]
    if token not in PROFILE["policyUniverseMap"]:
        raise EvalRefusal("EVALUATOR_POLICY_UNIVERSE_TOKEN_UNKNOWN", token)
    if not rule["enabled"]:
        return empty, [], {}, []
    kind_req = rule["subjectEnumeration"]["subjectKind"]
    primary = "symbol" if kind_req == "export" else kind_req
    defs, refs, incomplete, population = [], [], [], []
    subjects, unresolved = {}, set()
    for (ci, po, kind), (digest, inv) in sorted(inp.inventories.items()):
        cell = inp.enum_plan["cells"][ci]
        if kind != primary or LANGUAGE_MODES[cell["languageMode"]] != token:
            continue
        b = cell["programBindings"][po]
        ref = {"domain": "subject-inventory", "digest": digest}
        refs.append(ref)
        if inv["state"] != "complete":
            incomplete.append(ref)
            defs.append({"source": "enumeration", "cause": "incomplete-inventory", "subjectId": None, "predicateId": None,
                         "inputRefs": [ref], "evidenceKind": None, "nativeCause": inv["nativeCause"], "universe": None})
            if inv["deficiency"] == "source-syntax-invalid":
                defs.append({"source": "enumeration", "cause": "source-syntax-invalid", "subjectId": None, "predicateId": None,
                             "inputRefs": [ref], "evidenceKind": None, "nativeCause": None, "universe": None})
        for row in inv["rows"]:
            population.append((b["universe"], row))
            se = rule["subjectEnumeration"]
            if not rule_enumeration_selects(se.get("include"), se.get("exclude"), row["path"]):
                continue
            if inp.scope_document is not None and not scope_document_selects(inp.scope_document, row["path"]):
                continue
            rec = {"schemaVersion": 3, "universe": b["universe"], "kind": row["kind"], "nativeSubjectId": row["nativeSubjectId"]}
            if row["kind"] == "package":
                rec["packageManifestPath"] = row["path"]
            sid = K.identifier("evaluation-subject", rec)
            if kind_req == "export":
                if row.get("exported") == "not-exported":
                    continue
                if row.get("exported") != "exported":
                    unresolved.add(sid)
                    defs.append({"source": "enumeration", "cause": "unknown-export-membership", "subjectId": sid, "predicateId": None,
                                 "inputRefs": [ref], "evidenceKind": None, "nativeCause": None, "universe": None})
                    continue
            if sid in subjects:
                if K.C(subjects[sid]["row"]) != K.C(row):
                    raise EvalRefusal("cb24.ENUMERATION_ATTRIBUTION_CONFLICT", sid)
                continue
            subjects[sid] = {"record": rec, "row": row, "cell": cell, "binding": b, "inventoryRef": ref}
    if not refs:
        defs.append({"source": "enumeration", "cause": "no-covering-program", "subjectId": None, "predicateId": None,
                     "inputRefs": [], "evidenceKind": None, "nativeCause": None, "universe": None})
    enum = {"state": "incomplete" if defs else "complete", "inventoryRefs": cset(refs),
            "selectedSubjectIds": sorted(subjects, key=ckey), "unresolvedSubjectIds": sorted(unresolved, key=ckey),
            "incompleteInventoryRefs": cset(incomplete)}
    return enum, cset(defs), subjects, population


# ------------------------------------------------------------------ native atom (endpoint=source), atom contract s3-s5
def fold_entries(entries):
    rank_cov = {"complete": 0, "unknown": 1}
    rank_rc = {"complete": 0, "not-applicable": 0, "partial": 1, "incomplete": 2, "not-attempted": 3}
    rank_cw = {"closed": 0, "open": 1, "unknown": 2}
    cur = dict(entries[0])
    kinds = list(cur["derivationKinds"])
    for e in entries[1:]:
        if rank_cov[e["coverage"]] > rank_cov[cur["coverage"]]:
            cur["coverage"] = e["coverage"]
        cur["confidenceMillionths"] = min(cur["confidenceMillionths"], e["confidenceMillionths"])
        if rank_rc[e["resolutionCompleteness"]["state"]] > rank_rc[cur["resolutionCompleteness"]["state"]]:
            cur["resolutionCompleteness"] = e["resolutionCompleteness"]
        if rank_cw[e["closedWorld"]["exportsClosed"]] > rank_cw[cur["closedWorld"]["exportsClosed"]]:
            cur["closedWorld"] = e["closedWorld"]
        kinds += [k for k in e["derivationKinds"] if k not in kinds]
    cur["derivationKinds"] = kinds
    cur["deficiency"], cur["nativeCause"] = next(((e["deficiency"], e["nativeCause"]) for e in entries if e["deficiency"] is not None), (None, None))
    return cur


def refusal_key(name, fallback):
    return name if name in str(PROJ.get("refusals", "")) else fallback


def filter_admission(atom):
    rel, table = atom["relation"], PROJ["comparatorTable"]
    for f in atom["filters"]:
        spec = PROJ["relations"][rel]["filters"].get(f["field"], "forbidden")
        if isinstance(spec, dict):
            spec = spec.get(atom["minResolution"], "forbidden")
        if spec == "forbidden":
            raise EvalRefusal(refusal_key("ATOM_FILTER_FIELD_FORBIDDEN", "cb24.ATOM_FILTER_FIELD_FORBIDDEN"), f"{rel}:{f['field']}")
        if not table[f["field"]].get(f["cmp"]):
            raise EvalRefusal("ATOM_FILTER_COMPARATOR_ILLEGAL", f"{f['field']}:{f['cmp']}")
        enum = table[f["field"]].get("enum")
        if f["field"] == "universe":
            enum = PROJ["engineFamilies"]["portableUniverseDomains"]
        elif f["field"] == "resolution":
            enum = RELS[rel]["ladder"]
        if enum and f["cmp"] in ("eq", "neq", "in"):
            vals = f["value"] if isinstance(f["value"], list) else [f["value"]]
            if any(v not in enum for v in vals):
                raise EvalRefusal("ATOM_FILTER_ENUM_LITERAL_UNKNOWN", f"{f['field']}:{f['value']}")


def projection_value(field, rel, fact, payload, subject, min_rung):
    spec = PROJ["relations"][rel]["filters"][field]
    if isinstance(spec, dict):
        spec = spec[min_rung]
    if spec.startswith("payload."):
        return payload.get(spec[8:])
    if spec == "fact.anchors[0].path":
        return fact["anchors"][0]["path"] if fact["anchors"] else None
    if spec == "fact.resolution":
        return fact["resolution"]
    if spec == "fact.confidenceMillionths":
        return fact["confidenceMillionths"]
    if spec == "endpoint-universe-domain":
        return subject["domain"]
    if spec == "inventory.kind" or spec.startswith("source-endpoint-kind"):
        return subject["record"]["kind"]
    if spec.startswith("targetAttribution."):
        return None  # outgoing atoms carry no target attribution in this reconstruction: unknown, never a nomatch
    raise EvalRefusal("cb24.ATOM_FILTER_PROJECTION_NOT_RECONSTRUCTED", spec)


def filter_match(f, value):
    cmp, want = f["cmp"], f["value"]
    if value is None:
        return None
    if cmp == "eq":
        return value == want
    if cmp == "neq":
        return value != want
    if cmp == "in":
        return value in want
    if cmp == "prefix":
        return isinstance(value, str) and value.encode().startswith(want.encode())
    if cmp == "glob":
        return isinstance(value, str) and glob_match(want, value)
    if cmp == "gte":
        return value >= want
    if cmp == "lte":
        return value <= want
    return None


def occupies_source(rel, fact, payload, subject):
    rec = subject["record"]
    if rel == "package":
        return payload.get("packageName") == rec["nativeSubjectId"] and payload.get("manifestPath") == rec.get("packageManifestPath")
    field = PROJ["relations"][rel]["sourceField"]
    if field == "anchors[0].path":
        return bool(fact["anchors"]) and fact["anchors"][0]["path"] == rec["nativeSubjectId"]
    return payload.get(field) == rec["nativeSubjectId"]


def dep_closure(rel):
    seen, queue, out = {rel}, [rel], []
    while queue:
        r = queue.pop(0)
        for d in DEPENDS_ON.get(r, []):
            if d["relation"] not in seen:
                seen.add(d["relation"])
                out.append(d)
                queue.append(d["relation"])
    return out


def native_atom(inp, atom, subject, sel_views):
    rel, minr = atom["relation"], atom["minResolution"]
    if atom.get("endpoint", "source") != "source":
        raise EvalRefusal("cb24.ATOM_ENDPOINT_TARGET_NOT_RECONSTRUCTED")
    if rel not in PROJ["relations"] or PROJ["relations"][rel]["plane"] != "native" or not ladder_ok(rel, minr):
        raise EvalRefusal("cb24.ATOM_RELATION_OR_RUNG_UNREGISTERED", f"{rel}@{minr}")
    if atom.get("evidence") is not None:
        raise EvalRefusal("ATOM_EVIDENCE_KIND_MISMATCH", "native atom with evidence kind")
    reg = PROJ["relations"][rel]
    if subject["record"]["kind"] != reg["sourceSubjectKind"]:
        raise EvalRefusal("ATOM_KIND_INCOMPATIBLE", f"{rel}:{subject['record']['kind']}")
    filter_admission(atom)
    U = subject["record"]["universe"]
    nid = subject["record"]["nativeSubjectId"]
    sub_family = FAMILY_OF_DOMAIN.get(subject["domain"])
    cap = PROJ["capabilityForRelation"][rel]
    owed = [(cell, b) for cell in inp.enum_plan["cells"] if cell["capabilityId"] == cap for b in cell["programBindings"]]
    causes, native_defs, scope_ids, coverage_ids = [], [], [], set()
    complete = True

    def cause(code, universe=None, native_cause=None):
        c = {"code": code, "evidenceKind": None, "nativeCause": native_cause}
        if universe is not None:
            c["universe"] = universe
        causes.append(c)

    for cell, b in owed:  # P1
        if b["universe"] is None:
            bfam = FAMILY_OF_MODE.get(cell["languageMode"])
            if bfam is not None and sub_family is not None and bfam != sub_family:
                cause("cross-family-edge-not-owed")
    sel_scopes = sorted({s for v in sel_views for s in inp.views[v]["scopeIds"]}, key=ckey)
    sel_covs = sorted({c for v in sel_views for c in inp.views[v]["coverageIds"]}, key=ckey)
    if not owed:  # P2
        cause("missing-relation-coverage")
        complete = False
    elif not any(b["universe"] == U for _, b in owed):  # step 1
        cause("selector-unbound")
        complete = False
    else:
        containing = [s for s in sel_scopes if inp.scopes[s]["relation"] == rel and inp.scopes[s]["resolution"] == minr
                      and inp.scopes[s]["sourceUniverse"] == U and nid in inp.scopes[s]["subjects"]]
        if not containing:  # step 2
            cause("uncovered-expected-source-subject", U)
            complete = False
        else:  # step 3
            scope_ids = containing
            paired = {s: [c for c in sel_covs if inp.coverages[c][0]["scopeId"] == s] for s in containing}
            unpaired = [s for s in containing if not paired[s]]
            for _ in unpaired:
                cause("scope-without-coverage", U)
            if unpaired:
                complete = False
            else:  # step 4
                for cid in sorted({c for cs in paired.values() for c in cs}, key=ckey):
                    coverage_ids.add(cid)
                    key, entry = inp.coverages[cid][1]["key"], inp.coverages[cid][1]["entry"]
                    view = {rel: entry}
                    positions = [entry]
                    for dep in dep_closure(rel):
                        drel, drung = dep["relation"], dep["minResolution"]
                        same_kind = PROJ["relations"][drel]["sourceSubjectKind"] == reg["sourceSubjectKind"]
                        picked = []
                        for dc in sel_covs:
                            dcov, dpay = inp.coverages[dc]
                            dk = dpay["key"]
                            if dk["relation"] != drel or dk["resolution"] != drung or dk["sourceUniverse"] != key["sourceUniverse"] \
                                    or dk["targetUniverse"] != key["targetUniverse"]:
                                continue
                            if same_kind:
                                ds = inp.scopes[dcov["scopeId"]]
                                if not (ds["relation"] == drel and ds["resolution"] == drung and ds["sourceUniverse"] == key["sourceUniverse"]
                                        and nid in ds["subjects"]):
                                    continue
                            picked.append(dc)
                        picked = sorted(set(picked), key=ckey)
                        if picked:
                            folded = fold_entries([inp.coverages[p][1]["entry"] for p in picked])
                            view[drel] = folded
                            positions.append(folded)
                            coverage_ids |= set(picked)
                    quant = "universal-negative" if minr in RESOLVED else "existential"
                    req = {"relation": rel, "minResolution": minr, "completeness": "complete", "quantifier": quant,
                           "unresolvedEdgePolicy": "forbid", "externalConsumerPolicy": "forbid", "minConfidenceMillionths": 0}
                    s = sufficiency_v2(req, view)
                    if not s["satisfied"]:
                        nc = next((p["nativeCause"] for p in positions if p["nativeCause"] is not None), None)
                        cause("coverage-unknown", key["sourceUniverse"], nc)
                        native_defs.append(s["deficiency"])
                        complete = False
    known, uncertain = set(), set()
    for v in sel_views:
        for fid in inp.views[v]["facts"]:
            f, p = inp.facts[fid], inp.fact_payloads[fid]
            if f["relation"] != rel or not ladder_ok(rel, f["resolution"]) or ladder_index(rel, f["resolution"]) < ladder_index(rel, minr):
                continue
            if f["sourceUniverse"] != U or not occupies_source(rel, f, p, subject):
                continue
            verdicts = [filter_match(flt, projection_value(flt["field"], rel, f, p, subject, minr)) for flt in atom["filters"]]
            if all(x is True for x in verdicts):
                known.add(fid)
            elif not any(x is False for x in verdicts):
                uncertain.add(fid)
    blocking = [c for c in causes if c["code"] not in NONBLOCKING]
    comp_ok = complete and not blocking and not uncertain
    op = atom["op"]
    if op == "exists":
        value = "true" if known else ("false" if comp_ok else "indeterminate")
    elif op == "none":
        value = "false" if known else ("true" if comp_ok else "indeterminate")
    elif op == "count-at-most":
        value = "false" if len(known) > atom["n"] else ("true" if comp_ok else "indeterminate")
    else:
        value = "true" if (complete and not blocking) else "indeterminate"
    return {"plane": "native", "value": value, "knownFactIds": sorted(known, key=ckey), "uncertainFactIds": sorted(uncertain, key=ckey),
            "knownRows": [], "uncertainRows": [], "coverageIds": sorted(coverage_ids, key=ckey), "scopeIds": scope_ids,
            "causes": causes, "nativeDeficiencies": native_defs}


# ------------------------------------------------------------------ imported atoms (atom contract s6)
IMPORT_REL_KIND = {"runtime-observation": "runtime", "history-change": "history"}


def imported_atom(inp, atom, subject, rule):
    rel = atom["relation"]
    kind = IMPORT_REL_KIND.get(rel)
    if kind is None:
        raise EvalRefusal("cb24.IMPORTED_ATOM_RELATION_NOT_RECONSTRUCTED", rel)
    if atom.get("evidence") != kind:
        raise EvalRefusal("ATOM_EVIDENCE_KIND_MISMATCH", f"{rel}:{atom.get('evidence')}")
    path = subject["row"]["path"]
    owed = [iid for iid in sorted(inp.plan["importIds"], key=ckey)
            if inp.imports[iid]["kind"] == kind and M.in_foundation_scope(path, inp.import_scopes[iid])]
    causes, known_rows, uncertain_rows = [], [], []
    complete = True

    def cause(code, iid=None):
        c = {"code": code, "evidenceKind": kind, "nativeCause": None}
        if iid is not None:
            c["importId"] = iid
        causes.append(c)

    if not owed:
        cause("zero-owed-wrappers")
        cause("evidence-kind-unavailable")
        complete = False
    for iid in owed:
        wrapper, payload, obs = inp.imports[iid], inp.import_payloads[iid], inp.import_observations[iid]
        flags = inp.import_flags[iid]
        if not flags["consumable"]:
            cause("import-unmapped-only", iid)
            complete = False
            continue
        if wrapper["completeness"] != "complete":
            cause("wrapper-partial", iid)
            complete = False
        if kind == "runtime":
            if (obs.get("window") is not None and obs["window"] != payload["observationWindow"]) or \
                    (obs.get("population") is not None and obs["population"] != payload["observedPopulation"]):
                raise EvalRefusal("ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN")
            if payload.get("observationWindow") is None or payload.get("observedPopulation") in (None, "unknown"):
                cause("observation-window-insufficient", iid)
                complete = False
            rows = [(i, r) for i, r in enumerate(payload["subjects"]) if r["path"] == path and r.get("symbol") is None]
            if len(rows) > 1:
                raise EvalRefusal("RUNTIME_SUBJECT_DUPLICATE_KEY")
            pol = [f for f in atom["filters"] if f["field"] == "observability"]
            if not rows:
                cause("no-consumable-row", iid)
                complete = False
            for i, r in rows:
                addr = {"importId": iid, "selector": "runtime-subject", "ordinal": i}
                if r["observability"] in ("observed-hit", "observable-unhit"):
                    if all(filter_match(f, r["observability"]) for f in pol):
                        known_rows.append(addr)
                else:
                    uncertain_rows.append(addr)
                    cause("unobservable-subject" if r["observability"] == "unobservable" else "unmapped-subject", iid)
                    complete = False
        else:
            rr = payload["revisionRange"]
            if (obs.get("revisionRange") is not None and
                    (obs["revisionRange"]["from"] != rr["from"] or obs["revisionRange"]["to"] != rr["to"])):
                raise EvalRefusal("ATOM_IMPORT_OBSERVATION_PAYLOAD_JOIN")
            if rr.get("truncated"):
                cause("history-truncated", iid)
                complete = False
            rows = [(i, r) for i, r in enumerate(payload["subjects"]) if r["path"] == path]
            if payload["collectionScope"] == "listed-paths" and not rows:
                cause("history-outside-collection-scope", iid)
                complete = False
            known_rows += [{"importId": iid, "selector": "history-subject", "ordinal": i} for i, _ in rows]
    known_rows, uncertain_rows = cset(known_rows), cset(uncertain_rows)
    comp_ok = complete and not uncertain_rows
    op = atom["op"]
    if op == "exists":
        value = "true" if known_rows else ("false" if comp_ok else "indeterminate")
    elif op == "none":
        value = "false" if known_rows else ("true" if comp_ok else "indeterminate")
    elif op == "count-at-most":
        value = "false" if len(known_rows) > atom["n"] else ("true" if comp_ok else "indeterminate")
    else:
        value = "true" if comp_ok else "indeterminate"
    return {"plane": "import", "value": value, "knownFactIds": [], "uncertainFactIds": [], "knownRows": known_rows,
            "uncertainRows": uncertain_rows, "coverageIds": [], "scopeIds": [], "causes": causes, "nativeDeficiencies": []}


# ------------------------------------------------------------------ composition s9.5 atom-mapped deficiencies
def atom_deficiencies(res, atom, sid, addr, EI, inp):
    plane, out = res["plane"], []
    for c in res["causes"]:
        if c["code"] not in set(DEFREG["sources"][plane]) | NONBLOCKING and c["code"] not in ("scope-without-coverage",):
            raise EvalRefusal("EVALUATOR_ATOM_CAUSE_UNREGISTERED", c["code"])
        if plane == "import" and c["evidenceKind"] != atom.get("evidence"):
            raise EvalRefusal("EVALUATOR_ATOM_CAUSE_PLANE_JOIN", c["code"])
        out.append({"source": plane, "cause": c["code"], "subjectId": sid, "predicateId": addr, "inputRefs": EI,
                    "evidenceKind": atom.get("evidence") if plane == "import" else None, "nativeCause": c["nativeCause"],
                    "universe": c.get("universe")})
    for d in res["nativeDeficiencies"]:
        out.append({"source": "native", "cause": d, "subjectId": sid, "predicateId": addr, "inputRefs": EI,
                    "evidenceKind": None, "nativeCause": None, "universe": None})
    for cid in res["coverageIds"]:
        cov, payload = inp.coverages[cid]
        if payload["entry"]["deficiency"] is not None:
            out.append({"source": "native", "cause": payload["entry"]["deficiency"], "subjectId": sid, "predicateId": addr,
                        "inputRefs": [{"domain": "coverage", "digest": sfx(cid)}], "evidenceKind": None,
                        "nativeCause": payload["entry"]["nativeCause"], "universe": payload["key"]["sourceUniverse"]})
    return cset(out)


def is_blocking(d, rule):
    if d["cause"] in NONBLOCKING:
        return False
    if d["source"] == "import":
        return any(e["kind"] == d["evidenceKind"] and e["requirement"] == "required" for e in rule["evidenceUse"])
    return True


def budget_charge(inp, enumerations, sel_views, EI, rules):
    E = sum(len(inv["rows"]) for _, inv in inp.inventories.values()) + len(inp.inventories)
    F = len({f for v in sel_views for f in inp.views[v]["facts"]})
    I = 0
    for iid in inp.plan["importIds"]:
        p = inp.import_payloads[iid]
        I += len(p.get("subjects", [])) if "subjects" in p else len(p.get("tests", [])) + 1
    Kc = len({r["digest"] for r in EI if r["domain"] == "coverage"})
    total = E
    for rule in rules:
        if not rule["enabled"]:
            continue
        nodes = node_list(rule["emitWhen"])
        A = sum(1 for _, n in nodes if n["op"] in ATOM_OPS)
        per = len(nodes) + A * (F + I + Kc)
        total += len(enumerations[rule["ruleId"]][2]) * per
        if total > U64_MAX:
            return U64_MAX + 1, {"E": E, "F": F, "I": I, "K": Kc, "overflow": True}
    return total, {"E": E, "F": F, "I": I, "K": Kc, "overflow": False}


def evaluate(inp):
    blobs, objects = {}, {}
    xi = {"domain": "execution-inputs", "digest": inp.exec_inputs_digest}
    EI = cset(inp.exec_inputs["selectedRefs"] + [xi])
    sel_views = sorted(["view2:" + r["digest"] for r in EI if r["domain"] == "view"], key=ckey)
    policy = inp.policy
    program = build_rule_program(policy)
    program_digest = K.raw_digest(program)
    blobs[program_digest] = K.C(program)
    bindings = {r["ruleId"]: r for r in inp.emission["rules"]}
    rules = sorted(policy["rules"], key=lambda r: r["ruleId"].encode())
    enumerations = {r["ruleId"]: rule_enumeration(inp, r) for r in rules}
    charge, charge_detail = budget_charge(inp, enumerations, sel_views, EI, rules)
    exhausted = charge > inp.plan["budget"]["limit"]
    exec_defs = bridge(inp.required_rows, xi)
    if exhausted:
        exec_defs = cset(exec_defs + [{"source": "execution", "cause": "work-budget-exhausted", "subjectId": None, "predicateId": None,
                                       "inputRefs": EI, "evidenceKind": None, "nativeCause": None, "universe": None}])
    import_kinds = {inp.imports[i]["kind"] for i in inp.plan["importIds"]}
    predicate_proofs, findings, rule_results, waived = [], [], [], []
    for rule in rules:
        enum, enum_defs, subjects, population = enumerations[rule["ruleId"]]
        rdefs, rfindings = list(enum_defs), []
        blocked_root = False
        required_import_missing = False
        if rule["enabled"]:
            for ev in rule["evidenceUse"]:
                if ev["requirement"] == "required" and ev["kind"] not in import_kinds:
                    required_import_missing = True
                    rdefs.append({"source": "import", "cause": "evidence-kind-unavailable", "subjectId": None, "predicateId": None,
                                  "inputRefs": [], "evidenceKind": ev["kind"], "nativeCause": None, "universe": None})
            if exhausted:
                rdefs.append({"source": "execution", "cause": "work-budget-exhausted", "subjectId": None, "predicateId": None,
                              "inputRefs": [], "evidenceKind": None, "nativeCause": None, "universe": None})
            else:
                for sid in enum["selectedSubjectIds"]:
                    subject = dict(subjects[sid], domain=inp.bound[subjects[sid]["record"]["universe"]]["domain"])
                    results = {}
                    for addr, node in node_list(rule["emitWhen"]):
                        op = node["op"]
                        ppd = {"schemaVersion": 2, "ruleProgramDigest": program_digest, "ruleId": rule["ruleId"], "predicateId": addr,
                               "operation": op, "nodeDigest": hashlib.sha256(K.C(node)).hexdigest()}
                        ppd_digest = K.raw_digest(ppd)
                        blobs[ppd_digest] = K.C(ppd)
                        if op in ATOM_OPS:
                            res = imported_atom(inp, node, subject, rule) if node.get("evidence") is not None or \
                                node["relation"] in IMPORT_REL_KIND else native_atom(inp, node, subject, sel_views)
                            defs = atom_deficiencies(res, node, sid, addr, EI, inp)
                            witness = {"schemaVersion": 3, "programPredicateDigest": ppd_digest, "matchingFactIds": res["knownFactIds"],
                                       "coverageIds": res["coverageIds"], "countLimit": node["n"] if op == "count-at-most" else None,
                                       "childPredicateIds": [], "matchingImportRows": res["knownRows"],
                                       "uncertainFactIds": res["uncertainFactIds"], "uncertainImportRows": res["uncertainRows"],
                                       "deficiencies": defs, "kind": "native-atom" if res["plane"] == "native" else "imported-atom"}
                            value = res["value"]
                            node_res = {"value": value, "defs": defs, "facts": set(res["knownFactIds"]), "ufacts": set(res["uncertainFactIds"]),
                                        "rows": res["knownRows"], "urows": res["uncertainRows"], "coverage": set(res["coverageIds"]),
                                        "scopes": set(res["scopeIds"]), "refs": EI,
                                        "blocking": [d for d in defs if is_blocking(d, rule)] if value == "indeterminate" else []}
                            rdefs += defs
                        else:
                            chs = children_addrs(node, addr)
                            value = kleene(op, [results[c]["value"] for c in chs])
                            defs = cset([d for c in chs for d in results[c]["defs"]])
                            witness = {"schemaVersion": 3, "programPredicateDigest": ppd_digest, "matchingFactIds": [], "coverageIds": [],
                                       "countLimit": None, "childPredicateIds": sorted(chs, key=ckey), "matchingImportRows": [],
                                       "uncertainFactIds": [], "uncertainImportRows": [], "deficiencies": defs, "kind": "boolean"}
                            node_res = {"value": value, "defs": defs,
                                        "facts": set().union(*[results[c]["facts"] for c in chs]),
                                        "ufacts": set().union(*[results[c]["ufacts"] for c in chs]),
                                        "rows": cset([r for c in chs for r in results[c]["rows"]]),
                                        "urows": cset([r for c in chs for r in results[c]["urows"]]),
                                        "coverage": set().union(*[results[c]["coverage"] for c in chs]),
                                        "scopes": set().union(*[results[c]["scopes"] for c in chs]),
                                        "refs": cset([r for c in chs for r in results[c]["refs"]]),
                                        "blocking": [d for c in chs if results[c]["value"] == "indeterminate" for d in results[c]["blocking"]]
                                        if value == "indeterminate" else []}
                        wd = K.raw_digest(witness)
                        blobs[wd] = K.C(witness)
                        node_res["witnessDigest"] = wd
                        results[addr] = node_res
                        predicate_proofs.append({"ruleId": rule["ruleId"], "subjectId": sid, "predicateId": addr, "operation": op,
                                                 "inputRefs": node_res["refs"], "scopeIds": sorted(node_res["scopes"], key=ckey),
                                                 "value": value, "witnessDigest": wd})
                    root = results["p"]
                    if root["value"] == "indeterminate" and root["blocking"]:
                        blocked_root = True
                    if root["value"] == "true":
                        f, corr = mint_finding(inp, rule, bindings[rule["ruleId"]], subject, sid, root, EI, enum, population, blobs, objects)
                        rdefs += corr
                        rfindings.append(f)
        findings += rfindings
        rwaived = [f["findingId"] for f in rfindings if waiver_matches(inp.waivers, f)]
        waived += rwaived
        gating = rule["enabled"] and rule["gate"] and SEV[rule["severity"]] >= SEV[policy["gateSeverityAtLeast"]]
        if not rule["enabled"]:
            outcome = "disabled"
        elif gating and any(f["findingId"] not in rwaived for f in rfindings):
            outcome = "fail"
        elif gating and (enum["state"] == "incomplete" or enum["unresolvedSubjectIds"] or blocked_root or exhausted or required_import_missing):
            outcome = "indeterminate"
        else:
            outcome = "pass"
        rule_results.append({"ruleId": rule["ruleId"], "enumeration": enum, "outcome": outcome,
                             "findingIds": sorted({f["findingId"] for f in rfindings}, key=ckey),
                             "deficiencies": cset(rdefs) if rule["enabled"] else []})
    predicate_proofs.sort(key=lambda p: (p["ruleId"].encode(), p["subjectId"].encode(), p["predicateId"].encode()))
    finding_ids = sorted({f["findingId"] for f in findings}, key=ckey)
    if any(r["outcome"] == "fail" for r in rule_results):
        verdict = "fail"
    elif any(r["outcome"] == "indeterminate" for r in rule_results) or exec_defs:
        verdict = "indeterminate"
    else:
        verdict = "pass"
    proof = {"schemaVersion": 3, "planId": inp.plan_id, "executionPlanId": inp.exec_plan_id, "evaluatorClosure": inp.evaluator_closure,
             "ruleProgramDigest": program_digest, "evaluationInputRefs": EI, "predicateProofs": predicate_proofs,
             "findingIds": finding_ids, "verdict": verdict, "evaluationState": "budget-exhausted" if exhausted else "evaluated",
             "ruleResults": rule_results, "waivedFindingIds": sorted(set(waived), key=ckey),
             "executionDeficiencies": exec_defs, "executionInputsDigest": inp.exec_inputs_digest}
    proof_id = K.identifier("proof-bundle", proof)
    objects[proof_id] = ("proof-bundle", proof)
    view_ids = sel_views
    cov_ids = {c for v in view_ids for c in inp.views[v]["coverageIds"]} | {"coverage2:" + r["digest"] for r in EI if r["domain"] == "coverage"}
    evidence = {"schemaVersion": 3, "planId": inp.plan_id, "viewIds": view_ids, "coverageIds": sorted(cov_ids, key=ckey),
                "importIds": sorted(inp.plan["importIds"], key=ckey), "findingIds": finding_ids, "proofBundleId": proof_id}
    evidence_id = K.identifier("semantic-evidence", evidence)
    objects[evidence_id] = ("semantic-evidence", evidence)
    seal = {"schemaVersion": 3, "planId": inp.plan_id, "executionPlanId": inp.exec_plan_id, "evidenceId": evidence_id,
            "evaluatorClosure": inp.evaluator_closure, "policyDigest": inp.plan["policyDigest"], "proofBundleId": proof_id, "verdict": verdict}
    seal_id = K.identifier("evaluation-seal", seal)
    objects[seal_id] = ("evaluation-seal", seal)
    run = {"schemaVersion": 3, "projectId": inp.project_id, "snapshotId": inp.plan["snapshotId"], "planId": inp.plan_id,
           "evidenceId": evidence_id, "evaluationSealId": seal_id, "capabilityManifestId": inp.plan["capabilityManifestId"]}
    run_id = K.identifier("run", run)
    objects[run_id] = ("run", run)
    pd = {"schemaVersion": 3, "planId": inp.plan_id, "proofBundleId": proof_id, "policyDigest": inp.plan["policyDigest"],
          "waiverDigest": inp.plan["waiverDigest"], "verdict": verdict}
    pd_id = K.identifier("policy-derivation", pd)
    objects[pd_id] = ("policy-derivation", pd)
    return {"proof": proof, "proofId": proof_id, "evidenceId": evidence_id, "sealId": seal_id, "runId": run_id,
            "policyDerivationId": pd_id, "findings": findings, "budget": {"charge": charge, **charge_detail},
            "blobs": blobs, "objects": objects}


def mint_finding(inp, rule, binding, subject, sid, root, EI, enum, population, blobs, objects):
    row, rec = subject["row"], subject["record"]
    kind = row["kind"]
    defs, reasons = [], []
    disc = EMPTY_DISCRIMINATOR
    if kind == "symbol":
        proj = next((p for p in row["projections"] if p["closureId"] == binding["detectorClosure"]), None)
        tokens = proj["signatureTokens"] if proj else []
        if not tokens:
            reasons.append("projection-unavailable")
        if enum["incompleteInventoryRefs"]:
            reasons.append("population-incomplete")
        if tokens:
            klass = (rec["universe"], row["subjectLanguage"], kind, row["path"], row["qualifiedName"])
            for uni, other in population:
                if (uni, other["subjectLanguage"], other["kind"], other["path"], other["qualifiedName"]) != klass or \
                        other["nativeSubjectId"] == row["nativeSubjectId"]:
                    continue
                op = next((p for p in other["projections"] if p["closureId"] == binding["detectorClosure"]), None)
                if op is not None and op["signatureTokens"] == tokens:
                    reasons.append("signature-ambiguous")
                    break
            disc = hashlib.sha256(K.C(tokens)).hexdigest()
        for reason in reasons:
            defs.append({"source": "correspondence", "cause": reason, "subjectId": sid, "predicateId": "p",
                         "inputRefs": enum["inventoryRefs"], "evidenceKind": None, "nativeCause": None, "universe": None})
    fingerprint = None
    if not reasons:
        desc = {"schemaVersion": 2, "ruleStableId": binding["ruleStableId"], "detectorSemanticsMajor": binding["semanticsMajor"],
                "subjectKey": {"language": row["subjectLanguage"], "kind": kind, "logicalPath": row["path"],
                               "qualifiedName": row["qualifiedName"], "discriminator": disc},
                "relatedSubjectKeys": []}
        fingerprint = K.identifier("finding-fingerprint", desc)
        objects[fingerprint] = ("finding-fingerprint", desc)
    message = rule.get("messageCode", rule["ruleId"])
    params = {"schemaVersion": 2, "messageCode": message,
              "parameters": {"ruleId": rule["ruleId"], "subjectPath": row["path"], "qualifiedName": row["qualifiedName"],
                             "subjectKind": kind, "subjectLanguage": row["subjectLanguage"],
                             "matchingFactCount": len(root["facts"]), "matchingImportCount": len(root["rows"])}}
    pdig = K.raw_digest(params)
    blobs[pdig] = K.C(params)
    refs = [{"domain": "predicate-witness", "digest": root["witnessDigest"]}]
    refs += [{"domain": "fact", "digest": sfx(f)} for f in root["facts"] | root["ufacts"]]
    refs += [{"domain": "coverage", "digest": sfx(c)} for c in root["coverage"]]
    refs += [{"domain": "import", "digest": sfx(r["importId"])} for r in root["rows"] + root["urows"]]
    refs += [{"domain": "import", "digest": r["digest"]} for r in EI if r["domain"] == "import"]
    finding = {"schemaVersion": 3, "fingerprint": fingerprint,
               "correspondence": {"state": "matched" if fingerprint else "unmatched", "reason": None if fingerprint else reasons[0]},
               "ruleClosure": binding["detectorClosure"], "ruleId": rule["ruleId"], "subjectId": sid,
               "subject": {"language": row["subjectLanguage"], "kind": kind, "logicalPath": row["path"], "qualifiedName": row["qualifiedName"]},
               "messageCode": message, "parameterDigest": pdig, "severity": rule["severity"], "evidenceRefs": cset(refs)}
    fid = K.identifier("finding", finding)
    objects[fid] = ("finding", finding)
    objects[sid] = ("evaluation-subject", rec)
    return {"findingId": fid, "finding": finding, "subjectPath": row["path"]}, defs


def waiver_matches(waivers, f):
    for w in waivers["waivers"]:
        t = w["target"]
        if "fingerprint" in t:
            if f["finding"]["fingerprint"] is not None and t["fingerprint"] == f["finding"]["fingerprint"]:
                return True
        elif t.get("ruleId") == f["finding"]["ruleId"] and t.get("subjectPath") == f["subjectPath"]:
            return True
    return False
