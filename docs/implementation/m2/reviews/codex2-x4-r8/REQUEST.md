CODEX2 review: law X4 r8, the live-guards law. r8 is an amendment, J1's successor **S11**: the gate word for the commit-phase cancellation latch.

This is a **law review**. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-x4-r8.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git read-only.
- No product builds or test runs. Timing-sensitive lanes may be using this machine. Do not run any lead set.
- Never touch the real home: `~/Library/Application Support/OpenSIP` must stay absent.
- Never read the private 413 UUID fixture.

## What is asked

J1 r5 decided S11 and named X4 r8 as its vehicle: "the cancellation latch as a gate source; the two window bits in the gate's word, preserved by every compare-exchange loop and never reset (8.1)" (J1:857).

X3d r9, now accepted, carries X3d's half of the latch: the token, where the window opens and closes, the results and the sample. It leaves five things to X4 r8 (X3D9 LD9-4, LD9-5, S10.11):
- the word's encoding;
- the masked compare-exchange loops;
- the state decoding;
- the never-reset rule;
- the record of `StopCause::Operator`.

The questions:
- **Faithfulness.** Is r8's S11 section exactly what J1 r5 and X3d r9 assume?
- **The lead decisions.** Does each of LD8-1 to LD8-5 decide only a point they leave open, and decide it soundly?
- **Findings.** Any of these is a finding:
  - a change that goes beyond J1 r5's S11;
  - a change that decides anything of X3d r9's half or X7 r7's (S9);
  - something a consumer needs that r8 misses.
- **Preservation.** No accepted outcome of X4 r7, or of another law, changes, apart from S11's declared changes.

## Pins

The pins are in `hashes.txt`. Apart from the subject and this request, every pin is an accepted snapshot or the review record that accepted one.
- **The subject:** `docs/implementation/m2/live-guards-x4/PROPOSAL.md`, X4 r8. It is the subject of `subjectSha256`.
- **The diff base:** `live-guards-x4/PROPOSAL-r7.md` (`fc8490f4…`, 26,577 bytes).
  - These are the r7 bytes Grok accepted, without the acceptance note. They equal `reviews/grok-live-guards-x4-r7/review.json`'s `subjectSha256`.
  - **The snapshot is new.** No r7 snapshot existed, so this drafting created it. It was made by removing exactly the 35-byte note " r7 ACCEPTED by Grok on 2026-10-01." from the working law, and its sha256 was checked against the review.
  - Diff PROPOSAL-r7.md against PROPOSAL.md.
- **S11's source:** J1 r5, `m3/host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`, = `m3/reviews/codex-host-pipeline-j-r5/review.json`'s `subjectSha256`). r8 cites it as J1. The parts used:
  - 8.1 (J1:514-542) and 8.3's last paragraph (J1:598);
  - 8.6's X4 line (J1:659) and the S11 row (J1:857);
  - J-C15 and J-C15b (J1:684-691), J3b (J1:882), and the forbidden substitutes at J1:913 and :916.
- **The sibling:** X3d r9, **accepted** by Grok with no required findings: `m2/commit-session-x3d/PROPOSAL-r9.md` (`c727001a…`, = `reviews/grok2-x3d-r9/review.json`'s `subjectSha256`). r8 cites it as X3D9.
  - The parts used: S10.2 to S10.5, S10.8, S10.9, LD9-3 to LD9-5, and S10.11.
  - Grok's `review.json` is pinned for its one observation, NBO-1: the window bits are S11's, not S10's.
  - The live `PROPOSAL.md` carries the acceptance note, so it is not pinned.
- **The consumer:** M3-L r5, accepted in review, `m3/provider-protocol-l/PROPOSAL-r5.md` (`f654ee4e…`, = `m3/reviews/grok-provider-protocol-l-r5/review.json`'s `subjectSha256`), items 16f and 18.
- **Not pinned:** X7 r7 (S9), drafted beside this revision and in its own review (`reviews/codex2-x7-r7`). r8 decides nothing for it and relies on nothing in it.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `cca4fe4`, read-only.
  - Main has since moved to `d2c00a9`. `git diff cca4fe4 d2c00a9` touches none of the cited files.
  - J3b is not integrated.
  - The cited files:
    - `crates/security/src/commit_authority.rs`:
      - `:8-48`, the gate: `ADMITTED`, `LATCHED`, the decoder's `unreachable!` arm, `admit`'s compare-exchange from a literal 0, and the latch's `fetch_or`;
      - `:83-116`, `OperationGate`.
    - `crates/security/src/custody/operation_guard.rs`:
      - `:96-131`, `StopCause`, first cause wins;
      - `:199-226`, `Shared.cause`, `record`, the placeholder `latched()` and `lock`;
      - `:255-262`, the observer's latch and record;
      - `:419`, `OperationGuard::stop`, a cause-less latch;
      - `:512-518`, `admit`'s refusal;
      - `:543-575`, the checkpoint: the stale path at `:547-549`, step 3 at `:563-566`, and the boundary check at `:570-574`.
    - `crates/security/src/revocation.rs:121-193`, where the monitor latches before it returns an error.
    - `crates/security/src/custody/commit_session.rs:94-101`, `RevReason::of`.

## The shape of the diff

There are two replaced lines:
- the title;
- the r1–r7 history paragraph. It gains "r7 ACCEPTED by Grok on 2026-10-01.", the acceptance note already in the working law, as in earlier rounds.

Everything else is inserted. No r7 sentence is deleted or reworded. The insertions are:
- **The r8 header,** before "## Problem": the parts, the sources, and the "r8 changes" table.
- **Short "r8 (S11)" notes:**
  - item 2, the gate's word;
  - item 3, step 4's masked `admit`;
  - item 7, the third source;
  - item 8, `StopCause::Operator` and its row, by reference;
  - item 10, F41 and W-1 to W-7;
  - item 11, X4's part of J3b.
- **The new section "S11 (r8): the gate word"** (S11.1 to S11.12), after the r5 block.
- **One forbidden-substitute group,** "The gate word (r8, S11)", and two "Not claimed" lines.

## What r8 decides

1. **S11.1, the word.**
   - **The bits.** `ADMITTED` 1 and `LATCHED` 2 are the state bits. `WINDOW_OPEN` 4 and `WINDOW_CLOSED` 8 are the window bits. Bits 4 to 7 are never set (LD8-1).
   - **The state law, unchanged.** The state is `word & 3` (0..3), and every reader decodes it. The transitions stay 0→1, 0→2 and 1→3.
   - **The window's four combinations.** `WINDOW_OPEN` and `WINDOW_CLOSED` are independent flags, so there are four.
2. **S11.2, the operations.**
   - **`admit`** is a strong compare-exchange loop. It requires state 0 and sets `ADMITTED`. Today's literal 0 → 1 exchange would refuse every admission once the window is open.
   - **The existing latch** is unchanged: one `fetch_or(2)`.
   - **The cancellation latch** is a compare-exchange loop inside the stop-cause record's lock. Its results are `OutsideWindow` (tested first), `AlreadyStopped`, `BeforeAdmission` or `AfterAdmission`.
   - **The opening and the close** are one `fetch_or` each. The close returns the prior word's decoded state as the sample.
   - **Order.** Everything is `SeqCst` on one atomic.
3. **S11.3, the gate never resets.** No operation clears a bit. Each bit is set at most once, the window bits included.
4. **S11.4, at most one permit.** The only producer is `admit`'s exchange from state 0. The window bits neither enable nor refuse admission.
5. **S11.5, how each source sets the bits.** The existing sources ignore the window. The cancellation latch acts only inside it.
6. **S11.6, the first stop and `StopCause::Operator`.**
   - **The record.** X4a's first-cause rule is recorded.
   - **The variant.** `Operator { signal }` is recorded from X3d r9 LD9-4. Its `REV` reason and its row are X3d r9's.
   - **The first stop** is the exchange that set the latch bit. `AlreadyStopped` records nothing.
7. **S11.7, what does not change.**
8. **S11.8, controls W-1 to W-7.** These are J-C15's and J-C15b's gate halves, the exhaustive word trace, and the tests for LD8-2 to LD8-4.
9. **S11.9, units.** X4's part of J3b, which lands with X3d r9's latch code after r8 is accepted.
10. **S11.10, the lead decisions.**
    - **LD8-1.** The bit values.
    - **LD8-2.** Strong compare-exchange. `admit` makes at most three exchanges, and the cancellation latch at most two.
    - **LD8-3.** The cancellation latch's exchange and its `Operator` record are one critical section of the stop-cause record's lock. This closes a race in which a checkpoint, on the session thread, records the placeholder `FailStop { latched }` between the exchange and the record. Without it, an operator stop would end on `OBSERVER.FAIL_STOP` 4 with `REV(observer-fail-stop)`.
    - **LD8-4.** `x4.gate.latch.after` follows a successful exchange and its record, outside the lock, and never a no-op.
    - **LD8-5.** The close returns only the decoded state. The opening returns nothing. Both are crate-private.
11. **S11.11, D8-1, disclosed and not decided.** X4a's placeholder record can still win against two existing latches:
    - **X3d's cause-less stop.** An observer tick before `finish` can turn `REV(operation-stopped)` into `REV(observer-fail-stop)`.
    - **The checkpoint's stale path.** The refusal row can become `OBSERVER.FAIL_STOP`.

    Neither touches the operator stop. Lead decision: route this to a follow-up, X4-F3, rather than amend X3d r9's and X4a's existing sources here.
12. **S11.12, cross-law items.**
    - **X3d r9:** none required. Two readings are offered as record notes.
    - **X7 r7, J1, X8 and X9 r17:** none.

## Decide

1. **Faithfulness.** Is the word exactly J1 8.1's? That means:
   - two window bits in the gate's own `AtomicU8`, beside the state bits;
   - one total order;
   - `admit`, `observe` and the existing latch masking the window bits;
   - the opening and the close as `fetch_or`s, with the close's prior value as the sample;
   - every compare-exchange loop preserving the window bits;
   - never-reset.

   Is it exactly what X3d r9's S10.2, S10.3 and S10.4 assume: the four results in their order, the sample's state bits, and "first stop"? Does r8 decide anything that is X3d r9's or X7 r7's?
2. **The state law and F41.** Do the 0..3 state law, F18, F38, F39 and F41 survive with three sources and the window? Is S11.4's one-permit argument complete? Is it right that a closed window does not refuse `admit`?
3. **The masked loops (LD8-2).** Is the bound argument right: the word only gains bits, and a strong exchange fails only on a change? Is rejecting weak compare-exchange right? Is S11.2's account of why today's literal-0 `admit` cannot stay correct against `commit_authority.rs:31-38`?
4. **LD8-3.** Against `operation_guard.rs`, does the race exist as stated? Does taking `Shared.cause`'s lock across the exchange and the record close it for every reader? Those readers are:
   - checkpoint step 3;
   - `admit`'s refusal;
   - the boundary check;
   - an observer tick.

   Does the lock introduce any wait, deadlock or lock-order change? Are the rejected alternatives right?
5. **LD8-4 and LD8-5.** Is "after a successful exchange and its record, outside the lock" the right reading of J1:532's "fires after it" and of X3d r9 S10.9's reuse? Should `OutsideWindow` or `AlreadyStopped` reach the point? Is the close's narrowed return right?
6. **`StopCause::Operator` (S11.6).** Is the record faithful to X3d r9 LD9-4 (variant, `REV` mapping and row are X3d's; X4 records only)? Is the first-cause rule as stated a faithful record of X4a's code?
7. **D8-1.** Is the disclosure accurate against the cited lines? Is routing it to X4-F3, rather than fixing it in r8, acceptable? Or does it falsify something r8, J1 r5 (J1:598) or X3d r9 (S10.4) needs, so that it must be fixed here?
8. **Controls and units.** Do W-1 to W-7 cover J-C15's and J-C15b's gate halves and each lead decision? Is the J3b split with X3d r9 right?
9. **Preservation.** Does every r7 sentence survive verbatim, apart from the title and the acceptance note? Apart from S11's declared changes, does any accepted outcome of X4 r7 or of another law change?
10. **Anything else wrong.**

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with an id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"noAcceptedOutcomeChanged"`: true or false, judged apart from S11's declared changes;
- `"subjectSha256"`: PROPOSAL.md's sha256;
- `"preservedSnapshot"`: PROPOSAL-r7.md's path, bytes and sha256.

Do not commit.
