Grok review: law X9 r12, an amendment found by unit X9-3's development run. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT**.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under /tmp/opensip-implementation/reviews/grok-crash-matrix-x9-r12.
- This is a law review with no product cargo. Run git read-only, against product main `b999ae3`.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What changed

Pins are in hashes.txt. `crash-matrix-x9/PROPOSAL-r11.md` holds the r11 bytes you accepted: 111180 bytes, `51f4fa16…`, equal to `reviews/grok-crash-matrix-x9-r11/review.json`'s `subjectSha256`. Diff PROPOSAL.md against it.

**How it was found.** X9-3 transcribed its 58 rows from r11 and ran each once on `b999ae3`, uncommitted, before any lead run set. 46 rows passed. Six failed and two were harness errors (F13, F14 ×2, F24 wrong generation, F27 operation and execution, F49(a), and F44/F45 under F39's script). The lead's decisions are made under the owner's standing direction. They are:

1. **F13/F14 (and F15): R2 commits a distinct Run.**
   - **The failure:** after a landed evidence `COMMIT`, R2 replays the same synthetic Run, because the candidate gives one RunId per project. Staging then refuses on X3c item 10's invariant row ("a retained key already holds"; `project_commit.rs` `classify_staging`).
   - **The fix:** a distinct candidate variant, test support in storage's `crash_matrix_support`, inputs only. One source file's bytes in the snapshot are replaced by same-length salted bytes before the existing fixpoint rewrite, and then re-derived.
   - **Where it is used:** R2 of F13, F14 and F15.
   - **Rejected:** expecting the invariant row. Re-committing one Run stays X3d-2's known limit.
2. **F14's `x3d.finish.settle.before` moves to X9-4.** `finish` reaches it only when a REV or CLN is owed (`commit_session.rs`, `finish`), and no X9-3 run owes one. It becomes an owed-end-record run after F39's script.
3. **F24 wrong store generation.** Every row's digest is changed and the ledger stays readable. The result is the owner's §2 "both absent, no row" outcome: R1 UAU, R2 Committed, R3 `swept` with nothing written. The other two F24 variants are unchanged.
4. **F27's operation and execution swaps give R1 UC `ledger-join`.** That is `join_ledger` and X6 r4 item 4: BU is for a store-generation, namespace or carrier mismatch, or a requested binding.
5. **F49(a) gives R1 CH `pendingSettlement`.** The owner's one fresh capture reconciles the moved tail. "Never UQ, never a corruption diagnosis" is unchanged.
6. **F36 is F09 and F11 only.** The F19 and F38 variants cannot exist, because R2 is refused under the revoked view (C5, r3). The later ExecutionId is a fifth ladder step, R5.
7. **F39's script holds at `x3c.evidence.commit.before#1`.** `x4.gate.admit.after` is inside the checkpoint's shared-monitor section (`operation_guard.rs` `steps` holds the monitor through `FinalGate::admit`), so the observer's tick cannot latch while the writer is held there. X9-3 reproduced the watchdog.
   - The new point is the first one after the monitor is released, with the gate admitted.
   - The revocation names the session's own core closure, as X8c's B6 does.
   - This is law for F39, F44 and F45, and X9-4 inherits it.
   - Rejected: moving X4a's placement.
8. **Item 11's timing guard.**
   - **Where it applies:** every run that arms `x4.observer.tick`.
   - **The measurement:** the parent's monotonic clock, from the writer's first tick-hold record to its admission-hold record. The observer starts only after the first monitored read admits the view (`OperationGuard::start`).
   - **The record:** an optional `timingGuard` member. Above 2000 ms the run is a `HARNESS-ERROR`. The checker requires the member where the script arms the tick.
   - **Who implements it:** X9-3 for F44 and F45, and X9-4 reuses it.
9. **Record:** item 7's per-unit limit list is L1 to L11, as r8 set. The r4 bullet still said L1 to L10. You noted this in the X9-2 review.

Each change also has a short "r12" note at the item 8 ladder, the item 9 cells (F13, F14, F15, F24, F27, F36, F39, F44, F45, F49), item 11's timing guard, and item 12's X9-3 and X9-4 lines. Nothing else changes, including every X9-2 row and X9-5's host rules.

## Decide

- Does each decision follow from the owning law (X3c item 10, X6 r4 items 4 and 6, the owner's §2 and step 3, X4 r7 item 3's monitor section, C5) and the evidence named?
- Do the decisions change nothing else?
- Is anything else wrong?

Write REVIEW.md and review.json under the output directory. review.json needs:
- "verdict";
- "requiredFindings";
- "noAcceptedOutcomeChanged";
- "subjectSha256";
- "subject" (path, bytes, sha256);
- "preservedSnapshot": the accepted r11, `PROPOSAL-r11.md`, 111180 bytes, `51f4fa16…`.

Do not commit.
