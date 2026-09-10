"""Independent public termination examples for the workflow scenarios, each
validated against the owning closed schemas:

  common.schema.json#/$defs/StepTermination      (the closed D9 projection)
  command-envelope.schema.json                   (CommandEnvelope major 2)
  public-detail-registry.v1.json                 (the single closed detail set)

Authored by the blind consumer from workflows sections 1-3, 6-9, 12, identity
sections 4-5, native section 10 and security S12/S12.1.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graph as G

SUBJECT = G.SUBJECT
RUN = "run2:" + "9c" * 32
REQ = "req1_" + "ab" * 16
EXEC = "exec1_" + "cd" * 16
COV = "coverage2:" + "7e" * 32

EXIT = {"success": 0, "policy-failed": 1, "request-rejected": 2,
        "indeterminate": 3, "operational-failed": 4, "interrupted": 130}


def T(cls, **kw):
    t = {"class": cls}
    t.update(kw)
    return t


def D(code, remedy, subject=None):
    d = {"code": code, "remedy": remedy}
    if subject is not None:
        d["subject"] = subject
    return d


SCENARIOS = [
    # ---------------------------------------------- current-baseline audit --
    ("TERM-01-audit-clean-against-current-baseline", "audit --baseline",
     "workflows 3 (audit profile code-regression), 1 (aggregate termination)",
     "Comparison attributes every fingerprint to its first changed axis; no entry "
     "gates; the analysis Run is authoritative and its own verdict stands.",
     T("success", runId=RUN),
     "workflow comparison subsystem owns the gate; the analysis step's Run keeps "
     "its own verdict (verdictGate=delegated)."),
    ("TERM-02-baseline-pivot-detector-missing", "audit --baseline",
     "workflows 2 (fresh CI closure resolution), 3 (E0 unavailable), 9 goldens",
     "The baseline names a prior detector closure2 that is not retained, not "
     "installed and not in the signed closure bundle: E0 is unavailable, so the "
     "code axis cannot be evaluated and attribution is indeterminate.",
     T("indeterminate", reasonCodes=["BASELINE.RECIPE_UNSUPPORTED"],
       domainDetail=D("BASELINE.PIVOT_DETECTOR_UNAVAILABLE",
                      "install or bundle the baseline detector closure, or "
                      "re-adopt with `opensip baseline upgrade`",
                      "closure2:" + "11" * 32)),
     "workflow baseline/comparison subsystem decides availability; the security "
     "subsystem decides current trust of the resolved closure; neither is a Run."),
    ("TERM-03-comparison-required-evidence-unavailable", "audit --baseline",
     "workflows 3 (evidence axis), 9 goldens",
     "A gating rule declares evidenceUse required for an import kind that is "
     "absent on the current side: the entry is INDETERMINATE with "
     "required-evidence-unavailable and the rule's coverage is unsatisfied. "
     "Required evidence loss can never disappear as a non-gating delta.",
     T("indeterminate", reasonCodes=["VERDICT.INDETERMINATE"],
       domainDetail=D("COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE",
                      "re-import the runtime evidence for the current snapshot and "
                      "re-run the audit", "kind=runtime")),
     "workflow comparison subsystem owns evidence-axis attribution; the identity "
     "subsystem owns the import2 identity whose change was observed."),
    ("TERM-04-empty-result-comparison-still-indeterminate", "audit --baseline",
     "workflows 12 ('even when both observed finding sets are empty'), 3",
     "Both observed finding sets are empty, but a required E2 policy "
     "re-evaluation was never bound while an enabled rule gates. Entry counts "
     "cannot prove the absence of a finding that missing evaluation could hide.",
     T("indeterminate", reasonCodes=["VERDICT.INDETERMINATE"],
       domainDetail=D("COMPARISON.PIVOT_REEVALUATION_UNAVAILABLE",
                      "bind the E2 policy re-evaluation; a host failure to execute "
                      "a computable pivot is an operational failure, not an option",
                      "axis=policy")),
     "workflow comparison subsystem; zero emitted findings never establish "
     "complete analysis (workflows 3)."),

    # ------------------------------------- test / preparation authorization --
    ("TERM-05-test-interactive-consent-in-ci", "test run",
     "workflows 7, 9 goldens; security S10 (interactive-explicit never in CI)",
     "Repository code execution is disabled by default. In CI the security unit "
     "admits only a pre-existing policy record; interactive consent refuses at "
     "security admission, before any spawn.",
     T("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED",
       domainDetail=D("TEST.INTERACTIVE_CONSENT_IN_CI",
                      "provide a pre-existing policy-record grant bound to this "
                      "project, snapshot and argv digest")),
     "security subsystem decides the RepoExecutionGrantV2 admission; the workflow "
     "subsystem only consumes the host projection of an actually admitted grant."),
    ("TERM-06-test-confinement-claim-refused", "test run",
     "workflows 7; security S10 truth-table equality; native 5.2 EnforcementV1",
     "The step claims an enforced network bound on a platform whose truth table "
     "says DISCLOSURE-ONLY. Every effect value must EQUAL the security owner's "
     "platform truth-table entry; a stronger or weaker claim refuses.",
     T("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED",
       domainDetail=D("TEST.CONFINEMENT_CLAIM_REFUSED",
                      "declare the effects exactly as the platform truth table "
                      "states; OpenSIP claims no sandbox",
                      "network=ENFORCED-PLATFORM claimed, DISCLOSURE-ONLY measured")),
     "security subsystem owns permission-truth-tables.v9; native and workflows "
     "copy, never assert, those values."),
    ("TERM-07-native-preparation-not-authorized-in-ci", "native prepare",
     "native 5.2 / 10; security S10; workflows 12",
     "CI without a policy record bound to the same dependencySourceSetId and "
     "toolchain: no owner runs, no prepared row is captured, no Run is minted "
     "(a preparation step never mints a Run).",
     T("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED",
       domainDetail=D("native.execution-not-authorized",
                      "create a policy record bound to this dependency source set "
                      "and toolchain, or run interactively")),
     "security subsystem admits the grant; native owns the preflight descriptor; "
     "the workflow subsystem owns the step outcome and receipt."),

    # ------------------------------------------------- repair authorization --
    ("TERM-08-repair-apply-consent-not-bound", "repair apply",
     "workflows 6; security S10.1 RepairApplyAuthorizationV1",
     "Repair apply is host-brokered FIRST-PARTY source mutation, not repository "
     "execution. Its authorization must bind projectId, repairPlanId and "
     "baseSnapshotId to this invocation; an unbound consent refuses before the "
     "EXCLUSIVE lease is used to write anything.",
     T("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED",
       domainDetail=D("REPAIR.CONSENT_NOT_BOUND",
                      "obtain an authorization bound to this exact repairPlanId "
                      "and base snapshot")),
     "security subsystem admits RepairApplyAuthorizationV1; the workflow "
     "subsystem owns the journal and the mutation receipt."),
    ("TERM-09-repair-target-preimage-mismatch", "repair apply",
     "workflows 6 (STAGED -> FAILED_CLEAN)",
     "A target file no longer matches the preimage digest the plan recorded from "
     "the snapshot inventory. The journal leaves FAILED_CLEAN; no postimage is "
     "renamed into place and the plan is not relocated heuristically.",
     T("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED",
       domainDetail=D("REPAIR.TARGET_PREIMAGE_MISMATCH",
                      "re-run `opensip repair preview` against the current source",
                      "src/a.ts")),
     "workflow repair subsystem owns the guarded preimage/postimage mechanics; "
     "identity owns the snapshot inventory digest that was compared."),
    ("TERM-10-repair-recovery-blocked", "repair recover --apply-recovery",
     "workflows 6 (RECOVERY_BLOCKED); security S10.2",
     "A renamed target is neither the plan preimage nor the plan postimage, so no "
     "automatic action is lawful. The journal is retained and the paths listed.",
     T("operational-failed", errorCode="HOST.IO_FAILURE", faultCause="host-io",
       domainDetail=D("REPAIR.RECOVERY_BLOCKED",
                      "inspect the retained journal; recovery never re-applies an "
                      "edit and never overwrites an unrecognized target",
                      "src/b.ts")),
     "workflow recovery table decides the action; security S10.2 admits the "
     "recovery authorization; neither may waive the guarded mechanics."),

    # -------------------------------------------------- purge / replay ------
    ("TERM-11-purge-of-a-pinned-run-refuses", "purge",
     "identity 5 (retention roots and pinned purge)",
     "The Run is a retention root of an active baseline. A direct purge refuses "
     "unless the explicit destructive purge also revokes the named pins after "
     "disclosing the consequences.",
     T("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED"),
     "identity retention subsystem owns pins and reachability GC; workflows owns "
     "the baseline pin that made this Run a root."),
    ("TERM-12-query-requiring-proof-after-purge", "query proof.show",
     "identity 5 ('Query of retained manifest is allowed after purge')",
     "The sealed manifest, provenance and tombstone survive, so a manifest query "
     "still answers and states evidence unavailable; a query REQUIRING actual "
     "proof refuses BEFORE evaluation. Purged is not deleted-history, and a "
     "retention decision never turns expired evidence into `no match`.",
     T("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED",
       domainDetail=D("evidence.purged",
                      "the evidence bytes were purged; the sealed verdict and "
                      "assurance are unchanged and still queryable", RUN)),
     "identity retention/availability subsystem; the sealed assurance and "
     "historical verdict are immutable and are NOT rewritten by availability."),
    ("TERM-13-regeneration-mismatch", "verify --regenerate",
     "identity 4 (regeneration verification refusal)",
     "Regeneration executed the exact retained producer and Plan input closure "
     "into a candidate namespace and a required byte disagreed. Recovered "
     "availability is not published; it cannot replace the sealed Run.",
     T("operational-failed", errorCode="HOST.IO_FAILURE", faultCause="host-io",
       runId=RUN,
       domainDetail=D("evidence.regeneration-mismatch",
                      "the regenerated bytes differ from the sealed identity; "
                      "availability stays unavailable and the Run is unchanged")),
     "identity evidence/availability subsystem; a mismatch is an operational "
     "refusal, never a new verdict."),

    # ------------------------------------------- required output failure ----
    ("TERM-14-required-renderer-failed-after-commit", "analyze --format sarif",
     "workflows 8 / 9 goldens; admission 5 item 6",
     "The Run was committed and acknowledged; the selected REQUIRED renderer then "
     "failed. Required rendering is later than commit and cannot rewrite the Run, "
     "so the runId is carried in the termination and the assurance is unchanged.",
     T("operational-failed", errorCode="DELIVERY.REQUIRED_FAILED",
       faultCause="delivery-required", runId=RUN,
       domainDetail=D("DELIVERY.RENDERER_FAILED_AFTER_COMMIT",
                      "re-render from the committed Run with `opensip query`; the "
                      "Run and its verdict are unchanged")),
     "workflow output subsystem owns delivery; identity owns the already-committed "
     "Run whose assurance delivery may not touch."),
    ("TERM-15-optional-export-sink-failed", "analyze --export-optional",
     "workflows 8 ('failure of an optional export sink leaves success')",
     "Egress never changes a verdict.",
     T("success", runId=RUN),
     "workflow output subsystem; the distinction between required and optional "
     "delivery is the workflow's, never the renderer's."),

    # ---------------------------------------------------- other positions ---
    ("TERM-16-ephemeral-cannot-supply-authority", "analyze --ephemeral --baseline",
     "workflows 1; identity 5 ('--ephemeral is explicitly non-authoritative')",
     "An ephemeral result mints no Run and no commit receipt, so it cannot satisfy "
     "baseline adoption, repair, verify or authoritative replay prerequisites.",
     T("request-rejected", errorCode="REQUEST.UNSATISFIABLE",
       domainDetail=D("WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY",
                      "re-run without --ephemeral to seal a durable authoritative "
                      "Run")),
     "workflow invocation subsystem; identity owns the durable custody rule that "
     "makes ephemeral non-authoritative."),
    ("TERM-17-admitted-incomplete-native-inputs", "analyze",
     "native 10 fault law; identity 5 ('successfully admitted partial native "
     "inputs may instead produce an indeterminate Run')",
     "A stage terminated CLEANLY over successfully admitted but incomplete inputs "
     "(a missing external crate). Facts and typed Coverage are admitted, an "
     "AUTHORITATIVE Run is sealed, and the deficiency travels as typed detail "
     "inside the coverage2 record the termination names.",
     T("indeterminate", reasonCodes=["VERDICT.INDETERMINATE"], runId=RUN,
       coverageId=COV),
     "native owns the deficiency/nativeCause typed detail in the coverage2 record; "
     "the host owns the D9 class; no D9 enum changes anywhere (native H-3)."),
    ("TERM-18-worker-fault-contributes-nothing", "analyze",
     "native 10 fault law; native 9.2 state machine FAULT",
     "A worker that faults contributes NO facts, NO Coverage entries and NO Run. "
     "Its stderr and fault detail are an operational record only and can never "
     "mint an authoritative fact.",
     T("operational-failed", errorCode="PROVIDER.PROTOCOL_VIOLATION",
       faultCause="provider-protocol", executionId=EXEC,
       domainDetail=D("native.worker-fault",
                      "run `opensip doctor`; the provider closure faulted and no "
                      "evidence was admitted")),
     "native/provider protocol subsystem observes the fault; the host owns the "
     "class; the identity subsystem seals nothing."),
    ("TERM-19-sigint-before-settle-with-a-committed-run", "opensip",
     "workflows 1 (cancellation), 9 goldens",
     "The signal arrived before every required step was terminal, so remaining "
     "steps are cancelled and the aggregate is interrupted; a Run committed by an "
     "earlier step is still named. After-settle would NOT be reclassified.",
     T("interrupted", signal="SIGINT", runId=RUN),
     "workflow invocation subsystem owns cancellation phase; identity owns the "
     "already-committed Run."),
    ("TERM-20-doctor-defects-found-is-success", "doctor",
     "workflows 8 / 9; security S11 ('CI gates on .outcome, never the exit code')",
     "A PRODUCED report is success even when defects are found; only an "
     "unproducible report is HOST.IO_FAILURE.",
     T("success",
       domainDetail=D("DOCTOR.DEFECTS_FOUND",
                      "inspect doctor.defectsFound in the machine report; the exit "
                      "code is not the gate")),
     "workflow doctor subsystem; security supplies the trust/offline observations."),
    ("TERM-21-backup-custody-choice-required-in-ci", "opensip",
     "identity 5 (TM V17); security S3.1",
     "The storage root is classified detected backup-managed and CI never prompts. "
     "The refusal happens BEFORE creating evidence. UNKNOWN backup status would "
     "instead admit with a mandatory disclosure, never as not-backed-up.",
     T("request-rejected", errorCode="REQUEST.PRECONDITION_FAILED",
       domainDetail=D("storage.backup-choice-required",
                      "select another admitted storage root, choose --ephemeral, or "
                      "pass --allow-backup-custody")),
     "security storage-write admission decides; identity owns the durable custody "
     "posture the choice protects."),
    ("TERM-22-workspace-unit-limit", "opensip",
     "native 1.4 U-7 / 14; security S3 / S12; the shared discovery rule",
     "More than 4096 FIRST-PARTY unit directories. Installed dependency manifests "
     "are pruned first and never count. Never truncation, never an exception.",
     T("request-rejected", errorCode="REQUEST.UNSATISFIABLE",
       domainDetail=D("PROJECT.WORKSPACE_UNIT_LIMIT",
                      "narrow the explicit workspace selection", "4200>4096")),
     "the ONE shared discovery rule; both the security instrument and the native "
     "unit instrument refuse the same population with the same public code."),
]


def build():
    rows = []
    for vid, command, selectors, story, term, owner in SCENARIOS:
        envelope = {
            "schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
            "kind": "failure" if term["class"] in ("request-rejected", "operational-failed")
                    else "invocation",
            "requestId": REQ,
            "termination": term,
            "exitCode": EXIT[term["class"]],
        }
        constructible = True
        if envelope["kind"] == "failure":
            if "domainDetail" not in term:
                # BLOCKER, not an invention: kind=failure requires a non-empty
                # `errors` array whose every code is a member of the closed
                # public-detail registry, and the registry has NO member for this
                # normatively required refusal.  No admissible envelope exists.
                constructible = False
            else:
                envelope["errors"] = [term["domainDetail"]]
        rows.append({"envelopeConstructible": constructible,
                     "id": vid, "command": command, "owningSelectors": selectors,
                     "story": story, "termination": term,
                     "exitCode": EXIT[term["class"]],
                     "subsystemOwnership": owner,
                     "envelopeKind": envelope["kind"], "envelope": envelope})
    return rows


def validate(rows):
    import jsonschema
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    def load(p):
        return json.load(open(os.path.join(SUBJECT, p)))

    docs = [load("docs/coop/design-corrections/workflows/schemas/" + n) for n in
            ("common.schema.json", "command-envelope.schema.json",
             "invocation-record.schema.json", "comparison-result.schema.json",
             "imported-evidence.schema.json", "test-execution.schema.json",
             "repair.schema.json", "policy-document.schema.json",
             "baseline-artifact.schema.json", "graph-query.schema.json",
             "policy-test.schema.json", "review.schema.json",
             "command-inventory.schema.json")]
    registry = Registry()
    for doc in docs:
        if "$id" in doc:
            registry = registry.with_resource(doc["$id"], Resource.from_contents(doc))
    common = docs[0]
    envelope_doc = docs[1]
    reg = json.load(open(os.path.join(
        SUBJECT, "docs/coop/design-corrections/public-detail-registry.v1.json")))
    registered = set()
    for r in reg["records"]:
        registered.add(r["code"] if isinstance(r, dict) and "code" in r else r)
    enum_codes = set(common["$defs"]["DomainDetailCode"]["enum"])

    tv = Draft202012Validator({"$ref": common["$id"] + "#/$defs/StepTermination"},
                             registry=registry)
    ev = Draft202012Validator({"$ref": envelope_doc["$id"]}, registry=registry)
    for row in rows:
        errs = []
        pairs = [("StepTermination", tv, row["termination"])]
        if row["envelopeKind"] == "failure" and row["envelopeConstructible"]:
            pairs.append(("CommandEnvelopeV2", ev, row["envelope"]))
        for label, validator, instance in pairs:
            try:
                validator.validate(instance)
                row.setdefault("validation", {})[label] = "valid"
            except Exception as exc:
                row.setdefault("validation", {})[label] = "INVALID: " + str(exc).split("\n")[0][:300]
        code = row["termination"].get("domainDetail", {}).get("code")
        if code is not None:
            row["detailRegistered"] = code in enum_codes
    return rows, sorted(enum_codes), sorted(registered)


if __name__ == "__main__":
    rows, enum_codes, registered = validate(build())
    out = {"terminations": rows,
           "domainDetailEnumSize": len(enum_codes),
           "publicDetailRegistrySize": len(registered),
           "enumEqualsRegistry": set(enum_codes) == set(registered)}
    path = "/tmp/opensip-design-corrections/consumer-b.v2/output/terminations.json"
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
        fh.write("\n")
    bad = [r for r in rows if any(v != "valid" for v in r["validation"].values())
           or r.get("detailRegistered") is False]
    out_blocked = [r["id"] for r in rows if not r["envelopeConstructible"]]
    print("envelope NOT constructible (design gap):", out_blocked)
    print("scenarios:", len(rows), "invalid-or-unregistered:", len(bad))
    for r in bad:
        print(" !", r["id"], r["validation"], "detailRegistered=",
              r.get("detailRegistered"), r["termination"].get("domainDetail", {}).get("code"))
    print("enum size", len(enum_codes), "registry size", len(registered),
          "equal:", set(enum_codes) == set(registered))
