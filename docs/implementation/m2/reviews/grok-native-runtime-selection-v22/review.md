# Native-runtime selection v22 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Frozen source46 is composed, not re-accepted here. Private 47 Plan-policy/input structure is out of scope. Complete first-evaluation structural closure, predicate truth, reconstruction, replay, and custody remain separate. Root assent and private activation remain required.

**subjectManifestSha256** `5ca6c4d78829714bca383b50fcc8160878dc4cd96fde29c394f2ab9f74f37eca`  
`docs/implementation/m2/native-runtime-selection-v22-subject.json` **16135** bytes, **72** members, 71 successor candidates + successor record, paths sorted unique, **0** pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v22/successor.json` **16495** / `15601e17c019cdd882568897f8d43832902e372dd8f392ca30aeec41d243911f`. `passageOverrides` is `[]`. Candidates equal the subject minus that record. Parents sorted unique.

## Parents

Live lock **28 inventory / 40 contract** (`81145` / `159dc8b9affa9074cbccf92eea5fe217b4f68e0048c7ee74fe89d5cb5820d52a`). Export `product/design-lock.json` is byte-equal that lock. Independent `verify_design.py` on the export **passed** and is **byte-equal** `evidence/design.stdout` **418899** / `bcc9ec22f34931270a0e5e1e7caab8c5c769d2cc023f88d409f27960ee86ca61` (also equals `export-design.stdout` and host-isolation `design.stdout`). Selected inventory **v30**.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| inventory **candidate** v30 | 152687 | `487c36323deb7235453b1f22f55192d273b6f67c7143010d5a9a156c051aa6fd` | last inventory candidate; **405** files, **20** packages |
| runtime-21 successor | 16475 | `8c005e680b223c604a51f2f8cff31021fabb7c306f9bcb417333ec8cd7bac99b` | last contract record (`ACCEPTED-DESIGN-UNIT`) |

Four inherited descriptions are already parented at **v30** with JSON pointers `/files/7|13|211|278/description`, projecting by stable path to `apps/cli/src/bootstrap.rs`, `apps/report/package.json`, `package.json`, `schemas/sources/imported-v1.schema.json`. Zero passage overrides. This unit does not insert inventory rows, so those indices stay.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-22/subject.json` **51624** / `f0f022e1a577c0cce40f8847df97a3b922064ece86e9b0130f22338ba0e38bf3` (evidence copy byte-equal). Export `/tmp/opensip-implementation/m2-native-runtime-subject-22`: **283/283**, 0 extras. Archive **1890584** / `037dced9ea4413e1d15abce8a5d324667c51a5948ab4d01523bf84c9b77882bb` matches trial and evidence `archive-pin.json`.

**266** product files excluding workspace `design-lock.json` are byte-identical to frozen46 (`m2-execution-inputs-subject-46/product`; subject `dfd49eef…75c5`). Entire export product tree (267 files including lock) equals frozen46 product. Nested typescript-boundary fixture `design-lock.json` and `Cargo.lock` retained.

Materialization map **6** owned paths, all inventory-30 planned. Versus runtime-21 `baseline.json` **263** files: **2** changed + **4** new:

| Kind | Paths |
| --- | --- |
| new | `execution-registry.json`, `execution_inputs.rs`, `execution_reader.rs`, `execution-input-fixtures.json` |
| changed | `lib.rs`, `native_owner_tests.rs` |

Every map pin equals architecture candidate copy and export. Evaluator still depends only on identity. Identity sources, dependency-policy, and `Cargo.lock` are byte-equal runtime-21. Identity policy evidence: **299** sources, 8 parse-only tuples, passed. Contracts `--feature-profile toml-workspace` unchanged.

Public owner: `inspect_execution_input_join` — Plan/execution/evaluator locators + shaped refs; exactly one capture; exact `selectedRefs ∪ {self}`; one-pass promises; parameter/enumeration/Plan view/import/stage prerequisites; private kernel; late semantic REFUSE keeps diagnostics. No synthetic Run, proof outputs, caller ADMIT, maps, or store census. Plan45 wrappers remain exported. `inspect_first_evaluation_structure` is **absent** (private 47).

## Source46 (archived, not re-accepted)

Report `docs/implementation/m2/reviews/grok-execution-inputs-source-46/report.json` **6019** / `e05b72c7ef4df553fce5739e6ad63a28ce9d32ea3bf09aa7f8cd3f790a9e24af`, verdict **NO-REQUIRED-FINDINGS**. Root disposition **545** / `de0f8a3f8878acdbfbccfe54b8f383a440d888eb31cc6f4bcfdd2532676af771`. Formal composition only. Portable 139 = 134 production + 5 injected test-only probes is source46 evidence, not re-run here.

## Guards and isolation

Host isolation **fresh**: **147** sources, **23** archives. tests.stdout named **133** (host crate **57**, including `execution_inputs_recheck_retained_selection_and_capture_without_outputs`). Composition/workspace **134** is that plus the extra workspace crate test (frozen46 workspace sum **134**). Independent host fixture test: **ok**. Fixture **51** cases: **18** no-output originals + **4** semantic refusals + **29** controls.

Provider isolation **carried**, no new build: **26** sources and **19** archives **byte-equal** runtime-21 provider receipt. Three unavailable commands expected exit 1. `nativeCompilerIntegrationImplemented: false`.

## requiredFindings

None.

## Limits / not claimed

Not live write. Not source46 re-acceptance. Not private 47. Not complete first-evaluation structural closure, predicate truth, reconstruction, replay, custody, native compiler provider, or M2/release. Standing is root assent + private activation after this review.
