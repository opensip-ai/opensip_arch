# CI-2 + CI-3 r1: the component store, its installer, and the retained-tree capability (law CI r5 items 4 to 7)

**Unreviewed candidate, 2026-10-17. It needs Codex review.** It implements sub-units CI-2 and CI-3 of the component installation implementation plan r3 (`../PLAN-r3.md`, accepted by Codex `codex-component-install-plan-r3` with amendment CI-A1), as **one package, one lane and one review**, with separate control ownership (the Q1 ruling). The law is "component release installation and tree custody" (`../PROPOSAL.md`: r5 under its acceptance note, with CI-A1; r5's bytes are `../PROPOSAL-r5.md`). **This unit proposes law amendment CI-A2 (§4), in CI-A1's shape; accepting the unit accepts CI-A2, and a verdict of REQUIRED-FINDINGS against CI-A2 rejects both.** Until CI-A2 is accepted, LAW stands as written and this code is not conforming.

**Product base:** main at the lane's start, as `source.json` and `checks.json` record it (product `50f1ac1`, inventory v225, when drafted). **Worktree:** `/Users/sb/code/opensip-ai/opensip-ci2`. **Changed:** see `product-map.json`.

## 1. What changes

| File | Change |
| --- | --- |
| `crates/platform/src/component_tree.rs` (new) | P-1 to P-7 (LD-CIP-1, -2, -10, -11): the positioned chunk write, `fchmod`, the standalone file barrier and its opaque `StandaloneBarrierReceipt`, `symlinkat`/`readlinkat`, the no-follow regular open from a retained directory (`TreeFile`), the no-follow open of the operator's archive, a no-follow entry status read, the identity sample, and the one-call pin `try_pin`/`PinLock`. P-7 is `status_read_cost()`, the filesystem's identical expression. macOS only: every other target refuses before any charge or native call. |
| `crates/platform/src/component_tree_tests.rs` (new) | CI-PT-1, CI-PT-5, CI-PT-6 and each primitive's charge-before-call. |
| `crates/platform/src/lib.rs` | Appends `pub mod component_tree` under `#[allow(unsafe_code)]`, as `custody_entry` is declared. |
| `crates/lifecycle/src/installation.rs` (new) | The store (`ComponentStore`), the tree model borrowed from the validated manifest, the prices, the charged orderings and searches, the structural walk shared with CI-3, the generation record's hand encoder, `B_install`, and the transaction `install` (LAW item 4). Realizes the planned inventory row. |
| `crates/lifecycle/src/installation_tests.rs` (new) | CI-2's controls (§6). |
| `crates/lifecycle/src/retained_tree.rs` (new) | CI-3: `open_retained_tree`, `RetainedTree`, `transfer`, `VerifiedSink`, `TreeReadFailure`, `PinRequest`, `B_open` and `B_transfer` (LAW items 6 and 7). |
| `crates/lifecycle/src/retained_tree_tests.rs` (new) | CI-3's controls (§6). |
| `crates/lifecycle/src/lib.rs` | Declares the two public modules (macOS), names them in its header as the crate's public effect API, and carries law X9 r1 item 2's compile guard for its forwarded `crash-matrix` feature (platform's `no_manifest_enables_the_crash_matrix_feature` requires it). |
| `crates/lifecycle/src/locations.rs` | Gains `COMPONENT_STORE = "components"` (LAW item 5, LD-CI-7). |
| `crates/lifecycle/Cargo.toml` | Gains the `opensip-security` edge (O1-a permits it), the two fixture features forwarded to security's and never default, and a dev-dependency enabling `scenario-fixtures` for this crate's own tests (LD-CIP-3). |
| `Cargo.lock` | The one new internal edge. |
| `crates/security/src/component_closure.rs` | C2a-1's candidate types (with C2a-3k's `Retention`, which `ClosureRefusal` carries) and `component_candidate` become `pub` (LD-CI2-1). Nothing else changes; C2a-3k's kernel stays crate-private. |
| `crates/security/src/trust_admitted_components.rs` | `AuthenticatedComponent`'s accessors become `pub`; its constructor stays the trust owner's. `TestComponent` moves from `cfg(test)` to the joint fixture predicate and becomes `pub` (shared gate 7; LD-CI2-1). |
| `crates/security/src/trust.rs` | The bridge's re-exports become `pub`; `TestComponent`'s is under the joint predicate. |
| `crates/security/src/lib.rs` | Appends the public re-exports of C2a-1's bridge and candidate, `Retention` as `ClosureRetention` (base-dirty for rustfmt: append-only). |
| `crates/security/src/crash_matrix_sites.rs` | X9-1's pinned site list gains shared gates 7 (`TestComponent`: `trust_admitted_components.rs` 2 sites, one more each in `trust.rs` and `lib.rs`) and 8 (`ComponentStore::fixture` in lifecycle's `installation.rs`), by name, and lifecycle's compile guard. |

No census-bound file changes (§7).

## 2. Lead decisions recorded (LD-CI2-n)

The lead agreed these on 2026-10-17, on the implementer's recommendations:
- **LD-CI2-1. C2a-1's bridge, public.** The bridge and candidate were crate-private, and no production path reaches the bridge yet (C2a-4 will). Their items become `pub`, re-exported by appending to security's `lib.rs`; no second trust interface is added, and only the trust owner constructs an `AuthenticatedComponent`. `TestComponent` becomes shared fixture gate 7, by name.
- **LD-CI2-2. CI-T11's signed half waits for C2a-2.** C2a-2 does not exist on main, and its in-progress rows carry `archiveProfileId: "synthetic"`, which CI-2 must refuse (`Profile`). CI-2's fixtures use `TestComponent` (real body validation; the test's release row with a profile-1 artifact and the real archive digests). C2a-2 can use CI-1's fixture-only emitter in a follow-up so its signed releases install through the same code.
- **LD-CI2-3. The admission bound is a reservation.** `WorkLedger` has no remaining-allowance query, and `work_ledger.rs` is census-bound. So `install` reserves the bound with `WorkScope::effect(0, bound)` and runs the whole transaction inside `ReservedPostchecks::prepaid(bound)`: an excess at the reservation is `install-budget` before any acquisition, and every later charge draws from the credit, a shortfall there being law 468's in-operation route. The reserved bound is the componentwise maximum of `B_install` and the re-install path's bound (step 1's existence check and the store's custody, plus `B_open`), so the re-install path is funded too (CI-A2-e).
- **LD-CI2-4. `desc(k)`** is D3a-0's descent formula, `{3, 3, k + 1 + 4·LEVEL}`, over CI-2's own traversal level type (`installation.rs`'s `Level`); D3a-0's `descend_cost` and `Level` are private to `process.rs`. LAW says `LEVEL` is a compile-time property of the code.

## 3. Implementation decisions (ID-CI2-n)

- **ID-CI2-1. Nothing is copied from the evidence.** The tree is the validated manifest's selected-platform entries, read on demand (`Tree`); the only per-row allocations are the priced index buffers.
- **ID-CI2-2. Member order is a charged index (CI-A2-a).** CI-1's codec takes the rows in PKG-AP's member order by position (`ArchiveRows`). The manifest's entries are unordered, so step 2 sorts the row indices by path bytes with the two-buffer charged merge sort, at CI-A2-a's price.
- **ID-CI2-3. One component-order index serves V1, step 4 and V2** (CI-A1-b; CI-A2-f). It is computed once, at the start of step 3.
- **ID-CI2-4. Chunk writes are exactly `⌈len/64 KiB⌉` per file.** Bodies are written at 64 KiB file offsets, one P-1 attempt each. A chunk split across two archive reads stays at the start of the shared buffer until the next read completes it (no second buffer). Each archive read is one charged attempt within `env(L)`, and at most `L + 1` bytes are read; `archive-read-attempts` refuses before an unfunded attempt.
- **ID-CI2-5. The walk finds every row by its own status read, and lists each directory once, at its pop.** Each listing is charged `children + 3` before it is made; its entry count, excluding `.` and `..`, must equal the children found: any other is `Extra`. Names are unique, and every expected child was already found, so an equal count is an equal set. No name is collected and no `readdir` result names a row.
- **ID-CI2-6. The finalization walk** (step 4) is CI-A1-c's branch-local post-order on the same index: each file's final mode then its barrier; each directory's `0500` then its barrier at its pop; `tree/` last; then `generation.json`, `pin.lock` and the stage's barrier. The finalization open is read-only (LD-CIP-6): on macOS a read-only descriptor takes `fchmod` and `F_FULLFSYNC`; a failure is an I/O failure, never a reopen.
- **ID-CI2-7. Association is byte equality.** V2 and the open compare `generation.json`'s bytes with the owned expected record, hand-encoded at exactly `R`; no parse. C2a-1's Blobs are checked against the file rows at both ends: at installation, in one charged pass over the member order (both are in byte order; CI-A2-a's third row), so a candidate of the same body's other platform row stages nothing; at the open, by charged binary search in the component index (CI-A2-b). The manifest-digest binding alone would not catch that case: the candidate's digest is the body's, whichever platform row it projects.
- **ID-CI2-8. Test seams.** `installation.rs` carries `#[cfg(test)]` seams (a named-step hook and a read cap) for the failure-point, crash-prefix, tamper and lost-race controls. They are compiled into this crate's tests only; they name no feature, so they are not fixture sites.

## 4. Amendment CI-A2 (proposed with this unit)

LAW prices one index (CI-A1-b, step 4) but the implementation needs its orderings and lookups in four more places, one status read and one ACL append that LAW's rows omit. **CI-A2 is narrow: it adds rows and one sentence, changes no rule, and every new row uses CI-A1-b's recipe** (two `u32` index buffers, each charged before it is allocated, objects 2 and bytes `2·n·size_of::<u32>()`, checked; one edge before each comparison).
- **CI-A2-a, step 2's member order** (LAW :159, the lead's decision). Current row: "| 2 | archive read attempts | `env(L)` | `rd` each |". Replacement: two rows inserted before it:

  | Step | Operation | Count | Price |
  |---|---|---|---|
  | 2 | the member order: two owned `u32` index buffers over the TreeCommitment's `n` rows, each charged before it is allocated | 2 | objects 1 and bytes `n·size_of::<u32>()` each, checked |
  | 2 | the member order's deterministic bottom-up merge sort by the full path's UTF-8 bytes (PKG-AP's member order): one edge before each comparison | at most `n·⌈log₂ n⌉` | one edge each |
  | 2 | C2a-1's Blobs against the file rows, both in byte order: one comparison per file row, charged first (LAW item 6's association, at installation) | `F` | one edge each |

  And item 4 step 2 (:229): "For each member, verified against its row by item 3's codec as it streams:" becomes "For each member, matched to its row by the member order (step 2's index) and verified against it by item 3's codec as it streams:".
- **CI-A2-b, `B_open`'s index and association** (LAW :195). Current row: "| `tree/`: descent from the generation, **retained** as the capability's base (r5, RF-1) | 1 | `desc(4)` |". Replacement: that row, then three rows inserted after it:

  | Operation | Count | Price |
  |---|---|---|
  | the component-ordered index (CI-A1-b's order) over the `n` rows: two owned `u32` buffers, each charged before it is allocated, one **retained** by the capability | 2 | objects 1 and bytes `n·size_of::<u32>()` each, checked |
  | its merge sort: one edge before each comparison | at most `n·⌈log₂ n⌉` | one edge each |
  | the Blobs' association: one binary search per Blob in that index, one edge before each comparison | at most `F·(⌈log₂ n⌉ + 1)` | one edge each |

  The traversal walks that index (CI-A1-c's branch-local post-order, each directory entered once).
- **CI-A2-c, `B_transfer`'s lookup** (LAW :207). Current first row: "| descent along `f`'s parent chain, one component at a time, from the retained `tree/` handle (none for a root-level file, `k(f) = 1`) | `k(f) − 1` | `desc(len(seg_i))` each |". Replacement: one row inserted before it: "| `f`'s row, found by binary search in the capability's retained index | at most `⌈log₂ n⌉ + 1` | one edge each |".
- **CI-A2-d, `tree/`'s own mode.** LAW item 5 requires `tree/` itself at `0500`, and V2 and the open check every installed mode, but no row reads `tree/`'s status. Current V2 row (:178): "| 5 | V2: descent into `tree/` and every dir row, listing reads and per-entry status reads, as V1 | 1 + `D`; `n + 3·(D + 1)`; `n` | as V1 |". Replacement: that row, then "| 5 | V2: `tree/`'s own status in the stage (its installed mode) | 1 | `st` |". And `B_open` gains, after the `tree/` row, "| `tree/`'s own status in the generation | 1 | `st` |".
- **CI-A2-e, the funding** (LAW :122). Current: "Before any acquisition, the installer computes a **deterministic, conservative admission bound** `B_install`, and compares it with the ledger's remaining allowance." Replacement: "Before any acquisition, the installer computes a **deterministic, conservative admission bound**, the componentwise maximum of `B_install` and the re-install path's bound (step 1's existence check and the store's custody, then `B_open`), and reserves it on the ledger (`WorkLedger::effect` with `ReservedPostchecks::prepaid`), since the ledger exposes no allowance query; every later charge draws from that reservation." The next sentence's "If `B_install` exceeds the allowance" reads "If the bound exceeds the allowance". Nothing else changes: an excess is `install-budget` before any byte is read, and an in-operation shortfall is law 468's route.
- **CI-A2-g, the stage's ACL sentinel** (LAW :156). The custody rule (`admit_custody_directory`) refuses a directory with no ACL (`AclUnavailable`): every private directory carries one zero-rights owner allow. FS creates the stage with no ACL ("the zero-rights owner allow belongs to the security layer", `directory_publication.rs`:58-59), so the stage's custody check cannot pass as LAW's rows stand. Current row: "| 2 | the stage's custody | 1 | `cust` |". Replacement: one row inserted before it: "| 2 | the stage's ACL sentinel: one zero-rights owner allow appended to the stage (`append_owner_zero_allow_accounted`) | 1 | `append_owner_zero_allow_cost()` |". The generation inherits it by the rename; the store's is provisioning's.
- **CI-A2-f, CI-A1-b's index serves V1, step 4 and V2.** CI-A1-b's two step-4 ordering rows are charged once, at the start of step 3, and the same index orders V1, the finalization walk and V2. Their step label reads "3–5" instead of "4"; their counts and prices are unchanged.
- **Aligned here:** `install_bound`, `open_bound`, `transfer_bound`, and CI-T22's controls (§6).

## 5. Interfaces

- **Installer:** `install(store: &ComponentStore, component: &AuthenticatedComponent, candidate: &ClosureCandidate, platform: SelectedPlatform, archive: &Path, work: &mut WorkScope) -> Result<Installed, InstallFailure>`. The caller holds the lifecycle fence (CI-4 acquires it) and supplies the ledger (interim: `snapshot_profile()`, X-CI-1). `Installed::{Published, AlreadyInstalled}`. `InstallFailure::{Admission(AdmissionRefusal), Io(InstallIo), Budget, Corrupt(TreeReadFailure)}` map one to one onto LAW item 8's installation rows; CI-4 derives the terminations.
- **Store:** `ComponentStore::open_in(install_root, invoking_uid)` (no-follow `components/` under the admitted root); `ComponentStore::fixture(directory, uid)` under the joint predicate only.
- **Capability (what C2a-3 binds):** `open_retained_tree(store, component, candidate, platform, pin: PinRequest, work) -> Result<RetainedTree, TreeReadFailure>`; `RetainedTree::transfer(&mut self, path, sink: &mut impl VerifiedSink, work)`; `VerifiedSink::{begin(sha256, length), chunk(bytes), finish(verified)}`. `TreeReadFailure::{NotInstalled, Absent, Length, Digest, Type, Mode, LinkTarget, Extra, Association, Pin, Custody, Budget, Io}`. LAW item 6 names `AdmittedRelease`; here it is C2a-1's `AuthenticatedComponent` with the `SelectedPlatform` (LD-CIP-7). `transfer` takes `&mut self` because it uses the capability's one retained buffer.

## 6. Controls

CI-T1, CI-T2 and CI-T5 are CI-1's (accepted). This unit's, by owner:
- **CI-2 (`installation_tests.rs`):**
  - **CI-T3:** `artifact-digest-split`, a profile other than 1 (`"synthetic"`), and a wrong `archiveDigest` (refused at the stream's end; the stage stays inert).
  - **CI-T4:** platforms with no S8 row refuse; the alias appears only as the record's `platform`.
  - **CI-T6:** `archive-changed` (the archive's mtime changed at the `streamed` seam) and `archive-read-attempts` (reads capped at 4 KiB spend `env(L)`).
  - **CI-T2/CI-T5 at the installer:** a wrong-length archive and a 101-byte path refuse before anything is staged.
  - **CI-T7:** a failure at each of five step points publishes nothing and leaves exactly one inert stage, never cleaned.
  - **CI-T8:** re-install of a verifying generation is a no-op; of a corrupted one refuses `Corrupt(Digest)` and rewrites nothing.
  - **CI-T13:** source pins over `installation.rs`, `retained_tree.rs` and `component_tree.rs`.
  - **CI-T14:** a foreign ACL entry on the store refuses `Custody` before staging.
  - **CI-T18:** `0200` → `0400`, `0600` dir → `0500` traversed, `0100` → `0500`, `0750` → `0500`, symlinks untouched; staging `0700`/`0600` at V1 and final modes after step 4 (seams).
  - **CI-T19:** crash prefixes by seam: before the rename each restarts absent (`NotInstalled`); after it, the generation is present and verifies, and a later install is a no-op.
  - **Association at installation:** a candidate of the same body's `{macos, x86_64}` row refuses `Evidence` and stages nothing; the matching candidate installs.
  - **CI-T22 (B_install):** for file-only, nested and metadata-heavy trees, exactly one P-1 attempt per 64 KiB chunk is made (a test-only counter), and the bare transaction's actual charges are within `B_install`, and an independent enumeration in the test matches every object and byte exactly and every edge but comparisons and read attempts, which lie within their worst cases; `B_install`'s own fixed rows equal the enumeration exactly. The bound exceeded by one edge refuses `install-budget` before anything is staged; exactly the bound suffices. Ledgers short by one unit fail by law 468's route and publish nothing. The re-install path runs within its bound.
  - **CI-T23:** the stage is a store sibling; a failed act leaves it, and the open never returns it.
  - **CI-T24:** a nested tree installs; every byte, link, mode, the record's `0400` and `pin.lock`'s empty `0600` are as LAW requires.
  - **CI-T25:** a name created at the `prerequisites` seam gives `LostRace`: the act ends, the stage stays inert, the winner is untouched.
  - **CI-T26:** the reservation's arguments are pinned, and a ledger one edge short of the suffix refuses before the rename by law 468's route, with no cleanup.
  - **CI-PT-2:** the record's length and bytes are the identity crate's canonical encoding, including escapes. **CI-PT-3:** one read-only finalization access mode, no `ReadWrite`. **CI-PT-7:** the sort's two buffers and every comparison are charged first, at `n = 1, 2, 8, 9, 100,000`; one unit short refuses before the scratch buffer, and before the next comparison. `buffer_cost` equals SNAP's expression.
- **CI-3 (`retained_tree_tests.rs`):**
  - **CI-T10:** `NotInstalled` versus `Absent`; a short ledger is `Budget`; another platform's candidate fails `Association` before the generation is opened.
  - **CI-T9/CI-T17:** a modified, truncated, removed or symlink-replaced file refuses `Digest`, `Length`, `Absent` or `Type`; an extra file `Extra`; a removed empty directory `Absent`; a changed symlink target `LinkTarget`; a directory replaced by a file `Type`; a changed record `Association`; a changed mode `Mode`, including `tree/`'s own; another release's candidate `Association`.
  - **CI-T15:** an ephemeral open and transfer change no byte, entry or time in the store; a missing `pin.lock` fails `Pin` and is never recreated.
  - **CI-T20:** GC's exclusive probe is busy while a capability lives, and free after it drops; a non-empty or wrong-mode `pin.lock` fails `Pin`.
  - **CI-T21:** every file transfers exactly and commits only on `finish(true)`; a non-file path is `Association`; a file changed mid-transfer fails `Digest` and the sink commits nothing.
  - **CI-T22 (B_open, B_transfer):** the open's charges are within `B_open`, objects and bytes exactly; transfers of a root-level and a nested Blob are within `B_transfer`, with exactly `k − 1` descents.
  - **CI-T12:** by construction (only the trust owner constructs the evidence); revocation at R10a is the reader's, exercised with C2a-2's signed fixtures and C2a-4.
- **Platform (`component_tree_tests.rs`):** CI-PT-1 (P-7's expression), CI-PT-5 (one `flock`; busy hands back; release is the close; no `LOCK_UN`), CI-PT-6 (the receipt's exact handle; a failed barrier gives none), and each primitive's charge before its call.
- **Mutations (27; `evidence/ci2-r1-checks/controls.json`), each failing its crate's focused tests:** `scratch-buffer-uncharged`, `comparison-charged-after`, `member-order-rows-left-out`, `install-association-skipped`, `bound-checked-after-acquisition`, `rename-charged-twice`, `lost-race-as-success`, `v2-record-skipped`, `v2-pin-skipped`, `extra-entry-ignored`, `directory-reentry-byte-order`, `archive-digest-unchecked`, `chunk-written-twice`, `readdir-in-step-4`, `archive-read-envelope-unchecked`, `descent-uncharged`, `access-mode-retry-path`, `fixture-store-unpredicated`, `pin-file-recreated`, `record-trusted`, `association-skipped`, `sink-committed-unverified`, `generation-custody-skipped`, `symlink-followed`, `barrier-skipped`, `receipt-by-inode`, `pin-unlock-added`. They include plan r3 §5's CI-2 and CI-3 items, except two: a cleanup after a failure is excluded by construction (no code path removes a stage; CI-T7 asserts the stage remains), and a handle held per entry is unmeasured (no descriptor-count control).
- **Not exercised here, by design:** CI-T11's signed half (LD-CI2-2), CI-T16 (CI-4), the crashed-holder release of CI-T20 (the OS's `flock` semantics; the drop-release is tested), and an injected parent-barrier failure after a funded rename (the platform barrier has no seam; the `renamed` seam simulates a stop at that point); CI-T22's 100,000-entry handle-discipline case, which needs a descriptor-count or `RLIMIT_NOFILE` control that this crate cannot set without unsafe code. By construction, the code holds only the stage, `tree/`, one member's parent chain in step 2, and the current-branch stack elsewhere; CI-PT-7 runs the ordering at 100,000 rows.

## 6b. The lane

`evidence/ci2-r1-checks/` (`run_ci2_checks.py`), one lane hold, nice 10, private 0700 TMPDIR. Once the runner holds the lock it moves the worktree to main's head, but only when main descends from the worktree's base and changed no candidate path. **Attempt 6, at main `2ead5cf`, passed every row** (`checks.json`, `allPassed: true`):
- **Suites:** lifecycle 32 → 73 (41 new, exactly the two new test files'); platform 331 → 340, run serially (9 new, exactly `component_tree_tests.rs`'s); security 1281 → 1281. Failure sets are equal, the same 14 security base-environment failures on both sides, and suite counts are equal.
- **Static checks:**
  - warning-denied all-targets Clippy on the three crates;
  - the workspace all-targets check;
  - the `scenario-fixtures` and `crash-matrix` checks of security and lifecycle.
- **Symbol checks,** each against the exact rlib its build produced:
  - the release build defines `installation::install`, and neither `ComponentStore::fixture` nor `TestComponent::new`;
  - the fixture build defines both.
- **Repository checks:**
  - package edges under the O1-a policy (lifecycle → identity, platform, security);
  - rustfmt on the edited base-clean files, with security's `lib.rs` base-dirty and checked append-only;
  - the environment exceptions;
  - operability's source census with its mint audit (no findings);
  - `census-closure-unchanged`;
  - `receipt-inputs-unchanged` (23 discovery-bound and 37 companion-bound files, none changed; the four receipt files byte-equal to base);
  - verify_design.
- **Mutations:** all 27 caught, each failing its crate's focused tests (`controls.json`).

**Attempt history** (earlier attempts are kept at `/tmp/opensip-implementation/ci2-r1-checks-attempt{1,2,3,4,5}`):
1. **Attempt 1** stopped at the move-to-main step: main had gained D3a-3 (`2fbb779`), whose `Cargo.lock` change overlapped the candidate's one-line edge. The candidate was rebased (main's lock plus the same edge).
2. **Attempt 2** found five defects, all fixed:
   - warning-denied Clippy refused five `stat` field casts that are identities on macOS (now one local, commented `allow` for the portable casts);
   - platform's `no_manifest_enables_the_crash_matrix_feature` required law X9 r1 item 2's compile guard in lifecycle's `lib.rs` for its forwarded feature (added, and pinned in the site list);
   - the release/fixture symbol checks picked the newest rlib by time, not the build's own (now read from the build's JSON artifact messages);
   - three mutations survived:
     - `extra-entry-ignored`: the listing's entry limit still caught it, so the mutation now lifts the limit too;
     - `chunk-written-twice`: no control counted writes, so a test-only counter now asserts exactly one P-1 attempt per chunk;
     - `association-skipped`: no constructible input reached it, because the evidence check's manifest-digest binding refused first. The same body's other platform row is such an input, so the association now also runs at installation (CI-A2-a's third row), and both ends have controls.
3. **Attempt 3** stopped at the move-to-main step: C2a-3k (`274dccc`) had changed `component_closure.rs`. The candidate was rebased: main's file with the same visibility edits, plus `Retention`, which C2a-3k added to `ClosureRefusal`.
4. **Attempt 4**, at `274dccc`, passed:
   - the three suites (lifecycle 32 → 73, platform 331 → 340, security 1257 → 1257, with equal failure sets);
   - the workspace and all four feature checks;
   - the package edges, the environment exceptions, operability, both census checks and verify_design;
   - all 27 mutations.

   It found two defects, both fixed:
   - warning-denied Clippy refused a test-only `Evidence` field, a doc-list continuation and a complex test type;
   - the symbol checks matched only hashed `deps/` rlib names, but a requested package's rlib is uplifted without a hash.
5. **Attempt 5** stopped at the move-to-main step: C1b-1 (`ae141a3`) had appended to security's `lib.rs`. The candidate was rebased: main's `lib.rs` plus the same appended block.
6. **Attempt 6** is the packaged lane.

## 7. Census and receipts

No census-bound file changes: the new platform module is outside `CLOSURE` (LD-CIP-1), and the lifecycle and security files are in neither receipt's bound set. The lane's `receipt-inputs-unchanged` check (CI-PT-4) derives both sets from the receipts' own binding code and checks the changed-file set against them, and that the four receipt files are byte-equal to base. No census mode is run (they need the T2 cache).

## 8. Not delivered

- CI-4: the command, the fence acquisition and the terminations.
- X-CI-1-a: the sourced installation profile.
- GC's census and removal of inert stages.
- C2a-3's binding, and C2a-2's profile-1 signed fixtures.
