# K1a T2 documentary manifest r1 — ACCEPT-UNIT

This accepts the documentary-manifest reader in the bound K1a corpus CLI. The accepted T2 manifest is original JSON, kind `opensip-t2-corpus-manifest`, schema `2-draft`, and it contains finite observational decimals such as `rustCfgPerKloc`. The canonical record parser refuses those decimals, so feeding the manifest through `parse` stopped at `MANIFEST-UNREADABLE` before fetch or verify. `manifest_document` reads that document without changing the canonical parser, encoder, case digests, or ledger digests.

## Subject

Worktree `/Users/sb/code/opensip-ai/opensip-k1a-manifest` is detached at `d3fcd4777ffb288f327e7e33e88d76ebf728b6c7`. The dirty paths are the modified `tools/quality/corpus.py` and the untracked test. `evidence/k1a-manifest.diff` is 8250 bytes, sha256 `94d7281f40f501662fbab6763fc7802edaf892fc3f0d25ec8796bfb4e1ddcef9`.

| Path | Bytes | SHA-256 |
|---|---:|---|
| `tools/quality/corpus.py` | 4839 | `539f158fd07b60d27e776f2137e2f0c9f651db98b2ac8cec742e28ce0b1bb6c7` |
| `tools/quality/test_corpus_manifest.py` | 4710 | `9b95e6878f72a73f53a3120d4e6b4d156aedcd546e85147b9526d23edbb85e54` |

Authorities match the pins. `DESIGN-r13.md` is 151216 bytes, sha256 `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`. `FETCH-SPEC.md` is 10659 bytes, sha256 `4ebe90a491721e48d252f11e6378b6c73312b506b59af89b24c03829416f8858`. The draft manifest is 322483 bytes, sha256 `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`.

## Reader

`manifest_document` accepts only a `bytes` value of at most 4 MiB. It decodes strict UTF-8, requires one JSON object, refuses duplicate keys at every object, and refuses `NaN` and infinities. Finite number tokens that are not integers become exact `Decimal` values, so `19.3` and `1e-20` keep the token text. Integers, bools, and null stay those types. Strings must be Unicode scalars. Containers at depth 32 are refused, and 31 nested arrays are admitted. The root must be an object. Trailing bytes and leading-zero integers are refused.

`main` now calls `manifest_document` on the original file bytes. Repository identity, the two algorithm ids, and workspace identity are the same checks as before. Fetch still passes `sha256` of those original bytes into acquisition. Verify calls `store.verify` and does not import the fetch module. `canonical` still rejects a `Decimal`, including one nested under a receipt field such as `licence`. The five workspace overlays in the published manifest remain canonical JSON. This reader does not interpret family, exposure, or source standing.

On the published documentary bytes, `parse` raises `FLOAT_OR_NONFINITE_FORBIDDEN`. `manifest_document` returns the object: kind and schema match section 2, and the 22 `rustCfgPerKloc` values are finite `Decimal`s. Verify of all 49 entries against a missing temporary store returned 49 `STORE-VERIFY-MISMATCH` lines and exit 1. No line was `MANIFEST-UNREADABLE`. No repository was fetched.

## Checks

From `/Users/sb/code/opensip-ai/opensip-k1a-manifest`, with `nice -n 10`, no `HOME` assignment, and no lane lock:

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_corpus_manifest.py`

`/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/quality/test_quality.py`

The clock before the pair was 2026-10-06T06:53:17Z. The new module ran 6 tests, 0 failed, 0.004s. The existing module ran 23 tests, 0 failed, 1.976s. No Cargo ran. `~/Library/Application Support/OpenSIP` was absent.

## Inventory v151

Candidate `docs/implementation/m2/repository-file-inventory.v151.json` is 598177 bytes, sha256 `8ef9dddf9fc9ef8f27719673747b5cd246c1413e961df912ab0717271c361e10`. Parent v150 is 597640 bytes, sha256 `2d78689209538698036df6513fca6c227f7de6b36fc4b5ce05c64bd80c86c1e7`. Successor record is 307509 bytes, sha256 `3d51907cccbc012785ee1adaffa058902702b755c5f0e1659989ac9c63dece6f`. Subject manifest is 665 bytes, sha256 `dcb85bf5bd6c4b0d9fe52fe8e9db29097bb69f9aaa7f9a6415b3548f402a7ebb`, and its three member hashes match the staged README, successor, and candidate.

v151 adds exactly `tools/quality/test_corpus_manifest.py` (index 974, package `tooling`, role `test`, `generated: false`, `standing: proposed`). `tools/quality/corpus.py` stays at index 964 and its inventory row matches the parent, including the acquisition and verification description. Files stay sorted and unique. All 1038 parent rows match by value. `packages` and `pendingDecisions` match. The candidate standing sentence remains the v150 sentence. The successor standing names this component. The 103 design-lock passages, parented on v150, keep their before and after text by path. 102 selectors stay. `tools/tests/test_check_crash_matrix.py` moves from `/files/985/description` to `/files/986/description`. `design-lock.json` is unchanged in the worktree. No `SCRATCH` pin is in the candidate.

Inventory verdict: ACCEPT. No required findings.

Network acquisition, public source inspection, family and exposure admission, and qualification remain separate obligations.
