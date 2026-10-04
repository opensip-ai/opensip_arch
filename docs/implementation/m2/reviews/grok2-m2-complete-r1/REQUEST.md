GROK2 review: the **M2 completion record**, r1. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**, on factual accuracy.

> **Lead: do not send this request yet.** Send it only after all three of these:
> 1. Grok's X9-6 rerun on C (`reviews/grok-crash-matrix-x96-r2`) has returned and is recorded in arch.
> 2. The lead has filled every `[[RERUN:…]]` token and the `[[LEAD:…]]` token in `M2-COMPLETE.md`, and decided §5 items 13–16.
> 3. `hashes.txt` here has been recomputed over the finalized bytes and committed.
>
> The hashes committed with this draft pin the COMPLETE (finalized after Grok's accepted rerun, arch 50047b7ed) draft. They are not the bytes to review.

Claude Opus 5.5 leads, and you are the reviewer.
- Do not edit any repository, commit, push or delegate.
- Write only under `/tmp/opensip-implementation/reviews/grok2-m2-complete-r1`.
- Run git read-only. Run only read-only commands, plus `verify_design` at `nice -n 19` if you want to re-derive §6.
- Run no cargo, no tests, and no crash-matrix binary or checker. Every number to check is already in a committed record.
- `~/Library/Application Support/OpenSIP` stays absent: do not read or create it. Never read the private 413 fixture.

## Subject

The pins are in `hashes.txt`:
- **`docs/implementation/m2/M2-COMPLETE.md`:** the record. It claims M2 complete against the build plan's M2 row (`docs/v2/architecture/implementation-boundaries-and-build-plan.md:886`), on acceptance of Grok's rerun.
- **`docs/implementation/m2/EXIT-PLAN.md`:** only the units table's "Status / notes" column is refreshed. Four rows (X4T-0, X4T, X4B and X12) were padded from four cells to six, and one line follows the table. Review the change with `git -C /Users/sb/code/opensip-ai/opensip_arch diff <parent> -- docs/implementation/m2/EXIT-PLAN.md`, where `<parent>` is the commit before the one that lands this record.

**Repositories, read-only:**
- product `/Users/sb/code/opensip-ai/opensip`, main `3e64266`; the matrix commit C is `3d2d5b5`;
- arch `/Users/sb/code/opensip-ai/opensip_arch`.

## Decide

Check every row and every claim against its cited source. A wrong commit, inventory, review directory, revision, count, date, owner or status is a required finding. So is any claim the cited evidence does not support.

1. **§1, the claim.**
   - Does each "claims" item follow from the evidence in §2?
   - Is each "does not claim" item correct and sourced? These cover product qualification, compiler qualification, gates, D-372 condition 4, real-machine use, the CLI, platforms and M3.
   - Does the record claim more than BP:886 and the evidence support?
2. **§2, the evidence.**
   - **§2.1 (X8):** the law revision and its sha; the integration commits; the fixture counts under `crates/host/tests/refusal/` at `3e64266`; the B0–B8 names; X8c's lane numbers.
   - **§2.2 (X9):** every value against `crash-matrix-x9/evidence/3d2d5b5…/check.json`, both `matrix.json` files, the 479 run records (labels and verdicts), `release-absence.json` and `hashes.txt`; the run-set arithmetic (381 = 231 + 57 + 47 + 46; 98 = 94 + 4); and the earlier reviewer reruns cited from `grok-crash-matrix-x92-r1` to `-x96-r1`. **The rerun values:** check them against `grok-crash-matrix-x96-r2/review.json`, once filled.
   - **§2.3 and §2.4:** the labels; the file presences and line counts at `3e64266`; the four absent owner files and the reason given for each.
   - **§2.5:** each gate's preparing units, and what each gate does not cover.
3. **§3, the units.**
   - **§3.1:** each law's accepted revision, accepting review directory, arch commit and date. Use `git log -- <law>/PROPOSAL.md` and each review's `status.json` and `review.json`.
   - **§3.2:** each of the 62 rows: product commit (`git log d4239a5..3e64266`), selected inventory (`design-lock.json` at that commit), review directory and reviewer, and the law revision. That revision is named either in the commit message or, where marked "(review)", in the review request. Confirm that every commit in the range appears exactly once.
   - **§3.3:** confirm that X3a-2, X4b and X4T-c are declared by the cited law items, are not built at `3e64266`, and have no deferral record anywhere in arch. If you find a deferral record, that is a required finding against the record.
4. **§4, known limits.**
   - Are L1–L11's "recorded owner" values verbatim from `matrix.json`'s `limits`?
   - Does L11's text match X9 r16 item 10 and EXIT-PLAN's "M2 known limit"?
   - Is every *inference* labelled as one?
   - Is §4.2 sourced?
5. **§5, open follow-ups.**
   - For each row: is the status (open, owned or closed), the owner and the timing what the cited source says?
   - Is the "Closed EXIT-PLAN follow-ups" list correct?
   - Is any open M2 follow-up, from EXIT-PLAN, the laws, the M2 reviews or `OVERNIGHT-2026-10-03.md`, missing from §5?
6. **§6, the product state.**
   - `git diff --stat 3d2d5b5 3e64266`;
   - the v134 bytes, sha and planned-file count;
   - the `verify_design` values at `3e64266`;
   - the lane table against `grok-crash-matrix-x96-r1/REQUEST.md` "Lanes";
   - the policy-check states (F8a's review, the F8b proposal).
7. **§8, discrepancies.** Is each listed discrepancy real and correctly described? In particular, the git dates against the record dates.
8. **The EXIT-PLAN refresh.**
   - Did only the status column change, apart from the padding and the one note line?
   - Is every new status cell accurate?
   - Is `EXIT-PLAN.md` absent from product `design-lock.json` and from `docs/coop/design-corrections/reviews/application-subject.v46.json`?
9. **Anything else** that is wrong, missing or overstated.

## Useful commands

```
git -C /Users/sb/code/opensip-ai/opensip log --format='%h %ad %s' --date=iso d4239a5..3e64266
git -C /Users/sb/code/opensip-ai/opensip show <commit>:design-lock.json   # inventorySuccessors[-1].candidate.path; contractSuccessors
cd /Users/sb/code/opensip-ai/opensip && nice -n 19 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/verify_design.py --architecture /Users/sb/code/opensip-ai/opensip_arch --implementation .
```

## Output

Write `REVIEW.md` and `review.json`. `review.json` needs:
- `"verdict"`;
- `"requiredFindings"`, each with the section and row it concerns;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: the sha256 of `M2-COMPLETE.md` as reviewed;
- `"exitPlanSha256"`: the sha256 of `EXIT-PLAN.md` as reviewed;
- `"rowsChecked"`: counts for §3.1, §3.2, §4.1 and §5.

Do not commit.
