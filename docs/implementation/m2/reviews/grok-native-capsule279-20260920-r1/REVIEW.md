# Independent review — native capsule and descriptor consistency 279

**Standing:** bounded native-Rust review of frozen `native-capsule-bindings-checkpoint-279`. Pure private owner for capsule/descriptor phase, role, head and publication consistency on the **same** guarded operation Budget. **Not** authentication, live head selection, complete lifecycle reachability, event effects, durable publication, physical capsule/reference admission, clock/accepted-role effects, current/historical population, private-policy merge, whole-state effects, native custody/census/writers, source selection, or M3–M6. **Not** applied inside 278's restore-proof reader. Archived 278 (`e15849d2…52fd`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5603648 B, 567 members, SHA256 `8b081b4f5eb8bd3335cc0b1c332484cde692d571b8fc73fc1c2a737aa8f34e9d`**. Pin, tar, member count, and every `subject.json` hash matched **before** extract; extract rehashed **567/567**. Product-inputs **413/413** live-equal.

Nested parent 278 pin `1be3f364…548c` (5940900 B / 729 / 412 files) equals the reviewed 278 freeze; live trial tar still matches; `trust-before.rs` equals that 278 `trust.rs`. Nested 265 `73c3b3f5…86df`. Nested 227 r9 (`trust-codecs-wip-227-r9`) `818604dd…6e44` (155008 B / 211). `Cargo.lock` unchanged vs 278. Inherited 278 fixtures byte-identical. `lib.rs` unchanged.

Product vs 278: **413** files, **411** unchanged, **1** changed (`trust.rs` `26dc458f…e67e` — private `capsule_consistency`), **1** added (`capsule279.ndjson`). No public API. No full workspace rerun (277 515+2 predecessor only).

---

## What 279 adds

Still private: `capsule_consistency` is not in `lib.rs` and is **not** called from `restore_proof` / `restore_event`.

**Capsule consistency** (`capsule_consistency(budget, capsule, descriptor, before)`): full current 125 `TrustCapsuleV1` and `PublicationDescriptorV1` shapes, plus an explicit full BEFORE-image shape precondition when supplied. Exact descriptor raw SHA/length pin, predecessor locator, store/revision identity, and `afterProjection` (capsule minus `publication`). P0/P1 (`phase != retained`) have no heads/history; P2 has both and exact root/catalog/revocation counters. Role RECOVERY iff ceremony; pre-acceptance has no accepted role; TRUSTED/REVOKED require accepted history; INDEX alone carries an accepted catalog; reset requires history; TRUSTED clears both condition slots; REVOKED has revocation evidence; ceremonies bind the live batch descriptor. P2 needs some accepted role history and three accepted metadata times. Explicit event head; last publication event agrees when events are nonempty.

**Empty-event publications** are permitted only in the original narrow structural case: exact BEFORE capsule, same store / revision+1 / previous hash, same event head, unchanged roles/staged/batch/sourceFence, retained phase on both sides, and unchanged time evidence, F/L/anchor/recovery serial/challenge. There is **no** blanket empty-event prohibition. Two valid empty-event fixture rows exist.

This is a **pure owned-value** owner: `budget.scope(|_| { ... })` with **no** `Budget.load` / I/O / invented object or edge charges. Tests prime prior retain+edge, assert counters stay `(1, 2, 5)` across a repeated successful check, and assert a failed check closes subsequent budget use. `CapsuleBound` owns capsule/descriptor/optional BEFORE after source values and Budget drop. Positive consistency fixtures are **not** necessarily reachable lifecycle states.

`no unbound recovery role` is present but logically implied by the earlier per-role live-ceremony batch check; the mutant driver makes **no** independent omit-control claim for it.

The first fixture generator used an invalid `ST-STALE` fallback. Before native tests it was corrected to actual `ST-STALE-REVOCATION`. The 628-row beforeimage is retained; production was not changed.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **221/221** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 30 compiled r1 controls + baseline | **31/31**; core fields/patches/source SHA-equal frozen `mutation-check-r1` |
| Exact live | Python source/fixture probes | **32/32** |
| Inspected | 649 rows / 116 positive | 504 phase×role×7 StateToken×accepted/ceremony; 43 `original-*`; 81 near-shape + 21 isolated joins |
| Inspected | 69 original 227 checks | r2 report `originalChecks.caseCount` **69**; 43 traced direct owner calls. Shape-only remainder is **reference coverage**. Not rerun here. |
| Inspected | 277 workspace 515+2 | predecessor only; not rerun |

Seven StateToken values in the 504-row matrix (72 each): `ST-UNBOOTSTRAPPED`, `ST-RECOVERY`, `ST-TRUSTED`, `ST-REVOKED`, `ST-EXPIRED`, `ST-STALE-REVOCATION`, `ST-QUORUM-LOST`. Current corpus has **no** invalid `ST-STALE` token.

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): omit descriptor-raw-pin, predecessor-pin, descriptor-identity, pre-acceptance-heads-absent, head-counter-identity, ceremony-iff-recovery, pre-acceptance-has-no-accepted-role, INDEX-only-accepted-catalog, never-established-has-no-reset, authorized-entry-clears-condition-slots, revoked-standing-has-evidence, retained-phase-has-accepted-role-history, retained-accepted-times-required, publication-final-event, empty-event-predecessor-binding, empty-event-publication-preserves-event-head, empty-event-publication-has-no-hidden-role-or-ceremony-effect, empty-event-publication-cannot-hide-a-clock-write, omit-before-shape.

First fail **other** assertions (not exploit proofs):

- `omit-exact-after-projection`: later `standing requires accepted history`.
- `omit-retained-heads-and-history-required`: panic `closed shape checked`.
- `omit-standing-requires-accepted-history`: later `revoked standing has evidence`.
- `omit-live-ceremony-batch-binding`: later `no unbound recovery role` (the redundant guard).
- `omit-new-capsule-has-explicit-event`: later `publication final event`.
- `omit-empty-event-head-update-stays-retained`: later empty-event clock/head reason.
- `force-all-publications-have-events`: over-refusal of the valid empty-D LIMITED path (`invented-no-empty-publication`).
- `drop-owned-before`: lost BEFORE fact.
- `omit-capsule-shape` / `omit-descriptor-shape`: later shape/reason panics.
- `omit-failure-latch`: follow-up not `BudgetError::Closed`.

Frozen `mutation-check-r1` was not overwritten. r1 baseline `sourceSha256` is current `trust.rs` `26dc458f…e67e`. No r2 round; no escaped controls.

---

## Focused findings

### Empty-D LIMITED path is not blanket-refused

When `descriptor.events` is empty, the owner requires an exact BEFORE image and the original narrow structural equalities (store/revision+1/previous, head, roles/staged/batch/sourceFence, retained phase both sides, T/F/L/anchor/epoch/challenge). Inventing a “all publications have events” guard over-refuses those rows. Actual metadata authentication and complete effects remain separate owners.

### Same Budget, no invented I/O

The owner latches `budget.scope` but does not load objects or charge edges. Tests prove prior counters `(1,2,5)` survive a second successful call. This is supplied typed-value consistency, not a capture producer, and is not wired into 278 restore composition.

### ST-STALE fixture repair

The 628-row beforeimage (`capsule-before-state-token-fix.ndjson`) used invalid `ST-STALE` (72 rows). Current 649-row corpus uses `ST-STALE-REVOCATION`. Production functions were not changed for that fixture repair.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | `capsule_consistency` not in `lib.rs` |
| Not in 278 proof | no call from `restore_proof` / `restore_event` |
| Pure scope | `budget.scope(\|_|` ; no `b.load` |
| Empty-D valid rows | 2 |
| Seven StateTokens | EXPIRED present; invalid ST-STALE absent |
| 649/116 | asserted in tests and counted in fixtures |
| 69 original / 43 traced | r2 report |
| No omit-no-unbound-recovery | absent from mutant driver and r1 report |
| Repeat counters | `(1,2,5)` twice |

---

## Remaining (do not count closed)

Physical capsule/reference admission; clock and accepted-role effects/base selection; current/historical populations/nonkeys/other roots/private-policy merge/artifacts/repair/S4/floors/whole-state effects; native custody/fence/slots/census/durability/writers; runtime/source selection; M3–M6; wiring this owner into 278 restore proof. Positive fixtures may not be reachable lifecycle states. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 413 product files: 411 unchanged vs 278. Nested 278/265/227 pins match live trial archives.
- [x] **221** security tests, Clippy, and fmt reproduced. Thirty compiled r1 controls behave as documented (nineteen wrong admissions; eleven other-first). No workspace rerun.
- [x] Pure same-Budget capsule/descriptor joins; empty-D LIMITED path kept; ST-STALE-REVOCATION fixture repair; not applied inside 278 proof.
- [ ] **Not** authentication, live publication, current authority, physical admission, or product installation.
