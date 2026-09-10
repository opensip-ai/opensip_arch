# Foundation trace recheck

**Verdict: `TRACE_DATA_ADMITS`**

Same-origin bounded successor recheck of original phase-3 standalone traces. Not a full Run, not whole-consumer ACCEPT. Unchanged non-trace foundation data keeps only its previous scoped standing.

## Hashes

Data manifest SHA-256 `ffe67281dd8fc681310797d9f3c79f9e7463d58921da6e36e4edda01e858414c` matches. All seven listed files match declared SHA-256 and byte length. Original kit manifest remains `ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8`.

Successor-changed vs prior review:

| File | Prior SHA-256 | This SHA-256 | Change |
|---|---|---|---|
| unavailable.json | `b190f4d4…40463` | `6e288447…f23c0` | claimed `final.stageCount` 1 → 0 |
| fault.json | `2d244e03…a7821` | `f2d79f2f…9c723` | claimed `final.stageCount` 1 → 0 |
| identity-before-source.json | `df990cfe…2511f3` | `c3825476…02381` | added `finalStageCount: 0` on the no-identity OpenUniverse case |

Byte-identical to prior: complete, cancel, terminal, executed-vs-host.

## Reproduction

```text
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/consumer-b.v12-kit-foundation-trace-recheck.v1/output/trace_recheck.py
```

Owner: `docs/coop/design-corrections/native/protocol3-transitions.v1.json`. Identity tokens from native-evidence §9.1. Replay starts from published `initialState`. `stateUpdates` apply only after a successful row match. Claimed finals are comparison targets, not oracles.

## Prior finding disposition

**`FD-SHOULD-TRACE-STAGECOUNT-WITHOUT-ANALYZE` is closed as an existing-law correction, not a missing-law repair.**

Published law: `initialState.stageCount = 0`; the only `stateUpdates` writer is Analyze (`stageCount = the invocation's stage count`). Unavailable, fault, and OpenUniverse-without-identity never send Analyze, so independent `stageCount` is 0.

The prior exhibits claimed `1`. These successor exhibits claim `0`. Independent replay now matches every claimed final field on those paths. No kit recipe was missing or contradictory.

## Five original kinds — actual finals

Every per-event `traceId`, `phaseAfter`, `identityNegotiated`, `sourceBytesSent`, and `terminalKind` independently matches. Every published `initialState` field in `final` independently matches.

| Kind | ID | Analyze? | Independent final | All final fields match |
|---|---|---|---|---|
| complete | R-TRACE-COMPLETE | yes | DONE, terminal complete, stageCount 1, stageIndex 1, stagesCompleted 1, sourceBytesSent true | yes |
| unavailable | R-TRACE-UNAVAILABLE | no | DONE, terminal unavailable, stageCount 0, stageIndex 0, stagesCompleted 0, sourceBytesSent true | yes |
| cancel | R-TRACE-CANCEL | yes | DONE, terminal cancelled, stageCount 1, stageIndex 0, stagesCompleted 0, sourceBytesSent true | yes |
| fault | R-TRACE-FAULT | no | FAULT, terminal null, stageCount 0, sourceBytesSent false | yes |
| terminal | R-TRACE-TERMINAL | yes | FAULT via `post-terminal-frame`, terminalKind remains complete, stageCount 1 | yes |

Cancel still has `stageCount=1` because Analyze ran (`stageCount` taken from that event) and Cancel occurred before CoverageV3, so `stageIndex` and `stagesCompleted` stay 0. That is the published table, not the prior defect.

## Discriminatory cases

**Identity before source (R-TRACE-IDENTITY-BEFORE-SOURCE):** HelloAck with the four identity tokens sets `identityNegotiated=true` and `sourceBytesSent=false`. OpenUniverse then sets `sourceBytesSent=true` (P3-03). HelloAck without identity tokens leaves `identityNegotiated=false`; OpenUniverse does not match P3-03, so P3-34 FAULT and `sourceBytesSent` stays false (updates are not applied on no-match). Independent `stageCount=0`.

**Executed vs host (R-TRACE-EXECUTED-VS-HOST):** every step is labeled executed; frame payload schema, OS pipes, and process spawn remain future-host assumptions.

## Mapping

| ID | Result |
|---|---|
| R-TRACE-COMPLETE | executed-pass |
| R-TRACE-UNAVAILABLE | executed-pass |
| R-TRACE-CANCEL | executed-pass |
| R-TRACE-FAULT | executed-pass |
| R-TRACE-IDENTITY-BEFORE-SOURCE | executed-pass |
| R-TRACE-TERMINAL | executed-pass |
| R-TRACE-EXECUTED-VS-HOST | executed-pass |

Existing-law misses: none remaining on these traces. Missing/contradictory norm: none.

## Limitations

- Frame payload schema, OS pipes, and native process spawn are future-host assumptions.
- Standalone traces were not upgraded to complete Runs.
- Non-trace foundation exhibits were not re-run; previous `FOUNDATION_DATA_ADMITS` standing for that scoped set is unchanged.
- S-\* author-process custody remains external-root-custody-required from the prior review.
- This is not whole-consumer ACCEPT.
