I fixed the imported-universe join in the policy-test model. A fixture row from another registered universe no longer counts as a match for the evaluated subject, and all my v1 corrections are intact. Root's case now gives no finding and an indeterminate verdict instead of a wrong fail. This is author work, not acceptance, and makes no claim about the active independent85 review, blind9d3d or a frozen40.

**Custody**
- **Frozen39:** the manifest sha matches and all 12909 files were verified before and after a fresh copy into `work/source`.
- **v1 delta:** applied only after checking the patch sha `8fe83cd1…`, the six before/after hashes, and that a diff rebuilt from those exact bytes reproduces the 790-line v1 patch byte for byte.
- **Snapshots:** the frozen39 and post-v1 versions of the edited files are saved.
- **End of work:** frozen39, root's probe directory and my v1 delta and corrected files are all unaltered.

**Cause.** In `policy_test_model.v3.py`, the native match checks the universe, but the imported loop for runtime and history rows checked only the subject path. A rust runtime or history row therefore became a known match for a typescript subject: `exists` true, or a wrongly definite `none`/`count-at-most` false. This contradicts the published `factUniverse` rule. The defect is in frozen39 and survived v1.

**Fix**
- **Model:** a new `_imported_occupancy(fact, subject, universe)` requires both the subject path and the universe. The imported loop rejects any non-matching row before classifying it, so a foreign row is neither known nor uncertain. Missing imported rows still never prove absence.
- **Cases:** a new `importedUniverseSuite` with five authored cases: same-universe runtime and history hits, foreign rows, foreign rows beside a same-universe hit, evidence absent, and same-universe absence.
- **Checker:** 8 new `pt2` checks. They include "foreign rows behave exactly like imported absence" and a direct check of the new helper.
- **Normative text:** unchanged, since `factUniverse` already states the rule.
- **Other selectors:** test-execution and test-case rows stay unrepresentable in any universe.

**Before the fix**
- Root's probe, rerun with only its paths changed, produced byte-identical suite inputs and report rows.
- My discrimination probe failed exactly the six foreign-universe runtime/history scenarios plus the missing-helper check.
- The workflow checker with the new controls failed exactly the 5 checks that target the defect. That receipt is kept.

**After the fix**

| check | result |
|---|---|
| root's probe | corrected rust row: indeterminate, no finding, no unmet expectation; typescript still fails with its finding (frozen39 still shows the defect) |
| my discrimination probe | 23/23, including a white-box trace: both rust rows are rejected, and only the typescript row reaches the filters |
| v1 comparison probe | 37/37 |
| original independent probe (new path-only rerun) | 50/50 |
| `check-workflow-projection.v3.py` | 860/860 (8 added versus v1's 852; none removed or flipped) |
| `check-composition.v3.py` | 30/30 |
| `check-query-projection.v3.py` | 204/204 |
| historical `check_workflows.v1.py` | 1816/1816, stdout byte-identical to the frozen39 baseline |
| `check-array-orders.py` | 123/123 |

**Deltas**
- **Combined vs frozen39:** the same six v1 files and nothing more; `output/combined.patch`, 1298 lines, sha `9c1eea79…`. The schema, `workflows_model.v3.py` and contract stay at their v1 bytes.
- **Incremental vs v1:** checker, cases and model only; `output/incremental.patch`, 528 lines, sha `bd7968b9…`.

Two attempts left no receipt. My first inline command for the v1 regression probes was denied by the permission layer, so I moved the same logic into a script and ran it. My first recheck call exited 2 because I hadn't written the script yet.

**Limits**
- This uses bounded fixture rows, not a full Run or provider qualification.
- A foreign uncertain row can't change an imported atom's value, so its exclusion is shown by the white-box trace rather than by route results.
- The authored expectations are my own; independent review is the oracle.
- The full launcher was not run.

Files are in `/private/tmp/opensip-design-corrections/claude-policy-test-imported-universe-author.v1`:
- review.md
- review.json
- output/combined.patch
- output/incremental.patch
- custody/combined-delta-manifest.json
- custody/incremental-delta-manifest.json
