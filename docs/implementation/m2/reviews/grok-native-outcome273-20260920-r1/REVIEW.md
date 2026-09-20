# Independent review — native prepared-outcome bindings 273

**Standing:** bounded native-Rust review of frozen `native-outcome-bindings-checkpoint-273`. Prepared-data bindings of asserted COMPLETED/FAILED outcomes after 272 full graph. **Not** effect proof, durable publication, original-scope lookup, replay permission, current trust authority, complete input/event/clock/publication/restore joins, historical/current population, non-key subjects, other-root contexts, private-policy adoption/merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, native custody/fence/census/durability/writers, source selection, or M3–M6. Archived 272 (`47170863…9251`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**. No compiler-failure controls.

---

## Verification

Frozen archive: **5237192 B, 553 members, SHA256 `b665c977d4c8b2919ddb3d0c8a3807a249eea82a613e36b37e5295a7969d2cfe`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed **553/553**. Product-inputs **405/405** live-equal.

Nested parent 272 pin `f2010bcc…f5c3` (5188496 B / 513 / 400 files) equals the reviewed 272 freeze; live trial tar still matches; `trust-before.rs` equals that 272 `trust.rs`. Nested 265 `73c3b3f5…86df`. Nested original 241 `393a4999…b447` (30244 B / 26, live `installation-trust-outcome-wip-241-r1`). Nested historical 239 r2 `822e3a9f…48c3` (7058132 B / 1486, live `trust-operation-integration-reference-wip-239-r2`). Schema `1328ba16…4208`. 265 command/action table is eight commands / ten actions. `Cargo.lock` unchanged vs 272.

Product vs 272: **405** files, **399** unchanged, **1** changed (`trust.rs` `b649811c…142c` — `mod trust_outcomes` plus private `prepared_trust_outcomes`), **5** added (`trust_outcomes.rs` `5574f45e…d2bb`; `trust_outcome_tests.rs`; `outcome273-{pure,joins,graph}.ndjson`). Inherited 272 fixtures unchanged. No public API. final-r6 is the authoritative snapshot.

---

## What 273 adds

Private `trust_outcomes` admits through the 270 product-canonical 125-definition owner (4MiB / 32 containers / product integer domain). `decode`/`shape` run **before** field access (`unreachable!("closed shape admitted")`). Installation scope is closed `(schemaVersion, kind, requestId, stepId, operation, store)`; extra `executionId`/`projectId`/`path` fail shape. `bind_params` joins only `kind`/`mutationClass`/`idempotencyKey`. Full StepSpec remains elsewhere.

Identity uses existing `hash_canonical_value` (product H frame `opensip.product.v1\0` + domain + length + canonical). Intent domain `workflow.mutation-intent`. Receipt identity domain `workflow.mutation-receipt` over the **eleven-field** `TrustMutationReceiptV1` **except** `receiptId`, then `receipt2:` + hex. Original receipts require `replayed=false`, `commitClass=IRREVERSIBLE`, `effectOutcome` COMPLETED or FAILED (schema consts/enums).

`bind_outcome` joins actual operation bytes (sha+length), command/action table, store, scope request/step, receipt request/step/Exec, receipt operation/intent key, whole receipt identity. `bind_descriptor` additionally joins outcome bytes, operation, store, and projection store/revision/previous. `Bound` owns operation, outcome, and optional descriptor. `prepare` is an inert asserted-outcome constructor and re-admits through `bind_outcome`.

`prepared_trust_outcomes::walk` runs **272 full graph first** on the same `Budget`, then in visit order: each descriptor **with** `commandOutcome` reloads outcome+operation; each outcome visit reloads operation. Physical cache shares bytes; every `load` still charges. Descriptors without optional outcome stay structurally walkable. Direct typed-input wrappers use the same budget. Failures latch `budget.scope`. Evidence remains after dropping budget and clearing store.

Synthetic creation-event + clock-challenge graphs test this structural/prepared owner only. Event action/effect semantics are **not** established.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **212/212** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 18 compiled controls + baseline | **19/19**; core fields/patches/source SHA-equal frozen `mutation-check-r1` |
| Exact live | Python source/fixture probes | **38/38** |
| Inspected | 289 pure / 107 positive / 7 functions | full command/action Cartesian × COMPLETED/FAILED (20 prepare positives: 10+10); unknown/bootstrap aliases, noncanonical, shapes, partial params, domain separation |
| Inspected | 23 coherent negative joins / 0 positive | independent rehashed scope/receipt identities for each join |
| Inspected | 38 graph/input cases / 13 positive | owned facts after store/budget drop; exact/one-short object/edge/byte; repeats; graph-first missing dep; descriptor without outcome stays structural |
| Inspected | original 241 84 checks | claimed reproduced inside the 289; not independently counted as a separate 84-row subset |
| Inspected | 272 workspace 506+2 | predecessor only; not rerun here |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): omit OperationBytes, CommandAction, Store, ScopeInvocation, ReceiptInvocation, ReceiptScope, ReceiptIdentity, DescriptorOutcome, DescriptorOperation, DescriptorStore, Projection.

First fail **other** assertions (not exploit proofs):

- `wrong-intent-domain` / `wrong-receipt-domain`: installation_key / receipt_identity digest mismatch, then valid `outcome-walk` over-refused.
- `receipt-hash-includes-receipt-id`: valid `outcome-walk` / `prepare_outcome` over-refused (`ReceiptIdentity`).
- `omit-descriptor-binding`: binding count **1 vs 2**.
- `omit-outcome-binding`: binding count **0 vs 1**.
- `reset-shared-budget`: counters **(0,0,0) vs (2,3,1197)**.
- `omit-binding-failure-latch`: follow-up walk is not `BudgetError::Closed`.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | `trust_outcomes` / `prepared_trust_outcomes` not exported from `lib.rs` |
| Schema before fields | `admit`/`shape` then `object()`; extra scope fields fail |
| Domain split | intent vs receipt domains differ; including `receiptId` over-refuses valid |
| Command table | exact 265 eight-command / ten-action map |
| Optional descriptor outcome | walk skips binding when `commandOutcome` absent; still visits structure |
| Graph then bind | `graph::walk` precedes descriptor/outcome reloads; each reload `load`s again |
| Ownership | graph test clears store, drops budget, then re-encodes held `Bound` values |
| No skip list | walk takes budget, kind, reference, store only |

---

## Remaining (do not count closed)

Complete input/event/clock/publication/restore joins; current/historical population and non-key subjects; other-root contexts; private-policy adoption/merge; artifact/repair/S4/floors; command/role/batch/whole-image effects; native custody/fence/slots/census/durability/writers; source selection; M3–M6. Asserted COMPLETED/FAILED is not an effect or publication proof. 273 is not installed runtime source. No native project/workflow implementation.

---

## Verdict

- [x] Archive/pins/members verified. 405 product files: 399 unchanged vs 272. Nested 272/265/241/239 pins match live trial archives.
- [x] **212** security tests, Clippy, and fmt reproduced. Eighteen compiled controls behave as documented (eleven wrong admissions; seven other-first, including receiptId over-refusal of valid).
- [x] Product H domains, closed installation scope, schema-before-access, coherent negative joins, same-budget 272 graph then charged reloads, failure latch, owned Bound after drop.
- [ ] **Not** effects, publication, replay grant, current authority, native custody, or product installation.
