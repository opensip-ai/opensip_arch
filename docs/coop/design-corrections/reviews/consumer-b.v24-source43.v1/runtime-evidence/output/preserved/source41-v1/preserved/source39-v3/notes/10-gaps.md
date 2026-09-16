# Phase 10: design gaps, algorithm freedom and blockers (R-IDENTIFY-GAPS, R-FREEDOM-VS-MISSING, R-BLOCKER-NOT-ADJUST) — source39.v3

This is the adjudication of the source39.v2 self-audit, completed in runtime source39.v3 on the unchanged source39 kit. The kit's
manifest is `c2f2f88d…`, it has 104 members, and its rows are identical to v1 and v2 (`vectors/phase0-custody.json`,
`runs/final-custody.json`). It replaces `preserved/source39-v1/notes/10-gaps.md` as current adjudication; the v1 note stays
own history.

## Adjudication rules (unchanged)

- **Algorithm freedom.** The kit fixes the observable result, and hosts may reach it any way they like. Freedom is not an issue.
- **Missing or contradictory contract.** It is a design gap when two conforming readers of the selected kit would do any of the following:
  - mint different identity-bearing bytes;
  - admit different Runs;
  - produce different public results;
  - be unable to represent a required public field without inventing one.
- **Severity.**
  - **MUST:** a lawful required result is unreachable, a valid Run is unclosable, or identity-bearing bytes are undetermined.
  - **SHOULD:** a public or cross-host result is undetermined or contradictory, but bounded.
  - **Advisory:** internal naming, disclosed drift, an unreachable but deterministic branch, or a wording/scoping note with a deterministic reading.
- **Helper bugs are not gaps.** A helper failure with a precise kit answer is corrected, and the original failure is preserved. Records:
  - `tools/hc_v2.py`: HC-33..HC-36 were made in v2 and HC-37..HC-38 in v3;
  - `preserved/source39-v1/tools/hc_source39.py`: HC-14..HC-32.
- **Evidence standard.** Every item was checked against the source39 selector. No author model, prior review or root artifact is an oracle.

## MUST

### s39-M1 (carried, unresolved) — U-4b assigns no `unitKind` to a tsjs unit, but UnitMembershipV1 is identity

**Selectors**
- native-evidence.md lines 730-732 (U-4b): "`UnitMembershipV1` enters `PlanId` through `membershipDigest`, so every choice below is identity and none is left to an implementation".
- native-evidence.md lines 744-748 (U-4b.2) give a tsjs unit its marker, mode, `recognizerId` and `recognizerVersion`, but no `unitKind`.
- By contrast, lines 739-740 assign rust `unitKind` and lines 854-855 assign the fallback `unitKind`.
- native-evidence.md line 622 and `native/native-evidence.schemas.v2.json#/$defs/WorkspaceUnitV2/properties/unitKind` publish the enum `ts-program|js-program` with no mapping.
- `foundation/enumeration-plan.schema.v1.json` `membershipDigest` → analysis-spec parameter → `analysisSpecDigest` → PlanId.

**Measured.** `vectors/discovery-membership.json#u4b-tsjs-unit-kind-not-assigned` was re-executed in v2 (`logs/v2-disc-mode.0.discovery_vectors.log`), and its document is equal to v1's.
- One `js-allowjs` unit, spelled `js-program` and `ts-program`:
  - both are schema-valid;
  - both pass `ENUMERATION_MEMBERSHIP_ORDER` / `_ROW_DERIVATION`;
  - they mint different `membershipDigest` values (`34d0e48f…` vs `52a0e505…`), and so different PlanIds.

**Gap.** Two conforming hosts mint different PlanIds for one repository.

**Status.** No new normative owner was supplied, so the finding stays MUST and CHANGES_REQUIRED.
- Reconstruction choice: `ts-tsconfig` → `ts-program`; `js-allowjs` / `js-synthesized` → `js-program` (`ref/membership.py`).
- This review invents no mapping.

## SHOULD

None.

## Advisories

**Carried from source39.v1.** The kit is unchanged, and the measurements were re-executed in v2 or v3.
- **A-c1.** Some internal refusal names are unpublished and still carry `cb24` names:
  - syntax grammar-capability scope mismatch and undisclosed variants;
  - E0 pivot joins;
  - detector listing refusals;
  - test consent relabel;
  - native-preparation grant joins.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination. This is a live successor-artifact obligation (native s10 lines 3285-3299).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change, so gating evidence rules attribute INDETERMINATE `evidence-content-changed` (workflows s3 lines 440-449).
- **A-n1.** Closed per-entry IndeterminateReason order: reason (3), the detector disposition, is unreachable for entries (workflows s3 lines 402-411).
- **A-n2.** Run-termination s6 order vs members: `errorCode`/`faultCause`/`signal` can be read as UNKNOWN_FIELD or NOT_DERIVED. Both readings refuse.
- **A-n3.** Run-termination: a non-object candidate has no published key; the `…_UNEXPLAINED_INDETERMINATE_*` name is a wildcard.
- **A-n4.** Run-termination s7.3 commit-inventory member set is fixed "as the reference commit path inventories them". Operational, and outside Run identity.
- **A-n5.** U-4b.2 "deepest workspace" is self-referential for nested workspaces. Cargo rejects those; unmeasured.
- **A-n6.** U-4b does not restate a rust unit's languageMode; it is derivable from the mode table.

**New in the source39.v2/v3 self-audit**
- **A-v2-1. Typed-prefix closure boundary for workflow-owned Plan input documents.**
  - Composition s7 line 74 closes typed-prefix references of *outputs*.
  - The kit does not say whether schema-declared typed-prefix values inside workflow-owned Plan inputs are closure references. Examples: WaiverSetV1 `target.fingerprint` (finding-key2) and PolicyDocumentV2 import addresses.
  - Measured (`logs/v2-build.4.from_scratch.log`): a literal "every owning schema" reading makes lawful `cmp-empty` and `cmp-budget` unclosable. Each has a fingerprint waiver whose finding never occurs.
  - The deterministic reading comes from s7 "these outputs", s5 waiver equality and identity s3 lines 597-600/627-631 (HC-36). One scoping sentence would settle it.
- **A-v2-2. `policy-derivation3` is outside the reachable output set.**
  - It is constructed (s7 line 70, s9.7), but no run3/seal3/evidence3/proof3 field references it.
  - Reachable-set equality (s7 line 76) therefore cannot include it, and its retention is not required by that law.
  - Exports retain it as an unreachable, non-authoritative frame.
- **A-v2-3. "Closed" representation and retention wording in identity s3 vs the bundle digest laws.**
  - Identity s3 lines 441-467 call the representations and retention modes closed, and close `derived` / `owner-retained` to single identity fields.
  - The native and relation `x-opensip-digest-law` vocabularies publish further modes and representations (census counts in `vectors/reference-census.json`).
  - Each bundle's own law is the deterministic owner; the sentence reads as scoped to identity-schemas.v3.
  - A literal cross-bundle reading would refuse lawful native and relation fields.

## Limitations of this reconstruction (not gaps)

- **Run-termination.** s7.5 row 2 and s5 stage-terminal carriers are not constructed from built Runs (`vectors/run-termination.json#/notConstructedFromBuiltRuns`).
- **Absent reference implementation.** `docs/coop/design-corrections/discovery-defaults.py` is a reference implementation that native U-4a governs by text. Its absence is not a custody gap.
- **Walker scope** (`ref/retained_graph.py`).
  - Executed: retention, identity, schema and registry joins, closure membership/kinds, selected imports (HC-37), and SourceUnitOwnershipV1 `unitId` derivation (HC-38).
  - Delegated to owner graph admission, which runs as its own stage and names each item:
    - `languageVersionBinding` derivation;
    - clones body-identity parse joins;
    - native context/universe admission and binding (including the rust universe `configProjectionSha256` join, which `domainSets` does not list);
    - enumeration and execution-input derivation.
- **Census classes with no constructed positive.** `canonical-record/owner-retained`, `raw-artifact/owner-retained` and `snapshot-path/not-joined` have no positive graph and no negative. They are not claimed.
- **Result provenance.** Some results were measured in source39.v2 and reused in v3, with evidence (`notes/12-v3-completion.md`).
- **Future qualification** was not performed: real OS/compiler/crypto/SQLite, provider execution as enforcement, host authentication and synthetic TCB.

## Blocker statement (R-BLOCKER-NOT-ADJUST)

No gap blocked a promised vector.
- Where a recipe was missing (s39-M1), the choice is recorded beside its measured alternative.
- Where the kit gave a precise answer to a helper defect (HC-33..HC-38), the helper was corrected and the original failure preserved.
- No meaning was adjusted, and no author code was imported.

One MUST gap remains, so the verdict cannot be ACCEPT-RECONSTRUCTABLE. It is CHANGES_REQUIRED, not BLOCKED.
