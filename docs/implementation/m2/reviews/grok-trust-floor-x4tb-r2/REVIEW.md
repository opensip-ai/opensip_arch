# X4T-a2 and X4T-b r2

ACCEPT-UNIT. RF-1 is closed. Inventory v106, rebuilt on v112, is ACCEPT. Nothing new is wrong.

Law is X4T r9. The worktree is `opensip-x4tb` at `f1b832183c1c9fc0ef1da647945b45453061a06c`. `git diff` is 106921 bytes, sha256 `513adaeb1cf17b361cfd45479ca4696d2bb3eb665ec48537596f6fb4b82cbb6d`, 13 files, 2079 insertions and 86 deletions. The two new files are intent-to-add. Every product file in hashes.txt matches. `~/Library/Application Support/OpenSIP` is absent. The real account home was not opened.

r1's judgment calls 1 to 10, 12 and 13 stand. The diff of this round against the r1 diff changes only `installation_session.rs` (the attempt bound is now `pub(crate)`), `floor_publication.rs`, and `floor_publication_tests.rs`. The other ten files are the same hunks r1 accepted. The unit does not touch `custody.rs`, `first_registration.rs`, `installation_read.rs`, `ordinary_writer.rs`, `namespace_lease.rs`, or `work_ledger.rs`, and it does not call `reserve_settlement`. X3d-0 left `effect`, `prepaid`, `spend`, `charge`, and `scope` as they were: `effect` charges the whole reserve before the closure, and a prepaid charge draws from that allowance.

## RF-1

`capped_read` is gone. `file_cost` and `confirmation_cost` both reserve `exact_read`, which is `read_bounded_cost(len, installation_session::attempts(len))`. `attempts` is the read session's own function: one growth to `len + 1` on the 4 KiB doubling sequence, the EOF read, and four spare. It is reused, not copied. The growth step is the platform's `next_buffer`.

`read_bounded_cost` is one object, that many edges, and the sum of every requested growth through `len + 1`. `read_bounded_accounted` charges that object, one edge and the full buffer size on each growth, and one edge on a later attempt. For a file of length `len` read at `max = len`, a full read charges exactly those growth bytes. Across every length from 1 through 131072 the reserved bytes equal the charged bytes, and the reserved edges cover the read. At r1's seven boundaries the old `2·len + 8192` allowance was short by 4097, 1, 20481, 1, 53249, 1, and 118785 bytes. The platform cost covers each of those.

`publish` charges the opening owner recheck, then one `effect` of the writes plus the confirmation. The confirmation's second judged sample is the owner's closing recheck, inside that reservation. After the effect, `publish` decodes the reread it already paid for and rechecks the fence, which does not take the ledger. `fenced_first_read` returns on that publication. On the no-write path it still rechecks the fence and the owner.

The other reserved terms are the published platform costs r1 accepted: ACL captures, the owner allow, child opens, the absence probe, `write_new_regular_cost`, `rename_replace_cost`, the directory barrier, and `open_regular_cost`. The pointer's reopen term is `publish_private_file`'s `reopen_confirmation_cost` (2 objects, 4 edges, `len + 1` bytes), and that reopen is its own `work.run` of the same cost. The read-only admission still reads through `Budget::load`.

`the_reservation_covers_both_exact_rereads_at_every_growth_boundary` publishes, at 16384, 20480, 32768, 53248, 65536, 118784, and 131072, a capsule padded to that length beside an equal content-addressed record, so both exact rereads run. A measured ledger total completes on a fresh site and advances the pointer and the owner. One byte less refuses on the budget row, `state.v1` is unchanged, and no `state.v1.*` temporary is left beside it. Because `effect` charges the reserve before the closure, that short ledger fails before the first write.

## Inventory v106

v106 is 791 files: all 789 v112 rows by value, plus `floor_publication.rs` and `floor_publication_tests.rs`. Schema, packages, and pending decisions match v112. The standing this candidate authors names law X4T r9 and units X4T-a2 and X4T-b. The two added descriptions name the exact reread at `read_bounded_cost` with the session attempt bound, and the seven growth boundaries. The number 106 sits below 112; the parent pin is v112. The sixteen description overrides stay on the v112 rows, re-indexed by path. `build_v106.py` lists v109, v110, and v112 as prior parents and was not re-executed, because it writes the architecture tree. The candidate bytes were checked against v112 directly.

Subject manifest sha256 `2ba7003f99c7d8e3e11f9d1d22bed5c27cd72521f4e97f1f6a4e131724686903` (2108 bytes). Each file it names matches.

## Replay

`cargo test --locked --offline -p opensip-security --lib`, default `TMPDIR`, `CARGO_TARGET_DIR` under this review directory: 13 floor-publication tests, 19 current-trust admission tests, 7 accepted-store fixture tests, and `a_confirmed_trust_publication_is_the_only_advance_of_the_state_v1_owner`. 40 passed, 0 failed. The boundary test is one of the 13.

`cargo clippy --locked --offline -p opensip-security --all-targets -- -D warnings` passed. `rustfmt --edition 2024 --check` on the thirteen touched files reports the same wrap class r1 recorded on these files and their parents. That is not a finding. The two workspace runs the lead reports (1433 passed, 0 failed, 3 ignored) were not replayed, and workspace clippy was not replayed.

`verify_scratch` on the worktree lock at f1b8321 passed: 74 inventory successors, 72 contract successors, 16 inheritance rows, v106 selected. `verify_projection` against that lock: 16 rows, 83 corruptions refused, read-only. `check_package_edges --lane host` against v106 passed: 19 declared edges, 19 resolved. The cargo target was removed after the replay.
