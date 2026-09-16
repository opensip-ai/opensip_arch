# Advisory: CoverageResultV3 producer admission (next owner after capability-support)

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Bounded next-owner map. **Not ACCEPT-DESIGN-UNIT. Not frozen source. Not private-16 draft review. Not full Run.**
**Work tree:** `/tmp/opensip-implementation/m2-grok-coverage-producer-boundary-17/review`. No live/frozen/history edits.

Selected identity `619d6e3c…41e6` / 158555; selected native `e6784aa1…e2b9` / 319944. Live product native-v2 `e5834d37…7773` / 280357; identity-v3 `311c1feb…b68f` / 197480. Live lock independently **13/17**. Private capability-support-16 is **not** treated as accepted or correct here.

## What this owner is (and is not)

`admit_coverage_result_v3` (native 1545–1625) is the **producer boundary for one CoverageResultV3**. It judges one provider payload against a **host-recomputed** foundation subject-scope. Schema-valid JSON is not admission (identity 1921–1924).

Editable-16 / inventory-16 (capability_support) owns only the three **post-producer** guards:

| Guard | Identity lines | Native helper |
| --- | ---: | --- |
| ownership | `coverage_dialect_prerequisite` 1332–1376 | `clone_ownership_disclosure` 1311–1356 |
| syntax | `syntax_capability_prerequisite` 1171–1212 | `syntax_capability_support` 896–940 |
| source-variant | `coverage_source_variant_prerequisite` 1377–1450 | `source_variant_capability_support` 967–1029 |

Those run at identity 1938–1947 **after** `admit_coverage_result_v3` returns ADMIT. They are not this owner.

Also **not** this owner: `coverage_inventory_totality` (identity 1255–1296, needs view facts + snapshot); view **partition disjointness** (identity 1863–1892); `coverage_view_use` (native 1628–1642, not called from `open_run_closure`); Plan-native counts; caller Coverage ADMIT.

## Calling order inside `open_run_closure`

1. **1650** `walk(run)` — facts, including `syntax_capability_supported` / `body_identity_join` on relation payloads.
2. **1689–1749** Plan-native block (installed `inspect_plan_native`). Counts only.
3. **1853+** per view: well-formedness, **1863–1892 partition**, facts/anchors, **1913–1916** retained-scope ladder via `_rung_index`.
4. **1917–1948** per `view.coverageIds`:
   - 1918–1919 `COVERAGE_SCOPE_JOIN`
   - 1925 `payload_of_coverage` → `registered_payload` class `coverage`
   - 1927–1928 unresolved-edge payloads of **this view** as `{relation, referrer, edgeKind}`
   - 1932–1933 host dialect table from retained universe row (`body_eligibility_table`), never from payload
   - **1934 `admit_coverage_result_v3`** ← this owner
   - 1936 `COVERAGE_PRODUCER_ADMISSION` if not ADMIT
   - 1937 `COVERAGE_ADMITTED_IDENTITY` if `admitted['coverageId'] != cid`
   - 1938–1947 three guards (16)
   - 1948 inventory totality (identity)

Producer does **not** see the snapshot. Identity injects `examinedSubjects=scope_descriptor['subjects']` only inside native 1573.

## Exact producer obligations (`admit_coverage_result_v3` 1545–1625)

Input: trusted observation `payload`; host `scope_descriptor`; `unresolved_facts`; optional `payload_schema_digest`; optional `universe_dialect` (**context**, native 1578–1581 — never read from payload).

1. `validate_native("CoverageResultV3", payload)` — schemaVersion const 3; `key` CoverageKeyV2; `entry` ViewEntryV3 (native-v2 1418–1436, 1285–1416).
2. Recompute `subject_scope_commitment(scope_descriptor)` (1530–1542):
   - `_rung_index` on host relation/rung (1513–1514) else `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER`
   - duplicate subjects refuse (1516–1517); order by `C.canonical` for the foundation encoder (1515)
   - `scope2:` + H(`subject-scope`, descriptor); commitment is `sha256:` + same 64 hex (1537–1539). One preimage, two spellings. Not a native H domain.
3. Key vs host scope: `relation`, `resolution`, `sourceUniverse`, `targetUniverse` (1559–1563) → `native.coverage-key-scope-mismatch:<field>`. Both identity subject-scope (641–655) and CoverageKeyV2 (1383–1403) use **bare 64 hex** for universes.
4. `key.subjectScopeCommitment` vs recomputed (1564–1565) → `native.subject-scope-commitment-mismatch`.
5. `entry.relation/resolution` vs `key` (1566–1567) → `native.coverage-entry-key-mismatch`.
6. `entry.examinedUniverse.subjectScopeCommitment` (1569–1570) → `native.examined-universe-commitment-mismatch`.
7. `examinedUniverse.subjectCount` vs `len(host subjects)` (1571–1572) → `native.examined-universe-subject-count-mismatch`. ExaminedUniverseV1 (1216–1240) carries **only** commitment + count, not the subject list.
8. `coverage_bijection` (1380–1486) on `dict(entry, examinedSubjects=scope_descriptor['subjects'])` plus unresolved facts:
   - **RC-0 first**, independent of facts: `_rung_index` none → `RC-0: rung is not a member of this relation's own ladder`; no empty-ladder fallback (1383–1390, 1408–1409).
   - **RC-6** before rung branch, no `continue` (1412–1448): `coverage==complete` ⇒ `examinedExhaustive is True`. Implication, not equality. `unknown` + exhaustive is lawful.
   - Non-resolved rungs (`RESOLVED_RUNGS` 684): **RC-1** not-applicable, count 0, `attempted` false, empty class list; `stageTerminal` unconstrained (1398–1453).
   - Resolved: **RC-2** (1461–1485). Filter facts with RC-4 inheritance (1458–1459): reachability also counts `calls` referrers in examined. `complete` needs attempted + exhaustive + `stageTerminal==complete` + zero facts + empty class list. `not-attempted` cannot carry counts/`attempted`/classes. `incomplete`/`partial` counts and classes must match observed; incomplete also needs ≥1 edge, complete stage, exhaustive else it is partial.
   - `completeness_from_stage` (1358–1376) **generates** a claimed RC-2; **admit does not call it**. Checking claimed state is bijection’s job.
9. `deficiency_cause_faults` (1246–1308) one-way: declared pair vs entry carriers (`x-opensip-deficiency-cause-registry`). Null deficiency with a cause refuses. Does **not** derive an owed deficiency (RC-3 complete+incomplete+no deficiency is lawful).
10. **Producer-local source-variant slice** (1589–1605): only if caller supplied `universe_dialect` **and** relation has `bodyIdentityJoin` **and** `subjectKind==source-path`. Symbol/inventory branches are **not** decided here (1583–1588). Names `native.coverage-source-variant-*`. Closure still runs `coverage_source_variant_prerequisite` (1947) with identity names `COVERAGE_SOURCE_VARIANT_*`. `scopeCapabilityLaw.refusals` (identity-v3 4790): producer may fire first so closure names are not always reached.
11. `payloadSchemaDigest` must equal SHA-256 of the registered native schema **document** bytes (1606–1612) → `native.coverage-payload-schema-not-registered`. Caller may restate, never choose.
12. Output `CoverageAdmissionV1` (native-v2 6582+): REFUSE if any refusals **or** bijection faults; ADMIT mints `coverageId = identifier('coverage', {schemaVersion:2, scopeId, payloadSchemaDigest, payloadDigest: raw_sha256(C.canonical(payload))})` (1620–1623).

`coverage_view_use` (1628–1642) is a **separate** native helper (view must name producer-admitted coverage2 whose scopeId ∈ view.scopeIds). Identity instead does `COVERAGE_SCOPE_JOIN` (1919) and `VIEW_COVERAGE_JOIN` (1906). Do not substitute one for the other.

## Recommended bounded Rust API

Evaluator, sibling of `capability_support.rs`, **not** inside it and **not** inside `plan_native.rs`.

```
admit_coverage_result(
  inputs,                    // schema registry + identity H for subject-scope / coverage2
  payload: CoverageResultV3, // provider bytes, already or to-be shape-admitted
  scope: SubjectScopeV2,     // HOST descriptor (objects[scopeId]), not payload.key
  unresolved: &[{relation, referrer, edgeKind}],  // this view only
  payload_schema_digest: Option<[u8; 32]>,
  universe_dialect_table: Option<&BTreeMap<…>>,   // host context; None = skip producer source-variant slice
  work: usize,
) -> Result<CoverageAdmission, CoverageProducerError>
```

- No `PlanNativeChecks`, no caller ADMIT token, no snapshot walk, no fact graph, no Coverage producer “success” implying Run.
- Recompute commitment from `scope`; inject `examinedSubjects` from `scope.subjects` only.
- `refusals: Vec<String>` vs `faults: Vec<{entry, fault}>` kept distinct (ADMIT iff both empty).
- Closed data: native-v2 `#/$defs/CoverageResultV3`, `#/$defs/CoverageAdmissionV1`, `#/$defs/SubjectScopeCommitmentV1`, `x-opensip-deficiency-cause-registry`, relation ladders / `RESOLVED_RUNGS`. Extract kebab `coverage-registry.json` rather than restating.

Identity `open_run_closure` 1934 remains the caller that supplies dialect table and compares `coverageId`.

## Differential fixtures (producer only)

| Case | Expect |
| --- | --- |
| Schema-valid payload, commitment hex ≠ H(host scope) | `native.subject-scope-commitment-mismatch` REFUSE; no coverage2 |
| Count ≠ len(host subjects) | `native.examined-universe-subject-count-mismatch` |
| Key universe/relation ≠ host scope | `native.coverage-key-scope-mismatch:*` |
| `file@enumerated` + `complete` + `examinedExhaustive=false` | bijection RC-6 fault (even with zero unresolved facts) |
| `unknown` + `examinedExhaustive=true` | RC-6 silent (lawful) |
| `unresolved-edge@enumerated` entry | RC-0 ladder fault |
| `declares@syntactic` claiming `state=complete` | RC-1 not-applicable |
| Resolved `complete` with zero count but nonempty `unresolvedEdgeClasses` | RC-2 class-list fault |
| `reachability` + a `calls` unresolved-edge whose referrer is examined | counted (RC-4) |
| `complete` + `state=incomplete` + matching edges + exhaustive + stage complete + null deficiency | ADMIT at producer (RC-3); 16-guards may still refuse |
| `derivationPolicy` deficiency on `references` | `native.coverage-cause-relation-not-in-scope` |
| Wrong `payloadSchemaDigest` | `native.coverage-payload-schema-not-registered` |
| TS clones `source-path` over `package.json` + dialect table supplied + `complete` | producer `native.coverage-source-variant-unsupported-complete` |
| Same without dialect table | producer silent on variant; closure 1947 still decides |
| Symbol-kind scope | producer source-variant slice skipped (1583–1588) |
| Minted coverage2 bytes ≠ `identifier('coverage', …)` | identity `COVERAGE_ADMITTED_IDENTITY` (1937), not producer REFUSE |

Do **not** use Plan-native empty-refusal counts as a fixture oracle for commitment.

## Traps (function + line)

- **1573** injecting `examinedSubjects` from payload or omitting them (bare `resolutionCompleteness` helper path skips RC-6, 1441–1445).
- **1358 vs 1573**: calling `completeness_from_stage` instead of bijection.
- **1388–1390 / 1408**: empty-ladder fallback; RC-0 independent of unresolved facts.
- **1412–1433**: treating RC-6 as equality (`unknown` forbids exhaustive).
- **1458–1459**: forgetting RC-4 `calls` under `reachability`.
- **1461–1472**: `complete` checking count only (class list must be empty).
- **1246–1257**: deriving owed deficiency from RC-2 incomplete.
- **1578–1605**: reading dialect from payload; treating producer source-variant as replacing 1947; folding 1938–1939 into producer.
- **1934 vs 1628**: using `coverage_view_use` as Run closure; using Plan counts as `scopeIds` proof.
- **1620–1623**: hashing payload with H-frame or `sha256:` prefix instead of `raw_sha256(C.canonical(payload))`; using `scope2` vs `sha256:` interchangeably in the key field.
- **1609–1612**: digest of a selector or CoverageResultV3 instance instead of the native schema **document**.
- **1921–1936**: treating shape-admit of CoverageResultV3 as producer ADMIT.
- Schema prose on ViewEntryV3.`coverage` (native-v2 ~1312) names carrier `native.coverage-bijection-mismatch` at Run closure; selected identity emits `COVERAGE_PRODUCER_ADMISSION:` + `refusals` + `str(faults)` (1936). Native public-route table (3612) lists `native.coverage-bijection-mismatch` as operational-failed/4. **Do not implement the prose carrier as the identity refusal string.**

## Dependencies / files

Evaluator: new `coverage.rs` + closed `coverage-registry.json` (deficiency-cause extract, resolved-rung set, RC state enum). Uses identity H/`identifier` for `subject-scope` and `coverage`; schema admit for CoverageResultV3 / SubjectScopeCommitmentV1 / CoverageAdmissionV1. May call `source_variant_capability_support` **only** for the 1589–1605 slice (optional dialect). Must not depend on `inspect_plan_native` success.

Identity stays the Run caller (1934–1937). Relation ladders from relation-payload registry (`LADDERS` / `_rung_index` 765–767). Unresolved-edge shape UnresolvedEdgePayloadV1 (native-v2 1438+).

## requiredFindings

1. **Carrier name split (specification).** Live native-v2 ViewEntryV3.`coverage` description (e5834d37, ~1312) states bijection disagreement at retained Run closure uses `native.coverage-bijection-mismatch`. Selected `admit_coverage_result_v3` (1573, 1613–1615) puts RC-* strings in `faults[]` and `native.*` keys in `refusals[]`. Selected identity 1936 prefixes `COVERAGE_PRODUCER_ADMISSION:`. The DomainDetail code exists (native model 3612; common-v4 enum) but is **not** what those two selected functions emit. A bounded producer must preserve the selected split (`refusals` vs `faults`) and must not invent a Run-closure refusal equal to the schema-prose carrier unless a later unit explicitly rebinds it.

No other selected-function contradiction found between CoverageKeyV2/subject-scope universe spelling (both bare hex) and commitment recipe (scope2 vs sha256: of the same hex).

## Verdict

**NOT ACCEPTANCE.** Next implementation owner is `admit_coverage_result_v3` as a bounded evaluator producer: host-recomputed commitment/count, RC-0/6/1/2 bijection, deficiency-cause support, optional source-path variant slice, registered schema-document digest, CoverageAdmissionV1 identity. Editable-16 guards and inventory totality stay out. No caller ADMIT or Plan-count authority.
