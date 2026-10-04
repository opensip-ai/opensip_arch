CODEX2 review: M3-C r4, the sealed snapshot and Plan law. This is a **law and contract-soundness** review, round 4. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r4.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests or arithmetic, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, the r4 law. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r3.md` (`2e455c70…`), the r3 bytes you reviewed.
- **Your r3 review:** `/tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r3/`, including its frozen inputs (`m3-b-live-pinned.md`, `x12-r4-pinned.md`, `x2-r9-pinned.md`).
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `30c5db1`, read-only.

r4 changes only what the "r4 changes" table at the top lists. Everything else is r3's bytes.

## What r4 changes

1. **C3-R1, carrier presence (item 1, rule 2).**
   - **The handoff.** B1 hands C1 the carrier **observation**: `absent`, or `present` with digest D. X2's types are unchanged, and no bytes are handed over.
   - **The join.** Sealing admits exactly two cases: present with exactly one regular-file `opensip.json` row of digest D, or absent with no such entry in the root's listing.
   - **The refusals.** `SnapshotCarrierChanged`, with no retry, for `digest`, `present-absent`, `absent-present`, `type` and `excluded` (covered by `ignorePaths`; cross-law finding X-7 for B1).
   - **Outside the join:** the local carrier and members' `opensip.json`.
   - **Controls:** C1-T26.
2. **C3-R2, counter population (item 12, rule 7, and DS-6's steps).**
   - **Protocol counters** count only the **final admitted set**: activated, non-path, in-profile packages (NEM:1832-1845, :1870-1883). They are checked once, after activation and admission, and before the descriptor, wrapper or transport. Only a proven overflow refuses as `DependencySetBound`.
   - **Pre-activation acquisition bounds** cover the candidates. Their owner is C3a, at 16,384 archives, 4,000,000 files and 32 GiB, with their own refusal `DependencyAcquisitionBound`. A single oversized candidate is decided after activation: if it is activated, the set provably overflows; if not, it is dropped with an omission.
   - **Decoder counters** D1 to D4 are per archive and are the only bounds during decoding, beside the acquisition bounds.
   - **Controls:** C3-T6c (inactive excess, late rejection, oversized candidates, and an acquisition crossing that does not depend on order).
3. **Non-blocking items:**
   - **C3-N1:** the ledger byte cap is derived from C1a's pricing recipe, no longer the 2^33 figure. The census adds bytes, and C1-T27 is added.
   - **C3-N2:** D3 is reworded, with its Cargo margin as R6 evidence. There is a genuine D1-only crossing control, the 16,386-byte `L` case is labelled D2, and C3-T6 is qualified.
   - **C3-N3:** capture origin is an operational side record. Identity rows stay `{path, sha256, bytes}`, and the read rules are narrowed to source reads.

## Decide

1. **C3-R1.** Is the carrier join now two-sided and total? Check every presence, type and digest transition, the `ignorePaths` interaction, and that no bytes cross from X2.
2. **C3-R2.**
   - Are the protocol counters now computed only over the final admitted set, and checked at the right point?
   - Are the acquisition bounds properly owned, quantified and disposed of, and distinct from `DependencySetBound`?
   - Is the oversized-candidate rule sound?
   - Do C3-T6c's cases discharge your counterexamples?
3. **C3-N1 to C3-N3.** Are they adequately absorbed?
4. **Regressions.** Did any r4 edit contradict a decision you accepted in r1 to r3?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The contract successors (CRC-1, CR-1, NIJ-1, VCS-1, SX-1, S-B, S-R, T2-DEP) need `ACCEPT-DESIGN-UNIT` reviews of their own. X12d and the C code units are inventory units, reviewed with `ACCEPT-UNIT` and `inventoryCandidateAssessment`. Acceptance of this law still waits for its gate: M3-L and X12 r4 accepted. Do not commit.
