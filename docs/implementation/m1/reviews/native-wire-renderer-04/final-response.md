# Review 04 verdict: changes required (1 finding, 4 advisories), subject `606639b2…1671b5`

Review03's selection-shape finding is fixed, but one representation problem remains. It has been there since subject-01, and I missed it in all three earlier reviews. `review.json` (it parses) and `review.md` are in `m1-native-wire-renderer-review-04/`.

**Integrity and reproduction:**
- Before and after my work, the 24 files matched their hashes and all 11 input pins equalled their origins.
- Only `render.py`, `test_render.py` and `UNIT.md` changed; everything else is byte-identical to subject-03.
- A fresh render gives identical `wire.rs`, `wire.ts` and `render-result.json`, and the 13 Python tests pass.
- I did not rebuild Rust or TS, since no compiled file changed; that evidence comes from review03.

**Review03 finding (fixed):** all 18 malformed payloads I tried are refused with `ValueError`. They include empty, one or three alternatives, a missing or unknown `select`, extra keys, the `selector` typo, and nested or mixed shapes. The mutations for exact keys, the empty-alternatives regression, the mechanism check, type-object alternatives and mixed type/selection are all caught.

## Required finding
- **RF-1: which selector a variant belongs to depends on JSON key order.** Selection variants are named `FactBatch0`/`FactBatch1` and `Unavailable0`/`Unavailable1` by their position in the alternatives object. No generated file records which selector value each one belongs to.
  - If an equivalent input lists `true` before `false`, it still renders, but `FactBatch0` now holds the V3 payload.
  - Two alternatives of the same type also render, and then position is the only thing telling them apart.
  - Today the two types differ, so the compiler would catch a mismatch in a hand-written decoder. But `UNIT.md` says M3 decodes by frame tag plus admitted host selector, so the mapping needs to be fixed rather than order-derived.
  - **Fix:** name variants from the selector key, or iterate in a fixed order per mechanism and record the key for each variant. Refuse or disclose same-type alternatives, and add a test that reordering the alternatives doesn't change output. The fixed-order option keeps today's output byte-identical.

## Advisories
- **A1:** removing the non-dict payload check or the alternatives-must-be-a-map check still passes every test. Those inputs then fail with `TypeError` instead of `ValueError`.
- **A2:** the positive test's TS check also matches Rust3 rows. Dropping only the Ts2 selection rows passes the Python tests; only comparing generated output catches it.
- **A3:** a selection object placed anywhere other than a frame payload fails with `KeyError` rather than `ValueError`.
- **A4:** review03's advisories carry over. `UNIT.md` now assigns closed-profile, name and injection validation to final integration.
