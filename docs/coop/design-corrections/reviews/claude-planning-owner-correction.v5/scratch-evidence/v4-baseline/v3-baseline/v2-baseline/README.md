# claude-planning-owner-correction.v2 — PS-01 / PS-04 revision 2

Authored, not self-accepted. Resolves the eight concrete issues root raised against
v1. v1 is retained and immutable at
`/tmp/opensip-design-corrections/claude-planning-owner-correction.v1/scratch`
and copied here unmodified as `v1-baseline/` with `hashes.v1-baseline.json`.

Baseline normative source stays frozen candidate25 (12869 members, 0 mismatches,
re-verified). Nothing in frozen25 or in the frozen planning inputs is edited.

## Issue disposition

| # | Issue | Resolution |
|---|---|---|
| 1 | Manifest self-reference | `manifestSelfReference` section: the pinned manifest is forbidden as an asset row (`MANIFEST_SELF_LISTED`) and excluded from completeness by **exact path equality**; coverage stays total. Executed against a real temporary release tree. |
| 2 | Optional-surface row | No longer success/exit 0. Defers to the §8 aggregate over **required steps only**; demonstrated that 1/3/4 stay 1/3/4. Anchor B11 added. |
| 3 | Digest recipe reordering | Withdrawn. The frozen `canonical()` sorts keys, so input key order is not observable. Add/remove/rename still change it. The control now imports the **actual frozen canonicalizer**. |
| 4 | Floors | Split three ways: authorized S9 transition (copy forward / max of both / only S4.5 lowers), fresh installation, and evidence-restore or adoption. The restore rule no longer invalidates the migration carry-forward. |
| 5 | Aborted rows vs active joins | Nodes are written only after `COMMITTED`, so an aborted attempt writes nothing and can never be read as lineage. Recovery is now **total over all six** owner journal states and never replaces the owner's ABORT at `PREPARED` with a quarantine. |
| 6 | core-rollback, unchanged schema | Node-writing is derived from the intent's own from/to values, not the operation name, because S9.2 publishes no store rule for `core-rollback`. Same-store and ancestor-reselect are now distinct and neither mints a fresh identity. |
| 7 | intentDigest is not an attempt id | Primary key moved to the admitted binding triple; `intentDigest` is evidence only. A concrete retry trace shows a lawful post-abort retry produces no collision, and a post-commit replay is refused by the owner's own `CURRENT_STORE_MISMATCH`. No new public field. Cross-file atomicity is no longer claimed: the node is derivable from the journal plus the two store-root markers, so a one-sided footprint reconciles by reconstruction. |
| 8 | No normative owner patch | `patches/security-and-lifecycle.md.S9.3.patch`: **one hunk, pure insertion of 62 lines** after S9.2, removing no line, for clean three-way merge with the separate carrier author's S1/S6/S9/WA13 edits. |

Not expanded: no core release manifest is authored. The CORE catalog/manifest shape
is recorded as **not provided by candidate25 and unassigned** — explicitly *not* the
active grant-journal carrier author's work.

## Changed files

| File | v1 | v2 | Patch |
|---|---|---|---|
| `implementation-boundaries-and-build-plan.md` | 82985 B | 85756 B | 4 hunks, +59/-18 |
| `store-instance-lineage.v1.json` | 30224 B | 35761 B | 8 hunks, +272/-217 |
| `report-asset-binding.v1.json` | 22929 B | 27714 B | 6 hunks, +40/-7 |
| `security-and-lifecycle.md` (frozen25) | 94428 B | 98652 B | 1 hunk, +62/-0 |

The other eight planning inputs are byte-identical to their frozen originals. Both
generated blocks of the plan remain byte-identical to the frozen input, so root's
CR-19 F32 regeneration does not collide. Exact digests are in `hashes.json`.

## Artifacts

- `work/` — working tree (nine planning inputs plus two companions)
- `owner-successor/` — candidate25 owner file with S9.3 inserted, for diffing only
- `patches/` — three v1→v2 patches plus the frozen25 S9.3 insertion
- `controls/` — three executable controls
- `control-evidence.json`, `hashes.json`, `hashes.v1-baseline.json`, `patch-summary.json`

## Executed controls

    python docs/operations/check_repository_file_inventory.py --check
    python docs/operations/check_implementation_planning.py --source <c25> --check
    python controls/check_store_instance_lineage.py work <c25>
    python controls/check_report_asset_binding.py  work <c25>
    python controls/check_report_asset_fixture.py

All five PASS. `check_report_asset_fixture` builds a real temporary release tree
and passes 12/12 cases. `check_store_instance_lineage` imports the frozen
canonicalizer and executes four properties. Only focused controls were run; no
full evaluator suite.

## Limitations

- Both companions and the S9.3 insertion are **proposed**, unaccepted, unfrozen,
  and confer no readiness. Another substantive review on newly frozen bytes is
  required; I do not accept my own corrections.
- No product code. Owning modules are named for planning only and all already
  exist in the inventory, so no inventory row and no generated-section change.
  The two companion JSON documents are planned architecture sources, not product
  inventory files.
- The lineage control executes the digest property with the exact frozen
  canonicalizer; the node, retry and reconciliation rules remain **models**, not
  carrier tests.
- `check_report_asset_fixture` is temporary-filesystem evidence. It is not a
  release build, a browser test or any parity or qualification claim.
- Whole-install-root substitution stays undetected — frozen25's existing stated
  bound, not a new weakness.
- S9.2 publishes no store-generation rule for `core-rollback`. The companion reads
  the admitted intent's values rather than asserting one; if the owner later
  publishes such a rule, the derived cases must be rechecked.
- COV-03 and the separately active versioned carrier, migration and read-only
  anchor work remain open; the required join is named, not assumed.
