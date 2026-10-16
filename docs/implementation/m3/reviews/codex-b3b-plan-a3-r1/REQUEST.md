# Review request: B3-b plan r2, amendment A3 (B3-b2b2 in three steps)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b-plan-a3-r1/`).

## Boundaries

- Do not edit either repository or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing and Git queries.

## Subject

- **The amendment:** `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A3.md` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 6427 bytes, SHA-256 `3f5567a9ec75aea52cec2486c921e765c74abb22c2024ba45a9657002851980d`.
- **Bases:**
  - architecture `e8f6023cb90847a8d859fadd31e62d9884518765`;
  - product main `46c0ebb3e88e4cfaa8d5a1021b3fdcccee2e63a8` (B3-b2b1 bound, inventory v205).

## Authority

- The B3-b plan r2 (`b3-b/PLAN-r2.md`), as amended by A1 and A2 (your `codex-b3b2a-r1` and `codex-b3b-plan-a2-r2`), A2-1's B3-b2b2.
- Law M3-B r9 items 19 to 24.
- As built on product main:
  - B3-b1's `git_tracking.rs` (`RootObservation`, `NoRepository`, `observe_members`; your `codex-b3b1-r3`);
  - B3-b2b1's `custody/workspace_declarations.rs` (your `codex-b3b2b1-r2`);
  - `project_chain.rs`, `operation_handoff.rs` and `first_registration.rs`.

## What to review

1. **Completeness.** Does A3 keep every obligation of A2-1's B3-b2b2? Each must land in B3-b2b2a, b or c. Is anything weakened?
2. **B3-b2b2a's binding.** A process-unique, never-reused chain identity, recorded by item 6a but excluded from the observation's recheck equality, so item 6a is unchanged. `NoRepository::retained(chain, observation)` compares it, and `OperationHandoff::member_precondition()` builds the proof from the subject's own pair.
   - Does this satisfy your B3B1-R2-RF-1 requirement once the chain and the observation are stored apart?
   - Is excluding the identity from the recheck equality right? Every recheck site re-observes the same retained chain.
3. **The item-6b session.** It checks the pass-level sources once, then answers per member, for the core's per-candidate verdicts. `observe_members` stays as `begin` plus `observe`. Is that faithful to law item 21 and B3-b1's accepted behaviour?
4. **B3-b2b2b.** The native observation's discipline (accounted observations, ACL capture as the walker captures, same-object checks, non-latching verdicts), the composition, and the V3 completion. Are the closure re-pins and controls sufficient?
5. **B3-b2b2c.** Unchanged from plan r2 section 3 and NBO-1?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3BA3-R1-RF-n` / `B3BA3-R1-NBO-n`.
