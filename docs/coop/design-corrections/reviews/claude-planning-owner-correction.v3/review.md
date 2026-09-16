# PS-01 node recovery contradiction fixed — v3

Both of root's counterexamples are correct and accepted. v2 and all earlier inputs are immutable (44/44 hashes verified); root's two counterexample files are retained unchanged in `root-counterexamples/`. Frozen25 re-verified at 12869 members, 0 mismatches. **PS-04 bytes unchanged** (`ae82ca6a…`), as directed.

---

## 1. Recovery is now conditional on the same case as publication

The v2 defect was real: publication branched on the selection case, recovery did not. For a same-store operation `from == to`, so the unconditional reconstruction named itself.

Both paths now call one derivation in `controls/lineage_law.py`:

- **forward selection** — this transition created the node, so it alone is reconstructible from the committed intent plus the two markers. Because the owner forbids a same store here, the predecessor can never equal the node; a reconstruction that would name itself is **refused rather than written**.
- **same-store** / **ancestor re-selection** — the selected node came from an **earlier, unrelated act**. Recovery validates it and **never rewrites its predecessor or origin digest**. A missing one is not repairable from the current intent — the intent does not carry that origin — so it is `QUARANTINE` / `MIGRATION.CORRUPT`, never fabricated. The ancestor branch additionally verifies the target really is an ancestor, which the owner cannot check.
- **owner precedence at PREPARED** is honoured exactly: a core operation ABORTs, a store operation follows the S9 footprint, and the companion acts only once the owner's *returned action* settles the transition as committed (`RESUME-COMMIT`/`RELEASE-ONLY` → `DONE`). It never decides a journal state itself.
- **pre-COMMITTED** no longer says "node absent" — that was also wrong, since the selected store's ancestry always exists. The invariant is: *no node may carry this transition's `intentDigest`, and for a forward selection no node may occupy its `to` pair.* Either is a premature-node contradiction.

Root's exact scenario, now:
```
ownerAdmitted: true   ownerAction: RESUME-COMMIT
companionNodeAction: validated-existing
selfPredecessorProduced: false
originPreserved: {predecessor: null, selectedByIntentDigest: null}
```

## 2. Composed controls against the actual owner

`check_lineage_recovery.py` imports the frozen model and calls `admit_transition_intent`, `transition_intent_digest`, `transition_journal_record`, `recover_transition_journal`. Seven owner-admitted **eleven-member** intents (six frozen fixtures + one composed schema-retreating `core-rollback`, admitted before use) × six journal states = 42 cells. Both RC-2 refusals are regressed:

```
core-rollback  (5,1)->(4,1) -> ["TRANSITION.SAME_SCHEMA_KEEPS_STORE"]
store-rollback (5,1)->(4,1) -> ["TRANSITION.STORE_ROLLBACK_REQUIRES_SCHEMA_RETREAT"]
```

Matrix summary — all three same-store cases and both ancestor cases `validated-existing` with no node written; both forward cases `reconstructed-and-written` only where the owner settled to DONE (including `store-migrate` at PREPARED with a RESTORED-fenced footprint); every stripped-ancestry variant quarantines. Zero self-predecessor or cyclic nodes anywhere.

**A second defect found while developing this revision is on the record:** an interim draft derived the case from *stored ancestry*, which let a damaged lineage reclassify a rollback as a forward selection and fabricate a node. My own control caught it. The case is now a pure function of the admitted intent — decidable without trusting the very records recovery is about to check.

## 3. Overstatement withdrawn; pair law added to S9.2

`admit_transition_intent` lines 2189–2192 and 2198–2201 enforce the pair for `core-update` **and** `core-rollback`, and the module's own comment says it outright. Read off the owner:

| operation | same schema, different store | schema change, same store |
|---|---|---|
| core-update | `SAME_SCHEMA_KEEPS_STORE` | `SCHEMA_CHANGE_SELECTS_NEW_STORE` |
| core-rollback | `SAME_SCHEMA_KEEPS_STORE` | `ROLLBACK_CANNOT_RAISE_SCHEMA`, `SCHEMA_CHANGE_SELECTS_NEW_STORE` |

The owner patch is now **two hunks, both pure insertions, +82/−0**: hunk 1 states the pair law in S9.2 itself (so a blind consumer needs no excluded model, restating existing behaviour and changing no refusal); hunk 2 inserts the corrected S9.3. I placed hunk 1 between paragraphs rather than mid-sentence specifically to keep it removal-free for the carrier author's three-way merge.

## 4. Collision claim corrected

Replaced "cannot collide" with: distinct construction and preimage framing give **domain separation**, enforced by where each digest is required; any non-collision statement rests on the standard SHA-256 **collision-resistance assumption**, which this design assumes and does not prove. Still no new public H-domain.

## 5. Lineage root covers restore and adoption

Generalised from "installation" to any authorized local act materialising a new physical store — installation, or an authorized evidence restore / portable adoption. Obligations: allocate a fresh `storeInstanceId`; **replace** any marker present in copied bytes before first publication so a restored store never impersonates its source; import no node, floor, grant or local authority; invent no transition to manufacture an `intentDigest`. A source digest is simply not in the local chain — the walk terminates at the local root and reports unavailability. Which act created a root is recorded by `installation.rs` / `backup.rs`, so the **six-member record shape is unchanged**.

---

## Deliverables

| File | v2 | v3 | Patch |
|---|---|---|---|
| `implementation-boundaries-and-build-plan.md` | 85756 B | 86912 B | 1 hunk, +32/−16 |
| `store-instance-lineage.v1.json` | 35761 B | 49961 B | 15 hunks, +207/−111 |
| `report-asset-binding.v1.json` | 27714 B | **unchanged** `ae82ca6a…` | — |
| `security-and-lifecycle.md` (25) | `12dcebea…` 94428 B | `18601fa1…` 99928 B | **2 hunks, +82/−0** |

Eight of nine planning inputs byte-identical to frozen; both generated plan blocks byte-identical; JSON valid with no duplicate keys; no trailing whitespace or tabs; links resolve. Exact digests in `manifest.json`.

**All six controls PASS** (`control-evidence.json`): both planning checkers unchanged (198 paths; 320 mappings, 38 cases), `check_store_instance_lineage`, `check_lineage_recovery`, `check_report_asset_binding`, `check_report_asset_fixture`. Unrelated suites not rerun.

## Limitations

Proposed, unaccepted, unfrozen; no readiness — another substantive review on newly frozen bytes is required and I do not accept my own corrections. No product code; all owning modules already exist in the inventory, so no inventory row or generated-section change, and the companions are planned architecture sources. Owner results in `check_lineage_recovery` are the frozen model's own returns; the companion law is a design reference, not a carrier implementation, crash test or qualification. `StateSchema` is `{1,2}`, so chains are short — a wider enum would admit multiple distinct ancestors at one schema, and although the ancestor branch already refuses an ambiguous match, no owner-admitted example exercises that today. Whole-install-root substitution stays undetected (frozen25's existing bound). The CORE release catalog/manifest shape remains not provided by candidate25 and **unassigned** — not the grant-journal carrier author's work; COV-03 and the separately active carrier work remain open.
