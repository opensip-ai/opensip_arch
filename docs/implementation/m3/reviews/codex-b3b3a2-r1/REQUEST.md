# Review request: B3-B3A2-r1, the pre-run gate (the blind mode over the D15 terms, and B3-b3b's run; M3-B unit B3-b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b3a2-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- Do not run the census tool with `--t2-cache` or `--held-out-blind`, and do not run `evidence/run_b3b3b_blind.py`.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- **Never open a T2 held-out entry's store or overlay.** This review is the gate before any is opened.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - the committed receipt `crates/security/src/custody/discovery_census_held_out.json` (ids, verdicts and margins only);
  - in the candidate worktree, `python3 -I -B tools/tests/test_discovery_census_blind.py`, which is synthetic and hermetic;
  - in the candidate worktree, `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, which checks the vectors only and reads no T2 store.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b3a2-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 14119 bytes, SHA-256 `afa0e3a3c4fcf0bc1e0f4b1ad4223d2c59d415781c5ceae39ae08f3ad4989651`, 59 members. Rehash every member.
- **Bases:**
  - product main `2dd54bae4afa0f6494ff2c4208982af5fcd7ff41`, clean (B3-b3a1 bound, inventory v208, 170 contract successors);
  - architecture `abbf48fb0992b48178bf3de0aac2c42015e48b4e`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b3a2`, detached at the product base. It holds the exact bytes `product-map.json` lists.

## Authority

- **The owner's decision of 2026-10-16** (`owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md`): the mechanical blind run.
- **The B2-b4 plan r6 §2.5:** the blind receipt, its allowlist and its lifecycle. Your `codex-b2b4c1-r2`, `codex-b2b4c3-prerun` and `codex-b2b4c3-r1`.
- **The B3-b plan r2 amendment A5** (your `codex-b3b-plan-a5-r1`):
  - A5-2's B3-b3a2: the blind mode extended to the new terms, margins only, with B2-b4c's output allowlist unchanged; the receipt's binding covering the extended closure; the controls extended; your acceptance of these exact bytes before any held-out store is opened;
  - A5-2's B3-b3b: the blind run of this tool.
- **B3-b3a1** (your `codex-b3b3a1-r1`, ACCEPT-UNIT, with NBO-1 on the no-follow wording).

## What to review

`SCOPE.md` describes the unit and lead decisions LD-B3B3A2-1 to 3. `RUN-PLAN.md` and `evidence/run_b3b3b_blind.py` are the run. Judge:
1. **Confidentiality.** Over a held-out tree, can the extended blind mode emit, print or store anything but the closed row? Consider:
   - the carriers' text kept in memory and parsed by the terms;
   - every exception path in `blind_measure`, `repository_terms`, `d15_terms` and `full_ledger`;
   - the `require` messages;
   - `SystemExit`.

   Is the canary control over the real terms (canary carriers, valid and malformed) adequate?
2. **Equivalence.** Does a blind row's margin and verdict equal what a lead-readable row's `d15.fullLedger` would give for the same tree? Look at:
   - `repository_terms` shared by both;
   - the byte margin at R = 4,096;
   - the verdict check;
   - the lane's blind equivalence over every lead-readable store, which presents each to `blind_row` as held out.

   Does that program open only lead-readable stores?
3. **LD-B3B3A2-1, the format kept.** Is "margins and verdict are the full ledger's, no new key, schema version unchanged" the right reading of "margins only, with B2-b4c's output allowlist unchanged"? Is a single full-ledger verdict equivalent to the lead-readable rows' failing rule? Is the walker-only committed receipt correctly stale rather than refused?
4. **The binding.** Does a change to the tool, the member model or any closure file make a receipt stale? Is anything else the blind row depends on left unbound?
5. **The controls.** The six new and one extended, the synthetic rule (LD-B3B3A2-3), and the three mutations. Is any regression the gate should catch left uncaught?
6. **NBO-1.** Is `read_envelope`'s docstring now accurate about which reads are no-follow?
7. **The run.** Does `run_b3b3b_blind.py`:
   - run the reviewed blind mode exactly once, in a clean detached worktree of main;
   - pin the tool's and the member model's bytes to this candidate's;
   - remove only the stale receipt;
   - hold the lane, nice 10 and a private TMPDIR;
   - record the comparison `RUN-PLAN.md` states?

   Does anything in it read held-out content outside the blind mode? Are the outcomes and the failure path right?
8. **Evidence:**
   - equal base failure sets and no new Rust test;
   - the equality projection (only the vectors' `/memberModel`);
   - the census `--check`;
   - the blind equivalence;
   - the 25 blind controls;
   - the mutations;
   - verify_design.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...], "runAuthorized": true|false}`, with ids `B3B3A2-R1-RF-n` / `B3B3A2-R1-NBO-n`. `runAuthorized` is true only if B3-b3b may proceed exactly as `RUN-PLAN.md` states, once this unit's code and lock are on main at the reviewed bytes.
