# Report projection and fit successor contract (author-06)

## 0. Standing

This is an **author-06 correction candidate** answering the fresh independent review `m1-report-projection-review-05` of frozen `m1-report-projection-subject-05` (manifest `a9f6c22a…de2a4`), covering RPR5-1..3 and advisories A1–A7. Root reproduced the subject-05 strict check independently; review-05's "root still running" note is stale process status. This candidate is not approval: a separate review and root acceptance are still required.

| Scope | State |
|---|---|
| Carrier unit | Candidate for review |
| Report design | **Blocked**: all 11 feature blockers (RP-DO-01, 03..12) stay open. RP-DO-03/05/09/10 are being closed by the separate author `m1-report-evidence-design-author-01` and are not duplicated here. |
| M1 final integration | **Blocked** by RP-OBL-C01 (pre-Run interruption empty form), RP-OBL-C02 (cancellation Run selection successor) and RP-OBL-K01 (coverage key) |
| AUDIT-G10 | Open |

**Parents and successors:**
- **envelope5 bytes are unchanged** (`45de2b0a…789d`, 36,852 B). They are the exact parent of the unselected envelope6 candidate.
- Envelope6 and root interruption successor03 (`dcec8ab9…4e14`, unreviewed) are **not adopted**, and no file here references `command-envelope:6`.
- Current behaviour kept: the owner model's required-only cancellation Run selection and the required-only settled D9 aggregate.

**Not claimed:** no browser, renderer, generator, product runtime, host signal handling or performance.

## 1. Subject, closure and how to check

**Subject.** `subject-files.json` lists 19 files and excludes only itself. The two new owner records are `owner/builtin-step-planning.v1.json` and `owner/query-fixture-correction.v1.json`.

**Run it from a copy of exactly the listed files:**

`TMPDIR=<existing absolute dir> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py --architecture ARCH --subject-strict [--out RESULT]`

**Closure.** This is a trusted-reference claim only, not a sandbox.
- **Pins:** 82 files and 3 listings. New since subject-05 are `query_projection_model.v3.py`, `query-projection-contract.v3.md` and `foundation/evaluator-projection-registry.v1.json`, plus the evaluator3 schema listing; the owner query model is now executed.
- **Hook:** governed opens are re-hashed at open, listings recomputed at use, and aliases resolved through realpath, case-folding and `(st_dev, st_ino)`.
- **Scratch (A1):** the exemption now applies only to the **resolved target**. A link placed inside scratch that points elsewhere stays governed.
- **Loading:** the fresh-source loader compiles verified bytes, no child process runs, and only the declared out path is written (confirmed by the observed-writes line).
- **Out of claim (A6):** hard links, native extensions and concurrent-writer TOCTOU.

## 2. Finding-by-finding disposition (review05)

### RPR5-1 (blocking): host requirement and dependency flags — corrected

**Owner reading.**
- No owner text binds builtin expansions, and the inventory `steps` field is only a kind summary.
- The pinned owner shapes are:
  - `workflow-cases.v1.json` invocation cases: analysis then render(terminal) on [0]; audit as a delegated primary analysis, then comparison on [0] with `currentStep` 0, then render(terminal) on [0,1];
  - `AnalysisParams.role`: the pivot analysis is auto-planned before the primary analysis only when a comparison needs the detector pivot and its closure is admitted;
  - `workflows-and-surfaces.md` §1 Dependencies: the generic DAG law.

**Smallest owner successor.** `owner/builtin-step-planning.v1.json` binds the exact expansion (`planRole`, kind, requirement, `dependsOn`, `dependencyGate`, params binding, planning condition) for all eight html commands:

| Command | Variants |
|---|---|
| default | primary: analysis → render[0] terminal |
| analyze | primary: analysis → render[0]. `with-import` is recorded as **unresolved, not plannable**: no ImportParams grammar and no owner planning condition (RP-OBL-P01). No bogus import is planned. |
| fit | analysis → query[0] → render[0,1] |
| audit | `no-pivot`: delegated analysis → comparison[0] (`currentStep` 0) → render[0,1]<br>`with-pivot`: pivot analysis → delegated primary → comparison[0,1] (`currentStep` 1, `pivotStep` 0) → render[0,1,2] |
| candidates, inspect, review-brief | query → render[0] |
| repair-preview | repair-preview (`--run` evidence source) → render[0] |

**Selector delta.** `owner/command-inventory.v5.schema.json#/$defs/Command/properties/steps/description` changes from absent to "maximal step-kind summary …; exact expansions bound by builtin-step-planning.v1". The restoration check removes exactly that description.

**Fixture corrections.**
- Subject-05's audit comparison `dependsOn [1]` versus `[0,1]`, and its planned analyze import, were constructions. They are replaced by bound variants.
- New base `audit-with-pivot` is added.

**Admission.** The ledger now carries `planVariant`, and each step carries `planRole` and `dependencyGate`. The joins run in this order:
1. `J-LEDGER-DAG`: the generic law, the same codes as `validate_dag`.
2. `J-LEDGER-PLAN`: steps must equal the declared plannable variant exactly.
3. `J-LEDGER-MODE`: ephemeral only with the command's `--ephemeral` flag.
4. `J-LEDGER-RUN`: the envelope Run is the primary analysis step's Run, not the pivot's.

The variant's planning condition is host-asserted.

**Executed evidence (`builtinPlanning`).**
- The pinned owner `workflows_model.v1.py validate_dag` admits every plannable expansion.
- Every mutant is refused by the owner with the same code as the report DAG law: required step made optional → `WORKFLOW.REQUIRED_DEPENDS_ON_OPTIONAL`; terminal gate on a non-render step → `GATE_NOT_APPLICABLE`; forward dependency → `DEPENDENCY_CYCLE`.
- A comparison whose `currentStep` is dropped from its dependencies is refused by the owner (`DEPENDENCY_INVALID`) and by the report's `J-LEDGER-PLAN`.

**Report cases.**
- Reviewer **S1** on all 6 bases → `J-LEDGER-DAG`.
- **S2** (edges also dropped) on all 6 → `J-LEDGER-PLAN`.
- Kind drift, variant label mismatch, dropped comparison dependency and swapped pivot/primary roles → `J-LEDGER-PLAN`.
- Pivot Run as envelope Run → `J-LEDGER-RUN`.
- Planned analyze import → `J-LEDGER-PLAN`.
- Terminal gate on analysis and forward dependency → `J-LEDGER-DAG`.
- Default ephemeral → `J-LEDGER-MODE`.

### RPR5-2 (required): page law narrower than the owner fixture — resolved by owner evidence, fixture corrected

**Verified reading.** In `query_projection_model.v3.py`, `finish_operation` is called by both `execute_graph_query` and `traverse_projected_graph`. It computes every logical unit, applies the produced cap, then slices the page. So:
- `producedItems` is the produced-prefix length, and `totalItems` equals it;
- a cursor names `position+items` inside the prefix;
- lower-bound arises only from a reached visited or produced cap.

That is the selected eager law, and no owner evidence contradicts it. The `query_surface_projection.v3.py:620-645` case is an isolated renderer fixture that `finish_operation` cannot produce. No lazy algorithm is added.

**Exact correction** (`owner/query-fixture-correction.v1.json`; parents not edited; each before-text is asserted against the pinned bytes):
- `query_surface_projection.v3.py` 621–627: `ctx_lb` total/produced 2/2 → **100000/100000** (lower-bound, truncated-page, 2 rows with cursor).
- line 513: `graph_ctx` default `producedItems` 5 → **2** (total 2).
- `query-projection-contract.v3.md` line 136 appends the produced-prefix basis and page slice. Line 140 appends the cursor meaning and "lower-bound only from a reached cap; an intermediate lower-bound page is a full page of a capped prefix".

**Executed owner controls (`queryOwnerControls`).**
- 5 units with test cap 3 and page size 2: page 1 is 3/3 lower-bound, truncated-page, 2 rows with a cursor; page 2 is truncated-bound, 1 row, no cursor. Both are lawful under the report page law.
- Exact paging of the same 5 units under public bounds never yields lower-bound.
- The **100,001-fact operation** under public bounds: page 1 and the continuation page 2 are each 100000/100000 lower-bound, truncated-page, 2 rows with a cursor, and lawful.
- The fixture before-shapes are refused; the after-shapes are lawful.

The page law still refuses every earlier contradiction (G1–G6, S2 of review-03).

### RPR5-3 (required): interruption detail rule — corrected with a ledger join

**New `J-ENV-INTERRUPTION-DETAIL`.** A `kind=failure` interrupted envelope is admitted only when joined to this invocation's recorded steps. Its `errors` must equal **exactly the in-step-order list of recorded request-rejected/operational-failed `domainDetail`s** (`report_model.recorded_failure_details`).
- Invented, changed, reordered, extra or unjoined details are refused.
- Skipped-step terminations carry no detail and contribute none.
- A composed route detail counts only if the host persisted it in `StepTermination.domainDetail`.
- `errors=[]` stays envelope5 `SCHEMA-ENV` and pending (envelope6 not adopted).

Report documents pass their ledger steps. `failure_envelope` composes interruption errors from recorded details.

**Envelope cases:**

| Case | Outcome |
|---|---|
| real recorded `CONFIG.INVALID` (reviewer I1) | accept |
| two real details in step order | accept |
| remedy changed | refused |
| unrecorded detail | refused |
| real plus invented | refused |
| reordered | refused |
| no ledger join | refused |
| skipped termination given a fake detail | refused |
| empty errors | `SCHEMA-ENV` |

**Delivered goldens** (× human/json/agent/html; envelope5-admitted with the join):
- fit analysis rejected, query skipped, SIGINT during the required render;
- review-brief query failed (`evidence.missing`), SIGTERM;
- audit pivot rejected and primary failed, SIGINT: `errors` holds 2 details in step order.

**Report cases.** An invented detail → `J-ENV-INTERRUPTION-DETAIL`. A real detail passes the envelope join and is then refused `J-LEDGER-AGGREGATE`, because a delivered report cannot carry an interruption.

**Still pending.** The 8 pending goldens for the empty form (no earlier detail) are still not counted as delivered. RP-OBL-C01's register text is updated to this law.

### Advisories

| Advisory | Disposition |
|---|---|
| A1 scratch alias | Corrected (§1): the exemption applies to the resolved target only. |
| A2 continuation position | Admission embeds first pages only (position 0 bound by the cursor join). Continuation relabels stay a host assertion (`response-is-owner-admitted-query-result`). The owner controls exercise continuation law. |
| A3 L01/K01 | Kept as recorded: L01 non-blocking, K01 blocking the coverage owner; neither waives a feature. |
| A4 C01 tracking | Kept; the invented-detail pending golden is now ledger-joined. |
| A5 cancellation Run selection | Required-only kept (current owner model). Successor03's optional-commit change is **RP-OBL-C02**, pending integration and blocking M1. No bound html variant plans an optional analysis, so no report ledger differs today. Profile workflows are still not exercised. |
| A6 hard links/native/TOCTOU | Outside the claim. |
| A7 RP-DO-12, G01 | Open. |

## 3–9. Carrier law (unchanged unless noted)

- **Fit successor, envelope5 host admission:** unchanged except `J-ENV-INTERRUPTION-DETAIL`.
- **Report document, panels, disclosures, provenance:** unchanged. Ledger provenance now verifies `generic-step-dag-law`, `steps-equal-a-plannable-builtin-planning-variant`, `run-id-produced-by-primary-analysis-step` and `skipped-records-supported-by-dependencies`, and host-asserts `planning-variant-condition-held`.
- **D9, skipped and cancellation:** owner reference model unchanged. A delivered report still requires cancellation phase `none`.
- **Graph page law:** eager owner law (§2 RPR5-2).
- **History:** unchanged; recent-only.
- **Codec:** `documentMaxBytes` **27,828,318** (the ledger bound grows with `planVariant`, `planRole` and `dependencyGate`: audit 19,436,268). Structural bounds only; codec record bound RP-OBL-L01.

## 10. Obligation register

| Id | Kind | Standing |
|---|---|---|
| RP-DO-01, 03..12 | report design blockers | proposals to owners; open |
| RP-DO-02 | conditional, not selected | holds no row open |
| RP-OBL-C01 | envelope/workflow owner | pending integration, blocks M1: empty pre-Run interruption form; real recorded details now delivered |
| RP-OBL-C02 | workflow owner | pending integration, blocks M1: cancellation Run selection successor03 |
| RP-OBL-K01 | coverage owner | pending successor, blocks M1 |
| RP-OBL-P01 | command/workflow owner | pending decision, non-blocking: analyze import planning; review issue on the analyze coverage row |
| RP-OBL-L01 | invocation record owner | pending statement, non-blocking |

Other obligations: B01, B02, H01, M01, G01, E01.

## 11. Coverage and overrides

- **Coverage:** RP-OBL-P01 is added on `commands:analyze`; the C01 rows are unchanged. The full owned validator gives unscoped base/overlay "Missing/extra module milestone prerequisite", and scoped valid/valid.
- **Overrides:** the seven passage overrides are unchanged. The query fixture and prose corrections are separate conditional proposals to the query owner.

## 12. Evidence and limits

**`check.py` verifies:**
- closure, alias probe and bytecode demonstration;
- regeneration of 10 owner outputs and fixtures;
- restorations including the steps description, the 43 metadata cases and the in-process accepted checker;
- coverage and register;
- builtin planning against the owner `validate_dag`;
- owner query paging controls and the fixture correction;
- 22 aggregate cases, 64 delivery goldens (16 scenarios), 8 pending goldens and 17 static-parity goldens;
- **31 envelope cases:** 9 accept, 9 schema, 13 host admission;
- **184 report cases on 17 bases, each with its exact code:** 28 accept, 29 schema, 15 codec/boundary, 16 envelope host, 43 ledger, 29 graph, 24 other;
- graph controls, byte law, worst-case sizes and codec reachability.

**Limits:**
- The planning record is a proposal. Its sources are owner cases and prose; no owner has accepted it. Pivot planning conditions are host-asserted.
- `validate_dag` ran on spec-derived step specs with binding params only; full StepSpec params schemas were not exercised.
- `run_invocation` was not re-executed this round; review-05 executed it on fit shapes.
- Owner query controls use `traverse_projected_graph`, which shares `finish_operation` with `execute_graph_query`. A full retained-run `execute_graph_query` replay was not repeated here.
- Fixtures and the mock graph owner are constructions.
- This is not browser, renderer, generator, performance or product qualification.
