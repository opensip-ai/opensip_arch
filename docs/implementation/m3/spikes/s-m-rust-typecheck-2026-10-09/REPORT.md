# Preliminary virtual-source direct-Rustc library-cohort observations

New observations, unreviewed partial S-M. No SM4/SM11/fullSM/LG1/effectiveL/production source admission or confinement claim. Accepted S-P/foundation/other S-M and owner/law scopes remain closed.

The retained coherent official Rust1.95 sysroot builds this first-party rustc_driver wrapper with RUSTC_BOOTSTRAP=1 only for that wrapper compilation. The initial compilation identified two actual pinned API differences (Arc binary-file return and current_directory requirement); the corrected wrapper compiled with the same sysroot. First build failure log is retained. Analyzed inputs never receive RUSTC_BOOTSTRAP. No Cargo, build script, package script or proc-macro native code runs.

The wrapper installs a FileLoader before parsing. Source text and binary include reads resolve only from a prepared in-memory exact-byte map, under lexical absolute path normalization; no source fallback reads from disk. This boundary covers Rust SourceMap/module/include callbacks, not every compiler filesystem/metadata/runtime operation. The pinned sysroot remains the trusted standard metadata/runtime source. The wrapper stops at after_analysis before emission. One matching callback with exit0 is positive evidence of successful analysis for that declared root, not whole workload truth. Failed callbacks/type errors/missing dependencies remain explicit.

Exact seven Rust medium dev repositories plus the defined mr-rs-medium-serde-json overlay were selected before reads, members heldOut=false, store.verify passed. Every regular source-map byte was read no-follow with inode/size/time checks and hashed; nonregular/symlink entries excluded explicitly. Overlay aliases were checked against their exact verified member stores, and the existing overlay digest independently recomputes. No synthetic root Cargo.toml, dependency .rmeta, generated build output or SourceCap is supplied.

Selection is exploratory every retained Cargo.toml package with a declared/default retained library root, including tests/examples/fixture packages, excluding bin-only/virtual/unreadable/missing-lib cases explicitly. Direct rustc arguments use the root name/types, direct or finite retained-ancestor workspace edition, and bare local default-feature-label reachability. This is NOT Cargo-compatible full feature/optional-dependency/resolver/target/build/environment/config semantics or an admitted workspace/native profile. dep: and forwarded dependency feature strings are not projected; no extern dependency artifacts or Cargo package/build-output environment are supplied. Cargo-home stays the required user path; HOME unchanged; other inherited environment is excluded except the named locale/timezone fields. No ambient secret variables are made available to compiler env macros.

Three root-set warmups then seven runs; each declared library uses a fresh child. Eight sets contain48 roots,480 child observations. Phase/exit/read-count shapes repeat across all10 sets. Seven roots reach after_analysis with exit0 on each repetition (70children);41 roots do not. Four positive napi roots are three source fixtures and crates/build; three tokio roots are tests-build, tests-integration and tokio/src/lib.rs under this direct feature cohort. These successes do not establish repository-wide native readiness. Failure process costs are not labelled successful typecheck/analysis costs.

| Workload | Declared library roots | Successful after-analysis roots | Median entire root-set ns | Maximum entire root-set ns |
| --- | ---: | ---: | ---: | ---: |
| poly-medium-napi-rs | 18 | 4 | 2556407542 | 2563789250 |
| rs-medium-aws-lambda-rust-runtime | 6 | 0 | 1795055917 | 1817478042 |
| rs-medium-axum | 4 | 0 | 645128250 | 646790875 |
| rs-medium-hyper | 1 | 0 | 41487333 | 42037834 |
| rs-medium-serde | 4 | 0 | 511129250 | 521599083 |
| rs-medium-serde-json | 2 | 0 | 290329125 | 420399542 |
| rs-medium-tokio | 7 | 3 | 417672166 | 421651750 |
| mr-rs-medium-serde-json | 6 | 0 | 805380583 | 808975334 |

The entire root-set span includes child spawn/runtime/map decode/failed and successful compiler invocations and owned output-directory bookkeeping; it is not pure analysis. Per-child times, callback events, native macwait4RSS bytes and stdout/stderr are retained. Output directories stayed empty on these480 observations; this does not prove worker-wide peak scratch or accounted-memory equivalence. No cold reset/F/T/medium budget or Q6 conclusion.

Six first-party synthetic API controls: valid typecheck; type error E0308; module/text/binary includes; missing OUT_DIR build context; unavailable derive dependency; denied out-of-map text include. Valid roots reach successful after_analysis, failed roots exit101, denied include records one denied read and no successful callback. Actual type error occurs after_expansion even though after_analysis is not reached; labels record phases rather than claim no typechecking occurred. An owned outside marker remained unchanged; this is only an API map denial, not OS confinement.

Still required: lawful full Cargo/native context, missing dependency and build/proc expansion data, complete snapshot/dependency sets, actual whole workload typecheck and per-subject/scratch figures, full replay graph, scope derivations and actual fact/spool/payload/frame/census/stage volumes. No native failure route is inferred from exit101/English diagnostics, and no product code, identity, registry, profile, inventory or lock is changed.
