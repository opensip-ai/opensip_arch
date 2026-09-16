"""Scoped successor rows joining the candidate's pre-spawn refusals to the OWNER public route law (candidate 03, RF-1).

Owner law followed, not restated: native-evidence.schemas.v2.json#/x-opensip-public-route-registry rows derive the
workflows common StepTermination through native_evidence_model.v2 public_termination_for(key, origin) and the
kind=failure envelope errors through failure_envelope_errors(key, origin); exit derives from CLASS_TO_EXIT. Where no
closed DomainDetailCode names the condition, termination.domainDetail is ABSENT and errorCode names it (the
release-declaration route precedent); the envelope still owes one DomainDetail whose remedy is a true next step for every
key using that code (remedyKeyingConstraint).

Choice (follows existing public-route law, minimal vocabulary): three INTERNAL keys with domainDetail absent, errorCode
REQUEST.PRECONDITION_FAILED, class request-rejected; exactly TWO new DomainDetailCode members used only as envelopeDetail,
because no existing member's remedy is a true next step for 'the provider input exceeds the wire limits' or 'a dependency
identity string cannot be carried unchanged'. One new originating boundary value, admitted-plan-input, is an explicit
vocabulary extension of possibleOrigins. check_routes.py applies the PUBLISHED rows (public-route-successor.v1.json) in
memory to the pinned owner model and derives every public field with the owner functions.
"""
import ast
import copy
import hashlib

NEW_ORIGIN = "admitted-plan-input"
DEP_KEY = "native.dependency-source-not-wire-representable"
PREP_KEY = "native.prepared-output-exceeds-wire-limit"
REQ_KEY = "native.provider-request-exceeds-wire-limit"

NEW_DETAIL_MEMBERS = {
    "native.provider-input-exceeds-wire-limit":
        "the Plan-bound provider input (snapshot, dependency sources or prepared outputs) does not fit the provider protocol "
        "frame, entry or request limits; reduce or split that input - nothing is truncated",
    "native.provider-input-not-representable":
        "a dependency source package name, version, source id or file path cannot be carried by the provider protocol "
        "unchanged (non-NFC text, a scalar at or below U+0020 in name or version, a package key over 4096 scalars, or a "
        "path over 4096 scalars or with an empty, '.', '..' or drive-prefix segment); rename or exclude it - nothing is normalized",
}

_OPERATIONAL = "the internal decision key and its subject are retained in the operational diagnostic record"

ROUTE_KEYS = {
    DEP_KEY: {
        "possibleOrigins": [NEW_ORIGIN], "originDependent": False,
        "route": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": None,
                  "operationalCarrier": _OPERATIONAL,
                  "why": "an owner-admitted dependency source set whose identity-bearing strings the Rust3 wire cannot carry unchanged, refused at dependency-source set admission before PlanId",
                  "envelopeDetail": "native.provider-input-not-representable"}},
    PREP_KEY: {
        "possibleOrigins": [NEW_ORIGIN], "originDependent": False,
        "route": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": None,
                  "operationalCarrier": _OPERATIONAL,
                  "why": "an explicitly selected, owner-admitted prepared output set with more inert rows or blob bytes than the retained ProtocolLimitsV3 bounds, refused at prepared set admission before Plan construction",
                  "envelopeDetail": "native.provider-input-exceeds-wire-limit"}},
    REQ_KEY: {
        "possibleOrigins": [NEW_ORIGIN], "originDependent": False,
        "route": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED", "domainDetail": None,
                  "operationalCarrier": _OPERATIONAL,
                  "why": "a planned host-to-worker frame over maxFramePayloadBytes, or a planned major-3 request over maxRequestPayloadBytesTotal or maxRequestFrames, refused by the Plan-time pre-spawn planner",
                  "envelopeDetail": "native.provider-input-exceeds-wire-limit"}},
}

PRE_SPAWN_TIMINGS = ["before-plan-id", "before-plan-construction", "plan-time-no-spawn"]

SELECTORS = {
    DEP_KEY: {
        "ownerFunction": "dependency_source_set_admit",
        "successorFunction": "tools/representability.py#dependency_source_set_admit_successor",
        "rules": ["DEPSRC-SET-KEY-CONSTRAINTS", "DEPSRC-WIRE-REPRESENTABILITY"],
        "applies": "only after the owner function admits the set; owner refusals keep precedence; a refused set mints no dependencySourceSetId",
        "timing": "before-plan-id",
        "timingAnchor": {"pin": "nativeMd", "line": 2500, "needle": "snapshot seal and dependency-source admission, before PlanId:"}},
    PREP_KEY: {
        "ownerFunction": "prepared_output_set_admit",
        "successorFunction": "tools/representability.py#prepared_output_set_admit_successor",
        "rules": ["PREPARED-V3-WIRE-LIMIT"],
        "applies": "only when the owner outcome is admitted; owner non-inert/stale refusals and the defaulted-mode fallback keep precedence",
        "timing": "before-plan-construction",
        "timingAnchor": {"pin": "nativeMd", "line": 1855, "needle": "is refused before Plan construction (`REQUEST.PRECONDITION_FAILED`, detail"}},
    REQ_KEY: {
        "ownerFunction": None,
        "successorFunction": "tools/representability.py#plan_rust3_request / plan_ts2_request",
        "rules": ["REQUEST-WIRE-ACCOUNTING"],
        "applies": "after PlanId and every set admission, before any worker is spawned",
        "timing": "plan-time-no-spawn",
        "timingAnchor": {"pin": "nativeMd", "line": 2848, "needle": "1. **Plan time (no spawn).**"}},
}

# The owner rows each successor route must reproduce in (class, errorCode, domainDetail-absent) and exit.
JOINED_OWNER_ROUTE_ROW = {"key": "native.release-capability-unregistered", "origin": "authenticated-release-declaration"}
JOINED_OWNER_D9_ROW = "native.prepared-output-not-inert"

ROUTE_TABLE_ROWS = [
    {"target": {"pin": "nativeMd", "line": 3525, "rowNeedle": "non-inert prepared row"},
     "condition": "explicitly selected prepared output set over maxPreparedOutputEntries inert rows or maxPreparedOutputTotalBlobBytes blob bytes",
     "class": "request-rejected", "exitCode": "2", "errorCode": "REQUEST.PRECONDITION_FAILED", "carrier": "termination.domainDetail absent; envelope errors[0] native.provider-input-exceeds-wire-limit; key native.prepared-output-exceeds-wire-limit in the operational record", "routeKey": PREP_KEY},
    {"target": {"pin": "nativeMd", "line": 3525, "rowNeedle": "non-inert prepared row"},
     "condition": "owner-admitted dependency source set with a non-NFC or <= U+0020 name/version, non-NFC sourceId, key over 4096 scalars, or a non-NFC, over-long or non-canonical path (new row in the same request-precondition family; no owner route row for dependency-source set refusals existed)",
     "class": "request-rejected", "exitCode": "2", "errorCode": "REQUEST.PRECONDITION_FAILED", "carrier": "termination.domainDetail absent; envelope errors[0] native.provider-input-not-representable; key native.dependency-source-not-wire-representable in the operational record", "routeKey": DEP_KEY},
    {"target": {"pin": "nativeMd", "line": 3525, "rowNeedle": "non-inert prepared row"},
     "condition": "planned host-to-worker frame over maxFramePayloadBytes, or planned major-3 request over maxRequestPayloadBytesTotal / maxRequestFrames",
     "class": "request-rejected", "exitCode": "2", "errorCode": "REQUEST.PRECONDITION_FAILED", "carrier": "termination.domainDetail absent; envelope errors[0] native.provider-input-exceeds-wire-limit; key native.provider-request-exceeds-wire-limit in the operational record", "routeKey": REQ_KEY},
]


def function_source_sha256(module_text, name):
    tree = ast.parse(module_text)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    return hashlib.sha256(ast.get_source_segment(module_text, node).encode("utf-8")).hexdigest()


def successor_document(arch_pin_rows, model_text):
    pins = {r["key"]: r for r in arch_pin_rows}
    selectors = copy.deepcopy(SELECTORS)
    for sel in selectors.values():
        if sel["ownerFunction"]:
            sel["ownerFunctionSourceSha256"] = function_source_sha256(model_text, sel["ownerFunction"])
            sel["ownerFunction"] = "docs/coop/design-corrections/native/native_evidence_model.v2.py#" + sel["ownerFunction"]
    return {
        "artifact": "opensip.native-evidence.public-route-registry.successor", "version": "1",
        "standing": "AUTHOR candidate 03 scoped successor to native-evidence.schemas.v2.json#/x-opensip-public-route-registry, public-detail-registry.v1.json records, workflows common.schema.json $defs/DomainDetailCode, native_evidence_model.v2.py PUBLIC_ROUTE_REMEDIES and the native-evidence.md section 10 request-precondition route row. Parent bytes unchanged; not approval.",
        "parents": [pins[k] for k in ("evidence", "publicDetailRegistry", "workflowCommon", "nativeModel", "nativeMd")],
        "publicForm": "internal-key-domainDetail-absent",
        "newOrigin": {"id": NEW_ORIGIN, "vocabularyExtension": "possibleOrigins",
                      "meaning": "a Plan-bound input the host admitted from the repository, a lockfile, a vendored or imported tree or a preparation step: external to the host (never a host invariant) and never a user configuration"},
        "addKeys": copy.deepcopy(ROUTE_KEYS),
        "addDomainDetailCodes": [{"code": c, "owner": "native", "selector": "native-evidence.schemas.v2.json#/x-opensip-public-route-registry envelopeDetail (public-route-successor.v1.json)", "remedy": r}
                                 for c, r in NEW_DETAIL_MEMBERS.items()],
        "selectors": selectors,
        "preSpawnTimings": PRE_SPAWN_TIMINGS,
        "joinedOwnerRows": {"routeRegistry": JOINED_OWNER_ROUTE_ROW, "modelD9Map": JOINED_OWNER_D9_ROW},
        "routeTableRows": ROUTE_TABLE_ROWS,
        "unchanged": ["every existing key, class, errorCode, faultCause and reasonCode", "the D9 class to exit table", "all 315 existing DomainDetailCode members and their remedies", "model D9_MAP (its keys are public detail codes; these routes carry none)"],
    }


class Overlay:
    """Apply a PUBLISHED successor document in memory to an already-loaded pinned owner model; restore on exit."""

    def __init__(self, NE, doc):
        self.NE, self.doc = NE, doc

    def __enter__(self):
        self.saved = (copy.deepcopy(self.NE.PUBLIC_ROUTE_REGISTRY["keys"]), dict(self.NE.PUBLIC_ROUTE_REMEDIES))
        keys, rem = self.NE.PUBLIC_ROUTE_REGISTRY["keys"], self.NE.PUBLIC_ROUTE_REMEDIES
        for k, row in self.doc["addKeys"].items():
            if k in keys:
                raise RuntimeError("successor key already owned: " + k)
            keys[k] = copy.deepcopy(row)
        for m in self.doc["addDomainDetailCodes"]:
            if m["code"] in rem:
                raise RuntimeError("successor member already owned: " + m["code"])
            rem[m["code"]] = m["remedy"]
        return self

    def __exit__(self, *exc):
        keys, rem = self.NE.PUBLIC_ROUTE_REGISTRY["keys"], self.NE.PUBLIC_ROUTE_REMEDIES
        keys.clear(); keys.update(self.saved[0])
        rem.clear(); rem.update(self.saved[1])
        return False

    def derive(self, raw_key, origin=NEW_ORIGIN):
        term = self.NE.public_termination_for(raw_key, origin)
        errors = self.NE.failure_envelope_errors(raw_key, origin)
        return {"termination": term, "errors": errors, "exitCode": self.NE.CLASS_TO_EXIT[term["class"]]}


def common_schema_with_members(common, doc):
    out = copy.deepcopy(common)
    enum = out["$defs"]["DomainDetailCode"]["enum"]
    for m in doc["addDomainDetailCodes"]:
        if m["code"] in enum:
            raise RuntimeError("member already present: " + m["code"])
        enum.append(m["code"])
    return out
