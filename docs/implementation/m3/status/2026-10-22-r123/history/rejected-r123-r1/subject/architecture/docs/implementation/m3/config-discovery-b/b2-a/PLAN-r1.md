# B2-a implementation plan r1 (M3-B unit B2-a: the shared discovery rule)

**Lead plan record, 2026-10-14; r1. Not law, not code.** B2-a may start at day 0: P0 and L are met, and SX-1 is bound with B-S1. Product is at `2191674` (B1-a, B1-b and B3-a bound; inventory v190; 162 contract successors). Codex reviews this plan before any reference or code is written.

**Authority.**
- **M3-B r5** (`config-discovery-b/PROPOSAL-r5.md`, cited as MB):
  - item 13, the S3 boundary: "B2-a provides the shared rule (item 14, U-4a) as **one** pure implementation, `crates/security/src/custody/discovery_rule.rs`";
  - item 14's U-4a row: "The shared rule, from B2-a only";
  - the B2-a row of "Units after the law": "the shared rule (U-4a; DD's entry points)", the SX-1 anchor, and the DD reference refresh for that anchor and D15's `memberRepositories` (BS1 LD-14, BS1-F3);
  - "Controls the bound design units add".
- **B-S1** (bound, contract successor 78):
  - SX-1 (README §1; LD-3; LD-4);
  - the passages SL:195, SL:205 and SL:215;
  - NE:714, NE:719, NE:730-731, NE:939 and NE:940;
  - LD-14 and BS1-F3;
  - "Controls owed by the implementing units" (B2-a row).
- **NE §1.4 U-4a** (NE:703-743, as B-S1 overrides it). It is normative: "where the two disagree, this text governs".
- **SL S3** (SL:187-250), the shared rule, explicit roots and the depth bound.
- **The discovery pruning reference correction r2** (contract successor 124, ACCEPTED-DESIGN-UNIT). Its copy `discovery-pruning-reference-r2/reference/discovery-defaults.pruning-r1.py` corrects `classify_path` and `cargo_roots_from_markers`: the outermost anchor wins across every reason, and Cargo roots derive parent-first through the full classifier. Its parent, the original `docs/coop/design-corrections/discovery-defaults.py` (DD), is kept as a before-image only.

## 0. What exists (product `2191674`)

- **`crates/security/src/custody/discovery_rule.rs`.** Absent. It is not an inventory row: v190 plans `crates/host/src/discovery.rs`, `crates/host/tests/discovery_tests.rs` and `crates/security/src/custody.rs`, but not this path.
- **No product code implements any part of the rule.** No discovery provenance or boundary record is produced.
- **The only generated discovery types** are native V1 (`Native2AdmittedBoundaryInventoryV1`, `Native2PrunedTreeV1` in `contracts/src/generated/evidence.rs`). B-S1's V3 records are schema fragments (`b-s1/schemas/*-additions.json`) that the product units materialize.
- **B1-a's resolver** already refuses a Config2 logical path with a trailing `/` (`configuration.rs:640-645`), as SL:228-232 requires: "a Config2 value spelled with a trailing `/` is refused earlier".
- **The reference.** The live DD is still the uncorrected version 2. The corrected pruning copy is still version 2, without SX-1 or V3.

## 1. What B2-a delivers

B2-a has two deliverables in sequence, and this plan covers both. The steps are in section 4.

### 1.1 The reference refresh (owed by BS1-F3 and LD-14): a design unit

A new reference copy, `config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py`. Like the pruning precedent, it is a separate file: DD and the pruning copy keep their bytes.
- **Base.** The corrected copy `discovery-defaults.pruning-r1.py`, byte for byte, then exactly these changes:
  - `DISCOVERY_DEFAULTS_VERSION = 3`.
  - **SX-1.** The constant `OPENSIP_CUSTODY_STATE = '.opensip'` and the reason `opensip-custody-state` appended to `PRUNE_REASONS`.
  - `classify_path(relpath, cargo_roots, member_roots=())` adds the exact anchor `.opensip` at `""` and at each member root, and keeps the outermost-anchor rule across all four reasons.
  - `cargo_roots_from_markers`, `pruned_anchors_from_directories` and `enumerate_units` gain `member_roots=()` and pass it through.
  - `conventional_excluded_prefixes(unit_roots, cargo_roots, member_roots=())` always adds `.opensip` at the root and at each member root (LD-3).
  - **D15.** `boundary_inventory_from_provenance` converts a `DiscoveryProvenanceV3` into an `AdmittedBoundaryInventoryV3`: `schemaVersion` 3, V3 pruned rows, and `memberRepositories` (relative, at most 64, UTF-8 order). `CURRENT_PROVENANCE_VERSION` and `BOUNDARY_INVENTORY_VERSION` become 3, and the supported tuples gain 3. A V2 record refuses as `PROVENANCE_VERSION_UNSUPPORTED:2`, under the DD's existing two-lane rule: reading is not converting.
- **Its checker** (`evidence/check.py`, in the pruning precedent's form):
  - reruns all 49 pruning controls against the new copy, with every result unchanged;
  - adds the SX-1 controls (section 3) and the V3 converter controls;
  - validates each converter output against B-S1's `AdmittedBoundaryInventoryV3` fragment, merged into its pinned base bundle;
  - proves by AST comparison with the pruning copy that only the named functions and constants changed.
- **Not overridden.** No passage, schema or bundle changes, and DD itself is untouched. SLM and the native model keep importing DD: BS1-F3 owes a refresh of DD's reference, not of its consumers.
- **Publication.** Codex reviews it as ACCEPT-DESIGN-UNIT. It is published arch-only and bound as contract successor **163** (precedent: successor 124).

### 1.2 The product rule: `crates/security/src/custody/discovery_rule.rs` (pure)

One implementation of U-4a and DD's entry points, over relative logical paths (`&str`, internal form with `""` for the root). It has no I/O, no environment and no platform types, and every output order is UTF-8 byte order (`str` `Ord`).

| Function | Reference | Obligation |
|---|---|---|
| `normalize_explicit_root(&str) -> Result<String, RootGrammar>` | DD:80-92; SL:224-232 | `.` → `""`. One trailing `/` dropped. Absolute, backslash, NUL, empty, `.` or `..` segment refuses. |
| `spell_root(&str) -> &str` | DD:95-97 | `""` → `.` |
| `classify_path(relpath, cargo_roots, member_roots) -> Option<PrunedAnchor>` | pruning-r1, plus SX-1 | Exact segments, never substrings. The outermost anchor across `dependency-tree`, `vcs-tree`, `cargo-build-output` and `opensip-custody-state`. `.opensip` only at `""` and member roots. |
| `cargo_roots_from_markers(markers, member_roots)` | pruning-r1 | Parent-first (depth, then bytes), through the full classifier: no marker inside any pruned tree makes a root. |
| `pruned_anchors_from_directories(dirs, cargo_roots, member_roots)` | DD:104-126 | Anchors from the directory observation alone; no descent. |
| `enumerate_units(markers, options) -> UnitEnumeration` | DD:164-237 | Units are the marker directories outside pruned trees. Pruned rows carry `(path, reason, markerCount, markerCountBasis)`, with `not-enumerated` → `None` and per-row unreadable anchors. More than 4096 units is the typed `WorkspaceUnitLimit { unit_count }` with no units: no truncation, and dependencies are never counted. |
| `relative_locator(selected_root, absolute)` | DD:248-262 | `LOCATOR_OUTSIDE_ROOT`, `LOCATOR_GRAMMAR` |
| `classify_boundary(path, nested_repositories, nested_projects)` | DD:318-328 | Repositories first |
| `classify_custody_exclusion(unit_dir, marker, rows)` | DD:331-341 | `MARKER_CUSTODY:` exact; otherwise at or below |
| `boundary_excluded_prefixes(...)` | DD:344-351 | Members add no prefix (NE:940) |
| `conventional_excluded_prefixes(unit_roots, cargo_roots, member_roots)` | refresh | Includes `.opensip` at the root and at each member root, always (LD-3) |
| `classify_entry(relpath, kind, cargo_roots, member_roots) -> EntryDisposition` | SX-1; SL:195 | **New, the walker's per-entry decision.** A pruned anchor is `NeverEnter { anchor, reason, recorded }`, where `recorded` is true only for a directory. Otherwise the entry is `Ordinary`. The anchor is decided from the parent's listing, before any open (B-S1: "observed only as an entry of its parent directory and never opened or listed"). |

**Typed outputs.** These are rule outputs, not schema records:
- `PruneReason` is a closed enum, and its `as_str` gives the four spellings.
- `PrunedTreeRow { path, reason, marker_count: Option<u64>, basis }`.
- `UnitEnumeration { unit_dirs, pruned_trees }` or `WorkspaceUnitLimit`.
- `RootGrammar` and `LocatorRefusal`.
- No public row is mapped here. `JOIN_PATH_GRAMMAR`, `JOIN_INSIDE_PRUNED_TREE:<reason>:<anchor>` and `PROJECT.WORKSPACE_UNIT_LIMIT` are B2-b's projections.

**Member roots.** Every SX-1 function takes the admitted D15 member roots (`&BTreeSet<String>`, internal relative form). Until B3-b admits members, callers pass the empty set. B2-a never decides membership.

## 2. Lead decisions

**LD-B2A-1. The refresh is a separate reference copy, reviewed as its own design unit before the code.**
- The B1-a vector pattern needs an accepted reference to generate from. NE:708-710 makes DD the reference, and BS1-F3 owes its refresh.
- The pruning precedent keeps DD's bytes and adds a corrected copy, bound as a contract successor. The refresh follows it, layered on the corrected copy, so the refreshed reference carries both corrections.
- **Rejected:**
  - **editing DD in place.** It is pinned by the accepted candidate subject, and SLM and the native model import it.
  - **code first, reference after.** The product would have no cross-implementation check.
  - **one combined review.** A design artifact and product code have different acceptance types.

**LD-B2A-2. The provenance and boundary records are B2-b's.**
- B2-a gives typed rule outputs and `relative_locator`. The V3 record types, `boundary_inventory(result)` and their materialization from B-S1's fragments are the instrument's (MB item 13 table; the B2-b row: "`DiscoveryProvenanceV2`, the boundary inventory").
- The refreshed reference still carries the V3 converter, as BS1-F3 requires, so B2-b has a reference to reproduce.
- **Rejected:** materializing the V3 schemas in B2-a, which would build record types with no producer.

**LD-B2A-3. No public export yet.**
- `discovery_rule` is `pub(crate)` under `#[allow(dead_code)]`, like B3-a's `grants`. B2-b consumes it inside the crate.
- The host's native instrument (B2-c) is the first consumer outside the crate, and adds the re-export with its own public-surface pin.
- **Rejected:** exporting now, which is surface with no consumer.

**LD-B2A-4. SX-1 is entry-type independent, and the row is for directories only.**
- The anchor path is classified whatever its entry type, so a `.opensip` file or symlink is never source and never inventoried.
- Only an observed directory is recorded in `prunedTrees` (SL:195: "when it is observed as a directory it is recorded once").
- `recorded` is false for every non-directory anchor, of any reason, which keeps DD's directory-only `pruned_anchors_from_directories`.
- **Rejected:** a row for a `.opensip` file. It is not a tree, and the law records only directories.

**LD-B2A-5. B2-a's half of the CI-trace control is the disposition; the trace is B2-b's.**
- B-S1 owes B2-a "the CI trace shows no open or listing of `.opensip`". B2-a performs no I/O. Its half is `classify_entry`: `.opensip` at the root or a member root is `NeverEnter`, decided from the parent's entry alone, for every entry kind.
- The instrument that walks (B2-b) records the trace over a real scratch tree. Item 13's walker obligations ("never descending") are its own.
- **Rejected:** a mock walker in B2-a, which would test a walk that does not exist.

**LD-B2A-6. Segments are exact bytes, with no case folding.**
- U-4a says "by **exact path segment**". `Node_Modules` and `.OpenSIP` are ordinary segments. That holds even on APFS, which X2 item 2's installation-parent comparison folds, because that is a different, law-stated rule.
- **Rejected:** folding. It would hide ordinary source, which MC forbids for `.opensip`.

## 3. Tests

- **Reference vectors (the B1-a pattern).** `tools/security/discovery_rule_vectors.py` runs the refreshed reference at its accepted bytes. It writes or checks `crates/security/src/discovery_rule_vectors.json` over:
  - the 49 pruning controls;
  - the SX-1 controls below;
  - `normalize_explicit_root` cases, including `.`, a trailing `/`, `a//b`, `..`, `/a`, backslash, NUL and empty;
  - the 4096/4097 cap, and 4200 installed manifests as one anchor in both bases;
  - `relative_locator`, `classify_boundary` and `classify_custody_exclusion` cases;
  - both excluded-prefix functions.

  The Rust test reproduces every vector.
- **SX-1** (the B-S1 B2-a controls):
  - the anchor at `""` and at a member root;
  - `.opensip` anywhere else (`src/.opensip`, a non-member `m/.opensip`) is source;
  - `.opensip` as a file or symlink is `NeverEnter` with `recorded: false`;
  - `.opensip/package.json` is never a unit, and `.opensip/Cargo.toml` never a Cargo root;
  - the conventional prefix holds with and without the directory observed;
  - outermost against `node_modules` and `target` in both orders.
- **Rule properties.**
  - Outputs are sorted and unique.
  - The functions are total over supplied strings, and absolute or root entries are skipped as DD skips them.
  - The cap does not truncate.
  - `markerCount` is `None` when not enumerated.
- **Purity.** A source pin: no `std::fs`, `std::io`, `std::env`, `std::process` or platform crate. The module sits under B1-b's environment lint.
- **Verification.** Security and host suites, base against candidate, with equal failure sets; all-targets Clippy with warnings denied; rustfmt; the environment-exception pin, with its list unchanged; the operability census; the vector check; verify_design; mutations (outermost-only-within-subset, the parent-first order, an `.opensip` segment matched at any depth, a recorded non-directory, cap truncation, a dropped trailing-slash rule).

## 4. Sequence

1. This plan, reviewed by Codex.
2. **The reference refresh** (1.1): the copy, its checker, Codex ACCEPT-DESIGN-UNIT, the architecture record, and the lock bind as contract successor 163.
3. **The product rule** (1.2): stage, checks, Codex ACCEPT-UNIT, the architecture record, then the product code commit.
4. **Inventory successor v191**, adding `discovery_rule.rs`, its tests, the vectors and the tool.
5. **A status round.**

## 5. Not claimed

- No walker, ledger profile, provenance record, boundary inventory, public row, refusal mapping or T2 census (B2-b).
- No native unit instrument, U-0 to U-9 beyond U-4a, JSONC reader or public export (B2-c).
- No membership decision (B3-b).
- No read set (C1).
- No SLM or native-model refresh.
- No law or passage change, and no qualification.
