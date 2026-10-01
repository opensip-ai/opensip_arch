Grok review: X2d, namespace admission and leases (law X2 r8 item 7), returning `FencedNamespace` with the installation fence still held, with inventory v110 (parent v105). Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-namespace-lease-x2d-r1. If you build or test, use a CARGO_TARGET_DIR under that directory. Run git only read-only, and only against the worktree below.

Law: `docs/implementation/m2/project-root-x2/PROPOSAL.md` r8 (accepted), item 7 (including its ordering note and its r6 exception for the read-only recovery selector), with items 3, 4, 6a, 8, 9 and 10's X2d row as they bear on it. Item 7a (the handoff, unit X2e) is the next unit and is not built. Also: S7 "Leases and lock order" in `docs/v2/contracts/product-v1/security-and-lifecycle.md`; `journal-x3b/PROPOSAL.md` r8 as committed at arch 320ee4d38 (`git show 320ee4d38:docs/implementation/m2/journal-x3b/PROPOSAL.md`; the working copy is being amended to r9 by the X3b-4 unit and is not this subject), items 1, 3 and 4 (the floor step runs under the fence, before X2d's lease, with no project lock; X3b-3 composes it, not X2d). Integrated predecessors: X2a (chain walk), X2b-1 (`ProjectRootAdmission`, R0), X2b-2 (tracking), X2c (0206ce8, first registration, `RegisteredProject`, R2, the namespace with `writer.lease` and `readers.lease`), X1a (ordinary writer), 458c (read session). The private `lifecycle::leases` two-lock composition is the semantic starting point.

## Subject

Pins are in hashes.txt.
- **Product:** the worktree `/Users/sb/code/opensip-ai/opensip-x2d`, detached at 0206ce8 (X2c integrated, inventory v105 selected). Save `git -C <worktree> diff` (the two new files are intent-to-add) as product.diff and report its sha256. Lead's value: `90009b2e2fef312064a496bb7402b195146eebf03132876dd066544ce465bbb6`, 75110 bytes; 6 files, 1620 insertions, 20 deletions.
- **Arch:** v110 (parent v105: `repository-file-inventory.v105.json`, 359222 bytes, sha256 `ebd9cf3361d4f854adcfbe8fcffd8e6e5ca9bd0af38315f950638212b5934a08`), `namespace-lease-x2d-inventory-v110-subject.json` and `namespace-lease-x2d-inventory-v110/`. These files are untracked in arch until acceptance. v106, v108 and v109 are other units' in-flight candidates on the same parent; they are not part of this subject.

## What it does

New code: `crates/security/src/custody/namespace_lease.rs` (a macOS module of custody.rs) and its tests. Everything is crate-private, runs under a held installation fence on the fence holder's one ledger, and is charged before it runs.

- **Fence holders (`FenceHolder`).** Two implementations, each beside its private state:
  - the ordinary writer's gate (ordinary_writer.rs), used by `OrdinaryWriteAdmission::admit_namespace`;
  - the read session (installation_read.rs), used by `ReadSession::admit_namespace`.
  
  Each step runs on the holder's ledger with its receipt's premise. Then comes the holder's full recheck: the gate's recheck plus the write receipt's recheck (`settle`), or `ReadSession::recheck`. Any refusal spends the gate or latches the session, and drops whatever the step returned.
- **Subject (`NamespaceSubject`).** Either `Eligible { ProjectRootAdmission, TrackingObservation }` (R0), or `Registered(RegisteredProject)` (R2, writer only). The read session builds only `Eligible`.
- **N and the row snapshot (`active_row`).** N is never taken from a caller.
  - For Eligible, the classification must be `Eligible{N, P}`, and R0 must hold exactly one row at N: ACTIVE, with ProjectId P.
  - For Registered, R2's row must be ACTIVE and still classify `Eligible{N, P}`.
  - Otherwise: `NotEligible` (rows below) or `Invariant`.
  - The scan is charged.
- **`admit` → `NamespaceTarget` (no lock).**
  1. N and the row snapshot.
  2. The subject's recheck: `ProjectRootAdmission::recheck` and `recheck_tracking` against that admission's chain, or X2c's `recheck_registered`.
  3. Namespace confirmation through the retained I. Each of `host`, `projects` and N must be present (absence is the incomplete row), installation-private (`observe_private_directory`), exactly named, and on its parent's device. For Registered, N's identity must equal the directory X2c published.
  4. `writer.lease` and `readers.lease` are opened no-follow under N, judged private regular files (`private_file`: owner, 0600, one link, ACL), and retained with their full samples.
  5. The holder's full recheck.
  
  The target exposes `namespace_id`, `row`, `subject` and `namespace_directory`.
- **The floor-step seam.** `NamespaceTarget` is where X3b's floor step will run (X3b-3): the fence is held, R is current, and no project lock is held. Its probe can lock `writer.lease` through `namespace_directory()`, as a test shows. X2d does not compose the floor step.
- **`lease_writer(AppendWrite | Exclusive)` and `lease_shared()` → `FencedNamespace`.**
  1. The subject's recheck, the directories' rebind and privacy, and each retained carrier: the same full sample on its descriptor, and the same sample by a no-follow reopen of its name.
  2. One effect whose whole work is reserved before the first lock (`work.effect` + `prepaid`). It takes the locks with `FileLock::try_acquire` (LOCK_NB):
     - APPEND-WRITE: `writer.lease` EX;
     - SHARED-READ: `readers.lease` SH;
     - EXCLUSIVE: `writer.lease` EX, then `readers.lease` EX.
     
     Then, inside the same effect, each locked carrier's name binding is rechecked (reopen plus the pre-lock full sample, which proves that the name still binds the locked inode), and so are the directories.
  3. The holder's full recheck.
  
  A busy carrier is `Busy`. A lock I/O failure is host I/O. Any refusal after a lock drops `HeldLease`, which releases `readers.lease` before `writer.lease` (reverse acquisition order) while the holder still holds the fence.
- **`FencedNamespace`.** It holds the lease, the mode, the borrowed holder (`&mut OrdinaryWriteAdmission` or `&ReadSession`), the subject (the root admission), the ACTIVE row snapshot and the retained namespace. It has `mode`, `namespace_id`, `row`, `subject`, `namespace_directory`, and `recheck` (subject, directories, each locked carrier's binding, then the holder's recheck). It has no upgrade, no serialized form, no Clone and no release. Because it borrows the holder, the fence cannot be released while it lives. Dropping it releases the lease; the fence goes later, with its holder.
- **Rows.** `NamespaceRefusal::row()` returns X2c's `RegistrationRow`, which gains `Busy` (item 8's busy row, `LEDGER.BUSY_TIMEOUT` / `PROJECT.BUSY`). `ProjectWriteRefusal` gains `Namespace(Failure)`, and `ProjectWriteRow` maps it as before. `NamespaceSessionRefusal { Session, Namespace }` is new. No public code is added.
- **Supporting edits in first_registration.rs.** `Step::Lease`, the two variants above, `pub(super)` on owner checks and constants that X2d reuses (`private_child`, `rebind`, `identity`, `private_file`, `same_private`, `recheck_registered`, `admission`, `tracking`, `private`, `capture_cost`, `name_cost`, `HOST`, `PROJECTS`, `WRITER_LEASE`, `READERS_LEASE`, `STATUS`, `ELOOP`), and its header comment.

## Judgment calls: please rule on each

1. **Where the lease code lives.** X2d builds in `opensip-security`. It mirrors `lifecycle::leases`'s two-lock semantics on the platform `FileLock` and does not call that module: the module is private and works over supplied handles, and security has no edge to lifecycle. No crate edge is added.
2. **Two phases, with the target as the floor-step seam.** `admit_namespace` returns a lock-free `NamespaceTarget`, and only `lease_*` locks. X3b r8 item 3 needs a point under the fence, after R is current and before any lease, so the target is that point. `lease_*` reruns every recheck before the first lock, so anything that ran in between is seen. **Rejected:** a closure hook inside one call, which would hide the seam X3b-3 composes.
3. **Fence by borrow.** The target and `FencedNamespace` borrow the holder: `&mut` the writer, so at most one at a time, or `&` the session. "X2d does not release the fence" is therefore enforced at compile time, and drop order gives "lease, then fence". There is no explicit lease release: item 7a says that until X2e, a `FencedNamespace` "can only be dropped". Unlock errors on drop are not reported.
4. **Modes per holder.** The write gate offers APPEND-WRITE and EXCLUSIVE. The read session offers SHARED-READ only, since item 4 says read commands get Eligible's namespace for read leases. No SHARED-READ is offered on the write gate, because no writer path needs one. The read-only recovery selector's fence-free SHARED-READ (item 7's r6 exception) is X6's and is not built: every lease here is under a held fence.
5. **Namespace custody, not footprint.** Admission requires `host`, `projects` and N to be private and both carriers to be private regular files. It does **not** require X2c's exact two-entry footprint or empty carriers. X3b r8 item 2 puts the carrier, its sidecars and the witness in N, and no law sizes or writes a lease file. A Registered subject still goes through X2c's `recheck_registered`, which checks the exact footprint. That is correct within X2d, but it means X2e/X3b-3 must not run a Registered `FencedNamespace::recheck` after carrier creation (X3b 3a) without relaxing that check. This note is for X2e.
6. **Rows.**
   - FirstUseCandidate is invariant: it registers first, and asking for its namespace is a broken composition.
   - RecoveryNeeded and OneSided are `identity-recovery-required`; Contradiction is `identity-contradiction`.
   - A missing `host`, `projects`, N or carrier is 468's incomplete row: R's ACTIVE row names N, as X2c treats a transition slot.
   - Custody failures are 468's custody row (`private`, `symlink`, `not-a-regular-file`, `volume-unsupported`).
   - A changed owner is `required-files-changed`. A busy carrier is the new `RegistrationRow::Busy`. Lock and native I/O are host I/O.
7. **Busy spends the gate.** Busy spends the gate or latches the session, like every refusal on these ledgers. S7's backoff retry outside the fence therefore needs a fresh admission, and with one gate per process (X1 item 7) that is the composition owner's retry (X11), not X2d's.
8. **Rechecks.**
   - `admit`: the subject's recheck, then confirmation, then the holder's recheck.
   - `lease`: the subject, the directories and the carriers (descriptor sample and name) before the lock; then each locked carrier's binding and the directories; then the holder's recheck.
   
   Item 6a's tracking recheck therefore runs before any lease, at both points.
9. **Budget.** The locks and their post-lock rechecks form one effect, reserved before the first lock (467 item 6). Its cost is: each `LOCK` (lead's constant: 0 objects, 3 edges, 512 bytes, for the kind-check stat, `F_GETFD` and `flock`), plus each binding reopen and capture, plus three rebinds and captures. A shortfall fails closed before any lock. Unlocking on drop is uncharged, so a release can never be refused for budget.
10. **Inputs per call.** The trust groups, environment and system sources are passed to each call, as in X2c's `_with` forms. No production wrapper is added: the module is library-only, and X2e will own them.
11. **No transition gate here.** Item 7 names none, and S7 item 4's transition crash recovery is the first act under a fence, owned by the transition units. X2c's `transitions_quiet` stays registration-only.
12. **Stale description.** `ordinary_writer.rs`'s row is carried by value and stays out of date (the writer now also leases), deferred to the same description-only successor named at inventory97, 101, 102 and 105.

## Tests

`namespace_lease_tests.rs` has 11 tests. They use `ReadFixture` scratch homes and an ordinary writer over signed test trees that registers a scratch project (X2c). Other holders are simulated by `flock` on separate descriptors, which conflict like another process's. The environment is empty and there are no system sources.
- **Rows:** every `NamespaceRefusal` row, and `WriterLease` to mode.
- **Fresh registration, APPEND-WRITE:** the target holds no lock. `writer.lease` is exclusive and `readers.lease` is free for SH and EX. The fence is held throughout. `recheck` passes. Dropping releases the lease while the fence stays held until `writer.release()`.
- **Eligible root, new writer, EXCLUSIVE:** N comes from R0's classification. Both carriers refuse SH to others, and dropping frees both.
- **Read session, SHARED-READ:** other readers can take SH, EX is refused, and `writer.lease` stays free for EX. `recheck` and the session's recheck pass while the lease is held. Dropping frees the lease, and the fence frees only when the session drops.
- **Busy:**
  - EXCLUSIVE with an outside reader: busy, `writer.lease` free afterward, the fence still held, the writer latched.
  - APPEND-WRITE with an outside writer: busy.
  - SHARED-READ with an outside EXCLUSIVE: busy, and the session latched.
- **Not eligible:** a FirstUseCandidate is invariant, with nothing under I created. A one-sided root (marker removed) is `identity-recovery-required`.
- **Missing or foreign namespace:** no `readers.lease`, or N moved, is incomplete. N at 0755, a carrier at 0644, or a linked carrier is installation custody.
- **Change between target and lease:** a replaced carrier (`required-files-changed`), a new `.hg` (`vcs-unsupported`), and a rewritten registry (an admission row) each refuse with no lock held and the fence still held.
- **Floor seam:** a probe through `target.namespace_directory()` takes and releases `writer.lease` EX, then the lease succeeds.
- **Lease recheck:** a carrier replaced under a held SHARED-READ is `required-files-changed`, and the session latches.
- **Budget:** a session measured to the lease is reopened with limits cut at 0/4 to 3/4 of the lease's measured work. Each run refuses with no lock and the fence still held.

## Checks

- X2d tests: 11/11.
- Full workspace at 0206ce8 plus this diff, two clean runs: 1390 passed, 0 failed, 3 ignored each time. One earlier run 2 attempt hit the tracked F4 flake (`installation_observation::tests::an_earlier_ancestor_changed_during_capture_or_consumption_refuses`) while another worktree's suite ran concurrently. That test passed alone, and the full rerun was clean.
- `cargo clippy --workspace --all-targets --offline --locked -- -D warnings` and `cargo fmt --all --check` are clean.
- `rustfmt --check --edition 2024` is clean on both new files and on first_registration.rs. ordinary_writer.rs and installation_read.rs were not rustfmt-clean at base; the added hunks are.
- `~/Library/Application Support/OpenSIP` is absent.
- `check_package_edges --lane host` against v110 passes.
- verify_scratch (v110 appended over the real lock at 0206ce8) passes: 71 inventory successors, 72 contract successors, 16 inheritance rows, v110 selected.
- verify_projection against the real lock: 16 rows, 83 corruptions refused.
- `build_v110.py` reruns produce the same bytes.

## Decide

- Does X2d implement item 7 exactly? In particular:
  - N only from R's ACTIVE row (R0 or R2);
  - the namespace and both carriers confirmed under custody;
  - S7's three modes, nonblocking, in level order;
  - partial failure releasing every taken lock in reverse order before the fence;
  - no lease without the fence, no wait, no upgrade, and EXCLUSIVE only with both locks;
  - item 6a before any lease;
  - the fence never released by X2d;
  - `FencedNamespace` holding the lease, the row snapshot and the root admission.
- Is the target a sound seam for X3b's floor step (fence held, R current, no project lock), without X2d composing it?
- Rule on the judgment calls, in particular 2, 3, 5, 6 and 7.
- Is v110 right on v105?
- Is anything else wrong?

review.json must contain:
- "verdict": `ACCEPT-UNIT` or `REQUIRED-FINDINGS`;
- "requiredFindings";
- "subjectManifestSha256": the sha256 of `namespace-lease-x2d-inventory-v110-subject.json` (lead's value `4ba60b8b47529cfe8fed82b809570918e9a48ae5be38e1f2a7ca4dd4ecc869f8`);
- "inventoryCandidateAssessment": {verdict, requiredFindings, path, bytes, sha256 of v110, parent (the v105 pin), successorRecord (the pin of `namespace-lease-x2d-inventory-v110/successor.json`)}.

Write REVIEW.md and review.json. Do not commit.
