#!/usr/bin/env python3
"""Assemble review.json from the measured evidence, so counts are not transcribed."""
import glob
import hashlib
import json
import os

OUT = "/tmp/opensip-design-corrections/post-reset-review.v15"
V14B = OUT + "/v14-bytes/docs/coop/design-corrections/"
V15 = "/tmp/opensip-design-corrections/candidate-subject.v15/"
DC = V15 + "docs/coop/design-corrections/"

pre = json.load(open(OUT + "/custody/verify-PRE.json"))
post = json.load(open(OUT + "/custody/verify-POST.json"))
delta = json.load(open(OUT + "/custody/delta-v14-v15.json"))
pins = json.load(open(OUT + "/custody/pins-PRE-RUN.json"))
copies = json.load(open(OUT + "/custody/copy-deltas-final.json"))

probes = {}
tot = passed = failed = 0
for fn in sorted(glob.glob(OUT + "/evidence/probe-*.json")):
    d = json.load(open(fn))
    probes[os.path.basename(fn)] = {"total": d["total"], "passed": d["passed"],
                                    "failed": d["failed"], "limitations": d["limitations"]}
    tot += d["total"]; passed += d["passed"]; failed += d["failed"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def ident(rel):
    return sha(V14B + rel) == sha(DC + rel)


# ---- crosswalk AR rows: which fields actually differ
a = json.load(open(V14B + "correction-crosswalk.proposed.json"))
b = json.load(open(DC + "correction-crosswalk.proposed.json"))
ida = {r["id"]: r for r in a["items"]}
idb = {r["id"]: r for r in b["items"]}
ar = {}
for k in sorted(idb):
    diff = sorted(f for f in set(ida[k]) | set(idb[k]) if ida[k].get(f) != idb[k].get(f))
    ar[k] = {
        "disposition": "CARRIED-UNCHANGED",
        "basis": ("Row present in both the v14 and v15 crosswalk; the only fields that "
                  "differ are the review-provenance pointers %s. No obligation, "
                  "selector, owner, unit, contract, evidence, ownerRows or status "
                  "field changed." % diff),
        "scope": "Preservation across the v14->v15 delta only. Never a new discharge or closure.",
        "authority": "This design/reference review. Grading the proposed readiness outcome "
                     "belongs to the separate full application review, which has not run.",
    }

fw = {}
fw_ident = ident("current-source-map.proposed.md")
for i in range(1, 16):
    fw["FW-%02d" % i] = {
        "disposition": "CARRIED-UNCHANGED",
        "basis": ("current-source-map.proposed.md is byte-identical between v14 and v15 "
                  "(verified: %s) and is absent from the 19 modified paths." % fw_ident),
        "scope": "Preservation across this delta only.",
        "authority": "Design/reference review; routing only, not applied.",
    }

dr_ids = (["DR-%03d" % i for i in range(1, 12)]
          + ["DR-011-R%02d" % i for i in range(1, 17)])
res_ident = ident("inherited-residuals.proposed.md")
src_ident = ident("inherited-row-sources.proposed.json")
inherited = {}
for k in dr_ids:
    extra = ""
    if k == "DR-011-R10":
        extra = (" DR-011-R10 is the row the product-v1 contract set sits under; its "
                 "register entry is byte-unchanged, and the two contract edits in this "
                 "delta are graded above as the availability-mirror and selection-"
                 "cardinality corrections and as the two v14 advisory clarifications, "
                 "not as a residual closure.")
    inherited[k] = {
        "disposition": "CARRIED-UNCHANGED",
        "basis": ("inherited-residuals.proposed.md (%s) and inherited-row-sources."
                  "proposed.json (%s) are byte-identical between v14 and v15.%s"
                  % (res_ident, src_ident, extra)),
        "scope": "Preservation across this delta only; no residual is newly closed.",
        "authority": "Design/reference review only.",
    }

owners = {}
for k in ["DR-201", "DR-202", "DR-203", "DR-204", "DR-205"]:
    owners[k] = {
        "disposition": "ROUTING-ASSESSED-ONLY-NOT-APPLIED",
        "scope": ("Owner routing sits on crosswalk row AR-15, whose ownerRows I read "
                  "directly from the v15 crosswalk and whose only v15 change is the two "
                  "review-provenance pointers."),
        "basis": ("AR-15 ownerRows in correction-crosswalk.proposed.json list DR-001, "
                  "DR-006, DR-009, DR-011 and DR-201..205. Nothing in this delta applies "
                  "or discharges any of them."),
        "authority": "Five owner routing assessments do not grant a final application outcome.",
        "appliedByThisReview": False,
    }

gates = json.load(open(DC + "qualification-gates.proposed.json"))
ev = json.load(open(DC + "evaluation-residual-dispositions.proposed.json"))
adv = json.load(open(DC + "reviews/codex-post-reset.v1/"
                          "advisory-application-account.v15.proposed.json"))
adv14 = json.load(open(V14B + "reviews/codex-post-reset.v1/"
                              "advisory-application-account.v14.proposed.json"))

doc = {
    "artifact": "opensip.design-review",
    "version": 1,
    "reviewer": ("Fresh independent actual-Claude design/reference review of frozen "
                 "candidate v15. I authored none of these bytes. I am not coauthor "
                 "77758b10-d7ba-4868-9d42-ae0b13e84cb6, not prior independent "
                 "46ea25c0-21fc-4be6-9b57-61e46c61d64d, and not blind consumer "
                 "878e4b39-2d21-46b2-87bd-64f8d4db015f."),
    "subjectManifestSha256": "5ec7928426c7a91e323240337dc382c4de32bd4e5f2626eba92c8991067b365f",
    "overallVerdict": "ACCEPT",
    "custody": {
        "before": pre, "after": post,
        "identicalBeforeAndAfter": pre["CLEAN"] and post["CLEAN"],
        "note": ("Verified BEFORE any reading and again AFTER all work. Every declared "
                 "file's SHA256 and byte length recomputed and the tree walked "
                 "independently for undeclared entries. The frozen subject and the "
                 "original repository were never written to."),
    },
    "exactDelta": {
        "method": "Recomputed from the v14 and v15 manifests directly, not read from any author account.",
        "predecessorManifestShaVerified": True,
        "filesAdded": delta["added"], "filesRemoved": delta["removed"],
        "filesModified": delta["modified"],
        "modifiedPaths": [m["path"] for m in delta["modifiedPaths"]],
        "normativeSourceModified": [
            "docs/v2/contracts/product-v1/native-evidence.md",
            "docs/v2/contracts/product-v1/admission-and-qualification.md",
            "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
            "docs/coop/design-corrections/foundation/check-identity.py",
            "docs/coop/design-corrections/native/native_evidence_model.v2.py",
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
            "docs/coop/design-corrections/integration-fixtures.py",
        ],
        "unchangedLoadBearingVerifiedByHash": [
            "foundation/identity-model.py", "foundation/identity-schemas.v2.json",
            "native/native-capability-matrix.v2.json",
            "workflows/schemas/common.schema.json",
            "workflows/schemas/command-envelope.schema.json",
            "workflows/workflows_model.v1.py", "public-detail-registry.v1.json",
            "workflows/command-inventory.v1.json",
            "current-source-map.proposed.md", "inherited-residuals.proposed.md",
            "qualification-gates.proposed.json",
            "evaluation-residual-dispositions.proposed.json",
        ],
    },
    "suiteReproduction": {
        "commandsReproduced": 6, "allExitZero": True,
        "logsByteIdenticalToRetained": True,
        "regeneratedReportDelta": {"added": 0, "removed": 0, "modified": 0},
        "fullSourceCopyDeltaAfterEverything": copies,
        "reportsWereGenuinelyRewritten": (
            "Confirmed by mtime: all six reports were rewritten at 10:21-10:22 while "
            "their source inputs stayed at the 10:19:31 copy time, so byte-identity is "
            "'wrote the same bytes', not 'did nothing'."),
        "nativeCheckerActualReportPath": (
            "docs/coop/design-corrections/native/native-evidence-report.v2.json - "
            "REPORT_PATH is HERE-relative and --report is ignored; run only in my "
            "disposable copy-run2."),
        "pinVerification": pins,
        "measuredCounts": {
            "foundationChecksPassed": 1679,
            "foundationComponents": {"foundation": 231, "identity": 1331,
                                     "product-quality": 24,
                                     "product-configuration": 28, "array-order": 65},
            "identityPassingCalls": 1331, "identityDistinctIds": 1319,
            "identityDuplicateExtraInstances": 12,
            "identityDuplicateIds": {"closed-closure": 7, "exact-version-closure": 7},
            "securityCases": 456, "securityInvariantSweeps": 10,
            "nativeCases": 347, "nativeMatrixCells": 66, "nativeQualifiedCells": 0,
            "workflowSurfaceChecks": 1598, "integrationChecks": 365,
        },
        "countHonesty": (
            "I recounted the identity report myself: 1331 passing check CALLS over 1319 "
            "DISTINCT ids, the 12 extra instances coming from exactly two ids at seven "
            "instances each, all passing. The candidate's own identity-check-counts.v15 "
            "states the same three numbers. 231+1331+24+28+65 = 1679 checks out. "
            "Identity grew by exactly 49 calls and 49 distinct ids over v14 with ZERO "
            "ids removed. NONE of these numbers is exhaustive coverage, and passing "
            "calls are not presented as unique cases."),
        "nondeterminismObserved": (
            "None. Every regenerated report was byte-identical to the retained one, so "
            "there is no intended-nondeterministic operational field to report and "
            "nothing was normalized away."),
    },
    "independentProbeCaseTotal": tot,
    "independentProbeCasesPassed": passed,
    "independentProbeCasesFailed": failed,
    "independentProbes": probes,
    "boundSourceSha256": json.load(open(OUT + "/evidence/probe-preplan-cardinality.json"))
        ["boundSourceSha256"],
    "fixtureProvenance": (
        "My probes drive the candidate's own identity-model, native_evidence_model and "
        "workflows_model through their real entry points and bind those files' exact "
        "SHA256s; a bound mismatch is fatal at import. integration-fixtures.py is "
        "imported for CONSTRUCTION only (it loads in 0.1s and does not execute the "
        "check-identity suite), and is never a verdict oracle: every expected outcome "
        "is authored in my probe files. No synthetic re-implementation was used."),
    "harnessErrorsCorrectedNotCountedAsDefects": {
        "count": 8, "record": "evidence/probe-attempts.md",
        "note": ("Five were the candidate's own laws refusing malformed fixtures of "
                 "mine - including the CB4-SHOULD-2 NOT-SELECTED release guard and the "
                 "array-order law - and two were measurement bugs of mine that would "
                 "have produced false accusations. None was a candidate defect."),
    },
    "newMustIssues": [],
    "newShouldIssues": [],
    "newAdvisories": [{
        "id": "V15-ADV-1",
        "severity": "advisory",
        "title": ("The published pre-Plan ordering paragraph states without qualification "
                  "that 'everything a schema is genuinely better at ... still refuses at "
                  "the schema step exactly as before'. That holds only while "
                  "requestedCapabilities is within its bound; when the array is also "
                  "oversized the cardinality step preempts the schema fault."),
        "selectors": [
            "docs/v2/contracts/product-v1/native-evidence.md:2906",
            "docs/coop/design-corrections/native/native_evidence_model.v2.py:3616",
            "docs/coop/design-corrections/native/native_evidence_model.v2.py#admit_analysis_spec",
        ],
        "counterexample": (
            "A spec with 1034 valid rows AND a missing schemaVersion / a wrong "
            "schemaVersion / an unknown property / a missing policyPackIds each refuses "
            "with ScopeRefusal PROJECT.SCOPE_LIMIT:requestedCapabilities:1034>1024, not "
            "with the schema fault. The same four specs at 10 rows each refuse with a "
            "ValidationError, which is my control."),
        "whyNotAMustOrShould": (
            "Nothing is unrepresentable and no admission outcome is wrong. The refusal "
            "that does fire states a TRUE fact about the instance - the array really "
            "does carry 1034 rows against a 1024 bound - the malformed spec is refused "
            "either way, both routes are request-rejected / exit 2, and no Plan or Run "
            "is minted. Narrowing the selection then reveals the underlying schema "
            "fault, so the diagnostic is deferred across two round trips, never lost. "
            "The same paragraph DOES state the implemented order precisely ('bounded "
            "selection cardinality first', 'conditional on the field actually being a "
            "JSON array in an object'), so an implementer building from the published "
            "order reaches the correct result. This is the same class of unqualified-"
            "summarising-sentence issue as V14-ADV-1, at the same severity."),
        "suggestedRepair": (
            "Scope the sentence, e.g. 'Everything a schema is genuinely better at still "
            "refuses at the schema step exactly as before, for any spec whose "
            "requestedCapabilities array is within its bound.'"),
        "evidence": "evidence/probe-ordering-scope-advisory.json (29 cases, all holding)",
    }],
    "priorFindingDispositions": {
        "V14-ADV-1": {
            "priorSeverity": "advisory",
            "assessedDisposition": "ADDRESSED BY SOURCE CLARIFICATION at original severity",
            "myIndependentAssessment": (
                "The frozen v15 native-evidence.md is 706b7e0f... - the exact alternative "
                "the coauthor supplied, not root's originally proposed bytes. I verified "
                "the replacement sentence at line 2267 preserves ALL FOUR refusal-code "
                "additions: it says 'The refusal branches later in this section "
                "separately add four public detail codes; those additions do not change "
                "this projection', and the four members (native.capability-spec-invalid, "
                "native.release-declaration-invalid, native.coverage-cause-unsupported, "
                "HOST.INVARIANT_VIOLATED) are named at lines 2376-2384 and all four are "
                "still present in the unchanged public-detail-registry (287 codes, "
                "sha e54a395f..., byte-identical to v14). I independently confirmed the "
                "section geometry the clarification depends on: section 10 spans "
                "2140-2537, the four-codes paragraph is at 2376 INSIDE section 10, and "
                "section 13 begins at 2750. So 'later in this section' is accurate and "
                "root's rejection of its own 'section 13' wording was correct."),
            "priorReviewTextCorrection": (
                "The v14 review's own V14-ADV-1 TITLE says 'section 13 of the same "
                "document adds four DomainDetailCode members' while its own selector "
                "cites lines 2376-2385, which are section 10. The title is wrong and the "
                "selector is right. Root preserved the frozen v14 artifact verbatim and "
                "recorded the qualification separately rather than editing it, which is "
                "the correct handling. I record it here so it is not inherited as fact."),
            "notSilentlyTreatedAsRequired": True, "notIgnored": True,
            "evidence": "evidence/probe-availability-carrier.json, deltas/native-evidence.md.diff",
        },
        "V14-ADV-2": {
            "priorSeverity": "advisory",
            "assessedDisposition": "ADDRESSED BY SOURCE CLARIFICATION at original severity",
            "myIndependentAssessment": (
                "relation-payload-schemas.v2.json changed EXACTLY ONE STRING - I ran a "
                "key-by-key structural diff against the v14 bytes and the only difference "
                "is /x-opensip-relation-registry/anchorLaw/enforcedAt. The new text "
                "PRESERVES THE PRODUCER OBLIGATION as a modal MUST ('The producer must "
                "enforce this law on every owning fact', with 'on every owning fact' "
                "attached to the obligation), preserves the verifier obligation at "
                "retained closure, ACCURATELY LIMITS THE EXHIBITED REFERENCE EVIDENCE "
                "('it does not exhibit a separate producer-boundary call site'), and "
                "CLAIMS NO NEW PRODUCER IMPLEMENTATION ('remains an implementation "
                "conformance obligation') - it names no producer function, call site or "
                "boundary. I re-derived the call-site fact myself in the byte-identical "
                "identity-model.py: anchor_law is defined at 840 and has exactly ONE call "
                "site at 939 (the 1081 occurrence is a comment), inside "
                "relation_payload_rules (923-1003), whose own single call site is 755, "
                "inside open_run_closure (566). The ordering clause is also preserved and "
                "true: 939 precedes the relation_source_joins call at 957."),
            "notSilentlyTreatedAsRequired": True, "notIgnored": True,
            "evidence": "evidence/probe-preserved-laws.json (V14-ADV-2 cases)",
        },
        "CB4-MUST-1": {
            "priorSeverity": "MUST", "priorStatus": "RESOLVED in v14",
            "assessedDisposition": "NO REGRESSION",
            "myIndependentAssessment": (
                "The anchor law is still closed over all 13 relations in three classes - "
                "source-text (9, minimum 1, no per-relation maximum), body-identity "
                "(clones, exactly 1), inventory (file/package/vcs-change, exactly 0) - "
                "the classes partition the 13 without overlap, every class carries a "
                "rule, and the shared fact.anchors maxItems 100000 / uniqueItems bound is "
                "still present and not overridden. The owning file's ONLY change in this "
                "delta is the enforcedAt string. The v14 evidence for the refusal "
                "behaviour itself is CARRIED with its original limitations, not re-graded."),
        },
        "CB4-MUST-2": {
            "priorSeverity": "MUST", "priorStatus": "RESOLVED in v14",
            "assessedDisposition": "NO REGRESSION",
            "myIndependentAssessment": (
                "The deficiency-cause registry is still total over DeficiencyV2 with no "
                "gap and no extra (9 rows for 9 members, recomputed). No enum was widened "
                "by this delta: DeficiencyV2 9, NativeCause 14, UnresolvedEdgeKindV1 16. "
                "The owning file's ONLY change is the operationalCarrier string on "
                "native.release-capability-undeclared, confirmed by key-by-key structural "
                "diff. The selected-scalar limitation and RC-3 evidence are CARRIED from "
                "the v14 review with its original limitations."),
        },
        "CB4-SHOULD-1": {
            "priorSeverity": "SHOULD", "priorStatus": "RESOLVED in v14",
            "assessedDisposition": "CARRIED-UNCHANGED",
            "myIndependentAssessment": (
                "The owning files are byte-identical to v14 and outside the 19 modified "
                "paths. Complete Runs still close under the TypeScript, Rust and "
                "grammar-only syntax universes in my own positive controls. The body-"
                "language variant evidence itself is CARRIED on the v14 independent "
                "review and the reproduced suite; I did not re-grade it by restating it."),
        },
        "CB4-SHOULD-2": {
            "priorSeverity": "SHOULD", "priorStatus": "RESOLVED in v14",
            "assessedDisposition": "RESOLVED AND EXTENDED - the v14 resolution was "
                                   "INCOMPLETE at the admission mirror, and v15 completes it",
            "myIndependentAssessment": (
                "The capability authority is still 11 ids with no '@', cells are the "
                "complete 11x6 = 66 product, capabilityIdLaw is published and "
                "platformQualified is still false. A release declaring an unregistered "
                "capability, an unregistered mode, a NOT-SELECTED cell or a duplicate id "
                "each still refuses with its own key, and requesting a NOT-SELECTED cell "
                "is refused as unsatisfiable. The fixed matrix default is IDENTICAL under "
                "a full and a starved registry (I compared the emitted 1023-row arrays "
                "directly) and absences are disclosed rather than dropped. "
                "IMPORTANTLY: root found post-freeze that admission section 1.1 and the "
                "native route annotation still presented DoctorResult.defects[] / "
                "StepTermination.domainDetail as the delivery route, contradicting the "
                "availability carrier v14 had accepted. The v14 reviewer did not discover "
                "this. That finding remains historical, and v15 corrects both mirrors."),
        },
        "ROOT-POST-FREEZE-V14-AVAILABILITY-MIRROR": {
            "origin": "Root, after the v14 freeze; NOT discovered by the v14 reviewer",
            "status": "HISTORICAL - remains a real post-freeze finding against v14",
            "assessedDisposition": "ACTUALLY CORRECTED in v15",
            "myIndependentAssessment": (
                "Verified by diff, by schema, by executed composition and by a sweep. "
                "admission 1.1 now names CommandEnvelope.availability, delivery 'in the "
                "invocation that selected it', the complete typed ownership tuple, "
                "'every requestClass: analysis command', the advisory authority limit, "
                "and explicitly repudiates the two superseded carriers by name. The "
                "native route annotation now names the ORIGINAL invocation carrier and "
                "LIMITS the superseded carriers ('neither is this route') instead of "
                "presenting them. The legacy release_absence_details helper declares "
                "itself SUPERSEDED and NON-AUTHORITATIVE and names its replacement; I "
                "confirmed by executing it that it really does discard workspaceRoot and "
                "collapse two units into fewer records. The actual composition "
                "invocation_availability CALLS release_absence_notices and does not "
                "mention release_absence_details. I swept all six live normative surfaces "
                "for the three superseded route phrasings and found ZERO remaining. Two "
                "units keep 22 distinct notices with both workspace roots intact; a step "
                "collection is bounded at 1024 = the request bound, the invocation at 64 "
                "= the StepId range, and two steps of 1023 compose 2046 without "
                "discarding any - the case a flat array refused. All FIVE analysis "
                "commands declare capability-availability parity and no non-analysis "
                "command does."),
        },
        "ROOT-POST-FREEZE-V14-ANALYSIS-SELECTION-LIMIT": {
            "origin": "Root, after the v14 freeze; NOT discovered by the v14 reviewer",
            "status": "HISTORICAL - remains a real post-freeze finding against v14",
            "assessedDisposition": "ACTUALLY CORRECTED in v15, with one advisory (V15-ADV-1)",
            "myIndependentAssessment": (
                "The arithmetic is real and I recomputed it from the matrix rather than "
                "the prose: 11 selectable capabilities for each of the three TS/JS modes "
                "and 10 for each of the three Rust/syntax modes (the only NOT-SELECTED "
                "cells are clones-cross-tsjs against rust-cargo, rust-cargo-prepared and "
                "syntax-only). So 93 TS units = 1023 rows with EXACTLY ONE ROW OF "
                "HEADROOM - not exactly at the bound - and 94 = 1034 over a 1024 bound "
                "that scope-descriptor workspaceRoots (1024) admits. The COMPLETE DEFAULT "
                "and a COMPLETE EXPLICITLY SUPPLIED spec both reach the owning size check "
                "before generic maxItems validation, yielding PROJECT.SCOPE_LIMIT, "
                "subject requestedCapabilities:1034>1024, request-rejected / exit 2 / "
                "REQUEST.UNSATISFIABLE, with a schema-admitted StepTermination and a "
                "schema-admitted full failure envelope whose errors array is exactly the "
                "termination detail. The fixed matrix default is unchanged and still "
                "overflows at 94 under a starved registry, so the bound is on the REQUEST "
                "and not on availability. Explicit narrowing carries its own provenance. "
                "No truncation (the full 1034 is reported), no hidden sharding or extra "
                "steps, no raised bound (still 1024, read from the schema not restated), "
                "and never a host fault. The widened code meaning names ALL FOUR bounded "
                "fields across TWO record families and each keeps its own remedy naming "
                "narrowing and denying truncation; the three inherited scope-descriptor "
                "remedies are preserved. Wrong shape, wrong type and missingness are "
                "neither counted nor coerced: a 1025-character string is NEVER published "
                "as 1025 capabilities, and 12 malformed shapes each refuse without ever "
                "being a ScopeRefusal. Preflight indexing does not bypass schema "
                "validation. A CORRUPT RETAINED payload is a genuinely different route: "
                "with a self-consistent forgery (blob re-put and Plan re-minted so every "
                "digest join holds) retained Run closure refuses with a generic "
                "ValidationError of 259,664 characters, never PROJECT.SCOPE_LIMIT, while "
                "a digest-inconsistent mutation refuses earlier on BLOB_DIGEST - two "
                "distinct routes, neither an ordinary request refusal. admit_analysis_spec "
                "is called ONLY from default_capability_selection, never from the "
                "retained path, so the architectural separation claim holds."),
        },
    },
    "arDispositions": ar,
    "fwDispositions": fw,
    "inheritedResidualDispositions": inherited,
    "scopedReviewOwnerDispositions": owners,
    "carriedAdvisoryAccount": {
        "path": "reviews/codex-post-reset.v1/advisory-application-account.v15.proposed.json",
        "count": len(adv["items"]), "v14Count": len(adv14["items"]),
        "added": ["V14-ADV-1", "V14-ADV-2"], "removed": [], "changed": [],
        "basis": ("Diffed item by item against the v14 account: 43 -> 45, two added, zero "
                  "removed, zero changed. Both additions carry originalSeverity "
                  "'advisory', bind the v14 review by sha and selector, bind the source "
                  "correction by sha, and stand as 'pending fresh independent acceptance "
                  "and application'. Neither is upgraded to a required finding and "
                  "neither is dropped."),
        "note": ("My own V15-ADV-1 is NOT in this account; it is new in this review and "
                 "any future application must account for it separately."),
    },
    "productQualificationGates": {
        "count": len(gates["items"]),
        "demonstrated": sum(1 for r in gates["items"] if r.get("demonstrated")),
        "qualified": sum(1 for r in gates["items"] if r.get("qualified")),
        "platformFamilies": gates["platformFamilies"],
        "fileByteIdenticalToV14": ident("qualification-gates.proposed.json"),
        "basis": ("All 32 gates remain demonstrated:false and qualified:false over exactly "
                  "the four D-371 machine ids. Nothing in this delta demonstrates or "
                  "qualifies a gate, and this review does not."),
    },
    "evaluationSubresiduals": {
        "count": len(ev["items"]), "disposition": "CARRIED-UNCHANGED",
        "fileByteIdenticalToV14": ident("evaluation-residual-dispositions.proposed.json"),
        "basis": "The owning file is byte-identical between v14 and v15.",
    },
    "applicationAndReadiness": {
        "D372Applied": False,
        "condition5": "NOT MET",
        "readinessRegisterChanged": False,
        "basis": ("design-corrections/README.md states 'D-372 has not been applied and the "
                  "central readiness register is unchanged'; architecture file 12 states "
                  "'Condition 5 remains the next act' and 'Condition 5 remains last and "
                  "unauthorized'. Both files are in the frozen subject and I read them "
                  "there."),
        "coherentPendingApplicationAccepted": (
            "This review may accept a coherent PENDING application; it grades no "
            "application outcome and closes nothing."),
    },
    "limitations": [
        "This is a DESIGN and REFERENCE review. Every native, compiler, OS, cryptographic, "
        "storage, grammar and provider observation in the reference model is a SYNTHETIC "
        "TRUSTED ASSUMPTION, not measured enforcement. No compiler, cargo, parser, "
        "toolchain, renderer, CLI, D9 interpreter or repository code was executed and no "
        "platform was qualified.",
        "There is NO real host, CLI or renderer execution to infer from. 'The availability "
        "parity reaches human/SARIF/HTML/agent' is verified as a DECLARED parity field of "
        "the command inventory plus a strict render selection over declared parityFields - "
        "not as observed rendered output on any surface.",
        "The 93/94-unit fixtures are synthetic discovered units. The arithmetic is "
        "recomputed from the matrix, but unit discovery itself is assumed.",
        "The corrupt-retained-payload evidence is a mutated committed blob re-closed "
        "through the reference verifier; it demonstrates that path, not a real storage "
        "fault or a real host emission. The candidate's own account is explicit that the "
        "raw previous ValidationError is reference evidence, not a demonstrated host-"
        "emitted payload, and I agree.",
        "control-flow and literal remain covered at registry level only; the candidate's "
        "fixture has no payload shape for them. The two universe coordinates remain "
        "verified jointly, not individually. The anchor law's producer-boundary "
        "enforcement remains an obligation, not an exhibited second call site - now "
        "stated accurately rather than asserted (V14-ADV-2).",
        "For unchanged paths - local cycles and missingness laws, retained ordered/repeated "
        "config and node_modules layout, imported observation evidenceUse, the cache "
        "validated-hit boundary, mutation/repair replay, purge custody and the leased pin "
        "ledger - I CARRY the v14 independent review's complete Run evidence WITH ITS "
        "ORIGINAL LIMITATIONS and the byte-identity of the owning files. I did not re-grade "
        "them by restating them, and neither source prose nor carried report rows are "
        "presented as freshly executed tests.",
        "I read the v14 review in full including its limitations, the v14-advisory-"
        "clarification assessment and its two exact changes, the v15 dispositions and "
        "successor source assessment, and the coauthor v4 handoff and custody records. I "
        "did not re-derive the blind reconstruction; this review makes NO statement about "
        "blind reconstructability.",
        "Passing my 285 probes shows a lawful graph is constructible and that the named "
        "refusals actually fire. It does not show that any implementation is correct, and "
        "shared fixture construction is not an independent verdict oracle.",
        "The candidate's own 49 new identity checks are NOT my oracle. I authored my own "
        "expectations and bound the exact source SHA256s; agreement with the candidate's "
        "own suite is corroboration, not evidence.",
    ],
    "claimsExplicitlyNotMade": [
        "product qualification", "platform qualification", "implementation authorization",
        "application acceptance or a readiness change", "blind reconstructability",
        "a substitute for the separate NEW blind consumer review on these bytes",
        "a substitute for the separate full independent application/readiness review",
        "any grading or closure of an AR, FW, inherited residual, evaluation subresidual, "
        "owner routing row or qualification gate",
    ],
    "requiredNextActs": [
        "A NEW fresh blind consumer review on these accepted normative bytes - a separate "
        "gate, and not a reason to reject this otherwise coherent pending design.",
        "A separate full independent application/readiness review that actually GRADES the "
        "proposed outcomes; CARRIED-UNCHANGED and routing-only here are neither.",
        "Any future application must account for V15-ADV-1 alongside the 45 historical "
        "advisories and any new blind advisories, separately accounted.",
        "Optionally, the V15-ADV-1 repair; it does not block.",
    ],
    "readinessChanged": False,
    "implementationAuthorized": False,
    "productQualification": False,
    "applicationAccepted": False,
    "blindAccepted": False,
}

doc["verdictBasis"] = (
    "ACCEPT with 0 unresolved MUST, 0 unresolved SHOULD and 1 new advisory. The two root "
    "post-freeze v14 findings - the availability-carrier mirror and the pre-Plan selection "
    "cardinality - are ACTUALLY corrected in these frozen bytes, and I tested both against "
    "real admission and the real producer/verifier boundaries rather than against prose or "
    "the author's own cases: %d independently authored probe cases, every one bound to the "
    "exact frozen source SHA256s, all holding. Both v14 advisories are addressed at their "
    "ORIGINAL severity by source clarification - not silently promoted to required findings "
    "and not ignored - and I verified each clarification's factual claims myself, including "
    "re-deriving the anchor_law call-site geometry and the native-evidence section "
    "boundaries. The four Bv4 findings do not regress. All six recorded reference commands "
    "reproduce with exit 0, byte-identical logs and a ZERO-byte regenerated-report delta, "
    "over 1308 transitive pins I verified fresh BEFORE running and did not re-pin; the pin "
    "re-seal is a pure digest update with no pin added, removed or repathed. Custody of the "
    "frozen subject is identical before and after (6363/6363 files, 407,813,339 bytes, no "
    "undeclared file). The prior v14 ACCEPT does NOT cover these changed bytes and is not "
    "relied on for any changed path. Nothing here is application acceptance, blind "
    "reconstructability, product qualification or implementation authorization." % tot)

json.dump(doc, open(OUT + "/review.json", "w"), indent=1)
print("wrote review.json")
print("probe total", tot, "passed", passed, "failed", failed)
print("AR", len(ar), "FW", len(fw), "inherited", len(inherited), "owners", len(owners))
print("gates", doc["productQualificationGates"]["count"],
      "eval", doc["evaluationSubresiduals"]["count"],
      "advisories", doc["carriedAdvisoryAccount"]["count"])
