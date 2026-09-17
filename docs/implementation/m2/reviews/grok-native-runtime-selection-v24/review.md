# Native-runtime selection v24 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Frozen source48 is composed, not re-accepted here. Atom truth, full composition, replay, and custody remain separate. Root assent and private activation remain required.

**subjectManifestSha256** `e0cf6bb44771c7b688ca666ade5ca138d09cfa73e31b1451aec36d5db4a36a19`  
`docs/implementation/m2/native-runtime-selection-v24-subject.json` **15891** bytes, **71** members, 70 successor candidates + successor record, paths sorted unique, **0** pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v24/successor.json` **16469** / `1ad92c24ef6f0bceadbd71efa33482d87a3d00203bc724fab4e602f170bbf027`. `passageOverrides` is `[]`. Candidates equal the subject minus that record. Parents sorted unique.

## Parents

Live lock **30 inventory / 43 contract** (`86154` / `46268ef8be0e1094ed1e03b76e4d0134f6ea9fee0c0247495b6fa45add502be9`). Export `product/design-lock.json` is byte-equal that lock. Independent `verify_design.py` on the export **passed** and is **byte-equal** `evidence/design.stdout` **451665** / `6239a0323fd50653b84875a32920859ce167dc100d79d96f7a4ad6f985cb95ef` (also equals `export-design.stdout` and host-isolation `design.stdout`). Selected inventory **v32**.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| inventory **candidate** v32 | 154945 | `105a260d966ab0cd61a11798493cd970e114aab9380c003d5eec5c27c513b72e` | last inventory candidate; **409** files, **20** packages |
| runtime-23 successor | 17186 | `95bb1d57501fb06bc7bbf6a932fd5fe8f2508a5934471be89d4743997833b6b9` | contract record (`ACCEPTED-DESIGN-UNIT`) |
| reconstruction-closure reference v1 (49) | 4344 | `54e84aed05f26bdd1f5a8744157be17447f21ec4c0c318e0eb11dae6a2b960d6` | last contract record (`ACCEPTED-DESIGN-UNIT`) |

Four inherited descriptions are parented at **v32** with JSON pointers `/files/7|13|215|282/description`, projecting by stable path to `apps/cli/src/bootstrap.rs`, `apps/report/package.json`, `package.json`, `schemas/sources/imported-v1.schema.json`. Zero passage overrides.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-24/subject.json` **52419** / `5ef9552550f21be915f0eb2416442678529b6779ffa4300064cd185c0d3f4cfa` (evidence copy byte-equal). Export `/tmp/opensip-implementation/m2-native-runtime-subject-24`: **287/287**, 0 extras. Archive **2049800** / `114587574a9765e7fe9671373cd7828464b5872ace242c7cde4024a374605229` matches trial and evidence `archive-pin.json`.

**270** product files excluding workspace `design-lock.json` are byte-identical to frozen48 (`m2-reconstruction-subject-48/product`; subject `1e6111fa…8e0e`). Entire export product tree (271 files including lock) equals frozen48 product. Nested typescript-boundary fixture `design-lock.json` and `Cargo.lock` retained.

Materialization map **5** owned paths, all inventory-32 planned. Versus runtime-23 `baseline.json` **269** files: **3** changed + **2** new:

| Kind | Paths |
| --- | --- |
| new | `input_reconstruction.rs`, `reconstruction-fixtures.json` |
| changed | `full_walk.rs`, `lib.rs`, `native_owner_tests.rs` |

Every map pin equals architecture candidate copy and export. Evaluator still depends only on identity. Identity sources, dependency-policy, and `Cargo.lock` are byte-equal runtime-23. Identity policy evidence: **299** sources, 8 parse-only tuples, passed. Contracts `--feature-profile toml-workspace` unchanged.

Public owner: `reconstruct_evaluator_inputs` — invokes fixed 47 `inspect_first_evaluation_structure`, then derives population, rule enumeration, scanner evidence, observation joins, deficiencies, and counts. No synthetic Run, proof, caller ADMIT, or maps. Plan-named scanner closures; transitive native closures remain in retained store. Occurrence lists preserved; local budgets copied. `inspect_first_evaluation_structure` remains exported.

## Source48 (archived, not re-accepted)

Report `docs/implementation/m2/reviews/grok-reconstruction-source-48/report.json` **4791** / `7182d2e9ccfc441220f207f058514f8ec40e516b31af52b803a575af33369497`, verdict **NO-REQUIRED-FINDINGS**. Root disposition **495** / `480d2b7272ded03104b4721def5a92c693a446ae7972b0a45607ff468ba46d98`. Formal composition only. Portable 139 = 138 production + 1 injected probe is source48 evidence, not re-run here.

## Guards and isolation

Host isolation **fresh**: **151** sources, **23** archives. tests.stdout named **137** (host crate **61**, including `reconstructs_retained_evaluator_inputs_without_run_outputs`). Composition/workspace **138** = **137** named + **1** compile-fail doctest. Independent host fixture test: **ok**. Fixture **87** cases: **78** reference + **9** controls. Additional **324** pure helper comparisons are source48 evidence.

Provider isolation **carried** from fresh runtime-23, no new build: **26** sources and **19** archives **byte-equal** v23 provider receipt. Three unavailable commands expected exit 1. `nativeCompilerIntegrationImplemented: false`.

## requiredFindings

None.

## Limits / not claimed

Not live write. Not source48 re-acceptance. Not atom truth, full composition, replay, custody, native compiler provider, or M2/release. Standing is root assent + private activation after this review.
