# OpenSIP

Implementation of the approved OpenSIP product design. Architecture, reference
models, review evidence and implementation progress live in the sibling
[`opensip_arch`](../opensip_arch/) repository. This repository owns product code,
its schemas, tests and build tools.

`design-lock.json` pins the governing design and approval evidence. Verify it
against an explicit architecture checkout before developing:

```sh
python3 -I -B tools/verify_design.py --architecture ../opensip_arch
```

The implementation is in progress. No release or platform qualification is
claimed. The current milestone and independent review results are recorded in
[`opensip_arch/docs/implementation`](../opensip_arch/docs/implementation/README.md).

The host/CLI, Rust provider, TypeScript provider, browser report and generation
lane have separate build inputs. Packages and modules appear as their actual
behavior is implemented; the approved file inventory remains the directory and
naming guide.

The development CLI currently implements help, version and shell completion:

```sh
cargo run --locked -p opensip-cli -- help
cargo run --locked -p opensip-cli -- version --format=json
cargo test --locked --workspace --all-targets
```

Repository analysis and the complete report application are still being
implemented. Metadata commands do not open project configuration, storage or
provider services. The CLI reports its compiled development build channel.

Reviewed contract generation, drift checks and TypeScript/Cargo package boundary
checks are available. The TypeScript check verifies the selected design and
execution inputs before checking the report, provider and generator lanes.
See [the maintenance tools guide](tools/README.md) for explicit provisioning and
command inputs. This does not complete the analysis engine or release qualification.
