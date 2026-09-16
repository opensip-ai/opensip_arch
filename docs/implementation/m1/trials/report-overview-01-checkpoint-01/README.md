# Report overview candidate01 — unaccepted

`apps/report/src/overview-view.ts` displays the decoded report's operational
summary, step outcomes, exact Run/Execution/Step identifiers, attempts, service
time and incomplete observations. It uses the staged report reader and existing
help control. It never derives a new verdict or Run, substitutes latest history,
or treats a missing identifier as proof that no Run exists.

Timing preserves measured zero, exact u64 milliseconds, missing observations,
legacy unretained timing and unfinished rendering. Service time is labelled as
attempt service time, not total elapsed time. Execution mode Standard makes no
promise of a durable commit. Error codes, remedies and subjects are rendered as
text; large structured pin/purge detail is acknowledged as embedded data instead
of silently presented as absent. This is a summary, not the full termination or
mandatory static parity surface.

The overview integrates contextual help, a semantic step table, a labelled
keyboard-focusable scroll region and explicit missing-child entries. Metadata
uses a compact wrapping grid. The staged `report.css` preserves the exact
predecessor bytes and appends only overview layout rules. Product files remain
unchanged pending actual review and final source/bundle integration.

Strict TypeScript compilation passes.12 browser groups pass in fresh headless
Chrome152 over a local file, with page network blocked. All31 unchanged current
reference reports render exact step and Run identifiers. Separate schema-only
formatting controls cover zero/max-u64 durations and hostile remedy/subject text;
those controls do not claim authentic clocks or complete host semantic admission.
Tests also cover legacy/unrecorded timing, semantic headings, contextual help,
focus return, disposal, narrow-page overflow containment and actual keyboard
horizontal table scrolling.

Desktop and390px viewport screenshots were inspected. Current browser03 images
are byte-identical to the inspected browser02 images; the final change adds
keyboard semantics to the scroll region. Earlier layouts, compiled code, browser
results and screenshots remain preserved in before-layout/, before-scroll/ and
browser01/02. Browser03 is current. This is not final CSP/bundle, all supported
browsers, mobile-browser or screen-reader qualification.

input-pins.json verifies generated-codec, reader, fixture and help/style inputs,
the selected Node binary and140 compiler files. This verification does not select
a final package manager/bootstrap recipe. Compile overview-view.ts and
report-data.ts with strict ES2022/CommonJS and rootDir apps/report/src into
compiled/, then run check-browser03.mjs in fresh staging (browser03 must not
exist). Earlier harness builders/runs remain historical evidence.

Actual Claude review remains pending. Further work includes navigation/entrypoint
integration, other report views and precise local selection routes, complete
static parity/error presentation, host semantic admission and delivery, final
asset/CSP binding, and full product/release qualification. This candidate does
not close M4 or the unaccepted report owner/source decisions.
