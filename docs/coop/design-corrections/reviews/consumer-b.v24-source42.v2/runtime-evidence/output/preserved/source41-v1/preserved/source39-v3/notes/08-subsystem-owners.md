# Phase 8: which subsystem owns each decision (R-SUBSYSTEM-OWNERS), runtime source39.v2

This note restates `preserved/source39-v1/notes/08-subsystem-owners.md` for this runtime; the kit is unchanged. The comparison
and envelope artifacts cited below were re-executed here (`logs/v2-p89.*`, `logs/v2-final-chain.*`), over cmp-* Runs rebuilt after
HC-35 (`logs/v2-build2.*`). This session added two rows: the retained-closure stage and the typed-prefix scope boundary.

Citation sources:
- workflows: `docs/v2/contracts/product-v1/workflows-and-surfaces.md`;
- security: `security-and-lifecycle.md`;
- native: `native-evidence.md`;
- detail-code owners: the `owner` field of `public-detail-registry.v1.json` rows.

## Run closure (new rows)

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Which retained descriptors a Run must carry, and whether its typed-prefix output references resolve in their prefix-selected domain before replay | foundation identity/evaluator composition | composition s7 lines 72-76; identity s3 identity table, closing digest law, retention modes, lines 616-617; identity-schemas.v3 `x-opensip-digest-domains` (byDomain, domainSets joins, closureMembership, closureKinds) | `runs/*.replay.json#/retainedClosure`; `vectors/retention-negatives.json`; `selfcheck/prepost-matrix.json` |
| Typed values inside workflow-owned Plan input documents (WaiverSetV1 `target.fingerprint`, PolicyDocumentV2 import addresses) | workflows (the document's own schema admission; waiver target equality of composition s5) | identity s3 lines 597-600, 627-631; composition s5 line 54 | cmp-empty / cmp-budget (a waiver fingerprint with no occurrence); advisory A-v2-1 |

## Comparisons and baselines

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Whether the current Run exists, and its identities | foundation identity/evaluator (`close_run` + composition s9) | identity-schemas.v3 `#/$defs/finding`, `#/$defs/finding-fingerprint`; composition s7, s9 | every `cmp-*` Run: `runs/cmp-*.replay.json` |
| Baseline descriptor, baselineId, embedded documents, retention pins | workflows | workflows s2; evaluator3 `baseline-artifact.schema.json` | `vectors/baseline-audit.json` |
| Detector identity (`detectorId` = emission `contributionId`) | workflows | workflows s2 lines 277-287; projection contract s11 line 192 | `vectors/baseline-audit.json`, `vectors/baseline-e0-e3.json` |
| ScopeDocument parameter join required for adoption | workflows (projection) | projection contract s3, s10 | `baseline-audit.json#/adoptionScopeParameterControl` |
| Trust resolution of pivot closures | security (current trust) | workflows s2 lines 289-298 | not performed (future qualification) |
| Detector compatibility listing | workflows s2 + security S1 tree binding | workflows s2 lines 300-321; evaluator3 `detector-manifest.schema.json` | `vectors/detector-compat-file.json` |
| Pivot chain, classification, first-axis attribution, `subsequentDeltas` | workflows | workflows s3 lines 331-358 | `baseline-e0-e3.json`, `pivot-only-fingerprints.json` |
| Presence knowledge and RuleCoverage `absenceKnowledge` | workflows, over foundation proof roots | workflows s3 lines 360-400; comparison-result `#/$defs/PivotPresence`, `#/$defs/RuleCoverage` | `vectors/comparison-absence-knowledge.json` |
| Closed per-entry IndeterminateReason order | workflows | workflows s3 lines 402-411 | `vectors/comparison-absence-knowledge.json`; `vectors/baseline-e0-e3.json` |
| E1..E3 substitution, non-substituted input preservation | workflows, joined against foundation inputs | workflows s3 lines 423-435 | `evaluationInputRefsEqualCurrent` in pivot views |
| Evidence axis | identity (import2) + workflows s3 | workflows s3 lines 440-449 | `comparison-evidence-changed.json`, `comparison-missing.json` |
| Audit profile gate semantics and verdict | workflows | workflows s3 lines 451-469 | `baseline-audit.json#/codeRegressionByProfile` |
| Step termination for a comparison | workflows mapper → D9 unit | invocation-record `ComparisonStepResult`; command-inventory.v3 goldens | step results in each comparison vector |

## Envelopes, terminations, authorization and output failures

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Whole analysis-Run indeterminate termination | foundation host finalizer | `foundation/run-termination-contract.v1.md` s1-s7 | `vectors/run-termination.json` |
| D9 class, exit code, cause precedence, reason-code map | D9 exit-contract unit, extended by the selected composition | `coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps`; native s10 route table | `vectors/d9-extension-precedence.json`, `envelopes/public-termination.json` |
| Public termination goldens (45) | workflows | `workflows/command-inventory.v3.json#/goldens` | `envelopes/public-termination.json` |
| DomainDetailCode membership | per-code owner in the public detail registry | `public-detail-registry.v1.json` | every golden |
| Test execution admission; argv digest recipe | workflows s7 with the security grant | workflows lines 1041-1080; security-and-lifecycle line 1074 | `vectors/test-prep-repair-authorization.json#/testExecution` |
| RepoExecutionGrantV2 bindings and platform truth table | security S10 | security-and-lifecycle S10 | same (values copied, not measured) |
| Repair apply authorization | security S10.1 | security-and-lifecycle S10.1 | `#/repairApply` |
| Native preparation AuthorizedExecutionV2 | native s14 + security | native lines 3870-3900; `#/$defs/AuthorizedExecutionV2` | `#/nativePreparation` |
| Pinned purge refusal | foundation (`evidence.pinned`) | workflows s12 | `envelopes/pinned-purge.json` |
| Availability generations; purged vs missing | identity s5 | identity-schemas.v3 `#/$defs/availability` | `envelopes/purge-replay-output-failure.json` |
| Required renderer failure after commit | workflows s8/s9 | golden `analyze-renderer-failed-after-commit` | `envelopes/public-termination.json`, `envelopes/purge-replay-output-failure.json` |
| Required projection failure before any Run | workflows s8 | workflows lines 1130, 1207-1208, 1372 | `envelopes/purge-replay-output-failure.json` |
| Host-captured work vs candidate-only returns | foundation execution-inputs | execution-inputs contract s4-s6 | `vectors/host-captured-vs-candidate.json` |
| Capability availability notices | native s1.4 + route registry | route `native.release-capability-undeclared` | `vectors/multi-unit-missing-caps.json` |
| Graph query public carrier | workflows s8 + query projection contract s7 | workflows lines 1197-1239; command-inventory.v3 `queryDispatch.parityPaths` | `vectors/graph-query.json` |
