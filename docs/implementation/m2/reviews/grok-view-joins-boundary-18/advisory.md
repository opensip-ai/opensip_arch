# Advisory: view / coverage / fact joins (next owner after Coverage producer)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded next-owner map over the selected `open_run_closure` **per-view** block. **Not ACCEPT-DESIGN-UNIT. Not frozen source. Not full Run. Not producer-17 or guards-16 source acceptance.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-view-joins-boundary-18/review`. No live/frozen/history edits.

Selected identity `619d6e3c…41e6` / 158555; selected native `e6784aa1…e2b9` / 319944. Live lock independently **14 inventory / 18 contract**. Producer-17 and capability-support-16 remain **local owners** this block **calls**; they do not see a second scope.

## Actual call trace (`open_run_closure`, not nearby helpers)

After walk (1650), Plan-native (1689–1749), `UNIVERSE_FRAME_UNRETAINED` (1750–1755), policy, stages (1788–1794), and proof/finding/predicate joins (1809–1852):

**Census immediately before the loop (callers 1809–1812):**

- `EVALUATION_VIEW_ROOTS`: `evidence.viewIds` == view ids derived from `proof.evaluationInputRefs` domain `view`.
- `EVALUATION_COVERAGE_ROOTS`: `evidence.coverageIds` == union of those views’ `coverageIds`.

This owner does **not** walk the proof bundle. It **consumes** those already-joined sets (especially `evidence.coverageIds` for `VIEW_COVERAGE_JOIN`).

**Per `evidence.viewIds` (1853–1948), in this order:**

| Line | What actually runs | Refusal |
| ---: | --- | --- |
| 1855–1856 | view `planId` / `producerClosure` ∈ `plan.semanticClosures` | `VIEW_PLAN_JOIN`, `UNSELECTED_PRODUCER` |
| 1857–1862 | **every** named scope: snapshot, enumerator selected, enumerator kind | `SCOPE_SOURCE_JOIN`, `UNSELECTED_ENUMERATOR`, `ENUMERATOR_CLOSURE_KIND` |
| 1875–1892 | partition disjointness over **all** `view.scopeIds`, including scopes **with no Coverage** | `SUBJECT_SCOPE_PARTITION_OVERLAP:<relation>@<rung>:<utf-8-byte-min subject>` |
| 1893–1905 | each `view.facts`: snapshot/producer; **existential** fact/scope join; snapshot inventory digest + byte range + UTF-8 of prefix and span | `FACT_SOURCE_PRODUCER_JOIN`, `FACT_SCOPE_JOIN`, `ANCHOR_SOURCE`, `ANCHOR_RANGE`, `ANCHOR_UTF8` |
| 1906 | each `view.coverageIds` ∈ `evidence.coverageIds` | `VIEW_COVERAGE_JOIN` |
| 1913–1916 | **every** retained scope `_rung_index` (native 765–767), Coverage or not | `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER:rel@rung` |
| 1917–1919 | coverage wrapper `scopeId` ∈ **this** view | `COVERAGE_SCOPE_JOIN` |
| 1925–1928 | `payload_of_coverage`; `unresolved_edge_payloads(view)` → `{relation,referrer,edgeKind}` of **this view only** | registered-payload / relation-payload faults |
| 1932–1937 | dialect table from **retained** `native_universes[scope.sourceUniverse][2]` (None if absent); **call** `admit_coverage_result_v3` (producer-17) | `COVERAGE_PRODUCER_ADMISSION:…`, `COVERAGE_ADMITTED_IDENTITY` |
| 1938–1947 | **call** 16-guards, most-specific first: dialect, syntax, source-variant | those guards’ names |
| 1948 | `coverage_inventory_totality` (1255–1296) | `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:<path>` |

**Not called here:** `coverage_view_use` (native 1628); `subject_scope_descriptor` (native 1499); `completeness_from_stage` (native 1358); Plan-native counts; caller ADMIT.

**Not this block (do not pull in by helper proximity):**

- `anchor_law` / `FACT_ANCHOR_CARDINALITY` (1245–1254) — runs in `relation_payload_rules` during **walk**, before 1853.
- `syntax_capability_supported` / `body_identity_join` — walk-time fact payload.
- Findings/predicates (1822–1852), imports (1951+), policy, `close_run` replay.

## Laws this owner must read, not restate

**Partition** (`relation-payload-v2` `coveragePartitionLaw`): key `snapshotId, relation, resolution, sourceUniverse, targetUniverse`. Same-partition `subjects` pairwise disjoint. Different partition ⇒ same subject lawful. Empty subjects lawful. Two **views** may share a scope. Overlap report: UTF-8 **byte** min, not canonical-JSON order. Registry: **internal** refusal; **no** DomainDetailCode / D9 row (`refusalShape` 88–89).

**Totality** (`file` `coverageTotality` only, rung `enumerated`): if `entry.coverage==complete`, every **scope subject that is in snapshot inventory** must have a **view** `file@enumerated` fact whose payload `path` is that subject **and** that agrees on `matchOn` (same five fields). Other-universe facts do **not** discharge. `unknown` / non-inventoried subjects / `package` / `vcs-change` owe nothing. Honest completeness: an inventoried missing file under `complete` refuses; under `unknown` it does not.

**Fact/scope join (1896–1897)** is **existential** over `view.scopeIds` on `relation, resolution, sourceUniverse, targetUniverse` only (not `snapshotId` here; walk already forced `REFERENCE_SOURCE_JOIN`). Totality is **stricter** on the same coordinates plus snapshot.

**Unresolved view membership (1799–1807, used 1927–1928):** only `view.facts` with `relation==unresolved-edge`, after `registered_payload`. Producer bijection must **not** receive another view’s edges or a Run-global bag.

**Ladder (1913–1916):** `_rung_index` on **retained** scope bytes. Unregistered pair (e.g. `unresolved-edge@enumerated`) refuses **here** even with no Coverage — producer RC-0 is not this scope’s only check.

**Dialect (1932–1933):** `body_eligibility_table` on the **retained universe row**, never payload. Missing `native_universes` entry ⇒ `None` (producer skips its source-path slice; 16 source-variant still runs). `UNIVERSE_FRAME_UNRETAINED` (1755) is the earlier census that facts/scopes’ universes were retained; this owner must not invent frames.

## Recommended bounded Rust owner

Sibling of `coverage.rs` / `capability_support.rs`, **not** inside either (producer cannot see a second scope; guards are per Coverage).

```
inspect_view_joins(
  inputs,                    // retained objects+blobs+schema
  view_id,
  evidence_coverage_ids,     // already-joined EVALUATION_COVERAGE_ROOTS set
  native_universe_rows,      // retained universe descriptors keyed by bare hex (from walk/plan-native)
  snapshot_inventory,        // retained snapshot.sourceInventory
  work,
) -> Result<ViewJoinChecks, ViewJoinError>
```

`ViewJoinChecks` is diagnostic counts/ids only — **not** ADMIT, **not** PlanNativeChecks, **not** CoverageAdmission as a token. Internally, in the table order above:

1. well-formedness of view + every named scope
2. partition over every named scope
3. facts: producer/snapshot, existential scope join, inventory anchors
4. `VIEW_COVERAGE_JOIN` then every-scope ladder
5. each coverage: `COVERAGE_SCOPE_JOIN`; **call actual** `admit_coverage_result`; **call actual** 16-guards; totality

No new crate/edge. Read `coveragePartitionLaw.partitionKey` / `file.coverageTotality` from the pinned relation-payload document; do not copy the key into a second table. Optional kebab extract only if a closed byte pin of those two rows is required — default is **read the selected schema**.

Identity later remains the Run caller (same pattern as `inspect_plan_native` / producer).

## Fixtures (order-sensitive)

| Case | Expect (internal name) |
| --- | --- |
| Two scopes, same partitionKey, intersecting subjects | `SUBJECT_SCOPE_PARTITION_OVERLAP:rel@rung:<utf8-byte-min>` **after** enumerator faults, **before** facts |
| Same subject, different `sourceUniverse` | no partition refusal |
| Scope with **no** coverage, overlapping same partition | still overlap (producer never runs) |
| Empty `subjects` | partition ok |
| Same scope id in two views | not overlap |
| Unselected enumerator | `UNSELECTED_ENUMERATOR`, not overlap |
| `unresolved-edge@enumerated` retained scope, no coverage | `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER` at 1913, not producer RC-0 |
| Coverage `scopeId` not in `view.scopeIds` | `COVERAGE_SCOPE_JOIN` |
| `view.coverageIds` ⊄ `evidence.coverageIds` | `VIEW_COVERAGE_JOIN` |
| Fact universes match **some** scope, not the file-complete one | `FACT_SCOPE_JOIN` ok; totality still omits if `matchOn` fails |
| `file@enumerated` complete, inventoried `a.ts`, no matching-universe file fact | `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH:file@enumerated:a.ts` **after** producer ADMIT + 16-guards |
| Same, `coverage=unknown` | no totality |
| `package@manifest-declared` complete empty facts | no totality row |
| Unresolved-edge fact in **other** view only | not in this view’s bijection bag |
| Anchor path missing / digest mismatch / `start>end` / non-UTF-8 span | `ANCHOR_SOURCE` / `RANGE` / `UTF8` |
| Schema-valid Coverage, wrong `subjectCount` | `COVERAGE_PRODUCER_ADMISSION:` + producer refusals/faults (call **actual** 17) |
| PlanNativeChecks `{1,1}` as partition proof | **must not** satisfy overlap |

## Internal causes vs public routing

Partition `refusalShape` (88–89): **internal admission refusal; no public DomainDetailCode; no D9 class/exit/code**.

`VIEW_COVERAGE_JOIN`, `COVERAGE_SCOPE_JOIN`, `FACT_SCOPE_JOIN`, `ANCHOR_*`, `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER`, `COVERAGE_INVENTORY_TOTALITY_OMITS_PATH`, `COVERAGE_PRODUCER_ADMISSION` are identity `AdmissionError` strings. They are **not** `native.coverage-bijection-mismatch` (that DomainDetail is host operational routing for **producer REFUSE**, advisory-17 followup). Do not `public_termination_for` these identity names. Host presentation of view-join failures is a **later** D9/exit-contract obligation unless a row already names them (none in §10 for partition/totality).

Producer REFUSE inside this owner still wraps as `COVERAGE_PRODUCER_ADMISSION:` then host maps that **class** per 17-followup (`PROVIDER.PROTOCOL_VIOLATION` / operational record). Totality/partition stay identity-internal until a later unit publishes a public row.

## What remains full graph

Walk + fact payload (`anchor_law`, syntax-supported, body join); Plan-native census/bind/grant; `UNIVERSE_FRAME_UNRETAINED`; policy/waivers/rule program; stage-spec/output schema; findings, predicate proofs, witness addresses; import/mapping; `close_run` evaluator replay. This owner is one view’s retained joins + calls into 17 and 16.

## Verdict

**NOT ACCEPTANCE.** Next bounded evaluator owner is **per-view joins** (`inspect_view_joins`): partition, fact/anchor joins, coverage membership, retained-scope ladders, unresolved-edge bag, then **actual** producer + 16-guards + inventory totality. No caller ADMIT or count tokens. Suggested files: `crates/evaluator/src/view_joins.rs` (no restated partition table).
