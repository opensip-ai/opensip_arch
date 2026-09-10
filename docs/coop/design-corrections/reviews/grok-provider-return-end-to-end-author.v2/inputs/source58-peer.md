# Provider-return correction — coauthor peer

**Standing.** Actual Grok coauthor peer of source58 bytes. Not blind. Not final-whole acceptance. Not readiness. Not source-pin seal. Not product implementation. Not a protocol3 version bump. Not a new DomainDetailCode or D9 code. Not compiler qualification.

**Verdict: `CORRECTIONS_REQUIRED`.**

A typed wrapper-to-host adapter result is the right *kind* of object (not a wire frame, not a Run preimage, not an `outputDomain`). These contracts still do not make an end-to-end occupancy return executable against original native worker isolation and host TCB. Passing 18 helper controls is a schema/atom/capture precondition, not owning admission.

Source58 hashes match the task manifest (15 files). Frozen24 `target-attribution.schema.v1.json` is untouched. Successor tree bytes for those 15 paths match the inputs. No source was mutated.

---

## 1. Helper preconditions vs owning admission

| Surface | What it is | Result this review | What it is not |
|---|---|---|---|
| `check-provider-attribution-return.v2.py` | Schema/atom/capture helper. Checker standing: “not full Run replay; LIVE D9 not discharged”. `fullRun: false` | **18/18 pass**, failed 0. Independently re-run. | Not `close_run`. Not worker execution. Not suite integration. Not a pin. |
| `check-atoms.v1.py` | Synthetic admitted-map atom unit. Standing: “not full Run replay; not compiler qualification” | **69/69 pass**, failed 0 (includes +3 C15). Independently re-run. | Not occupancy-table supply. Not execution-plan stage join. |
| `check-evaluator-faults.v3.py` | Bounded owner-route controls. Standing: “no LIVE D9 successor artifact or host qualification” | **passed**, count 40, including `input-schema-invalid:provider-return` and `input-join-invalid:provider-return`. Independently re-run. | Not LIVE D9 discharge. |
| Author-claimed `check-execution-inputs.v1.py` / `check-semantic-replay.v3.py` / query 114 | Not re-run here | Unverified this peer | Must not be reclaimed as this correction’s proof. |
| Evaluator3 / native / workflow / security source-pins | Author lists pin of new envelope as remaining | **Not sealed** | No global passing claim. |

The new checker is not referenced from any current suite runner in the successor design-corrections tree (search for `check-provider-attribution-return` outside its own file is empty). Integration remains future work, as the author already recorded.

---

## 2. End-to-end path (MUST) — not executable from these contracts

**Author claim.** After unchanged worker `FactBatch` and host fact2 mint, the language wrapper builds `ProviderTargetAttributionReturnV2` from the **same compiler-native resolution table** used to encode opaque `SubjectIdV1`. Envelope is adapter-stage invocation result, not wire. Protocol3 stays closed.

**Original isolation (owning native/delivery contracts, not a hypothetical API).**

- TypeScript: bundled Node one-shot worker. `retainAfterTerminal: false`, `residentWorker: false`. After one terminal, host closes protocol, waits for clean child exit, destroys scratch. “A child is never retained for a later request.” TypeScript compiler code is never embedded in the Rust host. Worker may construct candidate facts/Coverage; `workerMayMintHostIdentities: false`.
- Rust: one supervised provider process per semantic universe; TCB-accepted compiler process; stdin/stdout length-delimited CBOR. `oneAnalyzePerChild: true`, `residentSession: false`.
- Closed worker-to-host frames: `HelloAck`, `UniverseAccepted`, `SnapshotAccepted`, `FactBatch`, `Coverage`, `Unavailable`, `BudgetExhausted`, `Complete`, `Cancelled`. No TargetAttribution frame. Stdout is protocol-only.

**Data availability contradiction.**

1. Opaque `SubjectIdV1` is already on the wire (`ImportsPayloadV1.resolvedTarget` remains opaque SubjectIdV1). Encoding happens **in the worker** before `FactBatch`.
2. Occupancy is described as the second output of **that same encoding pass**, so the table exists in the worker at encode time.
3. `sourceFactId` is `fact2:…`, minted by the **host** after decoding CBOR and re-encoding to C.
4. `admit_provider_attribution_return` runs after fact2 mint. There is no `build_provider_attribution_return`, no table type, no table lifecycle, no candidateOrdinal join, no `execution_plan` / `stage_receipts` / `views` / `resolution_table` parameter.

After `FactBatch`, the child is on the path to Coverage/Complete/exit. The host then mints fact2. The wrapper that had the table is not specified as still reachable. Closed wire returns only `FactBatch`. This review does **not** invent a shared-memory, leftover-child, or side-channel whose fields and lifecycle are unspecified.

A typed adapter result **can** suffice without a protocol3 frame **if** isolation, invocation, inputs, output, and data availability are concrete. They are not. Prose “trusted first-party language wrapper” plus a host admit of a caller-supplied envelope is not an executable path.

**Probe.** `P-ISOLATION-CONTRACTS`, `P-NO-WRAPPER-BUILD`. `author_claim_holds: false`.

**Operand.** `foundation/provider_attribution_return_model.v2.py` `admit_provider_attribution_return`; `provider-target-attribution-return.schema.v2.json` `x-opensip-return-law.boundary` / `invocation`; native-evidence §9.6; `delivery.v2.json` `typescriptSemanticSubstrate.processModel` and `closedWorkerToHostFrames`; `rust-provider-protocol.v2.json` `protocolIdentity`.

**Remedy.** Specify one closed placement, then type it:

1. **Host-TCB wrapper (same process as admit).** Name the in-host function `build_provider_attribution_return(mintedFacts, retainedTable) -> envelope|null`. Publish the retained-table schema (join key that exists **before** fact2, then bind to minted `fact2`). State how that table is populated if encoding today happens inside the isolated child (today it does). Do not claim “same encoding pass” unless that pass actually runs where the table is retained.
2. **Worker-side wrapper.** Then occupancy must leave the child before exit. That is either a protocol/payload field (for example occupancy keyed by `candidateOrdinal` on or beside `FactBatch`) or a new host-to-worker call. `residentSession: false` / `oneAnalyzePerChild: true` forbid an unspecified callback after Complete. This review will not accept an implicit extra channel.
3. **Do not** parse `SubjectIdV1` on the host to rebuild the table. That remains forbidden host attestation.

Until one of those is specified with required fields and lifecycle, the return channel is not implementable by a normative consumer.

---

## 3. Invocation joins (MUST) — caller-echo, not execution-plan stage

Schema join law: `envelope.stageOrdinal` “equals invocation stageOrdinal **and names the execution-plan stage that minted the facts**.” Also: producerClosure is Plan-selected kind=provider; `sourceFactId` is a fact2 of that Plan **present in a selected view** of that producer.

`admit_provider_attribution_return` compares `envelope.stageOrdinal` to the **caller argument** `stage_ordinal` only. It has no `execution_plan` and no `hostCapture.stageReceipts`. Matching-but-wrong stage 99 with matching caller 99 **admits** and captures `hostDerivedRefs`. Mismatch of envelope 0 vs caller 1 refuses `PROVIDER_RETURN_STAGE_ORDINAL` — that is the author’s helper `test_stage_mismatch`, and it does not test the execution-plan.

Producer: `closures[pc].kind == provider` only. A producer that is kind=provider but **not** the EnumerationPlan selected enumerator **admits**.

Selected views: not an admit operand. V2 join law still requires the fact in a selected view. Later `execution_inputs_model` can join captured refs if they are already in `selectedRefs`; that is a different, later boundary. Return admit does not perform it. `execution_inputs_model.v1.py` does not call `admit_provider_attribution_return`; capture union into `hostDerivedRefs` remains prose step 5.

**Probes.** `P-STAGE-CALLER-ECHO`, `P-PRODUCER-NOT-PLAN-SELECTED`, `P-SELECTED-VIEWS-ABSENT`.

**Remedy.** Pass the admitted execution-plan and `hostCapture.stageReceipts`. Require `envelope.stageOrdinal` equal the receipt ordinal whose Analyze minted **these** facts for **this** `producerClosure`. Require that closure is the Plan-selected enumerator for that stage (`kind=provider`). Require each `sourceFactId` in the minted facts **and** in a selected view of that producer. Do not treat caller-supplied matching integers as that join.

---

## 4. Schema nesting and return-request input (MUST)

**Selected V2 same owner.** Envelope `records.items` is an object with `additionalProperties: true` and required `{schemaVersion, planId, sourceFactId, producerClosure}` only. It does not `$ref` `foundation/target-attribution.schema.v2.json`. An incomplete record with `unknownField` **passes envelope JSON Schema** and **fails** selected V2 (`additionalProperties` false; missing occupancy fields). Python `_admit_target_attributions` later refuses `TARGET_ATTRIBUTION_SCHEMA`. Nesting is model-only, not schema.

**Probe.** `P-SCHEMA-NEST-V2`.

**Remedy.** Envelope `records.items` must `$ref` (or `allOf` + `$ref`) the selected same-owner V2 schema. Keep utf-8 unique `sourceFactId` order on the array.

**Host-invented attestation.** `origin` is a caller argument, default `provider-return`. `origin=host-internal` **admits** and returns nonempty `hostDerivedRefs`. Public routing of host-internal to `HOST.INVARIANT_VIOLATED` exists on `route_internal_key`, but successful capture of host-constructed records is the opposite of “MUST NOT treat arbitrary host data as provider attestation.” Origin capture belongs to the host TCB; the design-reference admit must not be a capture path for `host-internal`.

**Probe.** `P-HOST-INTERNAL-CAPTURES`.

**Remedy.** `admit_provider_attribution_return(..., origin="host-internal")` must refuse without capture. Use `route_internal_key` only as the fault projection. Wrapper-produced envelopes use `origin=provider-return`, recorded by the host TCB, not supplied as an untrusted caller override that still captures.

Unknown extra `sourceFactId` refuses `PROVIDER_RETURN_UNKNOWN_FACT`. Mixed valid+unknown refuses the whole envelope (no capture returned). Refused C15 envelope raises; no refs. Missing envelope `status=omitted`; present empty records `status=admitted` with empty refs. Those parts hold (`P-RUNG-UNKNOWN-ATOMIC`, `P-FAILED-CAPTURE`, `P-MISSING-VS-EMPTY`).

---

## 5. C15 conflict guard — holds on the atom/return admit boundary

**Operand (author-reproduced).** Inventory file `nativeSubjectId=file:src/a.ts` and file `src/b.ts`. Payload `resolvedTarget=file:src/a.ts` so ephemeral first-party identity is `file:src/a.ts`. Sidecar first-party `evaluationNativeId=src/b.ts` uniquely joins the other row. Predecessor `_join_sidecar` checked kind/exists, not identity agreement; `_reconcile_attribution` then overwrote ephemeral `nativeId`.

**Guard.** In `_join_sidecar`, if both occupancies are first-party and `(kind, nativeId/evaluationNativeId, packageManifestPath or "")` disagree, refuse `TARGET_ATTRIBUTION_EPHEMERAL_IDENTITY_CONFLICT`. Independent exact-id identity is not rewritten. Agreement admits. Unknown sidecar keeps ephemeral (`exists` on `file:src/a.ts` remains `true`). Ordinary non-exact-id file first-party (`payload file:src/a.ts`, inventory `src/a.ts`, sidecar `evaluationNativeId=src/a.ts`) still admits. Missing inventory identity still `TARGET_ATTRIBUTION_FIRST_PARTY_NOT_IN_INVENTORY`. External vs ephemeral first-party remains `TARGET_ATTRIBUTION_EXTERNAL_CONTRADICTS_FIRST_PARTY` (pre-existing).

Return-channel admit reproduces the same atom join.

**Signatures (query-fix compatibility, other author copy not read).**

- `_reconcile_attribution(fact, spec, inputs) -> dict` unchanged.
- `_join_sidecar(fact, spec, sidecar, closures, inputs) -> None` unchanged.
- `_admit_provider_occupancy_conflicts(items, facts) -> None` unchanged.

C15 is a new refusal inside `_join_sidecar`. Query projection python still reads **raw** sidecar occupancy and does not call `_reconcile_attribution` (prose-only update this round). That is separately pending; signature compatibility is preserved. Do not treat query-contract prose as query integration.

**Probes.** `P-C15-UNIQUE-JOIN`, `P-C15-UNKNOWN-EPH`, `P-RECONCILE-SIGNATURE`, `P-QUERY-RAW-SIDECAR`.

This scoped C15 law is acceptable **as atom/return-admit behavior**. It does not make the return channel executable.

---

## 6. Public EVALUATION.INPUT_REFUSED / host invariant — holds on owner registry

Traced against `evaluator-fault-observation.schema.v3.json` `x-opensip-routes` (predecessor already had these pairs; this round did not invent them):

| Condition:origin | Public |
|---|---|
| `input-schema-invalid:provider-return` | operational-failed `PROVIDER.PROTOCOL_VIOLATION` `faultCause=provider-protocol` detail **`EVALUATION.INPUT_REFUSED`** |
| `input-join-invalid:provider-return` | same |
| `input-schema-invalid:host-internal` / `input-join-invalid:host-internal` | operational-failed `SYSTEM.OUTCOME.ILLEGAL_STATE` `faultCause=host-invariant` detail **`HOST.INVARIANT_VIOLATED`** |

`x-opensip-native-origin-map`: `provider-return` → `producer-boundary`. Both public details are existing `DomainDetailCode` members. Internal `TARGET_ATTRIBUTION_*` / `PROVIDER_RETURN_*` keys are not in that enum and are not D9/EVALUATION.TARGET aliases. `ROUTE_LAW.liveD9 = "not discharged"`. Missing envelope is lawful omission, not `required-output-pointer-omitted`.

No new D9 codes. No qualification claim. LIVE D9 successor-artifact remains future.

**Probe.** `P-PUBLIC-ROUTE-OWNER`. Helper `check-evaluator-faults.v3.py` count 40, standing bounded, no LIVE D9.

---

## 7. What else holds (not whole-design)

- Envelope is not an identity digest domain; captured records remain `byDomain.target-attribution` → `foundation/target-attribution.schema.v2.json`. Envelope `x-opensip-identity.digest` is null.
- Frozen24 still owns TargetAttributionV1 (`opensip.product.target-attribution.1`, 13480 bytes).
- Predecessor gap (“provider emits typed companions” with no invocation) is **named**. Naming is not execution.
- Protocol3 frames were not silently extended. That is correct **as a non-goal**; it does not substitute for table availability.
- `fullRun: false` on the new checker is honest labeling.

---

## 8. MUST / SHOULD / advisory

### MUST

1. **Executable wrapper path.** Selector: native-evidence §9.6; return schema `x-opensip-return-law.boundary`; `admit_provider_attribution_return`. Operand: one-shot child + closed `FactBatch` + host fact2 mint + `sourceFactId=fact2`. Remedy: §2 above. Do not add an unspecified transport.
2. **Stage/producer/plan join against actual execution-plan.** Selector: `admit_provider_attribution_return` stage/producer checks; execution-inputs §3 `stageReceipts`. Operand: matching stage 99 admits; non-selected enumerator admits. Remedy: §3.
3. **Selected-view join at return admit or a named subsequent owning admit that is actually invoked before `attach_host_capture`.** Selector: V2 `x-opensip-join-law.joins`; `execution_inputs_model` selected-view loop. Remedy: pass views or call the later join from the capture path.
4. **Schema-nest selected V2.** Selector: `provider-target-attribution-return.schema.v2.json` `properties.records.items`. Operand: `additionalProperties: true`, no `$ref`. Remedy: `$ref` selected V2.
5. **No capture of host-invented mapping.** Selector: `admit_provider_attribution_return` `origin`. Operand: `origin=host-internal` returns `hostDerivedRefs`. Remedy: refuse; route as host-invariant.

### SHOULD

1. Invoke `admit_provider_attribution_return` from the host-capture path (`attach_host_capture` / execution-inputs builder) so step 5 is code, not only prose.
2. Register the new schema/checker into the current evaluator suite and source-pins **after** MUST 1–5. Author already listed pins as remaining. Do not seal in this review.
3. Include the new envelope in the next array-order check (author remaining work).

### Advisory

1. Query-projection python still uses raw sidecar occupancy; contract prose now names V2 return. Separately pending. Shared atom signatures remain callable.
2. Author 18/18 and 69/69 are helper preconditions. Do not cite them as full owning admission.
3. Control-flow@syntactic / reachability@from-resolved-calls in native-evidence §9.6 match registry `targetNativeIdField` (`to` / `reachable`) and are not the omitted syntactic import/reference/call rungs. Keep that distinction if rewriting producer-supply tables.

---

## 9. Limitations of this peer

- Read-only: successor `target-provider-return-successor.v1`, predecessor `target-identity-successor.v1`, task inputs (15 files, manifest, patch, author report), frozen24 owning artifacts as needed.
- Did not read unrelated review histories, consumer helpers, other active author copies, private logs, web, or subagents.
- Did not re-run `check-execution-inputs.v1.py`, `check-semantic-replay.v3.py`, or `check-query-projection.v3.py`.
- Did not execute a native worker or `close_run`.
- Independent probes are design-reference synthetic maps, same class as the author’s helper checker, used to **falsify** caller-echo / isolation / nesting claims the helper suite does not test.

---

## 10. Verdict

**`CORRECTIONS_REQUIRED`.**

C15 identity-conflict, public EVALUATION.INPUT_REFUSED / HOST.INVARIANT_VIOLATED routing, missing-vs-empty, unknown-fact atomic refuse, and “envelope is not a digest domain / not a protocol3 frame” hold on the helper boundary. The advertised return channel is still not an executable wrapper-to-host path under original worker isolation, and stage/producer/view joins are not against the actual execution-plan.

No source-pin seal. No suite bypass. No global passing claim. No whole-design approval from 18 helper controls.
