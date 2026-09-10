#!/usr/bin/env python3
"""PROBE 3 - the capability-availability carrier must agree across every surface.

Independently authored expectations. Surfaces under test:
  native-evidence.md section 1.4, admission-and-qualification.md section 1.1,
  workflows-and-surfaces.md section 8, common.schema.json, the native route
  registry annotation, the native helpers, and command parity.

Claims under test:
  * CommandEnvelope.availability carries PER-STEP typed notices with the
    COMPLETE ownership tuple (capabilityId, languageMode, workspaceRoot) in the
    ORIGINAL invocation
  * the actual composition names and calls release_absence_notices, never
    release_absence_details
  * NO live mirror presents doctor / StepTermination as the FULL route; an
    optional generic environment note is not a substitute, and the legacy
    release_absence_details cannot substitute
  * candidate-only capabilities fabricate no fact, Coverage, Candidate or authority
  * all FIVE analysis commands declare capability-availability parity
  * exact notices/counts/order, and invocation-versus-step bounds
"""
import inspect
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as H  # noqa: E402

N, M, C, W = H.N, H.M, H.C, H.W
DC = H.DC
SUBJ = H.SUBJECT

COMMON = "workflows/schemas/common.schema.json"
COMMON_SCHEMA = json.loads((DC / "workflows/schemas/common.schema.json").read_text())
ENVELOPE_SCHEMA = json.loads(
    (DC / "workflows/schemas/command-envelope.schema.json").read_text())
NATIVE_SCHEMAS = json.loads((DC / "native/native-evidence.schemas.v2.json").read_text())
INVENTORY = json.loads((DC / "workflows/command-inventory.v1.json").read_text())

NATIVE_MD = (SUBJ / "docs/v2/contracts/product-v1/native-evidence.md").read_text()
ADMISSION_MD = (SUBJ / "docs/v2/contracts/product-v1/admission-and-qualification.md").read_text()
WORKFLOWS_MD = (SUBJ / "docs/v2/contracts/product-v1/workflows-and-surfaces.md").read_text()


def admits(document, selector, value):
    try:
        W.validate_import_record(document, selector, value)
        return True
    except Exception:  # noqa: BLE001
        return False


# ============================== 1. the actual composition calls the right helper
avail_src = inspect.getsource(N.invocation_availability)
H.check("the-composition-calls-release_absence_notices",
        "release_absence_notices" in avail_src)
H.check("the-composition-never-calls-the-legacy-release_absence_details",
        "release_absence_details" not in avail_src)
legacy_doc = " ".join(N.release_absence_details.__doc__.split())
H.check("the-legacy-helper-declares-itself-superseded-and-non-authoritative",
        "SUPERSEDED" in legacy_doc and "NON-AUTHORITATIVE" in legacy_doc)
H.check("the-legacy-helper-names-the-selected-replacement-route",
        "release_absence_notices" in legacy_doc
        and "CommandEnvelope.availability" in legacy_doc)
H.check("the-legacy-helper-states-it-cannot-carry-the-ownership-account",
        "DISCARDS" in legacy_doc and "workspaceRoot" in legacy_doc)

# The legacy shape genuinely cannot carry workspaceRoot - verified, not asserted.
two_units = [{"rootPath": r, "languageMode": "ts-tsconfig", "languageFamily": "tsjs"}
             for r in ("apps/a", "apps/b")]
undeclared = N.default_capability_selection(two_units, [])["undeclaredCapabilities"]
legacy = N.release_absence_details(undeclared)
H.check("the-legacy-detail-projection-really-discards-workspaceRoot",
        "workspaceRoot" not in json.dumps(legacy))
H.check("the-legacy-detail-projection-collapses-two-units-into-fewer-records",
        len({json.dumps(d, sort_keys=True) for d in legacy}) < len(undeclared),
        {"undeclared": len(undeclared), "distinctLegacy":
         len({json.dumps(d, sort_keys=True) for d in legacy})})

# ================== 2. the selected carrier keeps the complete ownership tuple
notices = N.release_absence_notices(undeclared)
tuples = {(n["capabilityId"], n["languageMode"], n["workspaceRoot"])
          for n in notices["notices"]}
H.check("two-units-keep-two-distinct-notices-per-capability",
        len(undeclared) == 22 and len(notices["notices"]) == 22 and len(tuples) == 22,
        {"undeclared": len(undeclared), "notices": len(notices["notices"]),
         "distinctTuples": len(tuples)})
H.check("both-workspace-roots-survive-in-typed-fields",
        {"apps/a", "apps/b"} == {n["workspaceRoot"] for n in notices["notices"]})
H.check("the-ownership-tuple-is-typed-and-never-concatenated",
        all(set(n) == {"code", "capabilityId", "languageMode", "workspaceRoot", "remedy"}
            for n in notices["notices"])
        and not any("@" in n["workspaceRoot"] for n in notices["notices"]))
H.check("every-notice-carries-the-single-condition-code",
        {n["code"] for n in notices["notices"]} == {"native.capability-unavailable"})
H.check("noticeCount-equals-the-array-length-exactly",
        notices["noticeCount"] == len(notices["notices"]))
H.check("the-notice-order-is-the-selection-own-order",
        [ (n["capabilityId"], n["workspaceRoot"]) for n in notices["notices"] ]
        == [ (u["capabilityId"], u["workspaceRoot"]) for u in undeclared ])

# every notice admits through the REAL schema
H.check("every-notice-admits-through-the-real-notice-schema",
        all(admits(COMMON, "#/$defs/CapabilityAvailabilityNoticeV1", n)
            for n in notices["notices"]))
H.check("a-step-entry-admits-through-the-real-step-schema",
        admits(COMMON, "#/$defs/CapabilityAvailabilityStepV1", dict(notices, stepId=0)))
inv = N.invocation_availability([(0, undeclared)])
H.check("the-invocation-collection-admits-through-the-real-invocation-schema",
        admits(COMMON, "#/$defs/CapabilityAvailabilityV1", inv))
H.check("workspaceRoot-is-a-UserInputPath-not-a-BoundedText",
        COMMON_SCHEMA["$defs"]["CapabilityAvailabilityNoticeV1"]["properties"]
        ["workspaceRoot"]["$ref"].endswith("UserInputPath"))

# a notice whose ownership tuple is incomplete must refuse
for missing in ("capabilityId", "languageMode", "workspaceRoot"):
    bad = {k: v for k, v in notices["notices"][0].items() if k != missing}
    H.check("an-incomplete-ownership-tuple-refuses--missing-" + missing,
            not admits(COMMON, "#/$defs/CapabilityAvailabilityNoticeV1", bad))
H.check("a-notice-carrying-a-foreign-code-refuses",
        not admits(COMMON, "#/$defs/CapabilityAvailabilityNoticeV1",
                   dict(notices["notices"][0], code="CONFIG.INVALID")))

# ===================== 3. invocation-versus-step bounds, exactly
step_max = COMMON_SCHEMA["$defs"]["CapabilityAvailabilityStepV1"]["properties"]["notices"]["maxItems"]
inv_max = COMMON_SCHEMA["$defs"]["CapabilityAvailabilityV1"]["properties"]["steps"]["maxItems"]
req_max = M.SCHEMA["$defs"]["analysis-spec"]["properties"]["requestedCapabilities"]["maxItems"]
H.check("the-step-notice-bound-equals-the-analysis-spec-request-bound",
        step_max == req_max == 1024, {"stepMax": step_max, "requestMax": req_max})
H.check("the-invocation-step-bound-is-64-the-StepId-range",
        inv_max == 64, {"stepsMax": inv_max})

# The case one flat array refused: two steps of 1023 notices compose 2046.
row = undeclared[0]
big = [dict(row, workspaceRoot="r%05d" % i) for i in range(1023)]
two_step = N.invocation_availability([(0, big), (1, big)])
H.check("two-steps-of-1023-notices-compose-2046-without-discarding-any",
        two_step["totalNoticeCount"] == 2046
        and sum(len(s["notices"]) for s in two_step["steps"]) == 2046,
        {"total": two_step["totalNoticeCount"]})
H.check("the-2046-notice-invocation-still-admits-through-the-real-schema",
        admits(COMMON, "#/$defs/CapabilityAvailabilityV1", two_step))
H.check("totalNoticeCount-is-the-exact-sum-of-the-step-counts",
        two_step["totalNoticeCount"] == sum(s["noticeCount"] for s in two_step["steps"]))
H.check("stepCount-is-the-exact-number-of-step-entries",
        two_step["stepCount"] == len(two_step["steps"]) == 2)

# a step over its own bound, and an invocation over the step bound, must refuse
H.check("a-forced-oversized-step-refuses-at-the-schema",
        not admits(COMMON, "#/$defs/CapabilityAvailabilityStepV1",
                   {"stepId": 0, "noticeCount": 1025,
                    "notices": [dict(notices["notices"][0], workspaceRoot="r%05d" % i)
                                for i in range(1025)]}))
H.check("a-65-step-invocation-refuses-at-the-schema",
        not admits(COMMON, "#/$defs/CapabilityAvailabilityV1",
                   {"stepCount": 65, "totalNoticeCount": 0,
                    "steps": [{"stepId": i, "noticeCount": 0, "notices": []}
                              for i in range(65)]}))
H.check("a-stepId-of-64-refuses-at-the-schema",
        not admits(COMMON, "#/$defs/CapabilityAvailabilityStepV1",
                   {"stepId": 64, "noticeCount": 0, "notices": []}))

# a step that selected and found nothing contributes an EMPTY array, not no entry
empty = N.invocation_availability([(3, [])])
H.check("a-step-that-found-nothing-absent-contributes-an-empty-array-entry",
        empty["stepCount"] == 1 and empty["steps"][0]["notices"] == []
        and empty["steps"][0]["stepId"] == 3)
H.check("an-invocation-with-no-selecting-step-is-an-empty-but-valid-account",
        admits(COMMON, "#/$defs/CapabilityAvailabilityV1",
               N.invocation_availability([])))

# =========================== 4. no live mirror presents the superseded full route
route = NATIVE_SCHEMAS
carrier = None
for path in ("x-opensip-public-route-registry",):
    pass


def find_carrier(o):
    if isinstance(o, dict):
        if "operationalCarrier" in o and isinstance(o["operationalCarrier"], str) \
                and "capability-unavailable" in json.dumps(o.get("route", o)):
            return o["operationalCarrier"]
        for v in o.values():
            r = find_carrier(v)
            if r:
                return r
    elif isinstance(o, list):
        for v in o:
            r = find_carrier(v)
            if r:
                return r
    return None


carrier = find_carrier(route)
H.check("the-route-annotation-was-located", carrier is not None)
if carrier:
    H.check("the-route-annotation-names-the-ORIGINAL-invocation-carrier",
            "CommandEnvelope.availability" in carrier
            and "ORIGINAL invocation" in carrier)
    H.check("the-route-annotation-names-the-complete-typed-ownership-tuple",
            all(k in carrier for k in ("capabilityId", "languageMode", "workspaceRoot")))
    H.check("the-route-annotation-limits-rather-than-presents-the-superseded-carrier",
            "neither is this route" in carrier
            and "DoctorResult" in carrier and "StepTermination" in carrier)
    H.check("the-route-annotation-keeps-the-existing-code-and-advisory-authority",
            "native.capability-unavailable" in json.dumps(route))

# admission section 1.1 prose
H.check("admission-1.1-names-CommandEnvelope.availability-as-the-carrier",
        "CommandEnvelope.availability" in ADMISSION_MD)
H.check("admission-1.1-delivers-in-the-invocation-that-selected-it",
        "in the invocation" in ADMISSION_MD and "that selected it" in ADMISSION_MD)
H.check("admission-1.1-carries-the-complete-typed-ownership-tuple",
        "ownership tuple in typed fields" in ADMISSION_MD
        and "`workspaceRoot`" in ADMISSION_MD)
H.check("admission-1.1-names-the-superseded-carriers-only-to-repudiate-them",
        "Earlier\nrevisions of this paragraph named" in ADMISSION_MD
        or "Earlier revisions of this paragraph named" in ADMISSION_MD.replace("\n", " "))
H.check("admission-1.1-no-longer-presents-doctor-or-StepTermination-as-the-route",
        "delivered publicly as a\n`DomainDetail`" not in ADMISSION_MD
        and "through\n`DoctorResult.defects[]` or `StepTermination.domainDetail`" not in ADMISSION_MD)
H.check("admission-1.1-preserves-the-advisory-authority-limit",
        "it terminates nothing" in ADMISSION_MD
        and "mints no Coverage" in ADMISSION_MD)
H.check("admission-1.1-does-not-claim-the-release-registry-fixes-request-scope",
        "does **not** fix the request" in ADMISSION_MD.replace("\n", " "))
H.check("admission-1.1-names-every-analysis-command-not-a-fixed-list",
        "every** `requestClass: analysis` command" in ADMISSION_MD.replace("\n", " "))

# native 1.4 prose
H.check("native-1.4-names-release_absence_notices-as-the-leaf-carrier",
        "release_absence_notices" in NATIVE_MD)
H.check("native-1.4-names-CapabilityAvailabilityStepV1",
        "CapabilityAvailabilityStepV1" in NATIVE_MD)
H.check("native-1.4-names-CommandEnvelope.availability",
        "CommandEnvelope.availability" in NATIVE_MD)

# workflows section 8 prose
H.check("workflows-8-carries-the-availability-const-code",
        "native.capability-unavailable" in WORKFLOWS_MD)
H.check("workflows-8-treats-the-code-as-a-const-of-the-typed-record",
        "a `const`" in WORKFLOWS_MD)

# The decisive negative, swept over ALL live normative surfaces: no live file may
# still present doctor/StepTermination as THE delivery route for this absence.
LIVE = ["docs/v2/contracts/product-v1/native-evidence.md",
        "docs/v2/contracts/product-v1/admission-and-qualification.md",
        "docs/v2/contracts/product-v1/workflows-and-surfaces.md",
        "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
        "docs/coop/design-corrections/native/native_evidence_model.v2.py",
        "docs/coop/design-corrections/workflows/schemas/common.schema.json"]
SUPERSEDED_AS_ROUTE = [
    "delivered publicly as a `DomainDetail`",
    "through `DoctorResult.defects[]` or `StepTermination.domainDetail`",
    "DoctorResult.defects[] for an environment report, or StepTermination.domainDetail on the step",
]
for rel in LIVE:
    text = " ".join((SUBJ / rel).read_text().split())
    hits = [p for p in SUPERSEDED_AS_ROUTE if p in text]
    H.check("no-live-mirror-presents-the-superseded-carrier-as-the-full-route--"
            + rel.rsplit("/", 1)[-1], not hits, {"hits": hits})

# ============================ 5. all FIVE analysis commands declare the parity
cmds = INVENTORY["commands"] if isinstance(INVENTORY, dict) else INVENTORY
analysis = [c for c in cmds if c.get("requestClass") == "analysis"]
H.check("there-are-exactly-five-analysis-commands", len(analysis) == 5,
        {"names": [c["name"] for c in analysis]})
H.check("all-five-analysis-commands-declare-capability-availability-parity",
        all("capability-availability" in c["parityFields"] for c in analysis),
        {"missing": [c["name"] for c in analysis
                     if "capability-availability" not in c["parityFields"]]})
# ATTEMPT 1 asserted every analysis command declares all four of
# human/json/sarif/html. That expectation was MINE and it was wrong: the
# published rule is that a DECLARED format must be applicable to the request
# class, not that every applicable format must be declared. `fit` declares no
# sarif and `repair-verify` no html. Both are unchanged from v14 and lawful.
RENDERERS = {r["format"]: r for r in INVENTORY["renderers"]}
H.check("every-declared-format-of-every-analysis-command-is-applicable-to-analysis",
        all(c["requestClass"] in RENDERERS[f]["applicability"]
            for c in analysis for f in c["formats"]))
H.check("the-availability-parity-reaches-every-format-each-analysis-command-declares",
        all("capability-availability" in c["parityFields"] and c["formats"]
            for c in analysis))
H.check("across-the-five-analysis-commands-the-parity-reaches-all-five-formats",
        {f for c in analysis for f in c["formats"]}
        == {"human", "json", "sarif", "html", "agent"},
        {"union": sorted({f for c in analysis for f in c["formats"]})})
H.check("the-two-commands-that-decline-an-applicable-format-do-so-by-declaration",
        {c["name"] for c in analysis if "sarif" not in c["formats"]} == {"fit"}
        and {c["name"] for c in analysis if "html" not in c["formats"]} == {"repair-verify"},
        {"note": "unchanged from v14; outside this delta"})
H.check("no-non-analysis-command-silently-carries-the-availability-parity",
        all("capability-availability" not in c.get("parityFields", [])
            for c in cmds if c.get("requestClass") != "analysis"))
H.check("availability-is-an-optional-field-of-the-envelope-not-a-required-one",
        "availability" in ENVELOPE_SCHEMA["properties"]
        and "availability" not in ENVELOPE_SCHEMA.get("required", []))

# ================== 6. candidate-only capabilities fabricate nothing
matrix = N.CAPABILITY_MATRIX
cand_only = [c for c in matrix["capabilities"] if not c["relations"]]
H.check("candidate-only-capabilities-are-exactly-clones-near-and-clones-cross-tsjs",
        sorted(c["id"] for c in cand_only) == ["clones-cross-tsjs", "clones-near"],
        {"ids": sorted(c["id"] for c in cand_only)})
H.check("candidate-only-capabilities-declare-no-relations-at-all",
        all(c["relations"] == [] for c in cand_only))
H.check("candidate-only-capabilities-carry-no-fact-authority",
        all(c.get("authority") != "fact" for c in cand_only),
        {"authorities": {c["id"]: c.get("authority") for c in cand_only}})
cand_absences = [u for u in undeclared if u["capabilityId"] in
                 {c["id"] for c in cand_only}]
H.check("a-candidate-only-absence-projects-to-selection-account-only",
        cand_absences and all(u["projection"] == "selection-account-only"
                              for u in cand_absences),
        {"n": len(cand_absences)})
H.check("a-candidate-only-absence-names-no-relation-at-rung",
        all(u["relations"] == [] for u in cand_absences))
H.check("a-candidate-only-absence-fabricates-no-coverage-fact-or-candidate",
        not any(k in json.dumps(cand_absences).lower()
                for k in ("\"candidate\"", "coverage2", "fact2")))
fact_absences = [u for u in undeclared if u["capabilityId"] not in
                 {c["id"] for c in cand_only}]
H.check("a-fact-producing-absence-still-projects-onto-its-coverage-entry",
        fact_absences and all(u["projection"] == "coverage-entry"
                              for u in fact_absences))
H.check("the-availability-notice-itself-grants-no-control-or-repair-authority",
        all(set(n) == {"code", "capabilityId", "languageMode", "workspaceRoot", "remedy"}
            for n in notices["notices"])
        and "candidate" not in json.dumps(notices).lower())

exit_code = H.report(
    str(pathlib.Path(__file__).resolve().parent.parent /
        "evidence/probe-availability-carrier.json"),
    "capability-availability carrier agreement across every surface",
    ["Reference-model and document evidence only. No renderer, CLI or host "
     "executes, so 'reaches human/SARIF/HTML/agent' is verified as a DECLARED "
     "parity field of the command inventory, not as observed rendered output.",
     "The prose checks are substring assertions over the frozen normative "
     "bytes; they establish what the documents say, not that an implementation "
     "obeys them.",
     "Notice ORDER is asserted against the selection's own order as produced by "
     "the reference default selection, not against a real discovery order."])
sys.exit(1 if exit_code else 0)
