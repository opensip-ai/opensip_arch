# HydraDB proposals — independent Grok coauthor query assessment

**Standing.** Read-only coauthor scope selection over frozen evaluator3 candidate **source23**. Not a new independent ACCEPT. Frozen23 has a separate actual-Grok ACCEPT; independent blind-10 is still running and is not this document. No source23 bytes, root application tooling, active blind output, or repository were edited. Output is only this directory.

**Subject.** Manifest `/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v23.json` SHA-256 `652c800166a8d3f37eacfbf273c9786bb84f6fd6b5c6ead57b5a254315859a25` (3068633 bytes, 12391 files). Snapshot `/tmp/opensip-design-corrections/candidate-subject.v23`. Independently re-hashed; matches the published manifest.

**Inputs.** Codex subagent `/tmp/opensip-hydradb-proposals-review.v1/assessment.md`. Local proposals `docs/coop/hydradb-review/` (not applied). All five product-contract hashes cited by those proposals **differ from source23** (`input-evidence.json`). Assessment uses current v23 owners, not source21 summaries.

**Verdict.** `AGREE_BOUNDED_QUERY_SUCCESSOR`. Most of the eight proposals are already owned. No HydraDB adoption, new authoritative store, or distributed service. One small public-query successor is warranted **before implementing** `graph.neighbors` / `graph.path` / `graph.reach`. Q1 and Q2 are MUST for those three operations. Q3 is SHOULD before agent-facing caller/impact output. This does not reopen sealed evaluator, native absence, or storage generations, and it does not change historical source23 ACCEPT.

---

## 1. What is already covered (checked on v23, not restated from source21)

| Claim | Exact v23 owner | Independent check |
|---|---|---|
| Native negative knowledge ≠ zero stored edges | `native-evidence.md`; `atom-evaluation-contract.v1.md` §§1–4 (incoming owed programs, `completeSearch` cannot override partial Coverage, `examinedExhaustive=false` never proves complete search) | Already a design feature. Query must cite it, not duplicate it. |
| Exact historical replay | `identity-and-evidence.md` ~1430–1468: `close_run` complete replay; equal counts/verdicts insufficient; new source/policy is a new Run | Covered for retained Runs. Proposal 2’s old-view *examples* are useful query goldens, not a missing custody model. |
| Immutable derived-index generations, crash, purge, project isolation | `06-evidence-and-persistence.md` GX-02/04 lines 134–168; identity §5 availability/purge ~1536–1577; `04-fact-plane.md` GX-01 lines 261–292 | Covered. Stale generations serve no new query; missing/corrupt acceleration never means “no edge.” Dense IDs are generation-local. |
| Map / import / advisory separation | workflows §§4–6, §8 `AdvisoryOperation` = only `comparison.diff`, `candidate.list`, `inspection.show`, `review.brief` | Covered. Graph ops are **not** in that enum. |
| Backend independence | Fact-plane exact-accelerator vs semantic producer; admission/qualification dependency obligations | Covered. CSR/GraphBLAS/SQLite indexes remain private optimization. |

**Proposal dispositions (independent):** 1 record a short decision-register note (no new gate). 4/7 already owned; optional implementer join text only. 5 optional borrow-register row, non-authoritative. 6 cross-reference existing workflows/atom law plus Q3. 8 measurement under existing G13/GX-09 — no performance finding here. Hydra fit-gap external claims were **not** re-audited.

Reject: numeric DB IDs as subjects; backend default order as public law; zero rows as absence; copied graph as purge custody; live deltas as sealed evidence; graph TX as OpenSIP commit.

---

## 2. Q1 — public graph selection and result units — **MUST** (scoped)

**Not already settled.** Schema title/description claim “parameters are closed per operation.” The schema implements one all-optional `Params` object. Independent probes (all `schemaAdmitted: true`):

- `graph.path` with `params: {}`
- `graph.neighbors` with only irrelevant `baselineId`
- `graph.path` / `graph.reach` with `subject`/`target` as `LogicalPath` only
- `graph.path` with `view: {snapshotId}` only
- `graph.path` with `view: {latest: true}`

`workflow_projection_model.v3.py` owns `query_finding` for `findingId`/`fingerprint`. There is **no** graph-operation admission helper. `workflow-cases.v1.json` `graph.reach` rows only exercise `QUERY.COMPLETENESS_UNMET` as an invocation observation (items 100000, truncated). They do not choose neighbors vs path vs reach result units.

**Existing law that does settle part of Q1 (GPT underweighted this).** `04-fact-plane.md` GX-01: a depth bound is **query semantics**; a response that stops at a bound must not present a truncated reachable set as exhaustive. `maxDepth` is therefore not a free work cutoff. That still does not choose result units, cycles, or endpoint identity.

**Counterexample A — two facts, one pair.** Admitted `fact2` `f1` and `f2` both join subject A→B at `calls@resolved-callee` with different provenance. Returning `{B}` once vs two relationship rows are both deterministic and disagree on `totalItems` and pagination. Native identity is `fact2`; collapsing to unique subjects is a **choice**, not implied by “deterministic.”

**Counterexample B — two TS program universes, same path.** Atom contract §1: *E* = (*U*, *K*, *N*). A Run may carry two TypeScript program universes that both contain `src/a.ts` with different callees. Params `subject: "src/a.ts"` does not select *U*. Snapshot-only view is weaker still: multiple Plans/Runs may analyze one `snapshot2`. RunId is necessary and not sufficient.

**Counterexample C — cycle.** A→B→A. `graph.reach` from A may be `{B}` or `{A,B}`. `graph.path` A→A may be empty, the cycle, or all simple cycles. Schema is silent.

**Minimal remedy (chosen, not “owner should define”).** See §5 table. Scope **only** `graph.neighbors|path|reach`. Do not reopen `finding.show` (already `query_finding`). Physical traversal/CSR remains free if parity with canonical fact-view walk is exhaustive for the declared query (GX-01).

---

## 3. Q2 — continuation bind — **MUST**; response `latest` is also MUST-to-fix schema

**Partial existing law.** `View.latest` description: resolver, never authority; empty domain `IDENTITY.UNKNOWN` (workflows §8). GX-02: a query pins one active generation **for its duration**. Identity: purged/unavailable proof cannot become no-match.

**Not settled.** GX-02 “duration” is one in-process query, not a later CLI/MCP request that resubmits `latest` plus a cursor. Cursor is an unconstrained 1..256 string. `GraphQueryResponseContext.resolvedView` `$ref`s request `View`, so `{latest: true}` is schema-admitted (probe `response-latest-still-unresolved`). That **contradicts** the same schema’s latest description. This is not a standalone-schema false positive: the `$ref` is the defect.

**Disagreement with the Codex subagent.** It treated “response must carry a concrete resolved ID, therefore resolving an old-view request to today’s graph is already forbidden” as enough to make the schema issue SHOULD. Per-response prose does not bind **page 2**. A first `latest` request can resolve Run A rows `[a,c]` and return `a` plus cursor; after Run B `[b,c]` a second `latest`+cursor can yield B’s second row. Each page names a concrete Run; the collection is not one historical answer.

If every request already carries `runId`, re-resolution of `latest` is avoided, but the cursor still must bind operation, effective params, order, and position or a client can resume `graph.path` with a `graph.neighbors` cursor.

**Counterexample D — page fullness vs exhaustion.** Probe `truncated-zero-total-with-cursor` is schema-admitted: `truncated=true`, `totalItems=0`, cursor present. Existing law does not say whether `totalItems` is the full selection, items emitted before a work bound, or the current page. An empty next-cursor must not prove native closed-world.

**Minimal remedy.** Opaque host cursor bound to `(projectId, runId, factViewSelection, operation, canonical effective params/order, position)`. Continuation reuses that selection or refuses. Never re-resolve `latest`. Split request `View` (may include latest/snapshot) from response `ResolvedView` (`runId` only for graph.*). Keep bounds 1000 / 100000 / 64 / 1000000 and `QUERY.COMPLETENESS_UNMET`.

---

## 4. Q3 — traversal completion vs native sufficiency — **SHOULD**

Native already permits complete examination with incomplete resolution (atom §4; RC-1/RC-2). Query `coverage` is a three-token enum that **name-collides** with native CoverageResult. `coverage=complete` plus zero neighbor rows can be misread as “no callers” while an unresolved dynamic edge keeps incoming use unknown.

Graph operations are unsealed (schema: never seal a Run) and **not advisory** under the closed `AdvisoryOperation` enum. Probe `advisory: true` on a graph response is schema-admitted because `advisory` is a free boolean, not cross-joined to the operation. Reclassifying all graph queries as advisory would be a product change, not a disclosure fix.

**SHOULD** before exposing caller/impact to agents: a separate traversal-completion token plus citations to existing Coverage/deficiencies. Do **not** mint a parallel absence evaluator. Any absence claim remains a host-derived native/atom result.

---

## 5. Chosen minimal public law (small table)

Owner of the successor: **workflows chapter §8 Query** (root normative) + **evaluator3 `graph-query` schema major 3** + **workflow projection/reference** (admission of request/response/cursor; no `close_run` change). Physical index/CSR/GraphBLAS stay GX-01 private.

### 5.1 Operations (only these three)

| Operation | Required selectors | Required params | Forbidden params | Result unit | Order | Cycle / duplicate | Path selection |
|---|---|---|---|---|---|---|---|
| `graph.neighbors` | `projectId`; request view; **effective `runId`**; fact-view selection (explicit `view2` digest set **or** “all admitted views of this Run at `relation@minResolution`”); `universe` if more than one matching program universe | `relation`; `minResolution` (rung); `direction`; **endpoint** as native identity (below) | `baselineId`, `fingerprint`, `findingId`, `otherRunId`, … | one row per distinct admitted `fact2` (relationship + provenance), not unique subjects | `(source subject3, target subject3, fact2)` utf-8 | same `fact2` once; two provenances = two rows | n/a |
| `graph.path` | same | neighbors plus **two** endpoints; `maxDepth` (semantic hop bound, GX-01) | same | one **simple path** = ordered `fact2` sequence | among tied shortest paths, least `fact2` id sequence | no repeated subject except optional close if start=end | **one shortest** by hop count; not all-paths |
| `graph.reach` | same | one start endpoint; `relation`; `minResolution`; `direction`; `maxDepth` | same | distinct evaluation-subjects reachable | `subject3` utf-8 | start **excluded** unless `includeStart=true` (default false) | membership, not paths |

**Endpoint (reuse native, no global DB id).** `{universe, kind, nativeSubjectId}` plus `packageManifestPath` when `kind=package` (atom §1). LogicalPath-only `subject`/`target` is request-rejected when it does not uniquely determine that tuple (`REQUEST.PRECONDITION_FAILED` / `QUERY.ENDPOINT_AMBIGUOUS` — new DomainDetail, same appendix pattern as `REPAIR.TARGET_*`). Ambiguous two-universe same-path: refuse; do not union.

**Fact-view selection.** Default: all admitted `view2` of the resolved Run whose scopes match the named `relation@minResolution`. Caller may narrow to explicit view digests. Silent “newest provider” is forbidden.

**Request vs response view.** Request `View` may be `{runId}|{snapshotId}|{latest:true}`. For **graph.***, `snapshotId` and `latest` are resolvers only. Response `ResolvedView` is `{runId}` only. Snapshot-only graph execution without a unique Run is `IDENTITY.UNKNOWN` / empty domain, same as unresolved latest.

### 5.2 Cursor and bounds

| Field | Chosen law |
|---|---|
| Cursor | Opaque host token. Binds `projectId`, concrete `runId`, fact-view selection, operation, canonical effective params+order, position. Implementation may rebuild the exact view and resume by canonical offset. |
| Continue | Reuse bound selection or refuse `REQUEST.PRECONDITION_FAILED` / `QUERY.CURSOR_MISMATCH`. Never re-resolve `latest`. Expired/unavailable view uses existing `evidence.{expired,purged,missing}` / availability routes. |
| Page fullness | `page.size` items or remaining units, whichever is smaller. Full page ≠ search exhausted. |
| Work / semantic bound | `maxDepth` semantic. `maxVisitedNodes` / `maxItemsPerOperation` work. Required completeness at either → `QUERY.COMPLETENESS_UNMET`. Best-effort → `truncated=true` + cursor if more semantic units exist. |
| `totalItems` | Count of result units in the **bound selection actually produced** before a work bound; not page size. When truncated by a bound, `totalItems` is that produced count, not a claimed universe cardinality. |
| Empty `nextCursor` | No further **result units** under the bound selection. Not native closed-world / no-callers. |

### 5.3 Q3 response disclosure (SHOULD, same schema bump if done together)

| Field | Law |
|---|---|
| `traversalCoverage` | `complete` (all result units under semantic maxDepth listed or paged) / `truncated-page` / `truncated-bound` |
| `evidenceSufficiency` | optional projection: native Coverage ids + evaluation-deficiency citations for the implied incoming/outgoing question, or omit when the caller did not ask an absence question |
| `advisory` | **false** for graph.* (schema join to operation; not a free boolean) |

Do not let `coverage: complete` mint “none” callers.

### 5.4 Faults (reuse, two new details)

| Condition | Route |
|---|---|
| Bound under `completeness=required` | existing `QUERY.COMPLETENESS_UNMET` (indeterminate, exit 3) |
| Unresolved latest / no Run for snapshot | existing `IDENTITY.UNKNOWN` / empty domain |
| Ambiguous or missing graph endpoint | `REQUEST.PRECONDITION_FAILED` + **new** `QUERY.ENDPOINT_AMBIGUOUS` |
| Cursor mismatch / param change | `REQUEST.PRECONDITION_FAILED` + **new** `QUERY.CURSOR_MISMATCH` |
| Purged/expired proof bytes | existing `evidence.{purged,expired,missing}` |
| Accelerator miss | GX-02 exact fallback; never empty-success |

Register the two DomainDetailCode members in evaluator3 `common:3` and the public-detail-registry appendix. Do not add a D9 family.

---

## 6. Isolation and freeze

These laws isolate to:

- `workflows-and-surfaces.md` §8 Query (root chapter; this assessment does not edit it)
- `schemas/evaluator3/graph-query.schema.json` major **2 → 3**
- `workflow-projection-contract.v3.md` query subsection + a small admission helper in `workflow_projection_model.v3.py`
- goldens under workflows checker (not `close_run` mutants)

Keep unchanged: native incoming/absence, identity `close_run`, execution-inputs, persistence GX-02 generations, sealed evaluator composition. Historical source23 ACCEPT is not rewritten. Successor review is a **new** bounded subject (query schema/projection + §8 paragraph), not a silent patch to frozen23.

`command-inventory.v3.json` still advertises `opensip query OPERATION [--view run2:...]` while evaluator3 RunId is `run3`. That is existing inventory drift, out of HydraDB scope; do not hide it, do not expand this successor to rewrite the whole inventory.

---

## 7. Alignment with the Codex subagent

**Agree:** no HydraDB; most of 8 already owned; Q1/Q2 before implementing graph ops; Q3 disclosure not a new evaluator; schema probes are not product acceptance; physical CSR/GraphBLAS freedom; no global DB ids; graph ops not advisory.

**Disagree / tighten:**

1. Q2 response-`latest` is a **MUST schema join**, not SHOULD. The `$ref` admits what the description forbids.
2. Proposal 2 is **partially** owned (replay/cache/isolation yes; multi-request continuation no). Do not file it as “already covered.”
3. GX-01 already makes `maxDepth` semantic; Q1’s remaining MUST is endpoint identity, result unit, cycle, path-selection, fact-view/universe selection.
4. Q1 applies to **three graph operations**, not the other 17. `finding.show` is already owned.
5. `coverage` enum name-collision with native Coverage is part of Q3 and should be renamed or split (`traversalCoverage`) rather than overloaded.

---

## 8. Required new review scope (if the successor is accepted)

- New frozen bytes: evaluator3 graph-query major 3, projection admission helper, §8 Query paragraph, two DomainDetail members, goldens for counterexamples A–D plus two-page A→B publication, changed-param cursor refusal, cache-loss continuation, at/over bound, two-universe path refusal, dual-provenance neighbors.
- Reviewers: same coauthor set; **not** a re-review of sealed evaluator/native/storage.
- Explicitly out of scope: HydraDB dependency, CSR recipe, FactViewId byte grammar (still parked), command-inventory v1/v3 full rewrite, source23 historical ACCEPT.

Passing schema probes or this assessment does **not** establish complete admission or product qualification.
