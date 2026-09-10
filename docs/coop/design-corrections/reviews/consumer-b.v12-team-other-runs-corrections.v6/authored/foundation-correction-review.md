# Foundation trace correction (claimed stageCount)

**Verdict: `FOUNDATION_TRACE_READY_FOR_INDEPENDENT_RECHECK`**

Bounded existing-law correction from the P6 foundation-data report’s should-issue. Other foundation identity exhibits and preimages were not reminted. Not whole-consumer ACCEPT. Standalone traces are not full Runs. S-* origin standing is not inferred from booleans.

## Law

`protocol3-transitions.v1.json` `initialState.stageCount` is **0**. Only **Analyze** writes `stageCount` from the invocation. Unavailable and fault traces never send Analyze, so independent finals are `stageCount = 0`. Discriminating P3 ids and terminals still hold.

## Helper

`helper/protocol3.py` previously pre-seeded `run_trace(..., stage_count=1)` and defaulted an omitted Analyze field to 1. That invented a claimed final of 1 on traces that never reached Analyze.

Correction: start from published initialState. Only an Analyze frame writes `stageCount` from the event field.

## Command (exit 0)

Did **not** run `foundation_reconstruct.py` (that would remint unrelated identity exhibits).

```bash
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-team-other-runs-corrections.v6/output/scripts/replay_foundation_traces.py
```

Failed exhibits preserved under `preserved-failures/v6-pre-peer-four-runs-and-traces/foundation/traces/`. Record: `foundation-trace-correction-record.json`.

## Claimed finals vs law

| Trace | Analyze? | Old claimed | New claimed | Lawful |
|---|---|---|---|---|
| unavailable | no | 1 | **0** | 0 |
| fault | no | 1 | **0** | 0 |
| complete | yes (1) | 1 | 1 | 1 |
| cancel | yes (1) | 1 | 1 | 1 |
| terminal | yes (1) | 1 | 1 | 1 |

Unmatched OpenUniverse remains P3-34 FAULT with `sourceBytesSent=false`. `output/traces/` (workflow copy) was frozen and not rewritten. Eighteen other foundation artifacts: freeze **0 mismatches**.
