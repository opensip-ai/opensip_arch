# S21 — the commit-outcome exception to WS's before-settle rule (contract successor of law M3-J1)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. **Draft r1, PROPOSED, not accepted.** It is a design unit: it edits only arch, and changes no product file, code, class, exit code, route or public code. It needs CODEX2's `ACCEPT-DESIGN-UNIT` and the lead's root assent before it can be bound in the product's `design-lock.json`.

**What it is.** Accepted law **M3-J1 r5** keeps 8.3's rules 1 and 2 against WS:226 (lead decision LD-r5-2, J1:600-627):
- **Rule 1.** A signal observed before settlement that meets a `CommitUndetermined` takes the durability row, with the ExecutionId (IE:1680-1681).
- **Rule 2.** A signal that meets a `Committed(PublishedCommit)` latched after admission takes the `DELIVERY.REQUIRED_FAILED` row, with the runId (SL:551-554).

WS:226 still makes every before-settle aggregate `interrupted` (130). J1 records the WS fix as an owed successor, **S21** (J1:868): "a passage successor to WS:226 and to WSE:226". S21 is that successor. It states the exception on WS:226 and on the matching line of WS's selected effective copy, and changes nothing else in WS.

**What waits on it** (J1:606-617):
- J3d's durable signal wiring;
- J-C14's rule-1 and rule-2 signal cases;
- J-C15b's phase-C projections;
- X9 rows S12-C and S12-U.

J2a's pure model, J3b's latch code, and rows S12-B and S12-D may go ahead.

**Product.** Main `218465f`, read only, with 91 contract successors. S18 has been bound since `5214350`. S21 binds at `218465f`, 91 to 92 (see "Evidence runs").

## Short names

| Name | Document |
|---|---|
| **J1** | `docs/implementation/m3/host-pipeline-j/PROPOSAL-r5.md`, the M3-J1 r5 bytes Codex accepted (146,331 bytes, `4ccb2320…`; `reviews/codex-host-pipeline-j-r5`). It is cited by line. |
| **WS** | `docs/v2/contracts/product-v1/workflows-and-surfaces.md` (133,335 bytes, `1ee203e3…`), an accepted lock input |
| **WSE** | `docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md` (139,497 bytes, `4478ce1a…`), WS's selected effective copy |
| **S18** | the bound final-output-section successor, `host-pipeline-j/s18/successor.json` (GROK2 ACCEPT-DESIGN-UNIT at r2; product `5214350`). On WS it binds lines 225, 227, 228, 231 and 1393, and on WSE lines 225, 229, 230, 235 and 1466. |
| **IE, SL** | `docs/v2/contracts/product-v1/{identity-and-evidence, security-and-lifecycle}.md`, accepted lock inputs. IE:1680-1681 is in IE §5, and SL:551-555 is in SL S6. No bound entry touches either passage. |
| **X3D, X7** | `docs/implementation/m2/commit-session-x3d/PROPOSAL-r8.md` (`5e491b92…`) and `finalization-x7/PROPOSAL-r6.md` (`9e17faf2…`) |
| **INV5** | `opensip/schemas/sources/invocation-v5.schema.json` at `218465f` |
| **CINV** | `docs/coop/design-corrections/workflows/command-inventory.v3.json` |

## Files

| File | What it is |
|---|---|
| `README.md` | this proposal |
| `PASSAGES.md` | generated: both overrides with exact `before` and `after`, and the cancellation paragraph as it reads with S18 and S21 on each parent |
| `successor.json` | the contract successor record: two parents (WS, WSE), two passage overrides, no supersession, six candidates |
| `evidence/reading-report.json` | generated: the bound entries on WS and WSE at `218465f`, S18's lines, and the effective cancellation paragraph line by line with each line's owner |
| `evidence/build_s21.py` | builds every generated file, the record, the subject manifest and the unit draft; `--check` compares instead of writing |
| `evidence/check_s21.py` | read-only, independent checks: pins, the lock and S18's lines, unbound records, the reading across S18's lines, content, no new code, exit or fault cause, and every citation |
| `evidence/verify_scratch.py` | runs the real `verify_design` with a synthetic review and assent, and a conflicting-override probe |
| `../s21-subject.json` | the subject manifest (generated) |
| `../s21-unit.json` | the lead's assent draft, `DRAFT-PENDING-REVIEW`, with the review path `reviews/codex2-s21-r1/review.json`; not part of the subject |

## What changes

**Two line overrides**, WS:226 and WSE:226. The two lines are the same text, and the two overrides have byte-identical `before` and `after`.

Before:

> `cancelled`, the aggregate is `interrupted` (130), and a Run committed by an earlier

After:

> `cancelled`, and the aggregate is `interrupted` (130) unless a required analysis or verify step's commit returned one of two outcomes, which govern instead (contract successor S21 of law M3-J1 r5): an undetermined commit is `operational-failed` (4) with `DURABILITY.COMMIT_FAILED`, fault cause `durability-commit`, no `runId` and the attempt's ExecutionId disclosed for read-only recovery (identity-and-evidence §5's `durability-undetermined`); a commit whose FinalGate was latched after admission stays committed and is `operational-failed` (4) through `DELIVERY.REQUIRED_FAILED` (`delivery-required`), with its `runId` (security-and-lifecycle S6's selected law). The outcome the commit returned decides, never the gate's latch state alone. In the `interrupted` case, a Run committed by an earlier

**How it reads.** S18's WS:225 ends "…: remaining steps are", and S18's WS:227 begins "step is named in the termination's `runId`." So the sentence reads: before-settle → remaining steps `cancelled` → `interrupted` (130) unless one of the two commit outcomes governs → "In the `interrupted` case, a Run committed by an earlier step is named in the termination's `runId`." Then S18's *after-settle* definition follows unchanged. On WSE, line 227 instead continues with the optional-Run sentences ("This includes optional analysis/verify steps…"), and they read on unchanged. `PASSAGES.md` prints the whole paragraph as it reads on each parent.

Nothing else changes: no other WS or WSE line, and no code, class, exit, field, fault cause, step outcome, public code, schema, inventory or product file.

## J1's S21 row, item by item

| J1 r5 (J1:868, with 8.3 at J1:588-627) | Where S21 carries it |
|---|---|
| "A signal observed before settlement leaves the aggregate `interrupted` (130), except where the analysis attempt's commit outcome governs" | "the aggregate is `interrupted` (130) unless a required analysis or verify step's commit returned one of two outcomes, which govern instead" (scope: LD-3) |
| "An undetermined commit takes IE:1680-1681's durability termination with its ExecutionId" (rule 1, J1:589) | "an undetermined commit is `operational-failed` (4) with `DURABILITY.COMMIT_FAILED`, fault cause `durability-commit`, no `runId` and the attempt's ExecutionId disclosed for read-only recovery (identity-and-evidence §5's `durability-undetermined`)". The code is IE:96's and X3D:283's, and the fault cause is WS:1360's. |
| "A commit latched after FinalGate admission takes SL:551-554's `DELIVERY.REQUIRED_FAILED` row" (rule 2, J1:590) | "a commit whose FinalGate was latched after admission stays committed and is `operational-failed` (4) through `DELIVERY.REQUIRED_FAILED` (`delivery-required`), with its `runId` (security-and-lifecycle S6's selected law)". The detail stays X7's (LD-5). |
| "Each is operational-failed 4 (8.3, rules 1 and 2)" | both outcomes, as quoted |
| X3d's returned outcome matched first; "the gate's state 3 alone proves neither a commitment nor a RunId" (J1:588, J1:605) | "The outcome the commit returned decides, never the gate's latch state alone" (LD-4) |
| "It adds no class, code or exit" | `check_s21.py`: every code is already in WS, IE or SL; every fault cause is in WS:1360-1361; every exit is in the fixed table |
| "leaves S18's lines (WS:225, :227-228, :231) as they are" | S21 selects only line 226 on each parent. `build_s21.py` and `check_s21.py` assert that S18 binds its five lines on each parent and that S21 selects none of them. |
| "S21 is to override WS:226 and WSE:226" (J1:605) | the two overrides |

## Why this form

- **Line 226 is free on both parents.** In the lock at `218465f`:
  - WS's bound lines are 225, 227, 228, 231 and 1393 (S18), 308 (CRC-1), 598 and 603 (I1-L), and 1296 (initial-root-binding);
  - WSE's are 225, 229, 230, 235 and 1466 (S18), 312 (CRC-1), 602 and 607 (I1-L), and 1300 (initial-root-binding).

  No unbound successor record in arch touches line 226 either.
- **S21 needs none of S18's lines.** Line 226 holds the whole consequence of the before-settle rule: "remaining steps are" ends S18's line 225, and "step is named in the termination's `runId`" begins S18's line 227. So S21's `after` keeps the line's first word, `cancelled`, and its last words, "a Run committed by an earlier". The sentence then flows into the bound lines on both sides unchanged.
- **The probe.** `verify_scratch.py` shows that a later conflicting override of WS:226 is refused ("conflicting contract passage overrides").

## Lead decisions

Each decision is dated 2026-10-04 and made under the owner's standing direction to proceed on the lead's recommendation. Each names the alternatives it rejects, and the owner may reverse any of them.

**LD-1. The form: one line override on each of WS:226 and WSE:226.**
- **Rejected:**
  - **a complete copy of WS and WSE.** The line is free, and a copy of a lock input would have to carry every bound override (S18, CRC-1, I1-L, initial-root-binding) and a selection statement. That is disproportionate for one line;
  - **overriding any line S18 binds.** `verify_design` refuses a second override of a bound line, and the lead's direction forbids it;
  - **stating the exception in a new paragraph on another line**, for example after WS:231 or at WS:233. WS:226 would still state `interrupted` unconditionally, and another WS line would change.

**LD-2. WSE takes the same override.** This follows I1-L's LD-L5 and S18's LD-2. WSE:226 is the same text as WS:226.
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

**LD-6. Nothing else in WS changes**, as J1's row and the lead's direction require. Two lines read close to the exception and are left:
- **WS:1393, §9's golden row "SIGINT before / after settle → interrupted 130 / settled class"**, which S18 binds. It is a selected golden. CINV's `interrupted-before-settle` is the no-commit case ("an attempt that had not committed leaves no Run"), and that stays true. A golden for rules 1 and 2 is the M4 CLI unit's (cross-law item 3).
- **WS:229's per-kind sentence, "an analysis attempt aborts and leaves no Run"** (WSE:233). It is free, and it describes an attempt the signal aborts, in phases A and B. The exception in the same sentence group states the two cases where the attempt is not aborted: the commit stays committed, or its outcome is undetermined. The specific rule governs.
- **Rejected:**
  - **overriding WS:229.** It is outside J1's S21 row and the direction. It is offered to the reviewer (R5) and recorded as cross-law item 6;
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
   - Item 13's S21 row should take LD-3's scope: a required analysis or verify step.
2. **The invocation-record owner (M4's invocation successor; M5's retained record).** INV5's `Cancellation.phase` description, "before-settle: … aggregate is interrupted (130)", takes S21's exception when it is restated. That goes with S18's NBO-1, the after-settle conjunct.
3. **CINV (the M4 CLI unit).** Add goldens for a signal that meets an undetermined commit and for one that meets a latched committed Run. WS:1393's row stays the ordinary case.
4. **OPP's next revision (J1's S15).** Rows A to C should carry 8.3 as J1 r5 states it:
   - rule 1 in A and B, for an undetermined attempt-row `COMMIT`, journal commit or barrier;
   - rules 1 and 2 in C.

   OPP r3's row C already says "**Not** `interrupted`". S18's copy leaves rows A to C to S15.
5. **The WS owner, when optional analysis or verify steps land (M5).** IE:1680-1681 makes any undetermined commit exit 4 to the caller. WS:235 says an optional step's failure never changes the aggregate. That tension predates S21, involves no signal, and is outside its scope (LD-3).
6. **WS:229 (LD-6).** If a later WS successor wants the per-kind sentence explicit, the minimal text is "an analysis attempt the signal aborts leaves no Run". WS:229 and WSE:233 are free.

## Points for the reviewer

- **R1. Exactness.** Is each `before` the parent's exact line, and are the two overrides identical? Does the `after` keep the line's first and last words so the sentence runs from S18's 225 into S18's 227 on both parents?
- **R2. Completeness against J1.** Does S21 carry J1:868's row and 8.3's rules 1 and 2 (J1:588-605), and nothing else?
- **R3. Scope (LD-3).** "A required analysis or verify step's commit" rather than "the analysis attempt".
- **R4. The rows (LD-4, LD-5).** Is rule 1 named exactly? Is rule 2 named as SL names it, with its detail left to X7? Is "never the gate's latch state alone" right?
- **R5. What is left (LD-6, LD-7).** Rule on WS:1393, on WS:229's per-kind sentence (an override, or a later successor) and on INV5.
- **R6. Selection.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules after S18, with no selector clash?

## Binding

S21 binds on the `verify_design` at main `218465f`, on top of all 91 contract successors, S18 among them, with no prerequisite. After `ACCEPT-DESIGN-UNIT`:
1. copy the review to `docs/implementation/m3/reviews/codex2-s21-r1/review.json`;
2. complete `s21-unit.json`;
3. append the four pins to the product lock in a binding-only commit;
4. run plain `verify_design`.

If main has moved by then, rerun `evidence/verify_scratch.py` on the new main first.

## Evidence runs

Every run used `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`, read only. Nothing ran cargo, a test, a generator or a product tool other than `verify_design` in the scratch harness, design-only.
- **`evidence/build_s21.py`**, twice. The second run's `--check` reported identical bytes.
- **`evidence/check_s21.py --rev 218465f`**: 74 checks pass.
- **`evidence/verify_scratch.py --rev 218465f`**: 91 to 92, passes. It shows two overrides, no supersession, the selected inventory (`v135`) and the inheritance (100) unchanged, and the conflicting-override probe refused.

## Not claimed

- No product code, test or build was run, and no product file is changed.
- `verify_design` ran only design-only, in the scratch harness, on synthetic review and assent bytes.
- INV5, CINV, IE, SL, X7, the operability plan and every other WS line are not edited.
- No crash-matrix row is transcribed here: S12-C and S12-U are S12's, after S21's acceptance.
