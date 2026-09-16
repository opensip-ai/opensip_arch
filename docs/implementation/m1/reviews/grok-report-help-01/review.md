# Independent Grok review: report-help01 original unit

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-report-help-subject-01`
**Manifest SHA-256:** `0e56a4aaeb7d73b6bd34f6f36e77d1cf94dbf1e029114806640f998bc3dda1da`
**Members:** 9
**Verdict:** **ACCEPT WITHIN STATED SOURCE/CONTROL SCOPE**

Initial product help control plus one Chrome headless DOM/keyboard lane. This is **not** final report integration, CSP/bundle, supported-browser, screen-reader, contrast, or M4 qualification. Help copy belongs to each report view; this helper only creates inert text and native dialog controls.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not executed against and not written. Product `apps/report/src/help-view.ts` and `report.css` are byte-identical to this freeze and were not edited.

| Check | Result |
| --- | --- |
| Manifest | `0e56a4aa…a1da` matches declared |
| Files | 9 listed = 9 walk |
| Tool pins | **4/4** (Node v24.16.0, tsc 6.0.3 `_tsc.js`, Chrome binary) |
| After | frozen hash unchanged |

## Compile and browser reproduction

Pinned `tsc` 6.0.3, `--strict --target ES2022 --module ES2022 --lib ES2022,DOM --noEmitOnError`: emit **byte-identical** to `emitted/help-view.js` (`c0bc34b9…acab`).

Private `check-browser.mjs` (pinned Node + Chrome/152.0.7977.83, fresh profile): **6/6**

1. Repository HTML payload stays text (no `img`, `untrustedExecuted` false)
2. Enter opens labelled modal (`aria-label` `About Evidence scope`) and focuses Close help
3. Tab cannot focus background Before/After buttons
4. Escape closes and returns focus to the opener
5. Close control returns focus
6. Dispose removes dialog and control; second dispose is a no-op

Screenshot inspected: modal over inert background, payload visible as text, Close help focused.

**Preserved failures.** `report-help-start/browser-01` and `browser-02` failed the Enter-open check because the CDP harness omitted Enter `text`/`keypress`. Product code was unchanged; the third run passed. Those failures are historical harness bugs, not this freeze’s source.

## Independent probes

Source has no `innerHTML`/`outerHTML`/`insertAdjacentHTML`; paragraphs use `textContent`; title uses `textContent` and `setAttribute`. Native `showModal`, autofocus close, idempotent dispose. Print CSS hides `.report-help`. AX tree (dialog open) has `activeModalDialog`, name `About Evidence scope`, Close help.

Extra Chrome case: HTML in the **title** stays text in opener, `aria-label`, and `h2`; no `img`, `titleExecuted` false.

## Must-fix / should-fix

None in the stated source/control scope.

This does not qualify all browsers, screen readers, contrast, or the final generated report. View-specific evidence-limitation copy is a caller duty.

## Remaining

Integrate view-specific explanations; generated payload/bundle/CSP; supported-browser and screen-reader/contrast/responsive qualification; M4 report completion.
