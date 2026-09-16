"""Complete positive Rust Run exhibiting PARTIAL ENUMERATION with an EMPTY CLONE VIEW.

  R-RUN-RUST-PARTIAL-EMPTY-CLONES  an empty clone view that must NOT claim complete Coverage
                                   from partial ownership
  R-CLONE-DEFICIENCY-PAIRING       the precise published deficiency / nativeCause pairing
                                   and output projection

Law (identity section 3 / native section 11 / the Rust dialect selectionLaw):
  "`partial` enumeration says the producer did not finish: an owner INSIDE the selected
  scope may exist that was never listed and could contradict a listed one, so NO BODY
  DIALECT IS ADMISSIBLE AT ALL, checked before any row is read ... Partial evidence still
  counts under the existing law rather than voiding a Run: the clones scope mints no body
  identity, its Coverage reports the incompleteness, and the predicate and seal are
  INDETERMINATE rather than a false pass."

Published pairing, from native x-opensip-deficiency-cause-registry:
  deficiency `input-closure-incomplete` carries its cause in `entry.nativeCause`, that cause
  is REQUIRED (a null there "record[s] that a disclosure was owed and not made"), and
  `body-language-owner-unenumerated` is one of its allowed causes -- added precisely for
  this clones ownership state. coverage is `unknown`, never `complete`.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_build as B
import opensip_eval as E
import opensip_compose as CO
import opensip_closure as CL
import opensip_capmanifest as CM
import run_rust as RR
import run_ts_full as TSF

OUT = '/tmp/opensip-design-corrections/consumer-b.v16/output'


def build():
    """Reuse the Rust subject, but commit PARTIAL ownership enumeration and mint no clone
    bodies. Built standalone so the partial ownership record is the only one in the graph."""
    g = RR.build()   # inherits the no-VCS snapshot, so `inapplicable-vcs` is lawful
    b, st = g['b'], g['st']
    # A fresh ownership record over the same units/rows, with enumeration = partial.
    own_partial = {'schemaVersion': 1, 'enumeration': 'partial', 'units': g['units'],
                   'selectedUnitIds': sorted([g['unit_ids']['lib'], g['unit_ids']['bin'],
                                              g['unit_ids']['core']],
                                             key=lambda s: s.encode()),
                   'ownership': g['ownership']}
    own_hex = b.native_framed('native.source-unit-ownership.v1', B.NATIVE_DOC,
                              '#/$defs/SourceUnitOwnershipV1', own_partial,
                              'source-unit-ownership:partial')
    base = st.objects['native.semantic-universe.rust.v2#' + g['uni_a']]
    uni_rec = dict(base, sourceUnitOwnershipId='sha256:' + own_hex)
    uni_hex = b.native_framed('native.semantic-universe.rust.v2', B.NATIVE_DOC,
                              '#/$defs/RustUniverseV2ResolvedInputs', uni_rec,
                              'native-universe:rust:partial')

    # Rebuild facts/scopes/coverage against the PARTIAL universe only. No clones fact is
    # minted at all: the dialect selector refuses before any ownership row is read.
    facts, fact_payloads = {}, {}
    scopes, coverages, coverage_payloads = {}, {}, {}
    sh = g['sh']

    def mk_fact(relation, rung, payload, anchors, label):
        fid = b.fact(g['snapshot_id'], relation, rung, uni_hex, uni_hex,
                     g['closures']['provider'], payload, anchors, 1000000, label + ':partial')
        facts[fid] = st.objects[fid]
        fact_payloads[fid] = payload
        return fid

    def anchor(path, span):
        row = [r for r in sh['inventory'] if r['path'] == path][0]
        return {'path': path, 'blobDigest': row['sha256'],
                'startByte': span[0], 'endByte': span[1]}

    for p in sorted(g['files'], key=lambda s: s.encode()):
        row = [r for r in sh['inventory'] if r['path'] == p][0]
        mk_fact('file', 'enumerated',
                {'path': p, 'contentSha256': row['sha256'], 'byteLength': row['bytes']},
                [], 'file:' + p)
    for sid, (path, qn) in sorted(g['syms'].items()):
        src = g['files'][path]
        mk_fact('declares', 'syntactic',
                {'container': 'rs:' + path, 'declared': sid, 'declarationKind': 'function'},
                [anchor(path, (0, len(src) - 1))], 'declares:' + sid)

    def mk_scope_cov(relation, rung, subjects, label, cov='complete', deficiency=None,
                     native_cause=None, exhaustive=True):
        sid = b.scope(g['snapshot_id'], relation, rung, uni_hex, uni_hex,
                      g['closures']['provider'], subjects, label + ':partial')
        scopes[sid] = st.objects[sid]
        rc = B.rc_not_applicable()
        rc['examinedExhaustive'] = exhaustive
        ent = B.entry(cov, B.closed_world_open(
            ['compilation ownership enumeration is partial: an owner inside the selected '
             'scope may exist that was never listed']),
            deficiency=deficiency, native_cause=native_cause, rc=rc)
        cid = b.coverage(sid, ent, label + ':partial')
        coverages[cid] = st.objects[cid]
        coverage_payloads[cid] = json.loads(
            st.get_blob(st.objects[cid]['payloadDigest']).decode())
        return sid, cid

    all_paths = sorted(g['files'], key=lambda s: s.encode())
    RS = sorted([p for p in all_paths if p.endswith('.rs')], key=lambda s: s.encode())
    s_file, c_file = mk_scope_cov('file', 'enumerated', all_paths, 'file-enumerated')
    s_decl, c_decl = mk_scope_cov('declares', 'syntactic', sorted(g['syms']),
                                  'declares-syntactic')
    # THE EMPTY CLONE VIEW: the scope is the full examined extent, no clones fact exists,
    # and the entry must NOT claim complete Coverage.
    s_clone, c_clone = mk_scope_cov(
        'clones', 'normalized-body-hash', RS, 'clones-partial-empty',
        cov='unknown', deficiency='input-closure-incomplete',
        native_cause='body-language-owner-unenumerated', exhaustive=False)

    g2 = dict(g)
    g2.update(dict(facts=facts, fact_payloads=fact_payloads, scopes=scopes,
                   coverages=coverages, coverage_payloads=coverage_payloads,
                   uni_hex=uni_hex, uni_a=uni_hex, uni_b=uni_hex, uni_c=uni_hex,
                   universe_digests=[uni_hex], own_partial=own_partial,
                   own_partial_hex=own_hex, rs=RS, all_paths=all_paths,
                   view_parts=dict(scopes=[s_file, s_decl, s_clone],
                                   coverages=[c_file, c_decl, c_clone])))
    return g2


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
    ]
    rules.sort(key=lambda r: r['ruleId'].encode())
    return {'schemaFamily': 'opensip.product.policy', 'schemaMajor': 2,
            'gateSeverityAtLeast': 'warning', 'rules': rules}


def complete(g):
    b, st, sh = g['b'], g['st'], g['sh']
    cl, snapshot_id, uni = g['closures'], g['snapshot_id'], g['uni_hex']
    ctx_hex = g['ctx_hex']
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

    all_paths, RS = g['all_paths'], g['rs']
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
        'rows': [{'path': p, 'languageFamily': 'rust', 'unitOrdinal': 0,
                  'membership': ('program-member' if p.endswith('.rs') else 'syntax-only'),
                  'reason': ('deepest-unit-in-language' if p.endswith('.rs')
                             else 'grammar-only')} for p in all_paths],
        'unsupportedFiles': [], 'outsideBoundaryFiles': [], 'erasedFiles': [],
    }
    b.admit(B.NATIVE_DOC, '#/$defs/UnitMembershipV1', membership, 'unit-membership')
    membership_dig = st.put_record(membership, label='unit-membership')

    def binding(extents):
        return {'ordinal': 0, 'provenance': 'default-unit',
                'enumerator': {'status': 'selected', 'closureId': cl['provider']},
                'nativeContextDigest': ctx_hex, 'universe': uni, 'programEntry': None,
                'extents': sorted([{'kind': k, 'paths': sorted(v, key=lambda s: s.encode())}
                                   for k, v in extents.items()],
                                  key=lambda e: e['kind'].encode())}

    cells = [
        {'capabilityId': 'clones-fact', 'languageMode': 'rust-cargo', 'workspaceRoot': '.',
         'required': False, 'kinds': ['file'], 'programBindings': [binding({'file': RS})]},
        {'capabilityId': 'inventory', 'languageMode': 'rust-cargo', 'workspaceRoot': '.',
         'required': True, 'kinds': ['file'],
         'programBindings': [binding({'file': all_paths})]},
        {'capabilityId': 'syntax', 'languageMode': 'rust-cargo', 'workspaceRoot': '.',
         'required': True, 'kinds': ['symbol'], 'programBindings': [binding({'symbol': RS})]},
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
    sym_rows = sorted([
        {'nativeSubjectId': sid, 'kind': 'symbol', 'path': path, 'qualifiedName': qn,
         'subjectLanguage': 'rust', 'exported': 'exported',
         'signatureTokens': ['rust', 'fn', qn, '(', ')'],
         'projections': [{'closureId': cl['detector'],
                          'signatureTokens': ['rust', 'fn', qn, '(', ')']}]}
        for sid, (path, qn) in g['syms'].items()],
        key=lambda r: r['nativeSubjectId'].encode())
    inventories = []
    for cap_id, kind, rows, examined in (('inventory', 'file', file_rows, all_paths),
                                         ('syntax', 'symbol', sym_rows, RS),
                                         ('clones-fact', 'file', rs_rows, RS)):
        inv = {'schemaVersion': 1, 'planId': plan_id, 'parameterDigest': enum_plan_dig,
               'cellOrdinal': cell_ord[cap_id], 'programOrdinal': 0, 'kind': kind,
               'state': 'complete', 'deficiency': None, 'nativeCause': None,
               'examinedPaths': sorted(examined, key=lambda s: K.C(s)), 'rows': rows}
        b.admit(B.SUBJ_INV_DOC, '#', inv, 'subject-inventory:%s:%s' % (cap_id, kind))
        d = st.put_record(inv, label='subject-inventory:%s:%s' % (cap_id, kind))
        inventories.append((d, inv))

    view_id = b.view(plan_id, g['view_parts']['scopes'], list(g['facts']),
                     g['view_parts']['coverages'], cl['provider'],
                     [B.doc_sha(B.RELATION_DOC), B.doc_sha(B.NATIVE_DOC)], 'rust-partial')
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
    stage_out = K.cset([{'domain': 'view', 'digest': st.suffix(view_id)}]
                       + [{'domain': 'coverage', 'digest': st.suffix(c)}
                          for c in g['view_parts']['coverages']])
    selected = K.cset(stage_out + host_derived)
    cov_by = {}
    for cid in g['view_parts']['coverages']:
        pay = g['coverage_payloads'][cid]
        cov_by[(pay['key']['relation'], pay['key']['resolution'])] = st.suffix(cid)
    rel_for_cap = {'inventory': [('file', 'enumerated'), ('package', 'manifest-declared'),
                                 ('vcs-change', 'vcs-reported')],
                   'syntax': [('declares', 'syntactic'), ('literal', 'syntactic'),
                              ('control-flow', 'syntactic')],
                   'clones-fact': [('clones', 'normalized-body-hash')]}
    cell_outcomes, accounts = [], []
    for i, c in enumerate(cells):
        invs = sorted([d for d, inv in inventories if inv['cellOrdinal'] == i],
                      key=lambda s: K.C(s))
        partial_cell = c['capabilityId'] == 'clones-fact'
        cell_outcomes.append({
            'ordinal': i, 'cellOrdinal': i, 'programOrdinal': 0,
            'capabilityId': c['capabilityId'], 'languageMode': c['languageMode'],
            'workspaceRoot': c['workspaceRoot'], 'required': c['required'],
            'kinds': c['kinds'], 'universe': uni, 'enumeratorStatus': 'selected',
            'enumeratorClosure': cl['provider'],
            'state': 'partial' if partial_cell else 'complete',
            'deficiency': 'input-closure-incomplete' if partial_cell else None,
            'nativeCause': 'body-language-owner-unenumerated' if partial_cell else None,
            'stageOrdinal': 0, 'stageOrdinalNullReason': None,
            'inventoryDigests': invs, 'viewDigests': [st.suffix(view_id)],
            'candidateResultDigest': None})
        for rel, rung in rel_for_cap[c['capabilityId']]:
            if (rel, rung) in cov_by:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': uni,
                                 'targetUniverse': uni,
                                 'applicability': 'supported-available',
                                 'coverageIds': [cov_by[(rel, rung)]]})
            elif rel == 'vcs-change':
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'inapplicable-vcs', 'coverageIds': []})
            else:
                accounts.append({'cellOrdinal': i, 'programOrdinal': 0, 'relation': rel,
                                 'resolution': rung, 'sourceUniverse': None,
                                 'targetUniverse': None,
                                 'applicability': 'unsupported-typed', 'coverageIds': []})
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

    inp = E.Inputs(st, plan_id, plan, exec_plan_id, cl['evaluator'], policy, rule_program,
                   waivers, emit, enum_plan, inventories,
                   {view_id: st.objects[view_id]}, g['facts'], g['scopes'], g['coverages'],
                   g['coverage_payloads'], g['fact_payloads'],
                   {uni: ('native.semantic-universe.rust.v2',
                          st.objects['native.semantic-universe.rust.v2#' + uni])},
                   {ctx_hex: ('native.context.rust.v2',
                              st.objects['native.context.rust.v2#' + ctx_hex])},
                   exec_inputs, snapshot=g['snapshot'])
    inp.analysis_spec = spec
    out = CO.compose(inp, st, emit, exec_in_dig, snapshot_id)
    TSF.retain_outputs(b, st, out)
    g.update(dict(policy=policy, plan=plan, plan_id=plan_id, spec=spec, out=out, inp=inp,
                  inventories=inventories, view_id=view_id, exec_inputs=exec_inputs,
                  exec_in_dig=exec_in_dig, enum_plan=enum_plan, emit=emit,
                  rule_program=rule_program, waivers=waivers))
    clone_cov = [cid for cid in g['view_parts']['coverages']
                 if g['coverage_payloads'][cid]['key']['relation'] == 'clones'][0]
    pay = g['coverage_payloads'][clone_cov]
    clone_facts = [f for f in g['facts'].values() if f['relation'] == 'clones']
    g['exhibits'] = {
        'R-RUN-RUST-PARTIAL-EMPTY-CLONES': {
            'ownershipEnumeration': g['own_partial']['enumeration'],
            'selectedUnitIds': g['own_partial']['selectedUnitIds'],
            'clonesFactCount': len(clone_facts),
            'emptyCloneView': len(clone_facts) == 0,
            'cloneScopeSubjectCount': len(pay['entry']['examinedUniverse']),
            'coverageClaim': pay['entry']['coverage'],
            'coverageIsNotComplete': pay['entry']['coverage'] != 'complete',
            'examinedExhaustive':
                pay['entry']['resolutionCompleteness']['examinedExhaustive'],
            'predicateValues': sorted({pp['value'] for pp in out['proof']['predicateProofs']
                                       if pp['ruleId'] == 'rule.a-no-clone-in-crates'}),
            'gatingRuleOutcome': [rr['outcome'] for rr in out['proof']['ruleResults']
                                  if rr['ruleId'] == 'rule.a-no-clone-in-crates'][0],
            'sealedVerdict': out['proof']['verdict'],
            'law': ('partial ownership enumeration admits NO body dialect at all, checked '
                    'before any row is read; the clones scope mints no body identity, its '
                    'Coverage reports the incompleteness, and the predicate and seal are '
                    'INDETERMINATE rather than a false pass.')},
        'R-CLONE-DEFICIENCY-PAIRING': {
            'coverageEntry': {'coverage': pay['entry']['coverage'],
                              'deficiency': pay['entry']['deficiency'],
                              'nativeCause': pay['entry']['nativeCause']},
            'registrySelector': ('native/native-evidence.schemas.v2.json'
                                 '#/x-opensip-deficiency-cause-registry/deficiencies/'
                                 'input-closure-incomplete'),
            'carrier': 'entry.nativeCause',
            'nativeCauseMode': 'required',
            'nativeCauseIsAnAllowedMember': True,
            'outputProjection': {
                'cellOutcomeState': 'partial',
                'cellOutcomeDeficiency': 'input-closure-incomplete',
                'cellOutcomeNativeCause': 'body-language-owner-unenumerated',
                'requiredCell': False,
                'executionDeficiencies': out['proof']['executionDeficiencies'],
                'note': ('the clones cell is required=false here, so the 9.6 '
                         'required-execution bridge emits no row; the disclosure travels on '
                         'the Coverage entry and the atom deficiency instead. A null '
                         'nativeCause on this deficiency would record a disclosure that was '
                         'owed and not made, and the closure refuses it.')}},
    }
    return g


def main():
    g = complete(build())
    out = g['out']
    print('runId', out['runId'], 'verdict', out['proof']['verdict'])
    for rr in out['proof']['ruleResults']:
        print('  %-30s outcome=%-14s defs=%s' % (rr['ruleId'], rr['outcome'],
                                                 sorted({d['cause']
                                                         for d in rr['deficiencies']})))
    print(json.dumps(g['exhibits']['R-RUN-RUST-PARTIAL-EMPTY-CLONES'], indent=1))
    c = CL.Closure(g['st'])
    rep = c.close_run(out['runId'], 'rust-partial')
    print('closure admitted', rep['admitted'], 'passed', rep['checksPassed'],
          'refused', rep['checksRefused'])
    for r in rep['refusals'][:20]:
        print('  REFUSE', r['check'], '|', json.dumps(r['detail'])[:240])


if __name__ == '__main__':
    main()
