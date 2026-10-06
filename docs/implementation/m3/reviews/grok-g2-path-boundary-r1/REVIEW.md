# G2 owned source-path boundary authoring controls r1

Verdict: ACCEPT.

Five rustc-private controls exercise the accepted `SealedSource` loader and the `FileLoader` bridge in `compiler_adapter.rs`. `Config.file_loader` is installed in `config` before the input is read. The positive control returns `Compilation::Stop` from `after_analysis`. The four negative controls stop at source loading. This archive does not change product code, inventory, or the design lock, and it does not claim confinement, metadata sealing, a signed production sysroot, provider launch, full G2, or qualification.

## Controls

The subject manifest is 2246 bytes, sha256 `4a3adfd62ca461e7e5bbdd2f43ebcddfb2e771d87522d40c7bc091154488cc52`. All eleven archive members match it. `checks.json` records six `nice -n 10` commands. `RUSTC_BOOTSTRAP` is set only on the wrapper build and removed before the five analysis runs. The wrapper uses `--edition 2024`, `-D warnings`, the cached sysroot, and `linker=/usr/bin/cc`. The scratch root remains mode `0700`.

`wrapper-build` exits 0 with an empty log. `root-shadow` exits 0 and prints only `SEALED_AFTER_ANALYSIS`. The virtual `lib.rs` and `helper.rs` are the admitted bytes; the physical files at those paths still contain `compile_error!("AMBIENT_ROOT_SHADOW")` and `compile_error!("AMBIENT_HELPER_SHADOW")`. Neither sentinel appears in any log.

The other four controls exit 101. `absolute-text` cannot read the absolute `external.txt`. `escape-binary` cannot read `../external.bin`. `path-module` cannot read `../external.rs`. `disk-symlink` reports E0583 for `mod alias` and does not follow the physical symlink. None of those logs contains `SEALED_AFTER_ANALYSIS`. The retained scratch still holds `OWNED_EXTERNAL_TEXT`, `OWNED_EXTERNAL_BINARY`, and `pub fn value() -> u8 { 23 }`, `alias.rs` still points at `external.rs`, and the output directory is empty. Those exit codes and diagnostics stay prototype driver observations.

## Pins

`sealed_vfs.rs` is 7814 bytes, sha256 `20e7bd8bc9192a12e6bfe908433ec0db3ffbfb864927739c5815784c0cc49d27`. `compiler_adapter.rs` is 1012 bytes, sha256 `0e97afd6b86988d2a50d4652c6246ced7c0cfd2fc3314a3ed4d5be8c1eedfa44`. Both commits `fd8eaff8f781552b4e5b6b830be2f74ca5a9a1e7` and `0cc355582b4dde21b7282b7061d879bd141d2eab` have those bytes. `0cc3555` descends from `fd8eaff`. The staged driver, the authoring driver, and the retained `path-driver` binary match the artifact pins (184440 bytes, sha256 `b95ca556f5c5ca28ce09b1913e164194fc62f1454466c7a6ffdee8871ac27af4`). `sysroot/bin/rustc` is 412504 bytes, sha256 `b829b733131d4e1673eeebd1f34d06ae1e9ff4977b051313cf42e2a9e79ecf1c`.

The three cached official 2026-04-16 `aarch64-apple-darwin` archives match the accepted S-P pins and this `acquisition.json`: rustc 67652240 / `149e85a285b6eba58eb6c8bdf7deb1b93763890598e62cb635a712e3a8454f04`, rust-std 27317176 / `9b30089b0f767cb91b2190ffec55a9beeb2a21a1405d8da0f664d7e09d08e6d8`, rustc-dev 118646732 / `c9f65810f625b8435c2d4e8486340f93f03f3d7393b4ee2c22865f2444298e48`. The v157 unit, snapshot-driver manifest, and S-P subject match their pins. Acquisition standing is authoring toolchain only. The unsigned sysroot still exposes metadata, dylibs, and the environment outside this source boundary.

This review did not run the wrapper, compiler, Cargo, formatter, producer, acquisition, tests, or network commands, and it did not inspect a corpus tree. Installation is absent. `fullG2Complete`, `providerLaunchAuthorized`, `productQualification`, and `confinementClaimed` stay false.
