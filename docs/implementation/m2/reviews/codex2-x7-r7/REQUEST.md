GROK2 review: law X7 r7, the host finalization law. r7 is an amendment, J1's successor **S9**: the host half of the commit-phase cancellation join. Its centre is the projection of X3d r9's new row "operator stop" (class `interrupted`, exit 130, no code) through finalization and delivery.

This is a **law review**. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-x7-r7.

**Lead note (reviewer change).** This request was written for CODEX2. **GROK2** reviews it, in parallel with CODEX2's review of its sibling X4 r8. The directory keeps its name. Write your output under `/tmp/opensip-implementation/reviews/codex2-x7-r7`. Don't run cargo.


**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- No product builds or test runs. Timing-sensitive lanes may be using this machine. Do not run any lead set.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What is asked

J1 r5's successor table gives X7 r7 "items 1, 3, 4 and 8 (items 7 and 8)" (J1:855). 8.6 lists the changes (J1:660-665):
- item 1, J1 item 7's order;
- item 3, the row `Refused(Interrupted { signal })` and the outcome-first precedence;
- item 4, step 1's terminality, the output decision point, phase D's row and phase O's deferral;
- item 8, the interrupted branch;
- four forbidden substitutes.

X3d r9, now accepted, adds the row "operator stop" and says "X7 r7 (S9) projects it" (X3D9 S10.5). It also has J3b's host side read `admitted_at_close()` (X3D9 S10.11).

The questions:
- **Faithfulness.** Is r7's S9 section exactly J1 r5's S9, read with the bound successors S18 and S21?
- **The lead decisions.** Does each of LD7-1 to LD7-5 decide only a point that J1 and X3d r9 leave open, and decide it soundly?
- **Findings.** Any of these is a finding:
  - a change that goes beyond J1 r5's S9;
  - a change that decides anything of X3d r9's or X4 r8's;
  - something a consumer needs that r7 misses.
- **Preservation.** No accepted outcome of X7 r6, or of another law, changes, apart from S9's declared changes.

## Pins

The pins are in `hashes.txt`. Apart from the subject and this request, every pin is an accepted snapshot, a bound successor, or the review record that accepted one.
- **The subject:** `docs/implementation/m2/finalization-x7/PROPOSAL.md`, X7 r7. It is the subject of `subjectSha256`.
- **The diff base:** `finalization-x7/PROPOSAL-r6.md` (`9e17faf2…`, 28,729 bytes).
  - These are the r6 bytes Grok accepted, without the acceptance note. They equal `reviews/grok-record-x3d-r7-x7-r6-x9-r3/x7/review.json`'s `subjectSha256`.
  - The snapshot already existed. It was checked, not rewritten.
  - Diff PROPOSAL-r6.md against PROPOSAL.md.
- **S9's source:** J1 r5, `m3/host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`, = `m3/reviews/codex-host-pipeline-j-r5/review.json`'s `subjectSha256`). r7 cites it as J1. The parts used:
  - 5.2 and 5.3 (J1:391-421) and item 7 (J1:476-510);
  - 8.1's results and REV reason (J1:537-542), and 8.2 to 8.4 (J1:549-640);
  - 8.6's X7 list (J1:660-665) and 8.7 (J1:667-693);
  - rows 36 to 48 (J1:762-774) and S12-D and S12-O (J1:838-839);
  - S9 (J1:855), J3b and J3d (J1:882-883), and the forbidden substitutes (J1:913-917).
- **The sibling:** X3d r9, **accepted** by Grok: `m2/commit-session-x3d/PROPOSAL-r9.md` (`c727001a…`, = `reviews/grok2-x3d-r9/review.json`'s `subjectSha256`). r7 cites it as X3D9.
  - The parts used: S10.2, S10.3, S10.5, S10.6, S10.9, S10.11 and LD9-3.
  - Grok's `REVIEW.md` is pinned for one line: the projection clauses of J1:914 are X7 r7's ("Forbidden substitutes" paragraph).
  - The live `PROPOSAL.md` carries the acceptance note, so it is not pinned.
- **The bound successors:**
  - **S18** (`m3/host-pipeline-j/s18/successor.json`; accepted by GROK2, `m3/reviews/codex2-s18-r2/review.json`; bound at product `5214350`);
  - **S21** (`m3/host-pipeline-j/s21/successor.json`; accepted at r2 by Grok, `m3/reviews/codex2-s21-r2/review.json`, directory name kept; bound at product `3f6f9a5`). Its passages are `s21/PASSAGES.md`.
- **The consumer:** M3-L r5, accepted in review, `m3/provider-protocol-l/PROPOSAL-r5.md` (`f654ee4e…`), items 16e, 16f and 18.
- **Not pinned:** X4 r8 (S11), drafted beside this revision and in its own review (`reviews/codex2-x4-r8`). r7 relies on nothing in it, because the port reaches the gate only through X3d r9's token.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `cca4fe4`, read-only.
  - Main has since moved to `d2c00a9`. `git diff cca4fe4 d2c00a9` touches none of the cited files.
  - J3b and J3d are not integrated.
  - The cited files:
    - `crates/host/src/finalization.rs`:
      - `:256-262`, `DeliveryPhase`;
      - `:283-319`, `deliver`, `required` and the `x7.delivery` points;
      - `:395-460`, `finalize`;
      - `:476-565`, the projection.
    - `crates/host/src/installation_termination.rs:21-28`, where `InstallationTerminationV1` requires `error_code`, and `:60`, `installation_termination`.
    - `crates/host/src/delivery.rs:17-21`, `deliver_required`.
    - `apps/cli/src/bootstrap.rs:36-60`, the coded line and "never append a replacement envelope".
    - `crates/security/src/custody/commit_session.rs:529-545`, `refused()` and `undetermined()`.
    - The five callers of `installation_termination`: `maintenance.rs`, `crash_matrix_support.rs`, `doctor_report.rs`, `recovery_route.rs` and `finalization.rs`.

## The shape of the diff

There are two replaced lines:
- the title;
- the r6 header's first line. It gains "r6 ACCEPTED by Grok on 2026-10-04.", the acceptance note already in the working law.

Everything else is inserted. No r6 sentence is deleted or reworded. The insertions are:
- **The r7 header,** after r6's header and before "## Problem": the parts, the sources, and the "r7 changes" table.
- **Short "r7 (S9)" notes** in items 1, 2, 3, 4, 8, 9, 10 and 11.
- **The new section "S9 (r7)"** (S9.1 to S9.9), after item 11.
- **One forbidden-substitute group** and one "Not claimed" line.

## What r7 decides

1. **S9.1, item 1: the order.** It is J1 item 7's:
   1. the session, opened at R12;
   2. replay;
   3. `prepare_commit` and `publish`;
   4. `finish`;
   5. the projection in phase D;
   6. the output decision point;
   7. phase O: SOP2's finalization, then rendering and output;
   8. settlement.

   `finalize` takes the open session and no `admit` closure. Every end before the commit goes through `refused()` and `finish`, once. Every end runs one step 1.
2. **S9.2, the cancellation port (LD7-2).** It has points P1 to P6.
   - **The token.** It is taken at the opening entry. It goes to the host's port only when `prepare_commit` returns `Ok(PreparedCommit)`. The port then latches at once if a signal was already observed ("handled as B"), and otherwise at once on the first signal while `publish` runs.
   - **P4.** It hands the port `admitted_at_close()` and whether the return enters D.
   - **P5.** It is the single cancellation check. It starts O.
3. **S9.3, item 3: the projection.** It is decided once, at P5, on the returned outcome first and then on whether a signal was observed:
   - **rule 1:** `CommitUndetermined` takes the durability row;
   - **rule 2:** a latched `Committed` takes F39, whatever the latch source;
   - **rule 3:** an unlatched `Committed` with a signal takes `interrupted` 130 with the runId (phase D);
   - **rule 4:** everything else with a signal takes `interrupted` 130 with no runId, the operator stop `Refused(Interrupted { signal })` included.

   S21 is bound, so rules 1 and 2 apply to signals now.
4. **S9.4, item 4: step 1.**
   - **The split.** `DeliveryPhase::render` splits into the D projection and O's rendering of the decided envelope.
   - **Phase O.** SOP2's hook runs, then the rendering, then `deliver_required`. A signal in O is deferred. A renderer failure takes F16 when a `PublishedCommit` exists, and row 44 otherwise. A write failure after the first byte has no replacement. An unrenderable failure envelope gives the one coded line.
   - **Settlement** is the output's return.
5. **S9.5, item 8.** `Interrupted { signal, run: Option<AuthoritativeRun> }`, with no errorCode and no wildcard arm. The host's coded projection gets an explicit `Interrupted` arm, which returns the invariant row and which finalization never reaches (LD7-3).
6. **S9.6, item 2.** Phase D's envelope takes its label and runId only through `&PublishedCommit`.
7. **S9.7, coverage, tests and units.**
   - **J1's controls,** X7's halves: J-C12, J-C14, J-C14b, J-C15b's projections and J-C16, with rows S12-D and S12-O.
   - **New tests:** T7-1 to T7-8.
   - **Units:** J3b carries finalization's part, and J3d carries O's wiring.
8. **S9.8, the lead decisions.**
   - **LD7-1.** Every facade call stays in `finalization.rs`, through an opening entry and an ending entry that the pipeline calls.
   - **LD7-2.** The port and the token's custody.
   - **LD7-3.** The interrupted branch, and the coded projection's invariant arm.
   - **LD7-4.** The `x7.delivery` points keep their reach. `x7.delivery.required` moves after P5 and SOP2's hook, as S12-O needs.
   - **LD7-5.** A failed D projection is F16 with no signal. A signal in D discards it, and the envelope is `interrupted` with the runId.
9. **S9.9, cross-law items.**
   - **X3d r9 and X4 r8:** none.
   - **X5 r4 (S8):** owed. Its order is assumed.
   - **J2a:** the failure envelope's bytes.
   - **X9 r17:** S12-D, S12-O, the re-transcription of the host drivers, and LD7-4's census.
   - **O1:** SOP2's hook.
   - **468's host projection:** LD7-3's arm.

## Decide

1. **Faithfulness.** Does S9 carry exactly J1 8.6's X7 list and the S9 row (items 1, 3, 4 and 8), citing each? Is it read correctly with S18 and S21? Does anything go beyond J1 r5, or decide anything of X3d r9's (the token, the window, the sample, the row itself) or of X4 r8's (the gate word)?
2. **The projection (S9.3).**
   - Is the table J1 8.3's, with the outcome first, never the gate's state?
   - Is the operator stop row projected as J1 says: the A/B `interrupted` envelope, with no runId?
   - Are rows 38, 42, 46 and 47 right?
   - Is S21 bound, so that the rule-1 and rule-2 signal cases may now run?
   - S9.3's last bullet notes that rule 4 sends an `ExistingAttempt`'s and an exhausted generation's disclosures only to the operational record when a signal was observed. Is that J1's and S21's reading, or a gap?
3. **Step 1 and phase O (S9.4).**
   - Is the split of `DeliveryPhase::render` the one J1:663 names?
   - Is "every decided envelope is rendered in O" right against item 4's "a failed or latched attempt never opens a delivery phase", which r7 keeps for the Run's own delivery?
   - Are the failure routes J1 8.2 row O's and S18's?
4. **LD7-1.** Is keeping every facade call in `finalization.rs`, through two entries, right against J1 item 7 ("opened by the pipeline") and X5 item 6? Or should the pipeline call `open`, `refused()` and `finish` itself?
5. **LD7-2.** Two questions:
   - **Is the token custody sound?** X3d r9 makes the token single-use, and a call outside the window consumes it. Does handing it over only at `Ok(PreparedCommit)` lose any signal that J1 requires to latch at once? In particular, does it change the outcome of a signal in phase B before `prepare_commit` returns? J1:555 and J1:567 ("Scope") say how such a signal is handled.
   - **Are the port's duties at P1 to P6 the ones finalization must own?** Or do they intrude on J3b's and J3d's host cancellation source?
6. **LD7-3.** Is an explicit invariant arm in the host's coded projection acceptable for a row only finalization can meet? Or is a different form required?
7. **LD7-4 and LD7-5.**
   - Do the `x7` points keep their census reach, with `x7.delivery.required` after P5 as S12-O needs (J1:839)?
   - Is LD7-5's reading of J1:558 right for a failed projection?
8. **Controls and units.** Do J1's controls and T7-1 to T7-8 cover every part of S9 and every lead decision? Is the J3b and J3d split J1's (J1:882-883)?
9. **Preservation.** Does every r6 sentence survive verbatim, apart from the title and the acceptance note? Apart from S9's declared changes, does any accepted outcome of X7 r6 or of another law change?
10. **Anything else wrong.**

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with an id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"noAcceptedOutcomeChanged"`: true or false, judged apart from S9's declared changes;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"preservedSnapshot"`: PROPOSAL-r6.md's path, bytes and sha256.

Do not commit.
