# Development tools

The product Cargo workspace, Rust provider, TypeScript provider, browser report and contract generator have separate dependency/build inputs. TypeScript packages use npm11.13.0 and independent package-lock.json files in apps/report, providers/typescript, tools/contracts and tools/typescript-boundary. The root package.json coordinates commands; it has no npm workspaces, dependencies or root lock. Installing one lane does not install a sibling lane.

Use Node24.16.0 and the selected Python3.14 development runtime. Tool arguments require explicit executable paths and an architecture checkout. Ordinary Cargo builds do not install npm/Python packages, build the contract generator or fetch report assets. Review changes to schemas, tool closures and loader policies before updating the design lock.

## Check design and boundaries

From the product root:

```sh
python3 -I -B tools/verify_design.py --architecture ../opensip_arch
python3 -I -B tools/check_typescript.py --architecture ../opensip_arch --node /absolute/path/to/selected/node
```

The boundary entry point first verifies the actual design/source approval chain. It then verifies the selected registry, checker/dependency files and Node executable. It checks the current report, provider and generator lanes. These checks do not prove host semantic admission, whole-tooling source purity or complete dynamic dependency closure. The checker itself is a trusted reviewed tool whose execution inputs are pinned; this command does not analyze its own regression harness as a product lane. Generator compiler-loader limitations are explicit in the selected policy and checker output. No caller exception list can replace that policy.

The selected registry records concrete source inputs. Adding a source file requires updating its lane record; the checker refuses undeclared source. A generator policy also pins all declared inputs/config/lock and each exception site, so changes require an updated reviewed policy. Repository JavaScript and plugins are not executed by resolution. Developer tools and system runtime remain trusted.

## Provision dependencies explicitly

Provision a lane with its own lock, after placing the exact required archives in an explicitly chosen npm cache. Use npm ci --offline --ignore-scripts --no-audit --no-fund with that cache and explicit empty user/global npm configs. A missing cached archive fails. The scripts do not fetch a substitute. The generator's Python packages are separately materialized by tools/provision_python.py from five supplied pinned wheel archives; no wheel installer or entry-point script runs. tools/build_contracts.py consumes supplied locked crate archives and an explicit Cargo/Rust toolchain to build the generator with a recorded receipt.

The current Python framework, native libraries, Seatbelt policy and executable pins describe this macOS development profile. They are not portable release qualification. Follow the selected manifests and observed provisioning receipts for exact inputs; do not change hashes just to admit a different installed tool.

## Regenerate contracts

```sh
python3 -I -B tools/generate_contracts.py --architecture ../opensip_arch --output /absolute/fresh/workdir --node /absolute/path/to/selected/node --generator /absolute/path/to/selected/generator --python /absolute/path/to/selected/child-python
```

The child Python path is explicit: macOS sys.executable may report a different launcher. Generation verifies the exact selected closure, snapshots inputs and runs seven confined phases. Default mode checks drift and returns nonzero for changed or missing generated files. Add --write to replace changed outputs after complete collection. Replacement is per file, not an eight-file transaction. Unexpected generated members refuse and are preserved; interrupted replacements are caught by the next check. No packages are provisioned or tools built implicitly.

## Checker regression tests

After explicitly provisioning tools/typescript-boundary, run its npm test script. The current regression profile requires macOS and Node24.16.0 and executes234tests, including real CLI aliases. Historical/synthetic approval records are test fixtures only. The runner creates and removes a disposable harness directory; capture stdout/stderr to inspect a failure. These tests do not constitute fresh blind consumer or release approval.

The full report application, provider protocol/runtime, release asset assembly and other milestones are still being implemented. Package/bootstrap selection does not represent feature completion.

## Cargo package boundaries

After design verification, capture fresh metadata from the exact workspace using the selected Cargo1.95.0 executable. Provision missing locked crate archives explicitly before this offline operation. The checker is read-only; it does not authenticate caller-supplied metadata or choose an inventory itself.

```sh
cargo metadata --locked --offline --format-version 1 > /absolute/fresh/cargo-metadata.json
python3 -I -B tools/check_package_edges.py --repository . --metadata /absolute/fresh/cargo-metadata.json --inventory ../opensip_arch/docs/implementation/m1/repository-file-inventory.v8.json --lane host
```

The inventory argument must be the selected inventory reported by the preceding design verification. Current manifests are compared with metadata, including inactive optional, target, build and dev declarations. The separate Rust-provider workspace uses its own metadata and `--lane rust-provider` once implemented. This is an internal dependency check; macro expansion, source inclusion, build-script effects, external feature closure and release target qualification remain separate obligations. Run `python3 -I -B tools/tests/test_package_edges.py` for the14regression groups and `python3 -I -B tools/tests/test_typescript_check.py` for wrapper helper regressions. The Cargo test process must have the selected Cargo executable on PATH.

## Platform entropy backend guard

The platform build refuses an effective `getrandom_backend` cfg override, including compiler flags or Cargo config. The pinned dependency chooses its target default. This does not authenticate the compiler or qualify every platform/backend fallback; those remain build/release obligations.

Run `python3 -I -B tools/tests/test_entropy_backend.py --cargo /absolute/path/to/selected/cargo` for five actual locked offline Cargo controls in a disposable checkout/target. Provision the selected crate archives first. These tests do not fetch dependencies and do not edit the original checkout.

## Contracts dependency and source profile

After design verification, use the selected contracts policy and explicit Cargo/target:

```sh
python3 -I -B tools/check_dependencies.py --manifest Cargo.toml --target aarch64-apple-darwin --cargo /absolute/path/to/selected/cargo
python3 -I -B tools/tests/test_dependency_policy.py --target aarch64-apple-darwin --cargo /absolute/path/to/selected/cargo
```

The command captures fresh locked offline target-filtered metadata. It checks the11reviewed dependency checksums and resolved features, the library-only production target, and eight exact local manifest/source pins. Unknown source files, symlinks, nonregular entries and byte changes refuse. This gates changes to the reviewed inert source set; it does not prove arbitrary native code pure, rehash all extracted registry trees, authenticate the compiler, or grant semantic admission. Generation drift remains a separate check. The caller must select the reviewed policy (default tools/contracts/dependency-policy.json); this helper does not authenticate arbitrary caller policies or Cargo executables. Other targets and the independently locked provider need their own matching build qualification.
