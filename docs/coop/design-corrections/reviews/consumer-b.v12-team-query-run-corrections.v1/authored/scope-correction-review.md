# Scope correction review — placeholder reconstruction (consumer-b.v12 team v2)

**Verdict: `SCOPE_INCOMPLETE`**

This is not whole-consumer acceptance and not a reaffirmation of historical `ACCEPT-RECONSTRUCTABLE`. The syntax-code pilot validator is independently reviewing v1; its outcome is unused and is not treated as admission. Original 123 accept-blocking requirements remain for later full consumer completion.

Bounded work: replace remaining standalone / schemaEnvelope / config / repair / comparison / invocation / standing / query **explanatory placeholders** with executed reconstruction against each row’s **owning schema**. Frozen Run stores were not rebuilt. Graph algorithm behavior is distinct from whole Run admission.

## Custody

| Object | SHA-256 | Result |
|---|---|---|
| kit manifest | `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8` | match |
| parent | `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb` | match |
| 80 kit files | — | PASS 80/80 |
| requirements.json | `855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495` | unchanged |
| peer `review.md` | `85f53f7ab981c6c8e2c49694ed6334a055a24137dd687c60fee4d8d7c7e884a9` | PASS |
| peer `review.json` | `9316778598b935d4333ed9ca11bacc7ab13f008244ed9050e788cecf9b31a257` | PASS |
| peer `self-audit.md` | `8012fcb4761bb49ed2f5e1569be344add40c66da613b0aa6fcd6d52684f74ccd` | PASS |
| peer `self-audit.json` | `ecbc09b44e610679d378d0a3a625dc59cc80aa3993cdb744bcb31df9c7b60709` | PASS |

Peer grades are not design authority. v1 prescriptions withdrawn in the self-audit (CommandEnvelope-for-all, cell state `indeterminate`, `tsconfigGraphHash` on the graph, nonempty import subjects, ban on synthetic TargetAttributionV1, wait-on-parallel-reviewer, RepairPlanV1 as universal owner) were honored.

## Frozen Run stores (untouched this pass)

| Store | SHA-256 | Bytes |
|---|---|---|
| syntax-code.store.json (corrected v1 pilot) | `2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7` | 867956 |
| ts.store.json | `885b8e4575235fe47fbee893d83e97d650aea230f9af870b8a711f25d943075d` | 642462 |
| rust.store.json | `67dc12f88fc19fb320385d30f6a740197c64ca9d574627b8db81cdb2f2000315` | 496105 |
| syntax-data.store.json | `1d07e4c8040035965a8821559a5916cf82014e19198e1e6acaf6e9b5ecdd6092` | 476183 |
| rust-partial-clones.store.json | `b6c2b240e11fff9699aeeacdd8a68a7ee7119f241029e3de0e4c955e2b058246` | 494017 |

Record: `output/frozen-run-hashes.json`. Historical placeholders: `output/preserved-failures/scope-placeholders-original/`. Path correction: `output/path-correction-record.v2.json`.

## From-scratch command and measured outcome

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v2/output/scripts/scope_reconstruct.py
```

Measured: exit 0; **48** IDs reconstructed this pass; **0** stock-schema failures on those records; five Run store hashes unchanged.

## What was reconstructed (owning records)

| Family | Owning record | Result |
|---|---|---|
| Failure / public / purge / D9 | CommandEnvelope `kind=failure` + StepTermination + DomainDetail | stock-valid; `exitCode` derived from inherited `classToExitCode` |
| Single/multi-step | InvocationRecord major 3 | 1-step analyze; 2-step analyze with profiles `default` vs `fit` |
| Invocation disclosure | command-inventory.v3 extraction | 45 commands; query formats/parityFields |
| Public termination | StepTermination only | six classes |
| D9 precedence | note+vector vs `d9-exit-contract.v1.14.json#/classToExitCode` | maps equal |
| Receipt/availability | identity `commit-receipt` + `availability` | bound to retained syntax-code `run3:f2542b3a…` (synthetic host observation labeled) |
| Config graphs | TypeScriptConfigGraphV1 + `SHA-256(C(graph))` | synthesized `entryConfigPath=null,nodes=[]`; custom multi-base; jsconfig+shared base. Hash is **not** a graph field |
| Comparison/baseline | ComparisonResult / BaselineArtifact | missing/evidence-changed/empty/scope-only/E0 vs E1–E3/pivot-only |
| Authorization | CommandEnvelope refusals | TEST / native-prepare / AUTHZ.POLICY_DOES_NOT_ADMIT_REPAIR |
| Repair / mutation | RepairPlanV1, MutationReplayScopeV1 (`operation=purge`, not repair-apply) | apply-key digest ≠ mutation-scope digest |
| Min-resolution | atom evaluator | syntactic/resolved/type qualifying vs insufficient values computed |
| Clones negatives / JS body / hidden mismatch | executed first-refusal + computed L0 | JS languageId ≠ TS provider identity; L0 pair distinct |
| Ownership stability | independently recomputed L0 pair | stable across ownership at edition 2018; distinct at 2021 |
| Graph query | GraphQueryRequestV1/ResponseV1 | neighbors, path (zero-hop, `maxDepth=1`), reach; unprojectable-fact disclosure for existing TS imports fact; lawful synthetic TargetAttributionV1; cursor page; QUERY.VIEW_UNKNOWN failure envelope; renderer parity from inventory. **`underlyingRunAdmissionUnverified: true`** |
| Three-valued replay | exists + missing Coverage | value `indeterminate`, not vacuous true/false |

Labels SHOULD/advisory/executed in the scope review did **not** waive owning schema or original verbs.

## 134-ID mapping (summary)

Full rows: `scope-correction-review.json#/mapping`.

| thisPassStatus | Count |
|---|---:|
| reconstructed-this-pass | 48 |
| standing-discipline-this-pass | 24 |
| prior-artifact-content-unverified-this-pass | 23 |
| frozen-run-property-untouched | 18 |
| incomplete | 12 |
| frozen-store-untouched | 6 |
| futureQualification | 3 |
| **total** | **134** |

## Remaining obligations (why INCOMPLETE)

1. **`R-REPLAY-EXPORT`** for ts / rust / syntax-data / rust-partial: no from-export complete-proof `replay.json`. Syntax-code already has one. Other-Run rebuild is a later pass; stores stayed frozen.
2. Independent closure / proof replay / root admission of those claimed positives is **not** asserted. Graph queries over the TS store are algorithm measurements, not `close_run`.
3. Rust-partial `clones-fact` cell state was **not** rewritten. Law derives **`partial`** (not `unavailable`/`indeterminate`); derivation is recorded in `vectors/rust-partial-cell-derivation.json`.
4. Historical traces/tables (cap, protocol3, rung matrix, CVE1, …) were not re-derived this pass.
5. Generic `x-opensip-digest` engine and component-manifest security profile remain notReached.
6. All 123 original accept-blocking IDs remain in force for later full consumer completion.

Peer MUST `MUST-REPLAY-EXPORT-EVERY-POSITIVE` is the blocking incomplete item inside this otherwise-executed placeholder reconstruction.
