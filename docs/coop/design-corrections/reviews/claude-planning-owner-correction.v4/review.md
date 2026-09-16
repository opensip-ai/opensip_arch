# PS-01 identity-selection boundary fixed — v4

I ran root's `repeated-generation.py` unchanged; it reproduces the supplied JSON byte-for-byte. Both counterexamples are correct and accepted. v3 is immutable (71/71 verified), frozen25 intact (12869 members, 0 mismatches), nine planning inputs unmodified, **PS-04 bytes unchanged** (`ae82ca6a…`).

---

## RC-4 — repeated generation across distinct stores

v3 looked nodes up by the numeric `(storeGeneration, stateSchema)` pair while the S9.3 prose it shipped with said the primary key is the **triple**. The helper contradicted its own prose. With retained branch `(b,4,2)`, active root `(a,3,1)`, fresh target `(e,4,2)`:

| state | owner | v3 companion | v4 companion |
|---|---|---|---|
| LEASED | `ABORT` | **QUARANTINE** "premature new node" | `none`, no refusal, 2 nodes untouched |
| COMMITTED | `RESUME-COMMIT` | **QUARANTINE** "stored node disagrees" | `reconstructed-and-written`, 3 nodes, invariants clean |

Every lookup now builds the full triple from the store-root **marker** of the store concerned. A retained branch at an equal numeric pair is a different store: it neither blocks admission nor is read as this attempt's node. No global generation uniqueness is invented beyond the owner. `intentDigest` is validated *on* the selected node, never scanned for — the record's own schema says it may repeat.

## RC-5 — missing predecessor at the decision boundary

v3 wrote broken ancestry with `refusal: None` because predecessor presence lived only in the unused `invariants()` helper. There is now **one admission law, `admit_node`, called by both publication and recovery**: six members, paired nulls, no self-reference, predecessor present at its exact triple, no disagreeing duplicate primary key, one acyclic lineage root afterwards. A refusal writes nothing. `invariants()` is now only a whole-set auditor for controls.

```
absent predecessor                              -> QUARANTINE (predecessor-absent), 0 written
predecessor names a node that does not exist    -> QUARANTINE, 0 written
duplicate predecessor key, identical contents   -> QUARANTINE
duplicate predecessor key, disagreeing contents -> QUARANTINE
duplicate target key, disagreeing contents      -> QUARANTINE
target key exists with a different origin       -> QUARANTINE
selected marker missing / malformed             -> QUARANTINE, nothing dereferenced
forward markers name the same store             -> QUARANTINE
ancestor reselect naming an off-chain store     -> QUARANTINE
ancestor reselect naming the verified chain     -> validated-existing
```

## Also corrected

**Non-forward joins** use the same full-triple principle: an ancestor is resolved from the retained store's marker and must lie on the **verified chain** from the current node; origins are never rewritten. **BUSY / REFUSE / QUARANTINE** now make no companion decision and inspect nothing — v3's prose said this but the generic branch still inspected nodes. **Stale metadata** fixed: both `correctionOf.remedy` and `ownerSuccessorDelta.normativePatch` now name `security-and-lifecycle.md.S9-pair-law-and-S9.3.patch` and say two hunks.

## New composed evidence

`check_lineage_recovery.py` keeps sections A (root v2 regressions) and C (7 owner-admitted operation cases × 6 journal states) and adds D (root v3 regressions), E, F, G. Shape admission (`admit_transition_intent`, eleven-member record) is reported separately from current-state/footprint admission (`recover_transition_journal` with registry, fence, leases, footprint).

Section E, composed with real owner-admitted intents:
```
migrate (3,1)->(4,2)        RESUME-COMMIT  reconstructed-and-written   2 nodes
store-rollback (4,2)->(3,1) RESUME-COMMIT  validated-existing          2 nodes, origin {null,null} preserved
second migrate (3,1)->(5,2) RESUME-COMMIT  reconstructed-and-written   3 nodes
final lineage: (a,3,1) root -> (e,4,2) and (f,5,2); retained branch origin digest unchanged
```

Section G confirms `REFUSE` / `BUSY` / `QUARANTINE` → `no-decision`, and that an unfenced PREPARED store operation is an owner `ABORT` with no companion refusal.

An interim failure is on the record: my first section-F expectation treated two identical duplicate **root** nodes as benign; the law correctly refused them on the one-root invariant — the test was wrong, not the law. Duplicates are now exercised where the decision path actually dereferences a key.

---

## Deliverables

| File | v3 | v4 | Patch |
|---|---|---|---|
| `implementation-boundaries-and-build-plan.md` | 86912 B | 88249 B | 2 hunks, +30/−10 |
| `store-instance-lineage.v1.json` | 49961 B | 59050 B | 12 hunks, +91/−45 |
| `report-asset-binding.v1.json` | 27714 B | **unchanged** | — |
| `security-and-lifecycle.md` (frozen25) | `12dcebea…` 94428 B | `4464780e…` 101061 B | **2 hunks, +97/−0** |
| `controls/lineage_law.py` · `check_lineage_recovery.py` · `check_store_instance_lineage.py` | | | 6 · 4 · 2 hunks |

Schema unchanged at six members; no new identifier, record or operation. Eight of nine planning inputs byte-identical to frozen; both generated plan blocks byte-identical; JSON valid with no duplicate keys; no trailing whitespace or tabs; links resolve. Exact digests in `manifest.json`; all four root counterexample files retained in `root-counterexamples/`.

**All six controls PASS** (`control-evidence.json`): both planning checkers unchanged (198 paths; 320 mappings, 38 cases), `check_store_instance_lineage`, `check_lineage_recovery`, `check_report_asset_binding`, `check_report_asset_fixture`. Unrelated suites not rerun.

## Limitations

Proposed, unaccepted, unfrozen; no readiness — independent review follows and I do not accept my own corrections. No product code; all named owning modules already exist in the inventory, so no inventory row or generated-section change. Owner results are the frozen model's own returns; the companion law is a design reference, not a carrier implementation, crash test or native lifecycle qualification. Node identity depends on readable markers — an unreadable one refuses rather than guessing, but a readable-and-wrong marker after an out-of-band copy stays in frozen25's stated undetected class. `StateSchema` is `{1,2}`, so no owner-admitted example exercises multiple distinct ancestors at one schema, though the ancestor branch already refuses ambiguous and off-chain matches. The CORE release catalog/manifest shape remains not provided by candidate25 and unassigned; COV-03 and the separately active carrier work remain open.
