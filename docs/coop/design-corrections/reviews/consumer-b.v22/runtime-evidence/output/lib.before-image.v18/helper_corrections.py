"""output/helper-corrections.json -- every helper defect this origin found IN ITS OWN CODE,
with the original failure preserved, the kit selector that settled it, and the correction.

A helper bug is NOT a design gap. These rows are kept separate from newMustIssues /
newShouldIssues for exactly that reason, and every one of them was corrected from the kit
alone -- no author model, checker or expected output was read.
"""
import json
import os
import sys

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'   # V17-D8: see that row below

ROWS = [
    {'id': 'V15-D1', 'generation': 'consumer-b.v15', 'status': 'corrected',
     'where': 'lib/rebind_v15.py, lib/verify_kit.py',
     'originalFailure': ('the path-rebinding helper rewrote its own pinned constants while '
                         'rewriting every other module, so the verifier compared the new kit '
                         'against itself'),
     'kitSelector': 'n/a -- a helper self-reference defect, not a kit question',
     'correction': ('a SELF_EXCLUDE set plus split string literals; before-images of every '
                    'rewritten module are retained under lib.before-image.*')},
    {'id': 'V15-D2', 'generation': 'consumer-b.v15', 'status': 'corrected',
     'where': 'lib/run_ts.py language mode of record',
     'originalFailure': ('the TypeScript subject was labelled `ts-tsconfig` while its '
                         'tsconfig.json sets allowJs:true and admits src/legacy.js as a '
                         'program root; the independent mode law refused it with '
                         'section1.2:TS_TSCONFIG_REQUIRES_ALLOWJS_ABSENT_OR_FALSE and '
                         'section1.2:TS_TSCONFIG_JAVASCRIPT_FILES_ARE_NOT_PROGRAM_ROOTS'),
     'kitSelector': 'native-evidence.md section 1.2 closed mode table',
     'correction': 'the mode of record is js-allowjs, shared by the universe, the context '
                   'and the enumeration cells'},
    {'id': 'V15-D3', 'generation': 'consumer-b.v15', 'status': 'corrected',
     'where': 'lib/opensip_schema.py _resolve_local',
     'originalFailure': ('$ref sibling keywords were discarded, so the keyword walker reached '
                         '1 annotated digest site on TypeScriptNativeContextV2 instead of 12'),
     'kitSelector': ('relation/native annotation law: "An annotation on the OCCURRENCE, its '
                     'enclosing schema path, or an intermediate alias applies to that '
                     'occurrence"; x-opensip-digest-domains.scope.nullableAlternatives'),
     'correction': ('siblings are merged over the resolved target and oneOf/anyOf branches '
                    'are resolved before probing, so nullable non-null branches are reached')},
    {'id': 'V15-D4', 'generation': 'consumer-b.v15', 'status': 'corrected',
     'where': 'lib/run_*.py VCS observation kind',
     'originalFailure': ('four Runs declared the execution-inputs account '
                         '`inapplicable-vcs` while their snapshots admitted a VCS '
                         'observation of kind=git'),
     'kitSelector': 'execution-inputs-contract.v1.md section 5 -- the basis of '
                    '`inapplicable-vcs` is an admitted VCS observation of kind=none',
     'correction': 'those subjects are unpacked trees with vcs_kind=none'},
    {'id': 'V16-D1', 'generation': 'consumer-b.v16', 'status': 'corrected',
     'where': 'lib/opensip_schema.py walk_keywords / _resolve_local',
     'originalFailure': ("KeyError('D9Class') raised while admitting a CommandEnvelope: the "
                         'walker kept passing the ORIGINAL document root down the recursion, '
                         'so a subschema reached through a CROSS-DOCUMENT $ref '
                         '(command-envelope -> common StepTermination) could not resolve its '
                         'own LOCAL $ref. Recorded exactly as observed: '
                         '{"check": "OWNING_SCHEMA", "detail": "\'D9Class\'"} on the '
                         'pinned-purge positive, which stock Draft 2020-12 admits.'),
     'kitSelector': ('identity-and-evidence section 3 payload registry: "validation by the '
                     'row SELECTOR against that document, resolved through the pinned local '
                     'registry closure" -- resolution is per-document, so the effective base '
                     'must follow the reference'),
     'correction': ('_resolve_local2 returns the resolved node WITH its effective root and '
                    'the walker threads that root through every branch, item and property; '
                    'measured effect: the native schema now reports 76 annotated occurrences '
                    'instead of a truncated walk, and all five Runs still close, replay and '
                    'pass their controls'),
     'notADesignGap': ('the kit bytes were correct throughout; the defect was in this '
                       "origin's keyword walker")},
    {'id': 'V16-D2', 'generation': 'consumer-b.v16', 'status': 'corrected',
     'where': 'lib/opensip_build.py component-manifest description',
     'originalFailure': ('the v15 path rebind rewrote a CONTENT-BEARING label, so the '
                         'runtime directory name entered component-manifest.description and '
                         'therefore closure.manifestDigest and every Run identity: '
                         'relocating the helper would have changed selected graph '
                         'identities with no semantic change'),
     'kitSelector': ('identity-and-evidence section 3: an identity is over the admitted '
                     'record bytes; nothing authorises a runtime path to enter them'),
     'correction': ('lib/opensip_fixture.py fixes the semantic fixture metadata explicitly, '
                    'and lib/relocation_control.py proves both halves: no retained byte '
                    'contains a runtime-location string, and a rebuild under a different '
                    'output directory reproduces the selected graph identity')},
    {'id': 'V16-R1', 'generation': 'consumer-b.v16',
     'status': 'reconstruction-strengthening (NOT a helper bug and NOT a kit defect)',
     'where': 'lib/run_ts.py, lib/run_ts_full.py -- the TypeScript subject and Run',
     'originalFailure': ('not a failure. The graph-query endpoint law cannot project a '
                         'resolved TARGET endpoint without a TargetAttributionV2 sidecar, and '
                         'the Run retained none; the pagination control also had only one '
                         'projectable outgoing edge, so a page boundary never arrived.'),
     'kitSelector': ('foundation/evaluator-projection-registry.v1.json relations.imports '
                     '(endpointTarget admitted-at-rung, targetNativeIdField) + '
                     'foundation/target-attribution.schema.v2.json + '
                     'execution-inputs-contract.v1.md section 6 '
                     '("Missing token / empty companions: lawful occupancy-unknown")'),
     'correction': ('the subject gained a second first-party import and the Run retains two '
                    'TargetAttributionV2 records as part of the same synthetic trusted '
                    'provider return as its facts. The Run was reminted and reclosed, and the '
                    'closure gained the TARGET_ATTRIBUTION_* owner joins (778 passed checks, '
                    'up from 716). The earlier Run was LAWFUL -- occupancy-unknown is the '
                    'published outcome for an absent companion -- so this row is a '
                    'strengthening, not a correction of an error.')},
    {'id': 'V17-D1', 'generation': 'consumer-b.' + 'v17', 'status': 'corrected',
     'where': 'lib/phase0.py ANCESTRY table, after the v16->v17 path rebind',
     'originalFailure': ('the mechanical path rebind rewrote the ancestry ROW LABEL '
                         "'consumer-b." + "v16' to 'consumer-b." + "v17' while leaving the v16 "
                         'digests beside it, so the table asserted that the v17 manifest digest '
                         'was 6aad82e6... Caught by READING the rebound file rather than '
                         'trusting the rebind; same defect class as V16-D2. (The generation-18 '
                         'rebind then rewrote this very sentence; see V18-D6, which restores it '
                         'and writes the labels as split literals so a mechanical rewrite '
                         'cannot reach them again.)'),
     'kitSelector': 'n/a -- a helper self-reference defect, not a kit question',
     'correction': ('digest constants are written beside their own generation, the v16 row is '
                    'preserved, and the current pair is asserted against the measured '
                    'manifest (phase0 hashVerification PASS)')},
    {'id': 'V17-D2', 'generation': 'consumer-b.' + 'v17', 'status': 'corrected',
     'where': 'lib/opensip_closure.py check_policy_admission filter admissibility',
     'originalFailure': ('a filter spec in the projection registry is EITHER a string or a '
                         'PER-RUNG map; the check compared the map object to the string '
                         '"forbidden", which is never equal, so every filter forbidden AT THE '
                         'REQUESTED RUNG was admitted (for example `target` on '
                         'calls@syntactic-callee-name)'),
     'kitSelector': ('atom-evaluation-contract.v1.md section 3: "Absent field at the requested '
                     'rung => filter forbidden at admission"; evaluator-projection-registry '
                     'relations[].filters per-rung maps'),
     'correction': ('the spec is resolved AT the atom rung before comparison; new refusal '
                    'atom3:FILTER_FIELD_FORBIDDEN_AT_THE_REQUESTED_RUNG with a control')},
    {'id': 'V17-D3', 'generation': 'consumer-b.' + 'v17', 'status': 'corrected',
     'where': 'lib/opensip_closure.py (no kind law at all) + run_syntax_code_full.py and '
              'run_rust_full.py disabled probe rules',
     'originalFailure': ('the checker validated only that an atom\'s relation was registered, '
                         'that its rung was on that relation\'s ladder and that the tree shape '
                         'was legal. It never compared the atom\'s actual SUBJECT KIND against '
                         'the endpoint\'s registered kinds. Measured consequence: TWO of the '
                         'five sealed graphs carried a DISABLED rule whose atom was '
                         'kind-incompatible (relation `literal`, sourceSubjectKind `symbol`, '
                         'against subjectKind `file` in syntax-code and `package` in rust), and '
                         'the `disabled` outcome hid it from every execution-side check. Both '
                         'graphs closed, replayed REPLAY_MATCH and passed 14 controls each '
                         'while containing a malformed program.'),
     'kitSelector': ('atom-evaluation-contract.v1.md sections 1/3/4 ("Wrong `subject.kind` for '
                     'the relation/endpoint is ATOM_KIND_INCOMPATIBLE, never vacuous `none`"; '
                     '"Export is not a kind token") + '
                     'evaluator-projection-registry.v1.json kindApplicability '
                     '(endpointSource / endpointTarget, unary relations and unresolved-edge '
                     'ATOM_ENDPOINT_UNAVAILABLE, resolved-* rung gating)'),
     'correction': ('check_atom_kind_and_endpoint over EVERY atom of EVERY rule including '
                    'disabled and empty ones, applied to BOTH the Plan PolicyDocumentV2 and '
                    'the compiled RuleProgramV2 (check_rule_program_kind_and_endpoint); the '
                    'two fixtures are corrected to subjectKind `symbol`; 6 new distinguishing '
                    'controls plus a lawful endpoint=target contrast')},
    {'id': 'V17-D4', 'generation': 'consumer-b.' + 'v17', 'status': 'corrected',
     'where': 'lib/opensip_closure.py (no enumeration checker) + all four non-data Run '
              'fixtures',
     'originalFailure': ('the enumeration plan was never validated: it was read only to index '
                         'cells for the execution-inputs derivation. Measured consequence: '
                         'four of five graphs declared a clones-fact FILE extent restricted to '
                         'compiler/grammar-readable paths (dropping package.json, lockfiles, '
                         'tsconfigs, .cargo/config.toml and every manifest); rust-partial '
                         'narrowed its `inventory` cell to kinds=[file], dropping the whole '
                         'package census; syntax-code had a binding with no extents and no '
                         'symbol inventory.'),
     'kitSelector': ('enumeration-contract.v1.md sections 1/3/4/5/8 and '
                     'enumeration-plan.schema.v1.json x-opensip-kind-derivation + '
                     'x-opensip-file-membership-extent-law ("Every remaining inventoried '
                     'first-party snapshot path ... REGARDLESS of compiler-mode program-member. '
                     'Inventory is not grammar-gated.")'),
     'correction': ('check_enumeration_plan derives the file and package extents from the '
                    'retained UnitMembershipV1 + scope + parsed manifests and compares THE '
                    'WHOLE SET, derives cell kinds from the registry, checks binding '
                    'provenance/ordinals/joins and the per-state inventory laws; the four '
                    'fixtures are corrected; 8 enumeration controls each reach their intended '
                    'law')},
    {'id': 'V17-D5', 'generation': 'consumer-b.' + 'v17',
     'status': 'corrected (and withdraws the v16 advisory V16-A2)',
     'where': 'lib/opensip_closure.py execution-inputs derivation + run_syntax_code.py '
              'unavailable binding',
     'originalFailure': ('the kinds-set-equality was WEAKENED in v16 to available bindings '
                         'only, and the gap was published as advisory V16-A2 claiming the '
                         'unavailable case was NOT STATED and that no inventory exists for it. '
                         'The graph itself then carried an unavailable cell with an EMPTY '
                         'extent and NO retained inventory.'),
     'kitSelector': ('enumeration-contract section 1 (unavailable binding: "`extents` still '
                     'populated from host membership"; enumerator row: "inventories empty '
                     '`unavailable` matching that pair"), sections 3/4 (exactly one per '
                     '(cellOrdinal, programOrdinal, kind); the unavailable shape; '
                     'ENUMERATION_INVENTORY_MISSING_RECORD) and execution-inputs section 6 '
                     '("exactly one per kind, kinds set-equal to the cell"; "Unselected or '
                     '`universe=null` does not discard same-cell inventory items")'),
     'correction': ('the set-equality is unconditional again, the unavailable binding keeps '
                    'its host extents, the cell has its retained `unavailable` inventory '
                    '(rows=[], examinedPaths=[], deficiency matching the binding carrier), and '
                    'two controls distinguish a MISSING record from a retained unavailable '
                    'one')},
    {'id': 'V17-D6', 'generation': 'consumer-b.' + 'v17', 'status': 'corrected',
     'where': 'lib/phase7.py multi-step invocation + lib/envelopes.py (no join checker)',
     'originalFailure': ('the v16 invocation record was SCHEMA-VALID with ONE-based stepIds, '
                         'no result at all for its comparison step, and no derivation binding '
                         'on any analysis attempt -- and only the schema was checked'),
     'kitSelector': ('workflows-and-surfaces.md section 1 ("`StepId` is the zero-based '
                     'position"; "Each analysis/verify attempt owns exactly one derivation '
                     'DAG ... recorded in the attempt\'s `derivation` binding"; dependsOn lower '
                     'ids only; required-not-on-optional; terminal gate only for '
                     'render/export-delivery; retry eligibility; aggregate D9 ordering over '
                     'required steps only) + invocation-record ComparisonStepResult ("Never '
                     'defaults to success")'),
     'correction': ('envelopes.invocation_joins executes the normative joins separately from '
                    'schema shape, against the ACTUAL admitted runIds; the record is rebuilt '
                    'zero-based with all three step results and per-attempt derivation '
                    'bindings; 12 negative + 2 positive controls, and 10 of the 12 are '
                    'admitted by the owning schema and refused only by the joins')},
    {'id': 'V17-D7', 'generation': 'consumer-b.' + 'v17', 'status': 'corrected',
     'where': 'lib/phase6_repair.py FileEdit admission',
     'originalFailure': ('only the local image shape was checked (create has no preimage, '
                         'etc.), never the SELECTED SNAPSHOT condition, so the "valid" '
                         'descriptor asked to CREATE `src/legacy.js` -- a path the selected '
                         'evidence snapshot already contained'),
     'kitSelector': ('workflows-and-surfaces.md section 6: per-file edits carry the "preimage '
                     'digest from the snapshot inventory", with REPAIR.SOURCE_MOVED and '
                     'REPAIR.TARGET_PREIMAGE_MISMATCH as the published refusals'),
     'correction': ('the per-edit action/path/preimage agreement is derived from the evidence '
                    'Run\'s own retained source inventory and compared; the positive creates a '
                    'genuinely new path and the unsafe case takes its preimage FROM the '
                    'inventory; 4 snapshot-condition controls. The snapshot join is evaluated '
                    'before the closed-world gate so the intended law is REACHABLE rather than '
                    'masked by an unsafe-action prerequisite, and that ordering choice is '
                    'recorded at the site.')},
    {'id': 'V17-D8', 'generation': 'consumer-b.' + 'v17',
     'status': 'corrected, with an irreversible side effect reported in full',
     'where': 'lib/rebind_v17.py SELF_EXCLUDE, lib/check_siblings_untouched.py, '
              'lib/helper_corrections.py',
     'originalFailure': (
         'SELF_EXCLUDE exists so a mechanical path rebind cannot rewrite a PINNED DIGEST or a '
         'prior-generation LABEL. Two modules that WRITE OUTPUT were wrongly listed in it, so '
         'their OUT root still named consumer-b.v16 and they wrote into the tree this '
         'generation is required not to alter. Detected by this origin\'s own control: the '
         'prior-generation-untouched stage FAILED with [\'consumer-b.v16\'].'),
     'exactScopeOfTheSideEffect': (
         'measured in notes/prior-generation-writes.json: TWO files, both under '
         'consumer-b.v16/output -- helper-corrections.json and notes/siblings-untouched.json. '
         'consumer-b.v14 and consumer-b.v15: ZERO writes. No Run export, no review file, no '
         'checkpoint and no vector of any prior generation was touched.'),
     'whatCannotBeUndone': (
         'those two v16 files were OVERWRITTEN with v17-era content. This origin did not '
         'retain their prior bytes, so it cannot restore them and does not claim to. The v16 '
         'review files, requirement status, checkpoints, Run exports and vectors are '
         'unaffected, and the v16 verdict and findings stand as reported in '
         'previous-review.source29.md.'),
     'kitSelector': 'n/a -- an instruction-compliance defect of this origin, not a kit question',
     'correction': ('both modules pin their own output root explicitly, SELF_EXCLUDE is '
                    'documented as digest/label protection only and no longer covers a writer, '
                    'and the prior-generation control plus a new write census '
                    '(lib/audit_v16_writes.py) are both in the single from-scratch command so '
                    'a recurrence fails the run')},
    {'id': 'V16-A1', 'generation': 'consumer-b.v16', 'status': 'self-correction',
     'where': "this origin's own v15 SHOULD about the native retention catalogue",
     'originalFailure': ('v15 reported that the native retention catalogue was missing a '
                         '`fragment` entry. That reading was OVER-BROAD: no annotated site '
                         'of the native document uses `fragment`, so declining to declare it '
                         'there is correct, and the v16 kit declares only the member the '
                         'document actually needs (`derived`, with the recipe this origin had '
                         'independently derived).'),
     'kitSelector': 'native x-opensip-digest-law.retention',
     'correction': ('withdrawn by this origin. The kit was not treated as an oracle: the '
                    'withdrawal follows from measuring the document, which reports '
                    'retention counts of preimage-frame 31, preimage 21, owner-retained 11, '
                    'closure-tree-member 10 and derived 3, and zero fragment sites.')},
    {'id': 'V18-D1', 'generation': 'consumer-b.' + 'v18', 'status': 'corrected',
     'where': 'lib/rebind_v18.py + lib/phase0.py ANCESTRY table and its historical note',
     'originalFailure': (
         'this generation\'s path rebind repeated the V17-D1 defect in two ways: it RENAMED the '
         'previous generation\'s ancestry ROW instead of adding a new one, deleting that '
         'generation from the table, and it rewrote the true historical sentence about the '
         'earlier rebind into a false one. A mechanical text substitution cannot tell a PATH '
         'from a SENTENCE. Caught by reading the rebound files rather than trusting the rebind, '
         'and then by re-running the rebind, which re-corrupted the hand repair -- which is why '
         'the fix had to be at the source.'),
     'kitSelector': 'n/a -- a helper self-reference defect of this origin, not a kit question',
     'correction': (
         'generation-labelled CONTENT modules are in SELF_EXCLUDE; every label in the ancestry '
         'table is written as a SPLIT string literal so a future mechanical rewrite cannot reach '
         'it; the rebind asserts that each excluded module\'s own OUTPUT ROOT is still this '
         'generation (exclusion protects digests and labels, never a write destination); and '
         'the literal path census runs before any copied code'),
     'sameDefectClassAs': ['V15-D1', 'V16-D2', 'V17-D1', 'V17-D8']},
    {'id': 'V18-D2', 'generation': 'consumer-b.' + 'v18', 'status': 'corrected',
     'where': 'lib/run_syntax_code.py and lib/run_syntax_data.py UnitMembershipV1 records, plus '
              'lib/opensip_closure.py (which had no U-1..U-4 law at all)',
     'originalFailure': (
         'two retained membership graphs INVENTED a unit: each declared a `syntax-only` unit of '
         'language family `none` and pointed every row at it. For the syntax CODE subject the '
         'error ran the other way too -- that snapshot holds package.json, so U-1 DOES derive a '
         '`tsjs` unit and the record had to say so. No clause derives either shape.'),
     'kitSelector': (
         'native-evidence.schemas.v2 section 1.4: U-1 marker precedence tsconfig.json > '
         'jsconfig.json > package.json (Cargo.toml -> rust unit); U-4 "A file reached that way '
         'is `syntax-only` membership with `unitOrdinal: null` ... NOT A MEMBER OF AN INVENTED '
         'UNIT"'),
     'correction': ('both graphs re-derived (syntax-code declares the derivable tsjs js-program '
                    'unit from its package.json marker; syntax-data declares units: [] with '
                    'unitOrdinal null throughout), and the closure gained '
                    'check_u1_unit_derivation, which re-derives the unit set from the snapshot '
                    'and refuses a retained unit no clause yields')},
    {'id': 'V18-D3', 'generation': 'consumer-b.' + 'v18', 'status': 'corrected',
     'where': 'lib/run_ts_full.py default-unit program binding + lib/opensip_closure.py '
              'check_enumeration_plan (no programEntry provenance law)',
     'originalFailure': ('the DEFAULT-unit binding named a non-null `programEntry`, and nothing '
                         'checked where a programEntry may come from'),
     'kitSelector': (
         'enumeration-plan.schema.v1.json #/$defs/AvailableProgramBindingV1/properties/'
         'programEntry: "TS/JS extra program: non-null LogicalPath of the selected inventoried '
         'config (snapshot member). U-1 DEFAULT USES NULL; admission derives the actual U-1 '
         'marker/synthesized entry and compares it to retained '
         'TypeScriptConfigGraphV1.entryConfigPath"'),
     'correction': ('the default-unit binding carries programEntry null, and the closure now '
                    'derives the U-1 entry and compares it with the retained config graph '
                    '(ENUMERATION_BINDING_PROGRAM_ENTRY), with its own control')},
    {'id': 'V18-D4', 'generation': 'consumer-b.' + 'v18', 'status': 'corrected',
     'where': 'lib/run_ts_full.py, lib/run_rust_full.py, lib/run_rust_partial.py membership rows',
     'originalFailure': ('manifest and config files (package.json, package-lock.json, both '
                         'tsconfigs, Cargo.toml, Cargo.lock, .cargo/config.toml) were recorded '
                         'as members of the program unit of the OTHER family, with a non-null '
                         'unitOrdinal'),
     'kitSelector': ('native-evidence.schemas.v2 section 1.4 U-3: "A file\'s family is fixed by '
                     'EXTENSION ... It belongs to the deepest unit of ITS OWN family. Units of '
                     'another family never claim it."'),
     'correction': ('family and unitOrdinal are derived from the EXTENSION at every row, so '
                    'those files are family-less `syntax-only` / `grammar-only` rows with '
                    'unitOrdinal null, and the closure checks the row joins with a control')},
    {'id': 'V18-D5', 'generation': 'consumer-b.' + 'v18', 'status': 'corrected',
     'where': 'lib/run_syntax_code.py unavailable binding AND its retained inventory, plus '
              'lib/opensip_closure.py check_enumeration_carrier_pair (new)',
     'originalFailure': (
         'the unavailable binding and its own SubjectInventoryV1 both declared '
         '`language-tier-unsupported` with a NULL nativeCause, while that deficiency\'s registry '
         'row makes the cause REQUIRED with allowedCauses ["capability-missing"]. Host '
         'membership was present and correct, which is exactly why it cannot make a missing '
         'carrier valid.'),
     'kitSelector': ('native-evidence.schemas.v2 x-opensip-deficiency-cause-registry (per-'
                     'deficiency carrier + nativeCause verdict, nullIsNotAnEscape, '
                     'noDeficiencyNoCause, "There is no default row") + enumeration-contract '
                     'section 1 ("`nativeCause` a NativeCause member or null AS THAT '
                     'DEFICIENCY\'S CARRIER LAW REQUIRES")'),
     'correction': ('both records carry ("language-tier-unsupported", "capability-missing"); the '
                    'closure applies the registry verdict to EACH carrying record separately '
                    '(an inventory\'s pair is not validated by its binding\'s), and seven '
                    'carrier controls distinguish copied-native, the local '
                    'source-syntax-invalid member and the complete/absent case')},
    {'id': 'V18-D6', 'generation': 'consumer-b.' + 'v18', 'status': 'corrected',
     'where': 'lib/helper_corrections.py ROWS (the generation field of V17-D1..V17-D8) and '
              'the V17-D1 narrative sentence, plus the stale consumerId in main()',
     'originalFailure': (
         'the generation-17 -> generation-18 path rebind rewrote generation-labelled CONTENT in '
         'this record: all eight V17-D* rows came to read generation "consumer-b.' + 'v18", and '
         'the V17-D1 sentence -- which describes the v16->v17 rebind -- came to say that the row '
         'label was rewritten to "consumer-b.' + 'v18", contradicting its own second half. '
         'main() separately still declared consumerId "consumer-b.' + 'v16". Adding this module '
         'to SELF_EXCLUDE after V18-D1 stopped further damage but did not repair what was '
         'already written. Settled by READING the file against a disclosed input: '
         'previous-review.source31.md lists V17-D1..V17-D8 as generation-17 rows.'),
     'kitSelector': 'n/a -- a helper self-reference defect of this origin, not a kit question',
     'correction': ('the eight generation fields and the V17-D1 sentence are restored and are '
                    'now written as SPLIT string literals, the consumerId names THIS generation '
                    '(also as a split literal), and openHelperFailuresOnAClaimedPositive is '
                    'DERIVED from row status instead of being a hardcoded empty list'),
     'sameDefectClassAs': ['V15-D1', 'V16-D2', 'V17-D1', 'V18-D1']},
    {'id': 'V18-D7', 'generation': 'consumer-b.' + 'v18',
     'status': 'OPEN -- correction identified, not yet executed in this generation',
     'where': 'lib/opensip_closure.py check_execution_inputs_derivation, the '
              'all-accounts-unsupported branch of the derived-state ladder',
     'originalFailure': (
         'the helper adds a derived-state branch the published table does not contain: "every '
         'account unsupported-typed and none complete => unavailable". execution-inputs-contract '
         'section 4 row 4 says "all inventories complete, every account '
         'complete/inapplicable/UNSUPPORTED, candidate complete if owed => complete", and '
         'section 5 routes the unsupported work to requiredCellDeficiencies / the proof bridge '
         'instead. The branch would REFUSE a lawful graph rather than miss a refusal. It is '
         'dormant on the five positives (no cell has an all-unsupported account set), which is '
         'why passing self-check counts never exposed it.'),
     'kitSelector': ('foundation/execution-inputs-contract.v1.md section 4 outcome table + '
                     'section 5 ("Required unsupported / unavailable / incomplete work is '
                     'semantic indeterminate (requiredCellDeficiencies)")'),
     'correction': ('the new independent instrument lib/indep_execution_inputs.py implements the '
                    'four table rows literally and does NOT reproduce the branch; removing the '
                    'branch from the retained closure and re-running every Run is the remaining '
                    'step and is blocked on interpreter execution in this session')},
    {'id': 'V18-D8', 'generation': 'consumer-b.' + 'v18',
     'status': 'OPEN -- PREDICTED by reading clause + fixture, NOT yet measured',
     'where': 'lib/run_syntax_code.py / run_ts_full.py / run_rust_full.py / run_rust_partial.py '
              'clones-fact cell outcomes, and lib/opensip_closure.py (the clause is absent '
              'there entirely)',
     'originalFailure': (
         'the clones-fact cells bind and retain a COMPLETE file inventory over the whole file '
         'extent (itself the V17-D4 correction: "the capability does not narrow the kind\'s '
         'extent"), while the returned clones partition covers only the files that carry clone '
         'bodies. execution-inputs-contract section 5 additionally requires that "every expected '
         'source subject from this cell\'s inventory/extent of the relation\'s subject-kind must '
         'be a member of some returned partition ... Missing expected subjects -> incomplete '
         'even if the remaining Coverage is complete", and relations.clones declares '
         'sourceSubjectKind=file. Section 4 row 3 then makes the cell PARTIAL, not complete. The '
         'retained closure never implemented the expected-subject clause, so its passing counts '
         'said nothing about it.'),
     'kitSelector': ('foundation/execution-inputs-contract.v1.md section 5 supported-available '
                     'row + foundation/evaluator-projection-registry.v1.json '
                     'relations.clones.sourceSubjectKind'),
     'declaredInterpretation': (
         'I-2 in lib/indep_execution_inputs.py: the table row binds for the subjects this cell '
         'actually RETAINS, while section 5\'s closing sentence ("Global missing expected '
         'subjects still needs a reconstruct join; this unit does not invent that census") '
         'withholds only a global snapshot-wide census. The alternative reading -- that the '
         'closing sentence suspends the table row -- is recorded and not assumed.'),
     'whyWideningTheScopeIsNotTheFix': (
         'scopeCapabilityLaw (identity-schemas.v3, enforced at opensip_closure.py '
         'check_scope_capability_law) makes a scope carrying paths the selected grammar cannot '
         'read an UNSUPPORTED scope whose Coverage must carry the prescribed unknown + typed '
         'pair -- which is "mixed complete+unknown -> not complete", i.e. partial again. Both '
         'lawful shapes agree that the complete row is the defect.'),
     'correction': ('identified, not applied: the affected cells must be re-derived as partial '
                    'and every affected Run re-sealed and re-replayed, and the clause must be '
                    'ported into the retained closure with its own discriminating control. Both '
                    'need interpreter execution, which was not available in this session.')},
]


def main():
    # V18-D6: derived from row status, never a hardcoded empty list, so an open row cannot be
    # reported as a closed record.
    open_rows = [r['id'] for r in ROWS if r['status'].startswith('OPEN')]
    doc = {'consumerId': 'consumer-b.' + 'v18', 'standing': __doc__,
           'helperCorrections': ROWS,
           'openHelperFailuresOnAClaimedPositive': open_rows,
           'rule': ('an OPEN helper failure on a claimed complete positive forbids ACCEPT. '
                    'This list is DERIVED from the rows above: while it is non-empty the '
                    'verdict stays CHANGES_REQUIRED, whatever the passing check counts say.')}
    with open(OUT + '/helper-corrections.json', 'w') as f:
        json.dump(doc, f, indent=1)
    print('helper-corrections.json: %d rows, %d open %s'
          % (len(ROWS), len(open_rows), open_rows))
    for r in ROWS:
        print('  %-8s %-18s %s' % (r['id'], r['status'][:18], r['where'][:60]))


main()
