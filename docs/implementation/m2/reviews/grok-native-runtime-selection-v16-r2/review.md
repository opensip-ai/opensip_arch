# Native-runtime selection v16-r2 — formal implementation-unit review

**Verdict: `ACCEPT-DESIGN-UNIT`**

Root remains lead. Not Claude agreement. Not live install. Frozen SOURCE-32 is **not** re-accepted. Original v16 unit and this reviewer’s NEEDS-CHANGES report are **preserved**. Root assent and private activation remain required.

**subjectManifestSha256** `9d1c600b639dc03587085f0a440c9ab372d627c4a5ba56d41a25adfe42e93729`  
`docs/implementation/m2/native-runtime-selection-v16-r2-subject.json` **17466** bytes, 77 members, 76 successor candidates + successor record, paths sorted unique, 0 pin mismatches.

Successor `docs/implementation/m2/native-runtime-selection-v16-r2/successor.json` **18225** / `09874cdac42e664559fa5bbe8c72f335354e6cdd3d1cf8eda7f57efcedef8246`. `passageOverrides` is `[]`. Ten mapped `candidatePath` values are under `native-runtime-selection-v16-r2/`.

## Correction of original v16

Archived original: unit subject `ca1e81cf…ccbf` / 16583; implementation `d9cb2079…7cb5` / 48431; review `bda9cdcc…cd99` / 6867 (`NEEDS-CHANGES`); root disposition `2254b15d…d46b` / 560 accepted the omission finding.

Cause: `shutil.ignore_patterns("target-*")` treated **`target-attribution-v2.schema.json` as a cache glob**, not only `target/` directories. Candidate-16 and host isolation already had the file; packaging the implementation subject dropped it.

r2 restores the exact inherited pin **23086** / `bd938f11c584be65e914bc1446193fdf3dd4a15f7b78630cc3eb628c5bca1d53`, copies from an **explicit SOURCE-32 product manifest**, and verifies **252** non-lock pins after copy.

**Future exports:** cache exclusion must apply **only to directories** (for example ignore a `target` directory), never a `target-*` filename glob over regular files.

## Parents (actual `contract_successor` 223–226)

Independently rebuilt live accepted map (**14576** vs **46** lock inputs). All **four** parents pass. None are `lock.inputs`. Inventory v24 **successor record** is not a parent.

| Parent | Live class |
| --- | --- |
| import-totality-v1 successor `ee921a88…f243` / 2892 | contract record |
| runtime-15 successor `0e69f1ec…8aab` / 11169 | contract record |
| inventory **candidate** v24 `332d47aa…bcb6` / 146038 | 392 files, 20 packages |
| stage-meta-v1 successor `129bceca…0cb5` / 10621 | contract record |

Parents sorted. Four live inheritance `before` texts still equal v24 rows (`/files/7`, `/files/13`, `/files/199`, `/files/266`).

## Composition

Implementation `docs/implementation/m2/trials/native-runtime-16-r2/subject.json` **49126** / `6c445dd0bd27cdd299cb6affe010fbc58bfd11cb6e752017d2399a311cd6927a`. Export `/tmp/opensip-implementation/m2-native-runtime-subject-16-r2`: **270/270**.

**252** non-lock product files byte-identical to frozen SOURCE-32 (0 omitted, 0 mutated). Only `design-lock.json` is current live **22/31** (`116fefcc…14e3` / 66066). Ten mapped inputs pin-match SOURCE-32 and the r2 candidate. Three **local** identity policy pins change; Cargo.lock, external TCB tuples, DAG, and prior native/import-joins/import-payload fixtures unchanged.

Independent `verify_design.py` on **this export**: **passed**, selected inventory v24, 22/31, `productQualification: false`. Source-guard 64, metadata, edges, contracts-deps, identity-policy **110** pass.

Law (SOURCE-32, not re-blinded): private `ClosedOwner`; default `RejectOwner`; public with-owner returns `StructuralChecks` only; no caller owner/registry/census/ADMIT on the complete API; registry `bodyIdentityJoin`; nested domain set; canonical map domain (advisory-33). 526 = 507 + 19; 122 tests.

## Isolation and archive

Host isolation **134** sources / **18** archives / **122** tests (121 + 1 doctest), help/version 0. All **134** receipt sources pin-match this export, including the restored schema.

Provider **rebuilt** (not v10 carry): **25** sources pin-match this export; **14** archives; **3** intentional unavailable commands (exit 1). Receipt bytes equal original v16 provider receipt (`c9b8c341…baed`) because the restored file is not a provider source; the three identity sources still differ from v10.

SOURCE-32 subject `c52cf367…ec96` unchanged. Selected archive remains **xz v2** `70587750…a9bd` / 3240476. Historical gzip pin not rewritten. Archived SOURCE-32 report `89a13ee2…84a1` / 5478 is not re-accepted.

Live still has **no** `full_walk.rs`.

## requiredFindings

None.

## Limits / not claimed

Not M2 complete, independent truth/replay, security, publication, or M3–M6. Not SOURCE-32 re-acceptance. Original v16 remains the historical NEEDS-CHANGES record. Standing is root assent + private activation, not a live write.
