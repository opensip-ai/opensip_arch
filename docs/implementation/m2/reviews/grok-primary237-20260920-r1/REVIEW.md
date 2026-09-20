# Independent frozen integration review — primary trust reference consolidation 237 r1

Complete frozen reference snapshot. **Not source/runtime/design selection, not product install, not
cumulative protocol approval.** Prior reviews
`/tmp/opensip-implementation/reviews/grok-publication235-20260920-r1/` and
`/tmp/opensip-implementation/reviews/grok-trustgraph236-20260920-r1/` are untouched. No repo,
candidate, or construction-script run against a live tree.

Six security modules now share the compiled 122-definition private schema and import primary
siblings. Guard/iterator **bodies** are the reviewed 230 r3 / 232 r4 / 234 r1 / 235 r1 / 236 r1
algorithms. The input validator is the one intended logic change: it no longer builds a parallel
110-definition bundle.

## Verification

- Frozen `producer-integration-reference-wip-237-r1` `dca9a702…d050` (4784556 B, **1453** members):
  pin and every `subject.json` member verified from the tar before extraction.
- Consumed `inputs/` archives verified the same way, pins matching prior reviews:
  201 `ebd5b03f…eeb5` (1376), 230 r3 `99288ae0…3c00` (38), 232 r4 `26bf1187…e2e9` (58),
  234 r1 `8ad2d813…1c66` (63), 235 r1 `112dc6a0…5468` (26), 236 r1 `f09cb777…dc62` (22).
- Reproduction used output-local extracts under the exact sibling names the driver expects, plus a
  symlink of this snapshot's `candidate/` as `m2-transition-carriers-reference-203/candidate`.
  `scripts/check_primary237.py` was copied with **one line** redirected (`T`/`S`/`O`). Frozen source
  untouched. Python 3.12.13 `-I -B`.

## Integration claims

`producer-integration237.json` lists six transforms and **59** pin updates. Each `after` hash equals
the candidate file. Originals/beforeimages are present (`before-primary-producers237/`,
`before-format-integration/`, `check_primary237-before-schema-metadata.py`, `primary237-check-r1/`).

| Primary module | Component input | Transform actually observed |
|---|---|---|
| `trust_record_reference.py` | 232 r4 `reference_reader.py` `c365187a…` | Canonical path only. Body from `def target(` **equal**. ROOTS tuple equal. |
| `trust_input_reference.py` | 230 r3 `trust_inputs_model.py` `45982508…` | Header replaces `build_schema` with pinned `private-trust-state.schemas.v1.json` (`a3a0b4f4…`, 122 defs). Body from `class Work:` **equal**. |
| `trust_event_reference.py` | 235 `event_bindings.py` `af8d063a…` | Canonical path only. `bind_events` body **equal**. |
| `trust_restore_reference.py` | 235 `restore_event_bridge.py` `e699a83a…` | Imports rebound to `trust_input_reference.py` / `trust_event_reference.py` with exact hashes. Iterator body **equal**. |
| `trust_metadata_index_reference.py` | 234 `envelope_index.py` `7d2e16db…` | Schema/routes/C/kernel relocated to primary paths. `class Index` body **equal**. |
| `trust_graph_reference.py` | 236 `graph_reader.py` `617043d3…` | Pins `trust_record_reference.py` `f149dc4a…`. `class Work` / walk body **equal**. |

No stale `/tmp/opensip-implementation/m2-*-draft-*` imports remain in the six modules.

`frozen-candidate.json`: **1332** candidate files, all disk hashes match. **43** differences from the
bundled 201 candidate: 32 new files, 11 modified. Declared change set equals the actual 201 delta
(no extras, no misses).

Five pin inventories verify against candidate bytes (0 faults): foundation 1297, evaluator3 1301,
native 1297, security 1305, workflows 1298. Envelope `qualification-report.json` `sourceBindings`
(1306) also match this candidate.

Entry prose is present: `trust-reference-producers.v1.md`, `metadata-envelope-pairing.v1.md`, and
the three updated owner sections (`core-distribution-binding`, `trust-proof-node-joins`,
`trust-input-joins`). They state the same pending-effects / unshared-budget / FULL-graph / no-grant
limits this review treats as remaining scope, not silent holes.

## Producer corpus on primary modules

Redirected driver reproduced frozen `primary237-check-r2/summary.json` **key-for-key**:

| Lane | Cases |
|---|---|
| record | 63 |
| inputs | 195 |
| index | 58 |
| events | 41 |
| graph | 35 |
| restore-bridge | 5 |
| assembled schema | 122 defs, `m.D` equals the compiled bundle |
| CoreAnchor | new fixture shape-admitted; underbound old anchor **refused** |

Per-lane case lists equal the frozen r2 JSON. The only test-source edit is the documented one:
`M.SCHEMA['x-author-draft']['new']` → the literal 12 new definition names. Behavioral cases
unchanged. `primary237-check-r1/` is a partial record-only receipt (inputs died on the obsolete
author-metadata lookup); it is retained, not counted as a pass.

Existing suite **receipts** in this snapshot (not re-executed as unbounded historical audits):
foundation 231/231 PASS; native 477, pins verified; security 580/580, `sourcePinsValid` true;
workflows 2193; carrier 479; integration 1787. Signature: 168 focused, 147 composition, 1803
historical with 47 explicit payload-dispatch deltas, 55 actual crypto checks, 6000 fuzz. Those
receipts bind this candidate; they remain owner receipts, not product qualification.

## Findings

No integration defect was found in the claimed surface: sibling imports, compiled 122-schema
adoption (including 229 CoreAnchor), algorithm-body preservation, pin inventories, and candidate
delta accounting.

Remaining limits are explicit and match the 235/236 component reviews:

- Literal events return **pending** role effects; they do not authorize tokens or whole-image
  clock/heads/history/batch/continuity effects.
- Graph/proof/index budgets are **not** one operation-wide `Work`.
- Graph cached bytes assume immutable captured input; reusing `Work` is not a live re-read.
- FULL graph is **not** S4.5 / safe-ABORT narrow missing-old-T scope.
- No native custody, host actor, held-root / current revocation / time / semantic admission.
- Command registry still awaits four trust and two evidence commands (transports/locks/outcomes).
- Structural standing is never current authority.

Historical reports under `candidate/` keep their original standing; new root reports bind 237.

## Verdict

- [x] Primary modules import pinned siblings; input module drops the 110-definition builder.
- [x] Guard/iterator bodies equal the supplied component inputs.
- [x] Five pin inventories and the 43-file 201 delta check out.
- [x] Producer corpus 63/195/58/41/35/5 plus 122-def / new-vs-old anchor reproduces on primary modules.
- [ ] **Not cumulative approval, not an implementation, not an install.**

No harness failure. Construction scripts were not run against a live tree.
