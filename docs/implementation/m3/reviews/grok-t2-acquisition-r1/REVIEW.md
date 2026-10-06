# Pinned public T2 acquisition and declared overlays r1 — ACCEPT

This accepts the pinned acquisition archive: 49 manifest entries fetched and verified, 49 canonical admission receipts, and five declared workspace overlays. Two of those overlays have the defined Cargo patch rendering. The npm and Python native renderings stay undefined. T1, native context, preparation, provider launch, full G2, product qualification, O1-a, and the owner/day0 gates remain open.

## Subject

The subject manifest is `docs/implementation/m3/corpus/t2-acquisition-2026-10-06-r1-subject.json`, 13901 bytes, sha256 `90cadf1bb85d160c324cd8a1462246d947c62f487cf5b3e10541a7d33088510f`. It lists 61 archive members. Every member's bytes and sha256 match the file under `/tmp/opensip-implementation/t2-acquisition-stage`. The manifest file is the only staged file outside that list. The archive proposes no product edit, no inventory successor, and no design-lock change.

Product `HEAD` is `5b97e57a7c1d23fe4f5fd256a8b42459557572bb`. Architecture `HEAD` is `4cabaa174bf0e6fd647206e7c3c9a94461b86f79`. Both are the pinned bases. The accepted T2 manifest is 322483 bytes, sha256 `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`. `FETCH-SPEC.md` is 10659 bytes, sha256 `4ebe90a491721e48d252f11e6378b6c73312b506b59af89b24c03829416f8858`. Those hashes match the worktrees and the blobs at the pinned commits. The five accepted K1 sources match the same way: `canonical.py` 2463 / `98579f7d151ed35e50b5a8e5d56f015d8fd86861676378135e69a36f617d2876`, `corpus.py` 4839 / `539f158fd07b60d27e776f2137e2f0c9f651db98b2ac8cec742e28ce0b1bb6c7`, `fetch.py` 9051 / `acc9639eef4435b36794ce5b31c8896e50d5fa75ea0e8ad5bbd2d94350fea76e`, `records.py` 11416 / `1e753f5701278e463d390b4006d4076b7b59cca53626a3a6672413138d49a744`, and `store.py` 9504 / `5fd74f14479a3e502dcf763ca3b52094f2da5c5385f28dab50fb7cc18aee0f28`. The manifest and those libraries stay accepted bases.

The manifest has 49 repository entries and five workspace definitions. Its algorithm ids are `opensip-qd22-tree-sha256/1` and `opensip-t2-content-sha256/1-draft`. The 49 tree digests are unique.

## Acquisition

`acquisition.json` is 20426 bytes, sha256 `84fbfeb9d8f6ebf5c973215f677353506377ce467a569b8dba3ef3d3f63d1df7`. Standing is pinned public T2 acquisition. It records 49 `VERIFIED` rows, zero refusals, and `reused: false` on every row. The row order is the manifest order. For every entry, the reported tree digest and content digest equal the manifest values. `elapsedSeconds` is present on every row and is finite. That report is pretty-printed JSON. Those timings stay on the acquisition report, outside the canonical admission records. The run started at `2026-10-06T17:18:47.490497+00:00`, finished at `2026-10-06T17:23:30.505893+00:00`, and records nice 10, scratch `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-t2-fetch-6qxo1q07`, and git executable `/usr/bin/git`. `T1ProducerRan`, `repositoryCodeExecuted`, `heldOutInspected`, `providerLaunched`, `productQualification`, and `HOMEChanged` are false.

`fetch-all.py` is the archived adapter. It checks the manifest pin, then replaces `fetch.command` so the argv still begins with the accepted `git` arguments and the executable is `/usr/bin/git`. The owner-fixed `PATH` recorded by the script is `/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin`. That path contains no Git executable. `/usr/bin/git` is present. The accepted `git_environment` keeps the process `HOME`, drops incoming `GIT_*` variables, and sets `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_TERMINAL_PROMPT=0`, `GIT_LFS_SKIP_SMUDGE=1`, and `XDG_CONFIG_HOME` to the private scratch. The accepted command also passes `core.hooksPath=/dev/null`, an empty credential helper, `protocol.ext.allow=never`, and an empty template directory. Fetch is a bare `git fetch` plus `cat-file`. This owner instruction overrides FETCH-SPEC section 1's private-HOME sentence. The adapter records `HOMEChanged: false`.

## Receipts and stores

`verification.json` is 29412 bytes, sha256 `1c017097422d70b8d1a31058133f20b7228bda9cb23020a967aefacf7132940f`. It is a separate offline pass: 49 verified entries and five workspaces, from `2026-10-06T17:25:14.611957+00:00` to `2026-10-06T17:26:28.843652+00:00`. `verify-overlays.py` has no subprocess and no network import. Its flags for repository-code execution, held-out inspection, provider launch, and product qualification are false.

The cache store is `/Users/sb/code/.opensip-implementation-cache/t2-corpus-c8cc48e1/store`. Its top-level names are exactly the 49 tree-digest directories and the 49 `<treeDigest>.admission.json` receipts. Each store directory is a real directory in mode 0555. Each receipt is mode 0444. Archived receipt bytes match the cache bytes, the verification pin, and canonical JSON plus a trailing newline. Receipt keys are the manifest identity fields plus `manifestSha256`, `fetchedAt`, and `gitVersion`. Every receipt names the manifest sha256 above. The whole `treeDigest` and `contentDigest` objects, including both algorithm ids, match the manifest entry, the acquisition row, and the verification row. `id`, `url`, `commit`, `gitTree`, `licence`, `family`, and `heldOut` match the manifest entry. All 49 receipts record `git version 2.54.0 (Apple Git-157)`. Ten receipts have `heldOut: true` and thirty-nine have `heldOut: false`, each equal to the manifest. Those fields stay the declared values. The archive standing remains pinned public acquisition. FETCH-SPEC section 1 treats this mechanical fetch and digest as acquisition, which QD-23 allows for held-out entries. This review hashed receipt and overlay metadata only. Corpus trees were not listed.

## Overlays

Each workspace-overlay file is the canonical overlay object. Its sha256 equals the manifest `overlayDigest` and the verification pin. Workspace directories are mode 0555. Overlay files are mode 0444. Each member mount is a symlink whose target is the store directory named by that member's tree digest, and the member count matches the manifest.

| Workspace | Members | Rendering |
|---|---|---|
| `mr-rs-medium-serde-json` | 2 | Cargo patch, overlay `68cb5d5b14445997755c5c49b4042f122592a2b516ab607416ab62e664aab2a9` |
| `mr-rs-large-aws-lambda-tokio` | 8 | Cargo patch, overlay `e8f4bf0311e6cac2afb9debedc968087a3157f4051d7964001b8c72ef482cbab` |
| `mr-ts-large-smithy-powertools` | 2 | `undefinedRenderings: ["npm"]`, overlay `1006513e537c53f923ba51596da1732f68cee98dce44e005a5137dca15b9484f` |
| `mr-ts-very-large-smithy-sdk` | 2 | `undefinedRenderings: ["npm"]`, overlay `6bec503038e9b49f107ee0b1c9b2c60595a44956e14519b6c2c10bec6533b88e` |
| `mr-py-medium-boto` | 2 | `undefinedRenderings: ["python"]`, overlay `6b0256ef19cd8629ff011cf08d99759f5a1e74669d59ffa1adb780088b1ff3a8` |

The two Cargo `config.toml` files match the accepted renderer: sorted `[patch.crates-io]` lines, 177 bytes / `6898db6e4a3e28461aacaea48c0948aea724e0de6be48a0a454b712aeda4fac2` and 839 bytes / `344bb98b7e6658ee13ebf51fe93e474cd056ed7089ee7372bbe47093b81c8cfd`. Each Cargo path starts at a member id. The npm and Python workspaces have no `.cargo` directory. Their link maps stay inside the canonical overlay. No package-manager or Python rendering is added.

## Boundaries

The reviewer did not run fetch, verify-overlays, Cargo, a compiler, a producer, or a network command, and did not assign `HOME`. `~/Library/Application Support/OpenSIP` is absent. Store contents stay in the named cache. Signature, sysroot, standard-library, configuration, dependency, native-context, and process-policy admission stay upstream. O1-a's three law gaps and the owner/day0 gates remain open.
