# Native-runtime selection v20 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Frozen SOURCE43 is composed, not re-accepted here. Private 45 Plan-scoped work is out of scope. Root assent and private activation remain required.

**subjectManifestSha256** `875356297cb86b5e75ddc11de8686f0748464689aec95158b60372fac437356b`  
`docs/implementation/m2/native-runtime-selection-v20-subject.json` **15888** bytes, **71** members, 70 successor candidates + successor record, paths sorted unique, **0** pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v20/successor.json` **16247** / `f7bdc3dc465ec317a5e0911a8c663ee2310be2d79c3c4e9857775054377fc2c3`. `passageOverrides` is `[]`. Candidates cover the subject minus the record; each candidate pin equals the subject row. Parents sorted; none overwrite a subject member.

## Parents (`contract_successor` 221–229)

Live lock **26 inventory / 38 contract** (`77114` / `6f01a356d19644b6ab9f15429b2f553894882870df1adadd2a6eb23ecc0e2e73`). Independent `verify_design.py` on the export **passed** (`productQualification: false`); selected inventory **v28**. Both parents match disk and the live accepted set.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| inventory **candidate** v28 | 150007 | `b67c6101369e7ae76898c6997e5dae5f97bf9dc0c00f4a0ac3a1b923a4184240` | last inventory; 400 files, 20 packages |
| runtime-19 successor | 17397 | `05be52901aab5df654394b5c1ee1e18fa08fa05499ae47c9a9994c30cfed7eff` | last contract record |

Four live inheritance rows remain parented at **v28** with `before` equal to v28 descriptions: `/files/7` `bootstrap.rs`, `/files/13` report `package.json`, `/files/206` `package.json`, `/files/273` `imported-v1.schema.json`. Zero passage overrides.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-20/subject.json` **50680** / `48722272b5a6919c8c3908fbb253f6775ccd5afa9bcf6eab3f75b637445fd6c8` (evidence copy byte-equal). Export `/tmp/opensip-implementation/m2-native-runtime-subject-20`: **278/278**, 0 extras. Archive `docs/implementation/m2/trials/native-runtime-20/subject.tar.xz` **1798376** / `7fef44763c1118733786a7156283044665f4450201430624f0198da13bca94f3`.

**261** product files excluding `design-lock.json` are byte-identical to frozen SOURCE43 (`trials/evaluator-parameters-43/subject.json` **98111** / `c81b78dc…`; export `/tmp/opensip-implementation/m2-evaluator-parameters-subject-43`). `product/design-lock.json` equals current live 26/38. `target-attribution-v2.schema.json` and nested typescript-boundary fixture lock retained. Identity `Cargo.toml`, evaluator `Cargo.toml`, workspace `Cargo.lock`, and identity dependency-policy are byte-equal runtime19 (no identity/dependency/feature changes). Evaluator still depends only on identity.

Materialization map **5** owned paths, all inventory-28 planned. Versus runtime-19 product: **1** new + **4** changed owned files (plus live lock update, not a mapped source):

| Kind | Paths |
| --- | --- |
| new | `crates/host/tests/fixtures/evaluator-parameter-fixtures.json` |
| changed | `atom-registry.json`, `lib.rs`, `policy.rs`, `native_owner_tests.rs` |

Every map pin equals architecture candidate copy and export. Prior 43 advisory prerequisite is resolved: 256 unchanged non-lock files remain exact accepted19; the five owned files are the frozen43 delta.

`evidence/design.stdout` **390457** / `0041f8cb7850392b1d0bdae14637ec73b2f0161fb590d1ed3a2f3b85114ccff0` equals `export-design.stdout`. Independent `verify_design` on this export is **byte-equal** that file (`passed: true`, selected inventory v28). Preflight used `--feature-profile toml-workspace`.

## Source43 (archived, not re-accepted)

Report `docs/implementation/m2/reviews/grok-evaluator-parameters-source-43/report.json` **4776** / `c68c8fcbc0f9da2ed338efebb80b640597e2d3b010616e71aa5b747042624eb2`, verdict **NO-REQUIRED-FINDINGS**. Root disposition **539** / `24163cf68173facfcd1a6a8ac9d3804b37f34043c2a2d21767e920a40ec91845`. Bounded 43 advisory archived byte-equal the original (`6c7e81edd0…`). Clippy `-D warnings` and 132 workspace tests were independently reproduced in that freeze; 23 reference comparisons + 31 host cases (8 typed controls) likewise.

Public owner: `inspect_evaluator_parameters` derives required registered parameters, policy binding, ordered emission rule totality, fingerprint namespaces, universe/rule-program/detector-closure joins from retained Plan/spec/payload bytes. Opaque inert `selected`/`policy`/`emission`. No caller ADMIT maps, full policy compilation, enumeration join, execution-input selection, reconstruction, replay, or custody.

## Guards and isolation

Identity policy independently **passed**: 8 registry tuples, **299** sources. Contracts `toml-workspace` still adds only `serde_core` `alloc`.

Host isolation receipt: **142** sources pin-equal export, **23** archives, `sourceAndLockUnchanged`. tests.stdout named **131** + doctest **1** = **132**. Provider **26** sources pin-equal export **and** runtime19, **19** archives; three unavailable outputs remain the intentional unimplemented-analysis message. **No new provider build.** Host fixture **31** cases (23 reference result/refusal + 8 owner/resource).

## requiredFindings

None.

## Limits / not claimed

Not live write. Not SOURCE43 re-acceptance. Not private-45. Not full M2, native compiler provider, Run, replay, custody, or release. Materialization-map/preflight `standing` strings still carry leftover template prose; command paths and pins are the v20 candidate. Standing is root assent + private activation after this review.
