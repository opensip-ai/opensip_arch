# Independent review — native publication event replay 274

**Standing:** bounded native-Rust review of frozen `native-event-bindings-checkpoint-274`. Literal event replay from a **supplied** logical before roles/head, after optional 273 prepared-outcome binding on the same Budget. **Not** logical-base selection/authentication, publication durability, accepted-role authorization, complete input/clock/whole-publication/restore proof, historical/current population, non-key subjects, other-root contexts, private-policy adoption/merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, native custody/fence/census/durability/writers, source selection, or M3–M6. Archived 273 (`c1d76b37…42b7`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5247056 B, 657 members, SHA256 `bd2d232e72811585d526e3f51d854b5e463e460187a1dbae2a20c64918597fe9`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed **657/657**. Product-inputs **406/406** live-equal.

Nested parent 273 pin `b665c977…2cfe` (5237192 B / 553 / 405 files) equals the reviewed 273 freeze; live trial tar still matches; `trust-before.rs` equals that 273 `trust.rs`. Nested 265 `73c3b3f5…86df`. Nested original 235 `112dc6a0…5468` (25584 B / 26, live `publication-events-wip-235-r1`). Nested 230 helper `99288ae0…3c00` (66388 B / 38, live `trust-inputs-wip-230-r3`). Schema `1328ba16…4208`. `Cargo.lock` unchanged vs 273.

Product vs 273: **406** files, **404** unchanged, **1** changed (`trust.rs` `49a95a1c…4183` — private `publication_events`), **1** added (`events274.ndjson`). Inherited 273 fixtures unchanged. No public API. Mutation **r4** is the complete 26-control set; r3 has no receipts (interrupted). final-r5 security / final-r6 Clippy are the live-matching snapshot.

---

## What 274 adds

Private `publication_events::bind(budget, descriptor, before_roles, before_head, store)` replays literal events. If `commandOutcome` is present, it **first** charges/retains canonical descriptor bytes (`edge(1)` + `retain(Publications)`) and invokes 273 `bind_descriptor_raw` (outcome/operation loads), **then** event replay. Same Budget, cached-edge charges, `budget.scope` latch. Retaining supplied descriptor bytes is not host capture proof.

EventRef (or NodeRef for BeginBatch) is **admitted before** `{sha256,bytes}` projection into `Budget.load`; locators (`store`/`sequence`) are checked separately after load. Six null-change kinds (`creation`, `clock-write`, `batch-termination`, `restore`, `continuity`, `abort-termination-annotation`); three role-change kinds (`role-event`, `standing-reset`, `private-ceremony-termination`) require non-null `roleChange` and literal event/change fields plus ordered role-before. Standing reset copies the whole record except exact `ST-UNBOOTSTRAPPED` and `reset.by` = this event reference. Termination loads actual `BeginBatch` on the **same** Budget, binds selected role/BEGIN, requires `revokedBy` if BEGIN was V, yields V or U and clears only `ceremony`. Refused role events require `after==before`. ABORT annotation looks up earlier SHA in **this** descriptor, then requires **full reference equality** (so same SHA with wrong sequence/bytes fails), then `role-event`/`EV-RECOVER-ABORT`/`accepted`, then exact role/from/to/batch. Final roles/head must equal projection. Accepted role events append `pendingAuthenticatedRoleEffects` objects; there is no boolean authorization conversion.

Events + BeginBatch are not a whole 272 graph. Returned roles/head/pending and optional prepared `Bound` remain after store clear and budget drop.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **213/213** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 26 compiled r4 controls + baseline | **27/27**; core fields/patches/source SHA-equal frozen `mutation-check-r4` |
| Exact live | Python source/fixture probes | **28/28** |
| Inspected | 75 Operation.events rows / 28 positive | all 9 kinds in positives; all 6 roles pending; repeats/exact/one-short; prepared receipt joins **before** event replay (`receipt-identity` with 2 captures); foreign logical head; revoked BEGIN without restriction; wrong BEGIN; annotation citing refused ABORT |
| Inspected | original-* rows | **40** (`original-0`…`original-39`); claimed 41 not independently matched as a 41-row subset |
| Inspected | r1 `omit-abort-same-descriptor` | **escaped** (`expectedOutcome` false) — absent earlier ABORT only |
| Inspected | r2 `omit-abort-accepted-role-event` | **escaped** (`expectedOutcome` false) — invalid clock profile |
| Inspected | r4 new fixtures | `annotation-existing-abort-wrong-sequence/bytes` → `abort-same-descriptor`; `schema-valid-refused-abort` / `annotation-cites-accepted-non-abort` → `abort-accepted-role-event` |
| Inspected | 272 workspace 506+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): omit descriptor-projection, event-locator, event-store-operation, event-chain, null-event-role-change, abort-same-descriptor, abort-annotation-binding, literal-role-event, ordered-role-before, reset-applicability, reset-exact-effect, termination-begin-binding, termination-active-restriction, termination-exact-effect, refused-no-role-change, all-roles-replayed, projection-event-head.

First fail **other** assertions (not exploit proofs):

- `omit-logical-head-store` / `omit-event-duplicate`: reason becomes `event-chain` first (`original-21` / `original-10`).
- `omit-abort-accepted-role-event`: `schema-valid-refused-abort` reason becomes `abort-annotation-binding`.
- `omit-role-event-change-required`: panics on `object(Null)` (`unreachable!("closed shape checked")`).
- `omit-termination-batch-binding`: `original-33` reason becomes `termination-begin-binding`.
- `omit-pending-authenticated-effects`: `original-3` pending list empty (fact loss).
- `omit-prepared-outcome-binding`: `prepared_outcome().is_some()` false vs descriptor `commandOutcome`.
- `reset-operation-budget`: `original-0` counters **(0,0,0) vs (1,1,314)**.
- `omit-failure-latch`: follow-up bind is not `BudgetError::Closed`.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | `publication_events` not exported from `lib.rs` |
| Nine kinds | all nine appear in **valid** store events |
| Six roles | closed before-set; pending fixture per role |
| EventRef before load | full EventRef/NodeRef admit, then physical `{sha256,bytes}` |
| ABORT equality | SHA lookup then `*prior_ref == e["abort"]`; wrong sequence/bytes caught as `abort-same-descriptor` |
| Pending ≠ authorized | `Vec` of `{event,role,before,after}`; no boolean |
| 273 before events | `bind_descriptor_raw` precedes the event loop; bad receipt fails before missing event |
| Same Budget | `scope` + BeginBatch `load`; cache still charges |
| No skip list | `bind` takes budget, descriptor, before roles/head, store only |

---

## Remaining (do not count closed)

Input/clock/whole-publication/restore proof; authenticated accepted-role guards/effects and logical-base selection; current/historical population and non-key subjects; other-root contexts; private-policy adoption/merge; artifact/repair/S4/floors; command/role/batch/whole-image effects; native custody/fence/slots/census/durability/writers; source selection; M3–M6. Structural replay is not current authority. 274 is not installed runtime source.

---

## Verdict

- [x] Archive/pins/members verified. 406 product files: 404 unchanged vs 273. Nested 273/265/235/230 pins match live trial archives.
- [x] **213** security tests, Clippy, and fmt reproduced. Twenty-six r4 controls behave as documented (seventeen wrong admissions; nine other-first). r1/r2 abort-control escapes are fixture gaps repaired in r4 without production change.
- [x] Supplied logical base; EventRef-before-load; full ABORT reference equality; pending authenticated effects not authorization; 273 prepared join on the same Budget before event replay; owned facts after drop.
- [ ] **Not** base selection, durability, accepted-role authorization, current authority, native custody, or product installation.
