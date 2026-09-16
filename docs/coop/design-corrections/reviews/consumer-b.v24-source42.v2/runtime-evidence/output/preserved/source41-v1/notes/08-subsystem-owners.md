# Phase 8: which subsystem owns each decision (R-SUBSYSTEM-OWNERS), runtime source41.v1

This note restates my own source39 owner map (`preserved/source39-v3/notes/08-subsystem-owners.md`) for the source41 kit.

Citation sources:
- workflows: `docs/v2/contracts/product-v1/workflows-and-surfaces.md`;
- native: `native-evidence.md`;
- security: `security-and-lifecycle.md`;
- execution-inputs and run-termination: `docs/coop/design-corrections/foundation/`;
- detail-code owners: the `owner` field of `public-detail-registry.v1.json` rows.

Line numbers are re-located in the source41 bytes for the five changed documents. For unchanged documents they are the same as in source39. Every artifact cited was re-executed in this runtime under the `logs/s41-fin-*` labels.

## Run closure

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Which retained descriptors a Run must carry, and whether its typed-prefix output references resolve before replay | foundation identity/evaluator composition | composition s7 lines 72-76; identity s3 identity table, closing digest law, retention modes; identity-schemas.v3 `x-opensip-digest-domains` | `runs/*.replay.fromscratch.json#/retainedClosure`; `vectors/retention-negatives.json` |
| Typed values inside workflow-owned Plan input documents (WaiverSetV1 `target.fingerprint`, PolicyDocumentV2 import addresses) | workflows (the document's own schema admission; waiver target equality of composition s5) | identity s3 lines 597-600, 627-631; composition s5 line 54 | cmp-empty / cmp-budget; advisory A-v2-1 |
| Unit roots, discovery, `unitKind`, mode selection and membership that enter PlanId through `membershipDigest` (source41) | native | native U-0 lines 626-651; s1.2 lines 516-560; U-1 lines 652-662; U-4b lines 733-804; `native-evidence.schemas.v2.json#/$defs/InternalUnitRootV1`, `#/$defs/CanonicalRelativeDirV1`, `#/x-opensip-config-node-kind-law` | `vectors/discovery-membership.json`; `runs/syntax-code~unit-kind-other-family`, `~unit-root-external-sentinel`, `ts-pass~unit-kind-not-mode-projection` |
| Which returned views a cell row carries (source41 view attribution) | foundation execution-inputs | execution-inputs contract s3 line 53; `execution-inputs.schema.v1.json` CellProgramOutcomeV1.viewDigests | closure `XI.admit` over every Run; `runs/syntax-code~row-view-omitted` |

## Comparisons and baselines

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Whether the current Run exists, and its identities | foundation identity/evaluator (`close_run` + composition s9) | identity-schemas.v3 `#/$defs/finding`, `#/$defs/finding-fingerprint`; composition s7, s9 | every `cmp-*` Run: `runs/cmp-*.replay.json` |
| Baseline descriptor, baselineId, embedded documents, retention pins | workflows | workflows s2 lines 257-275; evaluator3 `baseline-artifact.schema.json` | `vectors/baseline-audit.json` |
| Detector identity (`detectorId` = emission `contributionId`) | workflows | workflows s2 lines 277-287; projection contract s11 line 192 | `vectors/baseline-audit.json`, `vectors/baseline-e0-e3.json` |
| ScopeDocument parameter join required for adoption | workflows (projection) | projection contract s3, s10 | `baseline-audit.json#/adoptionScopeParameterControl` |
| Trust resolution of pivot closures | security (current trust) | workflows s2 lines 289-298 | not performed (future qualification) |
| Detector compatibility listing | workflows s2 + security S1 tree binding | workflows s2 lines 300-321; evaluator3 `detector-manifest.schema.json` | `vectors/detector-compat-file.json` |
| Pivot chain, classification, first-axis attribution, `subsequentDeltas` | workflows | workflows s3 lines 331-358 | `baseline-e0-e3.json`, `pivot-only-fingerprints.json` |
| Presence knowledge and RuleCoverage `absenceKnowledge` | workflows, over foundation proof roots | workflows s3 lines 360-400; comparison-result `#/$defs/PivotPresence`, `#/$defs/RuleCoverage` | `vectors/comparison-absence-knowledge.json` |
| Closed per-entry IndeterminateReason order | workflows | workflows s3 lines 402-411 | `vectors/comparison-absence-knowledge.json`; `vectors/baseline-e0-e3.json` |
| E1..E3 substitution, non-substituted input preservation | workflows, joined against foundation inputs | workflows s3 lines 423-432 | `evaluationInputRefsEqualCurrent` in pivot views |
| Evidence axis | identity (import2) + workflows s3 | workflows s3 lines 440-449 | `comparison-evidence-changed.json`, `comparison-missing.json` |
| Audit profile gate semantics and verdict | workflows | workflows s3 lines 451-469 | `baseline-audit.json#/codeRegressionByProfile` |
| Step termination for a comparison | workflows mapper → D9 unit | invocation-record `ComparisonStepResult`; command-inventory.v3 goldens | step results in each comparison vector |

## Envelopes, terminations, authorization and output failures

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Whole analysis-Run indeterminate termination and host composition | foundation host finalizer | run-termination contract s1-s7; s6 step 1 key line 173; s7.3 lines 240-270; s7.5 lines 294-324; s7.6 lines 326-336 | `vectors/run-termination.json` |
| D9 class, exit code, cause precedence, reason-code map | D9 exit-contract unit, extended by the selected composition | `coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps`; native s10 lines 3069-3079 (route table), 3274-3327 (origin routes, host-invariant extension, successor artifact) | `vectors/d9-extension-precedence.json`, `envelopes/public-termination.json` |
| Public termination goldens (45) | workflows | `workflows/command-inventory.v3.json#/goldens`; workflows s9 lines 1353-1417 | `envelopes/public-termination.json` |
| DomainDetailCode membership | per-code owner in the public detail registry | `public-detail-registry.v1.json` | every golden |
| Test execution admission; argv digest recipe | workflows s7 with the security grant | workflows lines 1046-1088 (argv digest lines 1061-1067); security-and-lifecycle line 1074 | `vectors/test-prep-repair-authorization.json#/testExecution` |
| RepoExecutionGrantV2 bindings and platform truth table | security S10 | security-and-lifecycle S10 | same (values copied, not measured) |
| Repair apply authorization | security S10.1 | security-and-lifecycle S10.1 | `#/repairApply` |
| Native preparation AuthorizedExecutionV2 | native s5.2 and s14 + security | native lines 2416-2484 and 3898-3928; `#/$defs/AuthorizedExecutionV2` | `#/nativePreparation` |
| Pinned purge refusal | foundation (`evidence.pinned`) | workflows s12 (from line 1454) | `envelopes/pinned-purge.json` |
| Availability generations; purged vs missing | identity s5 | identity-schemas.v3 `#/$defs/availability` | `envelopes/purge-replay-output-failure.json` |
| Required renderer failure after commit | workflows s8/s9 | golden `analyze-renderer-failed-after-commit` | `envelopes/public-termination.json`, `envelopes/purge-replay-output-failure.json` |
| Required projection failure before any Run | workflows s8 | workflows lines 1135, 1213, 1377 | `envelopes/purge-replay-output-failure.json` |
| Host-captured work vs candidate-only returns | foundation execution-inputs | execution-inputs contract s3-s6 (lines 49-259) | `vectors/host-captured-vs-candidate.json` |
| Capability availability notices | native s1.4 + route registry | route `native.release-capability-undeclared` | `vectors/multi-unit-missing-caps.json` |
| Graph query public carrier | workflows s8 + query projection contract s7 | workflows lines 1204-1230; command-inventory.v3 `queryDispatch.parityPaths` | `vectors/graph-query.json` |
