# Independent review — native current-record bindings 328

**Standing:** bounded native-Rust review of frozen `native-current-bindings-checkpoint-328`. Private unselected `CurrentRecordBindings` over **already-materialized C/D**: 327 `capsule_projection`, literal `StoreBinding`, retained-phase gate, existing eleven-field `clock::admit`, existing typed `descriptor` operation, **241/265 outcome bind iff `commandOutcome` is present**, then 325 `bind_trace`. Same `Budget` for retained dependency reads and failure latch. Not native capture, CurrentRecoveryImage, custody, complete census, original-T validity, or 215 effects. Installed product remains `fa72e50`. 327 REVIEW+ADDENDUM were read and are **unchanged**.

Python 3.12.13 `-I -B`. Rust 1.95.0 `--offline --locked`. Review-local copies. Frozen fixture/mutant directories were not overwritten. r1 248-case logs are historical; **final is r2 / 249**.

---

## Verification

Pins, tar bytes, member counts, and every `subject.json` hash matched **before** extract.

Frozen archive: **9691140 B, 1216 members, SHA256 `b9b0928b13faab7a17c6140a140c3535db87dab0fb8098824a87859ca26a2ae5`**, `allMembersRehashed: true`, **477** product pins. Extract rehashed **1216/1216**. Parent 327 live tar SHA `cc6aa473…51a8` (9623572 / 1182 / 475). Source 324 extract file count **639**. Packet `event_trace_reference325.py` / `capsule_projection_reference327.py` match the 327 freeze. 327 REVIEW `116f7c3d…13bd` and ADDENDUM `ae8ad7b6…951c` unchanged.

Product vs 327: **474** unchanged, **1** changed (`trust.rs` is 327 plus **only** `mod current_record_bindings { include!("trust/current_record_bindings.rs"); }` — reconstructed 327+include is byte-identical), **2** added (`current_record_bindings.rs` SHA256 `b329d797…e986` 11218 B; `current-bindings328.ndjson` SHA256 `95c8b891…945b`). `current_event_trace.rs` remains `cd4da31a…28fa`. `lib.rs` **unchanged**, no public export.

Kernel `security_lifecycle_model_v1.py` SHA256 **`df45c9c5444790b5f89b458efbee5cb068781d5fc1e82483c2678d2f10712299`**.

---

## Composition (source, not just tests)

`bind` is one `budget.scope`:

1. Canonical-admit caller `expectedStore` as `StoreBinding` (literal, **0** captures).
2. `capsule_projection` (327) — C/D clones, no I/O.
3. `c.store == expectedStore`.
4. `clock.phase == "retained"` else `Error::Phase`.
5. `clock::admit(record)` — closed **11** `RECORD_FIELDS`, calendar on the five timestamps, recovery counters/serial/challenge. Not S4 / original-T replay.
6. `inputs::descriptor` — same-store **stops at** `OperationInput`; cross-store continuity keeps intent/absence/source/target-before joins (`link-operation-store` if action is not continuity).
7. If `commandOutcome` **in** D: `bind_descriptor_raw` (outcome+operation+receipt/scope). Absent: `None`. Present missing/malformed bytes refuse.
8. `bind_trace` (325) — listed-event local claims, `partial-local-trace-only`.

Owned after Budget drop: projection C/D, admitted clock fields, operation, optional outcome, trace captures. Caller C/D are **not** charged as retained objects (`empty-retained-with-unknown-before` counters **(1, 1, 421)** / **1** read = operation only).

Empty current D does **not** invent a before or call full 279: `empty-retained-with-unknown-before` is a **positive** with `events: []`. Mutant `invent-full-before-requirement` (insert `capsule_consistency(..., None)`) **wrong-refuses** `event-original-27` with `empty-event publication needs exact before image`.

Old T locator `55…55` is on that retained capsule. `old-T-absent` and `old-T-malformed-present` remain positives with the **same** 1 operation read; **0** T hashes in any of the 249 expected read traces.

---

## Schema attachment vs 327 oracle limit

327 Python local prefix is original **227** eight-member D (64 `$defs`, no `commandOutcome`). Native shape is **127** `Definition`s with 241 optional `commandOutcome`. 327 ADDENDUM already recorded that as a 327 **oracle-coverage limitation**. 328 does **not** edit those 327 files.

Isolated `current_bindings_reference328.py` sets `P.shape = O.I.shape` (unchanged 265/241 `InputWork.shape`, **125** `$defs`, `commandOutcome` present). `before-schema-attachment328.py` has no such assignment. Predicate/kernel/schema bytes otherwise unchanged.

This reference can shape a current D with optional outcome. **649 327 cases still do not cover optional outcomes.** 328’s own corpus does:

| Case | First error / result |
|---|---|
| `event-prepared-outcome` | **accept**, 3 reads, counters (3, 4, 1986) |
| `required-outcome-absent` | `operation-capture-cap` |
| `required-outcome-malformed-present` | `operation-reference-bytes` |
| `event-prepared-wrong-receipt-before-event` | `receipt-identity` |

`skip-present-outcome` first-fails `event-prepared-outcome` **counters** `(2, 2, 1102)` vs `(3, 4, 1986)` — bind still returns `Ok` with `outcome=None`, so the kill is missing capture/ownership, not a negative false-accept. Present-outcome join is actually charged.

---

## Historical labels are new compositions

`prepare_current_bindings328.py` copies 274 event descriptors and 276 `descriptor_operation` rows, then **`promote()`** overlays P2 clock/heads/history/roles from a 279 retained empty-event before and **rebuilds** C. Default limits are **(65536, 131072, 268435456)**. Labels such as `event-prepared-one-short-objects` can be **true** here; they are **not** original 274 budgets or verdicts. Actual short-byte refusals in this freeze are `empty-retained-with-unknown-before-short-bytes` and `event-prepared-outcome-short-bytes` (`operation-byte-budget`).

276 `continuity-original-21` (sequence 4 after previous 1) remains **negative** (`event-chain`) after 325 trace. New `continuity-ancestor-current-trace` repins `previous+1` / event / D / C and is **positive** (5 reads, (5, 6, 4960)). No helper predicate change. r1 **248 / 43 / 41** is historical; final counts **249 / 44 / 42**.

These remain structural joins, not reachable lifecycle grants. Overlayed 274/276 rows include many `operation-capture-cap` negatives (125) that prove missing required non-time still latch, not original-274 admission.

---

## Primary oracle and live cargo

Independent replay of frozen ndjson through extract-local `current_bindings_reference328.py` with `budget.guard`: **249/249**, **0** mismatches, **44** first / **42** second positives. Verdicts, counters, and physical reads compared.

**Executed** review-local product, `cargo clean -p opensip-security` then:

| Kind | Result |
|---|---|
| `cargo test --offline --locked -p opensip-security` | **261 passed / 0 failed / 2 ignored**; `Compiling opensip-security`; 12.67s |
| Workspace Clippy `--all-targets -D warnings` | exit 0 |
| `cargo fmt --all --check` | exit 0 |
| `rustfmt --check` of **17** includes | exit 0 |

---

## Mutants

Eight compiled controls plus baseline replayed into `grok-out/io/mutation-check-live` (frozen r1/r2 not overwritten). Live `report.json` SHA256 **`4981ee7d…b7b9`**, **byte-identical** to frozen r2. All **9** compiled; no compile-fail counted as a kill.

| Control | First failure |
|---|---|
| `ignore-selected-store` | false-accept `wrong-selected-store` |
| `drop-retained-phase-check` | **panic** `no entry found for key` (`record` on P0) — not a false-accept |
| `normalize-invalid-calendar` | false-accept `invalid-calendar-evalHighWater` |
| `skip-present-outcome` | counters `event-prepared-outcome` (2,2,1102) vs (3,4,1986) |
| `invent-full-before-requirement` | wrong-refusal `event-original-27` empty-event exact-before |
| `erase-listed-events` | false-accept `event-original-0` |
| `new-budget-per-bind` | counters `event-original-0` (0,0,0) vs (2,2,716) |
| `drop-binding-failure-latch` | panic `event-original-0` failure latch |
| baseline | 261 passed / 2 ignored |

---

## Findings

The composition is faithful to the disclosed 327 local C/D owner, 325 local trace, 265 same-store/continuity operation, and 241 optional outcome **when present**. Empty current D is not smuggled through full 279. Old T is declared and not loaded. Optional-outcome present/absent/malformed/wrong-receipt are in **this** corpus, not 327’s 649. Prepared outcome is not durable completion; `LocalTrace` claims are not 215 effects. Expected store is a caller literal.

**Actionable defects in this freeze:** none that make `bind` self-contradictory with those pinned owners on the 249 structural cases.

Not claimed: live current-file identity, custody/capture accounting for C/D bytes, full action/creation-marker/restore semantics, original TCB/time, child census, or product installation.

---

## Remaining (do not count closed)

Native custody / current-file comparison and capture accounting; live child census/capacity/fence; scoped head/history authentication; original TCB/full time; creation/full action; nested carrying-T restore; writers/final-age/source-selection; M2–M6.

---

## Verdicts

- [x] **328 as frozen private current-record composition:** archive verified; 327 REVIEW+ADDENDUM preserved; schema attachment is isolated 125-profile `P.shape` only; 249/44/42 reference; native outcomes actually tested; empty D has no invented before; 0 T reads; live 261/2 ignored; Clippy/fmt17; 8 compiled controls + baseline frozen-r2-equal; phase-guard drop panics, not false-accepts.
- [ ] **Not** CurrentRecoveryImage, 327 optional-outcome coverage, original-T validity, live current/census, or product installation.
