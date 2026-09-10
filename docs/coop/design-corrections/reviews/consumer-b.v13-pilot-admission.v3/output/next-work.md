# Continuation after consumer-b.v13-pilot-admission.v3

Same origin `consumer-b.v13`. Original 123/8/3 + 8 standing rules + 3 `F-*` unchanged. `reconstructionAccepted` stays false. Root admission stays unobserved.

This directory completed the **condition-level** TS one-pilot-first admission prerequisite: required occurrences minus executed traces is empty. Keyword-only complete claims from v2 are retracted.

## Established here

- Condition inventory from selected kit tables without a container whitelist (`condition-inventory.json`).
- Required `(condition,instance,field)` from kit × this TS graph (`required-occurrences.json`).
- Traces emitted at comparison/rejoin (`executed-condition-trace.json`).
- `coverage-difference.open` empty (`coverage-difference.json`).
- `by-domain` sibling dispatch and `snapshot-path` inventory join implemented from kit selectors.
- Unit-boundary per-entry negatives for those new variants (`inventory/negatives-v3.json`).
- Full original TS schema/closure/native/Plan/source/evidence/proof/seal/Run path and fresh-process replay of exact export `runs/ts.store.json` SHA-256 `a2531c0ebd7e020a6167176e4dfc5400b41f0500718a920787cd2ab0d567eaa6`.

## Do not promote

Rust, rust-partial, syntax-code, syntax-data, graph query, workflow/envelope/vector collections, copied `requirement-status.json` flags, D9 host-invariant successor, `F-*`. Isolated helper negatives are not the original fully reminted semantic-negative requirement.

## Next

1. Root admits these TS frames (unobserved here).
2. Apply the same **condition-level** inventory + occurrence bind + comparison-site trace + coverage-difference method to one remaining complete Run (rust), loading rust domainSet rows rather than copying TS-only checks.
3. Then syntax Runs, then query/workflow over **this** export.
4. Whole-task verdict only after accept-blocking IDs are independently executed. Phase 11 must refuse ACCEPT if any accept-blocking ID is unexecuted.

## Commands

```
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v3/output/derive_conditions.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v3/output/run_condition_trace.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v3/output/pilot_ts_rebuild.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v3/output/pilot_ts_fresh_replay.py
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v3/output/run_negatives_v3.py
```
