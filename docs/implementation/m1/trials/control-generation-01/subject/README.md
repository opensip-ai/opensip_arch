# OpenSIP

Implementation of the approved OpenSIP product design. Architecture, reference
models, review evidence and implementation progress live in the sibling
[`opensip_arch`](../opensip_arch/) repository. This repository owns product code,
its schemas, tests and build tools.

`design-lock.json` pins the governing design and approval evidence. Verify it
against an explicit architecture checkout before developing:

```sh
python3 tools/verify_design.py --architecture ../opensip_arch
```

The implementation is in progress. No release or platform qualification is
claimed. The current milestone and Claude review results are recorded in
[`opensip_arch/docs/implementation`](../opensip_arch/docs/implementation/README.md).

The host/CLI, Rust provider, TypeScript provider, browser report and generation
lane have separate build inputs. Packages and modules appear as their actual
behavior is implemented; the approved file inventory remains the directory and
naming guide.
