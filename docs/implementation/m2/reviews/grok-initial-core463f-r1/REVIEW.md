# Review: InitialCore producer 463f-3 and tests 463g

Grok is the single reviewer. Claude Opus 5.5 leads. Code review of the producer and its tests. No repository edits.

Product HEAD `8e7eb49f35fb13446494223cad21f1fe23216d97`. The six files match `hashes.txt`. Two are new: `initial_core.rs` (33478 bytes, sha256 `95090cbbaa6c8bfd2b6608e430ce6dad9860587971ab94b3be895880919a881e`) and `initial_core_tests.rs` (21167 bytes, sha256 `2119e5d0e38767cd90a432a52fa8edfc8fa1d498fdc897974c79472ef88fe6c0`). Inventory v69 already plans both paths. Law is 463 r3 and items 1–12. Rustc `1.95.0` (`59807616e`). `cargo --locked --offline`.

## Verdict

**ACCEPT-UNIT.**

## Producer

`produce_initial_core` runs on one `attempt.run`, so a refusal latches. F0 admits the embedded values before any native call. A development build returns `EmbeddedRootAbsent` and the only charge is the lineage. The absence order is root, entrypoint, bootstrap. A target with no platform id returns `PlatformUnavailable`.

F1 observes the running image, at most 96 MiB. F2 requires the retained leaf's bytes, and then the on-disk spelling, to equal the entrypoint's last component. F3 uses `component_count()` as the index of the executable's directory: index 0 is `/`, and the last edge is that directory. With `n` entrypoint components the root index is `C − (n − 1)`, which is at least 1, so `/` is never the tree root. Directories above that index are not judged. From the root down, each directory is judged, and each name below the root must equal the matching entrypoint component. F4 judges the executable on the image's own descriptor. F5 opens `inventory.json` and `inventory.sig.json` under the root. F6 walks the bootstrap components. F7 opens the payload pair. F8 parses the manifest and admits its paths. Nothing is authenticated yet.

F9 opens each root-chain path, the revocation path, and each listed envelope by no-follow opens under judged directories, memoized, within 16 MiB. A symlink open is `ELOOP` and becomes `Custody(Symlink)` before the predicate. Exact on-disk names refuse a case variant. Item 9 then requires the envelope list to pair one-to-one, by carrier stored digest, with the chain bodies and the revocation body. An extra envelope is read inside that cap and then refused as `BootstrapEnvelopeSet`. It is not inserted in the store and not passed to authentication. That is the necessary order: the stored digest is inside the envelope bytes. The store still does not widen.

F11 builds the anchor from the embedded root binding and the compiled platform, with the closure from `project_v3` of that platform. F10 inserts exactly the anchor record, the inventory pair, the payload pair, the chain bodies, the revocation body, and the paired envelopes, keyed by sha256. A missing key is `Missing`. F12 calls `authenticate_embedded_release` on the borrowed budget. The receipt is built only after that returns: F13 checks the bootstrap directory, F14 reads K and the flags, F15 checks the entrypoint path and its sha256 and length against the image, F17 refuses a `release` entry naming this closure, F18 requires the image status to include the flag mask, and F19 maps writer 1 and 2 to `Stage1` and `Stage2`. F20 rechecks the image and every judged directory and file. F21 returns `InitialCore`.

`InitialCore` is private, not `Clone`, and its debug output is non-exhaustive. `recheck` refuses a foreign attempt and latches it. The injected image exists only under `cfg(test)`. Production `produce_initial_core` observes the live image.

The closing recheck requires the same metadata for every judged directory. The law does not state that sample. It matches a tree whose bytes are the committed rows: a later mode or inode change is `Changed`. The parse charges are the stated allowance of four times the source bytes, not a measured allocator bound. `MAX_IMAGE_BYTES` is 96 MiB. The law fixes no size for the real binary. The platform live-join test still uses its 64 MiB observation bound. Multi-component member paths and a mid-production budget exhaustion are untested. The code walks every component and charges each open.

## Tests

The eleven security tests use a signed on-disk tree, explicit ACLs, and the injected image. The positive test checks the closure, `Stage1` and `Stage2`, the lineage, and recheck, and a foreign recheck latches. The negatives cover each absent embedded value, an unavailable platform, the entrypoint name, a case-variant directory, `TreeRootBound`, omitted ACL, group write, links, symlinks, the envelope set, entrypoint bytes, the bootstrap path, a wrong embedded root, the flag mask, a quorum break, and a mutation after admission. Item 8 is the pure helper, as item 12 requires. The live development path refuses at F0 with only the lineage charged. The platform test copies the test binary, executes it, and checks that its kernel cdhash equals the parent's, with sha256, length, `CS_VALID`, and `Entries` of at least one on the file and its directory.

## Replay

- `cargo test --locked --offline -p opensip-security --lib`: exit 0. 479 passed, 0 failed, 2 ignored. All eleven `initial_core` tests passed.
- `cargo test --locked --offline -p opensip-platform --lib`: exit 0. 172 passed, 0 failed, 1 ignored. The copied-binary join passed. The ignored test is the child reporter.
- `cargo clippy --locked --offline --workspace --all-targets -- -D warnings`: exit 0.
- `cargo fmt --all -- --check`: exit 0.

Do not commit.
