"""Independent implementation of the published pure evaluator.

Sources: identity-and-evidence.md S4 (predicate table, witness record, node
addressing, verdict dominance), workflows-and-surfaces.md S5 (DSL shape and
strong-Kleene statement), relation-payload-schemas.v2 x-opensip-relation-registry
(ladders, membership rule, order comparison within one relation).

DOCUMENTED ASSUMPTIONS (see blind-review.md CB9-MUST-1 / CB9-MUST-2):
  * `Rule.subjectEnumeration.universe` is a CanonicalIdentifier while every
    fact and scope carries a 64-hex universe h-identity.  No document publishes
    the join.  This module binds it to the universe DOMAIN ROW's `language`
    value, which is the only CanonicalIdentifier-shaped universe name in the
    kit, and records the choice as an assumption.
  * `Rule.subjectEnumeration.subjectKind` (file|symbol|export|package) is bound
    to the relation registry `subjectKind` (source-path|package-name|symbol) by
    file->source-path, package->package-name, symbol/export->symbol.  Also an
    assumption; no document maps the two vocabularies.
  * FieldFilter is NOT implemented: no document projects `fact2` + relation
    payload onto {subject,target,subjectKind,targetKind,observability}.  An atom
    carrying a non-empty `filters` array raises FILTER_PROJECTION_UNPUBLISHED
    rather than being given invented semantics.
"""
from __future__ import annotations

import hashlib
import re

import canon as K
import kit
from store import Refusal

TRUE, FALSE, IND = "true", "false", "indeterminate"

SUBJECT_KIND_BINDING = {          # ASSUMPTION, see module docstring
    "file": "source-path",
    "package": "package-name",
    "symbol": "symbol",
    "export": "symbol",
}


class FilterProjectionUnpublished(Refusal):
    def __init__(self, field):
        super().__init__("FILTER_PROJECTION_UNPUBLISHED", field)


# ---------------------------------------------------------------------------
# node addressing (identity S3 `program-predicate`)
# ---------------------------------------------------------------------------

def address_nodes(root):
    """Yield (address, node) for every node of one rule's emitWhen tree.

    "the rule's emitWhen root has address `p`; the i-th operand of an and/or
    node at address a has address a.i with i zero-based in shortest decimal
    without a leading zero; the single operand of a not node at a has a.0"
    """
    out = []

    def walk(node, addr):
        out.append((addr, node))
        op = node["op"]
        if op in ("and", "or"):
            for i, child in enumerate(node["operands"]):
                walk(child, f"{addr}.{i}")
        elif op == "not":
            walk(node["operand"], f"{addr}.0")

    walk(root, "p")
    return out


def child_addresses(addr, node):
    op = node["op"]
    if op in ("and", "or"):
        return [f"{addr}.{i}" for i in range(len(node["operands"]))]
    if op == "not":
        return [f"{addr}.0"]
    return []


def node_digest(node) -> str:
    return hashlib.sha256(K.C(node)).hexdigest()


def program_predicate(rule_program_digest, rule_id, predicate_id, operation, node):
    return {"schemaVersion": 2, "ruleProgramDigest": rule_program_digest,
            "ruleId": rule_id, "predicateId": predicate_id,
            "operation": operation, "nodeDigest": node_digest(node)}


# ---------------------------------------------------------------------------
# glob (workflows S5: only `*`, `?` and whole-segment `**`)
# ---------------------------------------------------------------------------

def glob_match(pattern: str, path: str) -> bool:
    segs = pattern.split("/")
    rx = []
    for s in segs:
        if s == "**":
            rx.append("(?:[^/]+/)*[^/]+")
        else:
            part = ""
            for ch in s:
                if ch == "*":
                    part += "[^/]*"
                elif ch == "?":
                    part += "[^/]"
                else:
                    part += re.escape(ch)
            rx.append(part)
    return re.fullmatch("/".join(rx), path) is not None


# ---------------------------------------------------------------------------
# the evaluation input view
# ---------------------------------------------------------------------------

class EvalView:
    """The Plan-bound, schema-admitted finite fact view the evaluator consumes."""

    def __init__(self, facts, scopes, coverages, universe_language, imports=None):
        # facts: {factId: descriptor}; scopes: {scopeId: descriptor}
        # coverages: {coverageId: {"scopeId":..., "payload": CoverageResultV3}}
        self.facts = facts
        self.scopes = scopes
        self.coverages = coverages
        self.universe_language = universe_language   # {universeHex: "typescript"}
        self.imports = imports or {}

    def ladder(self, relation):
        row = kit.RELATIONS.get(relation)
        if row is None:
            raise Refusal("RELATION_UNREGISTERED", relation)
        ladder = row.get("ladder")
        if not ladder:
            # "Membership is decided against `ladder`, always, with no
            #  empty-ladder fallback"
            raise Refusal("RELATION_LADDER_MISSING", relation)
        return ladder

    def rung_index(self, relation, rung):
        ladder = self.ladder(relation)
        if rung not in ladder:
            raise Refusal("RUNG_NOT_IN_RELATION_LADDER", f"{relation}@{rung}")
        return ladder.index(rung)

    def matching_facts(self, relation, min_resolution, filters):
        """Facts of this view selected by the atom, as sorted fact ids."""
        if filters:
            raise FilterProjectionUnpublished(filters[0]["field"])
        want = self.rung_index(relation, min_resolution)
        out = []
        for fid, f in self.facts.items():
            if f["relation"] != relation:
                continue
            if self.rung_index(relation, f["resolution"]) >= want:
                out.append(fid)
        return sorted(out)

    def coverage_for(self, relation, min_resolution):
        """Coverage entries of this view whose (relation, rung) is the atom's."""
        out = []
        for cid, c in self.coverages.items():
            entry = c["payload"]["entry"]
            if entry["relation"] != relation:
                continue
            if self.rung_index(relation, entry["resolution"]) < \
               self.rung_index(relation, min_resolution):
                continue
            out.append(cid)
        return sorted(out)

    def examination_complete(self, coverage_ids) -> bool:
        """claim 1: `coverage: complete` over the examined partition."""
        if not coverage_ids:
            return False
        return all(self.coverages[c]["payload"]["entry"]["coverage"] == "complete"
                   for c in coverage_ids)

    def resolution_complete(self, coverage_ids) -> bool:
        """claim 2: resolution completeness (native S4.1/S4.3)."""
        if not coverage_ids:
            return False
        return all(
            self.coverages[c]["payload"]["entry"]["resolutionCompleteness"]["state"]
            == "complete" for c in coverage_ids)


# ---------------------------------------------------------------------------
# atoms and the three-valued algebra (identity S4 table)
# ---------------------------------------------------------------------------

def eval_atom(view: EvalView, atom):
    relation = atom["relation"]
    min_res = atom["minResolution"]
    # "Membership of THIS atom's relation's ladder is sufficient and is enforced
    #  at admission" -- refuse a rung of another relation.
    view.rung_index(relation, min_res)
    matches = view.matching_facts(relation, min_res, atom["filters"])
    cov = view.coverage_for(relation, min_res)
    complete = view.examination_complete(cov)
    op = atom["op"]

    if op == "exists":
        # "true on a matching fact; false only on complete absence"
        if matches:
            value = TRUE
        elif complete:
            value = FALSE
        else:
            value = IND
    elif op == "none":
        # "false on a known match; true only on complete absence"
        if matches:
            value = FALSE
        elif complete:
            value = TRUE
        else:
            value = IND
    elif op == "count-at-most":
        n = atom["n"]
        if len(matches) > n:
            value = FALSE               # "false once more than N distinct matches exist"
        elif complete:
            value = TRUE                # "true when complete count <= N"
        else:
            value = IND
    elif op == "all-covered":
        # "true only with admitted resolution-complete coverage for the
        #  requested universe/rung"; otherwise indeterminate.
        value = TRUE if (cov and view.resolution_complete(cov)) else IND
    else:
        raise Refusal("ATOM_OP_UNREGISTERED", op)
    return value, matches, cov


def kleene_and(values):
    if FALSE in values:
        return FALSE           # "false dominates and"
    if IND in values:
        return IND
    return TRUE


def kleene_or(values):
    if TRUE in values:
        return TRUE            # "true dominates or"
    if IND in values:
        return IND
    return FALSE


def kleene_not(v):
    return {TRUE: FALSE, FALSE: TRUE, IND: IND}[v]


# ---------------------------------------------------------------------------
# subject enumeration (documented assumption)
# ---------------------------------------------------------------------------

def enumerate_subjects(view: EvalView, rule):
    se = rule["subjectEnumeration"]
    want_lang = se["universe"]
    want_kind = SUBJECT_KIND_BINDING.get(se["subjectKind"])
    if want_kind is None:
        raise Refusal("SUBJECT_KIND_UNREGISTERED", se["subjectKind"])
    subjects = set()
    for scope in view.scopes.values():
        row = kit.RELATIONS.get(scope["relation"])
        if row is None or row["subjectKind"] != want_kind:
            continue
        if view.universe_language.get(scope["sourceUniverse"]) != want_lang:
            continue
        subjects.update(scope["subjects"])
    out = sorted(subjects)
    inc, exc = se.get("include"), se.get("exclude")
    if inc:
        out = [s for s in out if any(glob_match(p, s) for p in inc)]
    if exc:
        out = [s for s in out if not any(glob_match(p, s) for p in exc)]
    return out


# ---------------------------------------------------------------------------
# the replay
# ---------------------------------------------------------------------------

def replay(policy, rule_program, rule_program_digest, view: EvalView,
           waivers=None, evaluation_input_refs=None):
    """Run the published evaluator.  Returns the complete recomputed bundle."""
    waivers = waivers or {"schemaFamily": "opensip.product.waivers",
                          "schemaMajor": 1, "waivers": []}
    rules_by_id = {r["ruleId"]: r for r in policy["rules"]}
    program_by_id = {r["ruleId"]: r for r in rule_program["rules"]}
    if set(rules_by_id) != set(program_by_id):
        raise Refusal("RULE_PROGRAM_NOT_POLICY_PROJECTION", "ruleId set differs")

    predicate_proofs = []
    witnesses = {}                   # witnessDigest -> witness record
    program_predicates = {}          # digest -> program-predicate record
    findings = []
    rule_outcomes = {}

    for rule_id in sorted(rules_by_id, key=lambda s: s.encode("utf-8")):
        rule = rules_by_id[rule_id]
        prog = program_by_id[rule_id]
        if prog["emitWhen"] != rule["emitWhen"]:
            raise Refusal("RULE_PROGRAM_NOT_POLICY_PROJECTION", rule_id)
        subjects = enumerate_subjects(view, rule)
        outcome = {"subjects": subjects, "emitted": [], "indeterminate": []}
        addressed = address_nodes(prog["emitWhen"])
        by_addr = dict(addressed)
        for subject in subjects:
            values = {}
            # evaluate bottom-up: longest addresses first
            for addr, node in sorted(addressed, key=lambda t: (-len(t[0]), t[0])):
                op = node["op"]
                if op in ("and", "or", "not"):
                    kids = child_addresses(addr, node)
                    kid_vals = [values[k] for k in kids]
                    value = (kleene_and(kid_vals) if op == "and" else
                             kleene_or(kid_vals) if op == "or" else
                             kleene_not(kid_vals[0]))
                    matches, cov, limit = [], [], None
                else:
                    value, matches, cov = eval_atom(view, node)
                    kids = []
                    limit = node["n"] if op == "count-at-most" else None
                values[addr] = value

                pp = program_predicate(rule_program_digest, rule_id, addr, op, node)
                ppd = hashlib.sha256(K.C(pp)).hexdigest()
                program_predicates[ppd] = pp
                witness = {"schemaVersion": 2, "programPredicateDigest": ppd,
                           "matchingFactIds": sorted(matches),
                           "coverageIds": sorted(cov),
                           "countLimit": limit,
                           "childPredicateIds": sorted(kids)}
                wd = hashlib.sha256(K.C(witness)).hexdigest()
                witnesses[wd] = witness
                scope_ids = sorted({view.coverages[c]["scopeId"] for c in cov})
                predicate_proofs.append({
                    "ruleId": rule_id, "subjectId": subject, "predicateId": addr,
                    "operation": op,
                    "inputRefs": _input_refs(view, matches, cov),
                    "scopeIds": scope_ids,
                    "value": value, "witnessDigest": wd})
            root = values["p"]
            if root == TRUE:
                outcome["emitted"].append(subject)
            elif root == IND:
                outcome["indeterminate"].append(subject)
        rule_outcomes[rule_id] = outcome
        for subject in outcome["emitted"]:
            findings.append({"ruleId": rule_id, "subject": subject})

    verdict = compute_verdict(policy, rule_outcomes, waivers)
    predicate_proofs.sort(key=lambda p: (p["ruleId"].encode("utf-8"),
                                         p["subjectId"].encode("utf-8"),
                                         p["predicateId"].encode("utf-8")))
    return {"predicateProofs": predicate_proofs, "witnesses": witnesses,
            "programPredicates": program_predicates, "findings": findings,
            "ruleOutcomes": rule_outcomes, "verdict": verdict}


def _input_refs(view, matches, cov):
    refs = [{"domain": "coverage", "digest": c.split(":", 1)[1]} for c in cov]
    return sorted(refs, key=K.C)


SEVERITY_ORDER = {"note": 0, "warning": 1, "error": 2}


def compute_verdict(policy, rule_outcomes, waivers):
    """"Aggregate policy fail dominates indeterminate, which dominates pass.\""""
    threshold = SEVERITY_ORDER[policy["gateSeverityAtLeast"]]
    waived_targets = {(w["target"].get("ruleId"), w["target"].get("subjectPath"))
                      for w in waivers["waivers"] if "ruleId" in w["target"]}
    fail = False
    indeterminate = False
    for rule in policy["rules"]:
        if not rule["enabled"]:
            continue
        gating = rule["gate"] and SEVERITY_ORDER[rule["severity"]] >= threshold
        out = rule_outcomes[rule["ruleId"]]
        if gating:
            for subject in out["emitted"]:
                if (rule["ruleId"], subject) not in waived_targets:
                    fail = True
            if out["indeterminate"]:
                indeterminate = True
    if fail:
        return "fail"
    if indeterminate:
        return "indeterminate"
    return "pass"
