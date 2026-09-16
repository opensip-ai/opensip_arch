# Admission inventory v11 — additive layout review

**Verdict: `ACCEPT-UNIT`**

Not runtime acceptance. Not a Claude claim. Frozen/live/history not edited. Code-unit review waits on private integration.

Subject `docs/implementation/m2/admission-inventory-v11-subject.json` SHA-256 `79ef7b0c6d881a1a4a46170e421507f100cc4f43d2a5084f4903a3210aa88d9c` (622 bytes). Three members pin-match: README, `successor.json`, `repository-file-inventory.v11.json` (127200 bytes, `0ae9d439…`).

## Parent is live inventory 10

Live 8/12 lock (`m2-exact-profile-activation-01/product/design-lock.json`: 8 inventory successors, 12 contract successors) last inventory **candidate** is:

`docs/implementation/m1/repository-file-inventory.v10.json` 121810 bytes SHA-256 `6608fabd31f1fb89feb565ad5b930c4be49f096a30dd92ecdc21466251fd8bc9`

That is exactly this unit’s `successor.parent`. Admission-runtime candidate lock uses the same last inventory pin. Parent artifact bytes are the accepted current inventory.

## Candidate assessment: **ACCEPT**

| Claim | Check |
|---|---|
| 333 inherited rows | v10 has 333 unique paths; all present in v11; **0 mutated** (byte-equal row objects) |
| 15 new files | identical to `successor.addedFiles`; none removed |
| 348 total | 333+15 |
| 20 packages / DAG | `packages` and `pendingDecisions` identical; no cycles; contracts remain leaf (`[]`); **host already lists `opensip-identity`** |
| v10 path order | v10 paths are a subsequence of v11 (insertions only) |

New ownership matches the README:

- Identity: `schema.rs`, `schema_patterns.rs`, `schema_registry.rs`, `schema_tests.rs` (package `opensip-identity`; interpreter/registry/test — not a second descriptors owner). Existing `descriptors.rs` / `lib.rs` rows unchanged.
- Host: `schema_sources.rs` (`opensip-host`, adapter: compiled raw documents, no path lookup/fallback).
- Shared assets: `admission-registry.json`, `admission-source-map.json`, plus **8** `schemas/sources/*` admission-only schemas (generation `registry.json` / `source-map.json` still present; schema source count 40→48).
- Source-guard edits stay on existing `tools/verify_design.py` and `tools/tests/test_design_binding.py` (not new files). No new package or factory.

Successor record shape matches the last accepted inventory successor (`parent` / `candidate` / `addedFiles` / `inheritedRowsEqualByValue`). Standing is layout-only.

## Three inherited description overrides

Live lock `inventoryPassageInheritance` still points at **v10 indices** `/files/7|13|158/description` (`bootstrap.rs`, `apps/report/package.json`, root `package.json`). v11 copies the **parent (before) text**, not the after-text. `package.json` moves **158 → 163**. Activation must project those three by **stable file path**, not old jsonPointers. This candidate does not bake overrides into inherited rows.

## requiredFindings

None.

## Scope / limits

No product files created here. No runtime, replay, report, native, or release claim. Next: code unit once private integration exists.
