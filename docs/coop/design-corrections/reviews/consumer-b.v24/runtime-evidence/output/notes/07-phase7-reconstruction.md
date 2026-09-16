# Phase 7 reconstruction — invocation, availability, envelopes, D9

Workflows citations are to `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (selected by the kit manifest).
Everything below was computed by `tools/phase7_vectors.py`, which re-admits the committed Runs through `ref/closure.py`.
Real OS/provider/durability/signing enforcement is future qualification. It was not performed, and that is not a design omission.

## 1. Zero-config chain to receipt (R-CHAIN-ZERO-CONFIG-TO-RECEIPT)

`vectors/chain-zero-config.json` maps each arrow to an executed artifact:

| Arrow | Owner | Executed artifact |
|---|---|---|
| security admitted boundaries → unit discovery | native s1.4 (U-8), security discovery records | `vectors/multi-unit-missing-caps.json#/units`; `ref/membership.py` inside every `runs/*.replay.json` |
| discovery → UnitMembershipV1 + scope-descriptor | native s1.4 U-1..U-4a | closure re-derivation (`cb24.SCOPE_DESCRIPTOR_DERIVATION`, `cb24.UNIT_MEMBERSHIP_DERIVATION`) passes on all positive Runs |
| release declaration + units → default analysis-spec | native s1.4 default selection; identity `#/$defs/analysis-spec` (`x-opensip-uniqueness` ownership tuple) | `#/defaultAnalysisSpec` (32 rows, admitted) |
| analysis-spec + snapshot → enumeration/emission parameters → plan2 | identity s4, enumeration contract | plan objects in `runs/*.store.json`; closure parameter-cardinality checks |
| CVE1 manifest → capabilityManifestId | CAP-MANIFEST-ID-V1 | `vectors/capability-manifests.json`; closure recomputation |
| plan2 → protocol3 session | native s9, protocol3 transitions | `traces/complete.json`, `unavailable.json`, `cancel.json`, `fault.json`, `terminal.json` |
| provider returns → fact2/scope2/coverage2/view2 | native s4 producer admission | `runs/*.replay.json#/graphAdmission` |
| stage returns → ExecutionInputsV1 | execution-inputs contract | closure `XI.admit` recomputation |
| inputs → proof3 → evidence3 → seal3 → run3 | composition s9 | `runs/*.replay.json#/semanticReplay` (byte-equal proof and identities) |
| run3 → commit-inventory / commit-receipt / availability | identity `#/$defs/commit-receipt`, `#/$defs/availability` | `envelopes/receipt-availability.json` |
| run3 + termination → CommandEnvelope | workflows s8–s9 | `envelopes/invocation-disclosure.json`, `single-step.json`, `multi-step.json` |

## 2. Semantic identity vs operational authority; seal vs non-seal steps

- **Operational identities are not semantic authority.** Workflows s1 lines 75–82: `RequestId` is minted before admission. Each attempt gets an `ExecutionId`. Line 25 names these as operational identities, distinct from the evaluator's content identities.
  - Measured: the same `run3` from `runs/ts-pass.store.json` appears under a different `RequestId` in `envelopes/invocation-disclosure.json`. `multi-step.json` cites two Runs under one request. No Run identity changes.
- **Only `analysis` and `verify` seal or link a `run3`** (lines 79–82). Every other step kind is operational and never mints a Run.
- **Receipts are bound by step kind** (lines 127–149, table 138–143), from `repair.schema.json#/x-opensip-mutation-operation-map/byStepKindReceiptOperation`: `mutation`, `repair-apply`, `import`, `native-preparation`. Measured in `vectors/authority-and-steps.json#/stepKinds`.
- **Retry.** Lines 102–107: `idempotent-retry` is lawful only for analysis/verify/query/render/doctor/export-delivery. `StepSpec.allOf[0]` enforces `retryPolicy none` for the seven non-retry kinds, and the prose and schema agree (measured).
  - Refused by schema: mutation with idempotent-retry; analysis with a `terminal` gate (lines 95–97); `repair-apply` as a generic `mutationClass` (lines 192–193, 203–205).
- **Keys.**
  - Generic mutation key: `H("workflow.mutation-intent", MutationReplayScopeV1)` (lines 109–115).
  - Repair-apply key: raw SHA-256 over `C({operation,projectId,repairPlanId,baseSnapshotId})` (lines 203–206).
  - A replay delivery gets its own `receipt2:` receipt with `replayed=true` and the same key. Measured in `receipt-availability.json`.

## 3. Promise vs installed availability vs override vs prerequisite (R-PROMISE-VS-AVAILABILITY)

`vectors/multi-unit-missing-caps.json` covers 3 units (`""` rust-cargo, `""` js-synthesized, `packages/web` ts-tsconfig):
- **Default selection:** every promised cell, `required=true`, giving 32 rows. The one NOT-SELECTED cell is never requested.
- **Release declaration:** declares only inventory, syntax, calls@ts and clones-fact@{rust,ts}. That yields 23 `native.capability-unavailable` notices in one `CapabilityAvailabilityV1` step. Each notice carries the full `(capabilityId, languageMode, workspaceRoot)` tuple.

The four layers are distinct:
1. **Product promise.** The matrix cell state, `SUPPORTED-DESIGN` for all sampled rows.
2. **Installed availability.** The release registry row. Absent means notice only, never a termination (route `native.release-capability-undeclared` has `notATermination: true`).
3. **Explicit override.** `analysis.capabilities` = [inventory, syntax] shrinks the request to 6 rows with 0 notices. The promise is unchanged.
4. **Semantic prerequisite.** Rust clones need SourceUnitOwnershipV1. TS clones need the source-variant scope law. Types need the resolved rung plus derivationPolicy.

**Candidate-only.** `clones-near` and `clones-cross-tsjs` have `relations: []` and no `capabilityForRelation` preimage, so they project as selection-account-only, not coverage entries. `CandidateProducerResultV1` admits with `authority: candidate-only`. A `semanticEquivalenceClaimed: true` variant is refused by the schema `const`.

## 4. Public response from internal refusal (R-PUBLIC-FROM-INTERNAL-REFUSAL, envelopes)

Each envelope takes an **actual** refusal string emitted by a reference guard. It is normalized by longest registered key, then routed by `x-opensip-public-route-registry` with an explicitly supplied origin (`helperDoesNotGuessOrigin`). Errors are composed per `envelopeErrorsComposition`. Each envelope is schema-validated as a complete `kind=failure` CommandEnvelope, with its exit code taken from the class table:

| Envelope | Internal refusal | Origin | Class / errorCode / faultCause | errors[0].code | Exit |
|---|---|---|---|---|---|
| config-input | `native.requested-capability-unregistered:made-up-capability` | external-configuration | request-rejected / CONFIG.INVALID | CONFIG.INVALID (= termination.domainDetail) | 2 |
| retained-external-input | `native.requested-capability-duplicate-ownership-tuple:calls:ts-tsconfig:.` | externally-supplied-spec | request-rejected / REQUEST.PRECONDITION_FAILED | native.capability-spec-invalid (envelopeDetail) | 2 |
| host-invalid-internal | `native.requested-capability-duplicate-ownership-tuple:inventory:js-synthesized:.` | host-generated-internal-layer | operational-failed / SYSTEM.OUTCOME.ILLEGAL_STATE / host-invariant | HOST.INVARIANT_VIOLATED | 4 |
| producer-boundary | `native.coverage-cause-not-for-deficiency:provider-unavailable:body-language-owner-ambiguous` (cause registry over an admitted ts-pass entry) | producer-boundary | operational-failed / PROVIDER.PROTOCOL_VIOLATION / provider-protocol | native.coverage-cause-unsupported | 4 |

Controls:
- A producer key with origin external-configuration refuses `native.public-route-origin-not-possible`.
- An unregistered key refuses `native.public-route-key-unregistered`.
- The same config key under the host origin becomes operational-failed.
- A 4096-code-point mode value elides to exactly 1024 code points, keeping the key verbatim plus `...#sha256:<hex>`.

The stale selected import uses the published golden `import-stale-selected` (command-inventory v3 `#/goldens`) over the refusal from `runs/ts-pass~import-stale-snapshot.replay.json`.

## 5. D9 extension vs inherited contract (R-D9-EXTENSION-PRECEDENCE)

Checked against `vectors/d9-extension-precedence.json`. `coop/artifacts/d9-exit-contract.v1.14.json` and the selected composition (`native-evidence.schemas.v2.json#/x-opensip-public-route-registry/hostInvariantSuccessor`, evaluator3 common `D9FaultCause`) agree on every point except one:
- **Unchanged:** `classToExitCode`, errorCodes, reasonCodes and cause precedence `[faultCause, rejectionCause, deficiency]`. Every inherited faultCause is preserved.
- **The one difference:** the selected faultCause set has exactly one extra member, `host-invariant`, and its mapped code `SYSTEM.OUTCOME.ILLEGAL_STATE` had no inherited cause preimage. The composition admits the host-invariant StepTermination. A checker holding only the inherited artifact refuses it.

The kit itself publishes this as a MANDATORY, LIVE, CROSS-UNIT `successorArtifactObligation` owed by the D9 exit-contract unit. Adjudication (phase 10): the obligation is disclosed and owned, not concealed. My measurement confirms its stated consequence exactly, so I record it as an advisory for interop consumers and do not raise a new design issue.

## 6. Receipts and availability (R-DURABLE-RECEIPT-AVAILABILITY)

For ts-pass, `envelopes/receipt-availability.json` contains:
- **commit-inventory:** 72 objects and 198 blobs; its raw digest is the commit-receipt `inventoryDigest`.
- **commit-receipt:** admitted.
- **availability:** generation 0 is `retained`. Generation 1 is `purged`, with `missingRefs` naming the proof bundle.
- **Mutation receipts:** the purge `MutationReceiptV1` and its replay-delivery receipt are admitted, plus the kind=mutation envelope.

Not performed: receipt signing, fsync, ledger pins.
