I’ll recheck only the v3 MUST/SHOULD items against the current root tooling and write the v4 confirmation (or remaining issues) into the exclusive recheck directory.**CORRECTIONS_CONFIRMED** for the v3 tooling scope only. Not design ACCEPT, not blind ACCEPT, not application.

| v3 finding | Status |
|---|---|
| MUST-1 absent live resume guides | Closed: `liveState` `absent\|exactDigest`, nullable `liveSha256`, not staged; `verify-applied.py` checks named paths and absent state. No blanket `reviews/` skip. |
| MUST-2 eval 30 copied from R12 | Closed: per-id `evaluationResidualDispositions`; binder uses accepted-snapshot inventory (30) and refuses a dropped row. Independent review ids match. |
| SHOULD-1 evaluator3 8400 | Closed: outer budget **8700** vs 14×600. |

Disposable probes **19/19** (`recheck-probes.json`). Root `coauthor-v3-correction-checks.json` still records 30 rows + dropped-row refusal. Draft 17 `beforeSha256` still match live.

Still outside this verdict: blind10 not accepted; no bind/assemble/activation; final application review must still grade every row.

Written only to `/tmp/opensip-design-corrections/grok-application-successor-recheck.v4/review.md` and `review.json`.
