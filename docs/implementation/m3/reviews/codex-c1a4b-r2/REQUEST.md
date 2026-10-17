# Review request: C1A4-BLIND-r2, the pre-run gate (the companion snapshot blind mode, and the C1a4 blind validation run; C1a plan r6 RF-3), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a4b-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane. Do not take the shared lane lock.
- Do not run either census tool with `--t2-cache` or `--held-out-blind`, and do not run `evidence/run_c1a4_blind.py`, `evidence/run_c1a4b_post_checks.py` or the lane's blind-equivalence program.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay.** This review is the gate before any is opened.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - the committed discovery receipt `crates/security/src/custody/discovery_census_held_out.json` (ids, verdicts and margins only);
  - in the candidate worktree: `python3 -I -B tools/tests/test_snapshot_ledger_census_blind.py` and `python3 -I -B tools/tests/test_discovery_census_blind.py`, which are synthetic and hermetic;
  - in the candidate worktree: `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, which checks the vectors only and reads no T2 store.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a4-blind-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 10356 bytes, SHA-256 `2aed6034e37a9e1c5e62e6d3ebde9f8e48ac16b074d5e23948e681b6261327ef`, 44 members. Rehash every member.
- **Your round 1:** `codex-c1a4b-r1` (REQUIRED-FINDINGS, `runAuthorized: false`: C1A4B-R1-RF-1 and NBO-1), at `/tmp/opensip-implementation/reviews/codex-c1a4b-r1/` and copied under the architecture repository's `docs/implementation/m3/reviews/codex-c1a4b-r1/`. The round-1 package `c1a4-blind-r1/` and its subject are frozen history. **No product byte changed:** the four candidate files are round 1's.
- **Bases:** product main `b7538549b727e13013f36d3b7c2e2917e767f3f2`, clean (C1a4 integrated, inventory v221 bound; D2b-0b integrated, 175 contract successors); architecture as `source.json` names. **The gate freezes on this main:** nothing else integrates before the run, and C1b-0 (which changes the generator closure again) is sequenced after it (`RUN-PLAN.md`, precondition 4).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-c1a4`, detached at the product base. It holds the exact bytes `product-map.json` lists (4 files, 1 new).

## Authority

- **The owner's decision of 2026-10-16** (`docs/implementation/m3/owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`): the mechanical blind run.
- **The C1a plan r6** (`docs/implementation/m3/snapshot-plan-c/c1a/PLAN-r6.md`; your `codex-c1a-plan-r6`): RF-3, steps 1 to 4.
- **The B2-b4 plan r6 §2.5** (`docs/implementation/m3/config-discovery-b/b2-b4/PLAN-r6.md`): the blind receipt, its allowlist and its lifecycle.
- **The accepted M3-C r9** (`docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md`): the caps, the pricing and the over-item-5 classification.
- **C1a4** (your `codex-c1a4-r1`, ACCEPT-UNIT, with C1A4-R1-NBO-1 and NBO-2 carried here).
- **The precedent:** B3-b3a2 (your `codex-b3b3a2-r1`, the pre-run gate carrying the run plan and script) and B3-b3b (your `codex-b3b3b-r1`, the run). Note B3-b3b's missed `sizes` expectation.

## What to review

`SCOPE.md` opens with a "Round 2" section, then describes the unit and lead decisions LD-C1A4B-1 to 5. `RUN-PLAN.md`, `evidence/run_c1a4_blind.py` and `evidence/run_c1a4b_post_checks.py` are the run. Judge, first, round 1's findings:
- **C1A4B-R1-RF-1.** Is the post-run checker now in the package and the subject, with its exact bytes? Does the run script refuse unless the file beside it has the pinned SHA-256? Are both invocations in `RUN-PLAN.md` unambiguous: the pinned interpreter and the committed paths? Does the checker refuse unless the run worktree is the run's: detached at main, main the freeze plus the gate commit, and changes exactly the four run files?
- **C1A4B-R1-NBO-1.** Before anything is removed, does the run script assert all of the following, and do they freeze every bound input?
  - main is `b753854` plus exactly one commit, the gate's, changing exactly the product-map paths to their candidate bytes;
  - the run worktree is detached, clean with no untracked file, and a worktree of the product repository;
  - the architecture-side bound inputs keep their gate bytes.

Then, as in round 1:
1. **Confidentiality of the companion blind mode.** Over a held-out tree, can it emit, print or store anything but the closed row and the one stdout line? Consider:
   - every exception path in `blind_row`, `measure`, `d15_terms` and the snapshot model;
   - the `require` messages;
   - `SystemExit`;
   - the command line's redaction in `main`.

   Is the canary control adequate?
2. **Access.** Does the companion reach held-out stores only through `discovery_census.held_out_store_path` with discovery's token (LD-C1A4B-1)? Does its ordinary mode never touch one? Is reusing discovery's join from a second tool acceptable?
3. **Equivalence.** Does a blind row's margin and verdict equal what the lead-readable row gives for the same tree: one `measure`, the population check, the margins against the profile's caps? Does the lane's blind equivalence, over every lead-readable store presented as held out, show it, and does that program open only lead-readable stores?
4. **NBO-1, the binding** (LD-C1A4B-3).
   - Is `snapshotSources` the complete snapshot cost-source closure: the model's pinned and anchored files, the session's, the ledger, sealing, and the identity bound and encoding sources? Do discovery's receipt bindings in full, the four tools, the caps, item 5's bounds, the depth bound and the sealing bound complete it?
   - Does the completeness control (the census building in a product holding only the bound sources, and every named path bound) establish it?
   - Is freshness checked before a receipt is composed?
5. **NBO-2, row identity.** Does the margin test now compare the record's unique id sets with discovery's compiled lead-readable and held-out rows, so a consistently truncated or duplicated record fails? Check the two record mutations.
6. **The closed formats and the over-item-5 row** (LD-C1A4B-2). The lead ruled that the row may carry only `id`, the status and `integrity`, and `population` only as a closed label. `population` is kept as the population check's boolean verdict. Is the row within the owner's allowlist? Are the state rule and the validation right?
7. **The record changes** (LD-C1A4B-4): only `heldOutEntries`, `heldOutMargin`, `capsStatus`, `counts.heldOut`, the tool pin and the standing text; every lead-readable row byte-equal.
8. **The run.** Does `run_c1a4_blind.py`:
   - run each reviewed blind mode exactly once, the companion only after discovery's success, in a clean detached worktree of main;
   - pin the companion's bytes to this gate's `product-map.json`, the four unchanged tools to main's, the architecture-side inputs to their gate bytes and the post-run checker to its reviewed bytes;
   - assert the freeze and the run worktree before removing anything;
   - remove only the stale discovery receipt;
   - hold the lane, nice 10 and a private TMPDIR;
   - record the comparison `RUN-PLAN.md` states?

   **Are the expected bindings complete** (B3-b3b's lesson)? For discovery's receipt, against `b753854`: exactly `closure` (its two rows, C1a4's), `reference` (its one row, `tools/contracts/generator-closure.json`, D2b-0b's) and `tool` changed, and `limits`, `manifest`, `memberModel`, `rootLengths` and `sizes` unchanged. For the companion's, all seven new. Is the freeze sufficient? Is "every discovery row equal to the old receipt's" the right expectation? Does anything read held-out content outside the two blind modes? Are the outcomes and the failure path right?
9. **Evidence:** `evidence/c1a4b-checks-r2/`, the lane of record, on `b753854`, rerun over the unchanged candidate. Check:
   - the security suite (14 = 14, no new test);
   - Clippy and rustfmt;
   - the focused margin and census tests;
   - the 21 companion and 25 discovery blind controls;
   - the equality projection;
   - the three `--check`s over the lead-readable cache;
   - the blind equivalence (39 lead-readable stores, all equal);
   - the census closure unchanged;
   - the environment exceptions, operability and verify_design;
   - the eight mutations.
10. **LD-C1A4B-5, inventory:** is one successor after the run, for both new paths, acceptable?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "runAuthorized": true|false}`, with ids `C1A4B-R2-RF-n` / `C1A4B-R2-NBO-n`. `runAuthorized` is true only if the run may proceed exactly as `RUN-PLAN.md` states, once this unit's code is on main at the reviewed bytes.
