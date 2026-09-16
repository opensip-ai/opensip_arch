# Phase 10: design gaps, algorithm freedom and blockers (R-IDENTIFY-GAPS, R-FREEDOM-VS-MISSING, R-BLOCKER-NOT-ADJUST), source39

## Adjudication rules (unchanged from this origin's prior work)

- **Algorithm freedom.** The kit fixes the observable result, and hosts may reach it any way they like: accelerator, BFS implementation, store layout, parsing strategy behind admitted canonical bytes. Freedom is not an issue.
- **Missing or contradictory contract.** The test is whether two conforming readers of the selected kit would do any of the following:
  - mint different identity-bearing bytes;
  - admit different Runs;
  - produce different public results;
  - be unable to represent a required public field without inventing one.

  If so, it is a design gap.
- **Severity.**
  - **MUST:** a lawful required result is unreachable, a valid Run is unclosable, or identity-bearing bytes are undetermined.
  - **SHOULD:** a public or cross-host result is undetermined or contradictory, but bounded.
  - **Advisory:** internal naming, disclosed drift, an unreachable-but-deterministic branch, or a process note.
- **Helper bugs are not gaps.** Every source39 helper failure was corrected from the kit, with the original preserved: HC-14..HC-32 in `tools/hc_source39.py`, `preserved/s39-original/`, `preserved/s39-tool-error/`, and `logs/s39-*`.
- **Evidence standard.** Every item was re-verified against the source39 selector in this session. Findings are measured where measurable. No author model and no prior review is an oracle; the prior runtime is own history only.

## MUST

### s39-M1 U-4b assigns no `unitKind` to a tsjs unit, but UnitMembershipV1 is identity

**Selectors**
- native-evidence.md lines 730-732 (U-4b): "`UnitMembershipV1` enters `PlanId` through `membershipDigest`, so every choice below is identity and none is left to an implementation".
- native-evidence.md lines 744-748 (U-4b.2) gives a tsjs unit its marker (first present of tsconfig/jsconfig/package.json), its mode (U-1), its `recognizerId` (`typescript-config` / `node-package`) and `recognizerVersion` 1. It assigns no `unitKind`.
- By contrast, lines 739-740 assign rust `unitKind` (`cargo-workspace` / `cargo-package`), and lines 854-855 assign the fallback `unitKind` `syntax-only`.
- native-evidence.md line 622 and `native/native-evidence.schemas.v2.json#/$defs/WorkspaceUnitV2/properties/unitKind` publish the enum `ts-program|js-program` with no mapping. A kit-wide search finds no other occurrence.
- `foundation/enumeration-plan.schema.v1.json` `membershipDigest` is the raw SHA-256 of C(UnitMembershipV1), which feeds the analysis-spec parameter, then `analysisSpecDigest`, then PlanId.

**Measured** (`vectors/discovery-membership.json#u4b-tsjs-unit-kind-not-assigned`, `tools/discovery_vectors.py`)
- One repository: `tsconfig.json` with `allowJs`, plus `src/a.ts` and `src/b.js`, giving a `js-allowjs` unit.
- Its membership record spelled with `unitKind` `js-program` and with `ts-program`:
  - both admit against `UnitMembershipV1`;
  - both pass every published U-4b.5 enforcement check (`ENUMERATION_MEMBERSHIP_ORDER`, `ENUMERATION_MEMBERSHIP_ROW_DERIVATION`);
  - they mint different `membershipDigest` values (`34d0e48f…` vs `52a0e505…`), and so different PlanIds.

**Gap.** Two conforming hosts mint different PlanIds for one repository, which is exactly what U-4b promises cannot happen.
- `ts-tsconfig`/`ts-program` and `js-synthesized`/`js-program` are only name-suggestive.
- A tsconfig with `allowJs` (mode `js-allowjs`, recognizer `typescript-config`) has no determinate kind.

**Reconstruction choice.** `ts-tsconfig` → `ts-program`; `js-allowjs` and `js-synthesized` → `js-program` (`ref/membership.py`). The alternative is recorded beside it. The remedy belongs to the kit: one mapping row in U-4b.2.

## SHOULD

None remain.

## Disposition of this origin's prior issues under source39

| Prior | Disposition | Source39 selector | Measured |
|---|---|---|---|
| M1 clones census | resolved | identity `bodyEligibilityLaw`; execution-inputs s5; native lines 931-945 | `ts-clones-required` and `syntax-mixed-omitted` seal pass; `rust-mixed-clones-required` pass under the closed `.rs` set |
| M2 nodeDigest policy-1 Predicate | resolved | identity-schemas.v3 `program-predicate.nodeDigest` names `policy-document.v2.schema.json#/$defs/Predicate` | `syntax-code~explicit-endpoint-source` ADMIT |
| M3 membership order | resolved, except the tsjs `unitKind` remainder (s39-M1) | native U-4b lines 730-787 | `syntax-code~membership-reordered` refuses `ENUMERATION_MEMBERSHIP_ORDER:rows`; `vectors/discovery-membership.json` |
| M4 detectorId | resolved | workflows lines 277-287; projection contract s11 line 192 | `vectors/baseline-audit.json` |
| M5 query-response carrier | resolved | workflows lines 1197-1239; command-envelope `querySurface`/`queryResponse`; inventory `parityPaths` | `vectors/graph-query.json#/measuredQueryResponseCarrier` (probe admitted) |
| S1 stage output registry | resolved | identity lines 1303-1325; stage-spec `outputSchemaDigest.registeredBy` | `syntax-code~stage-output-schema-relation-doc` refuses `STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH` |
| S2 level-spec custody | resolved | identity lines 1065-1089; `normalizationSpecificationLaw` | `syntax-code~clone-level-spec-not-in-grammar` refuses `BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE`; `vectors/clones-negatives.json` |
| S3 zero-config syntax-only | resolved | native U-9 lines 851-877 | `vectors/discovery-membership.json#u9-*`; syntax Runs carry the DEFAULTED fallback unit |
| S4 account targetUniverse | resolved | execution-inputs s5 ("one canonical value: null"); schema type null | all 26 ported Runs refused before HC-14 (`logs/s39-original-closure.0.from_scratch.log`) |
| S5 argvDigest | resolved | workflows lines 1056-1064; security line 1074 | `vectors/test-prep-repair-authorization.json` |
| S6 failure goldens without detail | resolved | command-inventory.v3 goldens | `envelopes/public-termination.json` (45/45, none without detail) |
| S7 unknown absence reason | resolved | workflows s3 lines 376-411; evaluator3 comparison-result `IndeterminateReason`, `RuleCoverage.absenceKnowledge`, `PivotPresence` | `vectors/comparison-absence-knowledge.json` |
| A1 unannotated digests | resolved | execution-inputs.schema.v1 and incoming-search.schema.v1 annotate their digest fields | `runs/<run>.records.json` digest law |
| A2 v2 owner drift | resolved | no `identity-schemas.v2` owner names remain | kit search |
| A3 file count prose | resolved | charter counts requirements, not files; manifest 104 files | `runs/final-custody.json` |
| A4 pruned-tree bytes | resolved | identity lines 548-593; security lines 266-279 | `ts-pass` read row; `ts-pass~pruned-read-*` |
| A5 TS universe flags | resolved | native lines 537-540 | HC-20 |
| A6 correspondence reason | resolved | composition s4 (single first-applicable cause) | replay of every positive |
| A7 viewDigests standing | resolved | execution-inputs.schema.v1 `CellProgramOutcomeV1.viewDigests` ("must equal captured receipt views") | closure `XI.admit` |
| A8 unnamed internal keys | partly carried (A-c1) | query projectId row now published (s7) | see advisories |
| A9 required import vs root | resolved | composition s5 (required-import deficiency makes a gating rule indeterminate whatever its root value) | `vectors/comparison-missing.json` |
| A10 D9 successor artifact | carried (A-c2) | native s10 lines 3285-3299 | `vectors/d9-extension-precedence.json` |
| A11 ENFORCED-PLATFORM | resolved | workflows lines 1070-1074 | — |
| A12 gateReason detector hide | resolved | evaluator3 comparison-result `gateReason` description; workflows lines 460-463 | `vectors/pivot-only-fingerprints.json` |
| A13 projection failure detail | resolved | workflows lines 1130, 1207-1208, 1372; registry `DELIVERY.REQUIRED_PROJECTION_FAILED` | `envelopes/purge-replay-output-failure.json` |
| A14 exact-snapshot evidence churn | carried (A-c3) | workflows s3 lines 440-449; line 508 | `cmp-code-det2` |

## Advisories

**Carried**
- **A-c1.** Some internal refusal names are still unpublished and carry cb24 names:
  - the syntax grammar-capability scope mismatch and undisclosed variants (only `SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE` / `_FACT` are named, native s1.2);
  - E0 pivot joins;
  - detector compatibility listing refusals;
  - the test consent relabel;
  - native-preparation grant joins.
- **A-c2.** The inherited `d9-exit-contract.v1.14` alone refuses the selected `host-invariant` termination. The kit records a live cross-unit successor-artifact obligation (native s10 lines 3285-3299).
- **A-c3.** Exact-snapshot import correspondence changes `import2` on every source change. Under the evidence axis (workflows s3 lines 440-449), any gating evidence rule then attributes `INDETERMINATE` (`evidence-content-changed`). This is a designed consequence, measured in `cmp-code-det2`.

**New in source39**
- **A-n1. Closed per-entry IndeterminateReason order: reason (3) is unreachable.** Workflows s3 lines 402-411 order the reasons (1) a changed axis's pivot presence null, …, (3) the detector disposition's own reason when its method is `indeterminate`.
  - A detector whose method is `indeterminate` never runs E0, so the changed detector map's E0 presence is null and (1) always applies first.
  - The disposition keeps its own reason, and entries publish `pivot-reevaluation-unavailable`. Measured: `vectors/baseline-e0-e3.json` det2 without E0.
  - Deterministic, so advisory. The member is dead for entries, and the whole-comparison `BASELINE.RECIPE_UNSUPPORTED` termination must be read from the dispositions.
- **A-n2. Run-termination s6 check order vs members.** Step 2 refuses "a member outside the projection and delegated members" (`RUN_TERMINATION_UNKNOWN_FIELD`), while step 3 lists "any `errorCode`, `faultCause` or `signal`" under `RUN_TERMINATION_NOT_DERIVED` (run-termination-contract lines 168-176, s1 lines 34-35).
  - A checker reading `errorCode` as outside the projection reports UNKNOWN_FIELD.
  - One reading it as a projection-governed member reports NOT_DERIVED.
  - Both refuse. This reconstruction reads them as governed (`ref/run_termination.py`).
- **A-n3. Run-termination unnamed keys.** Step 1 (a non-object candidate) has no key, and `RUN_TERMINATION_UNEXPLAINED_INDETERMINATE_*` is published as a wildcard (lines 84-85). This reconstruction uses `cb24.RUN_TERMINATION_NOT_AN_OBJECT` and the suffixes `_RULE` / `_RUN`.
- **A-n4. Run-termination s7.3 commit inventory.** The receipt's `inventoryDigest` join re-derives `commit_inventory(runId, objects, blobs)` "as the reference commit path inventories them" (lines 242-249). Identity `#/$defs/commit-inventory` states the intent ("the exact set … the commit published for this Run"), but the published member set is fixed only by a reference implementation absent from the kit.
  - Operational, excluded from Run identity.
  - This reconstruction inventories the exported Run store.
- **A-n5. U-4b.2 nested workspace wording.** A `Cargo.toml` directory "strictly below the root of a `cargo-workspace` unit is folded into the DEEPEST such workspace". For a workspace manifest below another workspace this is self-referential: the inner workspace is itself folded, so "deepest" never selects it.
  - Cargo rejects nested workspaces, so there is no practical divergence.
  - Not measured. This reconstruction folds into the outermost unit workspace.
- **A-n6. U-4b does not restate a rust unit's `languageMode`.** `rust-cargo` vs `rust-cargo-prepared` is derivable from the mode table (native lines 165-166: prepared iff an admitted PreparedOutputSetV3), so it is recorded only as a restatement note.

## Limitations of this reconstruction (not gaps)

- Run-termination s7.5 row 2 (`COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`) and s5 stage-terminal carriers are exercised only by the published law code paths. No built Run has a `provider-unavailable` primary or a retained `budget-exhausted`/`unavailable` stage terminal (`vectors/run-termination.json#/notConstructedFromBuiltRuns`).
- `docs/coop/design-corrections/discovery-defaults.py` is named by native U-4a as a reference implementation that the text governs. Its absence is not a custody gap.
- Real OS/compiler/crypto/SQLite, provider execution as enforcement, host authentication and synthetic TCB enforcement are future qualification.

## Blocker statement (R-BLOCKER-NOT-ADJUST)

No gap blocked building a promised vector, and every accept-blocking requirement was executed under source39.
- Where a recipe was missing (s39-M1), the choice is recorded with its alternative and measured.
- No meaning was adjusted, and no author code was imported.

One MUST gap remains, so the verdict is **CHANGES_REQUIRED**, not BLOCKED.
