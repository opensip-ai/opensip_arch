# Independent Grok review: report history-view01

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-report-history-view-candidate-01`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/report-history-view-01-checkpoint-01/checkpoint.json`
**Manifest SHA-256:** `09bf007e44c078ef627eab8d142b940b46f2db5d714773f0fa4feb6d870397e4`
**Members:** 58 (browser profiles excluded)
**Verdict:** **ACCEPT WITHIN STATED SCOPE**

Staged history panel only. This verdict does not close composition-view01. Not a history engine, host custody, R11 source spans, full report app, or product install. Fixtures are shape/reference reports, not retained Runs. Synthetic 61-row/malicious-path inputs in the original harness are presentation-only controls, not native admitted retained Runs.

## Custody

58/58 listed files and archive `cb4c3674b1580dbfd7f527c98d0fccfa7eaae7652f86aa8e97c6c85601909cb4` / 1607853 bytes match before and after. Profiles excluded. Frozen subject was not executed against. Private copy of listed files only under `review/history/copy`. `history-view.ts` `bb7686baa9349107f75059dbdd674dcae07dec2d90c70ab3d0d73302ed6c1919` / 11184 bytes. Module is not in the product lock (source-selection v3 is).

Original `browser01/failure.json` is retained in the freeze: `"history fits narrow viewport without horizontal page overflow"` after long Run IDs in the native select. Browser02 17 groups; browser03 adds selected-detail narrow (18 groups). Scoped CSS `.history-view select, .history-view input { width: 100%; max-width: 100%; min-width: 0; }` is the recorded fix. That original failure is evidence, not a current defect.

## Module

`createHistoryView` displays the generated history union without deriving selection, verdicts, or a live list.

- **Automatic** (`baseline-source-then-prior-commit-sequence.1`): label “Baseline source, then earlier committed Runs”; shows current commit sequence, prior-runs-in-snapshot, included prior Runs, baseline and baseline source Run.
- **Explicit** (`explicit-run-ids.1`): label “Explicit Run identifiers”; shows current Run or “No retained Run identity”.
- Picker options are exactly `selection.requestedRunIds` in recorded order. `select(runId)` requires the id in both the snapshot map and that requested list. Unknown ids return false with no newest/latest substitution and no DOM change.
- **present:** recorded verdict, required coverage, deficiency, commit sequence, finding identity/path/waiver/fingerprint, embedded/omitted/matching counts. Local search and 25-row paging do not fetch.
- **current-run:** “current Run already represented in this report”; no invented historical findings list.
- **unavailable:** “Requested Run unavailable: {availability}” with optional detail; no findings list.
- Missing panel (“History is not included”), omitted/unavailable reasons, and empty requested list (“No historical Runs were requested”, disabled picker) stay distinct.
- `structuredClone` of panel data; later caller mutation cannot swap a mounted row. `textContent` only. `dispose` is idempotent and refuses later `select`.

Host observation time `reportObservedAt` stays visible. Help states a newer Run never replaces a requested Run.

## Reproduction (private copy)

Commands (Node v24.16.0, TypeScript 6.0.3 from `/tmp/opensip-implementation/m1-joint-generation-candidate-03/tools/contracts/node_modules/typescript/bin/tsc`, same paths as prior view reviews):

- `tsc -p tsconfig.json` in `review/history/copy` (Node16 + `exactOptionalPropertyTypes`, `outDir` `compiled02`): exit 0. `compiled02/history-view.js` byte-identical to freeze `7beca8fc89953550a4394216a9e37e856be7291876b9535fa0a52e0811050d4b` / 12173 bytes.
- `node check-browser03.mjs` after removing copied `browser03` outputs, fresh private Chrome 152 profile, page network blocked: **18/18**, `Chrome/152.0.7977.83`. Chrome closed.
- `node review/probes/independent_history.mjs`: **13/13**. Chrome closed.

**Native04 type delta (separate):** substituted `/tmp/opensip-implementation/m1-native-wire-integration-candidate-04/eight-j/output/apps/report/src/generated/report.ts` (`566dfe9d19316ab65e3da8f6d1cb027d54f9b5c062b0d897d46bc2683bc5228a`, 2166743 bytes) under `copy/native04-delta`. `tsc -p tsconfig.json` exit 0. Frozen generated `f5174bec08663c29440bd395431b547eed9faf678011fe814ceb0ee1e9836a69` / 2140727 bytes is preserved as original fixture evidence. Original fixtures predate native04 required-history-items.

## Independent DOM probes (13/13)

Automatic vs explicit policy labels; unknown Run does not substitute newest; unavailable row shows recorded reason not latest; current-run does not invent a historical copy; XSS Run id/path stay text (`<img>`/`<script>` literal, no markup, no `globalThis.xss`); embedded vs omitted vs matching search counts; exactly 25 findings disables Next; caller mutation cannot swap mounted row; missing panel distinct; empty requested Runs explicit; dispose refuses stale select; observation time and automatic snapshot counts/order; independent 200-character Run id at 390px does not overflow the page (counterexample of original browser01).

## Must-fix / should-fix

None in this view scope.

## Remaining

R11 source-location projection remains required before M4. Not assets/CSP, host custody, release, engine, or fresh blind consumer. Dense 61-row harness control is presentation-only. Copied composition01 sources in this freeze are a parent snapshot, not this unit’s verdict and not a waiver of composition-view01. Not Claude agreement.
