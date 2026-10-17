# C1c-0 r2: the read set's preparatory primitives (M3-C r8 items 1 and 3; C1c plan r4, sub-unit C1c-0)

**Lead scope record, 2026-10-17. Unreviewed candidate, round 2: the mechanical rebased round in the open C1b batch interval.**

**Round 1 was never submitted.** It was packaged on `72e0787`, ahead of C1b-0. C1b-0's census outputs then overlapped it, so its integration was refused by design. This round is the same change rebased onto C1b-0's main:
- it is byte-identical in every hand-written file except `snapshot_walk_tests.rs`, where C1b-0 changed no line, and the three-way apply only moved context;
- every generated output is regenerated on top of C1b-0's;
- the receipt record is cumulative.

It implements sub-unit C1c-0 of the C1c plan r4 (`c1c/PLAN-r4.md`, accepted by Codex `codex-c1c-plan-r4`). C1c-0 is the preparatory machinery that C2b's layout reads need and that the read set (C1c-1) builds on.
- **Library only:** no production caller. C2b consumes `capture_pruned`; C1c-1 consumes the rest.
- **One new path:** `crates/security/src/snapshot_read_set.rs`. An inventory successor follows.
- **One census-closure file changes:** `crates/security/src/custody/discovery_rule.rs` (LD-C1C-9).

**Base and sequencing.**
- **The lane base and candidate base** is product main `caa71e2` (unit D3a-2). In order, it holds:
  - C1a4's blind refresh (`0772eb7`, both receipts current);
  - C1b-0 (`c9c18f7`, the vcs-observation schema-3 materialization), which opened the C1b batch interval;
  - its contract-176 lock (`9ea2d4a`);
  - D3a-2 (`caa71e2`, components and platform).
- **The rebase was mechanical:**
  - the source patch reapplied without conflict. Of the files C1c-0 edits, main changed only the two generated census records;
  - the `discovery_rule.rs` CLOSURE re-pin carries unchanged, because no commit since `b753854` touches that file or the census tool;
  - every generated output was regenerated with the tools' own `--write` over the lead-readable cache, on top of C1b-0's records.
- **Against main's records, the regenerated outputs differ only as C1c-0 explains:**
  - **`discovery_census.json` and its vectors:** `closure`;
  - **the workspace ledger:** `closure` and `tools`;
  - **`snapshot_ledger_census.json`:**
    - `pins`;
    - the five workspaces' `allMountsAsMembers` rows, by the member copies, every row still passing 2×;
  - **the walk vectors:**
    - `pins`;
    - `prunedOpeners`;
    - only the member case's prediction (+1 object, +129 bytes);
  - **the session vectors:** `pins`.

  The held-out rows were already rendered stale by C1b-0.

**The integrate script refuses unless main's changes since `caa71e2` are disjoint from C1c-0's paths.** A later census-input unit therefore means another rebased round.

**Which interval (LD-C1C-9): C1c-0 joins the open C1b batch.**
- **The batch:**
  - C1b-0 r2 (ACCEPT-DESIGN-UNIT, `c1b-0-r2-unit.json`) opened it at its integration;
  - its accepted baseline is C1a4's blind refresh (`c1a4-blind-run-r1-unit.json`, receipts at `0772eb7`), with both receipts `holds (blind census)`;
  - its final-input freeze is set by the batch's pre-run review, which has not happened.
- **C1c-0 joins before the freeze.** It integrates into the open interval, and the batch's one refresh covers it. The integrate script records the join, and it refuses if CURRENT-STATE records the batch as frozen.
- **The cumulative receipt record** (`evidence/receipt_specific_record.py`; the lane's `receipt-specific.json`). From public receipt fields only, per receipt, it records:
  - **the baseline:** the receipt's bytes on main equal the refresh's and C1b-0's recorded baseline pins;
  - **the batch so far** (main against the receipt): exactly C1b-0's delta, the `generator-closure.json` digest in `reference`, and in the companion receipt that same digest under `discovery`;
  - **C1c-0's own delta** (the candidate against main):
    - **the discovery receipt:** `closure` (exactly the `discovery_rule.rs` row) and `tool` (the census tool's re-pinned CLOSURE);
    - **the companion snapshot receipt:**
      - `discovery` (the same two bindings);
      - `tools` (`discovery_census.py` and `snapshot_ledger_model.py`);
      - `snapshotSources`: `snapshot.rs` and `snapshot_tests.rs` (host), `snapshot_source.rs` and `snapshot_walk.rs` changed, and `snapshot_read_set.rs` added;
  - **the cumulative delta** (the candidate against the receipt): exactly the union of the two;
  - **the rendering:** neither receipt's bytes change, and both records render all ten held-out rows `outstanding: held-out (blind receipt stale)` with `heldOutMargin: outstanding`.
- **The batch's frozen inputs must include C1c-0's bindings.** An earlier refresh never covers them.

## What it changes

| File | Change |
| --- | --- |
| `crates/security/src/custody/discovery_rule.rs` | **`read_set_path(authorized, relative, first_party_cargo_roots, dependency_cargo_roots, member_roots)`** (LD-C1C-5, r3), beside `classify_path`, which is unchanged. It checks the full path (the authorized directory, then the descendant):<br>- `authorized` must hold an exact `node_modules` segment, or the result is `Forbidden`;<br>- a VCS segment anywhere excludes;<br>- the exact root and member `.opensip` anchors exclude (`custody_state`);<br>- a further `node_modules` below `authorized` excludes (a nested package);<br>- a `target` directly under a first-party or dependency-tree Cargo root excludes.<br>It reuses the rule's private tables and duplicates none.<br>**`is_dependency_cargo_root`** (LD-C1C-13). **`pruned_capture`**, the pruned-tree capture's place: its outermost dependency segment, `Outside`, or excluded by a VCS segment or a custody anchor. `ReadSetPath` and `ReadSetExclusion` are public, re-exported by the read-set module. `CARGO_MARKER` becomes `pub(crate)`. |
| `crates/security/src/snapshot_read_set.rs` (new) | **`open_pruned`** (LD-C1C-2): the pruned-tree capture opener. The validated copy is charged first and kept. The rule's temporaries are charged. The root is judged. Each directory component is observed no-follow through its parent, opened `O_NOFOLLOW` and compared, and judged under S3 custody only above the dependency anchor. The leaf is opened and compared, with no config-file custody (the Q2 ruling). A symlinked component refuses.<br>**`authorize_read`** (LD-C1C-5): `read_set_path` over the walk's own evidence, charged its published `read_set_path_cost`.<br>**`observes_dependency_cargo_root`** (LD-C1C-13): the charged no-follow `Cargo.toml` observation. No byte is read. |
| `crates/security/src/snapshot_walk.rs` | **`WalkEvidence`** (LD-C1C-13, r4): `walk_snapshot_retaining` returns the report and the evidence, and `walk_snapshot` keeps its signature over the one walk.<br>- **The first-party Cargo roots are a move.** A finished frame no longer drops its root from `known`, and `known` moves into the evidence. Each key was already charged once, as an owned record, when it was derived (`key_cost`). The ledger never refunds, so there is no new charge.<br>- **Classification is unchanged:** `classify_path` tests only a path's own prefixes, so a kept non-ancestor root never matches.<br>- **The member roots are new copies,** each charged `owned(len)` first.<br>`SnapshotExtent::member_roots()` is added for the opener. `Level` loses its now-unread `rel` and `pushed_cargo` fields. |
| `crates/security/src/snapshot_source.rs` | `SnapshotRefusal::PrunedPath {path, reason}`. |
| `crates/security/src/lib.rs` | `pub mod snapshot_read_set` (macOS), appended (the file is base-dirty). |
| `crates/host/src/snapshot.rs` | **`CaptureSession::capture_pruned`** (C2's layout reads): the kept capture if one exists, never a second read; otherwise `open_pruned`, then the one read. `CaptureSession::walk` keeps the walk's `WalkEvidence`, moved and uncopied, and `walk_evidence()` exposes it. |
| `crates/security/src/custody/discovery_rule_tests.rs`, `crates/security/src/snapshot_walk_tests.rs`, `crates/host/src/snapshot_tests.rs` | The controls (below). The session's source-read pin now covers the new module. |
| `tools/security/snapshot_ledger_model.py` | **The retention's model** (LD-C1C-13, r4):<br>- the frame-exit discard is gone (a `known.remove` refusal pins it);<br>- the member-root copies are charged;<br>- new anchors cover the kept roots, the move, the copy site and the pruned opener's charge shapes;<br>- the new module is pinned whole;<br>- **the pruned opener's model** (`pruned_opener_cost`) adds three `prunedOpeners` vector cases;<br>- the session's capture-site anchor counts three sites. |
| `crates/security/src/snapshot_ledger_vectors.json`, `crates/host/src/snapshot_session_vectors.json` | Regenerated. **Only the member case's prediction moves** (`opensip-anchors-root-and-member`: +1 object, +129 bytes, its one member root's copy). Every other walk case's prediction is unchanged: the Cargo-root move costs nothing. The session predictions are unchanged, and the pins move. |
| `tools/security/discovery_census.py`, `crates/security/src/custody/discovery_census.json`, the workspace ledger record, `crates/security/src/snapshot_ledger_census.json` | The CLOSURE row for `discovery_rule.rs` is re-pinned, and the records are regenerated by the tools' own `--write` over the lead-readable cache only. The `--check`s then pass. |

## Lead decisions

- **LD-C1C0-1. `walk_snapshot` keeps its signature.** Its existing callers are the host session and the security tests. `walk_snapshot_retaining` is the one implementation, and `walk_snapshot` drops its evidence. Every walk therefore charges the same, including the member copies, and the model prices one walk.
- **LD-C1C0-2. The opener refuses only what the rule places outside the read set's reach.** It refuses a path with no dependency segment before its leaf, or with a VCS segment or a custody anchor on it. Cargo build output, `ignorePaths` and boundaries are not the opener's to judge: a capture there stays a leftover unless the read set reaches it (LD-C1C-6, LD-C1C-12), and sealing refuses leftovers.
- **LD-C1C0-3. The rule's temporaries are priced by the read-set module.** `read_set_path_cost` and the opener's `pruned_capture_cost` are counted from the rule's source, as `classify_cost` is in the walk, because the rule is pure and holds no `WorkCost`. The model anchors the opener's charge shape.
- **LD-C1C0-4. The kept Cargo key's charge already covers its storage.** Each key is priced as `owned`: one object plus its bytes and the record overhead (`discovery_walk.rs`). That price is what the walk already pays for its share of the set's storage. Keeping the key changes no charge, and the exact vector equality on every Cargo case is the control.
- **LD-C1C0-5. This round is the rebased round in the C1b batch.** Round 1 ran on `72e0787`, after the blind run and ahead of C1b-0, and was not submitted. C1b-0 then opened the batch, with census outputs that overlap C1c-0's. LD-C1C-9 lets C1c-0 join a reviewed open interval only before its freeze. So this round rebases onto C1b-0's main and joins, rather than opening a second interval after the batch. The round's change is mechanical: the same hand-written bytes, the outputs regenerated, and the receipt record made cumulative.

## The tests

**Security:**
- **The rule, four tests:**
  - the full-path authorization: ordinary and pnpm descendants; a nested package refused and its own row admitted; VCS segments above, at and below `realPath`; Cargo output under a dependency-tree root, under a first-party root (`target/node_modules/a`) and inside another package's `target`; the lookalikes `target` without a Cargo parent (`vendor/target/node_modules/a`) and a non-anchor `.opensip`; the root and member custody anchors; `Forbidden` outside a dependency tree;
  - the dependency-tree Cargo root;
  - the pruned capture's place;
  - `classify_path` still outermost.
- **The walk module, seven tests:**
  - the pruned opener's charge equals the model on three cases;
  - custody above the anchor only: a group-writable package is read, while a group-writable first-party directory refuses;
  - the opener's refusals: outside, VCS, the member's `.opensip`, and a symlinked component;
  - a manifest replaced before its open refuses `Changed`;
  - **the walk's evidence:** the first-party Cargo roots `""`, `a` and `b`, siblings' included, and the member roots copied. The walk's charge with retention equals `walk_snapshot`'s;
  - the Cargo marker observation: a regular file in a dependency tree only, with a symlink and a first-party marker refused;
  - `authorize_read` over the walk's evidence, charged exactly its cost.
- **The soundness controls:** every vector case walked natively, and the pruned openers, at the model's prediction.

**Host, one test:** a pruned capture is read once and reused, stays a leftover after the walk (which prunes the dependency tree), and is never inventoried. The session keeps the walk's evidence.

## Checks

Lane `evidence/c1c0-checks-r2/`. It took one lane hold at nice 10, with a private TMPDIR, on `caa71e2`. **`allPassed: true`.**
- **Host and security suites** (`--no-fail-fast`), base against candidate: equal failure sets, with no test flaky in isolation.
  - **Host:** 411 passed and 8 failed on the base, against 412 passed and the same 8 failed on the candidate: 1 new passing test.
  - **Security:** 1,187 passed and 14 failed on the base, against 1,198 passed and the same 14 failed on the candidate: 11 new passing tests.
  - These are the base's standing failures (`test-comparison.json`).
- **rustfmt:** every new and base-clean edited file is clean. `crates/security/src/lib.rs` is base-dirty and appended only.
- **Clippy:** warning-denied, all targets, host and security.
- **The focused tests:** walk 25, rule 12, census 7 and session 30 (1 ignored), all passing.
- **The model and vectors:**
  - the charge model `--check`;
  - the vector moves: only `opensip-anchors-root-and-member` moves (+1 object, +129 bytes), the openers are equal, the three `prunedOpeners` are exact, and the session predictions are equal.
- **The retention's cap evidence:** the r9 adopted subtotal plus the worst-case member copies is 776,740 / 6,218,464 / 2,539,929,154. That passes r9's 2× rule against 2^21 / 2^24 / 2^33 (`retention-cap-evidence.json`).
- **The census checks:**
  - the discovery census, the workspace ledger and the snapshot census `--check`s over the lead-readable cache;
  - the census closure: exactly `discovery_rule.rs` changed;
  - the cumulative receipt record (above; `receipt-specific.json`).
- **The rule checks:** FW-01, the environment exceptions, the operability source census and verify_design.
- **14 of 14 mutations caught** (`controls.json`):
  - the custody split;
  - a followed symlink;
  - the rule's VCS refusal;
  - six read-set weakenings;
  - four retention weakenings, the copied key caught by the model `--check`;
  - a second pruned read.

## Not delivered

- **The read set itself** (C1c-1): the layout-driven walk, the extent binding (LD-C1C-12), the chosen authorizations, sealing's step-2 guard and the read-set model term.
- **The layout** (C2b).
- **The blind refreshes:** C1a4's run is a separate, earlier unit; C1c-0's receipts refresh in the interval LD-C1C-9 assigns.

## Not claimed

- No caller, no read set, no qualification. C1c is not claimed complete.

## Inventory

One new path, `crates/security/src/snapshot_read_set.rs`. Its additive inventory successor follows integration.
