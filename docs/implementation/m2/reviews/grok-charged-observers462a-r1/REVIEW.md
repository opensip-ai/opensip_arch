# Review: charged platform observers 462a r1

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the accounted boot, process, and loader observers. No repository edits.

Product HEAD `43c5e45313390201bceba6aa465a71a87e4b926d`. The seven platform files match `hashes.txt`. No file is added. Law is 462 item 3. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Answers

Every native call in the new accounted paths sits inside a charge taken before it runs. The unaccounted functions remain, and the live tests require each accounted result to equal its twin.

`macos_process_observation_cost` is 0 objects, 1 edge, and 12 bytes: one `sysctlbyname` of `sysctl.proc_translated` into an `i32` plus the length word. Both live on the stack.

`macos_boot_observation_cost` is charged once before `observe_macos_boot`. That function does two bounded sysctls (`kern.uuid` at 37 bytes, `kern.osversion` at 10), two `csr_check` calls, and then allocates the two validated strings, at most 36 and 9 bytes. The cost is those buffers, the two length words, four edges, and two string objects. The kernel name lookup and the csr syscall stay one edge each.

The loader still selects by the mapped dyld header. `capture_system_loader_accounted` charges `loader_header_cost` and calls `loaded_dyld_architecture` before any file open. `locate` then uses that architecture, `MH_DYLINKER`, and the same caps as the unaccounted capture. `capture_at` and `capture_at_accounted` perform the same checks: exact names, the leaf observation, the before-read check, the size bound, the lookahead read, the after-read check, the slice and hash, and the closing recheck. The equality test compares the cdhash, the CPU pair, the CodeDirectory, the slice, the raw bytes, and the metadata, and it checks the pair against `loaded_dyld_architecture`.

The read is charged at `IMAGE_CAP + 1` (16 MiB plus the lookahead) before the size is trusted. The buffer is `Vec::with_capacity(size + 1)`, so a grown file cannot reallocate past that charge. The parser vectors are charged at `MAX_ARCHITECTURES` and `MAX_SIGNATURE_SLOTS`. The hash is one call and 32 bytes. The move into the retained buffer is charged as a second image allocation at the cap. A ledger whose byte limit is the pre-read cost plus `IMAGE_CAP` refuses `Bytes` with `used()` still at the pre-read cost, on `/usr/lib` and on a fixture whose after-read hook does not run.

`descriptor_acl_cost` prices 128 entries, the same ending index the reader already refused. Opaque libSystem ACL allocations are objects with no byte size, and `mbr_uuid_to_id` is one call. Kernel work inside sysctl and `csr_check` is not measured. Reads assume no short read, as `macos_image` does. Those limits are stated on the cost functions.

The two cap-sized loader reservations are about 32 MiB. The attempt ledger is 256 MiB, and `InitialCore`'s image bound is 96 MiB. Both fit, with room for the rest of the act. Charging the cap before the size is known is the reservation that covers a dyld at the cap. A smaller dyld is a conservative overcount.

`recheck_exact_names_cost` now calls `recheck_exact_names_cost_for`, so the path method and the loader's pre-open price cannot drift. `filesystem_accounted` uses the existing `observe_filesystem_accounted` on the retained loader file.

## Replay

- `cargo test --locked --offline -p opensip-platform --lib`: exit 101. 176 passed, 1 failed, 1 ignored. The failure is `native_filesystem_original_file_lock_and_all_path_components_stay_owned`: `ChangedDuringRead` on a live descriptor.
- `cargo test --locked --offline --workspace --all-targets`: exit 0. 984 passed, 0 failed. That run includes the platform lib at 177 passed, 0 failed, 1 ignored, including the test that failed in the isolated run.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
