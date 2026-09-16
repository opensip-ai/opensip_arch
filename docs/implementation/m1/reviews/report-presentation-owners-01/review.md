# Review: four report presentation owner/reference proposals

This is a fresh, independent review. There are four **separate** verdicts: none is merged with another, and none claims report integration or feature delivery. Where a verdict accepts anything, it covers only the owner/reference unit.

| Subject | Obligations | Verdict |
|---|---|---|
| `m1-presentation-catalog-subject-01` | RP-DO-01/06/07/08 | **changes-required** |
| `m1-config-disclosure-subject-01` | RP-DO-04 | **changes-required (narrow)** |
| `m1-workflow-timing-subject-01` | RP-DO-11 | **changes-required** |
| `m1-history-selection-subject-01` | RP-DO-12 | **changes-required** |

## Custody and reproduction

- **Manifests:** checked before and after the runs (`probes/closure-before.json` equals `probes/closure-after.json`). For each subject, all of these match:
  - manifest SHA-256
  - exact file set (9/10/8/8 files)
  - per-file bytes and hashes
  - every external pin (10/6/3/5), plus the timing successor's parent pin
- **Bytecode:** no bytecode was written to any subject or to report-projection-subject-07. The architecture `__pycache__` inventory is unchanged; `foundation/__pycache__` already existed on Sep 6.
- **Root suites:** run on private copies with `metadata-reference-env/bin/python -I -B`. They pass **10 + 10 + 8 + 9** groups, all exit 0. These are reference tests over synthetic admitted dictionaries and callbacks, not runtime custody.
- **Mutants:** 18 single mutants (`probes/mutant-results.json`); 16 are killed.
  - Survivors: **CAT-M3** (canonical cap removed) and **CAT-M6** (undeclared capability keys admitted).
  - CAT-M5 is killed only because a root test pins the conflated label criticised in CAT-F1.
  - CFG-M4 is killed by shape tests only, not by any PlanId binding test.
- **Control corrections:**
  - CAT-C4 was meant as a float control but actually refused on a digest mismatch (`CATALOG.BLOB`). It is kept as a digest-swap control; float refusal is covered by the reproduced root test.
  - My first history probe run crashed with a `NameError` in my own code. It was fixed and rerun.

## 1. Presentation catalogue: changes-required

**Sound and reproduced:**
- Association of the reserved regular-file path via the identical Blob in `closure.tree`, with exact length and raw SHA-256.
- No embedded `closureId`, so no self-reference (the invalid control is preserved).
- A present-but-invalid listing never downgrades to absence.
- Canonical-owner parsing.
- Exact `ruleProgramRef` and `RecipeRef`-minus-`closureId` types.

**Blocking:**
- **CAT-F4: capability ownership.** The catalogue keys capabilities to "that same closure". But capabilities are native release declarations (`native-evidence.md:1014-1022`, `ReleaseCapabilityRegistryV1`). The report's `CapabilityCatalogV1` sources them from `release-capability-registry`/`registrySha256`, and RP-DO-01 names that owner.
  - Probe: two closures admit contradictory descriptions of `reachability`.
  - Correction: bind capability descriptions to the release registry through the Plan, or restrict closure listings to capabilities that closure itself declares. Refuse conflicting descriptions.
- **CAT-F1: absence and not-retained collapse.** `select_descriptions(None)` always reports `catalog-not-retained`, even when the admitted tree simply has no listing.
  - Correction: distinct closed states for no-catalogue-declared, not-retained, and refused/corrupt.

**Required:**
- **CAT-F2.** A row missing from a *retained* listing is labelled `descriptor-not-retained`, and selection accepts keys outside the declaration index.
  - Correction: rename that state to not-declared, and require selected keys to be a subset of the declaration index and the Run's selection.
- **CAT-F7.** The receipt omits `tree`, `platform` and `protocolMajor`, and the platform is never checked. That departs from the detector-compatibility receipt (`security-and-lifecycle.md:59-66`) the contract claims to reuse.
  - Correction: copy those members, or justify each omission.
- **CAT-F6.** `selector` consists only of constants copied from `RepairPreviewParams`, identical for every recipe. Describing `evidenceSource`/`targets` is a reasonable reading of "applicable parameters", but the selector says nothing recipe-specific.
  - Correction: add a declared per-recipe applicability selector validated against the index, or rename it to `targetBounds` and record that applicability comes from `RepairPlanDescriptor` at preview.
- **CAT-F5.** Names and descriptions admit U+202E bidi overrides, NUL, ESC and U+2028.
  - Correction: forbid C0/C1 and bidi controls in the schema, or assign an explicit renderer isolation duty with hostile fixtures.

**Minor:**
- **CAT-F3.** If the delivery tree lacks the listing but `closure.tree` has it, the result is absence.
- **CAT-T1.** Add tests that kill CAT-M3 and CAT-M6.

**Remaining integration:**
- Core catalogue file and completeness gate
- Report carrier and the four featureStates
- Real signed closure/platform admission and retention
- Renderer and browser tests
- Source/inventory/generator binding

## 2. Configuration disclosure: changes-required (narrow)

**Strong reproduced behaviour:**
- **Pinned resolver:** its semantic output and `resolvedConfigDigest` project with an equal digest and no leaked profile or path (CFG-C1). Winning-layer provenance exists in the resolver output but is not accepted by the projection.
- **No current-settings fallback:** a changed current configuration against an older Plan digest refuses (CFG-C2).
- **Noninterference:** 32 variants that differ only in redacted values, string lengths, or `version` vs `versionConstraint` produce identical carriers apart from the source digest (CFG-C3).
- **Missing, empty and present stay distinct:** not-present, redacted with itemCount 0, and redacted with a count.
- **Types:** exact integer budget.
- **Schema:** the closed schema regenerates from the pinned identity v3 selector. v2 and v3 `semantic-configuration` are equal.

**Required:**
- **CFG-F1.** `source.planId` is whatever the caller passes, for the same Plan; `admitted_plan` is never validated as a Plan.
  - Correction: validate the Plan and recompute its PlanId, or take PlanId from the admitted Run/envelope and mark the association host-asserted.
- **CFG-F2.** There is no `verifiedInDocument`/`hostAsserted` provenance, unlike sibling report carriers.
  - Correction: add a const provenance list.
- **CFG-F4.** "Owned unavailable-source state" is not mapped.
  - Correction: freeze the mapping from each failure (missing, purged, expired, corrupt, digest mismatch, future schema) to an existing `PanelNotPresentV1` state and reason.

**Minor:**
- **CFG-F3.** The `components.request` itemCount minimum should copy the owner's `minItems 1`.

**Advisory:** profile, capability and pack IDs are registry-closed per the resolver. Redacting them is conservative, not wrong.

**Remaining integration:**
- Host Plan/Run and retained-source handles
- Carrier and byte accounting
- Final serialized-HTML leakage and accessibility tests
- Binding and selection

## 3. Attempt duration (invocation:4): changes-required

**Sound:**
- **Measurement boundaries:** from after ExecutionId assignment to after the terminal outcome and before persistence. Backoff, queueing and the record write are excluded.
- **Zero:** zero is a real measurement, never a fallback.
- **Abandoned attempts:** only `supervisor-lost`, with no clock-subtraction across a crash.
- **invocation:3 records:** `not-retained` as a read projection only.
- **Identity:** duration is excluded from identity, authority and retry.
- **Sum label:** "sum of retained terminal attempt durations", with an incomplete/overflow state.
- **Schema delta:** v4 equals v3 plus `observedDuration` (reproduced).
- **Arithmetic:** floor holds over 20000 random pairs and at the boundaries.

**Blocking:**
- **TIM-F1.** The v4 `Attempt` schema accepts abandoned+measured, completed+supervisor-lost and abandoned+clock-unavailable. The outcome/reason law lives only in `timing.py`, even though `Attempt` already uses `allOf` if/then.
  - Correction: add the conditions to the schema and to the delta test.

**Required:**
- **TIM-F2.** Malformed samples paired with `None` return `clock-unavailable`, contrary to the contract.
- **TIM-F3.** `summarize_attempts` raises `KeyError` on bad input, sums duplicate ExecutionIds, and returns negative sums.
  - Correction: admit each projection before summing.
- **TIM-F4.** Retained invocation major 1 exists, and "other majors are refused" leaves its report state unowned.
  - Correction: map it to `incompatible/retained-schema-major-unsupported`.

**Advisory:** name the existing `render-in-progress` ledger state.

**Remaining integration:**
- Host monotonic clock and durable custody, including crash recovery
- Rebinding every invocation:3 consumer; the report ledger still references v3 and has no duration
- Ledger carrier, bounds and labels
- D9/identity qualification

## 4. Explicit history selection: changes-required

**Sound and reproduced:**
- Order preserved; 1-4 distinct full `run3` IDs.
- `latest`, prefix, comma, five IDs and duplicates all refuse before lookup.
- No implicit baseline or recent-Run insertion.
- `current-run` equality after deterministic analysis consumes a slot with no lookup.
- Exactly one lookup per other slot, with the owner's four unavailable states.
- The automatic no-flag owner is unchanged.

**Blocking:**
- **HIS-F1: route contradiction.** The owner already routes a non-applicable format to `REQUEST.UNKNOWN_OPTION` / `OUTPUT.FORMAT_NOT_APPLICABLE` (2) (`workflows-and-surfaces.md:1141-1142`), and `EVALUATION.SELECTION_LIMIT` exists for over-bound requests. The proposal folds format misuse, the count limit and malformed tokens into one new detail under `REQUEST.UNSATISFIABLE`.
  - Correction: split the route and add goldens.
- **HIS-F5: owning unit bypassed.** RP-DO-12 names `query-projection-contract.v3.md` §1 (typed `run.show` item). The subject neither pins nor types it; the lookup is an untyped callback.
  - Correction: resolve slots through typed `run.show` (project equality, `close_run` identity, availability mapping), or justify the bypass and name the owner.

**Required:**
- **HIS-F6.** Freeze the exact inventory flag record `{flag, owner, class, join}` for all eight HTML rows: value grammar, repeatability, format coupling and help text.
- **HIS-F2.** A malformed host `currentRunId` raises the user-facing `HistoryRefusal`; it should be an internal source refusal.
- **HIS-F3.** Define when the read snapshot is taken relative to this invocation's own commits. Specify the slot source for a requested pivot Run minted by the same invocation, which is currently an ordinary snapshot lookup.
- **HIS-F4.** Write the explicit-mode panel variant. It needs a present `HistoryRunV1`, unavailable and current-run slot union. Its provenance must drop the automatic mode's `not-current-run` and descending-sequence claims and add rows-equal-requested and current-run-equals-envelope. The reference accepts a present slot naming another project (synthetic; no custody claimed).

**Advisory:**
- **HIS-D1.** Measured overhead: the maximal selection record is 896 canonical bytes, and four minimal unavailable rows are 533 bytes. Put the exact bound, including the optional detail, into the budget derivations.

**Remaining integration:**
- DomainDetail, route table and goldens
- Inventory rows, CLI grammar and help
- Namespace snapshot lookups and Run handle binding
- Report union, provenance, budget and featureState
- Browser controls limited to embedded slots
- Final HTML parity

## Scope

Nothing outside this directory was modified. The report evidence owner author02 and the interruption-envelope work were not touched or assessed. Probes, results, private copies and mutants are in `probes/` and `runs/`.
