# source41 kit — law reading log and helper checks it implies (working record)

**Custody**
- Kit: `consumer-input-manifest.json` SHA-256 `31369cc8…`, parent `eb7a4c48…`, 104 members, all verified.
- Changed against my own source39 custody rows (`preserved/source39-v3/vectors/phase0-custody.json`): exactly 5 files. None was added or removed.
  - `docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md`
  - `docs/coop/design-corrections/foundation/run-termination-contract.v1.md`
  - `docs/coop/design-corrections/workflows/schemas/evaluator3/policy-test.schema.json`
  - `docs/v2/contracts/product-v1/native-evidence.md`
  - `docs/v2/contracts/product-v1/workflows-and-surfaces.md`

The source39 kit bytes themselves were not read, so a change is identified by reading the current text against the laws my
helpers implement and against my own source39 citations. It is never assumed.

## Read in full so far

`charter.md`, `requirements.json`, `execution-inputs-contract.v1.md`, `run-termination-contract.v1.md`,
`policy-test.schema.json`, `native-evidence.md` 1–1000, `workflows-and-surfaces.md` 1–850.

## Laws to check against the ported helpers (each becomes an execution check, not an assumption)

1. **native U-4b.2 (lines 755-766): tsjs `unitKind` is now assigned.**
   - The rule: `ts-program` exactly when the mode is `ts-tsconfig`; `js-program` for `js-allowjs` and `js-synthesized`. "The kind follows the mode, never the marker file name."
   - U-4b.5 (lines 796-799) enforces it. A tsjs unit whose `unitKind` is not the projection of its mode, or a `ts-program`/`js-program` kind on a unit of another family, refuses `ENUMERATION_MEMBERSHIP_ORDER`.
   - This is the mapping whose absence was my source39 MUST s39-M1. Check: does `ref/membership.py` emit the projection, and does enumeration admission enforce it? Re-execute the s39-M1 vector: the `ts-program` spelling of a `js-allowjs` unit must now refuse.
2. **native U-4b.2 (lines 744-754): nested Cargo workspaces are decided shallowest first.**
   - A nested workspace manifest below a `cargo-workspace` unit is a member, receives no members, and every `Cargo.toml` directory below it folds into the same enclosing unit.
   - This addresses source39 advisory A-n5. Check the folding in `membership.py`.
3. **native §1.2 (lines 516-560): effective `allowJs`/`checkJs` derivation over the retained config graph.**
   - A `jsconfig` node supplies `allowJs=true` unless the node writes it.
   - The node's own options beat its bases; later `extends` beat earlier ones.
   - After inheritance, an `allowJs` value wins, including `false`; otherwise `allowJs` follows the effective `checkJs`, default `false`.
   - The derivation introduces no compiler-option diagnostic refusal (TS 5052).
   - `jsAdmittedToProgram = allowJs AND len(jsRootFiles) > 0`; `jsDiagnosticsEnabled = checkJs`. A mismatch refuses `native.universe-context-field-mismatch:<field>`.
   - Check `native_ctx.py` and the phase-6 config vectors.
4. **native U-0 (lines 626-651): internal root representation.**
   - `rootPath` is `""` or a canonical relative directory; a member root is non-empty canonical.
   - `.` is the external sentinel only.
   - Violations refuse before membership: `NATIVE_UNIT_ROOT_REPRESENTATION`, or `ENUMERATION_MEMBERSHIP_UNIT_ROOT` via enumeration.
   - Check the helpers.
5. **native U-8 (lines 805-852):** the boundary inventory is a superset, tested on `(path, reason)` only; marker counts are provenance. Check the discovery vectors.
6. **execution-inputs §3 View attribution (line 53).** A candidate view V is attributed to a row iff:
   - `V.producerClosure` = P;
   - one and the same named scope S has `S.sourceUniverse` = U **and** `S.relation` is in the matrix capability relations (candidate-only: U alone);
   - a planId mismatch refuses `EXECUTION_INPUTS_PLAN_JOIN`;
   - every scope named by an attributed view must have `sourceUniverse` = U, else `EXECUTION_INPUTS_COVERAGE_DERIVE`.

   Check `execinputs.py`.
7. **execution-inputs §4: cross-source order for a cell row.**
   - Order: (1) enumerator/binding carrier, (2) non-complete inventories in `inventoryDigests` order, (3) candidate, (4) accounts in matrix `relations` authored order.
   - The carrier is the first source actually carrying a typed pair, else `(null, null)`.
   - The candidate carrier is the envelope's own pair, else the binding's declared pair, else `(null, null)`; it is never manufactured.
   - Check the derivation in `execinputs.py`.
8. **execution-inputs §5.**
   - Applicability is first-match in the published order: `inapplicable-vcs`, `unsupported-typed`, `unavailable-unselected`, `unavailable-null-universe`, `supported-available`.
   - `sourceUniverse` equals the binding U for every applicability (an external join); `targetUniverse` is null.
   - Missing-work carrier is `(null, null)`, not `provider-unavailable`.
   - A selected-U `UNSUPPORTED-TYPED` cell: the account names no Coverage, and `derivedAccounts` carry `accountState=unsupported` with the matrix pair.
   - Check `execinputs.py`.
9. **run-termination §7.3: derivation-binding joins** (attempt `planId`, `executionPlanId`, `stageCount`, stage progress) with their refusal keys. Also the §7.5 allowlist order, §7.4 authority and the §6 candidate order. Check `run_termination.py` and its vectors.
10. **policy-test.schema.json.**
    - `x-opensip-admission-precedence` has 5 steps.
    - `x-opensip-fixture-representation` covers subject, factUniverse, endpoint, fields/fieldsLaw, imported selectors and law, nativeLaw, ruleLaw, expectationLaw and resultLimit.
    - Check whether any vector of mine exercises policy test; the scope item is under workflows §5 "Authoring test".
11. **workflows §5 Authoring test (lines 631-673):** the precedence and fixture law restate the schema. Is there an original requirement that exercises policy test? Check vectors.

## Reading completed

`native-evidence.md` 1–3975 and `workflows-and-surfaces.md` 1–1699 are now fully read.

## Laws in native 2000–3975 my helpers already implement (re-execution checks, not new deltas)

12. **§4.3 RC-0 / RC-1 / RC-2 / RC-6.**
    - RC-0 is the relation-specific registered pair, checked first.
    - RC-1 covers the five resolved pairs and the twelve not-applicable pairs, including `unresolved-edge@observed`.
    - RC-6 says `coverage=complete` implies `examinedExhaustive=true` (an implication, not an equality) at both boundaries.
    - Check that `ref/closure.py` coverage_bijection still runs at closure.
13. **§10 deficiency/cause carrier table and per-row relation scoping** (derivation-policy-unmet is `types` only). The dialect ownership pair derivation order and the source-variant scope law (`COVERAGE_SOURCE_VARIANT_*`) also apply. My source39 Runs (rust-mixed, syntax-mixed, cmp-code-*) exercised these, so re-execute.
14. **§11 SourceUnitOwnershipV1.** `unitId = H(native.compilation-unit.v1, UnitIdentityV1)` is re-derived (HC-38). Selection order: no ownership, partial, equal path, not-compiled, not-selected, agreeing, ambiguous.
15. **§9.6 occupancy companion / DispatchBindingV1** timing and producer mapping (the syntax-only and clone rows omit the token).
16. **§14.** The bounded selection arrays and pre-Plan order are cardinality first, then schema, then vocabulary. Prospective-Plan overflow order is `semanticClosures`, `nativeContextDigests`, `importIds`.

## Outcomes of each check (what was measured and what changed)

The unchanged ported helpers ran first against this kit (logs `s41-original.*`, `s41-original-mut.*`, `s41-original-disc.*`; state preserved at `preserved/s41-original-state/`, re-executable at `preserved/pre-s41/`). Corrections are recorded in `tools/hc_source41.py`.

1. **U-4b.2/U-4b.5 tsjs unitKind: helper defect, corrected (HC-39a).**
   - The unchanged helper emitted the projection but did not enforce it. The s39-M1 alternative spelling (a `js-allowjs` unit spelled `ts-program`) passed every check (`logs/s41-original-disc.0`).
   - It now refuses `ENUMERATION_MEMBERSHIP_ORDER:unitKind:0` (`vectors/discovery-membership.json#u4b-tsjs-unit-kind-projection`). A `ts-program` kind on a rust unit refuses `…:unitKind-family:0`.
   - Run closure refuses both: `runs/ts-pass~unit-kind-not-mode-projection`, `runs/syntax-code~unit-kind-other-family`.
   - The kit now determines the membershipDigest that source39 left open.
2. **Nested Cargo workspaces: already conforming, now measured.** `vectors/discovery-membership.json#u4b-nested-cargo-workspace` gives the same units under the unchanged helper (`originalHelperUnits`). Source39 advisory A-n5 is answered by the kit text.
3. **§1.2 effective allowJs for mode selection: helper defect, corrected (HC-39b).** The unchanged helper disagreed on three of ten cases in `#s12-effective-allowjs-mode-selection`:
   - a `tsconfig.json` with `checkJs:true`;
   - a `jsconfig.json` writing `allowJs:false`;
   - a `tsconfig.json` extending a base named `jsconfig.json`.

   Context and universe flags were already `allowJs AND len(jsRootFiles)>0` / `checkJs` in closure (HC-20). The phase-6 vector spelling was corrected with no effect on results (HC-40).
4. **U-0 internal root representation: missing, added (HC-39c).**
   - The host decision is `NATIVE_UNIT_ROOT_REPRESENTATION`, and enumeration and closure use `ENUMERATION_MEMBERSHIP_UNIT_ROOT`. At closure the decision runs before schema admission and before the pruned-read Cargo-root join.
   - The helper's split-on-slash predicate agrees with the published pattern on 19 probe values (`#u0-root-grammar-agreement`).
   - The unchanged helper reported a `.` root as `ENUMERATION_MEMBERSHIP_ROW_DERIVATION` on another path, and reported a malformed member root not at all (`#u0-*`).
   - Run-closure control: `runs/syntax-code~unit-root-external-sentinel`.
5. **U-8 boundary inventory superset.**
   - Not constructed. The `(path, reason)` subset join is between security's admitted inventory and the host's marker inventory, before a Plan exists.
   - The Plan does not retain that inventory, and closure judges an `outside-project-boundary` row on family and null ordinal only (U-4b.5).
   - The discovery vectors supply boundaries directly (`#u8-boundary`). No original requirement owns the security instrument, so this is not reported as a design gap.
6. **Execution-inputs §3 view attribution: helper defect, corrected (HC-42), including the builders' host capture.**
   - The corrected admission refused the unchanged builder capture `EXECUTION_INPUTS_VIEW_TOTALITY:1:0` (`logs/s41-hc42-probe.0`).
   - My first correction broke the direct `derive_outcome` callers (`logs/s41-post-p4to9.0/.5`). My first omitted-view control was ineffective (HC-45, `logs/s41-post-mut.0` line 42).
   - The final control `runs/syntax-code~row-view-omitted` must refuse `EXECUTION_INPUTS_VIEW_TOTALITY`; checkpoint 9 gates on it.
7. **Execution-inputs §4 cross-source order: conforming by reading and measured.**
   - The source order is binding, inventories in `inventoryDigests` order, candidate, then accounts in matrix `relations` order with partitions in canonical H order. The carrier is the first source actually carrying a pair.
   - The candidate carrier is never manufactured.
   - Measured: `vectors/phase4-tables.json` outcome vectors `inventory-budget-carrier-kept`, `missing-work-null-carrier`, `candidate-optional-absent`, `two-carriers-first-in-h-order`.
8. **Execution-inputs §5 applicability, sourceUniverse join and unsupported-typed accounts: conforming and measured.** Vectors `unselected-optional`, `null-universe-required`, `unsupported-typed-outranks-unselected`, `unsupported-typed-available-required`, `vcs-none-inapplicable`.
9. **Run-termination §7.3 derivation-binding joins: present in the helper in the published order and measured.**
   - `vectors/run-termination.json` covers all four refusals: plan, execution plan, stage count, stage progress.
   - The §6 step 1 key is now published, so the helper's own `cb24.` name was replaced (HC-41).
   - The §6 step 2 text now places `errorCode`/`faultCause`/`signal` at step 3 (answers A-n2). §7.3 states the owning schema's order for `commit-inventory` (`canonical-set`; answers A-n4).
10. **policy-test.schema.json (PolicyTestSuiteV2).** No original requirement constructs a policy authoring test suite and no helper of mine builds one. The changed schema was read and is not exercised; this is stated rather than invented.
11. **workflows §5 Authoring test.** Same standing as item 10.
12. **§4.3 RC-0/RC-1/RC-2/RC-6:** re-exercised by `vectors/phase4-tables.json` (RC vectors) and by closure over every Run.
13. **§10 carriers, §11 dialect ownership pairs and source-variant scope law:** re-exercised by the rust-partial/ambiguous, syntax-mixed and syntax-data Runs and their controls.
14. **§11 SourceUnitOwnershipV1:** re-exercised; `rust-mixed~unit-id-not-derived` refuses.
15. **§9.6 occupancy companion:** the syntax-only and clone rows omit the token; no Run of mine negotiates `target-attribution-v2`.
16. **§14 bounded selections:** `vectors/multi-unit-missing-caps.json` (phase 7).
