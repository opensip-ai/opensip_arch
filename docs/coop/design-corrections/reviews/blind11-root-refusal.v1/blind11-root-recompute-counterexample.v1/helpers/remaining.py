"""Phase 6–8 standalone vectors and envelopes reconstructed from kit schemas."""
from __future__ import annotations

from helpers.canonical import C, H_id, sha256_hex
from helpers.graph import PROJECT
from helpers.status import dump_json
from helpers.paths import OUTPUT


REQ = "req1_" + "11" * 16
EXEC = "exec1_" + "22" * 16


def envelope_failure(*, code: str, remedy: str, error_code: str = "REQUEST.PRECONDITION_FAILED", extra=None, origin: str):
    env = {
        "schemaFamily": "opensip.product.envelope",
        "schemaMajor": 3,
        "kind": "failure",
        "requestId": REQ,
        "projectId": PROJECT,
        "termination": {
            "class": "request-rejected",
            "errorCode": error_code,
            "domainDetail": {"code": code, "remedy": remedy},
        },
        "exitCode": 2,
        "errors": [{"code": code, "remedy": remedy}],
    }
    if extra:
        env["errors"][0].update(extra)
        if "purgeDisclosure" in extra:
            env["termination"]["domainDetail"].update(extra)
    rec = {"envelope": env, "originatingBoundary": origin, "classification": "invalid"}
    return rec


def write_all(run_ts: dict, run_rust: dict) -> dict[str, str]:
    arts = {}
    # --- config vectors ---
    synthesized = {
        "filename": None,
        "origin": "js-synthesized",
        "configOrigin": "synthesized",
        "synthesizerVersion": 1,
        "options": {
            "allowJs": True,
            "checkJs": False,
            "module": "node16",
            "moduleResolution": "node16",
            "target": "es2022",
            "noEmit": True,
        },
        "identityNote": "TypeScriptUniverseV2ResolvedInputs.configOrigin=synthesized enters universe H",
        "classification": "valid",
    }
    arts["R-CONFIG-SYNTHESIZED"] = dump_json(OUTPUT / "vectors/config-synthesized.json", synthesized)

    multi = {
        "entry": "tsconfig.app.json",
        "kind": "other",
        "extendsResolved": ["tsconfig.base.json", "tsconfig.strict.json", "tsconfig.base.json"],
        "repeatedBasePrecedence": [
            {"ordinal": 0, "path": "tsconfig.base.json", "role": "first-base"},
            {"ordinal": 1, "path": "tsconfig.strict.json", "role": "middle"},
            {"ordinal": 2, "path": "tsconfig.base.json", "role": "repeated-base-later-wins-on-conflict-but-order-retained"},
        ],
        "law": "TypeScriptConfigGraphV1.extendsResolved preserves declared order including repeats; C never sorts this array (x-opensip-order sequence).",
        "classification": "valid",
    }
    arts["R-CONFIG-CUSTOM-MULTI-BASE"] = dump_json(OUTPUT / "vectors/config-custom-multi-base.json", multi)

    js_shared = {
        "a": {"path": "jsconfig.json", "kind": "jsconfig", "extendsResolved": ["tsconfig.base.json"]},
        "b": {"path": "tsconfig.json", "kind": "tsconfig", "extendsResolved": ["tsconfig.base.json"]},
        "sharedBase": "tsconfig.base.json",
        "classification": "valid",
    }
    arts["R-CONFIG-JS-SHARED-BASE"] = dump_json(OUTPUT / "vectors/config-js-shared-base.json", js_shared)

    js_through_ts = {
        "path": "src/util.js",
        "providerLanguage": "typescript",
        "engineUniverse": "native.semantic-universe.typescript.v2",
        "bodyLanguageId": "javascript",
        "sourceVariant": "js",
        "law": "identity-and-evidence §3 clones: languageId is the BODY language from suffix table, never the engine language field",
        "classification": "valid",
    }
    arts["R-JS-CLONE-BODY-THROUGH-TS"] = dump_json(OUTPUT / "vectors/js-body-through-ts.json", js_through_ts)

    clone_neg = [
        {
            "name": "unlisted-suffix",
            "path": "src/file.unknown",
            "firstRefusal": {"code": "BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN", "gate": "dialect-suffix-table"},
            "masksLater": True,
            "classification": "invalid",
        },
        {
            "name": "partial-ownership-no-body",
            "enumeration": "partial",
            "firstRefusal": {"code": "body-language-owner-unenumerated", "deficiency": "input-closure-incomplete"},
            "masksLater": False,
            "classification": "invalid",
        },
        {
            "name": "zero-anchors-clones",
            "firstRefusal": {"code": "FACT_ANCHOR_CARDINALITY", "relation": "clones"},
            "masksLater": True,
            "classification": "invalid",
        },
    ]
    arts["R-CLONES-NEGATIVE-VECTORS"] = dump_json(OUTPUT / "vectors/clones-negatives.json", {"negatives": clone_neg})

    # repair
    snap = run_ts["snapshotId"]
    plan = run_ts["planId"]
    runid = run_ts["runId"]
    repair_desc = {
        "schemaFamily": "opensip.product.repair-plan",
        "schemaMajor": 2,
        "projectId": PROJECT,
        "snapshotId": snap,
        "evidenceRunId": runid,
        "planId": plan,
        "recipe": {"recipeId": "opensip.repair.rename-symbol", "recipeMajor": 1},
        "recipeTrust": "first-party",
        "evidenceOrigin": "native-static",
        "closedWorld": False,
        "targets": [{"path": "src/index.ts", "kind": "file"}],
        "edits": [{"path": "src/index.ts", "startByte": 0, "endByte": 1, "replacementUtf8": "x"}],
        "totalPostimageBytes": 1,
        "evidenceRequirements": [
            {"relation": "file", "minResolution": "enumerated", "completeness": "complete", "satisfied": True}
        ],
        "permittedEditScope": ["src/index.ts"],
        "applicable": True,
        "unmetPreconditions": [],
        "limitations": ["synthetic-descriptor-not-host-apply"],
    }
    arts["R-REPAIR-DESCRIPTOR"] = dump_json(OUTPUT / "vectors/repair-descriptor.json", {"descriptor": repair_desc, "classification": "valid"})
    repair_auth = {
        "authorityBoundary": "security S10.1 repair apply is not a repository-execution grant",
        "perTarget": [
            {"path": "src/index.ts", "requiredConsent": True, "requiredCurrentTrust": True, "requiredClosedWorld": False}
        ],
        "positive": {"targetInScope": True, "consent": True},
        "negative": {
            "targetOutsidePermittedEditScope": True,
            "firstRefusal": {"code": "REPAIR.TARGET_CORRESPONDENCE_UNAVAILABLE"},
            "masksLater": True,
            "classification": "invalid",
        },
        "classification": "valid",
    }
    arts["R-REPAIR-AUTHORITY-PER-TARGET"] = dump_json(OUTPUT / "vectors/repair-authority.json", repair_auth)

    minres = []
    for level, rung, qual, insuf in [
        ("syntactic", "syntactic-specifier", True, False),
        ("resolved", "resolved-target", True, False),
        ("type", "checked", True, False),
        ("syntactic", "syntactic-specifier", False, True),
        ("resolved", "resolved-target", False, True),
        ("type", "checked", False, True),
    ]:
        minres.append(
            {
                "level": level,
                "minResolution": rung,
                "qualifying": not insuf,
                "factsPresent": not insuf,
                "coverage": "complete" if not insuf else "unknown",
                "predicateSatisfied": not insuf,
                "repairEvidenceRequired": True,
                "classification": "valid" if not insuf else "invalid",
            }
        )
    arts["R-MIN-RESOLUTION-THREE-LEVELS"] = dump_json(OUTPUT / "vectors/min-resolution.json", {"cases": minres})
    arts["R-MIN-RESOLUTION-REPAIR-EVIDENCE"] = dump_json(
        OUTPUT / "vectors/min-resolution-repair-evidence.json",
        {"tiedTo": "vectors/min-resolution.json", "requirement": "each level's repair evidenceRequirements.minResolution equals the predicate rung"},
    )
    arts["R-IMPORTED-OBSERVATION-BOUNDARY"] = dump_json(
        OUTPUT / "vectors/imported-observation-boundary.json",
        {
            "mayProve": ["observed runtime hit at mapped grain inside payload window"],
            "mayNotProve": [
                "static absence",
                "Coverage completeness",
                "native resolution",
                "unmapped subject observed",
            ],
            "nullObservationIsUndisclosed": True,
            "classification": "valid",
        },
    )
    mut_scope = {"kind": "mutation-replay-scope", "preimage": ["planId", "recipe", "targets", "edits"], "excludes": ["requestId", "executionId"]}
    apply_key = {"kind": "repair-apply-key", "preimage": ["repairPlanDigest", "consentRecord", "applyAttempt"]}
    arts["R-MUTATION-REPLAY-SCOPE"] = dump_json(OUTPUT / "vectors/mutation-replay-scope.json", {"scope": mut_scope, "C": sha256_hex(C(mut_scope))})
    arts["R-REPAIR-APPLY-KEY"] = dump_json(
        OUTPUT / "vectors/repair-apply-key.json",
        {
            "mutationReplayScopeDigest": sha256_hex(C(mut_scope)),
            "repairApplyKeyDigest": sha256_hex(C(apply_key)),
            "unequal": sha256_hex(C(mut_scope)) != sha256_hex(C(apply_key)),
            "classification": "valid",
        },
    )
    pinned = envelope_failure(
        code="evidence.pinned",
        remedy="revoke named pins under the purge writer lease before purge",
        extra={
            "subject": runid,
            "purgeDisclosure": {
                "runId": runid,
                "activePins": [{"pinId": "pin-baseline-1", "kind": "baseline"}],
                "consequences": [
                    "named-pins-revoked",
                    "dependent-evidence-replay-unavailable",
                    "sealed-history-retained",
                ],
            },
        },
        origin="durable-custody-purge-writer",
    )
    arts["R-PINNED-PURGE"] = dump_json(OUTPUT / "envelopes/pinned-purge.json", pinned)

    # phase 7
    chain = {
        "arrows": [
            {"from": "zero-config-discovery", "to": "typed-config/source", "artifact": "vectors/config-synthesized.json"},
            {"from": "invocation/step/attempt", "to": "analysis-Plan", "artifact": "envelopes/single-step.json"},
            {"from": "Plan", "to": "native facts/Coverage/view", "artifact": str(run_ts["runId"])},
            {"from": "view", "to": "proof verification", "artifact": run_ts["proofId"]},
            {"from": "proof", "to": "Evidence/Seal/Run", "artifact": run_ts["runId"]},
            {"from": "Run", "to": "durable receipt and availability", "artifact": "envelopes/receipt-availability.json"},
        ]
    }
    arts["R-CHAIN-ZERO-CONFIG-TO-RECEIPT"] = dump_json(OUTPUT / "vectors/chain-zero-config-to-receipt.json", chain)
    arts["R-MULTI-UNIT-MISSING-CAPS"] = dump_json(
        OUTPUT / "vectors/multi-unit-missing-caps.json",
        {
            "units": [{"root": "apps/web", "mode": "ts-tsconfig"}, {"root": "crates/core", "mode": "rust-cargo"}],
            "releaseAvailable": ["inventory", "syntax"],
            "advertisedMissing": ["types"],
            "candidateOnly": ["clones-near", "clones-cross-tsjs"],
            "disclosure": "CommandEnvelope.availability notices native.capability-unavailable per (capabilityId, languageMode, workspaceRoot)",
            "classification": "valid",
        },
    )
    arts["R-CANDIDATE-ONLY-CLONES"] = dump_json(
        OUTPUT / "vectors/candidate-only-clones.json",
        {
            "clones-near": "candidate-only; kinds=[] on enumeration cell; no fact2",
            "clones-cross-tsjs": "candidate-only",
            "notSelectedCompleteClones": True,
            "classification": "valid",
        },
    )
    inv_disc = {
        "ownershipFields": ["capabilityId", "languageMode", "workspaceRoot", "required"],
        "boundedCardinality": {"requestedCapabilities.maxItems": 1024, "availability.steps notices": "complete tuple"},
        "ordering": "canonical-set on requestedCapabilities",
        "outputFormats": ["json", "sarif", "html", "agent"],
        "classification": "valid",
    }
    arts["R-INVOCATION-DISCLOSURE"] = dump_json(OUTPUT / "envelopes/invocation-disclosure.json", inv_disc)
    arts["R-SINGLE-STEP"] = dump_json(
        OUTPUT / "envelopes/single-step.json",
        {"command": "analyze", "steps": [{"stepId": 0, "kind": "analysis", "capabilities": ["inventory", "syntax"]}], "classification": "valid"},
    )
    arts["R-MULTI-STEP-DIFFERENT-SELECTIONS"] = dump_json(
        OUTPUT / "envelopes/multi-step.json",
        {
            "invocationName": "analyze-then-compare",
            "steps": [
                {"stepId": 0, "kind": "analysis", "capabilities": ["inventory"]},
                {"stepId": 1, "kind": "analysis", "capabilities": ["clones-fact"]},
            ],
            "classification": "valid",
        },
    )
    arts["R-PUBLIC-FROM-INTERNAL-REFUSAL"] = dump_json(
        OUTPUT / "envelopes/public-from-internal.json",
        {
            "internal": {"boundary": "ADM-TYPE", "code": "SCHEMA_VERSION_TYPE"},
            "public": envelope_failure(code="CONFIG.INVALID", remedy="correct schemaVersion to a JSON integer", origin="capability-manifest-admission")["envelope"],
            "classification": "invalid",
        },
    )
    arts["R-ENVELOPE-CONFIG-INPUT"] = dump_json(OUTPUT / "envelopes/config-input.json", envelope_failure(code="CONFIG.INVALID", remedy="fix configuration types", origin="configuration-input"))
    arts["R-ENVELOPE-EXTERNAL-INPUT"] = dump_json(OUTPUT / "envelopes/retained-external-input.json", envelope_failure(code="EVALUATION.INPUT_REFUSED", remedy="replace retained invalid bytes", origin="retained-external-input"))
    arts["R-ENVELOPE-HOST-INVALID"] = dump_json(
        OUTPUT / "envelopes/host-invalid-internal.json",
        {
            **envelope_failure(code="EVALUATION.PROOF_VERDICT_INCONSISTENT", remedy="host invariant: regenerate from retained inputs", origin="host-generated-internal-record"),
            "d9Class": "operational-failed",
            "note": "invalid host-generated internal record is a host invariant fault, not caller CONFIG.INVALID",
        },
    )
    arts["R-ENVELOPE-PRODUCER-BOUNDARY"] = dump_json(
        OUTPUT / "envelopes/producer-boundary.json",
        envelope_failure(code="EVALUATION.INPUT_REFUSED", remedy="producer protocol violation", origin="producer-boundary"),
    )
    arts["R-FAILURE-ENVELOPES-D9"] = dump_json(
        OUTPUT / "envelopes/failure-composition.json",
        {
            "composition": "D9 class + common DomainDetail + native typed coverage detail",
            "notTerminationFragmentAlone": True,
            "example": envelope_failure(code="CONFIG.INVALID", remedy="see errors[]", origin="d9-composition")["envelope"],
        },
    )
    arts["R-D9-EXTENSION-PRECEDENCE"] = dump_json(
        OUTPUT / "vectors/d9-extension-precedence.json",
        {
            "inherited": "docs/coop/artifacts/d9-exit-contract.v1.14.json",
            "selected": "workflows/schemas/evaluator3/common.schema.json StepTermination",
            "precedence": "product successor grammar and class table; no new D9 enum members from native (native §10 Existing D9 codes only)",
            "classification": "valid",
        },
    )
    arts["R-DURABLE-RECEIPT-AVAILABILITY"] = dump_json(
        OUTPUT / "envelopes/receipt-availability.json",
        {
            "receipt": {
                "schemaVersion": 1,
                "runId": runid,
                "executionId": EXEC,
                "namespaceId": "ns1",
                "commitSequence": 1,
                "inventoryDigest": sha256_hex(b"store-inventory"),
                "sealedAssurance": True,
                "signerKeyId": "aa" * 32,
            },
            "availability": {"schemaVersion": 1, "runId": runid, "generation": 1, "state": "available", "missingRefs": [], "reason": "committed"},
            "classification": "valid",
        },
    )

    # phase 8
    arts["R-BASELINE-AUDIT"] = dump_json(
        OUTPUT / "vectors/baseline-audit.json",
        {"profile": "current-only", "axes": ["code", "policy", "scope", "waiver", "evidence"], "classification": "valid"},
    )
    arts["R-CMP-MISSING"] = dump_json(OUTPUT / "vectors/comparison-missing.json", {"case": "missing-evidence", "classification": "EvidenceAvailability=missing"})
    arts["R-CMP-EVIDENCE-CHANGED"] = dump_json(OUTPUT / "vectors/comparison-evidence-changed.json", {"case": "evidence-changed", "pivot": "finding-key2"})
    arts["R-CMP-EMPTY-RESULT"] = dump_json(OUTPUT / "vectors/comparison-empty-result.json", {"case": "empty-result", "distinctFrom": ["complete-empty", "unavailable", "missing-bytes"]})
    arts["R-TEST-PREP-REPAIR-AUTH"] = dump_json(
        OUTPUT / "vectors/test-prep-repair-authorization.json",
        {
            "testExecution": "explicit authorized test; does not seal run3",
            "nativePreparation": "prepare-code grant; inert prepared outputs",
            "repairApply": "separate consent; S10.1 not repository-code grant",
            "classification": "valid",
        },
    )
    arts["R-PURGE-REPLAY-OUTPUT-FAILURE"] = dump_json(
        OUTPUT / "envelopes/purge-replay-output-failure.json",
        envelope_failure(code="EVALUATION.OUTPUT_BOUND_EXCEEDED", remedy="narrow output or raise bound", origin="output-serialization"),
    )
    arts["R-SCOPE-POLICY-ONLY-COMPARISON"] = dump_json(
        OUTPUT / "vectors/comparison-scope-policy-only.json",
        {
            "unchanged": ["snapshotId", "sourceInventory"],
            "changed": {"ScopeDocumentV1": {"include": ["src/**"], "was": ["**/*"]}},
            "distinctFrom": "source/discovery scope (plan.scopeDigest)",
            "boundDocument": "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1",
            "classification": "valid",
        },
    )
    arts["R-PUBLIC-TERMINATION-EXAMPLES"] = dump_json(
        OUTPUT / "envelopes/public-termination.json",
        {
            "success": {"class": "success"},
            "policy-failed": {"class": "policy-failed", "runId": runid},
            "request-rejected": {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"},
            "indeterminate": {"class": "indeterminate", "reasonCodes": ["QUERY.COMPLETENESS_UNMET"]},
            "operational-failed": {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io"},
            "interrupted": {"class": "interrupted", "signal": "SIGINT"},
            "classification": "valid",
        },
    )
    arts["R-SUBSYSTEM-OWNERS"] = dump_json(
        OUTPUT / "vectors/subsystem-owners.json",
        {
            "identity": "identity-and-evidence / identity-schemas.v3",
            "native": "native-evidence / native-evidence.schemas.v2",
            "evaluator": "composition/atom/enumeration/execution-inputs/fault",
            "workflow": "workflows-and-surfaces / evaluator3 schemas",
            "security": "security-and-lifecycle S1–S16",
            "d9": "d9-exit-contract.v1.14 + common StepTermination",
        },
    )
    arts["R-E0-VS-E1-E3"] = dump_json(
        OUTPUT / "vectors/baseline-e0-e3.json",
        {
            "E0": "prior detector execution recorded in baseline entries",
            "E1-E3": "re-evaluation of current retained evidence without re-running native detectors",
            "classification": "valid",
        },
    )
    arts["R-PIVOT-ONLY-FINGERPRINTS"] = dump_json(
        OUTPUT / "vectors/pivot-only-fingerprints.json",
        {"fingerprintsPresentOnlyInPivots": ["finding-key2:aa" + "bb" * 31], "retainedAs": "pivot-only", "notInCurrentFindings": True},
    )
    arts["R-HOST-CAPTURED-VS-CANDIDATE"] = dump_json(
        OUTPUT / "vectors/host-captured-vs-candidate.json",
        {
            "hostCapturedRequiredWork": "executionInputs.hostCapture.stageReceipts",
            "candidateOnlyReturns": "candidate-producer-result envelopes; not fact2",
            "classification": "valid",
        },
    )
    arts["R-EMPTY-PARTIAL-UNAVAILABLE-MISSING"] = dump_json(
        OUTPUT / "vectors/empty-partial-unavailable-missing.json",
        {
            "complete-empty": "covering available binding + complete inventory + zero selected subjects",
            "partial": "inventory/coverage partial with known rows still evaluated",
            "unavailable": "provider/universe null with typed deficiency pair",
            "missing-committed-bytes": "pointer present, blob absent (retention loss)",
            "classification": "valid",
        },
    )
    arts["R-DETECTOR-COMPAT-FILE"] = dump_json(
        OUTPUT / "vectors/detector-compat-file.json",
        {
            "path": ".opensip/detector-compatibility.json",
            "not": "closure.manifestDigest body",
            "owners": "identity-and-evidence §3 signed-tree Blob; security S1 TreeCommitment",
            "classification": "valid",
        },
    )
    return arts
