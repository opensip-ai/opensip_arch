# S-M U-2b overlay entry: `mr-rs-medium-serde-json` / `rs-medium-serde-json`

This is the follow-on to U-2b (accepted, `codex-sm-u2b-r1`), which left this entry pending. The entry's `serde_json` depends on `serde_core`. The T2 overlay links `serde`, `serde_core` and `serde_derive` to the sibling `rs-medium-serde` mount, and the accepted command-data producer applies those links as projected `patch.crates-io` paths. The accepted metadata harness takes no projected configuration, so it could not resolve this entry.

## Variant

- **What it is.** An append-only change to a copy-on-write clone of the accepted command-data producer (`variant/`; the audit asserts the accepted file is an exact prefix). The appended test `collect_explicit_experimental_overlay_metadata`:
  - applies the accepted overlay projection (`values`) and query context (`graph`);
  - then calls Cargo's `output_metadata` instead of building the unit graph, with dependencies included, filtered to `aarch64-apple-darwin`, and frozen, locked and offline as the accepted harness ran.
- **Execution.** Nothing compiles or executes.
- **Build.** The accepted controls recipe (`build_overlay_metadata_r1.py`): `cargo test --no-run --locked --offline`, vendored source, lane held. The image is `478e5cfb…`.
- **Vendor tree.** The first build failed because macOS `com.apple.tmp_cleaner` had emptied the accepted vendor tree under `/tmp` (all 507 crate directories; `build-attempt0-eroded-vendor.log`). It was re-acquired with `cargo vendor --locked --versioned-dirs` into the implementation cache: 507 crates, with exactly the lost tree's directory names, each verified by Cargo against the producer's `Cargo.lock` (`vendor/`; lead decision `LD-WORKDIR-TMP-EROSION`).

## Runs

Each observation root has a private home whose registry is a copy-on-write clone of template r117 (U-2a). The corpus copies are checked unchanged.

| Run | Overlay links | Exit | Packages | Registry | Equals the accepted harness |
|---|---|---|---:|---:|---|
| control A: `rs-medium-serde` | none | 0 | 32 | 27 | True |
| control B: overlay `rs-medium-serde` | accepted | 0 | 32 | 27 | True |
| target: overlay `rs-medium-serde-json` | accepted | 0 | 38 | 34 | — |

The controls compare package ids and the resolve graph (node ids, dependency edges and features) with U-2b's accepted-harness metadata. With the overlay applied, the target has three fewer registry packages than standalone serde-json (37), because the overlay supplies `serde`, `serde_core` and `serde_derive` as path packages, which stay in the snapshot (NE:1687).

## Set

The U-2b audit and set scripts (`*_entry8.py`; only input and output names changed) give:
- set `sha256:f9a12b770a726cc66664dafa61cea5e04e052568092ad22839e757a3da60bd4d`;
- 34 registry packages, 1490 files and 15723557 bytes;
- reference model and product bridge in agreement;
- a generated lock, labelled a sizing stand-in (NE:1264), as in U-2b.

All set records are in `entry8-records.tar.xz` (index pinned). With this set, every Rust entry has a dependency-source set.

## Standing

- **Admission.** No source authentication, import admission or Plan.
- **Values.** No SM-5 or SM-7 value; those are U-2c's.
- **Gates.** L-G1 is open, and L is not in effect.
