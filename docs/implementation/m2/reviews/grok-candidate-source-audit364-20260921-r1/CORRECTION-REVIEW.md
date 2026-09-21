# Correction review — candidate-source-audit-364-r2 (metadata only)

**Standing:** verification of the already-frozen **metadata-only** successor `candidate-source-audit-364-r2`. Frozen original 364, this folder’s `REVIEW.md` (`d93e0f3f…4f37`, 6713 B), and `ADDENDUM.md` (`39e812a1…5eac`, 2104 B) are **unchanged**. No regeneration, Unicode rerun, source edit, or test rerun. 365 code and inventory v53 are **not** this file.

---

## Pin / membership

Original 364: **239 members / 764700 B / SHA256 `163a7387367b1e78a6937d827fc6346e97c87db39ba9600d6f088f90d44c3ddf`**. All 239 members rehashed before comparing 364-r2.

364-r2: **240 members / 764572 B / SHA256 `349697ec6f7f8a8909ef51c6765bade1d15b66facdaf3d17a8663b5d5e565c17`**. Standing: “Metadata-only correction of364 fixture/source prose; no source/test changes or reruns.” Every subject member rehashed.

Vs original 364:

| | Paths |
|---|---|
| Unchanged | **238** (including `unlisted-files.json`, `result.json`, `LAYOUT.md`, all generators, logs, Unicode audit, expected outputs) |
| Changed | **README.md** only |
| Added | **ROOT-CORRECTION.md** |
| Removed | none |

That matches “all 239 original verified, only README changed + ROOT-CORRECTION added” (238 unchanged + 1 changed README = 239 original paths; plus 1 new file = 240).

---

## Counts

Frozen machine `unlisted-files.json` (byte-identical to original 364): **213** unlisted, **133** fixtures, **80** Rust. Independent recount of that JSON: 133 `fixture: true`, 80 `.rs`, 80 non-fixture.

Corrected README now states 80 Rust / 133 fixtures, records r4 as 81 other / 132 fixtures, and names the original **79/134** README claim as the prose error. That 79/134 string remains only as a description of the defect, not as an accepted split.

This matches the independent 364 REVIEW finding and ADDENDUM: pin-budget174 classification correction is real; 79/134 arithmetic is not accepted.

---

## Verdicts

- [x] **364-r2 is metadata-only:** pins match the request; 238 original members byte-identical; only README changed; ROOT-CORRECTION added; machine 213/133/80 unchanged. No source/test/generation change is claimed or observed.
- [ ] **Not** a regeneration rerun, inventory/runtime acceptance, 365 layout approval, or product installation.
