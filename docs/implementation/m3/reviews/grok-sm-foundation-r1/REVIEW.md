# S-M foundation batch r1

Verdict: ACCEPT.

This accepts the exact partial measurement record in `s-m-foundation-2026-10-09`. It archives limited startup, configured-root semantic, and regular-file sealing evidence. S-M remains incomplete, L-G1 remains open, no SM-n placeholder is filled, L is not in effect, and the product is not qualified. Accepted S-P, the provider-protocol law, the T2 manifest, Q0 r13, and the 2026-10-09 owner decisions stay closed.

## Subject

`subject.json` is 77733 bytes, SHA-256 `f25501a5c790c33a82ced8a50072428fe8dd3810328b2abd89cee17e4f09b1bf`. It names 326 sorted unique members whose bytes sum to 15342083. Every staged member matches its pin. The spike directory is absent at architecture `9b8abe5bfb8d9828c95144123fbfe1c5185e3753` (`Record explicit O7, T2 corpus and Q0 r13 owner approvals.`). The worktree's only porcelain entry is the unrelated untracked `docs/implementation/m3/syntax-e/e2s/`.

Six authority pins match that commit: `M3-PLAN-r10.md` `ec8c38f8c6ac8d522989ea6226363817a1b77c5b37560e72e2520088601bb964`, provider-protocol `PROPOSAL-r5.md` `f654ee4e9149e62693ebae8177adcc1f3a8a595b745c1e7503e5f279b80e3e88`, `DESIGN-r13.md` `37438317e7233bbb8bdc64dc9c8fe838f590c7e06fba3e54a0966002c1436be4`, `t2-corpus-manifest.draft.json` `c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578`, `grok-s-p-r1/review.json` `dbb2b5708e9bcca03bc2e867624c9a8cbe3c1ec4d7f467ad21da81f078fd9313`, and `D13-OWNER-DECISION-2026-10-09.json` `92b30760d56005052874d879beffeae0e5d5c8b17a320e0f5f5c956f37ed4edb`.

Product `bf4be44ffbaf02e8518c276882524831ee8e12c4` is clean. `design-lock.json` remains 614747 bytes, SHA-256 `9c73578855ed10eb52dcd507a4498761045efa60c7a5899afb1726d35f43973f`, with 139 inventory successors ending at `repository-file-inventory.v179.json` and 154 contract successors. Inventory stays 179. Product code stays unchanged. `REPORT.md` has no links.

`verify_design.py` was not run. An architecture-only commit of this record still waits on this acceptance, substantive assent, and the current `verify_design`. It does not bind the design lock and it does not push.

## Retained pins, controls, and the private-feature boundary

The Node archive is v24.21.0, 27386080 bytes, SHA-256 `6239d4cf92d864487ec8cd3615038f7b67e7f58b77b21cd2f09ea9fbd68065fe`. The TypeScript archive is 6.0.3, 4515854 bytes, SHA-256 `33cd0ee1beaa8c9e9d15a9da836c62ddea4c34a42d7c2d349dbc80d94165d22a`. Both match the closed S-P pin files and the archives named by this record. The retained `typescript.js` pin is 9144216 bytes, SHA-256 `569177652966bd528c319171c7dd22860dbf72bde116cbc4f644f1d02bb12e39`. The closed S-P TypeScript 7.0.2 archive is a different pin and is not the compiler this batch runs. `productionSelection` is false.

The retained `rustc` pin is 412504 bytes, SHA-256 `b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c`, and that file still matches. The closed S-P record remains the authority for the three official 1.95.0 component archives. This batch reuses that coherent distribution and pins the retained compiler binary. It does not make a production toolchain selection.

`probe/startup.rs` enables `rustc_private` for the wrapper. `run_startup.py` sets `RUSTC_BOOTSTRAP` only on the wrapper compilation environment and removes it from the environment used for controls and measured runs. The build log is empty. The positive control stdout is `{"event":"after_analysis"}` with exit 0. The negative control stderr is `error[E0308]: mismatched types`, exit 101, and its stdout is empty. The startup probe path prints the ready marker and does not call `run_compiler`.

## Startup

Each prototype has ordinals 0–9, three warmups, and seven measured fresh processes, all exit 0. `readyElapsedNanos` is `readyNanos - startNanos` on every row. `rssBytes` equals `ruMaxrssNative`, and `rssUnit` is `bytes`. The seven measured Node/TypeScript samples have median 80610959 ns and maximum 81966792 ns. The seven Rust samples have median 9222083 ns and maximum 9511500 ns. Those are the figures in `REPORT.md`. Every Node ready record is `{"event":"ready","version":"6.0.3"}`. Every Rust ready record is `{"event":"ready","compiler":"1.95.0"}`. The ten stderr logs for each metric are empty, which is the stream the runner retained while the parent parsed stdout. `SMPlaceholderFilled` is false, and the standing is a preliminary retained prototype.

## Configured TypeScript

The six workload ids are `counts.tsjs.medium.devIds` in manifest order: `js-medium-express`, `poly-medium-napi-rs`, `ts-medium-powertools-lambda`, `ts-medium-smithy-typescript`, `ts-medium-umami`, `ts-medium-vite`. None is held out. Each stored tree and content digest equals the manifest entry. `verify` returns those digests only after the scanned tree matches the entry, and the stored `treeVerified` digests are those same values. The manifest hash in the result is the pinned T2b manifest.

`smithy-typescript` and `umami` each have ten exit-0 runs. Their measured medians are 847375583 ns and 1719613333 ns, and their measured maxima are 855241167 ns and 1727825375 ns. Across all ten samples of each, the diagnostic counts, configured-file count, program-file count, project-reference count, read-path set, and blocked-path set are identical. Call labels are stable. The sum of the timed public calls equals `totalInstrumentedNanos`, and the longest of those calls equals `maxPublicCompilerCall`. Syntactic and semantic calls each occur once per program source file (718 and 1430). Smithy records 659 configured files, 618 diagnostics, and codes including 2307. Umami records 1335 configured files, 2560 diagnostics, and codes including 2307. Both standings are `semantic-pass-with-deficiencies`. Project-reference counts are 0 and are retained. Every read path is under the recorded repository root or the retained TypeScript library directory. Blocked-path lists are empty. The maximum public-call field is the longest wrapped compiler API call. `SM8PlaceholderFilled` is false.

`express` and `vite` stop at ordinal 0 with exit 2 and `root-tsconfig-absent`. `napi-rs` and `powertools-lambda` stop at ordinal 0 with exit 2 and `no-configured-source-files`. Each median is null. That is the report's three other repository-only outcomes plus express. `fullWorkspaceSemanticsClaimed`, `dependencyTreePinned`, and `repositoryCodeExecuted` are false. `probe/semantic.cjs` reads through a host limited to the repository tree and the compiler library tree, throws on emission, and does not spawn a package manager, build, or proc-macro.

## Sealing

The twelve ids are the sorted union of the Rust and TS/JS medium dev lists. The overlap is `poly-medium-napi-rs`. None is held out, and each tree and content digest matches the manifest, including `treeVerified`. Each id has ten separate process stdout documents. Apart from `elapsedNanos`, the ten documents are identical, so the inventory digest, snapshot digest, plan digest, row count, byte count, and exclusion list are stable. The recorded median and maximum equal the seven measured stdout elapsed values. `rssBytes` again equals native `ru_maxrss` in bytes.

Regular-file rows run from 92 to 2836. Total regular bytes run from 737131 to 17644692. Snapshot-equivalent descriptors run from 11578 to 419807 bytes. Every plan-equivalent descriptor is 914 bytes. Recomputing `H(plan, canonical(plan))` from the workload id and the recorded snapshot digest reproduces that 914-byte length and `planEquivalentDigest` for all twelve. The plan's reference digests are the synthetic prototype seed. `referenceRecordsSynthetic` is true and `identityAdmissionClaimed` is false. The recorded bounds hold: rows are within 100000 and 200000, the snapshot descriptor is within 4194304 bytes, and the byte total is within 8589934592. `tsChunkBound1048576` is the constant 1048576, the read size in `probe/sealing.py`.

Nonregular rows are listed and omitted from the regular inventory. Empty exclusion lists are explicit for express, the AWS Lambda Rust runtime, serde-json, tokio, smithy-typescript, and umami. The other six record `nonregular` entries, `symlink-directory` entries, or both. `nonregularSnapshotPolicySelected` is false. Dependency source sets and the multi-repository overlay are not included. `SM5PlaceholderFilled` and `SM6PlaceholderFilled` are false.

## Boundaries that remain

The record keeps `SMComplete`, `LG1Met`, `SMPlaceholdersFilled`, `effectiveL`, and `productQualification` false. It records no production closure, no whole-workspace semantics, no admitted snapshot or plan identity, no dependency source set, no full transport or replay, no SM-11 through SM-14 result, no F/T or budget comparison, and no Q6 row. `macOSWholeTreeSettlementVerified` and charged-memory/RSS equivalence stay false. Process RSS is informational. The report's remaining-work list still includes repository and workspace selection, Rust typechecking, admitted-size accounting, framed transport, synthetic replay, the large workloads, cold/warm reset, envelope validation, and L's measured delta round.
