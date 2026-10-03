GROK2 review: the M3 analysis-quality plan, **r5**, a one-change amendment. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/grok2-analysis-quality-plan-r5. Read-only; do not commit.

**Subject:** `docs/implementation/m3/analysis-quality/PLAN.md`, 64603 bytes, sha256 `c8ceb480718c41a803c83fc170296ed89d1dde59885d61f6589d9a1eed2105d8`. **Previous:** `docs/implementation/m3/analysis-quality/PLAN-r4.md` (`52895ef2…`), the accepted r4. Diff the two.

r5 changes only:
- the title;
- the r5 changes section;
- §5.1's peak-memory rule.

It drops the acceptance note. The rule is a lead decision: on Linux, peak memory is the workload cgroup's `memory.peak`, labelled as charged memory, not RSS. It replaces r4's larger-of-two rule. Per-process `wait4` maxima are informational only, macOS stays `incomplete`, and whether `memory.peak` counts as AQ:268-272's "peak RSS bytes" for qualification goes to D13. The background is M3-Q0 r2–r8: per-process attribution never closed. The CODEX2 r8 review is in `docs/implementation/m3/reviews/codex2-harness-q0-r8/`.

## Decide

1. Facts: are the cited lines accurate? Does r5 contradict any accepted contract or gate, in particular AQ §3, QG items[12] or LQM, in a way it fails to route to a successor?
2. Method: is `memory.peak` a sound, conservative budget figure for exploratory measurement? Are its limits stated honestly?
3. Does r5 change anything else?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256".
