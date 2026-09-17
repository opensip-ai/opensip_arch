# Native-runtime selection v17 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. SOURCE-34/35 are **not** re-accepted. Root assent and private activation remain required.

**subjectManifestSha256** `b934097ad8ecdfbcba833cfa3b2ad5079b77d8d55fdf57fe03e30b4800df1453`  
`docs/implementation/m2/native-runtime-selection-v17-subject.json` **11030** bytes, 50 members, 49 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v17/successor.json` **11769** / `d41ff9c87ae12162b92b22f04f16c4889d3639941cd67ef8c1250d826bbb4853`. `passageOverrides` is `[]`.

## Parents (actual `contract_successor` 223–226)

Independently rebuilt live accepted map (**14657** vs **46** lock inputs). All **four** parents pass `path`/`bytes`/`sha256`. None are `lock.inputs`. Inventory v25 **successor record** is not a parent.

| Parent | Live class |
| --- | --- |
| `enumeration_model.v1.py` `69b0eee3…fe85` / 49811 | **application-manifest** row; extra `beforeSha256: null` on the accepted copy; pin fields match |
| capability-totality-v1 successor `6421e727…f064` / 3596 | contract record |
| runtime-16-r2 successor `09874cda…8246` / 18225 | contract record |
| inventory **candidate** v25 `414a83c7…ae3e` / 146522 | 393 files, 20 packages |

Parents sorted. Four live inheritance `before` texts still equal v25 rows (`/files/7`, `/files/13`, `/files/200`, `/files/267`).

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-17/subject.json` **49324** / `f63c79cb97b25f2b46bb9b72d9899fd2a2ad6a2b0bdbc305b020b08cb02a77b1`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-17`: **271/271**.

**254** non-lock product files byte-identical to frozen SOURCE-35 (includes restored `target-attribution-v2.schema.json` and nested `tools/typescript-boundary/tests/fixtures/product/design-lock.json`). Only `product/design-lock.json` is current live **23/32** (`393a690e…b722` / 68099). Four mapped inputs pin-match SOURCE-35 (`enumeration.rs` 20457 / `cdbcadb3…`, `lib.rs`, host tests, fixture **2842447** / `16d873d3…` under 4 MiB). Fixture `cases` **3712** extent rows unchanged by value from SOURCE-34. Identity sources, Cargo.lock, and other fixtures unchanged vs SOURCE-35.

Independent `verify_design.py` on **this export**: **passed**, selected inventory v25, 23/32, `productQualification: false`. Source-guard 64, metadata, edges, contracts-deps, identity-policy **110** pass.

Law (archived SOURCE-34/35, not re-blinded): extent projection + membership diagnostics; `RegisteredSchemas` exact pins; root-first unit representation; snapshot coverage; UTF-8 order; deepest same-family rows; outside suffix/null only. **Not** full enumeration, packages, discovery, custody, or replay. 2025 membership cases = **2019** selected-reference + **6** local limits (SOURCE-35 JSON `referenceComparisons=2025` includes the six; root disposition `457d6591…83b7` states the narrower split; original report preserved). 124 workspace tests.

## Isolation and carry

Host isolation **136** sources / **18** archives / **124** tests (123 + 1 doctest), help/version 0. All 136 receipt sources pin-match this export.

Provider: **explicit carry**, no rebuild. 16-r2 receipt `c9b8c341…baed` / 11398; **25** sources pin-match this export. Identity files equal SOURCE-35 (unchanged from the rebuilt 16-r2 provider set).

Archived SOURCE-35 report `9a0aa6ce…df5a` / 4831 and SOURCE-34 `de03e583…ab3d` / 3472 are not re-accepted. Live still has **no** `enumeration.rs`.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, full enumeration, package parsing, discovery, security custody, Run, or replay. Standing is root assent + private activation, not a live write.
