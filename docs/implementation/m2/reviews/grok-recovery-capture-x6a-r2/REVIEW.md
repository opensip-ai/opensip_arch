# X6a r2 — read-only recovery capture

ACCEPT-UNIT. r1's two findings are closed, and the rest of the accepted capture is unchanged. Inventory v124 is accepted on v123, with D2's four supersessions already folded into the parent's inheritance rows.

Product worktree `/Users/sb/code/opensip-ai/opensip-x6a`, detached at `54e616610e8b698e9b5bf7cbcb6ea89f1182e9b4`. `product.diff` is 85509 bytes, sha256 `eb5e1c8868ee29d2322bbf79bef3e565019279f078848999870cfffb3e0b8db8`: four files, 2137 insertions and 1 deletion. The two new files are intent-to-add. Commits from the r1 head `933e78be8cd8ebbf1b622b39a84b0b3dd1396117` through this head do not touch those four paths. The `carrier_dispatch.rs` and `carrier_floor.rs` hunks match r1. The capture source differs from r1 only in the closure query, the hazard verdict, and the two new tests. All 31 pins in `hashes.txt` match. `~/Library/Application Support/OpenSIP` is absent. `build_v124.py` was not run; it writes the inventory and the successor record.

## RF-1

Closed. `covers()` (recovery_capture.rs 654–657) is still true for a later-generation floor, and the only call is case C (`Reconciled::Revert`, line 843). In the `k > t` arm (806–810) the flag is `f1.generation == query.generation && f1.seq >= query.seq`. `Verdict::Hazard` carries `offending(h1)`, and `decide` (887–893) copies that digest into `UnknownQuarantineCondition.offending`.

`a_query_above_a_closed_generation_with_the_open_successor_floor_is_busy` plants a closed generation 1, a case-1 `COMMITTED (2, 0)`, and the floor at `(2, 0, null)`. A query one above generation 1's tail is `UnavailableBusy` after two captures. The SEAL below that tail confirms `WitnessCommittedTail` on the same state. `Fixture::recover` checks the bytes and the point order on both calls.

`floor_against` (carrier_floor.rs 752–760) still treats the open-successor floor as `Unchanged`, and floorOk still skips `seq == 0`, so that floor reaches the hazard arm. A same-generation floor at or above `k > t` is refused earlier when it has a body: `compare_with_floor` when the requested generation is the newest, and floorOk when it is closed and the row at that sequence is absent. `the_f43_hazard_retries_once_and_never_concludes_uncommitted` is unchanged and still takes that step-14 path, with the floor digest. The hazard quarantine arm implements owner step 3 and is reached by no current test. That is the reachability the fix produces. It is not a remaining defect.

## RF-2

Closed. For `g < newest`, `current_view` (523–528) counts rows in `[g, newest)` whose `record_type` is `TERMINAL` and whose `seq` equals `MAX(seq)` for that generation, and requires the count to equal `newest - g`. The distinct-generation count is gone. Under the `(grantGeneration, seq)` primary key the count is one per generation. A missing generation adds nothing. A generation whose highest-seq row is not `TERMINAL` adds nothing. An earlier `TERMINAL` in that generation does not add another.

`an_intermediate_generation_whose_last_row_is_not_terminal_breaks_the_chain` plants generation 2 as `TERMINAL` then `RA`, generation 3 closed, and generation 4 open with a matching witness and floor. `committed_tail` (513–522) only requires generation 3 to end in `TERMINAL`, so the predecessor check passes. The SEAL in generation 1 is `ProtocolViolation` after two stable captures. With generation 2 ending in its `TERMINAL`, the same SEAL confirms `WitnessCommittedTail`. `plant` still drops `gj3_append_laws`, inserts, and restores the trigger. The missing-generation case in `a_broken_succession_or_gap_is_a_protocol_violation_and_a_gap_in_g_is_contiguity` remains.

## Calls 1–11, 13, and 14

Accepted again. The r2 diff does not change them.

The journal snapshot still reads the tail, the requested generation's count and last row, the chain, and the SEAL. Contiguity remains `COUNT(*)` against that generation's last sequence. Row 1 returns `BindingUnusable` with zero captures (324–330). A witness or floor naming another project is a `CarrierBinding` candidate under the five stable observations. An absent floor beside a present carrier is `FloorLost`. `inherited_present` keeps the inherited-format observation: the unpublished `{A, B}` prefix is busy, and a fresh partial set is a footprint candidate. `SQLITE_BUSY` / `LOCKED` and an unreadable witness or floor are busy after the fresh capture. Other carrier I/O is `UnknownCustody{CarrierUnreadable}`.

F28 is unchanged: generations 1 and 2 removed, 3 closed, 4 open, predecessor intact, and an association in generation 1 is `RecordPruned` on one capture. A missing sequence inside `g` is `JournalContiguity`. `bytes()` omits `-shm` and an empty `-wal`. The module is `pub(super)` under `carrier_floor`, macOS only, with no crate re-export. `SealJoin`, `PendingAboveFloor`, `CarrierAbsent`, `CarrierUnreadable`, `RecordPruned`, and `NoSuccessor` settle on the first capture. Reads charge the caller's `WorkScope` and return `WorkBudgetError`. Every `Confirmed` has `limitation()` `interior-bodies-not-authenticated`.

The SEAL join (549–586) checks schema 3, type `SEAL`, operation ref, run id, the stored digest, a canonical body, the domain-framed digest (`opensip.metadata.journal.1` || 0x00 || canonical, computed in `JournalRecord::parse`), `seal_run_id`, and the body's generation, sequence, and operation ref. X8 has no owner row in this diff. X6b and X6c are uncalled.

`carrier_floor.rs` lines 9–10 still say a `CarrierLocation` has no production constructor until X3b-3. The v124 README leaves that description to the next description successor. The inherited row is equal by value. Disclosure only.

## Points

The `x6.recover` points are `after-w1`, `after-h1`, `after-j`, `after-w2`, `after-h2`, each immediately after its read (287–296), and `after-fresh-capture` once, after the second capture's `H2` and before `decide` (340–343). `after-lease` and `after-ledger-snapshot` are named in the module comment as X6b's. The source pin requires each of the six capture points exactly once, and `recover` requires the bracket order.

## Inventory

ACCEPT. v124 is 497254 bytes, sha256 `94d374791cda35d373d846c2c843439ee7df188f01f1c6dc929e79c4ddc1360c`, parent v123 490531 / `e183e6dafe21b40985f83136b9b5b2fe48e39a9a1cfad207a2d6d616fb5e6171`. Successor record 145222 / `2e58b8300c1f334ca0fc7d8fcb74c8f1bdb40d0840c643cc7be90f6606aa7cfc`. Subject 2146 / `4445a794bea86c827679d211419521410ff4751b9d30eec68ea57613e46094ae`.

924 files against v123's 922. Added `recovery_capture.rs` (validator) and `recovery_capture_tests.rs` (test). Removed none. All 922 inherited file records are equal by value. `packages`, `pendingDecisions`, and `schemaVersion` match. The standing text is this unit's sentence.

The validator description says the chain counts generations ending in a `TERMINAL` on the highest-seq row, and that the F43 hazard's F22 condition is a floor in the requested generation at or above the requested sequence, carrying that floor's digest. The test description names the open-successor busy case and the intermediate generation whose last row is not `TERMINAL`.

Projection: 55 rows, carried by stable path. 38 candidate selectors are unchanged and 17 advance by 2, which is the two paths inserted under `journal_store/`. Each row's `before` equals the v123 file description, and that description equals the v124 file description. For D2's four paths (`crates/identity/src/store_lineage.rs`, `crates/security/src/custody/installation_session.rs`, `crates/security/src/custody/read_premise.rs`, `crates/security/src/initial_installation.rs`) the lock's inheritance `after` on v123, and the projection's `effectiveDescription`, are D2's `after`. The file rows stay the raw `before`. No supersession is bound on v123: the builder's fold count for this parent is 0, and the lock has no `inventoryPassageSupersessions` key. D2's four records remain on v122 inside the contract successor.

`verify_projection.py` against the worktree lock at 54e6166: `{"readOnly": true, "projectionRows": 55, "positive": "PASS", "corruptionsRefused": 278, "directParentOverrideIncluded": true}`. `verify_scratch.py`: passed, 84 inventory successors, 74 contract successors, 55 inheritance rows, selected inventory v124 (`94d37479…`, 497254 bytes). The same `verify()` result's `inventoryPassageSupersessions` is 4, the historical D2 rows on v122. The scratch script's printed JSON does not include that field. The worktree `design-lock.json` matches the main checkout at this head (315501 bytes, `8adbb4df0b7d7a7b69afcd029005642517880c05926869780852f3e3903caa63`) and the verifier anchor.

## Replay

Private `TMPDIR` `$(getconf DARWIN_USER_TEMP_DIR)/grok-x6a-r2-tmp`, mode 0700, parent `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/`. `CARGO_TARGET_DIR` under this review directory. Both were removed after the runs.

`cargo test --locked --offline -p opensip-security --lib -- recovery_capture`: 25 passed, 0 failed, 917 filtered, 4.55s.

The same filter with `--features opensip-platform/crash-matrix`: 25 passed, 0 failed, 917 filtered, 4.36s.

Workspace `cargo test`, clippy, `cargo fmt`, and `check_package_edges` were not replayed.
