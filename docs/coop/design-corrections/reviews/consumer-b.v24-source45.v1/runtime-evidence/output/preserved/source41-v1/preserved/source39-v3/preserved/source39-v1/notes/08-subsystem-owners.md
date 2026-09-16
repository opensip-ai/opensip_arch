# Phase 8: which subsystem owns each decision (R-SUBSYSTEM-OWNERS), source39

Workflows citations are to `docs/v2/contracts/product-v1/workflows-and-surfaces.md`, security citations to `security-and-lifecycle.md`,
native citations to `native-evidence.md`, all in the source39 kit. Detail-code owners are the `owner` field of each
`public-detail-registry.v1.json` row.

## Comparisons and baselines

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Whether the current Run exists, and its identities | foundation identity/evaluator (`close_run` + composition s9) | identity-schemas.v3 `#/$defs/finding`, `#/$defs/finding-fingerprint`; composition s7, s9 | every `cmp-*` Run: `runs/cmp-*.replay.json` |
| Baseline descriptor, baselineId, embedded documents, retention pins | workflows | workflows s2; evaluator3 `baseline-artifact.schema.json` | `vectors/baseline-audit.json` |
| Detector identity: `detectorId` = the emission `contributionId`; one detectorClosure row per contribution | workflows | workflows s2 lines 277-287; workflow-projection-contract.v3 s11 line 192 | `vectors/baseline-audit.json`, `vectors/baseline-e0-e3.json` |
| ScopeDocument parameter join required for adoption | workflows (projection) | projection contract s3, s10 | `baseline-audit.json#/adoptionScopeParameterControl` |
| Trust resolution of pivot closures | security (current trust) | workflows s2 lines 289-298 | not performed (future qualification) |
| Detector compatibility listing: path, bytes, schema | workflows s2 + security S1 tree binding | workflows s2 lines 300-321; evaluator3 `detector-manifest.schema.json` | `vectors/detector-compat-file.json` |
| Pivot chain, classification, first-axis attribution, `subsequentDeltas` | workflows | workflows s3 lines 331-358 | `baseline-e0-e3.json`, `pivot-only-fingerprints.json` |
| Presence knowledge on every side (true / false non-selection or evaluated absence / null) and RuleCoverage `absenceKnowledge` | workflows, over foundation proof roots | workflows s3 lines 360-400; evaluator3 comparison-result `#/$defs/PivotPresence`, `#/$defs/RuleCoverage`; projection contract s12 | `vectors/comparison-absence-knowledge.json` and presence values in every comparison summary |
| Closed per-entry IndeterminateReason order | workflows | workflows s3 lines 402-411 | `vectors/comparison-absence-knowledge.json` (`current-absence-unknown`, `baseline-absence-unknown`); `vectors/baseline-e0-e3.json` (`pivot-reevaluation-unavailable`) |
| E1..E3 substitution, non-substituted input preservation | workflows, joined against foundation inputs | workflows s3 lines 423-435 | `evaluationInputRefsEqualCurrent` in pivot views |
| Evidence axis | identity (import2) + workflows s3 | workflows s3 lines 440-449 | `comparison-evidence-changed.json`, `comparison-missing.json` |
| Audit profile gate semantics and verdict | workflows | workflows s3 lines 451-469 | `baseline-audit.json#/codeRegressionByProfile` |
| Step termination for a comparison | workflows mapper → D9 unit | invocation-record `ComparisonStepResult`; command-inventory.v3 goldens | step results in each comparison vector |

## Envelopes, terminations, authorization and output failures

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Whole analysis-Run indeterminate termination: population, cause bridge, order, `coverageId`, candidate check, host composition | foundation host finalizer | `foundation/run-termination-contract.v1.md` s1-s7 | `vectors/run-termination.json` |
| D9 class, exit code, cause precedence, reason-code map | D9 exit-contract unit, extended by the selected composition | `coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps`; native s10 route table | `vectors/d9-extension-precedence.json`, `envelopes/public-termination.json` |
| Public termination goldens (45) | workflows | `workflows/command-inventory.v3.json#/goldens` | `envelopes/public-termination.json` |
| DomainDetailCode membership | per-code owner in the public detail registry | `public-detail-registry.v1.json` | membership checked for every golden |
| Test execution admission; argv digest recipe | workflows s7 with the security grant | workflows lines 1041-1080 (argvDigest lines 1056-1064); security-and-lifecycle line 1074 | `vectors/test-prep-repair-authorization.json#/testExecution` |
| RepoExecutionGrantV2 bindings and platform truth table | security S10 | security-and-lifecycle S10 | same (truth-table values copied, not measured) |
| Repair apply authorization | security S10.1 | security-and-lifecycle S10.1 | `#/repairApply` |
| Native preparation AuthorizedExecutionV2 and grant set reference | native s14 + security | native lines 3870-3900; native-evidence.schemas.v2 `#/$defs/AuthorizedExecutionV2` | `#/nativePreparation` |
| Pinned purge refusal | foundation (`evidence.pinned`) | workflows s12 | `envelopes/pinned-purge.json` |
| Availability generations; purged vs missing | identity s5 | identity-schemas.v3 `#/$defs/availability` | `envelopes/purge-replay-output-failure.json` |
| Required renderer failure after commit | workflows s8/s9 (`DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, committed runId on the termination) | golden `analyze-renderer-failed-after-commit`; evaluator3 common StepTermination | `envelopes/public-termination.json`, `envelopes/purge-replay-output-failure.json` |
| Required projection failure before any Run | workflows s8 (`DELIVERY.REQUIRED_PROJECTION_FAILED`, no runId) | workflows lines 1130, 1207-1208, 1372 | `envelopes/purge-replay-output-failure.json` |
| Host-captured work vs candidate-only returns | foundation execution-inputs | execution-inputs contract s4-s6 | `vectors/host-captured-vs-candidate.json` |
| Capability availability notices | native s1.4 + route registry | route `native.release-capability-undeclared` | `vectors/multi-unit-missing-caps.json` |
| Graph query public carrier | workflows s8 + query projection contract s7 | workflows lines 1197-1239; command-inventory.v3 `queryDispatch.parityPaths` | `vectors/graph-query.json` |
