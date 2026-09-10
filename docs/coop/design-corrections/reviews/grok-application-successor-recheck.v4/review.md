# v4 recheck of v3 tooling findings

Coauthor only. Not independent design ACCEPT, not NEW blind, not application ACCEPT. No bind/assembly/activation ran here.

Scope: the two v3 MUSTs and one SHOULD in `application-successor-root.v1`. Verdict: **CORRECTIONS_CONFIRMED** for that scope.

## MUST-1 (ASM-PRESERVE-ABSENT-LIVE-GUIDES) — closed

`assemble-records.successor.v1.py` now hashes live only if the file exists (`liveSha256` nullable). `liveState` is `absent|exactDigest`. `None != acceptedSha` holds for current live absence of both resume guides. They are not in the 93-file delta or the 17 draft edits, so they are not staged. The unaccounted-live loop still skips them and `NEXT-REVIEW.md`.

`verify-applied.py` now requires those two named paths, `rel not in applied_paths`, `liveState==absent` ⇒ not on live and `liveSha256 is None`, else exact digest, plus `acceptedSnapshotSha256`. No blanket `reviews/` skip. NEXT-REVIEW remains a separate named skip.

## MUST-2 (ASM-EVAL-30-FROM-R12-ONLY) — closed

Evaluation loop copies `design['evaluationResidualDispositions'][row['id']]` and requires the id set to equal the proposed inventory. Binder loads that inventory from the **accepted snapshot** via the frozen manifest, requires 30 ids, and `require_coverage` refuses a dropped row. Independent `review.json` id-set matches the frozen inventory (30/30). R12 remains the inherited parent only, not the eval-item source.

Root `coauthor-v3-correction-checks.json`: `evaluationIndividualRows` 30, `missingIndividualRowRefused` true, syntax passed. Disposable v4 probes: 19/19, including the same dropped-row refusal against the public independent review object.

## SHOULD-1 (RUN-EVALUATOR3-OUTER-BUDGET-NO-SLACK) — closed

`run-application-reference-suites.py` evaluator3 outer budget is **8700** (was 8400). 14×600 = 8400; 300s slack for pin check and process overhead. `8400` is gone from that job list.

## Not in this verdict

Blind10 interrupted at 60 and resumed on the same fresh origin: still no `ACCEPT-RECONSTRUCTABLE`, so bind/assemble remain blocked. Draft 17 `beforeSha256` still match live; rebase if those paths move. Final application review must still grade every row. Frozen23 independent ACCEPT does not authorize application.
