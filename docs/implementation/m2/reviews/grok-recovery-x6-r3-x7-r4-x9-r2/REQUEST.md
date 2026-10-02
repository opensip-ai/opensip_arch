Grok review, three law amendments together: X6 r3, X7 r4 and X9 r2. Claude Opus 5.5 leads. You are the single reviewer. No repository edits, commits, pushes or delegation. Write only under /tmp/opensip-implementation/reviews/grok-recovery-x6-r3-x7-r4-x9-r2. Law review; no product cargo. Run git only read-only. Never touch the real home (`~/Library/Application Support/OpenSIP` must stay absent) and never read the private 413 UUID fixture.

Pins are in hashes.txt. Each accepted predecessor is preserved byte for byte without its "ACCEPTED" note, and each snapshot's sha256 equals the subjectSha256 of the review that accepted it:
- `carrier-recovery-x6/PROPOSAL-r2.md` = X6 r2, `c81b939b…` (`reviews/grok-x5r2-x6r2-x2r6/x6/review.json`);
- `finalization-x7/PROPOSAL-r3.md` = X7 r3, `aa390f82…` (`reviews/grok-finalization-x7-r3/review.json`);
- `crash-matrix-x9/PROPOSAL-r1.md` = X9 r1, `325ccd75…` (`reviews/grok-crash-matrix-x9-r1/review.json`).

Diff each PROPOSAL.md against its snapshot.

## Why: a contradiction found while starting X6b

X6 r2 item 6 has the host call `recover` on X3d's `ExistingAttempt`, with X3d's requested binding, which exists only in the writer's own invocation. Items 2 and 3 admit recovery on the read receipt (458c-a). X1 r1 item 1 ("A process produces at most one, because the attempt is the process's one attempt") and item 7 ("One entry per process … a second entry ends as `Invariant`") make that impossible: the writer's process has spent its one attempt on the write receipt. At product 81214cb, `ATTEMPT_ALLOCATED` (`crates/security/src/initial_installation.rs`) is swapped once and never reset, `produce_read_platform` then fails `AlreadyAllocated`, and `StoppedSession::finish` returns only `SessionEnd`. X7 r3 item 4 has the same defect: its delivery phase reads "through the read session (458c)" in the writer's invocation. The coordinator took the narrowest fix as a lead decision; the larger alternative (finish handing back a spent write receipt, changing X3d item 7 and X1 item 1) is recorded as rejected. X9 r2 also settles EXIT-PLAN's open "X9 clock dependence" finding.

## X6 r3 (diff against PROPOSAL-r2.md)

- **Item 6 (F34).** `ExistingAttempt` is never recovered in the writer's invocation. It stays on X3d item 9's invariant row; finalization discloses the ExecutionId (subject) and the requested binding with a remedy naming a later recovery. A later read-entry invocation's `recover` takes a `RecoveryRequest` with that binding and compares each member exactly with the admitted binding and the snapshot's attempt row: any difference, or no attempt row, is `BindingUnusable` with the differing member as subject; the same binding gives the attempt's standing. This supersedes X3d item 9's "before X6 exists". `CommitUndetermined` is recovered later with a plain request (ExecutionId and namespace).
- **Item 1.** The custody half of admission (`RecoveryAdmission`, `RecoveryRequest`, `RequestedBinding`) is security's, because the walk, registry capture, endpoint values and lease carriers are security-private; storage's `recover` consumes it.
- **Item 2.** `RequestedBinding` (four checked members, inert). `NotPrepared::ExistingAttempt { execution_id, requested }`, built by storage from its plan, never from a read. `RecoveryRequest`'s two constructors. Recovery is one of X1 item 7's read entries: the public `admit(request)` produces the process's one read receipt; the `&mut ReadPremiseReceipt` form stays crate-private for tests.
- **Item 3 step 3.** The request's namespace only selects: exactly one row with that `namespaceId`, ACTIVE; N is that row's. Otherwise the unregistered-namespace refusal, before any lease.
- **Item 8.** Unregistered namespace: request-rejected, `EXTENSION.ADMISSION_REJECTED`, `RECOVERY.REFUSED`, subject `namespace-unregistered` (owner §1's "refused recovery request"; no new code or detail).
- **Item 12.** X6b restated (security, storage and host), including X9's `after-lease` and `after-ledger-snapshot` points. Forbidden substitutes gain `recover` in a writer's invocation, a non-`<Read>` receipt, and N from a request field or from more than one row.

## X7 r4 (diff against PROPOSAL-r3.md)

- **Item 3.** The `ExistingAttempt` row is X6 r3's: the invariant row, the ExecutionId as subject, the four requested-binding members disclosed, a remedy naming a later recovery; no recovery in this invocation.
- **Item 4 (lead decision).** The delivery phase reads nothing from the store. It projects only the `PublishedCommit` (built only after the evidence `COMMIT` succeeded) and the evaluation the invocation holds, which are the committed snapshot's bytes. No lease, receipt or read session; `finalize` lends the phase `&PublishedCommit` only. A future surface needing a store read (M3/M4) is a later read-entry invocation under its own law. Rejected: delivery inside the writer's session before `finish` (the lease hold, and it reverses owner §6.2's order); the write receipt's lending after `finish` (`finish` consumes it; would change X3d item 7 and X1 item 1); deferring all required delivery to a later invocation (a committed Run never delivered by its own invocation, and F16's row would describe another process). Please judge whether "over the committed snapshot" in owner §6.2 is met by in-memory bytes equal to the committed ones.
- **Item 5.** The namespace id is disclosed beside the durability row, as the later recovery's selector.
- **Items 7, 10, 11 and forbidden substitutes.** The read-session ledger line is withdrawn; tests for the `ExistingAttempt` row and a no-store-read source pin; a note on X7a (in flight, v125): only the `ExistingAttempt` arm, item 5's disclosure and the `DeliveryPhase` comment change; its trait and `finalize` order stand.

## X9 r2 (diff against PROPOSAL-r1.md)

- **Header.** r1's "ACCEPTED" note had been inserted mid-sentence in the "written under" line; r2 restores the sentence and records the note in its own paragraph.
- **F34's row.** Run A (`inject-id`): `ExistingAttempt` on the invariant row, ExecutionId subject, binding disclosed, no recover, no new row or SEAL. Run B, a separate `recover` process: with A's binding (different `operationRef`) BU, subject `operation`; with the earlier attempt's own binding, its standing; B leaves `normalizedSha256` unchanged. Ladder R1 is its own read entry with a plain request.
- **The clock (lead decision; items 3, 5, 6, 7, 12).** Since X4a a fenced first read publishes a floor only when the whole-second wall clock passes the stored F, so `x4t.floor-publication` counts and trust-store bytes vary between lawful runs (34 vs 39 creates). Chosen: a scripted wall clock under the feature and `OPENSIP_X9_CLOCK=<E>:<k>`: the n-th wall reading of the process with ordinal k is `E + 3600·k + n` s; monotonic readings and boot identity stay native, so every monotonic bound is unchanged. The fixture is built by a new `fixture` child (ordinal 0) under the script; the parent takes no wall reading. Runs carry a `scripted-clock` label and the record's clock; two census runs must be equal; repetition agreement includes `trustState`. X9-1 places the platform site. Rejected: comparing the trust store per publisher run (the kill set would still depend on timing, F00's X4T floor kills would need a wait, and trust publication would leave the repetition check), and freezing the clock.

## X8 B4 (no amendment)

X8 r3 item 5's B4 expects "`ExistingAttempt`, then the invariant row until X6 routes it". Under X6 r3 the invariant row is permanent in the writer's invocation, so B4's expected values are unchanged; only its "until X6 routes it" is now moot. Please confirm no X8 amendment is needed.

## Decide

For each law: is the amendment lawful and narrow, consistent with X1 r1 items 1 and 7, 458c r5, X3d r6 items 3, 7 and 9, X2 r8 item 7, owner §1, §2 and §6.2 of `commit-recovery-readonly.v3.md`, and X4T r11 item 7? Are the rejected alternatives rightly rejected? Is anything else wrong?

Write one REVIEW.md, and three verdict files: `x6/review.json`, `x7/review.json` and `x9/review.json`. Each must contain "verdict" (ACCEPT or REQUIRED-FINDINGS), "requiredFindings", "subjectSha256" (that law's PROPOSAL.md), and the preserved snapshot's path, bytes and sha256. Do not commit.
