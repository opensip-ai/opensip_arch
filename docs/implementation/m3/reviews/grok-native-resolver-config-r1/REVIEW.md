# NRC-1 conditional resolver configuration members

ACCEPT-DESIGN-UNIT.

The subject manifest is 2134 bytes, sha256 `73d53434371a3b2b2c45f10397fde7ce371ca83d0cfdc3c775bde39e0bfe1053`, with 9 sorted unique members. Product HEAD `af56300cf52a5ab6ed52a4a4a5946c5d766871ab` is clean. Its parent is `5112dc5d0b0d0d1c732086b294c6ca9e82be2a99`, “Bind reviewed GPE-1 Git package eligibility.” Architecture HEAD `b9fd21e156bf5390c6630d5d847745f9b998a73d` has parent `25c527f0ca0bd2b831d17ca3641f4dfb70d195f7`, “Reconcile M3 status after Git package eligibility design bind.” The tracked architecture tree matches that commit. The untracked `docs/implementation/m3/syntax-e/e2s/` tree is outside this unit.

NRC-1 prospectively selects one resolver leaf after the host-owned configuration input, the original logical definitions, and the current workspace association are admitted. This review publishes `resolverConfigMembersSelected` true. The candidate keeps that flag false until acceptance.

## Lock, parent, and selector

The product lock at that HEAD is 600646 bytes, sha256 `5b26d76c5490623a36fdb9fa2fd454e6c1bf7839a5919a8316bfd7b3b32988e5`, schemaVersion 4. It has 130 inventory successors, 150 contract successors, and 103 inventory-passage inheritance rows. The selected inventory is `repository-file-inventory.v170.json`, 639076 bytes, sha256 `6f6b43a8f6f75587864f87705482f7fa5db25e362276fa5fe0cb82e1c0db96ef`. The contract tail is the GPE-1 successor, 4373 bytes, sha256 `6df9fd177ef104cf9dcdcf506abd732ad58abc90a3b41eb2822993023228ca06`. All 150 bound record pins match the architecture tree. The prospective count after this unit is 151. No product path names this unit, and the product work tree has no diff.

The successor names one parent: `native-evidence.md`, 329013 bytes, sha256 `83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0`. That file is the same accepted parent already bound through GPE-1, and the architecture bytes match. `passageSupersessions` is empty. The single override selects line 1755. That line is the configuration sentence that names the two digests and begins the `projectionSha256` clause. The sentence occurs once, and line 1755 is absent from the bound native-evidence selectors. The replacement ends with the same sentence. The following line stays the raw digest of the single projected config file. Section 3.3 still honors `resolver` by name in the projected-key list and does not name `incompatible-rust-versions`, `feature-unification`, or `lockfile-path`. The eleven `source.json` pins match architecture `b9fd21e1`, including the GPE-1 assent unit, inventory 170, and 150 contract successors before this unit.

`CargoConfigProjectionV2` keeps `honoredKeys` and `strippedKeys` at maxItems 64, `replacedSnapshotConfigs` at maxItems 4096, and the two distinct 64-hex digests: raw `projectionSha256` of the projected file, and the 64-hex suffix of the whole-record H. CC-1 through CC-5, C-ENV1, and CRA-1 stay in place.

## Pinned Cargo 1.95 sources

The four files are Cargo commit `f2d3ce0bd7f24a49f8f72d9000448f8838c4e850`. Each staged copy matches its receipt and the GitHub raw bytes:

- `src/cargo/core/workspace.rs`, 98054 bytes, sha256 `fa321dfbd2857f42b4a1dd37054dd749a860f664baa89fc55e76978da32abbd2`
- `src/cargo/util/context/mod.rs`, 99798 bytes, sha256 `30310d878bb05ffed2db0c55699619bb1452834d4db5b2166ec2f2aeceebda62`
- `src/cargo/util/context/schema.rs`, 13580 bytes, sha256 `1451480abec24611eb903347ab6aeeee59f9e57b63b6037f238bbe8bb098958a`
- `src/cargo/util/context/value.rs`, 9413 bytes, sha256 `b3f98b232940c49b061aae7717bd035aa3ce99e1204f3dde2d9d834726786def`

`CargoResolverConfig` has three optional fields: `incompatible_rust_versions`, `feature_unification`, and `lockfile_path`. `IncompatibleRustVersions` deserializes the kebab-case strings `allow` and `fallback`. `FeatureUnification` deserializes `package`, `selected`, and `workspace`. The schema carries no extra enum alias and no unknown-field denial. `context/mod.rs` lists `resolver` among the top-level config keys, loads values through `GlobalContext::get`, and compares definition priority across file discovery, environment, and CLI. `value.rs` distinguishes built-in, path, environment, and CLI definitions.

`Workspace::set_resolve_behavior` first takes resolver version from the workspace manifest, the root package, or the edition default. It then reads `CargoResolverConfig` under `resolver`. When `incompatible_rust_versions` is present, `resolve_honors_rust_version` becomes true exactly for `Fallback` and false for `Allow`. When the leaf is absent, that assignment stays at the workspace and manifest result. The `feature_unification` branch runs only when `cli_unstable().feature_unification` is set; otherwise a present value produces a warning. The `lockfile_path` branch resolves a templated path, requires a `Cargo.lock` file name, and probes whether the path is a directory, only when `cli_unstable().lockfile_path` is set; otherwise it warns.

The selected leaf is `resolver.incompatible-rust-versions` with the exact strings `allow` and `fallback`. Absence keeps that pinned workspace and manifest behavior and does not invent a string. A malformed honored value, a non-table resolver input, or invalid TOML keeps its owning malformed origin. This unit adds no public failure code. Every other actual resolver member, including `feature-unification` and `lockfile-path`, is stripped and disclosed in the existing honored-key and stripped-key accounting. The unit does not resolve a lock template, probe a lock destination, read another `Cargo.lock`, or grant the unstable switches. The upstream member names stay interpretation evidence. The receipts claim no runtime profile and no signed-producer execution.

## Open gates

`sourceProfilePublished`, `ownerMappingPublished`, `actualOwnerAdmission`, `R3Resolved`, `productImplemented`, `productQualification`, and `entirePlanComplete` stay false. Owned effective merge, original logical definitions, the one-time initializer, read-set, deterministic projected bytes, feature state, sealed lock selection, failure assembly, signed profile, source, owner, library, product, and R3 stay open, as do effective L, O7, D3, D13, S-M, held work, ground truth, and qualification. Schema, identity, capacity, provenance, and population stay unchanged. This review did not run `verify_design.py`, `check_publication.py`, `run.py`, or Cargo. Binding still requires this acceptance, root assent, and a current `verify_design`, as separate architecture and lock commits, with no product-code change and no push.
