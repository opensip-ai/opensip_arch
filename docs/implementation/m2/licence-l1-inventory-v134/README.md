# Licence L1 inventory134

Adds exactly one file to inventory133 (unit X9-5, selected at product 8dcfe37 and still at 91cb45a, where X9-4 landed with no inventory successor; D1's thirty-nine overrides and D2's four supersessions are already folded into its fifty-five inheritance rows):
- LICENSE

It keeps all 967 existing rows by value, along with the packages and dependencies, the pending decisions and the carried unresolved obligations, for 968 planned files.

The row belongs to unit L1, which adopts the Apache License, Version 2.0 (owner decision D14, 2026-10-03, recorded in `docs/implementation/m3/analysis-quality/PLAN.md`).

- **LICENSE (documentation, package `repository`).** The canonical apache.org text, byte-identical to this repository's root `LICENSE`: 11358 bytes, sha256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`. It is not a runtime input.

**Changes to existing rows.** Every row is kept by value. Each description below stays true.
- **Eleven Cargo manifests** (`apps/cli`, the nine crates under `crates/`, and `providers/rust`) gain `license = "Apache-2.0"` in `[package]`, written in each manifest's own spacing. The workspace has no `[workspace.package]`, so the field is per crate. No `[features]` table, dependency or target changes.
- **Three package.json files** (root, `apps/report`, `providers/typescript`) gain `"license": "Apache-2.0"` after `"private": true`. Their lockfiles are unchanged.
- **README.md** gains a Licence section.
- **`tools/contracts/dependency-policy.json`** and **`tools/identity/dependency-policy.json`**: each one's `localSources` pin of its crate's `Cargo.toml` takes the new bytes and sha256, by a hand edit. No generator writes these policies, and no live check pins the policy files themselves.

**Not changed (lead decision, option A).** `tools/contracts/Cargo.toml`, `tools/contracts/package.json` and `tools/typescript-boundary/package.json` keep their bytes. They are pinned by the generator closure, the generator build receipt and the TypeScript lane registry, each selected by an accepted contract successor. They gain the field with the next closure or lane-registry successor.

**No new edge.** The row belongs to the `repository` package, which declares no dependencies. The builder asserts this.

**Order.** Its parent is the inventory the real product lock selects: inventory133 (unit X9-5) at product 91cb45a. Succession is by the lock's parent pin. `evidence/build_v134.py`:
- reads the parent from the lock;
- checks each inheritance row against the lock before carrying it;
- writes only its two paths;
- refuses tracked paths, and refuses while a lock selects inventory134.

Reruns reproduce the same bytes.

**Projection.** The fifty-five effective description overrides the lock binds to inventory133 stay bound by stable file path: the sixteen carried from inventory81 onward and D1's thirty-nine, with D2's four supersessions already folded. Only the selectors after the inserted row move. No contract successor bound at 91cb45a names inventory133 as a supersession parent, so nothing new is folded.

- `verify_projection.py` is inventory133's helper, with its comment updated for this parent. It runs against the real lock at 91cb45a: PASS, 55 rows, 278 corruptions refused.
- `evidence/verify_scratch.py` appends inventory134 in memory over the L1 worktree's lock. It replaces the inheritance rows with the record's fifty-five, and supplies a synthetic review and assent.
