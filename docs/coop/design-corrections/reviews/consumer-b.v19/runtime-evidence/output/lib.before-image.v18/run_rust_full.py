"""Completes the Rust Run and records its measured exhibits."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_build as B
import opensip_eval as E
import opensip_compose as CO
import opensip_closure as CL
import run_rust as RR
import run_ts_full as TSF

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'
BASE = 'run_rust'


def policy_document():
    rules = [
        {'ruleId': 'rule.a-no-clone-in-crates',
         'ruleProgramRef': {'contributionId': 'contrib.rust-hygiene',
                            'ruleStableId': 'rust-hygiene.no-clone-in-crates',
                            'semanticsMajor': 2,
                            'programDigest': K.raw_sha256(b'rust.no-clone.v2')},
         'enabled': True, 'severity': 'error', 'gate': True,
         'subjectEnumeration': {'universe': 'rust', 'subjectKind': 'file',
                                'include': ['crates/**/*.rs']},
         'emitWhen': {'op': 'none', 'relation': 'clones',
                      'minResolution': 'normalized-body-hash', 'filters': []},
         'evidenceUse': [], 'messageCode': 'clones.duplicate-body'},
        {'ruleId': 'rule.b-declares-present',
         'ruleProgramRef': {'contributionId': 'contrib.rust-hygiene',
                            'ruleStableId': 'rust-hygiene.declares-present',
                            'semanticsMajor': 1,
                            'programDigest': K.raw_sha256(b'rust.declares.v1')},
         'enabled': True, 'severity': 'warning', 'gate': False,
         'subjectEnumeration': {'universe': 'rust', 'subjectKind': 'symbol'},
         'emitWhen': {'op': 'exists', 'relation': 'declares',
                      'minResolution': 'syntactic', 'filters': []},
         'evidenceUse': [], 'messageCode': 'declares.present'},
        {'ruleId': 'rule.c-at-most-one-body',
         'ruleProgramRef': {'contributionId': 'contrib.rust-hygiene',
                            'ruleStableId': 'rust-hygiene.at-most-one-body',
                            'semanticsMajor': 1,
                            'programDigest': K.raw_sha256(b'rust.at-most-one-body.v1')},
         'enabled': True, 'severity': 'note', 'gate': False,
         'subjectEnumeration': {'universe': 'rust', 'subjectKind': 'file',
                                'include': ['crates/**/*.rs']},
         'emitWhen': {'op': 'count-at-most', 'n': 1, 'relation': 'clones',
                      'minResolution': 'normalized-body-hash', 'filters': []},
         'evidenceUse': [], 'messageCode': 'clones.body-count'},
        {'ruleId': 'rule.d-disabled-probe',
         'ruleProgramRef': {'contributionId': 'contrib.rust-hygiene',
                            'ruleStableId': 'rust-hygiene.disabled-probe',
                            'semanticsMajor': 1,
                            'programDigest': K.raw_sha256(b'rust.disabled.v1')},
         'enabled': False, 'severity': 'note', 'gate': True,
         # CORRECTED (V17-D3): `literal` registers sourceSubjectKind `symbol`; the earlier
         # `package` here was ATOM_KIND_INCOMPATIBLE and was hidden by the disabled outcome.
         'subjectEnumeration': {'universe': 'rust', 'subjectKind': 'symbol'},
         'emitWhen': {'op': 'exists', 'relation': 'literal',
                      'minResolution': 'syntactic', 'filters': []},
         'evidenceUse': [], 'messageCode': 'literal.present'},
    ]
    rules.sort(key=lambda r: r['ruleId'].encode())
    return {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2,
            'gateSeverityAtLeast': 'warning', 'rules': rules}


def complete(g):
    b, st, sh = g['b'], g['st'], g['sh']
    cl, snapshot_id = g['closures'], g['snapshot_id']
    uni_a, uni_b, ctx_hex = g['uni_a'], g['uni_b'], g['ctx_hex']

    policy = policy_document()
    policy_dig = b.record(B.POLICY_V2_DOC, '#/$defs/PolicyDocumentV2', policy, 'policy')
    waivers = {'schemaFamily': 'opensip.product.waivers', 'schemaMajor': 1, 'waivers': []}
    waiver_dig = b.record(B.POLICY_V1_DOC, '#/$defs/WaiverSetV1', waivers, 'waivers')
    rule_program = CO.build_rule_program(policy)
    b.record(B.POLICY_V2_DOC, '#/$defs/RuleProgramV2', rule_program, 'rule-program')
    emit = {'schemaVersion': 1, 'policyDigest': K.rec_digest(policy),
            'rules': sorted([{'ruleId': r['ruleId'],
                              'contributionId': r['ruleProgramRef']['contributionId'],
                              'ruleStableId': r['ruleProgramRef']['ruleStableId'],
                              'semanticsMajor': r['ruleProgramRef']['semanticsMajor'],
                              'detectorClosure': cl['detector'],
                              'stabilityClass': 'path-stable',
                              'emissionProfile': 'declarative-subject-v1'}
                             for r in policy['rules']],
                            key=lambda r: r['ruleId'].encode())}
    emit_dig = b.record(B.EMIT_PLAN_DOC, '#', emit, 'emission-plan')

    all_paths = sorted(g['files'], key=lambda s: s.encode())
    RS = sorted([p for p in all_paths if p.endswith('.rs')], key=lambda s: s.encode())
    membership = {
        'schemaVersion': 1,
        'units': [{'unitOrdinal': 0, 'rootPath': '', 'languageFamily': 'rust',
                   'languageMode': 'rust-cargo', 'unitKind': 'cargo-workspace',
                   'markerPath': 'Cargo.toml',
                   'markerSha256': K.raw_sha256(g['files']['Cargo.toml']),
                   'recognizerId': 'opensip-cargo-recognizer', 'recognizerVersion': 3,
                   'provenance': 'DISCOVERED',
                   'memberPackageRoots': sorted(['crates/app#1', 'crates/core-lib'],
                                                key=lambda s: s.encode())}],
        # CORRECTED (V18-D4): U-3 fixes the family by EXTENSION, so Cargo.toml, Cargo.lock and
        # .cargo/config.toml carry NO family and no unitOrdinal -- "Units of another family
        # never claim it."
        'rows': [{'path': p,
                  'languageFamily': 'rust' if p.endswith('.rs') else 'none',
                  'unitOrdinal': 0 if p.endswith('.rs') else None,
                  'membership': ('program-member' if p.endswith('.rs') else 'syntax-only'),
                  'reason': ('deepest-unit-in-language' if p.endswith('.rs')
                             else 'grammar-only')} for p in all_paths],
        'unsupportedFiles': [], 'outsideBoundaryFiles': [], 'erasedFiles': [],
    }
    b.admit(B.NATIVE_DOC, '#/$defs/UnitMembershipV1', membership, 'unit-membership')
    membership_dig = st.put_record(membership, label='unit-membership')

    def binding(extents, universe, ordinal=0):
        return {'ordinal': ordinal,
                'provenance': 'default-unit' if ordinal == 0 else 'explicit-plan-selection',
                'enumerator': {'status': 'selected', 'closureId': cl['provider']},
                'nativeContextDigest': ctx_hex, 'universe': universe,
                'programEntry': None,
                'extents': sorted([{'kind': k, 'paths': sorted(v, key=lambda s: s.encode())}
                                   for k, v in extents.items()],
                                  key=lambda e: e['kind'].encode())}

    cells = [
        # two program bindings for clones-fact: one per explicitly selected target set.
        # "one context never implies one universe" -- multiple bindings per cell are allowed.
        # CORRECTED (V17-D4): the FILE kind extent is first-party scoped snapshot MEMBERSHIP
        # and is therefore program-INDEPENDENT -- it is derived from (cell workspace, scope,
        # membership), not from the selected target set. The two bindings still differ where
        # the kit says they may: the selected UNIVERSE. The earlier per-binding `.rs` subsets
        # were compiler source-root sets, which the extent law does not admit here.
        {'capabilityId': 'clones-fact', 'languageMode': 'rust-cargo', 'workspaceRoot': '.',
         'required': True, 'kinds': ['file'],
         'programBindings': [binding({'file': all_paths}, uni_a, 0),
                             binding({'file': all_paths}, uni_b, 1)]},
        {'capabilityId': 'inventory', 'languageMode': 'rust-cargo', 'workspaceRoot': '.',
         'required': True, 'kinds': sorted(['file', 'package'], key=lambda s: K.C(s)),
         'programBindings': [binding({'file': all_paths,
                                      'package': [g['hash_dir'] + '/Cargo.toml',
                                                  'crates/core-lib/Cargo.toml']}, uni_a)]},
        {'capabilityId': 'syntax', 'languageMode': 'rust-cargo', 'workspaceRoot': '.',
         'required': True, 'kinds': ['symbol'],
         'programBindings': [binding({'symbol': RS}, uni_a)]},
    ]
    cells.sort(key=lambda c: (c['capabilityId'].encode(), c['languageMode'].encode(),
                              c['workspaceRoot'].encode()))
    enum_plan = {'schemaVersion': 1, 'snapshotId': snapshot_id,
                 'scopeDigest': sh['scopeDigest'], 'membershipDigest': membership_dig,
                 'cells': cells}
    enum_plan_dig = b.record(B.ENUM_PLAN_DOC, '#', enum_plan, 'enumeration-plan')
    cell_ord = {c['capabilityId']: i for i, c in enumerate(cells)}

    reqcaps = sorted([{'capabilityId': c['capabilityId'], 'languageMode': c['languageMode'],
                       'workspaceRoot': c['workspaceRoot'], 'required': c['required']}
                      for c in cells], key=lambda r: K.C(r))
    params = sorted([
        {'schemaDigest': B.doc_sha(B.ENUM_PLAN_DOC), 'payloadDigest': enum_plan_dig},
        {'schemaDigest': B.doc_sha(B.EMIT_PLAN_DOC), 'payloadDigest': emit_dig},
    ], key=lambda r: K.C(r))
    spec = {'schemaVersion': 2, 'requestedCapabilities': reqcaps,
            'policyPackIds': ['pack.rust-hygiene'], 'parameters': params}
    spec_dig = b.record(B.IDENTITY_DOC, '#/$defs/analysis-spec', spec, 'analysis-spec')
    grant = {'schemaVersion': 2, 'projectId': g['snapshot']['projectId'],
             'principals': K.cset([{'kind': 'first-party', 'closureId': cl['provider'],
                                    'ownerSourceDigest': None},
                                   {'kind': 'first-party', 'closureId': cl['evaluator'],
                                    'ownerSourceDigest': None}]),
             'analysisOperations': sorted(['read-source', 'native-analysis'],
                                          key=lambda s: K.C(s)),
             'scopeDigest': sh['scopeDigest']}
    grant_dig = b.record(B.IDENTITY_DOC, '#/$defs/semantic-grant', grant, 'semantic-grant')
    plan = {'schemaVersion': 2, 'snapshotId': snapshot_id,
            'capabilityManifestId': g['capres']['capabilityManifestId'],
            'semanticClosures': K.cset_strings([cl['provider'], cl['evaluator'],
                                                cl['detector']]),
            'analysisSpecDigest': spec_dig, 'resolvedConfigDigest': sh['configDigest'],
            'nativeContextDigests': [ctx_hex], 'importIds': [],
            'policyDigest': policy_dig, 'waiverDigest': waiver_dig,
            'scopeDigest': sh['scopeDigest'],
            'budget': dict(g['config']['analysis']['budget']),
            'semanticGrantDigest': grant_dig,
            'capabilityManifestBytesDigest': g['capres']['committedBytesSha256']}
    plan_id = b.framed('plan', B.IDENTITY_DOC, '#/$defs/plan', plan, 'plan')

    file_rows = sorted([{'nativeSubjectId': p, 'kind': 'file', 'path': p,
                         'qualifiedName': p,
                         'subjectLanguage': ('rust' if p.endswith('.rs')
                                             else 'toml' if p.endswith('.toml')
                                             else 'unspecified'),
                         'signatureTokens': [], 'projections': []} for p in all_paths],
                       key=lambda r: r['nativeSubjectId'].encode())
    rs_rows = sorted([r for r in file_rows if r['path'].endswith('.rs')],
                     key=lambda r: r['nativeSubjectId'].encode())
    lib_rows = [r for r in file_rows if r['path'] == g['libp']]
    pkg_rows = sorted([
        {'nativeSubjectId': 'app1', 'kind': 'package',
         'path': g['hash_dir'] + '/Cargo.toml', 'qualifiedName': 'app1',
         'subjectLanguage': 'toml', 'signatureTokens': [], 'projections': []},
        {'nativeSubjectId': 'core-lib', 'kind': 'package',
         'path': 'crates/core-lib/Cargo.toml', 'qualifiedName': 'core-lib',
         'subjectLanguage': 'toml', 'signatureTokens': [], 'projections': []}],
        key=lambda r: (r['nativeSubjectId'].encode(), r['path'].encode()))
    sym_rows = sorted([
        {'nativeSubjectId': sid, 'kind': 'symbol', 'path': path, 'qualifiedName': qn,
         'subjectLanguage': 'rust', 'exported': 'exported',
         'signatureTokens': ['rust', 'fn', qn, '(', ')'],
         'projections': [{'closureId': cl['detector'],
                          'signatureTokens': ['rust', 'fn', qn, '(', ')']}]}
        for sid, (path, qn) in g['syms'].items()],
        key=lambda r: r['nativeSubjectId'].encode())

    inventories = []
    for cap_id, kind, rows, examined, prog in (
            ('inventory', 'file', file_rows, all_paths, 0),
            ('inventory', 'package', pkg_rows,
             [g['hash_dir'] + '/Cargo.toml', 'crates/core-lib/Cargo.toml'], 0),
            ('syntax', 'symbol', sym_rows, RS, 0),
            # both clones-fact bindings owe the WHOLE derived file extent (section 4 file
            # totality); the per-program difference is the universe, not the file census
            ('clones-fact', 'file', file_rows, all_paths, 0),
            ('clones-fact', 'file', file_rows, all_paths, 1)):
        inv = {'schemaVersion': 1, 'planId': plan_id, 'parameterDigest': enum_plan_dig,
               'cellOrdinal': cell_ord[cap_id], 'programOrdinal': prog, 'kind': kind,
               'state': 'complete', 'deficiency': None, 'nativeCause': None,
               'examinedPaths': sorted(examined, key=lambda s: K.C(s)), 'rows': rows}
        b.admit(B.SUBJ_INV_DOC, '#', inv,
                'subject-inventory:%s:%s:%d' % (cap_id, kind, prog))
        d = st.put_record(inv, label='subject-inventory:%s:%s:%d' % (cap_id, kind, prog))
        inventories.append((d, inv))

    # ONE VIEW PER UNIVERSE (execution-inputs section 5). Each view carries only the scopes,
    # facts and Coverage of its own universe, so a cell/program binding fixed at one
    # universe never resolves a foreign-universe Coverage through its account derivation.
    views_by_uni = {}
    for uni_hex, part in sorted(g['view_parts_by_universe'].items()):
        facts_here = [fid for fid, f in g['facts'].items() if f['sourceUniverse'] == uni_hex]
        views_by_uni[uni_hex] = b.view(
            plan_id, part['scopes'], facts_here, part['coverages'], cl['provider'],
            [B.doc_sha(B.RELATION_DOC), B.doc_sha(B.NATIVE_DOC)], 'rust:' + uni_hex[:8])
    view_id = views_by_uni[uni_a]
    stage_spec = {'schemaVersion': 2, 'planId': plan_id, 'producerClosure': cl['provider'],
                  'operation': 'rust.analyze.v2',
                  'parameters': [p for p in params
                                 if p['schemaDigest'] == B.doc_sha(B.ENUM_PLAN_DOC)],
                  'outputDomains': sorted(['coverage', 'view'], key=lambda s: K.C(s)),
                  'outputSchemaDigest': B.doc_sha(B.NATIVE_DOC)}
    stage_dig = b.record(B.IDENTITY_DOC, '#/$defs/stage-spec', stage_spec, 'stage-spec')
    exec_plan = {'schemaVersion': 2, 'planId': plan_id,
                 'stages': [{'ordinal': 0, 'stageSpecDigest': stage_dig, 'requires': [],
                             'outputDomains': stage_spec['outputDomains']}]}
    exec_plan_id = b.framed('execution-plan', B.IDENTITY_DOC, '#/$defs/execution-plan',
                            exec_plan, 'execution-plan')

    host_derived = K.cset([{'domain': 'subject-inventory', 'digest': d}
                           for d, _ in inventories])
    stage_out = K.cset([{'domain': 'view', 'digest': st.suffix(v)}
                        for v in views_by_uni.values()]
                       + [{'domain': 'coverage', 'digest': st.suffix(c)}
                          for c in g['view_parts']['coverages']])
    selected = K.cset(stage_out + host_derived)
    rel_for_cap = {'inventory': [('file', 'enumerated'), ('package', 'manifest-declared'),
                                 ('vcs-change', 'vcs-reported')],
                   'syntax': [('declares', 'syntactic'), ('literal', 'syntactic'),
                              ('control-flow', 'syntactic')],
                   'clones-fact': [('clones', 'normalized-body-hash')]}
    cov_by = {}
    for cid in g['view_parts']['coverages']:
        pay = g['coverage_payloads'][cid]
        cov_by[(pay['key']['relation'], pay['key']['resolution'],
                pay['key']['sourceUniverse'])] = st.suffix(cid)
    cell_outcomes, accounts, ordinal = [], [], 0
    for i, c in enumerate(cells):
        for bnd in c['programBindings']:
            uni = bnd['universe']
            invs = sorted([d for d, inv in inventories
                           if inv['cellOrdinal'] == i
                           and inv['programOrdinal'] == bnd['ordinal']],
                          key=lambda s: K.C(s))
            cell_outcomes.append({
                'ordinal': ordinal, 'cellOrdinal': i, 'programOrdinal': bnd['ordinal'],
                'capabilityId': c['capabilityId'], 'languageMode': c['languageMode'],
                'workspaceRoot': c['workspaceRoot'], 'required': c['required'],
                'kinds': c['kinds'], 'universe': uni, 'enumeratorStatus': 'selected',
                'enumeratorClosure': cl['provider'], 'state': 'complete',
                'deficiency': None, 'nativeCause': None, 'stageOrdinal': 0,
                'stageOrdinalNullReason': None, 'inventoryDigests': invs,
                # each binding names ONLY its own universe's view
                'viewDigests': [st.suffix(views_by_uni[uni])],
                'candidateResultDigest': None})
            ordinal += 1
            for rel, rung in rel_for_cap[c['capabilityId']]:
                if (rel, rung, uni) in cov_by:
                    accounts.append({'cellOrdinal': i, 'programOrdinal': bnd['ordinal'],
                                     'relation': rel, 'resolution': rung,
                                     'sourceUniverse': uni, 'targetUniverse': uni,
                                     'applicability': 'supported-available',
                                     'coverageIds': [cov_by[(rel, rung, uni)]]})
                elif rel == 'vcs-change':
                    accounts.append({'cellOrdinal': i, 'programOrdinal': bnd['ordinal'],
                                     'relation': rel, 'resolution': rung,
                                     'sourceUniverse': None, 'targetUniverse': None,
                                     'applicability': 'inapplicable-vcs',
                                     'coverageIds': []})
                else:
                    accounts.append({'cellOrdinal': i, 'programOrdinal': bnd['ordinal'],
                                     'relation': rel, 'resolution': rung,
                                     'sourceUniverse': None, 'targetUniverse': None,
                                     'applicability': 'unsupported-typed',
                                     'coverageIds': []})
    exec_inputs = {
        'schemaVersion': 1, 'planId': plan_id, 'executionPlanId': exec_plan_id,
        'evaluatorClosure': cl['evaluator'], 'enumerationPlanDigest': enum_plan_dig,
        'analysisSpecDigest': spec_dig,
        'hostCapture': {'custody': 'host-tcb-evidence-store', 'observation': 'stage-return',
                        'stageReceipts': [{'ordinal': 0, 'stageSpecDigest': stage_dig,
                                           'producerClosure': cl['provider'],
                                           'outputDomains': stage_spec['outputDomains'],
                                           'outputRefs': stage_out, 'state': 'complete',
                                           'unavailableReason': None}],
                        'hostDerivedRefs': host_derived},
        'selectedRefs': selected, 'cellOutcomes': cell_outcomes,
        'nativeCoverageAccounts': accounts, 'candidateResultRefs': [],
    }
    b.admit(B.EXEC_IN_DOC, '#', exec_inputs, 'execution-inputs')
    exec_in_dig = st.put_record(exec_inputs, label='execution-inputs')

    universes = {}
    for hx in (g['uni_a'], g['uni_b'], g['uni_c']):
        universes[hx] = ('native.semantic-universe.rust.v2',
                         st.objects['native.semantic-universe.rust.v2#' + hx])
    inp = E.Inputs(st, plan_id, plan, exec_plan_id, cl['evaluator'], policy, rule_program,
                   waivers, emit, enum_plan, inventories,
                   {v: st.objects[v] for v in views_by_uni.values()},
                   g['facts'], g['scopes'], g['coverages'],
                   g['coverage_payloads'], g['fact_payloads'], universes,
                   {ctx_hex: ('native.context.rust.v2',
                              st.objects['native.context.rust.v2#' + ctx_hex])},
                   exec_inputs, snapshot=g['snapshot'])
    inp.analysis_spec = spec
    out = CO.compose(inp, st, emit, exec_in_dig, snapshot_id)
    TSF.retain_outputs(b, st, out)

    g.update(dict(policy=policy, waivers=waivers, plan=plan, plan_id=plan_id, spec=spec,
                  inventories=inventories, view_id=view_id,
                  views_by_universe=views_by_uni, exec_inputs=exec_inputs,
                  exec_in_dig=exec_in_dig, out=out, inp=inp, enum_plan=enum_plan,
                  emit=emit, rule_program=rule_program))
    g['exhibits'] = exhibits(g)
    return g


def exhibits(g):
    """Measured evidence for each Rust-specific required property."""
    own_a, own_b, own_c = g['own_lib'], g['own_test'], g['own_libonly']
    units = {u['unitId']: u for u in g['units']}
    return {
        'R-RUN-RUST-MIXED-EDITION': {
            'editionMapSize': len(g['editions']),
            'distinctEditions': sorted(set(g['editions'].values())),
            'editionMap': g['editions'],
            'measured': 'more than one edition in one workspace universe'},
        'R-RUN-RUST-LARGE-EDITION-MAP': {
            'crateCount': len(g['editions']),
            'rawMapCanonicalByteLength': len(K.C(g['editions'])),
            'u8ComponentMaximum': 255,
            'whyHashedNotEmbedded': (
                'The inherited FACT-IDENTITY frame gives each component a u8 length, so a '
                'component built by embedding the per-crate map is NOT REPRESENTABLE: this '
                'map alone is %d canonical bytes against a maximum of 255. The bounded '
                'component is the RAW 32 BYTES of SHA-256(C(body-language-version)), whose '
                'dialect member carries only {edition: year}.' % len(K.C(g['editions']))),
            'measuredVersionComponentByteLength': 32},
        'R-RUN-RUST-TARGET-EDITION': {
            'unit': {k: v for k, v in units[g['unit_ids']['test']].items()},
            'packageDefaultForCrateName': g['editions']['app1'],
            'targetEdition': units[g['unit_ids']['test']]['targetEdition'],
            'differs': units[g['unit_ids']['test']]['targetEdition']
                       != g['editions']['app1'],
            'bodyDialectUnderThatSelection': g['body_editions']['b']},
        'R-RUN-RUST-BODY-DIALECT': {
            'law': ('the EFFECTIVE edition of the SELECTED compilation target that owns '
                    'this body path: unit targetEdition when stated, else the universe '
                    'edition map entry for crateName. No fast path: the committed '
                    'SourceUnitOwnershipV1 is required for every Rust clones fact.'),
            'bodyLanguageVersionRecordSelectionA': g['blv']['a'],
            'bodyLanguageVersionRecordSelectionB': g['blv']['b'],
            'fieldsAreCopiedFromTheAdmittedContext': {
                'compilerName': 'const rustc',
                'compilerVersion': 'native-context toolchain.rustcVersion = '
                                   + g['toolchain']['rustcVersion'],
                'compilerBuild': 'native-context toolchain.rustCommitHash = '
                                 + g['toolchain']['rustCommitHash']},
            'excludedByTheBinding': sorted(['targetTriple', 'hostTriple', 'sysrootDigest',
                                            'rustcDevLlvmDigest',
                                            'standardLibraryComponentDigests',
                                            'cargoVersion', 'resolverVersion',
                                            'crateRootPaths', 'editionMapKeys'])},
        'R-RUN-RUST-SAME-FILE-TWO-EDITIONS': {
            'path': g['libp'],
            'selectionA': {'universe': g['uni_a'],
                           'selectedUnitIds': own_a['selectedUnitIds'],
                           'effectiveEdition': g['body_editions']['a'],
                           'bodyIdentity': 'sha256:' + g['bodies']['lib_a']},
            'selectionB': {'universe': g['uni_b'],
                           'selectedUnitIds': own_b['selectedUnitIds'],
                           'effectiveEdition': g['body_editions']['b'],
                           'bodyIdentity': 'sha256:' + g['bodies']['lib_b']},
            'sameBytes': True,
            'bodyIdentitiesDiffer': g['bodies']['lib_a'] != g['bodies']['lib_b'],
            'law': ('"The same physical source path compiled by two targets at two editions '
                    'has a valid form under each. The selection lives inside the record '
                    'whose identity the universe names, so choosing a different target is a '
                    'different sourceUniverse -- two analyses, not two readings of one." '
                    'Both universes are members of this one Run and both name the SAME '
                    'nativeContextId.')},
        'R-RUN-RUST-STABLE-BODY-ON-OWNERSHIP-CHANGE': {
            'path': g['shared'],
            'pairA': {'ownershipIdentity': 'sha256:' + g['own_hex']['a'],
                      'selectedUnitIds': own_a['selectedUnitIds'],
                      'effectiveEdition': g['body_editions']['a'],
                      'bodyIdentity': 'sha256:' + g['bodies']['shared_a']},
            'pairC': {'ownershipIdentity': 'sha256:' + g['own_hex']['c'],
                      'selectedUnitIds': own_c['selectedUnitIds'],
                      'effectiveEdition': g['body_editions']['c'],
                      'bodyIdentity': 'sha256:' + g['bodies']['shared_c']},
            'ownershipSelectionChanged':
                own_a['selectedUnitIds'] != own_c['selectedUnitIds'],
            'ownershipIdentityChanged': g['own_hex']['a'] != g['own_hex']['c'],
            'effectiveDialectUnchanged':
                g['body_editions']['a'] == g['body_editions']['c'],
            'bodyIdentityStable':
                g['bodies']['shared_a'] == g['bodies']['shared_c'],
            'law': ('Selected owners whose effective editions AGREE are admissible -- the '
                    'ordinary shared-file and lib-plus-test-target case. Paths, crate '
                    'names, unit ids and the selection itself ESTABLISH the selection and '
                    'then do not enter the record; what enters is {edition: year}.'),
            'note': ('The third universe (selection {lib, core}) is retained in this export '
                     'as the pair-vector input only. It is referenced by no fact, scope or '
                     'Coverage of this Run, so the closure reports it among unreferenced '
                     'CAS blobs: "Unreferenced CAS blobs are not evaluation inputs."')},
        'R-RUN-RUST-HASH-MARKER': {
            'markerDirectory': g['hash_dir'],
            'inventoriedPaths': sorted([p for p in g['files'] if '#' in p],
                                       key=lambda s: s.encode()),
            'compilationUnitIdentityIsHOverAPublishedPreimage': {
                'domain': 'native.compilation-unit.v1',
                'preimageSelector': 'native-evidence.schemas.v2.json#/$defs/UnitIdentityV1',
                'unitId': g['unit_ids']['lib']},
            'law': ('"not a delimiter label, which could stay injective only by forbidding '
                    'a # in a repository directory that the canonical path contract '
                    'admits."')},
        'R-RUN-RUST-VERSION-COMPONENT': {
            'derivationInputs': {
                'admittedNativeContextDigest': g['ctx_hex'],
                'toolchainRustcVersion': g['toolchain']['rustcVersion'],
                'toolchainRustCommitHash': g['toolchain']['rustCommitHash'],
                'bodyProvenanceOwnershipIdentity': 'sha256:' + g['own_hex']['a'],
                'effectiveEdition': g['body_editions']['a']},
            'recomputedRecord': g['blv']['a'],
            'rawSha256OfCanonicalRecord': K.rec_digest(g['blv']['a']),
            'frameComponentByteLength': 32,
            'retention': 'derived -- closure recomputes it rather than accepting it'},
        'R-NATIVE-PREIMAGE-JOINS': {
            'dependencySourceSetIdentity': 'sha256:' + g['dep_hex'],
            'dependencyFileManifestIdentity': g['man_hex'],
            'dependencyMemberBlobs': [{'path': r['path'], 'sha256': r['contentSha256'],
                                       'byteLength': r['byteLength']}
                                      for r in g['manifest']],
            'unifiedFeaturesIdentity': 'sha256:' + g['feat_hex'],
            'cargoConfigProjectionIdentity': g['cargo_hex'],
            'projectedConfigFileDigest': g['cargo_proj']['projectionSha256'],
            'twoDigestsAreNotInterchangeable': (
                'projectionSha256 is the RAW SHA-256 of the projected .cargo/config.toml '
                'FILE bytes; rust-v2.configProjectionSha256 is the 64-hex suffix of '
                'H(native.cargo-config-projection.v2, CargoConfigProjectionV2) over the '
                'whole record. Measured distinct: %s vs %s.'
                % (g['cargo_proj']['projectionSha256'][:16], g['cargo_hex'][:16])),
            'sourceUnitOwnershipIdentities': {k: 'sha256:' + v
                                              for k, v in g['own_hex'].items()},
            'preparedOutputSetId': None,
            'preparedResolution': 'none',
            'notExercised': ('PreparedOutputSetV3 / AuthorizedExecutionV2 / '
                             'preparedResolution host-prepared and imported-inert are NOT '
                             'exercised by this Run: preparedOutputSetId is null and '
                             'preparedResolution is none, which is the lawful '
                             'unselected-prepared-set state ("an unselected prepared set '
                             'stays absent: bytes in custody do not enter a resolution by '
                             'being in custody").')},
    }


def main():
    g = complete(RR.build())
    out = g['out']
    print('runId', out['runId'], 'verdict', out['proof']['verdict'])
    print('findings', len(out['findings']), 'predicateProofs',
          len(out['proof']['predicateProofs']))
    for rr in out['proof']['ruleResults']:
        print('  %-30s outcome=%-13s findings=%d defs=%s'
              % (rr['ruleId'], rr['outcome'], len(rr['findingIds']),
                 sorted({d['cause'] for d in rr['deficiencies']})))
    c = CL.Closure(g['st'])
    rep = c.close_run(out['runId'], 'rust')
    print('closure admitted', rep['admitted'], 'passed', rep['checksPassed'],
          'n/a', rep['checksNotApplicable'], 'refused', rep['checksRefused'])
    for r in rep['refusals'][:20]:
        print('  REFUSE', r['check'], '|', json.dumps(r['detail'])[:260])


if __name__ == '__main__':
    main()
