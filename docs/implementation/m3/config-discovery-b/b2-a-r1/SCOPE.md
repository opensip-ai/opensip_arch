# B2-a r1: what the candidate delivers (M3-B unit B2-a, the shared discovery rule)

**Lead scope record, 2026-10-14. Unreviewed candidate.** It implements section 1.2 of the accepted plan `config-discovery-b/b2-a/PLAN-r1.md` (Codex `codex-b2a-plan-r1`). Its base is product `6d425bc`, where the B2-a reference refresh is bound as contract successor 163 (Codex `codex-b2a-reference-r2`, ACCEPT-DESIGN-UNIT, after round 1's B2AREF-1).

## Paths

| Path | Change |
|---|---|
| `crates/security/src/custody/discovery_rule.rs` | **New.** The pure rule. |
| `crates/security/src/custody/discovery_rule_tests.rs` | **New.** Its controls. |
| `crates/security/src/custody/discovery_rule_vectors.json` | **New, generated.** 2,516 reference vectors. |
| `tools/security/discovery_rule_vectors.py` | **New.** The vector tool (the B1-a and B3-a pattern). |
| `crates/security/src/custody.rs` | Declares `#[allow(dead_code)] pub(crate) mod discovery_rule` in the module's existing `include!` form. No export. |

## The rule (plan 1.2)

The rule is one `pub(crate)` function per reference entry point, over internal relative paths:

| Function | Notes |
|---|---|
| `normalize_explicit_root` and `spell_root` | |
| `classify_path` | The outermost anchor across `dependency-tree`, `vcs-tree`, `cargo-build-output` and `opensip-custody-state` |
| `cargo_roots_from_markers` | Parent-first: depth, then bytes |
| `pruned_anchors_from_directories` | |
| `enumerate_units` | `EnumerationInput` carries `enforce_limit`, the observed directories, the basis, the unreadable anchors and the member roots. Rows are `PrunedTreeRow`, and the refusal is `WorkspaceUnitLimit { unit_count }` with no units. |
| `relative_locator` | |
| `classify_boundary` | |
| `classify_custody_exclusion` | |
| `boundary_excluded_prefixes` | Takes the inventory's three fields; the V3 record is B2-b's (LD-B2A-2) |
| `conventional_excluded_prefixes` | Always `.opensip` at the root and at each member root |
| `classify_entry` (new) | `NeverEnter { anchor, recorded }`, where `recorded` is true only for a directory that is the anchor itself; otherwise `Ordinary` (LD-B2A-4, LD-B2A-5) |

**Types and spelling.**
- Member and Cargo roots are `&BTreeSet<String>`. They are borrowed and iterable many times, so the reference's B2AREF-1 hazard has no Rust analogue.
- Segments compare as exact bytes (LD-B2A-6), and outputs come back in UTF-8 byte order.
- No public row is mapped here; that is B2-b's.

## Tests

- **`every_reference_vector_is_reproduced`.** All 2,516 vectors reproduce, and all 11 cross-checked entry points are exercised. It pins the reference's path and SHA-256. The vectors cover:
  - the pruning controls and the SX-1 controls of the refresh checker;
  - a sweep of every path of up to three segments over `a`, `node_modules`, `.git`, `target`, `.opensip`, `src` and `Cargo.toml`, under three Cargo-root and two member settings (2,394 `classify_path` cases);
  - 17 explicit-root spellings, including a trailing `/`, `a//b`, `..`, NUL and backslash;
  - enumeration: 4096 and 4097 units, enforced and not; 4200 installed manifests in both bases; unreadable anchors; non-markers and absolute paths; members;
  - the locators, boundaries, custody exclusions and both prefix functions.
- **The B-S1 SX-1 controls,** in `every_entry_kind_at_an_anchor_is_never_entered_and_only_directories_are_recorded`:
  - every entry kind at `.opensip`, a member's `.opensip`, `node_modules` and `.git` is never entered;
  - only a directory is recorded;
  - `.opensip` elsewhere, at a non-member, below a member, or in another case is ordinary;
  - an entry below an anchor is never recorded.
- **`classify_entry_agrees_with_classify_path_over_the_sweep`,** for both directories and files.
- **The cap.** 4096 admits. 4097 refuses with no units and no truncation. 5000 installed manifests are one row, not counted.
- **Order.** Outputs are sorted and unique.
- **Purity.** No `std::fs`, `std::io`, `std::env`, `std::process`, `std::net`, platform crate, `unsafe` or plain `pub` item. Its `use` line is pinned. The module is under B1-b's environment lint.

## Not claimed (plan section 5)

- **B2-b:** the walker and its trace, the ledger profile, records, public rows and the T2 census.
- **B2-c:** U-0 to U-9 beyond U-4a, and the export.
- **B3-b:** membership.
- **C1:** the read set.
- No law change and no qualification.
