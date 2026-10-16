# Review request: B3-B2A-r1 (the S3 walk and core with supplied D15 members; M3-B unit B3-b, sub-unit B3-b2a) and B3-b plan amendment A1

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2a-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds, the lane or the census tool.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry, store or overlay.
- Do not use other panes and do not delegate.
- **Permitted:**
  - read-only reading, hashing, JSON parsing and Git queries;
  - in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository <tree>`;
  - in the candidate worktree, `python3 -I -B tools/security/discovery_member_vectors.py --check --architecture /Users/sb/code/opensip-ai/opensip_arch --packages-root /Users/sb/code/opensip-ai/opensip`, which reads no filesystem tree.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2a-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 10932 bytes, SHA-256 `202a4c58ab99da1bc49126469cce50cbde793bb64f0c815c0b422579621a92a0`, 46 members. Rehash every member. The manifest includes the plan amendment `b3-b/PLAN-r2-A1.md`.
- **Bases.**
  - Product: the candidate's base is `25972e1` (168 contract successors, inventory v202).
  - Product main has since moved, by fast-forward, to `5b87728`. That is B3-b1's accepted code (`codex-b3b1-r3`), which touches only `git_tracking.rs` and its new test file, disjoint from this unit. Its inventory v203 is in review separately.
  - Architecture: `a97a12458c4d4a8ee3c9f7c86268c2ede78019d6`, which records B3-b1.
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2`, detached at `25972e1`. It holds the exact bytes `product-map.json` lists.

## Authority

- Law M3-B r9: item 22 (D15 members entered as ordinary directories, a member's own `opensip.json`), item 19's SX-1 (the `.opensip` anchor at each member root) and item 12 (the census) (`config-discovery-b/PROPOSAL-r9.md`).
- The B3-b plan r2 (`b3-b/PLAN-r2.md`; your `codex-b3b-plan-r2`), sections 3 and 4.2, and LD-B3B-4 and LD-B3B-7.
- B3-b0, the members-and-readers reference (contract successor 168): `b3-b-reference/reference/member_reader_reference.py`, at its bound bytes.

## What to review

**First, plan amendment A1** (`b3-b/PLAN-r2-A1.md`). It:
- splits B3-b2 into B3-b2a (walker and core with a supplied member set) and B3-b2b (the rest of section 3, unchanged);
- moves the census `CLOSURE` re-pin to the unit that changes a closure file, with section 4.2's equality projection for that change, leaving the cost-model extension in B3-b3a;
- states that the held-out margin is outstanding from B3-b2a until B3-b3b's single gated refresh.

Is A1 sound, and consistent with the plan's gates? Does it weaken any accepted obligation?

**Then the unit** (`b3-b2a-r1/SCOPE.md`, lead decisions LD-B3B2A-1 to 6):
1. **Fidelity to item 22 and SX-1** (`discovery_walk.rs`, `discovery_scan.rs`):
   - member roots reach the shared rule at the three sites;
   - a member root and its own `opensip.json` are not boundaries, in the listing and on the probe chain;
   - a member is not a nested repository, and is recorded in `memberRepositories`;
   - a member's own `opensip.json` goes to `memberConfigs`, unread;
   - nested repositories and projects inside a member stay boundaries;
   - unreadable anchors are classified with the members.

   Is there any change when the member set is empty, which is every production caller's case? Diff against the base.
2. **The vectors** (`tools/security/discovery_member_vectors.py`):
   - Do they faithfully run B3-b0's pass two at its bound bytes?
   - Is LD-B3B2A-3 correct? It restores each member's own VCS evidence and root `opensip.json` to the expected population, because the native walk observes both before entering.
   - Are the scan cases (LD-B3B2A-6) a sound way to cover the unreadable-ACL path a scratch tree cannot hold?
   - Do the twelve walk cases and four scan cases cover item 22's behaviours?
3. **The census.**
   - Is the closure re-pin exact?
   - `evidence/b3b2a-checks-r1/equality-projection.json`: does it show that the only changes are the two closure rows, the ten held-out rows' standing and composed result, and `heldOutMargin`, with every lead-readable row and every census-vector prediction unchanged?
   - Is the held-out standing honestly reported as outstanding?
4. **Controls and evidence** (`evidence/b3b2a-checks-r1/`):
   - the security suite, with 14 equal pre-existing failures and two new passing tests;
   - Clippy, rustfmt, every discovery vector check, FW-01, the walk-storage and census-tool controls, and the census `--check`;
   - ten mutations, each in a closure file. The gate skips the closure-pin test, so each must be caught behaviourally. Are they meaningful?
   - The SCOPE also records a pre-submission lane, not archived, in which two mutations survived until the probe-chain and scan cases were added.

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "planAmendmentA1": "ACCEPT" | "REQUIRED-FINDINGS", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2A-R1-RF-n` / `B3B2A-R1-NBO-n`.
