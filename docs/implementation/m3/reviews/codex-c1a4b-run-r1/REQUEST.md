# Review request: C1A4-BLIND-RUN-r1, the post-run review of the C1a4 blind validation run (C1a plan r6 RF-3 step 3)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-c1a4b-run-r1/`).

## Boundaries

- Do not edit either repository, the worktrees or the control files.
- Do not commit.
- Do not run Cargo, tests, either blind mode, the run script or the post-run checker.
- No network.
- Never read any T2 held-out store or overlay, the private 413 fixture, signing keys, held trees or `~/Library/Application Support/OpenSIP`.
- Do not use other panes and do not delegate.
- **Permitted:**
  - reading the two receipts (ids, verdicts and margins only);
  - hashing, JSON parsing and Git queries;
  - in the run worktree `/Users/sb/code/opensip-ai/opensip-c1a4b`, with `/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B` and the arguments `--architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip --t2-cache /Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1`:
    - `tools/security/discovery_census.py --check`;
    - `tools/security/snapshot_ledger_census.py --check`.

    The ordinary modes never open a held-out store.

## Subject

- **Manifest:** `docs/implementation/m3/snapshot-plan-c/c1a4-blind-run-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 7271 bytes, SHA-256 `0f1ad1a777af56504804a5ac938b93a04347ff2c4adf129236101955d3fa5a6f`, 25 members, plus a `gate` list pinning the C1a4-blind r2 records: the subject, the unit, `RUN-PLAN.md`, `run_c1a4_blind.py`, `run_c1a4b_post_checks.py` and your `codex-c1a4b-r2` review. Rehash every member and every gate pin.
- **The run worktree:** `/Users/sb/code/opensip-ai/opensip-c1a4b`, detached at product main `3742822e2823c3a7624aca3fea11220a46cffa16`: the frozen base `b753854` plus the gate commit. Its only changes are the four files `product-map.json` lists:
  - the two receipts, the companion's new;
  - the two census records.
- **Architecture:** `4088af763254018d6a3e70ef7b95c58b17ae8cc9`, which holds the gate (`c1a4-blind-r2/` and your `codex-c1a4b-r2`).

## Decide

1. **The authorized run.** Did it follow `run_c1a4_blind.py` exactly as authorized?
   - one invocation of each blind mode, the companion's after discovery's success, with empty stderr;
   - the preflight before anything was removed: the pinned post-run checker, the executable freeze, the detached clean worktree, the five tools on main and in the worktree, and the five architecture-side inputs;
   - only the stale discovery receipt removed;
   - the lane, nice 10 and a private TMPDIR.
2. **The receipts.**
   - Is each in its closed format, with every row measured, and every binding current against today's bytes?
   - Do the discovery receipt's changed bindings equal RUN-PLAN's exactly?
     - `closure`: its two rows;
     - `reference`: the generator closure;
     - `tool`;
     - the other five unchanged.
   - Are its rows equal to the old receipt's, as RUN-PLAN expects?
   - Are the companion receipt's seven bindings the expected ones?
   - Do its margins and verdicts agree with the snapshot profile's caps (2^21, 2^24, 2^33)?
3. **The census records.**
   - Do only the expected keys change from main's: `entries` and `heldOutMargin` for discovery's; `heldOutEntries` and `heldOutMargin` for the companion's?
   - Are every lead-readable and workspace row unchanged?
   - Are `failingEntries: []` and `caps: recorded-margin-holds`, and `failing2x: []` and `capsStatus: recorded-margin-holds`, right?
   - Do the two ordinary `--check`s pass with the new receipts?
4. **The post-run checks.**
   - The pinned checker's results: the composed-record margin and census tests, both blind control sets, verify_design.
   - The independent gate-identity check (`verify_c1a4b_gate_identity.py`, for your C1A4B-R2-NBO-1). It compares HEAD with the run record's `productBase` and repeats the gate-map path and byte checks. Does it satisfy that observation?
5. **Outcomes.** Under RUN-PLAN's outcomes, may the lead commit exactly these four files? Then the one inventory successor follows (v222, the companion receipt and the gate's controls; LD-C1A4B-5). Is C1a plan r6 RF-3 complete for C1a4, with every T2 entry within item 5 at 2× and the caps standing?
6. **Disclosure.** Does anything in the record or the evidence disclose held-out content beyond the owner's allowlist (ids, verdicts and per-mille margins)?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `C1A4BRUN-R1-RF-n` / `C1A4BRUN-R1-NBO-n`.
