# m1-pure-dependency-review-01: pure contracts external dependency audit

Date 2026-09-14 · Toolchain rustc/cargo 1.95.0 (Homebrew), host darwin arm64 · Scope TCB-SCOPE-01
(native/builtin context trusted; no in-process sandbox claim).

**What this covers.** The planned production dependencies of the proposed inert `opensip-contracts` crate:
`serde =1.0.229` with `derive`, and `serde_json =1.0.151` with default features. It checks them against the
frozen trial consumer `m1-eight-output-subject-01/compile-rust` (manifest sha256 `35171720…74d6`, lock sha256
`c7b72548…fb3`) and the generated carriers in `output-b/crates/contracts/src/generated`.

**What this does not cover.** It grants no production dependency approval, which stays with the main root.
It makes no M1-completion, registry, build-lane or release claim. It does not re-review `sha2-const-stable 0.1.0`
or the architecture, and it does not review the soundness of unsafe code.

Machine-readable record: `audit.json`. Raw evidence: `evidence-*`, `input-copy/`, `extracted/`, `evidence-sha256.txt`.

## 1. Exact pinned closure (lock v4, 11 packages)

| Package | Version | Lock checksum = archive sha256 | Archive = registry src | Role | Resolved features | build.rs |
|---|---|---|---|---|---|---|
| serde | 1.0.229 | ✔ `4148590a…e0ba` | ✔ | runtime | default, derive, serde_derive, std | yes |
| serde_core | 1.0.229 | ✔ `67dca2c9…2a48` | ✔ | runtime | result, std | yes |
| serde_json | 1.0.151 | ✔ `c841b55e…3f14` | ✔ | runtime | default, std | yes |
| itoa | 1.0.18 | ✔ `8f42a60c…5682` | ✔ | runtime | — | no |
| memchr | 2.8.3 | ✔ `cf8baf1c…3d98` | ✔ | runtime | alloc, std | no |
| zmij | 1.0.23 | ✔ `29666d0a…9b1b` | ✔ | runtime | — | yes |
| serde_derive | 1.0.229 | ✔ `e7a5d712…9348` | ✔ | host proc-macro | default | no |
| proc-macro2 | 1.0.107 | ✔ `985e7ec9…66d9` | ✔ | host compile-time | proc-macro | yes |
| quote | 1.0.47 | ✔ `1fbf4db1…9001` | ✔ | host compile-time | proc-macro | yes |
| syn | 3.0.5 | ✔ `12df2e01…89f9` | ✔ | host compile-time | clone-impls, derive, parsing, printing, proc-macro | no |
| unicode-ident | 1.0.24 | ✔ `e6e4313c…4e75` | ✔ | host compile-time | — | no |

The 11th lock entry is the root trial package. Every source is crates.io. No package declares `links`, and the
closure has no `[build-dependencies]`. Dependencies' dev-dependencies (for example reqwest, rand, criterion,
flate2/tar) are not resolved.

**Feature check.**
- serde_json has only default/std enabled. `preserve_order`, `arbitrary_precision`, `unbounded_depth`,
  `raw_value` and `float_roundtrip` are all off, and indexmap is not resolved, so `Map` is backed by BTreeMap.
- memchr has no libc or logging features.
- syn has no full, extra-traits or visit features.
- proc-macro2 has no span-locations feature.
- serde has no rc or unstable features.

This matches the plan.

**The lock lists two edges that are never compiled.** `serde_json→serde` and `serde_core→serde_derive` are
`[target.'cfg(any())'.dependencies]` entries. `cfg(any())` is false on every target, so they only couple versions.
cargo metadata confirms this.

## 2. Build-time effects (build host, not runtime)

| Build script | Env reads | Processes | Files | Observed active cfgs (earlier byte-identical build) |
|---|---|---|---|---|
| proc-macro2 | RUSTC, OUT_DIR, TARGET, RUSTC_BOOTSTRAP/STAGE, RUSTC_WRAPPER, RUSTC_WORKSPACE_WRAPPER, CARGO_ENCODED_RUSTFLAGS | `$RUSTC --version`; rustc compile probes (through wrappers, with RUSTFLAGS) | creates and removes OUT_DIR/probe | wrap_proc_macro, proc_macro_span_location, proc_macro_span_file |
| quote | RUSTC | `$RUSTC --version` | — | none |
| serde | OUT_DIR, CARGO_PKG_VERSION_PATCH, RUSTC | `$RUSTC --version` | writes OUT_DIR/private.rs (constant template) | if_docsrs_then_no_serde_core |
| serde_core | OUT_DIR, CARGO_PKG_VERSION_PATCH, TARGET, RUSTC | `$RUSTC --version` | writes OUT_DIR/private.rs | none |
| serde_json | CARGO_CFG_TARGET_ARCH / POINTER_WIDTH | — | — | fast_arithmetic="64" |
| zmij | RUSTC, OPT_LEVEL | `$RUSTC --version` | — | none (opt_level="s" only under s/z) |

None of the build scripts use the network or call a package manager. serde_derive, syn, quote and proc-macro2 run
unsandboxed inside rustc. Their source uses no fs, net, process or env access; it uses a compile-time `env!`,
`thread::panicking`, a ThreadId and a thread_local. All of these effects are build-lane TCB and produce only cfgs,
the constant `private.rs` and expanded derive code. The observed outputs come from
`m1-eight-output-trial-01/compile-rust/target`, whose manifest and lock hashes are identical, and were not re-run.

## 3. Runtime effects

**Generated carriers (57,969 lines).**
- Imports are only sibling `super::` modules.
- `std` usage is limited to String, Result, conversions, fmt, Deref, Vec, Option, NonZeroU*, BTreeMap (8 uses),
  Box, Cow and error::Error.
- serde usage is limited to serde traits. serde_json usage is limited to `Value` (272 uses) and `Map` (6 uses).
- The carriers contain no unsafe code, no extern or link attributes, no fs/net/process/env/thread/time/random use,
  no HashMap/HashSet and no floating-point fields.
- Token hits were identifiers such as `include_suppressed` and doc text.

Result: the carriers import no runtime effects.

**Linked dependency code.**
- **Actual imports.** memchr, itoa, zmij and serde_json are `no_std` and get std only through features.
  serde/serde_core re-export `std::net` and `SystemTime`/`UNIX_EPOCH` only for trait impls. The runtime crates
  contain no fs/process/env/thread/clock reads, no `now()`, no getrandom and no external `include_bytes!`.
- **Latent helper APIs (not used by the carriers).**
  - serde_json's `from_reader`/`to_writer` work over caller-supplied io traits. `File` and `TcpStream` appear only
    in doc comments.
  - serde_core has Serialize/Deserialize impls for IP/socket addresses (parsing only), SystemTime (no clock read),
    Path/OsString (no filesystem access), and generic `HashMap<K,V,S: BuildHasher + Default>`.
- **Randomized HashMap.** It does not appear in the runtime closure or in the carriers. It is latent only if a
  consumer picks `HashMap` with `RandomState`. `#[derive(Hash)]` on 318 types is inert.
- **CPU feature detection.** memchr's `std` feature is on (through serde_json/std).
  - On **x86_64** builds without compile-time avx2, memchr runs `std::is_x86_feature_detected!("avx2")` at runtime
    and caches the result in a process-global `AtomicPtr` function pointer. Results do not change.
  - On aarch64 (this host), NEON is chosen at compile time. wasm32 selection is also compile-time.
  - zmij and itoa have no runtime detection.
- **Potential file handles.** No runtime crate opens any.
- **Resource behavior.** serde_json caps nesting depth at 128 but does not bound input size or allocation.
- **Map ordering.** BTreeMap backing gives sorted, deterministic object order.

**Unsafe and native code.** These counts are `\bunsafe\b` tokens, including comments. This is not a soundness
review.

| Group | Crate | unsafe tokens | Notes |
|---|---|---|---|
| Runtime | serde | 2 | UTF-8 unchecked |
| Runtime | serde_core | 2 | UTF-8 unchecked |
| Runtime | serde_json | 16 | UTF-8 unchecked, pointer writes/offset, unreachable_unchecked, RawValue transmute (raw_value off) |
| Runtime | itoa | 13 | MaybeUninit buffers, get_unchecked |
| Runtime | memchr | 340 | SIMD intrinsics |
| Runtime | zmij | 70 | Pointer table loads, SIMD, 5 comment-template `asm!("/*{0}*/", inout(reg) …)` codegen hints (x86_64/aarch64, not miri) |
| Host-only | proc-macro2 | 6 | — |
| Host-only | syn | 98 | — |
| Host-only | unicode-ident | 2 | — |
| Host-only | serde_derive | 0 | — |
| Host-only | quote | 0 | — |

**FFI.** There are no extern blocks, `#[link]`, no_mangle, export_name, global_asm, links keys or cc builds.
syn's `extern "C"` hits are doc comments.

## 4. Findings

| ID | Status | Finding |
|---|---|---|
| PD-01 | accepted | 11/11 archive sha256 match the lock, and the extracted archives equal the registry src |
| PD-02 | accepted | The exact closure and resolved features match the plan; the cfg(any()) edges are not compiled |
| PD-03 | accepted | Generated carriers import no runtime effects, unsafe code, FFI, hashing or floats |
| PD-04 | accepted-with-record | Latent effect-capable helper APIs (io Read/Write, net/SystemTime/Path impls, generic HashMap) exist in the libraries but are unused; record them |
| PD-05 | **requires decision** | memchr runtime AVX2 CPUID detection on x86_64 (via serde_json/std). Recommend accepting it as builtin context under TCB-SCOPE-01 and recording it. The no-std alternative was not evaluated. |
| PD-06 | **requires decision** | Unsafe Rust (memchr SIMD, zmij including comment-only `asm!`, itoa, serde_json) in the runtime closure needs explicit TCB acceptance. No soundness claim. |
| PD-07 | **requires decision** | Build scripts spawn rustc and probes, honor wrappers/RUSTFLAGS and write to OUT_DIR; the proc macro runs unsandboxed. Accept as build TCB and record toolchain, target, profile, wrappers and RUSTFLAGS. Effects are recorded, not assumed absent. |
| PD-08 | **requires decision** | Workspace feature unification (root host workspace, provider workspace) could turn on preserve_order, arbitrary_precision etc. The resolved features must be enforced against each authoritative lock. |
| PD-09 | **requires decision** | Mechanized pure-boundary gates: dependency and feature allowlist, source scan (fs/net/process/env/thread/time, HashMap/RandomState, extern/link, unsafe), drift check |
| PD-10 | **requires decision** | Trial `main.rs` and `bin/carrier_probe.rs` use `std::fs::read` with absolute paths. They are harnesses only and must not be production contracts targets. |
| PD-11 | accepted-with-record | serde_json input size is unbounded (depth is capped at 128); callers or admission must bound input bytes |
| PD-12 | informational | The generator lock (typify 0.8.0, schemars, regress, syn 2.0.119, …) is a separate build-time closure and was not reviewed |

**Overall.** The audit supports this closure as the pure contracts dependency set under TCB-SCOPE-01. Integrity,
pinning and features all verify, there is no FFI, and the carriers are inert. That support depends on the root
resolving PD-05 through PD-10. This is supporting evidence for tool selection, not production dependency approval.

## 5. Test evidence and limits

**Performed**
- sha256 of each raw archive checked against the lock
- Extraction and recursive diff against the registry src
- Offline, `--locked` cargo tree and metadata on a copied manifest and lock; the lock was unchanged afterwards
- Reading all manifests and build.rs files
- Source pattern scans
- Reading an earlier byte-identical build's build-script outputs and the trial roundtrip logs

**Not performed**
- No Rust build or test re-run. The compile and roundtrip results (12 metadata cases, and 64,091 harvested cases
  across 110 targets reported in the README) come from the earlier trial.
- No unsafe soundness review, miri or sanitizers
- No non-host target builds; x86_64 behavior comes from reading source cfgs
- No network checks: index, yank state, RustSec advisories and licenses were not verified
- No production or provider workspace lock exists yet to review
- Pattern scans are evidence, not proof of absence
