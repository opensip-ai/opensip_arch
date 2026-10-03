# Unit X9-4 r1

Verdict: **ACCEPT-UNIT**. Inventory: **NOT-APPLICABLE**.

Law X9 r15 item 12, the lock and live-revocation rows. Worktree `/Users/sb/code/opensip-ai/opensip-x9-4` is detached at `9c5f1455a671b87a5717e1a90cb9d0d59e39b247`. Nothing was committed. `git diff 9c5f145` is 341701 bytes, sha256 `73f8f98afa6d77f93154e653c9046ba6af422a229bbc6a363379a0e7fb9c117b`, four files, +572 −21. Porcelain stayed those four paths. `~/Library/Application Support/OpenSIP` stayed absent.

No file is added. The lock at `9c5f145` selects `repository-file-inventory.v133.json` (551621 bytes, sha256 `36ffd87a7cadb8b551e2c9e1816160a68fd0df42339f2595bb5644b015f775e1`), and that inventory already lists all four paths: `commit_tests.rs` (test), storage's `required-runs.v1.json` (fixture), `tools/check_crash_matrix.py` (validator), and its test.

## What this review ran

Private 0700 `TMPDIR` under `DARWIN_USER_TEMP_DIR`. `CARGO_TARGET_DIR` under this review directory. `cargo --locked --offline`. The two matrix sets ran one after the other, with nothing else running beside them.

| Check | Result |
|---|---|
| Census `OPENSIP_X9_CENSUS_ONLY=1`, run set `x94-grok-census` | Passed in 8.72 s. `census.json` is byte-identical to the pinned `x94-census` file: 244 points, kill set 313, normalized trace 1346 records, sha256 `8a5a5a31b004ba510fdca5f7baf222af7ddd1cd742589ff98f7afc1b7680d00f`. The refused-end part reaches `x3d.finish.settle.before` and all 29 durable `x3b.append.rev.*` points. |
| `transcribe_x94.py` on `git show 9c5f145` of the landed required-runs file and that census | 47 rows appended. Output is byte-identical to the worktree fixture (169678 bytes, sha256 `b12efe670c6c58c289ad7337cd83a35795a2dc64415fdb4dba1d6552e8220859`). The 288-row prefix is the landed file. Counts: F06 2, F14 1, F18 2, F19 31, F26 1, F30 2, F34 1, F38 1, F39 1, F40 3, F41 2. By `in_unit`: X9-2 231, X9-3 57, X9-4 47. The only `unit` member is F14's moved row, `X9-4`. |
| Checker unit tests | 18 passed. |
| `opensip-cli` release, no features | 6315264 bytes, sha256 `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`. Scan found no `OPENSIP_X9_` string and no registered scope. Profile `release`, features empty, `featureBuildRefused` true. The string list matches the lead record. |
| `cargo build --release -p opensip-storage --features crash-matrix` and `-p opensip-host --features crash-matrix` | Each exited 101 at `crates/platform/src/lib.rs:6`. |
| `x9_4_matrix` as `x94-grok-1`, then `x94-grok-2` | Each 47 PASS, 0 FAIL, 0 HARNESS-ERROR. 265.43 s and 260.25 s. |
| `check-unit --unit X9-4` on that pair | Passed, and the JSON is byte-identical to `lead-check-unit.json`: 47 runs, census 244, kill set 313, 30 killed points, limits L1–L11, repetitions agree, `matrixPass` false. |
| Digests across `x94-lead-1`, `x94-lead-2`, `x94-grok-1`, `x94-grok-2` | Every run's `normalizedSha256` and every child's trace digest agree. Canonical map sha256 `df056f01072db1daf9a164bbd01834efde0cdb6ff434078ac4bec6428862c286`, 47 entries, 18 distinct. |

Timing guard, 39 runs in each reviewer set, parent monotonic milliseconds, limit 5000: set 1 measured 2566 to 2878; set 2 measured 2568 to 2831. The values are not compared.

Both reviewer `matrix.json` files are 43929 bytes and carry the census trace digest above. They differ from the lead matrices because the release-absence path and the timing values differ.

## What this review did not rerun

The full workspace, clippy, `cargo fmt`, `check_package_edges.py`, and a fresh X9-2, X9-3, or X9-5 set were left as the lead recorded them. The pinned regression files were checked: their canonical maps are `4e5cba34…` (X9-2, 231 runs), `b0f0a5a8…` (X9-3, 57 runs), and `5446751d…` (X9-5, 94 runs). Each `check-unit` passed and the repetitions agree.

## Scope

The diff stays in the storage matrix target, its required-runs fixture, and the checker. Host's X9-5 runners and X9-6's full matrix check are outside it. Added lines contain no `cfg`, no `compile_error`, and no authority type. The commit driver gains `refused-end=1` and discloses F34's `ExistingAttempt` binding after the scored head. The census unions a lawful commit and that refused end, each twice and required equal. `owned()` and the checker's `in_unit` both send a row with a `unit` member to that unit only. F14 stays in X9-3's case list and is selected for X9-4 by `"unit": "X9-4"`.

The timing window starts when the parent has read the tick-armed child's first `x4.observer.tick` hold and ends at that child's first hold at any other point. F39's script still ends the window at `x3c.evidence.commit.before#1`. The foreign holder is the parent's own `BEGIN IMMEDIATE`, released after the writer exits. The ladder step appends, and an `unchanged` child's two comparisons are a `<n>-compared` ladder entry.

## Judgment calls

1. **`.gate` lists state changes only.** Accepted. An idempotent latch leaves the recorded sequence at F38's `0,2` and F39's `0,1,3`. The trace itself is unchanged.
2. **F30's second B is the ladder's R2, with the distinct variant.** Accepted. The post state is captured at the ladder, before that commit. `R2.outcome` is Committed. Both reviewer sets agree with both lead sets on F30's digests.
3. **Hold points where a row names none.** Accepted. F06 holds at `x3c.attempt.commit.after#1` and releases the foreign holder after the writer exits. F30 holds at that point or at `x2.lease.writer/lock.after#1`. F41's latch-first order holds at `x4.checkpoint.before-observation#3`.
4. **F40's no-latch variants use F12's scripts under case F40.** Accepted.
5. **Unscored ladder steps still run.** Accepted. F26, F39, and F41 leave R3 and R4 out of `expected`. F19's fail-stop variant leaves R2 unscored. F41 leaves the writer outcome unscored and bounds `writer.evidenceCommits` and `writer.gate`.
6. **F06 does not score the earlier level-3 release.** Accepted. There is no barrier point for it.
7. **F30's hold under the unarmed observer.** Accepted. Both sets agree with the lead sets, including every child trace.
8. **The `unit` member is read by `owned()` and `in_unit`.** Accepted. The new checker test covers the moved row, the extra-run refusal for X9-3, `check` still requiring it, and an invalid unit.
9. **The ladder appends, and F30(a)'s comparisons are a ladder entry.** Accepted. That entry adds no evidence member. X9-3's rows have one ladder step, and the pinned X9-3 regression map is unchanged.
10. **F18 and F19 release the tick after `x3d.finish.settle.before#1` passes.** Accepted. F19's kill rows never resume the tick.
