# B2-a reference refresh: the shared discovery rule with SX-1 and the V3 boundary inventory

**Design unit, reference only, under the accepted B2-a plan r1** (`config-discovery-b/b2-a/PLAN-r1.md`, section 1.1, LD-B2A-1; Codex `codex-b2a-plan-r1`). It discharges B-S1's finding **BS1-F3** and its **LD-14**: `discovery-defaults.py` (DD) "lacks SX-1's anchor and D15's `memberRepositories` in `boundary_inventory_from_provenance`, so a reference refresh is owed" with B2-a's evidence. It is bound as contract successor 163, after the pruning correction (successor 124), whose precedent it follows.

## r2 changes

Codex's round 1 (`codex-b2a-reference-r1`, REQUIRED-FINDINGS) found **B2AREF-1**: `member_roots` was declared `Iterable[str]` but forwarded repeatedly. A single-pass iterator therefore lost member anchors after the first classification, which admitted a member's `.opensip` as a unit or Cargo root and dropped its observed row.
- **Fix.** `cargo_roots_from_markers`, `enumerate_units` and `pruned_anchors_from_directories` now materialize `member_roots` into a tuple on entry.
- **The same latent defect, inherited from DD.** `pruned_anchors_from_directories` forwarded `cargo_roots` once per directory; it is materialized too.
- **New controls.** Four list-versus-iterator controls cover all three entry points, including observed directories processed after marker classification.
- **Shown to bite.** Run against the r1 copy, the r2 checker fails on the first of them (review support, `r1-copy-under-r2-checker.txt`).
- **Round 1's NBO-1.** The outermost control now has a real member anchor (`target/m/.opensip/x`), and `.opensip/.git/x` covers the other order against `.git`.
- **Unchanged.** The changed-function set is the same six functions, and every other byte of r1 is kept.

## What it is

`reference/discovery-defaults.sx1-r1.py` is a separate copy. DD and the pruning copy `discovery-pruning-reference-r2/reference/discovery-defaults.pruning-r1.py` keep their bytes.

The new copy is the pruning copy, byte for byte, plus exactly these changes. `evidence/author.py` makes each one as an asserted replacement.

| Change | Text it implements |
|---|---|
| `DISCOVERY_DEFAULTS_VERSION` 2 → 3 | B-S1 LD-4: SX-1 makes version 3 current |
| `OPENSIP_CUSTODY_STATE = '.opensip'`; `PRUNE_REASONS` gains `opensip-custody-state`; `PRUNED_TREE_ROW_VERSION` 2 → 3 | SL:195 and SL:205; NE:714; SLS `PrunedTreeRowV3` (Codex NBO-1 on the plan) |
| `_custody_state(parts, member_roots)` (new) and `classify_path(relpath, cargo_roots, member_roots=())` | `.opensip` is an exact anchor at `""` and at each admitted member root, never a segment at any other depth. The outermost anchor still wins across all four reasons (the pruning correction, now including SX-1) |
| `member_roots=()` passed through `cargo_roots_from_markers`, `pruned_anchors_from_directories` and `enumerate_units`, each materialized on entry (r2), as is `pruned_anchors_from_directories`' `cargo_roots` | a marker inside `.opensip` is never a unit or a Cargo root; an observed `.opensip` directory is one row |
| `conventional_excluded_prefixes(unit_roots, cargo_roots, member_roots=())` | always `.opensip` at the root and at each member root (B-S1 LD-3; NE:939) |
| `CURRENT_PROVENANCE_VERSION`, `BOUNDARY_INVENTORY_VERSION` → 3; the supported tuples gain 3 | B-S1 LD-4; SLS `AdmittedBoundaryInventoryV3` |
| `boundary_inventory_from_provenance` adds `memberRepositories` (relative, UTF-8 order) | SLS `AdmittedBoundaryInventoryV3`; NE:940: members are not boundaries and add no prefix |
| module docstring: one SX-1 and V3 paragraph | — |

**What stays the same.**
- The defaults `member_roots=()` keep every earlier call meaning the same, and the 49 pruning controls are unchanged.
- The converter keeps DD's two-lane rule: reading a historical record is not converting it. V1 and V2 provenance now refuse at conversion as `PROVENANCE_VERSION_UNSUPPORTED:<n>`.

## Checks

`evidence/check.py` writes `evidence/checks.json`, which reports `passed: true` with 83 controls:
- **The 49 pruning controls,** rerun on both copies. Every result is unchanged and equals its expectation.
- **23 SX-1 controls:**
  - the root and member anchors;
  - `.opensip` elsewhere, at a non-member, below a member, in another case or as a substring is source;
  - outermost against `node_modules`, `.git` and `target` in both orders, including a member anchor inside a Cargo `target`;
  - never a Cargo root, never a unit;
  - an observed directory with no marker is a row, and an unobserved one is not;
  - the member row;
  - the prefix is present always, and with members.
- **4 iterator controls (r2).** A single-pass iterator equals a list for `member_roots` in all three forwarding entry points, and for `cargo_roots` in `pruned_anchors_from_directories`.
- **7 V3 controls.** The converter's outputs validate as `AdmittedBoundaryInventoryV3` in the SLS bundle merged with B-S1's additions under its merge rule. Members are sorted, relative and not prefixes; the no-member case is covered. V1, V2, V4 and a bool version refuse with their exact details, as does a member outside the root. The pruning copy refuses V3.
- **AST.** Against the pruning copy, only the six named functions, one added helper, eight constants (seven changed, one added) and the module docstring differ.

The checker imports the reference copies and the pinned `canonical.py` with the provisioned jsonschema snapshot. It reads no filesystem tree, runs no product code, and claims no qualification.

## Not claimed

- No product code. The rule `custody/discovery_rule.rs` is B2-a's next step, and it reproduces vectors generated from this copy.
- No passage override or supersession, and no schema change: B-S1's V3 fragments are used as they are.
- No SLM or native-model refresh (BS1-F3 owes DD's reference only).
- No walker or CI trace (B2-b), no membership decision (B3-b), no qualification.
