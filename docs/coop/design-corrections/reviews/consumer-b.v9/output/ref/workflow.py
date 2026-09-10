"""Workflow-surface reconstruction: default capability selection, the public
route derivation, bounded subjects, failure envelopes and invocation records.

Sources: native-evidence S1.4/S10 + x-opensip-public-route-registry,
workflows-and-surfaces S1/S8/S9/S12, admission-and-qualification S1.1,
identity-and-evidence S5, and the pinned workflow schemas.
"""
from __future__ import annotations

import hashlib

import canon as K
import kit
from store import Refusal

MATRIX = kit.doc("capability-matrix")
CELLS = {(c["capability"], c["mode"]): c for c in MATRIX["cells"]}
CAPABILITIES = {c["id"]: c for c in MATRIX["capabilities"]}
ROUTES = kit.PUBLIC_ROUTES["keys"]
EXIT_BY_CLASS = {"success": 0, "policy-failed": 1, "request-rejected": 2,
                 "indeterminate": 3, "operational-failed": 4, "interrupted": 130}


# ---------------------------------------------------------------------------
# Default capability selection: FIXED BY THE MATRIX, not by a release.
# ---------------------------------------------------------------------------

def default_capability_selection(units, declared_rows):
    """units: [{workspaceRoot, languageMode}]; declared_rows: the AUTHENTICATED
    release declaration [{capabilityId, languageModes[]}].

    "For each discovered unit the `default` profile MUST request every
    capability whose (capability, unit languageMode) cell is not NOT-SELECTED",
    including UNSUPPORTED-TYPED cells."""
    declared = {}
    seen = set()
    for row in declared_rows:
        if row["capabilityId"] in seen:
            raise Refusal("native.release-capability-duplicate", row["capabilityId"])
        seen.add(row["capabilityId"])
        if row["capabilityId"] not in CAPABILITIES:
            raise Refusal("native.release-capability-unregistered", row["capabilityId"])
        if row["capabilityId"].startswith("preview-"):
            raise Refusal("native.release-capability-preview-constant",
                          row["capabilityId"])
        for mode in row["languageModes"]:
            cell = CELLS.get((row["capabilityId"], mode))
            if cell is None:
                raise Refusal("native.release-capability-mode-unregistered", mode)
            if cell["state"] == "NOT-SELECTED":
                raise Refusal("native.release-capability-mode-not-selected",
                              f"{row['capabilityId']}|{mode}")
            declared.setdefault(row["capabilityId"], set()).add(mode)

    requested, notices, tuples = [], [], set()
    for unit in units:
        mode = unit["languageMode"]
        for cap_id in sorted(CAPABILITIES):
            cell = CELLS[(cap_id, mode)]
            if cell["state"] == "NOT-SELECTED":
                continue
            key = (cap_id, mode, unit["workspaceRoot"])
            if key in tuples:
                raise Refusal(
                    "native.requested-capability-duplicate-ownership-tuple",
                    "|".join(key))
            tuples.add(key)
            requested.append({"capabilityId": cap_id, "languageMode": mode,
                              "workspaceRoot": unit["workspaceRoot"],
                              "required": True})
            if mode not in declared.get(cap_id, set()):
                notices.append({"code": "native.capability-unavailable",
                                "capabilityId": cap_id, "languageMode": mode,
                                "workspaceRoot": unit["workspaceRoot"],
                                "remedy": "install the provider that declares "
                                          "this capability, or narrow "
                                          "analysis.capabilities explicitly"})
    spec = {"schemaVersion": 2,
            "requestedCapabilities": sorted(requested, key=K.C),
            "policyPackIds": [], "parameters": []}
    return spec, notices


def capability_availability(step_notices):
    """workflows S8 / native S1.4: composed PER STEP, never one flat array."""
    steps = []
    for step_id, notices in step_notices:
        steps.append({"stepId": step_id, "noticeCount": len(notices),
                      "notices": notices})
    return {"stepCount": len(steps),
            "totalNoticeCount": sum(s["noticeCount"] for s in steps),
            "steps": steps}


def capability_projection(cap_id):
    """native S1.4: fact-producing -> coverage-entry; candidate-only ->
    selection-account-only (no relation@rung, so no Coverage entry)."""
    cap = CAPABILITIES[cap_id]
    if cap.get("authority") == "candidate-only" or not cap["relations"]:
        return {"projection": "selection-account-only", "relations": []}
    return {"projection": "coverage-entry",
            "relations": [f"{r}@{g}" for r, g in cap["relations"]]}


# ---------------------------------------------------------------------------
# The public route derivation.
# ---------------------------------------------------------------------------

def normalize_internal_key(raw: str):
    """Longest registered key followed by a colon; the remainder is subject.
    A string matching no registered key REFUSES."""
    if raw in ROUTES:
        return raw, None
    best = None
    for key in ROUTES:
        if raw.startswith(key + ":") and (best is None or len(key) > len(best)):
            best = key
    if best is None:
        raise Refusal("native.public-route-key-unregistered", raw[:80])
    return best, raw[len(best) + 1:]


MARKER = "...#sha256:"


def bounded_subject(raw: str) -> str:
    """native S10: exactly 1024 Unicode code points, marker + SHA-256 of the
    untruncated subject's UTF-8 bytes."""
    if len(raw) <= 1024:
        return raw
    head = raw[: 1024 - len(MARKER) - 64]
    return head + MARKER + hashlib.sha256(raw.encode("utf-8")).hexdigest()


def public_termination_for(raw_key: str, origin: str):
    key, value = normalize_internal_key(raw_key)
    row = ROUTES[key]
    if origin not in row["possibleOrigins"]:
        raise Refusal("native.public-route-origin-not-possible",
                      f"{key}@{origin}")
    route = (row["byOriginatingBoundary"][origin] if row.get("originDependent")
             else row["route"])
    term = {"class": route["class"]}
    if "errorCode" in route:
        term["errorCode"] = route["errorCode"]
    if route.get("faultCause"):
        term["faultCause"] = route["faultCause"]
    if route.get("domainDetail"):
        subject = bounded_subject(key + (":" + value if value else ""))
        term["domainDetail"] = {"code": route["domainDetail"],
                                "remedy": _remedy(route["domainDetail"]),
                                "subject": subject}
    return term, route, key, value


def _remedy(code):
    return {
        "CONFIG.INVALID": "correct the analysis.capabilities selection in the "
                          "project configuration or on the command line",
        "PROVIDER.NOT_SELECTED": "this capability/mode cell is outside the "
                                 "selected product; remove it from the request",
    }.get(code, "see the operational diagnostic record for the decision key")


def failure_envelope_errors(termination, route, key, value):
    """"where the termination carries a detail, errors is EXACTLY that detail;
    where it does not, the route's own envelopeDetail supplies one.\""""
    if "domainDetail" in termination:
        return [dict(termination["domainDetail"])]
    return [{"code": route["envelopeDetail"],
             "remedy": _remedy(route["envelopeDetail"]),
             "subject": bounded_subject(key + (":" + value if value else ""))}]


def failure_envelope(request_id, raw_key, origin):
    """"Before a Plan or Run exists NO run envelope is fabricated - the failure
    envelope carries the termination, its errors and the request id.\""""
    term, route, key, value = public_termination_for(raw_key, origin)
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
           "kind": "failure", "requestId": request_id, "termination": term,
           "exitCode": EXIT_BY_CLASS[term["class"]],
           "errors": failure_envelope_errors(term, route, key, value)}
    kit.validate("command-envelope", "#", env, "failure envelope")
    return env


# ---------------------------------------------------------------------------
# Mutation replay scope and the repair-apply key.
# ---------------------------------------------------------------------------

def mutation_replay_scope(request_id, step_id, project_id, operation):
    scope = {"schemaVersion": 1, "requestId": request_id, "stepId": step_id,
             "projectId": project_id, "operation": operation}
    kit.validate("invocation-record", "#/$defs/MutationReplayScopeV1", scope,
                 "MutationReplayScopeV1")
    return scope, K.H("workflow.mutation-intent", scope)


def repair_apply_key(project_id, repair_plan_id, base_snapshot_id):
    """"raw SHA-256 of C({operation, projectId, repairPlanId, baseSnapshotId})"
    -- a DIFFERENT recipe from the generic H over MutationReplayScopeV1."""
    rec = {"operation": "repair-apply", "projectId": project_id,
           "repairPlanId": repair_plan_id, "baseSnapshotId": base_snapshot_id}
    return rec, K.canonical_record_digest(rec)


# ---------------------------------------------------------------------------
# Pinned-purge refusal (identity S5 + workflows S12).
# ---------------------------------------------------------------------------

PURGE_CONSEQUENCES = ["named-pins-revoked",
                      "dependent-evidence-replay-unavailable",
                      "sealed-history-retained"]


def pinned_purge_refusal(request_id, run_id, active_pins):
    pins = sorted(active_pins, key=lambda p: p["pinId"].encode("utf-8"))
    if len({p["pinId"] for p in pins}) != len(pins):
        raise Refusal("PIN_INVENTORY_NOT_UNIQUE", "")
    if len(pins) > 4096:
        raise Refusal("PIN_INVENTORY_OVER_BOUND", str(len(pins)))
    for p in pins:
        if len(p["pinId"]) > 256:
            raise Refusal("PIN_NAME_OVER_BOUND", p["pinId"][:32])
    detail = {"code": "evidence.pinned",
              "remedy": "revoke the named pins with the explicit destructive "
                        "purge authorization, or purge an unpinned Run",
              "subject": run_id,
              "purgeDisclosure": {"runId": run_id, "activePins": pins,
                                  "consequences": PURGE_CONSEQUENCES}}
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
           "kind": "failure", "requestId": request_id,
           "termination": {"class": "request-rejected",
                           "errorCode": "REQUEST.PRECONDITION_FAILED",
                           "domainDetail": detail},
           "exitCode": 2, "errors": [detail]}
    kit.validate("command-envelope", "#", env, "pinned purge refusal")
    return env
