# Law X3d r9 — ACCEPT

Reviewer: Grok. Directory name stays `grok2-x3d-r9`. No cargo, and no lead set.

**Verdict: ACCEPT.** S10 carries J1 r5's X3d half, and LD9-1 through LD9-6 decide only points those consumers leave open. CL-1 records X3c r8 and changes no X3d rule. One non-blocking observation: XL-1's scope list attributes the window bits to S10.

- Subject `docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, 97,231 bytes, sha256 `c727001a44e1ef48ce131b0262cb566e9417ff5537bf3d9446b97ca10a213fdf`.
- Preserved snapshot `docs/implementation/m2/commit-session-x3d/PROPOSAL-r8.md`, 62,445 bytes, sha256 `5e491b9223352ee82674109d056d5d428ed85625b9410a69834fa02d5075849c`.
- `noAcceptedOutcomeChanged` is true, judged apart from S10's declared changes.

## Preservation

A line diff of PROPOSAL-r8.md against PROPOSAL.md has two replacements and insertions only. The title changes from r8 to r9. The r8 paragraph's first line (r9:58) inserts `r8 ACCEPTED by Grok on 2026-10-02. ` and the remainder is byte-identical to r8's line. Every other r8 sentence survives verbatim. The insertions are the r7 known-limit note (r9:55), the r9 header (r9:79-170), the short item notes, the S10 section (r9:472-619), and four forbidden substitutes (r9:646-649).

## S10

The section cites the J1 r5 passages it carries: 8.1 and 8.6 (J1:512-547, :651-658), the S10 row (J1:856), `refused()` (J1:502), the reservation at `open` (J1:205-218), J3a and J3b (J1:881-882), and the S12 rows (J1:833-839). The phase effects match J1's table: B refuses at the next checkpoint and appends `REV(operator)` plus `CLN` when a `SEAL` is durable; C lets the evidence `COMMIT` stand and appends `REV(operator)` only after `Committed`; A ends through `refused()` and `finish`. J1:691 is the sentence S10.2 cites: a latch after `Ok(PreparedCommit)` and before `publish` is seen by `publish`'s first checkpoint.

Consumers receive what they name.

- M3-PLAN r9:317 assigns X3d r9 both S10 and CL-1, and gates J3a on item 2 and J3b on the rest. M3P:364 routes CL-1 to the X3d r9 row. S10.1 is J3a's reservation; S10.8 gives J3b the latch, the row, `refused()`, and `admitted_at_close()`.
- X3c r8 item 15.1's phase-B sentence is S10.2: the latch takes the gate 0→2, the staged re-commit rolls back, and `finish` appends `REV(operator)` plus `CLN` for a durable `SEAL`. The same item says the re-commit branch adds no window bit, latch source, checkpoint, crash point, or `REV` reason. S10.11 leaves the bits with X4 r8. Phase C's F39/F40-by-outcome and phase D's projection are J1 8.2 and X7 r7; S10.2 and S10.11 cite them and add no re-commit variant of S12.
- M3-L r5 items 16f and 18 review X3d r9, X4 r8, and X7 r7 each on its own, land them with J3b, and until then no signal sets the latch. S10.8 and LD9-5 say the same.

### The window, against the product at `cca4fe4`

The cited product files are the bytes at `cca4fe48d3cf44c6c73c0e625bd4de769cd34899`. They are unchanged from that commit through current `main` (`988f6ed`). `git diff --name-only e093e90 cca4fe4 -- crates/storage` lists only `src/store_root/native_marker.rs`.

Every producer of a `StoppedSession` is a closing step in S10.2:

- `open`'s refusal builds one at `commit_session.rs:572-587`.
- `reserve_end_path` (item 3 step 0) and `capacity` (step 3) build one.
- `prepare_commit` (`commit.rs:465-557`) returns `Refused` for steps 0-6, `CarrierCapacityExhausted`, `CommitUndetermined`, and `ExistingAttempt`, each with a `StoppedSession`. `Ok(PreparedCommit)` is that function's only continuing result.
- `publish` (`commit.rs:571`) returns `Committed`, `Refused`, or `CommitUndetermined`, each with a `StoppedSession`. Step 2's busy path is `JournalWriteTxn::abort` (`commit_session.rs:667`). Step 1's failure is `begin_journal_txn`. The three seal returns are `commit_session.rs:952-1016`.
- `refused()` and `undetermined()` are `commit_session.rs:529-545`.

`latchedAfterAdmission` is today's separate load at `commit_session.rs:953-954` (`AttemptState::AdmittedThenLatched`). S10.3 replaces that load with the close's sample and keeps the flag's meaning, state 3.

LD9-1 puts the opening call in `prepare_commit`, after step 4's successful `COMMIT` and before step 6's first object. Today `admit_and_publish` admits the attempt row and publishes the objects in one charge (`commit.rs:520-521`). The gate is security's (`commit_authority.rs:8-48` is the two state bits). Opening at `Ok(PreparedCommit)` would leave those objects outside the window, which contradicts J1:520. Storage setting the bit would mint security state. The session step between the two is the call site that keeps J1's point. J3b splits that charge so `prepare_commit` can make the call, the same way it already calls step 0.

LD9-2 is the producer J1:522-527 does not list. J1:521 closes the window in every step that produces a `StoppedSession`, and `open`'s refusal produces one. The token comes from a `CommitSession`, so that close changes no outcome.

### Lead decisions

- **LD9-3.** J1:567 says state bits 1 or 3 are phase C and 0 or 2 are phase B, and J3b carries the bit (J1:882). J1 8.6 does not say where the bit lives. `StoppedSession::admitted_at_close()` is a read-only bit on the session the host already receives with the outcome. A new `CommitOutcome` field would change item 6, which J1 8.6 leaves unchanged. Reading the gate after return would see a later observer latch, because the observer ignores the window bits (J1:538). A `CommitUndetermined` from `publish` is either an uncertain journal outcome or an undetermined evidence `COMMIT` (J1:569-570), so the outcome alone does not distinguish B from C.
- **LD9-4.** `StopCause` is X4's type (`operation_guard.rs:96-106`; first cause wins). J1:653 assigns `StopCause::Operator { signal }` to X3d r9. J1:857's S11 row does not name it. r9 carries the variant, the `REV` mapping, and the row, and asks X4 r8 to record the variant in its stop-cause list. That record does not decide the gate word, the loops, or never-reset.
- **LD9-5.** M3-L item 16f reviews this law before X4 r8 exists. The section states the source, the token, the open and close points, the results, and the sample, and cites J1 8.1 for the encoding. S10.1 gates J3a and does not depend on S11. Holding r9 for X4 r8 would hold that reservation and CL-1.
- **LD9-6.** J1 names S12-B, S12-C, and S12-U. S12-B holds at `x3d.publish.after-staging` (the barrier at `commit_session.rs:927`). S12-C and S12-U wait for S21, as J1:833-839 and J1:868 require. A latch in phase B before the `SEAL` is seen at step 3.2; its durable path is F18's (refused at the first checkpoint, no `SEAL`, `REV` from the reserve, no `CLN`). J-C15b already injects at step 3.1. S12-D and S12-O run with the window closed.

The reserve claim matches the code. `end_path_reserve_cost` (`commit_session.rs:172-182`) is the maximum canonical body over `RevReason::ALL`, plus the one `CLN` draft. `operator` is S6's word (`security-and-lifecycle.md:491`, `REV(policy|operator)`), eight characters against `observer-fail-stop` at eighteen. The maximum stays the existing draft, so the exact cost and its pin stay.

The row is `InstallationTermination::Interrupted { signal }`, class `interrupted`, exit 130, with no errorCode. The security enum at `installation_termination.rs:73` has no such variant yet. `InstallationTerminationV1` requires `error_code` (`crates/host/src/installation_termination.rs:21-28`), so X7 r7 carries the interrupted form. S10.5 adds no public code, class, exit, or detail. F00, F34, F18, F19, and F38 through F41 keep their transcribed values; the close sample yields the same `latchedAfterAdmission` the load did. No new crash point: the latch reuses `x4.gate.latch.after`, and `x3d.finish.end-step.after` remains the census point at `crash_matrix_census.rs:822`.

The four forbidden substitutes are J1 8.6's X3d list plus the two X3d clauses of J1:916 and J1:908. "A cancellation latch outside its window, minted twice, or used as authority" is J1:658 and J1:913. "The outcome selected from the gate's state rather than from the returned outcome" is J1:658; the longer projection clauses on J1:914 are X7 r7's. "Closing the window on `Ok(PreparedCommit)`, or anywhere a `StoppedSession` is not produced" is the X3d half of J1:916. The compare-exchange half of that line is the masked-loop rule S10.11 leaves with X4 r8. "A session ExecutionId used before its process reservation; a reservation released or reused" is X3d's slice of J1:233 and J1:908.

S10.11 routes the gate word, the masked loops, state decoding, and never-reset to X4 r8, and the `interrupted` projection to X7 r7. The section cites `commit_authority.rs` and decides none of that encoding.

## CL-1

X3c r8 item 16 says step 3.8 should become X3c item 6's staging, with availability and pins on a Run's first commit in (S, N) only, and "No X3d rule changes." The r9 note at :248 does that. Before any insert, staging reads standing and, on a re-commit, compares the Run material (6a.2, 6a.3). It then stages `stage_recovery_pair`, the Run material, and the object references. A first commit, meaning neither per-Run row exists, also stages generation 0 `retained` and the pins. A re-commit stages neither (6a.4, R8-4; 6a.5, R8-5). The header's standing section is 6a.2, including the one-sided `LEDGER.CORRUPT` refusal and the rule that a landed `COMMIT` makes the Run already committed even when the attempt was reported `CommitUndetermined`.

The r7 note records the one difference from r7's sketch. Material without an availability record is `LEDGER.CORRUPT`, which is 6a.2's rejection of treating a one-sided Run as a first commit. The product still stages availability and the empty pin set on every commit (`commit.rs:10-15`, `:701-710`, and `stage` at `:729-746`). X3c-3 is not in those bytes. `commit_tests.rs:493-603` still expects one availability row and no pin row after a first commit, which X3c r8 item 12b keeps.

Item 9's note is X3c item 10's three conditions on rows item 9 already has: a regeneration mismatch or a non-empty declared pin set on the invariant row, and a one-sided Run on the quarantine row with `domainDetail` omitted. Each follows item 4's stop order and item 7's `REV` and `CLN`. Item 13's note matches X3c items 6a.9 and 13: X3c-3 changes only those two doc comments in `commit.rs`.

The references table matches items 6a.1, 6a.8, 6a.9, 10, 12b, 13, 15.1, 15.3, and 16. Crash windows under CL-1 add no X3d point. RC-8 holds at `x3d.publish.after-staging` (`commit_session.rs:927`). RC-5 and RC-8 use `x3d.publish.commit-returned` (`:940`). RC-5 also uses `x3d.publish.published` (`commit.rs:617`) and `x3d.finish.end-step.after`. The `end(…)` values follow items 7 and 8: `REV` and `CLN` after a certain staging refusal that leaves a durable `SEAL` (RC-6, RC-7); nothing after an undetermined evidence `COMMIT` (RC-4); no `REV` when the process dies before `finish` (RC-3). The 19 storage runs, of which 18 change outcome, stay X3c item 14's record for X9 r17. GROK2's X3c r8 review, Cross-law, is the same CL-1 paragraph: restate step 3.8 and change no X3d rule.

## XL-1

The fold matches the accepted names. J1, M3-PLAN, X3c item 16, and M3-L items 16f and 18 all say "X3d r9" for S10, and M3P:317 and :364 put CL-1 on that same revision. Folding S10 into r9 keeps those references true. The rejected alternative, S10 as r10, would need a record note in each of those four laws. CL-1's notes and S10's sections are different sentences.

NBO-1 is the one slip in that rationale. Line 155 includes the window bits in what S10 covers. J1 assigns those bits to X4 r8, and LD9-5 and S10.11 already say so. The fold itself is right.

## Outcomes

Apart from S10's declared additions (the third latch source, `StopCause::Operator`, the `REV` reason `operator`, the operator-stop row, `admitted_at_close()`, the reservation, and the four substitutes), no accepted outcome, row, code, detail, lock order, budget, or crash point of X3d r8 changes. CL-1 restates step 3.8 as the record X3c r8 asked for. No accepted outcome of J1 r5, X3c r8, M3-L r5, or M3-PLAN r9 changes.
