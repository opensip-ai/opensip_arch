# Review request: B3-B2B2A-r1 (the item-6b session and the handoff binding; M3-B unit B3-b, sub-unit B3-b2b2a)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b2b2a-r1/`).

## Boundaries

- Do not edit either repository, the worktree or the control files.
- Do not run Cargo, rustc, tests, builds, the lane or the census tool.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry, store or overlay.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing, JSON parsing and Git queries; in the candidate worktree, `python3 -I -B tools/check_operability.py source --repository <tree>`.

## Subject

- **Manifest:** `docs/implementation/m3/config-discovery-b/b3-b2b2a-r1-subject.json` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 9841 bytes, SHA-256 `366efb40dbd2071a87c096d111e41635ee4aae20c6fd746647bade929a0f0c21`, 41 members. Rehash every member.
- **Bases:**
  - product main `46c0ebb3e88e4cfaa8d5a1021b3fdcccee2e63a8`, clean (B3-b2b1 bound, inventory v205);
  - architecture `cd0f3e52d554bbbdd093eb7d5bbcb8ad94163bfe` (A3 published).
- **The candidate worktree:** `/Users/sb/code/opensip-ai/opensip-b3b2b2a`, detached at the product base. It holds the exact bytes `product-map.json` lists.

## Authority

- The B3-b plan r2 with amendments A1 to A3 (A3-1's B3-b2b2a; your `codex-b3b-plan-a3-r1`).
- Law M3-B r9 item 21 (X2 r9 item 6b).
- Your B3-b1 reviews (`codex-b3b1-r1` to `r3`), especially B3B1-R2-RF-1.

## What to review

`b3-b2b2a-r1/SCOPE.md` describes the unit and lead decisions LD-B3B2B2A-1 to 3. Judge:
1. **The binding.**
   - Does `ChainIdentity` (one construction site, a process-wide never-reused counter, `ProjectChain` not `Clone`) with `NoRepository::retained` bind the proof to the retained object, as B3B1-R2-RF-1 requires, now that the chain and the observation are stored apart?
   - Can any caller obtain a proof for a chain item 6a did not observe?
   - Does `OperationHandoff::member_precondition` pair only the subject's own chain and tracking?
2. **Item 6a unchanged.** The identity is outside `TrackingObservation`'s equality by a manual `PartialEq`/`Eq`. Is `recheck_tracking`'s behaviour exactly unchanged at every call site? Are LD-B3B2B2A-1 and 2 sound?
3. **The session.** Does `MemberSession::begin`/`observe` keep `observe_members`' steps, order, charges and verdicts exactly, with the pass-level sources checked once? Does B3-b1's non-latching discipline hold?
4. **Census.** The `project_chain.rs` closure re-pin, and `evidence/b3b2b2a-checks-r1/equality-projection.json`, which must show changes only at `closure/2`.
5. **Controls and evidence** (`evidence/b3b2b2a-checks-r1/`):
   - the four new tests, and 14 = 14 base failures;
   - Clippy, the vector checks, the census and operability;
   - five mutations. Are they meaningful?

Write `review.json` as `{"verdict": "ACCEPT-UNIT" | "REQUIRED-FINDINGS", "subjectManifestSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3B2B2A-R1-RF-n` / `B3B2B2A-R1-NBO-n`.
