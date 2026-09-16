# Frozen trial review: coverage-producer-17

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of the private single-Coverage **producer** boundary over explicit host context. **Not runtime selection. Not Coverage-16 guards, inventory totality, view/Plan/full Run, replay, or public routing.** Layout inventory v17 is a separate accepted inventory unit; this source is **not** live-installed.
**Work tree:** `/tmp/opensip-implementation/m2-grok-coverage-producer-review-17/review`. Live, frozen, and history not edited. No commits.

The archived coverage-producer-boundary-17 advisory plus **two** follow-ups are **not** acceptance and **not** a fresh-blind of this source. They are used only for selected-function semantics (carrier layer; identifier-only commitment).

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/coverage-producer-17/subject.json` | 52278 | `6d4d2cd8c52ca49fb5588915bedc7b4bcf901fb322c3994161fc109c5a49e84e` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 51463917 | `7a04b7f9cda9785192fbda9119b2382f41efbf692dfcbfd589f784c6da67e5a4` |
| adjacent `coverage-result.json` | 317 | `ecefb4bb07cbc6989ba6aa57f3a508cad545187861e841f9d066a8c4dd416381` |
| adjacent `oracle-scope-account.json` | 2112 | `dd8612ddb8929cdca94a7452ab624e963edae3c7601a4d7f62994ec41b28e5fc` |
| export | `/tmp/opensip-implementation/m2-coverage-producer-subject-17` | 293/293 member pins match; tar 293/293; 0 extra; 0 missing |

293 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: capability-support-16 subject `6539a71f…be28`; runtime-v6 unit `81eecef4…8a8d`; inventory-v17 subject `89509a74…22c2`; advisory/followup/commitment-followup json `236f88e2…`, `c21e0b88…`, `7ae53762…`; selected native e678 `e6784aa1…e2b9`.

Live lock independently observed **15 inventory / 19 contract** (last inventory **candidate** v17; last contract native-runtime v6). Live tree has capability-support from v6 and **no** `coverage.rs` / `coverage-registry.json`.

## Source delta vs frozen 16 / live v6

**232** prior product files byte-identical to frozen capability-support-16, including identity `closure.rs` and identity source-policy. No new crate dependency. `Cargo.toml` unchanged vs live.

Changed: `lib.rs` export, host `native_owner_tests.rs`, host fixture. **New:** `coverage.rs` / `coverage-registry.json`.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `product/crates/evaluator/src/coverage.rs` | 17385 | `2fb1f295bebfa38b134286211137d9a8f409846d2c3529f7ee13e3fc58035e8d` |
| `product/crates/evaluator/src/coverage-registry.json` | 24708 | `ef21bc0d98ad8d60cf70edfd779686de4dec39a586c9989ccace23059de624bd` |

Closed registry `nativeSchemaSha256` equals live/export native-v2 `e5834d37…7773` / 280357.

Host fixture **4052701** bytes (`85e12d2a…8f2f`) is under the 4 MiB production parser cap; tests keep explicit per-request `blobDigests` membership.

## Law vs selected N `admit_coverage_result_v3` (e678) and advisory+corrections

`inspect_coverage_producer(inputs, CoverageProducerInput, budget)`:

- Retained payload via `registered_record_shape` against exact registered `CoverageResultV3` / native-v2 document digest.
- Host scope loaded as `SubjectScope`; identity `object()` rehashes identifier and checks `enumeratorClosure` role **provider**. Missing enumerator object is a fixture/retention error (initial 603/499), not a producer-code fix.
- Commitment is **`sha256:` + hex of the retained `scope2:` identifier** (Python `identifier` only). Does **not** call `subject_scope_descriptor` / `_rung_index` / `SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER`. `scope-rung-mismatch` refuses key/commitment joins with **empty faults**; `entry-rung-mismatch` is **RC-0** on the entry. Matches the commitment follow-up.
- Key/entry/examined commitment and **count** vs host `len(subjects)`.
- Bijection: **RC-0** first; **RC-6** implication (`complete` ⇒ exhaustive); non-resolved **RC-1**; resolved **RC-2** with **RC-4** reachability inheriting `calls` referrers. `golden-rc3-rc4-*` ADMIT (complete examination + incomplete resolution is lawful).
- One-way deficiency/carrier registry (`native.coverage-cause-*`); does not derive an owed deficiency.
- Optional **host** `universe_dialect` source-variant slice only; longest matching suffix; **null/None variant is unsupported**. FullRun still owes the 16 source-variant guard when dialect is omitted.
- ADMIT mints `coverage2:` from schemaVersion 2 + scopeId + payloadSchemaDigest + payloadDigest. REFUSE keeps separate `refusals[]` vs `faults[]` (carrier-layer follow-up: internal keys are not DomainDetail strings).
- Unresolved edges and dialect are **explicit host context**; this API does not prove census completeness.
- `steps==0` → `CoverageProducerError::Limit`. No `inspect_plan_native` / `inspect_coverage_prerequisites`. No caller Coverage ADMIT.

FullRun still: producer **before** the three 16 guards and inventory totality; then coverage-identity comparison; public D9 routing is host presentation, not this unit.

## History (fixtures/harness + one real product bug)

- Initial missing enumerator object: 603 cases, **499** mismatches; fixture corrected, no producer-code change.
- Initial 603 after that: 0 mismatch; later expanded rungs/enums (structural-dispatch, exact resolved-callee/from-resolved-calls); one intentional bad stage enum kept.
- Targeted **6** nullable-table cases: real draft bug (any matching suffix instead of **longest**, so `None` was ignored). **4** initial mismatches preserved (`a.ts` / `a.d.ts` / longest `.d.ts` None / `.ts` None vs `.d.ts` dts). Corrected `max_by_key(len)` + `is_none_or(Null)`. Final 6 match (2 ADMIT).
- Host fixture compacted under 4 MiB cap.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Frozen 775-row actual/expected independently classified: **775/775**, **229 ADMIT**, **0 mismatch** (21 raw `error` rows classify to expected invalid/unavailable).
- `cargo test --locked --offline -p opensip-host coverage_producer --lib` on the **export** product: **ok** (15 host cases including RC-3/RC-4/RC-6, schema/count, nullable longest-None, `steps:0` Limit).
- Identity policy independently passed: `sourceFilesVerified: 110` (unchanged vs 16). Frozen workspace.stdout sums to **102**. Final Clippy `-D warnings` compile-only.

Did not re-pipe 436 MiB `coverage-requests.ndjson`. Did not re-exec Unicode-15 or 07–12 corpora.

## requiredFindings

None.

## Limits (not required findings)

- Local ADMIT is not view completeness, Plan, inventory totality, 16 guards, `close_run`, or ReplayedRun.
- Unresolved/dialect host context is not a proven census.
- Public DomainDetail / D9 mapping is not this owner (carrier follow-up).
- Layout inventory v17 names these files; live runtime v6 does not install them.
- Did not re-pipe the 436 MiB request corpus through a rebuilt harness.

## Verdict

No required findings. Private producer matches selected `admit_coverage_result_v3` as corrected: identifier-only commitment, RC-0/6/1/2 + RC-4, one-way carriers, host dialect longest-suffix None unsupported, coverage2 on ADMIT, explicit host context without census authority. Not a live/runtime/full-Run selection.
