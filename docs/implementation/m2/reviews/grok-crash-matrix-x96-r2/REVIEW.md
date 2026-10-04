# X9-6 r2

**Verdict: ACCEPT.** The rerun on integrated commit `3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f` agrees with the lead's evidence, and the M2 matrix gate stands.

## Checkout

`/Users/sb/code/opensip-ai/opensip-x9-6` is detached at C and `git status --porcelain` is empty. Product main is at `3e64266` (F8a), with D3 at `30c5db1` between C and that tip. C is an ancestor of that tip. The matrix gate reviewed here is the gate on C.

The private temp directory is mode `0700`, recorded in `tmpdir.path`. `CARGO_TARGET_DIR` is `target/` under this review directory. `~/Library/Application Support/OpenSIP` is absent.

## Release absence

The release build of `opensip-cli` produced `target/release/opensip` in this review directory: 6315264 bytes, sha256 `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`. The checker's `release-absence` scan found none of the 26 strings (`OPENSIP_X9_` and the 25 scopes) and passed. Release builds of `opensip-storage` and `opensip-host` with `--features crash-matrix` each exited 101 at `crates/platform/src/lib.rs:6`. The binary hash was the same after those refusals.

`release-absence.json` in this directory is the record the four sets embedded. Its binary path is this review's release binary. Bytes, sha256, profile `release`, empty features, the 26 strings, empty `found`, `featureBuildRefused` true, and `passed` true match the lead record in the evidence directory. The lead record's path is `target/release/opensip`.

## Sets

The four sets ran one at a time, with `--locked --offline`, `--features crash-matrix`, and `--test-threads=1`. Each `x9_6_matrix` passed.

| Set | Test |
| --- | --- |
| `x96-grok-r2-1-storage` | 1919.37s, 381 runs |
| `x96-grok-r2-1-host` | 805.66s, 98 runs |
| `x96-grok-r2-2-storage` | 1922.70s, 381 runs |
| `x96-grok-r2-2-host` | 804.99s, 98 runs |

The harness wrote them under the worktree's gitignored `target/opensip-x9/`. The lead directories `x96-final-1-storage`, `x96-final-1-host`, `x96-final-2-storage`, and `x96-final-2-host` are still present, and their pins still match the evidence files.

## Checks

`tools/check_crash_matrix.py check --commit 3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f` on storage and host:

- Reviewer pair (set 1, set 2): `matrixPass` true. `passed` true, 479 runs, union census 321 points, kill set 383, 383 killed, `killedOutsideKillSet` empty, repetitions agree, limits L1–L11, `productQualification` false.
- Mixed pair (committed lead-1, reviewer set 1): the same scalars, `matrixPass` true.
- Lead pair (committed lead-1, live `x96-final-2`): `matrixPass` true. The checker's stdout is byte-identical to the committed `check.json` (56813 bytes, sha256 `cee0aaa1d6cde6715bb5e57b3a1f5650679aa022376fda93899cb931e9b299ab`).

Census traces match the committed check: storage 1379 records, `e9add21ea35fcd31da809930ed05c619cd36da3b77e818cfd8e651b6d4e8b61f`; host 1195 records, `93d0922ab69945043d769e0361fd0121662052ffadf44970c5425d78511cf8d6`. Storage has 88 distinct `normalizedSha256` values across 381 runs. Host has 18 across 98.

## Agreement

Every run's `postState.normalizedSha256` and every child's `trace` object were compared. `timingGuard` was left out of the comparison. Each pair below is 479 equal runs and 0 differing runs:

- reviewer set 1 against committed lead-1
- reviewer set 2 against committed lead-1
- reviewer set 1 against live lead-2 (`x96-final-2`)
- reviewer set 2 against live lead-2
- reviewer set 1 against reviewer set 2

Live `x96-final-1` matches the committed lead-1 runs on those same fields, 479 equal and 0 differing. The committed lead-2 `matrix.json` pins match the live `x96-final-2` run files, 0 mismatches.

## Evidence record

`hashes.txt` is 66611 bytes, sha256 `97f8367e46c07fddc627bb0661896b228e39348460af70cf29f1d535ed57da69`. All 491 file pins match, including both product `required-runs.v1.json` files at C. The footer line is `product commit 3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f`.

The directory matches r16's note on item 7: lead-1 storage and host `matrix.json`, census traces (`storage/census-trace.txt`, `host/census-trace-{a,b,c}.txt`), and `runs/`; lead-2's two `matrix.json` files; `check.json`; `release-absence.json`; `hashes.txt`. Storage `runs/` is 381 files and 18315301 bytes. Host `runs/` is 98 files and 3839504 bytes. Both are within 64 MB and are plain files. There is no `runs.tar.xz`.

The checkout is clean. Nothing was committed.
