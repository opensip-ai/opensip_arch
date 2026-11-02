# F1-a provider lane selection (F1A-LANE-r1)

PROPOSED. A contract successor selecting, by value, the loader policy and the lane registry the F1-a provider lane binds. It follows the generator-policy
precedent (native-owner-generator-loader-policy-r1), carries the adopted law by value (the X10 GA precedent), and adds no exception, target, loader or
capability. No product qualification, F1-b or F1-c acceptance, or runtime grant follows from it.

- `provider-loader-policy.json`: the adopted policy 8e660469 re-pinned to this head's bytes. Rows: 54 unchanged, 23 changed, 1 removed, 2 added (`audit.json`).
  Its only non-pin change is the gen-ts-enums reason owed at selection: digest, then load, then version. compiler.ts's record is byte-for-byte the adopted one.
- `product/tools/typescript-lanes.json`: the provider registry, parent `75816e0d41a256e7cf92d31f1a27abb3ddec5fec96e6a3ea969314798521a3bf`. Against its parent it adds the provider lane's inputs, names the policy in that lane's
  `toolPolicy`, and moves two checker pins (D-1). The other 158 pins and the Node pin are unchanged.
- `law/`: the adoption, the R3 review, the draft, the adopted policy, D-1's diff, and the corrections owed at selection (`CORRECTIONS-r1.md`).

Carry CP-F1C-COMPILER-VERIFY stays open, in all five parts. It is checked at F1-c's review.
