# Author reference package — native-v2 migration (successor of package15)

Built by `rebuild-author-package.v2.py` from package15 constructors plus the `author-package-migration.v1` overlay, on a CAPTURED successor source (`source-manifest.json`). The package15 exports are kept unchanged under `historical-source38-before-native-v2/`. No old export was repaired, re-serialized or imported. Every export here was reconstructed from inputs by constructors.

Migrated laws (helpers `author-helpers/native_v2.py`, `runs.py`, `ts_pilot.py`; finalizers in the two normalized/Rust-selection constructors):
- **S1 stage output registration.** Each provider closure registers `opensip-interface/stage-output/<operation>.schema.json`, and `outputSchemaDigest` is that member's digest.
- **S2 per-level normalization maps.** They live in the interpreting TypeScript toolchain, Rust toolchain and syntax grammar closures, next to their level specifications.
- **S4 account targets.** Every account's `targetUniverse` is null.
- **U-4b / U-9 membership.** Units and rows are deterministic, including the Cargo workspace member roots and the syntax-only fallback unit.
- **Schema digests.** The registered native and enumeration-plan schema digests are read from the declared kit.

Run `verify-package.py --source <frozen-successor> --out <new-dir>` with the reference interpreter `-I -B`. It covers all 17 structural and full semantic closures and the 7 query checks:
- 7 positives;
- 3 semantic controls;
- 3 binding controls;
- 4 S2 map controls, which must refuse structurally at their recorded boundary.

`probe-native-v2.py` records author self-consistency evidence over owner functions.

**Limits, unchanged and still pending.**
- Only the TypeScript checkpoint compares a partial consumer helper with the owner. The other positives are author-derived self-consistency under owner replay.
- Helper operators: exists/none are exercised; and/or/not are unexercised; count-at-most/all-covered are unimplemented.
- The two-binding construction is incomplete, with a single explicit binding.
- No compiler, provider, OS or process-isolation qualification.
- All 30 independent residual grades remain PENDING.
- This is not frozen-candidate acceptance and not a whole-source review.
- This author evidence must never be supplied to a blind consumer.
