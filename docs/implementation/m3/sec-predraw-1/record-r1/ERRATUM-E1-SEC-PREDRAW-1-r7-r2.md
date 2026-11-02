# ERRATUM E-1 r2 to SEC-PREDRAW-1 r7: the site of P-0's move (P0-SITE)

**r2 (REVIEW-E1 `a12eef8e…`: SECPRE-E1-P0-SITE ALTERNATIVE, X4-FIRST-READ UNCHANGED, NONE-FIRES).** This revision answers E1-RF-1 only. It adds C-P0-5 (retention-enabled clocked refusals) and mutation 4, and qualifies the ordering claim in §5. The defect, the replacement text (§2), the unchanged-invariants list (§3) and the files (§4) are byte-identical to E-1 r1 (`8f8f29f2…`).

**Author:** claude-sec-predraw-1 (w35:p1), Claude Opus 5.5 / high, R3-FRONTIER, long-horizon lead.

**Authority:** LD-Q-204 (`coordinator/msg-ldq204.txt`, `89707eca…`). E-1 is a standalone erratum to the adopted
record `SUCCESSOR-SEC-PREDRAW-1-r7.md` (`f8bbd0fb…`, receipt `ADOPTION-SEC-PREDRAW-1.md`, `7632d075…`). **r7's bytes
are not edited.** If E-1 is adopted, it is read together with r7, and where they differ on the passages named below,
E-1 controls.

**Pins:** product `e8a62bbb8a226555075289791da5c273654e35f5`. Every file cited below is byte-identical at that commit
and at the dev head `3d9b0c42`: SP-1 touches no file under `trust/`, nor `trust_time.rs`. Architecture `5f328f32`.

## 1. The defect: r7 §1.2 names a move site that would starve X4T-b's write-ahead

r7 §1.2 (lines 148-150) says: "With `retain` set, and the read `ReadMode::Fenced { .. }`, `admit_bound` moves
`input.times.proof.scoped.inventory`, `component_authorities` and the TR-COMPONENT bit into a private
`RetainedInventory`."

At the pin, `admit_bound` releases `input` differently on the two fenced reads (`current_trust_admission.rs`:1124-1137):
- `proposal = evaluate_retained_ordinary(input, observation, report)` (:1132) moves `input` into the time proposal
  (`trust_time.rs`:590-608; `OrdinaryClockProposal { inputs, observation, assessment }`, :464-468);
- **report reads** (`report: true`): the proposal is a local that is dropped at the end of the arm;
- **non-report reads** (`report: false`): `pending = Some(PendingWrite(proposal))` (:1135-1136). The durable R10 read is
  this case (`live_observation.rs`:131).

On a non-report read, X4T-b's write-ahead consumes the pending proposal in `fenced_first_read`
(`floor_publication.rs`:977-997):
- `build_floor_publication(owner, &pending, …)` (:983-990);
- that calls `proposed_time_input::assemble(&pending.0, …)` (:778);
- which reads `proposal.inputs().closure_raw()` (`proposed_time_input.rs`:106);
- which reads **through the inventory**: `times.proof.scoped.inventory.shared().retained().closure_raw()`
  (`ordinary_targets.rs`:622-630).

So a move inside `admit_bound` on a non-report read would remove the bytes that the write-ahead's `source.closure`
member is built from. r7 §1.1's "`admit_bound` keeps only `ViewClosure` … and drops the rest" (line 138) is likewise
exact only for report reads: on a non-report read, the rest is kept in `pending` until the write-ahead.

## 2. The replacement text

**Replace** r7 §1.2's "The retained values" bullet (lines 148-150) with:

> - **The retained values.** With `retain` set, and the read `ReadMode::Fenced { .. }`, the read moves
>   `input.times.proof.scoped.inventory`, `component_authorities` and the TR-COMPONENT bit into a private
>   `RetainedInventory` **at the point where it releases `input` today**:
>   - **report reads** (`report: true`): in `admit_bound`, from the local time proposal, after
>     `proposal.admission()` and before the arm ends. This is where the proposal is dropped today;
>   - **non-report reads** (`report: false`): in `fenced_first_read`, from the pending proposal that
>     `take_pending` returns. The move happens after `build_floor_publication` and `publish` when a write is needed,
>     immediately before that branch's `return`. When no write is needed, it happens immediately after the
>     `needs_write` decision, before the closing `fence.recheck` and `owner.recheck`. These are the points where the
>     pending proposal is dropped today.
>
>   The returned `AdmittedCurrentTrust` carries it as `Option`. A clocked refusal (`Admission::Clocked`) returns no
>   view, and its retained value is dropped with it.

**Add** to r7 §1.1's "Where it is lost" bullet (line 138), after "drops the rest":

> On a report read. On a non-report read, the rest is kept in `pending` until `fenced_first_read`'s write-ahead
> (E-1).

**Unchanged in r7 §1.2:**
- the `ViewInputs.retain` bullet, with its 13 constructor sites;
- the reserved set;
- **Bootstrap.** Both the first admission and the confirming admission run through `fenced_first_read`
  (`trust_bootstrap.rs`:1247-1262), so the retained value is the confirming admission's;
- **Taking it out** (`trust_start`'s `take_retained`);
- **Without `retain`.** Nothing moves, and `input` is released exactly as today on both reads;
- the revocation carrier.

## 3. What does not change

- **The same read, by move:** no copy, no new load, no new charge, and no new failure point. The move is a field
  move out of an owned value at an existing drop point.
- **X4's first-read semantics (X4T items 6, 7 and 9; the r12 order):**
  - the time proposal, its admission and refusal mapping;
  - the clocked-refusal-after-write-ahead rule;
  - `needs_write`;
  - the write-ahead's inputs, including `source.closure` from the same inventory bytes;
  - `publish` and its reserved confirmation;
  - the closing `fence.recheck`/`owner.recheck`, and their order.

  Each of these sees exactly the values it sees today. Retention only moves a field out of the pending proposal
  **after** the write-ahead's last read of it, at the point where the proposal would otherwise drop.
- **Publications and epochs:** no change to what is written, to confirmations, or to `advance_current`.
- **J1's R10/R10a/R11/R12 order and X2's lease terms:** unchanged. P-0 still completes inside R10's one read, before
  `trust_start` returns.
- **Without `retain`** (`begin`, rereads, doctor and every other caller): byte-for-byte the current code path.

## 4. Files added to the implementation by E-1

| File | Change | LD-Q-203 classification |
|---|---|---|
| `crates/security/src/trust_time.rs` | `OrdinaryClockProposal::into_inputs(self) -> OrdinaryClockInput`, a consuming accessor | no to census closure or receipts, no to PRICE_PREMISES, no to Cargo.lock |
| `crates/security/src/trust/floor_publication.rs` | the two non-report move points in `fenced_first_read` | no to census closure or receipts, no to PRICE_PREMISES, no to Cargo.lock |

The classifier was re-run over the 23-row planned set including these two files:
`evidence/ldq203-classification/CLASSIFICATION-v2-output.txt` (`557bdb9f…`), with 0 rows touching a shared artifact.

## 5. Controls added by E-1

- **C-P0-1 (non-report read):** with `retain` set, a fenced `report: false` read whose write-ahead is needed publishes
  exactly the same files, with the same `source.closure` bytes, as the same read without `retain`, and its view
  carries `Some(RetainedInventory)`. The no-write case is covered the same way.
- **C-P0-2 (report read):** with `retain` set, a report read returns a view with `Some(RetainedInventory)`, and the
  same row and epoch as without `retain`.
- **C-P0-3 (bootstrap):** on the bootstrap branch, the retained inventory is the confirming admission's. Its
  identities equal the confirmed catalog's.
- **C-P0-4 (without retain):** the existing first-read tests (`floor_publication_tests.rs`,
  `trust_bootstrap_tests.rs`, `current_trust_admission_tests.rs`) pass unchanged, with `retain: false` at their 11
  constructor sites. Every view without `retain` carries `None`.
- **The mutations,** each caught by a failing test:
  1. the non-report move point is skipped: C-P0-1 sees `None`;
  2. the report move point is skipped: C-P0-2 sees `None`;
  3. retention ignores `retain`, and moves on every fenced read: C-P0-4's `None` check fails.

  4. **(r2, E1-RF-1)** a retention-only early return: before `take_pending`, `return admission.into_view()` when
     `retain` is set and the admission is `Clocked`. This skips the write-ahead and its confirmation. C-P0-5's
     ordinary and bootstrapping clocked-refusal cases kill it, by requiring one confirmed publication before the
     refusal.

  **The ordering, stated precisely (r2).** The borrow checker establishes only the **ownership** dependency:
  `build_floor_publication` borrows `&pending`, so moving the retained fields out before it does not compile. It
  does **not** establish the control flow. In particular, it does not rule out an earlier return that drops
  `pending`, nor does it prove that `publish` and its confirmation ran before a clocked refusal. C-P0-5 establishes
  that order.
- **C-P0-5 (r2, E1-RF-1: clocked refusals with retention enabled).** The existing clocked-refusal fixtures run under
  **both** `retain` settings, and the original no-retention coverage is kept:
  - `floor_publication_tests.rs`:801-851 (`issued_later()`, `observation("boot-2", 100, STALE_WALL)`), through both
    the ordinary and the bootstrapping entry points. Each case must refuse **after one confirmed publication**, with
    the same owner advancement and the same capsule contents. Its second observation is the sticky refusal with no
    write;
  - :855-875: the report-only clocked refusal, and beyond-horizon precedence with no publication.

  For each case, the run with `retain` must be equal to the run without it in all of the following:
  - the refusal row and cause;
  - the durable effects (the published files and the capsule), the confirmations and the owner state;
  - no view is returned;
  - the existing sticky/no-write and report/horizon behaviour.
