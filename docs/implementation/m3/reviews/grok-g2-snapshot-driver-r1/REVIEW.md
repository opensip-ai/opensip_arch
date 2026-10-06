# G2 snapshot/source-loader/real-driver authoring composition r1 — ACCEPT

This accepts the owned authoring evidence that runs the accepted snapshot join through the accepted source loader and into one real `FileLoader` driver. Full G2, G2-v launch, and product qualification remain open.

## Subject

The evidence archive is `/tmp/opensip-implementation/g2-snapshot-driver-stage`. Its subject manifest is 2666 bytes, sha256 `6ee1405fe66b61a2ddeaae8378ff7aeef67461bea0be3bcd2a4a69e4958ee9bb`. All thirteen listed members match that manifest. The manifest file is the only staged file outside the list. No inventory candidate and no design-lock bind are in the archive.

Product `HEAD` is `59389ba7cab1768c94bbc85d4807bb72113a391a` and is clean. Architecture `HEAD` is `a8db85feaa847e383d7895a833719232643bf9cd`. The bound v157 and v158 unit records match the subject pins. Inventory v157 remains 604664 bytes, sha256 `a4a327db896a68e359c8a099aa328176d0152f0e8cd0d176651c5b20a58385fe`. Inventory v158 remains 605254 bytes, sha256 `db650c79d493c833179c3a5e5e4a73d4eef7a7879545fb9e55be249e05f5ca34`.

The twenty-five source pins match the clean product tree and the `checks.json` pin list. They are the three accepted G2 modules, both Cargo manifests, `Cargo.lock`, and all nineteen `crates/identity/src` Rust files. `providers/rust/src/lib.rs` remains the accepted 194-byte crate root, sha256 `0d0da199a847df62346ed942881cb17834bedf85c83e787b8513b6e1f96645e3`. `providers/rust/src/main.rs` still writes the development-build refusal and returns `ExitCode::FAILURE` before reading a request. The provider package manifest and lock are unchanged. The accepted loader and snapshot-join sources were not re-reviewed.

## Composition

`snapshot-driver.rs` is 5909 bytes, sha256 `7aca6c967c2c2d53caff805af0004d5d82c93c0f240e78d1c6cb8654a9100bb9`, and matches both retained authoring copies. It path-includes the three accepted modules, builds `RegisteredSchemas` from the public `source_requirements` documents, and calls `from_snapshot`. The positive fixture has four in-memory rows: `helper.rs`, `lib.rs` (`mod helper`), `notes.md`, and empty `zero`. On success it checks that `lib.rs` is absent from the namespace directory, installs the `SealedSource` in `Config.file_loader`, and `after_analysis` prints `VERIFIED_SNAPSHOT_AFTER_ANALYSIS` and returns `Compilation::Stop`.

The five hostile modes return before `rustc_driver::run_compiler`. Tampered bytes expect `BlobDigest`. A removed blob expects `MissingBlob`. A declared length one past the retained bytes expects `BlobLength`. A `scopeDigest` change under the already computed snapshot id expects `ObjectIdentity`. A `notes.md` file with a `notes.md/child` row expects `Namespace` and `InvalidInput`. Each prints `REFUSED_BEFORE_COMPILER:` plus the mode name and returns. Those are harness assertions with process exit 0, not a wire outcome or a product exit-status selection.

## Retained run

The reviewer did not run Cargo, rustc, or the script. `checks.json` completed at `2026-10-06T16:50:57.120474+00:00` on scratch `/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T/opensip-g2-composition-ci7mu4ug`, with `laneOwned` true and `nice` 10. `T1ProducerRan`, `providerLaunched`, `analyzedRepositoryCodeExecuted`, `fullSnapshotAdmission`, `nativeContextAdmitted`, `confinementClaimed`, `productionToolchainSelected`, and `productQualification` are false. `~/Library/Application Support/OpenSIP` was absent at this review. No `HOME` assignment was made.

`identity-build.log` is the offline `opensip-identity` compile and its trusted dependencies, finished in 1.26s, exit 0. The script sets that Cargo invocation's `RUSTC` to the official sysroot compiler. `wrapper-build.log` is empty. The wrapper compile uses that same compiler, `-D warnings`, `/usr/bin/cc`, and `RUSTC_BOOTSTRAP=1` only for the wrapper. Analysis uses the environment with bootstrap removed. The six run logs are exactly the expected single lines: positive `VERIFIED_SNAPSHOT_AFTER_ANALYSIS`, and the five `REFUSED_BEFORE_COMPILER` lines. The namespace directory is still empty.

The retained artifacts match their pins: `snapshot-driver` 1606896 bytes, sha256 `09f2fe49c19e9203aab81de9758dc3dd26de7ede65aad70b6744f80a9635a997`; `libopensip_identity-d9b80b1cef50e4b8.rlib` 14360424 bytes, sha256 `6da8fbbc6374deb15df045bc3835efdd4b4ad43b613fbec5b1654fe2a74a95e3`; sysroot `rustc` 412504 bytes, sha256 `b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c`. The three cached official 2026-04-16 archives match the accepted S-P pins recorded in `acquisition.json`. That distribution is authoring toolchain evidence. It selects no production toolchain.

Full snapshot capture, configuration, scope, and VCS admission, native context, signed closure, metadata and environment sealing, repository-code prevention, prepared substitution, provider launch, O7, D1b, G2-v, T1, and product qualification remain open.
