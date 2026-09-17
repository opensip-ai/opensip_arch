# Native-runtime selection v21 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Frozen source45 is composed, not re-accepted here. Private 46 execution helpers are out of scope. Full X selection, native Plan/enumeration, predicate truth, reconstruction, replay, and custody remain separate. Root assent and private activation remain required.

**subjectManifestSha256** `b039d62d7a1ed336d75dec0e3904bfe96432bf054ad6027cb3ee67b8a7680c66`  
`docs/implementation/m2/native-runtime-selection-v21-subject.json` **16112** bytes, **72** members, 71 successor candidates + successor record, paths sorted unique, **0** pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v21/successor.json` **16475** / `8c005e680b223c604a51f2f8cff31021fabb7c306f9bcb417333ec8cd7bac99b`. `passageOverrides` is `[]`. Candidates equal the subject minus that record. Parents sorted unique.

## Parents

Live lock **27 inventory / 39 contract** (`79122` / `08e5478eaa6973eb159b656e4920c55c5d62a96d495ab5b44a1d179f0cd9c00e`). Export `product/design-lock.json` is byte-equal that lock. Independent `verify_design.py` on the export **passed** and is **byte-equal** `evidence/design.stdout` **404580** / `00b7d1bc0615d8aab258af00527a8ba7dafbbb1bc5ce3be2962499969240461c` (also equals `export-design.stdout` and host-isolation `design.stdout`). Selected inventory **v29**.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| inventory **candidate** v29 | 150565 | `0a255a7161519352e589069566fc5cafa3e59f1ef8ac0d3d33a0cc9f3ee2ffc0` | last inventory candidate; **401** files, **20** packages |
| runtime-20 successor | 16247 | `f7bdc3dc465ec317a5e0911a8c663ee2310be2d79c3c4e9857775054377fc2c3` | last contract record (`ACCEPTED-DESIGN-UNIT`) |

Four inherited descriptions project by **stable path** to v29 1-based rows **7 / 13 / 207 / 274**: `apps/cli/src/arguments.rs`, `apps/report/package-lock.json`, `docs/report.md`, `schemas/sources/import-source-context-v1.schema.json`. Each path’s description equals v28. Zero passage overrides.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-21/subject.json` **50870** / `89d6305b8be82309f3c625a9938ca59dc322f50b5db345359fda8c97c5753ac1` (evidence copy byte-equal). Export `/tmp/opensip-implementation/m2-native-runtime-subject-21`: **279/279**, 0 extras, 0 pin mismatches. Archive `docs/implementation/m2/trials/native-runtime-21/subject.tar.xz` **1843820** / `044296930127ad1f71a6c4de7aa1bc757459b6473a38e9aa45a1fa8321a37f02` matches trial and evidence `archive-pin.json`.

**262** product files excluding workspace `design-lock.json` are byte-identical to frozen45 (`m2-plan-input-owners-subject-45/product`; trial `92f60984…1bc47f`). Nested typescript-boundary fixture `design-lock.json` and `Cargo.lock` retained. Entire export product tree (263 files including lock) equals frozen45 product.

Materialization map **6** owned paths, all inventory-29 planned. Versus runtime-20 `baseline.json` **262** files: **5** changed + **1** new:

| Kind | Paths |
| --- | --- |
| new | `crates/host/tests/fixtures/plan-input-fixtures.json` |
| changed | `view_joins.rs`, `import_joins.rs`, `stage_output.rs`, `lib.rs`, `native_owner_tests.rs` |

Every map pin equals architecture candidate copy and export. Evaluator still depends only on identity. Identity `lib.rs` / `closure.rs` / `canonical.rs`, identity dependency-policy, and `Cargo.lock` are byte-equal runtime-20. Identity policy evidence: **299** sources, 8 parse-only tuples, passed. Contracts `--feature-profile toml-workspace` unchanged (`serde_core` alloc+result+std).

Public owners: `inspect_plan_view_joins`, `inspect_plan_import_joins`, `inspect_plan_stage_specs`. Shared Run tails preserved (snapshot from Run on the Run import wrapper; seal→execution-plan on the Run stage wrapper). Plan wrappers take Plan/execution-plan/shaped `ProofInputRef`s; no synthetic Run, proof output, or caller ADMIT. Wrapper bytes equal bounded advisory45 pins (`9ab7fae9…`, `6f74728c…`, `6d6340e9…`, `e4668383…`). `full_walk.rs` still calls the Run wrappers.

## Source45 (archived, not re-accepted)

Report `docs/implementation/m2/reviews/grok-plan-input-owners-source-45/report.json` **7026** / `9e1ca3d9031666d1ea3435c66924ec84aab58de221a1105e02c0de4c22df2f64`, verdict **NO-REQUIRED-FINDINGS**. Root disposition **540** / `d30fc4f1b5ff0361768d275ba62283127185b46fbfbbcac946a77211a71a7676`. Bounded advisory45 **2724** / `fe30d17e1e90bb07cdbcc9e7f874bfa638da142a4a98368dc068cee626f4ea15` (this reviewer’s prior unit, not re-opened). Formal composition only.

## Guards and isolation

Host isolation **fresh**: **143** sources, **23** archives. tests.stdout named **132** (host crate **56**, including `plan_input_owners_require_no_run_or_proof_output`). Composition/workspace **133** is that plus the extra workspace crate test (same split as prior runtimes). Independent host test of the 69-case fixture: **ok**. Fixture standing: no Run/seal/proof/finding/semanticEvidence/evaluationSubject/predicate objects. **42** no-output packets from 10 owner-admitted references + **27** controls = **69**.

Provider isolation **carried**, no new build: **26** sources and **19** archives **byte-equal** runtime-20 provider receipt. Three unavailable commands expected exit 1. `nativeCompilerIntegrationImplemented: false`.

Preflight `toml-workspace` + identity policy + edges against inventory v29, all exit 0. `source-guard-tests` exit 0. Preflight `standing` still mentions older runtime-v19 template prose; exact pins/README/source-composition define this unit (same class of historical packaging text accepted on runtime-20).

## requiredFindings

None.

## Limits / not claimed

Not live write. Not source45 re-acceptance. Not private 46. Not full X capture selection, native Plan bind, enumeration join, predicate truth, reconstruction, replay, custody, native compiler provider, or M2/release. Standing is root assent + private activation after this review.
