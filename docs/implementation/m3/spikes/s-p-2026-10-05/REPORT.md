# S-P: compiler-host feasibility, preliminary

The Rust callback mechanism and the TypeScript compiler API work on this macOS host with a coherent retained prototype toolchain. The existing minimal Homebrew Rust pin cannot host the prototype unchanged. The successful Rust probe uses a complete official Rust 1.95.0 distribution with its matching stdlib and rustc-dev components, and RUSTC_BOOTSTRAP=1 only while compiling the trusted probe wrapper. The override is absent when that wrapper analyzes source. Production toolchain selection and packaging are not decided by this record.

This is S-P feasibility, not S-M, a performance result, confinement validation or qualification. No build script, proc-macro, package script or other repository code executes. No T1 producer or Rust T1 compilation runs. Neither owner D13 nor O7 is treated as approved.

## Pinned inputs and acquisition

The public T2 manifest is the accepted original documentary bytes: c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578, 322483 bytes. Explicit acquisition used the bound K1a corpus command. Both development-role stores were re-verified offline against their QD-22 and content digests before inspection. No held-out source was inspected and no corpus source is copied into either repository.

The selected inputs are http-body/src/size_hint.rs from rs-small-http-body at commit 929ff1c456c6cfe7a984e8d4bd70f506cbd9c78c, and src/metadata.ts from ts-small-constructs at commit 8264e196c3593a192dc79991f4d97c22ab4c08bf. Their exact byte pins, both tree/content pins, and admission receipts are in report.json and evidence/. Rust analyzes that unmodified standalone module as a library and stops at the after-analysis callback. TypeScript creates a Program over its unmodified selected module with no emission. Neither observation establishes whole-repository analysis or completeness.

Compiler and runtime acquisition is separate from all runs. Official Rust channel/component SHA256 values matched downloaded compiler, stdlib and dev archives. Official Node 24.21.0's archive SHA256 matched SHASUMS256.txt. TypeScript 6.0.3's archive matched the registry's SHA512 integrity field and is retained by SHA256. It is the explicitly pinned JavaScript Program-API prototype. TypeScript 7.0.2 was also acquired during metadata exploration but never executed or selected; its cached archive is not the tested compiler. Evidence records the exact archives and URLs. These are prototype file trees, not admitted signed product closures.

## Results

The installed Homebrew Rust 1.95.0 reports commit 59807616e1fa2540724bfbac14d7976d7e4a3860 and LLVM 22.1.3. Import of rustc_driver fails E0463; without the private-feature override it also fails E0554. The minimal providers/rust/rust-toolchain.toml pin lacks dev components.

The coherent official Rust 1.95.0 compiler, stdlib and dev components report the same commit and LLVM 22.1.2. With the matching distribution, the wrapper compiles without warnings after setting SDKROOT to the recorded macOS SDK. It reaches after_expansion and after_analysis on its own positive control and on the exact public http-body module. A deliberate type error gives E0308, exits 101, and never reaches after_analysis. That exit is the prototype's raw fatal-error behavior, not a product outcome mapping.

A separate owned-lane test attempts to build the same wrapper using the pinned Homebrew compiler with the official stdlib/dev metadata. It fails E0514. Matching semantic version and commit are insufficient to mix those builds. G2 must retain one coherent compiler/dev/LLVM/stdlib/driver distribution and its byte identities; it must not substitute components based only on version strings.

Node 24.21.0 loads TypeScript 6.0.3 by absolute retained path. createProgram and semantic diagnostics work. The public constructs metadata module has zero diagnostics. A deliberate string-to-number type error yields TS2322 and exit 1. Source files and read paths are retained in the logs. No repository TypeScript is required or evaluated as JavaScript.

## Run ordering and boundaries

The complete verified set and the separate mixed-build control each acquired the Darwin opensip-lanes.lock directory, checked for active cargo processes, held the owned directory for their entire set and removed only that owned directory. Evidence records start/end times and no active build before each set. All compiler and runtime invocations were nice 10. No Cargo ran. Private TMPDIR directories were mode 0700; HOME was not assigned. OpenSIP application state remained absent. No private 413 UUID fixture was read.

Earlier unaccepted sub-probes established packaging needs; only the checked owned-lane sets support the report's ordering claim. They run no measured performance statistic, so no median, memory, liveness or S-M placeholder is filled.

## Consequence

Feasibility is demonstrated for the retained coherent prototype, with an explicit component/build-setting requirement. G2 authoring can use that demonstrated API shape and must specify matching build/runtime packaging in its own review. This report does not accept or integrate G2, alter the production Rust pin, validate the supervisor or O7, release L's S-M/D13 gate, or qualify any language cell. All original owner and O1-a law gaps remain.
