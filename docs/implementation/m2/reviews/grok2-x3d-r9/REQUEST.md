Grok review: law X3d r9, the CommitSession facade law, which has two parts:
- **The main subject is J1's successor S10,** the commit-phase cancellation join. It is an amendment.
- **The second subject records X3c r8's cross-law item CL-1,** which you accepted.

This is a **law review**. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-x3d-r9.

**Lead note (reviewer change).** This request was written for GROK2. **Grok** reviews it, because GROK2 is busy with X4-F2. The directory keeps its name. Write your output under `/tmp/opensip-implementation/reviews/grok2-x3d-r9`. Don't run cargo.


**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- No product builds or test runs. Timing-sensitive lanes may be using this machine, and X4-F2's lanes and X9 regression are in flight. Do not run any lead set.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What is asked

- **S10 (main).** J1 r5 decided S10 and named X3d r9 as its vehicle. Is r9's S10 section faithful to J1 r5 as its consumers expect it? Do its six lead decisions, LD9-1 to LD9-6, decide only points the consumers leave open, and decide them soundly? A change that goes beyond J1 r5, decides anything of X4 r8 (S11) or X7 r7 (S9), or misses something a consumer needs is a finding.
- **CL-1 (secondary).** A record of X3c r8. A record that goes beyond its source or misstates it is a finding. So is a route from X3c r8 to X3d that r9 misses.
- **Both.** No accepted outcome of X3d r8 or of another law changes, apart from S10's declared changes.

## Pins

The pins are in `hashes.txt`. Every pin other than the subject and this request is an accepted snapshot, or a review record that accepted one.
- **The subject:** `docs/implementation/m2/commit-session-x3d/PROPOSAL.md`, X3d r9. It is the subject of `subjectSha256`.
- **The diff base:** `commit-session-x3d/PROPOSAL-r8.md` (`5e491b92…`, 62,445 bytes).
  - These are the r8 bytes Grok accepted, without the acceptance note. They equal `reviews/grok-evaluator-closure-x3d-r8/x3d/review.json`'s `subjectSha256`.
  - The snapshot already existed. It was checked, not rewritten.
  - Diff PROPOSAL-r8.md against PROPOSAL.md.
- **S10's source and consumers:**
  - J1 r5, `m3/host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`, = `m3/reviews/codex-host-pipeline-j-r5/review.json`'s `subjectSha256`). It is S10's source: items 2, 7, 8.1 to 8.7, 12, 13 (rows S10 to S12) and 14 (J3a, J3b), and the forbidden substitutes.
  - M3-PLAN r9, `m3/M3-PLAN-r9.md` (`72bc7a13…`, = `m3/reviews/grok2-m3-plan-r9/review.json`'s `subjectSha256`): :317 and :364.
  - X3c r8 items 15.1 and 16 (below).
  - M3-L r5, accepted in review, `m3/provider-protocol-l/PROPOSAL-r5.md` (`f654ee4e…`, = `m3/reviews/grok-provider-protocol-l-r5/review.json`'s `subjectSha256`): items 16f and 18.
- **CL-1's source:** X3c r8, `ledger-blob-x3c/PROPOSAL-r8.md` (`ba638efb…`, 66,778 bytes, = `reviews/grok2-ledger-blob-x3c-r8/review.json`'s `subjectSha256`). Your own review of it is pinned for its CL-1 paragraph ("Cross-law").
- **Not yet written:** X4 r8 (S11) and X7 r7 (S9). X4 r7 is cited by item only. Its live file carries an acceptance note, and no r7 snapshot exists to pin.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `cca4fe4`, read-only. X3c-3, J3a and J3b are not integrated.
  - **For S10:**
    - `crates/security/src/commit_authority.rs:8-48` (the gate's two-bit word);
    - `crates/security/src/custody/commit_session.rs`:
      - `:62-104` (`RevReason`) and `:172-182` (the reserve cost, the maximum over the closed set);
      - `:322-345` (`open`'s draw), `:529-545` (`refused()`, `undetermined()`) and `:572-587` (`open`'s refusal, which builds a `StoppedSession`);
      - `:952-1016` (`publish`'s three returns, with today's `latchedAfterAdmission` load at `:953-954`);
    - `crates/security/src/custody/operation_guard.rs:96-106` (`StopCause`, first cause wins);
    - `crates/security/src/installation_termination.rs:73` (468c's vocabulary);
    - `crates/storage/src/commit.rs:465-557` (`prepare_commit`'s returns; attempt admission and objects in one charge at `:521`) and `:571` (`publish`).
  - **For CL-1:**
    - Under `crates/storage`, `git diff --name-only e093e90 cca4fe4` lists only `src/store_root/native_marker.rs`, which X3c r8 does not cite. It lists none of X3c r8's other cited files (`identity/src/closure.rs`, `platform/src/filesystem.rs`, `security/src/custody/commit_session.rs`), and not `security/src/crash_matrix_census.rs`. So every product line X3c r8 cites at `e093e90` is the same at `cca4fe4`.
    - r9 cites `crates/storage/src/commit.rs:10-15`, `:701-710` and `:617`; `crates/storage/src/commit_tests.rs:493-603`; `crates/security/src/custody/commit_session.rs:927` and `:940`; and `crates/security/src/crash_matrix_census.rs:822`.

## The shape of the diff

There are two replaced lines:
- the title;
- the r8 paragraph's first line. It gains "r8 ACCEPTED by Grok on 2026-10-02.", the acceptance note already in the working law (`9f3712a0…`), as in earlier rounds.

Everything else is inserted. No r8 sentence is deleted or reworded. With r9 line numbers:
- **The r9 header** (:80-170), between r8's header and "## Problem":
  - the parts;
  - the "r9 changes" table, with S10 as row 1;
  - CL-1's standing;
  - the r7 known limit;
  - X3c r8's other references;
  - crash windows under CL-1;
  - XL-1, now resolved.
- **The S10 section** (:472-619), "S10 (r9)", after item 13: S10.1 to S10.11.
- **S10's "r9 (S10)" notes:**
  - item 1 (:205), item 2 (:212), item 5 (:269), item 6 (:276), item 7 (:313) and item 8 (:350);
  - item 9 (:394), item 11 (:419) and item 13 (:470);
  - four forbidden substitutes (:646-649).
- **CL-1's "r9 (record)" notes:**
  - the r7 known-limit bullet (:55);
  - item 4 step 3.8 (:248);
  - item 9 (:390-393);
  - item 13's X3d-2 line (:453).

## S10: what r9 carries (main subject)

1. **S10.1, item 2.** `open` reserves its drawn ExecutionId in `ExecutionIdReservations` before the session exists.
   - Collisions redraw, at most eight draws. Exhaustion takes the existing host I/O row.
   - There is no release.
   - The session holds `ReservedExecutionId`.
   - The census point, F34's injection and X3c's durable attempt-row reservation are unchanged.
   - This is J3a's.
2. **S10.2, items 1 and 5.**
   - **The token.** `take_cancellation_latch`, `Some` once per operation. `CancellationLatch::latch(self, D9Signal) -> LatchOutcome`.
   - **The window.** It opens when step 4's attempt row commits (LD9-1). It stays open across `Ok(PreparedCommit)`. It closes, with the sample, in every step that produces a `StoppedSession`: `prepare_commit`'s four error returns, `publish`'s three returns, `refused()`, `undetermined()` and `open`'s refusal (LD9-2).
   - **The results.** `BeforeAdmission`, `AfterAdmission`, `AlreadyStopped` and `OutsideWindow`.
   - **The phase effects.** B: the next checkpoint refuses, then `REV(operator)`, and `CLN` if there is a `SEAL`. C: the outcome stands. A: `refused()`.
   - **Item 5's law.** F38, F39 and F41 are kept.
3. **S10.3, item 6.** `latchedAfterAdmission` is the close's sample. `StoppedSession::admitted_at_close()` carries the admission bit to the host (LD9-3). No outcome is added.
4. **S10.4, items 7 and 8.**
   - `StopCause::Operator { signal }`, under X4's first-cause rule (LD9-4).
   - The `REV` reason `operator`. `AlreadyStopped` keeps the earlier reason.
   - The reserve is unchanged.
5. **S10.5, item 9.** The row "operator stop": `InstallationTermination::Interrupted { signal }`, class `interrupted`, exit 130, with no code or detail. X7 r7 projects it.
6. **S10.6, item 7.** The `refused()` record.
7. **S10.7, item 11.** X8 fixtures for `CancellationLatch` and `ReservedExecutionId`.
8. **S10.8, item 13.** J3a and J3b. Tests J-C4b, J-C12, J-C15 and J-C15b. Lands with X4 r8 (LD9-5).
9. **S10.9, crash windows.**
   - No new point.
   - Rows S12-B, S12-C and S12-U, J1's. S12-C and S12-U wait for S21.
   - No row for B before the `SEAL`, because F18's end path already qualifies it (LD9-6).
   - Existing rows keep their values.
10. **S10.10 and S10.11.**
    - The six lead decisions, each with rejected alternatives.
    - Cross-law items to X4 r8 (window bits, masked loops, never-reset, and recording `StopCause::Operator`), X7 r7, S21, X8 (record) and X9 r17.

## CL-1: what r9 records (secondary subject)

1. **Step 3.8 (X3c r8 item 16).** A first commit in (S, N) stages availability and pins. A re-commit of an already-committed Run stages neither (X3c r8 items 6, 6a.2, 6a.3, 6a.4 (R8-4) and 6a.5 (R8-5)). The header defines standing by X3c r8 item 6a.2.
2. **The r7 known limit** (PROPOSAL-r8.md:51-54). It is lifted in law by X3c r8, and in the product when X3c-3 integrates. X3c r8 differs from r7's sketch in one case: material without an availability record is `LEDGER.CORRUPT`.
3. **Item 9 (X3c r8 item 10).** Three re-commit refusals on existing rows.
4. **Item 13.** X3c-3 changes only doc comments in `commit.rs`.
5. **X3c r8's other references to X3d,** and crash windows under CL-1: no change implied.
6. **XL-1, resolved.** The lead folded S10 into r9, so every accepted "X3d r9" reference stays true. The rejected alternative was S10 as r10, which needs record notes in J1, M3-PLAN, X3c and M3-L.

## Decide

**S10:**
1. **Faithfulness.** Does the section carry exactly J1 r5's S10 (8.1, 8.6, the S10 row, item 2's reservation at `open`, item 7's `refused()` record), citing each? Does anything go beyond what J1 r5, M3P:317, X3c r8 item 15.1 and M3-L r5 items 16f and 18 name?
2. **The consumers.** Does r9 now give each consumer what it expects?
   - J1: units J3a and J3b, J-C4b, J-C12, J-C15, J-C15b, and S12-B, -C and -U.
   - M3P:317: J3a gated on item 2 only.
   - X3c r8 item 15.1: a re-commit in phase B.
   - M3-L r5: reviewed alone, landing with J3b.
3. **The window.** Against the product, is every `StoppedSession` producer a closing step? Is `Ok(PreparedCommit)` the only continuing result? Is LD9-2 (`open`'s refusal) right? Is LD9-1's opening point inside `prepare_commit` right, given that storage admits the attempt row and publishes the objects in one charge today?
4. **The lead decisions.** Is each of LD9-1 to LD9-6 needed, sound and limited to an open point? Are the rejected alternatives right? In particular:
   - LD9-3's `admitted_at_close()` against J1 r5:567 and :882;
   - LD9-4's home for `StopCause::Operator`;
   - LD9-5's review before X4 r8 exists.
5. **The boundaries.** Does r9 decide anything that is X4 r8's (the gate word, the masked loops, never-reset) or X7 r7's (projections)? Is S10.11's routing to them right?
6. **Rows and budget.**
   - Are S12-B, -C and -U the right rows, and enough of them? Is LD9-6 right?
   - Do F00, F34, F18, F19 and F38 to F41 keep their transcribed values?
   - Is the reserve claim right, given that the cost is the maximum over the closed set (`commit_session.rs:172-182`)?
7. **Forbidden substitutes.** Are the four new entries faithful to J1 r5:233, :658, :908 and :913-916?

**CL-1:**

8. **The record.** Is the step 3.8 restatement faithful to X3c r8 and CL-1? Are the r7 known-limit note, the item 9 and item 13 notes, and the references table right? Is "no change implied" for crash windows and controls under CL-1 correct?
9. **XL-1.** Is the lead's fold recorded faithfully, with its rejected alternative?

**Scope:**

10. **Preservation.**
    - Does every r8 sentence survive verbatim, apart from the title and the acceptance note?
    - Apart from S10's declared changes, does any accepted outcome of X3d or of another law change?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"noAcceptedOutcomeChanged"`: true or false, judged apart from S10's declared changes;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"preservedSnapshot"`: PROPOSAL-r8.md's path, bytes and sha256.

Do not commit.
