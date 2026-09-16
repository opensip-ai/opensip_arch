# Prototype report feature inventory

**Standing: source-inspected author proposal, 2026-09-11; actual Claude review pending.**

This is the single current inventory of prototype report features and their
proposed migration dispositions. [Chapter 14](14-repository-and-module-layout.md)
owns file locations; the [implementation plan](implementation-boundaries-and-build-plan.md)
owns API/build/milestone decisions. A “Preserve” or “Change” row is proposed
design scope, not an implemented or independently accepted parity claim.

## Evidence and limits

The sibling prototype checkout is clean at the already pinned commit `a62509d623173155d0946e9f5d5ca90c839893e0`.
The inventory inspects its host report composition, dashboard generator, browser
modules and selected test sources. File bytes and selected architectural source
digests are recorded in [planning sources](implementation-planning-sources.v1.json).
Links below resolve to that exact prototype commit, not its moving main branch.

The pinned tests supply followable evidence of intended cases: [change-impact tests](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/__tests__/dashboard-change-impact.test.ts), [editor-link tests](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/__tests__/dashboard-editor-link.test.ts), [validation integration tests](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/__tests__/dashboard-validation.integration.test.ts), and [graph-view tests](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/__tests__/dashboard-view-graph.test.ts). These are source references, not executed parity receipts.

This review did not execute the prototype, run its test suite, measure browser
performance or visually qualify accessibility. Test names are evidence of intended
coverage, not a passing result. Source comments describing earlier measurements
are not fresh measurements. The existing [prototype evidence reference](prototype-evidence-reference.md)
continues to own the general prototype pin and its non-authoritative standing.

## Feature dispositions

### R01 — Offline single-file report

**Proposed disposition: Preserve.** Inline the selected data, CSS, JS and vendored assets. No server or script-fetched evidence. Validate the built HTML with network blocked; asset absence must not masquerade as a valid required report.

Prototype evidence: [generator.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/generator.ts), [script-context-json.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/script-context-json.ts).

### R02 — Host composition across tools

**Proposed disposition: Change.** Preserve one coherent report. Replace open-ended tool-owned blobs and hard-coded tool authority with versioned host-approved projections. Tool identity can organize presentation; it cannot override runs, selection, findings or policy. Preserve reserved host-owned top-level keys. Presentation consumes versioned host-approved data projections only. Executable report hooks are not admitted under admission-and-qualification §5; trusted built-in projection and rendering code remain host-owned.

Prototype evidence: [report-compose.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/cli/src/report-compose.ts), [tool-tabs-registrations.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/tool-tabs-registrations.ts).

### R03 — Overview with parent runs and child steps

**Proposed disposition: Preserve.** Map the useful grouped ledger to Invocation/step/attempt/Run identities. Preserve missing child evidence, typed outcomes and duration separately from verdict. A displayed history subset carries its selection and limits.

Prototype evidence: [overview-ledger.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/overview-ledger.ts), [generator-artifacts.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/generator-artifacts.ts).

### R04 — Expandable finding details, sorting and pagination

**Proposed disposition: Change.** Preserve severity/location/details and grouped pagination. Preserve every required finding field; do not copy prototype rules that suppress a message because a metric appears redundant. Distinguish absent detail from a clean result.

Prototype evidence: [session-detail.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/session-detail.ts), [pagination.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/pagination.ts), [sortable.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/sortable.ts).

### R05 — Searchable check/rule catalogs and provenance

**Proposed disposition: Preserve.** Show selected policy/capability descriptions, search/tag/source filters and admitted provenance. Any historical run statistics state their included history and come from a host projection; they never replace the current verdict.

Prototype evidence: [checks.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/checks.ts), [catalog-provenance.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/catalog-provenance.ts).

### R06 — Recipe descriptions and configuration

**Proposed disposition: Preserve.** Display admitted recipe names, descriptions, selectors and applicable parameters. The report cannot execute recipes or confer a grant; unavailable catalog data has an explicit state.

Prototype evidence: [recipes.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/recipes.ts).

### R07 — Functions table with metrics and search

**Proposed disposition: Change.** Preserve sortable, searchable symbol exploration across supported languages. Bind metrics and test reachability to the exact universe/identity and show unknown values. Do not label static caller count as runtime hotness. Search/filter results describe the embedded projection only. Include every embedded occurrence by default, including test functions. Any test exclusion is an explicit visible presentation filter with its active state and resulting subset disclosed; do not inherit the hidden `includeTests: false` default.

Prototype evidence: [view-distribution.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/view-distribution.ts), [view-template.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/view-template.ts), [search.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/search.ts).

### R08 — Package coupling matrix and drilldown

**Proposed disposition: Change.** Preserve directional relationships and drilldown. Counts and evidence come from the selected host graph projection; a blank cell is not a global no-dependency proof when source resolution or projection is incomplete. Drilldown includes test occurrences by default and shares the visible filter state and subset disclosure of R07.

Prototype evidence: [view-coupling.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/view-coupling.ts).

### R09 — Coupling CSV download

**Proposed disposition: Preserve.** Keep an optional local export of the displayed admitted data, with formula-safe text and escaping. Include Run/view identity and completeness context in the export design; a CSV is not an authoritative evidence store or a newly advertised CLI format.

Prototype evidence: [view-coupling.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/view-coupling.ts).

### R10 — Interactive graph, scope controls and cycle highlighting

**Proposed disposition: Change.** Preserve pan/zoom, layout selection, search and package/function views. Use exact symbol identities, distinguish call/import relations and presentation limits, and show the meaning of each highlight. Select a renderer by measured offline size and usability; do not automatically adopt Cytoscape or its versions.

Prototype evidence: [view-graph.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/view-graph.ts), [view-graph-controls.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/view-graph-controls.ts).

### R11 — Function card, callers/callees and cross-view navigation

**Proposed disposition: Change.** Preserve the prototype’s qualified-occurrence entry point and bind it to the exact Run/universe/symbol key. Remove remaining body-hash fallback paths that can collapse distinct occurrences. Preserve location, relationship evidence, copyable paths and singleton detail navigation; twins/clones must remain separately identified.

Prototype evidence: [function-card.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/function-card.ts), [code-paths-panel.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/code-paths-panel.ts).

### R12 — Trace from inferred entry point

**Proposed disposition: Change.** Replace browser entry-point heuristics with a host-projected bounded path and explicit recognition/resolution evidence. A missing path is unavailable, incomplete or absent within a stated scope; it is not proof of dead code. Never execute analysis from the report.

Prototype evidence: [trace.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/trace.ts), [function-card.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/function-card.ts).

### R13 — Change Impact / audit evidence

**Proposed disposition: Change.** Preserve change summary, risks, affected entities and evidence navigation. Use the selected baseline/counterfactual/current Run model and distinguish proven findings from advisory impact or repair suggestions. No automatic repair or test execution in the browser.

Prototype evidence: [change-impact.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/change-impact.ts), [change-impact-trust.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/change-impact-trust.ts), [project.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/change-impact/project.ts).

### R14 — Exact historical run selection beyond recent history

**Proposed disposition: Change.** Preserve explicit historical selection without a latest-run fallback. The prototype special-cases built-in audit and initially lists 20 runs/sessions; the new selection follows applicable command contracts and their exact budgets rather than inheriting those limits or that audit-only restriction.

Prototype evidence: [report-history-selection.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/cli/src/report-history-selection.ts), [change-impact.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/change-impact.ts), [report-selection.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/report-selection.ts).

### R15 — Bounded graph and impact payloads

**Proposed disposition: Change.** Keep compact projections and visible limits. Report the source-analysis limit, host projection omission and browser defensive limit separately. Never drop required parity findings to fit an exploratory graph budget; fail required delivery if the required projection cannot be produced.

Prototype evidence: [bound-catalog.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/code-paths/bound-catalog.ts), [bound-runs.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/change-impact/bound-runs.ts), [change-impact-trust.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/change-impact-trust.ts).

The prototype uses an 8 MiB graph payload cap, a 2 MiB impact payload cap and initial 20-run/20-session history windows. These are pinned implementation observations for measurement cases, not selected product limits.

### R16 — Optional visualization degradation

**Proposed disposition: Change.** Keep independent panel failures visible without discarding usable required data. Distinguish absent, incompatible, corrupt and omitted payloads. Only explicitly optional visualization failure may degrade; a missing required projection is a delivery failure.

Prototype evidence: [generator-artifacts.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/generator-artifacts.ts), [graph-visualization-degradation.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/graph-visualization-degradation.ts), [views-registry.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/views-registry.ts).

### R17 — Script/DOM safety and runtime validation

**Proposed disposition: Change.** Preserve script-safe embedding and text-based DOM construction. Add schema-derived runtime shape validation and compatibility checks; TypeScript assertions or valid JSON alone do not admit evidence. Use deterministic presentation IDs where repeatable HTML is claimed. The embedding codec handles script terminators and, when needed by its selected script context, U+2028/U+2029 safely; browser validation must exercise the actual built output.

Prototype evidence: [script-context-json.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/script-context-json.ts), [el.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/el.ts), [generator.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/generator.ts).

### R18 — Keyboard navigation and accessible disclosures

**Proposed disposition: Preserve.** Preserve semantic tabs/tables, keyboard navigation, labelled controls and live selection/error announcements. Add explicit focus-return, keyboard graph alternatives and contrast checks to the built-browser acceptance lane; source inspection is not an accessibility qualification.

Prototype evidence: [tab-bar.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/tab-bar.ts), [change-impact.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/change-impact.ts).

### R19 — Contextual help

**Proposed disposition: Preserve.** Keep view-specific explanations, close controls and Escape behavior. Explain evidence scope and unknown values; help text stays with the view responsibility and cannot promise stronger analysis than the payload supplies.

Prototype evidence: [help-drawer.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/help-drawer.ts), [views-registry.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/views-registry.ts).

### R20 — Editor deep links and copy path fallback

**Proposed disposition: Change.** Preserve an explicit local convenience with a safe scheme allowlist and copyable relative path fallback. Do not embed absolute project roots in a shareable report by default. One explicit local-link choice controls absolute-root inclusion and editor links, identifies the path disclosure, and defaults to relative-path-only output; no arbitrary repository-supplied URL execution.

Prototype evidence: [editor-link.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/editor-link.ts), [function-card.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/function-card.ts).

### R21 — Guarded optional browser opening

**Proposed disposition: Preserve.** Keep browser opening opt-in, after successful required delivery, and suppressed in machine/CI/noninteractive or unsupported display contexts. An optional launch failure does not change a sealed result. Capture CI/SSH_CONNECTION/SSH_CLIENT/DISPLAY/WAYLAND_DISPLAY only as presentation observations for this choice, never as semantic Plan inputs or authority. The launcher belongs to `crates/platform/src/process.rs`; flag spelling follows the selected command owner.

Prototype evidence: [open-report.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/cli/src/open-report.ts), [report.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/cli/src/bootstrap/report.ts).

### R22 — Run-addressed artifact publication and cleanup

**Proposed disposition: Change.** Preserve safe artifact names and atomic publication through host delivery. Bind each artifact to the selected projection/Run; no arbitrary ID-to-path interpolation. Cleanup follows admitted storage policy and never implies deletion of shared/exported copies or retained evidence.

Prototype evidence: [report-artifact-store.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/cli/src/report-artifact-store.ts), [report-compose.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/cli/src/report-compose.ts).

### R23 — Declared inputs, configuration and provenance display

**Proposed disposition: Change.** Preserve useful input/provenance disclosure using the selected host schema and redaction policy. Make source/producer/coverage/runtime/history limitations visible without leaking secrets or treating imported observations as native proof.

Prototype evidence: [declared-inputs-html.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/declared-inputs-html.ts), [report-compose.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/cli/src/report-compose.ts).

### R24 — Named Fitness / Simulation / Graph / YAGNI and external tabs

**Proposed disposition: Change.** Preserve generic presentation for every selected supported result and advisory candidate. The selected product contracts contain no separate simulation capability or simulation-specific report contract; this inventory neither adds one nor defers an existing obligation. Exact legacy tab names and bespoke simulation/pass-rate dashboards are not required by that generic presentation contract. Future selected capabilities must retain their applicable report parity; this row cannot waive it.

| Prototype tab | Selected migration responsibility | Scope account |
|---|---|---|
| Fitness / fit | Selected fit results in the common findings/evidence projection | Preserve applicable fit HTML and parity fields |
| Code paths / graph | Exact host graph projections in graph and symbol views | Preserve bounded paths, occurrence identities and uncertainty |
| YAGNI | Advisory candidates, inspect and review-brief presentation | Preserve useful advisory results; no new YAGNI command or proof promotion |
| Simulation / sim | Generic presentation for any selected supported result | No separate simulation capability/contract is currently selected; no existing obligation is waived |
| External tools | Versioned host-approved data projections from selected admitted first-party capabilities | Preserve useful admitted output with host-owned validation, keys and rendering; no executable report-hook admission |

Prototype evidence: [tool-tabs-registrations.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/tool-tabs-registrations.ts), [tool-tabs.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/tool-tabs.ts), [generator.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/generator.ts).

## Proposed implementation owners and acceptance

| Responsibility | Owning target modules | Required evidence |
|---|---|---|
| Common projection, data validation and offline assembly | Reporting projection/html_embedding/assets; report report-data and generated binding | Applicable parity, hostile text, unknown/incompatible payloads, no network fetches, required failure propagation |
| Overview, historical selection and catalogs | Report overview-view, history-view and catalog-view; host query/configuration | Exact IDs and history scope, missing evidence states, admissible catalog provenance |
| Findings, evidence and audit | Report findings-view, evidence-view and comparison-view | Complete required fields, baseline attribution, runtime/import limitations and honest incomplete results |
| Graph and symbol exploration | Report graph-view and symbol-detail-view; host query and reporting projection | Exact occurrence identities, bounded relationship/path results, no client-derived policy or global absence claim |
| Navigation, help and exports | Report navigation, help-view and exports | Keyboard/focus behavior, safe routes/schemes, formula-safe local download, no analysis or mutation effects |
| Publication and optional opening | Host delivery and platform process/filesystem | Atomic artifact output, correct after-commit failures, no launch in disallowed contexts |

These browser modules are additions to the canonical filename inventory, not
new applications or providers. Sorting, fuzzy search and layout can be browser
presentation functions over embedded data. Any browser-computed subset statistic
must be labelled as such; semantic paths, completeness, verdicts and required
parity values come from the host projection. No client-side operation can obtain
new repository evidence or promote a display result to an authoritative finding.

## Explicit migration boundaries

- The prototype includes heuristic browser tracing and body-hash lookups. Their
  useful navigation is retained through exact identities and host evidence, not
  by reproducing those algorithms as authoritative analysis.
- The old shared graph filter drawer is not a retained feature: its source says
  it was removed ([filters.ts](https://github.com/opensip-ai/opensip-cli/blob/a62509d623173155d0946e9f5d5ca90c839893e0/packages/dashboard/src/client/filters.ts)). Current visualization owns its controls; other views use their
  own filters. The surviving hidden test exclusion is explicitly removed by R07/R08. Avoid restoring obsolete UI based on filenames alone.
- A report is an offline snapshot. Its availability observations describe the
  recorded observation time/generation; opening the file tomorrow does not learn
  whether the live store was purged. Fresh availability requires a new admitted
  host query/report, with explicit identity and observation provenance.
- HTML is advertised by exactly `default`, `analyze`, `fit`, `audit`,
  `candidates`, `inspect`, `review-brief` and `repair-preview`. Graph/history
  data reach those reports through embedded host projections. `query` advertises
  only human/JSON/agent output; it does not gain HTML from browser navigation.
  SARIF is advertised only by `default`, `analyze`, `audit` and `repair-verify`.
  The embedded projection/schema mapping must follow those exact applicability
  sets before UI implementation. These feature rows do not add arbitrary
  fields to closed CommandEnvelope schemas or advertise a new report command.
- Graph display budgets, browser limits and package-size targets need measured
  acceptance thresholds. Do not inherit the prototype’s 8 MiB graph budget or
  its history caps as product law. They are useful cases for the measurement plan.
- Visual styling, frontend framework, graph library and exact legacy simulation
  UI remain separate choices. R24 preserves generic selected-result presentation
  and records that no separate simulation capability is selected; it cannot
  remove a capability or waive required parity.

## Claude review request

Review all R01–R24 dispositions against the pinned source and final selected
product contracts. Confirm the owner/test mapping and R24 scope account, and check that history, completeness, report limits and optional panel
degradation cannot conceal a required output failure. Assess local editor-link
privacy and the distinction between offline evidence navigation and live queries.
Freeze final inputs at dispatch and retain the substantive response. This is an
additional nonblind review task; no Claude acceptance or prototype parity is claimed.
