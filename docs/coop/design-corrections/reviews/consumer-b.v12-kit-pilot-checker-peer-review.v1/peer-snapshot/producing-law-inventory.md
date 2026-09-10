# Producing-law inventory

Executed against both exact stores. Tamper producing assertions match the positive.

| id | document | field | status | applicable | checker |
|---|---|---|---|---|---|
| `ENUM-PARAM-IDENTITY` | enumeration-contract.v1.md | EnumerationPlanV1 identity | executed-pass | yes | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-FORBIDDEN-PARENT` | enumeration-contract.v1.md | EnumerationPlanV1.planId/analysisSpecDigest | executed-pass | yes | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-JOIN-snapshotId` | enumeration-contract.v1.md | EnumerationPlanV1.snapshotId | executed-pass | yes | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-JOIN-scopeDigest` | enumeration-contract.v1.md | EnumerationPlanV1.scopeDigest | executed-pass | yes | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-JOIN-membershipDigest` | enumeration-contract.v1.md | EnumerationPlanV1.membershipDigest | executed-pass | yes | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-CELL-ORDER` | enumeration-contract.v1.md | EnumerationPlanV1.cells order | executed-pass | yes | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-CELL-TUPLES` | enumeration-contract.v1.md | cells ↔ requestedCapabilities | executed-pass | yes | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-UNIVERSE-DOMAIN-0-0` | enumeration-contract.v1.md | universe domain | executed-pass | yes | `ProducingLaw._check_binding` |
| `ENUM-UNIVERSE-DOMAIN-1-0` | enumeration-contract.v1.md | universe domain | executed-pass | yes | `ProducingLaw._check_binding` |
| `ENUM-UNIVERSE-DOMAIN-2-0` | enumeration-contract.v1.md | universe domain | executed-pass | yes | `ProducingLaw._check_binding` |
| `ENUM-CELLS-BINDINGS` | enumeration-contract.v1.md | programBindings | executed-pass | yes | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-CANDIDATE-SOURCE-PATHS` | enumeration-contract.v1.md | programBindings[].candidateSourcePaths | notReached | no | `ProducingLaw._enum_plan_identity_and_joins` |
| `ENUM-MEM-COVER` | enumeration-contract.v1.md | UnitMembershipV1.rows | executed-pass | yes | `ProducingLaw._membership_cover_and_extents` |
| `ENUM-MEM-ERASED` | native-evidence.md §1.4 U-4 | UnitMembershipV1.erasedFiles | executed-pass | yes | `ProducingLaw._membership_cover_and_extents` |
| `ENUM-U1-REDISCOVER` | enumeration-contract.v1.md | UnitMembershipV1 via discover_units | notReached | no | `ProducingLaw._membership_cover_and_extents` |
| `ENUM-EXTENT-0-0-file` | enumeration-contract.v1.md | programBindings[].extents[kind=file].paths | executed-pass | yes | `ProducingLaw._membership_cover_and_extents` |
| `ENUM-EXTENT-1-0-file` | enumeration-contract.v1.md | programBindings[].extents[kind=file].paths | executed-pass | yes | `ProducingLaw._membership_cover_and_extents` |
| `ENUM-EXTENT-1-0-package` | enumeration-contract.v1.md | programBindings[].extents[kind=package].paths | executed-pass | yes | `ProducingLaw._membership_cover_and_extents` |
| `ENUM-EXTENT-2-0-symbol` | enumeration-contract.v1.md | programBindings[].extents[kind=symbol].paths | executed-pass | yes | `ProducingLaw._membership_cover_and_extents` |
| `ENUM-U1-UNITS` | enumeration-contract.v1.md | UnitMembershipV1.units | executed-pass | yes | `ProducingLaw._membership_cover_and_extents` |
| `ENUM-INV-CARDINALITY` | enumeration-contract.v1.md | SubjectInventoryV1 locator set | executed-pass | yes | `ProducingLaw._expected_inventories_and_totality` |
| `ENUM-FILE-ROW-hello.rs` | enumeration-contract.v1.md | InventoryRowV1 kind=file | executed-pass | yes | `ProducingLaw._check_file_row` |
| `ENUM-INV-ADMIT-d8bd5295` | enumeration-contract.v1.md | SubjectInventoryV1 | executed-pass | yes | `ProducingLaw._expected_inventories_and_totality` |
| `ENUM-FILE-ROW-hello.rs` | enumeration-contract.v1.md | InventoryRowV1 kind=file | executed-pass | yes | `ProducingLaw._check_file_row` |
| `ENUM-INV-ADMIT-28408046` | enumeration-contract.v1.md | SubjectInventoryV1 | executed-pass | yes | `ProducingLaw._expected_inventories_and_totality` |
| `ENUM-PKG-1` | enumeration-contract.v1.md | SubjectInventoryV1 kind=package | executed-pass | yes | `ProducingLaw._expected_inventories_and_totality` |
| `ENUM-INV-ADMIT-8488e4db` | enumeration-contract.v1.md | SubjectInventoryV1 | executed-pass | yes | `ProducingLaw._expected_inventories_and_totality` |
| `ENUM-SYM-2` | enumeration-contract.v1.md | SubjectInventoryV1 kind=symbol rows | executed-pass | yes | `ProducingLaw._expected_inventories_and_totality` |
| `ENUM-INV-ADMIT-7639aa21` | enumeration-contract.v1.md | SubjectInventoryV1 | executed-pass | yes | `ProducingLaw._expected_inventories_and_totality` |
| `EI-HOSTCAPTURE-SHAPE` | execution-inputs-contract.v1.md | hostCapture.custody/observation | executed-pass | yes | `ProducingLaw._stage_receipts` |
| `EI-RECEIPTS` | execution-inputs-contract.v1.md | hostCapture.stageReceipts | executed-pass | yes | `ProducingLaw._stage_receipts` |
| `EI-NO-STORE-POINTERS-FIELD` | execution-inputs-contract.v1.md | store_pointers (not a record field) | executed-pass | yes | `ProducingLaw._stage_receipts` |
| `EI-HELPER-FIXTURE` | execution-inputs-contract.v1.md |  | notReached | no | `ProducingLaw._stage_receipts` |
| `EI-SELECTED-TOTALITY` | execution-inputs-contract.v1.md | ExecutionInputsV1.selectedRefs | executed-pass | yes | `ProducingLaw._derive_selected_refs` |
| `EI-HOST-DERIVED` | execution-inputs-contract.v1.md | hostCapture.hostDerivedRefs | executed-pass | yes | `ProducingLaw._derive_selected_refs` |
| `EI-IMPORTS-NONE` | execution-inputs-contract.v1.md | selectedRefs domain=import | notReached | no | `ProducingLaw._derive_selected_refs` |
| `EI-CANDIDATE-NONE` | execution-inputs-contract.v1.md | candidateResultRefs / CandidateProducerResultV1 | notReached | no | `ProducingLaw._derive_selected_refs` |
| `EI-TARGET-ATTR-NONE` | atom-evaluation-contract.v1.md | selectedRefs domain=target-attribution | notReached | no | `ProducingLaw._derive_selected_refs` |
| `EI-INCOMING-SEARCH-NONE` | atom-evaluation-contract.v1.md | selectedRefs domain=incoming-search | notReached | no | `ProducingLaw._derive_selected_refs` |
| `EI-VCS-KIND` | execution-inputs-contract.v1.md | vcs-observation.kind → NativeCoverageAccountV1.applicability | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACC-0-clones-normalized-body-hash` | execution-inputs-contract.v1.md | NativeCoverageAccountV1 | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACC-1-file-enumerated` | execution-inputs-contract.v1.md | NativeCoverageAccountV1 | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACC-1-package-manifest-declared` | execution-inputs-contract.v1.md | NativeCoverageAccountV1 | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACC-1-vcs-change-vcs-reported` | execution-inputs-contract.v1.md | NativeCoverageAccountV1 | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACC-2-declares-syntactic` | execution-inputs-contract.v1.md | NativeCoverageAccountV1 | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACC-2-literal-syntactic` | execution-inputs-contract.v1.md | NativeCoverageAccountV1 | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACC-2-control-flow-syntactic` | execution-inputs-contract.v1.md | NativeCoverageAccountV1 | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACCOUNTS-EQUAL` | execution-inputs-contract.v1.md | ExecutionInputsV1.nativeCoverageAccounts | executed-pass | yes | `ProducingLaw._derive_native_accounts` |
| `EI-ACC-UNSUPPORTED-TYPED` | execution-inputs-contract.v1.md | applicability=unsupported-typed | notReached | no | `ProducingLaw._derive_native_accounts` |
| `EI-OUTCOME-0-0` | execution-inputs-contract.v1.md | CellProgramOutcomeV1.state and joined fields | executed-pass | yes | `ProducingLaw._derive_cell_outcomes` |
| `EI-OUTCOME-1-0` | execution-inputs-contract.v1.md | CellProgramOutcomeV1.state and joined fields | executed-pass | yes | `ProducingLaw._derive_cell_outcomes` |
| `EI-OUTCOME-2-0` | execution-inputs-contract.v1.md | CellProgramOutcomeV1.state and joined fields | executed-pass | yes | `ProducingLaw._derive_cell_outcomes` |
| `EI-OUTCOMES-ALL-COMPLETE` | execution-inputs-contract.v1.md | cellOutcomes[].state | executed-pass | yes | `ProducingLaw._derive_cell_outcomes` |
| `EI-REQUIRED-CELL-UNSATISFIED` | execution-inputs-contract.v1.md | derivedOutcomes / requiredCellDeficiencies | notReached | no | `ProducingLaw._derive_cell_outcomes` |
| `EI-DIGEST` | execution-inputs-contract.v1.md | proof.executionInputsDigest | executed-pass | yes | `ProducingLaw._evaluation_input_refs` |
| `COMP-EVAL-INPUT-REFS` | evaluator-composition-contract.v3.md | proof.evaluationInputRefs | executed-pass | yes | `ProducingLaw._evaluation_input_refs` |
| `EI-LOCATORS` | execution-inputs-contract.v1.md | planId/executionPlanId/evaluatorClosure/analysisSpecDigest/enumerationPlanDigest | executed-pass | yes | `ProducingLaw._evaluation_input_refs` |
| `COMP-POLICY-ONE-RULE` | evaluator-composition-contract.v3.md | PolicyDocumentV2.rules / subjectEnumeration.universe | executed-pass | yes | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-COMMITTED` | atom-evaluation-contract.v1.md | Atom endpoint/relation/minResolution/op/filters | executed-pass | yes | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-TARGET-ATTRIBUTION` | atom-evaluation-contract.v1.md | TargetAttributionV1 | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-INCOMING` | atom-evaluation-contract.v1.md | IncomingSearchV1 / endpoint=target | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-ALL-COVERED` | atom-evaluation-contract.v1.md | Atom.op=all-covered | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-NONE-TRUE-SUFFICIENCY` | atom-evaluation-contract.v1.md | sufficiency_v2 on none=true | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-IMPORT` | atom-evaluation-contract.v1.md | imported-atom / Plan importIds | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-COUNT-AT-MOST` | atom-evaluation-contract.v1.md | Atom.op=count-at-most | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-EXPORT-KIND` | atom-evaluation-contract.v1.md | subjectEnumeration.subjectKind=export | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `COMP-BASELINE` | evaluator-composition-contract.v3.md | baseline/comparison | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `COMP-FINDING-EMISSION` | evaluator-composition-contract.v3.md | finding3 | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `COMP-WAIVER-EMPTY` | evaluator-composition-contract.v3.md | WaiverSetV1 / proof.waivedFindingIds | executed-pass | yes | `ProducingLaw._atom_and_composition_branches` |
| `COMP-EMISSION` | evaluator-composition-contract.v3.md | EvaluatorEmissionPlanV1 | executed-pass | yes | `ProducingLaw._atom_and_composition_branches` |
| `COMP-SUBJECT-MINT-LAW` | evaluator-composition-contract.v3.md | evaluation-subject / subject3 | executed-pass | yes | `ProducingLaw._atom_and_composition_branches / Replay._enumerate_rule` |
| `COMP-DISABLED-RULE` | evaluator-composition-contract.v3.md | ruleResults[].outcome=disabled | notReached | no | `ProducingLaw._atom_and_composition_branches` |
| `COMP-BUDGET-EXHAUSTED-OUTPUT` | evaluator-composition-contract.v3.md | EVALUATION.WORK_BUDGET_EXHAUSTED | notReached | no | `Replay._evaluate budget preflight` |
| `EI-NOT-RUN` | execution-inputs-contract.v1.md | ExecutionInputsV1 vs run3 | executed-pass | yes | `ProducingLaw._atom_and_composition_branches` |
| `ATOM-KLEENE-NONE-FALSE` | atom-evaluation-contract.v1.md | predicateProofs[].value / PredicateWitnessV3.matchingFactIds | executed-pass | yes | `Replay._eval_atom / Replay._atom_proof` |
| `ATOM-WITNESS-FIELDS` | atom-evaluation-contract.v1.md | PredicateWitnessV3 / predicateProofs[].inputRefs,scopeIds,witnessDigest | executed-pass | yes | `Replay._atom_proof` |
| `COMP-RULE-OUTCOME-PASS` | evaluator-composition-contract.v3.md | ruleResults[].outcome / proof.verdict / executionDeficiencies | executed-pass | yes | `Replay._evaluate` |
| `COMP-ENUMERATION-COMPLETE` | evaluator-composition-contract.v3.md | ruleResults[].enumeration | executed-pass | yes | `Replay._enumerate_rule after ProducingLaw expected inventories` |
| `COMP-PROOF-FIELDS` | evaluator-composition-contract.v3.md | ProofBundleV3 derived fields | executed-pass | yes | `Replay._evaluate / Replay.run comparison` |
| `COMP-COMPLETE-REPLAY-CRITERION` | evaluator-composition-contract.v3.md | proof-bundle C + enclosing H | executed-pass | yes | `Replay.run after ProducingLaw.execute` |

Each row's paragraph, assertion, inputOperands, and executedResult are in `producing-law-inventory.json` `assertionsByGraph`.
