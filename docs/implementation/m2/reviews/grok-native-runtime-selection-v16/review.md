# Native-runtime selection v16 — formal implementation-unit review

**Verdict: `NEEDS-CHANGES`**

Root remains lead. Not Claude agreement. Not live install. Frozen SOURCE-32 is **not** re-accepted here. The mapped ten inputs, four parents, rebuilt provider isolation, xz archive binding, and canonical-map-domain law otherwise check. Private activation is blocked until the composed product again contains every inherited SOURCE-32 / inventory-24 / live regular file.

**subjectManifestSha256** `ca1e81cffaeefc1548fb8414ed54eee4d79a41b06062e601338f693e3e91ccbf`  
`docs/implementation/m2/native-runtime-selection-v16-subject.json` **16583** bytes, 74 members, 73 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v16/successor.json` **17320** / `f802213423e29e09f9e8c53782505ae18b9c63c821e564f133b44195ac4b8aab`. `passageOverrides` is `[]`.

## requiredFindings

### 1. `composed-product-omits-inherited-target-attribution-schema`

Frozen SOURCE-32 product, live tree, inventory v24, host-isolation receipt, and runtime-15 composition all contain:

`schemas/sources/target-attribution-v2.schema.json` **23086** / `bd938f11c584be65e914bc1446193fdf3dd4a15f7b78630cc3eb628c5bca1d53`

The frozen implementation subject / export `/tmp/opensip-implementation/m2-native-runtime-subject-16/product` **omits** it (47 vs 48 `schemas/sources` files). That is **not** one of the ten mapped deltas. Independent `verify_design.py` on this export:

`Design verification failed: missing or escaping regular file: schemas/sources/target-attribution-v2.schema.json`

`source-composition.json` claims `sourceFilesExcludingLock: 252` / “All252nonlockfiles exactfrozen32”. Independently: SOURCE-32 has **252** non-lock product files; this composition has **251** matching + **1 missing**. Candidate-16 still has the file; packaging the implementation subject dropped it.

**Action:** Restore that exact pin into the implementation product (and re-export / re-pin the implementation subject). Re-run `verify_design` on the frozen implementation tree. Do not rewrite SOURCE-32. Do not drop the file from inventory v24.

## Parents (actual `contract_successor` 223–226)

Independently rebuilt live accepted map (**14576** vs **46** lock inputs). All **four** frozen parents pass. None are `lock.inputs`. Inventory v24 **successor record** is not a parent.

| Parent | Live class |
| --- | --- |
| import-totality-v1 successor `ee921a88…f243` / 2892 | contract record |
| runtime-15 successor `0e69f1ec…8aab` / 11169 | contract record |
| inventory **candidate** v24 `332d47aa…bcb6` / 146038 | 392 files, 20 packages |
| stage-meta-v1 successor `129bceca…0cb5` / 10621 | contract record |

Parents sorted. Four live inheritance `before` texts still equal v24 rows (`/files/7`, `/files/13`, `/files/199`, `/files/266`). This unit does not rewrite them.

## What otherwise checks

Implementation `docs/implementation/m2/trials/native-runtime-16/subject.json` **48431** / `d9cb20799ad8ed752c3d07dbd763253d6756af083d1f6e10ae5484f6c9117cb5`. Export **266/266**. Live lock **22/31** `116fefcc…14e3` / 66066; implementation lock **equals** live. Ten mapped inputs pin-match frozen SOURCE-32 (`full_walk.rs` 13104 / `01dd5478…`, fixture 3888036, three identity sources, etc.). Prior native/import-joins/import-payload fixtures, Cargo.lock, schemas DAG/TCB tuples unchanged. Only three **local** identity policy pins change.

Law (from frozen 32, not re-blinded): private `ClosedOwner` composition; default `RejectOwner`; public with-owner returns `StructuralChecks` only; no caller owner/registry/census/ADMIT on the complete API; registry `bodyIdentityJoin`; nested domain set; canonical map domain (advisory-33). 526/507+19 and 122 tests remain SOURCE-32 facts.

**Host isolation (new):** receipt **134** sources / **18** archives / **122** tests (121 + 1 doctest), help/version 0. Receipt **includes** the omitted schema; export does not — restore the file so the frozen implementation matches isolation.

**Provider (rebuilt, not v10 carry):** **25** sources pin-match this export; **14** archives; **3** intentional unavailable commands (exit 1). Exactly the three identity sources differ from accepted v10 receipt `3aa90b48…9139`.

**Archive:** runtime-16 evidence binds SOURCE-32 **xz v2** `70587750…a9bd` / 3240476 and `archive-pin.v2.json`. Historical gzip pin `a4fd601f…9f3e` is not rewritten. Subject `c52cf367…ec96` unchanged.

Archived SOURCE-32 report `89a13ee2…84a1` / 5478 and root disposition `f4f8568c…addb` / 651: no source re-acceptance here.

Other preflights on this export: source-guard 64, metadata, edges, contracts-deps, identity-policy 110 **pass**. Design **fails** on the omitted file.

## Limits / not claimed

Not M2 complete, independent truth/replay, security, publication, or M3–M6. Not SOURCE-32 re-acceptance. Standing remains root assent + private activation **after** the composition file set is complete.
