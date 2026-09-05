# D-104 turn 2 — Record component-manifest-schemas.v11 as DR-103's accepted schema successor

> **Status:** DRAFT — under review.
> **Date:** 2026-08-14
> **Protocol:** D-000 new cycle, turn 2 of 3.
> **Decision type:** RULE-GOVERNED. Records independent dual
> ACCEPT-WITH-ADVISORIES (0 blockers, 0 SHOULD-FIX from both
> reviewers). Same form as D-013 / D-015 / D-035 / D-042.
> **Subject:** `docs/coop/artifacts/component-manifest-schemas.v11.json`
> only.

Turn-1 Codex OBJECT
`docs/coop/artifacts/coordinator-decisions.D-104.review-adversarial.codex.json`
`a1de0ff285e089af19f2728f0bd9343ac9caf32f80eb77eb93be3499ff4a04e2`
(0 MUST-FIX, 1 SHOULD-FIX `D104-SF-1`). Accepted into these bytes:
the decision-type header no longer cites unadopted D-103 as a form
precedent. Operative decision item 1 already named only the adopted
set; the header now matches.

Measured inputs:

| Path | sha256 |
|---|---|
| component-manifest-schemas.v11.json | `1c0b8868444a097256aaa7d9caf8ebaa1c6f73fb071dbb4dd712334abb17a005` |
| Claude 2 verdict | `45785457b25e50e51be7f3a1393427de637022752a9af70b38e87ecb79ce0f20` ACCEPT-WITH-ADVISORIES, 0 blockers, 0 SHOULD-FIX, 2 advisories |
| Codex verdict | `25b2a3fb0200cab5132b333543a708c3bfb024e1fab11b9751c44696e52b1372` ACCEPT-WITH-ADVISORIES, 0 blockers, 0 SHOULD-FIX, 1 advisory |
| D-104 turn-1 Codex review | `a1de0ff285e089af19f2728f0bd9343ac9caf32f80eb77eb93be3499ff4a04e2` OBJECT, 0 MUST-FIX, 1 SHOULD-FIX |
| COORDINATOR-DECISIONS.md | `12d192f758f48f692e69cb410a1d7a9bf776c765257c8e910272d3de457ec3e3` |
| file 08 | `1cdcf9d4071a6c5eaa7cd7d28fac288eaced796c9ee906b6f1db0f7a4b1f95b3` |

If a cited file moves, re-measure.

Finding-id collision (same token, different findings): Claude
`V11-A1` is the citationDiscipline / `whatThisDoesNotDo[1]`
duplication; Codex `V11-A1` is corpus-advance parked on OD-2. This
draft names them `CLAUDE-V11-A1` and `CODEX-V11-A1`. Claude
`V11-A2` has no Codex twin and is named `CLAUDE-V11-A2`.

D-013 remains the historical recording of schemas.v2
(`73114dde…`). This draft does not overturn D-013.

## Decision

1. Record `component-manifest-schemas.v11.json` as DR-103's
   accepted **schema** successor, on the same terms as D-013 /
   D-015 / D-035 / D-042. Both independent reviewers returned 0
   blockers and 0 SHOULD-FIX.
2. Advisories (`CLAUDE-V11-A1`, `CLAUDE-V11-A2`, `CODEX-V11-A1`)
   are not blockers. They do not prevent this recording. They
   remain owed as honesty work on a successor, not as a reason to
   withhold the recording.
3. DR-103 stays `OPEN`. No `SATISFIED`. The fixture-corpus half
   remains unmet (corpus v1 REJECTED; corpus v2 process-frozen
   against schemas.v9 at `70248781…`; SATISFIED-GRADE of that
   corpus is not opened by this recording). No lock is producible.
   ID-DEP-4 / D-013 SATISFIED-refusal stand. D-056 Class A is not
   opened: leftover is not only execution/measurement.
4. Does not edit file 08 (MF-6). No freeze motion. No blueprint.
   Does not authorize `docs/v2/implementation/`.
5. Does not mint a D-096 (A) grant. Does not dispose DR-117.
   Does not retarget corpus v2. Corpus v3, if authored, waits
   until this recording is adopted.

## Alternatives

- Wait for a v12 that folds the advisories. Rejected for this
  recording: 0 blockers and 0 SHOULD-FIX is the gate; advisories
  travel.
- Mark SATISFIED. Rejected: the exact-byte fixture corpus is
  unmet on D-013's own SATISFIED-refusal; lock members remain
  deferred until DR-111.
- Treat dual ACCEPT as application. Rejected: binds NOTHING.
- Retarget corpus v2 at v11. Rejected: V9-S1 / corpusAdvance;
  only corpus v3 or explicit unfreeze-and-recite.
- Keep D-103 in the header as a same-form citation. Rejected:
  D-103 is not an adopted COORD entry at the pinned digest
  (`D104-SF-1`).

## Readiness effect

Zero. Condition 2 stays 4 of 30 `SATISFIED`. Condition 5 stays last.

## Reversibility

Total. Overturn: C-D104.
