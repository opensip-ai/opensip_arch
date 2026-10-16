# Review request (round 2): B3-b plan r2, amendment A2 (B3-b2b as a pure decision core, then its native observation and composition)

Read and follow this request exactly. Write ONLY `REVIEW.md` and `review.json` in this directory (`/tmp/opensip-implementation/reviews/codex-b3b-plan-a2-r2/`).

## Boundaries

- Do not edit either repository or the control files.
- Do not run Cargo, rustc, tests, builds or the lane.
- No network.
- Do not read the private 413 fixture, the installation directory, signing keys, held trees or any T2 held-out entry.
- Do not use other panes and do not delegate.
- **Permitted:** read-only reading, hashing and Git queries.

## Subject

- **The amendment:** `docs/implementation/m3/config-discovery-b/b3-b/PLAN-r2-A2.md` in `/Users/sb/code/opensip-ai/opensip_arch` (uncommitted): 11194 bytes, SHA-256 `98c5cff08b8e9554fec5ff3f0a9e44dc66c849ff4e03a7e36d57f039ba1829f1`.
- **Bases:**
  - architecture `1f3f2b1ea4d019a1f24980f05cb2d2ef2501d766`;
  - product main `03876532b54d8327db96091fababb1fd994a83d2` (B3-b2a bound, inventory v204).

## Authority

- The B3-b plan r2 (`b3-b/PLAN-r2.md`; your `codex-b3b-plan-r2`), as amended by A1 (`b3-b/PLAN-r2-A1.md`; your `codex-b3b2a-r1`).
- Law M3-B r9 items 19 to 24 (`config-discovery-b/PROPOSAL-r9.md`).
- B3-b0, the reference (`b3-b-reference/`, contract successor 168), and its checker.
- B3-b1 as bound: `crates/security/src/custody/git_tracking.rs` on product main (`RootObservation`, `NoRepository`). Its review history is `codex-b3b1-r1` to `r3`.
- The operation handoff as built: `crates/security/src/custody/operation_handoff.rs` (the subject) and `first_registration.rs` (`observe_tracking_on_gate`, `RegisteredProject`).

## Round 2

Your `codex-b3b-plan-a2-r1` (`/tmp/opensip-implementation/reviews/codex-b3b-plan-a2-r1/review.json`) raised B3BA2-R1-RF-1 (TOML resource differences), RF-2 (forbidden-access assertions) and NBO-1 (disjoint reader and member terms). A2-4's table resolves them:
- every `parse_toml` error, resource bounds included, is the existing `parse` disposition (the G2 precedent), with labelled TOML differential controls and JSON alignment controls;
- the vectors carry the reference's lookup and read records and each case's `notRead` and `notObserved` lists, with subset and forbidden-path assertions and a forbidden-access mutation;
- A2-3 step 4 assigns each native charge to exactly one term.

**Judge first** whether each is resolved. The lead probed `tomllib` 3.14: it reads a 128-deep array and a 1,100,000-element array within 4 MiB, and raises `RecursionError` at about 1,000 levels. Then re-check the questions below.

## What to review

1. **Does A2 keep every obligation of plan section 3,** as A1 left it to B3-b2b? Each must land in B3-b2b1 or B3-b2b2. Is anything weakened? Consider especially:
   - the T2 link-map controls (a) and (b);
   - the joint sweep;
   - item 24's rows;
   - NBO-1's seam.
2. **The pure core.**
   - Is `WorkspaceObservation` a faithful and sufficient narrowing of B3-b0's access paths? The reference consults `_entry`, `_bytes`, `_markers`, the listings and `memberObservations`.
   - Is the two-phase split around branch A's trial walk faithful to B3-b0's SLM-first order (r2, B3B0REF-R1-RF-2)?
   - Is reusing B3-b0's own checker cases, without inventing any, adequate vector coverage?
3. **The parsers.** Cargo uses `parse_toml`, as B2-c1 did. npm uses `opensip_identity::parse_json` as the counterpart of the foundation's `canonical.parse` that B3-b0 uses. Are there semantic differences the vectors must expose?
4. **The NoRepository binding across the handoff.** A2 recommends a process-unique chain identity that item 6a records and the proof constructor compares. It rejects an unfenced second item-6a pass.
   - Does the recommended identity satisfy your B3B1-R2-RF-1 requirement (bound to the retained object, not to labels) once the observation and the chain are stored apart?
   - Is the rejected alternative rightly rejected?
5. **Census and bound consequences.** B3-b2b2 changes `project_chain.rs`, a closure file, which A1-2 re-pins. The member term now also covers the native reader and placement observation. Are these consequences stated correctly?

Write `review.json` as `{"verdict": "ACCEPT" | "REQUIRED-FINDINGS", "subjectSha256": "<sha>", "requiredFindings": [...], "nonBlockingObservations": [...]}`, with ids `B3BA2-R2-RF-n` / `B3BA2-R2-NBO-n`.
