# S21 — the commit-outcome exception to WS's before-settle rule (contract successor of law M3-J1)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r2, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs Grok's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`.

**Review history.** r1 (subject `090de59f…`) was reviewed by Grok in `reviews/codex2-s21-r1/`; the directory keeps the name of its first CODEX2 assignment. The verdict was REQUIRED-FINDINGS, with one required finding (RF-1) and no non-blocking observations.
- **Accepted:** LD-1 to LD-5, LD-7 and LD-8, the line-226 text itself, and selection at `218465f` (rulings R1 to R6).
- **Rejected:** LD-6, for WS:229 and WSE:233 only. Grok kept WS:1393 unchanged.

r2 answers RF-1 and changes nothing else of substance. The r1 members r2 changes are kept, byte for byte, in `reviews/codex2-s21-r2/r1-members/`.

**What it is.** Accepted law **M3-J1 r5** keeps 8.3's rules 1 and 2 against WS:226 (lead decision LD-r5-2, J1:600-627):
- **Rule 1.** A signal observed before settlement that meets a `CommitUndetermined` takes the durability row, with the ExecutionId (IE:1680-1681).
- **Rule 2.** A signal that meets a `Committed(PublishedCommit)` latched after admission takes the `DELIVERY.REQUIRED_FAILED` row, with the runId (SL:551-554).

WS:226 still makes every before-settle aggregate `interrupted` (130). J1 records the WS fix as an owed successor, **S21** (J1:868): "a passage successor to WS:226 and to WSE:226". S21 is that successor, in two parts:
- **The exception.** It is stated on WS:226 and on the matching line of WS's selected effective copy.
- **(r2, RF-1) The per-kind sentence.** The same paragraph's "Per kind: an analysis attempt aborts and leaves no Run" (WS:229, WSE:233) would be false under the exception, so it is qualified to "an analysis attempt that the signal aborts leaves no Run".

Nothing else in WS changes.

**What waits on it** (J1:606-617):
- J3d's durable signal wiring;
- J-C14's rule-1 and rule-2 signal cases;
- J-C15b's phase-C projections;
- X9 rows S12-C and S12-U.

J2a's pure model, J3b's latch code, and rows S12-B and S12-D may go ahead.

**Product.** Main `6190e66`, read only, with 92 contract successors (SYN-NS was bound after r1, which was built on `218465f` with 91). S18 has been bound since `5214350`. S21 binds at `6190e66`, 92 to 93 (see "Evidence runs").

## r2 changes and review response

| Finding | Change |
|---|---|
| **RF-1** (the per-kind sentence contradicts the exception) | **Two new line overrides**, WS:229 and WSE:233, with the same `before` and `after`. The `after` is Grok's replacement text, verbatim: <br>- before: "Per kind: an analysis attempt aborts and leaves no Run; an import discards its" <br>- after: "Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its" <br>The line still ends "an import discards its", so the next line's "staged bytes;" still joins (WS:230, WSE:234). Both lines are free at `6190e66`. S18 binds neither: WSE:229, which S18 binds, is a different line. LD-6 is amended to match. r1's cross-law item 6 (a later WS successor for this sentence) is withdrawn, because S21 now makes the change. Grok's text adds "that" to r1's proposed wording. |
| Base and records | The base is `6190e66`, read with `git show`. No lock entry is on any of S21's four selectors there. `verify_design.py` and INV5 are byte-identical to `218465f`. `build_s21.py` emits the review path `codex2-s21-r2`, and the unit draft is renewed. |

**What r2 changes, by member.** The diff base is the r1 subject, `090de59f…`. Every member changes:
- `successor.json`:
  - the two new overrides;
  - the `standing`, which now names WS:229 and WSE:233;
  - the candidate pins.

  The two line-226 overrides, their `before` and `after` included, and the parents are byte-identical to r1.
- `PASSAGES.md` and `evidence/reading-report.json` are regenerated. They show four overrides, the base `6190e66`, and the per-kind sentence as it now reads.
- `evidence/build_s21.py`, `check_s21.py` and `verify_scratch.py` are updated for four overrides and the new base.
- This README is updated.

## Short names

| Name | Document |
|---|---|
| **J1** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md`, the M3-J1 r5 bytes Codex accepted (146,331 bytes, `4ccb2320…`; `reviews/codex-host-pipeline-j-r5`). It is cited by line. |
| **RF-1** | Grok's finding on S21 r1, in `reviews/codex2-s21-r1/review.json` |
| **WS** | `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (133,335 bytes, `1ee203e3…`), an accepted lock input |
| **WSE** | `docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md` (139,497 bytes, `4478ce1a…`), WS's selected effective copy |
| **S18** | the bound final-output-section successor, `host-pipeline-j/s18/successor.json` (GROK2 ACCEPT-DESIGN-UNIT at r2; product `5214350`). On WS it binds lines 225, 227, 228, 231 and 1393, and on WSE lines 225, 229, 230, 235 and 1466. |
| **IE, SL** | `docs/v2/contracts/product-v1/{identity-and-evidence, security-and-lifecycle}.md`, accepted lock inputs. IE:1680-1681 is in IE §5, and SL:551-555 is in SL S6. No bound entry touches either passage. |
| **X3D, X7** | `docs/implementation/m2/commit-session-x3d/PROPOSAL-r8.md` (`5e491b92…`) and `finalization-x7/PROPOSAL-r6.md` (`9e17faf2…`) |
| **INV5** | `opensip/schemas/sources/invocation-v5.schema.json` at `6190e66` (unchanged since `218465f`) |
| **CINV** | `docs/coop/design-corrections/workflows/command-inventory.v3.json` |

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: all four overrides with exact `before` and `after`, and the cancellation paragraph as it reads with S18 and S21 on each parent |
| `successor.json` | the contract successor record: two parents (WS, WSE), four passage overrides, no supersession, six candidates |
| `evidence/reading-report.json` | generated: the bound entries on WS and WSE at `6190e66`, S18's and S21's lines, and the effective cancellation paragraph line by line with each line's owner |
| `evidence/build_s21.py` | builds every generated file, the record, the subject manifest and the unit draft; `--check` compares instead of writing |
| `evidence/check_s21.py` | read-only, independent checks: pins, the lock and S18's lines, unbound records, the readings across S18's lines and into the per-kind sentence's next line, content, no new code, exit or fault cause, and every citation |
| `evidence/verify_scratch.py` | runs the real `verify_design` with a synthetic review and assent, and a conflicting-override probe |
| `../s21-subject.json` | the subject manifest (generated) |
| `../s21-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, with the review path `reviews/codex2-s21-r2/review.json`; not part of the subject |

## What changes

**Four line overrides**, two on each parent. WS:226 and WSE:226 are the same text, as are WS:229 and WSE:233, and each pair has byte-identical `before` and `after`.

**WS:226 and WSE:226 (r1, unchanged in r2).** Before:

> `cancelled`, the aggregate is `interrupted` (130), and a Run committed by an earlier

After:

> `cancelled`, and the aggregate is `interrupted` (130) unless a required analysis or verify step's commit returned one of two outcomes, which govern instead (contract successor S21 of law M3-J1 r5): an undetermined commit is `operational-failed` (4) with `DURABILITY.COMMIT_FAILED`, fault cause `durability-commit`, no `runId` and the attempt's ExecutionId disclosed for read-only recovery (identity-and-evidence §5's `durability-undetermined`); a commit whose FinalGate was latched after admission stays committed and is `operational-failed` (4) through `DELIVERY.REQUIRED_FAILED` (`delivery-required`), with its `runId` (security-and-lifecycle S6's selected law). The outcome the commit returned decides, never the gate's latch state alone. In the `interrupted` case, a Run committed by an earlier

**WS:229 and WSE:233 (r2, RF-1).** Before:

> Per kind: an analysis attempt aborts and leaves no Run; an import discards its

After:

> Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its

**How it reads.** S18's WS:225 ends "…: remaining steps are", and S18's WS:227 begins "step is named in the termination's `runId`." So the sentence reads: before-settle → remaining steps `cancelled` → `interrupted` (130) unless one of the two commit outcomes governs → "In the `interrupted` case, a Run committed by an earlier step is named in the termination's `runId`." Then S18's *after-settle* definition follows unchanged, and then: "Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its staged bytes; …".
- **WSE.** Line 227 instead continues with the optional-Run sentences ("This includes optional analysis/verify steps…"), and they read on unchanged. The per-kind sentence is WSE:233.
- **The per-kind sentence now covers only the attempts the signal aborts.** That is an attempt the signal stops in phase A or B, through `refused()` and a checkpoint refusal. It no longer covers a commit that stayed committed or whose outcome is undetermined.
- `PASSAGES.md` prints the whole paragraph as it reads on each parent.

Nothing else changes: no other WS or WSE line, and no code, class, exit, field, fault cause, step outcome, public code, schema, inventory or product file.

## J1's S21 row, item by item

| J1 r5 (J1:868, with 8.3 at J1:588-627) | Where S21 carries it |
|---|---|
| "A signal observed before settlement leaves the aggregate `interrupted` (130), except where the analysis attempt's commit outcome governs" | WS:226: "the aggregate is `interrupted` (130) unless a required analysis or verify step's commit returned one of two outcomes, which govern instead" (scope: LD-3) |
| "An undetermined commit takes IE:1680-1681's durability termination with its ExecutionId" (rule 1, J1:589) | WS:226: "an undetermined commit is `operational-failed` (4) with `DURABILITY.COMMIT_FAILED`, fault cause `durability-commit`, no `runId` and the attempt's ExecutionId disclosed for read-only recovery (identity-and-evidence §5's `durability-undetermined`)". The code is IE:96's and X3D:283's, and the fault cause is WS:1360's. |
| "A commit latched after FinalGate admission takes SL:551-554's `DELIVERY.REQUIRED_FAILED` row" (rule 2, J1:590) | WS:226: "a commit whose FinalGate was latched after admission stays committed and is `operational-failed` (4) through `DELIVERY.REQUIRED_FAILED` (`delivery-required`), with its `runId` (security-and-lifecycle S6's selected law)". The detail stays X7's (LD-5). |
| "Each is operational-failed 4 (8.3, rules 1 and 2)" | both outcomes, as quoted |
| X3d's returned outcome matched first; "the gate's state 3 alone proves neither a commitment nor a RunId" (J1:588, J1:605) | "The outcome the commit returned decides, never the gate's latch state alone" (LD-4) |
| "It adds no class, code or exit" | `check_s21.py`: every code is already in WS, IE or SL; every fault cause is in WS:1360-1361; every exit is in the fixed table; the per-kind line adds none |
| "leaves S18's lines (WS:225, :227-228, :231) as they are" | S21 selects lines 226 and 229 on WS, and 226 and 233 on WSE. `build_s21.py` and `check_s21.py` assert that S18 binds its five lines on each parent and that S21 selects none of them. |
| "S21 is to override WS:226 and WSE:226" (J1:605) | the two line-226 overrides |
| (r2, RF-1: not in J1's row) the same paragraph's per-kind sentence, which the exception makes false | the WS:229 and WSE:233 overrides (LD-6) |

## Why this form

- **All four lines are free.** In the lock at `6190e66`:
  - WS's bound lines are 225, 227, 228, 231 and 1393 (S18), 308 (CRC-1), 598 and 603 (I1-L), and 1296 (initial-root-binding);
  - WSE's are 225, 229, 230, 235 and 1466 (S18), 312 (CRC-1), 602 and 607 (I1-L), and 1300 (initial-root-binding).

  WS:226, WS:229, WSE:226 and WSE:233 are none of them. No unbound successor record in arch touches any of the four either.
- **S21 needs none of S18's lines.**
  - **Line 226** holds the whole consequence of the before-settle rule: "remaining steps are" ends S18's line 225, and "step is named in the termination's `runId`" begins S18's line 227. So S21's line-226 `after` keeps the line's first word, `cancelled`, and its last words, "a Run committed by an earlier".
  - **The per-kind line** keeps its first words, "Per kind:", and its last words, "an import discards its", so the next line still joins.
- **The probe.** `verify_scratch.py` shows that a later conflicting override of WS:226 is refused ("conflicting contract passage overrides").

## Lead decisions

Each decision is dated 2026-10-04 and made under the owner's standing direction to proceed on the lead's recommendation. Each names the alternatives it rejects, and the owner may reverse any of them. Grok accepted LD-1 to LD-5, LD-7 and LD-8 in r1. LD-6 is amended in r2 for RF-1, and LD-1 and LD-2 now cover the per-kind lines.

**LD-1. The form: one line override on each of WS:226 and WSE:226, and (r2) on each of WS:229 and WSE:233.**
- **Rejected:**
  - **a complete copy of WS and WSE.** The lines are free, and a copy of a lock input would have to carry every bound override (S18, CRC-1, I1-L, initial-root-binding) and a selection statement. That is disproportionate for these lines;
  - **overriding any line S18 binds.** `verify_design` refuses a second override of a bound line, and the lead's direction forbids it;
  - **stating the exception in a new paragraph on another line**, for example after WS:231 or at WS:233. WS:226 would still state `interrupted` unconditionally, and another WS line would change.

**LD-2. WSE takes the same overrides.** This follows I1-L's LD-L5 and S18's LD-2. WSE:226 is the same text as WS:226, and WSE:233 is the same text as WS:229.
- **Rejected:** WS alone, which would leave the selected effective copy contradicting WS.

**LD-3. Scope: "a required analysis or verify step's commit".** J1's row says "the analysis attempt", and M3 has only that one, step 0. IE:1680-1681 and SL:551-554 are commit-protocol rows, though, not analysis rows. WS:82 lets verify steps commit Runs too. The before-settle consequence is about the aggregate, which is over required steps only (WS:233-235).
- **Rejected:**
  - **analysis only.** A verify commit would keep the same conflict, and another WS successor would be owed when verify lands;
  - **any step's commit, optional included.** WS:235 says an optional step's rejection or failure never changes the aggregate, and S21 does not reopen that. The pre-existing question it raises is cross-law item 5.

**LD-4. The returned outcome decides, never the latch state alone.** This is J1 8.3's first sentence (J1:588) and X3D:170's state-3 rule: the commit's own outcome stands. A latch after admission followed by an undetermined evidence `COMMIT` is rule 1, never rule 2.
- **Rejected:** omitting it. The exception would then admit a reading by gate state, which J1-R1 closed.

**LD-5. What the WS text names.**
- **Rule 1** is named in full: operational-failed 4, `DURABILITY.COMMIT_FAILED` (IE:96; X3D:283), fault cause `durability-commit` (WS:1360), no `runId`, and the ExecutionId disclosed for read-only recovery (IE:1680-1681).
- **Rule 2** is named as SL names it: the `DELIVERY.REQUIRED_FAILED` path (`delivery-required`, WS:1133), with its `runId`, the Run staying committed.
- **Rejected:**
  - **naming rule 2's detail, `DELIVERY.RENDERER_FAILED_AFTER_COMMIT`, in WS.** The detail is X7's F39 row ("the F16 row", X7:100; J1's row 42). WS:1376's row describes a renderer that failed, a different situation, and SL names only the path;
  - **citing J1's line numbers inside WS.** WS names laws, as B-S1 and S18 do.

**LD-6 (amended in r2, RF-1). The per-kind sentence is qualified, and nothing else in WS changes.**
- **WS:229 and WSE:233** become "Per kind: an analysis attempt that the signal aborts leaves no Run; an import discards its". This is Grok's replacement text.
  - Under the exception, a commit latched after admission stays committed with its RunId (SL:552-554), and an undetermined commit stays admitted, its caller receiving `DURABILITY.COMMIT_FAILED` (IE:96, IE:1680-1681). Neither attempt is aborted.
  - r1 read the unqualified sentence as meaning only the attempts the signal aborts. Grok ruled that the reading must be in the text (RF-1).
  - The import and repair-apply clauses are untouched.
- **WS:1393, §9's golden row "SIGINT before / after settle → interrupted 130 / settled class"**, which S18 binds, stays. Grok's R5 ruled so. It is a selected golden. CINV's `interrupted-before-settle` is the no-commit case ("an attempt that had not committed leaves no Run"), and that stays true. A golden for rules 1 and 2 is the M4 CLI unit's (cross-law item 3).
- **Rejected:**
  - **(r1's choice) leaving WS:229 and WSE:233 for a later successor.** Grok rejected it: J3d's signal wiring, which waits on S21, would still meet a same-paragraph rule that drops the Run;
  - **reaching WS:1393 by a complete copy,** which LD-1 rejects.

**LD-7. INV5 is not changed.** Its `Cancellation.phase` description says before-settle means "aggregate is interrupted (130)". A rule-1 or rule-2 signal is before-settle with an operational-failed aggregate. No M3 envelope carries the invocation record (S18's LD-5), so this is cross-law item 2.

**LD-8. Binding.** After acceptance, a binding-only product commit appends S21's four pins after S18. No product file is materialized. J3b and J3d implement S21 under their own reviews.

## Controls for J3b and J3d (J1's, mapped)

S21 adds no control. It lifts J1's gate on these (J1:606-617), which stand as J1 states them:
- J-C14's rule-1 and rule-2 signal cases (J1:669-670): "`Committed(PublishedCommit)` with the latch → exit 4 with the runId"; "`CommitUndetermined` → exit 4 with the ExecutionId", including a latch 1→3 followed by an undetermined evidence `COMMIT`, which never gives F39 or a runId;
- J-C15b's phase-C projections (F39 or F40 by the returned outcome);
- X9 rows S12-C (F39 with REV `operator`) and S12-U (F40, never `interrupted`);
- J3d's durable signal wiring.

Under LD-r5-1, a signal after a `publish` return that does not enter D is labelled B or C, and 8.3 projects it. S21 changes neither.

## Cross-law items

1. **J1's next revision.**
   - Record S21: on its acceptance, the gates at J1:606-617 lift, and 8.3's "WS's text does not say so" becomes historical.
   - Item 13's S21 row should take LD-3's scope (a required analysis or verify step) and the per-kind lines, WS:229 and WSE:233.
2. **The invocation-record owner (M4's invocation successor; M5's retained record).** INV5's `Cancellation.phase` description, "before-settle: … aggregate is interrupted (130)", takes S21's exception when it is restated. That goes with S18's NBO-1, the after-settle conjunct.
3. **CINV (the M4 CLI unit).** Add goldens for a signal that meets an undetermined commit and for one that meets a latched committed Run. WS:1393's row stays the ordinary case.
4. **OPP's next revision (J1's S15).** Rows A to C should carry 8.3 as J1 r5 states it:
   - rule 1 in A and B, for an undetermined attempt-row `COMMIT`, journal commit or barrier;
   - rules 1 and 2 in C.

   OPP r3's row C already says "**Not** `interrupted`". S18's copy leaves rows A to C to S15.
5. **The WS owner, when optional analysis or verify steps land (M5).** IE:1680-1681 makes any undetermined commit exit 4 to the caller. WS:235 says an optional step's failure never changes the aggregate. That tension predates S21, involves no signal, and is outside its scope (LD-3).

r1's item 6, a later WS successor for the per-kind sentence, is withdrawn: r2 makes that change (LD-6).

## Points for the reviewer (r2)

Grok ruled on r1's R1 to R6. For r2:
- **R1. Is RF-1 resolved?**
  - Are WS:229 and WSE:233 overridden with your replacement text, verbatim, with exact `before`s?
  - Does each line still end "an import discards its", so that WS:230 and WSE:234 join?
  - Is WSE:229 left with S18?
- **R2. Nothing else changed.** Are the two line-226 overrides and the parents byte-identical to r1? The r1 bytes are in `reviews/codex2-s21-r2/r1-members/`.
- **R3. Selection at the new base.** Is the record well-formed under `verify_design` at `6190e66`, after S18 and SYN-NS, with no selector clash?

## Binding

S21 binds on the `verify_design` at main `6190e66`, on top of all 92 contract successors, S18 among them, with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
1. copy the review to `docs/implementation/m3/reviews/codex2-s21-r2/review.json`;
2. complete `s21-unit.json`;
3. append the four pins to the product lock in a binding-only commit;
4. run plain `verify_design`.

If main has moved by then, rerun `evidence/verify_scratch.py` on the new main first.

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read only. Nothing ran cargo, a test, a generator or a product tool other than `verify_design` in the scratch harness, design-only.
- **`evidence/build_s21.py`**, twice. The second run's `--check` reported identical bytes.
- **`evidence/check_s21.py --rev 6190e66`**: 85 checks pass. These include the per-kind pair, Grok's text verbatim, and the per-kind line read into the next line on both parents.
- **`evidence/verify_scratch.py --rev 6190e66`**: 92 to 93, passes. It shows four overrides, no supersession, the selected inventory (`v135`) and the inheritance (100) unchanged, and the conflicting-override probe refused.

## Not claimed

- No product code, test or build was run, and no product file is changed.
- `verify_design` ran only design-only, in the scratch harness, on synthetic review and assent bytes.
- INV5, CINV, IE, SL, X7, the operability plan and every other WS line are not edited.
- No crash-matrix row is transcribed here: S12-C and S12-U are S12's, after S21's acceptance.
