# X6 r3, X7 r4, X9 r2

Claude Opus 5.5 leads. Grok is the single reviewer. Law review; no product cargo. Git was read-only. `~/Library/Application Support/OpenSIP` is absent. The private 413 fixture was not read.

| Law | Verdict | Live PROPOSAL.md | Preserved predecessor |
|---|---|---|---|
| X6 r3 | ACCEPT | `e57aef34213341ec97ef5ca9e7515bccf0469c6b1e3416d9b0c6883c9054f700`, 23197 bytes | `carrier-recovery-x6/PROPOSAL-r2.md`, `c81b939bc4f633265eb124df8c3445c3cb6fa0508515bae49ad114e6d175ddf4`, 15834 bytes |
| X7 r4 | REQUIRED-FINDINGS (RF-1 only) | `e28669d92dd5d6afc539b3c800dc5d3150ca34a96132079b6e8b0d8146dc921c`, 22037 bytes | `finalization-x7/PROPOSAL-r3.md`, `aa390f820472807235b3414122e1df2c2d9e3b7ec9452d849bd3e17aa1aa1c3e`, 17625 bytes |
| X9 r2 | ACCEPT | `b9b254c37599cb8adaf99fea666a062b24abad2a7edf236a516e74a07f05a9a9`, 55703 bytes | `crash-matrix-x9/PROPOSAL-r1.md`, `325ccd7524c90d0611f6b4aabcd4549d5029dc7e901245cb552afcac5cd38d82`, 50022 bytes |

Each snapshot sha256 equals the `subjectSha256` of the review that accepted it (`reviews/grok-x5r2-x6r2-x2r6/x6/review.json`, `reviews/grok-finalization-x7-r3/review.json`, `reviews/grok-crash-matrix-x9-r1/review.json`). The acceptance note lives in the live file. The snapshot is the accepted bytes.

X8 r3 item 5 B4 needs no amendment. See the last section.

## Why the contradiction is real

X1 r1 item 1 gives a process one attempt and therefore one receipt. Item 7 gives that process one entry, chosen from the creator, `admit_ordinary_writer`, or a 458c read entry. A second entry ends as `Invariant`. 458c r6 item 1 is the same rule the request calls r5: the attempt is the invocation's one charged act, one producer, and no second producer. The live 458c file is r6; r6 amended items 10 and 12, and item 1 still holds.

The writer's invocation has already spent that receipt on the write entry. It cannot also call `produce_read_platform` or open a 458c read session. X6 r2 item 6 had the host call `recover` on `ExistingAttempt` inside that invocation. X7 r3 item 4 had the delivery phase read through that same read session. Both are impossible under X1. The narrow fix is the one these amendments take. Handing the spent write receipt back out of `StoppedSession::finish` would change X3d item 7 and X1 item 1, and that alternative is rightly rejected.

## X6 r3 — ACCEPT

The amendment is narrow and matches the items the header names. Items 4, 5, 7, 9, 10 except F34's line, and 11 stay as r2 left them.

Item 6 is the lawful routing. `ExistingAttempt` is never recovered in the writer's invocation. It stays on X3d item 9's invariant row (`operational-failed`, `SYSTEM.OUTCOME.ILLEGAL_STATE`, `host-invariant`, `HOST.INVARIANT_VIOLATED`). Finalization discloses the ExecutionId as subject and the four requested-binding members, and the remedy names a later read-only recovery. A later read-entry invocation admits `recover` on a `RecoveryRequest` carrying that binding. Each member is compared exactly with the admitted binding and the snapshot's attempt row. A difference, or no attempt row against which to compare `operationRef`, is `BindingUnusable` (`RECOVERY.REFUSED`) with the first differing member as subject (`store-generation`, `namespace`, `carrier`, or `operation`). The same binding yields the attempt's standing. That supersedes X3d item 9's "before X6 exists" and meets X3d item 3 step 5 by disclosure plus a later invocation. `CommitUndetermined` is recovered later with a plain request (ExecutionId and namespace). X6 does not restate the finish-reconciliation parenthetical that X7 still carries.

Item 1 puts `RecoveryAdmission`, `RecoveryRequest`, and `RequestedBinding` in security, because the walk, registry capture, endpoint values, and lease carriers are security-private. Storage's `recover` consumes the admission. Moving those owners into storage is rightly rejected.

Item 2 makes `RequestedBinding` a public inert value with four checked members. Storage builds `NotPrepared::ExistingAttempt { execution_id, requested }` from the plan it was about to write. `RecoveryRequest` has two checked constructors: plain ExecutionId plus namespace, or ExecutionId plus `RequestedBinding`. Public `admit(request)` produces the process's one read receipt. The `&mut ReadPremiseReceipt` form stays crate-private for tests. A process that already entered refuses `Invariant` at receipt production. Recovery is one of X1 item 7's read entries.

Item 3 step 3 uses the request namespace id only as a selector. Exactly one registry row with that `namespaceId` and status ACTIVE supplies N, and N is that row's own `namespaceId`. No row, another status, or more than one row is the unregistered-namespace refusal, before any lease. The digest of (N, S, G, K) and SHA-256(N) are computed from admitted values. `RequestedBinding` is compared and is never an input. Mapping those three registry failures onto the existing unregistered refusal is fail-closed and matches the owner's "never from more than one row". The subject `namespace` is often unreachable when the selector is the binding's own `namespaceId`, and it still belongs in the comparison so the F27 subject list stays complete.

Item 8's unregistered-namespace row is request-rejected, `EXTENSION.ADMISSION_REJECTED`, detail `RECOVERY.REFUSED`, subject `namespace-unregistered`. `RECOVERY.REFUSED` is already in both `public-detail-registry.json` copies and in `common.v4.schema.json`. Owner §1's binding-unusable row is request-rejected / `EXTENSION.ADMISSION_REJECTED` / `RECOVERY.REFUSED` with a typed subject, and the owner already uses `RECOVERY.REFUSED` for a refused recovery request. The new subject tokens are free-form subjects under that existing detail. `diagnostic-routes.json` subjects are free text. No new public code or detail.

Item 12 restates X6b as security, storage, and host, including X9's `after-lease` and `after-ledger-snapshot` points. The forbidden substitutes add `recover` in a writer's invocation, a non-`<Read>` receipt, and N taken from a request field or from more than one row. The fence-free SHARED-READ lease remains X2's one exception: `readers.lease` `LOCK_SH|LOCK_NB`, never `writer.lease`, never upgraded, busy returns `UnavailableBusy`.

The F34 "no attempt row" refusal is the `RequestedBinding` comparison, which cannot confirm `operationRef`. The plain-request matrix still projects `unknown-attempt-unobserved` and its neighbours on the rows item 8 already has. That distinction holds.

Rejected, and rightly: settling from the writer path (owner §5); handing the spent write receipt back from `finish`; recovering before `finish` under the live writer session and lease.

Disclosed, and not findings. The written-under line still names X3d r3, 458c r6, and X2 r6. The operative items cite the rules that still hold. X2 r8 item 7 still says the recovery lease's admission is "X6 r2 item 3's", while X6 r3 step 4 still cites "X2 r6". The exception itself is unchanged, so neither citation needs an amendment in this round. X3d r6 item 6 still spells `ExistingAttempt { executionId }` without `requested`. X6 owns the routing X3d deferred, storage builds `requested` from the plan, and X7a adapts the match. No X3d amendment is required here.

## X7 r4 — REQUIRED-FINDINGS

### Item 4 is accepted

Owner §6.2, for an unlatched ordinary commit (state 1), runs required rendering and delivery as a separate `SHARED-READ` phase over the committed snapshot, drawing no authority from the returned stopped cleanup-only session. The handoff is commit confirmed, stopped session returned, cleanup `REV`/`CLN` while that session holds the operation lease, release the lease, S7 end handoff, then the delivery phase. After a latch (state 2 or 3) the host starts no new required-delivery phase.

r4 keeps that order, starts no delivery after a latch, and draws no authority from the stopped session. M2's required delivery projects the `PublishedCommit` (the exact committed receipt bytes and the RunId, built only after evidence `COMMIT` succeeded) and the evaluation whose replay produced the committed Run. Those bytes are the committed snapshot this invocation already holds. `finalize` lends the phase `&PublishedCommit` only. The phase takes no lease, no receipt, and no read session. `SHARED-READ` is the owner's way of reading a snapshot the process does not already hold. This process cannot produce a second receipt, so the mode word cannot be met by a new 458c session inside the writer. Meeting "over the committed snapshot" with the bytes already held is lawful for M2. A later surface that must read the store (M3/M4 artifact publication, HTML, SARIF) is a later read-entry invocation under its own law.

Rejected, and rightly: delivery under the writer lease; delivery inside the writer's session before `finish` (same lease hold, and it reverses §6.2's order); reading through the write receipt after `finish` (`finish` consumes it, and keeping it would change X3d item 7 and X1 item 1); deferring every required delivery to a later invocation (the committing invocation would never deliver its Run, and F16 would describe another process).

Items 7, 10, and 11 withdraw the read-session ledger line. The phase renders in-memory values and charges no ledger. The tests pin the `ExistingAttempt` row and a source check that `finalization.rs` admits no call into 458c read entries, X2 leases, or storage readers. The X7a note (in flight, inventory v125) limits that unit to the `ExistingAttempt` arm, item 5's namespace disclosure, and the `DeliveryPhase` comment. The trait (`render(&PublishedCommit)`, `output()`, `optional(&PublishedCommit)`) and the `finalize` order stand. Whichever of X6b and X7a integrates second adapts the match to `NotPrepared::ExistingAttempt { execution_id, requested }`. Forbidden substitutes cover calling `recover` for this invocation's `CommitUndetermined` or `ExistingAttempt`, and a store read, lease, receipt, or read session in the delivery phase.

The item 3 row matches X6 r3: invariant row, ExecutionId subject, four binding members disclosed, remedy naming a later recovery, no recovery in this invocation, exit 4, no `runId`. The intro still says the table uses X3d r3 item 9's rows unchanged. The codes on the new row are that invariant row. The disclosure is the amendment. That sentence is disclosure, not a finding.

### RF-1. Item 5 still describes the withdrawn finish reconciliation

Item 5 still says: "It finishes the stopped session (X3d item 7 reconciles under the lease and copies the floor only on OK, REVERT or ADVANCE)." r4 adds the namespace disclosure in the same paragraph and leaves that parenthetical.

`CommitUndetermined` is the uncertain outcome (journal, attempt-admission `COMMIT`, or evidence `COMMIT`). X3d r6's header records that this parenthetical describes r4, and orders X7's next revision to replace it with "finish appends nothing and copies no floor; the next writer reconciles". X3d r6 item 7 is that rule: after an uncertain outcome, `finish` appends nothing, does not reopen the carrier, does not run `reconcile_witness`, copies no floor, and releases the lease. The next writer's floor step and carrier start reconcile. r6 widens "appends nothing" to every uncertain `COMMIT`, and the settlement reserve is forfeited when the outcome is classified. The end step does not run.

An implementer who follows the parenthetical reconciles or copies a floor under the lease after an uncertain outcome. That work is charged to an attempt ledger the failure has already closed, and X3d forbids it.

Required fix, and only this: replace the parenthetical with X3d r6's sentence. Keep "finalization never calls `recover` in the same invocation". Keep the r4 sentence that discloses the namespace id as the later plain request's selector. Leave item 6's certain, ledger-open capacity path as written: there `finish` still appends any pending `REV` or `CLN` under the operation lease. The older `recover(executionId)` phrase plus the new namespace sentence together name X6's plain request. That is not a second finding.

## X9 r2 — ACCEPT

The header restores the written-under bullets that r1's acceptance note had split, and records the acceptance in its own paragraph. The snapshot `PROPOSAL-r1.md` is the clean accepted bytes. The r1 review records no acceptance date, so the stamp "2026-10-02" is not contradicted by that file. No further header edit is required.

F34 follows X6 r3 item 6 and X7 r4 item 3. Run A (`inject-id`) ends on the invariant row, discloses the ExecutionId and the binding, calls no `recover`, writes no new row and no SEAL, and leaves the earlier attempt's rows unchanged. Run B is a separate `recover` process. A's binding, whose `operationRef` differs, is `BindingUnusable` with subject `operation`. The earlier attempt's own binding yields that attempt's standing. B leaves `normalizedSha256` unchanged. Ladder R1 is its own process and read entry, with a plain `RecoveryRequest` naming the run's namespace. The subject spelling `operation` matches X6's member name. X9 adds no new public code. The forbidden substitute "recover inside F34's injected writer" matches X6. F34 cites X7 r4 item 3, so this acceptance does not depend on the item 5 parenthetical.

The clock amendment is a lawful test-only substitution, and it closes EXIT-PLAN's open "X9 clock dependence". Since X4a, a fenced first read publishes a floor when tEval exceeds the stored F (X4T item 7: tEval = max(F, W, A); when tEval exceeds stored F, or L or the anchor advance, publish under the held fence before the view returns, F := tEval). Whole-second wall time is how that comparison moves between lawful runs, which is why `x4t.floor-publication` counts and trust-store bytes varied (34 against 39 creates). X4T r11 changed item 4's revocation root. Item 7's write-ahead is the same rule. `CLOCK-REGRESSION` and `TRUST.FLOOR_AHEAD_OF_WALL` stay findings carried in the view. Only the fenced first read admits time. Monotonic bounds stay on the native clock.

Under the crash-matrix feature and `OPENSIP_X9_CLOCK=<E>:<k>`, `opensip_platform::observe_clock` takes wall readings from the script. Monotonic readings and boot identity stay native, so the 468 fence wait, S7 backoff, X4 freshness, and item 11's timing guard are unchanged. Without the variable, or without the feature, the wall reading is the OS. E is `clockEpoch` in `required-runs.v1.json`, inside every synthetic validity window. k is the process ordinal (parent numbers children 0, 1, 2, … in spawn order; the fixture child is 0). The n-th wall reading, n from 0, is `E + 3600·k + n` seconds with zero nanoseconds. Readings increase within a process and across ordinals. A 3600th reading is `HARNESS-ERROR`, so process k's last successful reading is n = 3599 and process k+1 starts a full hour later. The parent takes no wall reading. The fixture child driver `fixture`, ordinal 0, builds item 6's synthetic installation under the script, so no stored floor or trust time comes from the OS. Later children therefore see W past any floor the fixture wrote, and publication is deterministic. Runs carry `scripted-clock` beside `synthetic`. Records carry the child's ordinal and `"clock": {"epoch": E, "script": "x9-ordinal-3600"}`. Two census runs on one commit are equal point for point; a difference is `HARNESS-ERROR`. Repetition agreement includes `logical.trustState` together with `normalizedSha256` and the trace digest. `normalizedSha256` still replaces wall-clock data by appearance-order placeholders. X9-1 places the platform site (feature-only, under item 2's guards, listed with the crash_barrier module), the fixture driver, the label, and the census equality check.

Rejected, and rightly: comparing the trust store per publisher run (the kill set would still depend on timing, F00's X4T floor kills would need a wait, which item 3 forbids, and trust publication would leave the repetition check); freezing the clock (later fenced reads would publish nothing, which production does not do, and expiry could never pass).

Disclosed, and not a finding. The written-under list still names X6 r2, X7 r3, and X4T r9. The body follows X6 r3 and X7 r4, and the clock paragraph cites "X4T r9 item 7", whose write-ahead text is the r11 item 7 rule above.

## X8 B4 — no amendment

X8 r3 item 5's B4 row expects `ExistingAttempt`, then the invariant row until X6 routes it. The planted row stays unchanged and alone, with no SEAL. The owner is X3d-2 / X3c. Under X6 r3 the invariant row is the writer's permanent projection, so B4's expected termination and census are the values the row already states. The clause "until X6 routes it" is now moot commentary. X8 also says F34's routing is not an X8 owner row. No X8 amendment is needed.

## What was checked and left standing

- Owner §1 binding-unusable, the refused-recovery use of `RECOVERY.REFUSED`, step 0's unregistered-namespace refusal, and step 2's mismatch rule.
- Owner §6.2's handoff order and the no-authority rule on the stopped session.
- X2 r8 item 7's single fence-free SHARED-READ exception.
- X4T r11 items 6 and 7 for the scripted wall clock.
- Both public detail registries for `RECOVERY.REFUSED`, and the operational-failed `SYSTEM.OUTCOME.ILLEGAL_STATE` route. No new public code.
