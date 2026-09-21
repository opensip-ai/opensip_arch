# ADDENDUM — 364 README prose counts (not a rewrite of REVIEW.md)

**Standing:** documentation-count correction only. Frozen 364 archive and every member remain **unchanged**. REVIEW.md (`d93e0f3f…4f37`, 6713 B) is **unchanged**. Regeneration, Unicode full-scalar comparison, and source pins are **not** rerun. Root’s forthcoming 364-r2 freeze is metadata-only; this addendum does not author that freeze.

Root correction read: `/tmp/opensip-implementation/candidate-source-audit364-r2-correction/ROOT-CORRECTION.md` (copied as evidence `grok-out/ROOT-CORRECTION.md`, SHA256 `b5d94b66…6829`, 974 B).

---

## Accepted machine counts

Independent live recount (already in REVIEW.md §Inventory gap) and frozen `unlisted-files.json` agree:

| Set | Count |
|---|---|
| Unlisted total | **213** |
| r5 fixtures (`/fixtures/` in path) | **133** |
| r5 Rust sources | **80** |
| Inventory v32 rows not in candidate 363 | **114** |

r4 used `/tests/fixtures/`: **132** fixtures and **81** other, one of which was `crates/storage/fixtures/pin-budget174.json`. r5’s `/fixtures/` heuristic correctly moves that JSON into fixtures → **133+80**. The preliminary **80/133** total was already the right r5 split; the r4 heuristic error was separate.

---

## Original prose finding (not accepted)

Frozen README (SHA256 `28896c70…e95c`, 2588 B) and the 364 review request state that r5 supersedes 80/133 with **79/134**. That arithmetic is **false**. 79+134=213, but it is not the r5 JSON split and not the independent recount.

This review **did not** accept 79/134. REVIEW.md already recorded: pin-budget174 classification correction is real; 79/134 is not. Root now confirms the same prose error while drafting inventory33. Wrong README prose remains a **frozen documentation defect** until the separate metadata-only 364-r2 correction. It is not a generation/source-byte defect.

---

## Unchanged

No test rerun. No source, generator, or Unicode-table change. 365 layout and inventory v33 draft stay outside the 364 verdict. Five-member binding / current authority / writers / M2–M6 remain open.
