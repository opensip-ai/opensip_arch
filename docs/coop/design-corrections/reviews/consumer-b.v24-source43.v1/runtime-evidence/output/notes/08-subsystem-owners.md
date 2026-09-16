# Phase 8: which subsystem owns each decision (R-SUBSYSTEM-OWNERS), runtime source42.v1

This note restates my own source41 owner map (`preserved/source41-v1/notes/08-subsystem-owners.md`) for the source42 kit.

Citation sources:
- workflows: `docs/v2/contracts/product-v1/workflows-and-surfaces.md`;
- native: `native-evidence.md`;
- security: `security-and-lifecycle.md`;
- enumeration, execution-inputs and run-termination: `docs/coop/design-corrections/foundation/`;
- detail-code owners: the `owner` field of `public-detail-registry.v1.json` rows.

Only `enumeration-contract.v1.md` and `execution-inputs-contract.v1.md` changed since source41. Line numbers for every other document are those of my source41 map. Every artifact cited was re-executed in this runtime under the `logs/s42-fin-*` labels.

## Run closure

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Which retained descriptors a Run must carry, and whether its typed-prefix output references resolve before replay | foundation identity/evaluator composition | composition s7 lines 72-76; identity s3 identity table, closing digest law, retention modes; identity-schemas.v3 `x-opensip-digest-domains` | `runs/*.replay.fromscratch.json#/retainedClosure`; `vectors/retention-negatives.json` |
| Typed values inside workflow-owned Plan input documents | workflows (the document's own schema admission; waiver target equality of composition s5) | identity s3 lines 597-600, 627-631; composition s5 line 54 | cmp-empty / cmp-budget; advisory A-v2-1 |
| Unit roots, discovery, `unitKind`, mode selection and membership entering PlanId through `membershipDigest` | native | native U-0 lines 626-651; s1.2 lines 516-560; U-1 lines 652-662; U-4b lines 733-804 | `vectors/discovery-membership.json`; `runs/syntax-code~unit-kind-other-family`, `~unit-root-external-sentinel`, `ts-pass~unit-kind-not-mode-projection` |
| **Which program an enumeration binding names, and its entry (source42)** | foundation enumeration, joined to the native universe owner | enumeration contract s1 lines 20-47 (`default-unit` at most once at ordinal 0; `programEntry` null on an available default binding; derived U-1 marker entry vs `TypeScriptConfigGraphV1.entryConfigPath`; explicit entry = `programEntry`); `enumeration-plan.schema.v1.json#/$defs/AvailableProgramBindingV1/properties/programEntry` | closure enumeration admission over every Run; `runs/ts-pass~default-unit-program-entry`, `~explicit-entry-not-graph-entry`, `runs/rust-mixed~default-unit-program-entry`, `runs/syntax-code~second-default-unit-binding` |
| **Which returned views a cell row carries, and which views are candidates (source42)** | foundation execution-inputs | execution-inputs contract s3 line 53 (candidates = complete-receipt `outputRefs`; `selectedRefs` view on no receipt refuses `EXECUTION_INPUTS_SELECTED_COVER`; relation-column attribution); s8 `build_manifest` row | closure `XI.admit` over every Run; `runs/syntax-code~row-view-omitted`, `runs/syntax-code~selected-view-not-on-receipt` |

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
| Presence knowledge and RuleCoverage `absenceKnowledge` | workflows, over foundation proof roots | workflows s3 lines 360-400 | `vectors/comparison-absence-knowledge.json` |
| Closed per-entry IndeterminateReason order | workflows | workflows s3 lines 402-411 | `vectors/comparison-absence-knowledge.json`; `vectors/baseline-e0-e3.json` |
| E1..E3 substitution, non-substituted input preservation | workflows, joined against foundation inputs | workflows s3 lines 423-432 | `evaluationInputRefsEqualCurrent` in pivot views |
| Evidence axis | identity (import2) + workflows s3 | workflows s3 lines 440-449 | `comparison-evidence-changed.json`, `comparison-missing.json` |
| Audit profile gate semantics and verdict | workflows | workflows s3 lines 451-469 | `baseline-audit.json#/codeRegressionByProfile` |
| Step termination for a comparison | workflows mapper → D9 unit | invocation-record `ComparisonStepResult`; command-inventory.v3 goldens | step results in each comparison vector |

## Envelopes, terminations, authorization and output failures

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Whole analysis-Run indeterminate termination and host composition | foundation host finalizer | run-termination contract s1-s7; s6 step 1 key line 173; s7.3 lines 240-270; s7.5 lines 294-324; s7.6 lines 326-336 | `vectors/run-termination.json` |
| D9 class, exit code, cause precedence, reason-code map | D9 exit-contract unit, extended by the selected composition | `coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps`; native s10 lines 3069-3079, 3274-3327 | `vectors/d9-extension-precedence.json`, `envelopes/public-termination.json` |
| Public termination goldens (45) | workflows | `workflows/command-inventory.v3.json#/goldens`; workflows s9 lines 1353-1417 | `envelopes/public-termination.json` |
| DomainDetailCode membership | per-code owner in the public detail registry | `public-detail-registry.v1.json` | every golden |
| Test execution admission; argv digest recipe | workflows s7 with the security grant | workflows lines 1046-1088 (argv digest lines 1061-1067); security-and-lifecycle line 1074 | `vectors/test-prep-repair-authorization.json#/testExecution` |
| RepoExecutionGrantV2 bindings and platform truth table | security S10 | security-and-lifecycle S10 | same (values copied, not measured) |
| Repair apply authorization | security S10.1 | security-and-lifecycle S10.1 | `#/repairApply` |
| Native preparation AuthorizedExecutionV2 | native s5.2 and s14 + security | native lines 2416-2484 and 3898-3928 | `#/nativePreparation` |
| Pinned purge refusal | foundation (`evidence.pinned`) | workflows s12 (from line 1454) | `envelopes/pinned-purge.json` |
| Availability generations; purged vs missing | identity s5 | identity-schemas.v3 `#/$defs/availability` | `envelopes/purge-replay-output-failure.json` |
| Required renderer failure after commit | workflows s8/s9 | golden `analyze-renderer-failed-after-commit` | `envelopes/public-termination.json` |
| Required projection failure before any Run | workflows s8 | workflows lines 1135, 1213, 1377 | `envelopes/purge-replay-output-failure.json` |
| Host-captured work vs candidate-only returns | foundation execution-inputs | execution-inputs contract s3-s6 (lines 49-259) | `vectors/host-captured-vs-candidate.json` |
| Capability availability notices | native s1.4 + route registry | route `native.release-capability-undeclared` | `vectors/multi-unit-missing-caps.json` |
| Graph query public carrier | workflows s8 + query projection contract s7 | workflows lines 1204-1230; command-inventory.v3 `queryDispatch.parityPaths` | `vectors/graph-query.json` |
