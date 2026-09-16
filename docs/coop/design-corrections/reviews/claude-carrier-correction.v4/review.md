Done. Source25 pristine (12869/12869), root's inputs unmodified, v3 untouched.

## Both schedules were real defects in my v1 algorithm

I accept both diagnoses. v1 read tail, witness and floor once each and treated the tuple as coherent — it isn't.

**Race 1.** With receipt `k=9`, tail `t=10`, and a lawful concurrent append landing 11 plus witness `COMMITTED 11` before the reader's witness read, v1 hits `COMMITTED n > tail` and emits a quarantine diagnosis for an ordinary later append. Fixed by **bracketed capture**: witness-before, floor-before, journal snapshot, witness-after, floor-after, with byte stability per bracket. An anchor is usable only if its own bracket was stable, and an owner quarantine condition is reportable only under five stated conditions (both brackets stable, two journal snapshots agreeing on tail *seq and digest*, closed witness shape validated first, carrier naming matched). Otherwise → `unavailable-busy`. I state the stability argument as an **assumption about writer monotonicity, not a proof**.

**Race 2.** Fixed by removing the liveness probe entirely. I traced owners first: identity §2 **already** requires ExecutionId "reserved with uniqueness checked in the corresponding operational ledger before use", so the admitted phase is existing law. What's missing is durable terminality for a non-committing attempt. So `AttemptCustodyV1` adds a monotone phase to that *existing* reservation — settle ordered after the receipt write, read in the **same** snapshot. The crash case stays `unknown-attempt-open` forever, and the authorized settle-sweep is **named and not discharged**.

**Covered by schedules, not tuples:** 78,653 enumerated schedules, 14 configs, 0 violations, 7/7 coverage assertions — including that skew actually suppressed a corruption claim and that all five quiescent corrupt carriers are *still* diagnosable.

## Owners now selected, not just linked

Two candidate25 files patched (`identity-and-evidence.md` +35/−1, `security-and-lifecycle.md` +54/−0), both before-hashes asserted against the frozen manifest. No historical file touched — and since `WA-13` occurs **only** in immutable v8, the third generation-closure cause is stated in the current owner. F32's typed route is asserted preserved verbatim, including its move to `retention_tests.rs`. Cases renumbered F38–F49, no `F39b`. New S12 rows use only registered errorCodes and detail codes; the one carrier-quarantine detail code is **left undecided** with both options costed, since reusing `MIGRATION.CORRUPT` would put two remedies behind one code.

PS05 adopted verbatim: 132 schedules, 0 violations, all four bit states, permit single-use, fetch-OR idempotent, CAS-from-2 fails. Required delivery after a successful commit **can** proceed as a separate SHARED-READ phase drawing nothing from the closed session; for state 3 I selected the conservative reading (no delivery phase; existing `DELIVERY.REQUIRED_FAILED`) and flagged the alternative.

## Three things I'd want you to read skeptically

**My overclaim is withdrawn with a measurement.** C8: the frozen carrier admits **8 of 9** schema-3 types; incompatible cases are exactly `SEAL` and the three alias-only platform ids. And I separated attribution — the weak-chain limitation was already in your prompt and followup §4.2; only the two-frozen-document wording contradiction is mine.

**One negative-control drift is undetected and I did not hide it.** A2 keeps the brackets but drops the two-agreeing-tails requirement, and produces no violation — because in a lawful append the tail only moves with the witness. **My controls do not justify keeping that clause.** I retained it as defence in depth; you may drop it.

**My own validator was weak twice more.** Two drifts initially detected only by crashing it, and two drifts I wrote were badly constructed. Both fixed — clean failures now, and sandboxes carry the model reports.

`REPORT.md` §6 lists 11 remaining actual design gaps, kept separate from §7 unperformed qualification (no real processes — C6 interleaves a model, not two OS processes; no Rust compiled) and §8 already-selected honest limits.
