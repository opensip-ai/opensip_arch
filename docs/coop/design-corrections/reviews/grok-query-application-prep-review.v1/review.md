# Query24 application-prep tooling — coauthor review

**Standing.** Actual Grok, bounded read-only coauthor review of four prospective documentation-application adaptations. Not independent design ACCEPT, not NEW blind, not application ACCEPT, not bind/assembly/activation, not product implementation. The active independent-design worktree was not opened. Frozen24 snapshot, live tree, draft.v4, and successor-root tooling were read only; none of those trees was edited.

**Verdict: `SCOPED_CONFIRMATION`.** The four named query24 adaptations are sound against the v4 tooling corrections (`ASM-PRESERVE-ABSENT-LIVE-GUIDES`, `RUN-EVALUATOR3-OUTER-BUDGET-NO-SLACK`). No new MUST/SHOULD. No bind, assembly, or application was performed here.

Subject pins used as given and rehashed: frozen24 manifest `a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb`, archive `5c697bd673c6dbf05db22231ac4347a5007f096148571d75559aa046e339dde4`, snapshot `/tmp/opensip-design-corrections/candidate-subject.v24`. Root `current-status.json`: `readyForAssembly` false, `actualApplicationPerformed` false, `sourceAcceptance` false, 98-file source delta, no unexpected live deltas.

## 1. Draft.v4 current-review attribution — confirmed

`application-draft.v4` is v3 plus the three current D-372 attribution replacements in `current-review-attribution-correction.v1.json`. Byte diffs vs v3 are only:

- `files/docs/START-HERE.md`
- `files/docs/v2/architecture/08-decision-and-readiness-register.md`
- `documentation-proposal.json` (`proposedSha256` for those two paths)
- added `current-review-attribution-correction.v1.json`

All 17 `beforeSha256` values are identical to v3 and match live `opensip_arch`. All 17 draft after-images match `proposedSha256`. `readiness-row-map.proposed.json` is byte-identical to v3 (`01e37c6f…`). Condition 5 / `NOT MET` counts in the two changed files are unchanged.

| Path | Replacement |
|---|---|
| START-HERE current D-372 sentence | `following actual Claude's independent review and a fresh blind consumer review` → `following the independent design and fresh blind consumer reviews pinned in the application record` |
| Register D-372 pin sentence | `independent actual-Claude review` → `the pinned independent design review` |
| Register condition 3 | `fresh actual-Claude review of mixed final bytes` → `fresh independent design review of the exact final bytes` |

Those three `beforeText` strings are absent from v4 files and from live (they existed only in draft.v3 proposed bytes). Remaining Claude strings are historical: START-HERE Codex–Claude FAQ; register DR-001 historical verdict cell; D-134 `CONSENT Claude` ids; `### Historical depth-review findings — 2026-09-05` / “Actual Claude performed three independent review passes”.

This removes a false current Claude-agreement claim from the prospective D-372 text without changing the 17-file readiness set or live before-images.

## 2. Apply-advisory measured counts — confirmed

`apply-advisory-records.successor.v1.py` (`2ed606dc…`) parses. The preserved failure copy `apply-advisory-records.query24-syntax-failure.v1.py` (`825d3bd1…`) is still `SyntaxError` lineno 258, unterminated f-string. `apply-advisory-records.before-query24.v1.py` still has the source23-era hardcoded sentence (375 native / 14 schemas / older 132/thirteen stale / four current advisories).

Current compose (after assembly writes the chronology needle) interpolates accepted-snapshot reports:

`native['cases']['passed']`, `workflow['passed']`, `old['evaluator3']['suiteCount']`

Against frozen24 those fields are **375**, **1803**, **15**. The f-string contains none of `four current`, `132`, `thirteen`, or `stale`. It does not call source24 docs stale; it says historical source23 recording corrections are not unresolved current advisories. Frozen README still contains historical `native132` under stacked chronology headings; assemble places that live README under `## Historical correction chronology (not current status)`, and apply prepends the measured paragraph above that needle.

Assembly prerequisite is not bypassed: apply still `assert bound.get('readyForAssembly') is True` (assemble and launch assert the same). Apply reads the staged `application.v1.json` and the assemble-written README needle (`assert text.count(needle) == 1`). Root status remains `readyForAssembly` false.

## 3. Third historical guide, named exception only — confirmed

`assemble-records.successor.v1.py` `variant_paths` and `verify-applied.py` now name exactly:

- `docs/coop/design-corrections/reviews/resume-before-v24-next-review.v1.md` (new)
- `docs/coop/design-corrections/reviews/resume-before-v23-next-review.v1.md`
- `docs/coop/design-corrections/reviews/resume-source21-next-review.v1.md`

No blanket `reviews/` skip. `NEXT-REVIEW.md` remains a separate named skip.

Frozen24 contains all three (manifest+snapshot digest match). Live: all three **absent**. They are in neither the 17 draft edits nor the 98-file `application-source-delta.v24.json`, so assemble will not copy them into `stage/files`. Simulated live-absent loop: `liveState=absent`, `liveSha256=null`, `None != acceptedSha`. Verify requires `rel not in applied_paths` and absent ⇒ file missing. Snapshot copies stay in the frozen tree only.

Live `NEXT-REVIEW.md` is present and different from both snapshot `NEXT-REVIEW.md` (`fd8cf2d6…`, 763 bytes) and `resume-before-v24-next-review.v1.md` (`35c7b18b…`, 759 bytes). Live `NEXT-REVIEW.md` is `37c4ff0d…`, 41788 bytes. That mutable file is not in `variant_paths`.

`before-query-guide24.v1/` retains the two-guide originals (`assemble-records.successor.v1.py` `30fa2c3f…`, `verify-applied.py` `2f44e2cb…`).

This is the v4 `ASM-PRESERVE-ABSENT-LIVE-GUIDES` mechanism with one added named path, not a broadened ignore.

## 4. Evaluator3 outer budget 9300 / dynamic helper — confirmed

`run-application-reference-suites.py` evaluator3 job is 9300s. Source is `root/(dc+rel)` (`foundation/run-evaluator3-checks.py`), so the tree under `--root` supplies the helper. `8400` is gone.

Frozen24 / query-successor helper digest `dbdedb51…` (same bytes). The helper lists **15** jobs, each `timeout=600`, including `query-projection`. 15×600+300 = **9300**. That keeps the v4 closed SHOULD (outer slack of 300s over N×600; v4 closed at 8700 for 14 children).

The helper is new versus live (`beforeSha256` null in the 98-file delta; live path absent). Application reference runs use a disposable snapshot copy with staged overlay (`prepare-validation.py`), which has the helper. Dynamic selection is therefore compatible with source24. Product reference suites were not re-run here.

Root `finalizer-selftest.query-successor.v1.json`: 20/20, `failed: []`, `actualApplicationPerformed: false`. Synthetic ACCEPT labels in that selftest are not project review evidence.

## v4 findings (not re-opened)

| v4 id | Query24 relation |
|---|---|
| `ASM-PRESERVE-ABSENT-LIVE-GUIDES` | Closed pattern retained; third named snapshot-only guide added |
| `RUN-EVALUATOR3-OUTER-BUDGET-NO-SLACK` | Closed pattern retained; slack scaled 14→15 children (8700→9300) |
| `ASM-EVAL-30-FROM-R12-ONLY` | Not re-audited; outside these four adaptations |

## Outside this verdict

- Frozen24 has no independent ACCEPT in this review; source24 fresh independent review is a separate session.
- NEW blind kit 80 is prepared and not launched.
- No bind-review-receipt, no assemble, no apply, no freeze, no activation.
- Draft 17 `beforeSha256` still match live; rebase if those paths move before assemble.
- Final application review, if later authorized, must still grade every AR/FW/inherited/eval/condition-2/owner/gate row.

## Minimal remedy

None for these four adaptations.
