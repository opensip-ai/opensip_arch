# K1c sample accounting r2 — ACCEPT-UNIT

Closes K1C-ROOT-1. r1 (`/tmp/opensip-implementation/reviews/grok-k1c-accounting-r1`) accepted the sample-accounting component and left the r13 root-time implication to the later validator. The pinned ENV description requires `rootReapedElapsedNanos` to be non-null when `settlement-unverified-platform` is present and `run-failed` is absent. r2 enforces that implication in `summarize_slots`. This is still the sample-accounting component of K1c, not completion of K1c.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1c-accounting-r2` is detached at `ff90a5c2fe51be71e68d0eae7021e1dcbd7522d6`. The only dirty paths are the two untracked files. `evidence/k1c-accounting.diff` is 15166 bytes, sha256 `ba9552602b55c0826cbe4cc45ab2811793ea7badeece3b76023b47f38e5a69b0`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/measurement.py` | 5095 | `40ba28304ec4c2587df472afaaca3e79452b499e86e020eceec8b5cc17e8683e` |
| `tools/quality/test_measurement.py` | 9077 | `ba05b5d395c6760df93f26c1fe150d226f2d3880c43fc372971d620addb23c63` |

Against the r1 bytes (`measurement.py` sha256 `47a4fe3298846648a7bae0d6edd4e99cb2cc289a066149dd337d240b310982bc`, `test_measurement.py` sha256 `c256b68747fe27707b6b5275e6ca50e01c5a7681b4b2c3731e79c5aeb50dc4ee`), the module delta is two lines. After the existing check that a supplied root time requires `settlement-unverified-platform`, a measured slot whose root time is null, whose reasons include that reason, and whose reasons omit `run-failed`, raises `ROOT_REAPED_TIME_REQUIRED_UNLESS_RUN_FAILED`. A failed launch may still carry null. A supplied value is still refused without the settlement reason, and the value still never enters `elapsedNanos` or the median.

The test delta supplies that root time in the independent 15-reason and 105-pair table whenever `settlement-unverified-platform` is present without `run-failed`, and adds `test_unverified_settlement_requires_root_time_unless_run_failed`: null root with only that reason is refused, root time 9 is kept, and null is accepted once `run-failed` is added and the charged-memory sample is nulled with it.

The r1 QD-27 null mapping, seven positions, `sorted(elapsed)[3]`, peak maximum, and incomplete-on-any-reason rule are the same bytes.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1c-accounting-r2`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_measurement.py`

The clock before the run was 2026-10-06T03:35:54Z. 12 tests passed, 0 failed, 0.014s. That is the r1 set of 11 plus `test_unverified_settlement_requires_root_time_unless_run_failed`. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v145

Byte-identical to the r1 stage. The r1 structural assessment stands for these bytes.

Candidate `docs/implementation/m2/repository-file-inventory.v145.json` is 591225 bytes, sha256 `9cb22e61f30b2702bfe16c0196a60341d47b22903f19ed5204b373167f383689`. Parent v144 is 590018 bytes, sha256 `9f6c6009c174aa2ad914d34f24fc741f138fa95ba2ebd07d4c19cc737da58999`. Successor record is 307521 bytes, sha256 `9fdc292cc1371ac00ecd65a7c43bc5c523ea429cec3add3cfa22cafc2016df04`. Subject manifest is 669 bytes, sha256 `fe76ac6115e8baf41d87fbaf6b5176c667e412cac101097bb68629e7e1271615`.

v145 adds exactly the two `tools/quality` files. All 1025 parent rows are unchanged by value. `packages` and `pendingDecisions` are unchanged. The candidate standing sentence remains the v144 sentence. The 103 descriptions keep their design-lock before and after text by stable path. 102 selectors stay, and `tools/tests/test_check_crash_matrix.py` moves from index 972 to 974.

Inventory verdict: ACCEPT. No required findings.
