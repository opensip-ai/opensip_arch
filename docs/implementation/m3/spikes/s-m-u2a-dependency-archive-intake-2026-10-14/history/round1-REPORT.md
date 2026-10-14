# S-M U-2a: crates.io archive intake for the Rust dependency-source sets

This is an outside-product data unit, the first part of U-2 in the S-M report plan r3. Under D-2, the Rust dependency-source set for SM-5 and SM-7 is the contracts' `DependencySourceSetV1`: the activated, admitted, non-path population of each workload's lock. Building those sets for the Rust rows other than axum needs every locked crates.io archive.

The accepted registry template r116 lacked 41 locked archives of the eight generated locks (`index-inputs/receipt.json`, `lockedBy`). Ten of them are windows-target crates, and the rest are mostly dev-dependencies. This unit acquires and admits those archives with the accepted recipes, changing only paths, names and counts:

| Step | Script | Accepted parent |
|---|---|---|
| Index | `prepare_u2a_missing_public_indexes_r1.py`: anonymous HTTPS to index.crates.io, no proxy, auth or cookies, redirects refused. Names are **lock-derived** (lead decision 2026-10-10), not diagnostic-derived; each locked version and checksum must appear in the fetched index. | `prepare_sm_hierarchy_missing_public_indexes_r7.py` |
| Archives | `prepare_u2a_missing_public_archives_r1.py`: **every** published version of each name, from static.crates.io, verified whole against the index checksum. No version winner is chosen. | `prepare_sm_deno_smithy_missing_public_archives_r13.py` |
| Packet | `prepare_u2a_public_intake_packet_r1.py` | the r13 intake-packet recipe |
| Intake | `run_u2a_public_cache_intake_r1.py`: the closed lowercase supplied-entry intake image (accepted public intake entry). | `run_sm_smithy_hierarchy_public_cache_intake_r12.py` |
| Template | `prepare_u2a_registry_template_r117.py`: template r116 plus the intake's files. | the r13 supplemental-template recipe |

## Results

- **Index.** 23 names: cfg-if (17), env_logger (59), matchit (28), redox_syscall (115), regex-syntax (79), reqwest (126), serde_spanned (18), toml (122), toml_datetime (25), toml_parser (17), toml_writer (12), trybuild (123), windows-sys (23), windows-targets (23), windows_aarch64_gnullvm (20), windows_aarch64_msvc (35), windows_i686_gnu (37), windows_i686_gnullvm (5), windows_i686_msvc (38), windows_x86_64_gnu (37), windows_x86_64_gnullvm (20), windows_x86_64_msvc (38), winnow (111).
- **Archives.** 1128 archives fetched, every one matching its index checksum (292,751,770 bytes).
- **Intake.** Exit 0 and success: 23 indexes and 1128 version records, with the stock cache serialization round-tripped (`intake-outcome/`).
- **Template r117.** 11504 files: 11054 archives and 450 index files. The 47 overlaps are recorded in the template manifest: byte-identical archives kept once, and newer index files replacing their named slots.
- **Coverage** (`u2a-coverage-r1.json`). Every crates.io row of all nine Rust locks, axum's included, now has its archive in r117 with the lock's checksum.

**Retained, not staged.** The archive bytes (about 293 MB) stay in the working directory, pinned by `archive-inputs/receipt.json`; the template root likewise.

## Standing

- **Admission.** No source authentication, no native admission and no corpus resolution. The template is labelled a supplemental raw cache copy for future experiments.
- **Not yet built.** The dependency-source sets themselves are U-2b; the SM-5 and SM-7 series are U-2c.
- **Gates.** L-G1 is open, and L is not in effect.
