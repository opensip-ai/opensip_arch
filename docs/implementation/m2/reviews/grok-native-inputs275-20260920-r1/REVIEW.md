# Independent review — native creation, declaration and admission inputs 275

**Standing:** bounded native-Rust review of frozen `native-input-bindings-checkpoint-275`. Three current 265 `trust_input_reference` conditional joins on the **same** guarded operation Budget. **Not** native creation, live census/selected history, current trust authority, S4 execution, accepted role effects, durable publication, absence/restore/restriction authorization, complete clock/publication/restore proof, historical/current population, non-key subjects, other-root contexts, private-policy merge, artifact/repair/S4/floors, command/role/batch/whole-image effects, native custody/fence/census/durability/writers, source selection, or M3–M6. Archived 274 (`3471ec3e…3e52`) was not edited. Installed product remains `fa72e50`.

Python 3.12.13 `-I -B`. OpenSSL 3.6.3. Rust 1.95.0 `--offline --locked`. Review-local product copy only. Frozen fixture/key/result directories were not overwritten. Keys are **TEST ONLY**.

---

## Verification

Frozen archive: **5270056 B, 569 members, SHA256 `a56e8640cb6b20d47cb92b8489e9eba60a91ec175a7d4757b9be21fe94a88804`**. Pin, tar, member count, and every `subject.json` hash matched before extract; extract rehashed **569/569**. Product-inputs **407/407** live-equal.

Nested parent 274 pin `bd2d232e…7fe9` (5247056 B / 657 / 406 files) equals the reviewed 274 freeze; live trial tar still matches; `trust-before.rs` equals that 274 `trust.rs`. Nested 265 `73c3b3f5…86df`. Nested 230 r3 helper `99288ae0…3c00` (66388 B / 38). Schema `1328ba16…4208`. `Cargo.lock` unchanged vs 274.

Product vs 274: **407** files, **405** unchanged, **1** changed (`trust.rs` `6e55ab1a…339b` — private `trust_input_bindings`), **1** added (`inputs275.ndjson`). Inherited 274 fixtures unchanged. No public API. No full workspace rerun (272 506+2 predecessor only).

---

## What 275 adds

Private closed `Input` enum routes eight owned types (creation, marker, capsule, declaration, admission, observation, restriction, clock-write) to records or events. Full `NodeRef`/`EventRef` is admitted **before** `{sha256,bytes}` projection. Every `Budget.load` charges; actual bytes are hash/length/canonical/full-shape checked, including reuse. All owner errors latch `budget.scope`. `Bound` owns operation, events, optional capsule, and loaded inputs in order; facts remain after store/budget drop.

**Creation** (`action=creation`): admits CreationEvent/TrustCapsule/OperationInput; joins actual-op reference, creation-input ref, marker **72 bytes** + full StoreMarker + matching storeInstanceId, equal stores, sequence 1 / null previous, eventHead = this event, P0 (`revision=1`, null previous, null publication previous, unevaluated clock, heads/staged/batch/history/sourceFence null), all role **values** blank `ST-UNBOOTSTRAPPED`. Does not prove exclusive skeleton creation or placement.

**Declaration** (`acknowledge-restore`, variant `declared`): loads RestoreDeclarationInput and before capsule; binds store/`nativeBefore`; refuses active `batch`; requires strict increasing orphan SHA (duplicates fail `<`) and each orphan `previousCapsule` = before-image SHA. No live census/cleanliness/proven-history claim.

**Host admission** (`host-trust-admission`): loads TrustAdmissionInput. Restrictive observation owns only `EV-REVOKE`/`EV-QUORUM-OBSERVE` with `observed-context`, exact invocation/store, purpose revocation/quorum, evidence role. Install/continue owns its event plus `EV-CLOCK`; surface CORE/INDEX/COMPONENT except CLOCK allowed on all six roles; loaded ClockWrite must be source `s4`, same operation/store, locator match, sequence **before** the role event. This checks recorded clock input, not S4 execution. Empty events still admit the input only. Quorum `contextRoot` placeholders are not traversed.

---

## Reproduction vs inspection

| Kind | Corpus | Result |
|---|---|---|
| Exact live | `cargo test -p opensip-security` | **214/214** |
| Exact live | workspace Clippy `--all-targets -D warnings` | **pass** |
| Exact live | `cargo fmt --all --check` | **pass** |
| Exact live | 29 compiled controls + baseline | **30/30**; core fields/patches/source SHA-equal frozen `mutation-check-r1` |
| Exact live | Python source/fixture probes | **25/25** |
| Inspected | 112 InputWork rows / 41 positive | 63 `original-N` (three-owner traces); 82 initial = those + repeats/exact/one-short/empty; +30 role-matrix (install/continue surface + CLOCK exception + quorum per role) |
| Inspected | original 230 helper 195 checks | author driver wraps only `join_creation`/`join_declaration`/`join_admission` (63 traced). Remaining 195 are **reference coverage**, not native behavioral assertions. Not rerun here. |
| Inspected | static-schema adapter | test-only 12 definition names from original 230 `trust-inputs-root.v1.json` after `x-author-draft` removal; current schema/functions unchanged. Original failing driver retained. |
| Inspected | 272 workspace 506+2 | predecessor only; not rerun |

**Controls (honest):**

Wrong admission (`left: true` / `right: false`): omit operation-ref, event-store, creation-input-ref, creation-store, creation-event-head, creation-p0, creation-p0-roles, restore-variant, declaration-store, declaration-native-before, declaration-begun-ceremony, orphan-order, orphan-bucket, admission-event-not-owned, admission-observation-binding/purpose/role, admission-role-not-install-surface, admission-clock-write, admission-clock-order.

First fail **other** assertions (not exploit proofs):

- `omit-operation-action` / `omit-marker-bytes`: extra captures (`original-23` 1 vs 0; `original-11` 2 vs 1).
- `omit-marker-store` / `omit-creation-first-event`: later reason `creation-event-head`.
- `omit-admission-clock-kind`: panic on missing clock field.
- `omit-retained-inputs` / `only-first-admission-event`: lost loaded-input facts (`original-0` / `original-37`).
- `reset-operation-budget`: `original-0` counters **(0,0,0) vs (2,2,557)**.
- `omit-failure-latch`: follow-up call is not `BudgetError::Closed`.

---

## Independent probes

| Probe | Result |
|---|---|
| Public API | `trust_input_bindings` not exported from `lib.rs` |
| Eight Input types | closed enum; EventRef vs NodeRef before physical load |
| Marker 72 | `storeMarker.bytes == 72` then StoreMarker load |
| P0 | revision 1, null previous/publication previous, unevaluated clock, five null capsule slots, blank role values |
| CLOCK exception | CLOCK valid on BUNDLE/PROFILE/REPAIR; those roles refused as install/continue surface |
| Empty events | `empty-admission-events-are-only-input-joins` valid, 1 capture |
| Quorum per role | six valid rows, 3 captures; no contextRoot walk |
| Same Budget | three `scope` owners; load charges; latch on failure |
| Ownership | tests drop store/budget then re-encode Bound fields |

`creation-p0-roles` checks every role **value** is blank, not that six named keys exist; TrustCapsule shape is relied on for key set.

---

## Remaining (do not count closed)

Intent/absence/continuity; full restriction/history/restore proof and clock/publication joins; authenticated effects/base choice; current/historical population and non-key subjects; other-root contexts; private-policy merge; artifact/repair/S4/floors; command/role/batch/whole-image effects; native custody/fence/slots/census/durability/writers; source selection; M3–M6. These are private review candidates, not shipped behavior.

---

## Verdict

- [x] Archive/pins/members verified. 407 product files: 405 unchanged vs 274. Nested 274/265/230 pins match live trial archives.
- [x] **214** security tests, Clippy, and fmt reproduced. Twenty-nine compiled controls behave as documented (twenty wrong admissions; nine other-first).
- [x] Shapes before access; EventRef/NodeRef before load; creation P0 + 72-byte marker; declaration no-batch/orphan bucket; admission surface + CLOCK exception + recorded s4 clock; same-budget latch; owned Bound after drop.
- [ ] **Not** native creation, S4 execution, census, restriction/restore authorization, current authority, or product installation.
