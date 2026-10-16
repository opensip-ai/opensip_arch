# B2C-PLAN-r1 review

Verdict: **REQUIRED-FINDINGS**

Two required findings block acceptance of the exact plan.

## Subject and review basis

Verified subject.json: 449 bytes, SHA-256 `9162933b2ede7d5416c146029ea87311bc6793ecc13f1ef03488c35b049680b5`. Its sole member PLAN-r1.md is exactly 15286 bytes, SHA-256 `7c80cf87a1e2c10ffc0ecb477e5dbafc3fe278da699d96662efb46073f6f7a1e`.

Confirmed clean product main `c0e61a4b9ad48467430af8a5cfbe53ed7e6111c5` and architecture HEAD `ecd3c5a52a2faa10c91ac1ef96b62cde5a8152a0`; the lock has 160 inventory successors (v200 selected) and 165 contract successors. Inspected the selected contract records 81, 163 and 164, M3-B r7 item 14 and dependencies, NE's unit/configuration graph laws, B-S1's operative passages/schemas, the archived native model, public detail registry, product schema vocabulary, shared rule, identity dependencies and FW-01 check. No execution of references or tests was needed.

## Required findings

### B2CPLAN-R1-RF-1 — Internal aliases must not become public vocabulary

PLAN-r1.md:111–121 proposes adding four names to public schema/generated vocabulary through B-S10. The registry places all four in `internalAliases` (registry lines 1592–1615), and its `aliasRule` at line 1622 explicitly says these keys cannot appear in public DomainDetailCode.

| Internal decision | Existing public target |
| --- | --- |
| native.explicit-root-grammar | PROJECT.EXPLICIT_PATH_INVALID |
| native.explicit-root-crosses-boundary | PROJECT.EXPLICIT_PATH_INVALID |
| native.boundary-inventory-mismatch | PROJECT.DISCOVERY_INVENTORY_MISMATCH |
| native.too-many-units | PROJECT.WORKSPACE_UNIT_LIMIT |

All three targets already exist in the product schema. Their absence under the internal spellings is intentional. Section 2.1's refusal paragraph also misclassifies these spellings as registered public details.

Remove this proposed public vocabulary expansion and the alleged gap. Plan the normalization boundary and controls that prove each internal refusal reaches its registered existing public route. Revise B2-c0 and its sequence accordingly. B-S10's materialization route does not authorize publishing internal aliases as new public members.

### B2CPLAN-R1-RF-2 — V3 input requires the selected V3 output and join semantics

PLAN-r1.md:47–50 describes projecting historical input fields into the old model; line 70 explicitly promises UnitDiscoveryV2 output. B-S1's selected additions instead require UnitDiscoveryV3, PrunedTreeV3 and UnitBoundariesV2, including memberRepositories. Its PASSAGES replaces the U-4a V2 output (lines 215–227) and adds the U-8 member-consistency condition (line 298).

This matters immediately: the bound shared rule emits the SX-1 `opensip-custody-state` reason, which the old V2 pruned-tree schema cannot admit. With admitted members, dropping memberRepositories also loses required provenance and the check rejecting a nested vcs-tree anchor whose parent is not an admitted member. Deferring B3-b readers does not permit discarding fields or weakening the current admitted-input contract.

Specify the wrapper's current V3 output adaptation and the product's corresponding output admission, preserving the selected SX-1/member rules and all admitted fields. Historical V1/V2 replay remains separate. Add explicit current vectors for root `.opensip` with no members, admitted-member carry-through and a missing-member vcs-tree mismatch. B3-b still owns obtaining members and implementing readers.

## Other review conclusions

The overall intended separation of pure discovery from C1 inventory/custody, J1 production composition, B2-d recognition/YAML and B3-b readers is appropriate. U-5/U-6 joining remains owned by H/J under item 14; B supplies records. The marker/file-list inputs, shared-rule consumption through a narrow typed public security API, the identity TOML helper, FW-01 extension and planted negatives, cap/scope vectors and joint U-8 sweep are reasonable designs. Confirmed the current shared-rule API/module is crate-private and the identity crate pins toml =0.9.9; the required public API addition must remain explicit.

A current reference wrapper is needed, but the proposed adaptation is incomplete for the reasons in RF-2. There are exactly 26 units-* cases. The missing DD import path and V1/V2 dispatch are real. The model already performs the subset test in executable code; the quoted equality is a stale docstring, not evidence that the current algorithm still compares whole rows. The wrapper must also supply its complete pinned loading closure, since the archived file's adjacent foundation/schema/capability dependencies are absent at the naive relative paths (NBO-1).

The pre-Plan extends resolver needs a separately accepted law decision: the selected graph record describes resolved edges and effective option precedence but does not provide the proposed filesystem lookup algorithm. Data-only resolution under C1 custody, no provider/fetch before the Plan, explicit unresolved handling, bounded files/graph and cycle refusal are sound directions within such a law revision. This review does not approve unpublished r8 text. Its separate review should close exact resolution ordering/grammar and the disclosure carrier: UnitDiscoveryV3 is closed and has no unresolvedChoices field today (NBO-2).

Treating a missing operational inventory as an internal host-composition fault is a sound recommendation for the separately reviewed law step; absence from public aliases alone does not authorize an arbitrary new public detail. Keep its decision key/route and any change to the existing named invariant explicit. B2-c1 can technically consume an already-effective allowJs input while the resolver law is reviewed. The overall sequence as written is not sound because it first publishes the incorrect vocabulary expansion and incomplete V3 reference. Correct those prerequisites, and ensure any r8-dependent invariant change is not implemented early.

No product code, binding or law change is made or accepted here. No qualification is granted.

## Boundaries

Wrote only REVIEW.md and review.json in the requested directory. Neither repository, stage nor control files were edited. Used only read-only inspection, hashing, JSON parsing and Git queries. No Cargo, tests, builds, lane, network, other panes or delegation; no private fixture, installation directory, signing keys, held trees or T2 held-out source was accessed.
