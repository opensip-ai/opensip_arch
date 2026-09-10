"""Independently reconstructed workflow/public-surface derivations.

Sources: workflows-and-surfaces.md sections 1, 3, 4, 6, 8, 9, 10, 12;
native-evidence.md sections 1.4 and 10; native-evidence.schemas.v2.json
#/x-opensip-public-route-registry; admission-and-qualification.md section 1.1;
command-inventory.v1.json; the closed workflows schema bundle.
"""
from __future__ import annotations

import hashlib
import json

import closure as CL
import osip
import schemas
from osip import C, H, raw_sha256, record_digest

MATRIX = CL.MATRIX
CELLS = {(c["capability"], c["mode"]): c["state"] for c in MATRIX["cells"]}
CAP_IDS = [c["id"] for c in MATRIX["capabilities"]]
CAP_RELATIONS = {c["id"]: [tuple(r) for r in c["relations"]]
                 for c in MATRIX["capabilities"]}
ROUTES = CL.NATIVE["x-opensip-public-route-registry"]
INVENTORY = json.loads(osip.doc_bytes(
    "docs/coop/design-corrections/workflows/command-inventory.v1.json").decode())
COMMANDS = {c["name"]: c for c in INVENTORY["commands"]}
D9 = json.loads(osip.doc_bytes(
    "docs/coop/artifacts/d9-exit-contract.v1.14.json").decode())


# --------------------------------------------------------------------------
# native section 1.4 / admission section 1.1: the DEFAULT profile is fixed by
# the MATRIX, not by the release declaration.
# --------------------------------------------------------------------------

def default_capability_selection(units, release_registry):
    """units: [{workspaceRoot, languageMode}].
    release_registry: [{capabilityId, languageModes[]}] (authenticated input).
    Returns (analysis-spec rows, undeclaredCapabilities)."""
    declared = {}
    for row in release_registry:
        declared.setdefault(row["capabilityId"], set()).update(row["languageModes"])
    rows, undeclared = [], []
    for u in units:
        mode = u["languageMode"]
        for cid in CAP_IDS:
            state = CELLS[(cid, mode)]
            if state == "NOT-SELECTED":
                continue           # outside D-371; no promise, so not requested
            rows.append({"capabilityId": cid, "languageMode": mode,
                         "workspaceRoot": u["workspaceRoot"], "required": True})
            if mode not in declared.get(cid, set()):
                undeclared.append({"capabilityId": cid, "languageMode": mode,
                                   "workspaceRoot": u["workspaceRoot"]})
    rows.sort(key=lambda r: C(r))
    return rows, undeclared


def admit_release_capability_registry(rows):
    """The internal decision KEY alone; the helper is not passed an origin."""
    seen = set()
    for r in rows:
        cid = r["capabilityId"]
        if cid.startswith("preview-"):
            return "native.release-capability-preview-constant:" + cid
        if cid not in CAP_IDS:
            return "native.release-capability-unregistered:" + cid
        if cid in seen:
            return "native.release-capability-duplicate:" + cid
        seen.add(cid)
        for mode in r["languageModes"]:
            if (cid, mode) not in CELLS:
                return "native.release-capability-mode-unregistered:" + mode
            if CELLS[(cid, mode)] == "NOT-SELECTED":
                return "native.release-capability-mode-not-selected:%s/%s" % (cid, mode)
    return None


def admit_requested_capabilities(rows):
    for r in rows:
        cid, mode = r["capabilityId"], r["languageMode"]
        if cid not in CAP_IDS:
            return "native.requested-capability-unregistered:" + cid
        if mode not in CL.LANGUAGE_MODES:
            return "native.requested-capability-mode-unregistered:" + mode
        if CELLS[(cid, mode)] == "NOT-SELECTED":
            return "native.requested-capability-mode-not-selected:%s/%s" % (cid, mode)
    return None


def release_absence_notices(undeclared):
    notices = [{"code": "native.capability-unavailable",
                "capabilityId": u["capabilityId"],
                "languageMode": u["languageMode"],
                "workspaceRoot": u["workspaceRoot"],
                "remedy": "install or enable the provider that declares this "
                          "capability for this language mode"}
               for u in undeclared]
    return {"noticeCount": len(notices), "notices": notices}


def invocation_availability(step_leaves):
    """step_leaves: [(stepId, leaf)] for every analysis step that made a selection."""
    steps = [{"stepId": sid, "noticeCount": leaf["noticeCount"],
              "notices": leaf["notices"]} for sid, leaf in step_leaves]
    return {"stepCount": len(steps),
            "totalNoticeCount": sum(s["noticeCount"] for s in steps),
            "steps": steps}


def projection_for(cid):
    """native section 1.4: candidate-only capabilities have NO Coverage entry."""
    return ("selection-account-only" if not CAP_RELATIONS[cid]
            else "coverage-entry")


# --------------------------------------------------------------------------
# native section 10 public route derivation
# --------------------------------------------------------------------------

def normalize_internal_key(raw):
    """Longest registered key followed by a colon; the remainder is the subject.
    A raw string matching no registered key REFUSES."""
    best = None
    for k in ROUTES["keys"]:
        if raw == k:
            if best is None or len(k) > len(best):
                best = k
        elif raw.startswith(k + ":"):
            if best is None or len(k) > len(best):
                best = k
    if best is None:
        raise ValueError("native.public-route-key-unregistered:" + raw)
    return best, raw[len(best) + 1:] if len(raw) > len(best) else ""


MARKER = "...#sha256:"


def bounded_subject(raw):
    """BoundedText is 1024 UNICODE CODE POINTS; the SHA-256 input is raw as
    UTF-8 with no additional normalization."""
    if len(raw) <= 1024:
        return raw
    keep = 1024 - len(MARKER) - 64
    return raw[:keep] + MARKER + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def public_termination_for(raw_key, origin):
    key, subject = normalize_internal_key(raw_key)
    row = ROUTES["keys"][key]
    if origin not in row["possibleOrigins"]:
        raise ValueError("native.public-route-origin-not-possible:%s@%s" % (key, origin))
    route = row["route"] if not row["originDependent"] else \
        row["byOriginatingBoundary"][origin]
    t = {"class": route["class"]}
    if route.get("errorCode"):
        t["errorCode"] = route["errorCode"]
    if route.get("faultCause"):
        t["faultCause"] = route["faultCause"]
    if route.get("domainDetail"):
        d = {"code": route["domainDetail"],
             "remedy": "correct the refused value and re-run"}
        s = bounded_subject(raw_key)
        if s:
            d["subject"] = s
        t["domainDetail"] = d
    return t, route


def failure_envelope_errors(termination, route, raw_key):
    """Where the termination carries a detail, errors is EXACTLY that detail."""
    if "domainDetail" in termination:
        return [termination["domainDetail"]]
    d = {"code": route["envelopeDetail"],
         "remedy": "correct the refused value and re-run",
         "subject": bounded_subject(raw_key)}
    return [d]


def failure_envelope(request_id, raw_key, origin):
    t, route = public_termination_for(raw_key, origin)
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
           "kind": "failure", "requestId": request_id, "termination": t,
           "exitCode": D9["classToExitCode"][t["class"]],
           "errors": failure_envelope_errors(t, route, raw_key)}
    return env


# --------------------------------------------------------------------------
# workflows section 1: idempotency keys
# --------------------------------------------------------------------------

def mutation_replay_scope(request_id, step_id, project_id, operation):
    return {"schemaVersion": 1, "requestId": request_id, "stepId": step_id,
            "projectId": project_id, "operation": operation}


def mutation_intent_key(scope):
    """The bare 64-hex H('workflow.mutation-intent', MutationReplayScopeV1)."""
    return H("workflow.mutation-intent", scope)


def repair_apply_key(project_id, repair_plan_id, base_snapshot_id):
    """raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId})."""
    return raw_sha256(C({"operation": "repair-apply", "projectId": project_id,
                         "repairPlanId": repair_plan_id,
                         "baseSnapshotId": base_snapshot_id}))


def repair_plan_id(descriptor):
    return "repairplan2:" + H("workflow.repair-plan", descriptor)


def mutation_receipt_id(receipt_without_id):
    return "receipt2:" + H("workflow.mutation-receipt", receipt_without_id)


def baseline_id(descriptor):
    return "baseline2:" + H("workflow.baseline", descriptor)


def comparison_id(descriptor):
    return "comparison2:" + H("workflow.comparison", descriptor)


# --------------------------------------------------------------------------
# workflows section 6 / native section 4.6: the per-requirement plane
# --------------------------------------------------------------------------
NATIVE_RELATIONS = set(CL.RELATIONS)
IMPORTED_RELATIONS = {"runtime-observation", "history-change"}
NATIVE_DEFICIENCIES = set(
    schemas.LOADED["common"]["$defs"]["NativeSufficiencyDeficiency"]["enum"])
IMPORTED_DEFICIENCIES = set(
    schemas.LOADED["common"]["$defs"]["ImportedRequirementDeficiency"]["enum"])


def admit_evidence_requirement(req):
    """The PLANE is decided from the relation's registry membership, never
    from the value.  Presence is typed: deficiency is required exactly when
    satisfied is false and forbidden when it is true."""
    rel = req["relation"]
    if rel in NATIVE_RELATIONS:
        plane, vocab = "native", NATIVE_DEFICIENCIES
        if req["minResolution"] not in CL.RELATIONS[rel]["ladder"]:
            return "CONFIG.INVALID", ("minResolution %s is not a rung of %s's ladder %s"
                                      % (req["minResolution"], rel,
                                         CL.RELATIONS[rel]["ladder"]))
    elif rel in IMPORTED_RELATIONS:
        plane, vocab = "imported", IMPORTED_DEFICIENCIES
        if req["minResolution"] != "observed":
            return "CONFIG.INVALID", "imported relations carry the one-rung ladder [observed]"
    else:
        return "CONFIG.INVALID", "relation %s is in neither relation registry" % rel
    if req["satisfied"] is True:
        if "deficiency" in req:
            return "CONFIG.INVALID", "deficiency is forbidden when satisfied is true"
        return None, plane
    if "deficiency" not in req:
        return "CONFIG.INVALID", "deficiency is required when satisfied is false"
    if req["deficiency"] is None:
        return "CONFIG.INVALID", "an explicit null is refused in both branches"
    if req["deficiency"] not in vocab:
        return "CONFIG.INVALID", ("cross-plane value %r on the %s plane"
                                  % (req["deficiency"], plane))
    return None, plane


# --------------------------------------------------------------------------
# section 5 / identity section 4: the evaluator's strong-Kleene predicate table
# --------------------------------------------------------------------------

def atom_value(op, matches, coverage_complete, n=None):
    """exists/none/count-at-most/all-covered under strong Kleene."""
    if op == "exists":
        if matches:
            return "true"
        return "false" if coverage_complete else "indeterminate"
    if op == "none":
        if matches:
            return "false"
        return "true" if coverage_complete else "indeterminate"
    if op == "count-at-most":
        if len(matches) > n:
            return "false"
        return "true" if coverage_complete else "indeterminate"
    if op == "all-covered":
        return "true" if coverage_complete else "indeterminate"
    raise ValueError(op)


def min_resolution_satisfied(relation, have_rung, min_rung):
    """Satisfaction is LADDER-INDEX comparison INSIDE ONE RELATION.  Nothing
    orders a rung of one relation against a rung of another; a cross-relation
    comparison is an admission refusal, never a true or false predicate."""
    ladder = CL.RELATIONS[relation]["ladder"]
    if have_rung not in ladder:
        raise ValueError("CROSS_RELATION_RUNG_COMPARISON:%s@%s" % (relation, have_rung))
    if min_rung not in ladder:
        raise ValueError("ATOM_MIN_RESOLUTION_NOT_IN_RELATION_LADDER:%s@%s"
                         % (relation, min_rung))
    return ladder.index(have_rung) >= ladder.index(min_rung)


# --------------------------------------------------------------------------
# native section 4.3 RC-1: the registered (relation, rung) applicability table
# --------------------------------------------------------------------------

def rc1_table():
    rows = []
    for rel in sorted(CL.RELATIONS):
        for rung in CL.RELATIONS[rel]["ladder"]:
            resolved = rung in CL.RESOLVED_RUNGS
            rows.append({
                "relation": rel, "rung": rung, "resolvedRung": resolved,
                "state": "one of complete/incomplete/partial/not-attempted"
                         if resolved else "not-applicable",
                "attempted": "provider-decided" if resolved else False,
                "unresolvedEdgeCount": "provider-decided" if resolved else 0,
                "unresolvedEdgeClasses": "provider-decided" if resolved else [],
                "anchorClass": CL.RELATIONS[rel]["anchorLaw"]["class"],
                "anchors": CL.RELATIONS[rel]["anchorLaw"].get(
                    "cardinality", CL.RELATIONS[rel]["anchorLaw"].get("minimum")),
                "subjectKind": CL.RELATIONS[rel]["subjectKind"],
                "universeRule": CL.RELATIONS[rel]["universeRule"],
                "coverageTotality": "coverageTotality" in CL.RELATIONS[rel],
                "snapshotJoins": [j.get("form") for j in
                                  CL.RELATIONS[rel]["snapshotJoins"]],
            })
    return rows
