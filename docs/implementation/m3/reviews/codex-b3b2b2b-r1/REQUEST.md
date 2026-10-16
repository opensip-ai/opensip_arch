# Review request: B3-B2B2B-r1 (the native workspace observation and the D15 discovery composition; M3-B unit B3-b, sub-unit B3-b2b2b)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b2b-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds, the lane or the census tool.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry, store or overlay.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository <tree>`;
  - in the candidate worktree, `python3 -I -B tools/security/workspace_discovery_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, which reads no filesystem tree.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2b2b-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 12793 bytes, SHA-256 `68e817efdd5c8f960279913e10653685632d2617e76f663ca1427dc365e5de13`, 53 members. Rehash every member.
- **Bases:**
  - product main `d47f9892d5709a1e108c4ecf9a9f60ed7aae12b2`, clean (B3-b2b2a bound, inventory v205);
  - architecture `5c581b5c5a4e22ff3fa28d5e9f522df92a27c4a0`.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2b2b`, detached at the product base. It holds the exact bytes `product-map.json` lists.

## Authority

- The B3-b plan r2 with amendments A1 to A3 (A3-1's B3-b2b2b; your `codex-b3b-plan-a3-r1`), and plan r2 section 3.
- Law M3-B r9 items 19 to 24.
- B3-b0 (`b3-b-reference/`) at its bound bytes.
- As bound on main:
  - B3-b2a's walk and core;
  - B3-b2b1's decision core;
  - B3-b2b2a's binding and session.

## What to review

`b3-b2b2b-r1/SCOPE.md` describes the unit and lead decisions LD-B3B2B2B-1 to 9. Judge:
1. **The native observation** (`workspace_observation.rs`):
   - no-follow opens from W through the reused stack;
   - accounted observations, memoized as one object per path;
   - ACL capture exactly where the metadata-only judgment passes (LD-3);
   - non-latching captures and reads, and same-object checks;
   - positive marker lookups, listings through the walker's `ListingConversion`, and bounded reads;
   - the lazily begun item-6b session.

   Is anything observed that B3-b0 would not observe? Does any ordinary refusal latch the ledger?
2. **The composition** (`workspace_discovery.rs`):
   - phase one, then the trial walk, then phase two;
   - the accepted trial as the final walk (LD-4);
   - a member-rule refusal walking without members (LD-5);
   - the D9 branches;
   - the complete `DiscoveryResultV3` and its serializer;
   - the links.

   Is it faithful to B3-b0's `discover`?
3. **LD-B3B2B2B-1:** the pending provenance kept as the core's internal partial, with the composition's `DiscoveryResultV3` as the only emittable record. Does this satisfy plan r2 section 3's and A3's "the pending shape is removed", or must the type itself be removed?
4. **LD-B3B2B2B-2:** one observation per phase. Is the cross-phase consistency argument sound?
5. **The vectors and controls:**
   - Are the 19 composition cases, built as real scratch trees with `git init` members and compared record for record with B3-b0, adequate?
   - Does the access control (the core's requests within B3-b0's record, and the native operations within the requests' paths) meet A3?
   - Are the two mutations retired as equivalent rightly retired?
6. **The census and scenario.**
   - The `discovery_walk.rs` and `custody.rs` re-pins. `evidence/b3b2b2b-checks-r1/equality-projection.json` must show changes only at `closure/0` and `closure/6`.
   - The scenario path's use of the operation's precondition, and its `MemberInputs` (LD-9).
   - The host's `discovery_flag_tests` pass.
7. **Evidence** (`evidence/b3b2b2b-checks-r1/`):
   - 14 = 14 base failures and one new test;
   - Clippy with and without `scenario-fixtures`;
   - every vector check, the census and operability;
   - eleven mutations.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2B2B-R1-RF-n` / `B3B2B2B-R1-NBO-n`.
