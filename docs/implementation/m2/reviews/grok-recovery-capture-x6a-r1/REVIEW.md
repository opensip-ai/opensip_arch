# X6a r1 — read-only recovery capture

REQUIRED-FINDINGS. The capture mislabels one lawful floor state as a floor regression, and its closure chain can confirm a joining SEAL across a generation whose last row is not `TERMINAL`. Inventory v124 is accepted on v122 with D2 folded.

Product worktree `/Users/sb/code/opensip-ai/opensip-x6a`, detached at `933e78be8cd8ebbf1b622b39a84b0b3dd1396117`. `product.diff` is 82225 bytes, sha256 `8848ba37669838503989f44dbf5f5e964260b2bffca5c87fdcfcfea8c8363d75`: four files, `carrier_dispatch.rs`, `carrier_floor.rs`, and the two intent-to-add capture files. `~/Library/Application Support/OpenSIP` is absent. `build_v124.py` was not run.

## RF-1 — the hazard treats a later-generation floor as F22

Owner step 3 (`commit-recovery-readonly.v3.md`): when `k > t` still holds after the fresh capture, the F22 quarantine requires `stableH`, agreeing tails, and `H.lastSeq >= k`. Otherwise the standing is `unavailable-busy`.

`covers()` (`recovery_capture.rs` 647–653) is true for every floor in a later generation. The anchor uses that for case C, and that use is right: a floor written after `g` closes covers the records of `g`. The F43 arm (795–799) uses the same predicate when `query.seq > t`. A later generation then sets `covers: true`. `decide` (874–880) reports `UnknownQuarantineCondition` / `FloorRegression` with `offending: None`.

That arm is reached for a lawful open-successor floor. `floor_against` (carrier_floor.rs 747–759) returns `Unchanged` for a floor exactly at the witnessed successor’s empty tail `(G+1, 0, null)`. The floorOk check skips `seq == 0`. A query with `k > t` in the closed generation then takes the hazard. `H.lastSeq` is 0, and `0 >= k` is false for every admitted `journalSeq`. The owner’s standing is `UnavailableBusy`.

A same-generation floor above that generation’s own tail is already `FloorRegression` at step 14 when the floor is compared with the copy tail (`compare_with_floor`, Equal/Less) or fails floorOk. `the_f43_hazard_retries_once_and_never_concludes_uncommitted` plants the floor at `s.seq + 1` and expects the floor digest; that expectation is step 14. The hazard arm itself drops the digest.

`covers()` stays as it is for case C. In the `k > t` arm, `covers` is true only when `f1.generation == query.generation && f1.seq >= query.seq`. `Verdict::Hazard` carries `offending(h1)`, and the decide arm copies that digest into `UnknownQuarantineCondition.offending`. A test with a closed `g`, witness case-1 `COMMITTED 0`, floor `(G+1, 0, null)`, and a query sequence above `g`’s tail, both captures stable, expects `UnavailableBusy`.

## RF-2 — the closure chain sums TERMINAL rows

Call 12 is the right rule. A generation is closed when its last row is `TERMINAL`, which is how `committed_tail` reads the predecessor (carrier_floor.rs 513–522): the last row below the newest must be `TERMINAL` in the previous generation. The capture’s chain is that test for every generation in `[g, newest)`.

`current_view` (516–525) does something else. It requires `COUNT(DISTINCT grantGeneration) == span + 1` and `SUM(record_type = 'TERMINAL' AND grantGeneration < newest) == span`. The sum counts rows. A generation whose last row is not `TERMINAL` still contributes 1 when an earlier row is `TERMINAL`. `committed_tail` only inspects `newest - 1`, so an intermediate generation is invisible there. The requested generation’s own last-row check can still pass. A joining SEAL in `g`, with an OK witness on the open newest generation, then confirms.

Concrete shape the sum accepts: generation 1 closed on its last row; generation 2 holding a `TERMINAL` and a later non-terminal row; generation 3 closed on its last row; generation 4 open, with the witness and floor at that tail. `span` is 3 and the sum is 3. The predecessor of generation 4 is generation 3. The SEAL in generation 1 confirms.

`gj3_append_laws` (journal_store.rs 874–876) aborts a second `TERMINAL` and any append once one exists. Those are insert triggers. This module’s `plant` drops `gj3_append_laws`, inserts, and restores it (recovery_capture_tests.rs 85–113). Rows already in the file are what the reader classifies. The distinct-count case (generation 2 missing under generation 3) stays a `ProtocolViolation`.

Replace the sum. For `g < newest`, count generations in `[g, newest)` whose maximum-`seq` row has `record_type = 'TERMINAL'`, and require that count to equal `newest - g`. A missing generation and a generation whose last row is not `TERMINAL` both fail. An extra `TERMINAL` in one generation does not close another. Add the intermediate-generation case above and expect `ProtocolViolation`.

## Call 1

Accepted. X3b r10 item 4a assigns would-OPEN to X6, and the open-successor floor exception is r9. `succession` and `floor_against` apply that to the newest tail. On an open newest generation the witness is the owner’s A, B, C, and C′. On a closed generation the witness anchors the newest effective tail, and case C still uses `covers()` for records at or below that generation’s tail. A `PENDING` after a `TERMINAL` is `ProtocolViolation`. A floor at `(G+1, 0)` while the witness still names `G` is regression in `floor_against`. Literal `W.grantGeneration == A.grantGeneration` would busy every historical SEAL after OPEN moves the witness, and it is rightly unused. The laws do not contradict each other. RF-1 is the hazard arm applying `covers()` past `k > t`.

## Calls 2–11, 13, and 14

Accepted.

- The journal snapshot reads the tail, the requested generation’s count and last row, the chain, and the SEAL. `generation_anchor` and `bracketed_capture` are unchanged. Contiguity is `COUNT(*)` against the last seq under the primary key.
- Row 1 (`journalCarrierDigest` against SHA-256 of N) returns `BindingUnusable` with zero captures (324–330). A witness or floor naming another project is a `CarrierBinding` candidate and still needs the five stable observations.
- An absent floor beside a present carrier is `FloorLost` (760–761).
- `inherited_present` keeps the inherited-format observation. The unpublished `{A, B}` prefix is busy; a fresh partial set is a footprint candidate.
- `SQLITE_BUSY` / `LOCKED` is busy. Other carrier I/O is `UnknownCustody{CarrierUnreadable}`. An unreadable witness or floor is busy after the fresh capture.
- F28: generations 1 and 2 removed, 3 closed, 4 open, predecessor check intact, association in generation 1 is `RecordPruned` on one capture. A missing sequence inside `g` is `JournalContiguity`. A missing generation between `g` and the newest is `ProtocolViolation` through the distinct count. RF-2 is the unclosed intermediate generation that distinct count does not see.
- `bytes()` omits `-shm` and an empty `-wal` (171–174).
- The module is `pub(super)` under `carrier_floor` (1178–1181), macOS only, with no crate re-export.
- Points are `x6.recover` / `after-w1`, `after-h1`, `after-j`, `after-w2`, `after-h2`, and `after-fresh-capture` after the second capture’s decision is still pending (287–296, 340–343). `after-lease` and `after-ledger-snapshot` are absent.
- The hazard report also requires `stableW` and equal journal snapshots (869). That is step 4’s five observations, which include the owner’s `stableH` and agreeing tails.
- `SealJoin`, `PendingAboveFloor`, `CarrierAbsent`, `CarrierUnreadable`, `RecordPruned`, and `NoSuccessor` settle on the first capture.
- Reads charge the caller’s `WorkScope` and return `WorkBudgetError`.

The SEAL join checks schema 3, type `SEAL`, operation ref, run id, the stored digest, a canonical body, the domain-framed digest (`opensip.metadata.journal.1` || 0x00 || canonical), `seal_run_id`, and the body’s generation, sequence, and operation ref (549–582). X8 has no owner row in this diff. X6b and X6c are uncalled.

`carrier_floor.rs` lines 9–10 still say a `CarrierLocation` has no production constructor until X3b-3. The v124 README leaves that description to the next description successor. The inherited row is equal by value. Disclosure only.

## Inventory

ACCEPT. v124 is 491985 bytes, sha256 `ea302ab3b842b043701526590964feb1e4b7def3b3f48a8634261e603badf476`, parent v122 485705 / `69cf90db0ade09fc0f9536b3ef293d7de6aff68c7d3ae9a2aabfab4f6c244c7a`. Successor record 145238 / `70da80f6e024b405b8cf1da549ab64d2ecdd73995966149f02edf6dbd5f4c9f8`. Subject 2146 / `68fe96ea82ada0fb28217fd335add322833fd07fde99176a4a7f70e1821df00b`.

920 files against v122’s 918. Added `recovery_capture.rs` (validator) and `recovery_capture_tests.rs` (test). Removed none. 918 inherited file records are equal by value. `packages`, `pendingDecisions`, and `schemaVersion` match. The standing text differs.

Projection: 55 rows. Each D2 supersession keeps the raw v122 description as `before` and the v124 file description, and its `effectiveDescription` is D2’s `after`. D2’s `before` is the lock inheritance `after` for that selector. The four paths are `store_lineage.rs`, `installation_session.rs`, `read_premise.rs`, and `initial_installation.rs`. `verify_projection.py` against the worktree lock: `{"readOnly": true, "projectionRows": 55, "positive": "PASS", "corruptionsRefused": 278, "directParentOverrideIncluded": true}` with `folded == 4` and each parent file record equal to the candidate record. `verify_scratch.py`: passed, 83 inventory successors, 74 contract successors, 55 inheritance rows, selected inventory v124.

## Replay

Private `TMPDIR` `$(getconf DARWIN_USER_TEMP_DIR)/grok-x6a-tmp`, mode 0700. `CARGO_TARGET_DIR` under this review directory. Both were removed after the runs.

`cargo test --locked --offline -p opensip-security --lib -- recovery_capture`: 23 passed, 0 failed, 917 filtered, 4.92s.

The same filter with `--features opensip-platform/crash-matrix`: 23 passed, 0 failed, 917 filtered, 4.88s.

Workspace `cargo test`, clippy, `cargo fmt`, and `check_package_edges` were not replayed.
