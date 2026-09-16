# Native-runtime selection v6 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Root assent and private activation are still required. The archived capability-support-16 source review is **not** runtime acceptance and **not** a fresh-blind of this unit.

**subjectManifestSha256** `a281b51ef4f07383cb50bfeeb86138624b98685310e71f69b453cbce8e57b547`  
`docs/implementation/m2/native-runtime-selection-v6-subject.json` **15650** bytes, 70 members, 69 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

## What this unit is

Composes frozen capability-support-16 onto the **current live 14 inventory / 18 contract** base as **7 owned product inputs**. Inventory v16 is the selected inventory **candidate** (377 files, 20 packages/DAG). New evaluator `capability_support.rs` + closed `capability-support-registry.json`, `lib.rs` export, host tests/pooled fixture, `registered_record_shape` in `closure.rs`, and one local identity source-policy pin.

Does **not** include editable Coverage-17. Does **not** implement the Coverage producer.

## Parents (no inventory-record-as-contract)

| Parent | Live class |
| --- | --- |
| `capability-totality-reference-selection-v1/successor.json` `6421e727…f064` | accepted contract record |
| `native-runtime-selection-v5/successor.json` `09348f31…b593` | accepted contract record |
| `recognition-derived-reference-selection-v1/successor.json` `4b771e6e…4711` | accepted contract record |
| `repository-file-inventory.v16.json` `2da370ad…0438` | accepted **inventory candidate** |

Parents sorted. Disk pins match. `capability-support-inventory-v16/successor.json` is **not** a parent.

## Composition

Implementation subject `docs/implementation/m2/trials/native-runtime-06/subject.json` **45305** / `96d012a4d0d5d2975e4c4744b894729c8336bf69b9904863235940db4661f77b`. Archive **2518666** / `95d33a24807178ae22930b07a627ba142973a61726e7f415621656033bcfe477`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-06`: **249/249** members, tar 249, 0 extra, 0 hash mismatches.

**234** non-lock product files are byte-identical to frozen capability-support-16. The only product change vs 16 is `design-lock.json` (current live 14/18 base `b3aff3e9…bc16` / 44479). Materialization map **7/7** pins match unit product and export.

Identity TCB vs accepted runtime v5: external packages/features/archives unchanged (sha2-const-stable 0.1.0, tinyvec 1.13.3, unicode-normalization 0.1.24). Only `localSources[src/closure.rs]` pin updates `49900/7f6ea3be…` → `50730/72a73d74…`. Evaluator and identity `Cargo.toml` unchanged vs live. Body15 `body_identity.rs` unchanged vs live v5. No new package, production edge, or schema document. Host→evaluator remains **dev**.

Host fixture `native-context-fixtures.json` **4158383** bytes (`eabc4129…56ae`) is under the 4 MiB production parser cap; host tests keep explicit per-request `blobDigests` membership.

## Law (7 mapped files; 16 advisory not re-tried as blind)

`inspect_syntax_fact` is walk-time, before Plan: crate-private universe frame inputs then actual context owner; compiler universes skip; syntax uses **selected grammar row suffixes**; inventory capabilities are exempt. No `inspect_plan_native`, no caller ADMIT.

`inspect_coverage_prerequisites` rehashes Coverage/scope/snapshot via inert `registered_record_shape` (exact schema-document digest, raw schema bytes, canonical payload, shape) then runs **dialect ownership → syntax → source-variant**. Disclosure is derived from the committed universe, not a producer claim. Empty scopes are not vacuously complete. Gate counts are not Plan/Run authority. Full Coverage **producer** is not this unit and, in FullRun, must run **before** these guards.

Generic identity `inspect_relation_sources` still `Unsupported("relation body identity owner")`. `steps==0` is `NativeSupportError::Limit`.

## Evidence (root isolation + composed base)

Recorded, internally consistent:

- Host isolation: **116** sources, **18** verified archives, workspace tests **100** + evaluator doctest **1** = **101**, help/version exit 0. Commands use `m2-native-host-isolation-06`.
- Provider isolation: **25** sources, **14** archives, three honest unavailable cases (exit 1, “native analysis is not implemented”).
- Source-guard **64** tests OK; design **passed** (selected inventory v16); contracts-dependencies passed; identity-policy **110** files; host edges passed (`opensip-evaluator` → identity only; host→evaluator is **dev**). Six composed-base preflight commands exit 0; standing says v6 still unselected; command paths are `candidate-06`.

Independent this review (export, rustc 1.95, `--locked --offline`): identity-policy `passed` / 110 / 3 tuples; host `native_support_uses_selected_suffixes_and_derives_empty_view_disclosures` ok. Did not re-pipe 476 MiB support requests (archived source review classified frozen 660+8). Did not rerun million-scalar Unicode or 07–12 corpora.

Archived capability-support-16 source review pin-matches `evidence/prior-advisories.json`: `d8aed94f…60d6` / 6450, verdict NO-REQUIRED-FINDINGS, not runtime acceptance.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, Coverage producer, full Run, Plan-count authority, graph completeness, custody, native execution, or release. Isolation trusted-host linker/SDK limits remain. Materialization-map `standing` still says “retained body diagnostic inputs” (v5 template wording); README and successor standing name capability-support correctly. Standing for **this** unit is still root assent + private activation, not a live write. Coverage-17 editable is not this unit. Live tree still lacks `capability_support.rs`.
