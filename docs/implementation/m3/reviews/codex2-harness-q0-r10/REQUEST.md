CODEX2 review: M3-Q0, **r10**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r10. Read-only; do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r10), 133762 bytes, sha256 `c926077ce4403005360339d1dfab85240fb6506a3811d03d2a4c2a5d4717fee1`;
- the schema (r10), sha256 `6558bd39ce60f788b78c55c18e8925bee5e02823956b4a25e3f9f61e711e12a9`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r9.md` (`4db107c0…`). Your r9 review is in `docs/implementation/m3/reviews/codex2-harness-q0-r9/`. The quality plan is now accepted at r6, with the §5.1 wording you approved.

The r10 changes table maps R9-01 to 04 and your two non-blocking items. The main changes are:
- **QD-33, isolation:**
  - cgroup and mount namespaces;
  - a read-only cgroup v2 mount showing only the leaf, checked via `mountinfo`;
  - `close_range` with an fd audit;
  - a non-dumpable rule for other same-user processes;
  - continuous ownership of the leaf fd.
- **`cgroupLeaves[]`** leaf evidence.
- **QD-34, a charged-memory baseline with a basis digest.**
- **A child subreaper.**

## Decide

1. Is each r9 finding resolved?
2. Is the isolation argument sound? In particular, the non-dumpable rule and the mountinfo check.
3. Did r10 introduce any error?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
