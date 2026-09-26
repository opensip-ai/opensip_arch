# 463a r2 resumed 2026-09-26

The r2 request above is unchanged except for these facts. Read REQUEST.md first.

- The r2 bytes are now committed: product HEAD `5faf0a5` ("saving the files modified before llm models crashed", made by the owner, outside the review workflow). The four paths at HEAD match `hashes.txt` byte for byte. Review them as the r2 subject; an ACCEPT still integrates only these exact bytes.
- The machine was reimaged. It is now macOS 27.0 (26A428) on an Apple M5 Max, not macOS 26.6.2. Rust 1.95.0 was reinstalled from the Homebrew 1.95.0 bottle at `/opt/homebrew/Cellar/rust/1.95.0/bin` (rustc 59807616e, LLVM 22.1.3). Crates were re-fetched against the unchanged Cargo.lock into `~/.cargo/registry`. The native tool hash pins no longer match; the owner has authorised a separate re-pin unit. That is not part of this review.
- The lead's pre-dispatch replay on macOS 27: `cargo fmt --all --check` passes; workspace clippy `--all-targets -D warnings` passes; `cargo test -p opensip-platform --lib`: 165 pass, 2 fail:
  - `macos_image::tests::a_different_file_does_not_match_the_kernel_hash`
  - `macos_loader::tests::macos_loader_actual_system_artifact_reports_digest_without_authority`
  Both panic with `Malformed("ambiguous architecture")` from `capture_system_loader`. macOS 27 `/usr/lib/dyld` is a three-slice fat file: x86_64, arm64e (subtype 0x80000002) and a new arm64e.x1 (subtype 0x8000000c). The accepted loader law 348 requires exactly one slice of the matching CPU family and refuses rather than guess, so the refusal follows the 348 law. The running process's loaded dyld is the 0x80000002 slice (hw.cpusubtype 2). The lead will propose a separate 348 successor for slice selection. It is not part of 463a.

## Also decide

- Is it correct that the two failures belong to the 348 loader law and not to the 463a changes? Does anything in 463a's own tests, besides the loader-dependent one, rely on the macOS 26 environment?
- Replay on this host and report the exact results you observe.
