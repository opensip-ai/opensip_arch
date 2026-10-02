Grok review r1: X6b, read-only recovery's admission, `recover` and `RecoveredCommit`, and the host's recovery route (law X6 r3 items 1 to 6, 8 and item 12's X6b list), with X9 r1's `x6.recover` `after-lease` and `after-ledger-snapshot` points (item 5, gap G3), X7a's `ExistingAttempt` disclosure (X7 r5 item 10), and inventory v126 (parent v125). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-recovery-admission-x6b-r1. If you build or test, use a CARGO_TARGET_DIR under that directory, and run every test with a private TMPDIR: create a 0700 directory under `$(getconf DARWIN_USER_TEMP_DIR)` (for example `…/grok-x6b-tmp`), never the shared `/private/tmp/claude-501` tree, which other runs churn. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture. Toolchain: `PATH=/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin:$PATH`; Python is `python3.14`.

## The unit

X6 r3 item 12 defines X6b (security, storage and host):
- **Security:** `RequestedBinding`, `RecoveryRequest` and `RecoveryAdmission` (items 1 to 3: the read entry, 458c's walk without the fence, the registry and endpoint reads, X2 r8 item 7's fence-free SHARED-READ, the recheck), and the recovery-side carrier location constructor.
- **Storage:** `recover` and `RecoveredCommit` (items 4, 5 and 8), and `NotPrepared::ExistingAttempt`'s `requested` binding (item 6).
- **Host:** the read-entry route that admits a `RecoveryRequest`, calls `recover` and projects the result on item 8's rows.
- **X9 r1 points:** `after-lease` and `after-ledger-snapshot` in `x6.recover` (X6a placed the bracket points).

X6c (the sweep's settle write and `store-gc`) is not here. X8 r3 assigns X6 no owner row; B4's expected values (the invariant row) are unchanged under X6 r3 (confirmed in the X6 r3 / X7 r4 / X9 r2 review). Library only: no CLI command is wired, and nothing enables real-machine use.

## Law

All under arch `docs/implementation/m2/` unless named otherwise, accepted:
- `carrier-recovery-x6/PROPOSAL.md` r3, the law of this unit (r2 preserved in PROPOSAL-r2.md);
- `docs/v2/architecture/commit-recovery-readonly.v3.md`, the algorithm owner: §1 (vocabulary and projection), §2 steps 0 to 2 and 4, §2.1 to §2.3;
- `project-root-x2/PROPOSAL.md` r8, item 7's r6 exception (the read-only recovery selector's fence-free SHARED-READ);
- `commit-session-x3d/PROPOSAL.md` r6, items 3 step 5, 6 and 9 (`ExistingAttempt`, read with X6 r3 item 6);
- `finalization-x7/PROPOSAL.md` r5, items 3 and 10 (the `ExistingAttempt` row and its disclosure);
- `crash-matrix-x9/PROPOSAL.md` r2, item 5 and gap G3;
- `ordinary-platform-x1/PROPOSAL.md`, items 1 and 7 (one attempt, one entry per process);
- `read-premise-458c/PROPOSAL.md`, items 1 to 7 (the walk and member reads the admission shares);
- `refusal-suite-x8/PROPOSAL.md` r3 (B4; no X6 rows);
- your X6a reviews (`reviews/grok-recovery-capture-x6a-r1`, `-r2`): call 9 (the module was private with no re-export; X6b adds the public path and the location constructor) and call 14 (X6b maps the capture's budget failure).

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x6b`, detached at `f097c5b` (main, X7a integrated; the lock selects v125). The unit was written on 81214cb and moved to f097c5b when X7a integrated first: the diff applied unchanged, and X7a's `ExistingAttempt` disclosure was added (below). Save `git -C <worktree> diff` as product.diff and report its sha256. The eight new files are intent-to-add. Lead's value: `37c21bcffcfa7b1585915e9dcc3cb553e40277bf5b3c97c7ae84cf1f6f834f3f`, 160189 bytes; 27 files, 3462 insertions(+), 111 deletions(-).
- **Arch:** these files, all untracked:
  - `repository-file-inventory.v126.json` (parent v125);
  - `recovery-admission-x6b-inventory-v126-subject.json`;
  - `recovery-admission-x6b-inventory-v126/`.

## What was built

### Security

**`custody/recovery_admission.rs`** (new, macOS, `custody.rs`'s module):
- **`RequestedBinding`** (public, inert): `storeGenerationDigest` and `journalCarrierDigest` (64 lowercase hex), `namespaceId` (lowercase UUID v4 text) and `operationRef` (`op-` + 32 hex). One checked constructor.
- **`RecoveryRequest`** (public): `plain(executionId, namespaceId)` and `for_binding(executionId, RequestedBinding)`, whose binding's namespace is the selector.
- **`RecoveryAdmission::admit(request)`** (public) is one of X1 item 7's read entries: it produces the process's one read receipt (`produce_read_platform`; a process that already entered refuses on the invariant row there), allocates recovery's one ledger (`WorkLedger::new()`, the owner's caps, one per process; a second allocation is the invariant row), and runs the crate-private `admit_on(&mut ReadPremiseReceipt, …)`, the law's signature:
  1. **The walk.** `observe_account` and 458c's `walk_chain` from the root to I under the read receipt's lending. No fence: the fence file is neither opened nor waited on. A positive absence is the not-initialized row. The receipt's rechecks run.
  2. **The binding reads.** `installation_session::read_recovery_members`: `read_members` with its fence argument now `Option`; with `None` the fence member is neither read nor judged and the closing fence-identity check is skipped; every other member (registry judged; pair, marker, `state.v1`, node chain read and decoded) is read exactly as for the session. A finding is the incomplete row, a failure its own row. Then X3a's `validate_endpoint` against the receipt's selected core and K, and X2b's `capture_registry` on the judged registry sample.
  3. **N (r3).** Exactly one registry row with the request's namespace, status ACTIVE; N is that row's `namespaceId`. Otherwise `RecoveryRefusal::NamespaceUnregistered`, before any lease. S, G and K come from the endpoint only. `I/stores/S` is confirmed against the endpoint's admitted marker (X3d-2's `open_store_root` steps, moved unchanged into `store_root_in` and shared), and `I/trust` is confirmed private.
  4. **The lease.** `recovery_shared_lease`: `I/host`, `projects` and N confirmed (X2d's `required_directory`), `readers.lease` alone opened and judged (`open_carrier`), locked `LockMode::Shared` non-blocking (`lock`), then its binding and the directories rechecked, as one effect reserved first (`effect_lease`). It is built in this module from X2d's own primitives (made `pub(super)`, plus `HeldLease::shared_reader`), so `namespace_lease.rs` itself still takes no fence-free lease. `writer.lease` is never opened. A busy lock is `RecoveryRefusal::UnavailableBusy`. Then `crash_barrier!("x6.recover", "after-lease", step)` and a `cfg(test)`-only hook.
  5. **The recheck.** `recheck_files` over every captured sample (registry, pair, marker, `state.v1`, nodes) and N's spelling (`namespace_spelling`); any change is `UnavailableBusy`, never a conclusion. The receipt's rechecks run again.
- **What the admission lends:** `charge` and `charge_store` (recovery's ledger, with the admitted `I/stores/S`, its spelling and the user beside the scope), the admitted values (N, S, G, K, SHA-256(N)), the request, and `capture_carrier`: X6a's `recover_carrier` at `CarrierLocation::recovered`, charged to recovery's ledger, returning the public `CarrierObservation` (a budget failure or a query outside its representation is `CarrierCaptureFailure`).
- `RecoveryAdmission` is not Clone; dropping it releases the lease.

**`journal_store/recovery_location.rs`** (new, macOS child of `carrier_floor`, beside `recovery_capture`): `CarrierLocation::recovered(&RecoveryPlace)`, the recovery-side constructor, and `CarrierObservation` / `CarrierKind`, the public inert view of X6a's standing (kind, anchor class, would-write diagnosis, typed reason, offending digest, `limitation`, capture count). `journal_store.rs` re-exports `RecoveryQuery` and `recover_carrier` crate-wide and the two public types; `lib.rs` exports them with the admission types. X6a's own file is unchanged.

**Smaller security changes:** `store_custody::admit_existing_store_directory` (public; read-only admission of an existing store directory: no create, no barrier; `None` when positively absent); `commit_session`'s three row maps `pub(super)`.

### Storage

**`recover.rs`** (new, macOS):
- **`RecoveredCommit`** is exactly §1's standings, every variant `#[non_exhaustive]` so only storage constructs one; not Clone, Default or serializable: `CommittedHistorically { run_id, pending_settlement, legacy_custody_unknown, anchor, diagnosis }`, `CommittedAvailabilityDegraded { …, unavailable }`, `TerminalNotCommitted`, `UnknownAttemptOpen`, `UnknownAttemptUnobserved`, `UnknownCustody { reason, diagnosis }`, `UnknownQuarantineCondition { reason }`, `UnavailableBusy`, `BindingUnusable { subject }`, `UnknownCarrierIncompatible`. `standing()` is the owner's spelling; `limitation()` is `interior-bodies-not-authenticated` on both committed standings.
- **`recover(admission) -> Result<RecoveredCommit, RecoveryFailure>`** (call 1) composes `recover_from` over the admission:
  1. one ledger snapshot through `read_recovery_ledger` at the admitted binding (digest of (N, S, G, K) by X3d-2's recipe, now `pub(crate)`; N; SHA-256(N); the ExecutionId), then `crash_barrier!("x6.recover", "after-ledger-snapshot", step)`;
  2. a missing ledger (`ledger-missing`), a refused directory or ledger file, an unreadable or schema-drifted ledger (`ledger-unreadable`) are `UnknownCustody`; a busy one `UnavailableBusy`;
  3. (r3 item 6) a requested binding compared exactly: `storeGenerationDigest` with the admitted digest, `namespaceId` with N, `journalCarrierDigest` with SHA-256(N), `operationRef` with the snapshot's attempt row; the first difference, or no attempt row, is `BindingUnusable` with subject `store-generation`, `namespace`, `carrier` or `operation`;
  4. the settlement matrix (`join_ledger`, in that snapshot): `TerminalNotCommitted`, `UnknownAttemptOpen`, `UnknownAttemptUnobserved`, `UnknownCustody` (`ledger-join`), `BindingUnusable` (`association`), or continue;
  5. a joined receipt whose Run material row is absent is `UnknownCustody` (`run-material`) (call 9);
  6. X6a's capture through the admission; each carrier standing maps to its own (`BindingUnusable` with subject `carrier`); a budget failure is `RecoveryFailure::Budget`, a query outside its representation `Invariant`;
  7. for a confirmation, availability (call 10): every committed object (the inventory's typed objects by H digest and its raw blobs) read no-follow and hashed; all intact is `CommittedHistorically`, otherwise `CommittedAvailabilityDegraded` listing each unavailable one.
- `RecoveryFailure` (`Budget`, `Invariant`) maps to `WORK.BUDGET_EXHAUSTED` and the invariant row.

**`ledger_store/recovery_read.rs`** (new, `project_ledger`'s child): `read_recovery_ledger` (`projects` and N admitted only if present, the ledger's name observed absent or opened as a judged private file, one fixed snapshot cost charged, then exactly one `ReadSnapshot` that must name the same file and hold exactly the selected schema, then the existing `recovery_pins` capture, which nests the material, availability and ledger captures in that one snapshot; values returned, snapshot dropped). `check_objects` for the availability step. A refused directory or file is `ReadRefused`, which closed the ledger (call 7).

**`commit.rs`:** `NotPrepared::ExistingAttempt { execution_id, requested: Box<RequestedBinding> }`, built from the plan (`requested_binding`; an unbuildable one is the invariant row, unreachable). Boxed for clippy's `result_large_err` (call 12). **`availability.rs`:** `state_text`. **`recovery.rs`:** `LedgerStanding` derives Clone. **`commit_tests.rs`:** declares `recover_tests.rs` as its child module.

### Host

**`recovery_route.rs`** (new, macOS): `route_recovery(request)` → admission, one `recover`, then item 8's table through `standing` (one exhaustive match, no wildcard) and `project`: success (`Observed`) for `committed-historically` and `terminal-not-committed`, and for `committed-availability-degraded` with each unavailable object's `evidence.*` detail disclosed; the busy row for `unknown-attempt-open` and `unavailable-busy`; the host I/O row for `unknown-attempt-unobserved`, `unknown-custody` and `unknown-carrier-incompatible`; `LEDGER.CORRUPT`, no detail, for `unknown-quarantine-condition`; request-rejected, `EXTENSION.ADMISSION_REJECTED`, `RECOVERY.REFUSED` with the subject for `binding-unusable` and `namespace-unregistered`; admission refusals and the budget on their own rows. `required_object` is the degraded standing's second projection for a selected operation that needs an object (call 14). No `MIGRATION.CORRUPT` anywhere.

**`finalization.rs` (X7a, X7 r5 item 10):** `Joined` and `Concluded::ExistingAttempt` carry the requested binding; item 3's row now discloses all four members (`Termination.requested`, new; `namespace` is the binding's), beside the unchanged invariant row, ExecutionId subject and remedy. X7a's tests: the `ExistingAttempt` row checks the other three members, the join test passes the binding, and the source pin's exact security `use` line now names `RequestedBinding`.

## Judgment calls: please rule

1. **`recover` returns `Result<RecoveredCommit, RecoveryFailure>`**, not a bare `RecoveredCommit` as item 2 writes it. §1 has no budget standing, and item 5 says a limit failure "maps to the budget row and is never absence". Folding it into a standing would invent one. **Rejected:** a budget variant of `RecoveredCommit`.
2. **`RecoveredCommit`'s committed fields.** Item 2 lists `runId, pendingSettlement, legacyCustodyUnknown, confirmedUnderRetainedCustody, availability`. Confirmation is carried by the variant itself plus `anchor` (the class step 3 confirmed on), `diagnosis` and `limitation()`; availability by the variant (all available, or `CommittedAvailabilityDegraded` with the unavailable objects). No boolean can claim confirmation without an anchor.
3. **Admission's busy outcomes are refusals.** An EXCLUSIVE holder and a recheck change are `RecoveryRefusal::UnavailableBusy`: the admission is security's and `RecoveredCommit` is storage's, so it cannot return the standing. The host projects it on the same busy row as the `unavailable-busy` standing.
4. **The fence-free lease lives in `recovery_admission.rs`**, built from X2d's helpers, rather than in `namespace_lease.rs`: X2 r8 item 7 assigns the exception's admission to X6, and `namespace_lease.rs` keeps "no fence-free lease" true.
5. **What the recheck covers.** Every captured sample and N's spelling, plus the receipt's rechecks. 458c's `recheck_chain` is not run: it takes the held fence and compares it, which this selector may not hold. The chain was walked and admitted under the same receipt; item 3 step 5 names "the registry and endpoint samples". **Rejected:** a fence-free copy of `recheck_chain`.
6. **The admission confirms `I/stores/S` and `I/trust`** under recovery's ledger (the ledger and the floor live there), and refuses on the X2/468 rows if they are absent or not private. No fence is involved.
7. **The ledger's reads and refusals.** A positively absent `projects`, N or ledger file is `ledger-missing`, observed with if-present opens and an absence sample, never a failed open. A custody or I/O refusal of a directory or the ledger file fails its charged step, which closes recovery's ledger by the platform's rule; it is reported as `UnknownCustody` (`ledger-unreadable`), and nothing is charged after it. A busy ledger is `UnavailableBusy` (temporal, as X6a's call 6 treats a busy carrier). SQLite's read-only WAL open may create an empty `-wal` and `-shm`, as the existing readers do (X6a call 8); the ledger's bytes are unchanged (every storage test checks this).
8. **The F34 comparison runs before the matrix**, in the same snapshot, in the order store generation, namespace, carrier, operation; no attempt row is `operation`. The association-binding mismatch inside `join_ledger` keeps subject `association`, and the capture's §1 row 1 subject `carrier`.
9. **A joined receipt whose Run material row is absent is `UnknownCustody` (`run-material`).** The owner's step 1 reads the Run manifest in the snapshot; a receipt without its retained material is one-sided history (F23's family), never confirmed. The law is silent here.
10. **Availability.** For a confirmed receipt only (item 4): each object of the inventory (typed objects by H digest, raw blobs by digest) is opened no-follow under `objects/sha256` and must be one regular file with one link whose bytes hash to its name, its length charged first. Missing is `evidence.missing`, or `evidence.purged` / `evidence.expired` when the current availability record says purged or expired; anything else is `evidence.corrupt`; a refused objects directory makes every object `evidence.corrupt`. Other record states (`partial`, `corrupt`, `unavailable`) are not used to override an observation. Objects are not judged by the private-file predicate, because published objects are read-only (X3c item 4).
11. **The typed reasons** (`ledger-missing`, `ledger-unreadable`, `ledger-join`, `run-material`, and X6a's capture reasons) are operational values on the standing, never public details (§1).
12. **`requested` is boxed** in `NotPrepared::ExistingAttempt`; the variant still carries the whole binding.
13. **Tests split by crate, as X3d-2 did.** One process makes one read entry, and storage's tests cannot build security's admission (X9 r1 G1). So security tests admission plus the capture at the recovered location on real fixtures; storage tests `recover_from` (the function `recover` calls) over stores committed by X3d-2's own steps, with a scripted carrier verdict; the host tests its table on values. Admission and `recover` in one fresh process is X9-2/X9-3's.
14. **The degraded standing's second projection** (`required_object`) is provided but selected by no route here: the route selects no operation, and the selected operation's owner applies it (item 8).
15. **`read_members` takes an `Option` fence** rather than a copy of the member reader. With `Some`, its behaviour is byte-for-byte the session's (the fence member and the closing identity check stay); every existing session test is unchanged.
16. **Out-of-date inherited descriptions** are left for the next description successor (inventory README): `carrier_floor.rs` ("`CarrierLocation::admitted` … is CarrierLocation's only production constructor") is contradicted by X6 r3 item 12's recovery constructor; `installation_session.rs`'s consumer list, `store_custody.rs`, `commit_tests.rs` and X7a's `finalization_tests.rs` are out of date by omission.

## Tests

New: 23 tests. All 23 also pass with `--features opensip-platform/crash-matrix`, with the points live.
- **Security, `recovery_admission_tests.rs` (10):** the request and binding grammars; one ledger per process; N, S, G, K, SHA-256(N) and `I/stores/S` admitted while another holder keeps the installation fence for the whole admission, with `readers.lease` held shared and `writer.lease` free at `after-lease`, the lease released on drop and every file under I unchanged; an unregistered namespace refused with no lease; an EXCLUSIVE holder busy and an APPEND-WRITE holder (F29) admitted beside it; a changed registry, selection pair or store marker sample at `after-lease` busy; an absent I not initialized; a short ledger on the budget row; the carrier captured at the recovered location (another carrier refused with zero captures; no carrier yet is `carrier-absent` from one capture; a bad query refused) with I unchanged; and source pins (no fence, wait, writer lease, exclusive lock, create, publish, rename, sleep or SQL write; `after-lease` once; the shared lease and the fence-free member read as stated).
- **Storage, `recover_tests.rs` (9):** a confirmed commit `CommittedHistorically` with pending settlement, then without once settled, with the carrier asked exactly the association's half; the matrix (UAO and UAU without asking the carrier, the only negative, both contradictions); each carrier verdict its own standing; F34 member by member; F24 (no `projects`, a deleted ledger file, a non-database, a drifted schema); availability (`evidence.missing` and `evidence.corrupt`, then `evidence.purged` under a purged generation); a short ledger the budget failure; `ExistingAttempt`'s binding equal to the plan's and refused on `operation`; and source pins (no SQL write, transaction, creation, barrier, publication, settlement or sleep; `after-ledger-snapshot` once, after the snapshot).
- **Host, `recovery_route_tests.rs` (4):** every standing's row; the degraded standing's history success and second projection for each detail; admission refusals' rows; a source pin (one read entry, one `recover`, ten variants with no wildcard, no `MIGRATION.CORRUPT`, commit facade or writer admission).
- **X7a's `finalization_tests.rs`:** the `ExistingAttempt` row now checks all four binding members; 21 pass.

## Checks

At f097c5b plus this diff:
- **Workspace runs:** two full runs of `cargo test --locked --offline --workspace --all-targets`, each with its own private 0700 TMPDIR: each with 1660 passed, 0 failed and 3 ignored, across 17 test binaries (an earlier interrupted run is not counted).
- **Lints:** `cargo clippy --workspace --all-targets -- -D warnings` is clean; so are `-p opensip-platform --features crash-matrix` and `-p opensip-security`, `-p opensip-storage` and `-p opensip-host` each with `--features opensip-platform/crash-matrix`, all `--all-targets -- -D warnings`.
- **Formatting:** `cargo fmt --all -- --check` is clean, and the two new `include!`d security files are `rustfmt`-clean on their own (cargo fmt does not reach `include!`).
- **`check_package_edges --lane host`:** passes against v125 and v126, with 20 declared and 20 resolved edges.
- **verify_scratch** (v126 appended in memory to the worktree's lock at f097c5b, with the record's 55 rows): passes, with 86 inventory successors, 74 contract successors and 55 inheritance rows; v126 is selected.
- **verify_projection against the real lock at f097c5b:** 55 rows, 278 corruptions refused.
- **`build_v126.py`:** reruns produce the same bytes. 942 files; the 934 v125 rows are equal by value; 55 projection rows, each checked against the lock's inheritance row before it is carried, with D2's four `after` texts checked as their rows' effective descriptions.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X6b meet X6 r3 items 1 to 6 and 8 and item 12's X6b list, with the owner's step 0 to step 2 and §1's projection? In particular:
  - one read entry, the walk with no fence opened or waited on, N only from the one ACTIVE row, S, G and K only from the endpoint;
  - the fence-free SHARED-READ exactly as X2 r8 item 7's exception allows (no `writer.lease`, no upgrade, no wait), and busy for an EXCLUSIVE holder;
  - one recheck, with any change busy;
  - one ledger snapshot, the matrix inside it, F34's comparison, and no write, settle or repair on the path;
  - a missing, unreadable or fallback ledger never absence;
  - availability and both projections of the degraded standing.
- Are `after-lease` and `after-ledger-snapshot` right in name and place for G3?
- Is X7a's `ExistingAttempt` disclosure what X7 r5 items 3 and 10 require?
- Is v126 right on v125, with the eight added rows' text and the carried 55-row projection?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `recovery-admission-x6b-inventory-v126-subject.json` (lead's value `43e6c965eba581b32f971094eabe00747a4b1fded0e236951a22efe4c671b907`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v126, parent (the v125 pin), successorRecord (the pin of `recovery-admission-x6b-inventory-v126/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
