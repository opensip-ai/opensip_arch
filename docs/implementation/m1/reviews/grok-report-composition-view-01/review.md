# Independent Grok review: report view-composition01

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-report-view-composition-candidate-01`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/trials/report-view-composition-01-checkpoint-01/checkpoint.json`
**Manifest SHA-256:** `79e536aecd905dd6a46b656eb868872fce6dc6cf9359b9b382003f4edca4cbae`
**Members:** 57 (browser profiles excluded)
**Verdict:** **ACCEPT WITHIN STATED SCOPE**

Three-view integration harness (overview, evidence, catalog + local navigation). This verdict does not close history-view01. Not a completed application, host custody, R11 source spans, assets/CSP, or product install. Four local sources change: `report-data.ts`, `evidence-view.ts`, `navigation.ts`, `report.css`. Other copied view/help/generated modules remain exact parent bytes. Fixtures are shape/reference reports, not retained Runs. Ephemeral Plan evidence is a shape-only witness.

## Custody

57/57 listed files and archive `aab343fb88be0e122d8a385199ca20fd67327c99002e4716562bf231a687fa9f` / 1589338 bytes match before and after. Profiles excluded. Frozen subject was not executed against. Private copy of listed files only under `review/composition/copy`.

Local hashes:

| Path | SHA-256 | Bytes |
| --- | --- | --- |
| `apps/report/src/report-data.ts` | `4ac8229d983deac42654b2b454244e4c54f5f010d281a337ee5a1ac8b344cd7f` | 4269 |
| `apps/report/src/evidence-view.ts` | `de97365a5799dc86734daa44f5fcdb561b19787ef7b6988650c35d7a948c3736` | 10244 |
| `apps/report/src/navigation.ts` | `425c955b15700bae969c986145b8ede2a119383e2c6133d246845e4297f9c91b` | 7871 |
| `apps/report/src/report.css` | `2c41c99f8ba3e616f9a103c4fc9f2e6591d9a89e259ecdacef7f5e086d6469c6` | 11366 |

None of these modules are in the product lock (source-selection v3 is).

Original failures preserved in the freeze, not reopened:

- **browser01:** `"coverage detail has separate examination and resolution observations"` — harness expected a capitalized Confidence label; product label is `Analyzer confidence (millionths)`.
- **browser02:** hash/history route change left a top-layer help modal on a hidden panel. `navigation.ts` now closes `dialog[open]` inside a view before hiding it.
- **browser03** passed; **browser04** adds spacing between a focused expanded summary and the first field label (14 groups).

## Module

`decodeReportData` is a profile6 shape reader: family/major, `opensip.report-projection.development-caps.6`, document byte/depth caps, then generated `matches(report-projection:1#)`. Incompatible profile5 returns `{status:'unavailable', code:'incompatible-profile'}` with no `report` key and no partial object. Success deep-freezes the tree. The reader does not authenticate source custody, recompute a verdict, or grant tool authority.

Evidence presentation uses the generated EvidencePanelV1 source union: retained `runId`+`evidenceId` as “Source Run”; ephemeral `planId`+`evidenceId` as “Ephemeral source Plan” plus “no retained Run identifier”. Empty included rows with nonzero collection total stay distinct from a truly empty collection. Recorded counts, coverage ids, confidence millionths, and closed-world conditions display as text. “These recorded conditions are evidence inputs. They do not authorize a repair.” Hostile closed-world reasons stay `textContent`.

Navigation mounts only exact registered views. `select` of an unmounted id (including other report views such as findings) returns false with no substitution. Unknown `#view=` hides every panel and sets status “The requested view is unavailable in this report.” Route change closes open dialogs in the hidden view and restores tab focus when the hidden panel held focus. `dispose` is idempotent and restores original panel attributes.

Overview/catalog compose through the same `supportedReportViews` gate. Catalog is created with `panels.catalog ?? absent` and `panels.descriptions ?? absent` where `absent={state:'omitted',reason:'not-selected'}`. Catalog copy requires a reason string on omitted state (`words(state.reason)`); that is catalog-view’s existing contract, not a composition decoder defect.

## Reproduction (private copy)

Commands (Node v24.16.0, TypeScript 6.0.3 from `/tmp/opensip-implementation/m1-joint-generation-candidate-03/tools/contracts/node_modules/typescript/bin/tsc`):

- `tsc -p tsconfig.json` in `review/composition/copy` (Node16, `outDir` `compiled`): exit 0. Compiled JS frozen-identical: `report-data.js` `ff0c1d2f147e21abd2457a3de1066157d69c6317a642370916f342bcc4a914eb`, `evidence-view.js` `9c0e3fd8fbfe46d5a312cdadff9a40e5b6536a1129b07d936b3bea7953143ecd`, `navigation.js` `046dbc18226fffd0db1c783f797fd8d8248021937747208899876d2b464ccf92`.
- `node check-browser04.mjs` after removing copied `browser04` outputs, fresh private Chrome 152 profile, page network blocked: **14/14**, `Chrome/152.0.7977.83`. Chrome closed.
- `node review/probes/independent_composition.mjs`: **16/16** after two probe-setup corrections (below). Chrome closed.

**Native04 type delta (separate):** same native04 generated substitution (`566dfe9d…228a`) under `copy/native04-delta`. `tsc -p tsconfig.json` exit 0. Frozen generated `f5174bec…6a69` preserved. Original fixtures predate native04 required-history-items.

## Independent DOM probes (16/16)

All 32 current projections decode/compose; old profile5 refuses without a partial object; decoded tree freeze blocks mutation; only supported implemented views mount (findings/comparison/graph/history never appear); retained vs ephemeral identity; exact Run/evidence/coverage ids and recorded counts; catalog+overview compose with catalog’s no-execute limitation and overview observation time; empty included rows ≠ empty collection (`0 of 5` plus five omitted at item-cap); zero collection distinct; `9007199254740993n` examined-subject count exact; hostile closed-world reason is text; unknown `select` refuses; unknown hash shows unavailable without substitution; hash route closes hidden help modal and restores the selected tab’s focus; no `a[href]`; dispose removes navigation/views/modals.

Probe-setup failures preserved (not product defects):

1. First independent compose threw `TypeError: Cannot read properties of undefined (reading 'replaceAll')` in `catalog-view.words` because the probe mounted catalog with `{state:'omitted'}` and no `reason`. Original harness passes `absent={state:'omitted',reason:'not-selected'}`. Probe rewritten to match `check-browser04.mjs` `show()`.
2. Intermediate assertion fail (`review/results/independent-composition-probe-assertion-fail.json`): sloppy-mode assignment to a frozen object does not throw (value was unchanged); empty-rows check wrongly expected “5 of 5” included instead of the view’s correct “0 of 5”. Corrected probes then 16/16.

## Must-fix / should-fix

None in this composition scope.

Advisory: evidence-view holds a live `state.data` reference (it does not `structuredClone`). On the composed reader path `decodeReportData` deep-freezes the report, which is the mutation barrier. Unfrozen synthetic states can change on a later page render. Catalog-view still requires `reason` on omitted/unavailable states.

## Remaining

R11 source-location projection remains required before M4. Not assets/CSP, host custody, release, engine, remaining report views (findings/comparison/graph/history), or fresh blind consumer. History-view01 is a separate unit. Not Claude agreement.
