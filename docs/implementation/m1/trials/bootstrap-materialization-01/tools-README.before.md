# Development tools

Contract generation is an explicit maintenance operation. The current selected profile pins Node24.16.0, a macOS Python3.14 framework interpreter and the separately built Rust generator. It is development tooling, not portable release qualification.

Verify the actual design and source selection first:

```sh
python3 -I -B tools/verify_design.py --architecture ../opensip_arch
```

Check generated files using explicit executables whose bytes match tools/contracts/toolchain.json:

```sh
python3 -I -B tools/generate_contracts.py --architecture ../opensip_arch --output /absolute/fresh/workdir --node /absolute/path/to/selected/node --generator /absolute/path/to/selected/generator --python /absolute/path/to/selected/child-python
```

The child Python path must match both Python profiles in tools/contracts. A macOS framework launcher is not interchangeable with the selected Resources interpreter. The checked-out parent Python runs isolated without optimization. Source, tool and materialized dependency pins are verified before the seven confined generation phases.

Default mode detects missing or changed generated files. Add --write to repair them after complete generation and output collection. Replacement is per file, not an eight-file transaction; a subsequent check detects an interrupted replacement. Unexpected generated members refuse and remain untouched. The public selection-result.json records the verified design/tooling selection; the internal pipeline receipt alone does not establish approval.

Dependencies and tools are provisioned separately. tools/build_contracts.py consumes supplied locked crate archives and an explicit Cargo/Rust toolchain; tools/provision_python.py consumes five supplied pinned wheels. Each supports --help for its explicit inputs. The generator npm package has its own package-lock.json and uses npm11.13.0 with lifecycle scripts disabled. An offline install requires a previously provisioned explicit cache. Ordinary Cargo builds and generation do not download dependencies or build these tools.

The approved TypeScript generator loader policy records one finite local source set, one explicitly unenumerated compiler loader and one guarded optional dependency. It does not grant repository plugin permission or complete dynamic dependency closure. The generic checker/bootstrap commands are still being integrated; do not infer M1 or complete product readiness from successful generation.
