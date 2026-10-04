Codex review: S-OP-2, **r6**, a one-finding round. Verdict wanted: **ACCEPT-DESIGN-UNIT** (for the contract successor) or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex-s-op-2-r6. Read-only; do not commit.

**Subject:** `docs/implementation/m3/operability/s-op-2/PROPOSAL.md`, 130001 bytes, sha256 `ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d`. **Previous:** `docs/implementation/m3/operability/s-op-2/PROPOSAL-r5.md` (`a75afe9c…`), your r5 subject. Diff the two. r6 changes only:
- your SOP2-R5-01: item 13c's common **Objects** rule is restored, saying that writers use the listed key order, readers accept any order, and composites have exactly their listed form's keys, with no extra, missing or duplicate key;
- a C-4 key-order case: a permuted composite is admitted and re-encoded canonically, and an extra, missing or duplicate key is refused;
- the r6 changes section.

## Decide

1. Is SOP2-R5-01 resolved?
2. Does r6 change anything else?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256".
