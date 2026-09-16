# Independent Grok review: rust-provider-workspace-selection v1 (M1 bootstrap)

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject manifest:** `docs/implementation/m1/rust-provider-workspace-selection-v1-subject.json`
**Manifest SHA-256:** `7621eedcee592785790ce46ff58c8c53e4d901cacbdbc74422844d115aff894e`
**Members:** 31
**Verdict:** **ACCEPT-DESIGN-UNIT**

Checked-in `providers/rust` workspace/lock/toolchain plus a fail-closed development entry point. This can close the **checked-in bootstrap portion of RF05 after actual integration**. It is **not** M3 compiler/protocol/SDK, not successful analysis, not a cataloged provider, and not complete M1. This verdict is **not** merged with foundation-primitives-selection v2.

## Custody and joins

31/31 selection members match. Frozen implementation subject `docs/implementation/m1/trials/rust-provider-workspace-01/subject.json` SHA `94fa905c…7a49` — **206/206**. Adjacent archive matches `archive-pin.json`. Candidates are exactly the subject minus `successor.json` (30). Parents: accepted contracts-dependency-selection-v1 `c9a74172…3561` / 5972 and inventory v10 `6608fabd…8bc9` / 121810. All 4 map rows match frozen product and inventory v10 (`Cargo.toml`, `Cargo.lock`, `rust-toolchain.toml`, `src/main.rs`). Inventory still 20 packages; no extra paths/DAG. Root `Cargo.toml` already `exclude = ["providers/rust", ...]`. Genuine live 8/8 is not approval of these bytes. Private copy only (`review/copy/provider-v1`).

`Cargo.toml` `cd818152…fd67` / 268 and `Cargo.lock` `be35cf23…5176` / 3097 are byte-identical to the accepted isolation02 probe. `rust-toolchain.toml` is an explicit 1.95.0 minimal+rustfmt/clippy development pin, independent of host. `main.rs` is **not** the isolation02 probe binary: it is a fixed unavailable stub.

## Entry point

`main` writes one stderr line and returns `ExitCode::FAILURE` before reading stdin. No stdout frames, handshake, capability ack, or synthetic analysis. Independent runs with empty stdin, `{"kind":"hello"}\n`, and a NUL-bearing non-frame: **exit 1**, empty stdout, exact stderr `opensip Rust provider: native analysis is not implemented in this development build\n` (3/3). Host CLI/apps sources do not advertise this binary. A nonzero refusal is not analysis success; M3 must replace this with reviewed protocol handling.

## Private export / vendor / empty CARGO_HOME

Recreated 17 source files (13 shared + 4 provider) read-only; no export-root `Cargo.toml`/`apps`/`tools`/Node. 12 registry archives unpacked with `build_contracts.unpack_archive` against lock checksums into a private vendor; `CARGO_HOME` contained only `config.toml` replacing crates.io with that vendor. PATH `/usr/bin:/bin`; `RUSTC` Homebrew 1.95; no Node. `cargo build --locked --offline --target aarch64-apple-darwin` exit 0. Provider lock SHA unchanged through the run. Contracts checker 11/8 pass. Package-edges `--lane rust-provider` vs inventory v10 pass (edges only contracts+identity).

Host workspace metadata local packages: cli, contracts, host, identity, platform, reporting — **no** `opensip-rust-provider`. `cargo build -p opensip-rust-provider` from the host root refuses `package ID specification did not match any packages`. No first-party implicit cross-lane build.

## Prior identity bytes (mandatory limit)

Export identity files are the **pre-foundation** live bytes (`digests.rs` `8f39ca08…12a6` / 1973; `lib.rs` without `parse_hash_preimage`). They equal current live identity and isolation02 shared sources. They do **not** equal foundation v2 identity. After foundation integration, root must rebuild the export over **current** shared bytes before any current-byte isolation claim. This unit does not make that claim.

## Must-fix / should-fix

Must-fix: none. `requiredFindings` remain empty.

## Limits

- Closes checked-in workspace/lock/unavailable-entry bootstrap of RF05 **only after** genuine review, private activation, and live materialization. Not M3 compiler/protocol/sealed-VFS/session. Not successful analysis.
- `rust-toolchain.toml` is a rustup channel pin. This reproduction used Homebrew Cargo/rustc 1.95 paths, not a rustup toolchain fetch, and does not attest linker/SDK/compiler libraries.
- Source export is prior identity/contracts bytes. Foundation v2 identity is a different unit and a later rebuild duty.
- Isolation02 probe proved shared-source build feasibility; it did not satisfy checked-in workspace custody. This unit is that custody, not native-analysis quality.
- Native host-build-isolation-01 and TS-lane-isolation-01 are root proofs over other bytes, not this code.
- Not sandbox, release, signed provider closure, or fresh blind consumer. Full M1 remains open.
- This verdict is not merged with foundation-primitives-selection v2.
