# Report evidence view candidate01 — unaccepted

`apps/report/src/evidence-view.ts` presents coverage evidence with exact Run,
evidence collection and per-result identities. Examination coverage, resolution
completeness, subject counts, unresolved edges, confidence and closed-world
conditions remain distinct. Identity details are expandable beneath the useful
coverage observations. No findings, absence or repair authorization are derived.

The internal presentation input uses existing generated native/identity types.
It follows the separately proposed R-COVERAGE-SOURCE-1 source binding, but is not
a new wire decoder or final report carrier. The final generated report adapter,
source admission and whole-report budgeting still require integration. The
existing report reader cannot consume the proposed standalone panel as Report1.

Every declared unavailable/omitted/corrupt/incompatible reason remains explicit.
Zero embedded rows with omitted source rows is distinguished from a genuinely
empty source collection. Neither implies that no callers or dependencies exist.
Page controls show at most50 included rows, preserve source ordering, announce
the included range and move focus when a navigation button becomes disabled.
They never fetch omitted evidence. Long identifiers wrap; reasons/remedies render
as text. Contextual help explains confidence and the limits of coverage evidence.

Strict TypeScript Node16/ES2022 compilation passes. Initial compilation selected
deprecated node10 resolution and failed TS5107 before source checking; compile01
logs preserve it. compile02 passed. The final layout moves identity detail below
the coverage fields; compile03 and browser02 are current. browser01 and the prior
source/compiled layout remain preserved under before-layout/.

17 browser groups pass in fresh private headless Chrome152, using a local file
with page network blocked. Positive rows come from the two actual complete-replay
admitted synthetic reference Run results in coverage-binding01. Their generated
native/descriptor shape checks also pass in the browser. Separate formatting-only
controls cover empty/unknown/max-u64/zero-confidence, hostile strings and101-row
paging. Those controls deliberately do not assert native or source admission.
All11 missing-panel reasons match the current generated union. Native details
and pagination use actual keyboard events; help focus and disposal pass. Desktop
and390px screenshots were inspected after the layout change; no horizontal page
overflow was observed. AX trees are retained, not screen-reader qualification.

input-pins.json binds five source inputs to their durable checkpoints and verifies
the selected Node binary and140 TypeScript compiler files. Styles preserve the
entire overview predecessor as a prefix. Compile with strict ES2022, module and
moduleResolution Node16, lib ES2022/DOM, rootDir apps/report/src and outDir compiled.
Run check-browser02.mjs in fresh staging where browser02 does not exist.

Remaining: actual Claude review, report carrier/version and budget succession,
final generated adapter/entrypoint, actual immutable snapshot/host custody,
script-independent parity, final bundle/CSP, all supported browsers and full
accessibility/release qualification. No product files changed. This supplemental
checkpoint does not freeze a review target, establish acceptance or complete M4.
