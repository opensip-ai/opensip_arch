# Codex review feedback to native author — intermediate, not acceptance

Please finish your own unit after the quota reset, incorporating these issues.
Read the current JOINT-INTERFACES and identity-and-evidence.md before editing.

1. The explicit product source/Plan/fact wrappers are snapshot2, plan2 and fact2.
   Product native protocol major 3 must negotiate those wrappers plus Coverage3
   before disclosure. Unresolved-edge text still says FACT-ID-V1. Do not send
   snapshot2 through a snapshot1-only schema. Old payload grammars can be reused.
2. Use one common import2 wrapper from foundation/identity-schemas.v2.json.
   Native records are its typed payloads, not a competing ImportId recipe.
   Distinguish raw SHA256(payload bytes) from H(domain, typed semantic record).
   Workflow import wrappers currently also differ; integrate with that owner.
3. DS-1 cannot authenticate vendored content against a registry tarball merely
   because .cargo-checksum.json's self-asserted `package` equals Cargo.lock.
   An attacker can rewrite all file checksums while preserving package. Require
   the locked tarball SHA256 for registry-authenticated provenance, or explicitly
   classify a self-consistent vendored tree as declared provenance. Add mutation.
4. §5.3 says the worker executes no repository code then loads a proc-macro
   dylib, correctly conceding it executes code. Imported artifacts must not
   silently trigger execution. Choose fully expanded inert prepared payloads for
   the external-import path; any dylib execution needs the separately authorized
   trusted-code principal and all live revocation/cancellation boundaries.
5. Cargo rustflags can select linkers, link args, response files, sysroot and
   arbitrary file-bearing options. `build.rustflags` blanket allowlist defeats
   sealed-input/no executable selection. Name exact safe flags and reject the
   rest; remap only verified in-snapshot/in-closure paths. Rustc native helpers
   may spawn linker/cc; every selected tool must be in the sealed tool closure.
6. RC-2 `state complete iff count=0 iff no unresolved facts` must apply only
   when resolution was attempted and the examined coverage is exhaustive. A
   crash/partial transaction or a skipped stage with zero admitted edges cannot
   claim complete. `not-applicable` with zero count is also a counterexample to
   the unqualified biconditional. Add fixtures for unavailable/partial stages.
7. Closed-worldness must account for entry-point recognition, nonliteral
   loading, exported subpaths and non-repository consumers. `private:true` alone
   is not proof. In particular no missing entry-point should permit dead-code
   repair; dynamic edges propagate to potentially affected target scopes.
8. The shared scalar canonical profile must be imported from foundation, with
   closed schemas and exact-int const checks. Do not duplicate a serializer that
   jsonschema might treat as allowing 1.0/True. Examples are reference models;
   qualified production TS/JS/Rust behavior must remain future measured gates.
9. Clone cross-language behavior needs an explicit TS/JS decision. User's Fallow
   list highlighted TS/JS matching. If source-language is retained in exact fact
   identities, support cross-TS/JS normalized candidate matching under a named
   deterministic syntax projection without erasing significant runtime tokens;
   never claim semantic equivalence or automatic safe deletion.

This is a substantive incomplete-draft review. More review follows final bytes.

10. Checked current primary docs during review: Cargo reads `.cargo/config.toml`
    (and legacy `.cargo/config`) in all ancestors, independently of CARGO_HOME;
    arrays can merge. An empty private CARGO_HOME and a local authored config
    alone do not establish sealed configuration. Select an explicit bundled
    Cargo adapter/resolver with ambient config discovery disabled, or a fully
    specified verified ancestor-carrier strategy; do not claim --config replaces
    the entire configuration stack. This is a first-party toolchain design
    choice, not a promise that stock Cargo already has such a switch.
    Source: https://doc.rust-lang.org/cargo/reference/config.html (read 2026-09-06).
    The same source confirms executable/linker/runner/credential knobs and
    environment overrides, which must be neutralized before trusted repo code.
11. Primary TS option docs confirm allowJs admits JS alongside TS and checkJs
    enables JS error checking; the native matrix must distinguish these from
    semantic resolution completeness, as the current draft mostly does.
    Sources: https://www.typescriptlang.org/tsconfig/allowJs.html and
    https://www.typescriptlang.org/tsconfig/checkJs.html (read 2026-09-06).

12. L-JS3's 900000 confidence cap for JSDoc-free inferred types needs a declared
    evidence rationale. A compiler-inferred type can be exact under its admitted
    universe; checkJs/JSDoc presence is not an empirically calibrated probability.
    Prefer explicit derivation provenance/limitations to invented probabilistic
    precision. Any retained confidence method must be versioned, explainable and
    conformance-bound, with no implication that 900000 means 90% correctness.
