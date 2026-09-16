"""Source39 helper corrections of this origin's own ported helpers (continuing the prior numbering HC-1..HC-13, which remain history).

Each entry: the original failure and where its bytes or log are retained, the kit selector that answers it, and the correction. Helper bugs
with a precise normative answer are corrections, never design gaps. PHASE maps each correction to the checkpoint that records it.
"""
HC = {
    "HC-14": ("ref/execinputs.py: NativeCoverageAccountV1.targetUniverse carried the binding universe and the clones census owed the whole file "
              "extent. Original failure: all 26 Runs refused SCHEMA_REFUSED:execution-inputs /nativeCoverageAccounts/0/targetUniverse "
              "(logs/s39-original-closure.0.from_scratch.log; sources and stores preserved/s39-original/). Selectors: "
              "foundation/execution-inputs-contract.v1.md s5 ('targetUniverse has one canonical value: null'; body-eligible census); "
              "identity-schemas.v3.json#/x-opensip-digest-domains/bodyEligibilityLaw/census. Correction: targetUniverse null; census restricted "
              "to eligible paths under the cell languageMode's universe domain."),
    "HC-15": ("ref/closure.py + builders: stage output schemas were accepted when they were any registered payload document "
              "(cb24.STAGE_OUTPUT_SCHEMA_UNREGISTERED). HC-15b: the first corrected build refused every Run "
              "STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH because the builders still named the native bundle digest "
              "(logs/s39-hc-build.4.from_scratch.log). Selectors: identity-and-evidence.md lines 1303-1325; identity-schemas.v3.json "
              "#/$defs/stage-spec/properties/outputSchemaDigest/x-opensip-digest/registeredBy. Correction: ref/source39.stage_output_faults (five "
              "published refusals); provider closures ship opensip-interface/stage-output/<operation>.schema.json and stage specs name its digest."),
    "HC-16": ("ref/native_facts.py clones join: the level specification was only required to be retained (syntax: grammar tree membership, "
              "cb24.CLONE_LEVEL_SPEC_NOT_IN_GRAMMAR_CLOSURE); no closure carried a map. phase6 then refused four vectors "
              "BODY_NORMALIZATION_MAP_MISSING and its not-retained control reached LEVEL_VERSION_MISMATCH first "
              "(logs/s39-p456.2.phase6_vectors.log). Selectors: identity-and-evidence.md lines 1065-1089; identity-schemas.v3.json "
              "#/x-opensip-digest-domains/normalizationSpecificationLaw and #/$defs/normalization-specification-map. Correction: "
              "ref/source39.normalization_map_faults in published order; toolchain/grammar closures carry the map; the not-retained control keeps the "
              "mapped specification and drops its bytes; a another-level control was added."),
    "HC-17": ("ref/native_facts.py owed_disclosure: the source-variant law gated only closed-suffix-table dialects, ran after the syntax registry "
              "and before ownership, and named mismatches cb24.*; the TS builder returned a disclosed clones partition over package.json/tsconfig/README. "
              "Selectors: identity-schemas.v3.json#/x-opensip-digest-domains/scopeCapabilityLaw (appliesToBodyEligibility, guardOrder, refusals); "
              "native-evidence.md lines 931-945, 3454-3457, 3479-3512. Correction: ownership, then syntax capability, then body eligibility for every "
              "universe; published COVERAGE_SOURCE_VARIANT_* / COVERAGE_DIALECT_UNDISCLOSED names; default clones partitions over eligible paths only."),
    "HC-18": ("ref/membership.py + ref/enumeration.py + ref/closure.py: unit/row orders were forced cb24 choices, Cargo roots were every Cargo.toml "
              "directory including pruned ones, and closure re-derived the whole record from snapshot bytes (cb24.UNIT_MEMBERSHIP_DERIVATION), "
              "stricter than the law and blind to the security boundary inventory. Selectors: native-evidence.md U-4b lines 730-787; "
              "foundation/enumeration-plan.schema.v1.json#/x-opensip-new-internal-faults. Correction: published order, ordinals, Cargo roots, "
              "deepest-workspace folding, excluded units and row decision; ENUMERATION_MEMBERSHIP_ORDER / _ROW_DERIVATION over the retained record "
              "(runs/syntax-code~membership-reordered now refuses ENUMERATION_MEMBERSHIP_ORDER:rows)."),
    "HC-19": ("ref/membership.py discover_units emitted zero units for a syntax-only repository; builders declared explicit workspaceRoots ['.'] beside "
              "DISCOVERED provenance; closure ignored explicit roots. Selectors: native-evidence.md U-9 lines 851-877; Config2 join lines 879-903. "
              "Correction: the DEFAULTED fallback unit; zero-config discovery in builders; closure derives with the configuration's explicit roots."),
    "HC-20": ("ref/native_ctx.py bind_typescript_universe: jsAdmittedToProgram = allowJs and jsDiagnosticsEnabled = allowJs AND checkJs. "
              "Selector: native-evidence.md lines 537-540. Correction: allowJs AND len(jsRootFiles) > 0; checkJs."),
    "HC-21": ("builders/ts_runs.py + ref/closure.py: bytes the TS context read from node_modules were not snapshot rows and no closure join existed. "
              "Selectors: identity-and-evidence.md lines 548-593; security-and-lifecycle.md lines 266-279; native U-4a lines 718-726. "
              "Correction: read rows retained and joined to the layout (ref/source39.pruned_read_faults); negatives "
              "ts-pass~pruned-read-nested-node-modules and ~pruned-read-vcs-tree refuse SNAPSHOT_PRUNED_TREE_NOT_A_READ."),
    "HC-22": ("ref/closure.py did not join stage-spec parameters to the analysis-spec. Selectors: identity-and-evidence.md lines 1295-1298; "
              "identity-schemas.v3.json#/$defs/stage-spec/properties/parameters description; #/x-opensip-payload-registry/classes/parameter/"
              "selectionCardinality/notAStageSpecDuplicate. Correction: STAGE_SPEC_HIDDEN_PARAMETER."),
    "HC-23": ("ref/closure.py refused a second ScopeDocumentV1 as EVALUATOR_PARAMETER_CARDINALITY and did not guard other rows. Selectors: "
              "identity-and-evidence.md lines 718-752; #/x-opensip-payload-registry/classes/parameter/selectionCardinality. Correction: "
              "ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS for every registered row (ts-pass~scope-document-duplicate)."),
    "HC-24": ("tools/from_scratch.py labelled every refused positive a designed negative, inferring the role from an earlier replay "
              "(logs/s39-original-closure.0.from_scratch.log). Correction: the role is the Run's declared purpose; exit requires positives ADMIT and "
              "designed negatives REFUSE."),
    "HC-25": ("tools/phase9_graph_query.py used a {envelope, queryResponse} cb24 carrier and routed a project mismatch to QUERY.VIEW_UNKNOWN. "
              "Selectors: workflows-and-surfaces.md lines 1197-1239; workflows/command-inventory.v3.json query queryDispatch; "
              "query-projection-contract.v3.md s7 table (project mismatch -> QUERY.PARAMS_MALFORMED). Correction: CommandEnvelope major 3 with "
              "querySurface and queryResponse; parity read at the inventory parityPaths."),
    "HC-26": ("tools/phase8_compare.py: presence treated a disabled rule as a null pivot, had no B absence knowledge, and approximated unknown "
              "absence as pivot-reevaluation-unavailable. Selectors: workflows-and-surfaces.md s3 lines 360-411; evaluator3 comparison-result "
              "#/$defs/RuleCoverage/properties/absenceKnowledge and #/$defs/PivotPresence; workflow-projection-contract.v3.md s12 lines 201-204. "
              "Correction: one presence law on every side, RuleCoverage.absenceKnowledge at adoption, the closed five-step reason order, and the "
              "recipe termination read from detector dispositions."),
    "HC-27": ("tools/replay_all.py built the Rust designed negatives ambiguous-fact-present / partial-fact-present over rust-mixed, where they changed "
              "nothing and admitted (logs/s39-replay-all.0.replay_all.log; stores retired to preserved/s39-tool-error/). Correction: built over "
              "rust-ambiguous / rust-partial, where they refuse BODY_LANGUAGE_OWNER_AMBIGUOUS / _UNENUMERATED."),
    "HC-28": ("tools/phase9_graph_query.py stored a failed expectation's own record inside itself, making the vector file circular "
              "(logs/s39-p89.1.phase9_graph_query.log). Correction: the expectation detail is summarized."),
    "HC-29": ("tools/phase8_envelopes.py: the renderer-failed-after-commit goldens lacked the committed runId the evaluator3 StepTermination branch "
              "requires, and the required-incomplete and partial exhibits used ts-pass / ts-clones-required, which the source39 census completes "
              "(logs/s39-p89.0.phase8_envelopes.log). Correction: runId of the committed Run; exhibits over syntax-mixed-disclosed."),
    "HC-30": ("tools/final_custody.py carried the prior kit's expected manifest and parent hashes. Correction: the source39 values supplied with the "
              "continuation (charter line 3)."),
    "HC-31": ("tools/phase9_graph_query.py neighbors-evidence-limitations control expected execution deficiencies on ts-clones-required, which the "
              "source39 census now seals pass (logs/s39-rt-gq.1.phase9_graph_query.log). Correction: the control runs over syntax-mixed-disclosed."),
    "HC-32": ("tools/run_termination_vectors.py read d9-exit-contract goldens under a nonexistent key (logs/s39-rt.0.run_termination_vectors.log). "
              "Correction: #/goldenCases."),
}
PHASE = {5: ["HC-14", "HC-15", "HC-16", "HC-17", "HC-18", "HC-19", "HC-20", "HC-21", "HC-22", "HC-23", "HC-27"],
         6: ["HC-16"], 7: ["HC-18", "HC-19", "HC-32"], 8: ["HC-26", "HC-29"], 9: ["HC-24", "HC-25", "HC-28", "HC-30", "HC-31"]}


def for_phase(n):
    return [f"{k}: {HC[k]}" for k in PHASE.get(n, [])]


def all_entries():
    return [f"{k}: {v}" for k, v in HC.items()]
