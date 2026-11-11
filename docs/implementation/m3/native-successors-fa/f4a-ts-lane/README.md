# F4-a TypeScript lane registry (F4A-TS-LANE-r1)

PROPOSED. A contract successor selecting, by value, the TypeScript lane registry
re-pinned for the carried TypeScript lifecycle source r2: the joined esbuild stop,
awaited disposal and terminal receipt. The registry pins the runtime closure of
the lanes: the checker, its entry point and sources, and the patched esbuild files.
It does not pin test files. The regression harness update and the in-tree lifecycle
controls were reviewed at the product commit this unit names, not bound by the
registry.

- `product/tools/typescript-lanes.json`: the registry, byte for byte the product
  file at f4-carry-r1. Its parent is MG1-LANE-r1's copy
  (`9f7798c4c4b4a3d504e79f5ab39081714594d83bedb76193246abac4aa33f590`).

It adds no exception, target, loader or capability, and it does not change the
loader policy: the provider lane still names MG1-LANE-r1's policy. No product
qualification follows from it.
