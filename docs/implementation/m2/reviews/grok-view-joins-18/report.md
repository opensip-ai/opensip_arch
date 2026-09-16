# Frozen trial review: view-joins-18

**Reviewer:** Grok. Root remains lead. Not Claude agreement.
**Kind:** Scoped source review of private retained **per-view joins**. **Not runtime selection. Not full Run, Plan/proof census, walk, replay, or public routing.** Layout inventory v18 is a separate accepted inventory unit; this source is **not** live-installed.
**Work tree:** `/tmp/opensip-implementation/m2-grok-view-joins-review-18/review`. Live, frozen, and history not edited. No commits.

The archived view-joins-boundary-18 advisory is **not** acceptance and **not** a fresh-blind of this source.

## Subject pin

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/trials/view-joins-18/subject.json` | 49572 | `ebd25f0c5527cb45c0f5cd825a79356ebf931061caa9a861aa88946925148fbb` |
| adjacent `subject.tar.gz` / `archive-pin.json` | 24903090 | `9d32e8878a60cc80fcfda4024e599c13b4c112edff2405b6a711cabc140483fb` |
| adjacent `view-result.json` | 321 | `de84d65d038594ba19a2148798c52ae441fbd189c673fe23864735bb91988c48` |
| adjacent `oracle-scope-account.json` | 1560 | `255afb5b32c8ce98121f7a9a4fa602f546500d1e8d406082a4f95ef06763a50d` |
| export | `/tmp/opensip-implementation/m2-view-joins-subject-18` | 277/277 member pins match; tar 277/277; 0 extra; 0 missing |

277 `files[].path` values are unique and string-sorted.

Dependency pins hash-match: coverage-producer-17 subject `6d4d2cd8…e84e`; runtime-v7 unit `5346a18c…a61a`; inventory-v18 subject `f7376661…4001`; view-joins-boundary-18 advisory `0787682c…a38d`; selected identity 619d `619d6e3c…41e6`; selected native e678 `e6784aa1…e2b9`.

Live lock independently observed **16 inventory / 20 contract** (last inventory **candidate** v18; last contract native-runtime v7). Live tree has coverage producer from v7 and **no** `view_joins.rs` / `view-joins-registry.json`.

## Source delta vs frozen 17 / live v7

**233** prior product files byte-identical to frozen coverage-producer-17, including identity `closure.rs`, identity source-policy, `coverage.rs`, and evaluator `Cargo.toml`. No new crate dependency. External TCB unchanged.

Changed: `lib.rs` export; host tests/fixture; `capability_support.rs` **`pub(crate) fn eligibility` only** (body otherwise identical to live v7 / frozen 17). **New:** `view_joins.rs` / `view-joins-registry.json`.

| Path | Bytes | SHA-256 |
| --- | ---: | --- |
| `product/crates/evaluator/src/view_joins.rs` | 15794 | `ec5fa2487e330e419dacfe1aae778cf0ab456ffaa61d03394fe177f2c8c07bda` |
| `product/crates/evaluator/src/view-joins-registry.json` | 9498 | `fda05673098e1c099666ad47df0a3df9f782e3067b4d6ac0dd75dfbb0487d673` |

Closed registry `ladders` equals `coverage-registry.json`. `partitionLaw.refusal` is `SUBJECT_SCOPE_PARTITION_OVERLAP`; enumerator kind is `provider`. Adjacent `registry-sources.json` pins relation-payload-v2, identity-v3, and the coverage registry.

Host fixture **4160885** bytes (`b5eb5874…1ef8`) is under the 4 MiB production parser cap; host tests keep explicit per-request object/blob **indices** into a shared pool.

## Law vs selected I per-view block 1853–1948 (619d)

`inspect_view_joins(inputs, run_id, view_id, budget)` rehashes retained Run → Plan/snapshot/evidence, then the selected view (`ViewNotSelected` if `viewId` ∉ evidence.viewIds). No caller row, cached ADMIT, or Plan-count token.

Selected order, independently confirmed in source:

1. `VIEW_PLAN_JOIN` / `UNSELECTED_PRODUCER`.
2. Each scope: `SCOPE_SOURCE_JOIN`, **`UNSELECTED_ENUMERATOR`**, `ENUMERATOR_CLOSURE_KIND` — **before** partition.
3. Partition over **all** view scopes (including no-coverage); overlap reports UTF-8 **byte-min** subject (`partition-byte-min` reports `"\n"`).
4. Facts: `FACT_SOURCE_PRODUCER_JOIN`, existential `FACT_SCOPE_JOIN`, snapshot anchors; UTF-8 **prefix and span only** (unused invalid tail is lawful: `golden-anchor-utf8-unused-invalid-tail` checked). Split prefix/span refuse `ANCHOR_UTF8`.
5. `VIEW_COVERAGE_JOIN`; **every** retained-scope ladder (`SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER`).
6. Per coverage: `COVERAGE_SCOPE_JOIN`; unresolved bag from **this view’s facts only**; lazy `frame_candidate` rehash of actual universe bytes for eligibility (`pub(crate)`); **actual 17 producer** → **`COVERAGE_ADMITTED_IDENTITY`** → **16 `inspect_coverage_prerequisites`** → file inventory totality. Foreign-universe facts cannot discharge totality (`typescript-foreign-universe-cannot-pay-totality`).

In-view extra unresolved-edge with claimed complete is `COVERAGE_PRODUCER_ADMISSION` / RC-2. Outside-view retained unresolved facts are irrelevant (`golden-typescript-view-edges-False-0` checked). Unselected enumerator refuses **before** overlap (`UNSELECTED_ENUMERATOR`). `steps==0` is `ViewJoinError::Limit`.

Earlier walk/Plan-native/proof census and later imports/replay are **not** this API. Some unused foreign-universe fixtures are deliberately local.

## History

- Initial unresolved-edge fixture referrer `a.ts` violated SubjectIdV1; corrected to `symbol:fixture`. No source-code fix; `initial-unresolved-fixture.stderr` preserved.
- Initial 22-host membership lists grew the fixture to 4299022; script asserted **before write**. Indexed pool reduces to **4160885** under the unchanged 4 MiB cap. Initial oversize script preserved.
- One Clippy `needless_question_mark` before final corpus; no semantic change.

## Reproduction (independent, rustc 1.95.0, `--locked --offline`)

- Frozen 241-row actual/expected independently classified: **241/241**, **158 checked**, **0 mismatch**.
- `cargo test --locked --offline -p opensip-host view_joins --lib` on the **export** product: **ok** (22 host controls including UTF-8 tail/prefix/span, partition byte-min, foreign-universe totality, enumerator-before-overlap, `steps:0` Limit).
- Identity policy independently passed: `sourceFilesVerified: 110`. Frozen workspace.stdout sums to **103**. Clippy `-D warnings` compile-only.

Did not re-pipe 177 MiB `view-requests.ndjson`. Did not re-exec Unicode-15 or 07–12 corpora.

## requiredFindings

None.

## Limits (not required findings)

- Local counters are not ADMIT, Plan selection, proof-root census, `close_run`, or ReplayedRun.
- Lazy frame rehash is not `UNIVERSE_FRAME_UNRETAINED` / full walk.
- Payload parse of this view’s unresolved-edge/file facts re-runs `inspect_syntax_fact`; that does not replace walk-time syntax/body owners.
- Some unused foreign-universe fixtures are local, not FullRun validity.
- Layout inventory v18 names these files; live runtime v7 does not install them.
- Did not re-pipe the 177 MiB request corpus through a rebuilt harness.

## Verdict

No required findings. Private `inspect_view_joins` matches the selected per-view block: enumerators before partition, this-view unresolved bag, producer then coverage-identity then 16 guards then totality, UTF-8 prefix/span only, byte-min overlap, closed metadata, `pub(crate)` eligibility only. Not a live/runtime/full-Run selection.
