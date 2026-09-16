# Report evidence design candidate (author-01): RP-DO-03, RP-DO-05, RP-DO-09, RP-DO-10

## 0. Standing

This is an **author candidate** for actual separate review and root acceptance. It is not approval.

**Parent.** The unaccepted report candidate `/tmp/opensip-implementation/m1-report-projection-subject-05`, outer manifest `a9f6c22a…a2de4`. Its bytes are never edited; `check.py` verifies the outer manifest and every parent file it reads.

**Scope.** Four report feature owner gaps: coupling importer package membership (R08), entry-point recognition (R12), symbol metrics (R07) and test reachability (R07). The other seven feature obligations (RP-DO-01, 02, 04, 06, 07, 08, 11, 12) and every integration obligation of subject-05 are separate work and are not changed.

**Readiness:**

| Scope | State |
|---|---|
| Design of the four features | Candidate. Each has a delivered report carrier, owner joins and a reference model with positive and adversarial fixtures. |
| Owner successors S1–S4 (§7) | Proposals. No owner has accepted them. |
| Remaining blockers for these four | None found. Acceptance of S1–S4 is a dependency, not a blocker. |
| Not claimed | No runtime, browser, generator, performance or Run replay evidence. |

## 1. Subject, closure and how to check

**Subject.** `subject-files.json` lists every file and excludes only itself:
- **Code:** `reference_model.py`, `build_owner.py`, `build_fixtures.py`, `check.py`, `seal.py`.
- **Owner records:**
  - `owner/framework-recognition-plan.schema.v1.json`
  - `owner/report-projection-successor-patch.v1.json`
  - `owner/identity-parameter-registry-patch.v1.json`
  - `owner/evidence-design-successor.v1.json`
- **Data and documents:** `fixtures.json`, `source-pins.json`, `contract.md`.

**Run.** From the candidate directory:

```
TMPDIR=<existing absolute scratch> /tmp/opensip-implementation/metadata-reference-env/bin/python -I -B check.py \
  --architecture /Users/sb/code/opensip-ai/opensip_arch --subject-strict --out ../check-result.json
```

**Closure** (same trusted-reference claim as subject-05):
- **Pins.** Every governed read must be pinned in `source-pins.json`. Pins are verified before any external import and re-hashed at every open.
- **Loading.** Modules are compiled from verified source bytes; bytecode is never consulted, and the check includes a demonstration of that.
- **Child processes.** None are started.
- **Writes.** Only the declared `--out` may be written, and it may not be read.
- **Alias probe.** Spellings of the unpinned `docs/implementation/README.md` are refused before a byte is read.
- **External code executed:**
  - the accepted metadata checker's schema loader;
  - `foundation/canonical.py`;
  - subject-05 `report_model.py` (page law, subject3 minting, owner-ordered mock graph owner);
  - the `glob_match` function extracted by AST from the pinned `workflows_model.v1.py`.
- `seal.py` is an authoring tool that `check.py` never runs.

## 2. Challenge of the register's suggested mechanisms

| Obligation | Register suggestion | Why it is not taken as-is | Mechanism chosen |
|---|---|---|---|
| RP-DO-03 | Query owner coupling projection from retained `UnitMembershipV1` | Membership is workspace-granular: a Rust file belongs to the `cargo-workspace` unit, not to a package, and `#[path]` or shared files defeat directory inference (native §2.1: “`WorkspaceUnitV2` and `UnitMembershipV1` cannot supply this binding”). `SourceUnitOwnershipV1` is target ownership, not package ownership. | **Rust:** selected owning targets → declaring `markerPath` → first-party package inventory row. **TS/JS:** retained membership row → unit → its co-located `package.json` (U-1). Computed over a whole-view internal projection (S3); no public operation is added. |
| RP-DO-05 | Retain `FrameworkRecognitionV1.entryPoints` with the Run; query admits them as path starts | `entryPoints` is only `{state, source}`. The paths are per-unit recognized effects plus explicit configuration. Nothing binds a recognition to a unit or a Plan, yet FR-5 requires Plan visibility. | Per-unit `FrameworkRecognitionPlanV1` as an analysis-spec parameter (S2). Query start law unchanged: starts are admitted reachability origins whose native-attested path is in the retained effective entry set. |
| RP-DO-09 | Register metric relations | A stored metric relation would mint fact2/Coverage claims duplicating derived counts and would need its own totality law. | A closed catalog of five public graph operations over the exact endpoint, universe and fact-view. Each count is `exact`, `lower-bound` or `unknown`. |
| RP-DO-10 | Workflow/native test-reachability fact with import provenance | Imported `TestPayloadV1` has a free `testId` and an optional file `subjectPath` with no subject-under-test meaning. It is executed observation, “evidence, never Coverage”. A test name or path guess is not identity. | Exact native origins: Rust symbols on paths owned only by selected `test` targets, and TS/JS symbols of the unit matching a retained vitest-jest `testGlob`. Static reach uses public `graph.reach` and `graph.path`. |

## 3. RP-DO-03 coupling (`CouplingPanelV1`)

**Projection.** S3 is the whole-view `imports@resolved-target` projection under the query §8 closure:
- selected views; every projectable fact in fact2 order;
- reconciled target occupancy;
- the same `countBasis` and evidence disclosure.

It refuses on non-retained evidence.

**Importer attribution** (`World.symbol_attribution`):
- The importer is a symbol endpoint `(universe, nativeSubjectId)`.
- Its path is the `path` of the `SubjectInventoryV1` symbol rows whose `(cellOrdinal, programOrdinal)` binding names that universe. This is a native attestation.
- The `SubjectIdV1` spelling is never parsed.
- Causes when no single path is found:
  - `universe-not-plan-bound`;
  - `symbol-inventory-missing`;
  - `symbol-attribution-conflict` (two paths);
  - `symbol-inventory-incomplete` (not found in a partial inventory);
  - `symbol-not-inventoried` (not found in a complete inventory).

**Owner of a path** (`World.path_owner_keys`). No prefix, nearest manifest or spelling is used.

- **Rust.** Uses the universe's `SourceUnitOwnershipV1`:
  - `enumeration: partial` → `ownership-enumeration-partial`, decided before any row is read.
  - Rows are those whose `path` **equals** the path. None → `not-compiled-by-selected-targets`.
  - Rows are restricted to `selectedUnitIds`. None left → `owned-only-by-unselected-targets`.
  - Each selected target's `markerPath` must be a first-party package inventory row. Otherwise the cause is `package-inventory-incomplete`, `owner-manifest-not-package-inventoried` or `package-inventory-conflict`, and there is no fallback to another owner.
  - Several distinct manifests give several owners: `#[path]` shared files, e.g. `crates/core/src/shared.rs` owned by `core` and `app`.
  - A lib plus test target of one package is one owner.
  - `crates/app/src/vendored/util.rs` owned by `core`'s lib target belongs to `core`, not `app`.
- **TS/JS.** The retained `UnitMembershipV1` row must be `program-member` in `tsjs` with a unit. The owner is:
  - the first-party package `join(rootPath, "package.json")` when that path is inventoried (and must then have a package row);
  - otherwise the workspace unit itself.

  `packages/web-legacy` stays its own unit even though `packages/web` is a string prefix.

**Target attribution:**

| Target | Rule |
|---|---|
| `occupancy=unknown` | `unknown-occupancy` |
| `occupancy=external`, package | `external-package` owner (target side only) |
| `occupancy=external`, other kind | `external-non-package-target` |
| first-party package | The package row `(path, name)` must match exactly (`package-endpoint-inventory-mismatch` otherwise). |
| file | Owner of its path in the **target** universe (`file-not-inventoried` if the path is not inventoried). |
| symbol | Attribution then owner, in the target universe. |

Cross-universe targets therefore use their own universe's records.

**Carrier:**

| Member | Meaning |
|---|---|
| `owners` | Records keyed by `ownerKey = "owner1:" + sha256(C(key record))`: `first-party-package {path}`, `workspace-unit {markerPath}`, `external-package {universe, path, name}`. Cargo targets carry the `UnitIdentityV1` fields so `unitId` is recomputable. |
| `cells` | Directional `fromOwnerKey → toOwnerKey`. `facts` counts distinct fact2 (provenance duplicates stay distinct). `edges` counts distinct endpoint pairs. `importerSymbols`, `sharedImporterFacts`, `sharedTargetFacts` (a multi-owner fact is counted in each owner's cell), `internal`, `importerUniverses`. |
| `importerBuckets`, `targetBuckets` | Explicit unattributed facts by cause. A fact with an unattributed importer is only an importer bucket. |
| `totals` | `distinctFacts = attributedFacts + importerUnattributedFacts + targetUnattributedFacts`. |
| `absence` | `blankCellMeans: no-projected-fact` (const). `absenceSupported` ⇔ no blockers among `evidence-limitations`, `projection-lower-bound`, `unattributed-importers`, `unattributed-targets`. |
| `drilldown` | Includes test occurrences by default. `importerTestOrigin` feeds the visible filter state. Capped at 1000 with `drilldownProjection`. |

**Document joins:** `J-COUPLING-RUN`, `-OWNER-KEY`, `-CELL`, `-COUNT`, `-BUCKET`, `-TOTALS`, `-ABSENCE`, `-DRILL`.

**Host-asserted:** attribution, owner assignment, per-cell counts and occupancy. The reference host derivation refuses unlawful attribution with `J-COUPLING-OWNER`.

## 4. RP-DO-09 symbol metrics (`SymbolMetricV1`)

**Catalog** (closed). Each metric is one page-size-1 owner query over the subject endpoint:

| Metric | Operation |
|---|---|
| `distinct-resolved-callees-within-1-hop` | `graph.reach` calls outgoing, maxDepth 1 |
| `distinct-resolved-callers-within-1-hop` | `graph.reach` calls incoming, maxDepth 1 |
| `resolved-call-facts-incoming` | `graph.neighbors` calls incoming |
| `resolved-call-facts-outgoing` | `graph.neighbors` calls outgoing |
| `resolved-reference-facts-incoming` | `graph.neighbors` references@resolved-binding incoming |

**Reading law** (`metric_reading`):
- `native-evidence-unavailable` → `unknown`.
- `countBasis=exact` → `exact`; otherwise `lower-bound`.
- `value = totalItems`.
- `zeroSupportsAbsence` only when the reading is exact, the value is 0 and there are no limitations or deficiency citations.
- `interpretation` is const `static-projected-count`. A metric is never runtime hotness.

**Unknown readings:**
- A descriptor-not-retained subject → `unknown/subject-descriptor-not-retained`.
- Byte-budget omission is disclosed in `metricsProjection`.

**Joins:**
- `J-METRIC-REQUEST`: the request is recomputed from the catalog and the subject.
- `J-METRIC-RUN`, `J-METRIC-PAGE`: the subject-05 owner page law.
- `J-METRIC-ROWS`.
- `J-METRIC-STATE`, `J-METRIC-VALUE`, `J-METRIC-ABSENCE`.
- `J-METRIC-SUBJECT`, `J-METRIC-TOTALITY`.

Other metrics, such as size or complexity, need an owned native producer and a catalog successor.

## 5. RP-DO-05 entry points

**Parameter `FrameworkRecognitionPlanV1`** (`owner/framework-recognition-plan.schema.v1.json`):
- `{schemaVersion, snapshotId, membershipDigest, explicitEntryPoints, units[{unitOrdinal, rootPath, markerPath, recognitionId, recognition}]}`.
- Identity is raw SHA-256 of `C(record)`. It enters PlanId through `analysisSpecDigest`.
- The native records are copied and drift-checked; no `$ref` leaves the document.

**Admission joins:**

| Join | Rule |
|---|---|
| `J-FRP-SNAPSHOT` | `snapshotId` equals the Plan snapshot. |
| `J-FRP-MEMBERSHIP` | `membershipDigest` equals the `EnumerationPlanV1` membership digest. |
| `J-FRP-EXPLICIT` | `explicitEntryPoints` equals the committed `discovery.entryPoints`. |
| `J-FRP-ORDER` | Units are in strictly ascending `unitOrdinal`. |
| `J-FRP-UNIT-TOTALITY` | One row per rust or tsjs unit. |
| `J-FRP-UNIT` | `rootPath` and `markerPath` equal the retained unit. |
| `J-FRP-ID` | `recognitionId` equals `H(native.framework-recognition.v1, recognition)`. |
| `J-FRP-EVIDENCE` | Evidence path is inventoried and `contentSha256` equals the inventory digest. |
| `J-FRP-ENTRY` | Every entry path is inventoried. A unit-relative spelling such as `app/page.tsx` is refused. |
| `J-FRP-SUMMARY` | `entryPoints {state, source}` is recomputed by the native FR rule, with explicit configuration winning. |
| `J-FRP-BOUNDS` | FR-4 bounds. |

**Custody** (`recognition_custody`):
- No parameter → `not-plan-bound`, the historical profile. Nothing is inferred.
- Availability `expired`, `purged`, `corrupt` or `unavailable`, or `partial` with the parameter ref missing → `unavailable` with that availability.
- Otherwise `plan-bound` (`retained`, or `partial` with the parameter present).

The report is a snapshot of the observed generation.

**Effective entry set** (FR-2):
- Explicit `discovery.entryPoints` **replace** recognized effects.
- Otherwise the set is the recognized `effects.entryPoints` of the program's unit (cell `workspaceRoot` → unit).
- Recognized results are always retained as evidence.

**Trace law** (`derive_trace`, `EntryTraceV1`), for a planned symbol X:
1. `graph.neighbors reachability@from-resolved-calls incoming X`, page 100. `native-evidence-unavailable` → `unknown/reachability-evidence-unavailable`.
2. For each origin row in owner order: native-attested path, then membership in the effective entry set of the origin's universe.
3. The first matched origin is the start. `graph.path calls@resolved-callee outgoing start → X`, maxDepth 16, gives `path-found` or `path-not-within-bound`.
4. If no origin matches:
   - with a continuation cursor → `unknown/origin-page-set-not-embedded`;
   - otherwise `no-entry-origin` with counts, blockers (`entry-recognition-not-all`, `evidence-limitations`, `origin-attribution-unavailable`) and const `interpretation: …not-dead-code`.
5. Recognition `not-plan-bound` or `unavailable` → every trace is `unknown` with that cause.

**Joins:**
- `J-ENTRY-SUMMARY`, `J-ENTRY-ORDER`.
- `J-TRACE-REQUEST`, `-PAGE`, `-ROWS`, `-RUN`, `-SUBJECT`, `-TOTALITY`, `-STATE`, `-BLOCKERS`, `-AVAILABILITY`.
- `J-TRACE-START`: the start is an embedded origin row.
- `J-TRACE-ENTRY`: the entry path equals the attribution path. Explicit provenance needs an explicit count; recognized provenance needs a listed recognizer with entries and equal evidence.
- `J-TRACE-PATH`.

No browser heuristic is admissible: a `main`/`page`-named start is refused by the host derivation (`J-TRACE-ENTRY`).

## 6. RP-DO-10 test reachability

**Origin identity** (`derive_test_origins`, `TestOriginSetV1` per universe):
- **Rust** (`source: rust-test-targets`):
  - Origins are symbols whose attributed path's selected owners are all `targetKind=test` targets.
  - A path shared by test and non-test targets is not an origin (`shared-test-and-non-test-target-path`).
  - `completeness` is always `partial` with `in-target-unit-tests-not-identified`: `#[cfg(test)]` and `#[test]` inside lib or bin targets are not a target fact.
- **TS/JS** (`source: recognized-test-globs`):
  - The retained plan-bound vitest-jest recognition of the program's unit supplies the globs.
  - Origins are symbols whose retained membership row names **that** unit and whose unit-root-relative path matches a `testGlob` under `glob-pattern-contract.v1`.
  - Limitations that make the set `partial`: `recognizer-unresolved-choices`, `foreign-unit-paths-not-matched`, `symbol-attribution-conflict`, `symbol-inventory-incomplete`. Otherwise the set is `declared`.
- **No source** (`source: none`, cause required): `no-test-recognizer`, `recognition-not-plan-bound`, `recognition-unavailable`, `ownership-missing`, `universe-not-plan-bound`, `unsupported-language-family`.
- **Never an origin:** imported `TestPayloadV1` `testId` or `subjectPath`, symbol names, or file names.

**States** (`TestReachabilityV1`), for a planned symbol X:

| State | Condition |
|---|---|
| `is-test-origin` | X is an origin (with origin evidence). |
| `unknown/no-test-origin-identity` | The origin set is `none`. |
| `static-path-from-test-origin` | `graph.reach calls incoming X`, maxDepth 16, walked to the end. The witness is the least (depth, endpoint) origin; `graph.path` from origin to X is embedded. Interpretation: `static-calls-path-not-executed-coverage`. |
| `no-static-path-within-bound` | No origin reached, only when the reach is exact, there are no limitations and the origin set is `declared`. Interpretation: `…not-untested`. |
| `not-found-incomplete` | No origin reached, with blockers `reach-lower-bound`, `evidence-limitations` or `test-origin-set-partial`. |
| `unknown/calls-evidence-unavailable` | The calls view is unavailable. |

**Joins:**
- `J-TR-ORIGIN-SET`: glob sets must equal the embedded entry-recognition unit's vitest-jest recognizer and `recognitionId`; the Rust set is const partial with its limitation.
- `J-TR-ORIGIN`: glob retained, glob matches the relative path, attribution equals `rootPath` joined with the relative path, Rust `unitIds` ⊆ test targets.
- `J-TR-WITNESS`, `J-TR-REQUEST`, `J-TR-RUN`, `J-TR-PAGE`, `J-TR-ROWS`.
- `J-TR-STATE`, `J-TR-BLOCKERS`, `J-TR-SUBJECT`, `J-TR-TOTALITY`.
- `J-TR-SLICE`: a membership row that contradicts its unit root refuses.

## 7. Owner successors (`owner/evidence-design-successor.v1.json#/ownerSuccessors`)

| Id | Owner | Selector | Effect |
|---|---|---|---|
| S1 | native | `native-evidence.md` §8, after FR-5 | Prose FR-6: repository-relative evidence and entry paths; testGlobs unit-root-relative under the glob law. Prose FR-7: one recognition per rust/tsjs unit committed in the parameter; explicit replaces recognized. Model duty: `recognize_frameworks(files, unit_root)`. No schema change. |
| S2 | foundation/identity | `identity-schemas.v3.json#/x-opensip-payload-registry/classes/parameter/rows/foundation~1framework-recognition-plan.schema.v1.json` (absent before) | New parameter row with the existing `requiredForEvaluatorMajors: [3]` vocabulary. |
| S3 | query | `query-projection-contract.v3.md`, new §8a | Internal whole-view projection for host reporting. No schema or Operation change. |
| S4 | report | `owner/report-projection-successor-patch.v1.json` | §8 below. |
| S5–S7 | workflows import; enumeration/inventory; native `SourceUnitOwnershipV1` | — | No change; consumed as stated. |

**Identity effect of S2 (exposed in full):**
- **PlanId** changes for every evaluator3 Plan, and **RunId** changes through it.
- **Why this is not gratuitous:**
  - FR-5 already requires Plan visibility;
  - reachability origins and `ClosedWorldV2.entryPointsRecognized` consume these entry points;
  - replayable assurance needs the input.
- **Unchanged identities:** universe, context, fact2, coverage2 and subject3.
- **Historical Runs** stay admitted under their own profile and show `not-plan-bound`.
- **Also required:** the identity record-document digest sweep list and Run closure required refs must name the document (RP-EV-INT-IDENTITY).

## 8. Report schema successor (S4)

**Parent:** subject-05 `report-projection.schema.json`.

**Remove-rows ops:**
- `/$defs/FeatureId/enum` drops the four feature ids.
- The seven shared per-command consts `/allOf/{3..9}/then/properties/featureStates/const` (default, analyze, fit, audit, candidates, inspect, review-brief) drop their rows for these features. `allOf/10` (repair-preview) holds none.

**Composition.** These are shared selectors, so the ops are `remove-rows` with exact `before`/`after`. `check.py` proves they commute with another obligation's `remove-rows` on the same selectors.

**Add ops:**
- `PanelsV1.coupling` and `PanelsV1.symbolEvidence`.
- 20 new `$defs`: `CouplingPanelV1`, `SymbolEvidencePanelV1`, their state wrappers and parts.

**Unchanged:** `FeatureStateV1.reason` and all existing `$defs` except `FeatureId` and `PanelsV1`.

**`$id`.** It stays `report-projection:1` because no report-projection major was accepted. If one is accepted first, the same ops apply under `:2` (RP-EV-INT-SCHEMA).

**Panel prerequisites.** `symbolEvidence` subjects are exactly the graph panel's `subjectResolution` (`J-SE-SUBJECTS`). Without a present graph panel it is `unavailable/prerequisite-panel-not-present` (`J-SE-PREREQUISITE`).

**featureMap successor.** R07, R08 and R12 map to the new defs (register `featureMapSuccessor`).

## 9. Integration duties (register `integrationDuties`)

| Id | Duty |
|---|---|
| RP-EV-INT-SCHEMA | Apply the patch; drop the four featureStates rows and readiness blockers; swap the featureMap rows. |
| RP-EV-INT-BUDGET | Priority comparison, catalog, evidence, graph, symbolEvidence, coupling, history under the shared 4,194,304 B exploration cap. `documentMaxBytes` is unchanged. |
| RP-EV-INT-STATIC | Static parity successor names the host-asserted items. |
| RP-EV-INT-GENERATOR | Register the sources and regenerate bindings (not run). |
| RP-EV-INT-COVERAGE | Close `/reviewIssueAdditions/2, 4, 8, 9` only after S1–S4 review; add producer and projection delivery rows. |
| RP-EV-INT-IDENTITY | Sweep list and required-ref closure; refuse a missing required parameter under the successor profile. |
| RP-EV-INT-RETENTION | Parameter custody → `entryRecognition.state`. |
| RP-EV-INT-BROWSER | Views for unknown, lower-bound and blocker states and interpretations (not executed). |
| RP-EV-INT-MEASURE | Whole-view projection and query cost (not measured). |

## 10. Evidence and limits

**`check.py` verifies:**

1. **Parents and pins.** Subject-05 outer manifest and parent files; pins, alias probe and bytecode demonstration.
2. **Regeneration.** Byte-identical owner records and fixtures.
3. **Owner admission:**
   - parameter schema meta-validity, copy drift against native, no external `$ref`;
   - patch before/after, the only changed pointers, commutation, patched meta-validity, and every `$ref` registered;
   - identity row uses only existing vocabulary.
4. **Glob law.** The 22 contract examples plus 5 unit-relative examples; the model and the pinned `workflows_model.v1.glob_match` agree.
5. **Worlds.** Owner-schema validation of every world record (`UnitMembershipV1`, `EnumerationPlanV1`, `SubjectInventoryV1`, `SourceUnitOwnershipV1`, the parameter, `GraphEndpoint`) and World joins (`unitId` re-derivation, membership digest).
6. **Positive derivations with exact expected values:**
   - mixed Rust + TS/JS world: 17 facts, 8 cells, buckets, absence blockers, 35 metrics, trace and test states;
   - clean world: `absenceSupported`;
   - integration world aligned to subject-05 `audit-full`: explicit entry provenance, `no-static-path-within-bound`, witness.
7. **Variants:**
   - partial package inventory;
   - recognition not-plan-bound, purged, partial-missing and partial-present;
   - no reachability view;
   - 101 origins (page set not embedded);
   - 100,001 call facts (lower-bound 100,000);
   - metric byte-budget omission;
   - purged Run evidence (panels `unavailable/evidence-purged`).
8. **Adversarial cases, each with its exact code:**
   - **44 document cases:** coupling 12, metrics 11, traces 9, test reachability 12.
   - **14 recognition parameter cases.**
   - **6 host-derivation cases.** Prefix guess, symbol-spelling parse, target-ownership-as-package and browser entry-name heuristics pass browser-level admission and are refused only by the host derivation. The test-name guess is refused at `J-TR-ORIGIN-SET`; the imported testId at `SCHEMA`.
9. **Integration.** Subject-05 `audit-full` with the successor panels validates under the patched schema. A retained removed feature state → `SCHEMA`. Mismatched subjects → `J-SE-SUBJECTS`. Graph absent → `J-SE-PREREQUISITE`.
10. **Register.** Obligation, featureId and coverage-issue selectors against the parent; requirement-text sentences in the pinned inventory, native, query and workflow contracts.

**Limits:**
- Worlds and the mock graph owner are constructions following the cited laws. They are not the product engine, store, providers or browser.
- Occupancy reconciliation is taken as given on facts.
- Owner models are agreed by rule implementation, not by executing `native_evidence_model` or `query_projection_model`.
- S1–S4 are unaccepted proposals.
