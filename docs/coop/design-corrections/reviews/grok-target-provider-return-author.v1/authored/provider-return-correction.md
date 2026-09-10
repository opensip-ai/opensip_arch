# Provider-return correction — TargetAttributionV2 typed return channel

**Standing.** Actual Grok DESIGN COAUTHOR continuation of target63. Not acceptance. Not readiness. Not blind standing. Not product implementation. Not commit/push. No source pins sealed. No final-whole acceptance. Fresh peer of target63 is independent; this record does not assume its verdict. Original target63 source `/tmp/opensip-design-corrections/target-identity-successor.v1` remains read-only. Original63 outputs in `grok-target-identity-successor-author.v1/output` are preserved. Isolated work tree: `/tmp/opensip-design-corrections/target-provider-return-successor.v1`.

**Python.** `/tmp/opensip-architecture-review-env/bin/python -I -B`.

---

## 1. Gap that was resolved

Target63 advertised that the fact-producing provider returns typed TargetAttributionV2 companions and that the host captures them into `hostCapture.hostDerivedRefs`. Native-evidence §0, atom/XI, and schema `producerReturn` said protocol3 frames were unchanged. No return field, frame, or interface existed. execution-inputs §7 retained “Remaining stage-`outputDomains` extension is host/adapter work”. A normative consumer could not implement provider delivery.

This successor defines the return **now**, without adding a protocol3 frame and without deferring the required channel as future implementation design.

## 2. Return channel (one shared design)

**Envelope.** `foundation/provider-target-attribution-return.schema.v2.json` `ProviderTargetAttributionReturnV2`:

```
{schemaVersion: 2, planId, producerClosure, stageOrdinal, records: [TargetAttributionV2…]}
```

- Adapter-stage invocation artifact between the language-specific first-party **provider wrapper** and the **shared host adapter**.
- **Not** a protocol3 / typescript-semantic wire frame.
- **Not** a digest-domain blob, Run preimage, `selectedRefs` member, or execution-plan `outputDomain`.
- Captured admitted V2 records remain existing domain=`target-attribution`.
- Portable occupancy identity (file LogicalPath / packageName+packageManifestPath / symbol SubjectIdV1) stays distinct from opaque payload `SubjectIdV1`.

**Invocation.** After this producer’s Analyze-stage fact2 identities are minted from the worker FactBatch, before `attach_host_capture` / `close_run`:

`admit_provider_attribution_return(envelope|null, planId, producerClosure, stageOrdinal, facts, inventories, enumerationPlan, closures, origin)`

in `foundation/provider_attribution_return_model.v2.py`.

| Step | Actor | Contract |
|---|---|---|
| 1 | compiler worker | Unchanged protocol3 / typescript-semantic FactBatch |
| 2 | host adapter | Mint fact2 |
| 3 | language wrapper | Build envelope from the **same compiler-native resolution table** used to encode opaque payloads |
| 4 | host adapter | Admit envelope |
| 5 | host adapter | Capture admitted V2 records into `hostDerivedRefs` |
| 6 | host adapter | `attach_host_capture` then `close_run` |

**Missing envelope:** lawful. Occupancy unknown except exact-id ephemeral. **Not** `required-output-pointer-omitted`.
**Present partial records:** lawful omission of unlisted facts.
**Extra/unknown fact:** `PROVIDER_RETURN_UNKNOWN_FACT`.
**Refused envelope:** captures nothing.
**Order:** records strict unique utf-8 of `sourceFactId`. Capture refs canonical-set of `{domain,digest}`.

Wire extension is **not** necessary. Protocol3 stays closed. No silent invented frame. No version/transition plan because this is not a wire change.

## 3. How each current producer supplies the mapping

Occupancy mapping is the **second output of the same encoding pass** that writes opaque `SubjectIdV1` payloads. Host MUST NOT parse `namespace:opaque` and MUST NOT treat arbitrary host filesystem or package-manager data as provider attestation. File/package target support remains advertised and is supplied by the wrapper table, not denied.

| Mode | Worker (unchanged) | Wrapper supply |
|---|---|---|
| `ts-tsconfig`, `js-allowjs`, `js-synthesized` | typescript-semantic major 2 | After fact2 mint, one V2 per minted resolved-target / resolved-binding / resolved-callee / `to` / `reachable` fact the compiler-native table can attribute, or omit (unknown). File first-party: `evaluationNativeId` = inventory LogicalPath. Package first-party: packageName + `packageManifestPath`=row.path. External file/package as occupancy=external. Symbols MAY omit (exact-id ephemeral) or identity-map. Syntactic import/reference/call rungs MUST omit. |
| `rust-cargo`, `rust-cargo-prepared` | rust-semantic protocol major 3 | Same envelope and occupancy law. rustc/cargo resolved path vs package fills the wrapper table during SubjectIdV1 encoding. |
| `syntax-only` | syntax universe | Omit the envelope, or omit every file/package occupancy record. MUST NOT invent file/package occupancy from specifier text. |
| clone/candidate | candidate algorithms | Omit. Member IDs are never evaluation-subject identity. |

## 4. C15 conflict law (reproduced and guarded)

**Operand.** Inventory contains file `nativeSubjectId=file:src/a.ts` (SubjectIdV1 spelling that is also a LogicalPath) **and** file `src/b.ts`. Payload `resolvedTarget` exactly equals `file:src/a.ts`, so ephemeral occupancy identity `I_eph` is first-party `file:src/a.ts`. Sidecar occupancy=first-party `evaluationNativeId=src/b.ts` joins the other inventory row. `_join_sidecar` previously checked kind/exists but not identity agreement; `_reconcile_attribution` overwrote ephemeral `nativeId`.

**Law.** If ephemeral occupancy is first-party identity `I_eph` and sidecar occupancy is first-party identity `I_sc` and `I_eph ≠ I_sc`, refuse `TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT`. Independently known identity cannot be silently rewritten. Occupancy identity is `(kind, evaluationNativeId)` for file/symbol and `(kind, evaluationNativeId, packageManifestPath)` for package.

**Agreement.** Equal identities admit as sidecar+ephemeral. Unknown sidecar keeps ephemeral. External sidecar vs ephemeral first-party remains `TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY`.

Guard is in `atom_model.v1.py` `_join_sidecar`. Reproduced at both atom boundary and return-channel admit.

## 5. Public-route standing (existing evaluator-fault law)

Internal `TARGET_ATTRIBUTION_*` and `PROVIDER_RETURN_*` keys stay internal. They are **not** DomainDetailCode members. No alias. No new D9 code.

Traced existing routes in `evaluator-fault-observation.schema.v3.json` `x-opensip-routes`:

| Internal class | Observation | Public |
|---|---|---|
| Provider-emitted schema (`TARGET_ATTRIBUTION_SCHEMA`, `PROVIDER_RETURN_SCHEMA`, …) | `input-schema-invalid:provider-return` | operational-failed `PROVIDER.PROTOCOL_VIOLATION` `faultCause=provider-protocol` detail **`EVALUATION.INPUT_REFUSED`** |
| Provider-emitted join/conflict (`TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT`, occupancy conflict, unknown fact, …) | `input-join-invalid:provider-return` | same public detail |
| Host-invented mapping (payload parse / arbitrary host data claimed as attestation) | origin `host-internal` | operational-failed `SYSTEM.OUTCOME.ILLEGAL_STATE` `faultCause=host-invariant` detail **`HOST.INVARIANT_VIOLATED`** |

Host retains unmodified diagnostic bytes containing the internal key. Replaced “pending root public-detail/D9 integration” with this exact existing route after tracing. **LIVE D9 successor-artifact remains a future host obligation and is not discharged.** Missing envelope is lawful occupancy-unknown, not `required-output-pointer-omitted`.

## 6. Focused controls (not a full-suite Run)

Schema/atom/capture boundary. `fullRun: false`. No global pin rewrite.

| Check | Result | First failure |
|---|---|---|
| `check-provider-attribution-return.v2.py` | **18/18 pass**, failed 0 | none |
| `check-atoms.v1.py` | **69/69 pass**, failed 0 (was 66; +3 C15) | none |
| `check-evaluator-faults.v3.py` | passed, 40 route/envelope controls including `input-schema-invalid:provider-return` and `input-join-invalid:provider-return` | none |
| `check-execution-inputs.v1.py` | mismatches `[]`; host-derived V2 sidecar still admitted | none |
| `check-semantic-replay.v3.py` | **18/18 pass**, blocked `[]`; `imports-file-first-party-exists` `close_run` `run3:655602a89dfa346614c59f57a7f63550f7ca5eb7a244d97c0cdc4e8119ddd95d` | none |
| `check-query-projection.v3.py` | **not re-run** (python model unchanged; contract prose only) | n/a |

Provider-return cases actually executed: positive file first-party capture into `hostDerivedRefs`; missing envelope lawful omission; present empty records incomplete-not-omission; malformed envelope schemaVersion; malformed null eval id; extra unknown fact; record order; C15 conflict; C15 agreement; partial omit; refused envelope captures nothing; public route schema/provider, conflict/provider, host-invented; internal keys are not DomainDetailCode; LIVE D9 not discharged; stage mismatch; atom-boundary C15 overwrite refuses.

Query-projection 114/114 remains the target63 result and is not reclaimed here.

## 7. Changed paths and hashes

Isolated root: `/tmp/opensip-design-corrections/target-provider-return-successor.v1`.

### New

| Path | bytes | sha256 |
|---|---|---|
| `docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json` | 18012 | `3c6e104f572e17a16071874a498637d940113c9b3724ef8fa9bb3b2e9f43195c` |
| `docs/coop/design-corrections/foundation/provider_attribution_return_model.v2.py` | 6878 | `fb851602d1bdb73140d283e2b40f023f708db9c6cfb351ac2ec56646ae881ff2` |
| `docs/coop/design-corrections/foundation/check-provider-attribution-return.v2.py` | 16118 | `ba4cbe6d84b6ad083e927603aa28d943fcfff7c92b434d7e9183f176fd2629a0` |

### Changed this round (from target63 authored bytes)

| Path | bytes | sha256 |
|---|---|---|
| `docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md` | 23789 | `1934e94cbcd533376c3d82ac8108834df487d9c76a67f00af0bfe16c1cb3d0a3` |
| `docs/coop/design-corrections/foundation/atom_model.v1.py` | 91347 | `2023f8d81d83c57773f1826e8b51d0728d99e617f325374bfb47dc12e6353ec9` |
| `docs/coop/design-corrections/foundation/check-atoms.v1.py` | 91377 | `9984c82fa3f60d5bb712e41d94ee660d2f3d0115196cf55b45ce8e48eda1cb3b` |
| `docs/coop/design-corrections/foundation/target-attribution.schema.v2.json` | 22797 | `484dc8e10e15d93b55880c4e2823b72a0c4c3aa54f3bc56cf232e77da06277e6` |
| `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md` | 17798 | `95a246a40fafc4872c192bf8be3db9c3196f7b1df589af01ed0fad904435e222` |
| `docs/coop/design-corrections/foundation/execution_inputs_model.v1.py` | 71348 | `7e1c29af8f8c341c41a1dc6834ce234bf96dddc957c4d1eda59e52a636d0b9fb` |
| `docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json` | 59559 | `21fc419733d80a61d6368b94b0d2ff81e069c7d75c1d69413568ba6507fd7713` |
| `docs/coop/design-corrections/foundation/shared-profile-decisions.v1.md` | 2201 | `5fc83abae71302ac91b72d07e855b1da119ba8e7b66e9da4fa7bc714090451a8` |
| `docs/coop/design-corrections/foundation/evaluator-fault-contract.v3.md` | 8534 | `af0b57c3d88d89d439b3c9398f41ca161a6ded2001c8b59db0f5bfa818540395` |
| `docs/v2/contracts/product-v1/identity-and-evidence.md` | 119586 | `1e2413cf57c04356fdd3568cc6238195b2cc806d31b37479a34c2a4ffc1a8181` |
| `docs/v2/contracts/product-v1/native-evidence.md` | 267508 | `2e1d582a3b5e16e71af9cb144d426066d798b04fe585efbfc132f98281611e6d` |
| `docs/coop/design-corrections/workflows/query-projection-contract.v3.md` | 19384 | `3be16db345fd81fa8e1624ce4b6324c7e80ae3fb183170babba3c9a29931c46a` |

### Target63 authored files unchanged this round (hashes still target63)

| Path | bytes | sha256 |
|---|---|---|
| `docs/coop/design-corrections/foundation/check-execution-inputs.v1.py` | 61213 | `cedae4090f14f18dcdba7dc87ca7c707c2319dcc7f13cff2fca57d8f8c280ce4` |
| `docs/coop/design-corrections/foundation/check-semantic-replay.v3.py` | 22589 | `e1ff5ee2cd2985b9d12587ec6c3171eda5f7165f07d6ffce8b8219cbc1ca8aca` |
| `docs/coop/design-corrections/foundation/evaluator_semantic_fixture.v3.py` | 39520 | `3eb0f2794fd2e0aa0d5b1585a04f8e118dcddb6928f8962db67c262d9506eb03` |
| `docs/coop/design-corrections/foundation/identity-model.v3.py` | 138007 | `b748ab305d2d4ccb38ab2ffeb91061168334d41bf4d8424280e937488c659f82` |
| `docs/coop/design-corrections/foundation/identity-schemas.v3.json` | 184087 | `366e840db364805f9d90727c81e7ea85331d5ad560a566896a6fecb639405939` |
| `docs/coop/design-corrections/workflows/check-query-projection.v3.py` | 47911 | `23e7246e135daa77361b81601e2e61eacd52b9f5ede6340a03d164136cb23b4f` |
| `docs/coop/design-corrections/workflows/query_projection_model.v3.py` | 54283 | `083b16dcc57ede784b5c20168d22a56733c79ebf4b909286bf952c3925b41b95` |

The envelope is **not** registered as a new identity digest domain. Captured V2 records remain `identity-schemas.v3.json` `byDomain.target-attribution`.

## 8. Remaining root work (not discharged here)

- Pin new envelope schema + changed files into evaluator3/native/workflow/security source-pins. **Not sealed here.**
- Merge separate P7 closure-kind patch into `identity-model.v3.py` after handoff (this authoring still does not edit general `import.producerClosure=provider`).
- Do not rewrite frozen24.
- Regenerate whole-suite receipts only after both patches merge.
- Include v2 schema **and** the new return envelope in next check-array-orders.
- LIVE D9 successor-artifact remains future.
- Query-projection python was not re-run this round.

## 9. What this is not

Not acceptance. Not readiness. Not a sealed pin set. Not a full-suite Run. Not a protocol3 version bump. Not a new DomainDetailCode. Not a new D9 code. Not product implementation.
