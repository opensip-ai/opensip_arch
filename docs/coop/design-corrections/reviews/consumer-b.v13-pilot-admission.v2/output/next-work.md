# Continuation after consumer-b.v13-pilot-admission.v2

Same origin `consumer-b.v13`. Original 123/8/3 unchanged. This directory completed a **completeness audit** of the TS pilot-law-map and the TS one-pilot-first graph. `reconstructionAccepted` stays false.

## Established

- Unfiltered inventory of 462 `x-opensip-*` annotations + nested tables on selected schemas (`inventory/x-opensip-inventory.json`).
- Coverage reconciliation with 0 unmapped OPEN keywords (`inventory/coverage-reconciliation.json`).
- Executed registry checkers in `helpers/law_admit.py` wired into `close_run`.
- Isolated negatives 15/15 refuse (`inventory/negatives.json`).
- scopeCapabilityLaw correction of clones Coverage (v1 mixed-complete bytes preserved).
- `walk_order` now applies `x-opensip-order` under `allOf`/`if`/`then` even when `type` is omitted.
- Corrected TS export `runs/ts.store.json` SHA-256 `b62d7aedc9f257c56bd7a88b74739123172615e0b032af0af9ec94fd0fac62e5`, fresh replay equal proof C `86c3c464387ccadf15645ca78551fdcb1deed3457a9bc628ebe83ff1896d08fd`.

## Do not promote

Rust, rust-partial, syntax-code, syntax-data, graph query, workflow/envelope/vector collections, copied `requirement-status.json` flags, D9 host-invariant successor, `F-*`.

## Next

1. Root admits these TS frames (unobserved here).
2. Apply the same unfiltered inventory + checker + isolated-negative method to one remaining complete Run (rust), loading rust domainSet rows rather than copying TS-only checks.
3. Then syntax Runs, then query/workflow over **this** export.
4. Whole-task verdict only after accept-blocking IDs are independently executed.

## Commands

```
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v2/output/pilot_ts_rebuild.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v2/output/pilot_ts_fresh_replay.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v2/output/replay_export.py \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v2/output/runs/ts.store.json
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v2/output/run_negatives_v2.py
```
