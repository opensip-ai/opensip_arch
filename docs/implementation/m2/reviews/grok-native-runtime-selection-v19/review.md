# Native-runtime selection v19 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Frozen source41 is composed, not re-accepted here. Inventory28 is not a parent and must not be selected before this runtime19 activation. Source43 policy work is out of scope. Root assent and private activation remain required.

**subjectManifestSha256** `0307bbf0ae8b61d1852444d67392509fa630116625cc94c7b65803ba8f6fb08e`  
`docs/implementation/m2/native-runtime-selection-v19-subject.json` **16828** bytes, **75** members, 74 successor candidates + successor record, paths sorted unique, **0** pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v19/successor.json` **17397** / `05be52901aab5df654394b5c1ee1e18fa08fa05499ae47c9a9994c30cfed7eff`. `passageOverrides` is `[]`. Candidates cover the subject minus the record; each candidate pin equals the subject row. Parents sorted; none overwrite a subject member.

## Parents (`contract_successor` 221–229)

Live lock **25 inventory / 37 contract** (`75079` / `813aa62f39230b654ca6856266d292be6c83eae070f7a2748e6bb9e4e9a5b4ac`). Independent `verify_design.py` on the export **passed** (`productQualification: false`); selected inventory **v27**. All three parents match disk and the live accepted set.

| Parent | Bytes | SHA-256 | Live class |
| --- | ---: | --- | --- |
| inventory **candidate** v27 | 149414 | `202d9233ffa696b1c9f8b2777a3c4f76f5781a092b095be23e10bdfa148c59bc` | last inventory; 399 files, 20 packages |
| runtime-18 successor | 22076 | `7824be204290185b5c1197aefbb1f6477437c6591947682b31306daa0c408ad1` | contract record |
| locator-totality (reference42) successor | 3210 | `fdeff745cc1b40477b2f2fbe3692ce8c86ea99910a75705ec7c792c3f27cfa7c` | last contract record |

Four live inheritance rows remain parented at **v27** with `before` equal to v27 descriptions: `/files/7` `bootstrap.rs`, `/files/13` report `package.json`, `/files/205` `package.json`, `/files/272` `imported-v1.schema.json`. Zero passage overrides. Inventory **v28** is not a parent.

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-19/subject.json` **50459** / `a0f6134c77e385eaf6e02bce68b2d4be903386f1b7c22fc25146d720fd7ece12` (evidence copy byte-equal). Export `/tmp/opensip-implementation/m2-native-runtime-subject-19`: **277/277**, 0 extras. Archive pin `docs/implementation/m2/trials/native-runtime-19/subject.tar.xz` **1790108** / `a930d52842640cd8b0566f57ebb6e2ae76dc20efe2888e1acbd23ab94653084d`.

**260** product files excluding workspace `Cargo.lock` are byte-identical to frozen source41 (`trials/enumeration-join-41/subject.json` **105409** / `75b752ebda569d1ad94b1cf069d03cd5d412b9d46a18ad1733d8e93c84d49b77`; export `/tmp/opensip-implementation/m2-enumeration-join-subject-41`). `product/design-lock.json` equals current live 25/37. `target-attribution-v2.schema.json` and nested typescript-boundary fixture `design-lock.json` retained. Workspace `Cargo.lock` equals frozen 41.

Materialization map **9** owned paths, all inventory-27 planned. Versus runtime-18 product: **3** new + **6** changed owned files (plus live lock update, not a mapped source):

| Kind | Paths |
| --- | --- |
| new | `enumeration_join.rs`, `enumeration-registry.json`, `enumeration-join-fixtures.json` |
| changed | `enumeration.rs`, `lib.rs`, `native_universe.rs`, `native_owner_tests.rs`, `closure.rs`, `tools/identity/dependency-policy.json` |

Every map pin equals architecture candidate copy and export. Evaluator still depends only on identity. `policy.rs` remains live 16386 / `57637018…` (no source43 `inspect_evaluator_parameters`).

`evidence/design.stdout` **375506** / `0023d2bdb8dc2cb7f2918f8736173565b5f33440c9242fc32828c8f7a6f116a7` equals `export-design.stdout`. Independent `verify_design` on this export is **byte-equal** that file (`passed: true`, selected inventory v27). Preflight used `--feature-profile toml-workspace`.

## Source41 (archived, not re-accepted)

Report `docs/implementation/m2/reviews/grok-enumeration-join-source-41/report.json` **3758** / `ad3705074cd89cad1d6d4980019e6150a66643794fffc355316781ff0ed81803`, verdict **NO-REQUIRED-FINDINGS**. Root disposition **521** / `946d475d05f6991654a0c7e252c190ca7e530888b8f49852966eec34abb912cd`. Kernel41 advisory/addendum archived byte-equal the original private reports (`8f835080…`, `628cc594…`). Reference42 is a separately selected parent; historical sources unchanged. Clippy `-D warnings` and 1516 typed-list / 21 excluded non-list / 34 host cases are in that completed source review, not re-blinded here.

Public owner: `inspect_enumeration_join` derives inventory digests from shaped ProofInputRef values; typed owner/schema/missing/local-limit `Err` before join; reference ADMIT/REFUSE document after preconditions; refuse empties population. Opaque inert diagnostic. No caller maps, full Run, execution-input selection, predicate replay, or custody. Schema-failed Bool ordinal aliases diagnostic only. No Float JSON-C in mapped Rust.

## Guards and isolation

Identity policy independently **passed**: 8 registry tuples, **299** sources, parse-only pins. Frozen identity-deps stdout matches.

Contracts `toml-workspace`: `serde_core` `alloc,result,std` (adds only `alloc` vs standalone). No new dependency features.

Host isolation receipt: **141** sources pin-equal export, **23** archives, `sourceAndLockUnchanged`. tests.stdout named **130** + doctest **1** = **131**. Provider isolation **rebuilt** for identity helper: **26** sources pin-equal export, **19** archives; three unavailable outputs are the intentional “native analysis is not implemented” message. Host fixture **34** cases (20 reference documents + 14 typed-err controls).

## requiredFindings

None.

## Limits / not claimed

Not live write. Not source41 re-acceptance. Not inventory28 selection. Not source43. Not full M2, native compiler provider, Run, replay, custody, or release. Standing is root assent + private activation after this review.
