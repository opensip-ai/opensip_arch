# Syntax crate and grammar registry — proposal M3-E1 r2

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. Law for unit **M3-E** of the accepted M3 unit plan (M3P:214): sub-unit **E1**, the law. It also fixes the scope, order and gates of the E2 and E3 code units.

**Draft r2, not accepted. Not code.** This law touches no product file. P0 creates `crates/syntax` as a workspace member (M3P:210), and every E code unit waits for the gates in item 20.

r1 (`PROPOSAL-r1.md`, sha256 `90175f28…`, 69,559 bytes) was reviewed by Codex (`/tmp/opensip-implementation/reviews/codex-syntax-e-r1/`): three required findings (E-R1, E-R2, E-R3) and five non-blocking observations (E-N1 to E-N5). r2 answers all of them. The "r2 changes" table maps each finding to the items that change.

**Lead decisions.** Items 1 to 20, with 14a and 14b, hold lead decisions dated 2026-10-04. They are made under the owner's standing direction to decide on the lead's recommendation and to block only where no recommendation exists. Each one names the alternatives it rejects, and the owner may reverse any of them. No item needs an owner decision to proceed. Four are flagged to the owner in "Owner notes".

## r2 changes and review responses

| Finding | Change |
|---|---|
| **E-R1** (the candidate-only result) | New **item 14a**: the executed result of a syntax-only `clones-near` binding is the retained `CandidateProducerResultV1` (EXS:833-1058), bound through the existing execution-input owner (EXC §6; EXM:1465-1555). It has rows for a successful empty result, every per-file outcome, every parse and group bound, unsupported census paths and backend faults. No fact and no Coverage. New **item 14b**: the producer and stage coordinates of all syntax-universe work. It names the core provider closure, which needs cross-law obligation **X-C1** on C's CRC-1. The census rule is **X-C2**. New successor **SYN-1F** carries the `source-parse-error` mirror into every foundation `NativeCause` copy, including the execution-inputs schema (EXS:201-218) that EXM:851 holds equal to NES. New unit **E2s** applies SYN-1 and SYN-1F to the product's schema sources, registries and generated carriers. New controls E3-T8 to E3-T12 cover `clones-near` alone with a syntax-error file, with each exhausted bound, with an unsupported census path, with a backend fault, and with a successful empty result. E3-T13 and E3-T14 cover the producer. Items 10, 11, 12 and 19 cross-refer. |
| **E-R2** (the admission chain) | **Item 5** now states the complete, ordered admission chain A1 to A12: fixed paths, size bounds and canonical bytes; manifest-to-descriptor and **definition-to-manifest-row** equality for every repeated field; `executionModel` against module presence; engine and runtime compatibility; static module validation under the host's fixed feature set; zero imports; **closed exports with exact types**; the ABI version; and the **canonical `SymbolTableV1` digest** recomputed from the module. Under T-native, the same ABI, symbol-table and runtime joins are bound to the linked `Language` and the compiled-in table. Static incompatibility gets **pre-Plan refusal keys** on NE:3530's route. Execution faults stay `operational-failed`. Item 4 gains size bounds. New controls E2-T24 to E2-T32. SYN-1's key list is updated. |
| **E-R3** (the H join) | **Item 20**: E3 depends on the **accepted H law's interface**, which M3P:261 assumes before day 0, not on integrated H. Its integration edges are E2c, C1a, B2-c and E2s, so E3 finishes on **day 14** with **14 days of slack** (M3P:303, M3P:342). **Final wiring and its controls belong to whichever of E3 and H integrates second.** Under M3P r6 that is H (day 22), so the syntax join's end-to-end controls are in H's acceptance scope. The candidate envelope's capture belongs to J2 (day 25), which also integrates second. M3P r6's K2 (by day 28), O2_selected (by day 31), lead-set (by day 22) and 33-day host-chain figures are preserved. |
| E-N1 | M3P now cites the accepted **r6**. r4 is cited only for the historical lean (M3P-r4:299, the pinned bytes `1526c483…`, which Codex recovered from `6f85fe71`). |
| E-N2 | Dependency counts are marked estimates. SYN-DEP freezes the minimal feature set (`wasmi` with `default-features = false`, so no `wat`) and counts the resolved closure. P3 now says "ten dialect selectors (nine owned code suffixes plus `.d.ts`)". The missing declarative grammar in Rust parsers is a preference, not a prohibition. |
| E-N3 | DR-G21 scopes external components (REG:366). E's parser-survival controls are an **E extension**. The C-worker rejection now distinguishes what a same-user child does give (address-space, crash and resource separation) from what it does not (filesystem authority). |
| E-N4 | E0 is a feasibility choice, not qualification or hostile-input proof. The M3/M4 distinction is **exposure scope**, not benign bytes. T-wasm's isolation is conditional on the engine and validator TCB; T-native keeps possible host crashes and weaker bounds as declared residual risk. |
| E-N5 | No change needed. |

## Short names

Lines were checked against the files named here on 2026-10-04.

- **M3P** `docs/implementation/m3/M3-PLAN.md` (**r6, accepted**). **M3P-r4** the accepted r4 bytes (`1526c483…`), cited only at line 299 for the lead's earlier lean. **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r6, accepted). **B** `docs/implementation/m3/config-discovery-b/PROPOSAL.md` (r2, accepted). **C** `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` (r3, draft, with CODEX2). **L** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (r1, draft, acceptance-gated). **OPP** `docs/implementation/m3/operability/PLAN.md` (r3, accepted), cited by section.
- **BP** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`. **CH14** `docs/v2/architecture/14-repository-and-module-layout.md`. **COV** `docs/v2/architecture/implementation-coverage.v1.json`. **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`. **F02** `docs/v2/architecture/02-distribution-and-components.md`.
- **NE / IE / SL / AQ** `docs/v2/contracts/product-v1/{native-evidence,identity-and-evidence,security-and-lifecycle,admission-and-qualification}.md`.
- **EXC / EXS / EXM** `docs/coop/design-corrections/foundation/{execution-inputs-contract.v1.md, execution-inputs.schema.v1.json, execution_inputs_model.v1.py}`, the execution-input owner. **ENC / ENS** `docs/coop/design-corrections/foundation/{enumeration-contract.v1.md, enumeration-plan.schema.v1.json}`.
- **NES** `docs/coop/design-corrections/native/native-evidence.schemas.v2.json`. **NEM** `docs/coop/design-corrections/native/native_evidence_model.v2.py`. **NCM** `docs/coop/design-corrections/native/native-capability-matrix.v2.json`. **IDS** `docs/coop/design-corrections/foundation/identity-schemas.v3.json`. **RPS** `docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json`.
- Product paths are under `opensip/`, at main `3e64266`.
- **Upstream facts** (crates.io and GitHub REST API, read-only, 2026-10-04) are marked **[U]**. They are observations of public metadata on that date, not pins. The pins are made in E2a (item 6).

## Acceptance gate

This law may be reviewed and accepted now.
- **It launches nothing.** No process is spawned and no confinement is claimed, so O7 is not a gate item (M3P:476-487; L:494-506).
- **It relies on two drafts** for its code units only: C r3, for closure admission and the synthetic signer (C items 7 and 8, C:282 and C:320), and L r1, for "no in-process fallback" (L:132). Item 20 holds each E code unit until what it uses is accepted.
- **It places two obligations on C** (item 14b): **X-C1**, the core provider closure as the producer of syntax-universe work, which amends C item 9 and C2-T13 (C:409-411, C:435); and **X-C2**, the syntax-only `clones-near` census for C4a. They gate E3 and the producer fixtures E2b builds, not this law's acceptance. The lead routes them to C's next revision.
- **E0's outcome is not a gate.** Item 2 predeclares both branches and the rule that picks between them. E0's result is recorded as a lead decision, not as a revision of this law, unless it falls outside the predeclared branches (item 3).

## Decisions at a glance

| # | Decision | Rejected |
|---|---|---|
| 1–2 | **Backend: tree-sitter grammars, executed in the host inside a fuel-metered WebAssembly memory boundary** (one module per code grammar row, run by the pure-Rust `wasmi` interpreter). Natively linked tree-sitter is the predeclared fallback. | a pure-Rust parser per language; hand-written parsers; a confined syntax component; tree-sitter's own wasmtime store; native linking as the first choice |
| 3 | **E0**, a lead-run feasibility probe with six predeclared pass criteria, chooses between the two branches. | choosing without a probe |
| 4–6 | **The closure** holds the executed modules, their complete build inputs, one definition record per grammar row, a bundle manifest carrying the limits and the engine identity, the normalizer specification, and the notices. Every pin is a digest. **Admission is a complete ordered chain** (A1 to A12): every repeated field is joined, exports are closed and typed, and the ABI and symbol-table digest are checked. Static incompatibility refuses before PlanId. | regenerating `parser.c` from `grammar.js`; linking compiled-in grammars that have no retained build inputs; rebuilding modules at admission |
| 7 | **One grammar registry file**, owned by `opensip-identity` and used by discovery, the evaluator and the syntax crate. It is drift-checked against the pinned schema sources. | a second copy in `crates/syntax`; a dependency of syntax on the evaluator |
| 8 | **Seven languages, eight grammar rows, fourteen suffixes.** TypeScript has two rows, `typescript` and `tsx`. The four data-document rows are **format definitions: no parser is pinned, linked or run.** | pinning and shipping data-format parsers that no capability reads |
| 10–11 | **Per-file outcomes.** Any ERROR or MISSING node makes the whole file a parse error: no facts and no bodies from it, and the new cause `source-parse-error` (SYN-1). The size, fuel, memory, node and depth bounds give typed truncation (`budget-exhausted`). A backend fault fails the step. | salvaging error-free subtrees; reporting a truncation as complete; an operational fault disguised as Coverage |
| 12–16 | **The syntax-only mode** serves exactly its eleven cells, selects every bundle row, and never stands in for a semantic rung. **`clones-near`'s executed result is the retained `CandidateProducerResultV1`** (14a). **Syntax-universe work is produced by the core provider closure** at its own execution-plan stage (14b). | partial selections derived from repository content; any fallback after a provider failure; an empty successful envelope over a failed examination; the grammar closure re-kinded as a producer |
| 17–18 | **Placement: in the host, not a component.** The WebAssembly boundary is defence-in-depth memory isolation, **not a sandbox claim**. | a confined syntax worker at M3 |
| 19–20 | **Successors:** SYN-1 (native contract), SYN-1F (foundation mirrors), SYN-NS (normalizer specification), SYN-REG, SYN-DEP and SYN-LANE, plus C's CR-1 and the obligations X-C1 and X-C2. **Units:** E0, E2a, E2s, E2b, E2c and E3. E3 builds to the accepted H interface and finishes on day 14. The critical path does not move. | E3 gated on integrated H |

---

## A. The backend (CH14:614)

**1. Candidates and criteria.**
- **The question.** CH14:614 leaves open: "Review the pure crates/syntax backend, retained signed grammar inventory and host dispatch/admission joins; this selects no new provider protocol." M3P-r4:299 recommended "a trial between tree-sitter and hand-written parsers", with the lead leaning to tree-sitter and accepting that "its C runtime joins the host TCB (BP:680-682)". The brief asks for that lean to be weighed against O7's direction for hostile input (M3P:476-487).
- **Candidates.**
  - **T-native:** tree-sitter's C runtime and upstream generated grammars, compiled into the host through the `tree-sitter` crate and the grammar crates.
  - **T-wasm** (found here): the same C sources compiled once, by a pinned toolchain, into one WebAssembly module per grammar row. The modules are retained in the grammar closure and run inside the host by `wasmi`, a pure-Rust interpreter, under deterministic fuel.
  - **P-rust:** a pure-Rust parser per language: `oxc_parser` or `swc_ecma_parser` for TS/JS, and `ra_ap_syntax` or `syn` for Rust.
  - **H-hand:** first-party hand-written parsers.
  - **C-worker:** any of the above, run in a confined child process.
- **Product state** (`3e64266`). There is no tree-sitter, WebAssembly or grammar dependency anywhere in the workspace, and `crates/syntax` is not a member (`Cargo.toml:3`). The host already compiles C: `rusqlite` with `bundled` (`crates/storage/Cargo.toml:13`, `crates/security/Cargo.toml:10`) builds SQLite through `cc` (`Cargo.lock:21-24`, `:168-177`). The toolchain is `1.95.0` (`rust-toolchain.toml:2`).

| Criterion | T-native | T-wasm | P-rust | H-hand | C-worker |
|---|---|---|---|---|---|
| **Determinism across the four platforms** | Strong in practice, but it rests on four C compilers agreeing about C code that includes hand-written scanners. The work bound is the progress-callback operation count. No safe memory bound: the default allocator calls `abort()` on failure ([U] `lib/src/alloc.c`). | **By construction.** Bit-identical interpretation, deterministic `wasmi` fuel, and a fixed linear-memory ceiling ([U] `wasmi` 2.0.0 has a `deterministic` feature). | Strong, but differs per library | Strong | As the backend inside, plus IPC ordering |
| **Self-contained closure** (DR-119, REG:308; DR-G14, REG:359; BP:685-688) | Compiled into the host, so the closure is a **retained copy** of the sources, and a compiled-in digest table has to prove they match | **The executed bytes are the retained bytes.** The crate takes "admitted source and grammar bytes" literally (BP:677-678; CH14:375) | The "grammar definition" would be crate source code, with no declarative definition to retain | Same as P-rust | As the backend inside |
| **Licences** (product Apache-2.0, `LICENSE`, L1 at product `2967905`) | [U] runtime MIT; `tree-sitter-rust`, `-typescript`, `-javascript` MIT | Same, plus [U] `wasmi` family MIT/Apache-2.0, `wasmparser` Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT, `spin` MIT, `libm` MIT. The build toolchain is [U] Apache-2.0 (wasi-sdk) and build-only | MIT / Apache-2.0 | first-party | — |
| **Supply chain** | [U] `tree-sitter` 0.27.0 pulls `regex` (+`regex-automata`, `regex-syntax`), `streaming-iterator` and `tree-sitter-language`, plus three grammar crates. `cc` and `serde_json` are already locked, though the build dependency enables `serde_json/preserve_order`. About 8 new crates (an estimate; see below). | About 7 new crates in the host (`wasmi`, `wasmi_core`, `wasmi_ir`, `wasmi_collections`, `wasmparser`, `spin`, `libm`), with `default-features = false`, since [U] `wasmi`'s defaults include `wat`. The grammar sources are **lane inputs, not Cargo dependencies**. Plus one pinned build toolchain. | Large and fast-moving. [U] `oxc_parser` 0.152.0 needs Rust 1.96 (the newest release at ≤ 1.95 is 0.146.0); `ra_ap_syntax` 0.0.356 needs 1.98 and publishes weekly | none | + D1, D3 |
| **unsafe and C in the host address space** | [U] about 553 KB of runtime C and headers (`lib/src`, upstream HEAD), about 27 MB of generated parser C (mostly tables: Rust 6.5 MB, JS 2.9 MB, TS and TSX 8.7 MB each), and about 34 KB of hand-written external scanners (Rust 12,588 B; JS 10,576 B; TS `common/scanner.h` 10,097 B), **all parsing hostile bytes in the unconfined host** | **No C in the host.** The same C runs inside linear memory, with zero imports. The host's unsafe code is `wasmi`'s own, which the dependency policy records | Small unsafe; no C | none | C isolated by a process, but **effective only where O7's confinement works** |
| **Grammar pinning** | crate archive checksums plus member digests | module digests plus member digests of every build input | crate checksums | source digests | — |
| **Performance** | Fastest | Interpretive overhead, **unmeasured**. E0 measures it against floors (item 3) | Fast | Unknown | Spawn and IPC per universe |
| **Python readiness** | [U] `tree-sitter-python` 0.25.0, MIT | Same, plus no host relink for new grammar bytes | [U] `ruff_python_parser` 0.0.16 needs Rust 1.97 | A new parser | As the backend |
| **Fit with BP and CH14** | BP:680-682 accepted it | Fits BP:676-683 (in-host, pure crate) and CH14:375 | Fits, but has no grammar definition | Fits | **Contradicts** CH14:614 and BP:676-679 ("no … process execution"; no new protocol) |
| **Survives a parser fault.** This is an E extension: DR-G21 (REG:366) scopes external components, not the host's own parser | **No.** A segfault or `abort()` kills the host | **Yes.** A trap is an ordinary `Err` | Mostly (panics) | Mostly | Yes |

  **The crate counts are estimates.** They depend on the resolved feature graph. SYN-DEP (item 19) freezes the minimal host feature set and records the resolved closure, which is the binding count (E-N2).

**2. Decision: tree-sitter grammars, executed in the host inside a fuel-metered WebAssembly memory boundary (T-wasm). T-native is the predeclared fallback.**
- **Decision.**
  - **Grammar technology.** tree-sitter, using the upstream generated grammars for the four code rows (item 8): `tree-sitter-rust`; `tree-sitter-typescript`'s `typescript` and `tsx` grammars; and `tree-sitter-javascript`. The upstream generated `parser.c` and `scanner.c` are used as published, pinned by digest. They are never regenerated.
  - **Execution.**
    - One module per code grammar row is built from the pinned runtime, the pinned grammar sources and a first-party shim, by a pinned compiler with explicitly listed target features.
    - A module **imports nothing**. Its exports are the closed, typed set of item 5's step A10: the ABI version, the symbol table, allocation and its exhaustion flag, parse, and the result location.
    - `crates/syntax` interprets modules with `wasmi`, with fuel metering on and the `deterministic` feature, and with a fixed maximum of linear-memory pages.
    - **Each file gets a fresh instance.** No state, heap or table crosses files, so a corrupted instance can affect only the file that corrupted it, and results do not depend on order.
  - **Output.** The shim writes a flat preorder node array (`SyntaxTreeV1`, internal and not a contract): symbol, flags (named, extra, error, missing), field, start byte, end byte and child count. The host validates it completely before any use (item 10, outcome `backend-fault`).
  - **The executed bytes are the closure bytes.** The host executes the module bytes of the admitted `kind=grammar` closure. It holds no grammar code of its own.
  - **Engine identity is identity-bearing.** Fuel accounting is part of `wasmi`'s implementation. So the bundle manifest names the engine and its version (item 5), and a host whose compiled-in engine differs refuses the bundle (`native.syntax-grammar-engine-mismatch`, SYN-1). An engine upgrade is therefore a new grammar closure.
  - **The fallback (T-native).** If E0 fails any criterion, the same grammars are linked natively under BP:680-682's accepted TCB statement, with the controls of item 18. Items 4 to 16 hold for both branches. Where they differ, the item says so.
- **Basis:**
  - BP:676-683: a pure crate that "takes immutable admitted source and grammar bytes and returns inert candidates", with no "process execution", and with parser code as part of the host TCB.
  - BP:685-688: "Static linking does not remove the retained `kind=grammar` closure obligation … a compiled-in grammar with no retained closure is insufficient."
  - CH14:375: `parser.rs` parses "with the selected retained grammar".
  - M3P-r4:299, the lead's lean: one `grammarVariant` and anchor model across languages.
  - REG:366 (DR-G21): a component failure "never crashes the core". That gate scopes external components; holding the in-host parser to the same property is this law's extension (E-N3).
  - AQ:347: "Every physical dependency … belongs to the admitted closure/TCB inventory."
  - M3P:476-487: O7's direction hardens hostile-input handling. Under T-native the host's own parser would be the least hardened reader of the same bytes the confined providers read.
- **Rejected:**
  - **P-rust.**
    - Three different tree models, so three body, anchor and normalizer implementations, against M3P-r4:299's single model.
    - The current releases exceed the pinned toolchain ([U] Rust 1.96 for `oxc_parser`, 1.98 for `ra_ap_syntax`). Pinning older releases freezes the product on a fast-moving 0.x line, and moving the toolchain is a re-pin.
    - No declarative grammar definition to retain. BP:687 does not require one, so this is a preference for a reviewable, data-shaped definition, not a prohibition (E-N2).
    - [U] Its Python parser also exceeds the toolchain.
  - **H-hand.**
    - TS/JSX/Rust grammar coverage (generics, ASI, regex versus division, template literals, decorators, macros) is months of work, and its error modes are a quality risk under DR-G13 (REG:358).
    - AQP:114 forbids degrading "to a weaker parser".
    - It does not fit E2's sizing (M3P:303).
  - **C-worker at M3** (item 17).
  - **tree-sitter's own wasmtime "wasm store"** (the `wasm` feature of the `tree-sitter` crate; [U] it depends on `wasmtime-c-api-impl`). The runtime's parse loop still runs natively over hostile bytes, and only the lexers and scanners move into WebAssembly. It also brings a JIT and a large unsafe TCB.
  - **T-native as the first choice.** It is cheaper, but:
    - a parser memory-safety defect becomes code execution in the unconfined host, which holds the store and the trust state;
    - an allocation failure aborts the host (REG:366);
    - the work bound depends on a callback cadence rather than a fuel model;
    - the retained closure is only a copy, so the identity of what ran rests on a build-time digest table rather than on the executed bytes.
  - **Regenerating `parser.c` from `grammar.js`.** It needs Node and the tree-sitter CLI in the lane. Upstream's generated file is what upstream tests.
- **Forbidden substitutes:**
  - any grammar code compiled into the host under T-wasm;
  - a module with any import;
  - an instance reused across files;
  - a wall-clock timeout as a parse bound;
  - a parse result consumed before validation;
  - a grammar row whose module is not a member of the admitted closure;
  - an engine version other than the manifest's.
- **Controls** (E2b):
  - E2-T1: a module declaring any import refuses at load (`native.syntax-grammar-module-import-forbidden`).
  - E2-T2: the same file parsed first, last, alone, and after a hostile file, gives byte-identical trees and identical fuel.
  - E2-T3: a module whose bytes differ from its definition record's digest refuses.
  - E2-T4: a manifest naming another engine version refuses.
  - E2-T5: a trap inside a module is an `Err`, and the test process survives. This is the DR-G21 property, which E extends to its own parser.

**3. E0, the feasibility probe.**
- **Decision.**
  - **What it is.** E0 is a lead-run throwaway probe outside the product, like S-P and CF-P (M3P:207, M3P:501). It runs over public, pinned bytes only: the pinned upstream sources and T2a's code files. It executes no repository code.
  - **What it builds.** The four code modules, with a candidate toolchain (wasi-sdk, [U] latest release `wasi-sdk-34`) against tree-sitter's own WebAssembly libc subset ([U] `lib/src/wasm-stdlib`).
  - **Pass criteria, fixed now:**
    1. **P1, reproducible.** Two clean builds give byte-identical modules.
    2. **P2, closed.** Every module has zero imports.
    3. **P3, equivalent.** For every T2a file whose suffix matches one of the ten dialect selectors (the nine owned code suffixes plus `.d.ts`), up to 20,000 files, the module's `SyntaxTreeV1` equals the native tree-sitter tree for the same pinned runtime and grammar commits, byte for byte.
    4. **P4, order-free.** Shuffled orders and fresh instances give identical trees and identical fuel use.
    5. **P5, fast enough.** On this host, the median throughput is at least 1 MiB/s, and every file of at most 4 MiB parses within 10 s.
    6. **P6, bounded.** Fuel constants exist under which no T2a code file of at most 4 MiB uses more than 25% of its budget, and its peak linear memory stays within the page ceiling with the same margin.
  - **Outcome.**
    - All six pass: T-wasm. E0 records the measured constants, which E2a writes into the bundle manifest (item 5).
    - Any criterion fails: T-native. The failing criterion is recorded, item 18's fallback posture applies, and the manifest's `executionModel` is `native-linked-v1`.
  - **Also recorded, not gated:** the cost of item 5's admission chain (module validation and the one admission instantiation per code row), and the minimal `wasmi` feature set E0 used.
  - **What E0 is not.** It is a feasibility choice between two predeclared branches. It is not qualification evidence and not proof against hostile input (E-N4).
  - **Recording.** The report is `docs/implementation/m3/syntax-e/E0-REPORT.md`, a record and not law. A result outside both branches, for example a defect in the equivalence itself, reopens this law as r2.
- **Basis:** M3P-r4:299 asked for "a trial"; M3P:501 (CF-P) is the precedent probe with a predeclared fallback; AQP:126 (O3) says syntax-only cells have no latency budget, so P5 is a usability floor that this law sets, not a product budget.
- **Rejected:**
  - **Deciding without measuring.** Interpreter overhead is unknown here.
  - **A relative floor** (for example "at least ⅕ of native"). It would reject a design whose absolute speed is adequate for the population the syntax universe serves (item 15).
- **Forbidden substitutes:** E0 numbers presented as Q6 or qualification evidence; E0 code entering the product.
- **Controls:** E0-REPORT pins every input by sha256 and records the toolchain identity, the per-criterion result and the host.

---

## B. The `SyntaxGrammarBundleV1` closure

**4. What the closure contains.**
- **Decision.** One `kind=grammar` closure (IDS:278) holds exactly these regular files. Fixed paths are given here; `<g>` is a `grammarId`.

| Path | Member | Bound by |
|---|---|---|
| `opensip-interface/grammar/bundle-manifest.v1.json` | the bundle manifest (item 5) | `bundleDigest` (NES:2257) |
| `opensip-interface/grammar/<g>/definition.v1.json` | one definition record per row (below) | `grammars[].grammarDigest` |
| `opensip-interface/grammar/<g>/module.wasm` | the executed module (code rows; T-wasm only) | the definition record's `module.sha256` |
| `opensip-interface/grammar/<g>/source/**` | the upstream build inputs of a code row: `parser.c`, `scanner.c`, its headers, `grammar.json`, `node-types.json` and the upstream licence | the definition record's `sources[]` |
| `opensip-interface/grammar/runtime/source/**` | the tree-sitter runtime sources that the modules compile, and its licence | the definition records' `runtime.sources[]` |
| `opensip-interface/grammar/shim/**` | the first-party shim source | `shim.sha256` |
| `opensip-interface/grammar/build-receipt.v1.json` | toolchain identity (name, version, archive sha256), target features, and exact compile and link argument vectors | the manifest's `buildReceiptSha256` |
| `opensip-interface/grammar/normalizer.v1.json` | per-row node-kind tables (item 14) | `normalizer.specificationDigest` (NES:2375) |
| `opensip-interface/normalization/specification-map.v1.json` and the level specifications it names | the IE body-identity normalization law, at IE's fixed path | IE:1068-1089 |
| `opensip-interface/grammar/notices/**` | every third-party notice the closure's bytes require | the manifest's `notices[]` |

  - **A code-row definition record** is `{schemaVersion: 1, grammarId, languageId, syntaxClass, suffixes, grammarVersion, upstream: {repository, tag, commit}, sources: [{path, sha256, bytes}], runtime: {repository, tag, commit, sources: [...]}, shim: {path, sha256, bytes}, module: {path, sha256, bytes} | null, shimAbi, languageAbi, symbolTableSha256, notices: [path]}`.
    - `module` and `shimAbi` are `null` only under T-native.
    - `shimAbi` is the shim's export ABI (item 5, A10–A11), `1` in this law.
    - `languageAbi` is the tree-sitter language ABI of the grammar's generated tables.
    - `symbolTableSha256` is the raw SHA-256 of the grammar's canonical `SymbolTableV1` (item 5, A11).
  - **A data-document definition record** is `{schemaVersion: 1, grammarId, languageId, syntaxClass: "data-document", suffixes, grammarVersion: "format-definition.v1", format: {name, reference}, parse: "none"}` (item 8).
  - **Encoding.** Every record is canonical JSON under the identity crate's canonical encoder, the same rule IE:1072-1074 uses for the specification map.
  - **Size bounds,** checked on the tree row's `bytes` before any member is read: the manifest, each definition and the build receipt at most 1 MiB each; the normalizer specification at most 4 MiB; each module at most 32 MiB. A larger member refuses at A3 (item 5).
  - **The tree is closed.** Every member is named by the manifest or by a definition record, at the path it names (A6).
  - **Platforms.** A module is platform-neutral, so the closure tree is identical for every `platformId`. Each platform still gets its own `closure2` because `platform` is in the identity (BP:701-704). Body identity does not change across platforms, because `body-language-version` takes `parserName`, `parserVersion` and `bundleDigest`, not `closureId` (IDS:4533-4555).
- **Basis:**
  - BP:685-688: "Retain its exact manifest, grammar definitions and normalizer bytes".
  - NE:223-232: "every grammar definition, the bundle manifest and the normalizer specification present in the retained tree".
  - NEM:2426-2442, mirrored by the product at `crates/evaluator/src/native_context.rs:276-305`: the bundle, grammar and normalizer digests must be tree members.
  - IE:1068-1089: the specification-map path and its checks.
  - F02:98 and F02:136: a licence and notice inventory per component.
- **Rejected:**
  - **Retaining only the modules.** Without their build inputs, nobody could rebuild a module or audit its provenance.
  - **Retaining the toolchain in the closure.** It is a build input, identified by digest in the receipt. It is never executed at analysis time.
  - **One digest over all grammars.** NES requires a digest per grammar row.
- **Forbidden substitutes:** a member reached through a symlink or directory row (BP:707-709); a tree path outside `opensip-interface/`; any closure member that no record names.
- **Controls** (E2a, E2b):
  - E2-T6: a closure with a member no record names refuses.
  - E2-T7: a record naming a missing member refuses (`native.syntax-grammar-definition-mismatch`).
  - E2-T8: the existing NEM:2426-2442 refusals still fire (version, bundle, grammar and normalizer not in the closure).

**5. The bundle manifest and the complete admission chain.**
- **Decision.**
  - **The manifest** is `{schemaVersion: 1, parserName, parserVersion, executionModel, engine, limits, grammars, normalizer, buildReceiptSha256, notices}`.
    - `executionModel` is `wasm32-fuel-v1` or `native-linked-v1`.
    - `engine` is `{name: "wasmi", version, fuelModel}` or `{name: "tree-sitter", version}`.
    - `limits` are item 11's values.
    - `grammars` are the rows `{grammarId, languageId, syntaxClass, suffixes, grammarVersion, definitionPath, grammarDigest}`, ordered by `grammarId`.
    - `normalizer` is `{normalizerId, normalizerVersion, specificationPath, specificationDigest}`.
  - **Values.** `parserName` is `opensip.syntax.tree-sitter.wasm32`, or `opensip.syntax.tree-sitter.native` under T-native. `parserVersion` is the closure manifest's `semanticVersion` (NE:225-227). The normalizer is `opensip.syntax.normalizer` version `1`.
  - **The limits are identity-bearing.** `bundleDigest` is `body-language-version.compilerBuild` under the syntax universe (IDS:4533-4555). So changing a limit changes every syntax body identity, and a borderline file cannot silently flip between parsed and truncated under one identity.
  - **The admission chain (E-R2).** Admission runs when the host mints `native.context.syntax.v2`, before PlanId, in this order. Each step names its refusal keys. Every key is a `native.syntax-grammar-*` or `native.syntax-normalizer-*` key that SYN-1 adds to NE:3530's pre-Plan route: `request-rejected` (2), `REQUEST.PRECONDITION_FAILED`, request detail. Refusals are collected into one sorted, deterministic set. A step that would read a member an earlier step refused is skipped for that member. **Modules are never rebuilt at admission.**

| Step | Check | Owner | Refusal key (subject) |
|---|---|---|---|
| A1 | The closure is admitted through C2a's single signed path, with role `grammar` mapped to kind `grammar` and a regular-file tree only (C item 7, C:282) | security (C2a) | C's existing keys |
| A2 | The NE §1.2 row checks: version from the manifest, the bundle, grammar and normalizer digests in the tree, and class, body-language, suffix and ambiguity (NEM:2426-2478) | evaluator, `native_context.rs:276-361` | the existing `native.syntax-grammar-*` keys |
| A3 | **Fixed paths, sizes and canonical bytes.** The manifest is at `opensip-interface/grammar/bundle-manifest.v1.json`, within its size bound, canonical (re-encoding reproduces the bytes), and hashes to `bundleDigest`. Each row's `definitionPath` is exactly `opensip-interface/grammar/<grammarId>/definition.v1.json`, within bound, canonical, and hashes to `grammarDigest`. The normalizer is at `specificationPath` = `opensip-interface/grammar/normalizer.v1.json`, within bound and canonical, and hashes to `specificationDigest`. The build receipt hashes to `buildReceiptSha256`. Each module is within its bound. | `grammar.rs` | `-bundle-manifest-mismatch` (`<member>:<path\|size\|canonical\|digest>`); `-definition-mismatch` (`<g>:<path\|size\|canonical\|digest>`) |
| A4 | **Descriptor to manifest.** The admitted `SyntaxGrammarBundleV1` (NES:2257-2407) equals the manifest's projection field by field: `parserName`, `parserVersion`, every grammar row and `normalizer` | `grammar.rs` | `-bundle-manifest-mismatch` (`descriptor:<field>`) |
| A5 | **Definition to manifest row.** Each definition's repeated `grammarId`, `languageId`, `syntaxClass`, `suffixes` and `grammarVersion` equal its manifest row exactly (canonical value equality) | `grammar.rs` | `-definition-mismatch` (`<g>:<field>`) |
| A6 | **The member closure.** Every member a definition lists (sources, runtime sources, shim, module, notices) exists at its listed path with its listed sha256 and byte length. Every tree member is named by the manifest or a definition. Every code definition names the same runtime pin, so one runtime per bundle. | `grammar.rs` | `-definition-mismatch` (`<g>:member:<path>`); `-bundle-manifest-mismatch` (`unlisted:<path>`, `runtime-pin`) |
| A7 | **Execution model against module presence.** Under `wasm32-fuel-v1`, every code row has a non-null `module` at `opensip-interface/grammar/<g>/module.wasm` and a non-null `shimAbi`. Under `native-linked-v1`, every `module` and `shimAbi` is null. Every data row has `parse: "none"` and no module. | `grammar.rs` | `-execution-model-mismatch` (`<g>`) |
| A8 | **Engine and runtime compatibility.** The manifest's `engine` equals the host's compiled-in engine identity (`name`, `version`, `fuelModel`). Each limit is in its admissible range (item 11), and `maxMemoryPages` is at most the engine's 65,536. Under T-native, the definitions' runtime pin equals the compiled-in runtime version. | `grammar.rs` | `-engine-mismatch` (`<field>`) |
| A9 | **Static module validation** (T-wasm). The engine parses and validates each module under the host's **fixed** configuration, the same `wasmi` configuration and feature set used for execution, with fuel on. Invalid bytes, an unsupported feature, a start function, any table or global export, or a memory that is shared or 64-bit refuse. Any import refuses separately. | `parser.rs` | `-module-invalid` (`<g>:<reason>`); `-module-import-forbidden` (`<g>`) |
| A10 | **Closed exports with exact types.** The export set equals, by name and type: `memory` (one linear memory); `osg_abi_version: [] → [i32]`; `osg_symbols_ptr`, `osg_symbols_len`, `osg_result_ptr`, `osg_result_len` and `osg_alloc_failed`, each `[] → [i32]`; `osg_alloc: [i32] → [i32]`; `osg_parse: [i32, i32] → [i32]`. A missing, extra or wrongly typed export refuses. | `parser.rs` | `-module-exports-mismatch` (`<g>:<export>`) |
| A11 | **ABI and symbol table.** One admission instance per module, with a fixed admission fuel allowance and the page ceiling. `osg_abi_version()` must equal the host's shim ABI (`1`) and the definition's `shimAbi`. The exported symbol table is decoded within bounds (at most 65,535 symbols and 65,535 fields; names valid UTF-8 of at most 1,024 bytes; ids contiguous) into the canonical record `SymbolTableV1` = `{schemaVersion: 1, grammarId, languageAbi, symbols: [{id, name, named, visible}], fields: [{id, name}]}`, with both arrays in id order. Its raw SHA-256 must equal `symbolTableSha256`, and its `languageAbi` must equal the definition's. A trap, fuel exhaustion or bound violation during these calls is static incompatibility (`-module-invalid`, `<g>:admission-call`), not a parse fault. The admission instance is then discarded; no file is parsed with it. | `parser.rs` | `-abi-mismatch` (`<g>`); `-symbol-table-mismatch` (`<g>:<digest\|languageAbi\|bounds>`) |
| A12 | **Normalizer and registry.** Every node kind and field `normalizer.v1.json` names for a row exists in that row's `SymbolTableV1` (item 14). The bundle is the whole registry (item 7). | `grammar.rs` | `native.syntax-normalizer-kind-unknown` (`<g>:<kind>`); `-bundle-not-the-registry` |

  - **Under T-native** (if E0 fails), A9 to A11 bind to the linked code instead.
    - The host carries a compiled-in table, one row per code grammar: `{grammarId, grammarDigest, languageAbi, symbolTableSha256, runtimeVersion}`. The SYN-DEP tool generates it from the same pinned sources and checks it.
    - At admission, each definition must equal its table row.
    - The host also recomputes `SymbolTableV1` from each linked tree-sitter `Language`: the symbol and field counts, names and flags, and the language ABI. Its digest must equal the table's. This binds the compiled code itself, not only the table.
    - Mismatches refuse with `native.syntax-grammar-build-mismatch` (`<g>:<field>`). This is the drift check BP:688 needs when the parser is compiled in.
  - **Static versus execution failures.** Everything in A1 to A12 is a property of the installed closure. It is decided before PlanId and refuses the request; it is never `operational-failed`, and never Coverage. A fault while parsing a source file after admission is item 10's `backend-fault`, on the `operational-failed` route.
  - **A missing closure.** An installation with no admissible grammar closure cannot mint `native.context.syntax.v2`. A request that needs a syntax universe then refuses before PlanId under the native-context route (NE:3530; keys added by SYN-1). No other parser is substituted and no partial universe is minted.
- **Basis:** NES:2257-2407 (the descriptor); BP:685-691 and NE:223-232 (the exact retained grammar and context joins); NE:3530 (the pre-Plan route), and NE:3543-3544 (no detail may be left unmapped); IDS:4533-4555 (`compilerName`, `compilerVersion` and `compilerBuild` come from the bundle); BP:716-717 ("neither PATH nor a system compiler supplies an implicit fallback"). The evaluator's existing owner (`native_context.rs:276-361`) checks only versions, digest membership, class, body language, suffixes and ambiguity, so A3 to A12 are new and belong to `grammar.rs` and `parser.rs` (item 7).
- **Rejected:**
  - **Limits as host constants outside the closure.** A host upgrade could change outcomes under unchanged identities.
  - **A descriptor built by the caller.** The host mints it from the manifest (C item 8).
  - **Rebuilding modules at admission** to prove them. That needs the toolchain at analysis time. A3 to A11 bind the executed bytes directly; reproducibility is the lane's check (item 6).
  - **Trusting the definition's `symbolTableSha256` without recomputing it from the module.** A correctly hashed definition could then describe a different grammar.
  - **Routing static incompatibility to `operational-failed`.** It is a property of the installed closure, known before any file is read.
- **Forbidden substitutes:** a `parserVersion` typed beside the manifest rather than taken from it; a default grammar set when the closure is absent; an admission instance reused for parsing; a module accepted because its hash matches while its exports or ABI do not.
- **Controls:**
  - E2-T9: each manifest and descriptor field mismatch refuses separately (A4).
  - E2-T24: each of the five repeated definition fields, made to disagree with its row while every digest and the descriptor join still hold, refuses with its own subject (A5). This is the r1 counterexample.
  - E2-T25: a module present under `native-linked-v1`, missing under `wasm32-fuel-v1`, or present on a data row, refuses (A7).
  - E2-T26: a shim reporting ABI `2` against a definition saying `1` refuses (A11).
  - E2-T27: a definition whose `symbolTableSha256` or `languageAbi` differs from the module's recomputed `SymbolTableV1` refuses, with the definition re-hashed so that A3 passes (A11).
  - E2-T28: a correctly hashed member that is not WebAssembly refuses `-module-invalid` before PlanId, and no Plan exists (A9).
  - E2-T29: correctly hashed modules with, separately, an unsupported feature, a start function, an extra export, a missing export and a wrongly typed export each refuse their key (A9, A10).
  - E2-T30: an engine identity mismatch, and runtime pins that differ across definitions, refuse (A6, A8).
  - E2-T31 (T-native): a definition disagreeing with the compiled-in table, and a linked `Language` whose recomputed symbol table disagrees, refuse `-build-mismatch`.
  - E2-T32: an oversized or non-canonical manifest, definition or normalizer refuses at A3 before its bytes are parsed.
  - E3-T1: a syntax-only request with no grammar closure installed refuses before PlanId, and no Plan exists.

**6. Versions and pins.**
- **Decision.**
  - **Upstream pins.** Each code row pins its upstream repository, release tag and full commit, and the sha256 and length of every source member it compiles. The runtime is pinned the same way. Pins are taken from release tags, never from a branch head.
  - **Selection rule** for E2a: the newest upstream release, as of E2a, whose generated sources carry an ABI the pinned runtime accepts; MIT-licensed; recorded in the dependency policy (item 19, SYN-DEP).
    - [U] Candidates on 2026-10-04: runtime `tree-sitter` 0.27.0 (crate; Rust ≥ 1.90), `tree-sitter-rust` 0.24.2, `tree-sitter-typescript` 0.23.2 and `tree-sitter-javascript` 0.25.0.
    - `tree-sitter-typescript`'s last release dates from 2024-11 [U]. Newer TypeScript syntax may therefore produce parse errors. Those are measured as DR-G13 quality (REG:358) and disclosed by item 10. They are never patched locally.
  - **Toolchain pin.** The compiler archive by version and sha256, and the exact target-feature list, recorded in the build receipt. Feature defaults are never inherited.
  - **`grammarVersion`.** The upstream tag for a code row, such as `v0.24.2`, with the commit in the definition record. `format-definition.v1` for a data row.
  - **`semanticVersion`.** It changes with every change to the closure tree. The lane refuses to publish two different trees under one `semanticVersion`. C2-T5 (C:318) already makes a changed version over the same tree a new `closure2`.
  - **Updating a grammar** is a new closure plus a dependency-policy row change, reviewed as an inventory unit. A registry change, meaning a language, suffix, class or capability, is a registry successor (item 7).
  - **Under T-native,** the Cargo lock pins the crate archives by checksum, and the member digests are checked against the unpacked archives by the SYN-DEP checker.
- **Basis:** BP:696-697; BP:1055-1061 ("Record exact versions and license/dependency closures when a candidate is selected"); C2-T5 (C:318).
- **Rejected:**
  - **Tracking upstream heads.** That is non-reproducible.
  - **Local grammar patches.** The grammar would no longer be upstream's, and the definition record would mislead.
  - **Semver ranges** anywhere.
- **Forbidden substitutes:** a member pinned by version string alone; a toolchain found on PATH; a bundle rebuilt in place under the same `semanticVersion`.
- **Controls:** SYN-LANE's reproducibility check rebuilds from the retained sources with the pinned toolchain and compares bytes; E2-T10: a definition record whose member digest differs from the retained bytes refuses.

**7. One registry, closed and drift-checked.**
- **Decision.**
  - **One file.** The closed registry (`bundledGrammars`, `grammarCapabilities`, `bodyLanguages`, the grammar dialect table and `bodyLanguageByVariant`) moves into **one file owned by `opensip-identity`**, `crates/identity/src/grammar-registry.json`, exposed as a parsed, immutable table.
    - Today the first three members live in `crates/evaluator/src/native-context-registry.json` (read at `native_context.rs:15` and `native_universe.rs:393`).
    - The evaluator's `native_context.rs` and `native_universe.rs`, B2's `discovery.rs` (the U-4 suffix families, NE:788-805) and `crates/syntax/src/grammar.rs` all read it from identity.
    - The evaluator file keeps only `configNodeKindLaw`.
  - **Drift check.** A tool check (SYN-REG) asserts that the file equals the projection of `schemas/sources/native-v2.schema.json#/x-opensip-grammar-capability-registry` (`:571`) together with the syntax-universe dialect table and `bodyLanguageByVariant` of `schemas/sources/identity-v3.schema.json`. The source map already pins both (`schemas/source-map.json:125-133`). A byte drift fails the check.
  - **Admission.** It is layered.
    - The evaluator's existing owner (`native_context.rs:276-361`, mirroring NEM:2426-2478) keeps the NE §1.2 row checks: class, body-language, suffix and ambiguity.
    - `grammar.rs` adds the execution joins of items 4 to 6.
    - It adds one completeness rule: **a product bundle is the whole registry.** Its rows cover the seven languages and the fourteen suffixes exactly, each suffix owned by exactly one row (`native.syntax-grammar-bundle-not-the-registry`, SYN-1).
    - Synthetic fixtures may build partial bundles only to exercise refusals.
  - **No ambient discovery.** The host never scans for grammars. The only grammars are the rows of the admitted closure. No configuration key adds, removes or substitutes a grammar (BP:696-697).
  - **Language-neutral by construction.** `grammar.rs` and `parser.rs` contain no branch on a language. Every language-specific fact is registry data, definition-record data or normalizer-table data. The only per-language code is `normalization.rs`'s scope rules for L3 (item 14), behind one trait with one implementation per code language. Item 19's PY-REG lists what a Python row changes.
- **Basis:**
  - BP:676-677: syntax depends "only on contracts and identity", so it cannot read the evaluator's file.
  - BP:696-697: "New grammars or relations require a reviewed registry successor, not ambient plugin discovery."
  - NES:536-646 (the registry, "Normative and CLOSED"); NES:641 ("Adding one is a deliberate registry change, not a caller choice"); IDS:4598 (the bundled set and the body enum "held equal by an explicit drift check").
  - The precedent for an embedded registry is `crates/evaluator/src/capabilities.rs:12`.
- **Rejected:**
  - **A second copy in `crates/syntax` with an equality test.** It leaves two owners, and B2 would make a third.
  - **Syntax depending on the evaluator.** BP:676 forbids it.
  - **A registry passed in by the host.** That is caller-supplied law.
- **Forbidden substitutes:** a suffix table written into `discovery.rs` or `grammar.rs`; a grammar row admitted because its class or suffix "looks right"; a bundle row outside the registry used for anything.
- **Controls:**
  - E2-T11 (`grammar_tests.rs`, CH14:378): exactly seven languages and fourteen suffixes; each refusal of NEM:2426-2478 fires; an unbundled grammar refuses.
  - E2-T12: removing any one row from a product bundle refuses with the completeness key.
  - SYN-REG check: a one-byte change to the registry file, or to either schema source, fails.

---

## C. Languages, suffixes, outcomes and limits

**8. The table: seven languages, eight grammar rows, fourteen suffixes.**
- **Decision.**

| `languageId` | `syntaxClass` | `grammarId` | Suffixes (owned) | `grammarVariant` (IDS:4556-4583) | Body language | Parser | Capabilities (NES:543-640) |
|---|---|---|---|---|---|---|---|
| `javascript` | code | `javascript` | `.cjs` `.js` `.jsx` `.mjs` | `cjs` `js` `jsx` `mjs` | javascript | `tree-sitter-javascript` | syntax ×3, clones, inventory ×3 |
| `json` | data-document | `json` | `.json` | — | — | none (format definition) | inventory ×3 |
| `markdown` | data-document | `markdown` | `.md` | — | — | none | inventory ×3 |
| `rust` | code | `rust` | `.rs` | `rs` | rust | `tree-sitter-rust` | syntax ×3, clones, inventory ×3 |
| `toml` | data-document | `toml` | `.toml` | — | — | none | inventory ×3 |
| `typescript` | code | `tsx` | `.tsx` | `tsx` | typescript | `tree-sitter-typescript` (tsx) | syntax ×3, clones, inventory ×3 |
| `typescript` | code | `typescript` | `.cts` `.mts` `.ts` (`.d.ts` resolves through `.ts`) | `cts` `mts` `ts` `ts-declaration` | typescript | `tree-sitter-typescript` (typescript) | syntax ×3, clones, inventory ×3 |
| `yaml` | data-document | `yaml` | `.yaml` `.yml` | — | — | none | inventory ×3 |

  - **The count.** Fourteen suffixes: 4 + 1 + 1 + 1 + 1 + 1 + 3 + 2. Seven languages and eight rows. Here "syntax ×3" is `declares`, `literal` and `control-flow` at `syntactic`; "clones" is `clones@normalized-body-hash`; and "inventory ×3" is `file@enumerated`, `package@manifest-declared` and `vcs-change@vcs-reported`.
  - **Two TypeScript rows.** `.tsx` and `.ts` are different grammars upstream: type assertions `<T>x` against JSX. NE:517-524 already allows two rows of one language to own disjoint subsets.
  - **Data-document rows are format definitions.** Their `grammarDigest` names a definition record with `parse: "none"` (item 4). No data-format parser is pinned, linked, built or run. The files remain `grammar-only` members bearing inventory evidence (NE:281-288). This is a lead decision, recorded in SYN-1 as a clarifying sentence.
- **Basis:**
  - NE:260-263 and NE:788-796: the seven languages and the fourteen suffixes.
  - NCM:192: data grammars "mint no body identity and produce no code-construct fact".
  - NES:539-542, the `data-document` class law: "this kit publishes no tokenisation … law".
  - NES:642: data-format facts are "a bounded future capability".
  - NES:646: inventory is "not grammar-gated".
  - So no registered capability reads a data-document parse.
- **Rejected:**
  - **Pinning and running tree-sitter JSON, TOML, Markdown and YAML grammars** ([U] all MIT). That is four more C grammars in the parse path, two with large hand-written external scanners ([U] YAML 51,548 B, Markdown 59,243 B), for zero capability, and with a parse status that has no lawful carrier.
  - **Pinning them but never running them.** That is supply-chain and licence rows for dead bytes. A future capability must choose its parser together with the tokenisation law that NE:300-302 requires.
  - **One TypeScript row owning `.tsx`.** It would misparse either JSX or type assertions.
- **Forbidden substitutes:** a data-document row claiming `code`, or the reverse (NE:290-293); a `.d.ts` row; a suffix in two rows.
- **Controls:** E2-T11 covers the table; E2-T13: no data-document file ever reaches `parser.rs` (an assertion in the dispatch path and a test).

**9. Routing and unsupported files.**
- **Decision.**
  - **Membership** is B2's, under U-4: `syntax-only` / `grammar-only` when the final extension, taken from the last `.` of the file name, is one of the fourteen; otherwise `unsupported-file` / `no-bundled-grammar` (NE:788-796; NEM:3801-3803).
  - **Row selection** within the syntax universe is the unique longest suffix over the union of the selected rows' suffixes (NE:517-524). The grammar variant is then the longest match in the dialect table (IDS:4556-4573), so `x.d.ts` reads under the `typescript` row as `ts-declaration`.
  - **Matching is byte-exact and case-sensitive.** `.TS`, `.Rs` and `.YML` are `unsupported-file`. Changing that is a registry successor.
  - **An unsupported file** (including `.py` today, extensionless files and case variants) is inventoried, so `file@enumerated` is always available (NES:646). It never reaches the crate. A code-capability scope that names it is the published disclosure: `unknown`, `language-tier-unsupported`, `capability-missing` (NE:447-458, NE:496-504). It is never refused outright and never `complete`.
  - **A file with no unit of its family** in a mixed repository is `no-program-unit-for-language` and gets no syntax claim unless a syntax-only cell is explicitly requested at a root that contains it (NE:893-899; B:481).
- **Basis:** NE:693-702 (U-4); NE:304-306 (`.py`); B:411, B:480-481.
- **Rejected:** case-folding suffixes, which is a silent reinterpretation (IDS:4573); routing by content sniffing, which is a non-registry decision.
- **Forbidden substitutes:** parsing an `unsupported-file`; a `complete` code Coverage over an extent containing only unsupported or data paths.
- **Controls:** E3-T2: a repository of `.py` and `.md` files gives U-9's fallback unit, inventory `complete`, and `unknown` with `language-tier-unsupported`/`capability-missing` for every code cell (B:411's T1 case).

**10. Per-file parse outcomes and how each is typed.**
- **Decision.** `parser.rs` returns exactly one outcome per code-grammar file. The host derives Coverage; the crate never constructs it (BP:678-679). The table gives the Coverage of fact-bearing capabilities. **`clones-near` has no Coverage.** The same outcomes reach its retained candidate envelope instead (item 14a).

| Outcome | When | Facts and bodies | Coverage of code capabilities over any scope whose extent contains the file |
|---|---|---|---|
| `parsed` | valid tree, no ERROR or MISSING node | yes | complete, subject to the registry law (NE:308-360) |
| `syntax-error` | bytes are not valid UTF-8 (the parser is not run), or the tree has any ERROR or MISSING node | **none from the file** | `unknown`; `input-closure-incomplete`; `nativeCause` **`source-parse-error`** (new, SYN-1); `examinedExhaustive` true |
| `truncated:<bound>` | `size`, `fuel`, `memory`, `nodes` or `depth` (item 11) | none from the file | `unknown`; `budget-exhausted`; `nativeCause` null; `resolutionCompleteness.stageTerminal` `budget-exhausted`; `examinedExhaustive` false |
| `backend-fault` | a trap other than fuel or memory exhaustion; output failing `SyntaxTreeV1` validation (ranges outside the input or not nested, a symbol outside the table, count or depth disagreeing); or a protocol violation by the module | none | **not a Coverage answer.** The syntax step fails as an operational fault: class `operational-failed` (4), code `SYSTEM.OUTCOME.ILLEGAL_STATE` (the `host-invariant` mapping NES's `successorArtifactObligation` already owes), detail `HOST.INVARIANT_VIOLATED`, subject `native.syntax-backend-fault:<grammarId>`. SYN-1 proposes this route, and J1/`outcomes.rs` owns the projection. It is never retried with another backend. **No candidate envelope is emitted** (item 14a). |

  - **Several outcomes in one scope.** The declared deficiency follows NE §10's precedence (NE:3321-3324): `input-closure-incomplete` outranks `budget-exhausted`. The retained `stageTerminal` may still say `budget-exhausted`, because it is unconstrained on not-applicable entries (NES:881).
  - **Inventory is unaffected.** Inventory Coverage never depends on an outcome (NES:646).
  - **Clones.** A body in a non-`parsed` file is owed but unexamined. It therefore holds a required `clones-fact` cell at `unknown` and is never filtered out (NE:959-970).
  - **Why the whole file.** tree-sitter's error recovery can re-attribute structure outside the ERROR subtree, so "error-free subtree" does not mean "correctly read subtree". Deterministic all-or-nothing per file is the honest unit. Salvaging subtrees would need measured evidence and a successor.
  - **The trust limit.** Evaluator replay does not re-parse, so a host that misreports an outcome is not caught by replay. This is the same trust boundary as provider-produced Coverage, stated as a limit (compare NE:507-516). The determinism suite (AQP:324-327) re-derives outcomes from the retained bytes and closure.
- **Basis:**
  - NE:3365-3374, the §10 table: `input-closure-incomplete`'s cause is "required", and `budget-exhausted`'s carrier is the stage terminal.
  - NES:31-50, the deficiency-cause registry. The precedent for adding causes under `input-closure-incomplete` is the three `body-language-*` members (NES:775).
  - RC-6 (NES ViewEntryV3): `complete` requires `examinedExhaustive`, and `unknown` constrains it in neither direction.
  - AQP:114: refusal, not degradation.
  - AQP:476: typed partial results for broken syntax, which is language-neutral.
- **Rejected:**
  - **A new `DeficiencyV2` member.** It changes the deficiency enum, its D9 bridge and the workflows mirror. A cause under an existing deficiency follows precedent and changes no D9 class or code.
  - **`budget-exhausted` for syntax errors.** That is false.
  - **Partial facts with `complete`.** That is a false universal negative.
  - **Treating a backend fault as truncation.** It hides a defect in a trusted component.
- **Forbidden substitutes:** a null cause on `input-closure-incomplete` (NES:31); any fact anchored in a non-`parsed` file; byte rewriting (BOM stripping, newline normalization) before parsing.
- **Controls:**
  - E2-T14: one fixture per outcome.
  - E2-T15: invalid UTF-8 is `syntax-error`, and the module is not invoked (fuel unchanged).
  - E2-T16: a hostile shim fixture that emits overlapping ranges gives `backend-fault`.
  - E3-T3: the Coverage mapping per row, including precedence with both kinds of file in one scope.

**11. Limits and typed truncation.**
- **Decision.** These values are in the bundle manifest, so they are identity-bearing (item 5). E0 confirms or adjusts the provisional numbers before E2a freezes them. A later change needs a new closure.

| Bound | Provisional value | Checked by | Outcome |
|---|---|---|---|
| `maxFileBytes` | 4,194,304 (4 MiB) | host, before parsing | `truncated:size`; the parser is not run |
| fuel | `fuelBase + fuelPerByte × bytes` (constants from E0, P6) | engine | `truncated:fuel` |
| `maxMemoryPages` | from E0 (P6) | engine; the shim's allocator records the exhaustion before it traps, so this trap is told apart from a fault | `truncated:memory` |
| `maxNodes` | 4,194,304 | shim while serializing, then the host | `truncated:nodes` |
| `maxDepth` | 4,096 | shim, then the host | `truncated:depth` |
| `SubjectIdV1` text | 4,096 characters (RPS) | `candidates.rs` | `truncated:nodes` for the file. The identity is never shortened. |
| clone groups | `maxCandidatesPerGroup` 4,096 and `maxGroupsPerUniverse` 1,000,000 (NE:2576-2580) | `candidates.rs` | a `clones-fact` scope is `budget-exhausted`; a `clones-near` envelope is `partial`/`budget-exhausted` (item 14a). Groups are never cut. |

  - **Walkers are iterative.** Every host walker is iterative, so `maxDepth` bounds L3 scope stacks, not the call stack.
  - **No wall clock.** No bound uses the wall clock. Cancellation is the host's step cancellation (OPP §5.5): the pass checks for it between files, and a cancelled step produces no outcome and no Coverage.
  - **Parallelism.** E3 may parse files in parallel, but outputs are merged in path order, and no byte of output may depend on thread count or completion order.
  - **Under T-native,** fuel is replaced by an operation budget counted in progress-callback invocations, and memory by `maxFileBytes` plus the node bound. That is weaker, and it is recorded in item 18.
- **Basis:** AQP:126 (O3: `analyze` "has no work or termination bound" today, which this item supplies for the syntax pass); NE:2576-2580; NE §10 (`budget-exhausted`).
- **Rejected:**
  - **Unbounded parsing.** That is denial of service by one file.
  - **Wall-clock timeouts.** They make outcomes nondeterministic.
  - **Limits as configuration.** That would be a caller-chosen interpretation.
- **Forbidden substitutes:** silent truncation; partial facts from a truncated file; a limit read from the environment.
- **Controls:** E2-T17: one fixture at each bound ±1 (size, nodes, depth), and a fuel fixture; E2-T18: the same bound gives the same outcome under T2-order shuffles.

---

## D. The syntax-only mode

**12. The eleven cells.**
- **Decision.** The syntax universe serves exactly these cells (NCM rows; COV rows). Everything else is out of mode.

| Capability | NCM state | Produced by | Answer under the syntax universe |
|---|---|---|---|
| `inventory` | SUPPORTED-DESIGN (NCM:997) | host discovery and snapshot (B2, C1), minted under the syntax universe | always available; never grammar-gated (NES:646) |
| `syntax` | SUPPORTED-DESIGN (NCM:269) | `candidates.rs` from code rows (item 13) | `complete` only when item 10 allows it |
| `clones-fact` | SUPPORTED-DESIGN (NCM:855) | `normalization.rs` and `candidates.rs` (item 14) | as for `syntax`, plus the group bounds |
| `clones-near` | SUPPORTED-DESIGN (NCM:866) | `normalization.rs` and `candidates.rs` | candidate-only; no fact and no Coverage entry. **Its executed result is the retained `CandidateProducerResultV1`** (item 14a). NCM:176's `selection-account-only` is only its availability account, never its result. |
| `imports`, `references`, `calls`, `types`, `reachability`, `unresolved-edge` | UNSUPPORTED-TYPED (NCM:694, 704, 714, 724, 734, 744) | the host, no parse | `unknown`, `language-tier-unsupported`, `capability-missing`. Answered, never refused (NCM:162) |
| `clones-cross-tsjs` | NOT-SELECTED (NCM:933) | — | a request refuses `native.requested-capability-mode-not-selected` (NCM:162); never advertised |

  That is 4 supported, 6 unsupported and 1 not selected: 11 cells (COV:2254, 3395, 3432, 3469, 3506, 3543, 3580, 3947, 3984, 4191, 4391), matching M3P:104.
- **Basis:** NE:253-259 ("Capability is not widened"); NE:592 (the §1.3 row); NCM:162 and NCM:176; COV's method, "each syntax grammar is a separate fixture coordinate" (COV:2254-2292).
- **Rejected:** advertising `syntax` for data rows. NE:297-302 forbids it.
- **Forbidden substitutes:** a `complete` answer for any UNSUPPORTED-TYPED cell; a near or cross candidate presented as a fact.
- **Controls:** K2's syntax-only lane (M3P:221) holds one T1 fixture per grammar row per supported cell. E3-T4 checks the six typed disclosures and the one non-advertised cell.

**13. Syntax facts (`syntax@syntactic`).**
- **Decision.**
  - **What is produced.** `candidates.rs` produces inert `declares`, `literal` and `control-flow` candidates at `syntactic` from `parsed` code-row files only. Their payloads are RPS `DeclaresPayloadV1`, `LiteralPayloadV1` and `ControlFlowPayloadV1`, each with exactly one source-text anchor (the RPS anchor law).
  - **What E2c fixes,** inside `normalizer.v1.json`, which SYN-NS reviews:
    - which node kinds declare which `declarationKind`;
    - which tokens are literals of which `literalKind`, and the `valueText` rule;
    - the intra-body control-flow edges.
  - **Constraints this law sets on E2c:**
    - **Subject identities.** `SubjectIdV1` text uses the namespace `syntax`. It is derived from the anchor path and the syntactic container chain, with an occurrence ordinal among same-name, same-kind siblings. It contains **no byte offset and no line number**, matching finding-key2's exclusion (IE:199-202). It must be NFC.
    - **No resolution.** A call is not an edge, and an identifier is not a reference.
    - **No data-document facts** (NE:297-302).
    - **Admission is the host's.** `fact_admission.rs` admits the candidates in H's syntax join (BP:680-681; M3P:218). The crate never mints `fact2`.
  - **TS/Rust modes.** Under the TS and Rust modes, syntax facts come from the providers (`providers/typescript/src/analysis/syntax.ts`, CH14:514; M3P:216), never from `crates/syntax`.
- **Basis:** RPS `$defs`; NE:319-339 (the every-anchor law for code facts); CH14:377.
- **Rejected:** `crates/syntax` serving TS or Rust universes, which would equate a grammar parse with a compiler parse (NE:249-252); line-based subject identities.
- **Forbidden substitutes:** a candidate carrying a `fact2` identity; a subject ID built from offsets.
- **Controls:** E2-T19: inserting a blank line above a declaration leaves its subject ID unchanged; E2-T20: a Markdown-anchored code candidate cannot be produced, and the existing Run-closure guard `SYNTAX_CAPABILITY_UNSUPPORTED_FACT` (NE:319-339; `crates/evaluator/src/capability_support.rs`) refuses one if offered.

**14. Clones under syntax-only (NE:7).**
- **Decision.**
  - **Body spans.** Bodies are those of NE:2582-2598: function, method, closure or lambda, `impl` item and block bodies. Import-only bodies are excluded as candidates; kept bodies hash verbatim.
  - **Levels.** L0 verbatim, L1 lexical, L2 comment-insensitive and L3 identifier-insensitive, under NE's §6.3 tables. `near-v1` uses 5-gram shingles of the L3 stream with Jaccard ≥ 800,000 millionths. The parameters are NE:2576-2580's.
  - **Where the mapping lives.** The node kinds that realize each body kind, comment kind, directive and local-binding rule are tables in `normalizer.v1.json`. E2b refuses a table naming a kind that is absent from the module's symbol table (`native.syntax-normalizer-kind-unknown`, SYN-1). That is the drift check between the normalizer and the grammar version.
  - **Identity.** `body-language-version` is built from the bundle:
    - `compilerName` = `parserName`;
    - `compilerVersion` = `parserVersion`;
    - `compilerBuild` = `bundleDigest`;
    - `dialect` = `{grammarVariant}` (IDS:4504-4610).

    The level specifications sit at IE's fixed specification-map path in this closure (IE:1068-1089). A grammar-parsed body never shares an identity with a compiler-parsed one (NE:249-252).
  - **Owed bodies.** Clones are owed over body-eligible paths only, by suffix in the dialect table (NE:959-970). Data rows bear no body.
  - **Cross-TS/JS** is not selected in this mode (item 12).
- **Basis:** NE:2562-2647 (COV `native-evidence:7`); IE:1068-1089; IDS:4556-4610; NCM:855 and NCM:866.
- **Rejected:** reusing the providers' normalizers. Different tree models give different identity dialects anyway, and providers stay isolated (CH14:514).
- **Forbidden substitutes:**
  - stripping an internal `use` or `import` from a kept body (NE:2585-2591);
  - a level specification outside the closure;
  - L3 renaming of properties, imports, exports, globals, `this` members, fields, paths or macro-introduced names (the NE:2595-2598 tables).
- **Controls:** E2-T21 (`normalization_tests.rs`, CH14:379): the `clone-false-positive-boundary` cases (NE:2640-2643), the import-only exclusion, code/data separation, body grammar identity, and deterministic normalization; E2-T22: the same bytes as `.ts` and as `.js` never group.

**14a. The `clones-near` candidate result (E-R1).**
- **Decision.**
  - **The carrier.** A syntax-only `clones-near` binding's executed result is **exactly one retained `CandidateProducerResultV1`** (EXS:833-1058).
    - It is a host-derived envelope (EXC:259) in the `candidate-producer-result` canonical-record domain (EXC:263).
    - It is bound once to its `(cellOrdinal, programOrdinal)` by the existing execution-input owner (EXC §6, EXC:251-257; EXM:1465-1555; product `crates/evaluator/src/execution_inputs.rs`).
    - It is the **only** record of that work: no `fact2`, no `relation@rung`, no view and no Coverage entry.
    - NCM:176's `selection-account-only` describes release availability. It is never the carrier of an executed result.
  - **Coordinates.** The execution-input owner joins each of these (EXM:1466-1486):
    - `planId` and `executionPlanId` of the Run;
    - `cellOrdinal`, `programOrdinal`, `capabilityId: clones-near` and `languageMode: syntax-only`;
    - `universe`, the binding's syntax universe as bare 64-hex;
    - `producerClosure`, which must equal the binding's `enumerator.closureId`: the core provider closure (item 14b);
    - `stageOrdinal`, which must equal the binding row's syntax stage (item 14b);
    - the schema constants `authority: candidate-only`, `semanticEquivalenceClaimed: false` and `automaticDeletionEligible: false`.
  - **The census** is the binding's Plan `candidateSourcePaths` (ENC:49). For a syntax-only `clones-near` binding it is the scoped first-party paths under the cell workspace whose suffix selects a syntax dialect-table variant, which are the body-eligible paths (NE:959-970), plus any path an explicit scope names. C4a builds it (**X-C2**, item 14b), and E3 consumes it unchanged.
  - **Groups and bodies.**
    - `groupDigests` are the digests of `CloneCandidateGroupV2` records (NES:3573) with `mode: near`, `evidenceLevel: similar-candidate`, `authority: candidate-only`, `grouping`, `scoreMeaning` and `matchedEdges`. `language` is the body language, never `typescript+javascript` in this mode.
    - Members are opaque body ids: `sb1:` followed by the hex SHA-256 of the canonical `{grammarId, path, startByte, endByte}`. An id is at most 256 characters. It is a producer coordinate, not a subject identity (EXS:1006-1058).
    - `sourceBodies` has one row per id that appears in an emitted group: `{id, path, contentSha256, byteLength, universe}`, where `contentSha256` and `byteLength` are the snapshot file's (EXC:255). No other body is listed.
  - **The result, case by case:**

| Executed result | `state` | `deficiency` / `nativeCause` | `examinedPaths` | `groupDigests` and `sourceBodies` |
|---|---|---|---|---|
| The census is an explicit `[]` | `complete` | null / null | `[]` | `[]`, `[]` |
| Every census path `parsed`; no pair reaches the threshold (a successful empty result) | `complete` | null / null | the census | `[]`, `[]` |
| Every census path `parsed`; groups within the bounds | `complete` | null / null | the census | the groups and their members' bodies |
| Some census paths are `syntax-error` (item 10) | `partial` | `input-closure-incomplete` / **`source-parse-error`** | the `parsed` paths only | groups over bodies of `parsed` paths only |
| Some census paths are `truncated:size`, `:fuel`, `:memory`, `:nodes` or `:depth` (item 11) | `partial` | `budget-exhausted` / null | the `parsed` paths only | as above |
| A group would exceed `maxCandidatesPerGroup` (4,096), or the group count would exceed `maxGroupsPerUniverse` (1,000,000) | `partial` | `budget-exhausted` / null | the examined paths | An over-size group is **withheld whole, never cut**. Groups beyond the count bound, in canonical digest order, are withheld. |
| A census path that no selected code row reads: a data document, an unsupported suffix, or an explicitly named ineligible path | `partial` | `language-tier-unsupported` / `capability-missing` | excludes that path | as above |
| A `backend-fault` in any census file (item 10) | **no envelope** | — | — | The syntax step fails on the `operational-failed` route and nothing is retained. The envelope is never synthesized as `unavailable`, as an empty `complete`, or as `partial`. |

  - **Several conditions in one envelope.** It carries one pair, chosen by NE §10's precedence (NE:3321-3324): `language-tier-unsupported`, then `input-closure-incomplete`, then `budget-exhausted`. This is the same rule as for Coverage (item 10). `examinedPaths` always states exactly what was examined. The pair satisfies `_carrier` (EXM:321-337) against the NES registry rows.
  - **`unavailable` is never emitted** for a selected syntax binding. Every typed unavailability refuses before PlanId (item 5): a missing closure, or a static incompatibility. A backend fault or a cancellation produces no envelope.
  - **Required cells.** A `partial` envelope on a required cell supplies the row's candidate source pair and a `requiredCellDeficiencies` entry. The row is semantically indeterminate, never complete (EXC:72-106; EXM:540-565). A required cell with no envelope refuses `EXECUTION_INPUTS_CANDIDATE_REQUIRED` (EXC:96-106). That happens only after a backend fault, when the Run has already failed.
  - **The cause mirror.** `source-parse-error` must be a member of EXS's `NativeCause` (EXS:201-218), which EXM:851 holds equal to NES's. This is successor **SYN-1F** (item 19). E2s applies it to the product (item 20).
  - **Not `source-syntax-invalid`.** The enumeration-local `source-syntax-invalid` (ENC:120, ENC:147) is a subject-inventory deficiency for manifest parse failure, deliberately kept out of `DeficiencyV2` and `NativeCause`. It cannot appear on a Coverage entry or a candidate envelope, whose `deficiency` is `DeficiencyV2` or null. The two stay distinct.
- **Basis:** EXS:833-1058; EXC:72-106 and EXC:251-263; EXM:321-337, :540-565, :851 and :1465-1555; ENC:49; NCM:176; NE:2571 and NE:2628-2630 (near and cross candidates are candidate-only and mint no `fact2`); NES:3573.
- **Rejected:**
  - **An empty successful envelope over a failed examination.** It conceals the failure.
  - **A Coverage entry for `clones-near`.** It fabricates a relation (NCM:176).
  - **`selection-account-only` as the executed carrier.** That is availability, not execution.
  - **Truncating an over-size group's members.** A cut component misstates the similarity graph.
  - **Body ids built from subject identities.** They are not that authority (EXC:255).
- **Forbidden substitutes:** a near group inside a `fact2`; a `sourceBodies` row for a body in no group; a path outside the census in `sourceBodies` or `examinedPaths`; any envelope after a backend fault.
- **Controls** (E3, with E2c's candidate builder):
  - E3-T8: `clones-near` alone, over a census containing one syntax-error file, gives `partial`, `input-closure-incomplete`, `source-parse-error`. `examinedPaths` excludes the file, no Coverage entry exists, the execution-input owner admits the envelope, and a required row is indeterminate.
  - E3-T9: `clones-near` alone, with each exhausted bound in turn (size, fuel, memory, nodes, depth, group size, group count), gives `partial`/`budget-exhausted`/null, and the withheld-group rule holds.
  - E3-T10: a census naming a data document gives `partial`/`language-tier-unsupported`/`capability-missing`. An explicit `[]` census gives `complete` with three empty arrays.
  - E3-T11: a backend fault during a `clones-near` pass gives no envelope and an operational step failure, and no Run is committed.
  - E3-T12: a successful empty result gives `complete` with `groupDigests: []` and `examinedPaths` equal to the census.

**14b. Producer and stage coordinates of syntax-universe work.**
- **Decision.**
  - **The producer is the core.** Every syntax-universe record names the **core provider closure** in its producer field:
    - `subject-scope.enumeratorClosure`;
    - `view.producerClosure`, and so `fact.producerClosure` (IDS `equalToDirect`);
    - `stage-spec.producerClosure`;
    - the enumeration binding's `enumerator.closureId` (ENS:265, "a selected provider closure");
    - `CandidateProducerResultV1.producerClosure`.

    The core provider closure is `closure2:` + H("closure", D″), where D″ is the authenticated core inventory's selected-platform descriptor with `kind` set to `provider`. That is exactly C item 9's "core import-producer closure" (C:409-411): the same D and the same kind, so the same identity. The code that produces syntax candidates (`crates/syntax`, `host/syntax.rs` and the engine) ships in the core. The grammar closure is joined through the context (NE:223-232) and is never a producer; it stays kind `grammar` (IDS:4743).
  - **One stage per syntax universe.** C4a's execution plan has one stage per selected syntax universe, whose `producerClosure` is the core provider closure. Every syntax-only binding of that universe names that stage as its `stageOrdinal`. E3 executes the stage in the host and returns its outputs to the host capture: the syntax views, with facts and Coverage admitted by H, as the stage's `outputRefs`; and the candidate envelope as a host-derived ref (EXC:259).
  - **X-C1, an obligation on C and CRC-1.** C r3 restricts the core import-producer closure to `import.producerClosure` and forbids it in `plan.semanticClosures` (C:409-411; control C2-T13, C:435). E needs a second admitted use. C's next revision, and CRC-1, must:
    - admit the core provider closure in the producer fields above, **only** where the record's universe (or the stage's or binding's universe) is a `native.semantic-universe.syntax.v2` identity;
    - make it a `plan.semanticClosures` member (IDS:4794-4803) **exactly when** the Plan selects a syntax universe;
    - narrow C2-T13: a core provider projection in `semanticClosures` without a selected syntax universe refuses, and so does its use in any producer field of a TypeScript or Rust record.
  - **X-C2, an obligation on C4a:** item 14a's census rule.
- **Basis:** IDS:4726-4743 (producer fields are kind `provider`); IDS:4794-4803 (direct membership); ENS:265; EXM:1483-1486 (the envelope's `producerClosure` equals the binding's enumerator closure, and its `stageOrdinal` equals the row's); C item 9 (C:392-411), the in-core role pattern; BP:676-683 (the syntax pass is host code).
- **Rejected:**
  - **The grammar closure, re-kinded `provider`, as the producer.** C item 7 fixes the kind by role (C:282-302), and under T-native the grammar closure executes nothing.
  - **A distinct core "syntax-producer" projection.** The same descriptor with the same kind is the same `closure2`. A second name for one identity is a distinction no admission can see.
  - **A null producer.** The producer fields are required and kinded (IDS:4726-4743).
  - **A provider component for syntax.** CH14:614 and BP:676-679 rule it out (item 17).
- **Forbidden substitutes:** the TS or Rust provider's closure on a syntax record; the core provider closure on a TS or Rust record; a syntax stage with no execution-plan stage spec.
- **Controls** (E3, after X-C1 is accepted):
  - E3-T13: every syntax-universe view, scope, stage spec, binding and envelope names the core provider closure, and the Plan's `semanticClosures` contains it exactly when a syntax universe is selected.
  - E3-T14: the same closure on a TypeScript view refuses, under C's narrowed C2-T13.

**15. Grammar selection and the universe.**
- **Decision.**
  - **Every row.** A syntax universe selects **every grammar row of the admitted bundle** (`selectedGrammarIds` = all eight). Its identity therefore depends only on the bundle, never on which file types a repository contains.
  - **Where it arises.** A syntax universe arises only where the Plan binds one before PlanId: U-9's fallback unit (NE:879-905; B:411, B:674), or an explicitly requested `syntax-only` cell.
  - **Who binds it.** E3 mints the context through C2a's generic admission (C:403, "Syntax") and binds the universe with the evaluator's existing owner (`crates/evaluator/src/native_universe.rs:85`).
- **Basis:** NE:233-240 ("Selecting a different set is a different universe"); NE:443-445; NES:2425.
- **Rejected:**
  - **Selecting only the rows whose suffixes occur in the snapshot.** Adding one `.yaml` file would change the universe and every syntax `fact2` in the repository.
  - **A configurable selection.** No Config2 key exists, and inventing one is out of this law's scope.
- **Forbidden substitutes:** a universe minted after PlanId; a selection that varies with the snapshot.
- **Controls:** E3-T5: two snapshots of one repository, differing only by an added `.yml` file, give the same syntax universe ID.

**16. Never a substitute for a semantic rung (DR-G25).**
- **Decision.** The syntax pass never runs because a TS or Rust provider failed, was unavailable, or lacked a rung. Five structural reasons hold this:
  1. **Universes are fixed before dispatch.** `plan2` binds every universe before PlanId, so a post-failure syntax universe would need a new Plan.
  2. **Facts discharge only their own scope.** Matching is on relation, rung and both universes (NE:366-385), so a syntax fact never pays a TS or Rust obligation.
  3. **Distinct dialects.** The `{grammarVariant}` branch prevents any identity collision (NE:241-252).
  4. **No resolution claim.** The syntax universe is `resolutionAttempted=false`, and its semantic rungs are `language-tier-unsupported` (NE:253-259).
  5. **No in-process fallback** (L:132).

  A missing TS or Rust rung is that universe's own typed Coverage, and a required one makes the Run indeterminate (REG:370; AQP:115).
- **Basis:** REG:370 ("silent syntax fallback fails"); BP:695-696; AQP:114-115; L:132.
- **Rejected:** a "degraded mode" offering syntax facts when a provider is down. That is the failure DR-G25 names.
- **Forbidden substitutes:** any code path from a provider outcome to `host/syntax.rs`; a syntax fact in a TS-universe view answering a TS requirement.
- **Controls:**
  - E3-T6: a TS-unit fixture whose provider is unavailable gives a Run with no syntax universe, and the required semantic Coverage is `unknown`/`provider-unavailable`.
  - E3-T7: a source pin shows that `syntax.rs` has no caller in the provider-outcome path.
  - The existing Run-closure guard refuses a syntax fact offered against a TS scope.

---

## E. Security

**17. Threat model and placement.**
- **Decision.**
  - **The threat.** A repository's bytes are attacker-controlled. Untrusted pull requests in CI are the case M3P:486 names. The host holds the store, the trust state and the user's filesystem authority. The parser reads those bytes before any finding exists.
  - **Placement.** **The syntax pass runs in the host, as a pure crate, not as a component** (BP:676-683), with the parser behind T-wasm's memory boundary:
    - a defect in the parser's C, including its external scanners, can corrupt only that file's linear memory;
    - a trap is an error, not a crash;
    - fuel and the page ceiling bound CPU and memory deterministically;
    - zero imports means no system call is reachable;
    - the host validates every output before use.

    **Given a correct engine and output validator, a compromised parse can at most misdescribe the attacker's own file.** It cannot reach other files, the store or the host. That condition is the declared TCB: `wasmi` and the host validator (item 18). The isolation claim is only as strong as they are (E-N4).
  - **What this is not.** It is **not a sandbox claim**, not an untrusted-component admission, and not a confinement claim.
    - AQ:344 ("No process/WASM boundary is claimed as a sandbox"), SL:497, SL:1113, NE:2554 and REG:366 stand unchanged.
    - DR-128 stays closed (REG:317).
    - No user-facing text says "sandboxed".
    - The modules are first-party artifacts built from pinned sources in a signed first-party closure.
- **Basis:** M3P:476-487 (O7's direction); BP:676-683; REG:366 (DR-G21); AQ:344 and AQ:347; CH14:614 ("selects no new provider protocol").
- **Rejected:** **C-worker**, a confined syntax component, at M3.
  - It contradicts BP:676-679 and CH14:614. It needs a process, a wire format and producer-boundary admission, which together amount to a new protocol.
  - It depends on O7 (pending), D1's primitive and CF-P's macOS outcome (M3P:501, M3P:526).
  - Where confinement is unavailable (O7 item 3), a same-user child still gives address-space, crash and resource-accounting separation, but not filesystem or store authority separation (E-N3). T-wasm gives the first two inside the host, and its fuel and page bounds stand in for the third.
  - It adds a spawn per universe.
  - T-wasm gives memory isolation on all four platforms with no O7 dependency.
  - It may be reconsidered at M4 or M5 if E0 fails **and** O7's confinement is universal.
- **Forbidden substitutes:**
  - describing the boundary as a sandbox;
  - any import added to a module "for diagnostics";
  - a host function exposed to a module, which is an import by another name;
  - reading a module from anywhere but the admitted closure.
- **Controls:**
  - E2-T1 (zero imports) and E2-T5 (trap survival), both E extensions beyond DR-G21's external-component scope (REG:366).
  - E2-T23, a hostile-input corpus: deeply nested brackets, 4 MiB of one token, invalid UTF-8, NUL bytes, unterminated strings and comments, and pathological error recovery. Every case ends in one of item 10's typed outcomes, never a crash.
  - This law asks D5 and O3 (M3P:213, M3P:223) to add the syntax pass to the G21 control set.

**18. Residual risk, the fallback posture, and O7.**
- **Decision.**
  - **Under T-wasm, residual risk lies in:**
    - `wasmi`'s own unsafe code, executing trusted module code over attacker data. SYN-DEP's `unsafeAccounting` records it, as the identity policy does for its dependencies (`tools/identity/dependency-policy.json:1628-1632`).
    - The integrity of the attacker's own file's facts.
    - Denial of service, bounded by item 11.
  - **Under T-native (if E0 fails), residual risk is code execution in the host from a parser defect.** Possible host crashes and the weaker bounds of item 11 remain **declared residual risks, not guaranteed typed returns** (E-N4). The posture is then:
    - item 11's bounds, plus a fresh parser per file;
    - parsing on a dedicated thread with a fixed stack;
    - E2-T23 as a regression corpus;
    - the deployment guidance O7 item 3 already proposes, containers for untrusted pull requests (M3P:486), which applies to the host as a whole;
    - an M4 entry condition, recorded in M3P-E (item 19): before CLI `analyze` accepts untrusted input at M4 (BP:887), the lead re-decides placement with E0's data and O7's outcome.
  - **Interplay with O7.** E needs no O7 outcome. If the owner adopts O7's items 2 to 4, providers become confined and the syntax pass keeps its own memory boundary. No item here relaxes, pre-empts or depends on O7.
  - **Exposure scope.** At M3 the parser sees only harness inputs: public pinned T2 and owner-consented T3 (M3P:222; AQP:500). That bounds **who supplies the bytes**. It does not prove them benign (E-N4). The wider exposure, arbitrary repositories and untrusted pull requests, begins with M4's CLI.
- **Basis:** M3P:476-487, M3P:526; BP:887; REG:317.
- **Rejected:** claiming that T-wasm makes untrusted pull requests safe to analyze without a container (AQ:344); silently shipping T-native without an M4 re-decision.
- **Forbidden substitutes:** a residual-risk statement omitted from SYN-DEP; a confinement claim of any kind.
- **Controls:** SYN-DEP review; the M3P-E record row.

---

## F. Successors and units

**19. Successors.**

| ID | What | Kind and review | Owner | Needed before |
|---|---|---|---|---|
| **SYN-1** | **Native contract successor** (NE §1.2 and §10, NES, NEM, and the native-owned mirrors):<br>(a) `NativeCause` member `source-parse-error`, lawful only under `input-closure-incomplete`, with the NES:31 `allowedCauses` row and the NE §10 table row;<br>(b) the per-file outcome law for Coverage (items 10 and 11) and for `clones-near` envelopes (item 14a);<br>(c) the data-document "format definition, no parse" sentence (item 8);<br>(d) the route row. NE:3530's pre-Plan route gains every `native.syntax-grammar-*` and `native.syntax-normalizer-*` key. The existing keys (NEM:2426-2478, NE:227-246) are absent from that row today, a record gap found here. Item 5's chain adds `-bundle-manifest-mismatch`, `-definition-mismatch`, `-execution-model-mismatch`, `-engine-mismatch`, `-module-invalid`, `-module-import-forbidden`, `-module-exports-mismatch`, `-abi-mismatch`, `-symbol-table-mismatch`, `-bundle-not-the-registry`, `-build-mismatch` (T-native only) and `native.syntax-normalizer-kind-unknown`;<br>(e) the `backend-fault` route (item 10), with the D9 owner's assent;<br>(f) the native-owned `NativeCause` copies in `native/provider-startup.schemas.v1.json` (:83, :610). | contract successor; **ACCEPT-DESIGN-UNIT** | native owner (DR-G13 and G25 owners) | E2s; E2b (keys) |
| **SYN-1F** | **Foundation successor, joined with SYN-1** (E-R1). `source-parse-error` enters every foundation `NativeCause` copy:<br>- `execution-inputs.schema.v1.json` (EXS:201-218), which EXM:851 holds equal to NES;<br>- `identity-schemas.v3.json` (:3491);<br>- `subject-inventory.schema.v1.json` (:461);<br>- `enumeration-plan.schema.v1.json` (:260);<br>- `evaluator-projection-registry.v1.json` (:1160).<br>It also states that EXC §6 and EXM's candidate derivation (EXM:540-565, :1465-1555) apply unchanged to item 14a's syntax-only envelope, with the producer of item 14b. No new state, field or refusal code. | contract successor; **ACCEPT-DESIGN-UNIT**; reviewed beside SYN-1, both accepted before E2s | identity and execution-input owner | E2s |
| **X-C1** | **Obligation on C (and CRC-1):** the core provider closure as the producer and enumerator closure of syntax-universe work, a `semanticClosures` member exactly when a syntax universe is selected, and C2-T13 narrowed (item 14b) | C's next revision and CRC-1; ACCEPT-DESIGN-UNIT there | C's owners; identity (CRC-1) | E3 (and E2b's producer fixtures) |
| **X-C2** | **Obligation on C4a:** the syntax-only `clones-near` census (item 14a) | C's next revision; C4a code | C's owners | E3's envelope tests use fixture Plans built to it; C4a's acceptance carries the Plan leg |
| **SYN-NS** | `normalizer.v1.json`, the specification map and the L0–L3 level specifications, plus `near-v1`, as identity-bearing bytes (items 13 and 14) | design unit; **ACCEPT-DESIGN-UNIT**, reviewed with E2c | native and identity | E2c freezes its fixtures |
| **SYN-REG** | the identity-owned registry file, the evaluator re-pointed to it, and the drift-check tool (item 7) | inventory unit inside E2b; **ACCEPT-UNIT** with `inventoryCandidateAssessment` | identity, evaluator | E2b |
| **SYN-DEP** | `tools/syntax/dependency-policy.json`, after the shape of `tools/contracts/dependency-policy.json` and `tools/identity/dependency-policy.json`: exact crates, checksums, resolved features, licences, `unsafeAccounting`, residual risk (item 18), and its checker | inventory unit inside E2b; **ACCEPT-UNIT** | product | E2b |
| **SYN-LANE** | the grammar closure lane:<br>- the toolchain pin, entered in the dev-environment pins;<br>- the upstream pins;<br>- `tools/grammar/` (build, records, receipt);<br>- the reproducibility check;<br>- labelled fixture modules for development tests (BP:664-672 allows "labelled fixture assets"), with digests in the receipt. Release builds and signs at M6. | inventory unit, E2a; **ACCEPT-UNIT** | product, release | E2a |
| **CR-1** | the component-manifest role `grammar` mapping to kind `grammar` (C item 7) | C's contract successor | security, DR-103 | E2b's real admission (synthetic fixtures need it too) |
| **LP-1** | a product-wide third-party licence allowlist and notice inventory, for host binary notices and closure notices (F02:98). **Lead decision for E's rows now:** only MIT, Apache-2.0 and BSD/ISC/Zlib-family licences, and Apache-2.0 WITH LLVM-exception for build-only tools; every notice ships. | record or successor, recommended | lead; owner FYI | M4 distribution (not E) |
| **M3P-E** | planning record: E's units become E0, E2a, E2s, E2b, E2c and E3 (item 20); the second-integrator rule for E3's joins; X-C1 and X-C2 as cross-law items; and item 18's M4 entry condition | planning record | lead | — |
| **CH14-E** | CH14:614's gap closed by this law; `tools/grammar/` and `tools/syntax/` rows | record correction at the next CH14 refresh | — | — |
| **PY-REG** (not M3) | the Python registry successor template: the NES `languageId` enum and registry row; `bundledGrammars` and U-4's list (`.py` and `.pyi` moving from `unsupported-file` to `grammar-only`, which changes Plans and is disclosed); IDS `body-language-version.languageId`, the `grammarVariant` enum, the dialect table and `bodyLanguageByVariant`; a Python row in NE §6.3; NCM notes and COV fixture coordinates; a new module ([U] `tree-sitter-python` MIT) and normalizer tables; **no change to `grammar.rs` or `parser.rs`** | registry successor (BP:696-697; AQP:462) | after D9 (AQP:465) | — |

**20. Units.**

| Unit | Scope | Integration edges | Built against (accepted interfaces) | Review | Size | Days |
|---|---|---|---|---|---|---|
| **E0** | the probe (item 3); `E0-REPORT.md` | — (T2a fetched; network for the pinned sources and toolchain) | — | record; lead decision | S | 2 |
| **E2a** | SYN-LANE: the closure layout (item 4), manifest and definition records (items 5 and 6), `SymbolTableV1` digests, fixture modules and the receipt | E0, P0 | — | ACCEPT-UNIT | M | 2 |
| **E2s** | applies SYN-1 and SYN-1F to the product, all in one candidate:<br>- the schema sources `native-v2`, `execution-inputs-v1`, `identity-v3`, `subject-inventory-v1`, `enumeration-plan-v1` and `startup-v1` (under `schemas/sources/`);<br>- the evaluator registries `coverage-registry.json`, `execution-registry.json`, `atom-registry.json` and `enumeration-registry.json`;<br>- the regenerated carriers `crates/contracts/src/generated/{evidence,identity,protocol}.rs`, `apps/report/src/generated/report.ts` and `providers/typescript/src/generated/protocol.ts`, byte for byte under the closed generation registry (BP:722-765);<br>- the design-lock successor binding. | SYN-1 and SYN-1F accepted | — | ACCEPT-UNIT | M | 2 |
| **E2b** | `grammar.rs` (items 4 to 7, A3–A8 and A12), `parser.rs` (the engine, A9–A11, bounds, validation and outcomes; items 2, 10 and 11), SYN-REG, SYN-DEP, `grammar_tests.rs` | E2a; C2a (closure admission and the synthetic signer, C items 7 and 8; C:933) | CR-1; SYN-1's keys | ACCEPT-UNIT | L | 3 |
| **E2c** | `normalization.rs` and `candidates.rs` (items 13, 14 and 14a's envelope builder), SYN-NS, `normalization_tests.rs` | E2b | SYN-NS, accepted before its fixtures freeze | ACCEPT-UNIT + SYN-NS | L | 3 |
| **E3** | `crates/host/src/syntax.rs` (CH14:496):<br>- context minting through C2a, running item 5's chain;<br>- universe binding with every row selected (item 15);<br>- the syntax stage of item 14b;<br>- dispatch over C1a's custody bytes only (C:93, "No second read");<br>- outcomes to Coverage inputs (item 10) and to the `clones-near` envelope (item 14a);<br>- U-9 consumption;<br>- the DR-G25 controls (item 16) | E2c, C1a, B2-c, E2s | **the H law's syntax-join interface** (accepted before day 0, M3P:261); the C law's Plan, binding and census records (X-C1, X-C2); the existing execution-input owner (`crates/evaluator/src/execution_inputs.rs`) | ACCEPT-UNIT | M | 2 |

- **The H join (E-R3).** E3's integration edges are E2c, C1a, B2-c and E2s. **It does not wait for integrated H.** It is built and tested against the **accepted H law's** syntax-join interface, which M3P:261 assumes before day 0, as M3P r6's E row already lists (M3P:214, M3P:303).
- **The second-integrator rule.** For each join E3 shares with a later unit, **the final wiring and its end-to-end controls belong to whichever unit integrates second, and that join is inside that unit's acceptance scope.** Under M3P r6:
  - **H** integrates on day 22 (M3P:309), after E3's day 14. H's acceptance therefore covers the syntax views, facts and Coverage entering `fact_admission.rs`, with the end-to-end legs of E3-T3 and of E3-T6 (the Coverage leg). H's row already owns "the syntax … joins" (M3P:218), so its 3 days are unchanged.
  - **C4a** integrates on day 19 (M3P:296). Its acceptance carries the Plan legs of X-C1 and X-C2: E3-T13's `semanticClosures` leg, E3-T14, and the census of E3-T8 to E3-T12.
  - **J2** integrates on day 25 (M3P:311). Its acceptance carries the host capture of the syntax stage's receipt and the candidate envelope into `ExecutionInputsV1`, and the Run-level legs of E3-T6 and E3-T11.
  - **E3's own acceptance** covers everything up to those interfaces:
    - the context chain and refusals (E3-T1);
    - routing (E3-T2);
    - the outcome-to-Coverage inputs (E3-T3's unit leg);
    - cells (E3-T4);
    - selection (E3-T5);
    - the source pin (E3-T7);
    - envelope construction for every row of item 14a's table (E3-T8 to E3-T12), with admission by the existing execution-input owner over fixture execution inputs;
    - producer naming on bindings, stages and envelopes (E3-T13's unit leg).
  - If the order changes, so that H integrates before E3, E3 carries the H legs instead. The rule is about integration order, not about unit names.
- **Inventory numbers** are assigned at launch, and `git ls-files` is checked first (the parallel-numbering lesson). E2a and E2b may be one candidate if launched together. E2s is its own candidate, because it touches the contract-generation lane.
- **Under T-native,** E2a shrinks to the definition records over the crate archives, and E2b uses the `tree-sitter` crates. The units do not change.
- **DAG effect, against M3P r6's table (M3P:284-320):**
  - E0 → E2a finish before day 0 (M3P:302). E2s finishes before day 0, once SYN-1 and SYN-1F are accepted with E's law. At the latest it must finish by day 12, E3's start.
  - E2b runs from day 2, after C2a (M3P:290), to day 5.
  - E2c runs from 5 to 8.
  - E3 runs from 12 to 14, after C1a (12, M3P:291) and B2-c (10, M3P:288). **This is M3P:303's day 14.**
  - M3-M starts on day 28 (M3P:319), so **E3 keeps 14 days of slack (M3P:342)**.
  - Neither H (22) nor J2 (25) moves. M3P:309 integrates H after C4a and F1, using the "E3 or F1" alternative of H's row (M3P:218), and J2's edges (M3P:311) name neither E3 nor E2s.
  - **M3P r6's figures are preserved:** the 33-day conditional host chain (M3P:322-332); K2 by day 28 (M3P:329); O2_selected by day 31 (M3P:331); and X12d's X9 lead set by day 22 (M3P:332).

---

## G. Consistency with accepted and drafted laws

- **AQP (r6).**
  - Syntax-only cells are one T1 lane per grammar (M3P:221; item 12).
  - The determinism suite covers outcomes (AQP:324-327; item 10).
  - Python stays an AQP:465 decision. This law only keeps the registry language-neutral (items 7 and 19, PY-REG).
  - O3's missing bounds are supplied for the syntax pass only (item 11).
- **B (r2, accepted).**
  - U-9 is unchanged and hands the syntax fallback exactly where NE:879-905 says (B:411, B:674).
  - E3 consumes B2-c's fallback unit and membership rows.
  - **Cross-law note:** B2-c's U-4 suffix table reads the identity registry file (item 7). B item 14 does not name the table's source, so this adds no conflict.
- **C (r3, draft).**
  - Snapshot bytes are the only input. E3 reads C1a's custody, never the project (C:93, C:114).
  - The grammar closure is admitted by C2's single path, with role `grammar` mapped to kind `grammar` (CR-1).
  - C item 8 assigns `native.context.syntax.v2` to E (C:403).
  - **Two cross-law obligations (item 14b).**
    - **X-C1** amends C item 9 and C2-T13: the core provider closure gains its syntax-universe producer use.
    - **X-C2** gives C4a the `clones-near` census.

    Neither changes C's host chain. C4a's acceptance carries their Plan legs (item 20).
- **The execution-input owner** (EXC, EXS, EXM; product `crates/evaluator/src/execution_inputs.rs`). It is unchanged except for SYN-1F's enum mirror. Item 14a uses its existing envelope, binding, census, carrier and derivation rules as they stand.
- **L (r1, draft).**
  - Syntax is **in the host**, not a provider. L's one-child-per-universe rules do not apply to it.
  - Its "no in-process fallback" (L:132) is item 16's fifth reason.
  - L item 3's "no producer cache at M3" holds: no parse result crosses invocations.
- **M3P (r6, accepted).**
  - The E row (M3P:214) is honored: BP:684-688 by items 4 to 7, NE:260-263 by item 8, NE:2's syntax part by items 9 to 16 and 14a, and NE:7 by items 14 and 14a.
  - E3's day 14 and 14 days of slack (M3P:303, M3P:342) stand. The 33-day host chain and the K2, O2_selected and lead-set conditions (M3P:322-332) are unchanged. M3P-E adds E2s and the second-integrator rule.
  - M3P-r4:299's lean toward tree-sitter is kept. Its acceptance of a C runtime in the host TCB is narrowed: kept only as the fallback.
- **The product.**
  - The evaluator's syntax owners stay the single implementation of the NE §1.2 joins (`native_context.rs:276-361`, `native_universe.rs:85`, `capability_support.rs:77-222`). E adds execution joins only (item 7).
  - The generated `Native2SyntaxGrammarBundleV1` carrier (`crates/contracts/src/generated/evidence.rs:32984`) is the descriptor type E2b uses.

## Owner notes (FYI; none blocking)

1. **A new pinned build toolchain** (wasm `clang`, through wasi-sdk) enters the dev environment with SYN-LANE, beside the existing pinned tools. It is build-only and never run at analysis time.
2. **The product has no third-party licence allowlist yet.** LP-1 records the lead's interim rule for E and recommends a product-wide one before M4 distribution.
3. **If E0 fails,** the C parser joins the host TCB as BP:680-682 already allows, and item 18's M4 re-decision applies before CLI `analyze` takes untrusted input.
4. **X-C1 widens one of C's in-core role closures.** The core provider closure, which C r3 confines to the in-core importer, also becomes the producer of syntax-universe work, and a `semanticClosures` member whenever a syntax universe is selected. It is the same identity, because it is the same core. Every core release is therefore a new syntax producer, as it is already a new detector (C item 9).

## Questions for the reviewer

- **R-1.** Is the core provider closure (item 14b, X-C1) the right producer identity for in-host syntax-universe work, given C item 9's in-core role pattern and IDS:4726-4803?
- **R-2.** Is item 14a's table complete for every executed state of a syntax-only `clones-near` binding? Is the census rule (X-C2) the right reading of ENC:49 for syntax-only?
- **R-3.** Is item 5's chain (A1 to A12) complete, including the T-native equivalent? Is `SymbolTableV1` a sufficient canonical form?
- **R-4.** Is the second-integrator assignment in item 20 (H, C4a and J2) sound and consistent with M3P r6?
- **R-5.** Is SYN-1F's list of foundation `NativeCause` copies complete, together with E2s's list of product copies?

r1's questions R-1 to R-4 were answered in Codex's r1 assessment table.

## Not claimed

- No probe, build, parse or measurement was run for this law. Every [U] fact is public metadata as read on 2026-10-04, not a pin.
- No contract, schema, register row, gate or threshold changes here. SYN-1, SYN-1F and SYN-NS carry the changes, under their own reviews.
- No change to C is made here. X-C1 and X-C2 are obligations for C's next revision.
- No sandbox, confinement or untrusted-input safety is claimed (AQ:344).
- No Python support is decided (AQP:465).
- No data-format syntax capability is added (NE:300-302).
- No cross-platform qualification is claimed. M3-X claims only this host's family (M3P:474).
- The upstream size figures are from upstream HEAD, not the eventual pins.
