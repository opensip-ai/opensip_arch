# S-M-TS-CONFIGURATION-COHORT-PARTIAL-R1

ACCEPT. These are preliminary sealed TypeScript configuration-cohort observations for the six medium dev repositories. SM-2, SM-8, full S-M, L-G1, effective L, and product qualification stay open. Whole-workspace selection and full workspace semantics stay unselected. Accepted foundation evidence, the transfer and startup rows, the owner decisions, and the L law stay closed.

## Subject

`subject.json` is 39312 bytes, SHA-256 `c2ac192eb542545a36a22ba55d8570a91b958af4af7c829ca166f405cfa92e3e`, schemaVersion 1, unit `S-M-TS-CONFIGURATION-COHORT-PARTIAL-R1`. It pins 162 sorted unique members, and every hash matches the stage. The archive path `docs/implementation/m3/spikes/s-m-ts-cohort-2026-10-09` is absent at architecture `d17795a4dfd2a8632e77526473960ab4c9e6bc45` (log: “Record preliminary framed transfer and pinned Node startup measurements.”). Product `37581132d8099b8fb4ad9ef8fb2f90ff8b89d02d` is clean. The architecture tree’s only untracked path is `docs/implementation/m3/syntax-e/e2s/`, outside this packet. Product `design-lock.json` remains 615658 bytes, SHA-256 `018dbfe27c1bbba48dedcf88ff6625ce62072b01bfb0fae0aee8c3dc463fc283`, with inventory v179, 139 inventory successors, and 155 contract successors. The packet names none of those successors. The recorded host is macOS 27.0.1, build `26A434`.

The L-law pin at that architecture commit is `docs/implementation/m3/provider-protocol-l/PROPOSAL-r5.md`, 172198 bytes, SHA-256 `f654ee4e9149e62693ebae8177adcc1f3a8a595b745c1e7503e5f279b80e3e88`. The T2 manifest pin is 322483 bytes, SHA-256 `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`. The live Node 24.16.0 executable is 120573328 bytes, SHA-256 `1ee75375e33b94fc34b3b19aede049e11dae90efb63b374dc96d6bdace70c4b8`, matching `tools/contracts/generator-closure.json` and `engines.node`. The retained `typescript.js` is 9144216 bytes, SHA-256 `569177652966bd528c319171c7dd22860dbf72bde116cbc4f644f1d02bb12e39`.

## Cohort rows

The six workloads are `counts.tsjs.medium.devIds`, in that order: Express, napi, Powertools, Smithy, umami, and Vite. None is held out. Each retained `treeVerified` pair equals that repository’s T2 tree digest and content digest. This review did not call `store.verify` and did not rerun the copy.

The copy opens regular files with `O_NOFOLLOW`, checks the inode against the `lstat` identity, and checks size, mtime, and ctime again after the read. Symlink directories and other nonregular entries are excluded. The sealed copies were removed after the ten children. The retained inventories match those exclusion lists and the regular row counts 214, 644, 1389, 2315, 2026, and 2836.

Configuration selection is every retained regular basename matching `^tsconfig(?:\..*)?\.json$`. That list matches the inventory configurations on all six inputs: 0, 8, 51, 230, 7, and 55. Vite also has one `jsconfig` file, and that name is outside the configuration list. The selection keeps test, example, and tool configs and overlapping projects. Each inventory pins 110 compiler `.d.ts` libraries. Directory listings are computed in memory from those retained paths.

Express has an empty configuration list. Its ten children record empty `readPaths` and perform no `createProgram`. Their whole-process samples are initialization, covering runtime and compiler load plus sealed-map initialization. A parsed config with no file names stays `incomplete` with reason `no-configured-source-files`. An unreadable config stays `incomplete` with reason `config-read-diagnostic`. Those are the only incomplete reasons present. Vite records both. The other five inputs record only `no-configured-source-files`. The cohort source supplies no synthetic dependency files.

For each nonempty config the child calls `createProgram`, `getOptionsDiagnostics`, `getGlobalDiagnostics`, `getSyntacticDiagnostics`, and `getSemanticDiagnostics` over each Program source. Project references are retained on the configuration row. `writeFile` throws, and every retained stdout has `emitPerformed` false and `repositoryCodeExecuted` false.

Each input has three warmup children and seven measured children, 60 children in all, every one exit 0 with empty stderr. The parent span runs from before spawn through `wait4`, so it includes Node and TypeScript loading, sealed-map reads and hashes, and every configuration. Configured shapes, with call durations removed, are identical across the ten children and equal the stored `configuredShape`. Recomputed medians and maxima of the seven measured samples match the report table. `progress.json` carries the same medians and maxima.

| Dev input | Matching configs | Incomplete | Completed passes | Distinct configured files | Median ns | Max ns |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| js-medium-express | 0 | 0 | 0 | 0 | 92756583 | 93573084 |
| poly-medium-napi-rs | 8 | 2 | 6 | 193 | 1026995125 | 1038699750 |
| ts-medium-powertools-lambda | 51 | 2 | 49 | 936 | 3465557959 | 3547486500 |
| ts-medium-smithy-typescript | 230 | 4 | 226 | 1159 | 16295809334 | 16368380541 |
| ts-medium-umami | 7 | 1 | 6 | 1381 | 2302594708 | 2317559208 |
| ts-medium-vite | 55 | 18 | 37 | 678 | 8059186750 | 8139470666 |

Completed passes split as napi 5 with deficiencies and 1 completed, Powertools 49 with deficiencies, Smithy 226 with deficiencies, umami 4 with deficiencies and 2 completed, and Vite 31 with deficiencies and 6 completed. Configured-file listings exceed the distinct set where projects overlap: Powertools 2463 listings and 936 distinct, Smithy 5579 and 1159, umami 1429 and 1381, Vite 1113 and 678. Express and napi have no such excess.

Native `wait4` `ru_maxrss` is stored as `rssBytes` with unit `bytes`, and `rssBytes` equals `rssNative` on all 60 children. The ranges are Express 129449984–132464640, napi 429211648–503562240, Powertools 736608256–906608640, Smithy 853475328–999915520, umami 735264768–932970496, and Vite 1106247680–1836007424. They stay informational.

Compiler `readPaths` are identical across the ten children of each input. This review reopened every distinct path with `O_NOFOLLOW`, rehashed it against that input’s sealed-file or library row, and decoded it as strict UTF-8. The counts and byte totals are Express 0 / 0, napi 296 / 5101540, Powertools 1075 / 4458245, Smithy 1544 / 6737176, umami 1484 / 7851015, and Vite 994 / 6019672. Every path was in the inventory, every hash matched, and none was UTF-16 or a UTF-8 BOM. That check covers this cohort’s recorded compiler reads. It is silent on general encoding admission.

SM-2 in the accepted L law is a fresh-process Program creation plus a full semantic pass over the repository. These rows are an exploratory basename cohort. Express is unanalyzed, empty and unreadable configs stay incomplete, and overlapping test, example, and tool configs remain in the set. `SM2PlaceholderFilled` stays false. SM-8 is the longest single synchronous compiler call inside SM-2, the event-loop block. The packet retains per-config durations and the maximum among the wrapped public calls `readConfigFile`, `parseJsonConfigFileContent`, `createProgram`, and the four diagnostic calls. That maximum is a different figure from the event-loop block, so `SM8PlaceholderFilled` stays false. No F or T budget is derived.

## Controls

Five synthetic API controls exit 0 with empty stderr. The positive control is one completed configuration with diagnostic count 0. The type-error control records one TS2322. The outside-import control records one TS2307. Its target bytes are `export const value: number = 11;\n`, SHA-256 `18fc06ae20d95500703a65be5c66f349250b8182b03891ed1f227a56175cc827`, and that target is absent from `readPaths` and from `blockedPaths`. Virtual `fileExists` answers from map membership and does not record `blockedPaths`. `blockedPaths` records `readFile` misses only, and `fileExists` returns false before `readFile` for an absent path. The nested control has two configurations: the child completes with a semantic diagnostic call and zero diagnostics, and the empty root stays incomplete with reason `no-configured-source-files` while its project reference is retained. The no-config control has configuration count 0.

`run_controls.py` and `run_controls-first-attempt.py` are 27 lines and differ only on the outside-import assertion. The first attempt also required the target to appear in `blockedPaths`. The corrected assertion requires TS2307 and the target’s absence from `readPaths`. For positive, type-error, and outside-import, the retained input rows match on path, byte length, and SHA-256, including the 110 library pins. Their temporary roots differ. The three retained first-attempt stdouts show the same diagnostic results, and the first-attempt outside target is likewise absent from both path lists. First-attempt nested and no-config outputs are absent, which matches a stop at that outside assertion. `cohort.cjs` is the cohort host used for both. `productSecurityEnforcementClaimed` is false.

## Disposition

`verify_design.py` was not run. Archival is architecture-only, after this acceptance, root assent, and the actual design check. This review binds no lock and pushes nothing. Inventory stays 179. Contract successors stay 155. Product code stays unchanged.
