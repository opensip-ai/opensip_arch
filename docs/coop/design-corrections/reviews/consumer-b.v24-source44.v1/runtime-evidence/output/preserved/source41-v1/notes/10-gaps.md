# Phase 10 — gaps, contradictions and readings under the source41 kit (runtime source41.v1)

This is my own adjudication for the source41 kit. The source39.v3 version is preserved at `preserved/source39-v3/notes/10-gaps.md` and is history, not current evidence.

## Adjudication rules

- **Missing or contradictory law.**
  - MUST: a required record, identity or refusal cannot be determined from the kit, so two conforming hosts would disagree.
  - SHOULD: the kit determines the answer, but a normative sentence contradicts another one in a way a careful implementer could follow into a different result.
  - Advisory: wording, naming or scoping that does not change a determinate result, or an obligation the kit itself discloses.
- **Algorithm freedom is not a gap.** Where a published law fixes the result and leaves the algorithm open, the reconstruction's algorithm is a free choice. It is not reported.
- **Helper bugs are not gaps.** A helper failure with a precise kit answer is corrected as a numbered HC, and the original failure is preserved (`tools/hc_source41.py`, HC-39..HC-45).
- **Evidence standard.**
  - Every item is checked against a source41 selector and, where it can be, measured by an executed vector or Run.
  - No author model, fixture, prior review or root artifact is an oracle.
  - Readings adopted where text is ambiguous are named with their measured alternative.

## MUST

None.

## SHOULD

None.

## Disposition of my source39.v3 findings under the source41 kit

| Finding | Disposition | Source41 selector | Measured |
|---|---|---|---|
| s39-M1 (tsjs `unitKind` not assigned although UnitMembershipV1 is identity) | **Resolved by the kit.** Helper enforcement added (HC-39). | native-evidence.md lines 755-760 (U-4b.2: `ts-program` exactly for `ts-tsconfig`; `js-program` for `js-allowjs` and `js-synthesized`), 797-799 (U-4b.5) | `vectors/discovery-membership.json#u4b-tsjs-unit-kind-projection`: the source39 alternative is still schema-valid and now refuses `ENUMERATION_MEMBERSHIP_ORDER:unitKind:0`; only the projection admits. The unchanged helper admitted it (`logs/s41-original-disc.0`). Run closure: `runs/ts-pass~unit-kind-not-mode-projection`. |
| A-n2 (`errorCode`/`faultCause`/`signal`: UNKNOWN_FIELD or NOT_DERIVED) | Resolved by the kit | run-termination s6 step 2, lines 174-176 | `vectors/run-termination.json#fault-cause-present` refuses `RUN_TERMINATION_NOT_DERIVED` |
| A-n3 (non-object key unpublished; `_RULE`/`_RUN` wildcard) | Resolved by the kit; key adopted (HC-41) | run-termination line 173; lines 85-87 | `vectors/run-termination.json#non-object` |
| A-n4 (commit-inventory member order "as the reference commit path inventories them") | Resolved by the kit | run-termination s7.3 lines 246-253; identity-schemas.v3 `#/$defs/commit-inventory` `x-opensip-order: canonical-set` | receipt-inventory controls in `vectors/run-termination.json` |
| A-n5 (nested Cargo workspace folding self-referential) | Resolved by the kit | native lines 747-754 | `vectors/discovery-membership.json#u4b-nested-cargo-workspace` (the unchanged helper gives the same units) |
| A-c1, A-c2, A-c3, A-n1, A-n6, A-v2-1, A-v2-2, A-v2-3 | Carried as advisories (below) | re-located selectors below | as below |

## Advisories

- **A-c1.** Internal refusal names that no kit owner publishes are still spelled `cb24.*`. `blind-review.json#/advisories` lists the exact measured set emitted by `ref/*.py`.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination. The successor D9 artifact is a live cross-unit obligation that the kit discloses (native lines 3313-3327; `vectors/d9-extension-precedence.json`).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change, so gating evidence rules attribute INDETERMINATE `evidence-content-changed` (workflows s3 lines 440-449; `runs/cmp-code-det2`).
- **A-n1.** In the closed per-entry IndeterminateReason order (workflows s3 lines 402-411), reason (3), the detector disposition, is unreachable for entries. An indeterminate detector leaves the changed-detector E0 presence `null`, so (1) applies first (`vectors/baseline-e0-e3.json`).
- **A-n6 (re-examined under source41).** A rust unit's `languageMode` (`rust-cargo` vs `rust-cargo-prepared`) enters `membershipDigest` and, through the matrix-fixed default (lines 1070-1072), the requested capability rows.
  - **Why it is determinate.** The mode table decides it after U-1 (lines 165-166, 169-172): an admitted inert, non-stale `PreparedOutputSetV3`, with prepared mode selected explicitly or defaulted (PO-1, lines 1842-1847). Two hosts with the same admitted inputs spell it the same way, which is why this is not a MUST like s39-M1.
  - **What is missing.** U-4b.2 (lines 741-746) does not restate the rust mode, and U-4b.5 (lines 797-799) publishes retained-record enforcement only for the tsjs `unitKind` projection. No closure refusal exists for a mis-spelled rust mode, so none is implemented (`vectors/mode-rust-cargo-prepared.json`).
- **A-v2-1.** Composition s7 closes typed-prefix references of outputs. It does not say whether typed-prefix values inside workflow-owned Plan input documents are closure references.
  - The deterministic reading HC-36 adopted still applies: s7 line 74 "these outputs", s5 line 54, identity lines 597-600 and 627-631.
  - `cmp-empty` and `cmp-budget` admit under it.
- **A-v2-2.** `policy-derivation3` is a composition output that nothing reachable references. Reachable output-set equality cannot include it, and exports retain it as an unreachable non-authoritative frame (`runs/<run>.replay.fromscratch.json#/retainedClosure/unreachableRetained`).
- **A-v2-3.** Identity s3 (lines 441-467) calls the four representations and retention modes closed. The native and relation bundles publish their own `x-opensip-digest-law` vocabularies, and each bundle's own law owns its positions (`vectors/reference-census.json`).
- **A-s41-1 (new).** run-termination s7.6 step 1 (line 330), "A non-object refuses", names no key. s6 step 1 (line 173) publishes `RUN_TERMINATION_CANDIDATE_NOT_OBJECT` for the projection check. The reconstruction applies the s6 key at both boundaries. Both readings refuse; only the internal key could differ.
- **A-s41-2 (new).** U-1 (native lines 656-659) says an omitted value "defaults to false for a `tsconfig.json` entry". s1.2 (lines 524-526) instead derives an omitted `allowJs` from the effective `checkJs`, and lines 562-563 say `checkJs` can affect membership through that default.
  - The mode table (line 162) keys `ts-tsconfig` on the effective value.
  - The s1.2 derivation is applied: a `tsconfig.json` with `checkJs:true` selects `js-allowjs` (`vectors/discovery-membership.json#s12-effective-allowjs-mode-selection`, case `tsconfig-checkjs-true`).
  - Reading U-1's clause literally would give `ts-tsconfig` and a different `membershipDigest`. That is why it is recorded, although the s1.2 text and the mode table decide it.

## Kit changes exercised, and what required invention

Law by law, the source41 deltas and their measured outcomes are in `notes/01-source41-law-deltas.md`. Nothing required inventing a record, identity or refusal. Four places needed a named reading, each with its alternative measured or stated:
- A-s41-1 (the key at s7.6);
- A-s41-2 (s1.2 over U-1's wording);
- A-v2-1 (the typed-prefix closure scope);
- A-n6 (the rust unit mode from the mode table).

The PolicyTestSuiteV2 schema changed in source41. No original requirement constructs it, and it was read but not exercised.
