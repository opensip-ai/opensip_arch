# Component installation implementation plan r3: the profile codec, the store and installer, the retained-tree capability, and the command (law CI r5)

**Lead plan, 2026-10-17. Proposed; it needs Codex review.** Round 3 answers `codex-component-install-plan-r2` (REQUIRED-FINDINGS: CIPLAN-R2-RF-1; LC-1 confirmed, LC-2 incomplete for RF-1's reason). Round 2 answered `codex-component-install-plan-r1` (REQUIRED-FINDINGS: CIPLAN-R1-RF-1 and RF-2, NBO-1 and NBO-2, with rulings on Q1 and Q2). r1 (`PLAN-r1.md`) and r2 (`PLAN-r2.md`) are history. It implements the accepted law "component release installation and tree custody" (`component-install/PROPOSAL.md`, which is r5 under its acceptance note). The law was accepted by Codex in `codex-component-install-r5` after rounds 1 to 4, and published at ARCH `4088af76`. It also carries that review's three NBOs (LD-CIP-4 to LD-CIP-6).

**The amendment this plan proposes (r3, CI-A1; LD-CIP-12).** The lead approved r2's LC-1 and the corrected LC-2 as **one narrow law amendment, CI-A1**, proposed for acceptance with this plan in the LD-D3A-17 shape. LD-CIP-12 quotes each current LAW sentence and row, and gives its replacement:
- **CI-A1-a (was LC-1):** P-3 returns an opaque receipt witnessing that one barrier on that exact handle, not a `FileBarrierReceipt`.
- **CI-A1-b (was LC-2, corrected by CIPLAN-R2-RF-1):** `B_install` step 4 gains the ordering rows: **two** owned `u32` index buffers (objects 2, bytes `2·n·size_of::<u32>()`, checked), and at most `n·⌈log₂ n⌉` charged comparisons.
- **CI-A1-c:** step 4's "deepest first" is stated as what LAW intends: a **branch-local, descendant-before-parent** post-order, not a global depth order.

CI-A1 is accepted only with this plan, and **accepting this plan accepts CI-A1**. Until then LAW stands as written, and CI-2's step-4 code waits for the acceptance. **P-6 needs no amendment:** LD-CIP-11 makes its implementation exactly the law's one charged `flock` edge (confirmed in `codex-component-install-plan-r2`, item 1).

## r3 changes (round 3, answering `codex-component-install-plan-r2`)

| Finding | Change | Where |
| --- | --- | --- |
| **R2-RF-1** (the merge sort's scratch index) | The selected bottom-up merge sort is priced **in full**, as C2a r4 R3-RF-2 prices it (`c2a/PLAN-r4.md`:172-175): **two `u32` index buffers**, the source and its merge destination, at objects 2 and bytes `2·n·size_of::<u32>()`, plus one edge before each comparison, at most `n·⌈log₂ n⌉`. Every product and sum is checked; overflow is the `install-budget` refusal. **The complete ordering bound is in `B_install`, before acquisition**, and each buffer's allocation is charged immediately before it is made. CI-T22 and a new CI-PT-7 count every ordering allocation and comparison independently, and show refusal before an unfunded scratch allocation or comparison. New mutations catch a missing scratch charge. | LD-CIP-4 (r3); LD-CIP-12 (CI-A1-b); CI-T22; CI-PT-7; §5 |
| **Lead disposition of LC-1 and LC-2** | Both are approved as the narrow law amendment **CI-A1**, with LC-2 corrected as above, and the branch-local, descendant-before-parent finalization interpretation explicit (CI-A1-c, which Codex asked to keep). | header; LD-CIP-12; §7 |
| **Bases** | Rebased to product main `72e07879` and architecture `0b84657f`. Since `3742822e` the product has two commits. C1a4-blind's record (`0772eb7`) changed only the four committed census receipt files. D3a-1 (`72e07879`) changed `crates/components/*`, `crates/platform/src/{lib, process, process_tests}.rs` and `Cargo.lock`. `tools/security/` is unchanged, and no changed file is in `CLOSURE`, `snapshotSources` or `ANCHORED` (`snapshot_seal.rs`, `identity/src/{canonical, descriptors}.rs`, `custody/discovery_scan.rs`), so LD-CIP-8's sets are unchanged. The `lib.rs` change adds process readiness exports beside the module list that CI-2's `component_tree` declaration joins. C1a4-blind's refreshed receipts are now the current accepted baseline. | Bases; LD-CIP-8 |

## r2 changes (round 2, answering `codex-component-install-plan-r1`)

| Finding | Change | Where |
| --- | --- | --- |
| **RF-1** (P-6's call sequence) | `FileLock`'s full sequence is four native calls. `try_acquire` delegates to `try_acquire_retaining`, which makes three: `file.metadata()` (an `fstat`), `fcntl(F_GETFD)` and `flock(… \| LOCK_NB)` (`locks.rs`:43-94). Its release, explicit or on drop, makes a fourth: `flock(LOCK_UN)` (`locks.rs`:100-123). LAW prices P-6 at one edge. So P-6 is **its own one-attempt native lock in `component_tree.rs`** (LD-CIP-11), over the `pin.lock` handle that P-4's no-follow `openat` produced. That open always passes `O_CLOEXEC`, and `fopen` has already kind-checked it, so close-on-exec and regular-file kind hold **by construction**. P-6 makes exactly one `flock(LOCK_SH \| LOCK_NB)`, or `LOCK_EX \| LOCK_NB` for GC's probe: one edge, as LAW prices it. Busy returns the handle; there is no retry. Release is the descriptor's close when the capability drops, which FS's convention leaves uncounted (`filesystem/directory_publication.rs`:60-61: "descriptor closes … are not counted"). There is no `LOCK_UN` call, and the descriptor is never duplicated, so the close releases the lock. CI-PT-5 checks the call log. | LD-CIP-1, LD-CIP-11; CI-PT-5 |
| **RF-2** (P-3's receipt) | P-3 returns a **new opaque `StandaloneBarrierReceipt<'file>`**, produced only by `component_tree::barrier_file(&File, &mut WorkScope)`. It witnesses only that one barrier completed on that exact handle (`is_for` by handle-object identity), with no byte or read-back claim. V1's byte verification stays with V1. The existing `FileBarrierReceipt` and `file_effects.rs` are unchanged. There is no caller-asserted constructor, and the whole-buffer writer is never a substitute. Matching law correction LC-1, now CI-A1-a (r3). CI-PT-6 covers handle binding and barrier failure. | LD-CIP-10; CI-PT-6 |
| **NBO-1** (post-order) | The finalization walk is a **manifest-driven depth-first post-order with a retained current-branch stack**. Each directory is entered once, and finalized after all its descendants. The auxiliary order is priced (LC-2; r3: corrected and amended as CI-A1-b). CI-T22 gains mixed-depth sibling branches, and asserts no re-entry and no `readdir`. | LD-CIP-4 (r2); CI-T22 |
| **NBO-2** (the stop rule) | The stop-and-re-plan rule covers **any change to any bound input of either receipt**. For the discovery receipt that means `CLOSURE`, its tools, its reference-loading sources, the member model, and the caps and sizes. For the companion receipt it means its tools, `snapshotSources` and `ANCHORED`. `--check` results are kept distinct from public binding-freshness evidence, and freshness uses a current accepted baseline. | LD-CIP-8; CI-PT-4 |
| **Q1 ruling** | CI-2 and CI-3 are **one package, one lane and one review**, with separate control ownership. CI-1 lands first. An early partial commit is never presented as CI-2's acceptance. | §2 |
| **Q2 ruling** | macOS-first. Unimplemented targets **fail closed** through the existing typed `LaunchError::PlatformUnsupported`-style unsupported-platform route, with no silent barrier or access-mode fallback. Linux enablement needs its own native controls. The law's platform table is unchanged. | LD-CIP-6 |

**Bases (r3):** product main `72e07879`, and architecture `0b84657f` together with the files the subject manifest names.

**Short names** are as in the law. In addition:
- **LAW** is `component-install/PROPOSAL.md`. Its items and controls are cited as LAW item n and CI-Tn.
- **C2a** is the C2a plan r4 (`snapshot-plan-c/c2a/PLAN-r4.md`).

## 1. What exists, and what is missing

**What exists on main:**
- **The trust owner's ordinary reader**, which joins a validated manifest to its catalog release, envelope and preimage (`crates/security/src/trust_ordinary_metadata.rs`:90-160).
- **The manifest and catalog shapes:** CM (`component_manifest.rs`, with its generated shape) and RC (`trust/recovery_catalog.rs`).
- **Custody:** security's `admit_custody_directory` (`snapshot_source.rs`:444), which charges `descriptor_acl_capture_cost()`.
- **The platform's staging and publication primitives:** `create_private_directory_stage_accounted`, `publish_exclusive_reserved` and their law-467 route classes (`filesystem/directory_publication.rs`). Also the exclusive creates (`file_effects.rs`:24, `directory_effects.rs`:49), the directory barriers (`directory_effects.rs`:28, :103-112), and `WorkLedger::effect` and `ReservedPostchecks` (`work_ledger.rs`:388-400).
- **The snapshot read discipline** (`crates/host/src/snapshot.rs`:33-70), and D3a-0's descent recipe (`crates/platform/src/process.rs` `descend_cost`, `READ_COST`).
- **`FileLock`** with shared and exclusive modes (`crates/platform/src/locks.rs`).
- **`RetainedDirectory::as_file`** (`filesystem.rs`:340), the public descriptor access that `custody_entry.rs` builds on.
- **The lifecycle crate**, with `leases.rs`, `locations.rs`, `selection.rs` and `lineage.rs`. Its planned inventory rows include `installation.rs` ("Stage and publish authorized immutable component generations.") and `catalog.rs`.
- **The pinned archive profile:** PKG-AP, in `component-packaging-contract.v14.json` at its pinned SHA-256.

**What is missing:**
- the profile-1 codec;
- the component store and the installer transaction;
- platform primitives P-1 to P-7 (LAW item 4);
- the retained-tree capability and its transfer;
- lifecycle's dependency edge to security, which the O1-a package policy permits;
- the fixture store;
- the command surface;
- the controls.

## 2. The split

| Sub-unit | Delivers | Depends on |
| --- | --- | --- |
| **CI-1** | **The profile-1 codec**, pure and fed hostile input: a new `crates/security/src/archive_profile.rs`. It provides PKG-AP admission as a streaming verifier: headers are recomputed from TreeCommitment rows and compared octet for octet; the member/entry bijection, `archiveLength` and every capacity are checked (LAW item 3). It also provides PKG-AP's byte-algorithm emitter, **for fixtures only**, under the joint fixture predicate. No allocation is proportional to the archive. Headers are parsed inside the caller's read buffer. | nothing |
| **CI-2** | **The store and the installer.** It realizes the planned row `crates/lifecycle/src/installation.rs` and the transaction (LAW item 4, steps 1 to 6), with V1, V2, the funded suffix, the outcomes and LD-CI-12. It adds the store location to `crates/lifecycle/src/locations.rs`. It provides platform primitives **P-1 to P-6** in a new platform module, `crates/platform/src/component_tree.rs`, declared in `lib.rs` as `custody_entry.rs` is (LD-CIP-1). **P-7** is an equal published status price in that module (LD-CIP-2). Lifecycle's manifest gains `opensip-security`. | CI-1; C2a-1's `trust::admitted_components` bridge and `ClosureCandidate` |
| **CI-3** | **The retained-tree capability** (LAW item 6): `open_retained_tree`, `RetainedTree` (holding the retained generation, `tree/` and `pin.lock` handles and the buffer), `transfer`, and the typed `TreeReadFailure`. It also provides the pin (LAW item 7) and `ComponentStore::fixture` under the joint fixture predicate. It lives in a new `crates/lifecycle/src/retained_tree.rs`. **C2a-3 binds CI-3** (C2a §2). | CI-2 |
| **CI-4** | **The command surface** (LAW item 4's handoff; item 8's terminations). J1 exposes `install` with the operator-supplied archive file, under WS's command inventory. It maps every LAW item 8 row to its schema-valid termination, carrier and remedy (CI-T16). | CI-2; J1 |

**Order.** CI-1 first. Then **CI-2 and CI-3 as one package, one lane and one review** (r2, the Q1 ruling), with separate control ownership. CI-3's capability needs CI-2's generations, and CI-2's re-install no-op needs CI-3's reader. Separate implementation commits are possible, but an early partial commit is never presented as CI-2's acceptance. C2a-2's generator gains profile-1 archive emission through CI-1's emitter, so its synthetic releases install through CI-2. Then C2a-3 binds CI-3. CI-4 lands with J1.

## 3. Lead decisions

- **LD-CIP-1. The platform primitives live outside the census closure.** P-1 to P-6 go in a new top-level platform module, `component_tree.rs`, declared in `crates/platform/src/lib.rs` with `#[allow(unsafe_code)]`, as `custody_entry.rs` is (lib.rs:62-63). They are built on public filesystem API only: `RetainedDirectory::as_file` and `File`, with their own native calls:
  - **P-1:** a positioned chunk write (`pwrite`), one charged attempt per chunk, never retried;
  - **P-2:** `fchmod`;
  - **P-3:** the file barrier (`F_FULLFSYNC` on macOS, with no fallback; Linux fails closed until enabled, per Q2), returning `StandaloneBarrierReceipt` (LD-CIP-10, r2);
  - **P-4:** `symlinkat`, `readlinkat` and the no-follow `openat` for reading;
  - **P-5:** the no-follow regular open of the operator path;
  - **P-6:** its own one-attempt native `flock`, shared or exclusive non-blocking, over the admitted close-on-exec `pin.lock` handle (LD-CIP-11, r2). It is not a wrapper over `FileLock`, whose acquisition makes three calls.

  Each primitive publishes its price as the law states it: one edge per native call, plus copies as owned records. **Rationale:** the discovery census closure pins `filesystem.rs`, `filesystem/{descriptor_acl_capture, descriptor_filesystem, directory_entries, directory_open, path_binding}.rs`, `work_ledger.rs` and `work_reader.rs` (`tools/security/discovery_census.py`'s `CLOSURE`). A primitive placed in any of them would make the discovery receipt stale for no semantic reason.
- **LD-CIP-2. P-7 is an equal published price, not an exposure.** `path_binding.rs`'s `status_read_cost()` is `pub(super)` and in the closure. `component_tree.rs` therefore publishes `status_read_cost()` with **the identical expression**: one edge, and bytes equal to the larger of `size_of::<libc::stat>()` and `size_of::<std::fs::Metadata>()` (`path_binding.rs`:118-126). A source-pin control (CI-PT-1, §4) reads both definitions and asserts that their expressions are byte-identical. LAW item 4 permits this ("or of an equal published price"), and no closure file changes.
- **LD-CIP-3. The fixture predicate in lifecycle.** `ComponentStore::fixture` and CI-1's emitter are under exactly `cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))` (MC item 8). Lifecycle gains the two features, forwarding to `opensip-security/crash-matrix` and `opensip-security/scenario-fixtures`, never default. A release-build source pin (CI-T11) shows that neither is reachable.
- **LD-CIP-4. The finalization walk's source (`codex-component-install-r5` NBO-1; r2, plan NBO-1).** LAW item 4's step-4 walk is **a manifest-driven, branch-contiguous depth-first post-order over the borrowed authenticated TreeCommitment**, not a fresh filesystem enumeration, and not a global depth sort:
  - **The order (r3, R2-RF-1).** The `n` row indices are sorted once by path component sequence (component-wise byte comparison), with the C2a r4 R3-RF-2 recipe: a deterministic **bottom-up merge sort over `u32` indices** (`c2a/PLAN-r4.md`:172-175). Component order groups each directory's descendants contiguously after it. Its price is complete:
    - **two index buffers**, the source index and the merge destination that each pass writes into (the passes alternate between them). Each is `Vec::<u32>::with_capacity(n)`, exact, and is charged at objects 1 and bytes `n·size_of::<u32>()` **immediately before it is allocated**: objects 2 and bytes `2·n·size_of::<u32>()` in all. The products are checked. `n ≤ 100,000` (LAW :100), so every index fits a `u32`;
    - **one edge immediately before each comparison**, through the comparator's fallible charge, so `Budget` propagates out of the sort. The worst case is at most `n·⌈log₂ n⌉` comparisons, which is the bound's row; `⌈log₂ n⌉` is computed exactly in integers, and is 0 for `n = 1`;
    - nothing else is allocated. The walk reads whichever buffer the last pass wrote; the other is dropped, uncharged, as releases are.

    **These rows are in `B_install` before acquisition** (CI-A1-b), computed with checked arithmetic, so an overflow or excess is the `install-budget` refusal before any byte is read. With `B_install` admitted, an in-operation `Budget` failure can occur only on a shared ledger, and is LAW item 8's in-operation budget route, as for every other row.
  - **The walk.** The walk reads the index forward, keeping a **retained current-branch stack** of directory handles. Entering a directory pushes its `desc`, and it is entered **exactly once**. When the next row is not inside the top directory, the top is finalized, with its `fchmod` then its barrier, and popped. Files are opened by `fopen` from the top handle, finalized, and closed. After the last row the remaining stack is finalized, with `tree/` last.
  - **No `readdir` call** is made. The structure was checked at V1 and is re-checked at V2.

  So step 4's work is LAW's `B_install` step-4 rows plus CI-A1-b's two ordering rows. CI-T22's call log must show no `readdir` and no re-entry of a directory, including over mixed-depth sibling branches, and CI-PT-7 accounts for the ordering (§4).
  - **The interpretation (CI-A1-c).** LAW's "bottom-up" and "deepest first" mean **branch-local, descendant before parent**: each directory is finalized after every entry beneath it, and before its parent. Files and directories of different branches interleave in the walk. A directory in one branch may be finalized before a deeper directory in a later branch. No global depth order is used or needed, because a barrier covers only its own directory's entries and modes.
- **LD-CIP-5. Record length `R` (NBO-2).** `R` is the exact canonical-JSON length of `generation.json`'s closed record (LAW item 5): `{archiveDigest, archiveProfileId, catalogRelease: {envelopeDigest, manifestDigest, stableId, version}, closureId, componentManifestDigest, platform}`, with keys in canonical order.
  - **When.** It is computed before acquisition from the authenticated values: `closureId` from C2a-1, and the others from the ordinary reader's release, manifest and artifact row.
  - **How.** CI-2 computes it with a hand length function in the style of C1a3's sealing encoders (`snapshot_seal.rs` `string_len`/`decimal_len`), applying the identity crate's canonical escaping and UTF-8 rules. A control checks it against `opensip_identity::canonical_bytes(..).len()` on every fixture.
  - **The encoder.** The bytes are hand-encoded into one buffer reserved at exactly `R` (the C2a r4 R3-RF-1 lesson: no `canonical_bytes` temporaries).
- **LD-CIP-6. The finalization handle's access mode is selected before the charged open (NBO-3).** For P-2 and P-3 in step 4, CI-2 selects one access mode per supported platform at build time: read-only or read-write, no-follow. It records the choice in a platform table, and qualifies it by a control on each S8 platform it supports (macOS here; LD-D3A-1's macOS-first).
  - **No retry.** CI-2 never tries one mode, fails, and reopens in another: that would add unfunded calls, and break the failure latch and the no-retry rule.
  - **Price.** The `fopen` price is the same for both modes.
  - **Failure.** If the selected mode fails on a supported platform, that is an I/O failure (`EXTENSION.INSTALL_IO_FAILED`), not a retry.
  - **Unimplemented targets (r2, the Q2 ruling).** Only macOS is implemented and qualified. Every other target fails closed, through the existing typed unsupported-platform route, before any native call. There is no silent barrier or access-mode fallback. Enabling Linux needs its own native access-mode, barrier and custody controls, and the law's platform table is unchanged.
- **LD-CIP-7. The bridge to trust evidence.** CI-2 and CI-3 take the ordinary reader's evidence through C2a-1's `trust::admitted_components` bridge (C2a §2). Its `AdmittedRelease` value is the release row, the retained manifest body and the selected-platform TreeCommitment, all borrowed. CI adds no second trust interface. If C2a-1 lands later than CI-1, CI-2 waits for it.
- **LD-CIP-8. The census and receipt impact, per receipt** (the C1b plan r3 rules: generated-output checks pass after any re-pin; stale receipts are recorded separately from public fields):

  | Sub-unit | Discovery receipt | Companion snapshot receipt |
  |---|---|---|
  | CI-1 | unchanged: a new security file, not in `CLOSURE` | unchanged |
  | CI-2 | unchanged: new files in lifecycle and platform `component_tree.rs`, plus edits to `lib.rs`, lifecycle's `locations.rs` and its `Cargo.toml`, none of them in `CLOSURE` (LD-CIP-1, -2) | unchanged: CI-2 reuses `WorkLedger::snapshot_profile()` by call, and does not edit `work_ledger.rs` or any snapshot model source |
  | CI-3 | unchanged | unchanged |
  | CI-4 | unchanged: host command files | unchanged |

  **The receipts' bound sources at this plan's base** (`72e07879`; unchanged from `3742822e`, since `tools/security/` and every bound file are unchanged, and C1a4-blind's refreshed receipts at `0772eb7` are the current accepted baseline):
  - **The discovery receipt** binds `discovery_census.py`'s `CLOSURE`, through `receipt_bindings`.
  - **The companion snapshot receipt** binds the discovery bindings, plus its four tools, plus `snapshotSources` (`snapshot_ledger_census.py` `sources()`). Those are `crates/host/src/{candidate_custody, snapshot, snapshot_tests, snapshot_seal}.rs`, `crates/platform/src/{custody_entry, work_ledger}.rs`, `crates/platform/src/filesystem/file_effects.rs`, `crates/security/src/{private_access, snapshot_source, snapshot_walk}.rs`, and the identity bound and encoding sources the tool anchors (`ANCHORED`).

  **So CI must not edit any of them.** In particular, P-1 to P-6 go in the new `component_tree.rs`, **not** in `custody_entry.rs` or `file_effects.rs`, and CI calls `admit_custody_directory` without editing `snapshot_source.rs` or `private_access.rs`.

  **Every sub-unit's lane asserts its "unchanged" claim:** the census-closure check finds no closure file changed, and both census `--check`s pass with their receipts byte-equal to base. **If an implementation needs to change any bound input of either receipt** (r2, NBO-2), that sub-unit stops and is re-planned into a census batch, joining one before its freeze or opening its own interval, with receipt-specific deltas. The bound inputs are:
  - **for the discovery receipt:** everything `receipt_bindings` binds: `CLOSURE`, the tools, the reference-loading sources, the member model, and the caps and sizes;
  - **for the companion receipt:** everything `bindings()` binds: the discovery bindings, the four tools, `snapshotSources` and the `ANCHORED` sources.

  The lane computes the changed-file set against both of these sets from the receipts' own binding code, not from a hand list. **Passing `--check`s and byte-equal receipt files are evidence of regenerated output, not of freshness.** Where freshness is needed, it is judged against a current accepted baseline's public binding fields.
- **LD-CIP-10. P-3's receipt (r2, RF-2).** `component_tree::barrier_file(file: &File, work: &mut WorkScope) -> Result<StandaloneBarrierReceipt<'_>, WorkFailure<io::Error>>`:
  - it charges one edge first, then makes `fcntl(F_FULLFSYNC)` once on macOS, with no fallback and no retry;
  - on success it returns a receipt bound to that exact `File` object (`is_for(&File)` by pointer identity, as `FileBarrierReceipt::is_for`);
  - the receipt has private fields and no public constructor, and it claims nothing about bytes or read-back. V1 owns byte verification.
  The existing `FileBarrierReceipt` and `write_new_regular_accounted` are unchanged and unused by CI-2's streaming path. Unsupported targets refuse with the typed unsupported-platform error before any call (Q2 ruling). Matching law correction LC-1.
- **LD-CIP-11. P-6, one native call (r2, RF-1).** `component_tree::PinLock` is acquired by `try_pin(file: File, mode, work)`:
  - it charges one edge, then makes exactly one `flock(fd, LOCK_SH | LOCK_NB)`, or `LOCK_EX | LOCK_NB` for GC's probe;
  - `EWOULDBLOCK` or `EAGAIN` hands the `File` back as busy, with no retry; any other error is `Io`;
  - the guard owns the descriptor, never duplicates it, and releases the lock **by closing it on drop**, an uncounted descriptor close under FS's convention, with no `LOCK_UN`.

  **Its preconditions hold by construction:** `file` must come from P-4's `fopen`, which opens with `O_NOFOLLOW | O_CLOEXEC` and has already kind-checked it, and `try_pin` accepts only that module's opened-file type, not a bare `File`. So no `fstat` or `fcntl(F_GETFD)` is repeated. `FileLock` is not used for pins.
- **LD-CIP-9. The X-CI-1 gate.** The installer's interim ledger is `WorkLedger::snapshot_profile()` (LAW item 4; accepted interim in `codex-component-install-r2` Q9). X-CI-1's owner is the lead, as DR-103's delivery owner. **The gate:** before any first-party component release is qualified, or before CI-4's command is enabled for production use, whichever comes first, a sourced installation profile replaces the interim. It is derived by the r9 2× rule over a census of the first-party releases' `B_install` values, or by an explicit law revision.
  - **Its census impact.** The sourced profile needs a new `WorkLedger` constructor, which edits `work_ledger.rs`. That file is in the discovery `CLOSURE` and among the companion snapshot receipt's pins. **So X-CI-1's resolution changes both receipts.** It must be sequenced into a reviewed census batch, before that batch's freeze or with its own interval, with a fresh baseline, a pre-run review, the frozen-input blind refresh and a post-run review.
  - **The plan names this unit X-CI-1-a.** It is not part of CI-1 to CI-4.

- **LD-CIP-12. The law amendment CI-A1 (r3), proposed for acceptance with this plan.** LAW (`component-install/PROPOSAL.md`, r5 under its acceptance note) prices one `FileBarrierReceipt` that the plan cannot construct, and no ordering work for step 4's post-order. The amendment is narrow: it changes the two `B_install` rows and two sentences below, and no other rule. P-6, the handle discipline, the routes and every other price are unchanged. It is accepted only with this plan; until then those sentences stand as written.
  - **CI-A1-a, P-3's return type** (LAW item 4, :218). Current: "returning a `FileBarrierReceipt`." Replacement: "returning an opaque receipt that witnesses that one completed barrier on that exact handle, by handle identity, and claims no bytes." The rest of the P-3 bullet is unchanged.
  - **CI-A1-b, `B_install` step 4's ordering** (:170). Current row: "| 4 | finalization traversal, bottom-up: descent into `tree/` from the stage, then into every dir row | 1 + `D` | `desc(4)`, `desc(len(name))` |". Replacement: two rows inserted before it, and the row itself reworded:

    | Step | Operation | Count | Price |
    |---|---|---|---|
    | 4 | the finalization order: two owned `u32` index buffers over the TreeCommitment's `n` rows, each charged before it is allocated | 2 | objects 1 and bytes `n·size_of::<u32>()` each; objects 2 and bytes `2·n·size_of::<u32>()` in all, checked |
    | 4 | the order's deterministic bottom-up merge sort by path component sequence: one edge before each comparison | at most `n·⌈log₂ n⌉` | one edge each |
    | 4 | finalization traversal, a branch-local post-order (descendant before parent): descent into `tree/` from the stage, then into every dir row, each entered once | 1 + `D` | `desc(4)`, `desc(len(name))` |

  - **CI-A1-c, the finalization order** (:239, :243, :174). Current (:239): "Bottom-up, in a post-order traversal of `tree/` that reopens each entry by no-follow descent from the stage, following the handle discipline:". Replacement: "Bottom-up, in a branch-local post-order traversal of `tree/`, ordered by the step-4 index (`B_install`), that reopens each entry by no-follow descent from the stage, following the handle discipline. Each directory is entered once, and is finalized after every entry beneath it and before its parent; entries of different branches may interleave, and no global depth order is required:". Current (:243): "each **directory** inside `tree/`, deepest first, then `tree/` itself:". Replacement: "each **directory** inside `tree/`, after every entry beneath it (descendant before parent), then `tree/` itself:". Current row (:174): "| 4.4 | each dir row, deepest first, then `tree/`: …". Replacement: "| 4.4 | each dir row, after every entry beneath it, then `tree/`: …", with the rest of the row unchanged.
  - **Aligned here:** LD-CIP-4's order and walk, LD-CIP-10's receipt, CI-T18's and CI-T22's controls, CI-PT-6 and CI-PT-7, and §5's mutations.

## 4. Controls, mapped to sub-units

| Control (LAW) | Sub-unit | Notes |
|---|---|---|
| CI-T1, CI-T2, CI-T5 | CI-1 | PKG-AP's exact 15 cases, as codec outcomes. The size-max and mode-field cases are labelled metadata-only. A length mismatch refuses before any write. Capacity refusals happen before any read. |
| CI-T3, CI-T4, CI-T6 | CI-2 | digest, profile and digest-split refusals; the platform-token lookup; `archive-changed` and `archive-read-attempts` |
| CI-T7, CI-T8, CI-T9 | CI-2 (CI-T9's read side is CI-3's) | nothing installed at every step 1-5 failure point; re-install no-op and corrupt refusal; immutability |
| CI-T10, CI-T11, CI-T12 | CI-3 | every typed failure, and exact charges; the fixture store and its release pin; revocation |
| CI-T13 | CI-1, CI-2, CI-3 | source pins: no socket, URL or spawn |
| CI-T14, CI-T15 | CI-2, CI-3 | foreign ACL refuses `Custody`; the ephemeral path writes nothing |
| CI-T16 | CI-4 | every item 8 row's class, code, detail, carrier and remedy, on both paths |
| CI-T17 | CI-3 (CI-2's V1 and V2 for the stage side) | structure: extra, absent, type, link target, association |
| CI-T18 | CI-2 | modes, and bottom-up finalization in the branch-local, descendant-before-parent order (CI-A1-c) |
| CI-T19 | CI-2 | crash prefixes through the post-rename barrier, after each `fchmod` and each barrier |
| CI-T20, CI-T21 | CI-3 | pins and GC probes; transfer and its sink gating |
| CI-T22 | CI-2 (`B_install`), CI-3 (`B_open`, `B_transfer`) | independent call-log enumeration over the file-only, nested, metadata-heavy and pre-existing trees; root-level and nested transfers; the custody call chain; the handle discipline at 100,000 entries; **no `readdir` in step 4** (LD-CIP-4); and (r3) the step-4 ordering's two buffer allocations and every comparison, each enumerated independently and matched to CI-A1-b's rows inside `B_install` |
| CI-T23, CI-T24, CI-T25, CI-T26 | CI-2 | the layout; V1 and V2; `LostRace`; the funded suffix, with its split and routes |
| **CI-PT-1** (plan) | CI-2 | P-7's expression identical to `path_binding.rs`'s (LD-CIP-2) |
| **CI-PT-2** (plan) | CI-2 | `R` equals `canonical_bytes(..).len()` on every fixture, and the record is hand-encoded with no temporaries (LD-CIP-5) |
| **CI-PT-3** (plan) | CI-2 | the finalization access mode is selected per platform before the open; a failure is an I/O failure, never a reopen (LD-CIP-6) |
| **CI-PT-4** (plan, r2) | every sub-unit | the changed-file set misses every bound input of both receipts, computed from their own binding code; `--check` results are reported separately from freshness (LD-CIP-8) |
| **CI-PT-5** (plan, r2) | CI-3 (and GC's probe) | the call log of a pin acquisition is exactly one `flock`, funded before it runs; busy hands the handle back with no retry; release is the close alone, with no `LOCK_UN`; a bare `File` cannot be passed to `try_pin` (a compile-fail control) (LD-CIP-11) |
| **CI-PT-6** (plan, r2) | CI-2 | `StandaloneBarrierReceipt` is bound to its exact handle (`is_for` false for another handle to the same file); an injected barrier failure gives no receipt and no retry; the receipt type has no public constructor (a compile-fail control); and `write_new_regular_accounted` is never called on the streaming path (LD-CIP-10) |
| **CI-PT-7** (plan, r3) | CI-2 | the ordering's accounting (LD-CIP-4, CI-A1-b), counted independently of the ledger: exactly two `u32` buffer allocations of capacity `n`, each preceded by its charge (objects 1, bytes `n·size_of::<u32>()`), and one charge before each comparison, never more than `n·⌈log₂ n⌉`, over `n = 1`, a power of two, one above a power of two, and 100,000 rows; `B_install` includes both rows, and an overflowing product refuses `install-budget`; a test scope funded one unit short refuses **before** the scratch allocation, and another one short refuses **before** the next comparison, with neither made |

## 5. Mutations

Each must fail the controls:
- **CI-1:** a header compared only by its decoded fields; the alternate regular-file typeflag `0x00` accepted; the length checked after reading; a PAX or GNU extension accepted; a pad byte unchecked.
- **CI-2:**
  - a stage created outside the store, or under a subdirectory;
  - a final mode applied after its barrier;
  - V2 skipped;
  - `LostRace` followed by winner verification;
  - cleanup attempted after a failure;
  - the suffix not reserved, or the rename charged twice;
  - `B_install` checked after acquisition;
  - a write retried;
  - a symlink followed;
  - a handle held per entry;
  - `readdir` in step 4;
  - a directory re-entered in step 4 (a global depth sort instead of the branch-contiguous post-order);
  - (r3) the merge destination (scratch) buffer allocated uncharged, or charged after it is allocated; only one index buffer priced in `B_install`; a comparison made uncharged, or charged after it is made; the ordering rows left out of `B_install`; the products computed unchecked;
  - P-6 implemented over `FileLock` (extra uncharged calls), or a `LOCK_UN` added;
  - P-3's receipt constructed without a barrier, or `is_for` made inode-based;
  - the access mode retried after a failure.
- **CI-3:** a missing `pin.lock` recreated; `generation.json` trusted as authority; an extra entry ignored; a transfer opening `tree/<path>` in one `openat`; a sink committed before verification; an ephemeral read creating a pin; the fixture store reachable without the predicate.
- **CI-4:** a corrupt tree routed as not installed; an ephemeral detail emitted; the in-operation budget routed as `install-budget`.

## 6. Checks

Each sub-unit's lane covers:
- the touched crates' suites at base and candidate: platform serially, as D3a-0's lane does;
- warning-denied all-targets Clippy, rustfmt and the focused tests;
- the release-build source pins;
- the environment exceptions and the operability source census with its mint audit;
- **the census-closure check, and both census `--check`s with byte-equal receipts** (CI-PT-4);
- verify_design;
- the package edges, where CI-2 adds the lifecycle→security edge;
- the mutations.

## 7. Open questions

- **Q1 (ruled):** one CI-2/CI-3 package and lane (§2).
- **Q2 (ruled):** macOS-first, with other targets failing closed (LD-CIP-6, LD-CIP-10).
- **LC-1 and LC-2 (disposed, r3):** the lead approved them as the narrow law amendment CI-A1, with LC-2 corrected by R2-RF-1 (LD-CIP-12). Accepting this plan accepts CI-A1.
- **No new question.**

## 8. Not delivered

- X-CI-1-a, the sourced installation profile (LD-CIP-9).
- C2a-3's binding (C2a's), and C2b-1.
- GC's inert-stage removal: the GC owner's (LAW item 7).
- Updates, migration, multi-platform installation and network acquisition (LAW's exclusions).

## 9. Not claimed

- No trust-owner change, and no new key, root or role. The only new features are lifecycle's forwarders of the existing fixture features (LD-CIP-3).
- No public code, no qualification, and no release.
