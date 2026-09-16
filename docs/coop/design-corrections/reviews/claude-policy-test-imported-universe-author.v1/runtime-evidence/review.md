# Policy-test imported-universe join correction (follow-up to the completed known-hit v1)

Coauthor origin 823bf66b-e92a-4789-ab81-63a1a9dc371d. Runtime `R=/private/tmp/opensip-design-corrections/claude-policy-test-imported-universe-author.v1`.

**Standing.** This is a bounded AUTHOR follow-up. It was built in a fresh capture of verified frozen39, with my exact completed v1 delta applied.
- Not independent acceptance. The independent85 review and blind9d3d remain active and are not claimed.
- There is no frozen40.
- No product work, commits, pushes, pins, planning, registry or public-detail additions.
- Frozen39, root's probe directory and my v1 runtime are unaltered (§6).

`R/review.json` (sha256 `6a4f06f8…acfe161`) is built by `R/build_review.py`, which recomputes every claim below and refuses on mismatch.

## 1. Custody and v1 application

**Frozen39.**
- Manifest `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json`, sha256 `f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009`.
- All 12909 members (737605070 bytes) were verified before and after the copy: no fault, no unlisted file, no `__pycache__`.
- The fresh regular-file capture is `R/work/source` (`R/custody/frozen39-capture.json`).

**v1 delta** (`R/apply_v1_delta.py`, record `R/custody/v1-delta-application.json`, receipt `apply-v1-delta`):
- the v1 patch sha256 is `8fe83cd122eefeec384f4d48aebc2c2eaa505a5c1a1bac5958c6fe74672a9f28`;
- each of the six files' before bytes equals its frozen39 hash, and its after bytes (from the completed v1 copy) equal the v1 after hash;
- the unified diff regenerated from those exact bytes **reproduces the 790-line v1 patch byte for byte**;
- before-images are in `R/work/before-images-v39`;
- the post-v1 images, which are the base of the incremental delta, are in `R/work/before-images-v1` (`R/custody/before-images-v1.json`).

All v1 corrections are preserved unchanged: known hits under missing required evidence, the optional-evidence disclosure, the closed universe tokens, the schema/owner/contract text, and the v1 checks. The combined delta keeps the schema, `workflows_model.v3.py` and contract bytes exactly at the v1 after hashes.

**Root evidence read:**
- `probe.py` (sha `53c20dae…`, matching `command.json`);
- `command.json`, `report.json`, `stdout.json`, `stderr.txt` (empty);
- the four suite inputs (typescript suites `f4a17c69…`, rust suites `3c20d4ab…`; frozen39 and author-correction copies are identical pairs);
- `initial-observation/report.json`.

## 2. Diagnosis

`policy_test_model.v3._atom` matched imported rows by subject path only. This affected both representable selectors, `runtime-subject` and `history-subject`. `_native_occupancy` requires `fact.universe == evaluated universe`; the imported loop did not.

So a registry-valid fixture row of another registered universe:
- became a **known** match for the typescript subject: `exists` true, `none` false, `count-at-most` false above N;
- or, if unobservable, an uncertain row.

This contradicts the published `x-opensip-fixture-representation.factUniverse` law: "occupancy requires it to equal the evaluated subject universe, so a fact of another registered universe never occupies". The defect is present in frozen39 and survived v1, which only closed the token map.

**Reproduction before the fix.**
- **Root's probe** (new path-only adaptation `R/probes/root-probe.path-only.py` with its diff; only the output directory and author-correction source path change):
  - all four generated suite inputs are **byte-identical** to root's;
  - all report rows are **identical** to root's report;
  - rust rows fail with a known finding in both frozen39 and my v1-applied copy.
- **My discrimination probe** (`R/probes/imported_universe_probe.py`, pre-fix) failed exactly:
  - runtime `exists` for foreign rust and syntax rows;
  - runtime `none` and `count-at-most` giving a false *known* result;
  - history `exists` and `none`;
  - the white-box occupancy-helper check (helper absent).

  Same-universe, native, absence, optional/required-evidence and unrepresentable controls already agreed.
- **The workflow checker with the new controls, before the model fix** (receipt retained, exit 1): 860 checks, failing exactly the 5 new discriminating imported-universe checks.

## 3. Correction (minimal)

**`workflows/policy_test_model.v3.py`** (incremental: 6 added lines, 1 changed line):
- new `_imported_occupancy(fact, subject, universe)`, returning whether both the subject path and the universe match;
- the imported loop now skips any non-occupying row **before** observability classification, filter projection or keying. A foreign row is therefore neither a known nor an uncertain observation.
- Imported absence semantics are unchanged: absence never proves absence.

**`workflows/policy-test-cases.v3.json`:** an explicitly authored `importedUniverseSuite` with expected outcomes.
- **Rules:**
  - native control `file-exists` (non-gating);
  - `history-change-exists` (gating, optional history);
  - `runtime-hit-exists` (gating, optional runtime);
  - `runtime-hit-none` (non-gating).
- **Cases:**
  1. same-universe runtime and history hits → fail, three known findings;
  2. foreign-universe (rust) runtime, history and file rows → no finding; the imported rules are indeterminate; the native rule is a decided no-match; verdict indeterminate;
  3. foreign rows (rust unobservable runtime row, rust history row) beside a same-universe runtime hit → fail, with history listed as indeterminate;
  4. imported evidence absent → disclosed, verdict pass;
  5. same-universe imported absence → indeterminate.

  Summary: 4 passed, 1 indeterminate.

**`workflows/check-workflow-projection.v3.py`:** 8 `pt2` checks.
- suite schema admission and authored outcomes;
- same-universe runtime/history rows are known matches;
- foreign rows establish no known match;
- foreign rows behave **exactly like imported absence** (same verdict, findings and listed rules);
- a foreign uncertain row neither occupies nor weakens a same-universe hit;
- imported optional-evidence absence stays disclosed;
- `_imported_occupancy` requires subject and universe (typescript true; rust, syntax and another path false).

**Normative text:** no change. The published `factUniverse` law already states the universe join for every fixture fact.

**Other selectors:** `test-execution` / `test-case` stay unrepresentable, so no fixture row of any universe can occupy them; controls confirm this.

### Deltas

| delta | patch | sha256 | files |
|---|---|---|---|
| **combined vs frozen39** | `R/output/combined.patch` (1298 lines) | `9c1eea79e4df0558804583b1d5e5228c4e3c1c510c8391625b8b1bca71063e3f` | the same six v1 files, all modified: checker 111 patch lines, cases 1010, model 100, schema 29, `workflows_model.v3.py` 23, contract 25 |
| **incremental vs v1-applied** | `R/output/incremental.patch` (528 lines) | `bd7968b9a2b8a31a43bd784cf16b6da96f15e904e300ed9a3c94d7ba9a89edef` | checker 44, cases 460, model 24 |

The manifests are `R/custody/combined-delta-manifest.json` and `R/custody/incremental-delta-manifest.json`, with per-file before and after hashes.

## 4. Results after the fix (`R/receipts/`)

**Root probe** (post-fix path-only rerun, into a new directory, inputs byte-identical to root):

| source | fact universe | outcome | verdict | findings | listed | expectations |
|---|---|---|---|---|---|---|
| frozen39 (unchanged) | typescript | passed | fail | 1 | — | met, met |
| frozen39 (unchanged) | rust | failed | fail | 1 | — | unmet, unmet (defect remains in frozen39) |
| corrected copy | typescript | passed | fail | 1 | — | met, met |
| corrected copy | rust | indeterminate | indeterminate | 0 | runtime-hit | indeterminate, met (no unmet) |

**My discrimination probe:** 23/23 law rows.
- Runtime: foreign rust/syntax hit-only is unknown; the same-universe hit is a known fail; a foreign hit beside a same-universe hit still fails; foreign unobservable rows are unknown alone and don't weaken a hit; foreign `none` and `count-at-most` are unknown, not false, while same-universe rows give known false; absence with evidence available is unknown; optional absence is disclosed; required absence is a deficiency.
- History: same-universe hit fails; foreign `exists` and `none` are unknown; same-universe `none` is known false.
- Native: same-universe is a known fail; foreign universe is a decided no-match.
- Test-execution rows in typescript and rust stay unrepresentable.
- **White-box trace:** in a mixed run, `_imported_occupancy` returned false for both rust rows (unobservable and observed-hit) and true for the typescript row. Only the typescript row reached `_filters`. The direct helper check gives `[true, false, false]`.

**v1 regressions on the corrected copy:**
- v1 comparison probe (byte-identical copy, sha `bb7f65dc…`): 37/37 law rows. All 22 fixture-vs-composition comparisons still agree.
- Original independent probe (new path-only adaptation writing only into `R/work/repro-original`, diff `R/probes/original-probe.path-only.diff`): 50/50.

**Checkers on the corrected copy:**

| checker | result |
|---|---|
| `workflows/check-workflow-projection.v3.py` | **860/860**; vs v1 final (852): 8 added `pt2-*`, 0 removed, 0 flipped |
| `foundation/check-composition.v3.py` | 30/30 |
| `workflows/check-query-projection.v3.py --report` | 204/204 |
| `workflows/check_workflows.v1.py --report` (historical) | 1816/1816; stdout byte-identical to the frozen39 baseline; report differs only in its `sourceSha256` for the four changed workflow files |
| `foundation/check-array-orders.py --report` | 123/123 |

No child process remains.

## 5. Attempts not in a receipt

1. My first combined attempt to prepare and run the v1 regression probes was one inline `python -c` command. The tool permission layer denied it and nothing ran. I split the same path-only logic into the reviewed script `R/probes/make_regression_probes.py` (receipt `make-regression-probes`), then ran the two probes separately.
2. The first end-of-work recheck call exited 2 because I had not yet written `R/probes/end_of_work_recheck.py`. I wrote it and ran it under a receipt.

## 6. End-of-work recheck (`R/custody/end-of-work-recheck.json`, receipt `end-of-work-recheck`)

- **Frozen39:** all 12909 members still match; no unlisted file and no `__pycache__`.
- **Root's probe:** `probe.py` equals its recorded sha; the four suite inputs equal the hashes recorded at first read; `report.json` rows equal my pre-fix reproduction.
- **v1:** the delta manifest (`2114fd55…`) and patch (`8fe83cd1…`) are unchanged, and all six v1 corrected files still match their after hashes.

## 7. Limits

- **Bounded fixture reference.** Rows are finite path-only fixture rows with a declared universe token. There is no full Run, provider, native admission or import-wrapper completeness, and no claim here depends on a full Run.
- **Foreign uncertain rows can't be seen in route values.** Imported atoms decide only from known rows, so foreign uncertain rows never change a three-valued imported value in this model. Their exclusion is shown by the white-box occupancy trace and the helper check, not by route values alone.
- **Author expectations.** The authored `importedUniverseSuite` expectations follow the published `factUniverse` / `importedLaw` / `ruleLaw`; independent review is the oracle.
- **Checks run.** Only the checkers above were run; the full launcher and other children were not. Root rebinds pins, planning, reference and package, and integrates after the active independent review.
