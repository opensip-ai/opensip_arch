Codex review: unit **J3a** r2 of law M3-J1 r6, the durable entry, with **inventory v139**. This round answers RF-J3A-1 and nothing else. Grok leads as of 2026-10-04. You are the single reviewer. Verdict wanted: **ACCEPT-UNIT** on the product change and inventory v139, with an **`inventoryCandidateAssessment`**. J3a has no contract successor.

The r1 request, law pins, rulings and "not claimed" list still apply: `docs/implementation/m3/reviews/codex-j3a-r1/REQUEST.md`. Do not rewrite that review. r1 stays REQUIRED-FINDINGS at `/tmp/opensip-implementation/reviews/codex-j3a-r1/`.

**Rules:**
- No repository edits, commits, pushes or delegation.
- Write only under `/tmp/opensip-implementation/reviews/codex-j3a-r2`. If you build or test, use a `CARGO_TARGET_DIR` under that directory.
- Run git read-only, and only against the worktree named below.
- Run every command at `nice -n 19`, with a private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)`, and cargo `--locked --offline`. `CARGO_HOME` stays `/Users/sb/.cargo`.
- Before any cargo build, test or clippy, take `LOCK="$(getconf DARWIN_USER_TEMP_DIR)opensip-lanes.lock"` with `mkdir`, wait while it exists, and `rmdir` it only if your own `mkdir` succeeded. A lead-set rerun is not part of this review. If a script checks for load, match executables by `ps -Ao pid=,comm=`, never by command line. Do not leave a waiting process whose arguments mention `cargo`.
- Never touch `~/Library/Application Support/OpenSIP`. Never read the private 413 UUID fixture.

## The finding this round answers

RF-J3A-1 (P2), from `/tmp/opensip-implementation/reviews/codex-j3a-r1/review.json`. X8 r3 item 3 row F and item 3a's census: each non-public inherent constructor of a row D type is a group F case. r1's case-table comment said neither new identity type has a non-public inherent constructor, and that the census finds one feature-only constructor of `ReservedExecutionId` (the crash matrix's inject-id reservation). The code still had `ReservedExecutionId::reserved`.

The reviewer's alternative is the one taken: remove the private inherent helper and construct the value directly only on the uniqueness-checked registry paths. The group-F fixture was not added. The census comment is unchanged, and it is now true.

Both call sites insert into `ExecutionIdReservations` and only then build the struct:
- `ExecutionIdReservations::allocate` in `crates/platform/src/lib.rs`, after `self.reserved.insert(bytes)`;
- `reserve_injected_execution_id` in `crates/platform/src/crash_barrier.rs`, after the same insert. That function exists only under the test-only `crash-matrix` feature. It is the feature-only constructor the census already names. It is not an inherent constructor.

There is no `fn reserved` and no `ReservedExecutionId::reserved` call left in `crates/platform`.

## Subject

- **Worktree:** `/Users/sb/code/opensip-ai/opensip-j3a`, detached at **`b7b87b7`**. Not rebased. Product main has since bound HSR-1 at `2ea1571`; that binding is not part of this diff.
- **Diff:** `git diff b7b87b7` is 440454 bytes, sha256 `954c8ad416fc4631964f4c45bad0ee4b23562f221f715c7ab61191137ed5e86e`. A copy is `evidence/j3a.diff`. r1's diff was 440293 bytes, sha256 `76c7f540cc5c0a06d8f249b51c4c6e38c24ab4ecab704a365ab1c866b6d5c171`.
- **Inventory v139, unchanged by this correction.** No row was added and no description changed, so the candidate was not rebuilt.
  - Candidate `m2/repository-file-inventory.v139.json`, 583181 bytes, `f3bf66a6584e4fd41cef228aee9062c97ff670228c5f919c27ccd4762ad3061c`.
  - Parent v138, 571539 bytes, `90d5b09c…` (the r1 pin).
  - Record `m2/durable-entry-j3a-inventory-v139/successor.json`, 309837 bytes, `d7f57cc0caef2b2e8b5c1c69569773b6ab587771d036e7c0488dfe4bc843083e`.
  - Subject `m2/durable-entry-j3a-inventory-v139-subject.json`, 2556 bytes, `eb4b6f2f459d29f6ea8796baa381795923b00968dc62b64b59b282b3b5c4dac5`.
  - Staged worktree lock 521422 bytes, `e9d8fc07acf4e447589d358919c376994f9302991e329e5d9b69620e15b70372`, still the `SCRATCH-J3A` placeholders.
- **Lead rulings from r1 still stand.** The trust-admission ExecutionId stays undecided. Understated descriptions stay inherited.
- **X9 lead sets are not part of this review.** They run unniced, lock held for the whole set, on the integration commit, after acceptance. Do not treat their absence as a finding.

## Lead results (r2)

The worktree was `b7b87b7` before and after. The diff stayed 440454 bytes, sha256 `954c8ad416fc4631964f4c45bad0ee4b23562f221f715c7ab61191137ed5e86e`. `~/Library/Application Support/OpenSIP` was absent before and after. No source byte changed after these lanes. The r1 evidence script `newtests.sh` is not executable, so a direct `nice` exec exited 126 without running it. The same script was rerun with `zsh` and passed. Logs are under `/tmp/opensip-implementation/j3a-r2-lanes/`.

- **fmt** exit 0.
- **builds** exit 0: workspace, crash-matrix feature, scenario-fixtures, and the security feature build.
- **clippy `-D warnings`** exit 0 on those three lanes.
- **new tests** exit 0: 35 passed, 0 failed, 4 binaries.
- **workspace tests, twice:** each run 1805 passed, 0 failed, 3 ignored, 20 binaries.
- **doc tests:** 20 passed, 0 failed, 12 binaries.
- **crash-matrix feature lane:** 1703 passed, 0 failed, 3 ignored, 10 binaries.
- **drift** exit 0, `changed: []`, 40 sources, 8 outputs.
- **verify_scratch** staged exit 0 (inventory successors 98 to 99, v139 selected, 101 contract successors). **Plain verify_design** on the staged lock exit 1 with `missing or escaping regular file: SCRATCH-J3A/review.json` (expected). Plain verify_design on HEAD's lock exit 0.
- **verify_projection** exit 0: 103 rows, positive PASS, 518 corruptions refused.
- **package edges, dependency checkers and their tests** exit 0.
- **X9 lead sets were not run.** They are not part of this review. The lead runs them, unniced, under the lane lock, on the integration commit, before integrating.

## Decide

- Is RF-J3A-1 closed: no non-public inherent constructor of `RequestIdentity` or `ReservedExecutionId`, with the value built only after the uniqueness insert on those two paths?
- Does the plain surface still refuse a `ReservedExecutionId` from bytes, text, Default, Clone, Serialize or Deserialize, and is the inject-id reservation still absent there?
- Did any other behavior, inventory row or description change?
- Inventory v139: the bytes are the r1 candidate. Assess that candidate again for this round.

`review.json` needs:
- "verdict": ACCEPT-UNIT or REQUIRED-FINDINGS;
- "requiredFindings";
- "subjectSha256": `954c8ad416fc4631964f4c45bad0ee4b23562f221f715c7ab61191137ed5e86e`;
- "subjectManifestSha256": `eb4b6f2f459d29f6ea8796baa381795923b00968dc62b64b59b282b3b5c4dac5`;
- "inventoryCandidateAssessment": verdict, requiredFindings, the candidate's path, bytes and sha256, parent v138's pin, and successorRecord (the pin of `durable-entry-j3a-inventory-v139/successor.json`).

Do not commit.
