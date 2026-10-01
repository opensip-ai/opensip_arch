# Review: native current-trust admission X4T r1

Verdict: REQUIRED-FINDINGS.

Subject `docs/implementation/m2/trust-admission-x4t/PROPOSAL.md` is 17029 bytes, sha256 `131c59273fd48670c7174f4e33c8e43d8dc6d949fab92f3453c249dcf60baf91`, matching hashes.txt. Product HEAD is `f7acb6d7f8acadcbc0bf81d141f39077d817f043`. The real OpenSIP support directory is absent. No product cargo.

The live X4 text is r3. It says it aligns with this law. X4 r2 is `PROPOSAL-r2.md`. X3b's current text is the r2 revision. This review judges X4T against those texts and does not reopen them.

## What holds

Items 1 and 2 are sound. `AdmittedCurrentTrust` is a private borrowed view: the head, the closure the head names, authentication, revocation, the merged policy, the time admission, the S6 epoch, and the role states. It grants nothing. A P0 capsule plus the embedded root list is not a substitute. The read is by reference from the retained store and collection handles, each file at its owner's cap. That cap is 4 MiB: `trust::metadata::MAX_BYTES` and `retained_metadata_index::CAP` are both `4 * 1024 * 1024`. There is no census. `native_current::capture_head` remains a supplied-path provisional image.

Item 3 is sound. 463 authenticates the running release from the embedded root chain and the embedded revocation. X4T authenticates the installation from the accepted installation root through `trust_ordinary_roots::authenticate_shared`, evaluates a recorded chain N+1..M under S5, and reverifies every accepted envelope. The embedded root does not stand in for the installation root. Requiring the accepted core closure to equal the running core is the check X3a already joins.

Item 6 is sound. S4 runs on the fenced first read through `trust_time::evaluate_retained_ordinary`. `CLOCK-REGRESSION` and `TRUST.FLOOR_AHEAD_OF_WALL` are findings. Observer rereads do not re-admit wall time and do not write a floor. Advancing the handoff's tEval by elapsed sleep-inclusive monotonic time, and stopping on a boot change, is the evaluation that can run without the fence.

Item 8 is sound. The fenced first read uses the decoded `state.v1` and full sample X3a already retains. The dependency closure is new reading.

X4B is correct and correctly scoped. Until a role is `Trusted`, this law refuses the view. S4 step 2 is the first acceptance of the embedded bootstrap payload, and no unit in this law performs it. The M2 exit matrix runs on synthetic stores whose roles are already `Trusted`. EXIT-PLAN places X4B on X4T and before X11, which is the first creator command surface. Doctor trust reports stay unclaimed.

The carrier-floor split is sound. X3b's floor is `{highWaterSchema, projectKeyDigest, grantGeneration, lastSeq, tailSha256}` and records no trust epoch. Comparing F, L, root version, revocation version, and index snapshot version with SC-TRUST's own retained floors matches S6: a lower counter never revokes. `trust-rollback` is a lawful new subject of the existing `CONFIG.CUSTODY_REFUSED` row (request-rejected, exit 2, `CONFIG.INVALID`). It is not a new code. That subject is the handoff row.

`CONTINUE-CORE-NOT-TRUSTED` is a registered code, class request-rejected, exit 2, `EXTENSION.ADMISSION_REJECTED`. `TRUST.NO_ADMITTED_TIME_CONTEXT` is the S4 step 2 code, class request-rejected, exit 2, `REQUEST.PRECONDITION_FAILED`. Those classes are right for the cases named below; the role routing is not.

## Required findings

### RF-1 — The floor publication runs inside the handoff that already holds the lease

Item 9 puts the fenced admission, including item 7's write-ahead, inside X2's item 7a handoff. That handoff joins `FencedNamespace`. X2d has already taken the project lease, and the fence is released only at the end of the handoff. Item 7 then publishes a new capsule, its event and descriptor, and `state.v1`. Those are trust state. S7 writes trust state only under the fence and never under a lease.

X3b's carrier floor is written under the fence with no project lock, before X2d takes the lease. Only the carrier start, which writes namespace files, belongs inside the handoff. X4T's publication is the S4 trust floor, so it belongs with that pre-lease fence hold.

Failure scenario: item 7 of X2 takes the lease. Item 7a then runs this admission and publishes `state.v1` while the lease is held. S7 forbids the write. Skipping the write to satisfy S7 returns a view at a tEval whose floor was not written ahead, which S4 step 5 forbids.

The fenced admission, including the write-ahead, runs under the installation fence before X2d takes the lease. No project lock is held. The monitor's first read brackets that admission. Item 7a does not publish trust state.

### RF-2 — A later recheck rejects a lawful newer state.v1

Item 7 advances the retained `state.v1` owner only through this admission's confirmed publication. That part matches X2's publication rule. The next sentence applies the rule to every later recheck: any other change fails as `required-files-changed`.

Item 9 admits a newer `state.v1` published by another writer and leaves revoke, drift, and rollback to X4's S6 predicate. X4 r3 item 4 makes the old current-trust captures provenance after the fence release. The publication rule covers fenced rechecks before that release. It does not cover the observer.

Failure scenario: after this operation releases the fence, another writer publishes a higher revocation. The observer opens the new `state.v1`. Item 7 fails the recheck as `required-files-changed`. The predicate never sees the new epoch, so a revoking update and an unrelated update stop the operation the same way.

Fenced rechecks before the release compare with the owner this publication confirmed. After the release that capture is provenance. A newer pointer is admitted. A lower F, L, root version, revocation version, or index snapshot version than the retained SC-TRUST floors is `trust-rollback` at the handoff. An observer rollback or a second mixed view is X4's `OBSERVER.FAIL_STOP`, not this custody row and not `installation-incomplete`.

### RF-3 — The unfenced retry is nested, and a second mixed view has two rows

Item 9 opens `state.v1` at the start and again at the end, retries once from the new head, and stops on a second mixed read. It cites X4 r2 item RF-3. That r2 paragraph repeats the observation once within the tick. X4 r3, which is the text that aligns with this law, puts both attempts inside one `FreshnessMonitor::read` callback, because a second `read` call latches on the first error. Item 13 gives item 9, including that retry, to X4T-a. X4 r3 item 5 also retries, by repeating the steps that call X4T's admission.

Item 10 terminates a pointer that changes twice as `installation-incomplete` (`CONFIG.CUSTODY_REFUSED`, exit 2). Item 9 terminates the same event as an operation stop. X4 r3 terminates it as `OBSERVER.FAIL_STOP` (exit 4, `HOST.IO_FAILURE`). The per-observation ledger is sized at exactly two views.

Failure scenario: one atomic replacement lands during the first attempt. X4T retries internally, then X4 repeats the admission because its own reopen still differs. Four views are charged to a two-view ledger, and the tick fail-stops on budget. If the outer repeat is a second `read` call, the monitor latches on the first error and the same lawful replacement stops the operation. The termination, if it is item 10, is exit 2 `installation-incomplete` rather than the observer fail-stop.

X4T's unfenced reread is the body of that one callback: one retry, at most two views, and a second mixed view returns the error X4 latches as `OBSERVER.FAIL_STOP`. X4T does not wrap that body in another retry and does not call `read` again.

### RF-4 — Unbootstrapped and Expired use the wrong rows

`role_machine::continuation` refuses when the core is not `Trusted` (`CONTINUE-CORE-NOT-TRUSTED`). When the core is `Trusted`, an index in `Unbootstrapped`, `QuorumLost`, `Revoked`, or `Recovery` is `ContinueIndexNotTrusted`, and a component that is not `Trusted` is `ContinueComponentNotTrusted`. Neither index nor component code is in the public registry or the D9 table. An index in `Expired` or `StaleRevocation` is `ExistingOnly`: an existing verified process may continue, and a new process is not granted. Clock evaluation moves `Trusted` to `Expired` without a root-chain refusal. S5's `ROOT.EXPIRED_NO_CHAIN` and `ROOT.FINAL_EXPIRED` are the chain evaluation's own results.

Item 10 sends every `Unbootstrapped` role to `TRUST.NO_ADMITTED_TIME_CONTEXT`, and every `Expired` role to the S5 row. `Revoked`, `StaleRevocation`, `QuorumLost`, and `Recovery` all publish `CONTINUE-CORE-NOT-TRUSTED` with the state name as the subject.

Failure scenario: the core is `Trusted` and F is present. `TR-INDEX` is `Unbootstrapped`. The row is `TRUST.NO_ADMITTED_TIME_CONTEXT`, and the remedy asks for time evidence the installation already has. The index was never accepted. In the other direction the chain succeeds and the index is `Expired` because `catalogExpiresAt` is at or before tEval. Item 10 emits `ROOT.EXPIRED_NO_CHAIN` or `ROOT.FINAL_EXPIRED`. The root is current, and the remedy asks for a successor root.

`TRUST.NO_ADMITTED_TIME_CONTEXT` is only S4 step 2: F absent, no accepted bootstrap. That is the P0 case and X4B's precondition. A non-Trusted role while F is present uses that role's continuation. The core's code is `CONTINUE-CORE-NOT-TRUSTED`. The index and component keep the registered class of that continuation, and the subject names the role. They are not published as a core failure that names only the state, and they are not S5 root codes. S5 `ROOT.*` remains the chain evaluation's refusal and names the link. `CLOCK-EXCURSION-FORWARD` keeps both S4 subjects, `in-session` and `beyond-horizon`.

### RF-5 — The view ceiling does not cover the closure that sets it

Item 11 bounds a view by one head, one descriptor, six role records, and at most three accepted documents, plus a root chain "bounded by its own counter range." Each of those files is readable at 4 MiB. Eleven files at that cap are 44 MiB before any chain link past the accepted root. The ceiling is 32 MiB, and the per-observation ledger is twice that. `rootVersion` is admitted from 1 through `i64::MAX`. `verified_root_chains` refuses only when the chain exceeds the caller's `ChainBudget.max_links` and `max_stored_bytes`. This law never sets that budget. The synthetic five-link measurement is smaller than the closure the ceiling claims to bound, so a passing test does not show that a lawful view fits.

Failure scenario: the six role records, the descriptor, the head, and the accepted root, revocation, and policy are each just under 4 MiB, and the chain adds one link. The view's own caps admit every file. The charged bytes exceed 32 MiB. Admission refuses `WORK.BUDGET_EXHAUSTED`, and no operation can start. A longer chain, still inside an unset link budget, exceeds the 1024-object ceiling the same way.

Name the finite `ChainBudget` the root verifier requires. Size `TRUST_VIEW_COST` to the closure at each file's cap, including that chain, or lower those caps until they fit the ceiling. The X4T-a test still pins a measured view at or under the ceiling. A view over the ceiling refuses, and it is not truncated.

### RF-6 — The epoch's policy digest is not identified

Item 5 puts the merged policy's canonical digest in `permissionPolicyDigest`. `trust_policy::merge` returns two different 32-byte values. `Effective::digest` is the domain-separated hash `opensip.metadata.policy-effective.1` over the canonical bytes. The policy fixture separately records the raw SHA-256 of those bytes. S6 compares the epoch field with itself. The two hashes do not compare equal.

Failure scenario: the handoff stores the raw SHA-256. The reread stores `Effective::digest`. The bytes differ while the policy is unchanged. The predicate treats the difference as a policy change and revokes the operation, or the other way around and misses a real change.

The epoch stores the digest `merge` returns, on both the start read and the reread.
