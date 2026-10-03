# Unit X9-5 r1

Verdict: **ACCEPT-UNIT**. Inventory v133: **ACCEPT**.

Law X9 r15 item 12, with the r10 through r13 host rulings. Worktree `/Users/sb/code/opensip-ai/opensip-x9-5` is detached at `eb0d50398035fe3532dadc332f88cf1d8bc4cb69`. Nothing was committed. `git diff eb0d503` is 147921 bytes, sha256 `1276f8f5a248bace1e45e22e04fa34ecf609b755a7e8ffaec28dbb05ca87d276`, five files, +2371 −6. The two new files are intent-to-add, so the diff includes them. Porcelain stayed those five paths. `~/Library/Application Support/OpenSIP` stayed absent.

The subject manifest is `docs/implementation/m2/crash-matrix-x95-inventory-v133-subject.json`, 2110 bytes, sha256 `3b9cc6f1e0d5afb9f8d765a476e113c5cb577af1388d80b7ccc98c1437388198`.

## What this review ran

Private 0700 `TMPDIR` under `DARWIN_USER_TEMP_DIR`. `CARGO_TARGET_DIR` under this review directory. `cargo --locked --offline`. The two matrix sets ran one after the other, with nothing else running beside them.

| Check | Result |
|---|---|
| Host census `OPENSIP_X9_CENSUS_ONLY=1`, run set `x95-grok-census` | Passed in 33.00 s. 218 points, kill set 271, normalized trace 1195 records, sha256 `93d0922ab69945043d769e0361fd0121662052ffadf44970c5425d78511cf8d6`. `census.json` is byte-identical to the pinned `x95-census1` census. |
| `transcribe_required_runs.py` on that census and `census-trace-b.txt` | 94 rows, 74 F32 kills. Output is byte-identical to host `required-runs.v1.json` (52135 bytes, sha256 `4fd160922f6772d48f77293754296e89e0c140ac5db2f8dd041d0acc431cd71c`). |
| `a_process_makes_at_most_one_runner_call` | Passed. |
| Checker unit tests | 17 passed. |
| `opensip-cli` release, no features | 6315264 bytes, sha256 `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`. Scan found no `OPENSIP_X9_` string and no registered scope. |
| `cargo build --release -p opensip-storage --features crash-matrix` and `-p opensip-host --features crash-matrix` | Each exited 101 at `crates/platform/src/lib.rs:6`. |
| `x9_5_matrix` as `x95-grok-1`, then `x95-grok-2` | Each 94 PASS, 0 FAIL, 0 HARNESS-ERROR. 712.43 s and 710.67 s. |
| `check-unit --unit X9-5` on that pair | Passed, and the JSON is byte-identical to `lead-check-unit.json`: 94 runs, census 218, kill set 271, 77 killed points, limits L1–L11, repetitions agree, `matrixPass` false. |
| Digests across `x95-lead-1`, `x95-lead-2`, `x95-grok-1`, `x95-grok-2` | Every run's `normalizedSha256` and every child's trace digest (record count and sha256) agree. Canonical map sha256 `5446751d769edc875a924abd07b288f0c4ae9c47c54d23c757c6f98095ebb285`, 94 entries, 18 distinct. |

Timing guard, parent monotonic milliseconds, limit 5000: F39 measured 1092 and 1079; F40's latch variant measured 1085 and 1091. The lead sets measured 1036, 1054, 1028 and 1096. The values are not compared. All are under the limit.

`matrix.json` for the two reviewer sets is 46716 bytes each. Both carry the census trace digest above. They differ from the lead matrices because the release-absence path and the timing values differ.

Inventory, against the worktree lock at `eb0d503`:

- A shadow rerun of `evidence/build_v133.py` reproduced `repository-file-inventory.v133.json` and `successor.json` byte for byte (551621 / `36ffd87a…`, 145171 / `c0a2b280…`). 967 files, two added, 55 projection rows, `supersessionsFolded` 0.
- `verify_projection.py`: PASS, 55 rows, 278 corruptions refused.
- `evidence/verify_scratch.py`: passed, 93 inventory successors, 75 contract successors, 55 inheritance rows, v133 selected.
- The lock is byte-identical to the product checkout's lock, still selects v131 (`caaada92…`, 548804 bytes), and binds 55 inheritance rows.

## What this review did not rerun

The full workspace, clippy, `cargo fmt`, and `check_package_edges.py` were left as the lead recorded them. One fresh X9-2 or X9-3 storage set was not run. The pinned lead regression files were checked instead: X9-2's map is `4e5cba34…` (231 runs, census 212, kill set 281, 219 killed points) and X9-3's map is `b0f0a5a8…` (57 runs, census 227, kill set 289, 11 killed points). Both `check-unit` results passed and the repetitions agree.

The raw `census-trace-a.txt` from this census is the same length as the lead's (1009 lines) and diverges at one interleaving, while `census-trace-b.txt` and `census-trace-c.txt` keep the same point sequence. The census JSON, which hashes the normalized lines, is byte-identical. Transcription reads trace (b) only.

## Scope

The diff is the host target, the two runners and the candidate file in `crash_matrix_support.rs`, the sites pin, and host's required-runs file. Storage's checker and its tests are unchanged from `eb0d503`. Host's file has 94 rows and no `unit` member. The cases are F01, F12, F16, F17, F32, F39, F40 and F53, in the counts the law's table names. X9-4's moved row and X9-6's combined check are outside this diff.

`finalize_commit` reads the on-disk candidate, then calls host's `finalize` with `operation` as the admit closure and the fixed 19-byte delivery phase. `store_gc` calls `maintenance::run` over `settlement_sweep`. Each report is values: terminations, the RunId string, exit, end and rollover disclosures, delivered bytes, or per-namespace sweep outcomes. A second runner call in the same process returns the invariant row. The one-entry test covers a missing candidate file (host I/O, no entry) and then both runners.

The `candidate` child makes one `operation` entry, opens a `CommitSession`, writes X3d-3's candidate, the distinct variant, and `core_closure`, then ends refused before `prepare_commit`. The `finalize` child replays that file before its own custody. The publisher child holds no operation and revokes the release subject of that closure. The ladder's ExecutionId is the finalize child's draw. F01 and F53 run no ladder.

The census is three unarmed runs, each twice and required equal: a lawful finalize, an exhausted-carrier finalize at tail `…988`, and a `store_gc` after a lawful commit on the same root. Only the named child's trace is counted. The union keeps the largest occurrence count. The digest is the normalized lines of (a), then (b), then (c).

`object_groups_ordered` in the host target is the same text as storage's copy. The timing window starts when the parent has read `x4.observer.tick#1` and ends when it has read the script's awaited hold. Host's two tick-armed scripts await `x3c.evidence.commit.before#1`, which is that next hold. The clock is the one line `type GuardClock = std::time::Instant;`.

The added `cfg` line is the target's whole-file support predicate, which the sites pin counts once. The no-sleep pin admits that clock line at most once in each matrix target.

## Judgment calls

1. **F32 and X3b item 4a case 2.** Accepted. A kill before the G+1 witness is durable expects R2's witness action OPEN; a kill after it expects OK. That is item 4a's one OPEN write of `COMMITTED (G+1, 0)`, which item 13's table calls ADVANCE on the closing tail. The law's row text is unchanged. The transcription splits at `x3b.append.terminal.commit.after` and `x3b.rollover.open.witness/rename.after`.
2. **Substituted target keeps the closure blobs.** Accepted. The variant rebinds the evaluator closure onto another project and merges the lawful candidate's blobs, so replay refuses on the invariant row with the closure bytes present.
3. **F01 and F53 run no ladder.** Accepted. F01 has no attempt row. F53 scores `gc1` to `gc3`.
4. **The publisher is a matrix child under the scripted clock and holds no operation.** Accepted. It is a separate process from every runner.
5. **R1 for F16, F17 and F39 is `committed-historically:*`.** Accepted. The rows state the standing and leave the settlement member to the existing `:*` match.
6. **r15's guard end needs no host change.** Accepted. Those two scripts arm only the tick and the admission hold, and the tick stays at `#1`, so the awaited admission hold is the first other hold.
7. **`GuardClock` is counted per file.** Accepted. Storage's line and host's line each stay at one. Every other line of the no-sleep files stays pinned.
8. **Intent-to-add for the two new files.** Accepted. The subject diff includes them, and nothing else is staged.
9. **Inventory 133, with 132 unused.** Accepted. The lock's selected parent is v131. Succession follows that pin.

## Inventory v133

ACCEPT on v131. The candidate adds `crates/host/tests/commit_matrix_tests.rs` (test) and `crates/host/tests/fixtures/crash-matrix/required-runs.v1.json` (fixture). 965 inherited rows are equal by value. Packages, edges and pending decisions are unchanged. The projection is the 55 rows already bound to v131, with no new supersession folded.
