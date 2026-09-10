# Coauthor review of prospective application tooling (root.v1)

Not independent design review. Not NEW blind. Not application ACCEPT. Frozen subject `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25` has a separate actual Grok independent ACCEPT (`reviews/grok-independent-design.v23`, session `01a082bd-172b-7f73-a896-33f7899338c3`). That review does not authorize binding or application. Blind consumer10 is still running. This note only inspects public authored tooling.

Public probes only: draft `beforeSha256` vs live, source-delta vs draft/live/snapshot, resume-guide presence, independent `review.json` keys. No assembly, retain, or activation. No raw CLI envelopes.

## Current fixes that hold

- **Source transfer:** `application-source-delta.v23.json` is 93 paths, `designSubjectSha256` matches frozen23, `unexpectedLiveDeltas` empty. No overlap with the 17 draft edits. Architecture 03/10/13 and NEXT-REVIEW are not in the delta. All 93 `afterSha256` match the snapshot; all 93 `beforeSha256` match live (including 60 live-absent new paths as `null`). Assembler copies those from the snapshot only when the draft target is absent.
- **Pin closure:** `application_pins.prepare` compares staged bytes to the **accepted snapshot**, not live. Prospective-pin-check: three opening paragraphs on 03/10/13; four ordinary ledgers each retarget those three hashes; evaluator3 ledger retargets 3+4. Draft∩ledger is exactly those three chapters.
- **Receipts:** binder now copies `launch`. Retainer derives `chat_history.jsonl` from process cwd + session if the bound receipt has no transcript path, and still refuses a wrong named path. `check-retain-public.report.json` is 40/40. CLI raw stdout is excluded by `launch.stdoutName`, not one hardcoded name.
- **Runner:** six top-level groups plus nested `workflow-surface` from `workflows.json.check.exitCode`, matching frozen `final-reference.v23`’s seven names. Child timeouts are recorded inside evaluator3’s own report. `freeze-application.py` / `verify-applied.py` / `prepare-validation.py` now expect seven command rows. Post-apply runner delegates to the same suite.

## New findings

### MUST-1 — assemble preservation block cannot run on live

**Selector:** `assemble-records.successor.v1.py` `variant_paths` / `digest(root/rel)` (paths `docs/coop/design-corrections/reviews/resume-before-v23-next-review.v1.md`, `.../resume-source21-next-review.v1.md`).

**Reproduction:** Those two paths are in the v23 manifest and snapshot (`693d1be4…`, `4d3cb02f…`) and are **absent** on live `/Users/sb/code/opensip-ai/opensip_arch`. They are not in the 93-file delta. `digest(root/rel)` raises before any “preserve, do not overwrite” skip.

**Consequence:** Assembly of the otherwise-complete delta fails. The live mutable guide that actually differs is `NEXT-REVIEW.md` (live `b7f9ffdc…` vs accepted `35c7b18b…`), which is already skipped and not in the delta.

**Remedy:** Do not require live files. Record `acceptedSnapshotSha256` and live state `absent` or an exact live digest. Do not stage snapshot copies. Do not apply them.

### MUST-2 — 30 independent eval dispositions are dropped

**Selector:** `assemble-records.successor.v1.py` evaluation loop: `independentDisposition = design['inheritedResidualDispositions']['DR-011-R12']` for every proposed eval item.

**Reproduction:** Independent `review.json` has `evaluationResidualDispositions` with **30 distinct** rows (`RES-EP13-01` …), each `ROUTING-ASSESSED-ONLY-NOT-APPLIED` with its own basis. Assembler never reads that map. Binder `require_coverage` also does not require it.

**Consequence:** `evaluation-residual-dispositions.applied.v1.json` would cite R12 for all 30 and hide the independent per-item account the final application reviewer is told to grade.

**Remedy:** Copy `design['evaluationResidualDispositions'][item.id]` (fail if missing). Keep R12 as the parent inherited row only.

### SHOULD-1 — evaluator3 outer budget has no child-timeout slack

**Selector:** `run-application-reference-suites.py` job `evaluator3` `8400`; `foundation/run-evaluator3-checks.py` 14 sequential children `timeout=600`.

**Reproduction:** 14×600 = 8400. Pin check and process overhead sit outside the children. v21’s documented lesson was an outer budget **larger** than inner×N.

**Consequence:** A completing 14-child suite can still set top-level `timedOut` and fail the seven-row gate.

**Remedy:** Raise the outer cap (v21 used +600s slack) or stop the outer timer while children use their own 600s reports.

## Known remaining root work (not new)

1. **`verify-applied.py` still excepts only `NEXT-REVIEW.md`.** After apply it will require every other accepted path on live to match the snapshot. The two snapshot-only resume guides (absent on live) and any other same-named historical guide need **named** exceptions with exact before/accepted digests — not a blanket `reviews/` skip. Do not overwrite live `NEXT-REVIEW.md`.
2. **Draft rebase** remains required if those 17 paths move before assemble. **Today** all 17 `beforeSha256` values match live, and the disposable pin-check already passed those draft after-images against the accepted snapshot. Rebase is still the rule; it is not currently a stale-hash failure.
3. NEW blind is not finished. Binder/assembler must not run without `ACCEPT-RECONSTRUCTABLE` and Codex `rootBlindAssent`/`fullRead`.
4. Final application review must independently grade all 16 AR / 15 FW / 27 inherited / 30 eval / 28 condition-2 / 5 owners / 32 gates. Assembler `ACCEPT-DESIGN` wrappers are not that review.

## Out of scope / not bugs here

Foundation and workflows `source-pins.v1.json` are byte-identical in frozen v23 (1211 rows). Pin helper will keep them identical. That is snapshot fact, not this tooling. Public retain of application reviews looks fixed relative to v1’s rglob leak; do not run the v1 retainer.
