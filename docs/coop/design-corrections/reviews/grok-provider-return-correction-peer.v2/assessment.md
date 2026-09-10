Continuing the coauthor peer review into the v2 output directory: I’ll preserve the v1 bytes, copy and fix the probe, then finish the source58 review.I'll copy the probe into v2, tighten assertions so `ok` reflects author claims, and run the bounded checks.I'll tighten the v2 probe so `ok` and `author_claim_holds` are distinct, then run the bounded checkers.I'll truncate the oversized schema-error dump in the probe results, then write the peer md/json.**Verdict: `CORRECTIONS_REQUIRED`.** A typed wrapper-to-host result is the right *kind* of object, but these source58 contracts still do not make occupancy return executable against original native worker isolation.

All new artifacts are only under `/tmp/opensip-design-corrections/grok-provider-return-correction-peer.v2/output/`. v1 `independent-probe.py` is unchanged (`653c9571…`). Source58 hashes still match the 15-file manifest. No source edits, no pin seal.

### What is not executable
After closed-wire `FactBatch`, the one-shot worker is on the path to Complete/exit (`retainAfterTerminal: false`, `residentSession: false`, no TargetAttribution frame). Host then mints `fact2`. Occupancy is claimed as the second output of the **same** in-worker SubjectIdV1 encoding pass. There is no `build_provider_attribution_return`, no table schema/lifecycle, and no specified way for a wrapper *outside* the child to read that table. This review does not invent another transport.

`admit_provider_attribution_return` also only echoes caller `stageOrdinal` / `producerClosure` (stage 99 matching both sides **admits**; a kind=provider closure that is not the EnumerationPlan selected enumerator **admits**). Selected views are not an admit operand. Envelope `records.items` does not `$ref` selected V2 (`additionalProperties: true`). `origin=host-internal` **captures** `hostDerivedRefs`.

### What does hold (helper boundary, not owning admission)
C15 refuses contradictory first-party identity and does not skip unique inventory joins. Unknown sidecar keeps ephemeral. Missing envelope vs empty records, unknown-fact all-or-nothing refuse, and public `EVALUATION.INPUT_REFUSED` / `HOST.INVARIANT_VIOLATED` routes match the existing owner registry. No new D9 codes. Envelope is not a digest domain. Frozen24 V1 is untouched. Atom `_reconcile_attribution` / `_join_sidecar` signatures are unchanged for the separately pending query fix.

### Helper vs owning
Independently re-run: return checker **18/18** (`fullRun: false`), atoms **69/69** (synthetic maps, not compiler qualification), evaluator-faults **40** (bounded routes, LIVE D9 not discharged). Those are preconditions. They are not `close_run`, not worker execution, not suite integration. The new checker is not in the current suite runner. Execution-inputs / semantic-replay / query checkers were **not** re-run and are not reclaimed.

Five MUSTs, with selectors, operands, and remedies, are in `provider-return-correction-peer.md` and `.json`.
