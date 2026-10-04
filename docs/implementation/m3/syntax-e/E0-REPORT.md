# E0 — the syntax-backend feasibility probe: report

**Record, not law.** E0 is the lead-run throwaway probe of E1 item 3 (`PROPOSAL.md`, M3-E1 r3, accepted). It chooses between two predeclared branches: T-wasm (tree-sitter grammars compiled to WebAssembly and run by `wasmi`) and T-native (tree-sitter linked natively). It is **not qualification evidence and not proof against hostile input** (E-N4). No E0 code enters the product.

2026-10-04. Run by a lead-dispatched agent for Claude Opus 5.5, the implementation lead, during the overnight autonomous run. Phase 1 (downloads, clones, code) ran from 04:09 to 04:35 PDT. Phase 2 (builds, runs, analysis) ran from 12:07:59 to 12:20:47 UTC after the lead's "E0 phase 2: go". Nothing was committed, and the product repository was not touched.

## Outcome

**T-native.** Criterion **P5 fails**. On this host the median per-file throughput is **0.818 MiB/s**, below the 1.0 MiB/s floor (P5a). P1, P2, P3, P4 and P6 pass, and so does P5b: the slowest file parses in 6.23 s, within 10 s.

Under E1 item 3 the outcome is therefore:
- **T-native**, with P5 (P5a) recorded as the failing criterion;
- item 18's fallback posture applies;
- the manifest's `executionModel` is `native-linked-v1`.

**The result is inside the predeclared branches.** The equivalence P3 tests holds exactly: 8,351 of 8,351 files give byte-identical trees on the two legs. No defect was found that would reopen E1.

| Criterion | Result | Headline evidence |
|---|---|---|
| P1 reproducible | **PASS** | Two clean builds, in two different roots, give byte-identical modules for all four rows |
| P2 closed | **PASS** | 0 imports per module, by an independent binary reader and by the engine |
| P3 equivalent | **PASS** | 8,351/8,351 files have identical `SyntaxTreeV1` bytes on both legs; 13,943,471 nodes compared; 0 validation failures on either leg |
| P4 order-free | **PASS** | 4 runs (sorted, 2 shuffles, reverse; 1, 4 and 8 threads; modules from both build roots) agree on every file's status, tree, fuel and peak pages. Both discrimination controls detect what they should. |
| P5 fast enough | **FAIL** | P5a median 0.818 MiB/s < 1.0; P5b max 6.23 s ≤ 10 s |
| P6 bounded | **PASS** | `maxMemoryPages` 20,896 ≤ 65,536; the verification run under the derived constants truncates nothing |

## Short names

- **E1** `docs/implementation/m3/syntax-e/PROPOSAL.md` (M3-E1 r3, accepted). Items, steps A1–A12 and controls are cited by their E1 ids.
- **PROBE** `docs/implementation/m3/syntax-e/e0-probe/`. It holds:
  - `env.sh`, the environment and pins;
  - `fetch_pinned.py` and `phase1-fetch.sh`;
  - `build-modules.sh`;
  - `phase2-run.sh`, the run plan as executed;
  - `analyze.py`, the predeclared rules;
  - `shim/osg_shim.c`;
  - `harness/`, the Rust harness with its `Cargo.lock`;
  - `pins/`, every input pin;
  - `results/`, the small result records.
- **SCRATCH** `/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/e0/`. It holds the toolchain, sources, T2a bytes, builds and per-file run tables. Each per-file table is pinned in PROBE by sha256 (`results/run-tsv.sha256`).
- **RUN-x** a per-file run table `SCRATCH/out/run-x.tsv`, one row per selected file.

## Host

| Fact | Value | Evidence |
|---|---|---|
| OS | macOS 27.0 (26A428), Darwin 27.0.0, `xnu-13432.1.9~1/RELEASE_ARM64_T6050`, arm64 | `results/host.txt` |
| CPU and memory | Apple M5 Max, 18 cores, 128 GiB (137,438,953,472 bytes) | `results/host.txt` |
| Rust | rustc and cargo 1.95.0 (Homebrew Cellar), release profile, opt-level 3 | `results/host.txt`, `harness/Cargo.toml` |
| Native C compiler (T-native leg) | Apple clang 21.0.0 (clang-2100.3.34.2), through the `cc` crate | `results/host.txt` |
| Wasm C compiler | wasi-sdk 34.0: clang 23.1.0-wasi-sdk (llvm `895aa2c896ad`), wasi-libc `2e6fb9d8ee0c` (no wasi-libc byte is linked) | `results/build-receipt-a.txt` |
| Isolation | Private 0700 `TMPDIR` under `$(getconf DARWIN_USER_TEMP_DIR)e0-probe-tmp`. `HOME`, `CARGO_HOME` and `CARGO_TARGET_DIR` all in SCRATCH. `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_NOSYSTEM=1`, hooks path `/dev/null`, LFS smudge off. No system-wide install. | `env.sh` |
| Machine load during P5 | No foreign `cargo`, `rustc` or `check_crash_matrix` process before or after the timing run, so no wait was needed. Top process during the run was below 5% CPU. Spotlight (`corespotlightd`) had been at about 106% CPU at 12:14:40 and had settled before the warm-up at 12:14:51. | `results/p5-load.txt` |

## Inputs and pins

Every input is pinned by sha256: `pins/PINS.txt` and the four `pins/*.pins.tsv`, which hold one row per member file with sha256, byte length and git blob id.

| Input | Pin |
|---|---|
| wasi-sdk | `wasi-sdk-34` (tag object `86e11644…`, commit `5a0bf653…`). `wasi-sdk-34.0-arm64-macos.tar.gz`, 180,322,002 bytes, sha256 `9c59398106b417f8f14913380fdf0097a8cc0ff4af9eb3ce0065a859e88d49e9`, equal to GitHub's published asset digest. |
| tree-sitter runtime | `v0.27.0`, commit `6070dbfefd326bd735e5683eb128cc1b57dad0c0`. `lib/`, `LICENSE` and `crates/language/` (the wasm headers) are pinned per file in `pins/tree-sitter.pins.tsv`. |
| tree-sitter-rust | `v0.24.2`, commit `77a3747266f4d621d0757825e6b11edcbf991ca5` (generated ABI 15) |
| tree-sitter-typescript | `v0.23.2`, commit `f975a621f4e7f532fe322e13c4f79495e0a7b2e7`. Both the `typescript` and `tsx` grammars, generated ABI 14. |
| tree-sitter-javascript | `v0.25.0`, commit `44c892e0be055ac465d5eeddae6d3e194424e7de` (generated ABI 15) |
| Crates | `harness/Cargo.lock`, sha256 `8bdf9cdc6b7fced11f3ed97bc99bd9d996d813804810d4fe2407f148769bb928`.<br>`wasmi` 2.0.0, checksum `78693fcd…`.<br>`tree-sitter` 0.27.0, checksum `2038684e…`: **its 82 bundled `src/` and `include/` C files are byte-identical to the tag's `lib/`.**<br>`tree-sitter-language` 0.1.8: its 14 `wasm/` files are identical to the tag's `crates/language/wasm/`. |
| Shim | `shim/osg_shim.c`. The gated builds used sha256 `2f2cee98880be0f68dd4c089850633da49014b120066969a1b23348a1fb2f268`. The file now in PROBE (`cd62b40c…`) adds only an `#ifdef OSG_DIAG_ROOT_ONLY` block for the ungated diagnostic. A third clean build with the current file (build root C) gives the same module bytes (`results/p1-c.sha256`). |
| Build input tree | 132 files, digest `f44876d8934a1c816495a05b6bcbe6264c2d32e5b2d2d1676fc2993ad5292b4f`, the same in roots A and B (`inputs.sha256` per root) |
| T2a | `t2-corpus-manifest-T2a.draft.json`, sha256 `09fef028…bca5`.<br>All 19 T2a repositories were fetched by commit, and each one's `gitTree` and `contentDigest` matched the manifest.<br>Selected files: `pins/t2a-selected.tsv`, sha256 `dfc8a7fc…e99a`, one row per file with repo id, path, variant, grammar, mode, bytes, sha256 and git blob. The harness re-checks each file's sha256 before parsing it. |

**The T2a selection.**
- **Rule.** A file is selected when its name ends, byte-exactly and case-sensitively, in one of the ten dialect selectors (the nine owned code suffixes plus `.d.ts`), longest suffix first.
- **Result.** 8,354 files: 8,351 regular files totalling 49,153,127 bytes, plus 3 symlinks. The symlinks are hyper's `tests/support/tokiort.rs` and vite's `playground/preserve-symlinks/module-a/linked.js` and `playground/ssr-wasm/src/imports.js`. They are recorded and not parsed.
- **By grammar:**

  | Grammar | Files | Bytes |
  |---|---|---|
  | rust | 2,354 | 20.1 MB |
  | typescript | 3,788 | 16.5 MB |
  | javascript | 1,656 | 11.4 MB |
  | tsx | 553 | 1.0 MB |

  By variant: `ts` 3,669, `rs` 2,355, `js` 1,521, `tsx` 553, `mjs` 69, `ts-declaration` 64, `cjs` 59, `mts` 49, `jsx` 9, `cts` 6.
- **Size and encoding.** Every file is valid UTF-8, and 23 are empty. All are at most 4 MiB; the largest is napi-rs's `.yarn/releases/yarn-4.18.1.cjs` at 3,784,940 bytes. So `truncated:size` never applies.
- **Cap.** The 20,000-file cap was not reached, so no cap rule was exercised.

## Method

**The modules** (`build-modules.sh`).
- **Composition.** One module per code row (javascript, rust, tsx, typescript), linking:
  - the runtime's unity file `lib/src/lib.c`;
  - tree-sitter's wasm stdlib `lib/src/wasm-stdlib/{libc.c, stdio.c}`, with headers from `crates/language/wasm/include`;
  - the grammar's `parser.c` and `scanner.c`;
  - the first-party shim.
- **Compile.** `--no-default-config --target=wasm32-unknown-unknown -mcpu=mvp -mbulk-memory -msign-ext -nostdlibinc -std=c11 -O2 -fvisibility=hidden -ffunction-sections -fdata-sections -fno-ident -ffile-prefix-map=<root>=.`
- **Link.** `-nostdlib -Wl,--no-entry -Wl,--stack-first -Wl,-z,stack-size=1048576 -Wl,--gc-sections`
- `TREE_SITTER_WASM_STDLIB` is left **undefined** (lead ruling).
- The exact argument vectors are in `results/build-receipt-a.txt`.

**The engine** (`harness/src/wasm.rs`).
- **wasmi 2.0.0**, built with `default-features = false` and features `std`, `validate` and `deterministic`.
- **Configuration:**
  - fuel metering on;
  - `CompilationMode::Eager` (lead ruling);
  - start functions refused;
  - Wasm features: sign-extension and bulk-memory on; mutable-global, multi-value, multi-memory, saturating-float-to-int, reference-types, tail-call, extended-const, custom-page-sizes and wide-arithmetic off; floats on.
- **The page ceiling** is a `StoreLimits` limiter.
- **Per file,** a fresh `Store` and instance, then `osg_alloc`, an input copy, `osg_parse`, a result copy and complete host validation. Nothing persists across files.

**The native leg** (`harness/src/native.rs`).
- The `tree-sitter` 0.27.0 crate, with the four grammars compiled natively by `harness/build.rs` from the same pinned `parser.c` and `scanner.c`.
- A fresh `Parser` per file.
- Its `SyntaxTreeV1` serializer is written in Rust, independently of the shim. **P3 therefore also cross-checks two serializer implementations.**

**`SyntaxTreeV1` as E0 encodes it.** The lead ruled this layout probe-only; E2a fixes the normative one.
- **Header,** 16 bytes: `"OSGT"`, then u32 version 1, u32 node count, u32 maximum depth.
- **Records,** 20 bytes each, little-endian, one per **visible** node in the preorder of the `TSTreeCursor` walk (the public API view):
  - u16 symbol, from `ts_node_symbol`: the public symbol after aliasing, with ERROR = 0xFFFF;
  - u16 field, from `ts_tree_cursor_current_field_id`, 0 for none;
  - u16 flags: bit 0 named, bit 1 extra, bit 2 error (`ts_node_is_error`), bit 3 missing;
  - u16 reserved, always 0;
  - u32 start byte, u32 end byte, u32 child count (`ts_node_child_count`).
- **Depth** counts the root as 1.
- **Bounds:** `maxNodes` 4,194,304 and `maxDepth` 4,096, applied while serializing (item 11).

**Host validation** (`harness/src/tree.rs`), applied to every tree before use:
- header and length;
- every range within the input and nested in its parent;
- siblings ordered and non-overlapping;
- symbols in the table, or 0xFFFF (lead ruling);
- fields in the table;
- flags closed;
- child counts consistent with the preorder;
- depth and count agreeing with the header and within the bounds.

**Fuel** counts everything the fresh instance executes for the file (`osg_alloc` plus `osg_parse`), measured from the store. Instantiation consumes no fuel. The two result getters run after the measurement point.

**The rules.** `analyze.py` was written in phase 1, before any data existed, and was run unchanged in phase 2.

## Results by criterion

### P1 — reproducible: PASS

Build roots `SCRATCH/build-a` and `SCRATCH/build-b` each received fresh copies of every input. The 132-file input trees were identical, and so were the module bytes:

| Module | sha256 (A = B) | Bytes |
|---|---|---|
| javascript | `38ebebc5d9d5ac4a910c2a594211c27ef75e3ac23c216d5fadd3f5deb868cce9` | 510,841 |
| rust | `a6f1b0cdd20d5a6d339d756182d61797e498a2188b78264283ecff71151d82f0` | 1,218,678 |
| tsx | `f168a25d413dd6e30a1e2d4ba654e08a162907474823bd31e4d43f186596b260` | 1,545,173 |
| typescript | `634f6218687a1f796c6786d640530982ac18f6319f7ce3386875a74c562a75d6` | 1,510,790 |

Evidence: `results/p1-a.sha256` and `results/p1-b.sha256`. A third root, C, built later with the diagnostic-bearing shim, gives the same bytes (`results/p1-c.sha256`). Each four-module build took about 4 s.

### P2 — closed: PASS

Evidence: `results/p2-inspect.tsv`.
- **Imports.** Each module has **0 imports**, counted by the independent reader (`harness/src/wasmbin.rs`) and by wasmi's `Module::imports`.
- **Exports** are exactly A10's set, with A10's types: `memory`, then `osg_abi_version`, `osg_symbols_ptr`, `osg_symbols_len`, `osg_result_ptr`, `osg_result_len` and `osg_alloc_failed`, each `[]→[i32]`; `osg_alloc` `[i32]→[i32]`; and `osg_parse` `[i32,i32]→[i32]`. The engine-side shape check (A9/A10) reports `ok` for all four.
- **Other shape facts:**
  - no start function;
  - one memory per module, not shared and not 64-bit, with no declared maximum, and minimum pages of 22 (javascript), 33 (rust) and 38 (tsx, typescript);
  - one table and two globals;
  - two data segments, of 388,264 (javascript), 1,093,038 (rust), 1,415,120 (tsx) and 1,388,348 (typescript) bytes;
  - target features `+bulk-memory +bulk-memory-opt +sign-ext`;
  - custom sections `name` and `target_features`.
- **Float-free.** All four modules also validate with floats disabled (`results/admit-*.tsv`, column `float_free`). So the `deterministic` feature's NaN canonicalization has nothing to act on in these modules.

### P3 — equivalent: PASS

Evidence: RUN-a, sha256 `d977f7ea…0df2`; `results/summary.json` `P3`.
- **Scope:** all 8,351 regular selected files, sorted, one thread, both legs.
- **Equivalence.** The wasm status equals the native status for every file, and **all 8,351 tree byte strings are equal**.
- **Size of the comparison.** 13,943,471 nodes. The median tree has 393 nodes and depth 16. The largest is `yarn-4.18.1.cjs`, with 1,827,929 nodes and depth 430.
- **Validation.** No validation failure on either leg.
- **Not vacuous.**
  - 8,112 distinct (content, grammar) pairs map to 7,988 distinct trees, and no content maps to two trees.
  - The symbol tables agree too: A11's canonical `SymbolTableV1`, decoded from each module, has the same digest as the one recomputed from the natively linked `Language`.

  | Grammar | `SymbolTableV1` digest | Language ABI | Symbols | Fields |
  |---|---|---|---|---|
  | javascript | `5a0738c3…` | 15 | 265 | 36 |
  | rust | `0363b059…` | 15 | 355 | 31 |
  | tsx | `c8759474…` | 14 | 400 | 43 |
  | typescript | `daa3b998…` | 14 | 383 | 40 |

  The canonical JSON of each table, wasm and native, is in `SCRATCH/out/symtab/`.
- **Outcomes** (item 10), the same on both legs:

  | Grammar | `parsed` | `syntax-error` |
  |---|---|---|
  | javascript | 1,652 | 4 |
  | rust | 2,339 | 15 |
  | tsx | 550 | 3 |
  | typescript | 3,769 | 19 |

  That is 41 `syntax-error` files in all, for example napi-rs's `examples/napi/example.wasi.d.cts`. They are DR-G13 quality data, not an E0 criterion.

### P4 — order-free: PASS

Evidence: `results/summary.json` `P4`.
- **Rule.** Per file, the tuple (status, tree sha256, fuel, peak pages) must be identical across all four runs. Every run used a fresh instance per file.
- **The runs:**

  | Run | Order | Threads | Modules | Table sha256 |
  |---|---|---|---|---|
  | RUN-a | sorted | 1 | build root A | `d977f7ea…` |
  | RUN-b | shuffle, seed 1 | 1 | build root A | `51ef0223…` |
  | RUN-c | shuffle, seed 2 | 8 | build root A | `c495cea6…` |
  | RUN-d | reverse | 4 | build root B | `f802bb17…` |

- **Result:** 0 differing files in B, C or D. The runs processed 8,353, 8,352 and 8,354 files away from their list position, so the orders really differed.

**Discrimination controls** (not gated). They show that P4's check can detect order dependence when it exists.
- **Lazy translation** (wasmi's default `CompilationMode`; RUN-lazy, shuffle seed 1; RUN-lazy2, sorted):
  - 28 and 30 files respectively are charged extra fuel against the eager baseline;
  - the total is identical in both orders, 2,932,216 fuel;
  - but it lands on whichever files first reach each function: **43 files' fuel differs between the two lazy orders**;
  - trees are unchanged.

  **Fuel under lazy translation is order-dependent.** That makes `Eager` an E2b obligation (lead ruling).
- **Instance reuse** (RUN-reuse, forbidden in the product): 8,347 of 8,351 files' fuel differs from the fresh-instance baseline, and trees are unchanged.

### P5 — fast enough: FAIL (P5a)

Evidence: RUN-t, sha256 `e871c8d2…`; `results/summary.json` `P5`.
- **Setup.** Wasm leg only, sorted, one thread, on a quiet machine (see Host), after a warm-up over every tenth file (RUN-warmup).
- **Rule** (the lead's ruling on phase 1's predeclared reading). Per-file time is the whole per-file cost: fresh store and instance, input copy, parse including in-module serialization, result copy and host validation. Throughput is bytes ÷ time, in MiB/s (2^20 bytes).

| Measure | Value | Gate |
|---|---|---|
| **P5a**: median per-file throughput, over the 8,328 non-empty files | **0.818 MiB/s** | ≥ 1.0 → **fails** |
| **P5b**: slowest file | **6.23 s** (`yarn-4.18.1.cjs`, 3,784,940 bytes); next is `yarn-4.17.1.cjs` (3,019,751 bytes) at 5.50 s | ≤ 10 s → passes |
| Aggregate (Σ bytes ÷ Σ time) | 0.931 MiB/s | not gated |
| Median of the parse step alone (alloc, copy, parse, in-module serialization) | 0.883 MiB/s | not gated |

**Distribution.**
- The 10th and 90th percentiles are 0.453 and 1.383 MiB/s.
- Medians by grammar: javascript 0.631, rust 0.901, tsx 0.755, typescript 0.855 MiB/s.
- Aggregates by grammar: javascript 0.681, rust 1.072, tsx 0.824, typescript 1.038 MiB/s.
- The median fresh-instance cost is 113 µs.

**Where the time goes.**
- Instantiation is 1.5%.
- Parse plus serialization inside the module is 97.7%.
- Result copy plus host validation is 0.8%.

**The failure therefore does not depend on how "median throughput" is read.** The aggregate (0.931) and the parse-only median (0.883) also fall below 1.0. The shortfall is interpretation speed. For context only (a relative floor is rejected by E1 item 3): the native leg's median per-file throughput in RUN-a, which includes its serialization and validation, is 12.66 MiB/s, about 15.5× faster.

**Ungated diagnostic** (RUN-diag-rootonly, sha256 `7756af54…`; module digests in `results/diag-rootonly-modules.sha256`).
- **What it measures.** The same modules rebuilt with `-DOSG_DIAG_ROOT_ONLY`, so the shim emits only the root record and skips the serialization walk. This measures the parse alone.
- **Result.** The median becomes **1.047 MiB/s**, and the aggregate 1.195 MiB/s.
- **Serialization's share** is 22.1% of time but only 7.7% of fuel.
- **What it does and does not mean.** The margin is narrow. A product shim with a cheaper serialization could land on either side of the floor. **This diagnostic is not a product configuration,** because the host needs the full `SyntaxTreeV1` (item 2). It changes nothing in the predeclared outcome.

### P6 — bounded: PASS

Evidence: `results/summary.json` `P6`; RUN-limits, sha256 `1fb3faa0…`.

**Constants,** derived from RUN-a by the rule predeclared in phase 1:

| Constant | Value | Derivation |
|---|---|---|
| `fuelBase` | **190,000** | 4 × the maximum fuel over the 23 empty files (41,407–46,191), rounded up to 2 significant figures |
| `fuelPerByte` | **420,000** | ⌈max over non-empty files of (4 × fuel − base) ÷ bytes⌉, rounded up to 2 significant figures |
| `maxMemoryPages` | **20,896** | 4 × the maximum peak of 5,221 pages, rounded up to a multiple of 16 |

- **Fuel margin.** Every file uses at most **24.94%** of its budget, by construction. The tightest file is vite's `packages/vite/src/node/ssr/__tests__/fixtures/errors/syntax-error.js`: 13 bytes, 1,408,984 fuel, a syntax error.
- **Memory, the binding test (lead ruling).** The maximum peak is 5,221 pages (326 MiB, on `yarn-4.18.1.cjs`), so the ceiling is 20,896 pages, 1.28 GiB. **20,896 ≤ 65,536, so it passes.** The 4× ceiling uses 32% of the wasm32 limit.
- **Verification.** Under (190,000, 420,000, 20,896) as real bounds, RUN-limits ran 4 threads over all 8,351 files: **0 truncations and 0 faults** (8,310 `parsed`, 41 `syntax-error`).
- **Fuel budget for a 4 MiB file** (lead request): 190,000 + 420,000 × 4,194,304 = **1,761,607,870,000 fuel**. That is about **112 s** at the median fuel rate measured on T2a (15.8 G fuel/s, RUN-t).
  - **The time equivalent varies widely.** Per-file fuel rates, over files whose parse took at least 1 ms, range from 1.5 G to 81 G fuel/s, which puts the same budget at 22 s to 1,179 s.
  - **Why.** wasmi's fuel is not a count of executed operators. In wasmi 2.0, a `block` frame has no counter of its own and charges its operators to the enclosing loop, if or function frame, paid on entry (`translator/func/visit.rs`, `visit_block`). A `br_table` into one case of tree-sitter's generated lexer switch therefore pays for every case. The default cost table is 1 fuel per operator (control operators 0) and 1 fuel per 64 bytes of bulk copy.
  - **Consequence.** Fuel is deterministic (P4) but over-approximates executed work, so a fuel bound limits CPU time only within that spread.
- **Boundary controls** (not gated), over every tenth file (836), with budgets equal to each file's measured fuel and peak pages from RUN-a:

  | Budget | Result |
  |---|---|
  | Exact fuel and exact pages | no truncation (832 `parsed`, 4 `syntax-error`), fuel and trees equal to RUN-a |
  | One fuel unit less | `truncated:fuel` for all 836 |
  | One page less | `truncated:memory` for all 836: 633 through the allocator's `osg_alloc_failed` flag on a refused `memory.grow`, and 203 refused at instantiation, where the peak was the initial size |

  So exhaustion is told apart from a fault exactly as item 11 requires, and neither bound ever produced a `backend-fault`.

## Recorded, not gated

**Admission chain cost** (item 5, steps A9–A11 as E0 implements them). Three repetitions; evidence `results/admit-{1,2,3}.tsv`.

| Module | Read + hash | Parse, validate, eager translate | Shape | Instantiate | ABI + symbol table | **Total** | Admission fuel |
|---|---|---|---|---|---|---|---|
| javascript | 0.86–1.39 ms | 1.58–2.31 ms | ≤ 2 µs | 72–103 µs | 118–200 µs | **2.6–4.0 ms** | 126,116 |
| rust | 2.14–2.91 ms | 1.45–1.97 ms | ≤ 2 µs | 121–177 µs | 46–62 µs | **3.8–5.1 ms** | 163,985 |
| tsx | 2.64–3.43 ms | 1.51–1.87 ms | < 1 µs | 142–185 µs | 51–59 µs | **4.4–5.5 ms** | 187,165 |
| typescript | 2.61–3.12 ms | 1.47–1.65 ms | < 1 µs | 33–35 µs | 47–60 µs | **4.2–4.9 ms** | 178,318 |

**The minimal `wasmi` feature set used:** `default-features = false`, features `std`, `validate` and `deterministic` (`results/wasmi-features.txt`).
- **Dispatch.** No dispatch feature is enabled. wasmi then uses its tail-call dispatch, which aarch64 release builds support.
- **Optional features.** `std` is a convenience; wasmi is `no_std`-capable with `alloc`.
- **Not used:** `wat`, `simd`, `memory64`, `auto-dispatch`, `portable-dispatch`, `extra-checks`, `hash-collections`.
- **Crate closure.** This feature set resolves to **8** host crates: `wasmi`, `wasmi_core`, `wasmi_ir`, `wasmi_collections`, `wasmparser` 0.228.0, `spin`, `libm` and `bitflags` (`results/crate-closure.txt`). E1 item 1 estimated 7; the eighth, `bitflags`, comes in through `wasmparser`.

## Lead rulings applied

These rulings were made after phase 1 and before any data existed; they are recorded in the overnight log.

1. **P5:** the strict per-file reading is the gate. The aggregate and the parse-only median are reported, not gated.
2. **`SyntaxTreeV1` layout:** probe-only, documented above. E2a fixes the normative layout.
3. **wasmi compilation mode:** `Eager`. The lazy control was run and shows the order dependence. Eager compilation becomes an **E2b obligation**.
4. **ERROR symbol 0xFFFF:** the one explicit exception to the symbol-table and contiguity checks. This is an **E1 record item** (below).
5. **P6:** the predeclared derivation rule is used. The 4 MiB budget is given in seconds, and memory is the binding test.
6. **`TREE_SITTER_WASM_STDLIB`:** left undefined.
7. **Substitutions accepted;** each is recorded below.

## Substitutions

1. **Upstream pins.** E1 pins no commits; its versions are [U] observations, and E2a makes the pins. E0 used E1's named candidates at their release tags:
   - runtime `v0.27.0`;
   - `tree-sitter-rust` `v0.24.2`;
   - `tree-sitter-typescript` `v0.23.2`;
   - `tree-sitter-javascript` `v0.25.0`.

   The commits are in the Inputs table. Every generated ABI (15, 14, 14, 15) is inside the runtime's accepted range of 13–15.
2. **The module allocator.** tree-sitter's wasm-stdlib allocator (`external_scanner_allocator.c`) serves scanners only: it has a hard 4 MiB heap and a linear first-fit free list. It cannot serve the runtime.
   - **What E0 used instead:** a first-party, deterministic, O(1) segregated-fit allocator in the shim. It has an 8-byte header, 16-byte classes up to 256 bytes and power-of-two classes above that, with no splitting or coalescing.
   - **On exhaustion** it sets `osg_alloc_failed` and traps; it never returns NULL.
   - **Consequence:** P6's peak-page figures are this allocator's.
3. **wasi-sdk 34 rather than 33.** tree-sitter 0.27 itself pins wasi-sdk 33 for its own stdlib build; E1 names 34, and E0 used 34. The libc sources are vendored in the tree-sitter tag, and no SDK libc or compiler-rt is linked (`-nostdlib`), so only the compiler differs.
4. **Explicit Wasm target features:** `-mcpu=mvp -mbulk-memory -msign-ext`. Bulk-memory is what the vendored `memcpy`, `memset` and `memmove` are written for (`BULK_MEMORY_THRESHOLD`). The modules' `target_features` section lists exactly `bulk-memory`, `bulk-memory-opt` and `sign-ext`.

## E1 record items and observations

**Record item.**
- **The ERROR symbol (0xFFFF) lies outside `SymbolTableV1`'s contiguous ids** (A11) and outside "a symbol in the table" (item 10). It must be the one explicit exception in both checks. The Rust binding treats ids ≥ 65,534 as valid for the same reason; 65,534, the internal ERROR_REPEAT, never appears in the visible tree.

**Obligations and observations for E2a and E2b:**
- **Eager compilation is required** (P4 control). Lazy translation moves translation fuel onto whichever file first reaches a function. The engine identity's `fuelModel` should therefore name the compilation mode, or E2b should fix `Eager` in the host configuration.
- **Fuel over-approximates executed work** (P6). Per-file fuel rates vary about 50-fold. A fuel bound is a deterministic bound on CPU work, but not a tight one in wall time.
  - **The predeclared derivation is dominated by tiny error-recovery files.** The 13-byte file above costs about 108,000 fuel per byte. Files of at least 4 KiB never exceed 31,540 fuel per byte.
  - **So the resulting 4 MiB budget is loose:** about 112 s at the median rate.
  - E2a may want a derivation that fits small and large files separately. That would be a choice for E2a; E0's result stands.
- **Item 4's closure layout omits the wasm headers.** The modules compile against `crates/language/wasm/include/*.h`, which come from the tree-sitter tag (and its `tree-sitter-language` crate) and sit outside `lib/`. Under T-wasm, `runtime/source/**` would need to hold them along with `lib/src/wasm-stdlib/**`. This is moot under T-native.
- **`TREE_SITTER_WASM_STDLIB` would add `export_name` to every libc function** and break A10's closed export set. A T-wasm lane must leave it undefined.
- **Host crate count** under the minimal feature set is 8, not 7 (`bitflags`).
- **Supertype symbols.** tree-sitter 0.25+ has a fourth symbol type, supertype. `SymbolTableV1`'s `{named, visible}` maps it to `false/false`, the same as auxiliary symbols. The flags lose that distinction; E2a may want a type field.

## Deviations and side effects

- **The `fdopen` stub was removed.** Phase 1's shim carried an `fdopen` stub because a grep missed that `lib/src/wasm-stdlib/stdio.c` defines it. The first phase-2 link failed with a duplicate symbol; the stub was removed and the build re-run. Both P1 roots used the corrected shim (`2f2cee98…`).
- **The harness was fixed after the main runs.** RUN-a measures fuel before the two result-getter calls, so the first "exact budget" control starved those getters, and all 836 sampled files reported `backend-fault`.
  - **Fix:** the getters now get a small uncounted allowance, as the trap classifier's flag read already did (`harness/src/wasm.rs`).
  - **Re-run:** only the three boundary controls, which then behaved as predicted.
  - **Unaffected:** the fix runs after the fuel measurement point, so RUN-a to RUN-t and RUN-limits are unchanged.
- **Additions to phase 1's plan.** RUN-lazy2 (a second lazy order) and the root-only diagnostic were added in phase 2. `phase2-run.sh` now includes both, labelled as additions.
- **How the plan was run.** It was executed step by step from the agent's shell, with the same commands. zsh does not word-split the `$R` prefix that `sh` splits, so the first attempt of step 5 failed harmlessly before any run started.
- **No repository code was executed.** T2a bytes were fetched by commit into bare repositories with hooks disabled, then materialized with `git cat-file`; they were used only as parse input. Nothing was written into any repository.
- `~/Library/Application Support/OpenSIP` stayed absent. The private 413 UUID fixture was not read. The product repository was not touched.
- **Another process used the real `~/.cargo` during phase 1.** `~/.cargo/.global-cache` changed at 04:31:36 PDT, when someone else's `cargo test --workspace --locked --offline` (pid 21800) started; E0's cargo calls all used SCRATCH's `CARGO_HOME`.
- **Phase 2 wall time:** 12 min 48 s of machine work (12:07:59 to 12:20:47 UTC). That was a 7 s harness build, about 4 s per module build, and 14 sweeps, the longest of them 56 s. Writing the report took about 15 minutes more.

## Not claimed

- No qualification evidence, no Q6 figure and no hostile-input safety (E-N4). The fuel and page bounds were exercised on T2a only.
- No product decision beyond E1 item 3's predeclared outcome. The P5 margin and the ungated diagnostic are recorded for the lead's item-18 M4 re-decision. They are not grounds to choose T-wasm under E1 as written.
- No cross-platform claim. Every number is this host's.
- `SyntaxTreeV1`'s byte layout and `SymbolTableV1`'s canonical encoding are E0's own. E2a fixes the normative forms.
