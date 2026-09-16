# claude-planning-owner-correction.v4 — PS-01 identity-selection boundary fixed

Authored, not self-accepted. v3 and all earlier work are immutable and retained;
v3 is copied here as `v3-baseline/` with `hashes.v3-baseline.json`. All four of
root's supplied counterexample files are retained unchanged in
`root-counterexamples/`.

Frozen candidate25 unmodified. **PS-04 bytes unchanged** (`ae82ca6a…`).

## Root's v3 counterexamples: both accepted

I ran `repeated-generation.py` unchanged; it reproduces the supplied JSON exactly.

**RC-4 — repeated generation across distinct stores.** With retained branch
`(b,4,2)`, active root `(a,3,1)` and a fresh target `(e,4,2)`, the owner returns
ABORT at LEASED and RESUME-COMMIT at COMMITTED. v3 quarantined both. Cause: v3
looked nodes up by the numeric `(storeGeneration, stateSchema)` pair, while the
S9.3 prose and the primary key both say the triple — the helper contradicted the
prose it shipped with.

**RC-5 — missing predecessor.** Forward reconstruction against an empty node set
wrote a node with broken ancestry and `refusal: None`. Cause: predecessor
presence, acyclicity and uniqueness lived only in `invariants()`, which was never
on the decision path, and publication and recovery did not share an admission law.

## Corrections

1. **Full-triple identity everywhere**, with the instance component read from the
   store-root **marker** of the store concerned — new store for a forward
   selection, retained ancestor for a re-selection, unchanged store for
   same-store. A retained branch at an equal numeric pair is a different store: it
   neither blocks admission nor is read as this attempt's node. No global
   generation uniqueness is invented beyond the owner.
2. **`intentDigest` is never a search key** — the record's own schema says it may
   repeat, so it is validated *on* the selected node.
3. **One admission law, `admit_node`, on the decision path** for both publication
   and recovery: six members, paired nulls, no self-reference, predecessor present
   at its exact triple, no disagreeing duplicate primary key, one acyclic lineage
   root afterwards. A refusal writes nothing. `invariants()` remains only as a
   whole-set auditor for controls.
4. **Duplicate exact primary key with disagreeing contents refuses**, never picks
   first.
5. **Markers validated before any dereference**; missing or malformed refuses
   without reading anything.
6. **BUSY / REFUSE / QUARANTINE now make no companion decision at all** and
   inspect nothing — law and prose agree.
7. **Ancestor re-selection** resolves via the retained marker and requires the
   target to lie on the **verified chain** from the current node; an off-chain
   store at the same numeric pair never qualifies, and origins are never rewritten.
8. **Stale metadata fixed**: `correctionOf.remedy` and
   `ownerSuccessorDelta.normativePatch` now name
   `security-and-lifecycle.md.S9-pair-law-and-S9.3.patch` and say two hunks.

An interim failure during this revision is also on the record: my first section-F
expectation treated two identical duplicate **root** nodes as benign; the law
correctly refused them on the one-root invariant, and the test — not the law — was
wrong. Duplicates are now exercised where the decision path actually dereferences
a key.

## Files

| File | v3 | v4 | Patch |
|---|---|---|---|
| `implementation-boundaries-and-build-plan.md` | 86912 B | 88249 B | 2 hunks, +30/−10 |
| `store-instance-lineage.v1.json` | 49961 B | 59050 B | 12 hunks, +91/−45 |
| `report-asset-binding.v1.json` | 27714 B | **unchanged** | — |
| `security-and-lifecycle.md` (frozen25) | `12dcebea…` 94428 B | `4464780e…` 101061 B | **2 hunks, +97/−0** |
| `controls/lineage_law.py` | — | — | 6 hunks |
| `controls/check_lineage_recovery.py` | — | — | 4 hunks |
| `controls/check_store_instance_lineage.py` | — | — | 2 hunks |

Eight of nine planning inputs byte-identical to their frozen originals; both
generated plan blocks byte-identical. Exact digests in `manifest.json`.

## Controls

    python docs/operations/check_repository_file_inventory.py --check
    python docs/operations/check_implementation_planning.py --source <c25> --check
    python controls/check_store_instance_lineage.py work <c25>
    python controls/check_lineage_recovery.py <c25>
    python controls/check_report_asset_binding.py work <c25>
    python controls/check_report_asset_fixture.py

All six PASS. `check_lineage_recovery` sections: **A** root v2 regressions, **B**
owner pair law, **C** 7 operation cases × 6 journal states, **D** root v3
regressions, **E** composed migrate → rollback → second forward selection with a
retained branch, **F** damaged predecessor / duplicate full key / unreadable
markers / off-chain ancestor, **G** owner actions that decide nothing. Shape
admission (`admit_transition_intent`) is reported separately from current-state
and footprint admission (`recover_transition_journal`). Unrelated suites were not
rerun.

## Limitations

- Proposed, unaccepted, unfrozen; no readiness. Independent review follows — I do
  not accept my own corrections.
- No product code. Named owning modules already exist in the inventory, so no
  inventory row and no generated-section change; the companions are planned
  architecture sources.
- Owner results are the frozen model's own returns; the companion law is a design
  reference, not a carrier implementation, crash test or native lifecycle
  qualification.
- Node identity depends on readable store-root markers. An unreadable marker
  refuses rather than guessing, but a marker that is readable and wrong after an
  out-of-band copy is in frozen25's stated undetected class.
- `StateSchema` is `{1, 2}`, so chains are short and no owner-admitted example
  exercises multiple distinct ancestors at one schema; the ancestor branch already
  refuses an ambiguous or off-chain match.
- The CORE release catalog/manifest shape remains not provided by candidate25 and
  unassigned. COV-03 and the separately active carrier work remain open.
