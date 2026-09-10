"""Consumer-B series E: baseline audit, comparison, authorization, purge/replay
and required-output failure, as schema-validated public artifacts."""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cb_canonical as C  # noqa: E402

SUBJ = "/tmp/opensip-design-corrections/consumer-b.v1/subject"
WFS = os.path.join(SUBJ, "docs/coop/design-corrections/workflows/schemas")


def registry():
    from referencing import Registry, Resource
    docs = {}
    for f in os.listdir(WFS):
        d = json.load(open(os.path.join(WFS, f)))
        docs[d["$id"]] = d
    return (Registry().with_resources(
        [(k, Resource.from_contents(v)) for k, v in docs.items()]), docs)


REG, DOCS = registry()


def validate(ref, doc):
    from jsonschema import Draft202012Validator
    sch = {"$schema": "https://json-schema.org/draft/2020-12/schema",
           "$id": "urn:opensip:consumer-b:probe", "$ref": ref}
    return [e.message + " @" + "/".join(str(x) for x in e.path)
            for e in Draft202012Validator(sch, registry=REG).iter_errors(doc)]


CMP = "urn:opensip:product-v1:workflows:comparison-result#"
COMMON = "urn:opensip:product-v1:workflows:common#/$defs/"

H64 = lambda s: hashlib.sha256(s.encode()).hexdigest()  # noqa: E731

BASE_CTX = {
    "policyDigest": H64("policy-v1"), "scopeDigest": H64("scope-doc-v1"),
    "waiverSetDigest": H64("waivers-v1"),
    "detectorClosureIds": ["closure2:" + H64("detector-ts-1")],
    "evidenceAvailability": {
        "importKinds": ["runtime"],
        "relations": ["runtime-observation"],
        "imports": [{"kind": "runtime", "importId": "import2:" + H64("run-obs-1"),
                     "payloadDigest": H64("p1"),
                     "sourceCorrespondenceDigest": H64("c1"),
                     "scopeDigest": H64("s1"),
                     "observationDigest": H64("o1")}]}}

ZERO_COUNTS = {k: 0 for k in ["UNCHANGED", "CODE-NET-NEW", "CODE-FIXED",
                              "DETECTION-DELTA", "POLICY-DELTA", "SCOPE-DELTA",
                              "WAIVER-DELTA", "EVIDENCE-DELTA", "INDETERMINATE",
                              "gating"]}


def comparison(**over):
    d = {
        "schemaFamily": "opensip.product.comparison", "schemaMajor": 1,
        "baselineId": "baseline2:" + H64("baseline-1"),
        "currentRunId": "run2:" + H64("current-run"),
        "currentSnapshotId": "snapshot2:" + H64("current-snapshot"),
        "auditProfile": {"name": "code-regression", "gateCodeNetNew": True,
                         "gateNewlyLiveByPolicyAxes": False,
                         "gateAllCurrentLive": False,
                         "newWaiverSuppressesCodeNetNew": False,
                         "gateRuleUnder": "baseline-or-current"},
        "projectCorrespondence": "same-project", "comparisonPerformed": True,
        "baselineContext": BASE_CTX, "currentContext": BASE_CTX,
        "contextDelta": {"codeChanged": True, "detectorChanged": False,
                         "policyChanged": False, "scopeChanged": False,
                         "waiversChanged": False,
                         "evidenceAvailabilityChanged": False},
        "pivotsAvailable": {"E0": "not-needed", "E1": "not-needed",
                            "E2": "not-needed", "E3": "not-needed"},
        "detectors": [{"detectorId": "core.ts",
                       "baselineClosureId": "closure2:" + H64("detector-ts-1"),
                       "currentClosureId": "closure2:" + H64("detector-ts-1"),
                       "baselineSemanticsMajor": 2, "currentSemanticsMajor": 2,
                       "method": "identical-closure"}],
        "ruleDeficiencies": [], "entries": [], "counts": dict(ZERO_COUNTS),
        "verdict": "pass"}
    d.update(over)
    return d


def build(results):
    def rec(vid, title, sel, expect, obs, ok, extra=None):
        results.append({"id": vid, "title": title, "owningSelector": sel,
                        "expected": expect, "observed": obs, "pass": bool(ok),
                        "extra": extra or {}})

    # ---- E1 empty-result comparison that is still INDETERMINATE
    d = comparison(
        ruleDeficiencies=[{"ruleId": "core.unused-export", "gating": True,
                           "cause": "required-evidence-unavailable"}],
        contextDelta={"codeChanged": True, "detectorChanged": False,
                      "policyChanged": False, "scopeChanged": False,
                      "waiversChanged": False,
                      "evidenceAvailabilityChanged": True},
        verdict="indeterminate")
    cid = "comparison2:" + C.H("workflow.comparison", d)
    inst = {"comparisonResultId": cid, "descriptor": d}
    errs = validate(CMP, inst)
    rec("E1", "current-baseline audit, ZERO entries on both sides, required "
        "evidence lost on a gating rule -> verdict indeterminate (entry "
        "counts can never prove a finding's absence)",
        "workflows-and-surfaces.md §3 verdict rule and §12; "
        "comparison-result.schema.json#/$defs/RuleDeficiency",
        "schema-valid, entries=[], verdict=indeterminate",
        {"comparisonResultId": cid, "entries": len(d["entries"]),
         "verdict": d["verdict"], "schemaErrors": errs},
        errs == [] and d["entries"] == [] and d["verdict"] == "indeterminate")

    # ---- E2 whole-comparison indeterminacy: unmapped project
    d2 = comparison(projectCorrespondence="unmapped",
                    comparisonPerformed=False,
                    wholeIndeterminateReason="baseline-project-unmapped",
                    remedy={"code": "BASELINE.PROJECT_UNMAPPED",
                            "remedy": "re-adopt the baseline or pass "
                                      "--accept-origin"},
                    verdict="indeterminate")
    inst2 = {"comparisonResultId": "comparison2:" + C.H("workflow.comparison", d2),
             "descriptor": d2}
    errs = validate(CMP, inst2)
    rec("E2", "unmapped baseline project: NO comparison is performed, zero "
        "entries, typed remedy", "workflows-and-surfaces.md §2/§3",
        "schema-valid", {"schemaErrors": errs, "verdict": d2["verdict"]},
        errs == [])

    # ---- E3 evidence-changed attribution is conservative
    entry = {"fingerprint": "finding-key2:" + H64("fp-1"),
             "ruleId": "core.unused-export", "detectorId": "core.ts",
             "presence": {"B": True, "E0": None, "E1": True, "E2": True,
                          "E3": True, "E4": False, "waivedB": False,
                          "waivedC": False},
             "classification": "INDETERMINATE",
             "indeterminateReason": "evidence-content-changed",
             "subsequentDeltas": [], "liveInCurrent": False, "gates": False}
    d3 = comparison(entries=[entry],
                    counts=dict(ZERO_COUNTS, INDETERMINATE=1),
                    contextDelta={"codeChanged": False, "detectorChanged": False,
                                  "policyChanged": False, "scopeChanged": False,
                                  "waiversChanged": False,
                                  "evidenceAvailabilityChanged": True},
                    ruleDeficiencies=[{"ruleId": "core.unused-export",
                                       "gating": True,
                                       "cause": "required-evidence-unavailable"}],
                    verdict="indeterminate")
    inst3 = {"comparisonResultId": "comparison2:" + C.H("workflow.comparison", d3),
             "descriptor": d3}
    errs = validate(CMP, inst3)
    rec("E3", "a replaced import of the SAME kind is an evidence change; "
        "attribution is INDETERMINATE, never a claimed regression or a "
        "silent EVIDENCE-DELTA on a gating rule",
        "workflows-and-surfaces.md §3 'Evidence axis' and §12 "
        "'Evidence-change attribution is deliberately conservative'",
        "schema-valid INDETERMINATE entry", {"schemaErrors": errs}, errs == [])

    # ---- E4 missing prior detector pivot
    entry4 = dict(entry, indeterminateReason="pivot-detector-unavailable",
                  presence=dict(entry["presence"], E0=None))
    d4 = comparison(
        entries=[entry4], counts=dict(ZERO_COUNTS, INDETERMINATE=1),
        detectors=[{"detectorId": "core.ts",
                    "baselineClosureId": "closure2:" + H64("detector-ts-1"),
                    "currentClosureId": "closure2:" + H64("detector-ts-2"),
                    "baselineSemanticsMajor": 2, "currentSemanticsMajor": 2,
                    "method": "indeterminate",
                    "indeterminateReason": "pivot-detector-unavailable"}],
        contextDelta={"codeChanged": True, "detectorChanged": True,
                      "policyChanged": False, "scopeChanged": False,
                      "waiversChanged": False,
                      "evidenceAvailabilityChanged": False},
        pivotsAvailable={"E0": "unavailable", "E1": "not-needed",
                         "E2": "not-needed", "E3": "not-needed"},
        verdict="indeterminate")
    inst4 = {"comparisonResultId": "comparison2:" + C.H("workflow.comparison", d4),
             "descriptor": d4}
    errs = validate(CMP, inst4)
    rec("E4", "changed detector without a current-trusted E0 pivot: E0 is "
        "unavailable and the entry is INDETERMINATE; B is never substituted "
        "for E0", "workflows-and-surfaces.md §2 'Detector semantics' and §3 "
        "'Detector union'", "schema-valid", {"schemaErrors": errs}, errs == [])

    # ---- E5..E7 negative controls on the comparison schema
    neg = [
        ("E5", "comparisonPerformed=false with a non-empty entries array is "
         "schema-refused", comparison(
             comparisonPerformed=False,
             wholeIndeterminateReason="baseline-project-unmapped",
             remedy={"code": "BASELINE.PROJECT_UNMAPPED", "remedy": "x"},
             entries=[entry], verdict="indeterminate")),
        ("E6", "comparisonPerformed=false with verdict=pass is schema-refused",
         comparison(comparisonPerformed=False,
                    wholeIndeterminateReason="baseline-project-unmapped",
                    remedy={"code": "BASELINE.PROJECT_UNMAPPED", "remedy": "x"},
                    verdict="pass")),
        ("E7", "an INDETERMINATE entry with no indeterminateReason is "
         "schema-refused", comparison(
             entries=[{k: v for k, v in entry.items()
                       if k != "indeterminateReason"}],
             counts=dict(ZERO_COUNTS, INDETERMINATE=1),
             verdict="indeterminate")),
    ]
    for vid, title, dd in neg:
        inst = {"comparisonResultId": "comparison2:" + C.H(
            "workflow.comparison", dd), "descriptor": dd}
        errs = validate(CMP, inst)
        rec(vid, title, "comparison-result.schema.json allOf branch contract",
            "schema refusal", {"schemaErrors": errs}, errs != [])

    # ---- E8 comparison identity excludes operational identities
    d8a = comparison()
    d8b = comparison()
    same = C.H("workflow.comparison", d8a) == C.H("workflow.comparison", d8b)
    rec("E8", "comparison2 = H('workflow.comparison', descriptor); the "
        "descriptor is closed and carries no RequestId/ExecutionId/clock/"
        "receipt, so two attempts over equal inputs share one identity",
        "workflows-and-surfaces.md §3/§10; comparison-result.schema.json "
        "#/$defs/ComparisonDescriptor", "stable identity",
        {"comparison2": "comparison2:" + C.H("workflow.comparison", d8a)}, same)

    # ---- E9..E17 public terminations for the remaining scenarios
    TERM = COMMON + "StepTermination"
    T = [
        ("E9", "audit with a missing/revoked pivot closure -> indeterminate 3",
         "workflows-and-surfaces.md §9; §2",
         {"class": "indeterminate", "reasonCodes": ["BASELINE.RECIPE_UNSUPPORTED"],
          "domainDetail": {"code": "BASELINE.PIVOT_DETECTOR_UNAVAILABLE",
                           "remedy": "install the baseline detector release "
                                     "or re-adopt the baseline"}}),
        ("E10", "adopting an --ephemeral result as a baseline -> "
         "request-rejected 2", "workflows-and-surfaces.md §2 "
         "BASELINE.SOURCE_EPHEMERAL",
         {"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
          "domainDetail": {"code": "BASELINE.SOURCE_EPHEMERAL",
                           "remedy": "re-run a durable authoritative analysis"}}),
        ("E11", "interactive test consent offered in CI -> request-rejected 2 "
         "(security admission refuses; the workflow never relabels it)",
         "workflows-and-surfaces.md §7 and §12 consent mapping; security S10",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "TEST.INTERACTIVE_CONSENT_IN_CI",
                           "remedy": "supply an admitted policy-record "
                                     "consent"}}),
        ("E12", "a test step claiming enforcement without a measured platform "
         "primitive -> request-rejected 2",
         "workflows-and-surfaces.md §7; security S10 truth-table equality",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "TEST.CONFINEMENT_CLAIM_REFUSED",
                           "remedy": "declare DISCLOSURE-ONLY effects"}}),
        ("E13", "native preparation without an admitted RepoExecutionGrantV2 "
         "-> request-rejected 2", "native-evidence.md §10/§14; security S10",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "native.execution-not-authorized",
                           "remedy": "obtain an explicit preparation grant"}}),
        ("E14", "repair apply whose authorization is not bound to this exact "
         "repairPlanId -> request-rejected 2",
         "workflows-and-surfaces.md §6; security S10.1",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "REPAIR.CONSENT_NOT_BOUND",
                           "remedy": "re-authorize for this repair plan"}}),
        ("E15", "repair apply target preimage mismatch -> request-rejected 2, "
         "journal FAILED_CLEAN, no target changed",
         "workflows-and-surfaces.md §6",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "REPAIR.TARGET_PREIMAGE_MISMATCH",
                           "remedy": "re-run repair preview on the live tree"}}),
        ("E16", "recovery blocked: a renamed target is neither preimage nor "
         "postimage -> operational-failed 4, no automatic action",
         "workflows-and-surfaces.md §6 recover table; security S10.2",
         {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
          "faultCause": "host-io",
          "domainDetail": {"code": "REPAIR.RECOVERY_BLOCKED",
                           "remedy": "inspect the retained journal"}}),
        ("E17", "replay/regeneration mismatch cannot replace a sealed Run -> "
         "request-rejected 2", "identity-and-evidence.md §4 "
         "'A mismatch is `regeneration-mismatch`; it cannot replace the "
         "sealed Run'",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED"}),
        ("E18", "verify after apply: the fresh snapshot differs from "
         "appliedSnapshotId -> request-rejected 2, NO Run is sealed",
         "workflows-and-surfaces.md §6 Verify",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "REPAIR.SOURCE_MOVED",
                           "remedy": "re-run repair preview"}}),
    ]
    exit_of = {"success": 0, "policy-failed": 1, "request-rejected": 2,
               "indeterminate": 3, "operational-failed": 4, "interrupted": 130}
    codes = set(json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/public-detail-registry.v1.json"
    )))["records"] and [r["code"] for r in json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/public-detail-registry.v1.json"
    )))["records"]])
    for vid, title, sel, term in T:
        errs = validate(TERM, term)
        dd = term.get("domainDetail", {}).get("code")
        rec(vid, title, sel, "schema-valid; exit %d" % exit_of[term["class"]],
            {"termination": term, "exitCode": exit_of[term["class"]],
             "schemaErrors": errs,
             "detailInClosedRegistry": None if dd is None else dd in codes},
            errs == [])

    # ---- E19 the two documented positive cross-registry invariants
    reg = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/public-detail-registry.v1.json")))
    enum = DOCS["urn:opensip:product-v1:workflows:common"][
        "$defs"]["DomainDetailCode"]["enum"]
    rc = [r["code"] for r in reg["records"]]
    internal = {a["internalCode"] for a in reg["internalAliases"]}
    rec("E19", "the closed public-detail registry and the common.schema "
        "DomainDetailCode enum are exactly equal, sorted and free of internal "
        "decision aliases (the §12 drift-check holds)",
        "workflows-and-surfaces.md §12; public-detail-registry.v1.json; "
        "common.schema.json#/$defs/DomainDetailCode",
        "equal sets, sorted, no alias leakage",
        {"registry": len(rc), "enum": len(enum),
         "registryMinusEnum": sorted(set(rc) - set(enum)),
         "enumMinusRegistry": sorted(set(enum) - set(rc)),
         "aliasLeakage": sorted(internal & set(enum))},
        set(rc) == set(enum) and rc == sorted(rc) and enum == sorted(enum)
        and not (internal & set(enum)))

    # ---- E20 the S9.2 obligation on CoreTransitionIntentV1 is discharged
    cti = DOCS["urn:opensip:product-v1:workflows:invocation-record"][
        "$defs"]["CoreTransitionIntentV1"]
    ops = cti["properties"]["operation"]["enum"]
    rec("E20", "security S9.2's stated open obligation ('the current "
        "nine-field, three-operation workflow schema cannot express a store "
        "operation') is ALREADY discharged in these bytes: 11 fields, 5 "
        "operations", "security-and-lifecycle.md S9.2 vs "
        "invocation-record.schema.json#/$defs/CoreTransitionIntentV1",
        "5 operations incl. store-migrate/store-rollback and both store "
        "generation fields",
        {"operations": ops, "requiredFieldCount": len(cti["required"]),
         "hasStoreGenerations": (
             "fromStoreGeneration" in cti["required"]
             and "toStoreGeneration" in cti["required"])},
        set(ops) == {"core-update", "core-repair", "core-rollback",
                     "store-migrate", "store-rollback"}
        and len(cti["required"]) == 11)

    # ---- E21 PROFILE_SET.* / ENVELOPE.* details named by security are NOT
    #          in the closed public registry, so the schema refuses them.
    named = ["PROFILE_SET.NO_TR_PROFILE_ROLE", "PROFILE_SET.CORE_PIN_MISMATCH"]
    fam = {"PROFILE_SET.": [c for c in rc if c.startswith("PROFILE_SET.")],
           "ENVELOPE.": [c for c in rc if c.startswith("ENVELOPE.")]}
    refusals = {}
    for c in named:
        refusals[c] = validate(TERM, {
            "class": "request-rejected",
            "errorCode": "EXTENSION.ADMISSION_REJECTED",
            "domainDetail": {"code": c, "remedy": "x"}}) != []
    rec("E21", "security S9.1/S12 name PROFILE_SET.* and ENVELOPE.* as public "
        "typed details, but the closed registry has ZERO members of either "
        "family, so a conforming host cannot emit them",
        "security-and-lifecycle.md S9.1 ('detail `PROFILE_SET.NO_TR_PROFILE_"
        "ROLE`'), S8 ('refuses `PROFILE_SET.CORE_PIN_MISMATCH`'), S12 "
        "('`PAYLOAD-NOT-ADMISSIBLE` (incl. `ROOT.*`, `ENVELOPE.*`, "
        "`PROFILE_SET.*` details)') vs public-detail-registry.v1.json",
        "GAP: both families empty; emission is schema-refused",
        {"registeredMembersByFamily": fam,
         "rootFamilyForContrast": len([c for c in rc if c.startswith("ROOT.")]),
         "schemaRefusesNamedDetail": refusals},
        # This vector PASSES by demonstrating the gap reproducibly.
        fam["PROFILE_SET."] == [] and fam["ENVELOPE."] == []
        and all(refusals.values()))


def build_inventory(results):
    def rec(vid, title, sel, expect, obs, ok, extra=None):
        results.append({"id": vid, "title": title, "owningSelector": sel,
                        "expected": expect, "observed": obs, "pass": bool(ok),
                        "extra": extra or {}})
    inv = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/workflows/command-inventory.v1.json")))
    errs = validate("urn:opensip:product-v1:workflows:command-inventory#", inv)
    rec("E22", "the candidate single command inventory validates against its "
        "own closed schema (45 commands across the §8 groups)",
        "workflows-and-surfaces.md §8; command-inventory.schema.json",
        "schema-valid",
        {"commandCount": len(inv["commands"]), "schemaErrors": errs[:5]},
        errs == [])

    need = {"run-id", "verdict", "required-coverage", "deficiency", "findings",
            "termination-class", "retention-disclosure"}
    sarif = [c for c in inv["commands"] if "sarif" in (c.get("formats") or [])]
    miss = {c["name"]: sorted(need - set(c.get("parityFields", [])))
            for c in sarif}
    rec("E23", "the §8 SARIF parity MUST holds exactly: the four advertised "
        "SARIF commands are `default`, `analyze`, `audit`, `repair-verify` "
        "and each declares all seven common parity fields",
        "workflows-and-surfaces.md §8 'Every advertised SARIF command "
        "(`default`, `analyze`, `audit`, `repair-verify`) must declare the "
        "common fields ...; inventory admission refuses an omission.'",
        "four commands, zero omissions",
        {"sarifCommands": sorted(c["name"] for c in sarif),
         "missingParityFieldsByCommand": miss},
        sorted(c["name"] for c in sarif) == ["analyze", "audit", "default",
                                             "repair-verify"]
        and all(v == [] for v in miss.values()))
