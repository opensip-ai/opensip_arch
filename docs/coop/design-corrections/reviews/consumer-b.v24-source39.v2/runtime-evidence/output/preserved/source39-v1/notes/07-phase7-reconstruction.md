# Phase 7 reconstruction — invocation, availability, envelopes, D9 (source39)

Workflows citations are to `docs/v2/contracts/product-v1/workflows-and-surfaces.md` in the source39 kit.
- Everything below was computed by `tools/phase7_vectors.py`, `tools/discovery_vectors.py` and `tools/run_termination_vectors.py`. Those tools re-admit committed Runs through `ref/closure.py`.
- Real OS/provider/durability/signing enforcement is future qualification. It was not performed, and that is not a design omission.
- The prior runtime's phase-7 notes are own history only; nothing below reuses their measurements.

## 1. Zero-config chain to receipt (R-CHAIN-ZERO-CONFIG-TO-RECEIPT)

`vectors/chain-zero-config.json` maps each arrow to an executed artifact. Source39 changed these links:

| Arrow | Owner (source39) | Executed artifact |
|---|---|---|
| admitted boundaries → unit discovery | native s1.4 U-8, U-4b.1 (excluded units) | `vectors/discovery-membership.json#u8-boundary` |
| discovery → UnitMembershipV1 + scope-descriptor | native s1.4 U-4b (order, ordinals, row decision (a)-(e), Cargo roots from units); U-9 fallback | `vectors/discovery-membership.json`; Run closure enforces `ENUMERATION_MEMBERSHIP_ORDER` / `_ROW_DERIVATION` over the retained record (`runs/syntax-code~membership-reordered.replay.json` refuses `ENUMERATION_MEMBERSHIP_ORDER:rows`) |
| zero-config default selection | native s1.4 default selection; U-9 (every non-NOT-SELECTED syntax-only cell at `.`); `NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT` | `vectors/multi-unit-missing-caps.json#/defaultAnalysisSpec`; `vectors/discovery-membership.json#u9-*` |
| snapshot source inventory | identity s3 "What sourceInventory contains"; security S3 "Pruned trees and the read set" | `runs/ts-pass.store.json`, which retains the read `node_modules/left-pad/package.json` row joined to the TS context layout. Negatives: `runs/ts-pass~pruned-read-nested-node-modules` and `~pruned-read-vcs-tree` refuse `SNAPSHOT_PRUNED_TREE_NOT_A_READ` |
| analysis-spec → parameters → plan2 | identity s3 parameter class `selectionCardinality` (`ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS`) | `runs/ts-pass~scope-document-duplicate.replay.json` |
| stage spec → registered output schema | identity s3 "Who registers a stage output schema" | every positive's provider closure tree; `runs/syntax-code~stage-output-schema-relation-doc` refuses `STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH` |
| provider returns → fact2/scope2/coverage2/view2 | native s4 producer admission; identity `normalizationSpecificationLaw`, `bodyEligibilityLaw`, `scopeCapabilityLaw` | `runs/*.replay.json#/graphAdmission`; `runs/syntax-code~clone-level-spec-not-in-grammar` refuses `BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE` |
| stage returns → ExecutionInputsV1 | execution-inputs contract s4-s6 (account `targetUniverse` null; eligible clones census) | closure `XI.admit` recomputation over every positive |
| inputs → proof3 → evidence3 → seal3 → run3 | composition s9 | `runs/*.replay.json#/semanticReplay` (byte-equal proof and identities) |
| run3 → termination | foundation/run-termination-contract.v1.md s3-s7 | `vectors/run-termination.json` |
| run3 → commit-inventory / commit-receipt / availability | identity `#/$defs/commit-receipt`, `#/$defs/availability` | `envelopes/receipt-availability.json` |
| run3 + termination → CommandEnvelope | workflows s8-s9 | `envelopes/invocation-disclosure.json`, `single-step.json`, `multi-step.json` |

## 2. Semantic identity vs operational authority; seal vs non-seal steps

- **Operational identities are not semantic authority.** Workflows s1: `RequestId` is minted before admission, and each attempt receives its own `ExecutionId`. Neither is a content identity.
  - Measured: the same `run3` appears under different `RequestId`s in `envelopes/invocation-disclosure.json`.
  - `multi-step.json` cites two Runs under one request.
- **Only `analysis` and `verify` seal or link a `run3`.** Every other step kind is operational and never mints a Run.
- **Receipts are bound by step kind.** Source: `repair.schema.json#/x-opensip-mutation-operation-map/byStepKindReceiptOperation`. Measured in `vectors/authority-and-steps.json#/stepKinds`.
- **Composition of a Run termination.** Run-termination contract s7 applies these joins, measured in `vectors/run-termination.json#/hostComposition`:
  - the receipt, attempt and derivation joins;
  - `authority` omitted beside a committed `runId`;
  - the closed detail allowlist.

## 3. Promise vs installed availability vs override vs prerequisite (R-PROMISE-VS-AVAILABILITY)

`vectors/multi-unit-missing-caps.json` separates four layers:
1. The matrix cell promise.
2. The release registry row. When absent, the result is a notice, never a termination.
3. An explicit `analysis.capabilities` override, which removes notices without changing the promise.
4. The semantic prerequisites:
   - Rust clones need SourceUnitOwnershipV1.
   - Every universe's clones scope is governed by `bodyEligibility`.
   - Types need the resolved rung and derivationPolicy.

Candidate-only `clones-near` / `clones-cross-tsjs` stay selection-account-only.

## 4. Public response from internal refusal (R-PUBLIC-FROM-INTERNAL-REFUSAL, envelopes)

Each envelope takes an actual refusal string emitted by a reference guard. It is normalized by longest registered key and routed by `x-opensip-public-route-registry` with an explicit origin. Errors are composed per `envelopeErrorsComposition`, and the result is validated as a complete `kind=failure` CommandEnvelope major 3:

- `envelopes/config-input.json`
- `retained-external-input.json`
- `host-invalid-internal.json`
- `producer-boundary.json`

`envelopes/public-from-internal.json` carries the origin controls, the unregistered-key control and the 1024-code-point subject elision.

## 5. D9 extension vs inherited contract (R-D9-EXTENSION-PRECEDENCE)

`vectors/d9-extension-precedence.json` compares the selected composition with `coop/artifacts/d9-exit-contract.v1.14.json`:
- `classToExitCode`, errorCodes, reasonCodes and cause precedence are unchanged.
- The selected faultCause set adds exactly `host-invariant` → `SYSTEM.OUTCOME.ILLEGAL_STATE`.
- A checker holding only the inherited artifact refuses that lawful termination. Native s10 lines 3285-3299 record this as the D9 unit's live successor-artifact obligation.

Source39 native s10 (lines 3052-3083) routes three deficiencies to their `COVERAGE.*` codes instead of `VERDICT.INDETERMINATE`: `language-tier-unsupported`, `confidence-floor-unmet` and `required-relation-missing`. `ref/run_termination.py` bridges every cause through `codeMaps.deficiencyToReasonCode`, and `vectors/run-termination.json#/causeBridge` lists every registered cause.

## 6. Receipts and availability (R-DURABLE-RECEIPT-AVAILABILITY)

`envelopes/receipt-availability.json` holds the following for ts-pass:
- commit-inventory and commit-receipt admission;
- availability generations `retained` then `purged`;
- the purge MutationReceiptV1 and its replay delivery receipt.

Receipt signing, fsync and ledger pins were not performed.
