# Review request: D3A-0-r1 (the supervisor's platform mechanisms; M3-D r5 items 4, 16, 18 and 20, D3a sub-unit D3a-0), round 1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d3a-0-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees, any T2 store or the T2 cache.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; and, in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d3a-0-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 17409 bytes, SHA-256 `5dc0f5cf0da5217797561fb634e506b199ce0314c4c15085d58e36fba15abc90`, 75 members. Rehash every member.
- **The candidate base and lane base:** product main `23b3871269c6553c96097084dd412b3aa95dec68` (the v218 lock).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d3a0`, detached at `23b3871`, holding the exact bytes that `product-map.json` lists (4 files, all in `crates/platform`).
- **Main may move while you review,** by D2b-0's binding (schemas, identity, host and storage schema files, and a lock commit). Those paths are disjoint from this candidate's.

## Authority

- the D3a plan r4 (`docs/implementation/m3/supervisor-d/d3a/PLAN-r4.md`; your `codex-d3a-plan-r4`, ACCEPT, with the LD-D3A-17 amendment): sub-unit D3a-0, LD-D3A-8, -9, -12, -14 and -17, and §3's D3a-0 controls and mutations;
- law M3-D r5 items 4, 6, 16, 18 and 20 (`PROPOSAL-r5.md`, by line);
- D1a as integrated (`crates/platform/src/process.rs`, your D1a reviews).

## What to review

`SCOPE.md` states the change table, four lead decisions (LD-D3A0-1 to 4), the tests and the three lane attempts. Judge:
1. **`try_reap`:** `wait4(WNOHANG)`, never blocking; `None` leaves the child reserved; it shares `settle_reap` with `reap`.
2. **`abandon` and `Unreaped`:** an abandoned root is never signalled or reaped again, and neither `Child`'s nor `Unreaped`'s `Drop` signals or blocks. The root hold and any attached scratch are kept for the process's life. Is LD-D3A0-4's control (a live child abandoned, observed through the `SYSCALLS` seam) adequate for the mechanism?
3. **The bounded walks** (`measure`, `remove_bounded`):
   - iterative, under held descriptors; no link followed; no listing collected whole;
   - every read, status read, descent and unlink charged before it is made, at the published costs, including `descend_cost`'s stack term;
   - removal's re-pass until a directory reads empty;
   - exhaustion is `Budget` with no errno; an I/O failure carries its call and errno (LD-D3A-17).
   Are LD-D3A0-2 (what the measure counts) and LD-D3A0-3 (descriptor depth, `EMFILE`) right? Is the exact-charge control sound, given that it prices the recorded calls independently of the charge sites?
4. **The sampler** (`resident_bytes`) over `proc_pid_rusage(RUSAGE_INFO_V0)`.
5. **The `test-fixture` feature:** it exposes only `LaunchSpec::fixture` (and the class), it is refused without debug assertions, and no manifest enables it.
6. **LD-D3A0-1:** the stale-root sweep keeps D1a's walk. Is that within the plan's scope?
7. **The lane:**
   - attempt 3 of record: platform 0 = 0, 6 new, run serially;
   - attempts 1 and 2 and their stated causes;
   - Clippy, the workspace check, the feature checks, operability, the unchanged closure and verify_design;
   - six mutations.
8. **Rules:** no new mint-census call, no environment read, no `let _ =`; the policy stays D3's.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D3A0-R1-RF-n` / `D3A0-R1-NBO-n`.
