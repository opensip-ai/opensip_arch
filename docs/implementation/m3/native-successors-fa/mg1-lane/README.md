# MAIN-GENERATE-1 provider lane selection (MG1-LANE-r1)

PROPOSED. A contract successor selecting, by value, the re-pinned loader policy and the lane registry after 8 non-recipe modules move from `src/generated/` to `src/embedded/`, so that `tools/generate_contracts.py` passes on main again (LD-Q-304). It adds no exception, target, loader or capability. `CONTEXT_CAPABILITY` stays false. No product qualification, F1-b or F1-c acceptance, or runtime grant follows from it. F1A-LANE-r1's policy and registry stay at their own paths.

- `provider-loader-policy.json`: F1A-LANE-r1's policy re-pinned to this head's bytes. Rows: 52 unchanged, 19 changed, 8 removed, 8 added (`audit.json`). Its only exception change is gen-ts-enums.mjs's digest, by the coordinator's receipt (LD-Q-305). compiler.ts's record is byte for byte the parent's.
- `product/tools/typescript-lanes.json`: the provider registry, parent `d0c2f327e841c7c92bed5f5d539460b2216b35204fd07d8fa579b51776f2f17e`. Against its parent it renames the 8 lane inputs and names this policy in the provider lane's `toolPolicy`.
- `law/`: the plan, its review, the code review, the rulings and the receipt.

Carry CP-F1C-COMPILER-VERIFY stays open, in all five parts.
