# Review: evidence ledger X3c r2 and grant journal X3b r5

Verdict: REQUIRED-FINDINGS for both laws.

X3c r2 `docs/implementation/m2/ledger-blob-x3c/PROPOSAL.md` is 17037 bytes, sha256 `8344d819e77ff63b40cebfc022305a3d6ccb548af80f5837eda156ab9334d755`, matching hashes.txt. Preserved r1 is 16555 bytes, sha256 `b15f15d91fb293b9491808e093d71e9e6eb041a9ec255602f0f5781a6ba642e1`, the accepted X3c r1 subject.

X3b r5 `docs/implementation/m2/journal-x3b/PROPOSAL.md` is 25025 bytes, sha256 `51e927000d76488428784a626c01c0afe5a6a7da84d0a316b1bcd838392da2dd`, matching hashes.txt. The accepted X3b r4 subject is 24340 bytes, sha256 `296c05673cb535aec3d363f6ff908ef3d7011b2351d6322b67c47fa492c4a156`. On-disk `PROPOSAL-r4.md` is 24375 bytes, sha256 `304a679055ba3fc4b4fbf5ff2ea2ecf09246c303b0cc724e85c0c21f4754a4b9`.

The live product HEAD is `99f1c35b50ddd7a3a2724d9acadf9c72f27ce7da`. The real OpenSIP support directory is absent. No product cargo.

The X3c diff against r1 is the title, the provenance line, and item 8. The X3b diff against the on-disk r4 file is the title, the provenance line, and item 5 step 7.

## r1 RF-1, the path that reaches COMMIT

That path is now the same order in both laws. X3c item 8 and X3b item 5 step 7: journal transaction, ledger transaction, level 4, `SEAL` and the durable `COMMITTED` witness, staging, X4's repeated checkpoint and `AdmissionPermit`, ledger `COMMIT`, then release. Level 3 is never acquired or reacquired under level 4. The ledger transaction is acquired before level 4.

That order matches X4 r4 item 3, which repeats the checkpoint under `JournalAppendLock` after the `SEAL`, the witness, and association staging, and before evidence-commit admission. It matches the build plan's publication sequence: both level-3 transactions first, journal then ledger, and only then level 4, with the journal lock held through the ledger commit. A `REV` can no longer be appended between a `SEAL` and an evidence `COMMIT` that still proceeds.

## Required finding (both laws)

### RF-1 — A SEAL that stops before the evidence COMMIT never releases level 4

The new release condition fires only when the evidence `COMMIT` returns. X3b step 7 holds level 4 until that `COMMIT` returns `Committed` or `CommitUndetermined`. X3c item 8 step 8 releases on that same return. X3c's rejected sentence and its forbidden-substitutes line forbid releasing level 4 before the evidence commit, with no stop named.

Three stops never call that `COMMIT`, and level 4 is already held:

- An uncertain journal barrier. X3b item 5 says no evidence commit proceeds, and the writer refuses every further effect.
- A staging abort. X3c item 6 aborts the ledger transaction without commit. It does not release level 4.
- A failed post-SEAL checkpoint or `AdmissionPermit` refusal. X4 r4 item 3 latches and aborts the still-uncommitted evidence transaction. X3b item 10's journal half of F19 releases level 4 then level 3 and appends `REV` through a fresh level-3 then level-4 call. The build plan's F19 and F38 require that same release, then a new lawful journal call. Level 3 is never reacquired under level 4.

Level 4 is the in-process `JournalAppendLock`. Holding it until a `COMMIT` that this path must not call leaves the fresh `REV` acquire unable to run. X3b step 7 and X3b item 10 assign opposite releases for the checkpoint stop. X3c's forbidden sentence forbids the release F19 requires.

Item 7's commit outcomes are success and `CommitUndetermined`. The amendment's name `Committed` is not an item 7 outcome.

Required, in both laws: on the path that calls the evidence `COMMIT`, level 4 stays held until `COMMIT` returns success or `CommitUndetermined`, then is released. That is the order above. If the `SEAL` path stops before the evidence `COMMIT` — uncertain journal barrier, staging abort, or checkpoint or `AdmissionPermit` refusal — level 4 is released at that stop, before any fresh level-3 then level-4 `REV`. Level 3 is never acquired or reacquired under level 4. X3c's forbidden sentence must allow that stop's release. X3b step 7 and item 10 must state the same release.

## Required finding (X3b only)

### RF-2 — PROPOSAL-r4.md is not the accepted r4 subject

The r5 header says the r4 bytes are preserved in `PROPOSAL-r4.md`. They are not. The accepted subject is 24340 bytes, sha256 `296c05673cb535aec3d363f6ff908ef3d7011b2351d6322b67c47fa492c4a156`. The file on disk is 24375 bytes, sha256 `304a679055ba3fc4b4fbf5ff2ea2ecf09246c303b0cc724e85c0c21f4754a4b9`. Deleting the inserted date-paragraph sentence `r4 ACCEPTED by Grok on 2026-09-30. ` restores the accepted hash. r5's date paragraph carries that same insertion, so r5 is the stamped copy plus the step-7 amendment.

Required: `PROPOSAL-r4.md` is the accepted bytes, and r5's date paragraph does not carry that insertion. The r5 provenance line may record that r4 was accepted.

## What still matches

X3c r1's other rows are unchanged: ledger creation and the empty-file resume, attempt admission before objects, `blob_store` publication, non-waiting journal-then-ledger acquisition, all-or-none staging, `AdmissionPermit` on `COMMIT`, `CommitUndetermined` as `DURABILITY.COMMIT_FAILED`, the invariant row for a reused ExecutionId, and `WORK.BUDGET_EXHAUSTED` reserved before the first object. X3c does not open the witness or the floor. The header's law list still names X3b r4; item 8 cites X3b r5 for the hold.
