# Independent review — native successor link 329

**Standing:** bounded native-Rust review of frozen `native-successor-link-checkpoint-329`. Private unselected `SuccessorRecordBindings` joins **one** PublicationRef to a **caller-materialized logical before**: full before + full PublicationRef **before** descriptor I/O; exact `previousCapsule`; capture D at declared SHA/bytes; same store / revision+1 / prev; reconstruct after; **full 279** via `capsule_clock` (298 literal/calendar) with **actual** before; 265 operation; 241 outcome if present; **235** `bind_events` from **before** roles/head; ordinary `nativeBefore` = before revision/hash; restore-recovery **always** loads original **278** `restore_proof` and joins store/proven.image to logical before and observed revision/hash to D `nativeBefore`. Same Budget, failure latch, owned after drop. **Not** 327/325 partial owners, CurrentRecoveryImage, custody, census, durable publication, or 215 effects. Installed product remains `fa72e50`. 328 REVIEW was read and is **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. security-r1 compile-fail and security-r2 147-case logs are historical; **final is security-r3 / 148 / mutation-r1**.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **9689148 B, 1199 members, SHA256 `2d8b3de86b33fdf7eec1ce3a3b1dd497bff1015f3f87b3f7a259a4afa890ca89`**, `allMembersRehashed: true`, **479** product pins. Extract rehashed **1199/1199**. Parent 328 live tar SHA `b9b0928b…2ae5` (9691140 / 1216 / 477). Source 324 extract file count **639**. 328 REVIEW `97d04a58…f438` unchanged.

Product vs 328: **476** unchanged, **1** changed (`trust.rs` is 328 plus **only** `mod successor_record_bindings { include!(…); }` — reconstructed 328+include is byte-identical), **2** added (`successor_record_bindings.rs` SHA256 `c29e126f…1d2f` 14845 B; `successor-link329.ndjson` SHA256 `5da8e3b5…768c`). 328 `current_record_bindings.rs` remains `b329d797…e986`. 325 `current_event_trace.rs` remains `cd4da31a…28fa`. `lib.rs` **unchanged**, no public export of `SuccessorRecordBindings`.

The only native 329 source edit besides the new module is `JsonInteger::new(raw.len() as i128)` in `node` (r1 `From<usize>` compile-fail). `before-integer-conversion329.rs` still has `raw.len().into()`. No semantic predicate correction.

---

## Composition vs 327/325/278 (source)

`bind` does **not** call `capsule_projection` or `bind_trace`. Order:

1. Shape `TrustCapsuleV1` (before) and `PublicationRef` (no I/O).
2. `node(before)` digest; `reference.previousCapsule` must equal it (`reference predecessor`).
3. `Budget.load` Publications at declared SHA/bytes; admit current 127 D.
4. `successor identity`: same store, `revision == before.revision+1`, previous hash.
5. Reconstruct C from `afterProjection` + full reference.
6. `capsule_clock(..., Some(before))` — full 279 empty-event/before guards + 298 eleven-field record admit, six-field calendar projection. **Not** 327 local C/D-only.
7. `inputs::descriptor` — same-store may stop at OperationInput; continuity keeps existing intent/absence/before joins.
8. Outcome iff `commandOutcome` present (`bind_descriptor_raw`).
9. `bind_events(..., before.roles, before.eventHead)` — 235 known-before, **not** 325 touched-only, **not** AFTER roles/head.
10. Restore-recovery: `restore_proof` (278 nested originals + DIRECT terminal) then `restore logical predecessor` / `restore native predecessor`. Else `direct native predecessor`.

Python `successor_link_reference329.py` matches: `H.admit_shapes_and_joins` (full 279) with isolated `H.shape = O.I.shape` (125-profile, optional `commandOutcome`); `O.B.bind_events`; `op.proof`. 327 `admit_local_projection` is unused here.

**Before is not captured** by this helper: `empty-link-0` counters **(2, 2, 4899)** / two reads (publication + operation). Reconstructed after is derived, not a second physical object. Store callback collection/hash is not predecessor-path custody.

---

## Stated boundaries, independently tested

**Outer link is full 279/235; nested 278 is not.** `empty-hidden-timeEvidence` / `empty-hidden-evalHighWater` refuse `empty-event publication cannot hide a clock write`; `empty-hidden-roles` / `batch` / `staged` refuse hidden role/ceremony. Mutant `invent-after-as-before` **wrong-refuses** `empty-link-0` with `empty-event predecessor binding`. Mutant `events-from-after` **wrong-refuses** `clock-link-0` with 235 `event-chain`. Nested 278 still does **not** run 279/calendar/215 on every inner capsule.

**Empty outer restore is structural, not a reachable restore action.** `empty-restored-structural-link` is a **positive** (8 reads, (8, 9, 23542)) vs ordinary empty-link’s 2 reads — 278 nested originals + DIRECT terminal actually load. That success is **not** durable restore standing, creation/restore event law, or 215 effects. `skip-original-restore-proof` first-fails those counters (2, 2, 4888) vs (8, 9, 23542): bind can still return `Ok` without the proof. `empty-restore-native` / `parent` / `missing-original` / `non-direct-terminal` refuse with `restore native predecessor`, `restore logical predecessor`, `operation-capture-cap`, `witness-is-recovery-operation` (×3 graphs = 12). Mutants `ignore-restore-parent` / `ignore-restore-native` false-accept the first two.

**Adjacency is not projection equality.** `nonempty-nonadjacent-revision` sets D **and** `afterProjection.revision` to 13 against before 10; first error is `successor identity` after **1** publication read. Mutant `ignore-descriptor-identity` false-accepts it.

**Old T not followed.** Six T-bearing absent/malformed pairs remain positives with the same reads as their adjacency links; `ignoredTimeTargets` ∩ reads = **∅** on all 148.

**Optional outcome is actually joined.** `event-prepared-outcome` accepts (4 reads, (4, 5, 7053)). `outcome-missing` → `operation-capture-cap`; `outcome-malformed` → `operation-reference-bytes`; `outcome-different-operation` → `outcome-invocation-binding` (well-formed different `stepId`, not a missing `input.ref`). `skip-present-outcome` first-fails prepared-outcome counters.

**Historical 274 labels are new compositions:** P2 untouched roles/clock/heads/history, touched before/after from 274, real before hash, revision 11, generous limits. They do **not** preserve original 274 verdicts/budgets. 75 `event-*` rows.

Corpus families: **8** 326 adjacent links, **3** restored structural outers, **12** restore negatives, **6** T pairs, **75** event-274, plus identity/ref/calendar/hidden/missing/outcome/budget rows = **148 / 61 / 58**.

---

## Primary oracle and live cargo

Independent replay of frozen ndjson through extract-local `successor_link_reference329.py` with `budget.guard`: **148/148**, **0** mismatches. Verdicts, errors, counters, and physical reads compared.

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **262 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; 12.60s |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **18** includes | exit 0 |

security-r1: `JsonInteger: From<usize>` compile-fail — **not** a test result and **not** a mutation kill. r2 147 is historical.

---

## Mutants

Twelve compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1 not overwritten). Live `report.json` SHA256 **`017f3ef5…7070`**, **byte-identical** to frozen r1. All **13** compiled.

| Control | First failure |
|---|---|
| `drop-full-reference-shape` | counters `bad-ref-bytes-0` (0,1,0) vs (0,0,0) — shape-before-I/O |
| `ignore-reference-predecessor` | counters `wrong-descriptor-previousCapsule` (1,1,4663) vs (0,0,0) |
| `ignore-descriptor-identity` | false-accept `nonempty-nonadjacent-revision` |
| `invent-after-as-before` | wrong-refusal `empty-link-0` empty-event predecessor binding |
| `ignore-direct-native` | false-accept `wrong-descriptor-nativeBefore` |
| `ignore-restore-parent` | false-accept `empty-restore-parent` |
| `ignore-restore-native` | false-accept `empty-restore-native` |
| `skip-original-restore-proof` | counters `empty-restored-structural-link` (2,2,4888) vs (8,9,23542) |
| `skip-present-outcome` | counters `event-prepared-outcome` (3,3,6169) vs (4,5,7053) |
| `events-from-after` | wrong-refusal `clock-link-0` `event-chain` |
| `new-budget-per-link` | counters `empty-link-0` (0,0,0) vs (2,2,4899) |
| `drop-link-failure-latch` | counters `empty-restore-native` round1 (8,18,23542) vs (8,9,23542) |
| baseline | 262 passed / 2 ignored |

---

## Findings

The outer successor is a known-before 279/298/235/265/241 composition plus mandatory 278 on restore-recovery. 327/325 are not substituted. Nested 278 remains structural (DIRECT terminal + nested originals), not full historical replay of inner capsules. Empty restore positives must not be read as reachable restore authorization. Before bytes are not accounted here; reconstructed after is not a physical object; the store callback is not directory custody.

**Actionable defects in this freeze:** none that make `bind` self-contradictory with those pinned owners on the 148 structural cases.

Not claimed: live census/enumerator, native current, custody/fence, 215 effects, creation/restore action completeness, original TCB/time, or product installation.

---

## Remaining (do not count closed)

Physical enumerator / complete-bucket census / 64-canonical cap / foreign names; native custody/fence; recursive full historical 279 on nested restore capsules; 215 authenticated effects; creation/restore event law; original TCB/head/history/time; writers/final-age/source-selection; M2–M6.

---

## Verdicts

- [x] **329 as frozen known-before successor link:** archive verified; 328 report preserved; full 279/235 on the outer link; 327/325 not used as full before; 278 structural restore actually loaded and joined; empty restore not promoted to action standing; 148/61/58 reference; 0 T reads; live 262/2 ignored; Clippy/fmt18; 12 compiled controls + baseline frozen-r1-equal.
- [ ] **Not** CurrentRecoveryImage, durable restore, nested full-historical 279, live census/custody, or product installation.
