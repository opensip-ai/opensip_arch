# Review request: D3B-0-r1 (the macOS descendant mechanisms; M3-D r5 items 4, 8, 16 and 18, D3b sub-unit D3b-0), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3b-0-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing, diffing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3b-0-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 6752 bytes, SHA-256 `ae101c3401fe4fe079fca06941913bae916a10c408a22af9cdc68fff66515d8d`, 30 members. Rehash every member.
- **The candidate base and lane base:** product main `2ead5cf1796bb85f363c34fa8ff8fba715462369`, as `source.json` and the lane's `checks.json` record. The candidate was written on `d704ed4`. The lane runner moved the worktree onto main inside the lane lock, after checking that main's changes since then (C2a-3k and C1b-1, security files only) are disjoint from the candidate's paths (`evidence/d3b0-checks-r1/rebased.json`).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3b0`, detached at `2ead5cf`. It holds the exact bytes `product-map.json` lists: 3 files, all in `crates/platform`, none new.
- **Main may move while you review,** by other units' integrations and lock-only inventory commits. Judge against `2ead5cf`. The integrate script refuses if main changes a candidate path.

## Authority

- **The D3b plan r3** (`docs/implementation/m3/supervisor-d/d3b/PLAN-r3.md`; your `codex-d3b-plan-r3`, ACCEPT; published with its lead record `reviews/codex-d3b-plan-r3/lead-assent.json`):
  - sub-unit D3b-0;
  - LD-D3B-3 and LD-D3B-4;
  - the conditions carried to D3b-0 from rounds 1 to 3: Q1, Q9 and RF-4, and the round-1 "Bounds" text;
  - §3's D3b-0 controls and mutations.
- **Law M3-D r5** (`PROPOSAL-r5.md`, by line): item 4 (:241-264); item 8 (:329-347); item 16's process counts (:533); item 18 (:579-628).
- **D1a and D3a-0 as integrated:** `crates/platform/src/process.rs`.

## What to review

`SCOPE.md` states the change table, four lead decisions (LD-D3B0-1 to 4), the six tests, the eight mutations and the four lane attempts before the lane of record. Judge:
1. **The bounded listings.**
   - Do `child_processes` (a pid count) and `group_members_bounded` (bytes) each use one buffer of capacity plus one slots?
   - Is a filled buffer `Exceeded`, never a truncated list?
   - Is `ListingCapacity` returned when the buffer does not fit the call's `int`, with no doubling?
   - Is the count against bytes distinction pinned by a test with exactly two children?
2. **`process_identity`.** It uses `PROC_PIDTBSDINFO`'s pgid and start time. Is `None` on `ESRCH` right, given that it covers a zombie (LD-D3B0-4)? Is every other failure `Io`?
3. **`Child::kill_descendant`.**
   - Before any read, does it refuse `AfterReap`, `Root`, `InitOrGroup` (pid ≤ 1, LD-D3B0-3) and `Host`?
   - Does it then reread the identity and send `SIGKILL` only on an equal pid and start time, with no comparison of start times for order (RF-4)?
   - Are the outcomes right: `Exited` for `ESRCH` or a zombie, and `Io {call: "kill"}` otherwise (LD-D3B0-2)?
   - Is the stated reread-to-send race item 18's best effort, and is it claimed as nothing more?
4. **Policy.** None is added: no walk, no bound and no eligibility rule in the platform. Is LD-D3B0-1 acceptable, with the unbounded `group_members` kept until D3b-1 moves the supervisor's callers?
5. **Tests and mutations.** Are they adequate, including the escapee's `setpgid` on both sides, the zombie case, and the below-root start time?
6. **The lane.**
   - The lane of record: platform 331 to 337, equal failure sets (none), and six new tests, run serially.
   - Clippy, the workspace check, operability, the unchanged census closure and verify_design.
   - The eight mutations.
   - The runner's move onto main inside the lock.
   - Attempts 0 to 3 and their stated causes. The `pid(` mint-census member led to the `process_id()` accessor.
7. **Rules:** no new mint-census call, no environment read, no `let _ =`, and all three files base-clean under rustfmt.

Answer SCOPE's Q1 and Q2 explicitly.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3B0-R1-RF-n` / `D3B0-R1-NBO-n`.
