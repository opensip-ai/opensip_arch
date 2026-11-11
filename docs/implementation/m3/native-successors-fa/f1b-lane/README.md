# F1-b TypeScript provider lane selection (F1B-LANE-r1)

PROPOSED. A contract successor selecting, by value, the provider loader policy re-pinned to the F1-b provider worker delta (native-context recomputation, `CONTEXT_CAPABILITY` true in the worker), and the lane registry that names it. It adds no exception, target, loader or capability.

- `provider-loader-policy.json`: MG1-LANE-r1's policy with 14 row digests re-pinned to product `2eee585c` (`audit.json` lists them). No row added or removed; the two exception digests (gen-ts-enums.mjs, compiler.ts) are unchanged.
- `product/tools/typescript-lanes.json`: the registry, byte for byte the product file. Its parent is F4A-TS-LANE-r1's copy; the only difference is the provider lane's `toolPolicy`.

The code was reviewed separately (REVIEW-F1B-CODE-r2, accepted at c3504d02). No product qualification follows from this unit.
