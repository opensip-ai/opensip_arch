# Review request: D1A-r2 (the spawn primitive, `crates/platform/src/process.rs`; M3-D r5 items 1 to 8, macOS), round 2

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-d1a-r2/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 store.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository .`.

## Subject

- **Manifest:** `docs/implementation/m3/supervisor-d/d1a-r2-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 15127 bytes, SHA-256 `83551ba384edb7f6339f8d36ff31055b93b671ed92909b97ddf8189a92cc80bf`, 66 members. Rehash every member.
- **Bases:** product main `808ad6476fb848f84e732ee233a47229370081f4`, clean (inventory v212, 173 contract successors).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-d1a`, detached at the product base, holding the exact bytes `product-map.json` lists.
- **Round 1:** your `codex-d1a-r1` (`/tmp/opensip-implementation/reviews/codex-d1a-r1/`), REQUIRED-FINDINGS with D1A-R1-RF-1 to RF-5 and two NBOs. The r1 package `supervisor-d/d1a-r1/` is history.

## Authority

- **The D1a plan r2** (`supervisor-d/d1a/PLAN-r2.md`; your `codex-d1a-plan-r2`, ACCEPT; NBO-1 carried in `reviews/codex-d1a-plan-r2/lead-assent.json`).
- **Law M3-D r5** section A, items 1 to 8.
- **The contracts:** BBC (`docs/coop/completion/broker-bootstrap.contract.v2.md`) and DRJ2 (`docs/coop/artifacts/delivery-rust-provider-join.v2.json`).
- **The macOS SDK 27 headers** at `/Library/Developer/CommandLineTools/SDKs/MacOSX27.sdk/usr/include`, and the pinned libc 0.2.189.

## What to review

`SCOPE.md` opens with the r2 changes table, one row per round-1 finding. Judge:
1. **Each round-1 finding is resolved:**
   - **RF-1:** `ScratchRoot` and every `ChildScratch` share an `Arc<RootState>` (the parent, the root, the held lock and the name), so dropping the root never releases what a live child or taken scratch relies on.
   - **RF-2:** staged creation with the lock taken before the `renameatx_np(RENAME_EXCL)` publication; a sweep that keeps a root whose lock it cannot open or take, holds the lock through removal, and re-verifies with `same_entry`. Can two sweepers, or a sweeper and a creator, still remove a live root or remove one twice?
   - **RF-3:** `reap_exact` retries `EINTR`, treats `ECHILD` as nothing to reap and returns other errors; `Drop` marks reaped only on success; `wait4` retries `EINTR`. Does the injected-`EINTR` seam go through the same match as real results?
   - **RF-4:** `kill_and_reap` (the group, then the root, then the exact reap) for the setup failure and `Drop`. If that cleanup fails after a setup failure, `LaunchError::SetupAbandoned` returns both errors.
   - **RF-5:** no `from(` remains in the test helper.
   - **NBO-1 and NBO-2:** the metadata, and the exact `CString` names in `list` and removal.
2. **No regression** in the round-1 surface: the closed classes, the constructors, `VerifiedLaunch`, the spawn attributes, pipes, `dlsym` `addchdir`, `RLIMIT_CORE`, the exit source, the reap-last rule, `proc_listpids`, and the unsupported build. Is every new or changed `unsafe` block sound, including `renameatx_np`, `flock`, `fstatat` in `same_entry`, and the `waitpid` loop?
3. **The tests.**
   - Do the five new tests establish their findings? `a_child_keeps_its_scratch_root_and_lock_after_the_root_is_dropped` retries its probe and sweep across other tests' fork-to-exec windows; is that sound, or could it mask a real release?
   - Do the 15 mutations (three new) each prove a rule?
4. **The lane.**
   - Attempt 2 (`evidence/d1a-checks-r2/`) is the lane of record. Attempt 1 (`evidence/d1a-checks-r2-attempt1/`) failed only the operability census, on the discarded cleanup result.
   - Check: the serial platform suite at base and candidate with equal failure sets and 20 new tests; Clippy; rustfmt; FW-01; the environment exceptions; the operability census (unchanged, LD-D1A-5); verify_design; and the census closure unchanged.
5. **Rules:** no new `from(`, `into(`, `pid(`, `line(` or `issue(` call, no new environment read, and no Linux claim.
6. **Inventory:** two new paths for an inventory successor.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `D1A-R2-RF-n` / `D1A-R2-NBO-n`.
