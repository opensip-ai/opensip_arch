Grok review: **FA-1**, round 1. FA-1 is the native contract successor that the accepted fact-admission law M3-H r3 names for cross-law item **X-H2**: native-evidence §10's "facts before the terminal are admitted" against the retained discard selectors. This is a **design-unit (contract successor)** review. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT-DESIGN-UNIT** or **REQUIRED-FINDINGS**.

Write only under `/tmp/opensip-implementation/reviews/grok-fa-1-r1`.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation. Run git only read-only.
- No cargo, no builds, no tests, no crash-matrix binary or checker. P0's lanes are using this machine.
- If you run anything, use only the three evidence scripts named below, or read-only commands, with `nice -n 19` and `python3.14 -I -B` (`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14`). Use a private 0700 `TMPDIR` under your review directory if you need scratch files.
- Do not import or execute the native reference model. `check_fa1.py` parses it with `ast` only.
- Never touch the real home: `~/Library/Application Support/OpenSIP` stays absent. Do not read or create it.
- Never read the private 413 UUID fixture.

## Subject

The pins are in `hashes.txt`. The subject manifest is `docs/implementation/m3/native-successors-fa/fa-1-subject.json` (1,250 bytes, `56e656d7559eebcb4184c0b28fbd4932f9041b10400d4d27453c1f17c8dede50`). Its six members, all under `docs/implementation/m3/native-successors-fa/fa-1/`:
- `README.md`: the proposal. Read it first.
- `successor.json`: the record. One parent (NE), three line overrides, no supersession, five candidates.
- `PASSAGES.md`: generated. Each override's exact `before` and `after`, and the effective fault-law paragraph NE:3837-3855 after FA-1.
- `evidence/build_fa1.py`, `evidence/check_fa1.py`, `evidence/verify_scratch.py`.

All of these are untracked in arch until acceptance. `fa-1-unit.json` next to the manifest is the lead's draft, marked `DRAFT-PENDING-REVIEW`. It is not part of the subject.

**The lock** is `design-lock.json@cd5958b`, 82 contract successors. Read it with `git -C /Users/sb/code/opensip-ai/opensip show cd5958b:design-lock.json`. The product is `/Users/sb/code/opensip-ai/opensip` at main `cd5958b`, read-only. FA-1 changes no product byte.

**The source law.** `docs/implementation/m3/fact-admission-h/PROPOSAL-r3.md`, M3-H r3, the accepted snapshot (your ACCEPT, `reviews/grok-fact-admission-h-r3`, `7a562720…`). Read:
- G5 (H3:123) and decisions-at-a-glance rows 3, 4 and 13 (H3:132-136);
- item 3, the clean-settlement boundary, atomic per Analyze (H3:206-240);
- item 4, the lead decision: candidates discarded, terminal Coverage admitted (H3:242-263);
- item 13, the closed-world cross-checks, "wired only after FA-1" (H3:445-455);
- item 22's closed-world row (H3:734), H-C3 and H-C13 (H3:777, H3:787);
- the FA-1 successor row (H3:809) and X-H2 (H3:859).

M3-D r3's finding F7 (`supervisor-d/PROPOSAL-r3.md:623`, `:1107`) handed the choice to H.

## What it does

Three line overrides of `docs/v2/contracts/product-v1/native-evidence.md` (NE, `83b99783…`):

1. **NE:3849-3850, replaced.** "facts before the terminal are admitted" is withdrawn. On a `BudgetExhausted` or post-Analyze `Unavailable`, every fact candidate of that Analyze and every occupancy companion it carried is discarded. Only the terminal's exhaustive Coverage is admitted, at the producer boundary after a clean settlement. A pre-Analyze `Unavailable` has no candidates, and its Coverage is §9.7's host conversion.
   - The stage stays `partial` and the Run authoritative, so MJ row 31 is unchanged.
   - The text names the six retained selectors by exact path: DLV's `factBatchAtomicity.onUnavailable` and `.onBudgetExhausted`, `cleanUnavailable.candidateDisposition` and `deterministicBudget.candidateDisposition`, and RPP's `candidateAtomicity.discardAllOn` and `.unavailableAndBudgetCoverage`. It gives the reason: only `Complete` carries `factStreamCommitment`.
   - It states that `StageAuthorityV1.factsAdmitted` for these terminals is `none`, and that this text governs where the reference `stage_authority` returns `before-terminal`.
2. **NE:3529, insert-only.** The §10 producer-boundary route row (`operational-failed` 4, `PROVIDER.PROTOCOL_VIOLATION`, operational record) gains the internal key `native.coverage-closed-world-mismatch`. It covers the two §4.5 record laws (NE:2237-2239, NE:2221-2222), checked over the facts admitted from the entry's own stage. This is the second half of H3's FA-1 row (LD-A1).

## Lead decisions for you to rule on

- **LD-A1.** FA-1 carries both halves of H3's FA-1 row, not X-H2 alone.
- **LD-A2.** The reference triple is not overridden: NEM's `stage_authority` (B-S9 copy lines 3729 and 3733; v2 lines 3720 and 3724), NES's `StageAuthorityV1` enum, and NC:13342's case. The NE text states `none` (a member of the registered enum) and that it governs, following NE:708-710's rule. The refresh is finding FA1-F1.
- **LD-A3.** The discard names occupancy companions and the pre-Analyze case.
- **LD-A4.** The form is three line overrides, two of them replacements, with no §0 row.
- **LD-A5.** The closed-world key is producer-boundary only, scoped to the entry's own stage as H item 13 is, with no public code.

## FA-2

FA-2 r2 (in review with Codex, `reviews/codex-fa-2-r2`) overrides NE 93, 138, 1913, 1927, 2791, 2814, 2884, 2990, 3235, 3279, 3292, 3313 and 4195. None is FA-1's. FA-1 also stays off NE:138 (§0's last row), so the binding order is free. `verify_scratch.py` binds both orders. Their texts agree: FA-2's §9.8 already says the census rides only on `Complete` (`fa-2/section-9-8.md:75-80`).

## Feasibility (the lead's runs)

- **`build_fa1.py`**, then `build_fa1.py --check`: identical bytes. It asserts every `before`, that NE is an accepted lock input at its pinned bytes, that no bound successor overrides FA-1's lines, and that no unbound draft on NE (FA-2, rust3-lim, SYN-1, SD-5) does.
- **`check_fa1.py`** passes:
  - NE:3529 is one contiguous insertion that keeps the row's cells;
  - the new key exists nowhere else, and it is not a `DomainDetailCode` or a route-registry key;
  - the six selectors resolve to the quoted values, and NE names none of them anywhere;
  - only `CompleteV1` and `CompleteV2` carry `factStreamCommitment`;
  - the enum admits `none`, and both model files return `before-terminal`;
  - H3's text is as cited.
- **`verify_scratch.py`**, at `--rev cd5958b` and on the main checkout:
  - **FA-1 binds:** 82 to 83, with three overrides and no supersession. The selected inventory and inheritance are unchanged, and 40 generation sources are verified on the checkout.
  - **Binding order:** FA-2 then FA-1, and FA-1 then FA-2, both pass with 84. So do SD-5 then FA-1 and FA-1 then SD-5.
  - **A later override of NE:3849** refuses: `conflicting contract passage overrides`.

## Decide

1. **Exactness.** Is each `before` the exact parent line? Is NE:3529's `after` a pure insertion? Is every selector, value and law the texts cite real and quoted correctly?
2. **Agreement.** Does NE:3849-3850 as amended agree with the six retained selectors, with H3 items 3, 4 and 11, and with NE §9.6's occupancy timing, §9.7's terminal Coverage and the fault rule? Is the pre-Analyze case right?
3. **The reference (LD-A2).** Is stating `none` and "this text governs" in NE, with FA1-F1 owed, sound? Or must the model copies and the case change in this unit?
4. **The closed-world key (LD-A1, LD-A5).** Is its condition exactly H item 13's two laws, on the right row, with the right scope? Should it stay internal?
5. **FA-2 and the other drafts.** Is there any interaction beyond line disjointness?
6. **Form.** Is the successor well formed for selection under `verify_design`'s `contract_successor` and `successor_chain` rules? Is anything else wrong?

## Running the evidence (optional)

From any directory, with `nice -n 19 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B`:
1. `docs/implementation/m3/native-successors-fa/fa-1/evidence/build_fa1.py --check`, which rebuilds in memory, compares with the files on disk and writes nothing. Always pass `--check`: without it the script rewrites the generated files.
2. `.../fa-1/evidence/check_fa1.py`.
3. `.../fa-1/evidence/verify_scratch.py --rev cd5958b`. It execs `tools/verify_design.py` from `cd5958b` through `git show`, holds synthetic reviews in memory and writes nothing.

## Output

Write REVIEW.md and review.json. review.json must contain:
- `"verdict"`: `ACCEPT-DESIGN-UNIT` or `REQUIRED-FINDINGS`;
- `"requiredFindings"`: each with id, location, problem, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectManifestSha256"`: a single string, the sha256 of `fa-1-subject.json`. The lead's value is `56e656d7559eebcb4184c0b28fbd4932f9041b10400d4d27453c1f17c8dede50`;
- `"successor"`: `{path, bytes, sha256}` of `fa-1/successor.json`. The lead's value is 7,206 bytes, `a216e65d9b5b6927c2648c01daa6085018fa56cfe81877599cc8eb02f386ff59`.

This is a contract successor, so it has no `inventoryCandidateAssessment`. If you would change text, give the exact replacement. Do not commit.
