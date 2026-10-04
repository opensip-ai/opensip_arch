CODEX2 review: **S21**, the commit-outcome exception to WS's before-settle rule. It is a contract successor of the host pipeline law M3-J1, which you reviewed at r1 to r3 and Codex accepted at r5. J1 r5's lead decision LD-r5-2 keeps 8.3's rules 1 and 2 against WS:226 and records S21 as the owed WS fix. This is a **design unit** (a `verify_design` contract successor). Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** with `subjectManifestSha256`, or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/codex2-s21-r1`.

**Lead note (reviewer change).** This request was written for CODEX2. **Grok** reviews it, because Grok is free. The directory keeps its name, because the builder emits this review path. Write your output under `/tmp/opensip-implementation/reviews/codex2-s21-r1`. Don't run cargo.


**Rules:**
- **Read-only.** No repository edits, commits, pushes or delegation. Run git only read-only.
- **No builds or tests.** Run no cargo, no tests, no generator and no crash-matrix binary or checker.
- **Scripts.** If you run anything, use only the evidence scripts below and read-only commands, at `nice -n 19`, with any scratch files under your review directory.
- **`verify_design`.** Run it only through `evidence/verify_scratch.py`, which writes nothing and holds a synthetic review and assent in memory. Never edit the product or its lock.
- **Never touch the real home.** `~/Library/Application Support/OpenSIP` stays absent; do not read or create it.
- **Never read the private 413 UUID fixture.**
- **Product main is `218465f`** (`218465fb71fd62ca01856d40d26ec822f45233be`), read only, with 91 contract successors. S18 has been bound since `5214350`. **Lock pin:** `design-lock.json@218465f` (504,811 bytes, `ac1449a6…`), read with `git show`.

## Subject

The pins are in `hashes.txt`. Every file is untracked in arch until acceptance.
- **The subject manifest** is `docs/implementation/m3/host-pipeline-j/s21-subject.json`. Its sha256 is `subjectManifestSha256`.
- **Its 7 members** are:
  - `s21/successor.json`;
  - `README.md`;
  - `PASSAGES.md`;
  - `evidence/reading-report.json`;
  - `evidence/build_s21.py`, `check_s21.py` and `verify_scratch.py`.
- **Not part of the subject:** `s21-unit.json`, the lead's DRAFT-PENDING-REVIEW record.

**Law.** `host-pipeline-j/PROPOSAL-r5.md` (`4ccb2320…`, Codex's r5 acceptance, `reviews/codex-host-pipeline-j-r5`):
- 8.3's rules 1 to 4, J1:588-592;
- LD-r5-2, J1:600-627, with the gates at J1:606-617;
- the S21 row, J1:868;
- open question 7, J1:938.

**Bases:**
- IE:1680-1681 (IE §5) and IE:96;
- SL:551-555 (SL S6);
- X3D r8:170 and :283;
- X7 r6:100-101.

**The bound neighbour:** S18 (`host-pipeline-j/s18/successor.json`, `e83430ad…`). It binds WS 225, 227, 228, 231 and 1393, and WSE 225, 229, 230, 235 and 1466.

## What it does

The README has the full tables; `PASSAGES.md` prints both overrides and the cancellation paragraph as it reads on each parent.

**Two line overrides**, WS:226 and WSE:226. They are byte-identical in `before` and `after`. Line 226 is free on both parents at `218465f`, and S21 selects no line S18 binds.

The line goes from "`cancelled`, the aggregate is `interrupted` (130), and a Run committed by an earlier" to the following:
- **The rule stays:** "the aggregate is `interrupted` (130) unless a required analysis or verify step's commit returned one of two outcomes, which govern instead".
- **Rule 1:** "an undetermined commit is `operational-failed` (4) with `DURABILITY.COMMIT_FAILED`, fault cause `durability-commit`, no `runId` and the attempt's ExecutionId disclosed for read-only recovery (identity-and-evidence §5's `durability-undetermined`)".
- **Rule 2:** "a commit whose FinalGate was latched after admission stays committed and is `operational-failed` (4) through `DELIVERY.REQUIRED_FAILED` (`delivery-required`), with its `runId` (security-and-lifecycle S6's selected law)".
- **Matching:** "The outcome the commit returned decides, never the gate's latch state alone."
- **The ending:** "In the `interrupted` case, a Run committed by an earlier". S18's line 227 continues it: "step is named in the termination's `runId`."

So the before-settle sentence runs from S18's 225, through S21's 226, into S18's 227 unchanged, on both parents. Nothing else in WS changes.

## Lead decisions for you to rule on

The README records eight, each with the alternatives it rejects:
- **LD-1.** The form is one override per parent, not a complete copy, no S18 line, and no new paragraph elsewhere.
- **LD-2.** WSE takes the same override.
- **LD-3.** The scope is "a required analysis or verify step's commit", not J1's "the analysis attempt" alone. IE and SL are commit-protocol rows, and the aggregate is over required steps only (WS:233-235).
- **LD-4.** The returned outcome decides, never the latch state (J1:588; X3D:170).
- **LD-5.** What WS names:
  - rule 1 in full (IE:96, X3D:283, WS:1360, IE:1680-1681);
  - rule 2 as SL names it, with its detail `DELIVERY.RENDERER_FAILED_AFTER_COMMIT` left to X7's F39 row.
- **LD-6.** Nothing else in WS changes, including two lines that read close to the exception:
  - WS:1393's golden row, which S18 binds;
  - WS:229's per-kind "an analysis attempt aborts and leaves no Run", which is free and is read as the case the signal aborts.
- **LD-7.** INV5's before-settle description is left; it is a cross-law item.
- **LD-8.** Binding-only, after S18.

## Decide

1. **Exactness.**
   - Is each `before` the exact parent line, and are the two overrides identical?
   - Does the `after` keep the line's first word and last words, so that the sentence runs from S18's WS:225 into S18's WS:227, and from WSE:225 into WSE:227?
2. **Completeness against J1.** Does S21 carry J1:868's row and 8.3's rules 1 and 2 (J1:588-605) exactly, adding no class, code, exit or fault cause, and nothing else?
3. **Scope.** Rule on LD-3.
4. **The rows.** Rule on LD-4 and LD-5:
   - Is rule 1 exactly IE's and X3D's row?
   - Is rule 2 exactly SL's path, with the detail rightly left to X7?
5. **What is left.** Rule on LD-6 and LD-7:
   - Does WS:1393's golden, or WS:229's per-kind sentence, now read against §1 in a way S21 must fix? If WS:229 needs an override, give the exact text. It is free, as is WSE:233.
   - Is any other accepted passage in WS, WSE, INV5 or the CINV goldens left false?
6. **Selection.** Is the record well-formed under `verify_design`'s `contract_successor` and `successor_chain` rules at `218465f`, after S18, with no selector clash? Is anything else wrong?

## Running the evidence (optional)

Use `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` at `nice -n 19`. No extra dependencies are needed.
1. **Build check.** `docs/implementation/m3/host-pipeline-j/s21/evidence/build_s21.py --check` rebuilds everything in memory and compares it with the files on disk. It reads the lock at `218465f` through `git show`.
2. **Content checks.** `.../evidence/check_s21.py --rev 218465f` runs 74 checks. They cover:
   - the pins;
   - the lock, S18's lines and the unbound records (18 scanned);
   - the reading across S18's lines on both parents;
   - J1's row;
   - no new code, exit or fault cause;
   - every cited line in J1 r5, IE, SL, X3D, X7, WS, WSE, INV5 and CINV.
3. **`verify_design`.** `.../evidence/verify_scratch.py --rev 218465f` is design-only. It takes the lock from 91 to 92 successors, with two overrides and no supersession. The inventory (`v135`) and the 100 inheritance rows are unchanged. A later conflicting override of WS:226 is refused.

The lead ran the build twice, with identical bytes, and both other scripts, all passing.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `s21-subject.json`. The lead's value is `090de59ff7c4281f65d3f0ba2a63b9444d0583c820dc3f01a5c294d47eb72097`.
- `"successor"`: `{path, bytes, sha256}` of `s21/successor.json`. The lead's value is 5538 bytes, `3e8ad15dec56bc8a1e4f8d63a6a47654f483d68ba26662f6118f0c76f11c7294`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. One review maps exactly one subject. If you would change bytes, give the exact replacement text. Do not commit.
