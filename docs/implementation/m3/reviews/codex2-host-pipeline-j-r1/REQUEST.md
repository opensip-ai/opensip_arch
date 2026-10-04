CODEX2 review: M3-J1 r1, the guarded durable host pipeline. This is a **law and method-soundness** review, round 1. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-host-pipeline-j-r1.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs. A timing-sensitive crash-matrix rerun is using this machine; do not run any lead set.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`. The subject file is untracked in arch until acceptance.
- `docs/implementation/m3/host-pipeline-j/PROPOSAL.md`, the law. It is the subject of `subjectSha256`.

**The unit.** M3-J1 is the law row of M3-J in the accepted M3 plan (`docs/implementation/m3/M3-PLAN-r4.md:168`, the r4 bytes). The live `M3-PLAN.md` is draft r5, with the row at `:211`. J1 follows r5's P5-1 and P5-2 assignments (the resume writer to J-RW and J4; re-commit to X3c r8 and X3c-3). The row asks for four things:
- the X11 successor (X11:64-81);
- the invocation DAG (WS:76-256) as M3 implements it;
- the backup-status successor;
- the commit-phase cancellation join S-OP-12, with the X3D and X7 owners (OPP §5.5, §9).

**Governing and dependent records, and their status:**
- **Accepted:** X11 r1; X3d r8; X7 r6; 464 r2; 468 r5; X1 r1; X2 r9; X3a r5; X4 r7; X4B r5; X4T; X5 r3; X9 r16; M3-B r2; M3-I1 r2; the operability plan r3; M3-PLAN r4.
- **In review:**
  - X12 r4, which carries the first-use clause J1 implements (`m2/reviews/grok-policy-admission-x12-r4`, ASSIGNED);
  - M3-C, cited by its r4 bytes (`snapshot-plan-c/PROPOSAL-r4.md`, reviewed in `reviews/codex2-snapshot-plan-c-r4`). The live file has moved to draft r5;
  - S-OP-2 r4 (`reviews/codex-s-op-2-r4`).
- **Draft, not sent:** M3-L r1.

J1 cites M3-C and S-OP-2 by the pinned bytes' lines. If either changes before you finish, judge against the pinned bytes and note the drift.

**The product** is `/Users/sb/code/opensip-ai/opensip` at main `3e64266`, read-only. The law's product citations were read at that commit.

## What the law decides

1. **No command goes live in the binary at M3 (item 1).**
   - The four creator-class words keep X11 r1's refusals, and X11a's pins keep passing.
   - A host-library entry runs `default` and `analyze` durably, and `analyze --ephemeral`, for tests and the internal harness.
   - `fit` and `audit` are not at M3. The M4 CLI unit wires the binary.
2. **One RequestId per invocation (item 2).** It is minted at ingress and lent to the creation intent through a sealed `RequestIdentity` (a 464 r3 successor). The ExecutionIds are:
   - the creation prelude's own;
   - X3d's draw at the session's open, for the durable attempt;
   - a host draw, for the ephemeral attempt.
3. **The durable entry (item 3).** A charged, fence-free presence probe chooses the route.
   - **Steady state:** one attempt, with no intent or notice.
   - **First use:** the creator act on attempt A, then a fresh `admit_ordinary_writer` on attempt B. The two-slot attempt is typed by `CreatorActEnded`, and there is still one gate per process.
   - **Amendments:** 468 item 1, X1 items 1 and 7, X3a item 2, X4B item 1, X2 item 6 and 464 items 1 and 5. X11 r1 item 1a is reconciled with X12 r4.
4. **The pre-analysis order R0 to R12 (item 4),** including the S3.1 storage-choice slot and X12 r4's first-use control.
5. **The DAG (item 5).**
   - The step lists, with retry `none`.
   - Joins J-α to J-κ, and settlement.
   - M3-C's open choices: blob custody, the lease, the S-B projection, and where the full `admit_enumeration` runs.
6. **The ephemeral path (item 6).** It uses the 458c read entry, never writes, and owes four joins (E-1 to E-4) to B/X2, C and X4T.
7. **The session opens at the handoff (item 7),** so the ExecutionId precedes provider spawn. `finalize` takes the open session. X5 item 3's order is amended (X5 r4), and so is X7 item 1's (X7 r7).
8. **S-OP-12 (item 8).**
   - A windowed `CancellationLatch`, a third source of the existing FinalGate.
   - `StopCause::Operator` and the REV reason `operator` (S6's word).
   - The five-phase table, 8.3's precedence, and phase D's decision point.
   - The exact X3d r9, X4 r8 and X7 r7 changes.
9. **J-BS (item 9).** An in-place optional `RetentionDisclosure.backupStatus`, present exactly when `firstUse` (meaning `Published`) is true.
10. **The outcome matrix (item 10).** 51 rows on existing codes, with no new public code.
11. **Re-commit and resume (item 11).** J1 decides neither: they belong to X3c r8 with X3c-3, and to J-RW with J4. J1 records only the interface the pipeline needs.
12. **Controls and crash-matrix obligations (item 12)**, the successors S1 to S17 with S7b and S14b (item 13), and units J2a to J3d (item 14). J4 belongs to J-RW.

## Decide

1. **The X11 successor.** Is item 1's scope consistent with BP:887, BP:895, M3P:64, M3P:301 and AQP:500-502? Do items 2 to 4 discharge every obligation at X11:64-81?
   - the order;
   - the creator's host entry;
   - how the creator command ends;
   - one RequestId;
   - the terminations;
   - the backup-status successor;
   - the producer and Run closure;
   - the F0 restatement.
2. **First use (item 3).**
   - Is the presence probe lawful against OWN §1a (OWN:15-32), §5 (OWN:91-105) and §6 (OWN:107-122), and against X1 item 1's purpose-typed receipts?
   - Does the two-slot attempt keep what the one-attempt rule protects (`initial_installation.rs:28`, `:96-99`; X1:49-54)?
   - Are the six amendments complete and minimal?
   - Is the `Present`-then-`Absent` race lawfully routed to `INSTALLATION.NOT_INITIALIZED`?
3. **X12 r4's first-use clause (item 4; X12r4:33-47, :195-206).** Is R0 to R12 consistent with it, with M3-B item 10 and with M3-C's order table (M3C:788-804)? Is the S3.1 slot sound?
4. **The session at the handoff (item 7).**
   - Is it sound against IE:1657-1658, X5 item 3 (X5:39-43), X3d item 2 (X3D:113-117) and M3-L items 2 and 13 (M3L:120, :375-382)?
   - Does it really leave security and storage code, and X9's census, unchanged?
5. **S-OP-12 (item 8).**
   - Does the latch keep X3D:168-172, X3D:261 and X3D:383?
   - Is the window (`commit_session.rs:930`, `:953-954`) the right B/C boundary?
   - Is 8.3's precedence sound against WS:224-231, SL:546-555, IE:1680-1681 and X7:94-106?
   - Is phase D's decision point sound against the single-envelope rule (`bootstrap.rs:57-58`) and ENV7's `interrupted` branches?
6. **J-BS (item 9).** Is the in-place append to `invocation-v5` lawful? Is the `firstUse` reading the right one? Is presence correct against ENV7's branches (`command-envelope-v7.schema.json:704-723`, `:790`)?
7. **The outcome matrix (item 10).** Is each row's class, code, fault cause and detail right against NE §10 (NE:3317-3575, NE:3837-3855), X3D item 9, X7 item 3, the 468 table, X4T item 10 and WS §9? Is any reachable M3 failure class missing?
8. **The ephemeral path (item 6).** Is the 458c-read-entry decision sound? Are E-1 to E-4 the complete set of owed joins, and are the recommendations lawful?
9. **Method.** Are the successors S1 to S17 (with S7b and S14b), the units J2a to J3d and their dependencies sound, and is the critical-path claim (item 14) consistent with M3P:218-229, draft M3P5:303-305 and M3-C r4? Are the crash-matrix obligations (item 12) sufficient under X9 items 5, 7 and 9?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256, as one string.

This is a law review, not a `verify_design` unit. The later contract successor J-BS and the inventory units J2a to J3d each need reviews of their own. A contract successor's verdict must be `ACCEPT-DESIGN-UNIT`. Do not commit.
