# Report navigation candidate01 — unaccepted

`apps/report/src/navigation.ts` implements local view routing for mounted report
panels. Its view IDs are checked against the supplied generated/validated
supported-view list. Only exact registered `#view=...` fragments reach history;
there are no source requests, repository URLs or editor launches.

The component uses manual-activation tabs: arrows/Home/End move focus, native
Enter/Space selects. Each tab labels and controls its panel. Programmatic detail
navigation may focus a panel heading. Browser Back/Forward restores a registered
view. Empty location selects the first mounted view; an unknown nonempty route
hides all panels and explicitly states that the requested view is unavailable.
It never silently substitutes another view or a latest Run. Cross-view symbol,
candidate and Run selectors are not implemented by this view-only route.

Registration is copied; caller mutation cannot add/change a route. Duplicate,
unsupported, shared or nested panels refuse before DOM changes. Separate instances
reserve distinct IDs, including while detached. Labels use textContent. Disposal
removes listeners and restores the prior panel attributes/visibility and heading
focus attributes. History remains the caller's browser state.

Strict TypeScript compilation passes. A fresh Chrome152 headless process opens a
local file fixture with page network blocked.14 checks exercise actual keyboard
selection, links between tab/panel accessibility attributes, hostile labels,
history Back, focus transfer, unknown routes, immutable registration, invalid
mounts, repeated selection, disposal and detached-instance IDs. The screenshot
was inspected: the selected tab and focus outline are visible and hostile markup
remains literal text. This is a synthetic navigation fixture, not final report
layout, report-data integration, CSP/bundler, screen-reader or supported-browser
qualification. Actual Claude review remains pending.

The compiled navigation module has no runtime dependency on generated contracts;
its import is type-only. The generated file is pinned to report-codec checkpoint02
for compilation. This stages the local-route portion of the inventoried module.
Editor-link scheme validation, local-root opt-in/disclosure and copy-path fallback
remain separate unfinished navigation duties. No arbitrary scheme has been
selected, and no product files were installed.

Compile apps/report/src/navigation.ts using the pinned TS compiler with strict
ES2022/CommonJS, rootDir apps/report/src and outDir compiled. Run
`node check-browser.mjs` in fresh staging; browser01 must not already exist.
Private browser profile state is excluded from the checkpoint.
