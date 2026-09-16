# Phase 8: which subsystem owns each decision (R-SUBSYSTEM-OWNERS)

The phase-8 comparisons, envelopes and authorization vectors apply these owners. Workflows citations are to
`docs/v2/contracts/product-v1/workflows-and-surfaces.md`, security citations to `security-and-lifecycle.md`, and native
citations to `native-evidence.md`. Detail-code owners are the `owner` field of each row in `public-detail-registry.v1.json`.

## Comparisons and baselines

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| Whether the current Run exists, and its identities (run3, proof3, finding3, fingerprint preimage) | foundation identity/evaluator (`close_run` + composition s9) | identity-schemas.v3 `#/$defs/finding`, `#/$defs/finding-fingerprint`; workflow-projection-contract.v3 s8 ("Foundation `close_run` is the strong public check") | every `cmp-*` Run: `runs/cmp-*.replay.json` |
| Baseline descriptor, baselineId, embedded context documents, retention pins | workflows | workflows s2 lines 256-272; baseline-artifact `#/$defs/BaselineDescriptor`; projection contract s3, s9 | `vectors/baseline-audit.json` |
| ScopeDocument parameter join required for adoption | workflows (projection) | projection contract s3 (`verify_scope_parameter_binding`), s10 | `baseline-audit.json#/adoptionScopeParameterControl` |
| Trust resolution of pivot closures (retained generation / signed release / signed bundle) | security (current trust) | workflows s2 lines 278-283 | not performed (future qualification) |
| Detector compatibility listing: path, bytes, schema | workflows s2 + security S1 tree binding | workflows s2 lines 289-296; detector-manifest schema; projection contract s13-s15 | `vectors/detector-compat-file.json` |
| Listing signature and tree authentication | security TCB | projection contract s14 ("Signature verification remains security TCB") | not performed |
| Pivot chain, classification, first-axis attribution, `subsequentDeltas` | workflows | workflows s3 lines 311-336; projection contract s11-s12 | `baseline-e0-e3.json`, `pivot-only-fingerprints.json` |
| Absence knowledge from emitWhen roots | foundation evaluator proof, consumed by workflows | workflows s3 lines 338-352; projection contract s12, s14 | presence values in every comparison summary |
| E1..E3 substitution and non-substituted input preservation | workflows, joined against foundation inputs | workflows s3 lines 354-363; projection contract s13 | `evaluationInputRefsEqualCurrent` in the pivot views |
| Evidence axis: import2 identity, payload, correspondence and scope digests | identity (import2) + workflows s3/s4 | workflows s3 lines 371-380; comparison-result `EvidenceAvailability`/`BoundImport` | `comparison-evidence-changed.json`, `comparison-missing.json` |
| Audit profile gate semantics and verdict | workflows | workflows s3 lines 382-399; comparison-result `AuditProfile` | `baseline-audit.json#/codeRegressionByProfile` |
| Step termination for a comparison (fail → policy-failed, indeterminate → reason codes) | workflows mapper → D9 unit | invocation-record `ComparisonStepResult.description`; command-inventory v3 goldens | step results in each comparison vector |
| Audit gate ownership (`verdictGate=delegated`) | workflows s1 | workflows s1 lines 213-219 | `baseline-audit.json#/auditInvocationFail` / `auditInvocationPass` |

## Envelopes, authorization and output failures

| Decision | Owner | Selector | Exercised in |
|---|---|---|---|
| D9 class, exit code, cause precedence | D9 exit-contract unit, extended by the selected composition | `coop/artifacts/d9-exit-contract.v1.14.json`; native route registry `hostInvariantSuccessor` | `vectors/d9-extension-precedence.json`, `envelopes/public-termination.json` |
| DomainDetailCode membership | the per-code owner in the public-detail registry | `public-detail-registry.v1.json` (e.g. TEST.*/REPAIR.*/BASELINE.* workflows; evidence.purged/missing identity; evidence.pinned foundation) | membership checked for every golden |
| Test execution admission (argv0, environment, consent, confinement) | workflows s7 with the security grant | workflows lines 928-952, 1421, 1436-1443 | `vectors/test-prep-repair-authorization.json#/testExecution` |
| RepoExecutionGrantV2 bindings and platform truth table | security | security lines 1062-1124 | same (truth-table values copied, not measured) |
| Repair apply authorization bindings | security S10.1 | security lines 1152-1174 | `#/repairApply` |
| Repair journal, apply idempotency, verify | workflows s6 | workflows lines 892-924, 203-211 | `#/repairApply/idempotencyKey` |
| Native preparation AuthorizedExecutionV2, grant set reference | native + security | native lines 3728-3745; native-evidence.schemas.v2 `#/$defs/AuthorizedExecutionV2` | `#/nativePreparation` |
| Pinned purge refusal | foundation (`evidence.pinned`) | workflows lines 1351-1384 | `envelopes/pinned-purge.json` (re-validated) |
| Availability generations; purged / missing classification | identity s5 | identity-schemas.v3 `#/$defs/availability`; projection contract s0 | `envelopes/purge-replay-output-failure.json` |
| Replay refusal on missing bytes | foundation `close_run` | ref/closure.py over a store with one blob removed | same file |
| Required renderer failure after commit | workflows s8 (actual host exception handling is DR-G17/G20 implementation qualification) | workflows lines 995-1010; golden `analyze-renderer-failed-after-commit` | same file |
| Output bound exceeded | identity (EVALUATION.OUTPUT_BOUND_EXCEEDED) under D9 `output-serialization` | projection contract s6 | same file |
| Host-captured work vs candidate-only returns | foundation execution-inputs | execution-inputs.schema.v1 `#/$defs/CandidateProducerResultV1`; native matrix `clones-near` relations [] | `vectors/host-captured-vs-candidate.json` |
| Capability availability notices | native s1.4 + route registry | route `native.release-capability-undeclared` (`notATermination`) | `vectors/multi-unit-missing-caps.json` |
