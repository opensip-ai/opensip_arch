The audit is finished and written to `/tmp/opensip-implementation/m1-pure-dependency-review-01/` as `audit.json` and `audit.md`, with raw evidence and a sha256 manifest. The planned serde 1.0.229 (derive) plus serde_json 1.0.151 (default) dependencies hold up, but six findings need a root decision before approval. I did not approve the dependencies and made no M1, registry or release claim.

**Integrity and pinning:**
- **Hashes:** all 11 downloaded crate archives match their lock checksums, and each unpacked archive is identical to the registry source I reviewed.
- **Lock:** it has 11 entries, all from crates.io, and was unchanged after running cargo on the copy.
- **Linked into contracts:** serde, serde_core, serde_json, itoa, memchr and zmij.
- **Compile-time only on the build machine:** serde_derive, proc-macro2, quote, syn 3.0.5 and unicode-ident.
- **Features:** match the plan. serde_json has only default/std, with preserve_order, arbitrary_precision, unbounded_depth, raw_value and float_roundtrip all off, so its maps are sorted BTreeMaps. No crate declares `links` and none have build-dependencies.
- **Lock oddity:** two edges in the lock (`serde_json→serde`, `serde_core→serde_derive`) are gated on `cfg(any())`, which is never true. They only tie versions together and are never compiled.

**Generated carriers (about 58k lines):** no unsafe code, no FFI, and no use of files, network, processes, environment, threads, clocks or randomness. They use no HashMap/HashSet and have no float fields. Dependency features they don't call, such as serde_json's reader/writer helpers and serde_core's impls for network addresses, SystemTime, Path and generic HashMap, are recorded as unused.

**Accepted findings:**
- **PD-01 to PD-03:** integrity, exact closure and features, and inert carriers all verify.
- **PD-04 (unused effect-capable APIs):** accepted, but should be recorded so later use gets reviewed.
- **PD-11 (input size):** accepted with a note. serde_json limits nesting to 128 levels but not input size, so callers must bound input bytes.

**Findings that need a root decision:**
- **PD-05, CPU detection:** serde_json turns on memchr's `std` feature. On x86_64 without compile-time AVX2, memchr then checks for AVX2 at runtime and caches the choice in a global. Results don't change. On this arm64 host the choice is made at compile time. I recommend accepting it under TCB-SCOPE-01 and recording it.
- **PD-06, unsafe code:** unsafe Rust is linked in from memchr (SIMD), zmij (including 5 inline `asm!` hints whose body is only a comment), itoa, serde_json and serde/serde_core. There is no FFI. It needs explicit acceptance as trusted code; I did not review its soundness.
- **PD-07, build-time effects:** six build scripts run `rustc --version`. proc-macro2 also runs rustc test compiles that follow `RUSTC_WRAPPER` and `RUSTFLAGS`. serde and serde_core write `OUT_DIR/private.rs`. The proc macro runs unsandboxed inside rustc. None touch the network. The build lane should record toolchain, target, profile, wrappers and RUSTFLAGS.
- **PD-08, workspace features:** in a shared workspace, Cargo merges features across member crates. Another crate enabling serde_json `preserve_order` or similar would change contracts, so resolved features must be checked against each real workspace lock.
- **PD-09, enforcement:** automated checks are needed for the dependency and feature allowlist, a source scan for effects, HashMap and unsafe, and generated-code drift.
- **PD-10, trial binaries:** `main.rs` and `bin/carrier_probe.rs` read files from absolute paths. They are test harnesses and must not ship as production contracts targets.

The generator's separate lock (typify, schemars, syn 2.0.119 and others) is recorded but was not reviewed.

**Limits:**
- **No builds or tests:** I didn't build or run Rust. The build-script outputs I cite come from an earlier build of a byte-identical manifest and lock, and the roundtrip results are from that earlier trial.
- **No safety tooling:** no soundness review of unsafe code, no miri, no sanitizers.
- **Other targets:** x86_64 behaviour comes from reading source, not building.
- **No online checks:** no network checks of index, yank state, RustSec advisories or licenses.
- **Scope of scans:** the source scans are evidence, not proof that effects are absent.
- **Production locks:** no production workspace lock exists yet to check.
