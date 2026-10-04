# E0 report r1 — GROK2

**Verdict: ACCEPT**

Subject: `docs/implementation/m3/syntax-e/E0-REPORT.md`, 30,730 bytes, sha256 `c1011e836f48c3b4c338e712eca74b56bb336b5dd3da0e709d4554d4d669c24b`.

Record review of the syntax-backend feasibility probe of law M3-E1 r3, item 3. The question is whether the recorded outcome follows that item's predeclared rule from the recorded evidence. All 41 pins in `hashes.txt` match the files on disk. The fourteen per-file tables named in `results/run-tsv.sha256` are still in the probe scratch and match those digests. The gated statistics below were recomputed from those tables with the rules in `e0-probe/analyze.py`. The probe was not re-run. No build and no cargo command were run. `~/Library/Application Support/OpenSIP` was absent. The private 413 fixture was not read.

The law text used is `docs/implementation/m3/syntax-e/PROPOSAL-r3.md` (117,273 bytes, sha256 `d71031ff1aee01ba20b471e9db1891f4a0e976751741ffa10a783585eedd7c46`). Live `PROPOSAL.md` differs from that file by the acceptance note only. Item 3 is the pinned text. The lead's pre-data rulings are the "E0 phase 1 is ready" entry in `docs/implementation/OVERNIGHT-2026-10-03.md`.

## Outcome

T-native follows from item 3. Any failed criterion selects T-native, records the failing criterion, applies item 18's fallback posture, and sets `executionModel` to `native-linked-v1`. P5a is below the floor, so P5 fails. P1, P2, P3, P4, P5b, and P6 pass. P3 holds for every regular selected file, so the result stays inside the two predeclared branches.

P5a's reading was fixed before any data. The overnight entry defines the gate as the median, over non-empty files, of bytes divided by the full per-file cost (fresh instance, parse, copy, validation). Aggregate throughput is reported and is not gated. `analyze.py` implements that rule: a mebibyte is 1,048,576 bytes; the median is taken over rows with `bytes > 0`; the criterion passes only when that median is at least 1.0 and every file takes at most 10 seconds. Recomputation from `run-t.tsv` matches `results/summary.json` on every P5 field:

| Measure | Recomputed | Gate |
|---|---|---|
| Median, 8,328 non-empty files | 0.8182687907465771 MiB/s | ≥ 1.0, fails |
| Slowest file | 6.234220416 s (`yarn-4.18.1.cjs`, 3,784,940 bytes); next is `yarn-4.17.1.cjs` at 5.495 s | ≤ 10 s, passes |
| Aggregate | 0.9311700139827391 MiB/s | not gated |
| Parse-only median | 0.8833219854608008 MiB/s | not gated |

The aggregate and the parse-only median are also below 1.0, so the failure does not depend on choosing the per-file median. Time shares on RUN-t are instantiation 1.5%, the parse step 97.7%, and result copy plus host validation 0.8%. The native median on RUN-a is 12.657 MiB/s, 15.47 times the wasm median. The report's rounded headlines (0.818, 6.23 s, 0.931, 0.883, 15.5×) match these values.

The root-only diagnostic is outside the gate. `analyze.py` never reads `run-diag-rootonly.tsv`. Recomputation gives a median of 1.0466378750220364 MiB/s and an aggregate of 1.1951680559672375 MiB/s. Serialization is 22.1% of total time and 7.7% of fuel, measured against RUN-t on the same files. The report calls this build a non-product configuration, says it changes nothing in the predeclared outcome, and assigns the margin to the item-18 M4 re-decision. The outcome section, the criterion table, and "Not claimed" keep T-native. The overnight completion entry and the SYN-1 passage use the same split: the selected branch is native-linked, and the diagnostic is input to the M4 re-decision.

## Passing criteria

**P1.** `summary.json` records identical module digests for build roots A and B: javascript `38ebebc5…`, rust `a6f1b0cd…`, tsx `f168a25d…`, typescript `634f6218…`, with the byte lengths in the report. `results/p1-a.sha256`, `p1-b.sha256`, and `p1-c.sha256` are byte-identical.

**P2.** `results/p2-inspect.tsv` records 0 imports from the independent reader and from the engine for all four modules. The export names and types are item 5 step A10's set. Each module has no start function, one memory, and `engine_shape` `ok`. Admission repeats in `admit-1.tsv`, `admit-2.tsv`, and `admit-3.tsv` are `float_free` true, and each module's wasm and native `SymbolTableV1` digests are equal. The report's admission ranges, ABI numbers, symbol counts, and field counts match those three files. Symbol-table prefixes are javascript `5a0738c3`, rust `0363b059`, tsx `c8759474`, typescript `daa3b998`.

**P3.** RUN-a has 8,354 rows: 8,351 regular and 3 symlinks. Every regular row has wasm status equal to native status, `eq` 1, and validation `ok` on both legs. The node sum is 13,943,471. The median tree has 393 nodes and depth 16. The largest tree is napi-rs `.yarn/releases/yarn-4.18.1.cjs`, 1,827,929 nodes, depth 430. Outcomes are 8,310 `parsed` and 41 `syntax-error`, in the per-grammar counts the report prints. `pins/t2a-selected.tsv` has 8,351 regular files, 49,153,127 bytes, 23 empty files, all marked UTF-8, and a maximum of 3,784,940 bytes. Grammar counts are rust 2,354, typescript 3,788, javascript 1,656, tsx 553. The three symlinks are hyper `tests/support/tokiort.rs` and vite `playground/preserve-symlinks/module-a/linked.js` and `playground/ssr-wasm/src/imports.js`. The variant line in the report sums to 8,354 because it counts those three symlinks with the regular files.

**P4.** Runs B, C, and D differ from A on 0 files in status, tree, fuel, and peak pages. Files processed off list position are 8,353, 8,352, and 8,354. The lazy control differs in fuel on 28 files (shuffle, seed 1) and 30 files (sorted). Trees are unchanged. Each lazy order adds 2,932,216 fuel against the eager baseline, and 43 files differ in fuel between the two lazy orders. Instance reuse differs in fuel on 8,347 of 8,351 files, with trees unchanged. `summary.json` records the lazy and reuse controls; the second lazy order is in `run-lazy2.tsv`, which `run-tsv.sha256` pins.

**P6.** `analyze.py` derives the constants from RUN-a exactly as the report states. The 23 empty files use 41,407 to 46,191 fuel. `fuelBase` is 190,000, `fuelPerByte` is 420,000, and the maximum peak is 5,221 pages, so `maxMemoryPages` is 20,896, inside the 65,536-page ceiling. The tightest file is vite `packages/vite/src/node/ssr/__tests__/fixtures/errors/syntax-error.js`: 13 bytes, 1,408,984 fuel, fraction 0.24937769911504426. The 4 MiB budget is 1,761,607,870,000 fuel, 111.61 seconds at the measured median fuel rate. Files whose parse took at least 1 ms range from 1.49 to 80.6 billion fuel per second. RUN-limits covers all 8,351 regular files with 0 truncations and 0 faults (8,310 `parsed`, 41 `syntax-error`). The boundary sample is 836 files. The exact budget matches RUN-a's fuel and tree on all 836 (832 `parsed`, 4 `syntax-error`). One fuel unit less is `truncated:fuel` on all 836. One page less is `truncated:memory` on all 836. Of that sample, 203 files have peak pages equal to the initial size and 633 do not, which is the instantiation-refusal path and the allocator-flag path in `harness/src/wasm.rs`.

## Deviations

The gated shim in build roots A and B is sha256 `2f2cee98880be0f68dd4c089850633da49014b120066969a1b23348a1fb2f268` and contains no `fdopen`. The probe file `cd62b40cca12f2025933298de8a9d8da2adadfc97ee79af6cc325984cc1a0aca` differs from it only by the `#ifdef OSG_DIAG_ROOT_ONLY` block. Build root C and the diagnostic build used the probe file. `p1-c.sha256` matches roots A and B, so a default build, with that macro unset, produces the same module bytes.

In `harness/src/wasm.rs`, `fuel_total` and `fuel_parse` are sampled before the two result getters. The getters then receive an uncounted allowance of 1,000,000 fuel, the same allowance the trap classifier already uses for the exhaustion-flag read. `w_t_total_ns` still includes the result copy and the host validation in `main.rs`. The recorded exact-budget table matches RUN-a on fuel and trees and contains no `backend-fault`. The allowance is after the fuel sample that P5 and P6 use. RUN-lazy2 and the root-only diagnostic are labelled as phase-2 additions in `phase2-run.sh` and are outside the gate.

## Forbidden substitutes

Item 3 forbids presenting E0 numbers as Q6 or qualification evidence, and forbids E0 code entering the product. The report says E0 is not qualification evidence, not a Q6 figure, and not hostile-input proof, and that no E0 code enters the product. A search of the product tree for `wasmi`, `e0-harness`, `e0-probe`, and `osg_shim` found no matches. The figures 0.818 and 1.047 appear in this report, the overnight log, and the review request. The overnight log and the SYN-1 passage use them as the item-3 branch and the item-18 M4 input.

## E1 record items

**ERROR symbol 0xFFFF.** Item 10 treats a symbol outside the table as `backend-fault`. A11 requires contiguous symbol ids, at most 65,535 of them. The pinned runtime defines `ts_builtin_sym_error` as `(TSSymbol)-1` and `ts_builtin_sym_error_repeat` as that value minus one (65,534). The Rust binding accepts an id at or above `u16::MAX - 1` (`lib/binding_rust/lib.rs`). The report's statement of the required exception matches those sources. Host validation in `harness/src/tree.rs` allows `SYM_ERROR` (`0xFFFF`).

**Wasm headers.** Item 4's closure table does not name `crates/language/wasm/include`. `build-modules.sh` copies that directory beside `lib/` and compiles with `-Iin/language/include`. The report records the omission and says it is moot under T-native.

**Eager compilation.** `wasm.rs` uses `CompilationMode::Eager` unless the lazy control is requested. The lazy runs show order-dependent fuel with unchanged trees. The overnight ruling, made before any data, already made eager compilation an E2b obligation. The report states that obligation.

**Eight host crates.** The law's supply-chain row estimates about seven host crates and names `wasmi`, `wasmi_core`, `wasmi_ir`, `wasmi_collections`, `wasmparser`, `spin`, and `libm`, and it says the count is an estimate. `harness/Cargo.lock` pins `wasmparser` 0.228.0 with a dependency on `bitflags`. Those eight names are the wasmi-family crates present in `results/crate-closure.txt`. `results/wasmi-features.txt` records features `std`, `validate`, and `deterministic`. The closure file also lists the probe's native-leg crates (`tree-sitter`, `regex`, `sha2`, and their dependencies). The report's count of eight is the host set under that feature selection.

## Non-blocking observation

**NBO-1** (`E0-REPORT.md:177`). The pair count and the tree count are right, and within one grammar no content hash maps to two trees. Fourteen content hashes occur under two grammars and have two trees. The clause "no content maps to two trees" is broader than that per-grammar fact. It does not change P3 or the outcome.
