I'll copy the frozen digest, membership, and suffix-table patterns first, then write the three draft files to the isolated successor tree.I have the digest, order, and membership selectors. Next I’ll add only the three draft files and a v6 validation helper.Writing the two schemas and the contract appendix next, then a v6 shape-validation helper.Draft-only successor files are in place. Frozen21 and the live repo were not modified. Shape validation is 9 PASS / 6 REFUSED (not Run admission).

## Written (owned paths)

| Path | Bytes | SHA-256 |
|---|---:|---|
| `/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json` | 18596 | `f8eaa3e4026bbb7fac845e8421ecff8e95a6b6c89a495f41c39477020dd480c0` |
| `/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json` | 14405 | `2ba6ce7eff4f9f8e8a6bd44c41bec1675418a577c1c2853f3593e1a63a1c7a85` |
| `/tmp/opensip-design-corrections/evaluator-successor.v1/docs/coop/design-corrections/foundation/enumeration-contract.v1.md` | 10795 | `417a20307f7e620e2c730880020b16307ba3b0fe0eb8f5579162da4d8148d0ac` |

Helpers only under `/tmp/opensip-design-corrections/grok-subject-assessment.v6/` (`validate-enumeration-draft.py`, `validation-report.json`, `hashes.json`). Python: `/tmp/opensip-architecture-review-env/bin/python -I -B` + successor `canonical.py` ExactValidator.

## Root A–G as implemented

- **A.** Separate foundation parameter document; identity is raw `C(EnumerationPlanV1)`. No `planId` / `analysisSpecDigest`. Cells = requestedCapabilities tuples including `required`, ordered `{by:[capabilityId,languageMode,workspaceRoot]}`, max 1024. `kinds` stored on the cell. **Program bindings array**, not `requestedCapabilities.programEntry`. U-1 is `provenance=default-unit`; extras are `explicit-plan-selection` with `programEntry`.
- **B.** Available bindings pin universe H + context H + selected provider + per-kind extents **before Plan**. Unavailable bindings keep `universe: null`. Multiple bindings per cell allowed. Changed context/universe ⇒ new Plan.
- **C.** One `SubjectInventoryV1` per `(cellOrdinal, programOrdinal, kind)` located by `planId` + `parameterDigest` + ordinals + kind. Partial inventories still carry evaluating rows. Unavailable has no rows. File complete-empty only if file extent is empty.
- **D.** Per-kind extents. File includes data/unsupported/extensionless. Symbol is code scope. Packages first-party manifests. Membership/reason enums match `FileMembershipRowV1`. Root `.` is `Text`.
- **E.** Closed suffix table in the inventory schema; package language is json/toml format. No invented unbundled table (`unspecified`). Symbol `projections[]` is `{closureId, signatureTokens}` bound to detector `ruleClosure`. Empty projections = unavailable GR6, not `[]` file identity.
- **F.** Closed objects, `ordinal` integers, explicit nulls, supported `x-opensip-order` values, max **128 programs/cell** (not context 128). New faults labelled **NEW/internal**.
- **G.** Bare 64-hex fields carry `x-opensip-digest`. Universe/context remain `h-identity` + existing `domainSets`. New records are canonical-record preimages. Membership via native **document+selector**, not a second parameter `$def`.

## Remaining (not claimed done)

File totality, examined⊆extent, universe↔context rebind, and `kinds`↔extents equality are **closure joins**, not fully schema-enforced. Copied `DeficiencyV2`/`NativeCause` enums can drift. Payload-registry row, ProofInputRef, and public `ENUMERATION_*` routes are for root. GR6 hashing, G3–G9, majors remain open. `required` stays a boolean because it copies the existing ownership field.

No source acceptance. Root integrates proof/finding/waiver/atoms.
