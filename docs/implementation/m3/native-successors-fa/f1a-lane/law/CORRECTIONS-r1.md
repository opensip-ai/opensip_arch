# Corrections owed at selection (LD-Q-187; REVIEW-r3-r1.md paragraph 6)

These record, and do not rewrite, the frozen review subject and request.

1. **REQUEST item 8, test attribution.** The one new test that passes on the unpatched checker is "caller exception on the bound record", not
   browser/report (d1/suite-unpatched-with-new-tests.log:225-230). The browser refusal is an inherited test. The 247 total, 235 pass and 12 fail figures
   stand. The unpatched failures largely stop at the old binding restriction, so that comparison alone does not prove site matching; the review's
   patched observations do.
2. **Custody wording, narrower.** The R3 lock covered every named draft and evidence member and the six evidence-producing scripts. It did not cover
   f1/scripts/f1a-boundary/ as a whole: lock_review_r3.zsh excludes itself (its line 18), and its custody is not claimed. The subject bytes were
   established by the reviewer's independent rehash of every member.
3. **Generator lines and wording.** The digest comparison is at gen-ts-enums.mjs line 22, not 21; the load is line 23; the version check is line 24.
   The draft's "exactly those checked bytes" is conditional on stable build inputs, not atomicity. The successor policy's reason says so.
4. **"ADOPTED WITH A CONDITION"** at POLICY-DELTA-DRAFT-r3.md line 36 is proposed language. Adoption is the coordinator's act, in
   ADOPTION-LOADER-POLICY-F1A.md.
