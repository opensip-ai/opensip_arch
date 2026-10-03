CODEX2 review: M3-Q0, **r11**, a two-finding round. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r11. Read-only; do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r11), 143572 bytes, sha256 `c003a06a8d5eaa0ceb414f9458dc52d1fc644b304cf3aa73db6ef00317fac933`;
- the schema (r11), sha256 `8769ed0c156d5496d9df6640eab29c1a219303768ede9c417b59dc638d4f6975`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r10.md` (`c926077c…`).

r11's table maps:
- **R10-01:** detach the inherited cgroup mounts (lazily, innermost first) inside the private mount namespace, then mount a fresh read-only cgroup2 view. The invariant is stated over the mounts that remain.
- **R10-02:** no-leaf rows may carry the batch-level reasons, settlement depends on whether a leaf exists, and a new `settlement-failed` reason.
- your four non-blocking items.

## Decide

1. Are both r10 findings resolved?
2. Did r11 introduce any error, or change anything beyond its table?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
