Grok review r1: X4a, the live security guards (law X4 r7 items 2 to 8 and 11), with the `x4.*` crash points of law X9 r1 G4 and X8 r3's group D rows for X4a, and inventory v116 (parent v117). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-live-guards-x4a-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below. Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent. Never read or print the private 413 UUID fixture.

## The unit

X4 r7 item 11 defines X4a as:
- the monitor's creation and its first read at the lease-free point;
- `OperationGuard`'s creation inside X2e's handoff;
- the shared monitor history;
- the observer thread and its per-observation ledger;
- the checkpoint over a `JournalAppendLock` borrow;
- `FinalGate` admission;
- the termination mapping.

Its dependencies are integrated: X4T (X4T-a, X4T-a2 and X4T-b, `current_trust_admission.rs` and `floor_publication.rs`), X2e (`operation_handoff.rs`, whose commented seams this unit fills), X3a and X3b (`JournalAppendLock`). X9-0 (daa7b01) and X8a (c2352ae) integrated while this unit was being built. The unit was rebased onto each before any review. The points are placed with the real macros, and X8 r3 assigns this unit three rows of the compile-fail suite.

Library only: no command is wired, and nothing here enables real-machine use.

## Law

All under arch `docs/implementation/m2/`, accepted:
- `live-guards-x4/PROPOSAL.md` r7 (the law of this unit);
- `trust-admission-x4t/PROPOSAL-r9.md`, the accepted r9: items 6 to 11, in particular item 9 (the fenced first read and the one-attempt reread) and item 10 (the fenced rows). `PROPOSAL.md` is now the r10 draft in review (X4T-a3: which roots item 3 authenticates from); it changes no interface X4a uses;
- `trust-bootstrap-x4b/PROPOSAL.md` r5 item 1: the monitor and gate first, one first read. X4B-b later wires the bootstrap into that read; this unit leaves the seam;
- `commit-session-x3d/PROPOSAL.md` r6: what X3d-1 expects of X4a (`OperationGuard`, the checkpoint, `FinalGate`, `AdmissionPermit`; items 3, 4, 5 and 7);
- `crash-matrix-x9/PROPOSAL.md` r1: item 4 (the `gate` kind), item 5 (scopes `x4.checkpoint`, `x4.gate` and `x4.observer`) and G4;
- `refusal-suite-x8/PROPOSAL.md` r3 item 3: group D's unnameable row for `AdmissionPermit`, `FinalGate` and `OperationGuard` (E0603, unit X4a), the export rule and item 3a's constructor census;
- `project-root-x2/PROPOSAL.md` r8 item 7a (the handoff) and X3b r10 (the append lock), as X2e built them.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x4a`, detached at `c2352ae1a9aec1f569a501623a989aa4e095cf05` (main). The lock selects v117. Save `git -C <worktree> diff` as product.diff and report its sha256; the eight new files are intent-to-add. Lead's value: `c1bd016c0330c0aee9d09befab33d597e0822cf7298a8cb2781649ec5179a346`, 212038 bytes; 34 files, 4019 insertions, 100 deletions.
- **Arch:** these files, all untracked:
  - `repository-file-inventory.v116.json` (parent v117);
  - `live-guards-x4a-inventory-v116-subject.json`;
  - `live-guards-x4a-inventory-v116/`.

## What was built

**The lease-free point (item 2; X4B r5 item 1).** In `operation_handoff.rs`, `trust_start` runs first at X2e's lease-free point. That is under the writer's fence with R current, before any lease, and before X3b's floor step.
1. `LeaseFree::create` makes the operation's one gate and its `FreshnessMonitor`. The gate is `commit_authority::OperationGate`, made before any prepared value exists.
2. On the gate's ledger (`OrdinaryWriteAdmission::gate_step`, item 9), the monitor's first `read` runs:
   - X4T-b's `fenced_first_read`, over the retained `state.v1` owner bound to the gate's one read (its bytes and sample);
   - with the S4 observation projected from that read's own opening sample, by the existing `clock_observation` projection;
   - with the floor publication's invocation, which the caller supplies.
3. A confirmed write-ahead publication advances the gate's retained owner (`DurableInstallation::advance_current`), so the gate's recheck that follows passes.
4. The trust store's retained handles are opened and judged on that same ledger: `trust/stores/S`, its `events`, and `objects`, `records` and `publications`. Each is a no-follow child bound by exact name, judged private and on H's filesystem.
5. The gate's full recheck and the receipt's recheck run, still under the fence.

On refusal:
- a monitor failure is the fail-stop row;
- an X4T refusal is its item 10 row.

**The guard (item 6).** After X3b's carrier start and the post-start recheck, still under the fence, `OperationGuard::start` builds the guard. It is built from the gate, the monitor, the start view, the handles, the receipt's core closure and the trust groups. It moves into `ProjectOperation` as its first field, and its observer thread starts.
- `ProjectOperation::end` drops the guard first.
- A dropped operation drops the guard first, by declaration order.
- `guard()` exposes the gate's state, the first stop cause and the drift.

**The shared history (items 2 and 5).** There is one `MonitorCell` (the monitor and its clock) behind one mutex, shared by the observer's ticks and every checkpoint. No read resets it or the latch.
- `FreshnessMonitor` gains `read_sampled_with`: the counter receives the opening sample.
- It also gains `boundary_with`: item 3 step 4's single sample.

**The observer (item 5).** Each tick does one `read` whose counter is `LiveObservation::observe`, on a fresh per-observation ledger of 2 × `TRUST_VIEW_COST`.
1. Step 1 opens `state.v1` by name through the store handle.
2. Steps 2 and 3 run X4T-a's reread (`admit_current_trust` in `ReadMode::Reread`) through `RetainedStore`. That store opens each file by name under its collection's retained handle, located by the native readers' own `locator_components`.
3. Step 4 reopens `state.v1` by name and compares its identity and full sample.

All four steps run once more if step 4 differs; a second difference is `mixed`.
- A revoked closure component is the revoking observation.
- A view below the start view's floors or counters is a rollback, and never reaches the predicate.
- Then S6's `observe_revocation` runs against the immutable start epoch and closure, with empty required pairs.
- A revocation latches with `trust-revoked` or `policy`. Drift is recorded. Every other failure is a fail-stop with its reason.

Production ticks every 5 s (`recv_timeout`). Tests tick only on request (`Cadence::Manual`, `cfg(test)`). The observer never takes the fence and appends nothing.

**The checkpoint (items 3 and 4).** `ProjectOperation::journal` now lends a `Checkpoint` beside the location and carrier. It does this inside `WritePlatformReceipt::charge_guarded`, which lends the receipt's in-scope rechecks (the actor's, core's and platform's `_in` variants) on the same attempt-ledger scope. `Checkpoint::effect` and `Checkpoint::admit` take a `&JournalAppendHeld`, which must hold this operation's own append lock (`JournalAppendHeld::holds`). Inside `crash_scope!("x4.checkpoint")`:
1. **Step 1, the guard rechecks, charged to the attempt ledger:**
   - the write receipt;
   - the held lease, by name binding (`recheck_binding`) and by a fresh nonblocking EXCLUSIVE probe on a new descriptor;
   - the original owners: for an Eligible root, `ProjectRootAdmission::recheck_owners` (chain, incarnation, marker); for a registered project, `recheck_registered_owners` (chain, incarnation, `.opensip`, marker by descriptor and by name);
   - the namespace (`recheck_namespace_at`);
   - the store marker and lineage nodes, each by full sample;
   - the joins: N, S, G and K, and the append lock's N.
2. **Step 2:** the monitor is locked and the final monitored observation runs, with the predicate.
3. **Step 3:** the latch.
4. **Step 4:** `boundary_with`.

Then either `OperationGate::admit(prepared)` mints the one `AdmissionPermit`, handing the prepared value back on a refusal, or the effect's own intent append follows. The monitor is held from step 2 through admission. Any failure latches the gate, records the first stop cause and is returned as `GuardRefusal`.

**Rows (item 8).** `InstallationTermination` gains `RootDetail` and seven variants on existing details:
- `TrustNoAdmittedTimeContext`;
- `TrustContinuation { subject }`;
- `TrustRoot { detail, subject }`;
- `TrustPayloadNotAdmissible { subject }`;
- `ClockExcursionForward { subject }`;
- `RevokedDuringOperation { subject }`;
- `ObserverFailStop { subject }`.

Trust rollback and `required-files-changed` reuse `Custody`, and the remaining rows reuse their existing variants. `operation_guard::trust_termination` maps X4T's `TrustRow`. The host projection follows S12's classes: `ROOT.SCHEMA_UNSUPPORTED` is schema-major, the other chain details and `PAYLOAD-NOT-ADMISSIBLE` are admission rejections, and `CLOCK-EXCURSION-FORWARD` and F absent are precondition failures. The match stays exhaustive.

**X8 r3 group D (`crates/host/tests`).** Three cases under `refusal/cases/`, one per type:
- `security_admission_permit_unnameable.rs`;
- `security_final_gate_unnameable.rs`;
- `security_operation_guard_unnameable.rs`.

In each, the control (`use opensip_security::InstallationTermination`) compiles. The misuse names the type by its path and fails with exactly one E0603, on the first private module in that path: `commit_authority` for the first two, `custody` for the last. `admission_tests.rs`'s census gains them as unit X4a, group D, category forged receipt, through an `owned` row constructor. X8a's driver passes with 26 cases. A mutated fragment fails it.

**Crash points (X9 G4).** Each expands to nothing without the test-only feature. The security crate compiles with `--features opensip-platform/crash-matrix`.
- `x4.observer.tick`, of kind `gate`, wraps the observer's timed wait.
- `x4.observer.after-observation`.
- `x4.checkpoint.before-observation`, `.after-observation` and `.before-admit`.
- `x4.gate.admit.after` (in `OperationGate::admit`) and `x4.gate.latch.after` (in `FinalGate::latch`).

## Judgment calls: please rule

1. **X9-0 points placed with the real macros.** X9-0 landed mid-unit, so the unit was rebased and the points placed: G4's names in the registered scopes, the checkpoint wrapped in `crash_scope!("x4.checkpoint")`, and the gate points in `FinalGate`.
   - In a matrix run, the lease probe's `lock` and `unlock` primitives are named under `x4.checkpoint`.
   - Security gains no feature of its own: the macros take the platform feature, and per-crate support modules are X9-1's.
2. **A gate created before its prepared value.** `PreparedAttempt::new` binds the value at creation, but X4 item 2 creates the gate at the lease-free point, long before X3d's adapter exists. So `OperationGate::new` makes the gate alone, and `admit(prepared)` binds the value at item 3 step 4. A refusal hands the value back, for X3d's stop order. The same `FinalGate` and two-bit law are used. **Rejected:** a placeholder prepared value, and a second gate type.
3. **The closure subjects come from the start view.** Item 2 says the closure subjects are taken from the admitted view "and nowhere else"; item 6 lists them. The view now keeps X4T item 4's own `ClosureComponents`:
   - the release, which is the receipt's selected core closure as passed into the read;
   - the signing keys;
   - the namespaces;
   - the catalog snapshot.

   It also keeps the admitted `RevocationEvidence`, for the predicate. Item 6's "namespace N" is read as the revocation list's `namespace` subject kind, the signing namespaces. The project's N is not a revocation subject. **Rejected:** a second derivation of the subjects in X4a.
4. **A revoked component on a reread is the revoking observation.** X4T-a's reread refuses a revoked closure component on the continuation row, before X4's predicate can see it. X4T item 10's parenthetical gives that refusal to X4 during an operation, so it is classified as `trust-revoked`, by its subject's kind prefix (`release:`, `keyId:`, `namespace:`, `catalogSnapshot:`). A role-standing refusal (`core:…`, `index:…`, `component:…`) is a fail-stop, `standing`. The predicate's own match path still runs for subjects the reread's closure no longer contains.
5. **Rollback is judged against the start view.** A reread whose clock floors, or whose root, index or revocation counter, is below the start view's is the fail-stop `rollback`, decided before the predicate. X4 forbids a lower counter reaching it, and X4T item 9 makes rollback X4's callback error. Nothing extra is read.
6. **The reading path through the retained handles.** X4T-a's `admit_native` walks from the fence's I, and `capture_p2` hard-wires that walk. The observer uses the same loaders over a `RetainedStore`:
   - X4T-a's `admit_current_trust`, which runs the same `load_at` of the descriptor and `current_record_bindings::bind` (with `bind_trace`) that `capture_p2` runs;
   - `state.v1` read through `Budget::capture_current` under the store handle.

   **Rejected:** a `HeldFence` adapter, which would reopen every path from I.
7. **Step 4's identity, and the retry.** Step 4 reopens by name and compares:
   - the name's device and inode with the step-1 descriptor's;
   - link counts of 1;
   - the step-1 descriptor's fresh sample (metadata and ACL) with its step-1 sample.

   Any difference, or a missing name, is a retry. A refusal in attempt 1 is the observation's error, not a retry: an atomically replaced pointer's old closure is immutable and never deleted, so a refused first view is unreadable, not mixed.
8. **The S4 observation.** It is the projection of the first read's own opening sample (wall clock, the bracket's midpoint, boot), through `clock_observation`'s existing projection (`project_monitor_sample`).
9. **The floor publication's invocation.** No law says where an ordinary writer's `host-trust-admission` invocation comes from. `begin_operation` takes a `TrustInvocation` (`req1_`/`exec1_` with 32 lowercase hex, a step id) from its caller, X3d-1 or the CLI unit. **Rejected:** drawing ids at the handoff, which would put a request id on the record that is not the request's.
10. **The write gate as `HeldFence`.** `WriterFence`'s recheck checks that the locked descriptor's name is `lifecycle.fence`, and that the name under I is that descriptor (device and inode). It is uncharged, like the supplied fence's recheck. The gate's full recheck follows the step in `gate_step`. The fenced read and the handles are charged to the gate ledger, as item 9 requires.
11. **The guard set after the release (item 4).**
    - **Endpoint and lineage owners:** the required files under `stores/` (the store marker) and `transitions/` (the lineage nodes).
    - **Not rechecked, as provenance:** the registry, the selection pair, `state.v1` (another writer's floor publication changes it lawfully) and the fence carrier.
    - **Owners:** only the original owners X4 names; the registry, its `v1` absence and the tracking observation are excluded.
    - **Joins:** an in-memory mismatch of N, S, G and K, or the lock's N, is the invariant row.
12. **"Lock still held".** A fresh nonblocking EXCLUSIVE attempt on a new descriptor of the named carrier must be refused. If it is granted, the probe's lock is dropped at once, and the result is S7's busy row. An in-process `FileLock` cannot detect its own loss. Tests lose the lock through a `cfg(test)` seam that keeps the carrier's sample.
13. **The mutex wait.** The opening sample is taken after the monitor is acquired, so the monotonic ordering check holds. The bound runs from the previous read's earliest instant, which precedes any wait, so the waiting time is inside the waiting read's bounded interval (tested). No wait occurs between steps 2 and 4.
14. **Subjects.**
    - Monitor reasons: `clock-unavailable`, `clock`, `unreadable`, `stalled`, `latched`.
    - Observation reasons: `unreadable`, `mixed`, `unauthenticated`, `rollback`, `budget`, `standing`.
    - Any step-4 failure: `admission-boundary`.
    - A first-read monitor failure is the fail-stop row, never an X4T row.
15. **The first cause wins.** The guard records the first stop. A later refusal names it, and X3d's `finish` reads it with the state and the drift. A checkpoint refusal also closes the attempt ledger through its `Err`, as X3d r6 item 8 plans.
16. **The observer's lifetime.** It starts in `OperationGuard::start`, under the fence, as the guard moves into the operation. A spawn failure is the host I/O row. Dropping the guard sends Stop and joins the thread. X3d r6 item 3 step 0 says the observer "was started at the lease-free point". X4 item 5 starts it at the move into `ProjectOperation`, and this unit follows X4.
17. **The termination mapping.** Seven variants and `RootDetail` (item 8: new variants, existing details, no new code).
    - The doctor's remedy table is not extended: doctor never emits these rows, and CLI enablement is not claimed.
    - X4T's interim continuation detail stays `CONTINUE-CORE-NOT-TRUSTED`, with the role-naming subject, until X4T-c lands.
18. **Test support.**
    - X4T-0's `Spec` gains `store` and `revocation_version`, with unchanged defaults.
    - `root_payload.rs` gains a `cfg(test)` `write_accepted_trust`, so custody's tests never name the generator, and X4T-0's source pin holds unchanged.
    - `ReadFixture` gains:
      - `accept_trust` (in place);
      - `write_trust`;
      - `swap_trust`, which publishes like another writer: immutables first, then `state.v1` renamed over the old one.

      Every new trust file gets the zero-rights owner allow.
    - X2e's own 17 tests now run on accepted stores through a `begin_test` adapter (scripted clock, ticks on request). Their assertions are unchanged.
19. **`journal`'s signature.** The action gains `&Checkpoint`. No production caller exists yet; X3d-1 is the first.
20. **Inherited descriptions.** All rows stay by value. The README lists the descriptions now out of date, for the description-only successor; the most visible is `operation_handoff.rs`'s "OperationGuard (X4a) is a seam not built here".
21. **X8's rows for this unit.**
    - **Three rows.** One E0603 case per type the law names. `FinalGate` is pinned by its own name. This unit's new `OperationGate` sits in the same private module and is not a row of the law. **Rejected:** adding a fourth row of my own.
    - **Code and fragment.** The code is X8's (E0603). The fragment is rustc's "module `…` is private" on the first private module of the path. `custody` and `commit_authority` are both private modules of `opensip-security`, so the misuse cannot reach the type's own privacy.
    - **Category.** Forged receipt, which is row D's category.
    - **Constructor census (item 3a).** Every `cfg(test)` item of this unit is pinned by `OperationGuard`'s or the gate module's unnameable case, under the export rule. That covers `OperationGuard::tick`, `hold_monitor`, `Cadence::Manual`, `scripted`, `begin_operation_with`, `HeldLease::lose_locks` and `write_accepted_trust`. The last two live in already-unnameable custody and trust modules. There is no abstract test lock: the real `JournalAppendHeld` is used.

## Not done, for the lead

- **F-1: expiry on rereads.** X4T r9 item 6 says observer rereads "evaluate expiry and staleness at the handoff's tEval advanced by the elapsed sleep-inclusive monotonic time". X4T-a's accepted `ReadMode::Reread` evaluates no time, and X4 r7 does not assign this to X4a. This unit does not invent it. It needs an X4T-a successor, or an X4 amendment that assigns it.
- **Policy-change drift is not reachable end to end in M2.** There is no project permission-policy owner, so both reads use `Source::Missing`. The predicate's policy branch remains covered by the existing `revocation_observe_tests`.
- **The build plan's altered input, inventory, execution and generation handoff tests** need X3d's session. They are not built here.

## Tests

New, 32 in all:
- `operation_guard_tests.rs`: 7.
- `operation_live_tests.rs`: 19, through the real handoff:
  - **the first read:** the start view admitted before any lease, with the write-ahead and a clean tick; P0 refused `TRUST.NO_ADMITTED_TIME_CONTEXT` before any lease;
  - **admission:** one permit; a revoking tick after admission takes the gate from 1 to 3 without relabelling; a second admission refused;
  - **timing:** a pause beyond the bound fail-stops before any effect; ticks and checkpoints share one history; the admission boundary; a boot change; a read waiting on the monitor counts its wait;
  - **wrong caller:** another operation's level 4 is the invariant row;
  - **trust changes:** drift while another holder keeps the fence; revocation through the observer and through the checkpoint; a missing newly named revocation body is `unreadable`; a pointer below the start view is `rollback`; a replacement absorbed inside one read, and `mixed` twice;
  - **stale guards:** a lost lock is the busy row; a replaced lease file, a substituted marker, a replaced store marker, a namespace no longer private, a substituted root and a missing store marker each refuse on their own rows;
  - **operation scope:** an unrelated registration does not invalidate the operation; a repeated checkpoint after an RA; the end path.
- `live_observation_tests.rs`: 5.
- Host: 1 new test, and 8 new rows in the projection table.
- X8a's driver: 3 new compile-fail cases. It is still one test; there are now 26 cases.

Every test uses scripted clocks; no test sleeps. The only waits are channel receives on the test-requested tick and its acknowledgement.

## Checks

Product checks are at c2352ae plus this diff. Arch verifiers run against the real lock at c2352ae, which selects v117.
- **Workspace runs:** two full runs on the final bytes at c2352ae, each with 1526 passed, 0 failed and 3 ignored. (Before the X8 rows and the rebase, two runs at daa7b01 each had 1522 passed, 0 failed and 3 ignored.)
- **Lints:** `cargo clippy --workspace --all-targets --offline --locked -- -D warnings` is clean, and `cargo fmt --all -- --check` is clean.
- **`rustfmt --check --edition 2024`:**
  - clean on the five new files and on `operation_handoff.rs`, `operation_handoff_tests.rs` and `ordinary_targets.rs`;
  - every other touched file is at exactly its base delta (installation_admission 15, installation_read_fixture 8, ordinary_writer 2, project_admission 19, read_premise 1, accepted_store_fixture 4, current_trust_admission 12, root_payload 4).
- **Feature build:** `cargo build -p opensip-security --features opensip-platform/crash-matrix` compiles.
- **`check_package_edges --lane host` against v116:** passes, with 19 declared and 19 resolved edges.
- **verify_scratch:** passes, with 79 inventory successors, 72 contract successors and 16 inheritance rows; v116 is selected.
- **verify_projection against the real lock:** 16 rows; 83 corruptions refused.
- **`build_v116.py`:** reruns produce the same bytes. 843 files; the 835 v117 rows are equal by value.
- **Home:** `~/Library/Application Support/OpenSIP` is absent.

## Decide

- Does X4a meet X4 r7 items 2 to 8 and its item 11 scope? In particular:
  - the monitor and gate are created first, and the fenced read is the monitor's first read, at the lease-free point and before any lease;
  - the guard is built inside the handoff and moved into the operation;
  - there is one shared history;
  - the observer reads only through the retained handles, takes no fence, uses its own ledger and appends nothing;
  - the checkpoint's four steps run over a real level-4 borrow, with nothing between steps 2 and 4;
  - there is one permit;
  - each stop names item 8's row.
- Are the X9 G4 points the right names, kinds and places?
- Rule on calls 1 to 21, and on F-1.
- Do the three group D cases pin what X8 r3 assigns to X4a?
- Is v116 right on v117?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `live-guards-x4a-inventory-v116-subject.json` (lead's value `dbe4d3d72b4a99545b3de4e77952281016c9db03e58babf2e67720bb999c2c4a`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes and sha256 of v116, parent (the v117 pin), successorRecord (the pin of `live-guards-x4a-inventory-v116/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
