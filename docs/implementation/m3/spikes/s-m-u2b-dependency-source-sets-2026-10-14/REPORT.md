# S-M U-2b: Rust dependency-source sets

This is an outside-product data unit, the second part of U-2 in the S-M report plan r3. Under D-2, SM-5 and SM-7 take the Rust dependency-source set as the contracts' `DependencySourceSetV1`: the activated, admitted, non-path packages of the lock, for the target (NE:612, NE:1693-1694; DS4-P1). This unit builds that set for every Rust medium entry from the U-2a template r117, with axum, whose set was accepted earlier, carried through as the control.

## Pipeline

1. **Receipts** (`build_u2b_receipts_r1.py`).
   - **Source.** Built only from template r117. Each package's archive must match its lock checksum.
   - **Index lines.** Decoded byte for byte from r117's stock Cargo `.cache` files (format: `0x03`, index version 2, `Unknown`, then version and JSON-line pairs). Every locked version and checksum must be present.
   - **Lock sources.** Only crates.io sources occur; path packages stay in the snapshot (NE:1687).
2. **Resolved metadata** (`run_u2b_resolved_metadata_r1.py`).
   - **Recipe.** The accepted `run_axum_resolved_metadata.py` recipe, looped over the entries: the accepted harness image `45816163…` (its pin was checked), offline, frozen and locked, with dependencies included and filtered to `aarch64-apple-darwin`.
   - **Controls.** A private Cargo home seeded only from the receipt, and the corpus copy checked unchanged.
   - **Axum control.** It resolves 191 packages, 187 from crates.io, the accepted counts.
3. **Source audit** (`check_u2b_dependency_sources_r1.py`). The accepted audit, looped: every extracted tree equals its archive. Axum gives 187 packages and 7,338 files.
4. **Keys, features, manifests, descriptor** (`build_u2b_sets_r1.py`).
   - **Steps 5 and 7.** The accepted recipes, generalised.
   - **Step 6, reconstructed.** Its accepted script was not retained, so it is rewritten with the accepted format (sorted `[{path, contentSha256, byteLength}]`).
   - **Identities.** Every identity is computed by the reference model and by the product bridge, rebuilt from the accepted `hash_bridge.rs` source against the current `opensip-identity` (`hash-bridge/`). The two agree everywhere.
   - **Axum control.**
     - The rebuilt bridge first reproduced the accepted set `879ff234…` and unified features `7dfdb8a1…`.
     - The pipeline reproduces the accepted package keys, all **187 file manifests byte for byte**, and the accepted descriptor byte for byte, with set id `879ff234…`.
   - **jsonschema.** The reference model loads the product's vendored jsonschema 4.25.1. The earlier measurement copy is no longer complete.

## Sets

| Entry | State | Set id | Registry packages | Files | Bytes | Lock |
|---|---|---|---:|---:|---:|---|
| rs-medium-axum | built | sha256:879ff2348eb48e9c… | 187 | 7338 | 75258910 | original |
| poly-medium-napi-rs | built | sha256:72d01fef51839d92… | 153 | 6852 | 76407827 | generated (experimental) |
| rs-medium-aws-lambda-rust-runtime | built | sha256:f312a658d0a61014… | 234 | 11330 | 166417590 | generated (experimental) |
| rs-medium-hyper | built | sha256:89dedb96ed1a72f7… | 55 | 2880 | 37658554 | generated (experimental) |
| rs-medium-serde | built | sha256:eafd6cae491de11d… | 27 | 999 | 11156070 | generated (experimental) |
| rs-medium-serde-json | built | sha256:c0eddbb8c838cbfa… | 37 | 1586 | 17011309 | generated (experimental) |
| rs-medium-tokio | built | sha256:19b834946aac6330… | 146 | 6031 | 59869578 | generated (experimental) |
| mr-rs-medium-serde-json/rs-medium-serde | built | sha256:eafd6cae491de11d… | 27 | 999 | 11156070 | generated (experimental) |
| mr-rs-medium-serde-json/rs-medium-serde-json | pending | — | — | — | — | — |

The overlay's `rs-medium-serde` entry gives the same set as `rs-medium-serde` (same lock).

## Decisions and labels (lead, applied here)

- **Generated locks.** Only axum ships an original lock. For the others, `lockfileIdentity` is the experimental lock generated in the accepted corpus collection. NE:1264 says a missing original lock is `input-closure-incomplete` (`lockfile-missing`) and never an implicit generate-lockfile, so a product run over these trees would refuse. Their sets are therefore **sizing stand-ins** for SM-5 and SM-7, labelled as such, and not what a product run would admit.
- **Resolver.** Each set's resolver is taken as Cargo takes it: `workspace.resolver`, then `package.resolver`, else the package edition's default. The basis is recorded per set.
- **Overlay.** Each overlay entry is its own set, as D-3 runs it (two entry children).

## Pending: overlay entry `rs-medium-serde-json`

- **The failure.** Its metadata resolution fails in both attempts: `no matching package named serde_core`.
- **The cause.** The overlay links `serde`, `serde_core` and `serde_derive` to the sibling mount, as the accepted command-data producer projects them. The accepted harness takes no projected configuration and ignores config files, so attempt 2's private-home `config.toml` was not read.
- **What it needs.** A harness variant that applies the accepted overlay links. The working tree of the accepted harness producer is no longer complete, so the variant has to be built separately. It is owed before U-2c's R8 entry 8.
- **Retained.** Both attempts are under `pending-entry-8/`.

**Records.** Receipts, decoded index lines, metadata, audits, keys, manifests and descriptors are in `u2b-records.tar.xz`, with every member pinned in `u2b-records-index.json`.

## Standing

- **Admission.** No source authentication, import admission or Plan.
- **Values.** No SM-5 or SM-7 value; the series are U-2c.
- **Gates.** L-G1 is open, and L is not in effect.
