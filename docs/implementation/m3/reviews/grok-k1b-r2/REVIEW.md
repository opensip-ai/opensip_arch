# K1b r2 — ACCEPT-UNIT

Closes K1B-ROOT-1 on the r1 confidence module. r1 was ACCEPT-UNIT with no findings (`/tmp/opensip-implementation/reviews/grok-k1b-r1`). Root assent was withheld because a `Decimal` that compares equal to `Fraction(99, 100)` or `Fraction(9, 10)` could enter `k_min` and `statistic`, and `Decimal` exponentiation rounds. r2 refuses every target whose type is not `Fraction` before either function exponentiates. The inventory candidate is unchanged.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1b-r2` is detached at `f5f5b4d20eca34ab2312b3ffc141c378da326afe`. The only dirty paths are the two untracked files. `evidence/k1b.diff` is 15266 bytes, sha256 `25ed40cd387c297b01647255cc74f72287251af93f94e0c6546cdb39bd4cf528`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/confidence.py` | 7041 | `34633edd0db9f028db01ec11d41906353f89141c998361d2572ed92a0cea7f90` |
| `tools/quality/test_confidence.py` | 7293 | `0022ed67fcf2fb5ad8acbeb08d999ac9a9b60ae0e08ff1ada73bf515fa269f7e` |

Against the r1 bytes (`confidence.py` sha256 `12384f05b8d7f83cd5c97929db211c41e535a6ecd16d5ee793f9446ff5d666ab`, `test_confidence.py` sha256 `915561e98d5149cde942a1a0518f19e2baf542f9097b0428f637d8eef13e4398`), the delta is exactly four lines plus one test.

`k_min` and `statistic` now begin with `type(target) is not Fraction or target not in TARGETS`. Both checks stand before `target**k` and before the exact pass comparison. The test imports `Decimal` and refuses `Decimal('0.99')`, `Decimal('0.90')`, `0.99`, `0.90`, and `True` at both functions.

On this interpreter, `Decimal('0.99') == Fraction(99, 100)` and `Decimal('0.90') == Fraction(9, 10)` are both true, which is why r1's membership test admitted them. `Decimal('0.99') ** 29` differs from `Fraction(99, 100) ** 29` under the default precision of 28. Float `0.99` and `0.90` do not compare equal to those fractions; r2 refuses them by type as well. `True` is not a `Fraction`.

No other statement in the module changed. The r1 arithmetic, status order, population conservation, and ENV vocabulary are the same bytes.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1b-r2`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_confidence.py`

The clock before the run was 2026-10-06T03:18:14Z. 18 tests passed, 0 failed, 0.011s. That is the r1 set of 17 plus `test_fixed_targets_require_fraction_type`. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v144

Reaffirmed, not reopened. The staged candidate, successor, subject manifest, and README are byte-identical to the r1 stage.

Candidate `docs/implementation/m2/repository-file-inventory.v144.json` is 590018 bytes, sha256 `9f6c6009c174aa2ad914d34f24fc741f138fa95ba2ebd07d4c19cc737da58999`. Parent v143 is 588871 bytes, sha256 `2745e424f78185a4cda1da3dc573e753356a43a5985059d847dc5c5f44299acc`. Successor record is 307518 bytes, sha256 `8966af25b33df33896f26f1752588175d36831b0a437176dd04783ac54882b44`. Subject manifest is 647 bytes, sha256 `a8a2a6e54e92f05f4a47de632814a00c5e3af6157f38006b90506903f4d6c35e`.

The r1 assessment still holds for these bytes. v144 adds exactly the two `tools/quality` files. All 1023 parent rows are unchanged by value. `packages` and `pendingDecisions` are unchanged. The candidate standing sentence remains the v143 sentence, which the additive profile allows. The 103 descriptions keep their v143 before/after text. 102 selectors stay, and `tools/tests/test_check_crash_matrix.py` moves from index 970 to 972.

Inventory verdict: ACCEPT. No required findings.
