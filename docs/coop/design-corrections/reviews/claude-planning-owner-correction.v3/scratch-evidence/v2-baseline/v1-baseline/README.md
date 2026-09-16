# claude-planning-owner-correction.v1 — authored correction for PS-01 and PS-04

Authored, not self-accepted. This is a bounded author correction for two findings
from my own prior independent review. It requires another substantive review on
newly frozen bytes. It claims no readiness and no acceptance.

Baseline normative source stays frozen candidate25
(`/tmp/opensip-design-corrections/candidate-subject.v25`, manifest
`fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d`). Nothing in
frozen25 is edited. The prior nine planning inputs at
`/tmp/opensip-design-corrections/claude-planning-successor-review.v1/inputs`
are unmodified; all work is in `scratch/work/`.

## Scope

In scope (mine): PS-01 and PS-04 only.
Out of scope (root's, deliberately untouched): PS-02, PS-03, PS-05, PS-06,
PS-07, PS-08 and the CR-19 mapping. Both generated blocks of the implementation
plan are byte-identical to frozen input, so the CR-19 F32 regeneration pass does
not collide with this change.

## Changed and new files

| File | Status | Before | After |
|---|---|---|---|
| `docs/v2/architecture/implementation-boundaries-and-build-plan.md` | changed | 78397 B | 82985 B |
| `docs/v2/architecture/store-instance-lineage.v1.json` | new | — | 30224 B |
| `docs/v2/architecture/report-asset-binding.v1.json` | new | — | 22929 B |

The other eight planning inputs are byte-identical. Exact before/after digests
are in `hashes.json`. Plan edits are confined to frozen lines 239–261 (PS-01
prose) and 591–619 (PS-04 prose); `patches/` holds the unified diff.

## Artifacts

- `work/` — the full working tree (nine inputs, two new companions, and the
  candidate25 manifest at its expected relative path so the checkers run)
- `patches/implementation-boundaries-and-build-plan.md.patch` — unified diff
  against the exact frozen input
- `controls/check_store_instance_lineage.py` — PS-01 structural and join control
  with 11 negative controls and an executed digest-continuity property
- `controls/check_report_asset_binding.py` — PS-04 structural and join control
  with 17 admission vectors
- `control-evidence.json` — executed output of both planning checkers and both
  new controls
- `hashes.json`, `hashes.before.json` — before/after digests

## Re-running

    python docs/operations/check_repository_file_inventory.py --check
    python docs/operations/check_implementation_planning.py --source <c25> --check
    python controls/check_store_instance_lineage.py work <c25>
    python controls/check_report_asset_binding.py  work <c25>

Last executed: both planning checkers PASS unchanged (198 paths; 320 mappings,
38 cases), `check_store_instance_lineage` PASS with 11/11 negative controls
detected, `check_report_asset_binding` PASS with 17/17 vectors.

Only the two new controls and the two planning checkers were run. Unrelated
suites were not rerun for a prose-and-schema change.

## Limitations

- Both companions are proposed owner-successor deltas and private schemas. They
  are not accepted, not frozen, and confer no readiness.
- No product code exists. Owning modules are named for implementation planning
  only, and all named modules already appear in the existing inventory, so this
  correction adds no inventory row and no generated-section change.
- `check_store_instance_lineage` models the digest-continuity property with a
  stand-in canonicalizer; the real canonicalizer is owned by identity §3.
- `check_report_asset_binding` models manifest admission and the pin check only.
  It establishes no browser behaviour, no release build and no signing.
- Whole-install-root substitution stays undetected in both corrections. That is
  the bound frozen25 already states, not a new weakness and not a claim of
  tamper detection.
- The versioned physical carrier, migration, read-only anchors and additional
  race cases (COV-03 and the separately active carrier task) remain open. Both
  companions name their required joins with that work rather than assuming it.
- The exact CORE release catalog row shape is not published in candidate25. The
  selected PS-04 anchor deliberately does not depend on it; install-time
  provenance does, and is named as an open dependency.
