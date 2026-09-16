"""Scoped successor rows joining the candidate's refusals to the OWNER public route law (candidate 06; review-02 RF-1,
review-03 RF-3, A-1, A-2, A-3).

Owner law followed, not restated: native-evidence.schemas.v2.json#/x-opensip-public-route-registry rows derive the
workflows common StepTermination through native_evidence_model.v2 public_termination_for(key, origin) and the
kind=failure envelope errors through failure_envelope_errors(key, origin); exit derives from CLASS_TO_EXIT. Where no
closed DomainDetailCode names the condition, termination.domainDetail is ABSENT (release-declaration precedent) and the
envelope still owes one registered DomainDetail whose remedy is a true next step for every key using it.

Each key has a CONDITION CLASS that decides its owner family, errorCode and envelope detail:
  representability - a Plan-bound input whose content cannot satisfy the wire precondition; the request-precondition
      family of non-inert / stale prepared rows and invalid release declarations: REQUEST.PRECONDITION_FAILED,
      envelope native.provider-input-not-representable.
  bound - a well-formed input exceeding a published bound, refused without truncation; the PROJECT.SCOPE_LIMIT /
      native.too-many-units family (nativeMd row 3534): REQUEST.UNSATISFIABLE, envelope native.provider-input-exceeds-wire-limit.
One origin value, admitted-plan-input (actor external-input), is an explicit possibleOrigins vocabulary extension.
"""
import copy
import hashlib

NEW_ORIGIN = "admitted-plan-input"
DEP_KEY = "native.dependency-source-not-wire-representable"
PREP_PATH_KEY = "native.prepared-output-not-wire-representable"
PREP_KEY = "native.prepared-output-exceeds-wire-limit"
REQ_KEY = "native.provider-request-exceeds-wire-limit"
NOT_REPRESENTABLE = "native.provider-input-not-representable"
EXCEEDS = "native.provider-input-exceeds-wire-limit"

NEW_DETAIL_MEMBERS = {
    EXCEEDS: ("the Plan-bound provider input (snapshot, dependency sources or prepared outputs) does not fit the provider protocol "
              "frame, entry or request limits under the host's canonical send schedule; reduce or split that input - nothing is truncated or re-chunked"),
    NOT_REPRESENTABLE: ("a Plan-bound provider input string cannot be carried by the provider protocol unchanged: a dependency source package "
                        "name or version containing a scalar at or below U+0020, a non-NFC name, version, source id or path, a package key over 4096 "
                        "scalars, or a dependency source file path, prepared output site path or generated-file logical path with a '.' or '..' "
                        "segment, a leading '/', or an empty or drive-prefix segment where its path law forbids them; rename or exclude it - nothing is normalized"),
}

CONDITION_CLASSES = {
    "representability": {"errorCode": "REQUEST.PRECONDITION_FAILED", "envelopeDetail": NOT_REPRESENTABLE,
                         "ownerFamily": {"routeRegistry": {"key": "native.release-capability-unregistered", "origin": "authenticated-release-declaration"},
                                         "modelD9Map": "native.prepared-output-not-inert",
                                         "routeTable": {"pin": "nativeMd", "line": 3525, "rowNeedle": "non-inert prepared row"}}},
    "bound": {"errorCode": "REQUEST.UNSATISFIABLE", "envelopeDetail": EXCEEDS,
              "ownerFamily": {"routeRegistry": {"key": "native.requested-capability-mode-not-selected", "origin": "external-configuration"},
                              "modelD9Map": "PROJECT.SCOPE_LIMIT",
                              "routeTable": {"pin": "nativeMd", "line": 3534, "rowNeedle": "bounded selection array exceeds its published bound, without truncation"}}},
}

_OPERATIONAL = "the internal decision key and its subject are retained in the operational diagnostic record"


def _key(cls, why):
    c = CONDITION_CLASSES[cls]
    return {"possibleOrigins": [NEW_ORIGIN], "originDependent": False, "conditionClass": cls,
            "route": {"class": "request-rejected", "errorCode": c["errorCode"], "domainDetail": None, "operationalCarrier": _OPERATIONAL,
                      "why": why, "envelopeDetail": c["envelopeDetail"]}}


ROUTE_KEYS = {
    DEP_KEY: _key("representability", "an owner-selected dependency source set whose identity-bearing strings the Rust3 wire cannot carry unchanged, refused at dependency-source set admission before PlanId"),
    PREP_PATH_KEY: _key("representability", "a selected prepared output set whose expansion-site path or generated-file logical path fails its owner path law, refused at prepared set admission before Plan construction, in either prepared mode"),
    PREP_KEY: _key("bound", "an explicitly selected, owner-admitted prepared output set with more inert rows or blob bytes than the retained ProtocolLimitsV3 bounds, refused without truncation at prepared set admission before Plan construction"),
    REQ_KEY: _key("bound", "a request whose canonical host send schedule has a frame over maxFramePayloadBytes, or (major 3) payload bytes over maxRequestPayloadBytesTotal or frames over maxRequestFrames, refused without truncation by the Plan-time planner before any spawn"),
}

PRE_SPAWN_TIMINGS = ["before-plan-id", "before-plan-construction", "plan-time-no-spawn"]

SELECTORS = {
    DEP_KEY: {
        "ownerFunction": "dependency_source_set_admit",
        "successorFunction": "tools/representability.py#dependency_source_set_admit_successor",
        "rules": ["DEPSRC-SET-KEY-CONSTRAINTS", "DEPSRC-WIRE-REPRESENTABILITY"],
        "applies": "phase A, before the owner: a file path of a package the owner would hash that fails the owner path schema (the owner cannot mint its file-manifest identity); phase B, only after the owner admits the set, owner DS refusals keeping precedence: NFC, name/version scalars, key length, canonical-path narrowing. A refused set mints no dependencySourceSetId.",
        "timing": "before-plan-id",
        "timingAnchor": {"pin": "nativeMd", "line": 2500, "needle": "snapshot seal and dependency-source admission, before PlanId:"}},
    PREP_PATH_KEY: {
        "ownerFunction": "prepared_output_set_admit",
        "successorFunction": "tools/representability.py#prepared_output_set_admit_successor",
        "rules": ["PREPARED-V3-PATH-REPRESENTABILITY"],
        "applies": "before the owner (its typed admission would raise instead of refusing), in both explicit and defaulted prepared mode; it outranks the owner non-inert and stale refusals and the wire-limit rule, consistent with the owner validating the PreparedOutputSetV3 schema before any row rule",
        "timing": "before-plan-construction",
        "timingAnchor": {"pin": "nativeMd", "line": 1855, "needle": "is refused before Plan construction (`REQUEST.PRECONDITION_FAILED`, detail"}},
    PREP_KEY: {
        "ownerFunction": "prepared_output_set_admit",
        "successorFunction": "tools/representability.py#prepared_output_set_admit_successor",
        "rules": ["PREPARED-V3-WIRE-LIMIT"],
        "applies": "for every non-rejected owner outcome, judged over every row of the Plan-bound set (the manifest answers every row): when prepared mode was selected explicitly and the owner admitted the set it refuses; when prepared mode was defaulted, including a partially stale set the owner falls back on, the over-limit set is not selected: fallback-non-prepared with zero usable rows, the owner staleRows kept and a wireLimitDisclosure (owner PO-1 mode law, nativeMd 1853-1856); owner non-inert and stale rejections keep precedence",
        "modes": {"explicit": "refuse", "defaulted": "fallback-non-prepared-with-disclosure"},
        "timing": "before-plan-construction",
        "timingAnchor": {"pin": "nativeMd", "line": 1855, "needle": "is refused before Plan construction (`REQUEST.PRECONDITION_FAILED`, detail"}},
    REQ_KEY: {
        "ownerFunction": None,
        "successorFunction": "tools/representability.py#plan_rust3_request / plan_ts2_request; tools/sender_ref.py#consume",
        "rules": ["REQUEST-WIRE-ACCOUNTING", "HOST-SEND-SCHEDULE"],
        "applies": "after PlanId and every set admission, before any worker is spawned; the refusal is stated in terms of the canonical host send schedule, not of every lawful encoding",
        "timing": "plan-time-no-spawn",
        "timingAnchor": {"pin": "nativeMd", "line": 2848, "needle": "1. **Plan time (no spawn).**"},
        "anchorScope": "timing only: the anchored step's own existing outcome for a missing capability is Coverage unknown / provider-unavailable; this refusal is a distinct request refusal taken at the same no-spawn point",
        "planIdFate": "plan2 has been computed but is not published: the termination carries no runId, coverageId or executionId, no run3 and no Coverage is minted, no worker is spawned, and the plan2 value is retained only in the operational record"},
}


def _row(key, condition):
    cls = ROUTE_KEYS[key]["conditionClass"]
    c = CONDITION_CLASSES[cls]
    return {"routeKey": key, "conditionClass": cls, "target": copy.deepcopy(c["ownerFamily"]["routeTable"]), "condition": condition,
            "class": "request-rejected", "exitCode": "2", "errorCode": c["errorCode"],
            "carrier": "termination.domainDetail absent; envelope errors[0] %s; key %s in the operational record" % (c["envelopeDetail"], key)}


ROUTE_TABLE_ROWS = [
    _row(DEP_KEY, "owner-selected dependency source set with a file path failing the owner path schema, a non-NFC or <= U+0020 name/version, a non-NFC sourceId, a key over 4096 scalars, or a non-NFC, over-long or non-canonical path"),
    _row(PREP_PATH_KEY, "selected prepared output set (explicit or defaulted mode) with an expansion-site path or generated-file logical path failing its owner path law"),
    _row(PREP_KEY, "prepared output set over maxPreparedOutputEntries rows or maxPreparedOutputTotalBlobBytes blob bytes, counted over every row of the set, when prepared mode was selected explicitly and the owner admitted it; when prepared mode was defaulted (a partially stale set the owner falls back on included) the set is not selected, with zero usable rows and a disclosure, and owners are analyzed non-prepared (no refusal)"),
    _row(REQ_KEY, "canonical host send schedule with a frame over maxFramePayloadBytes, or a major-3 schedule over maxRequestPayloadBytesTotal / maxRequestFrames (the reserved Cancel counted)"),
]


def successor_document(arch_pin_rows, model_text, source_closure):
    pins = {r["key"]: r for r in arch_pin_rows}
    selectors = copy.deepcopy(SELECTORS)
    for sel in selectors.values():
        if sel["ownerFunction"]:
            closure = source_closure(model_text, [sel["ownerFunction"]])
            sel["ownerFunctionSourceSha256"] = closure[sel["ownerFunction"]]
            sel["calleeClosureSha256"] = closure
            sel["ownerFunction"] = "docs/coop/design-corrections/native/native_evidence_model.v2.py#" + sel["ownerFunction"]
    return {
        "artifact": "opensip.native-evidence.public-route-registry.successor", "version": "2",
        "standing": "AUTHOR candidate 06 proposed scoped successor to native-evidence.schemas.v2.json#/x-opensip-public-route-registry, public-detail-registry.v1.json records, workflows common.schema.json $defs/DomainDetailCode, native_evidence_model.v2.py PUBLIC_ROUTE_REMEDIES and the native-evidence.md section 10 route rows 3525 and 3534. Parent bytes unchanged; applied in memory; not approval; effective as selected semantics only after root acceptance and source-bridge promotion.",
        "parents": [pins[k] for k in ("evidence", "publicDetailRegistry", "workflowCommon", "nativeModel", "nativeMd")],
        "publicForm": "internal-key-domainDetail-absent",
        "newOrigin": {"id": NEW_ORIGIN, "actor": "external-input", "vocabularyExtension": "possibleOrigins",
                      "meaning": "a Plan-bound input the host admitted from the repository, a lockfile, a vendored or imported tree or a preparation step: external input to the host, never a host-generated internal layer and never a user configuration"},
        "conditionClasses": copy.deepcopy(CONDITION_CLASSES),
        "addKeys": copy.deepcopy(ROUTE_KEYS),
        "addDomainDetailCodes": [{"code": c, "owner": "native", "selector": "native-evidence.schemas.v2.json#/x-opensip-public-route-registry envelopeDetail (public-route-successor.v1.json)", "remedy": r}
                                 for c, r in NEW_DETAIL_MEMBERS.items()],
        "selectors": selectors,
        "preSpawnTimings": PRE_SPAWN_TIMINGS,
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


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
