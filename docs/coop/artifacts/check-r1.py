#!/usr/bin/env python3
"""Retained executable checker for the R-1 execution-core conformance contract.

Two criticals shaped this file:

  B-R1V12-01  the CORE minted an identity that admission owns, so retries and
              concurrent identical requests collided. The repair is subtle
              because ExecutionId must satisfy two opposed requirements at once:
              DISTINCT per attempt, so a crash can name a specific orphan (EC-6),
              and ABSENT from EvidenceDigest, so a retry is comparable to the
              original. Those are compatible only if it is injected metadata and
              never an input.
  B-R1V12-02  "the core reaches no ambient authority" either fails for every real
              core — it must read a snapshot somehow — or stops at an interface
              and proves nothing about production authority. Third recurrence of
              the absence-from-signature error, so R1-CAP refuses any
              exhaustiveness claim and requires the analysis boundary be stated.

  R1-ID     ExecutionId is host-allocated, injected, distinct, and digest-invariant
  R1-CAP    boundary-aware capability rules; no exhaustiveness claim; limits stated
  R1-FACT   a factoring is CHOSEN and the core runs only no-effect stages (C-2)
  R1-RET    CoreCompletion is a total union; the core never seals or terminates
  R1-SUITE  suites are split and no suite's failure is read as another's evidence
  R1-DIS    no property is discharged by a non-implementable test
  R1-FREEZE v1 is one-shot-only; residency and runtime denial stay parked

Usage: python3 artifacts/check-r1.py [contract]   ·   --selftest
Exit:  0 clean · 1 findings · 2 IO error
"""
from __future__ import annotations
import copy, json, sys, pathlib

BINDING = "r1-lifetime-neutrality.conformance.v1.4.json"
CLOSURE = "r1-lifetime-neutrality.freeze-closure-coordinator.v1.json"
C2 = "c2-plan-stage-schema.v3.json"
FP = "fact-plane.v1.json"
HERE = pathlib.Path(__file__).resolve().parent
NO_EFFECT_KINDS = {"rule-evaluation", "policy-evaluation"}
SEALED_STAGE_INPUT_FIELDS = {
    "observationSet", "targetUniverseId", "coverageContext", "planStageIds",
}
ATTEMPT_METADATA_FIELDS = {"executionId"}


def load(n):
    p = HERE / n
    return json.loads(p.read_text()) if p.exists() else None


def _closed_record_errors(value: dict, schema: dict, missing_outcome: str) -> list[str]:
    if not isinstance(value, dict):
        return [missing_outcome]
    required = set(schema.get("required", []))
    optional = set(schema.get("optional", []))
    if set(value) - required - optional:
        return [schema.get("unknownFieldOutcome") or "UNKNOWN_FIELD"]
    if required - set(value):
        return [missing_outcome]
    return []


def check(c: dict, c2, fp, closure: dict | None = None) -> list[str]:
    f: list[str] = []

    # ---- R1-ID ----
    io = c.get("identityOwnership")
    if not io:
        f.append("R1-ID: no identity ownership rule — the core may mint an ExecutionId "
                 "that admission owns (B-R1V12-01)")
    else:
        if "HOST" not in io.get("rule", "").upper():
            f.append("R1-ID: ExecutionId is not host-allocated")
        if "EvidenceDigest" not in io.get("mustNotAffect", ""):
            f.append("R1-ID: nothing forbids ExecutionId from reaching EvidenceDigest, so "
                     "a retry would be incomparable to the original")
        if "contentDerivedIdentity" not in io:
            f.append("R1-ID: no separate content-derived identity is defined, so the "
                     "attempt anchor would be pressed into that role")
    ln13 = next((t for t in c["conformanceTests"] if t["id"] == "LN-13"), None)
    if ln13 is None:
        f.append("R1-ID: LN-13 is absent — the digest-invariance of ExecutionId is untested")
    else:
        a = ln13["assert"]
        if "identical EvidenceDigest" not in a.replace("byte-", ""):
            f.append("R1-ID: LN-13 does not assert digest invariance")
        if "distinct" not in a:
            f.append("R1-ID: LN-13 does not assert ExecutionIds are distinct — without "
                     "that, a crash cannot name a specific orphan (EC-6)")

    # ---- R1-INPUT: RequestContext cannot enter the pure serialized boundary ----
    core_api = c.get("coreApi") or {}
    stage_schema = core_api.get("sealedStageInput") or {}
    attempt_schema = core_api.get("attemptMetadata") or {}
    if stage_schema.get("closed") is not True or \
            stage_schema.get("additionalProperties") is not False or \
            set(stage_schema.get("contains", [])) != SEALED_STAGE_INPUT_FIELDS or \
            set(stage_schema.get("required", [])) != SEALED_STAGE_INPUT_FIELDS or \
            stage_schema.get("optional") != [] or \
            set(stage_schema.get("fields", {})) != SEALED_STAGE_INPUT_FIELDS or \
            stage_schema.get("unknownFieldOutcome") != "CORE_STAGE_INPUT_UNKNOWN_FIELD":
        f.append("R1-INPUT: SealedStageInput is not the exact closed serialized record")
    if attempt_schema.get("closed") is not True or \
            attempt_schema.get("additionalProperties") is not False or \
            set(attempt_schema.get("required", [])) != ATTEMPT_METADATA_FIELDS or \
            attempt_schema.get("optional") != [] or \
            attempt_schema.get("unknownFieldOutcome") != \
            "CORE_ATTEMPT_METADATA_UNKNOWN_FIELD":
        f.append("R1-INPUT: AttemptMetadata is not exact/closed over ExecutionId only")
    completion_attempt = (c.get("coreCompletionSchema") or {}).get("AttemptMetadata") or {}
    if completion_attempt.get("closed") is not True or \
            completion_attempt.get("additionalProperties") is not False or \
            set(completion_attempt.get("required", [])) != ATTEMPT_METADATA_FIELDS or \
            completion_attempt.get("optional") != [] or \
            completion_attempt.get("unknownFieldOutcome") != \
            "CORE_ATTEMPT_METADATA_UNKNOWN_FIELD" or \
            completion_attempt.get("aliasOf") != "coreApi.attemptMetadata":
        f.append("R1-INPUT: duplicate AttemptMetadata schema drifted from coreApi")
    fixtures = {item.get("id"): item for item in c.get("sealedStageInputFixtures", [])}
    expected_negative = {
        "sealed-stage-input-reject-request-id": "CORE_STAGE_INPUT_UNKNOWN_FIELD",
        "sealed-stage-input-reject-unknown-field": "CORE_STAGE_INPUT_UNKNOWN_FIELD",
        "attempt-metadata-reject-request-id": "CORE_ATTEMPT_METADATA_UNKNOWN_FIELD",
    }
    if {key: fixtures.get(key, {}).get("expected") for key in expected_negative} != \
            expected_negative:
        f.append("R1-INPUT: RequestId/unknown-field fixture set or outcomes are not exact")
    positive = fixtures.get("sealed-stage-input-valid-minimal") or {}
    base_stage = positive.get("stageInput") or {}
    base_attempt = positive.get("attemptMetadata") or {}
    if positive.get("valid") is not True or \
            _closed_record_errors(base_stage, stage_schema, "CORE_STAGE_INPUT_MISSING_FIELD") or \
            _closed_record_errors(base_attempt, attempt_schema,
                                  "CORE_ATTEMPT_METADATA_MISSING_FIELD"):
        f.append("R1-INPUT: minimal serialized core input fixture is not valid")
    for fixture_id, expected in expected_negative.items():
        fixture = fixtures.get(fixture_id) or {}
        target = fixture.get("target")
        candidate = copy.deepcopy(base_stage if target == "stageInput" else base_attempt)
        candidate.update(fixture.get("addField") or {})
        schema = stage_schema if target == "stageInput" else attempt_schema
        missing = "CORE_STAGE_INPUT_MISSING_FIELD" if target == "stageInput" else \
            "CORE_ATTEMPT_METADATA_MISSING_FIELD"
        if fixture.get("valid") is not False or \
                _closed_record_errors(candidate, schema, missing) != [expected]:
            f.append(f"R1-INPUT {fixture_id}: unknown field is not rejected exactly")

    # ---- R1-CAP ----
    cap = c.get("capabilityBoundary")
    if not cap:
        f.append("R1-CAP: no capability boundary (B-R1V12-02)")
    else:
        for part in ("part1", "part2"):
            if part not in cap:
                f.append(f"R1-CAP: {part} missing — the core boundary and the adapter "
                         f"tests are separate obligations")
        if "honestLimit" not in cap:
            f.append("R1-CAP: no honest limit stated, so analysing to the port boundary "
                     "reads as proving adapter authority too")
    ab = c.get("analysisBoundary")
    if not ab:
        f.append("R1-CAP: no analysis boundary — the third recurrence of claiming absence "
                 "from an instrument that cannot see it (B-R1V12-05)")
    else:
        if not ab.get("limits"):
            f.append("R1-CAP: the analysis boundary states no limits")
        if "noExhaustivenessClaim" not in ab:
            f.append("R1-CAP: no explicit refusal of an exhaustiveness claim")
        if len(ab.get("instruments", [])) < 3:
            f.append("R1-CAP: too few instruments for the boundary claim to be meaningful")
        boundary_rule = ab.get("rule", "").lower()
        if "denied by construction" in boundary_rule or "not claimed" not in boundary_rule:
            f.append("R1-CAP: analysisBoundary turns a static/package rule into runtime "
                     "denial instead of TCB acceptance or v1 exclusion")

    # ---- R1-FACT: the core runs only stages C-2 says hold no effect authority ----
    fac = c.get("factoring")
    if not fac or not fac.get("chosen"):
        f.append("R1-FACT: no factoring is chosen, so the core either cannot run a Plan or "
                 "relies on unlisted orchestration authority (B-R1V12-03)")
    elif c2:
        kinds = c2["stageSchemas"]["kinds"]
        core_text = " ".join(fac.get("coreExecutes", []))
        for kind, spec in kinds.items():
            no_effect = spec.get("effectClass") == "no-effect"
            in_core = kind in core_text
            if no_effect and not in_core:
                f.append(f"R1-FACT: C-2 declares '{kind}' no-effect but the core does not "
                         f"execute it — the pure core is smaller than it could be")
            if not no_effect and in_core:
                f.append(f"R1-FACT: the core executes '{kind}', which C-2 declares "
                         f"effectful — lifetime neutrality would be a property of the "
                         f"supervisor, not the core")
        if "never calls back out" not in fac.get("interface", ""):
            f.append("R1-FACT: the core may call back out, which reintroduces the "
                     "orchestration authority B-R1V12-03 named")
    else:
        f.append(f"R1-FACT: could not load {C2} — the effect classes are unverified")

    # ---- R1-RET ----
    cc = c.get("coreCompletionSchema")
    if not cc:
        f.append("R1-RET: no typed CoreCompletion (B-R1V12-06)")
    else:
        variants = {v["variant"] for v in cc["variants"]}
        for need in ("completed", "incomplete", "cancelled", "faulted"):
            if need not in variants:
                f.append(f"R1-RET: CoreCompletion has no '{need}' variant, so that outcome "
                         f"has no truthful return value")
        if "NEVER seals" not in cc.get("rule", "") and "never seal" not in cc.get("rule", "").lower():
            f.append("R1-RET: nothing forbids the core from sealing a Run or mapping a "
                     "termination (D9 TO-2/TO-3)")
    if fp:
        vocab = set(fp["deficiencyVocabulary"]["values"])
        note = " ".join(v.get("note", "") for v in (cc or {}).get("variants", []))
        if "fact-plane" not in note:
            f.append("R1-RET: the incomplete variant does not reuse the fact-plane "
                     "deficiency vocabulary, so a new Coverage vocabulary would appear")

    # ---- identity + completion fixtures: the two repairs must be derivable ----
    for fx in c["identityFixtures"]:
        ids = fx["executionIds"]
        distinct = len(set(ids)) == len(ids)
        want_equal = fx["semanticInputs"] == "identical"
        conforms = distinct and (fx["expectDigestEqual"] == want_equal)
        if fx["valid"] and not conforms:
            f.append(f"R1-ID {fx['id']}: expected valid but distinct={distinct}, "
                     f"digestEqual={fx['expectDigestEqual']} for {fx['semanticInputs']} "
                     f"inputs")
        elif not fx["valid"] and conforms:
            f.append(f"R1-ID {fx['id']}: expected REJECTION ({fx.get('violates')}) but the "
                     f"assignment conforms")
    variants = {v["variant"] for v in (cc or {}).get("variants", [])}
    for fx in c["completionFixtures"]:
        bad = fx["variant"] not in variants or fx.get("seals")
        if fx["valid"] and bad:
            f.append(f"R1-RET {fx['id']}: expected valid but variant "
                     f"'{fx['variant']}' unknown or it seals")
        elif not fx["valid"] and not bad:
            f.append(f"R1-RET {fx['id']}: expected REJECTION ({fx.get('violates')}) but it "
                     f"validated")
    for v in variants:
        if not any(fx["valid"] and fx["variant"] == v for fx in c["completionFixtures"]):
            f.append(f"R1-RET: variant '{v}' has no positive fixture")

    # ---- R1-SUITE ----
    su = c.get("suites")
    if not su:
        f.append("R1-SUITE: suites are not split (B-R1V12-04)")
    else:
        assigned = {t for s in su["split"] for t in s["tests"]}
        declared = {t["id"] for t in c["conformanceTests"]}
        for t in declared - assigned:
            f.append(f"R1-SUITE: test {t} belongs to no suite")
        for t in assigned - declared:
            f.append(f"R1-SUITE: suite names unknown test {t}")
        for t in c["conformanceTests"]:
            if "suite" not in t:
                f.append(f"R1-SUITE: {t['id']} declares no suite")
        if "may NOT be read as evidence about another" not in su.get("rule", ""):
            f.append("R1-SUITE: nothing forbids reading one suite's failure as evidence "
                     "about another — the vacuity B-R1V12-04 named")

    # ---- PO-01 must be gone ----
    for po in c.get("productObligationsNotClosedHere", []):
        if po.get("id") == "PO-01" and "REMOVED" not in po.get("status", "").upper():
            f.append("R1-SUITE: PO-01 still carries a deployment obligation, bypassing the "
                     "v1 one-shot exclusion rather than resolving it (B-R1V12-07)")

    # ---- R1-DIS ----
    impl = {t["id"]: t.get("implementable", False) for t in c["conformanceTests"]}
    dis_rule = c.get("dischargeStatus", {}).get("rule", "")
    if "implementable:true is feasibility metadata only" not in dis_rule:
        f.append("R1-DIS: discharge rule does not state that implementable:true is "
                 "feasibility metadata only (R2-R1-04 / R2-FINAL-02)")
    for prop in c["dischargeStatus"]["properties"]:
        links = prop.get("dischargedBy", [])
        for tid in links:
            if tid not in impl:
                f.append(f"R1-DIS: '{prop['property']}' names unknown test '{tid}'")
            elif not impl[tid]:
                f.append(f"R1-DIS: '{prop['property']}' is discharged by '{tid}', which is "
                         f"not implementable — a paper seal")
        if prop["status"] != "DISCHARGED" and links:
            if prop.get("specifiedBy") != links:
                f.append(f"R1-DIS: '{prop['property']}' uses legacy dischargedBy links "
                         f"without an identical specifiedBy alias")
        if prop["status"] == "DISCHARGED" and not links:
            f.append(f"R1-DIS: '{prop['property']}' claims DISCHARGED with no tests")
        if prop["status"] == "DISCHARGED":
            if prop.get("evidenceGrade") != "DEMONSTRATED":
                f.append(f"R1-DIS: '{prop['property']}' is DISCHARGED without "
                         f"DEMONSTRATED evidenceGrade (R2-R1-04 / R2-FINAL-02)")
            if not prop.get("demonstrationEvidenceIds"):
                f.append(f"R1-DIS: '{prop['property']}' is DISCHARGED without retained "
                         f"demonstrationEvidenceIds (R2-FINAL-02)")
    for t in c["conformanceTests"]:
        if not t.get("implementable") and not (t.get("requiresHarness")
                                               or t.get("requiresMechanism")):
            f.append(f"R1-DIS: {t['id']} is not implementable and names no blocker")

    # ---- R1-BOUND: single core definition (R2-R1-01) ----
    ecb = c.get("executionCoreBoundary") or {}
    defn = ecb.get("definition", "")
    if "SealedRun" in defn and "does NOT produce a SealedRun" not in defn:
        f.append("R1-BOUND: executionCoreBoundary.definition still says the core produces "
                 "a SealedRun (R2-R1-01)")
    if "fact derivation" in defn.lower() and "does NOT" not in defn:
        f.append("R1-BOUND: definition still assigns fact derivation to the core (R2-R1-01)")
    inside_blob = json.dumps(ecb.get("inside", [])).lower()
    if "fact derivation" in inside_blob:
        f.append("R1-BOUND: inside authorities still include fact derivation (R2-R1-01)")
    if fac and "CoreCompletion" not in fac.get("interface", ""):
        f.append("R1-BOUND: factoring.interface does not return CoreCompletion")
    # definition must not contradict factoring
    if fac and "PURE EVALUATION CORE" in fac.get("chosen", "").upper():
        if "pure evaluation" not in defn.lower() and "CoreCompletion" not in defn:
            f.append("R1-BOUND: pure-core factoring chosen but definition does not describe "
                     "a pure evaluation CoreCompletion boundary (R2-R1-01)")

    # ---- R1-DEPS: no effectful ports / no entropy (R2-R1-02, R2-R1-06) ----
    cap = c.get("capabilityBoundary") or {}
    cap_blob = json.dumps(cap)
    if "StorePort" in cap_blob and "forbids" not in cap_blob.lower() and "forbidden" not in json.dumps(cap.get("part1", {})).lower():
        # permitted must not include StorePort
        perm = json.dumps((cap.get("part1") or {}).get("permitted", ""))
        if "StorePort" in perm or "ProviderPort" in perm or "SnapshotPort" in perm:
            f.append("R1-DEPS: capabilityBoundary still permits effectful ports "
                     "(SnapshotPort/StorePort/ProviderPort) (R2-R1-02)")
    part1 = cap.get("part1") or {}
    perm = str(part1.get("permitted", ""))
    for port in ("SnapshotPort", "StorePort", "ProviderPort"):
        if port in perm:
            f.append(f"R1-DEPS: part1.permitted includes {port} (R2-R1-02)")
    deps = cap.get("coreDepsSchema")
    if not isinstance(deps, dict):
        f.append("R1-DEPS: coreDepsSchema is absent — CoreDeps authority is undefined (R2-R1-02)")
    else:
        forb = json.dumps(deps.get("forbids", [])).lower()
        for need in ("entropy", "network", "filesystem", "storage"):
            if need not in forb:
                f.append(f"R1-DEPS: coreDepsSchema.forbids omits '{need}'")
    inj = json.dumps(ecb.get("injectedNotAmbient", [])).lower()
    if "entropy" in inj and "no entropy" not in inj and "never" not in inj:
        f.append("R1-DEPS: executionCoreBoundary still injects an entropy source (R2-R1-06)")
    if not (c.get("identityOwnership") or {}).get("noEntropyInCore"):
        f.append("R1-DEPS: identityOwnership.noEntropyInCore is not true (R2-R1-06)")

    # ---- R1-POL: policy outcome on completion (R2-R1-03) ----
    cc = c.get("coreCompletionSchema") or {}
    completed = next((v for v in cc.get("variants", []) if v.get("variant") == "completed"), None)
    if not completed:
        f.append("R1-POL: no completed variant")
    else:
        carries = completed.get("carries") or []
        if "policyOutcome" not in carries:
            f.append("R1-POL: completed CoreCompletion omits policyOutcome (R2-R1-03)")
        po = completed.get("policyOutcome") or {}
        for fld in ("policyId", "verdict", "derivationDigest"):
            if fld not in json.dumps(po):
                f.append(f"R1-POL: policyOutcome schema omits '{fld}' (R2-R1-03)")

    # ---- R1-SUITE composition (R2-R1-05) ----
    su = c.get("suites") or {}
    split = su.get("split") or []
    suite_names = {s.get("suite") for s in split}
    if "composition-acceptance" not in suite_names:
        f.append("R1-SUITE: composition-acceptance suite missing (R2-R1-05)")
    ln10 = next((t for t in c["conformanceTests"] if t["id"] == "LN-10"), None)
    if ln10 and ln10.get("suite") != "composition-acceptance":
        f.append("R1-SUITE: LN-10 is not in composition-acceptance (R2-R1-05)")
    # structural: suite field on tests must match split assignment
    assigned = {}
    for s in split:
        for tid in s.get("tests", []):
            assigned[tid] = s.get("suite")
    for t in c["conformanceTests"]:
        if t["id"] in assigned and t.get("suite") != assigned[t["id"]]:
            f.append(f"R1-SUITE: {t['id']} declares suite '{t.get('suite')}' but split "
                     f"assigns '{assigned[t['id']]}'")

    # ---- paper CLOSED via LN-12 (R2-R1-04) ----
    for fid, text_d in (c.get("priorFindingDispositions") or {}).items():
        if "CLOSED by" in text_d and "LN-12" in text_d and "NOT CLOSED by LN-12" not in text_d:
            f.append(f"R1-DIS: priorFindingDispositions[{fid}] claims CLOSED by LN-12 which "
                     f"is unimplementable (R2-R1-04)")

    # ---- topology floor (R2-R1-07) ----
    topo = c.get("initialTopology")
    if not isinstance(topo, dict) or not topo.get("normativeFloor"):
        f.append("R1-TOPO: initialTopology.normativeFloor is absent — week-one process "
                 "topology is undecided (R2-R1-07)")
    elif "one-shot" not in topo["normativeFloor"].lower():
        f.append("R1-TOPO: normativeFloor does not choose a one-shot host floor (R2-R1-07)")

    # ---- R1-FREEZE: coordinator scope closure is load-bearing ----
    if closure is None:
        f.append(f"R1-FREEZE: could not load {CLOSURE} — v1 scope/exclusions unverified")
    else:
        if closure.get("sealRecommendation", {}).get("verdict") != "SEAL-WITH-CHANGES":
            f.append("R1-FREEZE: coordinator verdict is not SEAL-WITH-CHANGES")
        arch = closure.get("v1Architecture") or {}
        initial = str(arch.get("initialTopology", "")).lower()
        if "one-shot" not in initial or "pure" not in initial:
            f.append("R1-FREEZE: closure does not bind one-shot host + pure core")
        if arch.get("coreBoundary") != c.get("coreApi", {}).get("signature"):
            f.append("R1-FREEZE: closure coreBoundary differs from the binding coreApi")
        resident = (topo or {}).get("optionalResidentHost") or {}
        if resident.get("permittedInV1") is not False:
            f.append("R1-FREEZE: initialTopology does not explicitly forbid resident mode in v1")
        exclusions = {item.get("id"): item for item in closure.get("v1Exclusions", [])}
        residency = exclusions.get("R1-PARK-RESIDENCY") or {}
        if residency.get("status") != "PARKED-OUTSIDE-V1":
            f.append("R1-FREEZE: residency is not PARKED-OUTSIDE-V1")
        runtime = exclusions.get("R1-PARK-RUNTIME-DENIAL") or {}
        if runtime.get("status") != "NOT-DISCHARGED-AND-NOT-CLAIMED-FOR-V1":
            f.append("R1-FREEZE: runtime denial is not explicitly NOT DISCHARGED")
        if runtime.get("blockedOn") != "ARCH.PROBE-CONTRACT":
            f.append("R1-FREEZE: runtime denial is not parked on ARCH.PROBE-CONTRACT")
        impl_state = closure.get("implementationEvidence", {}).get("status")
        if impl_state != "NOT-YET-DEMONSTRATED":
            f.append("R1-FREEZE: implementation evidence is not marked NOT-YET-DEMONSTRATED")
        patch = closure.get("claimRegisterPatch") or {}
        if patch.get("claimId") != "R-1":
            f.append("R1-FREEZE: closure does not target claim-register R-1")
        patch_set = patch.get("set") or {}
        if patch_set.get("sealBlockers") != []:
            f.append("R1-FREEZE: closure does not clear architecture sealBlockers")
        if len(patch_set.get("nonBlockingResiduals", [])) != 2:
            f.append("R1-FREEZE: closure must name exactly residency and runtime-denial residuals")
        if "UNREVIEWED" in c.get("status", "").upper() or "NOT REVIEWED" in c.get(
                "reviewStatus", "").upper():
            f.append("R1-FREEZE: binding metadata still says unreviewed")
        if c.get("peerReviewRequired"):
            f.append("R1-FREEZE: binding still carries unresolved peerReviewRequired entries")

    return f


# --------------------------------------------------------------------------
def _m_core_mints_id(c):
    c["identityOwnership"]["rule"] = "The core allocates an ExecutionId per evaluation."

def _m_id_in_digest(c):
    c["identityOwnership"]["mustNotAffect"] = "nothing in particular"

def _m_drop_distinctness(c):
    for t in c["conformanceTests"]:
        if t["id"] == "LN-13":
            t["assert"] = "Varying ExecutionId produces byte-identical EvidenceDigest."

def _m_exhaustive_again(c):
    del c["analysisBoundary"]["noExhaustivenessClaim"]
    c["analysisBoundary"]["limits"] = []

def _m_runtime_denial_by_construction(c):
    c["analysisBoundary"]["rule"] = (
        "Unmodelled dynamic and native paths are denied by construction.")

def _m_core_runs_effects(c):
    c["factoring"]["coreExecutes"].append("fact-derivation stages")

def _m_core_calls_out(c):
    c["factoring"]["interface"] = "The core receives a supervisor port and calls it."

def _m_drop_cancelled(c):
    c["coreCompletionSchema"]["variants"] = [
        v for v in c["coreCompletionSchema"]["variants"] if v["variant"] != "cancelled"]

def _m_core_seals(c):
    c["coreCompletionSchema"]["rule"] = "The core seals the Run and maps termination."

def _m_unsplit_suites(c):
    del c["suites"]["rule"]

def _m_restore_po01(c):
    c["productObligationsNotClosedHere"][0]["status"] = "OPEN OBLIGATION"

def _m_discharge_runtime(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"].endswith("AT RUNTIME"):
            p["dischargedBy"] = ["LN-12"]; p["status"] = "DISCHARGED"

def _m_demonstrated_without_evidence(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["status"] == "SPECIFIED":
            p["status"] = "DISCHARGED"
            p["evidenceGrade"] = "DEMONSTRATED"
            p["demonstrationEvidenceIds"] = []
            break

def _m_sealed_run_definition(c):
    c["executionCoreBoundary"]["definition"] = (
        "The execution core takes a sealed Snapshot and a validated Plan and produces a SealedRun.")

def _m_fact_derivation_inside(c):
    c["executionCoreBoundary"]["inside"] = [
        {"authority": "fact derivation, rule evaluation, policy evaluation", "why": "job"}]

def _m_permit_store_port(c):
    c["capabilityBoundary"]["part1"]["permitted"] = (
        "calls through SnapshotPort, StorePort, ProviderPort")

def _m_drop_core_deps(c):
    del c["capabilityBoundary"]["coreDepsSchema"]

def _m_drop_policy_outcome(c):
    for v in c["coreCompletionSchema"]["variants"]:
        if v["variant"] == "completed":
            v["carries"] = ["findings", "exactCoverage", "diagnosticsRef"]
            v.pop("policyOutcome", None)

def _m_ln10_host(c):
    for t in c["conformanceTests"]:
        if t["id"] == "LN-10":
            t["suite"] = "host"
    for s in c["suites"]["split"]:
        if s.get("suite") == "composition-acceptance":
            s["tests"] = [x for x in s["tests"] if x != "LN-10"]
        if s.get("suite") == "host":
            s.setdefault("tests", []).append("LN-10")

def _m_entropy_back(c):
    c["identityOwnership"]["noEntropyInCore"] = False
    c["executionCoreBoundary"]["injectedNotAmbient"].append({
        "authority": "ID and entropy source", "resolution": "INJECTED ambient random"})

def _m_close_via_ln12(c):
    c["priorFindingDispositions"]["A2-R1-01"] = (
        "CLOSED by executionCoreBoundary plus LN-11 and LN-12 (runtime denial).")

def _m_drop_topology(c):
    del c["initialTopology"]


def _m_open_sealed_stage_input(c):
    schema = c["coreApi"]["sealedStageInput"]
    schema["closed"] = False
    schema["additionalProperties"] = True


def _m_admit_request_id_to_stage_input(c):
    schema = c["coreApi"]["sealedStageInput"]
    schema["contains"].append("requestId")
    schema["required"].append("requestId")
    schema["fields"]["requestId"] = "operational RequestId"


def _m_admit_request_id_to_attempt_metadata(c):
    for schema in (c["coreApi"]["attemptMetadata"],
                   c["coreCompletionSchema"]["AttemptMetadata"]):
        schema["required"].append("requestId")


def _m_drop_stage_request_id_fixture(c):
    c["sealedStageInputFixtures"] = [
        item for item in c["sealedStageInputFixtures"]
        if item["id"] != "sealed-stage-input-reject-request-id"
    ]

MUTATIONS = [
    ("let the core mint ExecutionId (B-R1V12-01)", _m_core_mints_id),
    ("let ExecutionId reach EvidenceDigest (B-R1V12-01)", _m_id_in_digest),
    ("drop the distinctness half of LN-13 (EC-6)", _m_drop_distinctness),
    ("claim exhaustive dependency analysis again (B-R1V12-05)", _m_exhaustive_again),
    ("claim runtime denial by construction (R1-CAP)", _m_runtime_denial_by_construction),
    ("put effectful stages in the pure core (B-R1V12-03)", _m_core_runs_effects),
    ("let the core call back out (B-R1V12-03)", _m_core_calls_out),
    ("remove the cancelled outcome (B-R1V12-06)", _m_drop_cancelled),
    ("let the core seal a Run (B-R1V12-06 / D9 TO-2)", _m_core_seals),
    ("read one suite's failure as another's evidence (B-R1V12-04)", _m_unsplit_suites),
    ("restore PO-01 as an obligation (B-R1V12-07)", _m_restore_po01),
    ("discharge runtime authority with an unbuilt test (R1-DIS)", _m_discharge_runtime),
    ("claim DEMONSTRATED discharge without retained evidence (R2-FINAL-02)",
     _m_demonstrated_without_evidence),
    ("restore SealedRun core definition (R2-R1-01)", _m_sealed_run_definition),
    ("restore fact derivation inside core (R2-R1-01)", _m_fact_derivation_inside),
    ("permit effectful StorePort (R2-R1-02)", _m_permit_store_port),
    ("drop CoreDeps schema (R2-R1-02)", _m_drop_core_deps),
    ("drop policyOutcome from completion (R2-R1-03)", _m_drop_policy_outcome),
    ("move LN-10 back to host suite (R2-R1-05)", _m_ln10_host),
    ("reintroduce entropy in core (R2-R1-06)", _m_entropy_back),
    ("close finding via unimplementable LN-12 (R2-R1-04)", _m_close_via_ln12),
    ("drop initial topology floor (R2-R1-07)", _m_drop_topology),
    ("open SealedStageInput to unknown fields (R6-IP02-01)",
     _m_open_sealed_stage_input),
    ("admit RequestId into SealedStageInput (R6-IP02-01)",
     _m_admit_request_id_to_stage_input),
    ("admit RequestId into AttemptMetadata (R6-IP02-01)",
     _m_admit_request_id_to_attempt_metadata),
    ("drop SealedStageInput RequestId rejection fixture (R6-IP02-01)",
     _m_drop_stage_request_id_fixture),
]


def _m_closure_allows_resident(c):
    for item in c["v1Exclusions"]:
        if item["id"] == "R1-PARK-RESIDENCY":
            item["status"] = "OPTIONAL-IN-V1"

def _m_closure_discharges_runtime(c):
    for item in c["v1Exclusions"]:
        if item["id"] == "R1-PARK-RUNTIME-DENIAL":
            item["status"] = "DISCHARGED"

def _m_closure_drops_one_shot(c):
    c["v1Architecture"]["initialTopology"] = "resident host or one-shot host"

def _m_closure_keeps_blocker(c):
    c["claimRegisterPatch"]["set"]["sealBlockers"] = ["residency is unmeasured"]

CLOSURE_MUTATIONS = [
    ("permit resident mode inside v1 (R1-FREEZE)", _m_closure_allows_resident),
    ("paper-discharge runtime authority in closure (R1-FREEZE)",
     _m_closure_discharges_runtime),
    ("drop the one-shot-only floor from closure (R1-FREEZE)", _m_closure_drops_one_shot),
    ("leave a parked measurement as an architecture blocker (R1-FREEZE)",
     _m_closure_keeps_blocker),
]


def selftest(base, c2, fp, closure) -> int:
    pre = check(base, c2, fp, closure)
    if pre:
        print(f"REFUSING to self-test: the base contract has {len(pre)} finding(s).")
        for x in pre[:5]:
            print("  -", x)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, mut in MUTATIONS:
        c = copy.deepcopy(base)
        mut(c)
        found = check(c, c2, fp, closure)
        if not found:
            escaped += 1
        print(f"  {'reject' if found else 'ESCAPE':>6}  {name}")
        print(f"          {found[0] if found else 'NO FINDING — mutation survived'}")
    for name, mut in CLOSURE_MUTATIONS:
        candidate = copy.deepcopy(closure)
        mut(candidate)
        found = check(base, c2, fp, candidate)
        if not found:
            escaped += 1
        print(f"  {'reject' if found else 'ESCAPE':>6}  {name}")
        print(f"          {found[0] if found else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(MUTATIONS) + len(CLOSURE_MUTATIONS)} mutations ESCAPED — "
              f"the proof path is optional")
        return 1
    print(f"all {len(MUTATIONS) + len(CLOSURE_MUTATIONS)} mutations rejected — "
          f"the proof path is load-bearing")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    p = pathlib.Path(args[0]) if args else HERE / BINDING
    if not p.exists():
        print(f"missing contract: {p}", file=sys.stderr)
        return 2
    c = json.loads(p.read_text())
    c2, fp, closure = load(C2), load(FP), load(CLOSURE)
    if "--selftest" in sys.argv:
        return selftest(c, c2, fp, closure)
    f = check(c, c2, fp, closure)
    if not f:
        impl = sum(1 for t in c["conformanceTests"] if t.get("implementable"))
        print(f"R-1 OK — {p.name}, {len(c['conformanceTests'])} tests across "
              f"{len(c['suites']['split'])} suites, R1-ID / R1-INPUT / R1-CAP / R1-FACT / R1-RET / "
              f"R1-SUITE / R1-DIS / R1-FREEZE clean")
        print(f"  cross-checked against {C2}, {FP}, and {CLOSURE}")
        print(f"  {impl}/{len(c['conformanceTests'])} implementable; runtime authority is "
              f"NOT DISCHARGED; v1 is one-shot-only and future residency is parked")
        return 0
    print(f"{len(f)} finding(s) in {p.name}:")
    for x in f:
        print("  -", x)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
