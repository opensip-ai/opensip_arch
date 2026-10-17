# Review request: D4-1-r1 (`crates/components/src/manifest.rs`, the manifest-class excluded forms; M3-D r5 item 24), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d4-1-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not run Cargo, rustc, builds or lanes.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, private test keys, held trees, held-out entries, any T2 store or overlay, or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - `python3 -I -B tools/check_operability.py source --repository /Users/sb/code/opensip-ai/opensip-d4-1`;
  - `python3 -I -B tools/verify_design.py --architecture /Users/sb/code/opensip-ai/opensip_arch --implementation /Users/sb/code/opensip-ai/opensip-d4-1`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d4-1-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 9,803 bytes, SHA-256 `5b80d96dbaba2d2e4c949828e5adda6ec36603c21d014cdae8c06d1a9a199eb6`, 43 members (the scope, source record, product map, archived product files and lane evidence). Rehash them.
- **Candidate:** worktree `/Users/sb/code/opensip-ai/opensip-d4-1`, detached at product main `ae141a389b21997fb654f372a06c22cbeb2cc9d5` (C1b-1 integrated; inventory v227). Three changed paths: `crates/components/src/manifest.rs` (new; it realizes the inventory's planned row), `crates/components/src/manifest_tests.rs` (new) and `crates/components/src/lib.rs` (base-clean).
- **Architecture base:** `d547f2286bdf02745968caf4399bb7eafe7f0f35`.
- **Main may move while you review,** by other units' integrations. Read the base with `git show ae141a3:<path>`.

## Authority

- **The accepted plan:** D4 plan r2 (`docs/implementation/m3/supervisor-d/d4/PLAN-r2.md`; `reviews/codex-d4-plan-r2/review.json` ACCEPT with NBO-1; lead assent `reviews/codex-d4-plan-r2/lead-assent.json`), sub-unit D4-1: LD-D4-2 to LD-D4-10, §3 and §5's D4-1 controls, with round 2's Q1 to Q5 rulings (checked arithmetic and index conversion, no hidden sort scratch, the nine-pair projection, empty and singleton behaviour).
- **The law:** M3-D r5 item 24 (`supervisor-d/PROPOSAL-r5.md`:752-825), with D4-T4 and D4-T1's interface half; J1 r7 row 56 (`host-pipeline-j/PROPOSAL-r7.md`:826).
- **The sources the code pins:** the pinned manifest schema `tools/security/inputs/manifest-schema.json` (CMS's projection), and the native capability matrix `crates/host/src/native_capability_matrix.v2.json` (its nine provider pairs, as the round 2 Q3 ruling lists them).

## What to review

1. **Exactness against the plan:** the projection types; the policy's order checks; EE-1, EE-3b and EE-5a's arms (a), (b) and (c), in order; EE-4 carried by the pins only; `ExcludedFormClass`'s six members and order; `admit`'s algorithm (LD-D4-8); `Cleared` authorizing nothing; no parser and no security dependency.
2. **Accounting (RF-1 of the plan's round 1):**
   - every allocation, comparison and probe charged before its work, at LD-D4-10's prices;
   - the count and fill passes charged identically;
   - no hidden allocation;
   - saturating cost arithmetic refused by the ledger rather than wrapped;
   - `u32` index conversion refused before any charge.

   Judge whether the tests' independent model and per-site one-unit-short checks establish this, rather than restate the module's constants.
3. **The closed-world pins** (LD-D4-5, round 1 Q3): the nested CMS property sets and the exhaustive claim-type patterns.
4. **The controls and mutations:** the lane's 20 mutations each fail a focused test, not a compile (`evidence/d4-1-checks-r1/controls.json` and the mutation logs).
5. **Rules:**
   - no new mint-census call (the source census passes);
   - no `let _ =`;
   - no environment read;
   - rustfmt clean on the edited files (all base-clean or new).
6. **The lane evidence** (`evidence/d4-1-checks-r1/`):
   - The components suite has 73 → 88 passing tests (15 new). The same 54 supervisor tests fail on base and candidate alike. They are D3a's fixture-child tests. Each panics because `target/debug/deps/supervisor_fixture.path` "is written by the lane (LD-D3A-9); this test runs only there" (`supervisor_tests.rs`:353), and D4-1's generic lane does not build that fixture. The failing set is identical on both sides, and D4-1 changes no supervisor file.
   - Clippy (warning-denied, all targets), the workspace check, the release build, the focused tests, the environment exceptions, the operability source census, the census-closure check and verify_design all pass.
7. **Inventory:** two new paths, and the additive successor follows after integration (`/tmp/opensip-implementation/prepare_d4_1_inventory.py`). The integrate script is `/tmp/opensip-implementation/integrate_d4_1_r1.py`. Check that it refuses on overlapping main changes and checks only its own paths.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D41-R1-RF-n` / `D41-R1-NBO-n`.
