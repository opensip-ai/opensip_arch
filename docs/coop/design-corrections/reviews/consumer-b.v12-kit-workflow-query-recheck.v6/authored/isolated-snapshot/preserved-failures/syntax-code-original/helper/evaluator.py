"""Independent evaluator3 reconstruction: enumeration + Kleene atoms + composition.

Implements identity-and-evidence §4 / composition-contract.v3 over retained inputs.
Does not read claimed findings/verdicts as truth.
"""
from __future__ import annotations

import hashlib
from typing import Any

from helper.canonical import C
from helper.identity import H, typed_id

T, F, U = "true", "false", "indeterminate"

LADDERS = {
    "file": ["enumerated"],
    "package": ["manifest-declared"],
    "vcs-change": ["vcs-reported"],
    "declares": ["syntactic"],
    "literal": ["syntactic"],
    "control-flow": ["syntactic"],
    "clones": ["normalized-body-hash"],
    "imports": ["syntactic-specifier", "resolved-target"],
    "references": ["syntactic-name-match", "resolved-binding"],
    "calls": ["syntactic-callee-name", "resolved-callee"],
    "types": ["annotated", "checked"],
    "unresolved-edge": ["observed"],
    "reachability": ["from-resolved-calls"],
}

UNIVERSE_TOKEN = {
    "typescript": "native.semantic-universe.typescript.v2",
    "rust": "native.semantic-universe.rust.v2",
    "syntax": "native.semantic-universe.syntax.v2",
}


def kleene_not(v: str) -> str:
    if v == T:
        return F
    if v == F:
        return T
    return U


def kleene_and(vals: list[str]) -> str:
    if any(v == F for v in vals):
        return F
    if all(v == T for v in vals):
        return T
    return U


def kleene_or(vals: list[str]) -> str:
    if any(v == T for v in vals):
        return T
    if all(v == F for v in vals):
        return F
    return U


def rung_ge(relation: str, fact_rung: str, min_rung: str) -> bool:
    ladder = LADDERS[relation]
    if fact_rung not in ladder or min_rung not in ladder:
        return False
    return ladder.index(fact_rung) >= ladder.index(min_rung)


def filter_match(filt: dict, *, subject_id: str, payload: dict, fact: dict) -> bool:
    field, cmp_, val = filt["field"], filt["cmp"], filt["value"]
    if field == "subject":
        got = subject_id
    elif field == "resolution":
        got = fact["resolution"]
    elif field == "universe":
        got = fact["sourceUniverse"]
    else:
        got = payload.get(field)
        if got is None and field in payload:
            got = payload[field]
    if cmp_ == "eq":
        return got == val
    if cmp_ == "neq":
        return got != val
    if cmp_ == "in":
        return got in val
    if cmp_ == "prefix":
        return type(got) is str and got.startswith(val)
    if cmp_ == "glob":
        from fnmatch import fnmatch
        return type(got) is str and _glob(got, val)
    return False


def _glob(path: str, pat: str) -> bool:
    """Closed glob: *, ?, ** whole-segment. **/*.rs matches root hello.rs per atom contract."""
    # workflows glob: **/*.ts matches root a.ts
    if pat.startswith("**/"):
        rest = pat[3:]
        from fnmatch import fnmatch
        return fnmatch(path, rest) or fnmatch(path, pat.replace("**/", "*/")) or fnmatch(path.split("/")[-1], rest)
    from fnmatch import fnmatch
    return fnmatch(path, pat)


def occupancy_id(kind: str, payload: dict, native_id: str) -> str:
    if kind == "file":
        return payload.get("path", native_id)
    if kind == "package":
        return payload.get("packageName", native_id)
    return native_id


def eval_atom(atom: dict, *, subject: dict, facts: list[dict], coverages: list[dict], payloads: dict) -> dict:
    rel = atom["relation"]
    minr = atom["minResolution"]
    op = atom["op"]
    matching = []
    for f in facts:
        if f["record"]["relation"] != rel:
            continue
        if not rung_ge(rel, f["record"]["resolution"], minr):
            continue
        pl = payloads[f["id"]]
        sid = occupancy_id(subject["kind"], pl, subject["nativeSubjectId"])
        # subject occupancy: file path equals nativeSubjectId
        if subject["kind"] == "file" and pl.get("path") != subject["nativeSubjectId"]:
            # still allow filters on subject
            pass
        ok = True
        for filt in atom.get("filters") or []:
            occ = subject["nativeSubjectId"]
            if not filter_match(filt, subject_id=occ, payload=pl, fact=f["record"]):
                ok = False
                break
        if ok:
            matching.append(f["id"])
    cov_ids = [c["id"] for c in coverages if c["record"]["relation"] == rel and c["record"]["resolution"] == minr]
    # missing Coverage with no match → indeterminate (except exists with known match)
    has_cov = bool(cov_ids)
    known = matching
    if op == "exists":
        if known:
            value = T
        elif not has_cov:
            value = U
        else:
            # complete coverage, no match
            cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
            value = F if cov_complete else U
    elif op == "none":
        if known:
            value = F
        elif not has_cov:
            value = U
        else:
            cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
            value = T if cov_complete else U
    elif op == "count-at-most":
        n = atom["n"]
        if len(set(known)) > n:
            value = F
        elif not has_cov:
            value = U
        else:
            cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
            value = T if cov_complete and len(set(known)) <= n else U
    elif op == "all-covered":
        cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
        value = T if cov_complete and has_cov else U
    else:
        value = U
    defs = []
    if value == U and not has_cov:
        defs.append("missing-relation-coverage")
    return {
        "value": value,
        "matchingFactIds": sorted(set(known)),
        "coverageIds": sorted(cov_ids),
        "deficiencies": defs,
        "kind": "native-atom",
    }


def walk_predicate(node: dict, *, prefix: str, **kw) -> dict:
    op = node["op"]
    if op in ("exists", "none", "count-at-most", "all-covered"):
        r = eval_atom(node, **kw)
        r["predicateId"] = prefix
        r["operation"] = op
        r["children"] = []
        r["node"] = node
        return r
    if op in ("and", "or"):
        kids = []
        for i, ch in enumerate(node["operands"]):
            kids.append(walk_predicate(ch, prefix=f"{prefix}.{i}", **kw))
        vals = [k["value"] for k in kids]
        value = kleene_and(vals) if op == "and" else kleene_or(vals)
        return {
            "predicateId": prefix,
            "operation": op,
            "value": value,
            "children": kids,
            "matchingFactIds": [],
            "coverageIds": [],
            "deficiencies": [],
            "kind": "boolean",
            "node": node,
        }
    if op == "not":
        kid = walk_predicate(node["operand"], prefix=f"{prefix}.0", **kw)
        return {
            "predicateId": prefix,
            "operation": "not",
            "value": kleene_not(kid["value"]),
            "children": [kid],
            "matchingFactIds": [],
            "coverageIds": [],
            "deficiencies": [],
            "kind": "boolean",
            "node": node,
        }
    raise ValueError(op)


def flatten(node: dict) -> list[dict]:
    out = [node]
    for ch in node.get("children") or []:
        out.extend(flatten(ch))
    return out
