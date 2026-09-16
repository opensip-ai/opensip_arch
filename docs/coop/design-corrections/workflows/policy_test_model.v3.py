"""Evaluator3 policy.test fixture evaluator for PolicyTestSuiteV2 (reference evidence, not a host runtime).

Owner of the bounded deterministic authoring-test semantics of schemas/evaluator3/policy-test.schema.json
x-opensip-fixture-representation. Atom law comes from the current atom owner (foundation/atom_model.v1.py: its registry,
ladder comparison, filter comparators and three-valued match combination); this module adds no relation table. The facts
fixture is a finite FactRecordCandidate view, so a field or imported observation it cannot represent is unknown, never a
fabricated no-match. It raises no refusal: workflows_model.v3 admits the suite, resolves the policy and owns every
Refusal. Not production evaluator, provider, full Run or native qualification.
"""
import copy
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


A = _load("policy_test_atom_owner3", HERE.parent / "foundation" / "atom_model.v1.py")
REGISTRY = A.REGISTRY
W = A.W  # the atom owner's glob_match / in_scope / SEV_ORDER helpers
SUITE_SCHEMA = json.loads((HERE / "schemas" / "evaluator3" / "policy-test.schema.json").read_text())
REPRESENTATION = SUITE_SCHEMA["x-opensip-fixture-representation"]
FIELDS = REPRESENTATION["fields"]
SELECTORS = REPRESENTATION["importedObservationSelectors"]
_V2 = json.loads((HERE / "schemas" / "policy-document.v2.schema.json").read_text())["$defs"]
_CASES = json.loads((HERE / "schemas" / "policy-test.schema.json").read_text())["$defs"]
SEVERITIES = tuple(_V2["Severity"]["enum"])
# The closed policy universe token map of the evaluator profile (composition contract section 2: unknown tokens refuse
# admission; historical illustrative tokens such as typescript-v2 are not implicit aliases).
POLICY_UNIVERSES = json.loads((HERE.parent / "foundation" / "identity-schemas.v3.json").read_text())["x-opensip-evaluator-profile"]["policyUniverseMap"]
NUMERIC_FIELDS = frozenset(REGISTRY["fieldFilterSuccessor"]["numericFields"])
_fact_members = set(_CASES["FactRecordCandidate"]["properties"])
_registry_selectors = {row["observationAddressSelector"] for row in REGISTRY["relations"].values() if row.get("observationAddressSelector")}
if set(FIELDS) != set(_V2["FieldFilter"]["properties"]["field"]["enum"]) or not {m for m in FIELDS.values() if m} <= _fact_members:
    raise RuntimeError("fixture field representation drifted from PolicyDocumentV2 FieldFilter or FactRecordCandidate")
if set(SELECTORS) != _registry_selectors:
    raise RuntimeError("fixture imported-observation representation drifted from the atom registry selectors")
OVERRIDE_TYPES = {"enabled": "boolean", "gate": "boolean", "severity": "severity"}


def _kind(kind):
    """export is not a stored kind (registry exportLaw): it evaluates as symbol."""
    return "symbol" if kind == "export" else kind


def suite_faults(suite):
    """Fixture and override faults of a schema-admitted suite, in suite order. Empty means admissible."""
    faults = []
    rules = {r["ruleId"] for r in suite["candidatePolicy"]["rules"]}
    for i, o in enumerate(suite.get("overrides", [])):
        if o["ruleId"] not in rules:
            faults.append("overrides[%d] names rule %s, which is not a candidate rule" % (i, o["ruleId"]))
        elif OVERRIDE_TYPES[o["field"]] == "boolean" and type(o["value"]) is not bool or OVERRIDE_TYPES[o["field"]] == "severity" and o["value"] not in SEVERITIES:
            faults.append("overrides[%d] value does not have the type of field %s" % (i, o["field"]))
    for case in suite["cases"]:
        if case["subject"]["kind"] != "facts":
            continue
        for j, fact in enumerate(case["subject"]["facts"]):
            row = REGISTRY["relations"].get(fact["relation"])
            if row is None:
                faults.append("case %s fact %d names unregistered relation %s" % (case["id"], j, fact["relation"]))
            elif fact["resolution"] not in row["ladder"]:
                faults.append("case %s fact %d resolution %s is not a rung of %s" % (case["id"], j, fact["resolution"], fact["relation"]))
            if fact["universe"] not in POLICY_UNIVERSES:
                faults.append("case %s fact %d universe %s is not a registered policy universe token" % (case["id"], j, fact["universe"]))
    return faults


def unregistered_universes(policy):
    """(ruleId, token) of every candidate rule, enabled or not, whose subjectEnumeration.universe is not a token of the closed
    evaluator profile policy universe map; the evaluator input admission applies the same law to every rule."""
    return [(r["ruleId"], r["subjectEnumeration"]["universe"]) for r in policy["rules"] if r["subjectEnumeration"]["universe"] not in POLICY_UNIVERSES]


def apply_overrides(policy, overrides):
    """The effective policy: test-only field overrides of admitted candidate rules, in rule-ID order; never written."""
    effective = copy.deepcopy(policy)
    rules = {r["ruleId"]: r for r in effective["rules"]}
    for o in overrides:
        rules[o["ruleId"]][o["field"]] = o["value"]
    effective["rules"] = [rules[k] for k in sorted(rules, key=lambda s: s.encode())]
    return effective


# ------------------------------------------------------------------------------------------------- atoms
def _projection(fact, field, plane, kind):
    if plane == "imported" and field == "subjectKind":
        return kind
    if plane == "imported" and field == "resolution":
        return "observed"
    member = FIELDS[field]
    if member is None or fact.get(member) is None:
        return A.ABSENT
    value = fact[member]
    return _kind(value) if field in ("subjectKind", "targetKind") else value


def _filters(fact, atom, plane, kind):
    acc = A.MATCH
    for flt in atom.get("filters") or []:
        projected = _projection(fact, flt["field"], plane, kind)
        if projected is A.ABSENT:
            acc = A._and_fr(acc, A.FUNK)
            continue
        compare = A._cmp_int if flt["field"] in NUMERIC_FIELDS else A._cmp_string
        acc = A._and_fr(acc, compare(flt["cmp"], projected, flt["value"]))
        if acc == A.NOMATCH:
            break
    return acc


def _native_occupancy(fact, atom, spec, subject, kind, universe):
    if fact["universe"] != universe:
        return A.NOMATCH
    if atom.get("endpoint", "source") == "source":
        return A.MATCH if fact["subject"] == subject else A.NOMATCH
    if not spec.get("targetNativeIdField") or fact["target"] != subject:
        return A.NOMATCH
    target_kind = fact.get("targetKind")
    if target_kind is None:
        return A.FUNK
    return A.MATCH if _kind(target_kind) == kind else A.NOMATCH  # another first-party kind or external


def _imported_occupancy(fact, subject, universe):
    """A representable imported fixture row occupies the evaluated subject only in that subject's universe (factUniverse): a row
    of another registered universe is neither a known nor an uncertain observation of this subject."""
    return fact["subject"] == subject and fact["universe"] == universe


def _atom(atom, subject, kind, universe, fixture):
    """(value, causes): value True / False / None under strong Kleene; causes name why a None arose."""
    rel = atom["relation"]
    spec = REGISTRY["relations"][rel]
    evidence = atom.get("evidence")
    if evidence is not None and evidence not in fixture["evidenceAvailable"]:
        return None, {("evidence-absent", evidence)}
    facts = [f for f in fixture["facts"] if f["relation"] == rel and A._rung_ge(rel, f["resolution"], atom["minResolution"])]
    known, uncertain = set(), set()
    op, n = atom["op"], atom.get("n")
    if spec["plane"] == "native":
        for fact in facts:
            occupancy = _native_occupancy(fact, atom, spec, subject, kind, universe)
            if occupancy == A.NOMATCH:
                continue
            status = A._and_fr(occupancy, _filters(fact, atom, "native", kind))
            key = json.dumps(fact, sort_keys=True)
            if status == A.MATCH:
                known.add(key)
            elif status == A.FUNK:
                uncertain.add(key)
        decided = fixture["coverage"] == "complete" and not uncertain
        cause = {("uncertain-match",)} if uncertain else {("coverage",)}
        if op == "exists":
            value = True if known else (False if decided else None)
        elif op == "none":
            value = False if known else (True if decided else None)
        elif op == "count-at-most":
            value = False if len(known) > n else (True if decided else None)
        else:
            value = True if decided else None
        return value, (set() if value is not None else cause)
    if SELECTORS[spec["observationAddressSelector"]] != "representable":
        return None, {("unrepresentable", spec["observationAddressSelector"])}
    for fact in facts:
        if not _imported_occupancy(fact, subject, universe):
            continue
        key = json.dumps(fact, sort_keys=True)
        if spec["observationAddressSelector"] == "runtime-subject" and fact.get("observability") not in ("observed-hit", "observable-unhit"):
            uncertain.add(key)
            continue
        status = _filters(fact, atom, "imported", kind)
        if status == A.MATCH:
            known.add(key)
        elif status == A.FUNK:
            uncertain.add(key)
    if op == "exists" and known:
        return True, set()
    if op == "none" and known:
        return False, set()
    if op == "count-at-most" and len(known) > n:
        return False, set()
    return None, {("import-completeness-unrepresentable", spec["evidenceKind"])}


def _predicate(node, subject, kind, universe, fixture):
    if node["op"] in ("and", "or"):
        results = [_predicate(child, subject, kind, universe, fixture) for child in node["operands"]]
        dominant = False if node["op"] == "and" else True
        if any(v is dominant for v, _ in results):
            return dominant, set()
        if all(v is (not dominant) for v, _ in results):
            return (not dominant), set()
        return None, set().union(*(c for v, c in results if v is None))
    if node["op"] == "not":
        value, causes = _predicate(node["operand"], subject, kind, universe, fixture)
        return (None if value is None else not value), causes
    return _atom(node, subject, kind, universe, fixture)


# ------------------------------------------------------------------------------------------------- rules and cases
def evaluate(policy, scope, effective_waivers, fixture):
    """-> verdict, findings, indeterminateRules, optionalEvidenceAbsent and unknownSubjects (rule -> subjects)."""
    waived = set()
    for waiver in effective_waivers["waivers"]:
        target = waiver["target"]
        if "ruleId" in target:
            waived.add((target["ruleId"], target["subjectPath"]))
    available = set(fixture["evidenceAvailable"])
    findings, indeterminate, optional_absent, unknown = [], [], [], {}
    fail = gating_unknown = False
    for rule in sorted(policy["rules"], key=lambda r: r["ruleId"].encode()):
        if not rule["enabled"]:
            continue
        rid = rule["ruleId"]
        required = {u["kind"] for u in rule["evidenceUse"] if u["requirement"] == "required"}
        optional = {u["kind"] for u in rule["evidenceUse"] if u["requirement"] == "optional"}
        gating = rule["gate"] and W.SEV_ORDER[rule["severity"]] >= W.SEV_ORDER[policy["gateSeverityAtLeast"]]
        enum = rule["subjectEnumeration"]
        subjects = [s for s in fixture["subjects"] if W.in_scope(scope, s)
                    and (not enum.get("include") or any(W.glob_match(g, s) for g in enum["include"]))
                    and not any(W.glob_match(g, s) for g in enum.get("exclude", []))]
        # Composition contract sections 5 and 9.5: every selected subject is evaluated whatever the evidence. A declared REQUIRED
        # kind absent from evidenceAvailable is a rule-level deficiency independent of the root value: it never suppresses a
        # known finding, and a live unwaived gating finding still makes the verdict fail.
        required_absent = required - available
        kind, universe = _kind(enum["subjectKind"]), enum["universe"]
        absent_optional = {("evidence-absent", k) for k in optional - available}
        rule_unknown, blocking = set(), bool(required_absent)
        for subject in subjects:
            value, causes = _predicate(rule["emitWhen"], subject, kind, universe, fixture)
            if value is True:
                is_waived = (rid, subject) in waived
                findings.append({"ruleId": rid, "subject": subject, "waived": is_waived})
                fail = fail or (gating and not is_waived)
            elif value is None:
                rule_unknown.add(subject)
                # An unknown root blocks unless its only causes are absent OPTIONAL evidence; an incomplete-Coverage or
                # uncertain native match, a required kind or a fixture representation limit is itself a blocking cause.
                blocking = blocking or not causes <= absent_optional
            elif required_absent:
                rule_unknown.add(subject)  # a known false root is not an authoritative no-match while required evidence is absent
        if blocking:
            indeterminate.append(rid)
            unknown[rid] = rule_unknown
            gating_unknown = gating_unknown or gating
        elif rule_unknown:
            optional_absent.append(rid)
    verdict = "fail" if fail else "indeterminate" if gating_unknown else "advisory" if any(not f["waived"] for f in findings) else "pass"
    return {"verdict": verdict, "findings": findings, "indeterminateRules": sorted(set(indeterminate), key=lambda s: s.encode()),
            "optionalEvidenceAbsent": sorted(set(optional_absent), key=lambda s: s.encode()), "unknownSubjects": unknown}


def _expectation(expectation, ev):
    rid = expectation["ruleId"] if "ruleId" in expectation else None
    if expectation["kind"] == "verdict":
        return "met" if ev["verdict"] == expectation["verdict"] else "unmet"
    if expectation["kind"] == "indeterminate":
        return "met" if rid in ev["indeterminateRules"] else "unmet"
    unknown = ev["unknownSubjects"].get(rid, set())
    if expectation["kind"] == "no-finding":
        if any(f["ruleId"] == rid for f in ev["findings"]):
            return "unmet"
        return "indeterminate" if unknown else "met"
    wanted = expectation.get("subjects")
    matched = [f for f in ev["findings"] if f["ruleId"] == rid and (not wanted or f["subject"] in wanted)]
    open_subjects = unknown if not wanted else unknown & set(wanted)
    if "maxCount" in expectation and len(matched) > expectation["maxCount"]:
        return "unmet"
    if len(matched) >= expectation["minCount"]:
        return "indeterminate" if "maxCount" in expectation and open_subjects else "met"
    return "indeterminate" if open_subjects else "unmet"


def case_result(policy, scope, effective_waivers, case):
    """One CaseResult of PolicyTestResultV1 (unchanged shape)."""
    if case["subject"]["kind"] == "sources":
        return {"id": case["id"], "outcome": "not-executable", "observedVerdict": "indeterminate", "findings": [], "indeterminateRules": [],
                "expectationOutcomes": ["indeterminate"] * len(case["expectations"])}
    ev = evaluate(policy, scope, effective_waivers, case["subject"])
    outcomes = [_expectation(x, ev) for x in case["expectations"]]
    outcome = "failed" if "unmet" in outcomes else "indeterminate" if "indeterminate" in outcomes else "passed"
    return {"id": case["id"], "outcome": outcome, "observedVerdict": ev["verdict"], "findings": ev["findings"],
            "indeterminateRules": ev["indeterminateRules"], "expectationOutcomes": outcomes}
