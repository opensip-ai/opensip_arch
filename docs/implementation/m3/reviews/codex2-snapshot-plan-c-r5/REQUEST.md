CODEX2 review: M3-C r5, the sealed snapshot and Plan law. This is a **law and contract-soundness** review, round 5. Claude Opus 5.5 leads, and you are the single reviewer. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r5.

**Rules:**
- Read-only. No repository edits, commits, pushes or delegation.
- No product builds or test runs: a timing-sensitive crash-matrix run may be using this machine.
- Never touch the real home.
- Never read the 413 fixture.
- If you compute digests or arithmetic, use read-only scratch scripts under your review directory.

## Subject

The pins are in `hashes.txt`.
- **The subject:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md`, the r5 law. It is the subject of `subjectSha256`.
- **For diffing:** `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r4.md` (`bcf4baa1…`), the r4 bytes you reviewed.
- **Your r4 review:** `/tmp/opensip-implementation/reviews/codex2-snapshot-plan-c-r4/`.
- **The product:** `/Users/sb/code/opensip-ai/opensip` at main `30c5db1`, read-only.

r5 changes only what the "r5 changes" table at the top lists.

## What r5 changes

1. **C4-R1, by lead decision: the oversized shortcut is removed** (item 12, rule 7).
   - **To completion.** Every candidate is acquired to completion under its route's rules, the per-archive decoder counters (DS-2) and the acquisition bounds. It is admitted by its route, or rejected as a profile breach, before activation.
   - **Acquisition crossings** refuse as `DependencyAcquisitionBound` whatever the processing order.
   - **Materialization.** Admitted candidates are materialized whole, so Cargo decides activation from a lawful, complete tree. Rejected ones are never materialized, and if Cargo then fails for an absence, NE:1789-1791 governs.
   - **The protocol counters** are checked once, after activation and admission, over the admitted set. Only a proven overflow gives `DependencySetBound`.
   - **No special path** exists for a large single candidate. r4's rule is withdrawn.
   - **Controls.** C3-T6c's oversized cases become four variants each, for 8 GiB + 1 of content and for 1,000,001 files: valid or late-failing, active or inactive. They include a required late-failing package whose absence makes Cargo fail.
2. **C4-N1.**
   - Rule 6's end-region cap of 1,024 to 10,240 bytes is an explicit check of its own.
   - D1 is shown to be implied by rules 4 and 6, D2 and alignment. It is kept as a streaming guard, and its breach is reported as the rule it implies.
   - The D1-only control is withdrawn, and a 29,184-byte aligned empty stream tests the end-region cap.
3. **C4-N2.** The admitted set covers every route: DS-1 trees, DS-2 archives and DS-3 trees, each keeping its assurance level. CRATE-ARCHIVE-1 is DS-2 only. Tree candidates count toward the acquisition bounds, and a mixed-route control is added.
4. **C4-N3.** Acquisition runs in the canonical `(name, version, sourceId)` order, with a fixed field precedence: sources, then files, then content. The refusal's class is order-independent and its fields are deterministic. A two-crossing control is added.

## Decide

1. **C4-R1.** Does r5 remove every route by which a rejected or unvalidated prefix could become a set overflow or a manufactured activation? Is the materialization rule (admitted only, whole) lawful under NE:1785-1791? Do the C3-T6c variants discharge your examples?
2. **C4-N1 to C4-N3.** Are they adequately absorbed? In particular, is the D1 implication argument correct?
3. **Regressions.** Did any r5 edit contradict a decision you accepted in r1 to r4?

## Output

Write REVIEW.md and review.json. review.json needs:
- `"verdict"`: ACCEPT or REQUIRED-FINDINGS;
- `"requiredFindings"`: each with id, location, problem or claim, evidence and fix;
- `"nonBlockingObservations"`;
- `"subjectSha256"`: PROPOSAL.md's sha256.

This is a law review, not a `verify_design` unit. The contract successors (CRC-1, CR-1, NIJ-1, VCS-1, SX-1, S-B, S-R, T2-DEP) need `ACCEPT-DESIGN-UNIT` reviews of their own. X12d and the C code units are inventory units, reviewed with `ACCEPT-UNIT` and `inventoryCandidateAssessment`. Acceptance of this law still waits for its gate: M3-L and X12 r4 accepted. Do not commit.
