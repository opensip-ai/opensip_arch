# Review request: B3-B3A1-r1 (the D15 terms of the T2 census; M3-B unit B3-b, sub-unit B3-b3a1)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b3a1-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- Do not run the census tool with `--t2-cache` or `--held-out-blind`.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys or held trees.
- Never open a T2 held-out entry's store.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/security/discovery_census.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, which checks the vectors only and reads no T2 store;
  - importing `tools/security/discovery_member_model.py` read-only to try inputs.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b3a1-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 18195 bytes, SHA-256 `ffe3c284165b8a816450213a59797f8be3350aa8e1c1fc95b21e44d49fd9d92d`, 75 members. Rehash every member.
- **Bases:**
  - product main `e367d7f465d8d0a74819cad5010a58b8641e4c7a`, clean (B3-b2 complete, inventory v207, 170 contract successors);
  - architecture `ea65b4d5c6a481fde25974f48ef9588e2033898f`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b3a1`, detached at the product base. It holds the exact bytes `product-map.json` lists.

## Authority

- The B3-b plan r2:
  - §4.1 and §4.2;
  - amendment A2-3 step 4 (each charge in exactly one term, with placement and listing at n = 0);
  - amendment A5 (your `codex-b3b-plan-a5-r1`: B3-b3a1 is the bound; the bound is the ledger's).
- Law M3-B r9 item 12: the member observation's bound, its read-retry envelope, the caps and the margin rule.
- The bound B2-b4 census (its model, its closure discipline and its soundness controls).
- The accepted B3-b2 code on main: `git_tracking.rs`, `workspace_declarations.rs`, `workspace_observation.rs` and `workspace_discovery.rs`.

## What to review

`SCOPE.md` describes the unit and lead decisions LD-B3B3A1-1 to 7. Judge:
1. **Fidelity.** Does `discovery_member_model.py` mirror, charge by charge and in order:
   - the native observation;
   - item 6b;
   - the decision core's requests;
   - the composition's order?

   Is every native charge on those paths in exactly one term? Construct inputs where it might under-count.
2. **The closure and anchors.** Do the anchors pin every constant and formula the terms use? Is the closure extension complete for the terms' code?
3. **LD-B3B3A1-2, the read-retry envelope:** POSIX regular-file reads, uninterrupted, for the D15 terms, against the walker's one-byte envelope. Is it an acceptable explicit envelope under item 12, given that every D15 read is of a regular file opened no-follow, and the B2-b4 census already excludes interrupted retries? What would the one-byte envelope imply?
4. **LD-B3B3A1-3 and 4:** item 6b at its ceilings, the environment envelope, and the dearer branches.
5. **The repository rows and the equality projection.**
   - Is the full-ledger classification (and failing on it) right?
   - Is `evidence/b3b3a1-checks-r1/equality-projection.json`'s allowlist exactly the intended change?
6. **The validation:**
   - the measured-against-model control at three synthetic root spellings;
   - the measurement after item 6a;
   - the worst cases (including the exactly-4-MiB valid index);
   - their tightness;
   - the found under-count;
   - the five mutations.

   Is §4.2's validation met for the cases it names: a member, a shared path, exact roots, an excluded member, a nested repository inside a member, and boundaries?
7. **Evidence:**
   - 14 = 14 base failures and one new test;
   - Clippy and rustfmt;
   - the census `--check` over the T2 cache;
   - verify_design;
   - attempt 1's history.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B3A1-R1-RF-n` / `B3B3A1-R1-NBO-n`.
