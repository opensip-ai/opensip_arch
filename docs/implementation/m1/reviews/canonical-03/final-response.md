Subject04 is accepted (ACCEPT-UNIT), and inventory candidate v3 is accepted for its four additions, which closes INV-01 and INV-02; neither has required findings.

**Subject04 (`581d747a…`), checked and run by me**
- **Binding:** all 13 files match the manifest, with no extras. Moving the test to `tools/tests/test_design_binding.py` is the only change: after that one path swap, every file is byte-identical to subject03.
- **Tests:** the test still finds the product root, so its import of `tools/verify_design.py` now stays inside `tooling`. The nine Python tests ran from `tools/tests` with `-B` and all passed.
- **Verifier:** the real verifier passed with 46 inputs.
- **No side effects:** a before-and-after comparison of every snapshot file's hash and modification time showed nothing added, removed or changed, and no `__pycache__`.
- **Not rerun:** Rust, Cargo and the crypto checks, because those bytes are identical to subject03. My review02 results stand for them.

**Inventory v3 (`63027fb6…`)**
- **INV-01 is closed.** Compared with v2, the only row change is the test row: its path moves under `tools/tests/` and its package changes from `verification` to `tooling`. Package dependencies are unchanged.
- **INV-02 is closed.** The new successor record (`d0a42cac…`) no longer claims row positions were kept. It says the parent file is unchanged, inherited rows are equal by value, and rows are sorted by path. I checked:
  - v1 is still `47909b56…` (69,988 bytes).
  - All 198 original rows appear in v3 unchanged in value, sorted by path with no duplicates.
  - The 20 packages and pending decisions are identical.
  - Only the `standing` text differs.
- The other three additions are unchanged from v2, and the historical v2 candidate and its record still have their earlier hashes.

The acceptance covers only this unit and these four inventory additions. It doesn't cover full M1, binding v3 into the product design lock (not implemented yet), the startup refinements, the generation recipe, the metadata proposal or build-lane choices. All 32 release gates and 54 recovery cases remain unperformed. Review02's six nonblocking advisories carry forward by reference.

Files are in `/private/tmp/opensip-implementation/m1-canonical-review-03`:
- review.md
- review.json
- results/
