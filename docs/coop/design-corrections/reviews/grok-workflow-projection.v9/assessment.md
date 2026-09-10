I'll continue on the owned workflow3 files only, starting by reading the v8 presence/pivot code, the advertised declared-compatible law, and the current inventory/schema joins.I have the presence and detector-join laws. Next I’ll implement per-fingerprint absence knowledge, pivot-only fingerprints in the comparison universe, and the truthful declared-compatible limitation.Three v9 controls failed. I'll inspect the optional-unknown and partial-pivot graphs to see why.v9 is on the same owned workflow3 files. Reports are only under `grok-workflow-projection.v9/`. Historical v8 review and `root-clarification.txt` were not overwritten. This is still bounded projection work, not complete admission.

**Receipt:** 322/322 at `/tmp/opensip-design-corrections/grok-workflow-projection.v9/workflow-projection-check.json`. v8 remains 292. Counts are not acceptance. Root remints still PASS `open_run_closure` and REFUSE complete semantic close. Main execution v5 is active and not treated as finished wiring. `command-inventory.v1.json` was not edited.

### 1. Absence knowledge
Pivot presence is no longer enumeration-complete ⇒ whole-axis available/false. Per fingerprint/rule:

- **true** — known matched hit (including waived)
- **false** — only when that rule can prove a complete negative
- **null** — otherwise (incomplete population, indeterminate predicate, budget-exhausted, required execution failure, import unknown, disabled, advisory `outcome=pass`)

A known hit stays usable when another row is unknown. Native control: two-subject runtime baseline, partial one-subject E1; known `src/index.ts` stays E1 true; the other fingerprint is null, not false absence.

### 2. Pivot-only fingerprints
Comparison universe is baseline entries ∪ current matched occurrences ∪ bound pivot hits, with admitted pivot `(ruleId, detectorId)` metadata (not caller flags).

Native control: unmatched-symbol empty baseline, `enabled=False` current, `enabled=True` E1. The E1-only fingerprint is **CODE-NET-NEW** with subsequent **policy**. Disabled current does not drop that fingerprint or erase baseline unmatched gating.

### 3. `declared-compatible` standing (not implemented as a join)

workflows-and-surfaces §2 already requires the current detector’s **signed manifest** to list the baseline `closure2` at the same major, resolved under current trust (retained generation, installed signed release, or signed closureBundle). `compare_admitted` still refuses every caller `compatibleWith` map. That is the untrusted-input boundary, not an authenticated declaration.

There is no retained detector-manifest schema or security/release admission that projects a `compatibleClosures` listing. This unit does not invent `signatureVerified` booleans. **Proposed typed contract:** identity/release-owned detector manifest (bytes at `closure.manifestDigest`) with explicit `compatibleClosures` of `closure2` ids at the same `semanticsMajor`, admitted only via the §2 current-trust trio; workflows join that listing; request maps stay refused. Standing: advertised, not implemented as an authenticated join. Details: `declared-compatible-standing.v9.md`.

### 4. Policy-derivation clarification (v8 review kept)
`derive_policy_result` already calls `replay` (owner closure, Plan policy/waiver/import reconstruction, complete proof compare). Those joins are inherited transitively; they are not a new gap. `planId`/`proofBundleId` transitively bind snapshot/detector/scope/results; redundant fields are not required. The API projects an admitted Run, not a substitute-policy operation. Root’s second real Plan control is the right next check; remint-field mirrors are not necessary without a demonstrated failure. New file only: `policy-derivation-clarification.v9.md`.

### 5. Waived matched presence
Preserved. E4/E0–E3 remain any matched occurrence; `waivedC` is separate. Matches `root-clarification.txt`.

### 6. Command-inventory joins (v1 instance untouched)

| Surface | What it is now |
|---|---|
| `workflows/command-inventory.v1.json` | schemaMajor **1**, json renderer **version 2** / CommandEnvelope major **2**, golden `envelope-major-unsupported` still says pin schemaMajor **2** |
| `schemas/evaluator3/command-inventory.schema.json` | schemaMajor **3**, findings parity FindingSurface |
| Checker | loads inventory:3 schema, does **not** validate the v1 instance against it |
| Remaining joins | json renderer 2 vs envelope:3; v1 golden major 2 vs envelope:3; v1 parity token `findings` vs FindingSurface / sarif-adapter:2 |

Root will mint the version-3 inventory from unchanged commands plus JSON renderer 3 / envelope 3. Exact list: `command-inventory-joins.v9.md`.
