# claude-planning-owner-correction.v3 — PS-01 node recovery contradiction fixed

Authored, not self-accepted. v2 and all earlier inputs are immutable and retained;
v2 is copied here as `v2-baseline/` with `hashes.v2-baseline.json`. Root's two
counterexample files are retained unchanged in `root-counterexamples/`.

Frozen candidate25 re-verified: 12869 members, 0 mismatches. Nothing in frozen25
or in the frozen planning inputs is edited.

## Root's counterexamples: both accepted

**RC-1 — self-predecessor.** Root AST-extracted v2's `reconstruct()` unchanged and
ran it against the owner-admitted frozen `intentRepair`. It built a node whose
`predecessor` equalled its own triple. Real defect: v2 *published* conditionally on
the selection case but *reconstructed* unconditionally on COMMITTED/DONE, and for a
same-store operation `from == to`.

**RC-2 — mislabelled rollbacks.** v2's matrix called `(5,1)->(4,1)` a schema retreat
for both rollback kinds. The owner refuses both:
`TRANSITION.SAME_SCHEMA_KEEPS_STORE` and
`TRANSITION.STORE_ROLLBACK_REQUIRES_SCHEMA_RETREAT`. v2 used a four-member stand-in
and called it owner evidence.

**RC-3 — overstatement.** "S9.2 publishes no core-rollback store rule" is withdrawn.
`admit_transition_intent` (lines 2174–2215) enforces the pair for `core-update` and
`core-rollback` alike; only the short S9.2 *prose* omitted it.

## Corrections

1. **Recovery is conditional on the same case as publication.** Both derive the case
   from one function. Only a **forward selection** created a node, so only it is
   reconstructible; a reconstruction that would name itself is refused rather than
   written. A **same-store** or **ancestor re-selection** validates the retained node
   and never rewrites its predecessor or origin digest — that node came from an
   earlier, unrelated act whose origin the current intent does not carry, so a
   missing one is `QUARANTINE` / `MIGRATION.CORRUPT`, never fabricated. Owner
   precedence at `PREPARED` is honoured exactly: a core operation ABORTs, a store
   operation follows the S9 footprint, and the companion acts only once the owner's
   returned action settles the transition as committed. Before that, pre-existing
   ancestry is **expected**, and what must not exist is a *new* node for that
   transition.
2. **Composed controls** call the frozen `admit_transition_intent`,
   `transition_intent_digest`, `transition_journal_record` and
   `recover_transition_journal`: seven owner-admitted eleven-member intents × six
   journal states = 42 cells, plus both RC-2 refusals as regressions.
3. **The S9.2 pair law is inserted into S9.2 itself**, so a blind consumer needs no
   excluded model. It restates existing reference behaviour and changes no refusal.
4. **Collision claim corrected.** Domain separation by distinct construction and
   preimage framing, plus the standard SHA-256 collision-resistance assumption — not
   an impossibility claim. Still no new public H-domain.
5. **Lineage root generalised** from installation-only to any authorized local act
   that materialises a new physical store, so an evidence restore or portable
   adoption has a lawful root without inventing a public transition. A copied marker
   must be **replaced** so a restore cannot impersonate its source; no node, floor,
   grant or authority is imported. Record shape unchanged at six members.

A further defect found while developing this revision is also retained in the
record: an interim draft derived the case from the *stored ancestry*, which let a
damaged lineage reclassify a rollback as a forward selection and fabricate a node.
The case is now a pure function of the admitted intent.

## Files

| File | v2 | v3 | Patch |
|---|---|---|---|
| `implementation-boundaries-and-build-plan.md` | 85756 B | 86912 B | 1 hunk, +32/−16 |
| `store-instance-lineage.v1.json` | 35761 B | 49961 B | 15 hunks, +207/−111 |
| `report-asset-binding.v1.json` | 27714 B | **unchanged** `ae82ca6a…` | — |
| `security-and-lifecycle.md` (frozen25) | 94428 B `12dcebea…` | 99928 B `18601fa1…` | **2 hunks, +82/−0** |

PS-04 bytes are untouched, as root directed. Eight of nine planning inputs are
byte-identical to their frozen originals; both generated plan blocks remain
byte-identical. Exact digests: `manifest.json`.

## Controls

    python docs/operations/check_repository_file_inventory.py --check
    python docs/operations/check_implementation_planning.py --source <c25> --check
    python controls/check_store_instance_lineage.py work <c25>
    python controls/check_lineage_recovery.py <c25>
    python controls/check_report_asset_binding.py work <c25>
    python controls/check_report_asset_fixture.py

All six PASS; outputs in `control-evidence.json`. `controls/lineage_law.py` holds the
single publication/recovery law both paths call. Unrelated suites were not rerun.

## Limitations

- Proposed, unaccepted, unfrozen; no readiness. Another substantive review on newly
  frozen bytes is required — I do not accept my own corrections.
- No product code. All named owning modules already exist in the inventory, so no
  inventory row and no generated-section change. The companions are planned
  architecture sources, not product inventory files.
- Owner results in `check_lineage_recovery` are the frozen model's own returns. The
  companion law is a design reference: no carrier implementation, no crash test, no
  qualification.
- `StateSchema` is currently `{1, 2}`, so only two rollback operations can retreat and
  chains are short. A wider enum would admit multiple distinct ancestors at one
  schema; the ancestor branch already refuses an ambiguous match, but no
  owner-admitted example exercises that today.
- Whole-install-root substitution stays undetected — frozen25's existing stated bound.
- The CORE release catalog/manifest shape remains not provided by candidate25 and
  unassigned; it is not the grant-journal carrier author's work. COV-03 and the
  separately active carrier work remain open.
