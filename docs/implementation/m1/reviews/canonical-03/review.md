# Bounded continuation: INV-01/INV-02 closure on m1-canonical-subject-04

This is a nonblind continuation of review02 (`m1-canonical-review-02`). Only the test relocation
and the corrected inventory candidate are in scope. Unchanged behavioural and crypto scopes are
not reopened.

- **Subject:** `m1-canonical-subject-04.json`, SHA-256 `581d747aa2fa59da7243f116e88e946340c584237276c3f480021dfbcc317e55` (recomputed).
- **Unit verdict: ACCEPT-UNIT.** Scope: this unit only.
- **Inventory candidate** `docs/implementation/m1/repository-file-inventory.v3.json`
  (`63027fb69f55b6fd65f3cb5baa89d355736239060bfa2750f3137e93cbb716ee`): **ACCEPT**, scoped to its
  four additions.

## Subject04 (Claude-executed)

- **Binding:**
  - The manifest hash matches, and all 13 rows match SHA-256 and length.
  - There are no extra files and no symlinks.
  - `predecessorManifestSha256` is subject03's hash.
  - After the single substitution `tests/conformance/test_design_binding.py → tools/tests/test_design_binding.py`,
    the path→(sha256, bytes) map equals subject03's exactly.
  - Every file is byte-identical to its subject03 counterpart. `tests/` no longer exists.
- **Test location:** `parents[2]` of `tools/tests/test_design_binding.py` is the product root, so
  the test still loads `tools/verify_design.py`. That import now stays inside `tooling`.
- **Runs, all with `-B` and `PYTHONDONTWRITEBYTECODE=1`:**
  - `python3 -I -B -m unittest discover -s tools/tests -t tools/tests -v`: 9 tests OK.
  - `python3 -I -B tools/verify_design.py --architecture opensip_arch`: passed, 46 inputs,
    application `dab6e00f…`.
- **No mutation:** comparing the before and after state of every snapshot entry (hash and mtime)
  shows nothing added, removed or changed. No `__pycache__` appeared, and the manifest still
  verifies.
- **Not rerun:** Rust and Cargo, whose bytes are identical to the subject03 I tested and
  accepted. Review02's results stand for them.

## INV-01 / INV-02 closure

- **INV-01: closed.**
  - Relative to candidate v2, the only row change is the moved test row. Its `path` becomes
    `tools/tests/test_design_binding.py` and its `package` changes `verification → tooling`;
    description, role, generated and standing are unchanged.
  - `tooling` and `verification` still declare `dependencies: []`, and the source import is now
    within `tooling`.
  - The record's "no package dependency edges changed" is now accurate.
- **INV-02: closed.**
  - `inventory-successor.v2.json` (`d0a42cac…`) claims `parentArtifactBytesUnchanged` and
    `inheritedRowsEqualByValue`, and gives `candidateRowOrder` as "lexicographic by path;
    original row positions are not preserved".
  - Verified:
    - v1 is still `47909b56…`, 69988 bytes.
    - All 198 v1 rows appear in v3 equal by value, and v3 rows are sorted by path with no
      duplicates.
    - The 20 packages and `pendingDecisions` are identical.
    - The only other top-level difference is the `standing` text.
    - The candidate's hash and size (71497 bytes) match the record.
- **The other three additions are unchanged from v2:** `design-lock.json` (repository/manifest),
  `tools/verify_design.py` (tooling/validator) and `crates/identity/src/canonical_tests.rs`
  (opensip-identity/test).
- **Historical records untouched:** candidate v2 `f4352ab3…` and its record `f7972a33…` still
  have the hashes they had in review02.

Accepting v3 covers only these four inventory additions. It does not accept the startup
refinements, the generation recipe, the metadata proposal, or build-lane or tool choices. Binding
v3 into the product design lock (the successor-binding feature) is not implemented, and still
needs its own review.

## Required findings

None, for either the unit or the inventory candidate.

## Advisories

The nonblocking code advisories ADV-R2-01 through ADV-R2-06 from
`m1-canonical-review-02/review.json` carry forward unchanged. They cover software-hash
performance, dependency provenance, the verifier remainder, H over unadmitted values, public
re-export test coverage, and memory, precedence and recursion.

## Limitations

- Rust tests, clippy, the dependency graph and the crypto differentials were not rerun, because
  their bytes are unchanged from subject03 (see review02).
- Architecture chapter 14 names no Python test-file naming convention. `tools/tests/` is judged
  only against package ownership and the import edge.
- Acceptance is not full M1. The design-lock successor binding, metadata and generation choices,
  and build lanes remain pending. All 32 release gates and 54 recovery cases remain unperformed.
