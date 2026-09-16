# Independent Grok review: pure-provider-isolation-02 (shared-library build probe)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/trials/pure-provider-isolation-02/subject.json`
**Manifest SHA-256:** `3147a63a43825c4c9b1236d72f6b0afa36b507e3b518c13db4147f58c3479280`
**Members:** 36
**Verdict:** **ACCEPT-UNIT**

Bounded shared-source isolation evidence: current live `crates/contracts` and `crates/identity` sources compile and run from a read-only export that has no host root manifest, apps, tools, or Node, using a deliberately minimal separate provider workspace. This is **not** the Rust analysis provider, protocol transport, rustc/compiler integration, release qualification, sandbox, full M1, or a fresh blind consumer. README, build-receipt, source-pins, comparison, and export define scope.

## Custody

36/36 architecture members match the subject pins before and after independent execution. Subject SHA matches the stated value. Frozen architecture files and live product shared sources were not altered.

All **13** shared source files are byte-identical to current live selected `crates/contracts` and `crates/identity`, match `source-pins.json`, and are mode `0444` (`292`). Export tree has exactly **16** files (13 shared + `providers/rust/{Cargo.toml,Cargo.lock,src/main.rs}`). Isolation: no export-root `Cargo.toml`, `apps/`, `tools/`, `package.json`, `node_modules`, `crates/platform`, `crates/host`, `providers/rust/rust-toolchain.toml`, or JS/TS files. `provider-lock.selected` equals export `Cargo.lock` (`be35cf23…5176` / 3097). Live product has **no** `providers/rust` tree; the probe crate is not an installed provider implementation.

Execution used a private copy under `review/copy/export`, not the original `/tmp/opensip-implementation/m1-pure-provider-isolation-02` tree.

## Toolchain, environment, lock, source custody

Trusted Cargo/rustc 1.95 from `/opt/homebrew/Cellar/rust/1.95.0/bin`. Independent `--version --verbose` / `-vV` stdout is byte-identical to the frozen receipt logs:

| Tool | Version | stdout SHA-256 | bytes |
| --- | --- | --- | --- |
| cargo | 1.95.0 (f2d3ce0bd 2026-03-21) Homebrew | `23bd52f365167b59ceac26bec21ab63143d29c27108fd1b775b7bd4a32d3a552` | 314 |
| rustc | 1.95.0 (59807616e 2026-04-14) Homebrew | `d7fdd367b3ad098627179fd3b1d30a93f385ee891ae1138082e389d1b6317c68` | 203 |

Exec PATH was `/opt/homebrew/Cellar/rust/1.95.0/bin:/usr/bin:/bin:/usr/sbin:/sbin`. `which node` fails on that PATH (default nvm Node `v24.16.0` exists on the parent PATH and was excluded). Cleared and absent from the exec environment: `RUSTFLAGS`, `CARGO_ENCODED_RUSTFLAGS`, `RUSTC_WRAPPER`, `RUSTC_WORKSPACE_WRAPPER`, `RUSTC_BOOTSTRAP`, `RUSTUP_TOOLCHAIN`. Python: `/tmp/opensip-implementation/metadata-reference-env/bin/python -I -B` (CPython 3.14.6).

```
cargo run --locked --offline --manifest-path <private-copy>/providers/rust/Cargo.toml
cargo metadata --locked --offline --format-version 1 --filter-platform aarch64-apple-darwin
```

`CARGO_TARGET_DIR` was outside the export (`review/probes/provider-target`). **run exit 0**, empty stdout, compiled contracts + identity + the probe binary from the private copy in 19.39s. Direct binary re-run exit 0. Provider lock SHA unchanged after the locked run. Shared sources remained mode `0444` with unchanged hashes. Live host `Cargo.lock` SHA `1132d861…9b74` unchanged by host metadata.

This records tool versions, PATH, cleared compiler variables, lock bytes, and source modes. It is **not** a malicious-compiler attestation, same-user sandbox, or exhaustive native build-input receipt.

## Host vs provider dependencies

Independent target-filtered metadata: **14** shared packages; `allSharedVersionsSourcesFeaturesEqualHost: true`. Provider-only package: `opensip-rust-provider`. Independent rows match the frozen `comparison.json` names/versions/sources/features. The 11 policy registry checksums match the provider lock. Identity’s `sha2-const-stable 0.1.0` lock checksum is `5f179d4e…3ed9`.

## Proposed dependency checker and package edges

Used the actual-reviewed proposed checker + policy:

- `docs/implementation/m1/contracts-dependency-selection-v1/product/tools/check_dependencies.py` `d00f6d6f…1b34` / 6684
- `…/contracts/dependency-policy.json` `7e34a6a0…d6df` / 3771

Those bytes equal the live installed helper/policy. Against the private export, with Cargo 1.95 `--locked --offline --filter-platform aarch64-apple-darwin`: **pass**, 11 dependencies, 8 local contracts sources, `productQualification: false`. Result matches the frozen fixture except `workspace` (private copy path).

Installed `tools/check_package_edges.py` against **accepted inventory v10** (`6608fabd…8bc9` / 121810) `--lane rust-provider`: **pass**. Declared/resolved internal edges are only `opensip-rust-provider → opensip-contracts` and `→ opensip-identity`. `sourcePurityQualified: false`, `productQualification: false`. Exact match to the frozen fixture. Inventory v9 produces the same pass (rust-provider DAG unchanged). `--lane host` on the same provider metadata refuses `workspace crosses host/provider boundary`.

## Independent negative / isolation probes

Private mutant copies only:

| Probe | Result |
| --- | --- |
| Write to read-only shared `lib.rs` | EACCES (errno 13) |
| Extra file under `crates/contracts/src/` | refuses `local contracts source set differs` |
| Extra file at contracts package root | **still passes** (S1) |
| Extra file under `crates/contracts/tests/` | **still passes** (S1) |
| Unexpected `build.rs` at contracts package root | refuses `contracts production package must have one library target` (census does not see it; library-only target does) |
| Extra file under `crates/identity/src/` | contracts checker **still passes** (helper does not census identity; identity is covered here by pin/live byte equality) |
| Path-dep on a local `opensip-platform` | package-edges refuses `forbidden declared internal edge: opensip-rust-provider -> opensip-platform` |
| Node on restricted PATH | absent |
| Live `providers/rust` | missing, as expected |
| Probe provider files vs inventory v10 rust-provider file rows | deliberately minimal: only lock, manifest, `src/main.rs`; inventory lists toolchain + analysis/protocol modules that this probe does not implement |

## Must-fix / should-fix

Must-fix: none. `requiredFindings` remain empty.

**S1 (should-fix / disclosed inherited limit, reconfirmed):** `check_sources` observes `src/` plus `Cargo.toml` only. Extra regular files at the contracts package root or under `tests/` still pass. An unexpected `build.rs` at the package root is **not** in that census; it is refused later as a non-library production target. Do not treat a checker pass as a full package-tree census. This does not reopen the dependency-selection unit and does not block this isolation unit’s stated source-pin evidence.

## Limits (not fulfilled M1 duties)

- Shared-library isolated **build probe** only. The probe `opensip-rust-provider` is not the inventory rust-provider implementation (no `rust-toolchain.toml`, clones, compiler adapter, protocol, sealed VFS, or session).
- Package-edges pass attests allowed internal Cargo edges for `--lane rust-provider`, not inventory file completeness or source purity.
- The contracts checker attests the eight pinned contracts files plus 11 lock checksums/features; identity’s five files are attested here by subject pins and live byte equality, not by that helper.
- Does not authenticate Cargo/rustc, compiler wrappers, or cfg/proc-macro/build-script effects as a safety proof.
- Does not rehash crates.io archives or extracted registry trees.
- Does not implement rustc/compiler/provider transport, release, sandbox, full M1, or a fresh blind consumer.
- Read-only export modes are not malicious-owner filesystem isolation.
- `fullM1Complete` remains false.
