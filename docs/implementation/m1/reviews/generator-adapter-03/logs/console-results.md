# Console-only results (transcribed from executed commands)

## NR2 with real `cargo metadata --locked --offline --filter-platform aarch64-apple-darwin`
Cargo `/opt/homebrew/Cellar/rust/1.95.0/bin/cargo`. The workspace copies are in `work/nr2/`. The policy is
`subjectDeclaredFeatures={}` and `subjectResolvedFeatures=[]`.
- pass (unmodified copy): `dependencyCount 11`, passed
- feature-rc (`[features] reviewer-rc = ["serde/rc"]`): `dependency check refused: unselected declared contracts features`
- feature-empty-local (`[features] reviewer-local = []`): `dependency check refused: unselected declared contracts features`

## Build (`tools/build_contracts.py` from base copy, byte-identical to frozen)
- Ancestor refusal: `work/ancestor/.cargo/config.toml` (rustflags cfg injection) above `TMPDIR=work/ancestor/tmp`
  gives `build refused: ambient ancestor Cargo configuration is not selected`, exit 1. No output is created and no temp dir is left.
- Clean vendor build with `TMPDIR=work/build/tmp` under `sandbox-exec (allow default)(deny network*)` succeeded.
  It used 25 archives. Executable sha256 `6b35cbaf39d0240b219e7a66700304bf764bcce9a20ec2daa91fb1a02f0d3493`, 7201824 bytes.
  The frozen receipt/binary (build-04) is `0a49cfc4…0768e`, also 7201824 bytes. The build is not reproducible, as disclosed.
  The receipt fields equal the frozen receipt modulo temp paths except stdout/stderr/executable (`new-build-receipt-compare.json`).
- build-04 `receipt.json` is byte-identical to the frozen `tools/contracts/build-receipt.json`. The build-04 binary
  hash equals the closure toolchain pin and receipt executable.

## Archives
All 25 `.crate` files in `~/.cargo/registry/cache/index.crates.io-1949cf8c6b5b557f` match the receipt sha256/bytes and
the `tools/contracts/Cargo.lock` checksums.
- Build scripts: prettyplease, proc-macro2, quote, schemars, serde, serde_core, serde_json, thiserror, zmij.
- Proc-macros: schemars_derive, serde_derive, thiserror-impl.
- prettyplease 0.2.37 `build.rs` only emits check-cfg/version lines and reads `CARGO_PKG_VERSION`. Its `src/` has no
  `std::process|net|fs|env`, `include_*!`, `env!` or `Command` use; the only `unsafe` hits are printed keywords.
  Its dependencies are proc-macro2 and syn(full).

## Tool pins
Each matches `generator-closure.json` toolchain sha/bytes:
- generator `/tmp/opensip-implementation/m1-generator-build-04/opensip-contract-generator`
- node `/Users/sb/.nvm/versions/node/v24.16.0/bin/node`
- python `/opt/homebrew/bin/python3` (resolves to Cellar 3.14.6 `bin/python3.14`)

The TypeScript tree copied from `m1-generator-integration-candidate-03` gives 140 files equal to
`typescriptPackageFiles`, both at the origin and in the copy. The generator binary links only `/usr/lib/libSystem.B.dylib`.

## Architecture source-map pins
Checkout `/Users/sb/code/opensip-ai/opensip_arch`, HEAD `c3856824b5084eb9336622e76796c70c64f2523d`.
- All 28 `architectureSource` pins equal the checkout worktree bytes and equal the implementation source bytes.
- Only 6 of the 28 paths are tracked; 3 of those are modified vs HEAD (`native-evidence.schemas.v2.json`,
  workflows `common.schema.json`, `test-execution.schema.json`). 22 are untracked. The pins bind worktree bytes, not a commit.
- `verify_design.py --architecture` passed (`inputsVerified 46`, `productQualification false`).

## Witness corpus
Isolated in `work/witness`, using the frozen 8 outputs.
- The output bodies (after the 3-line provenance header) equal `m1-generator-integration-validation-03`.
- `tsc -p .` (strict, TypeScript 6.0.3 copy) exit 0.
- `check-report.cjs` with frozen options gives `{"selected":586,"deniedProbes":12,"matched":1338}`.
- The Rust `carrier_probe` (release build, offline, locked) gives `rows=1338, failures=0`.
- `carrier-cases.json` sha256 is `d79f78e0…`. It is the declared source `m1-eight-output-trial-02/.../carrier-cases.json`
  (`533f82b7…`) with the 5 superseded Native2 handshake rows removed; all 1343 values are identical.
