GROK2 review: law X3c r8, the re-commit successor to the evidence ledger and blob publication law. This is a **law and contract-soundness** review of an amendment. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-ledger-blob-x3c-r8.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine. Do not run any lead set.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.
- Use read-only scratch scripts under your review directory if you need them (for example, to tabulate the X9 evidence runs or recompute digests).

## Subject

The pins are in `hashes.txt`. The subject is uncommitted in arch until it is accepted.
- **The subject:** `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md`, law X3c r8. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m2/ledger-blob-x3c/PROPOSAL-r7.md` (`b9585372…`, 18,855 bytes). These are the r7 bytes Grok accepted, without the acceptance note, and they equal `reviews/grok-ledger-blob-x3c-r7/review.json`'s `subjectSha256`. Diff PROPOSAL-r7.md against PROPOSAL.md.
- **The unit.** The accepted M3 plan assigns X3c r8 (law) and X3c-3 (storage code, M, plus one serialized X9 lead set) by lead decision P5-2 (`docs/implementation/m3/M3-PLAN-r6.md:157, :217, :237, :310, :576-578`). X3c-3 must land before J3d, by M3 day 25.
- **The gap.** A Run already committed in the same store and namespace cannot be committed again: it is refused at staging, on the invariant row, after its durable `SEAL` (`m2/EXIT-PLAN.md:171`; `m2/M2-COMPLETE.md` §5 row 11; X3d r8's r7 note, `m2/commit-session-x3d/PROPOSAL.md:51-54`). The law's Problem section traces the cause to the product's lines.
- **Governing records and their status:**
  - **Accepted:** X3c r7; X3d r8; X6 r4; X7 r6; X9 r16; M3-PLAN r6; M3-J1 r3 (J1: item 8's commit phases and cancellation, item 11, successors S12 and S14). M2 is complete.
  - **The contracts:** identity-and-evidence (IE:104-107, :1665-1683, :1689-1692, :1721-1725, :1814-1815, :1825-1827) and security-and-lifecycle (SL:1456).
  - **In review with you, not accepted:** J-RW r1, the resume/repair writer (`docs/implementation/m3/resume-repair-jrw/PROPOSAL.md`, arch `80a5d822b`). It amends X3c too. r8 cites it, does not absorb its X3c text (its successor RW-S3), and follows its LD-11 for the order. Judge r8's items 15.2 and CL-2 to CL-5 against J-RW r1 as pinned.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `e093e90` (F8b), read-only. `git diff --name-only 3e64266 e093e90 -- crates/` is empty, so every cited product line is the same at `3e64266`. The key files are `crates/storage/src/commit.rs`, `crates/storage/src/ledger_store.rs`, `crates/storage/src/ledger_store/{project_commit,project_ledger,recovery_material,recovery_pins,pin_transactions}.rs`, `crates/storage/src/{availability,pin_inventory,recover}.rs`, `crates/security/src/custody/commit_session.rs`, and the matrix driver `crates/storage/tests/commit_tests.rs`.
- **The X9 evidence** at C = `3d2d5b5`: `docs/implementation/m2/crash-matrix-x9/evidence/3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f/storage/` (`census-trace.txt`, `matrix.json`, `runs/`).

**Scope.** In r7's text, r8 changes four places: the title, the history line, item 6's insert bullet, and item 11's hook sentence (the G2 restatement). Everything else is added: the r8 basis and changes table, a Problem paragraph, item 6a, r8 bullets in items 9, 10 and 12, and items 12b and 14 to 16. r8 also extends the forbidden substitutes and "Not claimed". Items 1 to 5, 7 and 8 must be unchanged. Item 2 in particular is untouched (CL-5).

## What r8 decides

1. **Identity (6a.1, R8-1).** A re-commit is the same Run, committed again by a new attempt. It has its own ExecutionId, attempt row, `SEAL`, receipt, association and Run-material row, and the next `commitSequence`. It ends `Committed(PublishedCommit)`, never on the invariant row. **Rejected:** returning the earlier receipt; refusing; reusing the earlier attempt.
2. **Standing (6a.2, R8-2).** Inside the open level-3 transaction, before any insert, staging reads the Run's committed per-Run rows only: its availability record and any Run-material row naming it.
   - Neither: a first commit, staged as r7 stages it.
   - Both: a re-commit.
   - Exactly one: `LEDGER.CORRUPT`.

   Standing never reads attempt rows, their phase, `SEAL`s, objects or uncommitted state. So an orphan `SEAL` leaves no standing (F36), and a landed but `admitted` or undetermined commit does. The earlier attempt stays X6's, as J-RW's out-of-scope list leaves it.
3. **Byte-identical material (6a.3, R8-3).** A re-commit's manifest and inventory must equal the Run's material row with the least ExecutionId, byte for byte. Otherwise the invariant row applies: IE's "regeneration mismatch refuses".
4. **Per-Run rows once (6a.4, 6a.5, R8-4, R8-5).** Only a Run's first commit stages availability and pins. A re-commit writes no availability successor and changes no pin. A non-empty declared pin set on a re-commit is the invariant row. Regeneration of availability is not claimed; it belongs to the retention and restoration owner.
5. **No DDL change, no new crash point, no new type or outcome (6a.9, R8-6).**
6. **Budget and rows (items 9 and 10).** Three new conditions, all on existing rows.
7. **X3c-3 (item 13).** The code, tests (12b), and one serialized lead set on both targets. Whichever of X3c-3 and J4 integrates second reruns both units' rows.
8. **The crash windows and X9 r17's `RC-` section (item 14, R8-7).**
   - Rows RC-1 to RC-9.
   - A census child (the lawful re-commit) that adds the confirm branch's `x3c.object/reopen-confirm` points to the kill set.
   - A record of 19 accepted runs with an unscored same-Run commit, 18 of which change outcome.
9. **Interactions (item 15) and cross-law items (item 16).**
   - J1's phases and S12 rows are unchanged.
   - J-RW is disjoint in meaning, and is sequenced by its LD-11.
   - CL-1 (X3d record), CL-2 (X9 r17's shared sections), CL-3 to CL-5 (J-RW).

## Decide

1. **Identity and idempotence.** Is 6a.1 sound under IE:104-107 and :1683? 6a.4 reads IE's commit order (IE:1670-1673): a duplicate retry inserts its separate receipt and per-attempt material, and leaves the shared Run's availability and pins as they are. Is that reading lawful, or does it need an IE passage successor?
2. **Standing.** Is 6a.2 complete and race-free under the writer lease and `BEGIN IMMEDIATE`? Is `LEDGER.CORRUPT` the right existing row for a one-sided Run (X3c item 10; readonly-recovery's quarantine row)? Does anything let two attempts both stage a first commit of one Run, or let a re-commit act on an earlier attempt's state?
3. **Material equality.** Is the least-ExecutionId row with induction a sound and deterministic test? Is the invariant row the right row for a regeneration mismatch?
4. **Safety.** Can any path in r8 silently overwrite a committed Run, or let two Runs claim one identity? Check 6a.6's table against the triggers in `ledger_store.rs:441-502, :762-773` and `recovery_material.rs:13-26`. Check 6a.4's treatment of a non-retained record against `recover.rs:432-458` (RC-9).
5. **The matrix.**
   - Is the "no new crash point" claim (6a.9) correct under X9 item 5 and r16's coverage rule?
   - Do RC-1 to RC-9 cover the windows where a re-commit's state differs from a first commit's?
   - Are their expected values derivable from the owning laws, with nothing read back from a run?
   - Is the 19-run record right? Check it against the evidence runs and the mutations in `crates/storage/tests/commit_tests.rs:2502-2657`.
6. **J1.** Are J1's phases, cancellation latch, 8.3 precedence and S12 rows unaffected (15.1)? Is J1 item 11's requirement met, with J-C21's storage half in 12b?
7. **J-RW.**
   - Does r8 cite J-RW's out-of-scope boundary (J-RW:79-81, :427) where a re-commit proceeds over an `admitted` or undetermined earlier commit?
   - Does r8 confine its edits to item 10 and the forbidden substitutes to re-commit, absorbing none of RW-S3?
   - Are CL-3 to CL-5 and the integration-order rule right?
8. **Cross-law.** Is any conflict with an accepted law missed? CL-1 claims that only X3d's step 3.8 wording conflicts.
9. **Scope.** Does r8 change anything in r7 beyond the four marked places?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not an inventory-unit review. X3c-3 gets its own unit review, and X9 r17's `RC-` section is transcribed and reviewed with it. Do not commit.
