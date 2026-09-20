# Clock observation latency / rounding (source note)

**Standing:** optional bounded source observation requested with 298. Not a 298 verdict, not an S4 implementation, not an OS qualification claim. Next root work remains typed-source plus retained-phase conditional S4 arithmetic.

---

## What already exists

`opensip_platform::observe_clock` (`crates/platform/src/clock.rs`) owns a **raw** OS sample: sleep-inclusive monotonic before wall, boot-id recheck, monotonic after. It refuses monotonic regression and boot-id change during the read. There is no fallback to process uptime, wall-only, or an invented boot identity. The type exposes `wall_unix_seconds`, `wall_nanoseconds`, `monotonic_before` / `monotonic_after`, `read_span`, and `boot_id`. The module comment states that **security** must enforce observation-latency bound and platform/namespace admission.

Pinned S4 (`security_lifecycle_model_v1.py` / `kernel201.py` SHA256 `df45c9c5…2299`; product-v1 `security-and-lifecycle.md` S4) already takes observation `(wall W, sleep-inclusive monotonic M, bootId B)` as a TCB **input**, not a measurement:

- payload/root future: issue time > W + 24 h → `PAYLOAD-NOT-ADMISSIBLE` (FC-FUTURE / `FUTURE_TOLERANCE_S`)
- unattested forward horizon: W > A + 90 d → `CLOCK-EXCURSION-FORWARD` (`UNATTESTED_FORWARD_HORIZON_S`)
- in-session: expected = `anchorWall + (M − anchorMono)`; > 24 h forward deviation is `CLOCK-EXCURSION-FORWARD` (`in-session`) unless a witness excuses it

Those are **admitted-time vs wall** rules after a sample is already in hand.

Private `crates/security/src/revocation.rs` fail-stop monitor uses `OBSERVATION_BOUND = 10s` on elapsed time **between successive samples** (`end.after − last.before`). That is counter-freshness stall detection, not an S4 bound on a single `observe_clock().read_span()`, and not a rounding/midpoint policy.

---

## What is missing

No pinned S4 / 215 D / 225 TIME-PRODUCER / 201 kernel source names:

1. a numeric bound on `ClockObservation.read_span()` (how long a single wall sample may take),
2. a rounding or truncation policy from `wall_nanoseconds` into S4's integer `W`,
3. a midpoint or endpoint policy from `(monotonic_before, monotonic_after)` into S4's integer `M`.

Do not treat the 10 s fail-stop stall bound, the 24 h future tolerance, or the 90 d horizon as that missing sample-latency law. They are different owners.

Until a typed-source S4 consumer states those three policies, the platform sample remains a raw observation and security has **no specified** observation-latency/rounding/midpoint gate to apply.

---

## Verdicts

- [x] Platform already brackets the raw sample; S4 already owns future/horizon/in-session arithmetic over supplied W/M/B.
- [x] Observation-latency bound, nanos rounding, and monotonic midpoint for that sample are **not specified** in the pinned S4 sources.
- [ ] Not an invented numeric limit, not OS qualification, not 298 clock-view approval.
