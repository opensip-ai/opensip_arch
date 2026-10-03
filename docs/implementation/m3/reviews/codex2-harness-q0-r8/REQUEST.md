CODEX2 review: M3-Q0, **r8**. Verdict wanted: **ACCEPT** or **REQUIRED-FINDINGS**.

Write only under /tmp/opensip-implementation/reviews/codex2-harness-q0-r8. Read-only; do not commit.

**Subjects:**
- `docs/implementation/m3/harness/DESIGN.md` (r8), 120918 bytes, sha256 `c958fdabce364316773b7238a98a6b2de118355f95f65872bd0c8e3a6dba89a8`;
- the schema (r8), sha256 `cc6f3cb842b65fc1b7b2802a1769ade3d712e593578ee2dcfae4b17753b57ea4`.

**Previous:** `docs/implementation/m3/harness/DESIGN-r7.md` (`c72f71ba…`). r7 was never sent to you. It answered your C2-Q0-R6-01 with post-S per-CPU probes, but recommended replacing the event-channel mechanism.

**Lead decision (QD-30, recorded with its rejected alternatives).** Linux RSS collection is now ptrace exit-stop collection: SEIZE with fork, vfork, clone, exec and exit tracing; EXITKILL; and a TRACESECCOMP filter that stops only on execve and execveat. VmHWM is read at each thread's exit stop, which gives a structural completeness proof in place of event channels, fences and per-CPU loss proofs.

The rejected alternatives are:
- keeping r7's mechanism;
- concurrent-sum-only budgeting, which needs an AQP/LQM successor.

QD-31 preregisters the tracing-overhead rule: if overhead is 1% or less, collection is combined with the timed runs; above that, RSS is taken in a separate traced batch, joined by `rssBatchId`.

## Decide

1. Is the ptrace mechanism sound and complete? Check:
   - attachment before a descendant runs;
   - exec and tgid takeover;
   - group-stop and signal reinjection;
   - the early-exiting leader case, read from the exiting thread;
   - the pre-exec image read through the seccomp stop;
   - the Yama handling;
   - tracer death and failure.
2. Does it interact safely with O7 confinement and with the timing measurements?
3. Is your C2-Q0-R6-01 moot under r8? Are the earlier findings still respected (the batch joins, per-quantity nulling, the host join)?
4. Is anything else wrong?

Write REVIEW.md and review.json. review.json needs:
- "verdict";
- "requiredFindings";
- "nonBlockingObservations";
- "subjectSha256": DESIGN.md's sha.
