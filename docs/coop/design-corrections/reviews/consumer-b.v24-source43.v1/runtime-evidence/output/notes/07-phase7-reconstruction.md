# Phase 7 reconstruction — invocation, availability, envelopes, D9 (runtime source42.v1)

**Standing**
- This note restates my own source41 phase-7 map (`preserved/source41-v1/notes/07-phase7-reconstruction.md`) for the source42 kit. The only changed documents are the enumeration and execution-inputs contracts (`vectors/phase0-custody.json#/kitDeltaFromPriorOwnCustodyRows`).
- Every artifact named below was re-executed in this runtime:
  - `logs/s42-fin-p4to9.3.phase7_vectors.log`;
  - `logs/s42-fin-disc.*`;
  - `logs/s42-fin-p4to9.8.run_termination_vectors.log`;
  - `logs/s42-fin-mut.0.replay_all.log`.
- Assertion results are recorded by `tools/checkpoint_p7.py` (checkpoint 7). The unchanged ported helpers' runs are kept under `logs/s42-original*` and `preserved/pre-s42/logs/`.
- Real OS, provider, durability and signing enforcement is future qualification. It was not performed, and that is not a design omission.

## 1. Zero-config chain to receipt (R-CHAIN-ZERO-CONFIG-TO-RECEIPT)

`vectors/chain-zero-config.json` maps each arrow to an executed artifact.

| Arrow | Owner | Executed artifact |
|---|---|---|
| admitted boundaries → unit discovery | native U-8 (lines 805-852), U-4b.1 | `vectors/discovery-membership.json#u8-boundary` |
| unit roots | native U-0 (lines 626-651) | `vectors/discovery-membership.json#u0-*`; `runs/syntax-code~unit-root-external-sentinel` |
| mode selection per configuration marker | native U-1 (lines 652-662), s1.2 (lines 516-560) | `vectors/discovery-membership.json#s12-effective-allowjs-mode-selection` |
| discovery → UnitMembershipV1 + scope-descriptor | native U-4b (lines 733-804); U-9 fallback | `vectors/discovery-membership.json`; `runs/syntax-code~membership-reordered`, `~unit-kind-other-family`, `runs/ts-pass~unit-kind-not-mode-projection` |
| **U-1 unit / Plan selection → EnumerationPlanV1 program bindings (source42)** | foundation enumeration contract s1 (lines 20-47) | every Run's enumeration admission (`programEntry` null on default bindings; derived U-1 marker entry equals the retained `entryConfigPath`); `runs/ts-pass~default-unit-program-entry`, `~explicit-entry-not-graph-entry`, `runs/rust-mixed~default-unit-program-entry`, `runs/syntax-code~second-default-unit-binding` |
| zero-config default selection | native s1.4; U-9 | `vectors/multi-unit-missing-caps.json#/defaultAnalysisSpec`; `vectors/discovery-membership.json#u9-*` |
| snapshot source inventory | identity s3 "What sourceInventory contains"; security S3 | `runs/ts-pass.store.json`; `runs/ts-pass~pruned-read-*` refuse `SNAPSHOT_PRUNED_TREE_NOT_A_READ` |
| analysis-spec → parameters → plan2 | identity s3 parameter `selectionCardinality` | `runs/ts-pass~scope-document-duplicate.replay.json` |
| stage spec → registered output schema | identity s3 "Who registers a stage output schema" | every positive; `runs/syntax-code~stage-output-schema-relation-doc` |
| provider returns → fact2/scope2/coverage2/view2 | native s4; identity `normalizationSpecificationLaw`, `bodyEligibilityLaw`, `scopeCapabilityLaw` | `runs/*.replay.json#/graphAdmission` |
| stage returns → ExecutionInputsV1 | execution-inputs contract s3 (line 53: candidates are complete-receipt views; attribution totality), s4, s5, s6 | closure `XI.admit` over every Run; `runs/syntax-code~row-view-omitted` (`EXECUTION_INPUTS_VIEW_TOTALITY`), `runs/syntax-code~selected-view-not-on-receipt` (`EXECUTION_INPUTS_SELECTED_COVER`) |
| inputs → proof3 → evidence3 → seal3 → run3 | composition s9 | `runs/*.replay.json#/semanticReplay` (byte-equal proof and identities) |
| retained output graph closed before replay | composition s7 | `runs/*.replay.fromscratch.json#/retainedClosure` and `#/semanticReplay/reachableOutputSet`; `vectors/retention-negatives.json` |
| run3 → termination | run-termination contract s3-s7 | `vectors/run-termination.json` |
| run3 → commit-inventory / commit-receipt / availability | identity `#/$defs/commit-inventory`, `#/$defs/commit-receipt`, `#/$defs/availability` | `envelopes/receipt-availability.json` |
| run3 + termination → CommandEnvelope | workflows s8-s9 | `envelopes/invocation-disclosure.json`, `single-step.json`, `multi-step.json` |

## 2. Semantic identity vs operational authority; seal vs non-seal steps

- **Operational identities are not semantic authority.** `RequestId` and `ExecutionId` are operational (workflows s1). The same `run3` appears under different `RequestId`s (`envelopes/invocation-disclosure.json`).
- **Only `analysis` and `verify` seal or link a `run3`.** Receipts are bound by step kind through `repair.schema.json#/x-opensip-mutation-operation-map/byStepKindReceiptOperation` (`vectors/authority-and-steps.json#/stepKinds`).
- **Run-termination host composition.** Measured in `vectors/run-termination.json#/hostComposition`, including the four derivation-binding refusals.

## 3. Promise vs installed availability vs override vs prerequisite (R-PROMISE-VS-AVAILABILITY)

`vectors/multi-unit-missing-caps.json` keeps four layers apart:
1. the matrix promise;
2. the release registry row (absent → notice, never a termination);
3. the explicit `analysis.capabilities` override;
4. semantic prerequisites.

Candidate-only `clones-near` / `clones-cross-tsjs` stay selection-account-only.

## 4. Public response from internal refusal (R-PUBLIC-FROM-INTERNAL-REFUSAL, envelopes)

Each envelope takes an actual refusal string emitted by a reference guard. It is normalized by longest registered key, routed by `x-opensip-public-route-registry` with an explicit origin, and validated as a complete `kind=failure` CommandEnvelope major 3. Exhibits:
- `envelopes/config-input.json`
- `retained-external-input.json`
- `host-invalid-internal.json`
- `producer-boundary.json`
- `public-from-internal.json`

## 5. D9 extension vs inherited contract (R-D9-EXTENSION-PRECEDENCE)

`vectors/d9-extension-precedence.json`:
- The selected composition adds exactly `host-invariant` → `SYSTEM.OUTCOME.ILLEGAL_STATE`.
- A checker holding only `d9-exit-contract.v1.14.json` refuses that lawful termination (advisory A-c2).
- Native s10 routes deficiencies through `codeMaps.deficiencyToReasonCode` (`vectors/run-termination.json#/causeBridge`).

## 6. Receipts and availability (R-DURABLE-RECEIPT-AVAILABILITY)

`envelopes/receipt-availability.json` holds, for ts-pass:
- commit-inventory and commit-receipt admission;
- availability generations `retained` then `purged`;
- the purge MutationReceiptV1.

Signing, fsync and ledger pins were not performed.
